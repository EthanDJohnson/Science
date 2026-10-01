#!/usr/bin/env python3
"""Constraints lens: does each candidate's prediction pattern fit every lifetime class and the SM route?

Units: lifetimes in s (SI); rates in s^-1; probabilities dimensionless.
Inputs: D-20..D-30 (lifetimes, errors as quoted, stat+sys in quadrature), D-21 (BL1 budget), D-25, D-62;
SM tau_beta routes from lens-constraints_sm_tau.py (A route 878.70 +- 0.83 s, a route 887.21 +- 2.93 s).
Sections: 1 J-PARC verdict; 2 required systematic sizes vs budgets; 3 n -> n' requirement vs SNS;
4 chi^2 ledger per candidate (linear least squares; J-PARC uses the side of its asymmetric error facing the model).
"""
import math
import sys

import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import stats_tools as st  # noqa: E402
import nn_mirror_osc as nm  # noqa: E402

q = math.hypot
BL1 = (887.7, q(1.2, 1.9)); SIL = (889.2, q(3.0, 3.8))
JP = (877.2, q(1.7, 4.0), q(1.7, 3.6))            # value, up, down
UCN = (877.82, q(0.22, 0.20)); EZH = (878.3, q(1.6, 1.0))
GRV = (881.5, q(0.7, 0.6)); SER05 = (878.5, q(0.7, 0.3)); MAM = (880.7, q(1.3, 1.2)); STE = (882.5, q(1.4, 1.5)); ARZ = (880.2, 1.2)
SM_A = (878.70, 0.83); SM_a = (887.21, 2.93)

print("=== 1. J-PARC 2024 verdict ===")
jp_e = (JP[1], JP[2])
for lab, x in (("BL1", BL1), ("UCNtau", UCN), ("Gravitrap", GRV), ("SM A route", SM_A), ("SM a route", SM_a)):
    t = st.tension(JP[0], jp_e, x[0], x[1])
    print(f"  J-PARC vs {lab:11s}: diff = {t['difference']:+.2f} s, sigma = {t['sigma']:.2f} s, z = {t['z']:.2f}")
S_int = math.sqrt(15.8 / 3)
jp_scaled = (q(1.7 * S_int, 4.0), q(1.7 * S_int, 3.6))
print(f"  J-PARC internal chi2/dof = 15.8/3 -> S = {S_int:.2f}; stat 1.7 -> {1.7*S_int:.2f} s; total +{jp_scaled[0]:.2f}/-{jp_scaled[1]:.2f} s")
for lab, x in (("BL1", BL1), ("UCNtau", UCN)):
    print(f"    scaled J-PARC vs {lab}: z = {st.tension(JP[0], jp_scaled, x[0], x[1])['z']:.2f}")


def gauss_like(x, mu, e_up, e_dn, s_model=0.0):
    s = e_up if mu > x else e_dn
    s = q(s, s_model)
    return math.exp(-0.5 * ((x - mu) / s) ** 2) / s


for lab, e in (("as quoted", jp_e), ("stat scaled by S", jp_scaled)):
    L_bottle = gauss_like(JP[0], UCN[0], e[0], e[1], UCN[1])
    L_beam = gauss_like(JP[0], BL1[0], e[0], e[1], BL1[1])
    print(f"  likelihood ratio L(J-PARC = storage value)/L(J-PARC = proton-beam value), {lab}: {L_bottle/L_beam:.1f}")
print("  -> favours candidates in which an electron-counting beam reads the storage value (proton-counting systematic,\n"
      "     strong-field n->n', electron-always new physics) over those in which it reads the proton-beam value\n"
      "     (bottle systematic, dark decay with no electron).")

