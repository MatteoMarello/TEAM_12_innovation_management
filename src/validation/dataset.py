"""Validate the master, sector subset and human reference contracts."""
from collections import Counter

from src.data_loading import LABELS, RELEVANT, index_by_family, load

EXPECTED = {
    'QWEN_GPU': 569,
    'CODEX_LOCAL': 1070,
    'CLAUDE_CODE_WEB': 1500,
    'CODEX_WEB_SUBAGENTS': 1500,
    'CODEX_COMPLETION': 678,
}


def validate(root=None):
    master = load('master', root=root)
    sector = load('sector', root=root)
    reference = load('reference', root=root)
    by_family = index_by_family(master)
    reference_index = index_by_family(reference)
    if len(by_family) != 5317 or any(r['final_policy_label'] not in LABELS for r in master):
        raise ValueError('Expected 5,317 unique, completely classified candidates')
    if sector != [r for r in master if r['final_policy_label'] in RELEVANT]:
        raise ValueError('Sector differs from the ordered CORE and ENABLING subset')
    if Counter(r['engine_provider'] for r in master) != EXPECTED:
        raise ValueError('Unexpected classification cohort coverage')
    for row in master:
        if not all(row.get(key, '').strip() for key in ('model_requested', 'policy_sha256', 'annotation_status')):
            raise ValueError(f'Missing provenance for {row["docdb_family_id"]}')
        original = row.get('source_engine_provider')
        if row['engine_provider'] == 'CODEX_LOCAL' and original != 'CODEX':
            raise ValueError('Original Codex local engine value was lost')
    if len(reference_index) != 300 or not reference_index.keys() <= by_family.keys():
        raise ValueError('Benchmark IDs must be 300 unique members of the master')
    if any(r['final_policy_label'] not in LABELS for r in reference):
        raise ValueError('Invalid benchmark label')
    return by_family, reference_index


if __name__ == '__main__':
    master, reference = validate()
    print(f'Validated {len(master)} classified families and {len(reference)} reference IDs')
