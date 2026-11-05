#!/usr/bin/env python3
"""cosmo_background: homogeneous FRW background cosmology for the H0 / sound-horizon chain.

WHAT IT COMPUTES
    H(z); comoving (D_C), transverse comoving (D_M), angular-diameter (D_A), luminosity (D_L)
    distances and the distance modulus mu; the Hubble distance D_H = c/H(z); the comoving sound
    horizon r_s(z) by direct integration; z_* (Hu & Sugiyama 1996 fit) and z_drag (Eisenstein & Hu
    1998 fit); r_* = r_s(z_*), r_d = r_s(z_drag); the Aubourg et al. 2015 calibrated r_d fit as a
    cross-check; theta_* = r_s(z_*)/D_M(z_*); BAO observables D_M/r_d, D_H/r_d, D_V/r_d; and an
    inverse solve for h that reproduces a given 100*theta_* at fixed omega_b, omega_c and extras.

MODEL (all densities are PHYSICAL densities omega_i(a) = rho_i(a) / rho_crit,100, where
rho_crit,100 = 3 (100 km/s/Mpc)^2 / (8 pi G); a = 1/(1+z))
    H(a) = 100 km/s/Mpc * sqrt( sum_i omega_i(a) + omega_k a^-2 ),   omega_k = Omega_k h^2
    photons     omega_g(a) = omega_g0 a^-4,  rho_g0 c^2 = 4 sigma_SB T_cmb^4 / c   (T_cmb = 2.7255 K)
    massless nu omega(a)   = N_ml (7/8)(4/11)^(4/3) omega_g0 a^-4
    massive nu  omega_i(a) = g_i (7/8)(4/11)^(4/3) omega_g0 a^-4 F(y_i a),  y_i = m_i c^2/(k_B T_nu0),
                T_nu0 = (4/11)^(1/3) T_cmb,  F(y) = (120/7pi^4) int_0^inf q^2 sqrt(q^2+y^2)/(e^q+1) dq
                (F(0) = 1; F -> 180 zeta(3) y /(7 pi^4) when non-relativistic).
                N_eff convention (CAMB, as in Planck 2018 "two massless states and a single massive
                neutrino of mass 0.06 eV"): each massive species carries g = N_eff/3 and is a Fermi-Dirac
                gas at T = g^(1/4) T_nu0 (so omega_nu,NR = g^(3/4) m / 94.06 eV; 0.06 eV -> 0.000645);
                the massless remainder is N_ml = N_eff - n_massive * N_eff/3.
    baryons, CDM omega_b a^-3, omega_c a^-3
    curvature    Omega_k (held fixed when h varies); D_M uses sinh / sin (Hogg 1999 eq. 16)
    dark energy  CPL: rho_DE ∝ a^{-3(1+w0+wa)} exp(-3 wa (1-a)), w(a) = w0 + wa (1-a);
                 Lambda is w0 = -1, wa = 0. Omega_DE is set by closure: Omega_DE = 1 - Omega_k - sum Omega_i(z=0).
    EDE fluid    (Poulin, Smith, Karwal, Kamionkowski 2019 eq. 1, effective-fluid approximation)
                 rho_EDE(a) = 2 rho_EDE(a_c) / [ (a/a_c)^{3(1+w_n)} + 1 ],  w_n = (n-1)/(n+1),
                 with rho_EDE(a_c) fixed by f_EDE = rho_EDE(a_c) / rho_tot(a_c) (solved by iteration).
    user rho_x   any callable rho_x(z) returning a physical density omega_x(z) (units of rho_crit,100).
    Sound speed  c_s = c / sqrt(3 (1+R)),  R = 3 rho_b / (4 rho_g) = (3 omega_b / 4 omega_g0) a.
    r_s(z) = int_z^inf c_s dz'/H(z') = int_{-inf}^{ln a} c_s/(a H) dln a   (Gauss-Legendre in ln a; the
             a -> 0 tail is added analytically from the local power-law slope).
    D_C(z) = c int_0^z dz'/H(z');  D_M = D_C (flat), (c/H0)/sqrt(Ok) sinh(sqrt(Ok) H0 D_C/c) (open), sin (closed)
    D_A = D_M/(1+z);  D_L = (1+z) D_M;  mu = 5 log10(D_L / 10 pc);  D_H = c/H(z);
    D_V = [z D_M^2 D_H]^(1/3);  theta_* = r_s(z_*)/D_M(z_*).
    z_* (Hu & Sugiyama 1996 eq. E-1) and z_d (Eisenstein & Hu 1998 eq. 4) use omega_m = omega_b + omega_c
    + omega_nu(massive, today) and omega_b.
    r_d (Aubourg et al. 2015 eq. 16): 55.154 exp[-72.3 (omega_nu+0.0006)^2] / (omega_cb^0.25351 omega_b^0.12807) Mpc,
    and eq. 17 for N_eff != 3.046.

ASSUMPTIONS AND VALIDITY
    * Homogeneous FRW background only; no perturbations; instantaneous decoupling at the fitted z_* / z_d.
    * IMPORTANT: the EH98 z_d fit is defined with a different drag optical-depth convention from CAMB. For
      Planck 2018 parameters it gives z_d ~ 1021 (CAMB: 1059.94), so r_s(z_d^EH98) is ~2-3% LARGER than
      CAMB's r_drag = 147.09 Mpc. Aubourg et al. 2015: "There are different conventions in use for defining
      r_d, which differ at the 1-2% level, but ratios of r_d for different cosmologies are independent of
      the convention". Use r_d_aubourg (CAMB convention, LCDM + N_eff only) or r_d('calibrated') for
      absolute values, and RATIOS of integrated r_s at a fixed convention for extended models (EDE, rho_x).
    * Likewise the raw HS96 z_* is 1091.9 for Planck 2018 (CAMB 1089.92, +0.18%), which moves 100 theta_*
      by -0.12% (4 Planck sigma) and h by about +0.6%. The DEFAULT z_* and the 'calibrated' z_drag are
      therefore the HS96 / EH98 fits times a constant (1089.92/HS96 and 1059.94/EH98 at the Planck 2018
      TT,TE,EE+lowE+lensing means). Checked on two other Planck Table 2 columns not used for the
      calibration: z_* within 1.4e-5, z_drag within 8e-6, theta_* within 5e-5, r_d within 1.2e-4.
      Raw fits stay available (method='hs96' / 'eh98').
    * The HS96 / EH98 fits assume standard recombination: they do not know about EDE, varying m_e, etc.
      (EDE changes H(z) near recombination and thus z_* slightly; a fit cannot capture that.) For models
      that change recombination physics, pass z_star / z_drag explicitly.
    * Fits valid for 0.0025 <= omega_b <= 0.25 and 0.025 <= omega_m <= 0.64 (HS96 App. E); refused outside.
      Aubourg eq. 16 only for N_eff = 3.046, sum m_nu < 0.6 eV, omega_b, omega_cb near Planck.
    * 0.2 <= h <= 2; omega_b >= 0, omega_c >= 0; z >= 0; EDE 0 <= f < 1, w_n > -1. A model with
      H^2 <= 0 anywhere on the integration path (e.g. a closed universe that recollapses) raises ValueError.

UNITS
    The Python API uses cosmology units, as the brief requires: H in km/s/Mpc, distances in Mpc,
    densities as omega = Omega h^2, temperatures in K, neutrino masses in eV. Helpers H_SI (1/s) and
    Mpc_to_m (metres) convert to SI via unit_tools (Mpc = 1e6 * 648000/pi au, IAU exact).

PYTHON USAGE
    import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
    from cosmo_background import Cosmology, solve_h_from_theta
    cp = Cosmology(h=0.6736, omega_b=0.02237, omega_c=0.1200)     # Planck 2018 LCDM, one 0.06 eV nu
    cp.H(0.5), cp.D_M(0.5), cp.distance_modulus(0.05)
    s = cp.cmb_summary()   # z_star, r_star, theta100, z_drag_EH98, r_d_aubourg, ...
    ede = Cosmology(h=0.72, omega_b=0.0226, omega_c=0.130, ede=dict(f=0.1, z_c=3500, n=3))
    solve_h_from_theta(1.04110, omega_b=0.02237, omega_c=0.1200)   # -> h ~ 0.674

COMMAND LINE
    python3 .claude/skills/conundrum/scripts/cosmo_background.py cmb --H0 67.36 --omega-b 0.02237 --omega-c 0.12
    python3 .../cosmo_background.py distances --H0 "67.36 km/s/Mpc" --omega-b 0.02237 --omega-c 0.12 --z 0.1 0.51 2.33
    python3 .../cosmo_background.py bao --H0 67.36 --omega-b 0.02237 --omega-c 0.12 --z 0.51 --rd aubourg
    python3 .../cosmo_background.py solve-h --theta100 1.04110 --omega-b 0.02237 --omega-c 0.12 --ede-f 0.1 --ede-zc 3500 --ede-n 3
    python3 .../cosmo_background.py selftest
"""
from __future__ import annotations

