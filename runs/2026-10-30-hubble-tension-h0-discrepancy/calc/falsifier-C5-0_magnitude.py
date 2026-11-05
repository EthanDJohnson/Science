#!/usr/bin/env python3
"""Falsifier C5-0 (magnitude): can local structure (void or bulk flow) carry MOST (>= 50%) of the H0 gap?
Units: H0 in km/s/Mpc; distances Mpc or h^-1 Mpc as labelled; magnitudes mag; velocities km/s.
Inputs (dossier): H0DN 73.264 +- 0.806 (D-22), H0DN original baseline 73.50 +- 0.81 (D-22), variant 0.03<z<0.10
72.667 +- 0.862 (D-23), CMB-SPA 67.19 +- 0.38, Om 0.3175 (D-44), BAO+BBN 68.50 +- 0.58 (D-45), LCDM sigma(H0_loc)
0.31 (D-10), SN Hubble-diagram bound |delta| < 0.20 at 4-5 sigma (D-11, Kenworthy 2019), SN Om 0.322 +- 0.012 (cands).
Sections:
 A  required void contrast for 50% and 100% of the gap
 B  largest share of the gap allowed by (i) LCDM cosmic variance (ii) the SN-diagram |delta|<0.2 bound
 C  bulk flow: monopole bias of a dipole flow on a SN sample; velocity needed; LCDM rms bulk flow (EH98 P(k))
 D  z_min trend predicted by a linear-theory void that carries the full gap, vs the H0DN 0.03-0.10 variant
 E  can a smooth flat-LCDM shape absorb the void's magnitude step?  best-fit Om and residual chi2 on a mock grid
"""
import math
import numpy as np

c = 299792.458
H_loc, H_cmb, H_bao = 73.264, 67.19, 68.50
Om, h = 0.3175, 0.6719
f = Om ** 0.55


def dHH_lin(d):
    return -f * d / 3


def dHH_bern(d):
    return (f / 2) * (1 - (1 + d) ** (2 / 3))


def d_for_lin(x):
    return -3 * x / f


def d_for_bern(x):
    return (1 - 2 * x / f) ** 1.5 - 1


print("=== A: required contrast ===")
for name, Hg in (("CMB-SPA", H_cmb), ("BAO+BBN", H_bao)):
    gap = H_loc - Hg
    for share in (0.5, 1.0):
        x = (Hg + share * gap) / Hg - 1
        print(f"{name}: gap {gap:.3f} km/s/Mpc; share {share:.0%}: dH/H = {100*x:.2f}% -> delta_lin = {d_for_lin(x):.3f},"
              f" delta_Bern = {d_for_bern(x):.3f}")

print("\n=== B: largest allowed share ===")
for d in (-0.20, -0.27):
    for lab, fn in (("lin", dHH_lin), ("Bern", dHH_bern)):
        x = fn(d)
        print(f"delta = {d:+.2f} ({lab}): dH/H = {100*x:.2f}%; dH = {H_cmb*x:.2f} (vs CMB-SPA, share {H_cmb*x/(H_loc-H_cmb):.0%}),"
              f" {H_bao*x:.2f} (vs BAO+BBN, share {H_bao*x/(H_loc-H_bao):.0%}); SN-diagram step {5*math.log10(1+x):.3f} mag")
for k in (2, 3, 5):
    print(f"LCDM {k} sigma local fluctuation = {k*0.31:.2f} km/s/Mpc = {k*0.31/(H_loc-H_cmb):.0%} of CMB-SPA gap,"
          f" {k*0.31/(H_loc-H_bao):.0%} of BAO+BBN gap")
print(f"half-gap in LCDM-variance units: CMB-SPA {(H_loc-H_cmb)/2/0.31:.1f} sigma, BAO+BBN {(H_loc-H_bao)/2/0.31:.1f} sigma")

# ---- mock Hubble-flow sample (ASSUMPTION: Pantheon+-like N(z) ~ z^2 /(1+(z/0.06)^3) on 0.023-0.15, isotropic sky)
rng = np.random.default_rng(1)
zg = np.linspace(0.0233, 0.15, 20000)
pz = zg**2 / (1 + (zg / 0.06) ** 3)
pz /= pz.sum()
N = 277
sig_int = 0.13


def w_of(z):
    sv = 5 / math.log(10) * 250.0 / (c * z)
    return 1 / (sig_int**2 + sv**2)


print("\n=== C: bulk flow ===")
for trial in range(2):
    z = rng.choice(zg, size=200000, p=pz)
    w = w_of(z)
    mu = rng.uniform(-1, 1, z.size)                 # cos angle to flow, isotropic
    for V in (400.0, 1000.0):
        # each SN: cz_obs = H r + V mu -> log H_i = log H + log(1 + V mu/(c z_cos)); estimator = weighted mean of log H_i
        bias_iso = np.sum(w * np.log1p(V * mu / (c * z))) / np.sum(w)
        hemi = mu > 0
        bias_hemi = np.sum(w[hemi] * np.log1p(V * mu[hemi] / (c * z[hemi]))) / np.sum(w[hemi])
        print(f"trial {trial}: V = {V:.0f} km/s: isotropic-sky bias {100*bias_iso:+.3f}%, one-hemisphere (worst) bias {100*bias_hemi:+.2f}%")
zz = rng.choice(zg, size=200000, p=pz)
ww = w_of(zz)
m1 = np.sum(ww * 0.5 / (c * zz)) / np.sum(ww)    # <mu>=1/2 on hemisphere
need = 0.0904 / m1
print(f"worst-case hemisphere needs V = {need:.0f} km/s for the full 9.04%; {0.5*need:.0f} km/s for half the gap")

