"""M-CONSTRAINTS-03 (F3, K13): exact QUMOND sphere-averaged radial boost via Gauss's law.

QUMOND: div g = div F, F = nu(|g_N|/a0) g_N, g_N = g_Ne z^ - (GM/r^2) r^ (total Newtonian field).
g - F is divergence-free and regular on the sphere's interior minus the point mass? (F's divergence
there is the same as g's, so flux(g) = flux(F) through any sphere.) The uniform external g_e has zero
sphere-averaged radial component, so <g_int . r^> = <F . r^>. Boost = -<F.r^>/(GM/r^2).
Independent cross-check: at small GM/r^2 the Gauss result must equal the explicit linearised
potential solution nu_e(1+K/3) (M-CONSTRAINTS-01), and at large GM/r^2 it must go to 1.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-11-wide-binary-anomaly-gaia-dr4/math/constraints")
import mpmath as mp
from math_checks import identity, finish
from cklib import ef_state, qumond_ef, sphere_boost, q, A0

mp.mp.dps = 20
gx = mp.mpf("1.785")
# Uniform field has zero sphere-averaged radial component: (1/2) int_{-1}^{1} c dc = 0
identity("integrate(c, (c, -1, 1))/2", "0", domain={"c": (-1, 1)})

table = {  # log10 g_N : (simple, n1.5, standard, MLS)
    -11.0: (1.4228, 1.1670, 1.0726, 1.3691), -10.5: (1.4222, 1.1670, 1.0728, 1.3686),
    -10.0: (1.4159, 1.1668, 1.0746, 1.3625), -9.75: (1.3821, 1.1633, 1.0779, 1.3321),
    -9.5: (1.2762, 1.1117, 1.0522, 1.2268), -9.0: (1.1076, 1.0262, 1.0070, 1.0585),
    -8.5: (1.0366, 1.0049, 1.0007, 1.0059), -8.0: (1.0119, 1.0009, 1.0001, 1.0001)}
names = ["simple", "n1.5", "standard", "MLS"]
gNe = {n: ef_state(n, gx)[0] for n in names}
q(gNe["simple"] * A0 / mp.mpf("1e-10"), 1.373, 1e-3, "g_Ne (simple) / 1e-10 m s^-2")

def boost(n, lg):
    return sphere_boost(n, mp.mpf(10) ** lg / A0, gNe[n])

for lg, vals in table.items():
    for n, v in zip(names, vals):
        q(boost(n, lg), v, 3e-4, f"{n} log g_N = {lg}")
# limits
for n in ["simple", "standard"]:
    q(boost(n, -14), qumond_ef(n, gx), 1e-4, f"{n}: Gauss result at g_N = 1e-14 equals linearised nu_e(1+K/3)")
    q(boost(n, -4), 1.0, 1e-4, f"{n}: Newton limit at g_N = 1e-4 m s^-2")
# scoring-bin average, log-uniform over [-10.5, -9.5]
for n, w in [("simple", 1.393), ("standard", 1.073), ("MLS", 1.341)]:
    avg = mp.quad(lambda t: boost(n, t), [-10.5, -10, -9.5])
    q(avg, w, 1e-3, f"{n} scoring-bin log-uniform mean")
# conversion-factor difference: 0.416 vs 0.375
q((boost("simple", -10) - 1) / (mp.mpf("1.3748") - 1) - 1, 0.11, 0.05, "relative difference in (gamma_MOND - 1), exact vs bz18_simple preset 1.3748 (preset value taken from lens)")
raise SystemExit(finish())
