#!/usr/bin/env python3
"""Exact certificate for the linear guard and the constant-width banded solve.

Proofs: notes/assembly-lu-guard.tex, notes/assembly-lu-resampling.tex and
notes/assembly-lu-note.tex.  This script re-derives the certified bit and
complex savings with the existing paired-bit and pair-star functions, checks
every finite constant used by the written lemmas, and verifies every strict
assembly constraint and margin of the headline witness
kappa = 296461013/(2*10^17) > 2^-30.

Standard library only; every decision uses integers or Fractions.  The
checks support the written arguments; they do not verify the upstream
multiplication theorem or the proofs themselves.
"""
from decimal import Context, Decimal
from fractions import Fraction as Q
from math import gcd
from pathlib import Path
import hashlib
import json
import random

from certify import Parameters, constraints as retained_constraints
from certify import margins as retained_margins, require, verify_sources
from compact_control_layer import layer_exponents
from complex_pair_star import COMPLEX_SAVING, counts as pair_star_counts
from complex_pair_star_parameters import (
    check as retained_check, normalized_counts, sharpened_bit_certificate,
    sharpened_parameters, supplied_counts)
from prepare_layers import serializable
from search_network import log_integer_bounds, log_ratio_bounds

ROOT = Path(__file__).resolve().parents[1]
ALPHA = 2
BETA = Q(1, 10)
GAP = Q(1, 10**12)                   # lambda' = 1 - a_b (1 - GAP)
DELTA = Q(1, 10**12)
EPSILON = Q(124999999, 250000000)
KAPPA = Q(296461013, 2*10**17)
RECORD = Q(5929220328, 10**19)
CHANGED = ('guard_width', 'gaussian_cost', 'dimension_upper_bound',
           'gamma_sublinear', 'alpha_below_sqrt_p')
PROOFS = ('notes/assembly-lu-guard.tex', 'notes/assembly-lu-resampling.tex',
          'notes/assembly-lu-note.tex')


# ---------------------------------------------------------------------------
# Rational enclosures
# ---------------------------------------------------------------------------

def arctan_bounds(x, terms):
    """For 0<x<1 consecutive alternating partial sums bracket arctan(x)."""
    s, prev = Q(0), None
    for k in range(terms):
        prev = s
        s += (-1)**k*x**(2*k+1)/(2*k+1)
    return min(prev, s), max(prev, s)


def pi_bounds(terms=30):
    lo5, hi5 = arctan_bounds(Q(1, 5), terms)
    lo239, hi239 = arctan_bounds(Q(1, 239), 8)
    return 16*lo5-4*hi239, 16*hi5-4*lo239


def exp_lower(x, terms=80):
    """A partial sum of the exponential series is a lower bound for x>0."""
    require(x > 0, 'positive exponent')
    s, term = Q(0), Q(1)
    for k in range(terms):
        s += term
        term = term*x/(k+1)
    return s


