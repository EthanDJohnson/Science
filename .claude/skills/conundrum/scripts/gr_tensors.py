#!/usr/bin/env python3
"""General-relativity toolkit for /conundrum agents.

Computes curvature, the stress-energy a metric requires (via Einstein's
equations), what observers measure, energy-condition probes, and slice
integrals, so claims like "this metric needs negative energy" get computed
rather than argued.

Conventions: signature (-,+,+,+), geometric units G = c = 1,
Gamma^a_bc = 1/2 g^ad (d_b g_dc + d_c g_db - d_d g_bc),
R_bd = d_a Gamma^a_bd - d_d Gamma^a_ba + Gamma^a_ae Gamma^e_bd - Gamma^a_de Gamma^e_ba,
G_ab = R_ab - 1/2 g_ab R = 8 pi T_ab. Coordinate 0 is time.

Usage from an agent's own script (run from the project root):

    import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
    import sympy as sp
    from gr_tensors import Spacetime, metrics, to_si

    st, s = metrics.alcubierre()            # s: dict of the symbols used
    rho = st.energy_density()               # Eulerian energy density, symbolic
    top_hat = metrics.alcubierre_top_hat(s)  # Alcubierre's tanh profile
    E = st.integrate_on_slice(rho, t=0.0, bounds=[(-1.8, 1.8)] * 3, n=96,
                              params={s["v"]: 1.0, s["R"]: 1.0, s["sigma"]: 8.0},
                              functions={s["f"]: top_hat})
    # E = -0.2233 (metres, geometric); resolve the wall (spacing <~ 1/(4 sigma)) and
    # confirm convergence by re-running with a larger n.
    print(E, "m (geometric) =", to_si.energy_joules(E), "J  (with lengths in metres)")

For spherically symmetric bubbles the same number follows from the 1D integral
E = -(v^2/12) * int_0^inf f'(r)^2 r^2 dr, a useful cross-check.

CLI:  python3 gr_tensors.py selftest   # verify the toolkit against known results
      python3 gr_tensors.py help       # print this text
"""
from __future__ import annotations

import math
import sys

try:
    import sympy as sp
except ImportError:  # pragma: no cover - exercised only without sympy
    sys.exit("gr_tensors.py needs sympy: pip install sympy numpy")

try:
    import numpy as np
except ImportError:  # pragma: no cover
    np = None

