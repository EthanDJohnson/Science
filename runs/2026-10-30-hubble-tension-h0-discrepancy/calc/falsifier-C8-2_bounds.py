"""Falsifier C8-2 (bounds angle): test C8's "team-independent anomaly ~4 km/s/Mpc at only ~3-3.7 sigma"
against every independent early-universe reference and against Cepheid-free / team-variant local sets.
Units: H0 in km/s/Mpc (astronomical units); significances are Gaussian-equivalent sigma.
Inputs are dossier values (D-IDs in comments); errors symmetrised where asymmetric (as in M-EXAMINER-03)."""
import math

def comb(items, C_extra=None):
    # inverse-variance (diagonal) mean
    w = [1/s**2 for _, s in items]
    m = sum(wi*x for wi, (x, _) in zip(w, items))/sum(w)
    return m, sum(w)**-0.5

def z(a, sa, b, sb):
    return abs(a-b)/math.hypot(sa, sb)

def p2(zv):
    return math.erfc(zv/math.sqrt(2))

# local, non-SH0ES classes (M-EXAMINER-03 set)
CCHP = (70.39, math.sqrt(1.22**2+1.33**2+0.70**2))   # D-24 total
SBF  = (73.8, math.hypot(0.7, 2.3))                  # D-29
TF   = (73.3, math.hypot(2.1, 3.5))                  # D-30
TD   = (71.1, 2.35)                                  # D-31 symmetrised
MAS  = (71.6, 3.7)                                   # D-32 stat only
GW   = (71.7, (9.4+7.5)/2)                           # D-33 symmetrised
SH0ES = (73.49, 0.93)                                # D-20
LiTRGB = (72.7, 1.8)                                 # D-27 midpoint of 72.1-73.3 +- 1.8 (SH0ES-side, Cepheid-free)
H0DN_noCep = (72.509, 1.296)                         # D-23 V08

base = [CCHP, SBF, TF, TD, MAS, GW]
m0, s0 = comb(base)
print(f"[1] non-SH0ES mean (CCHP,SBF,TF,TD,masers,sirens): {m0:.3f} +- {s0:.3f}  (check vs M-EXAMINER-03 71.692 +- 1.141)")

early = {
    "CMB-SPA 67.19+-0.38 (D-44)": (67.19, 0.38),
    "Planck PR4 67.64+-0.52 (D-41)": (67.64, 0.52),
    "ACT DR6 alone 66.51+-0.64 (D-42)": (66.51, 0.64),
    "SPT-3G alone 66.66+-0.60 (D-43)": (66.66, 0.60),
    "SPT+ACT (no Planck) 66.59+-0.46 (D-43)": (66.59, 0.46),
    "DESI BAO+BBN 68.50+-0.58 (D-45)": (68.50, 0.58),
    "inverse ladder 67.19+-0.65 (D-48)": (67.19, 0.65),
    "inverse ladder flat LCDM 67.67+-0.685 (D-48)": (67.67, 0.685),
}
# pooled independent early: CMB-SPA + BAO+BBN (treated independent; both share BBN-type omega_b info only loosely)
pe = comb([(67.19, 0.38), (68.50, 0.58)])
early["pooled CMB-SPA + BAO+BBN %.2f+-%.3f" % pe] = pe

print("\n[2] non-SH0ES mean vs each early reference: gap, sigma")
zs = []
for k, (e, se) in early.items():
    zz = z(m0, s0, e, se); zs.append(zz)
    print(f"   {k:48s} gap {m0-e:5.2f}  z = {zz:.2f}")
print(f"   range over references: {min(zs):.2f} - {max(zs):.2f} sigma")

print("\n[3] Variants of the 'team-independent' set vs CMB-SPA (67.19+-0.38) and vs SPT+ACT (66.59+-0.46)")
variants = {
    "drop TF (Cepheid/TRGB zero points via SH0ES-type hosts)": [CCHP, SBF, TD, MAS, GW],
    "drop TF and SBF (only CCHP + one-step)": [CCHP, TD, MAS, GW],
    "one-step only (TD, masers, sirens)": [TD, MAS, GW],
    "Cepheid-free, SH0ES-side TRGB replaces CCHP": [LiTRGB, SBF, TF, TD, MAS, GW],
    "H0DN no-Cepheid V08 alone": [H0DN_noCep],
    "H0DN no-Cepheid V08 + one-step": [H0DN_noCep, TD, MAS, GW],
}
for k, it in variants.items():
    m, s = comb(it)
    print(f"   {k:50s} {m:6.2f} +- {s:4.2f}  z_SPA = {z(m,s,67.19,0.38):.2f}  z_SPT+ACT = {z(m,s,66.59,0.46):.2f}  z_BAO+BBN = {z(m,s,68.50,0.58):.2f}")

