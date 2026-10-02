#!/usr/bin/env python3
"""Constraints lens: Natario zero-expansion drive and a smooth zero-vorticity (Lentz /
Fell-Heisenberg / Rodal class) drive, energy conditions for ALL observers and slice energy.

Geometric units G = c = 1, lengths in m. Unit lapse, flat slices:
  ds^2 = -dt^2 + sum_i (dx^i - X^i dt)^2   (Natario's sign; from_adm shift b = -X)
Bubble centre at z = v t, zeta = z - v t, r = |(x, y, zeta)|, f = Alcubierre tanh top hat
(Delta = 2/sigma wall convention, D-28).
  NAT: X = v curl( (f/2) (-y, x, 0) ) = v[(f + r f'/2) zhat - (f'/2)(zeta/r) rvec]  (div X = 0)
  IRR: X = v grad( zeta f ) = v[f zhat + zeta f'(r) rvec / r]                    (curl X = 0)
Both: X = v zhat inside (flat, comoving payload region), 0 outside.

1. All-observer NEC/WEC/SEC/DEC + Hawking-Ellis type over the whole wall with the finite-
   difference tool numeric_stress_energy.py (4th order, step-halving noise floor).
2. Eulerian density from the Natario formula rho = (theta^2 - K_ij K^ij)/16pi (D-01) with
   dX by centred differences of the analytic X, cross-checked against the tool at wall points.
3. Slice energy E = int rho d^3x by axisymmetric 2D quadrature, n vs 1.5 n.
4. Divergence identity: for ANY localized shift, theta^2 - d_iX_j d_jX_i is a total
   divergence, so for curl-free X (K_ij K^ij = d_iX_j d_jX_i) the Eulerian total is exactly 0:
   E+ = -E-. Checked numerically for IRR.
5. (not implemented)
"""
import math
import sys
import time

import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
from numeric_stress_energy import NumericSpacetime  # noqa: E402
from gr_tensors import to_si  # noqa: E402

MSUN, MJ = 1.989e30, 1.898e27


def top(r, R, s):
    T = math.tanh(s * R)
    f = (np.tanh(s * (r + R)) - np.tanh(s * (r - R))) / (2 * T)
    fp = s * (1 / np.cosh(s * (r + R)) ** 2 - 1 / np.cosh(s * (r - R)) ** 2) / (2 * T)
    return f, fp


def X_field(kind, v, R, s, t, x, y, z):
    zeta = z - v * t
    r = np.sqrt(x * x + y * y + zeta * zeta)
    rs = np.where(r > 0, r, 1e-300)
    f, fp = top(r, R, s)
    if kind == "NAT":
        a = f + r * fp / 2
        c = (fp / 2) * zeta / rs
        return v * (-c * x), v * (-c * y), v * (a - c * zeta)
    c = zeta * fp / rs
    return v * c * x, v * c * y, v * (f + c * zeta)


def metric_factory(kind, v, R, s):
    def g(t, x, y, z):
        X = X_field(kind, v, R, s, t, x, y, z)
        b = [-X[0], -X[1], -X[2]]
        b2 = b[0] ** 2 + b[1] ** 2 + b[2] ** 2
        one = np.ones_like(b2)
        zero = np.zeros_like(b2)
        return [[-1 + b2, b[0], b[1], b[2]],
                [b[0], one, zero, zero],
                [b[1], zero, one, zero],
                [b[2], zero, zero, one]]
    return g


def rho_natario(kind, v, R, s, x, y, z, eps):
    """Eulerian rho = (theta^2 - K_ij K^ij)/16 pi from centred differences of the analytic X."""
    J = np.zeros((3, 3) + np.shape(x))
    base = [x, y, z]
    for j in range(3):
        p = [b.copy() for b in base]
        m = [b.copy() for b in base]
        p[j] = p[j] + eps
        m[j] = m[j] - eps
        Xp = X_field(kind, v, R, s, 0.0, *p)
        Xm = X_field(kind, v, R, s, 0.0, *m)
        for i in range(3):
            J[i, j] = (Xp[i] - Xm[i]) / (2 * eps)      # d_j X_i
    K = 0.5 * (J + np.swapaxes(J, 0, 1))
    theta = J[0, 0] + J[1, 1] + J[2, 2]
    KK = np.einsum("ij...,ij...->...", K, K)
    JJt = np.einsum("ij...,ji...->...", J, J)
    return (theta ** 2 - KK) / (16 * math.pi), (theta ** 2 - JJt) / (16 * math.pi), theta


