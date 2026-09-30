"""M-CONSTRAINTS-13 (F15, K9): n -> n' arithmetic. Regeneration (n -> n' -> n) through two alike passages has
p = P^2, so P_max = sqrt(p_lim). Needed conversion P_trap = 1 - tau_UCN/tau_BL1. Resonance field B_res = dm/|mu_n|.
Landau-Zener passage probability through the resonance P = 1 - exp(-2 pi theta0^2 dm^2 / (hbar |d(mu B)/dt|)),
used here only to find the field gradient that the lens's quoted P = 0.167 implies (the SNS profile is not given)."""
import math
from _common import near, TAU_UCN, TAU_BL1
from math_checks import identity, quantity, finish

identity("sqrt(p)**2", "p")
Pmax = math.sqrt(2.5e-8)
need = 1 - TAU_UCN / TAU_BL1
near("P per passage", Pmax, 1.6e-4, 6e-6)
near("shortfall factor", need / Pmax, 70, 1.0)
near("regeneration at P = 0.167", 0.167**2, 3e-2, 0.003)
near("over limit", 0.167**2 / 2.5e-8, 1.1e6, 0.06e6)
near("tau ratio worked example", 1 / (1 - 0.0043), 1.0043, 6e-5)
mu_n = 6.0307e-8   # eV/T (|mu_n| = 1.91304 mu_N)
Bres = 280e-9 / mu_n
print(f"   resonance field for dm = 280 neV: {Bres:.2f} T (lies between 4.6 T trap and 6.6 T SNS solenoid)")
quantity(f"{Bres!r}", "4.64", rel_tol=0.01)
# gradient implied by P = 0.167 at v = 1000 m/s, theta0 = 1e-3
hbar = 6.582119569e-16  # eV s
dm, th, v = 280e-9, 1e-3, 1000.0
rate_needed = 2 * math.pi * th**2 * dm**2 / (hbar * -math.log(1 - 0.167))   # eV/s
print(f"   P = 0.167 implies |dB/dz| = {rate_needed / mu_n / v:.2f} T/m at the resonance")
raise SystemExit(finish())
