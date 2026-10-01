#!/usr/bin/env python3
"""Falsifier C4-2 (bounds): does the candidate's own n -> n' parameter window survive the
SNS cold-neutron regeneration limit p < 2.5e-8 (Broussard et al. PRL 128, 212503 (2022), 95% CL)?

SPECULATIVE PHYSICS (mirror sector). Units SI unless stated; Delta_m quoted in neV.

Method (no 'equal passages' premise):
 1. For each Delta_m in the candidate's window (resonance inside the 4.6 T trap, Delta_m from
    |mu_n| * 4.6 T = 277 neV up to ~40 neV above it), solve for the theta0 that gives
    tau_beam/tau_beta = 1.0113 in a BL1-like solenoid (toolkit beam_solenoid: 60 cm long,
    5 cm bore radius, trap |z| < 0.1 m; two bore radii tried), velocity-averaged over a
    cold-beam density spectrum.
 2. With that same theta0, compute the SNS regeneration probability in a split-pair profile
    matching the quoted magnet (4.8 T at centre, 6.6 T peaks at +-6.3 cm), neutron state
    collapsed at the absorber: p = P(n->n', upstream -> absorber) * P(n'->n, absorber -> downstream),
    P(n'->n) = P(n->n') for a 2x2 unitary. Spin-averaged (spin -1 never resonates; included).
    Velocities 776-1798 m/s (2.2-5.1 Angstrom, the paper's band), flat in wavelength.
    Landau-Zener hops composed incoherently (velocity spread averages phases), as in the tool.
 3. One direct numerical check (Schroedinger integration) at Delta_m = 289 neV, theta0 = 5e-3,
    v = 500 m/s against the paper's worked example (~60% n' at the catcher).
Ratio p / 2.5e-8 >> 1 means the candidate's parameters are excluded.
"""
import sys
import math
import numpy as np

sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/tools")
import nn_mirror_osc as m  # noqa: E402

P_LIMIT = 2.5e-8          # Broussard 2022, 95% CL apparent transmission
TARGET = 1.0113           # tau_beam / tau_beta needed (1.13 % ; candidates.md reference gap)

# ---------------- split-pair magnet model: two current loops at +-d, radius a
def loop_pair(z, a, d):
    g = lambda u: (1.0 + (u / a) ** 2) ** -1.5  # noqa: E731
    return g(z - d) + g(z + d)

def fit_split_pair():
    best = None
    for a in np.linspace(0.02, 0.10, 161):
        for d in np.linspace(0.03, 0.10, 141):
            zz = np.linspace(0, 0.2, 2001)
            b = loop_pair(zz, a, d)
            zpk = zz[np.argmax(b)]
            ratio = b[0] / b.max()
            err = (zpk - 0.063) ** 2 / 0.002 ** 2 + (ratio - 4.8 / 6.6) ** 2 / 0.005 ** 2
            if best is None or err < best[0]:
                best = (err, a, d, zpk, ratio)
    return best

err, A, D, zpk, ratio = fit_split_pair()
norm = 6.6 / loop_pair(np.array([zpk]), A, D)[0]
B_sns = lambda z: norm * loop_pair(np.asarray(z, float), A, D)  # noqa: E731
print(f"SNS split-pair model: loop radius a = {A:.4f} m, half-separation d = {D:.4f} m; "
      f"peak {6.6:.2f} T at z = +-{zpk:.4f} m, centre {float(B_sns(0.0)):.3f} T (target 4.8 T)")
zz = np.linspace(-0.3, 0.3, 6001)
gr = np.abs(np.gradient(B_sns(zz), zz))
print(f"  max |dB/dz| = {gr.max():.1f} T/m")

# ---------------- velocity sets
lam = np.linspace(2.2e-10, 5.1e-10, 12)
v_sns = 3956.0e-10 / lam            # m/s (h/m_n = 3.956e-7 m^2/s)
w_sns = np.ones_like(v_sns)
v_bl = np.linspace(400.0, 2200.0, 7)
w_bl = v_bl ** 2 * np.exp(-(v_bl / 800.0) ** 2)   # density weight (mechanist's choice)