print("\n=== 2. Required size of each systematic vs its published budget ===")
gap = BL1[0] - UCN[0]
frac = gap / BL1[0]
print(f"  gap BL1 - UCNtau = {gap:.2f} s = {100*frac:.3f}% of tau_beam; as a rate 1/877.82 - 1/887.7 = {1/UCN[0]-1/BL1[0]:.4e} s^-1")
print(f"  BL1: needed shift / quoted sys (1.9 s) = {gap/1.9:.1f}; / total (2.25 s) = {gap/BL1[1]:.1f}")
items = {"6LiF areal density (2005; replaced 2013)": (None, 2.2), "6Li cross section (2005; replaced)": (None, 1.2),
         "n-detector solid angle": (None, 1.0), "absorption by 6Li": (5.4, 0.8), "beam halo": (-1.0, 1.0),
         "trap nonlinearity": (-5.3, 0.8), "proton backscatter": (None, 0.4), "Si scattering": (-0.2, 0.5),
         "2013 fluence correction": (1.4, 0.5), "2013 6Li deposit mass change": (None, 0.9),
         "2013 'unassociated with fluence' line": (None, 1.7)}
for k, (corr, unc) in items.items():
    c = f"correction {corr:+.1f} s -> needed = {gap/abs(corr):.1f}x the correction" if corr else "no correction applied"
    print(f"    {k:42s}: unc {unc:.1f} s -> needed = {gap/unc:5.1f} sigma of the item; {c}")
print(f"  proton-loss equivalent: an unrecorded proton loss fraction f raises tau_beam by f*tau: need f = {100*frac:.2f}%")
print(f"    Caylor 2025 H2 charge-exchange estimate ~0.3% [D-17] -> {0.003*BL1[0]:.1f} s = {0.003/frac*100:.0f}% of the gap if wholly uncorrected")
print(f"  neutron-fluence equivalent: fluence over-counted by {100*frac:.2f}% (i.e. 6Li efficiency too high by that fraction)")
dG_mag = 1 / UCN[0] - 1 / BL1[0]
dG_mat = 1 / GRV[0] - 1 / BL1[0]
print(f"  Bottle: unaccounted loss needed in UCNtau = {dG_mag:.3e} s^-1; UCNtau sys (+0.20 s) as rate = {0.20/UCN[0]**2:.2e} s^-1 "
      f"-> {dG_mag/(0.20/UCN[0]**2):.0f}x the budget")
print(f"          in Gravitrap = {dG_mat:.3e} s^-1; Gravitrap sys 0.6 s = {0.6/GRV[0]**2:.2e} s^-1 -> {dG_mat/(0.6/GRV[0]**2):.0f}x")
print(f"          a single common loss must differ by {100*(dG_mag-dG_mat)/dG_mag:.0f}% between the magnetic and material traps "
      f"(UCNtau vs Gravitrap), i.e. {dG_mag-dG_mat:.2e} s^-1")
wm_mat = st.weighted_mean([GRV[0], SER05[0], MAM[0], STE[0], ARZ[0]], [GRV[1], SER05[1], MAM[1], STE[1], ARZ[1]])
wm_mag = st.weighted_mean([UCN[0], EZH[0]], [UCN[1], EZH[1]])
print(f"  material-bottle mean {wm_mat['mean']:.2f} +- {wm_mat['error_scaled']:.2f} s (chi2 {wm_mat['chi2']:.1f}/{wm_mat['dof']}); "
      f"magnetic mean {wm_mag['mean']:.2f} +- {wm_mag['error_scaled']:.2f} s")

