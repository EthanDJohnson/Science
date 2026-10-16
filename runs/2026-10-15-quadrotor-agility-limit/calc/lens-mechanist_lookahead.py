#!/usr/bin/env python3
"""Mechanist lens, calculation 1: the look-ahead chain for an UNSEEN obstacle.

SI units throughout (m, s, rad, N, kg, px).

Parts
  1. Required look-ahead distance vs speed, for the stop bound and the lateral-dodge bound,
     with the braking/dodging acceleration TIED to thrust-to-weight (a_h = g sqrt(TWR^2-1))
     instead of left free.  Crossing speed against a stated usable range.
  2. Usable depth range derived from stereo geometry (sigma_z = z^2 sigma_d /(f b)):
     the range at which depth noise equals the obstacle's own size.
  3. Field-of-view geometry: the body tilt a manoeuvre requires, and the longitudinal
     acceleration at which the direction of travel leaves a body-fixed camera's FoV.
  4. Motion blur: pixel smear from body rate and from translation, vs exposure time.
  5. Blind-phase dead-reckoning error from unmodelled aerodynamic force.
  6. Elasticities of the speed bound to range, acceleration, latency, and half-FoV.
"""
import math

g = 9.81  # m/s^2


# ---------------------------------------------------------------- part 1
def v_stop(s, a, tau):
    """Max speed such that v*tau + v^2/(2a) <= s.  m/s."""
    return a * (-tau + math.sqrt(tau ** 2 + 2.0 * s / a))


def v_dodge(s, a, tau, r):
    """Falanga-type lateral dodge: v = s/(tau + 2 sqrt(r/a)).  m/s."""
    return s / (tau + 2.0 * math.sqrt(r / a))


def elast(f, x, **kw):
    """Central-difference log-log elasticity d ln f / d ln x at x."""
    h = 1e-5 * x
    key = kw.pop("key")
    kw1, kw2 = dict(kw), dict(kw)
    kw1[key], kw2[key] = x + h, x - h
    f1, f2 = f(**kw1), f(**kw2)
    return (math.log(f1) - math.log(f2)) / (math.log(x + h) - math.log(x - h))


def a_horiz(twr):
    return g * math.sqrt(twr ** 2 - 1.0)


print("=" * 78)
print("PART 1  required look-ahead vs usable range; braking accel tied to thrust-to-weight")
print("=" * 78)
for twr, label in ((4.4, "onboard-only class (A-13/A-20: T/W 4.4)"),
                   (4.4 * 0.8, "same platform with the planner's 20% thrust margin (D-36)"),
                   (12.35, "mocap high-thrust platform (A-11)")):
    print(f"\nT/W = {twr:.2f}  [{label}]   a_h = {a_horiz(twr):.2f} m/s^2")
    a = a_horiz(twr)
    for tau in (0.05, 0.107, 0.15):
        for s in (3.0, 6.0, 10.0):
            vs = v_stop(s, a, tau)
            vd = v_dodge(s, a, tau, 0.5)
            print(f"   tau={tau*1000:6.1f} ms  s={s:5.1f} m -> v_stop={vs:6.2f} m/s"
                  f"   v_dodge(r=0.5 m)={vd:6.2f} m/s"
                  f"   look-ahead needed at 7 m/s: "
                  f"{7.0*tau + 49.0/(2*a):5.2f} m")

print("\nCrossing speeds: v at which the REQUIRED look-ahead equals the stated usable range")
a = a_horiz(4.4)
tau_perc = 0.1066  # s: 65.2 ms mapping + 41.6 ms policy (A-19), the measured onboard chain
for s in (3.0, 5.0, 6.0, 8.0, 10.0, 15.0):
    vs = v_stop(s, a, tau_perc)
    print(f"   s={s:5.1f} m, tau={tau_perc*1000:.1f} ms, a={a:.1f} m/s^2 -> v_cross={vs:6.2f} m/s"
          f"   (braking distance alone {vs**2/(2*a):5.2f} m, latency term {vs*tau_perc:5.2f} m)")

print("\n  Where the latency term equals the braking term: v = 2 a tau")
for tau in (0.04, 0.1066, 0.15):
    print(f"   tau={tau*1000:6.1f} ms -> v = {2*a*tau:5.2f} m/s  (above this, RANGE dominates"
          f" the budget, not latency)")


