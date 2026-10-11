"""M-DECOMPOSER-02: ln-gamma budget of the published gap (findings 2, 6, 7; lens budget calc).

Inputs (quoted from the dossier, not checked here): Chae 2024b gamma = 1.368; Boufourou E1 on
Chae's catalogue 1.12 (global) - 1.20 (deep); E2 1.045; E3 1.05; family-4 swing 1.00 -> 1.56;
generator differential residual 1.075 / 1.128; Boufourou full-median bias 1.08 / 1.13.
All gammas dimensionless. Claims: total ln(1.368/1.045) = 0.269; pipeline step 0.131-0.200
= 49-74%; family step 0.069-0.138 = 26-51%; E3 vs E2 ln = 0.005; ln(1.56) = 0.445 > ln(1.368)
= 0.313; residual shares 23%/38% (generator), 25%/39% (Boufourou); finding 2 says 23-39%.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, identity, inequality, finish

L = math.log
tot = L(1.368 / 1.045)
print("total", tot)
quantity(f"{tot}", "0.269", rel_tol=2e-3)
pipe_deep, pipe_glob = L(1.368 / 1.20), L(1.368 / 1.12)
fam_deep, fam_glob = L(1.20 / 1.045), L(1.12 / 1.045)
print("pipeline", pipe_deep, pipe_glob, pipe_deep / tot, pipe_glob / tot)
print("family", fam_deep, fam_glob, fam_deep / tot, fam_glob / tot)
quantity(f"{pipe_deep}", "0.131", rel_tol=4e-3)
quantity(f"{pipe_glob}", "0.200", rel_tol=4e-3)
quantity(f"{pipe_deep / tot}", "0.49", rel_tol=1.2e-2)
quantity(f"{pipe_glob / tot}", "0.74", rel_tol=1.2e-2)
quantity(f"{fam_deep}", "0.138", rel_tol=4e-3)
quantity(f"{fam_glob}", "0.069", rel_tol=8e-3)
# additivity: pipeline step + family step = total (log telescoping), symbolic
identity("log(a/b) + log(b/c)", "log(a/c)")
quantity(f"{L(1.05 / 1.045)}", "0.0048", rel_tol=2e-2)
quantity(f"{L(1.56)}", "0.445", rel_tol=2e-3)
quantity(f"{L(1.368)}", "0.313", rel_tol=2e-3)
inequality(f"{L(1.56)}", ">", f"{L(1.368)}")
for g, claim in ((1.075, 0.23), (1.128, 0.38), (1.08, 0.25), (1.13, 0.39)):
    sh = L(g) / L(1.368)
    print(g, "share", sh)
    quantity(f"{sh}", f"{claim}", rel_tol=0.025)
raise SystemExit(finish())
