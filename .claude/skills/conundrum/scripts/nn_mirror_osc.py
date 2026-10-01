#!/usr/bin/env python3
"""Neutron -> mirror-neutron (n -> n') conversion: probabilities, resonance passage and lifetime shifts.

SPECULATIVE PHYSICS. The mirror sector is a beyond-Standard-Model hypothesis (Berezhiani). This tool
computes what the hypothesis predicts; it says nothing about whether it is true.

MODEL (energies in joules in the Python API; "hbar = 1" formulas below are written with hbar shown)
-------------------------------------------------------------------------------------------------
Two-level system for one neutron spin state s = +1 or -1 along a field axis, basis (|n>, |n'>):

    H_s = [[ 0      , eps           ],
           [ eps    , delta_s(t)    ]]          (common diagonal energy dropped)

    eps        = hbar / tau_nn'                   mass mixing (J); tau_nn' = oscillation time (s)
    delta_s    = Delta_m - s*|mu_n|*(B - B'_par)  detuning (J); Delta_m = m_n' - m_n (J),
                                                  B = ordinary field magnitude (T) felt by n,
                                                  B'_par = mirror field along the same axis (T) felt by n'
    |mu_n|     = 9.6623651e-27 J/T (CODATA 2018) = 60.3077 neV/T
    theta      = mixing angle, tan(2 theta) = 2 eps / delta_s   (Berezhiani 2019 eq. 13 with B' = 0:
                 tan 2theta_B^{+-} = 2 eps / (Delta_m -+ Omega_B), Omega_B = |mu_n B|)
    theta_0    = vacuum mixing angle, tan(2 theta_0) = 2 eps / Delta_m  (theta_0 ~ eps/Delta_m)

1. Constant field, flight time t (Rabi formula, exact for the 2x2 problem):
       P(t) = [4 eps^2 / (delta^2 + 4 eps^2)] * sin^2( sqrt(delta^2 + 4 eps^2) * t / (2 hbar) )
   Time average: <P> = (1/2) sin^2(2 theta) = 2 eps^2 / (delta^2 + 4 eps^2).
   Small-time limit (|delta| t/hbar << 1, t << tau): P = (t / tau_nn')^2.
   Large-field limit (|delta| t/hbar >> 1): <P> = 2 eps^2/delta^2 = 2 hbar^2/(tau^2 delta^2).

2. Degenerate mirror model (Delta_m = 0) with a mirror field B' at angle beta to B (4x4 problem,
   first order in eps, averaged over the initial spin, summed over final spins) -- Abel et al. 2021
   eq. (2), with omega = |mu_n B|/(2 hbar), omega' = |mu_n B'|/(2 hbar):
       P = S(-) + S(+) + cos(beta) * (S(-) - S(+)),
       S(-+) = sin^2((omega -+ omega') t) / (2 tau^2 (omega -+ omega')^2)
   `prob_mirror_field` gives this closed form; `prob_4x4_constant` solves the full 4x4 problem
   exactly (any Delta_m, any directions of B and B') by diagonalisation.

3. Passage through a slowly varying field B(z) at speed v:
   - Landau-Zener (linear sweep through delta = 0, starting and ending far from resonance):
         P(n -> n') = 1 - exp( -2 pi eps^2 / (hbar |d delta/dt|) ),
         |d delta/dt| = |mu_n| |dB/dz| v at the resonance point.
     Small-eps limit: P = 2 pi eps^2 / (hbar |d delta/dt|).
     Berezhiani's adiabaticity parameter xi = Delta_m sin^2(2 theta_0) R / (hbar v), with
     R = B / (dB/dz) at resonance, satisfies exp(-pi xi / 2) = exp(-2 pi Gamma_LZ) exactly when
     eps << Delta_m (checked in selftest).
   - Adiabatic evolution with at most one resonance crossing (Berezhiani 2019 eq. 17-19, the
     neutrino "Parke" form), oscillations averaged out:
         P(z) = 1/2 - (1/2 - P_jump) cos(2 theta_i) cos(2 theta(z)),
     P_jump = exp(-2 pi Gamma_LZ) if the resonance was crossed, else 0; theta_i = mixing angle
     at the entry point.
   - `evolve_profile` integrates the 2x2 Schroedinger equation along a trajectory exactly for
     piecewise-constant H (step error O(dt^2)); it refuses step sizes with phase > 0.2 rad.

4. Beam experiment (proton counting, Berezhiani 2019 eq. 16): proton rate is proportional to the
   neutron (not n') density in the trap, fluence from the monitor at low field, so
       tau_beam / tau_beta = (1 - P_det) / (1 - P_trap),
   P_trap = conversion probability averaged over the decay (trap) region, P_det at the monitor.
   Velocity averaging: weight each velocity by the neutron DENSITY in the beam (flux(v)/v), since
   both the trap decay rate and a 1/v fluence monitor measure density.

5. UCN trap (material bottle): each wall reflection projects the neutron back onto |n> (an n'
   passes through the wall). With free-flight times t_f between collisions:
       loss per collision  = <P(t_f)>  (averaged over the free-flight-time distribution)
       loss rate           = <P(t_f)> / <t_f>          (s^-1),  Abel et al. 2021: exp(-m_s <P>),
                                                         m_s = t_s / t_f
       apparent lifetime   = 1 / (1/tau_n + loss rate).
   Magnetic trap (no walls): the tool offers two explicitly labelled effective models, both
   ASSUMPTIONS rather than derivations: (a) incoherent Landau-Zener losses at resonance crossings,
   rate = crossings per second x P_LZ; (b) a decoherence-time model, rate = <P(t_c)>/t_c.

ASSUMPTIONS AND VALIDITY
- Non-relativistic neutron; the spin follows the field adiabatically (spin-flip handled only in
  the 4x4 constant-field solver); neutron decay ignored during the flight (t << 880 s).
- Matter optical potentials are not included (vacuum or gas-free flight paths).
- B' is a mirror magnetic field of unknown size/direction; Delta_m of either sign is allowed.
- Landau-Zener formula needs a locally linear sweep and endpoints far from resonance
  (|delta| >> eps); the analytic profile formula handles 0 or 1 crossing and raises ValueError
  otherwise (use `evolve_profile`).
- Probabilities from first-order formulas (Abel eq. 2) need P << 1.

UNITS: SI in the Python API (J, s, T, m, m/s). Helpers: NEV (1 neV in J), eps_from_tau, tau_from_eps.
The command line accepts unit strings through unit_tools.Q ("280 neV", "4.6 T", "1 ms").

PYTHON
    import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
    import nn_mirror_osc as m
    eps = m.eps_from_tau(10.0)                                  # tau_nn' = 10 s
    m.rabi_probability(0.1, eps, 0.0)                           # ~ (0.1/10)^2 = 1e-4
    m.landau_zener(eps, m.MU_N * 10.0 * 5.0)                    # dB/dz = 10 T/m at 5 m/s
    m.beam_solenoid(dm=280*m.NEV, theta0=1e-3, B_center=4.6, v=1000.0)

COMMAND LINE
    python3 .claude/skills/conundrum/scripts/nn_mirror_osc.py selftest
    python3 .claude/skills/conundrum/scripts/nn_mirror_osc.py beam --dm "280 neV" --theta0 1e-3 --B "4.6 T" --v "1000 m/s"
    python3 .claude/skills/conundrum/scripts/nn_mirror_osc.py rabi --tau "10 s" --t "0.1 s" --dm "0 neV" --B "1 uT"
    python3 .claude/skills/conundrum/scripts/nn_mirror_osc.py lz --tau "1 s" --dBdz "10 T/m" --v "5 m/s"
    python3 .claude/skills/conundrum/scripts/nn_mirror_osc.py ucn --tau "10 s" --tf "0.05 s" --B "0 T" --Bp "0 T"
"""
from __future__ import annotations

