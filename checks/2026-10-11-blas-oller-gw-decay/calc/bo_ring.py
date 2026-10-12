"""Ring/shell engine for the B&O eq. S6 rate in their narrow-band approximation (omega_s = 1, G = 1).

Derivation (notes/taskA_derivation_notes.md has the steps):
  A(q1,q2) = (1/2) int dk1~ dk2~ sum_{l1 l2} f_l1(k1) f_l2(k2) M (2pi)^4 delta^4,   P = (1/2) sum_s int dq1~ dq2~ |A|^2
  (the first 1/2 is B&O's 4 pi G = (1/2) 8 pi G in eq. 7; the second is photon indistinguishability), dk~ = d^3k/((2pi)^3 2k).
  With |k_i| = omega in all denominators, 2 pi delta(E) -> T and the exact ring Jacobian
      int d^3k (both |K/2 -+ k| in the band) = (omega sigma)^2/K int_0^{2pi} d alpha ,
  and the profile H(n) = A_amp h(n) with int dOmega |h|^2 = 1, N = omega sigma A_amp^2/(16 pi^3):
      dP/dt = C G^2 N^2 omega^3 sigma^2 ,   C = J/(8192 pi^5),
      J = int_0^2 dK int dOmega_K int dOmega_cm  beta  sum_final | int_0^{2pi} d alpha  m(K, alpha; n) |^2
  where m is the two-graviton -> pair amplitude with the profile tensors h inserted (G = omega = 1) and beta the
  final-state CM velocity (1 for massless).  B&O's top-hat model: C = 3/(25 pi).
Axisymmetric patterns (all used here): int dOmega_K = 2 pi int dcos theta_K at phi_K = 0 (checked numerically)."""
from __future__ import annotations

import math

import numpy as np

import bo_common as bc

PI = math.pi


def gl(n, a, b):
    x, w = np.polynomial.legendre.leggauss(n)
    return 0.5 * (b - a) * x + 0.5 * (b + a), 0.5 * (b - a) * w


def cm_grid(nth, nph, split=True):
    """CM direction grid: Gauss-Legendre in cos(theta) (split at 0, where the ring lies) x uniform phi."""
    if split:
        c1, w1 = gl(nth, -1, 0)
        c2, w2 = gl(nth, 0, 1)
        c, w = np.concatenate([c1, c2]), np.concatenate([w1, w2])
    else:
        c, w = gl(nth, -1, 1)
    ph = (np.arange(nph) + 0.5) * 2 * PI / nph
    C, PH = np.meshgrid(c, ph, indexing="ij")
    W = np.outer(w, np.full(nph, 2 * PI / nph))
    return C.ravel(), PH.ravel(), W.ravel()


# ---------------------------------------------------------------- integrands m(alpha, n) for one K
def m_photon_physical(k1, k2, q1, q2, s, pat, engine="spinor"):
    """Returns list over final photon helicity states of arrays (Na, Nn) of amplitudes with pattern tensors."""
    n1 = k1[:, 1:] / np.linalg.norm(k1[:, 1:], axis=1, keepdims=True)
    n2 = k2[:, 1:] / np.linalg.norm(k2[:, 1:], axis=1, keepdims=True)
    H1, H2 = bc.to4(bc.pattern(pat, n1)), bc.to4(bc.pattern(pat, n2))
    if engine == "spinor":
        L1, L2, Lq1, Lq2 = bc.lam(k1), bc.lam(k2), bc.lam(q1), bc.lam(q2)
        cm1, cp1 = bc.graviton_coeffs(k1, H1, L1)
        cm2, cp2 = bc.graviton_coeffs(k2, H2, L2)
        out = []
        for la, lb in ((Lq1, Lq2), (Lq2, Lq1)):
            A = (cm1 * cp2)[:, None] * bc.F_photon(la[None], lb[None], L1[:, None], L2[:, None], s) \
                + (cp1 * cm2)[:, None] * bc.F_photon(la[None], lb[None], L2[:, None], L1[:, None], s)
            out.append(A)
        return out
    raise ValueError("engine must be 'spinor' (use m_photon_physical_module for the module route)")


