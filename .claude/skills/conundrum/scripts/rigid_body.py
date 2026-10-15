#!/usr/bin/env python3
"""Planar multibody dynamics in manipulator form, with the verification a simulation needs.

WHAT IT COMPUTES
    For a planar chain of rigid links joined by revolute joints under uniform gravity, the
    manipulator equations

        M(q) qddot + C(q, qdot) qdot + D qdot = tau_g(q) + B u

    with M the mass matrix, C the Coriolis/centrifugal matrix in Christoffel form, D a viscous
    damping matrix, tau_g the generalised gravity torque and B the actuation selection matrix.
    From those: forward dynamics, kinetic/potential/total energy, a state-space callable
    f(x, u) for control work, exact symbolic matrices (SymPy), fixed-step RK4 integration, and
    four model checks that say whether a simulation can be trusted:

        energy_drift        unforced, undamped energy must be conserved
        passivity_residual  Mdot - (C + C^T) must vanish (Christoffel property)
        convergence_order   halving the step must shrink the error like dt^4 for RK4
        cross_check         two independent dynamics implementations must agree

MODEL AND CONVENTIONS
    - Plane: x to the right, y up, gravity -g y.
    - Coordinates q are RELATIVE joint angles in radians. q1 is link 1's angle from the
      DOWNWARD vertical, so q = 0 is the chain hanging straight down and q = (pi, 0, ...) is
      straight up. This is the convention of Tedrake's Underactuated Robotics, so its
      published Acrobot matrices can be compared entry by entry (see selftest).
    - Each Link carries: mass m (kg), length l (m, its own joint to the next joint), lc (m,
      its own joint to its centre of mass) and izz (kg m^2, the moment of inertia ABOUT ITS
      OWN CENTRE OF MASS, not about the joint). Literature often tabulates the inertia about
      the joint instead; Link.from_pivot_inertia() takes that form, and Link.rod() and
      Link.point_mass() build the two common idealisations. Getting this wrong is the most
      common silent error in a hand-built model: it changes M but leaves the equations
      looking right.
    - C is the Christoffel-symbol factorisation, the one that satisfies
      Mdot = C + C^T. Other factorisations of C exist (Tedrake's published Acrobot C is one),
      and they differ entry by entry while the product C qdot is identical. Compare C qdot,
      never C, against a published matrix.
    - Rotation of a joint is NOT limited and no joint-limit or contact model is included. A
      chain whose links would pass through each other simulates happily; that is the model's
      problem, not a bug.

ASSUMPTIONS AND VALIDITY
    Rigid links, ideal revolute joints, no contact, no actuator dynamics, planar motion,
    uniform gravity, viscous joint damping only (no Coulomb friction, no backlash, no
    stiction). Torques are applied directly at the joints: real actuators have finite
    bandwidth and a torque-speed envelope, which this model does not represent. For an
    estimate of how far a conclusion drifts when those are included, perturb the parameters
    (control_tools.robustness_sweep) and treat the result as a bound, not a prediction.

UNITS
    SI throughout the Python API: kg, m, kg m^2, rad, rad/s, N m, s, J.

PYTHON USAGE
    import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
    from rigid_body import Chain, Link, acrobot, simulate
    chain = acrobot()                       # Spong's Acrobot parameters
    M = chain.mass_matrix([0.1, 0.2])
    qdd = chain.forward_dynamics([0.1, 0.2], [0.0, 0.0], [0.0])
    print(chain.energy([0.1, 0.2], [0.0, 0.0]))
    traj = simulate(chain, lambda t, x: [0.0], [0.1, 0.2, 0.0, 0.0], 5.0, 1e-3)
    print(traj.energy_drift)                # relative drift, should be ~1e-10 for RK4

COMMAND LINE
    python3 .claude/skills/conundrum/scripts/rigid_body.py selftest
    python3 .claude/skills/conundrum/scripts/rigid_body.py acrobot --state 0.1 0.2 0 0
    python3 .claude/skills/conundrum/scripts/rigid_body.py symbolic acrobot
"""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field, replace
from typing import Callable, Sequence

try:
    import numpy as np
except ImportError:  # pragma: no cover - the pipeline installs numpy at preflight
    raise SystemExit("rigid_body.py needs numpy: python3 -m pip install numpy")

G_EARTH = 9.81   # m/s^2, standard gravity used by Tedrake's Underactuated Robotics examples

__all__ = ["Link", "Chain", "Trajectory", "simulate", "acrobot", "cartpole_chain",
           "double_pendulum", "pendulum", "cross_check", "convergence_order", "G_EARTH"]


# ----------------------------------------------------------------------------- links

@dataclass(frozen=True)
class Link:
    """One rigid link of a planar chain.

    mass: kg. length: m, this link's joint to the next joint. com: m, this link's joint to
    its own centre of mass. izz: kg m^2 about the CENTRE OF MASS. damping: N m s/rad, viscous
    torque at this link's joint. actuated: whether a control torque acts at this joint.
    """
    mass: float
    length: float
    com: float
    izz: float
    damping: float = 0.0
    actuated: bool = True
    name: str = ""

    def __post_init__(self) -> None:
        if self.mass < 0 or self.length < 0 or self.izz < 0 or self.damping < 0:
            raise ValueError(f"mass, length, izz and damping must be >= 0: {self}")
        if self.com < 0:
            raise ValueError(f"com must be >= 0 (measured from this link's joint): {self}")

    @property
    def izz_pivot(self) -> float:
        """Moment of inertia about this link's own joint (parallel-axis theorem)."""
        return self.izz + self.mass * self.com ** 2

    @classmethod
    def from_pivot_inertia(cls, mass: float, length: float, com: float, izz_pivot: float,
                           **kw) -> "Link":
        """Build a link from an inertia tabulated about the JOINT, not the centre of mass."""
        izz = izz_pivot - mass * com ** 2
        if izz < -1e-12 * max(1.0, abs(izz_pivot)):
            raise ValueError(
                f"izz_pivot={izz_pivot} is below m*com^2={mass * com ** 2}: no rigid body has "
                "an inertia about a pivot smaller than m*d^2 (parallel-axis theorem)")
        return cls(mass=mass, length=length, com=com, izz=max(izz, 0.0), **kw)

    @classmethod
    def rod(cls, mass: float, length: float, **kw) -> "Link":
        """A uniform thin rod: com at length/2, izz = m L^2 / 12 about the centre of mass."""
        return cls(mass=mass, length=length, com=length / 2.0,
                   izz=mass * length ** 2 / 12.0, **kw)

    @classmethod
    def point_mass(cls, mass: float, length: float, **kw) -> "Link":
        """A massless rod with a point mass at its far end: com = length, izz = 0."""
        return cls(mass=mass, length=length, com=length, izz=0.0, **kw)


