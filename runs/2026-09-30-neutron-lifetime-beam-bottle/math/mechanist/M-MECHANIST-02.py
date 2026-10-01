"""M-MECHANIST-02 (F3, O3 row 1): BL1 tau = L * Ndot_alpha * eps_p / (Ndot_p * eps_0 * v0).
If the true monitor efficiency is eps0_t and the assumed eps0_a, tau_meas/tau_true = eps0_t/eps0_a.
If a fraction f of protons is lost (not in eps_p), Ndot_p,meas = (1-f) Ndot_p,true and tau_meas = tau_true/(1-f).
Lifetimes in s (SI)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, quantity, finish

L, Na, ep, Np, e0, v0, f, k = sp.symbols("L N_a e_p N_p e_0 v_0 f k", positive=True)
tau = L * Na * ep / (Np * e0 * v0)
# scaling: tau is linear in eps_p and inversely in eps_0
identity(sp.diff(tau, ep) * ep, tau)
identity(sp.diff(tau, e0) * e0, -tau)
# length-independent end loss cancels in the slope d(Np)/dL if Np = a*L + b
a, b = sp.symbols("a b", positive=True)
identity(sp.diff(a * L + b, L), a)
# proton loss fraction f: tau_meas/tau_true = 1/(1-f); small-f limit
limit((1 / (1 - f) - 1) / f, "f", 0, 1)

beam, ucn = 887.97, 877.82
r = beam / ucn
f_need = 1 - ucn / beam
print(f"eps0_true/eps0_assumed needed = {r:.6f} -> +{(r-1)*100:.3f} %")
print(f"proton loss fraction needed = {f_need*100:.4f} %")
quantity(f"{r-1}", "0.0116", rel_tol=5e-3)
quantity(f"{f_need}", "0.01143", rel_tol=1e-3)
# BL1 alone (887.7)
print(f"BL1-alone: eps0 +{(887.7/ucn-1)*100:.3f} %, loss {(1-ucn/887.7)*100:.3f} %")
raise SystemExit(finish())
