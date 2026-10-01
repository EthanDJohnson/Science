"""Quantitative facet: master-formula arithmetic from quoted inputs (units: seconds, dimensionless couplings).
Formula (Czarnecki-Marciano-Sirlin 2018): |Vud|^2 * tau_n * (1 + 3 lambda^2) = K, K = 4908.6(1.9) s.
Also shows the 2023 EFT shift: rate correction +0.026% => K -> K*(1-0.00026) (illustrative, from Cirigliano et al. 2023 text).
All inputs are as quoted in research/quantitative.md; outputs are derived here, not quoted."""
import math
K = 4908.6
K23 = K*(1-0.00026)
lams = {"PERKEO III 2019": 1.27641, "UCNA 2018": 1.2772, "PERKEO II 2013": 1.2748,
        "aSPECT 2020 (PDG)": 1.2677, "aSPECT reanalysis 2024": 1.2668, "PDG 2024 avg": 1.2754, "aCORN 2021": 1.2796}
vuds = {"PDG24 superallowed 0.97367": 0.97367, "Ma+24 lattice box 0.97386": 0.97386, "HT20+Seng 0.97361": 0.97361}
def tau(Kc, v, l): return Kc/(v*v*(1+3*l*l))
print("== tau_beta (s) predicted for each lambda and Vud, K=4908.6 s (CMS18) | K=4907.3 s (x(1-0.00026), EFT23 shift) ==")
for vn, v in vuds.items():
    for ln, l in lams.items():
        print(f"{vn:30s} {ln:26s} tau={tau(K,v,l):8.2f} s | {tau(K23,v,l):8.2f} s")
print()
print("== Vud implied by tau_n and lambda, K=4908.6 s ==")
for tn in (877.75, 878.4, 881.5, 887.7):
    for ln in ("PERKEO III 2019", "PDG 2024 avg"):
        l = lams[ln]; v = math.sqrt(K/(tn*(1+3*l*l)))
        print(f"tau_n={tn:7.2f} s lambda[{ln}]={l}: Vud={v:.5f}")
print()
print("== sensitivities at lambda=1.27641, Vud=0.97367 ==")
l=1.27641; v=0.97367; t=tau(K,v,l)
dlnt_dl = -6*l/(1+3*l*l); dlnt_dv=-2/v
print(f"tau={t:.2f} s; dln(tau)/dlambda={dlnt_dl:.4f}; dtau/dlambda={t*dlnt_dl:.1f} s per unit lambda; dtau/dVud={t*dlnt_dv:.0f} s per unit Vud")
print(f"delta_lambda for 1 s: {1/abs(t*dlnt_dl):.5f}; for 0.5 s: {0.5/abs(t*dlnt_dl):.5f}; for 0.1 s: {0.1/abs(t*dlnt_dl):.6f}")
print(f"relative lambda precision for 1 s: {1/abs(t*dlnt_dl)/l*100:.3f}% ; for 0.5 s: {0.5/abs(t*dlnt_dl)/l*100:.3f}%")
print(f"delta_Vud for 1 s: {1/abs(t*dlnt_dv):.6f} (relative {1/abs(t*dlnt_dv)/v*1e4:.2f}e-4)")
print(f"K uncertainty 1.9 s => tau uncertainty {t*1.9/K:.2f} s (RC only)")
print()
print("== gap translation: tau shift of 10 s vs lambda / Vud ==")
print(f"Delta_lambda for 10 s: {10/abs(t*dlnt_dl):.4f}; Delta_Vud for 10 s: {10/abs(t*dlnt_dv):.5f}")
print("== fractional gap: (887.7-877.75)/877.75 =", (887.7-877.75)/877.75)
print("== lambda-free CKM test: Vud from superallowed 0.97367, Vus 0.22431 (PDG), Vub=3.7e-3")
print(f"sum = {0.97367**2+0.22431**2+(3.7e-3)**2:.5f}")
print(f"sum with Vus=0.2243 and Vud 0.97386: {0.97386**2+0.2243**2+(3.7e-3)**2:.5f}")
print(f"sum with Vus=0.2250 (K_mu2) and Vud 0.97367: {0.97367**2+0.2250**2+(3.7e-3)**2:.5f}")
print(f"sum with Vus=0.2233 (Kl3) and Vud 0.97367: {0.97367**2+0.2233**2+(3.7e-3)**2:.5f}")
