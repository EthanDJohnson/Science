#!/usr/bin/env python3
"""Falsifier C6-0: linearized-gravity time-advance test, with NO generic condition used.

Units: geometric (G = c = 1), lengths in metres, delays in metres of light-travel (divide by c for s).

Physics (stationary source, harmonic gauge, signature -+++):
  lap(hbar_ab) = -16 pi T_ab.  For null k = (1,0,0,1): h_ab k^a k^b = hbar_ab k^a k^b (trace term drops).
  Coordinate-time delay of a straight null ray at transverse position b: dt(b) = 1/2 int h_kk dz.
  Integrating the Poisson equation along z:  lap_perp dt(b) = -8 pi Sigma(b),  Sigma(b) = int T_kk dz.
  So dt = -4 int Sigma(b') ln|b-b'| d^2b' + harmonic.  Point mass check: dt = -4 M ln b  (Shapiro).
  If Sigma >= 0 (implied by NEC; only the ANEC-like line integral is needed) dt is superharmonic, so
  by the minimum principle no ray inside a disc beats every ray on the boundary circle: no advance.
  Nowhere is the generic condition (or null completeness, for delta-like sources) used.

Test model: counter-streaming thick shell (zero net momentum, the "positive-energy warp" current pattern):
  rho(r) Gaussian wall at R, momentum density j_z = kappa * rho * tanh(x/s), stresses 0.
  T_kk = rho - 2 j_z  (T_0z = -j_z).  NEC for this (rho, j, p=0) block: rho >= 2|j|  <=>  kappa <= 1/2.
We scan kappa and report whether any interior ray beats all rays on circles of radius 2R, 3R, 4R.
"""
import numpy as np

R, w, s = 10.0, 1.5, 2.0     # m: wall radius, wall half-width, current-reversal width
rho0 = 1e-6                  # m^-2 (geo); result is linear in rho0, sign question is scale-free
L, N = 120.0, 600            # transverse half-box (m), grid
x = np.linspace(-L, L, N); dx = x[1] - x[0]
X, Y = np.meshgrid(x, x, indexing="ij")
z = np.linspace(-3 * R, 3 * R, 801); dz = z[1] - z[0]

def column(Xg, Yg):
    """int rho dz for the Gaussian shell, done numerically on a coarse radial table."""
    bb = np.linspace(0, 3 * R, 400)
    col = np.array([np.trapezoid(rho0 * np.exp(-((np.sqrt(b * b + z * z) - R) ** 2) / (2 * w * w)), z) for b in bb])
    return np.interp(np.hypot(Xg, Yg), bb, col, right=0.0)

COL = column(X, Y)

def delay_map(Sigma):
    """dt = -4 * (Sigma conv ln|b|) via zero-padded FFT."""
    M = 2 * N
    kx = (np.arange(M) - M // 2) * dx
    KX, KY = np.meshgrid(kx, kx, indexing="ij")
    rr = np.hypot(KX, KY); rr[rr == 0] = dx / 2.718  # regularize log at origin (cell average approx)
    G = -4.0 * np.log(rr)
    Sp = np.zeros((M, M)); Sp[:N, :N] = Sigma
    conv = np.real(np.fft.ifft2(np.fft.fft2(Sp) * np.fft.fft2(np.fft.ifftshift(G)))) * dx * dx
    return conv[:N, :N]

# --- point-mass check against Shapiro dt = -4 M ln b + const
Sig_pt = np.zeros((N, N)); i0 = N // 2; Sig_pt[i0, i0] = 1.0 / dx ** 2  # M = 1 m
dpt = delay_map(Sig_pt)
for b in (10.0, 40.0):
    j = np.argmin(abs(x - (x[i0] + b)))
    print(f"point-mass check: dt(b={b:4.0f})-dt(b=5) = {dpt[j,i0]-dpt[np.argmin(abs(x-(x[i0]+5))),i0]:+.4f} m;"
          f" Shapiro -4 ln(b/5) = {-4*np.log(b/5):+.4f} m")

def ring_min(D, rad):
    th = np.linspace(0, 2 * np.pi, 720, endpoint=False)
    xi = rad * np.cos(th); yi = rad * np.sin(th)
    ii = np.clip(np.round((xi + L) / dx).astype(int), 0, N - 1)
    jj = np.clip(np.round((yi + L) / dx).astype(int), 0, N - 1)
    return D[ii, jj].min()

print("\nkappa  NEC(kappa<=1/2)  min Sigma (m^-1)   interior-min(|b|<1.5R) - ring-min  [2R, 3R, 4R] (m)  advance?")
for kappa in (0.0, 0.25, 0.45, 0.50, 0.55, 0.75, 1.0, 1.5, 2.0, 3.0):
    Sigma = COL * (1.0 - 2.0 * kappa * np.tanh(X / s))
    D = delay_map(Sigma)
    inner = D[np.hypot(X, Y) < 1.5 * R].min()
    gaps = [inner - ring_min(D, k * R) for k in (2, 3, 4)]
    adv = any(g < -1e-12 * abs(D).max() for g in gaps)
    print(f"{kappa:5.2f}  {'pass' if kappa <= 0.5 else 'FAIL':>5}   {Sigma.min():+.3e}   "
          + "  ".join(f"{g:+.3e}" for g in gaps) + f"   {'ADVANCE' if adv else 'none'}")
    ok = (not adv) if kappa <= 0.5 else True
    print(("PASS" if ok else "FAIL") + f" kappa={kappa}: NEC-satisfying => no advance (minimum principle)" if kappa <= 0.5 else f"INFO: kappa={kappa} NEC-violating, advance={adv}")

# Convergence: repeat kappa = 0.45 and 1.0 at 1.5x grid is costly; instead check grid-independence of the
# sign with a coarser grid (N=400) inline.
N2 = 400; x2 = np.linspace(-L, L, N2); dx2 = x2[1] - x2[0]
print("\n(coarse-grid sign check, N=400, ring 3R)")
X2, Y2 = np.meshgrid(x2, x2, indexing="ij")
COL2 = column(X2, Y2)
def delay_map2(Sigma):
    M = 2 * N2
    kx = (np.arange(M) - M // 2) * dx2
    KX, KY = np.meshgrid(kx, kx, indexing="ij")
    rr = np.hypot(KX, KY); rr[rr == 0] = dx2 / 2.718
    G = -4.0 * np.log(rr)
    Sp = np.zeros((M, M)); Sp[:N2, :N2] = Sigma
    return np.real(np.fft.ifft2(np.fft.fft2(Sp) * np.fft.fft2(np.fft.ifftshift(G))))[:N2, :N2] * dx2 * dx2
for kappa in (0.45, 1.0, 2.0):
    D = delay_map2(COL2 * (1.0 - 2.0 * kappa * np.tanh(X2 / s)))
    inner = D[np.hypot(X2, Y2) < 1.5 * R].min()
    th = np.linspace(0, 2 * np.pi, 720, endpoint=False)
    ii = np.clip(np.round((3 * R * np.cos(th) + L) / dx2).astype(int), 0, N2 - 1)
    jj = np.clip(np.round((3 * R * np.sin(th) + L) / dx2).astype(int), 0, N2 - 1)
    print(f"kappa={kappa:4.2f}: interior-min - ring(3R)-min = {inner - D[ii, jj].min():+.3e} m")
