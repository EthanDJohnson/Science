"""M-CONSTRAINTS-13 (F14): error inflation the null needs.
Agreement at k = 2 sigma: |dH| / sqrt(sL^2 + sE^2) = 2.  Inflated local error sL' = sqrt((dH/2)^2 - sE^2); factor sL'/sL.
Unmodelled shift S: (dH - S)/sqrt(sL^2 + sE^2) = 2 -> S = dH - 2 sqrt(sL^2 + sE^2). Units km/s/Mpc."""
import sys, math
import sympy as sp
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/constraints")
from math_checks import identity, inequality, finish
from _bg import near

def need(hl, sl, he, se):
    d = hl - he
    s_new = math.sqrt((d / 2) ** 2 - se ** 2)
    return s_new, s_new / sl, d - 2 * math.hypot(sl, se)

for lab, args, want in [("H0DN-SPA", (73.264, .806, 67.19, .38), (3.01, 3.7, 4.3)),
                        ("H0DN-BAO+BBN", (73.264, .806, 68.50, .58), (None, 2.9, 2.8)),
                        ("SH0ES-SPA", (73.49, .93, 67.19, .38), (None, 3.4, None)),
                        ("SH0ES-BAO+BBN", (73.49, .93, 68.50, .58), (None, 2.6, None))]:
    s, fac, S = need(*args)
    print(lab, f"sL'={s:.3f} factor={fac:.3f} shift={S:.3f}")
    if want[0]: near("sL'", s, want[0], 0.006)
    near("factor", fac, want[1], 0.06)
    if want[2]: near("shift", S, want[2], 0.06)
# symbolic: the inflated error indeed gives exactly 2 sigma
d, se = sp.symbols("d s_e", positive=True)
s_new = sp.sqrt((d / 2) ** 2 - se ** 2)
identity(d / sp.sqrt(s_new ** 2 + se ** 2), sp.Integer(2), domain={"d": (2.1, 10), "s_e": (0.1, 1)})
# one-sided p for 3.3 sigma ~ 5e-4
p = 0.5 * math.erfc(3.3 / math.sqrt(2)); near("one-sided p(3.3 sigma)", p, 5e-4, 0.5e-4)
raise SystemExit(finish())