import argparse
import math
import sys

import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from unit_tools import HBAR, E_CHARGE, Q  # noqa: E402

# |mu_n|, CODATA 2018: mu_n = -9.6623651(23)e-27 J/T. Cross-checked in selftest against two
# independent published conversions (Abel et al. 2021 and Berezhiani 2019).
MU_N = 9.6623651e-27          # J/T
NEV = 1e-9 * E_CHARGE          # 1 neV in J
PEV = 1e-12 * E_CHARGE         # 1 peV in J
MAX_STEPS = 5_000_000


# ------------------------------------------------------------------ basic conversions
def eps_from_tau(tau: float) -> float:
    """Mixing energy eps = hbar / tau_nn' (J) from the oscillation time (s)."""
    if not tau > 0:
        raise ValueError("tau_nn' must be > 0 s")
    return HBAR / tau


def tau_from_eps(eps: float) -> float:
    if not eps > 0:
        raise ValueError("eps must be > 0 J")
    return HBAR / eps


def eps_from_theta0(theta0: float, dm: float) -> float:
    """eps from the vacuum mixing angle: tan(2 theta0) = 2 eps / Delta_m."""
    if not 0 < theta0 < math.pi / 4:
        raise ValueError("theta0 must be in (0, pi/4)")
    if dm == 0:
        raise ValueError("theta0 is undefined for Delta_m = 0; give tau or eps instead")
    return 0.5 * abs(dm) * math.tan(2 * theta0)


def zeeman(B: float) -> float:
    """Omega_B = |mu_n| B in J (B in T)."""
    return MU_N * abs(B)


def omega_half(B: float) -> float:
    """Abel et al. notation omega = |mu_n B| / (2 hbar) in rad/s."""
    return MU_N * abs(B) / (2 * HBAR)


def resonance_field(dm: float, Bp_par: float = 0.0) -> float:
    """Field magnitude (T) at which delta = 0 for the resonant spin state: |B - B'| = |Delta_m|/|mu_n|."""
    return abs(dm) / MU_N + Bp_par


def detuning(dm: float, B: float, s: int = +1, Bp_par: float = 0.0) -> float:
    """delta_s = Delta_m - s |mu_n| (B - B'_par)  (J). s = +1 or -1 labels the spin state."""
    if s not in (+1, -1):
        raise ValueError("s must be +1 or -1")
    return dm - s * MU_N * (B - Bp_par)


def mixing_angle(eps: float, delta: float) -> float:
    """theta in [0, pi/2], tan(2 theta) = 2 eps / delta."""
    return 0.5 * math.atan2(2 * eps, delta)


# ------------------------------------------------------------------ constant field
def rabi_probability(t, eps: float, delta: float):
    """Exact two-level P(n -> n') after time t (s) in a constant field (Rabi formula)."""
    t = np.asarray(t, dtype=float)
    if np.any(t < 0):
        raise ValueError("time must be >= 0")
    if eps < 0:
        raise ValueError("eps must be >= 0")
    W = math.sqrt(delta * delta + 4 * eps * eps)
    if W == 0:
        return np.zeros_like(t) if t.ndim else 0.0
    out = (4 * eps * eps / (W * W)) * np.sin(W * t / (2 * HBAR)) ** 2
    return out if out.ndim else float(out)


