"""Crux C4: consolidate the felt-acceleration fraction F = 1 - kappa of a payload
inside an externally pushed compact shell, across the models the three verdicts used,
and set the precision a nonlinear evolution would need to decide C4 against rivals.

Units: geometric (G = c = 1) for C = 2M/R and alpha; SI for masses, lengths, accelerations.
Models (all from the verdicts C4-0, C4-1, C4-2):
  - LBK neutral g00 law:   F = 1 - C            (C4-1 transfer of Lynden-Bell-Bicak-Katz 1999)
  - LBK extremal geometry: F = (1 - C/2)^2      (C4-1)
  - lapse law at the rebuild centre: F = N^2, N = 0.761 (rebuild interior lapse, candidates C1/C4)
  - Brill-Cohen rotational proxy: kappa = 4a(2-a)/((1+a)(3-a)), C = 4a/(1+a)^2 (isotropic a = M/2r)
  - linear coefficients: kappa = 2C (4M/R, harmonic non-retarded), 11C/6 (LBK retarded)
Tow alternative (C4-0, C4-2): payload in free fall a distance d = sqrt(GM/A) behind a pushed
mass feels only the tide 2 A L / d, so equal comfort F_tow = 2 L sqrt(A/(G M)).
"""
import math

G = 6.674e-11
g0 = 9.80665


def kappa_bc(C):
    # invert C = 4a/(1+a)^2 on 0 < a <= 1 by bisection
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if 4 * mid / (1 + mid) ** 2 < C:
            lo = mid
        else:
            hi = mid
    a = 0.5 * (lo + hi)
    return 4 * a * (2 - a) / ((1 + a) * (3 - a))


print("Weak-field check: C=1e-4 kappa_BC=%.6e vs Thirring 2C/3=%.6e" % (kappa_bc(1e-4), 2e-4 / 3))
print("Horizon check: C=1 kappa_BC=%.4f" % kappa_bc(1.0))

N = 0.761
print("\nF = 1 - kappa (felt fraction) by model")
print("%-8s %-10s %-10s %-10s %-10s %-10s %-10s" % ("C", "1-C", "(1-C/2)^2", "1-BC", "1-2C", "1-11C/6", "N^2"))
for C in (1 / 3, 0.335, 2 / 3, 8 / 9, 0.96, 48 / 49):
    print("%-8.4f %-10.3f %-10.3f %-10.3f %-10.3f %-10.3f %-10s" % (
        C, 1 - C, (1 - C / 2) ** 2, 1 - kappa_bc(C), 1 - 2 * C, 1 - 11 * C / 6,
        "%.3f" % (N ** 2) if abs(C - 1 / 3) < 1e-3 else "-"))

# Band at the published shell (C = 0.333-0.335), nonlinear models only
vals = [1 - 1 / 3, (1 - 1 / 6) ** 2, 1 - kappa_bc(0.335), N ** 2]
lo, hi = min(vals), max(vals)
print("\nPublished shell nonlinear band: F = %.3f to %.3f; gain 1/F = %.2f to %.2f" % (lo, hi, 1 / hi, 1 / lo))
print("Gap from no-drag (F=1) to band top: %.3f; band width: %.3f" % (1 - hi, hi - lo))
print("Precision needed to separate F_band from F=1 at 3 sigma: sigma_F <= %.3f" % ((1 - hi) / 3))
print("Precision needed to separate the nonlinear models from each other at 2 sigma: sigma_F <= %.3f" % ((hi - lo) / 4))

# DEC-limit floor across models
for C in (0.96, 48 / 49):
    f = [1 - C, (1 - C / 2) ** 2, 1 - kappa_bc(C)]
    print("C=%.4f: F range %.3f to %.3f (best gain %.0fx)" % (C, min(f), max(f), 1 / min(f)))

# Tow alternative at equal comfort to the published shell
M_shell = 4.511e27  # kg, rebuild M_ADM
L = 10.0  # m payload length
for A_g in (1.0, 10.0):
    A = A_g * g0
    for F in (lo, hi):
        M_tow = A * (2 * L / F) ** 2 / G
        d = math.sqrt(G * M_tow / A)
        rho_min = 3 * M_tow / (4 * math.pi * d ** 3)
        print("A=%4.0f g, L=%.0f m, equal felt F=%.3f: tow mass %.3e kg at d=%.1f m (L/d=%.2f, linear tide rough); "
              "shell/tow = %.2e; tug must fit inside d -> density >= %.2e kg/m^3" % (
                  A_g, L, F, M_tow, d, L / d, M_shell / M_tow, rho_min))

# Size constraint on the tow: the tug's radius r must be < d = sqrt(GM/A), i.e. its surface gravity >= A.
print("\nTow size constraint (tug radius <= d): surface gravity >= A")
A = 10 * g0
M0, d0 = 5.877e18, 2.0e3  # C4-0's tractor at A = 10 g
print("C4-0 tractor M=%.3e kg at d=%.0f m needs density >= %.2e kg/m^3" % (M0, d0, 3 * M0 / (4 * math.pi * d0 ** 3)))
rho_os = 2.26e4  # kg/m^3 osmium, as used by C4-2
M_min = (3 / (4 * math.pi * rho_os)) ** 2 * A ** 3 / G ** 3
r = (3 * M_min / (4 * math.pi * rho_os)) ** (1 / 3)
d = math.sqrt(G * M_min / A)
print("Osmium-density tug at A=10 g: min mass %.3e kg (r=%.3e m, d=%.3e m); shell/tug = %.1f; "
      "tide over 10 m = %.2e m/s^2 = %.2e of A" % (M_min, r, d, M_shell / M_min, 2 * A * L / d, 2 * L / d))
rho_shell = 1.53e23
print("Shell mean density %.2e kg/m^3 [D-22] vs C4-0 tractor floor: ratio %.1e" % (
    rho_shell, rho_shell / (3 * M0 / (4 * math.pi * d0 ** 3))))
