#!/usr/bin/env python3
"""Task A(4): scalar channel g g -> phi phi (B&O supplementary SD).
 (1) eq. S10 helicity amplitudes vs qft_second_order (massive, minimally coupled real scalar), label/crossing
     conventions; massless amplitude also vs the independent spinor closed form (bo_common).
 (2) B&O's model (real S10 amplitudes summed at amplitude level as in eq. 7, isotropic top-hat, eq.-S6 machinery):
     does the massless-limit coefficient 7/(450 pi) follow?  Does eq. S11 (finite m, N_phi = 0) follow, and for which
     way of combining the same- and opposite-helicity amplitudes?
 (3) physical coherent states (as in taskA3b) for massless scalars.
Real scalar: identical particles, factor 1/2 in the final phase space (as for photons). G = 1, omega_s = 1.
Usage: --part {amps, bo, physical}"""
import argparse
import math
import os
import sys
import time

import numpy as np
from scipy import integrate

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills", "conundrum", "scripts"))
import bo_common as bc  # noqa: E402
import bo_ring as br  # noqa: E402
import qft_second_order as q2  # noqa: E402

PI = math.pi
REF = 7 / (450 * PI)
ap = argparse.ArgumentParser()
ap.add_argument("--part", required=True, choices=["amps", "bo", "physical"])
a = ap.parse_args()

if a.part == "amps":
    print("(1) |module| vs eq. S10 magnitudes, labels = PHYSICAL helicities (l1 along graviton 1, l2 along graviton 2)")
    print("    S10: A++ = A-- = -8 pi G m^4 s/((t-m^2)(u-m^2)),  A+- = A-+ = -8 pi G (m^4 - t u)^2/(s (t-m^2)(u-m^2))")
    worst = {"same": 0.0, "opp": 0.0}
    for s, m in ((4.0, 0.3), (4.0, 0.9), (10.0, 1.2), (3.0, 0.1)):
        for th_deg, ph_deg in ((20, 0), (70, 33), (125, 250)):
            th, ph = math.radians(th_deg), math.radians(ph_deg)
            amps = q2.helicity_amplitudes_cm(s, th, ph, final="scalar", m=m)
            E = math.sqrt(s) / 2
            p = math.sqrt(E * E - m * m)
            t = m * m - 2 * (E * E - E * p * math.cos(th))      # (k_g1 - p_1)^2 = m^2 - 2 k.p
            u = m * m - 2 * (E * E + E * p * math.cos(th))
            same = 8 * PI * m ** 4 * s / abs((t - m * m) * (u - m * m))
            opp = 8 * PI * (m ** 4 - t * u) ** 2 / (s * abs((t - m * m) * (u - m * m)))
            r_same = [abs(amps[(2, 2)]) / same, abs(amps[(-2, -2)]) / same]
            r_opp = [abs(amps[(2, -2)]) / opp, abs(amps[(-2, 2)]) / opp]
            worst["same"] = max(worst["same"], max(abs(x - 1) for x in r_same))
            worst["opp"] = max(worst["opp"], max(abs(x - 1) for x in r_opp))
            print(f"   s={s}, m={m}, theta={th_deg}: |M(+2,+2)|/S10_same = {r_same[0]:.12f}, |M(+2,-2)|/S10_opp = {r_opp[0]:.12f}")
    print(f"   max deviation: same-helicity {worst['same']:.1e}, opposite-helicity {worst['opp']:.1e}")
    print("   => S10 magnitudes confirmed with A++ = physical SAME helicities (J_z = 0 head-on; the m^4 amplitude, nonzero")
    print("      in the forward direction) and A+- = physical OPPOSITE helicities (J_z = +-4; (m^4 - tu)^2 vanishes at theta = 0, pi).")
    th = 1e-3
    for (l1, l2) in ((2, 2), (2, -2)):
        v = abs(q2.helicity_amplitudes_cm(4.0, th, 0.0, final="scalar", m=0.5)[(l1, l2)]) / (8 * PI)
        print(f"   J_z check at theta = 1e-3 (s = 4, m = 0.5): |M({l1},{l2})|/(8 pi G) = {v:.3e}")
    # crossing: Compton phi g -> phi g with incoming graviton helicity +2 and outgoing helicity lf
    print("\n   crossing convention: gravitational Compton phi(p) g(k, +2) -> phi(p') g(k', lf), m = 1, omega = 0.7, lab:")
    m, w, thc = 1.0, 0.7, math.radians(70)
    wf = w / (1 + 2 * w / m * math.sin(thc / 2) ** 2)
    pin, qin = np.array([m, 0, 0, 0.0]), np.array([w, 0, 0, w])
    qout = wf * np.array([1.0, math.sin(thc), 0, math.cos(thc)])
    pout = pin + qin - qout
    sC = float(bc.mdot(pin + qin, pin + qin))
    tC = float(bc.mdot(qin - qout, qin - qout))
    uC = float(bc.mdot(qin - pout, qin - pout))
    # crossing to g(k) g(-k') -> phi(-p) phi(p'): s_x = t_C, t_x = (k - p')^2 = u_C, u_x = (k + p)^2 = s_C
    sx, tx, ux = tC, uC, sC
    same_x = m ** 4 * abs(sx) / abs((tx - m * m) * (ux - m * m))
    opp_x = (m ** 4 - tx * ux) ** 2 / abs(sx * (tx - m * m) * (ux - m * m))
    for lf in (2, -2):
        M = q2.compton_amplitude("scalar", pin, qin, q2.graviton_polarization(qin, 2), pout, qout,
                                 q2.graviton_polarization(qout, lf), m=m)
        print(f"      lf = {lf:+d}: |M|/(8 pi G) = {abs(complex(M))/(8*PI):.9f}")
    print(f"      S10 crossed (s,t,u)_gg = (t_C, u_C, s_C): same-helicity form = {same_x:.9f},"
          f" opposite-helicity form = {opp_x:.9f}")
    print("      => Compton helicity FLIP (+2 -> -2) = the S10 m^4 ('A++') form; crossing the outgoing graviton to an")
    print("      incoming one reverses its helicity, so the flip becomes gg -> phi phi with SAME physical helicities.")
    print("      Hence B&O's A^t_{++} (m^4) is labelled by the physical helicities of the two INCOMING gravitons, not by")
    print("      the (in, out) labels of the Compton amplitude it was crossed from - unlike eq. 6, whose nonzero labels")
    print("      only make sense as spin projections on a common axis (taskA1).")
    # massless: module vs spinor closed form, random configurations and tensors
    rng = np.random.default_rng(3)
    rat = []
    for _ in range(150):
        Kv = rng.normal(size=3) * 0.6
        Km = np.linalg.norm(Kv)
        if Km > 1.9:
            continue
        k1, k2, Q1, Q2, s_, _ = bc.ring_and_photons(Km, Kv / Km, rng.uniform(0, 2 * PI, 1), rng.uniform(-1, 1, 1),
                                                    rng.uniform(0, 2 * PI, 1))
        k1, k2, Q1, Q2 = k1[0], k2[0], Q1[0], Q2[0]
        Hs = []
        for k in (k1, k2):
            A = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
            Hs.append(bc.to4(bc.tt_project(k[1:] / np.linalg.norm(k[1:]), A + A.T)))
        Mm = complex(q2.amplitude_gg_to_scalars(k1, Hs[0], k2, Hs[1], Q1, Q2, 0.0))
        Ms = complex(bc.scalar_amp_general(k1, Hs[0], k2, Hs[1], Q1, Q2))
        rat.append(Mm / Ms)
    rat = np.array(rat)
    print(f"\n   massless scalar, {len(rat)} random configurations and random complex TT tensors: module/spinor mean ="
          f" {np.mean(rat):.12f}, max |ratio - mean| = {np.max(np.abs(rat - np.mean(rat))):.1e}")

