"""Interface contract example only: validate a candidate and prepare an offline task card.

This entry point parses a candidate and prepares its local task configuration.
"""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from historical_case import policy_literal


def prepare(source):
    return {
        'mode': 'OFFLINE_INTERFACE_EXAMPLE', 'network_calls': False,
        'policy': policy_literal(source),
        'student_must_define': ['question', 'data_split', 'objective', 'fixed_conditions',
                                'evaluation_rule', 'budget', 'stop_rule', 'heldout_plan'],
        'online_status': 'Requires Baidu-confirmed SDK/API, account, quota, permissions and trusted evaluator binding',
        'evaluation_status': 'Evaluation results are produced by actual training and the bound evaluator',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('candidate', type=Path)
    args = parser.parse_args()
    print(json.dumps(prepare(args.candidate.read_text(encoding='utf-8')), ensure_ascii=False, indent=2))
