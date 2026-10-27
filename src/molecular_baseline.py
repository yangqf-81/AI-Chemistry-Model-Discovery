"""Account-free ECFP4/LR foundation exercise; not the research GNN M0."""
import argparse
import csv
import hashlib
import json
import platform
from pathlib import Path

import numpy as np
import rdkit
import sklearn
from rdkit import Chem, DataStructs
from rdkit.Chem import rdFingerprintGenerator
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score

REQUIRED = {'canonical_smiles', 'label', 'record_id', 'generic_scaffold_id'}


def load_data(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        if not REQUIRED.issubset(reader.fieldnames or []):
            raise ValueError('Missing required CSV fields')
        rows = list(reader)
    if not rows:
        raise ValueError('Empty data')
    generator = rdFingerprintGenerator.GetMorganGenerator(
        radius=2, fpSize=2048, includeChirality=True)
    matrix = np.zeros((len(rows), 2048), dtype=np.uint8)
    labels, molecules, ids, scaffolds = [], set(), set(), set()
    for index, row in enumerate(rows):
        if row['label'] not in {'0', '1'}:
            raise ValueError('Labels must be 0 or 1')
        if not row['record_id'] or not row['generic_scaffold_id']:
            raise ValueError('Missing record or scaffold identity')
        mol = Chem.MolFromSmiles(row['canonical_smiles'])
        if mol is None:
            raise ValueError(f'Invalid SMILES at record {row["record_id"]}')
        identity = Chem.MolToSmiles(mol, canonical=True, isomericSmiles=True)
        if identity in molecules or row['record_id'] in ids:
            raise ValueError('Duplicate molecule or record within split')
        molecules.add(identity)
        ids.add(row['record_id'])
        scaffolds.add(row['generic_scaffold_id'])
        DataStructs.ConvertToNumpyArray(generator.GetFingerprint(mol), matrix[index])
        labels.append(int(row['label']))
    if set(labels) != {0, 1}:
        raise ValueError('Both classes are required')
    return rows, matrix, np.asarray(labels), molecules, ids, scaffolds


def check_boundaries(train, validation):
    for index, name in [(3, 'molecule'), (4, 'record'), (5, 'scaffold')]:
        if train[index] & validation[index]:
            raise ValueError(f'Train/validation {name} overlap')


def run(train_path, validation_path, output_path):
    train, validation = load_data(train_path), load_data(validation_path)
    check_boundaries(train, validation)
    model = LogisticRegression(
        solver='liblinear', class_weight='balanced', max_iter=1000, random_state=42)
    model.fit(train[1], train[2])
    score = model.decision_function(validation[1])
    probability = model.predict_proba(validation[1])[:, 1]
    if not np.isfinite(score).all() or not np.isfinite(probability).all():
        raise ValueError('Non-finite prediction')
    output = Path(output_path)
    output.mkdir(parents=True, exist_ok=True)
    metrics = {
        'model': 'ECFP4-2048 + balanced logistic regression; not GNN M0',
        'purpose': 'Foundation technical exercise; not student outcome or L6 reproduction',
        'train_rows': len(train[0]), 'validation_rows': len(validation[0]),
        'train_positive': int(train[2].sum()),
        'validation_positive': int(validation[2].sum()),
        'validation_prevalence': float(validation[2].mean()),
        'AP': float(average_precision_score(validation[2], score)),
        'AUROC': float(roc_auc_score(validation[2], score)),
        'input_sha256': {
            'train': hashlib.sha256(Path(train_path).read_bytes()).hexdigest(),
            'validation': hashlib.sha256(Path(validation_path).read_bytes()).hexdigest()},
        'environment': {'python': platform.python_version(), 'rdkit': rdkit.__version__,
                        'numpy': np.__version__, 'scikit_learn': sklearn.__version__},
    }
    with (output / 'predictions.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(['record_id', 'label', 'score', 'probability'])
        writer.writerows((row['record_id'], int(label), float(s), float(p))
                         for row, label, s, p in zip(validation[0], validation[2], score, probability))
    (output / 'metrics.json').write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return metrics


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--train', required=True)
    parser.add_argument('--validation', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.train, args.validation, args.output), ensure_ascii=False, indent=2))
