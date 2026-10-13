"""Mechanist lens: physical helicity amplitudes of g g -> gamma gamma (tree, Einstein-Maxwell) with phases,
and what B&O eq. 7's equal-sign 'unpolarized coherent' sum does to the pair yield.

Natural units hbar = c = 1, G = 1 (amplitudes quoted in units of 8 pi G s). CM frame: graviton 1 along +z,
graviton 2 along -z, each with PHYSICAL helicity w.r.t. its own momentum (toolkit graviton_polarization).
Photon 1 at polar angle th, azimuth ph. Mandelstam t = (q1-k1)^2 = -s(1-cos th)/2, u = -s(1+cos th)/2.
Independent route: compare |M| with B&O eq. 6 magnitudes 8 pi G t^2/s and 8 pi G u^2/s (Bjerrum-Bohr et al. via D-01).
"""
import math
import sys

import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import qft_second_order as q2  # noqa: E402

PI = math.pi
G = 1.0
s = 4.0           # E = 1 per graviton
E = 1.0
q1 = np.array([E, 0, 0, E])
qq2 = np.array([E, 0, 0, -E])


def photons(th, ph):
    n = np.array([math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th)])
    k1 = np.concatenate([[E], E * n])
    k2 = np.concatenate([[E], -E * n])
    return k1, k2


def amp(l1, l2, h1, h2, th, ph):
    k1, k2 = photons(th, ph)
    e1 = q2.graviton_polarization(q1, l1)
    e2 = q2.graviton_polarization(qq2, l2)
    p1 = q2.photon_polarization(k1[1:], h1)
    p2 = q2.photon_polarization(k2[1:], h2)
    return complex(q2.amplitude_gg_to_photons(q1, e1, qq2, e2, k1, p1, k2, p2, G=G))


print("Part 1: helicity amplitudes, CM frame, s = 4 (natural units), unit 8 pi G s")
print("graviton helicities (l1, l2) physical along own momentum; photon helicities (h1, h2) physical")
th, ph = 1.1, 0.7
t = -s * (1 - math.cos(th)) / 2
u = -s * (1 + math.cos(th)) / 2
print(f"th = {th} rad, ph = {ph} rad: t^2/s^2 = {t*t/s/s:.6f}, u^2/s^2 = {u*u/s/s:.6f}")
norm = 8 * PI * G * s
for l1 in (2, -2):
    for l2 in (2, -2):
        for h1 in (1, -1):
            for h2 in (1, -1):
                a = amp(l1, l2, h1, h2, th, ph) / norm
                print(f"  (l1,l2)=({l1:+d},{l2:+d}) (h1,h2)=({h1:+d},{h2:+d}): |M|/(8piG s) = {abs(a):.6f}"
                      f"  arg = {math.degrees(math.atan2(a.imag, a.real)) if abs(a) > 1e-12 else float('nan'):8.2f} deg")

print("\nPhase dependence on photon azimuth ph (opposite-helicity gravitons +2,-2):")
for php in (0.0, 0.7, 1.4, 2.1):
    for (h1, h2) in ((1, 1), (-1, -1), (1, -1), (-1, 1)):
        a = amp(2, -2, h1, h2, th, php) / norm
        if abs(a) > 1e-12:
            print(f"  ph={php:.1f} (h1,h2)=({h1:+d},{h2:+d}) |M|={abs(a):.6f} arg={math.degrees(math.atan2(a.imag, a.real)):8.2f} deg")

# Part 2: angular integrals, per unit (8 pi G)^2, over cos(th) of the CM photon direction (ph-independent magnitudes)
print("\nPart 2: final-state structure. For opposite-helicity gravitons the t^2 and u^2 amplitudes go to")
print("DIFFERENT final photon helicity states (orthogonal), so they cannot interfere in sum_final |M|^2.")
cs = np.linspace(-1, 1, 20001)
tt = (1 - cs) / 2      # |t|/s
uu = (1 + cs) / 2      # |u|/s
inc = np.trapezoid(tt ** 4 + uu ** 4, cs)          # sum of squares (physical, any single helicity pair +-)
bo = np.trapezoid((tt ** 2 + uu ** 2) ** 2, cs)    # B&O eq. 7 equal-sign coherent square
print(f"  int dcos (t^4+u^4)/s^4 = {inc:.6f} (exact 4/5)")
print(f"  int dcos (t^2+u^2)^2/s^4 = {bo:.6f} (exact 14/15)")
print(f"  ratio B&O-coherent / physical incoherent = {bo/inc:.6f} (exact 7/6)")

# check physical: sum over final helicities of |M|^2 for (+2,-2), integrated, vs inc
def sumfinal(l1, l2, th, ph):
    return sum(abs(amp(l1, l2, h1, h2, th, ph)) ** 2 for h1 in (1, -1) for h2 in (1, -1)) / norm ** 2

ths = np.linspace(0.02, PI - 0.02, 61)
vals = np.array([sumfinal(2, -2, x, 0.3) for x in ths])
pred = ((1 - np.cos(ths)) / 2) ** 4 + ((1 + np.cos(ths)) / 2) ** 4
print(f"  toolkit sum_final |M(+2,-2)|^2 / (8piGs)^2 vs (t^4+u^4)/s^4: max rel dev = {np.max(np.abs(vals/pred-1)):.2e}")
vals_same = np.array([sumfinal(2, 2, x, 0.3) for x in ths])
print(f"  same physical helicity (+2,+2): max sum_final |M|^2/(8piGs)^2 = {np.max(vals_same):.2e} (selection rule zero)")

# Part 3: superposed linear polarisations (c_R = c_L = 1/sqrt2 each graviton): interference depends on
# the relative phase between the two gravitons' helicity components, i.e. on azimuth -> averages out.
print("\nPart 3: two LINEARLY polarised gravitons ('plus' about each own axis), sum_final |M|^2 vs azimuth")
for chi in (0.0, PI / 4, PI / 2):
    # rotate graviton 2's linear polarisation by chi: eps = cos2chi plus + sin2chi cross
    vals = []
    for php in np.linspace(0, 2 * PI, 9)[:-1]:
        k1, k2 = photons(th, php)
        e1 = q2.graviton_polarization(q1, "plus")
        e2 = math.cos(2 * chi) * q2.graviton_polarization(qq2, "plus") + math.sin(2 * chi) * q2.graviton_polarization(qq2, "cross")
        tot = 0.0
        for h1 in (1, -1):
            for h2 in (1, -1):
                tot += abs(complex(q2.amplitude_gg_to_photons(q1, e1, qq2, e2, k1, q2.photon_polarization(k1[1:], h1),
                                                              k2, q2.photon_polarization(k2[1:], h2), G=G))) ** 2
        vals.append(tot / norm ** 2)
    vals = np.array(vals)
    print(f"  chi = {chi:.3f} rad: sum_final|M|^2/(8piGs)^2 over ph: min {vals.min():.5f} max {vals.max():.5f} mean {vals.mean():.5f}")
tt0, uu0 = (1 - math.cos(th)) / 2, (1 + math.cos(th)) / 2
print(f"  reference at th={th}: (t^4+u^4)/(2 s^4) = {(tt0**4+uu0**4)/2:.5f} [physical, half the gravitons pairs are +- ];"
      f" B&O real-sign (t^2+u^2)^2/(2 s^4) = {(tt0**2+uu0**2)**2/2:.5f}")
