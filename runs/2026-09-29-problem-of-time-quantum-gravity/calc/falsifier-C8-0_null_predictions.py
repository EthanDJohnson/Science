"""Falsifier C8-0: check C8's quantitative prediction
"C2-C6 calculated differences are at most 1e-11 fractional ... about 1e-60 in the lab".

Part A: (E/m_P)^2 at H = 1e14 GeV with both Planck-energy conventions, and at the
         inflationary energy scale V^(1/4) ~ 1e16 GeV (natural units, GeV).
Part B: C5 vs C2 (modular flow vs relational clock flow) for a non-Gibbs 3-level state,
         hbar = 1, energies in rad/s: is the difference O(1) rather than <= 1e-11?
Part C: C6 vs C2 over 13.8 Gyr (GPP exponent), SI.
"""
import numpy as np

hbar = 1.054571817e-34   # J s
c = 2.99792458e8         # m/s
G = 6.67430e-11          # m^3 kg^-1 s^-2
GeV = 1.602176634e-10    # J

# Part A
Ep_std = np.sqrt(hbar * c**5 / G) / GeV
Ep_kiefer = np.sqrt(3 * np.pi * hbar * c**5 / (2 * G)) / GeV
print("Part A: Planck energies (GeV): standard %.4e, Kiefer %.4e" % (Ep_std, Ep_kiefer))
for E in (1e14, 1e16):
    print("  E = %.0e GeV: (E/m_P)^2 standard = %.3e, Kiefer = %.3e" %
          (E, (E / Ep_std)**2, (E / Ep_kiefer)**2))

# Part B
E = np.array([0.0, 1.0, 3.0])      # rad/s
p = np.array([0.5, 0.2, 0.3])      # non-Gibbs weights
K = -np.log(p)                      # modular Hamiltonian eigenvalues (dimensionless)
ratios = (K[1:] - K[0]) / (E[1:] - E[0])   # rad^-1 s
print("Part B: modular/energy ratios (rad^-1 s):", np.round(ratios, 4))
# modular flow e^{-iK s} vs clock flow e^{-iH t}: best single rescaling s = t/beta_fit
# compare phase of level 2 relative to level 0 after matching level 1 phase over one clock period
beta1, beta2 = ratios
t = 2 * np.pi  # s, one period of level 1 in clock time
s = t / beta1  # modular parameter chosen to match level-1 phase
phase_mismatch = (beta2 * (E[2] - E[0]) * s) - (E[2] - E[0]) * t
print("  level-2 phase mismatch after matching level 1 over t = 2pi s: %.4f rad (fractional %.3f)" %
      (phase_mismatch, abs(phase_mismatch) / ((E[2] - E[0]) * t)))

# Part C
tP = np.sqrt(hbar * G / c**5)
omega = 2 * np.pi * 429e12
T = 13.8e9 * 3.15576e7
print("Part C: GPP exponent 1.5 tP^(4/3) T^(2/3) omega^2 at 13.8 Gyr = %.3e" %
      (1.5 * tP**(4 / 3) * T**(2 / 3) * omega**2))
