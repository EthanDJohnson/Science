#!/usr/bin/env python3
"""Linear control synthesis and analysis, with honest labels on what is proved and what is sampled.

WHAT IT COMPUTES
    linearize           A, B from any f(x, u) by central differences, with a step study
    controllability     Kalman rank, the smallest singular value, and the PBH test per mode
    observability       the same for (A, C)
    lqr / dlqr          continuous and discrete LQR: gain K, cost-to-go S, closed-loop poles
    lyapunov            A^T P + P A = -Q
    loop_margins        gain, phase and DELAY margin of a scalar loop L(s)
    state_feedback_margins   the same for L(s) = K (sI - A)^-1 B
    roa_sample          a SAMPLED estimate of a quadratic region of attraction
    roa_simulated       the same, verified by integrating the nonlinear plant
    robustness_sweep    success rate under parameter error, with a binomial interval

WHAT IS PROVED AND WHAT IS NOT
    lqr, lyapunov, controllability and the margins are exact linear algebra on the model you
    pass: they are proofs about that model and say nothing about the real system beyond it.
    roa_sample and roa_simulated are SAMPLED: they test a finite set of points, so they can
    only ever shrink an estimate, never certify one. A certified region needs a
    sum-of-squares programme (Tedrake, Underactuated Robotics, ch. "Lyapunov Analysis":
    "perform a simple line search on rho to find the largest value for which the convex
    optimization returns a feasible solution"), which needs an SDP solver this toolkit does
    not carry. Report a sampled region as "largest sampled level set", never as "the region
    of attraction", and say how many samples it rests on.

    A linear-model margin is also not a robustness claim about the nonlinear plant. LQR state
    feedback has an infinite gain margin and at least 60 degrees of phase margin (Safonov and
    Athans, "Gain and phase margin for multiloop LQG regulators", IEEE TAC 22 (1977) 173-179,
    doi:10.1109/tac.1977.1101470) -- a guarantee that holds at the plant input of the exact
    model, and that says nothing about an unmodelled delay in a different loop, a torque limit
    or an unmodelled mode. The selftest checks the 60-degree property numerically.

CONVENTIONS
    State-space xdot = A x + B u, feedback u = -K (x - x*), cost J = int x^T Q x + u^T R u dt,
    so Q penalises state error (units: cost per unit state^2 per second) and R penalises
    control effort (cost per unit u^2 per second). Only the RATIO matters: scaling Q and R
    together leaves K unchanged. The practical reading is Bryson's rule -- set Q_ii = 1 /
    (largest acceptable error in state i)^2 and R_jj = 1 / (largest acceptable effort in
    actuator j)^2 -- which makes each diagonal entry a statement about a tolerance, in that
    state's own units, rather than a free knob.

UNITS
    SI, radians, seconds. Frequencies are rad/s, not Hz. Margins: gain as a plain ratio (and
    in dB alongside), phase in degrees, delay in seconds.

PYTHON USAGE
    import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
    import numpy as np
    from rigid_body import acrobot
    from control_tools import linearize, lqr, state_feedback_margins, roa_simulated
    ch = acrobot()
    f = ch.state_dynamics()
    x_up = np.array([np.pi, 0.0, 0.0, 0.0])
    A, B, info = linearize(f, x_up, np.zeros(1))
    out = lqr(A, B, np.diag([10.0, 10.0, 1.0, 1.0]), np.eye(1))
    print(out["K"], out["closed_loop_poles"])

COMMAND LINE
    python3 .claude/skills/conundrum/scripts/control_tools.py selftest
    python3 .claude/skills/conundrum/scripts/control_tools.py acrobot-lqr
"""
from __future__ import annotations

import math
import sys
from typing import Callable, Sequence

try:
    import numpy as np
except ImportError:  # pragma: no cover
    raise SystemExit("control_tools.py needs numpy: python3 -m pip install numpy")

try:
    from scipy.linalg import solve_continuous_are, solve_discrete_are, solve_sylvester
    _HAVE_SCIPY = True
except ImportError:  # pragma: no cover - the pipeline installs scipy at preflight
    _HAVE_SCIPY = False

__all__ = ["linearize", "controllability", "observability", "lqr", "dlqr", "lyapunov",
           "loop_margins", "state_feedback_margins", "roa_sample", "roa_simulated",
           "robustness_sweep"]


def _need_scipy(what: str) -> None:
    if not _HAVE_SCIPY:
        raise RuntimeError(f"{what} needs scipy: python3 -m pip install scipy")


# ----------------------------------------------------------------------------- linearisation

def linearize(f: Callable, x0, u0, eps: float = None, refine: bool = True) -> tuple:
    """A = df/dx and B = df/du at (x0, u0) by central differences.

    eps defaults to a per-coordinate step scaled by the coordinate's own size, which keeps
    the truncation and round-off errors comparable. With refine=True the Jacobian is computed
    at eps and eps/2 and the two are compared; info['step_sensitivity'] is the largest
    disagreement, scaled by the matrix norm. A value above about 1e-5 means the step is in
    the round-off floor or f is not smooth here, and the linearisation should not be trusted
    to more digits than that.

    info also carries 'residual' = |f(x0, u0)|, which must be ~0 at an equilibrium. A
    non-zero residual means x0 is not a fixed point, and every eigenvalue below is about a
    point the system is not sitting at: the single most common silent error in a balance
    controller.
    """
    x0 = np.asarray(x0, dtype=float)
    u0 = np.atleast_1d(np.asarray(u0, dtype=float))
    n, m = x0.size, u0.size

    def jac(h_scale):
        A = np.zeros((n, n))
        for j in range(n):
            h = (eps if eps is not None else 1e-5 * max(1.0, abs(x0[j]))) * h_scale
            e = np.zeros(n)
            e[j] = h
            A[:, j] = (np.asarray(f(x0 + e, u0), dtype=float)
                       - np.asarray(f(x0 - e, u0), dtype=float)) / (2 * h)
        B = np.zeros((n, m))
        for j in range(m):
            h = (eps if eps is not None else 1e-5 * max(1.0, abs(u0[j]))) * h_scale
            e = np.zeros(m)
            e[j] = h
            B[:, j] = (np.asarray(f(x0, u0 + e), dtype=float)
                       - np.asarray(f(x0, u0 - e), dtype=float)) / (2 * h)
        return A, B

    A, B = jac(1.0)
    info = {"residual": float(np.max(np.abs(np.asarray(f(x0, u0), dtype=float)))),
            "step_sensitivity": float("nan")}
    if refine:
        A2, B2 = jac(0.5)
        scale = max(1.0, float(np.max(np.abs(A))), float(np.max(np.abs(B))))
        info["step_sensitivity"] = float(
            max(np.max(np.abs(A - A2)), np.max(np.abs(B - B2))) / scale)
    info["eigenvalues"] = np.linalg.eigvals(A)
    info["unstable_modes"] = int(np.sum(np.real(info["eigenvalues"]) > 1e-9))
    return A, B, info


