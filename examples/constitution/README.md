# Constitution example

This directory is a reproducible snapshot of the 15-chunk DraftRAG experiment.

## Contents

| File | Description |
| --- | --- |
| `source.txt` | Constitutional text used for indexing |
| `embedding_rules.md` | Generated 10-dimensional semantic scorecard |
| `rag_index.json` | 15 chunks and their LLM-generated vectors |
| `iteration.md` | Question, Draft 1 placeholders, retrieval, and final Draft 2 |

The source is derived from [Project Gutenberg eBook #5](https://www.gutenberg.org/ebooks/5).
Its publisher preface and license boilerplate were excluded before indexing. The Project
Gutenberg page marks the underlying work public domain in the USA.

## Reproduce from the repository root

```bash
python3 no_emb_rag.py --data-dir examples/constitution init \
  examples/constitution/source.txt --dimensions 10
python3 no_emb_rag.py --data-dir examples/constitution index \
  examples/constitution/source.txt --max-chars 2100
python3 no_emb_rag.py --data-dir examples/constitution ask \
  --top-k 3 --max-passes 5 --trace \
  "Using only the constitutional text, compare the minimum age, citizenship duration, residency requirement, and term length for a Representative, a Senator, and the President. Then explain how a presidential veto can be overridden, who appoints ambassadors and Supreme Court judges and what role the Senate plays, and how long federal judges hold office. Clearly separate each office and process."
```

LLM scoring and drafting are nondeterministic, so exact vectors and wording may differ
between runs. The saved files and walkthrough record one successful run.
