#!/usr/bin/env python3
"""Mechanist lens, calculation 2: the BLIND TIME chain, the rotor spin-down mechanism,
and the burst-power mechanism.  SI units throughout (m, s, rad, N, kg, W, A).

Why these three.  The look-ahead bound v*tau + v^2/(2a) <= s (calculation 1) treats tau as
a pure sensing+compute transport delay and a as instantly available.  Physically it is not:
an underactuated quadrotor must ROTATE its thrust vector before any braking or dodging
acceleration exists, and the rotation itself is rate-limited by rotor inertia and motor lag.
So actuator bandwidth enters the perception bound as an ADDITIVE latency, not as a separate
limit.  Parts:

  A. verification of the two look-ahead bounds of calculation 1 by direct integration.
  B. blind time: bang-bang reorientation to the braking attitude with first-order motor lag,
     giving tau_rot; then the speed penalty and the elasticities when tau_eff = tau_s + tau_rot.
  C. rotor spin-down with no active braking: J_r omega_dot = -k_m omega^2, which sets a FLOOR
     on the motor time constant for a fixed-pitch unidirectional rotor, and says what moving
     it would take (lighter rotor, active braking, more rotors).
  D. burst electrical power and pack current at the thrust ceiling, from momentum theory,
     the mundane mechanism behind the "battery-voltage fluctuation" failure cause (D-14).

Model/assumption notes are printed next to each result.  Lines beginning "PASS"/"FAIL" are
verification checks.
"""
import math
import sys

sys.path.insert(0, "runs/2026-10-15-quadrotor-agility-limit/tools")
import quadrotor as qr  # noqa: E402

g = 9.81
RHO = 1.225  # kg/m^3, sea-level air density

n_pass = [0]
n_fail = [0]


def check(name, got, want, tol, note=""):
    ok = abs(got - want) <= tol
    n_pass[0] += ok
    n_fail[0] += (not ok)
    print(f"  {'PASS' if ok else 'FAIL'} {name}: got {got:.6g}, want {want:.6g} "
          f"(tol {tol:.2g}){(' - ' + note) if note else ''}")


# ======================================================================= part A
print("=" * 78)
print("PART A  verification of the look-ahead bounds of calculation 1")
print("=" * 78)


def v_stop(s, a, tau):
    return a * (-tau + math.sqrt(tau ** 2 + 2.0 * s / a))


def distance_travelled(v, a, tau, dt=1e-6):
    """Integrate: tau seconds at constant v, then brake at a until v = 0."""
    x, vv, t = 0.0, v, 0.0
    while t < tau:
        x += vv * dt
        t += dt
    while vv > 0.0:
        x += vv * dt
        vv -= a * dt
    return x


for (s, a, tau) in ((6.0, 42.03, 0.1066), (3.0, 20.0, 0.05), (10.0, 120.76, 0.15)):
    v = v_stop(s, a, tau)
    d = distance_travelled(v, a, tau)
    check(f"stop bound s={s} m a={a} m/s^2 tau={tau*1e3:.1f} ms: integrated distance [m]",
          d, s, 2e-3, f"v_max = {v:.4f} m/s")
# zero-latency limit must reduce to sqrt(2 a s)
check("tau -> 0 limit of v_stop [m/s]", v_stop(6.0, 42.03, 0.0),
      math.sqrt(2 * 42.03 * 6.0), 1e-9, "sqrt(2 a s)")
# dodge bound: at v = s/(tau+2 sqrt(r/a)) the lateral displacement after the manoeuvre is r
r, a_lat, tau_d, s_d = 0.5, 42.03, 0.1066, 6.0
v_d = s_d / (tau_d + 2.0 * math.sqrt(r / a_lat))
t_man = s_d / v_d - tau_d                       # time available for the dodge
lat = 2.0 * (0.5 * a_lat * (t_man / 2.0) ** 2)  # bang-bang lateral displacement
check("dodge bound: lateral displacement achieved in the available time [m]", lat, r, 1e-9,
      f"v_dodge = {v_d:.4f} m/s")