if a.part == "bo":
    import sympy as sp
    print("(2a) B&O model, massless scalar, symbolic: amplitude-level sum (1/2) sum_{l1 l2} f f A_{l1 l2} with S10 at m=0")
    th, ph, al, K, w = sp.symbols("theta phi alpha K omega", positive=True)
    s = 4 - K ** 2
    cc = sp.sin(th) * sp.cos(ph - al)
    # photons: (t^2+u^2)/s = (s/2)(1 + c^2) per photon state, 2 states;   scalars: 2 x tu/s = (s/2)(1 - c^2), 1 state
    ring_ph = sp.integrate((s / 2) * (1 + cc ** 2), (al, 0, 2 * sp.pi))
    ring_sc = sp.integrate((s / 2) * (1 - cc ** 2), (al, 0, 2 * sp.pi))
    Iph = 2 * sp.integrate(sp.integrate(sp.expand(ring_ph ** 2) * sp.sin(th), (th, 0, sp.pi)), (ph, 0, 2 * sp.pi))
    Isc = sp.integrate(sp.integrate(sp.expand(ring_sc ** 2) * sp.sin(th), (th, 0, sp.pi)), (ph, 0, 2 * sp.pi))
    ratio = sp.simplify(sp.integrate(Isc, (K, 0, 2)) / sp.integrate(Iph, (K, 0, 2)))
    print(f"    scalar/photon rate ratio in the B&O model = {ratio};  x 3/(25 pi) = {sp.nsimplify(ratio*sp.Rational(3,25))}/pi"
          f"  (B&O: 7/(450 pi); tau_phi = (54/7) tau)")
    Cn = br.coefficient(lambda k1, k2, Q1, Q2, s_: br.m_scalar_bo(k1, k2, Q1, Q2, s_, "bo_plus", 0.0),
                        NK=8, NthK=4, nth=8, nph=16, na=32)
    print(f"    numerical ring engine, B&O model, m = 0: C = {Cn:.12f};  7/(450 pi) = {REF:.12f};  ratio = {Cn/REF:.12f}")

    print("\n(2b) eq. S11 vs the B&O-model ring integral at finite m (N_phi = 0), coefficient of G^2 N^2 omega^3 sigma^2")

    def S11_bracket(s, m):
        sig = math.sqrt(max(1 - 4 * m * m / s, 0.0))
        if m == 0:
            return s ** 1.5 * sig * 7 * s * s
        arccot = math.atan(math.sqrt(s - 4 * m * m) / (2 * m))
        return (s ** 1.5 * sig * (912 * m ** 4 - 136 * m * m * s + 7 * s * s) + 7680 * m ** 7 * arccot
                + 480 * m ** 4 * (s - 14 * m * m) * math.sqrt(s) * math.asinh(math.sqrt(s / (4 * m * m) - 1)))

    def S11_C(m):
        # ds/(s^{3/2} sqrt(4 - s)) with s = 4 - K^2: = 2 dK / s^{3/2}
        f = lambda Kk: 2 * S11_bracket(4 - Kk * Kk, m) / (4 - Kk * Kk) ** 1.5  # noqa: E731
        val, _ = integrate.quad(f, 0, 2 * math.sqrt(1 - m * m), limit=200, epsabs=0, epsrel=1e-11)
        return val / (15360 * PI)

    print(f"    m = 0: S11 coefficient = {S11_C(0.0):.12f}  (7/(450 pi) = {REF:.12f})")
    for m in (0.1, 0.3, 0.5, 0.7, 0.9):
        res = {}
        for combo in ("coherent", "opp_only", "same_only"):
            res[combo], Ks, jK = br.coefficient(
                lambda k1, k2, Q1, Q2, s_, combo=combo, m=m: br.m_scalar_bo(k1, k2, Q1, Q2, s_, "bo_plus", m, combo),
                NK=24, NthK=4, nth=16, nph=24, na=48, m=m, return_K=True)
            if combo == "coherent":
                jK_coh = jK
        inc = res["opp_only"] + res["same_only"]
        cs = S11_C(m)
        # pointwise check of the K integrand at three nodes
        pts = []
        for i in (2, 11, 20):
            Kk = Ks[i]
            pts.append(jK_coh[i] / (2 * S11_bracket(4 - Kk * Kk, m) / (4 - Kk * Kk) ** 1.5 / (15360 * PI)))
        print(f"    m = {m}: S11 = {cs:.6e} | B&O-model coherent (A++ + A+-) = {res['coherent']:.6e} (ratio {res['coherent']/cs:.6f})"
              f" | opposite only = {res['opp_only']:.6e} | same only = {res['same_only']:.6e} |"
              f" incoherent sum = {inc:.6e} (ratio {inc/cs:.6f}) | pointwise dC/dK ratio coherent/S11 at 3 K nodes:"
              f" {', '.join(f'{x:.6f}' for x in pts)}")