# ----------------------------------------------------------------------------- chain

class Chain:
    """A planar serial chain of revolute joints under gravity, in manipulator form.

    Two implementations of the same equations live here. The reference one builds M from
    centre-of-mass Jacobians and C by differencing M numerically; it is slow but has nothing
    between it and the geometry. The compiled one lambdifies the exact symbolic M, C qdot and
    tau_g once (needing sympy) and then evaluates them in microseconds, which is what makes a
    30-second simulation finish inside an agent's script budget. The public methods use the
    compiled path when sympy is available and fall back to the reference path when it is not;
    the *_reference methods always take the slow route, and the selftest cross-checks the two
    against each other.
    """

    def __init__(self, links: Sequence[Link], gravity: float = G_EARTH, compile: bool = True):
        self.links = list(links)
        if not self.links:
            raise ValueError("a chain needs at least one link")
        if gravity < 0:
            raise ValueError("gravity is a magnitude: pass g >= 0")
        self.gravity = float(gravity)
        self.n = len(self.links)
        acted = [i for i, lk in enumerate(self.links) if lk.actuated]
        self.B = np.zeros((self.n, len(acted)))
        for col, i in enumerate(acted):
            self.B[i, col] = 1.0
        self.m_actuated = len(acted)
        self.actuated_joints = acted
        self._want_compiled = bool(compile)
        self._compiled = None          # built lazily on first use
        self._compile_failed = False

    # -- the compiled fast path ----------------------------------------------

    def _fast(self):
        """Lambdified (M, C qdot, tau_g), built once. None when sympy is unavailable."""
        if self._compiled is not None or self._compile_failed or not self._want_compiled:
            return self._compiled
        try:
            import sympy as sp
            M, C, tau_g, (q, v, g) = self.symbolic(simplify=False)
            args = list(q) + list(v)
            sub = {g: self.gravity}
            mods = ["numpy"]
            self._compiled = {
                "M": sp.lambdify(args, sp.Matrix(M).subs(sub), modules=mods, cse=True),
                "Cv": sp.lambdify(args, sp.Matrix(C).subs(sub) * sp.Matrix(v),
                                  modules=mods, cse=True),
                "C": sp.lambdify(args, sp.Matrix(C).subs(sub), modules=mods, cse=True),
                "tau_g": sp.lambdify(args, sp.Matrix(tau_g).subs(sub), modules=mods,
                                     cse=True),
            }
        except Exception:              # sympy missing, or lambdify choked on a big chain
            self._compile_failed = True
            self._compiled = None
        return self._compiled

    # -- geometry -------------------------------------------------------------

    def _absolute(self, q) -> np.ndarray:
        """Absolute link angles from the downward vertical: cumulative sums of q."""
        return np.cumsum(np.asarray(q, dtype=float))

    def com_positions(self, q) -> np.ndarray:
        """(n, 2) centre-of-mass positions in metres, with y up and the base at the origin."""
        th = self._absolute(q)
        joint = np.zeros(2)
        out = np.zeros((self.n, 2))
        for i, lk in enumerate(self.links):
            d = np.array([math.sin(th[i]), -math.cos(th[i])])
            out[i] = joint + lk.com * d
            joint = joint + lk.length * d
        return out

    def joint_positions(self, q) -> np.ndarray:
        """(n + 1, 2) joint positions in metres, base first, free end last."""
        th = self._absolute(q)
        pts = np.zeros((self.n + 1, 2))
        for i, lk in enumerate(self.links):
            pts[i + 1] = pts[i] + lk.length * np.array([math.sin(th[i]), -math.cos(th[i])])
        return pts

    def _com_jacobians(self, q):
        """d(com_i)/dq as a list of (2, n) arrays, and d(absolute angle_i)/dq rows."""
        th = self._absolute(q)
        jac = [np.zeros((2, self.n)) for _ in range(self.n)]
        for i, lk in enumerate(self.links):
            # link i's centre of mass moves with joints 0..i
            for j in range(i + 1):
                # contribution of joint j: everything from link j outwards rotates about it
                for k in range(j, i + 1):
                    arm = self.links[k].com if k == i else self.links[k].length
                    jac[i][0, j] += arm * math.cos(th[k])
                    jac[i][1, j] += arm * math.sin(th[k])
        return jac, th

    # -- manipulator terms ----------------------------------------------------

    def mass_matrix(self, q) -> np.ndarray:
        """M(q), symmetric positive definite, in kg m^2."""
        fast = self._fast()
        if fast is not None:
            q = np.asarray(q, dtype=float)
            if q.shape != (self.n,):
                raise ValueError(f"q must have {self.n} entries, got {q.shape}")
            M = np.asarray(fast["M"](*q, *np.zeros(self.n)), dtype=float)
            return 0.5 * (M + M.T)
        return self.mass_matrix_reference(q)

    def mass_matrix_reference(self, q) -> np.ndarray:
        """M(q) from centre-of-mass Jacobians, with no symbolic step in between."""
        q = np.asarray(q, dtype=float)
        if q.shape != (self.n,):
            raise ValueError(f"q must have {self.n} entries, got {q.shape}")
        jac, _ = self._com_jacobians(q)
        M = np.zeros((self.n, self.n))
        for i, lk in enumerate(self.links):
            M += lk.mass * (jac[i].T @ jac[i])
            # the absolute angular velocity of link i is the sum of qdot[0..i]
            row = np.zeros((1, self.n))
            row[0, : i + 1] = 1.0
            M += lk.izz * (row.T @ row)
        return 0.5 * (M + M.T)   # kill the round-off asymmetry; M is symmetric by construction

    def _dM_dq(self, q, eps: float = 1e-6) -> np.ndarray:
        """dM/dq_k as an (n, n, n) array, by central differences on the analytic M."""
        q = np.asarray(q, dtype=float)
        out = np.zeros((self.n, self.n, self.n))
        for k in range(self.n):
            step = np.zeros(self.n)
            step[k] = eps
            out[:, :, k] = (self.mass_matrix(q + step) - self.mass_matrix(q - step)) / (2 * eps)
        return out

    def coriolis(self, q, qdot) -> np.ndarray:
        """C(q, qdot) in the Christoffel factorisation, so that Mdot = C + C^T.

        Other factorisations give the same product C qdot; compare products, not matrices.
        """
        fast = self._fast()
        if fast is not None:
            q = np.asarray(q, dtype=float)
            qdot = np.asarray(qdot, dtype=float)
            if qdot.shape != (self.n,):
                raise ValueError(f"qdot must have {self.n} entries, got {qdot.shape}")
            return np.asarray(fast["C"](*q, *qdot), dtype=float)
        return self.coriolis_reference(q, qdot)

    def coriolis_reference(self, q, qdot) -> np.ndarray:
        """C(q, qdot) from Christoffel symbols of a numerically differenced M."""
        q = np.asarray(q, dtype=float)
        qdot = np.asarray(qdot, dtype=float)
        if qdot.shape != (self.n,):
            raise ValueError(f"qdot must have {self.n} entries, got {qdot.shape}")
        dM = np.zeros((self.n, self.n, self.n))
        eps = 1e-6
        for k in range(self.n):
            step = np.zeros(self.n)
            step[k] = eps
            dM[:, :, k] = (self.mass_matrix_reference(q + step)
                           - self.mass_matrix_reference(q - step)) / (2 * eps)
        C = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                # C_ij = sum_k 1/2 (dM_ij/dq_k + dM_ik/dq_j - dM_jk/dq_i) qdot_k
                C[i, j] = 0.5 * np.sum(
                    (dM[i, j, :] + dM[i, :, j] - dM[j, :, i]) * qdot)
        return C

    def gravity_torque(self, q) -> np.ndarray:
        """tau_g(q) = -dU/dq in N m, the gravity term on the RIGHT-hand side."""
        fast = self._fast()
        if fast is not None:
            q = np.asarray(q, dtype=float)
            return np.asarray(fast["tau_g"](*q, *np.zeros(self.n)), dtype=float).ravel()
        return self.gravity_torque_reference(q)

    def gravity_torque_reference(self, q) -> np.ndarray:
        """tau_g(q) from centre-of-mass Jacobians."""
        q = np.asarray(q, dtype=float)
        jac, _ = self._com_jacobians(q)
        tau = np.zeros(self.n)
        for i, lk in enumerate(self.links):
            # U_i = m_i g y_i, so -dU_i/dq = -m_i g * (dy_i/dq)
            tau -= lk.mass * self.gravity * jac[i][1, :]
        return tau

    def damping_matrix(self) -> np.ndarray:
        """D, the diagonal viscous damping matrix in N m s/rad."""
        return np.diag([lk.damping for lk in self.links])

    def manipulator_terms(self, q, qdot):
        """(M, C qdot, tau_g): the three terms a published model is compared against."""
        return (self.mass_matrix(q), self.coriolis(q, qdot) @ np.asarray(qdot, dtype=float),
                self.gravity_torque(q))

    # -- energy ---------------------------------------------------------------

    def kinetic(self, q, qdot) -> float:
        """T = 1/2 qdot^T M(q) qdot, in joules."""
        qdot = np.asarray(qdot, dtype=float)
        return float(0.5 * qdot @ self.mass_matrix(q) @ qdot)

    def potential(self, q) -> float:
        """U = sum m_i g y_i in joules, zero with the base joint at the origin."""
        return float(sum(lk.mass * self.gravity * p[1]
                         for lk, p in zip(self.links, self.com_positions(q))))

    def energy(self, q, qdot) -> float:
        """Total mechanical energy T + U in joules."""
        return self.kinetic(q, qdot) + self.potential(q)

    def upright_energy(self) -> float:
        """U at the straight-up configuration q = (pi, 0, ..., 0), the swing-up target."""
        q = np.zeros(self.n)
        q[0] = math.pi
        return self.potential(q)

    # -- dynamics -------------------------------------------------------------

    def forward_dynamics(self, q, qdot, u) -> np.ndarray:
        """qddot from M qddot + C qdot + D qdot = tau_g + B u, in rad/s^2."""
        qdot = np.asarray(qdot, dtype=float)
        u = np.atleast_1d(np.asarray(u, dtype=float))
        if u.shape != (self.m_actuated,):
            raise ValueError(f"u must have {self.m_actuated} entries, got {u.shape}")
        M = self.mass_matrix(q)
        rhs = (self.gravity_torque(q) + self.B @ u
               - self.coriolis(q, qdot) @ qdot - self.damping_matrix() @ qdot)
        try:
            return np.linalg.solve(M, rhs)
        except np.linalg.LinAlgError as exc:   # a massless or degenerate link
            raise ValueError(f"M(q) is singular at q={np.asarray(q)}: {exc}") from exc

    def state_dynamics(self) -> Callable[[np.ndarray, np.ndarray], np.ndarray]:
        """f(x, u) for x = [q, qdot], the form control_tools.linearize expects."""
        n = self.n

        def f(x, u):
            x = np.asarray(x, dtype=float)
            return np.concatenate([x[n:], self.forward_dynamics(x[:n], x[n:], u)])
        return f

    def state_dynamics_reference(self) -> Callable[[np.ndarray, np.ndarray], np.ndarray]:
        """The same f(x, u) built only from the reference (uncompiled) terms."""
        n = self.n

        def f(x, u):
            x = np.asarray(x, dtype=float)
            q, qdot = x[:n], x[n:]
            u = np.atleast_1d(np.asarray(u, dtype=float))
            M = self.mass_matrix_reference(q)
            rhs = (self.gravity_torque_reference(q) + self.B @ u
                   - self.coriolis_reference(q, qdot) @ qdot
                   - self.damping_matrix() @ qdot)
            return np.concatenate([qdot, np.linalg.solve(M, rhs)])
        return f

    def equilibrium_torque(self, q) -> np.ndarray:
        """The constant u holding the chain at rest at q, least-squares if B is not square.

        Raises ValueError when no u can hold it: for the Acrobot that is every q whose first
        joint is off the vertical, since joint 1 is passive and feels gravity.
        """
        tau_g = self.gravity_torque(q)
        u, *_ = np.linalg.lstsq(self.B, -tau_g, rcond=None)
        residual = self.B @ u + tau_g
        if np.max(np.abs(residual)) > 1e-8 * max(1.0, float(np.max(np.abs(tau_g)))):
            raise ValueError(
                f"no actuator torque holds q={np.asarray(q)}: the unactuated joints feel a "
                f"residual gravity torque of {residual} N m")
        return u

    # -- model checks ---------------------------------------------------------

    def passivity_residual(self, q, qdot) -> float:
        """max |Mdot - (C + C^T)|, which the Christoffel C makes zero.

        A non-zero value means M and C disagree, the error that silently injects or removes
        energy in a simulation while every matrix still looks plausible.
        """
        dM = self._dM_dq(q)
        Mdot = np.tensordot(dM, np.asarray(qdot, dtype=float), axes=([2], [0]))
        C = self.coriolis(q, qdot)
        return float(np.max(np.abs(Mdot - (C + C.T))))

    def symbolic(self, simplify: bool = True):
        """Exact (M, C, tau_g) as SymPy matrices in symbols q0.., v0.., with g.

        C is the Christoffel factorisation. Returns (M, C, tau_g, (q, v, g)) so a caller can
        substitute or differentiate. Needs sympy. simplify=False skips the trigonometric
        tidying, which is what the compiled path uses: lambdify does not care how the
        expression reads, and simplify() is the expensive step on a longer chain.
        """
        import sympy as sp

        q = sp.symbols(f"q0:{self.n}", real=True)
        v = sp.symbols(f"v0:{self.n}", real=True)
        g = sp.Symbol("g", positive=True)
        th = [sum(q[: i + 1], sp.Integer(0)) for i in range(self.n)]
        joint = [sp.Integer(0), sp.Integer(0)]
        com = []
        for i, lk in enumerate(self.links):
            d = (sp.sin(th[i]), -sp.cos(th[i]))
            com.append((joint[0] + sp.Rational(1) * lk.com * d[0],
                        joint[1] + sp.Rational(1) * lk.com * d[1]))
            joint = [joint[0] + lk.length * d[0], joint[1] + lk.length * d[1]]
        T = sp.Integer(0)
        U = sp.Integer(0)
        for i, lk in enumerate(self.links):
            vx = sum(sp.diff(com[i][0], q[j]) * v[j] for j in range(self.n))
            vy = sum(sp.diff(com[i][1], q[j]) * v[j] for j in range(self.n))
            omega = sum(v[: i + 1], sp.Integer(0))
            T += sp.Rational(1, 2) * lk.mass * (vx ** 2 + vy ** 2) + \
                sp.Rational(1, 2) * lk.izz * omega ** 2
            U += lk.mass * g * com[i][1]
        M = sp.hessian(T, v)
        if simplify:
            M = sp.simplify(M)
        C = sp.zeros(self.n, self.n)
        for i in range(self.n):
            for j in range(self.n):
                entry = sum(
                    sp.Rational(1, 2) * (sp.diff(M[i, j], q[k]) + sp.diff(M[i, k], q[j])
                                         - sp.diff(M[j, k], q[i])) * v[k]
                    for k in range(self.n))
                C[i, j] = sp.simplify(entry) if simplify else entry
        tau_g = sp.Matrix([-sp.diff(U, q[i]) for i in range(self.n)])
        if simplify:
            tau_g = sp.simplify(tau_g)
        return M, C, tau_g, (q, v, g)

    def __repr__(self) -> str:
        return (f"Chain({self.n} links, {self.m_actuated} actuated at {self.actuated_joints}, "
                f"g={self.gravity})")


