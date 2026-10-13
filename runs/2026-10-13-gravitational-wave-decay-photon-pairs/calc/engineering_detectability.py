"""Engineering facet: can anything detect the photons B&O's GW -> gamma gamma process would make?

Inputs (SI unless noted): B&O eq. 8 pair rate, tau = 25 pi c^2 / (6 L^2 omega_s sigma^2), L = G E / c^4
(same ħ-free form as quantitative_inputs.py; I recompute it here from scratch).
All numbers below are at face value of B&O's model: they are NOT endorsed, only used to size detectability.
"""
import math

# CODATA / constants (SI)
G = 6.67430e-11
c = 2.99792458e8
hbar = 1.054571817e-34
kB = 1.380649e-23
eV = 1.602176634e-19
Msun = 1.98847e30
Mpc = 3.0856775814913673e22
yr = 3.15576e7
T0 = 2.7255  # K, CMB today

print("=== A. GW150914 point, B&O inputs (E_rel = 2 Msun c^2, nu = 150 Hz, t_m = 5 ms) ===")
E = 2 * Msun * c**2
nu = 150.0
w = 2 * math.pi * nu
tm = 5e-3
sigma = 1 / tm
L = G * E / c**4
tau_vac = 25 * math.pi * c**2 / (6 * L**2 * w * sigma**2)
x = hbar * w / (kB * T0)
f_gam = 1 / math.expm1(x)
stim = 1 + 2 * f_gam
tau_stim = tau_vac / stim
Lgam_stim = 1 / tau_stim  # photons/s as B&O define L_gamma = 1/tau
print(f"L = G E/c^4 = {L:.3e} m ; omega_s = {w:.3e} rad/s ; hbar*omega = {hbar*w/eV:.3e} eV = {hbar*w:.3e} J")
print(f"tau(vacuum) = {tau_vac:.3e} s ; f_gamma = {f_gam:.3e} ; stimulation 1+2f = {stim:.3e}")
print(f"tau(CMB-stimulated) = {tau_stim:.3e} s ; L_gamma = {Lgam_stim:.3e} photons/s")

print("\n=== B. Photon flux at an observer at D = 410 Mpc if the photons were emitted isotropically ===")
D = 410 * Mpc
area = 4 * math.pi * D**2
phi_n = Lgam_stim / area
print(f"4 pi D^2 = {area:.3e} m^2")
print(f"photon number flux = {phi_n:.3e} photons m^-2 s^-1 ; energy flux = {phi_n*hbar*w:.3e} W m^-2")
lam = c / nu
Aeff = lam**2 / (4 * math.pi)  # effective area of an isotropic antenna
print(f"lambda = {lam:.3e} m ({lam/1e3:.0f} km) ; isotropic effective area lambda^2/4pi = {Aeff:.3e} m^2")
for T in (1.0, 1e3):
    print(f"  expected photons absorbed by one isotropic antenna in {T:g} s = {phi_n*Aeff*T:.3e}")
# for comparison, flux needed for ONE photon per second in that antenna
print(f"  flux needed for 1 photon/s in that antenna = {1/Aeff:.3e} photons m^-2 s^-1 ; this is {1/Aeff/phi_n:.2e} x the B&O flux")

print("\n=== C. CMB's own Rayleigh-Jeans brightness at 150 Hz, per Hz, per sr ===")
B = 2 * nu**2 * kB * T0 / c**2
print(f"B_nu(RJ, 150 Hz) = {B:.3e} W m^-2 Hz^-1 sr^-1 ; 4pi sr, 1 Hz bandwidth: {B*4*math.pi:.3e} W m^-2")
print(f"B&O energy flux / this = {phi_n*hbar*w/(B*4*math.pi):.3e}")

print("\n=== D. Plasma cut-off: electron density at which 150 Hz is evanescent ===")
for f in (150.0, 2600.0):
    ne = (f / 8980.0) ** 2
    print(f"f = {f:g} Hz -> n_e = {ne:.3e} cm^-3 (nu_p = 8980 sqrt(n_e) Hz)")
