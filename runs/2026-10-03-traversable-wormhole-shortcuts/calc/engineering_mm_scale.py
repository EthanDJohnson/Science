"""Scale of a Maldacena-Milekhin 'humanly traversable' wormhole mouth, SI units.
Input (from arXiv:2008.06618 eq. 3.26): throat/extremal radius r_e > 1.5e7 m.
Each mouth ~ extremal magnetically charged black hole: r_e = G M / c^2 (extremal RN, geometric radius, Gaussian-type charge, Q^2 = G M^2).
Outputs: mass per mouth, rest energy, magnetic charge in Dirac units, Hawking-free cold-environment note.
Assumption: extremal RN relation r_e = G M/c^2 (valid for the outside geometry; the paper says mouths have 'up to a small correction' the same mass and charge as extremal BHs).
"""
import math
G=6.67430e-11; c=2.99792458e8; Msun=1.98847e30; hbar=1.054571817e-34; e=1.602176634e-19
eps0=8.8541878128e-12; mu0=4e-7*math.pi
r_e=1.5e7
M=r_e*c**2/G
E=M*c**2
print("r_e = %.3e m (input, MM eq 3.26)"%r_e)
print("M per mouth = %.3e kg = %.3e Msun"%(M,M/Msun))
print("two mouths rest energy = %.3e J"%(2*E))
# magnetic charge: Gaussian Q^2 = G M^2  -> in SI-magnetic (Weber) g_SI: B=mu0 g/(4 pi r^2) ; extremal condition mu0 g^2/(4 pi) = G M^2 ... 
# energy of magnetic field outside: use mu0 g^2/(4 pi r_e) = M c^2 *(...) ; here: g = sqrt(4 pi G M^2/mu0)
g=math.sqrt(4*math.pi*G*M**2/mu0)  # A*m
gD=2*math.pi*hbar/(mu0*e)          # Dirac magnetic charge in A*m (g_D = h/(mu0 e))
print("magnetic charge g = %.3e A m ; Dirac charge g_D = %.3e A m ; g/g_D = %.3e"%(g,gD,g/gD))
# Horizon-surface field
B=mu0*g/(4*math.pi*r_e**2)
print("B at r_e = %.3e T (cf. LHC Pb-Pb peak ~1e16 T? no: this is much smaller)"%B)
# Hawking temperature of extremal BH = 0; CMB T=2.725 K ; note Schwarzschild-equivalent temperature of mass M
kB=1.380649e-23
TH=hbar*c**3/(8*math.pi*G*M*kB)
print("Schwarzschild-equivalent Hawking T for this mass = %.3e K (for scale only; extremal -> 0)"%TH)
print("CMB photon boost: M-M say gamma amplification applies; CMB T = 2.725 K must be reduced -> 'refrigerator'")
print("Light-crossing time of r_e: %.3f s"%(r_e/c))
