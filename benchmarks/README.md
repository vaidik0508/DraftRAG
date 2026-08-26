# Embedding RAG vs DraftRAG benchmark

This benchmark tests the central DraftRAG claim—not whether it is generally faster than
an LLM or better than passing an entire small document.

> Can answer-local, multi-pass retrieval find the right evidence on demand, deliver less
> irrelevant source context, and produce a more complete multi-part answer than one-shot
> embedding retrieval?

Only two systems are part of the primary comparison:

| System | Retrieval behavior |
| --- | --- |
| `embedding_rag` | Embed the complete question once, retrieve cosine top-k once, then generate one answer. |
| `draftrag` | Draft inline evidence demands, retrieve separately for each demand, rewrite, and repeat while evidence is missing. |

Both systems use identical chunks, `top-k`, questions, gold evidence, answer deployment,
and final-answer instructions. Index construction is measured separately.

## What the benchmark measures

### Correct on-demand retrieval

- **Gold-chunk recall:** required source chunks found / required source chunks.
- **Unique retrieval precision:** required unique chunks / all unique chunks retrieved.
- **Useful demand-event rate:** placeholders whose result contains at least one required
  chunk / all retrieval placeholders. Embedding RAG's one search is one event.
- **Complete-evidence rate:** questions for which every required chunk was found.

### Context bloat

- **Unique irrelevant chunks:** retrieved unique chunks outside the gold evidence set.
- **Context-bloat ratio:** irrelevant unique source characters / all unique retrieved
  source characters.
- **Source context delivered:** source characters actually placed into answer-generation
  prompts. DraftRAG counts cumulative evidence banks and inline evidence again whenever
  they are re-injected on a later pass.
- **Source duplication ratio:** repeated source characters delivered across passes versus
  unique retrieved source characters.
- **Total versus unique chunks:** exposes repeated retrieval of the same text.

Retrieving five unique chunks but injecting them into three rewrite prompts is more
context load than retrieving them once; this benchmark reports that difference.

### Multi-pass and diverse demand generation

- **Retrieval events:** independently generated evidence demands.
- **Unique query count:** repeated semantic queries are deduplicated.
- **Query diversity:** mean pairwise Jaccard distance between query token sets.
- **Late gold discovery:** required chunks first found after retrieval round one.
- **Pass count and convergence:** whether refinement naturally stops.
- **Redundant retrieval rate:** repeated chunk hits / all chunk hits.

Query diversity is useful only when diverse queries retrieve different required evidence
and improve final coverage.

### Answer richness without rewarding verbosity

- **Claim recall:** requested gold facts present / requested gold facts.
- **Complete-answer rate:** every requested fact is present.
- **Rich-question claim recall:** claim recall on multi-aspect, sequential multi-hop, and
  version-conflict questions.
- **Rich-question complete rate:** fully answered rich questions / all rich questions.
- **Requested claims answered:** absolute gold details present.
- **Claim density:** requested claims answered per 100 answer words.

The answer can therefore be broad and detailed without receiving credit for unsupported
or repetitive prose.

## Corpora and questions

The dataset contains 180 chunks across three synthetic corpora:

- [`fictional_ops`](corpora/fictional_ops/source.txt): invented personnel, approval
  chains, incident controls, and distractor profiles;
- [`versioned_manual`](corpora/versioned_manual/source.txt): NovaDock 2.1, 2.2, and 3.0
  rules with intentionally conflicting limits and procedures;
- [`counterfactual_kb`](corpora/counterfactual_kb/source.txt): Meridian facts that must
  override conflicting Harbor and real-world knowledge.

Every corpus has 60 chunks, with gold facts scattered throughout the source. The
12-question set is [`datasets/pilot.jsonl`](datasets/pilot.jsonl) and covers single-hop,
multi-aspect, sequential multi-hop, version conflict, counterfactual, and unanswerable
cases.

```bash
python3 benchmarks/generate_data.py
```

## Azure configuration

Both deployments are required:

