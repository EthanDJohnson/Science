"""M-CONSTRAINTS-01 (F3, K13): Delta_R^V cancels between superallowed Vud and tau_beta.
Superallowed: |Vud|^2 = C_sa / [Ft (1 + dRV)]   (Hardy-Towner form; C_sa = 2984.43 s)
Neutron:      tau_beta = K_n / [|Vud|^2 (1 + 3 lam^2)(1 + dRV)(1 + dR')]  with the outer correction dR' shown
=> tau_beta (1 + 3 lam^2) = K_n Ft / C_sa, independent of dRV.
Lens's invariant: Vud^2 (1 + RC), RC = (1 + dR')(1 + dRV) - 1, the full rate correction (dR' = 0.014902)."""
import math
import sympy as sp
from _common import near, tau_beta, LAM
from math_checks import identity, limit, units, finish

Csa, Ft, dRV, lam, Kn, dRp = sp.symbols("C_sa F_t dRV lam K_n dRp", positive=True)
vud2 = Csa / (Ft * (1 + dRV))
tau = Kn / (vud2 * (1 + 3 * lam**2) * (1 + dRV) * (1 + dRp))
# (1) symbolic cancellation: d tau/d dRV = 0
identity(sp.diff(tau, dRV), 0)
identity(tau * (1 + 3 * lam**2), Kn * Ft / (Csa * (1 + dRp)))
# limit: lam -> 0 gives pure Fermi rate tau = Kn Ft/(Csa(1+dRp))
limit(tau, "lam", 0, Kn * Ft / (Csa * (1 + dRp)))
units("(5024.7 s) * (3072 s) / (2984.43 s)", "time")

# (2) numbers: invariant Vud^2 (1 + RC) for each consistent pairing
dRp_v = 0.014902
pairs = {"GS2023": (0.97361, 0.02479, 0.985891), "SGPR2018": (0.97366, 0.02467, 0.985877),
         "AVG2020": (0.97373, 0.02454, 0.985894)}
vals = {}
for k, (v, d, lens) in pairs.items():
    x = v**2 * (1 + d) * (1 + dRp_v)
    vals[k] = x
    near(f"Vud^2(1+RC) {k}", x, lens, 1.5e-6)
x_cms = 0.97420**2 * (1 + 0.03886)       # CMS 2018 RC already includes outer part
near("Vud^2(1+RC) CMS2018", x_cms, 0.985946, 1.5e-6)
vals["CMS2018"] = x_cms
spread = max(vals.values()) - min(vals.values())
print(f"   spread of invariant = {spread:.2e} (lens: constant to 7e-5)")
near("spread", spread, 7e-5, 1e-5)

# tau_beta(PERKEO III) per pairing: tau = K/(Vud^2(1+RC)(1+3lam^2)) with K fixed by GS pairing
lam3 = LAM["PERKEO III"][0]
t_gs = tau_beta(lam3, K=5024.7)
print(f"   with Tan K = 5024.46 s: {tau_beta(lam3):.3f} s")
print(f"   tau_beta GS2023 from 5024.7 s formula = {t_gs:.3f} s (lens 878.50)")
K_full = t_gs * vals["GS2023"] * (1 + 3 * lam3**2)
taus = {k: K_full / (x * (1 + 3 * lam3**2)) for k, x in vals.items()}
for k, t in taus.items():
    print(f"   tau_beta({k}) = {t:.3f} s")
near("min tau_beta consistent", min(taus.values()), 878.45, 0.06)
near("max tau_beta consistent", max(taus.values()), 878.51, 0.06)
near("CMS 5172.0/(1+3lam^2)", 5172.0 / (1 + 3 * lam3**2), 878.45, 0.006)
# Hardy-Towner route independent of dRV: 5024.7 * Ft / C_sa with Ft = 3072.24 s, C_sa = 2984.43 s
t_ht = 5024.7 * 3072.24 / 2984.43 / (1 + 3 * lam3**2)
near("HT Ft route tau_beta", t_ht, 878.5, 0.1)
# mixed pairing CMS RC with Vud 0.97367
t_mix = K_full / (0.97367**2 * (1 + 0.03886) * (1 + 3 * lam3**2))
near("mixed pairing tau_beta (my K is 0.04 s high: 5024.7 s rounding)", t_mix, 879.41, 0.05)
near("mixed pairing bias", t_mix - taus["GS2023"], 0.91, 0.006)
# Ma 2024: lattice box 3.65e-3 vs GS 3.85e-3 -> dRV shift = 2 * (-0.20e-3) -> 0.02439
drv_ma = 0.02479 + 2 * (3.65e-3 - 3.85e-3)
near("Ma inner RC", drv_ma, 0.02439, 5e-6)
t_ma = K_full / (0.97386**2 * (1 + drv_ma) * (1 + dRp_v) * (1 + 3 * lam3**2))
near("Ma pairing shift vs GS", t_ma - taus["GS2023"], 878.39 - 878.50, 0.006)
# consistency: shifting GS Vud by the box change alone
v_pred = 0.97361 * math.sqrt((1 + 0.02479) / (1 + drv_ma))
print(f"   GS Vud rescaled by dRV change alone = {v_pred:.5f} (Ma quotes 0.97386; rest from other inputs)")
# sqrt(K_CMS/K_GS) offset claim (U-01 (3))
near("sqrt(K_CMS/K_GS) = sqrt((1+RC_GS)/(1+RC_CMS))", math.sqrt(1.02479 * 1.014902 / 1.03886), 1.000578, 3e-6)
raise SystemExit(finish())
