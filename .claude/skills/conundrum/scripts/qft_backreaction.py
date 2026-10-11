#!/usr/bin/env python3
"""qft_backreaction: semiclassical (mean-field) back-reaction of pair production on a homogeneous
electric field in 1+1 dimensions, for Dirac fermions (spinor QED2) and charged scalars (scalar QED2),
with every function saying exactly WHICH quantity it returns (numpy + mpmath, no scipy).

Why this tool exists
    qft_production.py Part B computes pair production in a PRESCRIBED field. Once the produced pairs
    carry a current comparable to the displacement current, the field itself changes: it is screened,
    decays, and then oscillates (plasma oscillations). Here the field obeys Maxwell's equation driven by
    the renormalized in-in current of the quantum modes, which are evolved exactly in the self-consistent
    field. The traps are the same as in qft_production (in-in vs in-out, pairs vs particles, real
    production vs transient vacuum polarization, pair-number rate vs vacuum-decay rate) plus one more:
    a cutoff on CANONICAL momentum breaks gauge invariance and produces a spurious current e^2 A/pi.

Units (read this first)
    Natural units hbar = c = 1, Heaviside-Lorentz electromagnetism (e^2 = 4 pi alpha in 3+1, as in
    qft_production). In 1+1 dimensions the charge e has the dimension of a mass, and so does the field
    E; eE is a mass^2, the current j a mass^2, an energy per length a mass^2, pairs per length a mass,
    times are 1/mass. Pick ONE mass unit (e.g. the fermion mass m, or eV) for every input. Otto et al.
    (2019) define the 1+1 coupling constant alpha = e^2/(4 pi m^2). The command line accepts energies
    through unit_tools.Q ("0.511 MeV") and converts the results to s and m^-1 (length_density_to_SI).
    Like qft_production, this deviates from schemas.md's "SI in the Python API" on purpose: a 1+1-dimensional
    model has no SI field strength; the helpers convert densities and times.

Model (1+1 dimensions, field along x, temporal gauge, E(t) = -dA/dt)
    Modes are labelled by the canonical momentum k; the kinetic momentum is p(t) = k - e A(t)
    (dp/dt = eE), omega_k = sqrt(p^2 + m^2). The field obeys Maxwell's equation in 1+1,
        dE/dt = dE_ext/dt - j(t),     dA/dt = -E,
    with E_ext an optional external (prescribed) field and j the renormalized in-in current.
    * Spinor QED2: per k the Dirac equation is the two-level problem i dc/dt = (p sigma_z + m sigma_x) c
      (one 2-component spinor per k: in 1+1 there is no spin degeneracy, g = 1); it is
      qft_production.bogoliubov_fermion_efield with eps_perp = m. The mode that was the negative-energy
      (Dirac-sea) state at t0 is evolved as a Bloch vector s = c^dag sigma c, ds/dt = 2 b x s,
      b = (m, 0, p), n = b/omega. Adiabatic (zeroth-order) occupation f_k = (1 + n.s)/2 = |s + n|^2/4
      (= |beta_k|^2 of Otto et al.). Current and energy (Otto, Graeveling & Kaempfer 2019, eqs. 8 and 10):
          j = e int dk/2pi (s_z + p/omega) = 2e int dk/2pi [f_k p/omega - Re(alpha* beta) m/omega],
          energy per length = E^2/2 + int dk/2pi 2 omega f_k   (conserved when E_ext = None).
    * Scalar QED2: mode functions u_k'' + omega_k^2 u_k = 0, vacuum u = e^{-i omega t}/sqrt(2 omega)
      (Wronskian u u*' - u* u' = i); f_k = (omega/2)|u - i u'/omega|^2 (= |beta_k|^2, extracted directly);
          j = 2e int dk/2pi p (|u|^2 - 1/(2 omega)),  energy per length = E^2/2 + int dk/2pi 2 omega f_k.
    Renormalization: the zeroth-order adiabatic vacuum (s_z = -p/omega, |u|^2 = 1/(2 omega)) is
    subtracted mode by mode. Its integral vanishes over any window SYMMETRIC IN KINETIC MOMENTUM, so this
    is the gauge-invariant kinetic-momentum cutoff (Lambda -> infinity), not a canonical one. A cutoff
    |k| < Lambda on canonical momentum instead gives the vacuum a current -e int dk/2pi p/omega = e^2 A/pi
    (spinor), which is not gauge invariant and destroys the anomaly (selftest). In 1+1 no charge
    renormalization is needed: after the subtraction the integrand falls as p^-5 (spinor) or p^-3
    (scalar). A finite grid misses the polarization of the modes beyond it; 'chi_tail' reports that
    missing static susceptibility (scalar: about e^2/(8 pi K^2) for a grid reaching |p| = K).
    Initial state: the zeroth-order adiabatic vacuum of A(t0). If E(t0) != 0 the field is switched on
    suddenly at t0: the initial-value problem of Kluger et al. (1992) and Hebenstreit et al. (2013).

Closed forms (references for the self-test, and useful on their own)
    * Massless Schwinger model: as m -> 0 the anomaly makes the current exactly j = -(e^2/pi)(A - A0),
      so E(t) oscillates harmonically at mu = e/sqrt(pi) at ANY amplitude (schwinger_boson_mass).
    * One-loop vacuum susceptibility (P = chi E, Laplace variable s), a = sqrt(4 m^2 + s^2):
          spinor  chi_F(s) = (e^2/(2 pi s^2)) [2 - (8 m^2/(s a)) artanh(s/a)]
          scalar  chi_S(s) = (e^2/(2 pi)) [(2/(s a)) artanh(s/a) - (2 - (8 m^2/(s a)) artanh(s/a))/s^2]
      (derived here from the linearized mode equations; the self-test checks them against direct quadrature
      of the mode integral and against the full nonlinear solver at small amplitude).
      Static limit: epsilon = 1 + e^2/(6 pi m^2) (spinor), 1 + e^2/(12 pi m^2) (scalar); m -> 0 spinor:
      chi_F -> e^2/(pi s^2), i.e. the photon mass mu^2 = e^2/pi.
    * Constant field, no back-reaction: pairs per length per time Gamma = (eE/2pi) exp(-pi m^2/eE)
      (Hebenstreit, Berges & Gelfand 2013, eq. 70) for both fields; vacuum-decay rate per length
      w = -(eE/2pi) ln(1 - e^{-pi m^2/eE}) (spinor), +(eE/2pi) ln(1 + e^{-pi m^2/eE}) (scalar).
    * Transient polarization: while a weak, slowly varying field is on, the zeroth-order adiabatic
      number is n_pol = 3 (eE)^2/(256 m^3) (spinor), (eE)^2/(256 m^3) (scalar) per length: NOT pairs.

Numerics
    Poisson splitting of H = E^2/2 + H_matter(A): drift A at fixed E (with E_ext integrated by 3-point
    Gauss-Legendre), then evolve every mode EXACTLY at frozen A (a rotation for the Bloch vector or the
    oscillator) while E changes by minus the exactly integrated current; Yoshida's 4th-order composition
    of symmetric steps; the error is O(dt^4) and energy is conserved to it (no secular drift). Modes on a
    uniform canonical-momentum grid (or any nodes and weights you pass). A uniform grid of spacing dk is
    EXACTLY the problem on a ring of circumference L = 2 pi/dk: pair members separate by up to 2(t - t0),
    and the mode sum aliases once that exceeds L (Poisson summation), so the infinite-line answer needs
    t - t0 <= pi/dk (enforced unless finite_ring=True). The solver REFUSES (ValueError) runs whose pairs
    reached the grid edges, whose energy drifted (step too large) or whose omega_max dt exceeds 1.5.

Quantities (the traps)
    E(t), A(t), j(t): in-in expectation values, basis independent, gauge invariant (A up to a constant).
    pairs(t) = int dk/2pi f_k: mean number of PAIRS per unit length (one electron + one positron; for
    the scalar one particle + one antiparticle; no factor 1/2, as for any charged field), counted in the
    zeroth-order adiabatic basis. While the field is on this is basis dependent and contains transient
    vacuum polarization (adiabatic_polarization_pairs); it is a physical pair number only once the field
    is off or slowly varying. f_k: the same per mode k.

Assumptions and validity range
    Mean field (semiclassical) approximation: the classical E couples to the expectation value of the
    current; photon fluctuations, collisions and 1/N corrections are neglected. Homogeneous field in
    1+1 dimensions. For the massless spinor the mean-field equations are exact (the bosonized Schwinger
    model is free); for m > 0 they miss confinement (Gold et al. 2021 interpret the produced states as
    mesons). m > 0 for both fields (m -> 0 is reached smoothly for the spinor). 3+1 QED is NOT covered.

Python usage
    import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
    import qft_backreaction as br
    r = br.qed2_backreaction(m=1.0, e=1.0, E0=3.0, t_end=40.0, field="spinor", k_max=40.0, dk=0.075)   # ~2 s
    r["E"], r["pairs"], r["energy_drift"]                 # field, pairs per length, energy check
    br.oscillation_period(r["t_steps"], r["E_steps"], direction="any")["period"]   # ~13 (units 1/m)
    br.schwinger_boson_mass(1.0)                         # mu = e/sqrt(pi) = 0.5642 (units of e)
    br.dielectric_constant(1.0, 1.0, "spinor")           # 1 + e^2/(6 pi m^2)
    br.pair_rates_constant_field(1.0, 1.0, "spinor")     # Gamma vs vacuum decay, per length per time

Command line (from the project root)
    python3 .claude/skills/conundrum/scripts/qft_backreaction.py selftest
    python3 .claude/skills/conundrum/scripts/qft_backreaction.py qed2 --m 1 --e 0.5 --E0 2
    python3 .claude/skills/conundrum/scripts/qft_backreaction.py qed2 --m "0.511 MeV" --e "0.3 MeV" --E0 "1.7 MeV" --scalar
    python3 .claude/skills/conundrum/scripts/qft_backreaction.py screen --m 1 --e 1 --E0 0.001 --tau 10
    python3 .claude/skills/conundrum/scripts/qft_backreaction.py rate --m 1 --eE 0.5
    python3 .claude/skills/conundrum/scripts/qft_backreaction.py convergence    (slow: step, grid and HBG studies)
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

import qft_production as qp  # noqa: E402  (fixed-background solvers and closed forms, SI helpers)
from unit_tools import C, E_CHARGE, HBAR  # noqa: E402  (CODATA values shared by the toolkit)

PI = math.pi
_FIELDS = ("spinor", "scalar")
_W1 = 1.0 / (2.0 - 2.0 ** (1.0 / 3.0))            # Yoshida (1990) 4th-order composition weights
_W0 = 1.0 - 2.0 * _W1
_GLX = np.array([-math.sqrt(0.6), 0.0, math.sqrt(0.6)])   # 3-point Gauss-Legendre on [-1, 1]
_GLW = np.array([5.0 / 9.0, 8.0 / 9.0, 5.0 / 9.0])


# ---------------------------------------------------------------- SI helpers
def length_density_to_SI(n_eV: float) -> float:
    """Convert a number per unit length from eV (natural units) to m^-1: n_SI = n e/(hbar c).

    Quantity: number per unit length in m^-1 (whatever was counted: here usually pairs per length).
    Valid when: n_eV is a 1+1-dimensional density in eV (hbar = c = 1)."""
    return float(n_eV) * E_CHARGE / (HBAR * C)


# ---------------------------------------------------------------- input checks
def _finite(x, name: str) -> float:
    try:
        v = float(x)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be a real number") from None
    if not math.isfinite(v):
        raise ValueError(f"{name} must be finite")
    return v


def _pos(x, name: str) -> float:
    v = _finite(x, name)
    if v <= 0:
        raise ValueError(f"{name} must be > 0")
    return v


def _field(field: str) -> str:
    if field not in _FIELDS:
        raise ValueError(f"field must be one of {_FIELDS}")
    return field


# ---------------------------------------------------------------- closed forms
def schwinger_boson_mass(e: float) -> float:
    """Photon (boson) mass of the massless Schwinger model, mu = e/sqrt(pi).

    In massless QED2 the anomaly makes the induced current exactly j = -(e^2/pi)(A - A0), so a homogeneous
    field oscillates harmonically, E(t) = E0 cos(mu t), at any amplitude.
    Quantity: mu = e/sqrt(pi) (mass = angular frequency of the homogeneous field oscillation; the period is 2 pi/mu).
    Valid when: massless Dirac fermions in 1+1 dimensions (the mean field is exact there); for m << mu the
        frequency is shifted by O((m/mu)^2 ln(mu/m)) at small amplitude; e > 0 (a mass)."""
    return _pos(e, "e") / math.sqrt(PI)


def vacuum_susceptibility(s, m: float, e: float, field: str = "spinor") -> complex:
    """One-loop (retarded) vacuum susceptibility chi(s) of 1+1 QED in the Laplace variable s.

    P = chi E (j = dP/dt), so in frequency space s = -i nu + 0. With a = sqrt(4 m^2 + s^2):
        spinor: chi_F = (e^2/(2 pi s^2)) [2 - (8 m^2/(s a)) artanh(s/a)]
        scalar: chi_S = (e^2/(2 pi)) [(2/(s a)) artanh(s/a) - (2 - (8 m^2/(s a)) artanh(s/a))/s^2]
    = e^2 int dk/2pi {m^2, k^2}/(omega^3 (4 omega^2 + s^2)) (linearized mode equations).
    Quantity: the dimensionless susceptibility chi(s) (complex); 1 + chi is the vacuum permittivity at that
        frequency; chi(0) = e^2/(6 pi m^2) (spinor) or e^2/(12 pi m^2) (scalar). Im chi != 0 on the imaginary
        axis above |s| = 2m is real pair absorption.
    Valid when: weak fields (linear response around the vacuum, eE << m^2 or amplitudes small enough), m > 0,
        Re s >= 0 (on Re s = 0 the +0 side is taken for |Im s| > 2m)."""
    import mpmath as mp
    _field(field)
    m, e = _pos(m, "m"), _pos(e, "e")
    s = complex(s)
    if not (math.isfinite(s.real) and math.isfinite(s.imag)) or s.real < 0:
        raise ValueError("need finite s with Re s >= 0 (retarded response)")
    with mp.workdps(40):
        if abs(s) < 1e-6 * m:                                 # series: chi0 + chi2 s^2 (cancellation otherwise)
            c0 = e * e / (6 * PI * m * m) if field == "spinor" else e * e / (12 * PI * m * m)
            c2 = -e * e / (30 * PI * m ** 4) if field == "spinor" else -e * e / (120 * PI * m ** 4)
            return complex(c0 + c2 * s * s)
        sm = mp.mpc(s.real if s.real > 0 else mp.mpf(10) ** -30, s.imag)    # retarded side of the cut
        a = mp.sqrt(4 * m * m + sm * sm)
        at = mp.atanh(sm / a) / (sm * a)
        core = (2 - 8 * m * m * at) / (sm * sm)
        val = e * e / (2 * mp.pi) * (core if field == "spinor" else 2 * at - core)
        return complex(val)


def dielectric_constant(m: float, e: float, field: str = "spinor") -> float:
    """Static one-loop vacuum permittivity of 1+1 QED, epsilon = 1 + chi(0).

    Quantity: epsilon = 1 + e^2/(6 pi m^2) (spinor) or 1 + e^2/(12 pi m^2) (scalar), dimensionless: a weak,
        slowly varying external field E_ext is screened to E_ext/epsilon by vacuum polarization (no pairs).
    Valid when: eE << m^2 and the field varies slowly on the time 1/(2m); m > 0, e > 0."""
    _field(field)
    m, e = _pos(m, "m"), _pos(e, "e")
    return 1.0 + e * e / ((6.0 if field == "spinor" else 12.0) * PI * m * m)


def screened_sauter_field(t, m: float, e: float, E0: float, tau: float, field: str = "spinor") -> np.ndarray:
    """Linear-response total field E(t) when an external Sauter pulse E_ext = E0 sech^2(t/tau) acts on the vacuum.

    E(t) = (1/2pi) int dnu e^{-i nu t} E_ext~(nu)/(1 + chi(-i nu + 0)),  E_ext~(nu) = E0 pi tau^2 nu/sinh(pi tau nu/2),
    with chi = vacuum_susceptibility (retarded; above nu = 2m it is complex: real pair absorption).
    Quantity: the mean (in-in) total field E(t) at times t (same unit as E0), including vacuum screening and the
        ringing it leaves, to first order in E0 (one loop).
    Valid when: e E0 << m^2 (linear response; corrections O((eE0/m^2)^2)), m > 0, tau > 0, |t| <= 40 tau."""
    import mpmath as mp
    _field(field)
    m, e, tau = _pos(m, "m"), _pos(e, "e"), _pos(tau, "tau")
    E0 = _finite(E0, "E0")
    tt = np.atleast_1d(np.asarray(t, dtype=float))
    if not np.all(np.isfinite(tt)) or np.any(np.abs(tt) > 40 * tau):
        raise ValueError("need finite |t| <= 40 tau")
    nu_max = 120.0 / (PI * tau)                                 # E_ext~ ~ exp(-pi tau nu/2) < e^-60 beyond

    def spec(nu):
        x = PI * tau * nu / 2
        return 2 * tau if nu == 0 else PI * tau * tau * nu / mp.sinh(x)

    def inv_eps(nu):
        return 1 / (1 + mp.mpc(vacuum_susceptibility(complex(0.0, -float(nu)), m, e, field)))

    mu = schwinger_boson_mass(e)                                 # near-pole of 1/(1 + chi) for small m
    brk = sorted({0.0, min(2 * m, nu_max), nu_max} | ({mu} if mu < nu_max else set()))
    out = []
    with mp.workdps(20):
        for ti in tt:
            f = lambda nu, ti=ti: mp.re(mp.exp(-1j * nu * ti) * inv_eps(nu)) * spec(nu)  # noqa: E731
            out.append(float(E0 * mp.quad(f, brk) / PI))
    return np.array(out)


def pair_rates_constant_field(m: float, eE: float, field: str = "spinor") -> dict:
    """Constant field in 1+1 without back-reaction: pair-number rate AND vacuum-decay rate per unit length.

    Each canonical mode crosses p = 0 once, at a rate eE/(2 pi) modes per length per time, and ends with
    n = exp(-pi m^2/eE) (Landau-Zener; qft_production.schwinger_n_mode with k_perp = 0). Hence
        Gamma = (eE/2pi) n                          (Hebenstreit, Berges & Gelfand 2013 eq. 70),
        w     = -(eE/2pi) ln(1 - n) (spinor),  +(eE/2pi) ln(1 + n) (scalar)   (= 2 Im L_eff per length).
    Quantity: dict with 'pair_rate' Gamma (mean number of PAIRS per unit length per unit time, mass^2; in-in) and
        'decay_rate' w (vacuum decay: P(vacuum survives) = exp(-w L T), in-out, mass^2), 'n_mode' and 'ratio' w/Gamma.
    Valid when: constant homogeneous E in 1+1 for a time >> 1/sqrt(eE), back-reaction negligible
        (e^2 Gamma t^2 << eE, i.e. the induced field stays small), m > 0, eE > 0 (mass^2)."""
    _field(field)
    m, eE = _pos(m, "m"), _pos(eE, "eE")
    n = math.exp(-PI * m * m / eE)
    pair = eE / (2 * PI) * n
    decay = eE / (2 * PI) * (-math.log1p(-n) if field == "spinor" else math.log1p(n))
    return {"pair_rate": pair, "decay_rate": decay, "n_mode": n, "ratio": decay / pair if pair > 0 else float("nan")}


def adiabatic_polarization_pairs(m: float, eE: float, field: str = "spinor") -> float:
    """Zeroth-order adiabatic 'pair number' per length while a weak, slowly varying field eE is on.

    Leading adiabatic order: spinor f_k = (eE m)^2/(16 omega^6), scalar f_k = (eE p)^2/(16 omega^6), so
        n_pol = int dk/2pi f_k = 3 (eE)^2/(256 m^3) (spinor), (eE)^2/(256 m^3) (scalar).
    Quantity: the value the solver's 'pairs' output takes while the field is on: transient vacuum polarization
        counted in the instantaneous adiabatic basis, per unit length (mass). It is NOT a number of real pairs:
        it disappears when the field is switched off adiabatically.
    Valid when: eE << m^2 and the field is slowly varying (|d ln E/dt| << m); m > 0."""
    _field(field)
    m = _pos(m, "m")
    eE = abs(_finite(eE, "eE"))
    return (3.0 if field == "spinor" else 1.0) * eE * eE / (256.0 * m ** 3)


def _chi_static_window(m: float, e: float, field: str, p_lo: float, p_hi: float) -> float:
    """Static susceptibility of the modes with kinetic momentum in [p_lo, p_hi] (closed-form antiderivatives)."""
    def G(p):
        w = math.sqrt(p * p + m * m)
        if field == "spinor":                     # m^2 int dp/(4 w^5) ; int dp/w^5 = p/(3m^2 w^3) + 2p/(3 m^4 w)
            return m * m * (p / (3 * m * m * w ** 3) + 2 * p / (3 * m ** 4 * w)) / 4
        return p ** 3 / (3 * m * m * w ** 3) / 4      # int p^2 dp/(4 w^5)
    return e * e / (2 * PI) * (G(p_hi) - G(p_lo))


# ---------------------------------------------------------------- mode evolution (exact at frozen A)
def _v_spinor(st, p, om, h):
    """Rotate every Bloch vector about n = (m, 0, p)/omega by 2 omega h; return int_0^h (s_z + p/omega) dt per mode."""
    m = st["m"]
    nx, nz = m / om, p / om
    sx, sy, sz = st["sx"], st["sy"], st["sz"]
    ns = nx * sx + nz * sz
    th = 2.0 * om * h
    c, s = np.cos(th), np.sin(th)
    cx, cy, cz = -nz * sy, nz * sx - nx * sz, nx * sy                       # n x s
    integral = ns * nz * h + (sz - ns * nz) * s / (2 * om) + cz * (1 - c) / (2 * om) + h * nz
    sx, sy, sz = sx * c + cx * s + nx * ns * (1 - c), sy * c + cy * s, sz * c + cz * s + nz * ns * (1 - c)
    norm = np.sqrt(sx * sx + sy * sy + sz * sz)                             # pure state: |s| = 1 (roundoff)
    st["sx"], st["sy"], st["sz"] = sx / norm, sy / norm, sz / norm
    return integral


def _v_scalar(st, p, om, h):
    """Evolve (u, u') at frozen omega for time h; return int_0^h p (|u|^2 - 1/(2 omega)) dt per mode."""
    u, v = st["u"], st["v"]
    th = om * h
    c, s = np.cos(th), np.sin(th)
    uu, vv, uv = np.abs(u) ** 2, np.abs(v) ** 2, np.real(np.conj(u) * v)
    s2 = np.sin(2 * th)
    iu = uu * (h / 2 + s2 / (4 * om)) + vv / om ** 2 * (h / 2 - s2 / (4 * om)) + uv * s * s / om ** 2
    st["u"], st["v"] = u * c + v * (s / om), -om * s * u + c * v
    return p * (iu - h / (2 * om))


def _observables(st, A):
    """Per-mode adiabatic occupation f_k, current j, matter energy and pairs per length at gauge field A."""
    m, e, k, w = st["m"], st["e"], st["k"], st["w"]
    p = k - e * A
    om = np.sqrt(p * p + m * m)
    if st["field"] == "spinor":
        dx, dy, dz = st["sx"] + m / om, st["sy"], st["sz"] + p / om       # s + n: small, so f is accurate
        f = 0.25 * (dx * dx + dy * dy + dz * dz)
        j = e * float(np.sum(w * dz))
    else:
        u, v = st["u"], st["v"]
        f = 0.5 * om * np.abs(u - 1j * v / om) ** 2
        j = 2 * e * float(np.sum(w * p * (np.abs(u) ** 2 - 0.5 / om)))
    return f, j, float(np.sum(w * 2 * om * f)), float(np.sum(w * f)), p


def qed2_backreaction(m: float, e: float, E0: float, t_end: float, field: str = "spinor", *, t0: float = 0.0,
                      A0: float = 0.0, E_ext=None, backreaction: bool = True, k_max: float = None,
                      dk: float = None, k_nodes=None, k_weights=None, dt: float = None, record_every: int = None,
                      edge_tol: float = 1e-4, drift_tol: float = 1e-6, finite_ring: bool = False) -> dict:
    """Self-consistent mean-field evolution of a homogeneous E(t) and the charged quantum modes in 1+1 QED.

    Solves dE/dt = dE_ext/dt - j, dA/dt = -E with E(t0) = E0 + E_ext(t0), A(t0) = A0, the modes starting in the
    zeroth-order adiabatic vacuum of A0 (sudden switch-on if E(t0) != 0). backreaction=False drops j: the field
    is then the prescribed E0 + E_ext(t) and the modes reproduce qft_production's fixed-background results.
    Grid: canonical k on a uniform grid of spacing dk over eA0 +- k_max (defaults from m, eE0 and t_end), or your
    own k_nodes with quadrature weights k_weights for int dk. A uniform grid is exactly the problem on a ring of
    circumference L = 2 pi/dk; it equals the infinite line while t - t0 <= L/2 = pi/dk (pair members separate by up
    to 2(t - t0)), which is enforced unless finite_ring=True ('ring_length' is returned). With k_nodes the same
    rule applies to your spacing and is not checked. E_ext: callable t -> field (same unit as E0).
    Quantity: dict of arrays at record times 't': 'E' (total field: in-in mean field), 'A', 'j' (renormalized
        in-in current, gauge invariant, mass^2), 'pairs' (mean PAIRS per unit length in the zeroth-order adiabatic basis:
        basis dependent while E != 0, see adiabatic_polarization_pairs; physical once the field is off),
        'energy_field' E^2/2, 'energy_matter' int dk/2pi 2 omega f_k, 'energy_total' (energies per length);
        'E_steps' at every step 't_steps'; final per-mode 'f_k' on 'k' with kinetic momenta 'p';
        'energy_drift' (max relative change of the total energy; meaningful when E_ext is None),
        'edge_share' (fraction of the pairs in the outer 2% of the grid), 'chi_tail' (static susceptibility
        missing beyond the grid), 'ring_length', 'dt', 'steps'.
    Valid when: homogeneous field in 1+1, mean-field approximation; m > 0, e > 0; the grid resolves the mass
        scale (dk <= m) and holds the pairs (edge_share <= edge_tol, else ValueError); omega_max dt <= 1.5
        (else ValueError); with back-reaction and no E_ext the energy must be conserved to drift_tol (else
        ValueError: reduce dt);
        uniform grid: t_end - t0 <= pi/dk unless finite_ring=True (then the answer is for a ring of length 2 pi/dk)."""
    field = _field(field)
    m, e = _pos(m, "m"), _pos(e, "e")
    E0, t0, t_end, A0 = _finite(E0, "E0"), _finite(t0, "t0"), _finite(t_end, "t_end"), _finite(A0, "A0")
    if t_end <= t0:
        raise ValueError("need t_end > t0")
    if E_ext is not None and not callable(E_ext):
        raise ValueError("E_ext must be a callable t -> E_ext(t)")
    Eext = (lambda t: 0.0) if E_ext is None else (lambda t: float(E_ext(t)))   # noqa: E731
    E_start = E0 + Eext(t0)
    if not math.isfinite(E_start):
        raise ValueError("E_ext(t0) must be finite")
    eE_scale = abs(e * E0) + (abs(e * Eext(t0)) if E_ext is not None else 0.0)
    if k_nodes is not None:
        k = np.asarray(k_nodes, dtype=float).ravel()
        if k_weights is None:
            raise ValueError("k_weights (quadrature weights for int dk) must accompany k_nodes")
        wk = np.asarray(k_weights, dtype=float).ravel()
        if k.shape != wk.shape or k.size < 8 or not (np.all(np.isfinite(k)) and np.all(np.isfinite(wk))) \
                or np.any(wk <= 0) or np.any(np.diff(k) <= 0):
            raise ValueError("k_nodes must be >= 8 increasing finite values with positive finite k_weights")
    else:
        scale = max(m, math.sqrt(eE_scale))
        dk = _pos(dk, "dk") if dk is not None else min(scale / 8.0, m / 2.0, PI / (t_end - t0))
        if dk > m:
            raise ValueError(f"dk = {dk:g} > m = {m:g}: the grid must resolve the mass scale")
        # A uniform grid of spacing dk is exactly the system on a ring of circumference L = 2 pi/dk. Pair members
        # separate by up to 2(t - t0) (Poisson summation: the mode sum aliases once that exceeds L), so the
        # infinite-line answer is guaranteed only for t - t0 <= L/2 = pi/dk.
        if (t_end - t0) > PI / dk * (1 + 1e-12) and not finite_ring:
            raise ValueError(f"t_end - t0 = {t_end - t0:g} > pi/dk = {PI / dk:g}: pairs would meet their periodic images "
                             f"on the ring of circumference 2 pi/dk = {2 * PI / dk:g} the grid represents; lower dk, "
                             "or pass finite_ring=True to accept the finite-ring answer")
        if k_max is None:
            k_max = 12.0 * scale + min(abs(e * E0) * (t_end - t0), 30.0 * scale)
        k_max = _pos(k_max, "k_max")
        nk = 2 * int(math.ceil(k_max / dk)) + 1
        if nk > 400001:
            raise ValueError(f"grid of {nk} modes is too large (raise dk or lower k_max)")
        k = e * A0 + dk * (np.arange(nk) - nk // 2)
        wk = np.full(nk, dk)
    w = wk / (2 * PI)
    om_max = float(np.max(np.sqrt((k - e * A0) ** 2 + m * m)))
    if dt is None:
        # splitting error ~ (omega dt)^4: these give energy drifts of ~1e-8 (spinor) and ~3e-7 (scalar, whose
        # high-k modes carry more polarization) in the self-test runs
        dt = min((0.5 if field == "spinor" else 0.3) / om_max, 0.03 / max(m, math.sqrt(eE_scale), schwinger_boson_mass(e)))
    dt = _pos(dt, "dt")
    if om_max * dt > 1.5:
        raise ValueError(f"omega_max dt = {om_max * dt:.3g} > 1.5: the splitting would mis-resolve fast modes")
    nsteps = max(1, int(math.ceil((t_end - t0) / dt)))
    h = (t_end - t0) / nsteps
    if record_every is None:
        record_every = max(1, nsteps // 2000)
    record_every = int(record_every)
    if record_every < 1:
        raise ValueError("record_every must be >= 1")

    st = {"field": field, "m": m, "e": e, "k": k, "w": w}
    p0 = k - e * A0
    om0 = np.sqrt(p0 * p0 + m * m)
    if field == "spinor":
        st["sx"], st["sy"], st["sz"] = -m / om0, np.zeros_like(k), -p0 / om0
    else:
        st["u"] = (1.0 / np.sqrt(2 * om0)).astype(complex)
        st["v"] = -1j * om0 * st["u"]
    v_flow = _v_spinor if field == "spinor" else _v_scalar
    charge = e if field == "spinor" else 2 * e
    A, Eind, t = A0, E0, t0

    def drift(tau):
        nonlocal A, t
        integral = Eind * tau
        if E_ext is not None:
            integral += 0.5 * tau * sum(gw * Eext(t + 0.5 * tau * (gx + 1)) for gx, gw in zip(_GLX, _GLW))
        A, t = A - integral, t + tau

    rec = {key: [] for key in ("t", "E", "A", "j", "pairs", "energy_field", "energy_matter")}

    def record():
        f, j, em, npair, _ = _observables(st, A)
        Et = Eind + Eext(t)
        for key, val in zip(rec, (t, Et, A, j, npair, 0.5 * Et * Et, em)):
            rec[key].append(val)

    t_steps, E_steps = [t], [E_start]
    om_seen = om_max
    record()
    for i in range(nsteps):
        for c in (_W1, _W0, _W1):
            drift(0.5 * c * h)
            p = k - e * A
            om = np.sqrt(p * p + m * m)
            om_seen = max(om_seen, om[0], om[-1])              # |p| is largest at a grid end
            J = charge * float(np.sum(w * v_flow(st, p, om, c * h)))
            if backreaction:
                Eind -= J
            drift(0.5 * c * h)
        t = t0 + (i + 1) * h                                   # remove accumulated roundoff in t
        t_steps.append(t)
        E_steps.append(Eind + Eext(t))
        if (i + 1) % record_every == 0 or i + 1 == nsteps:
            record()
    if om_seen * h > 1.5:
        raise ValueError(f"omega_max dt reached {om_seen * h:.3g} > 1.5 (the field moved the grid): reduce dt")
    out = {key: np.array(val) for key, val in rec.items()}
    out["energy_total"] = out["energy_field"] + out["energy_matter"]
    f, j, em, npair, p = _observables(st, A)
    nedge = max(2, k.size // 50)
    # Real pairs that ran off the grid show up as a sizeable share of all pairs in the outer 2% of the nodes.
    # (A sudden switch-on excites every mode at the level (eE m)^2/(16 omega0^6): that tail is legitimately cut.)
    edge_pairs = float(np.dot(w[:nedge], f[:nedge]) + np.dot(w[-nedge:], f[-nedge:]))
    edge_share = edge_pairs / max(npair, 1e-300)
    edge_f = float(max(np.max(f[:nedge]), np.max(f[-nedge:])))
    if edge_share > edge_tol and edge_f > 1e-12:
        raise ValueError(f"{edge_share:.2g} of all pairs sit at the edges of the momentum grid (> {edge_tol:g}): "
                         "real pairs left the grid; raise k_max (or widen k_nodes)")
    etot = out["energy_total"]
    floor = 1e-13 * float(np.dot(w, np.sqrt((k - e * A0) ** 2 + m * m)))      # roundoff scale of the mode sums
    drift_rel = float(np.max(np.abs(etot - etot[0]))) / max(abs(etot[0]), floor)
    if backreaction and E_ext is None and drift_rel > drift_tol:
        raise ValueError(f"total energy drifted by {drift_rel:.2g} (> {drift_tol:g}): reduce dt")
    chi_tail = _chi_static_window(m, e, field, -1e12, float(p[0])) + _chi_static_window(m, e, field, float(p[-1]), 1e12)
    out.update({"t_steps": np.array(t_steps), "E_steps": np.array(E_steps), "k": k, "p": p, "f_k": f,
                "energy_drift": drift_rel, "edge_share": edge_share, "chi_tail": chi_tail, "dt": h,
                "steps": nsteps, "field": field, "backreaction": bool(backreaction),
                "ring_length": (2 * PI / dk if k_nodes is None else None),
                "mu": schwinger_boson_mass(e), "epsilon_static": dielectric_constant(m, e, field)})
    return out


def oscillation_period(t, E, t_min: float = None, direction: str = "up") -> dict:
    """Period of an oscillating field from its zero crossings (linear interpolation between samples).

    direction="up": successive upward crossings, period = their mean spacing. direction="any": crossings of
    either sign, period = 2 x mean spacing (half-periods); use it when the run holds fewer than two full periods.
    Quantity: dict with 'period' (in the unit of t, i.e. 1/mass), 'periods' (each interval; half-periods doubled
        for "any"), 'crossings' (the crossing times) and 'frequency' 2 pi/period.
    Valid when: E(t) is sampled finely (many samples per period) and has at least two upward crossings ("up") or
        three crossings ("any") after t_min (else ValueError); for anharmonic plasma oscillations the "any"
        estimate averages unequal half-periods."""
    t = np.asarray(t, dtype=float)
    E = np.asarray(E, dtype=float)
    if t.shape != E.shape or t.ndim != 1 or t.size < 4 or not (np.all(np.isfinite(t)) and np.all(np.isfinite(E))):
        raise ValueError("need finite 1-D arrays t, E of equal length >= 4")
    if np.any(np.diff(t) <= 0):
        raise ValueError("t must increase")
    if direction not in ("up", "any"):
        raise ValueError("direction must be 'up' or 'any'")
    sel = np.ones_like(t, dtype=bool) if t_min is None else t >= float(t_min)
    tt, EE = t[sel], E[sel]
    up = (EE[:-1] < 0) & (EE[1:] >= 0)
    i = np.where(up | ((EE[:-1] > 0) & (EE[1:] <= 0)) if direction == "any" else up)[0]
    if i.size < (2 if direction == "up" else 3):
        raise ValueError("too few zero crossings: run longer, lower t_min or use direction='any'")
    tc = tt[i] - EE[i] * (tt[i + 1] - tt[i]) / (EE[i + 1] - EE[i])
    P = np.diff(tc) * (1.0 if direction == "up" else 2.0)
    return {"period": float(P.mean()), "periods": P, "crossings": tc, "frequency": 2 * PI / float(P.mean())}


# ---------------------------------------------------------------- self-test
def selftest(verbose: bool = True) -> bool:
    """Compare with closed forms, published results and exact limits. Returns True if all pass."""
    results = []

    def check(name, got, want, tol, rel=False):
        err = abs(got - want) / (abs(want) if rel and want != 0 else 1.0)
        ok = bool(err <= tol)
        results.append(ok)
        if verbose:
            print(f"{'PASS' if ok else 'FAIL'}  {name}: {got:.10g} (expected {want:.10g}, "
                  f"{'rel' if rel else 'abs'} tol {tol:g})")

    sqpi = math.sqrt(PI)

    # A1. The closed-form susceptibility against its defining mode integral e^2 int dk/2pi {m^2, k^2}/(omega^3
    #     (4 omega^2 + s^2)), done independently by the trapezoid rule in x after k = m sinh x, |x| < 20, step 0.025
    #     (analytic integrand: the error falls like exp(-2 pi d/step), d ~ 0.3 the distance of the nearest complex
    #     singularity, i.e. < 1e-30; the cut-off tails ~ e^{-2|x|} add ~1e-17; tolerance 1e-10). m != 1 so that a
    #     wrong power of m cannot hide.
    xg = np.linspace(-20.0, 20.0, 1601)
    m_, e_ = 0.7, 1.3
    kq, wq = m_ * np.sinh(xg), m_ * np.cosh(xg) * (xg[1] - xg[0])
    om_q = np.sqrt(kq * kq + m_ * m_)
    for field in _FIELDS:
        num = m_ * m_ if field == "spinor" else kq * kq
        for sv in (0.7, 0.3 + 1.1j):
            q = e_ * e_ / (2 * PI) * np.sum(wq * num / (om_q ** 3 * (4 * om_q ** 2 + sv * sv)))
            check(f"{field} chi(s={sv}) closed form vs mode-integral quadrature (rel)",
                  abs(vacuum_susceptibility(sv, m_, e_, field) / q - 1), 0.0, 1e-10)

    # A2. Trap: pair-number rate vs vacuum-decay rate per length in a constant field (both from n = e^{-pi m^2/eE}):
    #     w > Gamma for fermions, w < Gamma for bosons (they agree only at weak field).
    rf, rs = pair_rates_constant_field(1.0, 2.0, "spinor"), pair_rates_constant_field(1.0, 2.0, "scalar")
    check("spinor: vacuum-decay rate exceeds pair rate (w/Gamma > 1)", float(rf["ratio"] > 1.05), 1.0, 0)
    check("scalar: vacuum-decay rate below pair rate (w/Gamma < 1)", float(rs["ratio"] < 0.95), 1.0, 0)

    # B1/B2. Back-reaction OFF, Sauter pulse E0 sech^2(t/tau): per-mode occupations against the exact result of
    #     Gavrilov & Gitman 1996 (arXiv:hep-th/9603152, p. 17), written for D space dimensions; 1+1 is p_perp = 0:
    #     "Thus, we get the mean numbers of fermions created, Np,r = sinh [ πα 2 (2eEα +ω− −ω+) ] sinh [ πα 2 (2eEα
    #     +ω+ −ω−) ] sinh(παω+) sinh(παω−) . (42)" and "For scalar particles it has a diﬀerent form Np,r = cosh2 [ π √
    #     (eEα 2)2 − 1 4 ] + sinh2 [ πα 2 (ω+ −ω−) ] sinh(παω+) sinh(παω−) . (43)", "ω± = √ m2 + p2 ⊥ + (pD ∓eEα)2"
    #     (alpha = tau; PDF extraction drops the fraction bars: numerator / denominator). Evaluated through
    #     qft_production.sauter_n_spinor/_scalar with k_perp = 0. 13 sample modes (not an integration grid, hence
    #     edge_tol = 1). Tolerance 1e-6: the 4th-order splitting error at dt = 0.02 is 9e-8 (6e-9 at dt = 0.01).
    m_, eE0, tau = 1.0, 1.0, 2.0
    ks = np.linspace(-3.0, 3.0, 13)
    A_in = eE0 * tau * math.tanh(15.0)                      # A(t) = -E0 tau tanh(t/tau): p = k + eE0 tau tanh(t/tau)
    sauter = lambda t: eE0 / math.cosh(t / tau) ** 2        # noqa: E731  (e = 1 here)
    for field, ref_fn in (("spinor", qp.sauter_n_spinor), ("scalar", qp.sauter_n_scalar)):
        r = qed2_backreaction(m_, 1.0, 0.0, 15 * tau, field, t0=-15 * tau, A0=A_in, E_ext=sauter, backreaction=False,
                              k_nodes=ks, k_weights=np.full(ks.size, 0.5), dt=0.02, edge_tol=1.0)
        ref = ref_fn(ks, 0.0, m_, eE0, tau)
        check(f"{field}, back-reaction off, Sauter: max rel. error of f_k over 13 modes vs Gavrilov-Gitman eq. "
              f"{42 if field == 'spinor' else 43}", float(np.max(np.abs(r["f_k"] / ref - 1))), 0.0, 1e-6)

    # B3. Back-reaction ON but e -> 0 at fixed eE0: the back-reaction shifts f_k by O(e^2) (measured 4.5e-2, 4.4e-4,
    #     4.5e-6 relative at e = 1e-2, 1e-3, 1e-4), so at e = 1e-5 the occupations must again be Gavrilov-Gitman eq. 42
    #     (same tolerance as B1).
    e_small = 1e-5
    kg = 0.1 * np.arange(-100, 101)
    r = qed2_backreaction(m_, e_small, 0.0, 15 * tau, "spinor", t0=-15 * tau, A0=A_in / e_small,
                          E_ext=lambda t: sauter(t) / e_small, k_nodes=kg, k_weights=np.full(kg.size, 0.1), dt=0.02)
    sel = np.searchsorted(kg, ks - 1e-9)
    check("spinor, back-reaction on with e = 1e-4 at fixed eE0: max rel. error of f_k vs eq. 42",
          float(np.max(np.abs(r["f_k"][sel] / qp.sauter_n_spinor(ks, 0.0, m_, eE0, tau) - 1))), 0.0, 1e-6)

    # B4. Back-reaction OFF, constant field switched on at t = 0 (m = eE = 1): late-time slope of the pair number
    #     per length against Hebenstreit, Berges & Gelfand 2013 (arXiv:1302.5537) eq. 70, "∆ n+ TLm 2 = ǫ 2π exp
    #     ( −π ǫ ) . (70)" with "ǫ = E0 Ec , (69) with the critical Schwinger ﬁeld strength Ec =m2/e", i.e.
    #     dn/dt = (eE/2pi) exp(-pi m^2/eE). Slope over 10 <= t <= 20 (after the switch-on transient). Tolerances:
    #     spinor 1e-4 (measured 1.6e-5, converged in dk and dt), scalar 1e-3 (the scalar adiabatic number keeps a
    #     slowly decaying oscillation after each crossing: measured -6.5e-4 here, between -4.5e-4 and -3.5e-5 in
    #     later windows).
    kc = np.arange(-26.0, 6.0 + 1e-9, 0.05)
    for field, tol in (("spinor", 1e-4), ("scalar", 1e-3)):
        r = qed2_backreaction(1.0, 1.0, 1.0, 20.0, field, backreaction=False, k_nodes=kc,
                              k_weights=np.full(kc.size, 0.05), dt=0.02, record_every=1)
        i1, i2 = np.searchsorted(r["t"], 10.0 - 1e-9), np.searchsorted(r["t"], 20.0 - 1e-9)
        slope = (r["pairs"][i2] - r["pairs"][i1]) / (r["t"][i2] - r["t"][i1])
        check(f"{field}, constant field, no back-reaction: pairs per length per time vs HBG eq. 70", slope,
              pair_rates_constant_field(1.0, 1.0, field)["pair_rate"], tol, rel=True)

    # C1. Massless limit (units mu = e/sqrt(pi) = 1, m = 0.05 mu), LARGE amplitude E0 = 1 (eE0 = 1.77 mu^2 = 700 m^2):
    #     the anomaly makes the current -(e^2/pi)(A - A0), so E oscillates harmonically at mu at any amplitude.
    #     Gold, McGady, Patil & Vardanyan 2021 (arXiv:2012.15824) eq. 2.4, the bosonized massless QED2 Hamiltonian:
    #     "Hϕ,D = 1 2 : ( Π2 ϕ + (∂xϕ)2 +g2 ( ϕ + Dext g )2) : , (2.4) where again g2 = e2/π" (a free boson of mass
    #     g = e/sqrt(pi), Schwinger 1962). Tolerance 1e-3 on the period (measured +2.4e-4 at m = 0.05, +5.8e-5 at
    #     m = 0.02: the mass correction vanishes as m -> 0).
    e_mu = sqpi
    loss = {}
    for m_l, dk_l in ((0.05, 0.01), (0.02, 0.005)):
        r = qed2_backreaction(m_l, e_mu, 1.0, 4 * 2 * PI, "spinor", k_max=5.0, dk=dk_l, dt=0.02)
        check(f"massless limit (m = {m_l} mu), large amplitude: period vs 2 pi/mu, mu = e/sqrt(pi)",
              oscillation_period(r["t_steps"], r["E_steps"])["period"], 2 * PI / schwinger_boson_mass(e_mu), 1e-3,
              rel=True)
        loss[m_l] = 1.0 - float(np.max(r["E_steps"][r["t_steps"] > 3 * 2 * PI]))
    # ... and harmonic in the limit: each passage through p = 0 leaves a Landau-Zener fraction ~ pi m^2/eE of the modes
    # unflipped, so the amplitude loss over 3 periods must scale as m^2 (ratio (0.05/0.02)^2 = 6.25; measured 6.13,
    # loss 5.1% and 0.83%). Tolerance 15% for the next order in m^2/eE.
    check("massless limit: amplitude loss over 3 periods scales as m^2 -> 0 (loss ratio m = 0.05 vs 0.02)",
          loss[0.05] / loss[0.02], 6.25, 0.15, rel=True)
    # C2. Energy budget E^2/2 + int dk/2pi 2 omega f_k conserved (Otto, Graeveling & Kaempfer 2019, arXiv:1812.10832,
    #     eq. 10: "ϵ = E2 2 + 2 ∫ dp 2π|β|2Ω− ∫ dt ˙EextE (10) and setting ˙ϵ = 0 . The last term is the work the external
    #     current must do to counteract the electric ﬁeld. We use the energy density to check the accuracy of the
    #     numerics."), here with E_ext = 0, over 4 plasma periods. Tolerance 1e-7 (4th-order splitting: 1.2e-8).
    check("energy E^2/2 + int 2 omega f conserved over 4 oscillations (max relative drift)", r["energy_drift"], 0.0, 1e-7)

    # C3. Massless limit at SMALL amplitude (E0 = 1e-4, linear regime): the frequency is mu up to
    #     O((m/mu)^2 ln(mu/m)) (measured -9.0e-4 at m = 0.01, -2.6e-4 at m = 0.005). Non-uniform grid k = m sinh x
    #     resolves the mass scale near p = 0. Tolerance 1e-3.
    m_s = 0.005
    xs = np.linspace(-math.asinh(8.0 / m_s), math.asinh(8.0 / m_s), 500)
    r = qed2_backreaction(m_s, e_mu, 1e-4, 4 * 2 * PI, "spinor", k_nodes=m_s * np.sinh(xs),
                          k_weights=m_s * np.cosh(xs) * (xs[1] - xs[0]), dt=0.05)
    check("massless limit (m = 0.005 mu), small amplitude: period vs 2 pi/mu",
          oscillation_period(r["t_steps"], r["E_steps"])["period"], 2 * PI, 1e-3, rel=True)

    # C4. Gauge invariance: a constant shift of A (here A0 = 0.37, not a multiple of the grid spacing) relabels the
    #     canonical modes and must leave E(t) unchanged (strong field eE0 = 1.5 m^2, real pairs). Tolerance 1e-7 E0:
    #     the shift moves the grid edges in kinetic momentum by eA0, changing the truncated tails (measured 3e-9).
    kgi = np.arange(-25.0, 25.0 + 1e-9, 0.1)
    runs = [qed2_backreaction(1.0, 1.0, 1.5, 8.0, "spinor", A0=a0, k_nodes=kgi, k_weights=np.full(kgi.size, 0.1),
                              dt=0.02) for a0 in (0.0, 0.37)]
    check("gauge invariance: max |E(t; A0 = 0.37) - E(t; A0 = 0)| / E0",
          float(np.max(np.abs(runs[1]["E_steps"] - runs[0]["E_steps"]))) / 1.5, 0.0, 1e-7)
    # C5. The canonical-cutoff trap: the vacuum at constant A summed over |k| < Lambda (canonical) carries
    #     j = -e int dk/2pi p/omega = (e/2pi)[omega(-Lambda - eA) - omega(Lambda - eA)] -> e^2 A/pi (spurious, gauge
    #     dependent); the kinetic-momentum (adiabatic) subtraction used here gives exactly 0. Lambda = 1e4, eA = 0.7:
    #     corrections O(m^2 eA/Lambda^2) ~ 1e-8 relative.
    e_, A_, Lam = 1.0, 0.7, 1e4
    j_canon = e_ / (2 * PI) * (math.hypot(-Lam - e_ * A_, 1.0) - math.hypot(Lam - e_ * A_, 1.0))
    check("canonical cutoff: vacuum current -> e^2 A/pi (spurious)", j_canon, e_ * e_ * A_ / PI, 1e-6, rel=True)
    st = {"field": "spinor", "m": 1.0, "e": e_, "k": kgi, "w": np.full(kgi.size, 0.1 / (2 * PI))}
    p_ = kgi - e_ * A_
    st["sx"], st["sy"], st["sz"] = -1.0 / np.hypot(p_, 1.0), np.zeros_like(p_), -p_ / np.hypot(p_, 1.0)
    check("renormalized (kinetic) current of the same vacuum", abs(_observables(st, A_)[1]), 0.0, 1e-14)

    # C6. Back-reaction ON, weak external Sauter pulse (eE0 = 1e-3 m^2, tau = 1/m, so its spectrum reaches above 2m):
    #     the self-consistent E(t) against the closed-form linear response (vacuum_susceptibility; an independent,
    #     frequency-domain method), at the peak and in the ringing afterwards. Tolerance 2e-6 E0 for the spinor
    #     (nonlinear corrections O((eE0/m^2)^2) and splitting error; measured 1.2e-7). The scalar polarization integrand
    #     falls only as p^-3, so the grid (|p| < 60) misses chi_tail ~ 1.1e-5 of it: tolerance 2 chi_tail E + 2e-6 E0
    #     (measured 1.2e-5 at the peak).
    E0w, tt_ = 1e-3, np.array([0.0, 2.0, 4.0])
    for field, kmax_, dk_, dt_ in (("spinor", 20.0, 0.125, 0.025), ("scalar", 60.0, 0.25, 0.02)):
        r = qed2_backreaction(1.0, 1.0, 0.0, 4.0, field, t0=-8.0, E_ext=lambda t: E0w / math.cosh(t) ** 2,
                              k_max=kmax_, dk=dk_, dt=dt_)
        got = np.interp(tt_, r["t_steps"], r["E_steps"])
        ref = screened_sauter_field(tt_, 1.0, 1.0, E0w, 1.0, field)
        tol = 2e-6 + (2 * r["chi_tail"] * float(np.max(np.abs(ref))) / E0w if field == "scalar" else 0.0)
        check(f"{field}: self-consistent E(t = 0, 2, 4) vs closed-form linear response, max |diff|/E0",
              float(np.max(np.abs(got - ref))) / E0w, 0.0, tol)
    # C7. Small mass (m = 0.05 mu): the ringing after a short pulse is a damped oscillation near mu (photon decaying
    #     into pairs above 2m); simulation vs closed-form linear response at t = 5, 10 (frequency AND damping).
    #     Tolerance 1e-5 E0 (measured 4e-6; E0 = 1e-4, the oscillation amplitude is ~1.2 E0).
    E0w, tt_ = 1e-4, np.array([5.0, 10.0])
    r = qed2_backreaction(0.05, e_mu, 0.0, 10.0, "spinor", t0=-8.0, E_ext=lambda t: E0w / math.cosh(t) ** 2,
                          k_max=10.0, dk=0.0125, dt=0.05)
    got = np.interp(tt_, r["t_steps"], r["E_steps"])
    ref = screened_sauter_field(tt_, 0.05, e_mu, E0w, 1.0, "spinor")
    check("m = 0.05 mu: ringing E(t = 5, 10) vs linear response (frequency and damping), max |diff|/E0",
          float(np.max(np.abs(got - ref))) / E0w, 0.0, 1e-5)

    # C8. Slow weak pulse (tau = 10/m, eE0 = 1e-3 m^2), spinor. (a) Peak field vs the closed form (1e-6 E0, measured
    #     2.8e-7); (b) the closed form's own adiabatic limit: E(0)/E0 = (1/eps)(1 + 2 chi2/(eps tau^2)) with
    #     eps = 1 + e^2/(6 pi m^2), chi2 = -e^2/(30 pi m^4) (series of chi_F; tolerance 1e-5 for the O(tau^-4) rest);
    #     (c) TRAP: the adiabatic 'pairs' at the peak are vacuum polarization, 3 (eE)^2/(256 m^3) (2%: next adiabatic
    #     order O(1/(m tau)^2), measured 0.85%), and (d) they vanish once the pulse is over (no real pairs).
    #     finite_ring=True: t - t0 = 160 > pi/dk, harmless here because only ~1e-30 real pairs are made (nothing
    #     propagates to meet its periodic image), and (a) cross-checks it.
    E0w, tau = 1e-3, 10.0
    r = qed2_backreaction(1.0, 1.0, 0.0, 8 * tau, "spinor", t0=-8 * tau, E_ext=lambda t: E0w / math.cosh(t / tau) ** 2,
                          k_max=20.0, dk=0.25, dt=0.05, finite_ring=True)
    E_pk = float(np.interp(0.0, r["t_steps"], r["E_steps"]))
    ref0 = float(screened_sauter_field(0.0, 1.0, 1.0, E0w, tau, "spinor")[0])
    check("slow pulse: peak E vs closed-form linear response (|diff|/E0)", abs(E_pk - ref0) / E0w, 0.0, 1e-6)
    eps, chi2 = dielectric_constant(1.0, 1.0, "spinor"), -1.0 / (30 * PI)
    check("closed form -> static screening E/E_ext = (1/eps)(1 + 2 chi2/(eps tau^2))", ref0 / E0w,
          (1 + 2 * chi2 / (eps * tau * tau)) / eps, 1e-5, rel=True)
    n_pk = float(np.interp(0.0, r["t"], r["pairs"]))
    check("TRAP: adiabatic 'pairs' at the peak = polarization 3(eE)^2/(256 m^3)", n_pk,
          adiabatic_polarization_pairs(1.0, E_pk, "spinor"), 0.02, rel=True)
    check("TRAP: ... and they are gone after the pulse (pairs_end/pairs_peak < 1e-3)",
          float(r["pairs"][-1] / n_pk < 1e-3), 1.0, 0)

    # C9. Strong field with back-reaction against Hebenstreit, Berges & Gelfand 2013 (arXiv:1302.5537), their
    #     parameters "For all subsequent numerical results we employ e/m = 0.3" and "an initial value ǫ = 1" (E0 = Ec =
    #     m^2/e, sudden switch-on). Their statements: "This process happens on rather short time scales of the order of
    #     ∆ t ∼ 25/m." and creation "eﬀectively terminates when the magnitude of the ﬁeld strength drops below ∼ 0.5Ec,
    #     corresponding to the approximate plateaus in n+(t)". Checks: n(25)/n(60) within 10% of 1 (measured 1.018),
    #     and n changes by < 5% between the first time |E| <= 0.5 Ec and t = 60 (measured 1.5%); energy conserved.
    #     (Their later numbers, "E ≃ Ec/2" and "Ω ≃ πm/50", come from a lattice with a_s = 0.075/m and L = 19.2/m and
    #     are compared, not checked, in the 'convergence' subcommand.)
    Ec = 1.0 / 0.3
    kh = np.arange(-45.0, 15.0 + 1e-9, 0.05)                 # pi/dk = 63 > 60: infinite-line answer
    r = qed2_backreaction(1.0, 0.3, Ec, 60.0, "spinor", k_nodes=kh, k_weights=np.full(kh.size, 0.05), dt=0.02)
    n25, n60 = np.interp([25.0, 60.0], r["t"], r["pairs"])
    t_half = float(r["t_steps"][np.argmax(np.abs(r["E_steps"]) <= 0.5 * Ec)])
    check("HBG e/m = 0.3, E0 = Ec: pair number levels off within ~25/m (n(25)/n(60))", n25 / n60, 1.0, 0.1)
    check("HBG: production stops once |E| < 0.5 Ec (|n(t_half) - n(60)|/n(60))",
          abs(float(np.interp(t_half, r["t"], r["pairs"])) - n60) / n60, 0.0, 0.05)
    check("HBG run: energy conserved (max relative drift)", r["energy_drift"], 0.0, 1e-6)
    # C10. Scalar QED2, Kluger et al. 1991 (PRL 67, 2427) abstract: "We investigate the mechanism of pair creation in
    #     scalar QED from spatially homogeneous strong electric fields in 1+1 dimensions. Solution of the semiclassical
    #     field equations shows particle creation followed by plasma oscillations." (m = e = E0 = 1): E reverses sign
    #     (min E/E0 measured -0.78), with energy conserved.
    r = qed2_backreaction(1.0, 1.0, 1.0, 40.0, "scalar", k_max=30.0, dk=0.075, dt=1.0 / 80)
    check("scalar, Kluger 1991: plasma oscillation (E reverses: min E/E0 < -0.5)",
          float(np.min(r["E_steps"]) < -0.5), 1.0, 0)
    check("scalar run: energy conserved (max relative drift)", r["energy_drift"], 0.0, 1e-6)

    passed = all(results)
    if verbose:
        print(f"\n{sum(results)}/{len(results)} checks passed")
    return passed


def _convergence() -> int:
    """Slow studies (not part of the self-test): step size, grid spacing (finite ring), scalar tail, HBG comparison."""
    import time
    e_mu = math.sqrt(PI)
    print("1. Step size, massless limit (m = 0.05 mu, E0 = 1, 4 periods): period/(2 pi/mu) - 1 and energy drift")
    for dt in (0.04, 0.02, 0.01):
        r = qed2_backreaction(0.05, e_mu, 1.0, 8 * PI, "spinor", k_max=5.0, dk=0.01, dt=dt, drift_tol=1.0)
        print(f"   dt {dt:5.3f}: {oscillation_period(r['t_steps'], r['E_steps'])['period'] / (2 * PI) - 1:+.3e}, "
              f"drift {r['energy_drift']:.2e}")
    print("2. Step size, scalar m = e = E0 = 1, t = 40: E(40) and energy drift")
    for dt in (1 / 60, 1 / 120, 1 / 240):
        r = qed2_backreaction(1.0, 1.0, 1.0, 40.0, "scalar", k_max=30.0, dk=0.075, dt=dt, drift_tol=1.0)
        print(f"   dt {dt:.4f}: E(40) = {r['E_steps'][-1]:.10f}, drift {r['energy_drift']:.2e}")
    print("3. Scalar polarization tail: chi_tail vs grid reach K (static, e = m = 1); e^2/(8 pi K^2) for comparison")
    for K in (20.0, 40.0, 80.0):
        print(f"   K = {K:4.0f}: chi_tail = {_chi_static_window(1, 1, 'scalar', -1e12, -K) * 2:.3e} "
              f"(estimate {1 / (8 * PI * K * K):.3e})")
    print("4. HBG parameters (e/m = 0.3, E0 = Ec): first upward zero crossing of E vs grid spacing dk.")
    print("   The infinite-line answer needs t <= pi/dk; coarser grids give the finite ring of length 2 pi/dk.")
    Ec = 1.0 / 0.3
    for dk in (0.0625, 0.03125, 0.015625):
        t0 = time.time()
        kn = np.arange(-45.0, 15.0 + 1e-9, dk)
        r = qed2_backreaction(1.0, 0.3, Ec, 200.0, "spinor", k_nodes=kn, k_weights=np.full(kn.size, dk), dt=0.02,
                              record_every=10)
        tt, EE = r["t_steps"], r["E_steps"]
        iu = np.where((tt[:-1] > 50.0) & (EE[:-1] < 0) & (EE[1:] >= 0))[0]
        tc = tt[iu] - EE[iu] * (tt[iu + 1] - tt[iu]) / (EE[iu + 1] - EE[iu])
        print(f"   dk {dk:.5f} (pi/dk = {PI / dk:6.1f}): first upward crossing t = {tc[0] if tc.size else float('nan'):.2f}, min E/Ec = "
              f"{r['E_steps'].min() / Ec:.4f}  ({time.time() - t0:.0f} s)")
    print("5. HBG's own box, a ring of L = 19.2/m (dk = 2 pi/L), to t = 800/m: plasma periods and amplitude.")
    print("   HBG 2013 quote: 'In our case E ≃ Ec/2 = m2/2e during these times such that with Ω ≃ πm/50 for the")
    print("   employed coupling e/m = 0.3' (Wilson lattice fermions, a_s = 0.075/m).")
    dk = 2 * PI / 19.2
    kn = dk * np.arange(int(math.floor(-60 / dk)), int(math.ceil(30 / dk)) + 1)
    r = qed2_backreaction(1.0, 0.3, Ec, 800.0, "spinor", k_nodes=kn, k_weights=np.full(kn.size, dk), dt=0.02,
                          record_every=10)
    P = oscillation_period(r["t_steps"], r["E_steps"], t_min=50.0)
    late = r["t_steps"] > 300
    print(f"   periods {np.round(P['periods'], 1)} (2 pi/periods: {np.round(2 * PI / P['periods'], 4)}; pi/50 = "
          f"{PI / 50:.4f}); max |E|/Ec after t = 300: {np.abs(r['E_steps'][late]).max() / Ec:.3f}")
    print("   Mean field on HBG's ring (continuum dispersion): the period falls from ~125/m to ~63/m as pairs accumulate")
    print("   (HBG: 'The oscillation frequency Ω increases with the number of produced fermions'), bracketing 100/m;")
    print("   the amplitude stays ~0.7-0.8 Ec, larger than HBG's 'E ≃ Ec/2' (not reproduced; their Wilson-lattice")
    print("   dispersion at a_s = 0.075/m differs from the continuum at the momenta p ~ 25 m the pairs reach).")
    return 0


# ---------------------------------------------------------------- command line
def _mass_inputs(names_texts: dict) -> tuple:
    """Parse energies: all bare numbers (one natural unit) or all with energy units (converted to eV)."""
    from unit_tools import Q
    vals, units = {}, []
    for name, text in names_texts.items():
        try:
            vals[name] = float(text)
            units.append(False)
        except ValueError:
            vals[name] = Q(text).expect("energy").si / E_CHARGE
            units.append(True)
    if any(units) and not all(units):
        raise ValueError("give " + ", ".join(names_texts) + " either all as bare numbers (one natural unit) "
                         "or all with energy units (e.g. '0.511 MeV')")
    return vals, all(units)


def _time_input(text, si_units: bool) -> float:
    try:
        return float(text)
    except ValueError:
        from unit_tools import Q
        if not si_units:
            raise ValueError("a time with units needs m, e, E0 with energy units too") from None
        return qp.time_to_inverse_eV(Q(text).expect("time").si)


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("selftest")
    qq = sub.add_parser("qed2", help="initial field E0, back-reaction on: oscillation period and pairs per length")
    for name in ("m", "e", "E0"):
        qq.add_argument(f"--{name}", required=True, help="a mass: bare number in your unit, or e.g. '0.511 MeV'")
    qq.add_argument("--t", help="time span (default min(6 x 2 pi/mu, 200/max(m, sqrt(eE0)))): bare number in "
                                "1/unit, or e.g. '1e-19 s'")
    qq.add_argument("--scalar", action="store_true", help="charged scalars instead of Dirac fermions")
    qq.add_argument("--kmax", type=float, help="half-width of the momentum grid (same unit as m)")
    qq.add_argument("--dk", type=float, help="grid spacing (same unit as m)")
    qq.add_argument("--dt", type=float, help="time step (1/unit)")
    qq.add_argument("--finite-ring", action="store_true", help="accept t > pi/dk (answer for a ring of length 2 pi/dk)")
    sp = sub.add_parser("screen", help="weak external Sauter pulse E0 sech^2(t/tau): self-consistent field vs "
                                       "linear response, and the polarization 'pairs' trap")
    for name in ("m", "e", "E0"):
        sp.add_argument(f"--{name}", required=True, help="a mass (bare number or energy with units)")
    sp.add_argument("--tau", required=True, help="pulse time: bare number in 1/unit, or e.g. '1e-20 s'")
    sp.add_argument("--scalar", action="store_true")
    rp = sub.add_parser("rate", help="constant field in 1+1: pair-number rate vs vacuum-decay rate per length")
    rp.add_argument("--m", required=True, help="mass (bare number or energy with units)")
    rp.add_argument("--eE", required=True, help="eE (mass^2): bare number, or e.g. '0.25 MeV^2'")
    rp.add_argument("--scalar", action="store_true")
    sub.add_parser("convergence", help="slow studies: step size, grid spacing (finite ring), HBG comparison")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "selftest":
            return 0 if selftest() else 1
        if args.cmd == "convergence":
            return _convergence()
        field = "scalar" if args.scalar else "spinor"
        if args.cmd == "rate":
            from unit_tools import Q
            vals, si = _mass_inputs({"m": args.m})
            try:
                eE = float(args.eE)
                if si:
                    raise ValueError("give eE with units (e.g. '0.25 MeV^2') when m has units")
            except ValueError as exc:
                if "give eE" in str(exc):
                    raise
                if not si:
                    raise ValueError("give m with units too when eE has units") from None
                eE = Q(args.eE).expect("J^2").si / E_CHARGE ** 2
            r = pair_rates_constant_field(vals["m"], eE, field)
            u = " eV^2" if si else " (mass^2)"
            print(f"{field} QED2, m = {vals['m']:.6g}, eE = {eE:.6g}: per-mode occupation n = exp(-pi m^2/eE) = {r['n_mode']:.6g}")
            print(f"pair-number rate (mean PAIRS per length per time, in-in) Gamma = {r['pair_rate']:.6g}{u}"
                  + (f" = {r['pair_rate'] * E_CHARGE / (HBAR * C) * E_CHARGE / HBAR:.6g} m^-1 s^-1" if si else ""))
            print(f"vacuum-decay rate (in-out, P(vacuum) = exp(-w L T)) w = {r['decay_rate']:.6g}{u}; w/Gamma = {r['ratio']:.6f}")
            return 0
        vals, si = _mass_inputs({"m": args.m, "e": args.e, "E0": args.E0})
        m, e, E0 = vals["m"], vals["e"], vals["E0"]
        mu = schwinger_boson_mass(e)
        unit = "eV" if si else "(your mass unit)"
        if args.cmd == "screen":
            tau = _time_input(args.tau, si)
            r = qed2_backreaction(m, e, 0.0, 8 * tau, field, t0=-8 * tau,
                                  E_ext=lambda t: E0 / math.cosh(t / tau) ** 2)
            E_pk = float(np.interp(0.0, r["t_steps"], r["E_steps"]))
            lin = float(screened_sauter_field(0.0, m, e, E0, tau, field)[0])
            n_pk = float(np.interp(0.0, r["t"], r["pairs"]))
            print(f"{field} QED2, m = {m:.6g}, e = {e:.6g}, E0 = {E0:.6g} {unit}, tau = {tau:.6g}; eE0/m^2 = {e * E0 / m**2:.3g}")
            print(f"peak total field / E0: self-consistent {E_pk / E0:.8f}, linear response {lin / E0:.8f}, "
                  f"static 1/eps {1 / dielectric_constant(m, e, field):.8f}")
            print(f"adiabatic 'pairs' per length at the peak {n_pk:.4g} (vacuum polarization estimate "
                  f"{adiabatic_polarization_pairs(m, e * E_pk, field):.4g}); after the pulse {r['pairs'][-1]:.3g}: "
                  "the peak value is transient polarization, not pairs")
            return 0
        t_span = _time_input(args.t, si) if args.t else min(6 * 2 * PI / mu, 200.0 / max(m, math.sqrt(abs(e * E0))))
        r = qed2_backreaction(m, e, E0, t_span, field, k_max=args.kmax, dk=args.dk, dt=args.dt,
                              finite_ring=args.finite_ring)
        print(f"{field} QED2 with back-reaction, m = {m:.6g}, e = {e:.6g}, E0 = {E0:.6g} {unit}; eE0/m^2 = "
              f"{e * E0 / m**2:.4g}; massless-limit frequency mu = e/sqrt(pi) = {mu:.6g}")
        print(f"grid: {r['k'].size} modes, dt = {r['dt']:.4g}, {r['steps']} steps; energy drift {r['energy_drift']:.2e}; "
              f"t = {t_span:.6g}")
        P = None
        for how in ("up", "any"):
            try:
                P = oscillation_period(r["t_steps"], r["E_steps"], direction=how)
                break
            except ValueError:
                pass
        if P is not None:
            per = f"{P['period']:.6g}" + (f" /eV = {qp.time_from_inverse_eV(P['period']):.4g} s" if si else "")
            what = "full periods" if how == "up" else "half-periods x 2"
            print(f"oscillation period of E(t) (mean of {len(P['periods'])} {what}): {per}  (2 pi/mu = {2 * PI / mu:.6g}); "
                  f"zero crossings at t = {np.array2string(P['crossings'], precision=4)}")
        else:
            print(f"fewer than three zero crossings of E within t = {t_span:.4g}: no period (try --t larger)")
        npair = r["pairs"][-1]
        print(f"pairs per length at the end {npair:.6g}" + (f" eV = {length_density_to_SI(npair):.4g} m^-1" if si else "")
              + f" (max {r['pairs'].max():.6g}); E(end)/E0 = {r['E_steps'][-1] / E0:.4f}")
        print("('pairs' are counted in the instantaneous adiabatic basis: while E != 0 they include transient polarization)")
    except (ValueError, KeyError) as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
