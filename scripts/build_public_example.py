"""Build a small teaching subset from separately downloaded public PubChem records."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
from rdkit import Chem
from rdkit.Chem.Scaffolds import MurckoScaffold


def build(source, output):
    source, output = Path(source), Path(output)
    assay_file = source / 'pubchem_aid743139_concise.csv'
    assay_rows = list(csv.DictReader(assay_file.open(encoding='utf-8-sig')))
    outcomes = {}
    for row in assay_rows:
        if row['CID'] and row['Activity Outcome'] in {'Active', 'Inactive'}:
            outcomes.setdefault(int(row['CID']), set()).add(row['Activity Outcome'])
    properties = {}
    for path in sorted(source.glob('properties_*.json')):
        for record in json.loads(path.read_text())['PropertyTable']['Properties']:
            properties[record['CID']] = record.get('ConnectivitySMILES', record.get('CanonicalSMILES'))
    candidates, selected = [], set()
    for outcome, limit in [('Active', 96), ('Inactive', 288)]:
        count = 0
        for row in assay_rows:
            if row['Activity Outcome'] != outcome or not row['CID']:
                continue
            cid = int(row['CID'])
            if cid in selected:
                continue
            selected.add(cid)
            candidates.append({'cid': cid})
            count += 1
            if count == limit:
                break
    buckets = {(split, label): [] for split in ('train', 'validation') for label in (0, 1)}
    seen = set()
    for record in candidates:
        cid = record['cid']
        if len(outcomes.get(cid, set())) != 1:
            continue
        outcome = next(iter(outcomes[cid]))
        mol = Chem.MolFromSmiles(properties.get(cid, '') or '')
        if mol is None:
            continue
        smiles = Chem.MolToSmiles(mol, canonical=True, isomericSmiles=True)
        if smiles in seen:
            continue
        seen.add(smiles)
        scaffold = MurckoScaffold.GetScaffoldForMol(mol)
        generic = Chem.MolToSmiles(MurckoScaffold.MakeScaffoldGeneric(scaffold)) if scaffold.GetNumAtoms() else 'ACYCLIC'
        digest = hashlib.sha256(generic.encode()).hexdigest()
        split = 'validation' if int(digest[:8], 16) % 4 == 0 else 'train'
        label = int(outcome == 'Active')
        buckets[(split, label)].append({
            'canonical_smiles': smiles, 'label': label, 'record_id': f'pubchem743139_cid{cid}',
            'generic_scaffold_id': 'generic_' + digest[:16], 'pubchem_cid': cid,
            'source_activity_outcome': outcome})
    output.mkdir(parents=True, exist_ok=True)
    for split, quotas in [('train', {0: 72, 1: 24}), ('validation', {0: 24, 1: 8})]:
        records = []
        for label, count in quotas.items():
            available = buckets[(split, label)]
            if len(available) < count:
                raise ValueError(f'Insufficient public candidates for {split}, label {label}')
            records.extend(available[:count])
        records.sort(key=lambda row: row['pubchem_cid'])
        with (output / f'{split}.csv').open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(records[0]), lineterminator='\n')
            writer.writeheader()
            writer.writerows(records)
    manifest = {
        'dataset': 'Public PubChem AID 743139 teaching subset',
        'assay_name': 'qHTS assay to identify aromatase inhibitors: Summary',
        'assay_url': 'https://pubchem.ncbi.nlm.nih.gov/bioassay/743139',
        'assay_download_url': 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/743139/concise/CSV',
        'property_api': 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{CID_LIST}/property/CanonicalSMILES/JSON',
        'retrieved_date': '2026-10-27',
        'labels': {'1': 'PubChem Activity Outcome = Active', '0': 'PubChem Activity Outcome = Inactive'},
        'selection': 'First 96 unique active and 288 unique inactive CIDs in source order form the downloaded candidate pool. Conflicting active/inactive labels, invalid structures and duplicate canonical structures are removed. No model scores used.',
        'split_rule': 'SHA256(generic Murcko scaffold SMILES), first 8 hex digits modulo 4: 0 for validation, others for train; empty scaffolds share ACYCLIC group.',
        'teaching_quotas': {'train': {'negative': 72, 'positive': 24}, 'validation': {'negative': 24, 'positive': 8}},
        'scope': 'Class-enriched workflow example, not assay population prevalence or research benchmark; unrelated to unpublished project splits and results.',
        'source_assay_sha256': hashlib.sha256(assay_file.read_bytes()).hexdigest(),
        'files': {name: hashlib.sha256((output / name).read_bytes()).hexdigest() for name in ['train.csv', 'validation.csv']},
        'rights': 'Public NIH/NCATS assay records accessed through PubChem. Original source terms apply; not relicensed as team-owned data.',
    }
    (output / 'source_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, help='Directory of downloaded public assay and property files')
    parser.add_argument('--output', default='data/example')
    args = parser.parse_args()
    print(json.dumps(build(args.source, args.output), ensure_ascii=False, indent=2))
