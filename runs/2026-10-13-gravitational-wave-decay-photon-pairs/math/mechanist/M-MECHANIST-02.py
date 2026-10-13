"""M-MECHANIST-02: interference of the two opposite-helicity channels for linearly polarised gravitons.

Lens claim (F2): cross term +-2 t^2 u^2 cos(4 chi), independent of photon azimuth; aligned linear
polarisations reproduce B&O's real-sign (t^2+u^2)^2/(2 s^4) after angular integration (14/15 vs 4/5 = 7/6);
anti-aligned 5/7 of B&O; pure (+2,-2) 12/7 of B&O.

Independent route: (i) rotation covariance: the two channels carry J_z = +4 and -4 along the collision axis,
so for any fixed final-polarisation basis rotated with the photons, cross(phi) = cross(0) e^{+-8 i phi};
checked numerically with KLT spinor amplitudes (own code, same as M-MECHANIST-01). (ii) sympy angular integrals.
Natural units, amplitudes in units of 8 pi G.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from math_checks import identity, quantity, finish


def lam(p):
    sgn = 1.0 if p[0] > 0 else -1.0
    q = sgn * np.asarray(p, float)
    E = q[0]
    th = np.arccos(np.clip(q[3] / E, -1, 1)); ph = np.arctan2(q[2], q[1])
    l = np.sqrt(2 * E) * np.array([np.cos(th / 2), np.sin(th / 2) * np.exp(1j * ph)])
    return l, np.conj(l) * (1.0 if sgn > 0 else -1.0)


def ang(a, b): return a[0][0] * b[0][1] - a[0][1] * b[0][0]
def sqb(a, b): return -(a[1][0] * b[1][1] - a[1][1] * b[1][0])


def amps(th, ph, w=1.0):
    n = np.array([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)])
    P = [np.r_[w, w * n], np.r_[w, -w * n], -np.array([w, 0, 0, w]), -np.array([w, 0, 0, -w])]
    S = [lam(p) for p in P]
    out = {}
    for name, br in (("ang", ang), ("sq", sqb)):
        a = lambda i, j: br(S[i - 1], S[j - 1])
        s12 = 4 * w * w
        dY = a(1, 2) * a(2, 3) * a(3, 4) * a(4, 1); dS = a(1, 2) * a(2, 4) * a(4, 3) * a(3, 1)
        Ma = s12 * a(2, 4) ** 4 / dY * a(1, 4) ** 2 * a(2, 4) ** 2 / dS   # graviton channel J_z = -4
        Mb = s12 * a(2, 3) ** 4 / dY * a(1, 3) ** 2 * a(2, 3) ** 2 / dS   # graviton channel J_z = +4
        out[name] = (Ma, Mb)   # "ang": photons (1+,2-); "sq" (parity image): photons (1-,2+)
    return out


th = 1.1
phis = np.linspace(0, 2 * np.pi, 41)[:-1]
X0 = {k: v[0] * np.conj(v[1]) for k, v in amps(th, 0.0).items()}
dev = {"ang": 0.0, "sq": 0.0}; SGN = {"ang": -8, "sq": 8}
for ph in phis:
    A = amps(th, ph)
    for k in A:
        X = A[k][0] * np.conj(A[k][1])
        if True:
            dev[k] = max(dev[k], abs(X - X0[k] * np.exp(1j * SGN[k] * ph)) / abs(X0[k]))
print(f"cross term X(phi) = M_(Jz=-4) conj(M_(Jz=+4)) at theta = 1.1: photons (1+,2-): max |X - X0 e^(-8i phi)|/|X0| = {dev['ang']:.2e},"
      f" photons (1-,2+): max |X - X0 e^(+8i phi)|/|X0| = {dev['sq']:.2e}")
for ph in phis[:6]:
    A = amps(th, ph)
    print(f"  phi = {ph:.3f}: " + "; ".join(
        f"{k}: |X/X0| = {abs(A[k][0]*np.conj(A[k][1])/X0[k]):.6f}, arg(X/X0)/phi = "
        f"{(np.angle(A[k][0]*np.conj(A[k][1])/X0[k]) / ph if ph else 0):.4f}" for k in A))
best = max(dev.values())
quantity(f"{1 + best:.15f}", "1", rel_tol=1e-10)   # cross term rotates as e^{+-8 i phi}: never constant

# Linear polarisations: coefficients c_a, c_b of modulus 1/2 per channel (product of two gravitons'
# 1/sqrt2), relative phase beta set by the orientations. Rate summed over both photon final states vs phi.
for beta in (0.0, np.pi / 4, np.pi / 2, 1.3):
    vals = []
    for ph in phis:
        A = amps(th, ph)
        r = sum(abs(0.5 * A[k][0] + 0.5 * np.exp(1j * beta) * A[k][1]) ** 2 for k in A) / 16.0   # /s^2 with s = 4
        vals.append(r)
    vals = np.array(vals)
    print(f"beta = {beta:.3f}: sum_final|M|^2/(8piG s)^2 over phi: min {vals.min():.5f} max {vals.max():.5f}"
          f" mean {vals.mean():.5f}")
tt = -(1 - np.cos(th)) / 2; uu = -(1 + np.cos(th)) / 2   # t/s, u/s
print(f"references at theta = 1.1: incoherent (t^4+u^4)/(2s^4) = {(tt**4+uu**4)/2:.5f},"
      f" B&O real-sign (t^2+u^2)^2/(2s^4) = {(tt**2+uu**2)**2/2:.5f}, (t^2-u^2)^2/(2s^4) = {(tt**2-uu**2)**2/2:.5f}")
A = [amps(th, ph) for ph in phis]
mean0 = np.mean([sum(abs(0.5 * a[k][0] + 0.5 * a[k][1]) ** 2 for k in a) / 16 for a in A])
quantity(f"{mean0:.12f}", f"{(tt**4+uu**4)/2:.12f}", rel_tol=1e-9)   # azimuth average = incoherent value
quantity(f"{(tt**2+uu**2)**2/2:.6f}", "0.18173", rel_tol=1e-4)
quantity(f"{(tt**4+uu**4)/2:.6f}", "0.14230", rel_tol=1e-4)
quantity(f"{(tt**2-uu**2)**2/2:.6f}", "0.10287", rel_tol=1e-4)

# Angular integrals (c = cos theta_CM, t = -s(1-c)/2, u = -s(1+c)/2), per s^4
c = sp.symbols("c", real=True)
T = -(1 - c) / 2; U = -(1 + c) / 2
inc = sp.integrate(T**4 + U**4, (c, -1, 1)); coh = sp.integrate((T**2 + U**2) ** 2, (c, -1, 1))
anti = sp.integrate((T**2 - U**2) ** 2, (c, -1, 1))
print("int (t^4+u^4)/s^4 =", inc, "; int (t^2+u^2)^2/s^4 =", coh, "; int (t^2-u^2)^2/s^4 =", anti)
identity(inc, sp.Rational(4, 5)); identity(coh, sp.Rational(14, 15)); identity(anti, sp.Rational(2, 3))
identity(coh / inc, sp.Rational(7, 6)); identity(anti / coh, sp.Rational(5, 7))
identity(inc / (coh / 2), sp.Rational(12, 7))          # pure (+2,-2) vs B&O per collision (7/15)
# Corrected: azimuth-averaged linear polarisation, ANY orientation, = inc/2 = 2/5 = 6/7 of B&O's 7/15
identity((inc / 2) / (coh / 2), sp.Rational(6, 7))
# Limit: at c = +-1 (forward) all three forms coincide (t or u = 0) -> no interference possible there
identity(((T**2 + U**2) ** 2 - (T**4 + U**4)).subs(c, 1), 0)
raise SystemExit(finish())
