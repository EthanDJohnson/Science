#!/usr/bin/env python3
"""Constraints lens: unit-lapse, flat-slice warp drives (Natario class) from the metric.

Metrics (geometric units G = c = 1, lengths in m; from_adm convention
ds^2 = -N^2 dt^2 + h_ij (dx^i + b^i dt)(dx^j + b^j dt), so b = -X in Natario's notation):
  ALC  Alcubierre 1994: b = (-v f(r_s), 0, 0), bubble moving along +x.
  NAT  Natario 2002 zero-expansion: X = curl( n(r) zhat x r ) with n = f/2, which gives
       X = (2n + r n') zhat - n' z rvec / r  -> X = v zhat inside (n = 1/2), 0 outside; div X = 0.
  IRR  zero-vorticity (Lentz / Fell-Heisenberg / Rodal class): X = grad( v zeta f(r) ),
       zeta = z - v t, so X = v zhat inside, 0 outside; curl X = 0.
f = Alcubierre tanh top hat, wall convention Delta = 2/sigma (dossier D-28).
Outputs: Eulerian density, all-observer NEC/WEC/SEC/DEC with Hawking-Ellis type over the
whole wall (axisymmetric (r, theta) grid in a meridian plane, plus off-plane points), and
the Eulerian slice energy E = int rho dV split into E-, E+ by 2D axisymmetric quadrature,
with a grid-convergence check (n vs 1.5 n).
"""
import math
import sys
import time

import numpy as np
import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from gr_tensors import Spacetime, metrics, to_si  # noqa: E402

MSUN, MJ = 1.989e30, 1.898e27

t, x, y, z = sp.symbols("t x y z", real=True)
v, R, sig = sp.symbols("v R sigma", positive=True)
r_ = sp.symbols("r", positive=True)
f = sp.Function("f")
TOP = sp.Lambda(r_, (sp.tanh(sig * (r_ + R)) - sp.tanh(sig * (r_ - R))) / (2 * sp.tanh(sig * R)))


def build(kind):
    if kind == "ALC":
        rs = sp.sqrt((x - v * t) ** 2 + y ** 2 + z ** 2)
        st = Spacetime.from_adm(1, [-v * f(rs), 0, 0], sp.eye(3), [t, x, y, z])
        axis = "x"
    else:
        zeta = z - v * t
        rs = sp.sqrt(x ** 2 + y ** 2 + zeta ** 2)
        if kind == "NAT":
            n = f(rs) / 2
            # X = curl(n(r) * (-y, x, 0)), computed symbolically (exactly divergence-free)
            A = [-y * n, x * n, 0]
            X = [sp.diff(A[2], y) - sp.diff(A[1], z),
                 sp.diff(A[0], z) - sp.diff(A[2], x),
                 sp.diff(A[1], x) - sp.diff(A[0], y)]
            X = [v * c for c in X]
        else:  # IRR
            Phi = v * zeta * f(rs)
            X = [sp.diff(Phi, x), sp.diff(Phi, y), sp.diff(Phi, z)]
        st = Spacetime.from_adm(1, [-c for c in X], sp.eye(3), [t, x, y, z])
        axis = "z"
    return st, axis


def meridian_points(axis, Rv, sg, nr=14, nth=13):
    """Points on t = 0 covering the wall r in [R - 3/sig, R + 3/sig] (well past the 1/e width),
    all polar angles measured from the motion axis, in the plane containing the axis, plus a
    rotated copy (azimuth 0.7 rad) to check axisymmetry."""
    rr = np.linspace(Rv - 3.0 / sg, Rv + 3.0 / sg, nr)
    th = np.linspace(0.02, math.pi - 0.02, nth)
    pts = []
    for phi in (0.0, 0.7):
        for a in rr:
            for b in th:
                par = a * math.cos(b)
                perp = a * math.sin(b)
                if axis == "x":
                    pts.append((0.0, par, perp * math.cos(phi), perp * math.sin(phi)))
                else:
                    pts.append((0.0, perp * math.cos(phi), perp * math.sin(phi), par))
    return pts


