# Methodology

The project maps inventions relevant to Enel's utility-scale electricity energy storage
sector. The DOCDB family is the unit of analysis. The preserved collection flags whether
the candidate entered via CPC classes, keywords, or both. The handoff describes
PATSTAT/TIP sourcing and discusses BM25, Patent SBERT and score or rank fusion in the
retrieval pipeline. Its candidate export does not include scores, ranks, model revisions,
queries or fusion settings sufficient to re-run or verify those retrieval stages.

The master combines disjoint source cohorts using original family IDs.
Qwen 3.5 9B originally used the Q9.3 prompt. Local Codex, Codex web, Claude Code and the
completion run used complete ASTRA V4. The V4 rulebook separately establishes a technical
electricity-storage relationship (Gate S) and utility, network or stationary industrial
relevance (Gate U). CORE changes the physical mechanism or integrated storage architecture.
ENABLING supplies storage-specific technical support or operation. An exclusion records
at least one unestablished gate. Peak-shifting dispatch ordinarily operates an existing
store and is ENABLING under the policy. Existing labels remain fixed in the canonical snapshot.

The 678 completion families were obtained by set difference, divided into disjoint
assignments and independently annotated in native Codex sessions. Validation verifies
exact IDs, field schema, gates, source matches and preserved evidence. The label-free
assignment files excluded benchmark labels. Complete V4 contains worked examples that
overlap the benchmark, and shared storage prevents verification of full isolation.

Reviewed benchmark labels are preserved separately. The owner confirms human review of
all 300 initially AI-assisted labels. Annotator identities, independence, selection
probabilities, dates and adjudication records are unavailable. The audit and proposed
technical changes are AI-assisted. Sourcing restrictions and evidence completeness matter
when interpreting case disagreements, particularly title/abstract-only reviews of cases
with richer historical EP material.
