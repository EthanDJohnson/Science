"""Independent recomputation of Van Den Broeck (1999, gr-qc/9905084) region-II QI check.

Written for checks/2026-10-27-prior-art (angle: recompute). Does NOT reuse the falsifier's
or lens's scripts. Formulas taken from the paper (v5 text, fetched with fetch_text.py):
  eq.12  B = alpha*(-(n-1) w^n + n w^(n-1)) + 1,  eq.13  w = (Rt + Dt - r)/Dt,  n = 80
  eq.11  T00 = (1/8pi) (B'^2/B^4 - 2 B''/B^3 - 4 B'/(r B^3))     (' = d/dr)
  eq.19  R_1212 = B'^2/B^4 - B''/B^3 - B'/(r B^3);  eq.20 rc,min = 1/sqrt(max|R_1212|)
  eq.21  tau0 = beta*rc,min, beta = 0.1;  eq.22  T00 >= -3/(32 pi^2 tau0^4)  (hbar=c=G=1)
Step A derives T00 and all orthonormal Riemann components from scratch with sympy for
ds^2 = -dt^2 + B(r)^2 (dr^2 + r^2 dOmega^2) and checks them against eqs 11 and 19.
Step B evaluates everything with mpmath (60 digits) at both parameter sets.
Step C cross-checks the curvature at one point with the toolkit's gr_tensors.curvature_at.
"""
import sys
import sympy as sp
import mpmath as mp

# ---------------- Step A: symbolic derivation -----------------------------------------
t, r, th, ph = sp.symbols("t r theta phi", positive=True)
Bf = sp.Function("B")(r)
coords = [t, r, th, ph]
g = sp.diag(-1, Bf**2, Bf**2 * r**2, Bf**2 * r**2 * sp.sin(th)**2)
gi = g.inv()
N = 4
Gam = [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], coords[c]) + sp.diff(g[d, c], coords[b])
                                     - sp.diff(g[b, c], coords[d])) for d in range(N)) / 2)
         for c in range(N)] for b in range(N)] for a in range(N)]
def Riem_up(a, b, c, d):  # R^a_bcd
    e = sp.diff(Gam[a][d][b], coords[c]) - sp.diff(Gam[a][c][b], coords[d])
    e += sum(Gam[a][c][k] * Gam[k][d][b] - Gam[a][d][k] * Gam[k][c][b] for k in range(N))
    return sp.simplify(e)
Rup = {}
for a in range(N):
    for b in range(N):
        for c in range(N):
            for d in range(N):
                Rup[(a, b, c, d)] = Riem_up(a, b, c, d)
def Rlow(a, b, c, d):
    return sp.simplify(sum(g[a, k] * Rup[(k, b, c, d)] for k in range(N)))
Ric = sp.Matrix(N, N, lambda b, d: sp.simplify(sum(Rup[(a, b, a, d)] for a in range(N))))
Rs = sp.simplify(sum(gi[a, b] * Ric[a, b] for a in range(N) for b in range(N)))
G00 = sp.simplify(Ric[0, 0] - g[0, 0] * Rs / 2)   # e_0 = d_t is already unit
T00_derived = sp.simplify(G00 / (8 * sp.pi))
Bp, Bpp = sp.diff(Bf, r), sp.diff(Bf, r, 2)
T00_paper = (Bp**2 / Bf**4 - 2 * Bpp / Bf**3 - 4 * Bp / (r * Bf**3)) / (8 * sp.pi)
# orthonormal components: divide by the norms of the coordinate legs
norms = [1, Bf, Bf * r, Bf * r * sp.sin(th)]
def Rhat(a, b, c, d):
    return sp.simplify(Rlow(a, b, c, d) / (norms[a] * norms[b] * norms[c] * norms[d]))
