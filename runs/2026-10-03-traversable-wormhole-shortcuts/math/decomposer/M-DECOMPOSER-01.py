"""M-DECOMPOSER-01: lag thresholds for shortcut and CTC in a one-sided wormhole with static mouths.

Model (independent of the lens's script): flat exterior, mouths A and B at rest, separation d.
Exterior coordinate time t (static observers synchronised through the exterior, c explicit).
Throat identification: a signal entering A at exterior time t leaves B at t + L/c + s,
where L is the throat's null path length and s the clock shift (s < 0 is a lag built up by
MTY mouth motion or by a potential difference). Exterior light time A->B is d/c.

T_thru(A->B) = L/c + s; shortcut iff T_thru < d/c  <=>  -s > (L-d)/c.
Closed causal loop A ->(throat) B ->(exterior) A takes L/c + s + d/c; CTC iff <= 0 <=> -s >= (L+d)/c.
Reverse loop B ->(throat) A ->(exterior) B takes L/c - s + d/c > 0 for s <= 0, so never a CTC.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, sign, limit, units, inequality, finish

L, d, c = sp.symbols("L d c", positive=True)
s = sp.symbols("s", real=True)

T_thru = L / c + s
T_ext = d / c
# shortcut threshold: solve T_thru = T_ext for -s
lag_short = sp.solve(sp.Eq(T_thru, T_ext), s)[0] * -1
lag_ctc = sp.solve(sp.Eq(T_thru + T_ext, 0), s)[0] * -1
print("lag for shortcut:", lag_short, " lag for CTC:", lag_ctc)
identity(lag_short, (L - d) / c)
identity(lag_ctc, (L + d) / c)
# ordering: CTC threshold minus shortcut threshold = 2d/c > 0 for every L > 0, d > 0 (long or short throat)
identity(lag_ctc - lag_short, 2 * d / c)
sign(lag_ctc - lag_short, "positive")
# reverse-direction loop is never closed-causal while s <= 0
sign((L / c - s + d / c).subs(s, -sp.Symbol("u", positive=True)), "positive")
# limits: short throat L -> 0 reduces to the MTY result (CTC once the lag exceeds d/c, shortcut already at s = 0)
limit(lag_ctc, "L", 0, d / c)
limit(lag_short, "L", 0, -d / c)
# mouths coincide d -> 0: both thresholds merge at L/c
limit(lag_ctc - lag_short, "d", 0, 0)
# units: (L +- d)/c is a time
units("(9.4e3 ly + 1e3 ly)/c", "time")
raise SystemExit(finish())
