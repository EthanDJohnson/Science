"""falsifier-C2-0 part 3: can a wider smoothing span restore the zero-shift DEC at high compactness?

SI units; R1 = 10 m, R2 = 20 m (Delta/R2 = 0.5); C = 2GM/(c^2 R2). Static type-I DEC ratio
max(|p_r|,|p_t|)/eps over eps > 1e-3 eps_max, toolkit build_shell with span_P = s (m), span_rho = 1.72 s.
Also the static max|p|/eps with no smoothing ignoring the R1 hoop sheet (interior bulk of the exact
constant-density TOV shell: p_r = P'(r), eps = rho c^2), to separate the sheet remnant from bulk pressure.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/tools")
import numpy as np
from warp_shell import build_shell, tov_constant_density_shell

Gc, cc = 6.674e-11, 2.998e8
R1, R2 = 10.0, 20.0
for C in (0.3334, 0.5, 0.6, 0.7, 0.8, 0.85):
    M = C * cc ** 2 * R2 / (2 * Gc)
    rs, Ps = tov_constant_density_shell(M, R1, R2)
    rho_c2 = 3 * M / (4 * np.pi * (R2 ** 3 - R1 ** 3)) * cc ** 2
    line = f"C = {C:.4f}: bulk P(R1)/eps = {Ps[0] / rho_c2:.3f}, R1 hoop sheet R1 P(R1)/2 = {R1 * Ps[0] / 2:.3e} N/m; smoothed max|p|/eps:"
    for s in (0.5, 1.0, 2.0, 3.0, 4.0):
        try:
            sh = build_shell(M, R1, R2, span_P=s)
            eps, pr, pt, r = sh.eps, sh.p_r, sh.p_t, sh.r
            msk = eps > 1e-3 * eps.max()
            q = np.max(np.maximum(np.abs(pr[msk]), np.abs(pt[msk])) / eps[msk])
            line += f"  s={s}: {q:.3f}"
        except Exception as e:  # noqa: BLE001
            line += f"  s={s}: fail({e})"
    print(line)
