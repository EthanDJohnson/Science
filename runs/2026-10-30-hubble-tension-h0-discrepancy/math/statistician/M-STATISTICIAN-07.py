"""M-STATISTICIAN-07: Bayes-factor bounds (F11, table A).
(a) Gaussian prior on offset delta ~ N(0, tau^2): observed D ~ N(delta, s^2).
    BF(two/one) = N(D; 0, s^2 + tau^2) / N(D; 0, s^2), derived here by direct integration.
(b) Sellke-Bayarri-Berger bound: BF_null >= -e p ln p for p < 1/e; max odds = 1/that."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/statistician")
import mpmath as mp
from _common import p2_of_z, quad, close
from math_checks import limit, identity, units, finish


def bf_int(D, s, tau):
    D, s, tau = mp.mpf(D), mp.mpf(s), mp.mpf(tau)
    like = lambda d: mp.npdf(D, d, s)
    m1 = mp.quad(lambda d: like(d) * mp.npdf(d, 0, tau), [-mp.inf, -20, 0, D, 20, mp.inf])
    return m1 / like(0)


def bf_closed(D, s, tau):
    return mp.npdf(D, 0, mp.sqrt(s**2 + tau**2)) / mp.npdf(D, 0, s)


def sellke(p):
    return -mp.e * p * mp.log(p)


s1 = quad(0.93, 0.38)
print("SH0ES vs CMB-SPA, D = 6.30, s =", float(s1))
for tau, cl in [(3, 1.5e7), (6, 3.3e7), (10, 2.8e7)]:
    a, b = bf_int(6.30, s1, tau), bf_closed(6.30, s1, tau)
    close(f"  integral vs closed form tau={tau} (rel)", abs(a / b - 1), 0, 1e-8)
    close(f"  BF tau={tau} (x1e7)", a / 1e7, cl / 1e7, 0.1 * cl / 1e7)
s2 = quad(0.93, 0.58)
for tau in (3, 6, 10):
    close(f"SH0ES vs BAO+BBN BF tau={tau} (x1e3), lens 3-4e3", bf_closed(4.99, s2, tau) / 1e3, 3.5, 0.6)

print("Sellke bounds")
p = p2_of_z(6.2709)
print(f"  p2(z=6.271) = {float(p):.3e}; bound = {float(sellke(p)):.3e}; max odds = {float(1/sellke(p)):.3e}")
close("  bound at the lens's rounded p2 = 3e-10 (x1e8)", sellke(mp.mpf('3e-10')) * 1e8, 1.8, 0.05)
close("  bound at the actual p2 for z = 6.27 (x1e8), lens 1.8", sellke(p) * 1e8, 1.8, 0.05)
close("  max odds at z = 3.9", 1 / sellke(p2_of_z(3.9)), 413, 3)
close("  max odds at z = 3.94 (H0DN no-Ceph actual z)", 1 / sellke(p2_of_z(3.9384)), 413, 3)
close("  prior for P = 0.5 at z = 3.9 (x1e3)", sellke(p2_of_z(3.9)) * 1e3, 2.4, 0.05)
close("  one-step: max odds at z = 1.88, lens 2.6", 1 / sellke(p2_of_z(1.8824)), 2.6, 0.1)
close("  one-step: max odds at heavy-tail z = 2.0", 1 / sellke(p2_of_z(2.0)), 2.6, 0.1)
for z in (1.4435, 1.65, 1.85, 2.36):
    close(f"  SH0ES-CCHP max odds at z = {z}, lens <= 1.4", 1 / sellke(p2_of_z(z)), 1.4, 0.05)
close("  CCHP vs SPA BF tau=3", bf_closed(3.20, quad(1.936, .38), 3), 1.05, 0.35)
close("  TD vs SPA BF tau=3", bf_closed(3.91, quad(2.3, .38), 3), 1.05, 0.35)
close("  CCHP vs SPA BF tau=10", bf_closed(3.20, quad(1.936, .38), 10), 1.05, 0.35)
close("  TD vs SPA BF tau=10", bf_closed(3.91, quad(2.3, .38), 10), 1.05, 0.35)

limit("sqrt(s**2/(s**2+t**2))*exp(D**2/2*(1/s**2 - 1/(s**2+t**2)))", "t", 0, "1")  # tau -> 0: models coincide
identity("exp(-D**2/(2*(s**2+t**2)))/sqrt(2*pi*(s**2+t**2)) / (exp(-D**2/(2*s**2))/sqrt(2*pi*s**2))",
         "sqrt(s**2/(s**2+t**2))*exp(D**2/2*(1/s**2 - 1/(s**2+t**2)))")
units("(6.30 km/s/Mpc)**2 / (1.0 km/s/Mpc)**2", "dimensionless")
raise SystemExit(finish())
