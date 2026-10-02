"""M-DECOMPOSER-03: in the flat cavity of the shell, metric (x^0 = ct)
   ds^2 = -A (dx^0)^2 + 2 g0x dx^0 dx + dx^2,  A = e^{2a} (constant), g0x = -b (covariant shift,
   warp_shell convention g_0x = -S beta_warp).  Null: u = dx/dx^0 = -g0x +- sqrt(g0x^2 + A) = b +- sqrt(b^2+A).
Claim: the +x ray beats flat-space light locally (u > 1) iff b > (1 - A)/2; with A = 0.579, 0.21.
Also: independent TOV integration (unsmoothed constant-density shell, SI) for A = e^{2a(R1)}."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
import numpy as np
from math_checks import sign, limit, identity, quantity, finish
A, b = sp.symbols("A b", positive=True)
up = b + sp.sqrt(b**2 + A)
# sign(u+ - 1) == sign(b - (1-A)/2) on 0<A<1, 0<b<1
sign((up - 1)*(b - (1 - A)/2), "nonnegative", domain={"A": (0.01, 0.999), "b": (0.001, 0.999)})
# exact threshold: u+ = 1 at b = (1-A)/2
identity(up.subs(b, (1 - A)/2), 1, domain={"A": (0.01, 0.999)})
limit((1 - A)/2, "A", 1, 0)        # flat lapse: any shift gives local advance
# weak-field: the naive contravariant answer 1 - sqrt(A) agrees to first order in (1-A)
x = sp.symbols("x", positive=True)
limit(((1 - (1 - x))/2) / (1 - sp.sqrt(1 - x)), "x", 0, 1)
print("threshold at A=0.579:", (1 - 0.579)/2, " (naive 1-sqrt(A) =", 1 - math.sqrt(0.579), ")")
quantity("(1 - 0.579)/2", "0.21", rel_tol=0.01)

# --- independent TOV for the unsmoothed constant-density shell, M = 4.49e27 kg, R1=10 m, R2=20 m
G, c = 6.67430e-11, 2.99792458e8
M, R1, R2 = 4.49e27, 10.0, 20.0
rho0 = 3*M/(4*math.pi*(R2**3 - R1**3))
def m(r): return M*(r**3 - R1**3)/(R2**3 - R1**3)
def rhs(r, y):
    P, a = y
    mm = m(r) + 4*math.pi*r**3*P/c**2
    den = r**2*(1 - 2*G*m(r)/(c**2*r))
    return np.array([-G*(rho0 + P/c**2)*mm/den, G*mm/(c**2*den)])
n = 20000; h = -(R2 - R1)/n
y = np.array([0.0, 0.5*math.log(1 - 2*G*M/(c**2*R2))]); r = R2
for i in range(n):
    k1 = rhs(r, y); k2 = rhs(r + h/2, y + h*k1/2); k3 = rhs(r + h/2, y + h*k2/2); k4 = rhs(r + h, y + h*k3)
    y = y + h*(k1 + 2*k2 + 2*k3 + k4)/6; r += h
e2a = math.exp(2*y[1])
print(f"compactness 2GM/(c^2 R2) = {2*G*M/(c**2*R2):.4f}; e^(2a) at R2 = {1-2*G*M/(c**2*R2):.4f}")
print(f"cavity e^(2a) (unsmoothed TOV, ours) = {e2a:.4f}; P(R1) = {y[0]:.3e} Pa")
quantity(f"{e2a}", "0.579", rel_tol=0.02)
raise SystemExit(finish())
