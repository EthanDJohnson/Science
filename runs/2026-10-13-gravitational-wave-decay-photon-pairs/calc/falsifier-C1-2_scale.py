"""Falsifier C1, refuter 2 (scale angle): required vs achievable local pair-production rate.

Question: can the outgoing wave's own local field sustain B&O's eq. 8 rate R (an r-independent
pair rate) at radius r? We bound the achievable rate from above by the most favourable
kinematics any graviton distribution of the given energy density can have.

Units: SI throughout (J, m, s), unless marked natural (hbar = c = 1).

Inputs (B&O GW150914 anchor, D-27): E = 2 Msun c^2, f = 150 Hz, sigma = 200 rad/s.

Local rate (kinetic / geometric-optics form, natural units; verified in M-IDEALIZER-05/06,
M-CONSTRAINTS-01, M-DIALECTICIAN-09):
    Gamma(x) = (2 pi/5) G^2 T_mn T^mn,
    T_mn T^mn = rho^2 * sum_ij p_i p_j (1 - n_i.n_j)^2,  p_i = energy fractions.
Max over all direction distributions: <(1 - n.n')^2> = 1 - 2|<n>|^2 + Tr(M^2), M = <n n^T>,
Tr M = 1 so Tr M^2 <= 1, hence max = 2 (two antipodal beams). So
    Gamma <= (4 pi/5) G^2 rho^2 / c^7   (SI; isotropic gives 8 pi/15, eq. 14).
This is checked numerically below by random sampling of direction distributions.

The outgoing shell at radius r: energy E in solid angle Omega, thickness l >= c/sigma (bandwidth
limit; a chirp only thickens it). rho = E/(Omega r^2 l). Total achievable rate in the shell:
    Ndot_max(r) = Gamma_max * Omega r^2 l = (4 pi/5) G^2 E^2 /(Omega r^2 l c^7).
"""
import math, random

G = 6.67430e-11
c = 2.99792458e8
hbar = 1.054571817e-34
Msun = 1.98847e30
Mpc = 3.0856775814913673e22
yr = 3.15576e7

E = 2 * Msun * c**2
f = 150.0
w = 2 * math.pi * f
sig = 200.0
l = c / sig
D = 410 * Mpc
t_prop = D / c

print("== Inputs (SI) ==")
print(f"E = {E:.4e} J, w = {w:.4f} rad/s, sigma = {sig} rad/s, shell thickness l = c/sigma = {l:.4e} m")
print(f"lambda = {c/f:.4e} m, lambda/(2 pi) = {c/w:.4e} m, D = 410 Mpc = {D:.4e} m, t_prop = {t_prop:.4e} s")

# B&O eq. 8 in SI (M-DIALECTICIAN-01): R = 3 G^2 E^2 w sigma^2/(25 pi c^10), pairs/s
R = 3 * G**2 * E**2 * w * sig**2 / (25 * math.pi * c**10)
print("\n== B&O eq. 8 (SI) ==")
print(f"R = {R:.4e} pairs/s ; sustained over t_prop: R*t_prop = {R*t_prop:.4e} pairs")

# --- numeric check of max <(1-n.n')^2> = 2 over direction distributions
def unit():
    while True:
        v = [random.gauss(0, 1) for _ in range(3)]
        s = math.sqrt(sum(x * x for x in v))
        if s > 0:
            return [x / s for x in v]

random.seed(1)
best = 0.0
for trial in range(4000):
    k = random.randint(1, 6)
    ns = [unit() for _ in range(k)]
    ps = [random.random() for _ in range(k)]
    S = sum(ps); ps = [p / S for p in ps]
    val = sum(ps[i] * ps[j] * (1 - sum(a * b for a, b in zip(ns[i], ns[j])))**2
              for i in range(k) for j in range(k))
    best = max(best, val)
anti = 2 * 0.25 * 4  # two antipodal beams of equal energy: cross terms only
# isotropic: <(1-c)^2> over c uniform in [-1,1] = 4/3
iso = 0.5 * sum(((1 - (-1 + 2 * (i + 0.5) / 200000))**2) for i in range(200000)) * (2 / 200000)
print("\n== Kinematic factor <(1 - n.n')^2> (dimensionless) ==")
print(f"random search max = {best:.4f} (must be <= 2); antipodal pair = {anti:.4f}; isotropic = {iso:.4f} (exact 4/3)")

# --- achievable rate bound vs required R
def Ndot_max(r, Omega=4 * math.pi, ell=l):
    return (4 * math.pi / 5) * G**2 * E**2 / (Omega * r**2 * ell * c**7)

