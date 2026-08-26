# DraftRAG validation run

Generated: 2026-08-26 13:40:52 +0530

Configuration: top-k=5, max DraftRAG passes=4, seed=20260826.

| System | Claim recall | Rich-question recall | Gold-chunk recall | Complete evidence | Retrieval precision | Context bloat | Source chars delivered |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| draftrag | 95.6% | 95.2% | 83.8% | 60.0% | 39.1% | 58.1% | 2156 |

## Answer richness

| System | Complete answers | Rich-question complete | Mean requested claims answered | Mean answer words | Claims per 100 words |
| --- | ---: | ---: | ---: | ---: | ---: |
| draftrag | 83.3% | 85.7% | 2.67 | 39.7 | 8.50 |

## On-demand retrieval behavior

| System | Retrieval events | Useful events | Late gold discovery | Query diversity | Total / unique chunks | Irrelevant chunks | Retrieval redundancy | Source duplication | Mean passes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| draftrag | 1.58 | 83.3% | 5.0% | 8.1% | 7.92 / 5.92 | 3.67 | 12.1% | 54.9% | 2.17 |

## Query-time efficiency

| System | Mean latency | p95 latency | Mean API calls | Total tokens |
| --- | ---: | ---: | ---: | ---: |
| draftrag | 18.06s | 26.45s | 3.33 | 108384 |

## Interpretation limits

This is a small deterministic pilot, not a statistically conclusive result. Claim recall is exact alias matching and does not measure unsupported extra claims. Index-building calls are separate from per-question latency. Inspect `results.jsonl` and DraftRAG traces before drawing conclusions.
