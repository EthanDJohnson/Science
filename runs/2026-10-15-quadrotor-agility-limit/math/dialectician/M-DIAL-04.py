"""M-DIAL-04. First-order actuator lag versus pure transport delay (synthesis S3).

Claims (lens finding 6 and contradiction 3; candidate DIAL-C):
 (a) With tau = 39.1 ms, an integrator loop with a first-order lag crosses over at
     w_c = 25.58 rad/s at PM 45 deg, and with a pure delay at 20.09 rad/s; ratio 1.27.
     At PM 60 deg: 14.77 vs 13.39, ratio 1.10.
 (b) With the actuator pole inverted and ~2 ms of transport delay left, w_c <= 392.7 rad/s
     (62.5 Hz) at PM 45 deg; contradiction 3 quotes "260-390 rad/s (42-63 Hz)" for 1-2 ms.
 (c) The delivered fraction of a commanded acceleration step over a manoeuvre of duration T is
     1 - (tau/T)(1 - exp(-T/tau)): 0.83 at T = 230 ms and 0.44 at T = 50 ms (losses 17.0 and
     56.4 per cent); losses 36.1 per cent at 100 ms, 24.0 per cent at 160 ms, 3.9 per cent at 1 s;
     and a_eff/a_cmd <= 0.76 at T ~ 150 ms.

Independent derivation (SI; rad/s, s):
  Lag loop  L1(s) = (K/s) * 1/(1 + s tau): phase = -pi/2 - atan(w tau); PM = pi/2 - atan(w tau),
  so atan(w_c tau) = pi/2 - PM  =>  w_c = tan(pi/2 - PM)/tau.
  Delay loop L2(s) = (K/s) e^{-s tau}: PM = pi/2 - w tau  =>  w_c = (pi/2 - PM)/tau.
  Ratio w_lag/w_delay = tan(x)/x with x = pi/2 - PM, which exceeds 1 for 0 < x < pi/2.
  Large signal: a(t) = a_cmd (1 - e^{-t/tau}) for a step at t = 0; the mean delivered fraction over
  [0, T] is (1/T) int_0^T (1 - e^{-t/tau}) dt = 1 - (tau/T)(1 - e^{-T/tau}).
Domain: tau > 0, 0 <= PM < pi/2, T > 0.
"""
import math
import sys

import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, limit, series, inequality, units, quantity, finish  # noqa: E402

TAU = 0.0391  # s


def wc_lag(tau, pm_deg):
    return math.tan(math.pi / 2.0 - math.radians(pm_deg)) / tau


def wc_delay(tau, pm_deg):
    return (math.pi / 2.0 - math.radians(pm_deg)) / tau


for pm in (45.0, 60.0):
    wl, wd = wc_lag(TAU, pm), wc_delay(TAU, pm)
    print(f"tau = 39.1 ms, PM = {pm:4.1f} deg: w_c(lag) = {wl:7.3f} rad/s, "
          f"w_c(delay) = {wd:7.3f} rad/s, ratio {wl/wd:.4f}")

for tau_ms in (1.0, 2.0, 3.0):
    for pm in (45.0, 60.0):
        w = wc_delay(tau_ms * 1e-3, pm)
        print(f"  pure transport {tau_ms:.0f} ms at PM {pm:.0f} deg: w_c <= {w:7.2f} rad/s "
              f"= {w/(2*math.pi):6.2f} Hz")
print("note: '260-390 rad/s (42-63 Hz)' corresponds to a 2 ms transport delay at PM 60-45 deg, "
      "not to 1-2 ms at a fixed PM (1 ms at PM 45 deg gives 785 rad/s)")

# numerical check of the lag crossover by solving the phase condition directly
def phase_lag(w, tau):
    return -math.pi / 2.0 - math.atan(w * tau)


w = wc_lag(TAU, 45.0)
print(f"phase of the lag loop at w_c = {w:.3f} rad/s: {math.degrees(phase_lag(w, TAU)):.3f} deg "
      f"-> PM = {180.0 + math.degrees(phase_lag(w, TAU)):.3f} deg")

print("delivered fraction 1 - (tau/T)(1 - exp(-T/tau)), tau = 39.1 ms:")
for T in (0.050, 0.100, 0.150, 0.160, 0.230, 1.0):
    frac = 1.0 - (TAU / T) * (1.0 - math.exp(-T / TAU))
    # independent route: numerical mean of the step response
    n = 200001
    mean = sum(1.0 - math.exp(-(i + 0.5) * T / n / TAU) for i in range(n)) / n
    print(f"  T = {T*1e3:6.1f} ms: fraction = {frac:.4f} (loss {100*(1-frac):5.2f} %); "
          f"quadrature mean = {mean:.4f}")

# --- symbolic checks ---------------------------------------------------------------
t, T, tau, x = sp.symbols("t T tau x", positive=True)
mean_expr = sp.integrate(1 - sp.exp(-t / tau), (t, 0, T)) / T
identity(sp.simplify(mean_expr), 1 - (tau / T) * (1 - sp.exp(-T / tau)),
         domain={"T": (0.001, 10.0), "tau": (0.001, 1.0)})
# the lag/delay crossover ratio is tan(x)/x > 1 on (0, pi/2)
identity("tan(x)/x", "(tan(x)/tau)/(x/tau)", domain={"x": (0.01, 1.5), "tau": (0.001, 1.0)})
inequality("tan(x)/x", ">", "1", domain={"x": (0.01, 1.5)})
# quasi-static limit: a long manoeuvre delivers everything
limit("1 - (tau/T)*(1 - exp(-T/tau))", "T", "oo", "1", domain={"tau": (0.001, 1.0)})
# short-manoeuvre limit: the fraction goes to 0 like T/(2 tau)
series("1 - (tau/T)*(1 - exp(-T/tau))", "T", 0, 3, "T/(2*tau) - T**2/(6*tau**2)",
       domain={"tau": (0.001, 1.0)})
# zero-phase-margin limit of the delay bound
limit("(pi/2 - PM)/tau", "PM", 0, "pi/(2*tau)", domain={"tau": (0.001, 1.0)})
units("1.0 / 0.0391 /s", "frequency")               # tan(pi/2 - PM)/tau = tan(45 deg)/tau
units("0.0391 s / (0.230 s)", "dimensionless")      # the delivered fraction is dimensionless
quantity("0.785398 / 0.002 /s", "392.7 /s", rel_tol=1e-3)
quantity("1.0 / 0.0391 /s", "25.575 /s", rel_tol=1e-3)
identity("1 - (0.0391/0.230)*(1 - exp(-0.230/0.0391))", str(1.0 - (TAU / 0.230) * (1.0 - math.exp(-0.230 / TAU))),
         domain={})
identity("1 - (0.0391/0.050)*(1 - exp(-0.050/0.0391))", str(1.0 - (TAU / 0.050) * (1.0 - math.exp(-0.050 / TAU))),
         domain={})

raise SystemExit(finish())
