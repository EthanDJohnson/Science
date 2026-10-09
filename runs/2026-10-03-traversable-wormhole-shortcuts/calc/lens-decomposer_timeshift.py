"""Decomposer lens: shortcut and CTC thresholds for a one-sided wormhole as a function
of the time shift between mouth clocks, and what it costs to reach them for the
Maldacena-Milekhin (MM) wormhole. Also the short-throat (Ellis) shortcut ratio and
payload/binding-energy ratios.

Model (exterior frame, c = 1 when stated; SI otherwise):
  mouths A, B at rest, exterior light-travel time between the static observers T_ext = d/c.
  throat transit (exterior coordinate time, incl. redshift delays) = L/c.
  s = identification shift: an object entering A at exterior time t leaves B at t + L/c + s
      (s < 0 means B's clock has been made to lag, e.g. by moving mouth B, MTY 1988).
  Shortcut:  T_thru = L/c + s < d/c        <=>  -s > (L - d)/c
  CTC (A->B through throat, B->A outside):  L/c + s + d/c <= 0  <=>  -s >= (L + d)/c
Since -s changes continuously with mouth motion, -s crosses (L-d)/c before (L+d)/c:
every route to a CTC passes through a shortcut stage first (for L > d too).
"""
import math

c = 2.99792458e8          # m/s
yr = 3.15576e7            # s (Julian)
ly = c * yr               # m
G = 6.67430e-11           # SI
Msun = 1.98892e30         # kg

print("=== 1. Generic thresholds (units of d/c) ===")
for L_over_d in [0.001, 0.5, 1.0, math.pi, 10.0]:
    sc = L_over_d - 1.0
    ctc = L_over_d + 1.0
    print(f"L/d = {L_over_d:8.3f}: shift for shortcut -s > {sc:+8.3f} d/c ; for CTC -s >= {ctc:8.3f} d/c ; "
          f"ratio CTC/shortcut = {('inf (already shortcut)' if sc <= 0 else f'{ctc/sc:.3f}')}")

print()
print("=== 2. MM numbers (Q-02, Q-04, Q-06): ell ~ 3e3 ly, L = pi*ell, M_e ~ 2.0e34 kg per mouth ===")
ell = 3.0e3 * ly
L = math.pi * ell
Me = 2.0e34
print(f"L = pi*ell = {L/ly:.4g} ly ; L/c = {L/c/yr:.4g} yr")
for d_ly in [1.0, 100.0, 1000.0, 3000.0]:
    d = d_ly * ly
    s_sc = (L - d) / c
    s_ctc = (L + d) / c
    print(f"d = {d_ly:7.0f} ly: T_thru/T_ext (no shift) = {L/d:9.4g}; shift for shortcut = {s_sc/yr:9.4g} yr;"
          f" for CTC = {s_ctc/yr:9.4g} yr")

print()
print("=== 3. Producing the shift by MTY-style mouth motion (out-and-back at speed v, exterior duration T) ===")
print("shift = T (1 - 1/gamma). Kinetic energy of one mouth at speed v: (gamma-1) M_e c^2.")
s_need = (L - 1000.0 * ly) / c   # shortcut threshold at d = 1000 ly
for beta in [0.01, 0.1, 0.5, 0.9]:
    g = 1.0 / math.sqrt(1 - beta**2)
    T = s_need / (1 - 1 / g)
    KE = (g - 1) * Me * c**2
    print(f"v = {beta:4.2f} c: gamma = {g:.5f}; exterior trip duration for shortcut shift (d=1000 ly) = {T/yr:.4g} yr;"
          f" one-way excursion ~ {beta*T/2/yr:.4g} ly; KE = {KE:.3g} J = {KE/(Msun*c**2):.3g} Msun c^2")

print()
print("=== 4. Producing the shift by gravitational time dilation (mouth B parked at lapse alpha) ===")
for alpha in [0.9, 0.5, 0.1]:
    T = s_need / (1 - alpha)
    print(f"alpha = {alpha}: parking time for shortcut shift (d = 1000 ly) = {T/yr:.4g} yr (exterior)")

print()
print("=== 5. Short throat for contrast: Ellis b0 = 1 m, observers at R = 10 m from each mouth, Phi = 0 ===")
b0, R = 1.0, 10.0
T_thru = 2 * math.sqrt(R**2 - b0**2) / c
for d_m in [1.0e3, 1.496e11, ly]:
    T_ext = (d_m - 2 * R) / c
    print(f"d = {d_m:.4g} m: T_thru = {T_thru:.4g} s, T_ext = {T_ext:.4g} s, ratio = {T_thru/T_ext:.3g};"
          f" CTC shift needed = (L+d)/c = {(2*math.sqrt(R**2-b0**2)+d_m)/c:.4g} s")

print()
print("=== 6. Payload vs binding energy, MM (Q-02: |E_bin| ~ 5e9 kg) ===")
Ebin = 5.0e9
for m in [1.0, 70.0, 1.0e3]:
    print(f"payload {m:7.1f} kg: m/|E_bin| = {m/Ebin:.3g}")
