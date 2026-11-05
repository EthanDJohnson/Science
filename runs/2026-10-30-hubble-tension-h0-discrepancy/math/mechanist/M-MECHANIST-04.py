"""M-MECHANIST-04: partial levers in mag (findings 4, 6, 3).
Δm = 5 log10(H_before/H_after). Wojtak & Hjorth: 73.04 -> 70.59 / 71.45 / 70.5 [D-35];
Percival -1.4, -1.0, -2.6 km/s/Mpc [D-88] (base not stated by the lens: try 73.04 and 73.264);
Pantheon+ vs CSP: +2 vs +0.8 -> 1.2 km/s/Mpc [D-25]; Dong 74.30 -> 71.37 [D-82].
Environment: offset = γ_env Δf, γ_env = 0.17 mag [Ginolin], Δf = 0.5 ASSUMED; Δf needed = gap/γ_env.
Naive sum = W&H conservative + Percival cut-off + Dong.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/mechanist")
import sympy as sp
from math_checks import identity, inequality, finish
from mm_common import dmag, near

gap = dmag(73.264, 67.19)
for after, claim in [(70.59, 0.074), (71.45, 0.048), (70.5, 0.077)]:
    near(f"W&H 73.04->{after}", dmag(73.04, after), claim, 0.0008)
near("W&H frac low", dmag(73.04, 71.45) / gap, 0.25, 0.006)
near("W&H frac high", dmag(73.04, 70.5) / gap, 0.41, 0.006)
for base in (73.04, 73.264):
    print(f"Percival base {base}")
    near("cut-off -1.4", dmag(base, base - 1.4), 0.042, 0.0008)
    near("prior -1.0", dmag(base, base - 1.0), 0.030, 0.0008)
    near("all -2.6", dmag(base, base - 2.6), 0.078, 0.0012)
    near("all -2.6 frac", dmag(base, base - 2.6) / gap, 0.42, 0.01)
for base in (68.8, 70.0, 73.0):
    near(f"compilation 1.2 at base {base}", dmag(base + 1.2, base), 0.038, 0.002)
dong = dmag(74.30, 71.37)
near("Dong mag", dong, 0.087, 0.0008)
near("Dong frac", dong / gap, 0.46, 0.006)
s = dmag(73.04, 71.45) + dmag(73.04, 73.04 - 1.4) + dong
near("naive sum mag", s, 0.177, 0.001)
near("naive sum frac", s / gap, 0.94, 0.01)
# Environment step
g, f = sp.symbols("g f", positive=True)
identity(sp.diff(g * f, f), g)
near("env offset 0.17*0.5", 0.17 * 0.5, 0.085, 1e-12)
near("env frac", 0.085 / gap, 0.45, 0.005)
inequality(f"{gap!r}/0.17", ">", "1")   # full gap needs Δf > 1 (impossible as a fraction difference)
raise SystemExit(finish())
