# Binary-cube orthogonality cores

> **Historical research, reconciled October 8, 2026.** Numerical uses of “current,”
> “retained,” and “next” below refer to this experiment’s checkpoint. For the
> published bound and active contracts, see [current status](current-status.md).
> These scoped experiments do not supersede later community constructions.

These families are newly analyzed in this repository; no priority claim about
their underlying graph or rank mechanisms is made.

**No improved kappa is established; the integrated conditional witness remains
2^-31.** This second overnight family changes the label geometry entirely.
A 32-dimensional rational cube representation and a constructive binary
factor give a positive instance of the existing three-stage compiler. Its
raw side circuit is far too large. The useful question is whether the cube's
symmetry supports a much cheaper side circuit with compatible frames.

## Rational labels and binary scalar matrix

Let q>=2 be a power of two, k=2q-1, and n=2^k. Label roles by x in F2^k, with
rational vectors

    v_x=(1,(-1)^x_1,...,(-1)^x_k) in Q^(k+1).

Use the ordinary positive-definite dot product. The norm is d=k+1=2q, and

    v_x dot v_y = 2q-2 weight(x+y).

Consequently labels at Hamming distance q are orthogonal. The n-by-n binary
central matrix is

    C_xy = 1 if x=y or weight(x+y)=q, and 0 otherwise.

It has diagonal one and all its off-diagonal ones join mutually orthogonal
rational lines. The rational fitting matrix has rank d: its columns are the
constant function and the k distinct sign characters, which are mutually
orthogonal nonzero functions on F2^k. This family needs no indefinite form.

## A constructive binary factor without expanding the enormous matrix

Identify the binary group algebra with

    F2[g_1,...,g_k]/(g_i^2-1),

and put y_i=g_i+1. Then y_i^2=0. The convolution kernel of C is

    1 + sum over |S|=q of product(g_i, i in S).

In the y basis the coefficient of a monomial of degree l is
C(k-l,q-l), with the additional constant one. For k=2q-1 and q a power of
two, parity leaves exactly the degree-q elementary symmetric polynomial

    e_q(y)=sum over |S|=q of product(y_i, i in S).

The parity identity follows from the product formula for (1+x)^t in F2;
the audit also checks all its finitely many coefficients for each screened q.

Let M be multiplication by e_q in this square-zero algebra. Its entry from
monomial S to monomial T is one precisely when S is contained in T and
|T|-|S|=q. Put a=q/2. Split its inputs into the low degrees |S|<a and the rest.
Every remaining input can contribute only to output degrees |T|>=q+a.
Therefore M factors through

    R = number of low input monomials + number of high output monomials
      = 2 sum_{i=0}^{q/2-1} C(2q-1,i).

This is an explicit factor, not an asserted exact large-matrix rank. Take
columns M[:,S] for low S, append coordinate columns for high T, and on the
second factor take the low coordinate rows plus the high rows of M with
low input columns removed. The product is M.

The change of basis Z has Z_TS=1 when T is contained in S and satisfies
Z^2=I over F2. Thus C=Z M Z, and conjugating the displayed factor gives the
binary central factor required by the core compiler. Exact expanded checks
at q=2 and q=4 verify the complete products; their actual binary ranks are
2 and 16 respectively. No claim that this finite check verifies the larger
cases replaces the general factor argument.

## Full compiler budget

The existing raw compiler now has

    n=2^(2q-1), d=2q,
    E=n C(2q-1,q),
    W=2n^3+3n^2(E+R), m=d^3,
    Delta=n^3-6n^2 R d.

All arbitrary side and central inputs are included. Positive deficit requires
n>6Rd for this factor. q=2,4,8 fail. q=16 gives

    n=2,147,483,648,
    d=32,
    R=7,144,448,
    n/(R d)=9.3931489... .

This is a generative positive bit construction, not an expansion of billions
of labels or their much larger compiled network. The raw saving is only about
1.176e-15, far below the retained 2.96e-9.

