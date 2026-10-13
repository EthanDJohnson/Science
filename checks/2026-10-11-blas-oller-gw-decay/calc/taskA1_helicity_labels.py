#!/usr/bin/env python3
"""Task A(1): relation between Blas & Oller's eq. 6 helicity labels and PHYSICAL helicities; magnitudes 8 pi G t^2/s,
u^2/s; vanishing configurations.  Two independent routes:
  (i)  qft_second_order.helicity_amplitudes_cm (Feynman diagrams via background-field method; labels = physical
       helicities along each particle's own momentum);
  (ii) bo_common spinor-helicity closed form (KLT double copy), with polarisation vectors built from the same spinors,
       evaluated for the module's OWN physical polarisation tensors/vectors by projection.
Then: angular-momentum (J_z) bookkeeping that maps physical helicities to spin projections on a common axis, and a
rephasing-invariant test of whether eq. 6 can hold as REAL amplitudes in any phase convention.
G = 1, s = 4 (graviton energies 1 in the CM)."""
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
np.set_printoptions(linewidth=150)


def section(t):
    print("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)


# ------------------------------------------------------------------ 0. spinor sanity
section("0. spinor-route sanity (independent of the module)")
rng = np.random.default_rng(1)
P = rng.normal(size=(6, 3))
P = np.concatenate([np.linalg.norm(P, axis=1)[:, None], P], axis=1)
L = bc.lam(P)
err = 0.0
for i in range(6):
    for j in range(6):
        err = max(err, abs(abs(bc.ang(L[i], L[j])) ** 2 - 2 * bc.mdot(P[i], P[j])))
print(f"max | |<ij>|^2 - 2 p_i.p_j | over random null pairs: {err:.2e}")
ep, em = bc.pol_vectors(P)
print(f"max |eps.k| (+,-): {np.max(np.abs(bc.mdot(ep, P))):.2e} {np.max(np.abs(bc.mdot(em, P))):.2e};"
      f"  eps+.eps- = {np.round(bc.mdot(ep, em), 12)[:2]} ; |eps+.conj(eps+)| = {np.round(np.abs(bc.mdot(ep, np.conj(ep))), 12)[:2]}")
kz = np.array([1.0, 0, 0, 1.0])
epz, emz = bc.pol_vectors(kz)
# remove the gauge part along k: spatial transverse components
print("k along +z: transverse spatial parts (x, y) of eps^+ :", np.round(epz[1:3] / epz[1], 6),
      "  of eps^- :", np.round(emz[1:3] / emz[1], 6))
print("  -> eps^- has (x + i y) form = physical helicity +1 for an INCOMING particle (wavefunction e^{-ikx} eps);")
print("     as the conjugated vector of an OUTGOING particle, eps^- = conj(physical -1)  => label '-' = physical -1 out.")
print("     So: outgoing labels = physical helicities; an incoming graviton of physical helicity +2 fills a '--' slot.")

# ------------------------------------------------------------------ 1. module helicity amplitudes vs closed forms
section("1. module helicity_amplitudes_cm: |M|/(8 pi G) against t^2/s and u^2/s (physical helicities)")
s = 4.0
print("graviton 1 along +z (helicity l1 along +z), graviton 2 along -z (helicity l2 along -z); photon 1 at (theta, phi).")
print("t = (k_g1 - q_gam1)^2, u = (k_g1 - q_gam2)^2  (B&O's definitions with their letters).")
rows = []
for th_deg, ph_deg in ((30, 0), (75, 40), (120, 200), (160, 310)):
    th, ph = math.radians(th_deg), math.radians(ph_deg)
    t = -s / 2 * (1 - math.cos(th))
    u = -s / 2 * (1 + math.cos(th))
    amps = q2.helicity_amplitudes_cm(s, th, ph, final="photon")
    print(f"\n theta = {th_deg} deg, phi = {ph_deg} deg:  t^2/s = {t*t/s:.6f}, u^2/s = {u*u/s:.6f}")
    for key in sorted(amps, key=lambda k: (-k[0], -k[1], -k[2], -k[3])):
        a = abs(amps[key]) / (8 * PI)
        tag = ""
        if a > 1e-12:
            tag = "= t^2/s" if abs(a - t * t / s) < 1e-10 else ("= u^2/s" if abs(a - u * u / s) < 1e-10 else "??")
        rows.append((key, a, tag))
        print(f"   (l1,l2,s1,s2) = {key}:  |M|/(8 pi G) = {a:.6e} {tag}")

# ------------------------------------------------------------------ 2. spinor closed form vs module, full complex amplitudes
section("2. independent spinor closed form vs module: complex ratio over all 16 helicity configs and kinematic points")
ratios = []
for th_deg, ph_deg in ((30, 0), (75, 40), (120, 200), (160, 310), (95, 123)):
    th, ph = math.radians(th_deg), math.radians(ph_deg)
    E = 1.0
    qa, qb = np.array([E, 0, 0, E]), np.array([E, 0, 0, -E])
    n = np.array([math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th)])
    k1, k2 = np.concatenate([[E], E * n]), np.concatenate([[E], -E * n])
    for l1 in (2, -2):
        for l2 in (2, -2):
            Ha, Hb = q2.graviton_polarization(qa, l1), q2.graviton_polarization(qb, l2)
            for s1 in (1, -1):
                for s2 in (1, -1):
                    e1, e2 = q2.photon_polarization(k1, s1), q2.photon_polarization(k2, s2)
                    Mm = complex(q2.amplitude_gg_to_photons(qa, Ha, qb, Hb, k1, e1, k2, e2))
                    Ms = complex(bc.photon_amp_general(qa, Ha, qb, Hb, k1, e1, k2, e2))
                    if abs(Mm) > 1e-9 or abs(Ms) > 1e-9:
                        ratios.append(Mm / Ms)
                    else:
                        ratios.append(None)
