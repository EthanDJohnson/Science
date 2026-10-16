"""M-DIAL-10. Arithmetic of the seen-versus-unseen speed ratios and the aero cost percentages.

Claims checked (lens finding 1, contradiction 2, finding 8 / DIAL-D):
 (a) 27.8-32.2 m/s on a seen track against 5-10 m/s in unseen clutter is "a factor of 3-6".
 (b) The observed seen:unseen ratio is "2.57-3.22" and the S2 bound is therefore "slack by ~2.6x"
     on the gate track.
 (c) The RL policy pays "~4 per cent of lap time (5.14 s RL vs 4.92 s nominal-model tracking)".
 (d) A limit worth 2.00-2.68 per cent of traversal time cannot explain a factor of 3-6.

These are arithmetic on quoted literature values, not derivations; only the arithmetic is checked.
Units: m/s for speeds, s for lap times, dimensionless ratios.
"""
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, quantity, units, inequality, finish  # noqa: E402

seen = (27.8, 32.2)
unseen = (5.0, 10.0)
ratios = [hi / lo for hi in seen for lo in unseen]
print(f"seen {seen} m/s, unseen {unseen} m/s")
print(f"  full ratio range: {min(ratios):.3f} to {max(ratios):.3f}  (lens: 'a factor of 3-6')")
print(f"  ratio to the 10 m/s end only: {seen[0]/10:.3f} to {seen[1]/10:.3f} "
      "(lens quotes 'observed 2.57-3.22'; the upper end matches 32.2/10 = 3.22, "
      "the lower end 2.57 is not reproducible from any stated pair; 27.8/10 = 2.78)")
for x in (2.57, 2.78, 3.22):
    print(f"    speed implied by ratio {x} against 10 m/s: {10*x:.1f} m/s")

print("S2 slack on the gate track = predicted ratio / observed ratio:")
for pred in (6.696, 8.50):
    for obs in (2.57, 2.78, 3.22):
        print(f"  predicted {pred:.3f} / observed {obs:.2f} = {pred/obs:.3f}")
print("  (the lens's '~2.6x slack' needs predicted 8.5 with observed 3.22, or predicted 6.70 with "
      "observed 2.57; with its own stated L = 10.71 m and observed 3.22 the slack is 2.08x)")

rl, nominal = 5.14, 4.92
print(f"RL lap {rl} s vs nominal-model tracking {nominal} s: "
      f"{100*(rl/nominal - 1):.3f} per cent slower (lens: ~4 per cent)")
print(f"aero model-fidelity penalty 2.00-2.68 per cent of traversal time corresponds to a speed "
      f"factor {1/(1-0.0268):.4f}-{1/(1-0.0200):.4f}, far below the "
      f"{min(ratios):.2f}-{max(ratios):.2f} seen/unseen factor")

quantity("(5.14 s - 4.92 s)/(4.92 s)*100", "4.47", rel_tol=1e-3)
quantity("27.8 m/s / (10 m/s)", "2.78", rel_tol=1e-3)
inequality("1/(1 - 268/10000)", "<", "2.78", domain={})
quantity("32.2 m/s / (10 m/s)", "3.22", rel_tol=1e-3)
quantity("(13.6 m/0.040 s)/(4 m/0.100 s)", "8.50", rel_tol=1e-3)
quantity("(10.7142857 m/0.040 s)/(4 m/0.100 s)", "6.696", rel_tol=1e-3)
units("32.2 m/s / (10 m/s)", "dimensionless")

raise SystemExit(finish())
