"""Shared, INDEPENDENT machinery for the Blas & Oller (arXiv:2607.24930) Task A checks.

Nothing here imports qft_second_order: it is a second route to the same amplitudes, used to cross-check that module.

Route: spinor-helicity closed forms for the tree amplitudes, with explicit polarisation vectors built from the SAME
spinors, so the full multilinear amplitude for ARBITRARY transverse-traceless graviton tensors (any phases) can be
evaluated by projecting each tensor on the spinor basis.

Conventions (natural units, metric +,-,-,-):
  p_{a adot} = p^0 1 + p.sigma = lam_a lamt_adot, lamt = conj(lam) for positive energy.
  <ij> = lam_i^1 lam_j^2 - lam_i^2 lam_j^1 ,  [ij] = same with lamt.
  eps^+_{a adot}(k;r) = sqrt2 r_a lamt_k / <r k> ,  eps^-_{a adot}(k;r) = sqrt2 lam_k rt / [k r]   (the vectors that
  enter the amplitude, i.e. already conjugated for an outgoing particle).  Dot product v.w = (1/2) eps eps v w.
  Incoming particle of momentum P with wavefunction E (tensor or vector) = outgoing particle of momentum -P whose
  amplitude slot receives E; lam(-P) = i lam(P), lamt(-P) = i lamt(P); for the formulas below the factors of i cancel
  (graviton slots carry net little-group weight 4), so the physical-momentum spinors are used directly.

Amplitudes (all-outgoing labels, kappa^2 = 32 pi G, (kappa/2)^2 = 8 pi G):
  photons:  M(1_gam^-, 2_gam^+, 3_h^{--}, 4_h^{++}) = (kappa/2)^2 s12 <13>^5 <23> / (<12>^2 <34>^2 <41> <24>)
            (KLT: s12 A_YM(1^-,2^+,3^-,4^+) A_YM+phi(1_phi,2_phi,4^+,3^-), derived in notes; |M| = 8 pi G s13^2/s12)
  massless minimally coupled scalars:
            M(1_phi, 2_phi, 3_h^{--}, 4_h^{++}) = (kappa/2)^2 <3|1|4]^4 / (s12 s13 s14),  |M| = 8 pi G |s13 s14|/s12
  All other helicity assignments vanish (MHV counting; same-helicity gravitons with massless pairs vanish).
  The overall constant phase is convention dependent and irrelevant: only |sum|^2 enters any rate, and every
  nonzero configuration used here is a relabelling of ONE formula, so relative phases are fixed.
"""
from __future__ import annotations

import math

import numpy as np

PI = math.pi
SQ2 = math.sqrt(2.0)
ETA = np.diag([1.0, -1.0, -1.0, -1.0])
SIG = [np.eye(2, dtype=complex),
       np.array([[0, 1], [1, 0]], dtype=complex),
       np.array([[0, -1j], [1j, 0]], dtype=complex),
       np.array([[1, 0], [0, -1]], dtype=complex)]
R_REF = np.array([1.0, 0.31, -0.52, math.sqrt(1.0 - 0.31 ** 2 - 0.52 ** 2)])   # generic null reference vector


# ---------------------------------------------------------------- spinors
def lam(p):
    """Holomorphic spinor of a positive-energy null 4-vector p (...,4); branch chosen for numerical stability."""
    p = np.asarray(p, dtype=float)
    E, px, py, pz = p[..., 0], p[..., 1], p[..., 2], p[..., 3]
    a = E + pz
    b = E - pz
    use1 = a >= b
    sa = np.sqrt(np.where(use1, a, 1.0))
    sb = np.sqrt(np.where(use1, 1.0, b))
    l1 = np.where(use1, sa, (px - 1j * py) / sb)
    l2 = np.where(use1, (px + 1j * py) / sa, sb)
    return np.stack([l1 + 0j, l2 + 0j], axis=-1)


def ang(li, lj):
    return li[..., 0] * lj[..., 1] - li[..., 1] * lj[..., 0]


def sqb(li, lj):
    lti, ltj = np.conj(li), np.conj(lj)
    return lti[..., 0] * ltj[..., 1] - lti[..., 1] * ltj[..., 0]


def mdot(a, b):
    return a[..., 0] * b[..., 0] - a[..., 1] * b[..., 1] - a[..., 2] * b[..., 2] - a[..., 3] * b[..., 3]


