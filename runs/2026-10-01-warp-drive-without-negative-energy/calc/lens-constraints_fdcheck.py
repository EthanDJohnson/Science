#!/usr/bin/env python3
"""Constraints lens: finite-difference step check for the reference-case (R = 100 m,
sigma = 2 /m, v = 10) Natario and zero-vorticity scans, where 'vacuum (within FD error)'
and unconverged points appeared at h = 0.01/sigma. Geometric units (1/m^2).
Re-scans the same wall points with several steps, and re-checks the scale-equivalent case
(lengths divided by 100: R = 1 m, sigma = 200 /m, v = 10; T scales by 100^2) to see whether
the verdicts are step-robust."""
import importlib.util
import sys

import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from numeric_stress_energy import NumericSpacetime  # noqa: E402

spec = importlib.util.spec_from_file_location(
    "ni", "runs/2026-10-01-warp-drive-without-negative-energy/calc/lens-constraints_natario_irrot.py")
ni = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ni)

for kind in ("NAT", "IRR"):
    for (R, s, v, lab) in ((100.0, 2.0, 10.0, "reference"), (1.0, 200.0, 10.0, "reference scaled by 1/100")):
        pts = ni.wall_points(R, s)
        for hfac in (0.04, 0.02, 0.01, 0.005):
            st = NumericSpacetime(ni.metric_factory(kind, v, R, s), h=hfac / s)
            sc = st.scan_energy_conditions(pts)
            print(f"{kind} {lab} h={hfac}/sigma: points {sc['points']} unconverged {sc['unconverged']}"
                  f" robust {sc['violations']} strict {sc['violations_strict']} types {sc['types']}"
                  f" worst nec_min {sc['worst']['nec_min'][0]:.4e}")
        # direct look at the largest-|rho| wall point with the finest step
        st = NumericSpacetime(ni.metric_factory(kind, v, R, s), h=0.02 / s)
        r = st.energy_conditions(pts[len(pts) // 4])
        print(f"   sample point {pts[len(pts)//4]}: type {r['type']} err {r['err']:.3e} max|T| "
              f"{np.max(np.abs(r['T_frame'])):.3e} nec {r['nec']} rho_E {r['rho_eulerian']:.4e}")
