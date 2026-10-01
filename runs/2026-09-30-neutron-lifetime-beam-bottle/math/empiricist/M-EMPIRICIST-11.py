"""M-EMPIRICIST-11: uncertainty of the PERKEO II-based SM tau_beta quoted in F13 (880.34 +- 1.40 s).
PERKEO II (Mund 2013, D-41): lambda = -1.2748 +- 0.0008 (stat) +0.0010/-0.0011 (sys). tau = K'/(1 + 3 lambda^2),
K' = 5172.0 s; sigma^2 = (dtau/dlambda sigma_lambda)^2 + (2 tau sigma_V/V)^2 + sigma_K^2 with sigma_V = 0.00032,
V = 0.97367, sigma_K = 0.19 s (the same budget that reproduces the lens's PERKEO III 0.88 s, see M-09)."""
import sys
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/empiricist")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from _inputs import *
from math_checks import limit, units, finish

limit("sqrt(a**2 + b**2)", "a", 0, "b")          # stat -> 0 recovers the sys-only error
units("(1146 s) * 0.0013", "s")
l = 1.2748; Kp = 4908.6 / 0.97420 ** 2; t = Kp / (1 + 3 * l * l); dl = 6 * l * t / (1 + 3 * l * l)
other = q(2 * t * 0.00032 / 0.97367, 0.19)
for label, sl in [("stat (+) sys, mean side", q(0.0008, 0.00105)), ("stat (+) sys, +side", q(0.0008, 0.0010)),
                  ("stat (+) sys, -side", q(0.0008, 0.0011)), ("sys -side only (0.0011)", 0.0011)]:
    print(f"{label}: sigma_lambda {sl:.5f}, sigma_tau {q(dl*sl, other):.3f} s")
s_full = q(dl * q(0.0008, 0.00105), other)
agree("lens 1.40 s vs full propagation", s_full, 1.40, 0.02)
zb = (887.97 - t) / q(s_full, 2.04); zs = (t - 878.41) / q(s_full, 0.25)
print(f"tau {t:.2f} s; with sigma {s_full:.2f} s: {zs:.2f} sigma from storage, {zb:.2f} sigma from proton beam")
raise SystemExit(finish())
