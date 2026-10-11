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

Command line (from the project root)
    python3 .claude/skills/conundrum/scripts/qft_production.py selftest
    python3 .claude/skills/conundrum/scripts/qft_production.py tanh --m 1 --A 2 --B 1 --rho 0.5 --k 0.5
    python3 .claude/skills/conundrum/scripts/qft_production.py schwinger --E "1.32e18 V/m"            (electron default)
    python3 .claude/skills/conundrum/scripts/qft_production.py sauter --E "3e17 V/m" --tau "1e-19 s" --scalar
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
        converged = bool(np.all(err[above] <= rtol * np.abs(b2[above]))) if np.any(above) else True
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
        converged = bool(np.all(err[above] <= rtol * np.abs(b2[above]))) if np.any(above) else True
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

    passed = all(results)
    if verbose:
        print(f"\n{sum(results)}/{len(results)} checks passed")
    return passed


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
    args = ap.parse_args(argv)
    try:
        if args.cmd == "selftest":
            return 0 if selftest() else 1
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
