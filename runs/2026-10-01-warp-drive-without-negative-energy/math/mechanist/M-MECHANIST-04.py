"""M-MECHANIST-04: two-thin-layer harmonic-gauge model and the cap beta <= C1 - C2.

Linear gravity, harmonic gauge, geometric units. A thin shell of mass m, radius R, moving at u:
h_bar_tx solves lap h_bar_tx = 16 pi sigma u delta(r-R) (lap h_bar = -16 pi T_mn, T_tx = -sigma u),
so inside h_tx = -4 m u / R (uniform). Two layers, M/2 each, at R1 and R2, moving at +u and -u:
|beta_int| = 2 M u (1/R1 - 1/R2) = u (C1 - C2), C_k = 2M/R_k.  Claim: u = beta/(C1 - C2) = 0.060, 0.119;
cap (|p_k| <= E_k, E1 + E2 <= M, p1 = p2) gives beta <= C1 - C2 = 0.335.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, inequality, quantity, limit, finish

r, R, m, u = sp.symbols("r R m u", positive=True)
# potential of a shell: phi = m/R inside, m/r outside; check Laplace both sides and jump = -4 pi sigma R^2/R^2
phi_in, phi_out = m / R, m / r
lap = lambda f: sp.diff(r**2 * sp.diff(f, r), r) / r**2
identity(lap(phi_in), "0"); identity(lap(phi_out), "0")
sigma = m / (4 * sp.pi * R**2)
jump = (sp.diff(phi_out, r) - sp.diff(phi_in, r)).subs(r, R)
identity(jump, -4 * sp.pi * sigma)   # lap phi = -4 pi sigma delta  -> phi = int sigma/|x-x'|
# h_bar_tx = -4 * (potential with source sigma*u) -> inside -4 m u/R
h_in = -4 * u * phi_in
M, R1, R2 = sp.symbols("M R1 R2", positive=True)
beta2 = sp.Abs((-4 * (M / 2) * u / R1) - (-4 * (M / 2) * (-u) / R2))  # inner +u, outer -u: fields add with opposite signs
beta_two = 4 * (M / 2) * u * (1 / R1 - 1 / R2)
identity(beta_two, u * (2 * M / R1 - 2 * M / R2))
# cap: p <= min(E1, E2) <= M/2  -> beta <= 4 p (1/R1 - 1/R2) <= C1 - C2
E1, p = sp.symbols("E1 p", positive=True)
inequality("4*p*(1/R1 - 1/R2)", "<=", "2*M/R1 - 2*M/R2",
           domain={"M": (1, 2), "p": (0, 0.5), "R1": (3, 5), "R2": (6, 10)})
# numbers: GM_ADM/c^2 from toolkit-rebuilt shell (4.511e27 kg)
G, c = 6.67430e-11, 2.99792458e8
mg = G * 4.5114e27 / c**2
C1, C2 = 2 * mg / 10, 2 * mg / 20
print(f"m = {mg:.4f} m, C1 = {C1:.4f}, C2 = {C2:.4f}, C1-C2 = {C1-C2:.4f}")
quantity(f"{C1-C2} m/m", "0.335 m/m", rel_tol=0.005)
quantity(f"{0.02/(C1-C2)} m/m", "0.060 m/m", rel_tol=0.01)
quantity(f"{0.04/(C1-C2)} m/m", "0.119 m/m", rel_tol=0.01)
limit(beta_two, "R2", R1, "0")  # thin-wall limit: counter-currents cancel
raise SystemExit(finish())
