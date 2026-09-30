#!/usr/bin/env python3
"""Constraints lens: dark-decay kinematic window, search coverage, and the hydrogen-decay corollary.

Units: masses and energies in MeV (natural units, c = 1); lifetimes in s.
Atomic mass excesses (keV) are AME2020 values quoted FROM MEMORY by this lens; they are validated below
against three independent printed numbers: Fornal-Grinstein's 937.900 MeV (D-84), S_n(11Be) = 501.6(3) keV
(D-65), and McKeen-Pospelov-Raj's "m_chi > 938.0 MeV" (this lens, F1). m_n, m_p, m_e: CODATA 2018 (D-55).
"""
import math

ME = 0.51099895000      # MeV
MN = 939.56542052       # MeV
MP = 938.27208816       # MeV
RY = 13.605693e-6       # MeV, hydrogen binding
MH = MP + ME - RY       # MeV, hydrogen atom
# AME2020 mass excesses, keV (from memory; validated below)
DM = {"n": 8071.31806, "1H": 7288.971064, "4He": 2424.91587, "8Be": 4941.671, "9Be": 11348.453,
      "10Be": 12607.49, "11Be": 20177.17}

print("=== 1. Nuclear thresholds (atomic masses; electrons cancel) ===")
Sn9 = (DM["8Be"] + DM["n"] - DM["9Be"]) / 1e3
S2an9 = (2 * DM["4He"] + DM["n"] - DM["9Be"]) / 1e3
Sn11 = (DM["10Be"] + DM["n"] - DM["11Be"]) / 1e3
lo_FG = MN - Sn9
lo_3b = MN - S2an9
print(f"  S_n(9Be -> 8Be + n)      = {Sn9*1e3:.2f} keV -> m_chi > m_n - S_n = {lo_FG:.3f} MeV  (F-G print 937.900 MeV: check {abs(lo_FG-937.900)<0.002})")
print(f"  S(9Be -> 2 alpha + n)    = {S2an9*1e3:.2f} keV -> m_chi > {lo_3b:.3f} MeV  (McKeen et al. print '938.0 MeV': check {abs(lo_3b-938.0)<0.05})")
print(f"  S_n(11Be -> 10Be + n)    = {Sn11*1e3:.2f} keV (D-65 prints 501.6(3) keV: check {abs(Sn11*1e3-501.6)<0.5})")
print(f"  11Be -> 10Be + chi open for m_chi < {MN-Sn11:.3f} MeV: covers the whole window -> 11Be ceiling B_X < 2.0e-4 [D-65] applies")
print(f"  m_H = m_p + m_e - 13.6 eV = {MH:.6f} MeV; p stability needs m_chi > m_p - m_e = {MP-ME:.3f} MeV (weaker than 9Be)")

print("\n=== 2. Windows (m_n > M_f > 9Be bound; chi stable against chi -> p e nu if m_chi < m_p + m_e) ===")
up_stab = MP + ME
for lab, lo in (("F-G printed (9Be->8Be+n)", lo_FG), ("three-body (9Be->2a+chi)", lo_3b)):
    # n -> chi gamma, chi = DM
    Eg = lambda m: (MN**2 - m**2) / (2 * MN)
    print(f"  [{lab}] lower bound {lo:.3f} MeV")
    print(f"    n->chi gamma (chi stable): {lo:.3f} < m_chi < {up_stab:.3f} MeV; E_gamma in ({Eg(up_stab):.3f}, {Eg(lo):.3f}) MeV")
    up_ee = MN - 2 * ME
    Tmax = MN - lo - 2 * ME
    print(f"    n->chi e+e-: {lo:.3f} < m_chi < {up_ee:.3f} MeV (range {1e3*(up_ee-lo):.0f} keV); pair kinetic energy "
          f"T_ee <= {1e3*Tmax:.0f} keV (T_ee ~ m_n - m_chi - 2m_e, chi recoil neglected)")
    # PERKEO II excluded 32-644 keV at 90% CL (D-61): unexcluded T_ee < 32 keV <-> m_chi > m_n - 2 m_e - 0.032
    m_open_lo = MN - 2 * ME - 0.032
    frac = (up_ee - m_open_lo) / (up_ee - lo)
    print(f"    unexcluded e+e- window (T_ee < 32 keV): {m_open_lo:.3f} < m_chi < {up_ee:.3f} MeV = {frac*100:.1f}% of the chi mass range")
    print(f"    n->chi phi: {lo:.3f} < m_chi + m_phi < {MN:.3f} MeV (width {1e3*(MN-lo):.0f} keV); no visible particle")

print("\n=== 3. Hydrogen decay H -> chi nu in the pure mixing model (n -> chi gamma) ===")
# Fornal-Grinstein eq.(7): dGamma = g_n^2 e^2/(8 pi) (1 - x^2)^3 m_n theta^2, theta = eps/(m_n - m_chi)
# McKeen-Pospelov-Raj eq.(3): tau_H = 1e29 s (1e-10/theta)^2 (m_e/Q)^2, Q = m_H - m_chi; bound tau_H >~ 1e29 s
GN = -3.82608545      # neutron g-factor (CODATA 2018, from memory)
ALPHA = 7.2973525693e-3
HBAR = 6.582119569e-22   # MeV s
e2 = 4 * math.pi * ALPHA
for tau_tot, tau_beta in ((877.82, 887.7),):
    Gam_n = HBAR / tau_tot
    dG = Gam_n * (1 - tau_tot / tau_beta)
    print(f"  Gamma_n = {Gam_n:.4e} MeV; needed dark rate = {dG:.4e} MeV (Br = {100*(1-tau_tot/tau_beta):.3f}%)")
    for m in (lo_3b, 938.2, 938.4, 938.6, 938.7):
        x = m / MN
        coef = GN**2 * e2 / (8 * math.pi) * (1 - x**2) ** 3 * MN
        theta = math.sqrt(dG / coef)
        Q = MH - m
        tauH = 1e29 * (1e-10 / theta) ** 2 * (ME / Q) ** 2
        print(f"    m_chi = {m:.3f} MeV: E_gamma = {(MN**2-m**2)/(2*MN):.3f} MeV, theta needed = {theta:.3e}, Q = {Q:.3f} MeV, "
              f"tau_H = {tauH:.2e} s (bound ~1e29 s: {'VIOLATES' if tauH < 1e29 else 'allowed'})")
print("  (Applies only to single-chi mixing with m_chi < m_H; the n->chi gamma channel is excluded independently by LANL [D-85].)")
