"""Theory facet: back-of-envelope scalings behind the early-time (sound-horizon) argument.

Units: H0 in km/s/Mpc; r_s dimensionless fractions. No unit system issues (ratios only).

(1) BAO+SN (inverse ladder) fix the product H0*r_d (beta = c/(r_d H0)); so for fixed beta,
    r_d / r_d(LCDM) = H0(LCDM) / H0(target).
(2) Pure N_eff scaling of Knox & Millea 2020 (matter scaled with radiation to hold equality):
    r_s ∝ (1+R_nu)^(-1/2), R_nu = (7/8)(4/11)^(4/3) N_eff. Check against their quoted N_eff ~ 4.2 for 7%.
(3) Equality-scale shift if omega_m raised to cut r_s: dl_EQ/l_EQ = 3 dr_s/r_s (Knox-Millea).
(4) Linear-theory estimate of the local underdensity needed: dH/H = -(1/3) f(Om) delta, f = Om^0.55.
    Linear, spherical, top-hat, rough; NOT a substitute for the N-body sample-variance results.
"""
import math

H_cmb = 67.4          # Planck 2018 LCDM, km/s/Mpc (Planck 2018 VI abstract value, quantitative facet owns)
for H_loc in (73.0, 73.04, 73.5):
    ratio = H_cmb / H_loc
    print(f"H_loc={H_loc}: H_loc/H_cmb-1 = {100*(H_loc/H_cmb-1):.2f} %, required r_d reduction at fixed H0*r_d = {100*(1-ratio):.2f} %")

# (2)
Rnu_per_Neff = (7/8) * (4/11)**(4/3)
print(f"R_nu per unit N_eff = {Rnu_per_Neff:.5f}; R_nu(3.046) = {Rnu_per_Neff*3.046:.4f}")
R0 = Rnu_per_Neff * 3.046
for red in (0.05, 0.07, 0.077, 0.09):
    # r_s ∝ (1+R)^(-1/2) -> (1+R) = (1+R0)/(1-red)^2
    R = (1 + R0) / (1 - red) ** 2 - 1
    print(f"r_s reduction {100*red:.1f} %: pure-scaling N_eff = {R/Rnu_per_Neff:.2f}  (Knox-Millea quote ~4.2 for 7 %)")
# check inverse
print("check: N_eff=4.2 gives r_s reduction", 100*(1 - math.sqrt((1+R0)/(1+Rnu_per_Neff*4.2))), "%")

# (3)
for red in (0.07, 0.077):
    print(f"omega_m route: r_s -{100*red:.1f} % -> delta_omega_m/omega_m = {100*4*red:.1f} %, l_EQ shift = {100*3*red:.1f} %")

# (4)
Om = 0.31
f = Om ** 0.55
for dH in (0.083, 0.05, 0.01):
    print(f"dH/H0 = {dH:.3f}: linear delta needed = {-3*dH/f:.2f} (f={f:.3f}); sample variance sigma(dH0)=0.31 km/s/Mpc = {100*0.31/67.4:.2f} % of H0")
print("SH0ES-Planck gap in units of Wu&Huterer 0.31 km/s/Mpc:", (73.04-67.4)/0.31)
