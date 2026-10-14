"""Falsifier C7-2 (scale angle).
(1) Is the GW -> photon-pair yield 'photon-vacuum pair creation on the classical second-order metric h^(2)'?
    Compare, for two crossing plane GW beams in the lab TT gauge, the phase-space integral of |M_s|^2
    (s-channel = Maxwell vertex fed with h^(2); what a Maxwell-on-h^(2) Bogoliubov/Part-D yield computes)
    with that of the full tree amplitude (contact + t/u photon exchange + s-channel).
    Natural units hbar = c = 1, G = 1 (ratios are G-independent).
(2) hbar scaling of the full two-beam rate in SI, and of eq. 8 when N = E/(hbar w).
(3) Scale: size of CMB-stimulated factor 2 f_gamma (Rayleigh-Jeans extrapolation) at LIGO frequencies.
"""
import sys, math
import numpy as np
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import qft_second_order as q2

PI = math.pi


def boost_matrix(beta_vec):
    b = np.linalg.norm(beta_vec)
    g = 1 / math.sqrt(1 - b * b)
    L = np.eye(4)
    if b == 0:
        return L
    n = beta_vec / b
    L[0, 0] = g
    L[0, 1:] = g * b * n
    L[1:, 0] = g * b * n
    L[1:, 1:] = np.eye(3) + (g - 1) * np.outer(n, n)
    return L  # maps CM 4-vectors (upper) to lab


def integrals(theta, pol1, pol2, w=1.0, nc=40, nph=40):
    qa = np.array([w, 0, 0, w])
    qb = np.array([w, w * math.sin(theta), 0, w * math.cos(theta)])
    Ea = q2.graviton_polarization(qa, pol1)
    Eb = q2.graviton_polarization(qb, pol2)
    K = qa + qb
    s = K[0] ** 2 - K[1:] @ K[1:]
    L = boost_matrix(K[1:] / K[0])
    E = 0.5 * math.sqrt(s)
    # Gauss-Legendre in cos(theta*) (midpoint offsets avoid exact t,u = 0)
    xg, wg = np.polynomial.legendre.leggauss(nc)
    phis = (np.arange(nph) + 0.37) * 2 * PI / nph
    Ws = Wt = Wc = Wtu = 0.0
    for c, wc in zip(xg, wg):
        st = math.sqrt(1 - c * c)
        for ph in phis:
            n = np.array([st * math.cos(ph), st * math.sin(ph), c])
            k1 = L @ np.concatenate([[E], E * n])
            k2 = L @ np.concatenate([[E], -E * n])
            k1[0] = np.linalg.norm(k1[1:]); k2[0] = np.linalg.norm(k2[1:])
            for s1 in (1, -1):
                for s2 in (1, -1):
                    e1 = q2.photon_polarization(k1, s1)
                    e2 = q2.photon_polarization(k2, s2)
                    try:
                        P = q2.amplitude_gg_to_photons(qa, Ea, qb, Eb, k1, e1, k2, e2, G=1.0, parts=True)
                    except ValueError:
                        continue
                    wt = wc * (2 * PI / nph)
                    Ws += wt * abs(P["s_channel"]) ** 2
                    Wt += wt * abs(P["total"]) ** 2
                    Wc += wt * abs(P["contact"]) ** 2
                    Wtu += wt * abs(P["tu_channel"]) ** 2
    return Ws, Wt, Wc, Wtu


print("=== (1) s-channel (Maxwell on h^(2)) vs full tree amplitude, integrated over final phase space ===")
print("cases: (theta_deg, pol1, pol2): ratio R = int|M_s|^2 / int|M_full|^2 ; lab TT gauge for the waves")
for th, p1, p2 in [(180, "R", "L"), (90, "R", "R"), (90, "R", "L"), (180, "plus", "plus"),
                   (90, "plus", "plus"), (30, "plus", "plus"), (120, "R", "L")]:
    res = {}
    for nc in (24, 40):
        Ws, Wt, Wc, Wtu = integrals(math.radians(th), p1, p2, nc=nc, nph=nc)
        res[nc] = (Ws, Wt)
    Ws, Wt = res[40]
    rel = abs(res[40][1] - res[24][1]) / max(abs(res[40][1]), 1e-300)
    ratio = Ws / Wt if Wt > 1e-20 * max(Ws, 1e-300) else float("inf")
    print(f"theta={th:4d} {p1:>4s}/{p2:<4s}: int|M_s|^2={Ws:.4e}  int|M_full|^2={Wt:.4e}  ratio={ratio:.4g}"
          f"  (full-integral change 24->40 nodes: {rel:.1e})")

print()
print("=== (2) hbar scaling (SI) ===")
c = 2.99792458e8; G = 6.674e-11; hbar = 1.054571817e-34
w = 2 * PI * 150.0; h = 1e-21
for fac in (1.0, 2.0):
    hb = hbar * fac
    # eq. 8 with N = E/(hbar w) in SI: dP/dt = 3 (G hbar/c^5)^2 N^2 w^3 sigma^2/(25 pi)
    E = 1e47; sig = 0.1 * w
    N = E / (hb * w)
    R = 3 * (G * hb / c ** 5) ** 2 * N ** 2 * w ** 3 * sig ** 2 / (25 * PI)
    Wph = 2 * R * hb * w
    print(f"hbar x {fac}: eq.8 pair rate = {R:.6e} 1/s, photon power (unstimulated) = {Wph:.6e} W")
r = q2.beams_pair_rate_SI(w, h, PI)
closed = w ** 4 * h ** 4 * (1 - math.cos(PI)) ** 2 / (1280 * PI * c ** 3)
print(f"two-beam head-on plus/plus full-amplitude rate (tool, SI) = {r['pair_rate_SI']:.6e} /m^3/s;"
      f" closed form w^4 h^4 (1-cos)^2/(1280 pi c^3) = {closed:.6e} /m^3/s (no hbar, no G)")

print()
print("=== (3) Rayleigh-Jeans CMB occupation at GW frequencies (extrapolated) ===")
kB = 1.380649e-23; T = 2.7255
for f in (10.0, 150.0, 1e-3):
    fg = 1 / math.expm1(2 * PI * hbar * f / (kB * T))
    print(f"f = {f:g} Hz: f_gamma = {fg:.3e}; 1+2f = {1 + 2 * fg:.3e}; stimulated photon number scales as 1/hbar")
