#!/usr/bin/env python3
"""Executable plant + onboard-style cascaded controller + course, for the simulator lens.

MODULE, not a standalone calculation: the experiment scripts import it.  Run it directly for
a smoke test.

WHAT IS IN THE MODEL
    * 17-state quadrotor (position, quaternion, world velocity, body rates, four rotor speeds)
      from the verified toolkit calculator `quadrotor.py` (`platform_sun2022`, the published
      0.75 kg parameter set of Sun et al., IEEE T-RO 38 (2022) 3357-3373 TABLE II).
    * First-order rotor-speed lag (motor_tau) with an optional slew limit, per-rotor thrust
      limits 0..8.5 N, and the exact four-rotor thrust/torque map with saturation handled by a
      torque-priority mixer (the racing-firmware convention).
    * Linear rotor drag kd = (0.26, 0.28, 0.42) kg/s and the h-force term kh = 0.01 kg/m,
      switchable, so "unmodelled aerodynamics" can be made a genuine PLANT-only effect: the
      controller's feed-forward uses the nominal (drag-free) model unless told otherwise.
    * TWO measurement delays, because they enter the cascade at different levels and this is
      the architectural fact the question turns on:
        tau_imu  -> body rates and attitude (gyro/IMU path, ~1 ms)
        tau_vio  -> position and velocity   (visual-inertial path, 10-60 ms)
      Each is a pure transport delay on the measured state, implemented by a history buffer.
    * Zero-order-hold sampling at f_inner (rate/attitude) and f_outer (position/velocity).
    * Additive Gaussian sensor noise, an external disturbance force, and a wind velocity.
    * Two reference architectures: "preview" (the whole trajectory known in advance, i.e. the
      seen-course regime of Swift and MonoRace) and "lookahead" (pure pursuit on a path that
      is only visible out to s_look metres, i.e. the unseen-course regime of the brief).

WHAT IS LEFT OUT (and which way each omission moves the answer)
    contact/crash dynamics                 -- none; a gate miss is scored, not simulated
    bearing/aero torque, blade flapping     -- would make high speed HARDER (aero candidate up)
    battery sag, thrust-vs-voltage          -- would make high speed HARDER (actuator up)
    airframe flexibility, prop unbalance    -- would lower the usable rate-loop gain
    VIO drift and estimation ERROR          -- only latency and white noise are modelled; drift
                                              would make the estimation candidate STRONGER
    motion blur / feature loss vs speed     -- not modelled; would make perception+estimation
                                              candidates stronger at high speed
    rotor-spin-up gyroscopic torque (G2)    -- small; would slightly lower the actuator ceiling
    ground effect, prop-wash, wind gusts    -- a steady wind and an impulse stand in for them

UNITS: SI throughout (m, s, kg, N, N m, rad, rad/s).
"""

from __future__ import annotations

import math
import os
import sys

import numpy as np

_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, os.path.join(_ROOT, ".claude", "skills", "conundrum", "scripts"))

import control_tools as ct                                   # noqa: E402
from quadrotor import Quadrotor, platform_sun2022, quat_to_rot  # noqa: E402

G = 9.80665

