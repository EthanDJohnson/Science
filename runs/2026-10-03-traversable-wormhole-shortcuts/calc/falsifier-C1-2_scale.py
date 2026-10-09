"""Falsifier C1-2 (scale angle): required vs achievable for C1's practice leg,
and the in-principle cost of a labelled-phantom (Bronnikov et al. 2013 type)
stable Ellis-metric shortcut carrying 1 kg. SI units throughout.
"""
import math

c = 2.99792458e8        # m/s
G = 6.67430e-11         # m^3 kg^-1 s^-2
hbar = 1.054571817e-34  # J s
eV = 1.602176634e-19    # J
ly = 9.4607e15          # m
yr = 3.15576e7          # s

print("=== 1. C1 practice leg: SM-MMP row, 1 kg payload vs binding ===")
m = 1.0
E_pay = m * c**2
# |E_min| range taken from M-ENGINEER-05 (verified): 7.17e-13 J (g=0.06,N=1) .. 5.23e-8 J (g=0.3,N=54)
for lab, Emin in [("g=0.06,N=1", 7.17e-13), ("g=0.06,N=54", 2.09e-9), ("g=0.3,N=54", 5.23e-8)]:
    print(f"{lab:12s} |E_min| = {Emin:.3e} J = {Emin/eV/1e9:.3e} GeV; 1 kg c^2/|E_min| = 10^{math.log10(E_pay/Emin):.2f}")

# extremal magnetic RN horizon field B_h = c/(sqrt(4 pi eps0 G) r_e)
eps0 = 8.8541878128e-12
r_e = hbar * c / (1e12 * eV)  # 1/TeV
B_h = c / (math.sqrt(4 * math.pi * eps0 * G) * r_e)
print(f"r_e = {r_e:.3e} m, B_h = {B_h:.3e} T; B_h/1200 T = 10^{math.log10(B_h/1200):.2f}")
M_mouth = r_e * c**2 / G
E_form = 2 * M_mouth * c**2
world = 5.92e20  # J/yr (anchor used by engineer lens)
print(f"mouth mass {M_mouth:.3e} kg; pair rest energy {E_form:.3e} J = {E_form/world:.3e} yr of world primary energy (10^{math.log10(E_form/world):.2f})")

# Could any MMP widening reach 1 kg at fixed SM species? |E_min| = g^2 hbar c/(256 pi r_e) falls as 1/r_e
g = 0.3
r_needed = g**2 * hbar * c / (256 * math.pi * E_pay)
print(f"SM-MMP widening: |E_min| >= 1 kg c^2 needs r_e <= {r_needed:.3e} m (Planck length 1.616e-35 m): "
      f"{'below' if r_needed < 1.616e-35 else 'above'} Planck length by 10^{math.log10(1.616e-35/r_needed):.1f}")

print()
print("=== 2. In principle: labelled-phantom stable Ellis throat (Bronnikov et al. 2013 metric) ===")
# Ellis metric, throat radius b0. Choose b0 for 1 kg payload and for a human.
casimir_u_02um = 0.2709  # J/m^3 ideal plates at 0.2 um (M-ENGINEER-02 anchor)
for lab, b0 in [("1 kg, b0=0.1 m", 0.1), ("1 kg, b0=1 m", 1.0), ("human, b0=4.5 km (1 g over 2 m slow crossing)", 4.5e3)]:
    rho = c**4 / (8 * math.pi * G * b0**2)          # |rho| at throat, J/m^3
    Omega = 2 * b0 * c**2 / G                        # |exotic mass| kg (M-ENGINEER-02 measure)
    frac = m / Omega
    # shortcut ratio, mouths separated by d through exterior; throat transit ~ pi*b0 + 2*10 b0 (observers at 10 b0)
    T_thru = (math.pi * b0 + 2 * 10 * b0) / c
    for dlab, d in [("1 AU", 1.496e11), ("1 ly", ly)]:
        print(f"{lab:46s} d={dlab:5s}: T_thru/T_ext ~ {T_thru/(d/c):.2e}")
    print(f"{lab:46s} |rho_throat| = {rho:.3e} J/m^3 (10^{math.log10(rho/casimir_u_02um):.1f} x Casimir at 0.2 um); "
          f"|exotic mass| = {Omega:.3e} kg; 1 kg / |exotic mass| = {frac:.2e}")

print()
print("=== 3. Payload back-reaction check for labelled-phantom row ===")
# A 1 kg payload perturbs the throat by ~ G m/c^2 relative to b0
for b0 in [0.1, 1.0]:
    print(f"b0 = {b0} m: G m / (c^2 b0) = {G*m/(c**2*b0):.2e} (dimensionless perturbation)")
