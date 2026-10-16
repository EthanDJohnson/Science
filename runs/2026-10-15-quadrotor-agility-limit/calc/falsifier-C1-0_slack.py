#!/usr/bin/env python3
"""Refuter 0 vs C1 ("the perceived volume ahead binds first").

Attack: an elasticity of a BOUND is not an elasticity of the METRIC.  The metric is
min over active bounds, so d ln v_metric / d ln s = 0 wherever the range bound sits
ABOVE the speed at which the vehicle actually stops meeting 90 per cent.  Everything
here uses C1's own numbers and the A-20 platform's own published optics.

SI units throughout (m, s, m/s, m/s^2, deg).  g = 9.80665 m/s^2.

Sections
  A  required look-ahead vs usable range at the measured operating point (A-20)
  B  the A-20 paper's OWN perception bound (A-21) against its own failure curve
  C  how small the usable range must be for the range leg to be ACTIVE at 7 m/s
  D  the solid-angle (1b) leg with the A-20 platform's real optics, both tilt signs
  E  does the banked dodge move the velocity out of a forward cone at all?
  F  the e_s = 1 identity: structural, not measured
"""
import math

import sympy as sp

G = 9.80665


def stop_bound(s, a, tau):
    """v tau + v^2/(2a) <= s  ->  v = a(-tau + sqrt(tau^2 + 2 s/a))   [D-32/A-33]"""
    return a * (-tau + math.sqrt(tau * tau + 2.0 * s / a))


def stop_range(v, a, tau):
    """inverse: the look-ahead a stop at speed v needs"""
    return v * tau + v * v / (2.0 * a)


def dodge_bound(s, a, tau, d=0.75):
    """v = s/(tau + 2 sqrt(d/a))  [D-31, symmetric bang-bang, M-SIMULATOR-08 verified]"""
    return s / (tau + 2.0 * math.sqrt(d / a))


def dodge_range(v, a, tau, d=0.75):
    return v * (tau + 2.0 * math.sqrt(d / a))


print(__doc__)

# ---------------------------------------------------------------- A
print("=" * 92)
print("A.  REQUIRED LOOK-AHEAD vs USABLE RANGE, at the A-20 operating point")
print("=" * 92)
# A-20 platform: 890 g, ~40 N, T/W 4.4 -> a_h = g sqrt((T/W)^2 - 1)
TW = 4.4
a_h = G * math.sqrt(TW ** 2 - 1.0)
print(f"  A-20 platform T/W = {TW}  ->  a_h = g sqrt(TW^2-1) = {a_h:.2f} m/s^2")
print(f"  {'v (m/s)':>8s} {'s_stop (m)':>11s} {'s_dodge (m)':>12s} "
      f"{'slack vs 6 m (stop)':>20s} {'slack vs 4.1 m (stop)':>22s}")
for v in (3.0, 5.0, 7.0, 10.0, 15.0):
    for tau in (0.107,):
        ss = stop_range(v, a_h, tau)
        sd = dodge_range(v, a_h, tau)
        print(f"  {v:8.1f} {ss:11.2f} {sd:12.2f} {6.0/ss:20.2f} {4.106/ss:22.2f}")
print("  (tau_sense = 107 ms, the mechanist's own value used in M-MECH-02/03;")
print("   6 m = C1's lower usable depth range; 4.106 m = C1's own stereo-noise")
print("   ceiling for a 50 mm baseline [M-MECH-06 verified].)")
print()
print("  Same table read as a SPEED bound (what range permits):")
print(f"  {'s (m)':>7s} {'v_stop (m/s)':>13s} {'v_dodge (m/s)':>14s}")
for s in (4.106, 5.807, 6.0, 10.0):
    print(f"  {s:7.2f} {stop_bound(s, a_h, 0.107):13.2f} "
          f"{dodge_bound(s, a_h, 0.107):14.2f}")
print("  OBSERVED: 100 % at 3 and 5 m/s, 80 % at 7 m/s, 60 % at 10 m/s [A-20].")
print("  The brief's 90-per-cent metric is therefore met at <= 5 m/s and lost by 7 m/s.")
v_obs = 7.0
for s in (4.106, 6.0, 10.0):
    print(f"      range leg at s = {s:5.2f} m exceeds the 7 m/s ceiling by "
          f"{stop_bound(s, a_h, 0.107)/v_obs:.2f}x (stop) and "
          f"{dodge_bound(s, a_h, 0.107)/v_obs:.2f}x (dodge)")

