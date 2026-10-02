#!/usr/bin/env python3
"""Stress-energy and energy conditions for a 4D metric known only numerically.

What it computes
----------------
Given a metric as a numpy-vectorised callable g(t, x, y, z) -> 4x4 nested list / array of
shape (4, 4, *S) (coordinates may be any chart: Cartesian, spherical, comoving ...), it
computes at chosen points, by finite differences:

  * Christoffel symbols  Gamma^a_bc = 1/2 g^ad (d_b g_dc + d_c g_db - d_d g_bc)
  * Riemann              R^a_bcd = d_c Gamma^a_db - d_d Gamma^a_cb
                                   + Gamma^a_ce Gamma^e_db - Gamma^a_de Gamma^e_cb
    with d_e Gamma^a_bc built analytically from first and second metric derivatives:
        d_e g^ad = -g^ap (d_e g_pq) g^qd,
        d_e Gamma^a_bc = (d_e g^ad) Gam_dbc + g^ad 1/2 (d_e d_b g_dc + d_e d_c g_db - d_e d_d g_bc)
  * Ricci R_bd = R^a_bad, scalar R = g^bd R_bd, Einstein G_ab = R_ab - 1/2 g_ab R
  * T_ab = G_ab / (8 pi)                       (Einstein's equations, G = c = 1)
  * Eulerian observer n^a = -N g^{a0}, N = 1/sqrt(-g^{00}); rho_E = T_ab n^a n^b
  * rho_u = T_ab u^a u^b for any timelike 4-velocity (normalised here)
  * NEC/WEC/SEC/DEC for ALL observers with the Hawking-Ellis type, by projecting T on an
    orthonormal frame and calling gr_tensors.classify_stress_energy (type I exact from the
    rest-frame density and principal pressures; types II/III/IV by sampled boosts up to
    0.99c and 64 null directions)
  * tidal tensor E_ij = R_(i)(0)(j)(0) in the orthonormal frame of an observer (relative
    acceleration of neighbouring geodesics a^i = -E^i_j xi^j), Kretschmann scalar
  * slice integrals int rho_E sqrt(det h) d^3x over a coordinate box on t = const, split
    into negative and positive parts (midpoint rule)

Finite differences (all 4th-order centred, step h_c per coordinate):
    d_c f   ~ [-f(+2) + 8 f(+1) - 8 f(-1) + f(-2)] / (12 h_c)
    d_c^2 f ~ [-f(+2) + 16 f(+1) - 30 f(0) + 16 f(-1) - f(-2)] / (12 h_c^2)
    d_c d_d f (c != d): the first-derivative stencil applied along c and along d (16 points).
Truncation error O(h^4); round-off in second derivatives ~ 1e-16 |g| / h^2.

Step-halving convergence estimate: every curvature quantity is computed with step h and
with h/2. The value returned is the h/2 one; the error estimate is |X(h) - X(h/2)|. In
the truncation-dominated regime the true error of X(h/2) is about |X(h)-X(h/2)|/15, so the
estimate is conservative by ~15x; when round-off dominates it still tracks the noise.
Energy-condition verdicts use this estimate as a noise floor: a condition counts as
violated only when the violating quantity is more negative than -(2 err + atol)
("robust" verdict, keys nec/wec/sec/dec). The strict verdicts of classify_stress_energy
(relative tolerance 1e-10 on the rescaled tensor) are kept as nec_strict etc.; a point with
strict-but-not-robust failure is reported as "marginal". If max |T_AB| is below the noise
floor the point is reported as vacuum (all conditions hold).

Assumptions and validity
------------------------
  * Signature (-,+,+,+), coordinate 0 is the time used for the Eulerian slicing (g^{00} < 0
    required for Eulerian quantities), geometric units G = c = 1 with lengths in metres:
    curvature and T_ab in 1/m^2, slice energies in metres (E[m] * c^4/G -> J).
  * The metric must be C^2 (better C^6) on the whole stencil (+-2h around each point,
    including in t). Kinks, jumps and thin shells carry distributional (delta-function)
    stress-energy that finite differences cannot represent: there the step-halving error
    estimate does not shrink, and the point is flagged "converged": False. Treat sheet
    contributions with Israel junction conditions instead.
  * Choose h ~ 1e-2 of the smallest feature length (wall thickness, 1/sigma, ...); points
    must stay at least 2h from coordinate singularities (r = 0, theta = 0, pi).
  * Sampling is pointwise: "everywhere" claims need a scan dense enough to resolve walls.
  * Raises ValueError for non-positive steps, non-finite or non-symmetric metrics, non-
    Lorentzian metrics (det g >= 0), non-timelike observers, or g^{00} >= 0.

Units: Python API takes coordinates in metres (and seconds * c, i.e. metres, for t);
returns geometric-unit tensors (1/m^2) plus SI conversions where densities and slice
energies are returned (J/m^3, J, kg) via gr_tensors.to_si.

Python usage (from the project root):
    import sys, numpy as np
    sys.path.insert(0, ".claude/skills/conundrum/scripts")
    from numeric_stress_energy import NumericSpacetime, alcubierre_metric
    g = alcubierre_metric(v=1.0, R=1.0, sigma=8.0)        # tanh top-hat, comoving at t
    st = NumericSpacetime(g, h=1e-3)
    pts = np.array([[0.0, 1.0, 0.3, 0.0], [0.0, 0.2, 0.95, 0.1]])
    print(st.eulerian_density(pts))                       # {'rho': [...], 'err': [...], ...}
    print(st.energy_conditions(pts[0]))                   # one point: type, nec, wec, ...
    print(st.scan_energy_conditions(pts))                 # many points: counts + worst
    print(st.integrate_parts(0.0, [(-2, 2)] * 3, n=48))   # E_-, E_+ on t = 0

Command line:
    python3 numeric_stress_energy.py selftest
    python3 numeric_stress_energy.py alcubierre --v 10 --R "100 m" --sigma "1 1/m" --n 9
    python3 numeric_stress_energy.py star --M "1 Msun" --R "10 km" --r "5 km"
    python3 numeric_stress_energy.py point --metric my_metric.py:g --h 1e-3 --at 0 1 0 0
"""
from __future__ import annotations

