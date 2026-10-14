"""Falsifier C2-1 (evidence angle): two side checks on the C2 null.

(A) Linear-in-h pair creation (Chakraborty et al. 2024, eq. 38, support delta(k'^2)):
    for a massless pair (k, p) whose total momentum q = k + p is null, k and p must be
    collinear with q, and a transverse-traceless eps(q) then kills the minimal-scalar vertex
    eps_mn T^mn(k,p).  Numerical check with random TT tensors.

(B) Cross-fusion of a far-zone wave with an isotropic stochastic GW background (SGWB):
    a GW150914 graviton (f = 150 Hz) meeting background gravitons along 410 Mpc.
    Sustained, R-linear, but tiny.  Uses qft_second_order.beams_pair_rate_SI (tree level,
    plane waves, in-in mean number), isotropic average of the angle.
Units: (A) natural, dimensionless components; (B) SI.
"""
import sys, math
import numpy as np
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import qft_second_order as q2

rng = np.random.default_rng(1)
eta = np.diag([1.0, -1.0, -1.0, -1.0])

def tt_pol(n):
    # random linear combo of plus/cross TT tensors for propagation direction n (lower spatial indices)
    a = np.cross(n, [0.3, 0.5, 0.8]); a /= np.linalg.norm(a)
    b = np.cross(n, a)
    e = np.zeros((4, 4))
    c1, c2 = rng.normal(size=2)
    sp = (np.outer(a, a) - np.outer(b, b)) * c1 + (np.outer(a, b) + np.outer(b, a)) * c2
    e[1:, 1:] = sp
    return e

print("(A) linear-in-h vertex for null total momentum")
worst = 0.0
for trial in range(5):
    n = rng.normal(size=3); n /= np.linalg.norm(n)
    w1, w2 = rng.uniform(0.2, 2.0, size=2)
    k = np.concatenate([[w1], w1 * n]); p = np.concatenate([[w2], w2 * n])  # collinear: q null
    qv = k + p
    q2norm = qv @ eta @ qv
    # minimal massless scalar: T^mn = k^m p^n + p^m k^n - eta^mn (k.p)
    kp = k @ eta @ p
    T = np.outer(k, p) + np.outer(p, k) - np.linalg.inv(eta) * kp
    e = tt_pol(n)
    amp = np.sum(e * T)
    worst = max(worst, abs(amp))
    print(f"  trial {trial}: q^2 = {q2norm:.2e}, k.p = {kp:.2e}, eps_mn T^mn = {amp:.2e}")
print(f"  max |vertex| over trials = {worst:.2e} (zero: null q forces collinear pair, TT kills it)")
# contrast: non-collinear pair, q timelike
n2 = rng.normal(size=3); n2 /= np.linalg.norm(n2)
k = np.concatenate([[1.0], n]); p = np.concatenate([[1.0], n2])
print(f"  non-collinear control: q^2 = {(k+p)@eta@(k+p):.3f} > 0 (needs time-like Fourier support of h)")

print()
print("(B) cross-fusion of a 150 Hz wave with an isotropic SGWB, SI")
rho_c = 7.7e-10  # J/m^3, critical energy density c^2 rho_c for h0 ~ 0.68 (SI)
w1 = 2 * math.pi * 150.0
t_prop = 410 * 3.0857e22 / 2.998e8  # s, 410 Mpc light travel time (no cosmology)
for label, f2, Omega in [("LVK-band SGWB at 25 Hz, Omega = 1e-8 (near LVK O3 bound)", 25.0, 1e-8),
                         ("PTA SGWB at 3.2e-8 Hz, Omega = 1e-8", 3.2e-8, 1e-8)]:
    w2 = 2 * math.pi * f2
    ref = q2.beams_pair_rate_SI(w2, 1e-21, math.pi / 2)
    rho_ref = ref["rho1_SI"]
    h2 = 1e-21 * math.sqrt(Omega * rho_c / rho_ref)
    # isotropic average over angle: sample cos theta uniformly
    cs = np.linspace(-0.999, 0.999, 401)
    gam = []
    for c in cs:
        th = math.acos(c)
        r = q2.beams_pair_rate_SI(w1, 1e-21, th, omega2_rad_s=w2, h2=h2)
        gam.append(r["pair_rate_SI"] / r["n1_SI"])  # pairs per wave graviton per s
    Gam = float(np.trapezoid(gam, cs) / 2.0) if hasattr(np, "trapezoid") else float(np.trapz(gam, cs) / 2.0)
    print(f"  {label}: h2 = {h2:.2e}, Gamma per 150 Hz graviton = {Gam:.2e} s^-1,"
          f" fraction fused over 410 Mpc = {Gam * t_prop:.2e}")
print(f"  (t_prop = {t_prop:.2e} s; this channel is R-linear but needs a second, non-collinear GW field;"
      " it is C6's multi-directional case, not self-decay)")