def rabi_time_average(eps: float, delta: float) -> float:
    """<P> = (1/2) sin^2(2 theta) = 2 eps^2 / (delta^2 + 4 eps^2)."""
    return 2 * eps * eps / (delta * delta + 4 * eps * eps)


def spin_averaged_rabi(t, eps: float, dm: float, B: float, Bp_par: float = 0.0):
    """Unpolarised average over s = +-1 of the collinear-field Rabi probability."""
    return 0.5 * (rabi_probability(t, eps, detuning(dm, B, +1, Bp_par))
                  + rabi_probability(t, eps, detuning(dm, B, -1, Bp_par)))


def prob_mirror_field(t, tau: float, B: float, Bp: float, cos_beta: float):
    """Abel et al. 2021 eq. (2): degenerate (Delta_m = 0) n-n' probability, first order in 1/tau,
    unpolarised, B and B' at angle beta. t in s, tau in s, B and B' magnitudes in T."""
    if not -1 <= cos_beta <= 1:
        raise ValueError("cos_beta must be in [-1, 1]")
    t = np.asarray(t, dtype=float)
    w, wp = omega_half(B), omega_half(Bp)

    def S(x):
        if x == 0:
            return t * t / (2 * tau * tau)
        return np.sin(x * t) ** 2 / (2 * tau * tau * x * x)
    Sm, Sp = S(w - wp), S(w + wp)
    out = Sm + Sp + cos_beta * (Sm - Sp)
    return out if np.ndim(out) else float(out)


def _pauli_dot(v):
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    return v[0] * sx + v[1] * sy + v[2] * sz


def prob_4x4_constant(t: float, eps: float, dm: float, Bvec, Bpvec) -> float:
    """Exact unpolarised P(n -> n', any spin) for constant vector fields B (felt by n) and B'
    (felt by n'), by diagonalising H = [[|mu| s.B, eps], [eps, dm + |mu| s.B']] (4x4)."""
    if t < 0:
        raise ValueError("t must be >= 0")
    H = np.zeros((4, 4), dtype=complex)
    H[:2, :2] = MU_N * _pauli_dot(np.asarray(Bvec, float))
    H[2:, 2:] = dm * np.eye(2) + MU_N * _pauli_dot(np.asarray(Bpvec, float))
    H[:2, 2:] = eps * np.eye(2)
    H[2:, :2] = eps * np.eye(2)
    w, V = np.linalg.eigh(H)
    U = V @ np.diag(np.exp(-1j * w * t / HBAR)) @ V.conj().T
    return float(0.5 * np.sum(np.abs(U[2:, :2]) ** 2))


# ------------------------------------------------------------------ resonance passage
def landau_zener(eps: float, ddelta_dt: float) -> float:
    """P(n -> n') for a linear sweep of the detuning through resonance at rate ddelta_dt (J/s):
    1 - exp(-2 pi eps^2 / (hbar |d delta/dt|))."""
    if ddelta_dt == 0:
        raise ValueError("sweep rate is zero: no Landau-Zener passage (use the Rabi formula)")
    return -math.expm1(-2 * math.pi * eps * eps / (HBAR * abs(ddelta_dt)))


def landau_zener_field(eps: float, dBdz: float, v: float) -> float:
    """Landau-Zener conversion for a neutron at speed v (m/s) crossing a resonance where the
    field gradient along its path is dBdz (T/m): d delta/dt = |mu_n| |dB/dz| v."""
    if not v > 0:
        raise ValueError("v must be > 0")
    return landau_zener(eps, MU_N * dBdz * v)


def lz_numeric(gamma: float, half_span: float = 400.0, n_steps: int = 800_000,
               avg_from: float = 0.4) -> float:
    """Numerical check of Landau-Zener: sweep delta linearly from -half_span*eps to +half_span*eps
    with Gamma = eps^2/(hbar |d delta/dt|) = gamma, start in |n>, and return P(n') averaged over the
    part of the sweep with delta > avg_from * half_span * eps (removes the finite-sweep ripple)."""
    eps = HBAR * 1.0e3
    rate = eps * eps / (HBAR * gamma)
    v, Bres = 1.0, 0.5
    dBdz = rate / MU_N
    zmax = half_span * eps / rate
    zg, Pg = evolve_profile(lambda zz: Bres + dBdz * zz, -zmax, zmax, v, eps, MU_N * Bres, +1,
                            n_steps=n_steps, record=True)
    return float(np.mean(Pg[zg > avg_from * zmax]))


def berezhiani_xi(dm: float, theta0: float, R: float, v: float) -> float:
    """xi = Delta_m sin^2(2 theta0) R / (hbar v), R = B/(dB/dz) at resonance (m)."""
    return abs(dm) * math.sin(2 * theta0) ** 2 * R / (HBAR * v)


def parke_probability(theta_i: float, theta_f: float, P_jump: float) -> float:
    """Oscillation-averaged P(n -> n') after adiabatic evolution with jump probability P_jump at
    the crossing (0 if none): 1/2 - (1/2 - P_jump) cos 2theta_i cos 2theta_f (Berezhiani eq. 19)."""
    if not 0 <= P_jump <= 1:
        raise ValueError("P_jump must be in [0, 1]")
    return 0.5 - (0.5 - P_jump) * math.cos(2 * theta_i) * math.cos(2 * theta_f)


