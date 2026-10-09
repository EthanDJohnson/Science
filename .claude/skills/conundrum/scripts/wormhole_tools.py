#!/usr/bin/env python3
"""wormhole_tools: energy conditions, the ANEC line integral, the Visser-Kar-Dadhich volume
integral and transit times for static, spherically symmetric traversable wormholes, smooth
(Part 1) or thin-shell (Part 2).

Conventions: signature (-,+,+,+); geometric units G = c = 1 with every length in metres, so
energy densities and pressures are in 1/m^2, surface densities in 1/m and masses in m. SI
conversions (c^4/G for energy, c^2/G for mass, 1/c for time) are reported alongside. Einstein's
equations G_ab = 8 pi T_ab. Coupled to the toolkit's unit_tools for CODATA constants.

PART 1. Smooth throats
----------------------
Proper-distance form  ds^2 = -e^{2 Phi(l)} dt^2 + dl^2 + r(l)^2 dOmega^2,  l in (-inf, inf).
Orthonormal stress-energy (rho, p_l, p_t), primes = d/dl:
    8 pi rho = (1 - r'^2 - 2 r r'') / r^2
    8 pi p_l = -(1 - r'^2) / r^2 + 2 Phi' r' / r
    8 pi p_t = r''/r + Phi'' + Phi'^2 + Phi' r'/r
    so rho + p_l = (-r'' + Phi' r') / (4 pi r) = -(e^{Phi} / (4 pi r)) d/dl (e^{-Phi} r').
Morris-Thorne form  ds^2 = -e^{2 Phi(r)} dt^2 + dr^2/(1 - b/r) + r^2 dOmega^2  (two identical
sheets r >= r0, b(r0) = r0) is mapped onto the proper-distance form with
    dr/dl = sqrt(1 - b/r),  d2r/dl2 = (b - b' r)/(2 r^2),  dPhi/dl = Phi_r sqrt(1 - b/r),
    d2Phi/dl2 = Phi_rr (1 - b/r) + Phi_r (b - b' r)/(2 r^2),
which gives back rho = b'/(8 pi r^2) (Morris & Thorne 1988) without coding that formula separately.
Pointwise energy conditions for the diagonal (Hawking-Ellis type I) tensor diag(rho, p_l, p_t, p_t):
    NEC: rho + p_l >= 0 and rho + p_t >= 0;   WEC: NEC and rho >= 0;
    SEC: NEC and rho + p_l + 2 p_t >= 0;      DEC: rho >= |p_l| and rho >= |p_t|.

ANEC along the radial null geodesic through the throat. Static metric: E = -k_t is conserved, so
k^t = E e^{-2 Phi}, k^l = +-E e^{-Phi}, T_kk = E^2 e^{-2 Phi} (rho + p_l), d lambda = e^{Phi} dl / E:
    I = int T_kk d lambda = E int e^{-Phi} (rho + p_l) dl                           (direct)
      = -(E/4 pi) [e^{-Phi} r'/r]_{l1}^{l2} - (E/4 pi) int e^{-Phi} (r'/r)^2 dl     (by parts)
The by-parts form is computed separately as a cross-check. When Phi stays bounded and the
boundary term vanishes (asymptotic flatness, l -> +-inf), I = -(E/4 pi) int e^{-Phi}(r'/r)^2 dl < 0:
every such wormhole violates the ANEC along the throat. Ellis throat r = sqrt(l^2 + b0^2), Phi = 0:
int l^2/(l^2 + b0^2)^2 dl = pi/(2 b0), so I = -E/(8 b0).
Units: lambda is in metres with k^t = 1 where Phi = 0 when E = 1; I is then in 1/m (geometric) and
I c^4/G in J/m^2 (SI).

Volume-integral quantifier (Visser, Kar & Dadhich 2003, PRL 90, 201102), coordinate measure
"r^2 dr" on both sheets: Omega = 2 int_{r0}^{R} (rho + p_r) 4 pi r^2 dr  (m; x c^2/G for kg), and
also  2 int rho 4 pi r^2 dr = 2 m_inf - r0  as R -> inf (VKD eq. 10).

Transit: a traveller moving radially at constant speed v (fraction of c) as measured by the static
observers it passes (Morris & Thorne 1988's parametrisation):
    coordinate time  dt = e^{-Phi} dl / v,     proper time  d tau = dl sqrt(1 - v^2) / v.
For light (v = 1) dt = e^{-Phi} dl and tau = 0. t is the proper time of static clocks where Phi = 0,
e.g. at infinity. Compare with a user-supplied exterior path through compare_paths().

PART 2. Thin-shell wormholes (Visser 1989; Poisson & Visser 1995; Garcia, Lobo & Visser 2012)
-----------------------------------------------------------------------------------------------
Two copies of the region r >= a of a static exterior  -A(r) dt^2 + dr^2/B(r) + r^2 dOmega^2,
glued at r = a(tau). Write Phi_ext = (1/2) ln(A/B) (so A = e^{2 Phi_ext} B). Israel-Lanczos:
    sigma = -sqrt(B + adot^2) / (2 pi a)
    P     = (1/4 pi) [ sqrt(B + adot^2)/a + (addot + B'/2 + Phi_ext' (B + adot^2)) / sqrt(B + adot^2) ]
(A = B = 1 - 2M/r reproduces Poisson & Visser 1995 eqs. 11-12.)  Shell energy conditions come in two
conventions, and energy_conditions() returns both:
- Surface (2+1) conditions on S_ab = diag(sigma, P, P), testing only directions tangent to the shell, as in
  Poisson & Visser 1995 eqs. 18-19: nec_surface sigma + P >= 0; wec_surface nec_surface and sigma >= 0;
  sec_surface nec_surface and sigma + 2P >= 0; dec_surface sigma >= |P|.
- 4D conditions on the distributional T_ab = S_ab delta(eta), which also test directions crossing the shell
  (keys nec, wec, sec, dec). A radial null vector k projects onto the shell as (-u.k) u, so
  T_kk = sigma (u.k)^2 delta(eta) (key nec_radial: sigma >= 0). Hence nec = wec = wec_surface;
  sec = sec_surface and sigma >= 0 (radially boosted observers); dec = dec_surface. A static thin-shell
  wormhole always has sigma < 0, so it violates all four 4D conditions, as its negative shell ANEC requires,
  even where nec_surface holds (2M < a <= 3M for Schwarzschild).
Shell mass m_s = 4 pi a^2 sigma.
Shell ANEC for a radial null crossing of a static shell: T_ab = S_ab delta(eta), S_kk = sigma (u.k)^2,
u.k = -E/sqrt(A(a)), d lambda = d eta / |k^eta|, so I_shell = sigma E / sqrt(A(a)); the vacuum exterior
adds nothing. For A = B: I_shell = -E/(2 pi a), the bound in VKD eq. 17.
Linear stability (Poisson & Visser): adot^2 + V(a) = 0 with V = B - (2 pi a sigma)^2, a barotropic
P(sigma) with beta^2 = dP/dsigma at the static radius a0, and the conservation law with the flux
term of Garcia-Lobo-Visser,  sigma' = -(2/a)(sigma + P) - sigma Phi_ext'. Then V(a0) = V'(a0) = 0
and V''(a0) is linear in beta^2; stable iff V''(a0) > 0. Returns V'' and the critical beta^2.
Transit across the shell: dt = dr / (v sqrt(A B)), d tau = dr sqrt(1-v^2) / (v sqrt(B)) on each side.

Assumptions and validity
- Static, spherically symmetric, classical GR; the stress tensor is whatever Einstein's equations
  require (no matter model). Quantum expectation values are not computed here.
- Part 1: r(l) > 0 and Phi finite everywhere integrated (no horizons). Morris-Thorne form needs
  b(r0) = r0, b'(r0) <= 1 (flare-out) and b(r) < r for r > r0; both sheets are identical.
  Infinite-range ANEC/VKD results assume asymptotic flatness; otherwise give finite limits.
- Part 2: A(a) > 0 and B(a) > 0 (shell outside every horizon of the exterior it keeps), and
  B + adot^2 > 0. Shell ANEC and transit are for a static shell. Stability is linear and radial only.
- Inputs outside these ranges raise ValueError.

Python usage (run from the project root):
    import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
    import wormhole_tools as wt
    th = wt.ProperThroat("sqrt(l**2 + b0**2)", "0", {"b0": 1.0})       # Ellis, b0 = 1 m
    th.anec()["anec_geom_per_m"]                                         # -0.125 = -1/(8 b0)
    th.transit(-1e3, 1e3, v=0.01)                                        # seconds
    sh = wt.ThinShell.schwarzschild(M=wt.mass_to_geom(wt.Q("1 Msun").si), a=1e4)
    sh.surface(); sh.energy_conditions(); sh.mass_kg(); sh.anec(); sh.stability(beta2=-1.0)

Command line:
    python3 wormhole_tools.py selftest
    python3 wormhole_tools.py throat --r "sqrt(l**2+b0**2)" --phi 0 --param b0="1 m" --l1 "-1 km" --l2 "1 km" --v 0.01
    python3 wormhole_tools.py mt --b "r0**2/r" --phi 0 --r0 "1 m" --r1 "1 km" --r2 "1 km" --v 1
    python3 wormhole_tools.py shell --exterior schwarzschild --M "1 Msun" --a "10 km" --beta2 -1
    python3 wormhole_tools.py shell --exterior custom --A "1-2*M/r" --B "1-2*M/r" --param M="1 km" --a "5 km"
    python3 wormhole_tools.py compare --t-thru "2 s" --ext-distance "1 au"
"""
from __future__ import annotations

