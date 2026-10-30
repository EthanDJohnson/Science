"""M-CONSTRAINTS-11 (F12): M_B / G transition sizes and timing.
Hubble-flow SNe brighter than calibrators by dm = 0.146-0.188 mag -> L_far/L_near = 10^(0.4 dm) (lens 1.14-1.19).
Chandrasekhar scaling L ~ M_Ch ~ G^(-3/2) -> G_far/G_near = (L ratio)^(-2/3) (lens 0.89-0.91); opposite sign L ~ G^(+3/2) -> 1.09-1.12.
Lookback times in CMB-SPA LCDM: z = 0.01 -> 144 Myr, z = 0.0233 -> 333 Myr; window ~190 Myr = 1.4% of t0; D(z=0.01) ~ 44 Mpc."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/constraints")
from math_checks import identity, limit, quantity, finish
from _bg import Model, ONU, near

for dm, wl, wg in [(0.146, 1.14, 0.914), (0.188, 1.19, 0.891)]:
    L = 10 ** (0.4 * dm)
    near(f"L ratio dm={dm}", L, wl, 0.006)
    near(f"G ratio (Chandrasekhar) dm={dm}", L ** (-2 / 3), wg, 0.006)
    print(f"  opposite-sign G ratio = {L ** (2/3):.4f}")
near("opposite sign, dm=0.146", 10 ** (0.4 * 0.146 * 2 / 3), 1.09, 0.006)
near("opposite sign, dm=0.188", 10 ** (0.4 * 0.188 * 2 / 3), 1.12, 0.006)
identity("(G**(-sp_rational))**(-1/sp_rational)".replace("sp_rational", "(3/2)"), "G")
wb, Om, h = 0.02237, 0.3175, 0.6719
m = Model(h, wb, Om * h * h - wb - ONU)
t1, t2, t0 = 1000 * m.lookback(0.01), 1000 * m.lookback(0.0233), m.age()
print(f"lookback z=0.01: {t1:.1f} Myr; z=0.0233: {t2:.1f} Myr; window {t2-t1:.1f} Myr = {(t2-t1)/1000/t0:.4f} of t0")
near("lookback 0.01 (Myr)", t1, 144, 2); near("lookback 0.0233 (Myr)", t2, 333, 3)
near("window (Myr)", t2 - t1, 190, 4); near("fraction of t0", (t2 - t1) / 1000 / t0, 0.014, 0.0006)
near("D_M(0.01) Mpc", m.DM(0.01, n=2000), 44, 1.0)
limit("log(1+z)/z", "z", 0, "1")  # lookback -> z/H0 at small z
quantity("0.01 / (67.19 km/s/Mpc)", "145.5 Myr", rel_tol=3e-3)
raise SystemExit(finish())
