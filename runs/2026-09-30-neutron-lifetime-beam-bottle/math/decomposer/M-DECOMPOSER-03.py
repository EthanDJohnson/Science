"""M-DECOMPOSER-03 (F3): storage internal consistency (7 results), material and magnetic class means.
S = sqrt(chi2/(N-1)); p = chi2 survival; material-magnetic difference with scaled material error. SI (s)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/decomposer")
from math_checks import limit, finish
from _inputs import *

ms, ss, c2, S = wmean(STORAGE)
p = chi2_sf(c2, 6)
print(f"storage: {ms:.3f} +- {ss:.3f}, chi2 {c2:.3f}/6, p {p:.3e}, S {S:.3f}")
near("storage chi2", c2, 23.3, 0.05)
near("storage p (1e-4)", p * 1e4, 7, 0.5)
near("storage S", S, 1.97, 0.005)
near("storage mean (s)", ms, 878.38, 0.005)
near("storage scaled sigma (s)", S * ss, 0.49, 0.005)
mm, sm, c2m, Sm = wmean(MATERIAL)
mg, sg, c2g, Sg = wmean(MAGNETIC)
print(f"material {mm:.3f} +- {sm:.3f} (S {Sm:.3f} -> {Sm*sm:.3f}), chi2 {c2m:.3f}/4")
print(f"magnetic {mg:.3f} +- {sg:.3f}, chi2 {c2g:.3f}/1")
near("material mean", mm, 880.03, 0.005)
near("material scaled sigma", Sm * sm, 0.70, 0.005)
near("material S", Sm, 1.43, 0.005)
near("magnetic mean", mg, 877.83, 0.005)
near("magnetic sigma", sg, 0.28, 0.005)
d = mm - mg; sd = q(Sm * sm, sg)
print(f"material - magnetic = {d:.3f} +- {sd:.3f} s, {d/sd:.3f} sigma")
near("difference (s)", d, 2.20, 0.005)
near("difference z", d / sd, 2.9, 0.05)
# limit: the S-scaled error reduces to the plain one when chi2 = N-1
limit("s*sqrt(c/k)", "c", "k", "s", domain={"k": (1, 10), "c": (0.1, 30), "s": (0.1, 10)})
raise SystemExit(finish())
