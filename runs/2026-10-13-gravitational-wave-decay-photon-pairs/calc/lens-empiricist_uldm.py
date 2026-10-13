"""Empiricist lens: B&O ULDM channel (eqs. 16-18) re-checked, and what any observation could see.

Units: natural units (hbar = c = 1) for the formulas, converted to SI (W, s, Hz) for output.
B&O = Blas & Oller arXiv:2607.24930v2, p. 5.
  eq. 16: N_phi ~ 6e87 (1e-22 eV/m)^4 (1e-3/v)^3 (Omega_DM/0.26) x_MW
  eq. 17: dP/dt ~ G^2 m^5 N0^2 v^6 N_phi / 128, valid for m <= omega_s <~ m(1+v^2/2), sigma_omega ~ m v^2/2
  text:   W_phi = 9 pi G m^2 v^3 N0^2 H0^2 Omega_DM / 256 (x_MW implied by eq. 18)
  eq. 18: W_phi ~ 1e14 x_MW (1e-21 eV/m)^2 (v/1e-3)^3 W ; ~1e54 s^-1 at m = 1e-21 eV
  binary: m_DM ~ omega_s ~ 8800 pi (Msun/M) s^-1 (ISCO); E_rel ~ 2 Msun (M/65 Msun) (merger scaling, D-27)
"""
import math
import sympy as sp

# --- constants (SI) ---
G = 6.67430e-11
c = 2.99792458e8
hbar = 1.054571817e-34
eV = 1.602176634e-19
Msun = 1.98892e30
Mpc = 3.0857e22
H0 = 67.4e3 / Mpc          # s^-1 (Planck 2018, D-32)
Omega_DM = 0.264
Lsun = 3.828e26            # W (IAU nominal)
rho_c = 3 * H0**2 / (8 * math.pi * G)  # kg/m^3
Mpl_eV = math.sqrt(hbar * c / G) * c**2 / eV  # 1/sqrt(G) in eV
hbar_eVs = hbar / eV
hbarc_eVm = hbar * c / eV

print("=== 1. Symbolic check: eq. 17 + eq. 16 -> W_phi ===")
Gs, m, N0, v, H, Om, x = sp.symbols("G m N0 v H0 Omega x", positive=True)
rho = 3 * H**2 * Om * x / (8 * sp.pi * Gs)
Nphi = (rho / m) * (2 * sp.pi) ** 3 / (sp.Rational(4, 3) * sp.pi * (m * v) ** 3)
dPdt = Gs**2 * m**5 * N0**2 * v**6 * Nphi / 128
W_from17 = sp.simplify(2 * m * dPdt)   # two scalars of energy ~m per event
W_BO = 9 * sp.pi * Gs * m**2 * v**3 * N0**2 * H**2 * Om * x / 256
print("  N_phi (B&O eq.16 form) =", sp.simplify(Nphi))
print("  2 m dP/dt from eq.17   =", W_from17)
print("  B&O printed W_phi*x    =", W_BO, " ; ratio =", sp.simplify(W_from17 / W_BO))

print()
print("=== 2. Numbers: eq. 16 and eq. 18 ===")
def N_phi(m_eV, v_, x_=1.0):
    rho_nat = Omega_DM * rho_c * c**2 / eV * hbarc_eVm**3 * x_   # eV^4
    return (rho_nat / m_eV) * (2 * math.pi) ** 3 / (4 * math.pi / 3 * (m_eV * v_) ** 3)
print(f"  N_phi(1e-22 eV, v=1e-3, x=1) = {N_phi(1e-22, 1e-3):.3e}  (B&O: 6e87)")

def merger(m_eV, E_frac):
    omega = m_eV / hbar_eVs                 # rad/s, graviton energy = m
    M = 8800 * math.pi / omega * Msun       # kg
    E = E_frac * M * c**2                   # J
    N0 = E / (hbar * omega)
    return omega, M, E, N0

def W_phi_SI(m_eV, v_, N0, x_=1.0):
    Gn = 1.0 / Mpl_eV**2                    # eV^-2
    H0_eV = hbar_eVs * H0
    W_nat = 9 * math.pi * Gn * m_eV**2 * v_**3 * N0**2 * H0_eV**2 * Omega_DM * x_ / 256  # eV^2
    return W_nat * eV / hbar_eVs            # J/s

for E_frac, lab in ((2.0 / 65, "E_rel=2/65 Mc^2 (B&O merger scaling)"), (3.0 / 65, "E_rel=3/65 Mc^2 (LVK GW150914 ratio)")):
    for m_eV in (1e-22, 1e-21, 2e-20):
        om, M, E, N0 = merger(m_eV, E_frac)
        W = W_phi_SI(m_eV, 1e-3, N0)
        print(f"  {lab}: m={m_eV:.0e} eV -> f_GW={om/2/math.pi:.3e} Hz, M={M/Msun:.3e} Msun, N0={N0:.3e}, "
              f"W_phi(x=1)={W:.3e} W, scalars/s={W/(m_eV*eV):.3e}")
