"""M-EXAMINER-10 (F9): DR4 hidden-companion window, order-of-magnitude model as the lens states it.
Symbols: inner pair mass M_in = 1.2 Msun, wide total M_w = 1.5 Msun, photocentre factor k = 0.27, circular inner orbit.
 (a) v_c(s) = sqrt(G M_w / s) (SI); velocity-relevant if photocentre speed k sqrt(G M_in/a_in) >= v_c(s)
     -> a_in <= k^2 (M_in/M_w) s.
 (b) P >= baseline T: a_in >= (M_in T^2)^(1/3) au (T in yr, M in Msun).
 (c) acceleration error from a least-squares quadratic fit, N epochs uniform on [-T/2, T/2]:
     sigma_g = sqrt(60) sigma_mu / T (the lens's relation) -- derived here from the normal equations.
 (d) photocentre acceleration k G M_in / a_in^2, angular = that / d; detected if >= 5 sigma_g; resolved if a_in/d >= 0.5".
 Hidden fraction = log-length of the undetected, unresolved part of [a_min, a_max] / log(a_max/a_min).
 Inputs: DR4 sigma_mu = 0.54 sigma_plx(D-51 table, uas) ; DR3 sigma_mu from the EDR3 z-model 0.96 sqrt(40+800z+30z^2) uas,
 and x1.8 of that (closer to Lindegren DR3 medians); the lens does not print its DR3 input.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import math
import sympy as sp
from math_checks import identity, limit, quantity, units, inequality, finish

# (c) normal equations for x = c0 + c1 t + c2 t^2, t uniform on [-T/2, T/2] (continuous limit, N points)
t, T, sig, Nn = sp.symbols("t T sigma N", positive=True)
mom = lambda k: sp.integrate(t**k, (t, -T / 2, T / 2)) / T
F = sp.Matrix([[mom(i + j) for j in range(3)] for i in range(3)]) * Nn / sig**2
C = F.inv()
sig_mu = sp.sqrt(C[1, 1])
sig_g = 2 * sp.sqrt(C[2, 2])          # acceleration = 2 c2
identity(sp.simplify(sig_g / sig_mu), sp.sqrt(60) / T)
identity(sp.simplify(sig_mu), sp.sqrt(12 / Nn) * sig / T)

# (a), (b)
quantity("(6.6743e-11 m^3/(kg s^2) * 1.5 Msun / (10000 au))^0.5", "0.365 km/s", rel_tol=3e-3)
units("(6.6743e-11 m^3/(kg s^2) * 1.5 Msun / (10000 au))^0.5", "m/s")
k, Min, Mw = 0.27, 1.2, 1.5
for s, want in ((3000, 175), (10000, 583), (20000, 1166)):
    amax = k**2 * Min / Mw * s
    print(f"s = {s} au: a_max = {amax:.1f} au (lens {want})")
    identity(sp.Float(round(amax)), sp.Float(want))
a_min = {rel: (Min * (Tm / 12) ** 2) ** (1 / 3) for rel, Tm in (("DR3", 34), ("DR4", 66))}
print("a_min (P = baseline):", {r: round(v, 2) for r, v in a_min.items()}, "au")
ain = sp.symbols("a_in", positive=True)
limit(k * sp.sqrt(Min / ain), "a_in", "oo", "0")    # wide inner orbits: photocentre speed -> 0

# (d) hidden fraction
G_mag = [13, 14, 15, 16, 17]
dr4_plx = dict(zip(G_mag, [10, 14, 22, 35, 59]))   # uas, D-51
def edr3_mu(G):
    z = 10 ** (0.4 * (max(G, 13) - 15))
    return 0.96 * math.sqrt(40 + 800 * z + 30 * z * z)  # uas/yr
def hidden(sig_mu_uas, Tyr, d_pc, s=10000.0):
    amin = (Min * Tyr**2) ** (1 / 3)
    amax = k**2 * Min / Mw * s
    sg = math.sqrt(60) * sig_mu_uas * 1e-3 / Tyr          # mas/yr^2
    acc_coef = k * 4 * math.pi**2 * Min * 1000.0 / d_pc   # mas/yr^2 at a_in = 1 au (1 au at d pc = 1000/d mas)
    a_acc = math.sqrt(acc_coef / (5 * sg))
    a_res = 0.5 * d_pc
    lo, hi = max(amin, a_acc), min(amax, a_res)
    return max(0.0, math.log(hi / lo)) / math.log(amax / amin), a_acc
rows = {}
for d in (100, 200):
    for G in G_mag:
        h3a, _ = hidden(edr3_mu(G), 34 / 12, d)
        h3b, _ = hidden(1.8 * edr3_mu(G), 34 / 12, d)
        h4, a4 = hidden(0.54 * dr4_plx[G], 66 / 12, d)
        rows[(d, G)] = (h3a, h3b, h4)
        print(f"d = {d} pc, G = {G}: hidden DR3 {h3a:.2f} (model) / {h3b:.2f} (x1.8), DR4 {h4:.2f} (a_acc,DR4 = {a4:.0f} au)")
h4_200_13 = rows[(200, 13)][2]
inequality(sp.Float(abs(h4_200_13 - 0.17)), "<", sp.Float(0.02))
dr3_all = [v[0] for v in rows.values()] + [v[1] for v in rows.values()]
dr4_all = [v[2] for v in rows.values()]
print(f"DR3 hidden range {min(dr3_all):.2f}-{max(dr3_all):.2f} (lens 0.17-0.48); DR4 {min(dr4_all):.2f}-{max(dr4_all):.2f} (lens 0.00-0.34)")
# what DR3 sigma_mu reproduces the lens's 0.35 at d = 200 pc, G = 13
lo, hi = 1.0, 100.0
for _ in range(80):
    mid = math.sqrt(lo * hi)
    if hidden(mid, 34 / 12, 200)[0] < 0.35: lo = mid
    else: hi = mid
print(f"DR3 sigma_mu giving 0.35 at 200 pc: {mid:.1f} uas/yr (EDR3 model at G=13: {edr3_mu(13):.1f})")
raise SystemExit(finish())