def m_photon_physical_module(k1, k2, Q1, Q2, s, pat):
    """Module route (qft_second_order.amplitude_gg_to_photons), all four photon helicity states."""
    import qft_second_order as q2
    n1 = k1[:, 1:] / np.linalg.norm(k1[:, 1:], axis=1, keepdims=True)
    n2 = k2[:, 1:] / np.linalg.norm(k2[:, 1:], axis=1, keepdims=True)
    H1, H2 = bc.to4(bc.pattern(pat, n1)), bc.to4(bc.pattern(pat, n2))
    out = []
    for s1, s2 in ((1, -1), (-1, 1), (1, 1), (-1, -1)):
        e1 = np.stack([q2.photon_polarization(q, s1) for q in Q1])
        e2 = np.stack([q2.photon_polarization(q, s2) for q in Q2])
        # explicit broadcast to the full (n_graviton, n_photon) grid: the reviewed module (2026-10-11 17:11)
        # no longer broadcasts (n,1,.) against (1,m,.) inside its CM frame helper
        nk, nq = k1.shape[0], Q1.shape[0]
        B = lambda x, gr: np.broadcast_to(x[:, None] if gr else x[None], (nk, nq) + x.shape[1:])  # noqa: E731
        A = q2.amplitude_gg_to_photons(B(k1, 1), B(H1, 1), B(k2, 1), B(H2, 1),
                                       B(Q1, 0), B(e1, 0), B(Q2, 0), B(e2, 0))
        out.append(np.asarray(A))
    return out


def m_photon_bo(k1, k2, q1, q2, s, profile):
    """B&O model: real eq.-6 amplitudes summed as in eq. 7: g(k1) g(k2) 8 pi (t^2 + u^2)/s for each of the two
    photon states (f_+ = f_- = g)."""
    n1 = k1[:, 1:] / np.linalg.norm(k1[:, 1:], axis=1, keepdims=True)
    n2 = k2[:, 1:] / np.linalg.norm(k2[:, 1:], axis=1, keepdims=True)
    g1, g2 = bc.bo_profile(profile, n1), bc.bo_profile(profile, n2)
    t = bc.mdot(k1[:, None] - q1[None], k1[:, None] - q1[None])
    u = bc.mdot(k1[:, None] - q2[None], k1[:, None] - q2[None])
    A = (g1 * g2)[:, None] * 8 * PI * (t * t + u * u) / s
    return [A, A]


def m_scalar_physical(k1, k2, q1, q2, s, pat, engine="spinor"):
    n1 = k1[:, 1:] / np.linalg.norm(k1[:, 1:], axis=1, keepdims=True)
    n2 = k2[:, 1:] / np.linalg.norm(k2[:, 1:], axis=1, keepdims=True)
    H1, H2 = bc.to4(bc.pattern(pat, n1)), bc.to4(bc.pattern(pat, n2))
    if engine == "spinor":
        L1, L2, Lq1, Lq2 = bc.lam(k1), bc.lam(k2), bc.lam(q1), bc.lam(q2)
        cm1, cp1 = bc.graviton_coeffs(k1, H1, L1)
        cm2, cp2 = bc.graviton_coeffs(k2, H2, L2)
        s13 = bc.mdot(q1[None] - k1[:, None], q1[None] - k1[:, None])
        s14 = bc.mdot(q1[None] - k2[:, None], q1[None] - k2[:, None])
        A = (cm1 * cp2)[:, None] * bc.F_scalar(Lq1[None], Lq2[None], L1[:, None], L2[:, None], s, s13, s14) \
            + (cp1 * cm2)[:, None] * bc.F_scalar(Lq1[None], Lq2[None], L2[:, None], L1[:, None], s, s14, s13)
        return [A]
    raise ValueError("engine must be 'spinor' (use m_scalar_physical_module for the module route)")


def m_scalar_physical_module(k1, k2, Q1, Q2, s, pat, m=0.0):
    import qft_second_order as q2
    n1 = k1[:, 1:] / np.linalg.norm(k1[:, 1:], axis=1, keepdims=True)
    n2 = k2[:, 1:] / np.linalg.norm(k2[:, 1:], axis=1, keepdims=True)
    H1, H2 = bc.to4(bc.pattern(pat, n1)), bc.to4(bc.pattern(pat, n2))
    nk, nq = k1.shape[0], Q1.shape[0]
    B = lambda x, gr: np.broadcast_to(x[:, None] if gr else x[None], (nk, nq) + x.shape[1:])  # noqa: E731
    return [np.asarray(q2.amplitude_gg_to_scalars(B(k1, 1), B(H1, 1), B(k2, 1), B(H2, 1),
                                                  B(Q1, 0), B(Q2, 0), m))]


