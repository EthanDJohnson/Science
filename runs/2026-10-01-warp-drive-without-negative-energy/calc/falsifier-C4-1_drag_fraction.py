"""Falsifier C4-1: how much of the shell's push does an interior payload still feel?

Units: geometric (G = c = 1) for compactness; SI for trip times.
F = felt fraction = (payload proper acceleration needed to co-move with shell) / (shell acceleration) = 1 - kappa.

Sources of the laws used:
 (L1) Lynden-Bell, Bicak & Katz 1999 (gr-qc/9812033) eq. (3.10): (g_p)_in/(g_p)_out = (V_in/V_out)^-2 = (1 + m/b)^-2
      for an extremal charged-dust shell (q = m) of conformastatic radius b, with M/Z -> 0. Areal radius r_s = b + m.
 (L2) Same law transferred to a neutral thin shell: F = g00_in/g00_out = 1 - C, C = 2M/R (OUR ASSUMPTION, labelled).
 (L3) Rebuild centre lapse N = 0.761 (toolkit warp_shell.py, quoted from candidates.md): F = N^2 under L1/L2's g00 law.
 (L4) Candidate's linear coefficient kappa = 4M/R (harmonic gauge, no retardation, no pusher stresses).
 (L5) Einstein de Donder weak-field with retardation, as evaluated by LBK p.7: field = (11/3) (m/b) alpha -> kappa = 11 m /(3 b).
 (BC) Brill-Cohen rotational dragging, for comparison (Pfister et al. 2005 say linear 'compares favourably' with it):
      omega/Omega = 4a(2-a)/((1+a)(3-a)), a = m/(2 r_iso), C (areal) = 4a/(1+a)^2.
"""
import math

def F_L1(C):
    # C = 2m/(b+m) -> x = m/b = C/(2-C); F = (1+x)^-2 = (1 - C/2)^2
    return (1 - C / 2) ** 2

def F_L2(C):
    return 1 - C

def kappa_BC(C):
    # solve C(1+a)^2 = 4a for a in (0,1]
    lo, hi = 1e-15, 1.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if 4 * mid / (1 + mid) ** 2 < C:
            lo = mid
        else:
            hi = mid
    a = 0.5 * (lo + hi)
    return 4 * a * (2 - a) / ((1 + a) * (3 - a))

print("=== Felt fraction F = 1 - kappa versus areal compactness C = 2M/R ===")
print(f"{'C':>8} {'F_L1(extremal LBK)':>20} {'F_L2(neutral g00)':>18} {'F_lin=1-2C (4M/R)':>20} {'F=1-11C/6 (LBK p7)':>20} {'1-BC rot':>10}")
for label, C in [("0.333 (R2=20m)", 1 / 3), ("0.667 (R1=10m)", 2 / 3), ("8/9 Buchdahl", 8 / 9), ("48/49 DEC", 48 / 49)]:
    print(f"{label:>16} {F_L1(C):12.4f} {F_L2(C):18.4f} {1 - 2 * C:20.4f} {1 - 11 * C / 6:20.4f} {1 - kappa_BC(C):10.4f}")

N = 0.761
print(f"\nRebuild centre lapse N = {N}: F = N^2 = {N**2:.4f}  (kappa = {1 - N**2:.4f}); if F = N instead: {N:.3f}")

print("\nLinear coefficient at the published mass (M = 4.49e27 kg):")
G, c = 6.674e-11, 2.998e8
M = 4.49e27
for R in (10.0, 20.0):
    m = G * M / c**2
    print(f"  R = {R:4.0f} m: m = {m:.3f} m, 4m/R = {4*m/R:.3f}, 11m/(3R) = {11*m/(3*R):.3f}, LBK strong-field kappa (C=2m/R) = {1-F_L1(2*m/R):.3f}, neutral g00 kappa = {2*m/R:.3f}")

print("\nCompactness needed for felt fraction F (neutral g00 law L2: C = 1 - F; extremal L1: C = 2(1 - sqrt F)):")
for F in (0.5, 0.1, 0.01):
    print(f"  F = {F}: C_L2 = {1-F:.3f}, C_L1 = {2*(1-math.sqrt(F)):.3f}  (Buchdahl 0.889, DEC cap 0.980)")

# Trip-time value of g-reduction: payload limited to 1 g felt, shell pushed at a = 1 g / F.
ly = 9.4607e15
d = 4.37 * ly
g = 9.80665
yr = 3.15576e7
def trip(a):
    D = d / 2
    t_half = math.sqrt((D / c) ** 2 + 2 * D / a)
    tau_half = (c / a) * math.acosh(1 + a * D / c**2)
    return 2 * t_half / yr, 2 * tau_half / yr
print("\nAlpha Cen 4.37 ly, accelerate-flip-decelerate at shell acceleration a = 1 g / F (payload feels 1 g):")
for F in (1.0, 0.579, 0.333, 0.111, 0.0204):
    T, tau = trip(g / F)
    print(f"  F = {F:6.4f}: a = {1/F:6.2f} g, Earth-frame time = {T:.3f} yr, ship time = {tau:.3f} yr")
print(f"  light-time floor = 4.37 yr")
