#!/usr/bin/env python3
"""M-MECH-05  Rotor spin-down closed form and the rotor inertia it implies.

CLAIM (mechanist finding 5)
  Symbols, SI: J_r rotor-group polar inertia [kg m^2]; k_m = 2.37e-8 N m s^2/rad^2 the drag-torque
  coefficient of omega^2 (Sun et al. TABLE II c_q); omega(t) rotor speed [rad/s];
  omega_0 = omega_hover = 1103 rad/s; t_c = J_r/(k_m omega_0) [s].
  Assumptions: fixed-pitch unidirectional rotor, no active braking, aerodynamic drag torque
  k_m omega^2 the only torque, no motor or ESC torque, thrust = k_f omega^2.
  Claimed: J_r omega' = -k_m omega^2 has the exact solution omega(t) = omega_0/(1 + t/t_c) with
  t_c = J_r/(k_m omega_0); identifying t_c with the measured 39.1 ms thrust time constant gives
  J_r = 1.0e-6 kg m^2 and with the 33 ms rotor-speed constant 8.6e-7 kg m^2; a 1e-5 kg m^2 rotor
  group would give t_c = 382 ms and 20.7 ms to shed 10 per cent of thrust.
"""
import math
import sys

import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, limit, quantity, units  # noqa: E402

KM, W0 = 2.37e-8, 1103.0
print(f"inputs: k_m = {KM:g} N m s^2/rad^2, omega_0 = {W0} rad/s")

# ---------------------------------------------------------------- closed form solves the ODE
t, Jr, km, w0 = sp.symbols("t J_r k_m w0", positive=True)
tc = Jr / (km * w0)
w = w0 / (1 + t / tc)
residual = sp.simplify(Jr * sp.diff(w, t) + km * w**2)
sp.pprint(residual)
from math_checks import identity  # noqa: E402
identity(residual, sp.Integer(0), domain={"t": (0.0, 10), "J_r": (1e-3, 10), "k_m": (1e-3, 10),
                                          "w0": (0.1, 10)})
limit(w, "t", 0, w0)                     # initial condition
limit(w, "t", "oo", 0)                   # the rotor coasts to rest
# small-time expansion: omega ~ omega_0 (1 - t/t_c), i.e. the initial slope is -k_m w0^2/J_r
from math_checks import series  # noqa: E402
series(w, "t", 0, 2, w0 - km * w0**2 * t / Jr)
units("1e-6 kg m^2/((2.37e-8 N m s^2)*(1103/s))", "s")

# ---------------------------------------------------------------- J_r implied by a constant
for tcv, label in ((0.0391, "39.1 ms (thrust constant, read as t_c)"),
                   (0.033, "33 ms (rotor-speed constant, read as t_c)")):
    J = tcv * KM * W0
    print(f"t_c = {label}: J_r = {J:.4g} kg m^2")
quantity(f"{0.0391*KM*W0:.8g} kg m^2", "1.0e-6 kg m^2", rel_tol=3e-2)
quantity(f"{0.033*KM*W0:.8g} kg m^2", "8.6e-7 kg m^2", rel_tol=3e-2)

# convention check: t_c is the HALF-LIFE of omega, not its 1/e time, and thrust ~ omega^2
t_1e_w = (math.e - 1)                     # in units of t_c: omega falls to 1/e
t_1e_f = (math.e**0.5 - 1)                # thrust falls to 1/e
print(f"in units of t_c: omega -> 1/e at t = {t_1e_w:.4f} t_c, thrust -> 1/e at t = {t_1e_f:.4f} t_c")
print(f"if 39.1 ms is the THRUST 1/e time, t_c = {0.0391/t_1e_f*1e3:.1f} ms and "
      f"J_r = {0.0391/t_1e_f*KM*W0:.3g} kg m^2 (1.6x the lens's value)")
print(f"if 33 ms is the ROTOR-SPEED 1/e time, t_c = {0.033/t_1e_w*1e3:.1f} ms and "
      f"J_r = {0.033/t_1e_w*KM*W0:.3g} kg m^2")

# ---------------------------------------------------------------- the 1e-5 kg m^2 rotor group
tc_big = 1e-5 / (KM * W0)
t_10pct = (1 / math.sqrt(0.9) - 1) * tc_big      # thrust ~ (1 + t/t_c)^-2 = 0.9
print(f"J_r = 1e-5 kg m^2 -> t_c = {tc_big*1e3:.1f} ms (lens 382 ms), "
      f"10 per cent of thrust shed in {t_10pct*1e3:.2f} ms (lens 20.7 ms)")
quantity(f"{tc_big:.8f} s", "382 ms", rel_tol=5e-3)
quantity(f"{t_10pct:.8f} s", "20.7 ms", rel_tol=1e-2)

raise SystemExit(finish())