R_rtrt = Rhat(1, 2, 1, 2)    # radial-tangential (paper's R_1212 on the x axis)
R_tptp = Rhat(2, 3, 2, 3)    # tangential-tangential
R_0i0j = [Rhat(0, i, 0, i) for i in (1, 2, 3)]
R1212_paper = Bp**2 / Bf**4 - Bpp / Bf**3 - Bp / (r * Bf**3)
print("== Step A: symbolic checks ==")
print("T00 derived - eq.11  :", sp.simplify(T00_derived - T00_paper))
print("R_(r th r th) derived:", sp.simplify(R_rtrt))
print("R_(r th r th) - eq.19:", sp.simplify(R_rtrt - R1212_paper))
print("R_(th ph th ph)      :", sp.simplify(R_tptp))
print("R_(0i0i)             :", R_0i0j)
# all independent nonzero orthonormal components
nz = set()
for a in range(N):
    for b in range(a + 1, N):
        for c in range(N):
            for d in range(c + 1, N):
                v = Rhat(a, b, c, d)
                if v != 0:
                    nz.add(((a, b, c, d), sp.simplify(v)))
print("nonzero orthonormal R_abcd (a<b, c<d):", sorted(k for k, _ in nz))

# ---------------- Step B: numerics -----------------------------------------------------
mp.mp.dps = 60
G_N = mp.mpf("6.67430e-11"); C = mp.mpf(299792458); HBAR = mp.mpf("1.054571817e-34")
C2_G = C**2 / G_N                     # kg/m
LP = mp.sqrt(HBAR * G_N / C**3)
MSUN = mp.mpf("1.98847e30")
n = 80
rr, al, Dt, Rt = sp.symbols("rr alpha Dt Rt", positive=True)
w_r = (Rt + Dt - rr) / Dt
B_r = al * (-(n - 1) * w_r**n + n * w_r**(n - 1)) + 1
sub = {Bpp: sp.diff(B_r, rr, 2), Bp: sp.diff(B_r, rr), Bf: B_r}
def lam(expr):
    e = expr.subs(r, rr)
    e = e.subs({sp.Derivative(sp.Function("B")(rr), rr, 2): sp.diff(B_r, rr, 2)})
    e = e.subs({sp.Derivative(sp.Function("B")(rr), rr): sp.diff(B_r, rr)})
    e = e.subs({sp.Function("B")(rr): B_r})
    return sp.lambdify((rr, al, Dt, Rt), e, "mpmath")
f_T00 = lam(T00_derived)
f_Rrt = lam(R_rtrt)
f_Rtp = lam(R_tptp)
f_B = sp.lambdify((rr, al, Dt, Rt), B_r, "mpmath")

def peak(fun, a, D, Rtil, sign):
    """global extremum over w in (0,1) of sign*fun: grid then golden refinement."""
    best = None
    M = 4000
    for i in range(1, M):
        w = mp.mpf(i) / M
        v = sign * fun(Rtil + D - w * D, a, D, Rtil)
        if best is None or v > best[1]:
            best = (w, v)
    lo, hi = best[0] - mp.mpf(1) / M, best[0] + mp.mpf(1) / M
    phi = (mp.sqrt(5) - 1) / 2
    for _ in range(200):
        m1, m2 = hi - phi * (hi - lo), lo + phi * (hi - lo)
        if sign * fun(Rtil + D - m1 * D, a, D, Rtil) > sign * fun(Rtil + D - m2 * D, a, D, Rtil):
            hi = m2
        else:
            lo = m1
    w = (lo + hi) / 2
    return w, fun(Rtil + D - w * D, a, D, Rtil)

def zero_cross(a, D, Rtil):
    """w where T00 changes sign from negative to positive (near w ~ 0.98)."""
    f = lambda w: f_T00(Rtil + D - w * D, a, D, Rtil) * D**2   # dimensionless
    ws = [mp.mpf(i) / 2000 for i in range(1, 2000)]
    for w1, w2 in zip(ws, ws[1:]):
        if f(w1) < 0 and f(w2) > 0:
            return mp.findroot(f, (w1, w2), solver="bisect")
    return None