import argparse
import math
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from unit_tools import Q  # noqa: E402

try:
    import sympy as sp
    import mpmath as mp
except ImportError:  # pragma: no cover
    sys.exit("wormhole_tools.py needs sympy (with mpmath): pip install sympy")

C = Q("c").si                    # m/s, exact
G = Q("G").si                    # m^3 kg^-1 s^-2, CODATA 2018
K_E = 8.9875517923e9             # Coulomb constant 1/(4 pi eps0), N m^2 C^-2, CODATA 2018
mp.mp.dps = max(mp.mp.dps, 30)   # at least 30 digits; never lower a precision another module set

L_SYM, R_SYM = sp.Symbol("l", real=True), sp.Symbol("r", positive=True)


# ----------------------------------------------------------------------------- unit helpers
def mass_to_geom(m_kg: float) -> float:
    """Mass in kg -> geometric length G m / c^2 in metres."""
    return m_kg * G / C**2


def geom_to_kg(m_geom: float) -> float:
    """Geometric mass in metres -> kg (x c^2/G)."""
    return m_geom * C**2 / G


def geom_density_to_si(x: float) -> float:
    """Energy density or pressure 1/m^2 -> J/m^3 (= Pa); surface density 1/m -> J/m^2; ANEC 1/m -> J/m^2."""
    return x * C**4 / G


def charge_to_geom(q_coulomb: float) -> float:
    """Charge in coulombs -> geometric length Q = q sqrt(G k_e) / c^2 (Reissner-Nordstrom)."""
    return q_coulomb * math.sqrt(G * K_E) / C**2


def _parse(expr, params: dict | None):
    loc = {"l": L_SYM, "r": R_SYM, "pi": sp.pi, "E": sp.E}
    e = sp.sympify(expr, locals=loc) if isinstance(expr, str) else sp.sympify(expr)
    if params:
        e = e.subs({sp.Symbol(k, real=True): v for k, v in params.items()})
        e = e.subs({sp.Symbol(k, positive=True): v for k, v in params.items()})
        e = e.subs({sp.Symbol(k): v for k, v in params.items()})
    return e


def _fn(expr, sym):
    return sp.lambdify(sym, expr, modules="mpmath")


def _ec(rho, pl, pt, tol=0.0):
    """Pointwise energy conditions of diag(rho, p_l, p_t, p_t). tol absorbs round-off at exact zeros."""
    nec = rho + pl >= -tol and rho + pt >= -tol
    return {"nec": nec, "wec": nec and rho >= -tol, "sec": nec and rho + pl + 2 * pt >= -tol,
            "dec": rho >= abs(pl) - tol and rho >= abs(pt) - tol,
            "rho_plus_pl": rho + pl, "rho_plus_pt": rho + pt}


# ----------------------------------------------------------------------------- Part 1
def _stress_from_l_derivs(r, r1, r2, ph1, ph2, omr=None):
    """(rho, p_l, p_t) in 1/m^2 from r, r', r'', Phi', Phi'' (derivatives in proper distance l).
    omr = 1 - r'^2 supplied analytically where possible: computing it as 1 - r1**2 loses all digits
    far from the throat, and over an infinite range the leftover ~1/r error does not integrate away."""
    if omr is None:
        omr = 1 - r1**2
    rho = (omr - 2 * r * r2) / (8 * mp.pi * r**2)
    pl = (-omr / r**2 + 2 * ph1 * r1 / r) / (8 * mp.pi)
    pt = (r2 / r + ph2 + ph1**2 + ph1 * r1 / r) / (8 * mp.pi)
    return rho, pl, pt


