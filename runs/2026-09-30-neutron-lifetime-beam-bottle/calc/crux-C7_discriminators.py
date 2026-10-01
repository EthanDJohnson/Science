"""Crux C7: separation power of planned measurements between the narrowed null (C7)
and its rivals, plus the heavy-tail cost the narrowed null must pay.
Units: SI (lifetimes in s); lambda, a dimensionless.
Inputs (all from candidates.md / dossier.md / verdicts):
  storage pole 878.32 +- 0.43 s (M-STATISTICIAN-02), UCNtau 877.82 +- 0.29 s (D-27 symmetrised)
  proton pole 887.97 +- 2.04 s (M-STATISTICIAN-02), BL1 887.7 +- 2.25 s (D-20)
  lambda PERKEO III -1.27641(56) (D-40), aSPECT 2024 -1.2668(27) (D-42)
  Nab goal dlambda/|lambda| = 0.04 % (D-107)
  BL2 < 1 s (D-100), BL3 0.3 s (D-101), LiNA ~1 s (D-102), UCNProBe 1-2 s (D-106)
  BL1 budget items (D-20): fluence 0.5, deposit 0.9, unassoc 1.7, proton stat 1.2 s
  pulls BL1 4.26, Sussex 2.3 (verdict C7-0), aSPECT a-route vs anchor 3.17 (verdict C7-2)
"""
import math
from scipy import stats

def z(x, sx, y, sy):
    return abs(x - y) / math.hypot(sx, sy)

S_POLE, S_ERR = 878.32, 0.43
P_POLE, P_ERR = 887.97, 2.04
print("== 1. BL2 / BL3 reading R: distance from storage pole and proton pole (sigma) ==")
for name, sig in (("BL2", 1.0), ("BL3", 0.3)):
    for R in (878.3, 880.0, 882.0, 884.0, 886.0, 888.0):
        print(f"{name} sigma {sig:.1f} s, R = {R:.1f} s: vs storage {z(R,sig,S_POLE,S_ERR):5.2f} sigma, "
              f"vs proton pole {z(R,sig,P_POLE,P_ERR):5.2f} sigma")

print("\n== 2. C1 (one effect >= 2/3 of gap) vs C7 (each item <= 1/3 of gap) ==")
gap_bl1 = 887.7 - 877.82
one_big = 2/3 * gap_bl1
each_small = 1/3 * gap_bl1
print(f"BL1-UCNtau gap {gap_bl1:.2f} s; C1 single effect >= {one_big:.2f} s; C7 items <= {each_small:.2f} s")
for sig in (0.5, 1.0, 1.1, 1.5, 2.4):
    print(f"  scan-difference error {sig:.1f} s: separation (one_big - each_small)/sigma = {(one_big-each_small)/sig:.2f}")
bl1_half_stat = 1.2 * math.sqrt(2)
diff_err = bl1_half_stat * math.sqrt(2)
print(f"BL1 existing 5 ms vs 10 ms split (equal halves): each stat {bl1_half_stat:.2f} s, difference error {diff_err:.2f} s;"
      f" C1-A2 predicted 5.1 s -> {5.1/diff_err:.2f} sigma from 0")

print("\n== 3. BL1 excess as spread over its own budget items (Gaussian) ==")
items = {"fluence": 0.5, "deposit": 0.9, "unassoc": 1.7, "p-stat": 1.2}
tot = math.sqrt(sum(v*v for v in items.values()))
print(f"BL1 budget quadrature {tot:.2f} s; excess vs UCNtau {gap_bl1:.2f} s")
k_equal = gap_bl1 / sum(items.values())
print(f"equal-k pull on every item (same sign): k = {k_equal:.2f}")
print(f"min-chi2 spread (shift ∝ sigma_i^2): total pull = {gap_bl1/math.hypot(tot,0.29):.2f} sigma (unchanged by spreading)")
for S in (1.0, 1.5, 2.0, 2.3):
    zz = gap_bl1 / math.hypot(S*2.25, 0.29)
    print(f"BL1 error x{S}: {zz:.2f} sigma, one-sided p = {stats.norm.sf(zz):.3g}")

print("\n== 4. Heavy-tail cost: BL1 + Sussex + aSPECT all high, independent (unit-scale Student-t) ==")
for nu in (2, 3, 4, 1e6):
    p_b = stats.t.sf(4.26, nu); p_s = stats.t.sf(2.3, nu); p_a = stats.t.sf(3.17, nu)
    joint = p_b * p_s * p_a
    lab = "Gauss" if nu > 1e5 else f"nu={nu}"
    print(f"{lab}: one-sided P BL1 {p_b:.3g}, Sussex {p_s:.3g}, aSPECT {p_a:.3g}; joint {joint:.3g}; "
          f"BL1+Sussex {p_b*p_s:.3g}")

print("\n== 5. Nab: PERKEO-like vs aSPECT-like ==")
lA, sA = -1.27641, 0.00056
la, sa = -1.2668, 0.0027
sN = 0.0004 * abs(lA)
d = abs(lA - la)
print(f"sigma_Nab = {sN:.5f}; |Delta lambda| = {d:.5f}")
print(f"Nab reads PERKEO-like: {d/math.hypot(sN, sa):.2f} sigma from aSPECT")
print(f"Nab reads aSPECT-like: {d/math.hypot(sN, sA):.2f} sigma from PERKEO III (A route)")

print("\n== 6. UCNProBe beta-rate minus storage lifetime in one trap ==")
for sd in (1.0, 1.5, 2.0, 2.5):
    print(f"difference error {sd:.1f} s: C2/C3 predicted +9.65 s -> {9.65/sd:.2f} sigma from C7's 0")

print("\n== 7. LiNA (~1 s) ==")
for R in (878.0, 883.0, 888.0):
    print(f"LiNA R = {R:.1f} +- 1.0 s: vs storage {z(R,1.0,S_POLE,S_ERR):.2f} sigma; vs proton pole {z(R,1.0,P_POLE,P_ERR):.2f} sigma")
