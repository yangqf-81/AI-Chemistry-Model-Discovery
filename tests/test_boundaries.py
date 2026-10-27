import csv
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from molecular_baseline import check_boundaries, load_data


class DataBoundaryTests(unittest.TestCase):
    def test_scaffold_overlap_is_rejected(self):
        train = (None, None, None, {'CCO'}, {'a'}, {'same'})
        validation = (None, None, None, {'CCN'}, {'b'}, {'same'})
        with self.assertRaisesRegex(ValueError, 'scaffold overlap'):
            check_boundaries(train, validation)

    def test_equivalent_smiles_are_duplicate(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'data.csv'
            with path.open('w', encoding='utf-8', newline='') as stream:
                writer = csv.writer(stream)
                writer.writerow(['canonical_smiles', 'label', 'record_id', 'generic_scaffold_id'])
                writer.writerows([['CCO', '0', 'a', 's1'], ['OCC', '1', 'b', 's2']])
            with self.assertRaisesRegex(ValueError, 'Duplicate molecule'):
                load_data(path)

    def test_missing_class_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'data.csv'
            path.write_text('canonical_smiles,label,record_id,generic_scaffold_id\nCCO,0,a,s1\n',
                            encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Both classes'):
                load_data(path)


if __name__ == '__main__':
    unittest.main()
