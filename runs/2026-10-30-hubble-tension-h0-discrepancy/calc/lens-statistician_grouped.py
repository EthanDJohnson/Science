"""Grouped chi2 within and between measurement classes, alternative partitions (premise 2),
correlated (GLS/BLUE) combination with a shared NGC 4258 anchor, CMB-internal consistency,
Bayes factor for one-vs-two H0 with explicit priors. Units km/s/Mpc.
Asymmetric errors are symmetrized as the mean of the two sides (stated per line)."""
import sys, math
import numpy as np
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from stats_tools import grouped_chi2, weighted_mean, tension, total_error, p_to_sigma, _chi2_sf

sym = lambda up, dn: 0.5 * (up + dn)

# one value per independent dataset (current values only)
SH0ES = (73.49, 0.93)                                    # D-20
CCHP = (70.39, total_error(1.22, 1.33, 0.70))            # D-24 (=1.94)
SBF = (73.8, total_error(0.7, 2.3))                      # D-29
TF = (73.3, total_error(2.1, 3.5))                       # D-30
TD = (71.1, sym(2.4, 2.3))                               # D-31 mean of sides
MAS = (71.6, 3.7)                                        # D-32 stat only
GW = (71.7, sym(9.4, 7.5))                               # D-33 mean of sides
PL = (67.64, 0.52); ACT = (66.51, 0.64); SPT = (66.66, 0.60)  # D-41..43
SPA = (67.19, 0.38)                                      # D-44
BBN = (68.50, 0.58)                                      # D-45
INV = (67.19, sym(0.66, 0.64))                           # D-48 (r_d from CMB: correlated with CMB)
NORS = (69.2, sym(1.3, 1.4))                             # D-49 Zaborowski sound-horizon-free (CMB lensing x unWISE)

def g(*items):
    return ([x[0] for x in items], [x[1] for x in items])

def show(title, groups):
    r = grouped_chi2(groups)
    print(f"\n== {title} ==")
    for n, d in r["groups"].items():
        print(f"  {n}: mean = {d['mean']:.2f} +- {d['error']:.2f}, chi2 = {d['chi2']:.2f}/{d['dof']}, p = {d['p_consistent']:.3f}")
    print(f"  within chi2 = {r['within_chi2']:.2f}/{r['within_dof']} (p = {r['p_within']:.3f}); "
          f"between chi2 = {r['between_chi2']:.2f}/{r['between_dof']} (p = {r['p_between']:.2e}, z = {r['between_z']:.2f})")
    pm = r["pooled"]
    print(f"  pooled: {pm['mean']:.2f} +- {pm['error']:.2f}, chi2 = {pm['chi2']:.2f}/{pm['dof']}, S = {pm['scale_factor']:.2f}, "
          f"p = {pm['p_consistent']:.2e}")
    return r

# CMB internal consistency (ACT and SPT alone share the PR4 tau prior; treated as independent here)
show("CMB experiments alone (Planck PR4, ACT DR6, SPT-3G D1) vs BAO+BBN",
     {"CMB": g(PL, ACT, SPT), "BAO+BBN": g(BBN)})

# Partition 1: early vs late (all local classes)
show("P1 early (CMB-SPA, BAO+BBN) vs late (all local classes, CCHP for TRGB)",
     {"early": g(SPA, BBN), "late": g(SH0ES, CCHP, SBF, TF, TD, MAS, GW)})
# Partition 2: Cepheid-SN vs everything else
show("P2 SH0ES Cepheid-SN vs everything else",
     {"Ceph-SN": g(SH0ES), "rest": g(SPA, BBN, CCHP, SBF, TF, TD, MAS, GW)})
# Partition 3: three groups
show("P3 early | Ceph-SN | other local",
     {"early": g(SPA, BBN), "Ceph-SN": g(SH0ES), "other local": g(CCHP, SBF, TF, TD, MAS, GW)})
# Partition 4: uses r_s vs does not (adds sound-horizon-free BAO to non-r_s side)
show("P4 uses r_s (CMB-SPA, BAO+BBN) vs no r_s (all local + sound-horizon-free BAO D-49)",
     {"r_s": g(SPA, BBN), "no r_s": g(SH0ES, CCHP, SBF, TF, TD, MAS, GW, NORS)})
# Per-class grouped chi2 (each class its own group)
show("Per-class groups",
     {"CMB-SPA": g(SPA), "BAO+BBN": g(BBN), "Ceph-SN": g(SH0ES), "TRGB-SN (CCHP)": g(CCHP),
      "non-SN ladders": g(SBF, TF), "time delays": g(TD), "masers": g(MAS), "sirens": g(GW)})
# Same with SH0ES-side TRGB instead of CCHP (D-27: 72.1-73.3 +-1.8, take 72.7)
show("Per-class groups, SH0ES-side TRGB (72.7+-1.8, D-27) in place of CCHP",
     {"early": g(SPA, BBN), "Ceph-SN": g(SH0ES), "TRGB-SN (Li 2026)": g((72.7, 1.8)),
      "other local": g(SBF, TF, TD, MAS, GW)})
