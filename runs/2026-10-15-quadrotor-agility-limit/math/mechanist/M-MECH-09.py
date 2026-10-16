#!/usr/bin/env python3
"""M-MECH-09  Burst electrical power at the thrust ceiling, pack sag, and the T/W it costs.

CLAIM (mechanist finding 9)
  Symbols: T total thrust [N]; rho = 1.225 kg/m^3; A total rotor disc area [m^2] (four 5-inch
  rotors, R = 0.0635 m); FM = 0.65 propeller figure of merit; eta = 0.8 motor+ESC efficiency;
  P_elec = T^1.5/(sqrt(2 rho A) FM eta) [W]; V = 14.8 V nominal 4S (16.8 V full);
  R_int = 20 mOhm assumed pack resistance; thrust proportional to V^2.
  Assumptions: hover-like momentum theory (no forward-flight inflow), uniform disc loading,
  all four rotors at the limit, constant efficiencies.
  Claimed: P = 1130 W at 35 N, 1354 W at 40 N, 2729 W at 63 N; 76 / 91 / 184 A at 14.8 V, i.e.
  42-102 C on an 1800 mAh pack; 90 A through 20 mOhm sags the pack 10.7 per cent, turning
  T/W 4.40 into 3.51 and a_h from 42.0 into 33.0 m/s^2, which "costs ~4 per cent of speed"
  given d ln v/d ln a ~ 0.4.
"""
import math
import sys

import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import finish, identity, limit, quantity, units  # noqa: E402

RHO, R, FM, ETA = 1.225, 0.0635, 0.65, 0.8
A = 4 * math.pi * R**2
G = 9.81
print(f"inputs: rho = {RHO} kg/m^3, R = {R} m (5 inch), A = {A:.6f} m^2, FM = {FM}, eta = {ETA}")

# momentum theory: v_i = sqrt(T/(2 rho A)), P_ideal = T v_i
T, rho, Ad = sp.symbols("T rho A_d", positive=True)
v_i = sp.sqrt(T / (2 * rho * Ad))
identity(sp.simplify(T * v_i), T ** sp.Rational(3, 2) / sp.sqrt(2 * rho * Ad),
         domain={"T": (1, 100), "rho": (0.5, 2), "A_d": (0.01, 1)})
limit(T * v_i, "T", 0, 0)
units("35 N/(2*1.225 kg/m^3 * 0.0507 m^2)", "m^2/s^2")
units("35 N * 16.6 m/s", "W")


def p_elec(Tn, area=A):
    return Tn**1.5 / math.sqrt(2 * RHO * area) / (FM * ETA)


for Tn, want in ((35.0, "1130 W"), (40.0, "1354 W"), (63.0, "2729 W")):
    P = p_elec(Tn)
    print(f"T = {Tn:5.1f} N: v_i = {math.sqrt(Tn/(2*RHO*A)):5.2f} m/s, P_elec = {P:7.1f} W"
          f"   (lens: {want}); current at 14.8 V = {P/14.8:6.1f} A, "
          f"C-rate on 1800 mAh = {P/14.8/1.8:5.1f} C")
quantity(f"{p_elec(35.0):.6f} W", "1130 W", rel_tol=1e-2)
quantity(f"{p_elec(63.0):.6f} W", "2729 W", rel_tol=1e-2)
quantity(f"{p_elec(40.0):.6f} W", "1354 W", rel_tol=1e-2)
# what disc area would be needed for 1354 W at 40 N?
area_needed = (40.0**1.5 / (1354 * FM * ETA)) ** 2 / (2 * RHO)
print(f"1354 W at 40 N needs A = {area_needed:.5f} m^2, i.e. R = "
      f"{math.sqrt(area_needed/(4*math.pi)):.4f} m ({math.sqrt(area_needed/(4*math.pi))/0.0254*2:.1f} inch props)")
quantity(f"{p_elec(40.0)/p_elec(35.0):.6f} m", f"{(40/35)**1.5:.6f} m", rel_tol=1e-9)
quantity(f"{p_elec(35.0)/14.8:.6f} m", "76 m", rel_tol=1e-2)
quantity(f"{p_elec(63.0)/14.8:.6f} m", "184 m", rel_tol=1e-2)

# ---------------------------------------------------------------- sag and the T/W it costs
I = 90.0
dV = I * 0.020
for Vref in (14.8, 16.8):
    print(f"90 A x 20 mOhm = {dV:.2f} V sag = {100*dV/Vref:.1f} per cent of {Vref} V")
quantity(f"{100*dV/16.8:.6f} m", "10.7 m", rel_tol=1e-2)      # the lens used 16.8 V (4S full)
units("90 A * 0.020 ohm", "V")

sag = dV / 16.8
twr_sag = 4.40 * (1 - sag) ** 2
a_sag = G * math.sqrt(twr_sag**2 - 1)
print(f"T/W 4.40 -> {twr_sag:.3f} (thrust ~ V^2); a_h 42.03 -> {a_sag:.2f} m/s^2")
quantity(f"{twr_sag:.6f} m", "3.51 m", rel_tol=5e-3)
quantity(f"{a_sag:.6f} m/s^2", "33.0 m/s^2", rel_tol=5e-3)

# the speed cost: d ln v/d ln a ~ 0.4 applied to the change in a, not to the voltage sag
dln_a = math.log(a_sag / 42.034448)
print(f"d ln a_h = {dln_a:+.4f} ({100*dln_a:+.1f} per cent), so with d ln v/d ln a = 0.40 "
      f"the speed cost is {100*0.40*dln_a:+.2f} per cent   (lens: ~ -4 per cent)")
print(f"0.40 x the VOLTAGE sag (-10.7 per cent) would be {0.40*-10.7:+.2f} per cent - "
      f"the chain the lens's 4 per cent matches")
quantity(f"{abs(100*0.40*dln_a):.6f} m", "4.0 m", rel_tol=1e-1)

raise SystemExit(finish())
