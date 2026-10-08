#!/usr/bin/env python3
"""Independent pinned-source patch for the pair-star complex network.

Retains the earlier project refinements and changes only the complex motif
and the resulting exact assembly witness. The pinned upstream is untouched.
"""
import difflib
from fractions import Fraction as Q
from pathlib import Path

from certify import require
from complex_pair_star_parameters import certificate as parameter_certificate
from make_compact_control_patch import patched_files as compact_files
from make_patch import replace_once

ROOT = Path(__file__).resolve().parents[1]
HEADLINE = r'5929220328/10^{19}'


def note(name):
    return (ROOT/'notes'/name).read_text()


def motifs(text):
    text=replace_once(text,r'''\tau=1-\frac{296}{10^{11}},\qquad \sigma_{50}''',
                     r'''\tau_0=1-\frac{296}{10^{11}},\qquad \sigma_{50}''')
    text=replace_once(text,note('independent-complex.tex'),
                     r'''\subsection{A sharper exponent for the retained bit network}
\label{sec:paired-exponent-refinement}
Keep the same paired $h_{\rm b}=50$ bit graph and its exact counts.
Its arity and relative rank deficit are
\[
 m_{\rm b}=125000,\qquad\eta_{\rm b}=\frac{23}{661055000}.
\]
The conservative exponent $\tau_0$ above can be sharpened without changing
the graph. Put $a_{\rm b}=29646101715649/10^{22}$. With the rational
logarithm bounds $S,E_0$ just defined, set
\[
 L_{\rm b}=16\bigl(S(2)+E_0(2)\bigr)
       +S(125000/2^{16})+E_0(125000/2^{16}).
\]
Then $\log m_{\rm b}\le L_{\rm b}$, and exact rational comparison gives
$\eta_{\rm b}+\eta_{\rm b}^2/2>a_{\rm b}L_{\rm b}$.
\begin{lemma}\label{lem:paired-bit-sharp-exponent}
The retained paired bit graph satisfies
$s_{\rm b}/W_{\rm b}<m_{\rm b}^{1-a_{\rm b}}$.
\end{lemma}
\begin{proof}
Since $0<\eta_{\rm b}<1$, the positive logarithm series gives
\[
 -\log(1-\eta_{\rm b})
 >\eta_{\rm b}+\eta_{\rm b}^2/2
 >a_{\rm b}L_{\rm b}\ge a_{\rm b}\log m_{\rm b}.
\]
Exponentiating and using $s_{\rm b}/W_{\rm b}
=m_{\rm b}(1-\eta_{\rm b})$ proves the claim.
\end{proof}

''' +note('complex-pair-star-construction.tex'))
    text=replace_once(text,r'''The exponents used from now on are
\begin{equation}\label{eq:explicit-motif-exponents}
 \tau=1-296/10^{11},\qquad\sigma=1-418/10^{12}.
\end{equation}''',r'''The exponents used from now on are
\begin{equation}\label{eq:explicit-motif-exponents}
 \tau=1-29646101715649/10^{22},\qquad\sigma=1-4/10^9.
\end{equation}
The exact pair-star deficit is $\eta_{\rm c}=37/948319488$.
An exact rational logarithm enclosure gives
$\eta_{\rm c}>(4/10^9)\log(13824)$, so
$s_{\rm c}/W_{\rm c}<m_{\rm c}^{\sigma}$ by $e^{-x}>1-x$.
The bit and complex arities remain independent: the bit primitive supplies
arbitrary-width swaps with exponent $\tau$, and the complex layer uses its
own fixed $m_{\rm c},W_{\rm c},s_{\rm c}$ for branching and depth.''')
    return text


def layers(text):
    text=text.replace('prop:compact-complex-interface','prop:pair-star-complex-interface')
    text=replace_once(text,r'''$m=m_{\rm c}=15625$, $W=W_{\rm c}=58645352620000$ and
$s=s_{\rm c}=916333630984500000$''',r'''$m=m_{\rm c}=13824$, $W=W_{\rm c}=4496369044992$ and
$s=s_{\rm c}=62157803252796416$''')
    text=replace_once(text,r'''$\tau=1-296/10^{11}$.''',
                     r'''$\tau=1-29646101715649/10^{22}$.''')
    text=replace_once(text,r'''Fix $\tau=1-296/10^{11}$ and $\sigma=1-418/10^{12}$.''',
                     r'''Fix $\tau=1-29646101715649/10^{22}$ and $\sigma=1-4/10^9$.''')
    return text


