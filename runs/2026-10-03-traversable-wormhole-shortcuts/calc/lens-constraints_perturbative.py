"""Constraints lens: published integrals for the quantum-supported constructions, reproduced where tractable.
1  JT gravity in global AdS2 (Maldacena-Qi setting): ds^2 = (-dt^2 + ds^2)/sin^2 s, s in (0, pi).
   Field equation (sign fixed by null focusing of the dilaton, the 2D analogue of area):
       8 pi G T_ab = -nabla_a nabla_b phi + g_ab (box phi - phi).
   Check: the vacuum black hole phi = cos t / sin s has T = 0. Static eternal-wormhole dilaton with traceless
   (conformal) matter: box phi = 2 phi  =>  phi = phi0 [1 + (pi/2 - s) cot s]. Compute T_kk and the ANEC along the
   complete boundary-to-boundary null ray, affinely parametrised (k^t = 1 at the throat s = pi/2), and in terms of
   the renormalised boundary dilaton phi_r = phi0 pi/2 (phi -> phi_r / s near s -> 0 with boundary time = global time).
2  MMP energy (dossier Q-10): E(l) = r_e^3/(G l^2) - q/(8 l); minimise.
3  2D Casimir ANEC per loop for c species on a circle of light-length L: T_kk integral = -pi c/(3 L) (hbar = c = 1),
   compared with MMP's -q/(8 l).
4  Achronality margins T_thru - T_ext for the one-sided constructions (dossier values), and units check for MM.
"""
import math
import sympy as sp

print("=== 1. JT / Maldacena-Qi: static global AdS2 wormhole ===")
t, s = sp.symbols("t s", real=True)
phi0, G = sp.symbols("phi0 G", positive=True)
X = [t, s]
w = sp.sin(s) ** -2
g = sp.diag(-w, w)
gi = g.inv()
Gam = [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d])) for d in range(2)) / 2)
         for c in range(2)] for b in range(2)] for a in range(2)]

def hess(f):
    return sp.Matrix(2, 2, lambda a, b: sp.diff(f, X[a], X[b]) - sum(Gam[c][a][b] * sp.diff(f, X[c]) for c in range(2)))

def box(f):
    H = hess(f)
    return sp.simplify(sum(gi[a, b] * H[a, b] for a in range(2) for b in range(2)))

def T_of(f):
    H = hess(f)
    return sp.simplify((-H + g * (box(f) - f)) / (8 * sp.pi * G))

phi_bh = sp.cos(t) / sp.sin(s)
print("vacuum check, phi = cos t / sin s: T =", sp.simplify(T_of(phi_bh)), "; box phi - 2 phi =", sp.simplify(box(phi_bh) - 2 * phi_bh))
phi_st = phi0 * (1 + (sp.pi / 2 - s) * sp.cot(s))
print("static dilaton: box phi - 2 phi =", sp.simplify(box(phi_st) - 2 * phi_st), "(0 => traceless matter)")
T = T_of(phi_st)
trace = sp.simplify(sum(gi[a, b] * T[a, b] for a in range(2) for b in range(2)))
print("trace g^ab T_ab =", trace)
# null ray t = t0 + s (right-moving); affine: k^mu = sin^2 s (1, 1) (k^t = 1 at s = pi/2); d lambda = ds / sin^2 s
k = sp.Matrix([sp.sin(s) ** 2, sp.sin(s) ** 2])
Tkk = sp.simplify((k.T * T * k)[0])
print("T_kk(s) =", Tkk)
integrand = sp.simplify(Tkk / sp.sin(s) ** 2)
anec = sp.simplify(sp.integrate(integrand, (s, 0, sp.pi)))
print("ANEC = int T_kk d lambda over s in (0, pi) =", anec)
phir = sp.symbols("phi_r", positive=True)
print("in terms of phi_r = phi0 pi/2:", sp.simplify(anec.subs(phi0, 2 * phir / sp.pi)))
num = sp.integrate(integrand.subs({phi0: 1, G: 1}), (s, 0, sp.pi))
print("numeric check (phi0 = G = 1):", sp.N(num), " vs closed form", sp.N(anec.subs({phi0: 1, G: 1})))
Tpp_conf = sp.simplify((sp.Matrix([1, 1]).T * T * sp.Matrix([1, 1]))[0] / 4)   # T_{++} in x+ = t + s, x- = t - s
I_conf = sp.simplify(sp.integrate(Tpp_conf * 2, (s, 0, sp.pi)))                 # dx+ = 2 ds along x- = const
print("conformal-coordinate integral int T_{++} dx^+ =", I_conf, "=", sp.simplify(I_conf.subs(phi0, 2 * phir / sp.pi)), "(phi_r form)")
print("throat value phi(pi/2) =", sp.simplify(phi_st.subs(s, sp.pi / 2)), "; T_kk sign at throat:", sp.sign(Tkk.subs({s: sp.pi / 2, phi0: 1, G: 1})))

