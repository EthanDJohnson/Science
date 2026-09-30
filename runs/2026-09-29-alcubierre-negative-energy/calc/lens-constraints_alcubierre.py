"""Constraints lens: Alcubierre drive audit (geometric units G = c = 1, lengths in metres; SI where stated).

Computes, with .claude/skills/conundrum/scripts/gr_tensors.py:
 1. total Eulerian energy: 3D slice integral (toolkit) vs 1D formula E = -(v^2/12) int f'^2 r^2 dr, with n vs 1.5n
 2. reference case R = 100 m, v = 10c, Delta = 1 m (Pfenning-Ford convention) in kg and M_sun
 3. NEC/WEC/SEC/DEC + Hawking-Ellis type scan over the whole wall region at v = 0.1, 1, 10
 4. peak Eulerian density and curvature radius at the wall -> Ford-Roman QI limit on Delta (alpha = tau0/r_c)
 5. Lorentzian average of rho along an Eulerian geodesic crossing the wall (checks <rho> ~ rho_peak)
"""
import math
import sys
import time

import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from gr_tensors import Spacetime, metrics, qi, to_si, PLANCK_LENGTH  # noqa: E402

MSUN, MJ = 1.989e30, 1.898e27
T0 = time.time()
st, s = metrics.alcubierre()
top = metrics.alcubierre_top_hat(s)
v_, R_, sg_ = s["v"], s["R"], s["sigma"]


def f_np(r, R, sig):
    return (np.tanh(sig * (r + R)) - np.tanh(sig * (r - R))) / (2 * np.tanh(sig * R))


def fp_np(r, R, sig):
    return sig * (1 / np.cosh(sig * (r + R)) ** 2 - 1 / np.cosh(sig * (r - R)) ** 2) / (2 * np.tanh(sig * R))


def e1d(v, R, sig, npts=400001):
    """E = -(v^2/12) int_0^inf f'^2 r^2 dr (geometric, metres). Grid concentrated at the wall."""
    w = 40.0 / sig
    r = np.linspace(max(0.0, R - w), R + w, npts)
    y = fp_np(r, R, sig) ** 2 * r**2
    return -(v**2 / 12) * np.trapezoid(y, r)


def delta_pf(R, sig):
    t = math.tanh(sig * R)
    return (1 + t**2) ** 2 / (2 * sig * t)


def sigma_for_delta(R, D):
    lo, hi = 1e-6, 1e40
    for _ in range(300):
        mid = math.sqrt(lo * hi)
        if delta_pf(R, mid) > D:
            lo = mid
        else:
            hi = mid
    return math.sqrt(lo * hi)


print("=== 1. 3D toolkit integral vs 1D formula (R = 1 m, sigma = 8 /m, v = 1) ===")
rho = st.energy_density()
p = {v_: 1.0, R_: 1.0, sg_: 8.0}
for n in (64, 96):
    parts = st.integrate_parts(rho, t=0.0, bounds=[(-1.8, 1.8)] * 3, n=n, params=p, functions={s["f"]: top})
    print(f"n={n:3d}: total {parts['total']:.5f} m, negative {parts['negative']:.5f} m, positive {parts['positive']:.2e} m")
print(f"1D formula: {e1d(1.0, 1.0, 8.0):.5f} m ; tanh thin-wall approx -v^2 R^2 sigma/36 = {-8/36:.5f} m")

print("\n=== 2. Reference case (PF wall convention) ===")
for R, D, v in ((100.0, 1.0, 1.0), (100.0, 1.0, 10.0)):
    sig = sigma_for_delta(R, D)
    E = e1d(v, R, sig)
    E2 = e1d(v, R, sig, npts=600001)
    kg = to_si.mass_kg(E)
    print(f"R={R} m Delta_PF={D} m sigma={sig:.4f}/m v={v}c: E = {E:.5e} m (1.5n: {E2:.5e}) = {kg:.3e} kg = {kg/MSUN:.2f} Msun = {kg/MJ:.0f} MJ ; closed form -v^2R^2/(18D) = {-(v**2)*R**2/(18*D):.4e} m")

print("\n=== 3. Energy-condition scan over the wall (scale-free: R = 1, sigma = 8) ===")
pts = []
for xx in np.linspace(-1.6, 1.6, 17):
    for yy in np.linspace(0.05, 1.6, 12):
        r = math.hypot(xx, yy)
        if 0.55 < r < 1.45:  # wall region, |f'| > ~1e-3 sigma
            pts.append((0.0, xx, yy, 0.0))
for xx, yy, zz in ((0.3, 0.6, 0.6), (-0.4, 0.5, 0.7), (0.9, 0.2, 0.3), (-0.95, 0.1, 0.2)):
    pts.append((0.0, xx, yy, zz))
print(f"{len(pts)} points; stress_energy build ...", flush=True)
for v in (0.1, 1.0, 10.0):
    sc = st.scan_energy_conditions(pts, {v_: v, R_: 1.0, sg_: 8.0}, {s["f"]: top})
    types = {}
    fields = st._numeric_fields({v_: v, R_: 1.0, sg_: 8.0}, {s["f"]: top}, None)
    rho_min = 0.0
    for q in pts:
        rr = st._conditions_at(fields, q)
        types[rr["type"]] = types.get(rr["type"], 0) + 1
        rho_min = min(rho_min, rr["rho_observer"])
    print(f"v={v}: points {sc['points']} skipped {sc['skipped']} violations {sc['violations']} types {types} "
          f"min Eulerian rho {rho_min:.3e} /m^2 ; worst NEC {sc['worst']['nec_min'][0]:.3e}")
print(f"  [{time.time()-T0:.0f}s]")