# ---------------------------------------------------------------------------- the course
class Slalom:
    """y = A sin(2 pi x / L) at constant altitude z0; gates at the lateral extremes.

    Gate opening 1.5 m (the MonoRace gate, dossier A-26); scoring tolerance is the half
    opening minus a 0.25 m vehicle radius (5-inch airframe tip-to-tip ~0.4 m diagonal), i.e.
    0.5 m on both the lateral and the vertical error at the gate plane.
    """

    def __init__(self, amp=3.0, period=30.0, z0=2.0, x_end=90.0, tol=0.5):
        self.A, self.L, self.z0, self.x_end, self.tol = amp, period, z0, x_end, tol
        self.k = 2.0 * math.pi / period
        # gates at the extremes of the sine inside [0, x_end]
        self.gates = [x for x in np.arange(period / 4.0, x_end + 1e-9, period / 2.0)]

    def p(self, x):
        return np.array([x, self.A * math.sin(self.k * x), self.z0])

    def dpdx(self, x):
        return np.array([1.0, self.A * self.k * math.cos(self.k * x), 0.0])

    def d2pdx2(self, x):
        return np.array([0.0, -self.A * self.k ** 2 * math.sin(self.k * x), 0.0])

    def tangent(self, x):
        d = self.dpdx(x)
        return d / np.linalg.norm(d)

    def curvature(self, x):
        yp = self.A * self.k * math.cos(self.k * x)
        ypp = -self.A * self.k ** 2 * math.sin(self.k * x)
        return abs(ypp) / (1.0 + yp ** 2) ** 1.5

    def normal(self, x):
        """Unit principal normal (in the horizontal plane), pointing to the centre of curvature."""
        ypp = -self.A * self.k ** 2 * math.sin(self.k * x)
        t = self.tangent(x)
        n = np.array([-t[1], t[0], 0.0])        # left normal
        return n * (1.0 if ypp > 0 else -1.0) if abs(ypp) > 0 else n

    def arclength(self, x0=0.0, x1=None, n=20001):
        x1 = self.x_end if x1 is None else x1
        xs = np.linspace(x0, x1, n)
        sp = np.sqrt(1.0 + (self.A * self.k * np.cos(self.k * xs)) ** 2)
        return float(np.trapezoid(sp, xs)) if hasattr(np, "trapezoid") else float(np.trapz(sp, xs))

    # --- constant-x-rate reference: x = U t, so speed = U |dp/dx|
    def ref(self, t, U):
        x = U * t
        p = self.p(x)
        v = self.dpdx(x) * U
        a = self.d2pdx2(x) * U ** 2
        j = np.array([0.0, -self.A * self.k ** 3 * math.cos(self.k * x) * U ** 3, 0.0])
        return p, v, a, j

    def ref_peak_accel(self, U):
        return self.A * self.k ** 2 * U ** 2       # at the extremes, m/s^2

    def ref_feasible_U(self, a_max):
        return math.sqrt(a_max / (self.A * self.k ** 2))


def time_optimal_on_path(s, kappa, a_max, v_cap, v0=0.0, v1=0.0):
    """Generic time-optimal speed profile along a path given by arc length s (increasing) and
    curvature kappa(s), for a point mass with isotropic |a| <= a_max and top speed v_cap.

    Velocity limit curve  v_lim = min(v_cap, sqrt(a_max/kappa));
    tangential budget     a_t = sqrt(a_max^2 - (kappa v^2)^2);
    forward pass from v0, backward pass from v1, v = min of the two.  Returns the speed array.
    Known limits used as tests: kappa = 0 and v_cap = inf, rest to rest, gives
    t = 2 sqrt(S/a_max); constant kappa = 1/R with a long path gives a cruise speed
    sqrt(a_max R).
    """
    s = np.asarray(s, float)
    kappa = np.asarray(kappa, float)
    vlim = np.minimum(v_cap, np.where(kappa > 1e-12, np.sqrt(a_max / np.maximum(kappa, 1e-12)),
                                      np.inf))
    n = len(s)
    vf = np.empty(n); vf[0] = min(v0, vlim[0])
    for i in range(1, n):
        lat = kappa[i - 1] * vf[i - 1] ** 2
        at = math.sqrt(max(a_max ** 2 - lat ** 2, 0.0))
        vf[i] = min(vlim[i], math.sqrt(max(vf[i - 1] ** 2 + 2 * at * (s[i] - s[i - 1]), 0.0)))
    vb = np.empty(n); vb[-1] = min(v1, vlim[-1])
    for i in range(n - 2, -1, -1):
        lat = kappa[i + 1] * vb[i + 1] ** 2
        at = math.sqrt(max(a_max ** 2 - lat ** 2, 0.0))
        vb[i] = min(vlim[i], math.sqrt(max(vb[i + 1] ** 2 + 2 * at * (s[i + 1] - s[i]), 0.0)))
    return np.minimum(vf, vb)


def path_time(s, v):
    s, v = np.asarray(s, float), np.asarray(v, float)
    vm = np.maximum(0.5 * (v[1:] + v[:-1]), 1e-9)
    return float(np.sum(np.diff(s) / vm))


