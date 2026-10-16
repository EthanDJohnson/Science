"""M-CONSTRAINTS-02: the unidirectional-thrust torque ceiling and the peak body rate
(lens findings F2 and F13, candidate CONSTRAINTS-C).

Claim as I state it (SI units):
  Four rotors, per-rotor thrust f_i in [0, f_max].  Collective T = sum f_i.  For a roll torque
  about x in the X configuration the effective lever is l_eff = l sin(b) with l = 0.14 m,
  b = 56 deg; two rotors on one side carry f_hi, two on the other f_lo, so
      T = 2 (f_lo + f_hi),  tau_x = 2 l_eff (f_hi - f_lo).
  Maximising tau_x at fixed T over 0 <= f_lo, f_hi <= f_max gives
      tau_max(T) = l_eff * min(T, 4 f_max - T),
  hence (i) at hover collective T = m g, tau_max = l_eff m g, independent of f_max (provided
  m g <= 2 f_max); (ii) the global maximum is l_eff * 2 f_max at T = 2 f_max, which implies a
  net vertical acceleration (2 f_max - m g)/m;  (iii) with f_i >= 0 the downward acceleration
  is capped at -g while upward it is (4 f_max - m g)/m.
  Numbers: Swift-like m = 0.870 kg, f_max = 8.75 N, Jx = 2.5e-3 kg m^2:
    l_eff = 0.1161 m, tau_max(mg) = 0.990 N m, alpha = 396 rad/s^2, global 2.03 N m /
    812 rad/s^2 at ~1 g climb, up/down asymmetry 30.4/9.81 = 3.10;
  0.52 kg platform, f_max = 15.75 N, Jx = 1.7e-3: 0.592 N m, 348 rad/s^2, asymmetry 11.35.
  F13: a rest-to-rest bang-bang slew through theta at constant alpha peaks at
  omega_peak = sqrt(theta alpha) = 32.4 rad/s = 1857 deg/s for theta = 152 deg.
Domain: f_max > 0, 0 <= T <= 4 f_max, m, g, Jx, l_eff > 0, 0 < b < 90 deg.
"""
import sys
import math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, inequality, limit, units, quantity, finish


def approx(label, got, want, rel=0.015):
    print(f"  {label}: got {got:.6g}, lens {want:.6g}")
    return inequality(f"Abs({got!r} - ({want!r}))", "<", f"{rel}*Abs({want!r})")


G = 9.81
L_ARM, B_DEG = 0.14, 56.0
l_eff = L_ARM * math.sin(math.radians(B_DEG))
print(f"l_eff = l sin(b) = {l_eff:.5f} m")
approx("l_eff [m]", l_eff, 0.1161, rel=0.01)

# --- 1. the constrained maximisation, solved by brute force on a fine grid (independent of
#        the closed form) and compared with l_eff * min(T, 4 f_max - T)
print("1. numerical maximisation of tau_x at fixed T against the closed form")
f_max = 8.75
worst = 0.0
for i in range(0, 201):
    T = 4.0 * f_max * i / 200.0
    best = 0.0
    for j in range(0, 2001):
        f_lo = min(f_max, T / 2.0) * j / 2000.0
        f_hi = T / 2.0 - f_lo
        if f_hi < -1e-12 or f_hi > f_max + 1e-12:
            continue
        best = max(best, 2.0 * l_eff * (f_hi - f_lo))
    closed = l_eff * min(T, 4.0 * f_max - T)
    worst = max(worst, abs(best - closed))
