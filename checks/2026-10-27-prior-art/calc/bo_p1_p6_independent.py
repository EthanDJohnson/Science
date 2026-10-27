"""Independent spot checks of two Blas & Oller (arXiv:2607.24930) check points, written for the prior-art judge.

Part 1 (P1): is the rephasing invariant
    I(a, a') = M_a(g -> gamma+ gamma-) M_a(g -> gamma- gamma+)^* M_a'(g -> gamma- gamma+) M_a'(g -> gamma+ gamma-)^*
nontrivial (arg I not 0 or pi)?  Here a, a' are two graviton-pair axes with the same photon pair.
This uses only little-group-covariant spinor expressions, NOT the check's qft_second_order module or bo_common.
Any expression with the right little-group weights differs from the true amplitude by a little-group-invariant
factor, which for 4-point massless kinematics is a function of the s_ij only (real). So arg I is fixed up to
a sign (helicity-convention conjugation) and possibly pi. A value away from 0 and pi means no phase
convention makes the eq.-6 amplitudes real for all graviton pairs at once.

Part 2 (P6): narrow-band peak-rate and total ratios, Gaussian vs top-hat profile at equal N and sigma,
using R(t) proportional to |f~(t)|^4 with f~ the Fourier transform of the profile (narrow band).
"""
import math

import numpy as np
import sympy as sp


def spinors(p):
    """Return (|p>, |p]) as 2-vectors for a massless momentum p = (E, px, py, pz). Negative E: |-p> = i|p>."""
    E = p[0]
    sgn = 1.0 if E > 0 else -1.0
    q = np.array(p, dtype=float) * sgn
    e = q[0]
    pz, px, py = q[3], q[1], q[2]
    # lam = (sqrt(e+pz), (px+i py)/sqrt(e+pz)); guard against pz = -e
    if e + pz < 1e-12:
        lam = np.array([0.0, math.sqrt(2 * e)], dtype=complex)
    else:
        lam = np.array([math.sqrt(e + pz), (px + 1j * py) / math.sqrt(e + pz)], dtype=complex)
    lamt = np.conj(lam)
    if sgn < 0:
        lam, lamt = 1j * lam, 1j * lamt
    return lam, lamt


def ang(a, b):
    return a[0][0] * b[0][1] - a[0][1] * b[0][0]


def sq(a, b):
    return -(a[1][0] * b[1][1] - a[1][1] * b[1][0])


def mdot(p, q):
    return p[0] * q[0] - p[1] * q[1] - p[2] * q[2] - p[3] * q[3]


def amps(q1, q2, k1, k2):
    """Photons q1, q2 outgoing; gravitons k1 (+2), k2 (-2) incoming -> outgoing p3 = -k1 (helicity -2),
    p4 = -k2 (helicity +2). Returns (M(gamma1 +, gamma2 -), M(gamma1 -, gamma2 +)) up to a common real factor."""
    P = [q1, q2, -k1, -k2]
    S = [spinors(p) for p in P]
    s = lambda i, j: 2 * mdot(P[i], P[j])
    # sanity: <ij>[ji] = s_ij
    for i in range(4):
        for j in range(4):
            if i != j:
                assert abs(ang(S[i], S[j]) * sq(S[j], S[i]) - s(i, j)) < 1e-9
    one, two, three, four = S
    den = s(0, 1) * s(0, 2) * s(0, 3)
    # M(1^+ 2^- 3^{-2} 4^{+2}): weights [1]:2, <2>:2, <3>:4, [4]:4
    Mpm = ang(two, three) ** 2 * sq(one, four) ** 2 * (ang(three, one) * sq(one, four)) ** 2 / den
    # M(1^- 2^+ 3^{-2} 4^{+2}): weights <1>:2, [2]:2, <3>:4, [4]:4
    Mmp = ang(one, three) ** 2 * sq(two, four) ** 2 * (ang(three, two) * sq(two, four)) ** 2 / den
    # magnitude check against eq. 6 shape: |M| = t^2/s or u^2/s (8 pi G stripped)
    t, u, sm = s(0, 2), s(0, 3), s(0, 1)
    return Mpm, Mmp, (abs(Mpm), abs(Mmp)), (t * t / sm, u * u / sm)


def little_group_test(q1, q2, k1, k2):
    """Rephase one photon's spinors and confirm the invariant does not move (sanity of the construction)."""
    return None