import argparse
import importlib.util
import math
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (os.path.join(_HERE, "..", "..", "..", ".claude", "skills", "conundrum", "scripts"),
           ".claude/skills/conundrum/scripts"):
    if os.path.isdir(_p) and _p not in sys.path:
        sys.path.insert(0, _p)

from gr_tensors import _orthonormal_frame, classify_stress_energy, to_si  # noqa: E402

_W1 = {-2: 1.0 / 12, -1: -8.0 / 12, 1: 8.0 / 12, 2: -1.0 / 12}          # d/dx, times 1/h
_W2 = {-2: -1.0 / 12, -1: 16.0 / 12, 0: -30.0 / 12, 1: 16.0 / 12, 2: -1.0 / 12}  # d2/dx2, 1/h^2
_CHUNK = 4096


def _as_points(points):
    p = np.asarray(points, dtype=float)
    if p.ndim == 1:
        p = p[None, :]
    if p.ndim != 2 or p.shape[1] != 4:
        raise ValueError("points must have shape (4,) or (N, 4): (t, x1, x2, x3)")
    if not np.all(np.isfinite(p)):
        raise ValueError("points must be finite")
    return p


class NumericSpacetime:
    """A metric known only as a vectorised callable g(t, x1, x2, x3)."""

    def __init__(self, metric, h, sym_tol: float = 1e-12):
        self.metric = metric
        hv = np.broadcast_to(np.asarray(h, dtype=float), (4,)).copy()
        if not np.all(np.isfinite(hv)) or np.any(hv <= 0):
            raise ValueError("finite-difference step h must be positive (scalar or 4 values)")
        self.h = hv
        self.sym_tol = sym_tol

    # ----- metric evaluation ------------------------------------------------------
    def g(self, points):
        """Metric components g_ab at points (N,4) -> (N,4,4); validated."""
        p = _as_points(points)
        return self._g(p.T)

    def _g(self, X):
        n = X.shape[1]
        raw = self.metric(X[0], X[1], X[2], X[3])
        out = np.empty((n, 4, 4))
        for a in range(4):
            for b in range(4):
                out[:, a, b] = np.broadcast_to(np.asarray(raw[a][b], dtype=float), (n,))
        if not np.all(np.isfinite(out)):
            raise ValueError("metric returned non-finite values (singularity on the stencil?)")
        scale = np.max(np.abs(out), axis=(1, 2))
        if np.any(np.max(np.abs(out - out.transpose(0, 2, 1)), axis=(1, 2)) > self.sym_tol * scale):
            raise ValueError("metric is not symmetric")
        return 0.5 * (out + out.transpose(0, 2, 1))

    def _derivs(self, X, hv):
        """g, d_c g_ab (N,c,a,b), d_c d_d g_ab (N,c,d,a,b) by 4th-order centred differences."""
        n = X.shape[1]
        cache = {}

        def at(offset):
            key = tuple(offset)
            if key not in cache:
                Y = X + (np.asarray(offset, dtype=float) * hv)[:, None]
                cache[key] = self._g(Y)
            return cache[key]

        g0 = at((0, 0, 0, 0))
        dg = np.zeros((n, 4, 4, 4))
        ddg = np.zeros((n, 4, 4, 4, 4))
        for c in range(4):
            e = np.zeros(4, dtype=int)
            for k, w in _W1.items():
                e[:] = 0
                e[c] = k
                dg[:, c] += w * at(e)
            dg[:, c] /= hv[c]
            for k, w in _W2.items():
                e[:] = 0
                e[c] = k
                ddg[:, c, c] += w * at(e)
            ddg[:, c, c] /= hv[c] ** 2
        for c in range(4):
            for d in range(c + 1, 4):
                acc = np.zeros((n, 4, 4))
                for i, wi in _W1.items():
                    for j, wj in _W1.items():
                        e = np.zeros(4, dtype=int)
                        e[c], e[d] = i, j
                        acc += wi * wj * at(e)
                acc /= hv[c] * hv[d]
                ddg[:, c, d] = acc
                ddg[:, d, c] = acc
        return g0, dg, ddg

    @staticmethod
    def _geometry(g, dg, ddg):
        det = np.linalg.det(g)
        if np.any(det >= 0):
            raise ValueError("metric is not Lorentzian (det g >= 0) at some point")
        gi = np.linalg.inv(g)
        # Gam_dbc = 1/2 (d_b g_dc + d_c g_db - d_d g_bc); dg[n,k,i,j] = d_k g_ij
        glow = 0.5 * (np.einsum("nbdc->ndbc", dg) + np.einsum("ncdb->ndbc", dg) - dg)
        gam = np.einsum("nad,ndbc->nabc", gi, glow)
        dgi = -np.einsum("nap,nepq,nqd->nead", gi, dg, gi)          # d_e g^ad
        dglow = 0.5 * (np.einsum("nebdc->nedbc", ddg) + np.einsum("necdb->nedbc", ddg)
                       - np.einsum("nedbc->nedbc", ddg))           # d_e Gam_dbc
        dgam = np.einsum("nead,ndbc->neabc", dgi, glow) + np.einsum("nad,nedbc->neabc", gi, dglow)
        a_term = np.einsum("ncadb->nabcd", dgam)                    # d_c Gamma^a_db
        q_term = np.einsum("nace,nedb->nabcd", gam, gam)            # Gamma^a_ce Gamma^e_db
        riem = a_term - a_term.transpose(0, 1, 2, 4, 3) + q_term - q_term.transpose(0, 1, 2, 4, 3)
        ric = np.einsum("nabad->nbd", riem)
        ric = 0.5 * (ric + ric.transpose(0, 2, 1))
        rs = np.einsum("nbd,nbd->n", gi, ric)
        ein = ric - 0.5 * g * rs[:, None, None]
        return {"g": g, "ginv": gi, "christoffel": gam, "riemann": riem, "ricci": ric,
                "ricci_scalar": rs, "einstein": ein, "T": ein / (8 * math.pi)}

    def _curv_chunk(self, X, halving):
        res = self._geometry(*self._derivs(X, self.h))
        if not halving:
            return res, None
        fine = self._geometry(*self._derivs(X, self.h / 2))
        return fine, res

    # ----- public curvature API ---------------------------------------------------
    def curvature(self, points, halving: bool = True):
        """All curvature quantities at points (N,4). Values at step h/2 when halving (default),
        with '<key>_err' = |X(h) - X(h/2)| for christoffel, riemann, ricci_scalar, einstein, T."""
        p = _as_points(points)
        keys = ("christoffel", "riemann", "ricci", "ricci_scalar", "einstein", "T")
        out = {}
        for s in range(0, len(p), _CHUNK):
            fine, coarse = self._curv_chunk(p[s:s + _CHUNK].T, halving)
            for k, v in fine.items():
                out.setdefault(k, []).append(v)
            if coarse is not None:
                for k in keys:
                    out.setdefault(k + "_err", []).append(np.abs(fine[k] - coarse[k]))
        return {k: np.concatenate(v) for k, v in out.items()}

    def stress_energy(self, points, halving: bool = True):
        """T_ab (lower indices, 1/m^2) at points, with step-halving error 'T_err'."""
        c = self.curvature(points, halving)
        return {"T": c["T"], "T_err": c.get("T_err"), "g": c["g"], "ginv": c["ginv"]}

    @staticmethod
    def _eulerian(gi):
        g00 = gi[:, 0, 0]
        if np.any(g00 >= 0):
            raise ValueError("g^{00} >= 0: t = const is not spacelike, no Eulerian observer")
        lapse = 1.0 / np.sqrt(-g00)
        return -lapse[:, None] * gi[:, :, 0]

    @staticmethod
    def _normalise(u, g):
        u = np.asarray(u, dtype=float)
        norm = np.einsum("na,nab,nb->n", u, g, u)
        if np.any(norm >= 0):
            raise ValueError("observer 4-velocity is not timelike at some point")
        if np.any(u[:, 0] <= 0):
            raise ValueError("observer 4-velocity must be future-directed (u^0 > 0)")
        return u / np.sqrt(-norm)[:, None]

    def _observer(self, observer, p, g, gi):
        if observer is None:
            return self._eulerian(gi)
        if callable(observer):
            raw = observer(p[:, 0], p[:, 1], p[:, 2], p[:, 3])
            u = np.stack([np.broadcast_to(np.asarray(raw[a], float), (len(p),)) for a in range(4)], axis=1)
        else:
            u = np.broadcast_to(np.asarray(observer, float), (len(p), 4))
        return self._normalise(u, g)

    def energy_density(self, points, observer=None, halving: bool = True):
        """rho = T_ab u^a u^b (1/m^2) for observer u (None = Eulerian; a 4-vector, an (N,4)
        array or a callable (t,x,y,z) -> 4 components; normalised here). Also J/m^3."""
        p = _as_points(points)
        se = self.stress_energy(p, halving)
        u = self._observer(observer, p, se["g"], se["ginv"])
        rho = np.einsum("na,nab,nb->n", u, se["T"], u)
        err = None if se["T_err"] is None else np.einsum("na,nab,nb->n", np.abs(u), se["T_err"], np.abs(u))
        return {"rho": rho, "err": err, "rho_J_per_m3": to_si.energy_density_j_per_m3(rho), "u": u}

    def eulerian_density(self, points, halving: bool = True):
        return self.energy_density(points, None, halving)

    def tidal_tensor(self, points, observer=None):
        """E_ij = R_(i)(u)(j)(u) in the observer's orthonormal frame (1/m^2; times c^2 -> 1/s^2).
        Relative acceleration of geodesics separated by xi: a^i = -E_ij xi^j."""
        p = _as_points(points)
        c = self.curvature(p, halving=False)
        u = self._observer(observer, p, c["g"], c["ginv"])
        out = []
        for i in range(len(p)):
            e = _orthonormal_frame(c["g"][i], u[i])
            rlow = np.einsum("ae,ebcd->abcd", c["g"][i], c["riemann"][i])
            fr = np.einsum("Aa,Bb,Cc,Dd,abcd->ABCD", e, e, e, e, rlow)
            out.append(fr[1:, 0, 1:, 0])
        return np.array(out)

    def kretschmann(self, points):
        """R_abcd R^abcd (1/m^4)."""
        c = self.curvature(points, halving=False)
        g, gi, r = c["g"], c["ginv"], c["riemann"]
        rlow = np.einsum("nae,nebcd->nabcd", g, r)
        rup = np.einsum("nbf,ncg,ndh,nafgh->nabcd", gi, gi, gi, r)
        return np.einsum("nabcd,nabcd->n", rlow, rup)

    # ----- energy conditions --------------------------------------------------------
    def energy_conditions(self, points, observer=None, atol: float = 0.0, safety: float = 2.0):
        """NEC/WEC/SEC/DEC for all observers at each point. Returns a dict for one point or a
        list of dicts. Keys: type, nec/wec/sec/dec (robust: violation beyond safety*err+atol),
        nec_strict.. (classify_stress_energy verdict), marginal (list), rho_rest, pressures,
        nec_min/wec_min/sec_min (sampled minima, 1/m^2), rho_observer (u or Eulerian),
        rho_eulerian, err (max |T_AB(h)-T_AB(h/2)|), converged."""
        p = _as_points(points)
        single = np.asarray(points).ndim == 1
        se = self.stress_energy(p, halving=True)
        g, gi, T, Terr = se["g"], se["ginv"], se["T"], se["T_err"]
        n_e = self._eulerian(gi)
        u = n_e if observer is None else self._observer(observer, p, g, gi)
        results = []
        for i in range(len(p)):
            e = _orthonormal_frame(g[i], u[i])
            tf = e @ T[i] @ e.T
            tf = 0.5 * (tf + tf.T)
            err = float(np.max(np.abs(e) @ Terr[i] @ np.abs(e).T))
            results.append(self._classify(tf, err, atol, safety,
                                          float(u[i] @ T[i] @ u[i]), float(n_e[i] @ T[i] @ n_e[i])))
        return results[0] if single else results

    @staticmethod
    def _classify(tf, err, atol, safety, rho_obs, rho_eul):
        tol = safety * err + atol
        tmax = float(np.max(np.abs(tf)))
        base = {"rho_observer": rho_obs, "rho_eulerian": rho_eul, "err": err, "tol": tol,
                "T_frame": tf, "converged": err <= 1e-3 * max(tmax, atol) or tmax <= tol}
        if tmax <= tol:
            base.update({"type": "vacuum (within FD error)", "rho_rest": 0.0, "pressures": [0.0] * 3,
                         "nec_min": 0.0, "wec_min": 0.0, "sec_min": 0.0, "marginal": []})
            for k in ("nec", "wec", "sec", "dec"):
                base[k] = base[k + "_strict"] = True
            return base
        cl = classify_stress_energy(tf / tmax)        # scale-free: EC signs are homogeneous in T
        for k in ("nec_min", "wec_min", "sec_min"):
            base[k] = cl[k] * tmax
        base["type"] = cl["type"]
        for k in ("nec", "wec", "sec", "dec"):
            base[k + "_strict"] = bool(cl[k])
        if cl["rho_rest"] is not None:
            rho = cl["rho_rest"] * tmax
            ps = [q * tmax for q in cl["pressures"]]
            nec = all(rho + q >= -tol for q in ps)
            base.update({"rho_rest": rho, "pressures": ps, "nec": nec, "wec": nec and rho >= -tol,
                         "sec": nec and rho + sum(ps) >= -2 * tol,
                         "dec": rho >= -tol and all(abs(q) <= rho + tol for q in ps)})
        else:
            nec = base["nec_min"] >= -tol
            base.update({"rho_rest": None, "pressures": None, "nec": nec,
                         "wec": nec and base["wec_min"] >= -tol,
                         "sec": nec and base["sec_min"] >= -tol,
                         "dec": bool(cl["dec"]) and base["wec_min"] >= -tol})  # DEC: sampled flag
        base["marginal"] = [k for k in ("nec", "wec", "sec", "dec") if base[k] and not base[k + "_strict"]]
        return base

    def scan_energy_conditions(self, points, observer=None, atol: float = 0.0, safety: float = 2.0):
        """Energy conditions over many points. Returns robust and strict violation counts,
        Hawking-Ellis type counts, worst sampled minima with their points, the most negative
        Eulerian density, the number of unconverged points, and skipped points."""
        p = _as_points(points)
        counts = {k: 0 for k in ("nec", "wec", "sec", "dec")}
        strict = dict(counts)
        marginal = dict(counts)
        types, worst = {}, {k: (math.inf, None) for k in ("nec_min", "wec_min", "sec_min", "rho_eulerian")}
        evaluated = skipped = unconverged = 0
        for s in range(0, len(p), _CHUNK):
            block = p[s:s + _CHUNK]
            try:
                rows = self.energy_conditions(block, observer, atol, safety)
            except ValueError:
                rows = []
                for q in block:          # isolate the bad points
                    try:
                        rows.append(self.energy_conditions(q, observer, atol, safety))
                    except ValueError:
                        rows.append(None)
            for q, r in zip(block, rows):
                if r is None:
                    skipped += 1
                    continue
                evaluated += 1
                unconverged += 0 if r["converged"] else 1
                types[r["type"]] = types.get(r["type"], 0) + 1
                for k in counts:
                    counts[k] += 0 if r[k] else 1
                    strict[k] += 0 if r[k + "_strict"] else 1
                    marginal[k] += 1 if k in r["marginal"] else 0
                for k in worst:
                    if r[k] < worst[k][0]:
                        worst[k] = (r[k], tuple(float(x) for x in q))
        return {"points": evaluated, "skipped": skipped, "unconverged": unconverged,
                "violations": counts, "violations_strict": strict, "marginal": marginal,
                "types": types, "worst": worst}

    # ----- slice integrals --------------------------------------------------------------
    def integrate_parts(self, t, bounds, n=48, halving: bool = False):
        """Midpoint-rule integral of rho_E sqrt(det h) d^3x on t = const over a coordinate box.
        Returns total/negative/positive in metres (geometric energy), plus J and kg, and the
        step-halving change of the integral when halving=True. Compare n with ~1.5 n."""
        if len(bounds) != 3 or n < 2:
            raise ValueError("need three (lo, hi) bounds and n >= 2")
        axes, widths = [], []
        for lo, hi in bounds:
            if not hi > lo:
                raise ValueError("bounds must have hi > lo")
            step = (hi - lo) / n
            axes.append(lo + step * (np.arange(n) + 0.5))
            widths.append(step)
        yy, zz = np.meshgrid(axes[1], axes[2], indexing="ij")
        neg = pos = dsum = 0.0
        for xv in axes[0]:
            pts = np.stack([np.full(yy.size, float(t)), np.full(yy.size, xv), yy.ravel(), zz.ravel()], axis=1)
            d = self.energy_density(pts, None, halving)
            sqrt_h = np.sqrt(np.linalg.det(self.g(pts)[:, 1:, 1:]))
            vals = d["rho"] * sqrt_h
            neg += float(vals[vals < 0].sum())
            pos += float(vals[vals > 0].sum())
            if halving:
                dsum += float((d["err"] * sqrt_h).sum())
        dv = widths[0] * widths[1] * widths[2]
        tot = (neg + pos) * dv
        out = {"total": tot, "negative": neg * dv, "positive": pos * dv, "n": n,
               "total_J": to_si.energy_joules(tot), "negative_kg": to_si.mass_kg(neg * dv),
               "positive_kg": to_si.mass_kg(pos * dv), "total_kg": to_si.mass_kg(tot)}
        if halving:
            out["fd_err_bound"] = dsum * dv
        return out