def bispinor_to_vector(v):
    """v_{a adot} (...,2,2) -> contravariant 4-vector with v = v^0 1 + v.sigma."""
    v0 = 0.5 * (v[..., 0, 0] + v[..., 1, 1])
    v3 = 0.5 * (v[..., 0, 0] - v[..., 1, 1])
    v1 = 0.5 * (v[..., 0, 1] + v[..., 1, 0])
    v2 = (v[..., 1, 0] - v[..., 0, 1]) / (2j)
    return np.stack([v0, v1, v2, v3], axis=-1)


def pol_vectors(p, lp=None):
    """(eps_plus, eps_minus) contravariant 4-vectors for null p, built from lam(p) (or the given lp) and R_REF."""
    if lp is None:
        lp = lam(p)
    lr = lam(np.broadcast_to(R_REF, np.shape(p)))
    lpt, lrt = np.conj(lp), np.conj(lr)
    ep = SQ2 * lr[..., :, None] * lpt[..., None, :] / ang(lr, lp)[..., None, None]
    em = SQ2 * lp[..., :, None] * lrt[..., None, :] / sqb(lp, lr)[..., None, None]
    return bispinor_to_vector(ep), bispinor_to_vector(em)


def lower(v):
    return v * np.array([1.0, -1.0, -1.0, -1.0])


def graviton_coeffs(P, H_low, lp=None):
    """Coefficients (c_mm, c_pp) of a lower-index TT tensor H in the basis (eps^- eps^-, eps^+ eps^+) (upper index
    basis tensors; slot labels of the all-outgoing formula for an INCOMING graviton of momentum P)."""
    ep, em = pol_vectors(P, lp)
    out = []
    for e in (em, ep):
        E = e[..., :, None] * e[..., None, :]                       # upper indices
        num = np.einsum("...mn,...mn->...", np.conj(E), H_low)       # conj(E)^{mn} H_{mn}
        El = lower(lower(E).swapaxes(-1, -2)).swapaxes(-1, -2)       # lower both indices
        den = np.einsum("...mn,...mn->...", np.conj(E), El)
        out.append(num / den)
    return out[0], out[1]


def photon_coeffs(q, e_used_up, lq=None):
    """Coefficients (a_minus, a_plus) of a contravariant photon wavefunction (the vector that ENTERS the amplitude,
    i.e. conj of the physical polarisation for an outgoing photon) in the basis (eps^-, eps^+)."""
    ep, em = pol_vectors(q, lq)
    out = []
    for e in (em, ep):
        num = mdot(np.conj(e), e_used_up)
        den = mdot(np.conj(e), e)
        out.append(num / den)
    return out[0], out[1]


# ---------------------------------------------------------------- closed-form amplitudes (G = 1 unless given)
def F_photon(l1, l2, l3, l4, s12, G=1.0):
    """M(1_gam^-, 2_gam^+, 3_h^{--}, 4_h^{++}) for spinors l1..l4 (physical-momentum spinors; see module notes)."""
    return 8 * PI * G * s12 * ang(l1, l3) ** 5 * ang(l2, l3) / (
        ang(l1, l2) ** 2 * ang(l3, l4) ** 2 * ang(l4, l1) * ang(l2, l4))


def F_scalar(l1, l2, l3, l4, s12, s13, s14, G=1.0):
    """M(1_phi, 2_phi, 3_h^{--}, 4_h^{++}) for a massless minimally coupled scalar; <3|1|4] = <31>[14]."""
    return 8 * PI * G * (ang(l3, l1) * sqb(l1, l4)) ** 4 / (s12 * s13 * s14)


def photon_amp_general(P1, H1, P2, H2, q1, e1_phys, q2, e2_phys, G=1.0):
    """Full tree amplitude g(P1,H1) g(P2,H2) -> gam(q1, e1) gam(q2, e2) for arbitrary TT tensors (lower index) and
    physical photon polarisation vectors (contravariant), from the spinor closed form."""
    L1, L2, Lq1, Lq2 = lam(P1), lam(P2), lam(q1), lam(q2)
    cm1, cp1 = graviton_coeffs(P1, H1, L1)
    cm2, cp2 = graviton_coeffs(P2, H2, L2)
    am1, ap1 = photon_coeffs(q1, np.conj(e1_phys), Lq1)
    am2, ap2 = photon_coeffs(q2, np.conj(e2_phys), Lq2)
    K = np.asarray(q1) + np.asarray(q2)
    s = mdot(K, K)
    tot = 0.0
    # photon labels (q1 -, q2 +) and (q1 +, q2 -); graviton labels (P1 --, P2 ++) and (P1 ++, P2 --)
    for (aa, la, lb) in ((am1 * ap2, Lq1, Lq2), (ap1 * am2, Lq2, Lq1)):
        tot = tot + aa * (cm1 * cp2 * F_photon(la, lb, L1, L2, s, G) + cp1 * cm2 * F_photon(la, lb, L2, L1, s, G))
    return tot


