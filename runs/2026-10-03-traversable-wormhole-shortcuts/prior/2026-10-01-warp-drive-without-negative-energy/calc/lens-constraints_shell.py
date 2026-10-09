#!/usr/bin/env python3
"""Constraints lens: the Fuchs et al. 2024 warp shell (rebuilt by warp_shell.py), energy
conditions for ALL observers with the shift on, the shift cap, slice energy, light travel
along the axis, and momentum bookkeeping.

Units: metric and curvature in geometric units (x^0 = ct, lengths in m, T in 1/m^2);
SI conversions printed (J/m^3 = Pa via c^4/G, kg via c^2/G).

1. Shell at published parameters (M = 4.49e27 kg, R1 = 10 m, R2 = 20 m) for
   beta_warp in {0, 0.02 (the paper's EC-checked case), 0.04 (Table 1), 0.08, 0.15, 0.25, 0.4}.
   NumericSpacetime FD scan over the whole wall (r from R1 - 1 m to 24 m, all angles to the
   shift axis x, two azimuths), FD step h in {0.1, 0.05} m (the metric is Hermite-interpolated
   from a 0.006 m radial grid, so h must exceed the grid spacing), exact type-I tests.
2. Eulerian slice integral E-, E+ (axisymmetric about x) and comparison with M_ADM.
3. Light along the x axis through the centre: coordinate speeds from g_00, g_0x, g_xx and the
   one-way travel time over [-L, L] relative to flat 2L (Shapiro-type delay), both directions;
   the shift needed for a forward time ADVANCE.
4. ADM 4-momentum: exterior exactly Schwarzschild with zero shift -> P_ADM = 0, M_ADM unchanged.
"""
import math
import sys
import time

import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from numeric_stress_energy import NumericSpacetime  # noqa: E402
from warp_shell import build_shell  # noqa: E402
from gr_tensors import to_si  # noqa: E402

C = 299792458.0
G = 6.67430e-11
MJ, MSUN = 1.898e27, 1.989e30
M, R1, R2 = 4.49e27, 10.0, 20.0


def wall_points(nr=16, nth=13):
    rr = np.linspace(R1 - 1.0, 24.0, nr)
    th = np.linspace(0.05, math.pi - 0.05, nth)
    pts = []
    for phi in (0.0, 0.9):
        for a in rr:
            for b in th:
                pts.append((0.0, a * math.cos(b), a * math.sin(b) * math.cos(phi), a * math.sin(b) * math.sin(phi)))
    return np.array(pts)


def gfun(shell):
    def g(t, x, y, z):
        G4 = shell.metric_cartesian(t, x, y, z)
        return [[G4[..., a, b] for b in range(4)] for a in range(4)]
    return g


def scan(shell, h, pts):
    st = NumericSpacetime(gfun(shell), h=h)
    return st, st.scan_energy_conditions(pts)


