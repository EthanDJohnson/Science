#!/usr/bin/env python3
"""Actuator envelope of a racing-class quadrotor: thrust ceiling, torque ceiling at constant
altitude, the jerk ceiling set by the rotor-speed lag, the attitude-slew time, and the lap-time
penalty each of them costs.  All SI.

Owner calculation for the brief: "the acceleration and jerk ceiling set by rotor and motor
bandwidth, from the motor time constant and the thrust-coefficient curve, against the
thrust-to-weight ceiling."

Inputs (all from the dossier, cited in the printout):
  Sun2022 0.75 kg platform table (quadrotor.platform_sun2022; dossier A-01 class),
  motor thrust time constant 39.1 ms (A-03), rotor-speed time constant 33 ms (A-04),
  Swift mass 870 g with 35 N static thrust, T/W 4.10 (A-09),
  high-thrust mocap platform 0.52 kg / 63 N, T/W 12.35 (A-11).
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), ".claude", "skills", "conundrum", "scripts"))
import numpy as np
from quadrotor import Quadrotor, platform_sun2022

G = 9.80665

# --------------------------------------------------------------------------- platforms
sun = platform_sun2022()                                   # 0.75 kg, 8.5 N/rotor, tau = 39.1 ms
swift = sun.variant(mass=0.870, thrust_max=35.0 / 4.0, name="Swift-like(0.87kg,35N)")
hi = sun.variant(mass=0.520, thrust_max=63.0 / 4.0, inertia=(1.7e-3, 1.5e-3, 3.0e-3),
                 name="HiThrust-like(0.52kg,63N)")
plats = [sun, swift, hi]

print("=" * 78)
print("1. STATIC ENVELOPE (closed form, quadrotor.hover())")
print("=" * 78)
for p in plats:
    h = p.hover()
    print(f"{p.name:34s} m={p.mass:.3f} kg  T/W={h['thrust_to_weight']:.3f}  "
          f"a_horiz_max={h['a_max_horizontal']:.2f} m/s^2 ({h['a_max_horizontal']/G:.2f} g)  "
          f"tilt={h['tilt_for_max_horizontal_deg']:.1f} deg")
    print(f"{'':34s} a_up_max={h['a_max_vertical']:.2f}  a_down_max=-{G:.2f} m/s^2 "
          f"(thrust>=0 floor)  up/down asymmetry={h['a_max_vertical']/G:.2f}")
    print(f"{'':34s} hover throttle={100*h['throttle_fraction']:.1f} % of per-rotor max; "
          f"omega_hover={h['omega_hover']:.0f} rad/s of omega_max={p.omega_max:.0f}")

print()
print("=" * 78)
print("2. TORQUE CEILING vs COLLECTIVE THRUST (the unidirectional f_i >= 0 constraint)")
print("   Two rotors at f_lo, two at f_hi: T = 2(f_lo+f_hi), tau = lever*2(f_hi-f_lo),")
print("   0 <= f_lo, f_hi <= f_max  =>  tau_max(T) = lever * min(T, 4 f_max - T).")
print("   At hover collective T = m g this gives tau_max = lever * m g, INDEPENDENT of T/W;")
print("   the global maximum lever*T_max/2 sits at half throttle (and needs a climb).")
print("=" * 78)
for p in plats:
    h = p.hover()
    fh = h["thrust_per_rotor"]
    lever = p.arm_length * math.sin(math.radians(p.arm_angle_deg))
    W = p.mass * p.g
    tau_hover = lever * W
    a_hover = tau_hover / p.inertia[0]
    tau_peak = lever * 2.0 * p.thrust_max
    print(f"{p.name:34s} lever={lever:.4f} m  f_hover={fh:.3f} N  f_max={p.thrust_max:.3f} N  "
          f"W={W:.3f} N")
    print(f"{'':34s} tau_roll(T=mg)={tau_hover:.4f} N m -> alpha={a_hover:.1f} rad/s^2")
    print(f"{'':34s} tau_roll(T=2 f_max, half throttle)={tau_peak:.4f} N m -> "
          f"alpha={tau_peak/p.inertia[0]:.1f} rad/s^2  (ratio hover/peak {tau_hover/tau_peak:.3f})")
    print(f"{'':34s} cross-check vs hover()['torque_max_roll']={h['torque_max_roll']:.4f} N m "
          f"(= lever*2*(f_max-f_min), collective {2*p.thrust_max/W:.2f} m g)")
    for frac in (0.9, 1.0, 1.1):
        tq = frac * tau_hover
        ok = p.wrench_feasible(W, [tq, 0.0, 0.0])
        print(f"{'':34s} wrench_feasible(T=mg, tau_x={tq:.4f} N m) = {ok}")
    for mult in (0.5, 1.0, 1.5, 2.0, 3.0, 4.0):
        T = mult * W
        if T > 4 * p.thrust_max:
            continue
        tmax = lever * min(T, 4 * p.thrust_max - T)
        print(f"{'':34s} T={mult:.1f} m g: tau_max={tmax:.4f} N m, alpha={tmax/p.inertia[0]:6.1f} "
              f"rad/s^2, feasible={p.wrench_feasible(T, [0.999*tmax, 0, 0])}")

print()
print("=" * 78)
print("3. JERK CEILING FROM THE ROTOR-SPEED LAG (thrust coefficient f = k_f omega^2)")
print("   Full-throttle step from hover: domega/dt|_0 = (omega_max-omega_h)/tau,")
print("   dT/dt|_0 = 4 * 2 k_f omega_h (omega_max-omega_h)/tau,  j = (1/m) dT/dt.")
print("=" * 78)
taus = {"tau=39.1 ms (A-03, thrust)": 0.0391, "tau=33 ms (A-04, rotor speed)": 0.033,
        "tau=10 ms (5x faster, hypothetical)": 0.010}
for p in plats:
    h = p.hover()
    wh, wm = h["omega_hover"], p.omega_max
    for lbl, tau in taus.items():
        dTdt = 4.0 * 2.0 * p.k_thrust * wh * (wm - wh) / tau
        j = dTdt / p.mass
        # time for the collective thrust to reach 95 % of max under the lag
        # omega(t) = wm - (wm-wh) e^{-t/tau}; T = 4 k_f omega^2
        w_target = math.sqrt(0.95 * p.thrust_max / p.k_thrust)
        t95 = -tau * math.log((wm - w_target) / (wm - wh))
        print(f"{p.name:26s} {lbl:34s} j_z(0)={j:8.1f} m/s^3 ({j/G:6.1f} g/s)  "
              f"t_95%_thrust={1000*t95:5.1f} ms")
    print(f"{'':26s} a_horiz_max={h['a_max_horizontal']:.2f} m/s^2, so the time to build the "
          f"full envelope at j_z(0) is {1000*h['a_max_horizontal']/(4*2*p.k_thrust*wh*(wm-wh)/0.0391/p.mass):.0f} ms")

print()
print("=" * 78)
print("4. ATTITUDE SLEW: time to rotate the thrust vector by 152 deg (reversal of the")
print("   maximum-horizontal-acceleration tilt) under bang-bang roll torque, with and")
print("   without the rotor lag.  Full nonlinear plant, RK4, quaternion state.")
print("=" * 78)


def _roll_angle(q):
    w_, xq, yq, zq = q
    return math.atan2(2 * (yq * zq + w_ * xq), 1 - 2 * (xq * xq + yq * yq))


def slew_rest_to_rest(p, angle_rad, motor_tau, dt=5e-4, t_end=0.40, iters=20):
    """Rest-to-rest bang-bang roll through angle_rad at the constant-altitude torque ceiling.

    The switch time is found by bisection so that the roll RATE reaches zero exactly at
    angle_rad (that is what rest-to-rest means); the returned time is the first instant after
    the switch at which the rate is <= 0.  Full nonlinear plant, RK4, quaternion state.
    """
    pp = p.variant(motor_tau=motor_tau, enable_drag=False, enable_h_force=False)
    fh = pp.hover()["thrust_per_rotor"]
    f_hi = 2.0 * fh                     # f_lo = 0, so T = m g and tau = lever * m g
    up = np.sqrt(np.array([0.0, f_hi, f_hi, 0.0]) / pp.k_thrust)
    dn = np.sqrt(np.array([f_hi, 0.0, 0.0, f_hi]) / pp.k_thrust)
    x0 = pp.hover_state()

    def run(ts):
        u = lambda t, x: (up if t < ts else dn)
        out = pp.simulate(x0, u, dt=dt, t_end=t_end, renormalise=True)
        X, tt = out["x"], out["t"]
        rate = X[:, 10]
        # the roll angle must be UNWRAPPED: atan2 wraps at +-180 deg and a 152 deg slew with
        # overshoot crosses it, which would destroy the monotonicity the bisection needs.
        phi_u = np.unwrap(np.array([_roll_angle(q) for q in X[:, 3:7]]))
        i0 = int(math.ceil(ts / dt)) + 1
        idx = np.where(rate[i0:] <= 0.0)[0]
        if idx.size == 0:
            return float("nan"), float("nan"), float(np.max(rate))
        k = i0 + int(idx[0])
        return float(tt[k]), float(phi_u[k]), float(np.max(rate[:k + 1]))

    lo, hi_ = dt, 0.55 * t_end
    for _ in range(iters):
        mid = 0.5 * (lo + hi_)
        t, phi, pk = run(mid)
        # monotone in ts: a larger switch time means a larger angle at rest, and a switch time
        # so large that the rate never returns to zero inside t_end counts as "too large".
        if math.isfinite(phi) and phi < angle_rad:
            lo = mid
        else:
            hi_ = mid
    t, phi, pk = run(0.5 * (lo + hi_))
    return t, pk, phi


angle = math.radians(152.0)
for p in (swift, hi):
    rows = []
    for tau in (0.0, 0.010, 0.033, 0.0391, 0.060):
        t, pk, phif = slew_rest_to_rest(p, angle, tau)
        rows.append((tau, t, pk, phif))
        print(f"{p.name:30s} motor_tau={1000*tau:5.1f} ms -> rest-to-rest 152 deg in "
              f"{1000*t:6.1f} ms, peak rate {math.degrees(pk):7.0f} deg/s, "
              f"end angle {math.degrees(phif):.1f} deg")
    t0 = rows[0][1]
    t39 = [r[1] for r in rows if abs(r[0] - 0.0391) < 1e-9][0]
    print(f"{'':30s} lag share of the slew time: {1000*(t39-t0):.1f} ms of {1000*t39:.1f} ms "
          f"= {100*(t39-t0)/t39:.1f} %  (the rest is the torque ceiling)")
    tlo = slew_rest_to_rest(p, angle, 0.0391 / 1.2)[0]
    thi = slew_rest_to_rest(p, angle, 0.0391 * 1.2)[0]
    el = (math.log(thi) - math.log(tlo)) / (2 * math.log(1.2))
    print(f"{'':30s} d ln(t_slew)/d ln(motor_tau) = {el:+.3f}")
    # distance flown during one reversal at a representative course speed
    for v in (5.0, 10.0, 15.0, 20.0):
        print(f"{'':30s} at v={v:4.1f} m/s the 152 deg reversal costs {v*t39:5.2f} m of travel "
              f"with the thrust vector mis-aligned; a 40 ms sensorimotor latency costs "
              f"{v*0.040:4.2f} m")
    # effective jerk from rotating the thrust vector, vs the collective-thrust jerk ceiling
    a_h = p.hover()["a_max_horizontal"]
    print(f"{'':30s} thrust-vector rotation gives |da/dt| ~ a*omega = "
          f"{a_h*pk:.0f} m/s^3 at a={a_h:.1f} m/s^2, omega_peak={pk:.1f} rad/s; the collective "
          f"lag ceiling is j_z(0) above")

print()
print("=" * 78)
print("5. SEGMENT TIME WITH A FIRST-ORDER ACCELERATION LAG (1-D bang-bang)")
print("   a_cmd = +A up to t_s then -A; a follows da/dt = (a_cmd - a)/tau_a.")
print("   tau_a is the thrust lag alone (39.1 ms) or thrust lag + measured slew time.")
print("=" * 78)


def seg_time(dist, A, tau_a, dt=1e-4):
    """Rest-to-rest distance dist with a first-order acceleration lag.  Bisect on the switch
    time so that the vehicle is at rest exactly when it has covered dist.

    The lag is integrated exactly for a piecewise-constant command,
    a(t+dt) = a_cmd + (a - a_cmd) exp(-dt/tau_a), so the only discretisation error is in the
    trapezoid for v and x and in the resolution of the v = 0 crossing."""
    decay = math.exp(-dt / tau_a) if tau_a > 1e-12 else 0.0

    def run(ts):
        t = 0.0
        a = v = x = 0.0
        while t < 20.0:
            acmd = A if t < ts else -A
            a_new = acmd + (a - acmd) * decay
            x += dt * v + 0.5 * dt * dt * a
            v += 0.5 * dt * (a + a_new)
            a = a_new
            t += dt
            if t > ts and v <= 0.0:
                return t, x
        return float("nan"), float("nan")
    lo, hi_ = 1e-3, 10.0
    for _ in range(45):
        mid = 0.5 * (lo + hi_)
        t, x = run(mid)
        if x < dist:
            lo = mid
        else:
            hi_ = mid
    t, x = run(0.5 * (lo + hi_))
    return t, x


for p in (swift,):
    h = p.hover()
    A = h["a_max_horizontal"]
    print(f"platform {p.name}: A = a_horiz_max = {A:.2f} m/s^2")
    for dist in (5.0, 10.0, 20.0):
        t_ideal = 2.0 * math.sqrt(dist / A)
        for tau_a in (0.0391, 0.033, 0.010, 0.080):
            t, xf = seg_time(dist, A, tau_a)
            print(f"  d={dist:5.1f} m  tau_a={1000*tau_a:5.1f} ms: t={t:.4f} s "
                  f"(ideal bang-bang {t_ideal:.4f} s, penalty {1000*(t-t_ideal):5.1f} ms = "
                  f"{100*(t/t_ideal-1):4.1f} %), x_end={xf:.4f} m")
        # elasticity of segment time to tau_a at 39.1 ms
        t_lo, _ = seg_time(dist, A, 0.0391 / 1.2)
        t_hi, _ = seg_time(dist, A, 0.0391 * 1.2)
        el = (math.log(t_hi) - math.log(t_lo)) / (2 * math.log(1.2))
        # elasticity to A (thrust-to-weight route) at tau_a = 39.1 ms
        tA_lo, _ = seg_time(dist, A / 1.2, 0.0391)
        tA_hi, _ = seg_time(dist, A * 1.2, 0.0391)
        elA = (math.log(tA_hi) - math.log(tA_lo)) / (2 * math.log(1.2))
        print(f"  d={dist:5.1f} m  d ln(t_seg)/d ln(tau_a) = {el:+.4f}   "
              f"d ln(t_seg)/d ln(a_max) = {elA:+.4f}")

print()
print("=" * 78)
print("6. CONVERGENCE AND VERIFICATION")
print("=" * 78)
d = swift.variant(motor_tau=0.0391).diagnostics(dt=1e-3, t_end=2.0, rk4_dt=0.02)
for k, v in d.items():
    print(f"  integrator {k}: {v:.3e}" if isinstance(v, float) else f"  {k}: {v}")
# 1-D lag solver: dt vs dt/1.5 (and the tau -> 0 closed form)
for dtt in (1e-4, 1e-4 / 1.5, 1e-4 / 3.0):
    t, x = seg_time(10.0, swift.hover()["a_max_horizontal"], 0.0391, dt=dtt)
    print(f"  seg_time(10 m, tau=39.1 ms) at dt={dtt:.2e}: t={t:.6f} s, x_end={x:.6f} m")
t0, x0 = seg_time(10.0, swift.hover()["a_max_horizontal"], 0.0)
print(f"  seg_time with tau -> 0: t={t0:.6f} s vs closed form "
      f"2 sqrt(d/A) = {2*math.sqrt(10.0/swift.hover()['a_max_horizontal']):.6f} s")
# slew solver: dt vs dt/1.5
for dtt in (5e-4, 5e-4 / 1.5):
    t, pk, phif = slew_rest_to_rest(swift, angle, 0.0391, dt=dtt)
    print(f"  slew_rest_to_rest(152 deg, tau=39.1 ms) at dt={dtt:.2e}: t={1000*t:.3f} ms, "
          f"phi={math.degrees(phif):.3f} deg")
# closed-form cross-check of the torque-free slew with no lag
h = swift.hover()
lever = swift.arm_length * math.sin(math.radians(swift.arm_angle_deg))
dmax = min(h["thrust_per_rotor"], swift.thrust_max - h["thrust_per_rotor"])
alpha = lever * swift.mass * swift.g / swift.inertia[0]
t_cf = 2 * math.sqrt(angle / alpha)
print(f"  closed-form bang-bang slew (no lag, no gyroscopic coupling): alpha={alpha:.1f} "
      f"rad/s^2, t = 2 sqrt(theta/alpha) = {1000*t_cf:.1f} ms")
