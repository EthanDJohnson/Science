#!/usr/bin/env python3
"""General-relativity toolkit for /conundrum agents.

Computes curvature, the stress-energy a metric requires (Einstein's equations), what
observers measure, energy conditions (NEC/WEC/SEC/DEC with Hawking-Ellis type),
quantum-inequality bounds, horizons, and slice integrals, so claims like "this metric
needs negative energy" get computed rather than argued.

Conventions: signature (-,+,+,+), geometric units G = c = 1 with lengths in metres,
Gamma^a_bc = 1/2 g^ad (d_b g_dc + d_c g_db - d_d g_bc),
R^a_bcd = d_c Gamma^a_db - d_d Gamma^a_cb + Gamma^a_ce Gamma^e_db - Gamma^a_de Gamma^e_cb,
R_bd = R^a_bad, G_ab = R_ab - 1/2 g_ab R = 8 pi T_ab. Coordinate 0 is time.

Quick start (run from the project root):

    import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
    from gr_tensors import Spacetime, metrics, qi, horizons_1p1, to_si

    st, s = metrics.alcubierre()        # built with from_adm, so the fast paths apply
    rho = st.energy_density()           # Eulerian rho via the Hamiltonian constraint
    top = metrics.alcubierre_top_hat(s)
    params = {s["v"]: 1.0, s["R"]: 1.0, s["sigma"]: 8.0}
    parts = st.integrate_parts(rho, t=0.0, bounds=[(-1.8, 1.8)] * 3, n=96,
                               params=params, functions={s["f"]: top})
    print(parts["total"], "m ->", to_si.mass_kg(parts["total"]), "kg")   # -0.2233 m
    ec = st.energy_conditions((0.0, 1.0, 0.3, 0.0), params, {s["f"]: top})
    print(ec["type"], ec["nec"], ec["wec"], ec["sec"], ec["dec"])
    scan = st.scan_energy_conditions(points, params, {s["f"]: top})      # many points

For a spherically symmetric Alcubierre bubble the total energy also follows from the 1D
integral E = -(v^2/12) * int_0^inf f'(r)^2 r^2 dr, a useful cross-check.

Practical rules
- Speed: build 3+1 metrics with Spacetime.from_adm. It supplies the inverse metric in
  closed form, and energy_density() then uses the Hamiltonian constraint instead of the
  4D Einstein tensor. einstein() and riemann() are exact but can be slow for
  complicated shifts.
- Sweeps: compile(expr, params, functions, free=[v]) returns f(t, x, y, z, v). Compiled
  functions are cached, so repeated calls are cheap.
- Precision: float64 can lose everything to cancellation at large dynamic range (e.g.
  Van Den Broeck with B ~ 1e6). Run precision_check(...) on surprising values; it
  compares float64 with 50-digit mpmath.
- Grids: keep grid points off coordinate singularities such as r_s = 0. Integrals drop
  NaN points, count them and warn.
- Convergence: compare n with about 1.5 n for every integral, and resolve thin walls
  (grid spacing at most about 1/(4 sigma)).
- Scans: one point can mislead; use scan_energy_conditions over the whole region.
- Long runs: Bash calls stop after 10 minutes. Test on a coarse grid first; run longer
  scripts in the background, have them write a marker file when done, and stop
  processes by PID (never pkill -f / pgrep -f, which match your own shell).

CLI:  python3 gr_tensors.py selftest   # verify the toolkit against known results
      python3 gr_tensors.py help       # print this text
"""
from __future__ import annotations

import math
import sys
import warnings

try:
    import sympy as sp
except ImportError:  # pragma: no cover - exercised only without sympy
    sys.exit("gr_tensors.py needs sympy: pip install sympy numpy")

try:
    import numpy as np
except ImportError:  # pragma: no cover
    np = None

# CODATA 2018 (exact SI values where defined); M_SUN from the IAU 2015 nominal GM_sun.
C = 299_792_458.0
G_NEWTON = 6.67430e-11
HBAR = 1.054571817e-34
K_B = 1.380649e-23
PLANCK_LENGTH = math.sqrt(HBAR * G_NEWTON / C**3)
PLANCK_TIME = PLANCK_LENGTH / C
PLANCK_MASS = math.sqrt(HBAR * C / G_NEWTON)
M_SUN = 1.3271244e20 / G_NEWTON


class to_si:
    """Convert geometric-unit results (lengths in metres) to SI."""

    @staticmethod
    def energy_density_j_per_m3(rho_geometric: float) -> float:
        """rho [1/m^2] -> J/m^3 (multiply by c^4/G)."""
        return rho_geometric * C**4 / G_NEWTON

    @staticmethod
    def energy_joules(e_geometric: float) -> float:
        """E [m] -> J (multiply by c^4/G)."""
        return e_geometric * C**4 / G_NEWTON

    @staticmethod
    def mass_kg(e_geometric: float) -> float:
        """E [m] -> kg (multiply by c^2/G)."""
        return e_geometric * C**2 / G_NEWTON

    @staticmethod
    def hawking_temperature_k(kappa_per_m: float) -> float:
        """Surface gravity kappa [1/m] -> temperature T = hbar c kappa / (2 pi k_B) [K]."""
        return HBAR * C * kappa_per_m / (2 * math.pi * K_B)


