"""M-MECHANIST-06 (F12): UCNtau ratios. A small extra constant loss rate l shifts the fitted
lifetime by dtau = tau - 1/(1/tau + l) ~ tau^2 l. Depolarisation bound 1.0e-7 s^-1 (D-quoted);
gas correction +0.11 s. A constant loss is degenerate with decay: N0 exp(-(G + l) t) depends on G + l only. SI."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, series, quantity, units, finish

tau = 877.82
lam = 1 / 877.82 - 1 / 887.97
ratio_dp = lam / 1.0e-7
l_gas = 1 / (tau - 0.11) - 1 / tau          # exact: tau_obs = tau - 0.11 corrected up by 0.11
l_gas_lin = 0.11 / tau**2
print(f"needed/depol bound = {ratio_dp:.1f}; gas rate exact {l_gas:.4e}, linear {l_gas_lin:.4e} s^-1; ratio {lam/l_gas:.1f}")
quantity(f"{ratio_dp}", "130", rel_tol=0.01)
quantity(f"{l_gas} Hz", "1.4e-7 Hz", rel_tol=0.03)
quantity(f"{lam/l_gas}", "90", rel_tol=0.03)
units("0.11 s / (877.82 s)^2", "Hz")
t_, g, l, N0 = sp.symbols("t g l N0", positive=True)
identity(N0 * sp.exp(-g * t_) * sp.exp(-l * t_), N0 * sp.exp(-(g + l) * t_))
series("tau - 1/(1/tau + l)", "l", 0, 2, "tau**2*l")
raise SystemExit(finish())
