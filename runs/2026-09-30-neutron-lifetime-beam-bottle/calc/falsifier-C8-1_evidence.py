"""Falsifier C8-1 (evidence angle): size of the common proton-side cause that C8's R-strong needs,
set against the proton-side items of the two experiments' own published budgets, plus the
updated aCORN (Wietfeldt 2024) lambda.
Units: lifetimes in s (SI); lambda, a dimensionless.
Sources (numbers as quoted):
  aSPECT 2020 (arXiv:1908.04785) Table VII: backscattering/threshold shifts a by -0.1 %;
     "the listed systematic effects may add up to a relative shift in a of delta a_sys/a ~ 1 %".
  aSPECT 2024 (D-42): a = -0.10402(82), lambda = -1.2668(27).
  PERKEO III (D-40): lambda = -1.27641(45)(33).
  aCORN 2024 (Wietfeldt, arXiv:2306.15042 abstract): lambda = -1.2712 +- 0.0061.
  aCORN 2021 (Hassan, D-41): lambda = -1.2796 +- 0.0062.
  BL1 (D-20, D-21): 887.7 s; proton backscatter calc unc 0.4 s; Si scattering unc 0.5 s;
     trap nonlinearity correction -5.3 s (unc 0.8 s).
  Caylor 2025 (D-17): ~0.3 % proton-loss probability from H2 charge exchange (large uncertainty).
  Gap BL1 vs UCNtau (candidates.md header, M-EXAMINER-04): 9.88 s, 1.113 %.
  R-strong a deficit (M-DIALECTICIAN-05): 2.67 %.
"""
from math import sqrt

def z(x1, s1, x2, s2):
    return (x1 - x2) / sqrt(s1**2 + s2**2)

pk3, spk3 = -1.27641, sqrt(0.00045**2 + 0.00033**2)
asp, sasp = -1.2668, 0.0027
acn24, sacn24 = -1.2712, 0.0061
acn21, sacn21 = -1.2796, 0.0062

print("PERKEO III combined sigma = %.5f" % spk3)
print("aCORN2021 vs PERKEO III z = %+.2f ; vs aSPECT2024 z = %+.2f" % (z(acn21, sacn21, pk3, spk3), z(acn21, sacn21, asp, sasp)))
print("aCORN2024 vs PERKEO III z = %+.2f ; vs aSPECT2024 z = %+.2f" % (z(acn24, sacn24, pk3, spk3), z(acn24, sacn24, asp, sasp)))

# Required R-strong biases vs proton-side budget items
need_a = 2.67   # percent, a deficit aSPECT
asp_bs = 0.1    # percent, aSPECT Table VII backscattering/threshold shift
asp_all = 1.0   # percent, aSPECT all listed systematic corrections added up
print("aSPECT: needed |a| bias %.2f %% = %.0f x backscatter/threshold item (%.1f %%), = %.1f x sum of ALL listed corrections (%.1f %%)"
      % (need_a, need_a / asp_bs, asp_bs, need_a / asp_all, asp_all))

gap_s = 9.88
tau = 887.7
for name, unc in [("proton backscatter calc unc", 0.4), ("Si scattering unc", 0.5), ("trap nonlinearity unc", 0.8)]:
    print("BL1: needed shift %.2f s = %.1f x '%s' (%.1f s)" % (gap_s, gap_s / unc, name, unc))
print("BL1: needed shift %.2f s = %.1f x the full trap-nonlinearity CORRECTION (5.3 s)" % (gap_s, gap_s / 5.3))
cx = 0.003 * tau
print("Caylor 2025 H2 charge exchange ~0.3%% -> %.2f s = %.0f %% of the gap" % (cx, 100 * cx / gap_s))

# tau-equivalent tolerance of the 'one-to-one' match: aSPECT tau_beta 889.58 +- 3.20 s vs BL1 887.7 +- 2.3 s
asp_tau, s_asp_tau = 889.58, 3.20
bl1, sbl1 = 887.7, sqrt(1.2**2 + 1.9**2)
print("aSPECT tau_beta vs BL1: z = %+.2f ; any aSPECT tau_beta in [%.1f, %.1f] s matches BL1 within 1 sigma"
      % (z(asp_tau, s_asp_tau, bl1, sbl1), bl1 - sqrt(s_asp_tau**2 + sbl1**2), bl1 + sqrt(s_asp_tau**2 + sbl1**2)))
print("i.e. an aSPECT offset from the A route (878.71 s) of anything from %.1f to %.1f s would 'map one-to-one'"
      % (bl1 - sqrt(s_asp_tau**2 + sbl1**2) - 878.71, bl1 + sqrt(s_asp_tau**2 + sbl1**2) - 878.71))
