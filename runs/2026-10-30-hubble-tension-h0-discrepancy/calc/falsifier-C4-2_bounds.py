"""Falsifier C4-2 (bounds angle): independent constraints on late-time new physics.

Units: H0 in km/s/Mpc; pressures and bulk moduli in GPa; fluxes in W/m^2; temperatures in K;
G ratios, exponents dimensionless.

A. Variant (i) smooth H(z): inverse distance ladder (D-48) vs anchored ladder (D-22).
B. Variant (ii) G step: Earth's radius response to a G change for a self-gravitating body with
   effective adiabatic index gamma = dlnP/dlnrho = K/P (homologous polytrope: R ∝ G^(-1/(3*gamma-4))).
   Days per year N = T_year/T_day with T_year ∝ G^-2 (orbital angular momentum conserved) and
   T_day ∝ I ∝ R^2 (spin angular momentum conserved).
   Perivolaropoulos & Ruchika 2025 (arXiv:2508.04395, eq. 12) assume R ∝ G^-1, i.e. gamma = 5/3.
C. Solar insolation step: L ∝ G^a (a = 4: rebuttal; a = 5.6: Banik et al. 2025) and r ∝ 1/G.
D. Variant (ii) non-gravitational SN-only step: one-step and SBF H0 vs the 'true' early H0.
"""
import math

print("=== A. Variant (i): inverse ladder vs anchored ladder ===")
inv = [(67.19, 0.65, "inverse ladder, cosmography (D-48)"), (67.67, 0.685, "inverse ladder, flat LCDM (D-48)")]
lad = (73.264, 0.806)
for v, s, lab in inv:
    t = (lad[0] - v) / math.hypot(lad[1], s)
    print(f"{lab}: {v} +- {s}; H0DN {lad[0]} +- {lad[1]} -> difference {lad[0]-v:.2f} km/s/Mpc = {t:.2f} sigma")
print("Any H(z) change with standard r_d leaves the inverse-ladder H0 (SN-shape anchored at z->0) at these values.")

print("\n=== B. Earth radius response and days per year across a G step ===")
# Approximate PREM values (from memory, illustrative; GPa): (label, P, K)
prem = [("upper mantle ~400 km", 13.0, 200.0), ("mid mantle ~1500 km", 60.0, 350.0),
        ("lowermost mantle (CMB)", 136.0, 656.0), ("outer core top", 136.0, 644.0),
        ("centre", 364.0, 1425.0)]
for lab, P, K in prem:
    g = K / P
    x = -1.0 / (3 * g - 4)
    print(f"{lab}: P = {P} GPa, K = {K} GPa, gamma = K/P = {g:.2f}, dlnR/dlnG = {x:+.3f}")
print("gamma needed for R ∝ G^-1 (rebuttal eq. 12): 3*gamma-4 = 1 -> gamma = 5/3 = 1.667, i.e. K = 1.667 P")
print("  -> at CMB pressure 136 GPa that needs K = 227 GPa vs ~650 GPa (factor ~2.9 too stiff); at centre 607 vs ~1425 GPa")


def n_ratio(gratio, gamma):
    """days/year ratio (pre-step / post-step) for G_pre/G_post = gratio."""
    x = -1.0 / (3 * gamma - 4)
    t_year = gratio ** -2
    t_day = gratio ** (2 * x)
    return t_year / t_day


cases = [("GSM 4% (G higher before step; rebuttal)", 1.04), ("Banik/Sakstein 11% at 130 Myr", 1.11),
         ("C4 (ii) Chandrasekhar sign low", 0.914), ("C4 (ii) Chandrasekhar sign high", 0.891),
         ("C4 (ii) opposite sign low", 1.094), ("C4 (ii) opposite sign high", 1.122)]
for lab, gr in cases:
    row = []
    for gamma in (5.0 / 3.0, 2.5, 3.5, 4.0, 5.0):
        row.append(f"gamma={gamma:.2f}: {100*(n_ratio(gr, gamma)-1):+.1f}%")
    print(f"{lab}: G_pre/G_post = {gr}; change in days/year (pre vs post): " + "; ".join(row))
print("check: gamma = 5/3 gives exactly 0% (rebuttal's result is recovered only at gamma = 5/3)")
print(f"check: limit gamma -> inf (incompressible): days/year ∝ G^-2 -> 4% step gives {100*(1.04**-2-1):+.1f}%")

print("\n=== C. Insolation step at Earth (L ∝ G^a, r ∝ 1/G => flux ∝ G^(a+2)) ===")
S_abs = 240.0  # W/m^2 globally absorbed solar flux today
for a in (4.0, 5.6, 7.0):
    for lab, gr in (("4% (pre-step G higher)", 1.04), ("11%", 1.11), ("9% lower (Chandrasekhar sign)", 0.91)):
        f = gr ** (a + 2)
        dF = (f - 1) * S_abs
        dT_nofb = 288.0 * (f ** 0.25 - 1)
        print(f"a = {a}: {lab}: insolation ratio {f:.3f}; absorbed-flux change {dF:+.0f} W/m^2 "
              f"= {dF/3.7:+.1f} CO2-doubling equivalents; no-feedback surface dT {dT_nofb:+.1f} K; "
              f"with 3 K/doubling {3*dF/3.7:+.0f} K")

print("\n=== D. Non-gravitational SN-only step: non-SN probes vs true H0 ===")
probes = {"TD (D-31)": (71.1, 2.35), "masers (D-32, stat)": (71.6, 3.7), "sirens (D-33)": (71.7, 8.45),
          "SBF (D-29)": (73.8, math.hypot(0.7, 2.3))}


def comb(keys):
    w = [1 / probes[k][1] ** 2 for k in keys]
    m = sum(wi * probes[k][0] for wi, k in zip(w, keys)) / sum(w)
    return m, 1 / math.sqrt(sum(w))


for keys in (["TD (D-31)", "masers (D-32, stat)", "sirens (D-33)"],
             ["TD (D-31)", "masers (D-32, stat)", "sirens (D-33)", "SBF (D-29)"]):
    m, s = comb(keys)
    for truth, st in ((67.19, 0.38), (68.50, 0.58)):
        t = (m - truth) / math.hypot(s, st)
        print(f"{'+'.join(k.split()[0] for k in keys)}: {m:.2f} +- {s:.2f}; vs true {truth}: {t:.2f} sigma")
