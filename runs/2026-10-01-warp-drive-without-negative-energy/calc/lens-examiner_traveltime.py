"""Examiner lens: travel-time test (brief premise 2).

Geometric units G = c = 1, lengths in metres, times in metres of light travel
(1 m = 3.3356 ns). Convention: ds^2 = -N^2 dt^2 + (dx - b dt)^2 along the x-axis
(Alcubierre's own sign: b = v f > 0 moves Eulerian observers toward +x).

Part A  Alcubierre bubble moving at v in the exterior frame (N = 1, flat slices).
        Payload arrival vs exterior light; one-way advance/delay of light that
        crosses the bubble; co- minus counter-propagating difference (Sagnac-like),
        compared with Fuchs et al. Table 1 (Alcubierre R = 15 m, v = 0.04: 8.0 ns).
        Gauge test: exterior-frame shift vs comoving Killing-vector norm.
Part B  Idealized thin-shell model of the 2024 warp shell: Schwarzschild exterior,
        flat interior with lapse N_in = sqrt(1 - 2M/R_s), constant interior shift b.
        Does a forward light ray through the cavity arrive before flat-space light?
        Minimum interior shift for any advance; Sagnac difference vs 7.6 ns.
Part C  Fell-Heisenberg static linear interior shift 1.26 (length unit assumed 1 m):
        local crossing advance of a stream through a static region.
"""
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

c = 299792458.0
ns_per_m = 1e9 / c
G = 6.674e-11
LY = 9.4607e15

print("=== Part A: Alcubierre, tanh wall f(r) = [tanh(s(r+R)) - tanh(s(r-R))]/(2 tanh(sR)) ===")


def f_alc(r, R, s):
    return (np.tanh(s * (r + R)) - np.tanh(s * (r - R))) / (2 * np.tanh(s * R))


def oneway_advance(R, s, v, direction, L=None):
    """Light along x-axis crossing a bubble of speed v (N=1).
    Comoving xi = x - v t: d xi/dt = direction*1 + v f - v.
    Advance = (|dx| covered) - (elapsed t); >0 means earlier than flat-space light."""
    if L is None:
        L = R + 40.0 / s
    if direction > 0:
        dt = quad(lambda xi: 1.0 / (1.0 - v * (1 - f_alc(abs(xi), R, s))), -L, L, limit=400)[0]
        dx = 2 * L + v * dt
    else:
        dt = quad(lambda xi: 1.0 / (1.0 + v * (1 - f_alc(abs(xi), R, s))), -L, L, limit=400)[0]
        dx = -2 * L + v * dt
    return abs(dx) - dt


for (R, s, v, label) in [(15.0, 2.0, 0.04, "Fuchs Table-1 comparator R=15 m, v=0.04 (s=2/m assumed)"),
                         (15.0, 0.5, 0.04, "same, softer wall s=0.5/m"),
                         (100.0, 2.0, 0.5, "R=100 m, Delta=1 m, v=0.5")]:
    a_f = oneway_advance(R, s, v, +1)
    a_b = oneway_advance(R, s, v, -1)
    print(f"{label}: forward advance = {a_f:.4f} m ({a_f*ns_per_m:.3f} ns); "
          f"backward advance = {a_b:.4f} m ({a_b*ns_per_m:.3f} ns); "
          f"co-minus-counter = {a_f - a_b:.4f} m = {(a_f - a_b)*ns_per_m:.3f} ns; "
          f"analytic 2Rv = {2*R*v:.4f} m, 4Rv = {4*R*v:.4f} m = {4*R*v*ns_per_m:.3f} ns")

print("\nSuperluminal reference case R = 100 m, Delta = 1 m (s = 2/m), v = 10:")
R, s, v = 100.0, 2.0, 10.0
D = 4.37 * LY
print(f"  Payload at centre: dx/dt = v f(0) = {v*f_alc(0, R, s):.6f}; proper time = coordinate time (N=1).")
print(f"  Alpha Cen D = 4.37 ly: payload arrival {D/(v*c)/3.156e7:.3f} yr vs exterior light {D/c/3.156e7:.3f} yr "
      f"-> genuine time advance IF the bubble already exists along the path.")
