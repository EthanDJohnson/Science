"""M-DIAL-03. Latency-versus-feature-spacing speed bound (synthesis S2).

Claim (lens finding 5 and contradiction 2; feeds DIAL-E and the "tight in clutter, slack on the
gate track" conclusion):
  w_c = (pi/2 - PM)/tau_eff  (dossier D-25, integrator loop with pure delay);
  requiring w_c >= 2*pi*k*v/L with reference manoeuvre frequency v/L and k correction cycles per
  feature gives v <= w_c*L/(2*pi*k), with elasticities exactly +1 in L and exactly -1 in tau_eff.
  Numbers claimed: tau = 40 ms, L = 10.71 m -> 33.5 m/s (k=1) / 16.7 (k=2);
  tau = 100 ms, L = 4 m -> 5.00 / 2.50; tau = 30 ms, L = 4 m -> 16.7 / 8.3;
  L = 75 m / 7 gates = 10.71 m; predicted seen:unseen speed ratio 8.52.

Independent derivation (SI: rad/s, m, s, m/s). PM in radians.
  Loop L(s) = (w_c/s) e^{-s tau}: phase at w_c is -pi/2 - w_c tau, so PM = pi/2 - w_c tau and
  w_c = (pi/2 - PM)/tau. Speed condition: v = (L/(2 pi k)) * w_c.
  Elasticities: d ln v / d ln L = 1; d ln v / d ln tau = -1 (v ~ 1/tau at fixed PM, L, k).
Domain: tau > 0, 0 <= PM < pi/2, L > 0, k >= 1.
"""
import math
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, limit, quantity, units, finish  # noqa: E402


def wc(tau, pm_deg=45.0):
    return (math.pi / 2.0 - math.radians(pm_deg)) / tau


def v_bound(tau, L, k=1, pm_deg=45.0):
    return wc(tau, pm_deg) * L / (2.0 * math.pi * k)


print("w_c = (pi/2 - PM)/tau_eff at PM = 45 deg; v <= w_c L/(2 pi k)")
print(f"gate spacing from 75 m / 7 gates = {75.0/7.0:.3f} m (lens: 10.71 m)")
rows = [("gate track", 0.040, 75.0 / 7.0), ("clutter, 100 ms", 0.100, 4.0),
        ("clutter, 30 ms", 0.030, 4.0)]
for name, tau, L in rows:
    print(f"  {name:16s} tau = {tau*1e3:5.1f} ms, L = {L:5.2f} m: w_c = {wc(tau):7.3f} rad/s, "
          f"v(k=1) = {v_bound(tau, L, 1):6.2f} m/s, v(k=2) = {v_bound(tau, L, 2):6.2f} m/s")

ratio = v_bound(0.040, 75.0 / 7.0) / v_bound(0.100, 4.0)
print(f"predicted seen:unseen ratio with L_gate = {75.0/7.0:.2f} m: {ratio:.3f}  (lens: 8.52)")
print(f"  ratio is (L_gate/tau_gate)/(L_clutter/tau_clutter) = "
      f"{(75.0/7.0/0.040)/(4.0/0.100):.3f}, independent of PM and k")
for Lg in (10.714, 12.0, 13.6, 14.0):
    print(f"  L_gate = {Lg:5.2f} m -> ratio {(Lg/0.040)/(4.0/0.100):.3f}; "
          f"spacing-only factor L_gate/L_clutter = {Lg/4.0:.3f}")
print("note: 8.52 requires L_gate = 13.6 m (ratio 8.50), not the 10.71 m stated in finding 5 "
      "(which gives 6.70); 10.71/4 = 2.68, not the 3.4 spacing factor quoted in contradiction 2")

# elasticities, numerically (central differences in logs) and symbolically
def elast(f, x, *rest, h=1e-6):
    return (math.log(f(x * (1 + h), *rest)) - math.log(f(x * (1 - h), *rest))) / (2 * h)


e_L = elast(lambda L: v_bound(0.040, L), 10.714)
e_tau = elast(lambda tau: v_bound(tau, 10.714), 0.040)
print(f"elasticities: d ln v/d ln L = {e_L:.6f} (claim +1), d ln v/d ln tau = {e_tau:.6f} (claim -1)")

identity("((pi/2 - PM)/tau)*L/(2*pi*k)", "L*(pi/2 - PM)/(2*pi*k*tau)",
         domain={"PM": (0.0, 1.5), "tau": (0.001, 1.0), "L": (0.5, 50.0), "k": (1.0, 4.0)})
# elasticity in L is exactly 1: d/dlnL of ln v
identity("L*diff(log(L*(pi/2 - PM)/(2*pi*k*tau)), L)", "1",
         domain={"PM": (0.0, 1.5), "tau": (0.001, 1.0), "L": (0.5, 50.0), "k": (1.0, 4.0)})
identity("tau*diff(log(L*(pi/2 - PM)/(2*pi*k*tau)), tau)", "-1",
         domain={"PM": (0.0, 1.5), "tau": (0.001, 1.0), "L": (0.5, 50.0), "k": (1.0, 4.0)})
# zero-phase-margin limit: w_c tau -> pi/2
limit("(pi/2 - PM)/tau", "PM", 0, "pi/(2*tau)", domain={"tau": (0.001, 1.0)})
# vanishing delay: the bound becomes unbounded
limit("((pi/2 - PM)/tau)*L/(2*pi)", "tau", 0, "oo",
      domain={"PM": (0.0, 1.5), "L": (0.5, 50.0)})
quantity("(0.785398/0.040 /s) * 10.7142857 m / (2*pi)", "33.47 m/s", rel_tol=2e-3)
quantity("(0.785398/0.100 /s) * 4 m / (2*pi)", "5.00 m/s", rel_tol=2e-3)
units("(0.785398/0.040 /s) * 10.7142857 m / (2*pi)", "speed")
units("0.785398/0.040 /s", "frequency")

raise SystemExit(finish())
