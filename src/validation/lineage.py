"""Verify the master against the original source records in an authorized extract."""
import argparse
import json
import sqlite3
from pathlib import Path

from src.data_loading import index_by_family, read_rows
from src.validation.dataset import validate


def decisions(database, statement):
    with sqlite3.connect(database.as_uri() + '?mode=ro', uri=True) as handle:
        if handle.execute('PRAGMA integrity_check').fetchone() != ('ok',):
            raise ValueError(f'Checkpoint integrity failed: {database.name}')
        return [(str(key), json.loads(payload)) for key, payload in handle.execute(statement)]


def check(integration):
    master, reference = validate()
    inputs = integration / 'inputs'
    candidates = index_by_family(read_rows(inputs / 'TEAM12_TEST_CANDIDATES.csv'))
    if list(candidates) != list(master):
        raise ValueError('Master changed the original family universe or order')
    for key, source in candidates.items():
        if any(master[key][column] != value for column, value in source.items()):
            raise ValueError(f'Original source text or metadata changed for {key}')
    consumed = set()
    datasets = [
        ('QWEN_GPU', decisions(inputs / 'QWEN_CHECKPOINT_569.sqlite', 'SELECT id,payload FROM done')),
        ('CODEX_LOCAL', decisions(inputs / 'CODEX_LOCAL_CHECKPOINT_1070.sqlite', 'SELECT id,row_json FROM done')),
    ]
    for cohort, filename in [
        ('CLAUDE_CODE_WEB', 'CLAUDE_CODE_FINAL_1500.csv'),
        ('CODEX_WEB_SUBAGENTS', 'CODEX_WEB_FINAL_1500.csv'),
    ]:
        datasets.append((cohort, list(index_by_family(read_rows(inputs / filename)).items())))
    complete = [
        (row['docdb_family_id'], row)
        for path in sorted((integration / 'completions/parts').glob('*.json'))
        for row in json.loads(path.read_text(encoding='utf-8'))['decisions']
    ]
    datasets.append(('CODEX_COMPLETION', complete))
    for cohort, items in datasets:
        for key, source in items:
            if key in consumed:
                raise ValueError(f'Duplicate source decision for {key}')
            consumed.add(key)
            row = master[key]
            label = source.get('final_policy_label', source.get('label'))
            if row['engine_provider'] != cohort or row['final_policy_label'] != label:
                raise ValueError(f'Classification lineage changed for {key}')
            for field in ('policy_sha256', 'model_requested', 'annotation_status'):
                if field in source and row[field] != source[field]:
                    raise ValueError(f'Source {field} changed for {key}')
            if 'engine_provider' in source and row['source_engine_provider'] != source['engine_provider']:
                raise ValueError(f'Original engine value changed for {key}')
    if consumed != master.keys():
        raise ValueError('Master and source decision universe differ')
    audited = index_by_family(read_rows(integration / 'benchmark/ASTRA_300_AI_REFERENCE.csv'))
    if {key: value['final_policy_label'] for key, value in audited.items()} != {
        key: value['final_policy_label'] for key, value in reference.items()
    }:
        raise ValueError('Human reference no longer matches the historical Astra labels')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--integration', type=Path, required=True)
    args = parser.parse_args()
    check(args.integration.resolve())
    print('Verified original family order, metadata, all 5,317 source labels, provenance and reference IDs')
