"""Arithmetic cross-check of the numbers quoted in finding "fuchs-shell" (topical angle).

Only internal consistency of the quoted numbers is tested here; nothing is rebuilt.
Inputs are the finding's own quoted values plus standard constants.
"""
import math

G = 6.67430e-11
c = 299792458.0
M_J = 1.89813e27          # Jupiter mass, kg

# (b) compactness and beta_crit/C
M_ADM = 4.5114e27         # kg, rebuild value (report Key numbers)
M_PAPER = 4.49e27         # kg, published value (Le appendix / Fuchs)
R2 = 20.0
for label, M in (("rebuild", M_ADM), ("paper", M_PAPER)):
    rs = 2 * G * M / c**2
    C = rs / R2
    print(f"{label}: M={M:.4e} kg = {M / M_J:.3f} M_J, 2GM/c^2 = {rs:.4f} m, C = 2GM/(c^2 R2) = {C:.4f}")

C = 2 * G * M_ADM / c**2 / R2
beta_crit = 0.0239
print(f"beta_crit / C = {beta_crit / C:.4f}   (finding says about 0.0716)")
print(f"beta=0.02 versus beta_crit: ratio {0.02 / beta_crit:.3f} (below cap), beta=0.04 versus cap {0.04 / beta_crit:.3f} (above cap)")

# (c) margin of superluminality threshold over NEC cap
beta_super = 0.2103
print(f"beta_super / beta_crit = {beta_super / beta_crit:.2f}  (finding says at least 3.4x in the design scan; 8.8x at the reference)")
print(f"1 - lapse for lapse 0.7611 = {1 - 0.7611:.4f}  (rough scale of the forward-light-exceeds-c threshold)")

# (d) Sagnac asymmetry scaling with beta
s002 = 6.86
print(f"Sagnac asymmetry linear in beta: 0.04 -> {2 * s002:.2f} ns (finding quotes 13.72 ns); Fuchs 2024 quotes ~7.6 ns (at vwarp=0.04c per Table 1 caption)")
print(f"ratio our(0.04)/Fuchs = {2 * s002 / 7.6:.2f}  (different path/definition; not a contradiction by itself)")

# (e) stress-to-energy ratio against graphene
sigma_graphene = 130e9    # Pa, intrinsic strength (Lee et al. 2008, widely quoted)
for rho_label, rho in (("graphite 2200 kg/m^3", 2200.0), ("graphene sheet effective 1000 kg/m^3", 1000.0)):
    ratio = sigma_graphene / (rho * c**2)
    print(f"graphene strength/(rho c^2) with {rho_label}: {ratio:.3e}; 0.539 / that = {0.539 / ratio:.3e} -> {math.log10(0.539 / ratio):.2f} orders")
# NOTE: the 0.539 peak is the finding's value; we do not recompute it.
