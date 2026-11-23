"""Describe coverage and the sector technology mix without reclassifying records."""
import argparse
import json
from collections import Counter
from pathlib import Path

from src.data_loading import load

SOURCE_FIELDS = (
    'docdb_family_id', 'appln_title', 'appln_abstract', 'cpc_codes',
    'source_channel', 'representative_appln_id', 'title_appln_id', 'abstract_appln_id',
    'title_language', 'abstract_language',
)


def profile():
    master, sector = load('master'), load('sector')
    cpc = Counter()
    for row in sector:
        codes = {''.join(c.split())[:4] for c in row['cpc_codes'].split('|') if c.strip()}
        cpc.update(codes)
    return {
        'master_families': len(master),
        'sector_families': len(sector),
        'labels': dict(Counter(r['final_policy_label'] for r in master)),
        'source_field_nonempty': {
            field: sum(bool(row[field].strip()) for row in master) for field in SOURCE_FIELDS
        },
        'source_channels': dict(Counter(r['source_channel'] for r in master)),
        'sector_segments': dict(Counter(r['technology_segment'] or 'UNSPECIFIED' for r in sector)),
        'sector_cpc_subclass_family_counts': dict(sorted(cpc.items())),
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    content = json.dumps(profile(), indent=2) + '\n'
    if args.output:
        args.output.write_text(content, encoding='utf-8')
    else:
        print(content, end='')
