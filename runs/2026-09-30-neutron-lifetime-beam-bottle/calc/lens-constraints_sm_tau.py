#!/usr/bin/env python3
"""Constraints lens: SM prediction of the beta-decay partial lifetime tau_beta and what it constrains.

Units: lifetimes in s (SI); lambda, Vud, Vus, RC, Br dimensionless.
Inputs (dossier IDs): lambda D-40..D-42; Vud D-43; Vus D-45; Vub D-46; RC D-48; lifetimes D-20, D-23, D-27, D-28.
Tool: .claude/skills/conundrum/scripts/neutron_beta_decay.py (selftest passes), stats_tools.py.

Sections
 A. Re-derivation of U-01 (Delta_R^V cancels when a superallowed Vud is paired with its own inner RC).
 B. tau_beta table: each lambda input x each consistently paired Vud.
 C. Group averages of lambda (beta-asymmetry vs proton-recoil a-coefficient) and their tension.
 D. Exotic branch Br_X = 1 - tau_bottle/tau_beta, and z of tau_beta vs beam and vs bottle.
 E. The lambda and Vud each lifetime requires; first-row CKM sums.
 F. Sensitivities and the lambda precision at which the SM route decides (3 and 5 sigma).
 G. Fierz-term escape: b needed to reconcile PERKEO III lambda with the beam lifetime.
"""
import math
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import neutron_beta_decay as nb  # noqa: E402
import stats_tools as st  # noqa: E402

print("=== A. Re-derivation of U-01: Delta_R^V cancels for a consistently paired superallowed Vud ===")
# Superallowed: |Vud|^2 = C_nuc / [Ft (1 + Delta_R^V)]  ->  Vud^2 (1 + Delta_R^V) = C_nuc/Ft, independent of Delta_R^V.
# Neutron: tau_beta = K0 / [(1+delta'_R)(1+Delta_R^V) Vud^2 (1+3 lam^2)] = K0 Ft / [C_nuc (1+delta'_R)(1+3 lam^2)].
pairings = [  # (label, Vud, sigma_Vud, rc_set or explicit inner RC, source)
    ("GS2023  ", 0.97361, 0.00032, "GS2023", None, "Gorchtein-Seng 2024 Vud with GS2023 Delta_R^V=0.02479 [D-43,D-48]"),
    ("SGPR2018", 0.97366, 0.00015, "SGPR2018", None, "Seng 2018 Vud with Delta_R^V=0.02467 [D-43,D-48]"),
    ("AVG2020 ", 0.97373, 0.00031, "AVG2020", None, "Hardy-Towner 2020 Vud with Delta_R^V=0.02454 [D-43,D-48]"),
    ("CMS2018 ", 0.97420, 0.00021, "CMS2018", None, "CMS 2018 Vud 0.97420(10)(18) with RC 0.03886 [D-49]"),
    ("Ma2024* ", 0.97386, 0.00031, None, 0.02439, "Ma et al. 2024 lattice box Vud; Delta_R^V=0.02479-2*(3.85-3.65)e-3 "
                                                   "is THIS LENS'S INFERENCE (2 x box shift) [D-43]"),
]
lam_P3, s_P3 = 1.27641, math.hypot(0.00045, 0.00033)
print(f"PERKEO III |lambda| = {lam_P3} +- {s_P3:.5f} (stat 45, sys 33 in quadrature) [D-40]")
for lab, vud, svud, rc, dR, src in pairings:
    if rc is None:
        r = nb.tau_beta(lam_P3, s_P3, vud, svud, delta_RV=dR, sig_delta_RV=0.00021)
        one, _, _ = nb.rc_factor(delta_RV=dR)
    else:
        r = nb.tau_beta(lam_P3, s_P3, vud, svud, rc_set=rc)
        one, _, _ = nb.rc_factor(rc)
    print(f"  {lab}: Vud^2*(1+RC) = {vud**2*one:.6f}   tau_beta(PERKEO III) = {r['tau']:.2f} +- {r['sigma']:.2f} s   ({src})")
r_mixed = nb.tau_beta(lam_P3, s_P3, 0.97367, 0.00032, rc_set="CMS2018")
print(f"  MIXED (CMS2018 RC with PDG-2024 Vud 0.97367): tau_beta = {r_mixed['tau']:.2f} s  <- the D-50 bias")

