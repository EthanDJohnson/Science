"""M-MECHANIST-03: PM-noise floor. Per-star PM error σ_μ = 0.02 mas/yr per axis; relative velocity error per
axis = sqrt(2) σ_μ d (transverse velocity v = 4.74047 km/s * μ[arcsec/yr] * d[pc]). s = 20 kau, M = 1.5 Msun,
d = 100-200 pc. Lens: 0.05-0.10 v_c on DR3."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, units, finish
GM_sun = 1.3271244e20; AU = 1.495978707e11; PC = AU * 648000 / math.pi; YR = 365.25 * 86400
mas = math.pi / (180 * 3600 * 1000)
vc = math.sqrt(GM_sun * 1.5 / (20e3 * AU))
for d_pc in (100, 200):
    v1 = 0.02 * mas / YR * d_pc * PC
    vrel = math.sqrt(2) * v1
    print(f"d = {d_pc} pc: per-star {v1:.2f} m/s, relative (x sqrt2) {vrel:.2f} m/s; /v_c = {v1/vc:.4f} (single), {vrel/vc:.4f} (relative)")
quantity("4.74047 km/s * 1e-3", "1 au/yr * 1e-3", rel_tol=1e-4)  # 1 arcsec/yr at 1 pc = 1 au/yr
quantity("2^0.5 * 0.02e-3 au/yr * 100 / (G*1.5*Msun/(20e3 au))^0.5", "0.052", rel_tol=0.03)
quantity("2^0.5 * 0.02e-3 au/yr * 200 / (G*1.5*Msun/(20e3 au))^0.5", "0.104", rel_tol=0.03)
units("0.02e-3 au/yr * 100", "m/s")
raise SystemExit(finish())
