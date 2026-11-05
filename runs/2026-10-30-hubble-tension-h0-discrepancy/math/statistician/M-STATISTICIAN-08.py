"""M-STATISTICIAN-08: Student-t two-sided tail at t = 6.27 (unit scale) for nu = 2, 3, 5 (F12).
p2 = 2 * integral_t^inf f_nu(x) dx; checked by quadrature and by closed forms for nu = 2, 3."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/statistician")
import mpmath as mp
from _common import p2_of_z, close
from math_checks import limit, finish


def tpdf(x, nu):
    nu = mp.mpf(nu)
    return mp.gamma((nu + 1) / 2) / (mp.sqrt(nu * mp.pi) * mp.gamma(nu / 2)) * (1 + x**2 / nu) ** (-(nu + 1) / 2)


def tp2(t, nu):
    return 2 * mp.quad(lambda x: tpdf(x, nu), [t, mp.inf])


t = mp.mpf("6.2709")
close("nu=2 quad vs closed 1 - t/sqrt(t^2+2)", tp2(t, 2) - (1 - t / mp.sqrt(t**2 + 2)), 0, 1e-12)
c3 = 1 - 2 * (t / (mp.sqrt(3) * (1 + t**2 / 3)) + mp.atan(t / mp.sqrt(3))) / mp.pi
close("nu=3 quad vs closed form", tp2(t, 3) - c3, 0, 1e-12)
close("nu=2 p2", tp2(t, 2), 0.025, 0.001)
close("nu=3 p2", tp2(t, 3), 0.008, 0.0005)
close("nu=5 p2", tp2(t, 5), 0.0015, 0.0001)
# limit: nu -> infinity recovers the Gaussian
close("nu=1e6 vs Gaussian at t=3 (rel)", abs(tp2(3, 10**6) / p2_of_z(3) - 1), 0, 1e-4)
limit("(1 + x**2/n)**(-(n+1)/2)", "n", "oo", "exp(-x**2/2)")
raise SystemExit(finish())
