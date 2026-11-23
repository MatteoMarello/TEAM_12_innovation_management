# Reproducibility

Python 3.10+ and the standard library are sufficient for the pipeline. Run commands from
the repository root. Extract the restricted dataset package at the root or point
`TEAM12_DATA_ROOT` to the extraction directory, which contains `data/`.

```bash
sha256sum -c docs/CANONICAL_SHA256SUMS.txt
python -m src.validation.dataset
python -m unittest discover -s tests -v
python -m src.evaluation.benchmark
python -m src.data_loading.profile --output reports/DATASET_PROFILE.json
```

Authorized users can independently regenerate all three canonical files from the private
integration package, which retains the immutable input snapshots, original reference,
completion decisions and offline consolidation scripts.

```bash
python -m src.classification.export_canonical --integration /path/to/TEAM12_MASTER_INTEGRATION_FOR_CODEX --destination . --checksum-file docs/CANONICAL_SHA256SUMS.txt
```

The exporter first runs strict consolidation and normalizes the original reference. It
checks the ordered family universe and metadata against the original candidate CSV. It
then writes the same ordered master and sector subset and reports their SHA-256 values.
The review and comparison scripts in the private integration folder regenerate audit
tables from committed decisions. They run no model inference. Reproducing stored outputs
and regenerating model judgments are distinct operations.

Open optional notebooks with a kernel that includes the repository on `PYTHONPATH`.
The notebooks use the same loader and never import an independently named CSV copy.
