#!/usr/bin/env python3
"""Independent pinned-source patch for the linear guard and constant-width solve.

Retains the pair-star patch and changes only the coefficient guard of the
simultaneous layer, the solve of the square Gaussian system, and the
resulting assembly parameters, cost row, margins and witness.  The pinned
upstream is untouched.
"""
import difflib
from fractions import Fraction as Q
from pathlib import Path

from assembly_lu import KAPPA, certificate as assembly_certificate
from certify import require
from make_complex_pair_star_patch import patched_files as pair_star_files
from make_patch import replace_once

ROOT = Path(__file__).resolve().parents[1]
HEADLINE = r'296461013/(2\cdot10^{17})'
PAIR_STAR_HEADLINE = r'5929220328/10^{19}'


def note(name):
    return (ROOT/'notes'/name).read_text()


def motifs(text):
    return replace_once(text, r'''Consequently the retained guard recurrence may use its existing node
charge $E=64(W+m+1)^3$, now evaluated with the new network constants.
The recursive residual calls are charged separately by $sA(e/m)$,
as before.''', r'''Consequently the linear guard of Section~\ref{sec:linear-guard} may use
the node charge $E=64(W+m+1)^3$, evaluated with the new network constants.
Completed recursive residual calls are charged there by their exact
kernels.''')


def layers(text):
    start = text.index(r'\subsection{A generalized stopped-depth guard}')
    end = text.index(r'\begin{proposition}[Simultaneous normalized butterfly layer]', start)
    text = text[:start]+note('assembly-lu-guard.tex')+'\n'+text[end:]
    text = replace_once(text, r'''This fact also bounds their coefficient
dependency depth by the same $8d$ allowance used in the guard proof.''',
                        r'''This fact also bounds their coefficient
growth by the same $8d$ allowance used in the guard proof.''')
    text = replace_once(text, r'''Let $c,\epsilon,\lambda,\lambda',\beta,\zeta$ be fixed positive rational numbers
with $0<\beta<1$, and put
\[
 C_1=5-4\beta+\zeta,\qquad
 \chi=\tau+(1-\beta)\max\{\sigma-\tau,0\}.
\]
Require
\[
 \max\{\tau,\sigma,\chi\}<\lambda<\lambda'<1,\qquad
 \max\{\sigma+\beta(1-\sigma),1-c,0\}<\lambda',\qquad
 \epsilon C_1<1.
\]''', r'''Let $c,\epsilon,\lambda,\lambda',\beta$ be fixed positive rational numbers
with $0<\beta<1$, and put
\[
 \chi=\tau+(1-\beta)\max\{\sigma-\tau,0\}.
\]
Require
\[
 \max\{\tau,\sigma,\chi\}<\lambda<\lambda'<1,\qquad
 \max\{\sigma+\beta(1-\sigma),1-c,0\}<\lambda',\qquad
 \epsilon<1.
\]''')
    text = replace_once(text, r'''\[
 C_0=\left\lceil\max\{128mB^2,18mB^2(1+1/\zeta)\}\right\rceil,
 \qquad B=s_{\rm c}+64(W_{\rm c}+m+1)^3,
\]
where $m,W_{\rm c},s_{\rm c}$ are the fixed constants of
Proposition~\ref{prop:pair-star-complex-interface}. The procedure uses
at most $p+\lceil C_0d^{C_1}\rceil$ fractional bits and
$\lceil C_0d^{C_1}\rceil+3$ integer and sign bits per real component
internally; these widths are $O(p)$.''', r'''\[
 C_0^*=64(W_{\rm c}+m+1)^3+2s_{\rm c}+m+26,
\]
where $m,W_{\rm c},s_{\rm c}$ are the fixed constants of
Proposition~\ref{prop:pair-star-complex-interface}. The procedure uses
at most $p+C_0^*d$ fractional bits and
$C_0^*d+3$ integer and sign bits per real component
internally; these widths are $O(p)$.''')
    text = replace_once(text, r'''Put $\Delta=\lceil C_0d^{C_1}\rceil$. Since $d\le b_dp^\epsilon$
and $\epsilon C_1<1$, a common cutoff gives $\Delta\le p$.''',
                        r'''Put $\Delta=C_0^*d$. Since $d\le b_dp^\epsilon$
and $\epsilon<1$, a common cutoff gives $\Delta\le p$.''')
    text = replace_once(text, r'''The guard-width calculation above bounds both denominator and magnitude
growth by $\lceil C_0d^{C_1}\rceil$. Since $d\le b_dp^\epsilon$ and
$\epsilon C_1<1$, this is $o(p)$ uniformly over the allowed $d$, so''',
                        r'''Proposition~\ref{prop:linear-guard} bounds both denominator and magnitude
growth by $C_0^*d$. Since $d\le b_dp^\epsilon$ and
$\epsilon<1$, this is $o(p)$ uniformly over the allowed $d$, so''')
    return text


