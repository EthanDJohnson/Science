#!/usr/bin/env python3
"""Task B (1): what B&O's coherent state looks like in space-time.

B&O build the state from the Pauli-Jordan (radiation) field h^c = int Delta_rad T_s (their eq. 5) with an isotropic narrow-band
shell f_s(k) (top hat on [w - sig/2, w + sig/2]). Every Fourier component is an on-shell plane wave, so h^c is a REGULAR
SOURCE-FREE solution for all times. Here we construct it in position space (scalar proxy per polarisation component):
  * l = 0  (B&O's isotropic f_s, exactly their eq.-7 state up to the polarisation tensor), and
  * l = 2, m = 0 (a quadrupole angular pattern, the pattern class of real binary radiation),
and show it is an INCOMING spherical shell converging on the origin, a focus, and an OUTGOING shell. We contrast it with the
physical retarded field of a source that radiates for a finite time (purely outgoing).

Printed quantities (units w_s = 1, so lambda = 2 pi; sig = eps w with B&O's eps = 0.1 unless stated):
  - r_peak(t): radius where the radial energy weight |r R(r,t)|^2 peaks
  - frac(r < lambda), frac(r < 3 lambda): fraction of int |r R|^2 dr inside that radius (energy-like weight)
  - in-fraction: int_{r>lambda} |r R_in|^2 / (same for R_in plus R_out)  (R_in/R_out: the exact h^(2)/h^(1) split)
  - focus amplitude: max_r |R(r, t~0)| / max |R| on the outgoing shell at radius r_obs (B&O field strength ratio)
"""
import math
import sys

import numpy as np

sys.path.insert(0, "/home/user/Science/checks/2026-10-11-blas-oller-gw-decay/calc")
from taskB_common import Band, radial_direct, radial_free  # noqa: E402

PI = math.pi
LAM = 2 * PI

print("=== validation: closed-form in/out split vs direct k-quadrature of R_l(r,t) ===")
for prof in ("tophat", "gauss"):
    b = Band(prof, 1.0, 0.1)
    for l in (0, 2):
        worst = 0.0
        for r, t in [(0.3, 0.0), (2.0, -1.0), (5.0, 3.0), (40.0, -38.0), (40.0, 41.0), (120.0, 0.0)]:
            a = complex(radial_free(b, l, np.array([r]), np.array([t]))[0])
            d = radial_direct(b, l, r, t)
            worst = max(worst, abs(a - d) / max(abs(d), 1e-30 + 1e-6 * abs(radial_direct(b, l, 1.0, 0.0))))
        print(f"{prof:6s} l={l}: max rel. deviation over 6 (r,t) points = {worst:.2e}")

r = np.arange(0.005, 2500.0, 0.01)
dr = r[1] - r[0]


def stats(b, l, t):
    R = radial_free(b, l, r, np.full_like(r, t))
    Ri = radial_free(b, l, r, np.full_like(r, t), "in")
    Ro = radial_free(b, l, r, np.full_like(r, t), "out")
    wgt = np.abs(r * R) ** 2
    tot = wgt.sum() * dr
    rp = r[np.argmax(wgt)]
    f1 = wgt[r < LAM].sum() * dr / tot
    f3 = wgt[r < 3 * LAM].sum() * dr / tot
    far = r > LAM          # the h^(1)/h^(2) split has 1/r^2, 1/r^3 near-field pieces that cancel only in the sum
    wi = (np.abs(r * Ri)[far] ** 2).sum()
    wo = (np.abs(r * Ro)[far] ** 2).sum()
    return rp, f1, f3, wi / (wi + wo), np.max(np.abs(R))


