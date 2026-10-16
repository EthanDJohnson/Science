#!/usr/bin/env python3
"""M-MECH-04  Blind time of the braking reorientation, with and without the motor lag.

CLAIM (mechanist finding 4, candidate MECH-D)
  Symbols, SI: J_y = 2.1e-3 kg m^2 pitch inertia; l = 0.14 m arm, beta = 56 deg arm angle,
  f_max = 8.5 N per-rotor thrust limit, k_f = 1.51e-6 N s^2/rad^2 (Sun et al. TABLE II);
  tau_max = pitch torque with the rear pair at f_max and the front pair at 0;
  alpha_max = tau_max/J_y; theta_t = atan(a_h/g) = 77.5 deg the full-brake tilt;
  motor_tau = 39.1 ms, a first-order lag on ROTOR SPEED (thrust goes as omega^2).
  Claimed: tau_max = 1.331 N m, alpha_max = 634 rad/s^2; a rest-to-rest bang-bang rotation to
  theta_t takes 91.6 ms with no motor lag and 95.6 ms with the 39.1 ms lag, so the motor
  constant costs 3-9 ms while rotational inertia costs ~90 ms; and, counting half the rotation
  as latency, d ln v/d ln motor_tau ~ -0.02 (a 10 per cent faster motor buys 0.1-0.2 per cent
  speed).
  Checked: the torque and alpha arithmetic; the ideal time against 2 sqrt(theta/alpha); the
  lagged time by direct integration of the rotor-speed lag with quadratic thrust (and, as a
  cross-check, of a first-order lag on the torque itself); the lag -> 0 limit; the elasticity.
"""
import math
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, quantity, units  # noqa: E402

G = 9.81
M, L, BETA, JY = 0.75, 0.14, math.radians(56.0), 2.1e-3
FMAX, KF = 8.5, 1.51e-6
TWR = 4 * FMAX / (M * G)
A_H = G * math.sqrt(TWR**2 - 1)
THETA_T = math.atan(A_H / G)
TAU_MAX = 2 * L * math.cos(BETA) * FMAX        # (f3+f4) - (f1+f2) = 2 f_max at the limit
ALPHA = TAU_MAX / JY
W_HOVER = math.sqrt(M * G / 4 / KF)
W_MAX = math.sqrt(FMAX / KF)
print(f"inputs: J_y = {JY} kg m^2, l cos(beta) = {L*math.cos(BETA):.6f} m, f_max = {FMAX} N")
print(f"T/W = {TWR:.4f}, a_h = {A_H:.3f} m/s^2, theta_t = {math.degrees(THETA_T):.2f} deg")
print(f"tau_max = {TAU_MAX:.4f} N m (lens 1.331), alpha_max = {ALPHA:.1f} rad/s^2 (lens 634)")
print(f"omega_hover = {W_HOVER:.1f} rad/s, omega_max = {W_MAX:.1f} rad/s")
quantity(f"{TAU_MAX:.6f} N m", "1.331 N m", rel_tol=3e-3)
quantity(f"{ALPHA:.6f} 1/s^2", "634 1/s^2", rel_tol=3e-3)
units("0.14 m * 0.5592 * 2 * 8.5 N / (2.1e-3 kg m^2)", "1/s^2")

# ---------------------------------------------------------------- ideal bang-bang
t_ideal = 2 * math.sqrt(THETA_T / ALPHA)
print(f"ideal rest-to-rest time 2 sqrt(theta/alpha) = {t_ideal*1e3:.2f} ms   (lens: 91.6 ms)")
quantity(f"{t_ideal:.8f} s", "91.6 ms", rel_tol=2e-2)

