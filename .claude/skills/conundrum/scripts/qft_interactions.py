#!/usr/bin/env python3
"""qft_interactions: the leading effects of INTERACTIONS on particle production, where the free-field
tools of qft_production.py are incomplete, with every function saying exactly WHICH quantity it returns
(numpy + mpmath, no scipy).

Why this tool exists
    qft_production.py treats free fields in prescribed backgrounds. Two interaction effects change the
    answer at leading order: (A) the produced pair attracts itself (Coulomb), which multiplies the weak-field
    Schwinger rate by exp(pi alpha); (B) produced quanta act back on the background that makes them
    (mean-field back-reaction, preheating). The usual traps still apply and are kept explicit in every
    "Quantity:" line: in-in expectation vs in-out amplitude vs vacuum persistence, per mode vs per volume,
    vacuum-decay rate vs pair-number rate, particles vs pairs (1/2 for a real field), real production vs
    transient vacuum polarization; plus two new ones: the bare vs the physical mass in the Schwinger exponent,
    and what the mean-field (Hartree) approximation leaves out (rescattering).

Units (read this first)
    Natural units hbar = c = 1, Heaviside-Lorentz electromagnetism (e^2 = 4 pi alpha), exactly as
    qft_production. Pick ONE energy unit (e.g. eV, or the mass m) for every energy, mass, momentum and field
    amplitude (a 3+1 scalar field has the dimension of a mass); times and lengths are in 1/energy, eE in
    energy^2, densities in energy^3, rates per volume in energy^4. SI conversions: qft_production's helpers
    (density_to_SI, rate_density_to_SI, time_from_inverse_eV, eE_from_field_SI). The command line accepts
    units through unit_tools.Q ("0.511 MeV", "1e17 V/m", "1e13 GeV").

PART A. Radiative (Coulomb) corrections to Schwinger pair production, weak constant field
-----------------------------------------------------------------------------------------
    Worldline instanton (Affleck, Alvarez & Manton 1982, Nucl. Phys. B197, 509; free account: Gould & Rajantie
    2017, arXiv:1704.04801, eqs. 9-11, 33-36, 41, 48-49). In Euclidean space a closed charged worldline x(tau)
    carries the action (on the proper-time saddle)
        S[x] = m L[x] - eE A[x] + e^2 V[x],      V[x] = (1/8 pi^2) oint oint dx.dy / |x - y|^2,
    L = length, A = area projected on the (x3, x4) plane, V = photon exchange in Feynman gauge (propagator
    1/(4 pi^2 r^2); the gauge part drops out on a closed loop). Without V the stationary loop is the circle of
    radius R = m/(eE), with m L - eE A = pi m^2/(eE): Schwinger's exponent.
    Mass renormalization (Polyakov's regularization, Gould & Rajantie eq. 41):
        V_a[x] = (1/8 pi^2) [ oint oint dx.dy / (|x - y|^2 + a^2)  -  (pi/a) L[x] ].
    The subtracted term is the self-energy of a straight piece of worldline, (1/8 pi^2) int ds/(s^2 + a^2) = 1/(8 pi a)
    per unit length, i.e. a mass shift delta m = e^2/(8 pi a) absorbed into m: the m in S is the PHYSICAL mass.
    For the circle the double integral is done exactly (int_0^2pi cos phi dphi/(A - B cos phi) = (2pi/B)(A/sqrt(A^2-B^2) - 1)):
        V_a(circle) = (1/4) [ (2 + eps^2)/(eps sqrt(4 + eps^2)) - 1 - 1/eps ] = -1/4 + 3 eps/32 + O(eps^3),  eps = a/R,
    so S_int = -e^2/4 = -pi alpha (R-independent) and the rate gains exp(+pi alpha) (Gould & Rajantie eq. 48:
    S = pi - kappa/4 in units where e^2 = kappa/eps). worldline_coulomb_action does the regulated double integral
    numerically for ANY smooth closed loop (spectrally accurate trapezoid, explicit counterterm, Richardson
    extrapolation a -> 0); the self-test reproduces -1/4 for the circle in two regularizations.
    Corrected rate (schwinger_radiative_rate), n = 1 (single-instanton) term, spin factor 2s + 1:
        Gamma_1 = (2s + 1) (eE)^2/(8 pi^3) exp(-pi m^2/(eE) + pi alpha)        [all orders in alpha, quenched]
        Gamma_1^(2-loop) = (2s + 1) (eE)^2/(8 pi^3) (1 + pi alpha) exp(-pi m^2/(eE))
                           [spinor: Lebedev & Ritus, Dunne eq. 4.16; scalar: the O(alpha) term of AAM's exp(pi alpha)]
    with relative corrections O(alpha sqrt(eE)/m) (spinor: -0.44 alpha pi sqrt(eE/m^2), Dunne 2004 eq. 4.20),
    O(e^{-pi m^2/eE}) (n = 2 terms) and O(kappa) = O(e^2 eE/m^2) (prefactor at leading order in kappa).
    WHICH QUANTITY: Gamma_1 is the n = 1 term of the vacuum-decay rate w = 2 Im L_eff (in-out: P(vacuum survives)
    = exp(-w V T)) AND, at the same leading weak-field order, the mean number of PAIRS per unit volume per unit
    time (in-in). Both, because at one loop the pair-number rate IS the n = 1 term (Nikishov; qft_production
    rates_from_modes), the Coulomb factor acts inside that single worldline loop (one pair attracting itself),
    and the decay rate and the pair rate differ only by multi-instanton terms O(e^{-2 pi m^2/eE}) (Gould &
    Rajantie's dilute instanton gas, eqs. 27-29). The n >= 2 terms are NOT given: their k coincident windings
    repel and the two-loop prefactor has singular -c_k sqrt(m^2/eE) terms (Dunne eqs. 4.16-4.19).

PART B. Self-interacting fields in mean field (Hartree / leading large N): preheating
-------------------------------------------------------------------------------------
    Minkowski space (no Hubble expansion). L = (1/2)(d phi)^2 - (1/2) m_phi^2 phi^2 - (lam_phi/4) phi^4
    + (1/2)(d chi)^2 - (1/2) m_chi^2 chi^2 - (1/2) g^2 phi^2 chi^2 - [chi self-interaction, Hartree]. The
    condensate phi0(t) is classical and homogeneous; chi is Gaussian with <chi> = 0, expanded in modes chi_k(t)
    that start in the adiabatic vacuum chi_k = e^{-i w t}/sqrt(2 w) (Wronskian chi chi*' - chi* chi' = i):
        chi_k'' + [k^2 + M^2(t)] chi_k = 0,       M^2 = m_chi^2 + g^2 phi0^2 + lam <chi^2>_ren,
        phi0'' + m_phi^2 phi0 + lam_phi phi0^3 + g^2 <chi^2>_ren phi0 = 0      (KLS 1997 eq. 86 with H = 0),
        <chi^2>_ren = int d^3k/(2pi)^3 [ |chi_k|^2 - 1/(2k) + theta(k - kappa) M^2(t)/(4 k^3) ].
    lam is the coefficient of <chi^2> in the chi mass: lam = 3 lam4 for one field with lam4 chi^4/4 (Hartree);
    lam = lam_N per component for an O(N) vector with (lam_N/4N)(chi.chi)^2 at leading order in 1/N (where the
    mean field is the controlled leading term). The solver is for ONE chi field coupled to phi0 (N = 1 in the
    condensate force g^2 <chi^2>_ren phi0 and in the energy): for an N-component chi coupled by g^2 phi^2 chi.chi/2
    the force on phi0 would be N g^2 <chi_1^2>_ren phi0, which no rescaling of g absorbs, so this code would
    underestimate that back-reaction by a factor N. n_chi, rho_chi, chi2_ren are per component.
    Renormalization (adiabatic subtraction to second order, Cooper et al. 1994 sec. 5; scale kappa, default m_phi):
    on the quadrature grid (cutoff Lambda) let Q = int d^3k/(2pi)^3 1/(2k) (~ Lambda^2/8pi^2) and
    L = int_{k > kappa} d^3k/(2pi)^3 1/(4k^3) (~ ln(Lambda/kappa)/8pi^2). The equations above are EXACTLY the bare
    Hartree equations, with S_B = int |chi_k|^2 = <chi^2>_ren + Q - L M^2, of the bare couplings
        1/lam_B = 1/lam - L,  g_B^2 = g^2/(1 - lam L),  m_chiB^2 = (m_chi^2 - lam Q)/(1 - lam L),
        m_phiB^2 = m_phi^2 + g^2 (L m_chiB^2 - Q),  lam_phiB = lam_phi + g^2 g_B^2 L,
    whose energy density is conserved exactly:
        H_B = pi0^2/2 + int (|chi_k'|^2 + k^2 |chi_k|^2)/2 + m_phiB^2 phi0^2/2 + lam_phiB phi0^4/4
              + m_chiB^2 S_B/2 + g_B^2 phi0^2 S_B/2 + lam_B S_B^2/4     (minus its constant initial value).
    (m_phi, lam_phi, m_chi, g, lam) are renormalized parameters at scale kappa: as Lambda grows at fixed values the
    solution converges like 1/Lambda^2 (leading missing tail of <chi^2>_ren: 3 M^4/(64 pi^2 Lambda^2), reported;
    the self-test checks the change when Lambda doubles, the 'convergence' subcommand the rate). Subtracting only
    1/(2k) would leave <chi^2> drifting like -Delta M^2 ln(Lambda)/(8 pi^2) (both show it). lam L < 1 is required (the Landau pole
    of the large-N model; refused otherwise).
    Initial state: phi0 = Phi at rest (a turning point, where d omega/dt = 0); chi in the zeroth-order adiabatic
    vacuum of M^2(0), solved self-consistently (gap equation) when lam != 0.
    Numerics: Hamiltonian splitting. H_0 = pi0^2/2 + m_phi^2 phi0^2/2 + sum_k W_k (|chi'|^2 + (k^2 + M_ref^2)|chi|^2)/2
    is rotated exactly, the rest (a function of positions only) is applied as kicks; Yoshida's 4th-order
    composition of Strang steps. Symplectic: the Wronskian of every mode is preserved to roundoff and the energy
    error is O(dt^4) and bounded. k grid: Gauss-Legendre on [0, kappa] and [kappa, Lambda], W_k = w_k k^2/(2 pi^2).
    The solver REFUSES (ValueError) a run whose energy drifted (step too large) or whose modes near the cutoff
    were excited (Lambda too low).
    Floquet reference (no back-reaction, lam = lam_phi = 0): phi0 = Phi cos(m_phi t) and each mode obeys the Mathieu
    equation y'' + (A - 2q cos 2z) y = 0 (DLMF 28.2.1) with z = m_phi t (+ pi/2),
        A_k = (k^2 + m_chi^2)/m_phi^2 + 2q,   q = g^2 Phi^2/(4 m_phi^2)      (KLS 1997 eq. 30);
    Floquet exponent mu from the monodromy matrix M over z in [0, pi], Delta = tr M / 2 = w_I(pi) (DLMF 28.2.16,
    evaluated over half a period with DLMF 28.2.11),
        mu = ln(|Delta| + sqrt(Delta^2 - 1))/pi  (|Delta| > 1),  0 otherwise;   n_k ~ exp(2 mu z) (KLS p. 7).
    Instability bands b_n(q) < A < a_n(q) (characteristic values from the Fourier-matrix eigenvalues; small-q
    series in DLMF 28.6). Narrow resonance: mu(A = 1) = q/2 (1 - 0.117 q^2 + ...) (KLS p. 10: mu_k ~ q/2).
    QUANTITIES: n_k(t) = (1/2 w_k)|w_k chi_k - i chi_k'|^2, w_k^2 = k^2 + M^2(t): the per-mode in-in mean number
    of chi PARTICLES in the instantaneous (zeroth-order adiabatic) basis. While phi0 oscillates this number is
    basis dependent (it contains transient vacuum polarization; in broad resonance it jumps at each zero of
    phi0): read it stroboscopically or where 'adiabaticity' is small; only after the condensate has decayed is it a
    final particle number. n_chi = int d^3k/(2pi)^3 n_k: particles per unit volume; chi is REAL, so each pair
    occupies k and -k: pairs = n_chi/2. <chi^2>_ren, phi0, energies: in-in expectation values.
    WHAT THE MEAN FIELD OMITS: rescattering (chi chi -> chi chi, chi phi0 -> chi delta-phi), the production of
    inflaton fluctuations delta-phi, and thermalization (KLS 1997 p. 24: the second polarization diagram "can
    be comparable"). Valid in the EARLY stage: from the vacuum through the onset of back-reaction, while
    occupation numbers have not yet driven 1/N or rescattering corrections to O(1).

Assumptions and validity range
    A: constant, homogeneous weak field eE <= m^2 (refused above), alpha <= 1 and kappa = 4 pi alpha eE/m^2 <= 1;
       quenched (one charged loop; virtual pairs only renormalize the charge, so alpha is the low-energy
       alpha = 1/137.036); m is the physical (pole) mass; leading exponential plus leading prefactor.
    B: Minkowski space; homogeneous condensate; Gaussian (Hartree / leading large-N) chi; early stage only; the
       k grid must resolve the resonance bands and reach beyond them (refused otherwise); lam L < 1.

Python usage
    import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
    import qft_interactions as qi
    qi.schwinger_radiative_rate(m=1.0, eE=0.05)                    # pair rate = n=1 decay term, x exp(pi alpha)
    qi.worldline_coulomb_action(qi.circle_instanton(1.0, 0.1, 2048))["V0"]   # -> -0.25 (action e^2 V0 = -pi alpha)
    qi.mathieu_floquet_exponent([1.0, 0.95], 0.1)["mu"]             # [~0.05, ...]
    qi.preheating_resonance_bands(m_phi=1.0, g=1e-2, Phi=200.0)     # q = 1: resonant k intervals
    r = qi.hartree_preheating(m_phi=1.0, g=0.1, Phi=60.0, t_end=40.0)   # q = 9, back-reaction on
    r["t"], r["phi0"], r["n_chi"], r["chi2_ren"], r["energy_drift_max"]

Command line (from the project root)
    python3 .claude/skills/conundrum/scripts/qft_interactions.py selftest
    python3 .claude/skills/conundrum/scripts/qft_interactions.py radiative --E "1e17 V/m"          (electron default)
    python3 .claude/skills/conundrum/scripts/qft_interactions.py worldline --n 2048
    python3 .claude/skills/conundrum/scripts/qft_interactions.py floquet --m-phi "1e13 GeV" --g 1e-4 --Phi "1e18 GeV" --k "2.5e13 GeV"
    python3 .claude/skills/conundrum/scripts/qft_interactions.py preheat --m-phi "1e13 GeV" --g 1e-3 --Phi "6e16 GeV" --t-end 60
    python3 .claude/skills/conundrum/scripts/qft_interactions.py convergence      (slow: regulator, cutoff and step studies)
"""
from __future__ import annotations