def sns_regen(dm, eps, zc=0.0):
    tot = 0.0
    for v, w in zip(v_sns, w_sns / w_sns.sum()):
        for s in (+1, -1):
            p1 = m.profile_probability_analytic(B_sns, -0.6, zc, v, eps, dm, s, incoherent_multi=True)
            # second segment: start at absorber, evolve to far downstream; P(n'->n) = P(n->n')
            p2 = m.profile_probability_analytic(lambda z: B_sns(z), zc, 0.6, v, eps, dm, s,
                                                incoherent_multi=True)
            tot += 0.5 * w * p1 * p2
    return tot

def bl_ratio(dm, theta0, radius):
    r = m.beam_solenoid(dm=dm, theta0=theta0, B_center=4.6, v=v_bl, weights=w_bl, radius=radius)
    return r["tau_beam_over_tau_beta"], r["eps_J"], r["P_trap"]

def solve_theta0(dm, radius):
    lo, hi = math.log(1e-4), math.log(5e-2)
    if bl_ratio(dm, math.exp(hi), radius)[0] < TARGET:
        return None
    for _ in range(16):
        mid = 0.5 * (lo + hi)
        if bl_ratio(dm, math.exp(mid), radius)[0] < TARGET:
            lo = mid
        else:
            hi = mid
    return math.exp(hi)

print()
print(f"mu_n * 4.6 T = {m.MU_N * 4.6 / m.NEV:.1f} neV ; mu_n * 4.8 T = {m.MU_N * 4.8 / m.NEV:.1f} neV ; "
      f"mu_n * 6.6 T = {m.MU_N * 6.6 / m.NEV:.1f} neV")
print("Delta_m  radius  theta0(needed)  tau_nn'(s)   P_trap     SNS p (zc=-3,0,+3 cm)            min p / 2.5e-8")
worst = None
for dm_nev in (278.0, 280.0, 285.0, 290.0, 300.0, 310.0, 320.0):
    dm = dm_nev * m.NEV
    for radius in (0.05, 0.10):
        th = solve_theta0(dm, radius)
        if th is None:
            print(f"{dm_nev:6.0f}   {radius:.2f}   not reachable with theta0 <= 5e-2")
            continue
        rr, eps, ptrap = bl_ratio(dm, th, radius)
        ps = [sns_regen(dm, eps, zc) for zc in (-0.03, 0.0, 0.03)]
        pmin = min(ps)
        fac = pmin / P_LIMIT
        worst = fac if worst is None else min(worst, fac)
        print(f"{dm_nev:6.0f}   {radius:.2f}   {th:.3e}      {m.HBAR / eps:.3e}  {ptrap:.3e}  "
              f"{ps[0]:.2e} {ps[1]:.2e} {ps[2]:.2e}     {fac:.2e}")
print(f"\nSmallest exclusion factor over the window: p_pred / p_limit >= {worst:.2e}")

# ---------------- numerical cross-check vs the paper's worked example (Fig. 1)
dm = 289.0 * m.NEV
eps = m.eps_from_theta0(5e-3, dm)
Pz = m.evolve_profile(B_sns, -0.4, 0.0, 500.0, eps, dm, +1, n_steps=1_500_000)
print(f"\nWorked-example check (Delta_m = 289 neV, theta0 = 5e-3, v = 500 m/s, spin +1, no phase "
      f"averaging): P(n') at magnet centre = {Pz:.3f}  (paper: ~0.6 at the beam-catcher)")
Pa = m.profile_probability_analytic(B_sns, -0.4, 0.0, 500.0, eps, dm, +1, incoherent_multi=True)
print(f"  same point, phase-averaged LZ composition: {Pa:.3f}")
