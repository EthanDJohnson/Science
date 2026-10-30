"""Quantitative-facet input numbers for the Blas & Oller (arXiv:2607.24930) check.
Uses B&O's formulas as printed (eq. 8, 10, S7, 14) ONLY to size inputs; correctness of the formulas is NOT tested here.
Natural units internally (hbar=c=1, energies in J, G_nat = G/(hbar c^5) [J^-2]); outputs in SI.
Verification: (a) dimensional round trip via two routes for eq.14; (b) G_nat vs 1/M_Planck^2; (c) known numbers (rho_crit, plasma freq. of ionosphere-like n_e).
"""
import math
hbar=1.054571817e-34; c=2.99792458e8; G=6.6743e-11; Msun=1.98847e30
eV=1.602176634e-19; kB=1.380649e-23; Mpc=3.0856775814913673e22; yr=3.15576e7
e=1.602176634e-19; eps0=8.8541878128e-12; me=9.1093837015e-31; mp=1.67262192369e-27
Gn=G/(hbar*c**5)              # J^-2
print("G_nat [J^-2] =",Gn)
# check vs Planck mass: M_P = sqrt(hbar c/G) in kg -> energy M_P c^2 ; G_nat = 1/(M_P c^2)^2
MP=math.sqrt(hbar*c/G); print("M_P c^2 [GeV] =",MP*c**2/eV/1e9, " 1/(MPc^2)^2 =",1/(MP*c**2)**2, "(should equal G_nat)")

H0=67.4e3/Mpc   # s^-1  (Planck 2018 h=0.674)
h=0.674
rho_c=3*H0**2/(8*math.pi*G)  # kg/m3 mass density
rho_c_E=rho_c*c**2
print("H0 [s^-1] =",H0," rho_crit energy density [J/m^3] =",rho_c_E," (check: 1.8788e-26 h^2 kg/m^3 * c^2 =",1.8788e-26*h**2*c**2,")")

# --- GW150914 ---
Lpk=3.6e56*1e-7   # W
Erad=3.0*Msun*c**2
dL=410*Mpc
flux=Lpk/(4*math.pi*dL**2)
print("\nGW150914: L_peak [W] =",Lpk," E_rad [J] =",Erad," d_L [m] =",dL)
print("  peak flux at Earth [W/m^2] =",flux," peak GW energy density at Earth [J/m^3] =",flux/c)

# --- B&O merger-phase inputs, eq. 8/10 as printed ---
def bo(Erel_J, nu_Hz, eps, label):
    w=2*math.pi*nu_Hz*hbar            # J
    N0=Erel_J/w
    sig=eps*w
    rate_pairs=3*Gn**2*N0**2*w**3*sig**2/(25*math.pi)/hbar   # s^-1  (eq. 8)
    rate_phot=2*rate_pairs
    tau=25*math.pi/(6*Gn**2*Erel_J**2*w*sig**2)*hbar             # s   (eq. 10)  tau=25pi/(6 G^2 E^2 w sig^2)
    print(f"\n[{label}] E_rel={Erel_J:.3e} J, nu={nu_Hz} Hz, hbar*omega_s={w/eV:.3e} eV, N0={N0:.3e}, eps={eps}")
    print(f"  eq.8 pair rate = {rate_pairs:.3e} /s ; photon rate = {rate_phot:.3e} /s ; tau(eq.10) = {tau:.3e} s ({tau/yr:.3e} yr)")
    print(f"  coherence time 1/(eps*omega) = {1/(eps*2*math.pi*nu_Hz):.3e} s")
    return w,N0,tau
w,N0,tau=bo(2*Msun*c**2,150,0.15,"B&O merger anchor eps=0.15")
bo(2*Msun*c**2,150,0.10,"B&O merger anchor eps=0.10")
bo(3.0*Msun*c**2,150,0.15,"GW150914 full E_rad=3.0 Msun c^2")
T0=2.7255
f_cmb=1/math.expm1(w/(kB*T0))
print(f"  CMB occupation f_gamma at omega_s=2pi*150Hz*hbar: kT0/hbar w = {kB*T0/w:.3e}; f = {f_cmb:.3e}; 1+2f = {1+2*f_cmb:.3e}")
tm=5e-3
print(f"  merger-phase duration t_m = {tm} s; number of photons in t_m w/o stimulation: {2*3*Gn**2*N0**2*w**3*(0.15*w)**2/(25*math.pi)/hbar*tm:.3e}")

# --- eq. 14 stochastic background ---
def eq14(rho_J_m3,label):
    rho_nat=rho_J_m3*(hbar*c)**3          # J^4
    r=8*math.pi/15*Gn**2*rho_nat**2        # J^4 (rate/volume in nat units)
    SI=r/((hbar*c)**3*hbar)                # m^-3 s^-1
    print(f"  {label}: rho_GW={rho_J_m3:.3e} J/m^3 -> dP/dtdV={SI:.3e} pairs m^-3 s^-1; photons 2x = {2*SI:.3e}")
