"""Falsifier C3-1 (evidence angle): closure fractions and P(H0 > midpoint)
for pre-recombination (EDE-led) fits WITHOUT a ladder prior, plus r_d-free H0.

Units: H0 in km/s/Mpc throughout.
Gap convention (as in candidates.md): early = CMB-SPA LCDM 67.19 (Khalife+2025 p.2),
late = SH0ES 73.49 (dossier value used by the lenses). Alternative late = 73.17
(the SH0ES value Khalife+2025 quote). C3's own definition of "dominant":
true global H0 above the midpoint (~70.2-70.3).
Asymmetric errors: for P(H0 > m) use the upper error if m > central, else the lower.
"""
from math import erf, sqrt

def Phi(x):
    return 0.5 * (1 + erf(x / sqrt(2)))

early = 67.19
for late in (73.49, 73.17):
    mid = 0.5 * (early + late)
    print(f"\n=== gap {early} -> {late}: gap = {late-early:.2f} km/s/Mpc, midpoint = {mid:.2f}")
    fits = [
        # name, central, +err, -err, source
        ("EDE CMB-SPA (Planck+ACT+SPT), no BAO", 68.03, 0.53, 1.1, "Khalife+2025 Table II"),
        ("EDE SPT+ACT", 67.25, 0.47, 1.1, "Khalife+2025 Table II"),
        ("EDE CMB-SPA + DESI DR2", 69.81, 0.95, 1.2, "Khalife+2025 Table II"),
        ("EDE SPT + DESI DR2", 70.9, 1.3, 1.9, "Khalife+2025 Table II"),
        ("EDE Planck+BAO+eBOSS Lya", 67.9, 0.4, 0.4, "Goldstein+2023 abstract"),
        ("EDE P-ACT-LB (ACT DR6)", 69.9, 0.8, 1.5, "D-52"),
        ("EDE Poulin 2026 profile", 71.0, 1.1, 1.1, "D-53"),
        ("EDE eROSITA + external", 71.4, 1.4, 1.4, "D-94"),
        ("Mod. recombination P-ACT-LB", 69.6, 1.0, 1.0, "D-52"),
        ("PMF P-ACT-LB", 69.1, 0.5, 0.5, "D-52"),
        ("r_d-free DESI: CMBlens x unWISE", 69.2, 1.3, 1.4, "D-49 Zaborowski 2026"),
        ("r_d-free DESI: DES Y3 6x2pt", 70.3, 1.4, 1.2, "D-49 Zaborowski 2026"),
        ("r_d-free DESI: lens + DES Y5 SN", 69.6, 1.3, 1.8, "D-49 Zaborowski 2026"),
    ]
    print(f"{'fit':40s} {'H0':>6s} {'closure':>8s} {'P(H0>mid)':>10s} {'tens vs late (sigma)':>20s}  source")
    for name, c, up, lo, src in fits:
        clos = (c - early) / (late - early)
        s = up if mid > c else lo
        p_above = 1 - Phi((mid - c) / s)
        # tension with SH0ES using facing-side error (SH0ES err 0.93 for 73.49, 0.86 for 73.17)
        se = 0.93 if late == 73.49 else 0.86
        t = (late - c) / sqrt(up**2 + se**2)
        print(f"{name:40s} {c:6.2f} {clos:8.2f} {p_above:10.3f} {t:20.2f}  {src}")

# Lya vs C3's needed f_EDE: the candidate needs f=0.124-0.188 for background closure,
# and its own 'tightest bound' partial case uses f=0.06-0.07.
print("\nLya bound f_EDE < 0.03 (95%, Goldstein+2023) vs C3 needs:")
for f in (0.06, 0.07, 0.09, 0.124, 0.137, 0.188):
    print(f"  f_EDE needed {f:.3f} = {f/0.03:.1f} x the Lya 95% upper limit")
