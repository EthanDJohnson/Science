"""M-DIALECTICIAN-02: MM worked-example numbers for the clock-offset table (F5).

Inputs (quoted): ell = 3e3 ly, T_thru = pi*ell/c (MM external crossing time). Rates: eps = v^2/(2c^2)
at v = 0.1c, eps = 0.1, eps = 1e-6 (illustrative). Accumulation time = Delta_s / eps.
Units: years (Julian, SI-based), light-years; c = 1 ly/yr.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, quantity, finish

ell = 3.0e3  # ly -> light-time in yr
T = math.pi * ell
print(f"T_thru = pi*ell/c = {T:.6g} yr")
quantity("pi * 3000 ly / c", "9.4248e3 yr", rel_tol=1e-3)

eps_orb = 0.5 * 0.1**2
print(f"eps(0.1c) = v^2/(2c^2) = {eps_orb}")
identity(str(eps_orb), "5e-3")

claims = {100: (9.3e3, 9.5e3, 1.9e6, 9.3e4), 1000: (8.4e3, 1.04e4, 1.7e6, 8.4e4)}
ok_rows = True
for d, (cs, cc, c_orb, c_bh) in claims.items():
    ds, dc = T - d, T + d
    t_orb, t_bh, t_gal = ds / eps_orb, ds / 0.1, ds / 1e-6
    print(f"d={d} ly: Delta_s={ds:.4g} yr (claim {cs}), Delta_CTC={dc:.4g} yr (claim {cc}), "
          f"t(eps=5e-3)={t_orb:.3g} yr (claim {c_orb}), t(eps=0.1)={t_bh:.3g} yr (claim {c_bh}), "
          f"t(eps=1e-6)={t_gal:.3g} yr (claim ~9e9)")
    # compare at the precision quoted (2 significant figures; 3 for 1.04e4)
    identity(f"{float(f'{ds:.2g}')}", f"{cs}")
    identity(f"{float(f'{dc:.3g}') if d == 1000 else float(f'{dc:.2g}')}", f"{cc}")
    identity(f"{float(f'{t_orb:.2g}')}", f"{c_orb}")
    identity(f"{float(f'{t_bh:.2g}')}", f"{c_bh}")
    identity(f"{round(t_gal / 1e9)}", "9" if d == 100 else "8")
# The "about 9e9 yr" (eps = 1e-6) is 9.3e9 (d=100 ly) and 8.4e9 (d=1000 ly) yr.
# Candidate B: "about 9e3 yr of offset, ~1e5 yr at eps=0.1, ~2e6 yr at 0.1c" -> consistent orders.
raise SystemExit(finish())
