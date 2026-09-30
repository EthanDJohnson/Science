"""Falsifier C3-2 (bounds angle): does an invisible ~1.1% dark branch survive the independent
constraints on tau_beta = 1/Gamma(n -> p e nu) that do NOT use proton counting?

Units: lifetimes in s (SI); lambda, Vud, branching ratios dimensionless.
Inputs: dossier values as transcribed in math/constraints/_common.py (D-20, D-23, D-27, D-40..D-49),
statistician reference combinations quoted in candidates.md.

Under C3: storage measures tau_n; proton beam, J-PARC (electron counting) and the SM master formula
all measure tau_beta = tau_n / (1 - Br_X).
"""
import math
from scipy import stats

K = 5024.46          # s, master-formula constant (D-49)
VUD, S_VUD = 0.97361, 0.00032
DRV = 0.02479
S_RC = 0.19          # s


def tau_beta(lam):
    return K / (VUD**2 * (1 + 3 * lam**2) * (1 + DRV))


def sig_tau_beta(lam, slam):
    t = tau_beta(lam)
    return math.sqrt((t * 6 * lam / (1 + 3 * lam**2) * slam) ** 2 + (2 * t / VUD * S_VUD) ** 2 + S_RC**2)


def wmean(vals):
    w = [1 / s**2 for _, s in vals]
    m = sum(wi * x for wi, (x, _) in zip(w, vals)) / sum(w)
    chi2 = sum(wi * (x - m) ** 2 for wi, (x, _) in zip(w, vals))
    return m, 1 / math.sqrt(sum(w)), chi2


def z_to_p2(z):
    return 2 * stats.norm.sf(abs(z))


LAM = {
    "PERKEO III": (1.27641, math.hypot(0.00045, 0.00033)),
    "UCNA": (1.2772, 0.0020),
    "PERKEO II": (1.2748, math.hypot(0.0008, 0.00105)),
    "aSPECT 2024": (1.2668, 0.0027),
    "aCORN": (1.2796, 0.0062),
}

# lifetimes
BEAM, S_BEAM = 887.97, 2.04            # proton-counting class (statistician)
BL1, S_BL1 = 887.7, math.hypot(1.2, 1.9)
STORE, S_STORE = 878.32, 0.43          # all storage, S-scaled (statistician)
UCNT, S_UCNT = 877.82, 0.30
JP, JP_UP, JP_DN = 877.2, math.hypot(1.7, 4.0), math.hypot(1.7, 3.6)
JP_UP_S = math.hypot(1.7 * 2.29, 4.0)  # stat inflated by S = 2.29 (four run conditions)

print("=== 1. World lambda average (aSPECT 2020 superseded by 2024; PDG-style scale factor) ===")
vals = list(LAM.values())
m, s, chi2 = wmean(vals)
N = len(vals)
S = max(1.0, math.sqrt(chi2 / (N - 1)))
print(f"|lambda| = {m:.5f} +- {s:.5f} (unscaled), chi2 = {chi2:.2f}/{N-1}, S = {S:.2f}, scaled sigma = {s*S:.5f}")
lam_scenarios = {
    "PERKEO III alone": LAM["PERKEO III"],
    "world avg, scaled": (m, s * S),
    "world avg, S inflated x2 more (S*2)": (m, s * S * 2),
    "aSPECT 2024 alone (C3 escape C-a)": LAM["aSPECT 2024"],
}

print("\n=== 2. Non-proton tau_beta routes vs the C3 requirement (tau_beta = beam value) ===")
print(f"C3 needs tau_beta = proton-beam class {BEAM} +- {S_BEAM} s; needed Br_X vs storage = "
      f"{100*(1-STORE/BEAM):.3f}% ; vs UCNtau = {100*(1-UCNT/BEAM):.3f}%")
rows = {}
for name, (lam, sl) in lam_scenarios.items():
    tb, stb = tau_beta(lam), sig_tau_beta(lam, sl)
    br = 1 - STORE / tb
    sbr = (STORE / tb) * math.hypot(S_STORE / STORE, stb / tb)
    ul = br + 1.645 * sbr
    need = 1 - STORE / BEAM
    z_need = (need - br) / sbr
    z_beam = (BEAM - tb) / math.hypot(S_BEAM, stb)
    rows[name] = (tb, stb)
    print(f"[{name}] tau_beta(SM) = {tb:.2f} +- {stb:.2f} s; Br_X = {100*br:.3f} +- {100*sbr:.3f}% ; "
          f"95% UL = {100*ul:.3f}% ; needed value at {z_need:.2f} sigma ; SM vs beam {z_beam:.2f} sigma")

