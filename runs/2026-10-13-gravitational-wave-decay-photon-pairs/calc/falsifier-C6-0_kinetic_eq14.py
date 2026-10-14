"""Falsifier C6-0 (physics angle): independent checks of eq. 14 as an incoherent kinetic rate,
its dependence on chirality and spectrum, its size across frequency and epoch, and the
dilution of a single source's local yield.

Units: natural (hbar = c = 1, G explicit) for parts A and D; SI for parts B and C.
Inputs taken as physics premises (not re-derived here): tree amplitudes for g g -> gamma gamma,
|M| = 8 pi G t^2/s and 8 pi G u^2/s for the two photon-helicity configurations of an
opposite-helicity graviton pair, zero for same helicity [D-01; M-MECHANIST-01].
"""
import numpy as np

rng = np.random.default_rng(12345)
G = 1.0

# ---------------- Part A: own cross section and own Monte Carlo kinetic rate -------------
# dsigma/dOmega (opposite-helicity pair, summed over photon helicities, 1/2 identical photons)
#   = (1/2) * (8 pi G)^2 (t^4 + u^4)/s^2 / (64 pi^2 s)
def sigma_RL(s, nquad=4000):
    c, wq = np.polynomial.legendre.leggauss(nquad)
    t = -s * (1 - c) / 2
    u = -s * (1 + c) / 2
    dsig = 0.5 * (8 * np.pi * G) ** 2 * (t ** 4 + u ** 4) / s ** 2 / (64 * np.pi ** 2 * s)
    return 2 * np.pi * np.sum(wq * dsig)

for s in [1.0, 3.7]:
    print(f"A1 sigma_RL(s={s})/(G^2 s) = {sigma_RL(s)/(G**2*s):.10f}  vs 4pi/5 = {4*np.pi/5:.10f}")

def mc_rate(nsamp, spectrum, chi):
    """Gamma/V / (G^2 rho^2) for an isotropic bath; chi = net circular polarisation
    (fraction R = (1+chi)/2). Only opposite-helicity pairs fuse."""
    # sample two graviton energies from the number spectrum, directions isotropic
    w1 = spectrum(nsamp); w2 = spectrum(nsamp)
    c1 = rng.uniform(-1, 1, nsamp); c2 = rng.uniform(-1, 1, nsamp)
    p1 = rng.uniform(0, 2*np.pi, nsamp); p2 = rng.uniform(0, 2*np.pi, nsamp)
    s1 = np.sqrt(1-c1**2); s2 = np.sqrt(1-c2**2)
    cos12 = c1*c2 + s1*s2*np.cos(p1-p2)
    s = 2*w1*w2*(1-cos12)
    sig = (4*np.pi/5)*G**2*s          # sigma_RL, checked numerically in A1
    pR = (1+chi)/2; pL = 1-pR
    p_opp = 2*pR*pL                   # probability the pair has opposite helicities
    integrand = 0.5 * p_opp * sig * (1-cos12)   # (1/2) n^2 <sigma v_rel>, n = 1
    # rho = n <w> with n = 1
    rho = 0.5*(np.mean(w1)+np.mean(w2))
    est = np.mean(integrand)/rho**2
    err = np.std(integrand)/np.sqrt(nsamp)/rho**2
    return est, err

mono = lambda n: np.ones(n)
loguni = lambda n: np.exp(rng.uniform(np.log(1e-3), np.log(1e3), n))
twoline = lambda n: np.where(rng.uniform(size=n) < 0.3, 1.0, 50.0)
target = 8*np.pi/15
print(f"A2 target 8pi/15 = {target:.6f}")
for name, spec in [("monochromatic", mono), ("two-line (1, 50)", twoline), ("log-uniform 1e-3..1e3", loguni)]:
    est, err = mc_rate(2_000_000, spec, 0.0)
    print(f"A2 unpolarised, {name:24s}: Gamma/(V G^2 rho^2) = {est:.5f} +- {err:.5f}  ratio {est/target:.4f}")
for chi in [0.0, 0.5, 0.9, 1.0]:
    est, err = mc_rate(2_000_000, mono, chi)
    print(f"A3 chirality chi={chi:.1f}: ratio to eq.14 = {est/target:.4f} +- {err/target:.4f}  (1-chi^2 = {1-chi**2:.4f})")

