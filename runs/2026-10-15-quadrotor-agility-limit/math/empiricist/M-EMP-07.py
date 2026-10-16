"""M-EMP-07. Latency's share of the required stopping distance.

Claim (empiricist F5/F6 and the calculations table; used to argue EMP-E's elimination):
"latency is 5-24 per cent of the required stopping distance above 5 m/s".

Statement checked: with d_stop(v) = v*tau + v^2/(2a), the latency share is
    s(v) = v*tau / d_stop(v) = tau / (tau + v/(2a)),
with tau = 40 ms and a = 40 m/s^2 (the lens's inputs elsewhere in F6).
s is strictly decreasing in v, so a range of shares corresponds to a range of
speeds; the question is which speeds give 5-24 per cent.

Symbols and domain: v speed (m/s, > 0), tau >= 0 s, a > 0 m/s^2, s dimensionless
in (0, 1]. Assumptions as in M-EMP-06 (straight line, constant deceleration).
"""
import sys

import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, inequality, limit, units  # noqa: E402

tau, a = 0.040, 40.0


def share(v):
    return tau / (tau + v / (2 * a))


print(f"inputs: tau = {tau * 1e3:.0f} ms, a = {a} m/s^2; s(v) = tau/(tau + v/(2a))")
for v in (5.0, 7.0, 10.0, 20.0, 30.0, 40.0, 60.0):
    print(f"  v = {v:5.1f} m/s: latency share = {100 * share(v):6.2f}%")

# the speed at which the share equals 24% and 5%
vs = sp.Symbol("v", positive=True)
v_24 = float(sp.solve(sp.Eq(tau / (tau + vs / (2 * a)), 0.24), vs)[0])
v_05 = float(sp.solve(sp.Eq(tau / (tau + vs / (2 * a)), 0.05), vs)[0])
print(f"share = 24% at v = {v_24:.2f} m/s; share = 5% at v = {v_05:.2f} m/s")
print(f"over the regime the lens discusses (5-20 m/s) the share is "
      f"{100 * share(20.0):.1f}-{100 * share(5.0):.1f}%")

# the claimed band 5-24% requires speeds from ~10 to ~61 m/s, not "above 5 m/s"
inequality(f"abs({v_24:.6f} - 10.13)", "<", "0.01")   # 24% is reached only at ~10.1 m/s
inequality(f"{v_05:.6f}", ">", "50")
inequality(f"{100 * share(5.0):.6f}", ">", "24")     # at 5 m/s the share exceeds the claimed band
inequality(f"{100 * share(5.0):.6f}", "<", "40")
inequality(f"{100 * share(20.0):.6f}", ">", "5")     # at 20 m/s it is still above 5 per cent
# but the qualitative content survives: the share is below one half above 5 m/s
inequality(f"{100 * share(5.0):.6f}", "<", "50")

identity("v*t/(v*t + v**2/(2*a))", "t/(t + v/(2*a))",
         domain={"v": (0.1, 60.0), "t": (0.01, 0.5), "a": (1.0, 100.0)})
limit("t/(t + v/(2*a))", "v", 0, "1", domain={"t": (0.01, 0.5), "a": (1.0, 100.0)})
limit("t/(t + v/(2*a))", "v", "oo", "0", domain={"t": (0.01, 0.5), "a": (1.0, 100.0)})
sp_sym = sp.Symbol("vv", positive=True)
deriv = sp.diff(tau / (tau + sp_sym / (2 * a)), sp_sym)
print("d s/d v =", sp.simplify(deriv))
inequality(str(sp.simplify(-deriv)).replace("vv", "v"), ">", "0", domain={"v": (0.1, 60.0)})
units("((5 m/s) * (0.04 s)) / (0.5125 m)", "dimensionless")
raise SystemExit(finish())
