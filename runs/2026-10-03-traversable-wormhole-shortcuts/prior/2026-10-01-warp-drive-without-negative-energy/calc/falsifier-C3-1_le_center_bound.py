"""Falsifier C3-1: Le arXiv:2606.22531v4 Corollary 3.4 (quoted):
   m_f/m_i <= (cosh(3C/2) + s_i sinh(3C/2))^-2,  s_i = sqrt(1 - 2 m_i/R0),  0 < 2m_i/R0 < 24/25,
where C is the supported cavity centre's rapidity change in the interior Minkowski frame.
Compare with the photon-rocket value e^-C for the same rapidity (geometric units, G = c = 1).
Small-C expansion: bound ~ 1 - 3 s_i C, photon ~ 1 - C, so the bound exceeds e^-C iff s_i < 1/3,
i.e. 2m_i/R0 > 8/9.
"""
import math

def bound(C, comp):
    s = math.sqrt(1 - comp)
    return (math.cosh(1.5 * C) + s * math.sinh(1.5 * C)) ** -2

print("threshold compactness 2m/R0 where s = 1/3:", 1 - 1/9)
for comp in (0.0, 0.6, 0.889, 0.9, 0.95, 0.959):
    for C in (0.04, 0.08, 0.3):
        bd = bound(C, comp)
        ph = math.exp(-C)
        tag = "cheaper than photon rocket allowed" if bd > ph else "costlier than photon rocket"
        print(f"2m/R0={comp:5.3f} C={C:4.2f}: Le bound m_f/m_i <= {bd:.5f}; photon e^-C = {ph:.5f}; {tag}")
ok = bound(0.04, 0.95) > math.exp(-0.04) and bound(0.04, 0.6) < math.exp(-0.04)
print("PASS" if ok else "FAIL", "Le centre bound beats photon rocket only above 2m/R0 = 8/9 at small C")
print("PASS" if abs(bound(0.5, 0.0) - math.exp(-1.5)) < 1e-12 else "FAIL", "weak-field limit gives e^-3C")