def swaps(text):
    return replace_once(text,r'''We use the rational value $\tau=1-\frac{296}{10^{11}}$ established in
\eqref{eq:explicit-motif-exponents}. Its verification uses fixed integer
comparisons and the displayed exponential inequality; it needs no
real-arithmetic oracle.''',r'''We use the rational value $\tau=1-29646101715649/10^{22}$ established in
Lemma~\ref{lem:paired-bit-sharp-exponent} and
\eqref{eq:explicit-motif-exponents}. Its verification uses fixed rational
comparisons and the displayed logarithm-series inequality; it needs no
real-arithmetic oracle.''')


def assembly(text):
    start=text.index('Put $a=296/10^{11}$')
    end=text.index(r'\subsection{Input and transform sizes}',start)
    text=text[:start]+r'''Put $a=29646101715649/10^{22}$, $a_{\rm c}=4/10^9$ and $t=10^{-12}$.
Choose
\begin{equation}\label{eq:fixed-parameters}
\begin{gathered}
 \tau=1-a,\quad\sigma=1-a_{\rm c},\quad
 \beta=\frac1{10},\quad\zeta=\frac1{100},\quad C_1=\frac{461}{100},\\
 \epsilon=\frac{399999999}{2000000000},\quad c=1,\quad\delta=\frac1{10^{12}},\\
 \lambda=1-a(1-t/2),\quad\lambda'=1-a(1-t),\quad
 \kappa=\frac{5929220328}{10^{19}}>2^{-31}.
\end{gathered}
\end{equation}
Here $\sigma<\tau$, so the compact-control recurrence has
$\chi=\tau+(1-\beta)\max\{\sigma-\tau,0\}=\tau$.
Exact rational comparisons give
\[
 \max\{\tau,\sigma,\chi\}<\lambda<\lambda'<1,\quad
 \sigma+\beta(1-\sigma)<\lambda',\quad 1-c=0<\lambda'.
\]
The stopping test is $e^{10}<d$. Section~\ref{sec:compact-stopped-guard}
proves the displayed $C_1$, with $\epsilon C_1<1$, using the new complex
network's actual $W_{\rm c},s_{\rm c}$ in its finite guard constants.

The choice $c=1$ gives $K=d$. The front and back reservation counts are
$O(\log p)$, while the row reservation count is $O(\log d)$.
Their sum is $o(d)$ since $d=\Theta(p^\epsilon)$, and their preprocessing
exponent $\max\{1-c,0\}=0$ is strictly below $\lambda'$.
The compact-field, repair and row-splitting proofs apply without change.
Also $2\epsilon<1$ gives $K=o(\ell)$.
The retained Gaussian choice gives the remaining comparisons
\[
 \epsilon<\tfrac13,\quad 2\epsilon<1,\quad
 \epsilon(1-\tau)<1-\tau,\quad
 \tfrac34+\delta+\tfrac54\epsilon<1,\quad
 \epsilon(1+c)<1,\quad \epsilon+\delta<1.
\]

''' +text[end:]
    text=replace_once(text,r'b^{1999/10000}',r'b^{399999999/2000000000}')
    text=replace_once(text,r'd^{10000}\le b^{1999}',
                     r'd^{2000000000}\le b^{399999999}')
    text=replace_once(text,r'b^{15997/20000}',r'b^{3199999997/4000000000}')
    text=replace_once(text,r'$C_1=49961/10000$',r'$C_1=461/100$')
    text=replace_once(text,r'''$O(\log d+d^{1-c}\log p)$ reserved row and compact-control axes,''',
                     r'''$O(\log d+\log p)$ reserved row and compact-control axes,''')
    start=text.index('Exact substitution in the unchanged seven-term assembly accounting gives')
    end=text.index('Here $d$',start)
    text=text[:start]+r'''Exact substitution in the unchanged seven-term assembly accounting gives
\[
 G_*:=\min_i g_i=g_3=\epsilon(1-\lambda')=\epsilon a(1-t)>
 \frac{5929220328}{10^{19}}=\kappa.
\]
In particular the absorption gap is the exact positive rational
\[
 \rho=G_*-\kappa
 =\frac{601639843694386501715649}{2\cdot10^{43}}
 >\frac3{10^{20}}>0.
\]
The compact movement, reservation and local repair costs remain included in
the completed-layer term $g_3$. The fixed strict gap absorbs all remaining
fixed powers of $\log p$.
The guard is $O(d^{461/100})=o(p)$, while
$\alpha=\Theta(p^{(1+\epsilon)/4})$ and
$\gamma=O(p^{(1+3\epsilon)/2})=o(p)$. Also
$K=d=\Theta(p^\epsilon)=o(\ell)$, $K/\log p\to\infty$,
and $\ell=\Theta(p^{1-\epsilon})$. The prime-interval ratio grows as
$p^{1-2\epsilon}$. All construction and precision conditions hold beyond
a common fixed cutoff.

''' +text[end:]
    return text


