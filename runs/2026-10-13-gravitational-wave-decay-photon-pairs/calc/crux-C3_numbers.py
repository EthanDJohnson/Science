"""Crux C3: GW150914 pair numbers implied by the verdicts' toy ratios, and thresholds vs rivals.

Inputs (all pair numbers per GW150914 packet, B&O inputs E = 2 Msun c^2, 150 Hz, sigma = 200 rad/s):
- P_BO = eq. 8 x T_eff = 2.9e-6 pairs [M-IDEALIZER-09, M-DIALECTICIAN-01]
- whole-space ret/sym, circular (2,2) pattern, p = 2: 2.87e-3 [verdict C3-2]
- monopole ret/sym at sigma/w = 0.21, p = 2: 0.0282 [verdict C3-2]
- outgoing beyond kr ~ 2: 0.003 to 0.053 (patterns) [verdict C3-2]
- C5 linear channel: P_lin = k x 9.3e-3 pairs [M-EXAMINER-09]
- C4 band: 0.3 to 3 x P_BO [candidates.md, C3 decisive test]
"""
P_BO = 2.9e-6
r_circ = 2.87e-3
r_mono = 0.0282
r_out_lo, r_out_hi = 0.003, 0.053
P_lin_over_k = 9.3e-3

P_circ = P_BO * r_circ
P_mono = P_BO * r_mono
print(f"circular-pattern scalar-toy total: {P_circ:.2e} pairs")
print(f"monopole (harmonic-gauge h_ij proxy) at GW150914 bandwidth: {P_mono:.2e} pairs")
print(f"outgoing wave beyond kr~2: {P_BO*r_out_lo:.1e} to {P_BO*r_out_hi:.1e} pairs")
print(f"x2.25 for E = 3 Msun c^2: circular {2.25*P_circ:.2e}, monopole {2.25*P_mono:.2e} pairs")
print(f"C5 linear channel dominates C3's fusion total if k > {P_circ/P_lin_over_k:.1e} (circular) "
      f"or k > {P_mono/P_lin_over_k:.1e} (monopole proxy); vs B&O total: k > {P_BO/P_lin_over_k:.1e}")
print(f"gap between C3 upper value 0.1 and C4 lower value 0.3: factor {0.3/0.1:.0f}; "
      f"between circular toy 2.87e-3 and C4 lower 0.3: factor {0.3/r_circ:.0f}")
