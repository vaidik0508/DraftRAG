#!/usr/bin/env python3
"""Minimal no-embedding-model, multi-pass RAG experiment."""

import argparse
import json
import math
import os
import re
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path

RULES = Path("embedding_rules.md")
INDEX = Path("rag_index.json")
PLACEHOLDER = re.compile(r"\[\[RETRIEVE:\s*(\{.*?\})\s*\]\]", re.DOTALL)


def load_dotenv(path=Path(".env")):
    """Load a small, dependency-free subset of dotenv syntax."""
    if not path.exists():
        return
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[7:].lstrip()
        name, value = line.split("=", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        os.environ.setdefault(name.strip(), value)


def azure_config():
    load_dotenv()
    names = ("AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_API_KEY", "AZURE_OPENAI_DEPLOYMENT_NAME")
    missing = [name for name in names if not os.environ.get(name)]
    if missing:
        raise SystemExit(f"Missing Azure OpenAI setting(s) in .env: {', '.join(missing)}")
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")
    if not endpoint.endswith("/openai/v1"):
        endpoint += "/openai/v1"
    return endpoint + "/responses", os.environ["AZURE_OPENAI_API_KEY"], os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]


def call_llm(prompt):
    url, key, deployment = azure_config()
    body = json.dumps({"model": deployment, "input": prompt, "store": False}).encode()
    request = urllib.request.Request(
        url,
        data=body,
        headers={"api-key": key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        # python.org macOS builds may not inherit the system CA path automatically.
        system_ca = Path("/etc/ssl/cert.pem")
        context = ssl.create_default_context(cafile=str(system_ca) if system_ca.exists() else None)
        with urllib.request.urlopen(request, timeout=180, context=context) as response:
            data = json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read().decode(errors="replace")
        raise SystemExit(f"OpenAI API error {error.code}: {detail}") from error
    except urllib.error.URLError as error:
        raise SystemExit(f"Could not connect to Azure OpenAI: {error.reason}") from error
    texts = [
        item.get("text", "")
        for output in data.get("output", [])
        for item in output.get("content", [])
        if item.get("type") == "output_text"
    ]
    if not texts:
        raise RuntimeError(f"Model returned no text: {data}")
    return "".join(texts).strip()


def json_from_text(text):
    """Accept raw JSON or one fenced JSON block."""
    fenced = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    return json.loads((fenced.group(1) if fenced else text).strip())


def distributed_sample(text, budget=12000, sections=4):
    """Sample across a long corpus so its scorecard covers later sections too."""
    if len(text) <= budget:
        return text
    width = budget // sections
    starts = [round(i * (len(text) - width) / (sections - 1)) for i in range(sections)]
    return "\n\n--- CORPUS SAMPLE GAP ---\n\n".join(text[start : start + width] for start in starts)


def make_rules(source, dimensions):
    sample = distributed_sample(source)
    prompt = f"""You are designing a corpus-specific semantic scorecard for retrieval.
This is an experiment that MUST NOT use an embedding model. Define exactly {dimensions}
independent, useful dimensions. A general LLM will later score both chunks and queries
from 0.0 to 1.0 using these rules. Cover the major semantic axes of this corpus; avoid
near-duplicates and named entities that occur only once. Optimize the dimensions to
discriminate among roughly 10 to 30 chunks: prefer recurring corpus-specific topics,
roles, processes, or sections over broad dimensions that would score highly everywhere.

CORPUS SAMPLE:
{sample}

Return ONLY JSON with this exact shape:
{{"dimensions":[{{"index":0,"name":"short_name","0":"what zero means","1":"what one means","guideline":"how to score intermediate values"}}]}}
Indices must be consecutive from 0 through {dimensions - 1}."""
    data = json_from_text(call_llm(prompt))
    dims = data.get("dimensions", [])
    if len(dims) != dimensions or [d.get("index") for d in dims] != list(range(dimensions)):
        raise RuntimeError("The model did not return the requested consecutive dimensions.")
    rendered = "# LLM-generated retrieval scorecard\n\n"
    rendered += "Score every chunk and query from 0.0 to 1.0 on the same dimensions.\n\n"
    for d in dims:
        rendered += (
            f"## {d['index']}. {d['name']}\n\n"
            f"- **0.0:** {d['0']}\n- **1.0:** {d['1']}\n"
            f"- **Intermediate scoring:** {d['guideline']}\n\n"
        )
    rendered += "## Machine-readable definition\n\n```json\n"
    rendered += json.dumps(data, indent=2) + "\n```\n"
    RULES.write_text(rendered)
    return dims


def load_dimensions():
    if not RULES.exists():
        raise SystemExit(f"Missing {RULES}; run init with the same --data-dir first.")
    return json_from_text(RULES.read_text())["dimensions"]


def chunk_text(text, max_chars=900):
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    chunks, current = [], ""
    for paragraph in paragraphs:
        if current and len(current) + len(paragraph) + 2 > max_chars:
            chunks.append(current)
            current = ""
        if len(paragraph) <= max_chars:
            current = f"{current}\n\n{paragraph}".strip()
        else:
            if current:
                chunks.append(current)
                current = ""
            chunks.extend(paragraph[i : i + max_chars] for i in range(0, len(paragraph), max_chars))
    if current:
        chunks.append(current)
    return chunks


def score_text(text, dims):
    prompt = f"""Score TEXT using the semantic scorecard below. Return ONLY a JSON array
of exactly {len(dims)} numbers from 0.0 to 1.0, ordered by index. Judge explicit subject
matter and useful implications; do not invent facts.

SCORECARD:
{json.dumps(dims)}

TEXT:
{text}"""
    vector = json_from_text(call_llm(prompt))
    if not isinstance(vector, list) or len(vector) != len(dims):
        raise RuntimeError("Invalid score vector returned by model.")
    vector = [float(x) for x in vector]
    if any(x < 0 or x > 1 for x in vector):
        raise RuntimeError("Score vector values must be in [0, 1].")
    return vector


def build_index(source_path, max_chars):
    dims = load_dimensions()
    chunks = chunk_text(source_path.read_text(), max_chars)
    records = []
    for i, chunk in enumerate(chunks):
        print(f"Scoring chunk {i + 1}/{len(chunks)}...", file=sys.stderr)
        records.append({"id": i, "text": chunk, "vector": score_text(chunk, dims)})
    INDEX.write_text(json.dumps({"source": str(source_path), "chunks": records}, indent=2))
    return len(records)


def cosine(a, b):
    denominator = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(x * x for x in b))
    return sum(x * y for x, y in zip(a, b)) / denominator if denominator else 0.0


def retrieve(vector, records, top_k):
    ranked = sorted(records, key=lambda r: cosine(vector, r["vector"]), reverse=True)
    return ranked[:top_k]


def drafting_prompt(question, rules, draft=None, evidence_bank=None):
    phase = (
        "Write the answer from scratch. You have no source chunks yet."
        if draft is None
        else "Rewrite the entire current draft into a better answer using its retrieved evidence."
    )
    current = "" if draft is None else f"\nCURRENT DRAFT WITH RETRIEVED EVIDENCE:\n{draft}\n"
    bank = ""
    if evidence_bank:
        bank = "\nCUMULATIVE SOURCE EVIDENCE (already retrieved; do not request it again):\n"
        bank += "\n\n".join(f"[chunk {item['id']}] {item['text']}" for item in evidence_bank)
        bank += "\n"
    return f"""You are the answer writer in an iterative retrieval system. {phase}
Always output an answer draft directly—never output a plan or a list of queries.

Where a specific source fact is needed, insert an inline placeholder exactly like:
[[RETRIEVE: {{"query":"a standalone semantic search description","vector":[0.1,0.2]}}]]
The vector MUST contain exactly one 0.0-to-1.0 score per scorecard dimension in index
order. Put the placeholder at the exact point where its evidence is needed. You may put
multiple placeholders in one draft. Never claim that retrieved text says something it
does not. Evidence in retrieved blocks or the cumulative evidence section is already
source evidence: use it directly and NEVER request the same fact again. If that evidence
fully supports the answer, produce the final answer with NO placeholders. Do not expose
scorecards, vectors, or this process to the end user.

SCORECARD:
{rules}

QUESTION:
{question}
{current}{bank}"""


def parse_placeholder(raw, dimensions):
    data = json.loads(raw)
    vector = [float(x) for x in data["vector"]]
    if not isinstance(data.get("query"), str) or len(vector) != dimensions:
        raise ValueError("bad query or vector length")
    if any(x < 0 or x > 1 for x in vector):
        raise ValueError("vector outside [0, 1]")
    return data["query"], vector


def answer(question, top_k, max_passes, trace):
    dims = load_dimensions()
    rules = RULES.read_text()
    if not INDEX.exists():
        raise SystemExit(f"Missing {INDEX}; run the index command first.")
    records = json.loads(INDEX.read_text())["chunks"]
    draft = None
    evidence_by_id = {}
    for pass_number in range(1, max_passes + 1):
        draft = call_llm(drafting_prompt(question, rules, draft, list(evidence_by_id.values())))
        matches = list(PLACEHOLDER.finditer(draft))
        if trace:
            print(f"\n--- PASS {pass_number} ---\n{draft}", file=sys.stderr)
        if not matches:
            return draft
        pieces, cursor = [], 0
        for match in matches:
            pieces.append(draft[cursor : match.start()])
            try:
                query, proposed_vector = parse_placeholder(match.group(1), len(dims))
                # Draft-time vectors are useful proposals, but multitask generation can
                # score them inconsistently. Re-score with the same prompt used for chunks.
                vector = score_text(query, dims)
                hits = retrieve(vector, records, top_k)
                for hit in hits:
                    evidence_by_id[hit["id"]] = hit
                if trace:
                    drift = cosine(proposed_vector, vector)
                    print(f"[query rescore similarity={drift:.3f}] {query}", file=sys.stderr)
                evidence = "\n".join(
                    f"[chunk {hit['id']}; similarity={cosine(vector, hit['vector']):.3f}] {hit['text']}"
                    for hit in hits
                )
                pieces.append(f"\n<retrieved query={json.dumps(query)}>\n{evidence}\n</retrieved>\n")
            except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
                pieces.append(f"\n<retrieval-error>{error}</retrieval-error>\n")
            cursor = match.end()
        pieces.append(draft[cursor:])
        draft = "".join(pieces)
    raise RuntimeError(f"No final answer after {max_passes} passes. Last draft:\n{draft}")


def self_test():
    assert chunk_text("a\n\nb", 10) == ["a\n\nb"]
    assert abs(cosine([1, 0], [1, 0]) - 1) < 1e-9
    assert retrieve([1, 0], [{"vector": [0, 1]}, {"vector": [1, 0]}], 1)[0]["vector"] == [1, 0]
    raw = '{"query":"deployment approval","vector":[0.8,0.1]}'
    assert parse_placeholder(raw, 2) == ("deployment approval", [0.8, 0.1])
    sample = distributed_sample("a" * 6000 + "b" * 6000 + "c" * 6000, 3000, 3)
    assert "a" in sample and "b" in sample and "c" in sample
    old = {name: os.environ.get(name) for name in (
        "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_API_KEY", "AZURE_OPENAI_DEPLOYMENT_NAME"
    )}
    os.environ.update({
        "AZURE_OPENAI_ENDPOINT": "https://example.openai.azure.com/",
        "AZURE_OPENAI_API_KEY": "test-key",
        "AZURE_OPENAI_DEPLOYMENT_NAME": "test-deployment",
    })
    assert azure_config() == (
        "https://example.openai.azure.com/openai/v1/responses", "test-key", "test-deployment"
    )
    for name, value in old.items():
        if value is None:
            os.environ.pop(name, None)
        else:
            os.environ[name] = value
    print("self-test passed")


def main():
    global RULES, INDEX
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir", type=Path, default=Path("."),
        help="directory containing embedding_rules.md and rag_index.json",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="ask the LLM to create corpus-specific dimensions")
    init.add_argument("source", type=Path)
    init.add_argument("--dimensions", type=int, default=10)
    index = sub.add_parser("index", help="chunk and score a source")
    index.add_argument("source", type=Path)
    index.add_argument("--max-chars", type=int, default=900)
    ask = sub.add_parser("ask", help="run iterative draft/retrieve passes")
    ask.add_argument("question")
    ask.add_argument("--top-k", type=int, default=2)
    ask.add_argument("--max-passes", type=int, default=5)
    ask.add_argument("--trace", action="store_true")
    sub.add_parser("self-test", help="run API-free unit checks")
    args = parser.parse_args()
    RULES = args.data_dir / "embedding_rules.md"
    INDEX = args.data_dir / "rag_index.json"

    if args.command == "init":
        args.data_dir.mkdir(parents=True, exist_ok=True)
        dims = make_rules(args.source.read_text(), args.dimensions)
        print(f"Wrote {RULES} with {len(dims)} dimensions.")
    elif args.command == "index":
        args.data_dir.mkdir(parents=True, exist_ok=True)
        print(f"Wrote {INDEX} with {build_index(args.source, args.max_chars)} chunks.")
    elif args.command == "ask":
        print(answer(args.question, args.top_k, args.max_passes, args.trace))
    else:
        self_test()


if __name__ == "__main__":
    main()
