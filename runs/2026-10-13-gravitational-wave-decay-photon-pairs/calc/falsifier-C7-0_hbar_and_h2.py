#!/usr/bin/env python3
"""Falsifier C7-0 (physics). Two checks of C7's core and of its stated decisive test.

(1) hbar counting (SI) of B&O eq. 8 and of the two-beam pair rate: pair number hbar-free?
(2) C7's mechanism / decisive test: is the pair yield 'photon-vacuum pair creation on the
    second-order metric h^(2)' (a linear-response, Redi-Tesi-type functional fed with h^(2)),
    or does it need the contact and photon-exchange (t/u) pieces of the O(h^2) background-field
    amplitude? Uses qft_second_order (tree-level Einstein-Maxwell, every diagram) and
    qft_production Part D (first-order-in-background pair yield, fed with dg2 = s-channel).
Units: natural (hbar = c = 1) for amplitudes and beam rates in units of omega; SI where stated.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
import qft_second_order as q2
import qft_production as qp

print("=== (1) hbar counting, SI ===")
G, hbar, c, E, w, sig, h, th = sp.symbols("G hbar c E omega sigma h theta", positive=True)
Gnat = G / (hbar * c**5)                 # 1/J^2
N = E / (hbar * w)
rate_eq8 = sp.Rational(3, 25) / sp.pi * Gnat**2 * N**2 * (hbar * w)**3 * (hbar * sig)**2 / hbar   # 1/s
rate_eq8 = sp.simplify(rate_eq8)
print("eq.8 pair rate (SI):", rate_eq8, "  d ln R / d ln hbar =", sp.simplify(hbar * sp.diff(rate_eq8, hbar) / rate_eq8))
# two-beam kinetic rate: n = c^2 w h^2/(32 pi G hbar), sigma_lin = (2/5) pi Gnat^2 s (hbar c)^2, s = 2 (hbar w)^2 (1-cos th)
n = c**2 * w * h**2 / (32 * sp.pi * G * hbar)
s = 2 * (hbar * w)**2 * (1 - sp.cos(th))
sigma_lin = sp.Rational(2, 5) * sp.pi * Gnat**2 * s * (hbar * c)**2
Gam = sp.simplify(n**2 * sigma_lin * c * (1 - sp.cos(th)))
print("two-beam pair rate per volume (SI):", Gam)
print("  equals w^4 h^4 (1-cos)^2/(1280 pi c^3):", sp.simplify(Gam - w**4 * h**4 * (1 - sp.cos(th))**2 / (1280 * sp.pi * c**3)) == 0)
print("  d ln Gamma / d ln hbar =", sp.simplify(hbar * sp.diff(Gam, hbar) / Gam),
      "; d ln Gamma / d ln G =", sp.simplify(G * sp.diff(Gam, G) / Gam))

print("\n=== (1b) numerical: full tree-level beam rate vs closed form, and G-independence at fixed strain ===")
hh = 1e-3
for thd in (30, 90, 150, 180):
    t_ = math.radians(thd)
    full = q2.beams_pair_rate(1.0, hh, 1.0, hh, t_, "plus", "plus")["pair_rate"]
    fullG = q2.beams_pair_rate(1.0, hh, 1.0, hh, t_, "plus", "plus", G=1e-3)["pair_rate"]
    cf = hh**4 * (1 - math.cos(t_))**2 / (1280 * math.pi)
    print(f"plus/plus th={thd:3d} deg: full={full:.6e}  closed={cf:.6e}  ratio={full/cf:.12f}  G=1e-3/G=1: {fullG/full:.12f}")

print("\n=== (2) pair creation on h^(2) alone (Part D fed with dg2 = s-channel) vs the full O(h^2) amplitude ===")
def partD_dg2(pa, pb, t_):
    A_, B_ = q2._beams(1.0, hh, 1.0, hh, t_, pa, pb, 1.0)
    so = q2.second_order_metric(A_["q"], A_["H"], B_["q"], B_["H"])
    X2, X0 = qp._metric_weights(*[np.array([cc]) for cc in so["K"]], so["dg2"][None])
    r2, r0 = qp.stress_spectral_densities([so["s"]], "photon")
    return float(0.25 * (r2[0] * X2[0] + r0[0] * X0[0]))

rows = [("R", "R", 90), ("R", "L", 180), ("R", "L", 90), ("R", "L", 30),
        ("plus", "plus", 30), ("plus", "plus", 90), ("plus", "plus", 180),
        ("plus", "cross", 90), ("plus", "cross", 180)]
for pa, pb, thd in rows:
    t_ = math.radians(thd)
    full = q2.beams_pair_rate(1.0, hh, 1.0, hh, t_, pa, pb)["pair_rate"]
    pd = partD_dg2(pa, pb, t_)
    ref = q2.beams_pair_rate(1.0, hh, 1.0, hh, t_, "R", "L")["pair_rate"]
    ratio = (pd / full) if full > 1e-20 * ref else float("inf") if pd > 1e-20 * ref else float("nan")
    print(f"{pa:>5}/{pb:<5} th={thd:3d}: full={full/ref:.4e} x RL  h2-only={pd/ref:.4e} x RL  h2-only/full={ratio:.4g}")

print("\n=== (2b) gauge dependence of the h^(2)-only piece: shift eps1 -> eps1 + q1 xi + xi q1 ===")
rng = np.random.default_rng(1)
Mcm = 1.0
q1 = np.array([1.0, 0.0, 0.0, 1.0]); q2v = np.array([1.0, 0.0, 0.0, -1.0])
e1 = q2.graviton_polarization(q1, "R"); e2 = q2.graviton_polarization(q2v, "L")
k1 = np.array([1.0, math.sin(0.7), 0.0, math.cos(0.7)]); k2 = np.array([1.0, -math.sin(0.7), 0.0, -math.cos(0.7)])
p1 = q2.photon_polarization(k1, +1); p2 = q2.photon_polarization(k2, -1)
xi = np.array([0.0, 0.3, -0.2, 0.0])  # q1.xi = 0 (q1 along z, xi transverse)
eta = np.diag([1.0, -1.0, -1.0, -1.0])
q1l, xil = eta @ q1, eta @ xi
e1s = e1 + 0.5 * (np.outer(q1l, xil) + np.outer(xil, q1l))
P0 = q2.amplitude_gg_to_photons(q1, e1, q2v, e2, k1, p1, k2, p2, parts=True)
P1 = q2.amplitude_gg_to_photons(q1, e1s, q2v, e2, k1, p1, k2, p2, parts=True)
print("parts (unshifted):", P0)
print("parts (shifted)  :", P1)
