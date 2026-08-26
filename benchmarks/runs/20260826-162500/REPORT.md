# DraftRAG validation run

Generated: 2026-08-26 16:28:15 +0530

Configuration: top-k=5, max DraftRAG passes=4, seed=20260826.

Scorecard: v6; benchmark-answer leakage check: passed.

| System | Claim recall | Rich-question recall | Gold-chunk recall | Complete evidence | Retrieval precision | Context bloat | Source chars delivered |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| draftrag | 94.5% | 90.5% | 84.3% | 60.0% | 43.8% | 56.2% | 1691 |

## Answer richness

| System | Complete answers | Rich-question complete | Mean requested claims answered | Mean answer words | Claims per 100 words |
| --- | ---: | ---: | ---: | ---: | ---: |
| draftrag | 83.3% | 71.4% | 2.67 | 32.8 | 11.49 |

## On-demand retrieval behavior

| System | Retrieval events | Useful events | Late gold discovery | Query diversity | Total / unique chunks | Irrelevant chunks | Retrieval redundancy | Source duplication | Mean passes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| draftrag | 1.33 | 83.3% | 0.0% | 7.8% | 6.25 / 5.33 | 3.08 | 6.1% | 47.8% | 2.00 |

## Query-time efficiency

| System | Mean latency | p95 latency | Mean API calls | Total tokens |
| --- | ---: | ---: | ---: | ---: |
| draftrag | 16.22s | 20.27s | 3.00 | 158713 |

## Interpretation limits

This is a small deterministic pilot, not a statistically conclusive result. Claim recall is exact alias matching and does not measure unsupported extra claims. Index-building calls are separate from per-question latency. Inspect `results.jsonl` and DraftRAG traces before drawing conclusions.
