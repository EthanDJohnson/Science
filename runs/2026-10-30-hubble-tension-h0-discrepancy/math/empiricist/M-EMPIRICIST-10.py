"""M-EMPIRICIST-10: two-sided tail probabilities P(|X| > n) for a standard Gaussian and unit-scale Student t.
Student t (ν dof): P(|T| > t) = I_{ν/(ν+t^2)}(ν/2, 1/2) (regularised incomplete beta). Closed forms used as
limits: ν = 1 (Cauchy) 1 - (2/π) atan t; ν = 2: 1 - t/sqrt(2 + t^2); ν -> ∞ tends to the Gaussian erfc(t/√2).
Claims (table, F11): n = 6.27: Gauss 3.6e-10, t2 0.025, t3 0.008, t4 0.003; n = 3.24: 0.0012, 0.08, 0.05, 0.03.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/empiricist")
import mpmath as mp
from math_checks import identity, finish
from _common import cmp

mp.mp.dps = 30


def t_tail(t, nu):
    nu, t = mp.mpf(nu), mp.mpf(t)
    return mp.betainc(nu / 2, mp.mpf(1) / 2, 0, nu / (nu + t**2), regularized=True)


# limits/closed forms the general formula must reduce to
t0 = mp.mpf("3.24")
identity(str(t_tail(t0, 1)), str(1 - 2 / mp.pi * mp.atan(t0)))
identity(str(t_tail(t0, 2)), str(1 - t0 / mp.sqrt(2 + t0**2)))
big = t_tail(t0, 10**8)
print(f"  ν = 1e8 tail at 3.24: {mp.nstr(big, 8)}, Gaussian {mp.nstr(mp.erfc(t0 / mp.sqrt(2)), 8)}")
cmp("large-ν limit equals Gaussian", float(big), float(mp.erfc(t0 / mp.sqrt(2))), 1e-8)

table = {6.27: (3.6e-10, 0.025, 0.008, 0.003), 3.24: (0.0012, 0.08, 0.05, 0.03)}
for n, (g, a2, a3, a4) in table.items():
    G = float(mp.erfc(mp.mpf(n) / mp.sqrt(2)))
    cmp(f"Gaussian two-sided at {n}", G, g, abs(g) * 0.05)
    for nu, q in ((2, a2), (3, a3), (4, a4)):
        v = float(t_tail(n, nu))
        # tolerance: half a unit in the lens's last printed digit
        last = 10 ** (len(repr(q).split(".")[1]) * -1) / 2 if "e" not in repr(q) else q * 0.05
        cmp(f"t ν={nu} two-sided at {n}", v, q, last + 1e-12)
raise SystemExit(finish())
