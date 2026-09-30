"""M-EMPIRICIST-07: heavy-tail probabilities (F9, candidate E). Two-sided tail of a unit-scale Student-t,
P(|T_nu| > z) = I_{nu/(nu+z^2)}(nu/2, 1/2) (regularized incomplete beta), cross-checked by direct quadrature of
the density; Gaussian P = erfc(z/sqrt 2). z = 4.65 (dimensionless)."""
import sys
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/empiricist")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from _inputs import *
from math_checks import identity, limit, finish

mp.mp.dps = 30
z = mp.mpf("4.65")

def dens(t, nu):
    return mp.gamma((nu + 1) / 2) / (mp.sqrt(nu * mp.pi) * mp.gamma(nu / 2)) * (1 + t * t / nu) ** (-(nu + 1) / 2)

def tail_quad(nu):
    return 2 * mp.quad(lambda t: dens(t, nu), [z, mp.inf])

def tail_beta(nu):
    return mp.betainc(mp.mpf(nu) / 2, mp.mpf(1) / 2, 0, nu / (nu + z * z), regularized=True)

# nu = 2 closed form: P(|T|>z) = 1 - z/sqrt(2+z^2)
identity("2*Integral((1 + t**2/2)**(-3/2)/(2*sqrt(2)), (t, z, oo))", "1 - z/sqrt(2 + z**2)")
# nu -> oo: the t kernel tends to the Gaussian kernel
limit("(1 + t**2/nu)**(-(nu + 1)/2)", "nu", "oo", "exp(-t**2/2)")

g = mp.erfc(z / mp.sqrt(2)); print(f"Gaussian two-sided P(>4.65) = {mp.nstr(g, 5)}")
agree("Gaussian", float(g), 3.3e-6, 0.06e-6)
for nu, lens in [(2, 0.043), (3, 0.019), (4, 0.0096)]:
    a, b = tail_quad(nu), tail_beta(nu)
    print(f"nu={nu}: quadrature {mp.nstr(a, 6)}, beta {mp.nstr(b, 6)}, Gaussian-equivalent z {zeq(a):.3f}")
    agree(f"nu={nu} quad = beta", float(a), float(b), 1e-15)
    agree(f"nu={nu} tail", float(a), lens, 0.006 * lens + 5e-5)
print(f"large-nu check nu=1e4: {mp.nstr(tail_beta(10000), 5)} vs Gaussian {mp.nstr(g, 5)}")
agree("Gaussian-equivalent range low (nu=2)", zeq(tail_quad(2)), 2.0, 0.06)
agree("Gaussian-equivalent range high (nu=4)", zeq(tail_quad(4)), 2.6, 0.06)
raise SystemExit(finish())
