"""Falsifier C1-0 (magnitude): can a ladder systematic, esp. at the SN Ia step, carry
most of the gap and put true H0 at 67-68.5 km/s/Mpc, given every measurement class?
Units: H0 in km/s/Mpc; magnitudes in mag (5 log10 H0 ratio). Gaussian errors, 68%.
All inputs from the run dossier (D-numbers in comments)."""
import math

def dm(a, b):
    return 5 * math.log10(a / b)

def p2(z):  # two-sided Gaussian p
    return math.erfc(abs(z) / math.sqrt(2))

def z_from_p(p):  # two-sided Gaussian-equivalent z
    lo, hi = 0.0, 40.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if p2(mid) > p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

def chi2_sf(x, k):  # survival function of chi2 with k dof (series / regularized gamma)
    # regularized upper incomplete gamma Q(k/2, x/2)
    a, t = k / 2.0, x / 2.0
    if t < a + 1:
        s, term, n = 1.0 / a, 1.0 / a, 0
        while abs(term) > 1e-16 * s:
            n += 1
            term *= t / (a + n)
            s += term
        P = s * math.exp(-t + a * math.log(t) - math.lgamma(a))
        return 1 - P
    # continued fraction
    b = t + 1 - a; c = 1e300; d = 1 / b; h = d
    for i in range(1, 500):
        an = -i * (i - a); b += 2
        d = an * d + b; d = 1 / d if d != 0 else 1e300
        c = b + an / c
        h *= d * c
        if abs(d * c - 1) < 1e-16:
            break
    return math.exp(-t + a * math.log(t) - math.lgamma(a)) * h

def tot(*e):
    return math.sqrt(sum(x * x for x in e))

print("=== 1. Required ladder shift to reach C1's true-H0 band ===")
for name, H in [("SH0ES 73.49 (D-20)", 73.49), ("H0DN corrected 73.264 (D-22)", 73.264), ("H0DN baseline 73.50 (D-22)", 73.50)]:
    for Ht in (67.0, 67.19, 68.5):
        print(f"  {name} -> {Ht}: {dm(H, Ht):.4f} mag")
gap = dm(73.264, 67.19)
print(f"  reference gap H0DN-CMB-SPA = {gap:.4f} mag; half = {gap/2:.4f} mag")
print(f"  fraction of gap removed if true H0 = 68.5: {dm(73.264,68.5)/gap:.3f}; =67.0: {dm(73.264,67.0)/gap:.3f}")

print("\n=== 2. Named SN-step levers vs requirement (D-35, D-25, M-MECHANIST-04) ===")
WH_max = dm(73.49, 70.59)    # Wojtak & Hjorth 2025 two-population, largest version
WH_min = dm(73.49, 71.45)
comp = 0.038                  # Pantheon+ vs CSP compilation (d), M-MECHANIST-04
env = 0.17 * 0.5              # environment step at ASSUMED df=0.5
print(f"  (a) W&H: {WH_min:.4f}-{WH_max:.4f} mag; (a') env step at df=0.5: {env:.4f} mag; (d) compilation: {comp:.4f} mag")
sn_only = WH_max + comp
print(f"  SN-step-only coherent max (a)+(d) = {sn_only:.4f} mag -> H0DN 73.264 falls to {73.264*10**(-sn_only/5):.2f}")
sn_only2 = max(WH_max, env) + comp
print(f"  using max((a),(a')) + (d) = {sn_only2:.4f} mag -> {73.264*10**(-sn_only2/5):.2f}")
print(f"  (a)+(a')+(d) if all independent and additive = {WH_max+env+comp:.4f} mag -> {73.264*10**(-(WH_max+env+comp)/5):.2f}")

print("\n=== 3. Internal SN-vs-no-SN consistency of the same network (D-22, D-23) ===")
# H0DN baseline 73.50 +- 0.81 vs no-SNe variant 73.434 +- 1.795 (same anchors/primary indicators).
# Nested-estimate difference: var = s_sub^2 - s_full^2 (full is the optimal combination containing sub).
Hf, sf = 73.50, 0.81
Hs, ss = 73.434, 1.795
dH = Hf - Hs
sd = math.sqrt(ss**2 - sf**2)
d_mag = dm(Hf, Hs)
sd_mag = (5 / math.log(10)) * sd / Hs
print(f"  SN-channel minus SN-free channel: {dH:+.3f} +- {sd:.3f} km/s/Mpc = {d_mag:+.4f} +- {sd_mag:.4f} mag")
# The SN-free channel's own information: SN channel alone estimate by subtraction of information
w_f, w_s = 1 / sf**2, 1 / ss**2
w_sn = w_f - w_s
H_sn = (Hf * w_f - Hs * w_s) / w_sn
s_sn = 1 / math.sqrt(w_sn)
print(f"  implied SN-channel-only H0 = {H_sn:.3f} +- {s_sn:.3f}; SN minus no-SN = {H_sn-Hs:+.3f} +- {math.sqrt(s_sn**2+ss**2):.3f}")
dd = dm(H_sn, Hs); sdd = (5/math.log(10))*math.sqrt(s_sn**2+ss**2)/Hs
print(f"  in mag: {dd:+.4f} +- {sdd:.4f}")
for need, lab in [(gap/2, "more than half the gap (C1 'most')"), (dm(73.50, 68.5), "reach 68.5"), (dm(73.50, 67.19), "reach 67.19")]:
    z = (need - dd) / sdd
    print(f"  SN-only bias needed to {lab}: {need:.4f} mag; tension with measured SN-minus-noSN offset: {z:.2f} sigma (one-sided p {p2(z)/2:.2e})")