class ProperThroat:
    """Wormhole in proper-distance form; r(l) and Phi(l) are sympy expressions or strings in 'l' (metres)."""

    def __init__(self, r_expr, phi_expr="0", params: dict | None = None):
        r = _parse(r_expr, params)
        phi = _parse(phi_expr, params)
        free = (r.free_symbols | phi.free_symbols) - {L_SYM}
        if free:
            raise ValueError(f"unset parameters {sorted(map(str, free))}; pass them in params")
        self.r, self.phi = r, phi
        d = lambda e, n: _fn(sp.diff(e, L_SYM, n), L_SYM)  # noqa: E731
        self._r, self._r1, self._r2 = _fn(r, L_SYM), d(r, 1), d(r, 2)
        self._p, self._p1, self._p2 = _fn(phi, L_SYM), d(phi, 1), d(phi, 2)
        try:                                  # 1 - r'^2 in closed form (e.g. b0^2/(l^2 + b0^2) for Ellis)
            self._omr = _fn(sp.simplify(1 - sp.diff(r, L_SYM)**2), L_SYM)
        except Exception:  # pragma: no cover - fall back to the subtractive form
            self._omr = lambda l: 1 - self._r1(l)**2
        self.scale = float(abs(self._r(0)))
        if not self.scale > 0:
            raise ValueError("r(0) must be positive")
        for k in range(-60, 61):                       # sample l = scale * tan(theta) over the line
            l = self.scale * math.tan(k * math.pi / 122)
            rv, pv = self._r(l), self._p(l)
            if not (mp.isfinite(rv) and rv > 0 and mp.isfinite(pv)):
                raise ValueError(f"need r(l) > 0 and finite Phi(l); fails at l = {l:.4g} m")

    def stress(self, l: float) -> dict:
        rho, pl, pt = _stress_from_l_derivs(self._r(l), self._r1(l), self._r2(l), self._p1(l), self._p2(l), self._omr(l))
        rho, pl, pt = float(rho), float(pl), float(pt)
        return {"rho": rho, "p_l": pl, "p_t": pt, "units": "1/m^2 (geometric)",
                "rho_J_m3": geom_density_to_si(rho), "p_l_Pa": geom_density_to_si(pl),
                "p_t_Pa": geom_density_to_si(pt)}

    def energy_conditions(self, l: float) -> dict:
        s = self.stress(l)
        return _ec(s["rho"], s["p_l"], s["p_t"], tol=1e-14 * max(1.0, abs(s["rho"])))

    def anec(self, l1: float = -math.inf, l2: float = math.inf, E: float = 1.0) -> dict:
        """ANEC integral along the radial null geodesic from l1 to l2, E = -k_t (dimensionless)."""
        if not l1 < l2:
            raise ValueError("need l1 < l2")
        a = mp.mpf(l1) if math.isfinite(l1) else -mp.inf
        b = mp.mpf(l2) if math.isfinite(l2) else mp.inf
        pts = [a] + [mp.mpf(x) for x in (-self.scale, 0, self.scale) if l1 < x < l2] + [b]

        def direct(l):
            rho, pl, _ = _stress_from_l_derivs(self._r(l), self._r1(l), self._r2(l), self._p1(l), self._p2(l), self._omr(l))
            return mp.e**(-self._p(l)) * (rho + pl)

        I_direct = E * mp.quad(direct, pts)
        I_parts_bulk = -E / (4 * mp.pi) * mp.quad(lambda l: mp.e**(-self._p(l)) * (self._r1(l) / self._r(l))**2, pts)

        def bterm(x):
            if math.isfinite(x):
                return mp.e**(-self._p(x)) * self._r1(x) / self._r(x)
            lim = sp.limit(sp.exp(-self.phi) * sp.diff(self.r, L_SYM) / self.r, L_SYM, sp.oo if x > 0 else -sp.oo)
            if not lim.is_finite:
                raise ValueError("boundary term e^{-Phi} r'/r diverges at infinity; integrate over a finite range")
            return mp.mpf(float(lim))
        I_bdry = -E / (4 * mp.pi) * (bterm(l2) - bterm(l1))
        I_parts = I_parts_bulk + I_bdry
        val = float(I_direct)
        return {"anec_geom_per_m": val, "anec_by_parts": float(I_parts), "boundary_term": float(I_bdry),
                "anec_J_per_m2": geom_density_to_si(val), "E": E,
                "agree": abs(float(I_direct - I_parts)) <= 1e-8 * max(abs(val), 1e-30)}

    def transit(self, l1: float, l2: float, v: float = 1.0) -> dict:
        """Radial crossing from l1 to l2 at constant local speed v (fraction of c, 0 < v <= 1)."""
        if not 0 < v <= 1:
            raise ValueError("v must satisfy 0 < v <= 1")
        if not (math.isfinite(l1) and math.isfinite(l2)):
            raise ValueError("transit needs finite l1, l2")
        lo, hi = sorted((l1, l2))
        pts = [mp.mpf(lo)] + [mp.mpf(x) for x in (-self.scale, 0, self.scale) if lo < x < hi] + [mp.mpf(hi)]
        t = float(mp.quad(lambda l: mp.e**(-self._p(l)), pts)) / v
        lprop = hi - lo
        tau = lprop * math.sqrt(1 - v * v) / v
        return {"proper_length_m": lprop, "t_coord_s": t / C, "tau_traveller_s": tau / C, "v": v}