# Non-SN, non-Cepheid local only vs early
show("Local without Cepheids and without SNe (SBF, TF, TD, masers, sirens) vs early",
     {"early": g(SPA, BBN), "no-SN local": g(SBF, TF, TD, MAS, GW)})
show("One-step only (TD, masers, sirens) vs early",
     {"early": g(SPA, BBN), "one-step": g(TD, MAS, GW)})

# ---- GLS with shared NGC 4258 anchor (sigma_a = 1.5% in distance, D-dossier sec 6) ----
print("\n== GLS local combination with shared NGC 4258 anchor ==")
names = ["SH0ES", "CCHP", "SBF", "TF", "TD", "MAS", "GW"]
vals = np.array([SH0ES[0], CCHP[0], SBF[0], TF[0], TD[0], MAS[0], GW[0]])
errs = np.array([SH0ES[1], CCHP[1], SBF[1], TF[1], TD[1], MAS[1], GW[1]])
# weight of NGC 4258 in each anchor set (assumption): SH0ES 1/3 (MW, LMC, NGC4258 [+SMC]); CCHP 1 (sole anchor);
# SBF 1 (JWST TRGB on NGC 4258); TF 0.5 (Cepheid/TRGB zero points); one-step 0
w = np.array([1/3, 1.0, 1.0, 0.5, 0.0, 0.0, 0.0])
for frac in (0.0, 0.015, 0.025):
    sa = frac * vals  # anchor error in km/s/Mpc
    C = np.diag(errs**2)
    for i in range(len(vals)):
        for j in range(len(vals)):
            if i != j:
                C[i, j] = w[i] * w[j] * sa[i] * sa[j]
    Ci = np.linalg.inv(C)
    one = np.ones(len(vals))
    var = 1 / (one @ Ci @ one)
    mean = var * (one @ Ci @ vals)
    r = vals - mean
    chi2 = r @ Ci @ r
    t1 = tension(mean, math.sqrt(var), SPA[0], SPA[1])
    t2 = tension(mean, math.sqrt(var), BBN[0], BBN[1])
    print(f"  anchor frac = {frac}: local GLS = {mean:.2f} +- {math.sqrt(var):.2f}, chi2 = {chi2:.2f}/{len(vals)-1} "
          f"(p = {_chi2_sf(chi2, len(vals)-1):.3f}); vs CMB-SPA z = {t1['z']:.2f}; vs BAO+BBN z = {t2['z']:.2f}")

# Early combination: CMB-SPA and BAO+BBN independent; inverse ladder correlated with CMB (r_d) -- show rho
print("\n== Early combination ==")
wm = weighted_mean([SPA[0], BBN[0]], [SPA[1], BBN[1]])
print(f"  CMB-SPA + BAO+BBN (indep.): {wm['mean']:.2f} +- {wm['error']:.2f}, chi2 = {wm['chi2']:.2f}/1 (z = {math.sqrt(wm['chi2']):.2f}), S = {wm['scale_factor']:.2f}")
for rho in (0.0, 0.5, 0.8):
    v = np.array([SPA[0], BBN[0], INV[0]]); e = np.array([SPA[1], BBN[1], INV[1]])
    C = np.diag(e**2); C[0, 2] = C[2, 0] = rho * e[0] * e[2]
    Ci = np.linalg.inv(C); one = np.ones(3)
    var = 1 / (one @ Ci @ one); mean = var * (one @ Ci @ v); r = v - mean
    print(f"  + inverse ladder, rho(CMB,inv) = {rho}: {mean:.2f} +- {math.sqrt(var):.2f}, chi2 = {r @ Ci @ r:.2f}/2")

# Bayes factor, one common H0 vs two values, with explicit Gaussian prior on the offset delta (width tau)
print("\n== Bayes factor two-values vs one-value, Gaussian prior on offset of width tau ==")
def bf_two_vs_one(d, s, tau):
    # marginal of d under H1: N(0, s^2+tau^2); under H0: N(0, s^2)
    l1 = -0.5 * d * d / (s * s + tau * tau) - 0.5 * math.log(s * s + tau * tau)
    l0 = -0.5 * d * d / (s * s) - 0.5 * math.log(s * s)
    return math.exp(l1 - l0)
for lab, (a, b) in {"SH0ES vs CMB-SPA": (SH0ES, SPA), "SH0ES vs BAO+BBN": (SH0ES, BBN),
                   "CCHP vs CMB-SPA": (CCHP, SPA), "TDCOSMO vs CMB-SPA": (TD, SPA)}.items():
    d = a[0] - b[0]; s = math.hypot(a[1], b[1])
    out = ", ".join(f"tau={tau}: {bf_two_vs_one(d, s, tau):.3g}" for tau in (3, 6, 10))
    print(f"  {lab}: d = {d:.2f} +- {s:.2f}; BF(two/one) {out}")
