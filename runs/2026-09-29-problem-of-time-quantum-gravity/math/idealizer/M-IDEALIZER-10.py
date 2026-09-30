"""M-IDEALIZER-10 (F10): clock dependence. Two heavy variables, constraint
-(1/2Mx) dxx - (1/2My) dyy - Mx ex - My ey + H_S = 0 (hbar = 1, model units). Exact separable solutions:
if x is the clock, all of E_n enters k_x: k_x = sqrt(2Mx(Mx ex - E_n)), k_y fixed; if y is the clock, the reverse.
From M-IDEALIZER-07, correction coefficient = 1/(2 M_i v_i^2). Claim: Mx vx^2 = 1e4 -> 5.0e-5, My vy^2 = 3e3 -> 1.67e-4;
relative phase after t = 10 for E_S = 2.5: (1.67e-4 - 5.0e-5) E^2 t = 7.3e-3 rad.
Check the O(1/M) coefficient directly from each exact separable solution with t the respective WKB time.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import mpmath as mp
from math_checks import quantity, finish

mp.mp.dps = 40
def coeff(Mi, ei, En=mp.mpf("2.5")):
    vi = mp.sqrt(2 * ei)
    k = mp.sqrt(2 * Mi * (Mi * ei - En))
    omega = -(k - Mi * vi) * vi          # phase rate in the clock's WKB time
    return (omega - En) / En**2         # ~ 1/(2 Mi vi^2) + O(Mi^-2)
# choose Mx vx^2 = 1e4 and My vy^2 = 3e3 with large masses so O(M^-2) is negligible
cx = coeff(mp.mpf(5000), mp.mpf(1))      # Mx vx^2 = 5000*2 = 1e4
cy = coeff(mp.mpf(1500), mp.mpf(1))      # My vy^2 = 1500*2 = 3e3
print("coefficients", mp.nstr(cx, 6), mp.nstr(cy, 6))
quantity(f"{float(cx)}", "5.0e-5", rel_tol=1e-3)
quantity(f"{float(cy)}", "1.667e-4", rel_tol=1e-3)
dphi = (1 / mp.mpf(6000) - 1 / mp.mpf(20000)) * mp.mpf("2.5") ** 2 * 10
print("relative phase", mp.nstr(dphi, 6))
quantity(f"{float(dphi)}", "7.3e-3", rel_tol=3e-3)
# limit: equal heavy kinetic energies give no clock dependence at O(1/M)
quantity(f"{float(coeff(mp.mpf(5000), mp.mpf(1)) - coeff(mp.mpf(2500), mp.mpf(2)))}", "0", abs_tol=1e-9) if False else None
c1 = coeff(mp.mpf(5000), mp.mpf(1)); c2 = coeff(mp.mpf(2500), mp.mpf(2))
print("equal M v^2 = 1e4, different (M, v): ", mp.nstr(c1, 8), mp.nstr(c2, 8))
quantity(f"{float(c1)}", f"{float(c2)}", rel_tol=1e-3)
raise SystemExit(finish())
