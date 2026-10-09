"""Idealizer: (a) relax 'classical exotic matter' to 'free quantum field obeying the flat-space quantum
inequality' for a uniform-throat and a thin-band throat (Ford-Roman scaling reproduced from the simplest
model); (b) two-sided wormhole as a teleportation channel: arrival time and payload quanta.

Units: SI; l_P = sqrt(hbar G / c^3). Geometric relations converted with c^4/G (energy density).
"""
import math

G = 6.67430e-11; c = 2.99792458e8; hbar = 1.054571817e-34
lP = math.sqrt(hbar * G / c**3)

print("=== (a) Quantum-inequality idealization ===")
print(" Required throat energy density |rho| ~ c^4/(8 pi G r0^2) (Ellis/MT order of magnitude, [Q-24])")
print(" Ford-Roman flat-space QI: |rho| <= 3 hbar c/(32 pi^2 (c tau)^4), sampling length c tau = f * (smallest length)")
for f in [1.0, 0.1, 0.01]:
    r0max = math.sqrt(3 / (4 * math.pi)) * lP / f**2
    print(f"  uniform throat, f = {f}: r0 <= sqrt(3/(4 pi)) l_P/f^2 = {r0max / lP:.3g} l_P = {r0max:.3e} m"
          f"   (dossier Q-20: l_P/f^2 or l_P/(2 f^2))")
print(" Thin band of width w carrying the flare-out: |rho| ~ c^4/(8 pi G r0 w); sampling length f w:")
print("  => w <= (3 r0 /(4 pi f^4 l_P))^(1/3) l_P   (Q-21 quotes (r0/(8 f^4 l_P))^(1/3) l_P)")
for r0 in [1.0, 9.4607e15, 1.5e7]:
    f = 0.01
    w = (3 * r0 / (4 * math.pi * f**4 * lP))**(1 / 3) * lP
    wq = (r0 / (8 * f**4 * lP))**(1 / 3) * lP
    rho_band = c**4 / (8 * math.pi * G * r0 * w)
    print(f"  r0 = {r0:.3g} m, f = 0.01: w <= {w:.2e} m (Q-21 form: {wq:.2e} m); band density ~ {rho_band:.2e} J/m^3"
          f" vs ideal Casimir at 10 nm 4.3e4 J/m^3 [Q-31]: ratio {rho_band / 4.3e4:.1e}")

print("\n=== (b) Two-sided wormhole as a channel (GJW/MQ idealization) ===")
print(" Model: message enters left at t_L = -t_s; the double-trace coupling acts at boundary time t0 and is itself")
print(" a non-gravitational L->R operation (in a lab: classical communication of the measured L outcomes).")
print(" The message cannot exit right before the right-side operation at t0 that it needs; so")
print(" t_arrival >= t0 + (time for the coupling's information to reach R).  Wormhole lead over channel: <= 0.")
print(" Teleportation bookkeeping: 1 qubit needs 1 ebit + 2 classical bits; MSY: quanta through <~ const x bits exchanged [Q-17].")
# payload quanta needed: energy E at wavelength ~ throat size R (must fit): N ~ E R/(hbar c)
for R in [1e-15, 1e-6, 1.0]:
    for m in [1.0, 70.0]:
        N = m * c**2 * R / (hbar * c)
        print(f"  throat/AdS scale R = {R:g} m, payload {m:g} kg: quanta of wavelength ~R needed N ~ m c R/hbar = {N:.1e}"
              f" -> coupling must carry >~ {N:.1e} bits through the classical channel anyway")
print(" FGM 2018 transit, BTZ: t* = -(l^2/r+) ln(|dV|/(2 l)) [Q-14]: logarithmic in the (small) negative shift |dV|.")
for dv in [1e-2, 1e-10, 1e-30]:
    print(f"  |dV|/(2l) = {dv:g}: t* r+/l^2 = {-math.log(dv):.1f}")
