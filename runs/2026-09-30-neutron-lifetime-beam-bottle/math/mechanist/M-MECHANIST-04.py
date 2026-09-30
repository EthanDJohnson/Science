"""M-MECHANIST-04 (F5, F13, M2): residual-gas proton loss in BL1.
Loss probability for a proton stored time t: P = 1 - exp(-n sigma v t) ~ n sigma v t.
Protons born uniformly in a cycle of length T and all released at its end: mean storage T/2.
Assumptions (the lens's): E_p ~ 300 eV, sigma = 1e-20..1e-19 m^2, T = 10 ms, T_gas = 300 K. SI."""
import math, sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, units, finish

eV = 1.602176634e-19; mp = 1.67262192369e-27; kB = 1.380649e-23
v = math.sqrt(2 * 300 * eV / mp)
print(f"v(300 eV proton) = {v:.4e} m/s")
quantity(f"{v} m/s", "2.4e5 m/s", rel_tol=0.01)
quantity("2 * 300 eV / (1.67262192369e-27 kg)", f"{v**2} m^2/s^2", rel_tol=1e-6)

# mean storage time for uniform birth over [0,T]: (1/T) int_0^T (T - t0) dt0 = T/2
t0, T, r = sp.symbols("t0 T r", positive=True)
identity(sp.integrate(T - t0, (t0, 0, T)) / T, T / 2)
# averaged survival (1/T) int exp(-r(T-t0)) -> loss ~ rT/2 at small r
avg_loss = 1 - sp.integrate(sp.exp(-r * (T - t0)), (t0, 0, T)) / T
limit(avg_loss / (r * T), "r", 0, sp.Rational(1, 2))

f = 1 - 877.82 / 887.97
t = 5e-3
for sig in (1e-20, 1e-19):
    n = f / (sig * v * t)
    p = n * kB * 300
    print(f"sigma={sig:g} m^2: n = {n:.3e} m^-3, p = {p:.3e} Pa = {p/100:.3e} mbar")
n_lo, n_hi = f / (1e-19 * v * t), f / (1e-20 * v * t)
quantity(f"{n_hi*kB*300} Pa", "4e-6 Pa", rel_tol=0.05)
quantity(f"{n_lo*kB*300} Pa", "4e-7 Pa", rel_tol=0.05)
units("1e15 m^-3 * 1.380649e-23 J/K * 300 K", "Pa")

# 10 ms vs 5 ms subsets, lens's reading: loss 1.143 % at 10 ms, half at 5 ms
tau0 = 877.82
d_lens = tau0 / (1 - f) - tau0 / (1 - f / 2)
print(f"split (all 1.143 % at 10 ms cycle) = {d_lens:.3f} s")
quantity(f"{d_lens} s", "5.1 s", rel_tol=0.01)
# alternative: equal-weight mix of the two subsets gives average loss 1.143 %: loss10 = 4f/3
f10 = 4 * f / 3
d_mix = tau0 / (1 - f10) - tau0 / (1 - f10 / 2)
print(f"split if data are an equal mix of 5 and 10 ms and the mix averages 1.143 %: {d_mix:.3f} s")

# Caylor ~0.3 %
c = 0.003
dc = 887.97 * c
print(f"Caylor 0.3 % of 887.97 s = {dc:.3f} s = {dc/(887.97-877.82)*100:.1f} % of the gap")
quantity(f"{dc} s", "2.7 s", rel_tol=0.02)
quantity(f"{dc/(887.97-877.82)}", "0.26", rel_tol=0.02)
# F13: needed density scales as 1/(1 - eps_ion)
e = sp.symbols("e", positive=True)
limit(f / (1 - e) / f, "e", 0, 1)
raise SystemExit(finish())
