"""M-DIALECTICIAN-01 (F1): a pure velocity boost v -> sqrt(gamma) v at fixed orbits rescales every quantile
of v~ by sqrt(gamma), so gamma(p) = (Q_p,obs / Q_p,Newt)^2 = gamma for all p and S = gamma(0.8)/gamma(0.3) = 1.
Also: a boost that varies across pairs (gamma(g_N) within a bin) is a mixture of rescalings and need not be flat;
additive Gaussian velocity noise breaks exact flatness at order (sigma/v)^2."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-11-wide-binary-anomaly-gaia-dr4/math/dialectician")
import numpy as np
import sympy as sp
from math_checks import identity, limit, quantity, finish
from kep import sample_e, kepler_vtilde, gamma_profile

# Symbolic: for any CDF F_X, Y = c X (c > 0) has F_Y(y) = F_X(y/c) so Q_Y(p) = c Q_X(p).
# Use a concrete invertible CDF F(x) = 1 - exp(-x^2/2) (Rayleigh) as the example family.
g, p = sp.symbols("g p", positive=True)
QX = sp.sqrt(-2 * sp.log(1 - p))
QY = sp.sqrt(g) * QX
identity((QY / QX) ** 2, g)                                  # gamma(p) = gamma, independent of p
# check that QY really is the quantile of sqrt(g) X: F_Y(QY) = 1 - exp(-(QY/sqrt(g))^2/2) = p
identity(1 - sp.exp(-(QY / sp.sqrt(g)) ** 2 / 2), p, domain={"p": (0.01, 0.99), "g": (0.5, 3)})
limit(((QY.subs(p, sp.Rational(8, 10)) / QX.subs(p, sp.Rational(8, 10))) ** 2) /
      ((QY.subs(p, sp.Rational(3, 10)) / QX.subs(p, sp.Rational(3, 10))) ** 2), "g", 1, 1)  # S = 1 (trivially at gamma -> 1)

# Monte Carlo with identical orbits (same seed), e ~ e^1.3 (HTZ-like in the low bin)
n = 200000
rng = np.random.default_rng(11)
e = sample_e(n, "power", rng, alpha=1.3)
st = rng.bit_generator.state
vt1 = kepler_vtilde(n, e, rng, 1.0)
rng.bit_generator.state = st
vt14 = kepler_vtilde(n, e, rng, 1.4)
gp = gamma_profile(vt14, vt1, ps=(0.1, 0.3, 0.5, 0.8, 0.9))
print("same orbits, gamma=1.4: gamma(p) at p=.1,.3,.5,.8,.9 =", np.round(gp, 6), " S =", gp[3] / gp[1])
quantity(f"{gp[3] / gp[1]}", "1", rel_tol=1e-9)
quantity(f"{gp[2]}", "1.4", rel_tol=1e-9)

# Independent orbits (different seed): flat to sampling noise
rng2 = np.random.default_rng(12)
vt14b = kepler_vtilde(n, sample_e(n, "power", rng2, alpha=1.3), rng2, 1.4)
gpb = gamma_profile(vt14b, vt1, ps=(0.3, 0.5, 0.8))
print("independent orbits gamma=1.4: gamma(.3,.5,.8) =", np.round(gpb, 4), " S =", round(gpb[2] / gpb[0], 4))
quantity(f"{gpb[2] / gpb[0]}", "1", rel_tol=0.02)

# Mixture of rescalings: half the pairs at gamma=1.15, half at 1.40 (a bin spanning gamma(g_N))
rng3 = np.random.default_rng(13)
h = n // 2
vA = kepler_vtilde(h, sample_e(h, "power", rng3, alpha=1.3), rng3, 1.15)
vB = kepler_vtilde(h, sample_e(h, "power", rng3, alpha=1.3), rng3, 1.40)
gpm = gamma_profile(np.concatenate([vA, vB]), vt1, ps=(0.3, 0.5, 0.8))
print("mixture 1.15/1.40: gamma(.3,.5,.8) =", np.round(gpm, 4), " S =", round(gpm[2] / gpm[0], 4))
quantity(f"{gpm[2] / gpm[0]}", "1", rel_tol=0.02)   # mixture of modest rescalings stays near-flat

# Units: v~ = v_p / sqrt(G M / s) is dimensionless
from math_checks import units
units("(300 m/s)^2 / (6.674e-11 m^3/(kg s^2) * 2e30 kg / (1.5e15 m))", "dimensionless")
raise SystemExit(finish())
