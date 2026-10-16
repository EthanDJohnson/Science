#!/usr/bin/env python3
"""Six-degree-of-freedom quadrotor plant with its actuator chain, in SI units.

WHAT IT COMPUTES
    Quadrotor(...)                  the plant: mass, diagonal inertia, X-arm geometry,
                                    thrust/drag-torque coefficients, per-rotor thrust limit,
                                    first-order motor lag + rotor-speed slew limit, linear
                                    drag and an h-force (rotor/blade-flapping) term, each
                                    switchable so its contribution can be isolated
    .wrench(omega_rotor)            forward map: four rotor speeds -> collective thrust T [N]
                                    and body torque tau [N m]
    .rotor_thrusts_from_wrench()    inverse map; RAISES ValueError when the four rotors cannot
                                    produce the commanded (T, tau) instead of returning a
                                    saturated (and therefore wrong) number
    .rotor_speeds_from_wrench()     the same, in rad/s
    .hover()                        hover equilibrium: T = m g, per-rotor thrust, hover rotor
                                    speed, thrust-to-weight, closed-form acceleration ceilings
    .dynamics(x, u)                 xdot for the 13-state rigid body (instantaneous thrust) or
                                    the 17-state plant (rotor speeds as states) when motor_tau>0
    .euler_dynamics(x12, u)         the same plant in a 12-state Euler parameterisation that
                                    control_tools.linearize can consume, with the input either
                                    the wrench [T, tau_x, tau_y, tau_z] or the four rotor speeds
    .hover_linearization()          analytic hover Jacobians (A, B) in that 12-state form
    .simulate(...)                  fixed-step RK4 with quaternion renormalisation
    .diagnostics(...)               conserved-quantity and known-limit checks on the integrator:
                                    quaternion-norm drift, torque-free |J omega| and rotational
                                    kinetic energy, free-fall closed form, RK4 order

MODEL AND FORMULAS
  Frames and attitude parameterisation (written down, because sign errors here are silent):
    World frame W is right-handed with +z UP; gravity is g_W = (0, 0, -g).
    Body frame B has +x forward, +y LEFT, +z up (so thrust acts along +z_B).
    Attitude is the unit quaternion q = (qw, qx, qy, qz), Hamilton convention, scalar first,
    mapping BODY vectors to WORLD vectors:  v_W = R(q) v_B,  with
        R(q) = [[1-2(y^2+z^2), 2(xy-wz),     2(xz+wy)    ],
                [2(xy+wz),     1-2(x^2+z^2), 2(yz-wx)    ],
                [2(xz-wy),     2(yz+wx),     1-2(x^2+y^2)]].
    Kinematics  qdot = 0.5 * q (x) (0, omega_B), omega_B in rad/s expressed in B.
    The Euler parameterisation used for linearisation is ZYX (yaw-pitch-roll):
    R = Rz(psi) Ry(theta) Rx(phi), with [phidot, thetadot, psidot] = T(phi, theta) omega_B.

  Rigid-body dynamics (NeuroBEM eq. 3, quoted in the selftest):
        pdot   = v
        vdot   = (1/m) R(q) (T z_B + f_aero_B) + g_W
        qdot   = 0.5 q (x) (0, omega_B)
        Jdot omega = tau_prop + tau_aero - omega x (J omega)      J = diag(Jx, Jy, Jz)

  Rotor map (X configuration).  Rotor i sits at body position
        r_i = (+-l cos beta, +-l sin beta, 0),  beta measured from the +x_B axis,
    numbered counter-clockwise seen from above starting front-right:
        1 front-right (+x,-y), 2 front-left (+x,+y), 3 rear-left (-x,+y), 4 rear-right (-x,-y),
    with spin signs sigma = (+1, -1, +1, -1); sigma_i = +1 means the rotor's angular velocity
    points along +z_B (counter-clockwise seen from above), so its reaction torque on the
    airframe points along -z_B.  Each rotor makes thrust f_i = k_f omega_i^2 along +z_B and a
    drag torque of magnitude k_m omega_i^2 about its own axis, so
        T     = sum_i f_i
        tau_x = sum_i y_i f_i      = l sin(beta) (-f1 +f2 +f3 -f4)
        tau_y = -sum_i x_i f_i     = l cos(beta) (-f1 -f2 +f3 +f4)
        tau_z = -sum_i sigma_i k_m omega_i^2 = (k_m/k_f)(-f1 +f2 -f3 +f4)
    The 4x4 matrix [T, tau]^T = M f is invertible for 0 < beta < 90 deg, k_f, k_m, l > 0; the
    inverse map solves it and then checks 0 <= f_i <= f_max.

  Actuator chain.  Commanded rotor speeds u (rad/s) reach the rotor through a first-order lag
  with time constant motor_tau and a slew limit on rotor speed:
        omega_r_dot = clip((u - omega_r)/motor_tau, -slew_max, +slew_max)      [rad/s^2]
    motor_tau = 0 removes the rotor states (13-state plant, instantaneous thrust).  The lag is
    on ROTOR SPEED, not on thrust: thrust then responds as omega^2, which matters above hover.

  Aerodynamics (switchable).  Body-frame force, with v_B = R^T v_W (zero wind):
        f_aero_B = (-kd_x vx, -kd_y vy, -kd_z vz + k_h (vx^2 + vy^2))
    the linear rotor-drag plus h-force/blade-flapping model of Sun et al. (quoted in the
    selftest).  enable_drag switches the linear part, enable_h_force the quadratic part, so
    each contribution can be isolated.  No aerodynamic torque model is included: the sources
    that measure it (NeuroBEM) do it with a blade-element or learned model, which is outside
    this calculator; omit it rather than invent a coefficient.

ASSUMPTIONS AND VALIDITY RANGE
    * Rigid airframe, rigid propellers, centre of mass at the body-frame origin, principal axes
      aligned with the body axes (diagonal J).  A real airframe's off-diagonal inertia is
      typically <5 per cent of the diagonal; this model drops it.
    * Fixed-pitch, unidirectional rotors: f_i >= 0.  Reversible thrust needs a different map.
    * Thrust quadratic in rotor speed with a constant k_f, i.e. static thrust at zero inflow.
      This is the standard identification at hover; at high axial or edgewise speed the true
      coefficient changes by tens of per cent (that is what the aero terms above partly
      absorb), so treat results above about 20 m/s as model-error-limited, not exact.
    * No rotor gyroscopic/inertial torque from rotor spin-up (the G2 omegadot_rotor term), no
      ground effect, no battery sag, no wind.
    * Small-angle validity: euler_dynamics raises ValueError at |pitch| > 85 deg (gimbal
      singularity of the ZYX chart); use the quaternion state there.
    * SI throughout the Python API: m kg, l m, J kg m^2, k_f N/(rad/s)^2, k_m N m/(rad/s)^2,
      omega rad/s, T N, tau N m, times s.  Rotor speeds in rpm only in printed output.

PYTHON USAGE
    import sys; sys.path.insert(0, "runs/<slug>/tools")
    from quadrotor import Quadrotor, platform_sun2022
    q = platform_sun2022()                 # published 0.75 kg research quadrotor
    h = q.hover()
    print(h["omega_hover"], h["thrust_to_weight"], h["a_max_horizontal"])
    f = q.rotor_thrusts_from_wrench(h["thrust_total"], [0.1, 0.0, 0.0])   # roll command
    x0 = q.hover_state(); out = q.simulate(x0, q.hover_input(), dt=1e-3, t_end=1.0)
    print(out["diagnostics"]["quat_norm_drift"])

COMMAND LINE
    python3 runs/<slug>/tools/quadrotor.py selftest
    python3 runs/<slug>/tools/quadrotor.py hover --mass 0.75kg --thrust-max 8.5N
    python3 runs/<slug>/tools/quadrotor.py step --tau 0.0391 --torque 0.1
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass, field
from typing import Callable, Sequence

import numpy as np

# --------------------------------------------------------------------------- toolkit imports
_HERE = os.path.dirname(os.path.abspath(__file__))
for _cand in (
    os.path.join(os.getcwd(), ".claude", "skills", "conundrum", "scripts"),
    os.path.abspath(os.path.join(_HERE, "..", "..", "..", ".claude", "skills", "conundrum", "scripts")),
):
    if os.path.isdir(_cand) and _cand not in sys.path:
        sys.path.insert(0, _cand)

try:  # units for the command line only; the Python API is plain SI floats
    from unit_tools import Q as _Q
except Exception:  # pragma: no cover
    _Q = None

try:
    import control_tools as _ct
except Exception:  # pragma: no cover
    _ct = None

G_STANDARD = 9.80665  # m/s^2, exact by definition (CIPM 1901 / SI standard gravity)


# --------------------------------------------------------------------------- quaternion utils
def quat_mul(a, b):
    """Hamilton product (w, x, y, z)."""
    aw, ax, ay, az = a
    bw, bx, by, bz = b
    return np.array([
        aw * bw - ax * bx - ay * by - az * bz,
        aw * bx + ax * bw + ay * bz - az * by,
        aw * by - ax * bz + ay * bw + az * bx,
        aw * bz + ax * by - ay * bx + az * bw,
    ])


def quat_to_rot(q):
    """Rotation matrix R with v_world = R v_body, q = (w, x, y, z), Hamilton, scalar first."""
    w, x, y, z = q / np.linalg.norm(q)
    return np.array([
        [1 - 2 * (y * y + z * z), 2 * (x * y - w * z), 2 * (x * z + w * y)],
        [2 * (x * y + w * z), 1 - 2 * (x * x + z * z), 2 * (y * z - w * x)],
        [2 * (x * z - w * y), 2 * (y * z + w * x), 1 - 2 * (x * x + y * y)],
    ])


def euler_zyx_to_rot(phi, theta, psi):
    """R = Rz(psi) Ry(theta) Rx(phi): body -> world, roll phi, pitch theta, yaw psi."""
    cphi, sphi = math.cos(phi), math.sin(phi)
    cth, sth = math.cos(theta), math.sin(theta)
    cps, sps = math.cos(psi), math.sin(psi)
    return np.array([
        [cps * cth, cps * sth * sphi - sps * cphi, cps * sth * cphi + sps * sphi],
        [sps * cth, sps * sth * sphi + cps * cphi, sps * sth * cphi - cps * sphi],
        [-sth, cth * sphi, cth * cphi],
    ])


def euler_zyx_rates(phi, theta, omega_body):
    """[phidot, thetadot, psidot] from body rates, ZYX chart."""
    cphi, sphi = math.cos(phi), math.sin(phi)
    cth, tth = math.cos(theta), math.tan(theta)
    Tm = np.array([
        [1.0, sphi * tth, cphi * tth],
        [0.0, cphi, -sphi],
        [0.0, sphi / cth, cphi / cth],
    ])
    return Tm @ np.asarray(omega_body, dtype=float)


# --------------------------------------------------------------------------- the plant
@dataclass
class Quadrotor:
    """A quadrotor plant.  All quantities SI (see module docstring for conventions)."""

    mass: float = 0.75                      # kg
    inertia: tuple = (2.5e-3, 2.1e-3, 4.3e-3)   # kg m^2, diag(Jx, Jy, Jz)
    arm_length: float = 0.14                # m, hub to rotor axis
    arm_angle_deg: float = 56.0             # deg from +x_B to the arm, X configuration
    k_thrust: float = 1.51e-6               # N/(rad/s)^2   f_i = k_thrust omega_i^2
    k_torque: float = 2.37e-8               # N m/(rad/s)^2 drag torque of one rotor
    thrust_max: float = 8.5                 # N per rotor
    thrust_min: float = 0.0                 # N per rotor (unidirectional rotors)
    motor_tau: float = 0.0                  # s, first-order rotor-speed lag; 0 = instantaneous
    slew_max: float = float("inf")          # rad/s^2, rotor-speed slew-rate limit
    kd: tuple = (0.26, 0.28, 0.42)          # kg/s, linear body-frame rotor drag
    k_h: tuple = 0.01                       # kg/m, h-force / blade-flapping term
    enable_drag: bool = True
    enable_h_force: bool = True
    enable_gyroscopic: bool = True          # the -omega x (J omega) term
    g: float = G_STANDARD                   # m/s^2
    name: str = "generic"

    # ---------------------------------------------------------------- validation
    def __post_init__(self):
        if not (self.mass > 0):
            raise ValueError(f"mass must be > 0, got {self.mass}")
        J = np.asarray(self.inertia, dtype=float)
        if J.shape != (3,) or np.any(J <= 0):
            raise ValueError(f"inertia must be three positive diagonal entries, got {self.inertia}")
        if not (J[0] + J[1] >= J[2] - 1e-12 and J[1] + J[2] >= J[0] - 1e-12
                and J[0] + J[2] >= J[1] - 1e-12):
            raise ValueError(
                "inertia violates the triangle inequality Ji + Jj >= Jk, so no rigid body "
                f"has it: {self.inertia}")
        if not (0.0 < self.arm_angle_deg < 90.0):
            raise ValueError(f"arm_angle_deg must be in (0, 90), got {self.arm_angle_deg}")
        if not (self.arm_length > 0 and self.k_thrust > 0 and self.k_torque > 0):
            raise ValueError("arm_length, k_thrust, k_torque must all be > 0")
        if self.motor_tau < 0:
            raise ValueError(f"motor_tau must be >= 0, got {self.motor_tau}")
        if self.slew_max <= 0:
            raise ValueError(f"slew_max must be > 0, got {self.slew_max}")
        if self.thrust_max <= self.thrust_min:
            raise ValueError("thrust_max must exceed thrust_min")
        if self.thrust_max * 4.0 <= self.mass * self.g:
            raise ValueError(
                f"four rotors at thrust_max = {4*self.thrust_max:.3f} N cannot hold the weight "
                f"{self.mass*self.g:.3f} N: this vehicle cannot hover")
        self._J = J
        self._Jinv = 1.0 / J

    # ---------------------------------------------------------------- geometry and maps
    @property
    def omega_max(self) -> float:
        """Rotor speed at thrust_max, rad/s."""
        return math.sqrt(self.thrust_max / self.k_thrust)

    @property
    def omega_min(self) -> float:
        return math.sqrt(max(self.thrust_min, 0.0) / self.k_thrust)

    @property
    def spin_dirs(self) -> np.ndarray:
        """sigma_i = +1 if rotor i spins counter-clockwise seen from above (+z_B)."""
        return np.array([+1.0, -1.0, +1.0, -1.0])

    def rotor_positions(self) -> np.ndarray:
        """(4, 3) rotor hub positions in the body frame, m."""
        b = math.radians(self.arm_angle_deg)
        cx, sy = self.arm_length * math.cos(b), self.arm_length * math.sin(b)
        return np.array([[cx, -sy, 0.0], [cx, sy, 0.0], [-cx, sy, 0.0], [-cx, -sy, 0.0]])

    def mix_matrix(self) -> np.ndarray:
        """(4, 4) M with [T, tau_x, tau_y, tau_z]^T = M f, f = per-rotor thrusts (N)."""
        r = self.rotor_positions()
        c = self.k_torque / self.k_thrust  # m, torque per unit thrust about z
        M = np.zeros((4, 4))
        M[0, :] = 1.0
        M[1, :] = r[:, 1]
        M[2, :] = -r[:, 0]
        M[3, :] = -self.spin_dirs * c
        return M

    def wrench(self, omega_rotor) -> dict:
        """Forward map: rotor speeds (rad/s) -> collective thrust (N) and body torque (N m)."""
        w = np.asarray(omega_rotor, dtype=float).reshape(4)
        if np.any(w < -1e-12):
            raise ValueError(f"rotor speeds must be >= 0 (unidirectional rotors), got {w}")
        f = self.k_thrust * w ** 2
        v = self.mix_matrix() @ f
        return {"thrust": float(v[0]), "torque": v[1:].copy(), "rotor_thrusts": f}

    def rotor_thrusts_from_wrench(self, thrust: float, torque, tol: float = 1e-9) -> np.ndarray:
        """Inverse map -> per-rotor thrusts (N).  Raises ValueError if not producible."""
        b = np.array([float(thrust), *np.asarray(torque, dtype=float).reshape(3)])
        f = np.linalg.solve(self.mix_matrix(), b)
        lo, hi = self.thrust_min - tol, self.thrust_max + tol
        if np.any(f < lo) or np.any(f > hi):
            raise ValueError(
                "command (T = %.4f N, tau = [%.4f, %.4f, %.4f] N m) needs per-rotor thrusts "
                "%s N, outside the achievable [%.3f, %.3f] N: the rotors cannot produce it"
                % (b[0], b[1], b[2], b[3], np.array2string(f, precision=4), self.thrust_min,
                   self.thrust_max))
        return np.clip(f, self.thrust_min, self.thrust_max)

    def rotor_speeds_from_wrench(self, thrust: float, torque) -> np.ndarray:
        """Inverse map -> rotor speeds (rad/s).  Raises ValueError if not producible."""
        f = self.rotor_thrusts_from_wrench(thrust, torque)
        return np.sqrt(np.maximum(f, 0.0) / self.k_thrust)

    def wrench_feasible(self, thrust: float, torque) -> bool:
        try:
            self.rotor_thrusts_from_wrench(thrust, torque)
            return True
        except ValueError:
            return False

    # ---------------------------------------------------------------- equilibrium, ceilings
    def hover(self) -> dict:
        """Hover equilibrium and the closed-form acceleration ceilings."""
        W = self.mass * self.g
        f_h = W / 4.0
        if f_h > self.thrust_max:
            raise ValueError("cannot hover: hover thrust per rotor exceeds thrust_max")
        w_h = math.sqrt(f_h / self.k_thrust)
        twr = 4.0 * self.thrust_max / W
        return {
            "thrust_total": W,                       # N, = m g exactly
            "thrust_per_rotor": f_h,                 # N
            "omega_hover": w_h,                      # rad/s
            "rpm_hover": w_h * 60.0 / (2 * math.pi),
            "throttle_fraction": f_h / self.thrust_max,
            "thrust_to_weight": twr,
            "a_max_thrust": twr * self.g,            # m/s^2, |thrust| / m at full throttle
            "a_max_vertical": (twr - 1.0) * self.g,  # m/s^2, climbing straight up
            "a_max_horizontal": self.g * math.sqrt(max(twr ** 2 - 1.0, 0.0)),
            "tilt_for_max_horizontal_deg": math.degrees(math.acos(1.0 / twr)),
            "torque_max_roll": self.arm_length * math.sin(math.radians(self.arm_angle_deg))
                               * 2.0 * (self.thrust_max - self.thrust_min),
            "alpha_max_roll": self.arm_length * math.sin(math.radians(self.arm_angle_deg))
                              * 2.0 * (self.thrust_max - self.thrust_min) / self._J[0],
        }

    def hover_state(self, yaw: float = 0.0, position=(0.0, 0.0, 0.0)) -> np.ndarray:
        """Equilibrium state vector (13 or 17 entries, see state_dim)."""
        q = np.array([math.cos(yaw / 2), 0.0, 0.0, math.sin(yaw / 2)])
        x = np.concatenate([np.asarray(position, float), q, np.zeros(3), np.zeros(3)])
        if self.motor_tau > 0:
            x = np.concatenate([x, np.full(4, self.hover()["omega_hover"])])
        return x

    def hover_input(self) -> np.ndarray:
        """Equilibrium commanded rotor speeds, rad/s."""
        return np.full(4, self.hover()["omega_hover"])

    @property
    def state_dim(self) -> int:
        return 17 if self.motor_tau > 0 else 13

    # ---------------------------------------------------------------- aerodynamics
    def aero_force_body(self, v_body) -> np.ndarray:
        """Body-frame aerodynamic force, N (zero wind)."""
        v = np.asarray(v_body, dtype=float).reshape(3)
        f = np.zeros(3)
        if self.enable_drag:
            f -= np.asarray(self.kd, dtype=float) * v
        if self.enable_h_force:
            f[2] += float(self.k_h) * (v[0] ** 2 + v[1] ** 2)
        return f

    # ---------------------------------------------------------------- dynamics
    def dynamics(self, x, u, clip_commands: bool = True) -> np.ndarray:
        """xdot for the quaternion state.

        x = [p(3), q(4), v_world(3), omega_body(3)]              if motor_tau == 0
        x = [p(3), q(4), v_world(3), omega_body(3), omega_r(4)]  if motor_tau > 0
        u = four commanded rotor speeds, rad/s (clipped into [omega_min, omega_max] when
        clip_commands, which is what an ESC does; set it False to raise instead).
        """
        x = np.asarray(x, dtype=float)
        if x.shape != (self.state_dim,):
            raise ValueError(f"state must have {self.state_dim} entries, got {x.shape}")
        u = np.asarray(u, dtype=float).reshape(4)
        if clip_commands:
            u = np.clip(u, self.omega_min, self.omega_max)
        elif np.any(u < self.omega_min - 1e-9) or np.any(u > self.omega_max + 1e-9):
            raise ValueError(f"commanded rotor speeds {u} outside "
                             f"[{self.omega_min:.2f}, {self.omega_max:.2f}] rad/s")

        p, q, v, om = x[0:3], x[3:7], x[7:10], x[10:13]
        wr = x[13:17] if self.state_dim == 17 else u

        R = quat_to_rot(q)
        w = self.wrench(np.maximum(wr, 0.0))
        T, tau = w["thrust"], w["torque"]

        v_body = R.T @ v
        f_b = np.array([0.0, 0.0, T]) + self.aero_force_body(v_body)
        vdot = R @ f_b / self.mass + np.array([0.0, 0.0, -self.g])
        qdot = 0.5 * quat_mul(q, np.array([0.0, *om]))
        Jom = self._J * om
        rhs = tau - (np.cross(om, Jom) if self.enable_gyroscopic else 0.0)
        omdot = self._Jinv * rhs

        out = [v, qdot, vdot, omdot]
        if self.state_dim == 17:
            wdot = np.clip((u - wr) / self.motor_tau, -self.slew_max, self.slew_max)
            # a rotor cannot be driven below zero speed or above omega_max
            wdot = np.where((wr <= 0.0) & (wdot < 0), 0.0, wdot)
            wdot = np.where((wr >= self.omega_max) & (wdot > 0), 0.0, wdot)
            out.append(wdot)
        return np.concatenate(out)

    # ------------------------------------------------- 12-state Euler form for linearize
    def euler_dynamics(self, x, u, input_kind: str = "wrench") -> np.ndarray:
        """xdot for x = [p(3), v_world(3), (phi, theta, psi), omega_body(3)].

        input_kind "wrench": u = [T, tau_x, tau_y, tau_z]  (N, N m)
        input_kind "rotor_speed": u = four rotor speeds (rad/s)
        Motor lag is NOT part of this form (it is a separate first-order block, which is how
        control_tools.linearize and loop_margins want it); use dynamics() for the full plant.
        """
        x = np.asarray(x, dtype=float).reshape(12)
        u = np.asarray(u, dtype=float).reshape(4)
        p, v, eul, om = x[0:3], x[3:6], x[6:9], x[9:12]
        phi, theta, psi = eul
        if abs(theta) > math.radians(85.0):
            raise ValueError(f"pitch {math.degrees(theta):.1f} deg is outside the ZYX chart's "
                             "validity (|pitch| <= 85 deg); use the quaternion state")
        if input_kind == "wrench":
            T, tau = float(u[0]), u[1:].copy()
        elif input_kind == "rotor_speed":
            w = self.wrench(np.clip(u, self.omega_min, self.omega_max))
            T, tau = w["thrust"], w["torque"]
        else:
            raise ValueError("input_kind must be 'wrench' or 'rotor_speed'")
        R = euler_zyx_to_rot(phi, theta, psi)
        f_b = np.array([0.0, 0.0, T]) + self.aero_force_body(R.T @ v)
        vdot = R @ f_b / self.mass + np.array([0.0, 0.0, -self.g])
        euldot = euler_zyx_rates(phi, theta, om)
        Jom = self._J * om
        rhs = tau - (np.cross(om, Jom) if self.enable_gyroscopic else 0.0)
        return np.concatenate([v, vdot, euldot, self._Jinv * rhs])

    def euler_state_dynamics(self, input_kind: str = "wrench") -> Callable:
        """f(x, u) closure for control_tools.linearize."""
        return lambda x, u: self.euler_dynamics(x, u, input_kind=input_kind)

    def hover_equilibrium_euler(self, input_kind: str = "wrench"):
        """(x0, u0) for the 12-state Euler form at hover, yaw = 0."""
        x0 = np.zeros(12)
        if input_kind == "wrench":
            u0 = np.array([self.mass * self.g, 0.0, 0.0, 0.0])
        else:
            u0 = self.hover_input()
        return x0, u0

    def hover_linearization(self) -> dict:
        """Analytic hover Jacobians of euler_dynamics with input_kind='wrench', yaw = 0.

        With drag off, the standard small-perturbation hover model:
            xddot = g theta,  yddot = -g phi,  zddot = dT/m,
            phiddot = tau_x/Jx, thetaddot = tau_y/Jy, psiddot = tau_z/Jz.
        Linear drag adds -kd_i/m on the matching velocity diagonal.
        """
        A = np.zeros((12, 12))
        B = np.zeros((12, 4))
        A[0:3, 3:6] = np.eye(3)
        A[3, 7] = self.g        # d xddot / d theta
        A[4, 6] = -self.g       # d yddot / d phi
        if self.enable_drag:
            kd = np.asarray(self.kd, dtype=float)
            A[3, 3], A[4, 4], A[5, 5] = -kd[0] / self.mass, -kd[1] / self.mass, -kd[2] / self.mass
        A[6:9, 9:12] = np.eye(3)
        B[5, 0] = 1.0 / self.mass
        B[9, 1] = self._Jinv[0]
        B[10, 2] = self._Jinv[1]
        B[11, 3] = self._Jinv[2]
        return {"A": A, "B": B,
                "states": ["x", "y", "z", "vx", "vy", "vz", "phi", "theta", "psi", "p", "q", "r"],
                "inputs": ["T", "tau_x", "tau_y", "tau_z"]}

    # ---------------------------------------------------------------- integration
    def simulate(self, x0, u, dt: float, t_end: float, renormalise: bool = True,
                 clip_commands: bool = True) -> dict:
        """Fixed-step RK4 on the quaternion state.  u is an array or a callable u(t, x)."""
        if dt <= 0 or t_end <= 0:
            raise ValueError("dt and t_end must be > 0")
        n = int(round(t_end / dt))
        if n < 1:
            raise ValueError("t_end must be at least one step")
        uf = u if callable(u) else (lambda t, x, _u=np.asarray(u, float): _u)
        x = np.asarray(x0, dtype=float).copy()
        if x.shape != (self.state_dim,):
            raise ValueError(f"x0 must have {self.state_dim} entries, got {x.shape}")
        X = np.empty((n + 1, x.size))
        tt = np.arange(n + 1) * dt
        X[0] = x
        f = lambda t, y: self.dynamics(y, uf(t, y), clip_commands=clip_commands)
        for i in range(n):
            t = tt[i]
            k1 = f(t, x)
            k2 = f(t + dt / 2, x + dt / 2 * k1)
            k3 = f(t + dt / 2, x + dt / 2 * k2)
            k4 = f(t + dt, x + dt * k3)
            x = x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
            if renormalise:
                x[3:7] /= np.linalg.norm(x[3:7])
            X[i + 1] = x
        qn = np.linalg.norm(X[:, 3:7], axis=1)
        return {"t": tt, "x": X, "dt": dt,
                "diagnostics": {"quat_norm_drift": float(np.max(np.abs(qn - 1.0)))}}

    def diagnostics(self, dt: float = 1e-3, t_end: float = 2.0, rk4_dt: float = 0.02) -> dict:
        """Conserved-quantity and known-limit checks on the integrator.

        1. torque-free rigid body (thrust and drag off): |J omega| in WORLD axes and the
           rotational kinetic energy 0.5 omega^T J omega are exact invariants of Euler's
           equations, so their drift measures the integrator.
        2. free fall with zero thrust reduces to Newtonian ballistics z = z0 + vz0 t - g t^2/2.
        3. RK4 convergence order from Richardson comparison of dt and dt/2.
        """
        free = self.variant(enable_drag=False, enable_h_force=False, thrust_min=0.0,
                            motor_tau=0.0)
        x0 = free.hover_state()
        x0[10:13] = np.array([3.0, -2.0, 1.5])  # rad/s, torque-free tumble
        out = free.simulate(x0, np.zeros(4), dt, t_end)
        X = out["x"]
        J = free._J
        Lw, Ek = [], []
        for row in X:
            R = quat_to_rot(row[3:7])
            om = row[10:13]
            Lw.append(np.linalg.norm(R @ (J * om)))
            Ek.append(0.5 * float(om @ (J * om)))
        Lw, Ek = np.array(Lw), np.array(Ek)
        # free fall
        x1 = free.hover_state(position=(0.0, 0.0, 100.0))
        o1 = free.simulate(x1, np.zeros(4), dt, 1.0)
        z_num = o1["x"][-1, 2]
        z_exact = 100.0 - 0.5 * free.g * 1.0 ** 2
        # RK4 order by self-convergence: order = log2(|x(h) - x(h/2)| / |x(h/2) - x(h/4)|).
        # The base step must be coarse enough that the truncation error is well above double
        # roundoff: at dt = 1e-3 on this tumble the difference is already ~1e-14 and the
        # estimate collapses to the roundoff floor (it reads ~3, not 4), which is a property
        # of floating point, not of the integrator.
        hb = max(rk4_dt, 1e-3)
        oc = free.simulate(x0, np.zeros(4), hb, 0.2)
        of = free.simulate(x0, np.zeros(4), hb / 2, 0.2)
        oh = free.simulate(x0, np.zeros(4), hb / 4, 0.2)
        d1 = np.linalg.norm(oc["x"][-1] - of["x"][-1])
        d2 = np.linalg.norm(of["x"][-1] - oh["x"][-1])
        order = math.log2(d1 / d2) if d2 > 0 else float("inf")
        return {
            "angular_momentum_drift": float(np.max(np.abs(Lw - Lw[0])) / abs(Lw[0])),
            "rotational_energy_drift": float(np.max(np.abs(Ek - Ek[0])) / abs(Ek[0])),
            "quat_norm_drift": out["diagnostics"]["quat_norm_drift"],
            "free_fall_error": float(abs(z_num - z_exact)),
            "rk4_order": float(order),
        }

    def _spec(self) -> dict:
        """The constructor arguments of this plant (so variants can be built from it)."""
        keys = ("mass", "inertia", "arm_length", "arm_angle_deg", "k_thrust", "k_torque",
                "thrust_max", "thrust_min", "motor_tau", "slew_max", "kd", "k_h",
                "enable_drag", "enable_h_force", "enable_gyroscopic", "g", "name")
        return {k: getattr(self, k) for k in keys}

    def variant(self, **changes) -> "Quadrotor":
        """A copy with some parameters changed (for one-at-a-time sensitivity studies)."""
        return Quadrotor(**{**self._spec(), **changes})


# --------------------------------------------------------------------------- platforms
def platform_sun2022(**changes) -> Quadrotor:
    """The 0.75 kg research quadrotor of Sun, Romero, Foehn, Kaufmann and Scaramuzza,

    "A Comparative Study of Nonlinear MPC and Differential-Flatness-based Control for
    Quadrotor Agile Flight", IEEE T-RO 38 (2022) 3357-3373, arXiv:2109.01365, TABLE II
    ("Quadrotor Configurations"), quoted verbatim from the arXiv PDF p. 7:
        "m [kg] 0.75   l [m] 0.14   b [deg] 56   I v [gm2] diag(2.5, 2.1, 4.3)
         (umin,u max) [N] (0, 8.5)   cq [Nm2] 2.37e-8   ct [N2] 1.51e-6
         [kd,x, kd,y, kd,z] [kg/s] (0.26, 0.28, 0.42)   kh [kg/m] 0.01"
    (the table's "[Nm2]" and "[N2]" are N m s^2/rad^2 and N s^2/rad^2, i.e. coefficients of
    omega^2 with omega in rad/s; the hover rotor speed below confirms the reading).
    The motor time constant is not in that table; the default here is the 39.1 ms measured on
    the closely related Agilicious platform (Foehn et al., Science Robotics 7 (2022) eabl6259,
    arXiv:2307.06100 p. 6: "the motor's time constant of 39.1ms, which dictates the actuator
    bandwidth limitations").
    """
    base = dict(mass=0.75, inertia=(2.5e-3, 2.1e-3, 4.3e-3), arm_length=0.14,
                arm_angle_deg=56.0, k_thrust=1.51e-6, k_torque=2.37e-8,
                thrust_max=8.5, thrust_min=0.0, motor_tau=0.0391,
                kd=(0.26, 0.28, 0.42), k_h=0.01, name="Sun2022-0.75kg")
    return Quadrotor(**{**base, **changes})


# --------------------------------------------------------------------------- selftest
def selftest(verbose: bool = True) -> bool:
    ok = [True]
    n = [0]

    def check(name, got, want, tol, note=""):
        n[0] += 1
        good = abs(got - want) <= tol
        ok[0] &= bool(good)
        if verbose:
            print(f"  [{'ok ' if good else 'FAIL'}] {name}: got {got:.8g}, want {want:.8g} "
                  f"(tol {tol:.2g}){(' - ' + note) if note else ''}")
        return good

    def check_true(name, cond, note=""):
        n[0] += 1
        ok[0] &= bool(cond)
        if verbose:
            print(f"  [{'ok ' if cond else 'FAIL'}] {name}{(' - ' + note) if note else ''}")
        return bool(cond)

    q = platform_sun2022()
    h = q.hover()

    if verbose:
        print("1. Hover equilibrium: thrust = m g (Newton's second law, exact definition)")
    # REFERENCE: hand arithmetic from Sun et al. TABLE II (quoted in platform_sun2022):
    #   m g = 0.75 kg * 9.80665 m/s^2 = 7.3549875 N; per rotor 1.8387469 N;
    #   omega_hover = sqrt(1.8387469 / 1.51e-6) = sqrt(1217713.2) = 1103.50 rad/s,
    #   = 1103.50 * 60 / (2 pi) = 10537.6 rpm.
    # (An earlier draft of this comment wrote 1103.44 rad/s from a slip in the long division;
    # the reference was wrong, not the code, so it is corrected here rather than tolerated.)
    # 1103 rad/s (about 10500 rpm) is the right size for a 5-inch racing propeller at hover,
    # which is the check that TABLE II's "ct [N2]" is per (rad/s)^2 and not per rpm^2: read as
    # rpm^2 it would give a hover speed of 1103 rpm, which no 5-inch rotor can hover a 0.75 kg
    # vehicle on.
    check("hover thrust [N]", h["thrust_total"], 0.75 * 9.80665, 1e-9)
    check("hover thrust per rotor [N]", h["thrust_per_rotor"], 1.8387469, 1e-6)
    check("hover rotor speed [rad/s]", h["omega_hover"], 1103.50, 0.02)
    check("hover rotor speed [rpm]", h["rpm_hover"], 10537.6, 0.5)
    # the hover state must be an equilibrium of the nonlinear plant: xdot = 0 but for position
    xd = q.dynamics(q.hover_state(), q.hover_input())
    check("hover residual |xdot| (v, q, omega, rotors) [SI]",
          float(np.linalg.norm(np.concatenate([xd[3:13], xd[13:17]]))), 0.0, 1e-12)

    if verbose:
        print("2. Thrust-to-weight -> acceleration ceilings (closed form) and the published TWR")
    # REFERENCE: Sun et al. TABLE II gives per-rotor (umin, umax) = (0, 8.5) N, so by hand
    #   TWR = 4 * 8.5 / (0.75 * 9.80665) = 34 / 7.3549875 = 4.622713,
    #   a_max         = T_max/m = 34/0.75 = 45.333333 m/s^2 (= TWR * g),
    #   a_max_vertical  = a_max - g = 45.333333 - 9.80665 = 35.526683 m/s^2,
    #   a_max_horizontal = sqrt(a_max^2 - g^2) = sqrt(2055.1111 - 96.17038)
    #                    = sqrt(1958.9407) = 44.259922 m/s^2 (= g sqrt(TWR^2 - 1)).
    # (An earlier draft evaluated these from the ROUNDED TWR = 4.6227 and so quoted 45.3407,
    # 35.534 and 44.2915; the references were wrong in the fourth digit, not the code.)
    # The same paper's abstract/Fig. 1 caption reports flights "with speeds up to 20 m/s (i.e.,
    # 72 km/h) and accelerations up to 5g" (arXiv:2109.01365 p. 1), which must sit between
    # (TWR-1) g = 3.62 g (pure climb) and (TWR+1) g = 5.62 g (thrust plus gravity): it does.
    check("thrust-to-weight", h["thrust_to_weight"], 4.622713, 1e-5)
    check("a_max from thrust [m/s^2]", h["a_max_thrust"], 45.333333, 1e-5)
    check("a_max vertical [m/s^2]", h["a_max_vertical"], 35.526683, 1e-5)
    check("a_max horizontal [m/s^2]", h["a_max_horizontal"], 44.259922, 1e-4)
    check_true("measured 5 g is within [(TWR-1) g, (TWR+1) g]",
               h["thrust_to_weight"] - 1.0 <= 5.0 <= h["thrust_to_weight"] + 1.0,
               "Sun et al. report accelerations up to 5g on this platform")
    # the ceilings must also come out of the nonlinear plant, not just the formula
    qd = q.variant(motor_tau=0.0, enable_drag=False, enable_h_force=False)
    x0 = qd.hover_state()
    full = np.full(4, qd.omega_max)
    xd = qd.dynamics(x0, full)
    check("plant vertical accel at full throttle [m/s^2]", float(xd[9]), h["a_max_vertical"], 1e-9)
    # tilt by acos(1/TWR) about +y (pitch up) and the horizontal accel must be g sqrt(TWR^2-1)
    th = math.acos(1.0 / h["thrust_to_weight"])
    xt = qd.hover_state()
    xt[3:7] = np.array([math.cos(th / 2), 0.0, math.sin(th / 2), 0.0])
    xdt = qd.dynamics(xt, full)
    check("plant horizontal accel at optimal tilt [m/s^2]", float(xdt[7]),
          h["a_max_horizontal"], 1e-7)
    check("plant vertical accel at optimal tilt [m/s^2]", float(xdt[9]), 0.0, 1e-7)

    if verbose:
        print("3. Attitude step with motor lag against the analytic lagged double integrator")
    # The differential command delta = (-d, +d, +d, -d) rad/s about the hover speed makes the
    # omega^2 cross terms cancel exactly (sum of signs = 0), so with a first-order rotor lag
    #   tau_x(t) = tau_bar (1 - e^{-t/tm}),  tau_bar = 8 l sin(beta) k_f omega_h d,
    # and tau_y = tau_z = 0.  A pure roll keeps omega x J omega = 0, so the closed form is
    #   phi(t) = (tau_bar/Jx) (t^2/2 - tm t + tm^2 (1 - e^{-t/tm})),
    # the step response of a first-order lag into a double integrator (e.g. Franklin, Powell
    # and Emami-Naeini, Feedback Control of Dynamic Systems, ch. 3: the response of 1/s^2
    # driven by a lagged step is the convolution above).  This is the reference; the plant is
    # integrated numerically and must match it.
    tm = 0.0391  # s, Agilicious measured motor time constant (quoted in platform_sun2022)
    qm = q.variant(motor_tau=tm, enable_drag=False, enable_h_force=False, slew_max=1e12)
    d = 20.0     # rad/s differential command
    b = math.radians(qm.arm_angle_deg)
    tau_bar = 8.0 * qm.arm_length * math.sin(b) * qm.k_thrust * qm.hover()["omega_hover"] * d
    u = qm.hover_input() + np.array([-d, d, d, -d])
    sim = qm.simulate(qm.hover_state(), u, dt=2e-5, t_end=0.2)
    qf = sim["x"][-1, 3:7]
    phi_num = 2.0 * math.atan2(qf[1], qf[0])  # roll from the quaternion (pure x rotation)
    t_end = 0.2
    phi_ref = (tau_bar / qm._J[0]) * (t_end ** 2 / 2 - tm * t_end
                                      + tm ** 2 * (1 - math.exp(-t_end / tm)))
    check("roll after 0.2 s with 39.1 ms lag [rad]", phi_num, phi_ref, 1e-6,
          f"tau_bar = {tau_bar:.5f} N m")
    check("roll rate after 0.2 s [rad/s]", float(sim["x"][-1, 10]),
          (tau_bar / qm._J[0]) * (t_end - tm * (1 - math.exp(-t_end / tm))), 1e-6)
    check_true("no parasitic pitch/yaw torque from a pure roll command",
               abs(qm.wrench(u)["torque"][1]) < 1e-12 and abs(qm.wrench(u)["torque"][2]) < 1e-12)
    # Slew limit: with the lag much faster than the ramp, a rotor-speed command above the limit
    # must be followed at exactly slew_max, so omega_r(t) = omega_h + slew_max t until it
    # reaches the command.  Closed form (ramp, not exponential): with slew_max = 2000 rad/s^2
    # and a 200 rad/s step, after 50 ms the rotor is at omega_h + 100 rad/s.
    qsl = q.variant(motor_tau=1e-4, slew_max=2000.0, enable_drag=False, enable_h_force=False)
    big = qsl.hover_input() + np.array([-200.0, 200.0, 200.0, -200.0])
    ssl = qsl.simulate(qsl.hover_state(), big, dt=1e-5, t_end=0.05)
    check("rotor speed after 50 ms at a 2000 rad/s^2 slew limit [rad/s]",
          float(ssl["x"][-1, 14]), qsl.hover()["omega_hover"] + 100.0, 0.2,
          "exact ramp; the 0.2 rad/s allowance is the 1e-4 s lag at the start of the ramp")

    if verbose:
        print("4. motor_tau -> 0 reduces to the instantaneous-thrust case (required limit)")
    # Known limit: lim_{tm->0} phi(t) = tau_bar t^2 / (2 Jx), the undelayed double integrator.
    phi_inst = tau_bar * t_end ** 2 / (2 * qm._J[0])
    q0 = q.variant(motor_tau=0.0, enable_drag=False, enable_h_force=False)
    s0 = q0.simulate(q0.hover_state(), u, dt=2e-5, t_end=t_end)
    qf0 = s0["x"][-1, 3:7]
    check("roll after 0.2 s, instantaneous thrust [rad]",
          2.0 * math.atan2(qf0[1], qf0[0]), phi_inst, 1e-6)
    # The lag costs exactly phi_inst - phi(tm) = (tau_bar/Jx)(tm t - tm^2 (1 - e^{-t/tm})),
    # which -> 0 as tm -> 0 and is asymptotically (tau_bar/Jx) tm t, i.e. FIRST ORDER in tm.
    # Both statements are checked: the deficit against its closed form at each tm, and the
    # slope (deficit / tm) converging to (tau_bar/Jx) t = the first-order coefficient.
    slope_ref = (tau_bar / qm._J[0]) * t_end
    for tms in (4e-3, 1e-3, 2.5e-4):
        qs = q.variant(motor_tau=tms, enable_drag=False, enable_h_force=False, slew_max=1e12)
        ss = qs.simulate(qs.hover_state(), u, dt=min(2e-5, tms / 20), t_end=t_end)
        qfs = ss["x"][-1, 3:7]
        err = abs(2.0 * math.atan2(qfs[1], qfs[0]) - phi_inst)
        exact = (tau_bar / qs._J[0]) * (tms * t_end - tms ** 2 * (1 - math.exp(-t_end / tms)))
        check(f"lag deficit at motor_tau = {1e3*tms:g} ms [rad]", err, exact, 1e-8)
        # first-order convergence: deficit/tm -> slope_ref with a relative error ~ tm/t
        check(f"deficit/motor_tau at {1e3*tms:g} ms [rad/s]", err / tms, slope_ref,
              1.1 * slope_ref * tms / t_end,
              "tolerance is the O(tm/t) term of the expansion, stated not loosened")

    if verbose:
        print("5. Closed-loop small-angle attitude response against the textbook second order")
    # REFERENCE: a second-order system phiddot + 2 zeta wn phidot + wn^2 phi = 0 released from
    # phi(0) = phi0 has the standard underdamped solution
    #   phi(t) = phi0 e^{-zeta wn t} [cos(wd t) + (zeta/sqrt(1-zeta^2)) sin(wd t)], wd = wn sqrt(1-zeta^2)
    # (Ogata, Modern Control Engineering, 5th ed., ch. 5, "Transient response of second-order
    # systems"), with peak |phi| overshoot of the velocity-free release and zero crossing at
    # wd t = pi - atan(sqrt(1-zeta^2)/zeta).  Here the torque that realises it is produced
    # through the rotor map: tau_x = -Jx (wn^2 phi + 2 zeta wn phidot), inverted to rotor speeds.
    wn, zeta = 30.0, 0.7  # rad/s, -
    qc = q.variant(motor_tau=0.0, enable_drag=False, enable_h_force=False)
    phi0 = 0.02  # rad, small angle so the linearisation is tight
    xc = qc.hover_state()
    xc[3:7] = np.array([math.cos(phi0 / 2), math.sin(phi0 / 2), 0.0, 0.0])

    def ctrl(t, x):
        phi = 2.0 * math.atan2(x[4], x[3])
        p = x[10]
        tau_x = -qc._J[0] * (wn ** 2 * phi + 2 * zeta * wn * p)
        return qc.rotor_speeds_from_wrench(qc.mass * qc.g, [tau_x, 0.0, 0.0])

    sc = qc.simulate(xc, ctrl, dt=1e-4, t_end=0.4)
    wd = wn * math.sqrt(1 - zeta ** 2)
    tt = sc["t"]
    phi_num = 2.0 * np.arctan2(sc["x"][:, 4], sc["x"][:, 3])
    phi_ana = phi0 * np.exp(-zeta * wn * tt) * (np.cos(wd * tt)
                                                + zeta / math.sqrt(1 - zeta ** 2) * np.sin(wd * tt))
    check("max |phi_sim - phi_analytic| over 0.4 s [rad]",
          float(np.max(np.abs(phi_num - phi_ana))), 0.0, 2e-5,
          "tolerance allows the O(phi0^2) error of the small-angle reference; the agreement is "
          "in fact at integrator precision because a pure roll has omega x J omega = 0 and "
          "phidot = p exactly, so the nonlinear plant IS the second-order system here")
    t_zero_ref = (math.pi - math.atan2(math.sqrt(1 - zeta ** 2), zeta)) / wd
    i0 = int(np.argmax(phi_num <= 0.0))
    check("first zero crossing [s]", float(tt[i0]), t_zero_ref, 2e-3)

    if verbose:
        print("6. Aerodynamic terms against the published model and coefficients")
    # REFERENCE: Sun et al. eq. (9), quoted from the arXiv PDF p. 4:
    #   "f B a = [ -kd,x vx ; -kd,y vy ; -kd,z vz + kh (v2 x +v2 y) ]"
    # with TABLE II's (kd,x, kd,y, kd,z) = (0.26, 0.28, 0.42) kg/s and kh = 0.01 kg/m.
    # At v_B = (10, 0, 0) m/s: f = (-2.6, 0, +1.0) N by hand.
    fa = q.aero_force_body([10.0, 0.0, 0.0])
    check("drag force x at 10 m/s [N]", float(fa[0]), -2.6, 1e-12)
    check("h-force z at 10 m/s [N]", float(fa[2]), +1.0, 1e-12)
    q_nodrag = q.variant(enable_drag=False, enable_h_force=True)
    check("drag switch off leaves only the h-force [N]",
          float(np.linalg.norm(q_nodrag.aero_force_body([10.0, 0.0, 0.0]) - np.array([0, 0, 1.0]))),
          0.0, 1e-12)
    # size check by hand: at 10 m/s the drag is 2.6 / 7.3549875 = 0.35350 of the weight, so
    # level flight needs a tilt of atan(0.35350) = 19.4685 deg (small-tilt reading, where the
    # body-frame kd acts horizontally).
    check("drag at 10 m/s as a fraction of weight", 2.6 / h["thrust_total"], 0.353501, 1e-5)
    # KNOWN LIMIT: with thrust off and only linear drag, the plant must reach the terminal
    # velocity of Stokes-like fall, m g = kd_z |vz| -> |vz| = 7.3549875 / 0.42 = 17.5119 m/s,
    # approached with time constant m/kd_z = 0.75/0.42 = 1.7857 s (so 30 s is ~17 constants).
    qt = q.variant(motor_tau=0.0, enable_h_force=False)
    st = qt.simulate(qt.hover_state(position=(0, 0, 1000.0)), np.zeros(4), dt=1e-3, t_end=30.0)
    check("terminal vertical speed, thrust off [m/s]", float(st["x"][-1, 9]), -17.5119, 1e-3)

    if verbose:
        print("7. Rotor map: round trip, geometry, and refusal of impossible commands")
    w_h = h["omega_hover"]
    wr = q.rotor_speeds_from_wrench(h["thrust_total"], [0.1, -0.05, 0.02])
    back = q.wrench(wr)
    check("round-trip thrust [N]", back["thrust"], h["thrust_total"], 1e-9)
    check("round-trip |torque error| [N m]",
          float(np.linalg.norm(back["torque"] - np.array([0.1, -0.05, 0.02]))), 0.0, 1e-12)
    check("hover map gives the hover speed [rad/s]",
          float(np.max(np.abs(q.rotor_speeds_from_wrench(h["thrust_total"], [0, 0, 0]) - w_h))),
          0.0, 1e-9)
    # geometry: roll arm = l sin(beta) = 0.14 * sin(56 deg) = 0.11606 m, pitch arm
    # l cos(beta) = 0.07828 m, yaw torque per unit thrust = k_m/k_f = 2.37e-8/1.51e-6 = 0.015695 m
    M = q.mix_matrix()
    check("roll arm l sin(beta) [m]", float(M[1, 1]), 0.14 * math.sin(math.radians(56.0)), 1e-12)
    check("pitch arm l cos(beta) [m]", float(M[2, 3]), 0.14 * math.cos(math.radians(56.0)), 1e-12)
    check("yaw torque per unit thrust k_m/k_f [m]", float(abs(M[3, 0])), 2.37e-8 / 1.51e-6, 1e-15)
    refused = False
    try:  # 4 N m of roll needs 2 * 4/0.11606 = 34.5 N of thrust difference: impossible
        q.rotor_thrusts_from_wrench(h["thrust_total"], [4.0, 0.0, 0.0])
    except ValueError:
        refused = True
    check_true("refuses a roll torque the rotors cannot make", refused)
    check_true("accepts the largest roll torque they can make",
               q.wrench_feasible(4 * q.thrust_max / 2, [q.thrust_max * M[1, 1] * 0.99, 0, 0]))
    bad = False
    try:
        Quadrotor(mass=5.0, thrust_max=8.5)  # 34 N cannot hold 49 N
    except ValueError:
        bad = True
    check_true("refuses a vehicle that cannot hover", bad)
    bad2 = False
    try:
        Quadrotor(inertia=(1e-3, 1e-3, 5e-3))  # violates Jx + Jy >= Jz
    except ValueError:
        bad2 = True
    check_true("refuses an inertia no rigid body has", bad2)

    if verbose:
        print("8. Integrator diagnostics: exact invariants of the torque-free body and free fall")
    # REFERENCE: for torque-free motion Euler's equations conserve the world-frame angular
    # momentum J omega and the rotational kinetic energy 0.5 omega^T J omega exactly (Landau
    # and Lifshitz, Mechanics, sec. 36-37); free fall with no thrust reduces to Newtonian
    # ballistics z = z0 - g t^2 / 2.
    dg = q.diagnostics(dt=1e-3, t_end=2.0)
    check("torque-free |J omega| drift (relative)", dg["angular_momentum_drift"], 0.0, 1e-9)
    check("torque-free rotational energy drift (relative)",
          dg["rotational_energy_drift"], 0.0, 1e-9)
    check("quaternion norm drift", dg["quat_norm_drift"], 0.0, 1e-12)
    check("free-fall position error after 1 s [m]", dg["free_fall_error"], 0.0, 1e-9)
    check("RK4 convergence order", dg["rk4_order"], 4.0, 0.3)

    if verbose:
        print("9. Hover linearisation: control_tools.linearize against the analytic Jacobians")
    lin = q.hover_linearization()
    if _ct is None:
        if verbose:
            print("  [skip] control_tools not importable; analytic Jacobians only")
    else:
        f = q.euler_state_dynamics("wrench")
        x0e, u0e = q.hover_equilibrium_euler("wrench")
        A, B, info = _ct.linearize(f, x0e, u0e)
        check("linearize residual at hover [SI]", float(np.linalg.norm(info["residual"])), 0.0, 1e-9)
        check("max |A_num - A_analytic|", float(np.max(np.abs(A - lin["A"]))), 0.0, 1e-6)
        check("max |B_num - B_analytic|", float(np.max(np.abs(B - lin["B"]))), 0.0, 1e-6)
    # the analytic form must contain the textbook hover couplings xddot = g theta, yddot = -g phi
    check("d(xddot)/d(theta) = g [m/s^2/rad]", float(lin["A"][3, 7]), 9.80665, 1e-12)
    check("d(yddot)/d(phi) = -g [m/s^2/rad]", float(lin["A"][4, 6]), -9.80665, 1e-12)
    check("d(phiddot)/d(tau_x) = 1/Jx [1/kg/m^2]", float(lin["B"][9, 1]), 1 / 2.5e-3, 1e-9)

    if verbose:
        print(f"\n{'PASS' if ok[0] else 'FAIL'}: {n[0]} checks")
    return bool(ok[0])


# --------------------------------------------------------------------------- CLI
def _qty(s, unit):
    """Parse a command-line quantity, with units if unit_tools is available."""
    if _Q is not None:
        try:
            v = _Q(s).to(unit)
            return float(v if not hasattr(v, "value") else v.value)
        except Exception:
            pass
    try:
        return float(s)
    except ValueError:
        raise ValueError(f"cannot read {s!r} as a quantity in {unit}") from None


def _cmd_hover(argv) -> int:
    import argparse
    p = argparse.ArgumentParser(prog="quadrotor.py hover")
    p.add_argument("--mass", default=None, help="e.g. 0.75kg")
    p.add_argument("--thrust-max", default=None, help="per rotor, e.g. 8.5N")
    p.add_argument("--k-thrust", type=float, default=None, help="N/(rad/s)^2")
    p.add_argument("--arm", default=None, help="arm length, e.g. 0.14m")
    p.add_argument("--arm-angle", type=float, default=None, help="deg from +x")
    p.add_argument("--motor-tau", type=float, default=None, help="s")
    a = p.parse_args(argv)
    ch = {}
    if a.mass:
        ch["mass"] = _qty(a.mass, "kg")
    if a.thrust_max:
        ch["thrust_max"] = _qty(a.thrust_max, "N")
    if a.k_thrust:
        ch["k_thrust"] = a.k_thrust
    if a.arm:
        ch["arm_length"] = _qty(a.arm, "m")
    if a.arm_angle:
        ch["arm_angle_deg"] = a.arm_angle
    if a.motor_tau is not None:
        ch["motor_tau"] = a.motor_tau
    q = platform_sun2022(**ch)
    h = q.hover()
    print(f"platform: {q.name}  m = {q.mass} kg  J = {tuple(q.inertia)} kg m^2  "
          f"l = {q.arm_length} m  beta = {q.arm_angle_deg} deg")
    print(f"  hover thrust      {h['thrust_total']:.4f} N total, "
          f"{h['thrust_per_rotor']:.4f} N per rotor")
    print(f"  hover rotor speed {h['omega_hover']:.1f} rad/s = {h['rpm_hover']:.0f} rpm "
          f"({100*h['throttle_fraction']:.1f} % of max thrust)")
    print(f"  thrust-to-weight  {h['thrust_to_weight']:.3f}")
    print(f"  a_max             {h['a_max_thrust']:.2f} m/s^2 = {h['a_max_thrust']/q.g:.2f} g "
          f"(thrust only); vertical {h['a_max_vertical']:.2f} m/s^2; "
          f"horizontal {h['a_max_horizontal']:.2f} m/s^2 at "
          f"{h['tilt_for_max_horizontal_deg']:.1f} deg tilt")
    print(f"  max roll torque   {h['torque_max_roll']:.4f} N m -> "
          f"{h['alpha_max_roll']:.1f} rad/s^2 roll acceleration")
    if q.motor_tau > 0:
        print(f"  motor lag         {1e3*q.motor_tau:.1f} ms -> first-order corner at "
              f"{1/q.motor_tau:.1f} rad/s = {1/(2*math.pi*q.motor_tau):.2f} Hz; "
              f"thrust-rate ceiling ~ {h['a_max_thrust']/q.motor_tau:.0f} m/s^3 jerk")
    return 0


def _cmd_step(argv) -> int:
    import argparse
    p = argparse.ArgumentParser(prog="quadrotor.py step")
    p.add_argument("--tau", type=float, default=0.0391, help="motor time constant, s")
    p.add_argument("--torque", type=float, default=0.1, help="commanded roll torque, N m")
    p.add_argument("--t-end", type=float, default=0.2, help="s")
    a = p.parse_args(argv)
    q = platform_sun2022(motor_tau=a.tau)
    h = q.hover()
    wr = q.rotor_speeds_from_wrench(h["thrust_total"], [a.torque, 0.0, 0.0])
    sim = q.simulate(q.hover_state(), wr, dt=min(2e-5, max(a.tau, 1e-6) / 20), t_end=a.t_end)
    qf = sim["x"][-1, 3:7]
    phi = 2.0 * math.atan2(qf[1], qf[0])
    phi_inst = a.torque / q.inertia[0] * a.t_end ** 2 / 2
    print(f"roll step of {a.torque} N m with motor_tau = {1e3*a.tau:.1f} ms")
    print(f"  rotor speeds      {np.array2string(wr, precision=1)} rad/s")
    print(f"  roll after {a.t_end:.3f} s  {math.degrees(phi):.3f} deg "
          f"(instantaneous thrust: {math.degrees(phi_inst):.3f} deg, "
          f"lag costs {math.degrees(phi_inst-phi):.3f} deg)")
    print(f"  roll rate         {sim['x'][-1,10]:.2f} rad/s; "
          f"quaternion norm drift {sim['diagnostics']['quat_norm_drift']:.2e}")
    return 0


def _main(argv) -> int:
    if len(argv) < 2 or argv[1] in ("-h", "--help", "help"):
        print(__doc__)
        print("commands: selftest | hover | step")
        return 0
    cmd, rest = argv[1], argv[2:]
    if cmd == "selftest":
        return 0 if selftest(verbose=True) else 1
    if cmd == "hover":
        return _cmd_hover(rest)
    if cmd == "step":
        return _cmd_step(rest)
    print(f"unknown command {cmd!r}; try selftest | hover | step")
    return 2


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
