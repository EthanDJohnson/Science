"""
Falsifier C5-2 (bounds): nuclear stability of Veselsky's n -> X+ e- nubar, X+ -> 2A0 e+ chain.

Natural units, energies in MeV; rates converted to s^-1 with hbar = 6.582119569e-22 MeV s.

Logic
-----
1. Kinematic window for on-shell X+: free-neutron decay needs m_X < m_n - m_e;
   stability of 9Be against 9Be -> 8Be + X+ e- nubar (on shell) needs m_X > m_n - S_n(9Be) - m_e.
2. But the full chain ends in 2A0 + e+ e- nubar with 2 m_D = 740-920 MeV (Veselsky's m_D = 370-460 MeV),
   far below m_n - S_n for every stable nucleus.  Bound neutrons can therefore decay through an
   OFF-SHELL X+.  Rate (narrow-width / Breit-Wigner tail, per bound neutron with separation energy S):
     Gamma_nuc = (Gamma_0 / f(Q0)) * Int dM f(m_n - S - M - m_e) * rho(M),
     rho(M) dM = (1/pi) * 2 M^2 Gamma_X(M) / (M^2 - m_X^2)^2 dM,
   Gamma_X(M) = Gamma_X * Phi(M)/Phi(m_X)  [variant A: constant |amplitude|^2, 3-body phase space]
   Gamma_X(M) = Gamma_X * (Q_X(M)/Q_X(m_X))^5  [variant B: steeper, conservative]
   f(Q) = Int_0^Q p E (Q - T)^2 dT  (beta phase space, no Fermi function).
   Gamma_0 = Br * Gamma_n is the free-neutron exotic rate the candidate needs.
3. BL1 needs the X+ gone before its ~10 ms trapping period ends (else it is trapped like a proton and
   counted), so Gamma_X >= hbar / 10 ms (generous).  That fixes a MINIMUM bound-neutron decay rate.
4. Compare with (a) Earth's surface heat flow ~47 TW and (b) nucleon-lifetime limits ~1e29 yr and beyond.
"""
import numpy as np
from scipy import integrate

hbar = 6.582119569e-22  # MeV s
m_n = 939.56542   # MeV
m_p = 938.27209   # MeV
m_e = 0.51099895  # MeV
yr = 3.15576e7    # s

tau_n = 877.82    # s (UCNtau, dossier)
Br = 0.01113      # needed exotic branch (M-CONSTRAINTS-03)
Gamma0 = Br / tau_n
print(f"Inputs: tau_n = {tau_n} s, Br = {Br}, Gamma_0 = Br/tau_n = {Gamma0:.4e} s^-1")

# neutron separation energies (MeV), AME2020 rounded
S = {"2H": 2.2246, "9Be": 1.6654, "12C": 18.722, "13C": 4.9463, "16O": 15.6637,
     "17O": 4.1431, "24Mg": 16.531, "28Si": 17.180, "27Al": 13.058, "56Fe": 11.197}

mX_lo = m_n - S["9Be"] - m_e
mX_hi = m_n - m_e
print(f"On-shell X+ window: {mX_lo:.3f} MeV < m_X < {mX_hi:.3f} MeV (9Be stability / free decay)")

def f_beta(Q):
    if Q <= 0:
        return 0.0
    g = lambda T: np.sqrt(T * (T + 2 * m_e)) * (T + m_e) * (Q - T) ** 2
    return integrate.quad(g, 0, Q, limit=200)[0]

def dalitz_area(M, m1, m2, m3):
    """Area of the Dalitz plot (m12^2, m23^2) for M -> 1 2 3; Gamma ~ area / M^3 for const |amp|^2."""
    if M <= m1 + m2 + m3:
        return 0.0
    def span(m12sq):
        m12 = np.sqrt(m12sq)
        E2 = (m12sq - m1**2 + m2**2) / (2 * m12)
        E3 = (M**2 - m12sq - m3**2) / (2 * m12)
        p2 = np.sqrt(max(E2**2 - m2**2, 0)); p3 = np.sqrt(max(E3**2 - m3**2, 0))
        return 4 * p2 * p3
    lo, hi = (m1 + m2) ** 2, (M - m3) ** 2
    return integrate.quad(span, lo, hi, limit=200)[0]

