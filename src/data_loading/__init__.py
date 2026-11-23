"""Canonical family-level data access for every project step."""
import csv
import os
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
MASTER = Path('data/final/TEAM12_PATENTS_5317_FINAL.csv')
SECTOR = Path('data/final/TEAM12_SECTOR_RELEVANT_CORE_ENABLING.csv')
REFERENCE = Path('data/reference/TEAM12_GROUND_TRUTH_HUMAN_REVIEWED_300.csv')
LABELS = ('CORE', 'ENABLING', 'IRRELEVANT')
RELEVANT = frozenset(LABELS[:2])


def read_rows(path):
    with path.open(encoding='utf-8-sig', newline='') as handle:
        return list(csv.DictReader(handle))


def load(kind='sector', *, root=None):
    """Return CSV rows without numeric coercion of identifiers."""
    path = {'master': MASTER, 'sector': SECTOR, 'reference': REFERENCE}[kind]
    base = Path(root or os.environ.get('TEAM12_DATA_ROOT', REPOSITORY))
    if not (base / path).is_file():
        raise FileNotFoundError(
            f'Missing {base / path}. Extract the private Team 12 dataset into '
            'the repository root or set TEAM12_DATA_ROOT to its root.'
        )
    return read_rows(base / path)


def index_by_family(rows):
    index = {}
    for row in rows:
        family_id = row['docdb_family_id']
        if not family_id.isascii() or not family_id.isdigit() or family_id in index:
            raise ValueError(f'Invalid or duplicate DOCDB family ID: {family_id!r}')
        index[family_id] = row
    return index
