#!/usr/bin/env python3
"""gw_coherent_fusion: tree-level graviton fusion g g -> gamma gamma (and g g -> phi phi) inside ONE coherent
gravitational-wave packet, for a chosen angular polarisation pattern and radial (spectral) profile. Returns the
in-out pair yield P (mean number of pairs made by the whole packet, leading order) and, for comparison with
Blas & Oller (B&O, arXiv:2607.24930, eq. 8), the "rate" P/T obtained with their 2 pi delta(0) -> T step.
Built on qft_second_order's physical (Lorentz-invariant) amplitudes with their phases; numpy only.

Model (natural units hbar = c = 1, Heaviside-Lorentz; G = 1/M_Pl^2)
    Coherent state |alpha> = exp( int dk~ alpha(k).a^dag(k) - h.c. ) |0>, dk~ = d^3k/((2pi)^3 2|k|), with
        alpha(k) = f(|k|) E(k^),   E(k^) = c_R(k^) eps_R(k^) + c_L(k^) eps_L(k^)      (TT tensor on the sphere)
    eps_R/L the helicity +-2 tensors of qft_second_order (e_theta, e_phi of k^ about the lab z axis). The angular
    pattern is normalised <|c_R|^2 + |c_L|^2>_sphere = 1, so the mean graviton number is
        N = int dk~ |alpha|^2 = (1/4 pi^2) int k |f(k)|^2 dk  ~=  (w/4 pi^2) int |f|^2 dk.
    This is the convention of B&O eqs. 2-4 / S4 (a_lam(k)|f> = f_lam(k)|f>, measure d^3k/((2pi)^3 2k)); B&O's
    top hat per helicity Theta = sqrt(2 pi^2 N/(w sigma)) is our c_R = c_L = 1/sqrt2 with f = sqrt2 Theta.
    Leading-order amplitude for the pair (p1, p2) (the 1/2! of the exponential cancels against the two ways of
    taking one graviton from each factor, exactly as in qft_second_order Part B):
        F(p1, p2) = (1/2) int dk1~ dk2~ alpha(k1) alpha(k2) M(k1, E(k1^), k2, E(k2^) -> p1, p2) (2pi)^4 delta^4(k1+k2-p1-p2)
    M = qft_second_order.amplitude_gg_to_photons / _to_scalars, which is bilinear in the two polarisation tensors,
    so the pattern's tensors (with their phases) are fed in directly: no helicity phase convention is chosen here.
    Yield (pairs; sym = 1/2 for photons and a real scalar, 1 for a complex scalar):
        P = sym int dPi1 dPi2 sum_final |F|^2.
    Narrow-band reduction (sigma << w; exact Jacobian d^3k = (ab/K) da db dphi, the ab cancels against 1/(4ab)):
    for K = (K0, K) the graviton pairs with k1 + k2 = K lie on a ring k1,2 = K/2 -+ rho (cos phi u1 + sin phi u2),
    rho = sqrt(w^2 - K^2/4), and
        F = C(K0) / (32 pi^2 |K|) int_0^2pi dphi M(phi),       C(K0) = int da f(a) f(K0 - a)
        P = J_f * I_ang,   J_f = int dK0 C(K0)^2,
        I_ang = sym (2pi)^-4 (32 pi^2)^-3 int_0^{2w} d|K| int dOmega_K int dOmega*_gamma beta sum_final |int dphi M|^2
    (dOmega* in the CM of K, beta = |p*|/E* = 1 for massless). M is evaluated at |k1| = |k2| = w, K0 = 2w,
    s = 4w^2 - |K|^2 (exactly B&O's S6 kinematics). Then P = c_tot G^2 N^2 w^3 sigma, c_tot a pure number for each
    (pattern, profile, final state). Profiles (sigma = B&O's sigma_w):
        'tophat'  : f = Theta on [w - sigma/2, w + sigma/2]  -> J_f = (32 pi^4/3) N^2 sigma/w^2
        'gaussian': f = Theta exp(-(k-w)^2/(2 sigma^2))     -> J_f = 16 sqrt(2pi) pi^4 N^2 sigma/w^2
    B&O's 2 pi delta(0) -> T (S6) replaces 2pi delta(E - E') by T in the quartic profile integral, i.e. it defines
        T_eff = 2 pi J_f / (int f dk)^4 = (4 pi/3)/sigma (top hat),  sqrt(pi/2)/sigma (Gaussian),
    and their "rate" is P / T_eff = c_rate G^2 N^2 w^3 sigma^2, c_rate = c_tot sigma T_eff. With their real-sign
    'unpolarized' amplitudes and the top hat this must give c_rate = 3/(25 pi) (photons) and 7/(450 pi) (massless
    real scalar): the self-test reproduces both.

Patterns (lab z = source axis; iota = polar angle of k^, varphi its azimuth)
    'linear_quadrupole': mass quadrupole oscillating along z: h_+ ~ sin^2 iota, h_x = 0 ->
                         c_R = c_L = sqrt(15/16) sin^2 iota.
    'circular_binary'  : circular binary, orbital axis z: h_+ = (1+cos^2 iota)/2 cos 2Phi, h_x = cos iota sin 2Phi ->
                         c_R = sqrt(5/8) e^{2i varphi} (1+cos iota)^2/2, c_L = sqrt(5/8) e^{2i varphi} (1-cos iota)^2/2
                         (positive-frequency part a e_+ + i b e_x = (a+b) eps_R + (a-b) eps_L; the e^{2i varphi} is the
                         azimuthal retardation of the rotating source; e^{2i varphi} eps_R is smooth at the north pole).
    'pure_circular'    : helicity +2 in every direction, c_R = e^{2i varphi}, c_L = 0 (same-helicity gravitons:
                         zero yield for massless final states, an exact selection rule).
    'isotropic_plus'   : c_R = c_L = 1/sqrt2 with the toolkit's phases (E = eps_plus(k^), 'plus' axes e_theta,
                         e_phi of every direction): B&O's helicity content with ONE explicit phase convention.
    'bo_real_sign'     : B&O eq. 7: c_R = c_L = 1/sqrt2 and every contributing physical helicity amplitude added with
                         a real positive sign, sum_{l1 l2} |c||c| |M_{l1 l2 -> s1 s2}|. Not a quantum state: it is the
                         model whose coefficient B&O print; kept as the reference limit.

Quantity and interpretation (read before quoting a number)
    P is the IN-OUT leading-order pair yield for the coherent state used as an IN-state (= mean pair number at
    O(G^2 N^2)). A momentum-space profile f(|k|) E(k^) with |k| ~ w in all directions of the pattern is, in position
    space, a shell that converges onto the origin for t < 0 and re-expands for t > 0 (time-symmetric field); the
    fusion of non-collinear gravitons happens where the shell is small. P is a TOTAL per packet, not a rate; the
    "rate" P/T_eff is only B&O's bookkeeping, valid as a rate for nothing in particular (T_eff ~ 1/sigma is the
    packet's spectral coherence time). Pairs; photons = 2 x pairs.

Assumptions and validity
    Tree level, flat background, no plasma (massless photons), s << M_Pl^2; narrow band: corrections O(sigma/w) and
    the angular pattern must vary on scales >> sigma/w rad (refused: sigma/w > 0.1); 2 graviton helicities only
    (TT); N >= 1, w > 0, sigma > 0; scalars m >= 0 with s > 4 m^2 (massive: toolkit refuses m^2/s < 1e-8 at a node).
    G^2 N^2 w^3 sigma << 1 (perturbative; refused if P > 0.1). Quadrature (K = 2w sin u, Gauss in u and in the
    polar angle of K). Measured for 'circular_binary' (c_tot, top hat): default grid 0.08992; n_K = n_cK = 11:
    0.08994; n_phi = 48: 0.08984; photon grid 12 x 24: 0.09098 (+1.2%); an older cos-theta grid with every count
    doubled gave 0.0932. Physical-pattern coefficients therefore carry a ~2-4% quadrature uncertainty dominated by
    the CM photon-angle grid (raise n_cg, n_pg for more); the 'bo_real_sign' model is exact to ~1e-9.
    Cost: ~100 microseconds per amplitude (qft_second_order), ~1 min per physical pattern at the default grid.
    B&O's own GW150914 inputs (sigma_w = 200 /s at w = 2 pi 150 /s, sigma/w = 0.21) are REFUSED as not narrow-band.

Units
    Python API natural units (any energy unit, G in its inverse square) for yield_natural; SI for yield_SI
    (energy in J, f in Hz, sigma in rad/s; returns pairs and pairs/s).

Python usage
    import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
    import gw_coherent_fusion as gf
    gf.coefficients("bo_real_sign", "tophat")        # {'c_tot': 0.16, 'c_rate': 3/(25 pi) = 0.0382, ...}
    gf.yield_SI(3.57e47, 150.0, 200.0, pattern="circular_binary", profile="gaussian")   # pairs, pairs/s

Command line (from the project root)
    python3 .claude/skills/conundrum/scripts/gw_coherent_fusion.py selftest
    python3 .claude/skills/conundrum/scripts/gw_coherent_fusion.py table
    python3 .claude/skills/conundrum/scripts/gw_coherent_fusion.py yield --E "2 Msun*c^2" \
        --f "150 Hz" --sigma "200 Hz" --pattern circular_binary --profile tophat
"""
from __future__ import annotations