# collimated (anisotropic) bath: directions within a cone of half-angle a about z
for a in [np.pi, 0.5, 0.1, 0.01]:
    n = 2_000_000
    cmin = np.cos(a)
    c1 = rng.uniform(cmin, 1, n); c2 = rng.uniform(cmin, 1, n)
    p1 = rng.uniform(0, 2*np.pi, n); p2 = rng.uniform(0, 2*np.pi, n)
    cos12 = c1*c2 + np.sqrt(1-c1**2)*np.sqrt(1-c2**2)*np.cos(p1-p2)
    val = np.mean(0.5*0.5*(4*np.pi/5)*2*(1-cos12)**2)
    print(f"A4 cone half-angle {a:.3f} rad: ratio to isotropic = {val/target:.3e}")

# ---------------- Part B: SI sizes today ----------------------------------------------
Gs = 6.67430e-11; c = 2.99792458e8; hbar = 1.054571817e-34; kB = 1.380649e-23
T0 = 2.7255
a_rad = 7.565723e-16
rho_gam = a_rad*T0**4
H0 = 67.4e3/3.0857e22
for dN in [0.3, 0.1]:
    rho = (7/8)*(4/11)**(4/3)*dN*rho_gam
    Gam = (8*np.pi/15)*Gs**2*rho**2/c**7
    print(f"B1 DeltaN_eff={dN}: rho_GW = {rho:.3e} J/m^3, pair rate = {Gam:.3e} m^-3 s^-1")
rho = (7/8)*(4/11)**(4/3)*0.3*rho_gam
Gam = (8*np.pi/15)*Gs**2*rho**2/c**7
for f in [1e-8, 25.0, 1e3, 1e9, 1e14, 1.855e43]:
    w = 2*np.pi*f
    frac = Gam*2*hbar*w/(H0*rho)
    with np.errstate(over="ignore"): occ = 1/np.expm1(hbar*w/(kB*T0))
    frac_stim = frac*(1+2*occ)
    print(f"B2 f = {f:.3e} Hz: energy fraction converted per Hubble time = {frac:.3e} (vacuum), {frac_stim:.3e} (CMB-stimulated)")

# ---------------- Part C: early universe, stimulated route (M-CONSTRAINTS-03 scaling) ----
# d(Drho/rho)/dln a = 1.444 r^2 (T/M_Pl)^3, r = rho_GW/rho_gamma = 0.0681 (DeltaN_eff = 0.3)
r = 0.0681
for T_GeV in [1e3, 1e9, 1e16, 1.22e18]:
    x = T_GeV/1.221e19
    print(f"C1 T = {T_GeV:.2e} GeV: conversion per e-fold = {1.444*r**2*x**3:.3e}")
xstar = (1e-5/(1.444*r**2))**(1/3)
print(f"C2 conversion per e-fold reaches 1e-5 only at T = {xstar:.3f} M_Pl = {xstar*1.221e19:.2e} GeV")

# ---------------- Part D: single source, local kinetic yield beyond R ---------------------
# Shell of energy E, thickness L at radius r: rho = E/(4 pi r^2 L). Local rate density
# K rho^2 g(theta(r)), shell volume 4 pi r^2 L, dt = dr/c.  Yield beyond R:
#   Y(R) = (K E^2/(4 pi L c)) Int_R^inf g(theta(r)) r^-2 dr
from math import inf
def Y(R, p):   # g = theta^4 with theta = (k r)^-p  (k = 1); p = 0 means fixed angle 1
    rr = np.logspace(np.log10(R), np.log10(R)+12, 200001)
    gg = rr**(-4*p)
    return np.trapezoid(gg*rr**-2, rr)
for p in [0.0, 0.5, 1.0]:
    y1, y2 = Y(1e2, p), Y(1e4, p)
    print(f"D1 theta ~ r^-{p}: Y(1e4)/Y(1e2) = {y2/y1:.3e}  -> slope {np.log10(y2/y1)/2:.3f} (yield beyond R converges)")
