"""M-EMPIRICIST-06: (a) 410 Mpc in metres and its ratio to a 1e11 m decay length; e^-(L/l) survival;
(b) CMB Bose-Einstein occupation at 150 Hz, T = 2.7255 K: 1 + 2 f, f = 1/(exp(h nu/kT) - 1). SI.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, limit, finish

Mpc = 3.0856775814913673e22
L = 410 * Mpc
print(f"410 Mpc = {L:.4e} m; L/1e11 m = {L/1e11:.4e}")
quantity("410 Mpc", "1.3e25 m", rel_tol=0.03)
quantity(f"{L / 1e11}", "1.3e14", rel_tol=0.03)
# amplitude survival exp(-L/l) underflows: log10 survival
print(f"log10 survival (energy, e-folding 1e11 m) = {-(L/1e11)/math.log(10):.4e}")

h, kB, T, nu = 6.62607015e-34, 1.380649e-23, 2.7255, 150.0
xx = h * nu / (kB * T)
f = 1 / math.expm1(xx)
print(f"h nu/kT = {xx:.4e}; f = {f:.4e}; 1 + 2f = {1 + 2*f:.4e}")
quantity(f"{1 + 2 * f}", "7.6e8", rel_tol=0.01)
# Rayleigh-Jeans limit: f -> kT/(h nu) as x -> 0
limit("x*(1/(exp(x) - 1))", "x", 0, "1")
raise SystemExit(finish())