def E_II(a, D, Rtil, w0):
    """E = int 4 pi r^2 B^3 T00 dr  (sqrt(gS) = B^3), split at w0. Returns metres (geometric)."""
    integrand = lambda w: 4 * mp.pi * (Rtil + D - w * D)**2 * f_B(Rtil + D - w * D, a, D, Rtil)**3 \
        * f_T00(Rtil + D - w * D, a, D, Rtil) * D
    pts_neg = [0] + [mp.mpf(k) / 20 for k in range(1, 20) if mp.mpf(k) / 20 < w0] + [w0]
    neg = mp.quad(integrand, pts_neg)
    pos = mp.quad(integrand, [w0, (w0 + 1) / 2, mp.mpf(1)])
    return neg, pos

def qi_bound_kg_m3(tau0_m):
    return -3 * HBAR / (32 * mp.pi**2 * C * tau0_m**4)

def analyse(label, a, D, Rtil, beta=mp.mpf("0.1")):
    a, D, Rtil = mp.mpf(a), mp.mpf(D), mp.mpf(Rtil)
    print(f"\n== {label}: alpha={mp.nstr(a,3)}, Dt={mp.nstr(D,3)} m, Rt={mp.nstr(Rtil,3)} m, n={n} ==")
    wr, rho = peak(f_T00, a, D, Rtil, -1)
    print(f" T00 peak (most negative): w = {mp.nstr(wr,5)}, T00 = {mp.nstr(rho*D**2,5)}/Dt^2 m^-2"
          f" = {mp.nstr(rho,5)} m^-2 = {mp.nstr(rho*C2_G,5)} kg/m^3")
    w1, R1 = peak(lambda *x: abs(f_Rrt(*x)), a, D, Rtil, +1)
    w2, R2 = peak(lambda *x: abs(f_Rtp(*x)), a, D, Rtil, +1)
    print(f" max|R_(r th r th)| (eq.19) at w = {mp.nstr(w1,5)}: {mp.nstr(R1,5)} m^-2 -> 1/sqrt = Dt/{mp.nstr(D*mp.sqrt(R1),5)}")
    print(f" max|R_(th ph th ph)|       at w = {mp.nstr(w2,5)}: {mp.nstr(R2,5)} m^-2 -> 1/sqrt = Dt/{mp.nstr(D*mp.sqrt(R2),5)}")
    Rmax = max(R1, R2)
    rc = 1 / mp.sqrt(Rmax)
    tau0 = beta * rc
    bound = qi_bound_kg_m3(tau0)
    lhs = rho * C2_G
    print(f" r_c,min = {mp.nstr(rc,5)} m = Dt/{mp.nstr(D/rc,5)} = {mp.nstr(rc/LP,5)} L_P;  tau0 = {mp.nstr(beta,2)} r_c = {mp.nstr(tau0,4)} m")
    print(f" QI (eq.22): LHS T00 = {mp.nstr(lhs,4)} kg/m^3 ; RHS = {mp.nstr(bound,4)} kg/m^3")
    ok = lhs >= bound
    print(f"  -> {'SATISFIED' if ok else 'VIOLATED'}; |LHS|/|RHS| = {mp.nstr(lhs/bound,4)}")
    w0 = zero_cross(a, D, Rtil)
    neg, pos = E_II(a, D, Rtil, w0)
    print(f" T00 sign change at w = {mp.nstr(w0,5)}; E_II,- = {mp.nstr(neg*C2_G,4)} kg ({mp.nstr(neg*C2_G/MSUN,3)} Msun),"
          f" E_II,+ = {mp.nstr(pos*C2_G,4)} kg")
    # scale-free pass condition: rho = k_rho/Dt^2, rc = Dt/k_c; pass iff rc < rc_max
    k_rho, k_c = -rho * D**2, D / rc
    rc_max = LP * k_c * mp.sqrt(3 / (32 * mp.pi**2 * k_rho)) / beta**2
    print(f" pass condition at this alpha (same w-profile): r_c < {mp.nstr(rc_max/LP,4)} L_P, i.e. Dt < {mp.nstr(rc_max*k_c,4)} m")
    return dict(w_rho=wr, rho=lhs, rc=rc, bound=bound, ratio=lhs / bound)