print("\n=== B. tau_beta by lambda input (GS2023 pairing, Vud = 0.97361(32)) and spread over pairings ===")
lams = {  # |lambda|, sigma (symmetric; asymmetric parts symmetrised as quadrature of stat and mean sys)
    "PERKEO III (A)": (1.27641, s_P3),
    "UCNA 2018 (A)": (1.2772, 0.0020),
    "PERKEO II (A)": (1.2748, math.hypot(0.0008, 0.00105)),
    "PDG 2024 avg (S=2.7)": (1.2754, 0.0013),
    "aSPECT 2020 (a)": (1.2677, 0.0028),
    "aSPECT 2024 (a)": (1.2668, 0.0027),
    "aCORN 2021 (a)": (1.2796, 0.0062),
}
tb = {}
for name, (l, sl) in lams.items():
    r = nb.tau_beta(l, sl, 0.97361, 0.00032, rc_set="GS2023")
    spread = []
    for lab, vud, svud, rc, dR, src in pairings:
        rr = nb.tau_beta(l, sl, vud, svud, rc_set=rc) if rc else nb.tau_beta(l, sl, vud, svud, delta_RV=dR)
        spread.append(rr["tau"])
    tb[name] = (r["tau"], r["sigma"])
    comp = r["components"]
    print(f"  {name:22s} |lam|={l:.5f}({sl:.5f}): tau_beta = {r['tau']:.2f} +- {r['sigma']:.2f} s "
          f"[lam {comp['lambda']:.2f}, Vud {comp['Vud']:.2f}, K {comp['K(RC,f)']:.2f}]; pairing range "
          f"{min(spread):.2f}-{max(spread):.2f} s")

print("\n=== C. lambda by method class ===")
A_names = ["PERKEO III (A)", "UCNA 2018 (A)", "PERKEO II (A)"]
a_names = ["aSPECT 2024 (a)", "aCORN 2021 (a)"]
wA = st.weighted_mean([lams[n][0] for n in A_names], [lams[n][1] for n in A_names])
wa = st.weighted_mean([lams[n][0] for n in a_names], [lams[n][1] for n in a_names])
wall = st.weighted_mean([lams[n][0] for n in A_names + a_names], [lams[n][1] for n in A_names + a_names])
for lab, w in (("beta-asymmetry (A) group", wA), ("proton-recoil (a) group", wa), ("all five current", wall)):
    print(f"  {lab}: |lam| = {w['mean']:.5f} +- {w['error']:.5f}, chi2 = {w['chi2']:.2f}/{w['dof']}, S = {w['scale_factor']:.2f}")
g = st.grouped_chi2({"A": ([lams[n][0] for n in A_names], [lams[n][1] for n in A_names]),
                     "a": ([lams[n][0] for n in a_names], [lams[n][1] for n in a_names])})
print(f"  grouped chi2: within {g['within_chi2']:.2f}/{g['within_dof']}, between {g['between_chi2']:.2f}/{g['between_dof']} (z = {g['between_z']:.2f})")
tA = nb.tau_beta(wA["mean"], wA["error"], 0.97361, 0.00032, rc_set="GS2023")
ta = nb.tau_beta(wa["mean"], wa["error"], 0.97361, 0.00032, rc_set="GS2023")
tall = nb.tau_beta(wall["mean"], wall["error_scaled"], 0.97361, 0.00032, rc_set="GS2023")
tb["A-group avg"] = (tA["tau"], tA["sigma"]); tb["a-group avg"] = (ta["tau"], ta["sigma"])
tb["all-5 avg (S-scaled)"] = (tall["tau"], tall["sigma"])
print(f"  tau_beta(A group)  = {tA['tau']:.2f} +- {tA['sigma']:.2f} s")
print(f"  tau_beta(a group)  = {ta['tau']:.2f} +- {ta['sigma']:.2f} s")
print(f"  tau_beta(all five, error x S) = {tall['tau']:.2f} +- {tall['sigma']:.2f} s")
t12 = st.tension(lam_P3, s_P3, 1.2668, 0.0027)
print(f"  PERKEO III vs aSPECT 2024 lambda tension: z = {t12['z']:.2f}")

