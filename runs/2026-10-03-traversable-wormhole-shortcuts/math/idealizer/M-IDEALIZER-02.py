"""M-IDEALIZER-02: unaligned gluing (m = O n != n) leaves no achronal complete through-ray, even at L = 0.

Same independent model as M-IDEALIZER-01 (c = 1, point mouths A = 0, B = D, throat light-time L).
Incoming P1(s1) = (-s1, -n s1), outgoing P2(s2) = (L + s2, D + m s2).
Exterior-only margin for the pair: L + s1 + s2 - |D + n s1 + m s2|.
With s1 = s2 = S: margin >= L + (2 - |n + m|) S - |D|, and |n + m| < 2 whenever m != n (unit vectors),
so the margin -> +oo: chronal for every L >= 0 and every D.
Mirror gluing m = -n: margin = L + 2S - |D|.
"""
import sys
import random
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
import numpy as np
from math_checks import identity, limit, sign, inequality, finish

S, L, Dm = sp.symbols("S L Dm", positive=True)
th = sp.symbols("theta", positive=True)   # angle between n and m, 0 < theta <= pi
# |n + m| = 2 cos(theta/2) < 2 for theta > 0
lower = L + (2 - 2 * sp.cos(th / 2)) * S - Dm
limit(lower, "S", "oo", sp.oo, domain={"theta": (0.01, 3.14159), "L": (0, 10), "Dm": (0, 10)})
sign(2 - 2 * sp.cos(th / 2), "positive", domain={"theta": (0.001, 3.14159)})
# mirror gluing exactly: margin = L + 2S - |D|; at L = 0, d = 1 m, S = 400 m it is +799 m
identity(lower.subs(th, sp.pi), L + 2 * S - Dm)
margin_num = (L + 2 * S - Dm).subs({L: 0, S: 400, Dm: 1})
print("mirror gluing, L = 0, d = 1 m, S = 400 m: margin =", margin_num, "m")
identity(margin_num, 799)


# numeric: random unaligned gluings, exact exterior margin at large S
def margin(Dv, n, m, Lv, s):
    return Lv + 2 * s - np.linalg.norm(Dv + n * s + m * s)


rng = random.Random(3)
chronal = 0
trials = 200
for _ in range(trials):
    Dv = np.array([rng.uniform(-2, 2) for _ in range(3)])
    v = np.array([rng.gauss(0, 1) for _ in range(3)]); n = v / np.linalg.norm(v)
    w = np.array([rng.gauss(0, 1) for _ in range(3)]); m = w / np.linalg.norm(w)
    if margin(Dv, n, m, 0.0, 1e6) > 0:
        chronal += 1
print(f"random unaligned gluings chronal at L = 0: {chronal}/{trials}")
sign(sp.Integer(1 if chronal == trials else -1), "positive")

# rotated gluing about axis k by angle alpha: m = n only for n parallel to k
alpha = 1.0
k = np.array([0, 0, 1.0])
def rot(v):
    return (v * np.cos(alpha) + np.cross(k, v) * np.sin(alpha) + k * (k @ v) * (1 - np.cos(alpha)))
on_axis = rot(k)
print("rotation leaves the axis fixed:", np.allclose(on_axis, k))
sign(sp.Integer(1 if np.allclose(on_axis, k) else -1), "positive")
raise SystemExit(finish())
