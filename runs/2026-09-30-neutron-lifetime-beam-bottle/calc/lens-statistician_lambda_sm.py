"""Statistician lens, part 2: lambda by method (beta asymmetry A vs proton recoil a), the SM tau_beta
as an extra 'measurement', exotic-branch significance, UCNtau per-year scatter, time stability of the gap,
J-PARC as discriminator between partitions, and Nab/lambda precision needed. Units: s; lambda dimensionless."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from stats_tools import (weighted_mean, grouped_chi2, tension, sigma_to_p, p_to_sigma, min_bayes_factor,
                         prior_needed, precision_needed)
from neutron_beta_decay import tau_beta, br_exotic

def q(*a): return math.sqrt(sum(x * x for x in a))

VUD, SVUD = 0.97361, 0.00032          # GS2023 pairing [U-01, D-43]
P_BEAM, S_P = 887.966, 2.038          # from lens-statistician_combination.py
STORE, S_ST = 878.321, 0.434          # scaled
MAG, S_MAG = 877.815, 0.267

print("== 1. lambda by method ==")
A_route = {"PERKEO III": (1.27641, q(0.00045, 0.00033)), "UCNA": (1.2772, 0.0020),
           "PERKEO II": (1.2748, q(0.0008, 0.5 * (0.0010 + 0.0011)))}
a_route = {"aSPECT 2024": (1.2668, 0.0027), "aCORN Hassan21": (1.2796, 0.0062)}
a_route_alt = {"aSPECT 2024": (1.2668, 0.0027), "aCORN Wietfeldt24": (1.2712, 0.0061)}
for lab, ar in [("aCORN=Hassan21", a_route), ("aCORN=Wietfeldt24 (PDG listing)", a_route_alt)]:
    g = grouped_chi2({"A (beta asym)": ([v for v, _ in A_route.values()], [e for _, e in A_route.values()]),
                      "a (p recoil)": ([v for v, _ in ar.values()], [e for _, e in ar.values()])})
    print("--", lab)
    for k, v in g["groups"].items():
        print("   %-14s mean %.5f +- %.5f chi2 %.2f/%d" % (k, v["mean"], v["error"], v["chi2"], v["dof"]))
    print("   within chi2 %.2f/%d, between chi2 %.2f (z %.2f)" % (g["within_chi2"], g["within_dof"], g["between_chi2"], g["between_z"]))
    gA = g["groups"]["A (beta asym)"]; ga = g["groups"]["a (p recoil)"]
    for nm, grp in [("A-route", gA), ("a-route", ga)]:
        tb = tau_beta(grp["mean"], grp["error"], VUD, SVUD, rc_set="GS2023")
        print("   tau_beta(%s) = %.2f +- %.2f s  [lambda part %.2f, Vud part %.2f, K part %.2f]" %
              (nm, tb["tau"], tb["sigma"], tb["components"]["lambda"], tb["components"]["Vud"], tb["components"]["K(RC,f)"]))
t = tension(1.27641, q(0.00045, 0.00033), 1.2668, 0.0027); print("PERKEO III vs aSPECT 2024: z %.2f" % t["z"])

print("\n== 2. SM tau_beta as arbiter ==")
cases = {"PERKEO III": (1.27641, q(0.00045, 0.00033)), "aSPECT 2024": (1.2668, 0.0027),
         "PDG 2024 avg (S=2.7)": (1.2754, 0.0013)}
for nm, (lam, sl) in cases.items():
    tb = tau_beta(lam, sl, VUD, SVUD, rc_set="GS2023")
    t1 = tension(tb["tau"], tb["sigma"], P_BEAM, S_P); t2 = tension(tb["tau"], tb["sigma"], STORE, S_ST)
    print("%-22s tau_beta %.2f +- %.2f s: vs p-beam z %.2f, vs storage z %.2f; LR(storage-true : pbeam-true) = %.3g"
          % (nm, tb["tau"], tb["sigma"], t1["z"], t2["z"], math.exp(0.5 * (t1["z"]**2 - t2["z"]**2))))
    for tot, stot, lab in [(STORE, S_ST, "storage"), (MAG, S_MAG, "magnetic")]:
        b = br_exotic(tot, stot, tb["tau"], tb["sigma"])
        print("     Br_X = 1 - tau_%s/tau_beta = %.4f +- %.4f (95%% one-sided UL %.4f); needed Br for gap = %.4f -> z of needed vs measured %.2f"
              % (lab, b["br"], b["sigma"], b["upper"], 1 - STORE / P_BEAM, (1 - STORE / P_BEAM - b["br"]) / b["sigma"]))

print("\n== 3. UCNtau per-year scatter (D-27) ==")
yrs = [(877.73, 0.32), (877.80, 0.50), (879.39, 0.89), (878.41, 0.58), (876.93, 0.57)]
w = weighted_mean([v for v, _ in yrs], [e for _, e in yrs])
print("per-year: mean %.3f +- %.3f, chi2 %.2f/%d, p %.3f, S %.2f" % (w["mean"], w["error"], w["chi2"], w["dof"], w["p_consistent"], w["scale_factor"]))

print("\n== 4. Stability of the gap over time (signal fading?) ==")
t18 = tension(888.0, 2.0, 879.4, 0.6); print("CMS 2018 averages [D-33]: gap %.1f s, z %.2f" % (t18["difference"], t18["z"]))
t26 = tension(P_BEAM, S_P, STORE, S_ST); print("2026 (this calc): gap %.2f s, z %.2f" % (t26["difference"], t26["z"]))
tpdg = tension(887.7, q(1.2, 1.9), 878.3, 0.4); print("BL1 vs PDG 2026 UCN avg: gap %.2f s, z %.2f" % (tpdg["difference"], tpdg["z"]))

print("\n== 5. J-PARC discriminates dark decay (e-beam = p-beam) from p-count systematic / strong-field n-n' (e-beam = storage) ==")
for lab, up, dn in [("quoted", q(1.7, 4.0), q(1.7, 3.6)), ("stat x2.29", q(3.89, 4.0), q(3.89, 3.6))]:
    zb = abs(877.2 - P_BEAM) / q(up, S_P)   # facing up toward beam
    zs = abs(877.2 - STORE) / q(up, S_ST)   # J-PARC below storage -> use up side
    lr = math.exp(0.5 * (zb**2 - zs**2))
    print("J-PARC %-10s: z vs p-beam %.2f, vs storage %.2f -> likelihood ratio (e=storage : e=p-beam) %.2f; posterior from 50:50 = %.3f"
          % (lab, zb, zs, lr, lr / (1 + lr)))

print("\n== 6. lambda precision for SM prediction to separate poles ==")
gap = P_BEAM - STORE
dtdl = abs(tau_beta(1.27641, 0.0, VUD, 0.0)["dtau_dlambda"])
svud_part = tau_beta(1.27641, 0.0, VUD, SVUD)["sigma"]
print("dtau/dlambda = %.0f s; Vud+K part = %.3f s" % (dtdl, svud_part))
for z in (3, 5):
    budget = precision_needed(gap, z)
    s_needed = math.sqrt(max(0, budget**2 - svud_part**2 - S_ST**2))
    print("z=%d: tau_beta vs storage sigma budget %.2f s -> lambda sigma <= %.5f (%.3f%% relative)" % (z, budget, s_needed / dtdl, 100 * s_needed / dtdl / 1.2754))
print("Nab target dl/l = 0.04%% -> sigma_lambda %.5f -> tau part %.2f s" % (0.0004 * 1.2754, 0.0004 * 1.2754 * dtdl))
# a-route vs A-route difference: Nab (a-coefficient) needs to separate aSPECT from PERKEO III
d = 1.27641 - 1.2668
for z in (3, 5):
    print("Nab lambda sigma to separate aSPECT-central from PERKEO III at %d sigma (vs PERKEO III err): %.5f" % (z, math.sqrt(max(0, (d / z)**2 - q(0.00045, 0.00033)**2))))