import argparse
import functools
import math
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (".claude/skills/conundrum/scripts", os.path.join(_HERE, "..", "..", "..", ".claude", "skills",
                                                             "conundrum", "scripts")):
    if os.path.isdir(_p) and _p not in sys.path:
        sys.path.insert(0, _p)

import qft_second_order as q2  # noqa: E402
from unit_tools import C, E_CHARGE, HBAR, Q  # noqa: E402

PI = math.pi
PATTERNS = ("linear_quadrupole", "circular_binary", "pure_circular", "isotropic_plus", "bo_real_sign")
PROFILES = ("tophat", "gaussian")
_ED = np.array([1.0, -1.0, -1.0, -1.0])
_SQ2 = math.sqrt(2.0)


# ------------------------------------------------------------------ polarisation tensors (toolkit convention)
def _basis(n):
    """(e_theta, e_phi) of unit vectors n (...,3): same formula as qft_second_order._transverse_basis."""
    n = np.asarray(n, dtype=float)
    rho = np.hypot(n[..., 0], n[..., 1])
    ph = np.arctan2(n[..., 1], n[..., 0])
    on = rho > 0
    safe = np.where(on, rho, 1.0)
    cp = np.where(on, n[..., 0] / safe, np.cos(ph))
    sp = np.where(on, n[..., 1] / safe, np.sin(ph))
    et = np.stack([n[..., 2] * cp, n[..., 2] * sp, -rho], axis=-1)
    ep = np.stack([-sp, cp, np.zeros_like(cp)], axis=-1)
    return et, ep


