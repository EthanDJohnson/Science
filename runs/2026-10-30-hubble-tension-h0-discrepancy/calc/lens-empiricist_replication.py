"""Empiricist lens: H0 by replication class (who measured it, with what, independent of whom).

Units: H0 in km/s/Mpc; magnitudes in mag. Inputs are dossier anchors (IDs in comments).
Stat and sys errors are combined in quadrature (total_error) where the source quotes them separately.
Asymmetric errors are symmetrised (mean of up and down) only for the weighted means; tensions use
the side facing the other value (stats_tools.tension).
Correlations: NGC 4258 is shared by SH0ES, CCHP, SBF and the maser sample (Stiskalek treats NGC 4258
separately, so the maser H0 of 5 other galaxies is nearly independent of it). The shared-anchor term
is shown explicitly as a sensitivity case.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from stats_tools import tension, weighted_mean, grouped_chi2, total_error, min_bayes_factor, sigma_to_p

def sym(e):
    return 0.5 * (e[0] + e[1]) if isinstance(e, tuple) else e

# ---- local results (current values, dossier section 2) ----
SH0ES = (73.49, 0.93)                                  # D-20 Cepheid-SN HST+JWST (SH0ES team)
CCHP = (70.39, total_error(1.22, 1.33, 0.70))          # D-24 TRGB-SN (CCHP team)
SBF = (73.8, total_error(0.7, 2.3))                    # D-29 SBF ladder (Jensen 2025)
TF = (73.3, total_error(2.1, 3.5))                     # D-30 Tully-Fisher (same hosts; not independent)
TDC = (71.1, (2.4, 2.3))                               # D-31 TDCOSMO-2026, preprint
MAS = (71.6, 3.7)                                      # D-32 masers, stat only, preprint
GW = (71.7, (9.4, 7.5))                                # D-33 GWTC-5.0 sirens, preprint
# ---- early results ----
CMB = (67.19, 0.38)                                    # D-44 CMB-SPA
BBN = (68.50, 0.58)                                    # D-45 DESI DR2 BAO+BBN
INV = (67.19, (0.66, 0.64))                            # D-48 inverse ladder (r_d from CMB; correlated with CMB)
PL4 = (67.64, 0.52)                                    # D-41 Planck PR4 alone

print("== Inputs (km/s/Mpc, total 1-sigma) ==")
for n, v in [("SH0ES", SH0ES), ("CCHP", CCHP), ("SBF", SBF), ("TF", TF), ("TDCOSMO", TDC),
             ("masers", MAS), ("sirens", GW), ("CMB-SPA", CMB), ("BAO+BBN", BBN), ("inverse ladder", INV),
             ("Planck PR4", PL4)]:
    print(f"  {n:15s} {v[0]:6.2f} +/- {v[1] if not isinstance(v[1], tuple) else v[1]}")

print("\n== Tension of each local class vs CMB-SPA and vs BAO+BBN (two-sided, uncorrelated) ==")
for n, v in [("SH0ES", SH0ES), ("CCHP TRGB", CCHP), ("SBF", SBF), ("TF", TF), ("TDCOSMO", TDC),
             ("masers", MAS), ("sirens", GW)]:
    t1 = tension(v[0], v[1], CMB[0], CMB[1]); t2 = tension(v[0], v[1], BBN[0], BBN[1])
    print(f"  {n:10s} vs CMB-SPA: {t1['z']:.2f} sigma (diff {t1['difference']:+.2f}); vs BAO+BBN: {t2['z']:.2f} sigma")

def wm(name, items):
    vals = [i[0] for i in items]; errs = [sym(i[1]) for i in items]
    r = weighted_mean(vals, errs)
    t = tension(r['mean'], r['error'], CMB[0], CMB[1]); tb = tension(r['mean'], r['error'], BBN[0], BBN[1])
    print(f"  {name:48s} mean {r['mean']:.2f} +/- {r['error']:.2f} (chi2 {r['chi2']:.2f}/{r['dof']}, S {r['scale_factor']:.2f}); "
          f"vs CMB-SPA {t['z']:.2f} sigma; vs BAO+BBN {tb['z']:.2f} sigma")
    return r

print("\n== Combinations by replication class ==")
one_step = wm("one-step only (TDCOSMO+masers+sirens)", [TDC, MAS, GW])
not_shoes = wm("all local, SH0ES-team results excluded (CCHP+SBF+1-step)", [CCHP, SBF, TDC, MAS, GW])
no_ceph_no_sn = wm("no SN Ia at all (SBF + 1-step)", [SBF, TDC, MAS, GW])
allloc = wm("all local naive (SH0ES+CCHP+SBF+1-step; overcounts NGC4258)", [SH0ES, CCHP, SBF, TDC, MAS, GW])
early = wm("early naive (CMB-SPA + BAO+BBN)", [CMB, BBN])

# Shared NGC 4258 anchor: ~1.5% in distance (dossier section 6, RE gaps) -> 1.5% of H0 fully correlated
# between CCHP and SBF (both NGC 4258-only anchored). Sensitivity: add it as a common floor.
anchor = 0.015 * 71.0
print(f"\n  NGC 4258 common-anchor term ~1.5% of H0 = {anchor:.2f} km/s/Mpc (applies to CCHP and SBF jointly)")
# Approximate: combine CCHP and SBF with independent parts only, then add anchor in quadrature
cchp_ind = math.sqrt(max(CCHP[1]**2 - anchor**2, 0)); sbf_ind = math.sqrt(max(SBF[1]**2 - anchor**2, 0))
r_lad = weighted_mean([CCHP[0], SBF[0]], [cchp_ind, sbf_ind])
lad_err = math.sqrt(r_lad['error']**2 + anchor**2)
r2 = weighted_mean([r_lad['mean'], TDC[0], MAS[0], GW[0]], [lad_err, sym(TDC[1]), MAS[1], sym(GW[1])])
t2 = tension(r2['mean'], r2['error'], CMB[0], CMB[1])
print(f"  non-SH0ES local with anchor correlation: {r2['mean']:.2f} +/- {r2['error']:.2f}; vs CMB-SPA {t2['z']:.2f} sigma")

print("\n== Grouped chi2: are local classes mutually consistent? ==")
g = grouped_chi2({"Cepheid-SN (SH0ES)": ([SH0ES[0]], [SH0ES[1]]),
                  "TRGB-SN (CCHP)": ([CCHP[0]], [CCHP[1]]),
                  "non-SN ladder": ([SBF[0]], [SBF[1]]),
                  "one-step": ([TDC[0], MAS[0], GW[0]], [sym(TDC[1]), MAS[1], sym(GW[1])])})
for k, v in g.items():
    print(f"  {k}: {v}" if k != "groups" else "  groups: " + "; ".join(f"{a}: mean {b['mean']:.2f}+/-{b['error']:.2f}" for a, b in v.items()))
t_sc = tension(SH0ES[0], SH0ES[1], CCHP[0], CCHP[1])
print(f"  SH0ES vs CCHP (treated independent; they share NGC4258 and some hosts): {t_sc['z']:.2f} sigma")

print("\n== Gap in magnitudes, 5 log10(H_loc/H_early) ==")
for n, h in [("SH0ES/CMB-SPA", SH0ES[0]), ("CCHP/CMB-SPA", CCHP[0]), ("one-step/CMB-SPA", one_step['mean']),
             ("non-SH0ES local/CMB-SPA", not_shoes['mean'])]:
    print(f"  {n:26s} {5*math.log10(h/CMB[0]):.3f} mag; {100*(h/CMB[0]-1):.2f} %")

print("\n== Evidence ceiling: minimum Bayes factor for each significance ==")
for n, z in [("one-step vs CMB", tension(one_step['mean'], one_step['error'], CMB[0], CMB[1])['z']),
             ("non-SH0ES local vs CMB", t2['z']),
             ("SH0ES vs CMB", tension(SH0ES[0], SH0ES[1], CMB[0], CMB[1])['z'])]:
    p = sigma_to_p(z, two_sided=True)
    print(f"  {n:24s} z={z:.2f}, p={p:.3g}, min BF = {min_bayes_factor(p)}")

print("\n== Precision a one-step (ladder-free) method needs to separate 73.0 from 67.2 / 70.0 at 3 and 5 sigma ==")
for target, other in [(73.0, 67.19), (70.0, 67.19), (73.0, 70.0)]:
    d = abs(target - other)
    for z in (3, 5):
        need = math.sqrt(max((d / z)**2 - CMB[1]**2 * (1 if other == 67.19 else 0), 0))
        print(f"  separate {target} from {other} at {z} sigma: sigma_H0 <= {need:.2f} km/s/Mpc = {100*need/target:.2f} %")

print("\n== Sensitivity: add the two lensed-supernova time-delay H0 values (single-object, cluster lenses) ==")
REF = (64.8, (4.4, 4.3))   # Kelly et al. 2023, Science 380, abh1322 (8 cluster models, blinded)
HOPE = (75.4, (8.1, 5.5))  # SN H0pe (Agrawal et al. 2026 abstract quoting the H0pe result)
wm("one-step + lensed SNe (Refsdal, H0pe)", [TDC, MAS, GW, REF, HOPE])
wm("non-SH0ES local + lensed SNe", [CCHP, SBF, TDC, MAS, GW, REF, HOPE])
print("PASS: script completed")
