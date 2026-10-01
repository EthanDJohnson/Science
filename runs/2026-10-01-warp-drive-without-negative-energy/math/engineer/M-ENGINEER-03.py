"""M-ENGINEER-03 (F6, F7, table): build gaps log10(required/demonstrated) for the published shell
and for the same shell scaled x10 in radius at fixed compactness (R1 = 100 m, R2 = 200 m).
Inputs: M_ADM = 4.51e27 kg; peak eps = 1.376e40 J/m^3 and peak p_t = 3.874e39 Pa (our own rebuild,
M-ENGINEER-02); ISS 419,725 kg; world 5.9e20 J/yr; osmium 2.26e4 kg/m^3; nuclear 0.16 fm^-3;
1 TPa; Parker Solar Probe 6.4e-4 c (lens's D-45 figure, quoted). Scaling at fixed C:
M x10, density /100, stress /100 (TOV self-similarity, checked in M-ENGINEER-04). SI."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/math/engineer")
from common import *
from math_checks import quantity, units, finish

M, eps, pt = 4.511e27, 1.376e40, 3.874e39
ISS = 419725.0
rho = eps / c**2
print(f"rho_nuc = {RHO_NUC:.4g} kg/m^3, rho_nuc c^2 = {RHO_NUC*c**2:.4g} Pa")
near("mass gap vs ISS", lg(M / ISS), 22.0, 0.05)
rel("Mc^2 (J)", M * c**2, 4.0e44, 0.02)
near("energy gap vs world-year", lg(M * c**2 / WORLD_YR), 23.8, 0.05)
near("density gap vs osmium", lg(rho / RHO_OS), 18.8, 0.05)
near("density gap vs nuclear", lg(rho / RHO_NUC), 5.8, 0.05)
near("stress gap vs 1 TPa", lg(pt / 1e12), 27.6, 0.05)
near("stress gap vs rho_nuc c^2", lg(pt / (RHO_NUC * c**2)), 5.2, 0.05)
rel("rho_nuc c^2 (Pa)", RHO_NUC * c**2, 2.4e34, 0.02)
near("speed gap 0.02c vs Parker 6.4e-4c", lg(0.02 / 6.4e-4), 1.5, 0.05)
near("speed gap 0.04c vs Parker 6.4e-4c", lg(0.04 / 6.4e-4), 1.8, 0.05)
print("x10 shell (fixed compactness, ours):")
M10 = 10 * M
rel("M (kg)", M10, 4.5e28, 0.01)
near("M in M_J", M10 / Mjup, 23.8, 0.05)
near("mass gap", lg(M10 / ISS), 23.0, 0.05)
near("energy gap", lg(M10 * c**2 / WORLD_YR), 24.8, 0.05)
near("density over nuclear", lg(rho / 100 / RHO_NUC), 3.8, 0.05)
near("stress over 1 TPa", lg(pt / 100 / 1e12), 25.6, 0.05)
quantity("4.511e27 kg * c^2", "4.054e44 J", rel_tol=2e-3)
units("1 kg/m^3 * c^2", "Pa")
raise SystemExit(finish())