class MorrisThorne:
    """Morris-Thorne wormhole with b(r), Phi(r) in 'r' (metres), throat r0; two identical sheets."""

    def __init__(self, b_expr, phi_expr="0", r0: float = 1.0, params: dict | None = None, r_check_max: float | None = None):
        b, phi = _parse(b_expr, params), _parse(phi_expr, params)
        free = (b.free_symbols | phi.free_symbols) - {R_SYM}
        if free:
            raise ValueError(f"unset parameters {sorted(map(str, free))}; pass them in params")
        self.b, self.phi, self.r0 = b, phi, float(r0)
        d = lambda e, n: _fn(sp.diff(e, R_SYM, n), R_SYM)  # noqa: E731
        self._b, self._b1, self._b2 = _fn(b, R_SYM), d(b, 1), d(b, 2)
        self._p, self._p1, self._p2 = _fn(phi, R_SYM), d(phi, 1), d(phi, 2)
        if abs(float(self._b(r0)) - r0) > 1e-9 * r0:
            raise ValueError(f"throat condition b(r0) = r0 fails: b(r0) = {float(self._b(r0)):.6g} m")
        if float(self._b1(r0)) > 1 + 1e-12:
            raise ValueError("flare-out condition b'(r0) <= 1 fails")
        rmax = r_check_max or 1e6 * r0
        for k in range(1, 400):
            rr = r0 * (rmax / r0) ** (k / 400)
            if not float(self._b(rr)) < rr or not mp.isfinite(self._p(rr)):
                raise ValueError(f"need b(r) < r and finite Phi for r > r0; fails at r = {rr:.4g} m")

    def _lderivs(self, r, f=None):
        """r, dr/dl, d2r/dl2, dPhi/dl, d2Phi/dl2 and 1 - (dr/dl)^2 = b/r at radius r (f = 1 - b/r if known)."""
        r = mp.mpf(r)
        b, b1, p1, p2 = self._b(r), self._b1(r), self._p1(r), self._p2(r)
        if f is None:
            f = max(1 - b / r, mp.mpf(0))
        r_l = mp.sqrt(f)
        r_ll = (b - b1 * r) / (2 * r**2)
        return r, r_l, r_ll, p1 * r_l, p2 * f + p1 * r_ll, b / r

    def _fs(self, u):
        """With r = r0 + u^2: (r, f = 1 - b/r, s = sqrt(f)/u). Near the throat r - b cancels catastrophically,
        so for u^2 < 1e-6 r0 use r - b = u^2 (1 - b'(r0)) - u^4 b''(r0)/2 + O(u^6) (relative error ~1e-12)."""
        u = mp.mpf(u)
        r = self.r0 + u * u
        if u * u < 1e-6 * self.r0:
            g = (1 - self._b1(self.r0)) - u * u * self._b2(self.r0) / 2
            return r, u * u * g / r, mp.sqrt(g / r)
        f = 1 - self._b(r) / r
        return r, f, mp.sqrt(f) / u

    def stress(self, r: float) -> dict:
        if r < self.r0:
            raise ValueError("r must be >= r0")
        rho, pl, pt = (float(x) for x in _stress_from_l_derivs(*self._lderivs(r)))
        return {"rho": rho, "p_r": pl, "p_t": pt, "units": "1/m^2 (geometric)",
                "rho_J_m3": geom_density_to_si(rho), "p_r_Pa": geom_density_to_si(pl),
                "p_t_Pa": geom_density_to_si(pt)}

    def energy_conditions(self, r: float) -> dict:
        s = self.stress(r)
        return _ec(s["rho"], s["p_r"], s["p_t"], tol=1e-14 * max(1.0, abs(s["rho"])))

    def _uq(self, g, R):
        """Both sheets: 2 * int_0^{sqrt(R - r0)} g(r, f, s, u) du, with r = r0 + u^2 (g includes dr/du = 2u)."""
        if 1 - float(self._b1(self.r0)) < 1e-12:
            raise ValueError("b'(r0) = 1 (marginal flare-out): the proper length near the throat diverges; not supported")
        if R < self.r0:
            raise ValueError("R must be >= r0")
        Ru = mp.sqrt(R - self.r0) if math.isfinite(R) else mp.inf
        k = mp.sqrt(self.r0)
        return 2 * mp.quad(lambda u: g(*self._fs(u), u), [0, k, Ru] if Ru > k else [0, Ru])

    def anec(self, R: float = math.inf, E: float = 1.0) -> dict:
        """ANEC along the radial null geodesic from r = R on one sheet through the throat to r = R on the other."""
        def direct(r, f, s, u):                       # e^{-Phi} (rho + p_l) dl/du, dl/du = 2u/sqrt(f) = 2/s
            rho, pl, _ = _stress_from_l_derivs(*self._lderivs(r, f))
            return mp.e**(-self._p(r)) * (rho + pl) * 2 / s
        I_direct = E * self._uq(direct, R)
        bulk = -E / (4 * mp.pi) * self._uq(lambda r, f, s, u: mp.e**(-self._p(r)) * s * 2 * u * u / r**2, R)
        bd = 0 if not math.isfinite(R) else -E / (2 * mp.pi) * mp.e**(-self._p(R)) * mp.sqrt(1 - self._b(R) / R) / R
        val = float(I_direct)
        return {"anec_geom_per_m": val, "anec_by_parts": float(bulk + bd), "boundary_term": float(bd),
                "anec_J_per_m2": geom_density_to_si(val), "E": E,
                "agree": abs(float(I_direct - bulk - bd)) <= 1e-7 * max(abs(val), 1e-30)}

    def vkd(self, R: float = math.inf) -> dict:
        """Visser-Kar-Dadhich quantifiers on both sheets with the r^2 dr measure (VKD eq. 9)."""
        def rp(r):
            s = _stress_from_l_derivs(*self._lderivs(r))
            return (s[0] + s[1]) * 4 * mp.pi * r**2
        lo = self.r0
        hi = R if math.isfinite(R) else mp.inf
        pts = [lo, 2 * lo, hi] if hi > 2 * lo else [lo, hi]
        om = 2 * mp.quad(rp, pts)
        mrho = 2 * mp.quad(lambda r: _stress_from_l_derivs(*self._lderivs(r))[0] * 4 * mp.pi * r**2, pts)
        return {"omega_rho_plus_pr_m": float(om), "omega_kg": geom_to_kg(float(om)),
                "int_rho_dV_m": float(mrho), "int_rho_dV_kg": geom_to_kg(float(mrho))}

    def proper_length(self, r: float) -> float:
        """Proper radial distance from the throat to r on one sheet, metres."""
        if r < self.r0:
            raise ValueError("r must be >= r0")
        return float(self._uq(lambda rr, f, s, u: 2 / s, r)) / 2

    def transit(self, r1: float, r2: float, v: float = 1.0) -> dict:
        """From r1 on sheet 1 through the throat to r2 on sheet 2 at constant local speed v."""
        if not 0 < v <= 1:
            raise ValueError("v must satisfy 0 < v <= 1")
        def tint(r, f, s, u):
            return mp.e**(-self._p(r)) * 2 / s
        t = (float(self._uq(tint, r1)) + float(self._uq(tint, r2))) / 2 / v
        lprop = self.proper_length(r1) + self.proper_length(r2)
        return {"proper_length_m": lprop, "t_coord_s": t / C,
                "tau_traveller_s": lprop * math.sqrt(1 - v * v) / v / C, "v": v}


