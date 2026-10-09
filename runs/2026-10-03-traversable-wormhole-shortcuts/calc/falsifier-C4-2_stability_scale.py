"""Falsifier C4-2 (scale angle): does the phantom-scalar Ellis shortcut stay open long enough
to be crossed, and what throat does a payload crossing force?

Inputs (quoted, not re-derived):
- Gonzalez, Guzman & Sarbach 2009 (arXiv:0806.0608, Table I): e-folding time of the single
  unstable mode, T = tau_unstable / r_throat = 0.846 for gamma1 = 0 (massless Ellis), 0.590 as
  gamma1 -> infinity (geometric, G = c = 1; i.e. tau = T * b0 / c in SI).
- Transverse tide at the Ellis throat for a radial traveller: gamma^2 v^2 xi / b0^2 (M-IDEALIZER-06,
  verified), so b0 >= gamma v sqrt(xi / a_max).
- Crossing proper length taken as pi*b0 (as in M-IDEALIZER-06).
- Throat mass scale |M| = b0 c^2 / G (M-IDEALIZER-04, mass-function measure).

Model of the seed: a positive-energy perturbation of fractional size delta = (perturbing mass) /
(b0 c^2/G) grows as exp(t/tau); the throat is taken as lost when delta*exp(N) reaches eps = 0.1.
This is an order-of-magnitude linear-growth estimate, not a nonlinear evolution.
SI units throughout unless marked.
"""
import math

c = 2.99792458e8      # m/s
G = 6.67430e-11       # m^3 kg^-1 s^-2
g0 = 9.80665          # m/s^2
Msun = 1.98892e30     # kg
yr = 3.15576e7        # s
ly = 9.4607e15        # m
T_GGS = 0.846         # tau/b0 (geometric), massless Ellis, GGS 2009 Table I
eps = 0.1

def tau(b0):
    return T_GGS * b0 / c

print("== 1. Slow crossings proposed in C4 sub-hypothesis (a), v = 10 km/s ==")
v = 1.0e4
for b0, label in [(1.0, "1 m"), (504.9, "505 m (20 g over 0.5 m)"), (4516.0, "4.5 km (1 g over 2 m)")]:
    t_cross = math.pi * b0 / v
    N = t_cross / tau(b0)
    print(f"b0 = {label}: tau_unstable = {tau(b0):.3e} s, crossing time = {t_cross:.3e} s, "
          f"e-folds during crossing N = {N:.3e}, log10 growth = {N/math.log(10):.3e}")
print("N is independent of b0: N = pi c /(0.846 v) =", f"{math.pi*c/(T_GGS*v):.4e}")

print("\n== 2. Seed from the payload itself and the minimum crossing speed ==")
def solve(m_pay, xi, a_max):
    # iterate: b0 from tide at speed v, delta from payload, N_max = ln(eps/delta), v = pi c/(T N_max)
    v = 0.05 * c
    for _ in range(200):
        gam = 1.0 / math.sqrt(1 - (v / c) ** 2)
        b0 = gam * v * math.sqrt(xi / a_max)
        delta = G * m_pay / (c ** 2 * b0)
        Nmax = math.log(eps / delta)
        v_new = math.pi * c / (T_GGS * Nmax)
        if abs(v_new - v) < 1e-12 * c:
            break
        v = v_new
    return v, b0, delta, Nmax

for m_pay, xi, a_max, label in [(1.0, 0.5, 20 * g0, "1 kg, 0.5 m, 20 g"),
                                 (70.0, 2.0, 1 * g0, "70 kg human, 2 m, 1 g"),
                                 (70.0, 0.5, 20 * g0, "70 kg, 0.5 m, 20 g")]:
    v, b0, delta, Nmax = solve(m_pay, xi, a_max)
    M = b0 * c ** 2 / G
    print(f"{label}: delta = {delta:.3e}, N_max = {Nmax:.1f}, v_min = {v:.3e} m/s = {v/c:.4f} c, "
          f"b0_min (tide) = {b0:.3e} m, |M| ~ {M:.3e} kg = {M/Msun:.3e} Msun, "
          f"crossing time = {math.pi*b0/v:.3e} s, tau = {tau(b0):.3e} s")

print("\n== 3. Unattended lifetime of a static throat bathed in the CMB ==")
u_cmb = 4.17e-14   # J/m^3, CMB energy density at 2.725 K
for b0 in [1.0, 4516.0, 6.9e6]:
    # mass-energy falling into the throat during one e-folding time
    dm = u_cmb * c * 4 * math.pi * b0 ** 2 * tau(b0) / c ** 2
    delta = dm / (b0 * c ** 2 / G)
    life = tau(b0) * math.log(eps / delta)
    print(f"b0 = {b0:.3e} m: CMB infall per e-fold = {dm:.3e} kg, delta = {delta:.3e}, "
          f"lifetime ~ {life:.3e} s ({math.log(eps/delta):.1f} e-folds)")

print("\n== 4. Control bandwidth needed for active stabilisation ==")
for b0 in [1.0, 4516.0, 6.9e6]:
    print(f"b0 = {b0:.3e} m: growth rate 1/tau = {1/tau(b0):.3e} s^-1; light-crossing of throat "
          f"circumference 2 pi b0 / c = {2*math.pi*b0/c:.3e} s = {2*math.pi/T_GGS:.2f} tau")

print("\n== 5. Clock drift that erodes a designed T_thru/T_ext (one-sided, mouths 1 ly apart) ==")
d = ly
T_ext = d / c
for dv, label in [(3.0e4, "relative speed 30 km/s"), (2.2e5, "relative speed 220 km/s")]:
    rate = 0.5 * (dv / c) ** 2
    t_tm = (T_ext) / rate   # offset reaching ~ d/c (T_thru << d/c) closes a CTC
    print(f"{label}: offset rate {rate:.3e} s/s; offset reaches T_ext = {T_ext:.3e} s after "
          f"{t_tm:.3e} s = {t_tm/yr:.3e} yr")
