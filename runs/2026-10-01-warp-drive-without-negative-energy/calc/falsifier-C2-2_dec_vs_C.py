#!/usr/bin/env python3
"""Falsifier C2-2: does the ZERO-SHIFT rebuilt shell itself keep the DEC as compactness rises?
(The C2 slate extrapolates the shift cap to the Buchdahl compactness 8/9, which presumes the
unshifted shell stays energy-condition clean there.) SI units; ratios dimensionless.
Exact type-I test (static, diagonal T): DEC <=> eps >= |p_r| and eps >= |p_t|.
"""
import math
import sys

import numpy as np

sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/tools")
from warp_shell import build_shell, G, C  # noqa: E402

R1, R2 = 10.0, 20.0
for span in (1.0, 2.0, 3.0):
    print(f"--- span_P = {span} m (span_rho = 1.72 span_P), R1 = 10 m, R2 = 20 m ---")
    for Cc in (1 / 3, 0.36, 0.38, 0.40, 0.42, 0.45, 0.5, 0.6, 0.7, 0.8):
        M = Cc * C ** 2 * R2 / (2 * G)
        try:
            s = build_shell(M, R1, R2, span_P=span)
        except ValueError as exc:
            print(f"  C = {Cc:.3f}: refused ({exc})")
            continue
        ec = s.energy_conditions_static()
        print(f"  C = {Cc:.3f}: max|p|/eps = {ec['max_|p|/eps']['value']:.3f} at r = {ec['max_|p|/eps']['at_r_m']:.2f} m; "
              f"NEC {ec['NEC']['holds']}, WEC {ec['WEC']['holds']}, SEC {ec['SEC']['holds']}, DEC {ec['DEC']['holds']}")
# grid convergence spot check at the published compactness and at C = 0.5
for N in (8001, 16001):
    for Cc in (1 / 3, 0.5):
        s = build_shell(Cc * C ** 2 * R2 / (2 * G), R1, R2, N=N)
        ec = s.energy_conditions_static()
        print(f"  N = {N}, C = {Cc:.3f}: max|p|/eps = {ec['max_|p|/eps']['value']:.4f}, DEC {ec['DEC']['holds']}")