def resampling(text):
    text = replace_once(text, r'\subsection{The one-dimensional interface}',
                        note('assembly-lu-resampling.tex')+'\n'
                        r'\subsection{The one-dimensional interface}')
    text = replace_once(text, r'''be integers, with $\gcd(s,t)=1$ and
\[
 \theta:=t/s-1>p/\alpha^4.
\]
Define coordinate permutations by''', r'''be integers, with $\gcd(s,t)=1$ and $t<2s$. Let $L,w,m$ be as in
Section~\ref{sec:banded-solve}, and assume $L\le p$ and $s\ge4m$.
Define coordinate permutations by''')
    text = replace_once(text, r''' P_sF_s=2^{2\alpha^2}B_0P_tF_tA.
 \label{eq:no-sort-one-dimensional}''', r''' P_sF_s=2^{2\alpha^2+L+1}B_0P_tF_tA.
 \label{eq:no-sort-one-dimensional}''')
    text = replace_once(text, r'''than $p^2$ and time
\[
 O(tp^{3/2+\delta}\alpha).
\]
The constant is uniform''', r'''than $p^2$ and time
\[
 O(tp^{3/2+\delta}\alpha),
\]
the second given the factor stream of Lemma~\ref{lem:banded-solve}, which
is written once in time $O(sp^3)$.
The constant is uniform''')
    start = text.index(r'The exact Gaussian identity and inverse estimate proved in')
    end = text.index(r'which is \eqref{eq:no-sort-one-dimensional}.', start)
    text = text[:start]+r'''The exact Gaussian identity proved in
\cite[Theorem~4.2]{HarveyHoeven2021} gives
\begin{equation}
 \mathsf T P_sF_s=P_tF_t\mathsf S.
 \label{eq:gaussian-public-facts}
\end{equation}
It uses the negative Fourier sign in our definition of
$F_q$; its right-hand permutation is consequently multiplication of the
frequency by $-s$. The identity holds for every $\alpha>0$ and coprime
$s<t$~\cite[Section~4.1]{HarveyHoeven2021}. By
Lemma~\ref{lem:scaled-dominance}, $N$ is invertible; no lower bound on
$\theta=t/s-1$ is used. Put
\[
 \mathsf S'=\mathsf S/2,\qquad
 \mathsf J=N^{-1}/2^{L+2},\qquad
 \mathsf D'=2^{-(2\alpha^2-2)}\mathsf D.
\]
Lemma~4.5 and the estimate~(4.1) of the cited paper give
$\|\mathsf S\|<1+\alpha^{-1}\le\frac32$ and
$\|\mathsf D\|\le e^{\pi\alpha^2/4}<2^{1.14\alpha^2}\le2^{2\alpha^2-2}$
for $\alpha\ge2$, as in the proof of its Proposition~4.7(i), and
Lemma~\ref{lem:banded-solve} gives $\|\mathsf J\|\le0.251$. Thus
\[
 \|\mathsf S'\|<\frac34,\qquad
 \|\mathsf J\|<1,\qquad
 \|\mathsf D'\|<1.
\]
Now set $A=\mathsf S'$ and $B_0=\mathsf D'\mathsf JC$.
Because $\|C\|=1$, both are contractions. The diagonal map $\mathsf D$
is invertible, and $C\mathsf T=N\mathsf D^{-1}$, so
\[
 (\mathsf D N^{-1}C)\mathsf T
 =\mathsf D N^{-1}(N\mathsf D^{-1})=I.
\]
Applying this left inverse to \eqref{eq:gaussian-public-facts} gives
$\mathsf D N^{-1}CP_tF_t\mathsf S=P_sF_s$. The normalizations in
$\mathsf D'$, $\mathsf J$, and $\mathsf S'$ have product
$2^{-(2\alpha^2-2)}2^{-(L+2)}2^{-1}=2^{-(2\alpha^2+L+1)}$. Hence
\[
 B_0P_tF_tA
 =2^{-(2\alpha^2+L+1)}\mathsf D N^{-1}CP_tF_t\mathsf S
 =2^{-(2\alpha^2+L+1)}P_sF_s,
\]
'''+text[end:]
    text = replace_once(text, r'''Lemmas~4.8, 4.9 and 4.12 of
\cite{HarveyHoeven2021} supply the following algorithms.''',
                        r'''Lemmas~4.8 and~4.9 of
\cite{HarveyHoeven2021} and Lemma~\ref{lem:banded-solve} supply the
following algorithms.''')
    text = replace_once(text, r''' \widetilde{\mathsf J}'&3p^2/4&O(tp^{3/2+\delta}\alpha)\\
 \widetilde{\mathsf D}'&4&O(tp^{1+\delta}).
\end{array}
\]''', r''' \widetilde{\mathsf J}&2&O(smw^{1+\delta})\\
 \widetilde{\mathsf D}'&4&O(tp^{1+\delta}).
\end{array}
\]
The cited Lemmas~4.8 and~4.9 assume the hypotheses of the cited
Proposition~4.7, which include $\theta>p/\alpha^4$. Their proofs use only
$p>100$, $s,t<2^p$, $2\le\alpha<p^{1/2}$, the bounds $\|\mathsf S'\|<\frac34$
and $\|\mathsf D'\|<1$ above, the cited Lemmas~2.13 and~2.14 and
Corollary~2.10, and never $\theta$. Where the proof of Lemma~4.9 writes
$\alpha>2$, it bounds the weight $\frac12\alpha^{-1}$ by $\frac14$, which
also holds for $\alpha=2$. The bound for $\widetilde{\mathsf J}$ assumes the
factor stream of Lemma~\ref{lem:banded-solve}, written once in time
$O(sm^2w^2)=O(sp^3)$, since $L\le p$ gives $w=O(p)$ and $m\le\sqrt w$.
Also $smw^{1+\delta}=O(tp^{3/2+\delta})$.
''')
    text = replace_once(text, r''' \widetilde B_0=\widetilde{\mathsf D}'\,
                    \widetilde{\mathsf J}'\,C.
\]
Contraction of the exact maps yields errors less than $16p<p^2$ and
$4+3p^2/4<p^2$, respectively.''', r''' \widetilde B_0=\widetilde{\mathsf D}'\,
                    \widetilde{\mathsf J}\,C.
\]
Contraction of the exact maps yields errors less than $16p<p^2$ and
$4+2<p^2$, respectively.''')
    text = replace_once(text, r'''The algorithms for $A$ and $B_0$ use $C$ and the
three quoted arithmetic maps, with all their original truncations.''',
                        r'''The algorithms for $A$ and $B_0$ use $C$, the
two quoted arithmetic maps and the banded solve, with all their stated
truncations.''')
    start = text.index('The Neumann evaluation also keeps its computed records bounded.')
    end = text.index(r'\end{proof}', start)
    text = text[:start]+r'''For the $\mathsf S'$ procedure, if the window radius
$\varrho=\lceil\sqrt p\rceil\alpha$ satisfies $s\leq2\varrho$, then
$O(1+\varrho/s)$ traversals of the period cost $O((s+\varrho)p)=O(\varrho p)$
per output. This also covers windows longer than one period.

The banded solve replaces the cited Neumann evaluation. Its factor
stream depends only on $p,s,t,\alpha$ and is written once, before any line
is processed. Each call reads it once forward and once backward, so the
stream head ends where it started. The proof of
Lemma~\ref{lem:banded-solve} includes its record conversions, its queues
and its tape for the rows in $\mathcal B$. All truncations are those of
the cited algorithms and of Lemma~\ref{lem:banded-solve}, and the tape
count and constants remain uniform in the parameters.
'''+text[end:]
    text = replace_once(text, r'''Put $T=\prod_i t_i$, $\gamma=2d\alpha^2$, and''',
                        r'''Put $T=\prod_i t_i$, $\gamma=\sum_i(2\alpha^2+L_i+1)$, where $L_i$ is the
value of $L$ in Section~\ref{sec:banded-solve} for $(s_i,t_i)$, and''')
    text = replace_once(text, r'''$O(dTp^{3/2+\delta}\alpha)$, with a constant independent of $d$.''',
                        r'''$O(dTp^{3/2+\delta}\alpha)$, with a constant independent of $d$, and
their factor streams are written in total time $O(\sum_is_ip^3)$.''')
    text = replace_once(text, r'''Initial padding costs $O(Tp)$, and scanning and zeroing the remaining''',
                        r'''Before the lines of axis $i$ are compressed, its factor stream is
written once on a fixed work tape, in time $O(s_ip^3)$; every call on
that axis reads it there, and the tape is cleared afterwards.
Initial padding costs $O(Tp)$, and scanning and zeroing the remaining''')
    return text