print("\n=== D. Exotic branch and z-scores of tau_beta against each lifetime class ===")
tau_ucn, s_ucn = 877.82, math.hypot(0.22, 0.20)        # D-27 (upper sys side, conservative)
tau_bl1, s_bl1 = 887.7, math.hypot(1.2, 1.9)            # D-20
tau_jp, e_jp = 877.2, (math.hypot(1.7, 4.0), math.hypot(1.7, 3.6))  # D-23 (up, down)
print(f"  inputs: UCNtau {tau_ucn} +- {s_ucn:.2f} s; BL1 {tau_bl1} +- {s_bl1:.2f} s; J-PARC {tau_jp} +{e_jp[0]:.2f}/-{e_jp[1]:.2f} s")
need = 1 - tau_ucn / tau_bl1
print(f"  Br_X needed for dark decay (1 - tau_UCNtau/tau_BL1) = {need*100:.3f} %")
print(f"  {'lambda route':24s} {'tau_beta':>12s} {'Br_X (%)':>16s} {'95% UL (%)':>10s} {'z vs BL1':>9s} {'z vs UCNtau':>11s} {'z vs J-PARC':>11s}")
for name, (t, s) in tb.items():
    b = nb.br_exotic(tau_ucn, s_ucn, t, s)
    z1 = st.tension(t, s, tau_bl1, s_bl1)["z"]
    z2 = st.tension(t, s, tau_ucn, s_ucn)["z"]
    z3 = st.tension(t, s, tau_jp, e_jp)["z"]
    zneed = (need - b["br"]) / b["sigma"]
    print(f"  {name:24s} {t:7.2f}+-{s:4.2f} {b['br']*100:7.3f}+-{b['sigma']*100:5.3f} {b['upper']*100:10.3f} "
          f"{z1:9.2f} {z2:11.2f} {z3:11.2f}   (needed Br is {zneed:+.2f} sigma from this route's Br_X)")

print("\n=== E. lambda and Vud required by each lifetime; first-row CKM ===")
for lab, t, s in (("UCNtau", tau_ucn, s_ucn), ("Gravitrap", 881.5, math.hypot(0.7, 0.6)), ("BL1", tau_bl1, s_bl1),
                  ("J-PARC", tau_jp, 0.5 * (e_jp[0] + e_jp[1]))):
    L = nb.lambda_from_tau(t, s, 0.97361, 0.00032, rc_set="GS2023")
    V = nb.vud_from_tau(t, s, lam_P3, s_P3, rc_set="GS2023")
    Va = nb.vud_from_tau(t, s, 1.2668, 0.0027, rc_set="GS2023")
    print(f"  {lab:9s} tau={t}: needs |lam| = {L['lam']:.5f} +- {L['sigma']:.5f} (with Vud 0.97361); "
          f"Vud(PERKEO III) = {V['vud']:.5f} +- {V['sigma']:.5f}; Vud(aSPECT 2024) = {Va['vud']:.5f} +- {Va['sigma']:.5f}")
vus = {"Kl3 0.2233(5)": (0.2233, 0.0005), "Kmu2 0.2250(4)": (0.2250, 0.0004), "PDG avg 0.22431(85)": (0.22431, 0.00085)}
vub, svub = 0.0039, 0.0004   # midpoint of inclusive/exclusive [D-46]; |Vub|^2 ~ 1.5e-5, negligible
vud_cases = {"superallowed GS2023 0.97361(32)": (0.97361, 0.00032),
             "superallowed PDG2024 0.97367(32)": (0.97367, 0.00032)}
for lab, t, s in (("UCNtau", tau_ucn, s_ucn), ("BL1", tau_bl1, s_bl1)):
    for ln, (l, sl) in (("PERKEO III", (lam_P3, s_P3)), ("aSPECT 2024", (1.2668, 0.0027))):
        V = nb.vud_from_tau(t, s, l, sl, rc_set="GS2023")
        vud_cases[f"neutron {lab} + {ln}"] = (V["vud"], V["sigma"])
for vl, (v, sv) in vud_cases.items():
    row = []
    for ul, (u, su) in vus.items():
        c = nb.ckm_first_row(v, sv, u, su, vub, svub)
        row.append(f"{ul}: {c['sum']:.5f}({c['sigma']*1e5:.0f}e-5) z={c['z']:+.1f}")
    print(f"  {vl:38s} | " + " | ".join(row))
vuni = math.sqrt(1 - 0.22431**2 - vub**2)
tu = nb.tau_beta(lam_P3, s_P3, vuni, 0.0, rc_set="GS2023")
print(f"  Vud from exact unitarity (Vus PDG avg) = {vuni:.5f}; with PERKEO III lambda this gives tau_beta = {tu['tau']:.2f} s")
for ul, (u, su) in vus.items():
    vu = math.sqrt(1 - u**2 - vub**2)
    print(f"    unitarity with {ul}: Vud = {vu:.5f} -> tau_beta(PERKEO III) = {nb.tau_beta(lam_P3, 0, vu, 0, rc_set='GS2023')['tau']:.2f} s, "
          f"tau_beta(aSPECT 2024) = {nb.tau_beta(1.2668, 0, vu, 0, rc_set='GS2023')['tau']:.2f} s")

