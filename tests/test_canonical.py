import unittest

from src.data_loading import LABELS, index_by_family, load
from src.validation.dataset import validate


class CanonicalContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.master, cls.reference = validate()

    def test_full_coverage_and_allowed_labels(self):
        self.assertEqual(len(self.master), 5317)
        self.assertEqual({r['final_policy_label'] for r in self.master.values()}, set(LABELS))

    def test_sector_is_exact_ordered_filter(self):
        expected = [r for r in self.master.values() if r['final_policy_label'] in LABELS[:2]]
        self.assertEqual(load('sector'), expected)

    def test_benchmark_join_uses_family_id(self):
        self.assertEqual(len(self.reference.keys() & self.master.keys()), 300)
        self.assertTrue(all(key == row['docdb_family_id'] for key, row in self.reference.items()))

    def test_duplicate_id_rejected(self):
        row = next(iter(self.master.values()))
        with self.assertRaises(ValueError):
            index_by_family([row, row])


if __name__ == '__main__':
    unittest.main()
