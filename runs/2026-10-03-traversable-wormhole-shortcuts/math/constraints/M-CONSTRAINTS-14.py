"""M-CONSTRAINTS-14 (F16). Static spherical two-ended wormhole ds^2 = -e^{2Phi(l)} dt^2 + dl^2 + r(l)^2 dOmega^2.
Statement: for two points of the radial null geodesic, t2 - t1 = int_{l1}^{l2} e^{-Phi} dl. Any causal curve from the
first to the second has t2 - t1 >= int e^{-Phi} sqrt(l'^2 + r^2 |Omega'|^2) d sigma >= int e^{-Phi(l)} |dl| >= the
radial value, so no timelike curve links them: the radial null geodesic is achronal (lens states it for Phi = 0).
Check: the pointwise inequality, plus random trial paths for Ellis with Phi = 0 and Phi = -b0/r."""
import sys, random, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import inequality, finish

inequality("exp(-P)*sqrt(a**2 + r**2*w**2)", ">=", "exp(-P)*Abs(a)",
           domain={"P": (-3, 3), "a": (-5, 5), "r": (0.1, 10), "w": (-5, 5)})


def optical(path, phi):
    tot = 0.0
    for (l1, th1), (l2, th2) in zip(path, path[1:]):
        lm = 0.5 * (l1 + l2); r = math.sqrt(lm * lm + 1.0)
        tot += math.exp(-phi(lm)) * math.sqrt((l2 - l1)**2 + (r * (th2 - th1))**2)
    return tot


rng = random.Random(3)
worst = {}
for name, phi in [("Phi=0", lambda l: 0.0), ("Phi=-1/r", lambda l: -1.0 / math.sqrt(l * l + 1.0))]:
    N = 4000
    radial = optical([(-5 + 10 * i / N, 0.0) for i in range(N + 1)], phi)
    best = float("inf")
    for trial in range(300):
        amp = rng.uniform(0, 1.0); bump = rng.uniform(-0.5, 0.5); kk = rng.randint(1, 4)
        pts = []
        for i in range(N + 1):
            u = i / N
            l = -5 + 10 * u + bump * math.sin(math.pi * u * kk)          # may wander in l (non-monotone allowed)
            th = amp * math.sin(math.pi * u * kk)                          # returns to theta = 0
            pts.append((l, th))
        best = min(best, optical(pts, phi))
    print(f"{name}: radial optical length {radial:.6f}, shortest of 300 trial paths {best:.6f}")
    inequality(sp.Float(best - radial, 15), ">=", 0)
raise SystemExit(finish())
