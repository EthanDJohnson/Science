"""M-DECOMPOSER-04: weak-field Shapiro excess for a ray through the centre of a shell of mass M,
from x = -D to x = +D (exterior rest points), SI. Metric ds^2 = -(1+2Phi/c^2)c^2dt^2 + (1-2Phi/c^2)dx^2:
dt = (1 - 2Phi/c^2) dx / c. Thin shell radius R: Phi = -GM/r (r > R), -GM/R inside.
  dt_excess = (2GM/c^3) [ 2 ln(D/R) + 2 ].
Also the thick constant-density shell R1..R2 potential, as a cross-check of the R = 15 m choice."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, quantity, units, limit, finish
G, c = 6.67430e-11, 2.99792458e8
M = 4.49e27
x, R, D, GM = sp.symbols("x R D GM", positive=True)
expr = 2*GM*(2*sp.integrate(1/x, (x, R, D)) + sp.integrate(1/R, (x, -R, R)))
identity(sp.simplify(expr), 2*GM*(2*sp.log(D) - 2*sp.log(R) + 2), domain={"D": (20, 1e5), "R": (1, 19)})
units("6.674e-11 m^3/(kg s^2) * 4.49e27 kg / (3e8 m/s)^3", "time")
tau = 2*G*M/c**3
def thin(D, R=15.0): return tau*(2*math.log(D/R) + 2)
for Dv in (1e2, 1e3, 1e5):
    print(f"D = {Dv:.0e} m: thin-shell (R=15 m) weak-field excess = {thin(Dv)*1e9:.1f} ns")
quantity(f"{thin(1e3)*1e9} ns", "231 ns", rel_tol=0.01)
quantity(f"{thin(1e2)*1e9} ns", "100 ns", rel_tol=0.35)
quantity(f"{thin(1e5)*1e9} ns", "450 ns", rel_tol=0.05)
# thick shell potential, Newtonian: Phi(r) for constant density between R1, R2
R1, R2 = 10.0, 20.0
rho = 3*M/(4*math.pi*(R2**3 - R1**3))
def Phi(r):
    if r >= R2: return -G*M/r
    if r <= R1: return -2*math.pi*G*rho*(R2**2 - R1**2)
    menc = M*(r**3 - R1**3)/(R2**3 - R1**3)
    return -G*menc/r - 2*math.pi*G*rho*(R2**2 - r**2)
N = 200000; Dv = 1e3; dx = 2*Dv/N
s = sum(-2*Phi(abs(-Dv + (i + 0.5)*dx))/c**2 for i in range(N))*dx/c
print(f"thick-shell weak-field excess, D = 1e3 m: {s*1e9:.1f} ns; strong-field claim 240.0 ns -> diff {(240.0-s*1e9)/240*100:.1f} %")
print(f"compactness 2GM/(c^2 R2) = {2*G*M/(c**2*R2):.4f}")
quantity(f"2*G*{M} kg/(c^2*20 m)", "0.333", rel_tol=0.005)
limit("2*GM*(2*log(D/R)+2)", "GM", 0, 0, direction="+", domain={"D": (20, 1e5), "R": (1, 19)})
raise SystemExit(finish())
