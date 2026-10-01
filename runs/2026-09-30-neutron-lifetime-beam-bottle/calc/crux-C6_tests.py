"""Crux C6: size of the deciding tests for the surviving excited-neutron (n*) variant.

Units: SI (times in s, lifetimes in s). lambda, A, a dimensionless.
Inputs (all traced):
  - gap: BL1 887.7 s vs UCNtau 877.82 s -> 9.88 s [candidates.md header; D-20, D-27]
  - BL1 decaying-neutron ages: mean 94.5 ms, 10-90% 47-155 ms [verdict C6-0, its calc]
  - J-PARC ages 10-40 ms (C6-0) / 16-40 ms (C6-1); J-PARC 877.2 +4.35/-3.98 s [D-23]
  - Koch-Hummel toy state tau_e/tau_g = 25/9; required n*/n = 1.11-1.74 % [C6-0, C6-1]
  - PERKEO III A0 = -0.11985(17)(12) [D-40]; aSPECT a = -0.10402 +- 0.00082 [D-42]
  - lambda PERKEO III -1.27641(56), aSPECT 2024 -1.2668(27) [D-40, D-42]; Nab goal 0.04 % [D-107]
Model: the lifetime shift of a beam is linear in the n* fraction present at decay time,
which falls as exp(-t/tau_gamma) from production (Koch-Hummel eq. 6 in the small-fraction limit).
"""
import math

TAU_BOT = 877.82
GAP = 887.7 - 877.82          # s, BL1 vs UCNtau
T_BL1_MEAN = 0.0945           # s
T_FAST, T_SLOW = 0.047, 0.155 # s, BL1 10% / 90% ages
T_JP = (0.010, 0.025, 0.040)  # s, J-PARC ages
JP, JP_ERR_UP = 877.2, 4.35

print("== 1. Shift vs neutron age (equal production, calibrated to BL1 mean age) ==")
print("tau_g[s]  f0_needed(Ge->0)  BL1 fast(47ms)  BL1 slow(155ms)  fast-slow[s]  J-PARC(25ms) pred[s]  z_JPARC")
for tg in (0.05, 0.1, 0.3, 1.0, 3.0, 10.0, 139.0):
    f0 = 0.0111 * math.exp(T_BL1_MEAN / tg)
    s = lambda t: GAP * math.exp(-(t - T_BL1_MEAN) / tg)
    fast, slow = s(T_FAST), s(T_SLOW)
    jp = TAU_BOT + s(0.025)
    z = (jp - JP) / JP_ERR_UP
    print(f"{tg:8.2f}  {f0*100:14.2f}%  {fast:13.2f}  {slow:14.2f}  {fast-slow:11.2f}  {jp:19.2f}  {z:6.2f}")
print("Age-resolved (TOF) BL test resolves tau_g only where fast-slow exceeds the subset error;")
print("for tau_g >= 3 s the fast-slow difference is < 0.4 s: no age signature in any beam.")

print("\n== 2. Fission-only escape: BL2/BL3 (reactor) vs LiNA (spallation) ==")
print(f"C6-escape predicts BL2 ~ {TAU_BOT+GAP:.1f} s and LiNA ~ {TAU_BOT:.1f} s (same pattern as C5).")
print(f"C6-equal predicts LiNA ~ {TAU_BOT+GAP:.1f} s or more (same as C3).")
for sig in (1.0, 0.3):
    print(f"  at sigma = {sig} s the 888-vs-878 poles differ by {GAP/sig:.1f} sigma of the new result alone")
mid_c7 = 883.0
print(f"  C7 midpoint {mid_c7} s vs C6 {TAU_BOT+GAP:.1f} s at 1 s: {(TAU_BOT+GAP-mid_c7)/1.0:.1f} sigma")

print("\n== 3. SM A route: n* contamination of PERKEO III A (not a rate) ==")
sA = math.hypot(0.00017, 0.00012)
A0 = 0.11985
for ratio, fn in ((25/9, 0.0174), (1/0.04, 0.0116)):
    # fraction of decays from n*: (f/tau_e)/((1-f)/tau_g + f/tau_e)
    fd = (fn / ratio) / ((1 - fn) + fn / ratio)
    dA = sA / fd
    print(f"tau_e/tau_g={ratio:.2f}, n*/n={fn*100:.2f}% -> decay share {fd*100:.3f}%; "
          f"|A_e-A_g| must be < {dA:.3f} ({dA/A0*100:.0f}% of |A0|) to stay within 1 sigma ({sA:.5f})")
print("With Gamma_e -> 0 the decay share -> 0 and A is untouched.")

print("\n== 4. Nab lambda: C6 (PERKEO-like) vs C2/C3/C5/C8-strong (aSPECT-like) ==")
lp, la = 1.27641, 1.2668
snab = 0.0004 * 1.2716
d = lp - la
print(f"Delta|lambda| = {d:.5f}; Nab sigma at 0.04% = {snab:.5f}; separation {d/snab:.1f} sigma (Nab error only)")
print(f"with PERKEO error 0.00056 added: {d/math.hypot(snab,0.00056):.1f} sigma; "
      f"with aSPECT error 0.0027 added: {d/math.hypot(snab,0.0027):.1f} sigma")
