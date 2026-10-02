#!/usr/bin/env python3
"""Constraints lens: exact speed scaling of the Eulerian-frame stress tensor for unit-lapse,
flat-slice drives that translate rigidly, X(t, x) = v chi(x, y, z - v t).

In the Eulerian orthonormal frame (n, d_x, d_y, d_z) the ADM equations with N = 1, h = delta,
K_ij ~ v, d_t = -v d_zeta give rho ~ v^2, S_ij ~ v^2 and J_i ~ v, so
     T_frame(v) = v^2 A + v B      (A: rho and S blocks;  B: J block)   exactly.
We get A and B from finite-difference frames at v = 1 and v = 1/2 (where the FD tool converges),
verify the decomposition by predicting v = 2 and comparing with a direct FD frame, then build
T_frame(10) = 100 A + 10 B and classify it EXACTLY with gr_tensors.classify_stress_energy
(type I: rest-frame rho and principal pressures; otherwise sampled boosts to 0.99c and 64 null
directions). Geometric units, 1/m^2. Also prints the speed v_* above which the Eulerian
NEC combination along the worst null direction is dominated by the v^2 part.
"""
import importlib.util
import sys

import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from numeric_stress_energy import NumericSpacetime, _orthonormal_frame  # noqa: E402
from gr_tensors import classify_stress_energy  # noqa: E402

spec = importlib.util.spec_from_file_location(
    "ni", "runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-constraints_natario_irrot.py")
ni = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ni)


def frames(kind, v, R, s, pts, hfac):
    st = NumericSpacetime(ni.metric_factory(kind, v, R, s), h=hfac / s)
    se = st.stress_energy(pts, halving=True)
    out, errs = [], []
    for i in range(len(pts)):
        gi = se["ginv"][i]
        N = 1.0 / np.sqrt(-gi[0, 0])
        n = -N * gi[0]
        e = _orthonormal_frame(se["g"][i], n)
        tf = e @ se["T"][i] @ e.T
        out.append(0.5 * (tf + tf.T))
        errs.append(float(np.max(np.abs(e) @ se["T_err"][i] @ np.abs(e).T)))
    return np.array(out), np.array(errs)


def census(Tf):
    c = {"nec": 0, "wec": 0, "sec": 0, "dec": 0}
    types = {}
    worst = np.inf
    rho_e_neg = 0
    for T in Tf:
        m = np.max(np.abs(T))
        if m == 0:
            continue
        r = classify_stress_energy(T / m)
        types[r["type"]] = types.get(r["type"], 0) + 1
        for k in c:
            c[k] += 0 if r[k] else 1
        worst = min(worst, r["nec_min"] * m)
        rho_e_neg += 1 if T[0, 0] < 0 else 0
    return c, types, worst, rho_e_neg


for kind in ("NAT", "IRR"):
    for (R, s, lab) in ((1.0, 8.0, "paper-like R = 1 m, Delta = 0.25 m"), (100.0, 2.0, "reference R = 100 m, Delta = 1 m")):
        pts = ni.wall_points(R, s)
        hfac = 0.01
        T1, e1 = frames(kind, 1.0, R, s, pts, hfac)
        T05, e05 = frames(kind, 0.5, R, s, pts, hfac)
        A = 2 * (T1 - 2 * T05)
        B = T1 - A
        # check: B should live only in the T_0i block, A in T_00 and T_ij
        mA = np.max(np.abs(A))
        leakA = np.max(np.abs(A[:, 0, 1:])) / mA
        leakB = max(np.max(np.abs(B[:, 0, 0])), np.max(np.abs(B[:, 1:, 1:]))) / max(np.max(np.abs(B)), 1e-300)
        T2, e2 = frames(kind, 2.0, R, s, pts, hfac)
        pred2 = 4 * A + 2 * B
        scale2 = np.max(np.abs(T2), axis=(1, 2))
        rel2 = np.max(np.abs(pred2 - T2), axis=(1, 2)) / np.maximum(scale2, 1e-300)
        print(f"{kind} {lab}: max FD err/|T| at v=1: {np.max(e1/np.maximum(np.max(np.abs(T1),axis=(1,2)),1e-300)):.2e};"
              f" A leak into T_0i {leakA:.2e}; B leak into rho,S {leakB:.2e}; v=2 prediction vs direct FD: median rel diff"
              f" {np.median(rel2):.2e}, 95th pct {np.percentile(rel2,95):.2e}")
        for vv in (0.1, 0.5, 1.0, 2.0, 10.0):
            Tv = vv * vv * A + vv * B
            c, types, worst, nneg = census(Tv)
            print(f"   v = {vv:5.1f}: violations {c} of {len(pts)}; types {types}; worst NEC (sampled) {worst:.4e} 1/m^2;"
                  f" Eulerian rho < 0 at {nneg}")