# ----------------------------------------------------------------------------- structure

def controllability(A, B, tol: float = None) -> dict:
    """Kalman rank, conditioning, and which modes are uncontrollable (PBH test).

    Returns {'rank', 'n', 'controllable', 'min_singular_value', 'condition',
    'uncontrollable_modes'}. A full rank with a tiny smallest singular value means
    controllable in principle and barely so in practice: the control effort needed to move
    the weak direction grows like 1/sigma_min. For an underactuated robot that number, not
    the rank, is what decides whether a controller is implementable.
    """
    A = np.atleast_2d(np.asarray(A, dtype=float))
    B = np.atleast_2d(np.asarray(B, dtype=float))
    n = A.shape[0]
    if A.shape[0] != A.shape[1]:
        raise ValueError(f"A must be square, got {A.shape}")
    if B.shape[0] != n:
        raise ValueError(f"B must have {n} rows, got {B.shape}")
    blocks = [B]
    for _ in range(n - 1):
        blocks.append(A @ blocks[-1])
    ctrb = np.hstack(blocks)
    sv = np.linalg.svd(ctrb, compute_uv=False)
    tol = tol if tol is not None else sv[0] * max(ctrb.shape) * np.finfo(float).eps
    rank = int(np.sum(sv > tol))
    bad = []
    for lam in np.linalg.eigvals(A):
        # Popov-Belevitch-Hautus: [lam I - A, B] must have rank n for every eigenvalue
        mat = np.hstack([lam * np.eye(n) - A, B.astype(complex)])
        s = np.linalg.svd(mat, compute_uv=False)
        if int(np.sum(s > s[0] * max(mat.shape) * np.finfo(float).eps)) < n:
            bad.append(complex(lam))
    return {"rank": rank, "n": n, "controllable": rank == n,
            "min_singular_value": float(sv[-1]), "condition": float(sv[0] / max(sv[-1], 1e-300)),
            "uncontrollable_modes": bad}


def observability(A, C, tol: float = None) -> dict:
    """The dual of controllability: observable iff (A^T, C^T) is controllable."""
    A = np.atleast_2d(np.asarray(A, dtype=float))
    C = np.atleast_2d(np.asarray(C, dtype=float))
    out = controllability(A.T, C.T, tol=tol)
    return {"rank": out["rank"], "n": out["n"], "observable": out["controllable"],
            "min_singular_value": out["min_singular_value"], "condition": out["condition"],
            "unobservable_modes": out["uncontrollable_modes"]}


# ----------------------------------------------------------------------------- synthesis

def _check_weights(Q, R, n, m):
    Q = np.atleast_2d(np.asarray(Q, dtype=float))
    R = np.atleast_2d(np.asarray(R, dtype=float))
    if Q.shape != (n, n):
        raise ValueError(f"Q must be {n}x{n}, got {Q.shape}")
    if R.shape != (m, m):
        raise ValueError(f"R must be {m}x{m}, got {R.shape}")
    if np.min(np.linalg.eigvalsh(0.5 * (Q + Q.T))) < -1e-10:
        raise ValueError("Q must be positive semidefinite")
    if np.min(np.linalg.eigvalsh(0.5 * (R + R.T))) <= 0:
        raise ValueError("R must be positive definite (a zero entry means free control effort)")
    return 0.5 * (Q + Q.T), 0.5 * (R + R.T)


def lqr(A, B, Q, R) -> dict:
    """Continuous infinite-horizon LQR.

    Solves 0 = S A + A^T S - S B R^-1 B^T S + Q and returns
    {'K', 'S', 'closed_loop_poles', 'are_residual', 'stable'} with K = R^-1 B^T S and
    u = -K x. are_residual is the largest entry of the Riccati residual: a value that is not
    near zero means the solver returned something that does not solve the equation, which
    happens when (A, B) is not stabilisable, and the gain must not be used.
    """
    _need_scipy("lqr")
    A = np.atleast_2d(np.asarray(A, dtype=float))
    B = np.atleast_2d(np.asarray(B, dtype=float))
    n, m = A.shape[0], B.shape[1]
    Q, R = _check_weights(Q, R, n, m)
    ctrb = controllability(A, B)
    if not ctrb["controllable"]:
        unstable = [z for z in ctrb["uncontrollable_modes"] if z.real > -1e-9]
        if unstable:
            raise ValueError(
                f"(A, B) is not stabilisable: the uncontrollable modes {unstable} are not "
                "strictly stable, so no LQR gain exists")
    S = solve_continuous_are(A, B, Q, R)
    K = np.linalg.solve(R, B.T @ S)
    residual = S @ A + A.T @ S - S @ B @ np.linalg.solve(R, B.T @ S) + Q
    poles = np.linalg.eigvals(A - B @ K)
    return {"K": K, "S": S, "closed_loop_poles": poles,
            "are_residual": float(np.max(np.abs(residual))),
            "stable": bool(np.all(np.real(poles) < 0)),
            "cost_to_go": lambda x: float(np.asarray(x) @ S @ np.asarray(x))}


