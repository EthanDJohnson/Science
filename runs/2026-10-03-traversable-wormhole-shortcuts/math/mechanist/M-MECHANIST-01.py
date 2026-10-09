"""M-MECHANIST-01: shortcut and closed-causal-curve thresholds for a one-sided wormhole
whose mouth B clock lags exterior-synchronised time by Delta.

Model (built from definitions, not from the lens's script):
- flat 1+1 exterior, static mouths A at x = 0 and B at x = D (after the offset is built), exterior time t;
- mouth proper times: tau_A = t, tau_B = t - Delta (B lags);
- throat identification (MTY): a causal curve entering one mouth at mouth-clock reading tau exits
  the other at mouth-clock reading tau + T_w (T_w >= 0, the throat transit time in mouth proper time).
Units: any time unit; c = 1 so distances are light-times (D means D/c).
"""
import sys, itertools
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, sign, limit, finish

t0, Tw, D, Dl = sp.symbols("t0 T_w D Delta", real=True)

# B -> A through throat: enter B at exterior t0; B clock reads t0 - Delta; exit A at A reading t0 - Delta + Tw
arr_BA = (t0 - Dl + Tw) - t0
# A -> B through throat: enter A at t0 (A reads t0); exit B at B reading t0 + Tw => exterior t0 + Tw + Delta
arr_AB = (t0 + Tw + Dl) - t0
identity(arr_BA, Tw - Dl, domain={"t0": (-10, 10), "T_w": (0, 10), "D": (0.1, 10), "Delta": (-10, 10)})
identity(arr_AB, Tw + Dl, domain={"t0": (-10, 10), "T_w": (0, 10), "D": (0.1, 10), "Delta": (-10, 10)})

# Shortcut iff T_thru(B->A) < D  <=>  Delta > Tw - D
Dsc = sp.solve(sp.Eq(arr_BA, D), Dl)[0]
identity(Dsc, Tw - D, domain={"T_w": (0, 10), "D": (0.1, 10)})
# ratio T_thru/T_ext (finding 13)
identity(arr_BA / D, (Tw - Dl) / D, domain={"T_w": (0, 10), "D": (0.1, 10), "Delta": (-10, 10)})

# Closed causal loop: B->A through throat, then A->B through exterior (time D): net time shift
loop = arr_BA + D
Dctc = sp.solve(sp.Eq(loop, 0), Dl)[0]
identity(Dctc, Tw + D, domain={"T_w": (0, 10), "D": (0.1, 10)})
# difference of thresholds = 2D
identity(Dctc - Dsc, 2 * D, domain={"T_w": (0, 10), "D": (0.1, 10)})
# Limit: short throat Tw -> 0 gives Delta_ctc = D/c and shortcut at Delta = 0 (T_thru = 0 < D)
limit("T_w + D", "T_w", 0, "D")
sign(D - (Tw - 0) .subs(Tw, 0), "positive")   # at Tw=0, Delta=0: T_ext - T_thru = D > 0, so shortcut

# Brute force: every loop made of legs {throat B->A, throat A->B, exterior A->B, exterior B->A}
# that returns to its start mouth; the minimum net time shift must be (Tw - Delta) + D, i.e. the
# CTC condition is exactly Delta > Tw + D (no cheaper loop exists).
import random
random.seed(3)
bad = 0
for _ in range(2000):
    tw = random.uniform(0, 10); d = random.uniform(0.1, 10); dl = random.uniform(-25, 25)
    legs = {("B", "A", "throat"): tw - dl, ("A", "B", "throat"): tw + dl,
            ("A", "B", "ext"): d, ("B", "A", "ext"): d}
    best = None
    for n in range(1, 5):
        for seq in itertools.product(legs.keys(), repeat=n):
            ok = all(seq[i][1] == seq[i + 1][0] for i in range(n - 1)) and seq[-1][1] == seq[0][0]
            if not ok:
                continue
            shift = sum(legs[s] for s in seq) / 1.0
            # normalise per minimal cycle: a closed causal curve exists iff some cycle has shift <= 0
            best = shift if best is None else min(best, shift)
    has_ctc = best <= 0
    if has_ctc != (abs(dl) >= tw + d):   # either mouth may lag; the lens's convention is Delta > 0
        bad += 1
print(("PASS" if bad == 0 else "FAIL") + f" brute-force loop search: CTC exists iff |Delta| >= T_w + D/c ({bad} mismatches in 2000 random cases)")
if bad:
    from math_checks import RESULTS, Result
    RESULTS.append(Result("fail", "brute-force loop", "enumeration"))
else:
    from math_checks import RESULTS, Result
    RESULTS.append(Result("pass", "brute-force loop", "enumeration"))
raise SystemExit(finish())