# ---------------------------------------------------------------- B
print()
print("=" * 92)
print("B.  THE A-20 PAPER'S OWN PERCEPTION BOUND [A-21] AGAINST ITS OWN FAILURE CURVE")
print("=" * 92)
for name, vb in (("method 1", 12.0), ("method 2", 13.2), ("method 3", 13.5)):
    print(f"  {name}: v_max from sensing range + latency = {vb:.1f} m/s; "
          f"ratio to the 7 m/s 90-per-cent ceiling = {vb/7.0:.2f}x, "
          f"to the 10 m/s 60-per-cent point = {vb/10.0:.2f}x")
print("  A-21 is the SAME paper and the SAME platform as A-20 (1.5 m pole at 6 m,")
print("  0.2 m sphere, rotational dynamics included).  Its own perception-limited")
print("  speed is 1.7-1.9x above the speed at which its hardware already fails 20 %")
print("  of the time, so the perception-volume bound is NOT the active constraint there.")

# ---------------------------------------------------------------- C
print()
print("=" * 92)
print("C.  HOW SMALL MUST THE USABLE RANGE BE FOR THE RANGE LEG TO BE ACTIVE AT 7 m/s?")
print("=" * 92)
print(f"  {'a (m/s^2)':>11s} {'tau (s)':>9s} {'s_req stop (m)':>16s} {'s_req dodge (m)':>17s}")
for a, tau in ((a_h, 0.040), (a_h, 0.107), (a_h, 0.150),
               (16.33, 0.107), (16.33, 0.150), (5.44, 0.107), (5.44, 0.150)):
    print(f"  {a:11.2f} {tau:9.3f} {stop_range(7.0, a, tau):16.2f} "
          f"{dodge_range(7.0, a, tau):17.2f}")
print("  Even with C1's most pessimistic FoV-capped acceleration (5.44 m/s^2) and a")
print("  150 ms chain, the range the bound needs to be active at 7 m/s is 5.55 m (stop)")
print("  -- i.e. the leg becomes active only at the very bottom of its own quoted")
print("  6-10 m usable range, and only if the acceleration is simultaneously capped to")
print("  0.55 g, which is the leg (1b) whose own math check inverted its ranking")
print("  [M-MECH-03 refuted].")

# ---------------------------------------------------------------- D
print()
print("=" * 92)
print("D.  LEG (1b) WITH THE A-20 PLATFORM'S REAL OPTICS, BOTH TILT SIGNS")
print("=" * 92)
print("  A-20 sensor: D435i depth, ~90 deg HFoV, 58 deg VFoV, tilted 30 deg above 7 m/s.")
print("  C1 uses the 58 deg VERTICAL FoV with the tilt ADDED: a_u = g tan(29+30).")
print(f"  {'case':>46s} {'phi (deg)':>10s} {'a_u (m/s^2)':>12s} {'a_u/g':>7s} "
      f"{'v_stop at 6 m (m/s)':>20s}")
cases = [
    ("vertical half-FoV 29, level mount (C1's own 1a/1b)", 29.0),
    ("vertical half-FoV 29 + 30 up-tilt (C1's headline)", 59.0),
    ("vertical half-FoV 29 - 30 up-tilt (BRAKING sign)", -1.0),
    ("horizontal half-FoV 45 (A-20's ~90 deg HFoV), level", 45.0),
    ("horizontal half-FoV 45 + 30 (as C1 adds tilt)", 75.0),
]
for label, phi in cases:
    if phi <= 0.0:
        print(f"  {label:>46s} {phi:10.1f} {'n/a':>12s} {'n/a':>7s} "
              f"{'no forward view':>20s}")
        continue
    a_u = min(a_h, G * math.tan(math.radians(phi)))
    print(f"  {label:>46s} {phi:10.1f} {a_u:12.2f} {a_u/G:7.2f} "
          f"{stop_bound(6.0, a_u, 0.107):20.2f}")
