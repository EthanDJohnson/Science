#!/usr/bin/env python3
"""lens-constraints: candidate negative-energy sources vs the Alcubierre-wall requirement (SI units).

 1. Casimir, ideal parallel plates [D-03]: rho = -pi^2 hbar c/(720 a^4).  Normal pressure from
    P = -d(E/A)/da with E/A = rho a (derived here: p_z = 3 rho); lateral pressures from tracelessness of
    the Maxwell stress tensor (assumption: conformal field), p_x = p_y = -rho.  Energy conditions.
    Plate rest energy per area vs Casimir energy per area (net sign of the cavity's energy).
 2. Free-field states (squeezed vacuum, moving mirrors): Ford-Roman bound [D-04] |<rho>| <= 3 hbar/(32 pi^2 c^3 tau^4)
    per scalar-equivalent field; energy scale |rho| (c tau)^3; why the bound does not apply to Casimir.
 3. Gaps (orders of magnitude) to the wall requirement from lens-constraints_alcubierre_ec.py and _qi_wall.py.
 4. LABELLED SPECULATIVE: non-minimally coupled classical scalar. From S = int sqrt(-g)[R/(16 pi G) - (dphi)^2/2
    - xi R phi^2/2] the effective coupling is G_eff = G/(1 - 8 pi G xi phi^2); the critical amplitude is
    phi_c = E_Planck/sqrt(8 pi xi).  Order-of-magnitude matching xi d^2(phi^2) ~ G_ab/(8 pi G) ~ v^2/(32 pi G Delta^2)
    gives 8 pi G xi phi^2 ~ v^2/4, i.e. phi/phi_c ~ v/2, independent of Delta (scaling estimate, not a solution).
Run: python3 runs/smoke-constraints/calc/lens-constraints_sources.py
"""
import math
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from gr_tensors import C, G_NEWTON, HBAR

M_PROTON = 1.67262192369e-27        # kg, CODATA 2018 (input constant)
GEV = 1.602176634e-10               # J per GeV (exact SI)
E_PLANCK_GEV = math.sqrt(HBAR * C**5 / G_NEWTON) / GEV
print(__doc__.split(" 1.")[0])
print(f"hbar c = {HBAR * C:.5e} J m; m_p = {M_PROTON} kg; E_Planck = {E_PLANCK_GEV:.4e} GeV")

# ---------------------------------------------------------------- 1. Casimir
print("\n== 1. Casimir cavity, ideal plates [D-03] (zero temperature, perfect conductors)")
mu_min = M_PROTON / (0.3e-9) ** 2   # one nucleon per (0.3 nm)^2: generous lower bound on any solid plate
print(f"   plate areal mass lower bound mu_min = m_p/(0.3 nm)^2 = {mu_min:.3e} kg/m^2 (assumption; a real monolayer is heavier)")
print(f"   {'a':>8s} {'rho (J/m^3)':>12s} {'p_z (Pa)':>11s} {'p_x (Pa)':>10s} {'rho+p_z':>11s} {'rho+p_x':>8s} {'E_C/A (J/m^2)':>13s} "
      f"{'2 mu_min c^2/|E_C/A|':>20s} {'mu_crit (kg/m^2)':>16s}")
cas = {}
for a in (1e-9, 1e-8, 1e-7, 1e-6):
    rho = -math.pi**2 * HBAR * C / (720 * a**4)
    EA = lambda aa: -math.pi**2 * HBAR * C / (720 * aa**3)
    h = a * 1e-6
    pz = -(EA(a + h) - EA(a - h)) / (2 * h)          # pressure on the plates = stress T^zz between them
    px = -rho                                         # tracelessness: -rho + 2 p_x + p_z = 0
    ratio = 2 * mu_min * C**2 / abs(EA(a))
    mu_crit = abs(EA(a)) / C**2
    cas[a] = rho
    print(f"   {a:8.0e} {rho:+12.3e} {pz:+11.3e} {px:+10.3e} {rho + pz:+11.3e} {rho + px:+8.1e} {EA(a):+13.3e} {ratio:20.3e} {mu_crit:16.3e}")