# ---------------------------------------------------------------- part 2
print()
print("=" * 78)
print("PART 2  usable depth range from stereo geometry: sigma_z = z^2 sigma_d / (f b)")
print("=" * 78)
# D435i-class active stereo: baseline 50 mm, VGA 640x480 depth, depth HFoV about 87 deg.
b = 0.050            # m, baseline
W_px = 640           # px, depth image width
hfov = math.radians(87.0)
f_px = (W_px / 2.0) / math.tan(hfov / 2.0)   # px, pinhole focal length
print(f"  baseline b = {b*1000:.0f} mm, width {W_px} px, HFoV {math.degrees(hfov):.0f} deg"
      f" -> f = {f_px:.1f} px")
for sigma_d in (0.05, 0.1, 0.2):   # px, disparity matching noise
    row = []
    for z in (3.0, 5.0, 8.0, 10.0, 15.0):
        sz = z ** 2 * sigma_d / (f_px * b)
        row.append(f"z={z:4.1f} m: {sz:5.3f} m")
    print(f"  sigma_d={sigma_d:4.2f} px -> " + "  ".join(row))
for sigma_d in (0.05, 0.1, 0.2):
    for r_obs in (0.1, 0.5):
        z_use = math.sqrt(r_obs * f_px * b / sigma_d)
        print(f"  range where sigma_z equals obstacle half-size {r_obs:.2f} m "
              f"(sigma_d={sigma_d:.2f} px): z = {z_use:5.2f} m")
# angular resolution floor: a thin obstacle must subtend >= a few pixels
for d_obs, npx in ((0.05, 3.0), (0.1, 3.0), (0.3, 3.0)):
    z_ang = d_obs * f_px / npx
    print(f"  range where a {d_obs*100:4.1f} cm obstacle subtends {npx:.0f} px: z = {z_ang:5.2f} m")


# ---------------------------------------------------------------- part 3
print()
print("=" * 78)
print("PART 3  field-of-view geometry: the manoeuvre tilts the camera off the flight path")
print("=" * 78)
print("  tilt required for a horizontal acceleration a_x:  theta = atan(a_x/g)")
for ax in (5.0, 10.0, 20.0, 30.0, 38.0):
    print(f"   a_x={ax:5.1f} m/s^2 -> tilt {math.degrees(math.atan(ax/g)):5.1f} deg")
print("\n  largest |a_x| for which the flight direction stays inside a body-fixed FoV:")
print("    a_x,max = g tan(half-FoV + camera mount tilt)")
cams = [("D435i depth, vertical FoV 58 deg, level mount", 58.0, 0.0),
        ("D435i depth, vertical FoV 58 deg, mounted 30 deg up (A-20 above 7 m/s)", 58.0, 30.0),
        ("D435i depth, horizontal FoV 87 deg (lateral dodge)", 87.0, 0.0),
        ("MonoRace lens 155 x 115 deg, vertical 115 deg (A-26)", 115.0, 0.0),
        ("MonoRace lens, horizontal 155 deg (A-26)", 155.0, 0.0)]
for name, fov, mount in cams:
    half = fov / 2.0 + mount
    if half >= 89.9:
        print(f"   {name:72s}: half+mount = {half:5.1f} deg -> no tilt limit")
        continue
    axm = g * math.tan(math.radians(half))
    print(f"   {name:72s}: half+mount = {half:5.1f} deg -> a_x,max = {axm:6.2f} m/s^2"
          f"  (= {axm/g:4.2f} g); stop-bound speed at s=6 m, tau=107 ms:"
          f" {v_stop(6.0, axm, tau_perc):5.2f} m/s")
print("\n  Interpretation: beyond a_x,max the vehicle brakes or dodges BLIND (the obstacle and")
print("  the future path leave the image), so the usable acceleration in the look-ahead bound")
print("  is min(a_h, a_x,max), not a_h.")
print("\n  the same thing as a look-ahead TIME: at the tilt the manoeuvre needs, the scene point")
print("  the vehicle will reach in t seconds is in view only if its bearing < half-FoV.")
for v in (5.0, 7.0, 10.0, 15.0):
    a_lat = a_horiz(4.4)
    for s in (6.0,):
        psi_dot = a_lat / v                       # rad/s, heading rate in a max-g turn
        bearing = 0.5 * psi_dot * (s / v)         # rad, mid-path bearing offset
        print(f"   v={v:5.1f} m/s, max-g turn (a_lat={a_lat:.1f} m/s^2), look-ahead s={s:.0f} m:"
              f" path bearing offset {math.degrees(bearing):6.1f} deg"
              f" -> needs half-FoV >= that")


