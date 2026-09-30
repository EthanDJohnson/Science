"""Decomposer lens: calculations that settle leaves of the sub-question tree.

Units: SI (lifetimes in s, rates in s^-1). lambda, Vud, Vus, Br dimensionless.
Inputs are dossier items (IDs in comments). Sussex-ILL (D-22) is an unverified lead; every
combination is shown with and without it.
Asymmetric errors are symmetrised as the side facing the other class (stated where used)
or as (up+down)/2 for pooled means.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import stats_tools as st
import neutron_beta_decay as nb

def tot(stat, sys_):
    return st.total_error(stat, sys_)

print("=== L1: measurement inputs (s) ===")
BL1 = (887.7, tot(1.2, 1.9))                    # D-20
SIL = (889.2, tot(3.0, 3.8))                    # D-22 (lead, unverified)
JP_up, JP_dn = tot(1.7, 4.0), tot(1.7, 3.6)     # D-23
JP = (877.2, (JP_up, JP_dn))
UCNT_up, UCNT_dn = tot(0.22, 0.20), tot(0.22, 0.17)   # D-27
UCNT = (877.82, 0.5 * (UCNT_up + UCNT_dn))
EZH = (878.3, tot(1.6, 1.0))                    # D-30 (search-summary)
GRAV = (881.5, tot(0.7, 0.6))                   # D-28
SER05 = (878.5, tot(0.7, 0.3))                  # D-29
MAMBO = (880.7, tot(1.3, 1.2))                  # D-29
STEY = (882.5, tot(1.4, 1.5))                   # D-29
ARZ = (880.2, 1.2)                              # D-29
JPsym = (877.2, 0.5 * (JP_up + JP_dn))
for n, v in [("BL1", BL1), ("Sussex-ILL", SIL), ("J-PARC", JP), ("UCNtau", UCNT), ("Ezhov", EZH),
             ("Gravitrap", GRAV), ("Serebrov05", SER05), ("MAMBO II", MAMBO), ("Steyerl", STEY), ("Arzumanov", ARZ)]:
    print(f"  {n:11s} {v[0]:.2f} +- {v[1]}")

def wm(lst):
    return st.weighted_mean([x[0] for x in lst], [x[1] for x in lst])

print("\n=== L2: class means (s), PDG scale factor ===")
classes = {
    "proton beam (BL1 only)": [BL1],
    "proton beam (BL1+Sussex-ILL)": [BL1, SIL],
    "electron beam (J-PARC, sym)": [JPsym],
    "magnetic traps (UCNtau+Ezhov)": [UCNT, EZH],
    "material bottles (5)": [GRAV, SER05, MAMBO, STEY, ARZ],
}
cm = {}
for k, lst in classes.items():
    r = wm(lst); cm[k] = r
    print(f"  {k:32s} mean {r['mean']:.2f} err {r['error']:.2f} chi2/dof {r['chi2']:.2f}/{r['dof']} S {r['scale_factor']:.2f} err_scaled {r['error_scaled']:.2f}")
allbottle = wm([UCNT, EZH, GRAV, SER05, MAMBO, STEY, ARZ])
print(f"  all storage (7): mean {allbottle['mean']:.2f} err {allbottle['error']:.2f} chi2/dof {allbottle['chi2']:.2f}/{allbottle['dof']} S {allbottle['scale_factor']:.2f} err_scaled {allbottle['error_scaled']:.2f} p {allbottle['p_consistent']:.3g}")
mm = st.tension(cm["magnetic traps (UCNtau+Ezhov)"]["mean"], cm["magnetic traps (UCNtau+Ezhov)"]["error"],
                cm["material bottles (5)"]["mean"], cm["material bottles (5)"]["error_scaled"])
print(f"  material vs magnetic (material err scaled): diff {-mm['difference']:.2f} s, z {mm['z']:.2f}")

print("\n=== L3: partition tests (grouped chi2, symmetric errors; J-PARC symmetrised as mean of sides) ===")
storage = [UCNT, EZH, GRAV, SER05, MAMBO, STEY, ARZ]
def g(lst): return ([x[0] for x in lst], [x[1] for x in lst])
parts = {
    "P1 beam(BL1,SIL,JP) vs bottle": {"beam": g([BL1, SIL, JPsym]), "bottle": g(storage)},
    "P2 proton-counting(BL1,SIL) vs rest(JP+bottles)": {"proton": g([BL1, SIL]), "rest": g([JPsym] + storage)},
    "P3 BL1 vs rest (incl SIL, JP, bottles)": {"BL1": g([BL1]), "rest": g([SIL, JPsym] + storage)},
    "P4 proton / electron / material / magnetic": {"p": g([BL1, SIL]), "e": g([JPsym]),
        "mat": g([GRAV, SER05, MAMBO, STEY, ARZ]), "mag": g([UCNT, EZH])},
    "P5 strong field(>=4.6 T: BL1,SIL) vs weak (JP, bottles) [same sets as P2]": {"strong": g([BL1, SIL]), "weak": g([JPsym] + storage)},
}
for name, grp in parts.items():
    r = st.grouped_chi2(grp)
    print(f"  {name}: within {r['within_chi2']:.2f}/{r['within_dof']} (p {r['p_within']:.3g}); between {r['between_chi2']:.2f}/{r['between_dof']} (z {r['between_z']:.2f}); pooled chi2 {r['pooled']['chi2']:.2f}/{r['pooled']['dof']}")

print("\n=== L4: headline tensions (s) ===")
pb = cm["proton beam (BL1+Sussex-ILL)"]
for lab, b in [("BL1 only", BL1), ("BL1+SIL", (pb["mean"], pb["error"]))]:
    t1 = st.tension(b[0], b[1], UCNT[0], UCNT[1])
    t2 = st.tension(b[0], b[1], allbottle["mean"], allbottle["error_scaled"])
    print(f"  {lab} vs UCNtau: diff {t1['difference']:.2f} +- {t1['sigma']:.2f}, z {t1['z']:.2f};  vs all storage (scaled): diff {t2['difference']:.2f} +- {t2['sigma']:.2f}, z {t2['z']:.2f}")
gap = pb["mean"] - UCNT[0]
print(f"  fractional gap (BL1+SIL vs UCNtau) = {gap/pb['mean']:.4f}; missing rate dGamma = {1/UCNT[0]-1/pb['mean']:.3e} s^-1")
print(f"  BL1 only vs UCNtau: frac {(BL1[0]-UCNT[0])/BL1[0]:.4f}; dGamma = {1/UCNT[0]-1/BL1[0]:.3e} s^-1")

print("\n=== L5: J-PARC as discriminator ===")
for lab, b in [("BL1", BL1), ("BL1+SIL", (pb["mean"], pb["error"]))]:
    t = st.tension(JP[0], JP[1], b[0], b[1])
    print(f"  J-PARC vs {lab}: diff {t['difference']:.2f} +- {t['sigma']:.2f}, z {t['z']:.2f}")
t = st.tension(JP[0], JP[1], UCNT[0], UCNT[1]); print(f"  J-PARC vs UCNtau: diff {t['difference']:.2f} +- {t['sigma']:.2f}, z {t['z']:.2f}")
# internal inconsistency: per-condition (D-24), stat only (first error), chi2/dof 15.8/3 quoted
S = math.sqrt(15.8 / 3)
jp_up_s, jp_dn_s = tot(1.7 * S, 4.0), tot(1.7 * S, 3.6)
print(f"  quoted internal chi2/dof 15.8/3 -> S = {S:.2f}; stat 1.7 -> {1.7*S:.2f} s; total +{jp_up_s:.2f}/-{jp_dn_s:.2f} s")
t = st.tension(JP[0], (jp_up_s, jp_dn_s), BL1[0], BL1[1]); print(f"  J-PARC (stat scaled by S) vs BL1: z {t['z']:.2f}")
t = st.tension(JP[0], (jp_up_s, jp_dn_s), pb["mean"], pb["error"]); print(f"  J-PARC (stat scaled) vs BL1+SIL: z {t['z']:.2f}")
pc = [(870.9, 3.5), (868.3, 4.0), (868.2, 7.7), (884.8, 2.4)]
r = st.weighted_mean([x[0] for x in pc], [x[1] for x in pc])
print(f"  per-condition stat-only mean {r['mean']:.2f} +- {r['error']:.2f}, chi2 {r['chi2']:.2f}/{r['dof']} (paper quotes 15.8/3; differences from correlated sys)")
r3 = st.weighted_mean([x[0] for x in pc[:3]], [x[1] for x in pc[:3]])
print(f"  three mutually consistent conditions only: mean {r3['mean']:.2f} +- {r3['error']:.2f} (stat), chi2 {r3['chi2']:.2f}/{r3['dof']}")
# likelihood ratio J-PARC gives 'J-PARC ~ bottle' vs 'J-PARC ~ beam' hypotheses (Gaussian, point predictions)
for lab, err in [("quoted", JP[1]), ("S-scaled", (jp_up_s, jp_dn_s))]:
    zb = st.tension(JP[0], err, UCNT[0], 0.0)["z"]; zp = st.tension(JP[0], err, BL1[0], 0.0)["z"]
    print(f"  LR[J-PARC ~ storage : J-PARC ~ proton-beam] ({lab}, point predictions 877.82 vs 887.7) = {math.exp(-(zb**2 - zp**2)/2):.1f}")
# precision needed for an electron-counting or in-bottle beta experiment to split 877.8 vs 887.7
d = BL1[0] - UCNT[0]
print(f"  total sigma needed to split {d:.1f} s at 3 sigma: {d/3:.2f} s; at 5 sigma: {d/5:.2f} s")

print("\n=== L6: required systematic sizes vs published budgets ===")
print(f"  proton beam: need fractional error {d/BL1[0]:.4f} ({d:.1f} s) vs BL1 total sys 1.9 s -> {d/1.9:.1f} x sys; vs fluence unc 0.5 s -> {d/0.5:.0f} x; vs 'unassoc. with fluence' 1.7 s -> {d/1.7:.1f} x")
dG = 1/UCNT[0] - 1/BL1[0]
print(f"  bottle: need unidentified loss rate {dG:.3e} s^-1 (time constant {1/dG:.3e} s = {1/dG/86400:.2f} d)")
print(f"  UCNtau sys ~0.2 s -> equivalent rate {0.2/UCNT[0]**2:.2e} s^-1; need/budget = {dG/(0.2/UCNT[0]**2):.0f}")
print(f"  Gravitrap sys 0.6 s -> rate {0.6/GRAV[0]**2:.2e} s^-1; need/budget = {dG/(0.6/GRAV[0]**2):.0f}")
print(f"  a common bottle loss must be same size in material (Gravitrap 881.5) and magnetic (UCNtau 877.8) traps, which differ by {GRAV[0]-UCNT[0]:.1f} s in the opposite sense to the gap direction? Gravitrap is closer to beam by {GRAV[0]-UCNT[0]:.1f} s")

print("\n=== L7: SM arbitration: two self-consistent 'worlds' (GS2023 RC, paired superallowed Vud 0.97361(32)) ===")
VUD, SVUD = 0.97361, 0.00032
VUS, SVUS = 0.22431, 0.00085   # D-45 PDG average
lams = {"PERKEO III": (1.27641, 0.00056), "UCNA": (1.2772, 0.0020), "PERKEO II": (1.2748, 0.00132),
        "PDG2024": (1.2754, 0.0013), "aSPECT2024": (1.2668, 0.0027), "aCORN": (1.2796, 0.0062)}
for k, (l, sl) in lams.items():
    r = nb.tau_beta(l, sl, VUD, SVUD, rc_set="GS2023")
    tb = st.tension(r["tau"], r["sigma"], BL1[0], BL1[1]); tu = st.tension(r["tau"], r["sigma"], UCNT[0], UCNT[1])
    print(f"  lambda {k:10s} {l:.5f}({sl}) -> tau_beta {r['tau']:.2f} +- {r['sigma']:.2f} s; z vs BL1 {tb['z']:.2f}, z vs UCNtau {tu['z']:.2f}")
Aonly = st.weighted_mean([1.27641, 1.2772, 1.2748], [0.00056, 0.0020, 0.00132])
print(f"  A-coefficient lambda (PIII, UCNA, PII): {Aonly['mean']:.5f} +- {Aonly['error']:.5f}, chi2 {Aonly['chi2']:.2f}/{Aonly['dof']}")
tA = st.tension(Aonly["mean"], Aonly["error"], 1.2668, 0.0027); print(f"  A-route vs aSPECT2024 lambda: diff {tA['difference']:.5f}, z {tA['z']:.2f}")
print("  World A: lambda(A-route), tau = UCNtau; World B: lambda(aSPECT), tau = BL1")
for lab, l, sl, tau, stau in [("A", Aonly["mean"], Aonly["error"], UCNT[0], UCNT[1]), ("B", 1.2668, 0.0027, BL1[0], BL1[1]),
                             ("A-lambda + BL1 tau", Aonly["mean"], Aonly["error"], BL1[0], BL1[1]),
                             ("aSPECT lambda + UCNtau tau", 1.2668, 0.0027, UCNT[0], UCNT[1])]:
    v = nb.vud_from_tau(tau, stau, l, sl, rc_set="GS2023")
    tv = st.tension(v["vud"], v["sigma"], VUD, SVUD)
    row = nb.ckm_first_row(v["vud"], v["sigma"], VUS, SVUS)
    print(f"  {lab:28s}: Vud {v['vud']:.5f} +- {v['sigma']:.5f}; vs superallowed z {tv['z']:.2f}; row sum {row['sum']:.5f} +- {row['sigma']:.5f} (z {row['z']:.2f})")
print("  -> both A and B are internally consistent with superallowed Vud; CKM cannot arbitrate until the A-vs-a lambda split is resolved")

print("\n=== L8: exotic branch implied under each lambda route ===")
for k in ["PERKEO III", "PDG2024", "aSPECT2024"]:
    l, sl = lams[k]
    r = nb.tau_beta(l, sl, VUD, SVUD, rc_set="GS2023")
    b = nb.br_exotic(UCNT[0], UCNT[1], r["tau"], r["sigma"])
    print(f"  {k:10s}: Br_X = {100*b['br']:.3f} +- {100*b['sigma']:.3f} %, 95% one-sided upper {100*b['upper']:.3f} %  (needed ~{100*(1-UCNT[0]/BL1[0]):.2f} %)")

print("\n=== L9: lambda precision at which SM prediction alone separates 877.8 vs 887.7 ===")
for tgt, z in [(d/3, 3), (d/5, 5)]:
    # total sigma of tau_beta must be <= tgt; subtract Vud part in quadrature
    rv = nb.tau_beta(1.2754, 0.0, VUD, SVUD, rc_set="GS2023")
    sv = rv["sigma"]
    rem = math.sqrt(max(tgt**2 - sv**2, 0))
    print(f"  {z} sigma: sigma_tau_beta <= {tgt:.2f} s; Vud+K part {sv:.2f} s; lambda budget {rem:.2f} s -> sigma_lambda <= {nb.lambda_precision_for(rem):.5f} (rel {nb.lambda_precision_for(rem)/1.2754*100:.3f} %)")
print("  (PERKEO III alone already gives sigma_lambda 0.00056; the bottleneck is accuracy: the A-vs-a split of"
      f" {tA['difference']:.4f} = {abs(tA['difference'])*abs(nb.tau_beta(1.2754,0,VUD,0)['dtau_dlambda']):.1f} s in tau_beta)")

print("\n=== L10: leave-one-out robustness of the gap ===")
t = st.tension(SIL[0], SIL[1], UCNT[0], UCNT[1]); print(f"  without BL1: Sussex-ILL vs UCNtau diff {t['difference']:.2f} +- {t['sigma']:.2f}, z {t['z']:.2f}")
t = st.tension(SIL[0], SIL[1], allbottle['mean'], allbottle['error_scaled']); print(f"  without BL1: Sussex-ILL vs all storage (scaled) z {t['z']:.2f}")
noU = wm([EZH, GRAV, SER05, MAMBO, STEY, ARZ])
print(f"  storage without UCNtau: {noU['mean']:.2f} +- {noU['error_scaled']:.2f} (S {noU['scale_factor']:.2f})")
t = st.tension(BL1[0], BL1[1], noU['mean'], noU['error_scaled']); print(f"  BL1 vs storage-without-UCNtau: diff {t['difference']:.2f}, z {t['z']:.2f}")
t = st.tension(BL1[0], BL1[1], GRAV[0], GRAV[1]); print(f"  BL1 vs Gravitrap alone: diff {t['difference']:.2f}, z {t['z']:.2f}")
print(f"  Caylor ~0.3% H2 proton loss (D-17) = {0.003*BL1[0]:.1f} s vs needed {d:.1f} s ({0.003*BL1[0]/d*100:.0f}% of gap)")
print(f"  BL1 trap-nonlinearity correction -5.3 s and 6Li absorption +5.4 s (D-21): a 100% error in either alone = {5.3/d*100:.0f}% of gap")