def dlqr(A, B, Q, R, dt: float = None) -> dict:
    """Discrete LQR for x[k+1] = A x[k] + B u[k].

    Pass dt only to record it in the result; A and B must already be the discrete-time
    matrices. Poles are inside the unit circle for a stable loop, so 'stable' tests |z| < 1.
    """
    _need_scipy("dlqr")
    A = np.atleast_2d(np.asarray(A, dtype=float))
    B = np.atleast_2d(np.asarray(B, dtype=float))
    n, m = A.shape[0], B.shape[1]
    Q, R = _check_weights(Q, R, n, m)
    S = solve_discrete_are(A, B, Q, R)
    K = np.linalg.solve(R + B.T @ S @ B, B.T @ S @ A)
    residual = A.T @ S @ A - S - A.T @ S @ B @ K + Q
    poles = np.linalg.eigvals(A - B @ K)
    return {"K": K, "S": S, "closed_loop_poles": poles, "dt": dt,
            "are_residual": float(np.max(np.abs(residual))),
            "stable": bool(np.all(np.abs(poles) < 1.0))}


def zoh_discretize(A, B, dt: float) -> tuple:
    """Exact zero-order-hold discretisation by the matrix exponential of [[A, B], [0, 0]]."""
    from scipy.linalg import expm
    A = np.atleast_2d(np.asarray(A, dtype=float))
    B = np.atleast_2d(np.asarray(B, dtype=float))
    n, m = A.shape[0], B.shape[1]
    block = np.zeros((n + m, n + m))
    block[:n, :n] = A
    block[:n, n:] = B
    E = expm(block * dt)
    return E[:n, :n], E[:n, n:]


def lyapunov(A, Q) -> dict:
    """Solve A^T P + P A = -Q and report whether P is positive definite.

    P > 0 with Q > 0 certifies that A is stable, and V = x^T P x is then a Lyapunov function
    for the linear system (and for the nonlinear system near the fixed point).
    """
    _need_scipy("lyapunov")
    A = np.atleast_2d(np.asarray(A, dtype=float))
    Q = np.atleast_2d(np.asarray(Q, dtype=float))
    P = solve_sylvester(A.T, A, -Q)
    P = 0.5 * (P + P.T)
    return {"P": P, "residual": float(np.max(np.abs(A.T @ P + P @ A + Q))),
            "positive_definite": bool(np.min(np.linalg.eigvalsh(P)) > 0),
            "min_eigenvalue": float(np.min(np.linalg.eigvalsh(P)))}


# ----------------------------------------------------------------------------- margins

