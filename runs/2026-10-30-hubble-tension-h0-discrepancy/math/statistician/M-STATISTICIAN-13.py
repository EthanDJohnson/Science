"""M-STATISTICIAN-13: correlated (GLS) local combination with a shared NGC 4258 anchor (F8).
Local values x_i, total errors s_i; anchor share w_i (SH0ES 1/3, CCHP 1, SBF 1, TF 0.5, one-step 0);
anchor error a = f * H0 (f = 0, 1.5%, 2.5%). The lens does not state how the anchor term enters, so two
conventions are tried: (A) off-diagonal only, C_ij = s_i^2 delta_ij + (1 - delta_ij) w_i w_j a^2;
(B) added everywhere, C_ij = s_i^2 delta_ij + w_i w_j a^2.
GLS: mean = (1^T C^-1 x)/(1^T C^-1 1), var = 1/(1^T C^-1 1). km/s/Mpc."""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-10-30-hubble-tension-h0-discrepancy/math/statistician")
import mpmath as mp
from _common import quad, close
from math_checks import identity, units, finish

x = [73.49, 70.39, 73.8, 73.3, 71.1, 71.6, 71.7]
s = [0.93, float(quad(1.22, 1.33, .70)), float(quad(.7, 2.3)), float(quad(2.1, 3.5)), 2.35, 3.7, 8.45]
w = [1 / 3, 1, 1, 0.5, 0, 0, 0]


def gls(f, conv, H0=73.0):
    a2 = (f * H0) ** 2
    n = len(x)
    C = mp.matrix(n, n)
    for i in range(n):
        for j in range(n):
            C[i, j] = (s[i] ** 2 if i == j else 0) + (w[i] * w[j] * a2 if (i != j or conv == "B") else 0)
    Ci = C ** -1
    one = mp.matrix([1] * n)
    den = (one.T * Ci * one)[0]
    m = (one.T * Ci * mp.matrix(x))[0] / den
    return m, 1 / mp.sqrt(den)


res = {}
for conv in ("A", "B"):
    for f in (0, 0.015, 0.025):
        for H0 in (67.6, 73.0):
            m, e = gls(f, conv, H0)
            zs = (m - 67.19) / quad(e, .38); zb = (m - 68.50) / quad(e, .58)
            res[(conv, f, H0)] = (m, e)
            print(f"conv {conv} f={f} H0a={H0}: local {float(m):.3f} +- {float(e):.3f}; z vs SPA {float(zs):.2f}, vs BB {float(zb):.2f}")
m0, e0 = res[("A", 0, 73.0)]
close("f = 0: local mean", m0, 72.77, 0.01); close("f = 0: sigma", e0, 0.72, 0.01)
close("f = 0: z vs SPA", (m0 - 67.19) / quad(e0, .38), 6.85, 0.01)
close("f = 0: z vs BB", (m0 - 68.50) / quad(e0, .58), 4.62, 0.01)
print("Lens: f = 1.5% -> 72.86 +- 0.80 (z 6.40 / 4.41); f = 2.5% -> 73.24 +- 0.83 (z 6.66 / 4.70)")
# GLS with diagonal C reduces to inverse-variance weighting (limit f -> 0)
identity("(x1/s1**2 + x2/s2**2)/(1/s1**2 + 1/s2**2)", "(x1*s2**2 + x2*s1**2)/(s1**2 + s2**2)")
units("0.025 * 73 km/s/Mpc", "km/s/Mpc")
raise SystemExit(finish())
