#!/usr/bin/env python3
"""VERIFICATION of the simulator lens's plant, plus the time-optimal denominator.

Nothing in the lens's results is licensed unless this file prints PASS on every row.
Rows: a conserved quantity, two independent implementations, four known closed-form limits,
the integration error and its order, and the equilibrium the controller linearises about.

Then: the platform's time-optimal traversal time of the course (the denominator the whole
agility metric depends on), bracketed between a point-mass optimum and the best dynamically
feasible member of the reference family actually flown.

SI units throughout.  Seeds fixed.  Run:
  python3 .claude/skills/conundrum/scripts/math_run.py \
      runs/2026-10-15-quadrotor-agility-limit/calc/lens-simulator_verify.py
"""
import importlib.util
import math
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, ".claude", "skills", "conundrum", "scripts"))

import control_tools as ct                                            # noqa: E402
from quadrotor import platform_sun2022, quat_to_rot, euler_zyx_to_rot  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "simmodel", os.path.join(_HERE, "lens-simulator_model.py"))
M = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(M)

G = 9.80665
np.random.seed(0)

_rows = []


def row(name, method, got, expected, tol, note=""):
    ok = abs(got - expected) <= tol
    _rows.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    print(f"       method   : {method}")
    print(f"       got      : {got:.10g}")
    print(f"       expected : {expected:.10g}   (tol {tol:.3g})")
    if note:
        print(f"       note     : {note}")
    return ok


q = platform_sun2022()
course = M.Slalom()
print(M.model_card(q, course))
print()
print("=" * 78)
print("VERIFICATION TABLE")
print("=" * 78)

# ---------------------------------------------------------------- 1. conserved quantity
free = q.variant(enable_drag=False, enable_h_force=False, motor_tau=0.0)
x0 = free.hover_state(position=(0.0, 0.0, 50.0))
x0[7:10] = np.array([4.0, -3.0, 2.0])
x0[10:13] = np.array([3.0, -2.0, 1.5])
J = np.asarray(free.inertia, float)


def energy(x):
    v, om = x[7:10], x[10:13]
    return 0.5 * free.mass * float(v @ v) + 0.5 * float(om @ (J * om)) + free.mass * G * x[2]


for dtE in (1e-3, 5e-4):
    out = free.simulate(x0, np.zeros(4), dt=dtE, t_end=20.0)
    E = np.array([energy(r) for r in out["x"]])
    drift = float(np.max(np.abs(E - E[0])) / abs(E[0]))
    row(f"energy conservation (unforced, no drag, no thrust), dt={dtE*1e3:g} ms",
        "20 s RK4; E = 0.5 m|v|^2 + 0.5 om.J om + m g z", drift, 0.0, 1e-9,
        "ballistic + torque-free tumble: E is an exact invariant")

dg = free.diagnostics(dt=1e-3, t_end=2.0, rk4_dt=0.02)
row("angular momentum conservation (torque-free)",
    "quadrotor.diagnostics: max |J om|_world drift / |J om|_0 over 2 s",
    dg["angular_momentum_drift"], 0.0, 1e-9)
row("rotational kinetic energy (torque-free)",
    "quadrotor.diagnostics: max drift of 0.5 om.J om", dg["rotational_energy_drift"], 0.0, 1e-9)
row("quaternion norm", "max |‖q‖ - 1| over the 2 s tumble", dg["quat_norm_drift"], 0.0, 1e-12)

# ---------------------------------------------------------------- 2. independent implementations
# (a) quaternion 13-state dynamics vs the 12-state ZYX Euler dynamics, two separate code paths
phi, th, psi = 0.17, -0.23, 0.41
Rq = euler_zyx_to_rot(phi, th, psi)
cy, sy = math.cos(psi / 2), math.sin(psi / 2)
# build the quaternion from the same rotation matrix (Shepperd's method, w-dominant branch)
w = 0.5 * math.sqrt(max(1.0 + Rq[0, 0] + Rq[1, 1] + Rq[2, 2], 0.0))
qq = np.array([w, (Rq[2, 1] - Rq[1, 2]) / (4 * w), (Rq[0, 2] - Rq[2, 0]) / (4 * w),
               (Rq[1, 0] - Rq[0, 1]) / (4 * w)])
