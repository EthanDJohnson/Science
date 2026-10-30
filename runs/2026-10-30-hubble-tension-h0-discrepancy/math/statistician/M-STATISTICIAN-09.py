"""M-STATISTICIAN-09: calibrator-subsample variance (F14).
n of N iid calibrators with per-SN scatter s (mag): Var(mean_n - mean_N) = s^2 (1/n - 1/N).
sigma_H0 = H0 * ln(10)/5 * sigma_mag (from H0 proportional to 10^(0.2 M_B))."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/statistician")
import mpmath as mp
import sympy as sp
from _common import close
from math_checks import identity, limit, units, finish

n, N, s = sp.symbols("n N s", positive=True)
# nested: mean_N = (n/N) mean_n + ((N-n)/N) mean_rest; difference = (1 - n/N)(mean_n - mean_rest)
var_diff = (1 - n / N) ** 2 * (s**2 / n + s**2 / (N - n))
identity(var_diff, s**2 * (1 / n - 1 / N), domain={"n": (1, 20), "N": (21, 100), "s": (0.05, 0.3)})
limit(s**2 * (1 / n - 1 / N), "n", N, 0)  # whole sample: no subsample difference
units("70 km/s/Mpc * 0.0259", "km/s/Mpc")
H = sp.symbols("H", positive=True); M = sp.symbols("M")
identity(sp.diff(H * sp.exp(sp.log(10) / 5 * M), M), H * sp.exp(sp.log(10) / 5 * M) * sp.log(10) / 5, domain={"M": (-1, 1)})


def sig(nn, NN, smag, H0):
    return H0 * mp.log(10) / 5 * smag * mp.sqrt(mp.mpf(1) / nn - mp.mpf(1) / NN)


for H0 in (70.39, 73.49):
    a, b = sig(11, 42, 0.10, H0), sig(11, 42, 0.15, H0)
    c, d = sig(24, 42, 0.10, H0), sig(24, 42, 0.15, H0)
    print(f"H0 = {H0}: 11/42 sigma {float(a):.3f}-{float(b):.3f} -> z(2.5) {float(2.5/b):.2f}-{float(2.5/a):.2f}; "
          f"24/42 sigma {float(c):.3f}-{float(d):.3f} -> z {float(2.5/d):.2f}-{float(2.5/c):.2f}")
close("11/42, s = 0.10, H0 = 70.39: sigma", sig(11, 42, .10, 70.39), 0.84, 0.01)
close("11/42, s = 0.15, H0 = 73.49: sigma", sig(11, 42, .15, 73.49), 1.31, 0.01)
close("24/42, z at s = 0.15, H0 = 73.49", 2.5 / sig(24, 42, .15, 73.49), 3.7, 0.05)
close("24/42, z at s = 0.10, H0 = 73.49", 2.5 / sig(24, 42, .10, 73.49), 5.6, 0.1)
raise SystemExit(finish())
