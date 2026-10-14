"""Falsifier C8-0 (physics): B&O eqs. 16-18, Bose-enhanced resonant GW -> ULDM pairs.

Units: natural units (hbar = c = 1, energies in eV) for eqs. 16-18; SI for astrophysical numbers.
Parts:
 A. Reproduce eq. 18 at B&O's ISCO resonance (validation of inputs).
 B. Chirp time inside the resonance band sigma = m v^2/2 vs the coherence 1/sigma (independent route).
 C. Best case: a quasi-monochromatic binary slow enough to stay in band for 1/sigma; its eq.-17 power.
 D. DM density needed for 1 Lsun, and whether that region lies inside its own horizon.
 E. Kinematics: the outgoing multipole carries no incoming (head-on) component; Q ~ 0 Fourier
    weight of the 2w part of h^2 for retarded vs standing waves (scalar toy).
"""
import numpy as np
import sympy as sp

# --- constants (SI) ---
c = 2.99792458e8; G = 6.67430e-11; hbarSI = 1.054571817e-34; eVJ = 1.602176634e-19
hbar_eVs = hbarSI / eVJ
Msun = 1.98847e30; Lsun = 3.828e26; Mpc = 3.0857e22; yr = 3.15576e7
H0_SI = 67.4e3 / Mpc
h = 0.674; Omega_DM = 0.120 / h**2
rho_crit = 3 * H0_SI**2 / (8 * np.pi * G)          # kg/m^3
rho_DM_mean = Omega_DM * rho_crit
t_univ = 13.8e9 * yr

# natural-unit conversions
MPl_eV = np.sqrt(hbarSI * c**5 / G) / eVJ
G_nat = 1.0 / MPl_eV**2                               # eV^-2
H0_eV = H0_SI * hbar_eVs                              # eV

m_eV = 1e-21; v = 1e-3
w = m_eV / hbar_eVs                                   # rad/s, resonance w = m
f = w / (2 * np.pi)
sigma = w * v**2 / 2                                  # rad/s
print("=== inputs ===")
print(f"M_Pl = {MPl_eV:.4e} eV; H0 = {H0_eV:.4e} eV; Omega_DM = {Omega_DM:.4f}; rho_DM,mean = {rho_DM_mean:.3e} kg/m^3")
print(f"m = {m_eV:.1e} eV: w = {w:.4e} rad/s, f_GW = {f:.4e} Hz, sigma = m v^2/2 = {sigma:.4e} rad/s, 1/sigma = {1/sigma:.4e} s = {1/sigma/yr:.3e} yr")


def W_eq18(N0, x=1.0, m=m_eV, vv=v):
    """B&O eq. 17 x 2m with eq. 16 substituted: W = 9 pi G m^2 v^3 N0^2 H0^2 Omega x / 256 (natural units, eV^2) -> W (SI)."""
    W_eV2 = 9 * np.pi * G_nat * m**2 * vv**3 * N0**2 * H0_eV**2 * Omega_DM * x / 256
    return W_eV2 / hbar_eVs * eVJ


def N_phi(x=1.0, m=m_eV, vv=v):
    return 9 * np.pi * H0_eV**2 * Omega_DM * x / (4 * G_nat * m**4 * vv**3)

print(f"eq. 16: N_phi(1e-22 eV, x=1) = {N_phi(m=1e-22):.3e} (B&O ~6e87)")

# --- A. eq. 18 at ISCO ---
M = 2 * c**3 / (6**1.5 * G * w)                       # equal-mass binary with f_GW(ISCO) = f
E_rel = (2 / 65) * M * c**2
N0 = E_rel / (hbarSI * w)
WA = W_eq18(N0)
print("\n=== A. eq. 18 validation ===")
print(f"M(ISCO resonance) = {M/Msun:.4e} Msun, N0 = {N0:.4e}, W_phi(x=1) = {WA:.3e} W (B&O: ~1e14 W x_MW)")

# --- B. chirp in band ---
Mc = M * 0.25**0.6
fdot = (96 / 5) * np.pi**(8 / 3) * (G * Mc / c**3)**(5 / 3) * f**(11 / 3)
t_in = (v**2 / 2) * f / fdot
L_isco = (32 / 5) * (c**5 / G) * (np.pi * G * Mc * f / c**3)**(10 / 3)
print("\n=== B. chirp ===")
print(f"Mc = {Mc/Msun:.4e} Msun, f/fdot = {f/fdot:.4e} s, time in resonance band t_in = {t_in:.3f} s")
print(f"coherence needed 1/sigma = {1/sigma:.4e} s; shortfall t_in*sigma = {t_in*sigma:.3e}")
N_band = L_isco * t_in / (hbarSI * w)
print(f"quadrupole L at f = {L_isco:.3e} W; gravitons in band N_band = {N_band:.3e}; (N_band/N0)^2 = {(N_band/N0)**2:.3e}")
print(f"eq. 18 with N0 -> N_band: W = {W_eq18(N_band):.3e} W x_MW")

