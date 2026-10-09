"""Falsifier C6-1, part 2: throat of real proper length L (tube S^2(a) x [0, L], ultrastatic
-dt^2 + dl^2 + a^2 dOmega^2) instead of a zero-length thin shell with a fixed delay.
Flat exterior, c = 1, d = 1, mouths radius a at A = 0, B = e, orientable gluing G = -R.

A ray hitting sphere A at outward normal n with exterior velocity v (cos i = -v.n) crosses
the tube in time L / cos i while sweeping angle phi = L tan i / a along the great circle
in its tangential direction t: exit point n' = cos(phi) n + sin(phi) t, tangent
t' = -sin(phi) n + cos(phi) t; it leaves B + a G n' with velocity cos(i) G n' + sin(i) G t'.

Realignment v_out = v is solved by Newton's method on the 2 tangent coordinates of n, from
the small-i guess (sweep the hit point from -v to -R^{-1} v).  For the realigned line the
asymptotic achronality margin is tau_eff - (Q0 - P0).v, tau_eff = L / cos i, P0 = A + a n,
Q0 = B + a G n'.  Negative margin is necessary for an achronal complete through-line, and in
the thin-shell model (part 1) the large-separation limit was the supremum of the margin.
The full pair check is not repeated here.
"""
import numpy as np

d = 1.0
e = np.array([1.0, 0, 0]); A = np.zeros(3); B = d * e


def rot(axis, ang):
    axis = np.asarray(axis, float); axis /= np.linalg.norm(axis)
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * K @ K


def outv(n, v, G, a, L):
    n = n / np.linalg.norm(n)
    cosi = -(v @ n)
    vt = v - (v @ n) * n
    sini = np.linalg.norm(vt)
    t = vt / sini if sini > 1e-15 else np.zeros(3)
    phi = L * sini / cosi / a
    n2 = np.cos(phi) * n + np.sin(phi) * t
    t2 = -np.sin(phi) * n + np.cos(phi) * t
    return cosi * (G @ n2) + sini * (G @ t2), L / cosi, A + a * n, B + a * (G @ n2), cosi


def solve(v, G, a, L, R):
    target = -np.linalg.inv(R) @ v           # small-i: exit point n' ~ G^{-1} v = -R^{-1} v
    m0 = -v
    ang = np.arccos(np.clip(m0 @ target, -1, 1))
    tdir = target - (target @ m0) * m0
    if np.linalg.norm(tdir) < 1e-9:           # target = m0 or antipodal: any tangent works
        tdir = np.cross(v, [0, 0, 1.0])
        if np.linalg.norm(tdir) < 1e-9:
            tdir = np.cross(v, [0, 1.0, 0])
    tdir /= np.linalg.norm(tdir)
    i0 = np.arctan(ang * a / L)
    n = -np.cos(i0) * v - np.sin(i0) * tdir   # so that v = -cos i n + sin i t with t = tdir
    for it in range(40):
        ref = np.array([0, 0, 1.0]) if abs(n[2]) < 0.9 else np.array([0, 1.0, 0])
        b1 = np.cross(n, ref); b1 /= np.linalg.norm(b1); b2 = np.cross(n, b1)
        F = outv(n, v, G, a, L)[0] - v
        if np.linalg.norm(F) < 1e-12:
            break
        h = 1e-7
        J = np.stack([(outv(n + h * b, v, G, a, L)[0] - v - F) / h for b in (b1, b2)], 1)
        step = np.linalg.lstsq(J, -F, rcond=None)[0]
        step = np.clip(step, -0.05, 0.05)
        n = n + step[0] * b1 + step[1] * b2
        n /= np.linalg.norm(n)
        if n @ v >= 0:
            break
    vo, tau, P0, Q0, cosi = outv(n, v, G, a, L)
    return np.linalg.norm(vo - v), tau, P0, Q0, cosi, n


L = 0.5
print("Tube throat: proper length L = %.2f d, flat exterior, c = 1, d = 1" % L, flush=True)
for a in (0.05, 0.01):
    for name, R in (("R = I (aligned)", np.eye(3)),
                    ("R = 10 deg about z (perp e)", rot([0, 0, 1], np.radians(10))),
                    ("R = 90 deg about z (perp e)", rot([0, 0, 1], np.pi / 2)),
                    ("R = 180 deg about z (perp e)", rot([0, 0, 1], np.pi)),
                    ("non-orientable translation gluing G = +I (R = -I, idealizer mirror)", -np.eye(3))):
        G = -R
        best = None
        for beta in np.radians([0, 2, 5, 10, 20]):
            v = np.array([np.cos(beta), 0, np.sin(beta)])
            res, tau, P0, Q0, cosi, n = solve(v, G, a, L, R)
            if res > 1e-9 or cosi <= 0 or (Q0 - B) @ v <= 0:
                continue
            marg = tau - (Q0 - P0) @ v
            if best is None or marg < best[0]:
                best = (marg, tau, cosi, np.degrees(beta), res)
        if best is None:
            print("a = %.2f d, %s: Newton found no realigned ray" % (a, name), flush=True)
        else:
            print("a = %.2f d, %s: realigned ray |v_out - v| = %.1e; tau_eff = %.4f d (cos i = %.4f), "
                  "v tilted %.0f deg from e; asymptotic margin = %+.4f d -> %s"
                  % (a, name, best[4], best[1], best[2], best[3], best[0],
                     "negative (achronal candidate)" if best[0] < 0 else "non-negative (chronal)"), flush=True)
