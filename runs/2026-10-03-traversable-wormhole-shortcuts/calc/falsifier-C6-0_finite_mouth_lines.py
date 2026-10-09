"""Falsifier C6-0 (physics): do finite, smooth mouths restore a complete achronal
through-throat null line for MISALIGNED one-sided shortcuts?

Units: geometric, c = 1; lengths and times in units of the throat radius b0 (b0 = 1).

Model (static, so null geodesics = geodesics of the optical metric, arrival time = optical length):
  * Each mouth is an Ellis-type flare, optical metric dl^2 + (l^2 + b0^2) dOmega^2, asymptotically flat,
    optionally with a cylindrical throat segment of length L (r = b0) inserted at l = 0.
  * The two flares are embedded far apart (centres A, B, |B - A| = d >> b0) in one flat exterior; the
    side-2 frame is attached to B with an isometry M.  In the point-mouth language of M-IDEALIZER-01/02
    and M-DECOMPOSER-08 a radial ray entering A along n leaves B along O n with O = -M
    (O = I aligned, O = -I "mirror" = Visser natural identification, O = rotation = misaligned).
  * A through-ray with impact parameter b < b0 in a plane containing its direction e winds by
        dphi(b) = 2 (b/b0) K(b/b0)  [+ L b / (b0^2 sqrt(1 - b^2/b0^2)) on the cylinder]
    and leaves along  e_out = O R_plane(dphi) e.   (b = 0 recovers the point-mouth map e_out = O e.)
  * Its asymptotic transit-time excess (time minus projected distances to the mouth centres) is
        tau(b) = int_{-inf}^{inf} [ (1 - b^2/(l^2+b0^2))^{-1/2} - 1 ] dl  +  L / sqrt(1 - b^2/b0^2).
    tau(0) = L, the point-mouth centre-to-centre throat delay.
  * The exterior route between far points p = A + b_vec - S e and q = B + c_vec + S' e takes
    S + S' + e.D + O(1/S).  So a through-ray with e_out = e has asymptotic advance
        adv(e) = e.D - tau(b_req(e)),   b_req: dphi(b) = angle(e, O^{-1} e).
  * Limit-curve argument (Hawking & Ellis Lemma 6.2.1 / Beem-Ehrlich-Easley Thm 3.18 type): if
    max_e adv(e) > 0, the generators of dJ+(A - S e) reaching B + S e cross the throat and converge,
    as S -> inf, to an inextendible achronal null geodesic (a null line) through the throat.
"""
import numpy as np
from scipy.integrate import quad
from scipy.special import ellipk
from scipy.optimize import brentq

b0 = 1.0

def dphi(b, L=0.0):
    k = b / b0
    # scipy ellipk takes parameter m = k^2
    return 2.0 * k * ellipk(k * k) + L * b / (b0**2 * np.sqrt(1 - k * k))

def dphi_quad(b):
    f = lambda l: b / ((l * l + b0**2) * np.sqrt(1 - b * b / (l * l + b0**2)))
    return 2 * quad(f, 0, np.inf, limit=400)[0]

def tau(b, L=0.0):
    f = lambda l: 1.0 / np.sqrt(1 - b * b / (l * l + b0**2)) - 1.0
    return 2 * quad(f, 0, np.inf, limit=400)[0] + L / np.sqrt(1 - (b / b0)**2)

def b_for(theta, L=0.0):
    if theta <= 0:
        return 0.0
    return brentq(lambda b: dphi(b, L) - theta, 0.0, b0 * (1 - 1e-15), xtol=1e-14)

print("=== 1. Ellis through-ray: winding and transit excess (b0 = 1, geometric) ===")
for b in [0.0, 0.3, 0.6, 0.9]:
    dq = dphi_quad(b) if b > 0 else 0.0
    print(f"b = {b:.2f} b0: dphi = {dphi(b):.6f} rad (elliptic) vs {dq:.6f} rad (quadrature); tau = {tau(b):.6f} b0")
bpi = b_for(np.pi)
print(f"winding pi (needed for mirror gluing O = -I): b_pi = {bpi:.6f} b0, tau(b_pi) = {tau(bpi):.6f} b0  [L = 0]")

def rot(axis, ang):
    axis = np.asarray(axis, float) / np.linalg.norm(axis)
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * K @ K

def sphere_grid(n=4000):
    i = np.arange(n) + 0.5
    ph = np.arccos(1 - 2 * i / n)
    th = np.pi * (1 + 5**0.5) * i
    return np.stack([np.cos(th) * np.sin(ph), np.sin(th) * np.sin(ph), np.cos(ph)], 1)

E = sphere_grid()
Dhat = np.array([1.0, 0, 0])

def best_advance(O, L, d):
    Oinv = np.linalg.inv(O)
    best, arg = -np.inf, None
    for e in E:
        if e @ Dhat <= 0:
            continue
        c = np.clip(e @ (Oinv @ e), -1, 1)
        th = np.arccos(c)
        adv = d * (e @ Dhat) - tau(b_for(th, L), L)
        if adv > best:
            best, arg = adv, (e, th)
    return best, arg

