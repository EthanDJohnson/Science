"""M-MECHANIST-07 (F8, F9, O3): J-PARC tau = (neutron-density term)/S_beta. An unsubtracted
background fraction b of S_beta gives tau_meas = tau_true/(1+b). To move 887.97 -> 877.2 s,
b = 887.97/877.2 - 1. D-25 backgrounds (fractions of S_beta). s (SI)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, limit, finish

d = 877.2 - 887.97
b = 887.97 / 877.2 - 1
print(f"shift = {d:.2f} s, needed background fraction = {b*100:.3f} %")
quantity(f"{d} s", "-10.8 s", rel_tol=0.01)
quantity(f"{b}", "0.0123", rel_tol=0.01)
limit("(1/(1+b) - 1)/(-b)", "b", 0, 1)
ex100 = (4.9 - 1.3, 5.4 - 1.2)
ex50 = (3.1 - 0.67, 3.3 - 0.65)
print(f"excess 100 kPa {ex100[0]:.2f}-{ex100[1]:.2f} %, 50 kPa {ex50[0]:.2f}-{ex50[1]:.2f} %")
quantity(f"{ex100[0]}", "3.6", rel_tol=0.01)
quantity(f"{ex100[1]}", "4.2", rel_tol=0.01)
quantity(f"{ex50[0]}", "2.4", rel_tol=0.02)
quantity(f"{ex50[1]}", "2.6", rel_tol=0.02)   # 2.65 printed as 2.6
print(f"third of 100 kPa excess = {ex100[0]/3:.2f}-{ex100[1]/3:.2f} %")
print(f"needed/excess: {b*100/ex100[1]:.2f} (of 4.2 %) to {b*100/ex50[0]:.2f} (of 2.43 %)")
quantity(f"{b*100/ex100[1]}", "0.3", rel_tol=0.05)
quantity(f"{b*100/ex50[0]}", "0.5", rel_tol=0.05)
raise SystemExit(finish())
