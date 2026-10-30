"""M-DIALECTICIAN-02: subset-noise sigma for the SH0ES/CCHP selection effect (F2; C-I prediction ii).

Model: per-SN standardised residuals iid with scatter s (mag). For a subset of n drawn from N,
mean_sub - mean_all = (1 - n/N) mean_sub - (1/N) sum_rest, so
Var = s^2 (1/n - 1/N).  For two disjoint sets: Var = s^2 (1/n1 + 1/n2).
Converted to H0 by dH0 = H0 * ln10/5 * dM. Checked independently by Monte Carlo.
Inputs: s = 0.105-0.130 mag (M-01); n = 11 of N = 42; disjoint 11 vs 24; reference H0 ~ 70-73.
Observed differences: 73.75 (mid of 73.6-73.9) - 71.2 = 2.55 [D-28]; 74.1 - 70.39 = 3.71 [D-27, D-24].
"""
import sys, math, random
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, limit, inequality, units, finish
import sympy as sp

s, n, N = sp.symbols("s n N", positive=True)
# symbolic derivation of Var(mean_sub - mean_all) for nested subset
var_nested = (1 - n / N) ** 2 * s**2 / n + (N - n) * s**2 / N**2
identity(sp.simplify(var_nested), s**2 * (1 / n - 1 / N))
# limit: subset = full set gives zero noise
limit(s**2 * (1 / n - 1 / N), "n", N, 0)

# Monte Carlo cross-check (nested 11 of 42, s = 1)
rng = random.Random(3)
diffs = []
for _ in range(40000):
    x = [rng.gauss(0, 1) for _ in range(42)]
    diffs.append(sum(x[:11]) / 11 - sum(x) / 42)
mc = math.sqrt(sum(d * d for d in diffs) / len(diffs))
print(f"MC sd nested 11/42 (s=1): {mc:.4f}; analytic {math.sqrt(1/11 - 1/42):.4f}")
inequality(f"abs({mc} - {math.sqrt(1/11 - 1/42)})", "<=", "0.005")

k = math.log(10) / 5
rows = []
for sSN in (0.105, 0.130):
    for H0 in (70.0, 73.0):
        a = H0 * k * sSN * math.sqrt(1 / 11 - 1 / 42)
        b = H0 * k * sSN * math.sqrt(1 / 11 + 1 / 24)
        rows.append((sSN, H0, a, b, 2.55 / a, 3.71 / b))
        print(f"s={sSN} mag H0={H0}: nested sigma={a:.3f}, disjoint sigma={b:.3f} km/s/Mpc; "
              f"2.55/nested={2.55/a:.2f} sigma; 3.71/disjoint={3.71/b:.2f} sigma")
nest = [r[2] for r in rows]; disj = [r[3] for r in rows]
z1 = [r[4] for r in rows]; z2 = [r[5] for r in rows]
print(f"ranges: nested {min(nest):.2f}-{max(nest):.2f}; disjoint {min(disj):.2f}-{max(disj):.2f}; "
      f"z1 {min(z1):.2f}-{max(z1):.2f}; z2 {min(z2):.2f}-{max(z2):.2f}")
# lens: nested 0.89-1.10, disjoint 1.25-1.55, z1 2.3-2.9, z2 2.4-3.0
inequality(f"abs({min(nest)} - 0.89)", "<=", "0.03")
inequality(f"abs({max(nest)} - 1.10)", "<=", "0.03")
inequality(f"abs({min(disj)} - 1.25)", "<=", "0.03")
inequality(f"abs({max(disj)} - 1.55)", "<=", "0.03")
inequality(f"abs({min(z1)} - 2.3)", "<=", "0.1")
inequality(f"abs({max(z1)} - 2.9)", "<=", "0.1")
inequality(f"abs({min(z2)} - 2.4)", "<=", "0.1")
inequality(f"abs({max(z2)} - 3.0)", "<=", "0.1")
units("2.55 km/s/Mpc / (1.10 km/s/Mpc)", "dimensionless")
raise SystemExit(finish())
