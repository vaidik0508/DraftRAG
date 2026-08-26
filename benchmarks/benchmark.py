#!/usr/bin/env python3
"""Benchmark DraftRAG against Azure OpenAI baselines."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import random
import re
import ssl
import statistics
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
CORPORA = ROOT / "corpora"
DATASET = ROOT / "datasets" / "pilot.jsonl"
ARTIFACTS = ROOT / "artifacts"
RUNS = ROOT / "runs"
SCORECARD_VERSION = 3
PLACEHOLDER = re.compile(r"\[\[RETRIEVE:\s*(\{.*?\})\s*\]\]", re.DOTALL)
WORD = re.compile(r"[a-z0-9]+")


def load_dotenv(path=REPO / ".env"):
    if not path.exists():
        return
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[7:].lstrip()
        name, value = line.split("=", 1)
        os.environ.setdefault(name.strip(), value.strip().strip("\"'"))


def json_from_text(text):
    fenced = re.search(r"```(?:json)?\s*(.*?)```", text, re.I | re.S)
    return json.loads((fenced.group(1) if fenced else text).strip())


def percentile(values, fraction):
    ordered = sorted(values)
    return ordered[round((len(ordered) - 1) * fraction)] if ordered else None


class AzureClient:
    def __init__(self):
        load_dotenv()
        required = ("AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_API_KEY", "AZURE_OPENAI_DEPLOYMENT_NAME")
        missing = [name for name in required if not os.environ.get(name)]
        if missing:
            raise SystemExit("Missing Azure setting(s): " + ", ".join(missing))
        base = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")
        self.base = base if base.endswith("/openai/v1") else base + "/openai/v1"
        self.key = os.environ["AZURE_OPENAI_API_KEY"]
        self.model = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
        self.embedding_model = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME", "").strip()
        ca = Path("/etc/ssl/cert.pem")
        self.context = ssl.create_default_context(cafile=str(ca) if ca.exists() else None)
        self.events = []

    def _post(self, path, body, kind):
        last_error = None
        for attempt in range(1, 4):
            request = urllib.request.Request(
                self.base + path,
                data=json.dumps(body).encode(),
                headers={"api-key": self.key, "Content-Type": "application/json"},
                method="POST",
            )
            started = time.perf_counter()
            try:
                with urllib.request.urlopen(request, timeout=240, context=self.context) as response:
                    data = json.load(response)
                    request_id = response.headers.get("x-request-id")
                break
            except urllib.error.HTTPError as error:
                detail = error.read().decode(errors="replace")
                last_error = RuntimeError(f"Azure OpenAI error {error.code}: {detail}")
                if error.code != 429 and error.code < 500:
                    raise last_error from error
            except urllib.error.URLError as error:
                last_error = RuntimeError(f"Azure connection error: {error.reason}")
            print(f"  transient Azure failure; retry {attempt}/3", flush=True)
            if attempt < 3:
                time.sleep(attempt)
        else:
            raise last_error
        elapsed = (time.perf_counter() - started) * 1000
        usage = data.get("usage") or {}
        self.events.append({
            "kind": kind,
            "latency_ms": round(elapsed, 2),
            "input_tokens": usage.get("input_tokens", usage.get("prompt_tokens", 0)) or 0,
            "output_tokens": usage.get("output_tokens", usage.get("completion_tokens", 0)) or 0,
            "total_tokens": usage.get("total_tokens", 0) or 0,
            "request_id": request_id,
            "model": data.get("model"),
            "request_input_chars": len(json.dumps(body, ensure_ascii=False)),
        })
        return data

    def complete(self, prompt, kind="answer"):
        data = self._post("/responses", {"model": self.model, "input": prompt, "store": False}, kind)
        texts = [
            item.get("text", "")
            for output in data.get("output", [])
            for item in output.get("content", [])
            if item.get("type") == "output_text"
        ]
        if not texts:
            raise RuntimeError("Azure response contained no output_text")
        return "".join(texts).strip()

    def embed(self, texts):
        if not self.embedding_model:
            raise RuntimeError("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME is not configured")
        data = self._post("/embeddings", {"model": self.embedding_model, "input": texts}, "embedding")
        return [row["embedding"] for row in sorted(data["data"], key=lambda row: row["index"])]

    def mark(self):
        return len(self.events)

    def since(self, mark):
        events = self.events[mark:]
        return {
            "calls": len(events),
            "llm_calls": sum(e["kind"] != "embedding" for e in events),
            "embedding_calls": sum(e["kind"] == "embedding" for e in events),
            "input_tokens": sum(e["input_tokens"] for e in events),
            "output_tokens": sum(e["output_tokens"] for e in events),
            "total_tokens": sum(e["total_tokens"] for e in events),
            "api_latency_ms": round(sum(e["latency_ms"] for e in events), 2),
            "request_input_chars": sum(e["request_input_chars"] for e in events),
            "models": sorted({e["model"] for e in events if e["model"]}),
        }


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def chunks_for(corpus):
    return read_jsonl(CORPORA / corpus / "chunks.jsonl")


def cosine(a, b):
    denominator = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(x * x for x in b))
    return sum(x * y for x, y in zip(a, b)) / denominator if denominator else 0.0


def bm25_rank(query, chunks, k=5, k1=1.5, b=0.75):
    docs = [WORD.findall(c["text"].lower()) for c in chunks]
    qterms = WORD.findall(query.lower())
    average = sum(map(len, docs)) / len(docs)
    scored = []
    for chunk, tokens in zip(chunks, docs):
        counts = Counter(tokens)
        score = 0.0
        for term in set(qterms):
            df = sum(term in doc for doc in docs)
            idf = math.log(1 + (len(docs) - df + 0.5) / (df + 0.5))
            tf = counts[term]
            if tf:
                score += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * len(tokens) / average))
        scored.append((score, chunk))
    return [chunk for _, chunk in sorted(scored, key=lambda item: item[0], reverse=True)[:k]]


def evidence_text(chunks):
    return "\n\n".join(f"[{c['id']}] {c['text']}" for c in chunks)


def answer_prompt(question, evidence=None, no_source=False):
    if no_source:
        return f"Answer concisely. You have no source document. Do not invent fictional handbook facts; say information is unavailable when needed.\n\nQUESTION:\n{question}"
    return f"""Answer the QUESTION using only SOURCE. Include every requested fact, resolve conflicts using the exact named simulation or product version, and say the source does not specify an answer when absent. Do not mention retrieval or chunk IDs.

