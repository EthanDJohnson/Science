"""Engineering facet: can any instrument see photons at the GW frequency?  (SI units throughout.)

Inputs taken from sources (not computed):
  - B&O (arXiv:2607.24930, p.4): for a merger at the nominal frequency "L_gamma ... ~1e6 s^-1" (photon NUMBER luminosity).
  - GW150914-like: nu = 150 Hz (B&O Fig. 2 anchor), d_L = 410 Mpc (LVK), t_m = 5 ms (B&O scaling, one period).
  - Gurnett et al. 2013 (Science 341, 1489): n_e ~ 0.002 cm^-3 outer heliosphere, ~0.08 cm^-3 local ISM.
  - Kogut et al. 2011 (PIXIE): mu = 1.4 dE/E ; PIXIE 5-sigma mu < 1e-8.  FIRAS: |mu|<9e-5, |y|<1.5e-5 (Fixsen 1996).
Everything else is arithmetic.  Verification: plasma frequency checked against the textbook 8.98 kHz sqrt(n/cm^-3);
Planck-law RJ limit checked against kT/(h nu).
"""
import math

h = 6.62607015e-34; hbar = h / (2 * math.pi); c = 2.99792458e8
kB = 1.380649e-23; e = 1.602176634e-19; me = 9.1093837015e-31
eps0 = 8.8541878128e-12; G = 6.67430e-11; Mpc = 3.0856775814913673e22
yr = 3.15576e7; T0 = 2.7255

def fp(n_m3):  # plasma frequency in Hz
    return math.sqrt(n_m3 * e**2 / (eps0 * me)) / (2 * math.pi)

print("== verification of f_p against 8.98 kHz*sqrt(n/cm^-3) ==")
n_test = 1.0e6  # 1 cm^-3
print(f"f_p(1 cm^-3) = {fp(n_test):.1f} Hz (textbook 8980 Hz)")

nu = 150.0
Ephot = h * nu
print(f"\n== photon at the GW frequency nu = {nu} Hz ==")
print(f"h nu = {Ephot:.3e} J = {Ephot/e:.3e} eV ; wavelength = {c/nu:.3e} m ; lambda/2pi = {c/nu/2/math.pi:.3e} m")

print("\n== plasma cutoff: electron density above which a 150 Hz wave is evanescent ==")
n_crit = eps0 * me * (2 * math.pi * nu)**2 / e**2
print(f"n_crit = {n_crit:.3e} m^-3 = {n_crit*1e-6:.3e} cm^-3")
for name, ncc in [("outer heliosphere (Gurnett 2013)", 0.002), ("local ISM at Voyager 1 (Gurnett 2013)", 0.08),
                  ("mean IGM today (Omega_b h^2=0.0224,h=0.674,Y=0.245, fully ionised)", None)]:
    if ncc is None:
        rho_b = 0.0224 * 1.87847e-26  # kg/m^3 = (Omega_b h^2) * 1.87847e-26 (rho_crit0 = 1.87847e-26 h^2 kg/m^3; h cancels)
        mH = 1.6735575e-27
        Y = 0.245
        n_e = rho_b * (1 - Y) / mH + rho_b * Y / (4 * mH) * 2
        n_m3 = n_e
    else:
        n_m3 = ncc * 1e6
    print(f"{name}: n_e = {n_m3*1e-6:.3e} cm^-3, f_p = {fp(n_m3):.3e} Hz, f_p/150Hz = {fp(n_m3)/nu:.3g}")
z_cut = (n_crit / n_m3)**(1 / 3) - 1 if False else None
# IGM redshift above which the MEAN IGM is opaque at 150 Hz (observed frequency 150 Hz*(1+z) at emission epoch z; take rest frame)
# photon emitted at z with rest-frame frequency nu_rest; opaque if f_p(z) > nu_rest.  Observed photon of 150 Hz today was
# nu_rest = 150(1+z) at z, and n_e(z)=n_e0 (1+z)^3.  Solve f_p0 (1+z)^1.5 = 150 (1+z)  ->  (1+z)^0.5 = 150/f_p0.
fp0 = fp(n_m3)
print(f"mean-IGM f_p0 = {fp0:.3f} Hz ; a photon observed at 150 Hz today was opaque-blocked at z > {(nu/fp0)**2-1:.3g} (mean density only)")