print("\n== Step B: numerics (60 digits) ==")
print(f"c^2/G = {mp.nstr(C2_G,6)} kg/m, L_P = {mp.nstr(LP,6)} m")
A = analyse("v1-v4 eq.7 (Planck pocket)", "1e34", "1e-32", "1e-32")
Bres = analyse("v5 / published eq.7 (femtometre)", "1e17", "1e-15", "1e-15")
print("\n-- what VdB's printed eqs 14 and 20 give if Dt = 1e-15 m is simply plugged in --")
D5 = mp.mpf("1e-15")
lhs5 = mp.mpf(-490) / D5**2 * C2_G
rc5 = D5 / mp.mpf("72.5")
print(f" LHS = -4.9e2/Dt^2 * c^2/G = {mp.nstr(lhs5,4)} kg/m^3; rc = Dt/72.5 = {mp.nstr(rc5,4)} m;"
      f" RHS = {mp.nstr(qi_bound_kg_m3(rc5/10),4)} kg/m^3; ratio {mp.nstr(lhs5/qi_bound_kg_m3(rc5/10),4)}")
print("\n-- separate the effects: alpha vs Dt --")
analyse("alpha=1e17 with Dt=Rt=1e-32 m", "1e17", "1e-32", "1e-32")
analyse("alpha=1e34 with Dt=Rt=1e-15 m", "1e34", "1e-15", "1e-15")
print("\n-- sensitivity of the femtometre violation to beta --")
for beta in ("1", "0.1", "0.01", "0.001"):
    rcB = Bres["rc"]; bnd = qi_bound_kg_m3(mp.mpf(beta) * rcB)
    print(f" beta={beta}: ratio |LHS|/|RHS| = {mp.nstr(Bres['rho']/bnd,4)}")

# ---------------- Step C: toolkit cross-check at one point -------------------------------
if "--toolkit" not in sys.argv:
    print("\n== Step C skipped by default (symbolic Riemann of the explicit n=80 profile takes >7 min); see vdb_toolkit_crosscheck.py, or pass --toolkit ==")
    sys.exit(0)
print("\n== Step C: toolkit gr_tensors.curvature_at cross-check (Dt = 1 units) ==")
sys.path.insert(0, ".claude/skills/conundrum/scripts")
try:
    from gr_tensors import Spacetime
    T, X, Y, Z = sp.symbols("t x y z", real=True)
    for alpha_s, wtest in (("1e34", 0.348), ("1e17", None)):
        a_n = float(alpha_s)
        if wtest is None:
            wtest = float(peak(lambda *x: abs(f_Rrt(*x)), mp.mpf(alpha_s), mp.mpf(1), mp.mpf(1), +1)[0])
        Rexpr = sp.sqrt(X**2 + Y**2 + Z**2)
        wx = (2 - Rexpr)
        Bx = sp.Float(a_n) * (-(n - 1) * wx**n + n * wx**(n - 1)) + 1
        st = Spacetime(sp.diag(-1, Bx**2, Bx**2, Bx**2), [T, X, Y, Z])
        xpt = 2 - wtest
        cur = st.curvature_at((0.0, xpt, 0.0, 0.0))
        mine = max(abs(f_Rrt(mp.mpf(xpt), mp.mpf(alpha_s), 1, 1)), abs(f_Rtp(mp.mpf(xpt), mp.mpf(alpha_s), 1, 1)))
        print(f" alpha={alpha_s}, w={wtest:.4f}: toolkit max frame |R| = {cur['max_frame_component']:.6g},"
              f" mine = {mp.nstr(mine,6)}; toolkit r_c = Dt/{1/cur['curvature_radius']:.5g}")
except Exception as exc:  # report, do not hide
    print(" toolkit cross-check failed:", repr(exc))
