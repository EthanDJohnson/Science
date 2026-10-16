"""M-EMP-05. Latency elasticity implied by the human-vs-Swift lap times.

Claim (empiricist F5, ledger row 14; load-bearing for the elimination in EMP-E):
expert pilots at tau_h = 220 ms sensorimotor latency flew best three-lap times of
17.956 / 18.746 / 21.160 s against Swift's 17.465 s at tau_s = 40 ms, a 5.5x
latency ratio; the implied |e(speed, tau)| is 0.016-0.122, i.e. about 0.1.

Symbols: t_h, t_s = best three-lap times (s, > 0); tau_h, tau_s = sensorimotor
latencies (s, > 0); mean speed v = 3L/t for a common lap length L, so v_s/v_h =
t_h/t_s and L cancels. Elasticity (log-log, the standard definition for a ratio
this large):
    e = ln(v_s/v_h) / ln(tau_s/tau_h) = -ln(t_h/t_s) / ln(tau_h/tau_s),
so |e| = ln(t_h/t_s)/ln(5.5). Assumption: same airframe class and track, the
pilot's time attributed to the pilot (the lens flags this reading as its own
interpretation of the table). This is a two-point secant, not a derivative.
Also checked: the arc-elasticity variant (midpoint / Allen) to see whether the
claimed 0.122 upper end is a definitional difference.
"""
import math
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, inequality, limit, units  # noqa: E402

t_s = 17.465
pilots = (17.956, 18.746, 21.160)
tau_s, tau_h = 0.040, 0.220
ratio = tau_h / tau_s
print(f"inputs: t_s = {t_s} s, pilots {pilots} s, tau {tau_s * 1e3:.0f} vs {tau_h * 1e3:.0f} ms, "
      f"latency ratio = {ratio}")
inequality(f"abs({ratio} - 5.5)", "<", "1e-9")

es = []
for t_h in pilots:
    e = math.log(t_h / t_s) / math.log(ratio)
    es.append(e)
    speed_pen = 1 - t_s / t_h
    print(f"  t_h = {t_h} s: time penalty {100 * (t_h / t_s - 1):.2f}%, speed penalty "
          f"{100 * speed_pen:.2f}%, |e| (log-log) = {e:.4f}")
print(f"log-log range: {min(es):.4f} to {max(es):.4f} (lens claims 0.016 to 0.122)")
inequality(f"abs({min(es):.6f} - 0.016)", "<", "0.001")
inequality(f"abs({max(es):.6f} - 0.122)", "<", "0.012")     # 0.1126 vs 0.122: 8% apart
inequality(f"{max(es):.6f}", "<", "0.5")                    # the load-bearing content of F5

# arc / midpoint variant: (dv/v_bar) / (dtau/tau_bar)
for t_h in (pilots[0], pilots[-1]):
    v_s, v_h = 1 / t_s, 1 / t_h
    e_arc = ((v_s - v_h) / ((v_s + v_h) / 2)) / ((tau_s - tau_h) / ((tau_s + tau_h) / 2))
    print(f"  arc elasticity for t_h = {t_h}: {abs(e_arc):.4f}")
    inequality(f"{abs(e_arc):.6f}", "<", "0.5")

# structure: with v = C tau^(-p) the secant returns p exactly
identity("log(tau2**(-p)/tau1**(-p))/log(tau1/tau2)", "p",
         domain={"p": (0.01, 2.0), "tau1": (0.01, 1.0), "tau2": (0.01, 1.0)})
# if the two times were equal the elasticity would be exactly zero
limit("log(t/17.465)/log(5.5)", "t", 17.465, "0")
units("(0.22 s) / (0.04 s)", "dimensionless")
raise SystemExit(finish())
