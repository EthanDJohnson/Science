#!/usr/bin/env python3
"""qft_thermal: particle production by classical backgrounds when the in-state is THERMAL instead of the
vacuum: stimulated creation for bosons, Pauli blocking for fermions, per mode (exact, through Bogoliubov
coefficients), integrated, and at first order (Born) in spectral form (numpy only, no scipy; imports
qft_production, here qp, for its solvers, closed forms and Born machinery).

Why this tool exists
    qft_production answers "how many particles does the background make from the VACUUM". In a medium the
    in-state already holds particles, and the same Bogoliubov coefficients then give a different answer:
    bosons already present stimulate creation into their own modes, fermions already present block it.
    On top of qp's traps (in-in vs in-out, plane waves vs packets, real production vs transient
    polarisation, vacuum decay vs pair number, particles vs pairs) this module keeps apart:
      * the TOTAL out occupation <N_out(k)>, which includes the thermal particles that were there before,
        versus the NET created number <N_out(k)> - <N_in(k)>;
      * per mode versus per volume;
      * net pair creation (creation minus the stimulated annihilation of pairs already present) versus the
        scattering of medium particles by the background (Landau damping), which moves particles between
        modes without changing their number.
    Every public function has a "Quantity:" line (what is returned: in-in expectation, per mode or per
    volume, particles or pairs, total or net, units) and a "Valid when:" line, and refuses inputs outside
    that range with ValueError.

Units (read this first)
    Natural units hbar = c = 1 (and k_B = 1), Heaviside-Lorentz electromagnetism (e^2 = 4 pi alpha), exactly
    as qft_production: ONE energy unit for energies, masses, momenta, frequencies, temperatures T and chemical
    potentials mu; times in 1/energy; eE in energy^2; numbers per volume in energy^3. This deviates from
    schemas.md's "SI in the Python API" on purpose, like qp; SI helpers convert (temperature_to_eV,
    temperature_from_eV here; qp's energy_to_eV, time_to_inverse_eV, density_to_SI, eE_from_field_SI), and the
    command line accepts units through unit_tools.Q ("1e10 K", "0.511 MeV", "3e17 V/m", "1e-20 s").

The thermal in-state
    The grand-canonical ensemble of the FREE in-Hamiltonian (the field before the background acts),
    rho_in = exp(-(H_in - mu Q)/T)/Z: diagonal in the in-Fock basis, no anomalous correlations (<a_k b_-k> = 0).
    Particles (charge +1) in mode k and antiparticles in mode -k (both with the in-energy omega_in(k)) hold
        bosons    n_+(k) = 1/(e^{(omega_in - mu)/T} - 1),   n_-(-k) = 1/(e^{(omega_in + mu)/T} - 1)
        fermions  n_+(k) = 1/(e^{(omega_in - mu)/T} + 1),   n_-(-k) = 1/(e^{(omega_in + mu)/T} + 1).
    A real field carries no charge: mu = 0 and n_+ = n_- = n (it is its own antiparticle). Bosons need
    |mu| < omega_in for every mode (|mu| < m): otherwise the occupations diverge (condensation), which is
    refused. The medium is free: no thermal masses or collisional widths, and it does not re-equilibrate while
    the background acts. Temperatures and momenta are those of the frame in which the medium is at rest.

PART A. Exact per-mode result for a homogeneous background (no mode mixing)
--------------------------------------------------------------------------
    The background mixes particle k with antiparticle -k only:
        bosons    a_out(k) = alpha a_in(k) + beta* b_in^dag(-k),   |alpha|^2 - |beta|^2 = 1,
        fermions  a_out(k) = alpha a_in(k) + beta* b_in^dag(-k),   |alpha|^2 + |beta|^2 = 1   (phases: convention).
    The thermal in-in expectation (cross terms <a b> vanish) gives, with the upper sign for bosons:
        <N_out(k)> = |alpha|^2 n_+ + |beta|^2 (1 +- n_-) = n_+(k) + |beta_k|^2 (1 +- n_+(k) +- n_-(-k)),
    and the same for the antiparticles in -k with n_+ <-> n_- in the first term (charge is conserved, so the net
    change is the same for both). The NET created number per mode, = pairs created in the mode pair (k, -k):
        Delta N(k) = |beta_k|^2 (1 +- n_+(k) +- n_-(-k))   (bosons: stimulated; fermions: Pauli-blocked),
    the vacuum value |beta_k|^2 of qp times a thermal factor; at mu = 0 the factor is coth(omega_in/2T) (bosons)
    or tanh(omega_in/2T) (fermions): Kim, Lee & Yoon 2009 (arXiv:0811.0349) eqs. 18 and 20. Thermal fermions have
    n_+ + n_- < 1 for every mu (omega_in > 0), so they always net-create; only an inverted, non-thermal population
    net-annihilates. Real field: n_+ = n_- = n and Delta N(k) = |beta_k|^2 (1 + 2n); each created pair puts one
    particle in k and one in -k, so after summing over modes pairs = particles/2. Equivalently
    (n_out + 1/2) = (n + 1/2)(1 + 2|beta|^2): the symmetric (Wigner) occupation is amplified exactly like a
    classical action, so a random-phase classical ensemble (n >> 1) has <J_out>/<J_in> = 1 + 2|beta|^2 (the
    self-test checks this by Monte Carlo). |beta_k|^2 comes from qp: closed forms (tanh_model_beta2,
    sauter_n_scalar, sauter_n_spinor, schwinger_n_mode) or the solvers (bogoliubov_boson,
    bogoliubov_fermion_efield, frw_particle_production).

PART B. Electric field at finite temperature (mode level)
---------------------------------------------------------
    Sauter pulse E0 sech^2(t/tau): exact |beta_k|^2 from qp (Gavrilov & Gitman 1996 eqs. 42-43), in-energy
    omega_in = sqrt(m^2 + k_perp^2 + (k_par - eE0 tau)^2) (kinetic momentum before the pulse; the same for the
    particle in k and the antiparticle in -k), thermal factor as in Part A; integrated, the net pairs per volume
    g int d^3k/(2pi)^3 |beta_k|^2 (1 +- n_+ +- n_-) (Kim, Lee & Yoon 2009 eqs. 22-23 at mu = 0). A mode that sweeps
    through p = 0 in a long pulse has |beta|^2 -> exp(-pi eps_perp^2/eE) (Landau-Zener), times the same factor.
    NOT implemented: a thermal correction to the CONSTANT-field Schwinger rate. A constant field has no in-region
    in which to prepare a thermal state, and the thermal effective-action results disagree (Kim, Lee & Yoon 2009
    review it; Medina & Ogilvie 2017: the one-loop thermal correction "has proved difficult to calculate
    unambiguously"). Only the mode-level statement for a pulse with a thermal in-region is made here.

PART C. Spatially flat FRW (real scalar, conformal time eta, chi = a phi, k comoving)
------------------------------------------------------------------------------------
    In a static in-region (a = a_in) the thermal state at PHYSICAL temperature T_in has, per comoving mode,
    n_in(k) = 1/(e^{omega_in(k)/(a_in T_in)} - 1), omega_in = sqrt(k^2 + m^2 a_in^2) the conformal frequency
    (physical energy omega/a). Out: n_out(k) = n_in(k) + |beta_k|^2 (1 + 2 n_in(k)). Massless and conformally
    coupled (xi = 1/6): beta = 0 for every a(eta) (Parker 1969), so n_out(k) = n_in(k) = 1/(e^{p/T_out} - 1), p = k/a_out
    the physical momentum and T_out = T_in a_in/a_out: the Planck spectrum survives, redshifted. Otherwise the out
    spectrum is not thermal; frw_thermal_production returns T_eff(k) = E_out/ln(1 + 1/n_out) per mode, which is the
    same for all k only when the spectrum is thermal.

PART D. First order (Born, in-in) at finite temperature, spectral form
----------------------------------------------------------------------
    Vacuum (qp Part D): N_pairs = int d^4K/(2pi)^4 theta(K0) |V~(K)|^2 rho(s), s = K^2. In a thermal medium the
    background, at second order in V, (1) creates pairs with the statistical factor (1 +- n1)(1 +- n2); (2)
    annihilates pairs already present, n1 n2; (3) scatters a medium particle p1 -> p2 = p1 + K, n1 (1 +- n2),
    which needs K^2 = (p2 - p1)^2 <= 0 (spacelike: Landau damping) and changes no particle number. For a
    Fock-diagonal in-state, Delta<N> = sum_i p_i sum_f |<f|S1|i>|^2 (N_f - N_i) holds exactly at O(V^2) (the
    O(V^2) part of <i|S|i> multiplies N_i - N_i = 0), so the in-in NET change of the pair number is
        N_pairs(T) = int d^4K/(2pi)^4 theta(K0) |V~(K)|^2 rho(s) W(K),
        W = <(1 +- n1)(1 +- n2) - n1 n2> = <1 +- n1 +- n2> = (1 - e^{-K0/T}) <(1 +- n1)(1 +- n2)>
    (phase-space average at fixed K; the last form is detailed balance: the net yield is the thermal spectral
    function, the commutator, not the Wightman function). This IS the right in-in quantity for a classical
    background: the net change of the number. For a homogeneous V(t), K = (Omega, 0), each particle has Omega/2 and
    W = 1 +- n_+(Omega/2) +- n_-(Omega/2): exactly the first-order expansion of Part A (the self-test checks this
    against the exact mode solvers at finite T). For a vertex whose |M|^2 depends on s only (scalar V phi^2,
    V |phi|^2; Yukawa V psibar psi) the decay is isotropic in the pair rest frame, so the medium-frame energy E1 is
    UNIFORM on [E-, E+], E+- = (K0 +- kappa b)/2 (kappa = |K|, b = sqrt(1 - 4m^2/s)), and
        <n>_Bose  = (T/(kappa b)) ln[(1 - e^{-(E+ - mu)/T}) / (1 - e^{-(E- - mu)/T})],
        <n>_Fermi = (T/(kappa b)) ln[(1 + e^{-(E- - mu)/T}) / (1 + e^{-(E+ - mu)/T})]      (-> n(K0/2) as kappa -> 0).
    Spectral densities per PAIR: real scalar b/(16 pi) and complex scalar b/(8 pi) (qp); Dirac pairs through
    L = -V psibar psi: sum_spins |ubar(p1) v(p2)|^2 = 4(p1.p2 - m^2) = 2(s - 4m^2), so rho_psi = s b^3/(4 pi).
    Plane waves still make no pairs (null support), but at finite T a background with spacelike support also
    scatters medium particles; that changes momenta and energy, not numbers, and is not computed.

Assumptions and validity range
    Free fields in a prescribed classical background (no back-reaction, no interactions in the medium); adiabatic
    in and out regions; the thermal state is prepared in the in-region of the free field and is Fock-diagonal.
    Numbers between the ends are not computed (basis-dependent there). Born: first order in V, as in qp.

Python usage
    import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
    import numpy as np, qft_production as qp, qft_thermal as th
    k = np.linspace(0.1, 3, 30)                                     # units of m
    b2 = qp.tanh_model_beta2(k, 1.0, 2.0, 1.0, 0.5)                  # vacuum |beta_k|^2 (closed form)
    r = th.thermal_mode_production(b2, np.sqrt(k**2 + 1.0), T=0.5)   # r["net_created"], r["particles_out"]
    th.sauter_thermal_mode(0.0, 0.3, 1.0, 0.5, 2.0, T=0.8)["thermal_factor"]   # tanh(omega_in/2T), Pauli blocking
    th.born_scalar_homogeneous_thermal(lambda t: 0.05 * np.exp(-t**2 / 0.18), -4.0, 4.0, 1.0, 30.0, T=1.0)
    th.thermal_pair_weight(5.0, 2.0, 1.0, T=1.0)                     # <1 + n1 + n2> at K0 = 5, |K| = 2

Command line (from the project root)
    python3 .claude/skills/conundrum/scripts/qft_thermal.py selftest
    python3 .claude/skills/conundrum/scripts/qft_thermal.py mode --beta2 0.01 --omega "0.6 MeV" --T "5e9 K" --fermion
    python3 .claude/skills/conundrum/scripts/qft_thermal.py sauter --E "1e18 V/m" --tau "1e-21 s" --T "3e9 K"
    python3 .claude/skills/conundrum/scripts/qft_thermal.py convergence      (slow: Born-vs-exact and Monte Carlo studies)
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

import qft_production as qp  # noqa: E402  (mode solvers, closed forms, Born machinery, SI helpers)
from unit_tools import E_CHARGE, K_B  # noqa: E402  (CODATA values shared by the toolkit)

PI = math.pi


# ---------------------------------------------------------------- SI helpers
def temperature_to_eV(T_kelvin: float) -> float:
    """Convert a temperature in K to the natural-unit energy k_B T in eV.

    Quantity: k_B T in eV (the temperature in the natural units of this module when the energy unit is eV).
    Valid when: T_kelvin >= 0 (a temperature in kelvin)."""
    T = float(T_kelvin)
    if not (math.isfinite(T) and T >= 0):
        raise ValueError("temperature must be finite and >= 0 K")
    return T * K_B / E_CHARGE


def temperature_from_eV(T_eV: float) -> float:
    """Convert a natural-unit temperature k_B T in eV to kelvin.

    Quantity: temperature in K.
    Valid when: T_eV >= 0 (an energy k_B T in eV)."""
    T = float(T_eV)
    if not (math.isfinite(T) and T >= 0):
        raise ValueError("temperature must be finite and >= 0")
    return T * E_CHARGE / K_B


# ---------------------------------------------------------------- input checks and occupations
def _temperature(T) -> float:
    T = float(T)
    if not (math.isfinite(T) and T >= 0):
        raise ValueError("need a finite temperature T >= 0 (same energy unit as omega)")
    return T


def _sign(statistics: str) -> float:
    if statistics == "boson":
        return 1.0
    if statistics == "fermion":
        return -1.0
    raise ValueError("statistics must be 'boson' or 'fermion'")


def _field_mu(field: str, statistics: str, mu: float) -> float:
    if field not in ("real", "complex"):
        raise ValueError("field must be 'real' or 'complex'")
    mu = float(mu)
    if not math.isfinite(mu):
        raise ValueError("mu must be finite")
    if field == "real":
        if statistics != "boson":
            raise ValueError("a real (Majorana) fermion field is not covered: use field='complex' (Dirac)")
        if mu != 0:
            raise ValueError("a real field carries no conserved charge: mu must be 0")
    return mu


def bose_einstein(omega, T: float, mu: float = 0.0):
    """Bose-Einstein occupation n = 1/(exp((omega - mu)/T) - 1) of a free mode of energy omega.

    Quantity: mean number of bosons per mode in the grand-canonical thermal state (dimensionless; T = 0 gives 0).
    Valid when: T >= 0 and omega > mu for every entry (otherwise the occupation diverges or is negative:
        condensation, refused); omega, T, mu in one energy unit."""
    w = qp._arr(omega, "omega")
    T = _temperature(T)
    mu = float(mu)
    if not math.isfinite(mu) or np.any(w - mu <= 0):
        raise ValueError("Bose-Einstein occupation needs omega > mu for every mode (no condensate)")
    if T == 0:
        return np.zeros_like(w)
    return 1.0 / np.expm1((w - mu) / T)


def fermi_dirac(omega, T: float, mu: float = 0.0):
    """Fermi-Dirac occupation n = 1/(exp((omega - mu)/T) + 1) of a free mode of energy omega.

    Quantity: mean number of fermions per mode (per spin state) in the grand-canonical thermal state
        (dimensionless, 0 <= n <= 1; T = 0 gives the step theta(mu - omega), 1/2 at omega = mu).
    Valid when: T >= 0, any real mu; omega, T, mu in one energy unit."""
    w = qp._arr(omega, "omega")
    T = _temperature(T)
    mu = float(mu)
    if not math.isfinite(mu):
        raise ValueError("mu must be finite")
    if T == 0:
        return np.where(w < mu, 1.0, np.where(w == mu, 0.5, 0.0))
    return np.exp(-np.logaddexp(0.0, (w - mu) / T))


def _occupation(omega, T, mu, sign):
    return bose_einstein(omega, T, mu) if sign > 0 else fermi_dirac(omega, T, mu)


def thermal_in_occupations(omega_in, T: float, mu: float = 0.0, statistics: str = "boson",
                           field: str = "complex") -> dict:
    """Occupations of the thermal in-state: particles in mode k and antiparticles in mode -k.

    Quantity: dict with 'particles' n_+(k) (charge +1, chemical potential mu) and 'antiparticles' n_-(-k)
        (chemical potential -mu), mean numbers per mode (per spin state for fermions) in the grand-canonical
        ensemble of the free in-Hamiltonian, dimensionless. Real field: both entries are n(omega_in), the
        occupations of modes k and -k of the same field.
    Valid when: T >= 0; statistics 'boson' or 'fermion'; field 'real' (bosons, mu = 0) or 'complex'; bosons need
        omega_in > |mu|; omega_in is the energy of the mode in the in-region (same for k and -k)."""
    s = _sign(statistics)
    mu = _field_mu(field, statistics, mu)
    w = qp._positive(omega_in, "omega_in")
    return {"particles": _occupation(w, T, mu, s), "antiparticles": _occupation(w, T, -mu, s)}


# ---------------------------------------------------------------- Part A: exact per-mode result
def out_occupation(beta2, n_particle, n_antiparticle, statistics: str = "boson") -> dict:
    """Out occupations of the mode pair (k, -k) for a Fock-diagonal in-state with given occupations.

    Bosons:   N_out(k) = n_+ + |beta|^2 (1 + n_+ + n_-),  fermions: N_out(k) = n_+ + |beta|^2 (1 - n_+ - n_-),
    with n_+ = <N_in(k)> (particles) and n_- = <N_in(-k)> (antiparticles; for a real field the occupation of mode -k).
    Quantity: dict, per mode pair, of IN-IN expectations (dimensionless): 'particles_out' = <N_out(k)> (TOTAL, with
        the particles that were already there), 'antiparticles_out' = <N_out(-k)>, 'net_created' = <N_out(k)> -
        <N_in(k)> = |beta|^2 (1 +- n_+ +- n_-) (= net antiparticles created in -k = net pairs in the mode pair),
        'vacuum' = |beta|^2 (the T = 0 value), 'medium' = net_created - vacuum (stimulated > 0, blocked < 0) and
        'factor' = 1 +- n_+ +- n_-.
    Valid when: homogeneous background (k mixes only with -k); in-state diagonal in the in-Fock basis (thermal or
        any mixture of number states; no <a b> correlations); |beta|^2 >= 0 (<= 1 for fermions); occupations
        >= 0 (<= 1 for fermions)."""
    sg = _sign(statistics)
    b2 = qp._arr(beta2, "beta2")
    na, nb = qp._arr(n_particle, "n_particle"), qp._arr(n_antiparticle, "n_antiparticle")
    if np.any(b2 < 0) or np.any(na < 0) or np.any(nb < 0):
        raise ValueError("|beta|^2 and occupations must be >= 0")
    if sg < 0 and (np.any(b2 > 1) or np.any(na > 1) or np.any(nb > 1)):
        raise ValueError("fermions: |beta|^2 <= 1 and occupations <= 1 (Pauli)")
    fac = 1.0 + sg * (na + nb)
    net = b2 * fac
    return {"particles_out": na + net, "antiparticles_out": nb + net, "net_created": net, "vacuum": b2 * np.ones_like(net),
            "medium": net - b2, "factor": fac}


def thermal_mode_production(beta2, omega_in, T: float, mu: float = 0.0, statistics: str = "boson",
                            field: str = "complex") -> dict:
    """Per-mode production from a THERMAL in-state: out_occupation with thermal_in_occupations.

    Quantity: dict of per-mode IN-IN expectations (dimensionless, per spin state for fermions): 'net_created' =
        |beta_k|^2 (1 +- n_+ +- n_-) (net particles created in k = net antiparticles in -k = net pairs in the mode
        pair; for a real field the pair occupies k and -k), 'particles_out' (TOTAL <N_out(k)>, thermal particles
        included), 'antiparticles_out', 'vacuum' (|beta_k|^2), 'medium', 'factor' (= coth(omega/2T) for bosons,
        tanh(omega/2T) for fermions at mu = 0), and the in-occupations 'n_particles', 'n_antiparticles'.
    Valid when: as out_occupation and thermal_in_occupations; beta2 is the VACUUM |beta_k|^2 of the same mode
        (from qp), omega_in its energy in the in-region; same energy unit for omega_in, T and mu."""
    occ = thermal_in_occupations(omega_in, T, mu, statistics, field)
    out = out_occupation(beta2, occ["particles"], occ["antiparticles"], statistics)
    out.update(n_particles=occ["particles"], n_antiparticles=occ["antiparticles"])
    return out


def thermal_number_density(beta2_of_k, omega_in_of_k, T: float, kmax: float, mu: float = 0.0,
                           statistics: str = "boson", field: str = "complex", g: float = 1.0, n: int = 64,
                           kmin: float = 0.0) -> dict:
    """Integrated thermal production for an isotropic spectrum: g/(2 pi^2) int k^2 (...) dk by Gauss-Legendre.

    Quantity: dict of numbers PER UNIT VOLUME (energy^3; comoving volume in FRW), in-in, summed over g internal
        states: 'net_particles_per_volume' = g/(2pi^2) int k^2 |beta_k|^2 (1 +- n_+ +- n_-) dk (NET particles created;
        for a complex field equal to the net antiparticles and to the net PAIRS; for a real field pairs =
        particles/2), 'pairs_per_volume' (net), 'vacuum_pairs_per_volume' (same at T = 0), 'in_particles_per_volume'
        (thermal particles present before, within [kmin, kmax]) and 'out_particles_per_volume' (in + net).
    Valid when: omega and |beta_k|^2 depend on |k| only (homogeneous, isotropic background); beta2_of_k(k) returns
        the VACUUM |beta_k|^2 and omega_in_of_k(k) the in-energy; integrands negligible beyond kmax (check by
        raising kmax: thermal occupations fall like exp(-omega/T)); 0 <= kmin < kmax; n >= 4; other conditions as
        thermal_mode_production."""
    if not (0 <= kmin < kmax) or not math.isfinite(kmax):
        raise ValueError("need 0 <= kmin < kmax < inf")
    if n < 4 or not g > 0:
        raise ValueError("need n >= 4 nodes and g > 0")
    k, w = qp._gauss_legendre(kmin, kmax, n)
    r = thermal_mode_production(np.asarray(beta2_of_k(k), dtype=float), np.asarray(omega_in_of_k(k), dtype=float),
                                T, mu, statistics, field)
    pref = g / (2 * PI * PI)
    net = pref * float(np.sum(w * k * k * r["net_created"]))
    vac = pref * float(np.sum(w * k * k * r["vacuum"]))
    nin = pref * float(np.sum(w * k * k * r["n_particles"]))
    half = 0.5 if field == "real" else 1.0
    return {"net_particles_per_volume": net, "pairs_per_volume": half * net, "vacuum_pairs_per_volume": half * vac,
            "in_particles_per_volume": nin, "out_particles_per_volume": nin + net}


# ---------------------------------------------------------------- Part B: electric field (Sauter) at finite T
def sauter_thermal_mode(k_par, k_perp, m: float, eE0: float, tau: float, T: float, mu: float = 0.0,
                        fermion: bool = True) -> dict:
    """Pair production by the Sauter pulse E0 sech^2(t/tau) from a thermal in-state of charged particles, per mode.

    Vacuum |beta_k|^2: qp.sauter_n_spinor / sauter_n_scalar (exact); in-energy omega_in = sqrt(m^2 + k_perp^2 +
    (k_par - eE0 tau)^2) (kinetic momentum before the pulse, k = canonical momentum).
    Quantity: dict as thermal_mode_production, per mode k (per spin state for spinor QED; scalar QED is a complex
        field), in-in: 'net_created' = net pairs created in the mode pair (electron k, positron -k), 'particles_out'
        the TOTAL electrons in k, ..., plus 'omega_in' and 'thermal_factor' (= 'factor': coth(omega_in/2T) scalar,
        tanh(omega_in/2T) spinor at mu = 0; Kim, Lee & Yoon 2009 eqs. 18, 20).
    Valid when: as qp.sauter_n_* (homogeneous pulse, m^2 + k_perp^2 > 0, eE0 > 0, tau > 0); the thermal state is
        prepared before the pulse (in-region, free field); T >= 0; scalar QED needs |mu| < omega_in."""
    nvac = qp.sauter_n_spinor(k_par, k_perp, m, eE0, tau) if fermion else qp.sauter_n_scalar(k_par, k_perp, m, eE0, tau)
    k_par, k_perp = qp._arr(k_par, "k_par"), qp._arr(k_perp, "k_perp")
    w_in = np.sqrt(m * m + k_perp ** 2 + (k_par - eE0 * tau) ** 2)
    r = thermal_mode_production(nvac, w_in, T, mu, "fermion" if fermion else "boson", "complex")
    r.update(omega_in=w_in, thermal_factor=r["factor"])
    return r


def sauter_thermal_pairs_per_volume(m: float, eE0: float, tau: float, T: float, mu: float = 0.0,
                                    fermion: bool = True, n: int = 96) -> dict:
    """Net pairs per unit volume made by a Sauter pulse from a thermal in-state: g int d^3k/(2pi)^3 Delta N(k).

    Same quadrature as qp.sauter_pairs_per_volume (|k_par| <= eE0 tau + R, k_perp <= R, R = 12 (sqrt(eE0) + m + 1/tau)).
    Quantity: dict with 'pairs_per_volume' (NET mean number of PAIRS created per unit volume, energy^3, in-in; g = 2
        spin states for spinor QED, 1 for scalar QED; thermal particles already present are NOT counted),
        'vacuum_pairs_per_volume' (the same at T = 0, = qp.sauter_pairs_per_volume) and 'thermal_factor' (ratio).
    Valid when: as sauter_thermal_mode with m > 0; scalar QED needs |mu| < m; check convergence by changing n."""
    m = float(qp._positive(m, "m"))
    eE0, tau = float(qp._positive(eE0, "eE0")), float(qp._positive(tau, "tau"))
    if not fermion and abs(mu) >= m:
        raise ValueError("scalar QED in-state needs |mu| < m (no condensate)")
    reach = 12.0 * (math.sqrt(eE0) + m + 1.0 / tau)
    kz, wz = qp._gauss_legendre(-eE0 * tau - reach, eE0 * tau + reach, n)
    kp, wp = qp._gauss_legendre(0.0, reach, n)
    KZ, KP = np.meshgrid(kz, kp, indexing="ij")
    r = sauter_thermal_mode(KZ, KP, m, eE0, tau, T, mu, fermion)
    g = 2.0 if fermion else 1.0
    net = float(g * np.einsum("i,j,ij->", wz, wp * kp, r["net_created"]) / (4 * PI * PI))
    vac = float(g * np.einsum("i,j,ij->", wz, wp * kp, r["vacuum"]) / (4 * PI * PI))
    return {"pairs_per_volume": net, "vacuum_pairs_per_volume": vac, "thermal_factor": net / vac if vac > 0 else float("nan")}


# ---------------------------------------------------------------- Part C: FRW
def frw_redshifted_temperature(T_in: float, a_in: float, a_out: float) -> float:
    """Temperature of a thermal gas of massless, conformally coupled quanta after the universe expands a_in -> a_out.

    Quantity: physical temperature T_out = T_in a_in/a_out (same unit as T_in); the occupation of every comoving
        mode is unchanged, so the spectrum stays exactly Planckian (no particles created: Parker 1969).
    Valid when: free massless field with conformally invariant equation (scalar with xi = 1/6, photons, massless
        fermions), spatially flat FRW, T_in >= 0, a_in, a_out > 0."""
    T_in = _temperature(T_in)
    a_in, a_out = float(qp._positive(a_in, "a_in")), float(qp._positive(a_out, "a_out"))
    return T_in * a_in / a_out


def frw_thermal_production(k, a, m: float, xi: float, eta0: float, eta1: float, T_in: float, a_pp=None,
                           **solver) -> dict:
    """Real scalar in flat FRW starting in a thermal state at physical temperature T_in in the static in-region.

    Runs qp.frw_particle_production (keyword arguments go to the solver), then n_in(k) = 1/(exp(omega_in/(a_in T_in)) - 1)
    and n_out = n_in + |beta_k|^2 (1 + 2 n_in) (real field: n(k) = n(-k)).
    Quantity: dict of per-COMOVING-mode in-in expectations (dimensionless): 'n_in', 'n_out' (TOTAL out occupation),
        'net_created' (= |beta_k|^2 (1 + 2 n_in): net particles in mode k; pairs = particles/2 after summing modes),
        'beta2' (vacuum value) with the solver's 'floor' and 'resolved'; 'E_out' (physical out energy omega_out/a_out),
        'T_eff' (physical temperature a Bose-Einstein spectrum would need at each k, E_out/ln(1 + 1/n_out); 0 where
        n_out = 0) and 'T_redshifted' = T_in a_in/a_out. The spectrum is thermal only if T_eff is the same for all k.
    Valid when: as qp.frw_particle_production (a static at both ends, omega^2 > 0 and adiabatic there); T_in >= 0 in
        the energy unit of k/a (physical); real scalar, mu = 0."""
    T_in = _temperature(T_in)
    r = qp.frw_particle_production(k, a, m, xi, eta0, eta1, a_pp=a_pp, **solver)
    a_in, a_out = float(a(eta0)), float(a(eta1))
    n_in = bose_einstein(r["omega_in"], a_in * T_in)
    out = out_occupation(r["beta2"], n_in, n_in, "boson")
    E_out = r["omega_out"] / a_out
    with np.errstate(divide="ignore"):
        T_eff = np.where(out["particles_out"] > 0, E_out / np.log1p(1.0 / np.where(out["particles_out"] > 0,
                                                                                      out["particles_out"], 1.0)), 0.0)
    return {"n_in": n_in, "n_out": out["particles_out"], "net_created": out["net_created"], "beta2": r["beta2"],
            "floor": r["floor"], "resolved": r["resolved"], "E_out": E_out, "T_eff": T_eff,
            "T_redshifted": T_in * a_in / a_out, "a_in": a_in, "a_out": a_out}


# ---------------------------------------------------------------- Part D: Born at finite temperature
def _log1mexp(y):
    """ln(1 - e^{-y}) for y > 0, accurate at both ends (Maechler's switch at y = ln 2)."""
    y = np.asarray(y, dtype=float)
    small = y <= math.log(2.0)
    return np.where(small, np.log(-np.expm1(-np.where(small, y, 1.0))), np.log1p(-np.exp(-np.where(small, 1.0, y))))


def _avg_occupation(Em, Ep, T, mu, sign):
    """Average of the Bose (sign > 0) or Fermi occupation at chemical potential mu over E uniform on [Em, Ep]."""
    D = Ep - Em
    if T == 0:
        if sign > 0:
            return np.zeros_like(Em)
        with np.errstate(divide="ignore", invalid="ignore"):
            frac = (np.clip(mu - Em, 0, None) - np.clip(mu - Ep, 0, None)) / np.where(D > 0, D, 1.0)
        return np.where(D > 0, frac, np.where(0.5 * (Em + Ep) < mu, 1.0, np.where(0.5 * (Em + Ep) == mu, 0.5, 0.0)))
    out = np.empty_like(Em)
    small = D < 0.05 * T
    if np.any(small):     # 8-point Gauss-Legendre average: error ~ (D/T)^16, below 1e-20 here
        x, w = np.polynomial.legendre.leggauss(8)
        E = 0.5 * (Em[small] + Ep[small])[..., None] + 0.5 * D[small][..., None] * x
        y = (E - mu) / T
        nn = 1.0 / np.expm1(y) if sign > 0 else np.exp(-np.logaddexp(0.0, y))
        out[small] = 0.5 * np.sum(w * nn, axis=-1)
    big = ~small
    if np.any(big):
        ym, yp, Db = (Em[big] - mu) / T, (Ep[big] - mu) / T, D[big]
        if sign > 0:
            out[big] = T / Db * (_log1mexp(yp) - _log1mexp(ym))
        else:
            out[big] = T / Db * (np.logaddexp(0.0, -ym) - np.logaddexp(0.0, -yp))
    return out


def thermal_pair_weight(K0, kappa, m: float, T: float, mu: float = 0.0, statistics: str = "boson"):
    """Net-creation weight W = <1 +- n_+(E1) +- n_-(E2)> over the two-body phase space of a pair with momentum K.

    For a vertex whose |M|^2 depends only on s = K0^2 - kappa^2 the pair decays isotropically in its rest frame, so
    in the medium frame E1 is uniform on [E-, E+], E+- = (K0 +- kappa b)/2, b = sqrt(1 - 4m^2/s), and so is E2 = K0 - E1;
    the average is done in closed form (logs) or, for kappa b < 0.05 T, by 8-point Gauss-Legendre.
    Quantity: dimensionless weight W(K) multiplying the vacuum two-particle spectral density to give the NET (created
        minus annihilated, in-in) pair yield in a thermal medium; W = (1 - e^{-K0/T}) <(1 +- n1)(1 +- n2)>; 1 at T = 0
        (bosons, or fermions with mu = 0).
    Valid when: K timelike above threshold (K0 > kappa >= 0, s >= 4m^2; s > 0 if m = 0); T >= 0; K and T in the medium
        rest frame; vertex with |M|^2 = f(s) only (scalar V phi^2, V|phi|^2, Yukawa V psibar psi; NOT the gravity or
        vector vertex); bosons need |mu| < m (mu = 0 if m = 0); n_+ at +mu, n_- at -mu."""
    sg = _sign(statistics)
    T = _temperature(T)
    K0, kap = np.broadcast_arrays(qp._arr(K0, "K0"), qp._arr(kappa, "kappa"))
    K0, kap = K0.astype(float), kap.astype(float)
    m, mu = float(m), float(mu)
    if m < 0 or not math.isfinite(mu):
        raise ValueError("need m >= 0 and finite mu")
    if sg > 0 and (abs(mu) >= m and mu != 0):
        raise ValueError("bosons need |mu| < m (no condensate)")
    s = K0 * K0 - kap * kap
    if np.any(kap < 0) or np.any(K0 <= 0) or np.any(s <= 0) or np.any(s < 4 * m * m * (1 - 1e-12)):
        raise ValueError("need K timelike above threshold: K0 > kappa >= 0, s = K0^2 - kappa^2 >= 4 m^2 (> 0)")
    b = np.sqrt(np.clip(1.0 - 4 * m * m / s, 0.0, None))
    D = kap * b
    Em, Ep = 0.5 * (K0 - D), 0.5 * (K0 + D)
    if sg > 0 and T > 0 and np.any(Em - abs(mu) <= 0):
        raise ValueError("Bose occupations diverge at E- <= |mu| (massless pair on the light cone): need s > 0 strictly")
    return 1.0 + sg * (_avg_occupation(Em, Ep, T, mu, sg) + _avg_occupation(Em, Ep, T, -mu, sg))


def pair_spectral_density_yukawa(s, m: float):
    """Two-particle spectral density of psibar psi for Dirac pairs (the Yukawa vertex L = -V psibar psi).

    rho_psi(s) = sum_spins |ubar(p1) v(p2)|^2 x two-body phase space = 2 (s - 4m^2) x b/(8 pi) = s b^3/(4 pi),
    b = sqrt(1 - 4m^2/s) (particle and antiparticle are distinct: no identical-particle 1/2).
    Quantity: rho_psi(s) in energy^2, per PAIR (electron + positron, spins summed); the Born yield is N_pairs =
        int d^4K/(2pi)^4 theta(K0) |V~(K)|^2 rho_psi(K^2) (mean number of PAIRS = electrons = positrons).
    Valid when: s real; m >= 0; zero for s <= 4m^2 (it vanishes like s on the light cone when m = 0)."""
    s = qp._arr(s, "s")
    m = float(m)
    if m < 0:
        raise ValueError("m must be >= 0")
    th = 4 * m * m
    with np.errstate(divide="ignore", invalid="ignore"):
        b = np.where(s > th, np.sqrt(np.clip(1 - th / np.where(s > 0, s, 1.0), 0, None)), 0.0)
    return np.where(s > th, s, 0.0) * b ** 3 / (4 * PI)


def _thermal_born_checks(m, T, field, mu, statistics):
    T = _temperature(T)
    mu = _field_mu(field, statistics, mu)
    if statistics == "boson" and (mu != 0 and abs(mu) >= m):
        raise ValueError("bosons need |mu| < m (no condensate)")
    if statistics == "boson" and T > 0 and m <= 0:
        raise ValueError("thermal massless bosons: the stimulated factor ~ 4T/Omega makes the yield infrared-"
                         "sensitive; give m > 0 (or use born_scalar_general_thermal with s_min > 0)")
    return T, mu


def born_scalar_homogeneous_thermal(V_of_t, t0: float, t1: float, m: float, omega_max: float, T: float,
                                    field: str = "real", mu: float = 0.0, n_omega: int = 200) -> dict:
    """Born (first-order, in-in) NET pairs per volume from a homogeneous V(t) acting on a THERMAL medium of scalars.

    Builds on qp.born_scalar_homogeneous (vertex -(1/2) V phi^2 real, -V|phi|^2 complex): each pair has K = (Omega, 0),
    both particles carry Omega/2, and the vacuum spectrum is multiplied by W = 1 + n_+(Omega/2) + n_-(Omega/2):
        N/Vol = int_{2m}^{omega_max} dOmega/(2pi) |V~(Omega)|^2 rho(Omega^2) [1 + n_+(Omega/2) + n_-(Omega/2)].
    Quantity: dict with 'pairs_per_volume' (NET mean number of PAIRS created per unit volume = created minus
        annihilated, energy^3; thermal particles already present not counted), 'particles_per_volume' (= 2 x pairs),
        'vacuum_pairs_per_volume' (T = 0, = qp), 'thermal_factor' (ratio, > 1: stimulated), and the thermal
        spectrum 'dN_dOmega' on 'omega'.
    Valid when: as qp.born_scalar_homogeneous (first order in V; V -> 0 at both ends; spectrum negligible above
        omega_max > 2m); T >= 0 in the frame where V is homogeneous; m > 0 if T > 0; field 'real' (mu = 0) or
        'complex' (|mu| < m)."""
    T, mu = _thermal_born_checks(float(m), T, field, mu, "boson")
    r = qp.born_scalar_homogeneous(V_of_t, t0, t1, m, omega_max, field, n_omega)
    om = r["omega"]
    nodes, w = qp._gauss_legendre(2 * float(m), omega_max, n_omega)     # qp does not return its weights
    if not np.array_equal(nodes, om):
        raise RuntimeError("qp.born_scalar_homogeneous changed its Omega nodes: rebuild the weights here")
    W = thermal_pair_weight(om, np.zeros_like(om), m, T, mu, "boson")
    dN = r["dN_dOmega"] * W
    N = float(np.sum(w * dN))
    N0 = r["pairs_per_volume"]
    return {"pairs_per_volume": N, "particles_per_volume": 2 * N, "vacuum_pairs_per_volume": N0,
            "thermal_factor": N / N0 if N0 > 0 else float("nan"), "omega": om, "dN_dOmega": dN}


def born_scalar_general_thermal(Vtilde4, m: float, s_max: float, kappa_max: float, T: float, field: str = "real",
                                mu: float = 0.0, s_min: float = 0.0, n_s: int = 40, n_k: int = 40, n_c: int = 16,
                                n_p: int = 16) -> dict:
    """Born NET pairs from a background V(t, x) of any profile acting on a thermal medium of scalars (4D spectral form).

    N = int d^4K/(2pi)^4 theta(K0) |V~(K)|^2 rho(K^2) W(K), W = thermal_pair_weight, on qp's 4D nodes (qp._four_nodes);
    Vtilde4(K0, Kx, Ky, Kz) = int d^4x e^{i(K0 t - K.x)} V(t, x) with K in the medium rest frame.
    Quantity: dict with 'pairs' (total NET mean number of PAIRS created = created minus annihilated, in-in,
        dimensionless), 'particles' (= 2 x pairs), 'vacuum_pairs' (T = 0, = qp.born_scalar_general) and
        'thermal_factor'. Scattering of medium particles (spacelike K, Landau damping) is NOT included: it changes no
        number.
    Valid when: as qp.born_scalar_general (first order; spectrum negligible beyond s_max, kappa_max; m > 0 or
        s_min > 0; grids resolve V~); T >= 0; field 'real' (mu = 0) or 'complex' (|mu| < m)."""
    m, s_min = float(m), float(s_min)
    if m < 0 or s_min < 0:
        raise ValueError("need m >= 0 and s_min >= 0")
    qp._check_massless_scalar_vertex(m, s_min)
    T = _temperature(T)
    mu = _field_mu(field, "boson", mu)
    if mu != 0 and abs(mu) >= m:
        raise ValueError("bosons need |mu| < m (no condensate)")
    s_th = max(4 * m * m, s_min)
    if not s_max > s_th or not kappa_max > 0:
        raise ValueError("need s_max > max(4m^2, s_min) and kappa_max > 0")
    S, K0, Kx, Ky, Kz, Wq = qp._four_nodes(s_th, s_max, kappa_max, n_s, n_k, n_c, n_p)
    val = np.abs(np.asarray(Vtilde4(K0, Kx, Ky, Kz))) ** 2 * qp.pair_spectral_density_scalar(S, m, field)
    kap = np.sqrt(Kx * Kx + Ky * Ky + Kz * Kz)
    Wt = thermal_pair_weight(K0, kap, m, T, mu, "boson")
    N, N0 = float(np.sum(Wq * val * Wt)), float(np.sum(Wq * val))
    return {"pairs": N, "particles": 2 * N, "vacuum_pairs": N0, "thermal_factor": N / N0 if N0 > 0 else float("nan")}


def born_yukawa_homogeneous_thermal(V_of_t, t0: float, t1: float, m: float, omega_max: float, T: float,
                                    mu: float = 0.0, n_omega: int = 200) -> dict:
    """Born (first-order, in-in) NET Dirac pairs per volume from a homogeneous V(t) coupled as -V psibar psi, thermal medium.

    N/Vol = int_{2m}^{omega_max} dOmega/(2pi) |V~(Omega)|^2 rho_psi(Omega^2) [1 - n_+(Omega/2) - n_-(Omega/2)],
    rho_psi = s b^3/(4 pi) (pair_spectral_density_yukawa), V~(Omega) = int V(t) e^{i Omega t} dt (qp's quadrature).
    (V acts as a time-dependent mass m + V(t); per helicity the Dirac equation is the two-level problem of
    qp.bogoliubov_fermion_efield with p(t) -> m + V(t), eps_perp -> |k|, which the self-test uses as the exact check.)
    Quantity: dict with 'pairs_per_volume' (NET mean number of electron-positron PAIRS created per unit volume =
        electrons = positrons, energy^3, spins summed; thermal fermions already present not counted),
        'vacuum_pairs_per_volume' (T = 0), 'thermal_factor' (< 1: Pauli blocking), 'omega', 'dN_dOmega'.
    Valid when: first order in V (|V| << m, compare amplitudes); V -> 0 at both ends of [t0, t1]; spectrum
        negligible above omega_max > 2m; m >= 0; T >= 0 in the frame where V is homogeneous; any real mu."""
    m = float(m)
    T, mu = _thermal_born_checks(m, T, "complex", mu, "fermion")
    if m < 0 or not omega_max > 2 * m or t1 <= t0:
        raise ValueError("need m >= 0, omega_max > 2m and t1 > t0")
    om, w = qp._gauss_legendre(2 * m, omega_max, n_omega)
    Vt = qp._ft_time(V_of_t, t0, t1, om)
    dN0 = np.abs(Vt) ** 2 * pair_spectral_density_yukawa(om * om, m) / (2 * PI)
    dN = dN0 * thermal_pair_weight(om, np.zeros_like(om), m, T, mu, "fermion")
    N, N0 = float(np.sum(w * dN)), float(np.sum(w * dN0))
    return {"pairs_per_volume": N, "vacuum_pairs_per_volume": N0, "thermal_factor": N / N0 if N0 > 0 else float("nan"),
            "omega": om, "dN_dOmega": dN}


def born_yukawa_general_thermal(Vtilde4, m: float, s_max: float, kappa_max: float, T: float, mu: float = 0.0,
                                n_s: int = 40, n_k: int = 40, n_c: int = 16, n_p: int = 16) -> dict:
    """Born NET Dirac pairs from a background V(t, x) of any profile, Yukawa vertex -V psibar psi, thermal medium.

    N = int d^4K/(2pi)^4 theta(K0) |V~(K)|^2 rho_psi(K^2) W_F(K), W_F = <1 - n_+(E1) - n_-(E2)> (thermal_pair_weight).
    Quantity: dict with 'pairs' (total NET mean number of electron-positron PAIRS created, in-in, dimensionless,
        spins summed), 'vacuum_pairs' (T = 0) and 'thermal_factor'.
    Valid when: first order in V; |V~| negligible for s > s_max or |K| > kappa_max; m >= 0 (massless pairs are not
        collinear-singular here: rho_psi ~ s); grids resolve V~; T >= 0, any real mu, K in the medium rest frame."""
    m = float(m)
    T, mu = _thermal_born_checks(m, T, "complex", mu, "fermion")
    if m < 0:
        raise ValueError("m must be >= 0")
    s_th = 4 * m * m
    if not s_max > s_th or not kappa_max > 0:
        raise ValueError("need s_max > 4m^2 and kappa_max > 0")
    if m == 0:
        s_th = 1e-12 * s_max      # rho_psi ~ s: the light-cone end contributes nothing; keeps E- > 0
    S, K0, Kx, Ky, Kz, Wq = qp._four_nodes(s_th, s_max, kappa_max, n_s, n_k, n_c, n_p)
    val = np.abs(np.asarray(Vtilde4(K0, Kx, Ky, Kz))) ** 2 * pair_spectral_density_yukawa(S, m)
    Wt = thermal_pair_weight(K0, np.sqrt(Kx * Kx + Ky * Ky + Kz * Kz), m, T, mu, "fermion")
    N, N0 = float(np.sum(Wq * val * Wt)), float(np.sum(Wq * val))
    return {"pairs": N, "vacuum_pairs": N0, "thermal_factor": N / N0 if N0 > 0 else float("nan")}


# ---------------------------------------------------------------- independent integrators (self-test only)
def _rk4_oscillator(omega2, t0, t1, n, q, p):
    """Classical q'' = -omega^2(t) q by fixed-step RK4 (vectorised over columns); independent of qp's Magnus."""
    h = (t1 - t0) / n
    q, p = np.array(q, dtype=float), np.array(p, dtype=float)
    for j in range(n):
        t = t0 + j * h
        w1, w2, w4 = omega2(t), omega2(t + 0.5 * h), omega2(t + h)
        k1q, k1p = p, -w1 * q
        k2q, k2p = p + 0.5 * h * k1p, -w2 * (q + 0.5 * h * k1q)
        k3q, k3p = p + 0.5 * h * k2p, -w2 * (q + 0.5 * h * k2q)
        k4q, k4p = p + h * k3p, -w4 * (q + h * k3q)
        q = q + h / 6 * (k1q + 2 * k2q + 2 * k3q + k4q)
        p = p + h / 6 * (k1p + 2 * k2p + 2 * k3p + k4p)
    return q, p


def _rk4_two_level(pz_of_t, ex, t0, t1, n, c0, c1):
    """i dc/dt = (pz(t) sigma_z + ex sigma_x) c by fixed-step RK4 (vectorised); independent of qp's Magnus."""
    h = (t1 - t0) / n
    c0, c1 = np.array(c0, dtype=complex), np.array(c1, dtype=complex)

    def f(t, a, b):
        pz = pz_of_t(t)
        return -1j * (pz * a + ex * b), -1j * (ex * a - pz * b)
    for j in range(n):
        t = t0 + j * h
        a1, b1 = f(t, c0, c1)
        a2, b2 = f(t + 0.5 * h, c0 + 0.5 * h * a1, c1 + 0.5 * h * b1)
        a3, b3 = f(t + 0.5 * h, c0 + 0.5 * h * a2, c1 + 0.5 * h * b2)
        a4, b4 = f(t + h, c0 + h * a3, c1 + h * b3)
        c0 = c0 + h / 6 * (a1 + 2 * a2 + 2 * a3 + a4)
        c1 = c1 + h / 6 * (b1 + 2 * b2 + 2 * b3 + b4)
    return c0, c1


def _covariance_complex(n_a: float, n_b: float, w: float) -> np.ndarray:
    """Symmetrised covariance of (x1, p1, x2, p2) for a complex-field mode pair with <a^dag a> = n_a, <b^dag b> = n_b.

    Built by operator algebra: phi_k = (x1 + i x2)/sqrt2, A_j = sqrt(w/2)(x_j + i p_j/w), a = (A1 - i A2)/sqrt2,
    b = (A1 + i A2)/sqrt2, and the only nonzero in-state two-point functions <a^dag a>, <a a^dag>, <b^dag b>, <b b^dag>."""
    G = np.zeros((4, 4))                    # basis (a, a^dag, b, b^dag): G[i, j] = <e_i e_j>
    G[1, 0], G[0, 1], G[3, 2], G[2, 3] = n_a, n_a + 1.0, n_b, n_b + 1.0
    r2 = math.sqrt(2.0)
    A = [(np.array([1, 0, 1, 0]) / r2 + 0j, np.array([0, 1, 0, 1]) / r2 + 0j),
         (np.array([1j, 0, -1j, 0]) / r2, np.array([0, -1j, 0, 1j]) / r2)]     # (A_j, A_j^dag)
    ops = []
    for Aj, Ajd in A:
        ops += [(Aj + Ajd) / math.sqrt(2 * w), -1j * math.sqrt(w / 2) * (Aj - Ajd)]
    S = np.array([[0.5 * (oi @ G @ oj + oj @ G @ oi) for oj in ops] for oi in ops])
    return S.real


def _occupations_from_covariance(S: np.ndarray, w: float):
    """(<a^dag a>, <b^dag b>) at frequency w from the symmetrised covariance of (x1, p1, x2, p2)."""
    AA = [(w / 2) * (S[2 * j, 2 * j] + S[2 * j + 1, 2 * j + 1] / w ** 2) - 0.5 for j in (0, 1)]
    im12 = 0.5 * (S[0, 3] - S[1, 2])        # Im <A1^dag A2> = <x1 p2 - p1 x2>/2 (half the charge)
    base = 0.5 * (AA[0] + AA[1])
    return base + im12, base - im12


# ---------------------------------------------------------------- self-test
def selftest(verbose: bool = True) -> bool:
    """Compare with published equations, exact limits and independent numerical methods. Returns True if all pass."""
    results = []

    def check(name, got, want, tol, rel=False):
        err = abs(got - want) / (abs(want) if rel and want != 0 else 1.0)
        ok = bool(err <= tol)
        results.append(ok)
        if verbose:
            print(f"{'PASS' if ok else 'FAIL'}  {name}: {got:.10g} (expected {want:.10g}, "
                  f"{'rel' if rel else 'abs'} tol {tol:g})")

    # A1. Published: Kim, Lee & Yoon 2009 (arXiv:0811.0349), eq. 18 (scalar QED) as printed by fetch_text:
    #     "N sc k (T ) = |νk|2 Zk ∞∑ n,m =0 ⟨n, m |(n + m + 1)e−(n+m)βω k, in|n, m ⟩ = |νk|2 coth βω k, in 2 . (18)"
    #     (PDF extraction flattens the fraction; my reading: N_k(T) = |nu_k|^2 coth(beta omega_k,in/2), beta = 1/T,
    #     the mean number of pairs created in mode k; their eq. 16 is "(1/2Z) Tr(N_out - N_in) e^{-beta H}").
    #     Independent route: the thermal two-point function of the complex field, built by operator algebra
    #     (_covariance_complex), propagated with the classical transfer matrix of omega^2(t) = eps_perp^2 + p(t)^2 from
    #     a fixed-step RK4 (not qp's Magnus), read out at the end; |nu_k|^2 from Gavrilov & Gitman 1996 eq. 43 (qp).
    #     Sauter eE0 = 0.5, tau = 2, m = 1, k_perp = 0.3, T = 0.8; window +-12 tau (field e^-24 of its peak).
    eE0, tau, Tq, kp = 0.5, 2.0, 0.8, 0.3
    kz = np.array([-0.6, 0.0, 0.5])
    pf, _ = qp.sauter_kinetic_momentum(kz, eE0, tau)
    ep2 = 1.0 + kp * kp
    ta, tb = -12 * tau, 12 * tau
    # RK4 with h = 48/12000 = 0.004: the relative error of the vacuum |beta|^2 from the propagated covariance is 7e-9
    # at worst (measured; 2.4e-7 at 6000 steps: 5th-order convergence), and the thermal checks below measure 1.5e-8,
    # so the 1e-7 tolerances have a 7x margin (a wrong thermal factor fails them by > 1e-2).
    nst = 12000
    (Q1, Q2), (P1, P2) = _rk4_oscillator(lambda t: ep2 + pf(t) ** 2, ta, tb, nst, [np.ones(3), np.zeros(3)],
                                         [np.zeros(3), np.ones(3)])     # two fundamental solutions at once
    w_in, w_out = np.sqrt(ep2 + pf(ta) ** 2), np.sqrt(ep2 + pf(tb) ** 2)
    nu2 = qp.sauter_n_scalar(kz, kp, 1.0, eE0, tau)
    errs = []
    for i in range(3):
        n0 = float(bose_einstein(w_in[i], Tq))
        M = np.kron(np.eye(2), np.array([[Q1[i], Q2[i]], [P1[i], P2[i]]]))
        Na, Nb = _occupations_from_covariance(M @ _covariance_complex(n0, n0, w_in[i]) @ M.T, w_out[i])
        kly = nu2[i] / math.tanh(w_in[i] / (2 * Tq))
        errs.append(abs((Na - n0) / kly - 1) + abs((Nb - n0) / kly - 1))
    mod = sauter_thermal_mode(kz, kp, 1.0, eE0, tau, Tq, fermion=False)["net_created"]
    errs.append(float(np.max(np.abs(mod / (nu2 / np.tanh(w_in / (2 * Tq))) - 1))))
    check("KLY 2009 eq. 18 (scalar QED, Sauter, T = 0.8 m): propagated thermal covariance and sauter_thermal_mode "
          "vs |nu|^2 coth(omega/2T), max rel.", max(errs), 0.0, 1e-7)

    # A2. Published: KLY 2009 eq. 20 (spinor QED), printed: "N sp n (T ) = − |νn|2 Zn 1∑ n,m =0 ⟨n, m |(n + m −
    #     1)e−(n+m)βω n, in|n, m ⟩ = |νn|2 tanh βω n, in 2 . (20)" (my reading: |nu_n|^2 tanh(beta omega_n,in/2)).
    #     Independent route: the one-body density matrix rho1 = n_e |+><+| + (1 - n_p)|-><-| of the two-level
    #     reduction (in-adiabatic basis) propagated by RK4 (U rho1 U^dag, not qp's Magnus); electrons out =
    #     <+_out|rho1|+_out>, positrons out = 1 - <-_out|rho1|-_out>; |nu|^2 from GG eq. 42 (qp).
    th0, th1 = np.arctan2(math.sqrt(ep2), pf(ta)), np.arctan2(math.sqrt(ep2), pf(tb))
    plus0, minus0 = (np.cos(th0 / 2), np.sin(th0 / 2)), (-np.sin(th0 / 2), np.cos(th0 / 2))
    plus1, minus1 = (np.cos(th1 / 2), np.sin(th1 / 2)), (-np.sin(th1 / 2), np.cos(th1 / 2))
    c0, c1 = _rk4_two_level(pf, math.sqrt(ep2), ta, tb, nst, [plus0[0], minus0[0]], [plus0[1], minus0[1]])
    Up, Um = (c0[0], c1[0]), (c0[1], c1[1])                                    # U |+_in>, U |-_in>
    nu2f = qp.sauter_n_spinor(kz, kp, 1.0, eE0, tau)

    def fermion_out(ne, npos):
        amp = lambda out, U: out[0] * U[0] + out[1] * U[1]     # noqa: E731  (<out|U|in>, real adiabatic vectors)
        e_out = ne * np.abs(amp(plus1, Up)) ** 2 + (1 - npos) * np.abs(amp(plus1, Um)) ** 2
        p_out = 1 - (ne * np.abs(amp(minus1, Up)) ** 2 + (1 - npos) * np.abs(amp(minus1, Um)) ** 2)
        return e_out, p_out
    nF = fermi_dirac(w_in, Tq)
    e_out, p_out = fermion_out(nF, nF)
    kly = nu2f * np.tanh(w_in / (2 * Tq))
    modf = sauter_thermal_mode(kz, kp, 1.0, eE0, tau, Tq, fermion=True)["net_created"]
    check("KLY 2009 eq. 20 (spinor QED, Sauter, T = 0.8 m): propagated density matrix and sauter_thermal_mode vs "
          "|nu|^2 tanh(omega/2T), max rel.", float(np.max(np.abs((e_out - nF) / kly - 1) + np.abs((p_out - nF) / kly - 1)
                                                         + np.abs(modf / kly - 1))), 0.0, 1e-7)   # RK4 as above
    #     Quotable statement (v), KLY 2009 p. 5, as printed (the extraction splits "thermally"): "The production of
    #     scalar pairs is ther mally enhanced, while the production of fermion pairs is thermally suppressed as
    #     expected by the Pauli blocking". Same statement for bosons in Gavrilov, Gitman & Tomazelli 2008
    #     (hep-th/0612064) abstract: "It is shown that in the general case a presence of bosons (e.g., gluons) in the
    #     initial state increases the creation rate of the same type of bosons."
    check("thermal factor: scalar > 1 (stimulated) and spinor < 1 (Pauli blocked) in every mode",
          float(np.all(mod > nu2) and np.all(modf < nu2f)), 1.0, 0)

    # A3. Chemical potential, particle k vs antiparticle -k (no published table: an independent method). Complex
    #     scalar in the Bernard-Duncan tanh model (closed-form |beta|^2, Birrell & Davies eq. 3.140b via qp),
    #     T = 0.7, mu = 0.4: covariance propagation (RK4 transfer matrix) vs out_occupation's
    #     n_+ + |beta|^2 (1 + n_+ + n_-) and n_- + |beta|^2 (1 + n_+ + n_-); and charge conservation.
    kk = np.array([0.1, 0.4, 1.0])
    w2f, (ta, tb) = qp.tanh_model_omega2(kk, 1.0, 2.0, 1.0, 2.0, ends=15.0)
    (Q1, Q2), (P1, P2) = _rk4_oscillator(w2f, ta, tb, 4000, [np.ones(3), np.zeros(3)], [np.zeros(3), np.ones(3)])
    wi, wo = np.sqrt(w2f(ta)), np.sqrt(w2f(tb))
    b2 = qp.tanh_model_beta2(kk, 1.0, 2.0, 1.0, 2.0)
    mu = 0.4
    r = thermal_mode_production(b2, wi, 0.7, mu, "boson", "complex")
    errs, charge = [], []
    for i in range(3):
        M = np.kron(np.eye(2), np.array([[Q1[i], Q2[i]], [P1[i], P2[i]]]))
        S0 = _covariance_complex(r["n_particles"][i], r["n_antiparticles"][i], wi[i])
        Na, Nb = _occupations_from_covariance(M @ S0 @ M.T, wo[i])
        errs.append(max(abs(Na / r["particles_out"][i] - 1), abs(Nb / r["antiparticles_out"][i] - 1)))
        charge.append(abs((Na - Nb) - (r["n_particles"][i] - r["n_antiparticles"][i])))
    check("complex scalar, mu = 0.4 m, T = 0.7 m: covariance propagation = n_+- + |beta|^2 (1 + n_+ + n_-), max rel.",
          max(errs), 0.0, 1e-7)        # measured 4e-11 (RK4 at 4000 steps, h = 0.0038): 1e-7 leaves room for load-
    #                                    independent roundoff only; a wrong factor (e.g. 1 + 2n_+) fails by > 1e-1
    check("charge conservation: (N_+ - N_-)_out = (n_+ - n_-)_in", max(charge), 0.0, 1e-9)   # RK4 keeps L to ~1e-12
    # A4. Fermions with mu (electron excess): density-matrix propagation = closed form; net creation still > 0.
    ne, npos = fermi_dirac(w_in, Tq, 0.5), fermi_dirac(w_in, Tq, -0.5)
    e_out, p_out = fermion_out(ne, npos)
    rf = out_occupation(nu2f, ne, npos, "fermion")
    check("spinor QED, mu = 0.5 m: propagated density matrix = n_+- + |nu|^2 (1 - n_+ - n_-) (electrons, positrons), "
          "max rel.", float(np.max(np.abs(e_out / rf["particles_out"] - 1) + np.abs(p_out / rf["antiparticles_out"] - 1))),
          0.0, 1e-7)                   # same RK4 run as A2 (|beta|^2 error 7e-9 relative, diluted by n_+- here)

    # B. Classical-statistical limit (independent: classical mechanics). A random-phase ensemble of classical
    #    oscillators with exponentially distributed actions (Rayleigh amplitudes, mean J = 200: n >> 1) through the
    #    SAME omega(t) (tanh model, m = 1, A = 2, B = 1.5, rho = 4, k = 0.1), integrated one by one with RK4:
    #    <J_out>/<J_in> must equal 1 + 2|beta|^2 (closed form), the n >> 1 limit of
    #    N_out/n_in = 1 + 2|beta|^2 + |beta|^2/n. Tolerance: 4 standard errors of the ratio (delta method).
    k1 = np.array([0.1])
    w2c, (ta, tb) = qp.tanh_model_omega2(k1, 1.0, 2.0, 1.5, 4.0)
    b2c = float(qp.tanh_model_beta2(k1, 1.0, 2.0, 1.5, 4.0)[0])
    wi, wo = math.sqrt(float(w2c(ta)[0])), math.sqrt(float(w2c(tb)[0]))
    rng = np.random.default_rng(20261011)
    Nmc, Jbar = 8000, 200.0
    J = rng.exponential(Jbar, Nmc)
    ph = rng.uniform(0.0, 2 * PI, Nmc)
    q, p = _rk4_oscillator(lambda t: float(w2c(t)[0]), ta, tb, 2000,
                           np.sqrt(2 * J / wi) * np.cos(ph), -np.sqrt(2 * J * wi) * np.sin(ph))
    Jo = (p * p + wo * wo * q * q) / (2 * wo)
    R = float(Jo.mean() / J.mean())
    se = float(np.std(Jo - R * J) / math.sqrt(Nmc) / J.mean())
    check(f"classical Monte Carlo (8000 oscillators): <J_out>/<J_in> = 1 + 2|beta|^2 = {1 + 2 * b2c:.4f} "
          f"(standard error {se:.4f})", R, 1 + 2 * b2c, 4 * se)
    #    The module's QUANTUM formula at the same mean occupation (T chosen so that n_in = 200) must reproduce the
    #    classical ensemble: N_out/n_in = 1 + 2|beta|^2 + |beta|^2/n differs from 1 + 2|beta|^2 by 9e-4 << 4 se.
    nq = thermal_mode_production([b2c], [wi], wi / math.log1p(1 / Jbar), 0.0, "boson", "real")
    check("quantum thermal_mode_production at n_in = 200 vs the classical ensemble: N_out/n_in = <J_out>/<J_in>",
          float(nq["particles_out"][0] / nq["n_particles"][0]), R, 4 * se)
    check("the stimulated effect is resolved: (R - 1) > 20 standard errors and R - 1 = 2|beta|^2 >> |beta|^2/n",
          float((R - 1) > 20 * se), 1.0, 0)

    # C1. FRW, massless and conformally coupled. Parker 1969 (Phys. Rev. 183, 1057) abstract (lit_search): "We show
    #     that in a universe with flat 3-space containing only massless particles in equilibrium, there will be
    #     precisely no creation of massless particles as a result of the expansion". qp's FRW solver in a lumpy,
    #     non-tanh a(eta) (a_in = 1, a_out = 2): occupations unchanged and T_eff(k) = T_in a_in/a_out at every k.
    def lumpy(eta):
        return 1.0 + 0.5 * (1 + np.tanh(0.8 * eta)) + 0.3 * np.exp(-((eta - 1.0) / 0.7) ** 2)
    kc = np.linspace(0.05, 3.0, 12)
    rr = frw_thermal_production(kc, lumpy, 0.0, 1.0 / 6.0, -40.0, 40.0, 0.5)
    check("FRW m = 0, xi = 1/6, T_in = 0.5: max |n_out - n_in| (no creation, Parker 1969)",
          float(np.max(np.abs(rr["n_out"] - rr["n_in"]))), 0.0, 1e-12)   # solver floor ~1e-25 in |beta|^2
    check("... and the out spectrum is Planck at T_in a_in/a_out = 0.25: max rel. spread of T_eff(k)",
          float(np.max(np.abs(rr["T_eff"] / frw_redshifted_temperature(0.5, rr["a_in"], rr["a_out"]) - 1))), 0.0, 1e-10)
    # C2. Massive, conformally coupled, tanh universe a^2 = 2 + tanh(0.7 eta) (Birrell & Davies eq. 3.140b closed
    #     form): solver at finite T = closed form n_in + |beta|^2 (1 + 2 n_in); the out spectrum is NOT thermal.
    a_f, app_f, (e0, e1) = qp.frw_tanh_scale_factor(2.0, 1.0, 0.7)
    rr = frw_thermal_production(kc, a_f, 1.0, 1.0 / 6.0, e0, e1, 0.5, a_pp=app_f)
    nin = bose_einstein(np.sqrt(kc * kc + 1.0), 1.0 * 0.5)
    ref = nin + qp.tanh_model_beta2(kc, 1.0, 2.0, 1.0, 0.7) * (1 + 2 * nin)
    check("FRW tanh universe, m = 1, xi = 1/6, T_in = 0.5: net created = |beta|^2 (1 + 2 n_in) and n_out = n_in + net, "
          "max rel.", float(np.max(np.abs(rr["net_created"] / (ref - nin) - 1)) + np.max(np.abs(rr["n_out"] / ref - 1))),
          0.0, 1e-6)    # qp's solver: rtol 1e-7 on beta, |beta|^2 to ~1e-7 (qp checks 1e-6 against this closed form)
    spread = float(np.max(rr["T_eff"]) / np.min(rr["T_eff"]) - 1)
    check(f"... massive: out spectrum not thermal (T_eff(k) spread {spread:.3f} > 0.05)", float(spread > 0.05), 1.0, 0)

    # D1. Thermal weight: closed-form log average vs a direct average over the pair rest-frame decay angle
    #     (E1 = K0/2 + (kappa b/2) cos theta*, 400-point Gauss-Legendre in cos theta*), computed as
    #     (1 - e^{-K0/T}) <(1 +- n1)(1 +- n2)>, i.e. creation minus annihilation by detailed balance.
    xg, wg = np.polynomial.legendre.leggauss(400)
    worst = 0.0
    for stat, mu_, m_ in (("boson", 0.0, 1.0), ("boson", 0.6, 1.0), ("fermion", 0.0, 1.0), ("fermion", 1.7, 0.5),
                          ("fermion", -0.4, 0.0)):
        sg = _sign(stat)
        for K0_, kap_, T_ in ((2.5, 0.0, 1.0), (3.0, 1.2, 0.7), (6.0, 5.0, 1.5), (8.0, 2.0, 0.4), (4.0, 3.9, 2.0)):
            s_ = K0_ * K0_ - kap_ * kap_
            if s_ < 4 * m_ * m_ or s_ <= 0:
                continue
            bb = math.sqrt(1 - 4 * m_ * m_ / s_)
            E1 = 0.5 * K0_ + 0.5 * kap_ * bb * xg
            E2 = K0_ - E1
            occ = (lambda E, c: 1 / np.expm1((E - c) / T_)) if sg > 0 else (lambda E, c: 1 / (np.exp((E - c) / T_) + 1))
            n1, n2 = occ(E1, mu_), occ(E2, -mu_)
            direct = (1 - math.exp(-K0_ / T_)) * 0.5 * float(np.sum(wg * (1 + sg * n1) * (1 + sg * n2)))
            got = float(thermal_pair_weight(K0_, kap_, m_, T_, mu_, stat))
            worst = max(worst, abs(got / direct - 1))
    check("thermal_pair_weight (closed form) = (1 - e^{-K0/T}) <(1 +- n1)(1 +- n2)> by angular quadrature, "
          "bosons/fermions, mu != 0, max rel.", worst, 0.0, 1e-10)    # 400-point Gauss: quadrature error < 1e-13

    # D2. Born at finite T vs the EXACT mode solvers at finite T, homogeneous V = eps exp(-t^2/(2 tau^2)), tau = 0.3,
    #     m = 1, T = 1 (units of m). Exact: int d^3k/(2pi)^3 |beta_k|^2 (1 +- 2 n(omega_k)) with |beta_k|^2 from
    #     qp.bogoliubov_boson (scalar, omega^2 = k^2 + m^2 + V) and qp.bogoliubov_fermion_efield (Dirac with mass
    #     m + V(t): per helicity i c' = ((m + V) sigma_z + |k| sigma_x) c), 32 Gauss nodes in k <= 12 (48 nodes agree
    #     to 1e-6). Born is O(eps^2) exact, so |exact/Born - 1| must scale with eps (measured 0.28 eps scalar,
    #     0.63 eps Dirac, at T = 0 and at T = 1 alike).
    tau_ = 0.3
    fg = lambda t: np.exp(-t ** 2 / (2 * tau_ ** 2))    # noqa: E731
    kq, wq = qp._gauss_legendre(0.0, 12.0, 32)
    om_k = np.sqrt(kq * kq + 1.0)
    devs = {"scalar": [], "Dirac": []}
    for eps in (0.05, 0.1):
        rb = qp.bogoliubov_boson(lambda t, eps=eps: kq * kq + 1.0 + eps * fg(t), -12 * tau_, 12 * tau_, rtol=1e-6)
        ex = float(np.sum(wq * kq * kq * rb["beta2"] * (1 + 2 * bose_einstein(om_k, 1.0)))) / (2 * PI * PI)
        ex0 = float(np.sum(wq * kq * kq * rb["beta2"])) / (2 * PI * PI)
        bo = born_scalar_homogeneous_thermal(lambda t, eps=eps: eps * fg(t), -12 * tau_, 12 * tau_, 1.0, 30.0, 1.0)
        devs["scalar"].append(abs(ex / bo["particles_per_volume"] - 1))
        check(f"real scalar, V = eps f(t), eps = {eps} m^2: |exact/Born - 1| <= 0.6 eps at T = m (stimulated factor "
              f"{bo['thermal_factor']:.3f}) and at T = 0", max(devs["scalar"][-1],
                                                               abs(ex0 / (2 * bo["vacuum_pairs_per_volume"]) - 1)), 0.0, 0.6 * eps)
        sfac = bo["thermal_factor"]
        rf_ = qp.bogoliubov_fermion_efield(lambda t, eps=eps: 1.0 + eps * fg(t), kq, -12 * tau_, 12 * tau_, rtol=1e-6)
        ex = 2 * float(np.sum(wq * kq * kq * rf_["n"] * (1 - 2 * fermi_dirac(om_k, 1.0)))) / (2 * PI * PI)
        ex0 = 2 * float(np.sum(wq * kq * kq * rf_["n"])) / (2 * PI * PI)
        bo = born_yukawa_homogeneous_thermal(lambda t, eps=eps: eps * fg(t), -12 * tau_, 12 * tau_, 1.0, 30.0, 1.0)
        devs["Dirac"].append(abs(ex / bo["pairs_per_volume"] - 1))
        check(f"Dirac, Yukawa V = eps f(t), eps = {eps} m: |exact/Born - 1| <= 0.8 eps at T = m (Pauli factor "
              f"{bo['thermal_factor']:.3f}) and at T = 0 (rho_psi = s b^3/4pi)",
              max(devs["Dirac"][-1], abs(ex0 / bo["vacuum_pairs_per_volume"] - 1)), 0.0, 0.8 * eps)
    for tag in ("scalar", "Dirac"):
        check(f"{tag}: Born deviation halves when eps halves (ratio in [1.6, 2.4])", devs[tag][1] / devs[tag][0], 2.0, 0.4)
    check("thermal factors resolved: scalar 1 + 2n(Omega/2) > 1.3 (stimulated), Dirac 1 - 2n(Omega/2) < 0.85 (blocked)",
          float(sfac > 1.3 and bo["thermal_factor"] < 0.85), 1.0, 0)

    # D3. T -> 0 reproduces qp exactly (same quadrature): homogeneous and general Born, Sauter pairs per volume.
    #     Tolerances 1e-14 / 1e-13: only summation-order roundoff can differ (W = 1 exactly at T = 0).
    bh = born_scalar_homogeneous_thermal(lambda t: 0.05 * fg(t), -12 * tau_, 12 * tau_, 1.0, 30.0, 0.0)
    qh = qp.born_scalar_homogeneous(lambda t: 0.05 * fg(t), -12 * tau_, 12 * tau_, 1.0, 30.0)
    check("T = 0: born_scalar_homogeneous_thermal = qp.born_scalar_homogeneous", bh["pairs_per_volume"],
          qh["pairs_per_volume"], 1e-14, rel=True)

    def V4(K0, Kx, Ky, Kz):
        k2 = Kx * Kx + Ky * Ky + Kz * Kz
        return (2 * PI) ** 2 * np.exp(-k2 / 2) * 0.5 * (np.exp(-(K0 - 3.0) ** 2 / 2) + np.exp(-(K0 + 3.0) ** 2 / 2))
    check("T = 0: born_scalar_general_thermal = qp.born_scalar_general",
          born_scalar_general_thermal(V4, 1.0, 80.0, 8.0, 0.0, n_c=8, n_p=4)["pairs"],
          qp.born_scalar_general(V4, 1.0, 80.0, 8.0, n_c=8, n_p=4)["pairs"], 1e-13, rel=True)
    check("T = 0: sauter_thermal_pairs_per_volume = qp.sauter_pairs_per_volume (spinor, eE0 = 0.5, tau = 2)",
          sauter_thermal_pairs_per_volume(1.0, 0.5, 2.0, 0.0)["pairs_per_volume"],
          qp.sauter_pairs_per_volume(1.0, 0.5, 2.0, True), 1e-13, rel=True)

    # D4. The general 4D thermal spectral form against an INDEPENDENT 6D pair-momentum integral (reduced to 3D by the
    #     isotropy of V4): N = c int d^3p1 d^3p2/((2pi)^6 4 E1 E2) |V~(E1 + E2, p1 + p2)|^2 |M|^2 W(E1, E2), with
    #     c = 1/2, |M|^2 = 1, W = 1 + n(E1) + n(E2) (real scalar); c = 1, W = 1 + n_+(E1) + n_-(E2) (complex);
    #     c = 1, |M|^2 = 4 (p1.p2 - m^2), W = 1 - n_+(E1) - n_-(E2) (Dirac, Yukawa). m = 1, T = 0.7.
    p1, w1 = qp._gauss_legendre(0, 8, 48)
    c12, w12 = np.polynomial.legendre.leggauss(32)
    P1, P2, C12 = np.meshgrid(p1, p1, c12, indexing="ij")
    E1, E2 = np.sqrt(1 + P1 ** 2), np.sqrt(1 + P2 ** 2)
    Kn = np.sqrt(P1 ** 2 + P2 ** 2 + 2 * P1 * P2 * C12)
    base = np.abs(V4(E1 + E2, Kn, 0 * Kn, 0 * Kn)) ** 2 * P1 ** 2 * P2 ** 2 / (4 * E1 * E2)
    norm = 4 * PI * 2 * PI / (2 * PI) ** 6

    def direct(Wt, c=1.0, M2=1.0):
        return c * norm * float(np.einsum("i,j,k,ijk->", w1, w1, w12, base * M2 * Wt))
    Tg = 0.7
    nb_ = lambda E, c=0.0: 1 / np.expm1((E - c) / Tg)          # noqa: E731
    nf_ = lambda E, c=0.0: 1 / (np.exp((E - c) / Tg) + 1)      # noqa: E731
    got = born_scalar_general_thermal(V4, 1.0, 80.0, 8.0, Tg, n_c=8, n_p=4)
    check("general thermal Born (real scalar, T = 0.7) = direct 6D pair integral with 1 + n(E1) + n(E2)", got["pairs"],
          direct(1 + nb_(E1) + nb_(E2), 0.5), 1e-6, rel=True)      # qp's D4 grid gives 1e-6 at T = 0
    got = born_scalar_general_thermal(V4, 1.0, 80.0, 8.0, Tg, "complex", 0.3, n_c=8, n_p=4)
    check("... complex scalar, mu = 0.3: 1 + n_+(E1) + n_-(E2)", got["pairs"],
          direct(1 + nb_(E1, 0.3) + nb_(E2, -0.3)), 1e-6, rel=True)
    M2 = 4 * (E1 * E2 - P1 * P2 * C12 - 1.0)
    got = born_yukawa_general_thermal(V4, 1.0, 80.0, 8.0, Tg, 0.4, n_c=8, n_p=4)
    check("... Dirac pairs, Yukawa vertex, mu = 0.4: |M|^2 = 4(p1.p2 - m^2), 1 - n_+(E1) - n_-(E2)", got["pairs"],
          direct(1 - nf_(E1, 0.4) - nf_(E2, -0.4), 1.0, M2), 1e-6, rel=True)
    check("... and T = 0 Dirac pairs: rho_psi = s b^3/(4 pi) against sum |ubar v|^2 in 6D", got["vacuum_pairs"],
          direct(1.0, 1.0, M2), 1e-6, rel=True)

    passed = all(results)
    if verbose:
        print(f"\n{sum(results)}/{len(results)} checks passed")
    return passed


def _convergence() -> int:
    """Slow studies (not part of the self-test): Born-vs-exact deviation vs eps; Monte Carlo error vs N; 4D grids."""
    tau_ = 0.3
    fg = lambda t: np.exp(-t ** 2 / (2 * tau_ ** 2))    # noqa: E731
    kq, wq = qp._gauss_legendre(0.0, 12.0, 48)
    om_k = np.sqrt(kq * kq + 1.0)
    print("Born at finite T (T = m) vs exact mode solvers: |exact/Born - 1| should fall linearly with eps")
    for eps in (0.025, 0.05, 0.1, 0.2):
        rb = qp.bogoliubov_boson(lambda t: kq * kq + 1.0 + eps * fg(t), -12 * tau_, 12 * tau_, rtol=1e-7)
        ex = float(np.sum(wq * kq * kq * rb["beta2"] * (1 + 2 * bose_einstein(om_k, 1.0)))) / (2 * PI * PI)
        bo = born_scalar_homogeneous_thermal(lambda t: eps * fg(t), -12 * tau_, 12 * tau_, 1.0, 30.0, 1.0)
        rf = qp.bogoliubov_fermion_efield(lambda t: 1.0 + eps * fg(t), kq, -12 * tau_, 12 * tau_, rtol=1e-7)
        exf = 2 * float(np.sum(wq * kq * kq * rf["n"] * (1 - 2 * fermi_dirac(om_k, 1.0)))) / (2 * PI * PI)
        bf = born_yukawa_homogeneous_thermal(lambda t: eps * fg(t), -12 * tau_, 12 * tau_, 1.0, 30.0, 1.0)
        print(f"  eps = {eps:5.3f}: scalar {ex / bo['particles_per_volume'] - 1:+.5f}, "
              f"Dirac {exf / bf['pairs_per_volume'] - 1:+.5f}")
    print("Classical Monte Carlo <J_out>/<J_in> vs 1 + 2|beta|^2 (tanh model k = 0.1, A = 2, B = 1.5, rho = 4)")
    k1 = np.array([0.1])
    w2c, (ta, tb) = qp.tanh_model_omega2(k1, 1.0, 2.0, 1.5, 4.0)
    b2c = float(qp.tanh_model_beta2(k1, 1.0, 2.0, 1.5, 4.0)[0])
    wi, wo = math.sqrt(float(w2c(ta)[0])), math.sqrt(float(w2c(tb)[0]))
    rng = np.random.default_rng(1)
    for N in (1000, 4000, 16000, 64000):
        J = rng.exponential(200.0, N)
        ph = rng.uniform(0, 2 * PI, N)
        q, p = _rk4_oscillator(lambda t: float(w2c(t)[0]), ta, tb, 2000, np.sqrt(2 * J / wi) * np.cos(ph),
                               -np.sqrt(2 * J * wi) * np.sin(ph))
        Jo = (p * p + wo * wo * q * q) / (2 * wo)
        R = Jo.mean() / J.mean()
        se = np.std(Jo - R * J) / math.sqrt(N) / J.mean()
        print(f"  N = {N:6d}: R = {R:.5f} +- {se:.5f} (expected {1 + 2 * b2c:.5f}; deviation {(R - 1 - 2 * b2c) / se:+.2f} se)")
    print("General thermal Born (real scalar, T = 0.7, m = 1): grid doubling")

    def V4(K0, Kx, Ky, Kz):
        k2 = Kx * Kx + Ky * Ky + Kz * Kz
        return (2 * PI) ** 2 * np.exp(-k2 / 2) * 0.5 * (np.exp(-(K0 - 3.0) ** 2 / 2) + np.exp(-(K0 + 3.0) ** 2 / 2))
    for n_s, n_k in ((20, 20), (40, 40), (80, 80)):
        r = born_scalar_general_thermal(V4, 1.0, 80.0, 8.0, 0.7, n_s=n_s, n_k=n_k, n_c=8, n_p=4)
        print(f"  n_s = n_k = {n_s}: pairs {r['pairs']:.10g} (vacuum {r['vacuum_pairs']:.10g})")
    return 0


# ---------------------------------------------------------------- command line
def _energy(text: str) -> float:
    """Parse an energy ('0.511 MeV' -> eV) or a bare number (already in the chosen natural unit)."""
    try:
        return float(text)
    except ValueError:
        from unit_tools import Q
        return Q(text).expect("energy").si / E_CHARGE


def _temperature_arg(text: str) -> float:
    """Parse a temperature ('1e10 K' -> k_B T in eV), an energy ('1 MeV' -> eV) or a bare number (natural unit)."""
    try:
        return float(text)
    except ValueError:
        from unit_tools import Q
        q = Q(text)
        if q.kind == "temperature":
            return temperature_to_eV(q.si)
        if q.kind != "energy":
            raise ValueError(f"T must be a temperature (e.g. '1e10 K') or an energy k_B T (e.g. '1 MeV'), got {text!r}")
        return q.si / E_CHARGE


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("selftest")
    mp = sub.add_parser("mode", help="one mode: total out occupation and net created number from a thermal in-state")
    mp.add_argument("--beta2", type=float, required=True, help="vacuum |beta_k|^2 of the mode (from qft_production)")
    mp.add_argument("--omega", required=True, help="in-energy of the mode: a number in your natural unit, or e.g. '0.6 MeV'")
    mp.add_argument("--T", required=True, help="temperature, e.g. '5e9 K' or '0.4 MeV' (or a number in your unit)")
    mp.add_argument("--mu", default="0", help="chemical potential (energy; complex fields only)")
    mp.add_argument("--fermion", action="store_true", help="fermions (Dirac) instead of bosons")
    mp.add_argument("--real", action="store_true", help="real (neutral) boson field: mu must be 0")
    sp = sub.add_parser("sauter", help="Sauter pulse E0 sech^2(t/tau): net pairs per volume at T vs T = 0")
    sp.add_argument("--m", default="0.51099895 MeV", help="mass (default: electron)")
    sp.add_argument("--E", required=True, help="peak field, e.g. '1e18 V/m'")
    sp.add_argument("--tau", required=True, help="pulse time scale, e.g. '1e-21 s'")
    sp.add_argument("--T", required=True, help="temperature of the in-state, e.g. '3e9 K'")
    sp.add_argument("--mu", default="0", help="chemical potential (energy)")
    sp.add_argument("--scalar", action="store_true", help="scalar QED instead of spinor QED")
    sub.add_parser("convergence", help="slow studies: Born vs exact at finite T, Monte Carlo error, 4D grids")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "selftest":
            return 0 if selftest() else 1
        if args.cmd == "convergence":
            return _convergence()
        if args.cmd == "mode":
            w, T, mu = _energy(args.omega), _temperature_arg(args.T), _energy(args.mu)
            stat = "fermion" if args.fermion else "boson"
            r = thermal_mode_production([args.beta2], [w], T, mu, stat, "real" if args.real else "complex")
            print(f"{stat}s, omega_in = {w:.6g}, T = {T:.6g}, mu = {mu:.6g} (same unit; eV if units were given)")
            print(f"thermal in-state: n_+(k) = {r['n_particles'][0]:.6g}, n_-(-k) = {r['n_antiparticles'][0]:.6g}")
            print(f"net created in the mode pair (in-in): {r['net_created'][0]:.6g} = |beta|^2 {args.beta2:.6g} x factor "
                  f"{r['factor'][0]:.6g} ({'stimulated' if r['factor'][0] > 1 else 'Pauli-blocked' if r['factor'][0] < 1 else 'vacuum'})")
            print(f"TOTAL out occupation of mode k (thermal particles included): {r['particles_out'][0]:.6g}")
            return 0
        from unit_tools import Q
        m = _energy(args.m)
        eE = qp.eE_from_field_SI(Q(args.E).expect("V/m").si)
        tau = qp.time_to_inverse_eV(Q(args.tau).expect("time").si)
        T, mu = _temperature_arg(args.T), _energy(args.mu)
        fermion = not args.scalar
        r = sauter_thermal_pairs_per_volume(m, eE, tau, T, mu, fermion)
        print(f"{'spinor' if fermion else 'scalar'} QED, m = {m:.6g} eV, eE0 = {eE:.6g} eV^2 = {eE / m**2:.4g} m^2, "
              f"tau = {tau:.6g} /eV, T = {T:.6g} eV = {temperature_from_eV(T):.4g} K, mu = {mu:.4g} eV")
        print(f"net pairs per volume from the thermal in-state: {r['pairs_per_volume']:.6g} eV^3 = "
              f"{qp.density_to_SI(r['pairs_per_volume']):.6g} m^-3 (thermal particles already present not counted)")
        print(f"from the vacuum (T = 0): {r['vacuum_pairs_per_volume']:.6g} eV^3 = "
              f"{qp.density_to_SI(r['vacuum_pairs_per_volume']):.6g} m^-3; ratio {r['thermal_factor']:.6g} "
              f"({'Pauli blocking' if fermion else 'stimulated'})")
    except (ValueError, KeyError) as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
