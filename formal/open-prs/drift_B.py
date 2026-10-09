#!/usr/bin/env python3
"""Drift test: every annotated Lean literal equals the value in the PR's own certificate.

Each checked line of `PRChecksB/*.lean` ends with a tag

    <lean code ending in a literal>  -- json <certificate>.json <dotted.key.path>

(the `Key` refs of `formal/lean/sources.py`, written inline). The checked literal is the
last numeric literal `a` or `a / b` in the code part of the line. The certificate is read
from the worktree of the PR that the module checks (`MODULES`), at
`certificates/<certificate>.json`; list indices in paths are integers.

The test fails if
  * a tagged literal differs from the certificate value (exact `Fraction` comparison),
    or a tagged path does not exist, or a tagged line has no literal;
  * a core certificate value (`REQUIRED` prefixes: counts, eta, log bounds, guard,
    parameters, slacks, recurrence, margins, minimum, gap, ceiling) has no tag;
  * a definition whose body is a bare numeric literal, or a `Params` field, has no tag;
  * a Lean file contains `sorry`, `admit`, `native_decide` or an `axiom` declaration.

Usage: python3 drift.py [--selftest] [PR5=/path/to/worktree ...]
`--selftest` also perturbs one certificate value per module in memory and checks that
the test then reports exactly that tag.
"""
from fractions import Fraction
from pathlib import Path
import json
import re
import sys

HERE = Path(__file__).resolve().parent
LEAN = HERE.parent / 'lean' / 'PRChecksB'

# module -> PR worktree whose certificates it checks
MODULES = {
    'PR5': str(HERE / 'data' / 'pr5'),
    'PR5Analytic': str(HERE / 'data' / 'pr5'),
    'PR6': str(HERE / 'data' / 'pr6'),
    'PR7': str(HERE / 'data' / 'pr7'),
}

# (module, certificate) -> key prefixes whose numeric leaves must all be tagged
REQUIRED = {
    ('PR5', 'complex-network.json'): [
        'complex_counts.v', 'complex_counts.m', 'complex_counts.N', 'complex_counts.I',
        'complex_counts.W', 'complex_counts.L', 'complex_counts.s', 'complex_counts.deficit',
        'complex_counts.eta', 'complex_counts.side_roles_per_invocation',
        'complex_counts.original_side_wires_per_invocation', 'complex_deficit_slack',
        'complex_saving', 'bit_saving', 'log_m_upper', 'log_enclosure', 'gates',
        'scoped_ceiling.upper', 'improvement_over_compact_control', 'labels.active_nodes',
        'witness.guard', 'witness.parameters', 'witness.constraint_slacks', 'witness.recurrence',
        'witness.margins', 'witness.minimum_margin', 'witness.absorption_gap'],
    ('PR5', 'fast-gaussian.json'): [
        'complex_counts.W', 'complex_counts.s', 'complex_counts.eta', 'complex_saving',
        'bit_saving', 'scoped_ceiling.upper', 'improvement_over_compact_control',
        'improvement_over_compressed_complex', 'neumann_samples',
        'witness.guard', 'witness.parameters', 'witness.constraint_slacks', 'witness.recurrence',
        'witness.margins', 'witness.minimum_margin', 'witness.absorption_gap'],
    ('PR6', 'aligned-bit-network.json'): [
        'bit_counts.v', 'bit_counts.m', 'bit_counts.N', 'bit_counts.W', 'bit_counts.L',
        'bit_counts.s', 'bit_counts.deficit', 'bit_counts.eta', 'bit_counts.published_roles',
        'bit_counts.side_and_center_roles', 'bit_deficit_slack', 'bit_saving', 'complex_saving',
        'previous_bit_saving', 'previous_counts.deficit', 'log_m_upper', 'log_enclosure',
        'scoped_ceiling.upper', 'improvement_over_fast_gaussian',
        'witness.guard', 'witness.parameters', 'witness.constraint_slacks', 'witness.recurrence',
        'witness.margins', 'witness.minimum_margin', 'witness.absorption_gap'],
    ('PR7', 'prime-field28.json'): [
        'witness.bit.v', 'witness.bit.m', 'witness.bit.N', 'witness.bit.W', 'witness.bit.L',
        'witness.bit.D', 'witness.bit.s', 'witness.bit.eta', 'witness.bit.roles',
        'witness.bit.retained_totals', 'witness.complex.v', 'witness.complex.m',
        'witness.complex.N', 'witness.complex.I', 'witness.complex.W', 'witness.complex.L',
        'witness.complex.D', 'witness.complex.s', 'witness.complex.eta', 'witness.complex.roles',
        'witness.complex.scalar_gates', 'witness.deficit_slacks', 'witness.log_upper',
        'witness.guard', 'witness.parameters', 'witness.constraints', 'witness.recurrence',
        'witness.margins', 'witness.minimum_margin', 'witness.absorption_gap'],
}

TAG = re.compile(r'--\s*json\s+(\S+\.json)\s+(\S+)\s*$')
LIT = re.compile(r'(?<![\w.])(\d+)(?:\s*/\s*(\d+))?(?![\w.])')
NUMERIC = re.compile(r'^-?\d+(?:/\d+)?$')
FORBIDDEN = [(re.compile(r'\bsorry\b'), 'sorry'), (re.compile(r'\badmit\b'), 'admit'),
             (re.compile(r'native_decide'), 'native_decide'),
             (re.compile(r'^\s*(?:private\s+)?axiom\b', re.M), 'axiom declaration')]


