"""M-DIALECTICIAN-01: per-SN calibrator scatter from dossier error terms (F1).

Model: the calibrator term in the error budget is the standard error of the mean of n iid
per-SN residuals, sigma_mean = sigma_SN / sqrt(n). Converting an H0 error to magnitudes:
H0 ∝ 10^(0.2 M_B)  =>  dM = (5/ln10) dH0/H0.
Inputs (dossier): R22 'SN calibrator statistics 0.020 mag', n = 42 (D-20/§6);
CCHP sigma_SN = 0.70 km/s/Mpc on H0 = 70.39 km/s/Mpc, n = 24 (D-24).
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, limit, inequality, quantity, units, finish
import sympy as sp

# derivative relation dM/dlnH0 = 5/ln10 (symbolic)
H = sp.symbols("H", positive=True)
identity(sp.diff(5 * sp.log(H, 10), H) * H, 5 / sp.log(10))
# small-offset limit: 5 log10(1+x) / x -> 5/ln10
limit("5*log(1+x, 10)/x", "x", 0, "5/log(10)")

s_r22 = 0.020 * math.sqrt(42)
dm_cchp = 5 / math.log(10) * 0.70 / 70.39
s_cchp = dm_cchp * math.sqrt(24)
print(f"R22: 0.020 mag * sqrt(42) = {s_r22:.4f} mag")
print(f"CCHP: 0.70/70.39 km/s/Mpc -> {dm_cchp:.5f} mag; * sqrt(24) = {s_cchp:.4f} mag")
inequality(f"abs({s_r22} - 0.130)", "<=", "0.0010")
inequality(f"abs({s_cchp} - 0.105)", "<=", "0.0010")
# units: the H0 error ratio is dimensionless
units("0.70 km/s/Mpc / (70.39 km/s/Mpc)", "dimensionless")
raise SystemExit(finish())