def loop_margins(L: Callable[[complex], complex], w_min: float = 1e-3, w_max: float = 1e4,
                 points: int = 4001) -> dict:
    """Gain, phase and delay margin of a scalar loop transfer function L(s).

    L: a callable taking a complex s and returning a complex scalar (the loop gain, so the
    closed loop is 1 / (1 + L)). Returns
      {'gain_margin', 'gain_margin_db', 'gain_margin_up', 'gain_margin_down',
       'w_phase_crossover', 'phase_margin_deg', 'w_gain_crossover', 'delay_margin'}
    with inf (or 0 for gain_margin_down) where no crossing exists in [w_min, w_max].

    GAIN MARGIN HAS TWO SIDES, and conflating them inverts the conclusion. Each crossing of
    -180 degrees gives a factor 1/|L| by which the gain may change before the loop goes
    unstable. A factor above 1 is headroom for MORE gain (gain_margin_up); a factor below 1
    is headroom for LESS (gain_margin_down). 'gain_margin' is the conventional single number,
    the 1/|L| closest to instability, which is what MATLAB's margin() returns and which can
    be less than 1: read on its own, a reported "gain margin of 0.1" looks terrible and in
    fact means the loop tolerates any gain increase and a tenfold decrease. LQR state
    feedback is exactly this case: infinite up, 0.5 down.

    The delay margin is phase_margin (radians) / gain-crossover frequency: the smallest pure
    time delay anywhere in the loop that drives it unstable. For a sampled controller, a
    sample period T contributes about T/2 of delay on top of any computation and
    communication latency, so a loop with a 10 ms delay margin cannot be run at 100 Hz.

    Crossings are located on a log grid and then refined by bisection on L itself, so the
    result is accurate to about 1e-12 in frequency and does not depend on the grid density --
    but the grid must still bracket the crossings: start w_min below every pole and zero of
    interest and w_max above them. Two crossings closer together than the grid spacing can be
    missed, so widen `points` rather than the band if a margin looks implausible.
    """
    if w_min <= 0 or w_max <= w_min:
        raise ValueError("need 0 < w_min < w_max")
    w = np.logspace(math.log10(w_min), math.log10(w_max), points)
    vals = np.array([L(1j * float(wi)) for wi in w])
    mag = np.abs(vals)

    def bisect(g, a, b, iterations: int = 80):
        ga = g(a)
        for _ in range(iterations):
            mid = math.sqrt(a * b)            # geometric bisection: the grid is logarithmic
            gm_ = g(mid)
            if (gm_ > 0) == (ga > 0):
                a, ga = mid, gm_
            else:
                b = mid
        return math.sqrt(a * b)

    def brackets(y):
        s = np.sign(y)
        return np.where(s[:-1] * s[1:] < 0)[0]

    # Crossings of 180 degrees, found as sign changes of Im L with Re L < 0 -- the exact
    # condition, and the only formulation that does not depend on phase bookkeeping. Locating
    # them on the unwrapped phase instead misses half of them: a loop whose phase RISES
    # through +180 degrees, which is what an open-loop-unstable plant does, never makes
    # (phase + pi) change sign even though +180 and -180 are the same point on the circle.
    # Refining on Im L also avoids numpy's branch cut at +-pi, which sits on the crossing.
    up, down = math.inf, 0.0
    w_up, w_down = math.inf, math.inf
    for i in brackets(np.imag(vals)):
        wc = bisect(lambda x: float(np.imag(L(1j * x))), float(w[i]), float(w[i + 1]))
        value = L(1j * wc)
        if value.real >= 0:
            continue
        amp = abs(value)
        if amp <= 0:
            continue
        factor = 1.0 / amp
        if factor > 1.0:
            if factor < up:
                up, w_up = factor, wc
        elif factor > down:
            down, w_down = factor, wc
    # the conventional single number: the crossing closest to instability in log terms
    if up < math.inf and (down == 0.0 or math.log(up) <= -math.log(down)):
        gm, w_pc = up, w_up
    elif down > 0.0:
        gm, w_pc = down, w_down
    else:
        gm, w_pc = math.inf, math.inf

    # Unity-gain crossings, and from them the phase and delay margins.
    #
    # A pure delay has unit magnitude at every frequency, so it can only move phase: the
    # closed loop 1 + L(jw) e^{-jw tau} can first reach the stability boundary only where
    # |L(jw)| = 1. At such a crossing with phase phi, the smallest added lag that puts the
    # loop on the boundary is theta* = (phi + pi) mod 2pi, and the delay that produces it is
    # theta*/w. The true delay margin is the SMALLEST theta*/w over every unity-gain
    # crossing, which need not be the crossing with the smallest theta*. Taking the modulus
    # per crossing also removes the branch ambiguity in the unwrapped phase, which is what
    # makes the textbook "180 + unwrapped phase" formula return nonsense (phase margins
    # above 180 degrees, and delay margins orders of magnitude too large) on an
    # open-loop-unstable plant such as a robot balancing at an inverted equilibrium.
    pm, w_gc, dm = math.inf, math.inf, math.inf
    crossings_gc = []
    for i in brackets(mag - 1.0):
        wc = bisect(lambda x: abs(L(1j * x)) - 1.0, float(w[int(i)]), float(w[int(i) + 1]))
        phi = float(np.angle(L(1j * wc)))
        theta = (phi + math.pi) % (2 * math.pi)       # smallest positive destabilising lag
        crossings_gc.append({"w": wc, "phase_margin_deg": math.degrees(theta),
                             "delay_margin": theta / wc if wc > 0 else 0.0})
    if crossings_gc:
        worst = min(crossings_gc, key=lambda c: c["delay_margin"])
        dm = worst["delay_margin"]
        pm = worst["phase_margin_deg"]
        w_gc = worst["w"]
    return {"gain_margin": gm,
            "gain_margin_db": (20 * math.log10(gm) if 0 < gm < math.inf else
                               (math.inf if gm == math.inf else -math.inf)),
            "gain_margin_up": up, "gain_margin_down": down,
            "w_phase_crossover": w_pc, "phase_margin_deg": pm,
            "w_gain_crossover": w_gc, "delay_margin": dm,
            "gain_crossovers": crossings_gc}


def state_feedback_margins(A, B, K, **kw) -> dict:
    """Margins of the loop broken at the plant input: L(s) = K (sI - A)^-1 B.

    Single input only (B one column, K one row). This is the loop LQR's guarantee applies
    to; breaking the loop at a sensor instead gives different, usually worse, margins.
    """
    A = np.atleast_2d(np.asarray(A, dtype=float))
    B = np.atleast_2d(np.asarray(B, dtype=float))
    K = np.atleast_2d(np.asarray(K, dtype=float))
    if B.shape[1] != 1 or K.shape[0] != 1:
        raise ValueError("state_feedback_margins handles one input only; B must be n x 1 "
                         f"and K 1 x n, got {B.shape} and {K.shape}")
    n = A.shape[0]
    eye = np.eye(n)

    def L(s):
        return complex((K @ np.linalg.solve(s * eye - A, B))[0, 0])
    return loop_margins(L, **kw)


# ----------------------------------------------------------------------------- regions

def roa_sample(f: Callable, x_star, P, u_of_x=None, rho_max: float = None,
               samples: int = 2000, levels: int = 40, rng=None) -> dict:
    """Largest SAMPLED level set of V = (x - x*)^T P (x - x*) on which Vdot < 0.

    Samples points on each level set's surface and shrinks rho until every sample has
    Vdot < 0. This can only overestimate Vdot's worst case from a finite sample, so the
    answer is an UPPER bound on the certifiable level set and a guess at the true region.
    Report it as such, with the sample count.

    f: f(x, u) -> xdot. u_of_x: the controller, u = u_of_x(x); None means zero input.
    Returns {'rho', 'rho_max', 'samples_per_level', 'worst_point', 'margin'}.
    """
    x_star = np.asarray(x_star, dtype=float)
    P = np.atleast_2d(np.asarray(P, dtype=float))
    n = x_star.size
    rng = np.random.default_rng(0 if rng is None else rng) if not isinstance(
        rng, np.random.Generator) else rng
    ctrl = u_of_x or (lambda x: np.zeros(1))
    # a scale for rho: the level set that reaches about 1 rad / 1 rad per s in every direction
    if rho_max is None:
        rho_max = float(np.max(np.linalg.eigvalsh(P)))
    L = np.linalg.cholesky(P)
    best_rho, worst_point, margin = 0.0, None, math.inf
    for rho in np.linspace(rho_max, rho_max / levels, levels):
        pts = rng.normal(size=(samples, n))
        pts /= np.linalg.norm(pts, axis=1, keepdims=True)
        # map the unit sphere onto the ellipsoid V = rho:  x = x* + sqrt(rho) L^-T v
        shell = x_star + math.sqrt(rho) * (np.linalg.solve(L.T, pts.T)).T
        worst, where = -math.inf, None
        for x in shell:
            dx = x - x_star
            xdot = np.asarray(f(x, np.atleast_1d(ctrl(x))), dtype=float)
            vdot = float(2.0 * dx @ P @ xdot)
            if vdot > worst:
                worst, where = vdot, x
        if worst < 0:
            best_rho, worst_point, margin = float(rho), where, worst
            break
    return {"rho": best_rho, "rho_max": float(rho_max), "samples_per_level": samples,
            "worst_point": None if worst_point is None else np.asarray(worst_point).tolist(),
            "margin": margin, "certified": False,
            "note": "sampled, not certified: a finite sample cannot bound Vdot's worst case"}


