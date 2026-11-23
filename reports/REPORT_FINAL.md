# Team 12 final integration and technical review

## Dataset and lineage

The strict merge validated all 5,317 distinct DOCDB patent families. The original 4,639 source labels were preserved, and 678 missing families received new complete ASTRA V4 labels. The 34 completion parts passed ID, gate, policy, schema and verbatim-evidence checks. No audit proposal was applied to the canonical dataset.

| Label | Families |
|---|---:|
| CORE | 558 |
| ENABLING | 2,233 |
| IRRELEVANT | 2,526 |

## Human-reviewed benchmark

All 300 reference IDs join uniquely. Accuracy is 0.8567, macro F1 is 0.8423, weighted F1 is 0.8545, and Cohen’s kappa is 0.7565. The historical Astra artifact has the same IDs and labels. It therefore reproduces these values under its historical AI-only provenance. Team 12 confirms subsequent human review. Independent adjudication, sampling and review protocol were unavailable. Classification scores apply to this benchmark overlap.

## Technical reannotation

The 300-family reannotation agrees with the reviewed benchmark on 88.67% and with the preserved master labels on 89.33%. Agents received label-free files and were instructed to avoid previous labels. The unabridged rulebook names 28 benchmark families and the shared work environment lacked access isolation. This is a non-blind technical audit.

Excluding the 28 benchmark IDs named by the manual gives 88.97% agreement across 272 families. This sensitivity analysis does not establish independent blinding.

### Most frequent divergent label patterns

| Human benchmark | Original master | Technical audit | Families |
|---|---|---|---:|
| ENABLING | IRRELEVANT | IRRELEVANT | 15 |
| ENABLING | IRRELEVANT | ENABLING | 14 |
| ENABLING | CORE | ENABLING | 4 |
| CORE | CORE | ENABLING | 3 |
| ENABLING | ENABLING | IRRELEVANT | 3 |
| ENABLING | CORE | CORE | 3 |
| IRRELEVANT | IRRELEVANT | ENABLING | 2 |
| IRRELEVANT | ENABLING | ENABLING | 2 |
| CORE | CORE | IRRELEVANT | 2 |
| CORE | IRRELEVANT | IRRELEVANT | 2 |

## Adjudication queue

The unblinded priority review assessed all 40 initial disagreements, proposed 24 changes and agreed with the benchmark on 23. Conflicts turn on whether the contribution improves storage hardware or controls an existing store, whether a named store serves a qualifying electrical network, and whether richer historical patent material establishes a link missing from the abstract.

The unified queue contains 54 proposal records covering 29 distinct families. Distinct review streams retain their own evidence and can propose competing labels. The dedicated Qwen audit checked the 569-record snapshot and examined selected boundary cases. Current-policy human adjudication should resolve competing proposals using the same evidence edition and verified technical context before any dataset update.

| Proposal stream | Records |
|---|---:|
| Technical Reannotation Converges With Benchmark | 20 |
| Unblinded Priority 40 | 24 |
| Unblinded Qwen Technical Review | 10 |

## Reproduction and remaining scope

Run strict consolidation, benchmark evaluation, technical-audit comparison and proposal assembly on the archived source versions. These operations validate and assemble genuine saved model decisions. They do not infer labels. Retrieval recall requires an independently evaluated universe or sampling beyond the selected candidates.
Technology mix and CPC counts are available. Temporal, applicant and ownership, citation, geographical, status and market valuation analyses require additional sourced enrichment.
