#!/usr/bin/env python3
"""Task A(2), single graviton pair: how the helicity phases change sum_s |A|^2 relative to B&O's eq. 7 integrand
(s^2 - 2tu)^2/s^2 = (t^2 + u^2)^2/s^2, for definite physical polarisation states of ONE head-on pair.

B&O's eq. 7 per pair, written for unit-normalised polarisations f_l (H = sum_l f_l eps_l):
    A_BO(mu mu) = sum_l f_l(k1) f_l(k2) A^{eq.6}_{l l mu mu}, real amplitudes 8 pi G t^2/s, u^2/s, 2 photon states.
For a linear 'plus' state f_+ = f_- = 1/sqrt2 this is (1/2) 8 pi G (t^2 + u^2)/s per photon state.
Physical: module amplitude with the full tensors (cross-checked against the spinor closed form, bo_common).
G = 1, s = 4, gravitons along +z and -z in the CM."""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills", "conundrum", "scripts"))
import bo_common as bc  # noqa: E402
import qft_second_order as q2  # noqa: E402

PI = math.pi
s = 4.0
E = 1.0
qa, qb = np.array([E, 0, 0, E]), np.array([E, 0, 0, -E])

# pair states (graviton 1 along +z, graviton 2 along -z), unit-normalised tensors
states = {
    "B&O-literal pair (f+ = f- real, module convention = plus/plus aligned)":
        (bc.to4(bc.pattern("bo_plus", np.array([0, 0, 1.0]))) * math.sqrt(8 * PI) / math.sqrt(2),
         bc.to4(bc.pattern("bo_plus", np.array([0, 0, -1.0]))) * math.sqrt(8 * PI) / math.sqrt(2)),
    "plus (x) plus, aligned": (q2.graviton_polarization(qa, "plus"), q2.graviton_polarization(qb, "plus")),
    "plus (x) cross (45 deg)": (q2.graviton_polarization(qa, "plus"), q2.graviton_polarization(qb, "cross")),
    "R (x) L  (physical helicities +2, -2)": (q2.graviton_polarization(qa, 2), q2.graviton_polarization(qb, -2)),
    "R (x) R  (physical helicities +2, +2)": (q2.graviton_polarization(qa, 2), q2.graviton_polarization(qb, 2)),
}

nth, nph = 24, 64
x, wx = np.polynomial.legendre.leggauss(nth)
phis = (np.arange(nph) + 0.5) * 2 * PI / nph


def sum_s_M2(Ha, Hb, cth, ph, route="module"):
    sth = math.sqrt(1 - cth * cth)
    n = np.array([sth * math.cos(ph), sth * math.sin(ph), cth])
    k1, k2 = np.concatenate([[E], E * n]), np.concatenate([[E], -E * n])
    tot = 0.0
    for s1 in (1, -1):
        for s2 in (1, -1):
            e1, e2 = q2.photon_polarization(k1, s1), q2.photon_polarization(k2, s2)
            if route == "module":
                M = complex(q2.amplitude_gg_to_photons(qa, Ha, qb, Hb, k1, e1, k2, e2))
            else:
                M = complex(bc.photon_amp_general(qa, Ha, qb, Hb, k1, e1, k2, e2))
            tot += abs(M) ** 2
    return tot


def bo_pair(Ha, Hb, cth, reading="literal"):
    """B&O eq.-7 per pair: projections f_l = <eps_l, H> in the module's helicity basis, real eq.-6 amplitudes.
    reading 'literal': f_l(k1) f_l(k2) A_ll (coherent-state helicity label = amplitude label, as eq. 7 is written);
    reading 'axis'   : f_l(k1) f_-l(k2) A_ll (amplitude label = spin projection on the k1 axis, section 3 of A1)."""
    t = -s / 2 * (1 - cth)
    u = -s / 2 * (1 + cth)
    f = {}
    for lab, H, q in (("a", Ha, qa), ("b", Hb, qb)):
        for l in (2, -2):
            e = q2.graviton_polarization(q, l)
            f[(lab, l)] = np.einsum("mn,mn->", np.conj(e), H)     # spatial-only tensors: lower = upper
    fb = {2: f[("b", 2)], -2: f[("b", -2)]} if reading == "literal" else {2: f[("b", -2)], -2: f[("b", 2)]}
    amp_pp = 8 * PI * (f[("a", 2)] * fb[2] * t * t / s + f[("a", -2)] * fb[-2] * u * u / s)  # mu = ++
    amp_mm = 8 * PI * (f[("a", 2)] * fb[2] * u * u / s + f[("a", -2)] * fb[-2] * t * t / s)  # mu = --
    return abs(amp_pp) ** 2 + abs(amp_mm) ** 2


