"""Crux C1: how far the refuters' labelled-phantom Ellis shortcut goes.

Checks, for a static Ellis throat r(l) = sqrt(l^2 + b0^2), Phi = 0 (G = c = 1 inside,
SI outside):
 1. e-folds of the unstable mode needed for a crossing between static observers at
    r = R_obs, at speed v (coordinate time = proper-length / v, Phi = 0 so t is proper
    time of static observers), with the worst-case e-folding time tau_e = b0/(sqrt(3) c)
    (Gonzalez-Guzman-Sarbach bound quoted in verdict C1-0);
 2. e-folds available before a 1 kg payload seed eps = gamma G m/(c^2 b0) goes nonlinear;
 3. the minimum speed at which the payload crosses before the mode goes nonlinear;
 4. lateral tidal acceleration on a radially moving body at the throat.
    For dl^2 + r(l)^2 dOmega^2, R_{theta l theta l} (orthonormal) = -r''/r = -1/b0^2 at l = 0.
    With R_{theta t theta t} = 0 (Phi = 0) the boosted lateral tidal component is
    gamma^2 v^2 / b0^2, so |Delta a| = gamma^2 (v/c)^2 c^2 xi / b0^2 (SI), for body size xi.
"""
import math

c = 2.99792458e8      # m/s
G = 6.67430e-11       # m^3 kg^-1 s^-2
ly = 9.4607e15        # m
g0 = 9.80665          # m/s^2

def proper_len(b0, R):
    # proper radial length from throat to areal radius R, one side: l = sqrt(R^2 - b0^2)
    return math.sqrt(R * R - b0 * b0)

def efolds_needed(b0, R_obs, v):
    T = 2 * proper_len(b0, R_obs) / (v * c)   # s, between static observers on both sides
    tau = b0 / (math.sqrt(3) * c)             # s, worst-case e-folding time
    return T, T / tau

def efolds_avail(b0, m, v):
    gam = 1 / math.sqrt(1 - v * v)
    eps = gam * G * m / (c * c * b0)
    return eps, math.log(1 / eps)

def lateral_tide(b0, v, xi):
    gam2 = 1 / (1 - v * v)
    return gam2 * v * v * c * c * xi / (b0 * b0)

print("Units: SI; v in units of c; b0 throat areal radius; R_obs = 10 b0")
T, N = efolds_needed(1.0, 10.0, 1.0)
print(f"check vs C1-0: b0 = 1 m, v = c: T_cross = {T:.4e} s, e-folds needed = {N:.2f}")
print(f"shortcut ratio at d = 1 ly: {T / (ly / c):.3e}")

m = 1.0  # kg
for b0 in [1.0, 1.0e3, 1.0e6, 1.0e9]:
    # bisection for minimum v such that needed <= available
    lo, hi = 1e-6, 1 - 1e-12
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        _, Nn = efolds_needed(b0, 10 * b0, mid)
        _, Na = efolds_avail(b0, m, mid)
        if Nn <= Na:
            hi = mid
        else:
            lo = mid
    vmin = hi
    eps, Na = efolds_avail(b0, m, vmin)
    a01 = lateral_tide(b0, vmin, 0.1)
    print(f"b0 = {b0:.1e} m, 1 kg: e-folds available = {Na:.1f}; minimum crossing speed "
          f"v_min = {vmin:.3f} c; lateral tide on a 0.1 m body at v_min = {a01:.2e} m/s^2 "
          f"= {a01 / g0:.2e} g")

# throat needed for the tide on a 0.1 m body at v = 0.6 c to stay below 20 g
v = 0.6
gam2 = 1 / (1 - v * v)
b_req = math.sqrt(gam2 * v * v * c * c * 0.1 / (20 * g0))
print(f"b0 needed for lateral tide < 20 g on 0.1 m at v = 0.6 c: {b_req:.2e} m")
print(f"exotic mass scale b0 c^2/G at that b0 (coefficient-1 measure, Q-26): "
      f"{b_req * c * c / G:.2e} kg")
# stress estimate in a 0.1 m, 1 kg body at b0 = 1 m, v_min: sigma ~ (m/xi^2) * a / 2
a = lateral_tide(1.0, 0.56, 0.1)
print(f"order-of-magnitude stress in a 1 kg, 0.1 m body at b0 = 1 m, v = 0.56 c: "
      f"{(1.0 / 0.1**2) * a / 2:.1e} Pa (steel yield ~1e9 Pa, order of magnitude)")
