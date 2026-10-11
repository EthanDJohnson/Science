"""M-EMPIRICIST-03: pairwise tensions (empiricist F3).

z = (gamma_hi - gamma_lo) / sqrt(sigma_hi,down^2 + sigma_lo,up^2)   (facing-side errors, independent).
Claims: Chae 2024b (stat+syst) vs Boufourou E2: 2.51; stat only 3.50; Chae 2024b vs Banik(gamma): 2.91;
Chae+26 vs Saad & Ting 36-pair: 2.16; Chae 2023 vs Banik: 6.6. gamma dimensionless.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, limit, sign, inequality, finish

def z(hi, hi_dn, lo, lo_up):
    return (hi - lo) / (hi_dn**2 + lo_up**2) ** 0.5

c24b_dn_tot = (0.09**2 + 0.09**2) ** 0.5
cases = {
    "Chae2024b(tot) vs BoufE2": (z(1.37, c24b_dn_tot, 1.045, 0.023), 2.51),
    "Chae2024b(stat) vs BoufE2": (z(1.37, 0.09, 1.045, 0.023), 3.50),
    "Chae2024b(tot) vs Banik gM=1.333": (z(1.37, c24b_dn_tot, 0.993, 0.022), 2.91),
    "Chae2024b(tot) vs Banik gM=1.44": (z(1.37, c24b_dn_tot, 0.991, 0.029), 2.91),
    "Chae+26 vs ST36": (z(1.60, 0.14, 1.00, 0.24), 2.16),
    "Chae2023 vs Banik gM=1.333": (z(1.43, 0.06, 0.993, 0.022), 6.6),
    "Chae2023 vs Banik gM=1.44": (z(1.43, 0.06, 0.991, 0.029), 6.6),
}
for k, (val, lens) in cases.items():
    print(f"{k}: z = {val:.3f} (lens {lens})")
    # agreement to the lens's rounding (0.01 for 2-decimal values, 0.05 for 6.6)
    tol = 0.05 if lens == 6.6 else 0.006
    print("NUMERIC", "PASS" if abs(val - lens) <= tol else "DIFF", k)

# limit: identical values give zero tension; sign: adding a systematic in quadrature lowers z
limit("D/sqrt(a**2 + b**2 + t**2)", "t", "oo", "0")
sign("D/sqrt(a**2 + b**2) - D/sqrt(a**2 + b**2 + t**2)", "positive")
identity("(x - x)/sqrt(a**2 + b**2)", "0")
inequality(str(cases["Chae2024b(tot) vs BoufE2"][0]), "<", str(cases["Chae2024b(stat) vs BoufE2"][0]))
raise SystemExit(finish())
