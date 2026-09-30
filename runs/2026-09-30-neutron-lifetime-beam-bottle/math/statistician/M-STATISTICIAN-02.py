"""M-STATISTICIAN-02: beam-storage gap (F4, S1, D-35 supersession).
Delta = m_p - m_s, sigma_D = sqrt(sigma_p^2 + sigma_s^2) (independent classes), z = Delta/sigma_D,
p2 = erfc(z/sqrt2). Fraction 1 - m_s/m_p; missing rate 1/m_s - 1/m_p (s^-1). Lifetimes in s (SI)."""
import sys
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/statistician")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from _inputs import *
from math_checks import identity, limit, series, quantity, units, finish
import sympy as sp

mp_, sp_, *_ = wmean(PROTON)
ms, ss, c, d, S = wmean(STORAGE)
D = mp_ - ms
sD = q(sp_, ss * S); sDu = q(sp_, ss)
z, zu = D / sD, D / sDu
say("Delta (s)", f"{D:.3f} +- {sD:.3f}", "9.65 +- 2.08")
say("z scaled / unscaled", f"{z:.3f} / {zu:.3f}", "4.63 / 4.70")
say("p2", f"{p2(z):.3g}", "3.7e-6")
identity(f"{D:.2f}", "9.65"); identity(f"{sD:.2f}", "2.08")
identity(f"{z:.2f}", "4.63"); identity(f"{zu:.2f}", "4.70")
identity(f"{p2(z):.1e}", "3.7e-6")
frac = 1 - ms / mp_
rate = 1 / ms - 1 / mp_
say("fraction", frac, "0.0109"); say("rate s^-1", rate, "1.24e-5")
identity(f"{frac:.4f}", "0.0109"); identity(f"{rate:.2e}", "1.24e-5")
# symbolic: missing rate = Delta/(m_s m_p), and small-Delta limit rate -> Delta/m^2
a, b = sp.symbols("a b", positive=True)
identity(1 / a - 1 / b, (b - a) / (a * b))
Dl = sp.symbols("Dl", positive=True)
series(1 / a - 1 / (a + Dl), "Dl", 0, 2, "Dl/a**2")
units("1/(878.32 s) - 1/(887.97 s)", "Hz")
quantity("1/(878.32 s) - 1/(887.97 s)", "1.2373e-5 Hz", rel_tol=1e-3)
# BL1 alone and Sussex alone vs scaled storage
for row, lens in [(BL1, "4.10"), (SUS, "2.24")]:
    zz = (row[1] - ms) / q(row[2], ss * S)
    say(f"{row[0]} vs storage z", f"{zz:.3f}", lens); identity(f"{zz:.2f}", lens)
# 2018 averages D-33: beam 888.0(2.0) vs trap 879.4(0.6)
z18 = (888.0 - 879.4) / q(2.0, 0.6)
say("2018 gap z", f"{z18:.3f}", "4.12"); identity(f"{z18:.2f}", "4.12")
raise SystemExit(finish())