def solenoid_field(z, B_center: float, length: float, radius: float):
    """On-axis field (T) of a finite ideal solenoid, normalised to B_center at z = 0."""
    def raw(zz):
        a, b = zz + length / 2, zz - length / 2
        return 0.5 * (a / np.sqrt(a * a + radius * radius) - b / np.sqrt(b * b + radius * radius))
    return B_center * raw(np.asarray(z, float)) / raw(0.0)


def evolve_profile(Bfunc, z0: float, z1: float, v: float, eps: float, dm: float, s: int = +1,
                   Bp_par: float = 0.0, n_steps: int = 100_000, record: bool = False):
    """Integrate i hbar dpsi/dt = H_s(t) psi along z = z0 + v t, starting in |n>.
    Exact propagator for piecewise-constant H at step midpoints. Returns P(n->n') at z1, or
    (z_grid, P_grid) if record. Raises ValueError if the phase per step exceeds 0.2 rad."""
    if not v > 0 or z1 <= z0:
        raise ValueError("need v > 0 and z1 > z0")
    if n_steps > MAX_STEPS:
        raise ValueError(f"n_steps > {MAX_STEPS}: use the analytic (adiabatic/LZ) formulas")
    dz = (z1 - z0) / n_steps
    dt = dz / v
    zm = z0 + (np.arange(n_steps) + 0.5) * dz
    delta = dm - s * MU_N * (np.asarray(Bfunc(zm), float) - Bp_par)
    W = np.sqrt(delta ** 2 + 4 * eps ** 2)
    phase = W * dt / (2 * HBAR)
    if phase.max() > 0.2:
        raise ValueError(f"phase per step {phase.max():.3g} rad > 0.2: raise n_steps to "
                         f">= {int(n_steps * phase.max() / 0.1) + 1}")
    # H = (delta/2) I + h.sigma with h = (eps, 0, -delta/2); U = e^{-i delta dt/2hbar}(cos - i sin n.sigma)
    c = np.cos(phase)
    sn = np.where(W > 0, np.sin(phase) / np.where(W > 0, W, 1.0), 0.0)
    g = np.exp(-1j * delta * dt / (2 * HBAR))
    u11 = g * (c + 1j * sn * delta)           # n.sigma_z = -delta/W
    u22 = g * (c - 1j * sn * delta)
    u12 = g * (-1j * sn * 2 * eps)
    a, b = 1.0 + 0j, 0.0 + 0j
    if record:
        P = np.empty(n_steps)
    for k in range(n_steps):
        a, b = u11[k] * a + u12[k] * b, u12[k] * a + u22[k] * b
        if record:
            P[k] = (b.real * b.real + b.imag * b.imag)
    if record:
        return zm + dz / 2, P
    return float(b.real * b.real + b.imag * b.imag)


def profile_probability_analytic(Bfunc, z_start: float, z: float, v: float, eps: float, dm: float,
                                 s: int = +1, Bp_par: float = 0.0, n_grid: int = 20001,
                                 incoherent_multi: bool = False) -> float:
    """Oscillation-averaged P(n->n') at z for spin s after flying from z_start (Parke/Berezhiani
    eq. 19): adiabatic, with a Landau-Zener hop between adiabatic branches at each resonance
    crossing, P = 1/2 - 1/2 (1 - 2 p_hop) cos 2theta_i cos 2theta_f.
    One crossing: p_hop = P_jump = exp(-2 pi eps^2/(hbar |d delta/dt|)) (exactly Berezhiani eq. 19).
    Several crossings: phases between crossings interfere; only with incoherent_multi=True (an
    ASSUMPTION valid after averaging over a velocity spread) are hops composed classically,
    p <- p (1 - q) + (1 - p) q. Otherwise raises ValueError."""
    if z <= z_start:
        raise ValueError("need z > z_start")
    zg = np.linspace(z_start, z, n_grid)
    d = dm - s * MU_N * (np.asarray(Bfunc(zg), float) - Bp_par)
    th_i = mixing_angle(eps, d[0])
    th_f = mixing_angle(eps, d[-1])
    crossings = np.nonzero(np.sign(d[:-1]) * np.sign(d[1:]) < 0)[0]
    if len(crossings) > 1 and not incoherent_multi:
        raise ValueError("more than one resonance crossing: phases interfere; use evolve_profile "
                         "or incoherent_multi=True")
    p_hop = 0.0
    for k in crossings:
        ddz = (d[k + 1] - d[k]) / (zg[k + 1] - zg[k])       # J/m
        q = math.exp(-2 * math.pi * eps * eps / (HBAR * abs(ddz) * v))
        p_hop = p_hop * (1 - q) + (1 - p_hop) * q
    return parke_probability(th_i, th_f, p_hop)


# ------------------------------------------------------------------ experiments
def beam_lifetime_ratio(P_trap: float, P_det: float) -> float:
    """tau_beam / tau_beta = (1 - P_det) / (1 - P_trap)  (Berezhiani 2019 eq. 16 form)."""
    for p in (P_trap, P_det):
        if not 0 <= p < 1:
            raise ValueError("probabilities must be in [0, 1)")
    return (1 - P_det) / (1 - P_trap)


