#!/usr/bin/env python3
"""qft_inhomogeneous: pair production by a STATIC, spatially inhomogeneous electric field E(z) beyond
Born (the Klein-paradox regime), with every function saying exactly WHICH quantity it returns
(numpy + mpmath, no scipy). Companion of qft_production.py (homogeneous E(t), FRW, Born), which it
imports for its mode integrator, Schwinger closed forms, quadrature and unit helpers.

Why this tool exists
    A static field makes pairs at a constant RATE, not a number: the mean number of pairs grows like
    (time) x (transverse area). The usual mistakes are the same as for time-dependent fields (in-in
    versus in-out, vacuum-decay rate versus pair-number rate, particles versus pairs) plus two of
    its own: reading the Klein-paradox scattering coefficients of ONE mode as a number of pairs
    without the in/out construction that says which coefficient it is, and applying the same algebraic
    formula outside the Klein zone, where it is an ordinary transmission probability and nothing is
    created. Every public function has a "Quantity:" line and a "Valid when:" line and refuses
    inputs outside that range with ValueError.

Units (read this first)
    Natural units hbar = c = 1, Heaviside-Lorentz electromagnetism (e^2 = 4 pi alpha), exactly as
    qft_production.py. Pick ONE energy unit (e.g. eV, or the mass m) and give every energy, mass and
    momentum in it; lengths are then in 1/energy and fields as eE in energy^2. Rates per unit
    transverse area per unit time are in energy^3. This deviates from schemas.md's "SI in the Python
    API" on purpose (precedent: qft_production.py, page_wootters.py): SI helpers convert
    (length_to_inverse_eV, rate_per_area_to_SI, and qft_production.eE_from_field_SI), and the command
    line accepts units through unit_tools.Q ("0.511 MeV", "1.32e18 V/m", "1e-12 m").

PART A. Modes of a static step and the in/out construction (Nikishov 1970; Gavrilov & Gitman 2016)
-------------------------------------------------------------------------------------------------
    A particle of charge e in the static potential energy V(z) = e A0(z) (field eE(z) = -V'(z) along z,
    V -> V_L for z -> -inf and V -> V_R for z -> +inf, constant outside a finite window). Modes
    exp(-i omega t + i k_perp.x_perp) psi(z):
      scalar:  psi'' + [(omega - V(z))^2 - m^2 - k_perp^2] psi = 0;
      spinor:  per spin state the Dirac equation reduces EXACTLY to the 2-component system
               -i sigma_x chi' + eps_perp sigma_z chi = pi(z) chi, i.e. a' = i(pi + eps_perp) b,
               b' = i(pi - eps_perp) a, with pi(z) = omega - V(z) (kinetic energy), eps_perp^2 = m^2 + k_perp^2;
               both spin states give identical equations (an operator commuting with alpha_z,
               alpha_x k_perp and beta m labels them), so the spin sum is a factor g = 2.
    Asymptotic momenta p_L,R = sqrt(pi_L,R^2 - eps_perp^2), pi_L,R = omega - V_L,R.
    KLEIN ZONE: pi_L and pi_R of opposite sign with |pi_L|, |pi_R| >= eps_perp, i.e.
        min(V_L, V_R) + eps_perp <= omega <= max(V_L, V_R) - eps_perp.
    It exists only if the step height Delta V = |V_L - V_R| >= 2 eps_perp; NO pairs at all for
    Delta V < 2m, whatever the field strength (threshold null result). Only modes in the Klein zone
    create pairs; outside it the same scattering formula is a transmission probability (over-barrier
    scattering) or there is total reflection, and the vacuum is stable.
    In/out (wave packets far from the step): on the side where pi < 0 the states are antiparticles; the
    group velocity of exp(i s p z) is s p/pi. A pair = an outgoing particle on the pi > 0 side plus an
    outgoing antiparticle on the pi < 0 side. The scattering solution that is purely outgoing on one
    side, incident with amplitude 1/sqrt(T) on the other, gives (flux-normalised):
        bosons:   R - T = 1 (the bosonic Klein paradox, R > 1),     fermions: R + T = 1,
        mean number of PAIRS created in mode (omega, k_perp, spin) per unit time-energy cell:
            n = T  (= GG's N^cr = |g(+|-)|^-2, eq. 7.7; KLY II's N = |nu|^2, eq. 9),
        relative vacuum persistence of the mode: p_v = 1 - n (fermions), 1/(1 + n) = 1/R (bosons)
            (GG eq. 9.8: P_v = prod (1 - kappa N^cr)^kappa, kappa = +1 fermions, -1 bosons).
    n is an IN-IN expectation (mean number of pairs; for a charged field it is also the number of
    particles = number of antiparticles in that mode: NO factor 1/2, the pair members are not identical).
    In the solver: scalar, psi = e^{-i p_L z}/sqrt(2 p_L) at the left end is continued to the right end and
    written as (alpha e^{-i p_R z} + beta e^{+i p_R z})/sqrt(2 p_R); then n = 1/|beta|^2, R = |alpha|^2/|beta|^2,
    |alpha|^2 - |beta|^2 = 1 (either orientation of the step). Spinor: a unit-flux wave outgoing on the
    left, decomposed on the right into unit-flux outgoing (c_out) and incident (c_in) waves:
    n = 1/|c_in|^2, |c_in|^2 - |c_out|^2 = 1. (Unit-flux spinors: (1, s kappa) e^{i s p z}/sqrt(2|kappa|),
    kappa = p/(pi + eps_perp), current J = 2 Re(a* b) = s sign(pi).)

PART B. Exact closed forms
---------------------------
    Sauter step: V(z) = -eE0 L tanh(z/L), eE(z) = eE0 sech^2(z/L), Delta V = 2 eE0 L (a = eE0 L), Klein
    zone -a + eps_perp <= omega <= a - eps_perp. Gavrilov & Gitman 2016 (PRD 93 045002, arXiv:1506.01156)
    eqs. 9.4 and 9.6, identical to Kim, Lee & Yoon 2010 (arXiv:0910.3363) eq. 25:
      spinor (per spin):  n = sinh(pi L p_L) sinh(pi L p_R) / [sinh(pi L (a + d)) sinh(pi L (a - d))],  d = (p_L - p_R)/2
      scalar:             n = sinh(pi L p_L) sinh(pi L p_R) / [cosh^2(pi lam) + sinh^2(pi L (p_L - p_R)/2)],
                          lam = sqrt((eE0 L^2)^2 - 1/4)   (cosh^2(pi lam) -> cos^2(pi |lam|) when eE0 L^2 < 1/2).
      Note: these are the INVERSE of the time-dependent Sauter-pulse occupations (KLY II, after eq. 25), and
      the scalar n can exceed 1 (Bose enhancement); the spinor n <= 1 (Pauli).
      Wide step (eE0 L^2 >> 1), omega = 0: n -> exp(-pi eps_perp^2/eE0) (Chervyakov & Kleinert 2009 eq. 25).
    Sharp (Klein) step, the L -> 0 limit at fixed Delta V (omega measured from the mid-step potential):
      scalar n = 4 p_L p_R/(p_L - p_R)^2 (= 1/R - 1 with CK eq. 20; divergent at p_L = p_R, i.e. omega = 0),
      spinor n = 4 p_L p_R/(Delta V^2 - (p_L - p_R)^2)  (n = 1 at eps_perp = 0: Klein tunnelling).
      Scalar vacuum-decay rate per area: Chervyakov & Kleinert 2009 (arXiv:0906.1422) eq. 47, elliptic integrals.
      The scalar PAIR-NUMBER rate of the sharp step is infinite (the omega integral of 1/omega^2 diverges);
      a Sauter step of small L gives pair rate ~ (a^2 - m^2)^{5/2}/(20 pi a^3 L) (our limit of eq. 9.6) while
      its vacuum-decay rate stays finite and tends to CK eq. 47: the vacuum-decay versus pair-number trap
      at its most extreme.

PART C. Numerical scattering solver for any static profile V(z)
----------------------------------------------------------------
    Scalar: qft_production's 4th-order Magnus integrator (exact 2x2 exponential, exact for piecewise-constant
    potentials), started with e^{-i p_L z}/sqrt(2 p_L). Spinor: a 4th-order Magnus integrator for the
    off-diagonal 2-component system above (its Magnus exponent has a real square, so cosh/cos branches as for
    bosons). Steps double until the step-halving change of |beta| (|c_in|) is below rtol, starting from at least 16 steps
    across the region where V changes (else two coarse passes on a wide window can both see only the plateaus, i.e. a
    sharp step, agree, and return a wrong n as converged; a run that max_steps keeps below that floor is unresolved).
    PRECISION (unlike the time-dependent problem there is NO absolute floor): n = 1/|beta|^2 is read off the
    exponentially GROWING solution in the tunnelling region, so its error is RELATIVE,
        n_relerr = 2 delta/|beta| + (delta/|beta|)^2,  delta = max(step-halving change, roundoff
        4 eps sqrt(N) max(|alpha|, |beta|), end mismatch (eps_end/4) max(|alpha|, |beta|)),
    eps_end = |dp/dz|/p^2 at the window ends (ends with eps_end > max_eps_end, default 1e-3, are refused: the field is
    still on). Modes very close to the edge of the Klein zone (p -> 0) need ever wider windows; rates_numeric admits
    them up to eps_end = 0.5 with that mismatch in their error, and reports the WEIGHTED error of the rates (their
    contribution is small because n ~ p there).
    Tunnelling numbers far below any absolute double-precision noise (1e-50 and ln n = -1012 in the self-test) are
    resolved: the state is renormalised every 8 steps (and the growth e^r of each hyperbolic Magnus step is factored
    out analytically), the log of the scale is accumulated, and ln|beta| is returned exactly, so no exponent
    overflows; below n ~ 1e-308 the 'n' output underflows to 0.0 and 'ln_n' carries the number (the closed forms
    take log=True for the same reason). A non-finite or under-resolved coarse pass only means "double the steps".
    Precision is lost instead where |beta| is small: bosons with n >> 1 (relative error ~ delta sqrt(1 + n)).
    Results with n_relerr > flag_rel (default 1%) are flagged resolved=False (strict=True raises).
    potential_from_field builds V(z) = -int eE dz from a field profile (Gauss-Legendre per cell, cubic Hermite
    interpolation with the exact derivative -eE, error O(h^4)).

PART D. Rates per unit transverse area: pair number versus vacuum decay, from the SAME n
-----------------------------------------------------------------------------------------
    Each energy omega in the Klein zone makes pairs at the rate d omega/(2 pi) (GG eq. 9.11; CK eq. 28):
        pair-number rate  Gamma_A = g int d omega/(2 pi) int d^2k_perp/(2 pi)^2 n(omega, k_perp)
                          (mean number of PAIRS per unit time per unit transverse area, energy^3; in-in)
        vacuum-decay rate w_A     = g int ... [-ln(1 - n)] (fermions), [+ln(1 + n)] (bosons)
                          (|<0out|0in>|^2 = exp(-w_A A T); w_A = 2 Im L_eff per area; KLY II eq. 24; CK eq. 32)
        g = 2 (Dirac, spin sum), 1 (complex scalar). w_A > Gamma_A for fermions, w_A < Gamma_A for bosons;
        equal only when n << 1. Im L_eff alone is w_A/2.
    Quadrature over the Klein zone: Gauss-Legendre in u = k_perp^2 (cut where n < e^-46 of its k_perp = 0 value
    when eE_max is known) times, on each half of the zone, omega = c - (W/2) cos(pi s) (nodes cluster at the
    zone edges, where n ~ p -> 0 (GG eq. 9.9), and at the midpoint, where the sharp scalar step is singular).
    Locally-constant-field approximation (LCFA): Gamma_A -> int dz Gamma_Schwinger(eE(z)), w_A -> int dz
    w_Schwinger(eE(z)) when the field varies slowly over the tunnelling length m/eE0 in BOTH senses:
        gamma = m/(eE0 L) << 1  and  pi m^4/(4 eE0^3 L^2) << 1,  i.e.  eE0 L^2 >> max(1, (m^2/eE0)^2).
    Expanding the exact omega = 0 exponent, 2 pi L (a - sqrt(a^2 - eps^2)) = pi eps^2/eE0 + pi eps^4/(4 eE0^3 L^2) + ...,
    the relative correction is about -[(pi/4)(m^2/eE0)^2 + O(m^2/eE0) + O(1)]/(eE0 L^2), and exact/LCFA ~
    exp(-pi m^4/(4 eE0^3 L^2)) once that exponent is not small. Measured (exact/LCFA - 1) x eE0 L^2 for the Sauter
    pair rate at eE0 L^2 = 4000 (spinor; scalar): eE0 = 2 m^2: -1.32; -0.54. 1: -2.54; -1.75. 0.5: -6.14; -5.36.
    0.3: -13.4; -12.6. 0.1: -90.6; -89.8. 0.05: -326; -326 (leading weak-field term -(pi/4)(m^2/eE0)^2 = -314).
    So the O(1/(eE0 L^2)) coefficients -2.54 (spinor) and -1.75 (scalar) hold ONLY at eE0 = m^2 and grow like
    (m^2/eE0)^2 in weak fields: at eE0 = 0.1 m^2, eE0 L^2 = 100 (m L = 32) the exact rate is still 62% BELOW the
    LCFA (exact/LCFA = 0.38). For the Sauter step this is GG eq. 9.18 (pair number, Psi-function form) and
    eq. 9.19 (vacuum decay): Gamma_A = g L (eE0)^2/(2 pi)^3 e^{-x} sqrt(pi) Psi(1/2, -1; x), x = pi m^2/eE0.
    (GG print delta both as sqrt(pi) Psi(1/2, -(d-2)/2; x) and as int dt t^-1/2 (t+1)^-(d-2)/2 e^{-xt}; these differ.
    The Psi form, = int dt t^-1/2 (1+t)^-5/2 e^{-xt} in d = 4, is the LCFA and is what the exact rate approaches;
    the printed integral form is 15.7% too high at eE0 = m^2, agreeing only to leading order in eE0/m^2.)
    The LCFA misses the threshold: it is nonzero for Delta V < 2m, where the exact rate is exactly zero
    (Gies & Klingmueller 2005: for eE0 = m^2 the rate vanishes at width L = 1/m).

Assumptions and validity range
    Free charged fields in a prescribed, static, classical potential A0(z) (no magnetic field, no back-
    reaction, no screening by the produced pairs); the field is maintained for a time T much longer than
    1/(width of the Klein zone), so that T x rate is the mean number of pairs; one spatial direction of
    inhomogeneity; V constant outside the window [z0, z1] given to the solver. Not computed: where in z the
    pairs appear (the local rate is not unique), pulses E(z, t), magnetic fields, loop corrections.

Python usage
    import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
    import numpy as np, qft_inhomogeneous as qi                     # units of m
    qi.sauter_step_n_spinor([0.0, 0.5], [0.0, 0.3], 1.0, 1.0, 3.0)  # per mode, per spin (GG eq. 9.4)
    V, (z0, z1), (VL, VR) = qi.sauter_step_potential(1.0, 3.0)
    r = qi.klein_mode_spinor(V, z0, z1, [0.0, 0.5], [0.0, 0.3], 1.0)  # same numbers by ODE: r["n"], r["n_relerr"]
    qi.sauter_step_rates(1.0, 1.0, 3.0, fermion=True)               # pair-number AND vacuum-decay rate per area
    qi.lcfa_rates_per_area(lambda z: 1.0 / np.cosh(z / 3.0) ** 2, -36, 36, 1.0, True)
    Vg = qi.potential_from_field(lambda z: 1.0 * np.exp(-(z / 3.0) ** 2), -30.0, 30.0)   # any E(z)
    qi.rates_numeric(Vg, -30.0, 30.0, 1.0, fermion=False, eE_max=1.0)

Command line (from the project root)
    python3 .claude/skills/conundrum/scripts/qft_inhomogeneous.py selftest
    python3 .claude/skills/conundrum/scripts/qft_inhomogeneous.py sauter --E "1.32e18 V/m" --L "1e-12 m"     (electron default)
    python3 .claude/skills/conundrum/scripts/qft_inhomogeneous.py mode --E "1.32e18 V/m" --L "1e-12 m" --omega "0 eV" --kperp "100 keV" --scalar
    python3 .claude/skills/conundrum/scripts/qft_inhomogeneous.py profile --shape gauss --E "2.6e18 V/m" --L "5e-13 m"
    python3 .claude/skills/conundrum/scripts/qft_inhomogeneous.py convergence      (slow: step and grid studies)
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

import qft_production as qp  # noqa: E402  (mode integrator, Schwinger closed forms, quadrature, SI helpers)
from unit_tools import C, E_CHARGE, HBAR  # noqa: E402  (CODATA values shared by the toolkit)

PI = math.pi
_EPS = np.finfo(float).eps
_SQRT3 = math.sqrt(3.0)
_G1, _G2 = 0.5 - _SQRT3 / 6.0, 0.5 + _SQRT3 / 6.0     # Gauss-Legendre nodes on [0, 1]


# ---------------------------------------------------------------- SI helpers
def length_to_inverse_eV(L_m: float) -> float:
    """Convert a length in m to natural units 1/eV: L_nat = L e/(hbar c) (1/eV = 1.97327e-7 m).

    Quantity: length in 1/eV.
    Valid when: L_m is a length in metres."""
    return L_m * E_CHARGE / (HBAR * C)


def length_from_inverse_eV(L_nat: float) -> float:
    """Convert a length in 1/eV (natural units) to m: L_SI = L_nat hbar c/e.

    Quantity: length in m.
    Valid when: L_nat is a length in units of 1/eV."""
    return L_nat * HBAR * C / E_CHARGE


def rate_per_area_to_SI(r_eV3: float) -> float:
    """Convert a rate per unit area from eV^3 to m^-2 s^-1: r_SI = r (e/(hbar c))^2 (e/hbar).

    Quantity: events per unit transverse area per unit time in m^-2 s^-1 (whatever was counted: pairs, or
        the exponent rate of vacuum decay).
    Valid when: r_eV3 is a rate per area in eV^3 (natural units)."""
    return r_eV3 * (E_CHARGE / (HBAR * C)) ** 2 * (E_CHARGE / HBAR)


# ---------------------------------------------------------------- input checks and helpers
def _arr(x, name: str) -> np.ndarray:
    a = np.asarray(x, dtype=float)
    if not np.all(np.isfinite(a)):
        raise ValueError(f"{name} must be finite")
    return a


def _pos(x, name: str) -> float:
    v = float(x)
    if not (math.isfinite(v) and v > 0):
        raise ValueError(f"{name} must be finite and > 0")
    return v


def _mass(m) -> float:
    m = float(m)
    if not (math.isfinite(m) and m >= 0):
        raise ValueError("m must be finite and >= 0")
    return m


def _log_sinh(x):
    """ln sinh(x) for x > 0 without overflow (x = 0 gives -inf)."""
    x = np.asarray(x, dtype=float)
    xs = np.maximum(x, 1e-300)
    with np.errstate(divide="ignore"):
        return np.where(x > 0, xs + np.log(-np.expm1(-2.0 * xs)) - math.log(2.0), -np.inf)   # expm1: exact for small x


def _momenta(omega, k_perp, m, V_left, V_right):
    """Broadcast (omega, k_perp); kinetic energies, asymptotic momenta and the Klein-zone mask."""
    om, kp = np.broadcast_arrays(_arr(omega, "omega"), _arr(k_perp, "k_perp"))
    if np.any(kp < 0):
        raise ValueError("k_perp must be >= 0 (it is |k_perp|)")
    ep2 = m * m + kp * kp
    piL, piR = om - V_left, om - V_right
    pL2, pR2 = piL * piL - ep2, piR * piR - ep2
    inz = (piL * piR < 0) & (pL2 > 0) & (pR2 > 0)
    pL = np.sqrt(np.where(pL2 > 0, pL2, np.nan))
    pR = np.sqrt(np.where(pR2 > 0, pR2, np.nan))
    return om, kp, np.sqrt(ep2), piL, piR, pL, pR, inz


# ---------------------------------------------------------------- Part A: Klein zone
def klein_zone(k_perp, m: float, V_left: float, V_right: float) -> dict:
    """Energy interval of the Klein zone for each k_perp: min(V_L,V_R) + eps_perp <= omega <= max(V_L,V_R) - eps_perp.

    Quantity: dict with 'omega_min', 'omega_max' (energy; NaN where the zone is empty), 'nonempty' (bool)
        and 'k_perp_max' = sqrt((Delta V/2)^2 - m^2) (energy; NaN if Delta V < 2m, then no mode makes pairs).
    Valid when: m >= 0, k_perp >= 0, V_left != V_right (finite potential energies of the charge at z -> -inf, +inf)."""
    m = _mass(m)
    kp = _arr(k_perp, "k_perp")
    if np.any(kp < 0):
        raise ValueError("k_perp must be >= 0 (it is |k_perp|)")
    VL, VR = float(V_left), float(V_right)
    if not (math.isfinite(VL) and math.isfinite(VR)) or VL == VR:
        raise ValueError("need finite V_left != V_right (a potential step)")
    ep = np.sqrt(m * m + kp * kp)
    lo, hi = min(VL, VR) + ep, max(VL, VR) - ep
    ne = hi > lo
    half = 0.5 * abs(VL - VR)
    return {"omega_min": np.where(ne, lo, np.nan), "omega_max": np.where(ne, hi, np.nan), "nonempty": ne,
            "k_perp_max": math.sqrt(half * half - m * m) if half > m else float("nan")}


def asymptotic_momenta(omega, k_perp, m: float, V_left: float, V_right: float) -> dict:
    """Asymptotic kinetic energies pi = omega - V and longitudinal momenta p = sqrt(pi^2 - eps_perp^2) on both sides.

    Quantity: dict with 'pi_left', 'pi_right' (kinetic energy, energy), 'p_left', 'p_right' (|momentum| along z,
        energy; NaN where evanescent) and 'in_klein_zone' (bool: opposite-sign kinetic energies, both p real;
        only these modes create pairs).
    Valid when: m >= 0, k_perp >= 0, finite V_left, V_right (energy)."""
    m = _mass(m)
    _, _, _, piL, piR, pL, pR, inz = _momenta(omega, k_perp, m, float(V_left), float(V_right))
    return {"pi_left": piL, "pi_right": piR, "p_left": pL, "p_right": pR, "in_klein_zone": inz}


# ---------------------------------------------------------------- Part B: exact closed forms
def sauter_step_potential(eE0: float, L: float, ends: float = 15.0):
    """The Sauter step V(z) = -eE0 L tanh(z/L), i.e. eE(z) = -V'(z) = eE0 sech^2(z/L) along +z.

    Quantity: (V, (z0, z1), (V_left, V_right)): a callable z -> potential energy V(z) of the charge (energy),
        the window +-ends*L (1/energy; ends = 15 leaves 2e^-30 of the step unswitched) and the asymptotic
        values (+eE0 L, -eE0 L); step height Delta V = 2 eE0 L.
    Valid when: eE0 > 0 (energy^2), L > 0 (1/energy), ends >= 8."""
    eE0, L = _pos(eE0, "eE0"), _pos(L, "L")
    if not ends >= 8:
        raise ValueError("ends must be >= 8 (the step must be switched off at the window ends)")
    a = eE0 * L
    return (lambda z: -a * np.tanh(np.asarray(z, dtype=float) / L)), (-ends * L, ends * L), (a, -a)


def _sauter_p(omega, k_perp, m, eE0, L):
    m = _mass(m)
    eE0, L = _pos(eE0, "eE0"), _pos(L, "L")
    a = eE0 * L
    om, kp, ep, piL, piR, pL, pR, inz = _momenta(omega, k_perp, m, a, -a)
    return np.where(inz, pL, 1.0), np.where(inz, pR, 1.0), inz, a, eE0, L


def sauter_step_n_spinor(omega, k_perp, m: float, eE0: float, L: float, log: bool = False):
    """Exact spinor-QED pair number per mode for the Sauter step eE(z) = eE0 sech^2(z/L) (GG 2016 eq. 9.4).

    n = sinh(pi L p_L) sinh(pi L p_R) / [sinh(pi L (a + d)) sinh(pi L (a - d))], a = eE0 L, d = (p_L - p_R)/2,
    p_L,R = sqrt((omega -+ a)^2 - m^2 - k_perp^2); evaluated in logs.
    Quantity: per-mode, per-spin-state in-in mean number of electron-positron PAIRS created per unit time-energy
        cell (omega, k_perp) (= tunnelling probability T; 0 <= n <= 1), dimensionless; exactly 0 outside the
        Klein zone. Multiply by g = 2 for the spin sum; turn into a rate with rates_from_n. With log=True: ln n
        (-inf outside the zone), which stays exact where n itself underflows to 0.0 (n < ~1e-308).
    Valid when: static Sauter step, eE0 > 0 (energy^2), L > 0 (1/energy), m >= 0, k_perp >= 0."""
    pL, pR, inz, a, eE0, L = _sauter_p(omega, k_perp, m, eE0, L)
    d = 0.5 * (pL - pR)
    num = _log_sinh(PI * L * pL) + _log_sinh(PI * L * pR)
    den = _log_sinh(PI * L * np.maximum(a + d, 1e-300)) + _log_sinh(PI * L * np.maximum(a - d, 1e-300))
    lnn = np.where(inz, np.minimum(num - den, 0.0), -np.inf)
    return lnn if log else np.exp(lnn)


def sauter_step_n_scalar(omega, k_perp, m: float, eE0: float, L: float, log: bool = False):
    """Exact scalar-QED pair number per mode for the Sauter step eE(z) = eE0 sech^2(z/L) (GG 2016 eq. 9.6).

    n = sinh(pi L p_L) sinh(pi L p_R) / [cosh^2(pi lam) + sinh^2(pi L (p_L - p_R)/2)], lam = sqrt((eE0 L^2)^2 - 1/4)
    (cosh^2(pi lam) -> cos^2(pi |lam|) for eE0 L^2 < 1/2); identical to KLY II eq. 25 (sigma = 0). In logs.
    Quantity: per-mode in-in mean number of PAIRS (charged scalar particle + antiparticle) created per unit
        time-energy cell (omega, k_perp) (= T = R - 1, may exceed 1), dimensionless; exactly 0 outside the
        Klein zone. Complex scalar field: g = 1. With log=True: ln n (-inf outside the zone; exact where n
        underflows, n < ~1e-308).
    Valid when: static Sauter step, eE0 > 0 (energy^2), L > 0 (1/energy), m >= 0, k_perp >= 0."""
    pL, pR, inz, a, eE0, L = _sauter_p(omega, k_perp, m, eE0, L)
    num = _log_sinh(PI * L * pL) + _log_sinh(PI * L * pR)
    lam2 = (eE0 * L * L) ** 2 - 0.25
    if lam2 >= 0:
        y = PI * math.sqrt(lam2)
        lc = 2.0 * (y + math.log1p(math.exp(-2.0 * y)) - math.log(2.0))       # ln cosh^2(pi lam)
    else:
        lc = 2.0 * math.log(abs(math.cos(PI * math.sqrt(-lam2))))             # ln cos^2(pi |lam|) (> 0 for eE0 > 0)
    ls = 2.0 * _log_sinh(np.abs(0.5 * PI * L * (pL - pR)))
    lnn = np.where(inz, num - np.logaddexp(lc, ls), -np.inf)
    return lnn if log else np.exp(lnn)


def _klein_step_p(omega, k_perp, m, dV):
    m = _mass(m)
    dV = _pos(dV, "dV")
    om, kp, ep, piL, piR, pL, pR, inz = _momenta(omega, k_perp, m, 0.5 * dV, -0.5 * dV)
    return np.where(inz, pL, 1.0), np.where(inz, pR, 1.0), inz, dV


def klein_step_n_scalar(omega, k_perp, m: float, dV: float):
    """Sharp (Klein) step of height dV, scalar QED: n = 4 p_L p_R/(p_L - p_R)^2 (the L -> 0 limit of GG eq. 9.6).

    omega is measured from the mid-step potential (V_L = +dV/2, V_R = -dV/2).
    Quantity: per-mode in-in mean number of PAIRS (complex scalar), dimensionless; +inf at p_L = p_R (omega = 0):
        the ideal step's bosonic pair number is singular and its PAIR-NUMBER rate is infinite, while its
        vacuum-decay rate is finite (klein_step_decay_rate_scalar); 0 outside the Klein zone.
    Valid when: dV > 0 (energy), m >= 0, k_perp >= 0; a step much sharper than every wavelength 1/p."""
    pL, pR, inz, dV = _klein_step_p(omega, k_perp, m, dV)
    with np.errstate(divide="ignore"):
        return np.where(inz, 4.0 * pL * pR / (pL - pR) ** 2, 0.0)


def klein_step_n_spinor(omega, k_perp, m: float, dV: float):
    """Sharp (Klein) step of height dV, spinor QED: n = 4 p_L p_R/(dV^2 - (p_L - p_R)^2) (L -> 0 limit of GG eq. 9.4).

    omega is measured from the mid-step potential (V_L = +dV/2, V_R = -dV/2).
    Quantity: per-mode, per-spin-state in-in mean number of PAIRS (0 <= n <= 1; n = 1 when m = k_perp = 0,
        Klein tunnelling), dimensionless; 0 outside the Klein zone.
    Valid when: dV > 0 (energy), m >= 0, k_perp >= 0; a step much sharper than every wavelength 1/p."""
    pL, pR, inz, dV = _klein_step_p(omega, k_perp, m, dV)
    return np.where(inz, 4.0 * pL * pR / (dV * dV - (pL - pR) ** 2), 0.0)


def klein_step_decay_rate_scalar(m: float, dV: float) -> float:
    """Vacuum-decay rate per unit area of a sharp step, scalar QED: Chervyakov & Kleinert 2009 eq. 47.

    w_A = v^3/(3 pi^2) (1 + m/v)^3 { [(1 - al^2) K(al) - (1 + al^2) E(al)]/2
          + (al/3) [(1 - al)(4 + al) F(phi, 1/al) + (1 + 3 al + al^2) E(phi, 1/al)] },
    v = dV/2, al = (v - m)/(v + m), phi = arcsin(al), elliptic integrals with modulus as second argument.
    Quantity: vacuum-decay rate per unit transverse area per unit time, w_A = int d omega/(2pi) d^2k/(2pi)^2 ln(1 + n)
        (= 2 Im L_eff per area; |<0|0>|^2 = exp(-w_A A T)), energy^3. NOT a pair-number rate (that one is infinite
        for the sharp bosonic step).
    Valid when: m > 0, dV > 0 (energy), any height above threshold (evaluated in mpmath with complete elliptic
        integrals only; relative accuracy ~1e-15 from dV = 2m(1 + 1e-12) to 1e6 m); returns 0.0 for dV <= 2m (no Klein zone)."""
    import mpmath as mp
    m = _pos(m, "m")
    v = 0.5 * _pos(dV, "dV")
    if v <= m:
        return 0.0
    # phi = arcsin(al) puts F(phi, 1/al) and E(phi, 1/al) exactly on their branch point (k sin phi = 1), where rounding
    # of phi gives a complex value; the reciprocal-modulus identities (mpmath parameter convention, checked at 40
    # digits) remove it: F(arcsin al | 1/al^2) = al K(al^2), E(arcsin al | 1/al^2) = [E(al^2) - (1 - al^2) K(al^2)]/al.
    # Near threshold the bracket cancels to ~al^2 relative (2 log10(1/al) digits lost), so the working precision grows.
    al_f = (v - m) / (v + m)
    dps = 30 + int(3 * max(0.0, -math.log10(al_f)))
    with mp.workdps(dps):
        vv, mm = mp.mpf(v), mp.mpf(m)
        al = (vv - mm) / (vv + mm)
        K, E = mp.ellipk(al * al), mp.ellipe(al * al)                  # mpmath takes the parameter m = modulus^2
        F1, E1 = al * K, (E - (1 - al * al) * K) / al
        br = (0.5 * ((1 - al * al) * K - (1 + al * al) * E)
              + al / 3 * ((1 - al) * (4 + al) * F1 + (1 + 3 * al + al * al) * E1))
        return float(mp.re(vv ** 3 / (3 * mp.pi ** 2) * (1 + mm / vv) ** 3 * br))


# ---------------------------------------------------------------- Part C: numerical scattering solver
def potential_from_field(eE_of_z, z0: float, z1: float, n: int = 4001):
    """Potential energy V(z) = -int_{z0}^{z} eE(z') dz' from a field profile, for the numerical solvers.

    Cell integrals by 6-point Gauss-Legendre on a uniform grid of n nodes, cubic Hermite interpolation with
    the exact slope V' = -eE at the nodes (error O(h^4)); V is held constant outside [z0, z1].
    Quantity: a callable z -> V(z) (energy; V(z0) = 0, so V_L = 0 and V_R = -int eE dz); eE in energy^2,
        z in 1/energy. eE > 0 accelerates the charge towards +z.
    Valid when: eE_of_z is vectorised and smooth on [z0, z1] and negligible at both ends (the solvers check
        this through the adiabaticity of the ends); z0 < z1 finite; n >= 101."""
    z0, z1 = float(z0), float(z1)
    if not (math.isfinite(z0) and math.isfinite(z1)) or z1 <= z0:
        raise ValueError("need finite z0 < z1")
    if n < 101:
        raise ValueError("need n >= 101 grid nodes")
    z = np.linspace(z0, z1, int(n))
    h = z[1] - z[0]
    x, w = np.polynomial.legendre.leggauss(6)
    pts = 0.5 * (z[:-1] + z[1:])[:, None] + 0.5 * h * x[None, :]
    F = np.asarray(eE_of_z(pts.ravel()), dtype=float).reshape(pts.shape)
    dVn = -np.asarray(eE_of_z(z), dtype=float)
    if not (np.all(np.isfinite(F)) and np.all(np.isfinite(dVn))):
        raise ValueError("eE(z) must be finite on [z0, z1]")
    Vn = np.concatenate([[0.0], -np.cumsum(0.5 * h * (F @ w))])
    N = int(n)

    def V(zz):
        za = np.asarray(zz, dtype=float)
        zc = np.clip(za, z0, z1)
        i = np.minimum(((zc - z0) / h).astype(int), N - 2)
        t = (zc - z[i]) / h
        out = ((1 + 2 * t) * (1 - t) ** 2 * Vn[i] + t * (1 - t) ** 2 * h * dVn[i]
               + t * t * (3 - 2 * t) * Vn[i + 1] + t * t * (t - 1) * h * dVn[i + 1])
        return float(out) if out.ndim == 0 else out
    return V


def _solver_setup(V, z0, z1, omega, k_perp, m, steps, max_steps, max_eps_end):
    if not 0 < max_eps_end <= 0.5:
        raise ValueError("need 0 < max_eps_end <= 0.5 (beyond that the plane-wave ends are meaningless)")
    z0, z1 = float(z0), float(z1)
    if not (math.isfinite(z0) and math.isfinite(z1)) or z1 <= z0:
        raise ValueError("need finite z0 < z1")
    if steps < 2 or max_steps < steps:
        raise ValueError("need 2 <= steps <= max_steps")
    m = _mass(m)
    VL, VR = float(np.asarray(V(z0))), float(np.asarray(V(z1)))
    if not (math.isfinite(VL) and math.isfinite(VR)):
        raise ValueError("V(z) must be finite at the window ends")
    om, kp, ep, piL, piR, pL, pR, inz = _momenta(omega, k_perp, m, VL, VR)
    return z0, z1, m, VL, VR, om, kp, ep, piL, piR, pL, pR, inz


def _min_steps(V, z0, z1):
    """Smallest step count that puts >= 16 Magnus steps across the region where V(z) changes (0.5% to 99.5% of its
    cumulative variation, scanned on 2001 points, taken >= 1/200 of the window). Without it a coarse pair of passes
    on a window much wider than the field can sample V only on its plateaus, see an effectively sharp step at both
    resolutions, and 'converge' to the wrong n."""
    zs = np.linspace(z0, z1, 2001)
    c = np.concatenate([[0.0], np.cumsum(np.abs(np.diff(np.asarray(V(zs), dtype=float))))])
    if not c[-1] > 0:
        return 2
    i0, i1 = np.searchsorted(c, 0.005 * c[-1]), np.searchsorted(c, 0.995 * c[-1])
    w = max(zs[min(i1, 2000)] - zs[max(i0 - 1, 0)], (z1 - z0) / 200.0)
    return int(math.ceil(16.0 * (z1 - z0) / w))


def _start_steps(steps, n_min, max_steps):
    return min(max(int(steps), n_min), max(int(steps), max_steps // 2))


def _end_adiabaticity(w2, z0, z1):
    scale = z1 - z0
    return np.maximum(qp._adiabaticity(w2, z0, scale), qp._adiabaticity(w2, z1, scale))


def _finish(shape, inz, n_in, lnn_in, rel_in, extra_in, eps_in, steps, converged, flag_rel, strict, what):
    n = np.zeros(inz.shape)
    lnn = np.full(inz.shape, -np.inf)
    rel = np.zeros(inz.shape)
    n[inz], lnn[inz], rel[inz] = n_in, lnn_in, rel_in
    resolved = rel <= flag_rel
    if strict and not np.all(resolved):
        raise ValueError(f"{int(np.sum(~resolved))} mode(s) have relative error of {what} above {flag_rel:g} "
                         f"(max {rel.max():.3g}); refine (steps/rtol) or widen the window")
    out = {"n": n.reshape(shape), "ln_n": lnn.reshape(shape), "n_relerr": rel.reshape(shape),
           "resolved": resolved.reshape(shape), "in_klein_zone": inz.reshape(shape), "steps": steps,
           "converged": converged}
    eps = np.zeros(inz.shape)
    eps[inz] = eps_in
    out["eps_end"] = eps.reshape(shape)
    for k, v in extra_in.items():
        full = np.full(inz.shape, np.nan)
        full[inz] = v
        out[k] = full.reshape(shape)
    return out


def _error_model(err_rel, ln_other_over_amp, eps_end, nsteps, _unused=0.0):
    """Relative error of n = 1/|amp|^2 from the relative step-halving change of |amp|, roundoff 4 eps sqrt(N) and the
    end mismatch eps_end/4, the last two relative to max(|amp|, |other|) (Part C), all as ratios to |amp|."""
    with np.errstate(over="ignore"):
        big = np.exp(np.maximum(ln_other_over_amp, 0.0))                     # max(|amp|, |other|)/|amp|
    x = np.maximum.reduce([err_rel, 4.0 * _EPS * math.sqrt(nsteps) * big, 0.25 * eps_end * big])
    return np.where(x < 1, 2 * x + x * x, np.inf)


def klein_mode_scalar(V, z0: float, z1: float, omega, k_perp, m: float, steps: int = 400, rtol: float = 1e-7,
                      max_steps: int = 2 ** 17, strict: bool = False, flag_rel: float = 1e-2,
                      max_eps_end: float = 1e-3) -> dict:
    """Scalar-QED pair number per mode for ANY static potential step V(z), by integrating the wave equation in z.

    psi'' + [(omega - V(z))^2 - m^2 - k_perp^2] psi = 0 with qft_production's 4th-order Magnus integrator,
    started as e^{-i p_L z}/sqrt(2 p_L) at z0 and written as (alpha e^{-i p_R z} + beta e^{i p_R z})/sqrt(2 p_R)
    at z1: n = 1/|beta|^2 (= transmission T), R = |alpha|^2/|beta|^2 = 1 + n (Klein paradox).
    Quantity: dict with 'n' (per-mode in-in mean number of PAIRS created per unit time-energy cell, complex scalar,
        dimensionless; exactly 0 for modes outside the Klein zone, which are not integrated), 'ln_n', 'n_relerr'
        (relative error estimate: there is no absolute floor, see Part C), 'resolved' (n_relerr <= flag_rel),
        'reflection' R, 'flux_error' = | |alpha|^2 - |beta|^2 - 1 | / |alpha|^2 (computed in scaled form),
        'in_klein_zone', 'eps_end', 'steps' (final step count), 'converged' (True if every mode met rtol before
        max_steps). Below n ~ 1e-308 'n' underflows to 0.0 and 'ln_n' is the meaningful output.
    Valid when: V(z) is vectorised, static and constant outside [z0, z1] (end adiabaticity |dp/dz|/p^2 <=
        max_eps_end <= 0.5, default 1e-3, else ValueError); m >= 0, k_perp >= 0; any tunnelling exponent (the state
        is renormalised during the integration, so ln_n stays finite)."""
    z0, z1, m, VL, VR, om, kp, ep, piL, piR, pL, pR, inz = _solver_setup(V, z0, z1, omega, k_perp, m, steps, max_steps,
                                                                          max_eps_end)
    shape = om.shape
    inz = inz.ravel()
    if not np.any(inz):
        return _finish(shape, inz, [], [], [], {"reflection": [], "flux_error": []}, [], 0, True, flag_rel, False, "n")
    o, e2 = om.ravel()[inz], (ep * ep).ravel()[inz]
    pl, pr = pL.ravel()[inz], pR.ravel()[inz]

    def w2(z):
        return (o - V(z)) ** 2 - e2

    eps_end = _end_adiabaticity(w2, z0, z1)
    if np.any(eps_end > max_eps_end):
        raise ValueError(f"window ends are not adiabatic (|dp/dz|/p^2 up to {eps_end.max():.3g} > {max_eps_end:g}): the field "
                         "is still on at z0 or z1 (widen the window), or a mode sits at the edge of the Klein zone")

    def run(n):
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            u, v, ls = _magnus_scalar(w2, z0, z1, n, pl)
            lb = np.log(np.abs(np.sqrt(pr / 2.0) * (u - 1j * v / pr))) + ls     # ln|beta|
            la = np.log(np.abs(np.sqrt(pr / 2.0) * (u + 1j * v / pr))) + ls     # ln|alpha|
        return lb, la

    n_min = _min_steps(V, z0, z1)
    lb, la, n, converged, err = _refine(run, _start_steps(steps, n_min, max_steps), rtol, max_steps)
    rel = _error_model(err, la - lb, eps_end, n, 0.0)
    if n < n_min:                                 # max_steps kept the run below the resolution floor: no verdict
        rel, converged = np.full_like(rel, np.inf), False
    with np.errstate(over="ignore", under="ignore"):
        refl = np.exp(2.0 * (la - lb))
        flux = np.abs(1.0 - np.exp(2.0 * (lb - la)) - np.exp(-2.0 * la))         # | |a|^2 - |b|^2 - 1 |/|a|^2, scaled
        nn = np.exp(-2.0 * lb)
    extra = {"reflection": refl, "flux_error": flux}
    return _finish(shape, inz, nn, -2.0 * lb, rel, extra, eps_end, n, converged, flag_rel, strict, "n")


def _refine(run, n, rtol, max_steps):
    """Double the step count until the step-halving change of |amplitude| (from ln|amp|) is below rtol.

    run(n) -> (ln|amp|, ln|other|). A non-finite result (an under-resolved pass) counts as unconverged, never as a
    verdict on n; only if the finest allowed pass is still non-finite is ValueError raised."""
    l1, _ = run(n)
    while True:
        l2, o2 = run(2 * n)
        with np.errstate(over="ignore", invalid="ignore"):
            err = np.abs(np.expm1(l1 - l2))                                     # = | |amp_1| - |amp_2| | / |amp_2|
        err = np.where(np.isfinite(err), err, np.inf)
        finite = bool(np.all(np.isfinite(l2)) and np.all(np.isfinite(o2)))
        converged = finite and bool(np.all(err <= rtol))
        if converged or 4 * n > max_steps:
            break
        n, l1 = 2 * n, l2
    if not finite:
        raise ValueError(f"non-finite scattering amplitudes even with {2 * n} steps (max_steps = {max_steps}): "
                         "raise max_steps or narrow the window")
    return l2, o2, 2 * n, converged, err


def _scaled_exp(q, r):
    """cos/cosh(r) and sin/sinh(r)/r of a 2x2 Magnus exponent with Omega^2 = q 1 (r = sqrt|q|), with the growth e^r of
    the hyperbolic branch factored out: returns (C, S, ln_scale) with exp(Omega) = e^{ln_scale} (C 1 + S Omega)."""
    hyp = q > 0
    rr = np.maximum(r, 1e-300)
    e2 = np.exp(-2.0 * r)
    Cf = np.where(hyp, 0.5 * (1.0 + e2), np.cos(r))
    Sf = np.where(hyp, -0.5 * np.expm1(-2.0 * rr), np.sin(r)) / rr               # sinh(r) e^-r / r, sin(r)/r
    Sf = np.where(r < 1e-300, 1.0, Sf)
    return Cf, Sf, np.where(hyp, r, 0.0)


def _magnus_scalar(omega2, z0, z1, n, p_in):
    """qft_production's 4th-order Magnus propagation of (psi, psi') from e^{-i p z}/sqrt(2p) at z0, with the state
    renormalised every 8 steps and the logarithm of the scale accumulated: returns (u, v, ln_scale), so tunnelling
    exponents of any size stay finite (the plain integrator overflows beyond e^{709})."""
    h = (z1 - z0) / n
    u = np.exp(-1j * p_in * z0) / np.sqrt(2.0 * p_in)
    v = -1j * p_in * u
    lsc = np.zeros(np.shape(p_in))
    for j in range(n):
        z = z0 + j * h
        a1 = np.asarray(omega2(z + _G1 * h), dtype=float)
        a2 = np.asarray(omega2(z + _G2 * h), dtype=float)
        c = (_SQRT3 * h * h / 12.0) * (a2 - a1)
        ab = 0.5 * (a1 + a2)
        q2 = c * c - h * h * ab
        Cf, Sf, ls = _scaled_exp(q2, np.sqrt(np.abs(q2)))
        u, v = (Cf + Sf * c) * u + Sf * h * v, -Sf * h * ab * u + (Cf - Sf * c) * v
        lsc = lsc + ls
        if j % 8 != 7 and j != n - 1:
            continue                                  # renormalise every 8 steps (hyperbolic growth already factored out)
        nrm = np.maximum(np.abs(u), np.abs(v))
        nrm = np.where(nrm > 0, nrm, 1.0)
        u, v, lsc = u / nrm, v / nrm, lsc + np.log(nrm)
    return u, v, lsc


def _magnus_spinor(pi_of_z, ep, z0, z1, n, a, b):
    """Propagate a' = i(pi + ep) b, b' = i(pi - ep) a with n 4th-order Magnus steps (exact 2x2 exponential).

    Generator A = [[0, x], [y, 0]], x = i(pi + ep), y = i(pi - ep); Omega = (h/2)(A1 + A2) + (sqrt3 h^2/12)[A2, A1]
    = [[c, X], [Y, -c]] with c = (sqrt3 h^2/6) ep (pi2 - pi1) real and Omega^2 = q 1, q = c^2 - (h^2/4)((pi1+pi2)^2 - 4 ep^2) real.
    The state is renormalised every 8 steps (growth e^r of hyperbolic steps factored out analytically): returns
    (a, b, ln_scale) with the true state = e^{ln_scale} (a, b), finite for tunnelling exponents of any size."""
    h = (z1 - z0) / n
    lsc = np.zeros(np.shape(ep))
    for j in range(n):
        z = z0 + j * h
        p1, p2 = pi_of_z(z + _G1 * h), pi_of_z(z + _G2 * h)
        c = (_SQRT3 * h * h / 6.0) * ep * (p2 - p1)
        s = p1 + p2
        X = 0.5j * h * (s + 2 * ep)
        Y = 0.5j * h * (s - 2 * ep)
        q = c * c - 0.25 * h * h * (s * s - 4 * ep * ep)
        Cf, Sf, ls = _scaled_exp(q, np.sqrt(np.abs(q)))
        a, b = (Cf + Sf * c) * a + Sf * X * b, Sf * Y * a + (Cf - Sf * c) * b
        lsc = lsc + ls
        if j % 8 != 7 and j != n - 1:
            continue                                  # renormalise every 8 steps (hyperbolic growth already factored out)
        nrm = np.maximum(np.abs(a), np.abs(b))
        nrm = np.where(nrm > 0, nrm, 1.0)
        a, b, lsc = a / nrm, b / nrm, lsc + np.log(nrm)
    return a, b, lsc


def klein_mode_spinor(V, z0: float, z1: float, omega, k_perp, m: float, steps: int = 400, rtol: float = 1e-7,
                      max_steps: int = 2 ** 17, strict: bool = False, flag_rel: float = 1e-2,
                      max_eps_end: float = 1e-3) -> dict:
    """Spinor-QED pair number per mode and spin state for ANY static step V(z), by integrating the Dirac equation in z.

    Per spin state the Dirac equation is exactly a' = i(pi + eps_perp) b, b' = i(pi - eps_perp) a, pi = omega - V(z).
    A unit-flux wave outgoing on the left (e^{i s p_L z}, s = -sign(pi_L)) is integrated to z1 and decomposed into
    unit-flux outgoing (c_out) and incident (c_in) waves: n = 1/|c_in|^2 = T, R = |c_out/c_in|^2 = 1 - n.
    Quantity: dict with 'n' (per-mode, per-spin-state in-in mean number of electron-positron PAIRS per unit
        time-energy cell, 0 <= n <= 1, dimensionless; both spins give the same n, so multiply sums by g = 2; 0 for
        modes outside the Klein zone), 'ln_n', 'n_relerr', 'resolved', 'reflection' R, 'flux_error' =
        | |c_in|^2 - |c_out|^2 - 1 | / |c_in|^2 (scaled form), 'in_klein_zone', 'eps_end', 'steps' (final step count),
        'converged' (every mode met rtol before max_steps). Below n ~ 1e-308 'n' underflows to 0.0: use 'ln_n'.
    Valid when: V(z) is vectorised, static and constant outside [z0, z1] (end adiabaticity <= max_eps_end <= 0.5,
        default 1e-3, else ValueError); purely electric field along z; m >= 0, k_perp >= 0; any tunnelling exponent
        (renormalised integration)."""
    z0, z1, m, VL, VR, om, kp, ep, piL, piR, pL, pR, inz = _solver_setup(V, z0, z1, omega, k_perp, m, steps, max_steps,
                                                                          max_eps_end)
    shape = om.shape
    inz = inz.ravel()
    if not np.any(inz):
        return _finish(shape, inz, [], [], [], {"reflection": [], "flux_error": []}, [], 0, True, flag_rel, False, "n")
    o, e = om.ravel()[inz], ep.ravel()[inz]
    pl, pr = pL.ravel()[inz], pR.ravel()[inz]
    pil, pir = piL.ravel()[inz], piR.ravel()[inz]

    def w2(z):
        return (o - V(z)) ** 2 - e * e

    eps_end = _end_adiabaticity(w2, z0, z1)          # |dp/dz|/p^2 >= |d ln kappa/dz|/p: the stricter of the two
    if np.any(eps_end > max_eps_end):
        raise ValueError(f"window ends are not adiabatic (|dp/dz|/p^2 up to {eps_end.max():.3g} > {max_eps_end:g}): the field "
                         "is still on at z0 or z1 (widen the window), or a mode sits at the edge of the Klein zone")
    sL, sR = -np.sign(pil), np.sign(pir)              # left-moving on the left, right-moving on the right
    kL, kR = pl / (pil + e), pr / (pir + e)
    a0 = np.exp(1j * sL * pl * z0) / np.sqrt(2 * np.abs(kL))
    b0 = sL * kL * a0
    NR = np.sqrt(2 * np.abs(kR))

    def run(n):
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            a, b, ls = _magnus_spinor(lambda z: o - V(z), e, z0, z1, n, a0 + 0j, b0 + 0j)
            cp = NR * np.exp(-1j * pr * z1) * (a + b / kR) / 2          # coefficient of the unit-flux e^{+i p z} wave
            cm = NR * np.exp(1j * pr * z1) * (a - b / kR) / 2           # ... and of e^{-i p z}  (both / e^{ls})
            cin = np.log(np.abs(np.where(sR > 0, cm, cp))) + ls
            cout = np.log(np.abs(np.where(sR > 0, cp, cm))) + ls
        return cin, cout

    n_min = _min_steps(V, z0, z1)
    lc, lo, n, converged, err = _refine(run, _start_steps(steps, n_min, max_steps), rtol, max_steps)
    rel = _error_model(err, lo - lc, eps_end, n, 0.0)
    if n < n_min:                                 # max_steps kept the run below the resolution floor: no verdict
        rel, converged = np.full_like(rel, np.inf), False
    with np.errstate(over="ignore", under="ignore"):
        refl = np.exp(2.0 * (lo - lc))
        flux = np.abs(1.0 - refl - np.exp(-2.0 * lc))                       # | |c_in|^2 - |c_out|^2 - 1 |/|c_in|^2, scaled
        nn = np.exp(-2.0 * lc)
    extra = {"reflection": refl, "flux_error": flux}
    return _finish(shape, inz, nn, -2.0 * lc, rel, extra, eps_end, n, converged, flag_rel, strict, "n")


# ---------------------------------------------------------------- Part D: rates per unit area
def _klein_nodes(V_left, V_right, m, n_omega, n_k, eE_max=None):
    """Nodes and weights of int d omega/(2pi) int d^2k_perp/(2pi)^2 over the Klein zone (no spin factor)."""
    dV = abs(V_left - V_right)
    if dV <= 2 * m:
        return np.zeros(0), np.zeros(0), np.zeros(0)
    umax = 0.25 * dV * dV - m * m
    if eE_max is not None:
        umax = min(umax, 46.0 * float(eE_max) / PI)          # n < e^-46 x its k_perp = 0 value beyond (|E| <= E_max)
    u, wu = qp._gauss_legendre(0.0, umax, int(n_k))
    s, ws = qp._gauss_legendre(0.0, 1.0, int(n_omega))
    U, S = np.meshgrid(u, s, indexing="ij")
    ep = np.sqrt(m * m + U)
    lo, hi = min(V_left, V_right) + ep, max(V_left, V_right) - ep
    mid, H = 0.5 * (lo + hi), 0.5 * (hi - lo)
    oms, ws_all = [], []
    for sgn in (-1.0, 1.0):                                    # two halves, cos map clusters nodes at both ends of each
        c = mid + sgn * 0.5 * H
        oms.append(c - 0.5 * H * np.cos(PI * S))
        ws_all.append(np.einsum("i,j->ij", wu, ws) * 0.5 * PI * H * np.sin(PI * S) / (8 * PI * PI))
    kp = np.sqrt(np.concatenate([U, U]).ravel())
    return np.concatenate(oms).ravel(), kp, np.concatenate(ws_all).ravel()


def _rates(nk, w, fermion):
    if not np.all(np.isfinite(nk)):
        raise ValueError("pair numbers must be finite (a non-finite n, e.g. at p_L = p_R of the sharp scalar step, "
                         "is not integrable by this rule)")
    if np.any(nk < 0) or (fermion and np.any(nk > 1)):
        raise ValueError("pair numbers must satisfy n >= 0 (and n <= 1 for fermions)")
    g = 2.0 if fermion else 1.0
    pair = g * float(np.sum(w * nk))
    with np.errstate(divide="ignore"):
        dec = g * float(np.sum(w * (-np.log1p(-nk) if fermion else np.log1p(nk))))
    return {"pair_rate": pair, "decay_rate": dec, "ratio": dec / pair if pair > 0 else float("nan"),
            "im_L_eff": dec / 2, "zone_empty": len(w) == 0}


def rates_from_n(n_of_mode, V_left: float, V_right: float, m: float, fermion: bool, n_omega: int = 48, n_k: int = 48,
                 eE_max: float = None) -> dict:
    """Pair-number rate AND vacuum-decay rate per unit transverse area, both from the same per-mode n(omega, k_perp).

    Gamma_A = g int d omega/(2pi) int d^2k/(2pi)^2 n;  w_A = g int ... [-ln(1 - n)] (fermions), [ln(1 + n)] (bosons);
    Gauss-Legendre in u = k_perp^2 (n_k nodes) x the cos-mapped omega rule on each half of the zone (n_omega each).
    Quantity: dict with 'pair_rate' (mean number of PAIRS per unit time per unit transverse area, energy^3; in-in),
        'decay_rate' (vacuum-decay exponent rate per area, |<0|0>|^2 = exp(-w_A A T), = 2 Im L_eff per area,
        energy^3), 'im_L_eff' = decay_rate/2, 'ratio' = w_A/Gamma_A, 'zone_empty' (True: Delta V <= 2m, both
        rates exactly 0). g = 2 (spinor; n per spin state), 1 (complex scalar).
    Valid when: n_of_mode(omega_array, k_perp_array) returns the finite per-mode pair number (0 <= n, n <= 1 for
        fermions; a NaN or inf n raises ValueError), integrable over the zone (NOT the sharp scalar step: use
        klein_step_rates); eE_max (finite > 0, energy^2) = max |eE(z)| if given cuts k_perp^2 at 46 eE_max/pi; check
        convergence by changing n_omega, n_k."""
    m = _mass(m)
    VL, VR = float(V_left), float(V_right)
    if not (math.isfinite(VL) and math.isfinite(VR)) or VL == VR:
        raise ValueError("need finite V_left != V_right")
    if n_omega < 4 or n_k < 4:
        raise ValueError("need n_omega, n_k >= 4")
    if eE_max is not None:
        eE_max = _pos(eE_max, "eE_max")
    om, kp, w = _klein_nodes(VL, VR, m, n_omega, n_k, eE_max)
    if len(w) == 0:
        return _rates(np.zeros(0), w, fermion)
    return _rates(np.asarray(n_of_mode(om, kp), dtype=float), w, fermion)


def sauter_step_rates(m: float, eE0: float, L: float, fermion: bool, n_omega: int = 48, n_k: int = 48,
                      flag_rel: float = 1e-2, strict: bool = False) -> dict:
    """Exact pair-number and vacuum-decay rates per unit area of the Sauter step (GG eqs. 9.4/9.6 integrated).

    Quantity: as rates_from_n ('pair_rate' = mean PAIRS per unit time per unit transverse area, 'decay_rate' =
        vacuum-decay rate per area, both energy^3; spin-summed for spinors), plus 'quad_relerr' = relative change
        of the pair rate with 1.5x the nodes, 'resolved' (quad_relerr <= flag_rel; strict=True raises otherwise),
        'dV' = 2 eE0 L and 'eE0L2' = eE0 L^2 (the LCFA needs eE0 L^2 >> max(1, (m^2/eE0)^2), see
        sauter_step_lcfa_closed_form; eE0 L^2 >> 1 alone is NOT enough in weak fields).
    Valid when: static Sauter step, m >= 0, eE0 > 0 (energy^2), L > 0 (1/energy); both rates are exactly 0 for
        eE0 L <= m (step height below 2m)."""
    m = _mass(m)
    eE0, L = _pos(eE0, "eE0"), _pos(L, "L")
    nf = (lambda o, k: sauter_step_n_spinor(o, k, m, eE0, L)) if fermion else (lambda o, k: sauter_step_n_scalar(o, k, m, eE0, L))
    r = rates_from_n(nf, eE0 * L, -eE0 * L, m, fermion, n_omega, n_k, eE_max=eE0)
    r2 = rates_from_n(nf, eE0 * L, -eE0 * L, m, fermion, n_omega + n_omega // 2, n_k + n_k // 2, eE_max=eE0)
    r["quad_relerr"] = abs(r2["pair_rate"] / r["pair_rate"] - 1) if r["pair_rate"] > 0 else 0.0
    r["resolved"] = bool(r["quad_relerr"] <= flag_rel)
    if strict and not r["resolved"]:
        raise ValueError(f"Sauter-step rate quadrature unresolved (relative change {r['quad_relerr']:.3g} > {flag_rel:g}): "
                         "raise n_omega, n_k")
    r["dV"], r["eE0L2"] = 2 * eE0 * L, eE0 * L * L
    return r


def klein_step_rates(m: float, dV: float, fermion: bool, n_omega: int = 48, n_k: int = 48) -> dict:
    """Rates per unit area of a SHARP potential step of height dV (the L -> 0 limit of the Sauter step).

    Quantity: dict with 'pair_rate' (mean PAIRS per unit time per unit transverse area, energy^3; +inf for scalars:
        the sharp bosonic step's n ~ 1/omega^2 is not integrable) and 'decay_rate' (vacuum-decay rate per area,
        energy^3; scalars: Chervyakov-Kleinert eq. 47 closed form; spinors: quadrature of -ln(1 - n)).
    Valid when: m > 0, dV > 0 (energy); a step sharper than every relevant wavelength (L << 1/dV)."""
    m = _pos(m, "m")
    dV = _pos(dV, "dV")
    if fermion:
        return rates_from_n(lambda o, k: klein_step_n_spinor(o, k, m, dV), 0.5 * dV, -0.5 * dV, m, True, n_omega, n_k)
    w = klein_step_decay_rate_scalar(m, dV)
    return {"pair_rate": float("inf") if dV > 2 * m else 0.0, "decay_rate": w, "im_L_eff": w / 2,
            "ratio": 0.0 if dV > 2 * m else float("nan"), "zone_empty": dV <= 2 * m}


def rates_numeric(V, z0: float, z1: float, m: float, fermion: bool, n_omega: int = 16, n_k: int = 16,
                  eE_max: float = None, **solver) -> dict:
    """Pair-number and vacuum-decay rates per unit area for ANY static step V(z), from the numerical mode solver.

    Evaluates klein_mode_spinor/klein_mode_scalar on the Klein-zone nodes of rates_from_n (all modes at once).
    Quantity: as rates_from_n ('pair_rate' = mean PAIRS per unit time per unit transverse area, 'decay_rate' =
        vacuum-decay rate per area, energy^3), plus 'pair_relerr' and 'decay_relerr' (relative error estimates of the
        two rates: the per-node n_relerr weighted by each node's contribution), 'resolved' (both <= flag_rel = 1e-2),
        'max_n_relerr' over the nodes, 'steps', and 'eE_max' used for the k_perp cut (estimated from V on a
        4001-point grid if not given). Nodes next to the zone edge are admitted up to end adiabaticity 0.5
        (max_eps_end; their mismatch enters their n_relerr).
    Valid when: as klein_mode_*; V constant outside [z0, z1]; quadrature error checked by changing n_omega, n_k
        (finer grids put nodes ever closer to the zone edge, where p -> 0: if the end-adiabaticity test refuses one,
        widen the window or use fewer nodes; 16 x 16 converges the Sauter step to 1e-9)."""
    m = _mass(m)
    z0, z1 = float(z0), float(z1)
    if not (math.isfinite(z0) and math.isfinite(z1)) or z1 <= z0:
        raise ValueError("need finite z0 < z1")
    VL, VR = float(np.asarray(V(z0))), float(np.asarray(V(z1)))
    if eE_max is None:
        zz = np.linspace(z0, z1, 4001)
        eE_max = float(np.max(np.abs(np.diff(np.asarray(V(zz), dtype=float)))) / (zz[1] - zz[0]))
    if VL == VR:
        raise ValueError("V(z0) == V(z1): no step, no Klein zone")
    om, kp, w = _klein_nodes(VL, VR, m, n_omega, n_k, eE_max)
    if len(w) == 0:
        r = _rates(np.zeros(0), w, fermion)
        r.update({"pair_relerr": 0.0, "decay_relerr": 0.0, "resolved": True, "max_n_relerr": 0.0, "steps": 0,
                  "eE_max": eE_max})
        return r
    solver.setdefault("max_eps_end", 0.5)
    sol = (klein_mode_spinor if fermion else klein_mode_scalar)(V, z0, z1, om, kp, m, **solver)
    nk, rel = sol["n"], sol["n_relerr"]
    r = _rates(nk, w, fermion)
    g = 2.0 if fermion else 1.0
    with np.errstate(invalid="ignore", divide="ignore"):
        dn = np.where(nk > 0, nk * rel, 0.0)                                    # absolute error of n per node
        pair_err = g * float(np.sum(w * dn))
        dec_err = g * float(np.sum(w * dn / np.where(fermion, 1.0 - nk, 1.0 + nk)))   # |d ln(1 -+ n)/dn| dn
    pr = pair_err / r["pair_rate"] if r["pair_rate"] > 0 else 0.0
    dr = dec_err / r["decay_rate"] if r["decay_rate"] > 0 else 0.0
    r.update({"pair_relerr": pr, "decay_relerr": dr, "resolved": bool(pr <= 1e-2 and dr <= 1e-2),
              "max_n_relerr": float(np.max(rel)), "steps": sol["steps"], "eE_max": eE_max})
    return r


def _li2(y):
    """Dilogarithm Li2(y) for 0 <= y <= 1, vectorised: 60-term series for y <= 1/2 (truncation < 2^-60), else Euler's
    reflection Li2(y) = pi^2/6 - ln(y) ln(1 - y) - Li2(1 - y)."""
    y = np.asarray(y, dtype=float)
    k = np.arange(1, 61, dtype=float)

    def series(t):
        return (t[:, None] ** k[None, :] / (k * k)[None, :]).sum(axis=1)
    out = np.empty_like(y)
    lo = y <= 0.5
    out[lo] = series(y[lo])
    t = y[~lo]
    with np.errstate(divide="ignore", invalid="ignore"):
        ll = np.where(t < 1.0, np.log(t) * np.log1p(-t), 0.0)
    out[~lo] = PI * PI / 6.0 - ll - series(1.0 - t)
    return out


def _schwinger_li_ratio(x, fermion):
    """w/Gamma of a constant field as a function of x = e^{-pi m^2/eE} in (0, 1]: Li2(x)/x (spinor), -Li2(-x)/x =
    [Li2(x) - Li2(x^2)/2]/x (scalar); the same sums as qft_production.schwinger_closed_forms, vectorised."""
    x = np.asarray(x, dtype=float)
    return (_li2(x) if fermion else _li2(x) - 0.5 * _li2(x * x)) / x


def _lcfa_integrand(eE_of_z, z, m, g):
    eE = np.abs(np.asarray(eE_of_z(z), dtype=float))
    if not np.all(np.isfinite(eE)):
        raise ValueError("eE(z) must be finite on [z0, z1]")
    with np.errstate(divide="ignore", under="ignore"):
        x = np.where(eE > 0, np.exp(-PI * m * m / np.maximum(eE, 1e-300)), 0.0)
    return g * eE * eE / (8 * PI ** 3) * x, x


def lcfa_rates_per_area(eE_of_z, z0: float, z1: float, m: float, fermion: bool, n: int = 400, rtol: float = 1e-9,
                        strict: bool = False, flag_rel: float = 1e-6) -> dict:
    """Locally-constant-field approximation: int dz of Schwinger's pair-number rate and of his vacuum-decay rate.

    Gamma_A = int dz g (eE)^2/(8 pi^3) e^{-pi m^2/|eE|};  w_A = int dz w_Schwinger(|eE(z)|) (all n; = Gamma integrand x
    Li2(x)/x, spinor, or -Li2(-x)/x, scalar, x = e^{-pi m^2/|eE|}, as qft_production.schwinger_closed_forms).
    Quadrature: |eE| is scanned on 4001 points of [z0, z1] and the scan is zoomed (up to 6 times) onto the LIVE support
    |eE| > pi m^2/700 (outside it e^{-pi m^2/eE} < e^{-700}: nothing to integrate) until that support spans >= 64 scan
    cells; the live support is then covered by composite 16-point Gauss-Legendre panels, doubled from n/16 panels
    until the panel-halving change of the pair rate is <= rtol (at most 2^14 panels).
    Quantity: dict with 'pair_rate' (mean PAIRS per unit time per unit transverse area, energy^3) and 'decay_rate'
        (vacuum-decay rate per area, energy^3) in the LCFA, spin-summed for spinors; 'ratio' = w/Gamma; 'quad_relerr'
        (panel-halving relative change of each rate, the larger), 'resolved' (quad_relerr <= flag_rel; strict=True
        raises otherwise), 'support' (the live interval integrated), 'panels'.
    Valid when: the LCFA itself holds: gamma = m/(eE0 L) << 1 AND pi m^4/(4 eE0^3 L^2) << 1, i.e. eE0 L^2 >>
        max(1, (m^2/eE0)^2) for a field of peak eE0 and width L. The relative correction is about
        -[(pi/4)(m^2/eE0)^2 + O(m^2/eE0) + O(1)]/(eE0 L^2) (measured for the Sauter step, spinor: -2.54 at
        eE0 = m^2, -13.4 at 0.3 m^2, -91 at 0.1 m^2, times 1/(eE0 L^2)); NOT simply O(1/(eE0 L^2)) in weak fields,
        where exact/LCFA ~ exp(-pi m^4/(4 eE0^3 L^2)). It ignores the threshold (nonzero even when the step height is
        below 2m, where the exact rate is 0). m > 0; eE vectorised, field negligible outside [z0, z1]; the live support
        (or one of its pieces) is wider than (z1 - z0)/4000, so that the first scan sees it."""
    m = _pos(m, "m")
    z0, z1 = float(z0), float(z1)
    if not (math.isfinite(z0) and math.isfinite(z1)) or z1 <= z0 or n < 16:
        raise ValueError("need finite z0 < z1 and n >= 16")
    g = 2.0 if fermion else 1.0
    thr = PI * m * m / 700.0
    a, b = z0, z1
    for _ in range(7):                                              # locate (and zoom onto) the live support
        zs = np.linspace(a, b, 4001)
        es = np.abs(np.asarray(eE_of_z(zs), dtype=float))
        if not np.all(np.isfinite(es)):
            raise ValueError("eE(z) must be finite on [z0, z1]")
        idx = np.nonzero(es > thr)[0]
        if len(idx) == 0:
            if (a, b) == (z0, z1):
                return {"pair_rate": 0.0, "decay_rate": 0.0, "ratio": float("nan"), "quad_relerr": 0.0,
                        "resolved": True, "support": (float("nan"), float("nan")), "panels": 0}
            break
        a, b = zs[max(idx[0] - 1, 0)], zs[min(idx[-1] + 1, 4000)]
        if idx[-1] - idx[0] >= 64:
            break

    def rule(P):
        edges = np.linspace(a, b, P + 1)
        x, w = np.polynomial.legendre.leggauss(16)
        zc, hw = 0.5 * (edges[:-1] + edges[1:]), 0.5 * (edges[1:] - edges[:-1])
        z = (zc[:, None] + hw[:, None] * x[None, :]).ravel()
        ww = (hw[:, None] * w[None, :]).ravel()
        f, xx = _lcfa_integrand(eE_of_z, z, m, g)
        return float(np.sum(ww * f)), ww, f, xx

    P = max(int(n) // 16, 1)
    I1 = rule(P)[0]
    while True:
        I2, ww, f, xx = rule(2 * P)
        rel_p = abs(I2 - I1) / abs(I2) if I2 > 0 else (0.0 if I1 == 0 else float("inf"))
        if rel_p <= rtol or 4 * P > 2 ** 14:
            break
        P, I1 = 2 * P, I2
    pair = I2
    live = f > 0
    ratio_x = np.zeros_like(f)
    ratio_x[live] = _schwinger_li_ratio(xx[live], fermion)
    dec = float(np.sum(ww * f * ratio_x))
    _, ww1, f1, xx1 = rule(P)
    l1 = f1 > 0
    r1 = np.zeros_like(f1)
    r1[l1] = _schwinger_li_ratio(xx1[l1], fermion)
    dec1 = float(np.sum(ww1 * f1 * r1))
    rel_d = abs(dec - dec1) / abs(dec) if dec > 0 else 0.0
    rel = max(rel_p, rel_d)
    if strict and rel > flag_rel:
        raise ValueError(f"LCFA quadrature unresolved (relative change {rel:.3g} > {flag_rel:g}); check the window")
    return {"pair_rate": pair, "decay_rate": dec, "ratio": dec / pair if pair > 0 else float("nan"), "quad_relerr": rel,
            "resolved": bool(rel <= flag_rel), "support": (float(a), float(b)), "panels": 2 * P}


def sauter_step_lcfa_closed_form(m: float, eE0: float, L: float, fermion: bool) -> dict:
    """LCFA rates of the Sauter step in closed form: GG 2016 eqs. 9.18 (pair number) and 9.19 (vacuum decay).

    Gamma_A = g L (eE0)^2/(2pi)^3 e^{-x} delta(x),  delta(x) = sqrt(pi) Psi(1/2, -1; x) = int_0^inf dt t^-1/2 (1+t)^-5/2 e^{-xt},
    x = pi m^2/eE0 (Psi = Tricomi U, mpmath.hyperu);  w_A = mu Gamma_A, mu = sum_{j>=0} (+-1)^j [delta((j+1)x)/delta(x)]
    e^{-jx}/(j+1)^2 (+ fermions, alternating bosons).
    Quantity: dict with 'pair_rate' (LCFA mean PAIRS per unit time per unit transverse area, energy^3) and
        'decay_rate' (LCFA vacuum-decay rate per area, energy^3), spin-summed for spinors; 'ratio' = w/Gamma;
        'gamma' = m/(eE0 L) and 'weak_field_exponent' = pi m^4/(4 eE0^3 L^2) (exact/LCFA ~ exp(-that) for weak
        fields; both must be << 1 for the LCFA to hold).
    Valid when: gamma = m/(eE0 L) << 1 and pi m^4/(4 eE0^3 L^2) << 1, i.e. eE0 L^2 >> max(1, (m^2/eE0)^2); relative
        correction ~ -[(pi/4)(m^2/eE0)^2 + O(m^2/eE0) + O(1)]/(eE0 L^2) (Part D; GG's "eE0 L^2 >> 1, >> m^2/eE0" is
        not enough: at eE0 = 0.1 m^2, eE0 L^2 = 100, exact/LCFA = 0.38); m > 0, eE0 > 0 (energy^2), L > 0 (1/energy)."""
    import mpmath as mp
    m, eE0, L = _pos(m, "m"), _pos(eE0, "eE0"), _pos(L, "L")
    x = PI * m * m / eE0
    g = 2.0 if fermion else 1.0
    delta = lambda y: math.sqrt(PI) * mp.hyperu(0.5, -1, y)      # noqa: E731
    d1 = delta(x)
    pair = float(g * L * eE0 * eE0 / (2 * PI) ** 3 * mp.e ** (-x) * d1)
    mu, j = mp.mpf(0), 0
    while True:
        term = (1 if fermion else (-1) ** j) * delta((j + 1) * x) / d1 * mp.e ** (-j * x) / (j + 1) ** 2
        mu += term
        if abs(term) < 1e-17 * abs(mu) or j > 2000:
            break
        j += 1
    return {"pair_rate": pair, "decay_rate": float(mu) * pair, "ratio": float(mu), "gamma": m / (eE0 * L),
            "weak_field_exponent": PI * m ** 4 / (4 * eE0 ** 3 * L * L)}


# ---------------------------------------------------------------- self-test
def selftest(verbose: bool = True) -> bool:
    """Compare with closed forms, exact limits and published results. Returns True if all pass."""
    import mpmath as mp
    results = []

    def check(name, got, want, tol, rel=False):
        err = abs(got - want) / (abs(want) if rel and want != 0 else 1.0)
        ok = bool(err <= tol)
        results.append(ok)
        if verbose:
            print(f"{'PASS' if ok else 'FAIL'}  {name}: {got:.10g} (expected {want:.10g}, {'rel' if rel else 'abs'} tol {tol:g})")

    def gg_mp(om, kp, m, eE0, L, fermion):
        """GG 2016 eqs. 9.4/9.6 evaluated literally in 40-digit mpmath (an independent code path from the log form)."""
        with mp.workdps(40):
            a = mp.mpf(eE0) * L
            ep2 = mp.mpf(m) ** 2 + mp.mpf(kp) ** 2
            pL, pR = mp.sqrt((om - a) ** 2 - ep2), mp.sqrt((om + a) ** 2 - ep2)
            num = mp.sinh(PI * L * pL) * mp.sinh(PI * L * pR)
            if fermion:
                return float(num / abs(mp.sinh(PI * L * (a + (pL - pR) / 2)) * mp.sinh(PI * L * (a - (pL - pR) / 2))))
            lam = mp.sqrt(mp.mpf(eE0 * L * L) ** 2 - mp.mpf(1) / 4)          # complex sqrt below 1/2: cosh(i x) = cos x
            return float(num / (mp.re(mp.cosh(PI * lam) ** 2) + mp.sinh(PI * L * (pL - pR) / 2) ** 2))

    # 1. Sharp Klein step, both solvers vs the closed forms. The Magnus steps are exact for a piecewise-constant
    #    potential when the jump sits on a grid node, so agreement must be at roundoff (tol 1e-10: roundoff of
    #    ~1e3 steps on amplitudes of order 1). Bosons: Chervyakov & Kleinert 2009 (arXiv:0906.1422, CK) p. 4, quoted
    #    (fetch_text; ligatures normalised, stray spaces closed): "In the limit k → ∞ where ¯δ → 1/2, Eq. (19) reproduces
    #    the well-known coefficient [7]: R =  p(−) 3 −p(+) 3 p(−) 3 +p(+) 3   2 (20) for the reflection of a relativistic
    #    particle off a potential step" -- the extraction drops the fraction bar and exponent; our reading:
    #    R = ((p3(-) - p3(+))/(p3(-) + p3(+)))^2. And p. 5: "the vacuum persistence probability, is related to the
    #    reflection coefficient by |⟨0|0⟩|2 = ∏ p0, p⊥ Rp", so in the Klein zone n = 1/R - 1 = 4 p_L p_R/(p_L - p_R)^2.
    #    Fermions: the L -> 0 limit of GG eq. 9.4 (quoted in check 2).
    dV, m = 4.0, 1.0
    Vs = lambda z: np.where(np.asarray(z) < 0, 0.5 * dV, -0.5 * dV)      # noqa: E731
    om = np.array([0.3, -0.7, 0.9, 0.05])                                 # all inside the Klein zone
    kp = np.array([0.0, 0.4, 0.2, 0.9])
    rs = klein_mode_scalar(Vs, -3.0, 3.0, om, kp, m, steps=50)
    rf = klein_mode_spinor(Vs, -3.0, 3.0, om, kp, m, steps=50)
    check("sharp step, scalar: ODE n vs 4 p_L p_R/(p_L - p_R)^2 (CK eq. 20), max rel. error",
          float(np.max(np.abs(rs["n"] / klein_step_n_scalar(om, kp, m, dV) - 1))) + float(not np.all(rs["in_klein_zone"])),
          0.0, 1e-10)
    check("sharp step, spinor: ODE n vs 4 p_L p_R/(dV^2 - (p_L - p_R)^2) (GG eq. 9.4 at L -> 0), max rel. error",
          float(np.max(np.abs(rf["n"] / klein_step_n_spinor(om, kp, m, dV) - 1))) + float(not np.all(rf["in_klein_zone"])),
          0.0, 1e-10)
    #    Textbook cross-check of the fermion formula, 1D Dirac Klein step (k_perp = 0): kinetic energies pi_R = 2,
    #    pi_L = -2, m = 1: T = 4|kappa|/(1 + |kappa|)^2, |kappa| = (p_L/|pi_L + m|)(pi_R + m)/p_R = 3 -> T = 3/4.
    check("sharp step, spinor at pi_L = -2, pi_R = 2, m = 1: n = 3/4 (1D Dirac Klein step)",
          float(klein_step_n_spinor(0.0, 0.0, 1.0, 4.0)), 0.75, 1e-14)

    # 2. Sauter step: both ODE solvers vs Gavrilov & Gitman 2016 (PRD 93 045002 = arXiv:1506.01156, GG) p. 34-35, quoted
    #    (fetch_text): "A0(x) =−αE tanh (x/α), α> 0, E(x) = E cosh−2 (x/α), U (x) =−eA0(x) = eEα tanh (x/α), (9.1)";
    #    "⏐⏐g ( + ⏐⏐− )⏐⏐−2 = sinh ( πα ⏐⏐pL⏐⏐) sinh ( πα ⏐⏐pR⏐⏐) ⏐⏐sinh { πα [ eEα + 1 2 (|pL|−| pR|) ]} sinh { πα [ eEα− 1 2
    #    (|pL|−| pR|) ]} ⏐⏐. (9.4)"; "⏐⏐g ( + ⏐⏐− )⏐⏐−2 = sinh ( πα ⏐⏐pL⏐⏐) sinh ( πα ⏐⏐pR⏐⏐) cosh2 [ π √ (eEα2)2− 1 4 ] + sinh2
    #    [ πα 2 (|pL|−| pR|) ] . (9.6)"; "In the range Ω 3, the quantity N cr n has the form N cr n =|g (+|− )|−2 (7.7), where
    #    |g (+|− )|−2 are given by Eq. (9.4) for fermions and by Eq. (9.6) for bosons." The extraction drops fraction bars
    #    and exponents; our reading (alpha = L): 9.4 = sinh(pi L pL) sinh(pi L pR) / |sinh(pi L [eE L + (pL - pR)/2])
    #    sinh(pi L [eE L - (pL - pR)/2])|, 9.6 = sinh(pi L pL) sinh(pi L pR) / (cosh^2[pi sqrt((eE L^2)^2 - 1/4)] +
    #    sinh^2[pi L (pL - pR)/2]). The same as Kim, Lee & Yoon 2010 (arXiv:0910.3363, KLY II) eq. 25, quoted: "Nω k⊥ σ =
    #    2 sinh(πLk z(+)) sinh(πLk z(− )) cosh(2πλ σ ) + (−1)2σ cosh(πLk z(+) − πLk z(− )) . (25)" with "λ σ = √ (qE0L2)2 −
    #    ( 1 − 2|σ | 2 ) 2 , (15)" (reading: N = 2 sinh sinh/[cosh(2 pi lam) +- cosh(...)], lam_0 = sqrt((qE0L^2)^2 - 1/4),
    #    lam_1/2 = qE0L^2), which agrees with our reading of GG term by term. Our check value is this reading, evaluated
    #    literally in 40-digit mpmath (gg_mp), independent of the log-space implementation.
    #    (eE0, L) = (10, 0.2) has eE0 L^2 = 0.4 < 1/2: the cos branch, with scalar n > 1 (Bose enhancement).
    #    Tolerance 1e-6: the solver's default rtol is 1e-7 on |beta| (n to ~2e-7; the step-halving estimate is ~15x
    #    conservative for a 4th-order method), and its own error estimate (/10) must also stay below 1e-6.
    worst_s = worst_f = flux_b = flux_f = 0.0
    for eE0, L in ((0.5, 3.0), (10.0, 0.2), (1.0, 1.5)):
        V, (z0, z1), _ = sauter_step_potential(eE0, L)
        kp = np.array([0.0, 0.2, 0.3, 0.1, 0.5])
        W = eE0 * L - np.sqrt(1 + kp * kp)
        om = np.array([0.0, 0.3, -0.5, 0.8, -0.95]) * W
        rs = klein_mode_scalar(V, z0, z1, om, kp, 1.0)
        rf = klein_mode_spinor(V, z0, z1, om, kp, 1.0)
        ref_s = np.array([gg_mp(o, k, 1.0, eE0, L, False) for o, k in zip(om, kp)])
        ref_f = np.array([gg_mp(o, k, 1.0, eE0, L, True) for o, k in zip(om, kp)])
        worst_s = max(worst_s, float(np.max(np.abs(rs["n"] / ref_s - 1))), float(np.max(rs["n_relerr"])) / 10)
        worst_f = max(worst_f, float(np.max(np.abs(rf["n"] / ref_f - 1))), float(np.max(rf["n_relerr"])) / 10)
        worst_s = max(worst_s, float(np.max(np.abs(sauter_step_n_scalar(om, kp, 1.0, eE0, L) / ref_s - 1))))
        worst_f = max(worst_f, float(np.max(np.abs(sauter_step_n_spinor(om, kp, 1.0, eE0, L) / ref_f - 1))))
        flux_b, flux_f = max(flux_b, float(rs["flux_error"].max())), max(flux_f, float(rf["flux_error"].max()))
        if eE0 == 10.0:
            nmax_bose = float(rs["n"].max())
    check("Sauter step, scalar: ODE and log-space closed form vs GG eq. 9.6 (mpmath), 15 modes, 3 steps, max rel.",
          worst_s, 0.0, 1e-6)
    check("Sauter step, spinor: ODE and log-space closed form vs GG eq. 9.4 (mpmath), max rel.", worst_f, 0.0, 1e-6)
    check(f"bosonic Klein paradox: R - T = 1 to roundoff, and n > 1 occurs (max n = {nmax_bose:.3f} at eE0 L^2 = 0.4)",
          flux_b + float(nmax_bose <= 1), 0.0, 1e-10)
    check("fermions: R + T = 1 (|c_in|^2 - |c_out|^2 = 1) to roundoff", flux_f, 0.0, 1e-10)

    # 3. No absolute precision floor: n ~ 2e-50 (eE0 = 0.03, L = 60, eE0 L^2 = 108) is read off the growing solution
    #    with a RELATIVE error. rtol 1e-6 on |beta| (estimate 8e-7, true error measured 5e-8 at 16000 steps); tol 1e-5
    #    leaves a factor 10 over the estimate. (The time-dependent solver of qft_production has an absolute floor ~1e-28.)
    V, (z0, z1), _ = sauter_step_potential(0.03, 60.0, ends=12.0)
    rs = klein_mode_scalar(V, z0, z1, [0.0, 0.5], [0.0, 0.2], 1.0, steps=2000, rtol=1e-6)
    ref = np.array([gg_mp(0.0, 0.0, 1.0, 0.03, 60.0, False), gg_mp(0.5, 0.2, 1.0, 0.03, 60.0, False)])
    check(f"deep tunnelling n = {ref[0]:.3g}, {ref[1]:.3g}: ODE vs GG eq. 9.6, max rel. error (resolved, no floor)",
          float(np.max(np.abs(rs["n"] / ref - 1))) + float(not np.all(rs["resolved"])), 0.0, 1e-5)
    #    ...and an unconverged run is flagged, not silently returned (strict refuses it).
    V, (z0, z1), _ = sauter_step_potential(1.0, 1.5)
    rc = klein_mode_scalar(V, z0, z1, [0.2], [0.1], 1.0, steps=2, max_steps=4, rtol=1e-12)
    check("a 4-step run is flagged resolved=False (n_relerr > 1%)", float(not rc["resolved"][0]), 1.0, 0)
    try:
        klein_mode_scalar(V, z0, z1, [0.2], [0.1], 1.0, steps=2, max_steps=4, rtol=1e-12, strict=True)
        refused = 0.0
    except ValueError:
        refused = 1.0
    check("strict=True refuses the unresolved run", refused, 1.0, 0)
    #    Exponents beyond the double range: a three-level staircase V = 2, 0, -2 (m = 1, omega = 0.1, k_perp = 0.2) with an
    #    evanescent middle of length D = 800 (kappa = 1.015, n ~ e^{-1620}, |beta| ~ e^{810} > 1e308). The Magnus steps are
    #    exact for piecewise-constant V with the jumps on grid nodes, so the renormalised ODE must match a 50-digit
    #    transfer-matrix reference (exact segment exponentials in mpmath) to roundoff in ln n (tol 1e-9 absolute on
    #    ln n ~ -1600: measured ~1e-12).
    D, om3, kp3 = 800.0, 0.1, 0.2
    V3 = lambda z: np.where(np.asarray(z) < 0, 2.0, np.where(np.asarray(z) < D, 0.0, -2.0))     # noqa: E731
    r3s = klein_mode_scalar(V3, -800.0, 1600.0, [om3], [kp3], 1.0, steps=48)
    r3f = klein_mode_spinor(V3, -800.0, 1600.0, [om3], [kp3], 1.0, steps=48)
    with mp.workdps(50):
        ep = mp.sqrt(1 + mp.mpf(kp3) ** 2)
        segs = [(mp.mpf(om3) - 2, 800), (mp.mpf(om3), D), (mp.mpf(om3) + 2, 1600 - D)]       # (kinetic energy, length)
        pL, pR = mp.sqrt(segs[0][0] ** 2 - ep ** 2), mp.sqrt(segs[2][0] ** 2 - ep ** 2)
        u = mp.exp(-1j * pL * (-800)) / mp.sqrt(2 * pL)                                        # scalar: (psi, psi')
        st = mp.matrix([u, -1j * pL * u])
        sL = -mp.sign(segs[0][0])                                                              # spinor: (a, b)
        kL, kR = pL / (segs[0][0] + ep), pR / (segs[2][0] + ep)
        a0 = mp.exp(1j * sL * pL * (-800)) / mp.sqrt(2 * abs(kL))
        sp = mp.matrix([a0, sL * kL * a0])
        for pi_, l in segs:
            k = mp.sqrt(mp.mpc(pi_ ** 2 - ep ** 2))
            st = mp.matrix([[mp.cos(k * l), mp.sin(k * l) / k], [-k * mp.sin(k * l), mp.cos(k * l)]]) * st
            Om = l * mp.matrix([[0, 1j * (pi_ + ep)], [1j * (pi_ - ep), 0]])
            q = mp.sqrt(mp.mpc(-(pi_ ** 2 - ep ** 2))) * l
            sp = (mp.cosh(q) * mp.eye(2) + mp.sinh(q) / q * Om) * sp
        lnn_s = -2 * mp.log(abs(mp.sqrt(pR / 2) * (st[0] - 1j * st[1] / pR)))
        lnn_f = -2 * mp.log(mp.sqrt(2 * abs(kR)) * abs(sp[0] - sp[1] / kR) / 2)              # pi_R > 0: c_in = c_-
    check(f"beyond the double range (ln n = {float(lnn_s):.1f} scalar, {float(lnn_f):.1f} spinor): renormalised ODE vs "
          "50-digit transfer matrices, max |ln n error|",
          max(abs(float(r3s["ln_n"][0] - lnn_s)), abs(float(r3f["ln_n"][0] - lnn_f)))
          + float(not (r3s["resolved"][0] and r3f["resolved"][0])), 0.0, 1e-9)

    # 4. Threshold null result: no Klein zone, no pairs, when Delta V < 2 sqrt(m^2 + k_perp^2); the total rate is
    #    EXACTLY 0 for Delta V < 2m. KLY II p. 3, quoted: "Pairs are produced only when ω + qE0L ≥ m and ω − qE0L ≤ − m,
    #    under which the particle- and antiparticle-state can be defined asymptotically".
    r0 = [sauter_step_rates(1.0, 1.0, 0.99, f)["pair_rate"] + sauter_step_rates(1.0, 1.0, 0.99, f)["decay_rate"]
          for f in (True, False)]
    V, (z0, z1), _ = sauter_step_potential(1.0, 0.99)
    rn = rates_numeric(V, z0, z1, 1.0, True)
    check("Delta V = 1.98 m < 2m: exact rates (both statistics, closed form and ODE path) are exactly 0",
          sum(r0) + rn["pair_rate"] + float(not rn["zone_empty"]), 0.0, 0)
    V, (z0, z1), _ = sauter_step_potential(1.0, 1.2)                     # Delta V = 2.4: zone closes at k_perp = 0.663
    rz = klein_mode_spinor(V, z0, z1, [0.0, 0.0], [0.5, 0.7], 1.0)
    check("Delta V = 2.4 m: k_perp = 0.7 mode (2 eps_perp = 2.44 > Delta V) gets n = 0, k_perp = 0.5 does not",
          float(rz["n"][1] == 0 and not rz["in_klein_zone"][1] and rz["n"][0] > 0), 1.0, 0)
    #    GG p. 35, quoted: "⏐⏐g ( + ⏐⏐− )⏐⏐−2 ∼ ⏐⏐αpR⏐⏐→ 0, ⏐⏐g ( + ⏐⏐− )⏐⏐−2 ∼ ⏐⏐αpL⏐⏐→ 0. (9.9)" and "c)|g (+|− )|−2→ 0 in
    #    the range Ω 3 if n tends to the boundary with the range Ω 2 ( ⏐⏐pR⏐⏐→ 0)" (reading: n ~ L p_R at the zone edge).
    #    By ODE, n/p_R at p_R = 0.02 and 0.01
    #    agrees within 1% (the next term is O(p_R^2 L^2) relative: 4e-4 here; tol 1% leaves room for the solver).
    eE0, L = 1.0, 1.5
    V, (z0, z1), _ = sauter_step_potential(eE0, L)
    pR = np.array([0.02, 0.01])
    om_e = np.sqrt(1.0 + pR * pR) - eE0 * L                              # (omega + a)^2 - m^2 = p_R^2, k_perp = 0
    re = klein_mode_scalar(V, z0, z1, om_e, [0.0, 0.0], 1.0)
    check("zone edge (GG eq. 9.9): n ~ p_R, ODE ratio [n/p_R](0.02)/[n/p_R](0.01)", float(re["n"][0] / pR[0] / (re["n"][1] / pR[1])),
          1.0, 1e-2)
    #    Onset: n ~ p_L p_R near threshold makes the rate grow like (Delta V - 2m)^3 (the zone's (omega, k^2) area
    #    ~ delta^2 times n ~ delta), delta = Delta V/2m - 1. Measured ratios rate(2 delta)/rate(delta): 7.63, 7.92, 7.98,
    #    8.00 (spinor) and 7.50, 7.90, 7.97, 7.99 (scalar) for delta = 0.01, 0.002, 5e-4, 1e-4: the O(delta) correction
    #    is ~0.05 at delta = 0.001, so tol 0.2 there.
    for fermion in (True, False):
        rt = [sauter_step_rates(1.0, 1.0, 1.0 + d, fermion)["pair_rate"] for d in (0.002, 0.001)]
        check(f"threshold onset ({'spinor' if fermion else 'scalar'}): rate ~ (Delta V - 2m)^3, ratio for doubling "
              "Delta V - 2m at Delta V = 2.002 m", rt[0] / rt[1], 8.0, 0.2)

    # 5. Wide step, one mode: n(omega = 0) -> exp(-pi eps_perp^2/eE0). CK p. 4, quoted: "A special case of uniform
    #    electric field along the z-direction is included here in the limit k → 0, v→ ∞ with vk = −eE = const." ...
    #    "so that the reflection coefficient (22) reduces to R = { 1 + exp [ −π(p2 ⊥ +m2) ¯h(e|E|) ]} −1 . (25)" (reading:
    #    R = 1/(1 + exp(-pi (p_perp^2 + m^2)/(hbar e|E|))), so n = 1/R - 1 = exp(-pi eps_perp^2/eE)).
    #    eE0 = 0.3, L = 100 (eE0 L^2 = 3000): leading correction -pi eps^4/(4 eE0^3 L^2) = -0.35% (Part D), measured -0.35%; tol 1%.
    for fermion in (True, False):
        nf = sauter_step_n_spinor if fermion else sauter_step_n_scalar
        check(f"eE0 L^2 = 3000, omega = 0: {'spinor' if fermion else 'scalar'} n -> exp(-pi eps_perp^2/eE0) (CK eq. 25)",
              float(nf(0.0, 0.3, 1.0, 0.3, 100.0)), math.exp(-PI * 1.09 / 0.3), 1e-2, rel=True)

    # 6. Locally-constant-field limit of the RATE: exact Sauter rates -> int dz Gamma_Schwinger(E(z)) (pair number) and
    #    int dz w_Schwinger(E(z)) (vacuum decay); at eE0 = m^2 the corrections are -2.54/(eE0 L^2) (spinor), -1.75/(eE0 L^2)
    #    (scalar), but the coefficient grows like (pi/4)(m^2/eE0)^2 in weak fields (checked below, Part D).
    #    The LCFA reference is GG p. 37, quoted: "ncr = J(d)αδ (2π)d−1 (eE) d 2 exp { −πm2 eE } . (9.18) Here δ = ∫ ∞ 0 dtt−1/ 2
    #    (t + 1)−(d−2)/ 2 exp ( −tπm2 eE ) =√πΨ (1 2,−d− 2 2 ;πm2 eE ) , where Ψ ( a,b ;x) is the confluent hypergeometric
    #    function [52]", and "Pv = exp (−µN cr), µ = ∞∑ j=0 (−1)(1−κ )j/ 2ǫj+1 (j + 1)d/ 2 exp ( −jπm2 eE ) , ǫj =δ−1√πΨ (1 2,
    #    −d− 2 2 ;jπm2 eE ) . (9.19)". Reading (d = 4): ncr = J L delta (eE)^2/(2 pi)^3 exp(-pi m^2/eE), delta = sqrt(pi)
    #    Psi(1/2, -1; pi m^2/eE) (Psi = Tricomi U). NOTE: the printed integral form of delta, with (t + 1)^-(d-2)/2, is NOT
    #    equal to the Psi form (which is the integral with (1 + t)^-(d+1)/2 = (1 + t)^-5/2, i.e. exactly the LCFA); the
    #    exact rate approaches the Psi form (below), the integral form is 15.7% higher at eE0 = m^2 (see source notes).
    #    First, the Psi form equals the direct z-quadrature of the Schwinger rates (2e-14 measured; tol 1e-9 for the
    #    400-node quadrature of exp(-pi m^2 cosh^2(z/L)/eE0)).
    cf = sauter_step_lcfa_closed_form(1.0, 1.0, 10.0, True)
    lq = lcfa_rates_per_area(lambda z: 1.0 / np.cosh(z / 10.0) ** 2, -120.0, 120.0, 1.0, True)
    check("GG eq. 9.18 (Psi form) = int dz Gamma_pairs(E(z)), spinor", cf["pair_rate"], lq["pair_rate"], 1e-9, rel=True)
    check("GG eq. 9.19 (mu series) = int dz w_Schwinger(E(z)) (polylog), spinor", cf["decay_rate"], lq["decay_rate"], 1e-9, rel=True)
    for fermion in (True, False):
        devs = []
        for L in (10.0, 20.0):
            ex = sauter_step_rates(1.0, 1.0, L, fermion)
            lc = sauter_step_lcfa_closed_form(1.0, 1.0, L, fermion)
            devs.append((ex["pair_rate"] / lc["pair_rate"] - 1, ex["decay_rate"] / lc["decay_rate"] - 1, ex["quad_relerr"]))
        tag = "spinor" if fermion else "scalar"
        check(f"{tag}, eE0 = m^2, L = 20/m: exact pair rate within 1% of the LCFA (GG eq. 9.18), quadrature converged",
              abs(devs[1][0]) + 100 * devs[1][2], 0.0, 1e-2)
        check(f"{tag}: deviation from the LCFA scales as 1/(eE0 L^2) (L = 10 -> 20: ratio in [3.6, 4.4])",
              devs[0][0] / devs[1][0], 4.0, 0.4)
        check(f"{tag}: vacuum-decay rate -> int dz w_Schwinger (GG eq. 9.19) with the same 1/L^2 deviation",
              abs(devs[1][1] - devs[1][0]), 0.0, 2e-3)
    #    Weak fields: the deviation coefficient C = (exact/LCFA - 1) eE0 L^2 is NOT O(1). Expanding the omega = 0 exponent,
    #    2 pi L (a - sqrt(a^2 - eps^2)) = pi eps^2/eE0 + pi eps^4/(4 eE0^3 L^2) + ..., gives C -> -(pi/4)(m^2/eE0)^2 for
    #    eE0 << m^2. At eE0 L^2 = 4000: C(0.05)/(-(pi/4)/0.05^2) measured 1.039 (spinor), 1.037 (scalar) (subleading
    #    terms are O(eE0/m^2) relative: tol 0.1 around 1.04); C(0.1 m^2)/C(m^2) measured 35.7 (spinor), i.e. the
    #    eE0 = m^2 coefficient underestimates the weak-field deviation by more than an order of magnitude (check > 20).
    #    And at eE0 = 0.1 m^2, eE0 L^2 = 100 (m L = 31.6: "eE0 L^2 >> 1, m L >> 1" both hold) exact/LCFA = 0.381,
    #    close to exp(-pi m^4/(4 eE0^3 L^2)) = exp(-0.785) = 0.456 (higher orders make up the rest): check < 0.5.
    coef = {}
    for fermion, e0 in ((True, 0.05), (False, 0.05), (True, 0.1), (True, 1.0)):
        Lw = math.sqrt(4000.0 / e0)
        ex = sauter_step_rates(1.0, e0, Lw, fermion, strict=True)
        coef[(fermion, e0)] = (ex["pair_rate"] / sauter_step_lcfa_closed_form(1.0, e0, Lw, fermion)["pair_rate"] - 1) * 4000.0
    for fermion in (True, False):
        check(f"weak field ({'spinor' if fermion else 'scalar'}), eE0 = 0.05 m^2, eE0 L^2 = 4000: LCFA deviation coefficient "
              "/ (-(pi/4)(m^2/eE0)^2) -> 1", coef[(fermion, 0.05)] / (-PI / 4 / 0.05 ** 2), 1.04, 0.1)
    check("spinor: deviation coefficient at eE0 = 0.1 m^2 / that at eE0 = m^2 (> 20: the eE0 = m^2 value does not carry over)",
          float(coef[(True, 0.1)] / coef[(True, 1.0)] > 20), 1.0, 0)
    ex, lc = sauter_step_rates(1.0, 0.1, math.sqrt(1000.0), True), sauter_step_lcfa_closed_form(1.0, 0.1, math.sqrt(1000.0), True)
    check(f"eE0 = 0.1 m^2, eE0 L^2 = 100, m L = 31.6: exact/LCFA = {ex['pair_rate'] / lc['pair_rate']:.3f} < 0.5 "
          f"(weak-field exponent {lc['weak_field_exponent']:.3f} is not small)", float(ex["pair_rate"] / lc["pair_rate"] < 0.5), 1.0, 0)
    #    LCFA quadrature on a window much wider than the field (Gaussian eE = 2 exp(-z^2), window +-200): the live support
    #    is found and integrated by panels; reference: 30-digit mpmath quadrature of the same integrand on [-8, 8] (outside,
    #    exp(-pi e^{64}/2) = 0). Tol 1e-9 (measured 2e-16).
    lw = lcfa_rates_per_area(lambda z: 2.0 * np.exp(-z * z), -200.0, 200.0, 1.0, True, strict=True)
    with mp.workdps(30):
        ref = mp.quad(lambda z: 2 * 4 * mp.exp(-2 * z * z) / (8 * mp.pi ** 3) * mp.exp(-mp.pi / (2 * mp.exp(-z * z))), [-8, 0, 8])
    check("LCFA pair rate, Gaussian field on a +-200 L window (200x wider than the field) vs mpmath quadrature",
          lw["pair_rate"], float(ref), 1e-9, rel=True)

    # 7. Pair number versus vacuum decay from the SAME n. (a) CK 2009 eq. 47 (sharp step, scalar decay rate, elliptic
    #    integrals; read from the PDF and confirmed by checking its eqs. 43 and 46 numerically) vs our quadrature of
    #    ln(1 + n) with n = 4 p_L p_R/(p_L - p_R)^2: measured 3e-7 with 48 nodes (log singularity at omega = 0); tol 2e-6.
    #    CK p. 8, quoted: "Finally, collecting all contributions in Eq. (40) yields the pair production rate per area w⊥ =
    #    v3 3π2¯h3 ( 1 + m v )3{ 1 2 [ (1 −α2) K(α) − (1 +α2)E(α) ] + α 3 [ (1 −α)(4 +α)F ( ϕ, 1 α ) + ( 1 + 3α +α2 ) E ( ϕ,
    #    1 α )]} . (47)", "with the argument α ≡ α−/α+ < 1, where α± = v ±m", "with ϕ = arcsinα" (reading: v^3/(3 pi^2)
    #    (1 + m/v)^3 {[...]/2 + (al/3)[...]} with F(phi, 1/al), E(phi, 1/al) of modulus 1/al). CK p. 5, quoted: "we
    #    obtain for the pair production rate per unit area in the Sauter potential ( 3) the integral representation w⊥ =
    #    − 1 (2π)2¯h3 ∫ v−m 0 dp0 ∫ (p0−v)2−m2 0 dp2 ⊥ lnR(p0,p 2 ⊥). (32)": what CK call the "pair production rate" is
    #    -sum ln R, the VACUUM-DECAY rate (KLY II eq. 24 calls the same integral 2 Im L_eff), not the pair number.
    #    Heights 1.01 m to 1000 m (v = 20, 100 and 1000 used to hit the branch point of F(arcsin al, 1/al) and fail):
    #    measured <= 3.4e-7.
    worst = 0.0
    for v in (1.01, 1.5, 4.0, 20.0, 100.0, 1000.0):
        rq = rates_from_n(lambda o, k: klein_step_n_scalar(o, k, 1.0, 2 * v), v, -v, 1.0, False)
        worst = max(worst, abs(rq["decay_rate"] / klein_step_decay_rate_scalar(1.0, 2 * v) - 1))
    check("sharp step v = 1.01 ... 1000 m: integral of ln(1 + n) = CK eq. 47 closed form, max rel.", worst, 0.0, 2e-6)
    #    (b) Sauter step with L -> 0 at fixed height 2v = 4m: decay rate -> CK eq. 47 with deviation ~ L (measured -5.5e-2
    #    at L = 0.01, -5.7e-3 at L = 0.001), while the PAIR rate diverges: L x pair rate -> (v^2 - m^2)^{5/2}/(20 pi v^3)
    #    (from eq. 9.6: n ~ p^4/(v^2 (v^2 L^2 p^2 + omega^2)) near omega = 0); measured -5.2e-2, -5.4e-3.
    v = 2.0
    ck, lim = klein_step_decay_rate_scalar(1.0, 2 * v), (v * v - 1.0) ** 2.5 / (20 * PI * v ** 3)
    d_dec, d_pair = [], []
    for L in (0.01, 0.001):
        r = rates_from_n(lambda o, k: sauter_step_n_scalar(o, k, 1.0, v / L, L), v, -v, 1.0, False)
        d_dec.append(r["decay_rate"] / ck - 1)
        d_pair.append(r["pair_rate"] * L / lim - 1)
    check(f"Sauter -> sharp step (L = 1e-3): decay rate within 1% of CK eq. 47 (deviation {d_dec[1]:+.2e})", abs(d_dec[1]), 0.0, 1e-2)
    check("... deviation shrinks ~ L (ratio for L/10 in [8, 12])", d_dec[0] / d_dec[1], 10.0, 2.0)
    check(f"... while the boson PAIR rate diverges: L x rate -> (v^2-m^2)^2.5/(20 pi v^3) (deviation {d_pair[1]:+.2e}, ~ L)",
          abs(d_pair[1]) + abs(d_pair[0] / d_pair[1] - 10) / 1000, 0.0, 1e-2)
    #    (c) Strong field: w > Gamma for fermions, w < Gamma for bosons (resolved); weak field: equal to n^2 order.
    for fermion in (True, False):
        rs_, rw_ = sauter_step_rates(1.0, 3.0, 3.0, fermion), sauter_step_rates(1.0, 0.3, 10.0, fermion)
        check(f"{'spinor' if fermion else 'scalar'}: w/Gamma - 1 = {rs_['ratio'] - 1:+.4f} at eE0 = 3 m^2 (sign "
              f"{'+' if fermion else '-'}, > 1e-3), {rw_['ratio'] - 1:+.1e} at eE0 = 0.3 m^2 (< 1e-4)",
              float((rs_["ratio"] > 1) == fermion and abs(rs_["ratio"] - 1) > 1e-3 and abs(rw_["ratio"] - 1) < 1e-4), 1.0, 0)

    # 8. Critical width (Gies & Klingmueller 2005, PRD 72 065001, arXiv:hep-ph/0505099) p. 7-9, quoted: "A0|M = −a tanh(kx1),
    #    A i|M = 0, E 1|M = ak cosh2(kx1)" (reading: E = ak/cosh^2), "The more interesting limit occurs for k = m where the
    #    production rate vanishes." and "Finally, Fig. 3 shows the integrated total pair-production rate ImΓ compared to the
    #    Nikishov result. The agreement is satisfactory and the vanishing pair production for ea = m is reproduced within
    #    the error bars." (scalar QED, Emax = m^2/e; Fig. 3 plots ImΓ/ImΓ_lc vs k/m; no numbers are tabulated, so this is
    #    qualitative). Their ImΓ is the imaginary part of the effective action, i.e. our VACUUM-DECAY rate. Measured
    #    exact/LCFA: 0.9956, 0.8439, 0.4198, 0.0215, 0.0002 at k/m = 0.05, 0.3, 0.6, 0.9, 0.98, and exactly 0 at k = m
    #    (the LCFA is not 0 there). Check: monotone, > 0.97 at k = 0.05 m (the O(k^2) = O(1/(eE0 L^2)) deviation of
    #    check 6), < 0.05 at k = 0.98 m, 0 at k = m.
    ks = (0.05, 0.3, 0.6, 0.9, 0.98)
    ratios = []
    for k in ks:
        ex = sauter_step_rates(1.0, 1.0, 1.0 / k, False)["decay_rate"]
        ratios.append(ex / sauter_step_lcfa_closed_form(1.0, 1.0, 1.0 / k, False)["decay_rate"])
    at_k1 = sauter_step_rates(1.0, 1.0, 1.0, False)["decay_rate"]
    if verbose:
        print("      Gies-Klingmueller curve (scalar decay rate, exact/LCFA) at k/m = "
              + ", ".join(f"{k}: {r:.4f}" for k, r in zip(ks, ratios)))
    check("critical width: exact/LCFA ratio monotone from > 0.97 (k = 0.05 m) to < 0.05 (k = 0.98 m), exactly 0 at k = m",
          float(all(a > b for a, b in zip(ratios, ratios[1:])) and ratios[0] > 0.97 and ratios[-1] < 0.05 and at_k1 == 0.0
                and sauter_step_lcfa_closed_form(1.0, 1.0, 1.0, False)["decay_rate"] > 0), 1.0, 0)

    # 9. Any profile: potential_from_field (numerical V from eE(z) = eE0 sech^2) + ODE reproduces GG eq. 9.4/9.6 per mode
    #    (tol 1e-6: Hermite error O(h^4) ~ 1e-10 relative), and its V matches the exact Gaussian-field potential
    #    -eE0 L (sqrt(pi)/2) erf(z/L) (tol 1e-10 relative to the step height).
    eE0, L = 1.0, 1.5
    Vn = potential_from_field(lambda z: eE0 / np.cosh(z / L) ** 2, -15 * L, 15 * L)
    Vsh = lambda z: Vn(z) + eE0 * L                     # noqa: E731  shift so that V_L = +a, V_R = -a (omega convention)
    om, kp = np.array([0.0, 0.2]), np.array([0.1, 0.3])
    rs, rf = klein_mode_scalar(Vsh, -15 * L, 15 * L, om, kp, 1.0), klein_mode_spinor(Vsh, -15 * L, 15 * L, om, kp, 1.0)
    check("potential_from_field(sech^2) + ODE vs GG eqs. 9.4/9.6, max rel. error over both statistics",
          max(float(np.max(np.abs(rs["n"] / sauter_step_n_scalar(om, kp, 1.0, eE0, L) - 1))),
              float(np.max(np.abs(rf["n"] / sauter_step_n_spinor(om, kp, 1.0, eE0, L) - 1)))), 0.0, 1e-6)
    Vg = potential_from_field(lambda z: np.exp(-(z / 2.0) ** 2), -20.0, 20.0)
    zt = np.array([-3.0, -0.4, 0.7, 2.5, 20.0])
    exact = np.array([-2.0 * math.sqrt(PI) / 2 * (math.erf(z / 2.0) + 1.0) for z in zt])
    check("potential_from_field(Gaussian) vs -L sqrt(pi)/2 [erf(z/L) + 1], max error / step height",
          float(np.max(np.abs(Vg(zt) - exact))) / (2 * math.sqrt(PI)), 0.0, 1e-10)

    # 10. The numerical-rate path: rates_numeric (ODE on every Klein-zone node) vs the closed-form rates on the SAME
    #     nodes (tol 1e-6: the quadrature cancels, leaving the solver's rtol-limited error).
    V, (z0, z1), _ = sauter_step_potential(1.0, 1.5)
    for fermion in (True, False):
        rn = rates_numeric(V, z0, z1, 1.0, fermion, n_omega=10, n_k=8, eE_max=1.0)
        rc = rates_from_n((lambda o, k: sauter_step_n_spinor(o, k, 1.0, 1.0, 1.5)) if fermion else
                          (lambda o, k: sauter_step_n_scalar(o, k, 1.0, 1.0, 1.5)), 1.5, -1.5, 1.0, fermion, 10, 8, eE_max=1.0)
        check(f"rates_numeric vs closed form on the same nodes ({'spinor' if fermion else 'scalar'}), pair and decay, max rel.",
              max(abs(rn["pair_rate"] / rc["pair_rate"] - 1), abs(rn["decay_rate"] / rc["decay_rate"] - 1),
                  rn["pair_relerr"] / 10, rn["decay_relerr"] / 10), 0.0, 1e-6)

    passed = all(results)
    if verbose:
        print(f"\n{sum(results)}/{len(results)} checks passed")
    return passed


def _convergence() -> int:
    """Slow studies (not part of the self-test): solver step counts, quadrature grids, LCFA approach."""
    print("ODE solver, Sauter step eE0 = 1, L = 1.5, (omega, k_perp) = (0.2, 0.1): n and error vs fixed step count")
    V, (z0, z1), _ = sauter_step_potential(1.0, 1.5)
    for fermion in (False, True):
        ref = float((sauter_step_n_spinor if fermion else sauter_step_n_scalar)(0.2, 0.1, 1.0, 1.0, 1.5))
        for n in (50, 100, 200, 400, 800, 1600, 3200):
            r = (klein_mode_spinor if fermion else klein_mode_scalar)(V, z0, z1, [0.2], [0.1], 1.0, steps=n,
                                                                       max_steps=2 * n, rtol=1.0)
            print(f"  {'spinor' if fermion else 'scalar'} steps {r['steps']:5d}: n = {r['n'][0]:.12e}, true rel. error "
                  f"{r['n'][0] / ref - 1:+.2e}, estimate {r['n_relerr'][0]:.2e}")
    print("Deep tunnelling eE0 = 0.03, L = 60 (n ~ 2e-50): relative error vs steps (no absolute floor)")
    V, (z0, z1), _ = sauter_step_potential(0.03, 60.0, ends=12.0)
    ref = float(sauter_step_n_scalar(0.0, 0.0, 1.0, 0.03, 60.0))
    for n in (500, 1000, 2000, 4000, 8000, 16000):
        r = klein_mode_scalar(V, z0, z1, [0.0], [0.0], 1.0, steps=n, max_steps=2 * n, rtol=1.0)
        print(f"  steps {r['steps']:6d}: n = {r['n'][0]:.10e} (exact {ref:.10e}), rel. error {r['n'][0] / ref - 1:+.2e}, "
              f"estimate {r['n_relerr'][0]:.2e}")
    print("Quadrature: Sauter spinor rates (eE0 = 1, L = 3) vs nodes")
    for n in (8, 16, 32, 48, 96):
        r = rates_from_n(lambda o, k: sauter_step_n_spinor(o, k, 1.0, 1.0, 3.0), 3.0, -3.0, 1.0, True, n, n, eE_max=1.0)
        print(f"  n_omega = n_k = {n:3d}: pair {r['pair_rate']:.14e}, decay {r['decay_rate']:.14e}")
    print("LCFA approach (eE0 = m^2): exact/LCFA - 1 for pair and decay rates")
    for fermion in (True, False):
        for L in (2.0, 5.0, 10.0, 20.0, 40.0, 80.0):
            ex = sauter_step_rates(1.0, 1.0, L, fermion, 64, 64)
            lc = sauter_step_lcfa_closed_form(1.0, 1.0, L, fermion)
            d = ex["pair_rate"] / lc["pair_rate"] - 1
            print(f"  {'spinor' if fermion else 'scalar'} L = {L:5.1f}: pair {d:+.5e} (x eE0 L^2: {d * L * L:+.3f}), "
                  f"decay {ex['decay_rate'] / lc['decay_rate'] - 1:+.5e}, quad {ex['quad_relerr']:.1e}")
    print("Numerical rates vs closed form, Sauter eE0 = 1, L = 1.5, growing grids")
    V, (z0, z1), _ = sauter_step_potential(1.0, 1.5)
    for n in (6, 10, 16, 24):
        rn = rates_numeric(V, z0, z1, 1.0, True, n_omega=n, n_k=n, eE_max=1.0)
        rc = sauter_step_rates(1.0, 1.0, 1.5, True, 96, 96)
        print(f"  n = {n:3d}: ODE pair rate {rn['pair_rate']:.12e} vs converged closed form {rc['pair_rate']:.12e}")
    return 0


# ---------------------------------------------------------------- command line
def _length(text: str) -> float:
    """Parse a length ('1e-12 m' -> 1/eV) or a bare number (already in 1/(natural energy unit))."""
    try:
        return float(text)
    except ValueError:
        from unit_tools import Q
        return length_to_inverse_eV(Q(text).expect("length").si)


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("selftest")
    sp = sub.add_parser("sauter", help="Sauter step E0 sech^2(z/L): exact pair-number and vacuum-decay rates per area vs LCFA")
    mp_ = sub.add_parser("mode", help="one mode (omega, k_perp) of the Sauter step: closed form vs ODE")
    pp = sub.add_parser("profile", help="rates for a field profile E(z) by the numerical solver (sauter, gauss)")
    for p in (sp, mp_, pp):
        p.add_argument("--m", default="0.51099895 MeV", help="mass, e.g. '0.511 MeV' (default: electron)")
        p.add_argument("--E", required=True, help="peak field, e.g. '1.32e18 V/m'")
        p.add_argument("--L", required=True, help="width L of the profile, e.g. '1e-12 m'")
        p.add_argument("--scalar", action="store_true", help="scalar QED instead of spinor QED")
    mp_.add_argument("--omega", default="0 eV", help="energy measured from the mid-step potential, e.g. '0 eV'")
    mp_.add_argument("--kperp", default="0 eV", help="transverse momentum (as an energy), e.g. '100 keV'")
    # (No Lorentzian E0/(1 + z^2/L^2): its 1/z^2 tail makes V approach its asymptotes only like 1/z, so the plane-wave
    # ends that the solver needs require windows of thousands of L for near-edge nodes; outside its contract.)
    pp.add_argument("--shape", default="gauss", choices=("sauter", "gauss"),
                    help="E(z) = E0 sech^2(z/L) or E0 exp(-z^2/L^2)")
    pp.add_argument("--n", type=int, default=12, help="quadrature nodes per direction")
    sub.add_parser("convergence", help="slow studies: solver steps, quadrature grids, LCFA approach")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "selftest":
            return 0 if selftest() else 1
        if args.cmd == "convergence":
            return _convergence()
        from unit_tools import Q
        m = qp._energy(args.m)
        eE0 = qp.eE_from_field_SI(Q(args.E).expect("V/m").si)
        L = _length(args.L)
        fermion = not args.scalar
        tag = "spinor (g = 2)" if fermion else "scalar (g = 1)"
        print(f"{tag} QED, m = {m:.6g} eV, eE0 = {eE0:.6g} eV^2 = {eE0 / m ** 2:.4g} m^2, L = {L:.6g} /eV "
              f"= {length_from_inverse_eV(L):.4g} m, eE0 L^2 = {eE0 * L * L:.4g}")
        if args.cmd == "sauter":
            r = sauter_step_rates(m, eE0, L, fermion)
            print(f"step height Delta V = 2 eE0 L = {2 * eE0 * L:.6g} eV = {2 * eE0 * L / m:.4g} m "
                  f"({'Klein zone exists' if 2 * eE0 * L > 2 * m else 'below 2m: NO pairs, exactly'})")
            print(f"pair-number rate (mean pairs per time per area) {r['pair_rate']:.6g} eV^3 = "
                  f"{rate_per_area_to_SI(r['pair_rate']):.6g} m^-2 s^-1   (quadrature rel. change {r['quad_relerr']:.1e}, "
                  f"resolved {r['resolved']})")
            print(f"vacuum-decay rate per area w = 2 Im L_eff  {r['decay_rate']:.6g} eV^3 = "
                  f"{rate_per_area_to_SI(r['decay_rate']):.6g} m^-2 s^-1; w/Gamma = "
                  f"{'n/a (no pairs)' if r['zone_empty'] else format(r['ratio'], '.6f')}")
            lc = sauter_step_lcfa_closed_form(m, eE0, L, fermion)
            print(f"locally-constant-field estimate (GG eq. 9.18): pair rate {lc['pair_rate']:.6g} eV^3 "
                  f"(exact/LCFA = {r['pair_rate'] / lc['pair_rate'] if lc['pair_rate'] > 0 else float('nan'):.4g}; "
                  f"LCFA validity: gamma = m/(eE0 L) = {lc['gamma']:.3g} and pi m^4/(4 eE0^3 L^2) = "
                  f"{lc['weak_field_exponent']:.3g} must both be << 1)")
            return 0
        if args.cmd == "mode":
            om, kp = qp._energy(args.omega), qp._energy(args.kperp)
            V, (z0, z1), (VL, VR) = sauter_step_potential(eE0 / m ** 2, L * m)        # solve in units of m
            mm = asymptotic_momenta(om / m, kp / m, 1.0, VL, VR)
            if not bool(mm["in_klein_zone"]):
                print("mode outside the Klein zone: no pairs in it (n = 0)")
                return 0
            cf = (sauter_step_n_spinor if fermion else sauter_step_n_scalar)(om, kp, m, eE0, L)
            r = (klein_mode_spinor if fermion else klein_mode_scalar)(V, z0, z1, [om / m], [kp / m], 1.0)
            print(f"p_L = {float(mm['p_left']) * m:.6g} eV, p_R = {float(mm['p_right']) * m:.6g} eV")
            print(f"mean pairs per mode{' per spin' if fermion else ''} n: closed form {float(cf):.10g}, ODE {r['n'][0]:.10g} "
                  f"(rel. error estimate {r['n_relerr'][0]:.1e}, resolved {bool(r['resolved'][0])}); "
                  f"reflection R = {r['reflection'][0]:.10g}")
            return 0
        # profile: work in units of m (dimensionless), then convert back
        e0, Lm = eE0 / m ** 2, L * m
        shapes = {"sauter": lambda z: e0 / np.cosh(z / Lm) ** 2, "gauss": lambda z: e0 * np.exp(-(z / Lm) ** 2)}
        half = {"sauter": 15 * Lm, "gauss": 7 * Lm}[args.shape]
        V = potential_from_field(shapes[args.shape], -half, half, 4001)
        dV = abs(V(-half) - V(half))
        print(f"{args.shape}: step height {dV:.6g} m ({'Klein zone exists' if dV > 2 else 'below 2m: NO pairs, exactly'})")
        r = rates_numeric(V, -half, half, 1.0, fermion, n_omega=args.n, n_k=args.n, eE_max=e0)
        lc = lcfa_rates_per_area(shapes[args.shape], -half, half, 1.0, fermion, n=800)
        conv = m ** 3
        print(f"pair-number rate {r['pair_rate'] * conv:.6g} eV^3 = {rate_per_area_to_SI(r['pair_rate'] * conv):.6g} m^-2 s^-1"
              f" (ODE, estimated rel. error {r['pair_relerr']:.1e}, resolved {r['resolved']})")
        print(f"vacuum-decay rate {r['decay_rate'] * conv:.6g} eV^3; w/Gamma = {r['ratio']:.6f}")
        print(f"LCFA: pair rate {lc['pair_rate'] * conv:.6g} eV^3 (exact/LCFA = "
              f"{r['pair_rate'] / lc['pair_rate'] if lc['pair_rate'] > 0 else float('nan'):.4g}; LCFA quadrature rel. "
              f"change {lc['quad_relerr']:.1e}); check the ODE rate by repeating with a larger --n")
    except (ValueError, KeyError) as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
