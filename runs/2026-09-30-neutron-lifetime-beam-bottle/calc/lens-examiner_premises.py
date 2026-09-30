#!/usr/bin/env python3
"""Examiner lens: premise tests for the neutron-lifetime puzzle.
Units: SI (lifetimes in s, rates in s^-1). lambda dimensionless.
Inputs: dossier D-20, D-22 (unverified lead), D-23/24/25, D-27..D-30, D-40..D-43.
Symmetrisation of asymmetric errors is stated at each use.
"""
import math, sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/tools")
import stats_tools as st
import neutron_beta_decay as nb

q = lambda *p: math.sqrt(sum(x * x for x in p))

# ---- measurements (value s, symmetric total error s) ----
BL1 = (887.7, q(1.2, 1.9))                 # D-20
SILL = (889.2, q(3.0, 3.8))                # D-22 (brief lead, UNVERIFIED)
JP_up, JP_dn = q(1.7, 4.0), q(1.7, 3.6)    # D-23
JP = (877.2, 0.5 * (JP_up + JP_dn))        # symmetrised as mean of sides
S_jp = math.sqrt(15.8 / 3)                 # D-23 internal chi2/dof
JP_inf = (877.2, 0.5 * (q(1.7 * S_jp, 4.0) + q(1.7 * S_jp, 3.6)))  # stat inflated by internal scale factor
UCNt = (877.82, q(0.22, 0.5 * (0.20 + 0.17)))  # D-27, sys symmetrised as mean
GRAV = (881.5, q(0.7, 0.6))                # D-28
EZH = (878.3, q(1.6, 1.0))                 # D-30 (search-summary)
MAMBO = (880.7, q(1.3, 1.2))               # D-29
STEY = (882.5, q(1.4, 1.5))                # D-29
ARZ = (880.2, 1.2)                         # D-29
SER05 = (878.5, q(0.7, 0.3))               # D-29

def g(*ms):
    return ([m[0] for m in ms], [m[1] for m in ms])

print("Inputs (value, symmetric total error) [s]:")
for n, m in [("BL1", BL1), ("SussexILL(unverified)", SILL), ("J-PARC", JP), ("J-PARC inflated", JP_inf),
             ("UCNtau", UCNt), ("Gravitrap", GRAV), ("Ezhov", EZH), ("MAMBOII", MAMBO), ("Steyerl", STEY),
             ("Arzumanov", ARZ), ("Serebrov05", SER05)]:
    print(f"  {n:24s} {m[0]:8.2f} +- {m[1]:.2f}")
print(f"  J-PARC internal scale factor sqrt(15.8/3) = {S_jp:.3f}")

mat = [GRAV, MAMBO, STEY, ARZ, SER05]
magn = [UCNt, EZH]

def report(name, groups):
    r = st.grouped_chi2(groups)
    print(f"\n== Partition: {name}")
    for k, v in r["groups"].items():
        print(f"   {k:28s} mean {v['mean']:8.2f} +- {v['error']:.2f} s  chi2 {v['chi2']:.2f}/{v['dof']}")
    print(f"   within chi2 = {r['within_chi2']:.2f}/{r['within_dof']} (p={r['p_within']:.3g}); "
          f"between chi2 = {r['between_chi2']:.2f}/{r['between_dof']} (p={r['p_between']:.3g}, z={r['between_z']:.2f})")
    pl = r["pooled"]
    print(f"   pooled {pl['mean']:.2f} +- {pl['error']:.2f} s chi2 {pl['chi2']:.2f}/{pl['dof']} S={pl['scale_factor']:.2f}")
    return r

# P1 beam vs bottle (J-PARC counted as beam)
report("P1 beam(BL1,SILL,JPARC) vs bottle(all)", {
    "beam": g(BL1, SILL, JP), "bottle": g(*(mat + magn))})
# P2 proton-counting vs everything else == strong-field (4.6-5 T) vs weak-field (<~1 T)
report("P2 proton-counting (=strong field) vs rest", {
    "proton-counting": g(BL1, SILL), "rest": g(JP, *(mat + magn))})
