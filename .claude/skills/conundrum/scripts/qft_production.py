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

Command line (from the project root)
    python3 .claude/skills/conundrum/scripts/qft_production.py selftest
    python3 .claude/skills/conundrum/scripts/qft_production.py tanh --m 1 --A 2 --B 1 --rho 0.5 --k 0.5
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
    args = ap.parse_args(argv)
    try:
        if args.cmd == "selftest":
            return 0 if selftest() else 1
        m, rho, k = _energy(args.m), _energy(args.rho), _energy(args.k)
        w2f, (t0, t1) = tanh_model_omega2([k], m, args.A, args.B, rho)
        r = bogoliubov_boson(w2f, t0, t1)
        ref = float(tanh_model_beta2([k], m, args.A, args.B, rho)[0])
        print(f"omega_in = {r['omega_in'][0]:.6g}, omega_out = {r['omega_out'][0]:.6g} (same unit as m)")
        print(f"|beta_k|^2 (mean particles in mode k, in-in): solver {r['beta2'][0]:.10g}, closed form {ref:.10g}")
        print(f"precision floor {r['floor'][0]:.2g}; resolved = {bool(r['resolved'][0])}; steps {r['steps']}")
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