if a.part == "physical":
    print("(3) physical coherent states, massless scalar (spinor engine; module cross-check on a coarse grid)")
    for pat, kw, grids in (
            ("bo_plus", dict(c_pole=16), (dict(NK=8, NthK=8, nth=8, nph=24, na=32),
                                          dict(NK=10, NthK=12, nth=8, nph=24, na=32))),
            ("binary", dict(splitK=False), (dict(NK=8, NthK=8, nth=8, nph=24, na=32),
                                            dict(NK=12, NthK=12, nth=10, nph=32, na=48))),
            ("linear", dict(splitK=False), (dict(NK=8, NthK=8, nth=8, nph=24, na=32),
                                            dict(NK=12, NthK=12, nth=10, nph=32, na=48))),
            ("circ", dict(c_pole=4), (dict(NK=4, NthK=4, nth=4, nph=8, na=16),))):
        for g in grids:
            t0 = time.time()
            C = br.coefficient(lambda k1, k2, Q1, Q2, s_: br.m_scalar_physical(k1, k2, Q1, Q2, s_, pat), **g, **kw)
            print(f"   {pat} grid {g}: C = {C:.8e};  C/(7/(450 pi)) = {C/REF:.6f}   [{time.time()-t0:.0f} s]")
    Cbo = br.coefficient(lambda k1, k2, Q1, Q2, s_: br.m_scalar_bo(k1, k2, Q1, Q2, s_, "linear", 0.0),
                         NK=16, NthK=16, nth=10, nph=32, na=64, splitK=False)
    print(f"   B&O model with the linear-quadrupole profile: C = {Cbo:.8e} (C/(7/(450 pi)) = {Cbo/REF:.6f})")
    g = dict(NK=3, NthK=3, nth=3, nph=8, na=16, c_alpha=4.0)
    for pat, kw in (("bo_plus", dict(c_pole=4)), ("binary", dict(splitK=False))):
        Cs = br.coefficient(lambda k1, k2, Q1, Q2, s_: br.m_scalar_physical(k1, k2, Q1, Q2, s_, pat), **g, **kw)
        Cm = br.coefficient(lambda k1, k2, Q1, Q2, s_: br.m_scalar_physical_module(k1, k2, Q1, Q2, s_, pat), **g, **kw)
        print(f"   module cross-check, identical coarse grid, {pat}: spinor {Cs:.12e}, module {Cm:.12e}, rel. diff {abs(Cs/Cm-1):.1e}")