# ----------------------------------------------------------------------------- simulation

@dataclass
class Trajectory:
    """The result of a simulation, with the diagnostics that say whether to trust it."""
    t: np.ndarray
    x: np.ndarray                 # (len(t), 2n)
    u: np.ndarray                 # (len(t), m)
    energy: np.ndarray            # (len(t),) joules
    dt: float
    steps: int
    saturated_fraction: float = 0.0
    diverged: bool = False
    meta: dict = field(default_factory=dict)

    @property
    def energy_drift(self) -> float:
        """|E(T) - E(0)| / max(1, |E(0)| range): the integrator's energy error.

        Meaningful only for an unforced, undamped run, where the true value is zero.
        """
        scale = max(1.0, float(np.max(self.energy) - np.min(self.energy)),
                    abs(float(self.energy[0])))
        return float(abs(self.energy[-1] - self.energy[0]) / scale)

    @property
    def final_state(self) -> np.ndarray:
        return self.x[-1]


def simulate(chain: Chain, controller, x0, t_end: float, dt: float,
             torque_limit=None, noise=None, rng=None, stop=None) -> Trajectory:
    """Integrate the chain under a feedback controller with fixed-step RK4.

    controller: u = controller(t, x), given the TRUE state unless noise is set.
    torque_limit: scalar or per-actuator array; torques are clipped to +-limit, and the
        fraction of steps that clipped comes back as traj.saturated_fraction.
    noise: dict with 'q' and/or 'qdot' standard deviations (rad, rad/s). The controller then
        sees a corrupted state while the plant integrates the true one, which is the only
        honest way to test a controller against sensor noise.
    stop: stop(t, x) -> True ends the run early (used for region-of-attraction searches).

    RK4 is used because a fixed step makes the energy-drift and convergence-order checks
    meaningful; a variable-step solver hides integration error in its own tolerance.
    """
    n = chain.n
    x = np.asarray(x0, dtype=float).copy()
    if x.shape != (2 * n,):
        raise ValueError(f"x0 must have {2 * n} entries, got {x.shape}")
    if dt <= 0 or t_end <= 0:
        raise ValueError("dt and t_end must be positive")
    steps = int(round(t_end / dt))
    rng = np.random.default_rng(0 if rng is None else rng) if not isinstance(
        rng, np.random.Generator) else rng
    sigma_q = float((noise or {}).get("q", 0.0))
    sigma_v = float((noise or {}).get("qdot", 0.0))
    limit = None if torque_limit is None else np.atleast_1d(
        np.asarray(torque_limit, dtype=float))

    def measured(xx):
        if sigma_q == 0.0 and sigma_v == 0.0:
            return xx
        out = xx.copy()
        if sigma_q:
            out[:n] += rng.normal(0.0, sigma_q, n)
        if sigma_v:
            out[n:] += rng.normal(0.0, sigma_v, n)
        return out

    f = chain.state_dynamics()
    ts = np.zeros(steps + 1)
    xs = np.zeros((steps + 1, 2 * n))
    us = np.zeros((steps + 1, chain.m_actuated))
    es = np.zeros(steps + 1)
    xs[0] = x
    es[0] = chain.energy(x[:n], x[n:])
    clipped = 0
    diverged = False
    k = 0
    for k in range(steps):
        t = k * dt
        u = np.atleast_1d(np.asarray(controller(t, measured(x)), dtype=float))
        if limit is not None:
            u_clipped = np.clip(u, -limit, limit)
            if np.any(np.abs(u_clipped - u) > 1e-12):
                clipped += 1
            u = u_clipped
        us[k] = u
        # RK4 on the closed-loop state with u held over the step (zero-order hold)
        k1 = f(x, u)
        k2 = f(x + 0.5 * dt * k1, u)
        k3 = f(x + 0.5 * dt * k2, u)
        k4 = f(x + dt * k3, u)
        x = x + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        if not np.all(np.isfinite(x)) or np.max(np.abs(x)) > 1e8:
            diverged = True
            ts, xs, us, es = ts[: k + 2], xs[: k + 2], us[: k + 2], es[: k + 2]
            ts[-1] = (k + 1) * dt
            xs[-1] = np.nan_to_num(x, nan=0.0, posinf=1e8, neginf=-1e8)
            es[-1] = es[k]
            break
        ts[k + 1] = (k + 1) * dt
        xs[k + 1] = x
        es[k + 1] = chain.energy(x[:n], x[n:])
        if stop is not None and stop(ts[k + 1], x):
            ts, xs, us, es = ts[: k + 2], xs[: k + 2], us[: k + 2], es[: k + 2]
            break
    else:
        us[steps] = us[steps - 1] if steps else 0.0
    done = len(ts) - 1
    return Trajectory(t=ts, x=xs, u=us, energy=es, dt=dt, steps=done,
                      saturated_fraction=clipped / max(1, done), diverged=diverged)


