"""M-CONSTRAINTS-08: compactness, Buchdahl ceiling, beta_crit/C ratio and its extrapolation (F9; B, E).

SI. C = 2GM/(c^2 R2). Buchdahl/Andreasson: C < 8/9 => M < 4 c^2 R2/(9 G).
Lens ratios beta_crit/C = 0.082, 0.079, 0.073, 0.066 at C = 0.083, 0.167, 0.333, 0.500 (lens numbers, taken
as data); claimed extrapolated cap at C = 8/9 'roughly 0.05-0.06'.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
from math_checks import quantity, units, finish

quantity("2*G*4.49e27 kg/(c^2 * 20 m)", "0.3334", rel_tol=2e-3)
quantity("4*c^2*20 m/(9*G)", "1.197e28 kg", rel_tol=2e-3)
quantity("4*c^2*20 m/(9*G)", "6.31 Mjup", rel_tol=3e-3)
C0 = 2 * 6.67430e-11 * 4.49e27 / (299792458.0**2 * 20)
quantity(f"{0.0244 / C0}", "0.073", rel_tol=1e-2)
quantity(f"{0.02386 / C0}", "0.0716", rel_tol=2e-3)       # with the corrected beta_crit (M-CONSTRAINTS-06b)
Cs = np.array([0.083, 0.167, 0.333, 0.500]); ratio = np.array([0.082, 0.079, 0.073, 0.066])
Cb = 8 / 9
lin = np.polyfit(Cs, ratio, 1); quad = np.polyfit(Cs, ratio, 2)
last2 = ratio[-1] + (ratio[-1] - ratio[-2]) / (Cs[-1] - Cs[-2]) * (Cb - Cs[-1])
caps = {"constant ratio 0.066": 0.066 * Cb, "linear fit": np.polyval(lin, Cb) * Cb,
        "last-two-points slope": last2 * Cb, "quadratic fit": np.polyval(quad, Cb) * Cb}
for k, val in caps.items():
    print(f"cap at C = 8/9, {k}: beta = {val:.4f}")
quantity(f"{caps['constant ratio 0.066']}", "0.0587", rel_tol=2e-3)
quantity(f"{caps['linear fit']}", "0.0457", rel_tol=2e-2)
units("G*1 kg/(c^2 * 1 m)", "dimensionless")
raise SystemExit(finish())
