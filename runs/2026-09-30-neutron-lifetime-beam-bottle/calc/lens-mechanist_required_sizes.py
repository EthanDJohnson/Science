"""Mechanist lens: required size of each systematic sub-hypothesis, in SI units (s, s^-1, m^-3, Pa).

Inputs from the dossier (values as quoted): BL1 887.7 +- 1.2 +- 1.9 s [D-20]; Sussex-ILL 889.2 +- 3.0 +- 3.8 s
(brief lead, unverified) [D-22]; UCNtau 877.82 +- 0.22 (+0.20/-0.17) s [D-27]; Gravitrap 881.5 +- 0.7 +- 0.6 s
[D-28]; J-PARC 877.2 +- 1.7 (+4.0/-3.6) s [D-23]; BL1 budget items [D-21]; Fluence corr. unc 0.5 s [D-20].
Items marked ASSUMED are order-of-magnitude inputs not in the dossier.
"""
import math, sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import neutron_beta_decay as nbd

def wmean(vals):
    w = [1/s**2 for _, s in vals]
    m = sum(v*wi for (v, _), wi in zip(vals, w))/sum(w)
    return m, math.sqrt(1/sum(w))

bl1 = (887.7, math.hypot(1.2, 1.9))
sus = (889.2, math.hypot(3.0, 3.8))
ucnt = (877.82, math.hypot(0.22, 0.185))
grav = (881.5, math.hypot(0.7, 0.6))
beam = wmean([bl1, sus])
print(f"proton-beam mean (BL1 + Sussex-ILL lead): {beam[0]:.2f} +- {beam[1]:.2f} s")
print(f"BL1 alone: {bl1[0]:.2f} +- {bl1[1]:.2f} s")
for name, bot in [("UCNtau", ucnt), ("Gravitrap", grav)]:
    for bn, b in [("beam mean", beam), ("BL1", bl1)]:
        f = 1 - bot[0]/b[0]
        dG = 1/bot[0] - 1/b[0]
        print(f"{bn} vs {name}: dtau = {b[0]-bot[0]:.2f} s, fraction = {f*100:.3f} %, dGamma = {dG:.3e} s^-1")

tau_b, tau_s = beam[0], ucnt[0]
f_req = 1 - tau_s/tau_b
dtau = tau_b - tau_s
print(f"\nREFERENCE for this lens: required fractional shift f = {f_req*100:.3f} % (dtau = {dtau:.2f} s)")

# --- proton-counting beam: tau = L * Ndot_alpha * eps_p / (Ndot_p * eps_0 * v_0)  (Nico 2005 eq. 6)
print("\n[Proton beam] tau_meas/tau_true = (eps_p,assumed/eps_p,true) * (eps_0,true/eps_0,assumed)")
print(f"  unrecognised proton loss fraction needed: {f_req*100:.2f} %  (proton-efficiency overestimated)")
print(f"  OR neutron-monitor efficiency underestimated by {f_req/(1-f_req)*100:.2f} % (eps_0,true/eps_0,assumed = {1/(1-f_req):.4f})")
items = {"fluence correction unc (2013)": 0.5, "systematics unassociated with fluence (2013)": 1.7,
         "trap nonlinearity correction (size)": 5.3, "trap nonlinearity unc": 0.8,
         "absorption by 6Li correction (size)": 5.4, "beam halo unc": 1.0, "proton backscatter unc": 0.4,
         "Si scattering unc": 0.5, "BL1 total sys (2013)": 1.9, "BL1 total (2013)": bl1[1]}
for k, v in items.items():
    print(f"  dtau / {k} ({v} s) = {dtau/v:.1f}")
print(f"  2013 Alpha-Gamma fluence re-calibration moved tau by +1.4 s = {1.4/887.7*100:.3f} % (sign: away from bottles)")