# LCDM rms bulk flow in a top-hat sphere (linear theory), EH98 no-wiggle as in lens script, sigma8 0.8137
ob, s8, ns = 0.02237, 0.8137, 0.9679
om = Om * h * h
fb = ob / om
theta = 2.7255 / 2.7


def T_nw(k_h):
    s = 44.5 * math.log(9.83 / om) / math.sqrt(1 + 10 * ob**0.75)
    aG = 1 - 0.328 * math.log(431 * om) * fb + 0.38 * math.log(22.3 * om) * fb**2
    k = k_h * h
    Geff = Om * h * (aG + (1 - aG) / (1 + (0.43 * k * s) ** 4))
    q = k_h * theta**2 / Geff
    L0 = np.log(2 * math.e + 1.8 * q)
    C0 = 14.2 + 731 / (1 + 62.5 * q)
    return L0 / (L0 + C0 * q * q)


def W(x):
    return 3 * (np.sin(x) - x * np.cos(x)) / x**3


for n in (4000, 8000):
    lk = np.linspace(math.log(1e-5), math.log(50.0), n)
    k = np.exp(lk)
    P0 = k**ns * T_nw(k) ** 2
    A = s8**2 / (np.trapezoid(k**3 * P0 * W(k * 8.0) ** 2, lk) / (2 * math.pi**2))
    out = []
    for R in (50, 100, 150, 300):
        # sigma_v^2 = (f H)^2/(2 pi^2) int P(k) W^2 dk ; H = 100 km/s/(h^-1 Mpc), P in (h^-1 Mpc)^3
        sv2 = (f * 100.0) ** 2 / (2 * math.pi**2) * np.trapezoid(k * A * P0 * W(k * R) ** 2, lk)
        out.append(f"R={R}: {math.sqrt(sv2):.0f}")
    print(f"n={n}: LCDM 3D rms bulk flow (km/s) " + ", ".join(out))

print("\n=== D: z_min trend for a full-gap linear-theory void ===")
# top-hat void radius R (edge redshift zR, global H); inside dH/H = x0; outside x0 (R/r)^3 (linear, uncompensated)
z = rng.choice(zg, size=400000, p=pz)
w = w_of(z)


def H_est(x0, zR, sel):
    r = z  # comoving distance ~ cz/H at these z (fractional accuracy enough for profile)
    x = np.where(r < zR, x0, x0 * (zR / r) ** 3)
    return H_cmb * math.exp(np.sum(w[sel] * np.log1p(x[sel])) / np.sum(w[sel]))


full = np.ones(z.size, bool)
s1 = (z > 0.03) & (z < 0.10)
s2 = z > 0.06
s3 = z < 0.06
for zR in (0.05, 0.07, 0.10, 0.15, 0.20):
    lo, hi = 0.0, 0.5
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if H_est(mid, zR, full) < H_loc:
            lo = mid
        else:
            hi = mid
    x0 = 0.5 * (lo + hi)
    Hf, H1, H2, H3 = (H_est(x0, zR, s) for s in (full, s1, s2, s3))
    print(f"edge z={zR:.2f}: needs inner dH/H={100*x0:.1f}% (delta_lin={d_for_lin(x0):.2f}); H0 full {Hf:.2f},"
          f" 0.03-0.10 {H1:.2f} (shift {H1-Hf:+.2f}), z>0.06 {H2:.2f} (shift {H2-Hf:+.2f}), z<0.06 {H3:.2f}")
print(f"observed (D-23, original baseline 73.50): 0.03-0.10 shift {72.667-73.50:+.3f}; 'z>0.06' shift {73.190-73.50:+.3f};"
      f" nested-subsample sigma of the shift ~ sqrt(0.862^2-0.81^2) = {math.sqrt(0.862**2-0.81**2):.2f}")

print("\n=== E: can a smooth flat-LCDM shape absorb the void step? ===")


def dL(zarr, Om_):
    out = []
    for zi in zarr:
        zz_ = np.linspace(0, zi, 400)
        Ez = np.sqrt(Om_ * (1 + zz_) ** 3 + 1 - Om_)
        out.append((1 + zi) * np.trapezoid(1 / Ez, zz_))
    return np.array(out)


# mock SNe: 300 in 0.023-0.15 (sample), 400 in 0.15-0.5, 300 in 0.5-1.0; sigma 0.15 mag each (ASSUMPTION)
zs = np.concatenate([rng.choice(zg, 300, p=pz), rng.uniform(0.15, 0.5, 400), rng.uniform(0.5, 1.0, 300)])
sig = 0.15
mu_true = 5 * np.log10(dL(zs, Om))
for zR in (0.15, 0.20):
    x0 = 0.0904
    x = np.where(zs < zR, x0, x0 * (zR / zs) ** 3)
    mu_void = mu_true - 5 * np.log10(1 + x)      # local H higher -> closer -> fainter mu smaller
    best = None
    for Om_ in np.linspace(0.0, 1.0, 201):
        m = 5 * np.log10(dL(zs, Om_))
        off = np.mean(mu_void - m)               # free M_B / H0 offset
        chi2 = np.sum(((mu_void - m - off) / sig) ** 2)
        if best is None or chi2 < best[1]:
            best = (Om_, chi2)
    print(f"void edge z={zR:.2f}, step {5*math.log10(1+x0):.3f} mag: best smooth flat-LCDM Om = {best[0]:.3f},"
          f" residual chi2 = {best[1]:.1f} for 1000 SNe (noise-free mock; = detection Delta-chi2), ~{math.sqrt(best[1]):.1f} sigma")
print("observed SN-only Om = 0.322 +- 0.012 (candidates.md matrix); CMB-SPA Om 0.3175")
