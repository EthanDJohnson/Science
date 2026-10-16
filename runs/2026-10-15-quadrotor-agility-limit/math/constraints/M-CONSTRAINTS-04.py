"""M-CONSTRAINTS-04: rest-to-rest slew and segment times with a first-order actuator lag, their
elasticities, and the distance lost at speed (lens findings F4 and F5, candidate CONSTRAINTS-C).

Claim as I state it (SI units):
  Plant: J xddot = u, udot = (u_cmd - u)/tc, u_cmd = +U up to a switch time, then -U, u(0) = 0.
  Rest-to-rest through a displacement D (angle or distance) the minimum-time bang-bang time is
      tc = 0:  t0 = 2 sqrt(D J / U)        (= 2 sqrt(theta/alpha) rotationally, 2 sqrt(d/A) linearly)
  and with tc > 0 the switch time is chosen so that both velocity and displacement hit their
  targets together.
  (a) Rotational: theta = 152 deg, alpha = U/J = 396.2 rad/s^2 (constant-altitude torque
      ceiling, M-CONSTRAINTS-02) -> t0 = 163.7 ms, and with tc = 39.1 ms, t = 201 ms, i.e. the
      lag adds 18.4 per cent; d ln t/d ln tc = +0.177.
  (b) Translational: d = 10 m, A = 39.0 m/s^2 -> t0 = 1012.5 ms, and with tc = 39.1 ms the
      penalty is 40.6 ms = 4.0 per cent; d ln t/d ln tc = +0.040, d ln t/d ln A = -0.481.
  (c) F5: at 15 m/s the 201 ms reversal occupies 3.02 m against 0.60 m for a 40 ms latency
      (factor 5); at 20 m/s, 4.02 m against 0.80 m.
Domain: J, U, D, tc > 0; one switch; no rate limit, no saturation other than |u_cmd| = U.
Verification: the semi-analytic solution is checked against an independent RK4 integration at
two step sizes, and against the tc -> 0 closed form.
"""
import sys
import math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, inequality, units, quantity, finish


def approx(label, got, want, rel=0.015):
    print(f"  {label}: got {got:.6g}, lens {want:.6g}")
    return inequality(f"Abs({got!r} - ({want!r}))", "<", f"{rel}*Abs({want!r})")


def state_phase1(t, acc, tc):
    """u_cmd = +U from rest with u(0) = 0; acc = U/J.  Returns (x, v, u/J)."""
    if tc <= 0.0:
        return 0.5 * acc * t * t, acc * t, acc
    e = math.exp(-t / tc)
    a = acc * (1.0 - e)
    v = acc * (t - tc * (1.0 - e))
    x = acc * (0.5 * t * t - tc * t + tc * tc * (1.0 - e))
    return x, v, a


def state_phase2(t, x1, v1, a1, acc, tc):
    """u_cmd = -U, starting from (x1, v1, a1) at t = 0 of this phase."""
    if tc <= 0.0:
        return x1 + v1 * t - 0.5 * acc * t * t, v1 - acc * t, -acc
    d = a1 + acc
    e = math.exp(-t / tc)
    a = -acc + d * e
    v = v1 - acc * t + d * tc * (1.0 - e)
    x = x1 + v1 * t - 0.5 * acc * t * t + d * tc * (t - tc * (1.0 - e))
    return x, v, a


def min_time(dist, acc, tc):
    """Bang-bang rest-to-rest time: bisect the switch time so that x hits dist when v = 0."""
    def finish_state(ts):
        x1, v1, a1 = state_phase1(ts, acc, tc)
        lo, hi = 0.0, 10.0
        for _ in range(200):                      # bisect on v(t') = 0
            mid = 0.5 * (lo + hi)
            if state_phase2(mid, x1, v1, a1, acc, tc)[1] > 0.0:
                lo = mid
            else:
                hi = mid
        t2 = 0.5 * (lo + hi)
        x, v, _ = state_phase2(t2, x1, v1, a1, acc, tc)
        return ts + t2, x, v
    lo, hi = 0.0, 10.0
    for _ in range(200):                          # bisect on the switch time
        ts = 0.5 * (lo + hi)
        if finish_state(ts)[1] < dist:
            lo = ts
        else:
            hi = ts
    ts = 0.5 * (lo + hi)
    t_tot, x_end, v_end = finish_state(ts)
    return t_tot, ts, x_end, v_end