print("\n=== 2. MMP energy minimisation (Q-10), hbar = c = 1 ===")
l, re, GN, q = sp.symbols("l r_e G_N q", positive=True)
E = re**3 / (GN * l**2) - q / (8 * l)
lmin = sp.solve(sp.diff(E, l), l)
print("dE/dl = 0 at l =", lmin, "; E_min =", sp.simplify(E.subs(l, lmin[0])), "; d2E/dl2 > 0:", sp.simplify(sp.diff(E, l, 2).subs(l, lmin[0])))

print("\n=== 3. 2D Casimir ANEC on a circle (c species, light-length L), hbar = c = 1 ===")
c_, L = sp.symbols("c L", positive=True)
Ttt = -sp.pi * c_ / (6 * L**2)       # ground-state energy density E0/L with E0 = -pi c/(6 L)
Tkk2 = 2 * Ttt                         # k = (1, 1), traceless static: T_kk = T_tt + T_xx = 2 T_tt
print("per loop: int T_kk dlambda =", sp.simplify(Tkk2 * L), "; total energy E0 =", -sp.pi * c_ / (6 * L))
print("E0 with c = q on L = pi l:", sp.simplify((-sp.pi * c_ / (6 * L)).subs({c_: q, L: sp.pi * l})), " vs MMP Casimir term -q/(8 l): ratio", sp.Rational(1, 6) / sp.Rational(1, 8))
print("complete null line wrapping the circle n times: ANEC = -n pi c/(3 L) -> -infinity; the line returns to its own spatial point, so it is chronal.")

print("\n=== 4. Achronality margins, one-sided constructions ===")
yr = 3.15576e7; ly = 9.4607e15; c = 299792458.0
ell = 3e3 * ly; re_mm = 0.05 * c
T_thru = math.pi * ell / c
print(f"MM worked example: pi l / c = {T_thru/yr:.4e} yr (pi r_e/c = {math.pi*re_mm/c:.4f} s traveller).")
for d_ly in (1.0, 1e2, 1e3, 2.99e3):
    T_ext = d_ly * ly / c
    print(f"  d = {d_ly:g} ly: T_thru - T_ext = {(T_thru - T_ext)/yr:.4e} yr > 0 -> throat geodesic chronal (exterior timelike curve links entry and exit events); T_thru/T_ext = {T_thru/T_ext:.3f}")
print("FGM 2019: t_min = d + logs > d -> T_thru - T_ext = logs > 0 -> chronal (marginal).")
print("Classical one-sided MT/Ellis with throat length l_thr and mouth separation d: chronal iff l_thr > d (static, Phi ~ 0).")
for lthr, d in ((2.0, 1.0e3), (1.0e3, 1.0)):
    print(f"  l_thr = {lthr:g} m, d = {d:g} m: T_thru - T_ext = {(lthr - d)/c:.3e} s -> {'achronal candidate (shortcut)' if lthr < d else 'chronal (long)'}")
