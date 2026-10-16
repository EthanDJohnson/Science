"""M-EMP-10. The measured sim-to-hardware speed discount and its geometric mean.

Claim (empiricist F10, base rates; load-bearing for EMP-C):
paired sim/hardware speeds give discount factors 1.89 (10.0 vs 5.3 m/s),
2.42 (19.4 vs 8 m/s) and 3.88 (19.4 vs 5 m/s), geometric mean 2.61.

Symbols: r_i = v_sim,i / v_real,i, dimensionless and > 1; the geometric mean is
(prod r_i)^(1/3). The three pairs are not independent (two share the 19.4 m/s
simulated number), which the lens states; that affects interpretation, not the
arithmetic checked here.
"""
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, inequality, limit, units  # noqa: E402

pairs = ((10.0, 5.3, 1.89), (19.4, 8.0, 2.42), (19.4, 5.0, 3.88))
ratios = []
for v_sim, v_real, claim in pairs:
    r = v_sim / v_real
    ratios.append(r)
    print(f"  {v_sim} m/s sim / {v_real} m/s real = {r:.4f} (claimed {claim})")
    inequality(f"abs({r:.6f} - {claim})", "<", "0.006")

prod = ratios[0] * ratios[1] * ratios[2]
gm = prod ** (1 / 3)
am = sum(ratios) / 3
hm = 3 / sum(1 / r for r in ratios)
print(f"product = {prod:.6f}; geometric mean = {gm:.6f} (claimed 2.61); "
      f"arithmetic {am:.4f}, harmonic {hm:.4f}")
inequality(f"abs({gm:.6f} - 2.61)", "<", "0.006")
# the mean must lie between the extreme ratios, and between harmonic and arithmetic means
inequality(f"{gm:.6f}", ">", f"{min(ratios):.6f}")
inequality(f"{gm:.6f}", "<", f"{max(ratios):.6f}")
inequality(f"{gm:.6f}", ">", f"{hm:.6f}")
inequality(f"{gm:.6f}", "<", f"{am:.6f}")
# the lens's "survives at roughly 40 per cent of its headline speed": 1/2.61
print(f"1/gm = {1 / gm:.4f} (claimed ~0.40)")
inequality(f"abs({1 / gm:.6f} - 0.40)", "<", "0.02")

identity("(a*b*c)**(1/3)", "exp((log(a)+log(b)+log(c))/3)",
         domain={"a": (0.5, 10.0), "b": (0.5, 10.0), "c": (0.5, 10.0)})
inequality("(a*b*c)**(1/3)", "<=", "(a+b+c)/3",
           domain={"a": (0.1, 10.0), "b": (0.1, 10.0), "c": (0.1, 10.0)})   # AM-GM
limit("(a*a*a)**(1/3)", "a", 2.61, "2.61")     # equal ratios -> the ratio itself
units("(19.4 m/s) / (5 m/s)", "dimensionless")
raise SystemExit(finish())
