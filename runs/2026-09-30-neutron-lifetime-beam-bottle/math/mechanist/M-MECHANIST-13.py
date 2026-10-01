"""M-MECHANIST-13 (M8, G): Zeeman energy vs decay Q-value. |mu_n| B at 4.6 T and 5 T vs Q = 0.782 MeV.
An energy shift dE changes the Sargent-like rate by roughly dGamma/Gamma ~ 5 dE/Q (Gamma ~ Q^5), and at most
of order dE/Q times a number of order 1-5. The needed change is 1.14e-2. Energies in eV (SI-derived)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, series, finish

mu = 60.3077e-9   # eV/T
Q = 0.782e6       # eV
for B in (4.6, 5.0):
    r = mu * B / Q
    print(f"B = {B} T: mu*B = {mu*B*1e9:.1f} neV, ratio to Q = {r:.3e}")
r46 = mu * 4.6 / Q
quantity(f"{r46}", "4e-13", rel_tol=0.15)
series("(1 + x)**5", "x", 0, 2, "1 + 5*x")
need = 0.01143
print(f"needed / (dE/Q) = {need/r46:.3e} (log10 {__import__('math').log10(need/r46):.2f}); "
      f"needed / (5 dE/Q) = {need/(5*r46):.3e}")
quantity(f"{need/r46}", "1e10", rel_tol=2.5)     # 'broken by 10 orders of magnitude' (M8)
quantity(f"{need/r46}", "1e13", rel_tol=0.5)     # '10^13 too small' (G)
raise SystemExit(finish())
