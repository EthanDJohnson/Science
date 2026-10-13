"""Quantitative inputs for the Blas-Oller (B&O, arXiv:2607.24930v2) re-check.

All numbers are computed taking B&O's eq. 8-12 AT FACE VALUE (this script does not test whether
eq. 8 is right, only what it implies numerically with real input numbers). SI unless stated.

tau (reaction time, B&O eq. 10) in hbar-free SI form:
    tau = 25*pi*c^2 / (6 * L^2 * omega_s * sigma_omega^2),  L = G*E_rel/c^4   (derived from eq. 10
    by restoring units; checked against eq. 11-12 below)
Photon number emitted in time t << tau:  N_gamma = t/tau  (eq. 9);  W_gamma = hbar*omega_s/tau (eq. 11).
CMB stimulation (eq. after 12): W -> W*(1 + 2 f_gamma(omega_s)), f = 1/(exp(hbar w/kT)-1).
"""
import math

# CODATA / standard constants (SI)
c = 2.99792458e8
G = 6.67430e-11
hbar = 1.054571817e-34
kB = 1.380649e-23
eV = 1.602176634e-19
Msun = 1.98841e30
Mpc = 3.0856775814913673e22
yr = 3.15576e7
T0 = 2.7255  # K, CMB
Mpl_eV = 1.220890e28  # Planck mass in eV (G = 1/Mpl^2 natural)
H0_kms = 67.4  # Planck 2018
H0 = H0_kms * 1e3 / Mpc  # s^-1
h = H0_kms / 100.0
Omega_c_h2 = 0.1200
Omega_b_h2 = 0.0224
Omega_DM = Omega_c_h2 / h**2
rho_c = 3 * H0**2 / (8 * math.pi * G)  # kg/m^3
alpha = 1 / 137.035999


def f_cmb(omega):
    x = hbar * omega / (kB * T0)
    return 1.0 / math.expm1(x)


def tau_BO(E_rel, omega, sigma):
    L = G * E_rel / c**4
    return 25 * math.pi * c**2 / (6 * L**2 * omega * sigma**2)


print("=== 1. GW150914 through B&O eqs. 8-13 (SI) ===")
for label, Erel_Msun in (("B&O input E_rel=2 Msun c^2", 2.0), ("LVK central E_rad=3.0 Msun c^2", 3.0)):
    E = Erel_Msun * Msun * c**2
    nu = 150.0
    omega = 2 * math.pi * nu
    tm = 5e-3
    sigma = 1.0 / tm
    tau = tau_BO(E, omega, sigma)
    N0 = E / (hbar * omega)
    fg = f_cmb(omega)
    stim = 1 + 2 * fg
    tau_s = tau / stim
    W = hbar * omega / tau
    W_s = W * stim
    rm = 2 * G * E / c**4
    ell = c * tm
    W12 = 3 / (50 * math.pi) * (rm / ell) ** 2 * hbar * omega**2
    MH = 65 * Msun
    WH = hbar * c**6 / (15360 * math.pi * G**2 * MH**2)
    print(f"-- {label}")
    print(f"   E_rel = {E:.3e} J ; omega_s = {omega:.1f} rad/s ; sigma_omega = 1/t_m = {sigma:.1f} s^-1")
    print(f"   N0 = E/(hbar omega) = {N0:.3e} gravitons")
    print(f"   tau (vacuum) = {tau:.3e} s  (>> t_m = 5 ms: B&O's tau<<t_m condition is violated at nominal point)")
    print(f"   W_gamma (eq.11) = {W:.3e} W ; via eq.12 = {W12:.3e} W (should agree)")
    print(f"   f_gamma(150 Hz) = {fg:.3e}; stimulation factor 1+2f = {stim:.3e}")
    print(f"   tau with CMB stim = {tau_s:.3e} s ; L_gamma = 1/tau = {1/tau_s:.3e} photons/s (B&O Fig 2b: ~1e6 s^-1)")
    print(f"   W_gamma with stim = {W_s:.3e} W ; photons emitted in one t_m = {tm/tau_s:.3e}")
    print(f"   Hawking W_H(65 Msun) = {WH:.3e} W ; W_H/W_gamma(vacuum) = {WH/W:.3e} (B&O eq.13: 1e2-1e3)")
    print(f"   energy in photons / E_GW over t_m (stim) = {W_s*tm/E:.3e}")
    print(f"   depletion time tau_h = tau*E/(hbar omega) (vacuum) = {tau*N0:.3e} s = {tau*N0/yr:.3e} yr")