print("\n=== F. Sensitivities and the lambda precision at which the SM route decides ===")
r0 = nb.tau_beta(lam_P3, 0.0, 0.97361, 0.0, rc_set="GS2023")
print(f"  dtau/dlambda = {r0['dtau_dlambda']:.1f} s per unit |lambda|; dtau/dVud = {r0['dtau_dVud']:.1f} s per unit Vud")
print(f"  1 s in tau_beta <-> d|lambda| = {1/abs(r0['dtau_dlambda']):.6f} or dVud = {1/abs(r0['dtau_dVud']):.6f}")
dtau = tau_bl1 - tau_ucn
s_vud_part = abs(r0["dtau_dVud"]) * 0.00032
print(f"  gap to resolve = {dtau:.2f} s; Vud(0.00032) contributes {s_vud_part:.2f} s")
for z in (3.0, 5.0):
    # (i) sharp hypotheses tau_beta = tau_bottle vs tau_beta = tau_beam (beam and bottle errors ignored)
    tot = dtau / z
    sl = math.sqrt(max(tot**2 - s_vud_part**2, 0)) / abs(r0["dtau_dlambda"])
    # (ii) include UCNtau error (0.30 s): reject "tau_beta = tau_bottle" when truth is tau_beam
    tot2 = math.sqrt(max((dtau / z) ** 2 - s_ucn**2, 0))
    sl2 = math.sqrt(max(tot2**2 - s_vud_part**2, 0)) / abs(r0["dtau_dlambda"])
    # (iii) include BL1 error (2.26 s): reject "tau_beta = tau_beam" when truth is tau_bottle
    rem = (dtau / z) ** 2 - s_bl1**2
    txt = (f"sigma_lambda <= {math.sqrt(max(rem - s_vud_part**2, 0))/abs(r0['dtau_dlambda']):.5f}" if rem > s_vud_part**2
           else f"IMPOSSIBLE (BL1 error alone caps z at {dtau/s_bl1:.2f})")
    print(f"  z={z:.0f}: (i) sharp: sigma_tau_beta <= {tot:.2f} s -> sigma_lambda <= {sl:.5f} "
          f"(= {sl/lam_P3*100:.3f} %); (ii) vs UCNtau error: sigma_lambda <= {sl2:.5f}; (iii) vs BL1 error: {txt}")
print(f"  lambda gap between the routes: {lam_P3-1.2668:.5f} -> {abs(r0['dtau_dlambda'])*(lam_P3-1.2668):.2f} s in tau_beta")
print(f"  Nab target d|lam|/|lam| = 0.04% -> d|lam| = {0.0004*lam_P3:.5f} -> {0.0004*lam_P3*abs(r0['dtau_dlambda']):.2f} s in tau_beta [D-107]")
for z in (3.0, 5.0):
    print(f"  a new lambda measurement separating PERKEO III (0.00056) from aSPECT 2024 (0.0027) at {z:.0f} sigma against the "
          f"FARTHER of the two needs sigma <= {math.sqrt(max(((lam_P3-1.2668)/z)**2 - 0.00056**2, 0)):.5f} "
          f"(vs PERKEO III error) and <= {math.sqrt(max(((lam_P3-1.2668)/z)**2 - 0.0027**2, 0)):.5f} (vs aSPECT error; 0 = impossible)")

print("\n=== G. Fierz-term escape ===")
# Rate with a Fierz term: Gamma = Gamma_SM (1 + b <m_e/E_e>), <.> over the beta spectrum (Fermi function, recoil endpoint).
W0 = nb.endpoint_W0()
N = 20000
num = den = 0.0
for i in range(1, N):
    W = 1 + (W0 - 1) * i / N
    p = math.sqrt(W * W - 1)
    w = nb.fermi_function(W, "rel") * p * W * (W0 - W) ** 2
    num += w / W
    den += w
me_E = num / den
num2 = den2 = 0.0
for i in range(1, int(1.5 * N)):
    W = 1 + (W0 - 1) * i / (1.5 * N)
    p = math.sqrt(W * W - 1)
    w = nb.fermi_function(W, "rel") * p * W * (W0 - W) ** 2
    num2 += w / W
    den2 += w
print(f"  W0 = {W0:.5f} m_e; <m_e/E_e> = {me_E:.5f} (N={N}); {num2/den2:.5f} (N={int(1.5*N)}) convergence check")
t_sm = tb["PERKEO III (A)"][0]
b_needed = (t_sm / tau_bl1 - 1) / me_E
print(f"  b needed so that tau_beta(PERKEO III lambda) = BL1 {tau_bl1} s: b = {b_needed:+.4f} "
      f"(rate effect only; b also biases the lambda extracted from A, which this ignores)")
print(f"  compare aSPECT 2024 free-fit b = -0.0098 +- 0.0193 [D-42]: z = {(b_needed+0.0098)/0.0193:+.2f}; "
      f"superallowed b_F <= 0.0033 (90% CL) constrains only the scalar (Fermi) part [D-66]")
