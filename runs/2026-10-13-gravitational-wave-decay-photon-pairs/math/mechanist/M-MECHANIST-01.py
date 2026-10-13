"""M-MECHANIST-01: g g -> gamma gamma helicity amplitudes (natural units, hbar = c = 1).

Independent route: KLT double copy of Parke-Taylor amplitudes in spinor-helicity form,
M = (kappa/2)^2 s12 A_YM(1,2,3,4) A_YMS(1phi,2phi,4,3) (kappa^2 = 32 pi G, so (kappa/2)^2 = 8 pi G),
photons = gluon x scalar, gravitons = gluon x gluon. All particles outgoing; 3, 4 are the crossed
incoming gravitons (negative energy). Claim: |M| = 8 pi G t^2/s and 8 pi G u^2/s for opposite graviton
helicities; same physical helicity gives zero; the final-helicity sum is (8 pi G)^2 (t^4+u^4)/s^2.
Normalisation anchor: crossing to gamma g -> gamma g must give Skobelev/Bjerrum-Bohr
dsigma/dt = 2 pi G^2 (s^4+u^4)/(s^2 t^2).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import sympy as sp
from math_checks import identity, limit, quantity, units, finish


def lam(p):
    """Spinor for a null momentum; negative energy: lam(-p), lamt = -conj(lam(-p))."""
    sgn = 1.0 if p[0] > 0 else -1.0
    q = sgn * np.asarray(p, float)
    E = q[0]
    th = np.arccos(np.clip(q[3] / E, -1, 1))
    ph = np.arctan2(q[2], q[1])
    l = np.sqrt(2 * E) * np.array([np.cos(th / 2), np.sin(th / 2) * np.exp(1j * ph)])
    lt = np.conj(l) * (1.0 if sgn > 0 else -1.0)
    return l, lt


def ang(a, b):
    return a[0][0] * b[0][1] - a[0][1] * b[0][0]


def sq(a, b):
    return -(a[1][0] * b[1][1] - a[1][1] * b[1][0])


def mdot(p, k):
    return p[0] * k[0] - p[1] * k[1] - p[2] * k[2] - p[3] * k[3]


def kin(w, th, ph):
    n = np.array([np.sin(th) * np.cos(ph), np.sin(th) * np.sin(ph), np.cos(th)])
    p1 = np.r_[w, w * n]
    p2 = np.r_[w, -w * n]
    p3 = -np.array([w, 0, 0, w])      # incoming graviton along +z, crossed
    p4 = -np.array([w, 0, 0, -w])     # incoming graviton along -z, crossed
    return [p1, p2, p3, p4]


def amps(w, th, ph):
    P = kin(w, th, ph)
    S = [lam(p) for p in P]
    a = lambda i, j: ang(S[i - 1], S[j - 1])
    s = lambda i, j: 2 * mdot(P[i - 1], P[j - 1])
    # spinor convention check: <ij>[ji] = s_ij
    conv = max(abs(a(i, j) * sq(S[j - 1], S[i - 1]) - s(i, j)) for i in range(1, 5) for j in range(1, 5) if i != j)
    s12 = s(1, 2)
    den_YM = a(1, 2) * a(2, 3) * a(3, 4) * a(4, 1)
    den_S = a(1, 2) * a(2, 4) * a(4, 3) * a(3, 1)
    # config a: photons (1+,2-), gravitons outgoing (3+,4-)
    Ma = s12 * (a(2, 4) ** 4 / den_YM) * (a(1, 4) ** 2 * a(2, 4) ** 2 / den_S)
    # config b: photons (1+,2-), gravitons outgoing (3-,4+)
    Mb = s12 * (a(2, 3) ** 4 / den_YM) * (a(1, 3) ** 2 * a(2, 3) ** 2 / den_S)
    return Ma, Mb, s12, s(1, 3), s(1, 4), conv


w = 1.0
worst = 0.0
for th in np.linspace(0.2, 2.9, 12):
    for ph in np.linspace(0.0, 6.0, 7):
        Ma, Mb, S_, T_, U_, conv = amps(w, th, ph)
        worst = max(worst, conv)
        ea = abs(abs(Ma) - T_ ** 2 / S_) / (T_ ** 2 / S_)
        eb = abs(abs(Mb) - U_ ** 2 / S_) / (U_ ** 2 / S_)
        worst = max(worst, ea, eb)
Ma, Mb, S_, T_, U_, conv = amps(1.0, 1.1, 0.7)
print(f"s = {S_:.6f}, t = {T_:.6f}, u = {U_:.6f} (natural units, w = 1, theta = 1.1, phi = 0.7)")
print(f"|M_a|/(8 pi G) = {abs(Ma):.6f} vs t^2/s = {T_**2/S_:.6f};  |M_b|/(8 pi G) = {abs(Mb):.6f} vs u^2/s = {U_**2/S_:.6f}")
print(f"in units of 8 pi G s: {abs(Ma)/S_:.6f}, {abs(Mb)/S_:.6f} (lens table: 0.074639, 0.528235)")
print(f"worst relative deviation over 84 kinematic points (incl. spinor convention): {worst:.2e}")
quantity(f"{abs(Ma)/S_:.12f}", "0.074639", rel_tol=1e-5)
quantity(f"{abs(Mb)/S_:.12f}", "0.528235", rel_tol=1e-5)
quantity(f"{1 + worst:.15f}", "1", rel_tol=1e-9)

# Selection rule: same physical helicity of incoming gravitons = outgoing (3+,4+) or (3-,4-).
# With photons (1+,2-): A_YM(1+,2-,3+,4+) has one negative helicity -> 0 at tree level;
# with photons (1+,1+) and gravitons (3-,4-): the scalar factor A(phi phi g- g-) = 0 (massless SWI).
# (Structural, from MHV classification; recorded, not a numeric test.)

# Normalisation anchor and crossing (symbolic, G = 1/(8 pi) * kappa^2/4 ...):
s, t, u, G = sp.symbols("s t u G", real=True)
Sum_gg = 2 * (8 * sp.pi * G) ** 2 * (t**4 + u**4) / s**2           # sum over all helicities, g g -> gamma gamma
Sum_cross = Sum_gg.subs({s: t, t: s}, simultaneous=True)            # crossing s <-> t: gamma g -> gamma g
dsdt = (Sum_cross / 4) / (16 * sp.pi * s**2)
identity(sp.simplify(dsdt), 2 * sp.pi * G**2 * (s**4 + u**4) / (s**2 * t**2),
         domain={"s": (0.1, 10), "t": (-10, -0.1), "u": (-10, -0.1), "G": (0.1, 10)})
# Forward limit: u^2/s -> s as t -> 0 (u = -s - t): amplitude ~ 8 pi G s, the Born-like growth
limit((-s - t) ** 2 / s, "t", 0, s, domain={"s": (0.1, 10), "t": (-1, 1)})
# Units: G (natural) has dimension mass^-2, t^2/s mass^2 -> M dimensionless (2->2 in 4D): check G*hbar/c^3 * (E/c)^2/hbar^2 ...
units("6.674e-11 m^3/(kg*s^2) * 1.0546e-34 J*s / (2.998e8 m/s)^3 * (1 J)^2 / (1.0546e-34 J*s * 2.998e8 m/s)^2", "dimensionless")
raise SystemExit(finish())