# ---------------------------------------------------------------- part 4
print()
print("=" * 78)
print("PART 4  motion blur in pixels: rotational f*omega*t_exp, translational f*v_perp*t_exp/z")
print("=" * 78)
f_rgb = (848 / 2.0) / math.tan(math.radians(87.0) / 2.0)  # px, same lens at 848 px wide
print(f"  f = {f_rgb:.1f} px (848 px wide, 87 deg HFoV)")
for texp in (0.001, 0.002, 0.005, 0.010):
    for wdeg in (100.0, 500.0, 1000.0):
        w = math.radians(wdeg)
        blur_rot = f_rgb * w * texp
        print(f"   t_exp={texp*1000:5.1f} ms, body rate {wdeg:6.0f} deg/s ->"
              f" {blur_rot:7.2f} px rotational blur")
    for v, z in ((10.0, 5.0), (20.0, 5.0), (20.0, 10.0)):
        blur_tr = f_rgb * v * texp / z
        print(f"   t_exp={texp*1000:5.1f} ms, v_perp={v:4.1f} m/s at z={z:4.1f} m ->"
              f" {blur_tr:7.2f} px translational blur")
print("  ratio rotational/translational at 500 deg/s, 20 m/s, 5 m:"
      f" {(math.radians(500.0))/(20.0/5.0):5.2f}")


# ---------------------------------------------------------------- part 5
print()
print("=" * 78)
print("PART 5  dead-reckoning error during the blind phase, from unmodelled aero force")
print("=" * 78)
m = 0.75  # kg (A-01)
for F_rms in (0.36, 1.0, 2.0):   # N; 0.352-0.365 N is the NeuroBEM BEM+NN force RMSE (A-18)
    da = F_rms / m
    for v in (7.0, 10.0, 20.0):
        tb = v / a_horiz(4.4)
        dx = 0.5 * da * tb ** 2
        print(f"   force error {F_rms:4.2f} N -> {da:5.2f} m/s^2; braking from {v:4.1f} m/s"
              f" takes {tb:5.3f} s -> position error {dx*100:6.2f} cm")


# ---------------------------------------------------------------- part 6
print()
print("=" * 78)
print("PART 6  elasticities of the stop bound and the dodge bound at the measured operating point")
print("=" * 78)
base = dict(s=6.0, a=a_horiz(4.4), tau=tau_perc)
v0 = v_stop(**base)
print(f"  operating point: s=6 m, a={base['a']:.2f} m/s^2, tau={tau_perc*1000:.1f} ms"
      f" -> v_stop={v0:.3f} m/s")
for k in ("s", "a", "tau"):
    print(f"   d ln v / d ln {k:3s} = {elast(v_stop, base[k], key=k, **{kk: vv for kk, vv in base.items() if kk != k}):+6.3f}")
bd = dict(s=6.0, a=a_horiz(4.4), tau=tau_perc, r=0.5)
print(f"  dodge bound at the same point -> v_dodge={v_dodge(**bd):.3f} m/s")
for k in ("s", "a", "tau", "r"):
    print(f"   d ln v / d ln {k:3s} = {elast(v_dodge, bd[k], key=k, **{kk: vv for kk, vv in bd.items() if kk != k}):+6.3f}")

print("\n  elasticity to half-FoV, through a = min(a_h, g tan(half)):")


def v_fov(s, tau, half_deg, twr=4.4):
    a_fov = g * math.tan(math.radians(half_deg))
    return v_stop(s, min(a_horiz(twr), a_fov), tau)


for half in (25.0, 29.0, 43.5, 57.5, 70.0):
    v = v_fov(6.0, tau_perc, half)
    e = elast(v_fov, half, key="half_deg", s=6.0, tau=tau_perc)
    print(f"   half-FoV={half:5.1f} deg -> v={v:6.2f} m/s, d ln v / d ln(half-FoV) = {e:+6.3f}")

print("\n  side-by-side: per cent speed gain from a 10 per cent relaxation of each limit")
for k, lab in (("s", "usable range"), ("a", "usable accel"), ("tau", "latency")):
    kw = {kk: vv for kk, vv in base.items() if kk != k}
    kw[k] = base[k] * (1.1 if k != "tau" else 0.9)
    print(f"   {lab:13s}: {100*(v_stop(**kw)/v0 - 1):+6.2f} %")
kwf = dict(s=6.0, tau=tau_perc, half_deg=29.0)
v_at29 = v_fov(**kwf)
kwf2 = dict(kwf); kwf2["half_deg"] = 29.0 * 1.1
print(f"   half-FoV     : {100*(v_fov(**kwf2)/v_at29 - 1):+6.2f} %  (from 29 deg, FoV-limited)")