def patched_files():
    from complex_pair_star import certificate as network_certificate
    network=network_certificate()
    n=network['counts']
    require((n['h'],n['m'],n['W'],n['L'],n['s'])==
            (24,13824,4496369044992,7078883328,62157803252796416),
            'Pair-star source constants differ from its exact construction')
    witness=parameter_certificate(n)['sharpened']
    p=witness['parameters']
    require(p['kappa'].numerator*10**19==5929220328*p['kappa'].denominator,
            'Unexpected sharpened pair-star headline')
    require(witness['absorption_gap']>Q(3,10**20),
            'Displayed strict absorption gap is too large')
    for name,old,new in compact_files():
        if name.endswith(('main.tex','00-introduction.tex')):
            new=replace_once(new,r'\kappa=83/10^{12}',r'\kappa='+HEADLINE)
            if name.endswith('main.tex'):
                new=replace_once(new,r'''\small Compact-control modifications: Douglas Colkitt}''',
                    r'''\small Earlier compact-control modifications: Douglas Colkitt\\
\small AI-generated pair-star experiment: odepoint}''')
                new=replace_once(new,
                    r'\title{Integer multiplication below \texorpdfstring{$n\log n$}{n log n}}',
                    r'\title{Integer multiplication, just for fun\\\large An experiment with AI-generated math}')
                new=replace_once(new,
                    'pdftitle={Integer multiplication below n log n}',
                    'pdftitle={Integer multiplication, just for fun}')
                new=replace_once(new,
                    'pdfauthor={OpenAI (original manuscript); Douglas Colkitt (modifications)}',
                    'pdfauthor={AI experiment by odepoint; original sources: OpenAI and Douglas Colkitt}')
                new=replace_once(new,
                    'Modified research draft; not an OpenAI release.',
                    'A just-for-fun experiment with AI-generated math; not an OpenAI release.')
                new=replace_once(new,
                    'Original: September 23, 2026; modified: October 7, 2026',
                    'Original: September 23, 2026; pair-star experiment: October 7, 2026')
                new=replace_once(new,r'''This derivative incorporates Douglas Colkitt's compact-control construction
and retained project refinements, prepared with assistance from OpenAI Codex.''',
                    r'''This derivative retains Douglas Colkitt's compact-control construction
and earlier project refinements, and adds the pair-star complex network
generated during odepoint's just-for-fun experiment with AI.
This write-up documents the model's proposed argument for a hobby project,
not a research paper.''')
        elif name.endswith('03-motifs.tex'):new=motifs(new)
        elif name.endswith('04-swap.tex'):new=swaps(new)
        elif name.endswith('05-layers.tex'):new=layers(new)
        elif name.endswith('08-assembly.tex'):new=assembly(new)
        new=replace_once(new,
            '% Conditional compact-control research draft; see main.tex for scope.',
            '% Integer multiplication, just for fun: an AI experiment by odepoint.\n'
            '% October 7, 2026. The math remains unreviewed; see main.tex for scope.')
        yield name,old,new


if __name__=='__main__':
    patch=''.join(''.join(difflib.unified_diff(old.splitlines(keepends=True),
            new.splitlines(keepends=True),fromfile=f'a/{name}',tofile=f'b/{name}'))
            for name,old,new in patched_files())
    path=ROOT/'patches/complex-pair-star-31.patch'
    path.write_text(patch)
    print('Wrote independent pair-star patch:',path.name)
    print('Conditional kappa=5929220328/10^19 > 2^-31.')
