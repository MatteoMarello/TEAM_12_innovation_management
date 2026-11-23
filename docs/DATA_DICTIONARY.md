# Data dictionary and analytical units

The observation is an original DOCDB family. `docdb_family_id` is a stable string join key.
`representative_appln_id`, `title_appln_id` and `abstract_appln_id` identify application records.
The representative and evidence applications can differ. A publication identifier, where present
in provenance, identifies a publication rather than a family or an application. 

| Field group | Meaning |
|---|---|
| `appln_title`, `appln_abstract`, respective language and application IDs | Original source evidence and its lineage |
| `cpc_codes` | Pipe-delimited family CPC assignments, preserved verbatim |
| `source_channel` | Candidate retrieval provenance, `cpc_only`, `keyword_only`, or `both` |
| `final_policy_label`, `technology_segment` | Model policy decision and technology segment |
| `principal_invention`, `storage_relationship`, `utility_sector_relationship` | Technical contribution and separately recorded Gate S and Gate U relationships |
| `primary_decision_rule_id`, `secondary_decision_rule_ids` | Decisive technical rule and optional semicolon-delimited additional rules |
| `evidence_*`, `classification_rationale_en` | Verbatim trace and its source, technical rationale and evidence limitations |
| `engine_provider`, `source_engine_provider`, `model_requested`, `source_model_revision`, `source_model_sha256` | Canonical cohort, verbatim available source engine, requested model and available artifact identifiers |
| `policy_sha256`, `annotation_status`, `input_batch`, `completed_utc` | Policy version and model-decision provenance. Historical source fields may be empty where unavailable. |

The 5,317 master rows include 5,316 titles, 5,308 abstracts and 5,282 CPC lists. The input
contains 4,445 CPC-only candidates, 484 keyword-only candidates and 388 from both channels.
The [coverage report](../reports/DATASET_PROFILE.json) is regenerated from the canonical loader.

Count each family once for total volumes, and once per distinct CPC subclass for the CPC view.
Multi-class families can contribute to several subclasses. The technology segment is a
single assignment and uses a different taxonomy from CPC. Keep an explicit unknown group
for blank data. Report the denominator and observation window with every indicator.

## Additional extraction

| Missing inputs | PATSTAT or external extraction |
|---|---|
| Priority and filing dates | Join family members to `TLS201_APPLN` by the DOCDB family and application keys. Resolve priorities through `TLS204_APPLN_PRIOR`. Define the family year as the earliest verified priority year, with earliest filing as an explicitly flagged fallback. Filter sentinel dates. |
| Applicants and ownership | Join `TLS207_PERS_APPLN` applicant roles to `TLS206_PERSON` through person ID. Harmonize names and applicant country before aggregation. Attribution requires a dated parent-entity concordance. Current ownership requires external assignment or register data. |
| Citations | Derive family-to-family links through `TLS212_CITATION`, `TLS211_PAT_PUBLN` and `TLS201_APPLN`. Dedupe directed family pairs, define citation windows and document self-citation and age-censoring rules. |
| Geography and grants | Use applications and publication authorities from `TLS201_APPLN` and `TLS211_PAT_PUBLN`. Define how WO and EP are represented. Validate grants and current legal status against dated register or `TLS231_INPADOC_LEGAL_EVENT` evidence, allowing for office-specific coverage. |
| Market, financial and innovation scoring | Obtain dated firm, market and financial inputs separately. Link vetted firm identifiers to normalized applicants. Use observed values and expose missingness, sources, weights and sensitivity. |

Confirm column names and sentinel values against the exact TIP/PATSTAT edition used.
Use fractional attribution across distinct applicants for concentration calculations unless
a separately reported whole-count view is needed. Maintain the same eligible family set
and year definition across Steps 1–6. For legal status, cite the snapshot date and jurisdiction.
