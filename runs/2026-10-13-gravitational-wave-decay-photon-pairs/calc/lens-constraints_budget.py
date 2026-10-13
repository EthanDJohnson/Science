"""Constraints lens: hbar counting of eqs. 8/11/12, universal near-source caps, eq. 19 overcount,
photofission/EBL source requirements, Hawking-vs-fusion comparison, free-free absorption, ULDM kinematics.

Units: SI unless stated; B&O formulas in natural units are converted by G -> G hbar / c^5 (dimension s^2).
Inputs: B&O eq. 8, 11, 12 [D-21, D-24, F7]; GW150914 [D-27..D-30]; GW170817 / inspiral recipe [D-48];
FIRAS [D-08]; N_eff [D-32, D-33]; BBN thresholds [D-37]; plasma [D-40]; ULDM [D-26, D-50].
"""
import math
import sympy as sp
from scipy import constants as K

hbar, c, G, kB, eV = K.hbar, K.c, K.G, K.k, K.e
Msun = 1.98847e30
tP = math.sqrt(hbar * G / c**5)
EP = hbar / tP                     # J
LP = c**5 / G                      # W
tH = 13.8e9 * 3.156e7              # s
TCMB = 2.7255                      # K
print(f"Planck: t_P = {tP:.4e} s, E_P = {EP/eV:.4e} eV, L_P = c^5/G = {LP:.4e} W, t_H = {tH:.3e} s")

# ---------------------------------------------------------------- Part A
print("\n=== Part A: hbar counting of eqs. 8, 11, 12 (sympy) ===")
Gs, cs, hb, E, w, sg, kT = sp.symbols('G c hbar E omega sigma kT', positive=True)
Gnat = Gs * hb / cs**5                         # natural-units G in s^2
N = E / (hb * w)
rate = sp.simplify(3 * Gnat**2 * N**2 * w**3 * sg**2 / (25 * sp.pi))
print("  eq. 8 pair rate with N = E/(hbar w):", rate, "; d/dhbar =", sp.simplify(sp.diff(rate, hb)))
W = 2 * hb * w * rate
eq11 = 6 * Gs**2 * hb * E**2 * w**2 * sg**2 / (25 * sp.pi * cs**10)
rm = 2 * Gs * E / cs**4
ell = cs / sg
eq12 = sp.Rational(3, 50) / sp.pi * (rm / ell)**2 * hb * w**2
eq12_dossier = sp.Rational(3, 50) / sp.pi * (rm / ell)**2 * (hb * w)**2
print("  W = 2 hbar w dP/dt minus eq. 11 :", sp.simplify(W - eq11))
print("  W minus eq. 12 [(3/50pi)(r_m/l)^2 hbar w^2]:", sp.simplify(W - eq12))
print("  eq. 12 as transcribed in D-24 [(hbar w)^2] divided by W:", sp.simplify(eq12_dossier / W), "(an energy: not a power)")
Wst = sp.series(W * (1 + 2 * kT / (hb * w)), kT, sp.oo, 1)  # leading term large kT
Wst_lead = sp.simplify(W * 2 * kT / (hb * w))
print("  CMB-stimulated leading term W x 2kT/(hbar w) =", Wst_lead, "; d/dhbar =", sp.simplify(sp.diff(Wst_lead, hb)))
Npairs_burst = sp.simplify(rate / sg)
print("  pairs per burst (rate x 1/sigma) =", Npairs_burst)
Npairs_ell = sp.simplify(Npairs_burst.subs(E, sp.Symbol('x') * cs**4 * ell / (2 * Gs)))
print("  ... with r_m = x l (x = r_m/l):", Npairs_ell, " -> pairs/burst = (3/(100 pi)) x^2 (w/sigma)")

def W_gamma(E_J, w_, s_):
    return 6 * hbar * G**2 * E_J**2 * w_**2 * s_**2 / (25 * math.pi * c**10)