def light_time(shell, L=2000.0, n=400001, y=0.0):
    x = np.linspace(-L, L, n)
    g = shell.metric_cartesian(0.0, x, np.full_like(x, y), np.zeros_like(x))
    g00, g0x, gxx = g[:, 0, 0], g[:, 0, 1], g[:, 1, 1]
    disc = np.sqrt(g0x ** 2 - g00 * gxx)
    u_plus = (-g0x + disc) / gxx      # dx/d(ct) > 0
    u_minus = (-g0x - disc) / gxx     # dx/d(ct) < 0
    dx = x[1] - x[0]
    tp = np.sum(1.0 / u_plus) * dx
    tm = np.sum(1.0 / np.abs(u_minus)) * dx
    return tp, tm, 2 * L, u_plus[n // 2], abs(u_minus[n // 2])


def main():
    pts = wall_points()
    print(f"wall points: {len(pts)} (r in [{R1-1}, 24] m, 13 angles to the x axis, 2 azimuths)")
    for beta in (0.0, 0.02, 0.04, 0.08, 0.15, 0.25, 0.4):
        shell = build_shell(M, R1, R2, beta_warp=beta)
        for h in (0.1, 0.05):
            t0 = time.time()
            st, sc = scan(shell, h, pts)
            print(f"beta_warp = {beta:.2f}, h = {h} m: unconverged {sc['unconverged']}, skipped {sc['skipped']};"
                  f" robust violations {sc['violations']}; strict {sc['violations_strict']}; types {sc['types']};"
                  f" worst nec_min {sc['worst']['nec_min'][0]:.3e} 1/m^2 at {tuple(round(q,2) for q in sc['worst']['nec_min'][1])};"
                  f" min Eulerian rho {sc['worst']['rho_eulerian'][0]:.3e} 1/m^2  [{time.time()-t0:.1f}s]")
        if beta in (0.02, 0.04):
            # NEC margin relative to the local energy density at the worst point
            r = st.energy_conditions(np.array(sc['worst']['nec_min'][1]))
            print(f"   worst-NEC point detail: type {r['type']}, rho_rest {r['rho_rest']}, pressures {r['pressures']},"
                  f" err {r['err']:.2e}, rho_E {r['rho_eulerian']:.4e} 1/m^2 = {to_si.energy_density_j_per_m3(r['rho_eulerian']):.3e} J/m^3")
    # finer angular scan of the shift-transition region at the paper's case and at the cap candidates
    print("--- dense scan of r in [10, 20] m (shift transition), 25 angles, h = 0.05 m ---")
    rr = np.linspace(10.05, 19.95, 34)
    th = np.linspace(0.02, math.pi - 0.02, 25)
    dense = np.array([(0.0, a * math.cos(b), a * math.sin(b), 0.0) for a in rr for b in th])
    for beta in (0.02, 0.04, 0.08, 0.15):
        shell = build_shell(M, R1, R2, beta_warp=beta)
        st, sc = scan(shell, 0.05, dense)
        print(f"beta_warp = {beta:.2f}: {sc['points']} pts, unconverged {sc['unconverged']}; robust {sc['violations']};"
              f" strict {sc['violations_strict']}; marginal {sc['marginal']}; types {sc['types']}; worst nec_min {sc['worst']['nec_min'][0]:.3e}")

    # slice energy (Eulerian), axisymmetric about x
    print("--- Eulerian slice energy (axisymmetric quadrature about the x axis) ---")
    for beta in (0.0, 0.02):
        shell = build_shell(M, R1, R2, beta_warp=beta)
        st = NumericSpacetime(gfun(shell), h=0.05)
        for nr, nth in ((130, 24), (195, 36)):
            r = (np.arange(nr) + 0.5) * (26.0 / nr)
            th = (np.arange(nth) + 0.5) * (math.pi / nth)
            RR, TT = np.meshgrid(r, th, indexing="ij")
            P = np.stack([np.zeros(RR.size), (RR * np.cos(TT)).ravel(), (RR * np.sin(TT)).ravel(), np.zeros(RR.size)], axis=1)
            rho = st.eulerian_density(P, halving=False)["rho"]
            sqrt_h = np.sqrt(np.linalg.det(st.g(P)[:, 1:, 1:]))
            w = 2 * math.pi * (RR ** 2 * np.sin(TT)).ravel() * (26.0 / nr) * (math.pi / nth)
            I = rho * sqrt_h * w
            Etot, Eneg, Epos = I.sum(), I[I < 0].sum(), I[I > 0].sum()
            print(f"beta = {beta}: n_r = {nr}, n_th = {nth}: E_total = {Etot:.5e} m = {to_si.mass_kg(Etot):.4e} kg"
                  f" ({to_si.mass_kg(Etot)/MJ:.4f} M_J); E- = {to_si.mass_kg(Eneg):.3e} kg; E+ = {to_si.mass_kg(Epos):.4e} kg;"
                  f" M_ADM = {shell.M_ADM:.4e} kg; E_total/M_ADM = {to_si.mass_kg(Etot)/shell.M_ADM:.4f}")

    # light along the axis
    print("--- light along the x axis through the centre (L = 2000 m each side) ---")
    for beta in (0.0, 0.02, 0.04, 0.1, 0.2, 0.25, 0.3):
        shell = build_shell(M, R1, R2, beta_warp=beta)
        tp, tm, flat, up, um = light_time(shell)
        print(f"beta = {beta:.2f}: interior light speeds +x {up:.4f} c, -x {um:.4f} c; one-way delay vs flat:"
              f" +x {(tp-flat)/C*1e9:.2f} ns, -x {(tm-flat)/C*1e9:.2f} ns; difference (-x) - (+x) = {(tm-tp)/C*1e9:.2f} ns")
    for L in (1000.0, 4000.0):
        shell = build_shell(M, R1, R2, beta_warp=0.04)
        tp, tm, flat, _, _ = light_time(shell, L=L, n=int(200 * L) + 1)
        print(f"   L = {L}: beta 0.04 delays +x {(tp-flat)/C*1e9:.3f} ns, -x {(tm-flat)/C*1e9:.3f} ns, difference {(tm-tp)/C*1e9:.3f} ns")
    s0 = build_shell(M, R1, R2, beta_warp=0.0)
    e2a = float(s0.lapse_static(0.0)) ** 2
    print(f"interior static lapse e^a = {math.sqrt(e2a):.4f}; interior forward light speed exceeds c only if"
          f" beta_warp > (1 - e^2a)/2 = {(1-e2a)/2:.4f}")
    # ADM momentum
    print(f"S(r >= R2) = {float(s0.S(np.array([20.0]))[0])}, so the exterior is exact Schwarzschild with zero shift:"
          f" K_ij = 0 there, P_ADM = 0 and M_ADM = {s0.M_ADM:.4e} kg independent of beta_warp")
    print(f"Andreasson/Buchdahl cap at R2 = 20 m: M < (8/9) R2 c^2/(2G) = {(8/9)*R2*C**2/(2*G):.4e} kg"
          f" = {(8/9)*R2*C**2/(2*G)/MJ:.3f} M_J (published shell at 2GM/(c^2 R2) = {2*G*M/(C**2*R2):.3f})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
