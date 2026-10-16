#!/usr/bin/env python3
"""Loop-side audit of a racing-class quadrotor: controllability and underactuation, the weak
direction's cost, transmission zeros (is the position loop minimum-phase?), LQR margins, the
delay-limited bandwidth of the rate loop with the motor lag in it, and the speed that a
feedback-only architecture permits against the speed a feedforward architecture permits.

All SI, radians, seconds; frequencies in rad/s with Hz alongside.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), ".claude", "skills", "conundrum", "scripts"))
import numpy as np
from quadrotor import platform_sun2022
from control_tools import linearize, controllability, lqr, state_feedback_margins, loop_margins

sun = platform_sun2022()
swift = sun.variant(mass=0.870, thrust_max=35.0 / 4.0, name="Swift-like(0.87kg,35N)")
G = 9.80665

print("=" * 78)
print("1. UNDERACTUATION AND CONTROLLABILITY AT HOVER (12-state Euler form, wrench input)")
print("=" * 78)
f = swift.euler_state_dynamics("wrench")
x0, u0 = swift.hover_equilibrium_euler("wrench")
res = f(x0, u0)
print(f"  equilibrium residual |f(x0,u0)| = {np.linalg.norm(res):.3e} (must be ~0 for a true"
      " equilibrium)")
A, B, info = linearize(f, x0, u0)
print(f"  linearize step study: {info}")
print(f"  states n = {A.shape[0]} (6 DOF x 2), inputs m = {B.shape[1]} "
      f"(T, tau_x, tau_y, tau_z) -> underactuated by {6 - B.shape[1]} DOF in the 6-DOF sense")
for drag in (True, False):
    sw = swift.variant(enable_drag=drag, enable_h_force=drag)
    Ad, Bd, _ = linearize(sw.euler_state_dynamics("wrench"), *sw.hover_equilibrium_euler("wrench"))
    c = controllability(Ad, Bd)
    print(f"  drag={drag}: Kalman rank {c['rank']}/{Ad.shape[0]}, controllable={c['controllable']}, "
          f"sigma_min(C) = {c['min_singular_value']:.3e}, condition = {c['condition']:.3e}"
          )
# the same in units that make the comparison meaningful: scale states by a tolerance
# (Bryson): 0.5 m position, 5 m/s velocity, 0.2 rad attitude, 10 rad/s rate; inputs by
# (m g, lever*m g, lever*m g, k_m/k_f * m g)
lever = swift.arm_length * math.sin(math.radians(swift.arm_angle_deg))
W = swift.mass * swift.g
Sx = np.diag([0.5, 0.5, 0.5, 5.0, 5.0, 5.0, 0.2, 0.2, 0.2, 10.0, 10.0, 10.0])
Su = np.diag([W, lever * W, lever * W, (swift.k_torque / swift.k_thrust) * W])
An = np.linalg.inv(Sx) @ A @ Sx
Bn = np.linalg.inv(Sx) @ B @ Su
cn = controllability(An, Bn)
print(f"  scaled (tolerance units): sigma_min = {cn['min_singular_value']:.4f}, "
      f"condition = {cn['condition']:.3e}")
u_, s_, vt_ = np.linalg.svd(np.hstack([np.linalg.matrix_power(An, k) @ Bn for k in range(12)]))
print(f"  weakest left-singular direction of the scaled controllability matrix (states "
      f"p,v,eul,omega):\n    {np.round(u_[:, -1], 3)}")
print("  reading: Kalman rank is full (12), so no mode is uncontrollable and Brockett's")
print("  condition is NOT an obstruction: a smooth time-invariant stabilising feedback exists at")
print("  hover. The vehicle is underactuated (4 inputs, 6 DOF) but not nonholonomic in that")
print("  sense. sigma_min in tolerance units is order 1, i.e. no direction is effort-starved;")
print("  the weak direction identified depends on the tolerance scaling, so the substantive")
print("  result is the rank and the order-1 sigma_min, not which axis comes out weakest.")

print()
print("=" * 78)
print("2. TRANSMISSION ZEROS: is the lateral position loop minimum-phase? (tests [D-28])")
print("=" * 78)
try:
    from scipy.signal import ss2tf
    for drag in (False, True):
        sw = swift.variant(enable_drag=drag, enable_h_force=drag)
        Ad, Bd, _ = linearize(sw.euler_state_dynamics("wrench"),
                              *sw.hover_equilibrium_euler("wrench"))
        # input 1 = tau_x (roll torque) -> output y (state index 1)
        C = np.zeros((1, 12)); C[0, 1] = 1.0
        num, den = ss2tf(Ad, Bd[:, [1]], C, np.zeros((1, 1)))
        # drop leading coefficients that are numerical noise: ss2tf leaves O(1e-13) leading
        # terms that np.roots turns into spurious zeros at 1e6
        nz = np.asarray(num[0], dtype=float)
        keep = np.abs(nz) > 1e-9 * np.max(np.abs(nz))
        first = int(np.argmax(keep))
        nz = nz[first:]
        z = np.roots(nz) if nz.size > 1 else np.array([])
        p = np.roots(den)
        print(f"  drag={drag}: tau_x -> y  zeros = {np.round(z, 4) if z.size else 'none'}")
        print(f"             poles (12) = {np.round(np.sort_complex(p), 4)}")
        print(f"             RHP zeros: {int(np.sum(np.real(z) > 1e-9))}, "
              f"RHP poles: {int(np.sum(np.real(p) > 1e-9))}")
except Exception as exc:  # pragma: no cover
    print(f"  scipy unavailable or ss2tf failed: {exc}")

print()
print("=" * 78)
print("3. LQR ON THE LATERAL CHAIN (y, vy, phi, p) <- tau_x: THE DELAY MARGIN OF THE")
print("   UNDERACTUATED DIRECTION, against the measured latency budget")
print("=" * 78)
idx = [1, 4, 6, 9]                      # y, vy, phi, omega_x in the 12-state layout
A4 = A[np.ix_(idx, idx)]
B4 = B[np.ix_(idx, [1])]
print("  A4 =\n" + str(np.round(A4, 4)))
print(f"  B4^T = {np.round(B4.ravel(), 2)}  (1/Jx = {1/swift.inertia[0]:.1f})")
Sx4 = np.diag([0.5, 5.0, 0.2, 10.0])
Su4 = np.array([[lever * W]])
Q4 = np.linalg.inv(Sx4) @ np.linalg.inv(Sx4)
print(f"  Bryson weights: tolerances y 0.5 m, vy 5 m/s, phi 0.2 rad, p 10 rad/s; "
      f"tau_x {lever*W:.3f} N m (= the constant-altitude ceiling)")
rows = []
for rscale in (1e5, 1e4, 1e3, 1e2, 1e1, 1.0, 1e-2, 1e-4):
    R4 = rscale * (np.linalg.inv(Su4) @ np.linalg.inv(Su4))
    out = lqr(A4, B4, Q4, R4)
    K4 = out["K"]
    m = state_feedback_margins(A4, B4, K4)
    bw = float(np.max(np.abs(out["closed_loop_poles"])))
    rows.append((rscale, bw, m))
    print(f"  R scale {rscale:7.0e}: closed-loop |pole|max {bw:7.2f} rad/s, PM "
          f"{m['phase_margin_deg']:5.1f} deg, GM {m['gain_margin']:.3g}, crossover "
          f"{m['w_gain_crossover']:7.2f} rad/s, DELAY MARGIN {1e3*m['delay_margin']:7.2f} ms")
print("  latency budget to fit inside the delay margin (the sum of [D-26]):")
for lbl, parts in [("Swift onboard, position loop", {"camera+VIO+policy (A-07/A-08)": 0.040,
                                                     "ZOH at 100 Hz / 2": 0.005,
                                                     "motor lag (A-03)": 0.0391}),
                   ("MonoRace-class", {"image delay (A-28)": 0.017,
                                       "ZOH at 500 Hz / 2": 0.001,
                                       "motor lag (A-03)": 0.0391}),
                   ("AlphaPilot 2019", {"camera+VIO chain (A-22)": 0.130,
                                        "ZOH at 50 Hz / 2": 0.010,
                                        "motor lag (A-03)": 0.0391})]:
    tot = sum(parts.values())
    print(f"    {lbl:28s} tau_eff = {1e3*tot:6.1f} ms  = " +
          " + ".join(f"{1e3*v:.1f} ({k})" for k, v in parts.items()))
    ok = [r for r in rows if r[2]["delay_margin"] > tot]
    if ok:
        best = max(ok, key=lambda r: r[1])
        print(f"      -> largest closed-loop bandwidth whose delay margin still covers it: "
              f"{best[1]:.2f} rad/s ({best[1]/2/math.pi:.2f} Hz) at R scale {best[0]:.0e}")
    else:
        print("      -> no sampled design has a delay margin that covers this budget")
print("  (LQR state feedback has >= 60 deg phase margin at the plant input of the exact model:")
print("   Safonov & Athans 1977. The delay margin is the quantity the latency budget must fit.)")

print()
print("=" * 78)
print("4. RATE-LOOP BANDWIDTH WITH THE MOTOR LAG AND A TRANSPORT DELAY")
print("   L(s) = k/(J s) * 1/(1 + tau_m s) * exp(-theta s);  k chosen for PM = 45 deg.")
print("=" * 78)
Jx = swift.inertia[0]


def rate_loop_crossover(tau_m, theta, pm_target_deg=45.0):
    """Largest gain crossover with the target phase margin, closed form + bisection."""
    pm = math.radians(pm_target_deg)
    # phase of L at w: -90deg - atan(w tau_m) - w theta; set = -(180 - PM)
    def phase_excess(w):
        ph = -math.pi / 2 - math.atan(w * tau_m) - w * theta
        return ph + (math.pi - pm)          # zero at the crossover we want
    lo, hi = 1e-4, 1e5
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if phase_excess(mid) > 0:
            lo = mid
        else:
            hi = mid
    wc = 0.5 * (lo + hi)
    k = Jx * wc * math.sqrt(1 + (wc * tau_m) ** 2)      # |L(jwc)| = 1
    return wc, k


print(f"  Jx = {Jx:.2e} kg m^2")
cases = [("no lag, no delay", 0.0, 0.0),
         ("motor lag 39.1 ms only [A-03]", 0.0391, 0.0),
         ("motor lag 33 ms only [A-04]", 0.033, 0.0),
         ("motor lag 10 ms only", 0.010, 0.0),
         ("lag 39.1 ms + 2 ms (1 kHz IMU + 500 Hz ZOH/2 + compute)", 0.0391, 0.002),
         ("lag 39.1 ms + 5 ms", 0.0391, 0.005),
         ("lag 10 ms + 2 ms", 0.010, 0.002)]
for lbl, tm, th in cases:
    wc, k = rate_loop_crossover(tm, th)
    # verify with the generic tool on the same loop
    L = (lambda s, _k=k, _tm=tm, _th=th: _k / (Jx * s) / (1 + _tm * s) * np.exp(-_th * s))
    mg = loop_margins(L)
    print(f"  {lbl:54s} wc = {wc:8.2f} rad/s ({wc/2/math.pi:6.2f} Hz), k = {k:.4f} N m/(rad/s); "
          f"tool: wc {mg['w_gain_crossover']:8.2f}, PM {mg['phase_margin_deg']:5.1f} deg, "
          f"delay margin {1e3*mg['delay_margin']:6.2f} ms")
wc0, _ = rate_loop_crossover(0.0391, 0.0)
wc1, _ = rate_loop_crossover(0.0391 * 1.2, 0.0)
wc2, _ = rate_loop_crossover(0.0391 / 1.2, 0.0)
print(f"  d ln(wc_rate)/d ln(tau_motor) = {(math.log(wc1)-math.log(wc2))/(2*math.log(1.2)):+.3f} "
      f"(pure delay would give exactly -1; a first-order lag gives the same -1 here)")

print()
print("=" * 78)
print("5. WHAT BANDWIDTH DOES THE TASK NEED? FEEDBACK-ONLY vs FEEDFORWARD + FEEDBACK")
print("   Feedback-only: a circular turn of radius Rc at speed v is a reference at")
print("   omega = v/Rc with amplitude Rc; for L = wc/s the tracking error is")
print("   e = |S(j omega)| Rc = Rc omega/sqrt(omega^2+wc^2) -> v/wc for omega << wc.")
print("   Feedforward (differential flatness, [D-01]): the reference is supplied open loop and")
print("   the loop only rejects the model-error disturbance a_d, giving e ~ a_d/wc^2.")
print("=" * 78)
e_allow = 0.60      # m: 1.5 m gate opening (A-26) -> 0.75 m half-width, minus a 0.15 m vehicle radius
a_d = 0.40 / swift.mass   # m/s^2 from a 0.40 N unmodelled force (A-18 force RMSE 0.352-0.365 N)
print(f"  e_allow = {e_allow} m (1.5 m gate [A-26] half-width minus 0.15 m vehicle radius)")
print(f"  a_d = {a_d:.3f} m/s^2 (0.40 N unmodelled aerodynamic force on {swift.mass} kg [A-18])")
for tau_eff, lbl in [(0.040, "40 ms sensorimotor latency [A-07]"),
                     (0.0175, "17.5 ms (MonoRace image 17 ms + IMU 0.5 ms) [A-28]"),
                     (0.130, "130 ms (AlphaPilot 2019) [A-22]"),
                     (0.005, "5 ms (event camera + 1 kHz estimator) [A-23/A-24]")]:
    for pm_deg in (45.0, 60.0):
        wc = (math.pi / 2 - math.radians(pm_deg)) / tau_eff
        v_fb = e_allow * wc
        e_ff = a_d / wc ** 2
        print(f"  {lbl:46s} PM {pm_deg:.0f} deg: wc <= {wc:7.2f} rad/s "
              f"({wc/2/math.pi:5.2f} Hz) -> feedback-only v_max = {v_fb:6.2f} m/s; "
              f"feedforward residual error = {1e3*e_ff:7.3f} mm")
wc_req = math.sqrt(a_d / e_allow)
print(f"  Bandwidth actually required to hold the model-error disturbance inside e_allow: "
      f"wc >= sqrt(a_d/e_allow) = {wc_req:.3f} rad/s ({wc_req/2/math.pi:.3f} Hz), which a pure"
      f" delay of up to {1e3*(math.pi/2-math.radians(45))/wc_req:.0f} ms still permits at PM 45 deg")
print(f"  margin factor on the measured 40 ms budget: {((math.pi/2-math.radians(45))/wc_req)/0.040:.1f}x")
print("  elasticity of the feedback-only speed ceiling to tau_eff = -1 exactly (v = e wc, "
      "wc ~ 1/tau_eff); of the feedforward residual error to tau_eff = +2.")

print()
print("=" * 78)
print("6. ESTIMATION ERROR IS NOT REJECTED BY THE LOOP: the error budget")
print("   e_allow >= e_estimate + e_feedforward_model + e_feedback_residual")
print("=" * 78)
for e_est in (0.05, 0.114, 0.151, 0.30, 0.50):
    for e_model in (0.049, 0.146, 0.232, 0.381):
        left = e_allow - e_est - e_model
        flag = "OK" if left > 0 else "INFEASIBLE"
        print(f"  e_est={e_est:.3f} m, e_model={e_model:.3f} m -> slack {left:+.3f} m  {flag}")
print("  (e_est values: T265 VIO 0.114-0.151 m at <=7 m/s, section 7 of the dossier; e_model")
print("   values: A-18 positional RMSE 0.049 m at 1.67 m/s to 0.381 m at 6.92 m/s mean speed.)")
