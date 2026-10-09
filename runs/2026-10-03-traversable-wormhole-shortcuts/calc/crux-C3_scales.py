"""Crux C3: reconcile the two single-scale self-consistency estimates in the
C3 verdicts (C3-0 typical-Casimir estimate vs C3-2 Ford-Roman QI ceiling) and
express each as curvature in species-cutoff units; plus thresholds used in the
deciding tests.

Units: geometric (G = c = 1, lengths in m) unless marked SI.
Inputs are taken from the verdicts' printed logs (cited in cruxes/C3.md).
"""
import math

l_P = 1.616e-35  # m (dossier convention line in C3-2 verdict)

# --- C3-0: R_max = sqrt(8 alpha eta N) l_P  -> R_max / l_sp = sqrt(8 alpha eta)
cases0 = {
    "alpha=1/(2880 pi^2), eta=1": (1/(2880*math.pi**2), 1.0),
    "alpha=pi^2/720, eta=10": (math.pi**2/720, 10.0),
}
print("C3-0 typical-state estimate (R_max/l_sp = sqrt(8 alpha eta)):")
for k, (a, e) in cases0.items():
    r = math.sqrt(8*a*e)
    print(f"  {k}: R_max/l_sp = {r:.4g}; curvature (l_sp/R)^2 = {1/r**2:.4g}")

# --- C3-2: QI ceiling a_max / l_* = 4.886e3 (f=0.01), 48.86 (f=0.1)
print("C3-2 Ford-Roman QI ceiling (a_max/l_*):")
for f, ratio in [(0.01, 4.886e3), (0.1, 48.86)]:
    print(f"  f={f}: a_max/l_* = {ratio:.4g}; curvature in cutoff units (l_*/a)^2 = {1/ratio**2:.4g}")
    # coefficient alpha*eta a state would need to reach the QI ceiling, in C3-0's parametrisation
    ae = ratio**2/8
    print(f"     alpha*eta needed to reach that ceiling in C3-0's form = {ae:.4g}")
    for k, (a, e) in cases0.items():
        print(f"     ratio to C3-0 case [{k}]: {ae/(a*e):.3g}")

# --- Gap between 'typical Casimir' and 'QI-allowed' throat sizes
r0_hi = math.sqrt(8*(math.pi**2/720)*10)
print(f"Gap in throat size, QI ceiling (f=0.01) / generous typical estimate: {4.886e3/r0_hi:.4g}")

# --- Time-machine lag for a short throat (T_thru -> 0): Delta_CTC = d/c (SI)
c = 2.99792458e8
for name, d in [("1 m", 1.0), ("1 AU", 1.495978707e11), ("1 ly", 9.4607e15)]:
    print(f"Delta_CTC (short throat) at d = {name}: {d/c:.4g} s")

# --- C7 window at MM scale: width 2d/c, d = ell = 3e3 ly
yr = 3.15576e7
d_ly = 3.0e3
print(f"C7 window width 2d/c at d = 3e3 ly: {2*d_ly:.4g} yr")
T_thru = math.pi*d_ly  # yr, pi*ell/c with ell = 3e3 ly
print(f"MM T_thru = pi*ell/c = {T_thru:.4g} yr; Delta_s = {T_thru-d_ly:.4g} yr; Delta_CTC = {T_thru+d_ly:.4g} yr")

# --- FGM 2018 threshold |dV| > 2 ell exp(-pi r+/ell) (units of ell), sample r+/ell
for rp in [0.5, 1.0, 2.0, 3.0]:
    print(f"FGM2018 shortcut threshold |dV|/ell > {2*math.exp(-math.pi*rp):.4g} at r+/ell = {rp}")