print(f"   max |grid optimum - l_eff min(T, 4 f_max - T)| over 201 collectives = {worst:.3e} N m")
inequality(f"{worst!r}", "<", "1e-9")
# symbolic: the two branches agree with the min() form
Tv, fm, le = sp.symbols("Tv fm le", positive=True)
identity(sp.Min(Tv, 4 * fm - Tv) * le, le * Tv, domain={"Tv": (0.1, 1.0), "fm": (1.0, 2.0), "le": (0.1, 0.3)})
identity(sp.Min(Tv, 4 * fm - Tv) * le, le * (4 * fm - Tv), domain={"Tv": (6.0, 7.9), "fm": (1.0, 2.0), "le": (0.1, 0.3)})
# the ceiling is a concave tent peaking at T = 2 f_max
inequality("le*Min(Tv, 4*fm - Tv)", "<=", "2*le*fm", domain={"Tv": (0.0, 8.0), "fm": (1.0, 2.0), "le": (0.1, 0.3)})

# --- 2. the three platforms
print("2. per-platform numbers")
plats = [("Swift-like", 0.870, 8.75, 2.5e-3, 0.990, 396.0, 3.10),
         ("Sun2022", 0.750, 8.50, 2.5e-3, None, None, None),
         ("0.52 kg T/W 12.35", 0.520, 15.75, 1.7e-3, 0.592, 348.0, 11.35)]
for name, m, fmx, Jx, want_tau, want_al, want_asym in plats:
    tau_h = l_eff * m * G
    al = tau_h / Jx
    a_up = (4 * fmx - m * G) / m
    asym = a_up / G
    print(f"   {name}: tau_max(mg) = {tau_h:.4f} N m, alpha = {al:.1f} rad/s^2, "
          f"a_up = {a_up:.2f} m/s^2, asymmetry = {asym:.2f}")
    if want_tau:
        approx(f"{name} tau_max(mg) [N m]", tau_h, want_tau, rel=0.01)
        approx(f"{name} alpha [rad/s^2]", al, want_al, rel=0.01)
        approx(f"{name} up/down asymmetry", asym, want_asym, rel=0.01)

# --- 3. the global maximum and its climb
print("3. global torque maximum (Swift-like)")
m, Jx = 0.870, 2.5e-3
tau_glob = l_eff * 2.0 * f_max
approx("global tau_max [N m]", tau_glob, 2.03, rel=0.01)
approx("global alpha [rad/s^2]", tau_glob / Jx, 812.0, rel=0.01)
approx("climb at T = 2 f_max [g]", (2.0 * f_max - m * G) / m / G, 1.0, rel=0.10)
approx("a_up Swift-like [m/s^2]", (4 * f_max - m * G) / m, 30.4, rel=0.01)
# independence of installed thrust: doubling f_max leaves tau_max(mg) unchanged
approx("tau_max(mg) with f_max doubled [N m]", l_eff * min(m * G, 4 * 2 * f_max - m * G), 0.990, rel=0.01)
units("0.1161 m * 0.870 kg * 9.81 m/s^2", "N*m")
units("0.990 N*m / (2.5e-3 kg*m^2)", "1/s^2")
quantity("0.1161 m * 0.870 kg * 9.81 m/s^2", "0.990 N*m", rel_tol=2e-3)

# --- 4. F13: peak rate of a rest-to-rest bang-bang slew
print("4. peak body rate of a bang-bang slew, theta = 152 deg, alpha = 396.2 rad/s^2")
th, al_s = sp.symbols("th al_s", positive=True)
t_half = sp.sqrt(th / al_s)                   # from th/2 = al_s t_half^2/2
identity(al_s * t_half, sp.sqrt(th * al_s))   # omega_peak = sqrt(theta alpha)
alpha = l_eff * m * G / Jx
w_pk = math.sqrt(math.radians(152.0) * alpha)
print(f"   omega_peak = {w_pk:.3f} rad/s = {math.degrees(w_pk):.1f} deg/s")
approx("omega_peak [deg/s]", math.degrees(w_pk), 1857.0, rel=0.01)
units("2.6529 rad * 396.2 rad/s^2", "1/s^2")
# limit: zero angle gives zero peak rate
limit(sp.sqrt(th * al_s), "th", 0, 0)

raise SystemExit(finish())