SOURCE:
{evidence}

QUESTION:
{question}"""


def make_dimensions(client, corpus, chunks, dimensions=10):
    folder = ARTIFACTS / corpus
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "scorecard.json"
    if path.exists():
        cached = json.loads(path.read_text())
        if cached.get("scorecard_version") == SCORECARD_VERSION:
            return cached["dimensions"]
    prompt = f"""Design exactly {dimensions} reusable semantic scoring dimensions for retrieving from this corpus. A general LLM will score chunks and queries independently from 0.0 to 1.0. Cover recurring topics, identity/version, rules, procedures, measurements, and exceptions. Avoid dimensions tied to one fact.

CRITICAL: define ABSOLUTE, QUERY-INDEPENDENT properties. Never define "matches the query", "requested entity", "relevance", or "answer completeness" because source chunks are indexed before a query exists. Each axis must be meaningful when either a chunk or query is scored alone.

Every dimension must DISCRIMINATE recurring concepts inside this corpus. Generic presence
axes such as "contains an entity", "has a version", "contains a rule", or "has a number"
are invalid because unrelated chunks receive the same score. Use topic, family, context,
or process affinities whose anchors state which recurring semantic region is expressed.
A 1.0 should apply to a focused subset, not nearly every chunk, and a typical chunk should
strongly activate only a few dimensions.

Define anchors 0.0, 0.25, 0.50, 0.75, and 1.0. Reserve 0.0 for complete absence or opposition and 1.0 for direct, central expression. Partial anchors must be meaningfully distinct, while absent properties must remain zero.

Return ONLY JSON: {{"dimensions":[{{"index":0,"name":"short","definition":"absolute property","anchors":{{"0.0":"absent","0.25":"weak/incidental","0.50":"meaningful partial","0.75":"strong but incomplete","1.0":"direct and central"}},"guideline":"score chunks and queries independently"}}]}}. Indices must be 0 through {dimensions - 1}.

CORPUS:
{evidence_text(chunks)}"""
    data = json_from_text(client.complete(prompt, "index_rules"))
    dims = data["dimensions"]
    if len(dims) != dimensions or [d.get("index") for d in dims] != list(range(dimensions)):
        raise RuntimeError(f"Invalid scorecard for {corpus}")
    required_anchors = {"0.0", "0.25", "0.50", "0.75", "1.0"}
    if any(not d.get("definition") or set(d.get("anchors", {})) != required_anchors for d in dims):
        raise RuntimeError(f"Scorecard for {corpus} omitted absolute partial-value anchors")
    path.write_text(json.dumps({"scorecard_version": SCORECARD_VERSION, "corpus": corpus, "dimensions": dims}, indent=2) + "\n")
    return dims


def validate_vectors(rows, expected_ids, dimensions):
    by_id = {str(row["id"]): row["vector"] for row in rows}
    if set(by_id) != set(expected_ids):
        raise RuntimeError("Vector response omitted or added IDs")
    for vector in by_id.values():
        if len(vector) != dimensions or any(float(v) < 0 or float(v) > 1 for v in vector):
            raise RuntimeError("Invalid semantic vector")
    return {key: [float(v) for v in value] for key, value in by_id.items()}


def score_batch(client, dims, items, kind, attempts=3):
    role_instruction = (
        "For every source chunk, score what it explicitly contains or strongly implies."
        if kind == "index_score"
        else "For every query, score the semantic properties and evidence needs it expresses."
    )
    prompt = f"""Score each TEXT against SCORECARD. Return ONLY JSON: {{"items":[{{"id":"same id","vector":[numbers]}}]}}. Each vector has exactly {len(dims)} values in index order, each 0.0 to 1.0. Judge explicit meaning; do not invent facts.

