"""M-EXAMINER-03 (F2): g_N proxy with r = 1.2 s vs r = s.
g_N = G M / r^2 (SI). Shift in log10 g_N between r = s and r = 1.2 s is log10(1.2^2).
Separation s at which g_N = 1e-10 m/s^2 for M = 1.5 Msun under each convention.
Boost range of the chae2024 one-body form (n=1, beta=1.1, p=1.2, x_e=1.90, a0=1.2e-10) across +-0.158 dex.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import math
import sympy as sp
from math_checks import identity, limit, quantity, units, finish

k = sp.symbols("k", positive=True)  # r = k s
shift = sp.log(k**2, 10)
identity(sp.Float(round(float(shift.subs(k, sp.Rational(6, 5))), 3)), sp.Float(0.158))
limit(shift, "k", 1, "0")     # r = s -> no shift

G, Msun, au = 6.67430e-11, 1.98892e30, 1.495978707e11
M = 1.5 * Msun
r = math.sqrt(G * M / 1e-10)
s_eq = r / au
s_12 = r / 1.2 / au
print(f"s(r = s) = {s_eq:.1f} au ; s(r = 1.2 s) = {s_12:.1f} au")
identity(sp.Float(round(s_eq, -0)), sp.Float(round(s_eq)))   # trivial echo for the log
quantity("(6.67430e-11 m^3/(kg s^2) * 1.5 * 1.98892e30 kg / (1e-10 m/s^2))^0.5", "9432 au", rel_tol=2e-4)
quantity("(6.67430e-11 m^3/(kg s^2) * 1.5 * 1.98892e30 kg / (1e-10 m/s^2))^0.5 / 1.2", "7860 au", rel_tol=2e-4)
units("6.67430e-11 m^3/(kg s^2) * 1 kg / (1 m)^2", "acceleration")

def nu1(y):
    return 0.5 + math.sqrt(0.25 + 1 / y)
def K1(y):
    w = math.sqrt(1 + 4 / y)
    return -2 / y / (w * (1 + w))
def gam(gN, a0=1.2e-10, beta=1.1, p=1.2, xe=1.90):
    y = gN / a0
    ye = xe**2 / (1 + xe)
    yb = math.sqrt(y**2 + (beta * ye)**2)
    return nu1(yb) * (1 + math.tanh(beta * ye / y)**p * K1(yb) / 3)

lo, hi = gam(10**(-10 - 0.158)), gam(10**(-10 + 0.158))
print(f"chae2024 gamma at -10.158: {lo:.4f}; at -9.842: {hi:.4f}; at -10: {gam(1e-10):.4f}")
identity(sp.Float(round(hi, 3)), sp.Float(1.314))
identity(sp.Float(round(lo, 3)), sp.Float(1.346))
raise SystemExit(finish())