vw = np.array([7.0, -2.0, 1.0])
om = np.array([1.1, -0.7, 0.3])
Tc, tauc = 9.0, np.array([0.06, -0.04, 0.01])
u_rot = q.rotor_speeds_from_wrench(Tc, tauc)
qi = q.variant(motor_tau=0.0)
x13 = np.concatenate([np.zeros(3), qq, vw, om])
d13 = qi.dynamics(x13, u_rot)
x12 = np.concatenate([np.zeros(3), vw, [phi, th, psi], om])
d12 = qi.euler_dynamics(x12, u_rot, input_kind="rotor_speed")
row("independent implementation: vdot, quaternion path vs Euler path",
    "same physical state in two parameterisations and two code paths",
    float(np.max(np.abs(d13[7:10] - d12[3:6]))), 0.0, 1e-12)
row("independent implementation: omegadot, quaternion path vs Euler path",
    "same state, two code paths", float(np.max(np.abs(d13[10:13] - d12[9:12]))), 0.0, 1e-12)

# (b) analytic hover Jacobians vs control_tools.linearize central differences
lin = q.hover_linearization()
x0e, u0e = q.hover_equilibrium_euler("wrench")
A, B, info = ct.linearize(qi.euler_state_dynamics("wrench"), x0e, u0e)
row("independent implementation: hover A matrix, analytic vs numerical Jacobian",
    "quadrotor.hover_linearization vs control_tools.linearize",
    float(np.max(np.abs(A - lin["A"]))), 0.0, 1e-6)
row("independent implementation: hover B matrix, analytic vs numerical Jacobian",
    "quadrotor.hover_linearization vs control_tools.linearize",
    float(np.max(np.abs(B - lin["B"]))), 0.0, 1e-6)

# (c) rotor map round trip and the mixer's null direction
rt = q.wrench(u_rot)
row("rotor map round trip (thrust)", "wrench(rotor_speeds_from_wrench(T, tau))",
    rt["thrust"], Tc, 1e-9)
row("rotor map round trip (torque)", "same, max component error",
    float(np.max(np.abs(rt["torque"] - tauc))), 0.0, 1e-12)
Mmix = q.mix_matrix()
row("mixer null direction: equal thrust on all four rotors makes pure collective",
    "max |M @ [1,1,1,1]| over the three torque rows",
    float(np.max(np.abs((Mmix @ np.ones(4))[1:]))), 0.0, 1e-12,
    "this is what the torque-priority mixer relies on")

# ---------------------------------------------------------------- 3. known limits
row("known limit: free fall", "zero thrust from z=100 m for 1 s vs z0 - g t^2/2",
    dg["free_fall_error"], 0.0, 1e-9)

# small-angle hover: xddot = g theta
eps = 1e-5
x12p = np.zeros(12); x12p[7] = eps
d = qi.variant(enable_drag=False, enable_h_force=False).euler_dynamics(
    x12p, np.array([qi.mass * G, 0, 0, 0]), input_kind="wrench")
row("known limit: small-angle hover xddot = g*theta", f"theta = {eps} rad, drag off",
    d[3] / eps, G, 1e-4)

# thrust-to-weight horizontal acceleration ceiling, by simulation
hov = q.hover()
twr = hov["thrust_to_weight"]
a_h_closed = G * math.sqrt(twr ** 2 - 1.0)
tilt = math.acos(1.0 / twr)
qn = q.variant(enable_drag=False, enable_h_force=False, motor_tau=0.0)
# ZYX: Ry(+theta) has body x = (cos, 0, -sin) in world, i.e. NOSE DOWN, which is the
# direction that converts thrust into +x acceleration.
Rt = euler_zyx_to_rot(0.0, tilt, 0.0)
wq = 0.5 * math.sqrt(1.0 + Rt[0, 0] + Rt[1, 1] + Rt[2, 2])
qt = np.array([wq, (Rt[2, 1] - Rt[1, 2]) / (4 * wq), (Rt[0, 2] - Rt[2, 0]) / (4 * wq),
               (Rt[1, 0] - Rt[0, 1]) / (4 * wq)])
