"""Crux C5: numbers for the deciding tests of the narrowed C5.
Units: lifetimes in s (SI); masses/energies in MeV (natural units, hbar=c=1); lambda dimensionless.
Inputs (all from candidates.md / dossier.md / U-01):
  proton pole 887.97 +- 2.04 s; storage pole 878.32 +- 0.43 s; BL1 887.7 +- 2.25 s (M-EXAMINER-11 uses 2.25)
  tau_beta(PERKEO III lambda = -1.27641(56)) = 878.50 +- 0.88 s (U-01, GS2023 pairing)
  aSPECT 2024 lambda = -1.2668(27); Nab goal dlambda/|lambda| = 0.04 % (D-107)
  m_n = 939.565 MeV (Fornal-Grinstein upper bound, D-84); 9Be bound M_f > 937.900 MeV (D-84); m_e = 0.511 MeV
  BL1 trapping times 5 ms and 10 ms (Nico 2005, as quoted in verdict C5-0)
"""
import math

def z(a, sa, b, sb):
    return abs(a - b) / math.hypot(sa, sb)

prot, sprot = 887.97, 2.04
stor, sstor = 878.32, 0.43
bl1, sbl1 = 887.7, 2.25

print("== 1. lambda that C5 needs (tau_beta = 887.7 s), from tau*(1+3 lambda^2) = const ==")
lamP = 1.27641
tauP = 878.50
C = tauP * (1 + 3 * lamP**2)
for tgt in (887.7, 887.97):
    lam = math.sqrt((C / tgt - 1) / 3)
    print(f"  tau_beta = {tgt} s  ->  |lambda| = {lam:.5f}   (Delta from PERKEO III = {lamP - lam:.5f}; aSPECT 2024 = 1.2668)")
lamC5 = math.sqrt((C / 887.7 - 1) / 3)
sig_nab = 0.0004 * 1.2716
print(f"  Nab sigma_lambda at 0.04 %: {sig_nab:.5f}")
print(f"  pole separation |lambda_C5 - lambda_PERKEO| / sigma_Nab = {(lamP - lamC5)/sig_nab:.1f} sigma (Nab alone, poles taken exact)")
# a reading of lamP measured by Nab vs C5's requirement, including uncertainty of C5's requirement
# C5's lambda requirement inherits BL1's error: dlambda/dtau = -lambda/(2 tau) * (1+3l^2)/(3 l^2)
dldt = (1 + 3 * lamC5**2) / (6 * lamC5 * 887.7)
s_req = dldt * sbl1
print(f"  C5's required |lambda| carries sigma = {s_req:.5f} from BL1's 2.25 s")
print(f"  Nab = PERKEO-like at 0.04 %: {(lamP - lamC5)/math.hypot(sig_nab, s_req):.1f} sigma against C5")

print("== 2. LiNA / UCNProBe (electron-counting) readings ==")
for val, s in ((878.0, 1.0), (888.0, 1.0), (878.0, 1.5), (888.0, 1.5)):
    print(f"  reading {val} +- {s} s: {z(val, s, prot, sprot):.1f} sigma from proton pole, {z(val, s, stor, sstor):.1f} sigma from storage pole")
print(f"  J-PARC 2024 877.2 (+4.35/-3.98 -> use 4.35 upward) vs proton pole: {z(877.2, 4.35, prot, sprot):.2f} sigma")

print("== 3. BL2 / BL3 readings (C5 predicts ~888 s) ==")
for val, s in ((888.0, 1.0), (888.0, 0.3), (878.0, 1.0), (878.0, 0.3)):
    print(f"  reading {val} +- {s} s: {z(val, s, bl1, sbl1):.1f} sigma from BL1, {z(val, s, stor, sstor):.1f} sigma from storage pole")

print("== 4. Narrowed C5 kinematics: n -> Y0 e+ e- nubar (via on-shell X+) ==")
mn, me, Mf_min = 939.565, 0.511, 937.900
Q = mn - Mf_min
print(f"  max total kinetic energy of e+ e- nubar Y0 = m_n - M_f,min = {Q:.3f} MeV")
print(f"  every such decay also gives 2 x 0.511 MeV annihilation photons = {2*me:.3f} MeV")

print("== 5. X+ counted fraction in BL1 vs trapping time T (uniform production during T, exponential decay) ==")
for tauX in (0.1e-3, 0.5e-3, 1e-3, 2e-3, 5e-3):
    fr = []
    for T in (5e-3, 10e-3):
        f = (tauX / T) * (1 - math.exp(-T / tauX))
        fr.append(f)
    sh = [9.88 * (1 - f) for f in fr]
    print(f"  tau_X = {tauX*1e3:.1f} ms: counted fraction 5 ms {fr[0]:.3f}, 10 ms {fr[1]:.3f}; beam shift {sh[0]:.2f} s vs {sh[1]:.2f} s; 10-5 ms difference {sh[1]-sh[0]:.2f} s")