def convergence_order(chain: Chain, x0, t_end: float, dt: float, controller=None,
                      refinements: int = 2) -> dict:
    """Estimate the integrator's order from Richardson extrapolation on the final state.

    Returns {'order', 'errors', 'steps'}. RK4 should give about 4. A much lower order means
    the dynamics are not as smooth as the integrator assumes (a saturating or switching
    controller, say), and the step must be chosen by the error, not by the order.
    """
    ctrl = controller or (lambda t, x: np.zeros(chain.m_actuated))
    finals = []
    for i in range(refinements + 2):
        traj = simulate(chain, ctrl, x0, t_end, dt / 2 ** i)
        finals.append(traj.final_state)
    errors = [float(np.max(np.abs(finals[i] - finals[-1]))) for i in range(len(finals) - 1)]
    orders = []
    for a, b in zip(errors, errors[1:]):
        if b > 0 and a > 0:
            orders.append(math.log2(a / b))
    return {"order": (sum(orders) / len(orders)) if orders else float("nan"),
            "errors": errors, "steps": [dt / 2 ** i for i in range(len(finals))]}


def cross_check(f_a, f_b, samples, u_samples=None) -> dict:
    """Compare two state-dynamics callables over the same states; the Phase-1 model check.

    f_a, f_b: f(x, u) -> xdot. samples: iterable of states. u_samples: matching inputs, or
    None for zero input. Returns {'max_abs', 'max_rel', 'worst_state'}: the largest absolute
    and relative disagreement and the state where it happened. Two implementations of the
    same model agree to round-off (about 1e-12 relative); anything larger is a real
    difference in the models, not noise.
    """
    samples = [np.asarray(s, dtype=float) for s in samples]
    if u_samples is None:
        u_samples = [np.zeros(1) for _ in samples]
    worst_abs, worst_rel, worst_state = 0.0, 0.0, None
    for x, u in zip(samples, u_samples):
        a = np.asarray(f_a(x, u), dtype=float)
        b = np.asarray(f_b(x, u), dtype=float)
        gap = float(np.max(np.abs(a - b)))
        scale = max(1e-12, float(np.max(np.abs(a))), float(np.max(np.abs(b))))
        if gap > worst_abs:
            worst_abs, worst_state = gap, x
        worst_rel = max(worst_rel, gap / scale)
    return {"max_abs": worst_abs, "max_rel": worst_rel,
            "worst_state": None if worst_state is None else worst_state.tolist()}