class qi:
    """Ford-Roman quantum inequality for a free massless scalar in 4D Minkowski space,
    Lorentzian sampling of width tau0 (Ford & Roman 1997): <rho> >= -3/(32 pi^2 tau0^4)
    with hbar = c = 1. It applies in curved spacetime only when tau0 is small compared
    with the local curvature radius (see Spacetime.curvature_at)."""

    @staticmethod
    def ford_roman_si(tau0_s: float) -> float:
        """Lower bound on the Lorentzian-averaged energy density, J/m^3, for tau0 in seconds."""
        return -3 * HBAR / (32 * math.pi**2 * C**3 * tau0_s**4)

    @staticmethod
    def ford_roman_geometric(tau0_m: float) -> float:
        """The same bound in geometric units (1/m^2) for a sampling length tau0 = c*tau0 in metres."""
        return -3 * PLANCK_LENGTH**2 / (32 * math.pi**2 * tau0_m**4)

    @staticmethod
    def lorentzian_average(rho_of_tau, tau0: float, n: int = 20001) -> float:
        """<rho> = int rho(tau) (tau0/pi)/(tau^2 + tau0^2) dtau, computed exactly over the whole
        line with tau = tau0 tan(theta) (the weight becomes d theta / pi). rho_of_tau must
        accept numpy arrays."""
        if np is None:
            raise RuntimeError("numpy is required: pip install numpy")
        theta = -math.pi / 2 + math.pi * (np.arange(n) + 0.5) / n
        return float(np.mean(rho_of_tau(tau0 * np.tan(theta))))


def horizons_1p1(u, xs):
    """Horizons of a 1+1 'river' metric ds^2 = -dt^2 + (dx - u(x) dt)^2: where u(x)^2 = 1.

    u: callable on numpy arrays (flow velocity, c = 1). xs: increasing grid that brackets
    the horizons. Returns [{"x": x_h, "kappa": |du/dx| at x_h}] with kappa in 1/length.
    Example: an Alcubierre bubble along its axis, in the comoving coordinate xi = x - v t,
    has u(xi) = -v (1 - f(|xi|)).
    """
    if np is None:
        raise RuntimeError("numpy is required: pip install numpy")
    xs = np.asarray(xs, dtype=float)
    h = np.asarray(u(xs), dtype=float) ** 2 - 1.0
    found = []
    for i in np.nonzero(np.sign(h[:-1]) * np.sign(h[1:]) < 0)[0]:
        lo, hi = xs[i], xs[i + 1]
        flo = float(u(np.array([lo]))[0] ** 2 - 1.0)
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            fmid = float(u(np.array([mid]))[0] ** 2 - 1.0)
            if (fmid < 0) == (flo < 0):
                lo, flo = mid, fmid
            else:
                hi = mid
        x_h = 0.5 * (lo + hi)
        step = max(abs(x_h), 1.0) * 1e-7
        du = (float(u(np.array([x_h + step]))[0]) - float(u(np.array([x_h - step]))[0])) / (2 * step)
        found.append({"x": x_h, "kappa": abs(du)})
    return found


def _fibonacci_directions(n: int):
    golden = math.pi * (3 - math.sqrt(5))
    out = []
    for i in range(n):
        z = 1 - 2 * (i + 0.5) / n
        r = math.sqrt(max(0.0, 1 - z * z))
        out.append((r * math.cos(golden * i), r * math.sin(golden * i), z))
    return out


def _orthonormal_frame(g, u):
    """Rows e_(A)^mu of an orthonormal frame with e_(0) along the timelike vector u."""
    n = g.shape[0]
    u = u / math.sqrt(-(u @ g @ u))
    frame = [u]
    for i in range(n):
        e = np.zeros(n)
        e[i] = 1.0
        for f in frame:
            e = e - (e @ g @ f) * (f @ g @ f) * f  # f.f = -1 for u, +1 for spatial vectors
        norm = e @ g @ e
        if norm > 1e-12 * max(1.0, float(np.max(np.abs(g)))) and len(frame) < n:
            frame.append(e / math.sqrt(norm))
    if len(frame) != n:
        raise ValueError("could not build an orthonormal frame at this point")
    return np.array(frame)