print("   p_z / rho = 3 (checked numerically above); NEC fails for null rays normal to the plates (rho + p_z = 4 rho < 0),")
print("   is marginal parallel to them (rho + p_x = 0); SEC: rho + sum p = 2 rho < 0; WEC, DEC: rho < 0.")
print("   Net cavity energy per area is positive unless plate areal mass < mu_crit, i.e. < ~1e-17 kg/m^2 even at a = 1 nm.")

# ---------------------------------------------------------------- 2. free-field QI budget
print("\n== 2. Ford-Roman bound [D-04] for free-field negative energy (squeezed states etc.), N = 1 scalar-equivalent")
print(f"   {'tau0':>8s} {'max |<rho>| (J/m^3)':>20s} {'|rho| (c tau0)^3 (J)':>21s}")
for tau in (1e-21, 1e-18, 1e-15, 1e-14, 1e-12, 1e-9, 1.0):
    q = 3 * HBAR / (32 * math.pi**2 * C**3 * tau**4)
    print(f"   {tau:8.0e} {q:20.3e} {q * (C * tau) ** 3:21.3e}")
q1s = 3 * HBAR / (32 * math.pi**2 * C**3 * 1.0**4)
print(f"   A Casimir cavity (a = 1 um) keeps rho = {cas[1e-6]:.2e} J/m^3 for as long as one likes, while the boundary-free")
print(f"   bound at tau0 = 1 s is {q1s:.1e} J/m^3 and -> 0 as tau0 -> infinity: the [D-04] form assumes no boundaries, so it")
print("   does not constrain Casimir sources (their limits are plate spacing and plate mass instead).")

# ---------------------------------------------------------------- 3. gaps to the requirement
print("\n== 3. Orders-of-magnitude gap: required peak |rho| in the wall vs source capability")
req = {  # from lens-constraints_alcubierre_ec.py section 4 (R = 100 m) and _qi_wall.py section 5
    "v=1, Delta=1 m": 1.204e42, "v=1, Delta=1 mm": 1.204e48, "v=10, Delta=1 m": 1.204e44,
    "v=1, QI-limited wall (alpha=0.1, N=1)": 1.757e108,
}
for k, r in req.items():
    gaps = ", ".join(f"a={a:.0e} m: {math.log10(r / abs(cas[a])):.1f}" for a in (1e-9, 1e-7, 1e-6))
    print(f"   {k:40s} |rho_req| = {r:.2e} J/m^3 -> log10 gap to ideal Casimir [{gaps}]")
tau_wall = 0.1 * (2.3094 / 2.0) / C          # alpha = 0.1, r_c = 2.3094/sigma with sigma = 2/Delta, Delta = 1 m, v = 1
qi_wall = 3 * HBAR / (32 * math.pi**2 * C**3 * tau_wall**4)
print(f"   free fields in a 1 m wall (v = 1): trusted sampling time 0.1 r_c/c = {tau_wall:.2e} s -> QI allows {qi_wall:.2e} J/m^3;"
      f" required 1.20e42 -> exceeds the bound by 10^{math.log10(1.204e42 / qi_wall):.1f}")

# ---------------------------------------------------------------- 4. non-minimally coupled scalar (speculative)
print("\n== 4. LABELLED SPECULATIVE: non-minimally coupled classical scalar (outside the free-field QI assumptions)")
for xi in (1 / 6, 1.0, 1e4):
    phic = E_PLANCK_GEV / math.sqrt(8 * math.pi * xi)
    row = ", ".join(f"v={v}: phi ~ {0.5 * v * phic:.1e} GeV ({'above' if 0.5 * v >= 1 else 'below'} phi_c)" for v in (0.1, 1.0, 2.0, 10.0))
    print(f"   xi = {xi:8.4g}: phi_c = {phic:.3e} GeV; need phi ~ (v/2) phi_c -> {row}")
print("   For v >= 2 the required amplitude reaches phi_c, where G_eff = G/(1 - 8 pi G xi phi^2) diverges and changes sign.")
