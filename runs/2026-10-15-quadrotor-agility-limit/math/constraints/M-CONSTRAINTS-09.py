"""M-CONSTRAINTS-09: the stop / look-ahead bound with reorientation time (lens finding F11,
candidate CONSTRAINTS-A).

Claim as I state it (SI units):
  A point mass flying at speed v towards a newly revealed static obstacle at range s reacts
  after a total dead time tau_tot = tau_sense + t_reorient, during which it travels v*tau_tot
  at constant speed, and then brakes at constant deceleration a > 0, needing v^2/(2a).
  Feasibility: v*tau_tot + v^2/(2a) <= s.  The boundary speed is
      v*(s, a, tau) = -a tau + sqrt((a tau)^2 + 2 a s).
  The reorientation time is the rest-to-rest bang-bang slew through angle theta at constant
  angular acceleration alpha: t_reorient = 2 sqrt(theta/alpha).
  Numbers the lens uses: alpha = 396.2 rad/s^2 (M-CONSTRAINTS-02), a = 39.0 m/s^2,
  tau_sense = 0.040 s, theta = 76 deg -> t_reorient = 116 ms (90 deg -> 126 ms);
  v* = 26.4 -> 22.5 m/s at s = 10 m and 20.1 -> 16.4 m/s at s = 6 m; elasticities
  d ln v*/d ln tau = -0.056 (sensing only) and -0.212 (with reorientation), of which
  tau_sense alone contributes -0.054; d ln v*/d ln s = +0.53 ... +0.64; required look-ahead
  1.10 / 2.84 / 5.22 / 8.24 m at 5 / 10 / 15 / 20 m/s with reaction fractions 71/55/45/38 %.
Domain: v, a, s, tau all > 0; a constant (no tilt dynamics during braking); single obstacle.
"""
import sys
import math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, inequality, units, quantity, finish


def approx(label, got, want, rel=0.015):
    print(f"  {label}: got {got:.6g}, lens {want:.6g}")
    return inequality(f"Abs({got!r} - ({want!r}))", "<", f"{rel}*Abs({want!r})")


v, a, s, tau, th, al = sp.symbols("v a s tau th al", positive=True)

# --- 1. the boundary speed solves the bound with equality
vstar = -a * tau + sp.sqrt((a * tau) ** 2 + 2 * a * s)
print("1. v* satisfies v tau + v^2/(2a) = s identically")
identity(sp.simplify(vstar * tau + vstar ** 2 / (2 * a)), s)

# --- 2. limits: no dead time -> Torricelli; large dead time -> s/tau
print("2. limits")
limit(vstar, "tau", 0, sp.sqrt(2 * a * s))
limit(vstar, "a", "oo", s / tau)   # infinite braking: the dead time alone sets the speed
units("5 m/s * 0.1557 s + (5 m/s)^2/(2 * 39.0 m/s^2)", "m")
units("1.3265 rad / (396.2 rad/s^2)", "s^2")

# --- 3. reorientation time
print("3. t_reorient = 2 sqrt(theta/alpha), alpha = 396.2 rad/s^2")
alpha = 396.2
t76 = 2.0 * math.sqrt(math.radians(76.0) / alpha)
t90 = 2.0 * math.sqrt(math.radians(90.0) / alpha)
approx("t_reorient(76 deg) [s]", t76, 0.116, rel=0.02)
approx("t_reorient(90 deg) [s]", t90, 0.126, rel=0.02)
# the closed form itself: bang-bang through theta, half the angle in half the time
t_sym = sp.Symbol("t_sym", positive=True)
identity(2 * sp.sqrt(th / al), sp.solve(sp.Eq(al * t_sym ** 2 / 4, th), t_sym)[0])

# --- 4. the numbers
A_BRAKE = 39.0
TS = 0.040
TT = TS + t76
print(f"4. a = {A_BRAKE} m/s^2, tau_sense = {TS} s, tau_tot = {TT:.5f} s")


def vmax(s_m, tau_s, a_b=A_BRAKE):
    return -a_b * tau_s + math.sqrt((a_b * tau_s) ** 2 + 2 * a_b * s_m)


approx("v*(s=10 m, sensing only) [m/s]", vmax(10.0, TS), 26.4)
approx("v*(s=10 m, + reorient) [m/s]", vmax(10.0, TT), 22.5)
approx("v*(s=6 m, sensing only) [m/s]", vmax(6.0, TS), 20.1)
approx("v*(s=6 m, + reorient) [m/s]", vmax(6.0, TT), 16.4)
quantity(f"{vmax(10.0, TT):.6f} m/s", "22.5 m/s", rel_tol=3e-3)

# --- 5. elasticities, symbolic then numeric
el_tau = sp.simplify(sp.diff(vstar, tau) * tau / vstar)
el_s = sp.simplify(sp.diff(vstar, s) * s / vstar)
print("5. elasticities  d ln v*/d ln tau =", el_tau, "   d ln v*/d ln s =", el_s)
f_tau = sp.lambdify((a, s, tau), el_tau)
f_s = sp.lambdify((a, s, tau), el_s)
approx("e_tau (s=10, sensing only)", float(f_tau(A_BRAKE, 10.0, TS)), -0.056, rel=0.03)
approx("e_tau (s=10, with reorient)", float(f_tau(A_BRAKE, 10.0, TT)), -0.212, rel=0.02)
approx("e_tau_sense alone = e_tau * tau_s/tau_tot",
       float(f_tau(A_BRAKE, 10.0, TT)) * TS / TT, -0.054, rel=0.03)
approx("e_s (s=10, sensing only)", float(f_s(A_BRAKE, 10.0, TS)), 0.53, rel=0.02)
approx("e_s (s=6, with reorient)", float(f_s(A_BRAKE, 6.0, TT)), 0.64, rel=0.02)
# a finite-difference cross-check of the symbolic elasticity
h = 1e-4
fd = (math.log(vmax(10.0, TT * (1 + h))) - math.log(vmax(10.0, TT * (1 - h)))) / (2 * h)
approx("e_tau by finite difference", fd, float(f_tau(A_BRAKE, 10.0, TT)), rel=1e-4)
# sign: more dead time can only reduce the admissible speed
inequality("a*tau/sqrt((a*tau)**2 + 2*a*s)", "<", "1", domain={"a": (1.0, 100.0), "s": (0.5, 50.0), "tau": (0.001, 1.0)})

# --- 6. required look-ahead and the reaction fraction
print("6. required look-ahead s(v) = v tau_tot + v^2/(2a)")
for vv, want_s, want_frac in ((5.0, 1.10, 71.0), (10.0, 2.84, 55.0), (15.0, 5.22, 45.0), (20.0, 8.24, 38.0)):
    react = vv * TT
    need = react + vv * vv / (2 * A_BRAKE)
    approx(f"s_req({vv} m/s) [m]", need, want_s, rel=0.01)
    approx(f"reaction fraction at {vv} m/s [%]", 100.0 * react / need, want_frac, rel=0.02)

# --- 7. candidate arithmetic: 2^0.53 and 2^0.040
print("7. elasticity-to-factor arithmetic in CONSTRAINTS-A")
approx("2^0.53", 2.0 ** 0.53, 1.44, rel=0.01)
approx("5 m/s * 2^0.53 [m/s]", 5.0 * 2.0 ** 0.53, 7.2, rel=0.01)
approx("2^0.040", 2.0 ** 0.040, 1.03, rel=0.01)

raise SystemExit(finish())