# --- C. slowest source that stays in band for 1/sigma ---
t_req = (2 / v**2) / sigma                            # f/fdot needed so that t_in >= 1/sigma
GMc_c3 = (5 / (96 * np.pi**(8 / 3) * f**(8 / 3) * t_req))**(3 / 5)
Mc_max = GMc_c3 * c**3 / G
L_max = (32 / 5) * (c**5 / G) * (np.pi * GMc_c3 * f)**(10 / 3)
N_coh = L_max * (1 / sigma) / (hbarSI * w)            # gravitons in one coherence cell
WC = W_eq18(N_coh)
print("\n=== C. long-lived, resonance-satisfying binary ===")
print(f"required chirp time f/fdot >= 4/(m v^4) = {t_req:.4e} s = {t_req/t_univ:.2f} x age of Universe")
print(f"=> Mc <= {Mc_max/Msun:.4e} Msun, L_GW <= {L_max:.4e} W, N0 per coherence cell = {N_coh:.4e}")
print(f"eq. 17/18 at face value with this N0: W_phi = {WC:.4e} W x_MW; at x = 1e5: {WC*1e5:.3e} W; ratio to L_GW (x=1e5) = {WC*1e5/L_max:.3e}")
print(f"best of chirp (B) and steady (C) feeds, x=1: {max(W_eq18(N_band), WC):.3e} W")

# --- D. density for 1 Lsun ---
print("\n=== D. DM density for 1 Lsun ===")
for label, W1 in [("eq. 18 as printed (ISCO, N0 = all gravitons)", WA),
                  ("in-band chirp feed (B)", W_eq18(N_band)),
                  ("steady resonant feed (C)", WC)]:
    x = Lsun / W1
    rho = x * rho_DM_mean
    R_h = np.sqrt(3 * c**2 / (8 * np.pi * G * rho))   # radius at which a uniform ball of this density is inside its own horizon
    print(f"{label}: x = {x:.3e}, rho = {rho:.3e} kg/m^3 ({rho/1.783e-27/1e6:.3e} GeV/cm^3), self-horizon radius = {R_h:.3e} m")
r_near = hbarSI * c / (m_eV * eVJ)
lam_dB = 2 * np.pi * hbarSI / (m_eV * eVJ / c**2 * v * c)
print(f"near-zone radius c/w = hbar c/m = {r_near:.3e} m; ULDM de Broglie wavelength = {lam_dB:.3e} m")

# --- E. kinematics ---
print("\n=== E. kinematics of an outgoing wave ===")
xs = sp.symbols('x', positive=True)
for l in (2, 3):
    hl = sp.expand_func(sp.jn(l, xs) + sp.I * sp.yn(l, xs))
    poly = sp.simplify(sp.expand((hl * sp.exp(-sp.I * xs)).rewrite(sp.exp)))
    has_exp = poly.has(sp.exp) or poly.has(sp.sin) or poly.has(sp.cos)
    print(f"l={l}: h_l^(1)(x) e^(-ix) = {poly}  -> contains e^(+-ix)? {has_exp} (no incoming e^(-ix) part)")
# Head-on window for the resonance (pairs within mv of rest), and far-zone angular spread
crit = 2 * np.arccos(1 / (1 + v**2 / 2))
print(f"resonance needs pi - theta <= {crit:.4e} rad (2v = {2*v:.1e})")
# Scalar toy: Q = 0 weight of the 2w component of h^2 between r0 = 1/k and R = 1/(2 m v) ~ 1/(2 k v)
k = 1.0
R = 1 / (2 * k * v)
r = np.linspace(1 / k, R, 4_000_001)
dr = r[1] - r[0]
ret = np.sum(np.exp(2j * k * r)) * dr * 4 * np.pi        # int d^3x e^{2ikr}/r^2  (outgoing h = e^{ikr}/r)
std = np.sum(np.cos(k * r)**2) * dr * 4 * np.pi         # standing h = cos(kr)/r  (2w part of h^2)
print(f"toy: |S_ret(Q=0)| = {abs(ret):.4e} /k ; |S_std(Q=0)| = {abs(std):.4e} /k ; rate ratio std/ret = {abs(std/ret)**2:.3e}; guaranteed minimum (|S_ret| <= 4 pi/k) = {(abs(std)/(4*np.pi))**2:.3e} ~ 1/(16 v^2) = {1/(16*v**2):.3e}")
r2 = np.linspace(1 / k, 2 * R, 8_000_001)
ret2 = np.sum(np.exp(2j * k * r2)) * (r2[1] - r2[0]) * 4 * np.pi
print(f"convergence: doubling R changes |S_ret| from {abs(ret):.4e} to {abs(ret2):.4e} (bounded); S_std grows ~R")