def strip_comments(text):
    text = re.sub(r'/-.*?-/', lambda m: '\n' * m.group(0).count('\n'), text, flags=re.S)
    return re.sub(r'--[^\n]*', '', text)


def at(data, path):
    for k in path.split('.'):
        data = data[int(k)] if isinstance(data, list) else data[k]
    return data


def leaves(data, prefix=''):
    if isinstance(data, dict):
        for k, v in data.items():
            yield from leaves(v, f'{prefix}.{k}' if prefix else k)
    elif isinstance(data, list):
        for i, v in enumerate(data):
            yield from leaves(v, f'{prefix}.{i}' if prefix else str(i))
    elif not isinstance(data, bool) and NUMERIC.match(str(data)):
        yield prefix, data


def tags():
    """Yield (module, file, line number, literal text, certificate, path)."""
    for f in sorted(LEAN.glob('*.lean')):
        for n, line in enumerate(f.read_text().split('\n'), 1):
            m = TAG.search(line)
            if not m:
                continue
            code = line[:line.index('--')]
            lits = list(LIT.finditer(code))
            yield f.stem, f, n, (lits[-1].group(0) if lits else None), m.group(1), m.group(2)


def check(roots, overrides=None):
    overrides = overrides or {}
    errors, cache, seen, count = [], {}, set(), 0
    for module, f, n, lit, cert, path in tags():
        where = f'{f.name}:{n}'
        if module not in roots:
            errors.append(f'{where}: module {module} has no PR worktree')
            continue
        root = roots[module]
        key = (root, cert)
        if key not in cache:
            try:
                cache[key] = json.loads((Path(root) / 'certificates' / cert).read_text())
            except FileNotFoundError:
                errors.append(f'{where}: {root}/certificates/{cert} not found')
                cache[key] = None
        if cache[key] is None:
            continue
        try:
            value = overrides.get((root, cert, path), at(cache[key], path))
        except (KeyError, IndexError, ValueError):
            errors.append(f'{where}: {cert} has no key {path}')
            continue
        if lit is None:
            errors.append(f'{where}: no literal before the tag for {cert} {path}')
            continue
        lean = Fraction(int(re.sub(r'\s', '', lit).split('/')[0]),
                        int(re.sub(r'\s', '', lit).split('/')[1]) if '/' in lit else 1)
        want = Fraction(str(value))
        count += 1
        seen.add((root, cert, path))
        if lean != want:
            errors.append(f'{where}: Lean literal {lit} != {cert} {path} = {value}')
    for (module, cert), prefixes in REQUIRED.items():
        root = roots[module]
        data = cache.get((root, cert))
        if data is None:
            continue
        for prefix in prefixes:
            found = [p for p, _ in leaves(at(data, prefix), prefix)]
            if not found:
                errors.append(f'{cert}: required prefix {prefix} has no numeric value')
            for p in found:
                if (root, cert, p) not in seen:
                    errors.append(f'{cert} {p}: core value not tagged in any Lean declaration')
    # a definition whose body is a bare numeric literal, or a field of a `Params` instance,
    # restates a certificate value and must carry a tag
    pure = re.compile(r'^\s*\d+(?:\s*/\s*\d+)?\s*(?:--.*)?$')
    for f in sorted(LEAN.glob('*.lean')):
        lines = f.read_text().split('\n')
        for n, line in enumerate(lines, 1):
            m = re.match(r'^(?:def \S+ : \S+ :=|\s+(?:τ|σ|ε|c|lam|lamp|κ|β|δ|C1) :=)(.*)$', line)
            if not m:
                continue
            body, at_line = m.group(1), line
            if not body.strip() and n < len(lines):
                body, at_line = lines[n], lines[n]
            if pure.match(body) and not TAG.search(at_line):
                errors.append(f'{f.name}:{n}: numeric literal definition without a json tag')
    for f in sorted(LEAN.glob('*.lean')) + [HERE.parent / 'lean' / 'PRChecksB.lean']:
        code = strip_comments(f.read_text())
        for pat, name in FORBIDDEN:
            if pat.search(code):
                errors.append(f'{f.name}: contains {name}')
    return errors, count, seen


def selftest(roots):
    """Perturb one tagged value per certificate and expect exactly that failure."""
    problems = []
    _, _, seen = check(roots)
    for root, cert in sorted({(r, c) for r, c, _ in seen}):
        path = sorted(p for r, c, p in seen if (r, c) == (root, cert))[0]
        value = at(json.loads((Path(root) / 'certificates' / cert).read_text()), path)
        bumped = str(Fraction(str(value)) + Fraction(1, 10 ** 30))
        errs, _, _ = check(roots, {(root, cert, path): bumped})
        hits = [e for e in errs if f'{cert} {path} =' in e]
        if not hits or len(errs) != len(hits):
            problems.append(f'selftest: perturbing {cert} {path} gave {errs}')
    return problems


def main(argv):
    roots = dict(MODULES)
    for arg in argv:
        if '=' in arg and not arg.startswith('--'):
            k, v = arg.split('=', 1)
            roots[k] = v
    errors, count, seen = check(roots)
    if '--selftest' in argv and not errors:
        errors += selftest(roots)
    if errors:
        print('\n'.join(errors))
        print(f'FAIL: {len(errors)} problem(s)')
        return 1
    certs = sorted({c for _, c, _ in seen})
    print(f'OK: {count} tagged Lean literals equal their certificate values '
          f'({len(seen)} distinct keys in {", ".join(certs)}); all core values tagged; '
          f'no sorry/admit/native_decide/axiom' + ('; selftest passed' if '--selftest' in argv else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
