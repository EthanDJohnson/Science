#!/usr/bin/env python3
"""Examiner lens: WHERE is the fusion yield of a coherent spherical wave generated, and does a purely
OUTGOING (retarded) wave keep producing pairs far from its source?

Toy model (labelled): a massless scalar monopole wave stands in for the GW; the second-order effective source
is j(x) = (phi+(x))^2 (the a a part of h h, B&O footnote 2 drops a^dag a), and pairs of massless quanta are
produced with vertex weight (q^2)^p:
    Y  ∝  ∫ d^4q θ(q0) θ(q^2) (q^2)^p |j~(q)|^2
p = 0 mimics a contact (phi^2 chi^2) coupling, p = 2 mimics graviton fusion, whose tree amplitude is ~ G s
(|M|^2 ∝ s^2, B&O eq. 6: 8 pi G t^2/s, 8 pi G u^2/s with t, u ~ s) and so vanishes for collinear partners.
Narrow band: g(u) = exp(-i w u - sigma^2 u^2/2), q0 fixed at 2w (|G2(q0)|^2 factors out of every ratio).

Two classical fields with the SAME outgoing wave at late times (same graviton number N):
  retarded (real source at r = 0 switched on/off):   phi+ = g(t-r)/r
  time-symmetric free solution (what a coherent state with a fixed alpha(k) spread over all directions carries;
  B&O eq. 5 uses the Pauli-Jordan function = G_ret - G_adv):  phi+ = [g(t-r) - g(t+r)]/r
      (incoming converging shell for t < 0, re-expanding shell for t > 0, regular at r = 0)
Fourier (spherical): j~(q0,|q|) = G2(q0) (4 pi/|q|) I(q), with
  I_ret(q) = ∫ dr W(r) e^{i q0 r} sin(q r)/r
  I_sym(q) = ∫ dr W(r) [2 cos(q0 r) - 2 exp(-sigma^2 r^2)] sin(q r)/r
W(r) = 1 (whole space) or a smooth window 0.5(1+tanh((r-R)/D)) keeping only r > R ("yield made beyond R").
Y(W) ∝ ∫_0^{q0} dq (q0^2 - q^2)^p |I(q)|^2.
Units: natural, w = 1 (so lengths in units of 1/w = lambda/2pi); sigma = 0.01 w.
"""
import math
import numpy as np

w = 1.0
q0 = 2 * w
sig = 0.01
L_damp = 1500.0          # adiabatic damping length for the oscillatory r integrals (>> 1/sigma = 100)
dr = 0.08
r = np.arange(dr / 2, 10 * L_damp, dr)
damp = np.exp(-r / L_damp)
nq = 1200
qq = (np.arange(nq) + 0.5) / nq * q0           # midpoint grid on (0, q0)
dq = q0 / nq


def radial_I(kind, W):
    out = np.empty(nq, dtype=complex)
    base = W * damp * dr
    if kind == "ret":
        ker = base * np.exp(1j * q0 * r)
    else:
        ker = base * (2 * np.cos(q0 * r) - 2 * np.exp(-(sig * r) ** 2))
    for i0 in range(0, nq, 60):
        qs = qq[i0:i0 + 60]
        s = np.sin(np.outer(qs, r)) / r
        out[i0:i0 + 60] = s @ ker
    return out


def Y(I, p):
    return float(np.sum((q0 ** 2 - qq ** 2) ** p * np.abs(I) ** 2) * dq)


print("=== Check 1: analytic whole-space values (W = 1) ===")
I_ret_an = 0.5j * np.log((q0 + qq) / (q0 - qq))
I_sym_an = -math.pi * np.array([math.erf(x / (2 * sig)) for x in qq])
I_ret_num = radial_I("ret", np.ones_like(r))
I_sym_num = radial_I("sym", np.ones_like(r))
mid = nq // 2
print(f"I_ret(q=w): numeric {I_ret_num[mid]:.4f}, analytic {I_ret_an[mid]:.4f}")
print(f"I_sym(q=w): numeric {I_sym_num[mid]:.4f}, analytic {I_sym_an[mid]:.4f}")
Yfull = {}
for p in (0, 2):
    Yr, Ys = Y(I_ret_an, p), Y(I_sym_an, p)
    Yfull[("ret", p)], Yfull[("sym", p)] = Y(I_ret_num, p), Y(I_sym_num, p)
    print(f"p={p}: analytic Y_ret/Y_sym = {Yr/Ys:.4f}  (p=0 exact value 1/12 = {1/12:.4f});"
          f" numeric {Yfull[('ret', p)]/Yfull[('sym', p)]:.4f}")
print("Note: for W = 1 the outgoing and incoming self-terms give ZERO time-like amplitude for the symmetric field;")
print("its whole yield is the cross term -2 g(t-r) g(t+r)/r^2, i.e. incoming x outgoing gravitons where the shells")
print("overlap (t ~ 0, r < 1/sigma).")

print()
print("=== Check 2: exact plane wave j = g(t-z)^2 has Fourier support only on q0 = q_z, q_perp = 0, i.e. q^2 = 0 ===")
print("θ(q^2>0) support is empty -> zero yield for any p (no time-like component). [analytic, no numerics]")

print()
print("=== Check 3: yield generated beyond radius R (smooth window, width D = R/4), fraction of whole-space yield ===")
print("R in units of 1/w = lambda/(2 pi)")
Rs = [1, 2, 5, 10, 20, 50, 100, 200, 400]
rows = []
for R in Rs:
    row = [R]
    for D_frac in (0.25,):
        W = 0.5 * (1 + np.tanh((r - R) / (D_frac * R)))
        Ir = radial_I("ret", W)
        Is = radial_I("sym", W)
        for p in (0, 2):
            row.append(Y(Ir, p) / Yfull[("ret", p)])
            row.append(Y(Is, p) / Yfull[("sym", p)])
    rows.append(row)
    print(f"R={R:5g}: ret p0 {row[1]:.3e} | sym p0 {row[2]:.3e} | ret p2 {row[3]:.3e} | sym p2 {row[4]:.3e}")

print()
print("=== Power-law slopes d ln F / d ln R between successive R (F = fraction beyond R) ===")
for k, lab in ((1, "ret p0"), (2, "sym p0"), (3, "ret p2"), (4, "sym p2")):
    sl = [math.log(rows[i + 1][k] / rows[i][k]) / math.log(rows[i + 1][0] / rows[i][0]) for i in range(len(rows) - 1)]
    print(lab + ": " + ", ".join(f"{s:.2f}" for s in sl))

print()
print("=== Window-shape sensitivity at R = 50 (D = R/2, R/4, R/8) ===")
for D_frac in (0.5, 0.25, 0.125):
    W = 0.5 * (1 + np.tanh((r - 50) / (D_frac * 50)))
    Ir, Is = radial_I("ret", W), radial_I("sym", W)
    print(f"D=R*{D_frac}: ret p2 {Y(Ir, 2)/Yfull[('ret', 2)]:.3e}, sym p2 {Y(Is, 2)/Yfull[('sym', 2)]:.3e}, "
          f"ret p0 {Y(Ir, 0)/Yfull[('ret', 0)]:.3e}, sym p0 {Y(Is, 0)/Yfull[('sym', 0)]:.3e}")
