"""M-EXAMINER-09: deciding precision (F12, Lens table A 'Settle').
Two point hypotheses H_a, H_b; a measurement with Gaussian total error sigma separates them at n sigma when
|H_a - H_b|/sigma = n, so sigma_req = gap/n; percentage quoted relative to 73.3."""
import sys
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/examiner")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, quantity, units, finish

identity("(a - b)/((a - b)/n)", "n", domain={"a": (71, 80), "b": (60, 70), "n": (1, 6)})
rows = [(73.3, 67.2, 6.1, 2.03, 2.77, 1.22, 1.66), (73.3, 70.0, 3.3, 1.10, 1.50, 0.66, 0.90), (73.3, 68.5, 4.8, 1.60, 2.18, 0.96, 1.31)]
for a, b, g, s3, p3, s5, p5 in rows:
    print(a, b, "gap", a - b, "3sig", (a - b) / 3, 100 * (a - b) / 3 / a, "5sig", (a - b) / 5, 100 * (a - b) / 5 / a)
    quantity(f"{a} - {b}", f"{g}", rel_tol=1e-9)
    quantity(f"({a} - {b})/3", f"{s3}", rel_tol=3e-3); quantity(f"100*({a} - {b})/3/{a}", f"{p3}", rel_tol=3e-3)
    quantity(f"({a} - {b})/5", f"{s5}", rel_tol=3e-3); quantity(f"100*({a} - {b})/5/{a}", f"{p5}", rel_tol=3e-3)
units("(73.3 km/s/Mpc - 67.2 km/s/Mpc)/3", "km/s/Mpc")
raise SystemExit(finish())