# ======================================================================= part B
print()
print("=" * 78)
print("PART B  blind time: reorienting the thrust vector before any braking exists")
print("=" * 78)
q = qr.platform_sun2022()
h = q.hover()
M = q.mix_matrix()
print(f"  platform: {q.name}, m = {q.mass} kg, Jy = {q.inertia[1]:.2e} kg m^2, "
      f"arm {q.arm_length} m at {q.arm_angle_deg} deg, per-rotor thrust limit "
      f"{q.thrust_max} N, motor_tau = {q.motor_tau*1e3:.1f} ms")
print(f"  hover: T/W = {h['thrust_to_weight']:.3f}, hover rotor speed "
      f"{h['omega_hover']:.1f} rad/s, horizontal accel ceiling "
      f"{g*math.sqrt(h['thrust_to_weight']**2 - 1):.2f} m/s^2")

lx = q.arm_length * math.cos(math.radians(q.arm_angle_deg))  # pitch moment arm [m]
tau_y_max = lx * 2.0 * q.thrust_max          # two rear rotors at the limit, two front at zero
alpha_max = tau_y_max / q.inertia[1]          # rad/s^2
check("pitch moment arm l cos(beta) [m]", lx, 0.14 * math.cos(math.radians(56.0)), 1e-12)
check("max pitch torque from the mix matrix [N m]",
      float(abs(M[2, 0])) * 2.0 * q.thrust_max, tau_y_max, 1e-12,
      "mix row 3 (tau_y) per unit rotor thrust, x2 rotors")
print(f"  max pitch torque {tau_y_max:.3f} N m -> max angular accel {alpha_max:.1f} rad/s^2 "
      f"({math.degrees(alpha_max):.0f} deg/s^2)  [ASSUMES the full thrust limit is spent on "
      "pitch, so collective is then m g only on two rotors: an upper bound on alpha]")


def rot_time_ideal(theta, alpha):
    """Rest-to-rest bang-bang rotation time [s] for a double integrator."""
    return 2.0 * math.sqrt(theta / alpha)


def rot_time_lag(theta, alpha, tau_m, dt=2e-6):
    """Same rotation with the torque passed through a first-order lag of tau_m.
    Bang-bang switch at half the angle; integrate until theta is reached with |rate| small."""
    if tau_m <= 0:
        return rot_time_ideal(theta, alpha)
    th, rate, acc, t = 0.0, 0.0, 0.0, 0.0
    decay = math.exp(-dt / tau_m)          # exact first-order update, stable for any tau_m
    while th < theta and t < 5.0:
        cmd = alpha if th < theta / 2.0 else -alpha
        acc = cmd + (acc - cmd) * decay
        rate += acc * dt
        th += rate * dt
        t += dt
    return t


check("rotation time, lag -> 0, matches the closed form [s]",
      rot_time_lag(1.0, alpha_max, 1e-6), rot_time_ideal(1.0, alpha_max), 1e-3)
check("rotation time grows with lag (monotone) [s]",
      1.0 if rot_time_lag(1.0, alpha_max, 0.08) > rot_time_lag(1.0, alpha_max, 0.02) else 0.0,
      1.0, 1e-12, "sanity: more lag, slower rotation")

print("\n  tilt the braking manoeuvre needs, and the time to get there")
print("  (theta = atan(a_x/g); tau_rot = rest-to-rest bang-bang time with motor lag;")
print("   the vehicle is effectively BLIND-and-inert for about tau_rot/2 of it,")
print("   because the braking force only builds as the tilt grows)")
for ax in (5.0, 10.0, 20.0, 30.0, 40.0):
    th = math.atan(ax / g)
    t_ideal = rot_time_ideal(th, alpha_max)
    t_lag = rot_time_lag(th, alpha_max, q.motor_tau)
    print(f"   a_x = {ax:5.1f} m/s^2 -> tilt {math.degrees(th):5.1f} deg: "
          f"tau_rot(no lag) {t_ideal*1e3:6.1f} ms, with {q.motor_tau*1e3:.1f} ms motor lag "
          f"{t_lag*1e3:6.1f} ms  (lag cost {(t_lag-t_ideal)*1e3:5.1f} ms)")

print("\n  effect on the look-ahead bound: tau_eff = tau_sense + f * tau_rot")
a_h = g * math.sqrt(h['thrust_to_weight'] ** 2 - 1)
theta_b = math.atan(a_h / g)
tau_rot = rot_time_lag(theta_b, alpha_max, q.motor_tau)
print(f"   full-brake tilt {math.degrees(theta_b):.1f} deg, tau_rot = {tau_rot*1e3:.1f} ms, "
      f"a_h = {a_h:.2f} m/s^2")
