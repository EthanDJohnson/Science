"""M-MECHANIST-02: perspective term. Δv_p ≈ v_sys * θ, θ = s/d (small angle, rad). v_sys = 40 km/s,
s = 20 kau, M = 1.5 Msun. Lens: Δv_p/v_c = 0.15 at d = 100 pc, 0.30 at d = 50 pc (SI throughout)."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import quantity, identity, limit, finish
GM_sun = 1.3271244e20; AU = 1.495978707e11; PC = AU * 648000 / math.pi
vc = math.sqrt(GM_sun * 1.5 / (20e3 * AU))
for d_pc, lens in [(100, 0.15), (50, 0.30)]:
    theta = 20e3 * AU / (d_pc * PC)
    dv = 40e3 * theta
    print(f"d = {d_pc} pc: theta = {theta:.3e} rad = {theta*206265:.1f} arcsec; dv = {dv:.2f} m/s; dv/v_c = {dv/vc:.4f} (lens {lens})")
    quantity(f"40 km/s * (20e3 au)/({d_pc} pc) / (G*1.5*Msun/(20e3 au))^0.5", f"{lens}", rel_tol=0.03)
# exact geometry: the perspective difference of two lines of sight separated by theta is v_sys*sin(theta) (transverse)
th, v = sp.symbols("theta v", positive=True)
limit(v * sp.sin(th) / (v * th), "theta", 0, "1")
# dv/v_c scales as s^(3/2)/d
s, d, G, Mm = sp.symbols("s d G M", positive=True)
identity((v * s / d) / sp.sqrt(G * Mm / s), v * s**sp.Rational(3, 2) / (d * sp.sqrt(G * Mm)))
raise SystemExit(finish())
