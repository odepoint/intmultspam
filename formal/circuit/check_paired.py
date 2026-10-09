"""Independent check of the paired bit side circuit behind R = 509194.

Reads only the graph written by `export_paired.py` and imports nothing from this repo.
Recomputes every support from scratch as a dense bitset over all C(50,3) triples, with
its own triple indexing, and checks the claims the network count relies on:

1. the graph is a DAG on earlier nodes, and every addition adds disjoint supports;
2. every partial output (i, T) has support exactly {S : i in S, S cap T = {i}};
3. per target T, the three partial outputs partition {S : |S cap T| = 1};
4. every node's triples share a common point (nondegeneracy of U_z under I - J/9);
5. the note's role allocation (one role per outgoing use at inputs, pivot reuse at
   additions, fresh slots) gives c + q roles; at h = 50, c = 450394, q = 58800 and
   R = 509194 (`notes/paired-construction.tex` lines 63 and 69-74).

Usage: python3 formal/circuit/check_paired.py GRAPH.json
"""
from itertools import combinations
import json
import sys

data = json.load(open(sys.argv[1]))
H = data['h']
triples = list(combinations(range(H), 3))
index = {t: i for i, t in enumerate(triples)}
assert [tuple(t) for t in data['inputs']] == triples, 'input order differs from C(50,3) order'
V = len(triples)
args = {int(k): tuple(v) for k, v in data['args'].items()}
outputs = [(i, tuple(t), n) for i, t, n in data['outputs']]

# reachable nodes from the outputs (our own pruning)
active = set(); stack = [n for _, _, n in outputs]
while stack:
    n = stack.pop()
    if n in active: continue
    active.add(n)
    if n in args: stack.extend(args[n])
adds = sorted(n for n in active if n in args)
ins = sorted(n for n in active if n not in args)
assert all(1 <= n <= V for n in ins), 'a leaf is not an input triple'

# use counts, to free supports early
uses = {}
for n in adds:
    for x in args[n]: uses[x] = uses.get(x, 0) + 1
want = {}
for i, T, n in outputs: want.setdefault(n, []).append((i, T))
for n in want: uses[n] = uses.get(n, 0) + len(want[n])

point_mask = [sum(1 << p for p in t) for t in triples]
support, core = {}, {}
for n in ins:
    support[n] = 1 << (n - 1); core[n] = point_mask[n - 1]
remaining = dict(uses)
expected_out = {}
by_target = {}
checked_out = 0

def expected(i, T):
    rest = [p for p in range(H) if p not in T]
    bits = 0
    for a, b in combinations(rest, 2):
        bits |= 1 << index[tuple(sorted((i, a, b)))]
    return bits

def release(x):
    remaining[x] -= 1
    if remaining[x] == 0 and x in support:
        del support[x]; del core[x]

order = sorted(active)
for n in order:
    if n in args:
        a, b = args[n]
        assert a < n and b < n, ('not topological', n)
        A, B = support[a], support[b]
        assert A & B == 0, ('overlapping supports', n)
        support[n] = A | B; core[n] = core[a] & core[b]
        assert core[n], ('no common point', n)
        release(a); release(b)
    for i, T in want.get(n, ()):
        assert core[n] >> i & 1
        assert support[n] == expected(i, T), ('wrong output', i, T)
        by_target.setdefault(T, []).append(support[n])
        checked_out += 1
        release(n)

for T in triples:
    parts = by_target[T]
    assert len(parts) == 3
    union = 0
    for p in parts:
        assert union & p == 0; union |= p
    tm = point_mask[index[T]]
    nbr = sum(1 << k for k, pm in enumerate(point_mask) if (pm & tm).bit_count() == 1)
    assert union == nbr and nbr.bit_count() == 3 * (H - 3) * (H - 4) // 2

# role allocation exactly as described in the note (fresh slots, pivot reuse)
users = {n: 0 for n in active}
for n in adds:
    for x in args[n]: users[x] += 1
for _, _, n in outputs: users[n] += 1
assert all(users[n] >= 1 for n in active)
roles = sum(users[n] for n in ins) + sum(users[n] - 1 for n in adds)

c, q = len(adds), len(outputs)
print(dict(additions=c, outputs=q, roles=roles, inputs_used=len(ins),
           outputs_checked=checked_out, targets_partitioned=len(by_target)))
assert q == H * (H - 1) * (H - 2) // 2 and roles == c + q
if H == 50:
    assert (c, q, roles) == (450394, 58800, 509194)
print(f'OK: h = {H}, R = c + q = {roles}; all supports disjoint, all outputs exact')
