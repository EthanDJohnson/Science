"""Scale estimates for the problem-of-time quantitative facet. SI units throughout.
Prints: Planck time, redshift per mm, Gambini-Porto-Pullin clock accuracy and decoherence
exponent for an optical clock transition, Pikovski time-dilation decoherence time,
Salecker-Wigner minimal clock mass."""
import math
import numpy as np

hbar = 1.054571817e-34; c = 299792458.0; G = 6.67430e-11; kB = 1.380649e-23
tP = math.sqrt(hbar*G/c**5)
lP = math.sqrt(hbar*G/c**3)
mP = math.sqrt(hbar*c/G)
print("Planck time tP = %.4e s ; Planck length = %.4e m ; Planck mass = %.4e kg" % (tP, lP, mP))

g = 9.80665
print("g*dh/c^2 for dh = 1 mm: %.4e (dimensionless)" % (g*1e-3/c**2))
print("g*dh/c^2 for dh = 1 m : %.4e" % (g*1.0/c**2))
print("Bothwell 7.6e-21 corresponds to height resolution dh = %.3e m" % (7.6e-21*c**2/g))

# Gambini-Porto-Pullin: dT ~ tP (T/tP)^(1/3), two-level decoherence exponent 3/2 tP^(4/3) T^(2/3) w^2
for T, label in [(1.0, "1 s"), (3.156e7, "1 yr"), (4.35e17, "age of universe 13.8 Gyr")]:
    dT = tP*(T/tP)**(1/3)
    w = 2*math.pi*4.29e14   # Sr clock transition ~ 429 THz
    expo = 1.5*tP**(4/3)*T**(2/3)*w**2
    print("T = %s: clock accuracy dT = %.3e s ; exponent for w=2pi*429 THz: %.3e" % (label, dT, expo))

# Pikovski: tau_dec = sqrt(2) hbar c^2 /(sqrt(N) kB T g dx)
def tau_dec(N, T, dx):
    return math.sqrt(2)*hbar*c**2/(math.sqrt(N)*kB*T*g*dx)
print("Pikovski tau_dec N=1e23, T=300 K, dx=1e-6 m : %.3e s" % tau_dec(1e23, 300, 1e-6))
print("Pikovski tau_dec N=1e10, T=300 K, dx=1e-6 m : %.3e s" % tau_dec(1e10, 300, 1e-6))
print("Pikovski tau_dec N=1e10, T=1 K, dx=1e-4 m  : %.3e s (nanoparticle, cryogenic)" % tau_dec(1e10, 1.0, 1e-4))
# QGEM-like microdiamond: m=1e-14 kg, rho=3500 -> N atoms of C
m = 1e-14; N = m/(12*1.6605e-27)
print("microdiamond m=1e-14 kg -> N = %.3e atoms ; tau_dec (T=0.15 K, dx=250 um) = %.3e s" % (N, tau_dec(N, 0.15, 250e-6)))

# Salecker-Wigner: clock running for time T with resolution dt needs M >= hbar T/(c^2 dt^2)
def SW_mass(T, dt): return hbar*T/(c**2*dt**2)
print("SW min clock mass, T=1 s, dt=1e-18 s: %.3e kg" % SW_mass(1.0, 1e-18))
print("SW min clock mass, T=1 s, dt=tP: %.3e kg" % SW_mass(1.0, tP))
print("SW min clock mass, T=4.35e17 s, dt=1 s: %.3e kg" % SW_mass(4.35e17, 1.0))


# QGEM-like gravitational phase: m = 1e-14 kg, centres separated by d = 450 um (closest approach d - dx = 200 um, dx = 250 um)
m = 1e-14; d = 450e-6; dx = 250e-6
E_far = G*m*m/(d + dx)      # LR? separation when the two masses are displaced apart
E_near = G*m*m/(d - dx)
E_mid = G*m*m/d
for tau in (1.0, 2.5):
    dphi = (E_near - E_far)*tau/hbar   # phase difference between closest and farthest branches (spread of the four-branch phases)
    print("QGEM-like: G m^2/d = %.3e J ; branch phase spread (E_near-E_far)*tau/hbar over tau=%.1f s = %.3f rad" % (E_mid, tau, dphi))
# mass gap: largest mass in a mechanical cat (Bild 2023, 16.2 ug effective mass) vs 1e-14 kg
print("Bild 2023 effective mass 16.2 ug = %.3e kg ; ratio to 1e-14 kg = %.3e" % (16.2e-9, 16.2e-9/1e-14))
