"""M-MECHANIST-07: BAO+BBN route. DESI DR2 fixes Ω_m = 0.2975 and h·r_d = 101.54 ± 0.73 Mpc [D-45].
(a) r_d must fall by 1 - 68.50/73.264 at fixed h·r_d; significance (fractional change)/(0.73/101.54).
(b) The lens says ω_b would have to rise ×1.69. Self-consistently, with Ω_m fixed by BAO, raising h also
    raises ω_cb = Ω_m h², which itself shrinks r_d. So solve h·r_d(h, ω_b, Ω_m h²) = 101.54 for h, and
    find the ω_b that moves h by 73.264/68.50. Compare with the fixed-ω_cb calculation (lens's number).
"""
import math
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/mechanist")
from scipy.optimize import brentq
from math_checks import inequality, finish
from mm_common import near
import mm_bg as B

Om, hrd = 0.2975, 101.54
# EH98 z_d with an exact integral overestimates r_d by ~2% (known); normalise to CAMB-like 147.09 Mpc at Planck 2018
NORM = 147.09 / B.rd(0.6736, 0.02237, 0.1430)
print(f"r_d normalisation factor {NORM:.4f}")
_rd = B.rd
B.rd = lambda h, ob, om: NORM * _rd(h, ob, om)
drop = 100 * (1 - 68.50 / 73.264)
near("r_d drop %", drop, 6.5, 0.05)
near("sigma vs 0.72%", drop / (100 * 0.73 / 101.54), 9.0, 0.2)


def h_of_ob(ob):
    return brentq(lambda h: h * B.rd(h, ob, Om * h * h) - hrd, 0.4, 1.3, xtol=1e-12)


ob0 = 0.02218  # BBN-like baseline
h0 = h_of_ob(ob0)
print(f"baseline: omega_b = {ob0}, h = {h0:.4f}, r_d = {hrd/h0:.2f} Mpc (DESI+BBN quotes 68.50)")
target = h0 * 73.264 / 68.50
ob_need = brentq(lambda ob: h_of_ob(ob) - target, ob0, 0.08, xtol=1e-10)
ratio_consistent = ob_need / ob0
print(f"self-consistent (Ω_m fixed): omega_b must rise x{ratio_consistent:.3f}")
# lens-style: r_d must drop by 68.50/73.264 holding omega_cb fixed at the baseline value
ocb0 = Om * h0 * h0
rd0 = B.rd(h0, ob0, ocb0)
ob_fixed = brentq(lambda ob: B.rd(h0, ob, ocb0) - rd0 * 68.50 / 73.264, ob0, 0.2, xtol=1e-10)
ratio_fixed = ob_fixed / ob0
print(f"fixed omega_cb (not BAO-consistent): omega_b must rise x{ratio_fixed:.3f}")
near("lens number reproduced only at fixed omega_cb", ratio_fixed, 1.69, 0.06)
near("self-consistent ratio vs lens 1.69", ratio_consistent, 1.69, 0.06)   # expected FAIL
inequality(f"{ratio_consistent!r} - 1", ">", "0.2")  # still >> 1% D/H precision: conclusion survives
# limit: zero H0 change -> ratio 1
near("no change limit", brentq(lambda ob: h_of_ob(ob) - h0, 0.01, 0.05, xtol=1e-12) / ob0, 1.0, 1e-6)
raise SystemExit(finish())
