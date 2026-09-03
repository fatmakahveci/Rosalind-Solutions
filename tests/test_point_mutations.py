import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "counting_point_mutations" / "counting_point_mutations.py"
SPEC = importlib.util.spec_from_file_location("point_mutations", MODULE_PATH)
point_mutations = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(point_mutations)


class PointMutationTests(unittest.TestCase):
    def calculate(self, first, second):
        with tempfile.TemporaryDirectory() as directory:
            input_path = Path(directory) / "sequences.txt"
            input_path.write_text(f"{first}\n{second}\n", encoding="utf-8")
            point_mutations.file_name = str(input_path)
            return point_mutations.calculate_point_mutations()

    def test_counts_hamming_distance(self):
        self.assertEqual(self.calculate("GAGCCT", "CATCGT"), 3)

    def test_identical_sequences_have_no_mutations(self):
        self.assertEqual(self.calculate("ACGT", "ACGT"), 0)


if __name__ == "__main__":
    unittest.main()
