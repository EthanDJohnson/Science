#!/usr/bin/env python3
"""Falsifier C7-1: is eq. 8's yield 'photon-vacuum pair creation on the classical second-order metric h^(2)'?

Natural units (hbar = c = 1), G = 1, s = 4 (CM energy^2). Tree-level g g -> gamma gamma in Einstein-Maxwell
via the toolkit's background-field amplitude (qft_second_order.amplitude_gg_to_photons, parts=True):
contact (h h A A), t/u photon exchange (second-order response of the quantised Maxwell field to h^(1)),
and s-channel = O(h) vertex fed with the classical second-order metric h^(2) (what C7 calls 'pair creation on h^(2)').

Quantities printed:
 (1) channel-by-channel |M|^2 summed over final photon helicities, CM frame, for the opposite-helicity
     (J_z = +-4) channel that carries B&O's eq. 7, and the same-helicity channel, at several angles;
 (2) phase-space integrated ratio  int |M_s|^2 / int |M_total|^2  (the 'h^(2)-only' yield over the full yield);
 (3) gauge test: eps -> eps + q xi + xi q changes each channel but not the total.
"""
import math
import sys

import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import qft_second_order as q2  # noqa: E402

s = 4.0
E = 1.0
q1 = np.array([E, 0, 0, E])
q2v = np.array([E, 0, 0, -E])


def final_state(theta, phi):
    n = np.array([math.sin(theta) * math.cos(phi), math.sin(theta) * math.sin(phi), math.cos(theta)])
    return np.concatenate([[E], E * n]), np.concatenate([[E], -E * n])


def channel_sq(eps1, eps2, theta, phi):
    k1, k2 = final_state(theta, phi)
    acc = {"contact": 0.0, "s_channel": 0.0, "tu_channel": 0.0, "total": 0.0}
    for s1 in (1, -1):
        for s2 in (1, -1):
            d = q2.amplitude_gg_to_photons(q1, eps1, q2v, eps2, k1, q2.photon_polarization(k1, s1), k2,
                                           q2.photon_polarization(k2, s2), G=1.0, parts=True)
            for key in acc:
                acc[key] += abs(complex(d[key])) ** 2
    return acc


cases = {"opposite helicity (+2,-2): J_z=+4, B&O eq. 7 channel": (2, -2),
         "same helicity (+2,+2): J_z=0": (2, 2)}
print("== (1) Channel |M|^2 (sum over photon helicities), CM, G=1, s=4, phi=0.3 ==")
for label, (l1, l2) in cases.items():
    e1 = q2.graviton_polarization(q1, l1)
    e2 = q2.graviton_polarization(q2v, l2)
    print(label)
    for th_deg in (30, 60, 90, 120, 150):
        a = channel_sq(e1, e2, math.radians(th_deg), 0.3)
        print(f"  theta={th_deg:3d} deg: |M_s|^2={a['s_channel']:.4e}  |M_contact|^2={a['contact']:.4e}  "
              f"|M_tu|^2={a['tu_channel']:.4e}  |M_total|^2={a['total']:.4e}")

print()
print("== (2) Phase-space integrated: Y_s = int dOmega |M_s|^2, Y_full = int dOmega |M_total|^2 ==")
nth, nph = 60, 16
xs, ws = np.polynomial.legendre.leggauss(nth)
for label, (l1, l2) in cases.items():
    e1 = q2.graviton_polarization(q1, l1)
    e2 = q2.graviton_polarization(q2v, l2)
    for n_t in (nth // 2, nth):
        xs, ws = np.polynomial.legendre.leggauss(n_t)
        Ys = Yf = 0.0
        for x, w in zip(xs, ws):
            th = math.acos(x)
            for j in range(nph):
                ph = 2 * math.pi * (j + 0.5) / nph
                a = channel_sq(e1, e2, th, ph)
                Ys += w * a["s_channel"] * (2 * math.pi / nph)
                Yf += w * a["total"] * (2 * math.pi / nph)
        print(f"  {label} [n_theta={n_t}]: Y_s={Ys:.6e}  Y_full={Yf:.6e}  ratio Y_s/Y_full="
              f"{(Ys / Yf if Yf > 0 else float('inf')):.6e}")
    # closed-form check of the full yield: sigma(RL) = (4/5) pi G^2 s per tool docstring
print(f"  closed-form sigma_total(R,L) = (4/5) pi G^2 s = {0.8 * math.pi * s:.6e}; tool: "
      f"{q2.sigma_total(s, 'R', 'L', final='photon'):.6e}")
print(f"  tool sigma_total(R,R) (same helicity) = {q2.sigma_total(s, 'R', 'R', final='photon'):.6e}")

print()
print("== (3) Gauge test: eps2 -> eps2 + q2 xi + xi q2 (q2.xi = 0), opposite-helicity case, theta=60 deg ==")
e1 = q2.graviton_polarization(q1, 2)
e2 = q2.graviton_polarization(q2v, -2)
xi_up = np.array([0.0, 0.7, -0.4j, 0.0], dtype=complex)  # q2.xi = 0 since xi has no t or z part
xi = xi_up * np.array([1, -1, -1, -1])
q2low = q2v * np.array([1, -1, -1, -1])
e2g = e2 + np.outer(q2low, xi) + np.outer(xi, q2low)
k1, k2 = final_state(math.radians(60), 0.3)
for tag, eps2 in (("original", e2), ("gauge-shifted", e2g)):
    d = q2.amplitude_gg_to_photons(q1, e1, q2v, eps2, k1, q2.photon_polarization(k1, 1), k2,
                                   q2.photon_polarization(k2, -1), G=1.0, parts=True)
    print(f"  {tag:14s}: M_s={complex(d['s_channel']):.5f}  M_contact={complex(d['contact']):.5f}  "
          f"M_tu={complex(d['tu_channel']):.5f}  M_total={complex(d['total']):.5f}")
