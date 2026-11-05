"""Falsifier C6-0 (magnitude angle): can the null 'no single dominant cause' carry the
whole local-vs-early gap with every contribution below half, and how much of the
allowed parameter space / posterior does that leave?

Units: H0 in km/s/Mpc (astronomical units, not SI); magnitudes in mag.
Inputs (dossier IDs): H0DN-corrected 73.264 +- 0.806 [D-22]; SH0ES 73.49 +- 0.93 [D-20];
CMB-SPA 67.19 +- 0.38 [D-44]; BAO+BBN 68.50 +- 0.58 [D-45]; one-step: TDCOSMO-2026
71.1 +2.4/-2.3 [D-31], masers 71.6 +- 3.7 [D-32], sirens 71.7 +9.4/-7.5 [D-33];
r_s-free 69.6 +1.3/-1.8 (lens + DES Y5) [D-49]; CCHP 70.39 +- 1.94 [D-24];
SBF 73.8 +- 2.40 [D-29]; TF 73.3 +- 4.08 [D-30]; EDE fits without ladder prior [D-52, D-53, D-94].
Boundary rule from candidates.md: a cause is dominant if it carries > half the gap.
"""
import math
import numpy as np
from scipy.stats import norm

XL, sL = 73.264, 0.806      # ladder (H0DN corrected)
XS, sS = 73.49, 0.93        # SH0ES alone
XE, sE = 67.19, 0.38        # CMB-SPA
D = XL - XE
DS = XS - XE
mid = 0.5 * (XL + XE)
sig_tot = math.hypot(sL, sE)
print("=== 1. Gap and boundary ===")
print(f"gap H0DN-SPA = {D:.3f} km/s/Mpc ({5*math.log10(XL/XE):.4f} mag); half = {D/2:.3f}; midpoint = {mid:.3f}")
print(f"gap SH0ES-SPA = {DS:.3f} km/s/Mpc; half = {DS/2:.3f}")
print(f"combined measurement sigma = {sig_tot:.3f} km/s/Mpc -> pure fluctuation = {D/sig_tot:.2f} sigma")

print("\n=== 2. C6(a) stated true-H0 range 69-71: share of gap carried by each side (no fluctuation) ===")
for H in [69.0, 69.5, 70.0, 70.23, 70.5, 71.0]:
    lad = (XL - H) / D
    ear = (H - XE) / D
    tag = "C1 (ladder >1/2)" if lad > 0.5 else ("early >1/2 (C2/C3)" if ear > 0.5 else "balanced")
    print(f" H_true={H:6.2f}: ladder share {lad:5.1%}, early share {ear:5.1%} -> {tag}")

print("\n=== 3. Window of true H0 where neither side exceeds half, given a fluctuation share ===")
# observed ladder = H + L + nL (nL>=0 helps), observed early = H - E + nE (nE<=0 helps)
# L<=D/2 -> H >= XL - nL - D/2 = mid - nL ; E<=D/2 -> H <= XE + nE' + D/2 with nE'=|nE| -> mid + |nE|
for k in [0.5, 1.0, 1.5, 2.0]:
    nL, nE = k * sL, k * sE
    lo, hi = mid - nL, mid + nE
    # joint two-sided probability of both fluctuating at least k sigma in the helpful directions
    p = norm.sf(k) ** 2
    print(f" k={k:.1f} sigma each: window [{lo:.2f}, {hi:.2f}] width {hi-lo:.2f} km/s/Mpc; "
          f"P(both >= k sigma helpful) = {p:.3g}")
# fraction of stated 69-71 range inside the 1-sigma and 2-sigma windows
for k in [1.0, 2.0]:
    lo, hi = mid - k * sL, mid + k * sE
    ov = max(0.0, min(hi, 71.0) - max(lo, 69.0))
    print(f" fraction of the stated 69-71 range inside the {k:.0f}-sigma window: {ov/2.0:.1%}")

print("\n=== 4. C6(a) cited part sizes: do they reach the gap with none > half? ===")
lad_rng = (1.0, 3.0)
ear_rng = (1.5, 3.0)
for L in [1.0, 2.0, 2.5, 3.0]:
    for E in [1.5, 2.0, 2.5, 3.0]:
        f = D - L - E
        print(f" L={L:.1f} ({L/D:4.0%}) E={E:.1f} ({E/D:4.0%}) -> fluctuation needed {f:5.2f} km/s/Mpc"
              f" = {f/sig_tot:4.2f} sigma_tot ({f/D:4.0%} of gap)")
print(f" max L+E from cited ranges = {lad_rng[1]+ear_rng[1]:.2f} vs gap {D:.3f}; DESI Omega_m offset 1.3 is ~{1.3/D:.0%}")