for s in (3.0, 6.0, 10.0):
    for tau_s in (0.040, 0.107):
        for frac, lab in ((0.0, "rotation ignored"), (0.5, "half the rotation counted"),
                          (1.0, "all of it counted")):
            tau_e = tau_s + frac * tau_rot
            print(f"   s={s:4.1f} m, tau_sense={tau_s*1e3:5.1f} ms, {lab:24s}: "
                  f"tau_eff={tau_e*1e3:6.1f} ms -> v_stop={v_stop(s, a_h, tau_e):6.2f} m/s")


def elast(f, x, h_rel=1e-5):
    hh = h_rel * x
    return (math.log(f(x + hh)) - math.log(f(x - hh))) / (math.log(x + hh) - math.log(x - hh))


print("\n  elasticities at s = 6 m, tau_sense = 40 ms, half the rotation counted")
tau_e0 = 0.040 + 0.5 * tau_rot
print(f"   tau_eff = {tau_e0*1e3:.1f} ms, v = {v_stop(6.0, a_h, tau_e0):.2f} m/s")
print(f"   d ln v / d ln s        = {elast(lambda x: v_stop(x, a_h, tau_e0), 6.0):+.3f}")
print(f"   d ln v / d ln a_h      = {elast(lambda x: v_stop(6.0, x, tau_e0), a_h):+.3f}")
print(f"   d ln v / d ln tau_sense= "
      f"{elast(lambda x: v_stop(6.0, a_h, x + 0.5*tau_rot), 0.040):+.3f}")
print(f"   d ln v / d ln tau_rot  = "
      f"{elast(lambda x: v_stop(6.0, a_h, 0.040 + 0.5*x), tau_rot):+.3f}")
# how tau_rot responds to the motor time constant and to the inertia
print("   d ln tau_rot / d ln motor_tau = "
      f"{elast(lambda x: rot_time_lag(theta_b, alpha_max, x), q.motor_tau, 2e-2):+.3f}")
print("   d ln tau_rot / d ln alpha_max = "
      f"{elast(lambda x: rot_time_lag(theta_b, x, q.motor_tau), alpha_max, 2e-2):+.3f}  "
      "(-0.5 is the no-lag scaling)")

# ======================================================================= part C
print()
print("=" * 78)
print("PART C  rotor spin-DOWN with no active braking: J_r omega' = -k_m omega^2")
print("=" * 78)
print("  Fixed-pitch unidirectional rotors can only reduce thrust by letting the rotor slow")
print("  against its own aerodynamic drag torque (unless the ESC brakes actively).  The exact")
print("  solution is omega(t) = omega0 / (1 + t/t_c) with t_c = J_r/(k_m omega0), so the")
print("  INITIAL time constant of the decay is t_c and it is NOT symmetric with spin-up.")
om_h = h['omega_hover']
print(f"  hover rotor speed omega_h = {om_h:.1f} rad/s; k_m = {q.k_torque:.3e} N m s^2/rad^2 "
      f"(Sun et al. TABLE II, via the tool)")


def spin_down(om0, J_r, k_m, t):
    return om0 / (1.0 + t * k_m * om0 / J_r)


def spin_down_num(om0, J_r, k_m, t_end, dt=1e-7):
    om, t = om0, 0.0
    while t < t_end:
        om += -k_m * om * om / J_r * dt
        t += dt
    return om


J_test, t_test = 1e-5, 0.03
check("spin-down closed form vs numerical integration [rad/s]",
      spin_down_num(om_h, J_test, q.k_torque, t_test),
      spin_down(om_h, J_test, q.k_torque, t_test), 2e-3)
print("  ASSUMED rotor+bell polar inertia J_r (not retrieved in the dossier; 5-inch racing")
print("  props with the motor bell are of order 1e-5 kg m^2):")
for J_r in (3e-6, 6e-6, 1e-5, 2e-5, 3e-5):
    t_c = J_r / (q.k_torque * om_h)
    # time to lose 10 per cent of thrust: thrust ~ omega^2, so omega -> 0.9487 omega_h
    t10 = (1.0 / math.sqrt(0.9) - 1.0) * t_c
    print(f"   J_r = {J_r:7.1e} kg m^2 -> free spin-down time constant t_c = {t_c*1e3:6.1f} ms;"
          f" time to shed 10 % of thrust {t10*1e3:5.1f} ms")
