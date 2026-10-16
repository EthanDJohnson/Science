#!/usr/bin/env python3
"""M-MECH-03  One-at-a-time elasticities of the coupled stop bound.

CLAIM (mechanist finding 3, candidates MECH-A and MECH-NULL)
  The bound v(a_u, s, tau_eff) = a_u (sqrt(tau_eff^2 + 2 s/a_u) - tau_eff), with
  a_u = min(a_h, g tan(phi)), phi = half-FoV + mount tilt, tau_eff = tau_sense + tau_rot/2 and
  tau_rot = 2 sqrt(atan(a_u/g)/alpha_max), evaluated at s = 6 m, tau_sense = 107 ms, half-FoV
  29 deg, mount 30 deg (so phi = 59 deg), a_h = 44.25 m/s^2, alpha_max = 633.7 rad/s^2.
  Claimed per +10 per cent relaxation of one limit: half-FoV +10.5 %, range +5.7 %, sensing
  latency (-10 %) +1.2 %, motor time constant (-10 %) +0.11 %, thrust-to-weight +0.00 %;
  and elasticities d ln v/d ln s = +0.58..0.60, d ln v/d ln a = +0.40,
  d ln v/d ln tau = -0.08..-0.20, d ln v/d ln(half-FoV) = +0.55 at 29 deg rising to +1.6 at 70 deg.
  Checked here: the analytic elasticities of the bound, and each one-at-a-time perturbation,
  distinguishing a +10 per cent change in the HALF-FoV alone from a +10 per cent change in the
  sum phi = half-FoV + mount.
"""
import math
import sys

import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, quantity  # noqa: E402

G = 9.81
M, L, BETA, JY, FMAX = 0.75, 0.14, math.radians(56.0), 2.1e-3, 8.5
A_H = G * math.sqrt((4 * FMAX / (M * G)) ** 2 - 1)
ALPHA = L * math.cos(BETA) * 2 * FMAX / JY
S0, TAU_S0, HALF0, MOUNT0, MTAU0 = 6.0, 0.107, 29.0, 30.0, 0.0391
print(f"inputs: a_h = {A_H:.3f} m/s^2, alpha_max = {ALPHA:.1f} rad/s^2, s = {S0} m, "
      f"tau_sense = {TAU_S0*1e3:.0f} ms, half-FoV = {HALF0} deg, mount = {MOUNT0} deg")


def tau_rot(theta, mtau):
    """Rest-to-rest bang-bang rotation time through theta with a first-order lag on the torque.

    Ideal (mtau = 0): 2 sqrt(theta/alpha). With a lag the accumulated angle at the switch time
    t_s is alpha [t_s^2/2 - mtau t_s + mtau^2 (1 - exp(-t_s/mtau))]; by symmetry the total is
    twice that and the total time 2 t_s.
    """
    if mtau <= 0:
        return 2 * math.sqrt(theta / ALPHA)
    f = lambda t: 2 * ALPHA * (t * t / 2 - mtau * t + mtau**2 * (1 - math.exp(-t / mtau))) - theta
    lo, hi = 1e-6, 10.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return 2 * 0.5 * (lo + hi)


def speed(half_deg=HALF0, mount_deg=MOUNT0, s=S0, tau_s=TAU_S0, a_h=A_H, mtau=MTAU0,
          use_rot=True):
    phi = math.radians(half_deg + mount_deg)
    a_u = min(a_h, G * math.tan(phi))
    theta = math.atan(a_u / G)
    tau_eff = tau_s + (tau_rot(theta, mtau) / 2 if use_rot else 0.0)
    return a_u * (math.sqrt(tau_eff**2 + 2 * s / a_u) - tau_eff), a_u, tau_eff


v0, au0, taueff0 = speed()
print(f"baseline: a_u = {au0:.3f} m/s^2, tau_eff = {taueff0*1e3:.1f} ms, v = {v0:.3f} m/s")

pert = {
    "half-FoV +10 % (half-FoV alone, 29 -> 31.9 deg)": speed(half_deg=HALF0 * 1.1)[0],
    "phi +10 % (half-FoV + mount, 59 -> 64.9 deg)": speed(half_deg=HALF0 * 1.1 + MOUNT0 * 0.1)[0],
    "range +10 % (6 -> 6.6 m)": speed(s=S0 * 1.1)[0],
    "sensing latency -10 % (107 -> 96.3 ms)": speed(tau_s=TAU_S0 * 0.9)[0],
    "motor tau -10 % (39.1 -> 35.2 ms)": speed(mtau=MTAU0 * 0.9)[0],
    "thrust-to-weight +10 % (a_h 44.25 -> 49.2 m/s^2)": speed(a_h=G * math.sqrt((1.1 * 4 * FMAX / (M * G)) ** 2 - 1))[0],
}
for k, vv in pert.items():
    print(f"{k:52s} v = {vv:7.4f} m/s   change {100*(vv/v0-1):+6.2f} %")