# ----------------------------------------------------------------------------- standard plants

def pendulum(mass: float = 1.0, length: float = 1.0, damping: float = 0.0,
             gravity: float = G_EARTH, point_mass: bool = True) -> Chain:
    """A single pendulum, actuated at its joint. point_mass=False gives a uniform rod."""
    lk = (Link.point_mass(mass, length, damping=damping, name="link1") if point_mass
          else Link.rod(mass, length, damping=damping, name="link1"))
    return Chain([lk], gravity=gravity)


def double_pendulum(m1: float = 1.0, m2: float = 1.0, l1: float = 1.0, l2: float = 1.0,
                    gravity: float = G_EARTH, point_mass: bool = True,
                    actuated=(True, True)) -> Chain:
    """A planar double pendulum. Default: equal point masses on massless rods."""
    build = (lambda m, l, **kw: Link.point_mass(m, l, **kw)) if point_mass else \
        (lambda m, l, **kw: Link.rod(m, l, **kw))
    return Chain([build(m1, l1, actuated=bool(actuated[0]), name="link1"),
                  build(m2, l2, actuated=bool(actuated[1]), name="link2")], gravity=gravity)


def acrobot(m1: float = 1.0, m2: float = 1.0, l1: float = 1.0, l2: float = 1.0,
            lc1: float = 0.5, lc2: float = 0.5, I1: float = 1.0 / 12.0,
            I2: float = 1.0 / 12.0, gravity: float = G_EARTH, damping: float = 0.0) -> Chain:
    """The Acrobot: a double pendulum actuated only at the elbow, joint 1 passive.

    The defaults are two uniform rods of 1 kg and 1 m: lc = L/2 and izz = m L^2 / 12 about
    each rod's centre of mass, so every number is derivable rather than asserted.

    They are NOT "the" Acrobot parameters. Published sets disagree, including on which
    inertia convention they quote, and secondary papers citing the same Spong papers report
    different values for I1 and I2 (compare arXiv:1201.6583, which uses unit inertias, with
    arXiv:2012.11663, which reports I1 = 0.2 and I2 = 1.0 and also attributes them to Spong).
    Take the parameters from whichever paper a run is reproducing and pass them in, and say
    in the analysis which set was used: a swing-up result is not comparable across sets.
    The selftest validates this module against Underactuated Robotics' Acrobot matrices
    symbolically, for arbitrary parameters, so the defaults carry no evidential weight.
    """
    return Chain([Link(mass=m1, length=l1, com=lc1, izz=I1, damping=damping,
                       actuated=False, name="shoulder"),
                  Link(mass=m2, length=l2, com=lc2, izz=I2, damping=damping,
                       actuated=True, name="elbow")], gravity=gravity)


