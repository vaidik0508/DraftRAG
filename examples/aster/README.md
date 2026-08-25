# Project Aster smoke test

`source.txt` is a short fictional operations handbook for quick and inexpensive tests.
It normally produces two chunks with the default chunk size.

From the repository root:

```bash
python3 no_emb_rag.py --data-dir examples/aster init \
  examples/aster/source.txt --dimensions 10

python3 no_emb_rag.py --data-dir examples/aster index \
  examples/aster/source.txt

python3 no_emb_rag.py --data-dir examples/aster ask --trace \
  "Can Mira deploy Aster at 10 PM on 25 August 2026? What must she do and who approves it?"
```

The generated `embedding_rules.md` and `rag_index.json` will remain in this directory.