print("\n== flux of B&O's photons at Earth (GW150914-like, d=410 Mpc) ==")
L_num = 1.0e6   # photons/s, B&O ~1e6 s^-1 (upper figure quoted for nominal frequency)
d = 410 * Mpc
P = L_num * Ephot
S = P / (4 * math.pi * d**2)
print(f"photon power at source = {P:.3e} W ; flux at Earth = {S:.3e} W/m^2")
print(f"photon arrival rate = {S/Ephot:.3e} photons m^-2 s^-1")
Erms = math.sqrt(S / (c * eps0)); Brms = Erms / c
print(f"equivalent E_rms = {Erms:.3e} V/m ; B_rms = {Brms:.3e} T")
A_earth = math.pi * 6.371e6**2
tm = 5e-3
print(f"photons emitted per event = L*t_m = {L_num*tm:.3e}; energy {L_num*tm*Ephot:.3e} J vs GW energy 2 Msun c^2 = {2*1.98847e30*c**2:.3e} J "
      f"(ratio {L_num*tm*Ephot/(2*1.98847e30*c**2):.3e})")
print(f"photons crossing an Earth-sized disk (area {A_earth:.3e} m^2) during t_m: {S/Ephot*A_earth*tm:.3e}")

print("\n== versus the thermal CMB occupation at 150 Hz (Rayleigh-Jeans) ==")
x = h * nu / (kB * T0)
nocc = 1 / math.expm1(x)
print(f"x = h nu/kT = {x:.3e}; occupation n = {nocc:.3e} (kT/h nu = {kB*T0/(h*nu):.3e}); 1+2f = {1+2*nocc:.3e}")
I_cmb = 2 * kB * T0 * nu**2 / c**2   # W m^-2 sr^-1 Hz^-1
print(f"CMB specific intensity at 150 Hz (RJ) = {I_cmb:.3e} W m^-2 sr^-1 Hz^-1 (if it could propagate; it cannot in the ISM)")
print(f"signal spectral flux density if spread over 1% fractional band (1.5 Hz): {S/1.5:.3e} W m^-2 Hz^-1 ; CMB over 4 pi: {I_cmb*4*math.pi:.3e}")

print("\n== instrument bands versus 150 Hz ==")
for name, f in [("COBE/FIRAS low end (0.4 cm^-1; Fixsen 1996)", 0.4 * c * 100), ("ARCADE 2 lowest channel", 3e9),
                ("LuSEE-Night lowest", 0.1e6), ("Earth ionosphere F-layer peak (~10 MHz)", 1e7)]:
    print(f"{name}: {f:.3e} Hz ; ratio to 150 Hz = {f/nu:.3e}")

print("\n== energy-injection sensitivity of spectral distortions vs B&O eq.14 stochastic-background emissivity ==")
rho_gamma = (math.pi**2 / 15) * (kB * T0)**4 / (hbar**3 * c**3)  # J/m^3 (u = pi^2/15 (kT)^4/(hbar c)^3)
print(f"rho_gamma(T0={T0} K) = {rho_gamma:.3e} J/m^3")
fac = (7 / 8) * (4 / 11)**(4 / 3)
for dN in (0.1,):
    rho_gw = dN * fac * rho_gamma
    # eq. 14: dP/dtdV = 8 pi G^2 rho^2 / 15 in natural units  ==  8 pi G^2 rho^2 /(15 c^7) in SI (derivation in the script header: hbar cancels)
    rate_pairs = 8 * math.pi * G**2 * rho_gw**2 / (15 * c**7)
    print(f"Delta N_eff = {dN}: rho_GW = {rho_gw:.3e} J/m^3 ; pair emissivity = {rate_pairs:.3e} m^-3 s^-1 ; photons = {2*rate_pairs:.3e}")
    tH = 4.35e17
    for hw_eV in (1e-13, 1e-10, 1e6, 1e10):
        dE = 2 * rate_pairs * hw_eV * e * tH     # J/m^3 injected over a Hubble time, no CMB stimulation, no redshift
        print(f"  photon energy {hw_eV:.0e} eV: injected energy over t_H = {dE:.3e} J/m^3 = {dE/rho_gamma:.3e} of rho_CMB")
for name, lim in [("FIRAS mu<9e-5  (dE/E = mu/1.4)", 9e-5 / 1.4), ("FIRAS y<1.5e-5 (dE/E = 4y)", 4 * 1.5e-5),
                  ("PIXIE 5-sigma mu<1e-8 (dE/E = mu/1.4)", 1e-8 / 1.4)]:
    print(f"{name}: fractional CMB energy injection limit = {lim:.3e} -> {lim*rho_gamma:.3e} J/m^3")
