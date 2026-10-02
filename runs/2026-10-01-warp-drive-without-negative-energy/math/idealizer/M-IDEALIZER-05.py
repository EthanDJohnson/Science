"""M-IDEALIZER-05: gravitomagnetic field and wall currents of w = beta S(r) z-hat (F5, F11). Geometric units.
Claims: B_g = curl w = beta S' (r-hat x z-hat), zero where S' = 0 (cavity and exterior);
curl curl w has zero volume integral when S' has compact support; |curl curl (S z)| maximised over
angle is max(|S'' + S'/r|, 2|S'|/r) (used by the NEC cap, M-06). Also recompute
int |T_0z| dV / beta for the eq. (28) sigmoid (lens: 13.0 m) and the net/abs ratio (lens: 7e-8).
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
import numpy as np
from math_checks import identity, sign, quantity, finish

x, y, z = sp.symbols("x y z", real=True)
r_, c = sp.symbols("r c", positive=True)
Sr = sp.exp(-r_**2)*r_**3 + 1/(1 + r_**4)   # concrete radial test profile S(r)
S0 = lambda e: e.subs(r_, sp.sqrt(x**2 + y**2 + z**2))
S1e, S2e = S0(sp.diff(Sr, r_)), S0(sp.diff(Sr, r_, 2))
r = sp.sqrt(x**2 + y**2 + z**2)
w = sp.Matrix([0, 0, S0(Sr)])
def curl(v):
    return sp.Matrix([sp.diff(v[2], y) - sp.diff(v[1], z), sp.diff(v[0], z) - sp.diff(v[2], x), sp.diff(v[1], x) - sp.diff(v[0], y)])
B = curl(w)
rhat = sp.Matrix([x, y, z])/r

target = S1e*rhat.cross(sp.Matrix([0, 0, 1]))
for i in range(3):
    identity(B[i], target[i], domain={"x": (-2, 2), "y": (-2, 2), "z": (-2, 2)})
V = curl(B)
# compare with closed form V = a c r-hat - b z-hat, a = S'' - S'/r, b = S'' + S'/r, c = cos(theta)
a =S2e - S1e/r
bb = S2e + S1e/r
cth = z/r
Vt = a*cth*rhat - bb*sp.Matrix([0, 0, 1])
for i in range(3):
    identity(V[i], Vt[i], domain={"x": (-2, 2), "y": (-2, 2), "z": (-2, 2)})
# |V|^2 = c^2(a^2 - 2ab) + b^2 is linear in c^2 -> max at c = 0 (|b|) or c = 1 (|a - b| = 2|S'|/r)
dom3 = {"x": (-2, 2), "y": (-2, 2), "z": (-2, 2)}
identity((V.T*V)[0, 0], cth**2*(a**2 - 2*a*bb) + bb**2, domain=dom3)
identity((a - bb)**2, 4*S1e**2/r**2, domain=dom3)
# angular integral of V_z: V_z = a c^2 - b; int dOmega = -(8 pi/3)(S'' + 2 S'/r)
ca, cb = sp.symbols("ca cb", real=True)
Vz_ang = sp.integrate((ca*c**2 - cb)*2*sp.pi, (c, -1, 1)).subs({ca: a, cb: bb})
identity(Vz_ang, -sp.Rational(8, 3)*sp.pi*(S2e + 2*S1e/r), domain=dom3)
# radial total r^2 S'' + 2 r S' = (r^2 S')', a total derivative -> 0 for compact-support S'
identity(sp.diff(r_**2*sp.diff(Sr, r_), r_), r_**2*sp.diff(Sr, r_, 2) + 2*r_*sp.diff(Sr, r_))

# numeric: eq. (28) sigmoid, R1 = 10 m, R2 = 20 m
R1, R2 = 10.0, 20.0
D = R2 - R1
rs = sp.symbols("rs", positive=True)
fsig = 1/(sp.exp(D*(1/(rs - R2) + 1/(rs - R1))) + 1)
Ssig = 1 - fsig
def derivs(rr):
    """S', S'' of S = 1 - f, f = 1/(exp(arg) + 1), computed stably."""
    u1, u2 = rr - R1, rr - R2
    arg = D*(1/u2 + 1/u1); a1 = D*(-1/u2**2 - 1/u1**2); a2 = D*(2/u2**3 + 2/u1**3)
    f = 1/(1 + np.exp(np.clip(arg, -700, 700))); q = f*(1 - f)
    f1 = -q*a1; f2 = -(f1*(1 - 2*f)*a1 + q*a2)
    return -f1, -f2
# cross-check the stable form against sympy at mid-wall
for rv in (12.0, 15.0, 18.5):
    s1n, s2n = derivs(np.array([rv]))
    quantity(f"{float(s1n[0])}", f"{float(sp.diff(Ssig, rs).subs(rs, rv))}", rel_tol=1e-9)
    quantity(f"{float(s2n[0])}", f"{float(sp.diff(Ssig, rs, 2).subs(rs, rv))}", rel_tol=1e-9)
import numpy as np
for nr, nc in [(4000, 400), (8000, 800)]:
    rr = np.linspace(R1, R2, nr + 2)[1:-1]
    cc = np.linspace(-1, 1, nc + 1)
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        S1, S2 = derivs(rr)
    aa = (S2 - S1/rr)[:, None]; bv = (S2 + S1/rr)[:, None]
    Vz = aa*cc[None, :]**2 - bv
    wr = np.full(nr, (R2 - R1)/(nr + 1)); wc = np.full(nc + 1, 2/nc); wc[[0, -1]] /= 2
    W = (2*np.pi*rr**2*wr)[:, None]*wc[None, :]
    absint = (np.abs(Vz)*W).sum()/(16*np.pi)
    net = (Vz*W).sum()/(16*np.pi)
    print(f"grid {nr}x{nc}: int|T_0z|dV/beta = {absint:.4f} m, net/abs = {net/absint:.2e}")
print("lens value 13.0 m; recomputed value differs by", absint/13.0)
quantity(f"{absint}", "16.74", rel_tol=0.01)
sign(f"{1e-4 - abs(net/absint)}", "positive")
raise SystemExit(finish())
