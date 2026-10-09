"""Dialectician lens: where do the Einstein-Dirac-Maxwell (EDM) static throats sit
against the Ford-Roman single-scale throat bound, and what fermion mass do they need?

Inputs (dossier):
  Kain 2023 Table I static EDM throats: R0/l_P = 75.28 to 498.4 at mu_bar = 0.2,
      e_bar/sqrt(4 pi) = 0.03 (Q-18).  mu_bar is the fermion mass in Planck units (D-11).
  Ford-Roman single-scale bound r0 <~ l_P / f^2 or l_P/(2 f^2), f ~ 0.01 (Q-20).
  Electron mass in Planck units: m_e / m_P (CODATA m_e = 9.1093837e-31 kg,
      m_P = 2.176434e-8 kg).
Outputs in SI (metres) and Planck units.
"""
l_P = 1.616255e-35      # m (CODATA 2018)
m_P = 2.176434e-8       # kg
m_e = 9.1093837015e-31  # kg
alpha = 7.2973525693e-3

for R in (75.28, 498.4):
    print(f"Kain static EDM throat R0 = {R} l_P = {R*l_P:.3e} m")
f = 0.01
print(f"Ford-Roman single-scale bound (f = {f}): l_P/f^2 = {1/f**2:.3g} l_P = {l_P/f**2:.3e} m ; "
      f"l_P/(2f^2) = {1/(2*f**2):.3g} l_P = {l_P/(2*f**2):.3e} m")
print(f"Ratio largest Kain throat / Ford-Roman l_P/(2f^2): {498.4/(1/(2*f**2)):.3g}")
print(f"EDM fermion mass mu_bar = 0.2 m_P = {0.2*m_P:.3e} kg ; electron mu_bar = m_e/m_P = {m_e/m_P:.3e}")
print(f"ratio required fermion mass / electron mass = {0.2*m_P/m_e:.3e}")
print(f"EDM coupling e_bar/sqrt(4pi) = 0.03 vs electron sqrt(alpha) = {alpha**0.5:.4f} "
      f"(e/sqrt(4pi) in Gaussian-natural units)")
print("Note: with one fermion, G mu^2/(hbar c) = mu_bar^2 is the gravitational strength; "
      f"electron value = {(m_e/m_P)**2:.3e}, so no electron-scale member of the Kain family exists "
      "unless that dimensionless parameter is irrelevant (it is not, for one particle).")