def cartpole_chain(*_args, **_kw):
    """Not a revolute chain: the cart-pole's first joint is prismatic.

    Chain models revolute joints only. The cart-pole is handled in the selftest by comparing
    the published cart-pole matrices against a direct Lagrangian derivation, not through
    Chain. Raised rather than silently returning a pendulum.
    """
    raise NotImplementedError(
        "cart-pole has a prismatic first joint; Chain models revolute joints only")


# ----------------------------------------------------------------------------- selftest

def _tedrake_acrobot_terms(ch: Chain, q, qdot):
    """M, C qdot and tau_g for the Acrobot, written out exactly as Underactuated Robotics
    gives them (https://underactuated.mit.edu/acrobot.html, fetched 2026-10-15):

        M = [[I1 + I2 + m2 l1^2 + 2 m2 l1 lc2 c2, I2 + m2 l1 lc2 c2],
             [I2 + m2 l1 lc2 c2,                  I2]]
        C = [[-2 m2 l1 lc2 s2 qd2, -m2 l1 lc2 s2 qd2],
             [ m2 l1 lc2 s2 qd1,    0]]
        tau_g = [[-m1 g lc1 s1 - m2 g (l1 s1 + lc2 s_{1+2})],
                 [-m2 g lc2 s_{1+2}]]
        B = [[0], [1]]

    with "the moments of inertia I1, I2 taken about the pivots" -- hence izz_pivot below.
    Note this C is NOT the Christoffel factorisation, so only the product C qdot may be
    compared with Chain.coriolis().
    """
    s1, s2 = math.sin(q[0]), math.sin(q[1])
    c2 = math.cos(q[1])
    s12 = math.sin(q[0] + q[1])
    l1, lc1, lc2 = ch.links[0].length, ch.links[0].com, ch.links[1].com
    m1, m2 = ch.links[0].mass, ch.links[1].mass
    I1, I2 = ch.links[0].izz_pivot, ch.links[1].izz_pivot
    g = ch.gravity
    b = m2 * l1 * lc2
    M = np.array([[I1 + I2 + m2 * l1 ** 2 + 2 * b * c2, I2 + b * c2],
                  [I2 + b * c2, I2]])
    C = np.array([[-2 * b * s2 * qdot[1], -b * s2 * qdot[1]],
                  [b * s2 * qdot[0], 0.0]])
    tau_g = np.array([-m1 * g * lc1 * s1 - m2 * g * (l1 * s1 + lc2 * s12),
                      -m2 * g * lc2 * s12])
    return M, C @ np.asarray(qdot, dtype=float), tau_g


def _tedrake_cartpole_accelerations(mc, mp, l, g, theta, thetadot, fx):
    """The cart-pole accelerations exactly as Underactuated Robotics gives them
    (https://underactuated.mit.edu/acrobot.html, fetched 2026-10-15):

        xddot     = [fx + mp sin(th) (l thdot^2 + g cos th)] / (mc + mp sin^2 th)
        thetaddot = [-fx cos th - mp l thdot^2 cos th sin th - (mc + mp) g sin th]
                    / (l (mc + mp sin^2 th))

    Used to check the generic Lagrangian machinery on a chain Chain itself cannot express,
    by building M, C and tau_g for the cart-pole by hand from the same published page:
        M = [[mc + mp, mp l cos th], [mp l cos th, mp l^2]]
        C = [[0, -mp l thdot sin th], [0, 0]], tau_g = [[0], [-mp g l sin th]], B = [[1],[0]]
    """
    s, c = math.sin(theta), math.cos(theta)
    den = mc + mp * s ** 2
    xdd = (fx + mp * s * (l * thetadot ** 2 + g * c)) / den
    thdd = (-fx * c - mp * l * thetadot ** 2 * c * s - (mc + mp) * g * s) / (l * den)
    return xdd, thdd