def slice_energy(kind, v, R, s, n_r, n_th):
    rmax = R + 12.0 / s
    dr = rmax / n_r
    rr = (np.arange(n_r) + 0.5) * dr
    dth = math.pi / n_th
    th = (np.arange(n_th) + 0.5) * dth
    RR, TT = np.meshgrid(rr, th, indexing="ij")
    x, y, z = RR * np.sin(TT), np.zeros_like(RR), RR * np.cos(TT)
    rho, div_form, theta = rho_natario(kind, v, R, s, x, y, z, eps=min(1e-3, 0.002 / s))
    w = 2 * math.pi * RR ** 2 * np.sin(TT) * dr * dth
    I = rho * w
    return dict(total=float(I.sum()), neg=float(I[I < 0].sum()), pos=float(I[I > 0].sum()),
                div_total=float((div_form * w).sum()), theta_max=float(np.abs(theta).max()),
                rho_min=float(rho.min()), rho_max=float(rho.max()))


def wall_points(R, s, nr=12, nth=13):
    rr = np.linspace(R - 3.0 / s, R + 3.0 / s, nr)
    th = np.linspace(0.03, math.pi - 0.03, nth)
    pts = []
    for phi in (0.0, 0.7):
        for a in rr:
            for b in th:
                pts.append((0.0, a * math.sin(b) * math.cos(phi), a * math.sin(b) * math.sin(phi), a * math.cos(b)))
    return np.array(pts)


def kg(e):
    return to_si.mass_kg(e)


def main():
    cases = [("paper-like R = 1 m, sigma = 8 /m (Delta = 0.25 m), v = 1", 1.0, 8.0, 1.0),
             ("reference R = 100 m, sigma = 2 /m (Delta = 1 m), v = 10", 100.0, 2.0, 10.0)]
    for kind in ("NAT", "IRR"):
        print(f"===== {kind} =====")
        for label, R, s, v in cases:
            t0 = time.time()
            st = NumericSpacetime(metric_factory(kind, v, R, s), h=0.01 / s)
            pts = wall_points(R, s)
            sc = st.scan_energy_conditions(pts)
            print(f" {label}: {sc['points']} wall points, unconverged {sc['unconverged']}, skipped {sc['skipped']}")
            print(f"   robust violations {sc['violations']}; strict {sc['violations_strict']}; types {sc['types']}")
            print(f"   worst nec_min {sc['worst']['nec_min'][0]:.4e} 1/m^2 at {sc['worst']['nec_min'][1]};"
                  f" wec_min {sc['worst']['wec_min'][0]:.4e}; most negative Eulerian rho {sc['worst']['rho_eulerian'][0]:.4e} 1/m^2"
                  f"  [{time.time()-t0:.1f}s]")
            # cross-check the closed-form Eulerian density against the FD tool at 6 wall points
            sub = pts[::60][:6]
            tool = st.eulerian_density(sub)["rho"]
            mine = rho_natario(kind, v, R, s, sub[:, 1], sub[:, 2], sub[:, 3], eps=min(1e-3, 0.002 / s))[0]
            print("   Eulerian rho cross-check tool vs (theta^2-K^2)/16pi:",
                  "; ".join(f"{a:.5e}/{b:.5e}" for a, b in zip(tool, mine)))
            # Eulerian sign census over the wall points
            rho_w = rho_natario(kind, v, R, s, pts[:, 1], pts[:, 2], pts[:, 3], eps=min(1e-3, 0.002 / s))[0]
            print(f"   Eulerian rho on wall points: min {rho_w.min():.4e}, max {rho_w.max():.4e} 1/m^2;"
                  f" negative at {(rho_w < -1e-12*np.abs(rho_w).max()).sum()}/{len(rho_w)}")
            # slice energy, convergence
            n_r = 3000 if R > 10 else 400
            res = []
            for nr, nt in ((n_r, 160), (int(1.5 * n_r), 240)):
                e = slice_energy(kind, v, R, s, nr, nt)
                res.append(e)
                print(f"   E (n_r={nr}, n_th={nt}): total {e['total']:.6e} m = {to_si.energy_joules(e['total']):.4e} J"
                      f" = {kg(e['total']):.4e} kg = {kg(e['total'])/MSUN:.4e} Msun; E- {e['neg']:.6e} m = {kg(e['neg']):.4e} kg"
                      f" = {kg(e['neg'])/MSUN:.4e} Msun; E+ {e['pos']:.6e} m = {kg(e['pos']):.4e} kg;"
                      f" divergence-form total {e['div_total']:.4e} m; max|theta| {e['theta_max']:.3e}")
            d = abs(res[1]['total'] - res[0]['total']) / max(abs(res[1]['neg']), 1e-300)
            print(f"   convergence |dE|/|E-| = {d:.2e}; E_total/|E-| = {res[1]['total']/abs(res[1]['neg']):.3e}")
            if kind == "NAT":
                Delta = 2.0 / s
                print(f"   fit check: E/(v^2 R^4/Delta^3) = {res[1]['total']/(v*v*R**4/Delta**3):.5f}"
                      f" (dossier D-34 fit -0.0445 for its convention)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
