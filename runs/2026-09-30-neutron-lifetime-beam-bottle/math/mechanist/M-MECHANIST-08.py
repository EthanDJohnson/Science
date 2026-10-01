"""M-MECHANIST-08 (F10): J-PARC per-condition values (D-24; stat errors), pair means, split,
linear extrapolation tau(P) to P = 0 from 100 and 50 kPa means: tau0 = 2 tau50 - tau100;
tensions with beam 887.97 +- 2.04 s and UCNtau 877.82 +- 0.287 s; J-PARC 877.2 +- 1.7 (+4.0/-3.6). s (SI)."""
import math, sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import quantity, identity, finish

def wmean(pts):
    w = [1 / s**2 for _, s in pts]
    return sum(wi * x for wi, (x, _) in zip(w, pts)) / sum(w), 1 / math.sqrt(sum(w))

c100o, c100n, c50o, c50n = (870.9, 3.5), (868.3, 4.0), (868.2, 7.7), (884.8, 2.4)
m100, s100 = wmean([c100o, c100n]); m50, s50 = wmean([c50o, c50n])
d = m50 - m100; sd = math.hypot(s50, s100)
print(f"100 kPa {m100:.2f}+-{s100:.2f}; 50 kPa {m50:.2f}+-{s50:.2f}; diff {d:.2f}+-{sd:.2f} = {d/sd:.2f} sigma")
quantity(f"{m100} s", "869.8 s", rel_tol=2e-5); quantity(f"{m50} s", "883.3 s", rel_tol=1e-4)
quantity(f"{d} s", "13.6 s", rel_tol=5e-3); quantity(f"{sd} s", "3.5 s", rel_tol=0.01)
quantity(f"{d/sd}", "3.9", rel_tol=0.01)
t0 = 2 * m50 - m100; s0 = math.hypot(2 * s50, s100)
print(f"extrapolated to 0 kPa: {t0:.1f} +- {s0:.1f} s")
quantity(f"{t0} s", "897 s", rel_tol=1e-3); quantity(f"{s0} s", "5 s", rel_tol=0.08)
P, a, bb = sp.symbols("P a b", real=True)
line = a + bb * P
identity((2 * line.subs(P, 50) - line.subs(P, 100)), line.subs(P, 0))
mo, so = wmean([c100o, c50o]); mn, sn = wmean([c100n, c50n])
print(f"old SFC {mo:.2f}+-{so:.2f}, new SFC {mn:.2f}+-{sn:.2f}")
quantity(f"{mo} s", "870.4 s", rel_tol=1e-4); quantity(f"{mn} s", "880.4 s", rel_tol=1e-4)
# tensions
jp = 877.2
beam, sb = 887.97, 2.04
ucn, su = 877.82, math.hypot(0.22, 0.185)
for label, side in (("facing (+4.0)", 4.0), ("symmetrised 3.8", 3.8), ("lower (-3.6)", 3.6)):
    sj = math.hypot(1.7, side)
    print(f"{label}: beam {(beam-jp)/math.hypot(sj, sb):.3f} sigma, UCNtau {(ucn-jp)/math.hypot(sj, su):.3f} sigma")
zb = (beam - jp) / math.hypot(math.hypot(1.7, 4.0), sb)
zu = (ucn - jp) / math.hypot(math.hypot(1.7, 4.0), su)
quantity(f"{zb}", "2.24", rel_tol=5e-3)
quantity(f"{zu}", "0.16", rel_tol=0.05)
raise SystemExit(finish())
