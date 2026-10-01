"""M-MECHANIST-01: gap sizing (F2). Own transcription of D-20, D-22, D-27, D-28. Lifetimes in s (SI)."""
import math, sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import identity, series, quantity, units, finish

def tot(stat, sys_):
    return math.hypot(stat, sys_)

bl1 = (887.7, tot(1.2, 1.9))          # D-20
sil = (889.2, tot(3.0, 3.8))          # D-22 (unverified lead)
ucn = (877.82, tot(0.22, (0.20 + 0.17) / 2))  # D-27
grav = (881.5, tot(0.7, 0.6))         # D-28
w = [1 / bl1[1] ** 2, 1 / sil[1] ** 2]
m = (w[0] * bl1[0] + w[1] * sil[0]) / sum(w)
s = 1 / math.sqrt(sum(w))
print(f"proton-beam mean = {m:.3f} +- {s:.3f} s")
gap = m - ucn[0]
frac = gap / m
rate = 1 / ucn[0] - 1 / m
print(f"gap = {gap:.3f} s, fraction of beam = {frac*100:.4f} %, fraction of UCNtau = {gap/ucn[0]*100:.4f} %")
print(f"rate = {rate:.4e} s^-1, time constant = {1/rate:.4e} s = {1/rate/86400:.3f} d")
g_bl1 = bl1[0] - ucn[0]
print(f"BL1 alone gap = {g_bl1:.2f} s ({g_bl1/bl1[0]*100:.3f} %)")
g_gr = m - grav[0]
print(f"vs Gravitrap gap = {g_gr:.2f} s ({g_gr/m*100:.3f} %)")

quantity(f"{m} s", "887.97 s", rel_tol=2e-5)
quantity(f"{s} s", "2.04 s", rel_tol=5e-3)
quantity(f"{gap} s", "10.15 s", rel_tol=1e-3)
quantity(f"{frac}", "0.01143", rel_tol=1e-3)
quantity(f"{rate} Hz", "1.30e-5 Hz", rel_tol=5e-3)
quantity(f"{1/rate} s", "7.7e4 s", rel_tol=5e-3)
quantity(f"{1/rate/86400}", "0.89", rel_tol=6e-3)
quantity(f"{g_bl1} s", "9.88 s", rel_tol=1e-3)
quantity(f"{g_bl1/bl1[0]}", "0.0111", rel_tol=5e-3)
quantity(f"{g_gr} s", "6.5 s", rel_tol=1e-2)
quantity(f"{g_gr/m}", "0.0073", rel_tol=1e-2)
# identity: rate difference 1/a - 1/b = (b-a)/(ab); small-gap limit rate -> gap/tau^2
identity("1/a - 1/b", "(b - a)/(a*b)")
series("1/a - 1/(a + d)", "d", 0, 2, "d/a**2")
units("10.15 s / (877.82 s * 887.97 s)", "Hz")
raise SystemExit(finish())
