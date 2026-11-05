"""M-CONSTRAINTS-12 (F13): local void. Linear theory: dH/H = -f delta/3, f = Omega_m^0.55 (growth rate, LCDM).
Bernardeau (1992) spherical: dH/H = (f/2) [1 - (1+delta)^(2/3)] (-> -f delta/3 for small delta).
sigma(R): top-hat variance of the EH98 no-wiggle P(k) ~ k^n_s T^2, sigma8 = 0.8137, n_s = 0.9679, h = 0.6719, Omega_m = 0.3175, omega_b = 0.02237.
Lens: dH/H = 9.04%; delta = -0.51 (lin), -0.46 (Bernardeau); sigma_delta = 0.155, 0.065, 0.037, 0.012, 0.006 at R = 50,100,150,300,450 h^-1 Mpc;
sigma(dH/H)(150) = 0.65% (0.44 km/s/Mpc); Copernican r < 370/6.07 = 61 Mpc, P = (61/640)^3 = 8.6e-4."""
import sys, math
import numpy as np
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/constraints")
from math_checks import series, units, finish
from _bg import bisect, near

h, Om, wb, ns, s8 = 0.6719, 0.3175, 0.02237, 0.9679, 0.8137
wm = Om * h * h; fb = wb / wm; Th = 2.7255 / 2.7
s = 44.5 * math.log(9.83 / wm) / math.sqrt(1 + 10 * wb ** 0.75)
aG = 1 - 0.328 * math.log(431 * wm) * fb + 0.38 * math.log(22.3 * wm) * fb ** 2
def T(k):  # k in h/Mpc
    G = Om * h * (aG + (1 - aG) / (1 + (0.43 * k * h * s) ** 4))
    q = k * Th ** 2 / G
    L0 = np.log(2 * math.e + 1.8 * q); C0 = 14.2 + 731 / (1 + 62.5 * q)
    return L0 / (L0 + C0 * q * q)
lnk = np.linspace(np.log(1e-5), np.log(50), 6001); k = np.exp(lnk)
P = k ** ns * T(k) ** 2
def sig2(R):
    x = k * R; W = 3 * (np.sin(x) - x * np.cos(x)) / x ** 3
    return np.trapezoid(k ** 3 * P * W ** 2, lnk) / (2 * math.pi ** 2)
A = s8 ** 2 / sig2(8.0)
sig = lambda R: math.sqrt(A * sig2(R))
f = Om ** 0.55
x = 6.074 / 67.19
near("dH/H", x, 0.0904, 0.0003)
dl = -3 * x / f; db = bisect(lambda d: f / 2 * (1 - (1 + d) ** (2 / 3)) - x, -0.99, 0.0, tol=1e-10)
print(f"f={f:.4f} delta_lin={dl:.4f} delta_Bern={db:.4f}")
near("delta linear", dl, -0.51, 0.01); near("delta Bernardeau", db, -0.46, 0.01)
for R, want in [(50, 0.155), (100, 0.065), (150, 0.037), (300, 0.012), (450, 0.006)]:
    sg = sig(R); print(f"R={R}: sigma={sg:.4f}; |delta_lin|/sigma={-dl/sg:.1f}; |delta_B|/sigma={-db/sg:.1f}")
    near(f"sigma_delta R={R}", sg, want, max(0.1 * want, 0.001))
sh = f * sig(150) / 3
near("sigma(dH/H) at 150", sh, 0.0065, 0.0004); near("in km/s/Mpc", sh * 67.19, 0.44, 0.03)
near("void edge z for R=50 h^-1 Mpc", 50 / h * 67.19 / 299792.458, 0.017, 0.0007)
r = 370 / 6.074; near("Copernican radius (Mpc)", r, 61, 0.5)
near("R = 430 h^-1 Mpc in Mpc", 430 / h, 640, 2)
near("probability", (r / 640) ** 3, 8.6e-4, 0.3e-4)
series("(f/2)*(1-(1+d)**(2/3))", "d", 0, 2, "-f*d/3", domain={"f": (0.1, 1)})
units("370 km/s / (6.074 km/s/Mpc)", "Mpc")
raise SystemExit(finish())