# ---------------------------------------------------------------- with the rotor-speed lag
def simulate(mtau, theta_t=THETA_T, dt=2e-5, model="omega"):
    """Bang-bang in commanded rotor speed; return the rest-to-rest time for theta_t.

    model 'omega': first-order lag on rotor speed, thrust = k_f omega^2 (the plant's own model).
    model 'torque': first-order lag on the pitch torque itself (cross-check).
    Switch time t_s is found by bisection so the body rate reaches zero exactly at theta_t.
    """
    def run(t_s, t_max=2.0):
        th, w = 0.0, 0.0
        wr, wf = W_HOVER, W_HOVER      # rear (accelerating) and front (decelerating) pair
        trq = 0.0
        t = 0.0
        while t < t_max:
            up = t < t_s
            if model == "omega":
                cmd_r, cmd_f = (W_MAX, 0.0) if up else (0.0, W_MAX)
                if mtau > 0:
                    wr += (cmd_r - wr) / mtau * dt
                    wf += (cmd_f - wf) / mtau * dt
                else:
                    wr, wf = cmd_r, cmd_f
                tq = 2 * L * math.cos(BETA) * KF * (wr**2 - wf**2)
            else:
                target = TAU_MAX if up else -TAU_MAX
                if mtau > 0:
                    trq += (target - trq) / mtau * dt
                else:
                    trq = target
                tq = trq
            w += tq / JY * dt
            th += w * dt
            t += dt
            if not up and w <= 0.0:
                return th, t
        return th, t
    lo, hi = 1e-5, 1.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        th_end, _ = run(mid)
        if th_end < theta_t:
            lo = mid
        else:
            hi = mid
    th_end, t_end = run(0.5 * (lo + hi))
    return t_end, th_end


for model in ("omega", "torque"):
    t0, th0 = simulate(0.0, model=model)
    print(f"[{model:6s}] lag = 0      : T = {t0*1e3:7.2f} ms (theta_end = {math.degrees(th0):.2f} deg)")
    t1, th1 = simulate(0.0391, model=model)
    print(f"[{model:6s}] lag = 39.1 ms: T = {t1*1e3:7.2f} ms (theta_end = {math.degrees(th1):.2f} deg)")
    if model == "omega":
        T_LAG = t1
        T_NOLAG = t0

# lag -> 0 limit must recover the closed form (dt = 2e-5 s resolves a lag down to ~1e-3 s)
print("lag sweep (omega model), monotone approach to the closed form as the lag -> 0:")
for mt in (0.0, 1e-3, 5e-3, 1e-2, 2e-2, 0.0391, 0.06):
    tt, _ = simulate(mt, model="omega")
    print(f"   motor_tau = {mt*1e3:5.1f} ms -> T = {tt*1e3:7.2f} ms")
t_small, _ = simulate(1e-3, model="omega")
quantity(f"{t_small:.8f} s", f"{t_ideal:.8f} s", rel_tol=5e-2)
quantity(f"{T_NOLAG:.8f} s", f"{t_ideal:.8f} s", rel_tol=5e-3)
print(f"lens's claim for the lagged time: 95.6 ms; computed {T_LAG*1e3:.2f} ms")
quantity(f"{T_LAG:.8f} s", "95.6 ms", rel_tol=5e-2)
print(f"cost of the motor lag = {(T_LAG-T_NOLAG)*1e3:.2f} ms (lens: 3-9 ms)")

# ---------------------------------------------------------------- elasticity in motor_tau
def speed(mtau, a_u=None, s=6.0, tau_s=0.107):
    a_u = a_u if a_u is not None else G * math.tan(math.radians(59.0))   # FoV-capped operating point
    trot, _ = simulate(mtau, theta_t=math.atan(a_u / G))
    tau_eff = tau_s + trot / 2
    return a_u * (math.sqrt(tau_eff**2 + 2 * s / a_u) - tau_eff), trot


v0, tr0 = speed(0.0391)
v1, tr1 = speed(0.0391 * 1.1)
e_rot = math.log(tr1 / tr0) / math.log(1.1)
e_v = math.log(v1 / v0) / math.log(1.1)
print(f"tau_rot(39.1 ms) = {tr0*1e3:.2f} ms, tau_rot(43.0 ms) = {tr1*1e3:.2f} ms")
print(f"d ln tau_rot/d ln motor_tau = {e_rot:+.3f}   (lens: +0.21)")
print(f"v = {v0:.4f} -> {v1:.4f} m/s; d ln v/d ln motor_tau = {e_v:+.4f}   (lens: ~ -0.02)")
quantity(f"{abs(e_v):.6f} m", "0.02 m", rel_tol=5e-1)
v_half, _ = speed(0.0391 * 0.5)
print(f"halving motor_tau: v = {v0:.4f} -> {v_half:.4f} m/s "
      f"({100*(v_half/v0-1):+.2f} %)   (lens: 19.49 -> 19.70 m/s, +1.08 %)")

raise SystemExit(finish())
