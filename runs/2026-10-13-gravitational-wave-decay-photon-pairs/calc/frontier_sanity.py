# Frontier sanity check: reproduce B&O's own quoted scale for a GW150914-like merger
# from their eqs. (10)-(12) as printed in v2 (SI units). Inputs are B&O's own merger scalings:
# nu = 150 Hz (65 Msun/M), E_rel = 2 Msun c^2 (M/65 Msun), t_m = 5 ms (M/65 Msun), M = 65 Msun.
import math
G=6.67430e-11; c=2.99792458e8; hbar=1.054571817e-34; kB=1.380649e-23; eV=1.602176634e-19
Msun=1.98847e30; T0=2.7255
M=65*Msun; nu=150.0; Erel=2*Msun*c**2; tm=5e-3
w=2*math.pi*nu
rm=2*G*Erel/c**4        # eq.(12) definition r_m = 2 G E_rel / c^4
ell=c*tm                # wavefront width l = c*delta t
# eq.(12): W_gamma = 3/(50 pi) (r_m/l)^2 hbar omega^2   [W]  (the printed 'hbar omega 2' read as hbar*omega^2)
W=3/(50*math.pi)*(rm/ell)**2*hbar*w**2
photon_energy=hbar*w
L=W/photon_energy
f_cmb=1/math.expm1(hbar*w/(kB*T0))      # CMB occupation at omega_s
Lenh=L*(1+2*f_cmb)
print("r_m = %.4g m ; l = c*t_m = %.4g m ; r_m/l = %.4g"%(rm,ell,rm/ell))
print("hbar*omega = %.4g J = %.4g eV"%(photon_energy,photon_energy/eV))
print("W_gamma (eq.12, no CMB factor) = %.4g W"%W)
print("L_gamma = W/(hbar omega) = %.4g photons/s"%L)
print("f_gamma(omega_s) at T0=2.7255 K = %.4g ; (1+2f) = %.4g"%(f_cmb,1+2*f_cmb))
print("L_gamma with (1+2f) = %.4g photons/s   [B&O quote ~1e6 s^-1 at nominal merger frequency]"%Lenh)
# check eq.(11) vs eq.(12) consistency in natural-unit form: W = 6 G^2 Erel^2 w^2 sigma^2/(25 pi) with sigma = 1/tm
# SI: W = 6 G^2 hbar/(25 pi c^10) Erel^2 w^2 delta^2, delta = 1/tm
W11=6*G**2*hbar/(25*math.pi*c**10)*Erel**2*w**2*(1/tm)**2
print("W_gamma from eq.(11) SI form with delta_omega=1/t_m = %.4g W (compare eq.12 %.4g W)"%(W11,W))
N0=Erel/(hbar*w)
print("graviton number N0 = Erel/(hbar omega) = %.4g"%N0)
print("photon number emitted in t_m with no CMB factor ~ L*t_m = %.4g (B&O: N_gamma << N0 required)"%(L*tm))
print("source: B&O arXiv:2607.24930v2 eqs. (10)-(12), merger scalings p.3")