def rk4_time(dist, acc, tc, dt):
    """Independent check: integrate xdot = v, vdot = a, adot = (a_cmd - a)/tc with RK4, using
    the switch time from min_time, and report when the velocity returns to zero."""
    _, ts, _, _ = min_time(dist, acc, tc)

    def f(t, y):
        a_cmd = acc if t < ts else -acc
        return (y[1], y[2], (a_cmd - y[2]) / tc if tc > 0 else 0.0)

    y = [0.0, 0.0, 0.0 if tc > 0 else acc]
    t = 0.0
    prev = y[:]
    while t < 5.0:
        ks = []
        for c, w in ((0.0, None), (0.5, 0), (0.5, 1), (1.0, 2)):
            base = y if w is None else [y[i] + dt * c * ks[w][i] for i in range(3)]
            ks.append(f(t + c * dt, base))
        y = [y[i] + dt / 6.0 * (ks[0][i] + 2 * ks[1][i] + 2 * ks[2][i] + ks[3][i]) for i in range(3)]
        t += dt
        if t > ts and y[1] <= 0.0:
            frac = prev[1] / (prev[1] - y[1])
            return t - dt + frac * dt, prev[0] + frac * (y[0] - prev[0])
        prev = y[:]
    return float("nan"), float("nan")


# ------------------------------------------------------------------ closed forms and limits
print("0. closed form for zero lag: t0 = 2 sqrt(D J/U)")
dd, jj, uu = sp.symbols("dd jj uu", positive=True)
t0_sym = 2 * sp.sqrt(dd * jj / uu)
# half the distance in half the time at constant acceleration U/J
identity(t0_sym, 2 * sp.sqrt(2 * (dd / 2) / (uu / jj)))
units("2 * (10 m / (39.0 m/s^2))^0.5", "s")

ALPHA = 0.11606535 * 0.870 * 9.81 / 2.5e-3        # rad/s^2, from M-CONSTRAINTS-02
THETA = math.radians(152.0)
print(f"1. rotational slew: theta = 152 deg, alpha = {ALPHA:.2f} rad/s^2")
t0 = 2.0 * math.sqrt(THETA / ALPHA)
approx("t0 (no lag) [ms]", 1000 * t0, 163.7, rel=0.01)
t_nolag, _, x_e, v_e = min_time(THETA, ALPHA, 0.0)
approx("solver t (tc = 0) [ms]", 1000 * t_nolag, 163.7, rel=0.01)
t_lag, ts_lag, x_e, v_e = min_time(THETA, ALPHA, 0.0391)
print(f"   with tc = 39.1 ms: t = {1000*t_lag:.2f} ms (switch at {1000*ts_lag:.2f} ms), "
      f"end angle {x_e:.6f} rad vs {THETA:.6f}, end rate {v_e:.2e} rad/s")
print(f"   (first-order-torque model: {1000*t_lag:.2f} ms, 3 per cent above the lens's 201 ms; see 1b)")
inequality(f"{abs(x_e - THETA)!r}", "<", "1e-9")           # the solver really lands on theta
for dt in (2e-5, 1e-5):
    t_rk, x_rk = rk4_time(THETA, ALPHA, 0.0391, dt)
    print(f"   RK4 dt = {dt:.0e}: t = {1000*t_rk:.3f} ms, x = {x_rk:.6f} rad")
    inequality(f"{abs(t_rk - t_lag)!r}", "<", "2e-5")
h = 0.01
el = (math.log(min_time(THETA, ALPHA, 0.0391 * (1 + h))[0])
      - math.log(min_time(THETA, ALPHA, 0.0391 * (1 - h))[0])) / (2 * h)
print(f"   d ln t_slew/d ln tc in the first-order-torque model: {el:+.4f}")

print("2. translational segment: d = 10 m, A = 39.0 m/s^2")
A_SEG, D_SEG = 39.0, 10.0
t0s = 2.0 * math.sqrt(D_SEG / A_SEG)
approx("t0 (no lag) [ms]", 1000 * t0s, 1012.5, rel=0.002)
t_seg = min_time(D_SEG, A_SEG, 0.0391)[0]
print(f"   with tc = 39.1 ms: t = {1000*t_seg:.2f} ms")
approx("segment penalty [ms]", 1000 * (t_seg - t0s), 40.6, rel=0.05)
approx("segment penalty [%]", 100.0 * (t_seg - t0s) / t0s, 4.0, rel=0.05)
el_tc = (math.log(min_time(D_SEG, A_SEG, 0.0391 * (1 + h))[0])
         - math.log(min_time(D_SEG, A_SEG, 0.0391 * (1 - h))[0])) / (2 * h)
approx("d ln t_seg / d ln tc", el_tc, 0.040, rel=0.05)
el_A = (math.log(min_time(D_SEG, A_SEG * (1 + h), 0.0391)[0])
        - math.log(min_time(D_SEG, A_SEG * (1 - h), 0.0391)[0])) / (2 * h)
approx("d ln t_seg / d ln A", el_A, -0.481, rel=0.05)
# the lag-free limit of the elasticity to A is exactly -1/2
el_A0 = (math.log(min_time(D_SEG, A_SEG * (1 + h), 0.0)[0])
         - math.log(min_time(D_SEG, A_SEG * (1 - h), 0.0)[0])) / (2 * h)
