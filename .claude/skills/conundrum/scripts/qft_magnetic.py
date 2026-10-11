#!/usr/bin/env python3
"""qft_magnetic: pair production with a magnetic field present (Landau levels, constant fields of any
orientation, and a time-dependent E(t) along a constant B), with every function saying exactly WHICH
quantity it returns (numpy + mpmath, no scipy). Companion of qft_production.py, which it imports for
its mode solvers, Sauter closed forms, Schwinger closed forms, quadrature and unit helpers.

Why this tool exists
    A magnetic field changes pair production in ways that are easy to get backwards. It quantises
    the transverse motion into Landau levels: a scalar's lowest level is lifted to m^2 + eB, so B
    SUPPRESSES scalar pair production exponentially; a Dirac particle's spin coupling cancels the
    zero-point term for one spin state, so the lowest spinor level stays at m^2, the Landau degeneracy
    eB/(2 pi) per unit area multiplies it, and B ENHANCES spinor pair production linearly. The usual
    traps also apply: in-in (mean pair number) versus in-out (vacuum persistence); the pair-number
    rate versus the vacuum-decay rate 2 Im L (they differ, and for massless fermions in E || B the
    first is finite and the second infinite); particles versus pairs; and real production versus
    configurations that make nothing (pure magnetic, crossed fields with |E| <= |B|, null fields).
    Every public function's docstring has a "Quantity:" line and a "Valid when:" line, and inputs
    outside that range are refused with ValueError.

Units (read this first)
    Natural units hbar = c = 1, Heaviside-Lorentz electromagnetism (e^2 = 4 pi alpha), exactly as
    qft_production.py. Pick ONE energy unit (e.g. eV, or units of the mass m) and give every energy,
    mass and momentum in it; fields enter as eE and eB in energy^2 (charge times field; in natural
    units B/E = c B_SI / E_SI), times in 1/energy, numbers per volume in energy^3, rates per volume in
    energy^4. This deviates from schemas.md's "SI in the Python API" on purpose (precedent:
    qft_production.py, page_wootters.py): SI helpers convert (eB_from_field_SI, field_E_to_SI,
    field_B_to_SI, landau_degeneracy_SI, and qft_production's eE_from_field_SI, rate_density_to_SI,
    density_to_SI, time_to_inverse_eV), and the command line accepts units through unit_tools.Q
    ("1e18 V/m", "1e9 T", "1e13 gauss", "0.511 MeV", "1e-20 s"; note "G" is Newton's constant there).

PART A. Constant parallel E and B along z: Landau levels
--------------------------------------------------------
    Gauge A = (0, B x, A_z(t)); kinetic momentum along z p(t) = k_par - e A_z(t), dp/dt = eE.
    Transverse motion: pi_perp^2 = p_x^2 + (k_y - eB x)^2 has eigenvalues (2n + 1) eB, n = 0, 1, ...,
    each with eB/(2 pi) states (orbit centres x0 = k_y/eB) per unit transverse area.
    * Scalar QED: eps_perp^2 = m^2 + (2n + 1) eB, one channel per orbit centre.
    * Spinor QED (g = 2): the transverse Dirac operator M = alpha_x pi_x + alpha_y pi_y + beta m obeys
          M^2 = m^2 + pi_perp^2 - eB Sigma_z,   {alpha_z, M} = 0,   [alpha_z, M^2] = 0,
      so eps_perp^2 = m^2 + (2n + 1 - s) eB, s = +1 / -1 the spin along eB (Dunne's lambda-/lambda+,
      Tanji's up/down). Grouped by eps_perp^2 = m^2 + 2 j eB: j = 0 has ONE channel (n = 0, s = +1;
      the lowest level is spin non-degenerate), every j >= 1 has TWO ((j, +1) and (j - 1, -1)).
      Because H = alpha_z p(t) + M with alpha_z and M anticommuting, each M^2 eigenspace is a set of
      copies of qft_production's two-level problem i dc/dt = (p(t) sigma_z + eps_perp sigma_x) c, for
      ANY E(t) parallel to a constant B. The self-test checks this without assuming it: it builds the
      4-component transverse Dirac operator on a Fourier grid, diagonalises it, and evolves each
      Landau block through a Sauter pulse.
    * Constant E: per mode (one orbit centre, one channel, one k_par crossing)
          n = exp(-pi eps_perp^2 / eE)                (Landau-Zener; Tanji 2009 eqs. 2.49, 2.71)
      Modes per unit volume per unit time: eE/(2 pi) (k_par crossings) x eB/(2 pi) (orbit centres).
      From the SAME n (g_j = channels of level j):
          pair-number rate  Gamma = eE eB/(4 pi^2) sum_j g_j n_j                    (in-in mean number)
          vacuum decay      w     = eE eB/(4 pi^2) sum_j g_j [-ln(1 - n_j)]  spinor   (in-out: the
                            w     = eE eB/(4 pi^2) sum_j     [+ln(1 + n_j)]  scalar    vacuum survives
                                                                                       with exp(-w V T))
      Closed forms (Kim & Page 2006 eqs. 1-4; Dunne 2004 eqs. 1.28, 1.40, which credit Nikishov, Bunkin & Tugov, Popov):
          spinor  Gamma = (e^2 E B/(4 pi^2)) coth(pi B/E) exp(-pi m^2/(eE))
                  w     = (e^2 E B/(4 pi^2)) sum_n (1/n) coth(n pi B/E) exp(-n pi m^2/(eE))
          scalar  Gamma = (e^2 E B/(8 pi^2)) csch(pi B/E) exp(-pi m^2/(eE))
                  w     = (e^2 E B/(8 pi^2)) sum_n ((-1)^(n+1)/n) csch(n pi B/E) exp(-n pi m^2/(eE))
      w = 2 Im L_eff (Im L_eff alone is w/2); Gamma is only the n = 1 term of the w series.
      Limits: B -> 0 gives Schwinger (qft_production.schwinger_closed_forms), with relative corrections
      (pi B/E)^2/3 (spinor) and -(pi B/E)^2/6 (scalar) in Gamma. Strong B (B >> E): only the lowest level
      survives; spinor Gamma -> (e^2 E B/(4 pi^2)) e^{-pi m^2/eE} and w -> -(e^2 E B/(4 pi^2)) ln(1 - e^{-pi m^2/eE})
      (1+1-dimensional Schwinger times eB/(2 pi): grows linearly with B); scalar Gamma ->
      (e^2 E B/(4 pi^2)) e^{-pi (m^2 + eB)/eE} (exponentially suppressed).
      Massless spinor with B > 0: the lowest level has n = 1 exactly, so Gamma is finite but w is
      infinite (vacuum persistence exactly zero); with B = 0 both are finite.
    Particles versus pairs: for a charged field n counts particles in the mode = antiparticles in the
    partner mode = pairs. NO factor 1/2 anywhere in this module (the pair members are not identical).

PART B. General constant fields: invariants and the parallel frame
--------------------------------------------------------------------
    eps^2 - eta^2 = E^2 - B^2,  eps eta = |E.B|,  eps, eta >= 0  (Dunne eqs. 1.4-1.6, a = eps, b = eta):
    the field strengths in a frame where E and B are parallel. That frame is reached by a boost along
    E x B with speed v, v/(1 + v^2) = |E x B|/(E^2 + B^2); it exists unless the field is null
    (E^2 = B^2 and E.B = 0, where v -> 1).
    Both rates are numbers per unit 4-volume: w through the in-out vacuum persistence exp(-w V T), a
    Lorentz scalar over the invariant 4-volume V T; Gamma counts pairs (a frame-independent number) per
    4-volume. So in ANY frame the rates equal the parallel-frame rates with eE -> e eps, eB -> e eta
    (Kim & Page 2006, before eq. 1). The momentum distribution of the pairs is NOT invariant.
    eps = 0 (pure B; crossed E perpendicular to B with |E| <= |B|; null fields): no pair production at
    all, Gamma = w = 0 (Dunne p. 12). eta = 0, eps > 0 (e.g. crossed with |E| > |B|): Schwinger with
    E -> eps = sqrt(E^2 - B^2).

PART C. Time-dependent E(t) along a constant B
----------------------------------------------
    Per Landau channel the B = 0 mode problems of qft_production apply with k_perp^2 replaced by
    eps_perp^2 - m^2 (Tanji 2009, "the same form as ... the pure electric field case ... with the
    replacement m^2 + zeta_n -> m^2 + p_T^2"):
      scalar:  u'' + (eps_perp^2 + p(t)^2) u = 0          -> qft_production.bogoliubov_boson
      spinor:  i dc/dt = (p sigma_z + eps_perp sigma_x) c  -> qft_production.bogoliubov_fermion_efield
      Sauter pulse E0 sech^2(t/tau): Gavrilov & Gitman 1996 eqs. 42-43 (qft_production.sauter_n_*)
      with k_perp = sqrt(eps_perp^2 - m^2).
    Total pairs per volume: N/V = eB/(2 pi) sum_j g_j int dk_par/(2 pi) n_j(k_par); the locally-constant-
    field estimate is int dt Gamma(E(t), B) with the coth/csch pair rate.

Assumptions and validity range
    One loop: free charged fields in prescribed classical fields (no back-reaction, no radiative
    corrections, no photon-assisted processes such as one-photon pair creation in strong B). Constant
    fields filling a region much larger than the formation length eps_perp/eE and lasting much longer
    than eps_perp/eE. In Part C, B is constant and parallel to E(t) (a time-dependent or non-parallel
    B is NOT covered), and particle numbers are read only after E has switched off (at intermediate
    times the "number" is basis dependent: transient vacuum polarisation).

Python usage
    import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
    import numpy as np, qft_magnetic as qm
    qm.landau_spectrum(m=1.0, eB=0.5, fermion=True, n_levels=4)      # eps_perp^2, channels, eB/(2pi)
    qm.parallel_n_mode(0, 1.0, eE=0.5, eB=0.5, fermion=True, spin=+1) # per-mode occupation
    qm.parallel_rates_from_modes(1.0, 0.5, 0.5, fermion=True)        # Gamma and w from Landau sums
    qm.parallel_closed_forms(1.0, 0.5, 0.5, fermion=True)            # Kim & Page eqs. 1-4
    qm.general_rates([0.3, 0.0, 0.4], [0.0, 0.5, 0.2], m=1.0, fermion=True)   # any constant field
    qm.landau_sauter_pairs_per_volume(1.0, eE0=0.5, tau=2.0, eB=0.25, fermion=True)

Command line (from the project root)
    python3 .claude/skills/conundrum/scripts/qft_magnetic.py selftest
    python3 .claude/skills/conundrum/scripts/qft_magnetic.py parallel --E "1e18 V/m" --B "1e9 T"
    python3 .claude/skills/conundrum/scripts/qft_magnetic.py parallel --E "1e18 V/m" --B "1e9 T" --scalar
    python3 .claude/skills/conundrum/scripts/qft_magnetic.py general --E "1e18 V/m" --B "4e9 T" --angle 80
    python3 .claude/skills/conundrum/scripts/qft_magnetic.py sauter --E "1e18 V/m" --B "1e9 T" --tau "1e-20 s"
    python3 .claude/skills/conundrum/scripts/qft_magnetic.py convergence     (slower: grids, steps, limits)
"""
from __future__ import annotations

