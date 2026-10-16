"""M-CONSTRAINTS-03: momentum-theory power, battery C-rate and lap energy (lens finding F12,
constraint-table row C9).

Claim as I state it (SI units):
  Ideal (induced) hover power of one rotor of disc area A at thrust T_r in air of density rho is
  P = T_r^1.5 / sqrt(2 rho A); for four rotors P_ideal = 4 T_r^1.5/sqrt(2 rho A).  Electrical
  power is P_ideal/FoM with a figure of merit 0.65-0.75.  Disc: 5-inch propeller, R = 0.0635 m,
  A = pi R^2 = 0.012668 m^2, rho = 1.225 kg/m^3.
  Numbers claimed: hover (T = m g = 8.535 N) 71 W ideal -> 94-109 W electrical, 3.5-4.1 C on a
  4S 1800 mAh (26.6 Wh) pack; half throttle (T = 2 f_max = 17.5 N) 208 W -> 277-320 W
  (9.6-12.0 C); full throttle (T = 35 N) 588 W -> 784-904 W (27-34 C, 53-61 A); and a 75 m lap
  at 15 m/s costs 0.41 Wh = 1.5 per cent of the pack.
Domain: rho, A, T_r > 0, 0 < FoM <= 1; hover (zero forward speed), uniform inflow.
"""
import sys
import math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, limit, inequality, units, quantity, finish


def approx(label, got, want, rel=0.015):
    print(f"  {label}: got {got:.6g}, lens {want:.6g}")
    return inequality(f"Abs({got!r} - ({want!r}))", "<", f"{rel}*Abs({want!r})")


RHO, R_PROP = 1.225, 0.0635
A_DISC = math.pi * R_PROP ** 2
print(f"A_disc = {A_DISC:.6f} m^2 per rotor")

print("1. momentum theory from first principles: T = 2 rho A v_i^2, P = T v_i")
tt, rh, aa = sp.symbols("tt rh aa", positive=True)
v_i = sp.sqrt(tt / (2 * rh * aa))
identity(sp.simplify(tt * v_i), tt ** sp.Rational(3, 2) / sp.sqrt(2 * rh * aa))
limit(tt * v_i / tt ** sp.Rational(3, 2), "aa", "oo", 0)      # an infinite disc costs no power
units("(2.1337 N)^1.5 / (2 * 1.225 kg/m^3 * 0.012668 m^2)^0.5", "W")


def p_ideal(T_total):
    return 4.0 * (T_total / 4.0) ** 1.5 / math.sqrt(2.0 * RHO * A_DISC)


PACK_WH, PACK_V, PACK_AH = 14.8 * 1.8, 14.8, 1.8
approx("pack energy [Wh]", PACK_WH, 26.6, rel=0.01)
cases = [("hover", 0.870 * 9.81, 71.0, 94.0, 109.0, 3.5, 4.1),
         ("half throttle", 17.5, 208.0, 277.0, 320.0, 9.6, 12.0),
         ("full throttle", 35.0, 588.0, 784.0, 904.0, 27.0, 34.0)]
for name, T, want_id, want_lo, want_hi, want_clo, want_chi in cases:
    pid = p_ideal(T)
    lo, hi = pid / 0.75, pid / 0.65
    print(f"   {name}: T = {T:.3f} N -> P_ideal = {pid:.1f} W, electrical {lo:.0f}-{hi:.0f} W, "
          f"{lo/PACK_WH:.2f}-{hi/PACK_WH:.2f} C, {lo/PACK_V:.1f}-{hi/PACK_V:.1f} A")
    approx(f"{name} P_ideal [W]", pid, want_id, rel=0.01)
    approx(f"{name} P_elec at FoM 0.75 [W]", lo, want_lo, rel=0.01)
    approx(f"{name} P_elec at FoM 0.65 [W]", hi, want_hi, rel=0.01)
    approx(f"{name} C-rate at FoM 0.65", hi / PACK_WH, want_chi, rel=0.03)
    approx(f"{name} C-rate at FoM 0.75", lo / PACK_WH, want_clo, rel=0.03)

print("2. full-throttle current at 14.8 V")
p_full_lo, p_full_hi = p_ideal(35.0) / 0.75, p_ideal(35.0) / 0.65
approx("current at FoM 0.75 [A]", p_full_lo / PACK_V, 53.0, rel=0.02)
approx("current at FoM 0.65 [A]", p_full_hi / PACK_V, 61.0, rel=0.02)
units("14.8 V * 1.8 A * 3600 s", "J")
print("   NOTE: C = P/(V*Ah) with V = 14.8 V gives 10.40 C (half) and 29.41 C (full) at FoM 0.75,")
print("   against the lens's 9.6 C and 27 C: its lower C-rate bounds are 8 per cent low, while")
print("   its hover 3.5 C and its upper bounds 12.0/34 C match 14.8 V exactly.")

print("3. lap energy: 75 m at 15 m/s")
t_lap = 75.0 / 15.0
for p in (p_ideal(17.5) / 0.75, p_ideal(17.5) / 0.65):
    e_wh = p * t_lap / 3600.0
    print(f"   at {p:.0f} W: {e_wh:.3f} Wh = {100*e_wh/PACK_WH:.2f} % of the pack")
e_mid = 295.0 * t_lap / 3600.0
approx("lap energy at ~295 W [Wh]", e_mid, 0.41, rel=0.02)
approx("lap energy as a fraction of the pack [%]", 100 * e_mid / PACK_WH, 1.5, rel=0.05)
inequality(f"{100*e_mid/PACK_WH!r}", "<", "5")        # energy is not the binding store
units("295 W * 5 s", "J")
quantity("295 W * 5 s", "0.4097 W*h", rel_tol=1e-3)

raise SystemExit(finish())