def stim(w_, T=TCMB):
    x = hbar * w_ / (kB * T)
    return 1 + 2 / math.expm1(x) if x < 700 else 1.0

# ---------------------------------------------------------------- Part B
print("\n=== Part B: near-source conversion fraction C = W_gamma/L_GW = (6/(25 pi)) (L/L_P) (hbar w/E_P)^2 ===")
def conv(L, w_):
    return 6 / (25 * math.pi) * (L / LP) * (hbar * w_ / EP)**2

def Lquad(Mc_sun, fgw):
    x = G * Mc_sun * Msun * math.pi * fgw / c**3
    return 32 / 5 * LP * x**(10 / 3)

# GW150914 at B&O's inputs: E = 2 Msun c^2, f = 150 Hz, t_m = 5 ms [D-27]
for Esun in (2.0, 3.0):
    E_J = Esun * Msun * c**2
    w_ = 2 * math.pi * 150
    s_ = 1 / 5e-3
    Wg = W_gamma(E_J, w_, s_)
    L = E_J * s_
    xr = 2 * G * E_J / c**4 / (c / s_)
    print(f"  GW150914 E = {Esun} Msun c^2: W_gamma = {Wg:.3e} W (D-42: 2.8e-35 / 6.3e-35 W); L = E sigma = {L:.3e} W; "
          f"C = {Wg/L:.3e} = formula {conv(L, w_):.3e}; r_m/l = {xr:.3e}; pairs per burst = {Wg/(2*hbar*w_)/s_:.3e}; "
          f"x CMB stim ({stim(w_):.3e}) = {Wg/(2*hbar*w_)/s_*stim(w_):.3e}")
cases = [("GW170817 at 100 Hz [D-48 L]", 1.8e44, 100.0),
         ("BBH M_c=28 at 50 Hz (quadrupole)", Lquad(28, 50.0), 50.0),
         ("WD binary M_c=0.3 at 6.2 mHz (ASSUMED, D-48)", Lquad(0.3, 6.2e-3), 6.2e-3),
         ("SMBH 1.8e10 Msun near ISCO, L = 1e-3 L_P", 1e-3 * LP, 4397 / 1.8e10),
         ("any merger at peak, L = 1e-3 L_P, f = 150 Hz", 1e-3 * LP, 150.0)]
for lab, L, f in cases:
    w_ = 2 * math.pi * f
    print(f"  {lab:48s}: L = {L:.3e} W, C_vac = {conv(L, w_):.3e}, C_stim(CMB today) = {conv(L, w_)*stim(w_):.3e}")
# Threshold for a photon-based bound to beat the N_eff bound on the same GW energy
rgam = (7 / 8) * (4 / 11)**(4 / 3) * 0.3
Cstar = 6e-5 / rgam
print(f"  rho_GW/rho_gamma allowed by DeltaN_eff = 0.3: {rgam:.4f}; FIRAS Delta rho/rho ~ 6e-5 -> needs C > {Cstar:.2e}")
hw_need = EP * math.sqrt(Cstar / (6 / (25 * math.pi)))  # L = L_P, unstimulated
print(f"  unstimulated, even at L = L_P: needs hbar w > {hw_need/eV:.3e} eV = {hw_need/EP:.3f} E_P (outside the EFT)")
for z in (1e3, 1e5, 3e6):
    kTz = kB * TCMB * (1 + z)
    # RJ: C = (6/25pi)(L/LP)(hw/EP)^2 * 2kT/(hw) = (12/25pi)(L/LP) hw kT / EP^2
    hw = Cstar * EP**2 / (12 / (25 * math.pi) * kTz)
    print(f"  stimulated at z = {z:.0e} (kT = {kTz/eV:.3e} eV), L = L_P: needs hbar w > {hw/eV:.3e} eV (RJ requires hbar w < kT: impossible)")

