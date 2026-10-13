"""M-EXAMINER-04: fraction of the retarded toy yield made beyond radius R (natural units, w = 1, q0 = 2w).
Own setup: window W_R(r) applied to the source j = g(t-r)^2/r^2; W_R a smooth step at R of width D with
dW/dr = normal pdf(r; R, D). Radial factor (M-EXAMINER-02 conventions):
  I_R(q) = Int_0^inf W_R(r) e^{i q0 r} sin(q r)/r dr = [K(q0 + q) - K(q0 - q)]/(2i),
  K(k) = Int W_R(r) e^{i k r}/r dr = Int W_R'(r) E1(-i k r) dr   (integration by parts; E1(-ikr) -> 0 as r -> inf).
Yield beyond R (p = 2 vertex):  Y(R) = Int_0^{q0} dq (q0^2 - q^2)^2 abs(I_R(q))^2;  whole space I = i artanh(q/q0).
Claims (lens F3): F(R) = Y(R)/Y(0) = 0.55, 0.16, 0.018, 2.7e-3, 3.6e-4, 2.3e-5, 2.9e-6 at wR = 1, 2, 5, 10, 20, 50, 100,
local slope ~ -3; window-shape sensitivity ~ x2 (D = R/8 vs R/4; checked here with R/8 and R/5).
Own scaling estimate: for delta = q0 - q, the slow term K(delta) ~ O(1) only for delta < 1/R, weight (q0^2-q^2)^2 ~ (2 q0 delta)^2,
so Y(R) ~ Int_0^{1/R} delta^2 d delta ~ R^-3 for a smooth window (a sharp window leaks ~ R^-2)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
from scipy.special import exp1
from scipy.integrate import quad
import sympy as sp
from math_checks import identity, inequality, finish

q0 = 2.0
xg, wg = np.polynomial.hermite_e.hermegauss(80)       # nodes for N(0,1)
wg = wg / wg.sum()

from scipy.special import ndtr
_grid = {}
def K(k, R, D):
    # K(k) = Int W(r) e^{ikr}/r dr, W = Phi((r-R)/D): dense trapezoid on [max(R-8D, R/1000), R+8D] (resolves
    # oscillations up to k = 4 and the window ramp), plus the exact tail Int_{R+8D}^inf e^{ikr}/r dr = E1(-i k (R+8D)).
    # (A first version used 80-node Gauss-Hermite on W' E1(-ikr); it under-resolves e^{ikr} once kD >> 10 and leaked
    # a spurious R^-2 floor at wR >= 50.)
    key = (R, D)
    if key not in _grid:
        a, b = max(R - 8 * D, R / 1000), R + 8 * D
        n = int((b - a) / min(0.02, D / 50)) + 1
        r = np.linspace(a, b, n)
        _grid[key] = (r, ndtr((r - R) / D) / r, b)
    r, wr, b = _grid[key]
    f = wr * np.exp(1j * k * r)
    return np.trapezoid(f, r) + exp1(-1j * k * b)

def I_R(q, R, D):
    return (K(q0 + q, R, D) - K(q0 - q, R, D)) / 2j

def Y(R, D, p=2):
    f = lambda u: (q0 ** 2 - (q0 - np.exp(u)) ** 2) ** p * abs(I_R(q0 - np.exp(u), R, D)) ** 2 * np.exp(u)
    lo, hi = np.log(1e-9), np.log(q0)
    pts = sorted(set([np.log(x) for x in (0.1 / R, 1 / R, 10 / R) if 1e-9 < x < q0]))
    return quad(f, lo, hi, points=pts, limit=800, epsabs=0, epsrel=1e-7)[0]

def Y0(p=2):
    return quad(lambda q: (q0 ** 2 - q ** 2) ** p * np.arctanh(q / q0) ** 2, 0, q0, limit=400)[0]

# sanity: tiny R recovers the whole-space value
print("I_R(q=1) at R=1e-2, D=1e-3:", I_R(1.0, 1e-2, 1e-3), "  whole space: i artanh(1/2) = 0.5493i")
identity(sp.Float(round(abs(I_R(1.0, 1e-2, 1e-3)), 3)), sp.Float(round(np.arctanh(0.5), 3)))

Rs = [1, 2, 5, 10, 20, 50, 100, 200]
lens = {1: 0.55, 2: 0.16, 5: 0.018, 10: 2.7e-3, 20: 3.6e-4, 50: 2.3e-5, 100: 2.9e-6}
y0 = Y0()
res = {}
for frac in (8, 5):
    F = [Y(R, R / frac) / y0 for R in Rs]
    res[frac] = F
    print(f"D = R/{frac}: " + ", ".join(f"wR={R}: {f:.3g}" for R, f in zip(Rs, F)))
    sl = [np.log(F[i + 1] / F[i]) / np.log(Rs[i + 1] / Rs[i]) for i in range(len(Rs) - 1)]
    print("   local slopes:", ", ".join(f"{s:.2f}" for s in sl))
for R in lens:
    i = Rs.index(R)
    print(f"wR={R}: lens {lens[R]:.3g}; own D=R/8 {res[8][i]:.3g}, D=R/5 {res[5][i]:.3g}")
F8 = res[8]
slope_10_100 = np.log(F8[Rs.index(100)] / F8[Rs.index(10)]) / np.log(10)
print(f"mean slope wR 10 -> 100 (D=R/8): {slope_10_100:.3f}")
inequality(sp.Float(slope_10_100), "<", sp.Float(-2.7))
inequality(sp.Float(slope_10_100), ">", sp.Float(-3.3))
# value at wR = 10 within a factor 3 of the lens's 2.7e-3
inequality(sp.Float(abs(np.log(F8[Rs.index(10)] / 2.7e-3))), "<", sp.Float(np.log(3)))
# sharp window (D -> small) for contrast: leakage expected to flatten the slope toward -2
Fs = [Y(R, R / 40) / y0 for R in (10, 100)]
print(f"narrower window D = R/40: F(10) = {Fs[0]:.3g}, F(100) = {Fs[1]:.3g}, slope {np.log(Fs[1]/Fs[0])/np.log(10):.2f}")
raise SystemExit(finish())
