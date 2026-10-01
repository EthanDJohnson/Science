"""M-DIALECTICIAN-02: J-PARC per-condition (D-24, stat only) pressure x SFC decomposition and a weighted
linear fit tau(p) = t0 + s p. Pressures in kPa, lifetimes in s. Also: 1% mis-subtraction of S_beta -> ~9 s."""
import sys
import numpy as np
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/dialectician")
from _common import *  # noqa

d = {(p, sfc): (t, e) for p, sfc, t, e in JCONF}
old = d[(50, "old")][0] - d[(100, "old")][0], q(d[(50, "old")][1], d[(100, "old")][1])
new = d[(50, "new")][0] - d[(100, "new")][0], q(d[(50, "new")][1], d[(100, "new")][1])
inter = new[0] - old[0], q(new[1], old[1])
print(f"old SFC tau(50)-tau(100) = {old[0]:+.2f} +- {old[1]:.2f} s")
print(f"new SFC tau(50)-tau(100) = {new[0]:+.2f} +- {new[1]:.2f} s")
print(f"interaction = {inter[0]:+.2f} +- {inter[1]:.2f} s = {inter[0]/inter[1]:.2f} sigma")
num("old diff", old[0], -2.7, abs_tol=0.01); num("old err", old[1], 8.5, abs_tol=0.05)
num("new diff", new[0], 16.5, abs_tol=0.01); num("new err", new[1], 4.7, abs_tol=0.05)
num("interaction", inter[0], 19.2, abs_tol=0.01); num("interaction err", inter[1], 9.7, abs_tol=0.05)

# Weighted least squares, built from the normal equations (not a library fit)
p = np.array([c[0] for c in JCONF], float); t = np.array([c[2] for c in JCONF]); e = np.array([c[3] for c in JCONF])
W = np.diag(1 / e**2); X = np.column_stack([np.ones_like(p), p])
C = np.linalg.inv(X.T @ W @ X); beta = C @ X.T @ W @ t
r = t - X @ beta; chi2 = float(r @ W @ r)
t0, s = beta; st0, ss = np.sqrt(np.diag(C))
print(f"fit: t0 = {t0:.2f} +- {st0:.2f} s, slope = {s:.4f} +- {ss:.4f} s/kPa, chi2 = {chi2:.2f}/2")
print(f"fit at 100 kPa: {t0+100*s:.2f} s; at 50 kPa: {t0+50*s:.2f} s")
num("t0", t0, 896.9, abs_tol=0.06); num("t0 err", st0, 5.3, abs_tol=0.06)
num("slope", s, -0.27, unit="s/kPa", abs_tol=0.006); num("slope err", ss, 0.07, unit="s/kPa", abs_tol=0.006)
num("chi2", chi2, 4.5, unit="", abs_tol=0.06)
# Sensitivity to the single driving point: refit without 50 kPa/new SFC
keep = [0, 1, 2]
Xk, Wk, tk = X[keep], W[np.ix_(keep, keep)], t[keep]
Ck = np.linalg.inv(Xk.T @ Wk @ Xk); bk = Ck @ Xk.T @ Wk @ tk
print(f"without 50kPa/new: t0 = {bk[0]:.1f} +- {np.sqrt(Ck[0,0]):.1f} s, slope = {bk[1]:+.3f} +- {np.sqrt(Ck[1,1]):.3f} s/kPa")

# Limit check: equal errors -> slope equals unweighted OLS slope; exact 2-point case: slope = (t2-t1)/(p2-p1)
identity("((t2 - t1)/(p2 - p1))*(p1) + (t1 - p1*(t2 - t1)/(p2 - p1))", "t1",
         domain={"t1": (800, 900), "t2": (800, 900), "p1": (10, 49), "p2": (51, 120)})
units("0.27 s/kPa * 100 kPa", "time")

# tau proportional to 1/S_beta for fixed neutron density: a fractional excess f in S_beta shortens tau by tau*f/(1+f)
tau = 877.2
shift = tau - tau / 1.01
print(f"1% mis-subtraction of S_beta: {shift:.2f} s (tau*f = {tau*0.01:.2f} s)")
num("1% of S_beta", shift, 9.0, abs_tol=0.35)
series("T/(1 + f)", "f", 0, 2, "T - T*f")
raise SystemExit(finish())