import functools
import math
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (_HERE, ".claude/skills/conundrum/scripts"):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import qft_production as qp  # noqa: E402
from unit_tools import C, E_CHARGE, HBAR  # noqa: E402  (CODATA values shared by the toolkit)

PI = math.pi
_SQRT3 = math.sqrt(3.0)
_G1, _G2 = 0.5 - _SQRT3 / 6.0, 0.5 + _SQRT3 / 6.0     # Gauss-Legendre nodes on [0, 1] (4th-order Magnus)


# ---------------------------------------------------------------- SI helpers
def eB_from_field_SI(B_tesla: float) -> float:
    """Natural-unit magnetic field strength eB in eV^2 from B in tesla: eB = |B| hbar c^2 / e.

    Quantity: eB in eV^2 (eB = m^2 at the critical field B_c = m^2 c^2/(e hbar) = 4.414e9 T for electrons).
    Valid when: B_tesla is a magnetic flux density in T (any sign; the magnitude is returned)."""
    return abs(float(B_tesla)) * HBAR * C * C / E_CHARGE


def field_B_to_SI(eB_eV2: float) -> float:
    """Inverse of eB_from_field_SI: B in tesla from eB in eV^2 (charge e = elementary charge).

    Quantity: magnetic flux density in T.
    Valid when: eB_eV2 is eB in eV^2 for the elementary charge."""
    return float(eB_eV2) * E_CHARGE / (HBAR * C * C)


def field_E_to_SI(eE_eV2: float) -> float:
    """Inverse of qft_production.eE_from_field_SI: E in V/m from eE in eV^2 (charge e = elementary charge).

    Quantity: electric field strength in V/m.
    Valid when: eE_eV2 is eE in eV^2 for the elementary charge."""
    return float(eE_eV2) * E_CHARGE / (HBAR * C)


def landau_degeneracy_SI(B_tesla: float) -> float:
    """Landau degeneracy per unit transverse area in SI: |e B|/(2 pi hbar) (elementary charge).

    Quantity: number of states (orbit centres) per Landau level and channel per unit area, in m^-2.
    Valid when: B_tesla is a magnetic flux density in T and the particle has charge +-e."""
    return abs(float(B_tesla)) * E_CHARGE / (2 * PI * HBAR)


# ---------------------------------------------------------------- input checks
def _num(x, name: str) -> float:
    try:
        v = float(x)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be a real number") from None
    if not math.isfinite(v):
        raise ValueError(f"{name} must be finite")
    return v


def _pos(x, name: str) -> float:
    v = _num(x, name)
    if v <= 0:
        raise ValueError(f"{name} must be > 0")
    return v


def _nonneg(x, name: str) -> float:
    v = _num(x, name)
    if v < 0:
        raise ValueError(f"{name} must be >= 0")
    return v


def _vec3(v, name: str) -> np.ndarray:
    a = np.asarray(v, dtype=float)
    if a.shape != (3,) or not np.all(np.isfinite(a)):
        raise ValueError(f"{name} must be a finite 3-vector")
    return a


@functools.lru_cache(maxsize=32)
def _leggauss(n: int):
    """Gauss-Legendre nodes/weights on [-1, 1], cached: numpy's leggauss diagonalises an n x n matrix,
    which can take seconds for n >= 400 when OpenBLAS threads compete on a shared machine."""
    return np.polynomial.legendre.leggauss(n)


def _composite_gl(a: float, b: float, panels: int, nodes: int):
    x0, w0 = _leggauss(nodes)
    edges = np.linspace(a, b, panels + 1)
    half = 0.5 * np.diff(edges)
    mid = 0.5 * (edges[1:] + edges[:-1])
    return (mid[:, None] + half[:, None] * x0[None]).ravel(), (half[:, None] * w0[None]).ravel()


def _gl(a: float, b: float, n: int):
    x0, w0 = _leggauss(n)
    return 0.5 * (b - a) * x0 + 0.5 * (b + a), 0.5 * (b - a) * w0


# ---------------------------------------------------------------- Part A: Landau levels
def _level_eps2(n, m: float, eB: float, fermion: bool, spin):
    n = np.asarray(n)
    if not np.issubdtype(n.dtype, np.integer):
        if not np.all(np.isfinite(n.astype(float))) or np.any(n.astype(float) != np.round(n.astype(float))):
            raise ValueError("Landau level n must be an integer >= 0")
        n = np.round(n.astype(float)).astype(int)
    if np.any(n < 0):
        raise ValueError("Landau level n must be an integer >= 0")
    if fermion:
        if spin not in (1, -1):
            raise ValueError("spinor QED needs spin = +1 (eps^2 = m^2 + 2n eB) or -1 (m^2 + (2n+2) eB)")
        return m * m + (2 * n + 1 - spin) * eB
    if spin not in (None, 0):
        raise ValueError("scalar QED has no spin label: pass spin=None")
    return m * m + (2 * n + 1) * eB


def landau_eps_perp2(n, m: float, eB: float, fermion: bool, spin=None):
    """Transverse energy squared eps_perp^2 of Landau level n (and spin s for spinors) in a field eB along z.

    scalar: m^2 + (2n + 1) eB;  spinor (g = 2): m^2 + (2n + 1 - s) eB, s = +1 / -1 (spin along eB).
    Quantity: eps_perp^2 in energy^2 (the "transverse mass squared" that replaces m^2 + k_perp^2 of B = 0),
        per orbital level n (array allowed) and spin state.
    Valid when: constant B (eB > 0, energy^2), m >= 0, n integer >= 0; spin = +-1 for spinors, None for scalars."""
    m, eB = _nonneg(m, "m"), _pos(eB, "eB")
    return _level_eps2(n, m, eB, fermion, spin)


def landau_degeneracy_per_area(eB: float) -> float:
    """Landau degeneracy eB/(2 pi): orbit centres per Landau level (per channel) per unit transverse area.

    Quantity: number of states per unit area in energy^2 (natural units; landau_degeneracy_SI gives m^-2).
    Valid when: constant uniform B, eB > 0 (energy^2), sample area >> 2 pi/eB."""
    return _pos(eB, "eB") / (2 * PI)


def landau_spectrum(m: float, eB: float, fermion: bool, n_levels: int) -> dict:
    """Landau levels grouped by transverse energy: eps_perp^2, number of pair channels, degeneracy.

    scalar: level j has eps_perp^2 = m^2 + (2j + 1) eB, 1 channel.
    spinor: level j has eps_perp^2 = m^2 + 2 j eB, 1 channel at j = 0 (spin non-degenerate lowest level),
            2 channels (orbital j with s = +1, orbital j - 1 with s = -1) for j >= 1.
    Quantity: dict with 'level' (j), 'eps_perp2' (energy^2), 'channels' (pair channels per orbit centre:
        states that each carry an independent per-mode occupation), 'degeneracy_per_area' = eB/(2 pi)
        (energy^2), and 'spin_content' (list of (orbital n, spin) per level, first 64 levels only; spin None
        for scalars).
    Valid when: constant uniform B (eB > 0), m >= 0, 1 <= n_levels <= 10^7."""
    m, eB = _nonneg(m, "m"), _pos(eB, "eB")
    if not (isinstance(n_levels, (int, np.integer)) and 1 <= n_levels <= 10 ** 7):
        raise ValueError("n_levels must be an integer between 1 and 1e7")
    j = np.arange(n_levels)
    if fermion:
        eps2 = m * m + 2 * j * eB
        ch = np.where(j == 0, 1, 2)
        spin = [[(0, +1)]] + [[(int(k), +1), (int(k) - 1, -1)] for k in j[1:min(n_levels, 64)]]
    else:
        eps2 = m * m + (2 * j + 1) * eB
        ch = np.ones(n_levels, dtype=int)
        spin = [[(int(k), None)] for k in j[:min(n_levels, 64)]]
    return {"level": j, "eps_perp2": eps2, "channels": ch, "degeneracy_per_area": eB / (2 * PI),
            "spin_content": spin}


def parallel_n_mode(n, m: float, eE: float, eB: float, fermion: bool, spin=None):
    """Constant parallel E and B: per-mode occupation n = exp(-pi eps_perp^2/(eE)) of Landau level n, spin s.

    Tanji 2009 eqs. 2.49 (scalar) and 2.70-2.71 (spinor); eps_perp^2 from landau_eps_perp2.
    Quantity: per-mode IN-IN mean number of particles (= antiparticles = pairs; no 1/2) in ONE mode:
        one orbit centre, one spin state, one k_par crossing; dimensionless, not a rate.
    Valid when: E and B constant and parallel (eE > 0, eB > 0, energy^2) for a time >> eps_perp/eE around
        the crossing; m >= 0; n integer >= 0; spin = +-1 for spinors, None for scalars. A massless spinor's
        lowest level (n = 0, s = +1) has n = 1 exactly."""
    m, eE, eB = _nonneg(m, "m"), _pos(eE, "eE"), _pos(eB, "eB")
    return np.exp(-PI * _level_eps2(n, m, eB, fermion, spin) / eE)