print("\neq.14 sizes (B&O formula as printed):")
for dNeff in (0.1,0.17,0.3):
    Oh2=5.6e-6*dNeff      # Maggiore 2000 eq.118 integrated  h^2 Omega_gw <= 5.6e-6 (Nnu-3)
    rho=Oh2/h**2*rho_c_E
    eq14(rho,f"BBN-type bound dNeff={dNeff} (h^2Omega=5.6e-6*dNeff={Oh2:.2e}, Omega={Oh2/h**2:.2e})")
eq14(5.8e-9*rho_c_E,"LVK O3 flat Omega_GW<=5.8e-9 (per log f; 95% CL)")
fyr=1/yr; A=2.4e-15
Om_pta=2*math.pi**2/3*fyr**2*A**2/H0**2
print(f"  NANOGrav 15yr A=2.4e-15 @1/yr: Omega_GW(f=1/yr)=2pi^2 f^2 A^2/(3H0^2) = {Om_pta:.3e}")
eq14(Om_pta*rho_c_E,"PTA Omega ~ 1 log-band at 1/yr")
eq14(flux/c,"GW150914 peak energy density at Earth (not a stochastic bkg; scale check only)")

# --- plasma frequencies ---
def wp_eV(ne_m3): return hbar*math.sqrt(e**2*ne_m3/(eps0*me))/eV
Ob_h2=0.0224; Y=0.245
rho_crit_mass=3*H0**2/(8*math.pi*G)
nb0=0.0224/h**2*rho_crit_mass/mp
ne0=nb0*(1-Y/2)  # fully ionised H+He, free electrons per baryon
print(f"\nPlasma: n_b0={nb0:.3f} m^-3 ; n_e0={ne0:.3f} m^-3 = {ne0*1e-6:.3e} cm^-3 ; omega_p0 = {wp_eV(ne0):.3e} eV (f_p = {wp_eV(ne0)*eV/hbar/2/math.pi:.3e} Hz)")
for z in (1,10,1100,1e3,1e5,3e6):
    print(f"  z={z:g}: omega_p = {wp_eV(ne0*(1+z)**3):.3e} eV  (fully ionised assumption; z>~1100 correct, z<~1100 only if reionised, mean IGM)")
print(f"  Galactic ISM n_e=0.03 cm^-3: f_p = {wp_eV(0.03e6)*eV/hbar/2/math.pi:.3e} Hz ; omega_p = {wp_eV(0.03e6):.3e} eV")
print(f"  Ionosphere F-layer peak n_e~1e12 m^-3: f_p = {wp_eV(1e12)*eV/hbar/2/math.pi:.3e} Hz (check: 8.98 MHz*sqrt(1e6 cm^-3)/1e3... expect ~9 MHz)")
print(f"  photon energy at 150 Hz: {2*math.pi*150*hbar/eV:.3e} eV ; at 1 kHz: {2*math.pi*1e3*hbar/eV:.3e} eV")
print(f"  CMB peak ~ 2.82 kT0 = {2.82*kB*T0/eV:.3e} eV ; kT0 = {kB*T0/eV:.3e} eV")
# --- ULDM eq. 16 as printed ---
for v in (1e-3,4e-3):
    for m in (1e-22,):
        print(f"\nULDM: N_phi eq16 at m={m} eV v={v}: {6e87*(1e-22/m)*(4e-3/v)**3*(0.26/0.26):.3e} (x_MW=1)  with x_MW=1e5: {6e87*(1e-22/m)*(4e-3/v)**3*1e5:.3e}")
# de Broglie / DM number density check
rho_dm=0.4e9*eV*1e6   # 0.4 GeV/cm^3 -> J/m^3
m=1e-22*eV
n_dm=rho_dm/m
lam=2*math.pi*hbar*c/(m*(1e-3)) /c  # de Broglie length = 2 pi hbar/(m v) ; here m in J -> m_kg=m/c^2
lam_dB=2*math.pi*hbar/((m/c**2)*1e-3*c)
print(f"\nULDM m=1e-22 eV, rho=0.4 GeV/cm^3: n={n_dm:.3e} m^-3 ; de Broglie lambda (v=1e-3 c) = {lam_dB:.3e} m = {lam_dB/3.0857e19:.3e} kpc ; occupation per mode ~ n*lam^3 = {n_dm*lam_dB**3:.3e}")
print(f"  cosmological mean DM density 0.26*rho_c = {0.26*rho_c_E/eV/1e9/1e6:.3e} GeV/cm^3 (expect ~1.3e-6)")
