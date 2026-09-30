#!/usr/bin/env python3
"""Falsifier C4-0 (magnitude): does the strong-field n -> n' mechanism that lengthens the BL1
proton-beam lifetime by ~1.1% survive the SNS regeneration limit p < 2.5e-8 (Broussard et al. 2022)?

Units: SI inside (J, T, m, m/s, s); energies printed in neV.

Steps
 A. For each mass splitting Delta_m in C4's window (just above |mu_n| * 4.6 T = 277.4 neV, where BL1
    has no resonance crossing), find theta0 such that BL1's tau_beam/tau_beta = 887.7/877.82
    (the gap C4 must carry), using the run's tested tool nn_mirror_osc.beam_solenoid
    (Berezhiani geometry: 0.6 m solenoid, 4.6 T centre, trap |z| < 0.1 m).
 B. With that (Delta_m, theta0), compute the n -> n' -> n regeneration probability through a model
    SNS magnet: symmetric double-hump profile with 6.63 T peaks (400 neV) and a 4.79 T central dip
    (289 neV), the features Broussard et al. name for their Fig. 1 field; absorber at the centre.
    P1 = P(n -> n') at the absorber (oscillation-averaged adiabatic + Landau-Zener, crossings
    composed incoherently); for a symmetric profile time reversal gives P(n' -> n) on the far half
    = P1, so p_regen = <P1^2> over spin (+/-) and velocity. Three hump widths bracket the gradient.
 C. Numerical spot check of P1 with the exact 2x2 integrator (evolve_profile).
 D. Magnitude ledger: beam shift if P_trap were capped by the SNS limit.
"""
import sys
import math
import numpy as np

sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/tools")
import nn_mirror_osc as m  # noqa: E402

NEV = m.NEV
MU = m.MU_N
TAU_BEAM, TAU_TRUE = 887.7, 877.82        # s: BL1 and magnetic-trap average (candidates.md matrix)
R_NEED = TAU_BEAM / TAU_TRUE
P_LIMIT = 2.5e-8                           # SNS 95% CL apparent transmission (Broussard 2022)
VS = np.array([500.0, 800.0, 1100.0, 1500.0, 2000.0])   # m/s, cold-beam velocities, equal weight

print(f"|mu_n| = {MU/NEV:.4f} neV/T; |mu_n|*4.6 T = {MU*4.6/NEV:.2f} neV; "
      f"|mu_n|*4.79 T = {MU*4.79/NEV:.1f} neV; |mu_n|*6.63 T = {MU*6.63/NEV:.1f} neV")
print(f"required tau_beam/tau_beta = {R_NEED:.5f}  (shift {TAU_BEAM-TAU_TRUE:.2f} s)")


def bl1_ratio(dm, th):
    r = m.beam_solenoid(dm=dm, theta0=th, B_center=4.6, v=VS, n_trap=21)
    return r


def theta_needed(dm):
    th = 1e-3
    for _ in range(6):
        r = bl1_ratio(dm, th)
        # P_trap ~ theta0^2 in the adiabatic (no-crossing) regime; rescale on (ratio - 1)
        th_new = th * math.sqrt((R_NEED - 1) / (r["tau_beam_over_tau_beta"] - 1))
        if abs(th_new / th - 1) < 1e-3:
            th = th_new
            break
        th = min(th_new, 0.3)
    r = bl1_ratio(dm, th)
    return th, r


# ---- model SNS profile: sum of two Gaussians, dip/peak = 4.79/6.63
def make_sns(w):
    target = 4.79 / 6.63

    def shape(z, d):
        return np.exp(-(z - d) ** 2 / (2 * w * w)) + np.exp(-(z + d) ** 2 / (2 * w * w))

    lo, hi = 0.1 * w, 3.0 * w
    zz = np.linspace(0, 6 * w, 6001)
    for _ in range(80):
        d = 0.5 * (lo + hi)
        s = shape(zz, d)
        ratio = shape(np.array([0.0]), d)[0] / s.max()
        if ratio > target:
            lo = d
        else:
            hi = d
    s = shape(zz, d)
    A = 6.63 / s.max()
    B = lambda z: A * shape(np.asarray(z, float), d)  # noqa: E731
    zmax = zz[np.argmax(s)]
    gmax = np.max(np.abs(np.gradient(B(zz), zz)))
    return B, d, zmax, gmax


def sns_regen(dm, th, B, zstart):
    eps = m.eps_from_theta0(th, dm)
    vals = []
    p1s = []
    for v in VS:
        for s in (+1, -1):
            P1 = m.profile_probability_analytic(B, zstart, 0.0, v, eps, dm, s,
                                                incoherent_multi=True, n_grid=40001)
            vals.append(P1 * P1)
            p1s.append(P1)
    return float(np.mean(vals)), p1s


dms = [278.0, 280.0, 283.0, 286.0, 289.5, 292.0, 296.0, 300.0, 310.0]
widths = [0.05, 0.10, 0.20]
profiles = {}
for w in widths:
    B, d, zpk, g = make_sns(w)
    profiles[w] = (B, d)
    print(f"SNS model w = {w:.2f} m: hump offset d = {d:.3f} m, peak at z = {zpk:.3f} m, "
          f"B(0) = {float(B(np.array([0.0]))[0]):.3f} T, B(peak) = {float(B(np.array([zpk]))[0]):.3f} T, "
          f"max |dB/dz| = {g:.1f} T/m")

