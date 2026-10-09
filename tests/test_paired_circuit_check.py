"""The independent paired-circuit checker accepts the real circuit and rejects mutations."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "formal" / "circuit" / "export_paired.py"
CHECK = ROOT / "formal" / "circuit" / "check_paired.py"


def run(path):
    return subprocess.run([sys.executable, "-I", str(CHECK), str(path)],
                          capture_output=True, text=True)


class PairedCircuitCheck(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.graph = Path(cls.tmp.name) / "c14.json"
        subprocess.run([sys.executable, str(EXPORT), str(cls.graph), "14"], check=True)
        cls.data = json.loads(cls.graph.read_text())

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_real_circuit_passes(self):
        result = run(self.graph)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("R = c + q = 7444", result.stdout)

    def test_mutations_fail(self):
        keys = sorted(self.data["args"], key=int)
        mutants = []
        d = copy.deepcopy(self.data); k = keys[len(keys) // 2]
        d["args"][k] = [d["args"][k][0]] * 2; mutants.append(d)
        d = copy.deepcopy(self.data); d["outputs"][5][2] = d["outputs"][6][2]; mutants.append(d)
        d = copy.deepcopy(self.data); d["outputs"] = d["outputs"][:-1]; mutants.append(d)
        for i, mutant in enumerate(mutants):
            path = Path(self.tmp.name) / f"mutant{i}.json"
            path.write_text(json.dumps(mutant))
            self.assertNotEqual(run(path).returncode, 0, f"mutant {i} was accepted")


if __name__ == "__main__":
    unittest.main()
