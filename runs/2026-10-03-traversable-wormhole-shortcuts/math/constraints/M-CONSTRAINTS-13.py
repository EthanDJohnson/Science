"""M-CONSTRAINTS-13 (F15, F20). Static one-sided wormhole, exterior-synchronised clocks.
Throat leg: entry event (t, A) to exit event (t + T_thru, B). Exterior light time T_ext.
(a) If T_thru > T_ext the exit event lies strictly inside the exterior future light cone of the entry event,
    so a timelike exterior curve links them: chronal. Achronal requires T_thru <= T_ext.
(b) Numbers: MM pi*l/c with l = 3e3 ly gives 9.42e3 yr; T_thru/T_ext = 9425, 94.2, 9.42, 3.15 for d = 1, 1e2, 1e3,
    2990 ly; a 2 m light-length throat vs 1 km: margin (2 m - 1000 m)/c = -3.3e-6 s.
(c) F20: with exit Delta earlier than throat transit implies, the closed loop entry -> throat -> exterior back
    returns at t + T_thru - Delta + T_ext; a closed causal curve exists iff Delta >= T_thru + T_ext."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, inequality, sign, quantity, finish

Tt, Te, D, tau = sp.symbols("T_thru T_ext Delta tau", positive=True)
# (a) a timelike exterior worldline of speed v < 1 covering distance T_ext in time T_thru exists iff T_thru > T_ext
v = Te / Tt
inequality(v, "<", 1, domain={"T_thru": (1.01, 10), "T_ext": (0.1, 1)})
# (c) return time minus start time
ret = Tt - D + Te
identity(sp.solve(sp.Eq(ret, 0), D)[0], Tt + Te)
sign(ret.subs(D, Tt + Te + tau), "negative")      # Delta beyond threshold: arrives before departure
# limit: classical shortcut T_thru -> 0 gives Delta > T_ext (MTY case)
identity(sp.limit(Tt + Te, Tt, 0), Te)
# (b) numbers
pil = 3.141592653589793 * 3e3       # years
print("pi l / c =", pil, "yr")
for d, cl in [(1, 9425), (1e2, 94.2), (1e3, 9.42), (2990, 3.15)]:
    inequality(abs(pil / d - cl) / cl, "<", 0.003)
quantity("(2 m - 1000 m) / c", "-3.33e-6 s", rel_tol=3e-3)
quantity("3.14159265 * 3000 ly / c", "9425 yr", rel_tol=3e-3)
raise SystemExit(finish())
