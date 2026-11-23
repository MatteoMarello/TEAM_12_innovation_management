# Analysis by course step

All steps use the centralized `src.data_loading.load('sector')` dataset, indexed by
DOCDB family ID. Later steps consume versioned enrichment tables keyed to this population.
Join and coverage contracts are specified in the [data dictionary](../docs/DATA_DICTIONARY.md).

| Step | Supported work and prerequisites |
|---|---|
| 0 · Dataset | Run the integrity notebook and benchmark. |
| 1 · Sector | Run the sector volume and CPC notebook. Temporal trends require verified family dates. |
| 2 · Competition | Normalize applicants, define entry windows and fractional family attribution, then add PEST sources. |
| 3 · Present value | Establish firm mapping, as-of dates, scoring inputs, weights and missing-data rules. |
| 4 · Future value | Add dated forward-looking inputs and evaluate against a separately specified temporal validation cohort. |
| 5 · Magic Quadrant | Use versioned Step 3 and Step 4 scores, common firm coverage and sensitivity around axis thresholds. |
| 6 · Recommendations | Synthesize validated findings and document strategic assumptions, alternatives and uncertainties. |
