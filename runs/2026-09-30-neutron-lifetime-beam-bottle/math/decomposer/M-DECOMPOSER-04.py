"""M-DECOMPOSER-04 (F4): partition chi2 over 10 results (2 proton, J-PARC, 7 storage).
chi2_total = chi2_within + chi2_between, chi2_between = sum_c W_c (m_c - m)^2. J-PARC sigma symmetrised
(stat 1.7 (+) mean sys 3.8). Strong-field (>= 4.6 T) set = {BL1, SIL} per D-20/L15. SI (s)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/decomposer")
from math_checks import identity, finish
from _inputs import *

ALL = PROTON + [JPARC] + STORAGE
m, s, c2, S = wmean(ALL)
print(f"pooled: {m:.3f}, chi2 {c2:.3f}/{len(ALL)-1}, J-PARC sigma {JPARC[1]:.3f}")
near("pooled chi2", c2, 45.3, 0.05)

def partition(groups):
    within = sum(wmean(g)[2] if len(g) > 1 else 0.0 for g in groups)
    return within, c2 - within

parts = {
    "beam(incl JP) vs bottle": ([PROTON + [JPARC], STORAGE], 16.5, 28.8),
    "proton vs rest": ([PROTON, [JPARC] + STORAGE], 21.8, 23.5),
    "BL1 vs rest": ([[BL1], [SIL, JPARC] + STORAGE], 16.9, None),
    "4 classes": ([PROTON, [JPARC], MATERIAL, MAGNETIC], 36.9, 8.3),
}
for name, (groups, b_l, w_l) in parts.items():
    w, b = partition(groups)
    dof_b = len(groups) - 1
    zb = z_from_p(chi2_sf(b, dof_b))
    print(f"{name}: within {w:.3f}, between {b:.3f}/{dof_b}, z {zb:.3f}")
    near(f"{name} between", b, b_l, 0.05)
    if w_l is not None:
        near(f"{name} within", w, w_l, 0.05)
    # check the decomposition directly
    bsum = sum(wmean(g)[0] * 0 + (1 / wmean(g)[1] ** 2) * (wmean(g)[0] - m) ** 2 for g in groups)
    near(f"{name} decomposition identity", bsum, b, 1e-6)
w4, b4 = partition(parts["4 classes"][0])
print(f"4-class within p = {chi2_sf(w4, 6):.3f}; between z = {z_from_p(chi2_sf(b4, 3)):.3f}")
near("4-class within p", chi2_sf(w4, 6), 0.22, 0.01)
near("4-class between z", z_from_p(chi2_sf(b4, 3)), 5.46, 0.02)
near("beam/bottle between z", z_from_p(chi2_sf(partition(parts['beam(incl JP) vs bottle'][0])[1], 1)), 4.06, 0.01)
near("proton/rest between z", z_from_p(chi2_sf(partition(parts['proton vs rest'][0])[1], 1)), 4.67, 0.01)
dd = partition(parts["proton vs rest"][0])[1] - partition(parts["beam(incl JP) vs bottle"][0])[1]
near("Delta chi2 proton/rest minus beam/bottle", dd, 5.3, 0.05)
# symbolic two-group decomposition identity (formalizable)
identity("w1*(x1-(w1*x1+w2*x2+w3*x3)/(w1+w2+w3))**2 + w2*(x2-(w1*x1+w2*x2+w3*x3)/(w1+w2+w3))**2 + w3*(x3-(w1*x1+w2*x2+w3*x3)/(w1+w2+w3))**2",
         "w1*(x1-(w1*x1+w2*x2)/(w1+w2))**2 + w2*(x2-(w1*x1+w2*x2)/(w1+w2))**2 + (w1+w2)*((w1*x1+w2*x2)/(w1+w2)-(w1*x1+w2*x2+w3*x3)/(w1+w2+w3))**2 + w3*(x3-(w1*x1+w2*x2+w3*x3)/(w1+w2+w3))**2",
         domain={"x1": (-5, 5), "x2": (-5, 5), "x3": (-5, 5)})
raise SystemExit(finish())
