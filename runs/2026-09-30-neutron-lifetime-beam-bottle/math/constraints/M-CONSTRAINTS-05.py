"""M-CONSTRAINTS-05 (F7, F17): separating power. Two sharp hypotheses tau = 877.82 s and 887.7 s (gap 9.88 s).
n sigma separation by the SM route needs sigma_tau <= gap/n, with sigma_tau^2 = (1142.7 sigma_lam)^2 + 0.577^2 (Vud) + 0.19^2 (RC).
A new measurement x with error s vs a pole P with error sP: z = gap/sqrt(s^2 + sP^2)."""
import math
from _common import near, TAU_UCN, S_UCN_UP, TAU_BL1, S_BL1, LAM, tau_beta, VUD_GS, S_VUD_GS
from math_checks import limit, inequality, finish

gap = TAU_BL1 - TAU_UCN
near("gap (s)", gap, 9.88, 0.006)
dtdl = 1142.7
s_vud = 2 * 878.5 / VUD_GS * S_VUD_GS
for n, want in [(3, 0.0028), (5, 0.00165)]:
    sl = math.sqrt((gap / n) ** 2 - s_vud**2 - 0.19**2) / dtdl
    near(f"sigma_lam for {n} sigma", sl, want, 6e-5 if n == 3 else 1e-5)
    print(f"   (subtracting also UCNtau 0.30 s: {math.sqrt((gap / n) ** 2 - s_vud**2 - 0.19**2 - 0.3**2) / dtdl:.5f})")
near("BL1 cap", gap / S_BL1, 4.4, 0.05)
limit("g/sqrt(s**2 + b**2)", "s", 0, "g/b")        # cap as the SM error -> 0
inequality("g/sqrt(s**2 + b**2)", "<=", "g/b", domain={"s": (0, 10)})
# Nab 0.04%
slN = 0.0004 * 1.2764
near("Nab dlam", slN, 5.1e-4, 6e-6); near("Nab dtau", slN * dtdl, 0.58, 0.006)
p3, asp = LAM["PERKEO III"], LAM["aSPECT 2024"]
near("Nab at aSPECT value vs PERKEO III", (p3[0] - asp[0]) / math.hypot(slN, p3[1]), 12.8, 0.1)
near("Nab at PERKEO value vs aSPECT", (p3[0] - asp[0]) / math.hypot(slN, asp[1]), 3.5, 0.06)
sN = math.sqrt((slN * dtdl) ** 2 + s_vud**2 + 0.19**2)
near("Nab sigma(tau_beta)", sN, 0.84, 0.006)
tP, tA = tau_beta(p3[0]), tau_beta(asp[0])
near("PERKEO-like tau_beta vs BL1", (TAU_BL1 - tP) / math.hypot(sN, S_BL1), 3.8, 0.06)
near("aSPECT-like tau_beta vs UCNtau", (tA - TAU_UCN) / math.hypot(sN, S_UCN_UP), 13.2, 0.06)
for s, w1, w2 in [(1.0, 4.0, 9.5), (2.0, 3.3, 4.9), (0.3, 4.4, 23.0)]:
    near(f"storage-like reading at {s} s vs BL1", gap / math.hypot(s, S_BL1), w1, 0.06)
    near(f"beam-like reading at {s} s vs UCNtau", gap / math.hypot(s, S_UCN_UP), w2, 0.5 if w2 > 20 else 0.06)
raise SystemExit(finish())
