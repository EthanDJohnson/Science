"""M-DECOMPOSER-09: arithmetic in F7 and Q5, using the lens's own table values (dimensionless).
Table: (mass fraction f, compactness C = f * 0.3334, beta_NEC, beta_adv).
Also: D-dependence of the light-shell advance (F5): the thin-shell Shapiro term grows by
(2 G f M / c^3) * 2 ln(D2/D1) between D1 and D2, SI."""
import sys
import math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, inequality, finish

rows = [(0.001, 1e-4, 2.1e-3), (0.01, 3e-4, 0.021), (0.1, 2.8e-3, 0.225), (0.5, 0.0132, None), (1.0, 0.0246, None)]
C0 = 0.3334
for f, bn, ba in rows:
    C = f * C0
    print(f"f = {f}: C = {C:.3e}, beta_NEC/C = {bn/C:.4f}" + (f", beta_adv/beta_NEC = {ba/bn:.1f}" if ba else ""))
ratios_adv = [ba / bn for f, bn, ba in rows if ba]
print("advance/NEC factors:", [round(x, 1) for x in ratios_adv], "-> claimed '8 to 80'")
quantity(f"{min(ratios_adv)}", "8", rel_tol=0.25)          # claimed lower end
quantity(f"{max(ratios_adv)}", "80", rel_tol=0.05)
r_above = [bn / (f * C0) for f, bn, ba in rows[1:]]
print("beta_NEC/C for rows above the lowest:", [round(x, 4) for x in r_above], "-> claimed 0.074-0.084")
quantity(f"{max(r_above)}", "0.084", rel_tol=0.03)
quantity(f"{min(r_above)}", "0.074", rel_tol=0.03)
print(f"f=0.01 row with +-6e-5: ratio in [{(3e-4-6e-5)/(0.01*C0):.3f}, {(3e-4+6e-5)/(0.01*C0):.3f}]")
print("extrapolation to 8/9 with 0.074-0.084:", 0.074 * 8 / 9, 0.084 * 8 / 9, "; with 0.091:", 0.091 * 8 / 9)
quantity(f"{0.084*8/9}", "0.07", rel_tol=0.08)
print("0.02 vs cap 0.0246: below by", 1 - 0.02 / 0.0246)
quantity(f"{1 - 0.02/0.0246}", "0.20", rel_tol=0.1)
quantity("4.49e27 / 1e5", "4.5e22", rel_tol=0.01)   # shell mass / payload mass, both kg
G, c = 6.67430e-11, 2.99792458e8
grow = 2 * G * (0.01 * 4.49e27) / c ** 3 * 2 * math.log(1e5 / 1e3) * 1e9
print(f"extra Shapiro delay, D 1e3 -> 1e5 m, f = 0.01: {grow:.2f} ns vs advance 1.87 ns -> at D = 1e5 m excess ~ {grow-1.87:+.2f} ns")
inequality(f"{grow}", ">", "1.87")
raise SystemExit(finish())