print("\n=== 4. Peak density, curvature radius, QI wall limit ===")
rho_c = st.compile(rho, {R_: 1.0, sg_: 8.0}, {s["f"]: top}, free=[v_])
for v in (1.0, 10.0):
    for sig in (8.0, 32.0):
        # equatorial plane point at the steepest part of the wall (x = 0, y = R)
        rr = np.linspace(0.8, 1.2, 4001)
        vals = np.array([rho_c(0.0, 0.0, y, 0.0, v) for y in rr]) if sig == 8.0 else None
        pk_r = 1.0
        rho_pk = -(v**2) / (32 * math.pi) * fp_np(pk_r, 1.0, sig) ** 2
        cur = st.curvature_at((0.0, 0.0, pk_r, 0.0), {v_: v, R_: 1.0, sg_: sig}, {s["f"]: top})
        # also a point on the axis (front wall)
        cur_ax = st.curvature_at((0.0, 1.0, 1e-6, 0.0), {v_: v, R_: 1.0, sg_: sig}, {s["f"]: top})
        D = delta_pf(1.0, sig)
        rc = min(cur["curvature_radius"], cur_ax["curvature_radius"])
        a_coef = abs(rho_pk) * D**2 / v**2
        b_coef = rc * v / D
        msg = f"v={v} sigma={sig}: Delta_PF={D:.4f} rho_peak={rho_pk:.4e} (=-{a_coef:.5f} v^2/Delta^2) r_c(eq)={cur['curvature_radius']:.4e} r_c(axis)={cur_ax['curvature_radius']:.4e} -> r_c = {b_coef:.3f} Delta/v"
        if vals is not None:
            msg += f" ; grid min rho on equator {vals.min():.4e}"
        print(msg)
# QI: |rho_pk| <= 3 lP^2/(32 pi^2 (alpha r_c)^4), rho_pk = a v^2/Delta^2, r_c = b Delta/v  =>  Delta <= v lP sqrt(3/(32 pi^2 a)) /(alpha^2 b^2)
a_coef = 1 / (32 * math.pi) / 1.0  # thin-wall tanh: rho_pk = v^2 sigma^2/(128 pi) = v^2/(32 pi Delta^2)
for v in (1.0, 10.0):
    sig = 32.0
    cur = st.curvature_at((0.0, 0.0, 1.0, 0.0), {v_: v, R_: 1.0, sg_: sig}, {s["f"]: top})
    cur_ax = st.curvature_at((0.0, 1.0, 1e-6, 0.0), {v_: v, R_: 1.0, sg_: sig}, {s["f"]: top})
    b = min(cur["curvature_radius"], cur_ax["curvature_radius"]) * v / delta_pf(1.0, sig)
    for alpha in (0.1, 0.01):
        Dmax = v * PLANCK_LENGTH * math.sqrt(3 / (32 * math.pi**2 * a_coef)) / (alpha**2 * b**2)
        sigq = 2 / Dmax
        E = -(v**2) * 100.0**2 * sigq / 36
        kg = to_si.mass_kg(E)
        print(f"QI (alpha={alpha}) v={v}c: b={b:.3f} -> Delta_max = {Dmax:.3e} m = {Dmax/PLANCK_LENGTH:.1f} L_P = {Dmax/PLANCK_LENGTH/v:.1f} v L_P ; "
              f"E(R=100 m) = {kg:.3e} kg = {kg/MSUN:.3e} Msun")

print("\n=== 5. Lorentzian average along an Eulerian geodesic through the wall (R=1, sigma=32, v=10) ===")
v, sig = 10.0, 32.0
rho_c2 = st.compile(rho, {R_: 1.0, sg_: sig}, {s["f"]: top}, free=[v_])
y0 = 1.0
xs, ts = -3.0, np.linspace(-1.0, 1.0, 400001)
# Eulerian worldline: dx/dt = v f(r_s), proper time = t (lapse 1). Start ahead of the bubble at t = -1: x = x0 + ...
x = np.empty_like(ts)
x[0] = 0.0 + 0.0  # observer initially at x = 0? bubble centre at v t = -10, far behind
for i in range(1, len(ts)):
    dt = ts[i] - ts[i - 1]
    rs = math.hypot(x[i - 1] - v * ts[i - 1], y0)
    k1 = v * f_np(rs, 1.0, sig)
    rs2 = math.hypot(x[i - 1] + 0.5 * dt * k1 - v * (ts[i - 1] + 0.5 * dt), y0)
    k2 = v * f_np(rs2, 1.0, sig)
    x[i] = x[i - 1] + dt * k2
rho_path = np.array([rho_c2(t, xx, y0, 0.0, v) for t, xx in zip(ts, x)])
imin = int(np.argmin(rho_path))
t_pk = ts[imin]
from numpy import interp  # noqa: E402
cur = st.curvature_at((0.0, 0.0, 1.0, 0.0), {v_: v, R_: 1.0, sg_: sig}, {s["f"]: top})
rc = cur["curvature_radius"]
for alpha in (1.0, 0.1, 0.01):
    tau0 = alpha * rc
    avg = qi.lorentzian_average(lambda tau: interp(t_pk + tau, ts, rho_path, left=0.0, right=0.0), tau0, n=200001)
    bound = qi.ford_roman_geometric(tau0)
    print(f"tau0 = {alpha} r_c = {tau0:.3e} m: <rho> = {avg:.4e} /m^2 (peak {rho_path[imin]:.4e}); ratio {avg/rho_path[imin]:.3f}; FR bound {bound:.3e} /m^2")
print(f"observer x-displacement {x[-1]-x[0]:.3f} m (dragged by the bubble); done in {time.time()-T0:.0f}s")