def assembly(text, gap):
    text = replace_once(text, r'''$p^2 2^{-p}$ and cost $O(tp^{3/2+\delta}\alpha)$ on a line of length
$t$.  Address''', r'''$p^2 2^{-p}$ and cost $O(tp^{3/2+\delta}\alpha)$ on a line of length
$t$, after a factorization computed once per axis.
Address''')
    start = text.index('Put $a=29646101715649/10^{22}$')
    end = text.index(r'\subsection{Input and transform sizes}', start)
    text = text[:start]+r'''Put $a=29646101715649/10^{22}$, $a_{\rm c}=4/10^9$ and $t=10^{-12}$.
Choose
\begin{equation}\label{eq:fixed-parameters}
\begin{gathered}
 \tau=1-a,\quad\sigma=1-a_{\rm c},\quad
 \beta=\frac1{10},\quad c=1,\quad\delta=\frac1{10^{12}},\\
 \epsilon=\frac{124999999}{250000000},\quad
 \lambda=1-a(1-t/2),\quad\lambda'=1-a(1-t),\\
 \kappa=\frac{296461013}{2\cdot10^{17}}>2^{-30}.
\end{gathered}
\end{equation}
Here $\sigma<\tau$, so the compact-control recurrence has
$\chi=\tau+(1-\beta)\max\{\sigma-\tau,0\}=\tau$.
Exact rational comparisons give
\[
 \max\{\tau,\sigma,\chi\}<\lambda<\lambda'<1,\quad
 \sigma+\beta(1-\sigma)<\lambda',\quad 1-c=0<\lambda'.
\]
The stopping test is $e^{10}<d$. Proposition~\ref{prop:linear-guard}
bounds the coefficient widths of the layer by $p+O(d)$, using the new
complex network's actual $W_{\rm c},s_{\rm c}$ in its node constant; it
needs only $\epsilon<1$.

The choice $c=1$ gives $K=d$. The front and back reservation counts are
$O(\log p)$, while the row reservation count is $O(\log d)$.
Their sum is $o(d)$ since $d=\Theta(p^\epsilon)$, and their preprocessing
exponent $\max\{1-c,0\}=0$ is strictly below $\lambda'$.
The compact-field, repair and row-splitting proofs apply without change.
Also $2\epsilon<1$ gives $K=o(\ell)$.
The constant-width Gaussian choice below gives the remaining comparisons
\[
 \epsilon<\tfrac12,\quad
 \epsilon(1-\tau)<1-\tau,\quad
 \tfrac12+\delta+\epsilon<1,\quad
 \epsilon(1+c)<1,\quad \epsilon+\delta<1;
\]
the first serves both the source scale and the prime intervals.

'''+text[end:]
    text = replace_once(text, r'''Set
\[
 \alpha=\left\lceil(32db)^{1/4}\right\rceil,
 \qquad \gamma=2d\alpha^2,\qquad \eta=\frac1{4d}.
\]
The ceiling does not affect the needed bounds: for $A\ge1$,
$\lceil A\rceil\le2A$, and hence
\begin{equation}\label{eq:gamma}
 \alpha\le2(32db)^{1/4},\qquad
 \gamma<46d^{3/2}\sqrt b\le46b^{1/2+3\epsilon/2}=46b^{3199999997/4000000000}.
\end{equation}
It follows that $2\le\alpha<\sqrt p$ eventually and $\gamma=o(b)$.
For example $b\ge2^{40}$ implies $\gamma\le b/4$.''', r'''Set
\[
 \alpha=2,\qquad \eta=\frac1{4d}.
\]
The source scale $\gamma$ depends on the prime lengths chosen below and
is fixed in \eqref{eq:gamma}.''')
    text = replace_once(text, r'''$\theta_i\geq\eta/(1-\eta)>\eta$. Therefore
\[
 \alpha^4\theta_i>\frac{32db}{4d}=8b>6b=p.
\]
The choice of $\alpha$ gives
$\alpha=\Theta(p^{1/4+\epsilon/4})$, and \eqref{eq:gamma} already
ensures $2\leq\alpha<\sqrt p$ for large $n$. We also have
$t_i\leq r\leq T<8n/b<2^{6b}=2^p$.''', r'''$\theta_i\geq\eta/(1-\eta)>\eta$, so $s_i/(t_i-s_i)=1/\theta_i<4d$.
The lower bound gives $s_i>(1-2\eta)t_i\geq t_i/2$, so $t_i<2s_i$. Put
\begin{equation}\label{eq:gamma}
 L_i=\left\lceil\frac{4533\,s_i}{4000\,(t_i-s_i)}\right\rceil,\qquad
 \gamma=\sum_{i=1}^d(2\alpha^2+L_i+1).
\end{equation}
This $L_i$ is the value of $L$ in Section~\ref{sec:banded-solve} for
$(s_i,t_i)$ and $\alpha=2$. Then $L_i\le\lceil4.533d\rceil$, and for
$d\ge22$
\[
 \gamma\le d(10+4.533d)\le5d^2\le5b^{2\epsilon}=5b^{124999999/125000000}.
\]
Hence $\gamma=o(b)$; for example $b\ge2^{541000000}$ gives
$b^{1-2\epsilon}\geq20$ and so $\gamma\le b/4$. Also $L_i\le p$, the solve
precision $w_i=3p+2L_i+12$ is at most $6p$, and the band
$m_i=\lceil\sqrt{w_i}/2\rceil$ satisfies $4m_i\le r/4\le s_i$ for large
$n$. We also have $2\le\alpha<\sqrt p$ and
$t_i\leq r\leq T<8n/b<2^{6b}=2^p$.''')
    text = replace_once(text, r'''For example, $d=\lfloor b^{399999999/2000000000}\rfloor$ is found by binary search
using exact comparisons $d^{2000000000}\le b^{399999999}$; the exponent is fixed.''',
                        r'''For example, $d=\lfloor b^{124999999/250000000}\rfloor$ is found by binary search
using exact comparisons $d^{250000000}\le b^{124999999}$; the exponent is fixed.''')
    text = replace_once(text, r'''Proposition~\ref{prop:simultaneous-layer} uses
$C_1=461/100$, so $\epsilon C_1<1$ makes its coefficient width $O(p)$.''',
                        r'''Proposition~\ref{prop:simultaneous-layer} uses the linear guard of
Proposition~\ref{prop:linear-guard}, so $\epsilon<1$ makes its coefficient
width $O(p)$.''')
    text = replace_once(text, r'''$b\ge2^{40}$, together with the other eventual construction conditions,''',
                        r'''$b\ge2^{541000000}$, together with the other eventual construction conditions,''')
    text = replace_once(text, r'''Gaussian line maps & $dp^{1/2+\delta}\alpha$ & $3/4+\delta+5\epsilon/4$\\''',
                        r'''Gaussian line maps & $dp^{1/2+\delta}$ & $1/2+\delta+\epsilon$\\''')
    text = replace_once(text, r''' g_5=1/4-\delta-5\epsilon/4,\\''', r''' g_5=1/2-\delta-\epsilon,\\''')
    start = text.index('Exact substitution in the unchanged seven-term assembly accounting gives')
    end = text.index(r'$K=d=\Theta(p^\epsilon)=o(\ell)$', start)
    require(gap == Q(22306317521666189976715649, 25*10**41) and gap > Q(8, 10**18),
            'Displayed absorption gap differs from the certificate')
    text = text[:start]+r'''Exact substitution in the seven-term assembly accounting gives
\[
 G_*:=\min_i g_i=g_3=\epsilon(1-\lambda')=\epsilon a(1-t)>
 \frac{296461013}{2\cdot10^{17}}=\kappa.
\]
In particular the absorption gap is the exact positive rational
\[
 \rho=G_*-\kappa
 =\frac{22306317521666189976715649}{25\cdot10^{41}}
 >\frac8{10^{18}}>0.
\]
The compact movement, reservation and local repair costs remain included in
the completed-layer term $g_3$. The fixed strict gap absorbs all remaining
fixed powers of $\log p$.
The guard is $O(d)=o(p)$, while $\alpha=2$ and
$\gamma=O(p^{2\epsilon})=o(p)$. Also
'''+text[end:]
    text = replace_once(text, r''' =O(dTp^{3/2+\delta}\alpha).
\]
Dividing by $V=Tp$ gives the fifth row.  The factor
$\alpha=\Theta(p^{1/4+\epsilon/4})$ explains its displayed power of $p$.''',
                        r''' =O(dTp^{3/2+\delta}),
\]
because $\alpha=2$. Dividing by $V=Tp$ gives the fifth row. The factor
streams of Lemma~\ref{lem:tensor-resampling} cost
$O(\sum_is_ip^3)=O(drp^3)$ for each tensor map. Since
$T/r\geq(r/2)^{d-1}$ and $r$ exceeds every fixed power of $p$, this is
$o(Tp)$.''')
    return text