def _levels_needed(eE: float, eB: float, rtol: float) -> int:
    # n_j / n_0 = exp(-2 pi j eB/eE) < rtol  ->  j > ln(1/rtol) eE/(2 pi eB)
    return int(math.ceil(math.log(1.0 / rtol) * eE / (2 * PI * eB))) + 2


def parallel_rates_from_modes(m: float, eE: float, eB: float, fermion: bool, rtol: float = 1e-17,
                              max_levels: int = 2_000_000) -> dict:
    """Pair-number rate AND vacuum-decay rate per volume for constant parallel E, B, by explicit Landau sums.

    Both from the same per-mode occupation n_j = exp(-pi eps_perp,j^2/eE) and channel counts g_j:
        Gamma = eE eB/(4 pi^2) sum_j g_j n_j,   w = eE eB/(4 pi^2) sum_j g_j [-ln(1 - n_j)] (spinor),
        w = eE eB/(4 pi^2) sum_j [ln(1 + n_j)] (scalar). Levels are summed until n_j/n_0 < rtol.
    Quantity: dict with 'pair_rate' Gamma (IN-IN mean number of PAIRS per unit volume per unit time,
        energy^4), 'decay_rate' w (vacuum decay: the IN-OUT persistence |<0out|0in>|^2 = exp(-w V T);
        w = 2 Im L_eff; energy^4; float('inf') for a massless spinor, whose lowest level has n = 1),
        'ratio' = w/Gamma, 'lll_pair_rate', 'lll_decay_rate' and 'lll_fraction' (lowest Landau level
        alone), 'levels' (number summed).
    Valid when: E, B constant and parallel (eE > 0, eB > 0, energy^2), m >= 0, one loop; the number of levels
        ~ 6 eE/eB must not exceed max_levels (for B/E -> 0 use qft_production.rates_from_modes)."""
    m, eE, eB = _nonneg(m, "m"), _pos(eE, "eE"), _pos(eB, "eB")
    if not (0 < rtol < 1e-3):
        raise ValueError("need 0 < rtol < 1e-3")
    J = _levels_needed(eE, eB, rtol)
    if J > max_levels:
        raise ValueError(f"B/E = {eB / eE:.3g} needs {J} Landau levels (> max_levels = {max_levels}); "
                         "use parallel_closed_forms, or qft_production.rates_from_modes for B -> 0")
    sp = landau_spectrum(m, eB, fermion, J)
    g = sp["channels"].astype(float)
    n = np.exp(-PI * sp["eps_perp2"] / eE)
    pref = eE * eB / (4 * PI * PI)
    with np.errstate(divide="ignore"):
        per = -np.log1p(-n) if fermion else np.log1p(n)
    pair = pref * float(np.sum(g * n))
    decay = pref * float(np.sum(g * per))
    lll_pair, lll_decay = float(pref * g[0] * n[0]), float(pref * g[0] * per[0])
    return {"pair_rate": pair, "decay_rate": decay, "ratio": decay / pair if pair > 0 else float("nan"),
            "lll_pair_rate": lll_pair, "lll_decay_rate": lll_decay,
            "lll_fraction": lll_pair / pair if pair > 0 else float("nan"), "levels": J}


def parallel_closed_forms(m: float, eE: float, eB: float, fermion: bool, rtol: float = 1e-17,
                          max_terms: int = 2_000_000) -> dict:
    """Published closed forms for constant parallel E and B (Kim & Page 2006 eqs. 1-4; Dunne 2004 eqs. 1.28, 1.40).

    spinor: Gamma = eE eB/(4 pi^2) coth(pi B/E) e^{-pi m^2/eE},  w = eE eB/(4 pi^2) sum (1/n) coth(n pi B/E) e^{-n pi m^2/eE}
    scalar: Gamma = eE eB/(8 pi^2) csch(pi B/E) e^{-pi m^2/eE},  w = eE eB/(8 pi^2) sum ((-1)^(n+1)/n) csch(n pi B/E) e^{-n pi m^2/eE}
    (B/E = eB/eE). The w series is summed term by term (NOT through the Landau sum) until the terms fall
    below rtol. eB = 0 gives Schwinger's forms (mpmath polylog Li_2, m = 0 allowed).
    Quantity: dict with 'pair_rate' Gamma (IN-IN mean number of PAIRS per unit volume per unit time) and
        'decay_rate' w = 2 Im L_eff (IN-OUT vacuum decay rate per unit volume), both energy^4,
        'im_L_eff' = w/2, 'ratio' = w/Gamma, 'terms' summed. w = inf for a massless spinor with eB > 0.
    Valid when: E, B constant and parallel, eE > 0, eB >= 0 (energy^2), m >= 0, one loop; the series needs
        about ln(1/rtol)/(pi m^2/eE) terms (<= max_terms; very strong E with tiny m is refused)."""
    m, eE, eB = _nonneg(m, "m"), _pos(eE, "eE"), _nonneg(eB, "eB")
    if not (0 < rtol < 1e-3):
        raise ValueError("need 0 < rtol < 1e-3")
    a = PI * m * m / eE
    if eB == 0.0:
        import mpmath as mp
        x = mp.e ** (-a)
        pref = eE * eE / (4 * PI ** 3) if fermion else eE * eE / (8 * PI ** 3)
        li = mp.polylog(2, x) if fermion else -mp.polylog(2, -x)
        w = float(pref * li)
        return {"pair_rate": float(pref * x), "decay_rate": w, "im_L_eff": w / 2, "ratio": float(li / x), "terms": 0}
    y = PI * eB / eE
    if fermion:
        pref = eE * eB / (4 * PI * PI)
        pair = pref * math.exp(-a) / math.tanh(y)
        if a == 0.0:
            return {"pair_rate": pair, "decay_rate": float("inf"), "im_L_eff": float("inf"), "ratio": float("inf"),
                    "terms": 0}
        N = int(math.ceil(math.log(1.0 / rtol) / a)) + 2
    else:
        pref = eE * eB / (8 * PI * PI)
        pair = pref * 2.0 * math.exp(-a - y) / (-math.expm1(-2.0 * y))
        N = int(math.ceil(math.log(1.0 / rtol) / (a + y))) + 2
    if N > max_terms:
        raise ValueError(f"the closed-form series needs {N} terms (> max_terms = {max_terms}); "
                         "use parallel_rates_from_modes (the Landau sum converges in ~6 eE/eB levels)")
    k = np.arange(1, N + 1, dtype=float)
    if fermion:
        terms = np.exp(-k * a) / (k * np.tanh(k * y))
    else:
        terms = np.where(k % 2 == 1, 1.0, -1.0) * 2.0 * np.exp(-k * (a + y)) / (k * (-np.expm1(-2.0 * k * y)))
    w = pref * float(np.sum(terms[::-1]))                 # smallest terms first
    return {"pair_rate": pair, "decay_rate": w, "im_L_eff": w / 2, "ratio": w / pair if pair > 0 else float("nan"),
            "terms": N}


def _pair_rate_closed_vec(m: float, eE: np.ndarray, eB: float, fermion: bool) -> np.ndarray:
    """Vectorised constant-field pair rate (Kim & Page eqs. 3-4; eB = 0: Schwinger), used for the LCFA."""
    eE = np.asarray(eE, dtype=float)
    out = np.zeros_like(eE)
    on = eE > 0
    e = eE[on]
    a = PI * m * m / e
    if eB == 0.0:
        out[on] = e * e / (4 * PI ** 3 if fermion else 8 * PI ** 3) * np.exp(-a)
        return out
    y = PI * eB / e
    if fermion:
        out[on] = e * eB / (4 * PI * PI) * np.exp(-a) / np.tanh(y)
    else:
        out[on] = e * eB / (8 * PI * PI) * 2.0 * np.exp(-a - y) / (-np.expm1(-2.0 * y))
    return out


# ---------------------------------------------------------------- Part B: invariants, any constant field
def field_invariants(eE_vec, eB_vec) -> dict:
    """Lorentz invariants of a constant field and the boost to the frame where E and B are parallel.

    eps^2 - eta^2 = E^2 - B^2, eps eta = |E.B| (Dunne 2004 eqs. 1.4-1.6 with a = eps, b = eta); boost
    velocity v along E x B with v/(1 + v^2) = |E x B|/(E^2 + B^2).
    Quantity: dict with 'eps' and 'eta' (e x field strength in the parallel frame, energy^2, >= 0),
        'E2_minus_B2' and 'E_dot_B' (the invariants, energy^4), 'boost_velocity' (3-vector, units of c;
        None for a null or zero field), and 'kind': 'parallel-frame', 'electric' (E.B = 0, E^2 > B^2:
        pure E after the boost), 'magnetic' (E.B = 0, B^2 > E^2: pure B), 'null' or 'zero'.
    Valid when: constant homogeneous fields; eE_vec, eB_vec are finite 3-vectors (energy^2) in one frame;
        |E.B| <= 1e-14 (E^2 + B^2) is treated as E.B = 0 (it is below the roundoff of the components)."""
    E, B = _vec3(eE_vec, "eE_vec"), _vec3(eB_vec, "eB_vec")
    E2, B2, G = float(E @ E), float(B @ B), float(E @ B)
    S = E2 + B2
    if S == 0.0:
        return {"eps": 0.0, "eta": 0.0, "E2_minus_B2": 0.0, "E_dot_B": 0.0, "boost_velocity": None, "kind": "zero"}
    if abs(G) <= 1e-14 * S:          # below the roundoff of the components (e.g. cos(90 deg) = 6e-17): E.B = 0
        G = 0.0
    F = 0.5 * (E2 - B2)
    root = math.hypot(F, G)
    if F >= 0:
        eps = math.sqrt(root + F)
        eta = abs(G) / eps if eps > 0 else 0.0
    else:
        eta = math.sqrt(root - F)
        eps = abs(G) / eta if eta > 0 else 0.0
    # Speed from v/(1 + v^2) = s = |E x B|/S. Since 1 - 4 s^2 = 4 (F^2 + G^2)/S^2, the root
    # v = 2 s/(1 + sqrt(1 - 4 s^2)) = 2 |E x B|/(S + 2 sqrt(F^2 + G^2)) has no cancellation near null fields
    # (the textbook form loses all digits there and can return v = 1 + 2e-16).
    v = np.cross(E, B) * (2.0 / (S + 2.0 * root))
    null = (G == 0.0 and abs(E2 - B2) <= 1e-14 * S) or float(np.linalg.norm(v)) >= 1.0
    if null:
        v, kind = None, "null"
        eps = eta = 0.0
    else:
        kind = "parallel-frame" if G != 0.0 else ("electric" if E2 > B2 else "magnetic")
    return {"eps": eps, "eta": eta, "E2_minus_B2": E2 - B2, "E_dot_B": G, "boost_velocity": v, "kind": kind}