def helicity_tensor(n, lam: int) -> np.ndarray:
    """Lower-index helicity tensor eps_{mu nu} = e_mu e_nu, e = (0, (-hel e_theta - i e_phi)/sqrt2), hel = lam/2.

    Quantity: complex (...,4,4), unit norm, TT w.r.t. n; identical to qft_second_order.graviton_polarization(n, lam).
    Valid when: n unit 3-vectors (...,3), lam = +2 or -2."""
    if lam not in (2, -2):
        raise ValueError("lam must be +2 or -2")
    et, ep = _basis(n)
    v = (-(lam // 2) * et - 1j * ep) / _SQ2
    e = np.concatenate([np.zeros(v.shape[:-1] + (1,)), v], axis=-1) * _ED
    return e[..., :, None] * e[..., None, :]


def pattern_coefficients(pattern: str, n):
    """Helicity coefficients (c_R, c_L) of the angular pattern at unit directions n (...,3), normalised so that
    the sphere average of |c_R|^2 + |c_L|^2 is 1. See the module docstring for each pattern.
    Quantity: two complex arrays (dimensionless). Valid when: pattern in PATTERNS."""
    n = np.asarray(n, dtype=float)
    c = n[..., 2]
    ph = np.arctan2(n[..., 1], n[..., 0])
    if pattern == "linear_quadrupole":
        a = math.sqrt(15.0 / 16.0) * (1 - c * c) + 0j
        return a, a
    if pattern == "circular_binary":
        p = math.sqrt(5.0 / 8.0) * np.exp(2j * ph)
        return p * (1 + c) ** 2 / 2, p * (1 - c) ** 2 / 2
    if pattern == "pure_circular":
        return np.exp(2j * ph), np.zeros_like(ph, dtype=complex)
    if pattern in ("isotropic_plus", "bo_real_sign"):
        a = np.full(c.shape, 1 / _SQ2, dtype=complex)
        return a, a
    raise ValueError(f"pattern must be one of {PATTERNS}")


def pattern_tensor(pattern: str, n) -> np.ndarray:
    """E(n) = c_R eps_R(n) + c_L eps_L(n): the coherent-state polarisation tensor field (lower indices, (...,4,4))."""
    cR, cL = pattern(n) if callable(pattern) else pattern_coefficients(pattern, n)
    return cR[..., None, None] * helicity_tensor(n, 2) + cL[..., None, None] * helicity_tensor(n, -2)


# ------------------------------------------------------------------ radial profiles
def profile_factors(profile: str, N: float, omega: float, sigma: float) -> dict:
    """Profile amplitude Theta (fixed by N), J_f = int dK0 C(K0)^2, I_f = int f dk and T_eff = 2 pi J_f / I_f^4.

    Quantity: dict (natural units: Theta in energy^-1 ... as implied by N = (w/4pi^2) int |f|^2 dk).
    Valid when: N > 0, omega > 0, 0 < sigma <= 0.1 omega; profile 'tophat' or 'gaussian'."""
    if not (N > 0 and omega > 0 and sigma > 0):
        raise ValueError("need N > 0, omega > 0, sigma > 0")
    if sigma > 0.1 * omega:
        raise ValueError("narrow-band model: need sigma <= 0.1 omega")
    if profile == "tophat":
        th = math.sqrt(4 * PI ** 2 * N / (omega * sigma))
        J, If = (2.0 / 3.0) * sigma ** 3 * th ** 4, th * sigma
    elif profile == "gaussian":
        th = math.sqrt(4 * PI ** 2 * N / (omega * sigma * math.sqrt(PI)))
        J, If = th ** 4 * sigma ** 3 * PI * math.sqrt(2 * PI), th * sigma * math.sqrt(2 * PI)
    else:
        raise ValueError(f"profile must be one of {PROFILES}")
    return {"Theta": th, "J_f": J, "I_f": If, "T_eff": 2 * PI * J / If ** 4}


# ------------------------------------------------------------------ quadrature rules
def _gl(n, a, b):
    x, w = np.polynomial.legendre.leggauss(n)
    return 0.5 * (b - a) * x + 0.5 * (b + a), 0.5 * (b - a) * w


def _ortho(Khat):
    a = np.array([1.0, 0.0, 0.0]) if abs(Khat[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
    u1 = np.cross(Khat, a)
    u1 /= np.linalg.norm(u1)
    return u1, np.cross(Khat, u1)


def _ring_integral(omega, Kmag, Khat, phi, wphi, cg, pg, wg, pattern, final, m, G):
    """sum_final w_gamma beta |sum_phi wphi M|^2 for one K (lab), integrated over CM photon angles.

    phi, wphi: ring nodes and weights (radians); cg, pg, wg: flattened CM photon (cos theta, phi, weight)."""
    u1, u2 = _ortho(Khat)
    rho = math.sqrt(max(omega * omega - 0.25 * Kmag * Kmag, 0.0))
    kv = rho * (np.cos(phi)[:, None] * u1 + np.sin(phi)[:, None] * u2)          # (nphi, 3)
    Kv = Kmag * Khat
    k1s, k2s = 0.5 * Kv - kv, 0.5 * Kv + kv
    q1 = np.concatenate([np.full((len(phi), 1), omega), k1s], axis=1)
    q2v = np.concatenate([np.full((len(phi), 1), omega), k2s], axis=1)
    n1, n2 = k1s / omega, k2s / omega
    s = 4 * omega * omega - Kmag * Kmag
    Es = 0.5 * math.sqrt(s)
    ps = math.sqrt(max(Es * Es - m * m, 0.0))
    beta_f = ps / Es
    # CM photon directions in the (u1, u2, Khat) frame, boosted along Khat with beta = |K|/K0
    sg = np.sqrt(np.clip(1 - cg * cg, 0, None))
    nst = (sg * np.cos(pg))[:, None] * u1 + (sg * np.sin(pg))[:, None] * u2 + cg[:, None] * Khat
    gam, bg = 2 * omega / math.sqrt(s), Kmag / math.sqrt(s)                      # gamma, gamma*beta
    par = ps * cg
    perp = ps * nst - par[:, None] * Khat

    def boost(sign):
        E = gam * Es + bg * sign * par
        pz = bg * Es + gam * sign * par
        return np.concatenate([E[:, None], sign * perp + pz[:, None] * Khat], axis=1)

    p1, p2 = boost(1.0), boost(-1.0)
    nphi, ng = len(phi), len(cg)
    sh = (nphi, ng)
    Q1 = np.broadcast_to(q1[:, None, :], sh + (4,))
    Q2 = np.broadcast_to(q2v[:, None, :], sh + (4,))
    P1 = np.broadcast_to(p1[None, :, :], sh + (4,))
    P2 = np.broadcast_to(p2[None, :, :], sh + (4,))
    if pattern == "bo_real_sign":
        cR1, cL1 = pattern_coefficients(pattern, n1)
        cR2, cL2 = pattern_coefficients(pattern, n2)
        combos = [(l1, l2, (np.abs(cR1) if l1 == 2 else np.abs(cL1)) * (np.abs(cR2) if l2 == 2 else np.abs(cL2)))
                  for l1 in (2, -2) for l2 in (2, -2)]
        tens = {(l, j): np.broadcast_to(helicity_tensor(nn, l)[:, None], sh + (4, 4))
                for l in (2, -2) for j, nn in ((1, n1), (2, n2))}
    else:
        E1 = np.broadcast_to(pattern_tensor(pattern, n1)[:, None], sh + (4, 4))
        E2 = np.broadcast_to(pattern_tensor(pattern, n2)[:, None], sh + (4, 4))
    # same-helicity photon pairs vanish identically for massless photons at tree level, whatever the graviton
    # helicities (qft_second_order docstring, Part A; checked once in our self-test): only s1 = -s2 is summed.
    finals = [(1, -1), (-1, 1)] if final == "photon" else [None]
    tot = np.zeros(ng)
    for fs in finals:
        def amp(e1, e2):
            if final == "photon":
                return q2.amplitude_gg_to_photons(Q1, e1, Q2, e2, P1, _photon_pol(P1, fs[0]), P2,
                                                  _photon_pol(P2, fs[1]), G)
            return q2.amplitude_gg_to_scalars(Q1, e1, Q2, e2, P1, P2, m, G)
        if pattern == "bo_real_sign":
            Mtot = sum(wt[:, None] * np.abs(amp(tens[(l1, 1)], tens[(l2, 2)])) for l1, l2, wt in combos)
        else:
            Mtot = amp(E1, E2)
        Fr = np.einsum("p,pg->g", wphi, Mtot)
        tot += np.abs(Fr) ** 2
    return float(np.dot(wg, tot)) * beta_f


def _photon_pol(k, hel):
    et, ep = _basis(np.asarray(k)[..., 1:] / np.linalg.norm(np.asarray(k)[..., 1:], axis=-1, keepdims=True))
    v = (-hel * et - 1j * ep) / _SQ2
    return np.concatenate([np.zeros(v.shape[:-1] + (1,)), v], axis=-1)


def _photon_grid(n_cg, n_pg):
    c, wc = _gl(n_cg, -1.0, 1.0)
    p = (np.arange(n_pg) + 0.5) * 2 * PI / n_pg + 0.1234567   # offset: keeps photons off graviton axes (t, u = 0)
    C_, P_ = np.meshgrid(c, p, indexing="ij")
    W_ = np.outer(wc, np.full(n_pg, 2 * PI / n_pg))
    return C_.ravel(), P_.ravel(), W_.ravel()


def _sym(final, field):
    if field not in ("real", "complex"):
        raise ValueError("field must be 'real' or 'complex'")
    return 0.5 if (final == "photon" or field == "real") else 1.0


@functools.lru_cache(maxsize=None)
def angular_integral(pattern: str, final: str = "photon", m_over_w: float = 0.0, field: str = "real",
                     n_K: int = 8, n_cK: int = 8, n_phi: int = 24, n_cg: int = 8, n_pg: int = 14) -> float:
    """I_ang / (G^2 w^5) for w = 1, G = 1: the pattern- and final-state-dependent factor of P = J_f I_ang.

    Uses axial symmetry of every pattern about z (|F|^2 independent of K's azimuth) and, for 'bo_real_sign', full
    isotropy. Quantity: dimensionless. Valid when: pattern in PATTERNS; final 'photon' or 'scalar'; 0 <= m/w < 1."""
    if pattern not in PATTERNS:
        raise ValueError(f"pattern must be one of {PATTERNS}")
    if final not in ("photon", "scalar"):
        raise ValueError("final must be 'photon' or 'scalar'")
    if not (0 <= m_over_w < 1) or (final == "photon" and m_over_w != 0):
        raise ValueError("need 0 <= m/w < 1 (scalars) and m = 0 for photons")
    sym = _sym(final, field)
    Kmax = 2.0 * math.sqrt(1.0 - m_over_w ** 2)
    un, uw = _gl(n_K, 0.0, PI / 2)            # K = Kmax sin u: removes the sqrt(4w^2 - K^2) endpoint behaviour
    Kn, Kw = Kmax * np.sin(un), Kmax * np.cos(un) * uw
    if pattern == "bo_real_sign":
        cK, cKw = np.array([0.3]), np.array([2.0])
    else:
        tK, tw = _gl(n_cK, 0.0, PI)            # polar angle of K (smooth in theta, not in cos theta)
        cK, cKw = np.cos(tK), np.sin(tK) * tw
    phi = np.arange(n_phi) * 2 * PI / n_phi
    wphi = np.full(n_phi, 2 * PI / n_phi)
    cg, pg, wg = _photon_grid(n_cg, n_pg)
    tot = 0.0
    for c, wc in zip(cK, cKw):
        Khat = np.array([math.sqrt(max(1 - c * c, 0.0)), 0.0, c])   # theta in (0, pi): sin theta >= 0
        for Km, wK in zip(Kn, Kw):
            tot += wc * 2 * PI * wK * _ring_integral(1.0, Km, Khat, phi, wphi, cg, pg, wg, pattern, final,
                                                     m_over_w, 1.0)
    return sym * tot / ((2 * PI) ** 4 * (32 * PI ** 2) ** 3)


_J_OVER = {"tophat": 32 * PI ** 4 / 3, "gaussian": 16 * math.sqrt(2 * PI) * PI ** 4}   # J_f / (N^2 sigma / w^2)
_TAU = {"tophat": 4 * PI / 3, "gaussian": math.sqrt(PI / 2)}                           # sigma * T_eff


def coefficients(pattern: str, profile: str = "tophat", final: str = "photon", m_over_w: float = 0.0,
                 field: str = "real", **grid) -> dict:
    """Pure numbers of the narrow-band model: P = c_tot G^2 N^2 w^3 sigma; B&O-style rate P/T_eff = c_rate G^2 N^2
    w^3 sigma^2 (c_rate = c_tot / (sigma T_eff)); 'ratio_to_BO' = c_rate / (3/(25 pi)).
    Quantity: dict of dimensionless coefficients. Valid when: as angular_integral; profile 'tophat' or 'gaussian'."""
    if profile not in PROFILES:
        raise ValueError(f"profile must be one of {PROFILES}")
    ia = angular_integral(pattern, final, m_over_w, field, **grid)
    c_tot = _J_OVER[profile] * ia
    c_rate = c_tot / _TAU[profile]
    return {"c_tot": c_tot, "c_rate": c_rate, "sigma_T_eff": _TAU[profile], "ratio_to_BO": c_rate / (3 / (25 * PI)),
            "I_ang": ia}


def yield_natural(N: float, omega: float, sigma: float, G: float, pattern: str = "bo_real_sign",
                  profile: str = "tophat", final: str = "photon", m: float = 0.0, field: str = "real", **grid) -> dict:
    """Pair yield of one coherent packet (natural units; omega, sigma, m in one energy unit, G in its inverse square).

    Quantity: dict 'pairs' (in-out leading-order mean number of pairs of the whole packet, dimensionless),
        'particles' (= 2 x pairs), 'T_eff' (B&O's 2 pi delta(0) -> T time, 1/energy), 'rate_BO_equiv' (pairs/T_eff,
        energy), 'c_tot', 'c_rate', 'ratio_to_BO'.
    Valid when: N >= 1, omega > 0, 0 < sigma <= 0.1 omega, G > 0, 0 <= m < omega; result P <= 0.1 (perturbative)."""
    if not (N >= 1 and omega > 0 and G > 0):
        raise ValueError("need N >= 1, omega > 0, G > 0")
    pf = profile_factors(profile, N, omega, sigma)
    co = coefficients(pattern, profile, final, m / omega, field, **grid)
    P = co["c_tot"] * G * G * N * N * omega ** 3 * sigma
    if P > 0.1:
        raise ValueError(f"P = {P:.3g} > 0.1: outside leading-order perturbation theory (depletion/back-reaction)")
    return {"pairs": P, "particles": 2 * P, "T_eff": pf["T_eff"], "rate_BO_equiv": P / pf["T_eff"], **co}


def yield_SI(E_J: float, f_Hz: float, sigma_rad_s: float, pattern: str = "bo_real_sign", profile: str = "tophat",
             final: str = "photon", m_eV: float = 0.0, field: str = "real", **grid) -> dict:
    """yield_natural in SI: packet energy E_J (J), carrier frequency f_Hz (Hz, w = 2 pi f), spectral width
    sigma_rad_s (rad/s, B&O's sigma_w), scalar mass m_eV (eV). N = E/(hbar w).
    Quantity: dict 'pairs' (dimensionless), 'T_eff_s' (s), 'rate_BO_equiv_per_s' (pairs/s), 'N', and the coefficients.
    Valid when: as yield_natural."""
    if not (E_J > 0 and f_Hz > 0 and sigma_rad_s > 0):
        raise ValueError("need E > 0, f > 0, sigma > 0")
    w_rad = 2 * PI * f_Hz
    N = E_J / (HBAR * w_rad)
    w, sg = HBAR * w_rad / E_CHARGE, HBAR * sigma_rad_s / E_CHARGE
    r = yield_natural(N, w, sg, q2.newton_G_natural(1.0), pattern, profile, final, m_eV, field, **grid)
    t_unit = HBAR / E_CHARGE                                     # seconds per eV^-1
    return {"pairs": r["pairs"], "particles": r["particles"], "N": N, "T_eff_s": r["T_eff"] * t_unit,
            "rate_BO_equiv_per_s": r["rate_BO_equiv"] / t_unit, "c_tot": r["c_tot"], "c_rate": r["c_rate"],
            "ratio_to_BO": r["ratio_to_BO"]}


# ------------------------------------------------------------------ two-beam limit (self-test reference route)
def _two_cap_yield(delta, sigma, n_lin=7, n_ring=7, n_cg=6, n_pg=6, width=1.5):
    """P for a coherent state made of two narrow Gaussian caps (helicity +2 around x^, helicity -2 around y^, angular
    width delta, Gaussian radial profile of width sigma, Theta = 1, w = 1, G = 1), by the same ring machinery with
    nodes concentrated where |F|^2 is non-negligible. Returns (P, A) with A the plane-wave amplitude of each beam."""
    na, nb = np.array([1.0, 0, 0]), np.array([0, 1.0, 0])

    def caps(n):
        ga = np.exp(-(np.arccos(np.clip(n @ na, -1, 1))) ** 2 / (2 * delta ** 2))
        gb = np.exp(-(np.arccos(np.clip(n @ nb, -1, 1))) ** 2 / (2 * delta ** 2))
        return ga + 0j, gb + 0j

    Kc = na + nb
    Kc_mag = np.linalg.norm(Kc)
    Kchat = Kc / Kc_mag
    e1 = np.array([0, 0, 1.0])
    e2 = np.cross(Kchat, e1)
    # |F|^2 is Gaussian in K with standard deviations delta/sqrt2 (|K|), delta/sqrt2 (tilt a along z) and delta/2
    # (tilt b in the x-y plane); the ring integrand has standard deviation delta in phi. Uniform (trapezoid) nodes
    # every `width` standard deviations: for a Gaussian the trapezoid error is ~ exp(-2 pi^2/width^2) (1.5e-4 at 1.5).
    j = np.arange(n_lin) - (n_lin - 1) / 2

    def trap(sd):
        return j * width * sd, np.full(n_lin, width * sd)

    Kn, Kw = trap(delta / _SQ2)
    Kn = Kn + Kc_mag
    an, aw = trap(delta / _SQ2)
    bn, bw = trap(delta / 2)
    jr = np.arange(n_ring) - (n_ring - 1) / 2
    rn, rw = jr * width * delta, np.full(n_ring, width * delta)
    cg, pg, wg = _photon_grid(n_cg, n_pg)
    tot = 0.0
    for a, wa in zip(an, aw):
        if True:
            for b, wb in zip(bn, bw):
                v = Kchat + a * e1 + b * e2
                jac = (1 + a * a + b * b) ** -1.5
                Khat = v / np.linalg.norm(v)
                u1, u2 = _ortho(Khat)
                for Km, wK in zip(Kn, Kw):
                    # ring angle where k1 = K/2 - rho(...) points closest to na; the second cap pair sits at +pi
                    d = 0.5 * Km * Khat - na
                    ph0 = math.atan2(d @ u2, d @ u1)
                    phi = np.concatenate([ph0 + rn, ph0 + PI + rn])
                    wphi = np.concatenate([rw, rw])
                    tot += wa * wb * jac * wK * _ring_integral(1.0, Km, Khat, phi, wphi, cg, pg, wg, caps,
                                                               "photon", 0.0, 1.0)
    I_ang = 0.5 * tot / ((2 * PI) ** 4 * (32 * PI ** 2) ** 3)
    J = sigma ** 3 * PI * math.sqrt(2 * PI)                        # Theta = 1 Gaussian
    A = sigma * math.sqrt(2 * PI) * 2 * PI * delta ** 2 / ((2 * PI) ** 3 * 2.0)   # int dk~ alpha, per beam
    return J * I_ang, A


def _overlap_4volume(delta, sigma):
    """int d^4x |E_a|^2 |E_b|^2 for Gaussian beams along x and y (closed-form Gaussian integral, position space):
    |E_a|^2 = exp(-sigma^2 (t-x)^2 - delta^2 (y^2 + z^2)), |E_b|^2 = exp(-sigma^2 (t-y)^2 - delta^2 (x^2 + z^2))."""
    s2, d2 = sigma ** 2, delta ** 2
    Mq = np.array([[2 * s2, -s2, -s2], [-s2, s2 + d2, 0.0], [-s2, 0.0, s2 + d2]])
    return math.sqrt(PI / (2 * d2)) * PI ** 1.5 / math.sqrt(np.linalg.det(Mq))


# ------------------------------------------------------------------ self-test
def selftest(verbose: bool = True) -> bool:
    ok = True

    def check(name, got, want, rel):
        nonlocal ok
        good = abs(got - want) <= rel * abs(want) if want != 0 else abs(got) <= rel
        ok &= bool(good)
        if verbose:
            print(f"[{'PASS' if good else 'FAIL'}] {name}: got {got:.10g}, want {want:.10g} (tol {rel:g})")

    # 0. Internal consistency (not a reference): our helicity tensors equal the toolkit's.
    n = np.array([0.3, -0.5, 0.81])
    n /= np.linalg.norm(n)
    d = max(np.max(np.abs(helicity_tensor(n, lam) - q2.graviton_polarization(np.concatenate([[1.0], n]), lam)))
            for lam in (2, -2))
    check("helicity tensors == qft_second_order.graviton_polarization", d, 0.0, 1e-14)

    # 0b. Justifies skipping s1 = s2 photon pairs: for a generic (binary-pattern) pair of tensors at 70 degrees the
    #     same-helicity photon amplitude is roundoff relative to the opposite-helicity one.
    nA, nB = np.array([0.2, 0.1, 0.97]), np.array([0.9, -0.3, 0.2])
    nA, nB = nA / np.linalg.norm(nA), nB / np.linalg.norm(nB)
    qa, qb = np.concatenate([[1.0], nA]), np.concatenate([[1.0], nB])
    EA, EB = pattern_tensor("circular_binary", nA), pattern_tensor("circular_binary", nB)
    K = qa + qb
    sK = K[0] ** 2 - K[1:] @ K[1:]
    gm, bgv = K[0] / math.sqrt(sK), K[1:] / math.sqrt(sK)
    nst = np.array([0.6, 0.0, 0.8])                              # CM photon direction, boosted to the lab
    Es = 0.5 * math.sqrt(sK)

    def lab(v):
        par = bgv @ v / np.linalg.norm(bgv) if np.linalg.norm(bgv) > 0 else 0.0
        bh = bgv / np.linalg.norm(bgv)
        return np.concatenate([[gm * Es + np.linalg.norm(bgv) * par], v + ((gm - 1) * par + np.linalg.norm(bgv) * Es) * bh])

    p1, p2 = lab(Es * nst), lab(-Es * nst)
    amps = {(a1, a2): abs(complex(q2.amplitude_gg_to_photons(qa, EA, qb, EB, p1, _photon_pol(p1, a1), p2,
                                                            _photon_pol(p2, a2), 1.0)))
            for a1 in (1, -1) for a2 in (1, -1)}
    same = max(amps[(1, 1)], amps[(-1, -1)]) / max(amps[(1, -1)], amps[(-1, 1)])
    check("same-helicity photon amplitude / opposite (binary pattern, generic kinematics)", same, 0.0, 1e-12)

    # 1. Exact definition: B&O p. 2 normalisation of the top hat per helicity.
    #    B&O arXiv:2607.24930 p. 2: "f s(k) = Θ fork∈[ω s− σω 2 , ωs + σω 2 ] and zero otherwise, with
    #    Θ = p 2π2N/ωsσω fixed by the average graviton number N." Ours: f = sqrt2 Theta_BO with c_R = c_L = 1/sqrt2.
    N, w, sg = 1e6, 1.0, 0.01
    th = profile_factors("tophat", N, w, sg)["Theta"]
    check("top-hat Theta/sqrt2 = B&O sqrt(2 pi^2 N/(w sigma))", th / _SQ2, math.sqrt(2 * PI ** 2 * N / (w * sg)), 1e-14)

    # 2. Exact definition of B&O's T (S6: "the remaining energy-conserving delta function is treated as
    #    2πδ(0)→T"): T_eff = 2 pi int dE C(E)^2 / (int f)^4; brute-force convolution of the top hat vs (4 pi/3)/sigma.
    x = np.linspace(-1.5, 1.5, 300001)
    tri = np.clip(1 - np.abs(x), 0, None)                         # C(E)/(Theta^2 sigma), E in units of sigma
    J_num = np.trapezoid(tri ** 2, x) if hasattr(np, "trapezoid") else np.trapz(tri ** 2, x)
    check("top-hat sigma*T_eff by direct convolution = 4 pi/3", 2 * PI * J_num, 4 * PI / 3, 1e-9)

    # 3. Pattern normalisation: standard quadrupole angular integrals (closed forms):
    #    int dOmega [((1+cos^2)/2)^2 + cos^2] = 16 pi/5 (binary), int dOmega sin^4 = 32 pi/15 (linear).
    cK, wK = _gl(40, -1, 1)
    for p in ("circular_binary", "linear_quadrupole", "pure_circular"):
        nn = np.stack([np.sqrt(1 - cK ** 2), np.zeros_like(cK), cK], axis=-1)
        cR, cL = pattern_coefficients(p, nn)
        check(f"pattern {p}: <|c_R|^2+|c_L|^2> = 1", 0.5 * float(np.dot(wK, np.abs(cR) ** 2 + np.abs(cL) ** 2)),
              1.0, 1e-13)

    # 4. Reference: B&O eq. 8 (arXiv:2607.24930 v2 p. 3), "dP/dt = 3G2N2ω3 sσ2 ω 25π .(8)" (PDF extraction of
    #    3 G^2 N^2 w_s^3 sigma_w^2/(25 pi)), for their real-sign unpolarised amplitudes and top hat.
    #    Independently re-derived by hand (in CM: t^2+u^2 = (s^2/2)(1+cos^2), int dOmega (1+c^2)(1+c'^2) averaged
    #    over the relative ring angle = 36 pi/5, int_0^{2w} (4w^2-K^2)^2 dK = 256 w^5/15).
    co = coefficients("bo_real_sign", "tophat", "photon")
    check("B&O real-sign top hat photons: c_rate = 3/(25 pi) [B&O eq. 8]", co["c_rate"], 3 / (25 * PI), 1e-6)

    # 5. Reference: B&O p. 5, scalar channel: "forω s≫m DM ... dP/dt= 7G 2N2 0ω3 sσ2 ω/450π. The result- ing
    #    reaction time isτ ϕ = (54/7)τ". Massless real scalar, same model.
    cs = coefficients("bo_real_sign", "tophat", "scalar")
    check("B&O real-sign top hat massless scalars: c_rate = 7/(450 pi) [B&O p. 5]", cs["c_rate"], 7 / (450 * PI), 1e-6)

    # 6. Selection rule (limit): same-helicity gravitons make no massless pairs at tree level, so a pure-circular
    #    packet yields exactly zero (qft_second_order docstring and self-test; B&O eq. 6 lists no other entries).
    cp = coefficients("pure_circular", "tophat", "photon", n_K=4, n_cK=4, n_phi=16, n_cg=6, n_pg=12)
    check("pure circular packet: c_tot = 0 (relative to B&O's 0.16)", cp["c_tot"] / co["c_tot"], 0.0, 1e-20)

    # 7. Limit: two narrow crossing beams -> the toolkit's two-beam rate times the overlap 4-volume.
    #    P = Gamma(R, L, 90 deg) int d^4x |E_a|^2 |E_b|^2, Gamma from qft_second_order.beams_pair_rate (itself checked
    #    against Holstein 2006 eq. 66 and Bjerrum-Bohr et al.), overlap from the closed-form Gaussian integral.
    #    Expected corrections: diffraction ~ delta, cap curvature/tilt ~ (sigma/delta)^2, amplitude variation ~ delta^2.
    #    Measured deficit 1.8% at delta = 0.04 and 1.0% at delta = 0.03: it scales as delta^2 (cap width), so each
    #    raw ratio is checked at 3% (the finite-width correction, not a loosened tolerance) and the Richardson
    #    extrapolation delta -> 0 (r0 = (r2 d1^2 - r1 d2^2)/(d1^2 - d2^2)) at 0.5%.
    h = 1e-3
    br = q2.beams_pair_rate(1.0, h, 1.0, h, PI / 2, "R", "L", G=1.0)
    Gamma_unit = br["pair_rate"] / (h / math.sqrt(32 * PI)) ** 4
    ratios = []
    for delta, sigma in ((0.04, 0.002), (0.03, 0.0015)):
        P_caps, A = _two_cap_yield(delta, sigma)
        P_ref = Gamma_unit * A ** 4 * _overlap_4volume(delta, sigma)
        ratios.append(P_caps / P_ref)
        check(f"two crossing caps (R x L, 90 deg, delta = {delta}) / [beams_pair_rate x overlap 4-volume]",
              ratios[-1], 1.0, 0.03)
    r0 = (ratios[1] * 0.04 ** 2 - ratios[0] * 0.03 ** 2) / (0.04 ** 2 - 0.03 ** 2)
    check("two-beam limit, Richardson-extrapolated to delta -> 0", r0, 1.0, 0.005)

    if verbose:
        print("selftest", "PASSED" if ok else "FAILED")
    return ok


def _table():
    print(f"{'pattern':18s} {'profile':9s} {'final':7s} {'c_tot':>12s} {'c_rate':>12s} {'rate/B&O':>10s}")
    for p in PATTERNS:
        for pr in PROFILES:
            for fin in ("photon", "scalar"):
                c = coefficients(p, pr, fin)
                print(f"{p:18s} {pr:9s} {fin:7s} {c['c_tot']:12.6g} {c['c_rate']:12.6g} {c['ratio_to_BO']:10.4g}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Graviton fusion yield inside one coherent GW packet")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("selftest")
    sub.add_parser("table")
    cv = sub.add_parser("convergence")
    cv.add_argument("--pattern", default="circular_binary")
    bc = sub.add_parser("beamcheck", help="two crossing caps vs qft_second_order two-beam rate x overlap")
    bc.add_argument("--delta", type=float, default=0.04)
    bc.add_argument("--sig", type=float, default=0.002)
    for nm, dv in (("--n_lin", 7), ("--n_ring", 7), ("--n_cg", 6), ("--n_pg", 6)):
        bc.add_argument(nm, type=int, default=dv)
    y = sub.add_parser("yield")
    y.add_argument("--E", required=True, help="packet energy, e.g. '2 Msun*c^2' or '3.57e47 J'")
    y.add_argument("--f", required=True, help="carrier frequency (cycles), e.g. '150 Hz'")
    y.add_argument("--sigma", required=True, help="spectral width sigma_w as an angular frequency, e.g. '200 Hz' = 200 rad/s")
    y.add_argument("--pattern", default="bo_real_sign", choices=PATTERNS)
    y.add_argument("--profile", default="tophat", choices=PROFILES)
    y.add_argument("--final", default="photon", choices=("photon", "scalar"))
    y.add_argument("--m", default="0", help="scalar mass, e.g. '1e-13 eV'")
    a = ap.parse_args(argv)
    if a.cmd == "selftest":
        return 0 if selftest() else 1
    if a.cmd == "table":
        return _table()
    if a.cmd == "beamcheck":
        import time
        t0 = time.time()
        P, A = _two_cap_yield(a.delta, a.sig, n_lin=a.n_lin, n_ring=a.n_ring, n_cg=a.n_cg, n_pg=a.n_pg)
        br = q2.beams_pair_rate(1.0, 1e-3, 1.0, 1e-3, PI / 2, "R", "L", G=1.0)
        ref = br["pair_rate"] / (1e-3 / math.sqrt(32 * PI)) ** 4 * A ** 4 * _overlap_4volume(a.delta, a.sig)
        print(f"caps P = {P:.8g}, beams x overlap = {ref:.8g}, ratio = {P / ref:.6f}  ({time.time() - t0:.1f} s)")
        return 0
    if a.cmd == "convergence":
        for g in ({"n_K": 8, "n_cK": 8, "n_phi": 48, "n_cg": 8, "n_pg": 14}, {},
                  {"n_K": 8, "n_cK": 8, "n_phi": 24, "n_cg": 12, "n_pg": 24}):
            print(g or "default", coefficients(a.pattern, "tophat", "photon", **g)["c_tot"])
        return 0
    E = Q(a.E).expect("energy").si
    f = Q(a.f).si
    sg = Q(a.sigma).si
    m = 0.0 if a.m.strip() == "0" else Q(a.m).expect("energy").si / E_CHARGE
    r = yield_SI(E, f, sg, a.pattern, a.profile, a.final, m)
    print(f"N = {r['N']:.4g} gravitons, pattern {a.pattern}, profile {a.profile}, final {a.final}")
    print(f"pairs per packet (in-out, leading order) P = {r['pairs']:.4g}   [c_tot = {r['c_tot']:.6g}]")
    print(f"B&O-style T_eff = {r['T_eff_s']:.4g} s;  P/T_eff = {r['rate_BO_equiv_per_s']:.4g} pairs/s  "
          f"[c_rate = {r['c_rate']:.6g}; ratio to B&O 3/(25 pi) model = {r['ratio_to_BO']:.4g}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
