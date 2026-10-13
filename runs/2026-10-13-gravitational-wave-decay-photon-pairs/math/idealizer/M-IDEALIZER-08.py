"""M-IDEALIZER-08: cumulative yield beyond x0, R(>x0) = (5/6) Int_{x0}^inf f(x)/x^2 dx (F6, F14), with f from
the M-IDEALIZER-07 toy (own implementation). Natural units, k = w = 1. Exact f is integrated up to x = 2000;
beyond, the exact asymptotes are used: outgoing f = A_m x^-2 (A from x = 1e5), standing <f> = 3 Int P^4 dOmega / L^2.
Also the large-x analytic standing plateau: TT -> 4 P^4 (sin^4 x + cos^4 x)/x^4, x-average 3 P^4/x^4.
"""
import sys, importlib.util
sys.path.insert(0, ".claude/skills/conundrum/scripts")
spec = importlib.util.spec_from_file_location("toy", "runs/2026-10-13-gravitational-wave-decay-photon-pairs/math/idealizer/M-IDEALIZER-07.py")
toy = importlib.util.module_from_spec(spec); spec.loader.exec_module(toy)
from math_checks import identity, quantity, finish
import mpmath as mp
import sympy as sp

toy.mp.mp.dps = 18; mp.mp.dps = 18
# analytic plateau for m = 2 (P = sin^2): 3 Int P^4 / (Int P^2 / 2)^2
u = sp.symbols("u", real=True)
IP4 = 2 * sp.pi * sp.integrate((1 - u**2)**4, (u, -1, 1)); IP2 = 2 * sp.pi * sp.integrate((1 - u**2)**2, (u, -1, 1))
plateau = sp.nsimplify(3 * IP4 / (IP2 / 2)**2)
print("standing plateau (x-averaged) =", plateau, float(plateau), " range", float(2 * IP4 / (IP2 / 2)**2), "to", float(4 * IP4 / (IP2 / 2)**2))
avg_num = mp.quad(lambda x: toy.f(x, 2, "st"), mp.linspace(3000, 3000 + 4 * mp.pi, 5)) / (4 * mp.pi)
quantity(f"{avg_num}", f"{float(plateau)}", rel_tol=2e-3)

def R(x0, m, kind, xmax=None):
    xmax = 2000 if kind == "out" else 200
    grid = [mp.mpf(v) for v in ([1, 1.5, 2, 3, 4, 6, 10, 20, 50, 100, 300, 1000, 2000] if kind == "out" else list(mp.linspace(1, 200, 128)))]
    pts = [x0] + [x for x in grid if x > x0]
    body = mp.quad(lambda x: toy.f(x, m, kind) / x**2, pts, method="gauss-legendre", maxdegree=4) if x0 < xmax else 0
    start = max(x0, xmax)
    if kind == "out":
        A = toy.f(1e5, m, "out") * mp.mpf(1e5)**2
        tail = A / (3 * start**3)
    else:
        tail = mp.mpf(float(plateau)) / start
    return mp.mpf(5) / 6 * (body + tail)

lens = {(2, "out"): [6.910e-2, 2.666e-4, 6.193e-8, 5.551e-14, 4.879e-19],
        (0, "out"): [1.364e-1, 4.609e-4, 8.763e-8, 5.629e-14, 3.745e-19],
        (2, "st"): [1.008, 1.605e-1, 1.008e-2, 1.008e-4, 2.145e-6]}
for key, lv in lens.items():
    for x0, l in zip([1, 2 * mp.pi, 100, 1e4, 4.7e5], lv):
        r = R(mp.mpf(x0), *key)
        print(f"{key} x0 = {mp.nstr(x0, 4)}: R = {mp.nstr(r, 4)}  (lens {l:.3e}, ratio lens/mine {l/float(r):.3f})")
for m in (2, 0):
    A = toy.f(1e5, m, "out") * mp.mpf(1e5)**2
    print(f"m={m}: exact far-zone law R(>x) -> {mp.nstr(5 * A / 18, 4)} x^-3; F8 uses 0.069 x^-3")
# limit/consistency: R(>x0) for outgoing at large x0 approaches the analytic law
quantity(f"{R(mp.mpf(1e4), 2, 'out')}", f"{5 * toy.f(1e5, 2, 'out') * 1e10 / 18 / 1e12}", rel_tol=1e-3)
raise SystemExit(finish())