def roa_simulated(step: Callable, x_star, directions, tolerance: float, t_end: float,
                  bracket=(1e-3, 3.0), iterations: int = 14, error: Callable = None) -> dict:
    """How far off the fixed point the closed loop still recovers, by simulation.

    step(x0, t_end) -> final state (or a trajectory whose last state is used); the caller
    supplies the whole closed-loop simulation, so torque limits, noise and delay are included
    exactly as they will be in the real run. For each direction in `directions` (vectors in
    state space), a bisection finds the largest multiple alpha for which the final state is
    within `tolerance` of x*. Returns {'per_direction': [...], 'min', 'max', 'tolerance'}
    with alpha in the units of each direction vector.

    error(x_final, x_star) -> vector, defaulting to x_final - x_star. PASS AN ERROR FUNCTION
    WHENEVER A COORDINATE IS AN ANGLE. A revolute joint lives on a circle, so a controller
    that recovers the upright posture after swinging through a full turn ends at q + 2 pi and
    a plain subtraction calls that a failure, shrinking the reported region to nothing for a
    reason that has no physical content. For a chain of revolute joints:
        err = lambda x, s: np.concatenate([(x[:n] - s[:n] + np.pi) % (2*np.pi) - np.pi,
                                           x[n:] - s[n:]])

    This is the practical region of attraction, and the only kind this toolkit can report
    with a torque limit in the loop. It is still sampled: it tests the directions given, and
    the recovered set is generally not a ball, so report the per-direction numbers, not only
    the minimum.
    """
    x_star = np.asarray(x_star, dtype=float)
    err = error or (lambda x, s: np.asarray(x, dtype=float) - np.asarray(s, dtype=float))
    out = []
    for d in directions:
        d = np.asarray(d, dtype=float)
        lo, hi = bracket
        if not _recovers(step, x_star, d, lo, tolerance, t_end, err):
            out.append({"direction": d.tolist(), "alpha": 0.0, "note": "fails even at the "
                        "smallest bracket value"})
            continue
        if _recovers(step, x_star, d, hi, tolerance, t_end, err):
            out.append({"direction": d.tolist(), "alpha": float(hi),
                        "note": "recovers at the top of the bracket; widen it"})
            continue
        for _ in range(iterations):
            mid = 0.5 * (lo + hi)
            if _recovers(step, x_star, d, mid, tolerance, t_end, err):
                lo = mid
            else:
                hi = mid
        out.append({"direction": d.tolist(), "alpha": float(lo)})
    alphas = [o["alpha"] for o in out]
    return {"per_direction": out, "min": min(alphas) if alphas else 0.0,
            "max": max(alphas) if alphas else 0.0, "tolerance": tolerance,
            "certified": False,
            "note": "simulated along the given directions only"}


def _recovers(step, x_star, d, alpha, tolerance, t_end, err) -> bool:
    try:
        final = step(x_star + alpha * d, t_end)
    except Exception:
        return False
    final = np.asarray(final, dtype=float)
    if final.ndim > 1:
        final = final[-1]
    if not np.all(np.isfinite(final)):
        return False
    return bool(np.max(np.abs(np.asarray(err(final, x_star), dtype=float))) <= tolerance)


# ----------------------------------------------------------------------------- robustness

def robustness_sweep(trial: Callable[[dict], bool], perturbations: Sequence[dict],
                     confidence: float = 0.95) -> dict:
    """Run trial() over a list of perturbed conditions and report the success rate honestly.

    trial(perturbation) -> True on success. perturbations: the dicts handed to it, each
    describing one perturbed plant, noise seed or disturbance. Returns
    {'trials', 'successes', 'rate', 'interval', 'failures'} where interval is the Wilson
    score interval from stats_tools -- the point estimate alone is meaningless at the trial
    counts a simulation study can afford (10 successes out of 10 is consistent with a true
    rate of 0.72).

    'failures' lists the perturbations that failed, which is the useful output: the failure
    boundary, not the average.
    """
    sys.path.insert(0, ".claude/skills/conundrum/scripts")
    from stats_tools import wilson_interval

    successes, failures = 0, []
    for p in perturbations:
        ok = False
        try:
            ok = bool(trial(p))
        except Exception as exc:                     # a diverged sim is a failure, not a crash
            failures.append({"perturbation": p, "error": f"{type(exc).__name__}: {exc}"})
            continue
        if ok:
            successes += 1
        else:
            failures.append({"perturbation": p})
    n = len(perturbations)
    interval = wilson_interval(successes, n, confidence=confidence) if n else (0.0, 1.0)
    return {"trials": n, "successes": successes, "rate": (successes / n) if n else float("nan"),
            "interval": interval, "confidence": confidence, "failures": failures}


# ----------------------------------------------------------------------------- selftest

