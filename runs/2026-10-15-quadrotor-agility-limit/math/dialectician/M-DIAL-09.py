"""M-DIAL-09. "At s = 3 m rather than 6 m every range-limited bound halves."

Claim (lens finding 3, feeding DIAL-A): because the range elasticity "is +1 exactly in the dodge
bound", replacing the assumed 6 m usable depth range with 3 m halves every range-limited bound.

Independent derivation (SI). Two range-limited bounds are in the dossier:
  D-31 dodge:  v_dodge(s) = s/(tau + 2 sqrt(r/a))        -> linear in s, elasticity exactly +1.
  D-32 stop:   v_stop(s)  = a(-tau + sqrt(tau^2 + 2 s/a)) -> elasticity
               e_s = (s/v)*dv/ds = (1/2)/(1 + tau*v/s) ... computed below; strictly between
               1/2 and 1, so halving s does NOT halve v_stop.
Domain: s, tau, r, a > 0.
"""
import math
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, limit, inequality, quantity, units, finish  # noqa: E402

A = 16.33   # m/s^2, the FoV-limited acceleration the lens uses
TAU = 0.100
R = 0.5


def v_dodge(s, tau=TAU, r=R, a=A):
    return s / (tau + 2.0 * math.sqrt(r / a))


def v_stop(s, tau=TAU, a=A):
    return a * (-tau + math.sqrt(tau**2 + 2.0 * s / a))


def elast(f, x, frac=1e-6):
    return math.log(f(x * (1 + frac)) / f(x * (1 - frac))) / math.log((1 + frac) / (1 - frac))


print(f"a = {A} m/s^2, tau = {TAU*1e3:.0f} ms, r = {R} m")
for s in (6.0, 3.0):
    print(f"  s = {s:4.1f} m: v_dodge = {v_dodge(s):6.3f} m/s (e_s = {elast(v_dodge, s):.4f}), "
          f"v_stop = {v_stop(s):6.3f} m/s (e_s = {elast(v_stop, s):.4f})")
print(f"ratio on halving the range: dodge {v_dodge(3.0)/v_dodge(6.0):.4f} (claim 0.5), "
      f"stop {v_stop(3.0)/v_stop(6.0):.4f}")
print("so the dodge bound halves exactly, while the stop bound D-32 falls by only "
      f"{100*(1 - v_stop(3.0)/v_stop(6.0)):.1f} per cent, not 50: "
      "'every range-limited bound halves' holds only for bounds linear in s")
for tau in (0.0, 0.03, 0.1, 0.3):
    print(f"  stop-bound range elasticity at tau = {tau*1e3:5.1f} ms, s = 6 m: "
          f"{elast(lambda x: v_stop(x, tau=tau), 6.0):.4f} (bounded by 1/2 and 1)")

identity("s*diff(log(s/(tau + 2*sqrt(r/a))), s)", "1",
         domain={"s": (0.5, 50.0), "tau": (0.005, 0.5), "r": (0.05, 5.0), "a": (1.0, 100.0)})
identity("(3*s)/(tau + 2*sqrt(r/a))", "3*(s/(tau + 2*sqrt(r/a)))",
         domain={"s": (0.5, 50.0), "tau": (0.005, 0.5), "r": (0.05, 5.0), "a": (1.0, 100.0)})
# the stop bound's range elasticity is strictly below 1 for tau > 0
inequality("s*diff(log(a*(-tau + sqrt(tau**2 + 2*s/a))), s)", "<", "1",
           domain={"s": (0.5, 50.0), "tau": (0.005, 0.5), "a": (1.0, 100.0)})
inequality("s*diff(log(a*(-tau + sqrt(tau**2 + 2*s/a))), s)", ">", "1/2",
           domain={"s": (0.5, 50.0), "tau": (0.005, 0.5), "a": (1.0, 100.0)})
# zero-latency limit of the stop bound: v -> sqrt(2 a s), elasticity 1/2
limit("a*(-tau + sqrt(tau**2 + 2*s/a))", "tau", 0, "sqrt(2*a*s)",
      domain={"s": (0.5, 50.0), "a": (1.0, 100.0)})
limit("s*diff(log(a*(-tau + sqrt(tau**2 + 2*s/a))), s)", "tau", 0, "1/2",
      domain={"s": (0.5, 50.0), "a": (1.0, 100.0)})
quantity("3 m / (0.1 s + 2*(0.5 m/(16.33 m/s^2))^0.5)", "6.667 m/s", rel_tol=2e-3)
quantity("16.33 m/s^2 * (-0.1 s + (0.01 s^2 + 2*3 m/(16.33 m/s^2))^0.5)", "8.40 m/s", rel_tol=3e-3)
units("16.33 m/s^2 * (-0.1 s + (0.01 s^2 + 2*3 m/(16.33 m/s^2))^0.5)", "speed")

raise SystemExit(finish())