def time_optimal_path_time(course, a_max, v_cap, pad=30.0, ds=0.02):
    """Time-optimal traversal of the GIVEN path for a point mass with isotropic horizontal
    |a| <= a_max and a top speed v_cap, by the standard velocity-limit-curve forward-backward
    integration.  The path is extended by `pad` metres on each side with v = 0 at the ends, and
    only the timed section x in [0, x_end] is reported, so entry and exit transients are
    excluded (a flying lap).

    v_limit(s) = min(v_cap, sqrt(a_max / kappa(s)));  a_tangential = sqrt(a_max^2 - (kappa v^2)^2).
    """
    xs = np.arange(-pad, course.x_end + pad + ds, ds)
    yp = course.A * course.k * np.cos(course.k * xs)
    ypp = -course.A * course.k ** 2 * np.sin(course.k * xs)
    kap = np.abs(ypp) / (1.0 + yp ** 2) ** 1.5
    sp = np.sqrt(1.0 + yp ** 2)                 # ds/dx
    s = np.concatenate([[0.0], np.cumsum(0.5 * (sp[1:] + sp[:-1]) * ds)])
    v = time_optimal_on_path(s, kap, a_max, v_cap, v0=0.0, v1=0.0)
    i0 = int(np.argmin(np.abs(xs - 0.0)))
    i1 = int(np.argmin(np.abs(xs - course.x_end)))
    t = path_time(s[i0:i1 + 1], v[i0:i1 + 1])
    return {"t_opt": t, "s_timed": float(s[i1] - s[i0]), "v_mean": float((s[i1] - s[i0]) / t),
            "v_min": float(np.min(v[i0:i1 + 1])), "v_max": float(np.max(v[i0:i1 + 1])),
            "v_cap": v_cap, "a_max": a_max}


def level_flight_v_max(q, tol=1e-4):
    """Highest steady level-flight speed along +x_B: solve for the tilt and thrust that balance
    gravity plus the drag/h-force model, with T <= 4 thrust_max.  Bisection on speed."""
    def feasible(v):
        # steady: R (T z_B + f_aero(v_B)) + m g = 0, flying along +x_W at speed v.
        # pitch theta (nose down, rotation about y_B): v_B = (v cos th, 0, -v sin th) for a
        # ZYX pitch of -th ... solve by a small 2-D search over theta.
        best = None
        for th in np.linspace(0.0, math.radians(85.0), 400):
            # body x axis tilted forward by th: R = Ry(-th) with +z_B up
            c, s_ = math.cos(th), math.sin(th)
            R = np.array([[c, 0.0, s_], [0.0, 1.0, 0.0], [-s_, 0.0, c]])
            vB = R.T @ np.array([v, 0.0, 0.0])
            fa = q.aero_force_body(vB)
            # need T z_B + fa to cancel m g e3 (world) -> solve least squares on the two
            # in-plane components; T is the free scalar.
            # world force = R(T e3 + fa) - m g e3 = 0
            A = R @ np.array([0.0, 0.0, 1.0])
            b = q.mass * np.array([0.0, 0.0, G]) - R @ fa
            T = float(A @ b / (A @ A))
            res = np.linalg.norm(A * T - b)
            if T <= 4 * q.thrust_max and res < 0.05 * q.mass * G:
                best = (T, th, res) if best is None or T < best[0] else best
        return best is not None
    lo, hi = 0.0, 120.0
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if feasible(mid):
            lo = mid
        else:
            hi = mid
    return lo


# ---------------------------------------------------------------------------- tuning rule
def max_crossover_for_pm(tau_delay, lag_tau, pm_target_deg=40.0, w_cap=400.0):
    """Largest rate-loop gain w (rad/s) whose phase margin is exactly pm_target, for
        L(s) = (w/s) exp(-s tau_delay) / (1 + s lag_tau).

    Solved in CLOSED FORM, not with loop_margins: for a pure delay the phase wraps, and a
    phase margin read off the principal value is wrong by multiples of 360 deg (this is a real
    trap -- an earlier version of this module used loop_margins here and reported crossovers
    20 times too high, which inverted the actuator-bandwidth conclusion).

    At the gain crossover w_c: |L| = 1 and
        PM = 90 deg - (w_c tau_delay + atan(w_c lag_tau)) in degrees.
    PM decreases monotonically in w_c, so bisect on w_c, then w = w_c sqrt(1 + (w_c lag_tau)^2).
    w_cap bounds the result where there is no delay and no lag at all (PM = 90 deg for every
    gain); 400 rad/s = 64 Hz is already five times any rate loop in the dossier.
    """
    target = math.radians(90.0 - pm_target_deg)       # allowed total phase lag, rad

    def lag(wc):
        return wc * tau_delay + math.atan(wc * lag_tau)

    if lag(w_cap) <= target:
        wc = w_cap
    else:
        lo, hi = 1e-6, w_cap
        for _ in range(200):
            mid = 0.5 * (lo + hi)
            if lag(mid) <= target:
                lo = mid
            else:
                hi = mid
        wc = lo
    return wc * math.sqrt(1.0 + (wc * lag_tau) ** 2)