J_match = 0.0391 * q.k_torque * om_h
print(f"  the J_r that makes t_c equal the MEASURED 39.1 ms thrust time constant (A-03): "
      f"{J_match:.2e} kg m^2")
J_match2 = 0.033 * q.k_torque * om_h
print(f"  the J_r that makes t_c equal the measured 33 ms rotor-speed constant (A-04): "
      f"{J_match2:.2e} kg m^2")
print("  Reading: a 1e-5 kg m^2 rotor group gives a free-decay constant of the same tens-of-ms")
print("  order as the measured constant, so the measured 'motor time constant' on a")
print("  unidirectional fixed-pitch rotor is largely the rotor's own inertia divided by its")
print("  drag torque, not an electrical limit.  Moving it needs a lighter/smaller rotor, an")
print("  actively braking ESC, or more rotors (same thrust, smaller J_r each).")
for scale, lab in ((0.5, "half the rotor inertia (3-inch prop class)"),
                   (1.0, "baseline"), (2.0, "double inertia (6-inch prop)")):
    tm = 0.0391 * scale
    print(f"   {lab:40s}: motor_tau {tm*1e3:5.1f} ms -> tau_rot "
          f"{rot_time_lag(theta_b, alpha_max, tm)*1e3:6.1f} ms -> v_stop(s=6 m, "
          f"tau_sense=40 ms, half rotation) "
          f"{v_stop(6.0, a_h, 0.040 + 0.5*rot_time_lag(theta_b, alpha_max, tm)):.2f} m/s")

# ======================================================================= part D
print()
print("=" * 78)
print("PART D  burst power and pack current at the thrust ceiling (momentum theory)")
print("=" * 78)
print("  P_ideal = T^(3/2)/sqrt(2 rho A_total) (hover/axial momentum theory, static);")
print("  shaft power = P_ideal / FM (figure of merit), electrical = shaft / eta_motor+ESC.")
for (d_in, n_rot, T_tot, label) in ((5.0, 4, 35.0, "Swift-class, 35 N max static (A-09)"),
                                    (5.1, 4, 40.0, "Agilicious/Loquercio-class, ~40 N (A-20)"),
                                    (5.0, 4, 63.0, "high-thrust mocap platform, 63 N (A-11)")):
    R = d_in * 0.0254 / 2.0
    A = n_rot * math.pi * R * R
    P_ideal = T_tot ** 1.5 / math.sqrt(2.0 * RHO * A)
    for FM, eta in ((0.65, 0.80),):
        P_sh = P_ideal / FM
        P_el = P_sh / eta
        for V in (14.8, 22.2):
            I = P_el / V
            print(f"   {label:46s} disk area {A:.4f} m^2: P_ideal {P_ideal:6.0f} W, "
                  f"P_elec {P_el:6.0f} W (FM {FM}, eta {eta}) -> {I:5.0f} A at {V:.1f} V "
                  f"= {I/1.8:4.0f} C on a 1800 mAh pack")
            break
print("  Sag: with an assumed pack internal resistance R_int the terminal voltage falls by")
print("  I*R_int, and static thrust scales about as V^2 (rotor speed ~ V), so:")
for R_int in (0.010, 0.020, 0.030):
    for I in (60.0, 90.0, 120.0):
        V0 = 16.8  # 4S fully charged, V
        V = V0 - I * R_int
        print(f"   R_int = {R_int*1e3:4.1f} mOhm, I = {I:5.1f} A -> V {V0:.1f} -> {V:.2f} V "
              f"({100*(1-V/V0):4.1f} % drop) -> thrust ratio {(V/V0)**2:.3f} "
              f"-> T/W 4.40 becomes {4.40*(V/V0)**2:.2f}, a_h "
              f"{g*math.sqrt(max((4.40*(V/V0)**2)**2-1,0)):.1f} m/s^2")