import math
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (_HERE, ".claude/skills/conundrum/scripts"):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import qft_production as qp  # noqa: E402  (free-field solvers, SI helpers)
from unit_tools import C, E_CHARGE, HBAR, unit  # noqa: E402  (CODATA 2018 values shared by the toolkit)

PI = math.pi
# Fine-structure constant from the toolkit's CODATA 2018 constants, alpha = e^2/(4 pi eps0 hbar c): 1/alpha = 137.0359990
# (the last digits carry the 11-digit rounding of eps0 in unit_tools, a 6e-10 relative effect).
ALPHA_FS = E_CHARGE ** 2 / (4 * PI * unit("eps0").si * HBAR * C)
_CBRT2 = 2.0 ** (1.0 / 3.0)
_Y1 = 1.0 / (2.0 - _CBRT2)          # Yoshida (1990) 4th-order triple-jump weights
_Y0 = -_CBRT2 / (2.0 - _CBRT2)


# ---------------------------------------------------------------- input checks
def _finite(x, name: str) -> float:
    try:
        x = float(x)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be a real scalar") from None
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x


def _pos(x, name: str) -> float:
    x = _finite(x, name)
    if x <= 0:
        raise ValueError(f"{name} must be > 0")
    return x


def _nonneg(x, name: str) -> float:
    x = _finite(x, name)
    if x < 0:
        raise ValueError(f"{name} must be >= 0")
    return x


# ================================================================ PART A: radiative corrections to Schwinger
def schwinger_radiative_rate(m: float, eE: float, alpha: float = ALPHA_FS, fermion: bool = True) -> dict:
    """Weak-field Schwinger rate with the leading radiative (Coulomb) correction, n = 1 (single-instanton) term.

    one_loop  = (2s+1) (eE)^2/(8 pi^3) exp(-pi m^2/eE)                 (2s+1 = 2 spinor, 1 scalar)
    two_loop  = one_loop x (1 + pi alpha)     spinor: Lebedev-Ritus, Dunne 2004 eq. 4.16 (spinor), c_1 = 0;
                                              scalar: the O(alpha) term of AAM's scalar exp(pi alpha) (the scalar
                                              two-loop Lagrangian is Ritus's, Dunne sec. 4.2), not eq. 4.16
    all_orders = one_loop x exp(pi alpha)                              (Affleck-Alvarez-Manton; quenched)
    Quantity: dict of rates per unit volume per unit time (energy^4): each is BOTH the n = 1 term of the in-out
        vacuum-decay rate w = 2 Im L_eff (Im L_eff alone is half of it) AND, at this leading weak-field order, the
        in-in mean number of PAIRS (one particle + one antiparticle; no 1/2 for a charged field) created per volume
        per time; 'enhancement' = exp(pi alpha); 'beta' = eE/m^2; 'kappa' = 4 pi alpha eE/m^2; 'n2_rel' = relative
        size of the omitted n = 2 term; 'next_rel' = estimated next correction, -0.44 alpha pi sqrt(beta) (spinor,
        Dunne eq. 4.20; None for scalars); 'log10_one_loop', 'log10_two_loop', 'log10_all_orders' = log10 of the
        rates in the same units (finite where the rates underflow to 0, pi m^2/eE > ~745).
    Valid when: constant homogeneous E; m > 0 is the PHYSICAL (pole) mass; 0 < eE <= m^2 (weak field; corrections
        O(alpha sqrt(eE)/m)); 0 < alpha <= 1 and kappa <= 1 (prefactor at leading order in kappa); quenched (alpha =
        low-energy value). n >= 2 terms are not included."""
    m, eE, alpha = _pos(m, "m"), _pos(eE, "eE"), _pos(alpha, "alpha")
    beta = (eE / m) / m
    if not (math.isfinite(beta) and beta > 0):
        raise ValueError(f"eE/m^2 = {beta!r} is not a finite positive number (inputs out of floating-point range)")
    if beta > 1.0:
        raise ValueError(f"eE/m^2 = {beta:.3g} > 1: not a weak field (the n = 1 instanton expansion fails)")
    if alpha > 1.0:
        raise ValueError("alpha > 1: outside the tested range")
    kappa = 4 * PI * alpha * beta
    if kappa > 1.0:
        raise ValueError(f"kappa = e^2 eE/m^2 = {kappa:.3g} > 1: the prefactor is only known at leading order in kappa")
    g = 2.0 if fermion else 1.0
    ln1 = math.log(g / (8 * PI ** 3)) + 2 * math.log(eE) - PI / beta    # no (eE)^2: it can overflow on its own
    if ln1 > 700:
        raise ValueError("rate exceeds the double-precision range (eE too large in these units)")
    pref = g * eE * eE / (8 * PI ** 3)
    # direct product where (eE)^2 is finite (keeps full relative precision; exp(ln1) would lose |ln1| x eps);
    # either form underflows to 0 for pi m^2/eE > ~745, where the log10 entries carry the value
    one = pref * math.exp(-PI / beta) if math.isfinite(pref) else math.exp(ln1)
    lg1 = ln1 / math.log(10)
    return {"one_loop": one, "two_loop": one * (1 + PI * alpha), "all_orders": one * math.exp(PI * alpha),
            "log10_one_loop": lg1, "log10_two_loop": lg1 + math.log10(1 + PI * alpha),
            "log10_all_orders": lg1 + PI * alpha / math.log(10),
            "enhancement": math.exp(PI * alpha), "beta": beta, "kappa": kappa,
            "n2_rel": 0.25 * math.exp(-PI / beta),
            "next_rel": (-0.44 * alpha * PI * math.sqrt(beta)) if fermion else None}


def circle_instanton(m: float, eE: float, n: int = 2048) -> np.ndarray:
    """Points of the one-loop worldline instanton of a constant field: a circle of radius R = m/(eE) in the
    Euclidean (x3, x4) plane, sampled at n equally spaced parameter values.

    Quantity: array (n, 2) of Euclidean coordinates in 1/energy (input for worldline_coulomb_action).
    Valid when: m > 0, eE > 0, n >= 16."""
    m, eE = _pos(m, "m"), _pos(eE, "eE")
    if int(n) < 16:
        raise ValueError("need n >= 16 points")
    th = 2 * PI * np.arange(int(n)) / int(n)
    return (m / eE) * np.stack([np.cos(th), np.sin(th)], axis=1)


def circle_exchange_action_closed(a_over_R) -> np.ndarray:
    """Exact Polyakov-regulated, self-energy-subtracted photon-exchange action of a circle, divided by e^2:
        V_a = (1/4) [ (2 + eps^2)/(eps sqrt(4 + eps^2)) - 1 - 1/eps ],   eps = a/R   (-> -1/4 as eps -> 0).

    Quantity: V_a (dimensionless, independent of R); the loop weight carries exp(-e^2 V_a).
    Valid when: a_over_R > 0 (any value; only the eps -> 0 limit is physical)."""
    e = np.asarray(a_over_R, dtype=float)
    if np.any(~np.isfinite(e)) or np.any(e <= 0):
        raise ValueError("a/R must be > 0")
    return 0.25 * ((2 + e * e) / (e * np.sqrt(4 + e * e)) - 1 - 1 / e)