def beam_solenoid(dm: float, theta0: float | None = None, B_center: float = 4.6, v=1000.0,
                  weights=None, eps: float | None = None, length: float = 0.6, radius: float = 0.05,
                  z_start: float = -1.5, trap: tuple = (-0.1, 0.1), z_det: float = 1.5,
                  Bp_par: float = 0.0, n_trap: int = 41) -> dict:
    """Apparent-lifetime shift of a proton-counting beam experiment whose decay volume sits in a
    solenoid (Berezhiani's Fig. 1 geometry by default: 60 cm long, 10 cm diameter, 4.6 T).
    Uses the oscillation-averaged adiabatic + Landau-Zener formula for each spin and velocity;
    velocities weighted by beam density (pass flux(v)/v as weights). Returns P_trap, P_det and
    tau_beam/tau_beta."""
    if eps is None:
        if theta0 is None:
            raise ValueError("give theta0 or eps")
        eps = eps_from_theta0(theta0, dm)
    vs = np.atleast_1d(np.asarray(v, float))
    w = np.ones_like(vs) if weights is None else np.asarray(weights, float)
    if np.any(vs <= 0) or np.any(w < 0) or w.sum() <= 0:
        raise ValueError("velocities must be > 0 and weights >= 0")
    w = w / w.sum()
    B = lambda zz: solenoid_field(zz, B_center, length, radius)  # noqa: E731
    zt = np.linspace(trap[0], trap[1], n_trap)
    Ptr, Pdt = 0.0, 0.0
    for vi, wi in zip(vs, w):
        for s in (+1, -1):
            p_trap = np.mean([profile_probability_analytic(B, z_start, zz, vi, eps, dm, s, Bp_par)
                              for zz in zt])
            # detector (monitor) after the solenoid: if B_center > B_res the path crosses the
            # resonance twice; hops composed incoherently (velocity spread averages the phase)
            p_det = profile_probability_analytic(B, z_start, z_det, vi, eps, dm, s, Bp_par,
                                                 incoherent_multi=True)
            Ptr += 0.5 * wi * p_trap
            Pdt += 0.5 * wi * p_det
    return {"eps_J": eps, "tau_nn_s": HBAR / eps, "P_trap": Ptr, "P_det": Pdt,
            "tau_beam_over_tau_beta": beam_lifetime_ratio(Ptr, Pdt),
            "B_res_T": resonance_field(dm, Bp_par)}


def ucn_loss(eps: float, delta_list, t_f_samples, t_f_weights=None) -> dict:
    """Material-bottle loss: <P(t_f)> per wall collision, averaged over free-flight times and over
    the detunings in delta_list (e.g. both spin states), and loss rate <P>/<t_f> in s^-1."""
    t = np.asarray(t_f_samples, float)
    if np.any(t <= 0):
        raise ValueError("free-flight times must be > 0")
    w = np.ones_like(t) if t_f_weights is None else np.asarray(t_f_weights, float)
    w = w / w.sum()
    P = np.mean([np.sum(w * rabi_probability(t, eps, d)) for d in delta_list])
    tf = float(np.sum(w * t))
    return {"P_per_collision": float(P), "mean_tf_s": tf, "loss_rate_per_s": float(P) / tf}


def apparent_lifetime(tau_n: float, loss_rate: float) -> float:
    """1 / (1/tau_n + loss_rate)."""
    if not tau_n > 0 or loss_rate < 0:
        raise ValueError("tau_n > 0 and loss_rate >= 0 required")
    return 1.0 / (1.0 / tau_n + loss_rate)


def lz_crossing_loss_rate(eps: float, dBdz: float, v: float, crossings_per_s: float) -> float:
    """Magnetic-trap effective model (ASSUMPTION: incoherent crossings, n' escapes before the next
    one): rate = crossings/s x P_LZ."""
    return crossings_per_s * landau_zener_field(eps, dBdz, v)


def regeneration_probability(P1: float, P2: float) -> float:
    """Wall-less regeneration n -> n' -> n through two field regions (ORNL/SNS type): P1 * P2."""
    return P1 * P2