# ----- example metrics (also used by the self-test) -------------------------------------------
def alcubierre_metric(v, R, sigma, x0=0.0):
    """Alcubierre (1994) with the tanh top-hat f, bubble centred at x = x0 + v t, unit lapse,
    shift beta^x = -v f(r_s): ds^2 = -dt^2 + (dx - v f dt)^2 + dy^2 + dz^2."""
    norm = 2 * math.tanh(sigma * R)

    def g(t, x, y, z):
        rs = np.sqrt((x - x0 - v * t) ** 2 + y**2 + z**2)
        f = (np.tanh(sigma * (rs + R)) - np.tanh(sigma * (rs - R))) / norm
        b = -v * f
        one, zero = np.ones_like(rs), np.zeros_like(rs)
        return [[-1 + b * b, b, zero, zero], [b, one, zero, zero],
                [zero, zero, one, zero], [zero, zero, zero, one]]
    return g


def alcubierre_rho_closed(v, R, sigma, t, x, y, z, x0=0.0):
    """Alcubierre (1994) eq. (19): rho_E = -(1/8pi) v^2 (y^2+z^2)/(4 r_s^2) (df/dr_s)^2."""
    rs = np.sqrt((x - x0 - v * t) ** 2 + y**2 + z**2)
    fp = sigma * (1 / np.cosh(sigma * (rs + R)) ** 2 - 1 / np.cosh(sigma * (rs - R)) ** 2) / (2 * math.tanh(sigma * R))
    return -(v**2) * (y**2 + z**2) * fp**2 / (32 * math.pi * rs**2)


