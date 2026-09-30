"""User-supplied correction U-01: pair a superallowed Vud with its own inner radiative correction.

Claim to check (dossier U-01):
  (1) Delta_R^V cancels analytically between a superallowed-derived Vud and the neutron partial
      lifetime tau_beta, so the SM prediction tau_beta(lambda) does not depend on which Delta_R^V
      evaluation is used -- PROVIDED Vud is the value extracted with that same Delta_R^V.
  (2) Dossier D-50 pairs the CMS 2018 constant K = 4908.6 s (Marciano-Sirlin 2006 inner RC,
      Delta_R^V = 0.02361) with the PDG 2024 Vud = 0.97367 (extracted with a 2018+ inner RC near
      0.0245-0.0248). That mixed pairing overstates tau_beta by about +0.95 s (0.11%).
  (3) The dossier's "unresolved 5.7e-4 offset" between the bare CMS-2018 Vud (0.97459) and the
      Gorchtein-Seng / Cirigliano value (0.97402) for the same tau and lambda is the same inner-RC
      update: Vud ratio = sqrt(K_CMS2018 / K_GS2023).

Units: lifetimes in s; lambda (= |gA/gV|), Vud, radiative corrections dimensionless.
Inputs are dossier anchors: D-40..D-44, D-48, D-49 (K constants and Delta_R^V sets), via the
toolkit calculator neutron_beta_decay.py (its RC sets match D-48/D-49).
"""
import sys

import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from neutron_beta_decay import master_constant, tau_beta, vud_from_tau  # noqa: E402

print("=" * 78)
print("Part 1. Symbolic: Delta_R^V cancels when Vud comes from superallowed decays")
print("=" * 78)
# Superallowed 0+ -> 0+:  |Vud|^2 = C_nuc / (Ft (1 + Delta_R^V))       (C_nuc: constants, Ft: corrected ft)
# Neutron:                tau_beta = K0 / (|Vud|^2 (1 + 3 lam^2)(1 + d_out)(1 + Delta_R^V))
C_nuc, Ft, DR, K0, lam, d_out = sp.symbols("C_nuc Ft Delta_R K0 lambda delta_out", positive=True)
Vud2 = C_nuc / (Ft * (1 + DR))
tau = K0 / (Vud2 * (1 + 3 * lam**2) * (1 + d_out) * (1 + DR))
tau_s = sp.simplify(tau)
print("tau_beta after substituting superallowed Vud^2 =", tau_s)
print("d tau_beta / d Delta_R^V =", sp.simplify(sp.diff(tau_s, DR)), "(zero => Delta_R^V cancels)")

print()
print("=" * 78)
print("Part 2. Numeric: PERKEO III lambda = 1.27641(56) (D-40) with each Vud / RC pairing")
print("=" * 78)
LAM, SLAM = 1.27641, 0.00056
pairs = [
    ("CMS2018", 0.97420, "consistent: CMS 2018 superallowed Vud with MS2006 inner RC (D-49)"),
    ("SGPR2018", 0.97366, "consistent: Seng 2018 Vud with Delta_R^V = 0.02467 (D-43, D-48)"),
    ("AVG2020", 0.97373, "consistent: Hardy-Towner 2020 Vud with Delta_R^V = 0.02454 (D-43, D-48)"),
    ("GS2023", 0.97361, "consistent: Gorchtein-Seng 2024 Vud with Delta_R^V = 0.02479 (D-43, D-48)"),
    ("GS2023", 0.97367, "near-consistent: PDG 2024 Vud with GS2023 RC"),
    ("CMS2018", 0.97367, "MIXED (as in D-50): CMS 2018 K with PDG 2024 Vud"),
]
print(f"{'rc set':9s} {'Vud':>8s} {'K (s)':>9s} {'tau_beta (s)':>14s}  pairing")
res = {}
for rc, vud, label in pairs:
    r = tau_beta(LAM, SLAM, vud, 0.00032, rc_set=rc)
    res[(rc, vud)] = r["tau"]
    print(f"{rc:9s} {vud:8.5f} {master_constant(rc)[0]:9.2f} {r['tau']:9.2f} +- {r['sigma']:.2f}  {label}")
cms_route = 5172.0 / (1 + 3 * LAM**2)
print(f"CMS 2018 superallowed-combined constant: 5172.0(1.1) s / (1 + 3 lam^2) = {cms_route:.2f} s (D-01, D-49)")
cons = [res[("CMS2018", 0.97420)], res[("SGPR2018", 0.97366)], res[("AVG2020", 0.97373)], res[("GS2023", 0.97361)]]
print(f"Consistent pairings span {min(cons):.2f} - {max(cons):.2f} s (spread {max(cons) - min(cons):.2f} s)")
bias = res[("CMS2018", 0.97367)] - res[("GS2023", 0.97361)]
print(f"Bias of the mixed pairing used in D-50: {bias:+.2f} s ({bias / res[('GS2023', 0.97361)] * 100:+.3f} %)")

print()
print("=" * 78)
print("Part 3. D-50 recomputed with a consistent pairing (GS2023 RC, Vud = 0.97361(32))")
print("=" * 78)
lams = [("PERKEO III", 1.27641, 0.00056), ("UCNA 2018", 1.2772, 0.0020), ("PERKEO II", 1.2748, (0.0008**2 + 0.00105**2) ** 0.5),
        ("PDG 2024 avg", 1.2754, 0.0013), ("aSPECT 2020", 1.2677, 0.0028), ("aSPECT 2024", 1.2668, 0.0027),
        ("aCORN", 1.2796, 0.0062)]
print(f"{'lambda source':14s} {'|lambda|':>9s} {'tau_beta consistent (s)':>24s} {'D-50 mixed (s)':>15s} {'shift (s)':>9s}")
for name, l, sl in lams:
    good = tau_beta(l, sl, 0.97361, 0.00032, rc_set="GS2023")
    mixed = tau_beta(l, sl, 0.97367, 0.00032, rc_set="CMS2018")
    print(f"{name:14s} {l:9.5f} {good['tau']:15.2f} +- {good['sigma']:5.2f} {mixed['tau']:15.2f} {good['tau'] - mixed['tau']:9.2f}")
print("(PERKEO II error: 0.0008 stat (+) 0.00105 sys, the systematic symmetrised from +0.0010/-0.0011; corrected after M-EMPIRICIST-11)")

print()
print("=" * 78)
print("Part 4. The 'unresolved 5.7e-4 Vud offset' (dossier section 6)")
print("=" * 78)
TAU, STAU = 877.75, 0.36          # UCNtau as used by Cirigliano 2023 / Gorchtein-Seng 2023 (D-44)
v_cms = vud_from_tau(TAU, STAU, LAM, SLAM, rc_set="CMS2018")["vud"]
v_gs = vud_from_tau(TAU, STAU, LAM, SLAM, rc_set="GS2023")["vud"]
ratio = (master_constant("CMS2018")[0] / master_constant("GS2023")[0]) ** 0.5
print(f"Vud(CMS2018 K) = {v_cms:.5f}; Vud(GS2023 K) = {v_gs:.5f}; difference = {v_cms - v_gs:.2e}")
print(f"sqrt(K_CMS2018 / K_GS2023) = {ratio:.6f}; Vud(GS2023) * ratio = {v_gs * ratio:.5f} (= Vud(CMS2018))")
print("=> the offset is the inner-RC update 0.02361 -> 0.02479, not unexplained physics.")