approx("d ln t_seg / d ln A at tc = 0", el_A0, -0.5, rel=1e-3)
identity(sp.diff(sp.log(t0_sym), uu) * uu, -sp.Rational(1, 2))   # lag-free elasticity to U is -1/2
limit(t0_sym, "uu", "oo", 0)                                     # infinite authority: zero time
# halving the lag buys about 2 per cent of segment time
t_half = min_time(D_SEG, A_SEG, 0.01955)[0]
approx("time saved by halving tc [%]", 100.0 * (t_seg - t_half) / t_seg, 2.0, rel=0.20)
t_ten = min_time(D_SEG, A_SEG, 0.010)[0]
approx("time saved by tc = 10 ms [%]", 100.0 * (t_seg - t_ten) / t_seg, 3.0, rel=0.20)

print("1b. the same slew with the rotor-speed lag acting through f = k_f omega^2")
# Independent second model, closer to the lens's plant: two rotors commanded to 0 and two to
# sqrt(2) omega_h from hover, omegadot = (omega_cmd - omega)/tc, tau_x = 2 l_eff k_f (w_hi^2 - w_lo^2).
L_EFF, K_F, M_V, JX = 0.11606535, 1.51e-6, 0.870, 2.5e-3
W_H = math.sqrt(M_V * 9.81 / (4.0 * K_F))
W_HI = math.sqrt(2.0) * W_H
print(f"   omega_h = {W_H:.1f} rad/s, omega_hi_cmd = {W_HI:.1f} rad/s")


def slew_quadratic(theta, tc, ts, dt=2e-5):
    """RK4 on (w_lo, w_hi, p, phi); command swaps at ts.  Returns (t at p = 0, phi then)."""
    def f(t, y):
        lo_cmd, hi_cmd = (0.0, W_HI) if t < ts else (W_HI, 0.0)
        tq = 2.0 * L_EFF * K_F * (y[1] ** 2 - y[0] ** 2)
        return ((lo_cmd - y[0]) / tc, (hi_cmd - y[1]) / tc, tq / JX, y[2])
    y = [W_H, W_H, 0.0, 0.0]
    t = 0.0
    prev = y[:]
    while t < 1.0:
        ks = []
        for c, w in ((0.0, None), (0.5, 0), (0.5, 1), (1.0, 2)):
            base = y if w is None else [y[i] + dt * c * ks[w][i] for i in range(4)]
            ks.append(f(t + c * dt, base))
        y = [y[i] + dt / 6.0 * (ks[0][i] + 2 * ks[1][i] + 2 * ks[2][i] + ks[3][i]) for i in range(4)]
        t += dt
        if t > ts and y[2] <= 0.0:
            fr = prev[2] / (prev[2] - y[2])
            return t - dt + fr * dt, prev[3] + fr * (y[3] - prev[3])
        prev = y[:]
    return float("nan"), float("nan")


def solve_q(tc, dt=2e-5):
    lo, hi = 0.0, 0.3
    for _ in range(40):                 # bisect the switch time so that phi(t_f) = theta
        mid = 0.5 * (lo + hi)
        if slew_quadratic(THETA, tc, mid, dt)[1] < THETA:
            lo = mid
        else:
            hi = mid
    return slew_quadratic(THETA, tc, 0.5 * (lo + hi), dt)


t_q, phi_q = solve_q(0.0391)
print(f"   quadratic-thrust model: t = {1000*t_q:.2f} ms, phi_end = {phi_q:.6f} rad "
      f"(target {THETA:.6f})")
approx("slew with 39.1 ms rotor lag, f ~ omega^2 [ms]", 1000 * t_q, 201.0, rel=0.02)
t_q2, _ = solve_q(0.0391, dt=1e-5)
inequality(f"{abs(t_q2 - t_q)!r}", "<", "1e-4")
approx("lag penalty as a fraction of the lagged slew [%]", 100.0 * (t_q - t0) / t_q, 18.4, rel=0.05)
el_q = (math.log(solve_q(0.0391 * 1.05)[0]) - math.log(solve_q(0.0391 * 0.95)[0])) / (2 * 0.05)
print(f"   d ln t_slew/d ln tc in the quadratic-thrust model: {el_q:+.4f}")
approx("d ln t_slew / d ln tc (quadratic model)", el_q, 0.177, rel=0.08)
print(f"   (the first-order-torque model gives {1000*t_lag:.1f} ms: the quadratic map raises the "
      f"initial torque slope by sqrt(2), shortening the slew)")

print("3. F5: distance travelled during the reversal and during the latency")
for v in (15.0, 20.0):
    print(f"   v = {v} m/s: reversal {v*t_q:.3f} m, latency {v*0.040:.3f} m, "
          f"ratio {t_q/0.040:.2f}")
approx("reversal distance at 15 m/s [m]", 15.0 * t_q, 3.02, rel=0.02)
approx("latency distance at 15 m/s [m]", 15.0 * 0.040, 0.60, rel=0.01)
approx("reversal distance at 20 m/s [m]", 20.0 * t_q, 4.02, rel=0.02)
approx("ratio reversal/latency", t_q / 0.040, 5.0, rel=0.05)
quantity("15 m/s * 0.201 s", "3.015 m", rel_tol=1e-3)
units("20 m/s * 0.040 s", "m")

raise SystemExit(finish())