class TimeOptimalRef:
    """Reference trajectory = the time-optimal speed profile of the path for an acceleration
    budget alpha * a_h, turned into p_ref(t), v_ref(t), a_ref(t).

    alpha = 1 is the platform's own point-mass optimum on this path, which leaves exactly zero
    acceleration margin for feedback; alpha < 1 buys margin at the cost of time.  Using this
    family instead of a constant-rate sinusoid removes the artificial ceiling a fixed reference
    family imposes, and makes "the fraction of the platform's time-optimal time" exact.
    """

    def __init__(self, course, a_h, alpha, v_cap=np.inf, pad=40.0, ds=0.01):
        self.course, self.alpha, self.a_h = course, alpha, a_h
        a_use = alpha * a_h
        xs = np.arange(-pad, course.x_end + pad + ds, ds)
        yp = course.A * course.k * np.cos(course.k * xs)
        ypp = -course.A * course.k ** 2 * np.sin(course.k * xs)
        kap = np.abs(ypp) / (1.0 + yp ** 2) ** 1.5
        sp = np.sqrt(1.0 + yp ** 2)
        s = np.concatenate([[0.0], np.cumsum(0.5 * (sp[1:] + sp[:-1]) * ds)])
        v = time_optimal_on_path(s, kap, a_use, v_cap, 0.0, 0.0)
        # time law, measured from x = 0
        dt_ = np.diff(s) / np.maximum(0.5 * (v[1:] + v[:-1]), 1e-9)
        t = np.concatenate([[0.0], np.cumsum(dt_)])
        i0 = int(np.argmin(np.abs(xs - 0.0)))
        self.t = t - t[i0]
        self.xs, self.s, self.v, self.kap, self.ypp = xs, s, v, kap, ypp
        # tangential acceleration a_t = v dv/ds
        self.at = v * np.gradient(v, s)
        i1 = int(np.argmin(np.abs(xs - course.x_end)))
        self.t_total = float(self.t[i1])
        self.v0 = float(v[i0])

    def __call__(self, tq):
        x = float(np.interp(tq, self.t, self.xs))
        v = float(np.interp(tq, self.t, self.v))
        at = float(np.interp(tq, self.t, self.at))
        c = self.course
        That = c.tangent(x)
        kap = c.curvature(x)
        ypp = -c.A * c.k ** 2 * math.sin(c.k * x)
        nhat = np.array([-That[1], That[0], 0.0]) * (1.0 if ypp > 0 else -1.0)
        p = c.p(x)
        return p, v * That, at * That + kap * v * v * nhat, x