import math
import sys

import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import unit_tools as ut  # noqa: E402

# ---------------------------------------------------------------- constants (SI, from unit_tools)
C_KMS = ut.C / 1e3                                   # speed of light, km/s
MPC_M = ut.Q("1 Mpc").si                             # metres
H100_SI = 1e5 / MPC_M                                # 100 km/s/Mpc in 1/s
RHO_CRIT100 = 3.0 * H100_SI**2 / (8.0 * math.pi * ut.G)   # kg/m^3
SIGMA_SB = ut.Q("1 sigma_SB").si
EV_J = ut.E_CHARGE
NU_FAC = 7.0 / 8.0 * (4.0 / 11.0) ** (4.0 / 3.0)     # rho_nu / rho_gamma per massless species
ZETA3 = 1.2020569031595942
PI = math.pi


def omega_gamma(T_cmb: float = 2.7255) -> float:
    """Photon physical density omega_g = rho_g / rho_crit,100, with rho_g c^2 = 4 sigma T^4 / c."""
    return 4.0 * SIGMA_SB * T_cmb**4 / ut.C**3 / RHO_CRIT100


def H_SI(H_kms_mpc: float) -> float:
    """Convert H from km/s/Mpc to 1/s."""
    return H_kms_mpc * 1e3 / MPC_M


def Mpc_to_m(d_mpc: float) -> float:
    return d_mpc * MPC_M


# ---------------------------------------------------------------- Gauss-Legendre helper
_GL_X, _GL_W = np.polynomial.legendre.leggauss(16)


def _gl_nodes(x0: float, x1: float, panels: int):
    """Composite 16-point Gauss-Legendre nodes and weights on [x0, x1]."""
    edges = np.linspace(x0, x1, panels + 1)
    half = 0.5 * np.diff(edges)
    mid = 0.5 * (edges[1:] + edges[:-1])
    x = (mid[:, None] + half[:, None] * _GL_X[None, :]).ravel()
    w = (half[:, None] * _GL_W[None, :]).ravel()
    return x, w


# ---------------------------------------------------------------- massive-neutrino Fermi-Dirac factor
def _F_direct(y: np.ndarray) -> np.ndarray:
    q, wq = _gl_nodes(0.0, 60.0, 24)
    y = np.atleast_1d(y)[:, None]
    integ = q[None, :] ** 2 * np.sqrt(q[None, :] ** 2 + y**2) / (np.exp(q[None, :]) + 1.0)
    return (120.0 / (7.0 * PI**4)) * (integ * wq[None, :]).sum(axis=1)


_LNY = np.linspace(math.log(1e-4), math.log(1e7), 3001)
_LNF = np.log(_F_direct(np.exp(_LNY)))
_F_NR = 180.0 * ZETA3 / (7.0 * PI**4)          # F(y) -> _F_NR * y for y >> 1


def F_nu(y):
    """rho_massive / rho_massless at the same temperature, for y = m c^2 / (k_B T_nu)."""
    y = np.asarray(y, dtype=float)
    out = np.exp(np.interp(np.log(np.clip(y, 1e-4, 1e7)), _LNY, _LNF))
    out = np.where(y > 1e7, _F_NR * y, out)
    return out


