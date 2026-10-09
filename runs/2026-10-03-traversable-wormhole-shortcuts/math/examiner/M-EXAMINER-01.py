"""M-EXAMINER-01: shortcut and CTC thresholds on the throat time shift Delta.

Model (independent): two static mouths A, B; exterior-synchronised static clocks; exterior light
time between the observers D/c (=: X). Through the throat, coordinate transit T_w measured in the
local static time, and the throat identifies local time t at A with t + Delta at B.
Edges (time increments on the synchronised clocks):
  A->B throat: T_w + Delta ;  B->A throat: T_w - Delta ;  A->B or B->A exterior: X.
Earliest arrival A->B = min(X, T_w + Delta); shortcut A->B iff T_w + Delta < X.
Closed causal loop iff some cycle has total increment < 0 (brute force over all simple cycles).
Units: years (SI-derived, Julian year; 1 ly / c = 1 yr).
"""
import sys, random, itertools
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, inequality, sign, limit, quantity, finish
import math

def edges(Tw, X, Dl):
    return {("A", "B"): [Tw + Dl, X], ("B", "A"): [Tw - Dl, X]}

def ctc_bruteforce(Tw, X, Dl):
    e = edges(Tw, X, Dl)
    # simple cycles on 2 nodes: one A->B edge plus one B->A edge
    return any(a + b < 0 for a in e[("A", "B")] for b in e[("B", "A")])

def shortcut_AB(Tw, X, Dl):
    return (Tw + Dl) < X

rng = random.Random(7)
bad_short = bad_ctc = bad_window = 0
for _ in range(200000):
    X = 10 ** rng.uniform(-3, 4)
    Tw = 10 ** rng.uniform(-9, 5)
    Dl = rng.uniform(-3, 3) * (Tw + X)
    # lens: A->B shortcut iff Delta < X - T_w
    if shortcut_AB(Tw, X, Dl) != (Dl < X - Tw):
        bad_short += 1
    # lens: CTC iff |Delta| > T_w + X
    if ctc_bruteforce(Tw, X, Dl) != (abs(Dl) > Tw + X):
        bad_ctc += 1
print("mismatches shortcut rule:", bad_short, " CTC rule:", bad_ctc)
identity(str(bad_short), "0")
identity(str(bad_ctc), "0")

# Window: A->B shortcut and no CTC  <=>  -(T_w+X) <= Delta < X - T_w ; width = 2X
identity("(X - T_w) - (-(T_w + X))", "2*X")
# The window is nonempty for every T_w (even T_w >> X): its width 2X > 0
sign("2*X", "positive")
# Limit: at Delta = 0 a long wormhole (T_w > X) is not a shortcut, and Delta = 0 never gives CTCs
inequality("T_w + 0", ">", "X", domain={"T_w": (5, 10), "X": (0.1, 4.9)})
inequality("T_w + X", ">", "0")
# Limit T_w -> 0 (instant throat): shortcut threshold -> X (any |Delta| < X keeps a shortcut A->B)
limit("X - T_w", "T_w", 0, "X")

# MM numbers: T_w = pi*l/c with l = 3e3 ly -> T_w = 3000*pi yr; d = l -> X = 3000 yr
Tw = 3000 * math.pi
for X, lens_short, lens_ctc in [(3000.0, -6.4248e3, 1.2425e4), (30.0, -9.3948e3, 9.4548e3)]:
    print(f"X={X} yr: shortcut needs Delta < {X - Tw:.6g} yr ; CTC needs |Delta| > {Tw + X:.6g} yr")
    quantity(f"{X - Tw} yr", f"{lens_short} yr", rel_tol=2e-4)
    quantity(f"{Tw + X} yr", f"{lens_ctc} yr", rel_tol=2e-4)
# Ellis at D = 1 ly: T_w = 6.64e-8 s, X ~ 1 yr: shortcut iff Delta < ~1 yr, CTC iff |Delta| > ~1 yr
TwE = 6.6378e-8 / (365.25 * 86400)
print("Ellis 1 ly: shortcut-without-CTC window for Delta:", -(TwE + 1), "to", 1 - TwE, "yr")
quantity(f"{1 - TwE} yr", "1 yr", rel_tol=1e-6)
quantity("3000 ly / c", "3000 yr", rel_tol=1e-6)
raise SystemExit(finish())