print("  The dilemma: a quadrotor DECELERATES by pitching NOSE-UP, so a camera already")
print("  tilted 30 deg up has phi = 29 - 30 < 0 deg of usable braking cone -- the bound")
print("  would forbid braking at ANY speed, contradicting 100 per cent success at 3 and")
print("  5 m/s [A-20].  With the tilt added (C1's reading) the coupled bound is 11.8 m/s,")
print("  ABOVE the 7 m/s failure onset.  Neither sign makes leg (1b) active at 7 m/s.")
print("  With the horizontal FoV that a lateral dodge actually uses, the cap is")
print(f"  {min(a_h, G*math.tan(math.radians(45.0))):.2f}-{min(a_h, G*math.tan(math.radians(75.0))):.2f}"
      f" m/s^2 and the bound is "
      f"{stop_bound(6.0, min(a_h, G*math.tan(math.radians(45.0))), 0.107):.2f}-"
      f"{stop_bound(6.0, min(a_h, G*math.tan(math.radians(75.0))), 0.107):.2f} m/s.")

# ---------------------------------------------------------------- E
print()
print("=" * 92)
print("E.  DOES THE BANKED DODGE PUSH THE VELOCITY OUT OF A FORWARD CONE?")
print("=" * 92)
print("  The simulator's dodge (the manoeuvre that carries e_range = +0.986/+1.082)")
print("  rolls about the body-x axis, which stays along the flight direction: a roll")
print("  does NOT move the optical axis off the velocity vector.  The only angular")
print("  excursion is the velocity's own side-slip at the end of the manoeuvre.")
print(f"  {'a_lat (m/s^2)':>14s} {'v (m/s)':>9s} {'v_lat at completion':>20s} "
      f"{'deflection (deg)':>17s} {'inside 45 deg half-HFoV?':>26s}")
for a_lat, v in ((44.26, 16.92), (44.26, 29.41), (42.03, 7.0), (16.33, 7.0)):
    t_man = 2.0 * math.sqrt(0.75 / a_lat)          # symmetric bang-bang, 0.75 m
    v_lat = a_lat * (t_man / 2.0)                  # peak, at the switch
    ang = math.degrees(math.atan2(v_lat, v))
    print(f"  {a_lat:14.2f} {v:9.2f} {v_lat:20.2f} {ang:17.2f} "
          f"{str(ang < 45.0):>26s}")
print("  So for the dodge manoeuvre the solid-angle leg is inactive by construction:")
print("  leg (1b) cannot be what caps the dodge whose elasticity leg (1a) quotes.")

# ---------------------------------------------------------------- F
print()
print("=" * 92)
print("F.  e_s = 1 IS A STRUCTURAL IDENTITY OF THE BOUND, NOT A MEASUREMENT")
print("=" * 92)
s, a, tau, d = sp.symbols("s a tau d", positive=True)
v_dodge = s / (tau + 2 * sp.sqrt(d / a))
e_s = sp.simplify(sp.diff(v_dodge, s) * s / v_dodge)
e_a = sp.simplify(sp.diff(v_dodge, a) * a / v_dodge)
print(f"  dodge bound v = s/(tau + 2 sqrt(d/a)):  d ln v/d ln s = {e_s}  (identically 1)")
print(f"                                          d ln v/d ln a = {sp.simplify(e_a)}")
r = sp.sqrt(tau ** 2 + 2 * s / a)
v_stop = a * (r - tau)
es2 = sp.simplify(sp.diff(v_stop, s) * s / v_stop)
ea2 = sp.simplify(sp.diff(v_stop, a) * a / v_stop)
print(f"  stop bound:   d ln v/d ln s + d ln v/d ln a = {sp.simplify(es2 + ea2)}")
print("  Both hold for EVERY (s, a, tau) > 0, including values where the bound sits")
print("  far above the speed the vehicle achieves.  An elasticity of 1 therefore")
print("  carries no information about which limit binds; it is the statement that the")
print("  bound is homogeneous of degree 1 in the range.")
print()
print("  The metric is the MINIMUM over active bounds.  Elasticity of min(v_perc, v_other):")
print(f"  {'v_perc (m/s)':>13s} {'v_other (m/s)':>14s} {'d ln v_metric/d ln s':>22s}")
for vp, vo in ((16.92, 7.0), (12.0, 7.0), (6.0, 7.0), (6.9, 7.0)):
    e = 1.0 if vp < vo else 0.0
    print(f"  {vp:13.2f} {vo:14.2f} {e:22.2f}")
print("  With the measured 90-per-cent ceiling at <= 5-7 m/s and every perception bound")
print("  computed above at 10-29 m/s, the metric's elasticity to range at the operating")
print("  point is 0, not 1.  The simulator's own attempt to measure a range elasticity")
print("  ON A COURSE (rather than on an isolated dodge) returned nan: every run failed")
print("  at 5 m/s for an unrelated controller reason [simulator F13].")
