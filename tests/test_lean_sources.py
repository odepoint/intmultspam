"""The Lean source table cites lines and certificate values that still match."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "formal" / "lean"))
import sources


class LeanSources(unittest.TestCase):
    def test_every_declaration_cites_current_lines_and_values(self):
        self.assertEqual(sources.check(), [])

    def test_table_is_regenerated(self):
        table = (ROOT / "formal" / "lean" / "SOURCES.md").read_text()
        self.assertEqual(table, sources.render())


if __name__ == "__main__":
    unittest.main()