print("\n== Achievable (upper bound, head-on kinematics everywhere) vs required R ==")
print("closed form ratio Ndot_max/R = (5 pi/3) c^2/(r^2 w sigma) for Omega = 4 pi, l = c/sigma")
rs = [("lambda/2pi", c / w), ("lambda", c / f), ("1e4 km", 1e7), ("1 R_earth-ish 6.4e6 m", 6.4e6),
      ("c*tau (B&O sphere, tau = 1/(2R))", c / (2 * R)), ("1 AU", 1.495978707e11),
      ("1 pc", Mpc / 1e6), ("1 Mpc", Mpc), ("410 Mpc", D)]
for name, r in rs:
    nd = Ndot_max(r)
    print(f"r = {r:.4e} m ({name}): Ndot_max = {nd:.4e} pairs/s ; Ndot_max/R = {nd/R:.4e}")
r_star = c * math.sqrt(5 * math.pi / (3 * w * sig))
print(f"crossover r* (bound = R) = {r_star:.4e} m = {r_star/(c/f):.3f} wavelengths")
# beaming: if energy confined to Omega = 0.1 * 4 pi the bound rises x10, r* rises x sqrt(10)
print(f"with beaming Omega = 0.4 pi: r* = {r_star*math.sqrt(10):.4e} m")

# --- integrated pairs beyond r under the bound: N(>r) = int Ndot_max dr/c = (4pi/5)G^2E^2/(Omega l c^8 r)
def Nbeyond_max(r, Omega=4 * math.pi, ell=l):
    return (4 * math.pi / 5) * G**2 * E**2 / (Omega * ell * c**8 * r)

print("\n== Pairs made beyond r: bound vs C1's sustained count ==")
for name, r in [("lambda", c / f), ("1 AU", 1.495978707e11), ("410 Mpc", D)]:
    print(f"N_max(>{name}) = {Nbeyond_max(r):.4e} pairs ; C1 count over remaining path to 410 Mpc"
          f" R*(D - r)/c = {R*max(D - r, 0)/c:.4e}")
print(f"C1 sustained count R*t_prop / bound N_max(>lambda) = {R*t_prop/Nbeyond_max(c/f):.4e}")
print("N_max(>r) falls as 1/r even with maximal (head-on) kinematics: it converges, slope -1;"
      " C1 needs slope +1 (count beyond R growing as the path).")
# per-packet B&O total (M-DIALECTICIAN-01): P = R * 4 pi/(3 sigma)
P = R * 4 * math.pi / (3 * sig)
print(f"B&O per-packet total P = R*T_eff = {P:.4e} pairs; N_max(>lambda)/P = {Nbeyond_max(c/f)/P:.4e}")

# --- realistic kinematics: spread theta ~ c/(w r) (source size ~ lambda/2pi), unpolarised
# sigma(1-cos) -> (pi/5) G^2 w^2 theta^4 (natural; M-DIALECTICIAN-10 corrected form)
# Gamma = (1/2) n^2 c * (pi/5) hbar^2 w^2 G^2 theta^4 / c^8 (SI); n = E/(hbar w Omega r^2 l)
def Ndot_real(r):
    th = c / (w * r)
    n = E / (hbar * w * 4 * math.pi * r**2 * l)
    Gam = 0.5 * n**2 * c * (math.pi / 5) * hbar**2 * w**2 * G**2 * th**4 / c**8
    return Gam * 4 * math.pi * r**2 * l

print("\n== Realistic outgoing kinematics, theta = c/(w r) (SI) ==")
for name, r in [("lambda", c / f), ("1 AU", 1.495978707e11), ("410 Mpc", D)]:
    print(f"r = {name}: Ndot = {Ndot_real(r):.4e} pairs/s ; /R = {Ndot_real(r)/R:.4e}")

# --- plasma: in a plasma photons need s >= 4 w_p^2; two gravitons have s <= (w1+w2)^2 = 4 w^2
print("\n== Plasma kinematic closure (SI) ==")
for name, ne_cm3 in [("mean IGM 2.2e-7 cm^-3", 2.2e-7), ("warm ISM 0.03 cm^-3", 0.03), ("VLISM 0.08 cm^-3", 0.08)]:
    fp = 8980.0 * math.sqrt(ne_cm3)
    wp = 2 * math.pi * fp
    state = "OPEN (head-on only)" if w > wp else "CLOSED at every angle"
    # max radius at which the outgoing wave's own angular spread theta ~ c/(w r) still gives s >= 4 wp^2:
    # s ~ w^2 theta^2 = c^2/r^2 >= 4 wp^2 ... use the lens's r_max = c w/wp^2 for comparison
    print(f"{name}: f_p = {fp:.4e} Hz ; 150 Hz is {state}; r_max = c w/w_p^2 = {c*w/wp**2:.4e} m")
