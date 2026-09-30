"""M-EMPIRICIST-05: gap size (F8, candidate A). Delta = tau_p - tau_s; fraction f = 1 - tau_s/tau_p;
missing loss rate r = 1/tau_s - 1/tau_p. Lifetimes in s (SI); rate in s^-1."""
import sys
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/empiricist")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from _inputs import *
from math_checks import identity, series, quantity, units, finish

identity("1/ts - 1/tp", "(tp - ts)/(tp*ts)")
series("1/t - 1/(t + d)", "d", 0, 2, "d/t**2")          # small-gap limit r ~ Delta/tau^2
identity("1 - ts/tp", "(tp - ts)/tp")
units("1/(878.41 s) - 1/(887.97 s)", "Hz")

tp, _ = wmean(PROTON); ts, _ = wmean(STORAGE)
d, f, r = tp - ts, 1 - ts / tp, 1 / ts - 1 / tp
print(f"tau_p {tp:.4f} s, tau_s {ts:.4f} s, gap {d:.4f} s, fraction {f:.5f}, rate {r:.4e} s^-1")
agree("gap", d, 9.55, 0.015)        # lens prints 9.55 in F8 and 9.56 in F14
agree("fraction", f, 0.0108, 0.00006)
quantity(f"{r} Hz", "1.23e-5 Hz", rel_tol=5e-3)
print(f"gap / BL1 total budget 2.3 s = {d/2.3:.3f}; BL1 total q(1.2,1.9) = {q(1.2,1.9):.3f} s")
agree("about 4x BL1 budget", d / 2.3, 4.0, 0.25)
print(f"0.3% of 888 s = {0.003*888:.3f} s")
agree("0.3% of 888 s", 0.003 * 888, 2.7, 0.06)
raise SystemExit(finish())
