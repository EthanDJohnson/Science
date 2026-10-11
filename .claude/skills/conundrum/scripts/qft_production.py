#!/usr/bin/env python3
"""qft_production: particle production by classical backgrounds, with every function saying
exactly WHICH quantity it returns (numpy + mpmath, no scipy).

Why this tool exists
    In QFT production problems the usual failure is computing the wrong quantity correctly:
    in-out amplitudes versus in-in expectation values, plane waves versus wave packets, real
    production versus transient vacuum polarisation, a vacuum-decay rate versus a pair-number
    rate, particles versus pairs. Every public function's docstring therefore has a "Quantity:"
    line (what is returned, per mode or integrated, rate or total, particles or pairs, units)
    and a "Valid when:" line, and refuses inputs outside that range with ValueError.

Units (read this first)
    Natural units hbar = c = 1, Heaviside-Lorentz electromagnetism (e^2 = 4 pi alpha). Pick ONE
    energy unit (e.g. eV, or units of the mass m) and give every energy, mass, momentum, frequency
    and inverse time in it; times are then in 1/energy and E-fields as eE in energy^2. Numbers
    per volume are in energy^3, rates per volume in energy^4. This deviates from schemas.md's "SI
    in the Python API" on purpose (the precedent is page_wootters.py): SI helpers below convert,
    and the command line accepts units through unit_tools.Q ("0.511 MeV", "1e18 V/m", "1 fs").

PART A. One bosonic mode with a time-dependent frequency
--------------------------------------------------------
    u''(t) + omega_k(t)^2 u(t) = 0,   omega^2 -> omega_in^2 > 0 (t -> -inf), omega_out^2 > 0 (t -> +inf).
    In vacuum: u = e^{-i omega_in t}/sqrt(2 omega_in) at early times (Wronskian u u*' - u* u' = i).
    Late times: u = (alpha e^{-i w t} + beta e^{+i w t})/sqrt(2 w), w = omega_out, |alpha|^2 - |beta|^2 = 1.
    |beta_k|^2 = <in| a_out^dag a_out |in>: the IN-IN expectation of the out number operator in mode
    k, i.e. the mean number of particles in mode k (and, for a complex field, also of antiparticles
    in mode -k). It is extracted DIRECTLY as beta = sqrt(w/2) e^{-iwt} (u - i u'/w), never as the
    difference (|u'|^2 + w^2|u|^2)/(2w) - 1/2, so the precision floor is (integration error)^2.
    Integrator: 4th-order Magnus (two Gauss points) with the exact 2x2 exponential, vectorised over
    modes; exact for piecewise-constant omega^2 and uniformly accurate for fast oscillations. The
    error estimate is the step-halving difference of beta; roundoff adds about 4 eps sqrt(N) |alpha|.
    Precision floor: floor(|beta|^2) = delta^2, delta = max(step-halving error, roundoff, window-end
    mismatch) (the |beta|^2 that pure numerical noise would show; measured about 1e-29..1e-28 for the
    tanh model, estimated conservatively at about 1e-27). The relative error of |beta|^2 is about
    2 delta/|beta| + delta^2/|beta|^2; results above flag_rel (default 1%) are flagged resolved=False,
    i.e. |beta|^2 must exceed about 4e4 x floor (strict=True raises ValueError instead).
    Window-end mismatch: starting the zeroth-order vacuum where the adiabaticity parameter is
    eps = |d omega/dt|/omega^2 seeds |beta| ~ eps/4, so ends with eps > 1e-3 are refused.

    Integrated spectrum (isotropic omega_k = omega(|k|)): particles per unit volume
        n = g/(2 pi^2) int_0^inf k^2 |beta_k|^2 dk     (g = internal states counted per k).
    For a REAL field each created pair occupies k and -k: pairs = particles/2. For a COMPLEX field
    |beta_k|^2 counts particles in k and equally antiparticles in -k: pairs = particles.

    Exact references (self-test):
      * sudden jump omega1 -> omega2:  |beta|^2 = (omega1 - omega2)^2 / (4 omega1 omega2);
      * the tanh model (Bernard & Duncan 1977; Birrell & Davies 1982 sec. 3.4), with tanh in omega^2:
            omega_k(eta)^2 = k^2 + m^2 (A + B tanh(rho eta)),  omega_in/out = sqrt(k^2 + m^2 (A -/+ B)),
            omega_-+ = (omega_out -+ omega_in)/2,
            |beta_k|^2 = sinh^2(pi omega_-/rho) / (sinh(pi omega_in/rho) sinh(pi omega_out/rho));
      * its adiabatic limit rho -> 0:  |beta_k|^2 -> exp(-2 pi min(omega_in, omega_out)/rho).

PART B. Pair production in a homogeneous electric field E(t) along z (charge e, mass m)
----------------------------------------------------------------------------------------
    Kinetic momentum p(t) = k_par - e A(t), dp/dt = eE(t); eps_perp^2 = m^2 + k_perp^2; omega^2 = eps_perp^2 + p^2.
    * Scalar QED: Part A's solver with omega_k(t)^2 = eps_perp^2 + p(t)^2.
    * Spinor QED: per spin state the Dirac equation reduces exactly to the two-level problem
      i dc/dt = (p(t) sigma_z + eps_perp sigma_x) c; n_k = probability of ending in the positive-energy
      adiabatic state when starting in the negative-energy one (constant E: Landau-Zener).
    * Sauter pulse E0 sech^2(t/tau): exact n_k (Narozhny & Nikishov 1970; Gavrilov & Gitman 1996 eqs. 42-43).
    * Constant field: n_k = exp(-pi eps_perp^2/(eE)) per mode (and per spin). From the SAME n_k:
        mean number of pairs per volume per time  Gamma = g eE/(2pi) int d^2k_perp/(2pi)^2 n_k
            = (eE)^2/(4pi^3) e^{-pi m^2/eE} (spinor, g = 2), (eE)^2/(8pi^3) e^{-pi m^2/eE} (scalar):
            ONLY the n = 1 term of Schwinger's series (Nikishov; Cohen & McGady 2008);
        vacuum-decay rate  w = g eE/(2pi) int d^2k_perp/(2pi)^2 [-ln(1 - n_k)] (fermions) or [+ln(1 + n_k)] (bosons)
            = 2 Im L_eff = (eE)^2/(4pi^3) sum_n n^-2 e^{-n pi m^2/eE} (spinor),
                           (eE)^2/(8pi^3) sum_n (-1)^{n+1} n^-2 e^{-n pi m^2/eE} (scalar).
      w > Gamma for fermions, w < Gamma for bosons; they agree only at weak field. Im L_eff alone is w/2.
    Pairs vs particles: for a charged (complex) field n_k is the number of particles in k, which equals the
    number of antiparticles in -k and the number of pairs in that mode: no factor 1/2.

PART C. Spatially flat FRW, ds^2 = a(eta)^2 (d eta^2 - dx^2), eta = conformal time, k comoving
-------------------------------------------------------------------------------------------
    chi = a phi:  chi_k'' + [k^2 + m^2 a^2 + (6 xi - 1) a''/a] chi_k = 0  (xi = 1/6 conformal, 0 minimal),
    solved by Part A between static in/out regions. Massless + conformal: omega_k = k, nothing is made for any
    a(eta). |beta_k|^2 is per comoving mode; number densities from number_density_isotropic are per comoving
    volume (divide by a_out^3), and for this real field pairs = particles/2.

PART D. First-order (Born, in-in) pair production from a weak classical background, spectral form
-------------------------------------------------------------------------------------------------
    Fourier convention V~(K) = int d^4x e^{i K.x} V(x), K.x = K0 t - K.x, metric (+,-,-,-), s = K^2.
    Positive K0 creates. At first order the mean number of PAIRS is
        scalar vertex  (L = -(1/2) V phi^2 real, -V|phi|^2 complex):
            N = int d^4K/(2pi)^4 theta(K0) |V~(K)|^2 rho(s),  rho = beta/(16 pi) (real) or beta/(8 pi) (complex)
        gravity vertex (g = eta + h, L = -(1/2) h_{mu nu} T^{mu nu}):
            N = (1/4) int d^4K/(2pi)^4 theta(K0) [rho2(s) X2 + rho0(s) X0],
            X2 = h~* Pi2 h~,  X0 = |pi^{mu nu} h~_{mu nu}|^2,  pi = eta - K K/s,
            real scalar: rho2 = s^2 beta^5/(480 pi), rho0 = (s (1 - 6 xi) + 2 m^2)^2 beta/(144 pi);
            photon:      rho2 = s^2/(40 pi), rho0 = 0  (photon/scalar = 12 = c1/c0 of Redi & Tesi 2026)
    (|Fourier transform of the background at total momentum K|^2 x two-particle spectral density.) The 6D
    pair phase space collapses to a 4D integral over K: the background's support decides everything.
    * Massive pairs need s >= 4 m^2. Every Fourier component of a source-free wave has s = 0, so a plane wave
      AND a freely propagating finite packet give ZERO at first order (Gibbons 1975 shows the plane-wave
      result for a massive scalar non-perturbatively). Nonzero first-order yields need timelike support:
      a source region (V~ = -J~/K^2 off the cone), a profile that is not a vacuum solution (e.g. cut off in
      time: wave_equation_residual_planar flags it), or a second-order background (e.g. a product of
      non-collinear waves). Two collinear waves stay on the light cone.
    * Massless pairs: the collinear phase space at s -> 0+ survives (rho_phi2 -> 1/(16 pi)) but the gravity
      vertex vanishes there (rho2, rho0 ~ s^2), so plane gravitational waves still give zero. The
      non-derivative vertex V phi^2 with m = 0 is collinear-singular on null support (the exact plane-wave
      answer is zero by light-front momentum conservation); those functions refuse it unless s_min > 0.
    * Entry points: born_*_homogeneous (V(t) or h(t): per unit volume), born_*_planar (V(t, z): per unit
      transverse area), born_*_general (any V~(K) or h~(K): total). The general ones accept any spectrum
      with timelike support, e.g. a second-order effective background.
    * Born is only O(eps^2) exact: the self-test checks it against the exact mode solver at two amplitudes
      and shows the deviation scaling as eps (scalar, FRW) or eps^2 (Bianchi I).

Assumptions and validity range
    Free fields in a classical, prescribed background (no back-reaction); adiabatic in AND out
    regions (omega^2 > 0 and slowly varying at both window ends). Inside the window omega^2 may be
    negative (tachyonic transient). Particle numbers between the ends are NOT computed: at
    intermediate times the "number" is basis-dependent (transient vacuum polarisation).

Python usage
    import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
    import numpy as np, qft_production as q
    k = np.linspace(0.1, 3, 30)                                   # units of m
    w2, (t0, t1) = q.tanh_model_omega2(k, m=1.0, A=2.0, B=1.0, rho=0.5)
    r = q.bogoliubov_boson(w2, t0, t1)                             # r["beta2"], r["floor"], r["resolved"]
    q.tanh_model_beta2(k, 1.0, 2.0, 1.0, 0.5)                      # closed form
    q.rates_from_modes(lambda kp: q.schwinger_n_mode(kp, 1.0, 1.0), 1.0, True, 12.0)   # Gamma vs w (units of m)
    q.sauter_n_spinor(0.0, 0.3, 1.0, 0.5, 2.0)                     # exact Sauter occupation per spin
    q.stress_spectral_densities([4.0], "photon")                   # (rho2, rho0) of photon pairs at s = 4 m^2
    q.born_scalar_general(lambda K0, Kx, Ky, Kz: ..., m=1.0, s_max=80.0, kappa_max=8.0)   # any V~(K)

Command line (from the project root)
    python3 .claude/skills/conundrum/scripts/qft_production.py selftest
    python3 .claude/skills/conundrum/scripts/qft_production.py tanh --m 1 --A 2 --B 1 --rho 0.5 --k 0.5
    python3 .claude/skills/conundrum/scripts/qft_production.py schwinger --E "1.32e18 V/m"            (electron default)
    python3 .claude/skills/conundrum/scripts/qft_production.py sauter --E "3e17 V/m" --tau "1e-19 s" --scalar
    python3 .claude/skills/conundrum/scripts/qft_production.py gwpacket --field photon --T 5 20 80
    python3 .claude/skills/conundrum/scripts/qft_production.py convergence      (slow: precision floor and grid studies)
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

from unit_tools import C, E_CHARGE, HBAR  # noqa: E402  (CODATA values shared by the toolkit)

PI = math.pi
_EPS = np.finfo(float).eps
_SQRT3 = math.sqrt(3.0)
_G1, _G2 = 0.5 - _SQRT3 / 6.0, 0.5 + _SQRT3 / 6.0     # Gauss-Legendre nodes on [0, 1]


# ---------------------------------------------------------------- SI helpers
def energy_to_eV(E_joule: float) -> float:
    """Convert an energy in J to eV (the natural-unit energy scale used by the command line).

    Quantity: energy in eV, E/e.
    Valid when: always (pure unit conversion)."""
    return E_joule / E_CHARGE


def time_from_inverse_eV(t_nat: float) -> float:
    """Convert a time given in 1/eV (natural units) to seconds: t_SI = t_nat * hbar/e.

    Quantity: time in s.
    Valid when: t_nat is a time in units of 1/eV."""
    return t_nat * HBAR / E_CHARGE


def time_to_inverse_eV(t_s: float) -> float:
    """Convert a time in s to natural units 1/eV: t_nat = t_SI e/hbar.

    Quantity: time in 1/eV.
    Valid when: t_s is a time in seconds."""
    return t_s * E_CHARGE / HBAR


def density_to_SI(n_eV3: float) -> float:
    """Convert a number per volume from eV^3 to m^-3: n_SI = n (e/(hbar c))^3.

    Quantity: number per unit volume in m^-3 (whatever was counted: particles or pairs).
    Valid when: n_eV3 is a number density in eV^3."""
    return n_eV3 * (E_CHARGE / (HBAR * C)) ** 3


def rate_density_to_SI(r_eV4: float) -> float:
    """Convert a rate per volume from eV^4 to m^-3 s^-1: r_SI = r (e/(hbar c))^3 (e/hbar).

    Quantity: events per unit volume per unit time in m^-3 s^-1 (whatever was counted).
    Valid when: r_eV4 is a rate density in eV^4."""
    return r_eV4 * (E_CHARGE / (HBAR * C)) ** 3 * (E_CHARGE / HBAR)


def eE_from_field_SI(E_V_per_m: float) -> float:
    """Natural-unit field strength eE in eV^2 from E in V/m: eE = e E hbar c / e^2 (Heaviside-Lorentz, hbar = c = 1).

    Quantity: eE in eV^2 (eE = m^2 at the critical field E_c = m^2 c^3/(e hbar) = 1.32e18 V/m for electrons).
    Valid when: E_V_per_m is a field strength in V/m (any sign; the magnitude is returned)."""
    return abs(E_V_per_m) * HBAR * C / E_CHARGE


# ---------------------------------------------------------------- input checks
def _arr(x, name: str) -> np.ndarray:
    a = np.asarray(x, dtype=float)
    if not np.all(np.isfinite(a)):
        raise ValueError(f"{name} must be finite")
    return a


def _positive(x, name: str) -> np.ndarray:
    a = _arr(x, name)
    if np.any(a <= 0):
        raise ValueError(f"{name} must be > 0")
    return a


def _log_sinh(x: np.ndarray) -> np.ndarray:
    """ln sinh(x) for x > 0 without overflow."""
    x = np.asarray(x, dtype=float)
    return x + np.log1p(-np.exp(-2.0 * x)) - math.log(2.0)


# ---------------------------------------------------------------- Part A: boson mode solver
def _magnus_boson(omega2, t0: float, t1: float, n: int, w_in: np.ndarray):
    """Propagate (u, u') from the in-vacuum at t0 to t1 with n 4th-order Magnus steps."""
    h = (t1 - t0) / n
    u = np.exp(-1j * w_in * t0) / np.sqrt(2.0 * w_in)
    v = -1j * w_in * u
    for j in range(n):
        t = t0 + j * h
        a1 = np.asarray(omega2(t + _G1 * h), dtype=float)
        a2 = np.asarray(omega2(t + _G2 * h), dtype=float)
        # Omega = (h/2)(A1 + A2) + (sqrt3 h^2/12)[A2, A1],  A = [[0, 1], [-omega^2, 0]]
        c = (_SQRT3 * h * h / 12.0) * (a2 - a1)
        ab = 0.5 * (a1 + a2)
        q2 = c * c - h * h * ab                      # Omega^2 = q2 * identity (traceless 2x2)
        x = np.sqrt(np.abs(q2))
        small = x < 1e-6
        xs = np.where(small, 1.0, x)
        osc = q2 < 0
        Cf = np.where(osc, np.cos(x), np.cosh(x))
        Sf = np.where(small, 1.0 + q2 / 6.0, np.where(osc, np.sin(x), np.sinh(x)) / xs)
        u, v = (Cf + Sf * c) * u + Sf * h * v, -Sf * h * ab * u + (Cf - Sf * c) * v
    return u, v


def _adiabaticity(omega2, t: float, scale: float) -> np.ndarray:
    """eps = |d omega/dt| / omega^2 at t, by a central difference with step scale."""
    d = 1e-4 * scale
    wp = np.sqrt(np.abs(np.asarray(omega2(t + d), dtype=float)))
    wm = np.sqrt(np.abs(np.asarray(omega2(t - d), dtype=float)))
    w = np.sqrt(np.abs(np.asarray(omega2(t), dtype=float)))
    return np.abs(wp - wm) / (2 * d) / np.maximum(w, 1e-300) ** 2


def bogoliubov_boson(omega2, t0: float, t1: float, steps: int = 2000, rtol: float = 1e-7,
                     max_steps: int = 2 ** 16, strict: bool = False, flag_rel: float = 1e-2) -> dict:
    """Bogoliubov coefficient |beta_k|^2 for u'' + omega_k(t)^2 u = 0 between adiabatic in/out vacua.

    omega2(t) must return omega_k(t)^2 (array over modes, energy^2); [t0, t1] is the window (1/energy).
    Steps double from `steps` until the step-halving change of beta is below rtol*|beta| for every
    mode above the floor, or max_steps is reached.

    Quantity: per-mode IN-IN expectation <in|N_out(k)|in> = |beta_k|^2 (mean number of particles in
        mode k after the background has switched off; dimensionless, not a rate, not a pair count),
        plus |alpha|^2, the error estimate of beta, the precision floor of |beta|^2, the estimated
        relative error 'beta2_relerr' and a boolean 'resolved' (beta2_relerr <= flag_rel). Also 'vacuum_persistence_mode' = 1/|alpha_k|^2, the
        in-out probability that mode pair k stays empty (bosons).
    Valid when: omega^2 > 0 at both ends and the ends are adiabatic (|d omega/dt|/omega^2 <= 1e-3);
        the background is classical and prescribed; t1 > t0."""
    t0, t1 = float(t0), float(t1)
    if not (math.isfinite(t0) and math.isfinite(t1)) or t1 <= t0:
        raise ValueError("need finite t0 < t1")
    w2_in = np.atleast_1d(np.asarray(omega2(t0), dtype=float))
    w2_out = np.atleast_1d(np.asarray(omega2(t1), dtype=float))
    if np.any(w2_in <= 0) or np.any(w2_out <= 0) or not (np.all(np.isfinite(w2_in)) and np.all(np.isfinite(w2_out))):
        raise ValueError("omega^2 must be > 0 at both window ends (no particle interpretation otherwise)")
    w_in, w_out = np.sqrt(w2_in), np.sqrt(w2_out)
    scale = (t1 - t0)
    eps_end = np.maximum(_adiabaticity(omega2, t0, scale), _adiabaticity(omega2, t1, scale))
    if np.any(eps_end > 1e-3):
        raise ValueError(f"window ends are not adiabatic (|d omega/dt|/omega^2 up to {eps_end.max():.3g} > 1e-3): "
                         "extend the window so the background has switched off")
    if steps < 2 or max_steps < steps:
        raise ValueError("need 2 <= steps <= max_steps")

    def run(n):
        u, v = _magnus_boson(omega2, t0, t1, n, w_in)
        ph = np.exp(-1j * w_out * t1)
        beta = np.sqrt(w_out / 2.0) * (u - 1j * v / w_out) * ph
        alpha = np.sqrt(w_out / 2.0) * (u + 1j * v / w_out) / ph
        return beta, alpha

    n = int(steps)
    b1, _ = run(n)
    while True:
        b2, a2 = run(2 * n)
        err = np.abs(b2 - b1)
        roundoff = 4.0 * _EPS * math.sqrt(2 * n) * np.abs(a2)
        floor_amp = np.maximum.reduce([err, roundoff, eps_end / 4.0])
        above = np.abs(b2) > 200 * floor_amp
        tol_amp = np.maximum(rtol * np.abs(b2), 2 * roundoff)          # no point asking for less than roundoff
        converged = bool(np.all(err[above] <= tol_amp[above])) if np.any(above) else True
        if converged or 4 * n > max_steps:
            break
        n, b1 = 2 * n, b2
    beta2 = np.abs(b2) ** 2
    floor = floor_amp ** 2
    with np.errstate(divide="ignore", invalid="ignore"):
        relerr = np.where(beta2 > 0, 2 * floor_amp / np.sqrt(beta2) + floor / beta2, np.inf)
    resolved = relerr <= flag_rel
    if strict and not np.all(resolved):
        raise ValueError(f"{int(np.sum(~resolved))} mode(s) have |beta|^2 too close to the precision floor "
                         f"(floor {floor.min():.3g}..{floor.max():.3g}, relative error > {flag_rel:g}); "
                         "use an analytic or high-precision method there")
    return {"beta2": beta2, "alpha2": np.abs(a2) ** 2, "beta_err": err, "floor": floor, "beta2_relerr": relerr, "resolved": resolved,
            "steps": 2 * n, "converged": converged, "omega_in": w_in, "omega_out": w_out,
            "eps_end": eps_end, "vacuum_persistence_mode": 1.0 / np.abs(a2) ** 2,
            "normalisation_error": np.abs(np.abs(a2) ** 2 - beta2 - 1.0)}


def sudden_jump_beta2(omega1, omega2):
    """Closed form for an instantaneous frequency jump omega1 -> omega2.

    Quantity: per-mode in-in mean particle number |beta|^2 = (omega1 - omega2)^2/(4 omega1 omega2)
        (dimensionless).
    Valid when: omega1, omega2 > 0 and the change is fast compared with 1/omega (sudden limit)."""
    w1, w2 = _positive(omega1, "omega1"), _positive(omega2, "omega2")
    return (w1 - w2) ** 2 / (4.0 * w1 * w2)


def sudden_jump_omega2(omega1: float, omega2: float, width: float = 0.0):
    """omega(t)^2 jumping from omega1^2 to omega2^2 at t = 0 (width 0: a step; else a tanh of that width).

    Quantity: a callable t -> omega(t)^2 (energy^2) and a window (t0, t1) in 1/energy.
    Valid when: omega1, omega2 > 0, width >= 0."""
    w1, w2 = float(_positive(omega1, "omega1")), float(_positive(omega2, "omega2"))
    if width < 0:
        raise ValueError("width must be >= 0")
    T = 20.0 / min(w1, w2) + 40.0 * width
    if width == 0:
        return (lambda t: w1 * w1 if t < 0 else w2 * w2), (-T, T)
    return (lambda t: 0.5 * (w1 * w1 + w2 * w2) + 0.5 * (w2 * w2 - w1 * w1) * math.tanh(t / width)), (-T, T)


def tanh_model_omega2(k, m: float, A: float, B: float, rho: float, ends: float = 25.0):
    """The Bernard-Duncan tanh model omega_k(t)^2 = k^2 + m^2 (A + B tanh(rho t)) (tanh in omega^2).

    Quantity: a callable t -> omega_k(t)^2 over the array k (energy^2) and a window (t0, t1) = +-ends/rho
        in 1/energy (the default ends = 25 leaves 2 e^{-50} of the tanh unswitched).
    Valid when: rho > 0, m >= 0, and k^2 + m^2 (A - |B|) > 0 (positive omega^2 everywhere)."""
    k = _arr(k, "k")
    rho = float(_positive(rho, "rho"))
    if m < 0:
        raise ValueError("m must be >= 0")
    if np.any(k * k + m * m * (A - abs(B)) <= 0):
        raise ValueError("need k^2 + m^2 (A - |B|) > 0")
    kk, mm = k * k, m * m
    return (lambda t: kk + mm * (A + B * np.tanh(rho * t))), (-ends / rho, ends / rho)


def tanh_model_beta2(k, m: float, A: float, B: float, rho: float):
    """Exact Bogoliubov coefficient of the tanh model (Bernard & Duncan 1977; Birrell & Davies sec. 3.4).

    |beta_k|^2 = sinh^2(pi omega_-/rho) / (sinh(pi omega_in/rho) sinh(pi omega_out/rho)),
    omega_in/out = sqrt(k^2 + m^2 (A -/+ B)), omega_- = (omega_out - omega_in)/2. Evaluated in logs.

    Quantity: per-mode in-in mean particle number |beta_k|^2 (dimensionless) for one real-scalar
        mode k; in FRW with a(eta)^2 = A + B tanh(rho eta) and conformal coupling it is the number
        in comoving mode k (eta = conformal time, k comoving).
    Valid when: rho > 0, m >= 0, k^2 + m^2 (A - |B|) > 0 and omega_in, omega_out > 0."""
    k = _arr(k, "k")
    rho = float(_positive(rho, "rho"))
    if m < 0:
        raise ValueError("m must be >= 0")
    if np.any(k * k + m * m * (A - abs(B)) <= 0):
        raise ValueError("need k^2 + m^2 (A - |B|) > 0")
    wi = np.sqrt(k * k + m * m * (A - B))
    wo = np.sqrt(k * k + m * m * (A + B))
    wm = 0.5 * np.abs(wo - wi)
    with np.errstate(divide="ignore"):
        num = np.where(wm > 0, 2.0 * _log_sinh(np.maximum(PI * wm / rho, 1e-300)), -np.inf)
    return np.exp(num - _log_sinh(PI * wi / rho) - _log_sinh(PI * wo / rho))


def adiabatic_limit_beta2(omega_in, omega_out, rho: float):
    """Leading adiabatic (rho -> 0) asymptote of the tanh model: exp(-2 pi min(omega_in, omega_out)/rho).

    Quantity: per-mode in-in mean particle number |beta_k|^2, leading exponential only (dimensionless).
    Valid when: rho << omega_in, omega_out (slow switching); corrections are O(exp(-2 pi |omega_-|/rho))
        relative."""
    wi, wo = _positive(omega_in, "omega_in"), _positive(omega_out, "omega_out")
    rho = float(_positive(rho, "rho"))
    return np.exp(-2.0 * PI * np.minimum(wi, wo) / rho)


def _gauss_legendre(a: float, b: float, n: int):
    x, w = np.polynomial.legendre.leggauss(n)
    return 0.5 * (b - a) * x + 0.5 * (b + a), 0.5 * (b - a) * w


def number_density_isotropic(beta2_of_k, kmax: float, n: int = 64, g: float = 1.0, kmin: float = 0.0) -> float:
    """Integrated spectrum g/(2 pi^2) int_kmin^kmax k^2 |beta_k|^2 dk by Gauss-Legendre with n nodes.

    beta2_of_k(k_array) returns |beta_k|^2 (e.g. a lambda wrapping bogoliubov_boson or a closed form).
    Quantity: mean number of PARTICLES per unit volume in energy^3 (comoving volume in FRW), summed
        over the g internal states; for a real field pairs = particles/2, for a complex field
        |beta_k|^2 counts particles (antiparticles equal) and pairs = particles.
    Valid when: omega depends on |k| only, |beta_k|^2 is negligible above kmax (check by raising kmax),
        0 <= kmin < kmax."""
    if not (0 <= kmin < kmax) or not math.isfinite(kmax):
        raise ValueError("need 0 <= kmin < kmax < inf")
    if n < 4:
        raise ValueError("need n >= 4 nodes")
    k, w = _gauss_legendre(kmin, kmax, n)
    b2 = np.asarray(beta2_of_k(k), dtype=float)
    return float(g / (2 * PI * PI) * np.sum(w * k * k * b2))


# ---------------------------------------------------------------- Part B: pair production in an electric field
def _magnus_two_level(ax_of_t, az_of_t, t0: float, t1: float, n: int, c0: np.ndarray, c1: np.ndarray):
    """Propagate i dc/dt = (ax sigma_x + az sigma_z) c with n 4th-order Magnus steps (exact SU(2) exponential)."""
    h = (t1 - t0) / n
    for j in range(n):
        t = t0 + j * h
        x1, z1 = np.asarray(ax_of_t(t + _G1 * h), dtype=float), np.asarray(az_of_t(t + _G1 * h), dtype=float)
        x2, z2 = np.asarray(ax_of_t(t + _G2 * h), dtype=float), np.asarray(az_of_t(t + _G2 * h), dtype=float)
        # b = (h/2)(a1 + a2) + (sqrt3 h^2/6)(a2 x a1), a = (ax, 0, az): a2 x a1 = (0, z2 x1 - x2 z1, 0)
        bx, bz = 0.5 * h * (x1 + x2), 0.5 * h * (z1 + z2)
        by = (_SQRT3 * h * h / 6.0) * (z2 * x1 - x2 * z1)
        nb = np.sqrt(bx * bx + by * by + bz * bz)
        cb = np.cos(nb)
        sb = np.where(nb < 1e-8, 1.0 - nb * nb / 6.0, np.sin(nb) / np.where(nb < 1e-8, 1.0, nb))
        # U = cos|b| - i sin|b|/|b| (bx sx + by sy + bz sz)
        n0 = cb * c0 - 1j * sb * (bz * c0 + (bx - 1j * by) * c1)
        n1 = cb * c1 - 1j * sb * ((bx + 1j * by) * c0 - bz * c1)
        c0, c1 = n0, n1
    return c0, c1


def bogoliubov_fermion_efield(p_of_t, eps_perp, t0: float, t1: float, steps: int = 2000, rtol: float = 1e-7,
                              max_steps: int = 2 ** 16, strict: bool = False, flag_rel: float = 1e-2) -> dict:
    """Spinor-QED pair occupation for a homogeneous E(t) along z, one spin state, by the two-level reduction.

    For fixed canonical momentum k and either spin, the Dirac equation in a homogeneous electric field reduces
    to i dc/dt = (p(t) sigma_z + eps_perp sigma_x) c, p(t) = k_par - e A(t) (kinetic momentum along E,
    dp/dt = eE), eps_perp = sqrt(m^2 + k_perp^2); the instantaneous energies are +-omega = +-sqrt(eps_perp^2 + p^2).
    Start in the negative-energy adiabatic state at t0; n_k = |<positive-energy adiabatic state at t1|c(t1)>|^2.
    Constant E gives Landau-Zener, n_k = exp(-pi eps_perp^2/(eE)) (= Schwinger's occupation).
    p_of_t(t) returns an array over modes (energy); eps_perp is an array (energy).

    Quantity: per-mode, per-spin-state in-in mean number of electrons in mode k (= positrons in -k = pairs
        in that mode) after the field has switched off, |beta_k|^2 (dimensionless); with error estimate,
        precision floor of n, relative error and 'resolved' flags as in bogoliubov_boson. Both spin
        states give the same n_k in a purely electric field (multiply sums by 2).
    Valid when: E(t) homogeneous (no magnetic field), the field is off at both window ends
        (|d theta/dt|/omega <= 1e-3, theta the adiabatic mixing angle), eps_perp > 0, t1 > t0."""
    t0, t1 = float(t0), float(t1)
    if not (math.isfinite(t0) and math.isfinite(t1)) or t1 <= t0:
        raise ValueError("need finite t0 < t1")
    ep = np.atleast_1d(_positive(eps_perp, "eps_perp")).astype(float)
    p_in = np.atleast_1d(np.asarray(p_of_t(t0), dtype=float)) * np.ones_like(ep)
    if not np.all(np.isfinite(p_in)):
        raise ValueError("p(t0) must be finite")

    def theta(t):
        return np.arctan2(ep, np.asarray(p_of_t(t), dtype=float) * np.ones_like(ep))

    d = 1e-4 * (t1 - t0)
    eps_end = np.zeros_like(ep)
    for te in (t0, t1):
        om = np.sqrt(ep ** 2 + (np.asarray(p_of_t(te), dtype=float) * np.ones_like(ep)) ** 2)
        eps_end = np.maximum(eps_end, np.abs(theta(te + d) - theta(te - d)) / (2 * d) / om)
    if np.any(eps_end > 1e-3):
        raise ValueError(f"window ends are not adiabatic (|d theta/dt|/omega up to {eps_end.max():.3g} > 1e-3): "
                         "extend the window so the field has switched off")
    if steps < 2 or max_steps < steps:
        raise ValueError("need 2 <= steps <= max_steps")
    th0, th1 = theta(t0), theta(t1)
    ax = lambda t: ep  # noqa: E731
    az = lambda t: np.asarray(p_of_t(t), dtype=float) * np.ones_like(ep)  # noqa: E731

    def run(n):
        c0, c1 = _magnus_two_level(ax, az, t0, t1, n, -np.sin(th0 / 2) + 0j, np.cos(th0 / 2) + 0j)
        up = np.cos(th1 / 2) * c0 + np.sin(th1 / 2) * c1            # <+|c>, |+> = (cos th/2, sin th/2)
        dn = -np.sin(th1 / 2) * c0 + np.cos(th1 / 2) * c1
        return up, dn

    n = int(steps)
    b1, _ = run(n)
    while True:
        b2, a2 = run(2 * n)
        err = np.abs(np.abs(b2) - np.abs(b1))                       # global phase is irrelevant
        roundoff = 4.0 * _EPS * math.sqrt(2 * n) * np.ones_like(ep)
        floor_amp = np.maximum.reduce([err, roundoff, eps_end / 4.0])
        above = np.abs(b2) > 200 * floor_amp
        tol_amp = np.maximum(rtol * np.abs(b2), 2 * roundoff)          # no point asking for less than roundoff
        converged = bool(np.all(err[above] <= tol_amp[above])) if np.any(above) else True
        if converged or 4 * n > max_steps:
            break
        n, b1 = 2 * n, b2
    nk = np.abs(b2) ** 2
    floor = floor_amp ** 2
    with np.errstate(divide="ignore", invalid="ignore"):
        relerr = np.where(nk > 0, 2 * floor_amp / np.sqrt(nk) + floor / nk, np.inf)
    resolved = relerr <= flag_rel
    if strict and not np.all(resolved):
        raise ValueError(f"{int(np.sum(~resolved))} mode(s) have n_k too close to the precision floor "
                         f"(floor {floor.min():.3g}..{floor.max():.3g})")
    return {"n": nk, "floor": floor, "n_relerr": relerr, "resolved": resolved, "steps": 2 * n,
            "converged": converged, "unitarity_error": np.abs(nk + np.abs(a2) ** 2 - 1.0), "eps_end": eps_end}


def sauter_kinetic_momentum(k_par, eE0: float, tau: float):
    """Kinetic momentum p(t) = k_par + eE0 tau tanh(t/tau) for the Sauter pulse E(t) = E0 sech^2(t/tau).

    (Gauge A_z = -E0 tau tanh(t/tau); dp/dt = eE(t). In -> out, p goes from k_par - eE0 tau to k_par + eE0 tau.)
    Quantity: a callable t -> p(t) over the array k_par (energy) and a window (t0, t1) = +-20 tau (1/energy).
    Valid when: eE0 > 0 (energy^2), tau > 0 (1/energy)."""
    k = _arr(k_par, "k_par")
    eE0, tau = float(_positive(eE0, "eE0")), float(_positive(tau, "tau"))
    return (lambda t: k + eE0 * tau * np.tanh(t / tau)), (-20.0 * tau, 20.0 * tau)


def _log_cosh(x):
    x = np.abs(np.asarray(x, dtype=float))
    return x + np.log1p(np.exp(-2.0 * x)) - math.log(2.0)


def _sauter_in_out(k_par, k_perp, m, eE0, tau):
    k_par, k_perp = _arr(k_par, "k_par"), _arr(k_perp, "k_perp")
    if m < 0:
        raise ValueError("m must be >= 0")
    eE0, tau = float(_positive(eE0, "eE0")), float(_positive(tau, "tau"))
    e2 = m * m + k_perp ** 2
    if np.any(e2 <= 0):
        raise ValueError("need m^2 + k_perp^2 > 0")
    w_in = np.sqrt(e2 + (k_par - eE0 * tau) ** 2)
    w_out = np.sqrt(e2 + (k_par + eE0 * tau) ** 2)
    return w_in, w_out, eE0, tau


def sauter_n_scalar(k_par, k_perp, m: float, eE0: float, tau: float):
    """Exact scalar-QED occupation for the Sauter pulse E(t) = E0 sech^2(t/tau) (Narozhny & Nikishov 1970).

    Gavrilov & Gitman 1996 (PRD 53, 7162) eq. 43; Kim, Lee & Yoon 2008 (arXiv:0807.2696) eq. 68:
        n_k = [cosh(2 pi lam) + cosh(pi tau (w_out - w_in))] / (2 sinh(pi tau w_in) sinh(pi tau w_out)),
        lam = sqrt((eE0 tau^2)^2 - 1/4) (cosh(2 pi lam) -> cos(2 pi |lam|) when eE0 tau^2 < 1/2),
        w_in/out = sqrt(m^2 + k_perp^2 + (k_par -/+ eE0 tau)^2) (k_par = canonical momentum along E).
    Quantity: per-mode in-in mean number of scalar particles in mode k (= antiparticles in -k = pairs in
        that mode), dimensionless; complex scalar field, charge e.
    Valid when: homogeneous Sauter pulse, m^2 + k_perp^2 > 0, eE0 > 0 (energy^2), tau > 0 (1/energy)."""
    w_in, w_out, eE0, tau = _sauter_in_out(k_par, k_perp, m, eE0, tau)
    lam2 = (eE0 * tau * tau) ** 2 - 0.25
    D = PI * tau * np.abs(w_out - w_in)
    den = math.log(2.0) + _log_sinh(PI * tau * w_in) + _log_sinh(PI * tau * w_out)
    if lam2 >= 0:
        num = np.logaddexp(_log_cosh(2 * PI * math.sqrt(lam2)), _log_cosh(D))
    else:
        num = _log_cosh(D) + np.log1p(math.cos(2 * PI * math.sqrt(-lam2)) * np.exp(-_log_cosh(D)))
    return np.exp(num - den)


def sauter_n_spinor(k_par, k_perp, m: float, eE0: float, tau: float):
    """Exact spinor-QED occupation per spin state for the Sauter pulse E(t) = E0 sech^2(t/tau).

    Gavrilov & Gitman 1996 eq. 42 (Narozhny & Nikishov 1970):
        n_k = sinh[(pi tau/2)(2 eE0 tau + w_in - w_out)] sinh[(pi tau/2)(2 eE0 tau + w_out - w_in)]
              / (sinh(pi tau w_in) sinh(pi tau w_out)),   w_in/out as in sauter_n_scalar.
    Quantity: per-mode, per-spin-state in-in mean number of electrons in mode k (= positrons = pairs in
        that mode), dimensionless; multiply by 2 for both spins.
    Valid when: homogeneous Sauter pulse, m^2 + k_perp^2 > 0, eE0 > 0 (energy^2), tau > 0 (1/energy)."""
    w_in, w_out, eE0, tau = _sauter_in_out(k_par, k_perp, m, eE0, tau)
    a = 2 * eE0 * tau
    num = _log_sinh(0.5 * PI * tau * (a + w_in - w_out)) + _log_sinh(0.5 * PI * tau * (a + w_out - w_in))
    return np.exp(num - _log_sinh(PI * tau * w_in) - _log_sinh(PI * tau * w_out))


def schwinger_n_mode(k_perp, m: float, eE: float):
    """Constant-field occupation per mode n_k = exp(-pi (m^2 + k_perp^2)/(eE)) (Landau-Zener form).

    Kim, Lee & Yoon 2008 (arXiv:0807.2696), after eqs. 46 and 51; Cohen & McGady 2008 eq. 20.
    Quantity: per-mode in-in mean number (per spin state for fermions; same for scalars) of particles
        in a mode whose kinetic momentum sweeps through k_par = 0 while the field is on; dimensionless.
    Valid when: E constant over a time T >> sqrt(m^2 + k_perp^2)/(eE) around the crossing; in a pulse,
        eE0 tau^2 >> 1 and |k_par| << eE0 tau (Sauter)."""
    kp = _arr(k_perp, "k_perp")
    if m < 0:
        raise ValueError("m must be >= 0")
    eE = float(_positive(eE, "eE"))
    if np.any(m * m + kp * kp <= 0):
        raise ValueError("need m^2 + k_perp^2 > 0")
    return np.exp(-PI * (m * m + kp * kp) / eE)


def rates_from_modes(n_of_kperp, eE: float, fermion: bool, kmax: float, n: int = 200) -> dict:
    """Pair-number rate AND vacuum-decay rate per unit volume, both from the same per-mode occupation n_k.

    In a constant field each k_par mode makes its transition once, at a rate eE/(2 pi) modes per unit
    length per unit time; summing over k_perp (d^2k/(2pi)^2) and the g spin states (2 for spinors, 1 for scalars):
        pair-number rate  Gamma = g eE/(2pi) int d^2k_perp/(2pi)^2 n_k              (in-in mean number)
        vacuum decay      w     = g eE/(2pi) int d^2k_perp/(2pi)^2 [-ln(1 - n_k)]   (fermions)
                          w     =   eE/(2pi) int d^2k_perp/(2pi)^2 [+ln(1 + n_k)]   (bosons)
    w = 2 Im L_eff (Schwinger's sum over n); Gamma is only its n = 1 term (Nikishov; Cohen & McGady 2008).
    Quantity: dict with 'pair_rate' (mean number of PAIRS per unit volume per unit time, energy^4) and
        'decay_rate' w (vacuum decay: P(vacuum survives) = exp(-w V T), energy^4), plus 'ratio' = w/Gamma.
    Valid when: constant homogeneous E (eE > 0, energy^2); n_of_kperp(k_perp) returns 0 <= n_k < 1
        (fermions) or n_k >= 0 (bosons); n_k negligible beyond kmax."""
    eE = float(_positive(eE, "eE"))
    if not (kmax > 0 and math.isfinite(kmax)) or n < 8:
        raise ValueError("need kmax > 0 and n >= 8")
    k, w = _gauss_legendre(0.0, kmax, n)
    nk = np.asarray(n_of_kperp(k), dtype=float)
    if np.any(nk < 0) or (fermion and np.any(nk >= 1)):
        raise ValueError("occupations must satisfy 0 <= n_k (< 1 for fermions)")
    g = 2.0 if fermion else 1.0
    pref = eE / (2 * PI) / (2 * PI)                          # eE/(2pi) x d^2k/(2pi)^2 = k dk/(2pi)
    pair = g * pref * float(np.sum(w * k * nk))
    decay = g * pref * float(np.sum(w * k * (-np.log1p(-nk) if fermion else np.log1p(nk))))
    return {"pair_rate": pair, "decay_rate": decay, "ratio": decay / pair if pair > 0 else float("nan")}


def schwinger_closed_forms(m: float, eE: float, fermion: bool) -> dict:
    """Schwinger closed forms (Cohen & McGady 2008 eqs. 2 and 5; Kim, Lee & Yoon 2008 eqs. 45-46, 50).

    spinor: Gamma = (eE)^2/(4 pi^3) e^{-pi m^2/eE},   w = (eE)^2/(4 pi^3) sum_n n^-2 e^{-n pi m^2/eE}
    scalar: Gamma = (eE)^2/(8 pi^3) e^{-pi m^2/eE},   w = (eE)^2/(8 pi^3) sum_n (-1)^{n+1} n^-2 e^{-n pi m^2/eE}
    (sums done exactly with mpmath polylog Li_2). w = 2 Im L_eff; Im L_eff alone is HALF the decay rate.
    Quantity: dict with 'pair_rate' Gamma (mean number of pairs per unit volume per unit time) and
        'decay_rate' w (vacuum decay rate per unit volume), both in energy^4, and 'im_L_eff' = w/2.
    Valid when: constant homogeneous E, m > 0, eE > 0 (energy^2); one-loop (no back-reaction)."""
    import mpmath as mp
    m = float(_positive(m, "m"))
    eE = float(_positive(eE, "eE"))
    x = mp.e ** (-mp.pi * m * m / eE)
    pref = eE * eE / (4 * PI ** 3) if fermion else eE * eE / (8 * PI ** 3)
    li = mp.polylog(2, x) if fermion else -mp.polylog(2, -x)
    w = float(pref * li)
    return {"pair_rate": float(pref * x), "decay_rate": w, "im_L_eff": w / 2, "ratio": float(li / x)}


def sauter_pairs_per_volume(m: float, eE0: float, tau: float, fermion: bool, n: int = 96) -> float:
    """Total pairs per unit volume made by a Sauter pulse: g int d^3k/(2pi)^3 n_k with the exact n_k.

    Quantity: mean number of PAIRS per unit volume after the pulse (energy^3; g = 2 spins for spinors,
        1 for a complex scalar); in-in expectation, not a rate.
    Valid when: as sauter_n_scalar/sauter_n_spinor, m > 0; the quadrature covers |k_par| <= eE0 tau + R and
        k_perp <= R, R = 12 (sqrt(eE0) + m + 1/tau); check convergence by changing n."""
    m = float(_positive(m, "m"))
    eE0, tau = float(_positive(eE0, "eE0")), float(_positive(tau, "tau"))
    reach = 12.0 * (math.sqrt(eE0) + m + 1.0 / tau)
    kz, wz = _gauss_legendre(-eE0 * tau - reach, eE0 * tau + reach, n)
    kp, wp = _gauss_legendre(0.0, reach, n)
    KZ, KP = np.meshgrid(kz, kp, indexing="ij")
    nk = sauter_n_spinor(KZ, KP, m, eE0, tau) if fermion else sauter_n_scalar(KZ, KP, m, eE0, tau)
    g = 2.0 if fermion else 1.0
    return float(g * np.einsum("i,j,ij->", wz, wp * kp, nk) / (4 * PI * PI))   # d^3k/(2pi)^3 = dk_z k dk/(4pi^2)


def lcfa_pairs_per_volume(m: float, eE0: float, tau: float, fermion: bool, n: int = 400) -> float:
    """Locally-constant-field estimate int dt Gamma_pairs(E(t)) for the Sauter pulse.

    Quantity: mean number of PAIRS per unit volume (energy^3), integrating the Schwinger pair-number rate
        (NOT the vacuum-decay rate) over E(t) = E0 sech^2(t/tau).
    Valid when: eE0 tau^2 >> 1 and m tau >> 1 (field slowly varying on the formation time); relative
        corrections O(1/(eE0 tau^2))."""
    m = float(_positive(m, "m"))
    eE0, tau = float(_positive(eE0, "eE0")), float(_positive(tau, "tau"))
    t, w = _gauss_legendre(-6 * tau, 6 * tau, n)
    eE = eE0 / np.cosh(t / tau) ** 2
    pref = 1 / (4 * PI ** 3) if fermion else 1 / (8 * PI ** 3)
    return float(np.sum(w * pref * eE * eE * np.exp(-PI * m * m / eE)))


# ---------------------------------------------------------------- Part C: spatially flat FRW
def frw_tanh_scale_factor(A: float, B: float, rho: float):
    """The Birrell-Davies sec. 3.4 universe a(eta)^2 = A + B tanh(rho eta), with analytic a''.

    a' = B rho sech^2/(2a);  a'' = -B rho^2 sech^2 tanh / a - (B rho sech^2)^2/(4 a^3).
    Quantity: callables (a(eta), a''(eta)) (dimensionless scale factor, a'' in energy^2 with eta in
        1/energy, conformal time) and a window (eta0, eta1) = +-25/rho.
    Valid when: A > |B| (a^2 > 0 everywhere), rho > 0."""
    rho = float(_positive(rho, "rho"))
    if not A > abs(B):
        raise ValueError("need A > |B| so that a(eta)^2 > 0")

    def a(eta):
        return np.sqrt(A + B * np.tanh(rho * eta))

    def a_pp(eta):
        sh2 = 1.0 / np.cosh(rho * eta) ** 2
        av = a(eta)
        return -B * rho * rho * sh2 * np.tanh(rho * eta) / av - (B * rho * sh2) ** 2 / (4 * av ** 3)

    return a, a_pp, (-25.0 / rho, 25.0 / rho)


def frw_omega2(k, a, m: float, xi: float, a_pp=None, h: float = None):
    """Mode frequency of chi = a phi for a scalar of mass m and coupling xi R phi^2/2 in flat FRW, conformal time.

    chi_k'' + omega_k(eta)^2 chi_k = 0,  omega_k^2 = k^2 + m^2 a^2 + (6 xi - 1) a''/a
    (conformal coupling xi = 1/6 removes the a''/a term, leaving the Birrell & Davies eq. 3.149 form
    omega^2 = k^2 + m^2 a^2; minimal coupling xi = 0 leaves -a''/a). If a_pp is None, a'' is taken by a
    5-point finite difference with step h (default 1e-2 in the units of eta): truncation about h^4 a^(6)/90,
    roundoff about 1e-16 a/h^2; a smaller h makes the a'' noise stall the solver's step doubling.
    Quantity: a callable eta -> omega_k(eta)^2 over the array of COMOVING wavenumbers k (energy^2, with
        eta in 1/energy; physical momentum = k/a).
    Valid when: a(eta) > 0; m >= 0; any real xi; spatially flat FRW (zero spatial curvature)."""
    k = _arr(k, "k")
    if m < 0:
        raise ValueError("m must be >= 0")
    if not math.isfinite(xi):
        raise ValueError("xi must be finite")
    kk, mm, c = k * k, m * m, 6.0 * xi - 1.0
    if a_pp is None:
        hh = 1e-2 if h is None else float(h)

        def a_pp(eta):   # noqa: F811  (5-point second derivative)
            return (-a(eta + 2 * hh) + 16 * a(eta + hh) - 30 * a(eta) + 16 * a(eta - hh) - a(eta - 2 * hh)) / (12 * hh * hh)

    def w2(eta):
        av = float(a(eta))
        if not av > 0:
            raise ValueError(f"a(eta) = {av} <= 0 at eta = {eta}")
        return kk + mm * av * av + (c * float(a_pp(eta)) / av if c != 0 else 0.0)

    return w2


def frw_particle_production(k, a, m: float, xi: float, eta0: float, eta1: float, a_pp=None, **solver) -> dict:
    """Particles created in flat FRW between adiabatic in (eta0) and out (eta1) regions, per comoving mode.

    Runs bogoliubov_boson on frw_omega2 (keyword arguments go to the solver).
    Quantity: dict whose "beta2" is the per-mode in-in mean number of particles in comoving mode k (real
        scalar, dimensionless), with the solver's floor and resolved flags. For the total use
        number_density_isotropic: particles per COMOVING volume (divide by a_out^3 for per physical
        volume); pairs = particles/2, since each pair occupies k and -k of one real field.
    Valid when: a(eta) and a''/a are static at both ends (omega^2 > 0 and adiabatic there), a > 0 throughout."""
    w2 = frw_omega2(k, a, m, xi, a_pp=a_pp)
    return bogoliubov_boson(w2, eta0, eta1, **solver)

# ---------------------------------------------------------------- Part D: first-order (Born, in-in) production
_ETA = np.diag([1.0, -1.0, -1.0, -1.0])     # mostly-minus metric, K^2 = s > 0 timelike


def pair_spectral_density_scalar(s, m: float, field: str = "real"):
    """Two-particle spectral density rho(s) of the operator a background V couples to, for scalar pairs.

    real field,    L_int = -(1/2) V phi^2, O = phi^2/2:  rho = beta/(16 pi) theta(s - 4m^2)
    complex field, L_int = -V |phi|^2,     O = |phi|^2:   rho = beta/(8 pi)  theta(s - 4m^2)
    beta = sqrt(1 - 4m^2/s); rho(K) = sum over pair states n of (2pi)^4 delta^4(K - p_n) |<n|O|0>|^2, the
    identical-particle 1/2 included for the real field (two-body phase space is beta/(8 pi)).
    Quantity: rho(s), dimensionless, per PAIR state; the Born yield is N_pairs = int d^4K/(2pi)^4 theta(K0)
        |V~(K)|^2 rho(K^2) (mean number of PAIRS; particles = 2 x pairs).
    Valid when: s real; m >= 0; returns 0 for s <= 4m^2 (s = 0 exactly gives 0: see the module notes
        on the collinear massless case)."""
    s = _arr(s, "s")
    if m < 0:
        raise ValueError("m must be >= 0")
    if field not in ("real", "complex"):
        raise ValueError("field must be 'real' or 'complex'")
    th = 4 * m * m
    with np.errstate(divide="ignore", invalid="ignore"):
        beta = np.where(s > th, np.sqrt(np.clip(1 - th / np.where(s > 0, s, 1.0), 0, None)), 0.0)
    return beta / (16 * PI if field == "real" else 8 * PI)


def stress_spectral_densities(s, field: str = "scalar", m: float = 0.0, xi: float = 0.0):
    """Spin-2 and spin-0 spectral densities of T^{mu nu} for pairs of a free field (the gravity vertex).

    rho^{mu nu rho sigma}(K) = sum_pairs (2pi)^4 delta^4(K - p1 - p2) <0|T^{mu nu}|n><n|T^{rho sigma}|0>
                             = rho2(s) Pi2 + rho0(s) pi^{mu nu} pi^{rho sigma},  pi = eta - K K/s,
    Pi2 = (pi pi + pi pi)/2 - pi pi/3. Derived from the explicit vertices (checked by quadrature in the self-test):
      real scalar (mass m, coupling xi R phi^2/2): rho2 = s^2 beta^5/(480 pi),
                                                    rho0 = (s (1 - 6 xi) + 2 m^2)^2 beta/(144 pi);
      photon (Maxwell):                             rho2 = s^2/(40 pi) = 12 x the massless scalar's, rho0 = 0.
    Both vanish like s^2 on the light cone when the field is massless (conformal or not, for rho2).
    Quantity: (rho2, rho0), dimensionful (energy^4), per PAIR state, identical-particle 1/2 included;
        the Born yield for g = eta + h is N_pairs = (1/4) int d^4K/(2pi)^4 theta(K0) [rho2 X2 + rho0 X0].
    Valid when: s real; field 'scalar' (m >= 0, any xi) or 'photon' (m must be 0); zero below threshold."""
    s = _arr(s, "s")
    if field == "photon":
        if m != 0:
            raise ValueError("photons are massless (m must be 0)")
        return np.where(s > 0, s * s / (40 * PI), 0.0), np.zeros_like(s)
    if field != "scalar":
        raise ValueError("field must be 'scalar' or 'photon'")
    if m < 0 or not math.isfinite(xi):
        raise ValueError("need m >= 0 and finite xi")
    th = 4 * m * m
    with np.errstate(divide="ignore", invalid="ignore"):
        beta = np.where(s > th, np.sqrt(np.clip(1 - th / np.where(s > 0, s, 1.0), 0, None)), 0.0)
    return s * s * beta ** 5 / (480 * PI), (s * (1 - 6 * xi) + 2 * m * m) ** 2 * beta / (144 * PI)


def _stress_spectral_numeric(s: float, field: str, m: float = 0.0, xi: float = 0.0, n: int = 24):
    """(rho2, rho0, max |K_mu t^{mu nu}|) by explicit two-body vertices and angular quadrature in the K rest frame."""
    E = math.sqrt(s) / 2
    p = math.sqrt(max(E * E - m * m, 0.0))
    ct, wct = np.polynomial.legendre.leggauss(n)
    ph = np.arange(2 * n) * PI / n
    rho = np.zeros((4, 4, 4, 4))
    K = np.array([math.sqrt(s), 0, 0, 0])
    viol = 0.0
    for c, wc in zip(ct, wct):
        st = math.sqrt(1 - c * c)
        for f in ph:
            nv = np.array([st * math.cos(f), st * math.sin(f), c])
            p1 = np.concatenate([[E], p * nv])
            p2 = np.concatenate([[E], -p * nv])
            ts = []
            if field == "scalar":
                pp = p1 @ _ETA @ p2
                t = -(np.outer(p1, p2) + np.outer(p2, p1)) + np.linalg.inv(_ETA) * (pp + m * m)
                t = t - 2 * xi * (s * np.linalg.inv(_ETA) - np.outer(K, K))
                ts.append(t)
            else:
                e1 = np.cross(nv, [0.0, 0.0, 1.0] if abs(c) < 0.9 else [1.0, 0.0, 0.0])
                e1 /= np.linalg.norm(e1)
                e2 = np.cross(nv, e1)
                for a in (e1, e2):
                    for b in (e1, e2):
                        ea, eb = np.concatenate([[0.0], a]), np.concatenate([[0.0], b])
                        f1 = np.outer(p1, ea) - np.outer(ea, p1)             # F^{mu nu} up to a common phase
                        f2 = np.outer(p2, eb) - np.outer(eb, p2)
                        f1l, f2l = _ETA @ f1 @ _ETA, _ETA @ f2 @ _ETA      # F_{mu nu}
                        g = np.linalg.inv(_ETA)
                        # T^{mu nu} = -F^{mu a} F^{nu}_a + (1/4) eta^{mu nu} F^2, bilinear part for two photons
                        t = -(f1 @ _ETA @ f2.T + f2 @ _ETA @ f1.T) + 0.25 * g * 2 * np.sum(f1l * f2)
                        ts.append(t)
            for t in ts:
                viol = max(viol, float(np.abs(K @ _ETA @ t).max()))
                rho += (wc * PI / n) * np.einsum("ab,cd->abcd", t, t)
    rho *= 0.5 * p / (16 * PI * PI * math.sqrt(s))    # identical-particle 1/2 x dPhi2/dOmega = |p|/(16 pi^2 sqrt s)
    P = np.linalg.inv(_ETA) - np.outer(K, K) / s                             # pi^{mu nu}
    Pl = _ETA @ P @ _ETA                                                      # pi_{mu nu}
    Pi2 = 0.5 * (np.einsum("ac,bd->abcd", Pl, Pl) + np.einsum("ad,bc->abcd", Pl, Pl)) - np.einsum("ab,cd->abcd", Pl, Pl) / 3
    rho2 = float(np.einsum("abcd,abcd->", Pi2, rho)) / 5.0
    rho0 = float(np.einsum("ab,cd,abcd->", Pl, Pl, rho)) / 9.0
    return rho2, rho0, viol


def _metric_weights(K0, Kx, Ky, Kz, H):
    """X2 = h* Pi2 h and X0 = |pi^{mu nu} h_{mu nu}|^2 for lower-index h_{mu nu}(K) (shape (..., 4, 4))."""
    Ku = np.stack([K0, Kx, Ky, Kz], axis=-1)
    s = K0 * K0 - Kx * Kx - Ky * Ky - Kz * Kz
    P = np.linalg.inv(_ETA) - Ku[..., :, None] * Ku[..., None, :] / s[..., None, None]
    H = 0.5 * (H + np.swapaxes(H, -1, -2))
    PHP = np.einsum("...ar,...rs,...bs->...ab", P, H, P)
    tr = np.einsum("...ab,...ab->...", P, H)
    X0 = np.abs(tr) ** 2
    X2 = np.real(np.einsum("...ab,...ab->...", np.conj(H), PHP)) - X0 / 3.0
    return X2, X0


def _ft_time(f_of_t, t0: float, t1: float, omega: np.ndarray, panels: int = None):
    """int_t0^t1 f(t) e^{i omega t} dt by composite 16-point Gauss-Legendre (f returns (..., ) or (..., 4, 4))."""
    if panels is None:
        panels = int(max(8, math.ceil(2.0 * float(np.max(omega)) * (t1 - t0) / PI)))
    x, w = np.polynomial.legendre.leggauss(16)
    edges = np.linspace(t0, t1, panels + 1)
    t = (0.5 * (edges[1:] - edges[:-1])[:, None] * x[None, :] + 0.5 * (edges[1:] + edges[:-1])[:, None]).ravel()
    wt = (0.5 * (edges[1:] - edges[:-1])[:, None] * w[None, :]).ravel()
    f = np.asarray(f_of_t(t))
    ph = np.exp(1j * np.outer(omega, t)) * wt[None, :]
    return np.tensordot(ph, f, axes=([1], [0]))


def _s_nodes(s_th: float, s_max: float, n: int):
    """Gauss nodes for int_{s_th}^{s_max} ds with s = s_th + u^2 (smooth across a sqrt threshold)."""
    u, wu = _gauss_legendre(0.0, math.sqrt(s_max - s_th), n)
    return s_th + u * u, 2 * u * wu


def born_scalar_homogeneous(V_of_t, t0: float, t1: float, m: float, omega_max: float, field: str = "real",
                            n_omega: int = 200) -> dict:
    """Born (first-order, in-in) pairs from a spatially homogeneous V(t) coupled as -(1/2) V phi^2 (real) or -V|phi|^2.

    N/Vol = int_{2m}^{omega_max} d Omega/(2 pi) |V~(Omega)|^2 rho(Omega^2),  V~(Omega) = int V(t) e^{i Omega t} dt.
    (Equivalent to sum_k |beta_k|^2 with beta_k = (1/(2 omega_k)) int V e^{2 i omega_k t} dt at first order.)
    Quantity: dict with 'pairs_per_volume' (mean number of PAIRS per unit volume, energy^3), 'particles_per_volume'
        (= 2 x pairs), and the spectrum 'dN_dOmega' (pairs per volume per unit pair energy Omega) on 'omega'.
    Valid when: |V| << m^2 + k^2 for the relevant modes (first order: compare several amplitudes), V(t) -> 0 at
        both ends of [t0, t1], and |V~| negligible above omega_max > 2m."""
    m = float(m)
    if m < 0 or not omega_max > 2 * m or t1 <= t0:
        raise ValueError("need m >= 0, omega_max > 2m and t1 > t0")
    lo = 2 * m
    om, w = _gauss_legendre(lo, omega_max, n_omega)
    Vt = _ft_time(V_of_t, t0, t1, om)
    dN = np.abs(Vt) ** 2 * pair_spectral_density_scalar(om * om, m, field) / (2 * PI)
    N = float(np.sum(w * dN))
    return {"pairs_per_volume": N, "particles_per_volume": 2 * N, "omega": om, "dN_dOmega": dN}


def born_metric_homogeneous(h_of_t, t0: float, t1: float, omega_max: float, field: str = "scalar", m: float = 0.0,
                            xi: float = 0.0, n_omega: int = 200) -> dict:
    """Born pairs of scalars or photons from a homogeneous metric perturbation g = eta + h(t), coupled as -(1/2) h T.

    h_of_t(t_array) returns lower-index h_{mu nu} with shape (len(t), 4, 4), mostly-minus signature. In the rest
    frame of K = (Omega, 0): X2 = sum_ij |h~_ij|^2 - |sum_i h~_ii|^2/3, X0 = |sum_i h~_ii|^2, and
    N/Vol = (1/4) int d Omega/(2 pi) [rho2 X2 + rho0 X0] (stress_spectral_densities).
    Quantity: dict with 'pairs_per_volume' (mean number of PAIRS per unit volume, energy^3), 'particles_per_volume'
        (= 2 x pairs), 'spin2_part' and 'spin0_part' of the pairs.
    Valid when: |h| << 1 (first order), h -> 0 at both ends of [t0, t1], negligible spectrum above omega_max > 2m."""
    if not omega_max > 2 * m or t1 <= t0:
        raise ValueError("need omega_max > 2m and t1 > t0")
    om, w = _gauss_legendre(2 * m, omega_max, n_omega)
    H = _ft_time(h_of_t, t0, t1, om)
    if H.shape[-2:] != (4, 4):
        raise ValueError("h_of_t must return shape (len(t), 4, 4)")
    z = np.zeros_like(om)
    X2, X0 = _metric_weights(om, z, z, z, H)
    r2, r0 = stress_spectral_densities(om * om, field, m, xi)
    p2 = float(np.sum(w * 0.25 * r2 * X2 / (2 * PI)))
    p0 = float(np.sum(w * 0.25 * r0 * X0 / (2 * PI)))
    return {"pairs_per_volume": p2 + p0, "particles_per_volume": 2 * (p2 + p0), "spin2_part": p2, "spin0_part": p0}


def _check_massless_scalar_vertex(m, s_min):
    if m == 0 and s_min <= 0:
        raise ValueError("massless pairs through the non-derivative vertex V phi^2: rho(s -> 0+) = 1/(16 pi) does not "
                         "vanish, so null (plane-wave) support gives a collinear-singular Born yield, while the exact "
                         "answer for a plane wave is zero; pass s_min > 0 to integrate only the timelike part")


def born_scalar_planar(Vtilde, m: float, s_max: float, y_max: float, field: str = "real", s_min: float = 0.0,
                       n_s: int = 320, n_y: int = 320) -> dict:
    """Born pairs per unit transverse area from a planar background V(t, z) (uniform in x, y), scalar vertex.

    Vtilde(K0, Kz) = int dt dz e^{i(K0 t - Kz z)} V(t, z) (arrays in, complex out). With K0 = sqrt(s) cosh y,
    Kz = sqrt(s) sinh y (dK0 dKz = ds dy/2):  N/A = int ds dy/(2 (2pi)^2) |V~|^2 rho(s), s > max(4m^2, s_min).
    Only timelike K contributes for massive pairs: a source-free wave (all support on K^2 = 0) gives zero.
    Quantity: dict with 'pairs_per_area' (mean number of PAIRS per unit transverse area, energy^2) and
        'particles_per_area' (= 2 x pairs).
    Valid when: first order in V; |V~| negligible for s > s_max or |y| > y_max; m > 0 (or s_min > 0 for m = 0);
        Gauss grids resolve V~ (near-light-cone features are narrow in y: check by doubling n_s, n_y and y_max)."""
    m, s_min = float(m), float(s_min)
    if m < 0 or s_min < 0:
        raise ValueError("need m >= 0 and s_min >= 0")
    _check_massless_scalar_vertex(m, s_min)
    s_th = max(4 * m * m, s_min)
    if not s_max > s_th or not y_max > 0:
        raise ValueError("need s_max > max(4m^2, s_min) and y_max > 0")
    s, ws = _s_nodes(s_th, s_max, n_s)
    y, wy = _gauss_legendre(-y_max, y_max, n_y)
    S, Y = np.meshgrid(s, y, indexing="ij")
    rs = np.sqrt(S)
    val = np.abs(np.asarray(Vtilde(rs * np.cosh(Y), rs * np.sinh(Y)))) ** 2 * pair_spectral_density_scalar(S, m, field)
    N = float(np.einsum("i,j,ij->", ws, wy, val) / (2 * (2 * PI) ** 2))
    return {"pairs_per_area": N, "particles_per_area": 2 * N}


def born_metric_planar(htilde, s_max: float, y_max: float, field: str = "scalar", m: float = 0.0, xi: float = 0.0,
                       n_s: int = 320, n_y: int = 320) -> dict:
    """Born pairs per unit transverse area from a planar metric perturbation h_{mu nu}(t, z), gravity vertex.

    htilde(K0, Kz) returns lower-index h~_{mu nu} with shape (..., 4, 4). N/A = (1/4) int ds dy/(2(2pi)^2)
    [rho2 X2 + rho0 X0], with X2, X0 the covariant projections (any frame). rho2, rho0 vanish as s^2 on the
    light cone for massless fields, so a plane gravitational wave (null support) gives zero even for massless pairs.
    Quantity: dict with 'pairs_per_area' (mean number of PAIRS per unit transverse area, energy^2), 'particles_per_area'.
    Valid when: |h| << 1; spectrum negligible beyond s_max, |y| > y_max; field 'scalar' (m, xi) or 'photon';
        Gauss grids resolve h~ (check by doubling n_s, n_y and y_max)."""
    if not s_max > 4 * m * m or not y_max > 0:
        raise ValueError("need s_max > 4 m^2 and y_max > 0")
    s, ws = _s_nodes(4 * m * m, s_max, n_s)
    y, wy = _gauss_legendre(-y_max, y_max, n_y)
    S, Y = np.meshgrid(s, y, indexing="ij")
    rs = np.sqrt(S)
    K0, Kz = rs * np.cosh(Y), rs * np.sinh(Y)
    H = np.asarray(htilde(K0, Kz))
    z = np.zeros_like(K0)
    X2, X0 = _metric_weights(K0, z, z, Kz, H)
    r2, r0 = stress_spectral_densities(S, field, m, xi)
    N = float(np.einsum("i,j,ij->", ws, wy, 0.25 * (r2 * X2 + r0 * X0)) / (2 * (2 * PI) ** 2))
    return {"pairs_per_area": N, "particles_per_area": 2 * N}


def _four_nodes(s_th, s_max, kappa_max, n_s, n_k, n_c, n_p):
    s, ws = _s_nodes(s_th, s_max, n_s)
    k, wk = _gauss_legendre(0.0, kappa_max, n_k)
    c, wc = np.polynomial.legendre.leggauss(n_c)
    p = np.arange(n_p) * 2 * PI / n_p
    S, Kk, Cc, Pp = np.meshgrid(s, k, c, p, indexing="ij")
    W = np.einsum("i,j,k->ijk", ws, wk * k * k, wc)[..., None] * (2 * PI / n_p)
    K0 = np.sqrt(S + Kk * Kk)
    st = np.sqrt(1 - Cc * Cc)
    return S, K0, Kk * st * np.cos(Pp), Kk * st * np.sin(Pp), Kk * Cc, W / (2 * K0 * (2 * PI) ** 4)


def born_scalar_general(Vtilde4, m: float, s_max: float, kappa_max: float, field: str = "real", s_min: float = 0.0,
                        n_s: int = 40, n_k: int = 40, n_c: int = 16, n_p: int = 16) -> dict:
    """Born pairs from a background V(t, x) of ANY space-time profile, scalar vertex, as a 4D spectral integral.

    Vtilde4(K0, Kx, Ky, Kz) = int d^4x e^{i(K0 t - K.x)} V(t, x) (arrays in, complex out); any spectrum, including
    one with timelike support (a source, a windowed profile, or a second-order background such as a product of waves):
        N = int d^4K/(2pi)^4 theta(K0) |V~(K)|^2 rho(K^2) = int ds rho(s) int d^3K/((2pi)^4 2 K0) |V~|^2.
    Quantity: dict with 'pairs' (total mean number of PAIRS, dimensionless; in-in) and 'particles' (= 2 x pairs).
    Valid when: first order in V; |V~| negligible for s > s_max or |K| > kappa_max; m > 0 (or s_min > 0); the
        Gauss grids resolve V~ (check by doubling n_s, n_k, n_c, n_p)."""
    m, s_min = float(m), float(s_min)
    if m < 0 or s_min < 0:
        raise ValueError("need m >= 0 and s_min >= 0")
    _check_massless_scalar_vertex(m, s_min)
    s_th = max(4 * m * m, s_min)
    if not s_max > s_th or not kappa_max > 0:
        raise ValueError("need s_max > max(4m^2, s_min) and kappa_max > 0")
    S, K0, Kx, Ky, Kz, W = _four_nodes(s_th, s_max, kappa_max, n_s, n_k, n_c, n_p)
    val = np.abs(np.asarray(Vtilde4(K0, Kx, Ky, Kz))) ** 2 * pair_spectral_density_scalar(S, m, field)
    N = float(np.sum(W * val))
    return {"pairs": N, "particles": 2 * N}


def born_metric_general(htilde4, s_max: float, kappa_max: float, field: str = "scalar", m: float = 0.0,
                        xi: float = 0.0, n_s: int = 40, n_k: int = 40, n_c: int = 16, n_p: int = 16) -> dict:
    """Born pairs from a metric perturbation h_{mu nu}(t, x) of ANY profile (g = eta + h), gravity vertex, 4D.

    htilde4(K0, Kx, Ky, Kz) returns lower-index h~_{mu nu}(K), shape (..., 4, 4). Feed it the Fourier transform
    of whatever effective background acts at this vertex (for example a second-order product of waves):
        N = (1/4) int d^4K/(2pi)^4 theta(K0) [rho2(K^2) X2 + rho0(K^2) X0].
    Quantity: dict with 'pairs' (total mean number of PAIRS, dimensionless; in-in), 'particles' (= 2 x pairs),
        'spin2_part', 'spin0_part'.
    Valid when: |h| << 1; spectrum negligible beyond s_max, kappa_max; field 'scalar' (m, xi) or 'photon'; the
        Gauss grids resolve h~ (check by doubling n_s, n_k, n_c, n_p)."""
    if not s_max > 4 * m * m or not kappa_max > 0:
        raise ValueError("need s_max > 4 m^2 and kappa_max > 0")
    S, K0, Kx, Ky, Kz, W = _four_nodes(4 * m * m, s_max, kappa_max, n_s, n_k, n_c, n_p)
    X2, X0 = _metric_weights(K0, Kx, Ky, Kz, np.asarray(htilde4(K0, Kx, Ky, Kz)))
    r2, r0 = stress_spectral_densities(S, field, m, xi)
    p2, p0 = float(np.sum(W * 0.25 * r2 * X2)), float(np.sum(W * 0.25 * r0 * X0))
    return {"pairs": p2 + p0, "particles": 2 * (p2 + p0), "spin2_part": p2, "spin0_part": p0}


def wave_equation_residual_planar(V_of_tz, t_range, z_range, n: int = 201) -> dict:
    """Is a planar profile V(t, z) a source-free wave? ||(d_t^2 - d_z^2) V|| / (||d_t^2 V|| + ||d_z^2 V||) on a grid.

    Every Fourier component of a solution of the free wave equation has K^2 = 0, so at first order it makes no
    massive pairs, and through the gravity vertex no massless ones either. A nonzero first-order yield therefore
    needs timelike support: a source region, a profile that is not a vacuum solution (e.g. a wave cut off in time),
    or a second-order background. This check flags the second kind so that a windowing artefact is not mistaken
    for physics.
    Quantity: dict with 'residual' (dimensionless ratio, 4th-order finite differences) and 'non_vacuum'
        (residual > 1e-3).
    Valid when: V is smooth and resolved by the n x n grid over t_range x z_range."""
    if n < 9:
        raise ValueError("need n >= 9")
    t = np.linspace(*t_range, n)
    z = np.linspace(*z_range, n)
    T, Z = np.meshgrid(t, z, indexing="ij")
    V = np.asarray(V_of_tz(T, Z), dtype=float)
    ht, hz = t[1] - t[0], z[1] - z[0]

    def d2(A, h, ax):
        A = np.moveaxis(A, ax, 0)
        out = (-A[4:] + 16 * A[3:-1] - 30 * A[2:-2] + 16 * A[1:-3] - A[:-4]) / (12 * h * h)
        return np.moveaxis(out, 0, ax)

    Vtt = d2(V, ht, 0)[:, 2:-2]
    Vzz = d2(V, hz, 1)[2:-2, :]
    res = float(np.linalg.norm(Vtt - Vzz) / max(np.linalg.norm(Vtt) + np.linalg.norm(Vzz), 1e-300))
    return {"residual": res, "non_vacuum": res > 1e-3}

# ---------------------------------------------------------------- self-test
def selftest(verbose: bool = True) -> bool:
    """Compare with closed forms and published results. Returns True if all pass."""
    results = []

    def check(name, got, want, tol, rel=False):
        err = abs(got - want) / (abs(want) if rel and want != 0 else 1.0)
        ok = bool(err <= tol)
        results.append(ok)
        if verbose:
            print(f"{'PASS' if ok else 'FAIL'}  {name}: {got:.10g} (expected {want:.10g}, "
                  f"{'rel' if rel else 'abs'} tol {tol:g})")

    # A1. Sudden frequency jump. Exact matching of u, u' at t = 0 gives
    #     |beta|^2 = (omega1 - omega2)^2/(4 omega1 omega2). The Magnus step is exact for piecewise-constant
    #     omega^2, so the step must reproduce it to roundoff; a fast tanh (width << 1/omega) to O((w width)^2).
    for w1, w2 in ((1.0, 3.0), (2.0, 0.5)):
        f, (t0, t1) = sudden_jump_omega2(w1, w2)
        r = bogoliubov_boson(lambda t, f=f: np.array([f(t)]), t0, t1, steps=200)
        check(f"sudden jump {w1}->{w2}: solver vs (w1-w2)^2/(4 w1 w2)", float(r["beta2"][0]),
              float(sudden_jump_beta2(w1, w2)), 1e-12)
    f, (t0, t1) = sudden_jump_omega2(1.0, 3.0, width=1e-3)
    r = bogoliubov_boson(lambda t: np.array([f(t)]), t0, t1, steps=4000)
    check("fast tanh (width 1e-3/omega) -> sudden limit", float(r["beta2"][0]), float(sudden_jump_beta2(1.0, 3.0)),
          1e-4, rel=True)

    # A2. The tanh model (Bernard & Duncan 1977; Birrell & Davies 1982 sec. 3.4, eq. 3.140b), solved numerically.
    k = np.linspace(0.05, 3.0, 25)
    for rho in (2.0, 0.7):
        w2f, (t0, t1) = tanh_model_omega2(k, 1.0, 2.0, 1.0, rho)
        r = bogoliubov_boson(w2f, t0, t1)
        ref = tanh_model_beta2(k, 1.0, 2.0, 1.0, rho)
        check(f"tanh model rho={rho}: max rel. error over 25 modes (all resolved)",
              float(np.max(np.abs(r["beta2"] / ref - 1))) + float(not np.all(r["resolved"])), 0.0, 1e-6)
        check(f"tanh model rho={rho}: |alpha|^2 - |beta|^2 = 1", float(r["normalisation_error"].max()), 0.0, 1e-10)

    # A3. Adiabatic limit rho -> 0: closed form -> exp(-2 pi min(w_in, w_out)/rho); the solver's precision floor.
    k1 = np.array([0.5])
    wi, wo = math.sqrt(0.25 + 1.0), math.sqrt(0.25 + 3.0)
    for rho in (0.05, 0.02):
        check(f"closed form -> exp(-2 pi w_min/rho) at rho={rho}", float(tanh_model_beta2(k1, 1, 2, 1, rho)[0]),
              float(adiabatic_limit_beta2(wi, wo, rho)), 1e-12, rel=True)
    # Five switching rates down to rho = 0.07 (exact |beta|^2 = 2.6e-44, far below double precision).
    flagged_ok, noise, last = True, None, None
    for rho in (0.5, 0.25, 0.12, 0.1, 0.07):
        w2f, (t0, t1) = tanh_model_omega2(k1, 1.0, 2.0, 1.0, rho)
        r = bogoliubov_boson(w2f, t0, t1, steps=2000, rtol=1e-6)
        ref = float(tanh_model_beta2(k1, 1, 2, 1, rho)[0])
        good = abs(r["beta2"][0] / ref - 1) < 2e-2
        flagged_ok &= bool(good) or not bool(r["resolved"][0])     # every unflagged result must be right
        noise, last = float(r["beta2"][0]), r
        if verbose:
            print(f"      rho={rho}: exact {ref:.3e}, solver {r['beta2'][0]:.3e}, floor {r['floor'][0]:.1e}, "
                  f"resolved={bool(r['resolved'][0])}")
    check("adiabatic limit: every result the solver does not flag is within 2%", float(flagged_ok), 1.0, 0)
    # At rho = 0.07 the solver returns pure noise: that IS the measured precision floor of |beta|^2.
    check("measured noise floor (rho=0.07 output) is between 1e-31 and 1e-26", float(1e-31 < noise < 1e-26), 1.0, 0)
    check("estimated floor bounds the measured noise and the result is flagged",
          float(last["floor"][0] >= noise and not last["resolved"][0]), 1.0, 0)
    try:
        bogoliubov_boson(w2f, t0, t1, strict=True)
        refused = 0.0
    except ValueError:
        refused = 1.0
    check("strict=True refuses the rho=0.07 result (exact 2.6e-44)", refused, 1.0, 0)

    # A4. Integrated spectrum against a closed-form integral: n = (1/2pi^2) int k^2 exp(-k^2) dk = 1/(8 pi^1.5).
    check("number_density_isotropic: Gaussian test integrand", number_density_isotropic(lambda kk: np.exp(-kk * kk), 12.0),
          1.0 / (8 * PI ** 1.5), 1e-12, rel=True)


    # B1/B2. Sauter pulse E(t) = E0 sech^2(t/tau), m = 1: both mode solvers against the exact occupations of
    #     Gavrilov & Gitman 1996 (hep-th/9603152) eqs. 42-43, quoted: fermions "Np,r = sinh[pi alpha/2 (2eE alpha +
    #     w- - w+)] sinh[pi alpha/2 (2eE alpha + w+ - w-)] / sinh(pi alpha w+) sinh(pi alpha w-)", scalars
    #     "Np,r = cosh^2[pi sqrt((eE alpha^2)^2 - 1/4)] + sinh^2[pi alpha/2 (w+ - w-)] / sinh(pi alpha w+) sinh(pi alpha w-)"
    #     (alpha = tau). (eE0, tau) = (0.2, 1) has eE0 tau^2 < 1/2, the cos branch of the scalar formula.
    for eE0, tau in ((0.5, 2.0), (0.2, 1.0)):
        kz = np.linspace(-1.2 * eE0 * tau, 1.2 * eE0 * tau, 9)
        kp = np.full_like(kz, 0.3)
        pf, (t0, t1) = sauter_kinetic_momentum(kz, eE0, tau)
        ep = np.sqrt(1.0 + kp * kp)
        rb = bogoliubov_boson(lambda t: ep ** 2 + pf(t) ** 2, t0, t1)
        rf = bogoliubov_fermion_efield(pf, ep, t0, t1)
        ns, nf = sauter_n_scalar(kz, kp, 1.0, eE0, tau), sauter_n_spinor(kz, kp, 1.0, eE0, tau)
        check(f"Sauter scalar QED (eE0={eE0}, tau={tau}): boson solver vs GG eq. 43, max rel. error over 9 k_par",
              float(np.max(np.abs(rb["beta2"] / ns - 1))), 0.0, 1e-6)
        check(f"Sauter spinor QED (eE0={eE0}, tau={tau}): two-level solver vs GG eq. 42, max rel. error",
              float(np.max(np.abs(rf["n"] / nf - 1))), 0.0, 1e-6)
    check("two-level solver: unitarity |<+|c>|^2 + |<-|c>|^2 = 1", float(rf["unitarity_error"].max()), 0.0, 1e-10)

    # B3. Constant-field limit, only where it applies (eE0 tau^2 >> 1, |k_par| << eE0 tau): n_k ->
    #     exp(-pi (m^2 + k_perp^2)/(eE0)) for both statistics (Kim, Lee & Yoon 2008, arXiv:0807.2696, after eq. 46:
    #     "Nk = e^-pi(m2+k2perp)/(qE)"). eE0 = 0.3, tau = 100: eE0 tau^2 = 3000; corrections O(1/(eE0 tau^2)).
    eE0, tau, kp = 0.3, 100.0, 0.3
    ref = float(schwinger_n_mode(kp, 1.0, eE0))
    check("Sauter -> Schwinger at k_par = 0 (scalar)", float(sauter_n_scalar(0.0, kp, 1.0, eE0, tau)), ref, 1e-2, rel=True)
    check("Sauter -> Schwinger at k_par = 0 (spinor)", float(sauter_n_spinor(0.0, kp, 1.0, eE0, tau)), ref, 1e-2, rel=True)
    check("...but NOT at the edge |k_par| = 1.3 eE0 tau (n_k < 1e-3 x Schwinger: limit does not apply)",
          float(sauter_n_spinor(1.3 * eE0 * tau, kp, 1.0, eE0, tau) < 1e-3 * ref), 1.0, 0)

    # B4. Schwinger: pair number versus vacuum decay, both from the SAME n_k. Cohen & McGady 2008 (arXiv:0807.1117)
    #     eq. 5: "Gamma = (qE)^2/4pi^3 exp(-pi m^2/qE) ... Remarkably it does not agree with w: the entire rate is
    #     given by the first term in the series for w"; eq. 2: "w = (qE)^2/4pi^3 sum 1/n^2 exp(-n pi m^2/qE)".
    #     Scalar: Kim, Lee & Yoon 2008 eq. 45, "Lsc_eff = ... + i (qE)^2/16pi^3 sum (-1)^(n+1)/n^2 e^(-pi m^2 n/qE)",
    #     i.e. Im L_sc; the decay rate is 2 Im L (their eq. 25: "2(Im Lsc_eff) = sum_k ln(1 + N_k)").
    for eE in (1.0, 10.0):
        x = math.exp(-PI / eE)
        for fermion in (True, False):
            r = rates_from_modes(lambda k: schwinger_n_mode(k, 1.0, eE), eE, fermion, 12.0 * math.sqrt(eE))
            tag = "spinor" if fermion else "scalar"
            pair_ref = eE * eE / (4 * PI ** 3 if fermion else 8 * PI ** 3) * x
            if fermion:
                w_ref = eE * eE / (4 * PI ** 3) * sum(x ** n / n ** 2 for n in range(1, 400))
            else:   # 2 x Im L_sc from KLY eq. 45, summed explicitly
                w_ref = 2 * eE * eE / (16 * PI ** 3) * sum((-1) ** (n + 1) * x ** n / n ** 2 for n in range(1, 400))
            check(f"{tag}, eE = {eE} m^2: pair rate from sum_k n_k = n=1 term", r["pair_rate"], pair_ref, 1e-10, rel=True)
            check(f"{tag}, eE = {eE} m^2: decay rate from sum_k ln(..n_k) = 2 Im L_eff (all n)", r["decay_rate"], w_ref,
                  1e-10, rel=True)
            check(f"{tag}, eE = {eE} m^2: decay/pair - 1 = {r['ratio'] - 1:+.4f} is resolved (|.| > 1e-3)",
                  float(abs(r["ratio"] - 1) > 1e-3 and (r["ratio"] > 1) == fermion), 1.0, 0)
            c = schwinger_closed_forms(1.0, eE, fermion)
            check(f"{tag}, eE = {eE} m^2: mpmath polylog closed form = mode sum", c["decay_rate"], r["decay_rate"], 1e-10,
                  rel=True)

    # B5. Total pairs per volume of a long Sauter pulse -> locally-constant-field integral of the PAIR rate,
    #     corrections O(1/(eE0 tau^2)) (measured 5% at tau = 30 and 0.45% at tau = 100, scaling as 1/tau^2).
    for fermion in (True, False):
        check(f"Sauter total pairs/volume -> int dt Gamma_pairs(E(t)) ({'spinor' if fermion else 'scalar'}, tau=100)",
              sauter_pairs_per_volume(1.0, 0.3, 100.0, fermion), lcfa_pairs_per_volume(1.0, 0.3, 100.0, fermion), 1e-2,
              rel=True)


    # C1. The tanh universe through the FRW module (Birrell & Davies sec. 3.4 via arXiv:2204.02786, eq. 3.133
    #     "a2(eta) = A + B tanh(rho eta)" and eq. 3.140b "|beta_k|2 = sinh2(pi w-/rho) / sinh(pi w1/rho) sinh(pi w2/rho)",
    #     conformal coupling, eta = conformal time; B&D build it in 1+1 dimensions, where conformal coupling is
    #     xi = 0; in 3+1 it is xi = 1/6 and the mode equation is the same).
    a_f, app_f, (e0, e1) = frw_tanh_scale_factor(2.0, 1.0, 0.7)
    kc = np.linspace(0.05, 3.0, 12)
    r = frw_particle_production(kc, a_f, 1.0, 1.0 / 6.0, e0, e1, a_pp=app_f)
    check("FRW tanh universe, conformal coupling: FRW module vs eq. 3.140b, max rel. error",
          float(np.max(np.abs(r["beta2"] / tanh_model_beta2(kc, 1.0, 2.0, 1.0, 0.7) - 1))), 0.0, 1e-6)

    # C2. Null result: a massless conformally coupled field is conformally invariant, so a conformally flat FRW
    #     produces nothing (omega_k = k exactly), for any a(eta). Here a lumpy, non-tanh expansion; minimal coupling
    #     in the same universe does produce particles (the a''/a term).
    def lumpy(eta):
        return 1.0 + 0.5 * (1 + np.tanh(0.8 * eta)) + 0.3 * np.exp(-((eta - 1.0) / 0.7) ** 2)
    r0 = frw_particle_production(kc, lumpy, 0.0, 1.0 / 6.0, -40.0, 40.0)
    check("FRW null: m = 0, xi = 1/6 gives max |beta_k|^2 = 0 (below 1e-25)", float(r0["beta2"].max() < 1e-25), 1.0, 0)
    r1 = frw_particle_production(kc, lumpy, 0.0, 0.0, -40.0, 40.0)
    check("same universe, minimal coupling: production is nonzero and resolved (max |beta|^2 > 1e-4)",
          float(r1["beta2"].max() > 1e-4 and np.all(r1["resolved"][kc < 1.5])), 1.0, 0)
    # minimal coupling, tanh universe: analytic a'' and the finite-difference a'' agree
    ra = frw_particle_production(kc, a_f, 1.0, 0.0, e0, e1, a_pp=app_f)
    rf = frw_particle_production(kc, a_f, 1.0, 0.0, e0, e1)
    check("FRW minimal coupling: finite-difference a'' matches analytic a'' (max rel.)",
          float(np.max(np.abs(rf["beta2"] / ra["beta2"] - 1))), 0.0, 1e-5)


    # D1. Spectral densities from the explicit vertices (angular quadrature of <p1 p2|T^{mu nu}|0>, conservation
    #     K_mu t^{mu nu} = 0 checked) against the analytic forms in stress_spectral_densities.
    for s_, fld, m_, xi_ in ((9.0, "scalar", 0.7, 0.0), (9.0, "scalar", 0.7, 0.3), (4.0, "photon", 0.0, 0.0)):
        r2n, r0n, viol = _stress_spectral_numeric(s_, fld, m_, xi_)
        r2a, r0a = stress_spectral_densities([s_], fld, m_, xi_)
        check(f"{fld} (m={m_}, xi={xi_}): rho2, rho0 by explicit vertices = analytic (max rel.; conservation)",
              max(abs(r2n / r2a[0] - 1), abs(r0n - r0a[0]) / max(abs(r0a[0]), r2a[0]), viol), 0.0, 1e-10)
    #     Redi & Tesi 2026 (arXiv:2606.28297) eq. 5, "Ndec = 2 Im Gamma_1PI = - cJ/30720pi int d4q/(2pi)4 theta(q2)
    #     h Pi h", with "c0 = 4/3, c1/2 = 4 and c1 = 16" (conformal scalar, Weyl fermion, gauge field). For a TT h in
    #     the rest frame h Pi h = -6 s^2 |h|^2, and theta(q^2) covers both light cones (equal for real h), so per
    #     positive-frequency cone the kernel of N in |h|^2 is 2 x 6 c s^2/30720 pi = c s^2/2560 pi = rho2/4.
    for fld, cJ in (("scalar", 4.0 / 3.0), ("photon", 16.0)):
        r2a, _ = stress_spectral_densities([2.0], fld)
        check(f"{fld}: rho2/4 = c s^2/(2560 pi) with Redi-Tesi c = {cJ:g}", float(r2a[0] / 4), cJ * 4.0 / (2560 * PI), 1e-14,
              rel=True)
    check("collinear phase space survives for massless pairs: rho_phi2(s -> 0+) = 1/(16 pi) ...",
          float(pair_spectral_density_scalar([1e-12], 0.0)[0]), 1 / (16 * PI), 1e-12, rel=True)
    check("... but the gravity vertex vanishes there: rho2(s -> 0+)/s^2 finite, rho2 -> 0",
          float(stress_spectral_densities([1e-12], "photon")[0][0]), 0.0, 1e-25)

    # D2. Cross-check with the exact mode solver (Part A) for homogeneous backgrounds, weak field. Born is
    #     O(eps^2) exact; the next term is O(eps^3) or O(eps^4), so the relative difference must scale with eps.
    #     f(t) = exp(-t^2/(2 tau^2)), tau = 0.3, m = 1 (units of m).
    tau_ = 0.3
    fg = lambda t: np.exp(-t ** 2 / (2 * tau_ ** 2))    # noqa: E731
    devs = []
    for eps in (0.05, 0.1):
        def b2(k, eps=eps):
            return bogoliubov_boson(lambda t: k * k + 1.0 + eps * fg(t), -12 * tau_, 12 * tau_, rtol=1e-6)["beta2"]
        ex = number_density_isotropic(b2, 12.0, n=48)
        bo = born_scalar_homogeneous(lambda t, eps=eps: eps * fg(t), -12 * tau_, 12 * tau_, 1.0, 30.0)["particles_per_volume"]
        devs.append(abs(ex / bo - 1))
        check(f"scalar vertex V = eps f(t), eps = {eps} m^2: |exact/Born - 1| <= 0.6 eps", devs[-1], 0.0, 0.6 * eps)
    check("scalar vertex: deviation halves when eps halves (ratio in [1.6, 2.4])", devs[1] / devs[0], 2.0, 0.4)
    devs = []
    for eps in (0.05, 0.1):    # FRW, minimal coupling: a = 1 + eps f(eta), h = 2 eps f eta_{mu nu}: trace channel only
        b2 = lambda k, eps=eps: frw_particle_production(k, lambda e: 1 + eps * fg(e), 1.0, 0.0, -12 * tau_, 12 * tau_,   # noqa: E731
                                                        rtol=1e-6)["beta2"]
        ex = number_density_isotropic(b2, 12.0, n=48)

        def hfrw(t, eps=eps):
            out = np.zeros((len(t), 4, 4))
            for i, sg in enumerate((1, -1, -1, -1)):
                out[:, i, i] = sg * 2 * eps * fg(t)
            return out
        bo = born_metric_homogeneous(hfrw, -12 * tau_, 12 * tau_, 30.0, "scalar", 1.0, 0.0)
        devs.append(abs(ex / bo["particles_per_volume"] - 1))
        check(f"FRW a = 1 + eps f, minimal coupling, eps = {eps}: gravity-vertex Born (spin 0) vs mode solver, <= 1.5 eps",
              devs[-1], 0.0, 1.5 * eps)
    check("FRW: deviation scales with eps (ratio in [1.6, 2.4]); spin-2 part exactly 0", devs[1] / devs[0]
          + 10 * abs(bo["spin2_part"]) / bo["pairs_per_volume"], 2.0, 0.4)
    #     Bianchi I, ds^2 = dt^2 - e^{2 eps f} dx^2 - e^{-2 eps f} dy^2 - dz^2 (sqrt(-g) = 1, so the mode equation
    #     omega^2 = m^2 + kx^2 e^{-2 eps f} + ky^2 e^{2 eps f} + kz^2 is exact); spin-2 channel only. m = 0.5.
    kk, wk = _gauss_legendre(0, 14.0, 28)
    cc, wc = _gauss_legendre(0, 1, 6)
    pp, wp = _gauss_legendre(0, PI / 2, 6)
    KK, CC, PP = np.meshgrid(kk, cc, pp, indexing="ij")
    SS = np.sqrt(1 - CC * CC)
    kx2, ky2, kz2 = ((KK * SS * np.cos(PP)) ** 2).ravel(), ((KK * SS * np.sin(PP)) ** 2).ravel(), ((KK * CC) ** 2).ravel()
    Wb = (np.einsum("i,j,k->ijk", wk * kk * kk, wc, wp) * 8 / (2 * PI) ** 3).ravel()
    devs = []
    for eps in (0.05, 0.1):
        r = bogoliubov_boson(lambda t, eps=eps: 0.25 + kx2 * math.exp(-2 * eps * fg(t)) + ky2 * math.exp(2 * eps * fg(t)) + kz2,
                             -12 * tau_, 12 * tau_, rtol=1e-5)
        ex = float(np.sum(Wb * r["beta2"]))

        def hb(t, eps=eps):
            out = np.zeros((len(t), 4, 4))
            out[:, 1, 1], out[:, 2, 2] = -2 * eps * fg(t), 2 * eps * fg(t)
            return out
        bo = born_metric_homogeneous(hb, -12 * tau_, 12 * tau_, 40.0, "scalar", 0.5, 0.0)
        devs.append(abs(ex / bo["particles_per_volume"] - 1))
        check(f"Bianchi I eps = {eps}: gravity-vertex Born (spin 2, rho2 = s^2 beta^5/480pi) vs exact modes, <= eps^2",
              devs[-1], 0.0, eps * eps)
    check("Bianchi I: deviation is O(eps^2) (ratio for eps doubling in [3, 5])", devs[1] / devs[0], 4.0, 1.0)

    # D3. Plane waves and packets, planar (t, z) backgrounds, m = 1 unless stated. A free packet F(t - z) has all its
    #     support on K^2 = 0; cutting it off in time with W(t) = exp(-t^2/2T^2) makes it NOT a vacuum solution
    #     (flagged), with timelike support of width 1/T. Exact transform: V~ = W~(K0 - Kz) F~(Kz).
    sg_, Om_ = 2.0, 4.0
    Fu = lambda u: np.exp(-u * u / (2 * sg_ ** 2)) * np.cos(Om_ * u)     # noqa: E731
    Fk = lambda k: math.sqrt(2 * PI) * sg_ / 2 * (np.exp(-(k - Om_) ** 2 * sg_ ** 2 / 2) + np.exp(-(k + Om_) ** 2 * sg_ ** 2 / 2))  # noqa: E731
    Wk = lambda q_, T: math.sqrt(2 * PI) * T * np.exp(-q_ * q_ * T * T / 2)  # noqa: E731
    res_free = wave_equation_residual_planar(lambda t, z: Fu(t - z), (-6, 6), (-6, 6))
    res_win = wave_equation_residual_planar(lambda t, z: Fu(t - z) * np.exp(-t * t / 18.0), (-6, 6), (-6, 6))
    check("free packet F(t - z): wave-equation residual < 1e-6 (a vacuum solution, not flagged)",
          float(res_free["residual"] < 1e-6 and not res_free["non_vacuum"]), 1.0, 0)
    check("same packet cut off in time (T = 3): flagged as not a vacuum solution", float(res_win["non_vacuum"]), 1.0, 0)
    #     Massive yield of the windowed packet falls like exp(-(2 m^2 T/Kz)^2) (s = (K0 - Kz)(K0 + Kz) >= 4 m^2 needs
    #     K0 - Kz >= 2 m^2/Kz, a Gaussian tail of W~): measured 4.9e-3, 1.3e-11, 1.2e-28 at T = 1, 10, 20.
    Ns = [born_scalar_planar(lambda K0, Kz, T=T: Wk(K0 - Kz, T) * Fk(Kz), 1.0, 200.0, 8.0)["pairs_per_area"]
          for T in (1.0, 10.0, 20.0)]
    check(f"massive pairs from a time-windowed packet: nonzero at T = 1 ({Ns[0]:.3g}) but -> 0 as T grows "
          f"(T = 20: {Ns[2]:.2g}): the free packet gives zero", float(Ns[0] > 1e-3 and Ns[1] < 1e-6 * Ns[0]
                                                                     and Ns[2] < 1e-20 * Ns[0]), 1.0, 0)
    #     Gravitational plane wave h_xx = -h_yy = F(t - z) W(t): massless pairs keep collinear phase space, but the
    #     vertex vanishes as s^2, so the yield of the windowed wave falls like 1/T (Gibbons 1975, Commun. Math. Phys.
    #     45, 191, abstract: "the time varying gravitational field of the wave produces no particles"; the exact
    #     statement is for a massive scalar, the massless case being its m^2 = 0 limit).
    def h_plane(T):
        def h(K0, Kz):
            out = np.zeros(K0.shape + (4, 4), dtype=complex)
            amp = Wk(K0 - Kz, T) * Fk(Kz)
            out[..., 1, 1], out[..., 2, 2] = amp, -amp
            return out
        return h
    for fld in ("scalar", "photon"):
        N5 = born_metric_planar(h_plane(5.0), 100.0, 8.0, fld)["pairs_per_area"]
        N20 = born_metric_planar(h_plane(20.0), 100.0, 8.0, fld)["pairs_per_area"]
        check(f"massless {fld} pairs from a windowed gravitational plane wave: N(T=20)/N(T=5) = 1/4 (vertex ~ s^2)",
              N20 / N5, 0.25, 0.05)
    Nm10 = born_metric_planar(h_plane(10.0), 200.0, 8.0, "scalar", 1.0)["pairs_per_area"]
    Nm20 = born_metric_planar(h_plane(20.0), 200.0, 8.0, "scalar", 1.0)["pairs_per_area"]
    check(f"massive scalar pairs from the windowed gravitational wave: no phase space as T grows "
          f"(T = 10: {Nm10:.2g}, T = 20: {Nm20:.2g}; massless at T = 20: {N20:.2g})",
          float(Nm10 < 1e-10 * N20 and Nm20 < 1e-15 * Nm10), 1.0, 0)
    #     Timelike support from a SOURCE region: V solves (d_t^2 - d_z^2) V = J for a localized J, so
    #     V~ = -J~/K^2 off the light cone. J = exp(-t^2/2 - z^2/2): J~ = 2 pi exp(-(K0^2 + Kz^2)/2).
    Nsrc = born_scalar_planar(lambda K0, Kz: 2 * PI * np.exp(-(K0 * K0 + Kz * Kz) / 2) / (K0 * K0 - Kz * Kz), 1.0, 200.0, 6.0)
    Nsrc2 = born_scalar_planar(lambda K0, Kz: 2 * PI * np.exp(-(K0 * K0 + Kz * Kz) / 2) / (K0 * K0 - Kz * Kz), 1.0, 200.0, 6.0,
                               n_s=640, n_y=640)
    check(f"source region: nonzero, converged yield ({Nsrc['pairs_per_area']:.4g} pairs per unit area)",
          float(Nsrc["pairs_per_area"] > 1e-6 and abs(Nsrc2["pairs_per_area"] / Nsrc["pairs_per_area"] - 1) < 1e-6), 1.0, 0)
    #     Second order in the wave: the product of counter-propagating free packets F(t - z) F(t + z) (a stand-in for
    #     any term quadratic in the wave) has K = k1 + k2 timelike: V~ = (1/2) F~((K0 + Kz)/2) F~((K0 - Kz)/2).
    #     (Two co-propagating waves stay on the light cone: their product is still a function of t - z.)
    N2 = born_scalar_planar(lambda K0, Kz: 0.5 * Fk((K0 + Kz) / 2) * Fk((K0 - Kz) / 2), 1.0, 400.0, 6.0)["pairs_per_area"]
    res2 = wave_equation_residual_planar(lambda t, z: Fu(t - z) * Fu(t + z), (-6, 6), (-6, 6))
    check(f"second order (counter-propagating product): nonzero ({N2:.4g}), and flagged as sourced, not free",
          float(N2 > 1e-3 and res2["non_vacuum"]), 1.0, 0)
    #     Independent check of the planar integrator in light-cone variables a = (K0 + Kz)/2, b = (K0 - Kz)/2:
    #     s = 4ab, dK0 dKz = 2 da db, so N/A = (1/8 pi^2) int_0^inf int_0^inf da db |F~(a)|^2 |F~(b)|^2 rho(4ab).
    aa, wa = _gauss_legendre(0.0, 12.0, 400)
    A_, B_ = np.meshgrid(aa, aa, indexing="ij")
    lc = float(np.einsum("i,j,ij->", wa, wa, np.abs(Fk(A_)) ** 2 * np.abs(Fk(B_)) ** 2
                         * pair_spectral_density_scalar(4 * A_ * B_, 1.0))) / (8 * PI * PI)
    check("planar integrator (s, rapidity) = light-cone double integral for the separable second-order background",
          N2, lc, 1e-6, rel=True)

    # D4. The general 4D spectral integral against an INDEPENDENT 6D pair-momentum integral (reduced to 3D by
    #     isotropy): V = exp(-t^2/2T^2 - r^2/2R^2) cos(Om t), real scalar, m = 1, T = R = 1, Om = 3:
    #     N = (1/2) int d^3p1 d^3p2 / ((2pi)^6 4 E1 E2) |V~(E1 + E2, p1 + p2)|^2.
    def V4(K0, Kx, Ky, Kz):
        k2 = Kx * Kx + Ky * Ky + Kz * Kz
        return (2 * PI) ** 2 * np.exp(-k2 / 2) * 0.5 * (np.exp(-(K0 - 3.0) ** 2 / 2) + np.exp(-(K0 + 3.0) ** 2 / 2))
    gen = born_scalar_general(V4, 1.0, 80.0, 8.0, n_c=8, n_p=4)["pairs"]
    p1, w1 = _gauss_legendre(0, 8, 48)
    c12, w12 = np.polynomial.legendre.leggauss(32)
    P1, P2, C12 = np.meshgrid(p1, p1, c12, indexing="ij")
    E1, E2 = np.sqrt(1 + P1 ** 2), np.sqrt(1 + P2 ** 2)
    Kn = np.sqrt(P1 ** 2 + P2 ** 2 + 2 * P1 * P2 * C12)
    integrand = np.abs(V4(E1 + E2, Kn, 0 * Kn, 0 * Kn)) ** 2 * P1 ** 2 * P2 ** 2 / (4 * E1 * E2)
    direct = 0.5 * 4 * PI * 2 * PI * float(np.einsum("i,j,k,ijk->", w1, w1, w12, integrand)) / (2 * PI) ** 6
    check("general 4D spectral form = direct 6D pair-momentum integral", gen, direct, 1e-6, rel=True)
    #     ...and the general gravity vertex in every frame: h = 2 eps f(x) eta_{mu nu} with xi = 1/6 couples only through
    #     the trace, T^mu_mu = -m^2 phi^2, so it must equal the scalar vertex with V = 2 eps m^2 f.
    def h4(K0, Kx, Ky, Kz):
        return V4(K0, Kx, Ky, Kz)[..., None, None] * (2 * 0.01) * _ETA
    gm = born_metric_general(h4, 80.0, 8.0, "scalar", 1.0, 1.0 / 6.0, n_c=8, n_p=4)
    gs = born_scalar_general(lambda *K: 2 * 0.01 * V4(*K), 1.0, 80.0, 8.0, n_c=8, n_p=4)
    check("general gravity vertex, conformally flat h, xi = 1/6 = scalar vertex with V = 2 eps m^2 f", gm["pairs"],
          gs["pairs"], 1e-10, rel=True)

    passed = all(results)
    if verbose:
        print(f"\n{sum(results)}/{len(results)} checks passed")
    return passed


def _convergence() -> int:
    """Slow convergence studies (not part of the self-test): mode-solver floor vs steps, Born grids."""
    k1 = np.array([0.5])
    print("Mode solver, tanh model k = 0.5, m = 1, A = 2, B = 1: |beta|^2 and floor vs fixed step count")
    for rho in (0.25, 0.12, 0.07):
        w2f, (t0, t1) = tanh_model_omega2(k1, 1.0, 2.0, 1.0, rho)
        ref = float(tanh_model_beta2(k1, 1, 2, 1, rho)[0])
        for n in (1000, 4000, 16000, 64000):
            r = bogoliubov_boson(w2f, t0, t1, steps=n, max_steps=2 * n, rtol=1.0)
            print(f"  rho={rho}: steps {r['steps']:6d}: |beta|^2 = {r['beta2'][0]:.4e} (exact {ref:.4e}), "
                  f"floor {r['floor'][0]:.1e}, resolved {bool(r['resolved'][0])}")
    print("Born planar, windowed packet T = 3, m = 1: pairs per area vs (y_max, grid)")
    Fk = lambda k: math.sqrt(2 * PI) * (np.exp(-(k - 4.0) ** 2 * 2) + np.exp(-(k + 4.0) ** 2 * 2))  # noqa: E731
    for ym, n in ((6.0, 80), (8.0, 80), (8.0, 160), (8.0, 320), (10.0, 320), (12.0, 640)):
        N = born_scalar_planar(lambda K0, Kz: math.sqrt(2 * PI) * 3 * np.exp(-(K0 - Kz) ** 2 * 4.5) * Fk(Kz), 1.0, 300.0, ym,
                               n_s=n, n_y=n)["pairs_per_area"]
        print(f"  y_max {ym}, n {n}: {N:.8g}")
    return 0


# ---------------------------------------------------------------- command line
def _energy(text: str) -> float:
    """Parse an energy ('0.511 MeV' -> eV) or a bare number (already in the chosen natural unit)."""
    try:
        return float(text)
    except ValueError:
        from unit_tools import Q
        return Q(text).expect("energy").si / E_CHARGE


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("selftest")
    tp = sub.add_parser("tanh", help="tanh model omega^2 = k^2 + m^2 (A + B tanh rho t): solver vs closed form")
    for name in ("m", "rho", "k"):
        tp.add_argument(f"--{name}", required=True, help="energy: a number in your natural unit, or e.g. '1 eV'")
    tp.add_argument("--A", type=float, required=True)
    tp.add_argument("--B", type=float, required=True)
    sp = sub.add_parser("schwinger", help="constant field: pair-number rate vs vacuum-decay rate, from the same n_k")
    sp.add_argument("--m", default="0.51099895 MeV", help="mass, e.g. '0.511 MeV' (default: electron)")
    sp.add_argument("--E", required=True, help="field, e.g. '1e18 V/m'")
    sp.add_argument("--scalar", action="store_true", help="scalar QED instead of spinor QED")
    pp = sub.add_parser("sauter", help="Sauter pulse E0 sech^2(t/tau): exact pairs per volume vs locally-constant-field")
    pp.add_argument("--m", default="0.51099895 MeV")
    pp.add_argument("--E", required=True, help="peak field, e.g. '5e17 V/m'")
    pp.add_argument("--tau", required=True, help="pulse time scale, e.g. '1e-20 s'")
    pp.add_argument("--scalar", action="store_true")
    gp = sub.add_parser("gwpacket", help="Born pairs per unit area from a gravitational plane-wave packet cut off in time "
                                         "(units: the packet's carrier frequency = 4, width 2)")
    gp.add_argument("--field", default="photon", choices=("photon", "scalar"))
    gp.add_argument("--m", type=float, default=0.0, help="scalar mass in the same units (photons: 0)")
    gp.add_argument("--T", type=float, nargs="+", default=[5.0, 20.0, 80.0], help="time-window widths")
    sub.add_parser("convergence", help="slow studies: mode-solver precision floor vs steps, Born grid convergence")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "selftest":
            return 0 if selftest() else 1
        if args.cmd == "convergence":
            return _convergence()
        if args.cmd == "gwpacket":
            sg_, Om_ = 2.0, 4.0
            print(f"h_xx = -h_yy = exp(-u^2/(2*{sg_}^2)) cos({Om_} u) exp(-t^2/(2T^2)), u = t - z: a free packet cut off in time")
            for T in args.T:
                res = wave_equation_residual_planar(lambda t, z: np.exp(-(t - z) ** 2 / (2 * sg_ ** 2)) * np.cos(Om_ * (t - z))
                                                    * np.exp(-t * t / (2 * T * T)), (-3 * T, 3 * T), (-3 * T, 3 * T), 401)

                def h(K0, Kz, T=T):
                    out = np.zeros(K0.shape + (4, 4), dtype=complex)
                    amp = (math.sqrt(2 * PI) * T * np.exp(-(K0 - Kz) ** 2 * T * T / 2) * math.sqrt(2 * PI) * sg_ / 2
                           * (np.exp(-(Kz - Om_) ** 2 * sg_ ** 2 / 2) + np.exp(-(Kz + Om_) ** 2 * sg_ ** 2 / 2)))
                    out[..., 1, 1], out[..., 2, 2] = amp, -amp
                    return out
                N = born_metric_planar(h, 200.0, 8.0, args.field, args.m)["pairs_per_area"]
                print(f"T = {T:8.3g}: mean pairs per unit transverse area {N:.4g} (natural units); wave-equation residual "
                      f"{res['residual']:.2g} -> {'NOT a vacuum solution (yield is a windowing effect)' if res['non_vacuum'] else 'vacuum'}")
            print("A free packet is the T -> infinity limit: the yield goes to zero (like 1/T for massless pairs).")
            return 0
        if args.cmd == "tanh":
            m, rho, k = _energy(args.m), _energy(args.rho), _energy(args.k)
            w2f, (t0, t1) = tanh_model_omega2([k], m, args.A, args.B, rho)
            r = bogoliubov_boson(w2f, t0, t1)
            ref = float(tanh_model_beta2([k], m, args.A, args.B, rho)[0])
            print(f"omega_in = {r['omega_in'][0]:.6g}, omega_out = {r['omega_out'][0]:.6g} (same unit as m)")
            print(f"|beta_k|^2 (mean particles in mode k, in-in): solver {r['beta2'][0]:.10g}, closed form {ref:.10g}")
            print(f"precision floor {r['floor'][0]:.2g}; resolved = {bool(r['resolved'][0])}; steps {r['steps']}")
            return 0
        from unit_tools import Q
        m = _energy(args.m)
        eE = eE_from_field_SI(Q(args.E).expect("V/m").si)
        fermion = not args.scalar
        tag = "spinor" if fermion else "scalar"
        if args.cmd == "schwinger":
            r = rates_from_modes(lambda k: schwinger_n_mode(k, m, eE), eE, fermion, 12 * math.sqrt(eE) + 12 * m)
            c = schwinger_closed_forms(m, eE, fermion)
            print(f"{tag} QED, m = {m:.6g} eV, eE = {eE:.6g} eV^2 = {eE / m**2:.4g} m^2")
            print(f"pair-number rate (mean pairs per volume per time) Gamma = {r['pair_rate']:.6g} eV^4 = "
                  f"{rate_density_to_SI(r['pair_rate']):.6g} m^-3 s^-1  (closed form {c['pair_rate']:.6g} eV^4)")
            print(f"vacuum-decay rate w = 2 Im L_eff = {r['decay_rate']:.6g} eV^4 = {rate_density_to_SI(r['decay_rate']):.6g}"
                  f" m^-3 s^-1  (closed form {c['decay_rate']:.6g} eV^4); w/Gamma = {r['ratio']:.6f}")
        else:
            tau = time_to_inverse_eV(Q(args.tau).expect("time").si)
            n = sauter_pairs_per_volume(m, eE, tau, fermion)
            l = lcfa_pairs_per_volume(m, eE, tau, fermion)
            print(f"{tag} QED, m = {m:.6g} eV, eE0 = {eE:.6g} eV^2, tau = {tau:.6g} /eV, eE0 tau^2 = {eE * tau * tau:.4g}")
            print(f"exact pairs per volume {n:.6g} eV^3 = {density_to_SI(n):.6g} m^-3; locally-constant-field "
                  f"{l:.6g} eV^3 (ratio {n / l if l > 0 else float('nan'):.4g})")
    except (ValueError, KeyError) as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