# ---------------------------------------------------------------------------- controller
class Cascade:
    """Rate -> attitude -> velocity/position cascade with explicit sampling and two delays."""

    def __init__(self, q, tau_imu=1e-3, tau_vio=20e-3, f_inner=500.0, f_outer=200.0,
                 pm_target=40.0, sep=3.0, know_drag=False, lead_compensation=False,
                 w_rate_fixed=None, nominal=None, w_rate_cap=60.0):
        self.q = q
        self.nominal = nominal if nominal is not None else q   # the controller's own model
        self.tau_imu, self.tau_vio = tau_imu, tau_vio
        self.f_inner, self.f_outer = f_inner, f_outer
        self.know_drag = know_drag
        self.lead = lead_compensation
        lag = 0.0 if lead_compensation else q.motor_tau
        self.tau_in = tau_imu + 0.5 / f_inner
        self.tau_out = tau_vio + 0.5 / f_outer
        # w_rate_cap: above about 60 rad/s this PROPORTIONAL cascade loses stability margin in
        # the full multi-loop nonlinear plant even though the SISO rate loop still has 40 deg
        # of phase margin (loop interaction, mixer saturation, yaw channel).  The cap is a
        # property of the controller architecture, not of the plant, so every actuator-
        # bandwidth result at motor_tau below about 20 ms is a LOWER bound on what a better
        # inner loop (INDI, dossier D-09) could extract.
        self.w_rate = (min(max_crossover_for_pm(self.tau_in, lag, pm_target), w_rate_cap)
                       if w_rate_fixed is None else w_rate_fixed)
        self.w_rate_capped = (w_rate_fixed is None
                              and max_crossover_for_pm(self.tau_in, lag, pm_target) > w_rate_cap)
        self.w_att = self.w_rate / sep
        # outer loop also cannot exceed what its own (slower) delay path allows
        w_out_delay = max_crossover_for_pm(self.tau_out, 0.0, pm_target)
        self.w_vel = min(self.w_att / sep, w_out_delay)
        self.w_pos = self.w_vel / sep

    def spec(self):
        return dict(tau_imu=self.tau_imu, tau_vio=self.tau_vio, f_inner=self.f_inner,
                    f_outer=self.f_outer, w_rate=self.w_rate, w_att=self.w_att,
                    w_vel=self.w_vel, w_pos=self.w_pos, know_drag=self.know_drag,
                    lead=self.lead, motor_tau=self.q.motor_tau)

    # ---- outer loop: desired world acceleration -> (thrust, desired tilt)
    def outer(self, p_m, v_m, p_ref, v_ref, a_ref):
        a = a_ref + self.w_vel * (v_ref - v_m) + self.w_pos * self.w_vel * (p_ref - p_m)
        if self.know_drag:
            kd = np.asarray(self.nominal.kd, float)
            a = a + kd * v_m / self.nominal.mass          # cancel linear drag (world ~ body at small tilt)
        return a

    def thrust_and_attitude(self, a_des, q_m, yaw_ref=0.0):
        m = self.nominal.mass
        f_w = m * (a_des + np.array([0.0, 0.0, G]))
        nf = np.linalg.norm(f_w)
        if nf < 1e-9:
            f_w, nf = np.array([0.0, 0.0, 1e-9]), 1e-9
        zb_des = f_w / nf
        R = quat_to_rot(q_m)
        T = float(f_w @ (R @ np.array([0.0, 0.0, 1.0])))   # projected thrust
        T = max(T, 0.0)
        return T, zb_des

    def rate_cmd(self, q_m, zb_des, yaw_ref=0.0):
        R = quat_to_rot(q_m)
        zb = R @ np.array([0.0, 0.0, 1.0])
        # reduced-attitude (tilt) error as a rotation vector in the BODY frame
        cr = np.cross(zb, zb_des)
        ncr = np.linalg.norm(cr)
        ang = math.atan2(ncr, float(np.clip(zb @ zb_des, -1.0, 1.0)))
        e_w = (cr / ncr) * ang if ncr > 1e-12 else np.zeros(3)
        e_b = R.T @ e_w
        # yaw error from the body x axis projected into the horizontal plane
        xb = R @ np.array([1.0, 0.0, 0.0])
        psi = math.atan2(xb[1], xb[0])
        e_yaw = math.atan2(math.sin(yaw_ref - psi), math.cos(yaw_ref - psi))
        return self.w_att * (e_b + np.array([0.0, 0.0, 1.0]) * e_yaw)

    def torque_cmd(self, om_m, om_des, om_rate_meas=None):
        J = np.asarray(self.nominal.inertia, float)
        alpha = self.w_rate * (om_des - om_m)
        if self.lead and self.q.motor_tau > 0:
            # lead term that partially inverts the first-order actuator lag (an INDI-like
            # inner loop): tau_cmd = J (alpha + motor_tau * dalpha/dt) approximated with the
            # measured rate error derivative held in the caller.
            alpha = alpha * (1.0 + 0.0)   # the inversion is applied in `step` via tau scaling
        return J * alpha + np.cross(om_m, J * om_m)

    def mix(self, T, tau):
        """Torque-priority mixer: find the largest collective thrust scale that keeps all four
        rotor thrusts inside [0, thrust_max] while preserving the commanded torque."""
        q = self.q
        M = q.mix_matrix()
        f = np.linalg.solve(M, np.array([T, *tau]))
        fmax, fmin = q.thrust_max, q.thrust_min
        if np.all(f >= fmin - 1e-12) and np.all(f <= fmax + 1e-12):
            return np.clip(f, fmin, fmax), False
        # shift collective (null direction of the torque rows is f + c*[1,1,1,1]/..., and
        # adding a constant to all four thrusts changes only T for this symmetric X layout)
        c_hi = fmax - np.max(f)
        c_lo = fmin - np.min(f)
        c = float(np.clip(0.0, c_lo, c_hi)) if c_lo <= c_hi else 0.5 * (c_lo + c_hi)
        f2 = f + c
        if np.all(f2 >= fmin - 1e-9) and np.all(f2 <= fmax + 1e-9):
            return np.clip(f2, fmin, fmax), True
        # torque itself is infeasible: scale the torque down until it fits
        lo, hi = 0.0, 1.0
        f0 = np.linalg.solve(M, np.array([T, 0.0, 0.0, 0.0]))
        for _ in range(40):
            mid = 0.5 * (lo + hi)
            ft = np.linalg.solve(M, np.array([T, *(mid * np.asarray(tau))]))
            cc = float(np.clip(0.0, fmin - np.min(ft), fmax - np.max(ft)))
            if np.all(ft + cc >= fmin - 1e-9) and np.all(ft + cc <= fmax + 1e-9):
                lo = mid
            else:
                hi = mid
        ft = np.linalg.solve(M, np.array([T, *(lo * np.asarray(tau))]))
        cc = float(np.clip(0.0, fmin - np.min(ft), fmax - np.max(ft)))
        return np.clip(ft + cc, fmin, fmax), True