# ------------------------------------------------------------------ self-test
def selftest(verbose: bool = True) -> bool:
    ok = True

    def check(name, got, ref, rel=None, abs_=None):
        nonlocal ok
        if abs_ is not None:
            good = abs(got - ref) <= abs_
        else:
            good = abs(got - ref) <= rel * abs(ref)
        ok &= good
        if verbose:
            print(f"{'PASS' if good else 'FAIL'}  {name}: got {got:.6g}, ref {ref:.6g}")

    # 1. Constant: omega = |mu_n B|/2 in Abel et al. 2021 (PLB 812, 135993; arXiv:2009.11046 p. 2):
    #    "!(¤) = ðnB(¤)ð∕2 = 45.81( µT ⋅s)−1B(¤)"  -> 45.81 rad/s per uT.
    check("omega/B = |mu_n|/(2 hbar) vs Abel 2021: 45.81 /(uT s)", omega_half(1e-6), 45.81, rel=2e-4)
    # 2. Constant: Berezhiani 2019 (EPJC 79, 484; arXiv:1807.07906):
    #    "B res = |∆m/µn| = (∆m/100 nev)× 1.66 T"
    check("B_res(100 neV) vs Berezhiani 2019: 1.66 T", resonance_field(100 * NEV), 1.66, rel=3e-3)

    # 3. Small-time limit P = (t/tau)^2 (degenerate, zero field). Abel 2021 eq. (2) with B = B' = 0
    #    reduces to sin^2(0)/0 -> t^2/tau^2; exact Rabi at delta = 0 is sin^2(t/tau).
    tau = 5.0
    check("Rabi small-time limit (t/tau)^2 at t = 0.01 s, tau = 5 s",
          rabi_probability(0.01, eps_from_tau(tau), 0.0), (0.01 / tau) ** 2, rel=1e-4)
    # 3b. exact definition at resonance: P = sin^2(t/tau) (full Rabi flop at t = pi tau / 2)
    check("Rabi full flop at t = pi tau/2, delta = 0", rabi_probability(math.pi * tau / 2, eps_from_tau(tau), 0.0),
          1.0, rel=1e-12)

    # 3c. Rabi formula, exact values. Wikipedia "Rabi cycle" (fetched 2026-09-30): "P + → − = ω 1 2
    #     Ω 2 sin 2 ⁡ ( Ω 2 t ) where Ω = Δ ω 2 + ω 1 2" i.e. P = (w1/W)^2 sin^2(W t/2),
    #     W = sqrt(dw^2 + w1^2). Our H has w1 = 2 eps/hbar, dw = delta/hbar.
    #     delta = 2 sqrt(3) eps -> W = 4 eps/hbar, (w1/W)^2 = 1/4; at W t/2 = pi/2, P = 1/4 exactly.
    #     delta = 2 eps -> (w1/W)^2 = 1/2; at W t/2 = pi/4, P = 1/4 exactly.
    e0 = eps_from_tau(1.0)
    check("Rabi exact: delta = 2 sqrt3 eps, W t/2 = pi/2 -> 1/4",
          rabi_probability(math.pi * HBAR / (4 * e0), e0, 2 * math.sqrt(3) * e0), 0.25, rel=1e-12)
    check("Rabi exact: delta = 2 eps, W t/2 = pi/4 -> 1/4",
          rabi_probability(math.pi / 4 * 2 * HBAR / (math.sqrt(8) * e0), e0, 2 * e0), 0.25, rel=1e-12)
    # 3d. Berezhiani 2019 eq. (9), vacuum time average: "1−Pnn = 1 2 sin2 2θ0 = 2 ε2 δm2"
    #     (delta_m^2 = Delta_m^2 + 4 eps^2 is the eigenvalue gap squared).
    dmv = 100 * NEV
    e1 = eps_from_theta0(1e-3, dmv)
    check("Berezhiani eq.9: <P> = (1/2) sin^2 2theta0 = 2 eps^2/delta_m^2",
          rabi_time_average(e1, dmv), 0.5 * math.sin(2e-3) ** 2, rel=1e-9)

    # 4. Rabi formula vs exact 4x4 diagonalisation (collinear B, Delta_m != 0, off resonance):
    #    the unpolarised 4x4 result must equal the spin average of the two 2x2 Rabi formulas.
    eps = eps_from_tau(0.3)
    dm, B = 0.02 * NEV, 0.2e-3
    for t in (0.001, 0.0123, 0.05):
        check(f"4x4 exact vs spin-averaged Rabi, t = {t} s", prob_4x4_constant(t, eps, dm, (0, 0, B), (0, 0, 0)),
              float(spin_averaged_rabi(t, eps, dm, B)), rel=1e-8)

    # 5. Abel 2021 eq. (2), Delta_m = 0, non-collinear B' (beta = 60 deg), vs exact 4x4 solution.
    #    Quote: "Pnn¤ BB¤(t)= sin2[(!−!¤)t] 2 2 nn¤(!−!¤)2 +sin2[(!+!¤)t] 2 2 nn¤(!+!¤)2 (2)
    #    + H sin2[(!−!¤)t] ... −sin2[(!+!¤)t] ... I cos" (first order in 1/tau: tau = 100 s, P ~ 1e-6)
    tau = 100.0
    Bm, Bpm, beta = 20e-6, 12e-6, math.radians(60)
    Bp_vec = (Bpm * math.sin(beta), 0, Bpm * math.cos(beta))
    for t in (0.02, 0.137):
        check(f"Abel 2021 eq.2 (beta=60 deg) vs 4x4 exact, t = {t} s",
              prob_4x4_constant(t, eps_from_tau(tau), 0.0, (0, 0, Bm), Bp_vec),
              float(prob_mirror_field(t, tau, Bm, Bpm, math.cos(beta))), rel=2e-4)
    # 5b. Abel 2021 eq. (4): "Pnn¤ 0B¤=1∕(2 2 nn¤!¤2) ... valid for !¤t ≫1": time average of eq. 2
    #     over many periods at B = 0 must be 1/(2 tau^2 omega'^2).
    tt = np.linspace(0.5, 1.5, 20001)
    Pbar = float(np.mean([prob_4x4_constant(x, eps_from_tau(tau), 0.0, (0, 0, 0), (0, 0, Bpm)) for x in tt[::200]]))
    # coarse sampling (101 points over ~550 rad of phase): sample-mean error ~ few % -> rel 5e-2
    check("Abel 2021 eq.4, B=0: <P> = 1/(2 tau^2 omega'^2)", Pbar, 1 / (2 * tau**2 * omega_half(Bpm) ** 2), rel=5e-2)

    # 6. Landau-Zener, linear sweep: numerical integration vs closed form.
    #    Wikipedia "Landau-Zener formula" (fetched 2026-09-30): "P D = e − 2 π Γ Γ = a 2 / ℏ |
    #    ∂ ∂ t ( E 2 − E 1 ) |" -- P_D = diabatic (stay-n) probability, so P(n->n') = 1 - P_D.
    eps = HBAR * 1.0e3                     # coupling 1e3 rad/s
    rate = HBAR * 1.0e7                     # d delta/dt = 1e7 rad/s^2 -> Gamma = 0.1
    dBdz = rate / MU_N                      # T/m at v = 1 m/s
    v = 1.0
    Bres = 0.5
    Bf = lambda zz: Bres + dBdz * zz        # noqa: E731
    # Convergence study (lznum subcommand): the step count is converged (0.8M and 1.6M steps agree to
    # 1e-6); the finite-sweep error falls with the sweep half-span: +4.5e-3 at 200 eps, +2.5e-3 at 400 eps,
    # +1.5e-4 at 800 eps. So the sweep runs over +-800 eps and the tolerance is 1e-3 absolute.
    assert abs(rate / MU_N - dBdz) < 1e-12 * dBdz and Bf(0.0) == Bres
    P_num = lz_numeric(0.1, half_span=800.0, n_steps=3_200_000)
    check("Landau-Zener: numeric linear sweep (+-800 eps) vs 1 - exp(-2 pi Gamma), Gamma = 0.1",
          P_num, landau_zener(eps, rate), abs_=1e-3)

    # 7. Berezhiani eq. 19 LZ exponent: exp(-pi xi/2) must equal exp(-2 pi Gamma) when eps << Delta_m.
    #    "P + nn′(z) = 1 2− (1 2−e−πξ/2 ) cos 2θ0 cos 2θ+ B(z)" ; "ξ = ∆m sin2 2θ0v−1R(zres)"
    dm, th0, Rr, vv = 280 * NEV, 1e-3, 0.1, 1000.0
    dBdz_res = resonance_field(dm) / Rr
    check("exp(-pi xi/2) (Berezhiani) vs 1 - P_LZ (Wikipedia form)",
          math.exp(-math.pi * berezhiani_xi(dm, th0, Rr, vv) / 2),
          1 - landau_zener_field(eps_from_theta0(th0, dm), dBdz_res, vv), rel=1e-5)

    # 8. Berezhiani eq. 17/18 (adiabatic, no crossing) vs numerical integration through a solenoid.
    #    "P± nn′(z) = 1 2− 1 2 cos 2θ0 cos 2θ± B(z) (17) where cos 2θ± B = cos 2θ0(1∓ ΩB ∆m ) √
    #    cos2 2θ0(1∓ ΩB ∆m )2 + sin2 2θ0 . (18)" -- paper states numerical solution "gives exactly
    #    the same result as Eq. (17)". Scaled-down parameters so the ODE is cheap: Delta_m = 1 neV,
    #    theta0 = 0.01, B_center = 0.98 B_res, v = 200 m/s.
    dm, th0 = 1.0 * NEV, 0.01
    eps = eps_from_theta0(th0, dm)
    Bc = 0.98 * resonance_field(dm)
    Bsol = lambda zz: solenoid_field(zz, Bc, 0.6, 0.05)  # noqa: E731
    zg, Pg = evolve_profile(Bsol, -1.0, 0.0, 200.0, eps, dm, +1, n_steps=400_000, record=True)
    P_num = float(np.mean(Pg[zg > -0.05]))           # average the fast oscillation near the centre
    x = 1 - MU_N * Bc / dm
    c2B = math.cos(2 * th0) * x / math.sqrt(math.cos(2 * th0) ** 2 * x * x + math.sin(2 * th0) ** 2)
    P_eq17 = 0.5 - 0.5 * math.cos(2 * th0) * c2B
    # residual non-adiabatic ripple from the solenoid fringe: 3% relative allowed
    check("Berezhiani eq.17/18 (adiabatic) vs numeric solenoid passage", P_num, P_eq17, rel=3e-2)
    check("analytic profile routine vs Berezhiani eq.17/18",
          profile_probability_analytic(Bsol, -1.0, 0.0, 200.0, eps, dm, +1), P_eq17, rel=1e-6)
    # 8b. Berezhiani eq. 19 with one resonance crossing in the solenoid fringe (B_center = 1.2 B_res,
    #     theta0 = 0.02, so xi ~ 1 and neither the adiabatic nor the sudden limit applies) vs numeric.
    #     The LZ formula assumes a linear sweep; the fringe field is curved, so 5% relative allowed.
    dm, th0 = 1.0 * NEV, 0.02
    eps = eps_from_theta0(th0, dm)
    Bsol2 = lambda zz: solenoid_field(zz, 1.2 * resonance_field(dm), 0.6, 0.05)  # noqa: E731
    zg, Pg = evolve_profile(Bsol2, -1.0, 0.0, 200.0, eps, dm, +1, n_steps=400_000, record=True)
    P_num = float(np.mean(Pg[zg > -0.05]))
    check("Berezhiani eq.19 (one LZ crossing) vs numeric solenoid passage", P_num,
          profile_probability_analytic(Bsol2, -1.0, 0.0, 200.0, eps, dm, +1), rel=5e-2)

    # 9. Berezhiani 2019 worked example (NIST-like solenoid, 4.6 T, theta0 = 1e-3, Delta_m = 280 neV):
    #    "P + nn′(z = 0)≈ 1 2(1− cos 2θ+ B)≈ 0.02 ... getting P tr nn′≈ 0.01" ; "τbeam/τβ≈ 1 +P tr nn′≈ 1.01".
    #    Our eq.17/18 value at exactly 4.6 T with CODATA mu_n is 0.0114: the result is steeply field
    #    dependent (1 - Omega_B/Delta_m = 0.9%), and 0.02 is reached at 4.611 T (0.2% higher), so the
    #    paper's rounded "≈ 0.02" is matched only to a factor 2. Tolerance: factor 2 (rel 0.5).
    r = beam_solenoid(280 * NEV, theta0=1e-3, B_center=4.6, v=1000.0, trap=(0.0, 0.0), n_trap=1)
    check("Berezhiani worked example P_tr ~ 0.01 (factor-2 check, see comment)", r["P_trap"], 0.01, rel=0.5)

    # 10. Large-field limit (reduces to the simpler law 2 eps^2/delta^2, Abel eq. 4 form): UCN loss
    #     per collision averaged over a broad exponential flight-time distribution.
    eps = eps_from_tau(10.0)
    delta = MU_N * 1e-5                      # 10 uT, omega t_f >> 1
    tf = np.random.default_rng(1).exponential(0.05, 20000)
    res = ucn_loss(eps, [delta], tf)
    check("UCN loss/collision, large field -> 2 eps^2/delta^2", res["P_per_collision"], 2 * eps**2 / delta**2, rel=3e-2)
    # 10b. zero-field limit: loss rate = <t_f^2>/(<t_f> tau^2) = 2 <t_f>/tau^2 for exponential t_f
    res0 = ucn_loss(eps, [0.0], tf)
    check("UCN zero-field loss rate -> <t^2>/(<t> tau^2)", res0["loss_rate_per_s"],
          float(np.mean(tf**2) / np.mean(tf)) / 10.0**2, rel=1e-3)
    # (the code uses the exact sin^2(t/tau); the (t/tau)^2 law differs by -(t/tau)^2/3 ~ 1e-4 here)

    if verbose:
        print("selftest", "PASSED" if ok else "FAILED")
    return ok


