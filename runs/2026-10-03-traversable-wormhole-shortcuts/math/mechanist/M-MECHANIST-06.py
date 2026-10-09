"""M-MECHANIST-06: toy feedback (finding 10), taking the lens's model as given:
T_w(Delta) = T_w0 / kappa(Delta, L), L = T_w(Delta) + d, kappa = L^2 (L^2 + Delta^2)/((L-Delta)^2 (L+Delta)^2),
T_w0 = pi*3000 yr, d = D/c. Self-consistent throat times are roots T > max(0, Delta - d) of
F(T) = T*kappa(Delta, T + d) - T_w0. The long branch is the root continued from T = T_w0 at Delta = 0;
it ends (folds) where it merges with another root, i.e. where it disappears from the root set.
Units: years. kappa itself (energy-density enhancement) is verified in M-MECHANIST-05.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from math_checks import limit, quantity, RESULTS, Result, finish

L_, D_ = sp.symbols("L Delta", positive=True)
limit(L_**2 * (L_**2 + D_**2) / ((L_ - D_)**2 * (L_ + D_)**2), "Delta", 0, "1")   # no-feedback limit

Tw0 = np.pi * 3000.0

def roots(Dl, d, n=200000):
    lo = max(0.0, Dl - d)
    T = lo + 1e-9 + 8 * Tw0 * (np.arange(1, n + 1) / n) ** 2
    L = T + d
    F = T * L**2 * (L**2 + Dl**2) / ((L - Dl)**2 * (L + Dl)**2) - Tw0
    idx = np.nonzero(np.sign(F[:-1]) * np.sign(F[1:]) < 0)[0]
    return [float((T[i] + T[i + 1]) / 2) for i in idx]

claims = {100: (2.3e3, 0.25), 1000: (2.7e3, 0.32), 3000: (3.3e3, 0.52)}
for d, (want_f, want_r) in claims.items():
    dsc = Tw0 - d
    prev = Tw0
    fold = None
    steps = 4000
    for k in range(1, steps + 1):
        Dl = dsc * k / steps
        rs = roots(Dl, d, n=40000)
        # continue the long branch: the root nearest the previous long-branch value, if it is close
        near = [r for r in rs if abs(r - prev) < 0.05 * prev + 50]
        if not near:
            fold = dsc * (k - 1) / steps
            print(f"INFO d = {d} yr: long branch last seen at Delta = {fold:.5g} yr (T_w = {prev:.4g} yr); "
                  f"roots at Delta = {Dl:.5g}: {[round(r, 1) for r in rs]}")
            break
        prev = min(near, key=lambda r: abs(r - prev))
    if fold is None:
        print(f"INFO d = {d} yr: long branch survives to Delta_sc = {dsc:.5g} yr")
        RESULTS.append(Result("fail", f"fold exists for d = {d}", "continuation"))
        continue
    print(f"INFO d = {d} yr: fold / Delta_sc = {fold / dsc:.4f}; lens: {want_f} yr, {want_r}")
    for frac in (0.2, 0.5, 0.9):
        D0 = fold * frac
        print(f"INFO   roots at Delta = {D0:.4g}: {[round(r, 1) for r in roots(D0, d)]}")
    quantity(f"{fold} yr", f"{want_f} yr", rel_tol=0.03)
    quantity(f"{fold / dsc}", f"{want_r}", rel_tol=0.03)
raise SystemExit(finish())
