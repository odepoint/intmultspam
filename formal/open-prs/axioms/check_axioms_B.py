#!/usr/bin/env python3
"""Generate Axioms.lean with `#print axioms` for every theorem in PRChecksB/*.lean, run it
with `lake env lean`, and check that only propext, Classical.choice and Quot.sound occur."""
from pathlib import Path
import re, subprocess, sys

HERE = Path(__file__).resolve().parent
LEAN_DIR = HERE.parents[1] / 'lean'
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}


def theorems():
    out = []
    for f in sorted((LEAN_DIR / 'PRChecksB').glob('*.lean')):
        stack = []
        for line in f.read_text().split('\n'):
            m = re.match(r'^namespace (\S+)', line)
            if m:
                stack.append(m.group(1)); continue
            m = re.match(r'^end (\S+)', line)
            if m and stack and stack[-1] == m.group(1):
                stack.pop(); continue
            m = re.match(r'^theorem (\S+)', line)
            if m:
                out.append('.'.join(stack + [m.group(1)]))
    return out


names = theorems()
src = 'import PRChecksB\n\n' + '\n'.join(f'#print axioms {n}' for n in names) + '\n'
(HERE / 'AxiomsB.lean').write_text(src)
res = subprocess.run(['lake', 'env', 'lean', str(HERE / 'AxiomsB.lean')], cwd=LEAN_DIR, capture_output=True, text=True)
text = res.stdout + res.stderr
(HERE / 'axioms-output-B.txt').write_text(text)
used, bad = set(), []
for m in re.finditer(r"'([^']+)' depends on axioms: \[([^\]]*)\]", text):
    axs = {a.strip() for a in m.group(2).split(',') if a.strip()}
    used |= axs
    if axs - ALLOWED:
        bad.append(f'{m.group(1)}: {sorted(axs - ALLOWED)}')
reported = len(re.findall(r"^'[^']+' (?:depends on axioms|does not depend on any axioms)", text, re.M))
if res.returncode or reported != len(names) or bad or re.search(r'(^|: )error', text, re.M):
    print(text[-3000:]); print('BAD:', bad, 'reported', reported, 'of', len(names)); sys.exit(1)
print(f'OK: {len(names)} theorems; axioms used: {sorted(used)}')
