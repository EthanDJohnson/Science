"""M-EMPIRICIST-02: grouped chi2 partitions (F5). chi2_total = chi2_within + chi2_between; between computed
directly from the group means; p from chi2 survival; z = two-sided Gaussian equivalent."""
import sys
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/empiricist")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from _inputs import *
from math_checks import identity, finish

# Two-group decomposition identity (symbolic, positive weights)
identity("a*(x-(a*x+b*y+c*z)/(a+b+c))**2 + b*(y-(a*x+b*y+c*z)/(a+b+c))**2 + c*(z-(a*x+b*y+c*z)/(a+b+c))**2",
         "a*(x-(a*x+b*y)/(a+b))**2 + b*(y-(a*x+b*y)/(a+b))**2 + (a+b)*((a*x+b*y)/(a+b) - (a*x+b*y+c*z)/(a+b+c))**2"
         " + c*(z-(a*x+b*y+c*z)/(a+b+c))**2", domain={"x": (-5, 5), "y": (-5, 5), "z": (-5, 5)})

parts = {
    "beam vs bottle": ([PROTON + EBEAM, STORAGE], 16.35, 28.5, 8),
    "proton vs rest": ([PROTON, EBEAM + STORAGE], 21.66, 23.2, 8),
    "BL1 vs rest": ([["BL1"], [k for k in ALL if k != "BL1"]], 16.78, None, 8),
    "four classes": ([PROTON, EBEAM, MATERIAL, MAGNETIC], 36.55, 8.33, 6),
    "material vs magnetic": ([MATERIAL, MAGNETIC], 14.81, None, 5),
}
for name, (groups, lb, lw, dofw) in parts.items():
    w, b, t = grouped(groups)
    bd = between_direct(groups)
    k = len(groups) - 1
    pb = pchi2(b, k); z = zeq(pb)
    print(f"{name}: within {w:.3f}/{dofw} (p {pchi2(w, dofw):.3g}), between {b:.3f}/{k} (direct {bd:.3f}), "
          f"z {z:.3f}, total {t:.3f}")
    agree(f"{name} between", b, lb, 0.006)
    agree(f"{name} between direct = decomposition", bd, b, 1e-9)
    if lw is not None:
        agree(f"{name} within", w, lw, 0.06)
agree("beam-bottle z", zeq(pchi2(grouped(parts['beam vs bottle'][0])[1], 1)), 4.04, 0.006)
agree("beam-bottle within p", pchi2(grouped(parts['beam vs bottle'][0])[0], 8), 3.8e-4, 0.06e-4)
agree("proton-rest z", zeq(pchi2(grouped(parts['proton vs rest'][0])[1], 1)), 4.65, 0.006)
agree("proton-rest within p", pchi2(grouped(parts['proton vs rest'][0])[0], 8), 0.003, 0.0006)
agree("BL1-rest z", zeq(pchi2(grouped(parts['BL1 vs rest'][0])[1], 1)), 4.10, 0.006)
agree("four-class z", zeq(pchi2(grouped(parts['four classes'][0])[1], 3)), 5.43, 0.006)
agree("four-class within p", pchi2(grouped(parts['four classes'][0])[0], 6), 0.22, 0.006)
agree("material-magnetic z", zeq(pchi2(grouped(parts['material vs magnetic'][0])[1], 1)), 3.85, 0.006)

# Gravitrap vs UCNtau
d = D["GRAV"][0] - D["UCNT"][0]
s_sym = q(D["GRAV"][1], D["UCNT"][1]); s_face = q(D["GRAV"][1], 0.22, 0.20)
print(f"Gravitrap - UCNtau {d:.3f} s; sigma sym {s_sym:.3f}, facing {s_face:.3f}; z {d/s_sym:.3f} / {d/s_face:.3f}")
agree("Grav-UCNtau diff", d, 3.68, 0.006); agree("Grav-UCNtau sigma (facing)", s_face, 0.97, 0.006)
agree("Grav-UCNtau z (facing)", d / s_face, 3.80, 0.006)
print("Sensitivity: UCNtau sys symmetrized as mean of sides (0.185 s) instead of the larger side (0.20 s)")
for name, (groups, *_r) in parts.items():
    w, b, t = grouped(groups, D_MEANSIDE); k = len(groups) - 1
    print(f"  {name}: between {b:.3f}/{k}, z {zeq(pchi2(b, k)):.3f}; within {w:.3f}")
print(f"  storage mean {wmean(STORAGE, D_MEANSIDE)[0]:.3f} s")
raise SystemExit(finish())
