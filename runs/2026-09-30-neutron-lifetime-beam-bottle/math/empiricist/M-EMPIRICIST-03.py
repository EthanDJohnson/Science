"""M-EMPIRICIST-03: leave-one-out of the proton-vs-rest partition (F6). Between chi2 of a two-group split
equals (m1 - m2)^2 / (s1^2 + s2^2) with m, s the group inverse-variance means."""
import sys
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/empiricist")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from _inputs import *
from math_checks import identity, finish

# Two-group between-chi2 identity: W1 (m1-M)^2 + W2 (m2-M)^2 == (m1-m2)^2/(1/W1 + 1/W2)
identity("W1*(m1-(W1*m1+W2*m2)/(W1+W2))**2 + W2*(m2-(W1*m1+W2*m2)/(W1+W2))**2", "(m1-m2)**2/(1/W1+1/W2)",
         domain={"m1": (-5, 5), "m2": (-5, 5)})

def two(a, b):
    (m1, s1), (m2, s2) = wmean(a), wmean(b)
    c = (m1 - m2) ** 2 / (s1 ** 2 + s2 ** 2)
    return c, m1, m2

rest = EBEAM + STORAGE
c, *_ = two(PROTON, rest); print(f"proton vs rest {c:.3f}")
c1, *_ = two(["BL1"], rest); print(f"without Sussex-ILL: {c1:.3f}")
agree("without Sussex chi2", c1, 16.89, 0.006)
c2, *_ = two(["SUS"], rest); print(f"without BL1: {c2:.3f}, z {c2**0.5:.3f}")
agree("without BL1 chi2", c2, 4.96, 0.006); agree("without BL1 z", c2 ** 0.5, 2.2, 0.06)
rest_nou = [k for k in rest if k != "UCNT"]
c3, m1, m2 = two(PROTON, rest_nou); print(f"without UCNtau: {c3:.3f}, z {c3**0.5:.3f}, rest mean {m2:.3f}")
agree("without UCNtau z", c3 ** 0.5, 3.86, 0.006); agree("rest mean without UCNtau", m2, 879.89, 0.006)
zs = (D["SUS"][0] - D["UCNT"][0]) / q(D["SUS"][1], D["UCNT"][1])
zs_face = (D["SUS"][0] - D["UCNT"][0]) / q(D["SUS"][1], 0.22, 0.20)
print(f"Sussex-ILL vs UCNtau z {zs:.3f} (facing {zs_face:.3f})")
agree("Sussex vs UCNtau", zs, 2.35, 0.006)
raise SystemExit(finish())