def interior_schwarzschild_metric(M, Rg):
    """Constant-density star in Schwarzschild coordinates (t, r, theta, phi), r <= Rg."""
    if not 0 < 2 * M / Rg < 8 / 9:
        raise ValueError("need 0 < 2M/R < 8/9 (Buchdahl) for finite central pressure")
    Rc2 = Rg**3 / (2 * M)

    def g(t, r, th, ph):
        a = 0.5 * (3 * np.sqrt(1 - Rg**2 / Rc2) - np.sqrt(1 - r**2 / Rc2))
        z = np.zeros_like(r * t * th * ph)
        return [[-(a**2) + z, z, z, z], [z, 1 / (1 - r**2 / Rc2) + z, z, z],
                [z, z, r**2 + z, z], [z, z, z, (r * np.sin(th)) ** 2 + z]]
    return g


def interior_schwarzschild_closed(M, Rg, r):
    """rho = M / (4/3 pi R^3); p = rho (cos eta - cos eta_g) / (3 cos eta_g - cos eta),
    cos eta = sqrt(1 - r^2/Rc^2), Rc^2 = R^3/(2M)  (geometric units)."""
    rho = M / (4 * math.pi / 3 * Rg**3)
    Rc2 = Rg**3 / (2 * M)
    ce, cg = math.sqrt(1 - r**2 / Rc2), math.sqrt(1 - Rg**2 / Rc2)
    return rho, rho * (ce - cg) / (3 * cg - ce)


