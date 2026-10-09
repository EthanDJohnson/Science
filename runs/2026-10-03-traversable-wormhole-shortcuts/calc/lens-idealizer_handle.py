"""Idealized one-sided wormhole: a 'handle' joining two small mouths in flat space.

Model (all idealizations stated):
  * Flat (Minkowski) exterior, c = 1, lengths in metres (geometric units; time in metres of light travel).
  * Mouth A at origin, mouth B at vector D (|D| = d). Mouth radius a -> 0 (point mouths) except where noted.
  * The throat is a tube of proper length L; light crosses it in time L (static, no redshift inside).
  * The gluing maps an incoming direction n_in at A to an outgoing direction n_out = O n_in at B,
    with O an orthogonal 3x3 matrix (proper rotation, or improper e.g. the mirror gluing O = -I).
  * Static mouths, clocks synchronised through the flat exterior (Einstein synchronisation).
  * A complete radial null geodesic gamma: comes in from infinity along -n_in, enters A, crosses the
    throat, leaves B along n_out to infinity.

Questions answered:
  (1) Shortcut test: T_thru = L vs T_ext = d (observers at the mouths). Ratio L/d.
  (2) Is gamma achronal?  gamma is chronal iff some pair p (before A), q (after B) on it can be joined by a
      causal route strictly faster than gamma's own elapsed time (exterior straight line, or the throat
      crossed in the other direction).  Sampled numerically over x, y in [0, X].
  (3) Closed-form expectation: achronal  <=>  O n = n (aligned gluing)  and  L <= D . n.
  (4) Time-machine threshold: with a time shift Delta between mouth clocks (identification t_B = t_A - Delta),
      a closed causal loop (throat A->B, exterior B->A) exists iff Delta >= d + L.
"""
import numpy as np

rng = np.random.default_rng(1)


def rot(axis, ang):
    axis = np.asarray(axis, float)
    axis /= np.linalg.norm(axis)
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * K @ K


def chronal(D, L, O, n_in, X=200.0, N=400):
    """Return (is_chronal, worst_margin). margin = gamma_time - fastest_alternative (>0 means chronal)."""
    n_in = n_in / np.linalg.norm(n_in)
    n_out = O @ n_in
    xs = np.concatenate([np.linspace(0, 5 * np.linalg.norm(D) + 5 * L + 1, N // 2), np.geomspace(1, X * (np.linalg.norm(D) + L + 1), N // 2)])
    A = np.zeros(3)
    B = np.asarray(D, float)
    worst = -np.inf
    for x in xs:
        p = A - x * n_in
        q = B + xs[:, None] * n_out[None, :]
        t_gamma = x + L + xs
        ext = np.linalg.norm(q - p[None, :], axis=1)
        # reverse crossing: p -> B (exterior), through throat B->A, A -> q (exterior)
        rev = np.linalg.norm(B - p) + L + np.linalg.norm(q - A[None, :], axis=1)
        alt = np.minimum(ext, rev)
        m = np.max(t_gamma - alt)
        worst = max(worst, m)
    return worst > 1e-9 * (np.linalg.norm(D) + L + 1), worst


d = 1.0
D = np.array([d, 0, 0])
print("=== (1)+(2) Aligned gluing O = I, ray along +D (n_in = D_hat) ===")
print(" L/d   shortcut(T_thru<T_ext)   gamma chronal?   worst margin (m, units of d=1 m)")
for Lr in [0.0, 0.5, 0.9, 0.99, 1.01, 1.5, 3.0, 10.0]:
    c, w = chronal(D, Lr * d, np.eye(3), np.array([1.0, 0, 0]))
    print(f" {Lr:5.2f}   {str(Lr < 1):5s}                    {str(c):5s}            {w:+.4f}")

print("\n=== Aligned gluing, ray direction at angle psi to D: achronal iff L <= d cos(psi) ===")
for psi_deg in [0, 30, 60, 89, 120]:
    psi = np.radians(psi_deg)
    n = np.array([np.cos(psi), np.sin(psi), 0])
    for Lr in [0.3, 0.7]:
        c, w = chronal(D, Lr * d, np.eye(3), n)
        pred = not (Lr <= np.cos(psi) + 1e-12)
        print(f" psi={psi_deg:3d} deg  L/d={Lr:.1f}  d cos(psi)={np.cos(psi):+.3f}  chronal={c}  predicted chronal={pred}  margin={w:+.4f}")

print("\n=== Mirror gluing O = -I (standard Visser cut-and-paste orientation), L = 0 (thin shell, maximal shortcut) ===")
for psi_deg in [0, 45, 90, 180]:
    psi = np.radians(psi_deg)
    n = np.array([np.cos(psi), np.sin(psi), 0])
    c, w = chronal(D, 0.0, -np.eye(3), n)
    print(f" ray angle {psi_deg:3d} deg: chronal={c}, margin={w:+.3f} m")

print("\n=== Rotated gluing O = R(axis, angle): only rays along the rotation axis can be achronal ===")
for ax, ang in [([0, 0, 1], np.radians(40)), ([1, 0, 0], np.radians(40)), ([0, 1, 0], np.radians(170))]:
    O = rot(ax, ang)
    axis = np.asarray(ax, float)
    res = []
    for trial in range(200):
        n = rng.normal(size=3)
        n /= np.linalg.norm(n)
        c, _ = chronal(D, 0.2 * d, O, n, N=120)
        res.append(c)
    c_ax, w_ax = chronal(D, 0.2 * d, O, axis)
    c_ax2, w_ax2 = chronal(D, 0.2 * d, O, -axis)
    print(f" axis={ax}, angle={np.degrees(ang):.0f} deg, L/d=0.2: random rays achronal: {200 - sum(res)}/200; "
          f"along +axis chronal={c_ax} (D.n={axis @ D:+.2f}); along -axis chronal={c_ax2} (D.n={-axis @ D:+.2f})")

print("\n=== Finite mouth radius a: exterior route must avoid mouths; straight line is a lower bound.")
print(" With a > 0 the facing-observer exterior time is d - 2a while gamma's far-field threshold stays ~ D.n;")
print(" e.g. a/d = 0.1: shortcut for facing observers iff L < 0.8 d; achronal aligned ray iff L <~ d (+O(a)).")

print("\n=== (4) Time-machine threshold: closed loop time = d + L - Delta ===")
for name, L_ly, d_ly in [("thin-shell shortcut", 0.0, 10.0), ("short throat", 1.0, 10.0),
                         ("MM-like long throat (Q-06: pi*ell ~ 9.4e3 ly)", 9.4e3, 1.0e3)]:
    print(f" {name}: d = {d_ly} ly, L = {L_ly} ly -> CTC iff Delta >= {d_ly + L_ly:.4g} yr")
# twin-paradox time shift for mouth moved out and back at speed v over exterior time T: Delta = T (1 - 1/gamma)
for v in [0.1, 0.5, 0.9, 0.99]:
    g = 1 / np.sqrt(1 - v * v)
    print(f"  mouth trip at v = {v}c: Delta/T = {1 - 1 / g:.4f}; T needed for MM-like Delta = 1.04e4 yr: {1.04e4 / (1 - 1 / g):.3g} yr")