def classify_stress_energy(t_frame):
    """Energy conditions from orthonormal-frame components T_AB (eta = diag(-1,1,1,1)).

    Type I (one timelike eigenvector of T^A_B, the usual case) is decided exactly from the
    rest-frame density and principal pressures: NEC rho+p_i >= 0; WEC NEC and rho >= 0;
    SEC NEC and rho + sum p_i >= 0; DEC rho >= |p_i|. Other Hawking-Ellis types fall back to
    sampling boosted observers and null directions. Sampled minima are always reported.
    """
    eta = np.diag([-1.0, 1.0, 1.0, 1.0])
    scale = max(1.0, float(np.max(np.abs(t_frame))))
    tol = 1e-10 * scale
    trace = float(np.trace(eta @ t_frame))
    dirs = _fibonacci_directions(64)
    nec_min, wec_min, sec_min, dec_ok_sampled = math.inf, math.inf, math.inf, True
    for beta in (0.0, 0.3, 0.6, 0.9, 0.99):
        gamma = 1 / math.sqrt(1 - beta * beta)
        for d in (dirs if beta else dirs[:1]):
            w = gamma * np.array([1.0, beta * d[0], beta * d[1], beta * d[2]])
            wec_min = min(wec_min, float(w @ t_frame @ w))
            sec_min = min(sec_min, float(w @ t_frame @ w) + 0.5 * trace)
            flux = -(eta @ t_frame @ w)  # -T^A_B w^B
            if not (flux @ eta @ flux <= tol * scale and flux[0] >= -tol):
                dec_ok_sampled = False
    for d in dirs:
        k = np.array([1.0, *d])
        nec_min = min(nec_min, float(k @ t_frame @ k))
    result = {"nec_min": nec_min, "wec_min": wec_min, "sec_min": sec_min}

    vals, vecs = np.linalg.eig(eta @ t_frame)
    timelike = [i for i in range(4)
                if abs(vals[i].imag) < tol and float(np.real(vecs[:, i]) @ eta @ np.real(vecs[:, i])) < -1e-9]
    if len(timelike) == 1 and np.all(np.abs(vals.imag) < tol):
        i0 = timelike[0]
        rho = -float(vals[i0].real)
        ps = [float(vals[i].real) for i in range(4) if i != i0]
        nec = all(rho + p >= -tol for p in ps)
        result.update({
            "type": "I", "rho_rest": rho, "pressures": ps,
            "nec": nec, "wec": nec and rho >= -tol, "sec": nec and rho + sum(ps) >= -tol,
            "dec": rho >= -tol and all(abs(p) <= rho + tol for p in ps),
        })
    else:
        # Complex eigenvalues mean type IV (which always violates the NEC); real eigenvalues
        # without a single timelike eigenvector mean type II or III.
        kind = "IV" if np.any(np.abs(vals.imag) >= tol) else "II/III"
        result.update({
            "type": f"{kind} (sampled)", "rho_rest": None, "pressures": None,
            "nec": nec_min >= -tol, "wec": wec_min >= -tol and nec_min >= -tol,
            "sec": sec_min >= -tol and nec_min >= -tol, "dec": dec_ok_sampled and wec_min >= -tol,
        })
    return result


