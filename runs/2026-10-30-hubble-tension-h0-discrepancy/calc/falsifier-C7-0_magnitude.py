"""Falsifier C7-0 (magnitude): does the H0 gap map entirely onto the two absolute
calibrations (M_B ladder scale vs sound horizon r_d), and how much can sit elsewhere?
Units: H0 in km/s/Mpc, magnitudes in mag, r_d in Mpc. Inputs are dossier values (IDs given).
"""
import math

def dmag(h1, h2):
    return 5 * math.log10(h1 / h2)

def tens(a, sa, b, sb):
    return (a - b) / math.hypot(sa, sb)

print("=== 1. Gap in magnitudes and in r_d (identity 5 log10 H0 = M_B + 5 a_B + 25) ===")
local = {"H0DN 73.264": 73.264, "SH0ES 73.49": 73.49, "anchored group 73.02": 73.02}
early = {"CMB-SPA 67.19": 67.19, "BAO+BBN 68.50": 68.50, "r_d group 67.51": 67.51}
for ln, lv in local.items():
    for en, ev in early.items():
        print(f"  {ln} vs {en}: gap {lv-ev:.3f} km/s/Mpc, {100*(lv/ev-1):.2f} %, {dmag(lv, ev):.4f} mag; "
              f"r_d needed = 147.00*{ev}/{lv} = {147.00*ev/lv:.2f} Mpc")
hrd = 101.54  # Mpc, DESI DR2 h r_d (D-45)
print(f"  DESI h*r_d = {hrd} Mpc -> r_d for 73.264: {hrd/0.73264:.2f} Mpc; for 73.02: {hrd/0.7302:.2f} Mpc")

print("\n=== 2. Is the naive M_B pair (0.122/0.141 mag) a measurement of the calibration gap? ===")
MB_lad, H_lad = -19.253, 73.04            # R22 (D-20 supersession note, D-21)
aB_lad = math.log10(H_lad) - 0.2 * MB_lad - 5
print(f"  a_B implied by R22 (M_B=-19.253, H0=73.04): {aB_lad:.5f}")
for lab, MB_inv, H_inv in [("cosmography", -19.375, 67.19), ("flat LCDM", -19.394, 67.67)]:
    aB_inv = math.log10(H_inv) - 0.2 * MB_inv - 5
    dM = MB_lad - MB_inv
    d5a = 5 * (aB_lad - aB_inv)
    print(f"  inverse ladder ({lab}, DES-SN5YR+DESI DR1, D-21/D-48): M_B={MB_inv}, H0={H_inv} -> a_B={aB_inv:.5f}")
    print(f"     Delta M_B = {dM:.4f} mag; 5*Delta a_B (SN-system intercept) = {d5a:.4f} mag; "
          f"sum = {dM+d5a:.4f} mag; H0 gap 5log10({H_lad}/{H_inv}) = {dmag(H_lad, H_inv):.4f} mag")
    H_if_same_aB = 10 ** (0.2 * MB_inv + aB_lad + 5)
    print(f"     inverse-ladder M_B with the R22 a_B would give H0 = {H_if_same_aB:.2f} (not {H_inv})")
    print(f"     share of H0 gap carried by the cross-system intercept: {100*d5a/dmag(H_lad, H_inv):.1f} %")

print("\n=== 3. Non-calibration freedom: how much of the gap can sit outside M_B and r_d? ===")
gap = 73.264 - 67.19
items = [
    ("inverse ladder: cosmography vs flat LCDM (H(z) shape freedom, D-48)", 67.67 - 67.19),
    ("SN-cosmology systematics in inverse ladder (Popovic 2026, D-07/D-48, upper bound)", 0.1),
    ("H0DN Hubble-flow cut variants 73.190 vs 72.667 (D-23)", 73.190 - 72.667),
    ("H0DN baseline 73.50 vs 0.03-0.10 cut 72.667 (D-22/D-23)", 73.50 - 72.667),
    ("Dong et al. 2026 preprint: host peculiar-velocity correction 74.30 -> 71.37 (D-82)", 74.30 - 71.37),
]
for lab, v in items:
    print(f"  {lab}: {v:.3f} km/s/Mpc = {100*v/gap:.1f} % of the {gap:.3f} km/s/Mpc gap")
print("  D-07: a -0.3 mag SN-shape shift recovers only 70.96 -> fraction",
      f"{(70.96-67.19)/gap*100:.1f} % of gap for 0.3 mag (10-sigma-class shape distortion)")

print("\n=== 4. Can the geometric anchors themselves carry the scale offset? ===")
for ln, lv in [("H0DN", 73.264), ("SH0ES", 73.49)]:
    for en, ev in [("SPA", 67.19), ("BAO+BBN", 68.50)]:
        frac = lv / ev - 1
        print(f"  {ln} vs {en}: anchor-distance shift needed {100*frac:.2f} % = {frac/0.0145:.1f} x the 1.45 % NGC 4258 error")