def selftest(verbose: bool = True) -> bool:
    """Check the module against independent references. Returns True when all pass."""
    ok = True

    def check(name, got, want, tol, note=""):
        nonlocal ok
        got_a, want_a = np.atleast_1d(np.asarray(got, dtype=float)), np.atleast_1d(
            np.asarray(want, dtype=float))
        err = float(np.max(np.abs(got_a - want_a)))
        good = err <= tol
        ok = ok and good
        if verbose:
            print(f"  {'ok  ' if good else 'FAIL'} {name}: max err {err:.3e} (tol {tol:.1e})"
                  + (f"  [{note}]" if note else ""))
        return good

    if verbose:
        print("rigid_body selftest")

    # -- 1. Tedrake's published Acrobot matrices, entry by entry -------------------------
    # Reference: Russ Tedrake, Underactuated Robotics, ch. "Acrobots, Cart-Poles, and
    # Quadrotors", https://underactuated.mit.edu/acrobot.html (fetched 2026-10-15).
    ch = acrobot()
    for q, qdot in [([0.3, -0.7], [1.1, -0.4]), ([math.pi, 0.0], [0.0, 0.0]),
                    ([-1.2, 2.4], [-0.9, 1.7]), ([0.0, 0.0], [2.0, -3.0])]:
        M, Cqd, tg = ch.manipulator_terms(q, qdot)
        M_r, Cqd_r, tg_r = _tedrake_acrobot_terms(ch, q, qdot)
        check(f"Acrobot M(q) vs Underactuated, q={q}", M, M_r, 1e-6)
        check(f"Acrobot C(q,qdot) qdot vs Underactuated, q={q}", Cqd, Cqd_r, 1e-5)
        check(f"Acrobot tau_g(q) vs Underactuated, q={q}", tg, tg_r, 1e-9)
    check("Acrobot B", ch.B, [[0.0], [1.0]], 0.0)
    # The same comparison for parameter sets nothing in this module was built around, so the
    # agreement is with the published equations, not with one convenient set of numbers.
    rng0 = np.random.default_rng(11)
    for _ in range(4):
        p = rng0.uniform(0.3, 3.0, 6)
        other = acrobot(m1=p[0], m2=p[1], l1=p[2], l2=p[3], lc1=p[2] * 0.4, lc2=p[3] * 0.7,
                        I1=p[4] * 0.1, I2=p[5] * 0.1, gravity=9.80665)
        q, qdot = [0.9, -1.4], [0.7, 2.1]
        M, Cqd, tg = other.manipulator_terms(q, qdot)
        M_r, Cqd_r, tg_r = _tedrake_acrobot_terms(other, q, qdot)
        check(f"Acrobot vs Underactuated, m=({p[0]:.2f},{p[1]:.2f}) l=({p[2]:.2f},{p[3]:.2f})",
              np.concatenate([M.ravel(), Cqd, tg]),
              np.concatenate([M_r.ravel(), Cqd_r, tg_r]), 1e-5)

    # -- 2. the cart-pole: the same Lagrangian machinery on a published second system -----
    # Chain cannot express a prismatic joint, so M, C and tau_g are taken from the published
    # page and checked against the page's own solved accelerations: an independent check that
    # the manipulator form and the solved form agree, and that this module's forward-dynamics
    # solve (M^-1 (tau_g + Bu - C qdot)) is the same operation.
    mc, mp, l, g = 1.0, 0.3, 0.5, 9.81
    for theta, thetadot, fx in [(0.4, -1.0, 2.0), (-1.3, 2.2, -1.5), (3.0, 0.1, 0.0)]:
        s, c = math.sin(theta), math.cos(theta)
        M = np.array([[mc + mp, mp * l * c], [mp * l * c, mp * l ** 2]])
        Cqd = np.array([[0.0, -mp * l * thetadot * s], [0.0, 0.0]]) @ np.array([0.0, thetadot])
        tau_g = np.array([0.0, -mp * g * l * s])
        acc = np.linalg.solve(M, tau_g + np.array([1.0, 0.0]) * fx - Cqd)
        want = _tedrake_cartpole_accelerations(mc, mp, l, g, theta, thetadot, fx)
        check(f"cart-pole manipulator form vs solved form, th={theta}", acc, want, 1e-9)

    # -- 3. small-oscillation frequencies, closed form ------------------------------------
    # Point-mass pendulum about hanging: omega = sqrt(g/l).  Uniform rod about its end:
    # omega = sqrt(3g/2L) (I_pivot = mL^2/3, torque arm L/2).  Both are standard results.
    for l_ in (0.5, 1.0, 2.5):
        p = pendulum(mass=2.0, length=l_)
        M = p.mass_matrix([0.0])[0, 0]
        k = 2.0 * p.gravity * l_                      # -d tau_g/dq at q = 0
        check(f"point-mass pendulum omega, l={l_}", math.sqrt(k / M),
              math.sqrt(p.gravity / l_), 1e-9, "sqrt(g/l)")
        r = pendulum(mass=2.0, length=l_, point_mass=False)
        Mr = r.mass_matrix([0.0])[0, 0]
        kr = 2.0 * r.gravity * (l_ / 2.0)
        check(f"uniform-rod pendulum omega, L={l_}", math.sqrt(kr / Mr),
              math.sqrt(3 * r.gravity / (2 * l_)), 1e-9, "sqrt(3g/2L)")

    # -- 4. double-pendulum normal modes, closed form -------------------------------------
    # Two equal point masses m on massless rods of equal length l, linearised about hanging:
    # det(K - w^2 M) = 0 with M = m l^2 [[2,1],[1,1]], K = m g l diag(2,1) gives
    # lambda^2 - 4 lambda + 2 = 0 for lambda = w^2 l / g, so w^2 = (2 -+ sqrt 2) g / l.
    # The quadratic's roots are algebra, independent of the eigenvalue solve below.
    import numpy.linalg as la
    for l_ in (0.7, 1.0, 1.9):
        dp = double_pendulum(m1=1.3, m2=1.3, l1=l_, l2=l_)
        M = dp.mass_matrix([0.0, 0.0])
        eps = 1e-6
        K = np.zeros((2, 2))
        for j in range(2):
            step = np.zeros(2)
            step[j] = eps
            K[:, j] = -(dp.gravity_torque(step) - dp.gravity_torque(-step)) / (2 * eps)
        w2 = sorted(np.real(la.eigvals(la.solve(M, K))))
        want = sorted([(2 - math.sqrt(2)) * dp.gravity / l_,
                       (2 + math.sqrt(2)) * dp.gravity / l_])
        check(f"double-pendulum normal modes, l={l_}", w2, want, 1e-6,
              "w^2 = (2 -+ sqrt2) g/l")

    # -- 5. the passivity identity Mdot = C + C^T -----------------------------------------
    # A property of the Christoffel factorisation (Spong & Vidyasagar; Siciliano et al.),
    # and the check that catches an M and C that disagree.
    for q, qdot in [([0.3, -0.7], [1.1, -0.4]), ([2.0, 1.0], [-2.0, 0.5])]:
        check(f"passivity residual at q={q}", ch.passivity_residual(q, qdot), 0.0, 1e-6)

    # -- 6. energy conservation and integrator order ---------------------------------------
    traj = simulate(ch, lambda t, x: [0.0], [0.6, -0.3, 0.0, 0.0], 10.0, 1e-3)
    check("Acrobot energy drift over 10 s, RK4 at 1 ms", traj.energy_drift, 0.0, 1e-9,
          "unforced and undamped")
    conv = convergence_order(ch, [0.6, -0.3, 0.0, 0.0], 2.0, 4e-3)
    good = 3.5 <= conv["order"] <= 4.6
    ok = ok and good
    if verbose:
        print(f"  {'ok  ' if good else 'FAIL'} RK4 convergence order: {conv['order']:.2f} "
              "(expect about 4)")
    # damping must remove energy, and a positive torque on the elbow must add some
    damped = simulate(Chain([replace(ch.links[0], damping=0.4), replace(ch.links[1], damping=0.4)],
                            gravity=ch.gravity), lambda t, x: [0.0],
                      [0.6, -0.3, 0.0, 0.0], 10.0, 1e-3)
    good = damped.energy[-1] < damped.energy[0] - 1e-3
    ok = ok and good
    if verbose:
        print(f"  {'ok  ' if good else 'FAIL'} viscous damping removes energy: "
              f"{damped.energy[0]:.4f} -> {damped.energy[-1]:.4f} J")

    # -- 7. symbolic and numeric agree -----------------------------------------------------
    try:
        import sympy as sp
        Ms, Cs, Ts, (qs, vs, gs) = ch.symbolic()
        sub = {qs[0]: 0.3, qs[1]: -0.7, vs[0]: 1.1, vs[1]: -0.4, gs: ch.gravity}
        check("symbolic M == numeric M", np.array(sp.Matrix(Ms).subs(sub), dtype=float),
              ch.mass_matrix([0.3, -0.7]), 1e-9)
        check("symbolic C qdot == numeric C qdot",
              np.array(sp.Matrix(Cs).subs(sub), dtype=float) @ np.array([1.1, -0.4]),
              ch.coriolis([0.3, -0.7], [1.1, -0.4]) @ np.array([1.1, -0.4]), 1e-6)
        check("symbolic tau_g == numeric tau_g",
              np.array(sp.Matrix(Ts).subs(sub), dtype=float).ravel(),
              ch.gravity_torque([0.3, -0.7]), 1e-9)
    except ImportError:
        if verbose:
            print("  skip sympy checks (sympy not installed)")

    # -- 8. the two implementations against each other -------------------------------------
    # The compiled symbolic path and the Jacobian/finite-difference reference path share no
    # code below the geometry, so agreeing to the reference's own differencing error (about
    # 1e-9) is a real check on both. This is also what cross_check() is for.
    rng1 = np.random.default_rng(7)
    states = rng1.uniform(-3.0, 3.0, (30, 4))
    cc = cross_check(ch.state_dynamics(), ch.state_dynamics_reference(), states,
                     [rng1.uniform(-5.0, 5.0, 1) for _ in range(30)])
    check("compiled dynamics vs reference dynamics", cc["max_rel"], 0.0, 1e-7,
          "relative; the reference differences M numerically")
    bare = Chain(ch.links, gravity=ch.gravity, compile=False)
    check("compile=False gives the reference path", bare.mass_matrix([0.3, -0.7]),
          ch.mass_matrix([0.3, -0.7]), 1e-9)
    # cross_check must also be able to FAIL: a chain with a 10 per cent heavier second link
    # is a different model, and the check has to say so rather than smoothing it over.
    heavier = acrobot(m2=1.1)
    cc_bad = cross_check(ch.state_dynamics(), heavier.state_dynamics(), states,
                         [np.zeros(1) for _ in range(30)])
    check_bigger = cc_bad["max_rel"] > 1e-3
    ok = ok and check_bigger
    if verbose:
        print(f"  {'ok  ' if check_bigger else 'FAIL'} cross_check detects a 10 per cent mass "
              f"error: max_rel {cc_bad['max_rel']:.3e}")

    # -- 9. the inertia convention ---------------------------------------------------------
    lk = Link.rod(2.0, 3.0)
    check("rod izz about com", lk.izz, 2.0 * 9.0 / 12.0, 1e-12, "m L^2 / 12")
    check("rod izz about pivot", lk.izz_pivot, 2.0 * 9.0 / 3.0, 1e-12, "m L^2 / 3")
    try:
        Link.from_pivot_inertia(1.0, 1.0, 0.5, 0.1)   # below m d^2 = 0.25
        ok = False
        if verbose:
            print("  FAIL from_pivot_inertia accepted an impossible inertia")
    except ValueError:
        if verbose:
            print("  ok   from_pivot_inertia refuses an inertia below m d^2")

    if verbose:
        print("PASS" if ok else "FAIL")
    return ok