# ---------------------------------------------------------------- fitting formulas
def _check_fit_range(omega_b, omega_m):
    if not (0.0025 <= omega_b <= 0.25 and 0.025 <= omega_m <= 0.64):
        raise ValueError(f"HS96/EH98 fits valid for 0.0025<=omega_b<=0.25, 0.025<=omega_m<=0.64; got {omega_b}, {omega_m}")


def z_star_HS96(omega_b: float, omega_m: float) -> float:
    """Hu & Sugiyama 1996 eq. (E-1): redshift of last scattering."""
    _check_fit_range(omega_b, omega_m)
    g1 = 0.0783 * omega_b**-0.238 / (1.0 + 39.5 * omega_b**0.763)
    g2 = 0.560 / (1.0 + 21.1 * omega_b**1.81)
    return 1048.0 * (1.0 + 0.00124 * omega_b**-0.738) * (1.0 + g1 * omega_m**g2)


def z_drag_EH98(omega_b: float, omega_m: float, prefactor: float = 1291.0) -> float:
    """Eisenstein & Hu 1998 eq. (4) (prefactor 1291); HS96 eq. (E-2) is the same with 1345."""
    _check_fit_range(omega_b, omega_m)
    b1 = 0.313 * omega_m**-0.419 * (1.0 + 0.607 * omega_m**0.674)
    b2 = 0.238 * omega_m**0.223
    return prefactor * omega_m**0.251 / (1.0 + 0.659 * omega_m**0.828) * (1.0 + b1 * omega_b**b2)


def r_d_aubourg(omega_b: float, omega_cb: float, omega_nu: float = 0.0006442, N_eff: float = 3.046) -> float:
    """Aubourg et al. 2015 (PRD 92, 123516) eq. 16 (N_eff = 3.046) or eq. 17 (other N_eff); Mpc, CAMB convention."""
    if not (0.015 <= omega_b <= 0.03 and 0.09 <= omega_cb <= 0.2):
        raise ValueError("Aubourg r_d fit calibrated only near Planck omega_b, omega_cb")
    if abs(N_eff - 3.046) < 1e-9:
        return 55.154 * math.exp(-72.3 * (omega_nu + 0.0006) ** 2) / (omega_cb**0.25351 * omega_b**0.12807)
    return (56.067 * math.exp(-49.7 * (omega_nu + 0.002) ** 2)
            / (omega_cb**0.2436 * omega_b**0.128876 * (1.0 + (N_eff - 3.046) / 30.60)))


# CAMB-convention calibration of the EH98 z_d at the Planck 2018 reference model (TT,TE,EE+lowE+lensing):
# z_drag(CAMB) = 1059.94 (Planck 2018 VI Table 2). Applied as a constant ratio; labelled "calibrated".
_ZD_PLANCK_CAMB = 1059.94


