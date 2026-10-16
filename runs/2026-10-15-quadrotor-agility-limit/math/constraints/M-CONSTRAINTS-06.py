"""M-CONSTRAINTS-06: the latency budget, the delay-margin bound and the cascaded rate-loop
crossover (lens finding F8, constraint-table row C5/C6).

Claim as I state it (SI units):
  (a) Budget sums: 40 ms sensorimotor + 5 ms (half a 10 ms ZOH period at 100 Hz) + 39.1 ms motor
      lag = 84.1 ms; 17 + 1 + 39.1 = 57.1 ms; 130 + 10 + 39.1 = 179.1 ms.
  (b) For a loop with pure delay th and phase margin PM the crossover obeys
      wc <= (pi/2 - PM)/th for an integrator-like loop (checked in M-CONSTRAINTS-07).
  (c) Cascaded rate loop L(s) = k e^{-th s}/(Jx s (1 + tc s)): at PM = 45 deg the crossover
      solves atan(wc tc) + wc th = pi/4, so with th = 0, wc = 1/tc exactly:
      tc = 39.1 ms -> 25.58 rad/s = 4.07 Hz; tc = 33 ms -> 30.30 rad/s; tc = 10 ms -> 100 rad/s;
      tc = 39.1 ms with th = 2 ms -> 23.30 rad/s; and d ln wc/d ln tc = -1 (th = 0).
  (d) The lens's single-loop claim "tau_eff = 84.1 ms admits a closed-loop bandwidth of only
      4.40 rad/s (0.70 Hz)" is an inference from its own LQR trace
        bandwidth (rad/s): 2.25, 4.40, 7.91, 14.07, 25.03, 44.50
        delay margin (ms): 179.37, 120.59, 76.74, 46.58, 27.25, 15.26
      (taken here as given data, one decade of R apart).  I check only the inference: since the
      delay margin falls monotonically with bandwidth, the largest bandwidth whose delay margin
      covers 84.1 ms lies strictly between 4.40 and 7.91 rad/s, so 4.40 rad/s is a
      grid-restricted lower bound, not the admissible bandwidth.
Domain: tc, th, Jx > 0; LTI SISO; gain k free (chosen to put crossover at wc).
"""
import sys
import math
import cmath
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, inequality, units, finish
from control_tools import loop_margins


def approx(label, got, want, rel=0.015):
    print(f"  {label}: got {got:.6g}, lens {want:.6g}")
    return inequality(f"Abs({got!r} - ({want!r}))", "<", f"{rel}*Abs({want!r})")


print("1. the latency budget sums")
approx("40 + 10/2 + 39.1 [ms]", 40.0 + 10.0 / 2 + 39.1, 84.1, rel=1e-3)
approx("17 + 2/2 + 39.1 [ms]", 17.0 + 2.0 / 2 + 39.1, 57.1, rel=1e-3)
approx("130 + 20/2 + 39.1 [ms]", 130.0 + 20.0 / 2 + 39.1, 179.1, rel=1e-3)
units("40 ms + 5 ms + 39.1 ms", "s")

print("2. the rate-loop phase condition, derived from arg L(j wc) = -pi + PM")
wc, tc, th, pm = sp.symbols("wc tc th pm", positive=True)
# arg L = -pi/2 - atan(wc tc) - wc th;  PM = pi + arg L
identity(sp.pi + (-sp.pi / 2 - sp.atan(wc * tc) - wc * th), sp.pi / 2 - sp.atan(wc * tc) - wc * th)
# with th = 0 and PM = pi/4: atan(wc tc) = pi/4 -> wc tc = 1
identity(sp.tan(sp.pi / 4) / tc, 1 / tc)
wc_sol = 1 / tc
identity(sp.diff(wc_sol, tc) * tc / wc_sol, -1)        # elasticity exactly -1
limit(sp.atan(wc * tc), "tc", 0, 0)                    # no lag: no phase lag, unbounded wc