def patched_files():
    result = assembly_certificate()
    require(result['headline_kappa'] == KAPPA == Q(296461013, 2*10**17),
            'Unexpected assembly headline')
    gap = result['witness']['absorption_gap']
    for name, old, new in pair_star_files():
        if name.endswith(('main.tex', '00-introduction.tex')):
            new = replace_once(new, r'\kappa='+PAIR_STAR_HEADLINE, r'\kappa='+HEADLINE)
            if name.endswith('main.tex'):
                new = replace_once(new, r'''generated during odepoint's just-for-fun experiment with AI.''',
                                   r'''generated during odepoint's just-for-fun experiment with AI.
A further revision replaces the coefficient guard of the simultaneous
layer and the solve of the Gaussian resampling system
(Sections~\ref{sec:linear-guard} and~\ref{sec:banded-solve}).''')
            else:
                new = replace_once(new, r'''source and target coordinate permutations in the transform identity,
so they need not be executed as separate full sorts.''',
                                   r'''source and target coordinate permutations in the transform identity,
so they need not be executed as separate full sorts. It also solves the
square Gaussian system by a precomputed banded factorization, which
allows a constant Gaussian width.''')
        elif name.endswith('03-motifs.tex'):
            new = motifs(new)
        elif name.endswith('05-layers.tex'):
            new = layers(new)
        elif name.endswith('07-resampling.tex'):
            new = resampling(new)
        elif name.endswith('08-assembly.tex'):
            new = assembly(new, gap)
        yield name, old, new


if __name__ == '__main__':
    patch = ''.join(''.join(difflib.unified_diff(old.splitlines(keepends=True),
            new.splitlines(keepends=True), fromfile=f'a/{name}', tofile=f'b/{name}'))
            for name, old, new in patched_files())
    path = ROOT/'patches/assembly-lu-30.patch'
    path.write_text(patch)
    print('Wrote independent assembly patch:', path.name)
    print('Conditional kappa=296461013/(2*10^17) > 2^-30.')