print("Per-pair comparison: physical sum_s |M|^2 vs B&O eq.-7 integrand (same pair, same normalisation).")
print("Columns: photon polar angle theta (from graviton 1); azimuthal average over phi of the physical value;")
print("min and max over phi; B&O value (phi independent).  Units (8 pi G)^2 = 1 removed.\n")
for name, (Ha, Hb) in states.items():
    print(f"--- {name}")
    phys_int, bo_int, bo_int2 = 0.0, 0.0, 0.0
    for cth, w in zip(x, wx):
        vals = np.array([sum_s_M2(Ha, Hb, cth, ph) for ph in phis[::2]]) / (8 * PI) ** 2
        phys_int += w * vals.mean()
        bo_int += w * bo_pair(Ha, Hb, cth) / (8 * PI) ** 2
        bo_int2 += w * bo_pair(Ha, Hb, cth, "axis") / (8 * PI) ** 2
    for cdeg in (30, 60, 90, 120):
        cth = math.cos(math.radians(cdeg)) + 1e-9
        vals = np.array([sum_s_M2(Ha, Hb, cth, ph) for ph in phis]) / (8 * PI) ** 2
        b = bo_pair(Ha, Hb, cth) / (8 * PI) ** 2
        b2 = bo_pair(Ha, Hb, cth, "axis") / (8 * PI) ** 2
        print(f"   theta={cdeg:3d}: phys <.>_phi = {vals.mean():.6f}  [min {vals.min():.6f}, max {vals.max():.6f}]"
              f"   B&O literal = {b:.6f}, B&O axis-reading = {b2:.6f}")
    rr = [f"{phys_int / v:.6f}" if v > 1e-12 else "n/a (B&O = 0)" for v in (bo_int, bo_int2)]
    print(f"   int dcos <.>_phi:  physical = {phys_int:.6f},  B&O literal = {bo_int:.6f} (phys/B&O = {rr[0]}),"
          f"  B&O axis-reading = {bo_int2:.6f} (phys/B&O = {rr[1]})")

# explicit cross-term structure for the aligned plus/plus pair
print("\nCross-term structure, aligned plus/plus pair: physical - [(t^4+u^4)/s^2]/2 (per (8 pi G)^2), Fourier in phi")
Ha, Hb = states["plus (x) plus, aligned"]
for cdeg in (40, 75, 110):
    cth = math.cos(math.radians(cdeg))
    t = -s / 2 * (1 - cth)
    u = -s / 2 * (1 + cth)
    vals = np.array([sum_s_M2(Ha, Hb, cth, ph) for ph in phis]) / (8 * PI) ** 2
    base = 0.5 * (t ** 4 + u ** 4) / s ** 2
    X = vals - base
    c = np.fft.rfft(X) / len(X)
    amp = 2 * np.abs(c)
    dom = int(np.argmax(amp[1:]) + 1)
    print(f"   theta={cdeg}: phi-mean of cross term = {X.mean():.2e};  dominant harmonic cos({dom} phi) with amplitude "
          f"{amp[dom]:.6f};  t^2 u^2/s^2 = {t*t*u*u/s**2:.6f};  B&O's cross term (1/2) 2 t^2u^2/s^2 = {t*t*u*u/s**2:.6f}")

# independent route for the same numbers
Ha, Hb = states["plus (x) plus, aligned"]
d = max(abs(sum_s_M2(Ha, Hb, c, p, "module") - sum_s_M2(Ha, Hb, c, p, "spinor")) / sum_s_M2(Ha, Hb, c, p, "module")
        for c in (0.3, -0.55) for p in (0.2, 1.7, 4.0))
print(f"\nspinor closed form vs module for these sums (max rel. diff): {d:.1e}")

# closed form for the angular-integrated ratio
from fractions import Fraction  # noqa: E402
# int_{-1}^{1} [(1-c)^4 + (1+c)^4] dc / int 4 (1+c^2)^2 dc  (t^4+u^4 vs (t^2+u^2)^2, common s^4/16)
num = Fraction(2 * 2) + Fraction(12 * 2, 3) + Fraction(2 * 2, 5)
den = 4 * (Fraction(2) + Fraction(4, 3) + Fraction(2, 5))
print(f"exact ratio int(t^4+u^4)/int(t^2+u^2)^2 over dcos = {num/den} = {float(num/den):.6f}")
