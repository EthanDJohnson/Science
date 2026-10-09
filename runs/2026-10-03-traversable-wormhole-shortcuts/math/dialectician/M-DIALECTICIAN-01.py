"""M-DIALECTICIAN-01: clock-offset thresholds for a one-sided wormhole.

Model (independent): throat = flat 1+1 strip, coordinates (t, x), x in [0, T] (T = T_thru, c = 1).
Mouth B at x = 0 is glued to exterior B at exterior time t; mouth A at x = T is glued to exterior A
at exterior time t - Delta (A's mouth clock is offset by Delta relative to exterior sync).
Exterior: flat, mouths a distance d apart (light time d).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, sign, limit, quantity, finish

T, d, Dl, t0 = sp.symbols("T d Delta t0", positive=True)

# B -> A through throat: leave exterior B at t0, enter x=0 at throat time t0, reach x=T at t0+T,
# which is exterior time t0 + T - Delta at A.
t_BA = (t0 + T - Dl) - t0
# A -> B: leave exterior A at t0 -> throat time t0 + Delta at x=T -> x=0 at t0+Delta+T = exterior.
t_AB = (t0 + Dl + T) - t0
identity(t_BA, T - Dl)
identity(t_AB, T + Dl)

# Shortcut B->A iff t_BA < d  <=> Delta > T - d
Delta_s = sp.solve(sp.Eq(t_BA, d), Dl)[0]
identity(Delta_s, T - d)
# Closed causal loop: B->A throat then A->B exterior returns to B at t0 + (T - Delta) + d; CTC iff < t0
Delta_ctc = sp.solve(sp.Eq(t_BA + d, 0), Dl)[0]
identity(Delta_ctc, T + d)
# window width
identity(Delta_ctc - Delta_s, 2 * d)
# Shortcut threshold precedes CTC threshold for any d > 0
sign(Delta_ctc - Delta_s, "positive")
# Just above Delta_s the throat is faster than exterior; check sign of (d - t_BA) at Delta = Delta_s + eps
eps = sp.symbols("eps", positive=True)
sign((d - t_BA).subs(Dl, T - d + eps), "positive")
# Limit: zero offset -> transit equals T (no shortcut for a long wormhole T > d)
limit(t_BA, "Delta", 0, "T", domain={"T": (1, 10), "d": (0.1, 1)})
# FGM 2019: T_thru = d + Lg (log term Lg > 0) -> Delta_s = Lg
Lg = sp.symbols("Lg", positive=True)
identity(Delta_s.subs(T, d + Lg), Lg)
# Units: thresholds are times; T in yr, d/c in yr
quantity("9424.78 yr - 1000 ly / c", "8424.78 yr", rel_tol=1e-3)

raise SystemExit(finish())