# ----- self-test --------------------------------------------------------------------------------
def selftest(verbose: bool = True) -> bool:
    results = []

    def check(name, ok, detail=""):
        results.append(bool(ok))
        if verbose:
            print(f"{'PASS' if ok else 'FAIL'}  {name}{('  ' + detail) if detail else ''}")

    # 1. Schwarzschild is vacuum. Wikipedia "Schwarzschild metric" (fetch_text, 2026-10-01):
    #    "According to Birkhoff's theorem, the Schwarzschild metric is the most general spherically
    #    symmetric vacuum solution of the Einstein field equations."
    M = 1.0

    def schw(t, r, th, ph):
        f = 1 - 2 * M / r
        z = np.zeros_like(r * t * th * ph)
        return [[-f + z, z, z, z], [z, 1 / f + z, z, z], [z, z, r**2 + z, z], [z, z, z, (r * np.sin(th)) ** 2 + z]]
    st = NumericSpacetime(schw, h=[1e-2, 1e-2, 1e-2, 1e-2])
    pts = np.array([[0.0, 3.0, 1.0, 0.5], [2.0, 5.5, 0.7, 2.0], [0.0, 10.0, 1.4, -1.0]])
    c = st.curvature(pts)
    worst = float(np.max(np.abs(c["einstein"])))
    check("Schwarzschild (t,r,th,ph): G_ab = 0", worst < 1e-8, f"max|G_ab| = {worst:.1e} 1/m^2 (M = 1 m)")
    #    Same vacuum in Painleve-Gullstrand Cartesian form (a coordinate change of the above, so
    #    still vacuum): N = 1, flat slices, shift beta^i = sqrt(2M/r) x^i / r -- a warp-like
    #    ADM metric with off-diagonal g_0i that exercises the mixed t-x derivatives.

    def pg(t, x, y, z):
        r = np.sqrt(x * x + y * y + z * z)
        s = np.sqrt(2 * M / r) / r
        b = [s * x, s * y, s * z]
        one, zero = np.ones_like(r), np.zeros_like(r)
        return [[-1 + b[0] ** 2 + b[1] ** 2 + b[2] ** 2, b[0], b[1], b[2]],
                [b[0], one, zero, zero], [b[1], zero, one, zero], [b[2], zero, zero, one]]
    st_pg = NumericSpacetime(pg, h=1e-2)
    pts_pg = np.array([[0.0, 3.0, 1.0, 0.5], [1.0, -2.0, 2.5, 1.5], [0.0, 0.5, -0.4, 4.0]])
    ec = st_pg.scan_energy_conditions(pts_pg)
    worst = float(np.max(np.abs(st_pg.curvature(pts_pg)["einstein"])))
    check("Painleve-Gullstrand Schwarzschild: G_ab = 0 and every point classed vacuum",
          worst < 1e-8 and ec["types"] == {"vacuum (within FD error)": 3}, f"max|G_ab| = {worst:.1e}")

    # 2. Riemann: Wikipedia "Kretschmann scalar" (fetch_text): "For a Schwarzschild black hole of
    #    mass M, the Kretschmann scalar is K = 48 G^2 M^2 / (c^4 r^6)."
    k = st.kretschmann(pts[:1])[0]
    check("Schwarzschild Kretschmann = 48 M^2/r^6 at r = 3M", abs(k / (48 / 3**6) - 1) < 1e-8,
          f"{k:.10f} vs {48 / 3**6:.10f} 1/m^4")
    #    Limit to Newton: static observer tidal tensor in Schwarzschild is exactly the Newtonian
    #    tidal tensor of a point mass, E = diag(-2M/r^3, M/r^3, M/r^3) (radial stretch 2GM/r^3).
    st_obs = lambda t, r, th, ph: [1 / np.sqrt(1 - 2 * M / r), 0 * r, 0 * r, 0 * r]  # noqa: E731
    E = st.tidal_tensor(pts[1:2], observer=st_obs)[0]
    want = np.diag([-2 * M / 5.5**3, M / 5.5**3, M / 5.5**3])
    check("Schwarzschild static tidal tensor = Newtonian diag(-2M/r^3, M/r^3, M/r^3)",
          np.max(np.abs(E - want)) < 1e-9, f"E_rr = {E[0, 0]:.6e} vs {want[0, 0]:.6e} 1/m^2")

    # 3. Flat FRW dust, a = (t/t0)^(2/3). Wikipedia "Friedmann equations" (fetch_text): "rho_c = 3H^2/
    #    (8 pi G) ... A universe at the critical density is spatially flat (k = 0)"; "Setting the
    #    pressure of the perfect fluid in the Friedmann equations to zero (p = 0) gives a
    #    cosmological dust model". For a ~ t^(2/3), H = 2/(3t), so rho = 1/(6 pi t^2), p = 0.
    t0 = 7.0

    def frw(t, x, y, z):
        a2 = (t / t0) ** (4.0 / 3.0)
        zz = np.zeros_like(t * x * y * z)
        return [[-1 + zz, zz, zz, zz], [zz, a2 + zz, zz, zz], [zz, zz, a2 + zz, zz], [zz, zz, zz, a2 + zz]]
    st_f = NumericSpacetime(frw, h=1e-2)
    pf = np.array([[2.0, 0.3, -1.0, 4.0], [5.0, 10.0, 2.0, -3.0]])
    rho = st_f.eulerian_density(pf)["rho"]
    want = 3 * (2 / (3 * pf[:, 0])) ** 2 / (8 * math.pi)
    ecs = st_f.energy_conditions(pf)
    pmax = max(max(abs(q) for q in r["pressures"]) for r in ecs)
    ok = (np.max(np.abs(rho / want - 1)) < 1e-8 and pmax < 1e-8 * want.max()
          and all(r["type"] == "I" and r["nec"] and r["wec"] and r["sec"] and r["dec"] for r in ecs))
    check("Flat FRW dust: rho = 3H^2/8pi, p = 0, type I, all ECs hold", ok,
          f"rho/rho_ref - 1 = {np.max(np.abs(rho / want - 1)):.1e}")
    #    Any observer: dust seen by an observer with Lorentz factor gamma relative to the comoving
    #    flow has rho_u = gamma^2 rho (T_ab = rho U_a U_b, -U.u = gamma). Take u = (gamma, gamma beta/a, 0, 0).
    beta = 0.6
    gam_f = 1 / math.sqrt(1 - beta**2)
    obs = lambda t, x, y, z: [gam_f + 0 * t, gam_f * beta / (t / t0) ** (2 / 3), 0 * t, 0 * t]  # noqa: E731
    rho_u = st_f.energy_density(pf, observer=obs)["rho"]
    check("FRW dust, boosted observer: rho_u = gamma^2 rho (beta = 0.6)",
          np.max(np.abs(rho_u / (gam_f**2 * want) - 1)) < 1e-8, f"{rho_u[0]:.8e} vs {gam_f**2 * want[0]:.8e}")
    #    de Sitter, a = exp(H t): rho = 3H^2/8pi with p = -rho; NEC/WEC/DEC hold (marginally,
    #    rho + p = 0 exactly) and SEC fails (rho + 3p = -2 rho < 0). Tests the noise floor.
    Hds = 0.2

    def ds(t, x, y, z):
        a2 = np.exp(2 * Hds * t)
        zz = np.zeros_like(t * x * y * z)
        return [[-1 + zz, zz, zz, zz], [zz, a2 + zz, zz, zz], [zz, zz, a2 + zz, zz], [zz, zz, zz, a2 + zz]]
    r = NumericSpacetime(ds, h=1e-2).energy_conditions([1.0, 0.5, 0.2, -0.3])
    ok = (abs(r["rho_eulerian"] / (3 * Hds**2 / (8 * math.pi)) - 1) < 1e-8 and r["nec"] and r["wec"]
          and r["dec"] and not r["sec"])
    check("de Sitter: rho = 3H^2/8pi; NEC, WEC, DEC hold, SEC fails", ok, f"type {r['type']}")

    # 4. Alcubierre. arXiv:gr-qc/0009013 eq. (19) (fetch_text): "T^{ab} n_a n_b = alpha^2 T^00 =
    #    (1/8pi) G^00 = -(1/8pi) v_s^2 rho^2/(4 r_s^2) (df/dr_s)^2", rho^2 = y^2 + z^2; and "The fact
    #    that this expression is everywhere negative implies that the weak and dominant energy
    #    conditions are violated."
    v, Rb, sig = 1.5, 1.0, 8.0
    st_a = NumericSpacetime(alcubierre_metric(v, Rb, sig), h=2e-3)
    pa = np.array([[0.0, 0.3, 0.9, 0.2], [0.0, -0.5, 0.6, -0.55], [0.4, 0.7, 0.1, 0.95], [0.0, 0.05, 1.1, 0.0]])
    d = st_a.eulerian_density(pa)
    want = alcubierre_rho_closed(v, Rb, sig, *pa.T)
    rel = float(np.max(np.abs(d["rho"] / want - 1)))
    check("Alcubierre tanh wall: Eulerian rho matches eq. (19)", rel < 1e-6, f"max rel err {rel:.1e}")
    #    convergence order: error of the h-result vs the h/2-result should shrink ~16x per halving
    e1 = np.abs(NumericSpacetime(alcubierre_metric(v, Rb, sig), h=8e-3).eulerian_density(pa, halving=False)["rho"] - want)
    e2 = np.abs(NumericSpacetime(alcubierre_metric(v, Rb, sig), h=4e-3).eulerian_density(pa, halving=False)["rho"] - want)
    order = float(np.log2(np.median(e1 / e2)))
    check("Finite differences converge at 4th order (Alcubierre wall)", 3.5 < order < 4.5, f"order {order:.2f}")
    sc = st_a.scan_energy_conditions(pa)
    check("Alcubierre wall: robust NEC and WEC violations at every wall point",
          sc["violations"]["nec"] == 4 and sc["violations"]["wec"] == 4, str(sc["types"]))
    #    Slice integral: integrating eq. (19) over angles (<(y^2+z^2)/r^2> = 2/3) gives
    #    E = -(v^2/12) int f'^2 r^2 dr; for f = exp(-r^2) that is -v^2 sqrt(pi)/(32 sqrt 2).
    def gauss(t, x, y, z):
        b = -np.exp(-(x * x + y * y + z * z))
        one, zero = np.ones_like(b), np.zeros_like(b)
        return [[-1 + b * b, b, zero, zero], [b, one, zero, zero], [zero, zero, one, zero], [zero, zero, zero, one]]
    parts = NumericSpacetime(gauss, h=1e-2).integrate_parts(0.0, [(-4.5, 4.5)] * 3, n=40)
    ref = -math.sqrt(math.pi) / (32 * math.sqrt(2))
    # E+ is exactly 0 analytically, but on the y = z = 0 axis (and far out) rho_E = 0 and the
    # finite-difference round-off there (~1e-12 1/m^2) has either sign, so E+ is only tiny,
    # not 0. The check therefore asks E+ < 1e-6 |E-| rather than E+ == 0.
    check("Gaussian Alcubierre slice energy = -sqrt(pi)/(32 sqrt 2) m (v = 1), E+ ~ 0",
          abs(parts["total"] / ref - 1) < 0.01 and parts["positive"] < 1e-6 * abs(parts["negative"]),
          f"{parts['total']:.6f} vs {ref:.6f} m; E+ = {parts['positive']:.1e} m")

    # 5. Interior Schwarzschild star. Wikipedia "Interior Schwarzschild metric" (fetch_text): line
    #    element "-1/4 (3 sqrt(1 - r_g^2/R^2) - sqrt(1 - r^2/R^2))^2 c^2 dt^2 + (1 - r^2/R^2)^-1 dr^2
    #    + r^2 dOmega^2" with "R^2 = r_g^3/r_s"; "rho = M/(4pi/3 r_g^3)"; "The Einstein tensor is
    #    diagonal ... pressure is isotropic. Its value is p = rho c^2 (cos eta - cos eta_g)/(3 cos
    #    eta_g - cos eta)" (cos eta = sqrt(1 - r^2/R^2) as in the metric).
    Ms, Rs = 1.0, 4.0
    st_s = NumericSpacetime(interior_schwarzschild_metric(Ms, Rs), h=1e-2)
    worst = 0.0
    for rr in (0.5, 2.0, 3.5):
        rep = st_s.energy_conditions([0.0, rr, 1.1, 0.4])
        rho_w, p_w = interior_schwarzschild_closed(Ms, Rs, rr)
        ok_t = rep["type"] == "I" and all((rep["nec"], rep["wec"], rep["sec"], rep["dec"]))
        dev = max(abs(rep["rho_rest"] / rho_w - 1), *[abs(q - p_w) / rho_w for q in rep["pressures"]])
        worst = max(worst, dev if ok_t else math.inf)
    check("Interior Schwarzschild (2M/R = 0.5): rho const, isotropic p, type I, all ECs hold",
          worst < 1e-7, f"max rel dev {worst:.1e}")

    # 6. Agreement with the symbolic gr_tensors on a generic time-dependent ADM metric
    #    (lapse, shift and spatial metric all varying): every T_ab component and the EC verdicts.
    import sympy as sp
    from gr_tensors import Spacetime
    T_, X_, Y_, Z_ = sp.symbols("t x y z", real=True)
    r2 = (X_ - sp.Rational(1, 2) * T_) ** 2 + Y_**2 + Z_**2
    lapse = 1 + sp.Rational(1, 5) * sp.exp(-r2)
    shift = [-sp.Rational(3, 2) * sp.exp(-r2), sp.Rational(1, 10) * Y_ * sp.exp(-r2), 0]
    hmat = sp.diag(1 + sp.Rational(3, 10) * sp.exp(-r2), 1, 1 + sp.Rational(1, 10) * X_ * sp.exp(-r2))
    sym = Spacetime.from_adm(lapse, shift, hmat, [T_, X_, Y_, Z_])
    gnum = sp.lambdify([T_, X_, Y_, Z_], sym.g.tolist(), "numpy")   # nested list of entries
    pts6 = np.array([[0.0, 0.4, 0.3, -0.2], [0.3, -0.6, 0.5, 0.4], [0.1, 1.0, -0.2, 0.7]])
    Tsym = np.array([np.array(sym.compile(sym.stress_energy())(*q), dtype=float) for q in pts6])
    Tnum = NumericSpacetime(gnum, h=5e-3).stress_energy(pts6)["T"]
    dev = float(np.max(np.abs(Tnum - Tsym)) / np.max(np.abs(Tsym)))
    agree = True
    for q in pts6:
        a = sym.energy_conditions(tuple(q))
        b = NumericSpacetime(gnum, h=5e-3).energy_conditions(q)
        agree &= a["type"] == b["type"] and all(a[k] == b[k] for k in ("nec", "wec", "sec", "dec"))
        agree &= abs(a["rho_observer"] - b["rho_observer"]) < 1e-7 * max(1.0, abs(a["rho_observer"]))
    check("Matches gr_tensors (symbolic) on a generic ADM metric: T_ab, types, EC verdicts",
          dev < 1e-7 and agree, f"max rel dev {dev:.1e}")
    #    ... and on gr_tensors' own Alcubierre top-hat at the brief's reference case (v = 10 c,
    #    R = 100 m, sigma = 1/m), inside (type IV) and outside (type I) the wall centre.
    from gr_tensors import metrics as _m
    sa, ss = _m.alcubierre()
    top = {ss["f"]: _m.alcubierre_top_hat(ss)}
    par = {ss["v"]: 10.0, ss["R"]: 100.0, ss["sigma"]: 1.0}
    st_ref = NumericSpacetime(alcubierre_metric(10.0, 100.0, 1.0), h=1e-2)
    agree, kinds = True, []
    for rr in (98.0, 99.5, 101.0, 102.0):
        q = (0.0, rr / math.sqrt(2), rr / math.sqrt(2), 0.0)
        a = sa.energy_conditions(q, par, top)
        b = st_ref.energy_conditions(np.array(q))
        kinds.append(b["type"])
        agree &= a["type"] == b["type"] and all(a[k] == b[k] for k in ("nec", "wec", "sec", "dec"))
        agree &= abs(a["rho_observer"] / b["rho_observer"] - 1) < 1e-7
    check("Matches gr_tensors on Alcubierre v = 10, R = 100 m, sigma = 1/m (types, ECs, rho_E)",
          agree, str(kinds))

    # 7. Input validation
    try:
        NumericSpacetime(schw, h=0.0)
        bad = False
    except ValueError:
        bad = True
    check("Refuses a non-positive step (ValueError)", bad)

    ok = all(results)
    if verbose:
        print(f"\n{sum(results)}/{len(results)} checks passed")
    return ok


