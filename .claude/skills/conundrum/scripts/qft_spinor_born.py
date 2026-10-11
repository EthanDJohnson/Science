#!/usr/bin/env python3
"""qft_spinor_born: first-order (Born, in-in) production of SPINOR pairs, and scalar-QED pairs, by weak
classical electromagnetic and gravitational backgrounds, in the spectral form of qft_production Part D,
plus the exact Dirac-in-FRW mode reduction used to test it (numpy + mpmath, no scipy).

Why this tool exists
    qft_production.py (imported here as qp) does Born production for scalar pairs (vertex V phi^2) and
    for scalar and photon pairs through the gravity vertex. This module adds the two vertices it lacks:
    the QED vertex -j.A for Dirac and scalar-QED pairs (vacuum polarisation), and the gravity vertex
    -(1/2) h T for Dirac (and Weyl) pairs. The traps are the same: in-in mean numbers versus in-out
    amplitudes and vacuum persistence; plane waves (zero at first order) versus sources and packets cut
    off in time; real production versus transient vacuum polarisation (nothing here is a number at
    intermediate times); vacuum-decay rate versus pair number (equal ONLY at this order); particles versus
    pairs. Every public function has a "Quantity:" and a "Valid when:" line and refuses inputs outside
    that range with ValueError.

Units (read this first)
    Natural units hbar = c = 1, Heaviside-Lorentz electromagnetism (e^2 = 4 pi alpha), exactly as qp.
    Pick ONE energy unit (eV, or units of the mass m) and give energies, masses, momenta and inverse
    times in it. The charge is absorbed into the field: inputs are eE (energy^2) and eA (energy), so alpha
    appears only in im_vacuum_polarization. Pairs per volume are energy^3, per area energy^2, total
    dimensionless. SI: use qp.eE_from_field_SI, qp.time_to_inverse_eV, qp.density_to_SI; the command line
    accepts units through unit_tools.Q ("1e16 V/m", "1e-21 s", "0.511 MeV").

Conventions (as qp Part D)
    Metric (+,-,-,-), s = K^2. V~(K) = int d^4x e^{i K.x} V(x), K.x = K0 t - K.x; positive K0 creates.
    A_mu is LOWER-index (A_0 = scalar potential phi, A_i = -A^i), E = -grad phi - dA/dt, B = curl A.
    Fourier: eE~ = -i (K eA~_0 + K0 eA~_vec,low), eB~ = -i K x eA~_vec,low (fields_from_potential).

PART 1. Vector-current spectral densities (QED vertex L = -j^mu A_mu)
------------------------------------------------------------------------
    j = e psibar gamma psi (Dirac, mass m) or j = i e (phi* d phi - phi d phi*) (complex scalar, scalar QED).
    First-order amplitude to make the pair state n: <n|S|0> = -i eA~_mu(p_n) <n|j^mu(0)|0>/e. Summing |.|^2:
        N_pairs = int d^4K/(2pi)^4 theta(K0) eA~*_mu(K) eA~_nu(K) rho^{mu nu}(K)/e^2,
        rho^{mu nu}(K) = sum_n (2pi)^4 delta^4(K - p_n) <0|j^nu|n><n|j^mu|0> = (K^mu K^nu - s eta^{mu nu}) e^2 rhoV(s),
    (current conservation fixes the tensor). The contraction is gauge invariant and equals the fields:
        X_V = |K.eA~|^2 - s eA~*.eA~ = -(1/2) eF~*_{mu nu} eF~^{mu nu} = |eE~|^2 - |eB~|^2   (>= 0 for s > 0),
        N_pairs = int d^4K/(2pi)^4 theta(K0) (|eE~(K)|^2 - |eB~(K)|^2) rhoV(K^2).
    Charge-stripped two-body densities (rhoV = rho/e^2, dimensionless, spin-summed, e- e+ distinguishable):
        Dirac:   rhoV = beta (3 - beta^2)/(12 pi) = beta (1 + 2 m^2/s)/(6 pi),    beta = sqrt(1 - 4m^2/s)
        scalar:  rhoV = beta^3/(24 pi)                                           (zero below s = 4 m^2)
    Vacuum polarisation: Im Pi(s) = (e^2/2) rhoV = (alpha/3) beta (1 + 2m^2/s) (Dirac), (alpha/12) beta^3 (scalar)
    (Rosner hep-ph/0108195 eqs. 45-46; Peskin & Schroeder eq. 7.92), and sigma(e+e- -> pairs) = e^2 (e^2 rhoV)/(2s)
    for massless electrons (PDG eq. 51.2). Massless Dirac: N = (e^2/6pi) int_{K0>0} = (e^2/12pi) int over BOTH light
    cones (Redi & Tesi 2026 eq. 7, written as 2 Im Gamma). At this order N = 2 Im Gamma (vacuum persistence
    |<0|0>|^2 = exp(-2 Im Gamma)); at higher orders they differ (qp Part B: pair number vs vacuum decay).
    Pairs vs particles: one electron + one positron per pair (distinguishable, no 1/2); particles = 2 x pairs.
    * Homogeneous E(t) (B = 0): N/V = int_{2m}^inf dOmega/(2pi) |eE~(Omega)|^2 rhoV(Omega^2) (vector E: sum of
      components). Per mode it is the first-order term of qp's exact solvers (derived by expanding them):
        spinor, per spin:  n_k = eps_perp^2 |eE~(2w)|^2/(4 w^4),  eps_perp^2 = m^2 + k_perp^2, w = sqrt(m^2 + k^2);
        scalar:            n_k = k_par^2   |eE~(2w)|^2/(4 w^4);
      2 int d^3k/(2pi)^3 n_k (spinor) or int d^3k/(2pi)^3 n_k (scalar) reproduces the spectral form.
    * Planar eA_mu(t, z): per unit transverse area; general eA_mu(t, x): total (as qp Part D).
    * Born is the LEADING order only when the one-photon Fourier content of the field at Omega >= 2m is not
      exponentially smaller than multi-photon terms. A smooth pulse of duration T with m T >~ 2 fails even at
      weak field: a Gaussian E(t) with m T = 2 (eE0 T^2 = 0.08) gives exact/Born = 3.1, with m T = 3 about 1e4
      (measured with qp's exact solver; see the 'convergence' command). born_qed_homogeneous therefore computes
      a second-order indicator R2 = max 2 |FT[(e dA)^2 - c^2]| / |eE~| over the Omega that carry the Born yield
      (dA = A - (A_in + A_out)/2, c = |A_out - A_in|/2; R2 = 2 eE0 tau^2 for a Sauter pulse) and an error estimate
      (1 + 2 m T) R2^2 (T = rms duration of |E|), refused above 0.5. Calibration (the 'convergence' command): it
      bounds the measured |exact/Born - 1| for Sauter pulses with m tau = 0.5..3 (the coefficient of (eE0 tau^2)^2
      grows with m tau: scalar 3.4, 7.5, 14, 21 at m tau = 0.5, 1, 2, 3; at m tau = 3, eE0 = 0.01: 0.21 estimated,
      0.17 measured) and for Gaussian pulses with m T = 0.5..3, where it is one to two orders of magnitude too
      cautious (m T = 1, eE0 = 0.05 m^2: 0.91 estimated, 0.025 measured, refused: verify with the exact solver and
      pass check=False). Outside that calibration (smooth pulses with m T > 3) treat it as a rough guide.

PART 2. Stress-tensor spectral densities of Dirac (and Weyl) pairs (gravity vertex L = -(1/2) h_{mu nu} T^{mu nu})
------------------------------------------------------------------------------------------------------------
    T^{mu nu} = (i/4) psibar (gamma^mu d^nu + gamma^nu d^mu - (left derivatives)) psi (on shell; the - eta L term
    vanishes on pair states):  <p1 p2|T^{mu nu}|0> = (1/4) ubar(p1) [gamma^mu q^nu + gamma^nu q^mu] v(p2), q = p1 - p2.
    rho^{mu nu rho sigma} = rho2 Pi2 + rho0 pi pi exactly as in qp.stress_spectral_densities; from the traces:
        Dirac:  rho2 = s^2 beta^3 (5 - 2 beta^2)/(240 pi) = s^2 beta^3 (1 + 8m^2/(3s))/(80 pi),
                rho0 = m^2 s beta^3/(36 pi)       (trace T^mu_mu = m psibar psi on shell: zero for m = 0),
        Weyl (m = 0): half of massless Dirac, rho2 = s^2/(160 pi), rho0 = 0.
    Ratios (massless): Dirac/real scalar = 6, Weyl/real scalar = 3 (Redi & Tesi c_1/2 = 4, c_0 = 4/3);
    photon/Dirac = 2 (Han, Lykken & Zhang eqs. 46 and 52). Mass dependence of rho2: beta^3 (1 + 8m^2/(3s)) (HLZ eq. 52).
    Born yield (pairs, e- e+ distinguishable, spin-summed): N = (1/4) int d^4K/(2pi)^4 theta(K0) [rho2 X2 + rho0 X0]
    with qp's X2 = h* Pi2 h, X0 = |pi^{mu nu} h_{mu nu}|^2. Entry points born_dirac_metric_homogeneous / _planar /
    _general mirror qp.born_metric_*. Plane gravitational waves still give zero (null support; rho2 ~ s^2).

PART 3. Dirac field in spatially flat FRW, ds^2 = a(eta)^2 (d eta^2 - dx^2) (exact)
-------------------------------------------------------------------------------
    psi = a^{-3/2} chi; chi obeys the FLAT Dirac equation with time-dependent mass m a(eta), and per comoving k and
    helicity the two-level problem i c' = (m a(eta) sigma_z + k sigma_x) c. So qp.bogoliubov_fermion_efield with
    p_of_t = m a(eta), eps_perp = k solves it (frw_dirac_production). n_k = in-in mean number of electrons in comoving
    mode k with that helicity (= positrons in -k = pairs in the mode); both helicities equal; per comoving volume.
    * a(eta) = A + B tanh(rho eta) (tanh in a, NOT a^2 as for the scalar Bernard-Duncan model) is exactly the Sauter
      problem (k_par -> m A, eE0 tau -> m B, tau -> 1/rho, eps_perp -> k): Gavrilov-Gitman eq. 42 closed form,
      frw_dirac_tanh_n; checked against Fuentes, Mann, Martin-Martinez & Moradi 2010 eq. 16 (Duncan's model).
    * m = 0: nothing is produced for any a(eta) (conformal invariance).
    * Born: a = 1 + eps f(eta) is h = 2 eps f eta_{mu nu} at first order (trace channel only):
        N/V = eps^2 int_{2m} dOmega/(2pi) |f~(Omega)|^2 m^2 Omega^2 beta^3/(4 pi)  (= born_dirac_metric_homogeneous).

Assumptions and validity range
    Free fields in a prescribed classical background (no back-reaction), first order in the background; the
    background is off at both ends of the time window. Born is O(field^2) exact: compare two amplitudes (the
    self-test shows the deviation scaling as E0^2 for QED, by charge conjugation, and as eps for FRW). Per-mode
    first-order occupations above 0.1, momentum kicks e|dA| > m/2 and error estimates (1 + 2mT) R2^2 > 0.5 are refused.

Python usage
    import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
    import numpy as np, qft_spinor_born as sb
    sb.vector_spectral_density([9.0], 1.0, "dirac")                # rhoV(s = 9 m^2), charge-stripped
    sb.im_vacuum_polarization([9.0], 1.0)                          # (alpha/3) beta (1 + 2m^2/s)
    r = sb.born_qed_homogeneous(lambda t: 0.05 / np.cosh(t) ** 2, -30, 30, m=1.0, omega_max=40.0)
    r["pairs_per_volume"], r["error_estimate"]                     # e+e- PAIRS per volume (units of m^3), est. rel. error
    sb.sauter_exact_pairs_per_volume(1.0, 0.05, 1.0, "dirac")      # exact (Gavrilov-Gitman) for comparison
    sb.dirac_stress_spectral_densities([9.0], m=1.0)               # (rho2, rho0) of Dirac pairs
    sb.frw_dirac_tanh_n([0.5], m=1.0, A=1.3, B=0.3, rho=0.8)       # exact n_k per helicity, comoving mode

Command line (from the project root)
    python3 .claude/skills/conundrum/scripts/qft_spinor_born.py selftest
    python3 .claude/skills/conundrum/scripts/qft_spinor_born.py spectral --sqrts "1.5 MeV" --m "0.511 MeV"
    python3 .claude/skills/conundrum/scripts/qft_spinor_born.py sauter --E "1e16 V/m" --tau "1e-21 s"
    python3 .claude/skills/conundrum/scripts/qft_spinor_born.py frw --m 1 --A 1.3 --B 0.3 --rho 0.8 --k 0.5
    python3 .claude/skills/conundrum/scripts/qft_spinor_born.py convergence      (slow: scaling and grid studies)
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

import qft_production as qp  # noqa: E402  (solvers, Fourier and quadrature helpers, SI conversions)

PI = math.pi
ALPHA = 7.2973525643e-3        # fine-structure constant, CODATA 2022 (NIST: "Numerical value 7.297 352 5643 x 10 -3")
_ETA = qp._ETA
_FIELDS_QED = ("dirac", "scalar")
_FIELDS_GRAV = ("dirac", "weyl")

# Dirac representation: gamma^0 = diag(1, 1, -1, -1), gamma^i = [[0, sigma_i], [-sigma_i, 0]]
_SIG = np.array([[[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]], dtype=complex)
_Z2 = np.zeros((2, 2), dtype=complex)
_GAM = np.array([np.diag([1, 1, -1, -1]).astype(complex)]
                + [np.block([[_Z2, _SIG[i]], [-_SIG[i], _Z2]]) for i in range(3)])


# ---------------------------------------------------------------- input checks
def _field(field: str, allowed) -> str:
    if field not in allowed:
        raise ValueError(f"field must be one of {allowed}")
    return field


def _mass(m) -> float:
    m = float(m)
    if not (math.isfinite(m) and m >= 0):
        raise ValueError("m must be finite and >= 0")
    return m


def _beta(s, m):
    s = qp._arr(s, "s")
    th = 4 * m * m
    with np.errstate(divide="ignore", invalid="ignore"):
        return s, np.where(s > th, np.sqrt(np.clip(1 - th / np.where(s > 0, s, 1.0), 0, None)), 0.0)


# ---------------------------------------------------------------- PART 1: vector current
def vector_spectral_density(s, m: float, field: str = "dirac"):
    """Charge-stripped two-body spectral density rhoV(s) of the electromagnetic current (spin-summed).

    rho^{mu nu}(K) = sum_pairs (2pi)^4 delta^4(K - p1 - p2) <0|j^nu|n><n|j^mu|0> = e^2 (K^mu K^nu - s eta^{mu nu}) rhoV(s):
        Dirac (j = e psibar gamma psi):           rhoV = beta (3 - beta^2)/(12 pi) = beta (1 + 2m^2/s)/(6 pi)
        scalar QED (j = i e (phi* d phi - c.c.)): rhoV = beta^3/(24 pi),         beta = sqrt(1 - 4m^2/s).
    Quantity: rhoV(s), dimensionless, per electron-positron PAIR state, summed over both spins (no identical-particle
        1/2: e- and e+ are distinguishable); the Born yield is N_pairs = int d^4K/(2pi)^4 theta(K0)
        (|eE~|^2 - |eB~|^2) rhoV(K^2) (particles = 2 x pairs). Im Pi = (e^2/2) rhoV (im_vacuum_polarization).
    Valid when: s real; m >= 0; field 'dirac' or 'scalar'; returns 0 for s <= 4m^2 (massless Dirac: 1/(6 pi) for s > 0)."""
    m = _mass(m)
    _field(field, _FIELDS_QED)
    s, b = _beta(s, m)
    if field == "dirac":
        return b * (3 - b * b) / (12 * PI)
    return b ** 3 / (24 * PI)


def im_vacuum_polarization(s, m: float, field: str = "dirac", alpha: float = ALPHA):
    """One-loop Im Pi(s) of the photon self-energy from a Dirac fermion or a complex scalar of unit charge.

    Im Pi = (e^2/2) rhoV = 2 pi alpha rhoV: (alpha/3) beta (1 + 2m^2/s) (Dirac), (alpha/12) beta^3 (scalar),
    the sign convention of Rosner (hep-ph/0108195) eqs. 44-46, Im Pi = s sigma(e+e- -> pairs)/(4 pi alpha) > 0.
    Quantity: Im Pi(s) on the upper lip of the cut, dimensionless: the absorptive part (real pair creation per unit
        background spectral weight, Im Pi = (e^2/2) rhoV), not the real part (transient vacuum polarisation, which
        creates nothing); not a pair count by itself.
    Valid when: s real; m >= 0; alpha > 0 (default CODATA 2022 value); one loop, zero below s = 4m^2."""
    if not (alpha > 0 and math.isfinite(alpha)):
        raise ValueError("alpha must be > 0")
    return 2 * PI * alpha * vector_spectral_density(s, m, field)


def em_weight(K0, Kx, Ky, Kz, eA):
    """The gauge-invariant Born weight X_V = |K.eA~|^2 - s eA~*.eA~ for a lower-index potential eA~_mu(K).

    eA has shape (..., 4) (components eA_0, eA_1, eA_2, eA_3, lower index); K0..Kz are the UPPER components of K.
    Equal to |eE~|^2 - |eB~|^2 = -(1/2) eF~* eF~ (see fields_from_potential); unchanged by eA -> eA + K lam.
    Quantity: X_V(K) = |eE~|^2 - |eB~|^2, real, in (units of eA~)^2 x energy^2 (>= 0 for timelike K); the Born yield
        is N_pairs = int d^4K/(2pi)^4 theta(K0) X_V rhoV(K^2) (vector_spectral_density).
    Valid when: arrays broadcast; K real; eA complex (any gauge)."""
    A = np.asarray(eA)
    if A.shape[-1] != 4:
        raise ValueError("eA must have a last axis of length 4 (lower-index eA_mu)")
    K0, Kx, Ky, Kz = (np.asarray(x, dtype=float) for x in (K0, Kx, Ky, Kz))
    s = K0 * K0 - Kx * Kx - Ky * Ky - Kz * Kz
    KA = K0 * A[..., 0] + Kx * A[..., 1] + Ky * A[..., 2] + Kz * A[..., 3]
    AA = np.abs(A[..., 0]) ** 2 - np.abs(A[..., 1]) ** 2 - np.abs(A[..., 2]) ** 2 - np.abs(A[..., 3]) ** 2
    return np.abs(KA) ** 2 - s * AA


def fields_from_potential(K0, Kx, Ky, Kz, eA):
    """Fourier-space fields from a lower-index potential: eE~ = -i (K eA_0 + K0 eA_low), eB~ = -i K x eA_low.

    (E = -grad phi - dA/dt, B = curl A, with phi = A_0 and A^i = -A_i; d/dt -> -i K0 and grad -> +i K.)
    Quantity: (eE~, eB~), complex arrays of shape (..., 3) (same units as K x eA~).
    Valid when: arrays broadcast; K real."""
    A = np.asarray(eA)
    if A.shape[-1] != 4:
        raise ValueError("eA must have a last axis of length 4 (lower-index eA_mu)")
    K = np.stack(np.broadcast_arrays(*(np.asarray(x, dtype=float) for x in (Kx, Ky, Kz))), axis=-1)
    K0 = np.asarray(K0, dtype=float)[..., None]
    a = A[..., 1:]
    E = -1j * (K * A[..., :1] + K0 * a)
    B = -1j * np.cross(K, a)
    return E, B


def born_mode_efield(k_par, k_perp, m: float, eEtilde, field: str = "dirac"):
    """First-order (Born, in-in) occupation of one mode in a homogeneous E(t) along z (charge absorbed: eE).

    eEtilde(Omega) returns eE~(Omega) = int eE(t) e^{i Omega t} dt (energy). With w = sqrt(m^2 + k^2):
        Dirac, per spin state:  n_k = eps_perp^2 |eE~(2w)|^2 / (4 w^4),  eps_perp^2 = m^2 + k_perp^2;
        scalar QED:             n_k = k_par^2 |eE~(2w)|^2 / (4 w^4).
    (First-order term of qp.bogoliubov_fermion_efield / qp.bogoliubov_boson: beta_k = int (theta'/2) e^{2iwt} dt with
    theta = arctan(eps_perp/p), resp. beta_k = (1/2w) int dw^2 e^{2iwt} dt with dw^2 = 2 k_par e dA.) If the pulse has
    a net area e int E dt != 0 the in and out momenta of the mode differ by that kick; at first order the label is
    ambiguous by O(eE), which is within Born's accuracy.
    Quantity: per-mode in-in mean number of electrons in mode k (= positrons in -k = pairs in the mode), dimensionless;
        per spin state for Dirac (multiply by 2 for both spins), the complex scalar for 'scalar'.
    Valid when: weak field (refused if any n_k > 0.1: first order is then not an estimate); m^2 + k_perp^2 > 0;
        E(t) homogeneous, linearly polarised, off at both ends; scalar QED also needs e|dA| << |k_par| (its first-order
        term is proportional to k_par, so near k_par = 0 the second-order (e dA)^2 term dominates)."""
    m = _mass(m)
    _field(field, _FIELDS_QED)
    kz, kp = np.broadcast_arrays(qp._arr(k_par, "k_par"), qp._arr(k_perp, "k_perp"))
    if np.any(m * m + kp * kp <= 0):
        raise ValueError("need m^2 + k_perp^2 > 0")
    w = np.sqrt(m * m + kp * kp + kz * kz)
    E2 = np.abs(np.asarray(eEtilde(2 * w))) ** 2
    num = (m * m + kp * kp) if field == "dirac" else kz * kz
    n = num * E2 / (4 * w ** 4)
    if np.any(n > 0.1):
        raise ValueError(f"first-order occupation up to {float(n.max()):.3g} > 0.1: not perturbative; use the exact solver "
                         "(qp.bogoliubov_fermion_efield / qp.bogoliubov_boson)")
    return n


def _uniform_A(eE_of_t, t0, t1, n):
    """eE and the cumulative e A(t) = -int eE dt on a uniform grid (trapezoid; for diagnostics only)."""
    t = np.linspace(t0, t1, n)
    E = np.asarray(eE_of_t(t), dtype=float)
    E2 = E.reshape(n, -1)
    dt = t[1] - t[0]
    A = np.vstack([np.zeros((1, E2.shape[1])), np.cumsum(0.5 * dt * (E2[1:] + E2[:-1]), axis=0)])
    return t, E2, A


def born_qed_homogeneous(eE_of_t, t0: float, t1: float, m: float, omega_max: float, field: str = "dirac",
                         n_omega: int = 200, check: bool = True) -> dict:
    """Born (first-order, in-in) electron-positron pairs per unit volume from a homogeneous field eE(t).

    eE_of_t(t_array) returns eE(t) (energy^2) with shape (len(t),) (fixed direction) or (len(t), 3); B = 0.
        N/V = int_{2m}^{omega_max} dOmega/(2pi) |eE~(Omega)|^2 rhoV(Omega^2),  eE~(Omega) = int eE(t) e^{i Omega t} dt.
    Perturbativity diagnostics on the Omega that carry 99.9% of the yield (refused when check=True):
      'occupation_max' = max |eE~(Omega)|^2/Omega^2 >= any per-mode Born occupation (refused > 0.1);
      'kick' = e max|dA|/m, dA = A - (A_in + A_out)/2 (refused > 0.5);
      'R2' = max 2 |FT[(e dA)^2 - c^2](Omega)| / |eE~(Omega)|: the second-order (two-photon) amplitude relative to
        the first (R2 = 2 eE0 tau^2 for a Sauter pulse);
      'error_estimate' = (1 + 2 m T) R2^2, T = rms duration of |eE(t)| (refused > 0.5): bounds the measured relative
        error of Born for Sauter pulses (m tau = 0.5..3) and Gaussian pulses (m T = 0.5..3, where it is 10-100x too
        cautious). A Gaussian pulse with m T = 2 (exact/Born = 3.1 at eE0 T^2 = 0.08) has error_estimate ~400 and is
        refused; pass check=False to get the first-order number after verifying with the exact solvers.
    Quantity: dict with 'pairs_per_volume' (in-in mean number of e+e- PAIRS per unit volume, spin-summed, energy^3;
        = electrons = positrons per volume), 'particles_per_volume' (= 2 x pairs), the spectrum 'dN_dOmega' on 'omega'
        (pairs per volume per unit pair energy), 'occupation_max', 'kick', 'R2', 'T_rms', 'error_estimate'.
        At this order it also equals
        2 Im Gamma per volume (vacuum persistence exponent); beyond it the two differ.
    Valid when: m > 0; first order (diagnostics above); eE(t) -> 0 at both ends of [t0, t1] (|eE| < 1e-6 max there);
        |eE~| negligible above omega_max > 2m; field 'dirac' or 'scalar'."""
    m = _mass(m)
    _field(field, _FIELDS_QED)
    t0, t1 = float(t0), float(t1)
    if not m > 0:
        raise ValueError("m must be > 0 (massless pairs in a homogeneous field are non-perturbative at small k)")
    if not (math.isfinite(t0) and math.isfinite(t1)) or t1 <= t0 or not omega_max > 2 * m or n_omega < 16:
        raise ValueError("need finite t0 < t1, omega_max > 2m and n_omega >= 16")
    ends = np.abs(np.asarray(eE_of_t(np.array([t0, t1])), dtype=float)).reshape(2, -1).max()
    peak = np.abs(np.asarray(eE_of_t(np.linspace(t0, t1, 2001)), dtype=float)).max()
    if not peak > 0:
        raise ValueError("eE(t) vanishes identically")
    if ends > 1e-6 * peak:
        raise ValueError(f"eE at the window ends is {ends / peak:.2g} of its peak: extend [t0, t1] until the field is off")
    u, wu = qp._gauss_legendre(0.0, math.sqrt(omega_max - 2 * m), n_omega)     # Omega = 2m + u^2: smooth at threshold
    om, w = 2 * m + u * u, 2 * u * wu
    Et = qp._ft_time(eE_of_t, t0, t1, om)
    E2 = np.abs(Et) ** 2 if Et.ndim == 1 else np.sum(np.abs(Et) ** 2, axis=-1)
    dN = E2 * vector_spectral_density(om * om, m, field) / (2 * PI)
    N = float(np.sum(w * dN))
    # diagnostics on the Omega carrying the yield
    cdf = np.cumsum(w * dN) / max(N, 1e-300)
    sel = (cdf > 5e-4) & (cdf < 1 - 5e-4) | (dN >= 1e-3 * dN.max())
    occ = float(np.max(E2[sel] / om[sel] ** 2)) if np.any(sel) else 0.0
    npts = int(min(200001, max(4001, 16 * omega_max * (t1 - t0) / PI)))
    t, _, A = _uniform_A(eE_of_t, t0, t1, npts)
    dA = A - 0.5 * (A[0] + A[-1])
    c2 = float(np.sum((0.5 * (A[-1] - A[0])) ** 2))
    kick = float(np.sqrt(np.sum(dA ** 2, axis=1)).max()) / m
    Emag = np.sqrt(np.sum(np.asarray(eE_of_t(t), dtype=float).reshape(npts, -1) ** 2, axis=1))
    tm = float(np.sum(t * Emag) / np.sum(Emag))
    T_rms = math.sqrt(float(np.sum((t - tm) ** 2 * Emag) / np.sum(Emag)))
    G = np.sum(dA ** 2, axis=1) - c2
    osel = om[sel][:: max(1, int(np.sum(sel)) // 40)]
    wt = np.full(npts, t[1] - t[0])
    wt[0] = wt[-1] = 0.5 * (t[1] - t[0])
    Gt = np.abs(np.exp(1j * np.outer(osel, t)) @ (wt * G))
    Ef = qp._ft_time(eE_of_t, t0, t1, osel)
    Ef2 = np.abs(Ef) if Ef.ndim == 1 else np.sqrt(np.sum(np.abs(Ef) ** 2, axis=-1))
    R2 = float(np.max(2 * Gt / np.maximum(Ef2, 1e-300))) if osel.size else 0.0
    err = (1 + 2 * m * T_rms) * R2 * R2
    if check:
        if occ > 0.1:
            raise ValueError(f"per-mode first-order occupation up to {occ:.3g} > 0.1 (resonant/Rabi regime): not perturbative")
        if kick > 0.5:
            raise ValueError(f"momentum kick e|dA|/m = {kick:.3g} > 0.5: not perturbative (use the exact mode solvers)")
        if err > 0.5:
            raise ValueError(f"Born error estimate (1 + 2 m T) R2^2 = {err:.3g} > 0.5 (second-order indicator R2 = {R2:.3g}, "
                             f"m T = {m * T_rms:.3g}): multi-photon terms may rival the one-photon Born term (e.g. a smooth "
                             "pulse with m T >~ 2). Verify with qp.bogoliubov_fermion_efield / qp.bogoliubov_boson, or pass "
                             "check=False to get the first-order number anyway")
    return {"pairs_per_volume": N, "particles_per_volume": 2 * N, "omega": om, "dN_dOmega": dN,
            "occupation_max": occ, "kick": kick, "R2": R2, "T_rms": T_rms, "error_estimate": err}


def sauter_born_pairs_per_volume(m: float, eE0: float, tau: float, field: str = "dirac", n: int = 200) -> float:
    """Born pairs per volume for the Sauter pulse eE(t) = eE0 sech^2(t/tau), with its exact Fourier transform.

    eE~(Omega) = eE0 pi Omega tau^2 / sinh(pi Omega tau/2), so N/V = int_{2m} dOmega/(2pi) |eE~|^2 rhoV(Omega^2).
    Quantity: in-in mean number of e+e- PAIRS per unit volume at first order (energy^3, spin-summed for Dirac;
        complex scalar for 'scalar').
    Valid when: m > 0, eE0 > 0, tau > 0 and the pulse is perturbative: error estimate (1 + 1.81 m tau)(2 eE0 tau^2)^2
        <= 0.5 (born_qed_homogeneous's, with T = 0.907 tau) and eE0 tau <= m/2 (refused otherwise; compare
        sauter_exact_pairs_per_volume)."""
    m = _mass(m)
    _field(field, _FIELDS_QED)
    eE0, tau = float(qp._positive(eE0, "eE0")), float(qp._positive(tau, "tau"))
    if not m > 0:
        raise ValueError("m must be > 0")
    err = (1 + 2 * m * tau * PI / math.sqrt(12.0)) * (2 * eE0 * tau * tau) ** 2      # T_rms(sech^2) = pi tau/sqrt(12)
    if err > 0.5 or eE0 * tau > 0.5 * m:
        raise ValueError(f"Sauter pulse not perturbative (error estimate {err:.3g}, R2 = 2 eE0 tau^2 = {2 * eE0 * tau * tau:.3g}, "
                         f"kick eE0 tau/m = {eE0 * tau / m:.3g}); use sauter_exact_pairs_per_volume")
    u, wu = qp._gauss_legendre(0.0, math.sqrt(60.0 / tau), n)
    om, w = 2 * m + u * u, 2 * u * wu
    with np.errstate(over="ignore"):
        Et = eE0 * PI * om * tau * tau / np.sinh(np.minimum(PI * om * tau / 2, 700.0))
    return float(np.sum(w * Et ** 2 * vector_spectral_density(om * om, m, field)) / (2 * PI))


def sauter_exact_pairs_per_volume(m: float, eE0: float, tau: float, field: str = "dirac", n_k: int = 160,
                                  n_c: int = 48) -> float:
    """Exact pairs per volume for the Sauter pulse: g int d^3k/(2pi)^3 n_k with the Gavrilov-Gitman occupations.

    Uses qp.sauter_n_spinor / qp.sauter_n_scalar (GG 1996 eqs. 42-43) on a spherical Gauss grid in the canonical
    momentum, |k| <= eE0 tau + 30/(2 pi tau) + 10 m + 10 sqrt(eE0) (resolves the weak-field, short-pulse case where
    qp.sauter_pairs_per_volume's default 96-node grid is off by several per cent).
    Quantity: in-in mean number of e+e- PAIRS per unit volume after the pulse (energy^3; g = 2 spins for Dirac, 1 for
        the complex scalar), all orders in the field (not a rate).
    Valid when: m > 0, eE0 > 0, tau > 0 and n_k is not too elongated along k_par for the spherical grid (weak or
        moderate fields, eE0 tau <~ 10 m); check by raising n_k, n_c."""
    m = _mass(m)
    _field(field, _FIELDS_QED)
    eE0, tau = float(qp._positive(eE0, "eE0")), float(qp._positive(tau, "tau"))
    if not m > 0 or n_k < 16 or n_c < 8:
        raise ValueError("need m > 0, n_k >= 16, n_c >= 8")
    if eE0 * tau > 10 * m:
        raise ValueError("eE0 tau > 10 m: n_k is too elongated for the spherical grid; use qp.sauter_pairs_per_volume")
    kmax = eE0 * tau + 30.0 / (2 * PI * tau) + 10 * m + 10 * math.sqrt(eE0)
    k, wk = qp._gauss_legendre(0.0, kmax, n_k)
    c, wc = np.polynomial.legendre.leggauss(n_c)
    K, C = np.meshgrid(k, c, indexing="ij")
    kz, kp = K * C, K * np.sqrt(1 - C * C)
    nn = qp.sauter_n_spinor(kz, kp, m, eE0, tau) if field == "dirac" else qp.sauter_n_scalar(kz, kp, m, eE0, tau)
    g = 2.0 if field == "dirac" else 1.0
    return g * float(np.einsum("i,j,ij->", wk * k * k, wc, nn)) / (4 * PI * PI)      # d^3k/(2pi)^3 = 2 pi k^2 dk dc/(2pi)^3


def born_qed_planar(eAtilde, m: float, s_max: float, y_max: float, field: str = "dirac", n_s: int = 320,
                    n_y: int = 320) -> dict:
    """Born pairs per unit transverse area from a planar potential eA_mu(t, z) (uniform in x, y), QED vertex.

    eAtilde(K0, Kz) = int dt dz e^{i(K0 t - Kz z)} eA_mu(t, z), LOWER index, shape (..., 4). With K0 = sqrt(s) cosh y,
    Kz = sqrt(s) sinh y:  N/A = int ds dy/(2 (2pi)^2) X_V rhoV(s), X_V = em_weight = |eE~|^2 - |eB~|^2.
    A source-free plane wave (all support on s = 0) gives zero; a wave cut off in time or a source does not
    (qp.wave_equation_residual_planar flags profiles that are not vacuum solutions).
    Quantity: dict with 'pairs_per_area' (in-in mean number of e+e- PAIRS per unit transverse area, spin-summed,
        energy^2) and 'particles_per_area' (= 2 x pairs).
    Valid when: first order in eA (compare two amplitudes); spectrum negligible for s > s_max or |y| > y_max;
        m >= 0; Gauss grids resolve eA~ (check by doubling n_s, n_y and y_max)."""
    m = _mass(m)
    _field(field, _FIELDS_QED)
    if not s_max > 4 * m * m or not y_max > 0 or min(n_s, n_y) < 8:
        raise ValueError("need s_max > 4m^2, y_max > 0 and n_s, n_y >= 8")
    s, ws = qp._s_nodes(4 * m * m, s_max, n_s)
    y, wy = qp._gauss_legendre(-y_max, y_max, n_y)
    S, Y = np.meshgrid(s, y, indexing="ij")
    rs = np.sqrt(S)
    K0, Kz = rs * np.cosh(Y), rs * np.sinh(Y)
    z = np.zeros_like(K0)
    X = em_weight(K0, z, z, Kz, np.asarray(eAtilde(K0, Kz)))
    N = float(np.einsum("i,j,ij->", ws, wy, X * vector_spectral_density(S, m, field)) / (2 * (2 * PI) ** 2))
    return {"pairs_per_area": N, "particles_per_area": 2 * N}


def born_qed_general(eAtilde4, m: float, s_max: float, kappa_max: float, field: str = "dirac", n_s: int = 40,
                     n_k: int = 40, n_c: int = 16, n_p: int = 16) -> dict:
    """Born pairs from a potential eA_mu(t, x) of ANY space-time profile, QED vertex, as a 4D spectral integral.

    eAtilde4(K0, Kx, Ky, Kz) = int d^4x e^{i(K0 t - K.x)} eA_mu(x), lower index, shape (..., 4):
        N = int d^4K/(2pi)^4 theta(K0) X_V rhoV(K^2) = int ds rhoV(s) int d^3K/((2pi)^4 2 K0) (|eE~|^2 - |eB~|^2).
    For massless Dirac this is Redi & Tesi's 2 Im Gamma (their eq. 7, both light cones = 2 x the K0 > 0 cone).
    Quantity: dict with 'pairs' (total in-in mean number of e+e- PAIRS, dimensionless, spin-summed) and 'particles'.
    Valid when: first order in eA; spectrum negligible beyond s_max, kappa_max; m >= 0; the Gauss grids resolve
        eA~ (check by doubling n_s, n_k, n_c, n_p)."""
    m = _mass(m)
    _field(field, _FIELDS_QED)
    if not s_max > 4 * m * m or not kappa_max > 0:
        raise ValueError("need s_max > 4m^2 and kappa_max > 0")
    S, K0, Kx, Ky, Kz, W = qp._four_nodes(4 * m * m, s_max, kappa_max, n_s, n_k, n_c, n_p)
    X = em_weight(K0, Kx, Ky, Kz, np.asarray(eAtilde4(K0, Kx, Ky, Kz)))
    N = float(np.sum(W * X * vector_spectral_density(S, m, field)))
    return {"pairs": N, "particles": 2 * N}


# ---------------------------------------------------------------- PART 2: gravity vertex, Dirac pairs
def dirac_stress_spectral_densities(s, m: float = 0.0, field: str = "dirac"):
    """Spin-2 and spin-0 spectral densities of T^{mu nu} for Dirac (or Weyl) pairs, normalised as qp's.

    rho^{mu nu rho sigma} = rho2 Pi2 + rho0 pi^{mu nu} pi^{rho sigma} (qp.stress_spectral_densities conventions):
        Dirac: rho2 = s^2 beta^3 (1 + 8m^2/(3s))/(80 pi),  rho0 = m^2 s beta^3/(36 pi)  (trace T = m psibar psi);
        Weyl:  m = 0 only, half of massless Dirac: rho2 = s^2/(160 pi), rho0 = 0.
    Quantity: (rho2, rho0), energy^4, per fermion-antifermion PAIR state, spin-summed (no identical-particle 1/2);
        Born yield for g = eta + h: N_pairs = (1/4) int d^4K/(2pi)^4 theta(K0) [rho2 X2 + rho0 X0].
    Valid when: s real; m >= 0 (Weyl: m = 0); zero below s = 4 m^2."""
    m = _mass(m)
    _field(field, _FIELDS_GRAV)
    if field == "weyl" and m != 0:
        raise ValueError("a Weyl fermion is massless (m must be 0)")
    s, b = _beta(s, m)
    r2 = s * s * b ** 3 * (5 - 2 * b * b) / (240 * PI)
    r0 = m * m * s * b ** 3 / (36 * PI)
    if field == "weyl":
        return 0.5 * r2, 0.0 * r0
    return r2, r0


def born_dirac_metric_homogeneous(h_of_t, t0: float, t1: float, omega_max: float, m: float = 0.0,
                                  field: str = "dirac", n_omega: int = 200) -> dict:
    """Born Dirac (or Weyl) pairs per volume from a homogeneous metric perturbation g = eta + h(t), vertex -(1/2) h T.

    h_of_t(t_array) returns lower-index h_{mu nu}, shape (len(t), 4, 4). As qp.born_metric_homogeneous:
    N/V = (1/4) int dOmega/(2pi) [rho2 X2 + rho0 X0] with dirac_stress_spectral_densities. FRW in conformal time,
    a = 1 + eps f(eta): h = 2 eps f eta_{mu nu} feeds only the trace channel (rho0 ~ m^2).
    Quantity: dict with 'pairs_per_volume' (in-in mean number of fermion-antifermion PAIRS per unit volume,
        spin-summed, energy^3; per comoving volume in FRW), 'particles_per_volume' (= 2 x pairs), 'spin2_part', 'spin0_part'.
    Valid when: |h| << 1 (first order), h -> 0 at both ends of [t0, t1], negligible spectrum above omega_max > 2m;
        m >= 0 (Weyl: m = 0)."""
    m = _mass(m)
    _field(field, _FIELDS_GRAV)
    if not omega_max > 2 * m or t1 <= t0 or n_omega < 16:
        raise ValueError("need omega_max > 2m, t1 > t0 and n_omega >= 16")
    if m > 0:
        u, wu = qp._gauss_legendre(0.0, math.sqrt(omega_max - 2 * m), n_omega)
        om, w = 2 * m + u * u, 2 * u * wu
    else:
        om, w = qp._gauss_legendre(0.0, omega_max, n_omega)
    H = qp._ft_time(h_of_t, t0, t1, om)
    if H.shape[-2:] != (4, 4):
        raise ValueError("h_of_t must return shape (len(t), 4, 4)")
    z = np.zeros_like(om)
    X2, X0 = qp._metric_weights(om, z, z, z, H)
    r2, r0 = dirac_stress_spectral_densities(om * om, m, field)
    p2 = float(np.sum(w * 0.25 * r2 * X2 / (2 * PI)))
    p0 = float(np.sum(w * 0.25 * r0 * X0 / (2 * PI)))
    return {"pairs_per_volume": p2 + p0, "particles_per_volume": 2 * (p2 + p0), "spin2_part": p2, "spin0_part": p0}


def born_dirac_metric_planar(htilde, s_max: float, y_max: float, m: float = 0.0, field: str = "dirac",
                             n_s: int = 320, n_y: int = 320) -> dict:
    """Born Dirac (or Weyl) pairs per unit transverse area from a planar metric perturbation h_{mu nu}(t, z).

    htilde(K0, Kz) returns lower-index h~_{mu nu}, shape (..., 4, 4). N/A = (1/4) int ds dy/(2 (2pi)^2) [rho2 X2 + rho0 X0].
    A plane gravitational wave (null support) gives zero: rho2 ~ s^2 on the light cone even for massless fermions.
    Quantity: dict with 'pairs_per_area' (in-in mean number of PAIRS per unit transverse area, spin-summed, energy^2)
        and 'particles_per_area'.
    Valid when: |h| << 1; spectrum negligible beyond s_max, |y| > y_max; m >= 0 (Weyl: m = 0); Gauss grids resolve h~."""
    m = _mass(m)
    _field(field, _FIELDS_GRAV)
    if not s_max > 4 * m * m or not y_max > 0 or min(n_s, n_y) < 8:
        raise ValueError("need s_max > 4 m^2, y_max > 0 and n_s, n_y >= 8")
    s, ws = qp._s_nodes(4 * m * m, s_max, n_s)
    y, wy = qp._gauss_legendre(-y_max, y_max, n_y)
    S, Y = np.meshgrid(s, y, indexing="ij")
    rs = np.sqrt(S)
    K0, Kz = rs * np.cosh(Y), rs * np.sinh(Y)
    z = np.zeros_like(K0)
    X2, X0 = qp._metric_weights(K0, z, z, Kz, np.asarray(htilde(K0, Kz)))
    r2, r0 = dirac_stress_spectral_densities(S, m, field)
    N = float(np.einsum("i,j,ij->", ws, wy, 0.25 * (r2 * X2 + r0 * X0)) / (2 * (2 * PI) ** 2))
    return {"pairs_per_area": N, "particles_per_area": 2 * N}


def born_dirac_metric_general(htilde4, s_max: float, kappa_max: float, m: float = 0.0, field: str = "dirac",
                              n_s: int = 40, n_k: int = 40, n_c: int = 16, n_p: int = 16) -> dict:
    """Born Dirac (or Weyl) pairs from a metric perturbation h_{mu nu}(t, x) of ANY profile, 4D spectral form.

    htilde4(K0, Kx, Ky, Kz) returns lower-index h~_{mu nu}(K), shape (..., 4, 4):
        N = (1/4) int d^4K/(2pi)^4 theta(K0) [rho2(K^2) X2 + rho0(K^2) X0].
    Quantity: dict with 'pairs' (total in-in mean number of fermion-antifermion PAIRS, spin-summed), 'particles',
        'spin2_part', 'spin0_part'.
    Valid when: |h| << 1; spectrum negligible beyond s_max, kappa_max; m >= 0 (Weyl: m = 0); grids resolve h~."""
    m = _mass(m)
    _field(field, _FIELDS_GRAV)
    if not s_max > 4 * m * m or not kappa_max > 0:
        raise ValueError("need s_max > 4 m^2 and kappa_max > 0")
    S, K0, Kx, Ky, Kz, W = qp._four_nodes(4 * m * m, s_max, kappa_max, n_s, n_k, n_c, n_p)
    X2, X0 = qp._metric_weights(K0, Kx, Ky, Kz, np.asarray(htilde4(K0, Kx, Ky, Kz)))
    r2, r0 = dirac_stress_spectral_densities(S, m, field)
    p2, p0 = float(np.sum(W * 0.25 * r2 * X2)), float(np.sum(W * 0.25 * r0 * X0))
    return {"pairs": p2 + p0, "particles": 2 * (p2 + p0), "spin2_part": p2, "spin0_part": p0}


# ---------------------------------------------------------------- PART 3: Dirac field in flat FRW (exact)
def frw_dirac_production(k, a, m: float, eta0: float, eta1: float, **solver) -> dict:
    """Exact Dirac pair creation in flat FRW per comoving mode and helicity, via the two-level reduction.

    psi = a^{-3/2} chi turns the Dirac equation in ds^2 = a(eta)^2 (d eta^2 - dx^2) into the flat one with mass m a(eta);
    per comoving k and helicity: i c' = (m a(eta) sigma_z + k sigma_x) c, solved by qp.bogoliubov_fermion_efield with
    p_of_t = m a(eta), eps_perp = k (keyword arguments go to that solver).
    Quantity: dict whose 'n' is the per-mode, per-helicity in-in mean number of electrons in comoving mode k (= positrons
        in -k = pairs in that mode), dimensionless, with the solver's floor/resolved flags. Both helicities give the same
        n; pairs per COMOVING volume = qp.number_density_isotropic(n_of_k, kmax, g=2) (divide by a_out^3 for physical).
    Valid when: k > 0 (comoving, energy), m >= 0, a(eta) > 0 and static at both ends of [eta0, eta1] (conformal time)."""
    m = _mass(m)
    k = np.atleast_1d(qp._positive(k, "k")).astype(float)
    for e in (eta0, eta1):
        if not float(a(e)) > 0:
            raise ValueError(f"a(eta) must be > 0 (a({e}) = {float(a(e))})")
    return qp.bogoliubov_fermion_efield(lambda eta: m * float(a(eta)) * np.ones_like(k), k, eta0, eta1, **solver)


def frw_dirac_tanh_n(k, m: float, A: float, B: float, rho: float):
    """Closed-form Dirac occupation in the FRW universe a(eta) = A + B tanh(rho eta) (tanh in a, not a^2).

    The two-level problem i c' = (m a sigma_z + k sigma_x) c is the Sauter problem with k_par -> m A, eE0 tau -> m B,
    tau -> 1/rho, eps_perp -> k, so n_k = qp.sauter_n_spinor(m A, k, 0, m B rho, 1/rho) (Gavrilov & Gitman 1996 eq. 42):
        n_k = sinh[pi (m B - w_-)/rho] sinh[pi (m B + w_-)/rho] / (sinh(pi w_in/rho) sinh(pi w_out/rho)),
        w_in/out = sqrt(k^2 + m^2 (A -/+ B)^2), w_- = (w_out - w_in)/2  (B > 0; the result is even in B).
    Quantity: per comoving mode, per helicity in-in mean number of electrons (= positrons = pairs in the mode),
        dimensionless.
    Valid when: k > 0, m > 0, rho > 0, A > |B| (a > 0 throughout); conformal time eta, comoving k."""
    m = _mass(m)
    k = qp._positive(k, "k")
    rho = float(qp._positive(rho, "rho"))
    if not m > 0:
        raise ValueError("m must be > 0 (massless: n_k = 0 exactly, conformal invariance)")
    if not A > abs(B):
        raise ValueError("need A > |B| so that a(eta) > 0")
    if B == 0:
        return np.zeros_like(k)
    return qp.sauter_n_spinor(m * A + 0.0 * k, k, 0.0, m * abs(B) * rho, 1.0 / rho)   # eps_perp^2 = 0^2 + k_perp^2 = k^2


# ---------------------------------------------------------------- explicit spinors (self-test machinery)
def _spinors(p, m):
    """u(p, s), v(p, s) in the Dirac representation, shape (..., 4, 2) (column = spin), ubar u = 2m, u^dag u = 2E."""
    p = np.asarray(p, dtype=float)
    E = np.sqrt(m * m + np.sum(p * p, axis=-1))
    sp = np.einsum("...i,iab->...ab", p, _SIG)
    r = np.sqrt(E + m)[..., None, None]
    eye = np.broadcast_to(np.eye(2), sp.shape)
    u = np.concatenate([r * eye, sp / r], axis=-2)
    v = np.concatenate([sp / r, r * eye], axis=-2)
    return u, v, E


def _currents(p1, p2, m):
    """J^mu[s1, s2] = ubar(p1, s1) gamma^mu v(p2, s2), shape (..., 4, 2, 2), by explicit spinors."""
    u, _, E1 = _spinors(p1, m)
    _, v, E2 = _spinors(p2, m)
    ubar = np.swapaxes(np.conj(u), -1, -2) @ _GAM[0]                               # (..., 2, 4)
    return ubar[..., None, :, :] @ (_GAM @ v[..., None, :, :]), E1, E2               # (..., 4, 2, 2)


def _rest_frame_pairs(s, m, n):
    E = math.sqrt(s) / 2
    p = math.sqrt(max(E * E - m * m, 0.0))
    ct, wct = np.polynomial.legendre.leggauss(n)
    ph = np.arange(2 * n) * PI / n
    C, P = np.meshgrid(ct, ph, indexing="ij")
    st = np.sqrt(1 - C * C)
    nv = np.stack([st * np.cos(P), st * np.sin(P), C], axis=-1)
    w = (wct[:, None] * np.ones_like(P)) * (PI / n) * p / (16 * PI * PI * math.sqrt(s))   # dPhi2 = |p| dOmega/(16 pi^2 sqrt s)
    p1 = np.concatenate([np.full(C.shape + (1,), E), p * nv], axis=-1)
    p2 = np.concatenate([np.full(C.shape + (1,), E), -p * nv], axis=-1)
    return p1, p2, w


def _vector_spectral_numeric(s: float, m: float, field: str, n: int = 16):
    """(rhoV, structure violation, max |K.J|) by explicit spinors / scalar vertices and angular quadrature."""
    p1, p2, w = _rest_frame_pairs(s, m, n)
    if field == "dirac":
        J, _, _ = _currents(p1[..., 1:], p2[..., 1:], m)                           # (..., 4, 2, 2)
        rho = np.einsum("xy,xyaij,xybij->ab", w, J, np.conj(J)).real
        cons = float(np.abs(J[..., 0, :, :]).max())                                # K_mu J^mu = sqrt(s) J^0
    else:
        q = p1 - p2                                                                # <p1 p2|j|0> = (p1 - p2)^mu
        rho = np.einsum("xy,xya,xyb->ab", w, q, q)
        cons = float(np.abs(q[..., 0]).max())
    rv = -np.einsum("ab,ab->", _ETA, rho) / (3 * s)
    target = rv * (np.outer([math.sqrt(s), 0, 0, 0], [math.sqrt(s), 0, 0, 0]) - s * np.linalg.inv(_ETA))
    return float(rv), float(np.abs(rho - target).max() / (s * abs(rv))), cons


def _stress_amplitudes(p1, p2, m):
    """t^{mu nu}[s1, s2] = (1/4) ubar [gamma^mu q^nu + gamma^nu q^mu] v, q = p1 - p2 (upper indices)."""
    J, E1, E2 = _currents(p1, p2, m)
    q = np.concatenate([(E1 - E2)[..., None], p1 - p2], axis=-1)
    t = 0.25 * (np.einsum("...aij,...b->...abij", J, q) + np.einsum("...bij,...a->...abij", J, q))
    return t, E1, E2


def _dirac_stress_numeric(s: float, m: float, n: int = 16):
    """(rho2, rho0, max |K_mu t^{mu nu}|) for Dirac pairs by explicit spinors and angular quadrature (K at rest)."""
    p1, p2, w = _rest_frame_pairs(s, m, n)
    t, _, _ = _stress_amplitudes(p1[..., 1:], p2[..., 1:], m)
    viol = float(np.abs(t[..., 0, :, :, :]).max())                                  # K_mu t^{mu nu} = sqrt(s) t^{0 nu}
    rho = np.einsum("xy,xyabij,xycdij->abcd", w, t, np.conj(t)).real
    K = np.array([math.sqrt(s), 0, 0, 0])
    Pl = _ETA @ (np.linalg.inv(_ETA) - np.outer(K, K) / s) @ _ETA
    Pi2 = 0.5 * (np.einsum("ac,bd->abcd", Pl, Pl) + np.einsum("ad,bc->abcd", Pl, Pl)) - np.einsum("ab,cd->abcd", Pl, Pl) / 3
    return float(np.einsum("abcd,abcd->", Pi2, rho)) / 5.0, float(np.einsum("ab,cd,abcd->", Pl, Pl, rho)) / 9.0, viol


# ---------------------------------------------------------------- self-test
def selftest(verbose: bool = True) -> bool:
    """Compare with closed forms, published equations, exact solvers and independent integrals. True if all pass."""
    results = []

    def check(name, got, want, tol, rel=False):
        err = abs(got - want) / (abs(want) if rel and want != 0 else 1.0)
        ok = bool(err <= tol)
        results.append(ok)
        if verbose:
            print(f"{'PASS' if ok else 'FAIL'}  {name}: {got:.10g} (expected {want:.10g}, "
                  f"{'rel' if rel else 'abs'} tol {tol:g})")

    e2 = 4 * PI * ALPHA

    # 1a. rhoV from explicit Dirac spinors / scalar vertices with angular quadrature (16 x 32 nodes; the integrand is a
    #     polynomial of degree 2 in the angles, so the quadrature is exact to roundoff: tol 1e-12), current conservation
    #     and the tensor structure (K K - s eta) to roundoff.
    for s_, m_, fld in ((9.0, 0.7, "dirac"), (4.0, 0.0, "dirac"), (9.0, 0.7, "scalar")):
        rv, struct, cons = _vector_spectral_numeric(s_, m_, fld)
        check(f"{fld} m={m_} s={s_}: rhoV by explicit vertices = closed form (rel.); structure and K.J = 0 (< 1e-12)",
              abs(rv / float(vector_spectral_density([s_], m_, fld)[0]) - 1) + float(max(struct, cons / s_) > 1e-12), 0.0,
              1e-12)

    # 1b. Rosner, "The Standard Model in 2001", hep-ph/0108195, p. 14 (fetch_text, verbatim): "For fermions f of charge
    #     ef and mass mf , Im Π f (s) = αe2 f 3 ( 1 + 2m2 f s )( 1− 4m2 f s )1/2 θ(s− 4m2 f ) , (45) while for scalar
    #     particles of charge es and mass ms, Im Π s(s) = αe2 s 12 ( 1− 4m2 s s )3/2 θ(s− 4m2 s) . (46)" -- the
    #     extraction drops the fraction bars; reading: Im Pi_f = (alpha e_f^2/3)(1 + 2m^2/s)(1 - 4m^2/s)^(1/2),
    #     Im Pi_s = (alpha e_s^2/12)(1 - 4m^2/s)^(3/2); his eq. 44 "Im Π i(s) = s 4πασ(e+e−→i¯i)" fixes the sign (> 0).
    #     (Peskin & Schroeder eq. 7.92, paywalled, is the same.) Ishikawa, Kimura, Shigaki & Tsuji, arXiv:1304.3655,
    #     p. 23: "The imaginary part is thus ImΠ(k2) =−α 6 (2 + 1/y) √ 1− 1/y. (D.3)" with "y≡k2/(2m)2" (reading:
    #     -(alpha/6)(2 + 1/y) sqrt(1 - 1/y), the opposite sign convention). Closed forms: roundoff tolerance.
    for s_ in (4.5, 9.0, 40.0):
        b = math.sqrt(1 - 4 / s_)
        check(f"Im Pi Dirac (s = {s_} m^2) = (alpha/3)(1 + 2m^2/s) beta [Rosner eq. 45]",
              float(im_vacuum_polarization([s_], 1.0)[0]), ALPHA / 3 * (1 + 2 / s_) * b, 1e-14, rel=True)
        check(f"Im Pi scalar (s = {s_} m^2) = (alpha/12) beta^3 [Rosner eq. 46]",
              float(im_vacuum_polarization([s_], 1.0, "scalar")[0]), ALPHA / 12 * b ** 3, 1e-14, rel=True)
    check("Ishikawa et al. eq. D.3: |Im Pi| = (alpha/6)(2 + 1/y) sqrt(1 - 1/y), y = s/4m^2 = 2.5",
          float(im_vacuum_polarization([10.0], 1.0)[0]), ALPHA / 6 * (2 + 1 / 2.5) * math.sqrt(1 - 1 / 2.5), 1e-14, rel=True)

    # 1c. PDG 2024 review "Cross-section formulae for specific processes" (pdg.lbl.gov rpp2024-rev-cross-section-
    #     formulae.pdf, p. 1, verbatim): "dσ dΩ=Nc α2 4sβ  1 + cos2θ+ (1−β2) sin2θ  Q2 f , (51.2) where βis v/c for the
    #     produced fermions in the c.m." (reading: dsigma/dOmega = Nc alpha^2/(4s) beta [1 + cos^2 + (1 - beta^2) sin^2]
    #     Q_f^2; the brackets are lost in extraction). Integrated over angles by 24-point
    #     Gauss-Legendre (a degree-2 polynomial in cos theta: exact), against sigma = e^2 (e^2 rhoV)/(2s) (massless e+e-,
    #     one-photon exchange, spin-averaged), the optical-theorem link between rhoV and a measured cross section.
    ct, wct = np.polynomial.legendre.leggauss(24)
    for s_, m_ in ((9.0, 1.0), (4.4, 1.0), (5.0, 0.0)):
        b = math.sqrt(1 - 4 * m_ * m_ / s_)
        sig_pdg = 2 * PI * float(np.sum(wct * ALPHA ** 2 / (4 * s_) * b * (1 + ct ** 2 + (1 - b * b) * (1 - ct ** 2))))
        check(f"PDG eq. 51.2 integrated (s = {s_}, m = {m_}) = e^4 rhoV/(2s)", e2 * e2 * float(
            vector_spectral_density([s_], m_)[0]) / (2 * s_), sig_pdg, 1e-13, rel=True)

    # 1d. Redi & Tesi 2026 (arXiv:2606.28297), p. 5 (fetch_text, verbatim): "2Im[Γ(A)] = Z d4q (2π)4Aµ(q)Aν(−q)Im[⟨Jµ(q)
    #     Jν(−q)⟩] = e2 12π Z d4q (2π)4θ(q2)(|⃗E(q)|2−| ⃗B(q)|2).(7)" ("Z" is the integral sign; reading: e^2/(12 pi) int
    #     d^4q/(2pi)^4 theta(q^2)(|E|^2 - |B|^2)), for massless Dirac. theta(q^2) covers BOTH light cones (equal for
    #     real A), so the K0 > 0 kernel is 2 e^2/(12 pi) = e^2 rhoV(m = 0). Exact.
    check("Redi-Tesi eq. 7: massless Dirac e^2 rhoV = 2 x e^2/(12 pi) (both cones -> K0 > 0)",
          e2 * float(vector_spectral_density([3.0], 0.0)[0]), 2 * e2 / (12 * PI), 1e-15, rel=True)

    # 1e. Algebra (consistency, not a reference): X_V = |eE~|^2 - |eB~|^2 and gauge invariance, random complex eA, timelike
    #     and spacelike K (roundoff tolerance relative to |K|^2 |A|^2).
    rng = np.random.default_rng(7)
    Ks = rng.normal(size=(6, 4)) * np.array([3, 1, 1, 1])
    As = rng.normal(size=(6, 4)) + 1j * rng.normal(size=(6, 4))
    X = em_weight(*Ks.T, As)
    Ef, Bf = fields_from_potential(*Ks.T, As)
    lam = rng.normal(size=6) + 1j * rng.normal(size=6)
    Kl = Ks * np.array([1, -1, -1, -1])                                                     # K_mu (lower)
    Xg = em_weight(*Ks.T, As + lam[:, None] * Kl)
    scale = float(np.max(np.sum(Ks ** 2, 1) * np.sum(np.abs(As) ** 2, 1)))
    check("X_V = |E|^2 - |B|^2 and gauge invariance (max abs. difference / scale)",
          float(max(np.abs(X - (np.sum(np.abs(Ef) ** 2, -1) - np.sum(np.abs(Bf) ** 2, -1))).max(),
                    np.abs(X - Xg).max())) / scale, 0.0, 1e-13)

    # 1f. Exact cross-check, homogeneous field: Sauter pulse eE0 sech^2(t/tau), m = tau = 1 (perturbative: gamma =
    #     m/(eE0 tau) = 20, 10). Exact pairs per volume from the Gavrilov-Gitman occupations (hep-th/9603152 eqs. 42-43,
    #     quoted in qp) integrated over modes, against born_qed_homogeneous (numerical Fourier transform). Born is
    #     O(E0^2) exact and the total is even in E0 (charge conjugation), so |exact/Born - 1| scales as E0^2: measured
    #     (4/3)(eE0 tau^2)^2 (Dirac) and 7.5 (eE0 tau^2)^2 (scalar) at m tau = 1 (the coefficient changes by < 0.3% between
    #     the two amplitudes). Bound: 1.5x that coefficient; the deviation must also stay below the function's own
    #     error_estimate, and R2 must equal its closed form 2 eE0 tau^2 to 1e-3 (trapezoid A(t) on a uniform grid).
    #     Ratio test: the next relative correction is O(E0^4), measured ratio 3.99-4.00, window [3.6, 4.4].
    for fld, coef in (("dirac", 4.0 / 3.0), ("scalar", 7.5)):
        devs = []
        for eE0 in (0.05, 0.1):
            ex = sauter_exact_pairs_per_volume(1.0, eE0, 1.0, fld)
            bo = born_qed_homogeneous(lambda t, eE0=eE0: eE0 / np.cosh(t) ** 2, -20.0, 20.0, 1.0, 30.0, fld)
            devs.append(ex / bo["pairs_per_volume"] - 1)
            check(f"Sauter {fld}, eE0 = {eE0} m^2: |exact (GG eqs. 42-43)/Born - 1| <= 1.5 x {coef:.3g} (eE0 tau^2)^2 "
                  f"and <= error_estimate = {bo['error_estimate']:.3g} (R2 = {bo['R2']:.3g}, analytic 2 eE0 tau^2)",
                  abs(devs[-1]) + float(abs(devs[-1]) > bo["error_estimate"] or abs(bo["R2"] / (2 * eE0) - 1) > 1e-3),
                  0.0, 1.5 * coef * eE0 ** 2)
        check(f"Sauter {fld}: deviation x4 when E0 doubles (O(E0^2) Born error; ratio in [3.6, 4.4])",
              devs[1] / devs[0], 4.0, 0.4)
    #     ...the numerical Fourier transform against the analytic one (consistency; the FT quadrature is converged to
    #     ~1e-12, and the sqrt-threshold Omega grid of both to 1e-10).
    check("born_qed_homogeneous (numerical FT) = sauter_born_pairs_per_volume (analytic FT)", bo["pairs_per_volume"],
          sauter_born_pairs_per_volume(1.0, 0.1, 1.0, "scalar"), 1e-9, rel=True)

    # 1g. Per mode: born_mode_efield against qp's exact two-level and boson solvers for a pulse with zero net kick,
    #     e A(t) = a exp(-t^2/2 tau^2) (tau = 0.5, m = 1), eE~(Omega) = -i Omega a sqrt(2 pi) tau exp(-Omega^2 tau^2/2).
    #     Per-mode corrections are O(a) (odd terms survive mode by mode): measured max 0.035 (Dirac) and 0.056
    #     (scalar) at a = 0.02; bounds 2.5 a and 4 a. The scalar Born term is proportional to k_par^2, so near k_par = 0
    #     the second-order (e dA)^2 term wins (k_par = 0.05: 40% off at a = 0.02): scalar modes need e|dA| << |k_par|,
    #     and only |k_par| >= 0.3 is compared for the scalar.
    kz = np.array([-0.8, -0.3, 0.05, 0.4, 1.0])
    kp = np.array([0.2, 0.5, 0.1, 0.3, 0.7])
    ep = np.sqrt(1 + kp * kp)
    tg = 0.5
    devs = {"dirac": [], "scalar": []}
    for a in (0.02, 0.04):
        eEt = lambda Om, a=a: -1j * Om * a * math.sqrt(2 * PI) * tg * np.exp(-Om * Om * tg * tg / 2)   # noqa: E731
        gf = lambda t, a=a: kz + a * np.exp(-t * t / (2 * tg * tg))   # noqa: E731
        rf = qp.bogoliubov_fermion_efield(gf, ep, -15 * tg, 15 * tg, rtol=1e-8)
        rb = qp.bogoliubov_boson(lambda t, gf=gf: ep ** 2 + gf(t) ** 2, -15 * tg, 15 * tg, rtol=1e-8)
        devs["dirac"].append(float(np.max(np.abs(rf["n"] / born_mode_efield(kz, kp, 1.0, eEt) - 1))))
        far = np.abs(kz) >= 0.3
        devs["scalar"].append(float(np.max(np.abs(rb["beta2"][far] / born_mode_efield(kz[far], kp[far], 1.0, eEt, "scalar")
                                                  - 1))))
        check(f"per-mode Born vs qp two-level solver (Dirac), a = {a}: max |exact/Born - 1| <= 2.5 a",
              devs["dirac"][-1], 0.0, 2.5 * a)
        check(f"per-mode Born vs qp boson solver (scalar QED), a = {a}: max |exact/Born - 1| <= 4 a",
              devs["scalar"][-1], 0.0, 4 * a)
    #     (the O(a^2) relative correction shifts the ratio by ~a: measured 1.98-2.02, window [1.8, 2.2])
    check("per-mode deviations double when a doubles (Dirac and scalar; ratios in [1.8, 2.2])",
          max(abs(devs[f][1] / devs[f][0] - 2) for f in devs), 0.0, 0.2)

    # 1h. Mode sum of the per-mode Born occupations (two-level reduction) = the spectral form (Dirac traces): two
    #     independent derivations of the same first-order number. Gaussian pulse above, a = 0.03; spherical Gauss grid
    #     (converged to ~1e-12 for this smooth integrand: tol 1e-9).
    eEt = lambda Om: -1j * Om * 0.03 * math.sqrt(2 * PI) * tg * np.exp(-Om * Om * tg * tg / 2)   # noqa: E731
    kk, wk = qp._gauss_legendre(0.0, 14.0, 96)
    cc, wc = np.polynomial.legendre.leggauss(24)
    KK, CC = np.meshgrid(kk, cc, indexing="ij")
    eAt = lambda t: 0.03 * np.exp(-t * t / (2 * tg * tg))   # noqa: E731
    for fld, g in (("dirac", 2.0), ("scalar", 1.0)):
        ms = g * float(np.einsum("i,j,ij->", wk * kk * kk, wc,
                                 born_mode_efield(KK * CC, KK * np.sqrt(1 - CC * CC), 1.0, eEt, fld))) / (4 * PI * PI)
        sp = born_qed_homogeneous(lambda t: eAt(t) * t / (tg * tg), -15 * tg, 15 * tg, 1.0, 40.0, fld)["pairs_per_volume"]
        check(f"{fld}: g int d^3k/(2pi)^3 n_k(Born, per mode) = spectral int dOmega |eE~|^2 rhoV/(2pi)", ms, sp, 1e-9,
              rel=True)

    # 1i. General 4D spectral form against an INDEPENDENT 6D pair-momentum integral with explicit spinors (reduced to 3D
    #     by isotropy, as qp's D4): a scalar potential eA_0 = exp(-r^2/2) cos(3 t) exp(-t^2/2) only, so the coupling is
    #     eA~_0 u^dag(p1) v(p2) and X_V = |K|^2 |eA~_0|^2. m = 1. Both grids converged to < 1e-7 (tol 1e-6).
    def phi4(K0, Kx, Ky, Kz):
        k2 = Kx * Kx + Ky * Ky + Kz * Kz
        return (2 * PI) ** 2 * np.exp(-k2 / 2) * 0.5 * (np.exp(-(K0 - 3.0) ** 2 / 2) + np.exp(-(K0 + 3.0) ** 2 / 2))
    A4 = lambda K0, Kx, Ky, Kz: np.stack([phi4(K0, Kx, Ky, Kz)] + [0 * K0] * 3, axis=-1)   # noqa: E731
    gen = born_qed_general(A4, 1.0, 80.0, 8.0, n_c=8, n_p=4)["pairs"]
    p1, w1 = qp._gauss_legendre(0, 8, 40)
    c12, w12 = np.polynomial.legendre.leggauss(24)
    P1, P2, C12 = np.meshgrid(p1, p1, c12, indexing="ij")
    v1 = np.stack([0 * P1, 0 * P1, P1], -1)
    v2 = np.stack([P2 * np.sqrt(1 - C12 ** 2), 0 * P2, P2 * C12], -1)
    J, E1, E2 = _currents(v1, v2, 1.0)
    Kn = np.sqrt(P1 ** 2 + P2 ** 2 + 2 * P1 * P2 * C12)
    amp2 = np.abs(phi4(E1 + E2, Kn, 0 * Kn, 0 * Kn)) ** 2 * np.sum(np.abs(J[..., 0, :, :]) ** 2, axis=(-1, -2))
    direct = 4 * PI * 2 * PI * float(np.einsum("i,j,k,ijk->", w1 * p1 * p1, w1 * p1 * p1, w12, amp2 / (4 * E1 * E2))) \
        / (2 * PI) ** 6
    check("QED general 4D spectral form = direct 6D e+e- momentum integral (explicit spinors)", gen, direct, 1e-6, rel=True)

    # 1j. Planar form against a direct pair-momentum integral (explicit spinors): longitudinal eA_3(t, z), so
    #     N/A = int d^2p_perp dp1z dp2z/((2pi)^4 4 E1 E2) sum |eA~_3 ubar gamma^3 v|^2 with p1_perp = -p2_perp. m = 0.6.
    def a3(K0, Kz):
        return PI * (np.exp(-(K0 - 3.0) ** 2 / 2) + np.exp(-(K0 + 3.0) ** 2 / 2)) * np.exp(-Kz * Kz / 2)
    A2 = lambda K0, Kz: np.stack([0 * K0, 0 * K0, 0 * K0, a3(K0, Kz)], axis=-1)   # noqa: E731
    pla = born_qed_planar(A2, 0.6, 80.0, 5.0, n_s=160, n_y=160)["pairs_per_area"]
    pt, wpt = qp._gauss_legendre(0, 7, 40)          # converged to 1e-7 (32 x 36 nodes on [0, 6]: 4e-7)
    pz, wpz = qp._gauss_legendre(-7, 7, 48)
    PT, Z1, Z2 = np.meshgrid(pt, pz, pz, indexing="ij")
    J, E1, E2 = _currents(np.stack([PT, 0 * PT, Z1], -1), np.stack([-PT, 0 * PT, Z2], -1), 0.6)
    amp2 = np.abs(a3(E1 + E2, Z1 + Z2)) ** 2 * np.sum(np.abs(J[..., 3, :, :]) ** 2, axis=(-1, -2))
    direct = 2 * PI * float(np.einsum("i,j,k,ijk->", wpt * pt, wpz, wpz, amp2 / (4 * E1 * E2))) / (2 * PI) ** 4
    check("QED planar (s, rapidity) form = direct pair-momentum integral (explicit spinors)", pla, direct, 1e-6, rel=True)
    #     ...and a TRANSVERSE potential eA_1(t, z): E_x = K0 a and B_y = Kz a are both nonzero, X_V = (K0^2 - Kz^2)|a|^2 =
    #     |E|^2 - |B|^2, so the magnetic term's minus sign is tested (|E|^2 + |B|^2 would give +10%). The azimuthal
    #     dependence is a trigonometric polynomial of degree 2: 8 angles are exact. The direct integral is converged to
    #     ~4e-7 (24 x 30 nodes on [0, 6] and 36 x 44 on [0, 7] agree to that), hence tol 1e-6.
    A1 = lambda K0, Kz: np.stack([0 * K0, a3(K0, Kz), 0 * K0, 0 * K0], axis=-1)   # noqa: E731
    pla1 = born_qed_planar(A1, 0.6, 80.0, 5.0, n_s=160, n_y=160)["pairs_per_area"]
    pt, wpt = qp._gauss_legendre(0, 6, 24)
    pz, wpz = qp._gauss_legendre(-6, 6, 30)
    phs = np.arange(8) * 2 * PI / 8
    PT, PH, Z1, Z2 = np.meshgrid(pt, phs, pz, pz, indexing="ij")
    J, E1, E2 = _currents(np.stack([PT * np.cos(PH), PT * np.sin(PH), Z1], -1),
                          np.stack([-PT * np.cos(PH), -PT * np.sin(PH), Z2], -1), 0.6)
    amp2 = np.abs(a3(E1 + E2, Z1 + Z2)) ** 2 * np.sum(np.abs(J[..., 1, :, :]) ** 2, axis=(-1, -2))
    direct = float(np.einsum("i,k,l,ijkl->", wpt * pt, wpz, wpz, amp2 / (4 * E1 * E2))) * (2 * PI / 8) / (2 * PI) ** 4
    check("QED planar, transverse eA_1 (E and B nonzero: weight |E|^2 - |B|^2) = direct pair-momentum integral", pla1,
          direct, 1e-6, rel=True)

    # 1k. The trap the R2 indicator exists for: a Gaussian E pulse with m tau = 2 at weak field (eE0 = 0.02 m^2,
    #     eE0 tau^2 = 0.08). qp's exact two-level solver over 1024 modes gives 3.1 x the one-photon Born yield
    #     (multiphoton absorption beats the exp(-2 m^2 tau^2) Fourier tail); born_qed_homogeneous must refuse it.
    taug = 2.0
    kq, wq = qp._gauss_legendre(0, 8, 64)
    cq, wcq = np.polynomial.legendre.leggauss(16)
    KQ, CQ = np.meshgrid(kq, cq, indexing="ij")
    kzq, kpq = (KQ * CQ).ravel(), (KQ * np.sqrt(1 - CQ * CQ)).ravel()
    shift = 0.02 * taug * math.sqrt(PI / 2)
    from math import erf
    rf = qp.bogoliubov_fermion_efield(lambda t: kzq + shift * erf(t / (math.sqrt(2) * taug)), np.sqrt(1 + kpq ** 2),
                                      -14 * taug, 14 * taug, rtol=1e-5)
    exg = 2 * float(np.einsum("i,j,ij->", wq * kq * kq, wcq, rf["n"].reshape(KQ.shape))) / (4 * PI * PI)
    gauss = lambda t: 0.02 * np.exp(-t * t / (2 * taug * taug))   # noqa: E731
    bog = born_qed_homogeneous(gauss, -14 * taug, 14 * taug, 1.0, 30.0, check=False)
    try:
        born_qed_homogeneous(gauss, -14 * taug, 14 * taug, 1.0, 30.0)
        refused = 0.0
    except ValueError:
        refused = 1.0
    check(f"Gaussian pulse, m tau = 2, eE0 tau^2 = 0.08: exact/Born = {exg / bog['pairs_per_volume']:.3g} > 2 and Born is "
          f"refused (error estimate {bog['error_estimate']:.3g} > 0.5)",
          float(exg / bog["pairs_per_volume"] > 2 and refused == 1.0), 1.0, 0)

    # 2a. Dirac stress densities from explicit spinors (angular quadrature exact for these polynomials: tol 1e-12),
    #     conservation K_mu t^{mu nu} = 0 to roundoff.
    for s_, m_ in ((9.0, 0.7), (4.0, 0.0), (20.0, 2.0)):
        r2n, r0n, viol = _dirac_stress_numeric(s_, m_)
        r2a, r0a = dirac_stress_spectral_densities([s_], m_)
        check(f"Dirac (m={m_}, s={s_}): rho2, rho0 by explicit spinors = closed forms (max rel.; conservation)",
              max(abs(r2n / r2a[0] - 1), abs(r0n - r0a[0]) / r2a[0], viol / s_), 0.0, 1e-12)

    # 2b. Redi & Tesi 2026 (arXiv:2606.28297), p. 4 (fetch_text, verbatim): "In our normalization,c 0 = 4/3,c 1/2 = 4
    #     andc 1 = 16 respectively for conformally coupled scalars, Weyl fermions and massless gauge fields. Using (3) we
    #     obtain, Ndec≡2ImΓ 1PI =− cJ 30720π Z d4q (2π)4θ(q2)hµν(q)Πµνρσ(q)hρσ(−q).(5)" (reading: -c_J/(30720 pi) int ...).
    #     For a TT h at rest h Pi h = -6 s^2 |h|^2 and theta(q^2) covers both cones, so the K0 > 0 kernel is rho2/4 =
    #     c s^2/(2560 pi) (as in qp's D1). Exact.
    check("Weyl: rho2/4 = c s^2/(2560 pi) with Redi-Tesi c_1/2 = 4", float(dirac_stress_spectral_densities([2.0], 0.0,
          "weyl")[0][0]) / 4, 4.0 * 4.0 / (2560 * PI), 1e-14, rel=True)
    r2s, _ = qp.stress_spectral_densities([2.0], "scalar")
    check("massless Dirac / real scalar rho2 = 2 c_1/2 / c_0 = 6", float(dirac_stress_spectral_densities([2.0])[0][0] / r2s[0]),
          6.0, 1e-14, rel=True)

    # 2c. Han, Lykken & Zhang, hep-ph/9811350, pp. 11-12 (fetch_text, verbatim): "Γ(~h →VV ) = N κ2m3 ~h 160π, (46)
    #     where N = 1 (8) for photons (gluons)" and "Γ(~h →f ¯f ) = Nc κ2m3 ~h 320π (1 − 4rf )3/2(1 + 8 3rf ), (52)"
    #     (reading: N kappa^2 m^3/(160 pi) and Nc kappa^2 m^3/(320 pi) (1 - 4r)^(3/2) (1 + 8r/3), r = m_f^2/m_h^2).
    #     Both widths are kappa^2 rho2(m_h^2)/(const x m_h) in the same normalisation, so photon/Dirac = (1/160)/(1/320) = 2
    #     (qp's photon rho2, itself checked there), and rho2(m)/rho2(0) at fixed s = (1 - 4r)^{3/2}(1 + 8r/3). Exact.
    r2p, _ = qp.stress_spectral_densities([5.0], "photon")
    check("HLZ eqs. 46/52: photon / Dirac rho2 (massless) = 2", float(r2p[0] / dirac_stress_spectral_densities([5.0])[0][0]),
          2.0, 1e-14, rel=True)
    for r in (0.05, 0.15, 0.24):
        check(f"HLZ eq. 52: rho2(m)/rho2(0) = (1 - 4r)^1.5 (1 + 8r/3) at r = m^2/s = {r}",
              float(dirac_stress_spectral_densities([1.0], math.sqrt(r))[0][0] / dirac_stress_spectral_densities([1.0])[0][0]),
              (1 - 4 * r) ** 1.5 * (1 + 8 * r / 3), 1e-13, rel=True)

    # 2d. Trace channel normalisation from the Higgs width. Djouadi, hep-ph/0503172 (fetch_text, verbatim): "LMV ∼M 2 V
    #     ( 1 + H v )2 , Lmf ∼ −mf ( 1 + H v ) (1.46)", i.e. H enters exactly as a mass perturbation dm/m = H/v, as the FRW
    #     trace channel does; "v = 1 ( √ 2Gµ)1/2 ≃ 246 GeV (1.48)"; "Γ Born(H →f ¯f ) = GµNc 4 √ 2π MHm2 fβ3 f (2.6)"
    #     (reading: v = (sqrt2 G_mu)^(-1/2), Gamma = G_mu Nc/(4 sqrt2 pi) M_H m_f^2 beta^3). The width of
    #     -(m/v) H psibar psi is |m psibar psi|^2 phase space/(2 M v^2) = 9 rho0(M^2)/(2 M v^2), since 9 rho0 =
    #     int |pi_{mu nu} t^{mu nu}|^2 = int |m ubar v|^2. Exact (Nc = 1).
    Gmu = 1.1663787e-5                                    # any value: the check is an identity in Gmu
    for M, mf in ((125.0, 4.18), (3.0, 1.2)):
        v2 = 1 / (math.sqrt(2) * Gmu)
        width = 9 * float(dirac_stress_spectral_densities([M * M], mf)[1][0]) / (2 * M * v2)
        b = math.sqrt(1 - 4 * mf * mf / (M * M))
        check(f"Djouadi eq. 2.6: Higgs width from rho0 (M = {M}, m_f = {mf})", width,
              Gmu / (4 * math.sqrt(2) * PI) * M * mf * mf * b ** 3, 1e-13, rel=True)

    # 3a. FRW reduction against published closed forms. a(eta) = A + B tanh(rho eta), m = 1, A = 1.3, B = 0.3, rho = 0.8:
    #     (i) qp's two-level solver run on i c' = (m a sigma_z + k sigma_x) c against the Sauter-map closed form
    #     (Gavrilov & Gitman eq. 42, frw_dirac_tanh_n), tol 1e-6 as qp's own Sauter checks; (ii) against Fuentes, Mann,
    #     Martin-Martinez & Moradi 2010 (arXiv:1007.1569), p. 3 (fetch_text, verbatim): "We consider the special solvable
    #     case presented in [50] C(η) = (1 + ǫ(1 + tanhρη))2" (so a = 1 + eps + eps tanh: A = 1 + eps, B = eps = 0.3) and
    #     "⏐⏐γ−⏐⏐2 = (ω− +mǫ)(ω+ +mǫ) (ω− −mǫ)(ω+ −mǫ) × sinh [ π ρ (ω− −mǫ) ] sinh [ π ρ (ω− +mǫ) ] sinh [ π ρ (ω+ +mǫ) ]
    #     sinh [ π ρ (ω+ −mǫ) ] (16)", "where ω± = (ωout ±ωin)/2" (reading: a ratio of the two rational products times
    #     sinh(pi(w- - m eps)/rho) sinh(pi(w- + m eps)/rho) / [sinh(pi(w+ + m eps)/rho) sinh(pi(w+ - m eps)/rho)]).
    #     Their gamma = beta/alpha refers to the unnormalised spinors
    #     of their eq. 15; the sinh structure is identical to GG's, and the rational prefactor equals (w_out + m a_out)/
    #     (w_out - m a_out), so n/(1 - n) = |gamma-|^2 (w_out - m a_out)/(w_out + m a_out) (our reading of their
    #     normalisation; it holds to roundoff for every k, tol 1e-10).
    kf = np.array([0.2, 0.7, 1.5, 3.0])
    eps_, rho_ = 0.3, 0.8
    rr = frw_dirac_production(kf, lambda e: 1 + eps_ + eps_ * math.tanh(rho_ * e), 1.0, -15 / rho_, 15 / rho_, rtol=1e-6)
    ncf = frw_dirac_tanh_n(kf, 1.0, 1 + eps_, eps_, rho_)
    check("FRW Dirac, a = A + B tanh(rho eta): two-level solver vs Sauter-map closed form (GG eq. 42), max rel.",
          float(np.max(np.abs(rr["n"] / ncf - 1))), 0.0, 1e-6)
    win, wout = np.sqrt(kf ** 2 + 1), np.sqrt(kf ** 2 + (1 + 2 * eps_) ** 2)
    wp, wm = (wout + win) / 2, (wout - win) / 2
    me = eps_
    g2 = ((wm + me) * (wp + me) / ((wm - me) * (wp - me)) * np.sinh(PI / rho_ * (wm - me)) * np.sinh(PI / rho_ * (wm + me))
          / (np.sinh(PI / rho_ * (wp + me)) * np.sinh(PI / rho_ * (wp - me))))
    mu = 1 + 2 * eps_
    check("FRW Dirac closed form vs Fuentes et al. eq. 16: n/(1-n) = |gamma|^2 (w - m a)/(w + m a) at out, max rel.",
          float(np.max(np.abs(ncf / (1 - ncf) / (g2 * (wout - mu) / (wout + mu)) - 1))), 0.0, 1e-10)

    # 3b. Exact null result: m = 0 is conformally invariant, so a lumpy (non-tanh) expansion makes nothing; the Born
    #     side agrees (rho0 = 0 for m = 0, and h = 2 eps f eta has X2 = 0).
    def lumpy(eta):
        return 1.0 + 0.5 * (1 + math.tanh(0.8 * eta)) + 0.3 * math.exp(-((eta - 1.0) / 0.7) ** 2)
    r0 = frw_dirac_production(kf, lumpy, 0.0, -20.0, 20.0)
    hconf = lambda t: 0.1 * np.exp(-t[:, None, None] ** 2) * _ETA   # noqa: E731
    htt_t = lambda t: 0.1 * np.exp(-t[:, None, None] ** 2) * np.diag([0.0, 1.0, -1.0, 0.0])   # noqa: E731
    bz = born_dirac_metric_homogeneous(hconf, -10.0, 10.0, 30.0, 0.0)["pairs_per_volume"]
    btt = born_dirac_metric_homogeneous(htt_t, -10.0, 10.0, 30.0, 0.0)["pairs_per_volume"]
    #     (roundoff: the exact solver's floor is ~1e-29 here; the conformal Born yield is a cancellation in X2,
    #     |.| < 1e-12 of the yield of a traceless h of the same amplitude)
    check("FRW null: m = 0 Dirac in a lumpy universe, exact max n_k < 1e-28; Born(conformal h) < 1e-12 Born(TT h)",
          float(r0["n"].max() < 1e-28 and abs(bz) < 1e-12 * btt), 1.0, 0)

    # 3c. Gravity-vertex Born (trace channel, rho0 = m^2 s beta^3/36pi) against the exact FRW solver (3a's reduction),
    #     a = 1 + eps f(eta), f = exp(-eta^2/2 tau^2), tau = 0.3, m = 1: h = 2 eps f eta at first order. Born is
    #     O(eps^2) exact; the next term is O(eps^3), so |exact/Born - 1| ~ eps: measured 0.63 eps. Bound 0.8 eps.
    tau_ = 0.3
    fg = lambda t: np.exp(-t ** 2 / (2 * tau_ ** 2))   # noqa: E731
    devs = []
    for eps in (0.05, 0.1):
        nk = lambda k, eps=eps: frw_dirac_production(k, lambda e: 1 + eps * float(fg(e)), 1.0, -12 * tau_, 12 * tau_,   # noqa: E731
                                                     rtol=1e-6)["n"]
        ex = qp.number_density_isotropic(nk, 12.0, n=48, g=2.0)

        def hfrw(t, eps=eps):
            return (2 * eps * fg(t))[:, None, None] * _ETA
        bo = born_dirac_metric_homogeneous(hfrw, -12 * tau_, 12 * tau_, 40.0, 1.0)
        devs.append(abs(ex / bo["pairs_per_volume"] - 1))
        check(f"FRW Dirac a = 1 + eps f, eps = {eps}: gravity-vertex Born (spin 0) vs exact modes, |dev| <= 0.8 eps",
              devs[-1], 0.0, 0.8 * eps)
    check("FRW Dirac: deviation scales with eps (ratio in [1.8, 2.2]); spin-2 part exactly 0",
          devs[1] / devs[0] + 10 * abs(bo["spin2_part"]) / bo["pairs_per_volume"], 2.0, 0.2)

    # 3d. Planar gravity vertex against a direct pair-momentum integral with explicit spinors and t^{mu nu}: a TT packet
    #     h_11 = -h_22 = g(K0, Kz) (lower index), N/A = int d^2p_perp dp1z dp2z/((2pi)^4 4E1E2) sum |(1/2) h_{mu nu} t^{mu nu}|^2.
    #     The azimuthal dependence is a trigonometric polynomial of degree 4, so 8 equally spaced angles are exact. m = 0.5.
    def gpl(K0, Kz):
        return PI * (np.exp(-(K0 - 3.0) ** 2 / 2) + np.exp(-(K0 + 3.0) ** 2 / 2)) * np.exp(-Kz * Kz / 2)

    def hpl(K0, Kz):
        out = np.zeros(np.shape(K0) + (4, 4), dtype=complex)
        out[..., 1, 1], out[..., 2, 2] = gpl(K0, Kz), -gpl(K0, Kz)
        return out
    bpl = born_dirac_metric_planar(hpl, 80.0, 5.0, 0.5, n_s=160, n_y=160)["pairs_per_area"]
    pt, wpt = qp._gauss_legendre(0, 6, 24)          # converged to 3e-8 (36 x 48 nodes on [0, 7]: same to 2e-8)
    pz, wpz = qp._gauss_legendre(-6, 6, 30)
    phs = np.arange(8) * 2 * PI / 8
    PT, PH, Z1, Z2 = np.meshgrid(pt, phs, pz, pz, indexing="ij")
    J, E1, E2 = _currents(np.stack([PT * np.cos(PH), PT * np.sin(PH), Z1], -1),
                          np.stack([-PT * np.cos(PH), -PT * np.sin(PH), Z2], -1), 0.5)
    q1, q2 = (2 * PT * np.cos(PH))[..., None, None], (2 * PT * np.sin(PH))[..., None, None]   # q = p1 - p2
    t11_22 = 0.5 * (J[..., 1, :, :] * q1 - J[..., 2, :, :] * q2)        # t^11 - t^22 = (1/4)(2 J^1 q^1 - 2 J^2 q^2)
    amp2 = 0.25 * np.abs(gpl(E1 + E2, Z1 + Z2)) ** 2 * np.sum(np.abs(t11_22) ** 2, axis=(-1, -2))
    direct = float(np.einsum("i,k,l,ijkl->", wpt * pt, wpz, wpz, amp2 / (4 * E1 * E2))) * (2 * PI / 8) / (2 * PI) ** 4
    check("Dirac planar gravity vertex = direct pair-momentum integral (explicit spinors, TT packet)", bpl, direct, 1e-6,
          rel=True)

    # 3e. Wiring (consistency, not a reference): general 4D Dirac = 1/2 x qp's photon for a TT spectrum (m = 0).
    def htt(K0, Kx, Ky, Kz):
        out = np.zeros(np.shape(K0) + (4, 4), dtype=complex)
        g = (2 * PI) ** 2 * np.exp(-(Kx * Kx + Ky * Ky + Kz * Kz) / 2) * np.exp(-(K0 - 3.0) ** 2 / 2)
        out[..., 1, 1], out[..., 2, 2] = g, -g
        return out
    gd = born_dirac_metric_general(htt, 60.0, 7.0, n_s=24, n_k=24, n_c=8, n_p=8)["pairs"]
    gp = qp.born_metric_general(htt, 60.0, 7.0, "photon", n_s=24, n_k=24, n_c=8, n_p=8)["pairs"]
    check("general 4D: massless Dirac pairs = 1/2 x photon pairs (spin 2 only)", gd / gp, 0.5, 1e-12, rel=True)

    passed = all(results)
    if verbose:
        print(f"\n{sum(results)}/{len(results)} checks passed")
    return passed


def _convergence() -> int:
    """Slow studies (not part of the self-test): Born vs exact for Sauter and Gaussian pulses; grid convergence."""
    print("Sauter pulse, m = 1: |exact/Born - 1| / (eE0 tau^2)^2 and R2 (Dirac, scalar)")
    for tau in (0.5, 1.0, 2.0, 3.0):
        for eE0 in (0.01, 0.02, 0.05):
            if (1 + 2 * tau * PI / math.sqrt(12.0)) * (2 * eE0 * tau * tau) ** 2 > 0.5:
                continue
            row = []
            for fld in ("dirac", "scalar"):
                ex = sauter_exact_pairs_per_volume(1.0, eE0, tau, fld, n_k=240, n_c=64)
                bo = sauter_born_pairs_per_volume(1.0, eE0, tau, fld)
                row.append(f"{fld}: {(ex / bo - 1) / (eE0 * tau * tau) ** 2:8.3f} (dev {ex / bo - 1:+.2e})")
            est = (1 + 2 * tau * PI / math.sqrt(12.0)) * (2 * eE0 * tau * tau) ** 2
            print(f"  tau = {tau}, eE0 = {eE0}, R2 = {2 * eE0 * tau * tau:.3f}, error estimate {est:.3g}: " + "; ".join(row))
    print("Gaussian pulse eE0 exp(-t^2/2tau^2), Dirac, m = 1: exact (qp two-level, 1024 modes) / Born, and R2")
    from math import erf
    kq, wq = qp._gauss_legendre(0, 8, 64)
    cq, wcq = np.polynomial.legendre.leggauss(16)
    KQ, CQ = np.meshgrid(kq, cq, indexing="ij")
    kzq, kpq = (KQ * CQ).ravel(), (KQ * np.sqrt(1 - CQ * CQ)).ravel()
    for tau, eE0 in ((0.5, 0.05), (1.0, 0.05), (1.5, 0.03), (2.0, 0.02), (3.0, 0.01)):
        sh = eE0 * tau * math.sqrt(PI / 2)
        rf = qp.bogoliubov_fermion_efield(lambda t: kzq + sh * erf(t / (math.sqrt(2) * tau)), np.sqrt(1 + kpq ** 2),
                                          -14 * tau, 14 * tau, rtol=1e-5)
        ex = 2 * float(np.einsum("i,j,ij->", wq * kq * kq, wcq, rf["n"].reshape(KQ.shape))) / (4 * PI * PI)
        bo = born_qed_homogeneous(lambda t: eE0 * np.exp(-t * t / (2 * tau * tau)), -14 * tau, 14 * tau, 1.0, 40.0,
                                  check=False)
        print(f"  m tau = {tau}, eE0 = {eE0}: exact/Born = {ex / bo['pairs_per_volume']:.4g}, R2 = {bo['R2']:.3g}, "
              f"error estimate {bo['error_estimate']:.3g}, kick = {bo['kick']:.3g}")
    print("sauter_exact_pairs_per_volume grid convergence (eE0 = 0.05, tau = 1): n_k, n_c")
    ref = None
    for nk_, nc_ in ((80, 24), (160, 48), (320, 96)):
        v = sauter_exact_pairs_per_volume(1.0, 0.05, 1.0, "scalar", n_k=nk_, n_c=nc_)
        ref = ref or v
        print(f"  {nk_} x {nc_}: {v:.12g} (rel. change {v / ref - 1:+.2e}); qp.sauter_pairs_per_volume(n=96): "
              f"{qp.sauter_pairs_per_volume(1.0, 0.05, 1.0, False):.6g}")
    return 0


# ---------------------------------------------------------------- command line
def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("selftest")
    sub.add_parser("convergence", help="slow: Born vs exact scaling for Sauter and Gaussian pulses, grid convergence")
    sp = sub.add_parser("spectral", help="rhoV, Im Pi and Dirac (rho2, rho0) at one pair energy sqrt(s)")
    sp.add_argument("--sqrts", required=True, help="pair invariant mass, e.g. '1.5 MeV' or a number in your unit")
    sp.add_argument("--m", default="0.51099895 MeV", help="fermion mass (default: electron)")
    pp = sub.add_parser("sauter", help="Sauter pulse E0 sech^2(t/tau): Born vs exact e+e- pairs per volume")
    pp.add_argument("--E", required=True, help="peak field, e.g. '1e16 V/m'")
    pp.add_argument("--tau", required=True, help="pulse time scale, e.g. '1e-21 s'")
    pp.add_argument("--m", default="0.51099895 MeV")
    pp.add_argument("--scalar", action="store_true", help="scalar QED instead of spinor QED")
    fp = sub.add_parser("frw", help="Dirac field in a(eta) = A + B tanh(rho eta): exact solver vs closed form, one k")
    for name in ("m", "rho", "k"):
        fp.add_argument(f"--{name}", required=True, help="energy: a number in your natural unit, or e.g. '1 eV'")
    fp.add_argument("--A", type=float, required=True)
    fp.add_argument("--B", type=float, required=True)
    args = ap.parse_args(argv)
    try:
        if args.cmd == "selftest":
            return 0 if selftest() else 1
        if args.cmd == "convergence":
            return _convergence()
        if args.cmd == "spectral":
            m, rs = qp._energy(args.m), qp._energy(args.sqrts)
            s = rs * rs
            rd, rsc = vector_spectral_density([s], m)[0], vector_spectral_density([s], m, "scalar")[0]
            r2, r0 = dirac_stress_spectral_densities([s], m)
            print(f"sqrt(s) = {rs:.6g}, m = {m:.6g} (same unit), s/4m^2 = {s / (4 * m * m) if m > 0 else float('inf'):.6g}")
            print(f"QED (charge-stripped, spin-summed, per e+e- pair state): rhoV Dirac = {rd:.6g}, scalar = {rsc:.6g}")
            print(f"Im Pi (alpha = {ALPHA:.10g}): Dirac {im_vacuum_polarization([s], m)[0]:.6g}, scalar "
                  f"{im_vacuum_polarization([s], m, 'scalar')[0]:.6g}")
            print(f"gravity vertex, Dirac pairs: rho2 = {r2[0]:.6g}, rho0 = {r0[0]:.6g} (energy^4, e.g. eV^4); "
                  f"rho2/rho2(m=0) = {r2[0] / (s * s / (80 * PI)):.6g}")
            return 0
        if args.cmd == "frw":
            m, rho, k = qp._energy(args.m), qp._energy(args.rho), qp._energy(args.k)
            ref = float(frw_dirac_tanh_n([k], m, args.A, args.B, rho)[0])
            r = frw_dirac_production([k], lambda e: args.A + args.B * math.tanh(rho * e), m, -25 / rho, 25 / rho)
            print(f"a(eta) = {args.A} + {args.B} tanh({rho:.6g} eta), m = {m:.6g}, comoving k = {k:.6g}")
            print(f"n_k per helicity (mean electrons = positrons = pairs in the comoving mode, in-in): solver {r['n'][0]:.10g}, "
                  f"closed form {ref:.10g}; precision floor {r['floor'][0]:.2g}")
            return 0
        from unit_tools import Q
        m = qp._energy(args.m)
        eE = qp.eE_from_field_SI(Q(args.E).expect("V/m").si)
        tau = qp.time_to_inverse_eV(Q(args.tau).expect("time").si)
        fld = "scalar" if args.scalar else "dirac"
        print(f"{fld}, m = {m:.6g} eV, eE0 = {eE:.6g} eV^2 = {eE / m ** 2:.4g} m^2, tau = {tau:.6g} /eV, m tau = {m * tau:.4g}, "
              f"R2 = 2 eE0 tau^2 = {2 * eE * tau * tau:.3g}, gamma = m/(eE0 tau) = {m / (eE * tau):.4g}")
        ex = sauter_exact_pairs_per_volume(m, eE, tau, fld)
        print(f"exact (Gavrilov-Gitman, all orders): {ex:.6g} eV^3 = {qp.density_to_SI(ex):.6g} e+e- pairs per m^3")
        try:
            bo = sauter_born_pairs_per_volume(m, eE, tau, fld)
        except ValueError as exc:
            print(f"Born (first order): not applicable here -- {exc}")
            return 0
        print(f"Born (first order, in-in):           {bo:.6g} eV^3 = {qp.density_to_SI(bo):.6g} pairs per m^3 "
              f"(exact/Born = {ex / bo:.6g})")
    except (ValueError, KeyError) as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
