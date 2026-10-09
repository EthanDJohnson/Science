"""Constraints lens: energy-condition table for the classical rows.
Geometric units G = c = 1, lengths in metres; SI via c^4/G (J/m^3, J/m^2) and c^2/G (kg).
A  Ellis-Bronnikov throat (Phi = 0, r = sqrt(l^2 + b0^2)), b0 = 1 m: stress, ECs, radial ANEC, convergence.
B  gr_tensors scan of NEC/WEC/SEC/DEC across the whole throat region (proper-distance chart),
   for Phi = 0 and for a bounded redshift Phi = -b0/r; curvature radius at the throat; precision check.
C  Morris-Thorne b = sqrt(r0 r), Phi = 0: rho > 0 for static observers but NEC fails; the radial
   boost speed above which a crossing observer measures negative energy density.
D  Slow-flare family r = b0 + sqrt(l^2 + L^2) - L: how small the radial ANEC can be made.
E  Thin shells (Visser): flat and Schwarzschild exteriors; sigma, P, 4D/surface ECs, shell ANEC, stability.
"""
import math
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
import numpy as np
import wormhole_tools as wt
from gr_tensors import Spacetime, to_si, PLANCK_LENGTH, M_SUN, G_NEWTON, C

c4G = C**4 / G_NEWTON
print("=== A. Ellis throat, b0 = 1 m ===")
b0 = 1.0
th = wt.ProperThroat("sqrt(l**2 + b0**2)", "0", {"b0": b0})
s = th.stress(0.0)
print(f"rho = {s['rho']:.6e} 1/m^2, p_l = {s['p_l']:.6e}, p_t = {s['p_t']:.6e}")
print(f"expected rho = p_l = -1/(8 pi b0^2) = {-1/(8*math.pi):.6e}; p_t = +{1/(8*math.pi):.6e}")
print(f"rho + p_l = {s['rho']+s['p_l']:.6e} 1/m^2 (expected -1/(4 pi) = {-1/(4*math.pi):.6e}) = {(s['rho']+s['p_l'])*c4G:.4e} J/m^3")
print(f"rho + p_l + 2 p_t = {s['rho']+s['p_l']+2*s['p_t']:.3e} (SEC trace part)")
print("ECs at throat:", th.energy_conditions(0.0))
a = th.anec()
print(f"ANEC full line: direct {a['anec_geom_per_m']:.8f} 1/m, by parts {a['anec_by_parts']:.8f}, closed form -1/8 = -0.125; agree={a['agree']}")
print(f"  SI: {a['anec_J_per_m2']:.4e} J/m^2 per unit E")
for Lc in (1e2, 1.5e2, 1e3, 1.5e3):
    af = th.anec(-Lc, Lc)
    print(f"  finite range |l| < {Lc:g} m: direct {af['anec_geom_per_m']:.6f}, by parts {af['anec_by_parts']:.6f}, boundary term {af['boundary_term']:.3e}")
# sign along the whole geodesic: rho + p_l at sampled l
ls = np.linspace(-50, 50, 2001)
vals = [th.stress(float(x))["rho"] + th.stress(float(x))["p_l"] for x in ls]
print(f"rho + p_l over l in [-50, 50] m (2001 pts): max {max(vals):.3e}, min {min(vals):.3e}; all negative: {all(v < 0 for v in vals)}")

print("\n=== B. gr_tensors scan across the throat region (proper-distance chart) ===")
t, l, thv, ph = sp.symbols("t l theta phi", real=True)
B0 = sp.symbols("b0", positive=True)
r_l = sp.sqrt(l**2 + B0**2)
for label, Phi in (("Phi = 0 (Ellis)", sp.Integer(0)), ("Phi = -b0/r (bounded redshift)", -B0 / r_l)):
    g = sp.diag(-sp.exp(2 * Phi), 1, r_l**2, r_l**2 * sp.sin(thv)**2)
    st = Spacetime(g, [t, l, thv, ph], simplify=True)
    params = {B0: 1.0}
    for n in (41, 61):
        pts = [(0.0, float(x), 1.1, 0.0) for x in np.linspace(-10, 10, n)]
        sc = st.scan_energy_conditions(pts, params)
        print(f"{label}, n={n} points on l in [-10,10] m: violations {sc['violations']} of {sc['points']} (skipped {sc['skipped']}); worst NEC {sc['worst']['nec_min'][0]:.4e} at l={sc['worst']['nec_min'][1][1]:.2f}")
    ec0 = st.energy_conditions((0.0, 0.0, 1.1, 0.0), params)
    print(f"  at throat: type {ec0['type']}, nec {ec0['nec']}, wec {ec0['wec']}, sec {ec0['sec']}, dec {ec0['dec']}, rho_observer {ec0['rho_observer']:.5e}")
    cv = st.curvature_at((0.0, 0.0, 1.1, 0.0), params)
    print(f"  curvature radius at throat {cv['curvature_radius']:.4f} m, Kretschmann {cv['kretschmann']:.4f} 1/m^4")
    # radial null T_kk with k = (e^{-Phi}, 1, 0, 0) (k^t from g_tt k^t k^t + k^l k^l = 0)
    T = st.stress_energy()
    k = [sp.exp(-Phi), 1, 0, 0]
    Tkk = sum(T[i, j] * k[i] * k[j] for i in range(4) for j in range(4))
    pc = st.precision_check(Tkk, [(0.0, 0.0, 1.1, 0.0), (0.0, 3.0, 1.1, 0.0)], params)
    print(f"  precision_check T_kk (radial null) at l=0 and l=3 m: {pc}")