# ---------------------------------------------------------------- Part C
print("\n=== Part C: eq. 19 overcount X = sigma t_prop and energy conservation of B&O's integration ===")
eps = 0.1
for hw_eV in (1e-10, 1e-7, 1e-5, 1e-3, 1.0, 10.0, 2.2246e6, 1.98e7, 1e9, 1e10):
    w_ = hw_eV * eV / hbar
    X = eps * w_ * tH
    # maximal-luminosity source (L = 1e-3 L_P) and hoop-limited (r_m = l) source
    Cn = conv(1e-3 * LP, w_)
    # hoop: x = r_m/l = 1 -> pairs/burst = (3/(100 pi))/eps, energy fraction = pairs*2hw/E, E = c^4 l/(2G), l = c/(eps w)
    E_hoop = c**4 * (c / (eps * w_)) / (2 * G)
    Nh = 3 / (100 * math.pi) / eps
    Ch = Nh * 2 * hbar * w_ / E_hoop
    print(f"  hbar w = {hw_eV:9.3e} eV: X = sigma t_H = {X:.2e}; L=1e-3 L_P: C_near = {Cn:.2e}, B&O C x X = {Cn*X:.2e}"
          f"{'  (> 1: violates energy conservation)' if Cn*X > 1 else ''}; hoop-limited: E <= {E_hoop/(Msun*c**2):.2e} Msun c^2, "
          f"pairs/burst <= {Nh:.3f}, C <= {Ch:.2e}, B&O C x X = {Ch*X:.2e}{'  (> 1)' if Ch*X > 1 else ''}")
# depletion time at maximal luminosity vs t_H
for hw_eV in (1e3, 1e6, 1e9, 1e10):
    w_ = hw_eV * eV / hbar
    Cn = conv(1e-3 * LP, w_)
    tauh = 1 / (eps * w_ * Cn)
    print(f"  hbar w = {hw_eV:.0e} eV, L = 1e-3 L_P: B&O depletion time tau_h = 1/(sigma C) = {tauh:.3e} s = {tauh/tH:.3e} t_H")

# ---------------------------------------------------------------- Part D
print("\n=== Part D: what sources the photofission / EBL windows need; Hawking emission of the same sources ===")
for lab, hw_eV in (("EBL (B&O: w_s >~ 10 eV)", 10.0), ("D(gamma,n)p 2.2246 MeV", 2.2246e6), ("4He(gamma,p)t 19.81 MeV", 1.98139e7),
                   ("Fig. 3 top 1e10 eV", 1e10)):
    w_ = hw_eV * eV / hbar
    M = 0.136 * c**3 / (G * w_)        # ISCO GW angular frequency w = 0.136 c^3/(G M)
    tev = 5120 * math.pi * G**2 * M**3 / (hbar * c**4)
    TH = hbar * c**3 / (8 * math.pi * G * (M / 2) * kB)   # each component of mass M/2
    print(f"  {lab:28s}: total mass at ISCO M = {M:.3e} kg = {M/Msun:.3e} Msun; component Hawking kT = {kB*TH/eV:.3e} eV; "
          f"evaporation time (mass M/2) = {tev/8/tH:.3e} t_H")
# W_H / W_gamma for a GW150914-like merger scaled to any mass (ratio is mass independent)
M = 65 * Msun
Eb = 3.0 / 65 * M * c**2
w_ = 2 * math.pi * 150
s_ = 1 / 5e-3
Wg = W_gamma(Eb, w_, s_)
WH_page = hbar * c**6 / (15360 * math.pi * G**2 * M**2)   # single BH of mass M, Page-type estimate
WH_two = 2 * hbar * c**6 / (15360 * math.pi * G**2 * (M / 2)**2)
print(f"  GW150914-like: W_gamma = {Wg:.3e} W; W_H(one BH of 65 Msun) = {WH_page:.3e} W (ratio {WH_page/Wg:.0f}); "
      f"W_H(two BHs of 32.5) = {WH_two:.3e} W (ratio {WH_two/Wg:.0f}); mass independent")

