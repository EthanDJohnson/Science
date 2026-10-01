"""M-ENGINEER-14 (table, ENGINEER-E, cost line): Lentz 20-50 M_sun at 10c (0.2-0.5 M_sun x v^2, D-30a quoted)
=> 3.6e48-8.9e48 J; gaps vs NIF 8.6 MJ 41.6-42.0, vs 5.9e20 J/yr 27.8-28.2. Cost line: world energy
5.9e20 J/yr = 6.6 t/yr of mass-energy; M_shell = 4.51e27 kg => 'about 1e23 years of world output'
(versus F6's 23.8 orders); 2.38 M_J = 'roughly twice' Jupiter. SI."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/math/engineer")
from common import *
from math_checks import quantity, units, finish

for ms, Ec, gn, gw in ((20, 3.6e48, 41.6, 27.8), (50, 8.9e48, 42.0, 28.2)):
    E = ms * Msun * c**2
    rel(f"{ms} M_sun c^2 (J)", E, Ec, 0.01)
    near(f"gap vs NIF ({ms} M_sun)", lg(E / 8.6e6), gn, 0.05)
    near(f"gap vs world-year ({ms} M_sun)", lg(E / WORLD_YR), gw, 0.05)
near("0.2 M_sun x 10^2", 0.2 * 100, 20, 1e-9)
rel("world mass-energy per year (kg)", WORLD_YR / c**2, 6.6e3, 0.01)
yrs = 4.511e27 / (WORLD_YR / c**2)
print(f"  shell mass / (world mass-energy per year) = {yrs:.3g} years = 10^{lg(yrs):.2f}")
near("cost line: log10 years vs lens 'about 1e23'", lg(yrs), 23.0, 0.5)
quantity("5.9e20 J / c^2", "6.565 t", rel_tol=2e-3)
units("1 J / c^2", "kg")
raise SystemExit(finish())
