"""Falsifier C3-1 (evidence angle): which independent lambda experiments must be wrong for C3?

Units: lifetimes in s (SI); lambda dimensionless.
Linearised master-formula route anchored on the constraints lens (M-CONSTRAINTS-03/-05 verified):
  tau_beta(lambda) = 878.50 s + K*(1.27641 - |lambda|),  K = dtau/d|lambda| = tau*6|l|/(1+3 l^2)
  sigma(tau_beta)  = sqrt((K sigma_lambda)^2 + 0.577^2 + 0.19^2)  (Vud and RC terms, as in M-CONSTRAINTS-05)
Inputs (sourced):
  PERKEO III  -1.27641(45)stat(33)sys  (Maerkisch 2019 abstract)
  UCNA        -1.2772(20)               (Brown 2018 abstract)
  PERKEO II   -1.2748 +-0.0008 (+0.0010/-0.0011)  (D-41, PDG listing; errors combined in quadrature, 0.00105 used)
  aSPECT 2024 -1.2668(27)               (Nab proceedings arXiv:2511.16678 quote, RF-11)
  aCORN       -1.2796(62)               (D-41)
  proton beam 887.97 +- 2.04 s; storage 878.32 +- 0.43 s (statistician, reference gap)
  J-PARC 2024 877.2 +4.35/-3.98 s (D-23, stat+sys quadrature)
"""
import math

tau0, lam0 = 878.50, 1.27641
lam = lam0
K = tau0 * 6 * lam / (1 + 3 * lam**2)
print(f"K = dtau/d|lambda| = {K:.1f} s")

def tau_beta(l, sl):
    t = tau0 + K * (lam0 - abs(l))
    s = math.sqrt((K * sl) ** 2 + 0.577**2 + 0.19**2)
    return t, s

exps = {
    "PERKEO III": (-1.27641, math.hypot(0.00045, 0.00033)),
    "UCNA 2018": (-1.2772, 0.0020),
    "PERKEO II": (-1.2748, math.hypot(0.0008, 0.00105)),
    "aSPECT 2024": (-1.2668, 0.0027),
    "aCORN": (-1.2796, 0.0062),
}
beam, sbeam = 887.97, 2.04
stor, sstor = 878.32, 0.43
J, sJup, sJlo = 877.2, 4.35, 3.98

print("\nPer-experiment tau_beta and tension with C3's requirement tau_beta = proton-beam value")
res = {}
for k, (l, sl) in exps.items():
    t, s = tau_beta(l, sl)
    res[k] = (t, s)
    z = (beam - t) / math.hypot(s, sbeam)
    br = 1 - stor / t
    sbr = (stor / t) * math.hypot(sstor / stor, s / t)
    print(f"  {k:12s} tau_beta = {t:8.2f} +- {s:5.2f} s  z(beam - tau_beta) = {z:+5.2f} sigma   Br_X = {100*br:+.3f} +- {100*sbr:.3f} %")

# Required |lambda| for tau_beta = beam value
lreq = lam0 - (beam - tau0) / K
slreq = sbeam / K
print(f"\nC3 needs |lambda| = {lreq:.5f} +- {slreq:.5f} (from beam 887.97 +- 2.04 s)")
for k, (l, sl) in exps.items():
    z = (abs(l) - lreq) / math.hypot(sl, slreq)
    print(f"  {k:12s} |lambda| - needed = {abs(l)-lreq:+.5f}  -> {z:+5.2f} sigma")

# Electron-detecting beta-asymmetry group (A route) excluding PERKEO III (the dominant one), and all three
def wmean(keys):
    w = [1 / res[k][1] ** 2 for k in keys]
    m = sum(wi * res[k][0] for wi, k in zip(w, keys)) / sum(w)
    s = 1 / math.sqrt(sum(w))
    chi = sum((res[k][0] - m) ** 2 / res[k][1] ** 2 for k in keys)
    return m, s, chi

for keys in (["UCNA 2018", "PERKEO II"], ["UCNA 2018", "PERKEO II", "PERKEO III"], ["UCNA 2018"]):
    m, s, chi = wmean(keys)
    z = (beam - m) / math.hypot(s, sbeam)
    print(f"\nA-route subset {keys}: tau_beta = {m:.2f} +- {s:.2f} s (chi2 {chi:.2f}/{len(keys)-1}); beam - tau_beta = {z:.2f} sigma")

# J-PARC vs C3 (C3 predicts J-PARC = tau_beta = beam)
zJ = (beam - J) / math.hypot(sJup, sbeam)
print(f"\nJ-PARC 2024 vs C3 prediction (= beam): {zJ:.2f} sigma (upper J error used)")
# J-PARC with S = 2.29 inflation of its own error
zJs = (beam - J) / math.hypot(sJup * 2.29, sbeam)
print(f"J-PARC with its error inflated by S=2.29: {zJs:.2f} sigma")

# Joint two-parameter C3 fit: tau_n (storage), tau_beta (beam, J-PARC, lambda experiments)
def fit(keys, useJ=True):
    # tau_beta weighted mean over beam, J-PARC (choose side), lambda subset; iterate side choice
    tb = beam
    for _ in range(20):
        obs = [(beam, sbeam)] + [res[k] for k in keys]
        if useJ:
            obs.append((J, sJup if tb > J else sJlo))
        w = [1 / s**2 for _, s in obs]
        tb = sum(wi * x for wi, (x, _) in zip(w, obs)) / sum(w)
    chi = sum((x - tb) ** 2 / s**2 for x, s in obs)
    return tb, 1 / math.sqrt(sum(w)), chi, len(obs) - 1

for label, keys in (("all five lambda", list(exps)), ("A group only (PIII, PII, UCNA)", ["PERKEO III", "PERKEO II", "UCNA 2018"]),
                    ("a route only (aSPECT)", ["aSPECT 2024"]), ("no lambda", [])):
    tb, s, chi, dof = fit(keys)
    br = 1 - stor / tb
    print(f"\nC3 fit [{label}] + beam + J-PARC: tau_beta = {tb:.2f} +- {s:.2f} s, chi2 = {chi:.2f}/{dof}, "
          f"p = {math.erfc(math.sqrt(chi/2)) if dof==1 else float('nan'):.3g}(dof1 only), Br_X = {100*br:.3f} %")
    # chi2 p-value via series for general dof
    def pchi(c, k):
        # regularized upper gamma Q(k/2, c/2) by series
        a, x = k / 2, c / 2
        if x == 0:
            return 1.0
        # lower gamma series
        term, ssum, n = 1 / a, 1 / a, 1
        while n < 500:
            term *= x / (a + n)
            ssum += term
            n += 1
        P = ssum * math.exp(-x + a * math.log(x) - math.lgamma(a))
        return max(0.0, 1 - P)
    print(f"   p(chi2 >= {chi:.2f} | {dof} dof) = {pchi(chi, dof):.3g}")