# ----------------------------------------------------------------------------- Part 2
class ThinShell:
    """Thin-shell wormhole: two copies of r >= a of -A dt^2 + dr^2/B + r^2 dOmega^2, glued at r = a."""

    def __init__(self, A_expr, B_expr=None, a: float = 1.0, params: dict | None = None):
        A = _parse(A_expr, params)
        B = A if B_expr is None else _parse(B_expr, params)
        free = (A.free_symbols | B.free_symbols) - {R_SYM}
        if free:
            raise ValueError(f"unset parameters {sorted(map(str, free))}; pass them in params")
        self.A, self.B, self.a = A, B, float(a)
        phi = sp.log(A / B) / 2
        self._A, self._B, self._B1, self._B2 = _fn(A, R_SYM), _fn(B, R_SYM), _fn(sp.diff(B, R_SYM), R_SYM), _fn(sp.diff(B, R_SYM, 2), R_SYM)
        self._ph1, self._ph2 = _fn(sp.diff(phi, R_SYM), R_SYM), _fn(sp.diff(phi, R_SYM, 2), R_SYM)
        if not (float(self._A(a)) > 0 and float(self._B(a)) > 0):
            raise ValueError(f"shell radius a = {a:.6g} m must lie outside the horizon: need A(a) > 0 and B(a) > 0")

    # presets (M, Q, Lambda geometric: M and Q in metres, Lambda in 1/m^2)
    @classmethod
    def schwarzschild(cls, M: float, a: float):
        return cls(f"1 - 2*({M!r})/r", None, a)

    @classmethod
    def reissner_nordstrom(cls, M: float, Qg: float, a: float):
        return cls(f"1 - 2*({M!r})/r + ({Qg!r})**2/r**2", None, a)

    @classmethod
    def schwarzschild_de_sitter(cls, M: float, Lam: float, a: float):
        """Lam > 0: de Sitter; Lam < 0: anti-de Sitter."""
        return cls(f"1 - 2*({M!r})/r - ({Lam!r})*r**2/3", None, a)

    def surface(self, adot: float = 0.0, addot: float = 0.0) -> dict:
        """sigma and P from the Israel junction conditions; adot = da/dtau, addot = d2a/dtau2 (1/m)."""
        a = self.a
        B, B1, ph1 = float(self._B(a)), float(self._B1(a)), float(self._ph1(a))
        s = B + adot**2
        if s <= 0:
            raise ValueError("need B(a) + adot^2 > 0")
        q = math.sqrt(s)
        sigma = -q / (2 * math.pi * a)
        P = (q / a + (addot + B1 / 2 + ph1 * s) / q) / (4 * math.pi)
        return {"sigma": sigma, "P": P, "units": "1/m (geometric)",
                "sigma_J_m2": geom_density_to_si(sigma), "P_N_m": geom_density_to_si(P)}

    def energy_conditions(self, adot: float = 0.0, addot: float = 0.0) -> dict:
        """4D conditions of the distributional shell (nec, wec, sec, dec, nec_radial) and the surface (2+1)
        conditions in Poisson & Visser's convention (*_surface); see the module docstring."""
        s = self.surface(adot, addot)
        sg, P = s["sigma"], s["P"]
        tol = 1e-14 * abs(sg)
        radial = sg >= -tol                      # radial null k: T_kk = sigma (u.k)^2 delta(eta)
        nec_s = sg + P >= -tol
        wec_s = nec_s and radial
        sec_s = nec_s and sg + 2 * P >= -tol
        dec_s = sg >= abs(P) - tol
        return {"nec": wec_s, "wec": wec_s, "sec": sec_s and radial, "dec": dec_s, "nec_radial": radial,
                "nec_surface": nec_s, "wec_surface": wec_s, "sec_surface": sec_s, "dec_surface": dec_s,
                "sigma_plus_P": sg + P, "sigma_plus_2P": sg + 2 * P}

    def mass(self) -> float:
        """Shell mass 4 pi a^2 sigma (static), geometric metres."""
        return 4 * math.pi * self.a**2 * self.surface()["sigma"]

    def mass_kg(self) -> float:
        return geom_to_kg(self.mass())

    def anec(self, E: float = 1.0) -> dict:
        """Shell contribution sigma E / sqrt(A(a)) to the ANEC for a radial null crossing of the static shell."""
        val = self.surface()["sigma"] * E / math.sqrt(float(self._A(self.a)))
        return {"anec_geom_per_m": val, "anec_J_per_m2": geom_density_to_si(val), "E": E}

    def stability(self, beta2: float | None = None) -> dict:
        """Linear radial stability about the static shell; V''(a0) as a function of beta^2 = dP/dsigma."""
        a = self.a
        B, B1, B2 = float(self._B(a)), float(self._B1(a)), float(self._B2(a))
        ph1, ph2 = float(self._ph1(a)), float(self._ph2(a))
        st = self.surface()
        s0, P0 = st["sigma"], st["P"]

        def derivs(b2):
            s1 = -(2 / a) * (s0 + P0) - s0 * ph1
            s2 = (2 / a**2) * (s0 + P0) - (2 / a) * (1 + b2) * s1 - s1 * ph1 - s0 * ph2
            m, m1, m2 = 2 * math.pi * a * s0, 2 * math.pi * (s0 + a * s1), 2 * math.pi * (2 * s1 + a * s2)
            return B - m * m, B1 - 2 * m * m1, B2 - 2 * (m1 * m1 + m * m2)
        V, V1, Vpp0 = derivs(0.0)
        slope = derivs(1.0)[2] - Vpp0
        scale = abs(B) + abs(B1) * a
        if abs(V) > 1e-9 * scale or abs(V1) * a > 1e-9 * scale:
            raise ValueError("internal check failed: static shell is not an equilibrium (V, V' != 0)")
        crit = -Vpp0 / slope if slope != 0 else math.nan
        out = {"V_pp_at_beta2_0": Vpp0, "dVpp_dbeta2": slope, "beta2_critical": crit,
               "stable_if": "beta2 < critical" if slope < 0 else "beta2 > critical"}
        if beta2 is not None:
            vpp = Vpp0 + slope * beta2
            out.update({"beta2": beta2, "V_pp": vpp, "stable": vpp > 0})
        return out

    def transit(self, r1: float, r2: float, v: float = 1.0) -> dict:
        """From r1 on side 1, through the static shell at a, to r2 on side 2 at constant local speed v."""
        if not 0 < v <= 1:
            raise ValueError("v must satisfy 0 < v <= 1")
        if r1 < self.a or r2 < self.a:
            raise ValueError("r1 and r2 must be >= a")
        def seg(r, f):
            return float(mp.quad(f, [self.a, r])) if r > self.a else 0.0
        ft = lambda r: 1 / mp.sqrt(self._A(r) * self._B(r))  # noqa: E731
        fl = lambda r: 1 / mp.sqrt(self._B(r))  # noqa: E731
        t = (seg(r1, ft) + seg(r2, ft)) / v
        lprop = seg(r1, fl) + seg(r2, fl)
        return {"proper_length_m": lprop, "t_coord_s": t / C,
                "tau_traveller_s": lprop * math.sqrt(1 - v * v) / v / C, "v": v}


def compare_paths(t_thru_s: float, ext_distance_m: float | None = None, t_ext_s: float | None = None) -> dict:
    """Shortcut test: T_thru against the exterior light time T_ext (given directly, or as distance/c)."""
    if (ext_distance_m is None) == (t_ext_s is None):
        raise ValueError("give exactly one of ext_distance_m or t_ext_s")
    t_ext = t_ext_s if t_ext_s is not None else ext_distance_m / C
    if not t_ext > 0:
        raise ValueError("exterior time must be positive")
    return {"t_thru_s": t_thru_s, "t_ext_s": t_ext, "ratio": t_thru_s / t_ext, "shortcut": t_thru_s < t_ext}