# ----- command line ------------------------------------------------------------------------------
def _q(text, unit):
    from unit_tools import Q
    return Q(text).to(unit) if isinstance(text, str) and not _isnum(text) else float(text)


def _isnum(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def _fmt(r):
    keys = ("type", "nec", "wec", "sec", "dec", "marginal", "rho_eulerian", "rho_observer", "rho_rest",
            "pressures", "nec_min", "err", "converged")
    return {k: r[k] for k in keys}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("selftest")
    a = sub.add_parser("alcubierre", help="scan an Alcubierre tanh bubble across its wall")
    a.add_argument("--v", type=float, default=10.0, help="bubble speed in units of c")
    a.add_argument("--R", default="100 m")
    a.add_argument("--sigma", default="1 1/m", help="wall steepness (1/length)")
    a.add_argument("--n", type=int, default=9, help="points along the wall at 45 degrees")
    s = sub.add_parser("star", help="constant-density star at one radius")
    s.add_argument("--M", default="1 Msun")
    s.add_argument("--R", default="10 km")
    s.add_argument("--r", default="5 km")
    p = sub.add_parser("point", help="energy conditions of a user metric file:function")
    p.add_argument("--metric", required=True, help="path.py:function returning 4x4 g_ab(t,x,y,z)")
    p.add_argument("--h", type=float, required=True, help="finite-difference step (coordinate units)")
    p.add_argument("--at", type=float, nargs=4, required=True)
    args = ap.parse_args(argv)
    if args.cmd == "selftest":
        return 0 if selftest() else 1
    if args.cmd == "alcubierre":
        R, sig = _q(args.R, "m"), _q(args.sigma, "1/m")
        st = NumericSpacetime(alcubierre_metric(args.v, R, sig), h=1e-2 / sig)
        rr = R + np.linspace(-3, 3, args.n) / sig
        pts = np.stack([0 * rr, rr / math.sqrt(2), rr / math.sqrt(2), 0 * rr], axis=1)
        print(f"Alcubierre v = {args.v} c, R = {R} m, sigma = {sig} 1/m; points at 45 deg in x-y plane")
        for q, r in zip(pts, st.energy_conditions(pts)):
            ref = alcubierre_rho_closed(args.v, R, sig, *q)
            print(f"r_s = {math.hypot(q[1], q[2]):9.4f} m  rho_E = {r['rho_eulerian']: .4e} 1/m^2 "
                  f"({to_si.energy_density_j_per_m3(r['rho_eulerian']): .3e} J/m^3; eq.19 {ref: .4e})  "
                  f"type {r['type']:<14} NEC {r['nec']} WEC {r['wec']} SEC {r['sec']} DEC {r['dec']}")
        print(st.scan_energy_conditions(pts)["violations"])
        return 0
    if args.cmd == "star":
        from unit_tools import Q
        Mg = Q(f"G*({args.M})/c^2").to("m")
        R, r = _q(args.R, "m"), _q(args.r, "m")
        if not 0 < r < R:
            raise ValueError("need 0 < r < R")
        st = NumericSpacetime(interior_schwarzschild_metric(Mg, R), h=[1e-3 * R, 1e-3 * R, 1e-3, 1e-3])  # angles in rad
        rep = st.energy_conditions([0.0, r, 1.0, 0.0])
        rho_w, p_w = interior_schwarzschild_closed(Mg, R, r)
        print(f"M = {Mg:.4f} m (geometric), R = {R} m, r = {r} m, 2M/R = {2 * Mg / R:.4f}")
        print(f"rho = {rep['rho_rest']:.6e} 1/m^2 = {to_si.energy_density_j_per_m3(rep['rho_rest']):.4e} J/m^3"
              f" (closed form {rho_w:.6e}); p = {rep['pressures'][0]:.6e} 1/m^2 = "
              f"{to_si.energy_density_j_per_m3(rep['pressures'][0]):.4e} Pa (closed form {p_w:.6e})")
        print(_fmt(rep))
        return 0
    if args.cmd == "point":
        path, func = args.metric.rsplit(":", 1)
        spec = importlib.util.spec_from_file_location("user_metric", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        print(_fmt(NumericSpacetime(getattr(mod, func), h=args.h).energy_conditions(args.at)))
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