print()
print("=== 2. Real-source inputs ===")
Lpeak = 3.6e49
print(f"GW150914 peak luminosity 3.6e56 erg/s = {3.6e56*1e-7:.2e} W ; LVK E_rad 3.0 Msun c^2 = {3.0*Msun*c**2:.3e} J")
# strain-to-energy flux check at 410 Mpc: F = c^3/(16 pi G) <hdot^2> ; peak h=1e-21, f~150 Hz (rough)
d = 410 * Mpc
F = Lpeak / (4 * math.pi * d**2)
print(f"peak GW energy flux at Earth, L/(4 pi d^2), d=410 Mpc: {F:.3e} W/m^2")
hpk = 1e-21
Fcheck = c**3 / (16 * math.pi * G) * (2 * math.pi * 150) ** 2 * hpk**2 / 2  # <hdot^2> = (w h)^2 /2 per polarization sum approx
print(f"c^3 w^2 h^2/(32 pi G) with h=1e-21, 150 Hz: {c**3*(2*math.pi*150)**2*hpk**2/(32*math.pi*G):.3e} W/m^2 (cross-check, order of magnitude only)")
fgw_isco = lambda M: c**3 / (6**1.5 * math.pi * G * M)  # GW frequency at ISCO = 2 * f_orb = c^3/(6^1.5 pi G M)
print(f"f_GW,ISCO for 1 Msun = {fgw_isco(Msun):.1f} Hz (B&O: 8800 pi rad/s /2pi = 4400 Hz) ; for 65 Msun = {fgw_isco(65*Msun):.1f} Hz")
print(f"GW150914 nominal merger frequency 150 Hz / f_GW,ISCO(65 Msun) = {150/fgw_isco(65*Msun):.2f}")

print()
print("=== 3. Plasma frequency (photon effective mass) ===")
me = 9.1093837015e-31
eps0 = 8.8541878128e-12
e = 1.602176634e-19


def nu_p(ne_cm3):
    ne = ne_cm3 * 1e6
    return math.sqrt(ne * e**2 / (eps0 * me)) / (2 * math.pi)


def w_p_eV(ne_cm3):
    return 2 * math.pi * nu_p(ne_cm3) * hbar / eV


nb0 = Omega_b_h2 * rho_c / (h**2) / 1.67262192e-27 * 1e-6  # baryon number density today, cm^-3 (all baryons as protons; approx)
Yp = 0.245
ne0 = nb0 * (1 - Yp / 2 * 1.0 / 1.0 * 1.0) if False else nb0 * ((1 - Yp) + Yp / 2)
print(f"n_b today = {nb0:.3e} cm^-3 ; fully ionised n_e today = {ne0:.3e} cm^-3 (B&O/brief: omega_p ~1e-14 eV)")
for label, ne in (("IGM mean, fully ionised, z=0", ne0), ("IGM z=0.5 mean (x(1+z)^3)", ne0 * 1.5**3),
                  ("fully ionised z=1e3 (not physical: recombined)", ne0 * 1e9), ("fully ionised z=1e5", ne0 * 1e15),
                  ("fully ionised z=3e6", ne0 * (3e6) ** 3), ("warm ISM 0.03 cm^-3", 0.03), ("solar wind at 1 AU ~5 cm^-3", 5.0),
                  ("ionospheric F-layer ~1e6 cm^-3", 1e6)):
    print(f"   {label:50s} n_e={ne:10.3e} cm^-3 : nu_p = {nu_p(ne):12.4e} Hz ; omega_p = {w_p_eV(ne):10.3e} eV")
