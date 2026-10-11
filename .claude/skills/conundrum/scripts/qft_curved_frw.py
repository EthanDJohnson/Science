#!/usr/bin/env python3
"""qft_curved_frw: particle creation in spatially CURVED Friedmann-Robertson-Walker universes (closed K = +1,
open K = -1, and flat K = 0 for comparison) for a real scalar of mass m and curvature coupling xi, in conformal
time, with every function saying exactly WHICH quantity it returns (numpy + mpmath, no scipy). Companion of
qft_production.py (flat FRW, homogeneous E fields, Born), whose mode solver bogoliubov_boson it uses for every
mode.

Why this tool exists
    Spatial curvature changes three things that are easy to get wrong: the spectrum of the spatial Laplacian
    (discrete on the 3-sphere, shifted on the hyperboloid), the curvature term xi R phi^2 (R contains K/a^2, so
    even a static closed universe has R != 0), and the counting (a closed universe has a finite volume, so its
    total particle number is a finite sum over levels with degeneracy n^2; an open universe only has densities).
    On top come the toolkit's usual traps: in-in versus in-out (|beta|^2 is an in-in mean number, 1/|alpha|^2 an
    in-out probability), real production versus transient polarisation (numbers are defined only between static
    in and out regions), and particles versus pairs (a real field makes pairs: pairs = particles/2). Every public
    function has a "Quantity:" line and a "Valid when:" line and refuses inputs outside that range (ValueError).

Units (read this first)
    Natural units hbar = c = 1, Heaviside-Lorentz electromagnetism (e^2 = 4 pi alpha), exactly as
    qft_production.py (no electromagnetism is used here). Pick ONE energy unit (e.g. eV, or the mass m) and give
    m, comoving wavenumbers k and inverse conformal times in it; conformal time eta and the comoving curvature
    radius L are then in 1/energy, and the scale factor a(eta) is dimensionless, so the PHYSICAL curvature radius
    is a L. "Curvature-radius units" (the default L = 1) measure eta, 1/k and 1/m in units of the comoving
    curvature radius. Numbers per comoving volume are in energy^3 (L = 1: per unit comoving volume of the unit
    sphere or hyperboloid). This deviates from schemas.md's "SI in the Python API" on purpose (precedent:
    qft_production.py, page_wootters.py): SI helpers convert (length_to_inverse_eV, and qft_production's
    density_to_SI), and the command line accepts units through unit_tools.Q ("0.511 MeV", "1e-12 m", "1e15 1/s").

Model
    Metric (signature + - - -; Anderson & Eaker 2000, gr-qc/9906055, eq. 1):
        ds^2 = a(eta)^2 [ d eta^2 - gamma_ij dx^i dx^j ],   gamma = S^3 (K = +1), H^3 (K = -1), R^3 (K = 0),
        gamma of constant sectional curvature K/L^2.
    Field equation (box + m^2 + xi R) phi = 0, conformal coupling xi = 1/6, minimal xi = 0, with
        R = 6 (a''/a^3 + K/(L^2 a^2))                     (A&E eq. 6 at L = 1; ' = d/d eta)
    in the sign convention where R > 0 for de Sitter and for the static closed universe. Writing
    phi = chi(eta) Y(x)/a(eta) with -Lap_gamma Y = lambda Y gives (derived with sympy and gr_tensors.py in the
    development scratch; identical to A&E eq. 5, k^2 + m^2 a^2 + (xi - 1/6) a^2 R):
        chi'' + omega^2(eta) chi = 0,
        omega^2 = lambda + m^2 a^2 + (6 xi - 1) a''/a + 6 xi K/L^2.
    Spatial spectrum (A&E eq. 4: Lap Y = -(k^2 - K) Y):
        closed S^3:  lambda_n = (n^2 - 1)/L^2,  n = 1, 2, 3, ...,  degeneracy n^2 (real modes per level),
                     comoving volume 2 pi^2 L^3;
        open H^3:    lambda_k = k^2 + 1/L^2,    k >= 0 (continuous), k^2 dk/(2 pi^2) modes per comoving volume
                     (the same density as flat space; supercurvature modes with imaginary k are not normalisable
                     and are not part of this spectrum);
        flat R^3:    lambda_k = k^2,            k^2 dk/(2 pi^2) per comoving volume (qft_production Part C).
    Conformal coupling: omega^2 = n^2/L^2 + m^2 a^2 (closed), k^2 + m^2 a^2 (open, flat): the curvature drops out
    and a massless conformal field makes NOTHING for any a(eta).
    Minimal coupling: omega^2 = lambda + m^2 a^2 - a''/a; the closed level n = 1 is the homogeneous mode
    (lambda = 0), a zero mode when m = 0 (refused: no particle interpretation).
    Conventions differ between sources: Vaudrevange & Kofman (below) write the conformally coupled equation as
    (box + m^2 - R/6) phi = 0 (their R has the opposite sign) and call the H^3 eigenvalue lambda^2, where -Lap on
    their harmonics gives lambda^2 + 1; their omega^2 = lambda^2 + m^2 a^2 is still right, because conformal
    coupling's 6 xi K/L^2 = -1 cancels the +1. Here lambda always means the eigenvalue of -Lap.

Quantities
    Per mode: |beta|^2 from qft_production.bogoliubov_boson between static (adiabatic) in and out regions = the
    IN-IN mean number of out-particles in ONE real mode of that level (every one of the n^2 modes of level n has
    the same |beta_n|^2). Totals:
        closed: total particles in the WHOLE universe N = sum_n n^2 |beta_n|^2 (finite), per comoving volume
                N/(2 pi^2 L^3), per physical volume at the end N/(2 pi^2 (L a_out)^3);
        open:   particles per comoving volume int_0^inf k^2 dk/(2 pi^2) |beta_k|^2 (the total is infinite).
    Real field: the quanta are created in pairs, pairs = particles/2. Complex field (two real fields): particles
    = antiparticles = sum n^2 |beta_n|^2 and pairs = particles. In-out vacuum persistence of the whole closed
    universe: |<0 out|0 in>|^2 = prod over real modes 1/|alpha| = exp(-(1/2) sum_n n^2 ln(1 + |beta_n|^2)) for a
    real field (each real mode is a single-mode squeezed state, overlap 1/cosh r = 1/|alpha|); -ln P < mean pairs.

Milne universe (exact benchmark, K = -1, L = 1, a = e^eta): R = 0 (it is flat space-time inside the light
    cone), so omega^2 = k^2 + m^2 e^{2 eta} for EVERY xi, solved by Bessel functions of order -ik. The in vacuum
    at eta -> -inf is the conformal vacuum, the out vacuum the adiabatic (= Minkowski) one, and
    |beta_k|^2 = e^{-pi k}/(2 sinh pi k) = 1/(e^{2 pi k} - 1) for every m > 0 (Vaudrevange & Kofman 2007,
    arXiv:0706.0980, eq. 23). This is not creation BY curvature: it is the conformal vacuum seen in the
    Minkowski particle basis. The solver's zeroth-order out basis converges to it as O(1/(m e^{eta1})).

Assumptions and validity range
    Free real scalar (complex = two copies) on a prescribed classical background, no back-reaction; a(eta) > 0;
    static or adiabatic in and out regions (omega^2 > 0 and |omega'|/omega^2 <= 1e-3 at both window ends, enforced
    by the solver); particle numbers at intermediate times are not defined. K in {+1, 0, -1}, L > 0, m >= 0, any
    real xi. Closed sums must converge inside n_max and open integrals inside k_max (checked; refused otherwise).
    Not covered: global de Sitter (its in/out vacua are not adiabatic: |omega'|/omega^2 -> H/m), spinors, photons,
    gravitons, renormalised stress tensors.

Python usage
    import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
    import numpy as np, qft_production as qp, qft_curved_frw as cf
    a, app, (e0, e1) = qp.frw_tanh_scale_factor(2.0, 1.0, 0.7)        # a^2 = 2 + tanh(0.7 eta), L = 1
    r = cf.curved_frw_particle_production(+1, [1, 2, 3], a, 1.0, 0.0, e0, e1, a_pp=app)   # r["beta2"] per mode
    cf.conformal_tanh_beta2(+1, [1, 2, 3], 1.0, 2.0, 1.0, 0.7)        # closed form (xi = 1/6 only)
    c = cf.closed_universe_production(60, a, 1.0, 0.0, e0, e1, a_pp=app)
    c["particles_total"], c["pairs_total"], c["per_comoving_volume"], c["vacuum_persistence"]
    o = cf.open_universe_density(5.0, a, 1.0, 0.0, e0, e1, a_pp=app)  # o["per_comoving_volume"]
    cf.milne_beta2([0.3, 0.5])                                        # exact Milne spectrum

Command line (from the project root)
    python3 .claude/skills/conundrum/scripts/qft_curved_frw.py selftest
    python3 .claude/skills/conundrum/scripts/qft_curved_frw.py tanh --K 1 --m 1 --xi 0 --A 2 --B 1 --rho 0.7 --nmax 40
    python3 .claude/skills/conundrum/scripts/qft_curved_frw.py tanh --K -1 --m "1 eV" --xi 0.1666666667 --A 2 --B 1 \\
            --rho "0.7 eV" --L "1.97e-7 m" --kmax 6
    python3 .claude/skills/conundrum/scripts/qft_curved_frw.py milne --m 1 --k 0.2 0.4
    python3 .claude/skills/conundrum/scripts/qft_curved_frw.py convergence      (slow: flat limit vs L, Milne vs window)
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

import qft_production as qp  # noqa: E402  (mode solver, tanh closed form, quadrature, SI helpers)
from unit_tools import C, E_CHARGE, HBAR  # noqa: E402  (CODATA values shared by the toolkit)

PI = math.pi


# ---------------------------------------------------------------- SI helpers
def length_to_inverse_eV(ell_m: float) -> float:
    """Convert a length in m to natural units 1/eV: ell_nat = ell e/(hbar c).

    Quantity: length (e.g. the comoving curvature radius L or a conformal time) in 1/eV.
    Valid when: ell_m is a length in metres."""
    return ell_m * E_CHARGE / (HBAR * C)


def inverse_eV_to_length(x_nat: float) -> float:
    """Convert a natural-unit length in 1/eV to metres: ell = x hbar c/e.

    Quantity: length in m.
    Valid when: x_nat is a length (or conformal time) in units of 1/eV."""
    return x_nat * HBAR * C / E_CHARGE


# ---------------------------------------------------------------- input checks
def _check_K(K) -> int:
    if K not in (-1, 0, 1) or isinstance(K, bool):
        raise ValueError("K must be +1 (closed), 0 (flat) or -1 (open)")
    return int(K)


def _check_L(L) -> float:
    L = float(L)
    if not (math.isfinite(L) and L > 0):
        raise ValueError("the comoving curvature radius L must be finite and > 0")
    return L


def _labels(K: int, labels) -> np.ndarray:
    x = np.atleast_1d(np.asarray(labels, dtype=float))
    if x.ndim != 1 or x.size == 0 or not np.all(np.isfinite(x)):
        raise ValueError("mode labels must be a non-empty 1-D array of finite numbers")
    if K == 1:
        if np.any(x < 1) or np.any(x != np.round(x)):
            raise ValueError("closed universe (K = +1): levels n must be integers >= 1 (lambda_n = (n^2 - 1)/L^2)")
    elif np.any(x < 0):
        raise ValueError("open/flat universe: comoving wavenumbers k must be >= 0")
    return x


def _check_m_xi(m, xi):
    if not (math.isfinite(m) and m >= 0):
        raise ValueError("m must be finite and >= 0")
    if not math.isfinite(xi):
        raise ValueError("xi must be finite")


# ---------------------------------------------------------------- spatial spectrum and curvature
def spatial_eigenvalue(K: int, labels, L: float = 1.0) -> np.ndarray:
    """Eigenvalue lambda of -Lap on the comoving 3-space of curvature K/L^2 (Anderson & Eaker 2000 eq. 4).

    closed S^3: (n^2 - 1)/L^2 for integer n >= 1; open H^3: k^2 + 1/L^2 for k >= 0; flat: k^2.
    Quantity: lambda in energy^2 (comoving), one value per label.
    Valid when: K in {+1, 0, -1}; closed labels are integers n >= 1, open/flat labels k >= 0; L > 0."""
    K, L = _check_K(K), _check_L(L)
    x = _labels(K, labels)
    if K == 1:
        return (x * x - 1.0) / (L * L)
    if K == -1:
        return x * x + 1.0 / (L * L)
    return x * x


def closed_degeneracy(n) -> np.ndarray:
    """Number of independent real modes of -Lap on S^3 at level n (eigenvalue (n^2 - 1)/L^2): n^2.

    Quantity: degeneracy n^2 (dimensionless count of real modes; all share the same |beta_n|^2).
    Valid when: n are integers >= 1."""
    return _labels(1, n) ** 2


def closed_comoving_volume(L: float = 1.0) -> float:
    """Comoving volume of the closed universe, the 3-sphere of radius L: 2 pi^2 L^3.

    Quantity: comoving volume in energy^-3 (physical volume = this x a^3).
    Valid when: L > 0."""
    return 2.0 * PI * PI * _check_L(L) ** 3


def open_spectral_density(k) -> np.ndarray:
    """Density of modes of -Lap on H^3 (or R^3) per unit comoving volume per unit comoving wavenumber: k^2/(2 pi^2).

    For H^3 of radius L the eigenvalue at label k is k^2 + 1/L^2; the density in k is the flat one.
    Quantity: modes per comoving volume per unit k, in energy^2.
    Valid when: k >= 0."""
    return _labels(-1, k) ** 2 / (2.0 * PI * PI)


def closed_mode_count(N: int) -> int:
    """Exact number of real modes on S^3 with level n <= N: sum_{n<=N} n^2 = N(N+1)(2N+1)/6.

    Quantity: number of modes in the WHOLE closed universe (dimensionless integer).
    Valid when: N is an integer >= 1."""
    if int(N) != N or N < 1:
        raise ValueError("N must be an integer >= 1")
    return int(np.sum(closed_degeneracy(np.arange(1, int(N) + 1))))


def weyl_mode_count(k_max: float, volume: float) -> float:
    """Weyl's law: number of modes with wavenumber <= k_max in a region of comoving volume V: V k_max^3/(6 pi^2).

    Quantity: mode count (dimensionless), the large-k_max asymptote of the exact count on any 3-space.
    Valid when: k_max >= 0, volume > 0; for S^3 compare with closed_mode_count(N) at k_max = N/L (relative
        difference O(1/N))."""
    if not (k_max >= 0 and volume > 0 and math.isfinite(k_max) and math.isfinite(volume)):
        raise ValueError("need k_max >= 0 and volume > 0")
    return volume * k_max ** 3 / (6.0 * PI * PI)


def ricci_scalar(a, a_pp, K: int, L: float = 1.0):
    """Ricci scalar of ds^2 = a(eta)^2 (d eta^2 - gamma), gamma of curvature K/L^2: R = 6 (a''/a^3 + K/(L^2 a^2)).

    Anderson & Eaker 2000 eq. 6 (L = 1); sign convention: R > 0 for de Sitter (12 H^2) and the static closed
    universe (6/(a L)^2), R = 0 for the Milne universe (a = e^{eta/L}, K = -1).
    Quantity: R in energy^2 (a'' = d^2 a/d eta^2 in energy^2, eta conformal time).
    Valid when: a > 0 (arrays allowed), K in {+1, 0, -1}, L > 0."""
    K, L = _check_K(K), _check_L(L)
    a = np.asarray(a, dtype=float)
    if np.any(a <= 0) or not np.all(np.isfinite(a)):
        raise ValueError("a must be finite and > 0")
    return 6.0 * (np.asarray(a_pp, dtype=float) / a ** 3 + K / (L * L * a * a))


# ---------------------------------------------------------------- mode frequency and solver
def curved_frw_omega2(K: int, labels, a, m: float, xi: float, a_pp=None, L: float = 1.0, h: float = None):
    """Mode frequency of chi = a phi for a scalar (mass m, coupling xi R phi^2/2) in curved FRW, conformal time.

    chi'' + omega^2 chi = 0,  omega^2 = lambda + m^2 a^2 + (6 xi - 1) a''/a + 6 xi K/L^2,
    lambda = spatial_eigenvalue(K, labels, L). Conformal coupling: omega^2 = n^2/L^2 + m^2 a^2 (closed),
    k^2 + m^2 a^2 (open). If a_pp is None, a'' is taken by a 5-point finite difference with step h (default 1e-2
    in the units of eta; truncation ~h^4 a^(6)/90), as in qft_production.frw_omega2.
    Quantity: a callable eta -> omega^2 (array over the labels, energy^2, with eta in 1/energy).
    Valid when: a(eta) > 0 (checked at every call); K in {+1, 0, -1}; closed labels integers n >= 1, open/flat
        k >= 0; m >= 0; any real xi; L > 0."""
    K, L = _check_K(K), _check_L(L)
    _check_m_xi(m, xi)
    lam = spatial_eigenvalue(K, labels, L)
    base = lam + 6.0 * xi * K / (L * L)
    mm, c = m * m, 6.0 * xi - 1.0
    if a_pp is None:
        hh = 1e-2 if h is None else float(h)
        if not hh > 0:
            raise ValueError("finite-difference step h must be > 0")

        def a_pp(eta):   # noqa: F811  (5-point second derivative)
            return (-a(eta + 2 * hh) + 16 * a(eta + hh) - 30 * a(eta) + 16 * a(eta - hh) - a(eta - 2 * hh)) / (12 * hh * hh)

    def w2(eta):
        av = float(a(eta))
        if not av > 0:
            raise ValueError(f"a(eta) = {av} <= 0 at eta = {eta}")
        return base + mm * av * av + (c * float(a_pp(eta)) / av if c != 0 else 0.0)

    return w2


def curved_frw_particle_production(K: int, labels, a, m: float, xi: float, eta0: float, eta1: float, a_pp=None,
                                   L: float = 1.0, **solver) -> dict:
    """Particles created per mode between static in (eta0) and out (eta1) regions of a curved FRW universe.

    Runs qft_production.bogoliubov_boson on curved_frw_omega2 (keyword arguments go to the solver).
    Quantity: dict whose "beta2" is the per-mode IN-IN mean number of particles in ONE real mode of each level
        (closed: each of the n^2 modes of level n; open/flat: one mode at comoving k), dimensionless, not a pair
        count and not a total; with the solver's "floor", "beta2_relerr", "resolved", "alpha2" and
        "vacuum_persistence_mode" (= 1/|alpha|^2, in-out, for a PAIR of modes; one real mode alone: 1/|alpha|),
        plus "labels", "eigenvalue", "K", "L". Totals: closed_universe_totals / open_universe_density.
    Valid when: a(eta) and a''/a are static (adiabatic) at both window ends, omega^2 > 0 there (e.g. the
        massless minimally coupled closed n = 1 zero mode is refused), a > 0 throughout, eta0 < eta1."""
    w2 = curved_frw_omega2(K, labels, a, m, xi, a_pp=a_pp, L=L)
    r = qp.bogoliubov_boson(w2, eta0, eta1, **solver)
    r.update(labels=_labels(K, labels), eigenvalue=spatial_eigenvalue(K, labels, L), K=K, L=float(L))
    return r


# ---------------------------------------------------------------- totals
def closed_universe_totals(n, beta2, L: float = 1.0, a_out: float = None, field: str = "real",
                           tail_tol: float = 1e-3) -> dict:
    """Totals over the closed universe from per-mode |beta_n|^2 for EVERY level n = 1..N.

    particles = sum_n n^2 |beta_n|^2 (real field: pairs = particles/2; complex field = two real fields:
    particles = antiparticles = sum_n n^2 |beta_n|^2 and pairs = particles); the tail (last 10% of levels, at
    least one) must hold <= tail_tol of the total. Vacuum persistence ln P = -(1/2) sum n^2 ln(1 + |beta_n|^2)
    per real field.
    Quantity: dict of IN-IN mean numbers for the WHOLE closed universe: "particles_total" (real field: particles;
        complex field: particles, with an equal "antiparticles_total"), "pairs_total" (real: particles/2;
        complex: = particles), "per_comoving_volume" (particles per comoving volume, energy^3: / (2 pi^2 L^3)),
        "per_physical_volume_out" (particles per physical volume at a_out, energy^3, if a_out is given), and the
        IN-OUT "vacuum_persistence" P = |<0 out|0 in>|^2 of the whole universe with "log_vacuum_persistence"
        (-ln P < pairs for bosons), plus "tail_fraction".
    Valid when: n is exactly 1, 2, ..., N (every level); |beta_n|^2 >= 0 finite; field 'real' or 'complex';
        the sum has converged (tail fraction <= tail_tol, else ValueError: raise N); L > 0, a_out > 0."""
    if field not in ("real", "complex"):
        raise ValueError("field must be 'real' or 'complex'")
    L = _check_L(L)
    n = _labels(1, n)
    if not np.array_equal(n, np.arange(1, n.size + 1)):
        raise ValueError("closed-universe totals need every level n = 1, 2, ..., N in order")
    b2 = np.asarray(beta2, dtype=float)
    if b2.shape != n.shape or not np.all(np.isfinite(b2)) or np.any(b2 < 0):
        raise ValueError("beta2 must be finite, >= 0 and match n")
    contrib = n * n * b2
    total = float(np.sum(contrib))
    ntail = max(1, n.size // 10)
    tail = float(np.sum(contrib[-ntail:])) / total if total > 0 else 0.0
    if tail > tail_tol:
        raise ValueError(f"closed-universe sum not converged: the last {ntail} level(s) hold {tail:.3g} of the total "
                         f"(> tail_tol = {tail_tol:g}); raise N")
    g = 0.5 if field == "real" else 1.0
    logP = -g * float(np.sum(n * n * np.log1p(b2)))
    out = {"particles_total": total, "pairs_total": 0.5 * total if field == "real" else total,
           "per_comoving_volume": total / closed_comoving_volume(L), "log_vacuum_persistence": logP,
           "vacuum_persistence": math.exp(logP), "tail_fraction": tail, "field": field, "N": int(n.size)}
    if field == "complex":
        out["antiparticles_total"] = total
    if a_out is not None:
        if not (math.isfinite(a_out) and a_out > 0):
            raise ValueError("a_out must be finite and > 0")
        out["per_physical_volume_out"] = total / (closed_comoving_volume(L) * a_out ** 3)
    return out


def closed_universe_production(n_max: int, a, m: float, xi: float, eta0: float, eta1: float, a_pp=None,
                               L: float = 1.0, field: str = "real", tail_tol: float = 1e-3, **solver) -> dict:
    """Run every level n = 1..n_max of a closed universe through the solver and total them.

    Quantity: closed_universe_totals(...) for the WHOLE closed universe (in-in mean particles, pairs, per
        comoving and per physical volume at a_out = a(eta1), in-out vacuum persistence), plus "modes" (the
        solver dict) and "total_relerr" (estimated relative error of particles_total from the solver's per-mode
        errors; unresolved modes count with their full value or floor).
    Valid when: as curved_frw_particle_production with K = +1; the level sum converges within n_max; n_max <= 20000
        (more levels mean n/L >> the switching rate: use the flat limit, corrections O(1/(k L)^2))."""
    if int(n_max) != n_max or n_max < 1 or n_max > 20000:
        raise ValueError("n_max must be an integer in 1..20000 (for more levels use the flat limit)")
    n = np.arange(1, int(n_max) + 1, dtype=float)
    r = curved_frw_particle_production(1, n, a, m, xi, eta0, eta1, a_pp=a_pp, L=L, **solver)
    tot = closed_universe_totals(n, r["beta2"], L=L, a_out=float(a(eta1)), field=field, tail_tol=tail_tol)
    err = np.where(r["resolved"], r["beta2"] * r["beta2_relerr"], np.maximum(r["beta2"], r["floor"]))
    s = tot["particles_total"]
    tot["total_relerr"] = float(np.sum(n * n * err)) / s if s > 0 else math.inf
    tot["modes"] = r
    return tot


def open_universe_density(k_max: float, a, m: float, xi: float, eta0: float, eta1: float, a_pp=None, L: float = 1.0,
                          K: int = -1, nodes: int = 64, field: str = "real", tail_tol: float = 1e-3, **solver) -> dict:
    """Particles per comoving volume in an open (K = -1) or flat (K = 0) universe: int_0^k_max k^2 dk/(2 pi^2) |beta_k|^2.

    Gauss-Legendre with `nodes` points on [0, k_max]; the integrand at the top node times k_max/10 must be
    <= tail_tol of the result (spectrum cut off inside k_max).
    Quantity: dict with "per_comoving_volume" (IN-IN mean PARTICLES per comoving volume, energy^3; complex field:
        particles, antiparticles equal), "pairs_per_comoving_volume" (real: /2; complex: = particles),
        "per_physical_volume_out" (at a_out = a(eta1)), "total_relerr", "modes" (solver dict at the nodes).
        The total number in an open universe is infinite: only densities exist.
    Valid when: K in {-1, 0}; k_max > 0, 8 <= nodes <= 4096; the spectrum is negligible above k_max (checked); and
        as curved_frw_particle_production."""
    K = _check_K(K)
    if K == 1:
        raise ValueError("K = +1 is discrete: use closed_universe_production")
    if field not in ("real", "complex"):
        raise ValueError("field must be 'real' or 'complex'")
    if not (math.isfinite(k_max) and k_max > 0) or not 8 <= int(nodes) <= 4096:
        raise ValueError("need k_max > 0 and 8 <= nodes <= 4096")
    k, w = qp._gauss_legendre(0.0, float(k_max), int(nodes))
    r = curved_frw_particle_production(K, k, a, m, xi, eta0, eta1, a_pp=a_pp, L=L, **solver)
    integrand = k * k * r["beta2"] / (2 * PI * PI)
    dens = float(np.sum(w * integrand))
    tail = float(integrand[-1] * k_max / 10.0) / dens if dens > 0 else 0.0
    if tail > tail_tol:
        raise ValueError(f"spectrum not cut off: the top of [0, k_max] carries ~{tail:.3g} of the result; raise k_max")
    err = np.where(r["resolved"], r["beta2"] * r["beta2_relerr"], np.maximum(r["beta2"], r["floor"]))
    a_out = float(a(eta1))
    return {"per_comoving_volume": dens, "pairs_per_comoving_volume": 0.5 * dens if field == "real" else dens,
            "per_physical_volume_out": dens / a_out ** 3, "field": field, "tail_fraction": tail,
            "total_relerr": float(np.sum(w * k * k * err)) / (2 * PI * PI) / dens if dens > 0 else math.inf,
            "modes": r}


# ---------------------------------------------------------------- exact benchmarks
def conformal_tanh_beta2(K: int, labels, m: float, A: float, B: float, rho: float, L: float = 1.0) -> np.ndarray:
    """Exact |beta|^2 for conformal coupling in the tanh universe a(eta)^2 = A + B tanh(rho eta) (Bernard & Duncan).

    With xi = 1/6, omega^2 = k_eff^2 + m^2 a^2 with k_eff = n/L (closed), k (open, flat), so the flat closed form
    qft_production.tanh_model_beta2 applies with k -> k_eff.
    Quantity: per-mode in-in mean number of particles |beta|^2 in one real mode (dimensionless).
    Valid when: xi = 1/6 only; A > |B| (a^2 > 0), rho > 0, m >= 0; closed labels integers n >= 1, open k >= 0
        (k_eff > 0 or m > 0)."""
    K, L = _check_K(K), _check_L(L)
    if not A > abs(B):
        raise ValueError("need A > |B| so that a(eta)^2 > 0")
    keff = np.sqrt(spatial_eigenvalue(K, labels, L) + K / (L * L))
    if m == 0 and np.any(keff == 0):
        raise ValueError("massless k = 0 mode has omega = 0")
    return qp.tanh_model_beta2(keff, m, A, B, rho)


def milne_scale_factor():
    """The Milne universe in conformal time, curvature-radius units (K = -1, L = 1): a(eta) = e^eta, a'' = e^eta.

    t = e^eta is proper time; the space-time is flat (R = 0) inside the future light cone.
    Quantity: callables (a(eta), a''(eta)) (dimensionless a; a'' in energy^2 with eta in curvature-radius units).
    Valid when: any real eta (use with K = -1, L = 1)."""
    return (lambda eta: np.exp(eta)), (lambda eta: np.exp(eta))


def milne_beta2(k) -> np.ndarray:
    """Exact Milne spectrum |beta_k|^2 = 1/(e^{2 pi k} - 1) (Vaudrevange & Kofman 2007, eq. 23), for every m > 0, xi.

    Quantity: per-mode in-in mean number of ADIABATIC (= Minkowski) quanta in the CONFORMAL vacuum (the in vacuum
        at eta -> -inf), in one real mode at comoving k (curvature-radius units), as eta_out -> inf. Not creation
        by curvature (Milne is flat space-time); dimensionless.
    Valid when: k > 0, m > 0, K = -1, L = 1, a = e^eta, out time m e^{eta_out} >> 1 (finite eta_out: use
        milne_beta2_finite)."""
    k = _labels(-1, k)
    if np.any(k == 0):
        raise ValueError("k must be > 0 (k = 0 diverges)")
    return 1.0 / np.expm1(2.0 * PI * k)


def milne_beta2_finite(k, m: float, eta1: float) -> np.ndarray:
    """Exact |beta_k|^2 at a FINITE out time eta1 in Milne, from the Bessel-function in mode (mpmath).

    chi_in = Gamma(1 - ik) (m/2)^{ik} J_{-ik}(m e^eta)/sqrt(2k) (-> e^{-ik eta}/sqrt(2k) as eta -> -inf; Vaudrevange &
    Kofman eq. 21 up to a phase), projected on the zeroth-order adiabatic out basis at eta1:
    |beta|^2 = (omega/2) |chi - i chi'/omega|^2, omega = sqrt(k^2 + m^2 e^{2 eta1}) (the basis bogoliubov_boson uses).
    Quantity: per-mode in-in mean number of zeroth-order adiabatic quanta at eta1 in the conformal vacuum
        (dimensionless); tends to milne_beta2(k) as O(1/(m e^{eta1})).
    Valid when: k > 0, m > 0, m e^{eta1} <= 1e7 (mpmath cost), K = -1, L = 1, a = e^eta."""
    import mpmath as mp
    k = _labels(-1, k)
    if np.any(k == 0) or not (math.isfinite(m) and m > 0):
        raise ValueError("need k > 0 and m > 0")
    z = m * math.exp(eta1)
    if not z <= 1e7:
        raise ValueError("m e^eta1 must be <= 1e7")
    out = []
    with mp.workdps(30):
        for kk in k:
            c = mp.gamma(1 - 1j * kk) * mp.power(m / 2.0, 1j * kk) / mp.sqrt(2 * kk)
            chi = c * mp.besselj(-1j * kk, z)
            chip = c * z * mp.besselj(-1j * kk, z, derivative=1)
            w = mp.sqrt(kk * kk + z * z)
            out.append(float((w / 2) * abs(chi - 1j * chip / w) ** 2))
    return np.array(out)


def _milne_window(k, m: float, z1: float = 1200.0, eps_in: float = 1e-6):
    """Window for Milne: in end where m^2 e^{2 eta0}/k_min^3 = eps_in (|omega'|/omega^2 there), out end m e^{eta1} = z1."""
    kmin = float(np.min(k))
    return 0.5 * math.log(eps_in * kmin ** 3 / (m * m)), math.log(z1 / m)


# ---------------------------------------------------------------- self-test helpers (independent methods)
def _heat_trace_closed(t: float, L: float = 1.0) -> float:
    """sum_n n^2 exp(-lambda_n t) over S^3 (whole universe), from the module's spectrum functions."""
    nmax = int(L * math.sqrt(60.0 / t)) + 2
    n = np.arange(1, nmax + 1)
    return float(np.sum(closed_degeneracy(n) * np.exp(-spatial_eigenvalue(1, n, L) * t)))


def _heat_trace_open(t: float, L: float = 1.0) -> float:
    """int dk k^2/(2 pi^2) exp(-lambda_k t) on H^3 (per unit comoving volume), Gauss-Legendre."""
    k, w = qp._gauss_legendre(0.0, math.sqrt(80.0 / t), 200)
    return float(np.sum(w * open_spectral_density(k) * np.exp(-spatial_eigenvalue(-1, k, L) * t)))


def _fock_squeeze_overlap(r: float, dim: int = 160):
    """Single-mode squeeze S(r) = exp(r (a^2 - a^dag^2)/2) in a truncated Fock space, by eigendecomposition.

    Returns (|<0|S|0>|^2, <0|S^dag N S|0>): an independent numerical check of 1/cosh r and sinh^2 r."""
    a = np.diag(np.sqrt(np.arange(1, dim)), 1)
    G = 0.5 * (a @ a - a.T @ a.T)                    # real antisymmetric generator
    Hm = 1j * G                                        # Hermitian
    ev, V = np.linalg.eigh(Hm)
    S = (V * np.exp(-1j * r * ev)) @ V.conj().T        # exp(r G) = exp(-i r (iG))
    psi = S[:, 0]
    return float(abs(psi[0]) ** 2), float(np.sum(np.arange(dim) * np.abs(psi) ** 2))


# ---------------------------------------------------------------- self-test
def selftest(verbose: bool = True) -> bool:
    """Compare with published equations, exact limits and independent methods. Returns True if all pass."""
    results = []

    def check(name, got, want, tol, rel=False):
        err = abs(got - want) / (abs(want) if rel and want != 0 else 1.0)
        ok = bool(err <= tol)
        results.append(ok)
        if verbose:
            print(f"{'PASS' if ok else 'FAIL'}  {name}: {got:.10g} (expected {want:.10g}, "
                  f"{'rel' if rel else 'abs'} tol {tol:g})")

    # 1. Spatial spectrum against the heat-kernel expansion. Vassilevich 2003 (hep-th/0306138) eq. 2.21,
    #    "TrL2(f exp(-tD)) ~= sum k>=0 t(k-n)/2 ak(f,D)", eqs. 4.26-4.28 with E = 0: "a0(f,D) = (4pi)-n/2 int
    #    dnx sqrt(g) trV{f}", "a2(f,D) = (4pi)-n/2 6-1 int dnx sqrt(g) trV{f(6E + R)}", "a4(f,D) = (4pi)-n/2 360-1 int
    #    ... (... 5R2 - 2RijRij + 2RijklRijkl ...)", with "R = 2 on the unit sphere S2". Unit S^3: R = 6,
    #    Ric^2 = 12, Riem^2 = 12, so Tr e^{t Lap} (4 pi t)^{3/2}/Vol = 1 + t + t^2/2 + O(t^3); unit H^3 (per unit
    #    volume): 1 - t + t^2/2 + O(t^3). This tests the eigenvalues n^2 - 1 and k^2 + 1, the degeneracy n^2, the
    #    density k^2/(2 pi^2) and the volume 2 pi^2 together. t = 0.05: the O(t^3) remainder is t^3/6 = 2.1e-5,
    #    so the tolerance is 3e-5.
    t = 0.05
    check("S^3 heat trace x (4 pi t)^1.5/(2 pi^2) = 1 + R t/6 + a4 t^2 (Vassilevich 4.26-4.28, R = 6)",
          _heat_trace_closed(t) * (4 * PI * t) ** 1.5 / closed_comoving_volume(), 1 + t + t * t / 2, 3e-5)
    check("H^3 heat trace per volume x (4 pi t)^1.5 = 1 + R t/6 + a4 t^2 (R = -6)",
          _heat_trace_open(t) * (4 * PI * t) ** 1.5, 1 - t + t * t / 2, 3e-5)
    #    Same with L = 3 (curvature K/L^2): R = 6K/9, so the t-coefficient is K/9.
    check("S^3 of radius L = 3: heat trace -> 1 + t/L^2 + t^2/(2 L^4)",
          _heat_trace_closed(t, 3.0) * (4 * PI * t) ** 1.5 / closed_comoving_volume(3.0), 1 + t / 9 + t * t / 162, 3e-5)
    #    Weyl's law (leading term): exact count / (V k^3/(6 pi^2)) at k = N/L must be 1 + 3/(2N) + 1/(2N^2), i.e. the
    #    count approaches Weyl's flat-space N^3/3 with an O(1/N) correction. Exact algebra: tolerance is roundoff.
    N = 400
    check(f"Weyl law on S^3: sum_(n<={N}) n^2 / (2 pi^2 N^3/(6 pi^2)) - 1 = 3/(2N) + 1/(2N^2)",
          closed_mode_count(N) / weyl_mode_count(float(N), closed_comoving_volume()) - 1, 1.5 / N + 0.5 / N ** 2, 1e-12)

    # 2. Mode equation against Anderson & Eaker 2000 (gr-qc/9906055): metric eq. 1 "ds2 = a2(eta)(deta2 - dr2/(1 - Kr2)
    #    - r2 dOmega2)", eq. 4 "Delta(3)Yk(x) = -(k2 - K)Yk(x)", eq. 5 "psi_k'' + (k2 + m2a2 + (xi - 1/6)a2R)psi_k = 0",
    #    eq. 6 "R = 6(a''/a3 + K/a2)". Evaluated independently here on a lumpy a(eta) with analytic a''; agreement is
    #    to roundoff (1e-12 relative).
    def a_l(e):
        return 1.3 + 0.4 * np.tanh(e) + 0.2 * np.exp(-e * e)

    def app_l(e):
        th = np.tanh(e)
        return -0.8 * th * (1 - th * th) + 0.2 * (4 * e * e - 2) * np.exp(-e * e)
    worst = 0.0
    for K, lab in ((1, np.array([1.0, 2, 5])), (-1, np.array([0.0, 0.7, 3.0]))):
        for xi in (0.0, 0.1, 1 / 6, 0.25, 1.0):
            w2 = curved_frw_omega2(K, lab, a_l, 0.8, xi, a_pp=app_l)
            for e in (-1.0, 0.2, 1.5):
                av, ap = float(a_l(e)), float(app_l(e))
                ae = lab ** 2 + 0.64 * av * av + (xi - 1 / 6) * av * av * 6 * (ap / av ** 3 + K / av ** 2)
                worst = max(worst, float(np.max(np.abs(w2(e) / ae - 1))))
    check("omega^2 = Anderson-Eaker eq. 5 with eq. 6 (K = +-1, xi in {0, .1, 1/6, .25, 1}), max rel. diff", worst, 0, 1e-12)
    #    Conformal coupling: omega^2 = n^2 + m^2 a^2 (closed), k^2 + m^2 a^2 (open), even with finite-difference a''.
    wc = curved_frw_omega2(1, [1, 2, 7], a_l, 0.8, 1 / 6)(0.3)
    wo = curved_frw_omega2(-1, [0.0, 2.5], a_l, 0.8, 1 / 6)(0.3)
    m2a2 = 0.64 * float(a_l(0.3)) ** 2
    check("conformal coupling: closed omega^2 = n^2 + m^2 a^2 and open k^2 + m^2 a^2 (max abs diff)",
          max(np.max(np.abs(wc - (np.array([1, 4, 49]) + m2a2))), np.max(np.abs(wo - (np.array([0, 6.25]) + m2a2)))),
          0, 1e-12)
    #    K = 0 reduces to qft_production.frw_omega2 (flat FRW, Birrell & Davies eq. 3.149 form).
    kf = np.array([0.3, 1.1, 2.0])
    check("K = 0: omega^2 identical to qft_production.frw_omega2 (minimal coupling)",
          float(np.max(np.abs(curved_frw_omega2(0, kf, a_l, 0.8, 0.0, a_pp=app_l)(0.4)
                              - qp.frw_omega2(kf, a_l, 0.8, 0.0, a_pp=app_l)(0.4)))), 0, 1e-13)

    # 3. Ricci scalar against exact geometry (no source needed: definitions). Milne a = e^eta, K = -1 is flat
    #    space-time: R = 0. De Sitter has R = 12 H^2 in every slicing: closed a = 1/(H cos eta), open
    #    a = -1/(H sinh eta) (eta < 0), flat a = -1/(H eta). Static closed universe: R = 6/a^2. Tolerance: roundoff.
    H, e = 0.7, -0.4
    sec = 1 / math.cos(e)
    R_vals = [
        ("Milne (a = e^eta, K = -1): R = 0", float(ricci_scalar(math.exp(e), math.exp(e), -1)), 0.0),
        ("closed de Sitter a = sec(eta)/H: R = 12 H^2",
         float(ricci_scalar(sec / H, sec * (2 * sec * sec - 1) / H, 1)), 12 * H * H),
        ("open de Sitter a = -1/(H sinh eta): R = 12 H^2",
         float(ricci_scalar(-1 / (H * math.sinh(e)),
                            -(math.cosh(e) ** 2 + 1) / (H * math.sinh(e) ** 3), -1)), 12 * H * H),
        ("flat de Sitter a = -1/(H eta): R = 12 H^2", float(ricci_scalar(-1 / (H * e), -2 / (H * e ** 3), 0)), 12 * H * H),
        ("static closed universe a = 2: R = 6/a^2", float(ricci_scalar(2.0, 0.0, 1)), 1.5),
    ]
    for name, got, want in R_vals:
        check(name, got, want, 1e-12)

    # 4. Exact null results. Massless conformal field: conformally invariant, omega = n (closed), k (open) for ANY
    #    a(eta) (here the lumpy, non-tanh a); and a static universe (a = const) makes nothing for any xi, m, K.
    #    Threshold 1e-25: about 1e3 above the solver's roundoff floor (qft_production measures 3e-30 .. 7e-28).
    nn = np.arange(1, 9, dtype=float)
    ko = np.array([0.05, 0.5, 1.5, 3.0])
    r0c = curved_frw_particle_production(1, nn, a_l, 0.0, 1 / 6, -30.0, 30.0)
    r0o = curved_frw_particle_production(-1, ko, a_l, 0.0, 1 / 6, -30.0, 30.0)
    check("massless conformal, closed n = 1..8 and open: max |beta|^2 < 1e-25 (any a(eta))",
          float(max(r0c["beta2"].max(), r0o["beta2"].max()) < 1e-25), 1.0, 0)
    r1c = curved_frw_particle_production(1, nn, a_l, 0.5, 0.0, -30.0, 30.0)
    check("same universe, m = 0.5, minimal coupling, closed: production nonzero and resolved (max |beta|^2 > 1e-4)",
          float(r1c["beta2"].max() > 1e-4 and bool(np.all(r1c["resolved"][:4]))), 1.0, 0)
    stat = max(float(curved_frw_particle_production(K, lab, lambda e_: 2.0, 1.0, 0.3, -5.0, 5.0, a_pp=lambda e_: 0.0,
                                                    steps=200)["beta2"].max())
               for K, lab in ((1, nn), (-1, ko)))
    check("static universe a = 2 (K = +-1, xi = 0.3, m = 1): max |beta|^2 < 1e-25", float(stat < 1e-25), 1.0, 0)

    # 5. Tanh universe with conformal coupling: Bernard & Duncan via Birrell & Davies sec. 3.4, quoted from
    #    arXiv:2204.02786: eq. 3.133 "a2(eta) = A + B tanh(rho eta)", eq. 3.140b "|beta_k|2 = sinh2(pi w-/rho) /
    #    sinh(pi w1/rho) sinh(pi w2/rho)". With xi = 1/6 the closed spectrum is k -> n (L = 1): the curvature terms
    #    must cancel exactly. Tolerance 1e-6: the solver's rtol default 1e-7 on beta, doubled for |beta|^2, x5 margin.
    #    rho = 1.5 and n <= 6 keep |beta_n|^2 >= 7e-13, far above the solver's precision floor (~1e-28; at rho = 0.7
    #    the levels n >= 5 fall below it and would be flagged unresolved), and every mode must be resolved.
    a_15, app_15, (s0, s1) = qp.frw_tanh_scale_factor(2.0, 1.0, 1.5)
    nc = np.arange(1, 7, dtype=float)
    rc = curved_frw_particle_production(1, nc, a_15, 1.0, 1 / 6, s0, s1, a_pp=app_15)
    check("closed tanh universe, conformal, n = 1..6: solver vs eq. 3.140b with k -> n, max rel. error (all resolved)",
          float(np.max(np.abs(rc["beta2"] / qp.tanh_model_beta2(nc, 1.0, 2.0, 1.0, 1.5) - 1)))
          + float(not np.all(rc["resolved"])), 0, 1e-6)
    a_t, app_t, (t0, t1) = qp.frw_tanh_scale_factor(2.0, 1.0, 0.7)
    kt = np.linspace(0.05, 3.0, 10)
    rt = curved_frw_particle_production(-1, kt, a_t, 1.0, 1 / 6, t0, t1, a_pp=app_t)
    check("open tanh universe, conformal: solver vs conformal_tanh_beta2 (eq. 3.140b), max rel. error",
          float(np.max(np.abs(rt["beta2"] / conformal_tanh_beta2(-1, kt, 1.0, 2.0, 1.0, 0.7) - 1))), 0, 1e-6)

    # 6. Milne universe (K = -1, L = 1, a = e^eta): Vaudrevange & Kofman 2007 (arXiv:0706.0980) eq. 12, "omega2 =
    #    lambda2 + m2a2", with "mu = ma with a = t = e^eta"; eq. 21 "v_lambda = sqrt(pi/2) 1/sqrt(sinh pi lambda)
    #    J-i lambda(mu)", "Its asymptotic form at eta -> -inf is given by the normalized positive frequency solution
    #    1/sqrt(2 lambda) e^-i lambda eta. This choice of eigenmode corresponds to the conformal vacuum"; eq. 23
    #    "alpha_lambda = e^(pi lambda/2)/sqrt(2 sinh pi lambda), beta_lambda = e^(-pi lambda/2)/sqrt(2 sinh pi lambda)",
    #    so |beta|^2 = e^{-pi k}/(2 sinh pi k) = 1/(e^{2 pi k} - 1), independent of m.
    #    (a) R = 0, so omega^2 must be the same for every xi: tests the K/L^2 and a''/a terms against each other.
    a_m, app_m = milne_scale_factor()
    km = np.array([0.15, 0.3, 0.5])
    e0, e1 = _milne_window(km, 1.0)
    diffs = [float(np.max(np.abs(curved_frw_omega2(-1, km, a_m, 1.0, xi, a_pp=app_m)(ee) / (km ** 2 + math.exp(2 * ee)) - 1)))
             for xi in (0.0, 1 / 6, 0.3, 2.0) for ee in (e0, 0.0, e1)]
    check("Milne: omega^2 = k^2 + m^2 e^(2 eta) for xi = 0, 1/6, 0.3, 2 (R = 0), max rel. diff", max(diffs), 0, 1e-12)
    #    (b) solver vs the exact Bessel solution projected at the same eta1 (mpmath, an independent method). The
    #        tolerance 2e-4 is 4x the measured 5.1e-5 integration error at 2 x 10000 steps (the phase m e^eta1 = 1200
    #        rad needs many steps: the frequency grows like e^eta; 2 x 24000 steps leave 3e-6, the in-end seeding).
    rm = curved_frw_particle_production(-1, km, a_m, 1.0, 0.0, e0, e1, a_pp=app_m, steps=10000, max_steps=20000, rtol=1.0)
    check("Milne, minimal coupling, m = 1: solver vs exact Bessel projection at eta1 (VK eq. 21), max rel. error",
          float(np.max(np.abs(rm["beta2"] / milne_beta2_finite(km, 1.0, e1) - 1))), 0, 2e-4)
    #    (c) the thermal spectrum (VK eq. 23). The zeroth-order out basis at m e^eta1 = 1200 differs from the
    #        eta1 -> inf limit by O(1/(m e^eta1)) in beta (measured 6e-4 .. 2.5e-3 relative in |beta|^2 for k = 0.15..0.6);
    #        tolerance 3e-3 for k <= 0.5.
    check("Milne: solver |beta_k|^2 -> 1/(e^(2 pi k) - 1) (VK eq. 23), max rel. error at m e^eta1 = 1200",
          float(np.max(np.abs(rm["beta2"] / milne_beta2(km) - 1))), 0, 3e-3)
    #    The reference itself: the Bessel projection must approach eq. 23 as c/(m e^eta1); c = 2.3 from the 1.9e-3 at
    #    1200 above, so 2.3e-5 at 1e5 (measured 2.4e-5); tolerance 5e-5 (2x).
    check("Milne: exact Bessel projection at m e^eta1 = 1e5 -> eq. 23 (rel. error O(1/(m e^eta1)))",
          float(np.max(np.abs(milne_beta2_finite(km, 1.0, math.log(1e5)) / milne_beta2(km) - 1))), 0, 5e-5)

    # 7. Large curvature radius -> flat FRW (qft_production), with the O(1/L^2) coefficient predicted: for
    #    xi = 0 the eigenvalue is k^2 - K/L^2 (k = n/L closed), so with f(k^2) = |beta_k|^2 flat,
    #    density(K) = (1/2pi^2) int k^2 f(k^2 - K/L^2) dk = flat + (K/(4 pi^2 L^2)) int_0^inf f dk + O(L^-4)
    #    (integration by parts; the closed sum equals the integral up to exponentially small terms by Poisson
    #    summation, since n^2 f(n^2/L^2 - 1/L^2) is even in n). Minimal coupling, m = 1, tanh universe A = 2, B = 1,
    #    rho = 0.7, L = 20: the O(L^-4) residual measured 0.43% of the coefficient at L = 20 (1.8% at L = 10:
    #    scales as 1/L^2), so the tolerance is 1%.
    kmax, Lc = 4.0, 20.0
    kg, wg = qp._gauss_legendre(0.0, kmax, 32)
    #    rtol = 1e-5 changes the densities by 1e-8 relative (measured against 1e-6), i.e. 3e-7 of the L^-2 term.
    rf = qp.frw_particle_production(kg, a_t, 1.0, 0.0, t0, t1, a_pp=app_t, rtol=1e-5)
    flat = float(np.sum(wg * kg * kg * rf["beta2"])) / (2 * PI * PI)
    coef = float(np.sum(wg * rf["beta2"])) / (4 * PI * PI)
    cl = closed_universe_production(int(kmax * Lc), a_t, 1.0, 0.0, t0, t1, a_pp=app_t, L=Lc, rtol=1e-5)
    op = open_universe_density(kmax, a_t, 1.0, 0.0, t0, t1, a_pp=app_t, L=Lc, nodes=32, rtol=1e-5)
    check("closed, L = 20: (n per comoving volume - flat) L^2 = +(1/4pi^2) int |beta_k|^2 dk",
          (cl["per_comoving_volume"] - flat) * Lc * Lc, coef, 1e-2, rel=True)
    check("open, L = 20: (n per comoving volume - flat) L^2 = -(1/4pi^2) int |beta_k|^2 dk",
          (op["per_comoving_volume"] - flat) * Lc * Lc, -coef, 1e-2, rel=True)

    # 8. Counting. (a) n^2 weighting against a polylog closed form: |beta_n|^2 = x^n gives sum n^2 x^n =
    #    x (1 + x)/(1 - x)^3 (Li_{-2}); tolerance: truncation at N = 200, x^200 ~ 1e-60, so roundoff 1e-13.
    x = math.exp(-1.0)
    nb = np.arange(1, 201, dtype=float)
    tot = closed_universe_totals(nb, x ** nb, L=2.0, a_out=3.0)
    exact = x * (1 + x) / (1 - x) ** 3
    check("closed totals: sum n^2 x^n = x(1+x)/(1-x)^3 (x = 1/e)", tot["particles_total"], exact, 1e-13, rel=True)
    check("real field: pairs = particles/2; per physical volume = N/(2 pi^2 (L a)^3)",
          float(abs(tot["pairs_total"] - exact / 2) < 1e-13 * exact
                and abs(tot["per_physical_volume_out"] - exact / (2 * PI * PI * 6.0 ** 3)) < 1e-13 * exact), 1.0, 0)
    totc = closed_universe_totals(nb, x ** nb, field="complex")
    check("complex field: pairs = particles = antiparticles = sum n^2 |beta_n|^2",
          float(totc["pairs_total"] == totc["particles_total"] == totc["antiparticles_total"]), 1.0, 0)
    #    (b) In-out vacuum persistence of a real field: each real mode is a single-mode squeezed state; truncated
    #        Fock-space exponential of the squeeze generator (independent numerics) gives |<0|S|0>|^2 = 1/cosh r and
    #        <N> = sinh^2 r = |beta|^2. Levels n = 1, 2 (1 + 4 real modes) -> P = (1 + b1)^(-1/2) (1 + b2)^(-2).
    #        Tolerance 1e-10: truncation at 160 quanta leaves a squeezed-amplitude tail ~ tanh(0.6)^80 ~ 3e-22, so only
    #        the roundoff of a 160 x 160 eigendecomposition (measured < 1e-13) remains; 1e-10 is a safe margin.
    r1, r2 = 0.6, 0.3
    p1, n1 = _fock_squeeze_overlap(r1)
    p2, n2 = _fock_squeeze_overlap(r2)
    vp = closed_universe_totals(np.array([1.0, 2.0]), np.array([n1, n2]), tail_tol=1.0)
    check("real-field vacuum persistence of levels n = 1, 2 vs Fock-space squeeze p1 * p2^4",
          vp["vacuum_persistence"], p1 * p2 ** 4, 1e-10, rel=True)
    check("Fock-space mean number sinh^2 r = |beta|^2 (sanity of the squeeze numerics)", n1, math.sinh(r1) ** 2, 1e-10, rel=True)
    check("bosons: -ln P (in-out) < mean pairs (in-in) for the same modes",
          float(-vp["log_vacuum_persistence"] < vp["pairs_total"]), 1.0, 0)

    passed = all(results)
    if verbose:
        print(f"\n{sum(results)}/{len(results)} checks passed")
    return passed


# ---------------------------------------------------------------- convergence studies (slow)
def _convergence() -> int:
    """Slow studies, not part of the self-test: flat limit vs L, Milne vs out time, closed tail vs n_max."""
    a_t, app_t, (t0, t1) = qp.frw_tanh_scale_factor(2.0, 1.0, 0.7)
    kmax = 5.0
    kg, wg = qp._gauss_legendre(0.0, kmax, 48)
    rf = qp.frw_particle_production(kg, a_t, 1.0, 0.0, t0, t1, a_pp=app_t, rtol=1e-7)
    flat = float(np.sum(wg * kg * kg * rf["beta2"])) / (2 * PI * PI)
    coef = float(np.sum(wg * rf["beta2"])) / (4 * PI * PI)
    print(f"Flat limit, minimal coupling, tanh universe A=2 B=1 rho=0.7 m=1: flat n = {flat:.8e} per comoving volume; "
          f"predicted (n_K - n_flat) L^2 -> K x coef, coef = (1/4pi^2) int |beta_k|^2 dk = {coef:.6e}")
    for L in (5.0, 10.0, 20.0, 40.0):
        cl = closed_universe_production(int(kmax * L), a_t, 1.0, 0.0, t0, t1, a_pp=app_t, L=L, rtol=1e-7)
        op = open_universe_density(kmax, a_t, 1.0, 0.0, t0, t1, a_pp=app_t, L=L, nodes=48, rtol=1e-7)
        print(f"  L = {L:5.1f}: closed {cl['per_comoving_volume']:.8e} ({(cl['per_comoving_volume'] - flat) * L * L / coef:.5f}"
              f" x coef), open {op['per_comoving_volume']:.8e} ({(op['per_comoving_volume'] - flat) * L * L / coef:.5f} x coef)")
    print("Milne, m = 1, minimal coupling: solver and exact Bessel projection vs eta1 -> inf (1/(e^{2 pi k} - 1))")
    a_m, app_m = milne_scale_factor()
    km = np.array([0.15, 0.3, 0.5, 0.8])
    for z1, steps in ((1200.0, 8000), (1200.0, 32000), (1e4, 40000)):
        e0, e1 = _milne_window(km, 1.0, z1)
        r = curved_frw_particle_production(-1, km, a_m, 1.0, 0.0, e0, e1, a_pp=app_m, steps=steps, max_steps=2 * steps,
                                           rtol=1.0)
        ex = milne_beta2_finite(km, 1.0, e1)
        fmt = {"float_kind": lambda v: f"{v:+.2e}"}
        print(f"  m e^eta1 = {z1:g}, steps {r['steps']}: solver/exact-at-eta1 - 1 = "
              f"{np.array2string(r['beta2'] / ex - 1, formatter=fmt)}, exact-at-eta1/thermal - 1 = "
              f"{np.array2string(ex / milne_beta2(km) - 1, formatter=fmt)}")
    print("Closed universe tail: particles_total vs n_max (tanh universe, minimal coupling, L = 1, m = 1)")
    for nmax in (4, 6, 8, 12):
        try:
            c = closed_universe_production(nmax, a_t, 1.0, 0.0, t0, t1, a_pp=app_t, tail_tol=1.0)
            print(f"  n_max = {nmax:3d}: N = {c['particles_total']:.10e}, tail fraction {c['tail_fraction']:.2e}")
        except ValueError as exc:
            print(f"  n_max = {nmax}: {exc}")
    return 0


# ---------------------------------------------------------------- command line
def _parse(text: str, kind: str) -> float:
    """A bare number (already in the chosen natural unit) or a quantity with units converted to eV-based natural units.

    kind 'energy': energy -> eV.  kind 'inverse': energy, 1/length or 1/time -> eV.  kind 'length': length or time
    -> 1/eV."""
    try:
        return float(text)
    except ValueError:
        pass
    from unit_tools import DimensionError, Q
    q = Q(text)
    if kind == "energy":
        return q.expect("energy").si / E_CHARGE
    if kind == "inverse":
        if q.dims == Q("1 J").dims:
            return q.si / E_CHARGE
        if q.dims == Q("1/m").dims:
            return q.si * HBAR * C / E_CHARGE
        if q.dims == Q("1/s").dims:
            return q.si * HBAR / E_CHARGE
        raise DimensionError(f"expected an energy, 1/length or 1/time, got {text!r}")
    if q.dims == Q("1 m").dims:
        return length_to_inverse_eV(q.si)
    if q.dims == Q("1 s").dims:
        return q.si * E_CHARGE / HBAR
    raise DimensionError(f"expected a length or time, got {text!r}")


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("selftest")
    tp = sub.add_parser("tanh", help="tanh universe a^2 = A + B tanh(rho eta) with curvature K: per mode and totals")
    tp.add_argument("--K", type=int, required=True, choices=(1, 0, -1))
    tp.add_argument("--m", required=True, help="mass: a number in your natural unit, or e.g. '1 eV'")
    tp.add_argument("--xi", type=float, required=True, help="curvature coupling (1/6 conformal, 0 minimal)")
    tp.add_argument("--A", type=float, required=True)
    tp.add_argument("--B", type=float, required=True)
    tp.add_argument("--rho", required=True, help="inverse conformal time: number, or e.g. '0.7 eV', '1e6 1/m', '1e15 1/s'")
    tp.add_argument("--L", default="1", help="comoving curvature radius: number (1/energy), or e.g. '1e-7 m' (default 1)")
    tp.add_argument("--nmax", type=int, default=None, help="closed: levels n = 1..nmax (default max(12, 10 rho L))")
    tp.add_argument("--kmax", type=float, default=None, help="open/flat: top comoving k (default 10 rho: |beta_k|^2 "
                                                              "falls like e^(-2 pi k/rho))")
    mp_ = sub.add_parser("milne", help="Milne universe (K = -1, a = e^eta): solver vs exact Bessel vs 1/(e^{2 pi k} - 1)")
    mp_.add_argument("--m", type=float, default=1.0, help="mass in units of 1/(comoving curvature radius)")
    mp_.add_argument("--k", type=float, nargs="+", default=[0.2, 0.4])
    mp_.add_argument("--z1", type=float, default=1200.0, help="out end m e^{eta1} (>= 1e3: adiabatic)")
    sub.add_parser("convergence", help="slow: flat limit vs L, Milne vs out time, closed tail vs n_max")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "selftest":
            return 0 if selftest() else 1
        if args.cmd == "convergence":
            return _convergence()
        if args.cmd == "milne":
            k = np.array(args.k, dtype=float)
            e0, e1 = _milne_window(k, args.m, args.z1)
            a_m, app_m = milne_scale_factor()
            steps = int(8 * args.z1)
            r = curved_frw_particle_production(-1, k, a_m, args.m, 0.0, e0, e1, a_pp=app_m, steps=steps,
                                               max_steps=4 * steps)
            ex, th = milne_beta2_finite(k, args.m, e1), milne_beta2(k)
            print(f"Milne universe, m = {args.m:g} (curvature-radius units), window eta in [{e0:.3f}, {e1:.3f}]")
            for i, kk in enumerate(k):
                print(f"  k = {kk:g}: |beta_k|^2 (in-in, conformal vacuum vs adiabatic quanta) solver {r['beta2'][i]:.8e}, "
                      f"exact at eta1 {ex[i]:.8e}, eta1 -> inf 1/(e^(2 pi k) - 1) = {th[i]:.8e}; resolved "
                      f"{bool(r['resolved'][i])}")
            return 0
        m, rho, L = _parse(args.m, "energy"), _parse(args.rho, "inverse"), _parse(args.L, "length")
        a_t, app_t, (t0, t1) = qp.frw_tanh_scale_factor(args.A, args.B, rho)
        a_out = math.sqrt(args.A + args.B)
        print(f"tanh universe K = {args.K:+d}, m = {m:.6g}, xi = {args.xi:g}, a^2 = {args.A:g} + {args.B:g} tanh({rho:.6g} eta), "
              f"L = {L:.6g} (natural units; if the energy unit is eV, L = {inverse_eV_to_length(L):.4g} m); "
              f"physical curvature radius at the end a L = {a_out * L:.6g}")
        if args.K == 1:
            nmax = args.nmax if args.nmax else max(12, int(math.ceil(10 * rho * L)))
            c = closed_universe_production(nmax, a_t, m, args.xi, t0, t1, a_pp=app_t, L=L)
            r = c["modes"]
            for i in range(min(5, nmax)):
                print(f"  level n = {i + 1} (x{(i + 1) ** 2} modes): |beta_n|^2 = {r['beta2'][i]:.6e} per mode, resolved "
                      f"{bool(r['resolved'][i])}")
            if abs(args.xi - 1 / 6) < 1e-9:
                print(f"  conformal closed form for n = 1: {conformal_tanh_beta2(1, [1], m, args.A, args.B, rho, L)[0]:.6e}")
            print(f"total particles in the whole closed universe (in-in mean) {c['particles_total']:.6e}; pairs "
                  f"{c['pairs_total']:.6e}; relative error ~{c['total_relerr']:.1g}; tail {c['tail_fraction']:.1e}")
            print(f"per comoving volume {c['per_comoving_volume']:.6e} energy^3; per physical volume at the end "
                  f"{c['per_physical_volume_out']:.6e} energy^3 (= {qp.density_to_SI(c['per_physical_volume_out']):.4g} m^-3 "
                  f"if the energy unit is eV)")
            print(f"in-out vacuum persistence of the whole universe P = {c['vacuum_persistence']:.6g} "
                  f"(-ln P = {-c['log_vacuum_persistence']:.4e} < mean pairs)")
        else:
            kmax = args.kmax if args.kmax else 10.0 * rho
            o = open_universe_density(kmax, a_t, m, args.xi, t0, t1, a_pp=app_t, L=L, K=args.K)
            name = "open" if args.K == -1 else "flat"
            print(f"{name}: particles per comoving volume (in-in mean) {o['per_comoving_volume']:.6e} energy^3; pairs "
                  f"{o['pairs_per_comoving_volume']:.6e}; per physical volume at the end {o['per_physical_volume_out']:.6e}"
                  f" energy^3 (= {qp.density_to_SI(o['per_physical_volume_out']):.4g} m^-3 if the energy unit is eV); "
                  f"relative error ~{o['total_relerr']:.1g}")
    except (ValueError, KeyError) as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
