"""M-DIALECTICIAN-02: regularity classes of the Eulerian-energy divergence identity.
Unit lapse, flat slice, beta = grad(phi); 16 pi rho_E = (lap phi)^2 - phi_ij phi_ij (M-01).
Separable phi = g(x) h(y) h(z), my own test functions (geometric units, lengths in m, phi in m):
  h(y) = exp(-y^2)
  C1 case:  g(x) = exp(-x^2) (1 + q x|x|/2)  -> g, g' continuous, g'' jumps by 2q at x = 0
  C0 case:  g(x) = exp(-x^2) (1 + k|x|/2)    -> [g'](0) = k, kink in phi
Claims: C1 total = 0; C0 bulk != 0 and cancelled by sheet sigma = (1/8pi)[d_n phi] lap_t phi on x = 0;
delta^2 terms cancel identically. Bulk integrals built from the six second-derivative products
by 1D quadrature on x<0 and x>0 separately (definitions), not from a closed formula.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
import mpmath as mp
from math_checks import identity, quantity, sign, limit, finish

mp.mp.dps = 30
x, y = sp.symbols("x y", real=True)

# delta^2 coefficient: coefficient of phi_xx^2 in lap^2 - quad
pxx, pyy, pzz, pxy, pxz, pyz = sp.symbols("pxx pyy pzz pxy pxz pyz", real=True)
expr = (pxx + pyy + pzz) ** 2 - (pxx**2 + pyy**2 + pzz**2 + 2 * pxy**2 + 2 * pxz**2 + 2 * pyz**2)
c2 = sp.Poly(sp.expand(expr), pxx).coeff_monomial(pxx**2)
print("coefficient of phi_xx^2 (delta^2 term):", c2)
identity(c2, 0)
# linear-in-phi_xx coefficient: 2(phi_yy + phi_zz) -> sheet 16 pi sigma = 2 [phi_x] lap_t phi
c1 = sp.Poly(sp.expand(expr), pxx).coeff_monomial(pxx)
identity(c1, 2 * (pyy + pzz))

h = sp.exp(-y**2)
H = {k: sp.lambdify(y, sp.diff(h, y, k), "mpmath") for k in range(3)}
def hint(f):
    return mp.quad(f, [-mp.inf, 0, mp.inf])
hh = hint(lambda t: H[0](t) ** 2)
h2h = hint(lambda t: H[2](t) * H[0](t))
h1h1 = hint(lambda t: H[1](t) ** 2)

def bulk_and_sheet(gpos, gneg):
    """gpos/gneg: sympy expressions of g on x>0 and x<0. Returns 16pi*int(bulk), 16pi*int(sheet)."""
    G = {}
    for k in range(3):
        fp = sp.lambdify(x, sp.diff(gpos, x, k), "mpmath")
        fn = sp.lambdify(x, sp.diff(gneg, x, k), "mpmath")
        G[k] = (fp, fn)
    def gint(a, b):
        return mp.quad(lambda t: G[a][1](t) * G[b][1](t), [-mp.inf, 0]) + mp.quad(lambda t: G[a][0](t) * G[b][0](t), [0, mp.inf])
    # 2*(xx*yy + xx*zz + yy*zz - xy^2 - xz^2 - yz^2), phi = g h(y) h(z)
    I_xx_yy = gint(2, 0) * h2h * hh
    I_xx_zz = gint(2, 0) * hh * h2h
    I_yy_zz = gint(0, 0) * h2h * h2h
    I_xy2 = gint(1, 1) * h1h1 * hh
    I_xz2 = gint(1, 1) * hh * h1h1
    I_yz2 = gint(0, 0) * h1h1 * h1h1
    bulk = 2 * (I_xx_yy + I_xx_zz + I_yy_zz - I_xy2 - I_xz2 - I_yz2)
    jump = G[1][0](mp.mpf(0)) - G[1][1](mp.mpf(0))
    g0 = G[0][0](mp.mpf(0))
    # sheet: 2 [phi_x] (phi_yy + phi_zz) on x = 0, [phi_x] = [g'] h(y)h(z)
    sheet = 2 * jump * g0 * (h2h * hh + hh * h2h)
    return bulk, sheet, jump

base = sp.exp(-x**2)
cases = {
    "smooth": (base * (1 + x / 3), base * (1 + x / 3)),
    "C1 (q=1)": (base * (1 + x**2 / 2), base * (1 - x**2 / 2)),
    "C0 (k=1)": (base * (1 + x / 2), base * (1 - x / 2)),
    "C0 (k=4)": (base * (1 + 2 * x), base * (1 - 2 * x)),
    "C0 (k=-1)": (base * (1 - x / 2), base * (1 + x / 2)),
}
res = {}
for name, (gp, gn) in cases.items():
    b, s, j = bulk_and_sheet(gp, gn)
    res[name] = (b, s)
    print(f"{name:10s}: [g'] = {mp.nstr(j, 6)}, 16pi*bulk = {mp.nstr(b, 12)}, 16pi*sheet = {mp.nstr(s, 12)}, total = {mp.nstr(b + s, 5)}")

identity(sp.Float(mp.nstr(res['smooth'][0], 25)), 0)
identity(sp.Float(mp.nstr(res['C1 (q=1)'][0], 25)), 0)
for name in ("C0 (k=1)", "C0 (k=4)", "C0 (k=-1)"):
    b, s = res[name]
    print(name, "bulk nonzero:", abs(b) > 1e-6, " bulk+sheet:", mp.nstr(b + s, 5))
    sign(sp.Float(str(abs(b))), "positive")
    identity(sp.Float(mp.nstr(b + s, 25)), 0)
# linearity in the kink strength (lens: 6.283 for [g']=1 and 25.13 for [g']=4, ratio 4)
ratio = res["C0 (k=4)"][0] / res["C0 (k=1)"][0]
print("bulk(k=4)/bulk(k=1) =", mp.nstr(ratio, 12), "(not exactly 4 here because my g also changes with k away from x=0)")
# closed form for separable phi: 16pi*bulk = 4 g(0)[g'] int h'^2 int h^2 ; check against the quadrature
for name in ("C0 (k=1)", "C0 (k=4)"):
    k = {"C0 (k=1)": 1, "C0 (k=4)": 4}[name]
    print(name, "4 g(0)[g'] int h'^2 int h^2 =", mp.nstr(4 * 1 * k * h1h1 * hh, 12))
    quantity(f"{float(res[name][0])} m", f"{float(4 * k * h1h1 * hh)} m", rel_tol=1e-12)
# limit: kink strength -> 0 gives bulk -> 0
kk = sp.symbols("kk", positive=True)
limit(4 * kk * sp.sqrt(sp.pi / 2) * sp.sqrt(sp.pi / 2) / 1, "kk", 0, 0)
raise SystemExit(finish())
