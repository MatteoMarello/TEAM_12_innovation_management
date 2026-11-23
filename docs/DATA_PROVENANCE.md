# Data provenance and access

The master uses 569 Qwen, 1,070 local Codex, 1,500 Claude Code, 1,500 Codex web and
678 new Codex completion decisions. Each retains its source label. The private integration
release contains the original SQLite checkpoints, CSVs, policy hashes, inputs and logs.
The public repository contains aggregate metrics, a data contract, code and documentation.
`docs/CANONICAL_SHA256SUMS.txt` identifies the exact authorized dataset snapshot.

The integration handoff and human-reviewed benchmark on the Team 12 Drive were verified
byte-for-byte against the supplied source files. The compact package omits the redundant
repository ZIPs and derived intermediate files. Its packaged manifest uses earlier
hashes for two instruction files, `PROMPT_CODEX_UNICO_PER_REPO.md` and
`README_START_HERE_IT.md`. The immutable dataset and policy files matched their manifest
hashes. The private integration bundle preserves both instruction files as delivered.

EPO licensing rules depend on the product and source terms. The handoff provides no
documented authorization to republish this TIP/PATSTAT-derived snapshot or associated
texts on a public repository. Canonical CSVs, raw inputs, evidence-level audit files and
benchmark rows are available through the authorized private Team 12 Drive release.
Ask the repository maintainer for access to the exact checksum-identified release.
Confirm permissions for the actual source and dataset before any broader redistribution.
[EPO PATSTAT terms](https://www.epo.org/en/service-support/ordering/patstat-data-terms-and-conditions) · [EPO patent information product terms](https://www.epo.org/en/service-support/ordering/pi-terms-and-conditions)