# P2b same with J-PARC inflated
report("P2b as P2, J-PARC error inflated by internal S", {
    "proton-counting": g(BL1, SILL), "rest": g(JP_inf, *(mat + magn))})
# P4 BL1 vs everything (drop unverified SILL)
report("P4 BL1 alone vs everything else (SILL dropped)", {
    "BL1": g(BL1), "rest": g(JP, *(mat + magn))})
# P5 four classes
report("P5 four classes", {"proton beam": g(BL1, SILL), "electron beam": g(JP),
                           "material": g(*mat), "magnetic": g(*magn)})
# P6 material vs magnetic only (second anomaly)
report("P6 material vs magnetic", {"material": g(*mat), "magnetic": g(*magn)})
# P6b material without Steyerl/Serebrov05 (only the three newest) vs magnetic
report("P6b modern material (Gravitrap,MAMBO,Arz) vs magnetic", {"material": g(GRAV, MAMBO, ARZ), "magnetic": g(*magn)})

# ---- J-PARC discrimination (asymmetric errors, side facing) ----
print("\n== J-PARC discrimination")
for lab, jst in [("as quoted", 1.7), ("stat inflated by S", 1.7 * S_jp)]:
    e = (q(jst, 4.0), q(jst, 3.6))
    t_beam = st.tension(877.2, e, BL1[0], BL1[1])
    t_ucn = st.tension(877.2, e, UCNt[0], UCNt[1])
    t_grav = st.tension(877.2, e, GRAV[0], GRAV[1])
    # likelihood ratio J-PARC | 'true e-rate = bottle(UCNtau)' vs '= beam(BL1)'
    lr = math.exp(-0.5 * (t_ucn["z"] ** 2 - t_beam["z"] ** 2))
    print(f"  [{lab}] J-PARC-BL1 {t_beam['difference']:.2f} s, z={t_beam['z']:.2f}; J-PARC-UCNtau z={t_ucn['z']:.2f}; "
          f"J-PARC-Gravitrap z={t_grav['z']:.2f}; likelihood ratio bottle:beam = {lr:.1f}")
# per-condition spread: drop the outlier and keep only 50kPa/newSFC
print("  per-condition (stat only): 870.9(3.5) 868.3(4.0) 868.2(7.7) 884.8(2.4)")
wm3 = st.weighted_mean([870.9, 868.3, 868.2], [3.5, 4.0, 7.7])
print(f"  three low conditions: {wm3['mean']:.2f} +- {wm3['error']:.2f} (stat) s; outlier 884.8(2.4) -> tension with BL1 "
      f"z={st.tension(884.8, q(2.4, 3.1), 887.7, BL1[1])['z']:.2f} (sys ~3.1 s symmetrised)")

# ---- Sizes the candidates need ----
print("\n== Required sizes")
tb, tt = BL1[0], UCNt[0]
dG = 1 / tt - 1 / tb
print(f"  missing rate 1/UCNtau - 1/BL1 = {dG:.3e} s^-1 ; time constant {1/dG:.3e} s = {1/dG/86400:.2f} d")
print(f"  fractional gap 1 - UCNtau/BL1 = {1 - tt/tb:.4%}")
print(f"  gap / BL1 total error = {(tb-tt)/BL1[1]:.2f}; gap / BL1 sys = {(tb-tt)/1.9:.2f}; gap / BL1 'unassociated' 1.7 s = {(tb-tt)/1.7:.2f}")
# missing rate needed in material bottle to pull 881.5 down? (sign: an unidentified loss shortens bottles)
print(f"  Gravitrap - UCNtau = {GRAV[0]-UCNt[0]:.2f} s -> extra loss in UCNtau relative to Gravitrap {1/UCNt[0]-1/GRAV[0]:.2e} s^-1")

# ---- SM arbiter (U-01 consistent pairing: GS2023 with Vud 0.97361(32)) ----
print("\n== SM tau_beta (rc GS2023, Vud 0.97361(32))")
lams = {"PERKEO III": (1.27641, 0.00056), "UCNA": (1.2772, 0.0020), "PERKEO II": (1.2748, 0.00105),
        "PDG2024 avg": (1.2754, 0.0013), "aSPECT 2024": (1.2668, 0.0027), "aCORN": (1.2796, 0.0062)}