# ---------------------------------------------------------------------------- closed loop
def run_course(q, ctl, course, U, dt=1e-3, mode="preview", s_look=12.0,
               noise=None, seed=0, wind=np.zeros(3), f_dist=None, t_extra=0.6,
               max_tilt_deg=85.0, ref=None):
    """Fly the course from a flying start and score the gates.

    noise: dict(p=, v=, att=, om=) standard deviations (m, m/s, rad, rad/s).
    f_dist: callable f(t) -> external force in WORLD frame (N), e.g. an impulse or a push.
    Returns gate errors, success, timing and effort statistics.
    """
    rng = np.random.default_rng(seed)
    assert q.state_dim == 17, "use motor_tau > 0 so the actuator chain is in the plant"
    x = np.zeros(17)
    if ref is not None:
        p0, v0, _, _ = ref(0.0)
    else:
        p0, v0, _, _ = course.ref(0.0, U)
    x[0:3] = p0
    x[3:7] = np.array([1.0, 0.0, 0.0, 0.0])
    x[7:10] = v0
    x[13:17] = q.hover()["omega_hover"]

    n_inner = max(1, int(round((1.0 / ctl.f_inner) / dt)))
    n_outer = max(1, int(round((1.0 / ctl.f_outer) / dt)))
    T_end = (ref.t_total if ref is not None else course.x_end / U) * 1.6 + t_extra
    nsteps = int(round(T_end / dt))
    hist = [x.copy()]                       # state history for the delay buffers
    k_imu = int(round(ctl.tau_imu / dt))
    k_vio = int(round(ctl.tau_vio / dt))

    gate_err, gate_done = [], 0
    u = x[13:17].copy()
    a_des = np.zeros(3)
    zb_des = np.array([0.0, 0.0, 1.0])
    thrust_cmd = q.mass * G
    peak_f, sumsq_f, nf_ = 0.0, 0.0, 0
    n_sat, n_ctl = 0, 0
    fail = None
    t = 0.0
    px_prev = x[0]
    t_cross = {}

    for i in range(nsteps):
        hi_imu = hist[max(0, len(hist) - 1 - k_imu)]
        hi_vio = hist[max(0, len(hist) - 1 - k_vio)]
        if noise:
            p_m = hi_vio[0:3] + rng.normal(0, noise.get("p", 0.0), 3)
            v_m = hi_vio[7:10] + rng.normal(0, noise.get("v", 0.0), 3)
            qq = hi_imu[3:7] + rng.normal(0, noise.get("att", 0.0), 4)
            q_m = qq / np.linalg.norm(qq)
            om_m = hi_imu[10:13] + rng.normal(0, noise.get("om", 0.0), 3)
        else:
            p_m, v_m = hi_vio[0:3], hi_vio[7:10]
            q_m, om_m = hi_imu[3:7], hi_imu[10:13]

        if i % n_outer == 0:
            if mode == "preview":
                p_ref, v_ref, a_ref, _ = (ref(t) if ref is not None else course.ref(t, U))
            else:                                    # pure pursuit on the visible path
                xv = p_m[0]
                xt = xv
                for _ in range(200):                 # march the carrot to distance s_look
                    d = np.linalg.norm(course.p(xt) - p_m)
                    if d >= s_look:
                        break
                    xt += 0.25
                p_ref = course.p(xt)
                dirn = p_ref - p_m
                nd = np.linalg.norm(dirn)
                v_ref = U * course.tangent(xt) if nd < 1e-9 else U * dirn / nd
                kap = course.curvature(xt)
                a_ref = U * U * kap * course.normal(xt)
                p_ref = p_m + dirn                   # position term folded into v_ref
                a_des = ctl.outer(p_m, v_m, p_m, v_ref, a_ref)
            if mode == "preview":
                a_des = ctl.outer(p_m, v_m, p_ref, v_ref, a_ref)
        if i % n_inner == 0:
            thrust_cmd, zb_des = ctl.thrust_and_attitude(a_des, q_m)
            om_des = ctl.rate_cmd(q_m, zb_des)
            tau_cmd = ctl.torque_cmd(om_m, om_des)
            f_cmd, _sat = ctl.mix(thrust_cmd, tau_cmd)
            n_ctl += 1
            n_sat += 1 if _sat else 0
            u = np.sqrt(np.maximum(f_cmd, 0.0) / q.k_thrust)

        # ---- integrate one dt with RK4, holding u (zero-order hold)
        def fdyn(tt, y):
            d = q.dynamics(y, u)
            extra = np.zeros(3)
            if f_dist is not None:
                extra = extra + np.asarray(f_dist(tt), float)
            if np.any(wind):
                # relative-airspeed correction: the plant used v, we want v - wind
                R = quat_to_rot(y[3:7])
                vb = R.T @ y[7:10]
                vbw = R.T @ (y[7:10] - wind)
                extra = extra + R @ (q.aero_force_body(vbw) - q.aero_force_body(vb))
            d[7:10] = d[7:10] + extra / q.mass
            return d

        k1 = fdyn(t, x)
        k2 = fdyn(t + dt / 2, x + dt / 2 * k1)
        k3 = fdyn(t + dt / 2, x + dt / 2 * k2)
        k4 = fdyn(t + dt, x + dt * k3)
        xn = x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        xn[3:7] /= np.linalg.norm(xn[3:7])

        fr = q.k_thrust * np.maximum(x[13:17], 0.0) ** 2
        peak_f = max(peak_f, float(np.max(fr)))
        sumsq_f += float(np.sum(fr ** 2)); nf_ += 4

        # ---- gate scoring at the crossing of each gate plane
        while gate_done < len(course.gates) and xn[0] >= course.gates[gate_done] > x[0]:
            xg = course.gates[gate_done]
            frac = (xg - x[0]) / max(xn[0] - x[0], 1e-12)
            pc = x[0:3] + frac * (xn[0:3] - x[0:3])
            pg = course.p(xg)
            gate_err.append((float(abs(pc[1] - pg[1])), float(abs(pc[2] - pg[2]))))
            t_cross[gate_done] = t + frac * dt
            gate_done += 1

        R = quat_to_rot(xn[3:7])
        tilt = math.degrees(math.acos(float(np.clip((R @ np.array([0, 0, 1.0]))[2], -1, 1))))
        if tilt > max_tilt_deg or not np.all(np.isfinite(xn)) or xn[2] < 0.2:
            fail = f"loss of control at t={t:.3f}s (tilt {tilt:.0f} deg, z={xn[2]:.2f} m)"
            x = xn
            break
        x = xn
        hist.append(x.copy())
        t += dt
        if x[0] >= course.x_end:
            break

    t_finish = t if x[0] >= course.x_end else float("nan")
    done = len(gate_err) == len(course.gates) and fail is None and np.isfinite(t_finish)
    worst = max((max(a, b) for a, b in gate_err), default=float("inf"))
    s_path = course.arclength()
    return {
        "ok": bool(done and worst <= course.tol),
        "completed": bool(done),
        "worst_gate_err": float(worst),
        "gate_err": gate_err,
        "fail": fail,
        "t_finish": float(t_finish),
        "v_mean_path": float(s_path / t_finish) if np.isfinite(t_finish) else float("nan"),
        "v_mean_x": float(course.x_end / t_finish) if np.isfinite(t_finish) else float("nan"),
        "peak_rotor_thrust": peak_f,
        "rms_rotor_thrust": math.sqrt(sumsq_f / max(nf_, 1)),
        "sat_fraction": n_sat / max(n_ctl, 1),
        "failure_mode": ("loss_of_control" if fail else
                         ("gate_miss" if (done and worst > course.tol) else
                          ("incomplete" if not done else "none"))),
        "U": U, "dt": dt, "mode": mode, "s_look": s_look,
    }


