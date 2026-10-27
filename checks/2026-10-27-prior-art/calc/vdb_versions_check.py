"""Independent check of the van-den-broeck finding (angle: versions).

Part A: arithmetic on the numbers printed in gr-qc/9905084 (all versions), SI conversion.
Part B: independent recomputation of the region-II geometry (metric -dt^2 + B^2 dx_i^2, B from
        VdB eq. 12/13) with sympy generating the Riemann tensor from the metric itself (not the
        paper's closed forms), then mpmath evaluation on a w-grid. Compares paper eqs (11), (19).
Part C: Ford-Roman QI test (tau0 = 0.1 r_c) at the v1-v4 parameters and at the v5 parameters.

Run:  python3 checks/2026-10-27-prior-art/calc/vdb_versions_check.py
"""
import mpmath as mp
import sympy as sp

mp.mp.dps = 50
G, c, hbar = mp.mpf("6.6743e-11"), mp.mpf("2.99792458e8"), mp.mpf("1.054571817e-34")
LP = mp.sqrt(hbar * G / c**3)
KGM = c**2 / G  # kg per metre; kg/m^3 per 1/m^2


def fmt(x, n=4):
    return mp.nstr(x, n)


print("=" * 70)
print("PART A: arithmetic on printed numbers")
print(f"L_P = {fmt(LP,5)} m ; c^2/G = {fmt(KGM,5)} kg/m")
for label, Dt in (("v1-v4 / (v5 text as printed)", mp.mpf("1e-32")), ("v5 eq.(7) Delta~", mp.mpf("1e-15"))):
    rc = Dt / mp.mpf("72.5")
    print(f"  Delta~ = {fmt(Dt,3)} m ({label}): Delta~/72.5 = {fmt(rc,4)} m = {fmt(rc/LP,4)} L_P")
# paper eq (14)/(15): T00 = -4.9e2 / Delta~^2  (geometric) -> kg/m^3 via c^2/G
for label, Dt in (("Delta~=1e-32", mp.mpf("1e-32")), ("Delta~=1e-15", mp.mpf("1e-15"))):
    lhs = mp.mpf("4.9e2") / Dt**2 * KGM
    rc = Dt / mp.mpf("72.5")
    tau0 = mp.mpf("0.1") * rc
    # QI in SI: rho >= -3 hbar/(32 pi^2 c tau0^4)  (kg/m^3, tau0 a length)  [= 3 L_P^2/(32 pi^2 tau0^4) * c^2/G]
    rhs = 3 * hbar / (32 * mp.pi**2 * c * tau0**4)
    print(f"  {label}: paper-formula LHS = -{fmt(lhs,3)} kg/m^3 ; RHS = -{fmt(rhs,3)} kg/m^3 ; |LHS|/|RHS| = {fmt(lhs/rhs,3)}"
          + ("  (QI satisfied)" if lhs < rhs else "  (QI VIOLATED)"))
# printed v1-v4 E_II- = -2.5e2*Delta~ = -3.4e-3 kg (Delta~ = 1e-32 m)
print(f"  v4 eq.(16): -2.5e2 * Delta~ * c^2/G at Delta~=1e-32 m = {fmt(-mp.mpf('2.5e2')*mp.mpf('1e-32')*KGM,3)} kg (paper: -3.4e-3 kg)")
# v1-v4 E_IV and v5 E_IV are not re-derived here.

print("=" * 70)
print("PART B: independent Riemann/Einstein from the metric (sympy), region II comoving frame")
r, th = sp.symbols("r theta", positive=True)
Bf = sp.Function("B")(r)
# 3-metric on t=const (lapse 1, K_ij = 0): g = B^2 (dr^2 + r^2 dtheta^2 + r^2 sin^2 theta dphi^2)
ph = sp.symbols("phi")
X = [r, th, ph]
g = sp.diag(Bf**2, (Bf * r) ** 2, (Bf * r * sp.sin(th)) ** 2)
ginv = g.inv()


def christoffel(a, b, cc):
    return sum(ginv[a, d] * (sp.diff(g[d, b], X[cc]) + sp.diff(g[d, cc], X[b]) - sp.diff(g[b, cc], X[d])) for d in range(3)) / 2


Gam = [[[sp.simplify(christoffel(a, b, cc)) for cc in range(3)] for b in range(3)] for a in range(3)]


def riemann(a, b, cc, d):  # R^a_{bcd}
    expr = sp.diff(Gam[a][b][d], X[cc]) - sp.diff(Gam[a][b][cc], X[d])
    expr += sum(Gam[a][cc][e] * Gam[e][b][d] - Gam[a][d][e] * Gam[e][b][cc] for e in range(3))
    return sp.simplify(expr)