# ----------------------------------------------------------------------------- CLI

def _main(argv) -> int:
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    cmd = argv[1]
    if cmd == "selftest":
        return 0 if selftest() else 1
    if cmd == "symbolic":
        import sympy as sp
        name = argv[2] if len(argv) > 2 else "acrobot"
        ch = {"acrobot": acrobot, "pendulum": pendulum,
              "double_pendulum": double_pendulum}[name]()
        M, C, tg, _ = ch.symbolic()
        print(f"{name}: M =\n{sp.pretty(M)}\n\nC =\n{sp.pretty(C)}\n\ntau_g =\n{sp.pretty(tg)}")
        return 0
    if cmd in ("acrobot", "pendulum", "double_pendulum"):
        ch = {"acrobot": acrobot, "pendulum": pendulum, "double_pendulum": double_pendulum}[cmd]()
        state = [float(v) for v in argv[argv.index("--state") + 1:]] if "--state" in argv \
            else [0.1] * ch.n + [0.0] * ch.n
        q, qd = state[: ch.n], state[ch.n:]
        print(f"{ch}\nq = {q}  qdot = {qd}")
        print(f"M(q) =\n{ch.mass_matrix(q)}")
        print(f"C(q,qdot) qdot = {ch.coriolis(q, qd) @ np.asarray(qd)}")
        print(f"tau_g(q) = {ch.gravity_torque(q)}")
        print(f"qddot (u = 0) = {ch.forward_dynamics(q, qd, np.zeros(ch.m_actuated))}")
        print(f"E = {ch.energy(q, qd):.6f} J   (upright potential "
              f"{ch.upright_energy():.6f} J)")
        print(f"passivity residual = {ch.passivity_residual(q, qd):.3e}")
        return 0
    print(f"unknown command: {cmd}\n{__doc__}")
    return 2


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