def m_scalar_bo(k1, k2, q1, q2, s, profile, m=0.0, combo="coherent"):
    """B&O model for scalars with eq. S10 amplitudes (real), f_+ = f_- = g:
    sum_{l1 l2} f f A_{l1 l2} = g g (2 A_{++} + 2 A_{+-}) ('coherent'); 'opp_only' keeps only A_{+-}, A_{-+};
    'same_only' only A_{++}, A_{--}."""
    n1 = k1[:, 1:] / np.linalg.norm(k1[:, 1:], axis=1, keepdims=True)
    n2 = k2[:, 1:] / np.linalg.norm(k2[:, 1:], axis=1, keepdims=True)
    g1, g2 = bc.bo_profile(profile, n1), bc.bo_profile(profile, n2)
    t = bc.mdot(k1[:, None] - q1[None], k1[:, None] - q1[None])
    u = bc.mdot(k1[:, None] - q2[None], k1[:, None] - q2[None])
    den = (t - m * m) * (u - m * m)
    App = -8 * PI * m ** 4 * s / den
    Apm = -8 * PI * (m ** 4 - t * u) ** 2 / (s * den)
    if combo == "coherent":
        tot = 2 * App + 2 * Apm
    elif combo == "opp_only":
        tot = 2 * Apm
    else:
        tot = 2 * App
    return [(g1 * g2)[:, None] * tot]


# ---------------------------------------------------------------- the integral J and coefficient C
ALPHA_OFFSET = 0.3819660112501051      # irrational fraction of a step: ring nodes never coincide with photon azimuths


def coefficient(mfun, NK=16, NthK=16, nth=12, nph=32, na=64, m=0.0, phiK=0.0, Kmax=None, c_alpha=16.0,
                splitK=True, return_K=False, c_pole=0.0, na_max=4096):
    """C = J/(8192 pi^5) for amplitude function mfun(k1, k2, q1, q2, s) -> list of (Na, Nn) arrays.

    Quadrature: K Gauss-Legendre on [0, Kmax]; cos theta_K Gauss-Legendre, split at +-K/2 (splitK: where the ring
    of graviton directions passes through the poles n = +-z, at which the polar-frame patterns are singular);
    CM final-state direction: Gauss-Legendre in cos theta split at 0 (the ring plane, where final particles can be
    collinear with gravitons) x uniform phi; ring angle alpha: uniform (periodic trapezoid) with
    na_i = max(na, c_alpha/|cos theta_i|, c_pole/d_pole) points at photon node i (near-collinear phase winding is
    resolved; d_pole = angular distance of the graviton ring from the poles +-z, where polar-frame patterns rotate
    rapidly), capped at na_max."""
    if Kmax is None:
        Kmax = 2.0 * math.sqrt(max(1.0 - m * m, 0.0))
    Ks, wK = gl(NK, 0.0, Kmax)
    cth, wth = np.concatenate([gl(nth, -1, 0)[0], gl(nth, 0, 1)[0]]), np.concatenate([gl(nth, -1, 0)[1], gl(nth, 0, 1)[1]])
    phis = (np.arange(nph) + 0.5) * 2 * PI / nph
    J = 0.0
    jK = []
    for K, wk in zip(Ks, wK):
        if splitK:
            bps = [-1.0, -K / 2, K / 2, 1.0]
            nodes = [gl(NthK, bps[i], bps[i + 1]) for i in range(3)]
            cK = np.concatenate([x for x, _ in nodes])
            wcK = np.concatenate([w for _, w in nodes])
        else:
            cK, wcK = gl(NthK, -1.0, 1.0)
        acc = 0.0
        th_r = math.acos(min(K / 2.0, 1.0))
        for c, wc in zip(cK, wcK):
            st = math.sqrt(max(1 - c * c, 0.0))
            Khat = np.array([st * math.cos(phiK), st * math.sin(phiK), c])
            thK = math.acos(max(-1.0, min(1.0, c)))
            d_pole = max(min(abs(thK - th_r), abs(PI - thK - th_r)), 1e-6)
            val = 0.0
            beta = 1.0
            for ci, wi in zip(cth, wth):
                nai = int(min(na_max, max(na, math.ceil(c_alpha / abs(ci)), math.ceil(c_pole / d_pole))))
                alphas = (np.arange(nai) + ALPHA_OFFSET) * 2 * PI / nai
                k1, k2, q1, q2, s, beta = bc.ring_and_photons(K, Khat, alphas, np.full(nph, ci), phis, m)
                for A in mfun(k1, k2, q1, q2, s):
                    R = A.sum(axis=0) * (2 * PI / nai)
                    val += wi * (2 * PI / nph) * np.sum(np.abs(R) ** 2)
            acc += 2 * PI * wc * beta * val
        jK.append(acc)
        J += wk * acc
    Cval = J / (8192 * PI ** 5)
    if return_K:
        return Cval, np.array(Ks), np.array(jK) / (8192 * PI ** 5)
    return Cval
