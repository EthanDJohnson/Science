"""M-CONSTRAINTS-01: the static actuator envelope and the jerk ceiling from the rotor-speed lag
(lens findings F1 and F3).

Claim as I state it (SI units):
  (a) Level flight at maximum thrust T_max = 4 f_max: the vertical component of thrust must
      carry the weight, so with tilt angle th, T_max cos(th) = m g and
      a_horiz_max = g sqrt((T/W)^2 - 1),  th = arccos(W/T_max).
      T/W 4.10 (0.870 kg, 35 N) -> 39.0 m/s^2 at 75.9 deg; T/W 4.62 (0.750 kg, 34 N) ->
      44.3 m/s^2; T/W 12.35 (0.520 kg, 63 N) -> 120.8 m/s^2 at 85.4 deg.
      Hover throttle (m g/4)/f_max = 24.4 / 21.6 / 8.1 per cent.
  (b) With f = k_f omega^2 and a first-order rotor-speed lag tc, a full-throttle step from hover
      gives, at t = 0+,
          dT/dt = 4 * 2 k_f omega_h (omega_max - omega_h)/tc,  j_z(0) = dT/dt / m,
      i.e. 514 m/s^3 (Swift-like), 577 (Sun2022), 1262 (0.52 kg), and 2011 m/s^3 at tc = 10 ms;
      collective thrust reaches 95 per cent of maximum at t = -tc ln[(w_max - w_95)/(w_max - w_h)]
      = 117 ms; and the rotational route gives |da/dt| ~ a * omega_peak = 860 m/s^3 at
      a = 39 m/s^2, omega = 22 rad/s.
Domain: f_max > 0, 4 f_max > m g, k_f > 0, tc > 0; rigid body, no inflow or battery sag.
"""
import sys
import math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, inequality, units, quantity, finish


def approx(label, got, want, rel=0.015):
    print(f"  {label}: got {got:.6g}, lens {want:.6g}")
    return inequality(f"Abs({got!r} - ({want!r}))", "<", f"{rel}*Abs({want!r})")


G = 9.81
K_F = 1.51e-6

print("1. the level-flight envelope, derived from T cos(th) = m g, T sin(th) = m a")
tw, th = sp.symbols("tw th", positive=True)
identity(sp.sqrt(tw ** 2 - 1), sp.tan(sp.acos(1 / tw)), domain={"tw": (1.001, 20.0)})
limit(sp.sqrt(tw ** 2 - 1), "tw", 1, 0)                 # T/W -> 1: no horizontal authority
limit(sp.sqrt(tw ** 2 - 1) / tw, "tw", "oo", 1)         # huge T/W: a -> g*(T/W)
units("9.81 m/s^2 * 3.977", "m/s^2")

plats = [("Swift-like", 0.870, 35.0, 4.10, 39.0, 75.9, 24.4, 514.0),
         ("Sun2022", 0.750, 34.0, 4.62, 44.3, None, 21.6, 577.0),
         ("0.52 kg hi-T/W", 0.520, 63.0, 12.35, 120.8, 85.4, 8.1, 1262.0)]
for name, m, T_max, want_tw, want_a, want_th, want_thr, want_j in plats:
    W = m * G
    tw_v = T_max / W
    a_h = G * math.sqrt(tw_v ** 2 - 1.0)
    tilt = math.degrees(math.acos(1.0 / tw_v))
    thr = (W / 4.0) / (T_max / 4.0) * 100.0
    print(f"   {name}: T/W = {tw_v:.3f}, a_horiz = {a_h:.2f} m/s^2 ({a_h/G:.2f} g) at "
          f"{tilt:.2f} deg, hover throttle {thr:.2f} %")
    approx(f"{name} T/W", tw_v, want_tw, rel=0.01)
    approx(f"{name} a_horiz [m/s^2]", a_h, want_a, rel=0.01)
    approx(f"{name} hover throttle [%]", thr, want_thr, rel=0.01)
    if want_th:
        approx(f"{name} tilt [deg]", tilt, want_th, rel=0.01)

print("2. jerk at the start of a full-throttle step from hover")
kf, wh, wm, tc, mm = sp.symbols("kf wh wm tc mm", positive=True)
# omega(t) = wm - (wm - wh) exp(-t/tc); T(t) = 4 kf omega^2; j = T'/mm
w_t = wm - (wm - wh) * sp.exp(-sp.Symbol("t", positive=True) / tc)
jerk = sp.diff(4 * kf * w_t ** 2, sp.Symbol("t", positive=True)) / mm
j0 = sp.simplify(jerk.subs(sp.Symbol("t", positive=True), 0))
print("   j(0) =", j0)
identity(j0, 8 * kf * wh * (wm - wh) / (tc * mm))
limit(j0, "tc", "oo", 0)                          # a slow motor gives no jerk: j ~ 1/tc
units("8 * 1.51e-6 N*s^2 * 1188.7 /s * 1218.5 /s / (0.0391 s * 0.870 kg)", "m/s^3")

for name, m, T_max, want_tw, want_a, want_th, want_thr, want_j in plats:
    w_h = math.sqrt(m * G / (4.0 * K_F))
    w_max = math.sqrt((T_max / 4.0) / K_F)
    j = 8.0 * K_F * w_h * (w_max - w_h) / (0.0391 * m)
    print(f"   {name}: omega_h = {w_h:.1f}, omega_max = {w_max:.1f} rad/s, j_z(0) = {j:.1f} m/s^3 "
          f"({j/G:.1f} g/s)")
    approx(f"{name} j_z(0) [m/s^3]", j, want_j, rel=0.01)

m, T_max = 0.870, 35.0
w_h = math.sqrt(m * G / (4.0 * K_F))
w_max = math.sqrt((T_max / 4.0) / K_F)
approx("j_z(0) at tc = 10 ms [m/s^3]", 8.0 * K_F * w_h * (w_max - w_h) / (0.010 * m), 2011.0, rel=0.01)
approx("j_z(0) in g/s", 8.0 * K_F * w_h * (w_max - w_h) / (0.0391 * m) / G, 52.0, rel=0.02)

print("3. time to 95 per cent of maximum collective thrust")
w95 = math.sqrt(0.95) * w_max
t95 = -0.0391 * math.log((w_max - w95) / (w_max - w_h))
print(f"   omega_95 = {w95:.1f} rad/s -> t95 = {1000*t95:.1f} ms")
approx("t95 [ms]", 1000 * t95, 117.0, rel=0.02)
inequality("1 - exp(-1)", "<", "0.95")             # 95 per cent needs more than one time constant

print("4. the rotational route to changing the acceleration vector")
approx("|da/dt| = a * omega [m/s^3]", 39.0 * 22.0, 860.0, rel=0.01)
units("39.0 m/s^2 * 22.0 /s", "m/s^3")
# the two routes are within a factor of two of each other
inequality(f"{39.0*22.0/514.3!r}", "<", "2")

raise SystemExit(finish())
