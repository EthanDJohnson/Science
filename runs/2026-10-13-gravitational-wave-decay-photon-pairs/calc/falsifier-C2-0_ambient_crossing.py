#!/usr/bin/env python3
"""Falsifier C2-0 (physics angle). Does an outgoing GW really have 'no lifetime, no path depletion'?

Test: a real outgoing GW (GW150914, B&O inputs) never propagates through an otherwise empty spacetime; it
crosses the ambient stochastic GW background (SGWB) made of waves from other sources, arriving from all
directions. Collisions with these non-collinear gravitons are NOT collinear, so s > 0 and the tree-level
g g -> gamma gamma rate is non-zero and SUSTAINED along the whole path (production per unit length constant),
unlike the self-induced production that falls as R^-4 per unit length (C2's R^-3 for the integral).

Physics used (natural units hbar = c = 1, G = 1/M_Pl^2):
  unpolarised sigma(g g -> gamma gamma) = (2 pi/5) G^2 s   [M-DIALECTICIAN-10 corrected form; M-MECHANIST-03 sigma_lin;
                                                              checked below against qft_second_order 'beams' output]
  test graviton (energy w) in an isotropic bath of energy density rho_b, any bath spectrum:
     Gamma_1 = n_b <sigma (1 - cos th)> = (2pi/5) G^2 * 2 w w_b <(1-cos)^2> n_b,  <(1-cos)^2>_iso = 4/3
             = (16 pi/15) G^2 w rho_b      (independent of the bath frequency)
  consistency: (1/2) Int n Gamma_1 = (8 pi/15) G^2 rho^2 = B&O eq. 14 / M-IDEALIZER-05 (checked symbolically below)
  SI: Gamma_1 = (16 pi/15) G^2 (hbar w) rho_E / c^7   [s^-1]  (units checked below)
"""
import math
import sympy as sp

# ---------- constants (SI, CODATA) ----------
G = 6.67430e-11; c = 2.99792458e8; hbar = 1.054571817e-34
Msun = 1.98892e30; Mpc = 3.0856775814913673e22; AU = 1.495978707e11; pc = 3.0856775814913673e16
eV = 1.602176634e-19; MPl_eV = 1.22089e28; hbarc_eVm = 1.973269804e-7

print("=== 0. Symbolic consistency of the per-graviton bath rate ===")
Gs, w, wb, rho, cth = sp.symbols('G w w_b rho c', positive=True)
avg = sp.integrate((1 - cth)**2, (cth, -1, 1)) / 2
print("<(1-cos)^2>_isotropic =", avg)
Gamma1 = sp.Rational(2, 5)*sp.pi*Gs**2 * 2*w*wb*avg * (rho/wb)
Gamma1 = sp.simplify(Gamma1)
print("Gamma_1 =", Gamma1, " (bath frequency cancels:", not Gamma1.has(wb), ")")
Gvol = sp.simplify(sp.Rational(1, 2) * (rho/w) * Gamma1)  # half for identical bath particles, monochromatic bath
print("(1/2) n Gamma_1 =", Gvol, "; equals (8 pi/15) G^2 rho^2 ?", sp.simplify(Gvol - sp.Rational(8, 15)*sp.pi*Gs**2*rho**2) == 0)

print("\n=== 1. Cross-section check against qft_second_order beams (150 rad/s, h=1e-21, head-on) ===")
s_eV2 = 3.899e-26          # printed by the tool
sigma_tool = 8.587e-152    # m^2, printed by the tool (linear 'plus' pair, azimuth-averaged)
sigma_formula = (2*math.pi/5) * s_eV2 / MPl_eV**4 * hbarc_eVm**2
print(f"(2pi/5) G^2 s = {sigma_formula:.4e} m^2 vs tool {sigma_tool:.4e} m^2; ratio {sigma_formula/sigma_tool:.4f}")

print("\n=== 2. SI units check of Gamma_1 = (16pi/15) G^2 (hbar w) rho_E / c^7 ===")
# dimensions as exponent vectors (kg, m, s)
dimG = (-1, 3, -2); dimE = (1, 2, -2); dimRho = (1, -1, -2); dimc = (0, 1, -1)
tot = tuple(2*a + b + r - 7*d for a, b, r, d in zip(dimG, dimE, dimRho, dimc))
print("dimension (kg, m, s) exponents:", tot, "-> expect (0, 0, -1) i.e. 1/s")

def gamma1_SI(omega, rhoE):
    return (16*math.pi/15) * G**2 * hbar*omega * rhoE / c**7