def scalar_amp_general(P1, H1, P2, H2, q1, q2, G=1.0):
    """Full tree amplitude g(P1,H1) g(P2,H2) -> phi(q1) phi(q2), massless minimally coupled scalar."""
    L1, L2, Lq1, Lq2 = lam(P1), lam(P2), lam(q1), lam(q2)
    cm1, cp1 = graviton_coeffs(P1, H1, L1)
    cm2, cp2 = graviton_coeffs(P2, H2, L2)
    P1, P2, q1, q2 = (np.asarray(x, dtype=float) for x in (P1, P2, q1, q2))
    s = mdot(q1 + q2, q1 + q2)
    s13, s14 = mdot(q1 - P1, q1 - P1), mdot(q1 - P2, q1 - P2)
    return (cm1 * cp2 * F_scalar(Lq1, Lq2, L1, L2, s, s13, s14, G)
            + cp1 * cm2 * F_scalar(Lq1, Lq2, L2, L1, s, s14, s13, G))


# ---------------------------------------------------------------- physical polarisation patterns on the sphere
def frame(n):
    """Spherical unit vectors (e_theta, e_phi) of unit vectors n (...,3) w.r.t. the z axis."""
    n = np.asarray(n, dtype=float)
    th = np.arccos(np.clip(n[..., 2], -1, 1))
    ph = np.arctan2(n[..., 1], n[..., 0])
    et = np.stack([np.cos(th) * np.cos(ph), np.cos(th) * np.sin(ph), -np.sin(th)], axis=-1)
    ep = np.stack([-np.sin(ph), np.cos(ph), np.zeros_like(ph)], axis=-1)
    return et, ep


def tt_project(n, Q):
    """Lambda(n) Q: transverse-traceless projection of a 3x3 (complex) tensor Q onto direction(s) n."""
    n = np.asarray(n, dtype=float)
    P = np.eye(3) - n[..., :, None] * n[..., None, :]
    PQP = np.einsum("...ik,kl,...lj->...ij", P, Q, P)
    tr = np.einsum("...ij,...ij->...", P, np.broadcast_to(Q, P.shape))
    return PQP - 0.5 * P * tr[..., None, None]


def _pattern_raw(name, n):
    n = np.asarray(n, dtype=float)
    et, ep = frame(n)
    if name == "bo_plus":
        return (et[..., :, None] * et[..., None, :] - ep[..., :, None] * ep[..., None, :]).astype(complex)
    if name == "bo_cross":
        return (et[..., :, None] * ep[..., None, :] + ep[..., :, None] * et[..., None, :]).astype(complex)
    if name == "circ":
        e = (-et - 1j * ep) / SQ2
        return e[..., :, None] * e[..., None, :]
    if name == "binary":
        v = np.array([1.0, 1j, 0.0])
        return tt_project(n, np.outer(v, v))
    if name == "linear":
        z = np.array([0.0, 0.0, 1.0])
        return tt_project(n, np.outer(z, z).astype(complex))
    raise ValueError(name)


_NORM = {}


def pattern_norm(name):
    """int dOmega |h_raw|^2 by Gauss-Legendre(40) x uniform(80) quadrature (exact for these polynomial patterns)."""
    if name not in _NORM:
        x, w = np.polynomial.legendre.leggauss(40)
        ph = (np.arange(80) + 0.5) * 2 * PI / 80
        X, PH = np.meshgrid(x, ph, indexing="ij")
        st = np.sqrt(1 - X ** 2)
        n = np.stack([st * np.cos(PH), st * np.sin(PH), X], axis=-1)
        h = _pattern_raw(name, n)
        val = np.einsum("i,ij->", w, np.sum(np.abs(h) ** 2, axis=(-1, -2))) * 2 * PI / 80
        _NORM[name] = float(val)
    return _NORM[name]


