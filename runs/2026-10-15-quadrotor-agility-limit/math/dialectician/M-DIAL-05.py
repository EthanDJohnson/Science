"""M-DIAL-05. Manoeuvre duration versus required lateral acceleration.

Claim (lens finding 6 and contradiction 3; candidate DIAL-C): actuator bandwidth becomes a
first-order term only for manoeuvres shorter than ~150 ms, "which on a 0.5 m-radius obstacle means
a > 90 m/s^2" (quoted as ~9 g).

Independent derivation (SI):
  The dodge bound D-31 charges a lateral manoeuvre time t_lat = 2*sqrt(r/u2_max): a bang-bang
  lateral profile with bounded acceleration a covers lateral displacement r in time t with
  r = 2 * (1/2) * a * (t/2)^2 = a t^2/4, so t = 2 sqrt(r/a) and a = 4 r / t^2.
  With r = 0.5 m and t = 0.150 s: a = 4*0.5/0.0225 = 88.9 m/s^2 = 9.06 g.
Domain: r > 0, t > 0, a > 0; point mass, no drag, instantaneous reversal of the lateral command.
"""
import math
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, limit, quantity, units, finish  # noqa: E402

G = 9.81
TAU = 0.0391


def a_required(r, t):
    return 4.0 * r / t**2


def t_lat(r, a):
    return 2.0 * math.sqrt(r / a)


for t in (0.100, 0.150, 0.160, 0.230):
    a = a_required(0.5, t)
    print(f"r = 0.5 m, t = {t*1e3:5.1f} ms: a = {a:7.2f} m/s^2 = {a/G:5.2f} g "
          f"(round trip t_lat(a) = {t_lat(0.5, a)*1e3:.2f} ms)")

print(f"inverse: at a = 90 m/s^2, t_lat = {t_lat(0.5, 90.0)*1e3:.2f} ms")
print(f"onboard-only platforms at T/W 4.4 reach a_h = {G*math.sqrt(4.4**2-1):.2f} m/s^2 "
      f"= {math.sqrt(4.4**2-1):.2f} g, below the 90 m/s^2 threshold; "
      f"T/W 12.35 reaches {G*math.sqrt(12.35**2-1):.2f} m/s^2 = {math.sqrt(12.35**2-1):.2f} g")
frac150 = 1.0 - (TAU / 0.150) * (1.0 - math.exp(-0.150 / TAU))
print(f"delivered fraction at T = 150 ms, tau = 39.1 ms: {frac150:.4f} "
      f"(lens quotes <= 0.76; 0.76 is reached at T = 160 ms: "
      f"{1.0 - (TAU/0.160)*(1.0 - math.exp(-0.160/TAU)):.4f})")

# bang-bang kinematics: two equal phases, displacement r in time t
identity("2*(a*(t/2)**2/2)", "a*t**2/4", domain={"a": (1.0, 200.0), "t": (0.01, 1.0)})
identity("4*r/(2*sqrt(r/a))**2", "a", domain={"r": (0.05, 5.0), "a": (1.0, 200.0)})
# the two forms are inverses
identity("2*sqrt(r/(4*r/t**2))", "t", domain={"r": (0.05, 5.0), "t": (0.01, 1.0)})
# limits: a large obstacle needs more acceleration for a fixed time; infinite acceleration -> zero time
limit("2*sqrt(r/a)", "a", "oo", "0", domain={"r": (0.05, 5.0)})
limit("4*r/t**2", "t", "oo", "0", domain={"r": (0.05, 5.0)})
quantity("4 * 0.5 m / (0.150 s)^2", "88.9 m/s^2", rel_tol=2e-3)
quantity("(4 * 0.5 m / (0.150 s)^2) / g0", "9.06", rel_tol=3e-3)
units("4 * 0.5 m / (0.150 s)^2", "acceleration")
units("2 * (0.5 m / (90 m/s^2))^0.5", "time")

raise SystemExit(finish())