th2 = wt.ProperThroat("sqrt(l**2 + b0**2)", "-b0/sqrt(l**2 + b0**2)", {"b0": 1.0})
a2 = th2.anec()
print(f"Phi = -b0/r: radial ANEC direct {a2['anec_geom_per_m']:.6f} 1/m, by parts {a2['anec_by_parts']:.6f}, agree={a2['agree']}")

print("\n=== C. Morris-Thorne b = r0 (1 + alpha (1 - r0/r)), alpha = 0.5, Phi = 0, r0 = 1 m: positive static density, finite ADM mass M = r0 (1+alpha)/2, NEC still fails ===")
mt = wt.MorrisThorne("r0*(1 + al*(1 - r0/r))", "0", r0=1.0, params={"r0": 1.0, "al": 0.5})
for r in (1.0, 1.5, 3.0, 10.0):
    sr = mt.stress(r)
    ec = mt.energy_conditions(r)
    print(f"r={r:5.1f} m: rho={sr['rho']:.4e} p_l={sr["p_r"]:.4e} p_t={sr['p_t']:.4e} rho+p_l={sr['rho']+sr["p_r"]:.4e}  NEC {ec['nec']} WEC {ec['wec']}")
sr = mt.stress(1.0)
v2 = -sr["rho"] / sr["p_r"]
print(f"radially boosted observer at throat sees gamma^2 (rho + v^2 p_l) < 0 for v > sqrt(-rho/p_l) = {math.sqrt(v2):.4f} c (expected sqrt(alpha) = 0.7071)")
am = mt.anec()
print(f"radial ANEC (both sheets): {am}")

print("\n=== D. Slow-flare family r = b0 + sqrt(l^2+L^2) - L, Phi = 0, b0 = 1 m ===")
for Lf in (1.0, 10.0, 100.0, 1e3, 1e4):
    thf = wt.ProperThroat("b0 + sqrt(l**2 + Lf**2) - Lf", "0", {"b0": 1.0, "Lf": Lf})
    af = thf.anec()
    s0 = thf.stress(0.0)
    est = -(1 / (4 * math.pi)) * (math.log(Lf / 1.0 + 1) ** 2 + 2) / Lf
    print(f"L/b0={Lf:8.0f}: ANEC {af['anec_geom_per_m']:.4e} 1/m (by parts {af['anec_by_parts']:.4e}, agree {af['agree']}); rho+p_l(throat) {s0['rho']+s0['p_l']:.4e} (expected -1/(4 pi b0 L) = {-1/(4*math.pi*Lf):.4e}); rho(throat) {s0['rho']:.4e}")

print("\n=== E. Thin-shell wormholes ===")
Msun_m = wt.mass_to_geom(M_SUN)
print(f"1 Msun = {Msun_m:.2f} m (geometric)")
cases = [("flat (M = 1e-9 m), a = 1 m", 1e-9, 1.0), ("flat, a = 1 km", 1e-9, 1e3),
         ("Schw 1 Msun, a = 2.5M", Msun_m, 2.5 * Msun_m), ("Schw 1 Msun, a = 3M", Msun_m, 3 * Msun_m),
         ("Schw 1 Msun, a = 4M", Msun_m, 4 * Msun_m), ("Schw 1 Msun, a = 10 km", Msun_m, 1e4)]
for lab, M, aa in cases:
    sh = wt.ThinShell.schwarzschild(M=M, a=aa)
    su = sh.surface()
    ec = sh.energy_conditions()
    an = sh.anec()
    stab = sh.stability()
    print(f"{lab}: sigma {su['sigma']:.4e} 1/m = {su['sigma_J_m2']:.4e} J/m^2; P {su['P_N_m']:.4e} N/m; m_s {sh.mass_kg():.4e} kg")
    print(f"   4D: nec {ec['nec']} wec {ec['wec']} sec {ec['sec']} dec {ec['dec']}; surface: nec {ec['nec_surface']} (sigma+P={ec['sigma_plus_P']:.3e}); shell ANEC {an['anec_geom_per_m']:.4e} 1/m = {an['anec_J_per_m2']:.4e} J/m^2")
    print(f"   stability: V''(beta2=0) {stab['V_pp_at_beta2_0']:.4e}, critical beta2 {stab['beta2_critical']:.4f}, stable if {stab['stable_if']}")
