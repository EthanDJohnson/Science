#!/usr/bin/env python3
"""M-SIMULATOR-08: the point-mass dodge bound and the simulated/point-mass ratios.

CLAIM (lens findings 8 and 9, candidate SIMULATOR-A): for a dodge of an obstacle detected at
range s with perception latency tau, requiring d = 0.75 m of lateral displacement at lateral
acceleration a = a_h = 44.260 m/s^2, the point-mass range elasticity is exactly 1 ("v scales
linearly in range at fixed latency" and "never saturates"), and the lens's simulated dodge
speeds are 0.848-0.920 of the point-mass bound: 0.848 (6 m, 20 ms), 0.875 (6 m, 50 ms),
0.920 (6 m, 100 ms), 0.913 (10 m, 50 ms), 0.884 (3 m, 50 ms).

SYMBOLS / DOMAIN. s > 0 m detection range; tau >= 0 s latency (blind time); d > 0 m required
lateral displacement; a > 0 m/s^2 lateral acceleration; v > 0 m/s forward speed, held
constant through the manoeuvre (the point-mass idealisation).

INDEPENDENT DERIVATION. The time available before reaching the obstacle is s/v. Of it, tau
is blind. Two candidate manoeuvre models:
  (A) one-sided: constant lateral acceleration for the whole manoeuvre,
      d = a t^2/2 -> t_man = sqrt(2 d/a);
  (B) symmetric bang-bang: accelerate for half the time, decelerate for the other half,
      ending at zero lateral rate, d = a t^2/4 -> t_man = sqrt(4 d/a).
In both, v = s/(tau + t_man), so d ln v/d ln s = 1 exactly at fixed tau, and
d ln v/d ln tau = -tau/(tau + t_man). Which model the lens used is decided here by which one
reproduces its stated ratios.
"""
import sys
from math import log, sqrt

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, inequality, limit, quantity, units  # noqa: E402

G = 9.80665
A_H = sqrt((4 * 8.5 / 0.75) ** 2 - G**2)
D = 0.75          # m of lateral displacement (0.5 m obstacle radius + 0.25 m vehicle radius)

t_one = sqrt(2 * D / A_H)
t_sym = sqrt(4 * D / A_H)
print("=== inputs (SI) ===")
print(f"d = {D} m, a = a_h = {A_H:.5f} m/s^2")
print(f"manoeuvre time: one-sided sqrt(2d/a) = {t_one:.6f} s; symmetric sqrt(4d/a) = {t_sym:.6f} s")


def v_pm(s, tau, t_man):
    return s / (tau + t_man)


sim = {(6.0, 0.020): None, (6.0, 0.050): 16.920, (6.0, 0.100): None,
       (10.0, 0.050): 29.412, (3.0, 0.050): 8.541}
lens_ratio = {(6.0, 0.020): 0.848, (6.0, 0.050): 0.875, (6.0, 0.100): 0.920,
              (10.0, 0.050): 0.913, (3.0, 0.050): 0.884}

print("\n=== which manoeuvre model reproduces the lens's ratios? ===")
print("  (s, tau)        v_pm one-sided  v_pm symmetric   v_sim    ratio one   ratio sym   lens")
for key in sorted(sim):
    s, tau = key
    v1, v2 = v_pm(s, tau, t_one), v_pm(s, tau, t_sym)
    vs = sim[key]
    if vs is None:
        print(f"  ({s:4.1f} m, {tau*1e3:5.1f} ms) {v1:9.3f}      {v2:9.3f}        --          --          --      "
              f"{lens_ratio[key]:.3f}  -> implied v_sim {lens_ratio[key]*v2:.3f} m/s (symmetric)")
    else:
        print(f"  ({s:4.1f} m, {tau*1e3:5.1f} ms) {v1:9.3f}      {v2:9.3f}    {vs:8.3f}   {vs/v1:8.4f}   "
              f"{vs/v2:8.4f}    {lens_ratio[key]:.3f}")

