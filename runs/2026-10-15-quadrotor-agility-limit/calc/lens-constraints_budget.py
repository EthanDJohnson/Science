#!/usr/bin/env python3
"""Three remaining constraint classes for an onboard-only racing quadrotor, with their
elasticities: (1) the model-error budget against gate clearance as a function of speed,
(2) the look-ahead bound with the thrust-vector REORIENTATION time included in the effective
latency, (3) power and energy (momentum theory + battery C-rate), and (4) one elasticity table.

All SI.  Inputs are the dossier's anchors, cited inline.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), ".claude", "skills", "conundrum", "scripts"))
import numpy as np
from quadrotor import platform_sun2022

G = 9.80665
RHO = 1.225          # kg/m^3, ISA sea level
sun = platform_sun2022()
swift = sun.variant(mass=0.870, thrust_max=35.0 / 4.0, name="Swift-like(0.87kg,35N)")
h = swift.hover()
a_h = h["a_max_horizontal"]
lever = swift.arm_length * math.sin(math.radians(swift.arm_angle_deg))
alpha_const_alt = lever * swift.mass * swift.g / swift.inertia[0]

print("=" * 78)
print("1. MODEL-ERROR BUDGET vs SPEED (A-18 replayed-flight positional RMSE, power-law fit)")
print("=" * 78)
# A-18: mean speed of the flight, positional RMSE of the model when the flight is replayed
v_dat = np.array([1.67, 2.38, 3.21, 6.92])
e_fit = np.array([0.061, 0.167, 0.183, 0.381])      # "Fit" (polynomial/least-squares) model
e_bem = np.array([0.059, 0.138, 0.146, 0.232])      # blade-element-momentum model
for name, e in (("Fit", e_fit), ("BEM", e_bem)):
    k, lc = np.polyfit(np.log(v_dat), np.log(e), 1)
    c = math.exp(lc)
    pred = c * v_dat ** k
    r2 = 1 - np.sum((np.log(e) - np.log(pred)) ** 2) / np.sum((np.log(e) - np.mean(np.log(e))) ** 2)
    print(f"  {name}: e_model(v) = {c:.4f} * v^{k:.3f} m  (log-log R^2 = {r2:.3f}); "
          f"residuals {np.round(e - pred, 4)}")
    for e_est, lbl in ((0.151, "T265 VIO 0.151 m (circle, <=7 m/s)"),
                       (0.114, "T265 VIO 0.114 m (lemniscate)"),
                       (0.30, "0.30 m onboard-VIO at racing speed (assumed)")):
        budget = 0.60 - e_est
        if budget <= 0:
            print(f"    e_est={e_est}: no budget left")
            continue
        v_star = (budget / c) ** (1.0 / k)
        # elasticity of v_star to the clearance and to the model coefficient
        el_clear = (1.0 / k) * (0.60 / budget)
        print(f"    with e_est = {e_est:.3f} m ({lbl}): model error fills the remaining "
              f"{budget:.3f} m at v = {v_star:5.2f} m/s; d ln v*/d ln(clearance) = {el_clear:+.2f}, "
              f"d ln v*/d ln(model error) = {-1.0/k:+.2f}")
    # what a 50 per cent force-error cut (D-08, BEM+NN) buys
    v_half = (0.449 / (0.5 * c)) ** (1.0 / k)
    v_base = (0.449 / c) ** (1.0 / k)
    print(f"    halving the model error (D-08 claims ~50 % force-error cut) moves v* from "
          f"{v_base:.2f} to {v_half:.2f} m/s (+{100*(v_half/v_base-1):.0f} %)")
print("  CAVEAT: A-18 is OPEN-LOOP replay prediction error over whole flights, so it is an upper")
print("  bound on the closed-loop consequence (F9 puts the feedback-rejected residual at ~1 mm);")
print("  it is the error a planner or a learned policy inherits through its model, not a measured")
print("  tracking error. The measured closed-loop tracking RMSE on the same platform class is")
print("  0.322 m at up to 16.7 m/s and 4 g with mocap state (A-06).")

print()
print("=" * 78)
print("2. LOOK-AHEAD BOUND WITH THE REORIENTATION TIME IN THE LATENCY")
print("   v tau_tot + v^2/(2 a) <= s,  tau_tot = tau_sense + t_reorient,")
print("   t_reorient = 2 sqrt(theta/alpha) for a rest-to-rest tilt to the braking attitude.")
print("=" * 78)
theta_brake = math.radians(90.0 - 0.0)     # from level to thrust-backwards for max deceleration
t_re_90 = 2 * math.sqrt(math.radians(90.0) / alpha_const_alt)
t_re_76 = 2 * math.sqrt(math.radians(75.9) / alpha_const_alt)
print(f"  alpha(const. altitude) = {alpha_const_alt:.1f} rad/s^2 -> rest-to-rest reorientation "
      f"76 deg in {1000*t_re_76:.0f} ms, 90 deg in {1000*t_re_90:.0f} ms "
      f"(the full-plant simulation with the 39.1 ms lag gave 201 ms for 152 deg)")


def v_stop(s, a, tau):
    return a * (-tau + math.sqrt(tau * tau + 2 * s / a))


def elasticity(fn, x, rel=1e-3):
    return (math.log(fn(x * (1 + rel))) - math.log(fn(x * (1 - rel)))) / (2 * math.log((1 + rel) / (1 - rel)) / 2)


for s, s_lbl in ((6.0, "6 m (A-21/A-33 pole experiment)"), (10.0, "10 m (depth-camera class)"),
                 (20.0, "20 m (LiDAR class, D-39)")):
    for tau_s, lbl in ((0.040, "sense 40 ms only [A-07]"),
                       (0.040 + t_re_76, "sense 40 ms + 76 deg reorientation"),
                       (0.017, "sense 17 ms only [A-28]"),
                       (0.017 + t_re_76, "sense 17 ms + 76 deg reorientation")):
        v = v_stop(s, a_h, tau_s)
        e_tau = elasticity(lambda t: v_stop(s, a_h, t), tau_s)
        e_s = elasticity(lambda x: v_stop(x, a_h, tau_s), s)
        e_a = elasticity(lambda x: v_stop(s, x, tau_s), a_h)
        print(f"  s={s:5.1f} m {s_lbl:32s} {lbl:40s} tau_tot={1000*tau_s:6.1f} ms -> "
              f"v_max={v:6.2f} m/s; e_tau={e_tau:+.3f}, e_s={e_s:+.3f}, e_a={e_a:+.3f}")
# the speed at which the two terms are equal, and the required range at a target speed
for v_t in (5.0, 10.0, 15.0, 20.0):
    tau_tot = 0.040 + t_re_76
    s_req = v_t * tau_tot + v_t ** 2 / (2 * a_h)
    print(f"  to run at {v_t:4.1f} m/s you must see {s_req:5.2f} m ahead "
          f"({100*v_t*tau_tot/s_req:4.1f} % of it is the reaction term, "
          f"{100*(v_t**2/(2*a_h))/s_req:4.1f} % braking)")

print()
print("=" * 78)
print("3. POWER AND ENERGY: momentum theory, figure of merit, battery C-rate")
print("   P_ideal = T^(3/2) / sqrt(2 rho A) per rotor (hover induced power, no forward speed)")
print("=" * 78)
D = 5.0 * 0.0254          # 5-inch propeller
A_disk = math.pi * (D / 2) ** 2
for lbl, T_tot in (("hover", swift.mass * G), ("half throttle", 0.5 * 4 * swift.thrust_max),
                   ("full throttle", 4 * swift.thrust_max)):
    T_r = T_tot / 4.0
    P_id = 4.0 * T_r ** 1.5 / math.sqrt(2 * RHO * A_disk)
    for fm in (0.65, 0.75):
        P_el = P_id / fm
        for V, Ah in ((14.8, 1.8), (22.2, 1.3)):
            I = P_el / V
            print(f"  {lbl:14s} T={T_tot:5.2f} N  P_ideal={P_id:7.1f} W  FoM={fm:.2f} -> "
                  f"P_elec={P_el:7.1f} W; on {V:.1f} V {Ah:.1f} Ah: I={I:6.1f} A = "
                  f"{I/Ah:5.1f} C, pack energy {V*Ah:.1f} Wh, endurance at this power "
                  f"{60*V*Ah/P_el:5.2f} min")
    print()
# energy for one 75 m lap at 15 m/s mean, vs the pack
for v_lap in (10.0, 15.0, 20.0):
    t_lap = 75.0 / v_lap
    P_el = (4.0 * (0.5 * 4 * swift.thrust_max / 4) ** 1.5 / math.sqrt(2 * RHO * A_disk)) / 0.70
    E = P_el * t_lap / 3600.0
    print(f"  a 75 m lap [A-10] at {v_lap:4.1f} m/s takes {t_lap:4.2f} s; at the half-throttle "
          f"power {P_el:.0f} W it costs {E:.3f} Wh of a 26.6 Wh 4S pack = {100*E/26.64:.1f} %")
print("  reading: ENERGY is not the binding constraint (a lap costs a few per cent of the pack);")
print("  the constraint on this axis is PEAK CURRENT and the voltage sag it causes, which the")
print("  literature names as a failure cause (D-14) rather than endurance.")

print()
print("=" * 78)
print("4. ELASTICITY TABLE (per cent change in the agility metric per per cent change in the")
print("   limit), each from the calculation named")
print("=" * 78)
rows = [
    ("perception range s (stop bound, unseen course)", "+0.50 to +0.53", "this script, part 2"),
    ("perception range s (lateral-dodge bound)", "+1.00 exactly", "dossier A-33/D-31"),
    ("thrust-to-weight T/W (via a_max)", "+0.48 to +0.53", "actuator script part 5; A-16 gives -0.565 on lap time"),
    ("model (aero) error coefficient", f"{-1.0/np.polyfit(np.log(v_dat), np.log(e_bem), 1)[0]:+.2f}",
     "this script, part 1 (BEM power law)"),
    ("sensing latency tau_sense (stop bound, with reorientation)", "-0.04 to -0.19", "this script, part 2"),
    ("motor time constant (segment time)", "-0.040", "actuator script part 5"),
    ("motor time constant (slew time)", "-0.177", "actuator script part 4"),
    ("motor time constant (rate-loop bandwidth)", "-1.000", "loop script part 4"),
    ("tau_eff (feedback-only speed ceiling)", "-1.000", "loop script part 5"),
    ("tau_eff (feedforward residual error)", "+2.000", "loop script part 5"),
]
for name, el, src in rows:
    print(f"  {name:58s} {el:>16s}   [{src}]")
print()
print("  CONVERGENCE/VERIFICATION of this script:")
for n in (1000, 1500):
    xs = np.linspace(0.0, 1.0, n)
    # integrate the stop bound by quadrature as a cross-check: distance to stop from v with
    # latency tau is v*tau + int_0^v (u/a) du = v*tau + v^2/(2a)
    v0 = 15.0
    d_quad = v0 * (0.040 + t_re_76) + np.trapezoid(xs * v0 / a_h, xs * v0) if hasattr(np, "trapezoid") \
        else v0 * (0.040 + t_re_76) + np.trapz(xs * v0 / a_h, xs * v0)
    d_cf = v0 * (0.040 + t_re_76) + v0 ** 2 / (2 * a_h)
    print(f"    n={n}: quadrature {d_quad:.6f} m vs closed form {d_cf:.6f} m "
          f"(diff {abs(d_quad-d_cf):.2e})")
print(f"    v_stop inverse check: v_stop(s=10, a={a_h:.3f}, tau=0.156) = "
      f"{v_stop(10.0, a_h, 0.156):.6f} m/s; substituting back gives s = "
      f"{v_stop(10.0, a_h, 0.156)*0.156 + v_stop(10.0, a_h, 0.156)**2/(2*a_h):.6f} m")
print(f"    reorientation closed form vs the actuator script's full-plant 152 deg slew: "
      f"2 sqrt(152 deg/alpha) = {2*math.sqrt(math.radians(152)/alpha_const_alt)*1000:.1f} ms "
      f"(no lag) against 164.0 ms simulated (no lag) and 201.0 ms with the 39.1 ms lag")