# ---------- GW150914 inputs (B&O) ----------
f = 150.0; omega = 2*math.pi*f; E = 2*Msun*c**2; sig = 200.0
N = E/(hbar*omega)
lam = c/f; lbar = c/omega
D = 410*Mpc
P_near = 2.927e-6   # B&O-model total pairs (rate x T_eff), M-IDEALIZER-09
print(f"\nGW150914: N = {N:.3e} gravitons, lambda = {lam:.3e} m, lambda/2pi = {lbar:.3e} m, D = {D:.3e} m")

# ---------- ambient background energy densities ----------
H0 = 67.4e3/Mpc
rho_c_E = 3*H0**2/(8*math.pi*G) * c**2   # J/m^3
print(f"rho_crit c^2 = {rho_c_E:.3e} J/m^3")
# NANOGrav 15-yr: h_c = 2.4e-15 at 1/yr [D-35]; Omega_gw(f) = 2 pi^2 f^2 h_c^2 / (3 H0^2) (per ln f)
fyr = 1/3.15576e7
Om_pta = 2*math.pi**2*fyr**2*(2.4e-15)**2/(3*H0**2)
cases = [
    ("PTA (NANOGrav 15-yr, Omega per ln f at 1/yr) [D-35]", Om_pta*rho_c_E),
    ("LVK CBC estimate Omega(25 Hz) = 0.9e-9 [D-34]", 0.9e-9*rho_c_E),
    ("LVK upper limit Omega(25 Hz) = 2.8e-9 [D-34]", 2.8e-9*rho_c_E),
    ("primordial N_eff ceiling rho = 2.8e-15 J/m^3 [D-33]", 2.8e-15),
]
print(f"Omega_PTA(1/yr) = {Om_pta:.3e}")

print("\n=== 3. Sustained cross-collision depletion of the GW150914 wave ===")
for name, rhoE in cases:
    g1 = gamma1_SI(omega, rhoE)
    tau = 1/g1
    P_path = N * g1 * D/c               # pairs made along 410 Mpc (Euclidean, z ignored)
    frac = g1*D/c                       # fraction of gravitons depleted
    # self-induced production per unit length beyond R (C2's law): P_self(>R) = P_near*A*(lbar/R)^3,
    # A = 0.0632 (idealizer exact asymptote, M-IDEALIZER-09) -> dP/dR = 3 P_near A lbar^3 / R^4
    A = 0.0632
    dPdR_cross = N*g1/c
    Rx = (3*P_near*A*lbar**3/dPdR_cross)**0.25
    P_self_beyond_D = P_near*A*(lbar/D)**3
    print(f"- {name}: rho = {rhoE:.2e} J/m^3")
    print(f"    Gamma_1 = {g1:.2e} 1/s, lifetime tau = {tau:.2e} s = {tau/3.156e7:.2e} yr")
    print(f"    depleted fraction over 410 Mpc = {frac:.2e}; pairs made along path = {P_path:.2e}")
    print(f"    self-induced pairs beyond 410 Mpc (C2 law) = {P_self_beyond_D:.2e}; cross/self = {P_path/P_self_beyond_D:.1e}")
    print(f"    crossover radius where cross production per length = self production per length: "
          f"R_x = {Rx:.2e} m = {Rx/pc:.2e} pc = {Rx/lam:.2e} lambda")
    print(f"    pairs from cross channel / B&O near-source total = {P_path/P_near:.2e}")

print("\n=== 4. Tail (curvature backscatter) estimate, order of magnitude only ===")
# Born backscatter by the curvature part of the Regge-Wheeler potential, V ~ 6 GM/(c^2 r^3):
# incoming amplitude fraction eps(r) ~ V/(4 k^2) = 6 r_g/(4 k^2 r^3). Head-on in x out rate ~ G^2 (4w^2) n^2 eps^2 * 2,
# self (diffraction) rate ~ G^2 n^2 /r^2 (theta^2 ~ 1/(kr)); ratio ~ 8 (eps k r)^2 (O(1) factors not tracked).
Mtot = 65*Msun; rg = G*Mtot/c**2; k = omega/c
for r in [lam, 10*lam, AU]:
    eps = 6*rg/(4*k**2*r**3)
    print(f"  r = {r:.2e} m: eps_in ~ {eps:.2e}, tail/diffraction rate ratio ~ {8*(eps*k*r)**2:.2e}")
print("  -> falls as r^-4 relative to the self term: tails do not break convergence (heuristic).")