def check_map(O, e, th, L):
    """Verify explicitly that the winding-th ray in the plane of (e, O^-1 e) leaves along e."""
    Oinv = np.linalg.inv(O)
    t = Oinv @ e
    if th < 1e-12:
        return np.linalg.norm(O @ e - e)
    if abs(th - np.pi) < 1e-9:
        nrm = np.cross(e, [0, 0, 1.0]) if abs(e[2]) < 0.9 else np.cross(e, [0, 1.0, 0])
    else:
        nrm = np.cross(e, t)
    nrm /= np.linalg.norm(nrm)
    eout = O @ (rot(nrm, th) @ e)
    return np.linalg.norm(eout - e)

print()
print("=== 2. Point-mouth counterexamples of M-DECOMPOSER-08 / M-IDEALIZER-02, re-done with finite mouths ===")
cases = [("rotated 10 deg about z (perp D)", rot([0, 0, 1], np.radians(10))),
         ("rotated 180 deg about z (perp D)", rot([0, 0, 1], np.pi)),
         ("mirror O = -I (Visser natural identification)", -np.eye(3)),
         ("aligned O = I", np.eye(3))]
for d in [20.0, 100.0, 1000.0]:
    for Lfrac in [0.0, 0.5, 0.9]:
        L = Lfrac * d
        for name, O in cases:
            adv, (e, th) = best_advance(O, L, d)
            err = check_map(O, e, th, L)
            print(f"d = {d:6.0f} b0, L = {Lfrac:.1f} d, {name:46s}: T_thru/T_ext(radial) = {L/d:.2f}; "
                  f"best advance of a through-line = {adv:+.4f} b0 at e.Dhat = {e@Dhat:.4f}, winding {np.degrees(th):6.1f} deg "
                  f"(|e_out - e| = {err:.1e}) -> {'ACHRONAL LINE EXISTS' if adv > 0 else 'no line'}")

print()
print("=== 3. Residual window: worst-case (winding pi) delay penalty delta(L) = tau(b_pi; L) - L ===")
print("A misaligned shortcut escapes the line argument only if d - L < delta (any orientation needs winding <= pi).")
for L in [0.0, 1.0, 3.0, 10.0, 30.0, 100.0, 1000.0, 1e4]:
    bp = b_for(np.pi, L)
    delta = tau(bp, L) - L
    approx = np.pi**2 * b0**2 / (2 * L) if L > 0 else float('nan')
    print(f"L = {L:8.1f} b0: b_pi = {bp:.5f} b0, delta = {delta:.5f} b0  (long-throat estimate pi^2 b0^2/(2L) = {approx:.5f} b0)")

print()
print("=== 4. Scale of the window against the mouth-size ambiguity of 'shortcut' ===")
dl0 = tau(b_for(np.pi, 0.0), 0.0)
print(f"thin (L = 0) Ellis mouths: delta = {dl0:.4f} b0; facing-surface vs centre exterior separation differs by 2 b0 = 2.0000 b0")
print(f"ratio delta / (2 b0) = {dl0/2:.4f}")
for d_m, b0_m, lab in [(9.46e15, 1.5e7, "MM-like r_e = 1.5e7 m, d = 1 ly"), (1.0e3, 1.0, "b0 = 1 m, d = 1 km")]:
    print(f"{lab}: worst-case escape window (L -> 0) = {dl0*b0_m:.3e} m of {d_m:.3e} m, fraction {dl0*b0_m/d_m:.2e}")

print()
print("=== 5. Null energy on the restored line (Ellis source, geometric units, E = 1) ===")
# Ellis orthonormal Einstein tensor (cf. M-IDEALIZER-04/05): 8*pi*rho = -b0^2/r^4, 8*pi*p_l = -b0^2/r^4,
# 8*pi*p_t = +b0^2/r^4, r^2 = l^2 + b0^2.  For k = E(e_t + cos(psi) e_l + sin(psi) e_perp):
#   G_kk = E^2 (b0^2/r^4)(-1 - cos^2 psi + sin^2 psi) = -2 E^2 b0^2 cos^2(psi) / r^4  (<= 0).
# Affine parameter: dl/dlambda = E cos(psi), cos(psi) = sqrt(1 - b^2/r^2).
def anec_G(b):
    f = lambda l: -2 * b0**2 * np.sqrt(1 - b * b / (l * l + b0**2)) / (l * l + b0**2)**2
    return 2 * quad(f, 0, np.inf, limit=400)[0]
for b in [0.0, bpi]:
    I = anec_G(b)
    print(f"b = {b:.5f} b0: integral G_kk dlambda = {I:.6f} /b0 ; ANEC = integral T_kk dlambda = {I/(8*np.pi):.6f} /b0 (negative)")
print("radial check: -E/(8 b0) from M-IDEALIZER-05 =", -1/8)