def boost_fields(eE_vec, eB_vec, v_vec):
    """Fields seen in a frame moving with velocity v (units of c) relative to the frame of (E, B).

    E' = gamma (E + v x B) - gamma^2/(gamma + 1) (v.E) v,   B' = gamma (B - v x E) - gamma^2/(gamma + 1) (v.B) v
    (natural units, Heaviside-Lorentz; the standard field transformation, checked in the self-test against an
    explicit tensor boost Lambda F Lambda^T).
    Quantity: tuple (eE', eB') of 3-vectors in the same units as the input (energy^2).
    Valid when: |v| < 1; finite 3-vectors."""
    E, B, v = _vec3(eE_vec, "eE_vec"), _vec3(eB_vec, "eB_vec"), _vec3(v_vec, "v_vec")
    v2 = float(v @ v)
    if v2 >= 1.0:
        raise ValueError("need |v| < 1")
    g = 1.0 / math.sqrt(1.0 - v2)
    k = g * g / (g + 1.0)
    return g * (E + np.cross(v, B)) - k * float(v @ E) * v, g * (B - np.cross(v, E)) - k * float(v @ B) * v


def general_rates(eE_vec, eB_vec, m: float, fermion: bool, method: str = "closed") -> dict:
    """Pair-number rate and vacuum-decay rate per volume for ANY constant field, via the parallel frame.

    Rates per unit 4-volume are Lorentz scalars, so they equal the parallel-frame rates with eE -> eps,
    eB -> eta (field_invariants). eps = 0 (pure B, crossed |E| <= |B|, null): no pair production.
    method = 'closed' (Kim & Page closed forms) or 'modes' (explicit Landau sums; for eta = 0 the
    continuous k_perp integral of qft_production.rates_from_modes).
    Quantity: dict with 'pair_rate' (IN-IN mean number of PAIRS per unit volume per unit time) and
        'decay_rate' (IN-OUT vacuum decay rate w = 2 Im L_eff per unit volume), both energy^4 and the same
        in every frame, plus 'eps', 'eta', 'kind', 'boost_velocity' from field_invariants.
    Valid when: constant homogeneous fields over a region and time much larger than the formation length
        eps_perp/(e eps); m >= 0 (m > 0 when eta = 0 and method = 'modes'); one loop."""
    inv = field_invariants(eE_vec, eB_vec)
    m = _nonneg(m, "m")
    if method not in ("closed", "modes"):
        raise ValueError("method must be 'closed' or 'modes'")
    out = dict(inv)
    if inv["eps"] == 0.0:
        out.update(pair_rate=0.0, decay_rate=0.0, reason="eps = 0 (magnetic-type, null or zero field): "
                   "no frame with an electric field, no pair production")
        return out
    eps, eta = inv["eps"], inv["eta"]
    if method == "closed":
        r = parallel_closed_forms(m, eps, eta, fermion)
    elif eta > 0:
        r = parallel_rates_from_modes(m, eps, eta, fermion)
    else:
        if m <= 0:
            raise ValueError("method='modes' with eta = 0 needs m > 0")
        r = qp.rates_from_modes(lambda k: qp.schwinger_n_mode(k, m, eps), eps, fermion,
                                12.0 * math.sqrt(eps) + 12.0 * m, n=96)
    out.update(pair_rate=r["pair_rate"], decay_rate=r["decay_rate"])
    return out


# ---------------------------------------------------------------- Part C: E(t) along a constant B
def landau_bogoliubov(p_of_t, t0: float, t1: float, n: int, m: float, eB: float, fermion: bool, spin=None,
                      **solver) -> dict:
    """Mode solver for a homogeneous E(t) parallel to a constant B, one Landau channel (level n, spin s).

    Scalar: qft_production.bogoliubov_boson with omega^2 = eps_perp^2 + p(t)^2; spinor: the exact two-level
    reduction qft_production.bogoliubov_fermion_efield with eps_perp from landau_eps_perp2. p_of_t(t) returns
    the kinetic momentum along B (array over k_par modes, energy), e.g. qft_production.sauter_kinetic_momentum.
    Quantity: dict with 'n' (per-mode IN-IN mean number of particles = antiparticles = pairs in ONE channel:
        one orbit centre, one spin state; dimensionless, after the field has switched off), 'eps_perp2',
        and the solver's diagnostics ('floor', 'resolved', 'steps', ...).
    Valid when: B constant and parallel to E(t), E off at both window ends (adiabatic), eB > 0, eps_perp > 0
        (m > 0 for the spinor's lowest level), t1 > t0; the solver's own ranges (qft_production)."""
    m, eB = _nonneg(m, "m"), _pos(eB, "eB")
    e2 = float(_level_eps2(n, m, eB, fermion, spin))
    if e2 <= 0:
        raise ValueError("eps_perp = 0 (massless spinor, lowest level): n = 1 for any crossing; no solver needed")
    ref = np.atleast_1d(np.asarray(p_of_t(float(t0)), dtype=float))
    if fermion:
        r = qp.bogoliubov_fermion_efield(p_of_t, np.full(ref.shape, math.sqrt(e2)), t0, t1, **solver)
    else:
        r = qp.bogoliubov_boson(lambda t: e2 + np.asarray(p_of_t(t), dtype=float) ** 2, t0, t1, **solver)
        r = dict(r)
        r["n"] = r["beta2"]
    r["eps_perp2"] = e2
    return r


def landau_sauter_n(k_par, n: int, m: float, eE0: float, tau: float, eB: float, fermion: bool, spin=None):
    """Exact occupation for the Sauter pulse E0 sech^2(t/tau) parallel to a constant B, one Landau channel.

    Gavrilov & Gitman 1996 eqs. 42 (spinor) / 43 (scalar) via qft_production.sauter_n_spinor/_scalar with
    k_perp^2 -> eps_perp^2 - m^2 of Landau level n and spin s.
    Quantity: per-mode IN-IN mean number of particles (= antiparticles = pairs) in ONE channel (one orbit
        centre, one spin state) with canonical momentum k_par along the field; dimensionless.
    Valid when: homogeneous Sauter pulse along a constant B, eE0 > 0 (energy^2), tau > 0 (1/energy), eB > 0,
        eps_perp^2 > 0 (m > 0 for the spinor's lowest level)."""
    m, eB = _nonneg(m, "m"), _pos(eB, "eB")
    e2 = _level_eps2(n, m, eB, fermion, spin)
    if np.any(e2 <= 0):
        raise ValueError("eps_perp = 0 (massless spinor, lowest level): need m > 0")
    kp = np.sqrt(np.maximum(e2 - m * m, 0.0))
    return qp.sauter_n_spinor(k_par, kp, m, eE0, tau) if fermion else qp.sauter_n_scalar(k_par, kp, m, eE0, tau)


def landau_sauter_pairs_per_volume(m: float, eE0: float, tau: float, eB: float, fermion: bool, n: int = 96,
                                   rtol: float = 1e-15, max_levels: int = 400_000) -> dict:
    """Total pairs per unit volume made by a Sauter pulse E0 sech^2(t/tau) parallel to a constant B.

    N/V = eB/(2 pi) sum_j g_j int dk_par/(2 pi) n_j(k_par), with the exact per-channel occupations
    (landau_sauter_n), k_par by n-point Gauss-Legendre over |k_par| <= eE0 tau + R (R = 12 (sqrt(eE0) + m + 1/tau),
    the same nodes as qft_production.sauter_pairs_per_volume), levels summed in blocks of 256 until a block
    adds less than rtol of the total.
    Quantity: dict with 'pairs_per_volume' (IN-IN mean number of PAIRS per unit volume after the pulse,
        energy^3; not a rate), 'lll_fraction' (share from the lowest Landau level), 'levels' summed.
    Valid when: as landau_sauter_n with m > 0; levels needed (up to R^2/(2 eB)) <= max_levels: for
        eB -> 0 use qft_production.sauter_pairs_per_volume (the B-dependence starts at O((eB/eE0)^2))."""
    m, eE0, tau, eB = _pos(m, "m"), _pos(eE0, "eE0"), _pos(tau, "tau"), _pos(eB, "eB")
    if n < 16 or not (0 < rtol < 1e-3):
        raise ValueError("need n >= 16 and 0 < rtol < 1e-3")
    reach = 12.0 * (math.sqrt(eE0) + m + 1.0 / tau)
    kz, wz = _gl(-eE0 * tau - reach, eE0 * tau + reach, n)
    jmax = int(reach * reach / (2.0 * eB)) + 1
    total, lll, j0, chunk = 0.0, 0.0, 0, 256
    while j0 <= jmax:
        if j0 >= max_levels:
            raise ValueError(f"B too weak: more than max_levels = {max_levels} Landau levels contribute; "
                             "use qft_production.sauter_pairs_per_volume (B -> 0)")
        j = np.arange(j0, min(j0 + chunk, jmax + 1))
        if fermion:
            kp, g = np.sqrt(2.0 * j * eB), np.where(j == 0, 1.0, 2.0)
        else:
            kp, g = np.sqrt((2.0 * j + 1.0) * eB), np.ones(len(j))
        KZ, KP = np.meshgrid(kz, kp, indexing="ij")
        nk = qp.sauter_n_spinor(KZ, KP, m, eE0, tau) if fermion else qp.sauter_n_scalar(KZ, KP, m, eE0, tau)
        per_level = np.einsum("i,ij->j", wz, nk) * g
        if j0 == 0:
            lll = float(per_level[0])
        part = float(np.sum(per_level))
        total += part
        j0 += chunk
        if total > 0 and part < rtol * total:
            break
    pref = eB / (2 * PI) / (2 * PI)
    return {"pairs_per_volume": pref * total, "lll_fraction": lll / total if total > 0 else float("nan"),
            "levels": min(j0, jmax + 1)}