# ----------------------------------------------------------------------------- selftest
def selftest(verbose: bool = True) -> bool:
    results = []

    def check(name, got, want, rel=1e-8, absol=0.0):
        ok = abs(got - want) <= max(rel * abs(want), absol)
        results.append(ok)
        if verbose:
            print(f"[{'PASS' if ok else 'FAIL'}] {name}: got {got:.12g}, want {want:.12g}")

    def truth(name, cond):
        results.append(bool(cond))
        if verbose:
            print(f"[{'PASS' if cond else 'FAIL'}] {name}")

    pi = math.pi
    # 1. Poisson & Visser 1995 (gr-qc/9506083) eqs. 11-12, fetched: "sigma = - 1/(2 pi a) sqrt(1 - 2M/a + adot^2);
    #    p = + 1/(4 pi a) (1 - M/a + adot^2 + a addot)/sqrt(1 - 2M/a + adot^2)".
    M, a, ad, add = 1.0, 3.7, 0.3, 0.05
    sh = ThinShell.schwarzschild(M, a)
    s = sh.surface(ad, add)
    q = math.sqrt(1 - 2 * M / a + ad**2)
    check("PV95 eq.11 sigma (Schwarzschild, dynamic)", s["sigma"], -q / (2 * pi * a), 1e-12)
    check("PV95 eq.12 P (Schwarzschild, dynamic)", s["P"], (1 - M / a + ad**2 + a * add) / (4 * pi * a * q), 1e-12)

    # 2. Flat limit M -> 0 of PV95 eqs. 18-19: sigma = -1/(2 pi a), P = +1/(4 pi a); shell mass -2a.
    #    In SI for a = 1 m: -2 c^2/G kg, compared with M_Jup = GM_J/G (IAU nominal, via unit_tools "Mjup").
    fl = ThinShell.schwarzschild(0.0, 2.0)
    check("flat limit sigma = -1/(2 pi a)", fl.surface()["sigma"], -1 / (4 * pi), 1e-14)
    check("flat limit P = 1/(4 pi a)", fl.surface()["P"], 1 / (8 * pi), 1e-14)
    one_m = ThinShell.schwarzschild(0.0, 1.0)
    check("flat a = 1 m shell mass / M_Jup (= -2 c^2/G / M_Jup)", one_m.mass_kg() / Q("Mjup").si,
          Q("-2 m * c^2 / G").si / Q("Mjup").si, 1e-12)

    # 3. PV95 eq. 27, fetched: "V''(a0) = -2 a0^-2 [ 2M/a0 + (M^2/a0^2)/(1 - 2M/a0) + (1 + 2 beta0^2)(1 - 3M/a0) ]".
    for a0, b2 in ((5.0, 0.4), (2.6, 4.0), (40.0, -0.7)):
        st = ThinShell.schwarzschild(1.0, a0).stability(b2)
        x = 1.0 / a0
        ref = -2 / a0**2 * (2 * x + x * x / (1 - 2 * x) + (1 + 2 * b2) * (1 - 3 * x))
        check(f"PV95 eq.27 V''(a0={a0} M, beta2={b2})", st["V_pp"], ref, 1e-9)
    # PV95 eq. 34, fetched: "a0_pm = 6(1 + 4 beta0^2) M / (3 + 10 beta0^2 -+ sqrt(4 beta0^4 - 12 beta0^2 - 3))";
    #    on that curve V'' = 0, so the critical beta^2 at a0 = a0_+ must equal beta0^2.
    b2 = 4.0
    ap = 6 * (1 + 4 * b2) / (3 + 10 * b2 - math.sqrt(4 * b2**2 - 12 * b2 - 3))
    check("PV95 eq.34 stability boundary a0+ (beta0^2 = 4)", ThinShell.schwarzschild(1.0, ap).stability()["beta2_critical"], b2, 1e-8)
    # PV95 eq. 36, fetched: "II : beta0^2 <= -1/2, a0 > a0-": far from the hole (M/a0 -> 0) the boundary is -1/2.
    check("PV95 region II boundary -> -1/2 as M/a0 -> 0", ThinShell.schwarzschild(1e-9, 1.0).stability()["beta2_critical"], -0.5, 1e-7)

    # 4. Garcia, Lobo & Visser 2012 (arXiv:1112.2057) eqs. 22-23 for A != B, fetched:
    #    "sigma = -1/(4 pi a)[sqrt(1 - b+/a + adot^2) + sqrt(1 - b-/a + adot^2)]",
    #    "P = 1/(8 pi a)[(1 + adot^2 + a addot - (b+ + a b+')/(2a))/sqrt(1 - b+/a + adot^2) + sqrt(1 - b+/a + adot^2) a Phi+' + (same for -)]".
    #    Exterior here: b = 2m + k^2/r (B = 1 - b/r), Phi = -g/r (A = e^{2 Phi} B), symmetric sides.
    m_, k_, g_, a, ad, add = 1.0, 0.8, 0.5, 4.2, 0.25, -0.07
    Bx = f"1 - (2*{m_} + {k_}**2/r)/r"
    sh = ThinShell(f"exp(-2*{g_}/r)*({Bx})", Bx, a)
    s = sh.surface(ad, add)
    bb, bp, php = 2 * m_ + k_**2 / a, -k_**2 / a**2, g_ / a**2
    qq = math.sqrt(1 - bb / a + ad**2)
    check("GLV12 eq.22 sigma (A != B)", s["sigma"], -2 * qq / (4 * pi * a), 1e-12)
    check("GLV12 eq.23 P (A != B)", s["P"],
          2 * ((1 + ad**2 + a * add - (bb + a * bp) / (2 * a)) / qq + qq * a * php) / (8 * pi * a), 1e-12)
    # Stability with A != B must still give an equilibrium (V = V' = 0 checked internally) - consistency only.
    truth("GLV12 flux term: static A != B shell is an equilibrium of V(a)", "beta2_critical" in sh.stability())

    # 5. Morris-Thorne stress tensor against GLV12 eqs. 2-4 (fetched): "rho(r) = b'/(8 pi r^2)",
    #    "p_r(r) = -1/(8 pi r^2)[2 Phi'(b - r) + b']",
    #    "p_t(r) = -1/(16 pi r^2)[(-b + 3 r b' - 2r) Phi' + 2r(b - r)(Phi')^2 + 2r(b - r) Phi'' + b'' r]".
    #    Our code reaches these through the proper-distance formulas, so this is an independent check.
    #    GLV's metric (their eq. 1) is ds^2 = -e^{2 Phi}(1 - b/r) dt^2 + ..., so Phi_GLV = Phi_MT - (1/2) ln(1 - b/r):
    #    we feed Phi_MT = -g/r + (1/2) ln(1 - b/r) and compare with GLV at Phi_GLV = -g/r (valid for r > r0).
    r0, mi, gg = 1.0, 0.3, 0.4
    bexpr = f"{r0}**2/r + 2*{mi}*(1 - {r0}/r)"
    mt = MorrisThorne(bexpr, f"-{gg}/r + log(1 - ({bexpr})/r)/2", r0)
    rs = 1.7
    X = sp.Symbol("x")
    bs = r0**2 / X + 2 * mi * (1 - r0 / X)
    bv, b1, b2_ = (float(sp.diff(bs, X, n).subs(X, rs)) for n in (0, 1, 2))
    p1, p2 = gg / rs**2, -2 * gg / rs**3
    st = mt.stress(rs)
    check("Morris-Thorne rho = b'/(8 pi r^2)", st["rho"], b1 / (8 * pi * rs**2), 1e-12)
    check("GLV12 eq.3 p_r", st["p_r"], -(2 * p1 * (bv - rs) + b1) / (8 * pi * rs**2), 1e-12)
    check("GLV12 eq.4 p_t", st["p_t"], -((-bv + 3 * rs * b1 - 2 * rs) * p1 + 2 * rs * (bv - rs) * p1**2
                                         + 2 * rs * (bv - rs) * p2 + b2_ * rs) / (16 * pi * rs**2), 1e-11)

    # 6. VKD 2003 eq. 10 (fetched): "including both asymptotic regions, we have oint rho dV = 2 m_inf - r0",
    #    with m_inf = mi for this b (b -> 2 mi at infinity).
    #    VKD's boundary term at infinity in eq. 12 vanishes only if e^{2 Phi} ~ 1 - 2 m_inf / r, so use Phi = -m_inf/r.
    mtv = MorrisThorne(bexpr, f"-{mi}/r", r0)
    vk = mtv.vkd()
    check("VKD03 eq.10 oint rho dV = 2 m_inf - r0", vk["int_rho_dV_m"], 2 * mi - r0, 1e-9)
    #    VKD03 eq. 13 (fetched): "oint [rho + p_r] dV = - int_{r0}^inf (1 - b') [ln(exp[2 phi]/(1 - b/r))] dr"
    #    (their phi is the Morris-Thorne Phi: their eq. 11 matches 8 pi (rho + p_r) = (b'r - b)/r^3 + 2(1 - b/r)Phi'/r;
    #    integrating eq. 11 x 4 pi r^2 over one sheet gives half of eq. 12, so eq. 13 already covers both sheets).
    #    The log is singular at r0, so integrate in t = r - r0 with the exact factorisation
    #    1 - b/r = t (t + 2 r0 - 2 m_inf)/r^2 (no cancellation). Closed form of the same integral: -2 r0 + 3 m - 2 m^2/r0.
    #    For t >= r0 write the same log as log1p(-(r0^2 + 2 m t)/(r0 + t)^2) (exact algebra): ln(1 - eps) computed
    #    as ln of a rounded number carries a ~1e-30 absolute error that tanh-sinh spreads over an enormous range.
    b1m = lambda x: (-r0**2 + 2 * mi * r0) / x**2  # noqa: E731
    lnf = lambda t: (mp.log(t * (t + 2 * r0 - 2 * mi) / (r0 + t)**2) if t < r0  # noqa: E731
                     else mp.log1p(-(r0**2 + 2 * mi * t) / (r0 + t)**2))
    eq13 = -mp.quad(lambda t: (1 - b1m(r0 + t)) * (-2 * mi / (r0 + t) - lnf(t)), [0, r0, mp.inf])
    check("VKD03 eq.13 volume-integral theorem (both sheets)", vk["omega_rho_plus_pr_m"], float(eq13), 1e-9)
    check("same, closed form -2 r0 + 3 m - 2 m^2/r0", vk["omega_rho_plus_pr_m"], -2 * r0 + 3 * mi - 2 * mi**2 / r0, 1e-9)

    # 7. Ellis throat r = sqrt(l^2 + b0^2), Phi = 0. Closed forms: rho = p_l = -b0^2/(8 pi r^4) (from b = b0^2/r
    #    in rho = b'/(8 pi r^2)), and int_{-inf}^{inf} l^2/(l^2 + b0^2)^2 dl = pi/(2 b0) (elementary; the
    #    antiderivative is (1/2b0) atan(l/b0) - l/(2(l^2 + b0^2))), giving ANEC = -E/(8 b0).
    #    The tool integrates rho + p_l directly; the by-parts form is reported separately.
    b0 = 2.5
    el = ProperThroat("sqrt(l**2 + b0**2)", "0", {"b0": b0})
    check("Ellis rho at throat = -1/(8 pi b0^2)", el.stress(0.0)["rho"], -1 / (8 * pi * b0**2), 1e-12)
    for E in (1.0, 2.7):
        an = el.anec(E=E)
        check(f"Ellis ANEC = -E/(8 b0), E = {E}", an["anec_geom_per_m"], -E / (8 * b0), 1e-10)
    truth("Ellis ANEC: direct and by-parts forms agree", el.anec()["agree"])
    mte = MorrisThorne(f"{b0}**2/r", "0", b0)
    check("Ellis in Morris-Thorne form: ANEC = -E/(8 b0)", mte.anec()["anec_geom_per_m"], -1 / (8 * b0), 1e-8)

    # 8. Thin-shell ANEC vs VKD03 eq. 17 (fetched): "the ANEC integral satisfies I < -(2/4pi) int_a^inf 1/r^2 dr
    #    = -1/(2 pi a)" when the geometry is Schwarzschild beyond a; a shell at a saturates it.
    for Mx in (0.0, 1.0):
        check(f"shell ANEC = -1/(2 pi a) (M = {Mx})", ThinShell.schwarzschild(Mx, 3.0).anec()["anec_geom_per_m"], -1 / (2 * pi * 3.0), 1e-12)
    #    Smooth flat-space regularisation r = a + sqrt(l^2 + eps^2) - eps -> thin shell as eps -> 0:
    #    exact bulk integral 2 int (r'/r)^2 dl -> 2/a, so the smooth ANEC must approach -1/(2 pi a) (eps = 1e-4 a,
    #    error O(eps/a): tolerance 1e-3 is set by eps, not loosened).
    sm = ProperThroat("3 + sqrt(l**2 + 1e-8) - 1e-4", "0")
    check("smooth -> thin-shell limit of the ANEC", sm.anec()["anec_geom_per_m"], -1 / (2 * pi * 3.0), 1e-3)

    # 9. Transit, Morris-Thorne integrator: b = 2M, Phi = 0 (spatial Schwarzschild). Flamm's closed form for
    #    proper radial distance from r = 2M: l(r) = sqrt(r(r - 2M)) + 2M ln[(sqrt r + sqrt(r - 2M))/sqrt(2M)].
    Mf = 1.0
    fla = MorrisThorne(f"2*{Mf}", "0", 2 * Mf)
    lf = lambda r: math.sqrt(r * (r - 2 * Mf)) + 2 * Mf * math.log((math.sqrt(r) + math.sqrt(r - 2 * Mf)) / math.sqrt(2 * Mf))  # noqa: E731
    tr = fla.transit(10.0, 30.0, v=1.0)
    check("Flamm proper length through throat (r1 = 10M, r2 = 30M)", tr["proper_length_m"], lf(10.0) + lf(30.0), 1e-9)
    check("light crossing time = proper length / c when Phi = 0", tr["t_coord_s"] * C, lf(10.0) + lf(30.0), 1e-9)
    #    Thin shell, Schwarzschild exterior: light time = tortoise difference
    #    r* = r + 2M ln(r/2M - 1) (Misner, Thorne & Wheeler 1973, eq. 25.30 form) on each side.
    ash = 3.0
    rstar = lambda r: r + 2 * Mf * math.log(r / (2 * Mf) - 1)  # noqa: E731
    ts = ThinShell.schwarzschild(Mf, ash).transit(10.0, 20.0, v=1.0)
    check("thin-shell light time = tortoise differences", ts["t_coord_s"] * C, rstar(10.0) - rstar(ash) + rstar(20.0) - rstar(ash), 1e-9)
    #    Special-relativity limit: Ellis, Phi = 0, v = 0.6: t = L/v, tau = L sqrt(1 - v^2)/v = 0.8 t.
    tt = el.transit(-100.0, 100.0, v=0.6)
    check("tau = t / gamma for Phi = 0 (v = 0.6)", tt["tau_traveller_s"] / tt["t_coord_s"], 0.8, 1e-9)

    # 10. Energy conditions for the Schwarzschild thin shell, from PV95 eqs. 18-19 (surface convention):
    #     sigma + P = (3M/a - 1)/(4 pi a sqrt(1 - 2M/a)), sigma + 2P = (M/a)/(2 pi a sqrt(...)) > 0, sigma < 0:
    #     surface NEC and SEC hold for 2M < a <= 3M, fail for a > 3M; surface WEC and DEC always fail.
    #     The 4D conditions also test radial directions, where T_kk = sigma (u.k)^2 delta < 0, so all four fail
    #     for every static shell. That must agree with the negative shell ANEC (a consistency check, not a reference).
    sh25 = ThinShell.schwarzschild(1.0, 2.5)
    e_in, e_out = sh25.energy_conditions(), ThinShell.schwarzschild(1.0, 4.0).energy_conditions()
    truth("shell at a = 2.5M: surface NEC and SEC hold, surface WEC and DEC fail",
          e_in["nec_surface"] and e_in["sec_surface"] and not e_in["wec_surface"] and not e_in["dec_surface"])
    truth("shell at a = 4M: surface NEC fails", not e_out["nec_surface"])
    truth("shell at a = 2.5M: 4D NEC, WEC, SEC and DEC all fail (radial T_kk < 0), consistent with its ANEC < 0",
          not (e_in["nec"] or e_in["wec"] or e_in["sec"] or e_in["dec"] or e_in["nec_radial"])
          and sh25.anec()["anec_geom_per_m"] < 0)
    ee = el.energy_conditions(0.0)
    truth("Ellis throat: NEC, WEC, SEC, DEC all fail", not (ee["nec"] or ee["wec"] or ee["sec"] or ee["dec"]))

    # 11. Refusals outside the validity range.
    def raises(fn):
        try:
            fn()
        except ValueError:
            return True
        return False
    truth("refuses shell inside the horizon", raises(lambda: ThinShell.schwarzschild(1.0, 1.9)))
    truth("refuses b(r0) != r0", raises(lambda: MorrisThorne("0.5", "0", 1.0)))
    truth("refuses flare-out violation b'(r0) > 1", raises(lambda: MorrisThorne("r**2", "0", 1.0)))

    n_ok = sum(results)
    if verbose:
        print(f"\n{n_ok}/{len(results)} checks passed")
    return n_ok == len(results)