for name, ne in (("mean IGM (z=0, fully ionised)", 2.2e-7), ("VLISM (Voyager 1)", 0.08), ("warm ISM", 0.03), ("solar wind 1 AU", 5.0), ("ionospheric F layer", 1e6)):
    print(f"  {name:32s} n_e = {ne:9.3g} cm^-3 -> nu_p = {8980*math.sqrt(ne):.3e} Hz ; 150 Hz photon propagates: {150 > 8980*math.sqrt(ne)}")

print("\n=== E. Stochastic background (eq. 14) vs CMB distortion sensitivity ===")
hbar_eV_s = 6.582119569e-16
hbarc_eV_m = 1.973269804e-7
MPl = 1.220890e28  # eV, G = 1/MPl^2 in natural units
Gnat = 1 / MPl**2
rho_crit_SI = 3 * (67.4e3 / Mpc) ** 2 / (8 * math.pi * G) * c**2  # J/m^3
print(f"rho_crit c^2 (h=0.674) = {rho_crit_SI:.3e} J/m^3")
def pair_rate(Omega):
    rho = Omega * rho_crit_SI / eV  # eV/m^3
    rho_nat = rho * hbarc_eV_m**3  # eV^4
    r_nat = 8 * math.pi * Gnat**2 * rho_nat**2 / 15  # eV^4 -> pairs per volume per time
    return r_nat / (hbarc_eV_m**3 * hbar_eV_s)  # per m^3 per s
rho_cmb_eV_m3 = (math.pi**2 / 15) * (kB * T0 / eV) ** 4 / hbarc_eV_m**3  # eV/m^3
print(f"rho_CMB = {rho_cmb_eV_m3:.3e} eV/m^3")
tH = 13.8e9 * yr
for label, Om, fgw in (("primordial bound, h2 Omega=1.7e-6 (Delta N=0.3)", 1.7e-6 / 0.674**2, 25.0), ("LVK scale-invariant Omega(25Hz)<=2.8e-9", 2.8e-9, 25.0), ("PTA-band Omega ~ 1e-9 at 1 nHz", 1e-9, 1e-9)):
    r = pair_rate(Om)
    Ephot = hbar * 2 * math.pi * fgw / eV  # eV per photon
    xx = Ephot * eV / (kB * T0)
    fg = 1 / math.expm1(xx)
    for st in (1.0, 1 + 2 * fg):
        dE = 2 * r * tH * Ephot * st  # eV/m^3 injected, no redshift, over a Hubble time
        print(f"{label}: pair rate = {r:.3e} m^-3 s^-1 ; photon E = {Ephot:.3e} eV ; stim x{st:.2e} ; injected energy over t_H = {dE:.3e} eV/m^3 ; fraction of rho_CMB = {dE/rho_cmb_eV_m3:.3e}")
print("Distortion thresholds (energy fraction ~ 4 y or mu/1.4 for mu-era injection):")
for name, y in (("FIRAS |y|<1.5e-5 (95%)", 1.5e-5), ("PIXIE 1 sigma y 3.4e-9", 3.4e-9), ("Super-PIXIE 1 sigma y 1.6e-9", 1.6e-9)):
    print(f"  {name}: dE/E = 4y = {4*y:.2e}")
for name, mu in (("FIRAS |mu|<9e-5 (95%)", 9e-5), ("PIXIE 1 sigma mu 3e-8", 3e-8), ("Super-PIXIE 1 sigma mu 7.7e-9", 7.7e-9)):
    print(f"  {name}: dE/E = mu/1.401 = {mu/1.401:.2e}")

print("\n=== F. GW amplitude depletion along path (B&O tau_h = tau N0), GW150914 at 410 Mpc ===")
N0 = E / (hbar * w)
tau_h_vac = tau_vac * N0
tau_h_stim = tau_stim * N0
tprop = D / c
print(f"N0 = {N0:.3e} gravitons ; tau_h(vac) = {tau_h_vac:.3e} s ; tau_h(stim) = {tau_h_stim:.3e} s ; light travel time = {tprop:.3e} s")
print(f"fractional energy lost over path: vac {tprop/tau_h_vac:.3e} ; stimulated {tprop/tau_h_stim:.3e}")
print("(compare LVK amplitude calibration uncertainty of order a few per cent: see engineering.md RE-10)")
