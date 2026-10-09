"""Crux C3: does Le's Corollary 3.4 (cavity-centre rapidity C) beat the photon-rocket floor
in the exterior (Bondi) rapidity that sets arrival between exterior rest points?

Inputs (from verdict C3-1, quoting Le arXiv:2606.22531v4 Cor. 3.4):
  m_f/m_i <= (cosh(3C/2) + s sinh(3C/2))^-2,  s = sqrt(1 - 2m/R0)   (geometric units)
  exterior DEC bound (Le p.18, elastic model): m_f/m_i <= e^{-3L}
  photon rocket (exterior, Lemma 2.1): m_f/m_i <= e^{-L}

Hypothesis tested (ours, NOT read in Le): the interior Minkowski frame runs on clocks
redshifted by the interior lapse s relative to infinity, so to first order a displacement
dx per asymptotic time dt reads as interior velocity v_int = v_ext / s, i.e. C ~ L/s.
Check 1: small-C expansion of Cor 3.4 is 1 - 3 s C; with C = L/s this is 1 - 3L, i.e. the
         exterior e^{-3L} bound, independent of compactness.
Check 2: Cor 3.4 beats e^{-C} at small C iff 3s < 1 iff 2m/R0 > 8/9 (refuter's threshold).
Check 3: at the refuter's point (2m/R0 = 0.95, C = 0.04) compare with the photon rocket in
         the mapped exterior rapidity L = sC.
"""
import math

def cor34(C, comp):
    s = math.sqrt(1 - comp)
    return (math.cosh(1.5 * C) + s * math.sinh(1.5 * C)) ** -2

# Check 1: small-C slope
for comp in (0.0, 0.335, 0.667, 8/9, 0.95):
    s = math.sqrt(1 - comp)
    C = 1e-6
    slope = (1 - cor34(C, comp)) / C
    print(f"2m/R0={comp:.4f}: s={s:.5f}; slope d(1-m_f/m_i)/dC = {slope:.6f}; 3s = {3*s:.6f}; "
          f"slope per unit L=sC: {slope/s:.6f} (exterior e^-3L slope = 3)")

# Check 2: threshold where 3s = 1
s_th = 1/3
print(f"threshold 3s=1 -> 2m/R0 = 1 - s^2 = {1 - s_th**2:.6f} (8/9 = {8/9:.6f})")

# Check 3: refuter's point
comp, C = 0.95, 0.04
s = math.sqrt(1 - comp)
L = s * C
print(f"refuter point 2m/R0=0.95, C=0.04: Cor3.4 bound {cor34(C, comp):.5f}; e^-C {math.exp(-C):.5f} "
      f"(beats in C: {cor34(C, comp) > math.exp(-C)})")
print(f"  mapped exterior rapidity L = sC = {L:.5f}; photon rocket e^-L = {math.exp(-L):.5f}; "
      f"e^-3L = {math.exp(-3*L):.5f}; Cor3.4 worse than photon rocket in L: {cor34(C, comp) < math.exp(-L)}")

# Finite-C check across compactness: is Cor3.4 (at C = L/s) ever above e^-L ?
worst = None
for comp in [i/1000 for i in range(0, 960, 5)]:
    s = math.sqrt(1 - comp)
    for L in (0.001, 0.01, 0.0408, 0.1, 0.5, 1.0):
        r = cor34(L / s, comp) / math.exp(-L)
        if worst is None or r > worst[0]:
            worst = (r, comp, L)
print(f"max over grid of Cor3.4(C=L/s)/e^-L = {worst[0]:.6f} at 2m/R0={worst[1]:.3f}, L={worst[2]} "
      f"(<1 means never beats photon rocket in exterior rapidity)")

# Published 2024 shell, 0.04 c leg: compare the two readings
v = 0.04
Lleg = math.atanh(v)
for comp in (0.335, 0.667):
    s = math.sqrt(1 - comp)
    print(f"2024 shell 2m/R={comp}: one leg L={Lleg:.5f}; photon e^-L={math.exp(-Lleg):.5f}; "
          f"Cor3.4 at C=L/s: {cor34(Lleg/s, comp):.5f}; e^-3L={math.exp(-3*Lleg):.5f}")