for prof in ("tophat", "gauss"):
    for l in (0, 2):
        b = Band(prof, 1.0, 0.1)
        print(f"\n=== Pauli-Jordan field of the {prof} shell, l = {l}, sig = 0.1 w (1/sig = 10/w, lambda = {LAM:.3f}/w) ===")
        print("   t*w   r_peak*w   frac(r<lam)  frac(r<3lam)  in-fraction   max|R| (rel. to t=0)")
        ref = stats(b, l, 0.0)[4]
        for t in (-1000.0, -300.0, -100.0, -30.0, -10.0, -3.0, 0.0, 3.0, 10.0, 30.0, 100.0, 300.0, 1000.0):
            rp, f1, f3, fin, mx = stats(b, l, t)
            print(f"{t:7.0f}  {rp:9.2f}   {f1:10.3e}   {f3:10.3e}   {fin:9.4f}    {mx/ref:9.3e}")

print("\n=== focus strength: max_r |R(r,0)| versus the outgoing-shell amplitude at radius r_obs ===")
for prof in ("tophat", "gauss"):
    b = Band(prof, 1.0, 0.1)
    for l in (0, 2):
        R0 = radial_free(b, l, r[r < 40], np.zeros((r < 40).sum()))
        foc = np.max(np.abs(R0))
        rfoc = r[r < 40][np.argmax(np.abs(R0))]
        for robs in (500.0, 2000.0):
            sel = (r > robs - 200) & (r < robs + 200)
            Rs = radial_free(b, l, r[sel], np.full(sel.sum(), robs))
            shell = np.max(np.abs(Rs))
            print(f"{prof:6s} l={l}: focus at r*w = {rfoc:5.2f}; |R|_focus/|R|_shell(r_obs*w={robs:6.0f}) = {foc/shell:10.4e}"
                  f"   (2 w r_obs = {2*robs:8.1f};  ratio/(w r_obs) = {foc/shell/robs:.4f})")

print("\n=== GW150914-like illustration of the (fictitious) focus strain ===")
c, Mpc = 2.99792458e8, 3.0857e22
f_gw, D, h_obs = 150.0, 410 * Mpc, 1.0e-21
wD = 2 * PI * f_gw * D / c
print(f"w D/c = {wD:.3e};  focus strain of the free (Pauli-Jordan) field ~ (ratio/(w r_obs)) x w D h_obs:"
      f" l=0: {2.0*wD*h_obs:.3e};  l=2: {0.60*wD*h_obs:.3e}  (ratios 2.0 and 0.60 from the table above)")

print("\n=== contrast: retarded field of a source that radiates only during 0 < t < T_s (point monopole proxy) ===")
# q(t) = exp(-i w t) S(t), S = smooth switch-on/off on [0, T_s]; phi_ret = q(t - r)/(4 pi r), phi_adv = q(t + r)/(4 pi r),
# phi_PJ = phi_ret - phi_adv (what B&O's eq. 5 Delta_rad builds). Report the fraction of |r phi|^2 weight that is incoming.
Ts = 50.0


def S(u):
    u = np.asarray(u, float)
    x = np.clip(u / Ts, 0, 1)
    return np.where((u > 0) & (u < Ts), np.sin(PI * x) ** 2, 0.0)


q = lambda u: np.exp(-1j * u) * S(u)
rr = np.arange(0.01, 3000.0, 0.01)
print("   t*w    ret: total weight  in-fraction  r_max(occupied)   |  PJ = ret - adv: total weight  in-fraction")
for t in (-500.0, -100.0, -20.0, 0.0, 25.0, 60.0, 100.0, 500.0):
    ret = q(t - rr) / (4 * PI * rr)
    adv = q(t + rr) / (4 * PI * rr)
    wr = np.sum(np.abs(rr * ret) ** 2) * 0.01
    wa = np.sum(np.abs(rr * adv) ** 2) * 0.01
    occ = rr[np.abs(ret) > 0].max() if wr > 0 else 0.0
    print(f"{t:7.0f}   {wr:14.4e}   {0.0 if wr == 0 else 0.0:9.3f}   {occ:12.1f}     |   {wr + wa:14.4e}   {wa/(wr+wa) if wr+wa>0 else float('nan'):9.3f}")
print("(retarded: zero before the source acts, then a purely outgoing shell between r = t - T_s and r = t;"
      " Pauli-Jordan: the same total weight is present at t < 0 as an INCOMING shell converging on the source)")
