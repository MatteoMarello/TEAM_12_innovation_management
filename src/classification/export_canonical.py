"""Export the canonical layout from a strict, validated integration checkout."""
import argparse
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from src.data_loading import MASTER, REFERENCE, RELEVANT, SECTOR, index_by_family, read_rows


def write_rows(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f'Empty export for {path}')
    temp = path.with_suffix('.tmp')
    with temp.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
    temp.replace(path)


def export(integration, destination):
    for command in [('consolidate.py', '--strict-complete'), ('normalize_reference.py',)]:
        subprocess.run([sys.executable, 'scripts/' + command[0], *command[1:]], cwd=integration, check=True)
    rows = read_rows(integration / 'outputs/TEAM12_ALL_LABELLED_5317.csv')
    candidates = read_rows(integration / 'inputs/TEAM12_TEST_CANDIDATES.csv')
    master = index_by_family(rows)
    original = index_by_family(candidates)
    if len(master) != 5317 or list(master) != list(original):
        raise ValueError('Candidate IDs or source order changed')
    for key, row in original.items():
        if any(master[key][column] != value for column, value in row.items()):
            raise ValueError(f'Original metadata changed for {key}')
    reference = read_rows(integration / 'benchmark/TEAM12_GroundTruth_dataset_NORMALIZED.csv')
    if len(index_by_family(reference)) != 300 or not index_by_family(reference).keys() <= master.keys():
        raise ValueError('Invalid human benchmark join')
    exports = {
        MASTER: rows,
        SECTOR: [row for row in rows if row['final_policy_label'] in RELEVANT],
        REFERENCE: reference,
    }
    for path, data in exports.items():
        write_rows(destination / path, data)
    return {path.as_posix(): hashlib.sha256((destination / path).read_bytes()).hexdigest() for path in exports}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--integration', type=Path, required=True)
    parser.add_argument('--destination', type=Path, required=True)
    parser.add_argument('--checksum-file', type=Path)
    args = parser.parse_args()
    hashes = export(args.integration.resolve(), args.destination.resolve())
    lines = ''.join(f'{digest}  {path}\n' for path, digest in hashes.items())
    if args.checksum_file:
        args.checksum_file.write_text(lines, encoding='utf-8')
    print(lines, end='')
