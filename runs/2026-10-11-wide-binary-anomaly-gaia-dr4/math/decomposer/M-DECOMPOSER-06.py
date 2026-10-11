"""M-DECOMPOSER-06: MOND target numbers quoted in Q4 and candidate G.

Independent re-implementation (mpmath, from the formulas, not the generator's code) of the
parametrised boost used in the run (Chae 2024 eq. 22 form, with QUMOND nu_n):
  nu_n(y) = [(1 + sqrt(1 + 4 y^-n))/2]^(1/n),   y = g_N / a0 (dimensionless)
  K(y)    = d ln nu_n / d ln y   (computed here by numerical differentiation, not the closed form)
  y_e     : Newtonian external field solving y_e nu_n(y_e) = x_e = g_ext/a0 (solved by root finding)
  y_b     = sqrt(y^2 + (beta y_e)^2);  gamma = nu(y_b) [1 + tanh(beta y_e / y)^p K(y_b)/3]
Presets: bz18_simple n=1, beta=1, p=1.2, g_ext = (232.8 km/s)^2/8.2 kpc; bz18_standard n=2 same g_ext;
chae2024 n=1, beta=1.1, p=1.2, g_ext = 1.9 a0; a0 = 1.2e-10 m/s^2 (SI).
Claims: gamma(1e-10 m/s^2) = 1.375 / 1.061 / 1.333; EF limit eta = nu_e(1 + K_e/3) = 1.4228 (BZ18
Table 3, simple); anisotropy range nu_e(1 + K_e/2) = 1.354 .. nu_e = 1.560 -> "+-7%" about 1.423 and
"~15%" orientation dependence.  Limits: y >> 1 -> 1; g_ext = 0, y -> 0 -> y^-1/2 (deep MOND).
"""
import sys
import mpmath as mp
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, inequality, finish

mp.mp.dps = 30
a0 = mp.mpf("1.2e-10")
kpc = mp.mpf("3.0856775814913673e19")
gext_bz = (mp.mpf("232.8e3")) ** 2 / (mp.mpf("8.2") * kpc)
print("g_ext BZ18 [m/s^2]", gext_bz, "x_e =", gext_bz / a0)

def nu(y, n):
    return ((1 + mp.sqrt(1 + 4 * y ** (-n))) / 2) ** (1 / mp.mpf(n))

def K(y, n):
    return mp.diff(lambda t: mp.log(nu(mp.e ** t, n)), mp.log(y))

def y_ext(xe, n):
    return mp.findroot(lambda yy: yy * nu(yy, n) - xe, xe)

def gamma(gN, n, beta, p, gext):
    y = gN / a0
    if gext == 0:
        return nu(y, n)
    ye = y_ext(gext / a0, n)
    yb = mp.sqrt(y ** 2 + (beta * ye) ** 2)
    return nu(yb, n) * (1 + mp.tanh(beta * ye / y) ** p * K(yb, n) / 3)

P = {"bz18_simple": (1, 1, 1.2, gext_bz), "bz18_standard": (2, 1, 1.2, gext_bz),
     "chae2024": (1, mp.mpf("1.1"), 1.2, mp.mpf("1.9") * a0)}
for name, claim in (("bz18_simple", "1.375"), ("bz18_standard", "1.061"), ("chae2024", "1.333")):
    g = gamma(mp.mpf("1e-10"), *P[name])
    print(name, "gamma(1e-10) =", g)
    quantity(f"{g}", claim, rel_tol=1.5e-3)

# EF-dominated limit (BZ18 eqs. 15-16), simple function
n = 1
ye = y_ext(gext_bz / a0, n)
nue, Ke = nu(ye, n), K(ye, n)
eta, lo, hi = nue * (1 + Ke / 3), nue * (1 + Ke / 2), nue
print("nu_e", nue, "K_e", Ke, "eta", eta, "range", lo, hi)
quantity(f"{eta}", "1.4228", rel_tol=5e-4)
quantity(f"{lo}", "1.354", rel_tol=1e-3)
quantity(f"{hi}", "1.560", rel_tol=1e-3)
# deep internal limit of the chae2024 / bz18_simple forms approaches eta (beta = 1 only)
g_deep = gamma(mp.mpf("1e-14"), *P["bz18_simple"])
print("bz18_simple gamma(1e-14)", g_deep)
quantity(f"{g_deep}", f"{eta}", rel_tol=1e-3)
# anisotropy: half-range relative to the angle average, and full max/min ratio
half = (hi - lo) / 2 / eta
ratio = hi / lo
print("half-range/eta", half, "max/min", ratio)
quantity(f"{half}", "0.07", rel_tol=0.06)
quantity(f"{ratio}", "1.15", rel_tol=0.01)
# limits: Newtonian y >> 1 -> 1 ; isolated deep MOND nu -> y^-1/2
quantity(f"{gamma(mp.mpf('1e-6'), *P['bz18_simple'])}", "1.0", rel_tol=1e-3)
yy = mp.mpf("1e-8")
quantity(f"{nu(yy, 1) * mp.sqrt(yy)}", "1.0", rel_tol=1e-3)
inequality(f"{gamma(mp.mpf('1e-10'), *P['bz18_standard'])}", "<", f"{gamma(mp.mpf('1e-10'), *P['bz18_simple'])}")
raise SystemExit(finish())