print("\n=== 3. Strong-field n -> n' (Berezhiani) requirement vs the SNS regeneration limit ===")
P_need = 1 - UCN[0] / BL1[0]
print(f"  needed conversion in the trap (P_det ~ 0): P_trap = {P_need:.4f}")
P_lim = math.sqrt(2.5e-8)
print(f"  SNS regeneration p < 2.5e-8 [D-62]; if both passages equal P: P < {P_lim:.2e} -> needed/allowed = {P_need/P_lim:.0f}")
r = nm.beam_solenoid(dm=280 * nm.NEV, theta0=1e-3, B_center=4.6, v=1000.0)
r66 = nm.beam_solenoid(dm=280 * nm.NEV, theta0=1e-3, B_center=6.6, v=1000.0)
print(f"  Berezhiani worked example (dm = 280 neV, theta0 = 1e-3, 4.6 T, v = 1000 m/s): P_trap = {r['P_trap']:.4f}, "
      f"P_det = {r['P_det']:.4f}, tau_beam/tau_beta = {r['tau_beam_over_tau_beta']:.5f} (needs {BL1[0]/UCN[0]:.5f})")
print(f"  same parameters, 6.6 T solenoid: P_det-like passage = {r66['P_det']:.4f}; regeneration ~ P^2 = {r66['P_det']**2:.2e} "
      f"vs limit 2.5e-8 -> ratio {r66['P_det']**2/2.5e-8:.1e} (geometry of the SNS magnets NOT modelled)")

print("\n=== 4. chi^2 ledger: each candidate's prediction pattern, fit by linear least squares ===")
data = [("BL1", "pbeam", BL1), ("SussexILL*", "pbeam", SIL), ("J-PARC", "ebeam", JP), ("UCNtau", "mag", UCN),
        ("Ezhov", "mag", EZH), ("Gravitrap", "mat", GRV), ("Serebrov05", "mat", SER05), ("MAMBO II", "mat", MAM),
        ("Steyerl12", "mat", STE), ("Arzumanov15", "mat", ARZ)]
# model: prediction_i = tau + sum_k c_ik * delta_k ; coefficient maps per class
models = {
    "N  null: one tau, no offsets": {},
    "P  proton-beam systematic / strong-field n-n' (pbeam offset)": {"pbeam": [1]},
    "B  bottle systematic, common to all traps (mag+mat offset)": {"mag": [1], "mat": [1]},
    "B2 bottle systematic, separate material and magnetic offsets": {"mag": [1, 0], "mat": [0, 1]},
    "D  dark decay, no electron (bottles = tau_beta(1-Br))": {"mag": [1], "mat": [1]},
    "V  electron-always, proton-less branch (Veselsky)": {"pbeam": [1]},
}
# SM route treatment: which models predict SM tau_beta = storage value vs beam value
sm_is_beam = {"N": None, "P": False, "B": True, "B2": True, "D": True, "V": True}


def fit(model_key, coef, sm=None, drop_sil=False):
    rows = [d for d in data if not (drop_sil and d[0].startswith("Sussex"))]
    npar = 1 + max((len(v) for v in coef.values()), default=0)
    X, y, s_list, names = [], [], [], []
    for name, cls, val in rows:
        c = coef.get(cls, [0] * (npar - 1))
        X.append([1.0] + list(c) + [0.0] * (npar - 1 - len(c))); y.append(val[0]); names.append(name)
        s_list.append(val[1] if len(val) == 2 else None)
    if sm is not None:
        tag = model_key.split()[0]
        beam_like = sm_is_beam[tag]
        smv = sm
        c_sm = [0.0] * (npar - 1)
        if beam_like and npar > 1:
            c_sm = [0.0] * (npar - 1)          # SM tau_beta = beam-side tau (the fitted tau is the beam-side value)
        X.append([1.0] + c_sm); y.append(smv[0]); s_list.append(smv[1]); names.append("SM tau_beta")
    X = np.array(X); y = np.array(y)
    pred = np.full(len(y), y.mean())
    for _ in range(5):
        s = np.array([sv if sv is not None else (JP[1] if p > JP[0] else JP[2]) for sv, p in zip(s_list, pred)])
        W = np.diag(1 / s**2)
        beta = np.linalg.solve(X.T @ W @ X, X.T @ W @ y)
        pred = X @ beta
    chi2 = float(np.sum(((y - pred) / s) ** 2))
    dof = len(y) - npar
    return beta, chi2, dof