xt = np.concatenate([np.zeros(3), qt, np.zeros(3), np.zeros(3)])
dt_ = qn.dynamics(xt, np.full(4, qn.omega_max))
row("known limit: T/W horizontal acceleration ceiling",
    f"full throttle at tilt acos(1/(T/W)) = {math.degrees(tilt):.2f} deg, drag off; "
    "simulated a_x vs g sqrt((T/W)^2 - 1)", float(dt_[7]), a_h_closed, 1e-6,
    f"T/W = {twr:.4f}; a_z residual {dt_[9]:.2e} m/s^2")
row("known limit: that ceiling holds altitude", "a_z at the same state", float(dt_[9]), 0.0, 1e-9)

# motor_tau -> 0 reduces to instantaneous thrust
qa = q.variant(motor_tau=1e-6)
xa = np.concatenate([np.zeros(3), qq, vw, om, u_rot])
da = qa.dynamics(xa, u_rot)
row("known limit: motor_tau -> 0 equals instantaneous thrust",
    "17-state plant at rotor speeds = command vs 13-state plant, max |dv, dom| difference",
    float(np.max(np.abs(np.concatenate([da[7:13]]) - np.concatenate([d13[7:13]])))), 0.0, 1e-12)

# time-optimal solver against two closed forms
S, a_max_t = 100.0, 20.0
s_line = np.linspace(0.0, S, 200001)
v_line = M.time_optimal_on_path(s_line, np.zeros_like(s_line), a_max_t, np.inf, 0.0, 0.0)
row("known limit: time-optimal solver on a straight path (rest to rest)",
    f"S={S} m, a_max={a_max_t} m/s^2 vs t = 2 sqrt(S/a_max)",
    M.path_time(s_line, v_line), 2 * math.sqrt(S / a_max_t), 2e-3)
R_c = 25.0
s_circ = np.linspace(0.0, 2000.0, 200001)
v_circ = M.time_optimal_on_path(s_circ, np.full_like(s_circ, 1.0 / R_c), a_max_t, np.inf,
                                0.0, 0.0)
row("known limit: time-optimal solver on a circle (cruise speed)",
    f"kappa = 1/{R_c} 1/m, a_max={a_max_t}; max speed vs sqrt(a_max R)",
    float(np.max(v_circ)), math.sqrt(a_max_t * R_c), 1e-6)

# delay-margin tool against the closed form for L = wc/s
for wc in (10.0, 100.0):
    m_ = ct.loop_margins(lambda s, w=wc: w / s, w_min=1e-2, w_max=1e5)
    row(f"delay margin of L = {wc:g}/s", "control_tools.loop_margins vs pi/(2 wc)",
        m_["delay_margin"], math.pi / (2 * wc), 1e-9)

# ---------------------------------------------------------------- 4. integration error
row("RK4 convergence order", "Richardson self-convergence at base step 20 ms on the tumble",
    dg["rk4_order"], 4.0, 0.25)

# closed-loop step-size check on the load-bearing quantity (gate error at U = 12 m/s)
ctl = M.Cascade(q)
r1 = M.run_course(q, ctl, course, 12.0, dt=1e-3)
r2 = M.run_course(q, ctl, course, 12.0, dt=5e-4)
r3 = M.run_course(q, ctl, course, 12.0, dt=2e-3)
print(f"       closed-loop worst gate error at U=12 m/s: dt=2 ms {r3['worst_gate_err']:.6f} m, "
      f"dt=1 ms {r1['worst_gate_err']:.6f} m, dt=0.5 ms {r2['worst_gate_err']:.6f} m")
