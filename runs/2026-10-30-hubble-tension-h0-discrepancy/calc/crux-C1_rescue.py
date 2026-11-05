"""Crux C1: can C1 survive the SN-free attacks of verdicts C1-0/1/2, and what precision do the deciding tests need?

Units: H0 in km/s/Mpc (astronomical); magnitude offsets in mag on 5 log10 H0; sigma Gaussian-equivalent.
Inputs (all from dossier or verdicts):
  H0DN 73.264 [D-22]; CMB-SPA 67.19 [D-44]; BAO+BBN 68.50 [D-45]
  SN-minus-noSN offset +0.002 +- 0.047 (nested) / 0.0595 (indep) mag [verdicts C1-0, C1-2]
  Dong 2026 forward Pantheon+ 74.30 -> 71.37 [D-82]
  SBF 73.8 (0.7 stat, 2.3 sys) [D-29]; TF 73.3 (2.1, 3.5) [D-30]; SNe II 75.4 (-3.7 stat, 1.5 sys) [verdict C1-1]
  H0DN no-SN 73.434 +- 1.795 [D-23]; TD 71.1 (-2.3) [D-31]; masers 71.6 +- 3.7 [D-32]; sirens 71.7 (-7.5) [D-33]
"""
import math

def mag(a, b):
    return 5 * math.log10(a / b)

def ivw(vals):
    w = [1 / s**2 for _, s in vals]
    m = sum(v * wi for (v, _), wi in zip(vals, w)) / sum(w)
    return m, (1 / sum(w)) ** 0.5

def chi2(vals, T):
    return sum(((v - T) / s) ** 2 for v, s in vals)

H0DN, SPA, BBN = 73.264, 67.19, 68.50
off, s_nest, s_ind = 0.002, 0.047, 0.0595
dc = mag(74.30, 71.37)
print("1. Flow lever (c) size: %.4f mag (%.1f%% of the 0.188 mag gap)" % (dc, 100 * dc / mag(H0DN, SPA)))

hf = {  # Hubble-flow ladder tracers that a flow-treatment error would reach
    "SBF": (73.8, math.hypot(0.7, 2.3)),
    "TF": (73.3, math.hypot(2.1, 3.5)),
    "SNII": (75.4, math.hypot(3.7, 1.5)),
}
onestep = {"TD": (71.1, 2.3), "masers": (71.6, 3.7), "sirens": (71.7, 7.5)}

for T in (SPA, BBN):
    need = mag(H0DN, T)
    print("\n== truth T = %.2f km/s/Mpc; total ladder bias needed %.4f mag" % (T, need))
    # Scenario S1: SN-step only
    z1n = (need - off) / s_nest; z1i = (need - off) / s_ind
    setY = list(hf.values()) + list(onestep.values())
    m, s = ivw(setY)
    print("S1 SN-step only: SN-vs-noSN deficit %.2f sigma (nested) / %.2f (indep); "
          "SN-free set (SBF,TF,SNII,TD,masers,sirens, no corr.) %.2f +- %.2f, %.2f sigma above T; chi2/6 = %.2f"
          % (z1n, z1i, m, s, (m - T) / s, chi2(setY, T)))
    # Scenario S2: flow lever on every Hubble-flow tracer + SN step for the rest
    bsn = need - dc
    z2n = (bsn - off) / s_nest; z2i = (bsn - off) / s_ind
    hf_s = [(v / 10 ** (dc / 5), sg / 10 ** (dc / 5)) for v, sg in hf.values()]
    setY2 = hf_s + list(onestep.values())
    m2, s2 = ivw(setY2)
    mh, sh = ivw(hf_s)
    print("S2 flow (c) %.4f + SN step %.4f mag: SN-vs-noSN deficit %.2f sigma (nested) / %.2f (indep)"
          % (dc, bsn, z2n, z2i))
    print("   shifted SN-free ladders %.2f +- %.2f (%.2f sigma above T); SN-free set %.2f +- %.2f, %.2f sigma above T; chi2/6 = %.2f"
          % (mh, sh, (mh - T) / sh, m2, s2, (m2 - T) / s2, chi2(setY2, T)))
    # Alternative S2 with H0DN no-SN (contains SBF, masers) in place of SBF and masers
    setX2 = [(73.434 / 10 ** (dc / 5), 1.795 / 10 ** (dc / 5)), hf_s[1], hf_s[2], onestep["TD"], onestep["sirens"]]
    m3, s3 = ivw(setX2)
    print("   variant set (H0DN noSN, TF, SNII shifted; TD, sirens): %.2f +- %.2f, %.2f sigma above T"
          % (m3, s3, (m3 - T) / s3))

print("\n2. Precision needed for deciding tests (separation d at n sigma: sigma <= d/n)")
for name, a, b in [("C1 68.5 vs C3 71.0", 68.5, 71.0), ("C1 68.5 vs C3 73.26", 68.5, 73.26),
                   ("C1 68.5 vs C6 70.5", 68.5, 70.5), ("C1 68.5 vs C8 71.0", 68.5, 71.0),
                   ("C1 67.19 vs C6 70.5", 67.19, 70.5)]:
    d = b - a
    print("  %-22s d = %.2f km/s/Mpc: sigma <= %.2f (3 sigma), %.2f (5 sigma) km/s/Mpc; %.2f%% / %.2f%% of 70"
          % (name, d, d / 3, d / 5, 100 * d / 3 / 70, 100 * d / 5 / 70))
for name, d in [("C1 SN-step share (S2, T=68.5) vs C7 0", mag(H0DN, BBN) - dc),
                ("C1 SN-step only (T=68.5) vs C7 0", mag(H0DN, BBN)),
                ("C4(ii) step 0.146 vs C1 0", 0.146)]:
    print("  %-40s d = %.4f mag: sigma <= %.4f (3 sigma), %.4f (5 sigma) mag" % (name, d, d / 3, d / 5))
