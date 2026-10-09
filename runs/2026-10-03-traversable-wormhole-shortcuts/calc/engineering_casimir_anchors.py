"""Engineering anchors for the wormhole run (SI). Ideal parallel-plate Casimir pressure and energy density,
Morris-Thorne throat tension and effective mass scale, and the gaps between them.
Ideal perfect-conductor, zero-temperature, parallel plates: P = pi^2 hbar c / (240 d^4) (attractive),
energy density between plates u = -pi^2 hbar c / (720 d^4). Real metals reduce these by tens of percent at d ~ 0.5 um.
Morris-Thorne radial tension at the throat (Phi finite, b(r0)=r0): tau0 = c^4 / (8 pi G r0^2).
Effective gravitational mass of a throat of radius b0 (b(r) = b0 => mass function b/2): M_eff = b0 c^2 / (2 G).
"""
import math
G = 6.67430e-11; c = 2.99792458e8; hbar = 1.054571817e-34; MJ = 1.898e27; Msun = 1.98847e30
def casimir_P(d): return math.pi**2 * hbar * c / (240 * d**4)
def casimir_u(d): return -math.pi**2 * hbar * c / (720 * d**4)
for d in (10e-9, 100e-9, 500e-9, 1e-6, 3e-6):
    print("d = %.0e m : P = %.3e Pa ; u = %.3e J/m^3" % (d, casimir_P(d), casimir_u(d)))
c4G = c**4 / G
print("c^4/G = %.3e N" % c4G)
for b in (1.0, 10.0, 1e3, 3e3):
    tau = c4G / (8 * math.pi * b**2)
    print("MT throat b0=%.0e m : tau0 = %.3e Pa ; M_eff = b0 c^2/(2G) = %.3e kg = %.3f M_J ; M_eff c^2 = %.3e J"
          % (b, tau, b * c**2 / (2 * G), b * c**2 / (2 * G) / MJ, b * c**4 / (2 * G)))
# gap: smallest-d Casimir pressure vs MT tension for b0 = 1 m, 1 km
Pmax = casimir_P(10e-9)
for b in (1.0, 1e3):
    tau = c4G / (8 * math.pi * b**2)
    print("tau0(b0=%.0e m)/P_Casimir(10 nm) = %.3e (%.1f orders)" % (b, tau / Pmax, math.log10(tau / Pmax)))
# energy: Casimir energy density at 1 um vs MT effective energy for b0 = 1 m; volume needed
u1 = abs(casimir_u(1e-6)); E1 = 0.5 * 1.0 * c**4 / G  # b0 c^4/(2G) for b0 = 1 m
print("volume of 1-um-gap Casimir cavity holding |E| = %.3e J (b0=1 m): %.3e m^3 (cube side %.3e m; Earth volume 1.08e21 m^3)"
      % (E1, E1 / u1, (E1 / u1) ** (1 / 3)))
# Wilson 2011 DCE: ~0.05c is NOT quoted by the source ('few percent of c')
print("Parker Solar Probe 192.2 km/s = %.3e c" % (192.2e3 / c))
# LHC-scale comparison for MMP: 1/TeV length
print("hbar c / (1 TeV) = %.3e m" % (hbar * c / (1e12 * 1.602176634e-19)))
