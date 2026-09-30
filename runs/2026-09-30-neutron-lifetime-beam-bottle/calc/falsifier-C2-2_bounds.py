"""Falsifier C2-2 (bounds angle): does the proton-beam value ~888 s survive the
independent, storage-free determinations of tau_beta (J-PARC electron counting,
SM master formula from lambda and Vud), and is a single common loss rate
consistent across material and magnetic traps?

Units: SI (lifetimes in s, rates in s^-1). Inputs from dossier / verified math checks:
  proton beam 887.97 +- 2.04 s (M-STATISTICIAN-01); BL1 887.7 +- 2.25 s (D-20)
  J-PARC 877.2 +4.35/-3.98 s (D-23, stat+sys in quadrature; M-CONSTRAINTS-11)
  SM tau_beta (M-STATISTICIAN-11): PERKEO III 878.53+-0.88, A route 878.73+-0.83,
     PDG lambda 879.68+-1.61, a route 887.24+-2.94, aSPECT 2024 889.60+-3.20
  storage 878.32 +- 0.43 (S-scaled), material 880.03 +- 0.70 (scaled), magnetic 877.82 +- 0.27
  individual storage results D-27..D-30
"""
import math

def z(a, sa, b, sb):
    return (a - b) / math.hypot(sa, sb)

def wmean(vals):
    w = [1 / s**2 for _, s in vals]
    m = sum(wi * v for wi, (v, _) in zip(w, vals)) / sum(w)
    chi2 = sum(wi * (v - m) ** 2 for wi, (v, _) in zip(w, vals))
    return m, 1 / math.sqrt(sum(w)), chi2

def p_chi2(chi2, dof):
    # survival function of chi^2 for integer dof via series (dof <= 4 here)
    if dof == 1:
        return math.erfc(math.sqrt(chi2 / 2))
    if dof == 2:
        return math.exp(-chi2 / 2)
    if dof == 3:
        x = chi2 / 2
        return math.erfc(math.sqrt(x)) + 2 * math.sqrt(x / math.pi) * math.exp(-x)
    if dof == 4:
        x = chi2 / 2
        return math.exp(-x) * (1 + x)
    raise ValueError

def sigma_of_p(p):
    # two-sided Gaussian equivalent
    lo, hi = 0.0, 40.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if math.erfc(mid / math.sqrt(2)) > p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

P = (887.97, 2.04)
BL1 = (887.7, 2.25)
J_up, J_dn, J = 4.35, 3.98, 877.2
SM = {
    "PERKEO III": (878.53, 0.88),
    "A route": (878.73, 0.83),
    "PDG lambda": (879.68, 1.61),
    "a route": (887.24, 2.94),
    "aSPECT 2024": (889.60, 3.20),
}
STOR = (878.32, 0.43)

print("== 1. Storage-free bound: J-PARC (+) SM tau_beta versus the proton beam ==")
for name, (t, s) in SM.items():
    # J-PARC side facing the beam value is the upper error
    comb, sc, chi_js = wmean([(J, J_up), (t, s)])
    zz = z(P[0], P[1], comb, sc)
    zb = z(BL1[0], BL1[1], comb, sc)
    print(f"  SM[{name:11s}] {t:.2f}+-{s:.2f}: J-PARC(+)SM = {comb:.2f} +- {sc:.2f} s "
          f"(internal chi2 {chi_js:.2f}); proton beam - this = {P[0]-comb:.2f} s = {zz:.2f} sigma; BL1: {zb:.2f} sigma")

print("\n== 2. Rival worlds with the storage-free data {J-PARC, SM} held fixed ==")
print("   C2-world: common tau from {proton beam, J-PARC, SM}; storage free (loss fitted)")
print("   C1-world: common tau from {storage, J-PARC, SM}; proton beam free (offset fitted)")
for name in ["A route", "PDG lambda", "a route"]:
    t, s = SM[name]
    # C2: fit tau to P, J, SM; J-PARC error side chosen according to fit tau
    def chi2_for(vals_fixed, tau):
        c = 0.0
        for v, sv in vals_fixed:
            c += ((v - tau) / sv) ** 2
        c += ((J - tau) / (J_up if tau > J else J_dn)) ** 2
        return c
    def fit(vals_fixed):
        best = min((chi2_for(vals_fixed, 870 + i * 0.005), 870 + i * 0.005) for i in range(5001))
        return best
    c2, tau2 = fit([P, (t, s)])
    c1, tau1 = fit([STOR, (t, s)])
    lr = math.exp((c2 - c1) / 2)
    print(f"  SM[{name:10s}] C2: tau={tau2:.2f} s chi2={c2:.2f}/2 dof p={p_chi2(c2,2):.2e} "
          f"({sigma_of_p(p_chi2(c2,2)):.2f} sigma) | C1: tau={tau1:.2f} s chi2={c1:.2f}/2 dof p={p_chi2(c1,2):.3f} | profile LR C1:C2 = {lr:.3g}")