print(f"   150 Hz photon energy = {2*math.pi*150*hbar/eV:.3e} eV ; CMB kT = {kB*T0/eV:.3e} eV")
print(f"   (1+z)^3 scaling: omega_p(z) = omega_p(0)*(1+z)^1.5 for a fully ionised medium; omega_s(z)=omega_s(0)*(1+z) so omega_s/omega_p falls as (1+z)^-0.5")

print()
print("=== 4. Stochastic background, B&O eq. 14 ===")
# rho_GW upper values
for label, OmGWh2 in (("BBN/CMB integral bound 5.6e-6*DeltaN, DeltaN=0.3 (Planck+BAO 95% ~ N_eff<3.3)", 5.6e-6 * 0.3),
                      ("DeltaN=0.1", 5.6e-6 * 0.1), ("DeltaN=0.05", 5.6e-6 * 0.05),
                      ("LVK O4a Omega(25Hz)<=2.8e-9 flat, h^2 included", 2.8e-9 * h**2),
                      ("NANOGrav ~ Omega h^2 ~ 1e-9 band", 1e-9)):
    Om = OmGWh2 / h**2
    rho = Om * rho_c  # kg/m^3
    u = rho * c**2  # J/m^3
    u_eV4 = u / eV  # eV/m^3
    # natural units: lengths in 1/eV
    m_inv_eV = hbar * c / eV  # 1 m = 1/(hbar c/eV) ... hbar c = 1.973e-7 eV m -> 1 m = 5.068e6 eV^-1
    inv_m_in_eV = hbar * c / eV  # eV per m^-1
    rho_nat = u_eV4 * inv_m_in_eV**3  # eV^4
    Gn = 1.0 / Mpl_eV**2
    rate_nat = 8 * math.pi * Gn**2 * rho_nat**2 / 15  # eV^4 -> pairs per volume per time
    # convert eV^4 -> m^-3 s^-1 : divide by (inv_m_in_eV)^3 for volume and multiply by eV/hbar for time
    rate_SI = rate_nat / inv_m_in_eV**3 * (eV / hbar)
    print(f"   {label}")
    print(f"      Omega_GW h^2 = {OmGWh2:.2e} ; Omega_GW = {Om:.2e} ; rho_GW c^2 = {u:.3e} J/m^3 = {u_eV4:.3e} eV/m^3")
    print(f"      eq.14 pair rate = {rate_SI:.3e} m^-3 s^-1 ; photon rate (x2) = {2*rate_SI:.3e} m^-3 s^-1 (B&O: ~1e-110)")

print()
print("=== 5. ULDM inputs and B&O eqs. 16-18 ===")
rho_DM_cosmic_GeVcm3 = Omega_DM * rho_c * c**2 / eV * 1e-6 / 1e9
print(f"Omega_DM = {Omega_DM:.4f} ; cosmic mean DM density = {rho_DM_cosmic_GeVcm3:.3e} GeV/cm^3")
hbarc_eVm = hbar * c / eV
for rho_loc in (0.3, 0.4, 0.6):
    print(f"   local DM {rho_loc} GeV/cm^3 / cosmic mean = {rho_loc/rho_DM_cosmic_GeVcm3:.3e} (B&O x_MW ~ 1e5)")
print(f"   v_rms ~ 220 km/s = {220e3/c:.2e} c (B&O v = 1e-3)")


def N_phi(m_eV, v, Om=Omega_DM, x=1.0):
    rho_eV_m3 = Om * rho_c * c**2 / eV  # eV/m^3
    rho_nat = rho_eV_m3 * hbarc_eVm**3 * x  # eV^4
    n = rho_nat / m_eV  # eV^3
    p = m_eV * v
    return n * (2 * math.pi) ** 3 / (4 * math.pi / 3 * p**3)


print(f"   N_phi(m=1e-22 eV, v=1e-3, Omega=0.26 version) = {N_phi(1e-22,1e-3,0.26):.3e} (B&O eq.16: 6e87; ratio shows B&O used (2pi)^3 n /(4pi/3 (m v)^3))")
print(f"   N_phi(m=1e-22 eV, v=1e-3, Planck Omega_DM={Omega_DM:.3f}) = {N_phi(1e-22,1e-3):.3e}")

