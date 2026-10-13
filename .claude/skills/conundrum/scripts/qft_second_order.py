#!/usr/bin/env python3
"""qft_second_order: production SECOND order in a classical background. Tree-level graviton fusion
g g -> gamma gamma and g g -> phi phi in Einstein-Maxwell (+ a minimally coupled real or complex scalar),
as on-shell amplitudes and as the mean number of pairs that two crossing classical gravitational waves
make (numpy only; imports qft_production for units and its first-order spectral machinery).

Why this tool exists
    qft_production Part D shows that a single gravitational plane wave, or any freely propagating packet,
    makes NO pairs at first order: every Fourier component of a free wave is null. Two NON-collinear waves
    have K = q1 + q2 timelike, so pairs appear at second order in the background. Every public function
    says which quantity it returns ("Quantity:") and when it applies ("Valid when:"), and refuses inputs
    outside that range with ValueError. The traps kept apart: in-out amplitude vs in-in mean number;
    plane waves (rates per volume per time) vs packets; real pairs (on-shell, energy conserving) vs
    transient polarisation; pair-number rate vs vacuum decay; pairs vs particles (photons and a real
    scalar are identical particles: a factor 1/2 in the final-state phase space).

Units and conventions (read this first)
    Natural units hbar = c = 1; Heaviside-Lorentz electromagnetism (e^2 = 4 pi alpha; no charge enters
    here). Metric signature (+,-,-,-), K.x = K0 t - K.x. Energies, momenta, frequencies in ONE chosen
    energy unit; G (Newton's constant) in 1/energy^2 (G = 1/M_Pl^2, M_Pl = 1.2209e28 eV); rates per volume
    in energy^4, cross sections in 1/energy^2. SI helpers convert (newton_G_natural, beams_pair_rate_SI);
    the command line accepts units through unit_tools.Q ("1 kHz", "1 eV").
    Gravity: g = eta + kappa h, kappa^2 = 32 pi G, h canonical (L2 = (1/2) d h d h - ... in de Donder gauge,
    propagator i P/(K^2 + i0), P = (eta eta + eta eta - eta eta)/2). Matter couples as
    L = -(kappa/2) h_{mu nu} T^{mu nu} + O(kappa^2). Field equation G_{mu nu} = 8 pi G T_{mu nu} with
    R_{mu nu} = d_r Gamma^r_{mu nu} - d_nu Gamma^r_{mu r} + Gamma Gamma - Gamma Gamma.
    Maxwell: L = -(1/4) sqrt(-g) g^{ma} g^{nb} F_mn F_ab. Scalar: L = sqrt(-g)[(1/2) g^{mn} d phi d phi - m^2 phi^2/2]
    (minimal coupling, xi = 0; complex: g^{mn} d phi* d phi - m^2 |phi|^2).
    Polarisations: photon e_+-(n) = (-+ e_theta - i e_phi)/sqrt2 (helicity +-1 along n, e_theta, e_phi the
    spherical unit vectors of n), graviton helicity +-2: eps_{mu nu} = e_mu e_nu (lower indices),
    linear 'plus' = (e_th e_th - e_ph e_ph)/sqrt2, 'cross' = (e_th e_ph + e_ph e_th)/sqrt2; all normalised
    eps*^{mu nu} eps_{mu nu} = 1, transverse and traceless.

PART A. The tree amplitude M(q1 eps1, q2 eps2 -> k1 s1, k2 s2) by the background-field method
-------------------------------------------------------------------------------------------
    Put the two gravitons in as classical plane waves h = eps1 e^{-i q1 x} + eps2 e^{-i q2 x} and expand the
    matter action in the metric to second order. The coefficient of e^{-i(q1+q2)x} gives (kappa^2 x):
      contact  : -(1/2) C2^{ma nb}[eps1, eps2] f1_mn f2_ab, C2 = cross term of sqrt(-g) g^{ma} g^{nb} at O(h^2),
                 f_mn = i(k_m e*_n - k_n e*_m) (outgoing photon); scalar: -S2^{mn} k1_m k2_n - m^2 c2;
      t, u     : two O(h) vertices joined by the photon (scalar) propagator, internal momentum k1 - q1 (k2 - q1);
      s-channel: the O(h) vertex fed with the SECOND-ORDER metric h^(2): G^(1)[h^(2)] = -G^(2)[h^(1), h^(1)]
                 (vacuum Einstein equation at second order; G^(2) = cross term of the Einstein tensor, built
                 from the Christoffel symbols of the two waves, solved in de Donder gauge
                 h^(2) = (2/K^2)(S - eta tr S/2), S = -G^(2), K = q1 + q2). This IS s-channel graviton exchange
                 with the cubic vertex, without writing the vertex down.
    M is dimensionless (kappa^2 x energy^2); the anchor |M| ~ 8 pi G s holds (photons: |M| = 8 pi G t^2/s <= 8 pi G s;
    massless scalars: 8 pi G |t u|/s <= 2 pi G s). Only the SUM is gauge invariant:
    eps_{mn} -> eps_{mn} + q_m xi_n + xi_m q_n (q.xi = 0) changes each channel by O(1) and the sum by
    roundoff (self-test). Photon shifts e -> e + c k leave every piece invariant by construction (all
    vertices are built from F). Results (checked against the literature in the self-test):
      * massless final states: M = 0 unless the two incoming gravitons have OPPOSITE helicity (total J_z = +-4
        along the collision axis); then |M| = (kappa/2)^2 t^2/s or (kappa/2)^2 u^2/s for the two opposite photon
        helicity assignments (same-helicity photons: 0), and (kappa/2)^2 |t u|/s for massless scalars.
        Same-helicity gravitons make neither photon pairs nor massless scalar pairs at tree level (for a massive
        scalar the same-helicity amplitude is ~ m^4 and nonzero).
      * CM cross sections (massless; for given opposite incoming helicities, summed over final helicities,
        identical-particle 1/2 included): sigma(gamma gamma) = (4/5) pi G^2 s, sigma(phi phi, real) = pi G^2 s/15
        (complex scalar, particle + antiparticle: 2 pi G^2 s/15); same helicities: 0. Linear polarisations
        (massless final states, any relative orientation): half the opposite-helicity value, because the two
        opposite-helicity channels (J_z = +4 and -4) do not interfere in the total cross section.
      * Crossing gives gravitational Compton scattering gamma g -> gamma g and phi g -> phi g (compton_amplitude).

Why contact and photon-exchange terms are not an "effective background" for qft_production Part D
    Part D couples a background to the pair only through -(1/2) h~_{mn}(K) T^{mn}(k1, k2), i.e. the pair
    amplitude depends on the final state only through the stress-tensor matrix element T^{mn}(k1, k2): a
    10-dimensional space at fixed K. The s-channel piece has exactly that form with h~ = kappa^2 h^(2)(K) (so
    qp.born_metric_general can take the second-order metric as its h~; the self-test checks that the phase-space
    integral of |M_s|^2 equals qp's (1/4)[rho2 X2 + rho0 X0]). The contact term contracts the two waves'
    polarisations with f1 and f2 SEPARATELY (e.g. eps1^{ma} eps2^{nb} f1_mn f2_ab), and the t/u terms carry the
    propagators 1/(k1 - q1)^2, 1/(k2 - q1)^2, which depend on k1 and k2 separately, not on K alone; the self-test
    shows numerically that the full amplitude lies outside the span of {h.T}. Since only the sum is gauge
    invariant, the s-channel (and hence Part D fed with h^(2)) alone is not a physical answer: for two same-helicity
    waves at 90 degrees Part D predicts about 8 times (8.26) the photon pairs an R/L pair really makes, while the
    full amplitude gives none;
    head-on R/L waves give the reverse (Part D zero, full nonzero); for linear polarisations it is off by
    angle-dependent factors (Part D/full, measured: plus/plus 22, 11, 3.0 at 30, 90, 180 deg; plus/cross 18, 9,
    1.09 at 30, 90, 150 deg and Part D zero head-on; R/L 3.6, 1.01, 0.25 at 30, 90, 120 deg). The self-test checks
    the first two cases.

PART B. Production by two classical waves (coherent states), in-in mean number of PAIRS
-------------------------------------------------------------------------------------
    A classical wave is the coherent state |alpha> with <h_can> = A eps e^{-iqx} + c.c.; its metric perturbation
    is delta g = kappa h_can = H e^{-iqx} + c.c., H = kappa A eps (dimensionless strain tensor). TT plane wave
    with GR strain amplitude h: 'plus' h_xx = -h_yy = h cos(w t - q.x): H = (h/sqrt2) eps_plus;
    circular ('R' = helicity +2, 'L' = -2) h_+ = h cos, h_x = +-h sin: H = h eps_{+-2}.
    Energy density rho = <hdot_ij hdot_ij>/(32 pi G) = w^2 |H|^2/(16 pi G) ('plus': w^2 h^2/(32 pi G)), number
    density n = rho/w = 2 w |A|^2.
    To leading order the background-field S-matrix makes the two-photon state with amplitude
        A(k1, k2) = int dq1~ dq2~ alpha_a(q1) alpha_b(q2) M(q1, q2 -> k1, k2) (2pi)^4 delta^4(q1 + q2 - k1 - k2):
    the 1/2! of the coherent-state expansion cancels the two ways of taking one graviton from each beam (identical
    gravitons); a single beam's own square has K = 2q null and gives nothing. The mean number of pairs is
        N = (1/2) int dPi1 dPi2 sum_{s1 s2} |A|^2      (1/2: identical photons; no 1/2 for a complex scalar).
    For two monochromatic plane waves the delta^4 squares to V T, so pairs per unit volume per unit time are
        Gamma = (1/2) int dPhi2 sum |M(H_a, H_b)|^2  (kappa = 1: G drops out at fixed strain)
              = sigma(s) n_a n_b (1 - cos theta),    s = 2 w_a w_b (1 - cos theta),
    sigma being the cross section for the waves' polarisation states. Gamma is G-independent at fixed strain
    (sigma ~ G^2 s, n ~ w h^2/G): linear polarisations give Gamma = w_a^2 w_b^2 h_a^2 h_b^2 (1 - cos th)^2/(1280 pi)
    for photons. It vanishes as theta -> 0 (collinear waves: s -> 0). Each produced photon pair carries energy
    ~ hbar w, so the emitted power is a quantum (vacuum-fluctuation) effect: the classical Einstein-Maxwell
    equations make no electromagnetic field from zero field.
    Gamma is the in-in mean pair number per volume per time at leading order (rate ~ h_a^2 h_b^2); the vacuum-decay
    rate from the in-out persistence |<0out|0in>|^2 = 1 - N + ... equals it at this order and differs only at
    higher order. Photons (or scalar particles) per volume per time = 2 Gamma.

Self-test references (python3 qft_second_order.py selftest)
    Exact: metric expansion (det/inv), Bianchi identity of G^(2), Ward identities, Bose symmetry, Newton (Poisson),
    GR light bending (theta = 4 G m/b) as the small-angle limit of graviton-mass scattering.
    Published: Isaacson stress (Flanagan & Hughes 2005, eqs. 5.35, 5.40, 5.41); Holstein 2006 eq. 66 (massive-scalar
    gravitational Compton, unpolarised lab cross section: agrees to 1e-14); Bjerrum-Bohr, Donoghue & Vanhove 2014
    eq. II.27 and Bjerrum-Bohr et al. 2016 eqs. A.10, A.11, A.16 (helicity amplitudes: shapes agree to 1e-12; the
    PRINTED normalisations of II.27 (= 2016 A.13) and A.10-A.11 are 2x and 4x ours, which agree with Holstein and
    with the one-graviton forward limit of A.16); qft_production's stress spectral densities (s-channel); the
    luminosity relation from two independent phase-space routes; the analytic same-helicity massive-scalar cross
    section (sigma_same_helicity_scalar_closed_form) for the graded quadrature; extreme boosts (frequency ratio 1e-12,
    opening angle 1e-9) against the closed forms.

Numerics (why the answers survive boosts)
    The channels are individually ~ kappa^2 s (K0^2/s)^2 in a frame where K = q1 + q2 moves fast and cancel to
    ~ kappa^2 t^2/s; contracted in such a frame they lose ~ (K0^2/s)^2 digits. Every physical entry point therefore
    first carries the momenta and wavefunctions to the CM of K (_CMFrame: light-cone variables, s = K+ K- with
    K- = q1- + q2- summed from cancellation-free components, the polarisations mapped in closed form straight to the
    CM radiation gauge, exact by the Ward identities) and reconstructs exact CM kinematics there. Polarisation frames
    are built without arccos (which loses 1e-16/theta near the poles). Measured: boosted g g -> gamma gamma and
    Compton amplitudes agree with the exact formulas to < 1e-14 for K0^2/s up to 4e24; beam rates agree with
    sigma n1 n2 (1 - cos theta) to < 1e-14 for w2/w1 down to 1e-20 and theta down to 1e-13. Remaining roundoff: the
    suppressed (kappa/2)^2 t^2/s amplitude, relative ~ 1e-16 s/|t| (3.5e-6 at theta = 1e-5); the massive
    same-helicity scalar amplitude ~ m^4/s, relative ~ 3e-17 s^2/m^4 at generic angles (3e-5 at m^2/s = 1e-6) and
    its cross section ~ 1e-14 s/m^2 (phase space refused below m^2/s = 1e-8).

Assumptions and validity range
    Tree level, flat background, |h| << 1 (refused at h >= 0.1), s << M_Pl^2, monochromatic infinite plane
    waves for rates (for long narrow-band packets multiply by the overlap 4-volume: not validated here), no
    medium or plasma (photons massless in vacuum), the classical waves prescribed (no back-reaction).

Python usage
    import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
    import numpy as np, qft_second_order as q2
    amps = q2.helicity_amplitudes_cm(s=4.0, theta=1.0, final="photon")    # {(l1, l2, s1, s2): M}, G = 1
    q2.sigma_total(4.0, "R", "L", final="photon")                          # = (4/5) pi G^2 s
    q2.beams_pair_rate(1.0, 1e-3, 1.0, 1e-3, np.pi, "plus", "plus")       # pairs per volume per time (w units)
    q2.beams_pair_rate_SI(2 * np.pi * 1e3, 1e-21, np.pi)                    # m^-3 s^-1
    a = q2.gw_plane_wave(1.0, 1e-3, [0, 0, 1], "R"); b = q2.gw_plane_wave(1.0, 1e-3, [1, 0, 0], "L")
    q2.second_order_metric(a["q"], a["H"], b["q"], b["H"])["dg2"]        # second-order metric (de Donder)

Command line (from the project root)
    python3 .claude/skills/conundrum/scripts/qft_second_order.py selftest
    python3 .claude/skills/conundrum/scripts/qft_second_order.py beams --omega "1 kHz" --h 1e-21 --theta 180
    python3 .claude/skills/conundrum/scripts/qft_second_order.py beams --f "100 Hz" --h 1e-20 --theta 90 --pol1 R --pol2 L
    python3 .claude/skills/conundrum/scripts/qft_second_order.py amplitudes --theta 60 --final scalar --m 0.5
    python3 .claude/skills/conundrum/scripts/qft_second_order.py compton --omega 0.3 --theta 40     (omega/m; G^2 m^2)
    python3 .claude/skills/conundrum/scripts/qft_second_order.py convergence    (quadrature and roundoff studies)
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

import qft_production as qp  # noqa: E402  (units and the first-order spectral machinery)
from unit_tools import C, E_CHARGE, HBAR  # noqa: E402
from unit_tools import G as G_SI  # noqa: E402

PI = math.pi
_ETA = np.diag([1.0, -1.0, -1.0, -1.0])
_ED = np.array([1.0, -1.0, -1.0, -1.0])
_POLS = ("R", "L", "plus", "cross")
_ONSHELL_TOL = 1e-9        # |p^2|/E^2 allowed for on-shell inputs (double-precision kinematics built by hand)


# ---------------------------------------------------------------- SI helpers
def newton_G_natural(unit_eV: float = 1.0) -> float:
    """Newton's constant in natural units, G = 1/M_Pl^2, for energies measured in units of unit_eV electronvolts.

    M_Pl = sqrt(hbar c^5/G)/e = 1.22089e28 eV (CODATA G = 6.67430e-11 m^3 kg^-1 s^-2 from unit_tools).
    Quantity: G in 1/(unit_eV eV)^2 (e.g. 6.7087e-57 eV^-2 for unit_eV = 1).
    Valid when: unit_eV > 0."""
    if not unit_eV > 0:
        raise ValueError("unit_eV must be > 0")
    m_pl = math.sqrt(HBAR * C ** 5 / G_SI) / E_CHARGE
    return (unit_eV / m_pl) ** 2


def area_to_SI(sigma_eV2: float) -> float:
    """Convert a cross section from 1/eV^2 to m^2: sigma_SI = sigma (hbar c/e)^2.

    Quantity: area in m^2.
    Valid when: sigma_eV2 is in eV^-2."""
    return sigma_eV2 * (HBAR * C / E_CHARGE) ** 2


# ---------------------------------------------------------------- tensor helpers (lower-index tensors, upper vectors)
def _low(v):
    return v * _ED


def _dot(a, b):
    return np.einsum("...m,...m->...", a, _low(b))


def _up2(H):
    return H * _ED[:, None] * _ED[None, :]


def _tr(H):
    return np.einsum("...aa,a->...", H, _ED)


def _o4(A, B):
    return np.einsum("...ma,...nb->...manb", A, B)


def _mm(Au, Bu):
    return np.einsum("...ml,l,...ln->...mn", Au, _ED, Bu)


def _x(v, n):
    return np.asarray(v)[(...,) + (None,) * n]


def _dG1(H):
    """First-order part of sqrt(-g) g^{ma} g^{nb} (upper indices) for g = eta + H (H lower)."""
    Hu = _up2(H)
    e = np.broadcast_to(_ETA, Hu.shape)
    return 0.5 * _x(_tr(H), 4) * _o4(e, e) - _o4(Hu, e) - _o4(e, Hu)


def _cross_scalars(A, B):
    """Cross terms at O(H^2), H = A + B: c2 of sqrt(-g) and g2^{mn} of g^{mn}."""
    Au, Bu = _up2(A), _up2(B)
    c2 = 0.25 * _tr(A) * _tr(B) - 0.5 * np.einsum("...ab,...ab->...", Au, B)
    return Au, Bu, c2, _mm(Au, Bu) + _mm(Bu, Au)


def _dG2(A, B):
    """Cross (A B) part of sqrt(-g) g^{ma} g^{nb} at second order."""
    Au, Bu, c2, g2 = _cross_scalars(A, B)
    e = np.broadcast_to(_ETA, Au.shape)
    tA, tB = _x(_tr(A), 4), _x(_tr(B), 4)
    out = _x(c2, 4) * _o4(e, e) - 0.5 * tA * (_o4(Bu, e) + _o4(e, Bu)) - 0.5 * tB * (_o4(Au, e) + _o4(e, Au))
    return out + _o4(g2, e) + _o4(e, g2) + _o4(Au, Bu) + _o4(Bu, Au)


def _dS1(H):
    """First-order parts of sqrt(-g) g^{mn} (upper) and sqrt(-g)."""
    return 0.5 * _x(_tr(H), 2) * _ETA - _up2(H), 0.5 * _tr(H)


def _dS2(A, B):
    """Cross parts of sqrt(-g) g^{mn} and sqrt(-g) at second order."""
    Au, Bu, c2, g2 = _cross_scalars(A, B)
    return _x(c2, 2) * _ETA - 0.5 * _x(_tr(A), 2) * Bu - 0.5 * _x(_tr(B), 2) * Au + g2, c2


# ---------------------------------------------------------------- second-order Einstein tensor
def _christoffel_low(E, q):
    """Gamma_{r m n} = (1/2)(d_m h_rn + d_n h_rm - d_r h_mn) for h = E e^{-iqx} (d -> -i q_lower)."""
    ql = _low(q)
    return -0.5j * (np.einsum("...m,...rn->...rmn", ql, E) + np.einsum("...n,...rm->...rmn", ql, E)
                    - np.einsum("...r,...mn->...rmn", ql, E))


def _ricci1(E, q):
    """Linearised Ricci tensor of h = E e^{-iqx} (zero for an on-shell transverse-traceless wave or pure gauge)."""
    ql = _low(q)
    Kh = np.einsum("...s,...sn->...n", q, E)
    return 0.5 * (-np.einsum("...m,...n->...mn", ql, Kh) - np.einsum("...n,...m->...mn", ql, Kh)
                  + _x(_dot(q, q), 2) * E + _x(_tr(E), 2) * np.einsum("...m,...n->...mn", ql, ql))


def _ricci2_ordered(EX, qX, EY, qY):
    """Coefficient of e^{-i(qX + qY)x} in R^(2)_{mn} from the products (X first, Y second)."""
    Kl = _low(qX + qY)
    GY = _christoffel_low(EY, qY)
    G2u = -np.einsum("...rs,...smn->...rmn", _up2(EX), GY)            # -h^{rs} Gamma_{s m n}
    GXu = np.einsum("...rmn,r->...rmn", _christoffel_low(EX, qX), _ED)
    GYu = np.einsum("...rmn,r->...rmn", GY, _ED)
    return (-1j * np.einsum("...r,...rmn->...mn", Kl, G2u) + 1j * np.einsum("...n,...rmr->...mn", Kl, G2u)
            + np.einsum("...rrl,...lmn->...mn", GXu, GYu) - np.einsum("...rnl,...lmr->...mn", GXu, GYu))


def _einstein2(Ea, qa, Eb, qb):
    R2 = _ricci2_ordered(Ea, qa, Eb, qb) + _ricci2_ordered(Eb, qb, Ea, qa)
    R1a, R1b = _ricci1(Ea, qa), _ricci1(Eb, qb)
    Rs = (_tr(R2) - np.einsum("...ab,...ab->...", _up2(Ea), R1b) - np.einsum("...ab,...ab->...", _up2(Eb), R1a))
    return R2 - 0.5 * _ETA * _x(Rs, 2) - 0.5 * (Ea * _x(_tr(R1b), 2) + Eb * _x(_tr(R1a), 2))


def _solve_linear(S, K):
    """h with G^(1)[h] = S in de Donder gauge: h = (2/K^2)(S - eta tr S/2) (needs K^2 != 0, K^m S_mn = 0)."""
    return _x(2.0 / _dot(K, K), 2) * (S - 0.5 * _ETA * _x(_tr(S), 2))


# ---------------------------------------------------------------- amplitude cores (kappa = 1, wavefunctions given)
def _fout(k, w):
    kl, wl = _low(k), _low(w)
    return 1j * (np.einsum("...m,...n->...mn", kl, wl) - np.einsum("...m,...n->...mn", wl, kl))


def _contact_ph(C4, f1, f2):
    return -0.5 * np.einsum("...manb,...mn,...ab->...", C4, f1, f2)


def _vertex_ph(C4, fext, p_in):
    pl = _low(p_in)
    eye = np.eye(4)
    fint = -1j * (np.einsum("...a,lb->...lab", pl, eye) - np.einsum("...b,la->...lab", pl, eye))
    return -0.5 * np.einsum("...manb,...mn,...lab->...l", C4, fext, fint)


def _core_photon(qa, Ea, qb, Eb, k1, w1, k2, w2):
    """kappa = 1 parts (contact, s, t+u) with OUTGOING-slot photon wavefunctions w1, w2 (e* for a real outgoing photon)."""
    f1, f2 = _fout(k1, w1), _fout(k2, w2)
    Mc = _contact_ph(_dG2(Ea, Eb), f1, f2)
    h2 = _solve_linear(-_einstein2(Ea, qa, Eb, qb), qa + qb)
    Ms = _contact_ph(_dG1(h2), f1, f2)
    Ca, Cb = _dG1(Ea), _dG1(Eb)
    Mtu = 0.0
    for fa, ka, fb in ((f1, k1, f2), (f2, k2, f1)):
        p = ka - qa
        Mtu = Mtu + _dot(_vertex_ph(Ca, fa, p), _vertex_ph(Cb, fb, -p)) / _dot(p, p)
    return Mc, Ms, Mtu


def _pair_sc(Sup, c, ka, kb, m):
    return -np.einsum("...mn,...m,...n->...", Sup, _low(ka), _low(kb)) - m * m * c


def _core_scalar(qa, Ea, qb, Eb, k1, k2, m):
    S2, c2 = _dS2(Ea, Eb)
    Mc = _pair_sc(S2, c2, k1, k2, m)
    S1, c1 = _dS1(_solve_linear(-_einstein2(Ea, qa, Eb, qb), qa + qb))
    Ms = _pair_sc(S1, c1, k1, k2, m)
    Sa, ca = _dS1(Ea)
    Sb, cb = _dS1(Eb)
    Mtu = 0.0
    for ka, kb in ((k1, k2), (k2, k1)):
        p = ka - qa
        Va = np.einsum("...mn,...m,...n->...", Sa, _low(ka), _low(p)) - m * m * ca
        Vb = np.einsum("...mn,...m,...n->...", Sb, _low(kb), _low(-p)) - m * m * cb
        Mtu = Mtu + Va * Vb / (m * m - _dot(p, p))
    return Mc, Ms, Mtu


def _parts_out(parts, kappa2, as_parts):
    Mc, Ms, Mtu = (kappa2 * np.asarray(x) for x in parts)
    if as_parts:
        return {"contact": Mc, "s_channel": Ms, "tu_channel": Mtu, "total": Mc + Ms + Mtu}
    return Mc + Ms + Mtu


# ---------------------------------------------------------------- polarisations and input checks
def _frame(n):
    n = np.asarray(n, dtype=float)
    nn = np.linalg.norm(n)
    if not nn > 0:
        raise ValueError("direction must be nonzero")
    return _transverse_basis(n)


def _spatial(k):
    k = np.asarray(k, dtype=float)
    if k.shape == (4,):
        return k[1:]
    if k.shape == (3,):
        return k
    raise ValueError("momentum must be a 4-vector or a 3-vector")


def photon_polarization(k, hel: int) -> np.ndarray:
    """Helicity polarisation vector e^mu = (0, (-hel e_theta - i e_phi)/sqrt2) for a massless particle moving along k.

    Quantity: contravariant complex 4-vector (dimensionless), e*.e = -1, e.k = 0; hel = +1 or -1 (helicity along k).
        For an OUTGOING photon pass this physical vector; the amplitude functions conjugate it.
    Valid when: k is a nonzero 3-vector or 4-vector (only its direction is used); hel in (+1, -1)."""
    if hel not in (1, -1):
        raise ValueError("photon helicity must be +1 or -1")
    et, ep = _frame(_spatial(k))
    return np.concatenate([[0.0], (-hel * et - 1j * ep) / math.sqrt(2.0)])


def graviton_polarization(q, pol) -> np.ndarray:
    """Normalised transverse-traceless polarisation tensor eps_{mu nu} (LOWER indices) for a graviton moving along q.

    pol: 'R' or +2 (helicity +2 = e_+ e_+), 'L' or -2 (helicity -2), 'plus' = (e_th e_th - e_ph e_ph)/sqrt2,
    'cross' = (e_th e_ph + e_ph e_th)/sqrt2, e_th, e_ph the spherical unit vectors of q (for q along +z: x, y;
    for q in the x-z plane: e_th in that plane, e_ph = y).
    Quantity: 4x4 complex tensor, eps*^{mn} eps_{mn} = 1, q^m eps_{mn} = 0, eta^{mn} eps_{mn} = 0 (dimensionless).
    Valid when: q nonzero; pol one of 'R', 'L', 'plus', 'cross', +2, -2."""
    key = {2: "R", -2: "L"}.get(pol, pol) if not isinstance(pol, str) else pol
    if key not in _POLS:
        raise ValueError("graviton polarisation must be 'R' (+2), 'L' (-2), 'plus' or 'cross'")
    qs = _spatial(q)
    if key in ("R", "L"):
        e = _low(photon_polarization(qs, 1 if key == "R" else -1))
        return np.outer(e, e)
    et, ep = _frame(qs)
    a = np.concatenate([[0.0], et])
    b = np.concatenate([[0.0], ep])
    a, b = _low(a), _low(b)
    t = np.outer(a, a) - np.outer(b, b) if key == "plus" else np.outer(a, b) + np.outer(b, a)
    return t.astype(complex) / math.sqrt(2.0)


def _check_null(p, name):
    p = np.asarray(p, dtype=float)
    if p.shape[-1] != 4 or not np.all(np.isfinite(p)):
        raise ValueError(f"{name} must be a finite 4-vector")
    if np.any(np.abs(_dot(p, p)) > _ONSHELL_TOL * np.max(p[..., 0] ** 2)):
        raise ValueError(f"{name} must be light-like (on-shell massless)")
    return p


def _check_tt(q, E, name):
    E = np.asarray(E, dtype=complex)
    if E.shape[-2:] != (4, 4):
        raise ValueError(f"{name} must be a 4x4 tensor")
    scale = np.max(np.abs(q)) * max(np.max(np.abs(E)), 1e-300)
    if (np.max(np.abs(E - np.swapaxes(E, -1, -2))) > 1e-9 * max(np.max(np.abs(E)), 1e-300)
            or np.max(np.abs(np.einsum("...m,...mn->...n", q, E))) > 1e-9 * scale
            or np.max(np.abs(_tr(E))) > 1e-9 * max(np.max(np.abs(E)), 1e-300)):
        raise ValueError(f"{name} must be symmetric, transverse (q^m eps_mn = 0) and traceless (on-shell graviton)")
    return E


def _check_final(q1, q2, k1, k2, m):
    q1, q2, k1, k2 = (np.asarray(v, dtype=float) for v in (q1, q2, k1, k2))
    if np.any(q1[..., 0] <= 0) or np.any(q2[..., 0] <= 0) or np.any(k1[..., 0] <= 0) or np.any(k2[..., 0] <= 0):
        raise ValueError("production kinematics needs positive energies for all four particles")
    K = q1 + q2
    if np.max(np.abs(K - k1 - k2)) > 1e-9 * np.max(K[..., 0]):
        raise ValueError("momentum not conserved: q1 + q2 != k1 + k2")
    for k, nm in ((k1, "k1"), (k2, "k2")):
        if np.any(np.abs(_dot(k, k) - m * m) > _ONSHELL_TOL * np.max(k[..., 0] ** 2)):
            raise ValueError(f"{nm} must be on shell (k^2 = m^2)")
    _check_boost(q1, q2)
    return q1, q2, k1, k2


_MAX_BOOST2 = 1e24     # largest tested K0^2/s (self-test 18 and 'convergence'); beyond it refused


def _check_boost(pa, pb, ma=0.0):
    """Refuse kinematics so close to collinear that even the light-cone CM transformation is untested."""
    F = _CMFrame(pa, ma, pb, 0.0)
    K0 = (pa + pb)[..., 0]
    if np.any(~(F.s > 0)):
        raise ValueError("need s = (q1 + q2)^2 > 0: collinear massless momenta (s = 0)")
    if np.any(K0 * K0 > _MAX_BOOST2 * F.s):
        raise ValueError(f"K0^2/s > {_MAX_BOOST2:.0e} (nearly collinear waves or extreme frequency ratio): outside the "
                         "tested range of the CM transformation")


# ---------------------------------------------------------------- exact CM transformation (light-cone form)
def _transverse_basis(qv):
    """Spherical unit vectors (e_theta, e_phi) of the direction of the 3-vectors qv (vectorised; no arccos, which
    loses ~1e-16/theta of the polar angle near the poles: e_theta = (cos th cos ph, cos th sin ph, -sin th) with
    sin th = rho = |n_perp|, cos th = n_z, (cos ph, sin ph) = (n_x, n_y)/rho; on the axis ph = atan2(n_y, n_x))."""
    qv = np.asarray(qv, dtype=float)
    n = qv / np.linalg.norm(qv, axis=-1, keepdims=True)
    rho = np.hypot(n[..., 0], n[..., 1])
    ph = np.arctan2(n[..., 1], n[..., 0])
    on = rho > 0
    safe = np.where(on, rho, 1.0)
    cp = np.where(on, n[..., 0] / safe, np.cos(ph))
    sp = np.where(on, n[..., 1] / safe, np.sin(ph))
    et = np.stack([n[..., 2] * cp, n[..., 2] * sp, -rho], axis=-1)
    ep = np.stack([-sp, cp, np.zeros_like(cp)], axis=-1)
    return et, ep


class _CMFrame:
    """Boost along K = pa + pb to its rest frame written in light-cone variables, so that NO component cancels.

    With z^ = K/|K| (lab), v+- = v0 +- v.z^ and v_perp: the boost is v+ -> v+ sqrt(s)/K+, v- -> v- K+/sqrt(s), v_perp
    unchanged. The small light-cone component of an on-shell vector is taken from v+ v- = m^2 + |v_perp|^2 (never by
    subtraction), K- = pa- + pb- and s = K+ K- (not K0^2 - |K|^2), and pa_perp = -pb_perp from the lower-energy one.
    Polarisations are mapped to their CM transverse (radiation-gauge) part T(L f) = L f - ((L f)^0/(L q)^0) L q in
    closed form, without forming the boosted vector (whose pure-gauge part grows like the boost factor):
        T_z = f_z q0/q'0,  T_perp = f_perp + f_z |K| q_perp/(sqrt(s) q'0)      (f0 = 0 gauge first; q'0 = CM energy).
    Since the tree amplitude is gauge invariant (Ward identities, self-test 5) this changes nothing but roundoff."""

    def __init__(self, pa, ma, pb, mb):
        K = pa + pb
        Kv = K[..., 1:]
        self.Kn = np.linalg.norm(Kv, axis=-1)
        safe = np.where(self.Kn > 0, self.Kn, 1.0)
        self.z = np.where((self.Kn > 0)[..., None], Kv / safe[..., None], np.array([0.0, 0.0, 1.0]))
        a_soft = (pa[..., 0] <= pb[..., 0])[..., None]
        perp_a = np.where(a_soft, self._perp(pa), -self._perp(pb))
        self.perp_ab = (perp_a, -perp_a)
        pa_pm, pb_pm = self._pm(pa, ma, perp_a), self._pm(pb, mb, -perp_a)
        self.Kp = pa_pm[0] + pb_pm[0]
        self.s = self.Kp * (pa_pm[1] + pb_pm[1])
        self.rs = np.sqrt(self.s)

    def _perp(self, v):
        """Component of v's 3-vector transverse to z^, as z^ x (v x z^) (no cancellation for v nearly along z^)."""
        z = np.broadcast_to(self.z, v[..., 1:].shape)
        return np.cross(z, np.cross(v[..., 1:], z))

    def _pm(self, v, m, perp):
        vz = np.einsum("...i,...i->...", v[..., 1:], self.z)
        tr = m * m + np.einsum("...i,...i->...", perp, perp)
        fwd = vz >= 0
        big = np.where(fwd, v[..., 0] + vz, v[..., 0] - vz)
        small = tr / big
        return np.where(fwd, big, small), np.where(fwd, small, big)

    def vec(self, v, m=0.0, perp=None):
        """CM components (same spatial axes) of the on-shell vector v of mass m."""
        perp = self._perp(v) if perp is None else perp
        vp, vm = self._pm(v, m, perp)
        vp, vm = vp * self.rs / self.Kp, vm * self.Kp / self.rs
        return np.concatenate([(0.5 * (vp + vm))[..., None], perp + (0.5 * (vp - vm))[..., None] * self.z], axis=-1)

    def pol(self, f, q, q0c, perp_q=None):
        """CM transverse part of the polarisation vector f (upper, f.q = 0) of the massless momentum q; q0c its CM energy."""
        f = f - (f[..., 0] / q[..., 0])[..., None] * q
        perp_q = self._perp(q) if perp_q is None else perp_q
        fz = np.einsum("...i,...i->...", f[..., 1:], self.z)
        fperp = f[..., 1:] - fz[..., None] * self.z
        Tz = fz * q[..., 0] / q0c
        Tv = fperp + (fz * self.Kn / (self.rs * q0c))[..., None] * perp_q + Tz[..., None] * self.z
        return np.concatenate([np.zeros(Tv.shape[:-1] + (1,), dtype=Tv.dtype), Tv], axis=-1)

    def tensor(self, E, q, q0c, perp_q=None):
        """CM TT part of the graviton polarisation tensor E (lower indices, q^m E_mn = 0) of the momentum q."""
        et, ep = _transverse_basis(q[..., 1:])
        z0 = np.zeros(et.shape[:-1] + (1,))
        basis = [np.concatenate([z0, et], axis=-1), np.concatenate([z0, ep], axis=-1)]
        c = [[np.einsum("...m,...n,...mn->...", fi, fj, E) for fj in basis] for fi in basis]
        tr = 0.5 * (c[0][0] + c[1][1])
        V = [_low(self.pol(fi, q, q0c, perp_q)) for fi in basis]
        out = 0.0
        for i in range(2):
            for j in range(2):
                cij = c[i][j] - (tr if i == j else 0.0)
                out = out + cij[..., None, None] * np.einsum("...m,...n->...mn", V[i], V[j])
        return out


def _gg_to_cm(q1, eps1, q2, eps2, k1, k2, m, e1=None, e2=None):
    """Exact CM kinematics and radiation-gauge wavefunctions for g g -> X X (see _CMFrame)."""
    F = _CMFrame(q1, 0.0, q2, 0.0)
    if np.any(~(F.s > 4 * m * m * (1 + 1e-12))) or np.any(~(F.s > 0)):
        raise ValueError("need s = (q1 + q2)^2 > max(4 m^2, 0): collinear gravitons (s = 0) make nothing")
    E = 0.5 * F.rs
    qa = F.vec(q1, 0.0, F.perp_ab[0])
    na = qa[..., 1:] / np.linalg.norm(qa[..., 1:], axis=-1, keepdims=True)
    kf = F.vec(k1, m)
    n1 = kf[..., 1:] / np.linalg.norm(kf[..., 1:], axis=-1, keepdims=True)
    p = np.sqrt(np.maximum(E * E - m * m, 0.0))
    Ex = E[..., None]
    q1c, q2c = np.concatenate([Ex, Ex * na], axis=-1), np.concatenate([Ex, -Ex * na], axis=-1)
    k1c, k2c = np.concatenate([Ex, p[..., None] * n1], axis=-1), np.concatenate([Ex, -p[..., None] * n1], axis=-1)
    E1c, E2c = F.tensor(eps1, q1, E, F.perp_ab[0]), F.tensor(eps2, q2, E, F.perp_ab[1])
    out = {"F": F, "s": F.s, "q1": q1c, "q2": q2c, "k1": k1c, "k2": k2c, "eps1": E1c, "eps2": E2c}
    if e1 is not None:
        out["e1"], out["e2"] = F.pol(e1, k1, E), F.pol(e2, k2, E)
    # t - m^2 = -2 E (E - p cos) with E - p cos = m^2/(E + p) + p |na - n1|^2/2 (no cancellation); u: n1 -> -n1
    for key, sg in (("t", 1.0), ("u", -1.0)):
        out[key] = m * m - 2 * E * (m * m / (E + p) + 0.5 * p * np.sum((na - sg * n1) ** 2, axis=-1))
    return out


def _check_tu(c, m):
    if m == 0:
        tu = np.minimum(np.abs(c["t"]), np.abs(c["u"]))
        if np.any(tu <= 1e-12 * c["s"]):
            raise ValueError("a final particle exactly collinear with a graviton (t or u = 0): the separate exchange "
                             "channels are singular there (their sum is finite); move off the axis")


# ---------------------------------------------------------------- Part A: amplitudes
def amplitude_gg_to_photons(q1, eps1, q2, eps2, k1, e1, k2, e2, G: float = 1.0, parts: bool = False):
    """Tree amplitude M for g(q1, eps1) g(q2, eps2) -> gamma(k1, e1) gamma(k2, e2) in Einstein-Maxwell, all diagrams.

    Contact (h h A A), t- and u-channel photon exchange and s-channel graviton exchange (the latter via the
    second-order metric of the two waves, see the module notes). Arrays broadcast over leading axes (e.g. a grid
    of final states). eps are LOWER-index graviton tensors of the incoming gravitons; e1, e2 are the PHYSICAL
    polarisation vectors of the outgoing photons (conjugated inside).
    Quantity: the IN-OUT S-matrix element <k1 s1, k2 s2| iT |q1, q2> = i M (2pi)^4 delta^4(...) stripped of i and
        delta: M, dimensionless, kappa^2 = 32 pi G included (O(8 pi G s)); per unit-normalised polarisations;
        with parts=True a dict of 'contact', 's_channel', 'tu_channel' (each gauge DEPENDENT) and 'total'.
    Valid when: tree level, s << 1/G; q1, q2, k1, k2 light-like with positive energy and q1 + q2 = k1 + k2,
        s > 0, |t|, |u| > 1e-12 s, K0^2/s <= 1e24 (refused beyond: untested); any frame (the inputs are carried to the
        CM exactly, see 'Numerics'): relative roundoff ~ 1e-15 for the unsuppressed amplitudes and ~ 1e-16 s/|t|
        for the suppressed (kappa/2)^2 t^2/s one; parts=True is evaluated in the caller's frame and gauge (there it
        loses ~ (K0^2/s)^2 digits when K moves fast); eps symmetric, transverse, traceless; e.k = 0; G > 0."""
    if not G > 0:
        raise ValueError("G must be > 0")
    q1, q2 = _check_null(q1, "q1"), _check_null(q2, "q2")
    k1, k2 = _check_null(k1, "k1"), _check_null(k2, "k2")
    q1, q2, k1, k2 = _check_final(q1, q2, k1, k2, 0.0)
    eps1, eps2 = _check_tt(q1, eps1, "eps1"), _check_tt(q2, eps2, "eps2")
    e1, e2 = np.asarray(e1, dtype=complex), np.asarray(e2, dtype=complex)
    _check_transverse(k1, e1, "e1")
    _check_transverse(k2, e2, "e2")
    c = _gg_to_cm(q1, eps1, q2, eps2, k1, k2, 0.0, e1, e2)
    _check_tu(c, 0.0)
    if parts:   # the gauge-dependent channels exist only for the wavefunctions and frame the caller supplied
        return _parts_out(_core_photon(q1, eps1, q2, eps2, k1, np.conj(e1), k2, np.conj(e2)), 32 * PI * G, True)
    return _parts_out(_core_photon(c["q1"], c["eps1"], c["q2"], c["eps2"], c["k1"], np.conj(c["e1"]), c["k2"],
                                   np.conj(c["e2"])), 32 * PI * G, parts)


def _check_transverse(k, e, name):
    if e.shape[-1] != 4 or not np.all(np.isfinite(e)):
        raise ValueError(f"{name} must be a finite 4-vector")
    if np.max(np.abs(_dot(k, e))) > 1e-9 * np.max(k[..., 0]) * max(np.max(np.abs(e)), 1e-300):
        raise ValueError(f"photon polarisation {name} must be transverse (e.k = 0)")


def amplitude_gg_to_scalars(q1, eps1, q2, eps2, k1, k2, m: float = 0.0, G: float = 1.0, parts: bool = False):
    """Tree amplitude M for g(q1, eps1) g(q2, eps2) -> phi(k1) phi(k2), minimally coupled scalar of mass m, all diagrams.

    Same for a real field (two identical particles) and a complex one (k1 particle, k2 antiparticle); only the
    final-state phase-space factor differs (see sigma_total).
    Quantity: IN-OUT amplitude M (dimensionless, kappa^2 = 32 pi G included), definition as in
        amplitude_gg_to_photons; parts=True gives the gauge-dependent channels and 'total'.
    Valid when: tree level; m >= 0; q1, q2 light-like, k1^2 = k2^2 = m^2, positive energies, q1 + q2 = k1 + k2,
        s > 4 m^2 (for m = 0 also |t|, |u| > 1e-12 s), K0^2/s <= 1e24; any frame (carried to the CM exactly);
        the same-helicity amplitude (~ 8 pi G m^4 s/((t - m^2)(u - m^2))) is a cancellation of O(s) channels:
        relative roundoff ~ 3e-17 s^2/m^4 at generic angles (5e-9 at m^2/s = 1e-4, 0.4 at 1e-8); eps transverse
        and traceless; G > 0."""
    if not G > 0 or not (m >= 0 and math.isfinite(m)):
        raise ValueError("need G > 0 and m >= 0")
    q1, q2 = _check_null(q1, "q1"), _check_null(q2, "q2")
    q1, q2, k1, k2 = _check_final(q1, q2, k1, k2, m)
    eps1, eps2 = _check_tt(q1, eps1, "eps1"), _check_tt(q2, eps2, "eps2")
    c = _gg_to_cm(q1, eps1, q2, eps2, k1, k2, float(m))
    _check_tu(c, float(m))
    if parts:
        return _parts_out(_core_scalar(q1, eps1, q2, eps2, k1, k2, float(m)), 32 * PI * G, True)
    return _parts_out(_core_scalar(c["q1"], c["eps1"], c["q2"], c["eps2"], c["k1"], c["k2"], float(m)), 32 * PI * G, parts)


def _cm_final(s, cth, phi, m):
    E = 0.5 * math.sqrt(s)
    p = math.sqrt(max(E * E - m * m, 0.0))
    sth = np.sqrt(np.clip(1 - cth * cth, 0, None))
    n = np.stack([sth * np.cos(phi), sth * np.sin(phi), cth], axis=-1)
    k1 = np.concatenate([np.full(n.shape[:-1] + (1,), E), p * n], axis=-1)
    k2 = np.concatenate([np.full(n.shape[:-1] + (1,), E), -p * n], axis=-1)
    return k1, k2, p


def _final_wavefunctions(final, k1, k2):
    """List of (label, w1, w2) outgoing-slot wavefunctions for all final helicities (photon) or [None] (scalar)."""
    if final != "photon":
        return [((), None, None)]
    out = []
    for s1 in (1, -1):
        for s2 in (1, -1):
            w1 = np.conj(_pol_array(k1, s1))
            w2 = np.conj(_pol_array(k2, s2))
            out.append(((s1, s2), w1, w2))
    return out


def _pol_array(k, hel):
    """photon_polarization vectorised over leading axes of k (4-vectors)."""
    et, ep = _transverse_basis(np.asarray(k, dtype=float)[..., 1:])
    v = (-hel * et - 1j * ep) / math.sqrt(2.0)
    return np.concatenate([np.zeros(v.shape[:-1] + (1,)), v], axis=-1)


def _check_final_kind(final, m):
    if final not in ("photon", "scalar"):
        raise ValueError("final must be 'photon' or 'scalar'")
    if not (m >= 0 and math.isfinite(m)):
        raise ValueError("m must be >= 0")
    if final == "photon" and m != 0:
        raise ValueError("photons are massless (m must be 0)")


def helicity_amplitudes_cm(s: float, theta: float, phi: float = 0.0, final: str = "photon", m: float = 0.0,
                           G: float = 1.0) -> dict:
    """All helicity amplitudes of g g -> gamma gamma (or phi phi) in the CM frame.

    Graviton 1 along +z, graviton 2 along -z (helicities l1, l2 = +-2 along their own directions); particle 1 at
    polar angle theta, azimuth phi, particle 2 opposite; photon helicities s1, s2 = +-1 along their own directions.
    Quantity: dict {(l1, l2, s1, s2): M} (photons) or {(l1, l2): M} (scalars) of IN-OUT amplitudes M
        (dimensionless, kappa^2 = 32 pi G included), phase conventions of photon_polarization/graviton_polarization.
    Valid when: s > 4 m^2 (energy^2), 0 < theta < pi with |t|, |u| > 1e-12 s for m = 0 (exactly forward/backward is
        refused because the separate photon-exchange channels are singular there although the sum is finite;
        the suppressed t^2/s amplitudes carry relative roundoff ~ 1e-16 s/|t|), m >= 0 (scalar only; same-helicity
        massive amplitudes: roundoff as in amplitude_gg_to_scalars), G > 0."""
    _check_final_kind(final, m)
    if not (s > 4 * m * m and s > 0 and math.isfinite(s)):
        raise ValueError("need finite s > 4 m^2")
    if not (0 < theta < PI):
        raise ValueError("need 0 < theta < pi")
    E = 0.5 * math.sqrt(s)
    q1, q2 = np.array([E, 0, 0, E]), np.array([E, 0, 0, -E])
    k1, k2, _ = _cm_final(s, np.array(math.cos(theta)), np.array(phi), m)
    out = {}
    for l1 in (2, -2):
        for l2 in (2, -2):
            e1, e2 = graviton_polarization(q1, l1), graviton_polarization(q2, l2)
            if final == "photon":
                for s1 in (1, -1):
                    for s2 in (1, -1):
                        out[(l1, l2, s1, s2)] = complex(amplitude_gg_to_photons(
                            q1, e1, q2, e2, k1, photon_polarization(k1, s1), k2, photon_polarization(k2, s2), G))
            else:
                out[(l1, l2)] = complex(amplitude_gg_to_scalars(q1, e1, q2, e2, k1, k2, m, G))
    return out


def compton_amplitude(target: str, p_in, q_in, eps_in, p_out, q_out, eps_out, e_in=None, e_out=None,
                      m: float = 0.0, G: float = 1.0, parts: bool = False):
    """Gravitational Compton amplitude X(p_in) g(q_in, eps_in) -> X(p_out) g(q_out, eps_out), X = photon or scalar.

    Obtained by crossing the g g -> X X amplitude (incoming graviton b <- outgoing graviton with eps_out*, outgoing
    X 2 <- incoming X with momentum -p_in and wavefunction e_in). e_in, e_out: physical photon polarisation vectors.
    Quantity: IN-OUT amplitude M (dimensionless, kappa^2 = 32 pi G), same normalisation as amplitude_gg_to_photons;
        parts=True gives the gauge-dependent channels (here 'contact', 's_channel' = graviton exchange in the
        t-channel of the Compton process, 'tu_channel' = X exchange) and 'total'.
    Valid when: tree level; target 'photon' (m = 0, e_in and e_out given, e_in.p_in = e_out.p_out = 0) or 'scalar'
        (m >= 0); on-shell momenta with positive energies, p_in + q_in = p_out + q_out, |t| > 1e-24 s (t = 0 is the
        graviton pole) and, for m = 0, |u| > 1e-24 s; any frame (carried to the CM of p_in + q_in exactly; measured
        < 2e-15 against Holstein eq. 66 down to theta_lab = 1e-10); eps transverse-traceless; G > 0."""
    if target not in ("photon", "scalar"):
        raise ValueError("target must be 'photon' or 'scalar'")
    if not G > 0 or not (m >= 0 and math.isfinite(m)):
        raise ValueError("need G > 0 and m >= 0")
    p_in, q_in, p_out, q_out = (np.asarray(v, dtype=float) for v in (p_in, q_in, p_out, q_out))
    for v, nm in ((p_in, "p_in"), (q_in, "q_in"), (p_out, "p_out"), (q_out, "q_out")):
        if v.shape[-1] != 4 or not np.all(np.isfinite(v)) or np.any(v[..., 0] <= 0):
            raise ValueError(f"{nm} must be a finite 4-vector with positive energy (physical Compton kinematics)")
    q_in, q_out = _check_null(q_in, "q_in"), _check_null(q_out, "q_out")
    if np.max(np.abs(p_in + q_in - p_out - q_out)) > 1e-9 * np.max(p_in[..., 0] + q_in[..., 0]):
        raise ValueError("momentum not conserved")
    for p, nm in ((p_in, "p_in"), (p_out, "p_out")):
        if np.any(np.abs(_dot(p, p) - m * m) > _ONSHELL_TOL * np.max(p[..., 0] ** 2)):
            raise ValueError(f"{nm} must be on shell")
    eps_in, eps_out = _check_tt(q_in, eps_in, "eps_in"), _check_tt(q_out, eps_out, "eps_out")
    if target == "photon":
        if m != 0 or e_in is None or e_out is None:
            raise ValueError("photon target: m = 0 and both photon polarisations required")
        e_in, e_out = np.asarray(e_in, dtype=complex), np.asarray(e_out, dtype=complex)
        _check_transverse(p_in, e_in, "e_in")
        _check_transverse(p_out, e_out, "e_out")
    if parts:   # the gauge-dependent channels exist only for the wavefunctions and frame the caller supplied
        if target == "photon":
            return _parts_out(_core_photon(q_in, eps_in, -q_out, np.conj(eps_out), p_out, np.conj(e_out), -p_in, e_in),
                              32 * PI * G, True)
        return _parts_out(_core_scalar(q_in, eps_in, -q_out, np.conj(eps_out), p_out, -p_in, float(m)), 32 * PI * G, True)
    _check_boost(p_in, q_in, float(m))
    # exact CM kinematics of p_in + q_in (light-cone transformation, _CMFrame); every vector in its CM radiation gauge
    F = _CMFrame(p_in, float(m), q_in, 0.0)
    rs = F.rs
    kc = (F.s - m * m) / (2 * rs)
    Ep = (F.s + m * m) / (2 * rs)
    def unit(v):
        return v[..., 1:] / np.linalg.norm(v[..., 1:], axis=-1, keepdims=True)
    n_in = unit(F.vec(q_in, 0.0, F.perp_ab[1]))
    n_out = unit(F.vec(q_out, 0.0))
    t = -kc * kc * np.sum((n_in - n_out) ** 2, axis=-1)          # (q_in - q_out)^2 without cancellation
    u = -kc * kc * np.sum((n_in + n_out) ** 2, axis=-1)            # (p_out - q_in)^2 for a massless target
    if np.any(np.abs(t) <= 1e-24 * F.s):
        raise ValueError("zero momentum transfer (exactly forward) is the graviton pole: refused")
    if m == 0 and np.any(np.abs(u) <= 1e-24 * F.s):
        raise ValueError("massless target scattered exactly along the incoming graviton (u = 0): the separate "
                         "exchange channels are singular there; move off the axis")
    kx, Ex = kc[..., None], Ep[..., None]
    qi = np.concatenate([kx, kx * n_in], axis=-1)
    qo = np.concatenate([kx, kx * n_out], axis=-1)
    pi_ = np.concatenate([Ex, -kx * n_in], axis=-1)
    po = np.concatenate([Ex, -kx * n_out], axis=-1)
    Ei, Eo = F.tensor(eps_in, q_in, kc, F.perp_ab[1]), F.tensor(eps_out, q_out, kc)
    if target == "photon":
        ei, eo = F.pol(e_in, p_in, kc, F.perp_ab[0]), F.pol(e_out, p_out, kc)
        core = _core_photon(qi, Ei, -qo, np.conj(Eo), po, np.conj(eo), -pi_, ei)
    else:
        core = _core_scalar(qi, Ei, -qo, np.conj(Eo), po, -pi_, float(m))
    return _parts_out(core, 32 * PI * G, parts)


def compton_scalar_lab_dsigma(omega: float, theta: float, m: float, G: float = 1.0) -> float:
    """Unpolarised laboratory cross section of gravitational Compton scattering off a scalar of mass m at rest.

    dsigma/dOmega = (omega_f/omega)^2 (1/2) sum_{l_i, l_f} |M|^2 / (64 pi^2 m^2), omega_f = omega/(1 + (2 omega/m) sin^2(theta/2)).
    Quantity: dsigma/dOmega per solid angle of the outgoing graviton, averaged over the 2 initial graviton helicities,
        summed over the final ones (1/energy^2).
    Valid when: tree level; m > 0, omega > 0 (energy), 0 < theta <= pi; G > 0."""
    if not (m > 0 and omega > 0 and 0 < theta <= PI and G > 0):
        raise ValueError("need m > 0, omega > 0, 0 < theta <= pi, G > 0")
    wf = omega / (1 + 2 * omega / m * math.sin(theta / 2) ** 2)
    pin = np.array([m, 0, 0, 0.0])
    qin = np.array([omega, 0, 0, omega])
    qout = wf * np.array([1.0, math.sin(theta), 0, math.cos(theta)])
    pout = pin + qin - qout
    tot = 0.0
    for li in (2, -2):
        for lf in (2, -2):
            M = compton_amplitude("scalar", pin, qin, graviton_polarization(qin, li), pout, qout,
                                  graviton_polarization(qout, lf), m=m, G=G)
            tot += abs(complex(M)) ** 2
    return 0.5 * tot * (wf / omega) ** 2 / (64 * PI * PI * m * m)


# ---------------------------------------------------------------- cross sections (CM)
def _pol_label(p):
    key = {2: "R", -2: "L"}.get(p, p) if not isinstance(p, str) else p
    if key not in _POLS:
        raise ValueError("polarisation must be 'R' (+2), 'L' (-2), 'plus' or 'cross'")
    return key


def _sym(final, field):
    if field not in ("real", "complex"):
        raise ValueError("field must be 'real' or 'complex'")
    return 0.5 if (final == "photon" or field == "real") else 1.0


_MIN_M2_OVER_S = 1e-8   # massive-scalar phase space refused below (same-helicity roundoff ~1e-14 s/m^2 = 1e-6 there)


def _polar_rule(final, m, s, order):
    """Nodes and weights in cos(theta) on [-1, 1] for the CM polar integral.

    Massless final states: one Gauss-Legendre rule of the given order (exact: the integrands are polynomials of degree
    <= 8). Massive scalars: the propagators 1/(t - m^2), 1/(u - m^2) peak within 1 - |cos| ~ delta = 1 - beta ~ 2 m^2/s
    of the axis (the same-helicity amplitude is ~ m^4 s/((t - m^2)(u - m^2)) and nothing else), so a single Gauss rule
    misses them for light scalars; here composite Gauss panels in x = 1 - |cos| are graded geometrically (ratio 2)
    from 1 down to 1e-3 delta, plus [0, 1e-3 delta], on both sides. On each panel [a, 2a] the integrand's nearest
    singularity (x = -delta) is >= 3 half-widths away, so the error falls like 5.8^(-2 order)."""
    c, w = np.polynomial.legendre.leggauss(order)
    if final == "photon" or m == 0:
        return c, w
    beta = math.sqrt(max(1.0 - 4 * m * m / s, 0.0))
    delta = 4 * m * m / (s * (1 + beta))                       # = 1 - beta without cancellation
    edges = [1.0]
    while edges[-1] > 1e-3 * delta and len(edges) < 200:
        edges.append(edges[-1] / 2)
    edges.append(0.0)
    xs, ws = [], []
    for a, b in zip(edges[1:], edges[:-1]):
        xs.append(0.5 * (b - a) * c + 0.5 * (b + a))
        ws.append(0.5 * (b - a) * w)
    x, wx = np.concatenate(xs), np.concatenate(ws)
    return np.concatenate([1 - x, x - 1]), np.concatenate([wx, wx])


def _phase_space_sum(qa, Ea, qb, Eb, final, m, n_theta, n_phi):
    """W = int dPhi2 sum_final |M|^2 (kappa = 1, no identical-particle factor) by quadrature in the CM.

    The waves are carried to the CM of K = qa + qb by _CMFrame (light-cone form: no cancellation in s, in the boost or
    in the polarisations, which arrive in the CM radiation gauge). Polar rule: _polar_rule; for massive scalars the
    integral is repeated with panel order + 4 and a relative change > 1e-8 raises ValueError (convergence guard)."""
    F = _CMFrame(qa, 0.0, qb, 0.0)
    s = float(F.s)
    M_ = math.sqrt(s)
    E = 0.5 * M_
    d = F.vec(qa, 0.0, F.perp_ab[0])[1:]
    d = d / np.linalg.norm(d)
    Ea_c, Eb_c = F.tensor(Ea, qa, E, F.perp_ab[0]), F.tensor(Eb, qb, E, F.perp_ab[1])
    # rotate so that graviton a moves along +z in the CM: the quadrature axis is then the collision axis, where the
    # interference of the J_z = +4 and -4 channels (linear polarisations) is non-smooth but integrates to zero exactly
    # under the uniform azimuthal rule; elsewhere the integrand is smooth (polynomial for massless final states).
    e1 = np.cross(d, [0.0, 1.0, 0.0] if abs(d[1]) < 0.9 else [1.0, 0.0, 0.0])
    e1 /= np.linalg.norm(e1)
    R4 = np.eye(4)
    R4[1:, 1:] = np.array([e1, np.cross(d, e1), d])
    Ea_c, Eb_c = R4 @ Ea_c @ R4.T, R4 @ Eb_c @ R4.T
    qa_c, qb_c = np.array([E, 0.0, 0.0, E]), np.array([E, 0.0, 0.0, -E])
    ph = (np.arange(n_phi) + 0.5) * 2 * PI / n_phi

    def integrate(order):
        c, wc = _polar_rule(final, m, s, order)
        C_, P_ = np.meshgrid(c, ph, indexing="ij")
        k1, k2, p = _cm_final(s, C_, P_, m)
        tot = np.zeros(C_.shape)
        for _, w1, w2 in _final_wavefunctions(final, k1, k2):
            if final == "photon":
                parts = _core_photon(qa_c, Ea_c, qb_c, Eb_c, k1, w1, k2, w2)
            else:
                parts = _core_scalar(qa_c, Ea_c, qb_c, Eb_c, k1, k2, m)
            tot += np.abs(sum(parts)) ** 2
        return float(np.einsum("i,ij->", wc, tot)) * (2 * PI / n_phi) * p / (16 * PI * PI * M_)

    if final == "photon" or m == 0:
        return integrate(n_theta), s
    if m * m < _MIN_M2_OVER_S * s:
        raise ValueError(f"m^2/s = {m * m / s:.1e} < {_MIN_M2_OVER_S:.0e}: the same-helicity amplitude ~ m^4/s is a "
                         "cancellation of channels ~ s (relative roundoff ~ 1e-14 s/m^2); use m = 0 (opposite-helicity "
                         "and linear-polarisation results then change by ~ 20 m^2/s < 2e-7) and "
                         "sigma_same_helicity_scalar_closed_form for the same-helicity piece")
    order = max(8, n_theta // 3)
    W, W2 = integrate(order), integrate(order + 4)
    # 1e-7: above the roundoff floor (~1e-14 s/m^2 <= 1e-6, measured) only where quadrature, not roundoff, dominates;
    # measured panel-order differences are <= 2e-8 down to m^2/s = 1e-8 at the default order 8.
    if abs(W2 - W) > 1e-7 * abs(W2) + 1e-300:
        raise ValueError(f"massive-scalar phase-space quadrature not converged (relative change {abs(W2 / W - 1):.1e} "
                         "between panel orders): raise n_theta")
    return W2, s


def dsigma_domega_cm(s: float, theta: float, pol1="R", pol2="L", final: str = "photon", m: float = 0.0,
                     G: float = 1.0, phi: float = 0.0) -> float:
    """CM differential cross section of g g -> gamma gamma (phi phi) for given incoming polarisations.

    Graviton 1 along +z, graviton 2 along -z, pol1/pol2 defined w.r.t. each graviton's own direction
    (graviton_polarization); particle 1 at (theta, phi). dsigma/dOmega = (|p*|/(sqrt(s)/2)) sum_final |M|^2/(64 pi^2 s).
    Quantity: dsigma/dOmega per solid angle of PARTICLE 1 (1/energy^2), summed over final helicities, for the given
        initial polarisation states; no identical-particle factor (integrating over 4 pi counts each pair twice
        for photons or a real scalar: use sigma_total).
    Valid when: tree level; s > 4 m^2, 0 < theta < pi; final 'photon' (m = 0) or 'scalar' (m >= 0); G > 0."""
    _check_final_kind(final, m)
    if not (s > 4 * m * m and s > 0 and 0 < theta < PI and G > 0):
        raise ValueError("need s > 4 m^2, 0 < theta < pi, G > 0")
    E = 0.5 * math.sqrt(s)
    q1, q2 = np.array([E, 0, 0, E]), np.array([E, 0, 0, -E])
    Ea, Eb = graviton_polarization(q1, _pol_label(pol1)), graviton_polarization(q2, _pol_label(pol2))
    k1, k2, p = _cm_final(s, np.array(math.cos(theta)), np.array(phi), m)
    tot = 0.0
    for _, w1, w2 in _final_wavefunctions(final, k1, k2):
        parts = _core_photon(q1, Ea, q2, Eb, k1, w1, k2, w2) if final == "photon" else _core_scalar(q1, Ea, q2, Eb, k1, k2, m)
        tot += abs(complex(sum(parts))) ** 2
    return (32 * PI * G) ** 2 * tot * (p / E) / (64 * PI * PI * s)


def sigma_total(s: float, pol1="R", pol2="L", final: str = "photon", m: float = 0.0, G: float = 1.0,
                field: str = "real", n_theta: int = 24, n_phi: int = 24) -> float:
    """Total cross section of g g -> gamma gamma (phi phi) at CM energy^2 s for given incoming polarisation states.

    sigma = sym/(2 s) int dPhi2 sum_final |M|^2, flux 2s (massless initial state), sym = 1/2 for identical final
    particles (photons, real scalar), 1 for a complex scalar (particle + antiparticle). Massless final states:
    Gauss-Legendre (n_theta) x uniform (n_phi) quadrature in the CM, exact for the polynomial integrands (degree <= 8
    in cos and e^{+-8 i phi}). Massive scalars: composite Gauss panels graded geometrically towards cos = +-1 on the
    scale 1 - beta ~ 2 m^2/s (order max(8, n_theta // 3) per panel; _polar_rule), repeated at order + 4 with a
    ValueError above 1e-7 relative change (measured against sigma_same_helicity_scalar_closed_form: <= 1.1e-9 for
    m^2/s >= 4e-6, 1e-6 at m^2/s = 1e-8).
    Quantity: sigma (1/energy^2) for the given initial polarisations (pol1 of graviton 1 along +z, pol2 of graviton 2
        along -z; 'R', 'L', 'plus', 'cross'), summed over final helicities, counting PAIRS (each pair once).
    Valid when: tree level; s > 4 m^2; final 'photon' (m = 0) or 'scalar' (m = 0 or m^2/s >= 1e-8: below that the
        same-helicity amplitude is roundoff-limited and the call is refused; use m = 0 plus
        sigma_same_helicity_scalar_closed_form); G > 0; n_theta >= 8, n_phi >= 17."""
    _check_final_kind(final, m)
    if not (s > 4 * m * m and s > 0 and math.isfinite(s) and G > 0):
        raise ValueError("need finite s > 4 m^2 and G > 0")
    if n_theta < 8 or n_phi < 17:
        raise ValueError("need n_theta >= 8 and n_phi >= 17")
    sym = _sym(final, field)
    E = 0.5 * math.sqrt(s)
    q1, q2 = np.array([E, 0, 0, E]), np.array([E, 0, 0, -E])
    Ea, Eb = graviton_polarization(q1, _pol_label(pol1)), graviton_polarization(q2, _pol_label(pol2))
    W, _ = _phase_space_sum(q1, Ea, q2, Eb, final, m, n_theta, n_phi)
    return sym * (32 * PI * G) ** 2 * W / (2 * s)


def sigma_total_massless_closed_form(s: float, pol1="R", pol2="L", final: str = "photon", G: float = 1.0,
                                     field: str = "real") -> float:
    """Closed-form total cross section for MASSLESS final states (helicity selection rule + |M| = (kappa/2)^2 x^2/s).

    Opposite helicities: sigma(gamma gamma) = (4/5) pi G^2 s; sigma(phi phi) = pi G^2 s/15 (real, identical) or
    2 pi G^2 s/15 (complex). Same helicities: 0. A linear polarisation is an equal-weight superposition of +-2 and the
    two opposite-helicity channels do not interfere in sigma (their J_z = +-4 differ), so any linear x any state
    gives half the opposite-helicity value. (From the crossed helicity amplitudes of Bjerrum-Bohr et al. 2016,
    eqs. A.10-A.13, normalised by the forward one-graviton-exchange limit; see source notes in the self-test.)
    Quantity: sigma (1/energy^2) for the given incoming polarisations, summed over final helicities, counting pairs.
    Valid when: tree level; massless final particles; s > 0; G > 0."""
    if final not in ("photon", "scalar"):
        raise ValueError("final must be 'photon' or 'scalar'")
    if not (s > 0 and G > 0):
        raise ValueError("need s > 0 and G > 0")
    sym = _sym(final, field)
    base = (8.0 / 5.0) * PI * G * G * s if final == "photon" else (2.0 / 15.0) * PI * G * G * s
    w = {"R": (1.0, 0.0), "L": (0.0, 1.0), "plus": (0.5, 0.5), "cross": (0.5, 0.5)}
    a, b = w[_pol_label(pol1)], w[_pol_label(pol2)]
    return sym * base * (a[0] * b[1] + a[1] * b[0])


def sigma_same_helicity_scalar_closed_form(s: float, m: float, G: float = 1.0, field: str = "real") -> float:
    """Closed-form total cross section of g g -> phi phi for SAME-helicity gravitons (R/R or L/L), massive scalar.

    The same-helicity amplitude is |M| = 8 pi G m^4 s/|(t - m^2)(u - m^2)| (the crossing of Bjerrum-Bohr, Donoghue &
    Vanhove 2014 eq. II.27 with its normalisation halved, see self-test 8). With t - m^2 = -(s/2)(1 - beta c),
    u - m^2 = -(s/2)(1 + beta c), beta = sqrt(1 - 4 m^2/s), sigma = sym/(2s) int dPhi2 |M|^2 integrates to
        sigma = sym 32 pi G^2 m^8 beta/s^3 [1/(1 - beta^2) + ln((1 + beta)/(1 - beta))/(2 beta)]
    (= 16 pi G^2 m^8 beta/s^3 [...] for a real scalar; sym = 1/2 real, 1 complex). For m^2 << s this is
    ~ sym 8 pi G^2 m^6/s^2: tiny, peaked within 1 - |cos theta| ~ 2 m^2/s of the collision axis.
    Quantity: sigma (1/energy^2) for incoming helicities (+2, +2) or (-2, -2), counting pairs.
    Valid when: tree level; 0 < m, s > 4 m^2 (energy^2); G > 0; any m^2/s (no cancellation in this form)."""
    if not (m > 0 and s > 4 * m * m and math.isfinite(s) and G > 0):
        raise ValueError("need m > 0, finite s > 4 m^2, G > 0")
    sym = _sym("scalar", field)
    x = 4 * m * m / s
    beta = math.sqrt(1 - x)
    one_m_b = x / (1 + beta)                                    # 1 - beta without cancellation
    return 2 * sym * 16 * PI * G * G * m ** 8 * beta / s ** 3 * (1 / x + (math.log1p(2 * beta / one_m_b) if beta > 0
                                                                        else 0.0) / (2 * beta if beta > 0 else 1.0))


# ---------------------------------------------------------------- Part A': the second-order metric
def second_order_metric(q1, H1, q2, H2) -> dict:
    """Second-order metric and Einstein tensor of two gravitational plane waves delta g = H1 e^{-iq1 x} + H2 e^{-iq2 x}.

    G[eta + dg1 + dg2] at second order: the cross term G2_{mn} e^{-iKx}, K = q1 + q2 (the e^{-2iq x} self-terms and
    terms with the complex conjugate waves are not returned). dg2 solves G^(1)[dg2] = -G2 in de Donder gauge.
    Quantity: dict with 'G2' (coefficient of e^{-iKx} in the second-order Einstein tensor, lower indices, energy^2),
        'dg2' (coefficient of e^{-iKx} in the second-order metric, lower, dimensionless, de Donder gauge; this is the
        h~ that qft_production's gravity vertex -(1/2) h T sees), 'K', 's' = K^2 and 'conservation' =
        max |K^m G2_mn| / max |G2| (Bianchi identity: roundoff for on-shell waves).
    Valid when: |H| << 1; q1, q2 light-like, H transverse-traceless (or gauge-shifted TT); s = K^2 != 0."""
    q1, q2 = _check_null(q1, "q1"), _check_null(q2, "q2")
    H1, H2 = _check_tt(q1, H1, "H1"), _check_tt(q2, H2, "H2")
    K = q1 + q2
    s = float(_dot(K, K)) if K.ndim == 1 else _dot(K, K)
    if np.any(np.abs(s) <= 1e-12 * np.max(K[..., 0] ** 2)):
        raise ValueError("collinear waves (K^2 = 0): the second-order source sits on the light cone")
    G2 = _einstein2(H1, q1, H2, q2)
    cons = float(np.max(np.abs(np.einsum("...m,...mn->...n", K, G2))) / max(np.max(np.abs(G2)), 1e-300)
                 / max(np.max(np.abs(K)), 1e-300))
    return {"G2": G2, "dg2": _solve_linear(-G2, K), "K": K, "s": s, "conservation": cons}


# ---------------------------------------------------------------- Part B: classical waves and beams
def gw_plane_wave(omega: float, h: float, direction, pol="plus", G: float = 1.0) -> dict:
    """A monochromatic gravitational plane wave as a coherent state: momentum, strain tensor, densities.

    GR strain amplitude h: 'plus': h_xx = -h_yy = h cos(w t - q.x) (H = (h/sqrt2) eps_plus); 'cross' likewise;
    'R'/'L': h_+ = h cos, h_x = +-h sin (H = h eps_{+-2}). delta g_{mn} = H e^{-iqx} + c.c.
    Quantity: dict with 'q' (4-momentum, energy), 'H' (strain tensor, lower, dimensionless), 'eps' (unit polarisation),
        'amp' = |H| (h/sqrt2 linear, h circular),
        'A' = |H|/kappa (canonical coherent amplitude, energy), 'rho' = w^2 |H|^2/(16 pi G) (energy density, energy^4;
        = w^2 h^2/(32 pi G) for linear polarisation), 'n' = rho/w (graviton number density, energy^3).
    Valid when: 0 < h < 0.1 (linear wave, perturbative), omega > 0 (energy), direction nonzero, G > 0."""
    if not (omega > 0 and math.isfinite(omega)):
        raise ValueError("omega must be > 0")
    if not (0 < h < 0.1):
        raise ValueError("need 0 < h < 0.1 (weak, perturbative wave)")
    if not G > 0:
        raise ValueError("G must be > 0")
    d = np.asarray(direction, dtype=float)
    if d.shape != (3,) or not np.linalg.norm(d) > 0:
        raise ValueError("direction must be a nonzero 3-vector")
    d = d / np.linalg.norm(d)
    q = np.concatenate([[omega], omega * d])
    key = _pol_label(pol)
    eps = graviton_polarization(q, key)
    amp = h / math.sqrt(2.0) if key in ("plus", "cross") else h
    rho = omega * omega * amp * amp / (16 * PI * G)
    return {"q": q, "eps": eps, "H": amp * eps, "amp": amp, "A": amp / math.sqrt(32 * PI * G), "rho": rho,
            "n": rho / omega, "pol": key, "h": h}


def _beams(omega1, h1, omega2, h2, theta, pol1, pol2, G):
    if not (0 < theta <= PI):
        raise ValueError("need 0 < theta <= pi (theta = angle between the propagation directions)")
    wa = gw_plane_wave(omega1, h1, [0.0, 0.0, 1.0], pol1, G)
    wb = gw_plane_wave(omega2, h2, [math.sin(theta), 0.0, math.cos(theta)], pol2, G)
    return wa, wb


def beams_pair_rate(omega1: float, h1: float, omega2: float, h2: float, theta: float, pol1="plus", pol2="plus",
                    final: str = "photon", m: float = 0.0, G: float = 1.0, field: str = "real",
                    n_theta: int = 24, n_phi: int = 24) -> dict:
    """Pairs made per unit volume per unit time where two monochromatic gravitational plane waves cross at angle theta.

    Wave 1 along +z, wave 2 in the x-z plane at angle theta (head-on: theta = pi); polarisations per gw_plane_wave
    ('plus' axes: in the x-z plane and along y). Gamma = sym int dPhi2 sum_final |M(H1, H2)|^2 (kappa = 1), computed in
    the CM frame of K = q1 + q2 by boosting the waves' momenta and polarisation tensors; equal to
    sigma(s) n1 n2 (1 - cos theta), s = 2 w1 w2 (1 - cos theta) = 4 w1 w2 sin^2(theta/2).
    Quantity: dict with 'pair_rate' (in-in mean number of PAIRS per unit volume per unit time, energy^4; leading
        order, ~ h1^2 h2^2), 'particle_rate' (= 2 x pairs: photons or scalars per volume per time), 'sigma'
        (cross section for these polarisation states, 1/energy^2), 'n1', 'n2' (graviton number densities, energy^3),
        'rho1', 'rho2' (energy densities, energy^4), 's' (energy^2), 'flux_factor' = 1 - cos theta.
    Valid when: tree level, |h| < 0.1, s << 1/G; infinite plane waves (a finite overlap region needs packets much
        longer than 1/omega: then multiply by the overlap volume x time, not validated here); s > 4 m^2; vacuum;
        any frequency ratio and angle with K0^2/s <= 1e24 (refused beyond; tested to w2/w1 = 1e-20, theta = 1e-13:
        the waves are carried to the CM exactly, s and 1 - cos theta = 2 sin^2(theta/2) taken in closed form);
        massive scalars need m^2/s >= 1e-8 (see sigma_total; the same-helicity rate is the m^4 piece, integrated on
        panels graded towards the collision axis). Same-helicity circular waves give exactly zero for massless pairs;
        the quadrature then returns roundoff (about 1e-30 of the opposite-helicity rate)."""
    _check_final_kind(final, m)
    if n_theta < 8 or n_phi < 17:
        raise ValueError("need n_theta >= 8 and n_phi >= 17")
    sym = _sym(final, field)
    wa, wb = _beams(omega1, h1, omega2, h2, theta, pol1, pol2, G)
    flux = 2.0 * math.sin(theta / 2) ** 2                       # 1 - cos(theta) without cancellation
    s = 2.0 * omega1 * omega2 * flux
    if not s > 4 * m * m:
        raise ValueError(f"below threshold: s = {s:.4g} <= 4 m^2")
    _check_boost(wa["q"] / omega1, wb["q"] / omega1)
    # unit polarisations and momenta in units of omega1 (W ~ energy^4, |M|^2 bilinear in |H1|^2 |H2|^2): no underflow
    W, _ = _phase_space_sum(wa["q"] / omega1, wa["eps"], wb["q"] / omega1, wb["eps"], final, m / omega1, n_theta, n_phi)
    rate = sym * W * omega1 ** 4 * (wa["amp"] * wb["amp"]) ** 2
    sigma = rate / (wa["n"] * wb["n"] * flux)
    return {"pair_rate": rate, "particle_rate": 2 * rate, "sigma": sigma, "n1": wa["n"], "n2": wb["n"],
            "rho1": wa["rho"], "rho2": wb["rho"], "s": s, "flux_factor": flux}


def beams_pair_rate_SI(omega1_rad_s: float, h1: float, theta: float, omega2_rad_s: float = None, h2: float = None,
                       pol1="plus", pol2="plus", final: str = "photon", m_eV: float = 0.0, field: str = "real") -> dict:
    """beams_pair_rate in SI: angular frequencies in rad/s, strains dimensionless, theta in radians.

    Natural units with energies in eV (hbar w/e), G = 1/M_Pl^2 in eV^-2 (newton_G_natural); converted back with
    qft_production's rate_density_to_SI and density_to_SI.
    Quantity: dict with 'pair_rate_SI' (mean photon (or scalar) PAIRS per m^3 per s), 'particle_rate_SI' (= 2 x),
        'sigma_m2' (cross section, m^2), 'n1_SI', 'n2_SI' (gravitons per m^3), 'rho1_SI', 'rho2_SI' (J/m^3),
        and the natural-unit dict under 'natural' (eV units).
    Valid when: as beams_pair_rate; omega > 0 (rad/s), 0 < h < 0.1, 0 < theta <= pi; m_eV >= 0 (scalars)."""
    omega2_rad_s = omega1_rad_s if omega2_rad_s is None else omega2_rad_s
    h2 = h1 if h2 is None else h2
    if not (omega1_rad_s > 0 and omega2_rad_s > 0):
        raise ValueError("angular frequencies must be > 0")
    w1, w2 = HBAR * omega1_rad_s / E_CHARGE, HBAR * omega2_rad_s / E_CHARGE
    G = newton_G_natural(1.0)
    r = beams_pair_rate(w1, h1, w2, h2, theta, pol1, pol2, final, m_eV, G, field)
    J_per_eV4 = E_CHARGE * (E_CHARGE / (HBAR * C)) ** 3
    return {"pair_rate_SI": qp.rate_density_to_SI(r["pair_rate"]), "particle_rate_SI": qp.rate_density_to_SI(r["particle_rate"]),
            "sigma_m2": area_to_SI(r["sigma"]), "n1_SI": qp.density_to_SI(r["n1"]), "n2_SI": qp.density_to_SI(r["n2"]),
            "rho1_SI": r["rho1"] * J_per_eV4, "rho2_SI": r["rho2"] * J_per_eV4, "natural": r}


def _beams_rate_lab(wa, wb, final, n_c=96, n_phi=48):
    """Independent route: lab-frame 2-body phase space about K, dPhi2 = E1 dOmega1/(16 pi^2 (K0 - |K| cos a)) (massless)."""
    K = wa["q"] + wb["q"]
    s = float(_dot(K, K))
    kv = K[1:]
    kn = float(np.linalg.norm(kv))
    z = kv / kn if kn > 1e-12 * K[0] else np.array([0.0, 0.0, 1.0])
    kn = kn if kn > 1e-12 * K[0] else 0.0
    xax = np.cross(z, [0.0, 1.0, 0.0])
    if np.linalg.norm(xax) < 1e-8:
        xax = np.cross(z, [1.0, 0.0, 0.0])
    xax /= np.linalg.norm(xax)
    yax = np.cross(z, xax)
    c, wc = np.polynomial.legendre.leggauss(n_c)
    ph = (np.arange(n_phi) + 0.5) * 2 * PI / n_phi
    C_, P_ = np.meshgrid(c, ph, indexing="ij")
    S_ = np.sqrt(1 - C_ * C_)
    n = (C_[..., None] * z + (S_ * np.cos(P_))[..., None] * xax + (S_ * np.sin(P_))[..., None] * yax)
    E1 = s / (2 * (K[0] - kn * C_))
    k1 = np.concatenate([E1[..., None], E1[..., None] * n], axis=-1)
    k2 = K - k1
    tot = np.zeros(C_.shape)
    for _, w1, w2 in _final_wavefunctions(final, k1, k2):
        parts = (_core_photon(wa["q"], wa["H"], wb["q"], wb["H"], k1, w1, k2, w2) if final == "photon"
                 else _core_scalar(wa["q"], wa["H"], wb["q"], wb["H"], k1, k2, 0.0))
        tot += np.abs(sum(parts)) ** 2
    jac = E1 / (16 * PI * PI * (K[0] - kn * C_))
    return 0.5 * float(np.einsum("i,ij->", wc, tot * jac)) * (2 * PI / n_phi)


def _span_residual(M_list, T_list):
    """Relative least-squares residual of fitting amplitudes M_i by h_{mn} T^{mn}_i (10 real-linear unknowns, complex h)."""
    idx = [(a, b) for a in range(4) for b in range(a, 4)]
    A = np.array([[T[a, b] * (1 if a == b else 2) for (a, b) in idx] for T in T_list])
    y = np.array(M_list)
    sol, *_ = np.linalg.lstsq(A, y, rcond=None)
    return float(np.linalg.norm(A @ sol - y) / np.linalg.norm(y))


def _photon_T(k1, w1, k2, w2):
    """<k1 k2| T^{mn} |0> (upper) for photons with outgoing-slot wavefunctions (qp's sign conventions)."""
    f1l, f2l = _fout(k1, w1), _fout(k2, w2)
    f1u, f2u = _up2(f1l), _up2(f2l)
    return -(f1u @ _ETA @ f2u.T + f2u @ _ETA @ f1u.T) + 0.5 * np.linalg.inv(_ETA) * np.sum(f1l * f2u)


# ---------------------------------------------------------------- self-test
def selftest(verbose: bool = True) -> bool:
    """Compare with exact identities, published amplitudes and cross sections, and qft_production. True if all pass."""
    results = []

    def check(name, got, want, tol, rel=False):
        err = abs(got - want) / (abs(want) if rel and want != 0 else 1.0)
        ok = bool(err <= tol)
        results.append(ok)
        if verbose:
            print(f"{'PASS' if ok else 'FAIL'}  {name}: {got:.10g} (expected {want:.10g}, {'rel' if rel else 'abs'} tol {tol:g})")

    rng = np.random.default_rng(7)
    kap2 = 32 * PI      # G = 1 throughout the self-test

    # 1. Exact definition: the O(H) and cross O(H^2) coefficients of sqrt(-g) g^{ma} g^{nb}, sqrt(-g) g^{mn} and sqrt(-g)
    #    against det/inv of eta + a A + b B (random symmetric A, B with O(1) entries) by symmetric differences with
    #    Richardson extrapolation. Tolerance 1e-6 (coefficients are O(30)): measured truncation without Richardson
    #    2.4e-3 d^2/1e-6 (d^2 law), after it O(d^4) ~ 1e-8; roundoff 1e-16 x 30/d^2 ~ 1e-8 at d = 5e-4.
    Ar, Br = rng.normal(size=(4, 4)), rng.normal(size=(4, 4))
    Ar, Br = Ar + Ar.T, Br + Br.T

    def exact(a, b):
        g = _ETA + a * Ar + b * Br
        gi = np.linalg.inv(g)
        sq = math.sqrt(-np.linalg.det(g))
        return sq * np.einsum("ma,nb->manb", gi, gi), sq * gi, sq
    def cross_fd(d):
        ex = [exact(a, b) for a, b in ((d, d), (d, -d), (-d, d), (-d, -d))]
        return [(ex[0][i] - ex[1][i] - ex[2][i] + ex[3][i]) / (4 * d * d) for i in range(3)]

    def first_fd(d):
        return [(exact(d, 0)[i] - exact(-d, 0)[i]) / (2 * d) for i in range(3)]
    d = 1e-3                                       # Richardson: (4 f(d/2) - f(d))/3 removes the O(d^2) truncation
    num = [(4 * a - b) / 3 for a, b in zip(cross_fd(d / 2), cross_fd(d))]
    e1 = [(4 * a - b) / 3 for a, b in zip(first_fd(d / 2), first_fd(d))]
    S2n, c2n = _dS2(Ar, Br)
    err2 = max(np.max(np.abs(num[0] - _dG2(Ar, Br))), np.max(np.abs(num[1] - S2n)), abs(num[2] - c2n))
    S1n, c1n = _dS1(Ar)
    err1 = max(np.max(np.abs(e1[0] - _dG1(Ar))), np.max(np.abs(e1[1] - S1n)), abs(e1[2] - c1n))
    check("metric expansion: O(h) and cross O(h^2) coefficients vs det/inv finite differences (max abs error)",
          max(err1, err2), 0.0, 1e-6)

    # 2. Isaacson effective stress tensor (Flanagan & Hughes 2005, arXiv:gr-qc/0501041, eqs. 5.35, 5.39-5.40; G = 1):
    #    "where the eﬀective GW stress-energy tensor is T GW, eﬀ ab = − 1 8π ⟨G(2) ab [hcd;gB ef ]⟩. (5.35)"
    #    "for the plane wave propagating in the z direction in ﬂat spacetime, given by hxx = −hyy =h0 cos(ωt −ωz),
    #    hab = 0 (all other components) , (5.39) the energy density and energy ﬂux are given by T tt =T tz = h2 0ω2 16π
    #    ⟨cos2(ωt −ωz)⟩= h2 0ω2 32π . (5.40)" (ACCESS: full-text). The average of G^(2) over a wavelength is the cross
    #    term of the e^{-iqx} wave with its conjugate: -G2/(8 pi) must give T_tt = T_tz = T_zz = h0^2 w^2/(32 pi).
    h0, w0 = 1.0, 1.7
    qz = np.array([w0, 0, 0, w0])
    Hp = (h0 / 2) * math.sqrt(2.0) * graviton_polarization(qz, "plus")      # h_xx = -h_yy = h0 cos = (h0/2)(e^{-i..} + c.c.)
    Tgw = -_einstein2(Hp, qz, np.conj(Hp), -qz).real / (8 * PI)
    want = h0 * h0 * w0 * w0 / (32 * PI)
    check("Isaacson: -<G^(2)>_tt/(8 pi) for h_xx = -h_yy = h0 cos(wt - wz) vs h0^2 w^2/(32 pi) [F&H eq. 5.40]",
          Tgw[0, 0], want, 1e-12, rel=True)
    check("Isaacson: T_tz and T_zz equal T_tt, all other components zero (max deviation / T_tt)",
          max(abs(Tgw[0, 3] + want), abs(Tgw[3, 3] - want), np.max(np.abs(np.delete(Tgw.ravel(), [0, 3, 12, 15])))) / want,
          0.0, 1e-12)
    #    ...and in a random direction with circular polarisation: <G2>_mn = -(1/2)|H|^2 q_m q_n (same law, 5.38).
    nd = rng.normal(size=3)
    qr = np.concatenate([[1.3], 1.3 * nd / np.linalg.norm(nd)])
    Hr = 0.7 * graviton_polarization(qr, "L")
    G2r = _einstein2(Hr, qr, np.conj(Hr), -qr)
    check("Isaacson in a random direction (helicity -2): max |<G2>_mn + |H|^2 q_m q_n/2| / (|H|^2 q0^2)",
          float(np.max(np.abs(G2r + 0.5 * 0.49 * np.outer(_low(qr), _low(qr))))) / (0.49 * 1.69), 0.0, 1e-12)

    # 3. Exact identity: contracted Bianchi identity K^m G2_mn = 0 for on-shell waves (also gauge-shifted ones).
    q1 = np.array([1.3, 0, 0, 1.3])
    nb = np.array([math.sin(2.2), 0.0, math.cos(2.2)])
    q2 = np.concatenate([[0.8], 0.8 * nb])
    xi = rng.normal(size=4) + 1j * rng.normal(size=4)
    xi = xi - _dot(q1, xi) / q1[0] * np.array([1.0, 0, 0, 0])
    sh = np.outer(_low(q1), _low(xi)) + np.outer(_low(xi), _low(q1))
    som = second_order_metric(q1, graviton_polarization(q1, "R") + sh, q2, graviton_polarization(q2, "plus"))
    check("Bianchi identity of the second-order Einstein tensor (gauge-shifted wave 1): |K.G2|/(|K||G2|)",
          som["conservation"], 0.0, 1e-14)

    # 4. Newtonian limit of the linear solve: a static mass m (T_00 = m delta^3) gives g_00 = 1 + 2 Phi, Phi = -G m/r,
    #    i.e. delta g_00(k) = -8 pi G m/k^2 (Poisson). Source G^(1)[dg] = 8 pi G T (G = 1, m = 1, k = 0.9).
    Tst = np.zeros((4, 4))
    Tst[0, 0] = 1.0
    Kst = np.array([0.0, 0.0, 0.0, 0.9])
    dg = _solve_linear(8 * PI * Tst, Kst)
    check("Newton: de Donder solve of G^(1)[dg] = 8 pi G T for a static point mass, dg_00 vs -8 pi G m/k^2",
          dg[0, 0], -8 * PI / 0.81, 1e-12, rel=True)
    check("Newton: dg_ij = dg_00 delta_ij (isotropic gauge, light bends twice the Newtonian amount)",
          float(np.max(np.abs(dg[1:, 1:] - dg[0, 0] * np.eye(3)))), 0.0, 1e-12)

    # 5. Ward identities (exact): graviton shifts eps -> eps + q xi + xi q (q.xi = 0) change the SUM by roundoff
    #    only, each channel by O(|M|). Photon final state, generic non-CM kinematics; tolerance 1e-12 relative to
    #    the channel size (amplitudes O(1) at G = 1/(32 pi) units here: roundoff of 256-term contractions ~ 1e-15).
    K = q1 + q2
    Ms_ = math.sqrt(_dot(K, K))
    k1c, k2c, _ = _cm_final(Ms_ ** 2, np.array(0.37), np.array(0.9), 0.0)
    b = K[1:] / K[0]
    g_ = 1 / math.sqrt(1 - b @ b)
    Lb = np.eye(4)
    Lb[0, 0] = g_
    Lb[0, 1:] = Lb[1:, 0] = g_ * b
    Lb[1:, 1:] += (g_ - 1) * np.outer(b, b) / (b @ b)
    k1, k2 = Lb @ k1c, Lb @ k2c
    worst_sum, worst_parts, worst_sc_sum, worst_sc_parts = 0.0, 1.0, 0.0, 1.0
    for l1, l2, s1, s2 in ((2, -2, 1, -1), (2, -2, -1, 1), (2, 2, 1, 1), (-2, 2, -1, 1)):
        Ea, Eb = graviton_polarization(q1, l1), graviton_polarization(q2, l2)
        e1, e2 = photon_polarization(k1, s1), photon_polarization(k2, s2)
        P0 = amplitude_gg_to_photons(q1, Ea, q2, Eb, k1, e1, k2, e2, parts=True)
        for qq, which in ((q1, 0), (q2, 1)):
            v = rng.normal(size=4) + 1j * rng.normal(size=4)
            xi = v - _dot(qq, v) / qq[0] * np.array([1.0, 0, 0, 0])
            sh = 0.8 * (np.outer(_low(qq), _low(xi)) + np.outer(_low(xi), _low(qq)))
            P1 = amplitude_gg_to_photons(q1, Ea + (sh if which == 0 else 0), q2, Eb + (sh if which == 1 else 0),
                                         k1, e1, k2, e2, parts=True)
            scale = max(abs(P0[c]) for c in ("contact", "s_channel", "tu_channel"))
            worst_sum = max(worst_sum, abs(P1["total"] - P0["total"]) / scale)
            worst_parts = min(worst_parts, max(abs(P1[c] - P0[c]) for c in ("contact", "s_channel", "tu_channel")) / scale)
        ks1, ks2, _ = _cm_final(Ms_ ** 2, np.array(0.37), np.array(0.9), 0.4)
        ks1, ks2 = Lb @ ks1, Lb @ ks2
        S0 = amplitude_gg_to_scalars(q1, Ea, q2, Eb, ks1, ks2, 0.4, parts=True)
        S1 = amplitude_gg_to_scalars(q1, Ea, q2, Eb + sh, ks1, ks2, 0.4, parts=True)     # sh: the shift of wave 2
        sc = max(abs(S0[c]) for c in ("contact", "s_channel", "tu_channel"))
        worst_sc_sum = max(worst_sc_sum, abs(S1["total"] - S0["total"]) / sc)
        worst_sc_parts = min(worst_sc_parts, max(abs(S1[c] - S0[c]) for c in ("contact", "s_channel", "tu_channel")) / sc)
    check("Ward identity g g -> gamma gamma: |delta M_total| / channel size under graviton gauge shifts (roundoff)",
          worst_sum, 0.0, 1e-12)
    check("...while some channel changes by > 10% of its size (channels separately NOT gauge invariant)",
          float(worst_parts > 0.1), 1.0, 0)
    check("Ward identity g g -> phi phi (m = 0.4): |delta M_total| / channel size (roundoff)", worst_sc_sum, 0.0, 1e-12)
    check("...and some scalar channel changes by > 10% (not separately invariant)", float(worst_sc_parts > 0.1), 1.0, 0)
    Ea, Eb = graviton_polarization(q1, 2), graviton_polarization(q2, -2)
    e1, e2 = photon_polarization(k1, 1), photon_polarization(k2, -1)
    M0 = amplitude_gg_to_photons(q1, Ea, q2, Eb, k1, e1, k2, e2)
    M1 = amplitude_gg_to_photons(q1, Ea, q2, Eb, k1, e1 + 0.7 * k1 / k1[0], k2, e2 - 1.3 * k2 / k2[0])
    check("photon gauge shift e -> e + c k (invariant by construction: every vertex built from F)",
          abs(M1 - M0) / abs(M0), 0.0, 1e-13)

    # 6. Bose symmetry (exact): exchange of the two gravitons and of the two photons.
    Mx = amplitude_gg_to_photons(q2, Eb, q1, Ea, k1, e1, k2, e2)
    My = amplitude_gg_to_photons(q1, Ea, q2, Eb, k2, e2, k1, e1)
    check("Bose symmetry: M(1 <-> 2 gravitons) and M(1 <-> 2 photons) equal M (max relative difference)",
          max(abs(Mx - M0), abs(My - M0)) / abs(M0), 0.0, 1e-13)

    # 7. Published unpolarised cross section, massive scalar target at rest: Holstein 2006, "Graviton physics",
    #    Am. J. Phys. 74, 1002, arXiv:gr-qc/0607045, eq. 66 (ACCESS: full-text; PDF extraction flattens fractions):
    #    "dσlab dΩ (S = 0) = ω2 f π F 2 1 16π(s−m2)2 (|C++|2 +|C+−|2) = G2m2(ωf ωi )2[ctn4 1 2θ cos4 1 2θ + sin4 1 2θ] (66)
    #    for a spinless target". Reading: dsigma/dOmega = G^2 m^2 (w_f/w_i)^2 [cot^4(th/2) cos^4(th/2) + sin^4(th/2)],
    #    w_f/w_i = 1/(1 + (2 w_i/m) sin^2(th/2)) (his eq. 13, quoted as "ωf = ωi 1 + 2 ωi m sin2 1 2θ (13)").
    #    Our amplitude is the crossed g g -> phi phi one, with
    #    the s-channel (here: graviton t-channel) from the second-order metric. Tolerance 1e-10: the closed form and
    #    the amplitude differ only by roundoff (no quadrature).
    worst = 0.0
    for w_, th_ in ((0.05, 0.3), (0.3, 1.3), (2.0, 2.5), (5.0, 3.0), (0.3, 1e-6)):
        mine = compton_scalar_lab_dsigma(w_, th_, 1.0)
        wfr = 1 / (1 + 2 * w_ * math.sin(th_ / 2) ** 2)
        hol = wfr ** 2 * (math.cos(th_ / 2) ** 8 / math.sin(th_ / 2) ** 4 + math.sin(th_ / 2) ** 4)
        worst = max(worst, abs(mine / hol - 1))
    check("massive-scalar gravitational Compton, lab frame, unpolarised: max |ours/Holstein eq. 66 - 1| (5 points, "
          "one at theta = 1e-6)",
          worst, 0.0, 1e-10)

    #    Classical limit: a slow graviton (w << m) grazing a mass is deflected like light, theta = 4 G m/b (GR light
    #    bending), so dsigma/dOmega = b |db/dtheta|/sin(theta) -> 16 G^2 m^2/theta^4 as theta -> 0. Tolerance 3e-5:
    #    the leading correction is -(5/6) theta^2 = -7.5e-6 at theta = 3e-3 (recoil: -(w/m) theta^2 = -1e-8).
    check("classical light-bending limit: Compton dsigma/dOmega x theta^4/(16 G^2 m^2) at w = 1e-3 m, theta = 3e-3",
          compton_scalar_lab_dsigma(1e-3, 3e-3, 1.0) * 3e-3 ** 4 / 16, 1.0, 3e-5)

    # 8. Published helicity amplitudes, massive scalar (Bjerrum-Bohr, Donoghue & Vanhove 2014, arXiv:1309.0804,
    #    eq. II.27, ACCESS: full-text; same formula as eq. A.13 of arXiv:1609.07477), all momenta incoming:
    #    "iM tree 0 (p1, p2, k+ 1 , k+ 2 ) = κ2 (4) 16 1 (k1· k2) m4 [k1 k2]4 (k1· p1)(k1· p2) , iM tree 0 (p1, p2, k− 1 , k+ 2 ) =
    #    κ2 (4) 16 1 (k1· k2) ⟨k1|p1|k2]2⟨k1|p2|k2]2 (k1· p1)(k1· p2)" with "κ2 (4) = 32 πGN".
    #    Reading (extraction flattens fractions and powers): iM = (kappa^2/16) m^4 [k1 k2]^4/((k1.k2)(k1.p1)(k1.p2)) and
    #    (kappa^2/16) <k1|p1|k2]^2 <k1|p2|k2]^2/((k1.k2)(k1.p1)(k1.p2)), kappa^2 = 32 pi G.
    #    Magnitudes: |[k1 k2]|^2 = 2|k1.k2|, |<k1|p|k2]|^2 = 2|2 (k1.p)(k2.p) - p^2 k1.k2|. SOURCE CORRECTION: our |M| is
    #    exactly HALF of eq. II.27 in both helicity structures and at all kinematics, while our cross section equals
    #    Holstein eq. 66 (check 7) and the light-bending forward limit (check 10); eq. II.27 as printed is twice too
    #    large. The check is that the RATIO is the same constant 1/2 everywhere (shape) to roundoff.
    def sq(a, P, bb):
        return abs(2 * (2 * _dot(a, P) * _dot(bb, P) - _dot(P, P) * _dot(a, bb)))
    ratios = []
    for w_, th_ in ((0.4, 0.7), (1.5, 2.0), (3.0, 1.1)):
        wf = w_ / (1 + 2 * w_ * math.sin(th_ / 2) ** 2)
        pin, qin = np.array([1.0, 0, 0, 0]), np.array([w_, 0, 0, w_])
        qout = wf * np.array([1.0, math.sin(th_), 0, math.cos(th_)])
        pout = pin + qin - qout
        p1_, p2_, k1_, k2_ = pin, -pout, qin, -qout
        den = abs(_dot(k1_, k2_) * _dot(k1_, p1_) * _dot(k1_, p2_))
        ref_pp = kap2 / 16 * (2 * abs(_dot(k1_, k2_))) ** 2 / den
        ref_mp = kap2 / 16 * sq(k1_, p1_, k2_) * sq(k1_, p2_, k2_) / den
        for li, lf, ref in ((2, 2, ref_mp), (-2, -2, ref_mp), (2, -2, ref_pp), (-2, 2, ref_pp)):
            M = compton_amplitude("scalar", pin, qin, graviton_polarization(qin, li), pout, qout,
                                  graviton_polarization(qout, lf), m=1.0)
            ratios.append(abs(complex(M)) / ref)
    check("massive scalar Compton helicity amplitudes / eq. II.27 of 1309.0804: constant ratio (spread)",
          max(ratios) - min(ratios), 0.0, 1e-12)
    check("...and that constant is 1/2 (source normalisation is 2x Holstein's; see source corrections)",
          float(np.mean(ratios)), 0.5, 1e-12)

    # 9. Published photon gravitational Compton amplitudes (Bjerrum-Bohr, Donoghue, Holstein, Plante & Vanhove 2016,
    #    arXiv:1609.07477, appendix A.2, ACCESS: full-text), photons p, gravitons k:
    #    "M(+−|+−) γ2G2 = κ2 8 [p1k1]2⟨p2k2⟩2⟨k2|p1|k1]2 (p1·p2)(p1·k1)(p1·k2) , (A.10) M(−+|+−) γ2G2 = κ2 8
    #    [p2k1]2⟨p1k2⟩2⟨k2|p2|k1]2 (p1·p2)(p1·k1)(p1·k2) , (A.11) and their complex conjugates" and the other
    #    configurations "vanish". Reading: M = (kappa^2/8) [p1k1]^2 <p2k2>^2 <k2|p1|k1]^2/((p1.p2)(p1.k1)(p1.k2)), etc.,
    #    all momenta incoming. Magnitudes: |A.10| = 2 kappa^2 (p1.k1)^2/|p1.p2|, |A.11| = 2 kappa^2 (p1.k2)^2/|p1.p2|.
    #    SOURCE CORRECTION: ours are exactly 1/4 of these (shape agrees to roundoff); the forward limit (check 10) and
    #    their own one-graviton-exchange eq. A.16 fix the normalisation at (kappa/2)^2 s^2/|t|.
    rat, zeros = [], 0.0
    for th_ in (0.6, 1.4, 2.6):
        Pin, Kin = np.array([1.0, 0, 0, -1.0]), np.array([1.0, 0, 0, 1.0])
        Kout = np.array([1.0, math.sin(th_), 0, math.cos(th_)])
        Pout = Pin + Kin - Kout
        p1_, p2_, k1_, k2_ = Pin, -Pout, Kin, -Kout
        r10 = 2 * kap2 * _dot(p1_, k1_) ** 2 / abs(_dot(p1_, p2_))
        r11 = 2 * kap2 * _dot(p1_, k2_) ** 2 / abs(_dot(p1_, p2_))
        found = []
        for hi in (1, -1):
            for ho in (1, -1):
                for li in (2, -2):
                    for lf in (2, -2):
                        M = abs(complex(compton_amplitude("photon", Pin, Kin, graviton_polarization(Kin, li), Pout, Kout,
                                                          graviton_polarization(Kout, lf), photon_polarization(Pin, hi),
                                                          photon_polarization(Pout, ho))))
                        if M > 1e-9 * r11:
                            found.append(M)
                        else:
                            zeros = max(zeros, M / r10)
        rat += [max(found) / max(r10, r11), min(found) / min(r10, r11)]
    check("photon Compton: the two nonzero |M| / |A.10|, |A.11| of 1609.07477: constant ratio (spread)",
          max(rat) - min(rat), 0.0, 1e-12)
    check("...that constant is 1/4 (source normalisation 4x the forward-limit value; see source corrections)",
          float(np.mean(rat)), 0.25, 1e-12)
    check("...and the other 12 helicity configurations vanish as the source says (max |M| / |A.10|)", zeros, 0.0, 1e-12)

    # 10. Limit: forward scattering is one-graviton exchange, the same for every massless probe (equivalence
    #     principle, light bending). 1609.07477 eq. A.16, photon off a scalar of mass M via one graviton:
    #     "M(1) (+−) γ2Φ2 =κ2⟨p2|p3|p1]2 4(p1 +p2)2 =κ2 (M 4−su)2 4t⟨p1|p3|p2]2" (reading: kappa^2 <p2|p3|p1]^2/(4 (p1 + p2)^2),
    #     t = (p1 + p2)^2) -> for M = 0 and t -> 0, |M| -> kappa^2 s^2/(4|t|).
    #     Our photon-graviton and massless-scalar-graviton helicity-conserving Compton amplitudes must approach the same.
    th_ = 1e-3
    Pin, Kin = np.array([1.0, 0, 0, -1.0]), np.array([1.0, 0, 0, 1.0])
    Kout = np.array([1.0, math.sin(th_), 0, math.cos(th_)])
    Pout = Pin + Kin - Kout
    s_, t_ = _dot(Pin + Kin, Pin + Kin), _dot(Kin - Kout, Kin - Kout)
    ref = kap2 * s_ * s_ / (4 * abs(t_))
    Mg = abs(complex(compton_amplitude("photon", Pin, Kin, graviton_polarization(Kin, 2), Pout, Kout,
                                       graviton_polarization(Kout, 2), photon_polarization(Pin, 1), photon_polarization(Pout, 1))))
    Mphi = abs(complex(compton_amplitude("scalar", Pin, Kin, graviton_polarization(Kin, 2), Pout, Kout,
                                         graviton_polarization(Kout, 2))))
    #     Tolerance 2e-6: the helicity-conserving photon amplitude equals (kappa/2)^2 s^2/|t| at all angles; the
    #     scalar one is (kappa/2)^2 s |u|/|t|, off by |t|/s = sin^2(th/2) = 2.5e-7 here.
    check("forward limit (theta_cm = 1e-3): photon-graviton |M| vs one-graviton exchange kappa^2 s^2/(4|t|) [A.16]",
          Mg / ref, 1.0, 2e-6)
    check("forward limit: massless-scalar-graviton |M| vs the same (universality)", Mphi / ref, 1.0, 2e-6)

    # 11. qft_production (independent code) at the s-channel: the pair yield of -(1/2) dg2 T with dg2 the second-order
    #     metric must equal qp's (1/4)[rho2 X2 + rho0 X0] (stress_spectral_densities, _metric_weights), i.e. the
    #     s-channel alone is a first-order background for Part D. Photons and a massive scalar (rho0 != 0).
    #     Quadrature: Gauss 24 x 24 is exact for the polynomial photon integrand; tolerance 1e-9 covers the scalar.
    for fld, mm in (("photon", 0.0), ("scalar", 0.3)):
        Ea, Eb = 0.01 * graviton_polarization(q1, "plus"), 0.02 * graviton_polarization(q2, "R")
        dg2 = second_order_metric(q1, Ea, q2, Eb)["dg2"]
        X2, X0 = qp._metric_weights(*[np.array([c]) for c in K], dg2[None])
        r2, r0 = qp.stress_spectral_densities([Ms_ ** 2], fld, mm)
        qp_val = float(0.25 * (r2[0] * X2[0] + r0[0] * X0[0]))
        Lr = np.linalg.inv(Lb)
        q1c, q2c = Lr @ q1, Lr @ q2
        Ec, Fc = Lb.T @ Ea @ Lb, Lb.T @ Eb @ Lb
        c, wc = np.polynomial.legendre.leggauss(24)
        ph = (np.arange(24) + 0.5) * 2 * PI / 24
        C_, P_ = np.meshgrid(c, ph, indexing="ij")
        kk1, kk2, pst = _cm_final(Ms_ ** 2, C_, P_, mm)
        tot = 0.0
        for _, w1, w2 in _final_wavefunctions(fld, kk1, kk2):
            Mss = (_core_photon(q1c, Ec, q2c, Fc, kk1, w1, kk2, w2)[1] if fld == "photon"
                   else _core_scalar(q1c, Ec, q2c, Fc, kk1, kk2, mm)[1])
            tot = tot + np.abs(Mss) ** 2
        ours = 0.5 * float(np.einsum("i,ij->", wc, tot)) * (2 * PI / 24) * pst / (16 * PI * PI * Ms_)
        check(f"s-channel = qft_production Part D fed with the second-order metric ({fld}): yield ratio", ours / qp_val,
              1.0, 1e-9)

    #     The trap: Part D fed with the second-order metric ALONE (gauge dependent) for two same-helicity waves at 90 deg
    #     predicts photon pairs, while the full tree amplitude gives none (check 13); head-on R/L it predicts none while the
    #     full answer is nonzero.
    for (pa, pb, th_) in (("R", "R", PI / 2), ("R", "L", PI)):
        A_, B_ = _beams(1.0, 1e-3, 1.0, 1e-3, th_, pa, pb, 1.0)
        so = second_order_metric(A_["q"], A_["H"], B_["q"], B_["H"])
        X2, X0 = qp._metric_weights(*[np.array([c]) for c in so["K"]], so["dg2"][None])
        r2, r0 = qp.stress_spectral_densities([so["s"]], "photon")
        part_d = float(0.25 * (r2[0] * X2[0] + r0[0] * X0[0]))
        full = beams_pair_rate(1.0, 1e-3, 1.0, 1e-3, th_, pa, pb)["pair_rate"]
        ref_scale = beams_pair_rate(1.0, 1e-3, 1.0, 1e-3, th_, "R", "L" if pa == "R" and pb == "R" else "L")["pair_rate"]
        check(f"trap: Part D fed dg2 alone vs full rate, {pa}/{pb} at {th_ * 180 / PI:.0f} deg (one is zero, the other "
              f"is not: |difference| / R-L rate > 0.5)", float(abs(part_d - full) / ref_scale > 0.5 and min(part_d, full)
                                                            < 1e-20 * ref_scale), 1.0, 0)

    # 12. The full amplitude is NOT of the form h~(K).T(k1, k2) (no effective background), the s-channel is:
    #     least-squares fit over 40 final states at fixed K.
    Ea, Eb = graviton_polarization(q1, "plus"), graviton_polarization(q2, "cross")
    Ml, Msl, Tl = [], [], []
    for _ in range(40):
        u = rng.normal(size=3)
        kk1, kk2, _p = _cm_final(Ms_ ** 2, np.array(u[2] / np.linalg.norm(u)), np.array(math.atan2(u[1], u[0])), 0.0)
        kk1, kk2 = Lb @ kk1, Lb @ kk2
        s1, s2 = (1 if rng.random() < 0.5 else -1), (1 if rng.random() < 0.5 else -1)
        w1, w2 = np.conj(photon_polarization(kk1, s1)), np.conj(photon_polarization(kk2, s2))
        Mc_, Ms2, Mtu_ = _core_photon(q1, Ea, q2, Eb, kk1, w1, kk2, w2)
        Ml.append(complex(Mc_ + Ms2 + Mtu_))
        Msl.append(complex(Ms2))
        Tl.append(_photon_T(kk1, w1, kk2, w2))
    check("effective-background test: s-channel lies in span{h.T} (relative residual)", _span_residual(Msl, Tl), 0.0, 1e-10)
    check("...the full amplitude does not (relative residual > 0.1)", float(_span_residual(Ml, Tl) > 0.1), 1.0, 0)

    # 13. Helicity selection (consistent with the vanishing configurations quoted in check 9): same-helicity gravitons
    #     make no massless pairs; opposite ones give |M| = (kappa/2)^2 t^2/s, (kappa/2)^2 u^2/s (photons) and
    #     (kappa/2)^2 |t u|/s (massless scalars), the crossing of eqs. A.10, A.11, A.13 with corrected normalisation.
    s0, th0 = 3.0, 1.1
    amps = helicity_amplitudes_cm(s0, th0, 0.4, "photon")
    t0, u0 = -s0 * (1 - math.cos(th0)) / 2, -s0 * (1 + math.cos(th0)) / 2
    same = max(abs(amps[(l, l, a, b)]) for l in (2, -2) for a in (1, -1) for b in (1, -1))
    opp = sorted(abs(amps[(2, -2, a, b)]) for a in (1, -1) for b in (1, -1))
    check("g g -> gamma gamma, same-helicity gravitons: max |M| (all photon helicities)", same / (kap2 * s0), 0.0, 1e-14)
    check("opposite helicities: |M| = (kappa/2)^2 {t^2, u^2}/s, same-helicity photons 0 (max rel. deviation)",
          max(abs(opp[2] / (kap2 / 4 * t0 * t0 / s0) - 1), abs(opp[3] / (kap2 / 4 * u0 * u0 / s0) - 1), opp[0] / opp[3], opp[1] / opp[3]),
          0.0, 1e-12)
    sc = helicity_amplitudes_cm(s0, th0, 0.4, "scalar")
    check("g g -> phi phi massless: same-helicity 0 and opposite (kappa/2)^2 |t u|/s (max rel. deviation)",
          max(abs(sc[(2, 2)]) / (kap2 * s0), abs(abs(sc[(2, -2)]) / (kap2 / 4 * t0 * u0 / s0) - 1)), 0.0, 1e-12)

    # 14. Total cross sections: numerical CM quadrature vs the closed forms (4/5) pi G^2 s, pi G^2 s/15 (opposite
    #     helicities) and the linear-polarisation half. Gauss 24 is exact for these polynomial integrands: tolerance 1e-10.
    for fin, p1_, p2_ in (("photon", "R", "L"), ("photon", "plus", "plus"), ("photon", "plus", "cross"),
                          ("scalar", "L", "R"), ("photon", "R", "R")):
        num_ = sigma_total(2.5, p1_, p2_, fin)
        cf = sigma_total_massless_closed_form(2.5, p1_, p2_, fin)
        check(f"sigma_tot g g -> {fin} pair ({p1_}, {p2_}) quadrature vs closed form (s = 2.5, G = 1)", num_,
              cf, 1e-10 * max(cf, 1.0))

    # 15. Luminosity relation, both sides independent: LEFT = lab-frame phase-space integral of |M(H1, H2)|^2 built from
    #     the strains (no CM, no cross section); RIGHT = closed-form sigma x n1 n2 (1 - cos theta) with n = rho/w and
    #     rho = w^2 h^2/(32 pi G) (F&H eq. 5.40, quoted at check 2) for linear polarisation, w^2 h^2/(16 pi G) circular.
    #     Lab quadrature: smooth (spectrally convergent) for circular polarisations; for linear ones the interference of
    #     the J_z = +-4 channels is non-smooth along the CM collision axis and the azimuthal rule about K converges as
    #     n_phi^-6 (measured 9e-7, 1.5e-8, 2.3e-10 at n_phi = 48, 96, 192; 'convergence'): n_c x n_phi = 192 x 96,
    #     tolerance 1e-7. The CM route aligns its axis with the collision axis and is exact: tolerance 1e-9.
    for th_, pa, pb, wa_, wb_, fin in ((2 * PI / 3, "plus", "plus", 1.0, 1.0, "photon"), (PI / 2, "R", "L", 1.0, 2.3, "photon"),
                                       (PI, "plus", "cross", 0.7, 1.0, "photon"), (1.2, "L", "R", 1.0, 0.6, "scalar")):
        A_, B_ = _beams(wa_, 1e-3, wb_, 2e-3, th_, pa, pb, 1.0)
        lin = pa in ("plus", "cross") or pb in ("plus", "cross")
        left = _beams_rate_lab(A_, B_, fin, 192 if lin else 64, 96 if lin else 32)
        rho_a = wa_ ** 2 * 1e-6 / (32 * PI) * (2 if pa in ("R", "L") else 1)
        rho_b = wb_ ** 2 * 4e-6 / (32 * PI) * (2 if pb in ("R", "L") else 1)
        s_ = 2 * wa_ * wb_ * (1 - math.cos(th_))
        right = sigma_total_massless_closed_form(s_, pa, pb, fin) * (rho_a / wa_) * (rho_b / wb_) * (1 - math.cos(th_))
        check(f"rate/volume = sigma n1 n2 (1 - cos th): lab-frame direct vs closed form ({fin}, th = {th_ * 180 / PI:.0f} deg,"
              f" {pa}/{pb})", left, right, 1e-7, rel=True)
        mid = beams_pair_rate(wa_, 1e-3, wb_, 2e-3, th_, pa, pb, fin)["pair_rate"]
        check("   ...and the CM-boosted route (beams_pair_rate) agrees", mid, right, 1e-9, rel=True)

    # 16. Limits and scalings: collinear waves give nothing ((1 - cos th)^2 -> 0); rate ~ h1^2 h2^2 and is independent
    #     of G at fixed strain. beams_pair_rate works with G-free strains, so its own G-independence is a consistency
    #     check only; the physics check goes through routes where G really enters: (a) sigma_total(G) (kappa^4) times
    #     the Isaacson densities n(G) = w h^2/(16 pi G) of gw_plane_wave, (b) the in-out amplitude with kappa^2 = 32 pi G
    #     fed the canonical coherent amplitudes A = |H|/sqrt(32 pi G).
    r1 = beams_pair_rate(1.0, 1e-3, 1.0, 1e-3, 1e-2, "plus", "plus")["pair_rate"]
    r2_ = beams_pair_rate(1.0, 1e-3, 1.0, 1e-3, 2e-2, "plus", "plus")["pair_rate"]
    check("collinear limit: rate(theta = 0.02)/rate(theta = 0.01) = ((1 - cos 0.02)/(1 - cos 0.01))^2 (~16: rate -> 0)",
          r2_ / r1, ((1 - math.cos(0.02)) / (1 - math.cos(0.01))) ** 2, 1e-9, rel=True)
    ra = beams_pair_rate(1.0, 1e-3, 1.0, 1e-3, 2.0, "R", "L", G=1.0)
    rb = beams_pair_rate(1.0, 2e-3, 1.0, 3e-3, 2.0, "R", "L", G=7.0)
    check("consistency: beams rate x (h1 h2)^-2 the same for (h1, h2, G) = (1e-3, 1e-3, 1) and (2e-3, 3e-3, 7)",
          rb["pair_rate"] / ra["pair_rate"], 36.0, 1e-9, rel=True)
    lum = []
    for G_ in (1.0, 7.0):
        A_, B_ = _beams(1.0, 1e-3, 1.3, 2e-3, 2.0, "R", "L", G_)
        lum.append(sigma_total(2 * 1.3 * (1 - math.cos(2.0)), "R", "L", G=G_) * A_["n"] * B_["n"] * (1 - math.cos(2.0)))
    check("G-independence at fixed strain: sigma_total(G) n1(G) n2(G) (1 - cos th), G = 7 vs 1 (G enters both factors)",
          lum[1] / lum[0], 1.0, 1e-12, rel=True)
    amp_G = []
    for G_ in (1.0, 7.0):
        A_, B_ = _beams(1.0, 1e-3, 1.3, 2e-3, 2.0, "plus", "R", G_)
        kq = A_["q"] + B_["q"]
        bb = kq[1:] / kq[0]                               # CM final state (along y, transverse to the 2-wave plane)
        gg = 1 / math.sqrt(1 - bb @ bb)                   # boosted to the lab
        Lg = np.eye(4)
        Lg[0, 0] = gg
        Lg[0, 1:] = Lg[1:, 0] = gg * bb
        Lg[1:, 1:] += (gg - 1) * np.outer(bb, bb) / (bb @ bb)
        Eh = 0.5 * math.sqrt(_dot(kq, kq))
        k1g = Lg @ np.array([Eh, 0.0, Eh, 0.0])
        k2g = kq - k1g
        Mg = amplitude_gg_to_photons(A_["q"], A_["A"] * A_["eps"], B_["q"], B_["A"] * B_["eps"], k1g,
                                     photon_polarization(k1g, 1), k2g, photon_polarization(k2g, -1), G=G_)
        amp_G.append(abs(complex(Mg)))
    check("G-independence at fixed strain: |M(kappa^2 = 32 pi G; A = |H|/sqrt(32 pi G))|, G = 7 vs 1",
          amp_G[1] / amp_G[0], 1.0, 1e-12, rel=True)

    # 17. SI: F&H eq. 5.41 "T tz = 1.5 mW m −2 ( h0 10−22 ) 2 ( f 1 kHz ) 2" (energy flux = rho c of a linear wave) and the
    #     closed-form photon rate w^4 h^4 (1 - cos th)^2/(1280 pi c^3) for linear waves (from (2/5) pi G^2 s).
    #     F&H round to 2 digits: tolerance 0.06.
    si = beams_pair_rate_SI(2 * PI * 1e3, 1e-22, PI)
    check("SI energy flux rho c of a 1 kHz, h = 1e-22 wave vs F&H eq. 5.41 (1.5 mW/m^2)", si["rho1_SI"] * C, 1.5e-3, 0.06, rel=True)
    w_ = 2 * PI * 1e3
    check("SI pair rate (head-on, plus/plus, 1 kHz, h = 1e-22) vs w^4 h^4 (1 - cos th)^2/(1280 pi c^3)",
          si["pair_rate_SI"], w_ ** 4 * 1e-88 * 4 / (1280 * PI * C ** 3), 1e-8, rel=True)

    # 18. Extreme kinematics (the CM transformation): before it, these were wrong by factors up to 1e22 (beams) and
    #     4e3 (amplitudes) without warning. (a) LIGO x PTA-like frequency ratio 1e-12 at 90 deg and (b) nearly collinear
    #     equal-frequency waves (theta = 1e-9, K0^2/s = 4e18) against sigma_closed_form n1 n2 (1 - cos theta);
    #     measured <= 4e-15: tolerance 1e-12. (c) A lab event with an opening angle d between the gravitons (w = 1 and
    #     1.3), photon 1 along a fixed lab direction n with E1 = s/(2 (K0 - K.n)) so that t = -2 E1 (1 - n_z), u = -s - t
    #     and s = 4 w1 w2 sin^2(d/2) are exact; |M| vs (kappa/2)^2 {t^2, u^2}/s and massless scalars vs (kappa/2)^2 |t u|/s
    #     at d = 1e-3 and 1e-6 (K0^2/s = 4e6, 4e12; measured <= 1e-14): tolerance 1e-12.
    worst = 0.0
    for w2_, th_, pols in ((1e-12, PI / 2, (("R", "L"), ("plus", "cross"))), (1.0, 1e-9, (("plus", "plus"), ("L", "R")))):
        for pa, pb in pols:
            A_, B_ = _beams(1.0, 1e-3, w2_, 2e-3, th_, pa, pb, 1.0)
            fl = 2 * math.sin(th_ / 2) ** 2
            want = sigma_total_massless_closed_form(2 * w2_ * fl, pa, pb) * A_["n"] * B_["n"] * fl
            worst = max(worst, abs(beams_pair_rate(1.0, 1e-3, w2_, 2e-3, th_, pa, pb)["pair_rate"] / want - 1))
    check("extreme beams: w2/w1 = 1e-12 (R/L, plus/cross) and theta = 1e-9 (plus/plus, L/R) vs sigma n1 n2 (1 - cos th)",
          worst, 0.0, 1e-12)
    worst = 0.0
    for d_ in (1e-3, 1e-6):
        qa_ = np.array([1.0, 0.0, 0.0, 1.0])
        qb_ = 1.3 * np.array([1.0, math.sin(d_), 0.0, math.cos(d_)])
        Kl = qa_ + qb_
        s_ = 4 * 1.3 * math.sin(d_ / 2) ** 2
        nl = np.array([math.sin(0.5) * math.cos(0.3), math.sin(0.5) * math.sin(0.3), math.cos(0.5)])
        E1 = s_ / (2 * (Kl[0] - Kl[1:] @ nl))
        k1l = np.concatenate([[E1], E1 * nl])
        k2l = Kl - k1l
        t_ = -2 * E1 * 2 * math.sin(0.25) ** 2
        u_ = -s_ - t_
        Ea, Eb = graviton_polarization(qa_, "R"), graviton_polarization(qb_, "L")
        got = sorted(abs(complex(amplitude_gg_to_photons(qa_, Ea, qb_, Eb, k1l, photon_polarization(k1l, a), k2l,
                                                          photon_polarization(k2l, -a)))) for a in (1, -1))
        want = sorted([kap2 / 4 * t_ * t_ / s_, kap2 / 4 * u_ * u_ / s_])
        Msc = abs(complex(amplitude_gg_to_scalars(qa_, Ea, qb_, Eb, k1l, k2l)))
        worst = max(worst, abs(got[0] / want[0] - 1), abs(got[1] / want[1] - 1), abs(Msc / (kap2 / 4 * abs(t_ * u_) / s_) - 1))
    check("boosted lab events (opening angle 1e-3, 1e-6): |M| vs (kappa/2)^2 {t^2, u^2}/s and |t u|/s (max rel. dev.)",
          worst, 0.0, 1e-12)

    # 19. Light massive scalar, same helicities (the whole answer is the m^4 piece, peaked within 2 m^2/s of the axis):
    #     graded-panel quadrature of the diagrammatic amplitude vs the analytic integral of the crossed eq. II.27
    #     (sigma_same_helicity_scalar_closed_form). Before the graded rule: 11% (m = 0.01) and 62% (m = 0.03) of the
    #     answer. Measured 4e-11 and 6e-12 (roundoff ~ 1e-14 s/m^2): tolerance 1e-9; beams head-on R/R, m = 0.02.
    worst = 0.0
    for m_ in (0.01, 0.02):
        worst = max(worst, abs(sigma_total(1.0, "R", "R", "scalar", m_) / sigma_same_helicity_scalar_closed_form(1.0, m_) - 1))
    A_, B_ = _beams(1.0, 1e-3, 1.0, 1e-3, PI, "R", "R", 1.0)
    rb_ = beams_pair_rate(1.0, 1e-3, 1.0, 1e-3, PI, "R", "R", "scalar", 0.02)["pair_rate"]
    worst = max(worst, abs(rb_ / (sigma_same_helicity_scalar_closed_form(4.0, 0.02) * A_["n"] * B_["n"] * 2.0) - 1))
    check("light scalar R/R (m/sqrt(s) = 0.01, 0.02; beams m = 0.02 head-on) vs the analytic same-helicity sigma",
          worst, 0.0, 1e-9)

    passed = all(results)
    if verbose:
        print(f"\n{sum(results)}/{len(results)} checks passed")
    return passed


# ---------------------------------------------------------------- convergence studies
def _convergence() -> int:
    """Quadrature and roundoff studies (not part of the self-test)."""
    print("sigma_tot (photon, R/L, s = 1) vs Gauss order; closed form (4/5) pi =", 0.8 * PI)
    for n in (8, 12, 24, 48):
        print(f"  n_theta = {n}, n_phi = {max(n, 17)}: {sigma_total(1.0, 'R', 'L', n_theta=n, n_phi=max(n, 17)):.15g}")
    print("massive scalar, s = 1: sigma_tot(R/R) / sigma_same_helicity_scalar_closed_form - 1 vs n_theta (graded panels)")
    for m in (0.4, 0.05, 0.01, 0.002, 1e-4):
        row = [f"{sigma_total(1.0, 'R', 'R', 'scalar', m, n_theta=n) / sigma_same_helicity_scalar_closed_form(1.0, m) - 1:+.1e}"
               for n in (24, 48, 96)]
        print(f"  m = {m:g}: n_theta = 24, 48, 96 -> {row}")
    print("beams vs sigma n1 n2 (1 - cos theta) - 1 at extreme kinematics (R/L, plus/cross)")
    for w2, th in ((1e-6, PI / 2), (1e-12, PI / 2), (1e-20, PI / 2), (1.0, 1e-5), (1.0, 1e-9), (1.0, 2.1e-12)):
        row = []
        for pa, pb in (("R", "L"), ("plus", "cross")):
            A_, B_ = _beams(1.0, 1e-3, w2, 1e-3, th, pa, pb, 1.0)
            fl = 2 * math.sin(th / 2) ** 2
            want = sigma_total_massless_closed_form(2 * w2 * fl, pa, pb) * A_["n"] * B_["n"] * fl
            row.append(f"{beams_pair_rate(1.0, 1e-3, w2, 1e-3, th, pa, pb)['pair_rate'] / want - 1:+.1e}")
        print(f"  w2/w1 = {w2:g}, theta = {th:g}: {row}")
    print("lab-frame direct rate / closed-form luminosity rate, plus/plus, vs (n_c, n_phi) and theta")
    for th in (PI / 6, PI / 3, 2 * PI / 3, PI):
        A_, B_ = _beams(1.0, 1e-3, 1.0, 1e-3, th, "plus", "plus", 1.0)
        right = sigma_total_massless_closed_form(2 * (1 - math.cos(th)), "plus", "plus") * (1e-6 / (32 * PI)) ** 2 * (1 - math.cos(th))
        row = [f"{_beams_rate_lab(A_, B_, 'photon', n, max(n // 2, 17)) / right - 1:+.2e}" for n in (24, 48, 96, 192)]
        print(f"  theta = {th * 180 / PI:5.1f} deg: n = 24, 48, 96, 192 -> {row}")
    print("energy-scale invariance: rate/scale^4 for waves of frequency 'scale' (should be constant)")
    for sc in (1e-12, 1.0, 1e12):
        r = beams_pair_rate(sc, 1e-3, sc, 1e-3, 2.0, "R", "L")
        print(f"  scale {sc:g}: rate/scale^4 = {r['pair_rate'] / sc ** 4:.15g}")
    return 0


# ---------------------------------------------------------------- command line
def _parse_energy(text: str) -> float:
    try:
        return float(text)
    except ValueError:
        from unit_tools import Q
        return Q(text).expect("energy").si / E_CHARGE


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("selftest")
    sub.add_parser("convergence", help="quadrature convergence and roundoff studies (slow-ish)")
    bp = sub.add_parser("beams", help="photon (or scalar) pairs per m^3 per s from two crossing gravitational waves")
    g = bp.add_mutually_exclusive_group(required=True)
    g.add_argument("--omega", help="ANGULAR frequency (unit 1/s): '1 kHz' means omega = 1000 rad/s")
    g.add_argument("--f", help="ordinary frequency, omega = 2 pi f, e.g. '100 Hz'")
    bp.add_argument("--omega2", help="angular frequency of wave 2 (default: same)")
    bp.add_argument("--h", type=float, required=True, help="GR strain amplitude of wave 1 (e.g. 1e-21)")
    bp.add_argument("--h2", type=float, help="strain of wave 2 (default: same)")
    bp.add_argument("--theta", type=float, required=True, help="angle between propagation directions, degrees (180 = head-on)")
    bp.add_argument("--pol1", default="plus", choices=_POLS)
    bp.add_argument("--pol2", default="plus", choices=_POLS)
    bp.add_argument("--final", default="photon", choices=("photon", "scalar"))
    bp.add_argument("--m", default="0", help="scalar mass, e.g. '1e-12 eV' (bare number = eV)")
    ap_ = sub.add_parser("amplitudes", help="CM helicity amplitudes and dsigma/dOmega (G = 1; s and m in one arbitrary "
                                            "energy unit, cross sections in its inverse square)")
    ap_.add_argument("--s", type=float, default=1.0)
    ap_.add_argument("--theta", type=float, required=True, help="degrees")
    ap_.add_argument("--final", default="photon", choices=("photon", "scalar"))
    ap_.add_argument("--m", type=float, default=0.0)
    cp = sub.add_parser("compton", help="unpolarised lab cross section of graviton scattering off a massive scalar (G = 1)")
    cp.add_argument("--omega", type=float, required=True, help="graviton energy in units of the mass (omega/m)")
    cp.add_argument("--theta", type=float, required=True, help="degrees")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "selftest":
            return 0 if selftest() else 1
        if args.cmd == "convergence":
            return _convergence()
        if args.cmd == "amplitudes":
            amps = helicity_amplitudes_cm(args.s, math.radians(args.theta), 0.0, args.final, args.m)
            print(f"g g -> {args.final} pair, s = {args.s}, m = {args.m} (one arbitrary energy unit), theta = {args.theta} deg "
                  "(G = 1 in that unit^-2; M dimensionless, in-out; dsigma/dOmega and sigma in unit^-2)")
            for key, M in amps.items():
                print(f"  {key}: M = {M.real:+.6e} {M.imag:+.6e} i   |M| = {abs(M):.6e}")
            for p1, p2 in (("R", "L"), ("R", "R"), ("plus", "plus")):
                print(f"  dsigma/dOmega({p1},{p2}) = {dsigma_domega_cm(args.s, math.radians(args.theta), p1, p2, args.final, args.m):.6e}"
                      f"   sigma_tot = {sigma_total(args.s, p1, p2, args.final, args.m):.6e} (pairs, 1/2 for identical)")
            return 0
        if args.cmd == "compton":
            ds = compton_scalar_lab_dsigma(args.omega, math.radians(args.theta), 1.0)
            print(f"unpolarised lab dsigma/dOmega = {ds:.8g} G^2 m^2 (omega/m = {args.omega:g}, "
                  f"theta = {args.theta:g} deg)")
            return 0
        from unit_tools import Q
        if args.omega is not None:
            w1 = Q(args.omega).expect("frequency").si
            if "hz" in args.omega.lower():
                print(f"note: --omega is an ANGULAR frequency; '{args.omega}' is read as omega = {w1:.6g} rad/s "
                      f"(f = {w1 / (2 * PI):.6g} Hz). For an ordinary frequency use --f (rate ~ omega^4).")
        else:
            w1 = 2 * PI * Q(args.f).expect("frequency").si
        w2 = Q(args.omega2).expect("frequency").si if args.omega2 else w1
        if args.omega2 and "hz" in args.omega2.lower():
            print(f"note: --omega2 is an ANGULAR frequency: omega2 = {w2:.6g} rad/s (f2 = {w2 / (2 * PI):.6g} Hz)")
        m_eV = _parse_energy(args.m)
        r = beams_pair_rate_SI(w1, args.h, math.radians(args.theta), w2, args.h2, args.pol1, args.pol2, args.final, m_eV)
        print(f"wave 1: omega = {w1:.6g} rad/s, h = {args.h:g} ({args.pol1}); wave 2: omega = {w2:.6g} rad/s, "
              f"h = {args.h2 if args.h2 else args.h:g} ({args.pol2}); angle {args.theta:g} deg")
        print(f"energy densities {r['rho1_SI']:.4g}, {r['rho2_SI']:.4g} J/m^3; graviton densities {r['n1_SI']:.4g}, {r['n2_SI']:.4g} m^-3")
        print(f"cross section for these polarisations sigma = {r['sigma_m2']:.4g} m^2  (s = {r['natural']['s']:.4g} eV^2)")
        print(f"{args.final} PAIRS per m^3 per s (in-in mean number, tree level, plane waves): {r['pair_rate_SI']:.6g}")
        print(f"{args.final}s per m^3 per s: {r['particle_rate_SI']:.6g}")
        massless = args.final == "photon" or m_eV == 0
        if massless and args.pol1 == args.pol2 and args.pol1 in ("R", "L"):
            print("note: same-helicity waves make NO massless pairs at tree level; the value above is quadrature roundoff")
    except (ValueError, KeyError) as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
