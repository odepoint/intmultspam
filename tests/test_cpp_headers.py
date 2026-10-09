"""Compile shared C++ headers without a caller's incidental includes."""

import os
from pathlib import Path
import shlex
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


class CppHeaderTests(unittest.TestCase):
    def test_binary_io_is_self_contained(self):
        source = r'''
#include "binary_io.hpp"
void exercise(std::ifstream& input, std::ofstream& output) {
    uint32_t header[4]{};
    std::vector<std::array<uint32_t, 2>> rows(1);
    normalize_le(rows.front());
    read_array(input, header);
    readv(input, rows);
    write_array(output, header);
}
'''
        result = subprocess.run(
            [*shlex.split(os.environ.get("CXX", "c++")), "-std=c++17",
             "-fsyntax-only", "-x", "c++", "-I",
             str(ROOT / "scripts/partial_swap"), "-"],
            input=source, text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
