"""M-DIAL-07. The contradiction-1 prediction: 15 m/s with perfect aerodynamics, ~26 m/s at 12 m range.

Claim (lens contradiction 1, "what the synthesis predicts"): a controller with perfect aerodynamics
and the A-20 sensing suite "will not exceed ~13-15 m/s at 90 per cent success on unseen clutter,
because the dodge bound at s = 6 m, tau = 50 ms caps it at 15.0 m/s even with FoV-limited
acceleration"; conversely "a vehicle with a crude aerodynamic model but 12 m of usable range should
reach ~26 m/s on the same clutter", and the synthesis says the range swap wins "by >50 per cent".

Independent derivation (SI): dodge bound v = s/(tau + 2 sqrt(r/a)) with r = 0.5 m and
a = a_FoV = g tan(30 deg + 58 deg/2) = 16.33 m/s^2.
Domain: s, tau, r, a > 0.
"""
import math
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, limit, quantity, units, inequality, finish  # noqa: E402

G = 9.81
A_FOV = G * math.tan(math.radians(30.0 + 58.0 / 2.0))
R = 0.5


def v(s, tau, a=A_FOV, r=R):
    return s / (tau + 2.0 * math.sqrt(r / a))


print(f"a_FoV = {A_FOV:.3f} m/s^2, r = {R} m")
for s, tau in ((6.0, 0.050), (6.0, 0.100), (12.0, 0.050), (12.0, 0.100)):
    print(f"  s = {s:5.1f} m, tau = {tau*1e3:5.1f} ms: v = {v(s, tau):6.2f} m/s")
print(f"'~26 m/s at 12 m' matches s = 12 m with tau = 100 ms ({v(12.0, 0.100):.2f} m/s), "
      f"not with the tau = 50 ms used in the same sentence ({v(12.0, 0.050):.2f} m/s)")
a_lat_50 = v(6.0, 0.050)
print(f"option (i) perfect aero, s = 6 m, tau = 50 ms: {a_lat_50:.2f} m/s")
print(f"option (ii) crude aero, s = 12 m, tau = 100 ms: {v(12.0, 0.100):.2f} m/s "
      f"-> (ii)/(i) = {v(12.0, 0.100)/a_lat_50:.3f}, i.e. "
      f"{100*(v(12.0, 0.100)/a_lat_50 - 1):+.1f} per cent (claim: >50 per cent)")
print("at equal latency the ratio is exactly the range ratio: "
      f"{v(12.0, 0.100)/v(6.0, 0.100):.3f}")

identity("2*s/(tau + 2*sqrt(r/a))", "2*(s/(tau + 2*sqrt(r/a)))",
         domain={"s": (0.5, 50.0), "tau": (0.005, 0.5), "r": (0.05, 5.0), "a": (1.0, 100.0)})
# doubling the range exactly doubles the bound, at fixed latency
identity("(2*s/(tau + 2*sqrt(r/a)))/(s/(tau + 2*sqrt(r/a)))", "2",
         domain={"s": (0.5, 50.0), "tau": (0.005, 0.5), "r": (0.05, 5.0), "a": (1.0, 100.0)})
# halving latency gives strictly less than doubling the range
inequality("s/(tau/2 + 2*sqrt(r/a))", "<", "2*s/(tau + 2*sqrt(r/a))",
           domain={"s": (0.5, 50.0), "tau": (0.005, 0.5), "r": (0.05, 5.0), "a": (1.0, 100.0)})
limit("s/(tau + 2*sqrt(r/a))", "s", "oo", "oo",
      domain={"tau": (0.005, 0.5), "r": (0.05, 5.0), "a": (1.0, 100.0)})
quantity("6 m / (0.05 s + 2*(0.5 m/(16.33 m/s^2))^0.5)", "15.00 m/s", rel_tol=2e-3)
quantity("12 m / (0.1 s + 2*(0.5 m/(16.33 m/s^2))^0.5)", "26.67 m/s", rel_tol=2e-3)
units("12 m / (0.1 s + 2*(0.5 m/(16.33 m/s^2))^0.5)", "speed")

raise SystemExit(finish())
