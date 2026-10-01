"""M-EXAMINER-01: grouped chi^2 partitions (examiner F4, F12 local values).
chi^2_total = chi^2_within + chi^2_between; within = sum_c sum_{i in c} w_i (x_i - m_c)^2,
between = sum_c W_c (m_c - m)^2. Lifetimes in s (SI); chi^2 dimensionless.
10 inputs: BL1, Sussex-ILL, J-PARC 2024, UCNtau 2025, Ezhov, Gravitrap, Serebrov05, MAMBO II, Steyerl, Arzumanov."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/examiner")
import sympy as sp
from math_checks import identity, finish
from _inputs import *
from _h import cmp, z_of_p2, chi2_sf

BOTTLE = {**MATERIAL, **MAGNETIC}
BEAM = {**PROTON, **ELECTRON}
REST = {**ELECTRON, **BOTTLE}

def show(name, classes):
    w, dw, b, db, tot = grouped(classes)
    z = z_of_p2(chi2_sf(b, db))
    pw = chi2_sf(w, dw)
    print(f"{name}: between {b:.3f}/{db} ({z:.3f} sigma), within {w:.3f}/{dw} (p={pw:.3g}), total {tot:.3f}, sum {w+b:.3f}")
    return w, dw, b, db, z, pw, tot

print("inputs (x, sigma):")
for d in (PROTON, ELECTRON, MATERIAL, MAGNETIC):
    for k, v in d.items():
        print(f"  {k}: {v[0]} +- {v[1]:.4f} s")

w, dw, b, db, z, pw, tot = show("beam vs bottle", [BEAM, BOTTLE])
cmp("beam/bottle between chi2", b, 16.49, 0.005)
cmp("beam/bottle z", z, 4.06, 0.005)
cmp("beam/bottle within chi2", w, 28.80, 0.005)
cmp("beam/bottle within p", pw, 3.4e-4, 0.05e-4)
cmp("decomposition within+between = total", w + b, tot, 1e-9)  # float round-off only

w2, dw2, b2, db2, z2, pw2, tot2 = show("proton vs rest", [PROTON, REST])
cmp("proton/rest between", b2, 21.80, 0.005)
cmp("proton/rest z", z2, 4.67, 0.005)
cmp("proton/rest within", w2, 23.49, 0.005)
cmp("proton/rest within p", pw2, 0.0028, 0.00005)
print(f"Delta chi2 between (proton/rest - beam/bottle) = {b2-b:.3f}")
cmp("Delta chi2_between", b2 - b, 5.3, 0.05)
_, _, chirest, _ = wmean(REST)
print(f"non-proton ('rest') internal chi2 = {chirest:.3f}/{len(REST)-1}, S = {(chirest/(len(REST)-1))**0.5:.3f}")
cmp("rest chi2", chirest, 23.4, 0.05)

# J-PARC stat inflated by sqrt(15.8/3)
S = (15.8 / 3) ** 0.5
JPi = {"JPARC": (JP_X, q(JP_STAT * S, (JP_UP + JP_DN) / 2))}
w3, dw3, b3, db3, z3, _, _ = show("proton vs rest, J-PARC inflated", [PROTON, {**JPi, **BOTTLE}])
cmp("inflated z", z3, 4.67, 0.005)

w4, dw4, b4, db4, z4, _, _ = show("BL1 alone vs rest", [{"BL1": BL1}, REST])
cmp("BL1 vs rest between", b4, 17.00, 0.005)
cmp("BL1 vs rest z", z4, 4.12, 0.005)

w5, dw5, b5, db5, z5, pw5, _ = show("four classes", [PROTON, ELECTRON, MATERIAL, MAGNETIC])
cmp("4-class between", b5, 36.95, 0.005)
cmp("4-class z", z5, 5.46, 0.005)
cmp("4-class within", w5, 8.33, 0.005)
cmp("4-class within p", pw5, 0.22, 0.005)

# limit check: a class whose error -> infinity contributes nothing to between (two classes, one point each)
x1, x2, s1, s2 = sp.symbols("x1 x2 s1 s2", positive=True)
m = (x1 / s1**2 + x2 / s2**2) / (1 / s1**2 + 1 / s2**2)
between2 = (x1 - m) ** 2 / s1**2 + (x2 - m) ** 2 / s2**2
identity(between2, (x1 - x2) ** 2 / (s1**2 + s2**2))  # two-point between chi2 = z^2
raise SystemExit(finish())
