"""M-MECHANIST-07: arithmetic on the lens's own injection grid (dimensionless γ), as tabulated in Lens-specific outputs.
Claims: F4 E1a Newton bias +0.10 at 10% residual and +0.15 at 16.5% (vs f = 0), Boufourou's +0.08–0.13 at 20–30% residual,
'my triples about twice as effective per unit residual fraction'; F5 E2a +0.11 to +0.15 vs own f = 0, E2b up to 1.165, E3 +0.03 to +0.075;
F7 f = 0 ranges 1.148–1.208 (γ_inj 1.2) and 1.282–1.396 (γ_inj 1.4); E3 1.386–1.452 and 1.208–1.255; MOND recovered 1.28–1.56;
E1b/E1c low by 0.10–0.12 at γ_inj 1.4, f = 0; F9 single-mechanism shifts for E1b (+0.05 no RUWE, +0.03 noise, +0.03 a_in, +0.04 ecc)."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, finish
cols = ["E1a", "E1b", "E1c", "E2a", "E2b", "E3", "E4"]
T = {
 (1.0, 0): [0.989, 0.938, 0.912, 0.971, 0.983, 0.971, 0.973], (1.0, .1): [1.042, 0.994, 0.971, 1.037, 1.045, 1.003, 1.038],
 (1.0, .2): [1.084, 1.012, 0.985, 1.081, 1.107, 1.027, 1.120], (1.0, .3): [1.141, 1.028, 1.006, 1.123, 1.165, 1.046, 1.164],
 (1.2, 0): [1.199, 1.168, 1.148, 1.208, 1.206, 1.208, 1.203], (1.2, .1): [1.282, 1.201, 1.185, 1.230, 1.252, 1.216, 1.227],
 (1.2, .2): [1.309, 1.210, 1.193, 1.259, 1.310, 1.221, 1.325], (1.2, .3): [1.347, 1.208, 1.196, 1.298, 1.383, 1.255, 1.385],
 (1.4, 0): [1.356, 1.300, 1.282, 1.386, 1.358, 1.386, 1.396], (1.4, .1): [1.476, 1.371, 1.362, 1.438, 1.466, 1.414, 1.450],
 (1.4, .2): [1.523, 1.419, 1.409, 1.478, 1.542, 1.452, 1.548], (1.4, .3): [1.559, 1.413, 1.406, 1.473, 1.563, 1.404, 1.540]}
col = lambda g, f, c: T[(g, f)][cols.index(c)]
resid = {0: 0.0, .1: 0.050, .2: 0.101, .3: 0.165}
d2 = col(1.0, .2, "E1a") - col(1.0, 0, "E1a"); d3 = col(1.0, .3, "E1a") - col(1.0, 0, "E1a")
print(f"E1a shift vs f=0: {d2:.3f} (f=0.2, resid 0.101), {d3:.3f} (f=0.3, resid 0.165); vs truth 1: {col(1.0,.2,'E1a')-1:.3f}, {col(1.0,.3,'E1a')-1:.3f}")
quantity(f"{d2}", "0.10", rel_tol=0.06); quantity(f"{d3}", "0.15", rel_tol=0.03)
mine = [d2 / 0.101, d3 / 0.165]; his = [0.08 / 0.20, 0.13 / 0.30]
print(f"slope per unit residual: mine {mine[0]:.2f}, {mine[1]:.2f}; Boufourou {his[0]:.2f}, {his[1]:.2f}; ratio {mine[0]/his[0]:.2f}-{mine[1]/his[1]:.2f}")
quantity(f"{(mine[0]+mine[1])/(his[0]+his[1])}", "2", rel_tol=0.2)
e2a = [col(1.0, f, "E2a") - col(1.0, 0, "E2a") for f in (.2, .3)]; e3 = [col(1.0, f, "E3") - col(1.0, 0, "E3") for f in (.1, .3)]
print(f"E2a shift vs f=0 at f=0.2/0.3: {e2a}; E3 shift f=0.1..0.3: {e3}; E2b max {max(col(1.0,f,'E2b') for f in resid)}")
quantity(f"{e2a[0]}", "0.11", rel_tol=0.02); quantity(f"{e2a[1]}", "0.15", rel_tol=0.02)
quantity(f"{e3[0]}", "0.03", rel_tol=0.1); quantity(f"{e3[1]}", "0.075", rel_tol=0.01)
r12 = T[(1.2, 0)]; r14 = T[(1.4, 0)]
print(f"γ_inj 1.2, f=0: {min(r12)}-{max(r12)}; γ_inj 1.4, f=0: {min(r14)}-{max(r14)}")
quantity(f"{min(r12)}", "1.148", rel_tol=1e-6); quantity(f"{max(r12)}", "1.208", rel_tol=1e-6)
quantity(f"{min(r14)}", "1.282", rel_tol=1e-6); quantity(f"{max(r14)}", "1.396", rel_tol=1e-6)
E3_14 = [col(1.4, f, "E3") for f in resid]; E3_12 = [col(1.2, f, "E3") for f in resid]
all14 = [v for f in resid for v in T[(1.4, f)]]
print(f"E3 at 1.4: {min(E3_14)}-{max(E3_14)}; at 1.2: {min(E3_12)}-{max(E3_12)}; all γ_inj 1.4: {min(all14)}-{max(all14)}")
quantity(f"{min(E3_14)}", "1.386", rel_tol=1e-6); quantity(f"{max(E3_14)}", "1.452", rel_tol=1e-6)
quantity(f"{min(all14)}", "1.282", rel_tol=1e-6); quantity(f"{max(all14)}", "1.563", rel_tol=1e-6)
print(f"E1b, E1c low at γ_inj 1.4, f=0: {1.4-col(1.4,0,'E1b'):.3f}, {1.4-col(1.4,0,'E1c'):.3f}")
ref_b = 1.003
for name, v, lens in (("no RUWE", 1.056, 0.05), ("PM noise", 1.036, 0.03), ("a_in", 1.030, 0.03), ("ecc thermal", 1.044, 0.04)):
    print(f"E1b {name}: {v - ref_b:+.3f} (lens {lens})"); quantity(f"{v - ref_b}", f"{lens}", rel_tol=0.2)
raise SystemExit(finish())
