#!/usr/bin/env python3
"""Idealizer lens, model M3: where does the conflict actually bite? Clock time in a superposed geometry.

All SI. Idealization: Newtonian potential, weak field, lowest order in 1/c^2; a two-level "clock" with
angular frequency omega (rad/s); no environment.

(a) Clock in a superposition of heights on a CLASSICAL background (Zych et al. 2011 idea):
    phase difference  dphi = omega * g * dh * t / c^2 ; visibility |cos(dphi/2)| -> first zero at t0 = pi c^2/(omega g dh)
(b) Clock at fixed position, SOURCE mass m in a superposition of two positions (geometry superposed):
    dphi = omega * dPhi * t / c^2 with dPhi = G m (1/d1 - 1/d2)
    mass needed for dphi = 1 rad in time t:  m* = c^2 / (omega * G * (1/d1 - 1/d2) * t)
(c) Rest-mass Compton clock: omega_C = m c^2/hbar. Then (b) becomes dphi = G m m' t (1/d1-1/d2)/hbar,
    which is exactly the QGEM gravitational phase (Bose et al.). Check against the dossier's Q-10 numbers.
(d) Smith-Ahmadi coupling lam = hbar G/(c^4 x) (s): fractional correction lam*omega_S
(e) Semiclassical WDW correction size: (E/m_P)^2 in Kiefer's convention m_P = sqrt(3 pi hbar c/(2G)) (dossier Q-17)
"""
import math

G = 6.67430e-11      # m^3 kg^-1 s^-2
c = 299792458.0      # m/s
hbar = 1.054571817e-34
g = 9.80665          # m/s^2
omega_sr = 2 * math.pi * 429.228e12   # Sr clock transition, rad/s

print("(a) clock (Sr, omega = 2pi*429.2 THz) in superposition of heights, classical Earth background")
for dh in (1e-3, 1e-2, 1.0, 10.0):
    rate = omega_sr * g * dh / c ** 2   # rad/s
    t0 = math.pi / rate
    print(f"  dh = {dh:g} m: dphi/dt = {rate:.3e} rad/s ; visibility first zero at t = {t0:.3e} s")

print("\n(b) superposed SOURCE mass, fixed clock (optical, omega = 2pi*429 THz), t = 1 s")
t = 1.0
for (d1, d2) in ((200e-6, 450e-6), (1e-3, 2e-3), (1e-2, 2e-2)):
    geo = 1 / d1 - 1 / d2
    mstar = c ** 2 / (omega_sr * G * geo * t)
    print(f"  d1={d1:g} m, d2={d2:g} m: mass for 1 rad in 1 s = {mstar:.3e} kg")

print("\n(c) same with the rest-mass (Compton) clock of a second mass m' = m = 1e-14 kg (QGEM scale)")
m = 1e-14
omega_C = m * c ** 2 / hbar
for (d1, d2, tt) in ((200e-6, 450e-6, 1.0), (200e-6, 450e-6, 2.5)):
    dphi = omega_C * G * m * (1 / d1 - 1 / d2) * tt / c ** 2
    dphi2 = G * m * m * (1 / d1 - 1 / d2) * tt / hbar
    print(f"  omega_C = {omega_C:.3e} rad/s; d1={d1*1e6:.0f} um, d2={d2*1e6:.0f} um, t={tt} s: dphi = {dphi:.3f} rad (=G m^2 t (1/d1-1/d2)/hbar = {dphi2:.3f})")
print("  ratio of 'clock frequencies' Compton/optical = %.2e" % (omega_C / omega_sr))

print("\n(d) Smith-Ahmadi relational-clock gravitational coupling lam = hbar G /(c^4 x)")
for x in (1e-3, 1.0, 6.371e6):
    lam = hbar * G / (c ** 4 * x)
    print(f"  x = {x:g} m: lam = {lam:.3e} s; lam*omega_Sr = {lam*omega_sr:.3e} (fractional shift, dimensionless)")

print("\n(e) semiclassical-time correction (E/m_P)^2, m_P = sqrt(3 pi hbar c/(2G))")
mP_kg = math.sqrt(3 * math.pi * hbar * c / (2 * G))
mP_GeV = mP_kg * c ** 2 / 1.602176634e-10
for label, E_GeV in (("optical photon 1.77 eV", 1.77e-9), ("LHC 14 TeV", 1.4e4), ("GUT 1e16 GeV", 1e16)):
    print(f"  {label}: (E/m_P)^2 = {(E_GeV/mP_GeV)**2:.3e}  (m_P = {mP_GeV:.3e} GeV)")
