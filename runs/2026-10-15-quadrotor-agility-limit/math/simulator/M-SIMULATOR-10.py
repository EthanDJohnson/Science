#!/usr/bin/env python3
"""M-SIMULATOR-10: the t_opt-fraction column of the results tables, and the Wilson interval.

CLAIMS.
(a) every row of the lens's closed-loop table satisfies mean path speed = S/t with
    S = 98.315 m and fraction of the time optimum = t_opt/t with t_opt = 4.5020 s;
(b) the failure-boundary row "baseline closed loop at U = 12 m/s (mean 13.053 m/s, 72 per
    cent of t_opt)";
(c) 30 successes out of 30 give a Wilson 95 per cent interval [0.886, 1.000].

SYMBOLS / DOMAIN. t > 0 s completion time; S = 98.315 m path length; t_opt = 4.5020 s;
fraction = t_opt/t in (0, 1]; n = 30 trials, k = 30 successes, z = 1.959964 for 95 per cent.

INDEPENDENT DERIVATION. Arithmetic, and the Wilson score interval
(p + z^2/2n +/- z sqrt(p(1-p)/n + z^2/4n^2)) / (1 + z^2/n) with p = k/n.
"""
import sys
from math import sqrt

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, inequality, quantity  # noqa: E402

S, T_OPT = 98.315, 4.5020
rows = [
    ("baseline, 1.5 m gate", 5.018, 19.592, 0.897),
    ("baseline, 0.9 m gate", 6.082, 16.165, 0.740),
    ("motor_tau 10 ms", 4.950, 19.862, 0.909),
    ("motor_tau 78.2 ms", 12.360, 7.954, 0.364),
    ("tau_vio 5 ms", 5.204, 18.892, 0.865),
    ("tau_vio 130 ms", 9.274, 10.601, 0.485),
    ("aero removed", 10.122, 9.713, 0.445),
    ("thrust 6 N/rotor", 5.838, 16.840, 0.771),
    ("time-optimal profile alpha = 0.10", 14.235, None, None),
]
print("=== (a) mean path speed and t_opt fraction, row by row ===")
worst_v, worst_f = 0.0, 0.0
for name, t, v_claim, f_claim in rows:
    v = S / t
    f = T_OPT / t
    dv = "--" if v_claim is None else f"{100*abs(v-v_claim)/v_claim:.3f} per cent"
    df = "--" if f_claim is None else f"{100*abs(f-f_claim)/f_claim:.3f} per cent"
    if v_claim:
        worst_v = max(worst_v, abs(v - v_claim) / v_claim)
    if f_claim:
        worst_f = max(worst_f, abs(f - f_claim) / f_claim)
    print(f"  {name:<34s}: t = {t:7.3f} s -> S/t = {v:7.3f} m/s (claim {v_claim}, off by {dv}); "
          f"t_opt/t = {f:.4f} (claim {f_claim}, off by {df})")
print(f"  worst relative discrepancy: speeds {100*worst_v:.3f} per cent, "
      f"fractions {100*worst_f:.3f} per cent")

print("\n=== (b) the U = 12 m/s failure-boundary row ===")
v12 = 13.053
t12 = S / v12
print(f"  mean 13.053 m/s -> t = S/v = {t12:.4f} s -> t_opt/t = {T_OPT/t12:.4f} "
       "(i.e. 59.8 per cent, not 72 per cent)")
print(f"  13.053/21.838 (mean-speed ratio to the optimum) = {13.053/21.838:.4f}")
print(f"  13.053/18.05 (ratio to U* at the 0.50 m tolerance) = {13.053/18.05:.4f}")
print(f"  13.053/16.165 (ratio to the 0.20 m baseline mean)  = {13.053/16.165:.4f}")
print("  -> the stated 72 per cent matches none of the t_opt-based readings; the nearest "
      "quantity is 13.053/18.05 = 0.723, a ratio to U*, not to t_opt")

print("\n=== (c) Wilson 95 per cent interval for 30/30 ===")
n, k, z = 30, 30, 1.959963985
p = k / n
den = 1 + z**2 / n
centre = (p + z**2 / (2 * n)) / den
half = (z / den) * sqrt(p * (1 - p) / n + z**2 / (4 * n**2))
lo, hi = centre - half, min(1.0, centre + half)
print(f"  p = {p}, centre = {centre:.6f}, half-width = {half:.6f}")
print(f"  interval = [{lo:.6f}, {hi:.6f}]")

print("\n=== checks ===")
quantity(f"{S/5.018:.4f} m/s", "19.592 m/s", rel_tol=1e-3)
quantity(f"{T_OPT/5.018:.5f}", "0.897", rel_tol=1e-3)
quantity(f"{S/6.082:.4f} m/s", "16.165 m/s", rel_tol=1e-3)
quantity(f"{T_OPT/12.360:.5f}", "0.364", rel_tol=2e-3)
quantity(f"{T_OPT/9.274:.5f}", "0.485", rel_tol=2e-3)
quantity(f"{S/10.122:.4f} m/s", "9.713 m/s", rel_tol=1e-3)
quantity(f"{lo:.6f}", "0.886", rel_tol=1e-3)
quantity(f"{hi:.6f}", "1.000", rel_tol=1e-3)
# (b) is the one row that does not close: flag it as an inequality that fails on the claim
inequality(f"{abs(T_OPT/t12 - 0.72):.6f}", "<", "0.01")
# arithmetic identities behind the table
import sympy as sp  # noqa: E402

S_, t_, to_ = sp.symbols("S_path t_run t_opt", positive=True)
identity((S_ / t_) / (S_ / to_), to_ / t_)
# Wilson's interval contains the point estimate's neighbourhood and is below 1 at the lower end
inequality(f"{lo:.6f}", "<", "1")
inequality(f"{lo:.6f}", ">", "0.8")
raise SystemExit(finish())