# ---------------------------------------------------------------- the model
class Cosmology:
    """Homogeneous FRW background. See the module docstring for the model.

    h: H0 / (100 km/s/Mpc).  omega_b, omega_c: physical densities.  N_eff: total effective neutrino number.
    m_nu: tuple of masses (eV) of the MASSIVE species (default one 0.06 eV state, Planck 2018 baseline).
    T_cmb: K (0 switches off photons and neutrinos).  Omega_k: curvature today.  w0, wa: CPL dark energy.
    ede: None or dict(f=..., z_c=..., n=...) or dict(f, z_c, w_n=...).  rho_x: None or callable z -> omega_x(z).
    """

    def __init__(self, h, omega_b, omega_c, N_eff=3.046, m_nu=(0.06,), T_cmb=2.7255, Omega_k=0.0,
                 w0=-1.0, wa=0.0, ede=None, rho_x=None):
        if not (0.2 <= h <= 2.0):
            raise ValueError(f"h={h} outside 0.2..2")
        if omega_b < 0 or omega_c < 0 or N_eff < 0 or T_cmb < 0:
            raise ValueError("omega_b, omega_c, N_eff, T_cmb must be >= 0")
        self.h, self.omega_b, self.omega_c = float(h), float(omega_b), float(omega_c)
        self.N_eff, self.T_cmb, self.Omega_k = float(N_eff), float(T_cmb), float(Omega_k)
        self.w0, self.wa = float(w0), float(wa)
        self.m_nu = tuple(float(m) for m in m_nu if m > 0)
        g = self.N_eff / 3.0
        self.g_massive = g
        self.N_massless = self.N_eff - g * len(self.m_nu)
        if self.N_massless < -1e-12:
            raise ValueError("more massive species than N_eff allows")
        self.omega_g0 = omega_gamma(self.T_cmb) if self.T_cmb > 0 else 0.0
        T_nu0 = (4.0 / 11.0) ** (1.0 / 3.0) * self.T_cmb
        # CAMB convention: a massive species with weight g = N_eff/3 is a degeneracy-1 Fermi-Dirac gas at
        # temperature g^(1/4) T_nu0, so rho_rel = g x (one standard species) and rho_NR ∝ g^(3/4) m.
        T_eff = T_nu0 * g**0.25 if g > 0 else T_nu0
        self.y_nu = tuple(m * EV_J / (ut.K_B * T_eff) for m in self.m_nu) if self.T_cmb > 0 else ()
        if self.m_nu and self.T_cmb == 0:
            raise ValueError("massive neutrinos need T_cmb > 0")
        self.rho_x = rho_x
        self.omega_k = self.Omega_k * self.h**2
        # EDE
        self.ede = None
        if ede:
            f = float(ede["f"])
            if not (0.0 <= f < 1.0):
                raise ValueError("EDE fraction f must be in [0, 1)")
            wn = float(ede["w_n"]) if "w_n" in ede else (float(ede["n"]) - 1.0) / (float(ede["n"]) + 1.0)
            if wn <= -1.0:
                raise ValueError("EDE w_n must exceed -1")
            self.ede = dict(f=f, z_c=float(ede["z_c"]), w_n=wn, a_c=1.0 / (1.0 + float(ede["z_c"])), rho_c=0.0)
        # closure for dark energy (iterate because f_EDE refers to rho_tot(a_c), which includes DE)
        self.omega_de0 = 0.0
        for _ in range(50):
            if self.ede:
                a_c = self.ede["a_c"]
                rest = float(self._omega_nonede(np.array([a_c]))[0])
                self.ede["rho_c"] = self.ede["f"] / (1.0 - self.ede["f"]) * rest
            new = self.h**2 - self.omega_k - float(self._omega_matter_rad_x(np.array([1.0]))[0])
            if abs(new - self.omega_de0) < 1e-15:
                self.omega_de0 = new
                break
            self.omega_de0 = new
        if self.omega_de0 < -1e-12 and not (self.w0 == -1.0 and self.wa == 0.0):
            raise ValueError("closure gives negative dark-energy density with dynamical w; check inputs")
        if abs(self.omega_de0) < 1e-14:
            self.omega_de0 = 0.0

    # ---- component densities (physical omega units) as functions of a (numpy arrays)
    def omega_nu_massive(self, a):
        a = np.asarray(a, dtype=float)
        out = np.zeros_like(a)
        for y in self.y_nu:
            out += self.g_massive * NU_FAC * self.omega_g0 * a**-4 * F_nu(y * a)
        return out

    def omega_rad(self, a):
        a = np.asarray(a, dtype=float)
        return (self.omega_g0 * (1.0 + NU_FAC * self.N_massless)) * a**-4

    def omega_ede(self, a):
        a = np.asarray(a, dtype=float)
        if not self.ede:
            return np.zeros_like(a)
        e = self.ede
        x = np.clip(a / e["a_c"], 1e-300, None)
        expo = np.clip(3.0 * (1.0 + e["w_n"]) * np.log(x), -700, 700)
        return 2.0 * e["rho_c"] / (np.exp(expo) + 1.0)

    def omega_x(self, a):
        a = np.asarray(a, dtype=float)
        if self.rho_x is None:
            return np.zeros_like(a)
        return np.asarray([float(self.rho_x(1.0 / ai - 1.0)) for ai in np.ravel(a)]).reshape(a.shape)

    def omega_de(self, a):
        a = np.asarray(a, dtype=float)
        if self.omega_de0 == 0.0:
            return np.zeros_like(a)
        return self.omega_de0 * a ** (-3.0 * (1.0 + self.w0 + self.wa)) * np.exp(-3.0 * self.wa * (1.0 - a))

    def _omega_matter_rad_x(self, a):
        a = np.asarray(a, dtype=float)
        return ((self.omega_b + self.omega_c) * a**-3 + self.omega_rad(a) + self.omega_nu_massive(a)
                + self.omega_ede(a) + self.omega_x(a))

    def _omega_nonede(self, a):
        a = np.asarray(a, dtype=float)
        return ((self.omega_b + self.omega_c) * a**-3 + self.omega_rad(a) + self.omega_nu_massive(a)
                + self.omega_x(a) + self.omega_de(a))

    def omega_total(self, a):
        """Sum of physical densities (no curvature), omega units."""
        return self._omega_matter_rad_x(a) + self.omega_de(a)

    # ---- expansion rate
    def H_of_a(self, a):
        a = np.asarray(a, dtype=float)
        E2 = self.omega_total(a) + self.omega_k * a**-2
        if np.any(E2 <= 0):
            raise ValueError("H^2 <= 0 on the requested range (recollapse or inconsistent inputs)")
        return 100.0 * np.sqrt(E2)

    def H(self, z):
        """H(z) in km/s/Mpc."""
        return self.H_of_a(1.0 / (1.0 + np.asarray(z, dtype=float)))

    @property
    def H0(self):
        return 100.0 * self.h

    @property
    def omega_nu(self):
        """Massive-neutrino physical density today."""
        return float(self.omega_nu_massive(np.array([1.0]))[0]) if self.y_nu else 0.0

    @property
    def omega_m(self):
        return self.omega_b + self.omega_c + self.omega_nu

    @property
    def Omega_m(self):
        return self.omega_m / self.h**2

    # ---- distances (Mpc)
    def D_C(self, z):
        """Line-of-sight comoving distance c int_0^z dz/H, Mpc."""
        z = float(z)
        if z < 0:
            raise ValueError("z must be >= 0")
        if z == 0:
            return 0.0
        U = math.log1p(z)
        u, w = _gl_nodes(0.0, U, max(8, int(16 * U) + 8))
        zz = np.expm1(u)
        return float(np.sum(w * C_KMS * (1.0 + zz) / self.H(zz)))

    def D_M(self, z):
        """Transverse comoving distance, Mpc (Hogg 1999 eq. 16)."""
        dc = self.D_C(z)
        if self.Omega_k == 0.0:
            return dc
        dh0 = C_KMS / self.H0
        sk = math.sqrt(abs(self.Omega_k))
        if self.Omega_k > 0:
            return dh0 / sk * math.sinh(sk * dc / dh0)
        return dh0 / sk * math.sin(sk * dc / dh0)

    def D_A(self, z):
        return self.D_M(z) / (1.0 + z)

    def D_L(self, z):
        return self.D_M(z) * (1.0 + z)

    def distance_modulus(self, z):
        """mu = 5 log10(D_L / 10 pc) = 5 log10(D_L/Mpc) + 25."""
        if z <= 0:
            raise ValueError("distance modulus needs z > 0")
        return 5.0 * math.log10(self.D_L(z)) + 25.0

    def D_H(self, z):
        return C_KMS / float(self.H(z))

    def D_V(self, z):
        if z <= 0:
            raise ValueError("D_V needs z > 0")
        return (z * self.D_M(z) ** 2 * self.D_H(z)) ** (1.0 / 3.0)

    # ---- sound horizon (Mpc)
    def R_baryon(self, a):
        if self.omega_g0 == 0.0:
            return 0.0 * np.asarray(a)
        return 0.75 * self.omega_b / self.omega_g0 * np.asarray(a, dtype=float)

    def _rs_integrand(self, lna):
        a = np.exp(lna)
        cs = C_KMS / np.sqrt(3.0 * (1.0 + self.R_baryon(a)))
        return cs / (a * self.H_of_a(a))

    def r_s(self, z, lna_min=-27.0):
        """Comoving sound horizon r_s(z) = int_z^inf c_s dz/H, Mpc (c_s = c/sqrt(3(1+R)))."""
        z = float(z)
        if z < 0:
            raise ValueError("z must be >= 0")
        lna1 = -math.log1p(z)
        if lna1 <= lna_min:
            raise ValueError("z too large for the integration start")
        x, w = _gl_nodes(lna_min, lna1, max(40, int(6 * (lna1 - lna_min))))
        body = float(np.sum(w * self._rs_integrand(x)))
        # analytic tail for a < a_min: integrand ~ a^p with local slope p
        i0, i1 = self._rs_integrand(np.array([lna_min, lna_min + 0.01]))
        p = (math.log(i1) - math.log(i0)) / 0.01
        if p <= 0:
            raise ValueError("sound-horizon integrand does not converge at a -> 0")
        return body + float(i0) / p

    # ---- CMB / BAO summary
    def z_star(self, method="calibrated"):
        """'hs96': raw Hu & Sugiyama 1996 eq. E-1 (for Planck 2018: 1091.9 vs CAMB 1089.92, +0.18%).
        'calibrated' (default): HS96 x [1089.92 / HS96(Planck 2018 means)], i.e. HS96's parameter
        dependence anchored to CAMB at the Planck point."""
        zs = z_star_HS96(self.omega_b, self.omega_m)
        if method == "hs96":
            return zs
        if method == "calibrated":
            return zs * _zs_calibration()
        raise ValueError(f"unknown z_star method {method!r}")

    def z_drag(self, method="eh98"):
        """'eh98': Eisenstein & Hu 1998 eq. 4 (for Planck: 1020.7, CAMB 1059.94); 'calibrated': x 1059.94/EH98(Planck)."""
        zd = z_drag_EH98(self.omega_b, self.omega_m)
        if method == "eh98":
            return zd
        if method == "calibrated":
            return zd * _zd_calibration()
        raise ValueError(f"unknown z_drag method {method!r}")

    def theta_star(self, z_star=None, method="calibrated"):
        zs = self.z_star(method) if z_star is None else z_star
        return self.r_s(zs) / self.D_M(zs)

    def r_d(self, method="aubourg", z_drag=None):
        """Drag-epoch sound horizon, Mpc. method: 'aubourg' (CAMB convention, fit), 'eh98' (integrated to
        the EH98 z_d; ~2-3% above CAMB), 'calibrated' (integrated to EH98 z_d * 1059.94/z_d^EH98(Planck)),
        or pass z_drag to integrate to that redshift."""
        if z_drag is not None:
            return self.r_s(z_drag)
        if method == "aubourg":
            if self.ede or self.rho_x is not None:
                raise ValueError("Aubourg fit is for standard pre-recombination physics; use 'calibrated' or z_drag")
            return r_d_aubourg(self.omega_b, self.omega_b + self.omega_c, self.omega_nu, self.N_eff)
        if method == "eh98":
            return self.r_s(self.z_drag())
        if method == "calibrated":
            return self.r_s(self.z_drag() * _zd_calibration())
        raise ValueError(f"unknown r_d method {method!r}")

    def cmb_summary(self, z_star=None):
        zs = self.z_star() if z_star is None else z_star
        rs = self.r_s(zs)
        dm = self.D_M(zs)
        zd = self.z_drag()
        zh = self.z_star("hs96")
        out = dict(z_star=zs, z_star_note="calibrated HS96 unless given", r_star_Mpc=rs, D_M_star_Mpc=dm,
                   theta100=100.0 * rs / dm, z_star_HS96_raw=zh, theta100_HS96_raw=100.0 * self.theta_star(zh),
                   z_drag_EH98=zd, r_d_EH98_Mpc=self.r_s(zd),
                   z_drag_calibrated=zd * _zd_calibration(), r_d_calibrated_Mpc=self.r_s(zd * _zd_calibration()),
                   omega_m=self.omega_m, Omega_m=self.Omega_m, omega_nu=self.omega_nu, Omega_DE=self.omega_de0 / self.h**2)
        try:
            out["r_d_aubourg_Mpc"] = self.r_d("aubourg")
        except ValueError as exc:
            out["r_d_aubourg_Mpc"] = f"n/a ({exc})"
        return out

    def bao(self, z, r_d):
        """BAO observables at z for a given r_d (Mpc)."""
        return dict(z=z, DM_over_rd=self.D_M(z) / r_d, DH_over_rd=self.D_H(z) / r_d, DV_over_rd=self.D_V(z) / r_d)