print("\n=== 3. J-PARC (electron counting) as an independent tau_beta measurement ===")
for lab, up in (("as quoted", JP_UP), ("stat scaled S=2.29", JP_UP_S)):
    br = 1 - STORE / JP
    sbr = (STORE / JP) * math.hypot(S_STORE / STORE, up / JP)
    need = 1 - STORE / BEAM
    print(f"[{lab}] Br_X(J-PARC) = {100*br:.3f} +- {100*sbr:.3f}% (upper-side err); 95% UL {100*(br+1.645*sbr):.3f}%;"
          f" needed {100*need:.3f}% at {(need-br)/sbr:.2f} sigma ; J-PARC vs beam {(BEAM-JP)/math.hypot(S_BEAM, up):.2f} sigma")

print("\n=== 4. Joint C3 goodness of fit: three tau_beta measurements (beam, J-PARC, SM) must agree ===")
print("   (storage then fixes tau_n and Br_X; 2 dof test of the C3 pattern)")
for lname in ("PERKEO III alone", "world avg, scaled", "world avg, S inflated x2 more (S*2)", "aSPECT 2024 alone (C3 escape C-a)"):
    tb, stb = rows[lname]
    for jlab, jup in (("J-PARC quoted", JP_UP), ("J-PARC scaled", JP_UP_S)):
        # J-PARC sits below every candidate tau_beta, so the upper error applies
        data = [(BEAM, S_BEAM), (JP, jup), (tb, stb)]
        mm, ss, c2 = wmean(data)
        # re-check side of J-PARC error
        p = stats.chi2.sf(c2, 2)
        zeq = stats.norm.isf(p / 2)
        print(f"[{lname} | {jlab}] common tau_beta = {mm:.2f} +- {ss:.2f} s ; chi2 = {c2:.2f}/2 ; p = {p:.2e} ; ~{zeq:.2f} sigma ;"
              f" implied Br_X = {100*(1-STORE/mm):.3f}%")

print("\n=== 5. Same pattern for C1 (proton beam biased; tau_beta = tau_n): storage, J-PARC, SM must agree ===")
for lname in ("PERKEO III alone", "world avg, scaled", "aSPECT 2024 alone (C3 escape C-a)"):
    tb, stb = rows[lname]
    # J-PARC below storage => its upper error; SM above storage => nothing asymmetric
    data = [(STORE, S_STORE), (JP, JP_UP), (tb, stb)]
    mm, ss, c2 = wmean(data)
    p = stats.chi2.sf(c2, 2)
    print(f"[C1 | {lname}] chi2 = {c2:.2f}/2 ; p = {p:.2e}")

print("\n=== 6. Combined non-proton exclusion of Br_X = needed (Stouffer, independent J-PARC + SM route) ===")
need = 1 - STORE / BEAM
for lname in ("PERKEO III alone", "world avg, scaled", "world avg, S inflated x2 more (S*2)", "aSPECT 2024 alone (C3 escape C-a)"):
    tb, stb = rows[lname]
    # inverse-variance combine the two non-proton tau_beta determinations
    for jlab, jup in (("J-PARC quoted", JP_UP), ("J-PARC scaled", JP_UP_S)):
        mm, ss, c2 = wmean([(JP, jup), (tb, stb)])
        br = 1 - STORE / mm
        sbr = (STORE / mm) * math.hypot(S_STORE / STORE, ss / mm)
        print(f"[{lname} | {jlab}] non-proton tau_beta = {mm:.2f} +- {ss:.2f} s (internal chi2 {c2:.2f}/1);"
              f" Br_X = {100*br:.3f} +- {100*sbr:.3f}% ; 95% UL {100*(br+1.645*sbr):.3f}% ; needed {100*need:.3f}% at {(need-br)/sbr:.2f} sigma")

print("\n=== 7. Vud shift toward unitarity (Cabibbo deficit) moves the bound which way? ===")
for dv in (0.0, 0.0005, 0.0009):
    v = VUD + dv
    tb = K / (v**2 * (1 + 3 * m**2) * (1 + DRV))
    print(f"Vud = {v:.5f}: tau_beta(world lambda) = {tb:.2f} s ; Br_X = {100*(1-STORE/tb):.3f}%")

print("\n=== 8. Fierz escape C-b: couplings needed for b_n = -0.0158 vs LHC (SMEFT) bounds ===")
# b_n = 0.35 eps_S - 5.15 eps_T  (Gonzalez-Alonso, Naviliat-Cuncic, Severijns 2019, eq. 38)
# LHC pp -> e + MET 90% CL: |eps_S| < 5.8e-3, |eps_T| < 1.3e-3 (same review, eqs. 121-122)
b_need = (878.50 / 887.7 - 1) / 0.6555
eT = -b_need / 5.15
eS = b_need / 0.35
print(f"b_n needed = {b_need:.4f}")
print(f"tensor only: eps_T = {eT:.3e}  -> {abs(eT)/1.3e-3:.2f} x LHC 90% bound 1.3e-3")
print(f"scalar only: eps_S = {eS:.3e}  -> {abs(eS)/5.8e-3:.2f} x LHC 90% bound 5.8e-3")
