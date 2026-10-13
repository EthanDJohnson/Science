"""Constraints lens: far-zone kinematics of one outgoing wave, and observational limits on path depletion.

Part A (kinematics). Pair production needs time-like total momentum q = k1 + k2, q^2 = s > 0. For the bilinear
source S(x) ~ h(x)^2 of an outgoing monochromatic spherical wave h ~ e^{i w (r - t)} W(r)/r (monopole toy, scalar
kinematics; W a smooth window switching the wave on at radius R over a width 0.15 R, times 1 - exp(-(r/0.5R)^4) so it vanishes at the origin), the 2w component of S has
spatial Fourier transform S(K) = (4 pi/K) int dr sin(K r) e^{2 i w r} W(r)/r. Keeping the slowly varying part,
|S(K)| depends on delta = 2w - K, and q^2 = 4 w^2 - K^2 ~ 4 w delta. The two-beam rate grows like s^2
(qft_second_order: Gamma ~ (1 - cos theta)^2), so the yield of the region beyond R is
    Y(R) ~ int_0^{2w} dK K^2 (4 w^2 - K^2)^2 |S(K)|^2 .
We compute Y(R) numerically for several w R and fit the power law. Expected: Y ~ (w R)^-3 (s ~ 4 w/R:
Fresnel-zone angular spread theta^2 ~ 1/(w R)). Units: w = 1 (lengths in 1/w).
Part B (observation). LIGO O3b calibration <= 11.29% in amplitude [D-39]; GW150914 at D_L = 410 Mpc [D-30];
GW amplitude ~ exp(-r/(2L)) for an energy e-folding length L. Lower bound on L, and what B&O and
Jones-Singleton (<r> ~ 1e11 m [D-53]) imply.
"""
import math
import numpy as np

print("=== Part A: yield of the region beyond R for one outgoing spherical wave (toy) ===")
w = 1.0

def Y(R, nK=400, nr=None):
    rmax = 40.0 * R
    nr = nr or int(60 * rmax)            # ~10 points per wavelength at 2w
    r = np.linspace(1e-3, rmax, nr)
    # on-window vanishes at r -> 0 (no constant leak near the origin), off-window far out
    Wr = 0.5 * (1 + np.tanh((r - R) / (0.15 * R))) * (1 - np.exp(-(r / (0.5 * R)) ** 4)) * 0.5 * (1 - np.tanh((r - 30 * R) / (3 * R)))
    # delta grid concentrated near the light cone
    d = np.geomspace(1e-4 / R, 2.0 * w, nK)
    K = 2 * w - d
    vals = np.empty_like(K)
    dr = r[1] - r[0]
    for i, Ki in enumerate(K):
        integrand = np.sin(Ki * r) * np.exp(2j * w * r) * Wr / r
        SK = 4 * math.pi / Ki * np.trapezoid(integrand, dx=dr) if Ki > 0 else 0.0
        vals[i] = Ki ** 2 * (4 * w ** 2 - Ki ** 2) ** 2 * abs(SK) ** 2
    return np.trapezoid(vals, d)

Rs = [20.0, 40.0, 80.0, 160.0]
Ys = []
for R in Rs:
    y1 = Y(R)
    y2 = Y(R, nK=600, nr=int(90 * 40 * R))      # convergence: 1.5x grids
    Ys.append(y1)
    print(f"  w R = {R:6.1f}: Y = {y1:.5e}  (1.5x grid: {y2:.5e}, rel diff {abs(y2-y1)/y1:.2e})")
sl = np.polyfit(np.log(Rs), np.log(Ys), 1)[0]
print(f"  fitted slope d ln Y / d ln R = {sl:.3f}   (expected -3)")
for i in range(len(Rs) - 1):
    print(f"    local slope {Rs[i]:.0f}->{Rs[i+1]:.0f}: {math.log(Ys[i+1]/Ys[i])/math.log(Rs[i+1]/Rs[i]):.3f}")

print("\n  Implication for GW150914 (lambda = c/150 Hz = 2.0e6 m): fraction of near-zone yield made beyond R,")
lam = 2.99792458e8 / 150.0
for R_m, lab in ((lam, "1 lambda"), (1e9, "1e9 m"), (1.5e11, "1 AU"), (3.086e19, "1 kpc"), (1.265e25, "410 Mpc")):
    print(f"    R = {lab:8s}: (lambda/(2 pi R))^3 = {(lam/(2*math.pi*R_m))**3:.3e}")

print("\n=== Part B: observational bound on path depletion ===")
D = 410 * 3.0857e22
cal = 0.1129
# amplitude factor exp(-D/(2L)) >= 1 - cal  ->  L >= D/(2 * -ln(1-cal))
Lmin = D / (2 * -math.log(1 - cal))
print(f"  GW150914: D_L = {D:.3e} m; amplitude calibration 11.29% -> energy e-folding length L > {Lmin:.3e} m = {Lmin/3.0857e22:.0f} Mpc")
LJS = 1e11
print(f"  Jones-Singleton <r> ~ 1e11 m: predicted amplitude factor exp(-D/(2L)) = exp(-{D/(2*LJS):.3e}) -> 0; "
      f"excluded by a factor D/(2 L_JS)/0.12 = {D/(2*LJS)/0.12:.2e} in the exponent")
# B&O face value: tau_h = 1.3e82 s (vacuum) and 1.7e73 s (stimulated) [D-47]
for tauh in (1.3e82, 1.7e73):
    frac = D / 2.99792458e8 / tauh
    print(f"  B&O tau_h = {tauh:.1e} s: energy fraction lost over 410 Mpc = {frac:.2e}; allowed <= {1-(1-cal)**2:.2f}")