{role_instruction} Treat dimensions as absolute axes, never as relevance to another item.
Use 0.25 for weak/incidental evidence, 0.50 for meaningful partial evidence, and 0.75 for
strong but incomplete evidence. Use 0.0 only when an axis is truly absent or opposed and
1.0 only when direct, central, and unambiguous. Do not force nonzero values for absent
properties. Values between anchors are allowed when justified. Score every item
independently; other items in this batch are not references.

SCORECARD:
{json.dumps(dims)}

ITEMS:
{json.dumps(items)}"""
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            rows = json_from_text(client.complete(prompt, kind))["items"]
            return validate_vectors(rows, [str(item["id"]) for item in items], len(dims))
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
            last_error = error
            print(f"  invalid {kind} JSON; retry {attempt}/{attempts}", flush=True)
    raise RuntimeError(f"Invalid structured response after {attempts} attempts: {last_error}")


def make_semantic_index(client, corpus, chunks, dims):
    path = ARTIFACTS / corpus / "semantic_index.json"
    partial_path = ARTIFACTS / corpus / "semantic_index.partial.json"
    fingerprint = hashlib.sha256(json.dumps({"scorecard_version": SCORECARD_VERSION, "chunks": chunks, "dimensions": dims}, sort_keys=True).encode()).hexdigest()
    if path.exists():
        data = json.loads(path.read_text())
        if data.get("fingerprint") == fingerprint:
            validate_semantic_index(data["chunks"])
            return data["chunks"]
    vectors = {}
    if partial_path.exists():
        partial = json.loads(partial_path.read_text())
        if partial.get("fingerprint") == fingerprint:
            vectors = partial.get("vectors", {})
    for start in range(0, len(chunks), 10):
        batch = chunks[start:start + 10]
        if all(chunk["id"] in vectors for chunk in batch):
            continue
        print(f"  scoring {corpus} chunks {start + 1}-{start + len(batch)}", flush=True)
        items = [{"id": c["id"], "text": c["text"]} for c in batch]
        vectors.update(score_batch(client, dims, items, "index_score"))
        partial_path.write_text(json.dumps({"fingerprint": fingerprint, "vectors": vectors}) + "\n")
    records = [{**chunk, "vector": vectors[chunk["id"]]} for chunk in chunks]
    validate_semantic_index(records)
    path.write_text(json.dumps({"fingerprint": fingerprint, "chunks": records}, indent=2) + "\n")
    partial_path.unlink(missing_ok=True)
    return records


def validate_semantic_index(records):
    vectors = [tuple(record["vector"]) for record in records]
    zero_count = sum(not any(vector) for vector in vectors)
    unique_count = len(set(vectors))
    most_common_count = max(Counter(vectors).values(), default=0)
    dimensions = len(vectors[0]) if vectors else 0
    minimum_unique = min(len(vectors), max(3, dimensions))
    if zero_count > max(1, math.floor(len(vectors) * 0.10)):
        raise RuntimeError(
            f"Semantic index collapsed: {zero_count}/{len(vectors)} all-zero vectors; "
            "regenerate the absolute partial-anchor scorecard"
        )
    if unique_count < minimum_unique:
        raise RuntimeError(
            f"Semantic index collapsed: only {unique_count}/{len(vectors)} unique vectors"
        )
    if most_common_count > max(2, math.ceil(len(vectors) * 0.25)):
        print(
            f"Warning: one semantic vector is shared by {most_common_count}/{len(vectors)} "
            "chunks; exact retrieval inside that class may need more dimensions.",
            flush=True,
        )


def make_embedding_index(client, corpus, chunks):
    safe_model = re.sub(r"[^a-zA-Z0-9_.-]+", "_", client.embedding_model)
    path = ARTIFACTS / corpus / f"embedding_index_{safe_model}.json"
    fingerprint = hashlib.sha256(json.dumps(chunks, sort_keys=True).encode()).hexdigest()
    if path.exists():
        data = json.loads(path.read_text())
        if data.get("fingerprint") == fingerprint:
            return data["chunks"]
    vectors = []
    for start in range(0, len(chunks), 32):
        vectors.extend(client.embed([c["text"] for c in chunks[start:start + 32]]))
    records = [{**chunk, "vector": vector} for chunk, vector in zip(chunks, vectors)]
    path.write_text(json.dumps({"fingerprint": fingerprint, "model": client.embedding_model, "chunks": records}) + "\n")
    return records


def draftrag_prompt(question, dims, draft=None, evidence=None):
    prior = "" if draft is None else f"\nCURRENT DRAFT:\n{draft}\n"
    bank = "" if not evidence else f"\nCUMULATIVE SOURCE EVIDENCE:\n{evidence_text(evidence)}\n"
    phase = "Write an answer draft now." if draft is None else "Rewrite the entire draft using evidence."
    return f"""You are an iterative answer writer. {phase} Never output a plan. Where a source fact is still needed, put this exact inline form where needed: [[RETRIEVE: {{"query":"standalone semantic search description","vector":[0.25,0.75]}}]]. The vector must contain exactly {len(dims)} scores from 0.0 to 1.0 in scorecard index order. Use partial values 0.25, 0.50, and 0.75 whenever an evidence need is weak, meaningful-but-partial, or strong-but-incomplete. Reserve 0.0 for an axis not needed and 1.0 for a direct central requirement; do not default most coordinates to binary endpoints and do not make absent axes nonzero. Multiple placeholders are allowed. Do not guess source facts. If evidence fully answers the question, return a concise final answer with no placeholders. If the source lacks a requested fact, explicitly say it is not specified after checking available evidence. Do not expose retrieval.

