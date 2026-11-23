"""Evaluate fixed model predictions against the separate human-reviewed labels."""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from src.data_loading import LABELS, RELEVANT
from src.validation.dataset import validate


def scores(pairs, labels):
    matrix = {truth: {label: 0 for label in labels} for truth in labels}
    for truth, prediction in pairs:
        matrix[truth][prediction] += 1
    n = len(pairs)
    measures = {}
    for label in labels:
        tp = matrix[label][label]
        support = sum(matrix[label].values())
        predicted = sum(matrix[truth][label] for truth in labels)
        precision = tp / predicted if predicted else 0.0
        recall = tp / support if support else 0.0
        measures[label] = {
            'precision': precision, 'recall': recall,
            'f1': 2 * tp / (support + predicted) if support + predicted else 0.0,
            'support': support, 'predicted': predicted,
        }
    accuracy = sum(matrix[label][label] for label in labels) / n
    expected = sum(item['support'] * item['predicted'] for item in measures.values()) / n**2
    return {
        'n': n, 'accuracy': accuracy,
        'macro_f1': sum(item['f1'] for item in measures.values()) / len(labels),
        'weighted_f1': sum(item['support'] * item['f1'] for item in measures.values()) / n,
        'cohen_kappa': (accuracy - expected) / (1 - expected) if expected != 1 else None,
        'per_class': measures, 'matrix_reference_rows_prediction_columns': matrix,
    }


def evaluate(root=None):
    master, reference = validate(root)
    pairs = []
    groups = defaultdict(list)
    for family, reference_row in reference.items():
        candidate = master[family]
        pair = reference_row['final_policy_label'], candidate['final_policy_label']
        pairs.append(pair)
        groups[candidate['engine_provider']].append(pair)

    def relevance(label):
        return 'RELEVANT' if label in RELEVANT else 'IRRELEVANT'

    return {
        'benchmark_provenance': 'Initially AI-assisted; human review confirmed by Team 12. Review independence and procedure are unverified.',
        'coverage': {'evaluated': len(pairs), 'reference': len(reference)},
        'master_label_counts': dict(Counter(r['final_policy_label'] for r in master.values())),
        'three_class': scores(pairs, LABELS),
        'binary_relevance': scores([(relevance(t), relevance(p)) for t, p in pairs], ('RELEVANT', 'IRRELEVANT')),
        'per_cohort': {key: scores(items, LABELS) for key, items in sorted(groups.items())},
    }


def chart(figures, result):
    figures.mkdir(parents=True, exist_ok=True)
    counts = result['three_class']['matrix_reference_rows_prediction_columns']
    largest = max(max(row.values()) for row in counts.values())
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="680" height="445" viewBox="0 0 680 445">',
           '<title>Three-class confusion matrix on 300 human-reviewed patent families</title>',
           '<rect width="680" height="445" fill="white"/>',
           '<g font-family="sans-serif" fill="#17324a">',
           '<text x="30" y="36" font-size="21" font-weight="bold">Classification confusion matrix</text>',
           '<text x="30" y="64" font-size="14">Rows are human-reviewed labels · columns are predictions</text>']
    for j, label in enumerate(LABELS):
        svg.append(f'<text x="{239 + j*145}" y="104" text-anchor="middle" font-size="14">{label}</text>')
    for i, truth in enumerate(LABELS):
        y = 122 + i*95
        svg.append(f'<text x="156" y="{y+49}" text-anchor="end" font-size="14">{truth}</text>')
        for j, pred in enumerate(LABELS):
            x = 170 + j*145
            value = counts[truth][pred]
            opacity = 0.10 + 0.85*value/largest
            color = 'white' if opacity > 0.57 else '#17324a'
            svg.append(f'<rect x="{x}" y="{y}" width="138" height="88" rx="5" fill="#12537b" fill-opacity="{opacity:.3f}"/>')
            svg.append(f'<text x="{x+69}" y="{y+51}" text-anchor="middle" font-size="22" fill="{color}">{value}</text>')
    svg += ['</g>', '</svg>']
    (figures / 'human_reference_confusion_matrix.svg').write_text('\n'.join(svg) + '\n', encoding='utf-8')


