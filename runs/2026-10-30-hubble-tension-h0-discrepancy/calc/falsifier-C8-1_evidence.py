"""Falsifier C8-1 (evidence angle): how robust is the 'team-independent ~4 km/s/Mpc at ~3-3.7 sigma' to
which non-SH0ES results count as team-independent, and do any sourced non-SH0ES-data routes reach >= 5 sigma?
Units: H0 in km/s/Mpc (astronomical units, not SI). Errors Gaussian, symmetrised where asymmetric, independent
unless stated. z = |dH| / sqrt(s1^2 + s2^2); two-sided.
Inputs are dossier values (D-20..D-33, D-23, D-44, D-45, D-41) and two abstracts fetched in this verdict:
Stiskalek et al. arXiv:2509.09665 (71.1 +- 1.4, SH0ES Cepheid data, no SNe) and
TDCOSMO arXiv:2610.14881 (no-SN 3.7 sigma vs Planck; no-ladder 2.7 sigma)."""
import math

def quad(*a):
    return math.sqrt(sum(x * x for x in a))

def ivmean(items):
    w = [1 / s ** 2 for _, s in items]
    m = sum(x * wi for (x, _), wi in zip(items, w)) / sum(w)
    return m, 1 / math.sqrt(sum(w))

def z(a, sa, b, sb):
    return (a - b) / math.sqrt(sa ** 2 + sb ** 2)

early = {"CMB-SPA": (67.19, 0.38), "Planck PR4": (67.64, 0.52), "BAO+BBN": (68.50, 0.58)}

CCHP = ("CCHP TRGB 70.39", (70.39, quad(1.22, 1.33, 0.70)))
CCHPJ = ("CCHP JWST-only 68.81", (68.81, 1.80))
SBF = ("SBF 73.8", (73.8, quad(0.7, 2.3)))
TF = ("TF CF4 73.3 (Cepheid/TRGB zero points)", (73.3, quad(2.1, 3.5)))
TD = ("TDCOSMO-2026 71.1", (71.1, 2.35))
MAS = ("Masers 71.6", (71.6, 3.7))
SIR = ("Sirens 71.7", (71.7, 8.45))

sets = {
    "A: lens set (CCHP,SBF,TF,TD,masers,sirens)": [CCHP, SBF, TF, TD, MAS, SIR],
    "B: drop TF (zero point via SH0ES-type Cepheids)": [CCHP, SBF, TD, MAS, SIR],
    "C: B with CCHP JWST-only instead of CCHP": [CCHPJ, SBF, TD, MAS, SIR],
    "D: one-step only (TD,masers,sirens)": [TD, MAS, SIR],
    "E: B plus Stiskalek Cepheid-only 71.1+-1.4 (SH0ES data, other team)": [CCHP, SBF, TD, MAS, SIR, ("Stiskalek", (71.1, 1.4))],
}
print("Non-SH0ES local combinations (inverse-variance, independent):")
for name, items in sets.items():
    m, s = ivmean([v for _, v in items])
    out = ", ".join(f"vs {k}: d={m - e[0]:+.2f}, z={z(m, s, *e):.2f}" for k, e in early.items())
    print(f"  {name}: {m:.2f} +- {s:.2f} | {out}")

print("\nSingle routes vs CMB-SPA 67.19 +- 0.38 (H0DN variants from D-23, original Pantheon+):")
singles = {
    "SH0ES 73.49 +- 0.93": (73.49, 0.93),
    "H0DN V08 no Cepheids 72.509 +- 1.296": (72.509, 1.296),
    "H0DN V08B custom baseline (same 35 SN calibrators) 72.873 +- 0.874": (72.873, 0.874),
    "H0DN V13 no SNe Ia 73.434 +- 1.795": (73.434, 1.795),
    "Stiskalek 2026 Cepheids-only, no SNe 71.1 +- 1.4": (71.1, 1.4),
    "SH0ES-side TRGB (Li 2026) 72.7 +- 1.8 (mid of 72.1-73.3)": (72.7, 1.8),
}
for k, (a, sa) in singles.items():
    print(f"  {k}: z_SPA = {z(a, sa, 67.19, 0.38):.2f}, z_PR4 = {z(a, sa, 67.64, 0.52):.2f}, z_BAO = {z(a, sa, 68.50, 0.58):.2f}")

print("\nPrecision a non-SH0ES local mean at 71.5 would need for 5 sigma vs CMB-SPA:")
d = 71.5 - 67.19
need = math.sqrt((d / 5) ** 2 - 0.38 ** 2)
print(f"  sigma_local <= {need:.3f} km/s/Mpc ({100 * need / 71.5:.2f}%)")
print("\nFreedman 2025 3.0 sigma check (their own construction: R22 74.03-2.00, sigma 1.44 vs Planck 67.4+-0.5):")
print(f"  z = {z(72.03, 1.44, 67.4, 0.5):.2f}")
