#!/usr/bin/env python3
"""Crux C2: is the smoothing tail beyond R2 of the rebuilt Fuchs 2024 shell energy-condition clean?

Answers verdict C2-1 (Le 2605.25417v1/v2: 22 of 25 exterior probes Hawking-Ellis Type IV).
Rebuild: warp_shell.build_shell (M = 4.49e27 kg, R1 = 10 m, R2 = 20 m), several edge spans.

Logic. In the rebuild the shift profile S(r) is identically 0 for r >= R2 - Rb (paper eqs. 27-28),
so for r > R2 the metric is the ZERO-SHIFT static spherical metric at every beta_warp. There T is
diagonal in the static orthonormal frame -> Hawking-Ellis type I, and the energy conditions are the
exact 1-D inequalities NEC eps+p_i >= 0, WEC eps >= 0, SEC eps+p_r+2p_t >= 0, DEC eps >= |p_i|.
Type IV (no timelike eigenvector) is a frame-invariant property, so it cannot arise in that region
in ANY frame (including the frame where the shell moves at v_s). We print:
  - max S(r) for r > R2 (must be 0),
  - outer edge of the smoothed matter support,
  - exact tail margins / eps_peak and max |p|/eps in the tail,
  - the same for the whole profile.
Units: SI (Pa = J/m^3); margins also given as a fraction of eps_peak (dimensionless).
"""
import sys

import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from warp_shell import build_shell  # noqa: E402

M, R1, R2 = 4.49e27, 10.0, 20.0

print("span_P[m] span_rho[m] | maxS(r>R2) | matter edge r[m] | tail min NEC/eps_pk  min WEC/eps_pk  min SEC/eps_pk  min DEC/eps_pk | tail max|p|/eps | whole-shell max|p|/eps (r)")
for span in (0.6, 1.0, 2.0, 3.0, 4.0):
    for beta in (0.0, 0.02):
        s = build_shell(M, R1, R2, beta_warp=beta, span_P=span, N=16001)
        r, e, pr, pt = s.r, s.eps, s.p_r, s.p_t
        ep = s.eps_peak
        tail = r > R2
        S_tail = float(np.max(s.S(r[tail])))
        mat = np.maximum(np.abs(e), np.maximum(np.abs(pr), np.abs(pt))) > 1e-12 * ep
        edge = float(r[mat].max())
        tm = tail & mat
        et, prt, ptt = e[tm], pr[tm], pt[tm]
        nec = np.minimum(et + prt, et + ptt).min() / ep
        wec = min(et.min(), (et + prt).min(), (et + ptt).min()) / ep
        sec = min((et + prt).min(), (et + ptt).min(), (et + prt + 2 * ptt).min()) / ep
        dec = np.minimum(et - np.abs(prt), et - np.abs(ptt)).min() / ep
        with np.errstate(divide="ignore", invalid="ignore"):
            ratio_t = np.where(et > 0, np.maximum(np.abs(prt), np.abs(ptt)) / et, np.inf)
        ec = s.energy_conditions_static()
        print(f"{s.smoothing['span_P_m']:.3f} {s.smoothing['span_rho_m']:.3f} beta={beta:.2f} | {S_tail:.1e} | {edge:.2f} | "
              f"{nec:+.3e} {wec:+.3e} {sec:+.3e} {dec:+.3e} | {np.max(ratio_t):.4f} | "
              f"{ec['max_|p|/eps']['value']:.4f} (r={ec['max_|p|/eps']['at_r_m']:.2f} m); all-hold "
              f"{all(ec[k]['holds'] for k in ('NEC','WEC','SEC','DEC'))}")

# tail-matter fraction of eps at r = 23.9 m (Le's worst probe) for each span
print("\neps(r=23.9 m)/eps_peak by span_P (0 means exact Schwarzschild vacuum there):")
for span in (0.6, 1.0, 2.0, 3.0, 4.0):
    s = build_shell(M, R1, R2, span_P=span, N=16001)
    print(f"  span_P = {span:.1f} m: {np.interp(23.9, s.r, s.eps) / s.eps_peak:.3e}")