If a new side circuit preserved the compiler's decreasing-rank loss while
using S roles, its saving would be computed by replacing E with S. Granting
S=0 gives a benchmark near 5.275e-7. To support the working bit target
1.6e-7, a sufficient side budget at q=16 is

    S/n < 1.538946... .

The necessary budget from the opposite logarithm enclosure is very close.
Neither is an implementation. The main target is consequently a side circuit
with roughly one role per label, together with its complete frame certificate.
The q=32 case has dimension 64 and just enough free-side headroom for the
necessary a_b>5/2^25 threshold, but not for the more comfortable 1.6e-7 target.
Larger dimensions face the earlier dimension screen for this compiler.

## Small quadratic-code subfamilies fail a cheap exact test

A possible way to reduce the huge role population is to retain only sign
vectors from low-degree Boolean polynomials. We tested the constant-free
quadratic code on t variables: use every polynomial of degree one or two,
and label it by its 2^t signs. Its rational dimension is exactly 2^t, since
the code contains every linear character. Two labels are orthogonal when
their difference polynomial is balanced.

For the specified binary choice C=I plus all those orthogonality edges, the
matrix is a Cayley matrix on the coefficient space. Its first row is generated
exactly by truth-table weights; other rows are XOR permutations. We stop
binary elimination once its rank lower bound prevents n>6rd.

| t | labels n | rational dimension d | certified binary rank lower bound |
| --- | ---: | ---: | ---: |
| 3 | 64 | 8 | 2 |
| 4 | 1,024 | 16 | 11 |
| 5 | 32,768 | 32 | 171 |

All three bounds exclude positive deficit for these specified cores. The
certificate records independent row indices and hashes; replay reconstructs
those exact rows and checks independence with binary arithmetic. These are
lower bounds sufficient for rejection, not claimed exact full ranks. The
screen does not exclude different binary matrices supported on the same
orthogonality graph, different subcodes, or general rational frames.

## Why the most obvious fast side circuit needs a rejection screen

Write A=C+I for the side map. In characteristic two C^2=0 and A^2=I. Computing
A as a direct low-rank update I+UV therefore looks tempting. However, if the
side circuit simply uses the same U,V factors as the central circuit and a
direct identity injection, their signed characteristic-zero interpretations
also cancel to the identity shear. The transparent dirty-workspace completion
then realizes the same bank exchange over Q. The
[characteristic-zero obstruction](stronger-rank-screens.md) excludes a
rational rank deficit for that field-uniform implementation.

There is a related topological trap in using a full subset-transform butterfly
for the side operation. A cube XOR shift by q coordinates is an orthogonal
input/output matching, but the butterfly's switching paths can implement
that shift. If those paths restore the logical identity connection between
the copied input and target roles, the same obstruction applies. Having only
n side roles is insufficient; the circuit must retain the characteristic
separation. Other matchings and different side topologies need their own
screen. No blanket exclusion of all cube side circuits is claimed.

This family therefore sharpens the next question: can the global cube
computation be shared without introducing a characteristic-zero realization
of the completed exchange, and can its rational frame changes remain cheap?
It is not enough to give a fast arithmetic implementation of A.

## Complex interface remains separate

This construction supplies a bit core. Reversing the roles of its two fields
would replace the small rational label dimension by the very large binary
factor dimension; it is not a competitive complex network. No complex
companion is asserted for this family. A bit improvement here must be paired
with an independently improved complex interface and a complete guard and
assembly audit before supporting the overnight multiplication target.

Run `python3 -S scripts/audit_cube_cores.py` and
`python3 -m unittest discover -s tests -p test_cube_core_family.py -v`.
The [certificate](../../certificates/cube-core-family.json) includes expanded
small factors, generative large ledgers, hypothetical side budgets, exact
quadratic-code rejection witnesses, and source hashes. The retained proof
artifacts are unchanged.