def crossover(tc_v, th_v, pm_deg=45.0):
    """Solve atan(wc tc) + wc th = pi/2 - PM by bisection."""
    target = math.pi / 2 - math.radians(pm_deg)
    lo, hi = 1e-6, 1e6
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if math.atan(mid * tc_v) + mid * th_v < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


JX = 2.5e-3
for tc_v, th_v, want in ((0.0391, 0.0, 25.58), (0.033, 0.0, 30.30), (0.010, 0.0, 100.0),
                         (0.0391, 0.002, 23.30), (0.0391, 0.005, 20.75), (0.010, 0.002, 74.04)):
    w = crossover(tc_v, th_v)
    k = JX * w * math.sqrt(1.0 + (w * tc_v) ** 2)       # makes |L(j w)| = 1

    def loop(s, k=k, t=th_v, tcl=tc_v):
        return k * cmath.exp(-t * s) / (JX * s * (1.0 + tcl * s))

    mar = loop_margins(loop)
    print(f"   tc = {1000*tc_v:.1f} ms, th = {1000*th_v:.1f} ms: wc = {w:.3f} rad/s "
          f"({w/2/math.pi:.3f} Hz), tool wc = {mar['w_gain_crossover']:.3f}, tool PM = "
          f"{mar['phase_margin_deg']:.3f} deg")
    approx(f"wc (tc = {1000*tc_v:.1f} ms, th = {1000*th_v:.1f} ms) [rad/s]", w, want, rel=0.01)
    approx(f"tool PM at that wc [deg]", mar["phase_margin_deg"], 45.0, rel=0.01)
approx("4.07 Hz from 25.58 rad/s", crossover(0.0391, 0.0) / (2 * math.pi), 4.07, rel=0.01)
# elasticity of the crossover to tc, numerically, with and without the extra 2 ms
h = 0.01
for th_v in (0.0, 0.002):
    el = (math.log(crossover(0.0391 * (1 + h), th_v)) - math.log(crossover(0.0391 * (1 - h), th_v))) / (2 * h)
    print(f"   d ln wc/d ln tc at th = {1000*th_v:.0f} ms: {el:+.4f}")
approx("d ln wc/d ln tc at th = 0", (math.log(crossover(0.0391 * 1.01, 0.0))
                                    - math.log(crossover(0.0391 * 0.99, 0.0))) / 0.02, -1.0, rel=1e-3)

print("3. the inference from the lens's own LQR delay-margin trace (its numbers, my inference)")
bw = [2.25, 4.40, 7.91, 14.07, 25.03, 44.50]
dm = [179.37, 120.59, 76.74, 46.58, 27.25, 15.26]
inequality(f"{max(dm[i+1] - dm[i] for i in range(len(dm)-1))!r}", "<", "0")   # strictly decreasing
for budget, lens_claim in ((84.1, 4.40), (57.1, 7.91), (179.1, 2.25)):
    # largest grid bandwidth whose delay margin covers the budget
    grid = max(b for b, d in zip(bw, dm) if d >= budget)
    # log-linear interpolation of the continuous trace
    i = next(i for i in range(len(bw) - 1) if dm[i] >= budget >= dm[i + 1])
    f = (math.log(budget) - math.log(dm[i])) / (math.log(dm[i + 1]) - math.log(dm[i]))
    interp = math.exp(math.log(bw[i]) + f * (math.log(bw[i + 1]) - math.log(bw[i])))
    print(f"   budget {budget:.1f} ms: lens {lens_claim} rad/s, grid maximum {grid} rad/s, "
          f"interpolated {interp:.2f} rad/s ({interp/2/math.pi:.2f} Hz)")
    approx(f"grid maximum at {budget} ms [rad/s]", grid, lens_claim, rel=1e-6)
    if budget == 84.1:
        inequality(f"{interp!r}", ">", f"{1.4*lens_claim!r}")   # the claim understates by >1.4x

raise SystemExit(finish())
