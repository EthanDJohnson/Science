"""M-IDEALIZER-10: species count required by the payload condition (hbar = c = 1 in the algebra).

Inputs: |E_min| = G N^2 q^2/(256 r_e^3) (M-IDEALIZER-08); extremal magnetic RN with Dirac quantisation
g Q_m = 2 pi q in Heaviside-Lorentz units: r_e^2 = G Q_m^2/(4 pi) = pi G q^2/g^2, i.e. kappa = r_e^2/(G q^2) = pi/g^2
(the lens's normalisation, re-derived here from the extremality condition); weak coupling g^2 N < 1.
Payload condition m <= |E_min|.
Claim: N >~ 256 pi m r_e (SI: 256 pi m c r_e / hbar) ~ 3e55 for m = 1e3 kg, r_e = 1.5e7 m.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, inequality, quantity, units, finish

G, N, q, re, g, m, Qm = sp.symbols("G N q r_e g m Q_m", positive=True)
# extremality r_e^2 = G Q_m^2 / (4 pi) with Q_m = 2 pi q / g
re2 = (G * Qm**2 / (4 * sp.pi)).subs(Qm, 2 * sp.pi * q / g)
identity(re2 / (G * q**2), sp.pi / g**2)
q2 = sp.solve(sp.Eq(re**2, re2), q)[0]**2
Emin = G * N**2 * q2 / (256 * re**3)
identity(Emin, N**2 * g**2 / (256 * sp.pi * re))
# with g^2 < 1/N, |E_min| < N/(256 pi r_e): so m <= |E_min| requires N > 256 pi m r_e
bound = N / (256 * sp.pi * re)
inequality(Emin, "<", bound, domain={"g": (0.001, 0.0099), "N": (1, 1e4)})  # g^2 N < 1 on this box
units("1 kg * c * 1 m / hbar", "dimensionless")
val = 256 * math.pi * 1e3 * 299792458.0 * 1.5e7 / 1.054571817e-34
print("256 pi m c r_e / hbar =", f"{val:.3e}")
quantity(f"{256*math.pi} * 1e3 kg * c * 1.5e7 m / hbar", "3.4e55", rel_tol=0.02)
raise SystemExit(finish())
