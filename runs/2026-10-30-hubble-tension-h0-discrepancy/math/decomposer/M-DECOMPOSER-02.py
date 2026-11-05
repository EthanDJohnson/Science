"""M-DECOMPOSER-02: one-mean chi2 and two-group partitions on the ten-result set (F2, Q2a).

chi2(one mean) = sum ((x_i - m)/s_i)^2, m inverse-variance mean, dof 9.
Two-group split: chi2 = chi2 about group-1 mean + chi2 about group-2 mean, dof 8.
Exhaustive search over all 2^9 - 1 nontrivial bipartitions.
"""
import sys
import itertools
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/decomposer")
from _common import TEN, LOCAL, EARLY, chi2_about_mean, chi2_sf, z_from_p2, num, finish, identity, units

names = list(TEN)
items = [TEN[n] for n in names]
c1 = chi2_about_mean(items)
p1 = chi2_sf(c1, 9)
num("chi2 one mean (9 dof)", c1, 49.65, 0.1)
num("p one mean", p1, 1.3e-7, 0.1e-7)
num("z equivalent of p (two-sided)", z_from_p2(p1), 5.3, 0.06)


def split(g1):
    g2 = [n for n in names if n not in g1]
    return chi2_about_mean([TEN[n] for n in g1]) + chi2_about_mean([TEN[n] for n in g2])


results = []
for r in range(1, len(names)):
    for g1 in itertools.combinations(names, r):
        if names[0] not in g1:     # each bipartition once
            continue
        results.append((split(list(g1)), g1))
results.sort()
for c, g in results[:6]:
    print(f"  {c:7.3f}  group with SH0ES: {g}")
best_c, best_g = results[0]
print("  best split:", best_g)
identity(str(int(set(best_g) == set(LOCAL))), "1")   # best split == all local vs early-type
num("best split chi2 (local vs early)", split(LOCAL), 8.48, 0.01)
num("p best split (8 dof)", chi2_sf(split(LOCAL), 8), 0.39, 0.01)

ladders = ["SH0ES", "CCHP", "SBF"]
num("all ladders vs rest", split(ladders), 11.2, 0.05)
rs_using = ["CMB", "BAOBBN"]
c_rs = split(rs_using)
print(f"  r_s-using (CMB, BAO+BBN) vs not: {c_rs:.3f}")
c_rs2 = split(["CMB", "BAOBBN", "RSFREE", "EQ"])  # = local vs early, for comparison
num("r_s-using vs not", c_rs, 12.6, 0.05)
c_sh = split(["SH0ES"])
num("SH0ES vs rest", c_sh, 16.9, 0.05)
num("p SH0ES vs rest", chi2_sf(c_sh, 8), 0.03, 0.005)
num("Delta chi2 SH0ES-vs-rest minus local-vs-early", c_sh - split(LOCAL), 8.5, 0.06)
num("Delta chi2 ladders-vs-rest minus local-vs-early (Q2a 2.7)", split(ladders) - split(LOCAL), 2.7, 0.06)
# next-best splits: dropping CCHP or sirens from the local group
for drop in ["CCHP", "SIREN"]:
    g = [n for n in LOCAL if n != drop]
    print(f"  local minus {drop}: chi2 = {split(g):.3f}, delta = {split(g) - split(LOCAL):.3f}")
    from _common import inequality
    inequality(f"{split(g) - split(LOCAL)!r}", "<=", "0.4")

# structural: chi2 of two points about weighted mean = (x1-x2)^2/(s1^2+s2^2)
identity("((x1 - (x1/s1**2 + x2/s2**2)/(1/s1**2 + 1/s2**2))/s1)**2 + ((x2 - (x1/s1**2 + x2/s2**2)/(1/s1**2 + 1/s2**2))/s2)**2",
         "(x1 - x2)**2/(s1**2 + s2**2)", domain={"x1": (60, 80), "x2": (60, 80)})
from _common import limit
limit("((x1 - x2)**2)/(s1**2 + s2**2)", "s2", "oo", "0", domain={"x1": (60, 80), "x2": (60, 80)})
units("((73.49 km/s/Mpc - 67.19 km/s/Mpc)/(0.93 km/s/Mpc))^2", "dimensionless")
raise SystemExit(finish())