print("\n=== 5. Early part as EDE without ladder prior: share of gap closed ===")
for name, H in [("ACT P-ACT EDE", 69.3), ("ACT P-ACT-LB EDE", 69.9), ("PMF (ACT)", 69.1),
                ("mod. recomb. (ACT)", 69.6), ("Planck NPIPE EDE 95% upper H0", 69.5),
                ("Poulin 2026 profile", 71.0), ("eROSITA+ext", 71.4)]:
    sh = (H - XE) / D
    print(f" {name:30s} H={H:5.1f}: closes {sh:5.1%} -> {'> half: C3 dominant' if sh > 0.5 else '<= half'}")

print("\n=== 6. Posterior on true H0 from SH0ES-independent, r_d-independent probes; P(region) ===")
def wmean(vals):
    w = np.array([1/s**2 for _, s in vals]); x = np.array([v for v, _ in vals])
    m = (w*x).sum()/w.sum(); s = w.sum()**-0.5
    chi2 = (w*(x-m)**2).sum()
    return m, s, chi2
onestep = [(71.1, 2.35), (71.6, 3.7), (71.7, 8.45)]
rsfree = [(69.6, 1.55)]
nonsh = [(70.39, 1.936), (73.8, 2.40), (73.3, 4.08)]
sets = {"A one-step": onestep, "B one-step + r_s-free": onestep + rsfree,
        "C B + CCHP + SBF + TF": onestep + rsfree + nonsh}

def p_balanced_given_H(H, XL=XL, sL=sL, XE=XE, sE=sE, D=D):
    # flat prior on L>=0 and E>=0; Gaussian measurement noise
    RL = XL - H; RE = H - XE
    # L = RL - nL, need 0 <= L <= D/2  <=> RL - D/2 <= nL <= RL
    den_L = norm.cdf(RL / sL)
    pL = (norm.cdf(RL / sL) - norm.cdf((RL - D/2) / sL)) / den_L if den_L > 0 else 0.0
    # E = RE + nE, need 0 <= E <= D/2 <=> -RE <= nE <= D/2 - RE
    den_E = norm.sf(-RE / sE)
    pE = (norm.cdf((D/2 - RE) / sE) - norm.cdf(-RE / sE)) / den_E if den_E > 0 else 0.0
    return pL, pE

Hgrid = np.linspace(60, 80, 8001)
for name, vals in sets.items():
    m, s, chi2 = wmean(vals)
    post = norm.pdf(Hgrid, m, s); post /= np.trapezoid(post, Hgrid)
    pb = np.array([np.prod(p_balanced_given_H(h)) for h in Hgrid])
    pLonly = np.array([1 - p_balanced_given_H(h)[0] for h in Hgrid])  # ladder > half
    pEonly = np.array([1 - p_balanced_given_H(h)[1] for h in Hgrid])  # early > half
    P6 = np.trapezoid(post * pb, Hgrid)
    P1 = np.trapezoid(post * pLonly, Hgrid)
    P3 = np.trapezoid(post * pEonly, Hgrid)
    print(f" {name:24s}: H = {m:.2f} +- {s:.2f} (chi2 {chi2:.2f}/{len(vals)-1});"
          f" P(balanced, C6) = {P6:.3f}; P(ladder>1/2) = {P1:.3f}; P(early>1/2) = {P3:.3f}")
print(" max over H of P(balanced|H):", f"{pb.max():.3f} at H = {Hgrid[pb.argmax()]:.2f}")
# limit check: if measurement noise -> 0 the balanced set shrinks to the midpoint
pl, pe = p_balanced_given_H(mid, sL=1e-6, sE=1e-6)
print(f" limit sigma->0 at the midpoint: pL={pl:.3f}, pE={pe:.3f} (expect 0.5, 0.5)")
pl, pe = p_balanced_given_H(mid - 1.0, sL=1e-6, sE=1e-6)
print(f" limit sigma->0 at midpoint-1: pL={pl:.3f}, pE={pe:.3f} (expect 0, 1)")

print("\n=== 6b. Decisive-test band check: the candidate's 70-71 band vs the balanced window ===")
lo1, hi1 = mid - sL, mid + sE
for H in [70.0, 70.5, 71.0]:
    pl, pe = p_balanced_given_H(H)
    print(f" true H={H:.1f}: P(ladder<=1/2)={pl:.3f}, P(early<=1/2)={pe:.3f}, P(balanced)={pl*pe:.3f}")
w = hi1 - lo1
print(f" 1-sigma balanced window width {w:.2f}; sigma needed to place an aggregate inside it at +-2 sigma: {w/4:.2f} km/s/Mpc ({w/4/mid:.2%})")

print("\n=== 7. Same with SH0ES alone as the ladder pole ===")
midS = 0.5 * (XS + XE)
for name, vals in sets.items():
    m, s, _ = wmean(vals)
    post = norm.pdf(Hgrid, m, s); post /= np.trapezoid(post, Hgrid)
    pb = np.array([np.prod(p_balanced_given_H(h, XL=XS, sL=sS, D=DS)) for h in Hgrid])
    print(f" {name:24s}: midpoint {midS:.2f}; P(balanced, C6) = {np.trapezoid(post*pb, Hgrid):.3f}")