def landau_lcfa_pairs_per_volume(m: float, eE0: float, tau: float, eB: float, fermion: bool,
                                 panels: int = 24, nodes: int = 16) -> float:
    """Locally-constant-field estimate int dt Gamma(E(t), B) for the Sauter pulse along a constant B.

    Uses the constant parallel-field PAIR rate (Kim & Page eqs. 3-4; NOT the vacuum-decay rate) at each
    instant, composite Gauss-Legendre over |t| <= 6 tau.
    Quantity: mean number of PAIRS per unit volume (energy^3) in the locally-constant-field approximation.
    Valid when: eE0 tau^2 >> 1 and eps_perp tau >> 1 (slowly varying on the formation time); relative
        corrections O(1/(eE0 tau^2)) (measured 0.4-0.6% at eE0 tau^2 = 3000); m >= 0, eB >= 0."""
    m, eE0, tau, eB = _nonneg(m, "m"), _pos(eE0, "eE0"), _pos(tau, "tau"), _nonneg(eB, "eB")
    if m == 0 and eB == 0:
        raise ValueError("m = 0 and eB = 0: use qft_production.lcfa_pairs_per_volume conventions (m > 0)")
    t, w = _composite_gl(-6 * tau, 6 * tau, panels, nodes)
    return float(np.sum(w * _pair_rate_closed_vec(m, eE0 / np.cosh(t / tau) ** 2, eB, fermion)))


# ---------------------------------------------------------------- independent check: explicit Dirac/KG grids
def _fourier_grid(N: int, L: float):
    """Odd-N periodic Fourier grid: x (symmetric about 0), spectral first (D1) and second (D2) derivatives.
    Odd N has no Nyquist mode, so D1 is exactly antisymmetric and has no spurious zero mode."""
    if N % 2 == 0:
        raise ValueError("use an odd number of grid points")
    h = L / N
    x = (np.arange(N) - (N - 1) / 2) * h
    k = 2 * PI * np.fft.fftfreq(N, d=h)
    F = np.fft.fft(np.eye(N), axis=0)
    D1 = np.real(np.fft.ifft(1j * k[:, None] * F, axis=0))
    D2 = np.real(np.fft.ifft(-(k * k)[:, None] * F, axis=0))
    return x, 0.5 * (D1 - D1.T), 0.5 * (D2 + D2.T)


def _scalar_landau_grid(eB: float, n_levels: int, N: int = 63, L_mag: float = 14.0) -> np.ndarray:
    """Lowest eigenvalues of pi_perp^2 = p_x^2 + (eB x)^2 (k_y = 0) on a Fourier grid of N points over
    L_mag magnetic lengths: assumes no Landau algebra."""
    x, _, D2 = _fourier_grid(N, L_mag / math.sqrt(eB))
    return np.linalg.eigvalsh(-D2 + np.diag((eB * x) ** 2))[:n_levels]


def _dirac_landau_blocks(m: float, eB: float, n_levels: int, N: int = 63, L_mag: float = 14.0) -> list:
    """Explicit 4-component transverse Dirac operator on a Fourier grid (Dirac representation, gauge
    A_y = B x, k_y = 0) -> the invariant blocks of each Landau level, assuming no Landau algebra.

    M = [[m, D], [D, -m]] with D = sigma_x p_x + sigma_y pi_y = i K (K real antisymmetric), so
    M^2 = diag(m^2 + K^T K) and the real symmetric Pauli operator K^T K = (sigma . pi_perp)^2 is diagonalised.
    The periodic grid makes pi_y = -eB x jump at the box edge: a domain wall carrying an extra zero mode,
    which is removed by keeping only eigenvectors localised in |x| < L/4 (the orbit centre is x = 0).
    For each level j (eigenvalue 2 j eB of K^T K) returns a dict with the bulk count k (= channels), the
    spin-up weight, the Rayleigh eigenvalue, and the block matrices A = Q^T alpha_z Q, C = Q^T M Q on the
    2k-dimensional space Q = {(u, 0), (0, u)}, plus invariance residuals."""
    L = L_mag / math.sqrt(eB)
    x, D1, _ = _fourier_grid(N, L)
    s_rot = np.array([[0.0, -1.0], [1.0, 0.0]])                       # sigma_y / i
    K = np.kron(np.array([[0.0, 1.0], [1.0, 0.0]]), -D1) + np.kron(s_rot, np.diag(-eB * x))
    P2 = K.T @ K
    w, U = np.linalg.eigh(0.5 * (P2 + P2.T))
    xx = np.concatenate([x, x])
    bulk = (np.abs(xx) < L / 4).astype(float)
    sz = np.concatenate([np.ones(N), -np.ones(N)])                     # sigma_z (x) 1
    out = []
    for j in range(n_levels):
        sel = np.where(np.abs(w - 2 * j * eB) < 1e-6 * eB + 1e-12)[0]
        W = U[:, sel]
        pb, V = np.linalg.eigh(W.T @ (bulk[:, None] * W))
        ub = W @ V[:, pb > 0.5]
        k = ub.shape[1]
        if k == 0:
            out.append({"level": j, "channels": 0})
            continue
        Kb = ub.T @ K @ ub
        Sb = ub.T @ (sz[:, None] * ub)
        Z = np.zeros((k, k))
        A = np.block([[Z, Sb], [Sb, Z]]).astype(complex)
        Cm = np.block([[m * np.eye(k), 1j * Kb], [1j * Kb, -m * np.eye(k)]])
        out.append({"level": j, "channels": k, "eig": float(np.mean(np.diag(ub.T @ P2 @ ub))),
                    "spin_up": float(np.sum(ub[:N] ** 2) / k), "A": A, "C": Cm,
                    "res_alpha": float(np.linalg.norm(sz[:, None] * ub - ub @ Sb)),
                    "res_M": float(np.linalg.norm(K @ ub - ub @ Kb)),
                    "anticomm": float(np.linalg.norm(A @ Cm + Cm @ A))})
    return out