def selftest(verbose: bool = True) -> bool:
    """Check against independent references. Returns True when all pass."""
    ok = True

    def check(name, got, want, tol, note=""):
        nonlocal ok
        got_a = np.atleast_1d(np.asarray(got, dtype=float))
        want_a = np.atleast_1d(np.asarray(want, dtype=float))
        err = float(np.max(np.abs(got_a - want_a)))
        good = err <= tol
        ok = ok and good
        if verbose:
            print(f"  {'ok  ' if good else 'FAIL'} {name}: max err {err:.3e} (tol {tol:.1e})"
                  + (f"  [{note}]" if note else ""))
        return good

    def check_true(name, cond, note=""):
        nonlocal ok
        ok = ok and bool(cond)
        if verbose:
            print(f"  {'ok  ' if cond else 'FAIL'} {name}" + (f"  [{note}]" if note else ""))
        return bool(cond)

    if verbose:
        print("control_tools selftest")
    if not _HAVE_SCIPY:
        print("  FAIL scipy is missing; lqr, dlqr and lyapunov cannot run")
        return False

    # -- 1. the double integrator, published closed form --------------------------------
    # Reference: Russ Tedrake, Underactuated Robotics, ch. "Linear Quadratic Regulators",
    # https://underactuated.mit.edu/lqr.html (fetched 2026-10-15): for A = [[0,1],[0,0]],
    # B = [[0],[1]], Q = I, R = 1 the page gives K = [1, sqrt(3)] and S = [[sqrt3, 1],
    # [1, sqrt3]].  (Substituting those into 0 = SA + A^T S - SBB^T S + Q reproduces them:
    # s2^2 = 1, s1 = s2 s3, 2 s2 - s3^2 + 1 = 0.)
    A = np.array([[0.0, 1.0], [0.0, 0.0]])
    B = np.array([[0.0], [1.0]])
    out = lqr(A, B, np.eye(2), np.eye(1))
    check("double-integrator LQR K vs Underactuated", out["K"].ravel(),
          [1.0, math.sqrt(3.0)], 1e-9)
    check("double-integrator LQR S vs Underactuated", out["S"],
          [[math.sqrt(3.0), 1.0], [1.0, math.sqrt(3.0)]], 1e-9)
    check("double-integrator ARE residual", out["are_residual"], 0.0, 1e-9)
    check_true("double-integrator closed loop stable", out["stable"])

    # -- 2. the scalar ARE, closed form -------------------------------------------------
    # For xdot = a x + b u with cost q x^2 + r u^2, the Riccati equation 2 a s - s^2 b^2/r
    # + q = 0 is a quadratic in s whose positive root is
    #     s = r (a + sqrt(a^2 + q b^2 / r)) / b^2,   K = b s / r.
    # Algebra, independent of the scipy solver below.
    for a, b, q, r in [(1.0, 1.0, 1.0, 1.0), (-0.5, 2.0, 3.0, 0.25), (2.0, 0.5, 1.0, 4.0)]:
        s_ref = r * (a + math.sqrt(a * a + q * b * b / r)) / (b * b)
        got = lqr([[a]], [[b]], [[q]], [[r]])
        check(f"scalar ARE S, (a,b,q,r)=({a},{b},{q},{r})", got["S"], [[s_ref]], 1e-9)
        check(f"scalar ARE K, (a,b,q,r)=({a},{b},{q},{r})", got["K"], [[b * s_ref / r]], 1e-9)

    # -- 3. controllability and stabilisability -----------------------------------------
    check_true("double integrator is controllable", controllability(A, B)["controllable"])
    bad = controllability([[1.0, 0.0], [0.0, 1.0]], [[1.0], [0.0]])
    check_true("a decoupled unforced mode is uncontrollable", not bad["controllable"],
               f"rank {bad['rank']} of {bad['n']}")
    check_true("the uncontrollable mode is identified",
               any(abs(z - 1.0) < 1e-9 for z in bad["uncontrollable_modes"]))
    try:
        lqr([[1.0, 0.0], [0.0, 1.0]], [[1.0], [0.0]], np.eye(2), np.eye(1))
        check_true("lqr refuses a non-stabilisable pair", False)
    except ValueError:
        check_true("lqr refuses a non-stabilisable pair", True)
    check_true("observability is the dual of controllability",
               observability(A.T, B.T)["observable"])

    # -- 4. the Lyapunov equation, closed form ------------------------------------------
    # Scalar: a p + p a = -q gives p = -q / (2a), real and positive for a < 0.
    for a, q in [(-1.0, 1.0), (-0.25, 3.0)]:
        res = lyapunov([[a]], [[q]])
        check(f"scalar Lyapunov P, a={a}", res["P"], [[-q / (2 * a)]], 1e-12)
    res = lyapunov([[0.0, 1.0], [-1.0, -1.0]], np.eye(2))
    check("2x2 Lyapunov residual", res["residual"], 0.0, 1e-12)
    check_true("2x2 Lyapunov P is positive definite", res["positive_definite"])

    # -- 5. gain margin, analytic -------------------------------------------------------
    # L(s) = 1 / (s (s+1)^2): the phase is -90 - 2 arctan(w), which reaches -180 at w = 1,
    # where |L| = 1 / (1 * |1 + j|^2) = 1/2.  So the gain margin is exactly 2 (6.02 dB) at
    # w = 1 rad/s.  Standard textbook example; the arithmetic is in this comment.
    m = loop_margins(lambda s: 1.0 / (s * (s + 1.0) ** 2))
    check("gain margin of 1/(s(s+1)^2)", m["gain_margin"], 2.0, 1e-9)
    check("gain margin is an upward margin here", m["gain_margin_up"], 2.0, 1e-9)
    check("phase crossover of 1/(s(s+1)^2)", m["w_phase_crossover"], 1.0, 1e-9)

    # An open-loop-unstable plant's loop phase RISES through +180 degrees instead of falling
    # through -180. Both are the same point on the circle, and a detector built on the
    # unwrapped phase sees only the second, silently reporting "no gain margin" for exactly
    # the loops a balance controller produces. L(s) = k (s + 1) / ((s - a)(s - b)) has that
    # shape; here the -180 crossing is where Im L = 0 with Re L < 0.
    rising = loop_margins(lambda s: 20.0 * (s + 1.0) / ((s - 2.0) * (s - 6.0)),
                          w_min=1e-4, w_max=1e5, points=8001)
    check_true(f"a rising phase crossing of +180 deg is found "
               f"(down {rising['gain_margin_down']:.3f})",
               0.0 < rising["gain_margin_down"] < 1.0,
               "a detector built on the unwrapped phase reports 0 here")
    # verified independently: at the crossing, Im L = 0 and the gain factor is 1/|L|
    w_x = rising["w_phase_crossover"]
    Lx = 20.0 * (1j * w_x + 1.0) / ((1j * w_x - 2.0) * (1j * w_x - 6.0))
    check("the reported crossing really has Im L = 0", Lx.imag, 0.0, 1e-9)
    check_true(f"and Re L < 0 there ({Lx.real:.3f})", Lx.real < 0)
    check("the downward margin is 1/|L| at that crossing",
          rising["gain_margin_down"], 1.0 / abs(Lx), 1e-9)

    # -- 6. delay margin, analytic ------------------------------------------------------
    # L(s) = 1/s crosses unity gain at w = 1 rad/s with a phase of -90 deg, so the phase
    # margin is 90 deg and the delay margin is (pi/2) / 1 = 1.5708 s.
    m = loop_margins(lambda s: 1.0 / s)
    check("phase margin of 1/s", m["phase_margin_deg"], 90.0, 1e-9)
    check("delay margin of 1/s", m["delay_margin"], math.pi / 2, 1e-9)
    # k/s scales the crossover: delay margin halves when the gain doubles.
    m2 = loop_margins(lambda s: 2.0 / s)
    check("delay margin of 2/s", m2["delay_margin"], math.pi / 4, 1e-9)

    # -- 7. the LQR margin guarantee ----------------------------------------------------
    # Safonov and Athans, IEEE TAC 22 (1977) 173-179, doi:10.1109/tac.1977.1101470: LQR
    # state feedback at the plant input tolerates any gain increase (upward gain margin
    # infinite), a halving of the gain (downward margin <= 0.5) and at least 60 degrees of
    # phase lag.  Checked numerically on random single-input systems; the downward margin is
    # also what makes the single-number gain margin misleading here.
    rng = np.random.default_rng(3)
    worst_pm, worst_up, worst_down, tested = math.inf, math.inf, 0.0, 0
    for _ in range(12):
        n = int(rng.integers(2, 5))
        Ar = rng.normal(size=(n, n))
        Br = rng.normal(size=(n, 1))
        if not controllability(Ar, Br)["controllable"]:
            continue
        g = lqr(Ar, Br, np.eye(n), np.eye(1))
        mg = state_feedback_margins(Ar, Br, g["K"], w_min=1e-4, w_max=1e5, points=6001)
        worst_pm = min(worst_pm, mg["phase_margin_deg"])
        worst_up = min(worst_up, mg["gain_margin_up"])
        worst_down = max(worst_down, mg["gain_margin_down"])
        tested += 1
    check_true(f"LQR phase margin >= 60 deg over {tested} random systems "
               f"(worst {worst_pm:.1f} deg)", worst_pm >= 59.9, "Safonov & Athans 1977")
    check_true(f"LQR upward gain margin is infinite (worst {worst_up})",
               worst_up == math.inf, "no -180 deg crossing above unity gain")
    check_true(f"LQR downward gain margin <= 0.5 (worst {worst_down:.3f})",
               worst_down <= 0.5 + 1e-9, "the classic factor-of-two gain reduction")

    # -- 8. a region of attraction with an exact answer ---------------------------------
    # xdot = -x + x^3 has the exact region of attraction |x| < 1 (for |x| >= 1 the flow
    # diverges), and with V = x^2, Vdot = 2x(-x + x^3) = -2x^2(1 - x^2) < 0 exactly on
    # 0 < |x| < 1.  So the largest level set of V with Vdot < 0 is rho = 1.
    roa = roa_sample(lambda x, u: np.array([-x[0] + x[0] ** 3]), [0.0], [[1.0]],
                     rho_max=4.0, samples=40, levels=400)
    check("sampled ROA of xdot = -x + x^3", roa["rho"], 1.0, 0.05, "exact rho = 1")
    check_true("sampled ROA is labelled uncertified", roa["certified"] is False)

    # -- 9. discrete LQR against the continuous limit -----------------------------------
    # Zero-order-hold discretising the double integrator at a small dt and solving the
    # discrete ARE must approach the continuous gain [1, sqrt 3].
    Ad, Bd = zoh_discretize(A, B, 1e-4)
    d = dlqr(Ad, Bd, np.eye(2) * 1e-4, np.eye(1) * 1e-4, dt=1e-4)
    check("dlqr -> continuous LQR as dt -> 0", d["K"].ravel(), [1.0, math.sqrt(3.0)], 2e-3)
    check("discrete ARE residual", d["are_residual"], 0.0, 1e-10)
    check_true("discrete closed loop inside the unit circle", d["stable"])

    # -- 10. linearisation against an analytic Jacobian ---------------------------------
    # The pendulum xdot = [v, -(g/l) sin(x) - c v] has A = [[0,1],[-(g/l) cos x, -c]].
    g_, l_, c_ = 9.81, 0.7, 0.3

    def f_pend(x, u):
        return np.array([x[1], -(g_ / l_) * math.sin(x[0]) - c_ * x[1] + u[0]])
    for x0 in ([0.0, 0.0], [math.pi, 0.0], [0.4, -1.0]):
        Aa, Bb, info = linearize(f_pend, x0, [0.0])
        check(f"linearize at x={x0}", Aa,
              [[0.0, 1.0], [-(g_ / l_) * math.cos(x0[0]), -c_]], 1e-6)
        check(f"linearize B at x={x0}", Bb, [[0.0], [1.0]], 1e-9)
    _, _, info = linearize(f_pend, [0.4, -1.0], [0.0])
    check_true("linearize flags a non-equilibrium point",
               info["residual"] > 1e-6, f"residual {info['residual']:.3f}")
    _, _, info_up = linearize(f_pend, [math.pi, 0.0], [0.0])
    check_true("linearize finds the upright mode unstable",
               info_up["unstable_modes"] == 1)

    # -- 11. the delay margin on an open-loop-unstable plant ----------------------------
    # The inverted pendulum linearised at the top: A = [[0,1],[g/l,0]], B = [[0],[1/(m l^2)]],
    # open-loop poles at +-sqrt(g/l).  Classical "180 + unwrapped phase" bookkeeping fails
    # here, so the delay margin is checked against its definition by a second, independent
    # route: at the critical delay tau the delayed closed loop
    #     det(jw I - A + B K e^{-jw tau}) = 0
    # must have a root on the imaginary axis, and at 0.9 tau it must not.
    g_p, l_p, m_p = 9.81, 0.5, 0.2
    Ap = np.array([[0.0, 1.0], [g_p / l_p, 0.0]])
    Bp = np.array([[0.0], [1.0 / (m_p * l_p ** 2)]])
    gp = lqr(Ap, Bp, np.diag([10.0, 1.0]), np.eye(1))
    mp_ = state_feedback_margins(Ap, Bp, gp["K"], w_min=1e-3, w_max=1e5, points=6001)
    tau = mp_["delay_margin"]
    check_true(f"inverted-pendulum LQR is open-loop unstable but closed-loop stable",
               np.any(np.real(np.linalg.eigvals(Ap)) > 0) and gp["stable"])

    def sv_ratio(tau_, wi):
        """smallest / largest singular value of the delayed characteristic matrix at jw."""
        mat = 1j * wi * np.eye(2) - Ap + Bp @ gp["K"] * np.exp(-1j * wi * tau_)
        sv = np.linalg.svd(mat, compute_uv=False)
        return float(sv[-1] / sv[0])
    w_star = mp_["w_gain_crossover"]
    check_true(f"delay margin {tau * 1e3:.2f} ms makes the delayed characteristic matrix "
               "singular at the crossover", sv_ratio(tau, w_star) < 1e-12,
               f"sigma_min/sigma_max {sv_ratio(tau, w_star):.2e}")
    grid = np.linspace(0.2 * w_star, 5 * w_star, 4001)
    check_true("at 0.9 of the delay margin nothing comes near the axis",
               min(sv_ratio(0.9 * tau, float(wi)) for wi in grid) > 1e-4,
               f"best sigma_min/sigma_max {min(sv_ratio(0.9 * tau, float(wi)) for wi in grid):.2e}")
    check_true(f"phase margin of the inverted-pendulum LQR is >= 60 deg "
               f"({mp_['phase_margin_deg']:.1f})", mp_["phase_margin_deg"] >= 59.9)

    # -- 12. robustness_sweep arithmetic ------------------------------------------------
    sweep = robustness_sweep(lambda p: p["x"] < 0.8, [{"x": i / 10.0} for i in range(10)])
    check("robustness_sweep success count", sweep["successes"], 8, 0)
    check_true("robustness_sweep interval brackets the rate",
               sweep["interval"][0] < 0.8 < sweep["interval"][1],
               f"{sweep['interval'][0]:.3f}..{sweep['interval'][1]:.3f}")
    check("robustness_sweep lists the failures", len(sweep["failures"]), 2, 0)
    crashy = robustness_sweep(lambda p: 1 / 0, [{"x": 1}])
    check_true("a crashing trial counts as a failure", crashy["successes"] == 0
               and "error" in crashy["failures"][0])

    if verbose:
        print("PASS" if ok else "FAIL")
    return ok


