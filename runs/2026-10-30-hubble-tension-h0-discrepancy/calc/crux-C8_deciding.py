"""Crux C8: precision and outcome windows for the deciding observation.

Units: H0 in km/s/Mpc (astronomical, not SI); sigma is Gaussian-equivalent.
Inputs (dossier IDs): SH0ES 73.49 +- 0.93 [D-20]; CMB-SPA 67.19 +- 0.38 [D-44];
BAO+BBN 68.50 +- 0.58 [D-45]; SPT+ACT 66.59 +- 0.46 [D-43];
non-SH0ES local mean 71.692 +- 1.141 [M-EXAMINER-03; verdicts C8-0, C8-2];
TDCOSMO-2026 71.1 +2.4/-2.3, 11 lenses, 3.3% [D-31].
"""
import math

SH0ES, s_SH0ES = 73.49, 0.93
SPA, s_SPA = 67.19, 0.38
BBN, s_BBN = 68.50, 0.58
SPTACT, s_SPTACT = 66.59, 0.46
REST, s_REST = 71.692, 1.141


def z(a, sa, b, sb):
    return abs(a - b) / math.hypot(sa, sb)


print("[1] current state")
print(f"  rest vs SH0ES  z = {z(REST, s_REST, SH0ES, s_SH0ES):.2f}")
print(f"  rest vs SPA    z = {z(REST, s_REST, SPA, s_SPA):.2f}")
print(f"  rest vs BBN    z = {z(REST, s_REST, BBN, s_BBN):.2f}")
print(f"  rest vs SPT+ACT z = {z(REST, s_REST, SPTACT, s_SPTACT):.2f}")

# [2] Can a perfect independent measurement separate 71.69 from SH0ES 73.49
# as a two-measurement comparison? Max z when sigma_new -> 0 is gap / s_SH0ES.
gap = SH0ES - REST
print("[2] two-measurement test of 'smaller' (SH0ES error kept)")
print(f"  gap {gap:.2f}; max z with sigma_new = 0: {gap / s_SH0ES:.2f}")
# point-null test (true local H0 = 73.49 exactly)
for k in (2, 3):
    print(f"  point-null 73.49 vs centre 71.69 at {k} sigma: sigma_new <= {gap / k:.2f}")

# [3] sigma needed to separate pairs of predicted centres at 3 sigma (point-null)
print("[3] sigma_new for 3-sigma separation of predicted centres (point values)")
pairs = {
    "C8 71.0 vs C1 68.5": (71.0, 68.5),
    "C8 71.0 vs C1 67.5": (71.0, 67.5),
    "C8 71.0 vs C3/C7 73.0": (71.0, 73.0),
    "C8 71.7 vs SH0ES 73.49": (71.7, 73.49),
}
for name, (a, b) in pairs.items():
    print(f"  {name}: sigma <= {abs(a - b) / 3:.2f} ({100 * abs(a - b) / 3 / a:.2f}% of {a})")

# [4] C4(ii) split test: anchor-free one-step vs team-independent TRGB ladder.
# C4(ii) predicts one-step ~67.5 and stellar ladders ~73 (split 5.5); C8 predicts ~0.
split = 73.0 - 67.5
need = split / 3
print("[4] C4(ii) split between one-step and team-independent ladder")
print(f"  split {split:.1f}; sigma on difference for 3 sigma {need:.2f};"
      f" each arm (equal) {need / math.sqrt(2):.2f}")

# [5] outcome windows for a team-independent local H0 at sigma_new
print("[5] outcome windows (C8 holds if value <= SH0ES - 3 s_new and value >= SPA + 3 s_comb)")
for s_new in (1.14, 0.8, 0.6, 0.5):
    hi = SH0ES - 3 * s_new  # 'smaller' established vs point SH0ES
    lo = SPA + 3 * math.hypot(s_new, s_SPA)  # excess over CMB-SPA real at 3 sigma
    lo_bbn = BBN + 3 * math.hypot(s_new, s_BBN)
    five = SPA + 5 * math.hypot(s_new, s_SPA)  # team-independent >= 5 sigma restores premise
    print(f"  s_new {s_new:.2f}: smaller-at-3sig if <= {hi:.2f}; excess-at-3sig(SPA) if >= {lo:.2f};"
          f" (BBN) >= {lo_bbn:.2f}; >=5sig vs SPA if >= {five:.2f}")

# [6] time-delay lens count needed (ASSUMED sigma ~ 1/sqrt(N), no floor; 11 lenses at 2.35)
s11 = 2.35
print("[6] time-delay lenses needed, no systematic floor (ASSUMED 1/sqrt(N) scaling)")
for s_new in (1.06, 0.67, 0.6):
    print(f"  sigma {s_new:.2f}: N ~ {11 * (s11 / s_new) ** 2:.0f}")
