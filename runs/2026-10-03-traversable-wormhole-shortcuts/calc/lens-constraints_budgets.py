"""Constraints lens: thermodynamic and back-reaction (energy-budget) constraints; polyhedral edge line mass.
SI unless marked; hbar = c = 1 relations converted with hbar c = 3.1615e-26 J m.
1  MM 2020 worked example (dossier Q-02/Q-07): environment temperature T < hbar c/(k_B l) vs CMB 2.725 K.
2  Standard-Model-scale MMP (Q-11): r_e = 2e-19 m, g = e (Heaviside-Lorentz 0.3028); q from r_e = sqrt(pi) q l_P / g;
   l = 16 r_e^3/(G q) and E_min = -G q^2/(256 r_e^3) (Q-10, G = l_P^2 with hbar = c = 1); extremal mouth mass r_e c^2/G.
3  Payload budgets: |binding energy| vs 1 kg and 70 kg rest energies (payload energy must stay below the
   negative binding energy, else the throat closes: [D-13], MM's 'collapse into a black hole').
4  Visser cube wormhole: each edge, after gluing, has total angle 2 x 3pi/2 = 3pi, a conical excess of pi.
   A straight static conical line source has mu = -excess c^2/(8 pi G) (cosmic-string relation, sign flipped).
"""
import math
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from gr_tensors import to_si, PLANCK_LENGTH as LP, C, G_NEWTON as G, HBAR, K_B

hbarc = HBAR * C
ly = 9.4607e15
print("=== 1. MM environment temperature ===")
ell = 3e3 * ly
T1 = hbarc / (K_B * ell)
T2 = to_si.hawking_temperature_k(1 / ell)     # hbar c kappa/(2 pi k_B) with kappa = 1/l
print(f"l = {ell:.3e} m: hbar c/(k_B l) = {T1:.3e} K ({hbarc/ell/1.602176634e-19:.2e} eV); with 1/(2 pi): {T2:.3e} K; CMB 2.725 K is {2.725/T1:.2e} times hotter")

print("\n=== 2. Standard-Model-scale MMP ===")
re = 2e-19
g = 0.30282212
q = re * g / (math.sqrt(math.pi) * LP)
l = 16 * re**3 / (LP**2 * q)
Emin_inv_m = -LP**2 * q**2 / (256 * re**3)
Emin_J = Emin_inv_m * hbarc
M_mouth = re * C**2 / G
print(f"q = {q:.3e}; throat length l = 16 r_e^3/(l_P^2 q) = {l:.3e} m; external transit pi l / c = {math.pi*l/C:.3e} s")
print(f"E_min = {Emin_inv_m:.3e} 1/m = {Emin_J:.3e} J = {Emin_J/1.602176634e-13:.3e} MeV")
print(f"extremal mouth mass r_e c^2/G = {M_mouth:.3e} kg each; required T < hbar c/(k_B l) = {hbarc/(K_B*l):.3e} K")
print(f"lowest-Landau-level check: q = {q:.2e} >> 1; ratio l/r_e = {l/re:.3e} (long throat)")

print("\n=== 3. Payload energy budgets ===")
for lab, Eb in (("SM-scale MMP", abs(Emin_J)), ("MM worked RS II (Q-02)", 4.5e26)):
    for m in (1.0, 70.0):
        print(f"{lab}: |E_bin| = {Eb:.3e} J; payload {m:g} kg rest energy {m*C**2:.3e} J; |E_bin|/(m c^2) = {Eb/(m*C**2):.3e}")
    print(f"   largest single quantum allowed ~ |E_bin| = {Eb/1.602176634e-19:.3e} eV")

print("\n=== 4. Visser cube wormhole: edge line mass ===")
excess = 2 * (3 * math.pi / 2) - 2 * math.pi
mu = -excess * C**2 / (8 * math.pi * G)
print(f"conical excess = {excess:.4f} rad; mu = {mu:.4e} kg/m per edge ({-excess/(8*math.pi):.4f} geometric, dimensionless)")
for side in (1.0, 1e3):
    print(f"cube side {side:g} m: 12 edges total line mass = {12*side*mu:.4e} kg (compare spherical thin shell of radius {side/2:g} m: {-2*(side/2)*C**2/G:.4e} kg)")
print("face-centred radial null ray: T_kk = 0 on flat faces (Visser 1989 eq. 2.4 with infinite radii) -> ANEC = 0 exactly; R_kk = 0 and Weyl = 0 along it -> null generic condition fails on that ray")