# ----------------------------------------------------------------------------- CLI

def _acrobot_lqr_demo() -> int:
    sys.path.insert(0, ".claude/skills/conundrum/scripts")
    from rigid_body import acrobot
    ch = acrobot()
    f = ch.state_dynamics()
    x_up = np.array([math.pi, 0.0, 0.0, 0.0])
    A, B, info = linearize(f, x_up, np.zeros(1))
    print(f"linearised at upright: residual {info['residual']:.2e}, "
          f"step sensitivity {info['step_sensitivity']:.2e}")
    print(f"open-loop eigenvalues: {np.round(info['eigenvalues'], 4)}")
    c = controllability(A, B)
    print(f"controllable: {c['controllable']} (rank {c['rank']}/{c['n']}, "
          f"sigma_min {c['min_singular_value']:.3e}, condition {c['condition']:.1f})")
    out = lqr(A, B, np.diag([10.0, 10.0, 1.0, 1.0]), np.eye(1))
    print(f"K = {np.round(out['K'], 4)}")
    print(f"closed-loop poles: {np.round(out['closed_loop_poles'], 4)}")
    m = state_feedback_margins(A, B, out["K"])
    print(f"gain margin {m['gain_margin']:.3g}, phase margin {m['phase_margin_deg']:.1f} deg, "
          f"delay margin {m['delay_margin'] * 1e3:.2f} ms")
    return 0


def _main(argv) -> int:
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[1] == "selftest":
        return 0 if selftest() else 1
    if argv[1] == "acrobot-lqr":
        return _acrobot_lqr_demo()
    print(f"unknown command: {argv[1]}\n{__doc__}")
    return 2


if __name__ == "__main__":
    sys.exit(_main(sys.argv))