# ---------------------------------------------------------------- Part E
print("\n=== Part E: free-free absorption of Hz-kHz photons (Rybicki-Lightman, RJ, cgs) ===")
e_esu, me_g, kB_cgs = 4.80320e-10, 9.10938e-28, 1.380649e-16
def alpha_ff(ne, T, nu, Z=1.0):
    gff = math.sqrt(3) / math.pi * (math.log((2 * kB_cgs * T)**1.5 / (math.pi * Z * e_esu**2 * me_g**0.5 * nu)) - 2.5 * 0.5772)
    return 0.018 * T**-1.5 * Z**2 * ne * ne * nu**-2 * gff, gff
Mpc_cm = 3.0857e24
for lab, ne, T in (("IGM mean today, all baryons", 2.2e-7, 1e4), ("IGM realistic mean", 2.75e-8, 1e4), ("hot halo gas (assumed)", 1e-4, 1e6)):
    for nu in (150.0, 1e3, 1e4):
        fp = 8980 * math.sqrt(ne)
        if nu <= fp:
            print(f"  {lab:30s} nu = {nu:7.0f} Hz: below f_pe = {fp:.1f} Hz (no propagation)")
            continue
        a, g = alpha_ff(ne, T, nu)
        print(f"  {lab:30s} n_e = {ne:.2e} cm^-3, T = {T:.0e} K, nu = {nu:7.0f} Hz: g_ff = {g:.1f}, absorption length = {1/a/Mpc_cm:.3e} Mpc")

# ---------------------------------------------------------------- Part F
print("\n=== Part F: ULDM channel kinematics (eqs. 16-18) ===")
v = 1e-3
print(f"  resonant regime (w = m(1+v^2/2)): |k1+k2| <= 2 m v requires opening angle theta >= pi - 2 arcsin(v/(1+v^2/2)) -> "
      f"within {2*math.asin(v/(1+v**2/2)):.3e} rad of head-on; solid-angle fraction ~ {(1-math.cos(2*v))/2:.2e}")
for m_eV in (1e-22, 1e-21):
    m = m_eV * eV
    w_res = m / hbar
    lam = 2 * math.pi * c / w_res
    # far-zone: s ~ 4 w (hbar c / r) (natural: 4w/r) >= 4 m^2 -> r <= hbar c w / m^2 (natural w/m^2), at w = m: r <= hbar c / m
    rmax = hbar * c / m
    print(f"  m = {m_eV:.0e} eV: resonant f = {w_res/(2*math.pi):.3e} Hz, lambda = {lam:.3e} m; production by an outgoing wave limited to r <~ hbar c/m = {rmax:.3e} m = lambda/2pi")
    # time to resolve the resonance vs time a chirp spends in the band
    sig_res = m * v**2 / (2 * hbar)
    Mtot = 4397 / (w_res / (2 * math.pi)) * Msun     # binary whose ISCO GW frequency is at resonance
    Mc = Mtot / 2**1.2
    tc = G * Mc / c**3
    f = w_res / (2 * math.pi)
    fdot = 96 / 5 * math.pi**(8 / 3) * tc**(5 / 3) * f**(11 / 3)
    t_in = f * v**2 / 2 / fdot
    print(f"    resonance width sigma = m v^2/2 = {sig_res:.3e} s^-1 (resolution time 1/sigma = {1/sig_res:.3e} s); binary at ISCO there: M = {Mtot/Msun:.2e} Msun, "
          f"df/dt = {fdot:.3e} Hz/s, time in band = {t_in:.3e} s; shortfall 1/(sigma t_in) = {1/(sig_res*t_in):.2e}")
    Lg = 1e-3 * LP
    print(f"    energy budget: W_phi (D-50) ~ 8.6e13 W x x_MW vs L_GW ~ 1e-3 L_P = {Lg:.2e} W")
