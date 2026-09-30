"""Falsifier C5-1 (evidence angle): nuclear/nucleon-stability test of the Veselsky X+ branch.

Units: natural units, energies/masses in MeV; times in s and yr; hbar = 6.582119569e-22 MeV s.

Scenario (arXiv:2507.17340): n -> X+ e- nubar (Br ~ 1.1 %), then X+ -> 2 A0 + e+ "immediately",
with the preprint's favoured m_A (its 'm_D') = 370-400 MeV (range scanned 300-460 MeV).

Part A: Fornal-Grinstein kinematic conditions (PRL 120, 191801, Eq. 2): the minimal final state f of the
exotic neutron decay must satisfy 937.900 MeV < M_f < 939.565 MeV (9Be stability), and M_f > m_p - m_e
(proton decay via p -> n* e+ nu).  Here f = 2A0 + e+ + e- + nubar, M_f = 2 m_A + 2 m_e.

Part B: if M_f < 937.9 MeV, a bound neutron (130Te, S_n ~ 8.4 MeV) can decay through an OFF-SHELL X+*:
  Gamma_bound / Gamma_1 = (1/pi) Int dm* [f(Q_eff)/f(Q_0)] * 2 m*^2 Gamma_X(m*) / (m*^2 - m_X^2)^2
where Gamma_1 = free partial rate of n -> X e nubar, f = Fermi phase-space integral (no Coulomb),
Q_eff = m_n - S_n - m_e - m* (e-/nubar energy available), Gamma_X(m*) = Gamma_X (Q*/Q_X)^nX with
Q* = m* - 2 m_A - m_e.  Compare with the mode-independent 130Te nucleon lifetime limit 1.6e25 yr
(Evans & Steinberg, Science 197, 989 (1977)).
"""
import numpy as np

hbar = 6.582119569e-22  # MeV s
yr = 3.15576e7          # s
m_n, m_p, m_e = 939.56542, 938.27209, 0.51099895

# ---------------- Part A ----------------
print("PART A: Fornal-Grinstein conditions applied to f = 2A0 + e+ + e- + nubar")
for mA in [370.0, 400.0, 460.0]:
    Mf = 2 * mA + 2 * m_e
    print(f"  m_A = {mA:6.1f} MeV: M_f = {Mf:8.3f} MeV; 9Be condition (M_f > 937.900) violated by {937.900 - Mf:7.3f} MeV;"
          f" proton-decay condition (M_f > m_p - m_e = {m_p - m_e:.3f}) violated by {m_p - m_e - Mf:7.3f} MeV")
mA_lo = (937.900 - 2 * m_e) / 2
mA_hi_nXe = None
# X+ must be produced on shell in free-neutron decay: m_X < m_n - m_e; and X+ -> 2A0 e+ needs m_X > 2 m_A + m_e
mA_hi = (m_n - m_e - m_e) / 2
print(f"  Window allowed by 9Be stability AND on-shell X+ chain: {mA_lo:.3f} MeV < m_A < {mA_hi:.3f} MeV "
      f"(width {mA_hi - mA_lo:.3f} MeV); preprint's scanned range tops out at 460 MeV -> below window by {mA_lo - 460:.2f} MeV")
print(f"  In that window the total kinetic energy shared by e-, e+, nubar and A0s is < m_n - 937.900 = {m_n - 937.900:.3f} MeV,"
      " i.e. the positron is NOT 'energetic' (MeV scale, the same class as n -> chi e+e- searched by UCNA/PERKEO II)")

# ---------------- Part B ----------------
def fermi_f(E0):
    """Phase-space integral Int_{m_e}^{E0} p E (E0-E)^2 dE (E0 = total e- energy endpoint, MeV); no Coulomb."""
    if E0 <= m_e:
        return 0.0
    E = np.linspace(m_e, E0, 4001)
    p = np.sqrt(np.maximum(E**2 - m_e**2, 0))
    return np.trapezoid(p * E * (E0 - E) ** 2, E)

Br = 0.0114
tau_n = 877.8  # s
Gamma1 = Br / tau_n  # s^-1, free partial rate required
print(f"\nPART B: off-shell X+* decays of bound neutrons in 130Te; Gamma_1 = {Gamma1:.3e} s^-1 (Br = {Br}, tau = {tau_n} s)")
S_n = 8.4  # MeV, 130Te neutron separation energy (approximate; result insensitive at the order-of-magnitude level)
tauN_lim_yr = 1.6e25  # Evans & Steinberg, mode independent, per nucleon
Gb_max = 1 / (tauN_lim_yr * yr)
print(f"  mode-independent limit tau_N > {tauN_lim_yr:.1e} yr -> Gamma_bound < {Gb_max:.3e} s^-1 per neutron")

tauX_BL1 = 1e-3  # s: X+ must decay before being trapped and counted as a proton (assumption: NIST trap ~10 ms)
for mX in [937.6, m_p, 938.9]:
    Q0_E0 = m_n - mX  # total electron-energy endpoint in free decay, MeV (E0 includes m_e)
    f0 = fermi_f(Q0_E0)
    for mA in [370.0, 400.0, 460.0]:
        QX = mX - 2 * mA - m_e
        for Qcut, nX in [(1.0, 4.0), (10.0, 3.0), (1e9, 2.5)]:
            mstar_max = m_n - S_n  # e- endpoint E0 = mstar_max - m*  (total energy)
            lo = max(2 * mA + m_e + 1e-3, mstar_max - m_e - Qcut)
            ms = np.linspace(lo, mstar_max - m_e - 1e-4, 6000)
            vals = []
            for m in ms:
                E0 = mstar_max - m
                ratio_f = fermi_f(E0) / f0
                Qs = m - 2 * mA - m_e
                gX = (Qs / QX) ** nX
                vals.append(ratio_f * 2 * m * m * gX / (m * m - mX * mX) ** 2)
            C = np.trapezoid(np.array(vals), ms) / np.pi  # MeV^-1 ; Gamma_bound = Gamma1 * C * Gamma_X
            GX_max = Gb_max / (Gamma1 * C)  # MeV
            tauX_min = hbar / GX_max
            tauX_s = hbar / (hbar / tauX_BL1)
            Gb_at_BL1 = Gamma1 * C * (hbar / tauX_BL1)
            tauN_pred_yr = 1 / Gb_at_BL1 / yr
            print(f"  m_X={mX:8.3f} m_A={mA:5.1f} Qcut={min(Qcut, 999):6.1f} nX={nX}: C={C:.3e}/MeV; "
                  f"tau_X(max for BL1)={tauX_BL1:.0e} s -> tau_N={tauN_pred_yr:.2e} yr; "
                  f"130Te limit needs tau_X > {tauX_min:.2e} s (factor {tauX_min / tauX_BL1:.1e} over BL1 max)")
print("  Note: interpretation: every row with tau_N(pred) << 1.6e25 yr means the preprint's parameters are excluded"
      " unless tau_X >> 1 ms, in which case X+ survives to the proton detector and C5's proton deficit vanishes.")

# ---------------- Part C ----------------
print("\nPART C: maximum X+ recoil kinetic energy in free n -> X+ e- nubar (two-body limit, nubar at rest)")
for mX in [937.4, 937.6, m_p, 938.9]:
    Tmax = ((m_n - mX) ** 2 - m_e ** 2) / (2 * m_n) * 1e6  # eV
    print(f"  m_X = {mX:8.3f} MeV: T_X,max = {Tmax:7.1f} eV  (a proton-like recoil; far too little to leave a TPC track)")