print("\n[4] Is the team-independent gap 'smaller' than the SH0ES gap?")
gap_rest = m0-67.19; sg = math.hypot(s0, 0.38)
gap_sh = SH0ES[0]-67.19
print(f"   rest-vs-SPA gap = {gap_rest:.2f} +- {sg:.2f} km/s/Mpc; SH0ES gap = {gap_sh:.2f}")
print(f"   SH0ES vs rest: diff {SH0ES[0]-m0:.2f} +- {math.hypot(SH0ES[1], s0):.2f}, z = {z(SH0ES[0],SH0ES[1],m0,s0):.2f}")
print(f"   the rest-only gap is below the SH0ES gap by only {(gap_sh-gap_rest)/sg:.2f} sigma (of its own error)")
mag_rest = 5*math.log10(m0/67.19); mag_sh = 5*math.log10(73.49/67.19)
print(f"   in mag: rest {mag_rest:.3f}, SH0ES {mag_sh:.3f}")

print("\n[5] Why the significance drops: precision, not disagreement")
for k in (5.0, 3.0):
    need = math.sqrt(max((gap_rest/k)**2 - 0.38**2, 0))
    print(f"   sigma_local needed for {k:.0f} sigma at the current non-SH0ES centre vs SPA: {need:.3f} (now {s0:.3f}; ratio {s0/need:.2f})")
# if the non-SH0ES set had SH0ES's centre with its own error
print(f"   non-SH0ES error with SH0ES centre 73.49: z = {z(73.49,s0,67.19,0.38):.2f}")
print(f"   SH0ES centre with SH0ES error but rest's centre 71.69: z = {z(m0,0.93,67.19,0.38):.2f}")

print("\n[3b] Robustness of the Cepheid-free near-5-sigma routes")
for lo_hi in (72.1, 73.3):
    it = [(lo_hi, 1.8), SBF, TD, MAS, GW]   # SH0ES-side TRGB at range ends, TF dropped
    m, s = comb(it)
    print(f"   SH0ES-side TRGB {lo_hi} +- 1.8, no TF: {m:.2f} +- {s:.2f}  z_SPA = {z(m,s,67.19,0.38):.2f}  z_SPT+ACT = {z(m,s,66.59,0.46):.2f}")
for sh in (-0.2, -0.4):   # D-20/D-22 corrected-Pantheon+ shift applied to H0DN V08
    m, s = comb([(72.509+sh, 1.296), TD, MAS, GW])
    print(f"   H0DN V08 shifted {sh:+.1f} + one-step: {m:.2f} +- {s:.2f}  z_SPA = {z(m,s,67.19,0.38):.2f}  z_SPT+ACT = {z(m,s,66.59,0.46):.2f}")
# GLS: SH0ES-side TRGB and SBF share NGC 4258 (1.45% in distance, as in M-EXAMINER-04)
import itertools
items = [LiTRGB, SBF, TF, TD, MAS, GW]
n = len(items)
C = [[(items[i][1]**2 if i == j else 0.0) for j in range(n)] for i in range(n)]
for i, j in ((0, 1), (1, 0)):
    C[i][j] = (0.0145*items[i][0])*(0.0145*items[j][0])
# invert 6x6 by Gauss-Jordan
A = [row[:] + [1.0 if i == k else 0.0 for k in range(n)] for i, row in enumerate(C)]
for c in range(n):
    p = max(range(c, n), key=lambda r: abs(A[r][c])); A[c], A[p] = A[p], A[c]
    pv = A[c][c]; A[c] = [v/pv for v in A[c]]
    for r in range(n):
        if r != c:
            f = A[r][c]; A[r] = [a - f*b for a, b in zip(A[r], A[c])]
Ci = [row[n:] for row in A]
w = [sum(Ci[i][j] for j in range(n)) for i in range(n)]
W = sum(w); m = sum(w[i]*items[i][0] for i in range(n))/W; s = W**-0.5
print(f"   GLS Cepheid-free (SH0ES-side TRGB, SBF share NGC 4258): {m:.2f} +- {s:.2f}  z_SPA = {z(m,s,67.19,0.38):.2f}  z_SPT+ACT = {z(m,s,66.59,0.46):.2f}")

print("\n[6] p-values of the candidate's band endpoints and of the computed range")
for zz in (3.0, 3.7, min(zs), max(zs), 5.0):
    print(f"   z = {zz:.2f}: two-sided p = {p2(zz):.2e}")
