"""M-EXAMINER-09 (F7, cand B): how much of a MOND-boosted bound population a v~ <= sqrt(2) cut removes.
Noise-free Kepler orbits with G -> gamma G (constant gamma, the lens's one-body approximation), f(e) ∝ e^1.3,
selection weight (s/a)^0.6 (dN/da ∝ a^-1.6), v~ = v_p / sqrt(G M / s) with the true mass (dimensionless).
Under Newton (gamma = 1) the cut removes nothing (bound: v~ <= sqrt(2)); with gamma it removes P(v~_N > sqrt(2/gamma)).
Also the El-Badry bound v~ <= sqrt(5/M_est) with M_est = 0.93 Msun: removes nothing noise-free if sqrt(2 gamma) < sqrt(5/0.93).
Lens (with DR3 noise and the chae2024 preset over 5-30 kau): sqrt(2) cut removes 0.68% (Newton) and 2.05% (MOND).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from math_checks import inequality, identity, limit, finish

rng = np.random.default_rng(11)
N = 2_000_000
e = rng.random(N) ** (1 / 2.3)
Mm = rng.random(N) * 2 * np.pi
E = Mm.copy()
for _ in range(60):
    E = E - (E - e * np.sin(E) - Mm) / (1 - e * np.cos(E))
r = 1 - e * np.cos(E)
f = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
pos = np.stack([r * np.cos(f), r * np.sin(f), np.zeros(N)], 1)
vel = np.sqrt(1 / (1 - e**2))[:, None] * np.stack([-np.sin(f), e + np.cos(f), np.zeros(N)], 1)
n = rng.normal(size=(N, 3)); n /= np.linalg.norm(n, axis=1)[:, None]
s = np.linalg.norm(pos - (pos * n).sum(1)[:, None] * n, axis=1)
vp = np.linalg.norm(vel - (vel * n).sum(1)[:, None] * n, axis=1)
vtN = vp * np.sqrt(s)
w = s ** 0.6
inequality(sp.Float(float(vtN.max())), "<=", sp.sqrt(2))
for g in (1.0, 1.22, 1.276, 1.333, 1.367):
    frac = w[vtN * np.sqrt(g) > np.sqrt(2)].sum() / w.sum()
    print(f"gamma = {g}: fraction above sqrt(2) = {100*frac:.3f}%")
frac133 = w[vtN * np.sqrt(1.333) > np.sqrt(2)].sum() / w.sum()
inequality(sp.Float(frac133), "<", sp.Float(0.03))          # ~2% scale: the cut removes only a few per cent
inequality(sp.Float(np.sqrt(2 * 1.37)), "<", sp.sqrt(sp.Rational(500, 93)))   # El-Badry bound removes 0 noise-free
g = sp.symbols("g", positive=True)
limit(sp.sqrt(2 / g), "g", 1, "sqrt(2)")      # gamma -> 1: threshold returns to the Newtonian bound
raise SystemExit(finish())