class Spacetime:
    """A metric g_ab over coordinates x^a, with lazily computed curvature."""

    def __init__(self, metric, coords, simplify: bool = False):
        self.g = sp.Matrix(metric)
        self.coords = list(coords)
        self.dim = len(self.coords)
        if self.g.shape != (self.dim, self.dim):
            raise ValueError(f"metric is {self.g.shape}, expected {self.dim}x{self.dim}")
        if self.g != self.g.T:
            raise ValueError("metric must be symmetric")
        self.simplify = simplify
        self.adm = None
        self._cache = {}
        self._compiled = {}

    # ----- construction ------------------------------------------------------------
    @classmethod
    def from_adm(cls, lapse, shift_up, spatial_metric, coords, simplify=False):
        """ds^2 = -N^2 dt^2 + h_ij (dx^i + b^i dt)(dx^j + b^j dt), with the inverse metric in
        closed form: g^00 = -1/N^2, g^0i = b^i/N^2, g^ij = h^ij - b^i b^j / N^2."""
        h = sp.Matrix(spatial_metric)
        b_up = sp.Matrix(shift_up)
        b_low = h * b_up
        lapse = sp.sympify(lapse)
        n = len(coords)
        g = sp.zeros(n, n)
        g[0, 0] = -lapse**2 + (b_up.T * b_low)[0, 0]
        for i in range(1, n):
            g[0, i] = g[i, 0] = b_low[i - 1]
            for j in range(1, n):
                g[i, j] = h[i - 1, j - 1]
        st = cls(g, coords, simplify=simplify)
        h_inv = sp.diag(*[1 / h[i, i] for i in range(n - 1)]) if h.is_diagonal() else h.inv()
        gi = sp.zeros(n, n)
        gi[0, 0] = -1 / lapse**2
        for i in range(1, n):
            gi[0, i] = gi[i, 0] = b_up[i - 1] / lapse**2
            for j in range(1, n):
                gi[i, j] = h_inv[i - 1, j - 1] - b_up[i - 1] * b_up[j - 1] / lapse**2
        st._cache["ginv"] = gi
        st.adm = {"lapse": lapse, "shift_up": b_up, "shift_low": b_low, "h": h, "h_inv": h_inv}
        return st

    def _s(self, expr):
        return sp.simplify(expr) if self.simplify else expr

    # ----- curvature ----------------------------------------------------------------
    @property
    def ginv(self):
        if "ginv" not in self._cache:
            gi = self.g.inv()
            self._cache["ginv"] = gi.applyfunc(sp.simplify) if self.simplify else gi
        return self._cache["ginv"]

    def christoffel(self):
        """Gamma[a][b][c] = Gamma^a_bc."""
        if "gamma" in self._cache:
            return self._cache["gamma"]
        n, g, gi, x = self.dim, self.g, self.ginv, self.coords
        dg = [[[sp.diff(g[i, j], x[k]) for k in range(n)] for j in range(n)] for i in range(n)]
        gam = [[[sp.Integer(0)] * n for _ in range(n)] for _ in range(n)]
        for a in range(n):
            for b in range(n):
                for c in range(b, n):
                    total = sp.Integer(0)
                    for d in range(n):
                        if gi[a, d] != 0:
                            total += gi[a, d] * (dg[d][c][b] + dg[d][b][c] - dg[b][c][d])
                    gam[a][b][c] = gam[a][c][b] = self._s(total / 2)
        self._cache["gamma"] = gam
        return gam

    def riemann(self):
        """Rm[a][b][c][d] = R^a_bcd."""
        if "riemann" in self._cache:
            return self._cache["riemann"]
        n, x, gam = self.dim, self.coords, self.christoffel()
        zero = sp.Integer(0)
        rm = [[[[zero] * n for _ in range(n)] for _ in range(n)] for _ in range(n)]
        for a in range(n):
            for b in range(n):
                for c in range(n):
                    for d in range(c + 1, n):
                        val = sp.diff(gam[a][d][b], x[c]) - sp.diff(gam[a][c][b], x[d])
                        for e in range(n):
                            val += gam[a][c][e] * gam[e][d][b] - gam[a][d][e] * gam[e][c][b]
                        val = self._s(val)
                        rm[a][b][c][d], rm[a][b][d][c] = val, -val
        self._cache["riemann"] = rm
        return rm

    def ricci(self):
        """R_bd (lower indices)."""
        if "ricci" in self._cache:
            return self._cache["ricci"]
        n, x, gam = self.dim, self.coords, self.christoffel()
        ric = sp.zeros(n, n)
        for b in range(n):
            for d in range(b, n):
                total = sp.Integer(0)
                for a in range(n):
                    total += sp.diff(gam[a][b][d], x[a]) - sp.diff(gam[a][b][a], x[d])
                    for e in range(n):
                        total += gam[a][a][e] * gam[e][b][d] - gam[a][d][e] * gam[e][b][a]
                ric[b, d] = ric[d, b] = self._s(total)
        self._cache["ricci"] = ric
        return ric

    def ricci_scalar(self):
        if "R" not in self._cache:
            gi, ric, n = self.ginv, self.ricci(), self.dim
            self._cache["R"] = self._s(sum(gi[a, b] * ric[a, b] for a in range(n) for b in range(n)))
        return self._cache["R"]

    def einstein(self):
        """G_ab (lower indices)."""
        if "einstein" not in self._cache:
            self._cache["einstein"] = (self.ricci() - self.g * self.ricci_scalar() / 2).applyfunc(self._s)
        return self._cache["einstein"]

    def stress_energy(self):
        """T_ab = G_ab / (8 pi): the matter a metric requires (lower indices)."""
        if "T" not in self._cache:
            self._cache["T"] = (self.einstein() / (8 * sp.pi)).applyfunc(self._s)
        return self._cache["T"]

    # ----- observers ------------------------------------------------------------------
    def eulerian_observer(self):
        """n^a for observers normal to t = const slices: n^a = -N g^{a0}, N = 1/sqrt(-g^{00})."""
        gi = self.ginv
        lapse = 1 / sp.sqrt(-gi[0, 0])
        return sp.Matrix([self._s(-lapse * gi[a, 0]) for a in range(self.dim)])

    def contract(self, tensor_low, u, v=None):
        """T_ab u^a v^b (v defaults to u)."""
        v = u if v is None else v
        n = self.dim
        return sum(tensor_low[a, b] * u[a] * v[b] for a in range(n) for b in range(n))

    def adm_energy_density(self):
        """Eulerian energy density from the Hamiltonian constraint:
        rho = (3R + K^2 - K_ij K^ij) / (16 pi), K_ij = (D_i b_j + D_j b_i - d_t h_ij) / (2N).
        Exact, and far cheaper than the 4D Einstein tensor. Needs from_adm."""
        if self.adm is None:
            raise ValueError("adm_energy_density needs a spacetime built with Spacetime.from_adm")
        if "rho_adm" in self._cache:
            return self._cache["rho_adm"]
        lapse, b_low, h, h_inv = (self.adm[k] for k in ("lapse", "shift_low", "h", "h_inv"))
        t, xs = self.coords[0], self.coords[1:]
        m = len(xs)
        spatial = Spacetime(h, xs)
        spatial._cache["ginv"] = h_inv
        gam3 = spatial.christoffel()
        k = sp.zeros(m, m)
        for i in range(m):
            for j in range(i, m):
                di_bj = sp.diff(b_low[j], xs[i]) - sum(gam3[q][i][j] * b_low[q] for q in range(m))
                dj_bi = sp.diff(b_low[i], xs[j]) - sum(gam3[q][j][i] * b_low[q] for q in range(m))
                k[i, j] = k[j, i] = (di_bj + dj_bi - sp.diff(h[i, j], t)) / (2 * lapse)
        tr_k = sum(h_inv[i, j] * k[i, j] for i in range(m) for j in range(m))
        kk = sum(h_inv[i, p] * h_inv[j, q] * k[i, j] * k[p, q]
                 for i in range(m) for j in range(m) for p in range(m) for q in range(m))
        rho = (spatial.ricci_scalar() + tr_k**2 - kk) / (16 * sp.pi)
        self._cache["rho_adm"] = self._s(rho)
        return self._cache["rho_adm"]

    def energy_density(self, u=None, method: str = "auto"):
        """rho = T_ab u^a u^b for a unit timelike u (default: Eulerian observers).
        method "auto" uses the Hamiltonian constraint when the metric came from from_adm and
        u is Eulerian; "einstein" forces the 4D route (useful as a cross-check)."""
        if u is None and method in ("auto", "adm") and self.adm is not None:
            return self.adm_energy_density()
        if method == "adm":
            raise ValueError("method='adm' needs from_adm and the default (Eulerian) observer")
        u = self.eulerian_observer() if u is None else sp.Matrix(u)
        return self._s(self.contract(self.stress_energy(), u))

    def spatial_volume_element(self):
        """sqrt(det h_ij) of the t = const slice."""
        h = self.adm["h"] if self.adm is not None else self.g[1:, 1:]
        return self._s(sp.sqrt(h.det()))

    # ----- numerics ---------------------------------------------------------------------
    @staticmethod
    def _prepare(expr, params=None, functions=None):
        expr = sp.sympify(expr)
        # Functions first: a concrete profile may itself contain parameters (R, sigma).
        if functions:
            for fn, lam in functions.items():
                expr = expr.subs(fn, lam)
            expr = expr.doit()
        if params:
            expr = expr.subs(params)
        return expr

    def compile(self, expr, params=None, functions=None, free=(), modules="numpy"):
        """Callable f(*coords, *free) after substituting params and concrete functions.
        Results are cached, so re-compiling the same expression is free."""
        if modules == "numpy" and np is None:
            raise RuntimeError("numpy is required for numeric evaluation: pip install numpy")
        if isinstance(expr, sp.MatrixBase):
            expr = sp.ImmutableMatrix(expr)
        key = (expr, tuple(sorted((params or {}).items(), key=lambda kv: str(kv[0]))),
               tuple(sorted((functions or {}).items(), key=lambda kv: str(kv[0]))), tuple(free), modules)
        if key in self._compiled:
            return self._compiled[key]
        prepared = self._prepare(expr, params, functions)
        leftover = prepared.free_symbols - set(self.coords) - set(free)
        if leftover:
            raise ValueError(f"unassigned symbols: {sorted(map(str, leftover))}; pass them in params or free")
        # cse: curvature expressions repeat the same subterms many times.
        fn = sp.lambdify(list(self.coords) + list(free), prepared, modules, cse=True)
        self._compiled[key] = fn
        return fn

    def evaluate(self, expr, point, params=None, functions=None, precision=None) -> float:
        """Evaluate a scalar at a coordinate point. precision=N uses N-digit mpmath arithmetic."""
        if precision is None:
            return float(self.compile(expr, params, functions)(*point))
        import mpmath
        with mpmath.workdps(precision):
            fn = self.compile(expr, params, functions, modules="mpmath")
            return float(fn(*[mpmath.mpf(repr(float(p))) for p in point]))

    def precision_check(self, expr, points, params=None, functions=None, digits=50):
        """Compare float64 with high-precision evaluation at each point. A large relative error
        or a sign flip means float64 cancellation: trust the mpmath value (or simplify)."""
        worst, worst_point, sign_flips, rows = 0.0, None, 0, []
        for p in points:
            f64 = self.evaluate(expr, p, params, functions)
            hp = self.evaluate(expr, p, params, functions, precision=digits)
            rel = abs(f64 - hp) / max(abs(hp), 1e-300)
            if (f64 > 0) != (hp > 0) and hp != 0:
                sign_flips += 1
            if rel > worst:
                worst, worst_point = rel, p
            rows.append((p, f64, hp))
        return {"max_rel_error": worst, "worst_point": worst_point, "sign_flips": sign_flips, "values": rows}

    def integrate_parts(self, density, t, bounds, n=64, params=None, functions=None):
        """Midpoint-rule integral of density * sqrt(h) d^3x on the slice x^0 = t over a box.

        Returns {"total", "negative", "positive", "nan_points", "n"}: the negative and
        positive parts matter for "how much exotic matter". Evaluated in x-slabs to bound
        memory. NaN/inf points (e.g. a grid point on r_s = 0) are dropped, counted, and warned.
        """
        if np is None:
            raise RuntimeError("numpy is required: pip install numpy")
        if self.dim != 4 or len(bounds) != 3:
            raise ValueError("integrate_parts expects 4 coordinates and 3 spatial bounds")
        integrand = self.compile(density * self.spatial_volume_element(), params, functions)
        axes, widths = [], []
        for lo, hi in bounds:
            step = (hi - lo) / n
            axes.append(lo + step * (np.arange(n) + 0.5))
            widths.append(step)
        yy, zz = np.meshgrid(axes[1], axes[2], indexing="ij")
        neg = pos = 0.0
        bad = 0
        for xv in axes[0]:
            vals = np.array(np.broadcast_to(integrand(t, np.full_like(yy, xv), yy, zz), yy.shape), dtype=float)
            finite = np.isfinite(vals)
            bad += int(vals.size - finite.sum())
            vals = np.where(finite, vals, 0.0)
            neg += float(vals[vals < 0].sum())
            pos += float(vals[vals > 0].sum())
        if bad:
            warnings.warn(f"{bad} grid point(s) gave NaN/inf and were dropped; move the grid off "
                          "coordinate singularities (e.g. use an even n on a symmetric box)")
        dv = widths[0] * widths[1] * widths[2]
        return {"total": (neg + pos) * dv, "negative": neg * dv, "positive": pos * dv,
                "nan_points": bad, "n": n}

    def integrate_on_slice(self, density, t, bounds, n=64, params=None, functions=None) -> float:
        """Net integral of density * sqrt(h) d^3x; see integrate_parts for the split and caveats."""
        return self.integrate_parts(density, t, bounds, n, params, functions)["total"]

    def _numeric_fields(self, params, functions, observer):
        u_sym = self.eulerian_observer() if observer is None else sp.Matrix(observer)
        return (self.compile(self.g, params, functions),
                self.compile(self.stress_energy(), params, functions),
                self.compile(u_sym, params, functions))

    def _conditions_at(self, fields, point):
        g_fn, t_fn, u_fn = fields
        n = self.dim
        g = np.array(g_fn(*point), dtype=float).reshape(n, n)
        t = np.array(t_fn(*point), dtype=float).reshape(n, n)
        u = np.array(u_fn(*point), dtype=float).reshape(n)
        e = _orthonormal_frame(g, u)
        result = classify_stress_energy(e @ t @ e.T)
        result["rho_observer"] = float(e[0] @ t @ e[0])
        return result

    def energy_conditions(self, point, params=None, functions=None, observer=None):
        """NEC/WEC/SEC/DEC at one point, from the full stress-energy (see classify_stress_energy).
        rho_observer is what the given (default Eulerian) observer measures; rho_rest is the
        matter's own rest-frame density. One point can mislead: prefer scan_energy_conditions."""
        if np is None:
            raise RuntimeError("numpy is required: pip install numpy")
        return self._conditions_at(self._numeric_fields(params, functions, observer), point)

    def scan_energy_conditions(self, points, params=None, functions=None, observer=None):
        """Energy conditions over many points, compiling once. Returns violation counts, the
        worst value of each condition's sampled minimum, and where it occurred."""
        if np is None:
            raise RuntimeError("numpy is required: pip install numpy")
        fields = self._numeric_fields(params, functions, observer)
        counts = {"nec": 0, "wec": 0, "sec": 0, "dec": 0}
        worst = {"nec_min": (math.inf, None), "wec_min": (math.inf, None), "sec_min": (math.inf, None)}
        evaluated = skipped = 0
        for p in points:
            try:
                r = self._conditions_at(fields, p)
            except (ValueError, FloatingPointError, np.linalg.LinAlgError):
                skipped += 1
                continue
            if not all(math.isfinite(r[k]) for k in worst):
                skipped += 1
                continue
            evaluated += 1
            for c in counts:
                counts[c] += 0 if r[c] else 1
            for k in worst:
                if r[k] < worst[k][0]:
                    worst[k] = (r[k], tuple(p))
        return {"points": evaluated, "skipped": skipped, "violations": counts, "worst": worst}

    def energy_condition_scan(self, point, params=None, functions=None, observer=None, n_dirs=64):
        """Backward-compatible alias of energy_conditions (adds rho, wec_ok and nec_ok keys)."""
        r = self.energy_conditions(point, params, functions, observer)
        r.update({"rho": r["rho_observer"], "wec_ok": r["wec"], "nec_ok": r["nec"]})
        return r

    def curvature_at(self, point, params=None, functions=None, observer=None):
        """Kretschmann scalar and the curvature radius r_c = 1/sqrt(max |R_ABCD|) in an
        orthonormal frame (default Eulerian) at one point, in geometric units (1/m^4 and m)."""
        if np is None:
            raise RuntimeError("numpy is required: pip install numpy")
        n = self.dim
        rm = self.riemann()
        flat = [rm[a][b][c][d] for a in range(n) for b in range(n) for c in range(n) for d in range(n)]
        rm_fn = self.compile(sp.Matrix(flat), params, functions)
        g_fn, _, u_fn = (self.compile(self.g, params, functions), None,
                         self.compile(self.eulerian_observer() if observer is None else sp.Matrix(observer),
                                      params, functions))
        g = np.array(g_fn(*point), dtype=float).reshape(n, n)
        r_up = np.array(rm_fn(*point), dtype=float).reshape(n, n, n, n)
        gi = np.linalg.inv(g)
        r_low = np.einsum("ae,ebcd->abcd", g, r_up)
        r_all_up = np.einsum("bf,cg,dh,afgh->abcd", gi, gi, gi, r_up)
        kretschmann = float(np.einsum("abcd,abcd->", r_low, r_all_up))
        e = _orthonormal_frame(g, np.array(u_fn(*point), dtype=float).reshape(n))
        frame = np.einsum("Aa,Bb,Cc,Dd,abcd->ABCD", e, e, e, e, r_low)
        peak = float(np.max(np.abs(frame)))
        return {"kretschmann": kretschmann, "max_frame_component": peak,
                "curvature_radius": (1 / math.sqrt(peak)) if peak > 0 else math.inf}