def Rlow(a, b, cc, d):
    return sp.simplify(sum(g[a, e] * riemann(e, b, cc, d) for e in range(3)))


# orthonormal sectional curvatures K_rt = R_{r th r th}/(g_rr g_thth), K_thph = R_{th ph th ph}/(g_thth g_phph)
K_rth = sp.simplify(Rlow(0, 1, 0, 1) / (g[0, 0] * g[1, 1]))
K_thph = sp.simplify(Rlow(1, 2, 1, 2) / (g[1, 1] * g[2, 2]))
# 3-Ricci scalar: R3 = 2*(2*K_rth + K_thph)  (sum over ordered pairs: 2*(K_r th + K_r ph + K_th ph), K_r th = K_r ph)
R3 = sp.simplify(2 * (2 * K_rth + K_thph))
rho_sym = sp.simplify(R3 / (16 * sp.pi))  # Eulerian density rho = G_00/(8 pi) = R3/(16 pi) when K_ij = 0
B1, B2 = sp.diff(Bf, r), sp.diff(Bf, r, 2)
rho_paper = (B1**2 / Bf**4 - 2 * B2 / Bf**3 - 4 * B1 / (Bf**3 * r)) / (8 * sp.pi)  # paper eq (11)
R1212_paper = B1**2 / Bf**4 - B2 / Bf**3 - B1 / (Bf**3 * r)  # paper eq (19)
print("  rho_sym - rho_paper(eq.11)      =", sp.simplify(rho_sym - rho_paper))
print("  K_r-theta  vs paper eq.(19) R1212 : difference =", sp.simplify(K_rth - R1212_paper), " (0 => same up to sign? check sign:)",
      sp.simplify(K_rth + R1212_paper))
print("  K_theta-phi =", sp.simplify(K_thph))

# numeric evaluation with explicit B(w) (VdB eq 12-13)
n_sym = 80
alpha_s, Rt_s, Dt_s = sp.symbols("alpha Rt Dt", positive=True)
w_s = (Rt_s + Dt_s - r) / Dt_s
B_expl = 1 + alpha_s * (-(n_sym - 1) * w_s**n_sym + n_sym * w_s ** (n_sym - 1))
rho_expr = rho_sym.subs(Bf, B_expl).doit()
Kr_expr = K_rth.subs(Bf, B_expl).doit()
Kt_expr = K_thph.subs(Bf, B_expl).doit()
f_rho = sp.lambdify((r, alpha_s, Rt_s, Dt_s), rho_expr, "mpmath")
f_Kr = sp.lambdify((r, alpha_s, Rt_s, Dt_s), Kr_expr, "mpmath")
f_Kt = sp.lambdify((r, alpha_s, Rt_s, Dt_s), Kt_expr, "mpmath")


def scan(alpha, Rt, Dt, N=4000, label=""):
    alpha, Rt, Dt = mp.mpf(alpha), mp.mpf(Rt), mp.mpf(Dt)
    best_rho = (mp.mpf(0), None)
    bestK = (mp.mpf(0), None)
    for i in range(1, N):
        w = mp.mpf(i) / N
        rr = Rt + Dt - w * Dt
        rho = f_rho(rr, alpha, Rt, Dt)
        K = max(abs(f_Kr(rr, alpha, Rt, Dt)), abs(f_Kt(rr, alpha, Rt, Dt)))
        if rho < best_rho[0]:
            best_rho = (rho, w)
        if K > bestK[0]:
            bestK = (K, w)
    rho, wr = best_rho
    K, wK = bestK
    rc = 1 / mp.sqrt(K)
    tau0 = mp.mpf("0.1") * rc
    bound = 3 * LP**2 / (32 * mp.pi**2 * tau0**4)
    print(f"  [{label}] alpha={fmt(alpha,2)} Delta~=Rt~={fmt(Dt,2)} m:")
    print(f"    density peak at w = {fmt(wr,4)}  rho = {fmt(rho,4)} /m^2 = {fmt(rho*KGM,4)} kg/m^3 ; rho*Dt^2 = {fmt(rho*Dt**2,4)}")
    print(f"    max |K| at w = {fmt(wK,4)} : {fmt(K,4)} /m^2 -> r_c = {fmt(rc,4)} m = Delta~/{fmt(Dt/rc,4)} = {fmt(rc/LP,4)} L_P")
    print(f"    QI bound (tau0=0.1 r_c) = -{fmt(bound*KGM,4)} kg/m^3 ; |rho_pk|/|bound| = {fmt(-rho/bound,4)}"
          + ("  -> QI SATISFIED" if -rho < bound else "  -> QI VIOLATED"))


print("PART C: QI tests")
scan("1e34", "1e-32", "1e-32", label="v1-v4 eq.(7)")
scan("1e17", "1e-15", "1e-15", label="v5 / CQG eq.(7)")
