"""M-DECOMPOSER-02: ratio of CTC lag to shortcut lag, (L+d)/(L-d), at L = pi d and L = 10 d."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, finish

L, d = sp.symbols("L d", positive=True)
k = sp.symbols("k", positive=True)  # L = k d, k > 1 (long throat)
ratio = ((L + d) / (L - d)).subs(L, k * d)
identity(ratio, (k + 1) / (k - 1), domain={"k": (1.01, 100), "d": (0.1, 10)})
r_pi = float(ratio.subs(k, sp.pi))
r_10 = float(ratio.subs(k, 10))
print(f"ratio at L = pi d: {r_pi:.4f}; at L = 10 d: {r_10:.4f}")
quantity(f"{r_pi}", "1.93", rel_tol=3e-3)
quantity(f"{r_10}", "1.22", rel_tol=3e-3)
# long-throat limit: thresholds converge (ratio -> 1); marginal throat k -> 1+: ratio diverges
limit((k + 1) / (k - 1), "k", sp.oo, 1)
limit((k - 1) / (k + 1), "k", 1, 0)  # inverse ratio -> 0 as the throat length approaches d
raise SystemExit(finish())
