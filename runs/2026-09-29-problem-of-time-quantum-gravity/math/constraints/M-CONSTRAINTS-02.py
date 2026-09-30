"""M-CONSTRAINTS-02: which internal clocks are monotonic in FRW + scalar minisuperspace (G = c = 1, units of L).

Equations (independent): a' = aH, H' = -4 pi phi'^2 + k/a^2, phi'' = -3H phi' - V'(phi), V = m^2 phi^2/2,
constraint H^2 = (8 pi/3)(phi'^2/2 + V) - k/a^2.  T4 = int a^3 dt.
Claims (qualitative, F2): (i) closed, massless: volume turns once; phi, H, T4 monotonic; SEC holds; DEC saturated.
(ii) flat, massive (m = 1/L): phi turns many times; a, H, T4 monotonic; SEC violated at some points, NEC never.
(iii) closed, massive: phi and H both turn (York time fails).
The exact counts (17, 17, 35) depend on initial data that F2 does not state; they are not re-derived here.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from math_checks import identity, sign, quantity, finish

# Analytic parts
pd, V, k, A = sp.symbols("pd V k A", real=True)
rho = pd**2 / 2 + V
p = pd**2 / 2 - V
identity(rho + 3 * p, 2 * pd**2 - 2 * V, domain={"pd": (-3, 3), "V": (0, 3)})   # SEC fails iff V > phi'^2
identity(rho + p, pd**2, domain={"pd": (-3, 3), "V": (0, 3)})                   # NEC always holds
# massless: rho = p (stiff), SEC rho+3p = 4 rho > 0, DEC rho - |p| = 0
identity((rho - p).subs(V, 0), "0", domain={"pd": (-3, 3)})
# flat: H^2 = 8 pi rho/3 > 0 => H cannot change sign => volume monotonic; H' = -4 pi phi'^2 <= 0
sign(-4 * sp.pi * pd**2, "nonpositive", domain={"pd": (-3, 3)})


def run(kv, m, a0, phi0, dphi0, T=60.0, n=60000):
    def rhs(t, y):
        a, H, ph, dph, T4 = y
        return [a * H, -4 * np.pi * dph**2 + kv / a**2, dph, -3 * H * dph - m**2 * ph, a**3]
    rho0 = dphi0**2 / 2 + m**2 * phi0**2 / 2
    H0 = np.sqrt(8 * np.pi / 3 * rho0 - kv / a0**2)
    ts = np.linspace(0, T, n)
    sol = solve_ivp(rhs, (0, T), [a0, H0, phi0, dphi0, 0.0], t_eval=ts, rtol=1e-10, atol=1e-12,
                    events=lambda t, y: y[0] - 1e-3)
    a, H, ph, dph, T4 = sol.y
    res = np.max(np.abs(H**2 - (8 * np.pi / 3 * (dph**2 / 2 + m**2 * ph**2 / 2) - kv / a**2)) / (H**2 + kv / a**2 + 1e-30))
    turns = lambda x: int(np.sum(np.diff(np.sign(np.diff(x))) != 0))
    sec_viol = int(np.sum(m**2 * ph**2 / 2 > dph**2))
    return dict(a=turns(a), H=turns(H), phi=turns(ph), T4=turns(T4), res=res, sec=sec_viol, npts=len(ts), tend=sol.t[-1])


r1 = run(1, 0.0, 1.0, 0.0, 0.5, T=60)   # closed, massless (stops if a -> 0 near recrunch)
r2 = run(0, 1.0, 1.0, 1.0, 0.0, T=60)
r3 = run(1, 1.0, 10.0, 0.1, 0.0, T=60)
for name, r in [("(i) closed massless", r1), ("(ii) flat massive", r2), ("(iii) closed massive", r3)]:
    print(name, r)
# Proper checks: (i) a turns exactly once; phi, H, T4 never
ok_i = r1["a"] == 1 and r1["phi"] == 0 and r1["H"] == 0 and r1["T4"] == 0
ok_ii = r2["phi"] > 0 and r2["a"] == 0 and r2["H"] == 0 and r2["T4"] == 0 and r2["sec"] > 0
ok_iii = r3["phi"] > 0 and r3["H"] > 0 and r3["T4"] == 0
print("PASS (i) closed massless: volume turns once, phi/H/T4 monotonic" if ok_i else "FAIL (i)")
print("PASS (ii) flat massive: phi turns, a/H/T4 monotonic, SEC violated somewhere" if ok_ii else "FAIL (ii)")
print("PASS (iii) closed massive: phi and H both turn (York time fails), T4 monotonic" if ok_iii else "FAIL (iii)")
# convergence: rerun (iii) with 1.5 n sampling
r3b = run(1, 1.0, 10.0, 0.1, 0.0, T=60, n=90000)
print("(iii) at 1.5n:", r3b)
print("PASS counts stable under n -> 1.5n" if (r3b["H"], r3b["phi"]) == (r3["H"], r3["phi"]) else "FAIL counts unstable")
raise SystemExit(finish() if (ok_i and ok_ii and ok_iii) else 1)