_CAL = {}
_ZS_PLANCK_CAMB = 1089.92   # Planck 2018 VI Table 2, TT,TE,EE+lowE+lensing


def _planck_omega_m():
    if "om" not in _CAL:
        _CAL["om"] = Cosmology(0.6736, 0.02237, 0.1200).omega_m
    return _CAL["om"]


def _zd_calibration():
    """Ratio z_drag(CAMB, Planck 2018 Table 2) / z_drag_EH98(Planck 2018 means)."""
    if "zd" not in _CAL:
        _CAL["zd"] = _ZD_PLANCK_CAMB / z_drag_EH98(0.02237, _planck_omega_m())
    return _CAL["zd"]


def _zs_calibration():
    """Ratio z_*(CAMB, Planck 2018 Table 2) / z_*_HS96(Planck 2018 means)."""
    if "zs" not in _CAL:
        _CAL["zs"] = _ZS_PLANCK_CAMB / z_star_HS96(0.02237, _planck_omega_m())
    return _CAL["zs"]


def solve_h_from_theta(theta100, omega_b, omega_c, z_star=None, method="calibrated", h_lo=0.3, h_hi=1.5,
                       tol=1e-9, **kw):
    """h such that 100*r_s(z_*)/D_M(z_*) = theta100 at fixed omega_b, omega_c and extra components (kw passed
    to Cosmology: N_eff, m_nu, Omega_k, w0, wa, ede, rho_x...). Omega_k (not omega_k) is held fixed.
    z_* from the (calibrated, by default) HS96 fit unless given; z_* then moves with omega_m(nu) only, not with h.
    Bisection; theta increases with h at fixed physical densities."""
    def g(h):
        cp = Cosmology(h, omega_b, omega_c, **kw)
        return 100.0 * cp.theta_star(z_star, method) - theta100
    # A low h can leave no room for dark energy (negative closure); raise h_lo until the model is valid.
    while True:
        try:
            glo = g(h_lo)
            break
        except ValueError:
            h_lo *= 1.05
            if h_lo >= h_hi:
                raise ValueError("no valid model in the h bracket")
    ghi = g(h_hi)
    if glo * ghi > 0:
        raise ValueError(f"theta100={theta100} not bracketed for h in [{h_lo}, {h_hi}]")
    lo, hi = h_lo, h_hi
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        gm = g(mid)
        if (gm > 0) == (ghi > 0):
            hi, ghi = mid, gm
        else:
            lo, glo = mid, gm
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------- self-test
def selftest(verbose: bool = True) -> bool:
    results = []

    def check(name, got, ref, rtol, note=""):
        ok = abs(got - ref) <= rtol * abs(ref)
        results.append(ok)
        if verbose:
            print(f"[{'PASS' if ok else 'FAIL'}] {name}: got {got:.8g}, ref {ref:.8g}, rel diff {abs(got-ref)/abs(ref):.2e} (tol {rtol:.1e}) {note}")
        return ok

    h = 0.7
    dh0 = C_KMS / (100 * h)
    # 1. Einstein-de Sitter (no radiation, Omega_m = 1): D_C = (2c/H0)(1 - 1/sqrt(1+z)) -- exact closed form,
    #    from int_0^z dz/(1+z)^{3/2}.
    eds = Cosmology(h, 0.0, h**2, N_eff=0, m_nu=(), T_cmb=0.0)
    for z in (0.5, 3.0, 1100.0):
        check(f"EdS D_C(z={z}) [Mpc]", eds.D_C(z), 2 * dh0 * (1 - 1 / math.sqrt(1 + z)), 1e-10)
    # 2. de Sitter (Lambda only): D_C = c z/H0, D_L = (1+z) c z / H0.
    ds = Cosmology(h, 0.0, 0.0, N_eff=0, m_nu=(), T_cmb=0.0)
    check("de Sitter D_L(z=2) [Mpc]", ds.D_L(2.0), 3.0 * 2.0 * dh0, 1e-10)
    # 3. Milne (empty, Omega_k = 1): D_M = (c/H0) sinh(ln(1+z)) = (c/H0) z(1+z/2)/(1+z); tests the sinh branch
    #    of Hogg 1999 eq. 16, quoted: "DM = DH 1/sqrt(Ωk) sinh[sqrt(Ωk) DC/DH] for Ωk > 0" (fetch_text, arXiv astro-ph/9905116).
    milne = Cosmology(h, 0.0, 0.0, N_eff=0, m_nu=(), T_cmb=0.0, Omega_k=1.0)
    check("Milne D_M(z=3) [Mpc]", milne.D_M(3.0), dh0 * 3.0 * 2.5 / 4.0, 1e-10)
    #    distance modulus definition, Hogg 1999 eq. 25: "DM ≡ 5 log ( DL / 10 pc )".
    check("Milne mu(z=0.1) [mag]", milne.distance_modulus(0.1),
          5 * math.log10(dh0 * 0.1 * 1.05 * MPC_M / (10 * ut.Q("1 pc").si)), 1e-12)
    # 4. Constant-w limit: flat, DE only with w = -1/3 gives H = H0(1+z), D_C = (c/H0) ln(1+z).
    wq = Cosmology(h, 0.0, 0.0, N_eff=0, m_nu=(), T_cmb=0.0, w0=-1.0 / 3.0)
    check("w=-1/3 D_C(z=4) [Mpc]", wq.D_C(4.0), dh0 * math.log(5.0), 1e-10)
    # 5. CPL definition (Chevallier-Polarski / Linder): w(a) = w0 + wa(1-a) = -1 - (1/3) dln rho/dln a.
    cpl = Cosmology(h, 0.022, 0.12, w0=-0.75, wa=-0.8)
    a0 = 0.5
    dl = (math.log(float(cpl.omega_de(np.array([a0 * 1.0001]))[0])) - math.log(float(cpl.omega_de(np.array([a0 / 1.0001]))[0]))) / (2 * math.log(1.0001))
    check("CPL w(a=0.5) from rho", -1 - dl / 3.0, -0.75 - 0.8 * 0.5, 1e-7)
    # 6. Matter-radiation(-baryon) analytic sound horizon, Eisenstein & Hu 1998 eq. 6 (fetch_text, arXiv
    #    astro-ph/9709112): "s = ∫ cs (1 + z)dt = 2/(3keq) sqrt(6/Req) ln[(sqrt(1 + Rd) + sqrt(Rd + Req))/(1 + sqrt(Req))]",
    #    exact for H^2 ∝ omega_m a^-3 + omega_r a^-4. Model: no Lambda (h^2 = omega_m + omega_r exactly), massless nu.
    ob, oc = 0.0224, 0.12
    og = omega_gamma(2.7255)
    orad = og * (1 + NU_FAC * 3.046)
    hmr = math.sqrt(ob + oc + orad)
    mr = Cosmology(hmr, ob, oc, N_eff=3.046, m_nu=())
    a_eq = orad / (ob + oc)
    k_eq = math.sqrt(2 * (ob + oc) * 100.0**2 / a_eq) / C_KMS          # 1/Mpc, = a_eq H(a_eq)/c
    R_eq = 0.75 * ob / og * a_eq
    for z in (1060.0, 300.0):
        Rd = 0.75 * ob / og / (1 + z)
        s_an = 2 / (3 * k_eq) * math.sqrt(6 / R_eq) * math.log((math.sqrt(1 + Rd) + math.sqrt(Rd + R_eq)) / (1 + math.sqrt(R_eq)))
        check(f"EH98 eq.6 matter+radiation r_s(z={z:.0f}) [Mpc]", mr.r_s(z), s_an, 1e-8)
    # 7a. Non-relativistic limit of the Fermi-Dirac quadrature, exact definition: one nu+nubar species at
    #     T_nu0 = (4/11)^(1/3) T_cmb has n = (3 zeta(3)/(2 pi^2)) (k T/(hbar c))^3, so omega_nu = m n / rho_crit,100
    #     (instantaneous decoupling, N_eff = 3 -> g = 1). Kinetic correction at y ~ 6000 is ~1e-7.
    nu1 = Cosmology(0.7, 0.022, 0.12, N_eff=3.0, m_nu=(1.0,))
    Tn = (4 / 11) ** (1 / 3) * 2.7255
    n_nu = 3 * ZETA3 / (2 * PI**2) * (ut.K_B * Tn / (ut.HBAR * ut.C)) ** 3
    check("omega_nu, 1 eV, N_eff=3 (m n / rho_crit)", nu1.omega_nu, EV_J / ut.C**2 * n_nu / RHO_CRIT100, 1e-5)
    # 7b. Lesgourgues & Pastor 2006 (arXiv astro-ph/0603494) eq. 12: "Ω ν = ∑ imi / (93.14 h2 eV)", which includes
    #     non-instantaneous decoupling; the CAMB scaling g^(3/4) with N_eff = 3.046 approximates that distortion,
    #     so agreement is expected only to ~0.2% (tolerance 0.3%, physics-convention difference, not numerics).
    nu2 = Cosmology(0.7, 0.022, 0.12, N_eff=3.046, m_nu=(1.0,))
    check("omega_nu, 1 eV, N_eff=3.046 vs 1/93.14 eV", nu2.omega_nu, 1 / 93.14, 3e-3)
    # 8. EDE fluid: Poulin et al. 2019 (arXiv 1811.04083) eq. 2, "wϕ(z) = (1 + wn)/(1 + (ac/a)^{3(1+wn)}) − 1"
    #    against -1 - (1/3) dln rho/dln a of the code's eq.-1 density; and f_EDE = rho_EDE(a_c)/rho_tot(a_c) by definition.
    ed = Cosmology(0.72, 0.0226, 0.130, ede=dict(f=0.1, z_c=3500.0, n=3))
    wn = 0.5
    ac = 1 / 3501.0
    for a in (ac / 3, ac, 3 * ac):
        d = (math.log(float(ed.omega_ede(np.array([a * 1.0001]))[0])) - math.log(float(ed.omega_ede(np.array([a / 1.0001]))[0]))) / (2 * math.log(1.0001))
        check(f"EDE w(a/a_c={a/ac:.2f}) Poulin eq.2", -1 - d / 3, (1 + wn) / (1 + (ac / a) ** (3 * (1 + wn))) - 1, 1e-6)
    fe = float(ed.omega_ede(np.array([ac]))[0] / ed.omega_total(np.array([ac]))[0])
    check("EDE f_EDE at z_c (definition)", fe, 0.1, 1e-9)

    # 9. Planck 2018 VI (arXiv 1807.06209) Table 2, column TT,TE,EE+lowE+lensing (posterior means), fetch_text p. 15-16:
    #    "Ωbh2 ... 0.02237± 0.00015", "Ωch2 ... 0.1200± 0.0012", "H0 ... 67.36± 0.54",
    #    "z∗ ... 1089.92± 0.25", "r∗ [Mpc] ... 144.43± 0.26", "100θ∗ ... 1.04110± 0.00031",
    #    "zdrag ... 1059.94± 0.30", "rdrag [Mpc] ... 147.09± 0.26"; baseline "a single massive neutrino of mass mν = 0.06 eV".
    #    These are posterior means of a CAMB+recombination-code calculation, not one model evaluated at mean
    #    parameters, so tolerances are set at about the quoted 1-sigma (r_*: 0.18%; theta: 0.03%; r_drag: 0.18%).
    pl = Cosmology(0.6736, 0.02237, 0.1200)
    check("Planck r_s(z_*=1089.92) [Mpc]", pl.r_s(1089.92), 144.43, 0.0018, "(direct integration at Planck's z_*)")
    check("Planck 100 theta_* (z_*=1089.92)", 100 * pl.theta_star(1089.92), 1.04110, 0.0003)
    check("Planck r_s(z_drag=1059.94) [Mpc]", pl.r_s(1059.94), 147.09, 0.0018, "(direct integration at Planck's z_drag)")
    # Raw HS96 eq. E-1. HS96 App. E (fetch_text, arXiv astro-ph/9510117): "fitting functions in this Appendix are
    #    designed to be valid at the percent level", so the published accuracy claim (1%) is the tolerance. The
    #    actual offset is +0.18% (1091.9 vs 1089.92), which shifts 100 theta_* by -0.12% (4 Planck sigma); hence
    #    the 'calibrated' default. The raw-theta check's 0.2% tolerance is that propagated offset, stated not tuned.
    check("Planck z_* (raw HS96 fit, 'percent level')", pl.z_star("hs96"), 1089.92, 1e-2)
    check("Planck 100 theta_* with raw HS96 z_*", 100 * pl.theta_star(method="hs96"), 1.04110, 2e-3)
    # Aubourg eq. 16 claims "accurate to 0.021%" vs CAMB; posterior-mean comparison so allow 0.18% (1 sigma).
    check("Planck r_d Aubourg eq.16 [Mpc]", pl.r_d("aubourg"), 147.09, 0.0018)
    # 9b. Two OTHER Planck 2018 Table 2 columns, not used for the calibration (fetch_text p. 16):
    #     TT+lowE: "Ωbh2 0.02212", "Ωch2 0.1206", "H0 66.88", "z∗ 1090.30", "r∗ 144.46", "100θ∗ 1.04097",
    #              "zdrag 1059.39", "rdrag 147.21";
    #     TE+lowE: "Ωbh2 0.02249", "Ωch2 0.1177", "H0 68.44", "z∗ 1089.57", "r∗ 144.95", "100θ∗ 1.04156",
    #              "zdrag 1060.03", "rdrag 147.59".
    #     Tolerances = the column's quoted 1 sigma (theta 0.00046-0.00049 -> 0.045%; r 0.48 Mpc -> 0.33%;
    #     z 0.41-0.54 -> 0.05%), since posterior means of nonlinear derived quantities differ from values at mean inputs.
    for lab, ob_, oc_, H0_, zs_, rs_, th_, zd_, rd_ in (("TT+lowE", 0.02212, 0.1206, 66.88, 1090.30, 144.46, 1.04097, 1059.39, 147.21),
                                                       ("TE+lowE", 0.02249, 0.1177, 68.44, 1089.57, 144.95, 1.04156, 1060.03, 147.59)):
        cc = Cosmology(H0_ / 100, ob_, oc_)
        check(f"{lab} calibrated z_*", cc.z_star(), zs_, 5e-4)
        check(f"{lab} r_* [Mpc]", cc.r_s(cc.z_star()), rs_, 3.3e-3)
        check(f"{lab} 100 theta_*", 100 * cc.theta_star(), th_, 4.5e-4)
        check(f"{lab} calibrated z_drag", cc.z_drag("calibrated"), zd_, 5e-4)
        check(f"{lab} r_d calibrated (integrated) [Mpc]", cc.r_d("calibrated"), rd_, 3.3e-3)
        check(f"{lab} r_d Aubourg [Mpc]", cc.r_d("aubourg"), rd_, 3.3e-3)
    # 10. EH98 eq. 4 = 0.96 x HS96 eq. E-2: EH98 text "we have reduced zd by a factor of 0.96 from HS96".
    check("EH98 z_d = 0.96 x HS96 z_d", z_drag_EH98(0.0224, 0.143), 0.96 * z_drag_EH98(0.0224, 0.143, 1345.0), 1e-3,
          "(1291/1345 = 0.95985)")
    # 11. Inverse solve: Planck 100 theta_* = 1.04110 at Planck omega_b, omega_c, z_* = 1089.92 must return
    #     H0 = 67.36 +- 0.54 (Table 2); tolerance 0.5 km/s/Mpc (< 1 sigma), and round trip to 1e-6.
    hsol = solve_h_from_theta(1.04110, 0.02237, 0.1200, z_star=1089.92)
    check("inverse solve H0 from Planck theta_* [km/s/Mpc]", 100 * hsol, 67.36, 0.5 / 67.36)
    check("inverse solve round trip", 100 * Cosmology(hsol, 0.02237, 0.1200).theta_star(1089.92), 1.04110, 1e-6)

    n_ok = sum(results)
    if verbose:
        print(f"{n_ok}/{len(results)} checks passed")
        print("info: Planck EH98 z_d =", round(pl.z_drag(), 2), " r_s(z_d^EH98) =", round(pl.r_s(pl.z_drag()), 3),
              "Mpc (convention differs from CAMB; see docstring)")
    return n_ok == len(results)


