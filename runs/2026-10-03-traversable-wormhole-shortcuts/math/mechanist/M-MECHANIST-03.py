"""M-MECHANIST-03: mouth-motion conversion (finding 7, O3).
A mouth moving at constant speed v (beta = v/c) relative to the exterior frame ages dtau = dt/gamma,
so the lag accumulates at rate 1 - 1/gamma per unit exterior time. Time to reach a target offset
Delta: t = Delta/(1 - 1/gamma). Kinetic energy per acceleration leg (gamma - 1) M c^2.
Circular motion at radius R and speed v needs a = gamma v^2/R ~ v^2/R; mutual gravity G M / R^2.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, series, quantity, units, finish

b = sp.symbols("b", positive=True)
gam = 1 / sp.sqrt(1 - b**2)
# small-speed limit: lag rate -> b^2/2 (Newtonian kinetic time dilation)
series(1 - 1 / gam, "b", 0, 4, "b**2/2")
series(gam - 1, "b", 0, 4, "b**2/2")

def lag(beta):
    return 1 - math.sqrt(1 - beta**2)
def gm1(beta):
    return 1 / math.sqrt(1 - beta**2) - 1

quantity(f"{lag(0.1)}", "5.0e-3", rel_tol=0.01)
quantity(f"{lag(0.9)}", "0.564", rel_tol=0.002)
# short throat, D = 1 ly: Delta_ctc = 1 yr
quantity(f"1 yr / {lag(0.1)}", "200 yr", rel_tol=0.01)
quantity(f"1 yr / {lag(0.9)}", "1.8 yr", rel_tol=0.02)
# short throat, D = 1 m: Delta_ctc = 3.34 ns
quantity(f"(1 m / c) / {lag(0.1)}", "0.67 us", rel_tol=0.01)
# MM: Delta_ctc = 1.04e4 yr, Delta_sc = 8.4e3 yr
Tw = math.pi * 3000
quantity(f"{Tw + 1e3} yr / {lag(0.1)}", "2.1e6 yr", rel_tol=0.02)
quantity(f"{Tw - 1e3} yr / {lag(0.1)}", "1.7e6 yr", rel_tol=0.02)
quantity(f"{Tw + 1e3} yr / {lag(0.9)}", "1.8e4 yr", rel_tol=0.03)
# energy per leg, M = 2.0e34 kg
quantity(f"{gm1(0.1)} * 2.0e34 kg * c^2", "9.1e48 J", rel_tol=0.01)
quantity(f"{gm1(0.1)} * 2.0e34 kg / Msun", "51", rel_tol=0.01)
quantity(f"{gm1(0.9)} * 2.0e34 kg * c^2", "2.3e51 J", rel_tol=0.02)
quantity(f"{gm1(0.9)} * 2.0e34 kg / Msun", "1.3e4", rel_tol=0.01)
quantity(f"{gm1(0.9)}", "1.29", rel_tol=0.005)
# out-and-back at 0.1c for the CTC time: turnaround distance = 0.1 c * t/2
quantity(f"0.1 * c * ({Tw + 1e3} yr / {lag(0.1)}) / 2", "1.0e5 ly", rel_tol=0.05)
# circling at R = 1e3 ly, v = 0.1c
quantity("(0.1 c)^2 / (1000 ly)", "9.5e-5 m/s^2", rel_tol=0.01)
quantity("2.0e34 kg * (0.1 c)^2 / (1000 ly)", "1.9e30 N", rel_tol=0.01)
quantity("G * 2.0e34 kg / (1000 ly)^2", "1.5e-14 m/s^2", rel_tol=0.02)
units("2.0e34 kg * (0.1 c)^2 / (1000 ly)", "force")
raise SystemExit(finish())