def outward(lo, hi, digits=30):
    """Short rational interval [lo', hi'] containing [lo, hi]."""
    scale = 10**digits
    return (Q((lo.numerator*scale)//lo.denominator, scale),
            Q(-((-hi.numerator*scale)//hi.denominator), scale))


SQRT2_UP = Q(99, 70)


# ---------------------------------------------------------------------------
# Savings, re-derived with the existing functions
# ---------------------------------------------------------------------------

def savings():
    bit = sharpened_bit_certificate()
    a_b = bit['saving']
    n = pair_star_counts()
    supplied = normalized_counts(supplied_counts())
    for key, legacy in (('W', 'Wc'), ('L', 'Lc'), ('s', 'sc'), ('m', 'm'), ('N', 'N')):
        require(n[key] == supplied[legacy], 'Pair-star count differs: '+key)
    require(n['s'] == n['W']*n['m']-2*n['N']+2*n['L'], 'Residual formula')
    eta = Q(n['W']*n['m']-n['s'], n['W']*n['m'])
    require(eta == n['eta'] == Q(37, 948319488), 'Complex deficit')
    log_lo, log_hi = log_integer_bounds(n['m'])
    a_c = COMPLEX_SAVING
    require(eta > a_c*log_hi, 'Complex saving lacks a strict certificate')
    # The repository's own record checker still passes on its witness.
    retained_check(sharpened_parameters(), supplied, sharpened_bit=True)
    return dict(a_b=a_b, a_c=a_c, counts=n, complex_eta=eta,
                complex_log_m_upper=log_hi, complex_proof_gap=eta-a_c*log_hi,
                bit_proof_gap=bit['proof_gap'])


# ---------------------------------------------------------------------------
# The assembly constraint system
# ---------------------------------------------------------------------------

def gaussian_rows(model):
    """(G0, G, caps): Gaussian power 1-G0+delta+G*eps and width caps a-b*eps."""
    if model == 'tight':
        return Q(1, 4), Q(5, 4), dict(dimension_upper_bound=(Q(1, 3), Q(1)),
                                      alpha_below_sqrt_p=(Q(1, 4), Q(1, 4)),
                                      gamma_sublinear=(Q(1, 2), Q(3, 2)))
    require(model == 'constant-width', 'Unknown Gaussian model')
    return Q(1, 2), Q(1), dict(dimension_upper_bound=(Q(1, 2), Q(1)),
                               alpha_below_sqrt_p=(Q(1, 2), Q(0)),
                               gamma_sublinear=(Q(1), Q(2)))


def constraints(p, gaussian='constant-width'):
    """Every strict exponent condition; names follow scripts/certify.py."""
    e, c, t, s, b = p.epsilon, p.c, p.tau, p.sigma, p.beta
    G0, G, caps = gaussian_rows(gaussian)
    ex = layer_exponents(t, s, b, c)
    out = {
        'tau_positive': t, 'tau_below_one': 1-t,
        'sigma_positive': s, 'sigma_below_one': 1-s,
        'c_positive': c, 'epsilon_positive': e,
        'beta_positive': b, 'beta_below_one': 1-b,
        'lambda_above_tau': p.lam-t, 'lambda_above_sigma': p.lam-s,
        'lambda_below_one': 1-p.lam,
        'packed_overhead': p.lam-ex['internal'],
        'lambda_prime_above_lambda': p.lamp-p.lam,
        'leaf_cost': p.lamp-ex['leaf'],
        'reserved_axes': p.lamp-ex['preprocessing'],
        'lambda_prime_below_one': 1-p.lamp,
        'guard_width': 1-e*p.C1,
        'crt_layout': (1-t)*(1-e),
        'gaussian_cost': G0-p.delta-G*e,
        'prefix_cost': 1-e*(1+c),
        'scalar_cost': 1-p.delta-e,
        'delta_positive': p.delta,
        'delta_below_one_eighth': Q(1, 8)-p.delta,
        'prime_interval_growth': 1-2*e,
        'K_smaller_than_ell': 1-e-e*c,
        'K_dominates_log_p': e*c,
        'r_superpolynomial': 1-e,
        'kappa_positive': p.kappa,
    }
    for name, (a, slope) in caps.items():
        out[name] = a-slope*e
    return out


def margins(p, gaussian='constant-width'):
    e, c, t = p.epsilon, p.c, p.tau
    G0, G, _ = gaussian_rows(gaussian)
    return {'g1': 1-e*(1+c), 'g2': e*c*(1-t), 'g3': e*(1-p.lamp),
            'g4': (1-t)*(1-e), 'g5': G0-p.delta-G*e,
            'g6': 1-p.delta-e, 'g7': e}


def transcription_check():
    """The retained model equals scripts/certify.py on the record witness."""
    rp = sharpened_parameters()
    repo = retained_constraints(rp, layout_model='nonadjacent',
                                assembly_model='tight-gaussian')
    ex = layer_exponents(rp.tau, rp.sigma, rp.beta, rp.c)
    repo['packed_overhead'] = rp.lam-ex['internal']
    repo['reserved_axes'] = rp.lamp-ex['preprocessing']
    mine = constraints(rp, 'tight')
    require(set(repo) == set(mine), 'Constraint names differ')
    for key, value in repo.items():
        require(mine[key] == value, 'Transcription mismatch: '+key)
    require(margins(rp, 'tight') == retained_margins(
        rp, layout_model='nonadjacent', assembly_model='tight-gaussian'),
        'Margin transcription mismatch')
    return len(repo)


def headline_parameters(a_b, a_c):
    return Parameters(tau=1-a_b, sigma=1-a_c, epsilon=EPSILON, c=Q(1),
                      lam=1-a_b*(1-GAP/2), lamp=1-a_b*(1-GAP), kappa=KAPPA,
                      beta=BETA, delta=DELTA, C1=Q(1))


def check_witness(p):
    """Every strict constraint, every margin and the absorption gap."""
    require(p.C1 == 1, 'The linear guard has exponent one')
    slacks = constraints(p)
    for name, value in slacks.items():
        require(value > 0, 'Failed strict constraint: '+name)
    gs = margins(p)
    g = min(gs.values())
    require(g > p.kappa, 'No strict absorption gap')
    return dict(constraint_slacks=slacks, margins=gs, minimum_margin=g,
                limiting=[k for k, v in gs.items() if v == g],
                absorption_gap=g-p.kappa)


def suprema(a_b, a_c):
    q = min(a_b, a_c)
    new, old = q/(2+2*q), q/(5+4*q)
    # The headline lies strictly between the record and the new supremum.
    require(RECORD < KAPPA < new < q/2, 'Unexpected headline position')
    require(Q(1, 2**30) < KAPPA < Q(1, 2**29), 'Unexpected dyadic scale')
    # Ceiling of this assembly: kappa < eps*min(q, c a_b) with eps<1/2 and
    # eps(1+c)<1 gives kappa < q/2 for every c>0.
    for c in (Q(1, 2), Q(1), Q(2)):
        cap = min(Q(1, 2), 1/(1+c))
        require(cap*min(q, c*a_b) <= q/2, 'Ceiling inequality')
    return dict(q=q, constant_width_supremum=new, retained_supremum=old,
                ceiling=q/2, ratio_to_record=KAPPA/RECORD,
                ratio_new_to_old_supremum=new/old)


# ---------------------------------------------------------------------------
# Constants of the written lemmas
# ---------------------------------------------------------------------------

def guard_constants(n):
    """Proposition prop:linear-guard with the pair-star node allowance."""
    h, v, m, W, s, R = n['h'], n['v'], n['m'], n['W'], n['s'], n['R']
    require(W == 2*n['N']+2*v*v*(R+h), 'Role count formula')
    data = json.loads((ROOT/'certificates/complex-pair-star.json').read_text())
    require(data['circuit']['additions']+data['circuit']['output_uses'] == R,
            'Side roles differ from the pair-star circuit')
    D_scalar = 3*v*v*(12*R+4*v*h+10*v)+8*W
    D_node = D_scalar+4*s
    E = 64*(W+m+1)**3
    depth = data['coefficient_depth']
    require((int(depth['scalar_operations_upper']), int(depth['total_node_depth_upper']),
             int(depth['retained_node_charge'])) == (D_scalar, D_node, E),
            'Node allowance differs from the pair-star certificate')
    require(D_node < E and m >= 3, 'Node allowance hypothesis')
    # Lemma lem:guard-kernels: entries of C^{(x)f} are units times
    # (1+i)^{f mod 2} 2^{-ceil(f/2)}, of modulus 2^{-f/2}.
    for f in range(1, 13):
        need = (f+1)//2
        for k in range(f+1):
            x, y = 1, 0
            for factor in [(1, 1)]*(f-k)+[(1, -1)]*k:
                x, y = x*factor[0]-y*factor[1], x*factor[1]+y*factor[0]
            require(x % (1 << (f-need)) == 0 and y % (1 << (f-need)) == 0,
                    'Kernel denominator')
            require(x*x+y*y == 2**f, 'Kernel modulus')
    # n <= (m-1)(1+floor(log_m d)) <= (m-1)d and ceil(log_m d) <= d.
    for d in list(range(1, 3000))+[10**k for k in range(4, 40)]:
        lg = 0
        while m**(lg+1) <= d:
            lg += 1
        require(1+lg <= d and (lg if m**lg == d else lg+1) <= d, 'Piece counts')
    return dict(h=h, m=m, W=W, s=s, side_roles=R, D_scalar=D_scalar,
                D_node=D_node, E=E, C0_star=E+2*s+m+26)


def psi_theta(x):
    """theta*psi(x) on [-1/2,1/2], Lemma lem:scaled-dominance."""
    if x <= Q(-1, 4):
        return x*(x+Q(1, 2))
    if x <= Q(1, 4):
        return Q(-1, 16)
    return x*(x-Q(1, 2))


def g_function(x):
    if x <= Q(-1, 4):
        return 2*x+Q(1, 2)
    if x <= Q(1, 4):
        return Q(0)
    return 2*x-Q(1, 2)


def beta_exact(l, s, t):
    x = Q(t*l, s)
    return x-(x+Q(1, 2)).__floor__()


def resampling_constants(seed=20261008):
    pil, piu = pi_bounds()
    l2l, l2u = log_ratio_bounds(Q(2))
    require(Q(314159, 10**5) < pil < piu < Q(314160, 10**5), 'pi enclosure')
    # rho_2 = 2 e^{-2 pi} + 2.01 e^{-4 pi} < 0.0038, 1/(1-0.0038) < 1.004.
    rho2 = 2/exp_lower(2*pil)+Q(201, 100)/exp_lower(4*pil)
    require(rho2 < Q(38, 10000) and 1/(1-Q(38, 10000)) < Q(1004, 1000), 'rho_2')
    require(2/exp_lower(14*pil) < Q(1, 200), 'Tail ratio e^{-14 pi}')
    # log2 R <= L uses pi*log2(e) < 4.533; e^{-pi w} < 2^{-w} uses pi*log2(e) > 1.
    require(piu/l2l < Q(4533, 1000) and pil/l2u > 1, 'pi log2 e enclosure')
    # Lemma lem:dominant-lu at rho = 1/10.
    rho = Q(1, 10)
    rhoL, rhoU = rho/(1-2*rho), rho/(1-rho)
    norms = (1/(1-rhoL), 1/(1-rhoU), (1/(1-rhoU))/(1-rho), 1/(1-rho))
    require((rhoL, rhoU) == (Q(1, 8), Q(1, 9)) and
            norms == (Q(8, 7), Q(9, 8), Q(5, 4), Q(10, 9)), 'LU constants')
    require(Q(38, 10000)+Q(1, 2**7) < Q(1, 10), 'Perturbed dominance')
    # Solve budgets of Lemma lem:banded-solve.
    require(SQRT2_UP**2 > 2, 'sqrt 2 bound')
    require(Q(8, 7)*Q(1, 2)+Q(1, 10**6) < Q(58, 100), 'forward norm')
    require(Q(58, 100)+Q(1, 10) <= Q(68, 100), 'g_i bound')
    require((Q(10, 9)+Q(1, 10**6))*Q(68, 100) < 1, 'backward induction')
    require(SQRT2_UP+Q(68, 100) < Q(22, 10), 'residual bound')
    require(Q(5, 4)*Q(8, 7)*SQRT2_UP+Q(9, 8)*Q(22, 10) < 5, 'solve budget')
    require(Q(1004, 1000)*Q(10, 9)*Q(1, 2) < Q(56, 100), 'comparison budget')
    for p, L in ((101, 0), (101, 101), (1000, 1000)):
        w = 3*p+2*L+12
        s_max = 2**p-1
        require(2**L*s_max*(s_max+1)*Q(1, 2**w) <= Q(1, 2**(p+L+12)), 'GE backward error')
        m = 1
        while m*m*4 < w:
            m += 1
        require(3+4*m <= 2**(2*p), 'band count')
        require(5*Q(1, 2**(3*p+L+12))+Q(56, 100)*Q(1, 2**(p+11)) < Q(1, 2**(p+10)),
                'final solve budget')
    require(SQRT2_UP+Q(1, 2**11) < 2 and Q(1004, 1000)/4 <= Q(251, 1000), 'output')
    # psi: continuity, periodicity, range; g bounds and the averaging step.
    require(psi_theta(Q(-1, 2)) == psi_theta(Q(1, 2)) == 0, 'psi periodic')
    lft, rgt = Q(-1, 4), Q(1, 4)
    require(lft*(lft+Q(1, 2)) == Q(-1, 16) == rgt*(rgt-Q(1, 2)), 'psi continuous')
    rng = random.Random(seed)
    for _ in range(3000):
        theta = Q(rng.randint(1, 999), 1000)
        x = Q(rng.randint(-5000, 5000), 10000)
        require(2*x-Q(1, 2) <= g_function(x) <= 2*x+Q(1, 2), 'g bounds')
        require(abs(g_function(x)) <= Q(1, 2), 'g modulus')
        require(Q(-1, 16) <= psi_theta(x) <= 0, 'psi range')
        b = Q(rng.randint(-5000, 4999), 10000)
        if b+theta < Q(1, 2):
            d = (psi_theta(b+theta)-psi_theta(b))/theta
            require(2*b+theta-Q(1, 2) <= d <= 2*b+theta+Q(1, 2), 'averaging')
        else:
            d = (psi_theta(b+theta-1)-psi_theta(b))/theta
        require(abs(d) <= Q(1, 2), 'step bound')
    # Exact instance checks of the two scaled-exponent inequalities.
    rows = 0
    for s, t in ((61, 62), (97, 101), (101, 128), (113, 127), (211, 217), (251, 254)):
        theta = Q(t, s)-1
        phi = [psi_theta(beta_exact(l, s, t))/theta for l in range(s)]
        for l in range(s):
            bl = beta_exact(l, s, t)
            for h in range(-6, 7):
                if h == 0:
                    continue
                Qh = (Q(t*h, s)+bl)**2-beta_exact(l+h, s, t)**2
                E = Qh-(phi[(l+h) % s]-phi[l])
                require(Qh >= abs(h)*(abs(h)-1), 'Q_h lower bound')
                require(E >= (Q(1, 2)+theta if abs(h) == 1 else abs(h)*(abs(h)-Q(3, 2))),
                        'scaled exponent')
            rows += 1
    return dict(pi=outward(pil, piu), rho_2_upper=Q(38, 10000),
                rho_2_enclosure=outward(rho2, rho2+Q(1, 10**25)),
                pi_log2_e_upper=Q(4533, 1000), checked_rows=rows)


def assembly_constants():
    """alpha = 2 bounds of the revised assembly (C.6 / sec 08)."""
    for d in list(range(22, 4000))+[10**k for k in range(4, 30)]:
        L_max = -((-4533*4*4*d)//16000)          # ceil(4533*alpha^2*(4d)/16000)
        require(L_max <= Q(4533, 1000)*d+1, 'L bound')
        require(d*(2*ALPHA*ALPHA+L_max+1) <= 5*d*d, 'gamma <= 5 d^2')
    require(1-2*EPSILON == Q(8, 10**9), 'Unexpected epsilon')
    # b >= 2^541000000 gives b^{1-2eps} >= 2^{4.328} > 20, hence gamma <= b/4.
    require(541000000*(1-2*EPSILON) == Q(4328, 1000) and 20**1000 < 2**4328,
            'gamma cutoff')
    # Fixed rational power used by the setup: d = floor(b^eps).
    require(EPSILON.denominator == 250000000 and EPSILON.numerator == 124999999,
            'setup exponent')
    # Once d >= 22: L_i <= 4.533 d + 1 <= p and w_i <= 6p for large p.
    return dict(alpha=ALPHA, gamma_bound='gamma <= 5 d^2 for d >= 22',
                gamma_cutoff_log2_b=541000000, one_minus_two_epsilon=1-2*EPSILON)


# ---------------------------------------------------------------------------
# Exact simulation of Lemma lem:banded-solve (regression tests, not a proof)
# ---------------------------------------------------------------------------

def solve_parameters(s, t, alpha, p):
    """L, w and m of Lemma lem:banded-solve."""
    L = -((-4533*alpha*alpha*s)//(16000*(t-s)))
    w = 3*p+2*L+12
    m = 1
    while m*m*alpha*alpha < w:
        m += 1
    return L, w, m


def truncate(x, w):
    """Q_w on a real Fraction: truncation toward zero to 2^-w."""
    n = x.numerator*2**w
    k = n//x.denominator if n >= 0 else -((-n)//x.denominator)
    return Q(k, 2**w)


def decimal_pi(ctx, digits):
    lo5, hi5 = arctan_bounds(Q(1, 5), digits)
    lo239, hi239 = arctan_bounds(Q(1, 239), digits//4+2)
    lo, hi = 16*lo5-4*hi239, 16*hi5-4*lo239
    require(hi-lo < Q(1, 10**(digits+5)), 'pi enclosure for the simulation')
    return ctx.divide(Decimal(lo.numerator), Decimal(lo.denominator))


def gaussian_terms(s, t, alpha, H, ctx, pi):
    """Decimal e^{-pi alpha^2 Q_h(l)} for 0 <= l < s and 0 < |h| <= H."""
    terms = {}
    for l in range(s):
        b = beta_exact(l, s, t)
        for h in range(-H, H+1):
            if h:
                q = (Q(t*h, s)+b)**2-beta_exact(l+h, s, t)**2
                require(q > 0, 'positive Gaussian exponent')
                x = ctx.multiply(pi, ctx.divide(Decimal(alpha*alpha*q.numerator),
                                                Decimal(q.denominator)))
                terms[l, h] = ctx.exp(ctx.minus(x))
    return terms


def decimal_solve(rows, rhs, ctx):
    """Gaussian elimination with partial pivoting on Decimal data."""
    n = len(rows)
    a = [rows[i][:]+[r[i] for r in rhs] for i in range(n)]
    k_rhs = len(rhs)
    for k in range(n):
        piv = max(range(k, n), key=lambda i: abs(a[i][k]))
        a[k], a[piv] = a[piv], a[k]
        for i in range(k+1, n):
            f = ctx.divide(a[i][k], a[k][k])
            if f:
                a[i] = [ctx.subtract(x, ctx.multiply(f, y)) if j >= k else x
                        for j, (x, y) in enumerate(zip(a[i], a[k]))]
    out = [[Decimal(0)]*n for _ in range(k_rhs)]
    for c in range(k_rhs):
        for i in range(n-1, -1, -1):
            acc = a[i][n+c]
            for j in range(i+1, n):
                acc = ctx.subtract(acc, ctx.multiply(a[i][j], out[c][j]))
            out[c][i] = ctx.divide(acc, a[i][i])
    return out


def banded_solve_simulation(s, t, alpha, p, count=2, seed=20261008):
    """Run the factor and solve steps of lem:banded-solve in exact arithmetic.

    The entries of E_m are 2^-w truncations of high-precision values, a valid
    output of the cited exponential routine.  The reference J u uses every
    term with |h| <= H of the full matrix N, Decimal elimination with partial
    pivoting, and a precision far beyond 2^-p.  Returns the worst output error
    in units of 2^-p together with the checked invariants.
    """
    require(1 < s < t < 2*s and gcd(s, t) == 1, 'instance shape')
    L, w, m = solve_parameters(s, t, alpha, p)
    require(L <= p and s >= 4*m, 'instance violates the lemma hypotheses')
    digits = (w+p)//3+60
    ctx = Context(prec=digits)
    pi = decimal_pi(ctx, digits)
    H = m+12
    terms = gaussian_terms(s, t, alpha, H, ctx, pi)
    A = [dict() for _ in range(s)]
    for l in range(s):
        A[l][l] = Q(1)
        for h in range(-m, m+1):
            if h:
                A[l][(l+h) % s] = truncate(Q(terms[l, h]), w)
    offdiag = max(sum(v for j, v in row.items() if j != i) for i, row in enumerate(A))
    B = set(range(s-m, s))
    J = [sorted((set(range(k+1, min(k+m, s-1)+1)) | B) & set(range(k+1, s))) for k in range(s)]
    in_p = lambda i, j: abs(i-j) <= m or i in B or j in B
    require(all(in_p(i, j) for i, row in enumerate(A) for j in row), 'band outside P')
    # Elimination with windows J_k.
    a = [dict(row) for row in A]
    lo, up, psi, pivots = {}, {}, [], []
    for k in range(s):
        pk = a[k][k]
        pivots.append(pk)
        require(Q(9, 10) <= pk <= Q(11, 10), 'pivot outside [9/10, 11/10]')
        for i in range(k+1, s):
            require(i in J[k] or a[i].get(k, 0) == 0, 'fill outside the window')
            require(i in J[k] or a[k].get(i, 0) == 0, 'fill outside the window')
        psi.append(truncate(1/pk, w))
        for j in J[k]:
            up[k, j] = a[k].get(j, Q(0))
        for i in J[k]:
            lo[i, k] = truncate(a[i].get(k, Q(0))/pk, w)
        for i in J[k]:
            for j in J[k]:
                a[i][j] = truncate(a[i].get(j, Q(0))-lo[i, k]*up[k, j], w)
                require(in_p(i, j), 'write outside P')
        require(all(abs(lo[i, k]) <= Q(2**L, 9)+Q(1, 2**w) for i in J[k]), 'L entry bound')
    # Backward error of the computed factors: |L U - A| < (s+1) 2^-w entrywise.
    for i in range(s):
        for j in range(s):
            lu = sum(lo[i, r]*up[r, j] for r in range(min(i, j))
                     if (i, r) in lo and (r, j) in up)
            lu += up[i, j] if i < j and (i, j) in up else 0
            lu += lo[i, j]*pivots[j] if i > j and (i, j) in lo else 0
            lu += pivots[i] if i == j else 0
            require(abs(lu-A[i].get(j, Q(0))) < Q(s+1, 2**w), 'factor backward error')
    # Reference matrix N with all aliases of every |h| <= H.
    N = [[Decimal(0)]*s for _ in range(s)]
    for l in range(s):
        N[l][l] = Decimal(1)
        for h in range(-H, H+1):
            if h:
                N[l][(l+h) % s] = ctx.add(N[l][(l+h) % s], terms[l, h])
    rng = random.Random(seed)
    inputs = [[((-1)**k*2**p, 0) for k in range(s)]]
    while len(inputs) < count:
        vec = []
        for _ in range(s):
            x, y = rng.randint(-2**p, 2**p), rng.randint(-2**p, 2**p)
            while x*x+y*y > 4**p:
                x, y = x//2, y//2
            vec.append((x, y))
        inputs.append(vec)
    rhs = []
    for vec in inputs:
        for part in (0, 1):
            rhs.append([ctx.divide(Decimal(z[part]), Decimal(2**(p+1))) for z in vec])
    ref = decimal_solve(N, rhs, ctx)
    worst = Q(0)
    for n, vec in enumerate(inputs):
        out = []
        for part in (0, 1):
            v = [Q(z[part], 2**(p+1)) for z in vec]
            yv = []
            for k in range(s):
                acc = v[k]-sum(lo[k, r]*yv[r] for r in range(k) if (k, r) in lo)
                yv.append(truncate(acc, w))
            xv = [Q(0)]*s
            for i in range(s-1, -1, -1):
                g = yv[i]-sum(up[i, j]*xv[j] for j in J[i])
                xv[i] = truncate(psi[i]*g, w)
            out.append([truncate(x/2**(L+1), p) for x in xv])
        for k in range(s):
            re = out[0][k]-Q(ref[2*n][k])/2**(L+1)
            im = out[1][k]-Q(ref[2*n+1][k])/2**(L+1)
            err2 = (re*re+im*im)*4**p
            require(err2 < 4, 'output error of at least 2 units')
            require(out[0][k]**2+out[1][k]**2 <= 1, 'output outside the disk')
            worst = max(worst, err2)
    return dict(s=s, t=t, alpha=alpha, p=p, L=L, w=w, m=m, unscaled_offdiag=offdiag,
                min_pivot=min(pivots), max_pivot=max(pivots), worst_error_squared=worst)


def certificate():
    sv = savings()
    a_b, a_c = sv['a_b'], sv['a_c']
    p = headline_parameters(a_b, a_c)
    witness = check_witness(p)
    require(witness['limiting'] == ['g3'], 'Expected g3 to limit')
    names = transcription_check()
    # At fixed parameters the Gaussian rows differ in exactly four entries;
    # the fifth, guard_width, changes through the guard exponent C1 = 1.
    retained, new = constraints(p, 'tight'), constraints(p)
    changed = {k for k in retained if retained[k] != new[k]}
    require(changed == set(CHANGED)-{'guard_width'}, 'Unexpected changed constraint')
    return dict(
        status='CONDITIONAL ASSEMBLY REFINEMENT: LINEAR GUARD AND CONSTANT-WIDTH BANDED SOLVE',
        upstream_commit=verify_sources(),
        headline_kappa=KAPPA,
        savings=dict(a_b=a_b, a_c=a_c, complex_eta=sv['complex_eta'],
                     complex_proof_gap=sv['complex_proof_gap'],
                     bit_proof_gap=sv['bit_proof_gap'],
                     pair_star_counts=sv['counts']),
        parameters=vars(p), witness=witness,
        retained_constraint_names=names, changed_constraints=list(CHANGED),
        suprema=suprema(a_b, a_c),
        guard=guard_constants(sv['counts']),
        resampling=resampling_constants(),
        assembly=assembly_constants(),
        proof_sha256={name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                      for name in PROOFS},
        verification_boundary=(
            'Checks exact savings, node allowances, kernel denominators, every '
            'rational constant of the written guard and banded-solve lemmas, '
            'instance checks of the scaled-dominance inequalities, all assembly '
            'constraints and the seven margins.  It does not verify the written '
            'proofs, the multitape implementation or the upstream theorem.'))


if __name__ == '__main__':
    result = certificate()
    (ROOT/'certificates/assembly-lu.json').write_text(
        json.dumps(serializable(result), indent=2, sort_keys=True)+'\n')
    print('PASS assembly LU certificate: kappa =', KAPPA, '> 2^-30')
    print('Minimum margin:', result['witness']['minimum_margin'])
    print('Ratio to the current record:', float(result['suprema']['ratio_to_record']))