print("  B&O eq.18: 1e14 W x_MW at 1e-21 eV ; ~1e54 s^-1")

print()
print("=== 3. Can the resonance (eq. 17) be met by a real chirp? m = 1e-21 eV, v = 1e-3 ===")
def chirp_checks(m_eV, v_, E_frac=2.0 / 65):
    om, M, E, N0 = merger(m_eV, E_frac)
    f = om / (2 * math.pi)
    Mc = M * 0.25 ** 0.6                     # equal mass chirp mass
    tc = G * Mc / c**3
    fdot = (96 / 5) * math.pi ** (8 / 3) * tc ** (5 / 3) * f ** (11 / 3)   # Newtonian quadrupole
    frac_bw = v_**2 / 2
    sigma = m_eV * v_**2 / 2 / hbar_eVs      # rad/s
    T_req = 1 / sigma                        # s, packet duration eq.17 assumes
    t_band = frac_bw * f / fdot              # s, time the chirp spends in the resonance band
    t_coh = 2 * math.pi * hbar_eVs / (m_eV * v_**2)   # ULDM coherence time
    f_over_fdot = f / fdot
    dEdf = (math.pi ** (2 / 3) / 3) * G ** (2 / 3) * Mc ** (5 / 3) * f ** (-1 / 3)  # J/Hz
    E_band = dEdf * frac_bw * f
    N_band = E_band / (hbar * om)
    W_face = W_phi_SI(m_eV, v_, N0)
    W_band = W_phi_SI(m_eV, v_, N_band)
    print(f"  m={m_eV:.0e} eV: f={f:.3e} Hz (period {1/f/86400:.1f} d), M={M/Msun:.2e} Msun")
    print(f"    resonance fractional bandwidth v^2/2 = {frac_bw:.1e}; sigma_omega = {sigma:.3e} rad/s")
    print(f"    packet duration eq.17 needs 1/sigma = {T_req:.3e} s = {T_req/3.156e7:.3e} yr ; ULDM coherence time = {t_coh/3.156e7:.3e} yr")
    print(f"    chirp f/fdot at that f (Newtonian, equal mass) = {f_over_fdot:.3e} s ; time inside resonance band = {t_band:.3e} s")
    print(f"    shortfall: t_band / (1/sigma) = {t_band/T_req:.3e}")
    print(f"    gravitons spectrally inside band: N_band = {N_band:.3e} vs B&O N0 = {N0:.3e} ; (N_band/N0)^2 = {(N_band/N0)**2:.3e}")
    print(f"    W_phi(x=1): face value {W_face:.3e} W ; with in-band N {W_band:.3e} W")
    return W_face, W_band, M, E

W_face, W_band, M, E = chirp_checks(1e-21, 1e-3)
chirp_checks(2e-20, 1e-3)

print()
print("=== 4. Compare with anything observable ===")
L_GW_peak = 3.6e49    # W, GW150914 peak; peak luminosity of comparable-mass mergers is ~mass independent
for x_ in (1.0, 1e5, 2.4e5):
    print(f"  x_MW={x_:.1e}: W_phi(face) = {W_face*x_:.3e} W = {W_face*x_/Lsun:.3e} Lsun ; W_phi/L_GW,peak = {W_face*x_/L_GW_peak:.3e}")
print(f"  x needed for W_phi = 1 Lsun at face value: {Lsun/W_face:.3e} (cosmic-mean multiples)")
# depletion of GW energy during a merger of duration ~ 10 GM/c^3 * ... use t_m = 5 ms (M/65 Msun)
t_m = 5e-3 * (M / Msun) / 65
print(f"  merger time t_m = {t_m:.3e} s ; fractional GW energy converted (face, x=1e5) = {W_face*1e5*t_m/E:.3e}")
print("  Scalars of energy ~1e-21 eV coupled only gravitationally: no detector channel exists (no lab coupling).")

print()
print("=== 5. Observational bound on GW damping from GW170817 (Lagos et al. 2019, c_M) ===")
OmL = 0.685
z = 0.0099   # NGC 4993 (GW170817 host) Hubble-flow redshift, approximate
for cM in (-9 - 28, -9, -9 + 21):
    # d_GW/d_EM = exp( 0.5 * int_0^z alpha_M/(1+z') dz' ), alpha_M = c_M Omega_L(z)/Omega_L0 ~ c_M at z << 1
    ratio = math.exp(0.5 * cM * math.log(1 + z))
    print(f"  c_M={cM:+d}: d_GW/d_EM - 1 = {ratio-1:+.3e} (amplitude); energy-flux change ~ {ratio**-2-1:+.3e}")
print("  => observed GW amplitudes are consistent with no damping to ~10% over ~40 Mpc; B&O depletion 1e-66..1e-57 [D-47] is untestable.")