print("\n=== 4. Channels an SN-step bias cannot move, tested against C1's true H0 ===")
SBF = (73.8, tot(0.7, 2.3))     # D-29, no Cepheids, no SNe
TF = (73.3, tot(2.1, 3.5))      # D-30
TD = (71.1, 2.35)               # D-31 symmetrised
MAS = (71.6, 3.7)               # D-32 stat only
GW = (71.7, 8.45)               # D-33 symmetrised
sets = {"SBF,TF,TD,MAS,GW": [SBF, TF, TD, MAS, GW], "one-step TD,MAS,GW": [TD, MAS, GW], "SBF alone": [SBF],
        "H0DN no-SN (D-23) + TD + GW": [(73.434, 1.795), TD, GW]}
for nm, s in sets.items():
    w = [1 / e**2 for _, e in s]
    m = sum(v * wi for (v, _), wi in zip(s, w)) / sum(w)
    sm = 1 / math.sqrt(sum(w))
    line = f"  {nm}: mean {m:.2f} +- {sm:.2f}"
    for Ht in (67.19, 68.5, 70.2):
        chi2 = sum(((v - Ht) / e) ** 2 for v, e in s)
        p = chi2_sf(chi2, len(s))
        zt = (m - Ht) / sm
        line += f" | Ht={Ht}: mean-z {zt:.2f}, chi2 {chi2:.2f}/{len(s)} p={p:.3g} (z_eq {z_from_p(p):.2f})"
    print(line)

print("\n=== 5. Flow lever (c), the only one reaching SBF/TF: size vs LCDM cosmic variance ===")
cv_mag = (5 / math.log(10)) * (0.31 / 67.19)   # M-DECOMPOSER-04 cosmic-variance figure, 0.46%
dong = dm(74.30, 71.37)
print(f"  Dong (c) shift {dong:.4f} mag = {dong/cv_mag:.1f} x LCDM local-H0 cosmic variance ({cv_mag:.4f} mag)")
print(f"  as a physical coherent flow it would be {dong/cv_mag:.1f} sigma; as a method correction it is a contested re-analysis (same data)")
print(f"  combined (a)max+(c)+(d) = {WH_max+dong+comp:.4f} mag ({(WH_max+dong+comp)/gap*100:.0f}% of gap), overlap unknown")
print(f"  with (c) alone acting on SBF: SBF 73.8 -> {73.8*10**(-dong/5):.2f}")

print("\n=== 6. 'Same SN-step amount' applied to the TRGB/JAGB-SN ladders (C1 prediction-matrix row) ===")
for lab, sh in [("needed for SH0ES->68.5", dm(73.49, 68.5)), ("needed for SH0ES->67.19", dm(73.49, 67.19))]:
    for nm, H, s in [("CCHP 70.39 (D-24)", 70.39, 1.94), ("CCHP JWST 68.81 (D-25)", 68.81, 2.29), ("JAGB CCHP 67.80 (D-26)", 67.80, 2.72), ("SH0ES-side TRGB 72.1 (D-27)", 72.1, 1.8), ("SH0ES-side TRGB 73.3 (D-27)", 73.3, 1.8)]:
        Hc = H * 10 ** (-sh / 5)
        print(f"  {lab} ({sh:.4f} mag): {nm} -> {Hc:.2f} +- {s*Hc/H:.2f}; vs CMB-SPA 67.19+-0.38: {(Hc-67.19)/math.hypot(s*Hc/H,0.38):+.2f} sigma")

print("\n=== 7. Narrowed endpoint scan: true H0 69.0-70.2 ===")
for Ht in (69.0, 69.5, 70.0, 70.2):
    need = dm(73.50, Ht)
    zsn = (need - dd) / sdd
    z1 = (72.39 - Ht) / 1.41
    z2 = (72.55 - Ht) / 1.41
    print(f"  Ht={Ht}: SN-step bias {need:.4f} mag ({dm(73.264,Ht)/gap*100:.0f}% of gap); SN-vs-noSN {zsn:.2f} sigma; SN-free means {z1:.2f} / {z2:.2f} sigma")
