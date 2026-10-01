"""Falsifier C4-1 (evidence angle): compare the n->n' conversion C4 needs in the
NIST BL1 proton trap with the published SNS regeneration limits.
Units: SI for lifetimes (s) and fields (T); energies in neV; probabilities dimensionless.
Inputs (published, quoted in the verdict):
  Broussard et al. 2022 PRL 128 212503: p < 2.5e-8 (95% CL, 6.6 T peak, B4C absorber)
  Gonzalez et al. 2024 PRD 110 072022, Table II: p_tr < 3.1e-10 (4.70 T), 4.4e-10 (2.35 T),
      2.8e-10 (combined), 95% CL, Cd absorber
  |mu_n| = 60.3077 neV/T (run value D-56 / M-MECHANIST-09)
  Gap: BL1 vs UCNtau 1.113 % (M-EXAMINER-04), proton beam 887.97 s
The sqrt(p) per-passage cap assumes two alike passages (the run's unverified premise);
it is printed only as an illustration. The published exclusions rest on full
density-matrix simulations with the measured field maps, not on this premise.
"""
import math

mu_n = 60.3077  # neV/T
tau_beam = 887.97  # s
P_needed = 0.01113  # fraction of beam neutrons that must convert in trap

print("Resonance fields for the Delta m band C4 needs:")
for dm in (260.0, 278.0, 280.0, 302.0):
    print(f"  Delta m = {dm:6.1f} neV -> B_res = {dm/mu_n:5.3f} T")
for B in (4.6, 4.70, 5.0, 6.6):
    print(f"  B = {B:4.2f} T -> |mu_n| B = {mu_n*B:6.1f} neV")

print()
print(f"Needed conversion in trap P_needed = {P_needed:.4e}; naive regeneration P^2 = {P_needed**2:.3e}")
limits = {"SNS 2022, 6.6 T (B4C)": 2.5e-8,
          "SNS 2024, 4.70 T (Cd)": 3.1e-10,
          "SNS 2024, combined (Cd)": 2.8e-10}
for name, p in limits.items():
    Pcap = math.sqrt(p)
    shift = tau_beam * (1.0 / (1.0 - Pcap) - 1.0)
    print(f"{name}: p < {p:.2e}; P^2 needed / limit = {P_needed**2/p:.3e}; "
          f"per-pass cap sqrt(p) = {Pcap:.3e} ({P_needed/Pcap:.0f}x below need); "
          f"beam shift cap = {shift:.4f} s vs gap 9.88 s")

# Berezhiani's own worked example (lens-constraints_consistency): P_trap = 0.0043
print()
print(f"Berezhiani worked example P_trap = 0.0043 -> tau ratio 1.0043 vs needed 1.0113; "
      f"fraction of gap = {0.0043/P_needed:.2f}")
