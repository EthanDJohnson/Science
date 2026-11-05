"""M-MECHANIST-10: SH0ES-CCHP split vs subset sampling noise (finding 9).
(a) Per-SN scatter: CCHP σ_SN = 0.70 km/s/Mpc on 70.39 over n = 24 SNe: σ_mag/sqrt(n) = (5/ln10)(0.70/70.39).
(b) Per-host total scatter s = sqrt(σ_SN,1² + 0.06²) (0.06 mag ASSUMED). For a simple random subset of n of N
    hosts (without replacement), Var(mean_n - mean_N) = s² (1/n - 1/N). Derived here symbolically from
    Var(mean_n) = s²/n·(N-n)/(N-1)·... check: mean_N = (n mean_n + (N-n) mean_rest)/N, independent parts.
(c) Observed splits 5 log10(73.18/70.39), 5 log10(73.18/68.81), and the "sigma" multiples.
"""
import math
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/mechanist")
import sympy as sp
from math_checks import identity, limit, finish
from mm_common import dmag, near

n, N, s = sp.symbols("n N s", positive=True)
# mean_N - mean_n = (N-n)/N (mean_rest - mean_n); Var = ((N-n)/N)^2 (s^2/(N-n) + s^2/n)
var = ((N - n) / N) ** 2 * (s**2 / (N - n) + s**2 / n)
identity(var, s**2 * (1 / n - 1 / N))
limit("s**2*(1/n - 1/Ntot)", "n", "Ntot", "0")   # full sample -> no difference

per_sn = (5 / math.log(10)) * (0.70 / 70.39) * math.sqrt(24)
near("per-SN scatter mag", per_sn, 0.105, 0.002)
sh = math.hypot(per_sn, 0.06)
for k, NN, claim in [(24, 35, 0.014), (11, 35, 0.030), (11, 55, 0.033)]:
    near(f"subset {k} of {NN} sigma mag", sh * math.sqrt(1 / k - 1 / NN), claim, 0.0012)
d1, d2 = dmag(73.18, 70.39), dmag(73.18, 68.81)
near("split 70.39", d1, 0.084, 0.0006)
near("split 68.81", d2, 0.134, 0.0006)
print(f"split/σ: 0.084 mag = {d1/(sh*math.sqrt(1/24-1/35)):.1f}σ (24 of 35), {d1/(sh*math.sqrt(1/11-1/35)):.1f}σ (11 of 35); "
      f"0.134 mag = {d2/(sh*math.sqrt(1/11-1/35)):.1f}σ (11 of 35)")
print(f"'~2σ' of sampling noise = {2*sh*math.sqrt(1/24-1/35):.3f} mag (24/35) or {2*sh*math.sqrt(1/11-1/35):.3f} mag (11/35)")
near("JAGB 0.11 mag fraction", 0.11 / dmag(73.264, 67.19), 0.59, 0.006)
near("JAGB 0.11 mag in H0 %", 100 * (10 ** (0.11 / 5) - 1), 5.2, 0.05)
near("0.17 mag fraction", 0.17 / dmag(73.264, 67.19), 0.90, 0.006)
raise SystemExit(finish())
