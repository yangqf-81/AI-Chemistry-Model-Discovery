"""Read genuine archived research results; never simulate a new model evaluation."""
import ast
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
AXES = {
    'fusion': ('concat', 'additive', 'film'),
    'projection_depth': (1, 2),
    'projection_hidden_multiplier': (0.5, 1, 2),
    'encoder_scope': ('frozen', 'top_block', 'full'),
    'w_off': (0, 0.25, 0.5),
    'lambda_anchor': (0, 0.1, 0.3, 1, 3),
}


def policy_literal(source):
    tree = ast.parse(source, mode='exec')
    if len(tree.body) != 1 or not isinstance(tree.body[0], ast.Assign):
        raise ValueError('Expected one literal POLICY assignment')
    stmt = tree.body[0]
    if len(stmt.targets) != 1 or not isinstance(stmt.targets[0], ast.Name) or stmt.targets[0].id != 'POLICY':
        raise ValueError('Only POLICY may be assigned')
    value = ast.literal_eval(stmt.value)
    if not isinstance(value, dict) or set(value) != set(AXES):
        raise ValueError('Unexpected policy keys')
    for key, options in AXES.items():
        if isinstance(value[key], bool) or value[key] not in options:
            raise ValueError('Illegal policy value: '+key)
    return value


def rows(name, directory=None):
    directory = Path(directory) if directory else ROOT/'examples/internal_historical'
    index = json.loads((directory/'source-index.json').read_text(encoding='utf-8'))
    path = directory/name
    if hashlib.sha256(path.read_bytes()).hexdigest() != index['files'][name]['sha256']:
        raise ValueError('Historical source changed: '+name)
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def summarize(directory=None):
    systems = rows('m1_systems.csv', directory)
    proposals = rows('l6_proposals.csv', directory)
    trajectory = rows('l6_trajectory.csv', directory)
    panel = rows('l6_system_metrics.csv', directory)
    grouped = defaultdict(list)
    for row in panel:
        grouped[row['policy_id']].append(row)
    for point in trajectory:
        values = grouped[point['policy_id']]
        if len(values) != 26 or len({x['system'] for x in values}) != 26:
            raise ValueError('Incomplete historical policy panel')
        if abs(mean(float(x['delta_net']) for x in values)-float(point['fitness'])) > 1e-12:
            raise ValueError('Historical score does not match table')
    policies = [policy_literal(row['source']) for row in proposals]
    validation = rows('validation5.csv', directory)
    return {
        'mode': 'HISTORICAL_REPLAY_ONLY; no platform call or new training',
        'm1_comparison': {'systems': len(systems),
            'mean_M1_minus_M0_AP': mean(float(x['M1_DeltaNet']) for x in systems),
            'positive_systems': sum(float(x['M1_DeltaNet']) > 0 for x in systems),
            'negative_systems': sum(float(x['M1_DeltaNet']) < 0 for x in systems)},
        'search': {'raw_proposals': len(proposals),
            'outcomes': dict(Counter(x['outcome'] for x in proposals)),
            'literal_policies_checked': len(policies), 'evaluated_policies': len(trajectory),
            'system_records': len(panel), 'all_published_fitness_recomputed': True},
        'heldout_system_case': {'systems': len(validation),
            'mean_L6_minus_M1_AP': mean(float(x['L6_minus_M1']) for x in validation),
            'scope': 'Held out relative to L6 selection; historical exposure and task-internal VAL early stopping disclosed'},
        'limitations': 'Historical scores are not scores for newly proposed policies; no searcher superiority or teaching-effect inference',
    }


if __name__ == '__main__':
    print(json.dumps(summarize(), ensure_ascii=False, indent=2))
