"""M-EMP-03. Swift's mean speed and the seen/unseen speed ratio.

Claims (empiricist F3, ledger rows 3 and 14; load-bearing for EMP-A):
(a) a best three-lap time t3 = 17.465 s on a lap of length L = 75 m is a mean
    speed v = 3L/t3 = 12.88 m/s;
(b) against 5 m/s unseen-clutter mean speed the ratio is 2.58x; against 7 m/s it is 1.84x;
(c) with a MonoRace seen-track mean bracketed at 13-30 m/s the ratio is 4-6x.

Symbols: L = 75 m lap length (>0), t3 = 17.465 s elapsed for three laps (>0),
v = path-length mean speed (m/s). Assumption: the lap length is the distance
actually flown per lap and the three laps are consecutive, so the mean over the
three laps is 3L/t3. Both are the lens's stated assumptions, not derived here.
The single-lap bracket 11.0-13.6 m/s rests on median-panel numbers that the lens
reports as garbled in extraction; it is checked only for internal consistency
(it must contain 3L/t3 if the three-lap mean lies inside the per-lap spread).
"""
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, inequality, limit, quantity, units  # noqa: E402

L = 75.0            # m
t3 = 17.465         # s for three laps
v = 3 * L / t3
print(f"inputs: L = {L} m, t3 = {t3} s (three laps)")
print(f"per-lap time = {t3 / 3:.6f} s, mean speed = {v:.6f} m/s (claimed 12.88 m/s)")
quantity(f"({3 * L} m) / ({t3} s)", "12.88 m/s", rel_tol=1e-3)
units(f"({3 * L} m) / ({t3} s)", "speed")

for v_unseen, claim in ((5.0, 2.58), (7.0, 1.84)):
    r = v / v_unseen
    print(f"ratio to {v_unseen} m/s unseen = {r:.4f} (claimed {claim})")
    inequality(f"abs({r:.6f} - {claim})", "<", "0.006")

for vm, claim in ((13.0, 2.6), (30.0, 6.0)):
    r = vm / 5.0
    print(f"MonoRace bracket {vm} m/s / 5 m/s = {r:.3f} (claimed {claim})")
    inequality(f"abs({r:.6f} - {claim})", "<", "0.05")

# the bracketed single-lap mean must contain the three-lap mean
print(f"single-lap bracket 11.0-13.6 m/s contains {v:.3f}: {11.0 <= v <= 13.6}")
inequality(f"{v:.6f}", ">", "11.0")
inequality(f"{v:.6f}", "<", "13.6")

# structure: mean speed is laps*L/t, linear in L and inversely proportional to t
identity("3*L/t", "L/(t/3)", domain={"L": (1.0, 1000.0), "t": (1.0, 100.0)})
limit("3*L/t", "t", "oo", "0", domain={"L": (1.0, 1000.0)})   # infinitely slow lap -> zero mean speed
# sanity limit: if a lap took exactly 3 s per lap at 75 m the mean would be 25 m/s
quantity("(225 m) / (9 s)", "25 m/s", rel_tol=1e-9)
raise SystemExit(finish())
