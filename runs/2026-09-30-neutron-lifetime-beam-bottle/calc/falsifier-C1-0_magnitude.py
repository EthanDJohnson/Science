"""Falsifier C1-0 (magnitude): shift C1 produces in each measurement class vs observed.
Units: SI (lifetimes in s, pressures in Pa). Inputs from dossier/candidates (cited there)."""
import math

def sig2p(z):  # two-sided p for a Gaussian z
    return math.erfc(abs(z) / math.sqrt(2))

# Class values (s)
BL1, sBL1 = 887.7, math.hypot(1.2, 1.9)          # D-20
SUS, sSUS = 889.2, math.hypot(3.0, 3.8)          # Byrne 1996 (PDG listing)
PROT, sPROT = 887.97, 2.04                        # statistician proton class
STOR, sSTOR = 878.32, 0.43                        # statistician all storage (S=1.85)
UCNT, sUCNT = 877.82, 0.287                       # UCNtau (D-27, sym approx)
MAT, sMAT = 880.0, 0.7                            # material bottles (D-73 ORNL grouping)
MAG, sMAG = 877.8, 0.2                            # magnetic traps (D-73)
JP = 877.2; sJPu = math.hypot(1.7, 4.0); sJPd = math.hypot(1.7, 3.6)  # D-23
SMA, sSMA = 878.70, 0.83                          # SM A-route tau_beta (M-CONSTRAINTS-02)

print("== Gap C1 must carry ==")
gap = PROT - STOR; sg = math.hypot(sPROT, sSTOR)
print(f"proton class - storage = {gap:.2f} +- {sg:.2f} s  ({gap/sg:.2f} sigma), frac of tau_true = {gap/STOR*100:.3f} %")
f_loss = 1 - STOR / PROT
print(f"equivalent multiplicative count deficit f = 1 - tau_true/tau_meas = {f_loss*100:.3f} %")
for name, t in [("magnetic 877.8", MAG), ("UCNtau 877.82", UCNT), ("material 880.0", MAT)]:
    print(f"  if true tau = {name}: needed shift = {PROT-t:.2f} s = {(PROT-t)/t*100:.3f} %")

print("\n== C1 predictions (true tau = storage 878.32 s) vs non-proton classes ==")
r = (JP - STOR)
s = sJPu if r < 0 else sJPd  # observed below prediction -> use upper error of measurement
print(f"J-PARC 2024: obs-pred = {r:+.2f} s, sigma = {math.hypot(s, sSTOR):.2f} s -> {r/math.hypot(s,sSTOR):+.2f} sigma")
r = SMA - STOR
print(f"SM A-route tau_beta: obs-pred = {r:+.2f} s -> {r/math.hypot(sSMA,sSTOR):+.2f} sigma")
r = MAT - MAG
print(f"storage internal (material - magnetic) = {r:+.2f} s -> {r/math.hypot(sMAT,sMAG):.2f} sigma unscaled (C1 predicts 0; residual left to C7)")

print("\n== Proton-counting members under C1 scopes ==")
zS = (SUS - STOR) / math.hypot(sSUS, sSTOR)
print(f"A-BL1 (Sussex-ILL unshifted): Sussex-ILL residual {SUS-STOR:+.2f} s = {zS:.2f} sigma, p2 = {sig2p(zS):.3f}")
# A-gen: common multiplicative factor k; fit k from BL1 and Sussex
k_BL1 = BL1 / STOR; k_S = SUS / STOR
sk_BL1 = sBL1 / STOR; sk_S = sSUS / STOR
w1, w2 = 1/sk_BL1**2, 1/sk_S**2
k = (w1*k_BL1 + w2*k_S)/(w1+w2); sk = (w1+w2)**-0.5
chi = ((k_BL1-k)/sk_BL1)**2 + ((k_S-k)/sk_S)**2
print(f"A-gen: common factor k-1 = {(k-1)*100:.3f} +- {sk*100:.3f} %, chi2 = {chi:.3f}/1 -> consistent")

print("\n== Named sub-hypotheses: fraction of gap each can carry at quoted size ==")
print(f"A1 fluence monitor: needed eps0 shift {f_loss*100:.2f} %; 2005 mass-based vs 2013 Alpha-Gamma calibrations differ by 1.4 s = {1.4/BL1*100:.3f} %")
print(f"   needed / (two-method difference) = {9.65/1.4:.1f}x; needed / 0.5 s uncertainty = {9.65/0.5:.1f}x")
print(f"A4 trap nonlinearity (-5.3 s) at 100% error: {5.3/gap*100:.0f} % of gap")
print(f"A4 6Li absorption (+5.4 s) sign-flipped (shift 10.8 s): {10.8/gap*100:.0f} % of gap")
print(f"A3 proton backscatter/dead layer budgets 0.4, 0.5 s: {0.4/gap*100:.1f} %, {0.5/gap*100:.1f} % of gap")
# A2 residual H2: Caylor loss 0.3% at 1e-7 Pa, 10 ms, 40 K; linear in P and t
p_pump = 1e-9 * 100  # 1e-9 mbar -> Pa
print(f"Nico 2005 ion-pump pressure 1e-9 mbar = {p_pump:.1e} Pa")
for frac10 in (1.0, 0.5):
    tbar = frac10*10 + (1-frac10)*5
    P_need = f_loss / (0.003 * tbar/10) * 1e-7
    print(f"A2: if {frac10*100:.0f}% of data at 10 ms (mean {tbar} ms) and every H2+ lost: need P_H2 = {P_need:.2e} Pa = {P_need/p_pump:.1f}x pump reading")
print(f"A2 Caylor worst case < 0.5 s = < {0.5/gap*100:.1f} % of gap")
# If all effects at quoted size summed linearly (worst-case stacking)
stack = 0.5 + 0.4 + 0.5 + 0.5 + 1.0 + 0.8 + 0.9
print(f"Linear stack of itemised budgets (fluence 0.5, backscatter 0.4, Si 0.5, H2 0.5, halo 1.0, nonlin 0.8, 6Li mass 0.9) = {stack:.1f} s = {stack/gap*100:.0f} % of gap")