def Phi(M, mD):
    return dalitz_area(M, mD, mD, m_e) / M**3

def coeff(Ssep, mX, mD, variant):
    """Gamma_nuc / (Gamma_0 * Gamma_X[MeV]) in MeV^-1."""
    Mmax = m_n - Ssep - m_e
    Mmin = 2 * mD + m_e
    if Mmax <= Mmin:
        return 0.0
    fQ0 = f_beta(mX_hi - mX)  # Q0 = m_n - m_X - m_e
    QXm = mX - Mmin
    PhiX = Phi(mX, mD)
    def integrand(M):
        if variant == "A":
            ratio = Phi(M, mD) / PhiX
        else:
            ratio = ((M - Mmin) / QXm) ** 5
        return f_beta(Mmax - M) * (2 * M**2 / np.pi) * ratio / (M**2 - mX**2) ** 2
    pts = np.linspace(Mmin, Mmax, 9)[1:-1]
    val = integrate.quad(integrand, Mmin, Mmax, points=list(pts), limit=400)[0]
    return val / fQ0

tauX_max = 0.010  # s, BL1 trapping period ~10 ms (Nico 2005)
GX_min = hbar / tauX_max
print(f"BL1 requirement: tau_X <= {tauX_max*1e3:.0f} ms  ->  Gamma_X >= {GX_min:.3e} MeV")
print()

# Earth heat-flow comparison: 1 neutron per nucleus, mean nuclear mass 40 u, >= 1.022 MeV to heat per decay
M_earth = 5.972e24; u = 1.66054e-27
N_nuc = M_earth / (40 * u)
Q_heat = 47e12  # W, Earth surface heat flow
E_dep = 1.022 * 1.602176634e-13  # J (e+ annihilation only)
rate_max_heat = Q_heat / E_dep / N_nuc
print(f"Earth: N_nuclei ~ {N_nuc:.2e}; heat flow {Q_heat:.1e} W; E_dep >= 1.022 MeV")
print(f"  -> max per-nucleus decay rate from heat flow = {rate_max_heat:.2e} s^-1 "
      f"(partial lifetime >= {1/rate_max_heat/yr:.2e} yr)")
print()

mX_list = [mX_lo + 0.05, 0.5 * (mX_lo + mX_hi), m_p, mX_hi - 0.2]
mD_list = [370.0, 400.0, 460.0]
earth_nuclei = ["16O", "28Si", "24Mg", "56Fe"]
worst_ratio = np.inf
print("Per-bound-neutron rate at Gamma_X = hbar/10 ms  (Gamma_nuc in s^-1; partial lifetime in yr)")
for variant in ["A", "B"]:
    for mD in mD_list:
        for mX in mX_list:
            row = []
            earth_rates = []
            for nuc in ["2H", "9Be", "13C", "17O", "16O", "28Si", "24Mg", "56Fe"]:
                c = coeff(S[nuc], mX, mD, variant)
                G = Gamma0 * c * GX_min
                row.append(f"{nuc}:{G:.1e}")
                if nuc in earth_nuclei:
                    earth_rates.append(G)
            emin = min(earth_rates)
            ratio = emin / rate_max_heat
            worst_ratio = min(worst_ratio, ratio)
            print(f"[{variant}] m_D={mD:.0f} m_X={mX:.3f} Q0={mX_hi-mX:.3f} MeV | " + " ".join(row))
            print(f"      min over Earth nuclei (O,Si,Mg,Fe) = {emin:.2e} s^-1 -> tau = {1/emin/yr:.2e} yr;"
                  f" / heat-flow max = {ratio:.1e}")
print()
print(f"Smallest (Earth-nucleus rate)/(heat-flow ceiling) over all cases = {worst_ratio:.2e}")
print("Nucleon-decay limits for comparison: > ~1e29 yr (invisible modes) and > 1e30-1e34 yr (visible modes).")