# Killing horizons in the comoving frame: comoving shift b' = v (f - 1); Killing vector d/dt' norm = -1 + v^2 (1-f)^2
rh = brentq(lambda r: v * (1 - f_alc(r, R, s)) - 1.0, R - 5, R + 5)
print(f"  Comoving Killing-vector norm -1 + v^2(1-f)^2 changes sign at r = {rh:.4f} m (f = {f_alc(rh,R,s):.4f} = 1 - 1/v);")
print(f"  for r > {rh:.3f} m (whole exterior) the comoving Killing vector is spacelike: horizon/ergoregion relative to the payload.")
print(f"  Exterior-frame shift at centre |b| = {v*f_alc(0,R,s):.2f} > N = 1, yet the centre is flat: '|b| > N' alone is gauge-dependent.")
for vv in [0.04, 0.5, 0.99]:
    mx = vv * 1.0  # max of v(1-f) is v (at f=0)
    print(f"  v = {vv}: max v(1-f) = {mx:.2f} < 1 -> no comoving Killing horizon")
# Forward light from payload stalls where d xi/dt = 1 - v(1-f) = 0 (same radius as rh)
print(f"  Forward-emitted light from the payload stalls at r = {rh:.4f} m (front horizon); backward light leaves.")

print("\n=== Part B: idealized thin-shell warp shell (Schwarzschild exterior, flat interior) ===")
M_kg = 4.49e27
M = G * M_kg / c**2
print(f"M = {M_kg:.3e} kg -> GM/c^2 = {M:.4f} m, 2GM/c^2 = {2*M:.4f} m")
for Rs in [10.0, 14.2, 20.0]:
    Nin = np.sqrt(1 - 2 * M / Rs)
    local_delay = 2 * Rs * (1 / Nin - 1)
    bmin = 1 - Nin
    for L in [100.0, 1e4]:
        ext = 2 * (2 * M * np.log((L - 2 * M) / (Rs - 2 * M)))
        print(f"  R_s = {Rs:5.1f} m: N_in = {Nin:.4f}; interior redshift delay (no shift) = {local_delay:.3f} m "
              f"({local_delay*ns_per_m:.2f} ns); exterior Shapiro-log term to r = {L:.0e} m on each side = {ext:.3f} m "
              f"({ext*ns_per_m:.2f} ns)")
    # with interior shift b (coordinate) forward crossing time 2Rs/(Nin+b)
    for b in [0.04, 0.04 * Nin]:
        fwd = 2 * Rs / (Nin + b)
        bwd = 2 * Rs / (Nin - b)
        print(f"     interior shift b = {b:.4f}: forward interior crossing {fwd:.3f} m vs flat {2*Rs:.1f} m -> "
              f"net {'ADVANCE' if fwd < 2*Rs else 'DELAY'} {abs(fwd-2*Rs):.3f} m before exterior log terms; "
              f"co-minus-counter = {bwd-fwd:.3f} m = {(bwd-fwd)*ns_per_m:.2f} ns (Fuchs: 7.6 ns)")
    print(f"     minimum interior coordinate shift for ANY forward advance (ignoring exterior delay): b > 1 - N_in = {bmin:.4f}"
          f" = {bmin/0.04:.1f} x the published 0.04")

print("\n=== Part C: Fell-Heisenberg static interior shift 1.26 (length unit assumed 1 m, r = 6) ===")
b, r = 1.26, 6.0
adv = 2 * r - 2 * r / (1 + b)
print(f"  forward stream crossing the interior (diameter {2*r} m) at coordinate speed 1+{b} gains {adv:.3f} m "
      f"({adv*ns_per_m:.2f} ns) on flat-space light; static region, so nothing is carried: a local time advance only,")
print("  which Olum / Gao-Wald tie to NEC failure (conceded by the authors).")