def _dirac_block_pairs(A: np.ndarray, C: np.ndarray, p_of_t, t0: float, t1: float, steps: int) -> np.ndarray:
    """Evolve i dpsi/dt = (p(t) A + C) psi in one Landau block (batched over k_par modes) with 4th-order
    Magnus steps and exact exponentials; start in the negative-energy eigenstates of H(t0) and return the
    summed probability of ending in positive-energy eigenstates of H(t1) = mean number of pairs in the
    block (all channels) per k_par mode."""
    d = A.shape[0]
    H = lambda t: np.asarray(p_of_t(t), dtype=float)[:, None, None] * A[None] + C[None]   # noqa: E731
    _, Wi = np.linalg.eigh(H(t0))
    psi = Wi[:, :, : d // 2].copy()
    h = (t1 - t0) / steps
    for i in range(steps):
        t = t0 + i * h
        H1, H2 = H(t + _G1 * h), H(t + _G2 * h)
        Km = 0.5 * h * (H1 + H2) - 1j * (_SQRT3 * h * h / 12.0) * (H2 @ H1 - H1 @ H2)
        ww, WW = np.linalg.eigh(Km)
        psi = WW @ (np.exp(-1j * ww)[:, :, None] * (np.conj(np.swapaxes(WW, 1, 2)) @ psi))
    _, Wo = np.linalg.eigh(H(t1))
    amp = np.conj(np.swapaxes(Wo[:, :, d // 2:], 1, 2)) @ psi
    return np.sum(np.abs(amp) ** 2, axis=(1, 2))


def _lorentz_tensor_boost(E: np.ndarray, B: np.ndarray, v: np.ndarray):
    """Independent field transformation: F'^{mu nu} = Lambda F Lambda^T with F^{0i} = -E^i,
    F^{ij} = -eps_{ijk} B^k (metric +---), Lambda the pure boost to a frame moving with velocity v."""
    F = np.zeros((4, 4))
    F[0, 1:], F[1:, 0] = -E, E
    F[1, 2], F[2, 3], F[3, 1] = -B[2], -B[0], -B[1]
    F[2, 1], F[3, 2], F[1, 3] = B[2], B[0], B[1]
    v2 = float(v @ v)
    g = 1.0 / math.sqrt(1.0 - v2)
    Lam = np.eye(4)
    Lam[0, 0] = g
    Lam[0, 1:] = Lam[1:, 0] = -g * v
    Lam[1:, 1:] += (g - 1.0) * np.outer(v, v) / v2 if v2 > 0 else 0.0
    Fp = Lam @ F @ Lam.T
    return -Fp[0, 1:], np.array([-Fp[2, 3], -Fp[3, 1], -Fp[1, 2]])


# ---------------------------------------------------------------- self-test
def selftest(verbose: bool = True) -> bool:
    """Compare with closed forms, published results and independent numerical methods. Returns True if all pass."""
    results = []

    def check(name, got, want, tol, rel=False):
        err = abs(got - want) / (abs(want) if rel and want != 0 else 1.0)
        ok = bool(err <= tol)
        results.append(ok)
        if verbose:
            print(f"{'PASS' if ok else 'FAIL'}  {name}: {got:.10g} (expected {want:.10g}, "
                  f"{'rel' if rel else 'abs'} tol {tol:g})")

    m, eB = 1.0, 0.25

    # 1. Scalar Landau spectrum without Landau algebra: p_x^2 + (eB x)^2 on a Fourier grid (63 points over 14
    #    magnetic lengths; spectral accuracy, measured 1e-13) -> (2n + 1) eB. Dunne 2004 (hep-th/0406216) p. 19,
    #    eq. 1.55: "There is no spin p rojection term in the eigenvalues of the Klein-Gordon operator, so the
    #    ζ-function is ζscalar(s) = eB 2π ∞∑ n=0 ∫ d2k⊥ (2π)2 (m2 +k2 ⊥ +eB(2n + 1) µ2 )−s"; Tanji 2009
    #    (arXiv:0810.4429) eq. 2.49: "np =e−2πan = exp { −π[m2 + (2n + 1)eB] eE }".
    ev = _scalar_landau_grid(eB, 6) / eB
    check("scalar: Fourier-grid pi_perp^2/eB = 1, 3, 5, ..., 11 (max abs error; tol 1e-9 >> measured 1e-13)",
          float(np.max(np.abs(ev - (2 * np.arange(6) + 1)))), 0.0, 1e-9)
    sp = landau_spectrum(m, eB, False, 6)
    check("scalar: landau_spectrum eps_perp^2 - m^2 = grid eigenvalues", float(np.max(np.abs(sp["eps_perp2"] - m * m
          - ev * eB))), 0.0, 1e-9)

    # 2. Spinor Landau spectrum and channel count without Landau algebra: explicit 4-component Dirac operator on
    #    the grid. Dunne 2004 p. 16, eq. 1.44: "the eigenvalues of t he Dirac operator are λ± n =m2 +k2 ⊥ +eB(2n
    #    + 1 ± 1) , n = 0, 1,... (1.44) where the ± refers to the two spin components"; Tanji 2009 eq. 2.70:
    #    "a↑ n≡ m2+2neB 2eE a↓ n≡ m2+(2n+2)eB 2eE (n = 0, 1,··· )". Expected: (sigma.pi)^2 = 2 j eB with ONE bulk
    #    state at j = 0 (spin up only) and TWO for j >= 1; alpha_z and M map each block into itself and anticommute.
    blocks = _dirac_landau_blocks(m, eB, 4)
    sps = landau_spectrum(m, eB, True, 4)
    check("spinor: grid bulk channels per level (j = 0..3) = landau_spectrum channels [1, 2, 2, 2]",
          float(sum(abs(b["channels"] - c) for b, c in zip(blocks, sps["channels"]))), 0.0, 0)
    check("spinor: grid (sigma.pi_perp)^2 eigenvalues = 2 j eB (max abs error over j = 0..3; tol 1e-9)",
          float(max(abs(b["eig"] - 2 * b["level"] * eB) for b in blocks)), 0.0, 1e-9)
    check("spinor: lowest level is pure spin-up (spin-up weight 1)", blocks[0]["spin_up"], 1.0, 1e-9)
    check("spinor: blocks invariant under alpha_z and M, {alpha_z, M} = 0 (max residual; roundoff)",
          max(max(b["res_alpha"], b["res_M"], b["anticomm"]) for b in blocks), 0.0, 1e-9)

    # 3. E(t) along B, spinor: the explicit 4-component Dirac evolution of each Landau block through a Sauter
    #    pulse vs channels x Gavrilov & Gitman 1996 (hep-th/9603152) eq. 42 with eps_perp^2 = m^2 + 2 j eB:
    #    "Np,r = sinh [ πα 2 (2eEα +ω− −ω+) ] sinh [ πα 2 (2eEα +ω+ −ω−) ] sinh(παω+) sinh(παω−) . (42)" (alpha = tau).
    #    Tolerance 1e-6: 2000 Magnus-4 steps, measured error 1.4e-7 .. 3.8e-7.
    eE0, tau = 0.5, 2.0
    kz = np.linspace(-1.2 * eE0 * tau, 1.2 * eE0 * tau, 5)
    pf, (t0, t1) = qp.sauter_kinetic_momentum(kz, eE0, tau)
    worst, worst2 = 0.0, 0.0
    for b in blocks[:3]:
        got = _dirac_block_pairs(b["A"], b["C"], pf, t0, t1, 2000)
        ref = b["channels"] * landau_sauter_n(kz, b["level"], m, eE0, tau, eB, True, spin=+1)
        worst = max(worst, float(np.max(np.abs(got / ref - 1))))
        r2 = landau_bogoliubov(pf, t0, t1, b["level"], m, eB, True, spin=+1)
        worst2 = max(worst2, float(np.max(np.abs(r2["n"] / ref * b["channels"] - 1))))
    check("Sauter || B, spinor: explicit Dirac blocks j = 0,1,2 vs channels x GG eq. 42 (max rel. error, 5 k_par)",
          worst, 0.0, 1e-6)
    check("Sauter || B, spinor: two-level solver with Landau eps_perp vs GG eq. 42 (max rel. error)", worst2, 0.0, 1e-6)

    # 4. E(t) along B, scalar: mode solver omega^2 = m^2 + (2n+1) eB + p(t)^2 vs GG 1996 eq. 43 with the Landau
    #    eps_perp: "Np,r = cosh2 [ π √ (eEα 2)2 − 1 4 ] + sinh2 [ πα 2 (ω+ −ω−) ] sinh(παω+) sinh(παω−) . (43)".
    #    Tanji 2009 p. 13: "Eq.(2.43) takes the same form as that in the pure electric ﬁeld case (2.8) with the
    #    replacementm2+ζn→m2+p2 T." Tolerance 1e-6 as in qft_production (solver rtol 1e-7).
    worst = 0.0
    for lev in range(3):
        r = landau_bogoliubov(pf, t0, t1, lev, m, eB, False)
        worst = max(worst, float(np.max(np.abs(r["n"] / landau_sauter_n(kz, lev, m, eE0, tau, eB, False) - 1))))
    check("Sauter || B, scalar: boson solver levels n = 0,1,2 vs GG eq. 43 (max rel. error)", worst, 0.0, 1e-6)

    # 5. Constant parallel fields: Landau mode sums vs the published closed forms. Kim & Page 2006
    #    (hep-th/0301132) eqs. 1-4: "2ImL(1) spinor = w(1) spinor = (qE)(qB) (2π)2 ∞∑ n=1 1 n coth ( nπB E ) exp ( −
    #    nπm2 qE ) , (1) and that for scalar QED by [1, 10, 11, 12] 2ImL(1) scalar = w(1) scalar = (qE)(qB) 2(2π)2
    #    ∞∑ n=1 (−1)n+1 n csch ( nπB E ) exp ( − nπm2 qE ) . (2) The pair-production rates per volume per time
    #    themselves ar e the ﬁrst terms in each of these series [13], N (1) spinor = (qE)(qB) (2π)2 coth ( πB E )
    #    exp ( − πm2 qE ) , (3) and N (1) scalar = (qE)(qB) 2(2π)2 csch ( πB E ) exp ( − πm2 qE ) . (4)".
    #    Same w in Dunne 2004 eq. 1.28 "ImL(1) spinor ∼ e2EB 8π2 ∞∑ n=1 1 n coth (B E nπ ) exp [ −m2πn eE ]" and
    #    eq. 1.40 "ImL(1) scalar ∼ e2EB 16π2 ∞∑ n=1 (−1)n−1 n 1 sinh (B Enπ )exp [ −m2πn eE ]" (Im L = w/2).
    #    Tolerance 1e-12: both are float sums of <= 65 positive (or rapidly alternating) terms; measured 4e-16.
    worst, order_ok = 0.0, True
    for fermion in (True, False):
        for eE in (0.5, 5.0):
            for b_over_e in (0.1, 1.0, 3.0):
                r = parallel_rates_from_modes(m, eE, b_over_e * eE, fermion)
                c = parallel_closed_forms(m, eE, b_over_e * eE, fermion)
                worst = max(worst, abs(r["pair_rate"] / c["pair_rate"] - 1), abs(r["decay_rate"] / c["decay_rate"] - 1))
                order_ok &= (r["decay_rate"] > r["pair_rate"]) == fermion
    check("E || B: Landau sums (Gamma and w) vs Kim & Page eqs. 1-4, 12 cases (max rel. error)", worst, 0.0, 1e-12)
    check("E || B: w > Gamma for spinors, w < Gamma for scalars (in-out decay vs in-in pair number)",
          float(order_ok), 1.0, 0)

    # 6. B -> 0: the Landau sum must reduce to Schwinger (qft_production.schwinger_closed_forms) and to the
    #    continuous k_perp integral (qft_production.rates_from_modes). At B/E = 1e-4 the exact closed forms
    #    differ from B = 0 by (pi B/E)^2/3 = 3.3e-8 (spinor) and -(pi B/E)^2/6 (scalar) in Gamma, and by about as
    #    much in w (measured 3.4e-8): tolerance 1e-7, i.e. the physical O((B/E)^2) effect, not numerical error.
    worst = 0.0
    for fermion in (True, False):
        eE = 1.0
        r = parallel_rates_from_modes(m, eE, 1e-4 * eE, fermion)
        s = qp.schwinger_closed_forms(m, eE, fermion)
        q = qp.rates_from_modes(lambda k: qp.schwinger_n_mode(k, m, eE), eE, fermion, 12.0, n=96)
        worst = max(worst, abs(r["pair_rate"] / s["pair_rate"] - 1), abs(r["decay_rate"] / s["decay_rate"] - 1),
                    abs(r["pair_rate"] / q["pair_rate"] - 1), abs(r["decay_rate"] / q["decay_rate"] - 1))
    check("B/E = 1e-4: Landau sums -> Schwinger closed forms and the k_perp integral (max rel. dev.)", worst, 0.0, 1e-7)

    # 7. Strong B (B/E = 5): only the lowest Landau level contributes. Limits of Kim & Page eqs. 1-4 with
    #    coth -> 1, csch(x) -> 2 e^{-x}: spinor Gamma = eE eB/(4 pi^2) e^{-pi m^2/eE} and w = -eE eB/(4 pi^2)
    #    ln(1 - e^{-pi m^2/eE}) (1+1-dimensional Schwinger x eB/2pi); scalar Gamma = eE eB/(4 pi^2) e^{-pi(m^2+eB)/eE}.
    #    Exact relative deviation 2 e^{-10 pi} = 4.5e-14: tolerance 1e-12. Tanji 2009 p. 17: "(i) pair creation of
    #    fermion in n = 0 and ↑-mode is not suppressed by the magnetic ﬁeld, while that of bosons in any Landau
    #    level is suppressed exponentially, and (ii) the number of modes degenerating in one Landau level per unit
    #    area is eB/2π".
    eE = 1.0
    eBs = 5.0 * eE
    x = math.exp(-PI * m * m / eE)
    cs, cb = parallel_closed_forms(m, eE, eBs, True), parallel_closed_forms(m, eE, eBs, False)
    pref = eE * eBs / (4 * PI * PI)
    check("B/E = 5, spinor: Gamma -> lowest-level (1+1 D Schwinger) x eB/2pi", cs["pair_rate"], pref * x, 1e-12, rel=True)
    check("B/E = 5, spinor: w -> -eE eB/(4pi^2) ln(1 - e^{-pi m^2/eE})", cs["decay_rate"], -pref * math.log1p(-x),
          1e-12, rel=True)
    check("B/E = 5, scalar: Gamma -> eE eB/(4pi^2) e^{-pi(m^2 + eB)/eE}", cb["pair_rate"],
          pref * math.exp(-PI * (m * m + eBs) / eE), 1e-12, rel=True)
    # Lowest-level share of the spinor pair rate: e^{-pi m^2/eE} / [coth(pi B/E) e^{-pi m^2/eE}] = tanh(pi B/E) exactly
    # (eq. 3); at B/E = 0.5 that is 0.917, so the check discriminates (at B/E = 5 it would be 1 - 4.5e-14).
    rs = parallel_rates_from_modes(m, eE, 0.5 * eE, True)
    check("B/E = 0.5, spinor: Landau sum's lowest-level share of Gamma = tanh(pi B/E) (eq. 3)", rs["lll_fraction"],
          math.tanh(0.5 * PI), 1e-12, rel=True)
    s0, b0 = qp.schwinger_closed_forms(m, eE, True), qp.schwinger_closed_forms(m, eE, False)
    check("B enhances spinor (x > 10) and suppresses scalar (x < 1e-5) pair rates at B/E = 5",
          float(cs["pair_rate"] > 10 * s0["pair_rate"] and cb["pair_rate"] < 1e-5 * b0["pair_rate"]), 1.0, 0)

    # 8. Massless spinor: with B > 0 the lowest level has n = 1 exactly, Gamma finite and w infinite. Abramchuk et
    #    al. 2016 (arXiv:1605.02379) abstract: "The pair production rate remains finite unlike the vacuum decay
    #    rate."; Hidaka et al. 2011 (arXiv:1103.3097) abstract: "for massless quarks, the vacuum persistency
    #    probability per unit space‐time volume is zero, i.e., the quark‐pair creation rate w is infinite, in
    #    general homogeneous color electromagnetic fields, while it is finite when the color magnetic field is
    #    absent." With B = 0 (Schwinger): w = (eE)^2/(4 pi^3) Li_2(1) = (eE)^2/(24 pi) exactly.
    r0, c0 = parallel_rates_from_modes(0.0, 1.0, 0.5, True), parallel_closed_forms(0.0, 1.0, 0.5, True)
    check("m = 0, B > 0: Gamma = eE eB/(4pi^2) coth(pi B/E) (Landau sum)", r0["pair_rate"],
          0.5 / (4 * PI * PI) / math.tanh(0.5 * PI), 1e-12, rel=True)
    check("m = 0, B > 0: w = infinity from both the Landau sum and the closed form",
          float(math.isinf(r0["decay_rate"]) and math.isinf(c0["decay_rate"])), 1.0, 0)
    check("m = 0, B = 0: w = (eE)^2/(24 pi) (finite)", parallel_closed_forms(0.0, 1.0, 0.0, True)["decay_rate"],
          1.0 / (24 * PI), 1e-12, rel=True)

    # 9. General constant fields. Dunne 2004 eqs. 1.4-1.6: "a2 −b2 = ⃗E2 − ⃗B2 = − 1 2FµνF µν ≡ −2F , (1.4) ab = ⃗E
    #    · ⃗B = − 1 4Fµν ˜F µν ≡ −G . (1.5) Thus a = √ √ F 2 + G2 − F , b = √ √ F 2 + G2 + F . (1.6) If G ⁄= 0, it is
    #    possible to transform to a Lorentz frame in which the elec- tric and magnetic ﬁelds are parallel"; Kim &
    #    Page 2006 p. 1: "one can go to a frame in which E and B are parallel with magnitude E and B". Independent
    #    method: the field tensor boosted with an explicit 4x4 Lorentz matrix. Tolerances 1e-12: roundoff of a
    #    few 4x4 products and square roots.
    rng = np.random.default_rng(7)
    Er, Br, vr = rng.normal(size=3), rng.normal(size=3), 0.6 * rng.normal(size=3) / math.sqrt(3)
    e1, b1 = boost_fields(Er, Br, vr)
    e2, b2 = _lorentz_tensor_boost(Er, Br, vr)
    check("boost_fields (3-vector formula) = explicit tensor boost Lambda F Lambda^T", float(np.max(np.abs(
          np.concatenate([e1 - e2, b1 - b2])))), 0.0, 1e-12)
    a0, bb0 = 0.7, 0.4
    vb = np.array([0.5, -0.3, 0.6])
    Eb, Bb = _lorentz_tensor_boost(np.array([0, 0, a0]), np.array([0, 0, bb0]), vb)
    inv = field_invariants(Eb, Bb)
    check("boosted parallel field: (eps, eta) recovered from the invariants", abs(inv["eps"] - a0) + abs(inv["eta"] - bb0),
          0.0, 1e-12)
    gr, pr = general_rates(Eb, Bb, m, True), parallel_closed_forms(m, a0, bb0, True)
    check("boosted parallel field: general_rates = parallel-frame rates (Lorentz-scalar rates)",
          abs(gr["pair_rate"] / pr["pair_rate"] - 1) + abs(gr["decay_rate"] / pr["decay_rate"] - 1), 0.0, 1e-12)
    Ep, Bp = _lorentz_tensor_boost(Eb, Bb, inv["boost_velocity"])
    par = float(np.linalg.norm(np.cross(Ep, Bp)) / (np.linalg.norm(Ep) * np.linalg.norm(Bp)))
    check("boost along E x B with v/(1+v^2) = |ExB|/(E^2+B^2) makes E || B with |E| = eps, |B| = eta",
          par + abs(np.linalg.norm(Ep) - a0) + abs(np.linalg.norm(Bp) - bb0), 0.0, 1e-12)

    # 10. Crossed and null fields. Dunne 2004 p. 12: "If E2 > B2, then the situation is as for the purely electric
    #    ﬁeld, with a vacuum instability. On the other hand, if B2 > E2, then the system behaves like the case of a
    #    purely magnetic ﬁe ld. If E2 =B2, then L(1) spinor vanishes and there are no quantum corrections at all."
    #    Crossed E > B: textbook boost v = B/E removes B, leaving E' = sqrt(E^2 - B^2).
    E0v, Bc = np.array([1.0, 0, 0]), np.array([0, 0.6, 0])
    ic = field_invariants(E0v, Bc)
    sc = qp.schwinger_closed_forms(m, 0.8, True)
    gc = general_rates(E0v, Bc, m, True)
    check("crossed |E| > |B|: eps = sqrt(E^2 - B^2), |v| = B/E, rates = Schwinger(eps)",
          abs(ic["eps"] - 0.8) + abs(np.linalg.norm(ic["boost_velocity"]) - 0.6) + abs(gc["pair_rate"] / sc["pair_rate"] - 1)
          + abs(gc["decay_rate"] / sc["decay_rate"] - 1), 0.0, 1e-12)
    zero = [general_rates(E0v, np.array([0, 1.5, 0]), m, fermion)["pair_rate"] for fermion in (True, False)]
    zero += [general_rates(E0v, np.array([0, 1.0, 0]), 0.0, True)["decay_rate"],
             general_rates([0, 0, 0], [0, 0, 2.0], m, False)["decay_rate"]]
    nulls = field_invariants(E0v, np.array([0, 1.0, 0]))
    check("no production: crossed |E| < |B|, null (|E| = |B|, even m = 0), pure B; null has no parallel frame",
          float(max(zero) == 0.0 and nulls["kind"] == "null" and nulls["boost_velocity"] is None), 1.0, 0)

    # 11. Sauter pulse along B, totals. (a) B -> 0: the Landau sum is a trapezoid/midpoint rule in k_perp^2 with step
    #     2 eB, so its B-dependence is O(eB^2); Richardson (eB = 0.01, 0.005) removes it and must reproduce the
    #     continuous k_perp integral of qft_production.sauter_pairs_per_volume (same k_par nodes). Measured 2.7e-8
    #     (O(eB^4) remainder): tolerance 1e-6. (b) Long pulse (eE0 tau^2 = 3000): exact Landau total -> int dt
    #     Gamma(E(t), B) with the coth/csch pair rate; measured 0.38% (spinor), 0.58% (scalar), falling as 1/tau^2
    #     (4.3-6.6% at tau = 30): tolerance 1e-2 as qft_production's B = 0 check.
    worst = 0.0
    for fermion in (True, False):
        a_ = landau_sauter_pairs_per_volume(m, 0.5, 2.0, 0.01, fermion)["pairs_per_volume"]
        b_ = landau_sauter_pairs_per_volume(m, 0.5, 2.0, 0.005, fermion)["pairs_per_volume"]
        worst = max(worst, abs((4 * b_ - a_) / 3 / qp.sauter_pairs_per_volume(m, 0.5, 2.0, fermion) - 1))
    check("Sauter || B, eB -> 0 (Richardson) -> qft_production.sauter_pairs_per_volume (max rel. dev.)", worst, 0.0, 1e-6)
    for fermion in (True, False):
        ex = landau_sauter_pairs_per_volume(m, 0.3, 100.0, 0.3, fermion)["pairs_per_volume"]
        lc = landau_lcfa_pairs_per_volume(m, 0.3, 100.0, 0.3, fermion)
        check(f"Sauter || B (B/E0 = 1, tau = 100), {'spinor' if fermion else 'scalar'}: exact -> int dt Gamma(E(t), B)",
              ex, lc, 1e-2, rel=True)

    passed = all(results)
    if verbose:
        print(f"\n{sum(results)}/{len(results)} checks passed")
    return passed


def _convergence() -> int:
    """Slower studies (not part of the self-test): grid size, Magnus steps, B -> 0 and long-pulse limits."""
    m, eB = 1.0, 0.25
    print("Fourier grid (Dirac blocks): max |(sigma.pi)^2 - 2 j eB|, j <= 4, and bulk channel counts")
    for N, Lm in ((31, 10.0), (47, 12.0), (63, 14.0), (95, 16.0)):
        bl = _dirac_landau_blocks(m, eB, 5, N=N, L_mag=Lm)
        errs = [abs(b.get("eig", float("nan")) - 2 * b["level"] * eB) for b in bl]
        print(f"  N = {N:3d}, L = {Lm:4.1f} l_B: max error {max(errs):.2e}, channels {[b['channels'] for b in bl]}")
    print("Dirac block evolution vs channels x GG eq. 42 (Sauter eE0 = 0.5, tau = 2): max rel. error vs steps")
    blocks = _dirac_landau_blocks(m, eB, 3)
    kz = np.linspace(-1.2, 1.2, 5)
    pf, (t0, t1) = qp.sauter_kinetic_momentum(kz, 0.5, 2.0)
    for steps in (500, 1000, 2000, 4000):
        err = max(float(np.max(np.abs(_dirac_block_pairs(b["A"], b["C"], pf, t0, t1, steps)
                                      / (b["channels"] * landau_sauter_n(kz, b["level"], m, 0.5, 2.0, eB, True, 1)) - 1)))
                  for b in blocks)
        print(f"  steps {steps:5d}: {err:.2e}")
    print("Constant E || B: Landau-sum Gamma relative to Schwinger, vs (pi B/E) coth(pi B/E) - 1 (spinor)")
    for b in (1e-1, 1e-2, 1e-3, 1e-4):
        r = parallel_rates_from_modes(m, 1.0, b, True)
        s = qp.schwinger_closed_forms(m, 1.0, True)
        print(f"  B/E = {b:7.0e}: {r['pair_rate'] / s['pair_rate'] - 1:+.4e} (exact {PI * b / math.tanh(PI * b) - 1:+.4e}),"
              f" {r['levels']} levels")
    print("Sauter || B totals: B -> 0 (eE0 = 0.5, tau = 2) and long-pulse ratio to the LCFA (eE0 = 0.3, eB = 0.3)")
    for fermion in (True, False):
        ref = qp.sauter_pairs_per_volume(m, 0.5, 2.0, fermion)
        vals = [landau_sauter_pairs_per_volume(m, 0.5, 2.0, e, fermion)["pairs_per_volume"] for e in (0.02, 0.01, 0.005)]
        print(f"  {'spinor' if fermion else 'scalar'}: eB = .02/.01/.005 rel. dev. "
              f"{', '.join(f'{v / ref - 1:+.2e}' for v in vals)}; Richardson {(4 * vals[1] - vals[0]) / 3 / ref - 1:+.2e}, "
              f"{(4 * vals[2] - vals[1]) / 3 / ref - 1:+.2e}")
        for tau in (30.0, 100.0, 300.0):
            ex = landau_sauter_pairs_per_volume(m, 0.3, tau, 0.3, fermion)["pairs_per_volume"]
            print(f"    tau = {tau:5.0f}: exact/LCFA - 1 = {ex / landau_lcfa_pairs_per_volume(m, 0.3, tau, 0.3, fermion) - 1:+.3e}")
    return 0


# ---------------------------------------------------------------- command line
def _energy(text: str) -> float:
    """Parse an energy ('0.511 MeV' -> eV) or a bare number (already in eV)."""
    try:
        return float(text)
    except ValueError:
        from unit_tools import Q
        return Q(text).expect("energy").si / E_CHARGE


def _print_rates(tag: str, r: dict, c: dict) -> None:
    print(f"  pair-number rate Gamma (mean pairs per volume per time, in-in): Landau sum {r['pair_rate']:.6g} eV^4 = "
          f"{qp.rate_density_to_SI(r['pair_rate']):.6g} m^-3 s^-1; closed form {c['pair_rate']:.6g} eV^4")
    print(f"  vacuum-decay rate w = 2 Im L_eff (in-out): Landau sum {r['decay_rate']:.6g} eV^4 = "
          f"{qp.rate_density_to_SI(r['decay_rate']):.6g} m^-3 s^-1; closed form {c['decay_rate']:.6g} eV^4; "
          f"w/Gamma = {r['ratio']:.6f}")
    print(f"  lowest Landau level share of Gamma: {r['lll_fraction']:.4f} ({r['levels']} levels summed; {tag})")


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("selftest")
    sub.add_parser("convergence", help="slower studies: grids, Magnus steps, B -> 0 and long-pulse limits")
    pp = sub.add_parser("parallel", help="constant parallel E and B: pair-number and vacuum-decay rates")
    gp = sub.add_parser("general", help="any constant E and B (angle between them): invariants and rates")
    sp = sub.add_parser("sauter", help="Sauter pulse E0 sech^2(t/tau) along a constant B: pairs per volume")
    for p in (pp, gp, sp):
        p.add_argument("--E", required=True, help="electric field, e.g. '1e18 V/m' (peak field for sauter)")
        p.add_argument("--B", required=True, help="magnetic field, e.g. '1e9 T' or '1e13 gauss' ('G' is Newton's G)")
        p.add_argument("--m", default="0.51099895 MeV", help="mass, e.g. '0.511 MeV' (default: electron)")
        p.add_argument("--scalar", action="store_true", help="scalar QED instead of spinor QED")
    gp.add_argument("--angle", type=float, required=True, help="angle between E and B in degrees")
    sp.add_argument("--tau", required=True, help="pulse time scale, e.g. '1e-20 s'")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "selftest":
            return 0 if selftest() else 1
        if args.cmd == "convergence":
            return _convergence()
        from unit_tools import Q
        m = _energy(args.m)
        eE = qp.eE_from_field_SI(Q(args.E).expect("V/m").si)
        eB = eB_from_field_SI(Q(args.B).expect("T").si)
        fermion = not args.scalar
        tag = "spinor QED" if fermion else "scalar QED"
        print(f"{tag}, m = {m:.6g} eV; eE = {eE:.6g} eV^2 = {eE / m ** 2:.4g} m^2, eB = {eB:.6g} eV^2 = "
              f"{eB / m ** 2:.4g} m^2 (B/E = cB/E = {eB / eE if eE > 0 else float('inf'):.4g})")
        if eB > 0:
            print(f"Landau degeneracy eB/(2 pi) = {landau_degeneracy_SI(field_B_to_SI(eB)):.6g} m^-2 per level and channel")
        if args.cmd == "parallel":
            if eE <= 0 or eB <= 0:
                raise ValueError("parallel needs E > 0 and B > 0 (B = 0: use qft_production.py schwinger)")
            r = parallel_rates_from_modes(m, eE, eB, fermion)
            c = parallel_closed_forms(m, eE, eB, fermion)
            _print_rates(tag, r, c)
            if m > 0:
                s = qp.schwinger_closed_forms(m, eE, fermion)
                print(f"  same E without B: Gamma {s['pair_rate']:.6g} eV^4 (B changes Gamma by x{r['pair_rate'] / s['pair_rate']:.4g})")
        elif args.cmd == "general":
            th = math.radians(args.angle)
            g = general_rates([0.0, 0.0, eE], [eB * math.sin(th), 0.0, eB * math.cos(th)], m, fermion)
            v = g["boost_velocity"]
            print(f"  invariants: kind = {g['kind']}; parallel-frame fields E = {field_E_to_SI(g['eps']):.6g} V/m, "
                  f"B = {field_B_to_SI(g['eta']):.6g} T; boost speed to that frame "
                  f"{'none (null field)' if v is None else f'{np.linalg.norm(v):.6g} c (1 - v/c = {1 - np.linalg.norm(v):.3g})'}")
            print(f"  pair-number rate Gamma (mean pairs per volume per time, in-in, any frame) {g['pair_rate']:.6g} eV^4 = "
                  f"{qp.rate_density_to_SI(g['pair_rate']):.6g} m^-3 s^-1")
            print(f"  vacuum-decay rate w = 2 Im L_eff (in-out) {g['decay_rate']:.6g} eV^4 = "
                  f"{qp.rate_density_to_SI(g['decay_rate']):.6g} m^-3 s^-1")
        else:
            tau = qp.time_to_inverse_eV(Q(args.tau).expect("time").si)
            if eE <= 0 or eB <= 0:
                raise ValueError("sauter needs E > 0 and B > 0 (B = 0: use qft_production.py sauter)")
            r = landau_sauter_pairs_per_volume(m, eE, tau, eB, fermion)
            lc = landau_lcfa_pairs_per_volume(m, eE, tau, eB, fermion)
            print(f"  eE0 tau^2 = {eE * tau * tau:.4g}, m tau = {m * tau:.4g}")
            print(f"  exact pairs per volume (in-in, after the pulse) {r['pairs_per_volume']:.6g} eV^3 = "
                  f"{qp.density_to_SI(r['pairs_per_volume']):.6g} m^-3 (lowest-level share {r['lll_fraction']:.4f}, "
                  f"{r['levels']} levels)")
            print(f"  locally-constant-field int dt Gamma(E(t), B): {lc:.6g} eV^3 (exact/LCFA = "
                  f"{r['pairs_per_volume'] / lc if lc > 0 else float('nan'):.4g})")
            print(f"  same pulse without B: {qp.sauter_pairs_per_volume(m, eE, tau, fermion):.6g} eV^3")
    except (ValueError, KeyError) as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