def _loop_velocity(x: np.ndarray) -> np.ndarray:
    """dx/dtau for tau in [0, 1) by spectral differentiation of a uniformly sampled closed loop."""
    n = x.shape[0]
    kf = np.fft.fftfreq(n, d=1.0 / n)
    if n % 2 == 0:
        kf[n // 2] = 0.0
    return np.real(np.fft.ifft(2j * PI * kf[:, None] * np.fft.fft(x, axis=0), axis=0))


def worldline_exchange_action(points, a, scheme: str = "polyakov") -> dict:
    """Regulated, mass-subtracted photon-exchange action of a closed Euclidean worldline, divided by e^2.

    polyakov (Gould & Rajantie 2017 eq. 41):
        V_a = (1/8pi^2) [ int int dtau dtau' xdot.xdot' / (|x - x'|^2 + a^2) - (pi/a) int |xdot| dtau ]
    gaussian (their eq. 42): the counterterm is (sqrt(pi)/a^2) int int xdot.xdot' exp(-|x - x'|^2/a^2) instead.
    Both double integrals by the trapezoidal rule on the uniform parameter grid (spectrally accurate for a smooth
    periodic integrand once the spacing h <= a/5), xdot by spectral differentiation.
    Quantity: dict with 'V' (array over the given a: the action e^2 V_a in units of e^2, dimensionless; the loop
        weight carries exp(-e^2 V_a)), 'length' (1/energy) and 'spacing' (largest point spacing).
    Valid when: points (n, d), n >= 16, d >= 2, sample a smooth closed loop without cusps or self-intersections
        at equally spaced parameter values; every a >= 5 x spacing (else refused); a in 1/energy."""
    x = np.asarray(points, dtype=float)
    if x.ndim != 2 or x.shape[0] < 16 or x.shape[1] < 2 or not np.all(np.isfinite(x)):
        raise ValueError("points must be a finite (n >= 16, d >= 2) array")
    if scheme not in ("polyakov", "gaussian"):
        raise ValueError("scheme must be 'polyakov' or 'gaussian'")
    av = np.atleast_1d(np.asarray(a, dtype=float))
    if np.any(~np.isfinite(av)) or np.any(av <= 0):
        raise ValueError("regulator a must be > 0")
    n, d = x.shape
    spacing = float(np.max(np.sqrt(np.sum((np.roll(x, -1, axis=0) - x) ** 2, axis=1))))
    if np.min(av) < 5 * spacing:
        raise ValueError(f"regulator a = {np.min(av):.3g} < 5 x point spacing {spacing:.3g}: use more points")
    xd = _loop_velocity(x)
    dbl = np.zeros(len(av))
    gau = np.zeros(len(av))
    chunk = max(1, 2 ** 19 // n)
    for i0 in range(0, n, chunk):
        sl = slice(i0, min(n, i0 + chunk))
        r2 = np.zeros((sl.stop - sl.start, n))
        for c in range(d):
            diff = x[sl, c][:, None] - x[None, :, c]
            r2 += diff * diff
        dot = xd[sl] @ xd.T
        for j, aj in enumerate(av):
            dbl[j] += float(np.sum(dot / (r2 + aj * aj)))
            if scheme == "gaussian":
                gau[j] += float(np.sum(dot * np.exp(-r2 / (aj * aj))))
    dbl /= n * n
    gau /= n * n
    length = float(np.mean(np.sqrt(np.sum(xd * xd, axis=1))))
    ct = PI / av * length if scheme == "polyakov" else math.sqrt(PI) / av ** 2 * gau
    return {"V": (dbl - ct) / (8 * PI * PI), "length": length, "spacing": spacing}


def worldline_coulomb_action(points, a_values=None, scheme: str = "polyakov") -> dict:
    """Finite (renormalized) photon-exchange action of a closed worldline: worldline_exchange_action at several
    regulators a, extrapolated to a -> 0 by an exact polynomial fit in a (Richardson).

    Default a_values = (0.16, 0.08, 0.04, 0.02) x L/(2 pi) (L = loop length). For a stationary loop (worldline
    instanton) of a weak field the leading Coulomb factor of the rate is exp(-e^2 V0); for the circle V0 = -1/4.
    Quantity: dict with 'V0' (a -> 0 limit of the mass-subtracted exchange action divided by e^2, dimensionless),
        'V0_err' (|4-point minus 3-point extrapolation|), 'a', 'V_a', 'length'; 'factor_per_alpha' = -4 pi V0, so
        that the rate factor is exp(factor_per_alpha x alpha) (= exp(pi alpha) for the circle).
    Valid when: as worldline_exchange_action (smooth closed loop, smallest a >= 5 x spacing, at least 3 values of
        a); only the self-energy (linear) divergence is present (no cusps or intersections), so V0 is scheme
        independent; the physical claim exp(-e^2 V0) needs the loop to be the one-loop stationary worldline."""
    x = np.asarray(points, dtype=float)
    if x.ndim != 2 or x.shape[0] < 16:
        raise ValueError("points must be an (n >= 16, d) array")
    if a_values is None:
        length = float(np.mean(np.sqrt(np.sum(_loop_velocity(x) ** 2, axis=1))))
        a_values = np.array([0.16, 0.08, 0.04, 0.02]) * length / (2 * PI)
    av = np.asarray(a_values, dtype=float)
    if av.ndim != 1 or len(av) < 3 or len(set(av.tolist())) != len(av):
        raise ValueError("need at least 3 distinct regulator values")
    r = worldline_exchange_action(x, av, scheme)
    V = r["V"]
    order = np.argsort(av)
    a_s, V_s = av[order], V[order]
    V0 = float(np.linalg.solve(np.vander(a_s, len(a_s), increasing=True), V_s)[0])
    V0b = float(np.linalg.solve(np.vander(a_s[:-1], len(a_s) - 1, increasing=True), V_s[:-1])[0])
    return {"V0": V0, "V0_err": abs(V0 - V0b), "a": a_s, "V_a": V_s, "length": r["length"],
            "factor_per_alpha": -4 * PI * V0}


# ================================================================ PART B: Mathieu / Floquet theory
def mathieu_floquet_exponent(A, q, rtol: float = 1e-11) -> dict:
    """Floquet exponent of y'' + (A - 2 q cos 2z) y = 0 (DLMF 28.2.1) from the monodromy matrix over one period.

    M maps (y, y') at z = 0 to z = pi; Delta = tr M/2 = w_I(pi) (DLMF 28.2.16: cos(pi nu) = w_I(pi; a, q)), and by
    the symmetry of cos 2z about pi/2, w_I(pi) = 2 w_I(pi/2) w_II'(pi/2) - 1 (DLMF 28.2.11), so the fundamental
    solutions are integrated over half a period with qft_production's 4th-order Magnus stepper, Richardson-
    extrapolated in the step (error O(h^4) -> O(h^6)), steps doubled until Delta changes by < rtol;
    mu = ln(|Delta| + sqrt(Delta^2 - 1))/pi for |Delta| > 1 (unstable), 0 otherwise, evaluated as
    (ln|Delta| + ln(1 + sqrt(1 - 1/Delta^2)))/pi so that nothing is squared.
    Quantity: dict with 'mu' (growth exponent per unit z of the growing solution, dimensionless: |y|^2 and the
        occupation number grow like exp(2 mu z)), 'half_trace' Delta, 'unstable' (|Delta| > 1), 'steps'.
    Valid when: A, q real and finite (arrays broadcast); |A| + 2|q| <= 1e6 (step count); pi mu <= 700, i.e.
        |Delta| <= 1e304 (Delta is formed in double precision: deep tunnelling A << -2|q| or A << 2q with large q,
        e.g. A = 0, q >= ~5e4, overflows); refused (ValueError) when Delta is not finite or exceeds that bound, or
        when the step doubling reaches its cap (2^15 steps per half period) without meeting rtol."""
    A = np.atleast_1d(np.asarray(A, dtype=float))
    q = np.atleast_1d(np.asarray(q, dtype=float))
    A, q = np.broadcast_arrays(A, q)
    A, q = A.astype(float).ravel(), q.astype(float).ravel()
    if not (np.all(np.isfinite(A)) and np.all(np.isfinite(q))):
        raise ValueError("A and q must be finite")
    scale = float(np.max(np.abs(A) + 2 * np.abs(q)))
    if scale > 1e6:
        raise ValueError("|A| + 2|q| > 1e6: too many steps per period")
    w = np.ones_like(A)
    big = 1e304                       # |Delta| bound: pi mu <= 700; the u v product below must stay finite

    def half_trace(n):
        # u(0) = 1/sqrt2, u'(0) = -i/sqrt2, so w_I = sqrt2 Re u and w_II = -sqrt2 Im u.
        with np.errstate(over="ignore", invalid="ignore"):
            u, v = qp._magnus_boson(lambda z: A - 2 * q * np.cos(2 * z), 0.0, 0.5 * PI, n, w)
            d = -4.0 * np.real(u) * np.imag(v) - 1.0
        if not np.all(np.isfinite(d)) or np.any(np.abs(d) > big):
            raise ValueError("|Delta| = |tr M|/2 exceeds 1e304 (pi mu > 700): deep-tunnelling (A, q) outside the "
                             "double-precision range of this monodromy computation")
        return d

    n = 2 ** max(4, int(math.ceil(math.log2(2 * PI * math.sqrt(scale + 1)))))
    h1 = half_trace(n)
    h2 = half_trace(2 * n)
    e_old = (16 * h2 - h1) / 15
    while True:
        n *= 2
        h1, h2 = h2, half_trace(2 * n)
        e_new = (16 * h2 - h1) / 15
        if np.all(np.abs(e_new - e_old) <= rtol * np.maximum(1.0, np.abs(e_new))):
            break
        if n >= 2 ** 15:
            bad = float(np.max(np.abs(e_new - e_old) / np.maximum(1.0, np.abs(e_new))))
            raise ValueError(f"monodromy did not converge to rtol = {rtol:g} with 2^16 steps per half period "
                             f"(last relative change {bad:.2g})")
        e_old = e_new
    ad = np.abs(e_new)
    with np.errstate(divide="ignore", invalid="ignore"):
        mu = np.where(ad > 1, (np.log(ad) + np.log1p(np.sqrt(np.maximum(1.0 - (1.0 / ad) ** 2, 0.0)))) / PI, 0.0)
    return {"mu": mu, "half_trace": e_new, "unstable": ad > 1, "steps": 2 * n}


def mathieu_characteristic_values(q: float, n_max: int = 4) -> dict:
    """Mathieu characteristic values a_n(q) (n = 0..n_max) and b_n(q) (n = 1..n_max) as eigenvalues of the
    truncated Fourier (tridiagonal) matrices of the four parity classes (cos/sin of even/odd multiples of z).

    Quantity: dict with 'a' (array, index n) and 'b' (array, index n; b[0] = nan), dimensionless; the n-th
        instability band of y'' + (A - 2q cos 2z) y = 0 is b_n(q) < A < a_n(q).
    Valid when: 0 <= q <= 1e4, 0 <= n_max <= 400 (truncation K = n_max + 30 + 4 sqrt(q) Fourier terms per class;
        checked to 1e-13 against independent values for q <= 200)."""
    q = _nonneg(q, "q")
    if q > 1e4 or not (0 <= int(n_max) <= 400):
        raise ValueError("need 0 <= q <= 1e4 and 0 <= n_max <= 400")
    n_max = int(n_max)
    K = n_max + 30 + int(4 * math.sqrt(q))
    j = np.arange(K, dtype=float)

    def tri(diag):
        return np.diag(diag) + np.diag(np.full(K - 1, q), 1) + np.diag(np.full(K - 1, q), -1)

    m_ee = tri((2 * j) ** 2)                     # cos 2jz:      a_0, a_2, ...
    m_ee[0, 1] = m_ee[1, 0] = math.sqrt(2.0) * q
    m_oe = tri((2 * j + 2) ** 2)                 # sin (2j+2)z:  b_2, b_4, ...
    d = (2 * j + 1) ** 2
    m_eo = tri(d + np.where(j == 0, q, 0.0))     # cos (2j+1)z:  a_1, a_3, ...
    m_oo = tri(d - np.where(j == 0, q, 0.0))     # sin (2j+1)z:  b_1, b_3, ...
    ee, oe, eo, oo = (np.linalg.eigvalsh(mm) for mm in (m_ee, m_oe, m_eo, m_oo))
    a = np.empty(n_max + 1)
    b = np.full(n_max + 1, np.nan)
    for n in range(n_max + 1):
        if n % 2 == 0:
            a[n] = ee[n // 2]
            if n > 0:
                b[n] = oe[n // 2 - 1]
        else:
            a[n], b[n] = eo[n // 2], oo[n // 2]
    return {"a": a, "b": b}


def mathieu_band_edges(q: float, n: int = 1) -> tuple:
    """Edges (b_n(q), a_n(q)) of the n-th instability band of the Mathieu equation y'' + (A - 2q cos 2z) y = 0.

    Quantity: tuple (A_lower, A_upper), dimensionless; mu > 0 strictly between them (q > 0).
    Valid when: n >= 1, 0 <= q <= 1e4 (as mathieu_characteristic_values)."""
    if int(n) < 1:
        raise ValueError("band index n must be >= 1 (A < a_0 is the n = 0 region)")
    cv = mathieu_characteristic_values(q, int(n))
    return float(cv["b"][int(n)]), float(cv["a"][int(n)])


def preheating_mathieu_parameters(k, m_phi: float, g: float, Phi: float, m_chi: float = 0.0):
    """Mathieu parameters of a chi mode in an oscillating condensate phi0 = Phi cos(m_phi t), coupling g^2 phi^2 chi^2/2
    (KLS 1997 eq. 30): A_k = (k^2 + m_chi^2)/m_phi^2 + 2q, q = g^2 Phi^2/(4 m_phi^2), z = m_phi t.

    Quantity: tuple (A_k array, q), dimensionless.
    Valid when: m_phi > 0, g >= 0, Phi >= 0, m_chi >= 0, k >= 0 (energies in one unit); no back-reaction, no
        expansion, lam_phi = 0 (harmonic condensate)."""
    m_phi, g, Phi, m_chi = _pos(m_phi, "m_phi"), _nonneg(g, "g"), _nonneg(Phi, "Phi"), _nonneg(m_chi, "m_chi")
    k = np.atleast_1d(np.asarray(k, dtype=float))
    if np.any(~np.isfinite(k)) or np.any(k < 0):
        raise ValueError("k must be >= 0")
    q = g * g * Phi * Phi / (4 * m_phi * m_phi)
    return (k * k + m_chi * m_chi) / (m_phi * m_phi) + 2 * q, q


def preheating_floquet(k, m_phi: float, g: float, Phi: float, m_chi: float = 0.0) -> dict:
    """Floquet growth of chi modes in the prescribed condensate phi0 = Phi cos(m_phi t) (no back-reaction).

    Quantity: dict with 'A', 'q', 'mu' (exponent per unit z = m_phi t, dimensionless) and 'growth_rate' = 2 mu m_phi
        (energy, i.e. per unit time): the late-time rate of d ln n_k/dt of the per-mode in-in occupation (particles
        in mode k, stroboscopic), before back-reaction.
    Valid when: as preheating_mathieu_parameters; the growth holds while n_k << 1/g^2 (no back-reaction), in
        Minkowski space (no redshift)."""
    A, q = preheating_mathieu_parameters(k, m_phi, g, Phi, m_chi)
    r = mathieu_floquet_exponent(A, q)
    return {"A": A, "q": q, "mu": r["mu"], "growth_rate": 2 * r["mu"] * m_phi}


def preheating_resonance_bands(m_phi: float, g: float, Phi: float, m_chi: float = 0.0, n_bands: int = 3) -> list:
    """Momentum intervals of the lowest n_bands ACCESSIBLE Mathieu instability bands for phi0 = Phi cos(m_phi t):
    k^2 = m_phi^2 (A - 2q) - m_chi^2 with b_n(q) < A < a_n(q) and k^2 > 0 (since A >= 2q, broad resonance q >> 1
    starts at band n ~ sqrt(2q)), plus the largest mu on a 41-point scan of each band.

    Quantity: list of dicts {'n' (Mathieu band index), 'k_lo', 'k_hi' (energy; band clipped to k >= 0), 'mu_max'
        (per unit z = m_phi t), 'growth_rate_max' (= 2 mu_max m_phi, energy: rate of ln n_k)}.
    Valid when: as preheating_mathieu_parameters, q <= 1e4, 1 <= n_bands <= 20 and the bands searched stay below
        Mathieu index 400."""
    if not (1 <= int(n_bands) <= 20):
        raise ValueError("need 1 <= n_bands <= 20")
    _, q = preheating_mathieu_parameters([0.0], m_phi, g, Phi, m_chi)
    n_hi = int(math.ceil(math.sqrt(2 * q + (m_chi / m_phi) ** 2))) + int(n_bands) + 2
    if n_hi > 400:
        raise ValueError("bands beyond Mathieu index 400 needed: q or m_chi/m_phi too large")
    cv = mathieu_characteristic_values(q, n_hi)
    out = []
    for n in range(1, n_hi + 1):
        if len(out) == int(n_bands):
            break
        lo, hi = cv["b"][n], cv["a"][n]
        k2lo = m_phi * m_phi * (lo - 2 * q) - m_chi * m_chi
        k2hi = m_phi * m_phi * (hi - 2 * q) - m_chi * m_chi
        if k2hi <= 0:
            continue
        As = np.linspace(max(lo, 2 * q + m_chi ** 2 / m_phi ** 2), hi, 43)[1:-1]
        mu = float(np.max(mathieu_floquet_exponent(As, q)["mu"])) if hi > lo else 0.0
        out.append({"n": n, "k_lo": math.sqrt(max(k2lo, 0.0)), "k_hi": math.sqrt(k2hi), "mu_max": mu,
                    "growth_rate_max": 2 * mu * m_phi})
    return out


# ================================================================ PART B: Hartree / large-N preheating solver
def _grid(kappa, kmax, n1, n2):
    k1, w1 = qp._gauss_legendre(0.0, kappa, n1)
    k2, w2 = qp._gauss_legendre(kappa, kmax, n2)
    return np.concatenate([k1, k2]), np.concatenate([w1, w2])


def hartree_preheating(m_phi: float, g: float, Phi: float, m_chi: float = 0.0, lam: float = 0.0,
                       lam_phi: float = 0.0, t_end: float = 40.0, kmax: float = None, kappa: float = None,
                       n_modes=None, steps_per_halfperiod: int = None, record_every: int = None,
                       backreaction: bool = True, k_nodes=None, k_weights=None, record_modes: bool = False,
                       check_cutoff: bool = True, _log_subtraction: bool = True,
                       _no_drift_check: bool = False) -> dict:
    """Self-consistent mean-field (Hartree / leading large-N) evolution of a homogeneous condensate phi0(t) and the
    chi modes it produces through g^2 phi^2 chi^2/2 (and a chi self-coupling lam), in Minkowski space.

        chi_k'' + (k^2 + m_chi^2 + g^2 phi0^2 + lam <chi^2>_ren) chi_k = 0,
        phi0'' + m_phi^2 phi0 + lam_phi phi0^3 + g^2 <chi^2>_ren phi0 = 0,
    <chi^2>_ren with the adiabatic second-order subtraction at scale kappa (module docstring, PART B); the run
    conserves the equivalent bare Hamiltonian exactly up to the O(dt^4) splitting error. Start: phi0 = Phi at rest,
    chi in the adiabatic vacuum of M^2(0) (gap equation if lam != 0). Grid: Gauss-Legendre with n_modes = (n1, n2)
    nodes on [0, kappa] and [kappa, kmax] (defaults kappa = m_phi, kmax = max(8 m_phi, 3 sqrt(g Phi m_phi), 4 M0) + 2 m_chi
    with M0 = sqrt(m_chi^2 + g^2 Phi^2), n_modes = (128, min(2048, max(128, 8 kmax/m_phi))); check convergence by
    doubling them; 'chi2_tail_estimate' = 3 max(M^2)^2/(64 pi^2 kmax^2) is the leading UV part of <chi^2>_ren that
    the grid misses), or your own k_nodes with dk weights k_weights. Time step pi/(m_phi steps_per_halfperiod) (default
    max(64, 20 g Phi/m_phi, pi Omega_max/m_phi), Omega_max = highest mode frequency; refused if dt g Phi > 1 or
    dt Omega_max > 2: step-size resonances of the splitting); records every record_every steps (default
    steps_per_halfperiod/4).
    backreaction=False freezes the chi -> phi0 force (phi0 = Phi cos m_phi t if lam_phi = 0: the Mathieu problem).
    Quantity: dict of arrays over record times 't' (1/energy): 'phi0', 'dphi0' (condensate, energy and energy^2),
        'M2' (chi effective mass^2), 'chi2_ren' (<chi^2>_ren, in-in, energy^2), 'n_chi' (mean number of chi PARTICLES
        per unit volume in the instantaneous adiabatic basis, energy^3; pairs = n_chi/2 for this real field),
        'rho_chi' (energy density of those quasi-particles, int w_k n_k, energy^4), 'rho_phi' (condensate energy
        density with renormalized parameters, energy^4), 'adiabaticity' (max_k |dw_k/dt|/w_k^2: n_k is a transient,
        basis-dependent number where this is not small), 'energy_drift' (change of the conserved bare energy
        relative to max(rho_phi(0), 'energy_roundoff_floor'), the rounding scale of the vacuum terms); final 'n_k' (per-mode in-in occupation, particles in mode k) on 'k' with
        quadrature weights 'W' (d^3k/(2pi)^3 = W); 'wronskian_error' (max |chi chi*' - chi* chi' - i|/(1 + 2 n_k)),
        'energy_drift_max', 'chi2_tail_estimate' (energy^2), 'edge_excitation' (max n_k for k > 0.8 kmax), 'bare',
        'Q', 'L'. n_chi, rho_chi, chi2_ren, n_k are per chi component (ONE chi field acts on phi0: N = 1).
        chi2_ren(0) != 0 even with no particles: it is the kappa-dependent vacuum (Coleman-Weinberg) part, so the
        condensate's motion includes the one-loop effective potential and departs from Phi cos(m_phi t) while
        n_chi ~ 0; m_phi and lam_phi are the parameters at scale kappa (not the oscillation frequency); only n_chi
        (and rho_chi) count produced particles.
        Mean field OMITS rescattering, delta-phi production and thermalization.
    Valid when: early stage of preheating (before rescattering matters), Minkowski space; m_phi > 0, g, Phi, m_chi,
        lam, lam_phi >= 0; lam L < 1 (Landau pole); M^2(0) > 0; the grid (automatic or k_nodes) resolves the
        resonance bands and kmax = max(k) lies beyond them (refused if modes with k > 0.8 kmax get excited, n_k >
        max(0.05, 1e-3 max n_k); check_cutoff=False skips this, for probe grids of decoupled modes, backreaction=False
        and lam = 0, where each n_k is exact on its own but n_chi, chi2_ren are grid sums); refused if the energy
        drifts by > 1e-4 (relative, as 'energy_drift')."""
    m_phi, g, Phi = _pos(m_phi, "m_phi"), _nonneg(g, "g"), _nonneg(Phi, "Phi")
    m_chi, lam, lam_phi = _nonneg(m_chi, "m_chi"), _nonneg(lam, "lam"), _nonneg(lam_phi, "lam_phi")
    t_end = _pos(t_end, "t_end")
    kappa = m_phi if kappa is None else _pos(kappa, "kappa")
    if not check_cutoff and (backreaction or lam > 0):
        raise ValueError("check_cutoff=False is only for decoupled modes (backreaction=False and lam = 0)")
    auto_grid = k_nodes is None
    if auto_grid:
        if kmax is None:
            kmax = max(8 * m_phi, 3 * math.sqrt(g * Phi * m_phi), 4 * math.hypot(m_chi, g * Phi)) + 2 * m_chi
        kmax = _pos(kmax, "kmax")
        if kmax <= kappa:
            raise ValueError("need kmax > kappa")
        if n_modes is None:
            n_modes = (128, min(2048, max(128, int(8 * kmax / m_phi))))
        n1, n2 = (int(v) for v in n_modes)
        if n1 < 8 or n2 < 8:
            raise ValueError("need at least 8 nodes in each panel")
        k, wk = _grid(kappa, kmax, n1, n2)
    else:
        k, wk = np.asarray(k_nodes, dtype=float).ravel(), np.asarray(k_weights, dtype=float).ravel()
        if k.shape != wk.shape or len(k) < 1 or np.any(~np.isfinite(k)) or np.any(k <= 0) or np.any(wk < 0):
            raise ValueError("k_nodes must be > 0 with matching non-negative k_weights")
        kmax = float(np.max(k))
    W = wk * k * k / (2 * PI * PI)
    Q = float(np.sum(W / (2 * k)))
    L = float(np.sum(np.where(k > kappa, W / (4 * k ** 3), 0.0))) if _log_subtraction else 0.0
    g2 = g * g
    if lam * L >= 1.0:
        raise ValueError(f"lam L = {lam * L:.3g} >= 1: beyond the Landau pole of the large-N model (lower kmax or lam)")
    one = 1.0 - lam * L
    lamB, g2B, mchiB2 = lam / one, g2 / one, (m_chi * m_chi - lam * Q) / one
    mphiB2 = m_phi * m_phi + g2 * (L * mchiB2 - Q)
    lamphiB = lam_phi + g2 * g2B * L

    def sren_static(M2):
        return float(np.sum(W * (0.5 / np.sqrt(k * k + M2) - 0.5 / k))) + L * M2

    M2 = m_chi * m_chi + g2 * Phi * Phi
    if lam > 0:
        for _ in range(500):
            if M2 <= -float(np.min(k)) ** 2:
                break
            new = m_chi * m_chi + g2 * Phi * Phi + lam * sren_static(M2)
            if abs(new - M2) <= 1e-15 * max(1.0, abs(M2)):
                M2 = new
                break
            M2 = new
        else:
            raise ValueError("gap equation for the initial chi mass did not converge")
    if not M2 > 0:
        raise ValueError("initial effective chi mass^2 must be > 0 (no adiabatic vacuum otherwise)")

    Mref2 = max(M2 - 0.5 * g2 * Phi * Phi, 0.0)      # oscillation average of M^2 (= M^2(0) in the vacuum)
    Om = np.sqrt(k * k + Mref2)
    om_max = float(np.max(Om))
    spp = int(steps_per_halfperiod) if steps_per_halfperiod else max(
        64, int(math.ceil(20 * g * Phi / m_phi)), int(math.ceil(PI * om_max / m_phi)))
    if spp < 8:
        raise ValueError("need steps_per_halfperiod >= 8")
    h = PI / (m_phi * spp)
    # Splitting with exact rotations has step-size resonances (Omega_k dt near multiples of pi) once the kicks are
    # not small: require dt g Phi <= 1 and dt Omega_max <= 2 (the default gives <= pi/20 and <= 1).
    if h * g * Phi > 1.0 or h * om_max > 2.0:
        need = int(math.ceil(max(PI * g * Phi, 0.5 * PI * om_max) / m_phi))
        raise ValueError(f"time step too large (dt g Phi = {h * g * Phi:.3g}, dt Omega_max = {h * om_max:.3g}): "
                         f"use steps_per_halfperiod >= {need}")
    nsteps = int(round(t_end / h))
    if nsteps < 1:
        raise ValueError("t_end shorter than one step")
    rec = int(record_every) if record_every else max(1, spp // 4)
    w0 = np.sqrt(k * k + M2)
    chi = 1 / np.sqrt(2 * w0) + 0j
    dchi = -1j * w0 * chi
    phi, pi0 = Phi, 0.0
    rot = {}
    for y in (_Y1, _Y0):
        hh = y * h
        rot[y] = (np.cos(Om * hh), hh * np.sinc(Om * hh / PI), -Om * np.sin(Om * hh),
                  math.cos(m_phi * hh), math.sin(m_phi * hh) / m_phi, -m_phi * math.sin(m_phi * hh))

    def S_B(c):
        return float(np.sum(W * (c.real * c.real + c.imag * c.imag)))

    def energy(ph, pp, c, dc):
        sb = S_B(c)
        kin = 0.5 * pp * pp + 0.5 * float(np.sum(W * (np.abs(dc) ** 2 + k * k * np.abs(c) ** 2)))
        return kin + (mphiB2 * ph * ph / 2 + lamphiB * ph ** 4 / 4 + mchiB2 * sb / 2 + g2B * ph * ph * sb / 2
                      + lamB * sb * sb / 4)

    def kick(ph, pp, c, dc, tau):
        sb = S_B(c)
        m2 = mchiB2 + g2B * ph * ph + lamB * sb
        sr = sb - Q + L * m2
        force = lam_phi * ph ** 3 + (g2 * sr * ph if backreaction else 0.0)
        return pp - tau * force, dc - tau * (m2 - Mref2) * c

    def rotate(ph, pp, c, dc, y):
        cc, ss, ms, cp, sp, msp = rot[y]
        return cp * ph + sp * pp, msp * ph + cp * pp, cc * c + ss * dc, ms * c + cc * dc

    def energy_terms_abs(ph, pp, c, dc):
        sb = S_B(c)
        return (0.5 * pp * pp + 0.5 * float(np.sum(W * (np.abs(dc) ** 2 + k * k * np.abs(c) ** 2)))
                + abs(mphiB2) * ph * ph / 2 + abs(lamphiB) * ph ** 4 / 4 + abs(mchiB2) * sb / 2
                + g2B * ph * ph * sb / 2 + lamB * sb * sb / 4)

    rho_phi0 = 0.5 * m_phi ** 2 * Phi ** 2 + 0.25 * lam_phi * Phi ** 4
    # The conserved bare energy contains vacuum chi terms of order Q ~ kmax^4 that cancel in differences; their
    # rounding (eps x sum of the absolute terms per evaluation, accumulating over the steps) is a floor below which
    # a drift says nothing about the step size. Normalize by max(rho_phi(0), that floor); the refusal threshold
    # (1e-4) is unchanged. Floor: 1e6 x eps x sum|terms| x sqrt(steps), so the refusal needs an absolute drift above
    # 100 eps sum|terms| sqrt(steps); pure roundoff (Phi = 1e-8 .. 1e-6, 64..800 steps per half period, lam = 0 and
    # 0.5) measured <= 12 eps sum|terms| sqrt(steps). For the default examples the floor is ~1e-8 of rho_phi(0).
    E_abs = energy_terms_abs(phi, pi0, chi, dchi)
    e_round = 1e6 * np.finfo(float).eps * E_abs * math.sqrt(nsteps)
    e_scale = max(rho_phi0, e_round) if rho_phi0 > 0 else max(m_phi ** 4, e_round)
    E0 = energy(phi, pi0, chi, dchi)
    keys = ("t", "phi0", "dphi0", "M2", "chi2_ren", "n_chi", "rho_chi", "rho_phi", "adiabaticity", "energy_drift")
    out = {key: [] for key in keys}
    nk_rec = []

    def record(t):
        sb = S_B(chi)
        m2 = mchiB2 + g2B * phi * phi + lamB * sb
        wk2 = k * k + m2
        good = wk2 > 0
        om = np.sqrt(np.where(good, wk2, 1.0))
        nk = np.where(good, np.abs(om * chi - 1j * dchi) ** 2 / (2 * om), np.nan)
        dm2 = 2 * g2B * phi * pi0 + lamB * float(np.sum(W * 2 * np.real(np.conj(chi) * dchi)))
        out["t"].append(t)
        out["phi0"].append(phi)
        out["dphi0"].append(pi0)
        out["M2"].append(m2)
        out["chi2_ren"].append(sb - Q + L * m2)
        out["n_chi"].append(float(np.sum(W * nk)))
        out["rho_chi"].append(float(np.sum(W * om * nk)))
        out["rho_phi"].append(0.5 * pi0 * pi0 + 0.5 * m_phi ** 2 * phi * phi + 0.25 * lam_phi * phi ** 4)
        out["adiabaticity"].append(abs(dm2) / (2 * float(np.min(om[good])) ** 3) if np.any(good) else np.inf)
        out["energy_drift"].append((energy(phi, pi0, chi, dchi) - E0) / e_scale)
        if record_modes:
            nk_rec.append(nk)
        return nk

    nk = record(0.0)
    try:
        with np.errstate(over="raise", invalid="raise"):
            for j in range(nsteps):
                pi0, dchi = kick(phi, pi0, chi, dchi, 0.5 * _Y1 * h)
                phi, pi0, chi, dchi = rotate(phi, pi0, chi, dchi, _Y1)
                pi0, dchi = kick(phi, pi0, chi, dchi, 0.5 * (_Y1 + _Y0) * h)
                phi, pi0, chi, dchi = rotate(phi, pi0, chi, dchi, _Y0)
                pi0, dchi = kick(phi, pi0, chi, dchi, 0.5 * (_Y1 + _Y0) * h)
                phi, pi0, chi, dchi = rotate(phi, pi0, chi, dchi, _Y1)
                pi0, dchi = kick(phi, pi0, chi, dchi, 0.5 * _Y1 * h)
                if (j + 1) % rec == 0 or j + 1 == nsteps:
                    nk = record((j + 1) * h)
    except (OverflowError, FloatingPointError) as exc:
        raise ValueError(f"the run overflowed ({exc}): step too large or runaway instability; "
                         "raise steps_per_halfperiod") from None
    res = {key: np.asarray(v) for key, v in out.items()}
    drift = float(np.max(np.abs(res["energy_drift"])))
    if backreaction and drift > 1e-4 and not _no_drift_check:
        raise ValueError(f"energy drifted by {drift:.2g} relative to max(rho_phi(0), roundoff floor {e_round:.2g}): "
                         "step too large, raise steps_per_halfperiod")
    # Cutoff check on EVERY grid (automatic or k_nodes): the top 20% of the k range must stay unexcited.
    edge = nk[k > 0.8 * kmax]
    edge_exc = float(np.nanmax(edge)) if edge.size and np.any(np.isfinite(edge)) else 0.0
    nmax = float(np.nanmax(nk)) if np.any(np.isfinite(nk)) else 0.0
    if check_cutoff and edge_exc > max(0.05, 1e-3 * nmax):
        raise ValueError(f"modes near the cutoff are excited (n_k up to {edge_exc:.3g} for k > 0.8 kmax = "
                         f"{0.8 * kmax:.3g}): raise kmax{'' if auto_grid else ' (extend k_nodes beyond the bands)'}")
    wr = float(np.max(np.abs(chi * np.conj(dchi) - np.conj(chi) * dchi - 1j) / (1 + 2 * np.abs(np.nan_to_num(nk)))))
    res["chi2_tail_estimate"] = 3 * float(np.max(np.abs(res["M2"]))) ** 2 / (64 * PI * PI * kmax * kmax)
    res.update({"k": k, "W": W, "n_k": nk, "edge_excitation": edge_exc, "wronskian_error": wr,
                "energy_drift_max": drift, "energy_scale": e_scale, "energy_roundoff_floor": e_round, "Q": Q, "L": L,
                "q": g2 * Phi * Phi / (4 * m_phi * m_phi), "dt": h, "steps": nsteps,
                "bare": {"m_phi2": mphiB2, "lam_phi": lamphiB, "m_chi2": mchiB2, "g2": g2B, "lam": lamB}})
    if record_modes:
        res["n_k_records"] = np.asarray(nk_rec)
    return res


# ---------------------------------------------------------------- self-test
def _dlmf_series(q):
    """DLMF 28.6.2-28.6.5, truncated at q^8 (as printed there)."""
    a1 = (1 + q - q ** 2 / 8 - q ** 3 / 64 - q ** 4 / 1536 + 11 * q ** 5 / 36864 + 49 * q ** 6 / 589824
          + 55 * q ** 7 / 9437184 - 83 * q ** 8 / 35389440)
    b1 = (1 - q - q ** 2 / 8 + q ** 3 / 64 - q ** 4 / 1536 - 11 * q ** 5 / 36864 + 49 * q ** 6 / 589824
          - 55 * q ** 7 / 9437184 - 83 * q ** 8 / 35389440)
    a2 = 4 + 5 * q ** 2 / 12 - 763 * q ** 4 / 13824 + 1002401 * q ** 6 / 79626240 - 1669068401 * q ** 8 / 458647142400
    b2 = 4 - q ** 2 / 12 + 5 * q ** 4 / 13824 - 289 * q ** 6 / 79626240 + 21391 * q ** 8 / 458647142400
    return a1, b1, a2, b2


def selftest(verbose: bool = True) -> bool:
    """Compare with closed forms, published equations and independent numerical methods. True if all pass."""
    results = []

    def check(name, got, want, tol, rel=False):
        err = abs(got - want) / (abs(want) if rel and want != 0 else 1.0)
        ok = bool(err <= tol)
        results.append(ok)
        if verbose:
            print(f"{'PASS' if ok else 'FAIL'}  {name}: {got:.10g} (expected {want:.10g}, {'rel' if rel else 'abs'} tol {tol:g})")

    # ---- A1. Regulated circle integral: numerical double sum (general-loop code) vs the exact closed form.
    #      Closed form from int_0^2pi cos(phi) dphi/(A - B cos phi) = (2pi/B)(A/sqrt(A^2 - B^2) - 1) with
    #      A = 2 + eps^2, B = 2. Tolerance 1e-12: the trapezoid is spectrally accurate at a >= 5 h (measured 4e-16).
    pts = circle_instanton(1.0, 1.0, 1024)                        # R = m/eE = 1
    av = np.array([0.24, 0.16, 0.08, 0.04])
    num = worldline_exchange_action(pts, av)["V"]
    check("circle, Polyakov-regulated exchange action: double sum = closed form (max abs over a/R = 0.04..0.24)",
          float(np.max(np.abs(num - circle_exchange_action_closed(av)))), 0.0, 1e-12)

    # ---- A2. a -> 0: the finite photon-exchange action of the circular instanton is -e^2/4 (AAM).
    #      Gould & Rajantie 2017 (arXiv:1704.04801) p. 8, eq. 41, quoted: "VPolyakov[x; 0] := 1 8π2 ∫ 1 0 ∫ 1 0
    #      dτdτ′ ˙xµ(τ) ˙xµ(τ′) (x(τ)−x(τ′))2 +a2 − 1 8π2 π a ∫ 1 0 √ ˙x2(τ)dτ. (41) The second term in (41),
    #      proportional to the length of the worldline, is a counterterm which absorbs the short distance divergence
    #      of the ﬁrst term." [PDF extraction flattens the fractions; reading: (1/8pi^2) int int xdot.xdot'/((x-x')^2
    #      + a^2) - (1/8pi^2)(pi/a) int |xdot|.] p. 10: "The resulting action is ˜S(κ, 0) =π− κ 4. (48) This result was
    #      ﬁrst derived in [35, 48]." and p. 11: "Forn = 0, the integral is−κ/4 after regularisation". With
    #      eps = gE/m^2, kappa = g^3 E/m^2 (their p. 5) the exponent S/eps = pi m^2/(gE) - g^2/4: V0 = -1/4.
    #      Tolerance 1e-6: Richardson from a/R = 0.24..0.04 leaves O(a^4) (measured 1.1e-7).
    w = worldline_coulomb_action(pts, av)
    check("circle instanton: a -> 0 exchange action / e^2 (Polyakov) = -1/4 [G&R eq. 48]", w["V0"], -0.25, 1e-6)
    #      Same limit in a different regularization (their eq. 42: "VR[x; 0] := 1 8π2 ∫ 1 0 ∫ 1 0 dτdτ′ ˙xµ(τ) ˙xµ(τ′)
    #      (x(τ)−x(τ′))2 +a2 − 1 8π2 √π a2 ∫ 1 0 ∫ 1 0 dτdτ′ ˙xµ(τ) ˙xµ(τ′)e−(x(τ)−x(τ′))2/a2 . (42) Equations (41) and
    #      (42) agree asa→ 0"): the finite part is scheme independent. Tolerance 1e-6 (measured 3.3e-7).
    wg = worldline_coulomb_action(pts, av, scheme="gaussian")
    check("circle instanton: same limit with the Gaussian counterterm [G&R eq. 42]", wg["V0"], -0.25, 1e-6)
    #      Consistency (not an independent reference): radius 3 and a non-uniform parametrization give the same V0
    #      (scale and reparametrization invariance of the renormalized action).
    th = 2 * PI * np.arange(1024) / 1024 + 0.3 * np.sin(2 * PI * np.arange(1024) / 1024)
    ww = worldline_coulomb_action(3.0 * np.stack([np.cos(th), np.sin(th)], 1), 3.0 * av)
    check("same, R = 3 and non-uniform parametrization (invariances)", ww["V0"], -0.25, 1e-6)

    # ---- A3. The rate. Dunne 2004 (hep-th/0406216) p. 50: "Aﬄeck et al [123] who showed that in the weak ﬁeld
    #      limit, the dominant result of all higher loop corrections to the leading one-loop pair production rate
    #      (1.10) is a multiplicative factor of ee2/4 =eαπ ≈ 1 +απ +..." [reading: e^{e^2/4} = e^{alpha pi}]. The
    #      numerical worldline action must reproduce that factor: exp(-e^2 V0) with e^2 = 4 pi alpha.
    #      Tolerance 1e-7: the 1e-6 tolerance on V0 times e^2 = 0.092 (measured 1e-8).
    r = schwinger_radiative_rate(1.0, 0.1)
    check("rate factor all_orders/one_loop = exp(-e^2 V0) from the numerical worldline action",
          r["all_orders"] / r["one_loop"], math.exp(-4 * PI * ALPHA_FS * w["V0"]), 1e-7, rel=True)
    #      kappa -> 0 limit reduces to Schwinger's n = 1 term, computed by qft_production's mpmath closed forms
    #      (Gould & Rajantie eq. 49: "Γ≈ (2s + 1)m4ϵ2 8π3 e− 1 ϵ (π−κ 4 ), (49) where s is the spin of the charged
    #      particle. At κ = 0 this reduces to Schwinger’s result"). Tolerance 1e-12 (same formula, double precision).
    for fermion in (True, False):
        c = qp.schwinger_closed_forms(1.0, 0.1, fermion)
        check(f"{'spinor' if fermion else 'scalar'}: one_loop = qft_production pair rate (n = 1 term), 2s+1 = "
              f"{2 if fermion else 1}", schwinger_radiative_rate(1.0, 0.1, fermion=fermion)["one_loop"],
              c["pair_rate"], 1e-12, rel=True)
    #      Two loops, spinor. Dunne eq. 4.16-4.17, quoted: "Im ( L(1) sp + L(2) sp ) =e2E2 8π3 ∞∑ k=1 1 k2 +απ − ck√ eE
    #      m2 + 1 +O (√ eE m2 ) e− m2πk eE (4.16)" with "c1 = 0" [extraction drops the brackets; reading:
    #      (e^2E^2/8pi^3) sum_k [1/k^2 + alpha pi (-c_k/sqrt(eE/m^2) + 1 + O(sqrt(eE/m^2)))] exp(-m^2 pi k/eE)]. The
    #      k = 1 term, doubled (decay rate = 2 Im L), written out independently here. Tolerance 1e-12 (transcription).
    beta = 0.1
    ref2 = 2 * beta ** 2 / (8 * PI ** 3) * (1 + ALPHA_FS * PI) * math.exp(-PI / beta)
    check("spinor two_loop = 2 x [Dunne eq. 4.16, k = 1, c_1 = 0]", r["two_loop"], ref2, 1e-12, rel=True)
    #      Lebedev-Ritus field-dependent mass, Dunne eq. 4.19: "m∗(k,E ) = m + 1 2αkc k √ eE − 1 2αkeE m" [k = 1,
    #      c_1 = 0: m* = m - alpha eE/(2m)]; exp(-pi m*^2/eE)/exp(-pi m^2/eE) = exp(pi alpha - pi alpha^2 beta/4): the
    #      module's all_orders/one_loop must equal it to O(alpha^2 beta). Compared as logarithms (the ratio itself is
    #      1.023, so a relative check of the ratio would be 40x weaker). Tolerance 2e-4 relative: the O(alpha^2)
    #      remainder is alpha beta/4 = 1.8e-4 relative to pi alpha at beta = 0.1.
    ls_shift = -PI * ((1 - ALPHA_FS * beta / 2) ** 2 - 1) / beta
    check("ln(all_orders/one_loop) = exponent shift of the Lebedev-Ritus mass m* (Dunne eq. 4.19)",
          math.log(r["all_orders"] / r["one_loop"]), ls_shift, 2e-4, rel=True)

    # ---- B1. Mathieu characteristic values (Fourier-matrix eigenvalues) vs the series of DLMF 28.6, quoted:
    #      "28.6.2 a 1 ⁡ ( q ) = 1 + q − 1 8 ⁢ q 2 − 1 64 ⁢ q 3 − 1 1536 ⁢ q 4 + 11 36864 ⁢ q 5 + 49 5 89824 ⁢ q 6 + 55 94
    #      37184 ⁢ q 7 − 83 353 89440 ⁢ q 8 + ⋯", "28.6.3 b 1 ⁡ ( q ) = 1 − q − 1 8 ⁢ q 2 + 1 64 ⁢ q 3 − 1 1536 ⁢ q 4 − 11
    #      36864 ⁢ q 5 + 49 5 89824 ⁢ q 6 − 55 94 37184 ⁢ q 7 − 83 353 89440 ⁢ q 8 + ⋯", "28.6.4 a 2 ⁡ ( q ) = 4 + 5 12 ⁢
    #      q 2 − 763 13824 ⁢ q 4 + 10 02401 796 26240 ⁢ q 6 − 16690 68401 45 86471 42400 ⁢ q 8 + ⋯", "28.6.5 b 2 ⁡ ( q ) =
    #      4 − 1 12 ⁢ q 2 + 5 13824 ⁢ q 4 − 289 796 26240 ⁢ q 6 + 21391 45 86471 42400 ⁢ q 8 + ⋯" (spaces inside numbers
    #      are DLMF's digit grouping). The series stop at q^8; the omitted q^10 term of a_2 is the largest
    #      (measured 1.2e-13 at q = 0.1, 1.2e-10 at q = 0.2). Tolerance 1e-12 at q = 0.1, and the a_2 residual must
    #      grow as q^10 (ratio 2^10 = 1024 from q = 0.1 to 0.2; window [800, 1300] for the q^12 admixture).
    res = []
    for q0 in (0.1, 0.2):
        cv = mathieu_characteristic_values(q0, 2)
        a1, b1, a2, b2 = _dlmf_series(q0)
        res.append((max(abs(cv["a"][1] - a1), abs(cv["b"][1] - b1), abs(cv["b"][2] - b2)), abs(cv["a"][2] - a2)))
    check("band edges a_1, b_1, a_2, b_2 at q = 0.1 vs DLMF 28.6.2-28.6.5 (max abs)", max(res[0]), 0.0, 1e-12)
    check("residual of a_2 vs its q^8-truncated series scales as q^10 (q = 0.2 vs 0.1)", res[1][1] / res[0][1],
          1024.0, 250.0)
    #      Two independent numerical methods: at the characteristic values the monodromy half-trace is exactly
    #      +-1 (periodic or antiperiodic solution), for small and large q. Tolerance 1e-9 (Floquet rtol 1e-11, eigenvalue
    #      roundoff amplified by |dDelta/dA| ~ 10 at q = 5; measured 1.1e-12).
    worst = 0.0
    for qq in (0.2, 1.0, 5.0):
        c2 = mathieu_characteristic_values(qq, 3)
        edges = np.array([c2["a"][0], c2["b"][1], c2["a"][1], c2["b"][2], c2["a"][2], c2["b"][3], c2["a"][3]])
        worst = max(worst, float(np.max(np.abs(np.abs(mathieu_floquet_exponent(edges, qq)["half_trace"]) - 1))))
    check("monodromy |tr M|/2 = 1 at the Fourier-matrix characteristic values (q = 0.2, 1, 5; 7 edges each)",
          worst, 0.0, 1e-9)
    #      KLS 1997 (hep-ph/9704452) p. 9, quoted: "One can write it as a Mathieu equation (Eq. (23)) with Ak = k2 m2 +
    #      2q, q = g2Φ 2 4m2 , z =mt. ForgΦ < mwe have a narrow resonance with q ≪ 1. ... The modes χ k with momenta
    #      corresponding to the cen- ter of the resonance at k ∼ m grow as eqz/ 2" and p. 10: "µ k ∼ q/ 2". At A = 1
    #      mu/(q/2) - 1 = O(q^2) (measured -0.117 q^2): tolerance 1e-4 at q = 0.02 and the deviation must scale as q^2.
    d1 = float(mathieu_floquet_exponent([1.0], 0.01)["mu"][0]) / 0.005 - 1
    d2 = float(mathieu_floquet_exponent([1.0], 0.02)["mu"][0]) / 0.01 - 1
    check("narrow resonance: mu(A = 1, q = 0.02)/(q/2) - 1 [KLS: mu ~ q/2]", d2, 0.0, 1e-4)
    check("...and the deviation scales as q^2 (ratio q = 0.02 vs 0.01 in [3.8, 4.2])", d2 / d1, 4.0, 0.2)
    lo, hi = mathieu_band_edges(0.2, 1)
    mus = mathieu_floquet_exponent([lo - 1e-3, 0.5 * (lo + hi), hi + 1e-3], 0.2)["mu"]
    check("mu = 0 just outside band 1, > 0 inside (q = 0.2)", float(mus[0] == 0 and mus[2] == 0 and mus[1] > 0.09), 1.0, 0)

    # ---- B2. Mean-field solver WITHOUT back-reaction vs Floquet theory (independent method: Yoshida splitting
    #      vs Magnus monodromy). KLS p. 7: "occupation numbers of quantum ﬂuctuations nk(t) ∝ exp(2µ (n) k z)".
    #      Stroboscopic n_k at t_j = j pi/m_phi; slope of ln n_k over the last 10 half-periods / (2 pi) = mu.
    #      Tolerance 1e-6 on mu: the decaying Floquet component leaves ~ n_k^-1 (n_k > 1e6 required) and the
    #      O(dt^4) step error (measured 1e-8 .. 4e-7).
    for qq, knodes, J, spp in ((0.1, [0.87, 0.90, 0.93, 1.2], 64, 64), (5.0, [0.3, 0.8, 1.5], 30, 200)):
        gg = 0.1
        PhiQ = math.sqrt(4 * qq) / gg
        rr = hartree_preheating(1.0, gg, PhiQ, t_end=J * PI, steps_per_halfperiod=spp, record_every=spp,
                                backreaction=False, k_nodes=knodes, k_weights=np.full(len(knodes), 1e-3),
                                record_modes=True)
        nkr = rr["n_k_records"]
        fl = preheating_floquet(knodes, 1.0, gg, PhiQ)["mu"]
        grow = fl > 0
        slope = (np.log(nkr[-1]) - np.log(nkr[-11])) / (10 * PI) / 2
        ok_grow = bool(np.all(nkr[-1][grow] > 1e6))
        check(f"no back-reaction, q = {qq}: growth of in-band modes = Floquet mu (max |diff|; all n_k > 1e6: {ok_grow})",
              float(np.max(np.abs(slope[grow] - fl[grow]))) + (0.0 if ok_grow else 1.0), 0.0, 1e-6)
        #  Out of band: bounded quasi-periodic n_k (transient polarization reaches 0.36 at q = 5), no growth.
        check(f"no back-reaction, q = {qq}: out-of-band modes stay bounded (max n_k < 1; in-band ones > 1e6)",
              float(np.max(nkr[:, ~grow])) if np.any(~grow) else 0.0, 0.0, 1.0)
    #      Exact solution: g = 0 leaves phi0 = Phi cos(m t) (rotated exactly) and chi in its vacuum. Tolerance 1e-12.
    r0 = hartree_preheating(1.0, 0.0, 3.0, m_chi=0.5, t_end=10.0, n_modes=(16, 16), steps_per_halfperiod=32)
    check("g = 0: phi0 = Phi cos(m_phi t) and n_k = 0 (max deviation)",
          float(np.max(np.abs(r0["phi0"] - 3.0 * np.cos(r0["t"]))) + np.max(np.abs(r0["n_k"]))), 0.0, 1e-12)

    # ---- B3. WITH back-reaction (q = 9): the bare Hamiltonian is conserved, the error is 4th order in dt, the
    #      Wronskian of every mode is exact. Tolerances: drift < 1e-6 of the condensate energy (measured 2.6e-7 at
    #      200 steps per half period), drift ratio for halved dt in [10, 22] (4th order: 16; measured 15),
    #      Wronskian relative to (1 + 2 n_k) below 1e-11 (the rounding of each exact rotation's determinant adds up
    #      linearly: ~ eps x 7600 stages = 2e-12; measured 8e-13).
    ra = hartree_preheating(1.0, 0.1, 60.0, t_end=40.0, kmax=14.0, steps_per_halfperiod=100)
    rb = hartree_preheating(1.0, 0.1, 60.0, t_end=40.0, kmax=14.0, steps_per_halfperiod=200)
    check("back-reaction (q = 9): max relative energy drift at 200 steps per half period", rb["energy_drift_max"], 0.0, 1e-6)
    check("energy error is 4th order: drift(dt)/drift(dt/2)", ra["energy_drift_max"] / rb["energy_drift_max"], 16.0, 6.0)
    check("mode Wronskians chi chi*' - chi* chi' = i preserved (relative)", rb["wronskian_error"], 0.0, 1e-11)
    check("back-reaction is real: phi0 phase shifted vs Phi cos t, chi2_ren > 0 at the end",
          float(abs(rb["phi0"][-1] - 60.0 * math.cos(rb["t"][-1])) > 10 and rb["chi2_ren"][-1] > 1), 1.0, 0)
    #      Renormalization: at fixed renormalized couplings the history <chi^2>_ren(t) converges as the cutoff doubles
    #      (max_t |difference| / max_t |<chi^2>_ren|; residual O(M^4/Lambda^2): measured 1.2% for Lambda 10 -> 20);
    #      subtracting only 1/(2k) leaves the log divergence (measured 15%). Tolerances 2.5% and > 10%.
    s = {}
    for logsub in (True, False):
        for km, n2 in ((10.0, 96), (20.0, 160)):
            s[(logsub, km)] = hartree_preheating(1.0, 0.1, 60.0, t_end=40.0, kmax=km, n_modes=(128, n2),
                                                 steps_per_halfperiod=100, _log_subtraction=logsub)["chi2_ren"]
    dev = {ls: float(np.max(np.abs(s[(ls, 20.0)] - s[(ls, 10.0)])) / np.max(np.abs(s[(ls, 20.0)]))) for ls in (True, False)}
    check("adiabatic 2nd-order subtraction: <chi^2>_ren(t) changes < 2.5% when the cutoff doubles", dev[True], 0.0, 0.025)
    check(f"...while subtracting only 1/(2k) changes it by {dev[False]:.0%} > 10% (log divergence)",
          float(dev[False] > 0.10), 1.0, 0)
    #      lam != 0 (large-N self-coupling): the vacuum (Phi = 0) is stationary only if the renormalized gap equation
    #      for M^2(0) and the bare-coupling mass M^2 = m_chiB^2 + lam_B S_B agree (tolerance 1e-12, roundoff);
    #      energy conserved with a condensate (1e-6, as above).
    rv = hartree_preheating(1.0, 0.1, 0.0, m_chi=1.0, lam=0.5, t_end=20.0, n_modes=(64, 64), kmax=10.0,
                            steps_per_halfperiod=64)
    check("lam = 0.5, Phi = 0: vacuum stays empty (max n_k) and <chi^2>_ren constant",
          float(np.max(np.abs(rv["n_k"])) + np.ptp(rv["chi2_ren"])), 0.0, 1e-12)
    rl = hartree_preheating(1.0, 0.1, 60.0, lam=0.05, t_end=40.0, kmax=14.0, steps_per_halfperiod=200)
    check("lam = 0.05 with condensate: max relative energy drift", rl["energy_drift_max"], 0.0, 1e-6)

    passed = all(results)
    if verbose:
        print(f"\n{sum(results)}/{len(results)} checks passed")
    return passed


# ---------------------------------------------------------------- convergence studies (slow)
def _convergence() -> int:
    """Regulator and grid studies for the worldline action; cutoff and step studies for the Hartree solver."""
    print("Worldline exchange action / e^2, circle (exact limit -1/4) and an ellipse (1.5, 0.7):")
    for n in (1024, 2048, 4096):
        for name, scale in (("circle", (1.0, 1.0)), ("ellipse", (1.5, 0.7))):
            th = 2 * PI * np.arange(n) / n
            pts = np.stack([scale[0] * np.cos(th), scale[1] * np.sin(th)], 1)
            for sch in ("polyakov", "gaussian"):
                try:
                    w = worldline_coulomb_action(pts, scheme=sch)
                    print(f"  n = {n:5d} {name:7s} {sch:9s}: V0 = {w['V0']:.10f} +- {w['V0_err']:.1e}")
                except ValueError as exc:
                    print(f"  n = {n:5d} {name:7s} {sch:9s}: {exc}")
    print("Hartree q = 9 (g = 0.1, Phi = 60, m_phi = 1), t = 40: <chi^2>_ren and phi0 at the end vs cutoff")
    for logsub in (True, False):
        for km, n2 in ((10.0, 96), (20.0, 160), (40.0, 256)):
            r = hartree_preheating(1.0, 0.1, 60.0, t_end=40.0, kmax=km, n_modes=(128, n2), steps_per_halfperiod=200,
                                   _log_subtraction=logsub)
            print(f"  {'adiabatic-2' if logsub else '1/(2k) only'} kmax = {km:5.1f}: chi2_ren = {r['chi2_ren'][-1]:.8f}, "
                  f"phi0 = {r['phi0'][-1]:.8f}, n_chi = {r['n_chi'][-1]:.6f}, drift {r['energy_drift_max']:.1e}")
    print("Hartree q = 9: energy drift vs steps per half period")
    for spp in (50, 100, 200, 400):
        r = hartree_preheating(1.0, 0.1, 60.0, t_end=40.0, kmax=14.0, steps_per_halfperiod=spp)
        print(f"  {spp:4d}: drift {r['energy_drift_max']:.3e}, phi0(40) = {r['phi0'][-1]:.10f}")
    return 0


# ---------------------------------------------------------------- command line
def _time_in_units(text: str, m_phi_eV: float) -> float:
    """A bare number is in units of 1/m_phi; a time with units ('1e-36 s') is converted."""
    try:
        return float(text)
    except ValueError:
        from unit_tools import Q
        return qp.time_to_inverse_eV(Q(text).expect("time").si) * m_phi_eV


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("selftest")
    rp = sub.add_parser("radiative", help="weak-field Schwinger pair rate with the exp(pi alpha) Coulomb factor")
    rp.add_argument("--m", default="0.51099895 MeV", help="physical mass, e.g. '0.511 MeV' (default: electron)")
    rp.add_argument("--E", required=True, help="field, e.g. '1e17 V/m'")
    rp.add_argument("--alpha", type=float, default=ALPHA_FS, help="fine-structure constant (default CODATA 2018)")
    rp.add_argument("--scalar", action="store_true", help="scalar QED instead of spinor QED")
    wp = sub.add_parser("worldline", help="numerical Coulomb action of the circular instanton (-> -e^2/4)")
    wp.add_argument("--n", type=int, default=2048, help="points on the loop")
    fp = sub.add_parser("floquet", help="Mathieu/Floquet growth of a chi mode in phi0 = Phi cos(m_phi t)")
    sp = sub.add_parser("preheat", help="self-consistent Hartree preheating run (back-reaction on)")
    for p in (fp, sp):
        p.add_argument("--m-phi", required=True, help="condensate mass, e.g. '1e13 GeV' (bare number = eV; sets the unit)")
        p.add_argument("--g", type=float, required=True, help="coupling g in g^2 phi^2 chi^2/2")
        p.add_argument("--Phi", required=True, help="initial amplitude of phi0 (an energy, e.g. '1e18 GeV'; bare number = "
                                                    "units of m_phi)")
        p.add_argument("--m-chi", default="0", help="chi mass (energy; bare number = units of m_phi)")
    fp.add_argument("--k", required=True, help="mode momentum (energy; bare number = units of m_phi)")
    sp.add_argument("--lam", type=float, default=0.0, help="chi self-coupling in the Hartree mass (dimensionless)")
    sp.add_argument("--t-end", default="40", help="duration: bare number = units of 1/m_phi, or e.g. '1e-35 s'")
    sp.add_argument("--kmax", default=None, help="momentum cutoff (energy; bare number = units of m_phi)")
    sp.add_argument("--no-backreaction", action="store_true")
    sub.add_parser("convergence", help="slow studies: regulator, cutoff and step dependence")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "selftest":
            return 0 if selftest() else 1
        if args.cmd == "convergence":
            return _convergence()
        if args.cmd == "worldline":
            pts = circle_instanton(1.0, 1.0, args.n)
            w = worldline_coulomb_action(pts)
            for a_, v_ in zip(w["a"], w["V_a"]):
                print(f"a/R = {a_:.4f}: V_a = {v_:.12f}  (closed form {float(circle_exchange_action_closed(a_)):.12f})")
            print(f"a -> 0: V0 = {w['V0']:.10f} +- {w['V0_err']:.1e} (AAM: -1/4); rate factor exp(-e^2 V0) = "
                  f"exp({w['factor_per_alpha']:.8f} alpha) = {math.exp(w['factor_per_alpha'] * ALPHA_FS):.8f} for QED")
            return 0
        from unit_tools import Q
        if args.cmd == "radiative":
            m = qp._energy(args.m)
            eE = qp.eE_from_field_SI(Q(args.E).expect("V/m").si)
            r = schwinger_radiative_rate(m, eE, args.alpha, fermion=not args.scalar)
            tag = "scalar" if args.scalar else "spinor"
            print(f"{tag} QED, m = {m:.6g} eV (physical mass), eE = {eE:.6g} eV^2 = {r['beta']:.4g} m^2, alpha = {args.alpha:.8g}")
            print("n = 1 term: vacuum-decay rate 2 Im L = mean pairs per volume per time (equal at this order):")
            ev4_to_si = qp.rate_density_to_SI(1.0)
            for key in ("one_loop", "two_loop", "all_orders"):
                lg = r["log10_" + key]
                if r[key] > 0 and qp.rate_density_to_SI(r[key]) > 0:
                    print(f"  {key:10s} {r[key]:.6g} eV^4 = {qp.rate_density_to_SI(r[key]):.6g} m^-3 s^-1")
                else:                     # exp(-pi m^2/eE) underflows double precision: print the logarithm
                    print(f"  {key:10s} 10^({lg:.6f}) eV^4 = 10^({lg + math.log10(ev4_to_si):.6f}) m^-3 s^-1 "
                          "(underflows double precision)")
            nxt = "n/a (scalar)" if r["next_rel"] is None else f"{r['next_rel']:+.2e}"
            print(f"Coulomb enhancement exp(pi alpha) = {r['enhancement']:.8f}; omitted: n = 2 term {r['n2_rel']:.1e}, "
                  f"next prefactor correction {nxt} (relative)")
            return 0
        m_phi = qp._energy(args.m_phi)
        Phi, m_chi = _in_mphi(args.Phi, m_phi), _in_mphi(args.m_chi, m_phi)
        if args.cmd == "floquet":
            kk = _in_mphi(args.k, m_phi)
            f = preheating_floquet([kk], 1.0, args.g, Phi, m_chi)
            rate = f["growth_rate"][0] * m_phi
            print(f"m_phi = {m_phi:.6g} eV; q = g^2 Phi^2/(4 m_phi^2) = {f['q']:.6g}; A_k = {f['A'][0]:.6g} (k = {kk:.6g} m_phi)")
            print(f"Floquet exponent mu = {f['mu'][0]:.6g} per unit m_phi t; growth rate of ln n_k = 2 mu m_phi = {rate:.6g} eV"
                  f" = {rate * E_CHARGE / HBAR:.6g} s^-1 (no back-reaction, Minkowski)")
            for b in preheating_resonance_bands(1.0, args.g, Phi, m_chi, 3):
                print(f"  band {b['n']}: {b['k_lo']:.5g} < k/m_phi < {b['k_hi']:.5g}, mu_max = {b['mu_max']:.4g}")
            return 0
        t_end = _time_in_units(args.t_end, m_phi)
        kmax = None if args.kmax is None else _in_mphi(args.kmax, m_phi)
        r = hartree_preheating(1.0, args.g, Phi, m_chi, lam=args.lam, t_end=t_end, kmax=kmax,
                               backreaction=not args.no_backreaction)
        print(f"Hartree preheating, units of m_phi = {m_phi:.6g} eV: q = {r['q']:.6g}, {len(r['k'])} modes, "
              f"{r['steps']} steps; mean field omits rescattering (early stage only)")
        print("   t m_phi       t [s]  amplitude/Phi  n_chi [m_phi^3]   n_chi [m^-3]   rho_chi/rho_phi(0)   chi2_ren [m_phi^2]")
        idx = np.unique(np.linspace(0, len(r["t"]) - 1, 11).astype(int))
        amp = np.sqrt(np.maximum(r["rho_phi"] / r["rho_phi"][0], 0.0)) if r["rho_phi"][0] > 0 else r["rho_phi"] * 0
        for i in idx:
            print(f"  {r['t'][i]:8.3f}  {qp.time_from_inverse_eV(r['t'][i] / m_phi):10.4g}  {amp[i]:12.5f}  "
                  f"{r['n_chi'][i]:14.6g}  {qp.density_to_SI(r['n_chi'][i] * m_phi ** 3):13.5g}  "
                  f"{r['rho_chi'][i] / r['rho_phi'][0]:17.6g}  {r['chi2_ren'][i]:16.6g}")
        print(f"amplitude = sqrt(rho_phi/rho_phi(0)) (condensate energy); n_chi counts chi PARTICLES in the instantaneous "
              f"adiabatic basis (pairs = n_chi/2; transient while phi0 oscillates); energy drift {r['energy_drift_max']:.1e}")
        print("chi2_ren(0) != 0 with n_chi = 0 is the kappa-dependent vacuum (Coleman-Weinberg) part: the condensate's "
              "motion includes the one-loop effective potential (m_phi, lam_phi defined at kappa = m_phi); only n_chi "
              "counts produced particles. One chi field (N = 1); quantities per component.")
    except (ValueError, KeyError) as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


def _in_mphi(text: str, m_phi_eV: float) -> float:
    """An energy in units of m_phi: a bare number is already in those units; '1e13 GeV' is converted."""
    try:
        return float(text)
    except ValueError:
        return qp._energy(text) / m_phi_eV


if __name__ == "__main__":
    sys.exit(main())