# Required Gamma_X to satisfy a 1e29 yr bound in 16O, and the implied X lifetime
print()
print("Gamma_X (and tau_X) needed so that 16O neutrons live > 1e29 yr, and > heat-flow bound:")
for mD in mD_list:
    for mX in [0.5 * (mX_lo + mX_hi)]:
        c = coeff(S["16O"], mX, mD, "B")
        GX_1e29 = (1 / (1e29 * yr)) / (Gamma0 * c)
        GX_heat = rate_max_heat / (Gamma0 * c)
        print(f"  m_D={mD:.0f}, m_X={mX:.3f}: Gamma_X < {GX_1e29:.2e} MeV (tau_X > {hbar/GX_1e29:.2e} s);"
              f" heat-flow: tau_X > {hbar/GX_heat:.2e} s  [variant B]")

# ---------------------------------------------------------------------------------------------
# Sanity check: free neutron (S = 0) with the full Breit-Wigner (width term kept) must return
# Gamma_nuc ~= Gamma_0 (the on-shell narrow-width limit), i.e. normalisation of rho(M) ~ 1.
print()
print("Sanity check (free neutron, full Breit-Wigner, test width Gamma_X = 1e-4 MeV):")
def coeff_fullBW(Ssep, mX, mD, GX):
    Mmax = m_n - Ssep - m_e; Mmin = 2 * mD + m_e
    fQ0 = f_beta(mX_hi - mX); PhiX = Phi(mX, mD)
    def integrand(M):
        GXM = GX * Phi(M, mD) / PhiX
        return f_beta(Mmax - M) * (2 * M**2 / np.pi) * GXM / ((M**2 - mX**2) ** 2 + mX**2 * GX**2)
    pts = sorted(set([mX - 10 * GX, mX, mX + 10 * GX, Mmax - 1.0]))
    pts = [p for p in pts if Mmin < p < Mmax]
    return integrate.quad(integrand, Mmin, Mmax, points=pts, limit=2000)[0] / fQ0
for GXt in [1e-4, 1e-8]:
    for mD in [400.0, 460.0]:
        r = coeff_fullBW(0.0, 938.222, mD, GXt)
        tail = coeff(0.0, 938.222, mD, "A") if False else None
        print(f"  Gamma_X={GXt:.0e} MeV, m_D={mD:.0f}: Gamma(free n -> chain)/Gamma_0 = {r:.4f}"
              "  (expect 1 + off-shell tail proportional to Gamma_X)")

# ---------------------------------------------------------------------------------------------
# Borexino-type check for the least favourable mass m_D = 460 MeV (12C channel closed; 13C open)
print()
print("Liquid-scintillator check, m_D = 460 MeV, 13C valence neutron (S_n = 4.9463 MeV):")
m_scint = 100e6  # g (100 t)
fracC = 108.0 / 120.0  # carbon mass fraction in pseudocumene C9H12
N_C = m_scint * fracC / 12.011 * 6.02214076e23
N_13C = N_C * 0.0107
print(f"  100 t pseudocumene: N_C = {N_C:.2e}, N_13C = {N_13C:.2e}")
for variant in ["A", "B"]:
    for mX in mX_list:
        c = coeff(S["13C"], mX, 460.0, variant)
        G = Gamma0 * c * GX_min
        per_day = G * N_13C * 86400
        print(f"  [{variant}] m_X={mX:.3f}: Gamma(13C) = {G:.2e} s^-1 -> {per_day:.2e} events/day/100 t"
              f" (Borexino 8B rate above 3 MeV: 0.217 cpd/100 t) ratio = {per_day/0.217:.1e}")
        # tau_X needed to bring the 13C rate to <= 0.217/day/100 t, even if every event were above 3 MeV
        GX_need = (0.217 / 86400 / N_13C) / (Gamma0 * c)
        print(f"        tau_X needed for <= 0.217 cpd/100 t: > {hbar/GX_need:.2e} s")
