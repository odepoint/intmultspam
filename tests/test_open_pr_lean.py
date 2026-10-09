"""Drift tests for the Lean checks of open PRs #3-#12, and the vendored PR data."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
OPEN = ROOT / "formal" / "open-prs"


class OpenPullRequestLean(unittest.TestCase):
    def test_vendored_data_matches_manifest(self):
        manifest = json.loads((OPEN / "data" / "MANIFEST.json").read_text())
        on_disk = {p.relative_to(OPEN / "data").as_posix()
                   for p in (OPEN / "data").rglob("*") if p.is_file()} - {"MANIFEST.json"}
        self.assertEqual(on_disk, set(manifest["sha256"]))
        for rel, digest in manifest["sha256"].items():
            self.assertEqual(hashlib.sha256((OPEN / "data" / rel).read_bytes()).hexdigest(),
                             digest, rel)

    def test_drift(self):
        for script, args in (("drift_A.py", []), ("drift_B.py", ["--selftest"]),
                             ("drift_C.py", [])):
            result = subprocess.run([sys.executable, "-I", str(OPEN / script), *args],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, script + "\n" + result.stdout + result.stderr)
            self.assertTrue(result.stdout.strip().splitlines()[-1].startswith("OK"), script)


if __name__ == "__main__":
    unittest.main()