nz = np.array([r for r in ratios if r is not None])
print(f"nonzero configurations: {len(nz)} of {len(ratios)} (both routes zero for the rest: "
      f"{all(r is None for r in ratios if r is None)})")
print(f"ratio module/spinor: mean = {np.mean(nz):.12f}, max |ratio - mean| = {np.max(np.abs(nz - np.mean(nz))):.2e}")

# random general kinematics, random complex TT tensors and random photon polarisations (lab frame, not CM)
section("2b. same test for RANDOM lab kinematics, random complex TT graviton tensors, random photon polarisations")


def random_tt(k, rng):
    A = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    A = A + A.T
    n = k[1:] / np.linalg.norm(k[1:])
    return bc.to4(bc.tt_project(n, A))


def random_photon_pol(q, rng):
    n = q[1:] / np.linalg.norm(q[1:])
    et, ep = bc.frame(n)
    c = rng.normal(size=2) + 1j * rng.normal(size=2)
    return np.concatenate([[0], c[0] * et + c[1] * ep])


rat = []
for trial in range(200):
    Kv = rng.normal(size=3) * 0.6
    Kmag = np.linalg.norm(Kv)
    if Kmag > 1.9:
        continue
    al = rng.uniform(0, 2 * PI, size=1)
    cth = rng.uniform(-1, 1, size=1)
    ph = rng.uniform(0, 2 * PI, size=1)
    k1, k2, Q1, Q2, s_, _ = bc.ring_and_photons(Kmag, Kv / Kmag, al, cth, ph)
    k1, k2, Q1, Q2 = k1[0], k2[0], Q1[0], Q2[0]
    H1, H2 = random_tt(k1, rng), random_tt(k2, rng)
    e1, e2 = random_photon_pol(Q1, rng), random_photon_pol(Q2, rng)
    try:
        Mm = complex(q2.amplitude_gg_to_photons(k1, H1, k2, H2, Q1, e1, Q2, e2))
    except ValueError:
        continue
    Ms = complex(bc.photon_amp_general(k1, H1, k2, H2, Q1, e1, Q2, e2))
    rat.append(Mm / Ms)
rat = np.array(rat)
print(f"{len(rat)} random configurations: ratio module/spinor mean = {np.mean(rat):.12f}, "
      f"max |ratio - mean| = {np.max(np.abs(rat - np.mean(rat))):.2e}")
print("=> the module's FULL multilinear amplitude (all phases) equals the KLT closed form up to one global constant.")