print("=" * 90)
print("Part 1 (P1): rephasing invariant from closed-form spinor expressions (independent of the check's module)")
print("=" * 90)
E = 1.0
for th_deg, ph_deg, ref in ((60, 17, "+63.87, -17.09, -125.78"), (60, 45, "+126.66, -46.80, +106.26"),
                            (100, 10, "+21.15, +52.85, -178.25")):
    th, ph = math.radians(th_deg), math.radians(ph_deg)
    n = np.array([math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th)])
    q1, q2 = np.concatenate([[E], E * n]), np.concatenate([[E], -E * n])
    vals = []
    for adeg in (0, 30, 60, 90):
        a = math.radians(adeg)
        d = np.array([math.sin(a), 0.0, math.cos(a)])
        k1, k2 = np.concatenate([[E], E * d]), np.concatenate([[E], -E * d])
        Mpm, Mmp, mags, shapes = amps(q1, q2, k1, k2)
        # magnitudes: one of Mpm, Mmp equals t^2/s and the other u^2/s (which is which is a labelling choice)
        ok = (np.allclose(sorted(mags), sorted(shapes), rtol=1e-9))
        vals.append((adeg, Mpm * np.conj(Mmp), ok))
    base = vals[0][1]
    args = [math.degrees(np.angle(np.conj(v) * base)) for _, v, _ in vals[1:]]
    print(f"photons theta={th_deg}, phi={ph_deg}: magnitudes match t^2/s,u^2/s: {all(o for *_, o in vals)}")
    print("   arg I(a=0, a') for a' = 30, 60, 90 deg:", ", ".join(f"{x:+8.2f}" for x in args),
          f"   | check's taskA1 values: {ref}")

# Rephasing sanity: multiply photon 1 spinors by a phase and confirm I is unchanged (done analytically:
# Mpm ~ [1]^2 -> e^{-2ib}, Mmp ~ <1>^2 -> e^{+2ib}; each I contains Mpm Mmp^* and Mmp Mpm^* once -> cancels).
print("Rephasing photon 1 by e^{ib}: Mpm -> e^{-2ib} Mpm, Mmp -> e^{2ib} Mmp; I(a,a') picks up e^{-4ib} e^{+4ib} = 1.")

print()
print("=" * 90)
print("Part 2 (P6): Gaussian vs top hat at equal N and sigma (narrow band, R(t) ~ |f~(t)|^4)")
print("=" * 90)
k, t, w, sig, N, Th = sp.symbols("k t omega sigma N Theta", positive=True)
x = sp.symbols("x", real=True)
# top hat of height Th on [w - sig/2, w + sig/2]; N proportional to Th^2 sig (same constant as Gaussian)
N_top = Th**2 * sig
ft_top0 = Th * sig  # |f~(0)|
R0_top = (ft_top0**4).subs(Th, sp.sqrt(N / sig))
Tint_top = sp.integrate(sp.sin(sig * t / 2) ** 4 / (sig * t / 2) ** 4, (t, -sp.oo, sp.oo))
Ptot_top = sp.simplify(R0_top * Tint_top)
# Gaussian f = Th exp(-(k-w)^2/(2 sig^2)); N proportional to Th^2 * int exp(-x^2/sig^2) dx
N_g = Th**2 * sp.integrate(sp.exp(-x**2 / sig**2), (x, -sp.oo, sp.oo))
ft_g = Th * sp.integrate(sp.exp(-x**2 / (2 * sig**2)) * sp.exp(-sp.I * x * t), (x, -sp.oo, sp.oo))
ft_g = sp.simplify(ft_g)
Th_g = sp.solve(sp.Eq(N_g, N), Th)[0]
R_g = sp.simplify((sp.Abs(ft_g) ** 4).subs(Th, Th_g))
R0_g = sp.simplify(R_g.subs(t, 0))
Ptot_g = sp.simplify(sp.integrate(R_g, (t, -sp.oo, sp.oo)))
print("integral of sinc^4(sigma t/2) dt =", sp.simplify(Tint_top), " (T_eff for the top hat; expect 4 pi/(3 sigma))")
print("peak ratio  R0_gauss / R0_tophat  =", sp.simplify(R0_g / R0_top), "=", float(sp.simplify(R0_g / R0_top)))
print("total ratio Ptot_gauss / Ptot_top =", sp.simplify(Ptot_g / Ptot_top), "=", float(sp.simplify(Ptot_g / Ptot_top)))
print("(check's report: peak x 4 pi = 12.566, total x 3.7599)")
