#!/usr/bin/env python3
"""Export the paired global bit side circuit exactly as `scripts/paired_network.py` builds it.

Usage: python3 formal/circuit/export_paired.py OUT.json [h]   (default h = 50)
The output holds only the graph; `check_paired.py` verifies it without this repo's code.
"""
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
from paired_network import circuit

h = int(sys.argv[2]) if len(sys.argv) > 2 else 50
c = circuit(h)
active = sorted(c.active)
json.dump(dict(h=c.h, inputs=c.inputs,
               args={n: c.args[n] for n in active if c.args[n]},
               outputs=[[i, list(t), n] for (i, t), n in sorted(c.outputs.items())]),
          open(sys.argv[1], 'w'))