print("\n=== the latency elasticities implied by the ratios, on the symmetric model ===")
v20 = lens_ratio[(6.0, 0.020)] * v_pm(6.0, 0.020, t_sym)
v100 = lens_ratio[(6.0, 0.100)] * v_pm(6.0, 0.100, t_sym)
v50 = sim[(6.0, 0.050)]
e_20_100 = log(v100 / v20) / log(0.100 / 0.020)
e_50_100 = log(v100 / v50) / log(0.100 / 0.050)
print(f"  implied v_sim: 20 ms {v20:.3f} m/s, 50 ms {v50:.3f} m/s, 100 ms {v100:.3f} m/s")
print(f"  e(20 -> 100 ms) = {e_20_100:+.4f} (lens -0.105); e(50 -> 100 ms) = {e_50_100:+.4f} (lens -0.143)")

print("\n=== point-mass elasticities ===")
for tau in (0.020, 0.050, 0.100):
    print(f"  tau = {tau*1e3:5.1f} ms: e_s = {1.0:+.4f} exactly, "
          f"e_tau = {-tau/(tau+t_sym):+.4f} (symmetric), {-tau/(tau+t_one):+.4f} (one-sided)")
print(f"  arc e_tau(20 -> 100 ms, symmetric) = "
      f"{log((0.020+t_sym)/(0.100+t_sym))/log(0.100/0.020):+.4f}")
print(f"  arc e_s(3 -> 6 m) = {log(v_pm(6,0.05,t_sym)/v_pm(3,0.05,t_sym))/log(2.0):+.6f}")

print("\n=== checks ===")
quantity(f"{sim[(6.0,0.050)]/v_pm(6.0,0.050,t_sym):.4f}", "0.875", rel_tol=2e-3)
quantity(f"{sim[(3.0,0.050)]/v_pm(3.0,0.050,t_sym):.4f}", "0.884", rel_tol=2e-3)
quantity(f"{sim[(10.0,0.050)]/v_pm(10.0,0.050,t_sym):.4f}", "0.913", rel_tol=2e-3)
quantity(f"{e_20_100:.4f}", "-0.105", rel_tol=1e-2)
quantity(f"{e_50_100:.4f}", "-0.143", rel_tol=1e-2)
quantity(f"{log(v_pm(6,0.05,t_sym)/v_pm(3,0.05,t_sym))/log(2.0):.8f}", "1.0", rel_tol=1e-9)
# the one-sided model does NOT reproduce the lens's ratios
inequality(f"{abs(sim[(6.0,0.050)]/v_pm(6.0,0.050,t_one) - 0.875):.4f}", ">", "0.15")
# e_s = 1 exactly, symbolically, for any manoeuvre time
import sympy as sp  # noqa: E402

s_, tau_, tm_ = sp.symbols("s_rng tau_lat t_man", positive=True)
v = s_ / (tau_ + tm_)
identity(sp.simplify(sp.diff(sp.log(v), s_) * s_), sp.Integer(1))
identity(sp.simplify(sp.diff(sp.log(v), tau_) * tau_), -tau_ / (tau_ + tm_))
# limits: zero latency makes v insensitive to latency; huge latency makes e_tau -> -1
limit(-tau_ / (tau_ + tm_), "tau_lat", 0, "0", domain={"tau_lat": (0, 10), "t_man": (0.01, 10)})
limit(-tau_ / (tau_ + tm_), "tau_lat", "oo", "-1", domain={"tau_lat": (0, 1e9), "t_man": (0.01, 10)})
# the symmetric manoeuvre time is sqrt(2) longer than the one-sided one
identity(sp.sqrt(4 * sp.Symbol("d", positive=True) / sp.Symbol("a", positive=True)),
         sp.sqrt(2) * sp.sqrt(2 * sp.Symbol("d", positive=True) / sp.Symbol("a", positive=True)))
units("(6 m) / (0.05 s + (4 * 0.75 m / (44.26 m/s^2))^(1/2))", "speed")
units("(4 * 0.75 m / (44.26 m/s^2))^(1/2)", "time")
raise SystemExit(finish())
