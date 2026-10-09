"""Falsifier C4-0 (physics): does the ghost-scalar (Ellis) instability kill C4's shortcuts?

Units: SI. Instability e-folding time from Gonzalez, Guzman & Sarbach 2009
(arXiv:0806.0608, Table I): tau_unstable = T * r_throat / c with T = 0.846 for the
massless (gamma1 = 0) Ellis wormhole, T -> 0.590 for large gamma1.
A perturbation of fractional amplitude delta grows to O(1) after ln(1/delta) e-folds.
Seeds considered (order of magnitude, fractional metric perturbation at the throat):
  quantum floor  delta_q = l_P / b0
  payload        delta_m = G m / (c^2 b0)
  single photon  delta_g = G E / (c^4 b0)
Crossing lengths: signal through |l| < 3 b0 (6 b0); observers at r = 10 m (2 sqrt(r^2 - b0^2));
payload through the flare region pi b0 (C4's own convention).
"""
import math

c = 2.99792458e8      # m/s
G = 6.67430e-11       # m^3 kg^-1 s^-2
hbar = 1.054571817e-34
lP = math.sqrt(hbar * G / c**3)
g0 = 9.80665
eV = 1.602176634e-19
T_GGS = 0.846         # dimensionless tau/r_throat, gamma1 = 0
T_GGS_inf = 0.590

def tau_u(b0, T=T_GGS):
    return T * b0 / c

print("Planck length l_P = %.4e m" % lP)
print("\n--- 1. Signal (light) crossing vs instability, Ellis b0 = 1 m ---")
b0 = 1.0
tu = tau_u(b0)
t_sig_core = 6 * b0 / c
t_sig_obs = 2 * math.sqrt(10.0**2 - b0**2) / c
print("tau_unstable = %.3e s" % tu)
print("signal |l|<3b0: %.3e s = %.2f e-folds" % (t_sig_core, t_sig_core / tu))
print("signal r=10 m to r=10 m: %.3e s = %.2f e-folds" % (t_sig_obs, t_sig_obs / tu))
for name, delta in [("quantum l_P/b0", lP / b0),
                    ("1 eV photon", G * 1 * eV / c**4 / b0),
                    ("1 kg payload", G * 1.0 / c**2 / b0),
                    ("70 kg payload", G * 70.0 / c**2 / b0)]:
    nf = math.log(1 / delta)
    print("  seed %-15s delta = %.3e -> %.1f e-folds to O(1) -> lifetime %.3e s = %.1f b0/c"
          % (name, delta, nf, nf * tu, nf * T_GGS))

print("\n--- 2. C4 sub-hypothesis (a): slow crossing at v = 10 km/s ---")
v = 1.0e4
for b0 in (504.9, 4516.0):
    tu = tau_u(b0)
    tcross = math.pi * b0 / v
    nq = math.log(b0 / lP)
    nm = math.log(1 / (G * 70.0 / c**2 / b0))
    print("b0 = %.1f m: tau_u = %.3e s; crossing pi b0/v = %.3e s = %.3e e-folds;"
          " quantum-seeded lifetime %.3e s (%.0f e-folds); 70 kg-seeded %.3e s (%.0f e-folds);"
          " crossing/lifetime = %.2e"
          % (b0, tu, tcross, tcross / tu, nq * tu, nq, nm * tu, nm, tcross / (nq * tu)))

print("\n--- 3. Minimum crossing speed for a ghost-scalar Ellis throat ---")
# Need pi b0 / v < T ln(1/delta) b0 / c  ->  v/c > pi / (T ln(1/delta)); independent of b0 except via log.
for b0 in (1.0, 1.0e3, 1.5e11, 9.46e15):
    for T in (T_GGS, T_GGS_inf):
        nq = math.log(b0 / lP)
        print("b0 = %.2e m, T = %.3f: ln(b0/l_P) = %.1f -> v_min = %.4f c" % (b0, T, nq, math.pi / (T * nq)))

print("\n--- 4. Human (1 g over 2 m) at v_min: tidal bound b0 >= gamma v sqrt(xi/a) ---")
xi, a = 2.0, g0
b = 1.0e6
for it in range(50):
    seed = max(lP / b, G * 70.0 / c**2 / b)
    beta = math.pi / (T_GGS * math.log(1 / seed))
    gam = 1 / math.sqrt(1 - beta**2)
    bnew = gam * beta * c * math.sqrt(xi / a)
    if abs(bnew - b) / b < 1e-12:
        break
    b = bnew
print("self-consistent: v_min = %.4f c, b0_min = %.3e m, |M| ~ b0 c^2/G = %.3e kg = %.3e M_sun"
      % (beta, b, b * c**2 / G, b * c**2 / G / 1.989e30))
print("crossing time pi b0/v = %.3e s vs lifetime %.3e s"
      % (math.pi * b / (beta * c), T_GGS * math.log(1 / seed) * b / c))

print("\n--- 5. Shortcut ratio is unaffected: T_thru set by b0, T_ext by d ---")
b0 = 1.0
tthru = 2 * math.sqrt(10.0**2 - b0**2) / c
for d in (1.0e3, 1.496e11, 9.4607e15):
    print("d = %.3e m: T_thru/T_ext = %.3e (T_ext = (d - 20 m)/c)" % (d, tthru / ((d - 20.0) / c)))
