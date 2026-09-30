"""M-MECHANIST-10 (F11): sign reversal when Dm < |mu_n| B_centre.
Then the path crosses resonance twice (entry and exit of the solenoid). Landau-Zener conversion per
crossing p = 1 - exp(-2 pi eps^2 / (hbar |d delta/dt|)), |d delta/dt| = |mu_n| |dB/dz| v.
Between the crossings (trap) P_trap ~ p; after both (monitor), incoherently (phase averaged over v)
P_det = 2 p (1 - p). tau_beam/tau_beta = (1 - P_det)/(1 - P_trap) < 1 for 0 < p < 1/2.
Own profile: finite solenoid L = 0.6 m, bore a = 0.1 m, 4.6 T; density-weighted velocity
spectrum n(v) ~ v^2 exp(-v^2/v0^2), v0 = 800 m/s (the lens's ASSUMED scale). neV, T, m, s (SI)."""
import math, sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import sign, limit, quantity, finish

mu = 60.3077; hbar = 6.582119569e-7
p = sp.symbols("p")
sign("(1 - 2*p*(1 - p))/(1 - p) - 1", "negative", domain={"p": (1e-9, 0.499)})
limit("((1 - 2*p*(1 - p))/(1 - p) - 1)/p", "p", 0, -1)

def bprof(z, B0=4.6, L=0.6, a=0.1):
    g = lambda zz: (zz + L / 2) / math.hypot(zz + L / 2, a) - (zz - L / 2) / math.hypot(zz - L / 2, a)
    return B0 * g(z) / g(0.0)

def crossing_slope(Bres, a=0.1):
    lo, hi = -2.0, 0.0   # entry side: B rises from ~0 to 4.6 T
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if bprof(mid, a=a) < Bres:
            lo = mid
        else:
            hi = mid
    dz = 1e-6
    return (bprof(mid + dz, a=a) - bprof(mid - dz, a=a)) / (2 * dz), mid

def shift(Dm, th0, a=0.1, v0=800.0):
    Bres = Dm / mu
    if Bres >= 4.6:
        return None
    slope, zc = crossing_slope(Bres, a)
    eps = th0 * Dm
    num = den = 0.0
    for i in range(1, 400):
        v = i * 10.0
        w = v**2 * math.exp(-(v / v0) ** 2)
        pc = 1 - math.exp(-2 * math.pi * eps**2 / (hbar * mu * slope * v))
        Pt, Pd = pc, 2 * pc * (1 - pc)
        num += w * ((1 - Pd) / (1 - Pt)); den += w
    return 877.82 * (num / den - 1), slope, zc

for a in (0.05, 0.1, 0.15):
    s_, slope, zc = shift(260.0, 1e-4, a=a)
    print(f"Dm = 260 neV, theta0 = 1e-4, bore a = {a} m: crossing at z = {zc:.3f} m, dB/dz = {slope:.1f} T/m, beam shift = {s_:.2f} s")
s_, _, _ = shift(260.0, 1e-4)
sign(f"{s_}", "negative")
quantity(f"{s_} s", "-9 s", rel_tol=0.5)
for Dm in (200.0, 230.0, 260.0, 275.0):
    print(f"Dm = {Dm} neV, theta0 = 1e-4: shift = {shift(Dm, 1e-4)[0]:.2f} s")
raise SystemExit(finish())
