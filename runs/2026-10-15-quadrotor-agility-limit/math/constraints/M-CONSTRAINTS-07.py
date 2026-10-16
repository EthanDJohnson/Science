"""M-CONSTRAINTS-07: feedback-only speed ceiling versus flatness feedforward (lens finding F9,
candidate CONSTRAINTS-D).

Claim as I state it (SI units):
  (a) A loop of crossover wc tracking a turn at speed v by feedback alone carries a lateral
      lag error e = v/wc, so v_max = e_allow * wc.
  (b) A pure transport delay tau with phase margin PM caps the crossover at
      wc <= (pi/2 - PM)/tau (integrator-like loop), hence v_max = e_allow (pi/2 - PM)/tau and
      d ln v_max / d ln tau = -1 exactly.
      Numbers with e_allow = 0.60 m: tau = 40 ms -> wc = 19.63 rad/s, v_max = 11.8 m/s
      (PM 45 deg) and 7.9 m/s (PM 60 deg); tau = 17.5 ms -> 26.9 m/s; tau = 130 ms -> 3.6 m/s.
  (c) With feedforward the loop must only reject a constant acceleration disturbance a_d, and a
      unity-damped second-order loop leaves e = a_d/wc^2, so wc_min = sqrt(a_d/e_allow).
      a_d = 0.40 N / 0.87 kg = 0.46 m/s^2 -> wc_min = 0.875 rad/s, which tolerates
      tau = (pi/2 - PM)/wc_min = 897 ms at PM 45 deg, a factor 22.4 over 40 ms; and at
      wc = 19.63 rad/s the residual is a_d/wc^2 = 1.2 mm.
Domain: wc, tau, e_allow, a_d > 0; 0 < PM < pi/2; LTI SISO, no saturation.
"""
import sys
import math
import cmath
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, inequality, units, quantity, finish
from control_tools import loop_margins


def approx(label, got, want, rel=0.015):
    print(f"  {label}: got {got:.6g}, lens {want:.6g}")
    return inequality(f"Abs({got!r} - ({want!r}))", "<", f"{rel}*Abs({want!r})")


wc, tau, ea, ad, pm = sp.symbols("wc tau ea ad pm", positive=True)

print("1. the delay-limited crossover, derived from the phase condition of k e^{-tau s}/s")
# arg L(j w) = -pi/2 - w tau; PM = pi + arg L = pi/2 - w tau
wc_bound = (sp.pi / 2 - pm) / tau
identity(sp.pi + (-sp.pi / 2 - wc_bound * tau), pm)
identity(sp.diff(wc_bound.subs(pm, sp.pi / 4), tau) * tau / wc_bound.subs(pm, sp.pi / 4), -1)
units("(1.5708 - 0.7854) / (0.040 s)", "1/s")
# independent numeric route: loop_margins on L(s) = k e^{-tau s}/s with k = wc
for tau_v, pm_v in ((0.040, 45.0), (0.0175, 45.0), (0.040, 60.0)):
    w_pred = (math.pi / 2 - math.radians(pm_v)) / tau_v
    def loop(s, k=w_pred, t=tau_v):
        return k * cmath.exp(-t * s) / s
    mar = loop_margins(loop)
    print(f"   tau = {1000*tau_v:.1f} ms, PM target {pm_v} deg: predicted wc = {w_pred:.3f} rad/s, "
          f"tool wc = {mar['w_gain_crossover']:.3f} rad/s, tool PM = {mar['phase_margin_deg']:.2f} deg")
    approx(f"tool PM at predicted wc (tau={1000*tau_v:.1f} ms) [deg]", mar["phase_margin_deg"], pm_v, rel=0.01)

print("2. feedback-only speed ceiling, e_allow = 0.60 m")
E_ALLOW = 0.60
for tau_v, pm_v, want in ((0.040, 45.0, 11.78), (0.040, 60.0, 7.85), (0.0175, 45.0, 26.93), (0.130, 45.0, 3.62)):
    w = (math.pi / 2 - math.radians(pm_v)) / tau_v
    approx(f"v_max (tau = {1000*tau_v:.1f} ms, PM {pm_v}) [m/s]", E_ALLOW * w, want, rel=0.01)
vmx = ea * (sp.pi / 2 - pm) / tau
identity(sp.diff(vmx, tau) * tau / vmx, -1)
units("0.60 m * 19.63 /s", "m/s")

print("3. feedforward: the disturbance-rejection bandwidth")
A_D = 0.40 / 0.87
approx("a_d [m/s^2]", A_D, 0.46, rel=0.01)
wc_min = math.sqrt(A_D / E_ALLOW)
approx("wc_min = sqrt(a_d/e_allow) [rad/s]", wc_min, 0.875, rel=0.01)
identity(sp.sqrt(ad / ea), sp.solve(sp.Eq(ad / wc ** 2, ea), wc)[0])
units("(0.46 m/s^2) / (0.60 m)", "1/s^2")
tau_ok = (math.pi / 2 - math.pi / 4) / wc_min
approx("tolerable delay at PM 45 deg [ms]", 1000 * tau_ok, 897.0, rel=0.01)
approx("margin over 40 ms", tau_ok / 0.040, 22.4, rel=0.01)
res = A_D / ((math.pi / 2 - math.pi / 4) / 0.040) ** 2
approx("residual error at 40 ms [mm]", 1000 * res, 1.193, rel=0.01)
units("0.46 m/s^2 / (19.63 /s)^2", "m")
inequality("ad/wc**2", "<", "0.60", domain={"ad": (0.46, 0.46), "wc": (1.0, 100.0)})
limit(ad / wc ** 2, "wc", "oo", 0)

print("4. consistency: the two architectures' ceilings differ by (e_allow wc^2/a_d) in bandwidth")
# feedback-only needs wc = v/e_allow; feedforward needs wc = sqrt(a_d/e_allow): ratio at v = 15 m/s
r = (15.0 / E_ALLOW) / wc_min
print(f"   at 15 m/s the feedback-only loop needs {15.0/E_ALLOW:.2f} rad/s against {wc_min:.3f} rad/s: "
      f"ratio {r:.1f}")
approx("bandwidth ratio at 15 m/s", r, 28.6, rel=0.05)

raise SystemExit(finish())
