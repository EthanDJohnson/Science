"""Falsifier C5-0 (part 2): scale-free cost of a Casimir mirror.

Dimensionless units: hbar = c = 1, gap a = 1, so energies per area are in
hbar c / a^3 (SI: multiply by hbar c / a^3).

Model (generous to the candidate):
 * Plates are plasma slabs of thickness y*a with eps(i xi) = 1 + x^2/xi^2,
   x = omega_p a / c. By the f-sum rule, eps(i xi) - 1 <= omega_p^2/xi^2 for any
   passive medium, so the lossless plasma is the MOST reflective medium at a
   given omega_p.
 * Lifshitz energy per area for two slabs, gap a:
     E/A = 1/(4 pi^2) Int_0^inf dq q Int_0^q dxi sum_p ln(1 - r_p^2 e^{-2q})
   slab r = r_inf (1 - e^{-2Ky}) / (1 - r_inf^2 e^{-2Ky}), K = sqrt(q^2 + x^2),
   r_TE,inf = (q-K)/(q+K), r_TM,inf = (eps q - K)/(eps q + K).
 * Plate energy: the charges giving omega_p must be electrons (lightest charge).
   For a degenerate gas, omega_p^2 = n e^2 c^2/(eps0 E_F) <= (4 alpha/3 pi) c^2 k_F^2
   in ALL regimes (E_F >= hbar c k_F), so k_F >= x / (0.0557 a).
   Energy density u >= (3/4) n hbar c k_F = hbar c k_F^4 / (4 pi^2)
   (kinetic only; ignores the rest mass of electrons and of the neutralizing ions).
 * Continuum validity: electrons spaced below the gap, k_F a >= 1, i.e. x >= 0.0557.
 * In an infinite stack there is one plate per gap, so ratio = u*y / |E/A|.
Self-check: ideal plates (r = 1) must give E/A = -pi^2/720 = -0.013708.
"""
import numpy as np
# scipy is not installed; use vectorised Gauss-Legendre (convergence checked below)

alpha = 1 / 137.035999
cpl = np.sqrt(4 * alpha / (3 * np.pi))   # omega_p <= cpl * c * k_F

def _nodes(n, lo, hi):
    t, w = np.polynomial.legendre.leggauss(n)
    return 0.5 * (hi - lo) * t + 0.5 * (hi + lo), 0.5 * (hi - lo) * w

def EA(x=None, y=None, ideal=False, nq=400, nt=200):
    # q in [0, 30] split in two panels to resolve small q; xi = q * t, t in [0, 1]
    q1, w1 = _nodes(nq // 2, 0.0, 3.0)
    q2, w2 = _nodes(nq // 2, 3.0, 30.0)
    q = np.concatenate([q1, q2]); wq = np.concatenate([w1, w2])
    if ideal:
        return np.sum(wq * q * q * 2 * np.log1p(-np.exp(-2 * q))) / (4 * np.pi ** 2)
    t, wt = _nodes(nt, 0.0, 1.0)
    Q = q[:, None]; XI = Q * t[None, :]
    eps = 1 + x * x / (XI * XI)
    K = np.sqrt(Q * Q + x * x)
    e = np.exp(-2 * K * y)
    s = 0.0
    for rinf in ((Q - K) / (Q + K), (eps * Q - K) / (eps * Q + K)):
        r = rinf * (1 - e) / (1 - rinf * rinf * e)
        s = s + np.log1p(-r * r * np.exp(-2 * Q))
    inner = np.sum(s * wt[None, :], axis=1) * q      # dxi = q dt
    return np.sum(wq * q * inner) / (4 * np.pi ** 2)

ideal = EA(ideal=True)
print(f"self-check ideal E/A = {ideal:.6f} hbar c/a^3 (exact {-np.pi**2/720:.6f})")
print(f"large-omega_p check x=200, y=5: E/E_ideal = {EA(200.0, 5.0)/ideal:.4f} (should approach 1)")
for (nq, nt) in [(200, 100), (400, 200), (800, 400)]:
    print(f"convergence x=0.1,y=0.3 nq={nq},nt={nt}: E/A = {EA(0.1, 0.3, nq=nq, nt=nt):.6e}")

def ratio(x, y):
    kF = x / cpl
    u = kF ** 4 / (4 * np.pi ** 2)
    E = EA(x, y)
    return u * y / abs(E), E

best = (np.inf, None)
print(" x=omega_p a/c   y=d/a   E/A (hbar c/a^3)  E/E_ideal   plate/deficit")
for x in [0.0557, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0]:
    for y in [0.03, 0.1, 0.3, 1.0, 3.0]:
        r, E = ratio(x, y)
        print(f" {x:8.4f}   {y:6.2f}   {E: .4e}      {E/ideal:.3e}   {r:.3e}")
        if r < best[0]:
            best = (r, (x, y))
print(f"minimum plate-energy/deficit on grid = {best[0]:.3e} at (x, y) = {best[1]}")
# refine near the minimum
x0, y0 = best[1]
for x in x0 * np.array([0.7, 1.0, 1.4]):
    if x < 0.0557:
        continue
    for y in y0 * np.array([0.5, 0.7, 1.0, 1.4, 2.0]):
        r, E = ratio(x, y)
        if r < best[0]:
            best = (r, (x, y))
print(f"refined minimum = {best[0]:.3e} at (x, y) = ({best[1][0]:.4f}, {best[1][1]:.3f})")
print("NOTE: the unconstrained minimum runs to y -> 0 (2D-sheet limit, E ~ sqrt(n_s)), where the")
print("plate has far fewer than one electron per a^2 and is no continuum mirror at scale a.")
print("Constrained scan: areal electron density n_s a^2 = (x/cpl)^3 y/(3 pi^2) >= 1")
cbest = (np.inf, None)
for x in [0.0557, 0.07, 0.1, 0.13, 0.17, 0.2, 0.3, 0.5, 0.7, 1.0, 2.0, 5.0]:
    ymin = 3 * np.pi ** 2 * cpl ** 3 / x ** 3
    row = []
    for y in ymin * np.array([1.0, 1.5, 2.0, 4.0]):
        if y > 60:
            continue
        r, E = ratio(x, y)
        row.append((r, y))
        if r < cbest[0]:
            cbest = (r, (x, y))
    rmin = min(row) if row else (np.nan, np.nan)
    print(f"  x = {x:6.4f}: y_min = {ymin:.3e}; best ratio {rmin[0]:.3e} at y = {rmin[1]:.3e}")
print(f"constrained minimum plate-energy/deficit = {cbest[0]:.3e} at (x, y) = "
      f"({cbest[1][0]:.4f}, {cbest[1][1]:.3e})")
print("Scale-free: holds for every gap a (the kinetic bound is exact in the ultra-relativistic "
      "limit and an under-estimate otherwise, where rest mass dominates).")
