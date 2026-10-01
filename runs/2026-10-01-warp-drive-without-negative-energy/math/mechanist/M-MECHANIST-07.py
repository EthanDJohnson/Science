"""M-MECHANIST-07: extra stress from ramping the shift, S_ramp ~ beta0 |f'| / (8 pi c tau).

Linear, unit lapse, flat slice: h_tx = beta0 g(t/tau) f(r), g ramps 0 -> 1 over tau (g' ~ 1/tau).
Own linearized Einstein tensor; the time-derivative part of G_ij must scale as beta0 g' f' (times
an O(1) angular factor). Then the claimed numbers at mid-wall r = 15 m of the toolkit profile
(S' = -0.2 /m analytically at r = 15 m), eps = 1.376e40 J/m^3, beta0 = 0.04, c tau = 10 m:
ratio 0.28; tau = 3.3 us: 2.8e-3; tau = 1 s: 9.3e-9.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from math_checks import identity, quantity, limit, finish
from warp_shell import shift_profile, build_shell, G, C

t, x, y, z = sp.symbols("t x y z", real=True)
b0, tau = sp.symbols("b0 tau", positive=True)
X = [t, x, y, z]
r = sp.sqrt(x**2 + y**2 + z**2)
eta = sp.diag(-1, 1, 1, 1)
f = sp.exp(-r**2)
gt = t / tau  # linear ramp
h = sp.zeros(4, 4)
h[0, 1] = h[1, 0] = b0 * gt * f
hu = eta * h
box = lambda e: sum(eta[i, i] * sp.diff(e, X[i], 2) for i in range(4))
Ric = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        e = sum(sp.diff(hu[q, n], X[q], X[m]) + sp.diff(hu[q, m], X[q], X[n]) for q in range(4))
        Ric[m, n] = (e - box(h[m, n])) / 2
Rs = sum(eta[i, i] * Ric[i, i] for i in range(4))
Gm = Ric - eta * Rs / 2
# spatial stress block, time-derivative part (only part present once the ramp has stopped is zero)
Sij = sp.Matrix(3, 3, lambda i, j: sp.simplify(Gm[i + 1, j + 1] / (8 * sp.pi)))
print("S_ij (linear ramp) =", Sij)
fp = sp.diff(sp.exp(-sp.Symbol("rr")**2), sp.Symbol("rr"))
# compare with b0 f'(r) cos(th) / (8 pi tau) form: S_xx should be -b0 f' (x/r)/(8 pi tau) * k
pt = {x: 0.7, y: 0.2, z: 0.3, b0: 0.1, tau: 2.0}
rv = float(r.subs(pt))
fpv = float((-2 * rv * np.exp(-rv**2)))
ref = 0.1 * abs(fpv) / (8 * np.pi * 2.0)
eig = np.linalg.eigvalsh(np.array(Sij.subs(pt), dtype=float))
print("principal stresses / [b0 |f'|/(8 pi tau)] at a sample point:", eig / ref)
# scaling: S_ij proportional to b0/tau exactly
identity(sp.simplify(Sij[0, 0] * tau / b0 - (Sij[0, 0] * tau / b0).subs({b0: 1, tau: 1})), "0")
limit(Sij[0, 0], "tau", sp.oo, "0")
# Max principal stress over angle relative to b0|f'|/(8 pi tau): sample many directions at fixed r
th = np.linspace(0, np.pi, 61); mx = 0
for a in th:
    p2 = {x: 1.0 * np.cos(a), y: 1.0 * np.sin(a), z: 0.0, b0: 1.0, tau: 1.0}
    ev = np.linalg.eigvalsh(np.array(Sij.subs(p2), dtype=float))
    mx = max(mx, np.abs(ev).max() / (abs(-2 * np.exp(-1.0)) / (8 * np.pi)))
print("max |principal stress| / [b0 |f'|/(8 pi tau)] over angles at r = 1:", mx)
# numbers
S = shift_profile(np.array([14.999, 15.001]), 10.0, 20.0)
Sp = (S[1] - S[0]) / 0.002
eps = float(np.interp(15.0, build_shell(4.49e27, 10.0, 20.0).r, build_shell(4.49e27, 10.0, 20.0).eps))
print(f"S'(15 m) = {Sp:.5f} /m, eps(15 m) = {eps:.4e} J/m^3")
for ctau, claim in [(10.0, "0.28"), (C * 3.3e-6, "2.8e-3"), (C * 1.0, "9.3e-9")]:
    ratio = 0.04 * abs(Sp) / (8 * np.pi * ctau) * C**4 / G / eps
    print(f"c tau = {ctau:.4g} m: ratio = {ratio:.3e}")
    quantity(f"{ratio} m/m", f"{claim} m/m", rel_tol=0.03)
quantity("10 m / (2.99792458e8 m/s)", "33 ns", rel_tol=0.02)
raise SystemExit(finish())