# CODATA 2018 values, SI.
C = 299_792_458.0
G_NEWTON = 6.67430e-11
HBAR = 1.054571817e-34


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
        self._cache = {}

    # ----- construction helpers -------------------------------------------------
    @classmethod
    def from_adm(cls, lapse, shift_up, spatial_metric, coords, simplify=False):
        """Build g from 3+1 data: ds^2 = -N^2 dt^2 + h_ij (dx^i + b^i dt)(dx^j + b^j dt)."""
        h = sp.Matrix(spatial_metric)
        b_up = sp.Matrix(shift_up)
        b_low = h * b_up
        n = len(coords)
        g = sp.zeros(n, n)
        g[0, 0] = -lapse**2 + (b_up.T * b_low)[0, 0]
        for i in range(1, n):
            g[0, i] = g[i, 0] = b_low[i - 1]
            for j in range(1, n):
                g[i, j] = h[i - 1, j - 1]
        return cls(g, coords, simplify=simplify)

    def _s(self, expr):
        return sp.simplify(expr) if self.simplify else expr

    # ----- curvature -------------------------------------------------------------
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

    # ----- observers ---------------------------------------------------------------
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

    def energy_density(self, u=None):
        """rho = T_ab u^a u^b for a unit timelike u (default: Eulerian observers)."""
        u = self.eulerian_observer() if u is None else sp.Matrix(u)
        return self._s(self.contract(self.stress_energy(), u))

    def spatial_volume_element(self):
        """sqrt(det h_ij) of the t = const slice."""
        h = self.g[1:, 1:]
        return self._s(sp.sqrt(h.det()))

    # ----- numerics ----------------------------------------------------------------
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

    def compile(self, expr, params=None, functions=None):
        """Numpy callable of the coordinates, after substituting params and concrete functions."""
        if np is None:
            raise RuntimeError("numpy is required for numeric evaluation: pip install numpy")
        prepared = self._prepare(expr, params, functions)
        leftover = prepared.free_symbols - set(self.coords)
        if leftover:
            raise ValueError(f"unassigned symbols: {sorted(map(str, leftover))}; pass them in params")
        # cse: curvature expressions repeat the same subterms many times.
        return sp.lambdify(self.coords, prepared, "numpy", cse=True)

    def evaluate(self, expr, point, params=None, functions=None) -> float:
        """Evaluate a scalar expression at a coordinate point (sequence in coordinate order)."""
        return float(self.compile(expr, params, functions)(*point))

    def integrate_on_slice(self, density, t, bounds, n=64, params=None, functions=None) -> float:
        """Midpoint-rule integral of density * sqrt(h) d^3x on the slice x^0 = t over a box.

        Resolve thin features: grid spacing should be a few times smaller than the
        thinnest wall (for Alcubierre's top hat, spacing <~ 1/(4 sigma)). Check
        convergence by comparing n and ~1.5 n. Evaluated in x-slabs to bound memory.
        """
        if np is None:
            raise RuntimeError("numpy is required: pip install numpy")
        if self.dim != 4 or len(bounds) != 3:
            raise ValueError("integrate_on_slice expects 4 coordinates and 3 spatial bounds")
        integrand = self.compile(density * self.spatial_volume_element(), params, functions)
        axes, widths = [], []
        for lo, hi in bounds:
            step = (hi - lo) / n
            axes.append(lo + step * (np.arange(n) + 0.5))
            widths.append(step)
        yy, zz = np.meshgrid(axes[1], axes[2], indexing="ij")
        total = 0.0
        for xv in axes[0]:
            xx = np.full_like(yy, xv)
            total += float(np.sum(np.broadcast_to(integrand(t, xx, yy, zz), yy.shape)))
        return total * widths[0] * widths[1] * widths[2]

    def energy_condition_scan(self, point, params=None, functions=None, observer=None, n_dirs=64):
        """Numerically probe WEC/NEC at one point.

        Builds an orthonormal spatial triad orthogonal to the observer (default Eulerian)
        and evaluates T(k, k) for null k = u + e over n_dirs unit directions e.
        Returns rho = T(u, u), the minimum T(k, k), and pass/fail flags.
        """
        if np is None:
            raise RuntimeError("numpy is required: pip install numpy")
        n = self.dim
        g_num = np.array(self.compile(self.g, params, functions)(*point), dtype=float).reshape(n, n)
        t_num = np.array(self.compile(self.stress_energy(), params, functions)(*point), dtype=float).reshape(n, n)
        u_sym = self.eulerian_observer() if observer is None else sp.Matrix(observer)
        u = np.array(self.compile(u_sym, params, functions)(*point), dtype=float).reshape(n)
        u = u / math.sqrt(-u @ g_num @ u)
        triad = []
        for i in range(1, n):
            e = np.zeros(n)
            e[i] = 1.0
            e = e + (e @ g_num @ u) * u  # remove the component along u (u.u = -1)
            for f in triad:
                e = e - (e @ g_num @ f) * f
            e = e / math.sqrt(e @ g_num @ e)
            triad.append(e)
        rho = float(u @ t_num @ u)
        k_vals = []
        golden = math.pi * (3 - math.sqrt(5))
        for i in range(n_dirs):  # Fibonacci sphere of directions
            zc = 1 - 2 * (i + 0.5) / n_dirs
            r = math.sqrt(1 - zc * zc)
            phi = golden * i
            dirn = (r * math.cos(phi), r * math.sin(phi), zc)
            k = u + sum(c * e for c, e in zip(dirn, triad))
            k_vals.append(float(k @ t_num @ k))
        nec_min = min(k_vals)
        tol = 1e-12 * max(1.0, float(np.max(np.abs(t_num))))
        return {"rho": rho, "nec_min": nec_min, "wec_ok": rho >= -tol and nec_min >= -tol,
                "nec_ok": nec_min >= -tol}


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

        v is the bubble speed in units of c (v > 1 is superluminal); f is the shape
        function (1 inside the bubble, 0 far away). Substitute a concrete f with
        alcubierre_top_hat() or your own sympy Lambda.
        """
        t, x, y, z = sp.symbols("t x y z", real=True)
        v, R, sigma = sp.symbols("v R sigma", positive=True)
        f = sp.Function("f")
        rs = sp.sqrt((x - v * t) ** 2 + y**2 + z**2)
        st = Spacetime.from_adm(1, [-v * f(rs), 0, 0], sp.eye(3), [t, x, y, z])
        return st, {"t": t, "x": x, "y": y, "z": z, "v": v, "R": R, "sigma": sigma, "f": f, "r_s": rs}

    @staticmethod
    def alcubierre_top_hat(symbols):
        """Alcubierre's profile f(r) = [tanh(s(r+R)) - tanh(s(r-R))] / (2 tanh(s R))."""
        r = sp.symbols("r", positive=True)
        R, s = symbols["R"], symbols["sigma"]
        return sp.Lambda(r, (sp.tanh(s * (r + R)) - sp.tanh(s * (r - R))) / (2 * sp.tanh(s * R)))


