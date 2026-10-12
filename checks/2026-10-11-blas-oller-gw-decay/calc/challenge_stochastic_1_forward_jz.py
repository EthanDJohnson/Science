#!/usr/bin/env python3
"""Probe of the helicity-label question behind the '4p(1-p)' caveat and S10 labels.
(1) J_z of the module's polarisation vectors (rotation about z).
(2) Module photon amplitudes near theta = 0 and pi for physical (+2,-2): |M| -> 8 pi G s although J_z(in) = 4 and
    J_z(out) = 2 for collinear photons. Exact rotational invariance forbids a nonzero EXACT-forward amplitude, so the
    limit is a non-uniform (phase-singular, [13]/<13>-type) massless-exchange feature, not a label error: the
    magnitude test alone cannot decide the physical-helicity class.
(3) S10 massive scalars (sympy): m^4 - t u = -4 E^2 p^2 sin^2(theta), so A_{+-} ~ (m^4 - tu)^2 ~ sin^4 theta = the
    J_z = 4 behaviour d^J_{40}, and A_{++} ~ m^4 s/((t-m^2)(u-m^2)) is nonzero forward = J_z = 0: S10 labels are
    common-axis-independent physical classes (same physical helicity <-> A_{++})."""
import sys, math, numpy as np, sympy as sp
sys.path.insert(0, '/home/user/Science/.claude/skills/conundrum/scripts')
import qft_second_order as q2
def Rz(a):
    c, s = math.cos(a), math.sin(a); R = np.eye(4); R[1, 1] = c; R[1, 2] = -s; R[2, 1] = s; R[2, 2] = c; return R
a = 0.37
for n, lab in [((0, 0, 1), '+z'), ((0, 0, -1), '-z')]:
    for h in (1, -1):
        e = q2.photon_polarization(np.array(n, float), h)
        print(f"  photon along {lab}, helicity {h:+d}: J_z = {-np.angle(np.vdot(e, Rz(a) @ e)) / a:+.6f}")
for theta in [1e-2, 1e-4, math.pi - 1e-4]:
    A = q2.helicity_amplitudes_cm(1.0, theta, final='photon')
    print(f"  theta = {theta:.6g}: nonzero |M|/(8 pi G s):", {k: round(abs(v) / (8 * math.pi), 8) for k, v in A.items() if abs(v) > 1e-9})
E, m, c = sp.symbols('E m c', positive=True)
p = sp.sqrt(E**2 - m**2)
t = m**2 - 2 * (E**2 - E * p * c); u = m**2 - 2 * (E**2 + E * p * c)
print("  m^4 - t u + 4 E^2 p^2 (1 - c^2) =", sp.simplify(sp.expand(m**4 - t * u + 4 * E**2 * p**2 * (1 - c**2))))
print("  A++ ~ m^4 s/((t-m^2)(u-m^2)) at c = 1:", sp.simplify((m**4 * 4 * E**2 / ((t - m**2) * (u - m**2))).subs(c, 1)))