SCORECARD:
{json.dumps(dims)}

QUESTION:
{question}
{prior}{bank}"""


def run_draftrag(client, question, dims, index, top_k=5, max_passes=4):
    draft = None
    evidence = {}
    trace = []
    retrieved = []
    converged = False
    source_context_chars_delivered = 0
    inline_evidence_chars = 0
    for pass_number in range(1, max_passes + 1):
        bank_chars = sum(len(row["text"]) for row in evidence.values())
        source_context_chars_delivered += bank_chars + inline_evidence_chars
        prompt = draftrag_prompt(question, dims, draft, list(evidence.values()))
        raw = client.complete(prompt, "draft")
        matches = list(PLACEHOLDER.finditer(raw))
        pass_info = {
            "pass": pass_number, "draft": raw, "queries": [], "retrieved": [], "events": [],
            "source_context_chars": bank_chars + inline_evidence_chars,
            "evidence_bank_chars": bank_chars,
            "inline_evidence_chars": inline_evidence_chars,
        }
        if not matches:
            draft, converged = raw, True
            trace.append(pass_info)
            break
        query_items = []
        for position, match in enumerate(matches):
            payload = json.loads(match.group(1))
            query_items.append({"id": str(position), "text": payload["query"]})
        vectors = score_batch(client, dims, query_items, "query_score")
        pieces, cursor = [], 0
        next_inline_evidence_chars = 0
        for position, match in enumerate(matches):
            query = query_items[position]["text"]
            query_vector = vectors[str(position)]
            ranked = [] if not any(query_vector) else sorted(
                ((cosine(query_vector, row["vector"]), row) for row in index),
                key=lambda pair: pair[0], reverse=True,
            )[:top_k]
            hits = [row for _, row in ranked]
            ids = [row["id"] for row in hits]
            pass_info["queries"].append(query)
            pass_info["retrieved"].append(ids)
            pass_info["events"].append({
                "event": position,
                "query": query,
                "hits": [
                    {"chunk_id": row["id"], "score": round(score, 6), "chars": len(row["text"])}
                    for score, row in ranked
                ],
                "new_chunk_ids": [row["id"] for row in hits if row["id"] not in evidence],
            })
            retrieved.extend(ids)
            for row in hits:
                evidence[row["id"]] = row
                next_inline_evidence_chars += len(row["text"])
            pieces.append(raw[cursor:match.start()])
            pieces.append("\n" + evidence_text(hits) + "\n")
            cursor = match.end()
        pieces.append(raw[cursor:])
        draft = "".join(pieces)
        inline_evidence_chars = next_inline_evidence_chars
        trace.append(pass_info)
    if not converged:
        source_context_chars_delivered += sum(len(row["text"]) for row in evidence.values())
        draft = client.complete(answer_prompt(question, evidence_text(list(evidence.values()))), "forced_final")
    queries = [query for step in trace for query in step["queries"]]
    return draft, retrieved, {
        "passes": len(trace), "converged": converged, "trace": trace,
        "retrieval_events": len(queries), "queries": queries,
        "source_context_chars_delivered": source_context_chars_delivered,
    }


def alias_present(answer, alias):
    normalized = " ".join(WORD.findall(answer.lower()))
    target = " ".join(WORD.findall(alias.lower()))
    return bool(re.search(r"(?:^| )" + re.escape(target) + r"(?: |$)", normalized))


def score_answer(item, answer, retrieved):
    passed = [any(alias_present(answer, alias) for alias in aliases) for aliases in item["claims"]]
    gold, found = set(item["gold_chunk_ids"]), set(retrieved)
    answer_words = len(WORD.findall(answer))
    return {
        "claim_hits": sum(passed), "claim_total": len(passed),
        "claim_recall": round(sum(passed) / len(passed), 4), "all_claims": all(passed),
        "gold_chunk_hits": len(gold & found), "gold_chunk_total": len(gold),
        "gold_chunk_recall": round(len(gold & found) / len(gold), 4) if gold else None,
        "all_gold_chunks": gold.issubset(found) if gold else None,
        "answer_word_count": answer_words,
        "answer_detail_density": round(sum(passed) * 100 / answer_words, 4) if answer_words else 0.0,
        "rich_question": item["category"] in {"multi_aspect", "sequential_multi_hop", "version_conflict"},
    }


def query_diversity(queries):
    token_sets = [set(WORD.findall(query.lower())) for query in queries]
    if len(token_sets) < 2:
        return 0.0
    distances = []
    for left in range(len(token_sets)):
        for right in range(left + 1, len(token_sets)):
            union = token_sets[left] | token_sets[right]
            similarity = len(token_sets[left] & token_sets[right]) / len(union) if union else 1.0
            distances.append(1 - similarity)
    return round(statistics.mean(distances), 4)


def retrieval_metrics(item, chunks, retrieved, metadata):
    by_id = {chunk["id"]: chunk for chunk in chunks}
    gold = set(item["gold_chunk_ids"])
    unique_ids = list(dict.fromkeys(retrieved))
    found_gold = gold & set(unique_ids)
    unique_chars = sum(len(by_id[chunk_id]["text"]) for chunk_id in unique_ids)
    useful_chars = sum(len(by_id[chunk_id]["text"]) for chunk_id in found_gold)
    total_chars = sum(len(by_id[chunk_id]["text"]) for chunk_id in retrieved)
    trace = metadata.get("trace", [])
    first_ids = set(
        chunk_id
        for group in (trace[0].get("retrieved", []) if trace else [])
        for chunk_id in group
    )
    later_ids = set(
        chunk_id
        for step in trace[1:]
        for group in step.get("retrieved", [])
        for chunk_id in group
    )
    trace_queries = [query for step in trace for query in step.get("queries", [])]
    queries = metadata.get("queries") or trace_queries
    retrieval_events = metadata.get("retrieval_events", len(queries) if queries else (1 if retrieved else 0))
    useful_events = 0
    if trace:
        useful_events = sum(
            bool(gold & set(group))
            for step in trace
            for group in step.get("retrieved", [])
        )
    elif retrieved:
        useful_events = int(bool(found_gold))
    if "source_context_chars_delivered" in metadata:
        source_delivered = metadata["source_context_chars_delivered"]
    elif trace:
        evidence_ids = set()
        inline_chars = 0
        source_delivered = 0
        for step in trace:
            source_delivered += sum(len(by_id[chunk_id]["text"]) for chunk_id in evidence_ids) + inline_chars
            groups = step.get("retrieved", [])
            inline_chars = sum(len(by_id[chunk_id]["text"]) for group in groups for chunk_id in group)
            evidence_ids.update(chunk_id for group in groups for chunk_id in group)
        if not metadata.get("converged", True):
            source_delivered += sum(len(by_id[chunk_id]["text"]) for chunk_id in evidence_ids)
    else:
        source_delivered = unique_chars
    return {
        "retrieval_events": retrieval_events,
        "useful_retrieval_events": useful_events,
        "placeholder_precision": round(useful_events / retrieval_events, 4) if retrieval_events else None,
        "retrieved_chunks_total": len(retrieved),
        "retrieved_chunks_unique": len(unique_ids),
        "redundant_retrieval_rate": round(1 - len(unique_ids) / len(retrieved), 4) if retrieved else 0.0,
        "useful_chunks_unique": len(found_gold),
        "irrelevant_chunks_unique": len(set(unique_ids) - gold),
        "retrieval_precision_unique": round(len(found_gold) / len(unique_ids), 4) if unique_ids else None,
        "retrieved_context_chars_total": total_chars,
        "retrieved_context_chars_unique": unique_chars,
        "useful_context_chars": useful_chars,
        "irrelevant_context_chars": unique_chars - useful_chars,
        "context_bloat_ratio": round((unique_chars - useful_chars) / unique_chars, 4) if unique_chars else None,
        "source_context_chars_delivered": source_delivered,
        "source_context_duplication_ratio": round(1 - unique_chars / source_delivered, 4) if source_delivered else 0.0,
        "late_gold_chunks": len((later_ids - first_ids) & gold),
        "late_gold_discovery": round(len((later_ids - first_ids) & gold) / len(gold), 4) if gold else None,
        "query_count": len(queries) if queries else retrieval_events,
        "unique_query_count": len(set(query.lower().strip() for query in queries)) if queries else retrieval_events,
        "query_diversity": query_diversity(queries),
    }


def run_system(client, system, item, resources, top_k, max_passes):
    chunks, retrieved, metadata = resources["chunks"], [], {}
    if system == "llm_only":
        answer = client.complete(answer_prompt(item["question"], no_source=True))
    elif system == "long_context":
        retrieved = [c["id"] for c in chunks]
        answer = client.complete(answer_prompt(item["question"], evidence_text(chunks)))
    elif system == "bm25_rag":
        hits = bm25_rank(item["question"], chunks, top_k)
        retrieved = [c["id"] for c in hits]
        answer = client.complete(answer_prompt(item["question"], evidence_text(hits)))
    elif system == "embedding_rag":
        vector = client.embed([item["question"]])[0]
        ranked = sorted(
            ((cosine(vector, row["vector"]), row) for row in resources["embedding_index"]),
            key=lambda pair: pair[0], reverse=True,
        )[:top_k]
        hits = [row for _, row in ranked]
        retrieved = [c["id"] for c in hits]
        metadata = {
            "retrieval_events": 1,
            "queries": [item["question"]],
            "source_context_chars_delivered": sum(len(c["text"]) for c in hits),
            "trace": [{
                "pass": 1,
                "queries": [item["question"]],
                "retrieved": [retrieved],
                "events": [{
                    "event": 0,
                    "query": item["question"],
                    "hits": [
                        {"chunk_id": row["id"], "score": round(score, 6), "chars": len(row["text"])}
                        for score, row in ranked
                    ],
                    "new_chunk_ids": retrieved,
                }],
            }],
        }
        answer = client.complete(answer_prompt(item["question"], evidence_text(hits)))
    elif system == "draftrag":
        answer, retrieved, metadata = run_draftrag(client, item["question"], resources["dims"], resources["semantic_index"], top_k, max_passes)
    else:
        raise ValueError(system)
    return answer, retrieved, metadata


def summarize(rows, skipped, index_metrics):
    summary = {"systems": {}, "skipped": skipped, "index_build": index_metrics}
    for system in sorted({row["system"] for row in rows}):
        group = [row for row in rows if row["system"] == system and not row.get("error")]
        if not group:
            summary["systems"][system] = {"questions": 0, "error": "all runs failed"}
            continue
        retrieval = [row["gold_chunk_recall"] for row in group if row["gold_chunk_recall"] is not None]
        rich = [row for row in group if row["rich_question"]]
        answerable = [row for row in group if row["gold_chunk_total"] > 0]
        summary["systems"][system] = {
            "questions": len(group),
            "mean_claim_recall": round(statistics.mean(row["claim_recall"] for row in group), 4),
            "all_claims_rate": round(statistics.mean(row["all_claims"] for row in group), 4),
            "mean_gold_chunk_recall": round(statistics.mean(retrieval), 4) if retrieval else None,
            "mean_latency_ms": round(statistics.mean(row["wall_latency_ms"] for row in group), 2),
            "p50_latency_ms": round(percentile([row["wall_latency_ms"] for row in group], .5), 2),
            "p95_latency_ms": round(percentile([row["wall_latency_ms"] for row in group], .95), 2),
            "mean_calls": round(statistics.mean(row["calls"] for row in group), 2),
            "total_tokens": sum(row["total_tokens"] for row in group),
            "convergence_rate": round(statistics.mean(row["metadata"].get("converged", False) for row in group), 4) if system == "draftrag" else None,
            "mean_passes": round(statistics.mean(row["metadata"].get("passes", 0) for row in group), 2) if system == "draftrag" else None,
            "mean_retrieval_precision_unique": round(statistics.mean(row["retrieval_precision_unique"] for row in group if row["retrieval_precision_unique"] is not None), 4),
            "mean_context_bloat_ratio": round(statistics.mean(row["context_bloat_ratio"] for row in group if row["context_bloat_ratio"] is not None), 4),
            "mean_source_context_chars_delivered": round(statistics.mean(row["source_context_chars_delivered"] for row in group), 2),
            "mean_unique_chunks": round(statistics.mean(row["retrieved_chunks_unique"] for row in group), 2),
            "mean_total_chunks": round(statistics.mean(row["retrieved_chunks_total"] for row in group), 2),
            "mean_irrelevant_chunks": round(statistics.mean(row["irrelevant_chunks_unique"] for row in group), 2),
            "mean_redundant_retrieval_rate": round(statistics.mean(row["redundant_retrieval_rate"] for row in group), 4),
            "mean_source_duplication_ratio": round(statistics.mean(row["source_context_duplication_ratio"] for row in group), 4),
            "mean_retrieval_events": round(statistics.mean(row["retrieval_events"] for row in group), 2),
            "mean_placeholder_precision": round(statistics.mean(row["placeholder_precision"] for row in group if row["placeholder_precision"] is not None), 4),
            "mean_late_gold_discovery": round(statistics.mean(row["late_gold_discovery"] for row in group if row["late_gold_discovery"] is not None), 4),
            "mean_query_diversity": round(statistics.mean(row["query_diversity"] for row in group), 4),
            "mean_answer_claims": round(statistics.mean(row["claim_hits"] for row in group), 2),
            "mean_answer_words": round(statistics.mean(row["answer_word_count"] for row in group), 2),
            "mean_answer_detail_density": round(statistics.mean(row["answer_detail_density"] for row in group), 4),
            "rich_question_claim_recall": round(statistics.mean(row["claim_recall"] for row in rich), 4) if rich else None,
            "rich_question_complete_rate": round(statistics.mean(row["all_claims"] for row in rich), 4) if rich else None,
            "complete_evidence_rate": round(statistics.mean(row["all_gold_chunks"] for row in answerable), 4) if answerable else None,
        }
    return summary


def write_report(run_dir, summary, args):
    title = "Embedding RAG vs DraftRAG" if set(summary["systems"]) == {"embedding_rag", "draftrag"} else "DraftRAG validation run"
    lines = [f"# {title}", "", f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S %z')}", "", f"Configuration: top-k={args.top_k}, max DraftRAG passes={args.max_passes}, seed={args.seed}.", "", "| System | Claim recall | Rich-question recall | Gold-chunk recall | Complete evidence | Retrieval precision | Context bloat | Source chars delivered |", "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for system, values in summary["systems"].items():
        retrieval = "—" if values["mean_gold_chunk_recall"] is None else f"{values['mean_gold_chunk_recall']:.1%}"
        lines.append(f"| {system} | {values['mean_claim_recall']:.1%} | {values['rich_question_claim_recall']:.1%} | {retrieval} | {values['complete_evidence_rate']:.1%} | {values['mean_retrieval_precision_unique']:.1%} | {values['mean_context_bloat_ratio']:.1%} | {values['mean_source_context_chars_delivered']:.0f} |")
    lines += ["", "## Answer richness", "", "| System | Complete answers | Rich-question complete | Mean requested claims answered | Mean answer words | Claims per 100 words |", "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for system, values in summary["systems"].items():
        lines.append(f"| {system} | {values['all_claims_rate']:.1%} | {values['rich_question_complete_rate']:.1%} | {values['mean_answer_claims']:.2f} | {values['mean_answer_words']:.1f} | {values['mean_answer_detail_density']:.2f} |")
    lines += ["", "## On-demand retrieval behavior", "", "| System | Retrieval events | Useful events | Late gold discovery | Query diversity | Total / unique chunks | Irrelevant chunks | Retrieval redundancy | Source duplication | Mean passes |", "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for system, values in summary["systems"].items():
        passes = "—" if values["mean_passes"] is None else f"{values['mean_passes']:.2f}"
        lines.append(f"| {system} | {values['mean_retrieval_events']:.2f} | {values['mean_placeholder_precision']:.1%} | {values['mean_late_gold_discovery']:.1%} | {values['mean_query_diversity']:.1%} | {values['mean_total_chunks']:.2f} / {values['mean_unique_chunks']:.2f} | {values['mean_irrelevant_chunks']:.2f} | {values['mean_redundant_retrieval_rate']:.1%} | {values['mean_source_duplication_ratio']:.1%} | {passes} |")
    lines += ["", "## Query-time efficiency", "", "| System | Mean latency | p95 latency | Mean API calls | Total tokens |", "| --- | ---: | ---: | ---: | ---: |"]
    for system, values in summary["systems"].items():
        lines.append(f"| {system} | {values['mean_latency_ms'] / 1000:.2f}s | {values['p95_latency_ms'] / 1000:.2f}s | {values['mean_calls']:.2f} | {values['total_tokens']} |")
    if summary["skipped"]:
        lines += ["", "## Skipped", ""] + [f"- `{name}`: {reason}" for name, reason in summary["skipped"].items()]
    lines += ["", "## Interpretation limits", "", "This is a small deterministic pilot, not a statistically conclusive result. Claim recall is exact alias matching and does not measure unsupported extra claims. Index-building calls are separate from per-question latency. Inspect `results.jsonl` and DraftRAG traces before drawing conclusions.", ""]
    (run_dir / "REPORT.md").write_text("\n".join(lines))


def write_retrieval_audit(run_dir, rows):
    lines = ["# Retrieval audit", "", "Every retrieval query, pass, ranked chunk, cosine score, and gold-evidence match.", ""]
    primary_rows = (row for row in rows if not row.get("error") and row["system"] in {"embedding_rag", "draftrag"})
    for row in sorted(primary_rows, key=lambda row: (row["question_id"], row["system"])):
        gold = set(row.get("gold_chunk_ids", []))
        lines += [f"## {row['question_id']} — `{row['system']}`", "", f"Question: {row['question']}", ""]
        trace = row.get("metadata", {}).get("trace", [])
        if not trace:
            lines += ["No retrieval trace.", ""]
            continue
        seen_ids = set()
        for step in trace:
            events = step.get("events", [])
            if not events:
                events = []
                fallback_seen = set(seen_ids)
                for event_number, (query, chunk_ids) in enumerate(zip(step.get("queries", []), step.get("retrieved", []))):
                    events.append({
                        "event": event_number,
                        "query": query,
                        "hits": [{"chunk_id": chunk_id, "score": None, "chars": None} for chunk_id in chunk_ids],
                        "new_chunk_ids": [chunk_id for chunk_id in chunk_ids if chunk_id not in fallback_seen],
                    })
                    fallback_seen.update(chunk_ids)
            if not events:
                continue
            lines += [f"### Pass {step['pass']}", ""]
            for event in events:
                lines += [f"Demand {event['event'] + 1}: `{event['query']}`", "", "| Rank | Chunk | Score | Gold | New | Chars |", "| ---: | --- | ---: | :---: | :---: | ---: |"]
                new_ids = set(event.get("new_chunk_ids", []))
                for rank, hit in enumerate(event["hits"], 1):
                    chunk_id = hit["chunk_id"]
                    score = "—" if hit.get("score") is None else f"{hit['score']:.6f}"
                    chars = "—" if hit.get("chars") is None else str(hit["chars"])
                    lines.append(f"| {rank} | `{chunk_id}` | {score} | {'yes' if chunk_id in gold else 'no'} | {'yes' if chunk_id in new_ids else 'no'} | {chars} |")
                    seen_ids.add(chunk_id)
                lines.append("")
    (run_dir / "RETRIEVAL_AUDIT.md").write_text("\n".join(lines))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--systems", default="embedding_rag,draftrag")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--max-passes", type=int, default=4)
    parser.add_argument("--seed", type=int, default=20260826)
    parser.add_argument("--build-only", action="store_true")
    parser.add_argument("--skip-missing-embedding", action="store_true")
    args = parser.parse_args()
    client = AzureClient()
    systems = [value.strip() for value in args.systems.split(",") if value.strip()]
    allowed = {"llm_only", "long_context", "bm25_rag", "embedding_rag", "draftrag"}
    if set(systems) - allowed:
        raise SystemExit("Unknown systems: " + ", ".join(sorted(set(systems) - allowed)))
    questions = read_jsonl(DATASET)
    questions = questions[:args.limit] if args.limit else questions
    skipped = {}
    if "embedding_rag" in systems and not client.embedding_model:
        reason = "AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME is absent or empty"
        if not args.skip_missing_embedding:
            raise SystemExit(reason + "; this benchmark requires embedding_rag for the requested comparison")
        skipped["embedding_rag"] = reason
        systems.remove("embedding_rag")
    resources = {}
    index_metrics = {"by_corpus": {}}
    index_mark = client.mark()
    for corpus in sorted({item["corpus"] for item in questions}):
        chunks = chunks_for(corpus)
        resource = {"chunks": chunks}
        index_metrics["by_corpus"][corpus] = {}
        if "draftrag" in systems:
            print(f"Preparing DraftRAG index for {corpus}", flush=True)
            system_mark = client.mark()
            resource["dims"] = make_dimensions(client, corpus, chunks)
            resource["semantic_index"] = make_semantic_index(client, corpus, chunks, resource["dims"])
            index_metrics["by_corpus"][corpus]["draftrag"] = client.since(system_mark)
        if "embedding_rag" in systems:
            print(f"Preparing embedding index for {corpus}", flush=True)
            system_mark = client.mark()
            resource["embedding_index"] = make_embedding_index(client, corpus, chunks)
            index_metrics["by_corpus"][corpus]["embedding_rag"] = client.since(system_mark)
        resources[corpus] = resource
    index_metrics["total"] = client.since(index_mark)
    if args.build_only:
        print(json.dumps({"index_build": index_metrics, "skipped": skipped}, indent=2))
        return
    run_dir = RUNS / time.strftime("%Y%m%d-%H%M%S")
    run_dir.mkdir(parents=True, exist_ok=True)
    schedule = [(item, system) for item in questions for system in systems]
    random.Random(args.seed).shuffle(schedule)
    rows = []
    for number, (item, system) in enumerate(schedule, 1):
        print(f"[{number}/{len(schedule)}] {system}: {item['id']}", flush=True)
        mark, started = client.mark(), time.perf_counter()
        try:
            answer, retrieved, metadata = run_system(client, system, item, resources[item["corpus"]], args.top_k, args.max_passes)
            row = {"question_id": item["id"], "corpus": item["corpus"], "category": item["category"], "system": system, "question": item["question"], "reference_answer": item["reference_answer"], "gold_chunk_ids": item["gold_chunk_ids"], "answer": answer, "retrieved_chunk_ids": retrieved, "metadata": metadata, **score_answer(item, answer, retrieved), **retrieval_metrics(item, resources[item["corpus"]]["chunks"], retrieved, metadata)}
        except Exception as error:
            row = {"question_id": item["id"], "corpus": item["corpus"], "category": item["category"], "system": system, "error": f"{type(error).__name__}: {error}", "metadata": {}}
        row.update(client.since(mark))
        row["wall_latency_ms"] = round((time.perf_counter() - started) * 1000, 2)
        rows.append(row)
        with (run_dir / "results.jsonl").open("a") as output:
            output.write(json.dumps(row, ensure_ascii=False) + "\n")
    summary = summarize(rows, skipped, index_metrics)
    (run_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    fields = ["question_id", "corpus", "category", "system", "claim_recall", "all_claims", "gold_chunk_recall", "all_gold_chunks", "retrieval_precision_unique", "context_bloat_ratio", "source_context_chars_delivered", "source_context_duplication_ratio", "retrieval_events", "retrieved_chunks_total", "retrieved_chunks_unique", "irrelevant_chunks_unique", "redundant_retrieval_rate", "late_gold_discovery", "query_diversity", "answer_word_count", "answer_detail_density", "wall_latency_ms", "calls", "total_tokens", "error"]
    with (run_dir / "metrics.csv").open("w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key) for key in fields})
    write_report(run_dir, summary, args)
    write_retrieval_audit(run_dir, rows)
    print(f"Results: {run_dir}")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
