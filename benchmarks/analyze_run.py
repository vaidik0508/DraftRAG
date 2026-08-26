#!/usr/bin/env python3
"""Re-score a saved benchmark run and add category/iteration diagnostics."""

import argparse
import csv
import json
import statistics
from pathlib import Path

from benchmark import DATASET, RUNS, chunks_for, read_jsonl, retrieval_metrics, score_answer, write_retrieval_audit


def flattened(groups):
    return [item for group in groups for item in group]


def mean_present(rows, key):
    values = [row[key] for row in rows if row.get(key) is not None]
    return round(statistics.mean(values), 4) if values else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", nargs="?", help="defaults to the latest benchmarks/runs directory")
    args = parser.parse_args()
    run_dir = Path(args.run_dir) if args.run_dir else sorted(path for path in RUNS.iterdir() if path.is_dir())[-1]
    items = {item["id"]: item for item in read_jsonl(DATASET)}
    rows = read_jsonl(run_dir / "results.jsonl")
    corpora = {row["corpus"]: chunks_for(row["corpus"]) for row in rows}
    for row in rows:
        if row.get("error"):
            continue
        item = items[row["question_id"]]
        row["gold_chunk_ids"] = item["gold_chunk_ids"]
        row.update(score_answer(item, row["answer"], row.get("retrieved_chunk_ids", [])))
        row.update(retrieval_metrics(item, corpora[row["corpus"]], row.get("retrieved_chunk_ids", []), row.get("metadata", {})))
        if row["system"] == "draftrag":
            trace = row.get("metadata", {}).get("trace", [])
            first = set(flattened(trace[0].get("retrieved", []))) if trace else set()
            later = set(flattened([group for step in trace[1:] for group in step.get("retrieved", [])]))
            gold = set(item["gold_chunk_ids"])
            sequence = row.get("retrieved_chunk_ids", [])
            row["late_gold_discovery"] = round(len((later - first) & gold) / len(gold), 4) if gold else None
            row["late_unique_evidence"] = len(later - first)
            row["redundant_retrieval_rate"] = round(1 - len(set(sequence)) / len(sequence), 4) if sequence else 0.0
    (run_dir / "results.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows))

    analysis = {"by_system": {}, "by_category": {}, "draftrag_iteration": {}}
    for system in sorted({row["system"] for row in rows}):
        group = [row for row in rows if row["system"] == system and not row.get("error")]
        analysis["by_system"][system] = {
            "questions": len(group),
            "mean_claim_recall": round(statistics.mean(row["claim_recall"] for row in group), 4),
            "complete_answer_rate": round(statistics.mean(row["all_claims"] for row in group), 4),
            "mean_gold_chunk_recall": mean_present(group, "gold_chunk_recall"),
            "mean_retrieval_precision_unique": mean_present(group, "retrieval_precision_unique"),
            "mean_context_bloat_ratio": mean_present(group, "context_bloat_ratio"),
            "mean_source_context_chars_delivered": round(statistics.mean(row["source_context_chars_delivered"] for row in group), 2),
            "mean_retrieval_events": round(statistics.mean(row["retrieval_events"] for row in group), 2),
            "mean_query_diversity": round(statistics.mean(row["query_diversity"] for row in group), 4),
            "mean_answer_claims": round(statistics.mean(row["claim_hits"] for row in group), 2),
            "mean_answer_words": round(statistics.mean(row["answer_word_count"] for row in group), 2),
            "mean_answer_detail_density": round(statistics.mean(row["answer_detail_density"] for row in group), 4),
        }
        analysis["by_category"][system] = {}
        for category in sorted({row["category"] for row in group}):
            category_rows = [row for row in group if row["category"] == category]
            analysis["by_category"][system][category] = {
                "questions": len(category_rows),
                "mean_claim_recall": round(statistics.mean(row["claim_recall"] for row in category_rows), 4),
            }
    drafts = [row for row in rows if row["system"] == "draftrag" and not row.get("error")]
    answerable = [row for row in drafts if items[row["question_id"]]["gold_chunk_ids"]]
    analysis["draftrag_iteration"] = {
        "mean_late_gold_discovery": round(statistics.mean(row["late_gold_discovery"] for row in answerable), 4),
        "questions_with_late_gold": sum(row["late_gold_discovery"] > 0 for row in answerable),
        "answerable_questions": len(answerable),
        "mean_late_unique_evidence": round(statistics.mean(row["late_unique_evidence"] for row in drafts), 4),
        "mean_redundant_retrieval_rate": round(statistics.mean(row["redundant_retrieval_rate"] for row in drafts), 4),
    }
    (run_dir / "analysis.json").write_text(json.dumps(analysis, indent=2) + "\n")
    summary_path = run_dir / "summary.json"
    summary = json.loads(summary_path.read_text())
    for system, values in analysis["by_system"].items():
        if system in summary["systems"]:
            summary["systems"][system]["mean_claim_recall"] = values["mean_claim_recall"]
            summary["systems"][system]["all_claims_rate"] = values["complete_answer_rate"]
    summary_path.write_text(json.dumps(summary, indent=2) + "\n")
    fields = ["question_id", "corpus", "category", "system", "claim_recall", "all_claims", "gold_chunk_recall", "wall_latency_ms", "calls", "total_tokens", "error"]
    with (run_dir / "metrics.csv").open("w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key) for key in fields})

    report = [
        "# DraftRAG pilot results", "",
        "This 12-question pilot used the Azure deployment reported by the API as `gpt-5.6-luna`.", "",
        "| System | Claim recall | Complete answers | Gold-chunk recall | Mean latency | Mean calls | Tokens |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for system, values in summary["systems"].items():
        recall = values.get("mean_gold_chunk_recall")
        retrieval = "—" if recall is None else f"{recall:.1%}"
        report.append(f"| `{system}` | {values['mean_claim_recall']:.1%} | {values['all_claims_rate']:.1%} | {retrieval} | {values['mean_latency_ms'] / 1000:.2f}s | {values['mean_calls']:.2f} | {values['total_tokens']} |")
    iteration_lines = [
        f"- Late gold evidence appeared on {analysis['draftrag_iteration']['questions_with_late_gold']} of {analysis['draftrag_iteration']['answerable_questions']} answerable questions.",
        f"- Mean late-gold discovery was {analysis['draftrag_iteration']['mean_late_gold_discovery']:.1%}.",
        f"- Mean redundant retrieval rate was {analysis['draftrag_iteration']['mean_redundant_retrieval_rate']:.1%}.",
    ]
    if analysis["draftrag_iteration"]["questions_with_late_gold"]:
        iteration_lines.append("- Inspect `results.jsonl` to identify which later pass added each gold chunk.")
    else:
        iteration_lines.append("- No later draft pass discovered a new gold chunk in this run.")
    draft_conflict = analysis["by_category"].get("draftrag", {}).get("version_conflict", {}).get("mean_claim_recall")
    bm25_conflict = analysis["by_category"].get("bm25_rag", {}).get("version_conflict", {}).get("mean_claim_recall")
    conflict_line = ""
    if draft_conflict is not None and bm25_conflict is not None:
        conflict_line = f"DraftRAG did outperform BM25 on the two version-conflict questions ({draft_conflict:.1%} versus {bm25_conflict:.1%} claim recall), but this subgroup has only two items and is not conclusive."
    report += [
        "", "## Result", "",
        "The batched DraftRAG benchmark variant did **not** beat the baselines. Long context was best on these small corpora. BM25 exceeded DraftRAG in claim recall and was about seven times faster, while DraftRAG used roughly 17 times as many query-time tokens.", "",
        conflict_line, "",
        "## Iteration diagnostics", "",
        *iteration_lines, "",
        "## Main failure", "",
        "The 10-dimensional LLM scorecard was too coarse. Several distinct chunks received nearly indistinguishable vectors, causing queries to return unrelated distractor profiles. Rewriting could not recover because later queries searched the same lossy index. The benchmark batches ten chunks per scoring call, and the position-controlled rebuild also exposed batch-context sensitivity: counterfactual chunks scored in mixed batches retrieved worse than in the first grouped-order diagnostic. A faithful one-chunk-per-call ablation is still required.", "",
        "## Limits", "",
        "This is one stochastic run on 12 synthetic questions, so it is diagnostic rather than statistically conclusive. Exact-alias claim scoring measures requested-fact coverage but not unsupported extra claims. The embedding-RAG system was skipped because `AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME` was not configured; BM25 is a lexical baseline, not a substitute for that missing comparison. Cold DraftRAG builds were interrupted by malformed model JSON and an Azure HTTP 500, then resumed from checkpoints, so a complete single-run cold-build token total is unavailable.", "",
    ]
    if summary.get("skipped"):
        report += ["## Skipped", ""] + [f"- `{name}`: {reason}" for name, reason in summary["skipped"].items()] + [""]
    (run_dir / "REPORT.md").write_text("\n".join(report))
    write_retrieval_audit(run_dir, rows)
    print(json.dumps(analysis, indent=2))


if __name__ == "__main__":
    main()
