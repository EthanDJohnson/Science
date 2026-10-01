"""M-EXAMINER-03: light along the axis of a subluminal Alcubierre bubble (N = 1).

Geometric units, lengths in metres; 1 m of light = 1/c s. Lab-frame null condition on the axis:
(dx - v f dt)^2 = dt^2  ->  dx/dt = v f(|x - v t|) +/- 1.
The displacement of the ray relative to flat-space light, after it has fully crossed the bubble,
is D = integral of v f dt along the ray (in +x for both directions). Forward ray gains D, backward
ray loses D. Claim: D ~ 2Rv each, co-minus-counter 4Rv = 2.400 m = 8.006 ns at R = 15 m, v = 0.04,
independent of sigma (2 and 0.5 1/m); 200.07 m = 667.4 ns at R = 100 m, v = 0.5.
Method here: direct RK4 integration of the lab-frame ray ODE (no comoving integral used).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import math
from math_checks import identity, limit, quantity, units, finish

def prof(r, R, s):
    return (math.tanh(s*(r + R)) - math.tanh(s*(r - R))) / (2*math.tanh(s*R))

def ray(direction, R, v, s, h=0.002):
    """Integrate x(t) from far outside until the ray is far beyond the bubble; return D = x - x_flat."""
    L = R + 40/s + 20
    # bubble centre at v t. Forward ray starts behind it at x = -L; backward ray starts ahead at x = +L
    x0 = -L if direction > 0 else L
    x, t = x0, 0.0
    rhs = lambda t_, x_: v*prof(abs(x_ - v*t_), R, s) + direction
    while True:
        rel = x - v*t
        if (direction > 0 and rel > L) or (direction < 0 and rel < -L):
            break
        k1 = rhs(t, x); k2 = rhs(t + h/2, x + h*k1/2); k3 = rhs(t + h/2, x + h*k2/2); k4 = rhs(t + h, x + h*k3)
        x += h*(k1 + 2*k2 + 2*k3 + k4)/6; t += h
    x_flat = x0 + direction*t
    return (x - x_flat)

c = 299792458.0
results = {}
for (R, v, s) in [(15.0, 0.04, 2.0), (15.0, 0.04, 0.5), (100.0, 0.5, 2.0), (100.0, 0.5, 0.5)]:
    Dp = ray(+1, R, v, s)
    Dm = ray(-1, R, v, s)
    diff = Dp + Dm     # forward ray ahead by Dp, backward ray behind by Dm
    results[(R, v, s)] = (Dp, Dm, diff)
    print(f"R={R} m v={v} sigma={s}/m: forward gain {Dp:.5f} m ({Dp/c*1e9:.4f} ns); backward loss {Dm:.5f} m "
          f"({Dm/c*1e9:.4f} ns); co-minus-counter {diff:.5f} m ({diff/c*1e9:.4f} ns); 4Rv = {4*R*v:.4f} m")

def check(name, got, want, tol):
    ok = abs(got - want) <= tol
    print(("PASS" if ok else "FAIL") + f" {name}: {got:.5f} vs {want} (tol {tol})")

Dp, Dm, d = results[(15.0, 0.04, 2.0)]
check("forward gain R=15, v=0.04, s=2", Dp, 1.2008, 2e-4)
check("backward loss R=15, v=0.04, s=2", Dm, 1.1992, 2e-4)
check("co-minus-counter R=15, v=0.04, s=2 [m]", d, 2.4000, 2e-4)
check("co-minus-counter R=15, v=0.04, s=2 [ns]", d/c*1e9, 8.006, 2e-3)
check("co-minus-counter R=15, v=0.04, s=0.5 [ns]", results[(15.0, 0.04, 0.5)][2]/c*1e9, 8.006, 2e-3)
check("co-minus-counter R=100, v=0.5, s=2 [m]", results[(100.0, 0.5, 2.0)][2], 200.07, 0.02)
check("co-minus-counter R=100, v=0.5, s=2 [ns]", results[(100.0, 0.5, 2.0)][2]/c*1e9, 667.4, 0.1)

# Top-hat (sharp wall) analytic: inside, forward dx/dt = 1 + v for a crossing time 2R in comoving terms
# Comoving X = x - v t: forward dX/dt = 1 inside (f=1); time inside = 2R; displacement = v*2R
identity("v*2*R", "2*R*v")
identity("2*R*v + 2*R*v", "4*R*v")
limit("4*R*v", "v", 0, "0")
quantity("2.4 m / c", "8.006 ns", rel_tol=1e-3)
quantity("200.07 m / c", "667.4 ns", rel_tol=1e-3)
units("2.4 m / c", "time")
raise SystemExit(finish())
