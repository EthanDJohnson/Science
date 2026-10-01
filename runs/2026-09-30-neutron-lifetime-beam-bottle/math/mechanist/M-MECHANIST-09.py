"""M-MECHANIST-09 (F11, O4): Berezhiani strong-field n -> n' in the BL1 solenoid, own model.
Two-level H = [[0, eps], [eps, delta(z)]], delta = Dm - |mu_n| B(z) (B' = 0), eps = theta0 * Dm
(small angle: tan 2theta0 = 2 eps/Dm). If Dm > |mu_n| B_max there is no level crossing; the passage is
adiabatic (checked below), so the n' probability inside the field is sin^2 theta(z), tan 2theta = 2eps/delta(z),
independent of velocity. At the low-field monitor, entering with theta_i = theta0 and ending at theta0,
the oscillation-averaged P_det = (1/2) sin^2(2 theta0) ~ 2 theta0^2.
Proton counting: tau_beam/tau_beta = (1 - P_det)/(1 - P_trap).
Units: energies in neV, fields in T, lengths in m, times in s (SI); hbar in neV s."""
import math, sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import quantity, identity, series, limit, finish

mu = 60.3077          # |mu_n| in neV/T  (9.6623651e-27 J/T / 1.602176634e-28 J/neV)
hbar = 6.582119569e-7  # neV s
quantity(f"{9.6623651e-27/1.602176634e-28}", f"{mu}", rel_tol=1e-5)
Dm = 280.0
Bres = Dm / mu
print(f"B_res = {Bres:.4f} T; mu*4.6 T = {mu*4.6:.2f} neV")
quantity(f"{Bres} T", "4.64 T", rel_tol=1e-3)
th0 = 1.66e-3
eps = th0 * Dm
tau_nn = hbar / eps
Pdet = 0.5 * math.sin(math.atan(2 * eps / Dm)) ** 2  # (1/2) sin^2(2 theta0), 2theta0 = atan(2eps/Dm)
print(f"eps = {eps:.4f} neV, tau_nn' = {tau_nn:.3e} s, P_det = {Pdet:.3e}")
quantity(f"{tau_nn} s", "1.4e-6 s", rel_tol=0.02)
quantity(f"{Pdet}", "5.5e-6", rel_tol=0.01)
t, e, d = sp.symbols("theta eps delta", positive=True)
# (1/2) sin^2(2theta) with tan 2theta = 2 eps/delta equals 2 eps^2/(delta^2 + 4 eps^2)
identity(sp.Rational(1, 2) * sp.sin(sp.atan(2 * e / d)) ** 2, 2 * e**2 / (d**2 + 4 * e**2))
series("2*eps**2/(delta**2 + 4*eps**2)", "eps", 0, 3, "2*eps**2/delta**2")

# required P_trap: tau_beam/tau_beta = 887.97/877.82
R = 887.97 / 877.82
Ptrap_req = 1 - (1 - Pdet) / R
print(f"required P_trap (tau_beta = 877.82 s) = {Ptrap_req:.4e}; with +1.143 % convention: {1-(1-Pdet)/1.01143:.4e}")

def sin2(delta, eps):
    th = 0.5 * math.atan2(2 * eps, delta)
    return math.sin(th) ** 2

def bprof(z, B0, L, a):
    g = lambda zz: (zz + L / 2) / math.hypot(zz + L / 2, a) - (zz - L / 2) / math.hypot(zz - L / 2, a)
    return B0 * g(z) / g(0.0)

def ptrap(theta0, B0=4.6, L=0.6, a=None, half=0.15, n=2001):
    eps = theta0 * Dm
    if a is None:
        return sin2(Dm - mu * B0, eps)
    zs = [-half + 2 * half * i / (n - 1) for i in range(n)]
    return sum(sin2(Dm - mu * bprof(z, B0, L, a), eps) for z in zs) / n

def solve(**kw):
    lo, hi = 1e-5, 1e-2
    for _ in range(80):
        mid = math.sqrt(lo * hi)
        if ptrap(mid, **kw) < Ptrap_req:
            lo = mid
        else:
            hi = mid
    return mid

th_uni = solve()
print(f"uniform 4.6 T field: theta0 needed = {th_uni:.3e}")
res = {}
for a in (0.05, 0.1, 0.15):
    for half in (0.1, 0.15, 0.2):
        th = solve(a=a, half=half)
        res[(a, half)] = th
        print(f"solenoid L=0.6 m, a={a} m, trap |z|<{half} m: B(edge)={bprof(half,4.6,0.6,a):.3f} T, theta0 = {th:.3e}")
lo_th, hi_th = min(res.values()), max(res.values())
print(f"range over profiles: {th_uni:.2e} (uniform) to {hi_th:.2e}")
# adiabaticity at the solenoid entrance: |d theta/dt| * hbar / splitting, max over z for v = 2000 m/s
v = 2000.0; a = 0.1; eps_ = 1.66e-3 * Dm
worst = 0.0
for i in range(1, 4000):
    z = -1.0 + i * 1e-3 / 2
    dz = 1e-5
    th1 = 0.5 * math.atan2(2 * eps_, Dm - mu * bprof(z, 4.6, 0.6, a))
    th2 = 0.5 * math.atan2(2 * eps_, Dm - mu * bprof(z + dz, 4.6, 0.6, a))
    split = math.hypot(Dm - mu * bprof(z, 4.6, 0.6, a), 2 * eps_) / hbar
    worst = max(worst, abs(th2 - th1) / dz * v / split)
print(f"max adiabaticity ratio |dtheta/dt|/splitting (v = 2000 m/s, a = 0.1 m) = {worst:.2e}")
quantity(f"{th_uni}", "1.66e-3", rel_tol=0.1)   # lens value vs uniform-field limit
quantity(f"{hi_th}", "1.66e-3", rel_tol=0.3)
# 300 neV check (F11: shift < 0.1 s at theta0 = 1e-3)
for label, kw in (("uniform", {}), ("a=0.1,half=0.15", {"a": 0.1, "half": 0.15})):
    D0 = Dm
    globals()["Dm"] = 300.0
    p = ptrap(1e-3, **kw); pd = 2 * (1e-3) ** 2
    globals()["Dm"] = D0
    print(f"Dm = 300 neV, theta0 = 1e-3, {label}: P_trap = {p:.3e}, shift = {877.82*((1-pd)/(1-p)-1):.3f} s")
raise SystemExit(finish())