def pattern(name, n):
    """Spatial TT tensor field h(n) (...,3,3), normalised so that int dOmega |h|^2 = 1 (|h|^2 = sum_ij |h_ij|^2).

    'bo_plus'  : e_th e_th - e_ph e_ph (polar frame about z), isotropic magnitude: what f_+ = f_- = real gives in
                 the e_+- = (-+ e_th - i e_ph)/sqrt2 convention (qft_second_order's); B&O's literal 'unpolarised' shell.
    'bo_cross' : e_th e_ph + e_ph e_th (f_+ = -f_- real in that convention), isotropic magnitude.
    'circ'     : pure helicity +2 everywhere, e_+ e_+ (isotropic magnitude).
    'binary'   : rotating-quadrupole pattern Lambda(n) (x + i y)(x + i y) (circular binary, orbital axis z).
    'linear'   : oscillating linear quadrupole Lambda(n) z z = (sin^2 th/2)(e_th e_th - e_ph e_ph).
    """
    return _pattern_raw(name, n) / math.sqrt(pattern_norm(name))


def to4(h3):
    """Spatial TT tensor (...,3,3) -> lower-index 4x4 (h_{ij} lower = h_ij for spatial indices)."""
    out = np.zeros(h3.shape[:-2] + (4, 4), dtype=complex)
    out[..., 1:, 1:] = h3
    return out


def bo_profile(name, n):
    """B&O-model real helicity profile g(n) with f_+ = f_- = g (only for patterns where that is the content)."""
    n = np.asarray(n, dtype=float)
    if name == "bo_plus":
        return np.full(n.shape[:-1], 1.0 / math.sqrt(8 * PI))
    if name == "linear":
        # Lambda z z = (sin^2/2)(e_th e_th - e_ph e_ph) = (sin^2/2)(eps_+ + eps_-): f_+ = f_- = (sin^2 th/2)/norm
        return (1 - n[..., 2] ** 2) / 2 / math.sqrt(pattern_norm("linear"))
    raise ValueError(name)


# ---------------------------------------------------------------- ring kinematics (narrow band, omega = 1)
def basis_perp(Khat):
    Khat = np.asarray(Khat, dtype=float)
    a = np.array([1.0, 0, 0]) if abs(Khat[0]) < 0.9 else np.array([0, 1.0, 0])
    e1 = a - Khat * (a @ Khat)
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(Khat, e1)
    return e1, e2


def ring_and_photons(Kmag, Khat, alphas, cth, phis, m=0.0):
    """Lab kinematics for one K: gravitons k1 = K/2 - rho u(alpha), k2 = K/2 + rho u(alpha) (energies 1, the
    narrow-band ring) and final particles with CM direction (cth, phi) about Khat, boosted to the lab.
    Returns k1, k2 (Na,4), q1, q2 (Nn,4), s, beta_cm (final-state velocity in the CM)."""
    e1, e2 = basis_perp(Khat)
    rho = math.sqrt(max(1.0 - Kmag ** 2 / 4.0, 0.0))
    u = np.cos(alphas)[:, None] * e1 + np.sin(alphas)[:, None] * e2
    Kv = Kmag * np.asarray(Khat)
    k1 = np.concatenate([np.ones((len(alphas), 1)), Kv / 2 - rho * u], axis=1)
    k2 = np.concatenate([np.ones((len(alphas), 1)), Kv / 2 + rho * u], axis=1)
    s = 4.0 - Kmag ** 2
    E = math.sqrt(s) / 2
    p = math.sqrt(max(E * E - m * m, 0.0))
    sth = np.sqrt(np.clip(1 - cth ** 2, 0, None))
    dirs = (sth * np.cos(phis))[:, None] * e1 + (sth * np.sin(phis))[:, None] * e2 + cth[:, None] * np.asarray(Khat)
    bet = Kmag / 2.0
    gam = 2.0 / math.sqrt(s)
    Khat = np.asarray(Khat)
    out = []
    for sign in (1, -1):
        pv = sign * p * dirs
        ppar = pv @ Khat
        En = gam * (E + bet * ppar)
        ppar_lab = gam * (ppar + bet * E)
        pl = pv + (ppar_lab - ppar)[:, None] * Khat
        out.append(np.concatenate([En[:, None], pl], axis=1))
    return k1, k2, out[0], out[1], s, p / E
