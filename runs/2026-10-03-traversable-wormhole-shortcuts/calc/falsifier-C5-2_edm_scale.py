"""Falsifier C5, refuter 2 (scale): required vs achievable for Einstein-Dirac-Maxwell wormholes.
Units: SI (CODATA 2018) unless labelled 'Planck units' (G = c = hbar = 1).
Inputs (quoted, not derived here):
  - Kain 2023 static EDM throats R0/l_P = 75.28 to 498.4 (mu_bar = 0.2) [dossier Q-18].
  - BKR 2021 scaling: (r, r0) -> lam (r, r0), (mu, q, w) -> (mu, q, w)/lam, Q_N -> lam^2 Q_N (one-particle condition Q_N = 1).
  - Kain QFT 2023 (arXiv:2308.00049) eq. 64: R0/l_P = 1/sqrt(Nbar_nj), one particle per mode.
  - BKR: all solutions have q/mu < 1 (Planck units).
"""
import math

hbar = 1.054571817e-34; c = 2.99792458e8; G = 6.67430e-11
l_P = math.sqrt(hbar*G/c**3); m_P = math.sqrt(hbar*c/G); t_P = l_P/c
GeV = 1.602176634e-10; m_e = 9.1093837015e-31; alpha = 7.2973525693e-3
mPGeV = m_P*c**2/GeV
print(f"l_P = {l_P:.4e} m, m_P = {m_P:.4e} kg = {mPGeV:.4e} GeV, t_P = {t_P:.4e} s")

R_lo, R_hi = 75.28*l_P, 498.4*l_P
print(f"Kain throats: {R_lo:.3e} m to {R_hi:.3e} m")

# 1. Scaling: particle number needed for throat R if size scales as sqrt(Q_N) at fixed dimensionless shape
for R_target, label in [(1e-15, "proton radius 1e-15 m"), (1e-2, "1 cm"), (2.0, "human 2 m")]:
    lam_lo = R_target/R_hi; lam_hi = R_target/R_lo
    N_lo, N_hi = lam_lo**2, lam_hi**2
    print(f"Throat {label}: scale factor lam = {lam_lo:.2e} to {lam_hi:.2e}; particles per spinor N = lam^2 = {N_lo:.2e} to {N_hi:.2e} (log10 {math.log10(N_lo):.1f} to {math.log10(N_hi):.1f})")
    # fermion mass after scaling, mu -> mu/lam, from mu_bar = 0.2 m_P
    mu_lo = 0.2*m_P/lam_hi; mu_hi = 0.2*m_P/lam_lo
    print(f"   rescaled fermion mass mu = {mu_lo:.2e} to {mu_hi:.2e} kg ({mu_lo*c**2/GeV:.2e} to {mu_hi*c**2/GeV:.2e} GeV); q/mu unchanged (scale-invariant)")
print("Pauli: one Dirac mode (n, j, m) holds at most 1 fermion, so N >> 1 in one spinor mode is forbidden; Kain QFT eq.64 R0/l_P = 1/sqrt(Nbar) per singly-occupied mode.")

# 2. q/mu requirement (scale-invariant) vs known fermions (Gaussian, q = sqrt(alpha) e-units in Planck units)
qmu_e = math.sqrt(alpha)/(m_e/m_P)
qmu_e_HL = math.sqrt(4*math.pi*alpha)/(m_e/m_P)
print(f"electron q/mu (Planck units) = {qmu_e:.3e} (Gaussian), {qmu_e_HL:.3e} (HL); needs < 1: gap {math.log10(qmu_e):.1f} to {math.log10(qmu_e_HL):.1f} orders")
m_req_unit = math.sqrt(alpha)*mPGeV
print(f"unit-charge fermion with q/mu < 1 needs m > {m_req_unit:.3e} GeV (Gaussian), {math.sqrt(4*math.pi*alpha)*mPGeV:.3e} GeV (HL)")
E_LHC = 13.6e3  # GeV, LHC pp centre-of-mass energy
print(f"vs LHC sqrt(s) = 13.6 TeV: gap log10 = {math.log10(m_req_unit/E_LHC):.1f} orders (Gaussian)")
m_top = 172.6
print(f"vs heaviest known fermion (top, {m_top} GeV): gap log10 = {math.log10(m_req_unit/m_top):.1f} orders")

# 3. Payload vs throat
for m, L, label in [(1.0, 0.1, "1 kg (10 cm)"), (70.0, 2.0, "human 70 kg, 2 m")]:
    rs = 2*G*m/c**2
    print(f"{label}: Schwarzschild radius {rs:.3e} m = {rs/R_hi:.2e} x largest Kain throat (log10 {math.log10(rs/R_hi):.1f}); size/throat log10 = {math.log10(L/R_hi):.1f}")
    M_wh = 2*0.2*m_P  # two fermions' rest mass, order-of-magnitude wormhole mass
    print(f"   payload mass / (2 mu = {M_wh:.2e} kg) = {m/M_wh:.2e} (log10 {math.log10(m/M_wh):.1f})")

# 4. Single-quantum signal of wavelength 2*pi*R0 (lowest quantum resolving throat): E = hbar c / R0
for R in (R_lo, R_hi):
    E = hbar*c/R
    print(f"R0 = {R:.3e} m: quantum E = hbar c/R0 = {E:.3e} J = {E/(m_P*c**2):.3e} m_P c^2; E/(2 mu c^2) = {E/(0.4*m_P*c**2):.3e}; crossing time R0/c = {R/c:.2e} s")