print("  ASSUMED: R_int values are plausible 4S racing-pack numbers, NOT retrieved from a")
print("  datasheet (dossier section 6 lists battery power limits as not retrieved); the V^2")
print("  static-thrust scaling assumes rotor speed proportional to applied voltage.")

print()
print("=" * 78)
print("PART E  the COUPLED bound: FoV-limited usable accel AND the blind time it costs")
print("=" * 78)
print("  usable braking accel a_u = min(a_h, g tan(half-FoV + mount tilt)), because beyond that")
print("  tilt the obstacle and the future path leave a body-fixed camera's image; tau_eff =")
print("  tau_sense + half the rotation time to the tilt a_u needs.")
for (half_deg, label) in ((29.0, "D435i depth, 58 deg V FoV, level mount"),
                          (59.0, "D435i depth, mounted 30 deg up (A-20 above 7 m/s)"),
                          (43.5, "D435i depth, 87 deg H FoV (lateral dodge)"),
                          (57.5, "MonoRace lens, 115 deg vertical (A-26)"),
                          (77.5, "MonoRace lens, 155 deg horizontal (A-26)"),
                          (90.0, "no FoV limit (omnidirectional sensing)")):
    a_fov = g * math.tan(math.radians(min(half_deg, 89.0)))
    a_u = min(a_h, a_fov)
    th_u = math.atan(a_u / g)
    t_rot_u = rot_time_lag(th_u, alpha_max, q.motor_tau)
    for (s, tau_s) in ((6.0, 0.107), (6.0, 0.040)):
        tau_e = tau_s + 0.5 * t_rot_u
        print(f"   {label:52s} a_u={a_u:5.1f} m/s^2, tau_rot={t_rot_u*1e3:5.1f} ms, "
              f"s={s:.0f} m, tau_sense={tau_s*1e3:5.1f} ms -> tau_eff={tau_e*1e3:5.1f} ms, "
              f"v_stop={v_stop(s, a_u, tau_e):6.2f} m/s")
print("\n  per cent speed gain from a 10 per cent relaxation of each limit, at the")
print("  D435i-30-deg-up operating point (s = 6 m, tau_sense = 107 ms):")
a_fov0 = g * math.tan(math.radians(59.0))
a_u0 = min(a_h, a_fov0)
t_rot0 = rot_time_lag(math.atan(a_u0 / g), alpha_max, q.motor_tau)
tau_e0b = 0.107 + 0.5 * t_rot0
v0 = v_stop(6.0, a_u0, tau_e0b)
print(f"   baseline v = {v0:.2f} m/s (a_u = {a_u0:.1f} m/s^2, tau_eff = {tau_e0b*1e3:.1f} ms)")
print(f"   +10 % range  (s 6 -> 6.6 m)      : {100*(v_stop(6.6, a_u0, tau_e0b)/v0-1):+5.2f} %")
print(f"   -10 % tau_sense (107 -> 96.3 ms) : "
      f"{100*(v_stop(6.0, a_u0, 0.0963 + 0.5*t_rot0)/v0-1):+5.2f} %")
_t_fast = rot_time_lag(math.atan(a_u0 / g), alpha_max, q.motor_tau * 0.9)
print(f"   -10 % motor_tau (39.1 -> 35.2 ms): "
      f"{100*(v_stop(6.0, a_u0, 0.107 + 0.5*_t_fast)/v0-1):+5.2f} %")
_a_fov10 = g * math.tan(math.radians(59.0 * 1.1))
_a_u10 = min(a_h, _a_fov10)
_t10 = rot_time_lag(math.atan(_a_u10 / g), alpha_max, q.motor_tau)
print(f"   +10 % half-FoV (59 -> 64.9 deg)  : "
      f"{100*(v_stop(6.0, _a_u10, 0.107 + 0.5*_t10)/v0-1):+5.2f} %")
_a_h2 = g * math.sqrt((1.1 * h['thrust_to_weight']) ** 2 - 1)
_a_u2 = min(_a_h2, a_fov0)
print(f"   +10 % thrust-to-weight           : "
      f"{100*(v_stop(6.0, _a_u2, 0.107 + 0.5*t_rot0)/v0-1):+5.2f} %  "
      "(zero when the FoV, not thrust, sets a_u)")

print()
print(f"checks: {n_pass[0]} PASS, {n_fail[0]} FAIL")