class metrics:
    """Standard metrics. Each returns (Spacetime, dict of symbols)."""

    @staticmethod
    def minkowski():
        t, x, y, z = sp.symbols("t x y z", real=True)
        return Spacetime(sp.diag(-1, 1, 1, 1), [t, x, y, z]), {"t": t, "x": x, "y": y, "z": z}

    @staticmethod
    def schwarzschild():
        t, r, th, ph = sp.symbols("t r theta phi", real=True)
        M = sp.symbols("M", positive=True)
        f = 1 - 2 * M / r
        g = sp.diag(-f, 1 / f, r**2, r**2 * sp.sin(th) ** 2)
        return Spacetime(g, [t, r, th, ph], simplify=True), {"t": t, "r": r, "theta": th, "phi": ph, "M": M}

    @staticmethod
    def flat_frw():
        t, x, y, z = sp.symbols("t x y z", real=True)
        a = sp.Function("a")
        g = sp.diag(-1, a(t) ** 2, a(t) ** 2, a(t) ** 2)
        return Spacetime(g, [t, x, y, z], simplify=True), {"t": t, "x": x, "y": y, "z": z, "a": a}

    @staticmethod
    def morris_thorne():
        """Static wormhole: ds^2 = -e^{2 Phi(r)} dt^2 + dr^2/(1 - b(r)/r) + r^2 dOmega^2."""
        t, r, th, ph = sp.symbols("t r theta phi", real=True)
        Phi, b = sp.Function("Phi"), sp.Function("b")
        g = sp.diag(-sp.exp(2 * Phi(r)), 1 / (1 - b(r) / r), r**2, r**2 * sp.sin(th) ** 2)
        return Spacetime(g, [t, r, th, ph], simplify=True), {
            "t": t, "r": r, "theta": th, "phi": ph, "Phi": Phi, "b": b}

    @staticmethod
    def alcubierre():
        """ds^2 = -dt^2 + (dx - v f(r_s) dt)^2 + dy^2 + dz^2, bubble centred at x = v t.

        v is the bubble speed in units of c (v > 1 is superluminal); f is the shape function
        (1 inside the bubble, 0 far away). Substitute a concrete f with alcubierre_top_hat()
        or your own sympy Lambda.
        """
        t, x, y, z = sp.symbols("t x y z", real=True)
        v, R, sigma = sp.symbols("v R sigma", positive=True)
        f = sp.Function("f")
        rs = sp.sqrt((x - v * t) ** 2 + y**2 + z**2)
        st = Spacetime.from_adm(1, [-v * f(rs), 0, 0], sp.eye(3), [t, x, y, z])
        return st, {"t": t, "x": x, "y": y, "z": z, "v": v, "R": R, "sigma": sigma, "f": f, "r_s": rs}

    @staticmethod
    def van_den_broeck():
        """ds^2 = -dt^2 + B(r_s)^2 [(dx - v f(r_s) dt)^2 + dy^2 + dz^2] (Van Den Broeck 1999).
        B is large in a pocket inside a small outer bubble and 1 outside; f as for Alcubierre."""
        t, x, y, z = sp.symbols("t x y z", real=True)
        v = sp.symbols("v", positive=True)
        f, B = sp.Function("f"), sp.Function("B")
        rs = sp.sqrt((x - v * t) ** 2 + y**2 + z**2)
        st = Spacetime.from_adm(1, [-v * f(rs), 0, 0], B(rs) ** 2 * sp.eye(3), [t, x, y, z])
        return st, {"t": t, "x": x, "y": y, "z": z, "v": v, "f": f, "B": B, "r_s": rs}

    @staticmethod
    def alcubierre_top_hat(symbols):
        """Alcubierre's profile f(r) = [tanh(s(r+R)) - tanh(s(r-R))] / (2 tanh(s R))."""
        r = sp.symbols("r", positive=True)
        R, s = symbols["R"], symbols["sigma"]
        return sp.Lambda(r, (sp.tanh(s * (r + R)) - sp.tanh(s * (r - R))) / (2 * sp.tanh(s * R)))