def class_score_chart(figures, result):
    colors = {'precision': '#155279', 'recall': '#347d68', 'f1': '#784972'}
    per_class = result['three_class']['per_class']
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="680" height="365" viewBox="0 0 680 365">',
           '<title>Precision, recall and F1 per benchmark class</title>',
           '<rect width="680" height="365" fill="white"/>',
           '<g font-family="sans-serif" fill="#17324a">',
           '<text x="26" y="38" font-size="22" font-weight="bold">Benchmark scores by class</text>']
    for tick in range(6):
        x = 164 + 91 * tick
        svg.append(f'<path d="M{x} 73V300" stroke="#e7edf1"/>')
        svg.append(f'<text x="{x}" y="321" text-anchor="middle" font-size="12">{tick / 5:.1f}</text>')
    for index, label in enumerate(LABELS):
        y = 83 + 73 * index
        svg.append(f'<text x="151" y="{y+29}" text-anchor="end" font-size="14">{label}</text>')
        for offset, (metric, color) in enumerate(colors.items()):
            value = per_class[label][metric]
            position = y + 18 * offset
            width = 455 * value
            svg.append(f'<rect x="164" y="{position}" width="{width:.2f}" height="14" fill="{color}"/>')
            svg.append(f'<text x="{169+width:.2f}" y="{position+12}" font-size="12">{value:.3f}</text>')
    for index, (metric, color) in enumerate(colors.items()):
        x = 165 + 125 * index
        svg.append(f'<rect x="{x}" y="335" width="12" height="12" fill="{color}"/>')
        svg.append(f'<text x="{x+17}" y="346" font-size="13">{metric.upper() if metric == "f1" else metric.title()}</text>')
    svg += ['</g>', '</svg>']
    (figures / 'human_reference_class_scores.svg').write_text('\n'.join(svg) + '\n', encoding='utf-8')


def report(path, result):
    lines = [
        '# Evaluation against the 300-family human-reviewed benchmark', '',
        result['benchmark_provenance'], '',
        'The supplied labels exactly match the historical Astra AI artifact. Both comparisons therefore '
        'have the same numbers and represent a single benchmark, with updated human-review provenance.', '',
        '## Overall and cohort results', '',
        '| Evaluation | Families | Accuracy | Macro F1 | Weighted F1 | Cohen’s κ |',
        '|---|---:|---:|---:|---:|---:|',
    ]
    evaluations = [
        ('Three-class', result['three_class']), ('Binary relevance', result['binary_relevance']),
        *result['per_cohort'].items(),
    ]
    for name, item in evaluations:
        kappa = item['cohen_kappa']
        lines.append(f"| {name} | {item['n']} | {item['accuracy']:.4f} | {item['macro_f1']:.4f} | "
                     f"{item['weighted_f1']:.4f} | {f'{kappa:.4f}' if kappa is not None else 'Undefined'} |")
    for name, item in evaluations[:2]:
        matrix = item['matrix_reference_rows_prediction_columns']
        labels = list(matrix)
        lines += ['', f'## {name}', '',
                  '| Class | Precision | Recall | F1 | Support |',
                  '|---|---:|---:|---:|---:|']
        for label, row in item['per_class'].items():
            lines.append(f"| {label} | {row['precision']:.4f} | {row['recall']:.4f} | {row['f1']:.4f} | {row['support']} |")
        lines += ['', '| Reference ↓ / Prediction → | ' + ' | '.join(labels) + ' |',
                  '|---|' + '---:|' * len(labels)]
        for label in labels:
            lines.append('| ' + ' | '.join([label, *(str(matrix[label][p]) for p in labels)]) + ' |')
    lines += [
        '', '![Human-reviewed benchmark confusion matrix](../figures/human_reference_confusion_matrix.svg)', '',
        '## Limitations', '',
        'The candidate frame was prefiltered. The benchmark selection probabilities, annotator identities, '
        'review procedure and adjudication history are unavailable. ASTRA V4 examples include benchmark '
        'families and the reference informed the methodology, so some evaluation leakage is possible.',
        'Cohorts were assigned different families and Qwen used Q9.3. Compare their results descriptively '
        'with the class support recorded in the JSON file. A zero-denominator class score is reported as zero.',
        'Retrieval recall requires judgments outside the candidate set or an independent relevant-patent universe.',
    ]
    path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--reports', type=Path, default=Path('reports'))
    args = parser.parse_args()
    metrics = evaluate()
    out = args.reports / 'evaluation'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'human_reference_metrics.json').write_text(json.dumps(metrics, indent=2) + '\n')
    report(out / 'BENCHMARK.md', metrics)
    chart(args.reports / 'figures', metrics)
    class_score_chart(args.reports / 'figures', metrics)