# ---------------------------------------------------------------- command line
def _parse_H0(text: str) -> float:
    try:
        return float(text)
    except ValueError:
        return ut.Q(text).to("km/s/Mpc")


def _build(args) -> Cosmology:
    H0 = _parse_H0(args.H0) if args.H0 is not None else None
    ede = dict(f=args.ede_f, z_c=args.ede_zc, n=args.ede_n) if args.ede_f else None
    kw = dict(N_eff=args.Neff, m_nu=tuple(args.mnu), T_cmb=args.Tcmb, Omega_k=args.Ok, w0=args.w0, wa=args.wa, ede=ede)
    return H0, kw


def main(argv=None) -> int:
    import argparse
    import json
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["selftest", "distances", "cmb", "bao", "solve-h"])
    ap.add_argument("--H0", default=None, help='H0, e.g. 67.36 or "67.36 km/s/Mpc"')
    ap.add_argument("--omega-b", type=float, default=0.02237)
    ap.add_argument("--omega-c", type=float, default=0.1200)
    ap.add_argument("--Neff", type=float, default=3.046)
    ap.add_argument("--mnu", type=float, nargs="*", default=[0.06], help="masses (eV) of massive species")
    ap.add_argument("--Tcmb", type=float, default=2.7255)
    ap.add_argument("--Ok", type=float, default=0.0)
    ap.add_argument("--w0", type=float, default=-1.0)
    ap.add_argument("--wa", type=float, default=0.0)
    ap.add_argument("--ede-f", type=float, default=0.0)
    ap.add_argument("--ede-zc", type=float, default=3500.0)
    ap.add_argument("--ede-n", type=float, default=3.0)
    ap.add_argument("--z", type=float, nargs="*", default=[0.51])
    ap.add_argument("--zstar", type=float, default=None, help="override z_* (else HS96 fit)")
    ap.add_argument("--rd", default="aubourg", help="aubourg | eh98 | calibrated | <number> (Mpc)")
    ap.add_argument("--theta100", type=float, default=1.04110)
    a = ap.parse_args(argv)
    if a.cmd == "selftest":
        return 0 if selftest() else 1
    H0, kw = _build(a)
    if a.cmd == "solve-h":
        h = solve_h_from_theta(a.theta100, a.omega_b, a.omega_c, z_star=a.zstar, **kw)
        cp = Cosmology(h, a.omega_b, a.omega_c, **kw)
        print(json.dumps(dict(H0_km_s_Mpc=100 * h, z_star=cp.z_star() if a.zstar is None else a.zstar,
                              r_star_Mpc=cp.r_s(cp.z_star() if a.zstar is None else a.zstar),
                              Omega_m=cp.Omega_m), indent=1))
        return 0
    if H0 is None:
        ap.error("--H0 required")
    cp = Cosmology(H0 / 100.0, a.omega_b, a.omega_c, **kw)
    if a.cmd == "cmb":
        print(json.dumps(cp.cmb_summary(a.zstar), indent=1, default=str))
    elif a.cmd == "distances":
        for z in a.z:
            print(json.dumps(dict(z=z, H_km_s_Mpc=float(cp.H(z)), D_C_Mpc=cp.D_C(z), D_M_Mpc=cp.D_M(z), D_A_Mpc=cp.D_A(z),
                                  D_L_Mpc=cp.D_L(z), D_H_Mpc=cp.D_H(z), mu_mag=cp.distance_modulus(z) if z > 0 else None)))
    elif a.cmd == "bao":
        try:
            rd = float(a.rd)
        except ValueError:
            rd = cp.r_d(a.rd)
        print(json.dumps(dict(r_d_Mpc=rd), indent=None))
        for z in a.z:
            print(json.dumps(cp.bao(z, rd)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