print("\n== 3. Is one loss rate 'common' to material and magnetic traps? ==")
tau_true = P[0]
for lab, (t, s) in {"material (scaled)": (880.03, 0.70), "magnetic": (877.82, 0.27),
                    "Gravitrap 2018": (881.5, math.hypot(0.7, 0.6)),
                    "UCNtau 2025": (877.82, math.hypot(0.22, 0.20)),
                    "Ezhov 2018": (878.3, math.hypot(1.6, 1.0)),
                    "Serebrov 2005": (878.5, math.hypot(0.7, 0.3)),
                    "MAMBO II 2010": (880.7, math.hypot(1.3, 1.2)),
                    "Steyerl 2012": (882.5, math.hypot(1.4, 1.5)),
                    "Arzumanov 2015": (880.2, 1.2)}.items():
    r = 1 / t - 1 / tau_true
    sr = s / t**2  # storage error only (the beam error is common to all and cancels in differences)
    print(f"  {lab:18s} tau={t:.2f}+-{s:.2f} s needs loss {r:.3e} +- {sr:.1e} s^-1 (1/r = {1/r:.3e} s)")
rm = 1 / 880.03 - 1 / 877.82
srm = math.hypot(0.70 / 880.03**2, 0.27 / 877.82**2)
print(f"  material - magnetic rate difference = {(1/880.03-1/tau_true)-(1/877.82-1/tau_true):.3e} +- {srm:.1e} s^-1 "
      f"= {abs(rm)/srm:.2f} sigma; ratio material/magnetic = {(1/880.03-1/tau_true)/(1/877.82-1/tau_true):.3f}")
# the same split exists under any hypothesis: check under C1 too
print("  (the material-magnetic split is independent of tau_true; it does not discriminate C2 from C1)")

print("\n== 4. What C2 needs from lambda: required lambda and distance from PERKEO III ==")
# tau_beta proportional to 1/(1+3 lambda^2); calibrate on PERKEO III 878.53 s at |lambda| = 1.27641
lamP, slamP = 1.27641, math.hypot(0.00045, 0.00033)
K = 878.53 * (1 + 3 * lamP**2)
for target in [887.97, 887.7]:
    lam = math.sqrt((K / target - 1) / 3)
    print(f"  tau_beta = {target} s needs |lambda| = {lam:.5f}; PERKEO III is {(lamP-lam)/slamP:.1f} sigma (lambda error only) away")
# first-row: Vud from beam + PERKEO III vs unitarity (from M-CONSTRAINTS-04: -4.6 sigma) is quoted, not recomputed

print("\n== 5. Magnitude of the combined non-storage penalty ==")
# How many independent auxiliary failures C2 needs: J-PARC (-10.5 s) and lambda (PERKEO III, UCNA, PERKEO II)
zJ = (P[0] - J) / math.hypot(J_up, P[1])
zA = z(P[0], P[1], *SM["A route"])
print(f"  J-PARC vs proton beam {zJ:.2f} sigma; A-route SM vs proton beam {zA:.2f} sigma; "
      f"(the proper joint figure is section 1, which accounts for the shared proton-beam error)")
# J-PARC with its internal scatter inflated by S = sqrt(15.8/3) on the stat part (M-CONSTRAINTS-11)
S = math.sqrt(15.8 / 3)
Jup_inf = math.hypot(1.7 * S, 4.0)
comb, sc, _ = wmean([(J, Jup_inf), SM["A route"]])
print(f"  J-PARC inflated (+{Jup_inf:.2f} s) (+) A route = {comb:.2f} +- {sc:.2f} s; proton beam at {z(P[0],P[1],comb,sc):.2f} sigma")
comb, sc, _ = wmean([(J, Jup_inf), SM["PDG lambda"]])
print(f"  J-PARC inflated (+) PDG-lambda route = {comb:.2f} +- {sc:.2f} s; proton beam at {z(P[0],P[1],comb,sc):.2f} sigma")
# without J-PARC at all (SM alone)
for name in ["A route", "PDG lambda"]:
    print(f"  SM {name} alone vs proton beam: {z(P[0],P[1],*SM[name]):.2f} sigma")
