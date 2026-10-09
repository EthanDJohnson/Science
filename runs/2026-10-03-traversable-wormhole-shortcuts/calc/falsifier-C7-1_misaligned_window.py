"""Falsifier C7-1: where does the achronal-ANEC barrier act for misaligned mouths?

Toy model of M-DECOMPOSER-08 (verified corrected form, refuted lens claim):
point mouths in flat exterior, throat delay A->B tau = T_thru - Delta (light-years
and years, c = 1 ly/yr). Shortcut iff tau < d. CTC iff tau <= -d.
A complete achronal throat-crossing null geodesic exists iff
    -d < tau <= d * max|e.n|  over directions n fixed by the relative mouth rotation R.
For R in SO(3) with axis at angle alpha to the separation e, max|e.n| = |cos alpha|.
So the conjecture can first act at Delta_a = T_thru - d|cos alpha|, which lies in
[Delta_s, T_thru]; the one-way-shortcut sub-window [Delta_s, Delta_a) is not
governed by the conjecture.
Units: years and light-years (c = 1 ly/yr).
"""
import math

ell = 3.0e3            # ly, MM throat scale (quoted, held fixed)
T_thru = math.pi * ell # yr, MM transit time pi*ell/c

for d in (1.0e3, ell):
    D_s = T_thru - d
    D_ctc = T_thru + d
    print(f"d = {d:.0f} ly: T_thru = {T_thru:.4g} yr, Delta_s = {D_s:.4g} yr, Delta_CTC = {D_ctc:.4g} yr, window 2d = {2*d:.4g} yr")
    for alpha_deg in (0, 30, 60, 80, 90):
        c = abs(math.cos(math.radians(alpha_deg)))
        D_a = T_thru - d * c
        unprotected = D_a - D_s          # shortcut but no achronal throat geodesic
        protected_before_ctc = D_ctc - D_a
        print(f"   axis angle {alpha_deg:3d} deg: barrier onset Delta_a = {D_a:.4g} yr; "
              f"unprotected one-way-shortcut span = {unprotected:.4g} yr "
              f"({unprotected/(2*d):.3f} of window); margin before CTC = {protected_before_ctc:.4g} yr")
    # sanity: barrier always before CTC since D_a <= T_thru < T_thru + d
    assert all(T_thru - d*abs(math.cos(math.radians(a))) < D_ctc for a in range(0, 91))
print("check: Delta_a <= T_thru < Delta_CTC for every axis angle (barrier precedes CTC): PASS")

# --- MM's own throat condition Omega << 1/ell (arXiv:2008.06618 App. B) vs the
# accumulation routes C7 lists. SI units.
G = 6.674e-11; c = 2.998e8; Msun = 1.989e30; yr = 3.156e7; ly = c * yr
gap = c / (ell * ly)                       # s^-1, energy gap 1/ell in exterior time
print(f"MM gap 1/ell = {gap:.3g} s^-1 (ell = 3000 ly)")
# (a) mouth parked on Sgr A* ISCO (M = 4.3e6 Msun, r = 6GM/c^2): orbital angular frequency
M = 4.3e6 * Msun
r = 6 * G * M / c**2
Om_isco = math.sqrt(G * M / r**3)
print(f"Sgr A* ISCO: r = {r:.3g} m, Omega = {Om_isco:.3g} s^-1, Omega*ell/c = {Om_isco/gap:.3g}")
# (b) 0.9c circuit keeping separation ~ d = 1000 ly (radius <= d/2)
R = 500 * ly
Om_09 = 0.9 * c / R
print(f"0.9c circuit, R = 500 ly: Omega = {Om_09:.3g} s^-1, Omega*ell/c = {Om_09/gap:.3g}")
# (c) slow circuit satisfying Omega*ell/c = 0.01 with R = d = 1000 ly: speed and time to Delta_s
v = 0.01 * gap * (1000 * ly)               # m/s
beta = v / c
D_s = T_thru - 1000.0                       # yr
T_acc = D_s / (1 - math.sqrt(1 - beta**2))  # yr
print(f"slow circuit obeying Omega*ell/c = 0.01 at R = 1000 ly: v = {beta:.3g} c, time to Delta_s = {T_acc:.3g} yr")