print("\nDelta_m | theta0 needed (BL1) | P_trap | P_det | tau ratio || SNS p_regen for w = 0.05/0.10/0.20 m"
      " | min ratio to limit")
rows = []
for dmv in dms:
    dm = dmv * NEV
    th, r = theta_needed(dm)
    regs = []
    for w in widths:
        B, d = profiles[w]
        reg, _ = sns_regen(dm, th, B, -(d + 6 * w))
        regs.append(reg)
    rows.append((dmv, th, r, regs))
    print(f"{dmv:6.1f} neV | {th:.3e} | {r['P_trap']:.4e} | {r['P_det']:.2e} | "
          f"{r['tau_beam_over_tau_beta']:.5f} || " + " / ".join(f"{x:.2e}" for x in regs)
          + f" | x{min(regs)/P_LIMIT:.2e}")

# ---- C. numerical spot check at Delta_m = 280 neV, v = 1000 m/s, spin +1, w = 0.10 m
dm = 280.0 * NEV
th = [row for row in rows if row[0] == 280.0][0][1]
eps = m.eps_from_theta0(th, dm)
B, d = profiles[0.10]
z0 = -(d + 6 * 0.10)
Pan = m.profile_probability_analytic(B, z0, 0.0, 1000.0, eps, dm, +1, incoherent_multi=True,
                                     n_grid=40001)
zg, Pg = m.evolve_profile(B, z0, 0.0, 1000.0, eps, dm, +1, n_steps=1_500_000, record=True)
tail = Pg[zg > -0.02]
print(f"\nspot check Delta_m = 280 neV, theta0 = {th:.3e}, v = 1000 m/s, s = +1, w = 0.10 m:")
print(f"  analytic (LZ + adiabatic) P1 = {Pan:.4f}; numeric P1 at absorber = {Pg[-1]:.4f}, "
      f"mean over last 2 cm = {tail.mean():.4f}")
eps_neV = eps / NEV
print(f"  eps = {eps_neV:.3f} neV, tau_nn' = {m.tau_from_eps(eps):.3e} s")

# ---- D. magnitude ledger
P_cap = math.sqrt(P_LIMIT)
print(f"\nSNS cap if equal passages: P <= {P_cap:.2e}; beam shift <= "
      f"{TAU_TRUE*(1/(1-P_cap)-1):.3f} s vs gap {TAU_BEAM-TAU_TRUE:.2f} s "
      f"({TAU_TRUE*(1/(1-P_cap)-1)/(TAU_BEAM-TAU_TRUE)*100:.2f}% of it)")
worst = min(min(r[3]) for r in rows)
print(f"smallest predicted SNS regeneration over the C4 window and profiles = {worst:.2e} "
      f"= {worst/P_LIMIT:.1e} x the 95% CL limit")

# ---- E. loophole check: attenuation of n' inside the B4C absorber (sintered B4C, natural boron)
# n in matter: energy raised by Fermi potential V, absorbed at rate G = N v sigma_a (1/v law -> v-independent).
# n' in matter acquires admixture (eps/delta_mat)^2, so its absorption rate is G (eps/delta_mat)^2,
# delta_mat = Delta_m - s|mu_n|B - V (Berezhiani-type two-level model with complex optical potential).
HB = 1.054571817e-34; MN = 1.67492750e-27; NA = 6.02214076e23
rho, M = 2.52e3, 55.25e-3                     # kg/m^3 (nominal), kg/mol for B4C
Nf = rho / M * NA                             # formula units per m^3
b = (4 * 5.30 + 6.646) * 1e-15                # m, coherent scattering lengths: B (nat) 5.30 fm, C 6.646 fm
V = 2 * math.pi * HB ** 2 / MN * Nf * b
sig = 4 * 767e-28                             # m^2 per formula at 2200 m/s (natural B, 767 b)
G = Nf * 2200.0 * sig                         # s^-1
print(f"\nB4C: Fermi potential V = {V/NEV:.0f} neV; n absorption rate G = {G:.2e} 1/s")
for dmv in (280.0, 300.0):
    th = [r for r in rows if r[0] == dmv][0][1]
    eps = m.eps_from_theta0(th, dmv * NEV)
    for s in (+1, -1):
        dmat = dmv * NEV - s * MU * 4.79 - V
        rate = G * (eps / dmat) ** 2
        for L in (0.1, 1.0):
            t = L / 1000.0
            print(f"  Delta_m {dmv:.0f} neV, s={s:+d}: delta_mat = {dmat/NEV:+.0f} neV, n' absorption "
                  f"{rate:.1f} 1/s; survival through {L:.1f} m at 1000 m/s = {math.exp(-rate*t):.4f}")
print("attenuation needed to hide the smallest predicted signal: factor "
      f"{worst/P_LIMIT:.1e} = e^{math.log(worst/P_LIMIT):.1f}")
