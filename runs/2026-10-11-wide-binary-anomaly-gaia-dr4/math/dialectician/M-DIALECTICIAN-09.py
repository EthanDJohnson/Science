"""M-DIALECTICIAN-09 (F9, F4): MOND boost in the Chae 2024 eq.-22 form, written from its definition:
y = gN/a0, nu(y) = (1 + sqrt(1 + 4/y))/2 (n = 1 QUMOND), y_e from y_e nu(y_e) = x_e (solved numerically here),
y_b = sqrt(y^2 + (beta y_e)^2), K = dln nu/dln y (numerical derivative here),
gamma = nu(y_b) [1 + tanh(beta y_e / y)^p K(y_b) / 3]; chae2024 preset beta = 1.1, p = 1.2, x_e = 1.90, a0 = 1.2e-10 m/s^2.
Lens: gN = G M/(1.2 s)^2 at s = 2646 au gives gamma = 1.185 (M = 0.8 Msun) and 1.090 (2.0 Msun), difference 0.095.
Bin truth ~1.26 in log10 gN in [-11, -9.5]."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import mpmath as mp
from math_checks import quantity, finish

G = 6.674e-11; MSUN = 1.98892e30; AU = 1.495978707e11; a0 = 1.2e-10
nu = lambda y: (1 + mp.sqrt(1 + 4 / y)) / 2
K = lambda y: mp.diff(lambda t: mp.log(nu(mp.e ** t)), mp.log(y))
ye = mp.findroot(lambda t: t * nu(t) - 1.90, 1.0)
print("y_e =", ye, " check closed form x^2/(1+x) =", 1.90 ** 2 / 2.90)
quantity(f"{ye}", f"{1.90 ** 2 / 2.90}", rel_tol=1e-9)


def gam(gN, beta=1.1, p=1.2):
    y = gN / a0
    yb = mp.sqrt(y ** 2 + (beta * ye) ** 2)
    return nu(yb) * (1 + mp.tanh(beta * ye / y) ** p * K(yb) / 3)


# limits: Newtonian (y >> 1) -> 1; K deep -> -1/2
quantity(f"{gam(1e-6)}", "1", rel_tol=1e-3)
quantity(f"{K(mp.mpf('1e-10'))}", "-0.5", rel_tol=1e-4)
vals = {}
for M in (0.8, 1.3, 2.0):
    gN = G * M * MSUN / (1.2 * 2646 * AU) ** 2
    vals[M] = float(gam(gN))
    print(f"s=2646 au, M={M}: gN = {gN:.3e} m/s^2, log10 {float(mp.log10(gN)):.3f}, gamma = {vals[M]:.4f}")
quantity(f"{vals[0.8]}", "1.185", rel_tol=0.002)
quantity(f"{vals[2.0]}", "1.090", rel_tol=0.002)
quantity(f"{vals[0.8] - vals[2.0]}", "0.095", rel_tol=0.03)
for lg in (-11.0, -10.5, -10.0, -9.75, -9.5):
    print(f"log10 gN = {lg}: gamma = {float(gam(10 ** lg)):.4f}")
lo, hi = float(gam(10 ** -9.5)), float(gam(10 ** -11.0))
print(f"bin range [{lo:.4f}, {hi:.4f}] contains 1.26: {lo <= 1.26 <= hi}")
quantity(f"{min(max(1.26, lo), hi)}", "1.26", rel_tol=1e-12)
raise SystemExit(finish())
