# Examples

All source documents, generated scorecards, indexes, and recorded traces live here so
the repository root stays code-focused.

| Example | Description | Artifacts |
| --- | --- | --- |
| [Constitution](constitution/README.md) | Primary 15-chunk cross-article experiment | Source, 10D rules, index, and two-draft walkthrough |
| [Project Aster](aster/README.md) | Small fictional smoke-test corpus | Source text |

Use the root CLI with `--data-dir` to keep generated artifacts inside an example:

```bash
python3 no_emb_rag.py --data-dir examples/constitution ask --trace "Your question"
```