# ----------------------------------------------------------------------------- CLI
def _len(text: str) -> float:
    """CLI length or mass -> geometric metres. Masses (kg units) are converted with G/c^2."""
    q = Q(text)
    if q.kind == "mass":
        return mass_to_geom(q.si)
    return q.expect("length").si


def _params(items) -> dict:
    out = {}
    for it in items or []:
        k, v = it.split("=", 1)
        q = Q(v)
        out[k] = mass_to_geom(q.si) if q.kind == "mass" else (q.si if q.kind != "dimensionless" else float(q))
    return out


def _fmt(d: dict) -> str:
    return "\n".join(f"  {k}: {v:.6g}" if isinstance(v, float) else f"  {k}: {v}" for k, v in d.items())


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv or argv[0] in ("help", "-h", "--help"):
        print(__doc__)
        return 0
    if argv[0] == "selftest":
        return 0 if selftest() else 1
    p = argparse.ArgumentParser(prog="wormhole_tools.py")
    sub = p.add_subparsers(dest="cmd", required=True)
    a1 = sub.add_parser("throat", help="proper-distance form r(l), Phi(l)")
    a1.add_argument("--r", required=True); a1.add_argument("--phi", default="0")
    a1.add_argument("--param", action="append"); a1.add_argument("--at", default="0 m")
    a1.add_argument("--l1"); a1.add_argument("--l2"); a1.add_argument("--v", type=float, default=1.0)
    a2 = sub.add_parser("mt", help="Morris-Thorne form b(r), Phi(r)")
    a2.add_argument("--b", required=True); a2.add_argument("--phi", default="0"); a2.add_argument("--r0", required=True)
    a2.add_argument("--param", action="append"); a2.add_argument("--r1"); a2.add_argument("--r2")
    a2.add_argument("--v", type=float, default=1.0)
    a3 = sub.add_parser("shell", help="thin-shell wormhole")
    a3.add_argument("--exterior", default="schwarzschild", choices=["schwarzschild", "rn", "sds", "custom"])
    a3.add_argument("--M", default="0 m"); a3.add_argument("--charge", default="0 m", help="geometric length or coulombs (C)")
    a3.add_argument("--Lambda", type=float, default=0.0, help="1/m^2"); a3.add_argument("--A"); a3.add_argument("--B")
    a3.add_argument("--param", action="append"); a3.add_argument("--a", required=True)
    a3.add_argument("--adot", type=float, default=0.0); a3.add_argument("--addot", default="0 1/m")
    a3.add_argument("--beta2", type=float); a3.add_argument("--r1"); a3.add_argument("--r2")
    a3.add_argument("--v", type=float, default=1.0)
    a4 = sub.add_parser("compare", help="shortcut test against an exterior path")
    a4.add_argument("--t-thru", required=True); a4.add_argument("--ext-distance"); a4.add_argument("--ext-time")
    args = p.parse_args(argv)
    try:
        if args.cmd == "throat":
            th = ProperThroat(args.r, args.phi, _params(args.param))
            at = Q(args.at).expect("length").si
            print(f"stress at l = {at:g} m:\n{_fmt(th.stress(at))}")
            print(f"energy conditions:\n{_fmt(th.energy_conditions(at))}")
            print(f"ANEC over the whole geodesic (E = 1):\n{_fmt(th.anec())}")
            if args.l1 and args.l2:
                print(f"transit:\n{_fmt(th.transit(Q(args.l1).expect('length').si, Q(args.l2).expect('length').si, args.v))}")
        elif args.cmd == "mt":
            r0 = _len(args.r0)
            mt = MorrisThorne(args.b, args.phi, r0, _params(args.param))
            print(f"stress at the throat r0 = {r0:g} m:\n{_fmt(mt.stress(r0))}")
            print(f"energy conditions at the throat:\n{_fmt(mt.energy_conditions(r0))}")
            print(f"ANEC (E = 1, both sheets to infinity):\n{_fmt(mt.anec())}")
            print(f"Visser-Kar-Dadhich volume integrals:\n{_fmt(mt.vkd())}")
            if args.r1 and args.r2:
                print(f"transit:\n{_fmt(mt.transit(_len(args.r1), _len(args.r2), args.v))}")
        elif args.cmd == "shell":
            a, M = _len(args.a), _len(args.M)
            cq = Q(args.charge)
            Qg = charge_to_geom(cq.si) if cq.kind != "length" else cq.si
            if args.exterior == "schwarzschild":
                sh = ThinShell.schwarzschild(M, a)
            elif args.exterior == "rn":
                sh = ThinShell.reissner_nordstrom(M, Qg, a)
            elif args.exterior == "sds":
                sh = ThinShell.schwarzschild_de_sitter(M, args.Lambda, a)
            else:
                if not args.A:
                    raise ValueError("custom exterior needs --A (and optionally --B)")
                sh = ThinShell(args.A, args.B, a, _params(args.param))
            addot = Q(args.addot).si
            print(f"shell at a = {a:g} m:\n{_fmt(sh.surface(args.adot, addot))}")
            print("energy conditions (nec, wec, sec, dec: 4D, including radial crossings; "
                  f"*_surface: 2+1, Poisson-Visser convention):\n{_fmt(sh.energy_conditions(args.adot, addot))}")
            print(f"  shell mass: {sh.mass():.6g} m = {sh.mass_kg():.6g} kg = {sh.mass_kg() / Q('Mjup').si:.4g} M_Jup")
            print(f"shell ANEC (static, E = 1):\n{_fmt(sh.anec())}")
            print(f"linear stability:\n{_fmt(sh.stability(args.beta2))}")
            if args.r1 and args.r2:
                print(f"transit:\n{_fmt(sh.transit(_len(args.r1), _len(args.r2), args.v))}")
        elif args.cmd == "compare":
            t = Q(args.t_thru).expect("time").si
            if args.ext_distance:
                print(_fmt(compare_paths(t, ext_distance_m=Q(args.ext_distance).expect("length").si)))
            else:
                print(_fmt(compare_paths(t, t_ext_s=Q(args.ext_time).expect("time").si)))
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
