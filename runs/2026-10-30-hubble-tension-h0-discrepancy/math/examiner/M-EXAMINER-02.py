"""M-EXAMINER-02: pairwise z of each non-SH0ES local class vs CMB-SPA (F3).
z = |H_a - H_b| / sqrt(s_a^2 + s_b^2), independent Gaussian errors; quoted stat and sys added in quadrature.
Computed both with the facing-side error (lens's stated tension() method) and with symmetrised errors."""
import sys
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/examiner")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from common import *
from math_checks import identity, limit, quantity, inequality, finish

# formula sanity: z of identical values is 0; with sb -> 0 reduces to single-error z
identity("(a - b)/sqrt(sa**2 + sb**2)", "(a-b)/sa", domain={"a": (60, 80), "b": (60, 80), "sa": (0.1, 10), "sb": (0, 0)})
claims = {"CCHP": (CCHP, 1.62), "SBF": (SBF, 2.72), "TF": (TF, 1.49), "TD": (TD, 1.64), "MASER": (MASER, 1.19), "SIREN": (SIREN, 0.53)}
zf_all = []
for k, (m, zc) in claims.items():
    zf, zs = z_facing(m, CMB), z_sym(m, CMB)
    zf_all.append(zf)
    print(f"{k}: H {m[0]} +{m[1]:.4f}/-{m[2]:.4f}; z facing {zf:.3f}, z symmetrised {zs:.3f}, lens {zc}")
    quantity(f"{zs}", f"{zc}", rel_tol=6e-3)
print("range facing:", min(zf_all), max(zf_all))
inequality(f"{min(zf_all)}", ">=", "0.5"); inequality(f"{max(zf_all)}", "<=", "2.75")
raise SystemExit(finish())