```dotenv
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_DEPLOYMENT_NAME=your-answer-deployment
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME=your-embedding-deployment
```

The current local `.env` does not contain the embedding deployment variable, so a valid
two-system run cannot yet be produced. The runner exits rather than silently omitting
embedding RAG or falling back to a public endpoint.

The request shapes follow the official [Responses API reference](https://developers.openai.com/api/reference/resources/responses/methods/create)
and [Embeddings API reference](https://developers.openai.com/api/reference/resources/embeddings/methods/create).

## Run the comparison

```bash
python3 benchmarks/benchmark.py
```

Defaults are `embedding_rag,draftrag`, top-k 5 per retrieval event, four maximum
DraftRAG passes, and seed `20260826`.

Each run produces:

```text
benchmarks/runs/<timestamp>/
  REPORT.md       focused comparison tables
  RETRIEVAL_AUDIT.md  every pass/query with ranked chunk IDs, scores, and gold markers
  results.jsonl   answers, chunks, drafts, and placeholder queries
  metrics.csv     per-question retrieval, bloat, richness, cost, and latency
  summary.json    aggregate metrics
```

The embedding index batches strings using the documented embeddings array input.
DraftRAG batches ten chunks per score-generation call to control cost. The main prototype
scores one chunk per call; because batching can introduce cross-item scoring drift, a
one-chunk-per-call ablation remains necessary.

Scorecard version 3 requires absolute, query-independent, corpus-discriminative dimensions and explicit anchors
at `0.0`, `0.25`, `0.50`, `0.75`, and `1.0`. Chunk and query prompts use the same anchors
but different roles: chunks score what they contain, while queries score what evidence
they request. Index creation aborts when more than 10% of chunks are all-zero or fewer
unique vectors exist than scorecard dimensions. A vector shared by more than 25% of
chunks produces a warning because repeated semantic templates can be legitimate but
cannot be distinguished inside that class. Partial values are encouraged when justified but are not required by quota;
clear absence and exact central expression should remain `0.0` and `1.0`.

## Success criteria

DraftRAG demonstrates its intended benefit only if it achieves these together:

1. higher rich-question claim recall or complete-answer rate;
2. equal or better gold-chunk recall;
3. lower context-bloat ratio or fewer source characters delivered;
4. useful late gold discovery on at least some questions;
5. acceptable redundancy and convergence.

Generating many placeholders or writing a longer answer is not success by itself.

## Canonical DraftRAG validation run

### Partial-anchor prompt validation

[`runs/20260826-133715/`](runs/20260826-133715/) records the canonical DraftRAG-only validation after
introducing absolute, corpus-discriminative dimensions and calibrated partial anchors.
It is not the embedding comparison, but it measures the prompt change against the same
12 questions:

| Metric | Original prompt | Scorecard v3 |
| --- | ---: | ---: |
| Claim recall | 54.2% | 95.6% |
| Gold-chunk recall | 36.0% | 83.8% |
| Unique retrieval precision | 19.2% | 39.1% |
| Context-bloat ratio | 80.6% | 58.1% |
| Source characters delivered | 3,184 | 2,156 |
| Retrieval redundancy | 26.7% | 12.1% |
| Rich-question claim recall | 64.3% | 95.2% |
| Rich-question complete rate | 42.9% | 85.7% |

The complete ranked per-placeholder trace is in the run's
[`RETRIEVAL_AUDIT.md`](runs/20260826-133715/RETRIEVAL_AUDIT.md). Remaining failures show
the ten-axis budget can still merge different facts—for example, water, moons, and
chemical symbols share one counterfactual-science axis.

Older development runs were removed so [`runs/`](runs/) contains only this canonical
scorecard-v3 result. It is not the requested embedding-RAG comparison; that comparison
still requires an Azure embedding deployment.

The positional control is motivated by
[Lost in the Middle](https://arxiv.org/abs/2307.03172). Separating retrieval coverage from
answer claim coverage follows [RAGChecker](https://arxiv.org/abs/2408.08067).