# --- storage-time scaling of any residual-gas proton loss (BL1 trapping periods 5 and 10 ms)
print("\n[Proton beam: residual-gas loss]  loss prob = n * sigma * v * t_store")
Ep_mean_eV = 300.0            # ASSUMED mean decay-proton kinetic energy in trap (spectrum endpoint 751 eV)
mp, e = 1.67262192e-27, 1.602176634e-19
v = math.sqrt(2*Ep_mean_eV*e/mp)
print(f"  proton speed at {Ep_mean_eV:.0f} eV: {v:.3e} m/s")
kB = 1.380649e-23
for t_cycle in (10e-3, 5e-3):
    t_store = t_cycle/2
    for sigma in (1e-20, 1e-19):   # ASSUMED H+ + H2 charge-transfer cross section range, m^2
        n = f_req/(sigma*v*t_store)
        print(f"  cycle {t_cycle*1e3:.0f} ms (mean store {t_store*1e3:.1f} ms), sigma={sigma:.0e} m^2: "
              f"n_H2 needed = {n:.2e} m^-3 -> p(300 K) = {n*kB*300:.2e} Pa = {n*kB*300/100:.2e} mbar; p(77 K) = {n*kB*77:.2e} Pa")
print("  If loss = 1.13% at 10 ms cycle, at 5 ms cycle loss = 0.56%:")
print(f"  predicted tau(10 ms) - tau(5 ms) = {tau_s/(1-f_req) - tau_s/(1-f_req/2):.2f} s")
print(f"  Caylor 2025 H2 estimate ~0.3% loss -> dtau = {0.003*887.7:.2f} s = {0.003/f_req*100:.0f}% of gap")

# --- bottle: unidentified loss rate
dG = 1/tau_s - 1/tau_b
print(f"\n[Bottle] extra loss rate needed = {dG:.3e} s^-1 (time constant {1/dG:.3e} s = {1/dG/86400:.2f} d)")
# residual-gas upscattering: rate = n * sigma_s * v_gas (1/v law: independent of UCN speed)
gases = {"N2 (sigma~20 b, v~475 m/s)": (20e-28, 475.0), "He (sigma~0.8 b, v~1250 m/s)": (0.8e-28, 1250.0),
         "H2 (sigma~160 b, v~1770 m/s)": (160e-28, 1770.0)}   # ASSUMED order-of-magnitude values, 300 K
for g, (s, vg) in gases.items():
    n = dG/(s*vg)
    print(f"  {g}: n needed = {n:.2e} m^-3 -> p(300 K) = {n*kB*300:.2e} Pa = {n*kB*300/100:.2e} mbar")
# magnetic trap: depolarisation (spin flip -> untrapped)
print(f"  magnetic trap: spin-flip probability per second needed = {dG:.2e}; per 1000 s hold = {1-math.exp(-dG*1000):.3e}")
# material bottle: loss per wall collision needed at typical collision rates (ASSUMED 5-50 /s)
for nu in (5.0, 20.0, 50.0):
    print(f"  material bottle, collision rate {nu:.0f} /s: extra loss per bounce needed = {dG/nu:.2e}")

# --- J-PARC: excess background fraction versus needed shift
print(f"\n[J-PARC] needed upward shift to reach proton beam = {tau_b-877.2:.1f} s = {(tau_b/877.2-1)*100:.2f} % of S_beta")
print("  observed background: 4.9-5.4% of S_beta at 100 kPa vs 1.2-1.3% MC; 3.1-3.3% at 50 kPa vs 0.65-0.67% [D-25]")
print(f"  excess (obs - MC) at 100 kPa ~ {4.9-1.3:.1f}-{5.4-1.2:.1f} %, at 50 kPa ~ {3.1-0.67:.1f}-{3.3-0.65:.1f} %")

# --- SM tau_beta (GS2023 pairing, U-01) and exotic branch
print("\n[SM] tau_beta from lambda, GS2023 with Vud 0.97361(32) [U-01 pairing]")
for name, lam, sl in [("PERKEO III", 1.27641, 0.00056), ("aSPECT 2024", 1.2668, 0.0027), ("PDG 2024", 1.2754, 0.0013)]:
    r = nbd.tau_beta(lam, sl, 0.97361, 0.00032, rc_set="GS2023")
    bx = nbd.br_exotic(tau_s, ucnt[1], r["tau"], r["sigma"])
    print(f"  {name}: tau_beta = {r['tau']:.2f} +- {r['sigma']:.2f} s; Br_X(UCNtau) = {bx['br']*100:.3f} +- {bx['sigma']*100:.3f} %, 95% upper {bx['upper']*100:.3f} %")
    print(f"     proton beam {tau_b:.1f} s vs tau_beta: {(tau_b-r['tau'])/math.hypot(beam[1], r['sigma']):.2f} sigma")
