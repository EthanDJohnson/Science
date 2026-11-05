"""M-EXAMINER-08: early-time fits, gap closed and residual vs SH0ES (F8).
gap closed f = (H_fit - H_LCDM)/(H_SH0ES - H_LCDM) with H_LCDM = CMB-SPA 67.19, H_SH0ES = 73.49.
Residual: z = (73.49 - H_fit)/sqrt(s_fit,+^2 + 0.93^2); the facing (upper) error of the fit is the relevant one.
Limits: H_fit = H_LCDM -> f = 0; H_fit = H_SH0ES -> f = 1."""
import sys, math
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/examiner")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from common import *
from math_checks import identity, quantity, finish

identity("((h - a)/(b - a)).subs(h, a)", "0", domain={"a": (60, 70), "b": (71, 80), "h": (60, 80)})
identity("((h - a)/(b - a)).subs(h, b)", "1", domain={"a": (60, 70), "b": (71, 80), "h": (60, 80)})
fits = {"EDE P-ACT-LB": ((69.9, 0.8, 1.5), 43, 2.43), "Poulin 2026": ((71.0, 1.1, 1.1), 60, 1.73),
        "eROSITA EDE": ((71.4, 1.4, 1.4), 67, 1.24), "Mod. recomb.": ((69.6, 1.0, 1.0), 38, 2.85),
        "PMF": ((69.1, 0.5, 0.5), 30, 4.16)}
for k, (m, fc, rc) in fits.items():
    f = 100 * (m[0] - CMB[0]) / (SH0ES[0] - CMB[0])
    zf, zsy = z_facing(m, SH0ES), z_sym(m, SH0ES)
    print(f"{k}: closed {f:.1f}% (lens {fc}); residual facing {zf:.3f}, symmetrised {zsy:.3f} (lens {rc})")
    quantity(f"{f}", f"{fc}", rel_tol=1.2e-2)
    quantity(f"{zf}", f"{rc}", rel_tol=5e-3)
# with ACT's own LCDM baseline 68.2 (D-52) for the P-ACT-LB EDE fit
print("P-ACT-LB closure vs its own LCDM 68.2:", 100 * (69.9 - 68.2) / (73.49 - 68.2), "%")
raise SystemExit(finish())