print("  Parametrisation: tau = the value read by classes WITHOUT an offset (for P and V: the storage/total value;")
print("  for B, B2, D: the proton-beam/true tau_beta value). SM tau_beta is attached to the offset-free classes, which is")
print("  where each candidate places it: P -> storage value; B, D, V -> beam value (V: tau_beta = proton-beam value).")
for sm_lab, sm in (("no SM input", None), ("SM A route 878.70(83)", SM_A), ("SM a route 887.21(293)", SM_a)):
    print(f"  --- {sm_lab} ---")
    for key, coef in models.items():
        tag = key.split()[0]
        if sm is not None and tag == "V":
            # V: tau_beta(p e nu) = proton-beam value -> SM attaches to the pbeam class: shift via offset coefficient
            coef_sm = coef
            # implement by treating SM as a pbeam-class datum
            data.append(("SM", "pbeam", sm))
            beta, chi2, dof = fit(key, coef_sm, None)
            data.pop()
        elif sm is not None and tag == "N":
            data.append(("SM", "any", sm))
            beta, chi2, dof = fit(key, coef, None)
            data.pop()
        else:
            beta, chi2, dof = fit(key, coef, sm)
        p = st._chi2_sf(chi2, dof)
        offs = ", ".join(f"{b:+.2f}" for b in beta[1:])
        print(f"    {key:66s} tau = {beta[0]:.2f} s, offsets [{offs}] s, chi2 = {chi2:6.2f}/{dof} (p = {p:.3g})")
print("  (* Sussex-ILL is a brief lead, not verified in the dossier [D-22]; rerun without it:)")
for key, coef in models.items():
    beta, chi2, dof = fit(key, coef, None, drop_sil=True)
    print(f"    {key:66s} chi2 = {chi2:6.2f}/{dof} (p = {st._chi2_sf(chi2, dof):.3g}) without Sussex-ILL, no SM")

print("\n=== 5. Separation power of the running/planned measurements (sharp predictions 877.82 s vs 887.7 s) ===")
gap = BL1[0] - UCN[0]
for lab, s in (("LiNA (J-PARC upgrade) ~1 s [D-102]", 1.0), ("UCNProBe 2 s [D-106]", 2.0), ("UCNProBe 1 s", 1.0),
               ("BL2 <1 s [D-100]", 1.0), ("BL3 0.3 s [D-101]", 0.3), ("tauSPECT 0.3 s [D-103]", 0.3)):
    z_sharp = gap / s
    z_vs_bl1 = gap / q(s, BL1[1])        # new value = storage-like, compared with BL1 as measured
    z_vs_ucn = gap / q(s, UCN[1])        # new value = beam-like, compared with UCNtau as measured
    print(f"  {lab:36s}: sharp z = {z_sharp:5.1f}; if it reads ~878: z vs BL1 = {z_vs_bl1:4.1f}; if ~888: z vs UCNtau = {z_vs_ucn:5.1f}")
s_nab_tau = q(0.58, 0.58, 0.19)   # Nab 0.04% lambda (0.58 s) + Vud (0.58 s) + K (0.19 s), from lens-constraints_sm_tau.py
print(f"  Nab lambda at 0.04%: sigma(tau_beta) = {s_nab_tau:.2f} s")
print(f"    if Nab ~ PERKEO III (tau_beta 878.50): z vs BL1 = {(BL1[0]-878.50)/q(s_nab_tau, BL1[1]):.1f}; vs UCNtau = {(878.50-UCN[0])/q(s_nab_tau, UCN[1]):.1f}")
print(f"    if Nab ~ aSPECT 2024 (tau_beta 889.58): z vs UCNtau = {(889.58-UCN[0])/q(s_nab_tau, UCN[1]):.1f}; vs BL1 = {(889.58-BL1[0])/q(s_nab_tau, BL1[1]):.1f}")