# ----- self-test ---------------------------------------------------------------------
def selftest(verbose: bool = True) -> bool:
    """Check the toolkit against textbook results. Returns True when every check passes."""
    results = []

    def check(name, ok, detail=""):
        results.append(ok)
        if verbose:
            print(f"{'PASS' if ok else 'FAIL'}  {name}{('  ' + detail) if detail else ''}")

    st, _ = metrics.schwarzschild()
    check("Schwarzschild is vacuum (G_ab = 0)", all(sp.simplify(e) == 0 for e in st.einstein()))

    st, s = metrics.flat_frw()
    a, t = s["a"], s["t"]
    rho = sp.simplify(st.energy_density())
    expected = 3 * (sp.diff(a(t), t) / a(t)) ** 2 / (8 * sp.pi)
    check("Flat FRW: rho = 3H^2/(8 pi)", sp.simplify(rho - expected) == 0)

    st, s = metrics.morris_thorne()
    r, b, Phi = s["r"], s["b"], s["Phi"]
    rho = sp.simplify(st.energy_density())
    check("Morris-Thorne: rho = b'/(8 pi r^2)",
          sp.simplify(rho - sp.diff(b(r), r) / (8 * sp.pi * r**2)) == 0)

    st, s = metrics.alcubierre()
    rho = st.energy_density()
    x, y, z, v, f = s["x"], s["y"], s["z"], s["v"], s["f"]
    rr = sp.symbols("rr", positive=True)
    gauss = sp.Lambda(rr, sp.exp(-(rr**2)))
    dfdr = sp.Lambda(rr, -2 * rr * sp.exp(-(rr**2)))
    rs = s["r_s"]
    closed = -(v**2) * (y**2 + z**2) * dfdr(rs) ** 2 / (32 * sp.pi * rs**2)
    worst = 0.0
    for p in [(0.0, 0.3, 0.4, -0.2), (0.0, -0.7, 0.1, 0.5), (0.5, 1.1, -0.6, 0.3)]:
        got = st.evaluate(rho, p, params={v: 1.7}, functions={f: gauss})
        want = st.evaluate(closed, p, params={v: 1.7})
        worst = max(worst, abs(got - want) / max(abs(want), 1e-30))
    check("Alcubierre: Eulerian rho matches Alcubierre (1994) closed form", worst < 1e-9,
          f"max rel. error {worst:.1e}")

    width = 1.0
    energy = st.integrate_on_slice(rho, t=0.0, bounds=[(-5, 5)] * 3, n=90,
                                   params={v: 1.0}, functions={f: gauss})
    analytic = -math.sqrt(math.pi) * width / (32 * math.sqrt(2))
    rel = abs(energy - analytic) / abs(analytic)
    check("Alcubierre Gaussian bubble: total energy = -v^2 sqrt(pi) w / (32 sqrt 2)", rel < 0.02,
          f"numeric {energy:.5f} vs analytic {analytic:.5f} ({rel:.1%})")

    scan = st.energy_condition_scan((0.0, 0.4, 0.5, 0.1), params={v: 1.0}, functions={f: gauss})
    check("Alcubierre: WEC and NEC fail inside the wall", (not scan["wec_ok"]) and (not scan["nec_ok"]),
          f"rho={scan['rho']:.3e}, min T(k,k)={scan['nec_min']:.3e}")

    mst, _ = metrics.minkowski()
    scan = mst.energy_condition_scan((0.0, 0.0, 0.0, 0.0))
    check("Minkowski: energy conditions hold trivially", scan["wec_ok"] and scan["nec_ok"])

    ok = all(results)
    if verbose:
        print(f"\n{sum(results)}/{len(results)} checks passed")
    return ok


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "selftest":
        sys.exit(0 if selftest() else 1)
    print(__doc__)
