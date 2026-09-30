"""M-STATISTICIAN-08: missing error (F8) and candidate A's '5x BL1 systematic'.
Extra error e added in quadrature to the gap: Delta/sqrt(sD^2 + e^2) = n  ->  e = sqrt((Delta/n)^2 - sD^2).
Uniform inflation k of all errors: z/k = n -> k = z_unscaled/n. Lens: e3 = 2.45 s, e2 = 4.35 s, k3 = 1.57, k2 = 2.35,
'BL1 budget would have to grow about 2.3x to reach 2 sigma'; 'shift about 5x BL1's quoted 1.9 s'."""
import sys, math
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/statistician")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from _inputs import *
from math_checks import identity, limit, finish
import sympy as sp

mp_, sp_, *_ = wmean(PROTON)
ms, ss, c, d, S = wmean(STORAGE)
D = mp_ - ms; sD = q(sp_, ss * S); zu = D / q(sp_, ss)
e3 = math.sqrt((D / 3) ** 2 - sD ** 2); e2 = math.sqrt((D / 2) ** 2 - sD ** 2)
print("e3, e2", e3, e2); identity(f"{e3:.2f}", "2.45"); identity(f"{e2:.2f}", "4.35")
print("k3, k2", zu / 3, zu / 2); identity(f"{zu/3:.2f}", "1.57"); identity(f"{zu/2:.2f}", "2.35")
print("e2/1.9 =", e2 / 1.9, "; quadrature-grown BL1 sys sqrt(1.9^2+e2^2)/1.9 =", q(1.9, e2) / 1.9)
print("Delta/1.9 =", D / 1.9); identity(f"{D/1.9:.0f}", "5")
# symbolic: e -> 0 when n -> Delta/sD
Dl, s, n = sp.symbols("Dl s n", positive=True)
limit(sp.sqrt((Dl / n) ** 2 - s ** 2), "n", Dl / s, "0")
raise SystemExit(finish())