# ----- self-test ----------------------------------------------------------------------
def selftest(verbose: bool = True) -> bool:
    """Check the toolkit against textbook results. Returns True when every check passes."""
    results = []

    def check(name, ok, detail=""):
        results.append(bool(ok))
        if verbose:
            print(f"{'PASS' if ok else 'FAIL'}  {name}{('  ' + detail) if detail else ''}")

    st, s = metrics.schwarzschild()
    check("Schwarzschild is vacuum (G_ab = 0)", all(sp.simplify(e) == 0 for e in st.einstein()))
    kr = st.curvature_at((0.0, 3.0, 1.0, 0.5), params={s["M"]: 1.0})["kretschmann"]
    check("Schwarzschild Kretschmann = 48 M^2 / r^6", abs(kr - 48 / 3**6) < 1e-10, f"{kr:.8f}")

    st, s = metrics.flat_frw()
    a, t = s["a"], s["t"]
    expected = 3 * (sp.diff(a(t), t) / a(t)) ** 2 / (8 * sp.pi)
    check("Flat FRW: rho = 3H^2/(8 pi)", sp.simplify(sp.simplify(st.energy_density()) - expected) == 0)

    st, s = metrics.morris_thorne()
    r, b = s["r"], s["b"]
    rho = sp.simplify(st.energy_density())
    check("Morris-Thorne: rho = b'/(8 pi r^2)", sp.simplify(rho - sp.diff(b(r), r) / (8 * sp.pi * r**2)) == 0)

    st, s = metrics.alcubierre()
    x, y, z, v, f, rs = s["x"], s["y"], s["z"], s["v"], s["f"], s["r_s"]
    q = sp.symbols("q", positive=True)
    gauss = {f: sp.Lambda(q, sp.exp(-(q**2)))}
    closed = -(v**2) * (y**2 + z**2) * (-2 * rs * sp.exp(-(rs**2))) ** 2 / (32 * sp.pi * rs**2)
    pts = [(0.0, 0.3, 0.4, -0.2), (0.0, -0.7, 0.1, 0.5), (0.5, 1.1, -0.6, 0.3)]
    worst_adm = worst_4d = 0.0
    for p in pts:
        want = st.evaluate(closed, p, params={v: 1.7})
        worst_adm = max(worst_adm, abs(st.evaluate(st.energy_density(), p, {v: 1.7}, gauss) - want) / abs(want))
        worst_4d = max(worst_4d, abs(st.evaluate(st.energy_density(method="einstein"), p, {v: 1.7}, gauss)
                                     - want) / abs(want))
    check("Alcubierre: Hamiltonian-constraint rho matches Alcubierre (1994)", worst_adm < 1e-9, f"{worst_adm:.1e}")
    check("Alcubierre: 4D Einstein-tensor rho agrees", worst_4d < 1e-9, f"{worst_4d:.1e}")

    energy = st.integrate_on_slice(st.energy_density(), 0.0, [(-5, 5)] * 3, 90, {v: 1.0}, gauss)
    analytic = -math.sqrt(math.pi) / (32 * math.sqrt(2))
    rel = abs(energy - analytic) / abs(analytic)
    check("Alcubierre Gaussian bubble: total energy = -v^2 sqrt(pi) w / (32 sqrt 2)", rel < 0.02,
          f"{energy:.5f} vs {analytic:.5f}")

    ec = st.energy_conditions((0.0, 0.4, 0.5, 0.1), {v: 1.0}, gauss)
    check("Alcubierre wall: NEC and WEC fail", not ec["nec"] and not ec["wec"], f"type {ec['type']}")
    ec = metrics.minkowski()[0].energy_conditions((0.0, 0.0, 0.0, 0.0))
    check("Minkowski: all four energy conditions hold", all(ec[k] for k in ("nec", "wec", "sec", "dec")))

    boosted = _boosted_fluid(rho=-1.0, p=3.0, beta=0.9)
    ec = classify_stress_energy(boosted)
    check("Boosted rho<0 fluid: WEC fails although the observer sees rho>0",
          (not ec["wec"]) and ec["nec"] and float(boosted[0, 0]) > 0, f"observer rho {boosted[0, 0]:.2f}")

    m = 1.0
    hz = horizons_1p1(lambda rr: -np.sqrt(2 * m / rr), np.linspace(0.5, 10, 2001))
    ok = len(hz) == 1 and abs(hz[0]["x"] - 2 * m) < 1e-8 and abs(hz[0]["kappa"] - 1 / (4 * m)) < 1e-6
    check("Painleve-Gullstrand horizon at r = 2M with kappa = 1/(4M)", ok)

    fr = qi.ford_roman_si(1e-15)
    check("Ford-Roman bound at tau0 = 1 fs is -0.0372 J/m^3", abs(fr + 0.0372) < 1e-4, f"{fr:.4f}")

    ok = all(results)
    if verbose:
        print(f"\n{sum(results)}/{len(results)} checks passed")
    return ok


def _boosted_fluid(rho, p, beta):
    """Frame components of an isotropic fluid (rest-frame rho, p) seen by an observer moving at beta."""
    gamma = 1 / math.sqrt(1 - beta * beta)
    lam = np.array([[gamma, -gamma * beta, 0, 0], [-gamma * beta, gamma, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    rest = np.diag([rho, p, p, p])
    return lam.T @ rest @ lam


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "selftest":
        sys.exit(0 if selftest() else 1)
    print(__doc__)