row("integration error, closed loop (1 ms vs 0.5 ms)",
    "worst gate error at U=12 m/s, relative difference",
    abs(r1["worst_gate_err"] - r2["worst_gate_err"]) / r2["worst_gate_err"], 0.0, 0.02,
    "dt = 1 ms is the step used for every headline number; 2 ms is used only in sweeps, "
    f"where its error is {abs(r3['worst_gate_err']-r2['worst_gate_err'])/r2['worst_gate_err']:.4f}")

# ---------------------------------------------------------------- 5. the equilibrium
row("linearisation equilibrium residual |f(x0, u0)| at hover",
    "control_tools.linearize residual, 12-state Euler form, wrench input",
    info["residual"], 0.0, 1e-12,
    f"step_sensitivity {info['step_sensitivity']:.2e}; unstable modes {info['unstable_modes']}")
ctrb = ct.controllability(A, B)
print(f"       controllability: rank {ctrb['rank']}/12, keys {sorted(ctrb.keys())}")

print()
print(f"VERIFICATION: {sum(_rows)}/{len(_rows)} rows PASS")
assert all(_rows), "verification failed - no result in this lens is licensed"

# ================================================================ the denominator
print()
print("=" * 78)
print("THE PLATFORM'S TIME-OPTIMAL TRAVERSAL TIME (the agility metric's denominator)")
print("=" * 78)
a_h = hov["a_max_horizontal"]
v_cap = M.level_flight_v_max(q)
print(f"  isotropic horizontal acceleration ceiling a_h = g sqrt((T/W)^2 - 1) = {a_h:.3f} m/s^2")
print(f"  drag-limited steady level-flight top speed v_cap = {v_cap:.3f} m/s "
      f"(solved from the plant's own thrust limit and kd, kh)")
for v_use, lab in ((v_cap, "with the plant's drag-limited speed cap"),
                   (np.inf, "with no speed cap (pure point mass)")):
    to = M.time_optimal_path_time(course, a_h, v_use)
    print(f"  point-mass time-optimal, {lab}:")
    print(f"      t_opt = {to['t_opt']:.4f} s over {to['s_timed']:.3f} m of path, "
          f"mean path speed {to['v_mean']:.3f} m/s, "
          f"v in [{to['v_min']:.2f}, {to['v_max']:.2f}] m/s")
to = M.time_optimal_path_time(course, a_h, v_cap)
U_feas = course.ref_feasible_U(a_h)
t_ref = course.x_end / U_feas
print(f"  best dynamically feasible member of the reference family (constant x-rate):")
print(f"      U_feas = {U_feas:.4f} m/s (peak reference |a| = a_h exactly), "
      f"t = {t_ref:.4f} s, mean path speed {course.arclength()/t_ref:.3f} m/s")
print(f"      this family is {100*(t_ref/to['t_opt'] - 1):.2f} per cent slower than the "
      f"point-mass optimum -> the reference family costs that much of the denominator")
print(f"  DENOMINATOR USED BELOW: t_opt = {to['t_opt']:.4f} s "
      f"(mean path speed {to['v_mean']:.3f} m/s)")
print("  caveat: this is a point-mass optimum on a FIXED path with an isotropic horizontal")
print("  acceleration bound, so it is a LOWER bound on the true platform optimum (the true")
print("  optimum must also respect rotation time, per-rotor limits and motor lag; the")
print("  published full-model penalty for exactly this is 2.00-2.68 per cent, dossier A-17).")

# how much thrust margin is left at the feasible reference speed
print()
print("  control margin along the reference (what is left for feedback):")
for U in (8.0, 12.0, 15.0, 18.0, U_feas):
    a_pk = course.ref_peak_accel(U)
    print(f"      U = {U:6.3f} m/s: peak reference lateral |a| = {a_pk:7.3f} m/s^2 = "
          f"{100*a_pk/a_h:5.1f} per cent of a_h; "
          f"margin for feedback = {a_h - a_pk:7.3f} m/s^2")