loo = {"baseline": 73.50, "no MW parallaxes": 73.609, "no NGC 4258": 73.084}
print("  H0DN leave-one-anchor-out (D-23):", loo, "-> max swing",
      f"{max(loo.values())-min(loo.values()):.3f} km/s/Mpc = {100*(max(loo.values())-min(loo.values()))/gap:.1f} % of gap")

print("\n=== 5. Spread inside the 'one' anchor-calibrated scale (same anchor NGC 4258) ===")
pairs = [("SH0ES Cepheid 73.49 vs CCHP TRGB 70.39", 73.49, 0.93, 70.39, math.sqrt(1.22**2+1.33**2+0.70**2)),
         ("SH0ES-side JAGB 73.3 vs CCHP JAGB 67.80 (overlapping data)", 73.3, math.hypot(1.4, 2.0), 67.80, math.hypot(2.17, 1.64)),
         ("SH0ES 73.49 vs CCHP JWST-only TRGB 68.81", 73.49, 0.93, 68.81, 1.80)]
for lab, a, sa, b, sb in pairs:
    print(f"  {lab}: {a-b:.2f} km/s/Mpc, {dmag(a, b):.4f} mag = {100*dmag(a,b)/dmag(73.264,67.19):.0f} % of the H0DN-SPA gap in mag; "
          f"naive {tens(a, sa, b, sb):.2f} sigma (overstated independence where data overlap)")

print("\n=== 6. Arbiter: anchor-free AND r_d-free H0 (C7's own decisive class) ===")
def ivm(vals):
    w = [1 / s**2 for _, s in vals]
    m = sum(v * wi for (v, _), wi in zip(vals, w)) / sum(w)
    return m, 1 / math.sqrt(sum(w))
sets = {
    "TD + sirens (one-step, anchor-free)": [(71.1, 2.35), (71.7, 8.45)],
    "TD + sirens + r_d-free BAO 69.6 + equality 65.1": [(71.1, 2.35), (71.7, 8.45), (69.6, 1.55), (65.1, 4.2)],
    "TD + sirens + r_d-free 67.9 (2411.16677, Pantheon+) + equality 65.1": [(71.1, 2.35), (71.7, 8.45), (67.9, 2.0), (65.1, 4.2)],
}
for lab, vals in sets.items():
    m, s = ivm(vals)
    pos = (m - 67.51) / (73.02 - 67.51)
    print(f"  {lab}: {m:.2f} +- {s:.2f}; {tens(73.02, 0.78, m, s):.2f} sigma below anchored group (73.02+-0.78), "
          f"{tens(m, s, 67.51, 0.29):.2f} sigma above r_d group (67.51+-0.29); position {pos:.2f} of the way from r_d to anchor")
print("  sigma needed to place a value 3 sigma from the midpoint-split: ", f"{(73.02-67.51)/2/3:.2f} km/s/Mpc")

print("\n=== 7. Does BAO+SN 'pin H(z)' at z < 0.1? Najera, Banik & Desmond 2026 (arXiv:2610.23657, preprint) ===")
from statistics import NormalDist
nd = NormalDist()
cases = [("DES-Dovekie only, cosmographic H(z), standard r_d", 76.25, 2.87),
         ("DES + legacy as published", 67.98, 0.69),
         ("DES + legacy, Delta H(z)=A exp(-z/z1), + local anchors", 67.66, 1.01),
         ("DES + legacy with free legacy offset (0.0646+-0.0391 mag)", 71.03, 1.99)]
base = 67.98
for lab, h, s in cases:
    print(f"  {lab}: H0 = {h} +- {s}; shift from DES+legacy {h-base:+.2f} km/s/Mpc = "
          f"{100*(h-base)/(73.264-base):.0f} % of the (73.264 - {base}) gap; vs H0DN {tens(73.264,0.806,h,s):.2f} sigma; "
          f"vs CMB-SPA {tens(h,s,67.19,0.38):.2f} sigma")
off, soff = 0.0646, 0.0391
print(f"  legacy offset significance: {off/soff:.2f} sigma; mag needed to move H0 by 3.05: {dmag(71.03, 67.98):.4f} mag")
p = 0.0124
print(f"  mock probability 1.24 % -> one-sided z = {nd.inv_cdf(1-p):.2f}, two-sided z = {nd.inv_cdf(1-p/2):.2f}")
print("  C7's own threshold: 'no H(z) change at 0<z<2 moves the gap by > ~0.5 sigma' -> 0.5 sigma of gap error",
      f"sqrt(0.806^2+0.69^2)={math.hypot(0.806,0.69):.2f}, i.e. {0.5*math.hypot(0.806,0.69):.2f} km/s/Mpc; "
      f"free-offset case moves it by {71.03-67.98:.2f} = {(71.03-67.98)/math.hypot(0.806,0.69):.2f} sigma")