for n, (l, sl) in lams.items():
    r = nb.tau_beta(l, sl, 0.97361, 0.00032, rc_set="GS2023")
    zb = st.tension(r["tau"], r["sigma"], *BL1)["z"]
    zu = st.tension(r["tau"], r["sigma"], *UCNt)["z"]
    print(f"  {n:12s} tau_beta = {r['tau']:.2f} +- {r['sigma']:.2f} s ; z vs BL1 {zb:.2f}, z vs UCNtau {zu:.2f}")
lb = nb.lambda_from_tau(BL1[0], BL1[1], 0.97361, 0.00032, rc_set="GS2023")
lu = nb.lambda_from_tau(UCNt[0], UCNt[1], 0.97361, 0.00032, rc_set="GS2023")
print(f"  lambda implied by BL1 = {lb['lam'] if 'lam' in lb else lb}")
print(f"  lambda implied by UCNtau = {lu['lam'] if 'lam' in lu else lu}")
tl = st.tension(1.27641, 0.00056, 1.2668, 0.0027)
print(f"  PERKEO III vs aSPECT 2024 lambda tension z={tl['z']:.2f}")
# lambda A-route vs a-route: which lifetime does each 'pick'?
r = nb.tau_beta(1.27641, 0.00056, 0.97361, 0.00032, rc_set="GS2023")
br = nb.br_exotic(UCNt[0], UCNt[1], r["tau"], r["sigma"])
print(f"  Br_X (UCNtau vs PERKEO III SM) = {br['br']:.4%} +- {br['sigma']:.4%}; 95% upper {br['upper']:.4%}")
br2 = nb.br_exotic(UCNt[0], UCNt[1], *[nb.tau_beta(1.2668, 0.0027, 0.97361, 0.00032)[k] for k in ("tau", "sigma")])
print(f"  Br_X (UCNtau vs aSPECT-2024 SM) = {br2['br']:.4%} +- {br2['sigma']:.4%}")
# Vud shift that would move SM(PERKEO III) to the beam value
v_beam = nb.vud_from_tau(BL1[0], BL1[1], 1.27641, 0.00056, rc_set="GS2023")
print(f"  Vud needed for BL1 with PERKEO III: {v_beam['vud']:.5f} +- {v_beam['sigma']:.5f}; shift from 0.97361 = {v_beam['vud']-0.97361:+.5f}")
# first-row: what shift of Vud would close CKM deficit -0.00166?
dv = 0.00166 / (2 * 0.97361)
print(f"  Vud shift that would close the 0+ row deficit (-0.00166): {dv:+.5f} -> changes SM tau_beta by {-2*r['tau']*dv/0.97361:+.2f} s (toward shorter)")

# ---- Future: precision to separate 'J-PARC ~ bottle' vs 'J-PARC ~ beam' ----
print("\n== Precision a future test needs (gap delta = BL1 - UCNtau)")
d = tb - tt
for z in (3, 5):
    print(f"  total sigma on a single new result to discriminate {d:.2f} s at {z} sigma: {st.precision_needed(d, z):.2f} s")

# ---- Look-elsewhere over partition choice, and Bayes-factor bounds ----
print("\n== Look-elsewhere over partitions and Bayes-factor bounds")
for lab, z in [("P2 proton-counting vs rest", 4.67), ("P1 beam vs bottle", 4.06), ("P4 BL1 vs rest", 4.12),
               ("P6 material vs magnetic", 3.88)]:
    p = st.sigma_to_p(z, two_sided=True)
    pg = st.sidak_global_p(p, 5)
    zg = st.p_to_sigma(pg, two_sided=True)
    mb = st.min_bayes_factor(p)
    print(f"  {lab}: local p={p:.2e} (z={z}); Sidak x5 partitions -> p={pg:.2e}, z={zg:.2f}; min Bayes factor {mb}")