def max_speed(q, ctl, course, dt=1e-3, mode="preview", s_look=12.0, lo=2.0, hi=22.0,
              iters=7, **kw):
    """Bisection on the reference speed U for the largest U that passes every gate."""
    if not run_course(q, ctl, course, lo, dt=dt, mode=mode, s_look=s_look, **kw)["ok"]:
        return {"U_max": float("nan"), "v_mean": float("nan"), "note": "fails at U_lo",
                "best": None}
    best = run_course(q, ctl, course, lo, dt=dt, mode=mode, s_look=s_look, **kw)
    a, b = lo, hi
    for _ in range(iters):
        mid = 0.5 * (a + b)
        r = run_course(q, ctl, course, mid, dt=dt, mode=mode, s_look=s_look, **kw)
        if r["ok"]:
            a, best = mid, r
        else:
            b = mid
    return {"U_max": a, "v_mean": best["v_mean_path"], "t_finish": best["t_finish"],
            "worst_gate_err": best["worst_gate_err"], "best": best}


def model_card(q, course, ctl=None):
    lines = ["MODEL CARD (SI units)",
             f"  plant        : {q.name}  m={q.mass} kg  J=diag{tuple(q.inertia)} kg m^2",
             f"  arm          : l={q.arm_length} m  beta={q.arm_angle_deg} deg",
             f"  rotors       : k_f={q.k_thrust} N/(rad/s)^2  k_m={q.k_torque} N m/(rad/s)^2"
             f"  f_i in [{q.thrust_min}, {q.thrust_max}] N",
             f"  actuator     : motor_tau={q.motor_tau*1e3:.2f} ms  slew_max={q.slew_max}",
             f"  aero (PLANT) : drag={q.enable_drag} kd={q.kd} kg/s  h_force={q.enable_h_force}"
             f" kh={q.k_h} kg/m",
             f"  hover        : T/W={q.hover()['thrust_to_weight']:.4f}  "
             f"a_max_horizontal={q.hover()['a_max_horizontal']:.3f} m/s^2  "
             f"omega_hover={q.hover()['omega_hover']:.2f} rad/s",
             f"  course       : y={course.A} sin(2pi x/{course.L}) m, z={course.z0} m, "
             f"x_end={course.x_end} m, {len(course.gates)} gates, tol={course.tol} m",
             f"  arc length   : {course.arclength():.3f} m",
             ]
    if ctl is not None:
        s = ctl.spec()
        lines += [f"  controller   : tau_imu={s['tau_imu']*1e3:.2f} ms  "
                  f"tau_vio={s['tau_vio']*1e3:.2f} ms  f_inner={s['f_inner']} Hz  "
                  f"f_outer={s['f_outer']} Hz",
                  f"                 w_rate={s['w_rate']:.3f} w_att={s['w_att']:.3f} "
                  f"w_vel={s['w_vel']:.3f} w_pos={s['w_pos']:.3f} rad/s  "
                  f"know_drag={s['know_drag']} lead={s['lead']}"]
    return "\n".join(lines)


if __name__ == "__main__":
    q = platform_sun2022()
    c = Slalom()
    ctl = Cascade(q)
    print(model_card(q, c, ctl))
    r = run_course(q, ctl, c, 10.0, dt=1e-3)
    print("smoke test U=10:", {k: r[k] for k in ("ok", "completed", "worst_gate_err",
                                                 "t_finish", "v_mean_path", "fail")})
