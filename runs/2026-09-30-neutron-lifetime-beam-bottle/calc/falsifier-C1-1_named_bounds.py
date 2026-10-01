"""Falsifier C1-1 (evidence): how much of the BL1-UCNtau gap the in-situ bounds on
C1's named mechanisms leave open. Units: SI (lifetimes in s; fractions dimensionless)."""
tau_BL1 = 887.7          # s, Yue 2013 (D-20)
tau_UCN = 877.82         # s, Musedinovic 2025 (D-27)
gap = tau_BL1 - tau_UCN  # s
frac_needed = gap / tau_UCN
print(f"gap BL1 - UCNtau = {gap:.2f} s; fractional = {100*frac_needed:.3f} %")

# A1: 6Li monitor efficiency. Yue 2018 Metrologia: efficiency determined to 0.058 %.
# tau is proportional to 1/eps_0 (tau = L N_a eps_p /(N_p eps_0 v0)), so d tau/tau = d eps/eps.
eps_unc = 0.058e-2
shift_A1_1sig = eps_unc * tau_BL1
print(f"A1: 1-sigma monitor-efficiency shift = {shift_A1_1sig:.2f} s; gap/that = {gap/shift_A1_1sig:.1f} sigma-equivalents")
# add the 2013 deposit-mass-change term (0.9 s) in quadrature as the most generous budget
import math
gen = math.hypot(shift_A1_1sig, 0.9)
print(f"A1 incl. 0.9 s deposit-mass term: {gen:.2f} s; gap/that = {gap/gen:.1f}")

# A2 (H2 charge exchange): Caylor 2025 worst case < 0.5 s
for lim in (0.5,):
    print(f"A2-H2: worst-case bound {lim} s = {100*lim/gap:.1f} % of gap; gap/bound = {gap/lim:.1f}")

# A3: proton backscatter 0.4 s, Si scattering 0.5 s (Nico 2005 Table IV)
a3 = math.hypot(0.4, 0.5)
print(f"A3: backscatter+Si scattering budget (quadrature) {a3:.2f} s; gap/that = {gap/a3:.1f}")

# A4: largest single correction at 100 % error
for name, c in (("6Li absorption", 5.4), ("trap nonlinearity", 5.3)):
    print(f"A4: {name} {c} s at 100% error = {100*c/gap:.0f} % of gap")
print(f"A4: both at 100% error, same sign = {100*(5.4+5.3)/gap:.0f} % of gap")
