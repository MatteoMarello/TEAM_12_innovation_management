# Team 12 · Utility-scale electricity energy storage

Innovation Management · Politecnico di Torino · 2026/27

Which patent families concern physical electricity storage at utility scale or the
technologies that technically enable it? This repository provides the reproducible
classification and evaluation pipeline for the Team 12 / Enel patent landscape.

## Dataset

| Purpose | Canonical path |
|---|---|
| All 5,317 families and original technical evidence | `data/final/TEAM12_PATENTS_5317_FINAL.csv` |
| Sector dataset for Steps 1–6 | `data/final/TEAM12_SECTOR_RELEVANT_CORE_ENABLING.csv` |
| Separate 300-family human-reviewed reference | `data/reference/TEAM12_GROUND_TRUTH_HUMAN_REVIEWED_300.csv` |

These paths are populated from the private Team 12 dataset release. The public repository
contains code and aggregate results. Access and data integrity are documented in
[Data provenance](docs/DATA_PROVENANCE.md) and [checksums](docs/CANONICAL_SHA256SUMS.txt).

From the repository root, extract the authorized release or set `TEAM12_DATA_ROOT` to the
directory containing its `data/` tree. Use the centralized loader in every downstream step.

```python
from src.data_loading import load

sector = load("sector")
```

## Method and results

The validated master contains 558 CORE, 2,233 ENABLING and 2,526 IRRELEVANT families.
The sector subset contains 2,791 families. Across the 300 reviewed cases, three-class
accuracy is 85.67%, macro F1 is 0.8423 and weighted F1 is 0.8545.

The source collection comes from PATSTAT/TIP CPC and keyword candidate searches.
The handoff describes BM25, Patent SBERT and fusion as retrieval stages without the
configuration and ranked data required to reproduce their execution. We preserve the
Qwen Q9.3, local Codex, Claude Code and Codex web outputs and independently completed
the remaining 678 families using full ASTRA V4. The policy separates physical storage
innovation (CORE) from storage-specific technical support (ENABLING) and scope
exclusions (IRRELEVANT). [Methodology](docs/METHODOLOGY.md) · [Full V4 policy](policy/ASTRA_DECISION_BOUNDARIES_AND_RULEBOOK_FULL_V4.txt)

[Human-reviewed evaluation](reports/evaluation/BENCHMARK.md) reports three-class and
binary relevance metrics, the confusion matrix and source-cohort results. The 300 labels
were initially AI-assisted and subsequently human-reviewed, as confirmed by Team 12.
The benchmarking limits and absence of independent-review evidence are documented in
[Evaluation](docs/EVALUATION.md). The [final methodology and technical review](reports/REPORT_FINAL.md) summarizes all 300 reannotations and the adjudication queue.

## Reproduce and extend

Run `python -m unittest discover -s tests -v` and `python -m src.evaluation.benchmark`
after provisioning the private data. For regeneration from the original handoff see
[Reproducibility](docs/REPRODUCIBILITY.md). The notebooks include validated dataset and
sector-volume/CPC analysis. [Step readiness](notebooks/README.md) and the
[data dictionary](docs/DATA_DICTIONARY.md) list the inputs needed for longitudinal,
competitive, financial and strategic work.