# ------------------------------------------------------------------ command line
def _si(text, kind=None):
    q = Q(text)
    return q.si if hasattr(q, "si") else float(q)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("selftest")
    b = sub.add_parser("beam", help="beam-lifetime shift in a solenoid proton trap")
    b.add_argument("--dm", required=True); b.add_argument("--theta0", type=float)
    b.add_argument("--tau"); b.add_argument("--B", default="4.6 T")
    b.add_argument("--v", default="1000 m/s", help="single speed, or comma list")
    b.add_argument("--length", default="0.6 m"); b.add_argument("--radius", default="0.05 m")
    r = sub.add_parser("rabi", help="constant-field conversion probability")
    r.add_argument("--tau", required=True); r.add_argument("--t", required=True)
    r.add_argument("--dm", default="0 neV"); r.add_argument("--B", default="0 T"); r.add_argument("--Bp", default="0 T")
    lz = sub.add_parser("lz", help="Landau-Zener passage")
    lz.add_argument("--tau", required=True); lz.add_argument("--dBdz", required=True); lz.add_argument("--v", required=True)
    u = sub.add_parser("ucn", help="material-bottle loss per collision and rate")
    u.add_argument("--tau", required=True); u.add_argument("--tf", required=True)
    u.add_argument("--dm", default="0 neV"); u.add_argument("--B", default="0 T"); u.add_argument("--Bp", default="0 T")
    u.add_argument("--tau_n", default="878 s")
    ln = sub.add_parser("lznum", help="numerical Landau-Zener sweep vs closed form (diagnostic)")
    ln.add_argument("--gamma", type=float, default=0.1); ln.add_argument("--half_span", type=float, default=400.0)
    ln.add_argument("--n_steps", type=int, default=800_000); ln.add_argument("--avg_from", type=float, default=0.4)
    a = p.parse_args(argv)
    if a.cmd == "selftest":
        return 0 if selftest() else 1
    if a.cmd == "lznum":
        Pn = lz_numeric(a.gamma, a.half_span, a.n_steps, a.avg_from)
        Pc = -math.expm1(-2 * math.pi * a.gamma)
        print(f"numeric {Pn:.6f}  closed form 1-exp(-2 pi Gamma) {Pc:.6f}  diff {Pn - Pc:+.2e}")
        return 0
    if a.cmd == "beam":
        dm = _si(a.dm)
        eps = eps_from_tau(_si(a.tau)) if a.tau else None
        vs = [_si(x) for x in a.v.split(",")]
        res = beam_solenoid(dm, a.theta0, _si(a.B), vs, eps=eps, length=_si(a.length), radius=_si(a.radius))
        print(f"Delta_m = {dm / NEV:.4g} neV, B_res = {res['B_res_T']:.4g} T, tau_nn' = {res['tau_nn_s']:.4g} s")
        print(f"P_trap = {res['P_trap']:.4g}, P_det = {res['P_det']:.4g}, "
              f"tau_beam/tau_beta = {res['tau_beam_over_tau_beta']:.6f} "
              f"(shift {(res['tau_beam_over_tau_beta'] - 1) * 878:.3g} s on 878 s)")
    elif a.cmd == "rabi":
        eps, t, dm, B, Bp = eps_from_tau(_si(a.tau)), _si(a.t), _si(a.dm), _si(a.B), _si(a.Bp)
        P = float(spin_averaged_rabi(t, eps, dm, B, Bp))
        print(f"P(n->n') unpolarised, collinear fields = {P:.6g} (dimensionless)")
    elif a.cmd == "lz":
        eps = eps_from_tau(_si(a.tau))
        print(f"P_LZ(n->n') = {landau_zener_field(eps, _si(a.dBdz), _si(a.v)):.6g} (dimensionless)")
    elif a.cmd == "ucn":
        eps, tf, dm, B, Bp = eps_from_tau(_si(a.tau)), _si(a.tf), _si(a.dm), _si(a.B), _si(a.Bp)
        t = np.random.default_rng(0).exponential(tf, 20000)   # exponential free-flight times
        res = ucn_loss(eps, [detuning(dm, B, +1, Bp), detuning(dm, B, -1, Bp)], t)
        tn = _si(a.tau_n)
        print(f"loss/collision = {res['P_per_collision']:.4g}, rate = {res['loss_rate_per_s']:.4g} 1/s, "
              f"apparent lifetime {apparent_lifetime(tn, res['loss_rate_per_s']):.3f} s (true {tn:.1f} s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
