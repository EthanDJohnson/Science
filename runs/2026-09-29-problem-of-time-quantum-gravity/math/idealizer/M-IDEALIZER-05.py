"""M-IDEALIZER-05 (F5): clock resolution. Clock states |t> = d^-1/2 sum_n e^{-i E_n t}|n>, E_n = n + const (unit spacing, period T = 2 pi s).
|<0|t>| = |sin(d t/2) / (d sin(t/2))|. t_half := first t with |<0|t>| = 1/2 (amplitude, not probability).
Claim: t_half = 0.970, 0.477, 0.237, 0.1185, 0.0592 for d = 4, 8, 16, 32, 64; t_half*d -> 3.8 (large-d limit 2 u*, sin u*/u* = 1/2).
POVM (d/2pi) int_0^{2pi} |t><t| dt = 1.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import mpmath as mp
from math_checks import quantity, identity, limit, finish

amp = lambda t, d: abs(np.sin(d * t / 2) / (d * np.sin(t / 2)))
claimed = {4: 0.970, 8: 0.477, 16: 0.237, 32: 0.1185, 64: 0.0592}
for d, want in claimed.items():
    th = float(mp.findroot(lambda t: mp.sin(d * t / 2) / (d * mp.sin(t / 2)) - 0.5, 1.9 / d * 2))
    # cross-check with direct sum
    ov = abs(np.sum(np.exp(-1j * np.arange(d) * th)) / d)
    print(f"d={d}: t_half={th:.5f}, direct |<0|t>|={ov:.6f}, t_half*d={th*d:.4f}, prob-half would give t={float(mp.findroot(lambda t: (mp.sin(d*t/2)/(d*mp.sin(t/2)))**2-0.5, 1.4/d*2)):.4f}")
    quantity(f"{th}", f"{want}", rel_tol=0.01)
# large-d limit: sin(u)/u = 1/2 -> u*, t_half*d -> 2u*
u = float(mp.findroot(lambda u: mp.sin(u) / u - 0.5, 1.9))
print("large-d t_half*d =", 2 * u)
quantity(f"{2*u}", "3.8", rel_tol=0.01)
limit("sin(d*x/(2*d))/(d*sin(x/(2*d)))", "d", "oo", "sin(x/2)/(x/2)")
# POVM resolution of identity
for d in (4, 8, 16):
    ts = np.linspace(0, 2 * np.pi, 4001)[:-1]
    S = sum(np.outer(np.exp(-1j * np.arange(d) * t), np.exp(1j * np.arange(d) * t)) / d for t in ts) * (d / (2 * np.pi)) * (2 * np.pi / len(ts))
    dev = np.linalg.norm(S - np.eye(d))
    print(f"d={d}: POVM defect {dev:.2e}")
    quantity(f"{1 + dev}", "1", rel_tol=1e-12)
raise SystemExit(finish())
