# Independent check of the R = 509194 paired circuit

`export_paired.py` writes the global h = 50 bit side circuit exactly as
`scripts/paired_network.py` builds it. `check_paired.py` reads only that graph,
imports nothing from this repository, recomputes every support from scratch as a dense
bitset over all C(50,3) triples, and checks:

1. every addition joins two earlier nodes with disjoint supports;
2. every partial output (i, T) is exactly {S : i ∈ S, S ∩ T = {i}};
3. each target's three partial outputs partition its intersection-one neighbors;
4. every node's triples share a common point (the hypothesis of
   `KappaCheck.Frames.label_anisotropic`);
5. the role allocation of `notes/paired-construction.tex` gives c + q roles:
   c = 450394, q = 58800, R = 509194.

```
python3 formal/circuit/export_paired.py /tmp/c50.json
python3 -I formal/circuit/check_paired.py /tmp/c50.json   # about 2 minutes
```

`tests/test_paired_circuit_check.py` runs the same checker at h = 14 and confirms that
three mutated circuits are rejected.

Not covered: that the scalar schedule built from these roles realizes the network
interface. The paired-network tests simulate it on small cases.