# eq. 18 reconstruction: W_phi = (9 pi/256) G m^2 v^3 N0^2 H0^2 Omega_DM * x_MW  (garbled in extraction; reconstructed from eq 17 + 16, ASSUMPTION)
def W_phi(m_eV, v, E_over_M=3.0 / 65.0, x=1e5):
    omega_s = m_eV / (hbar / eV)  # rad/s  (omega_s ~ m_DM)
    M = 27646.0 / omega_s * Msun  # B&O: omega_ISCO = 8800 pi (Msun/M) s^-1
    E = E_over_M * M * c**2
    N0 = E / (hbar * omega_s)
    Gm2 = (m_eV / Mpl_eV) ** 2
    H0_eV = hbar * H0 / eV
    W_nat = 9 * math.pi / 256 * Gm2 * v**3 * N0**2 * H0_eV**2 * Omega_DM * x  # eV^2
    W_SI = W_nat * eV * (eV / hbar)
    return W_SI, M / Msun, N0


for m in (1e-21, 1e-20, 1e-22):
    W, Mbin, N0 = W_phi(m, 1e-3)
    print(f"   m={m:.0e} eV: binary mass at ISCO {Mbin:.3e} Msun ; N0 = {N0:.3e} (E_rel=3/65 M c^2) ; W_phi (x_MW=1e5) = {W:.3e} W (B&O eq 18: ~1e14 W x ... ; reconstruction assumption)")

print()
print("=== 6. Inspiral cases through B&O eq.10 (quadrupole chirp; eps=0.1 bin; sigma_omega=1/t_eps; E_rel=t_eps*L_GW) ===")
# standard Newtonian chirp: df/dt = (96/5) pi^(8/3) (G Mc/c^3)^(5/3) f^(11/3); L = (32/5)(c^5/G)(G Mc pi f/c^3)^(10/3)
def inspiral(Mc_Msun, f, eps=0.1, label=""):
    Mc = Mc_Msun * Msun
    tc = G * Mc / c**3
    fdot = (96 / 5) * math.pi ** (8 / 3) * tc ** (5 / 3) * f ** (11 / 3)
    t_eps = eps * f / fdot
    L = (32 / 5) * (c**5 / G) * (tc * math.pi * f) ** (10 / 3)
    E = t_eps * L
    omega = 2 * math.pi * f
    sigma = 1.0 / t_eps
    tau = tau_BO(E, omega, sigma)
    fg = f_cmb(omega)
    stim = 1 + 2 * fg
    print(f"-- {label}: Mc={Mc_Msun} Msun, f_GW={f} Hz, eps={eps}")
    print(f"   fdot = {fdot:.3e} Hz/s ; t_eps = {t_eps:.3e} s ; L_GW = {L:.3e} W ; E_rel = {E:.3e} J")
    print(f"   tau(vacuum) = {tau:.3e} s ; 1/(eps omega) = {1/(eps*omega):.3e} s ; stim factor {stim:.3e} ; tau(stim) = {tau/stim:.3e} s ; L_gamma(stim) = {stim/tau:.3e} photons/s ; photon energy {hbar*omega/eV:.3e} eV")
    print(f"   photon power W_gamma(vacuum) = {hbar*omega/tau:.3e} W ; (stim) = {hbar*omega/tau*stim:.3e} W ; ratio to L_GW (stim) = {hbar*omega/tau*stim/L:.3e}")

inspiral(1.188, 100.0, label="GW170817-like DNS at 100 Hz")
inspiral(1.188, 30.0, label="GW170817-like DNS at 30 Hz")
inspiral(0.3, 6.2e-3, label="galactic WD binary ~ LISA band (HM Cnc-like Mc assumed 0.3 Msun, 6.2 mHz; ASSUMED parameters)")
inspiral(28.0, 50.0, label="GW150914-like BBH inspiral (Mc~28 Msun) at 50 Hz")