# ------------------------------------------------------------------ 3. J_z bookkeeping and B&O labels
section("3. mapping physical helicities to spin projections on a common axis (B&O's eq. 6 labels)")
print("Head-on CM: J along +z of the graviton pair = l1 - l2 (graviton 2 moves along -z).")
print("Photon pair along n: J along n = s1 - s2.  Nonzero physical configurations found above:")
th, ph = math.radians(75), math.radians(40)
amps = q2.helicity_amplitudes_cm(s, th, ph, final="photon")
t = -s / 2 * (1 - math.cos(th))
u = -s / 2 * (1 + math.cos(th))
for key, val in sorted(amps.items(), key=lambda kv: (-kv[0][0], -kv[0][1], -kv[0][2], -kv[0][3])):
    a = abs(val) / (8 * PI)
    if a < 1e-12:
        continue
    l1, l2, s1, s2 = key
    Jg, Jp = l1 - l2, s1 - s2                     # spin projections on the common axes
    lab_g = "++" if Jg > 0 else ("--" if Jg < 0 else "+-")
    lab_p1 = "++" if Jp > 0 else ("--" if Jp < 0 else "+-")    # photon axis = photon 1 direction
    lab_p2 = "--" if Jp > 0 else ("++" if Jp < 0 else "+-")    # photon axis = photon 2 direction
    which = "t^2/s" if abs(a - t * t / s) < 1e-10 else "u^2/s"
    print(f"  physical (l1,l2,s1,s2) = {key}:  J_z(gg) = {l1 - l2:+d}, J_n(gamma gamma) = {s1 - s2:+d};"
          f"  |M|/(8 pi G) = {which};  common-axis label (g-axis k1, photon axis q1): A_{lab_g}{lab_p1};"
          f"  (g-axis k1, photon axis q2): A_{lab_g}{lab_p2}")
print("B&O eq. 6: A++++ = A---- = 8 pi G t^2/s,  A++-- = A--++ = 8 pi G u^2/s, others zero.")
print("Physical-helicity reading of B&O's labels: A++++ would be (l1,l2,s1,s2) = (2,2,1,1): module |M| =",
      f"{abs(amps[(2, 2, 1, 1)]):.1e} (zero) -> that reading is refuted.")
print("Common-axis reading: magnitudes and zeros match; with the graviton axis along k1 and the photon axis along q2")
print("(or along k2 and q1) the t/u assignment is exactly B&O's; with axes (k1, q1) t and u are interchanged,")
print("which only relabels the two photons and cannot change any integrated rate.")

# ------------------------------------------------------------------ 4. can eq. 6 hold as REAL amplitudes in some convention?
section("4. rephasing-invariant phases: can all eq.-6 amplitudes be made real & positive by a choice of conventions?")
print("For fixed photons (q1, q2) and two graviton axes a, a' on the ring k1 + k2 = q1 + q2 (same K), the product")
print("  I(a, a') = M_a(+2,-2 -> +1,-1) M_a(+2,-2 -> -1,+1)^* M_a'(+2,-2 -> -1,+1) M_a'(+2,-2 -> +1,-1)^*")
print("is invariant under every rephasing of graviton and photon helicity states. Eq. 6 as real positive numbers")
print("would force arg I = 0 for all a, a'.")
E = 1.0
Kz = 0.0
for th_deg, ph_deg in ((60, 17), (60, 45), (100, 10)):
    th, ph = math.radians(th_deg), math.radians(ph_deg)
    n = np.array([math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th)])
    Q1, Q2 = np.concatenate([[E], E * n]), np.concatenate([[E], -E * n])
    out = []
    for adeg in (0, 30, 60, 90):
        a = math.radians(adeg)
        # graviton axis in the plane perpendicular to the CM z axis? use a general axis tilted by a about x
        d = np.array([math.sin(a), 0.0, math.cos(a)])
        k1, k2 = np.concatenate([[E], E * d]), np.concatenate([[E], -E * d])
        Hp, Hm = q2.graviton_polarization(k1, 2), q2.graviton_polarization(k2, -2)
        Mpm = complex(q2.amplitude_gg_to_photons(k1, Hp, k2, Hm, Q1, q2.photon_polarization(Q1, 1), Q2,
                                                 q2.photon_polarization(Q2, -1)))
        Mmp = complex(q2.amplitude_gg_to_photons(k1, Hp, k2, Hm, Q1, q2.photon_polarization(Q1, -1), Q2,
                                                 q2.photon_polarization(Q2, 1)))
        out.append((adeg, Mpm * np.conj(Mmp)))
    base = out[0][1]
    print(f"  photons at theta={th_deg}, phi={ph_deg}:  arg I(a=0, a') for a' tilted by "
          + ", ".join(f"{adeg} deg: {math.degrees(np.angle(np.conj(v) * base)):+8.2f}" for adeg, v in out[1:]))
print("=> nonzero rephasing-invariant phases: no phase convention makes all eq.-6 amplitudes real and positive at once;")
print("   eq. 6 is correct for the MAGNITUDES only, and a coherent sum over different graviton pairs (eq. 7) needs the")
print("   phases.")