def slice_energy(st, axis, params, n_r, n_th, Rv, sg):
    """E = 2 pi int int rho r^2 sin(th) dr dth (axisymmetric about the motion axis), midpoint rule."""
    rho_fn = st.compile(st.energy_density(), params, {f: TOP.subs({R: params[R], sig: params[sig]})})
    rmax = Rv + 12.0 / sg
    dr = rmax / n_r
    rr = (np.arange(n_r) + 0.5) * dr
    dth = math.pi / n_th
    th = (np.arange(n_th) + 0.5) * dth
    RR, TT = np.meshgrid(rr, th, indexing="ij")
    par, perp = RR * np.cos(TT), RR * np.sin(TT)
    zero = np.zeros_like(RR)
    if axis == "x":
        vals = rho_fn(zero, par, perp, zero)
    else:
        vals = rho_fn(zero, perp, zero, par)
    vals = np.broadcast_to(np.asarray(vals, dtype=float), RR.shape)
    w = 2 * math.pi * RR ** 2 * np.sin(TT) * dr * dth
    integ = vals * w
    return dict(total=float(integ.sum()), neg=float(integ[integ < 0].sum()), pos=float(integ[integ > 0].sum()),
                rho_min=float(vals.min()), rho_max=float(vals.max()))


def report_energy(label, e, v_c):
    tot = e["total"]
    print(f"  {label}: E_total = {tot:.6e} m (geo) = {to_si.energy_joules(tot):.4e} J = {to_si.mass_kg(tot):.4e} kg"
          f" = {to_si.mass_kg(tot)/MSUN:.4e} Msun; E- = {e['neg']:.6e} m = {to_si.mass_kg(e['neg']):.4e} kg;"
          f" E+ = {e['pos']:.6e} m = {to_si.mass_kg(e['pos']):.4e} kg; rho_min = {e['rho_min']:.4e} 1/m^2,"
          f" rho_max = {e['rho_max']:.4e} 1/m^2")


def main():
    cases = [("paper-like (R = 1 m, sigma = 8 /m, v = 1)", 1.0, 8.0, 1.0),
             ("reference (R = 100 m, Delta = 1 m -> sigma = 2 /m, v = 10)", 100.0, 2.0, 10.0)]
    for kind in ("ALC",):  # NAT and IRR symbolic Einstein tensors exceed 400 s; done numerically in lens-constraints_natario_irrot.py
        t0 = time.time()
        st, axis = build(kind)
        print(f"=== {kind} (motion axis {axis}); build {time.time()-t0:.1f}s")
        for label, Rv, sg, vv in cases:
            params = {v: vv, R: Rv, sig: sg}
            fn = {f: TOP.subs({R: Rv, sig: sg})}
            t1 = time.time()
            pts = meridian_points(axis, Rv, sg)
            sc = st.scan_energy_conditions(pts, params, fn)
            print(f" {label}: EC scan over {sc['points']} wall points (skipped {sc['skipped']}),"
                  f" violations {sc['violations']}; worst sampled minima (1/m^2) "
                  f"nec {sc['worst']['nec_min'][0]:.3e}, wec {sc['worst']['wec_min'][0]:.3e},"
                  f" sec {sc['worst']['sec_min'][0]:.3e}  [{time.time()-t1:.1f}s]")
            # Hawking-Ellis type census and Eulerian sign census
            types, eul_neg, eul_pos = {}, 0, 0
            fields = st._numeric_fields(params, fn, None)
            for p in pts:
                rr = st._conditions_at(fields, p)
                types[rr["type"]] = types.get(rr["type"], 0) + 1
                if rr["rho_observer"] < -1e-14:
                    eul_neg += 1
                elif rr["rho_observer"] > 1e-14:
                    eul_pos += 1
            print(f"   Hawking-Ellis types {types}; Eulerian density <0 at {eul_neg}, >0 at {eul_pos} points")
            # Eulerian slice energy with convergence n vs 1.5 n
            nr = 2000 if Rv > 10 else 300
            e1 = slice_energy(st, axis, params, nr, 120, Rv, sg)
            e2 = slice_energy(st, axis, params, int(1.5 * nr), 180, Rv, sg)
            report_energy(f"n_r={nr},n_th=120", e1, vv)
            report_energy(f"n_r={int(1.5*nr)},n_th=180", e2, vv)
            rel = abs(e2["total"] - e1["total"]) / max(abs(e2["neg"]), 1e-300)
            print(f"   convergence: |dE_total|/|E-| = {rel:.2e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
