"""M-MECHANIST-08: does calibration remove the triple bias? Lens claims (F6, verdict, cand A, F):
'Chae-style calibration removes the triple bias to ≤ +0.03' and 'premise 2 holds to ≲ 0.03 in γ for triples';
verdict: 'E1b/E1c within −0.06 to +0.03' while 'E2a +0.11 to +0.15 relative to its f = 0 value'.
Statement checked: for each estimator X, the triple-induced shift Δ_X(f) = γ_X(f) − γ_X(0) (same yardstick the lens uses for E2a),
the deviation from truth γ_X(f) − 1, and the slope Δ_X / residual fraction, from the lens's Newtonian grid rows (γ_inj = 1).
Bootstrap ±0.01–0.03 per entry (lens), so a difference of two entries has σ ≈ 0.014–0.04."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import inequality, quantity, finish
cols = ["E1a", "E1b", "E1c", "E2a", "E2b", "E3", "E4"]
N = {0: [0.989, 0.938, 0.912, 0.971, 0.983, 0.971, 0.973], .1: [1.042, 0.994, 0.971, 1.037, 1.045, 1.003, 1.038],
     .2: [1.084, 1.012, 0.985, 1.081, 1.107, 1.027, 1.120], .3: [1.141, 1.028, 1.006, 1.123, 1.165, 1.046, 1.164]}
resid = {.1: 0.050, .2: 0.101, .3: 0.165}
print("estimator | shift vs own f=0 (f=.1,.2,.3) | deviation from truth (f=0..0.3) | slope per unit residual (f=.3)")
sh = {}
for i, c in enumerate(cols):
    d = [N[f][i] - N[0][i] for f in (.1, .2, .3)]; dev = [N[f][i] - 1 for f in (0, .1, .2, .3)]
    sh[c] = d
    print(f"{c:4s} | {d[0]:+.3f} {d[1]:+.3f} {d[2]:+.3f} | {dev[0]:+.3f} {dev[1]:+.3f} {dev[2]:+.3f} {dev[3]:+.3f} | {d[2]/0.165:.2f}")
# The lens's '≤ +0.03' holds against truth:
inequality(f"{max(N[f][1] for f in N) - 1}", "<=", "0.03")
# ... but the triple-induced shift of the calibrated estimators, on the E2a yardstick, is 0.056–0.094 (> 0.03 by > 2σ of a difference)
for c in ("E1b", "E1c"):
    inequality(f"{sh[c][2]}", "<=", "0.03")      # expected FAIL: the claim '≲ 0.03 for triples' as a shift
# verdict range 'E1b/E1c within −0.06 to +0.03' vs truth
inequality(f"{min(N[0][1], N[0][2]) - 1}", ">=", "-0.06")   # expected FAIL: E1c at f=0 is −0.088
# share of the uncalibrated shift that calibration removes, at f = 0.3
for c in ("E1b", "E1c", "E3"):
    print(f"{c}: shift at f=0.3 is {sh[c][2]/sh['E1a'][2]:.2f} of E1a's and {sh[c][2]/sh['E2a'][2]:.2f} of E2a's")
# consequence for F9's budget: Chae−Boufourou gap 0.32; with calibrated triple share up to +0.09 instead of +0.03,
# the extra needed from unbound pairs at +1.54 per unit fraction:
for trip in (0.03, 0.09):
    print(f"triple share {trip}: remaining {0.32 - trip:.2f} -> unbound fraction {(0.32 - trip)/1.54:.3f}")
raise SystemExit(finish())
