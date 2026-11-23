# Evaluation

The authoritative comparison uses the normalized team-supplied human-reviewed labels.
The original is preserved unchanged in the private integration bundle. The original
semicolons, Windows-1252 encoding and empty trailing cells or rows are normalized to a
four-column UTF-8 CSV. All 300 IDs and labels match the historical Astra artifact exactly.
The updated human-review provenance applies to the benchmark only.

Scores use the family-ID join between immutable predictions and the reference. The
three-label matrix has reference rows and prediction columns. Binary relevance treats
CORE and ENABLING as positive and IRRELEVANT as excluded. Macro F1 averages equally over
labels. Weighted F1 weights by reference support. Source cohorts have different cases and
label distributions. Qwen used a different policy document. Zero-denominator class
scores are reported as zero and class supports are disclosed.

The separate AI technical review uses label-free input files but is not a strictly blind
audit. Complete V4 names 28 benchmark IDs and contains worked examples, and the shared
workspace permitted access to the other sources. The targeted priority disagreement audit
was intentionally unblinded. Differences may reflect both true scope interpretation and
differences in supplied evidence. Proposed changes remain separate from canonical labels.

The sample partners a convenience benchmark with a prefiltered candidate frame.
Consequently the benchmark agreement numbers cannot establish exhaustive retrieval.
An independent sampling frame of retrieved and excluded records with expert evaluation
is required for retrieval recall.

[Metrics and confusion matrix](../reports/evaluation/BENCHMARK.md)