quantity(f"{100*(pert['range +10 % (6 -> 6.6 m)']/v0-1):.6f} m", "5.7 m", rel_tol=3e-2)
quantity(f"{100*(pert['sensing latency -10 % (107 -> 96.3 ms)']/v0-1):.6f} m", "1.2 m", rel_tol=1e-1)
quantity(f"{100*(pert['thrust-to-weight +10 % (a_h 44.25 -> 49.2 m/s^2)']/v0-1):.6f} m",
         "0.0 m", rel_tol=1e-9)
# the lens's headline +10.5 % for "half-FoV +10 %":
quantity(f"{100*(pert['half-FoV +10 % (half-FoV alone, 29 -> 31.9 deg)']/v0-1):.6f} m",
         "10.5 m", rel_tol=5e-2)
quantity(f"{100*(pert['phi +10 % (half-FoV + mount, 59 -> 64.9 deg)']/v0-1):.6f} m",
         "10.5 m", rel_tol=5e-2)
# ranking claim: does the half-FoV perturbation beat the range perturbation?
half_pct = 100 * (pert["half-FoV +10 % (half-FoV alone, 29 -> 31.9 deg)"] / v0 - 1)
range_pct = 100 * (pert["range +10 % (6 -> 6.6 m)"] / v0 - 1)
print(f"RANKING: half-FoV {half_pct:.2f} % vs range {range_pct:.2f} % -> "
      f"{'FoV wins' if half_pct > range_pct else 'RANGE wins'}; ratio {half_pct/range_pct:.3f}")

# ---------------------------------------------------------------- analytic elasticities
v, tau, s, a = sp.symbols("v tau s a", positive=True)
vb = a * (sp.sqrt(tau**2 + 2 * s / a) - tau)
e_s = sp.simplify(s * sp.diff(vb, s) / vb)
e_a = sp.simplify(a * sp.diff(vb, a) / vb)
e_t = sp.simplify(tau * sp.diff(vb, tau) / vb)
# closed forms: with r = sqrt(tau^2 + 2 s/a),  e_s = 1/(r(r - tau)),  e_t = -tau/(r - tau) * (1 - tau/r)... check numerically
r = sp.sqrt(tau**2 + 2 * s / a)
dom = {"a": (1, 100), "tau": (0.0, 1), "s": (0.1, 50)}
# closed forms from v = a(r - tau), 2 s/a = r^2 - tau^2:
identity(e_s, (r + tau) / (2 * r), domain=dom)
identity(e_a, 1 - (r + tau) / (2 * r), domain=dom)
identity(e_t, -tau / r, domain=dom)
subs0 = {a: au0, tau: taueff0, s: S0}
print(f"d ln v/d ln s   = {float(e_s.subs(subs0)):+.4f}   (lens: +0.58..0.60)")
print(f"d ln v/d ln a   = {float(e_a.subs(subs0)):+.4f}   (lens: +0.40)")
print(f"d ln v/d ln tau = {float(e_t.subs(subs0)):+.4f}   (lens: -0.08..-0.20)")
quantity(f"{float(e_s.subs(subs0)):.6f} m", "0.59 m", rel_tol=5e-2)
quantity(f"{float(e_a.subs(subs0)):.6f} m", "0.40 m", rel_tol=5e-2)

# d ln v/d ln(half-FoV) at 29 deg and at 70 deg, level mount (no mount tilt)
for hd, want in ((29.0, 0.55), (70.0, 1.6)):
    vA = speed(half_deg=hd, mount_deg=0.0)[0]
    vB = speed(half_deg=hd * 1.001, mount_deg=0.0)[0]
    ela = math.log(vB / vA) / math.log(1.001)
    print(f"d ln v/d ln(half-FoV) at {hd} deg (level mount) = {ela:+.3f}   (lens: {want})")
    quantity(f"{ela:.6f} m", f"{want} m", rel_tol=1.5e-1)

raise SystemExit(finish())
