#!/usr/bin/env python3
"""Task C(3): dimensions and hbar counting of B&O eqs. 8, 9, 10, 11, 12 and the S6/C1 total P_tot; is N^2 just classical h^4?

Method: exponent bookkeeping in SI base units (kg, m, s).  Natural-unit symbols are converted with
   G_nat = G/(hbar c^5)  [J^-2],   w_s = hbar w,  sig_w = hbar delta  [J],   time t_nat = t/hbar [J^-1],   N = E_rel/(hbar w).
For each B&O formula we (i) find the unique hbar, c exponents that make it dimensionally consistent in SI (independent of B&O's
own restoration) and (ii) convert the natural-unit expression and read off the hbar power at FIXED CLASSICAL inputs
(E_rel, w, delta, G, c).  Then (iii) the classical-field check: express P_tot through the classical strain amplitude with B&O's
own flux relation  E_rel sig_w/(4 pi r^2) = w_s^2 h_r^2/(32 pi G)  and verify P_tot ∝ h_r^4 with no hbar.
"""
import sympy as sp

hb, c, G, E, w, d, t, r, h = sp.symbols("hbar c G E omega delta t r h", positive=True)
# SI dimensions as (kg, m, s) exponent vectors
dims = {hb: (1, 2, -1), c: (0, 1, -1), G: (-1, 3, -2), E: (1, 2, -2), w: (0, 0, -1), d: (0, 0, -1), t: (0, 0, 1),
        r: (0, 1, 0), h: (0, 0, 0)}


def dim(expr):
    expr = sp.powsimp(sp.expand_power_base(sp.factor(expr), force=True), force=True)
    v = [0, 0, 0]
    for b, e in expr.as_powers_dict().items():
        if b in dims:
            for i in range(3):
                v[i] += e * dims[b][i]
    return tuple(sp.nsimplify(x) for x in v)


Gn = G / (hb * c ** 5)          # natural-unit Newton constant, J^-2
ws, sg = hb * w, hb * d         # energies
N = E / (hb * w)

print("=" * 100)
print("(i)+(ii) SI restoration and hbar power at fixed classical (E_rel, w, delta)")
print("=" * 100)
cases = {
    "eq.8  dP/dt  [pairs per J^-1 -> per s: multiply by 1/hbar]": (3 * Gn ** 2 * N ** 2 * ws ** 3 * sg ** 2 / (25 * sp.pi)) / hb,
    "eq.9  N_gamma(t), t in s (t_nat = t/hbar)": Gn ** 2 * N ** 2 * 6 * ws ** 3 * sg ** 2 * (t / hb) / (25 * sp.pi),
    "eq.10 tau [s] (= hbar x natural)": hb * 25 * sp.pi / (6 * Gn ** 2 * E ** 2 * ws * sg ** 2),
    "eq.11 W_gamma [W] (energy per natural time / hbar)": 6 * Gn ** 2 * E ** 2 * ws ** 2 * sg ** 2 / (25 * sp.pi) / hb,
    "C1    P_tot [pairs, whole history]": sp.Rational(4, 25) * Gn ** 2 * N ** 2 * ws ** 3 * sg,
}
targets = {"eq.8": (0, 0, -1), "eq.9": (0, 0, 0), "eq.10": (0, 0, 1), "eq.11": (1, 2, -3), "C1  ": (0, 0, 0)}
for name, ex in cases.items():
    ex = sp.simplify(ex)
    p_hb = sp.degree(sp.powsimp(ex), hb) if ex.has(hb) else 0
    p_hb = sp.Poly(ex * hb ** 20, hb).degree() - 20 if ex.has(hb) else 0
    print(f"   {name}:\n      SI form = {ex}\n      dims (kg,m,s) = {dim(ex)};  hbar power at fixed E,w,delta = {p_hb}")
B_eq11 = 6 * G ** 2 * hb * E ** 2 * w ** 2 * d ** 2 / (25 * sp.pi * c ** 10)
print(f"   B&O's own SI form of eq.11, 6 G^2 hbar E^2 w^2 delta^2/(25 pi c^10): dims = {dim(B_eq11)} (watt = (1, 2, -3));"
      f"  minus our conversion = {sp.simplify(B_eq11 - cases['eq.11 W_gamma [W] (energy per natural time / hbar)'])}")
# unique (x, y) with G^2 E^2 w^2 d^2 hbar^x c^y = watt
x, y = sp.symbols("x y")
base = dim(G ** 2 * E ** 2 * w ** 2 * d ** 2)
sol = sp.solve([base[0] + x - 1, base[1] + 2 * x + y - 2, base[2] - x - y + 3], [x, y], dict=True)
print(f"   unique exponents making G^2 E^2 w^2 delta^2 hbar^x c^y a power: {sol}")

print("\n   eq.12: W = (3/(50 pi)) (r_m/l)^2 hbar w^2 with r_m = 2 G E/c^4, l = c dt.  Equal to eq.11 iff dt = 1/delta:")
dt = sp.symbols("dt", positive=True)
eq12 = sp.Rational(3, 50) / sp.pi * (2 * G * E / c ** 4 / (c * dt)) ** 2 * hb * w ** 2
print(f"      eq.12/eq.11 = {sp.simplify(eq12 / B_eq11)}   -> = 1 for dt = 1/delta (B&O's 'dt ~ 1/sigma' taken as an equality)")

print("\n" + "=" * 100)
print("(iii) classical-field content: photon PAIRS and photon NUMBER rate are hbar-free at fixed classical wave")
print("=" * 100)
for name, ex in [("eq.8 dP/dt", cases["eq.8  dP/dt  [pairs per J^-1 -> per s: multiply by 1/hbar]"]),
                 ("C1 P_tot", cases["C1    P_tot [pairs, whole history]"])]:
    print(f"   {name} = {sp.simplify(ex)}   (hbar-free: a pure function of the classical wave E_rel, w, delta)")
print("   => W_gamma = hbar w x (hbar-free pair rate x 2): the single hbar is the photon quantum hbar w, as B&O say; the graviton")
print("      count N enters only through N hbar w = E_rel, so 'N^2' is (E_rel/(hbar w))^2 compensated by G_nat^2 = G^2/(hbar c^5)^2.")
# strain: E sig/(4 pi r^2) = ws^2 h^2/(32 pi G_nat)  (natural units)  -> SI
hs = sp.solve(sp.Eq(E * sg / (4 * sp.pi * r ** 2), ws ** 2 * h ** 2 / (32 * sp.pi * Gn) / (hb * c) ** 0), h)
# check dims of that relation in SI: LHS J^2/m^2 ... do it in natural units then convert r_nat = r/(hbar c)
rn = r / (hb * c)
hsq = sp.solve(sp.Eq(E * sg / (4 * sp.pi * rn ** 2), ws ** 2 * h ** 2 / (32 * sp.pi * Gn)), h ** 2)
hsq = [sp.simplify(sp.solve(sp.Eq(E * sg / (4 * sp.pi * rn ** 2), ws ** 2 * sp.Symbol("H") / (32 * sp.pi * Gn)),
                            sp.Symbol("H"))[0])][0]
print(f"   B&O flux relation -> h_r^2 = {hsq}  (dims {dim(hsq)}: dimensionless, hbar-free, = 8 G E delta/(c^3 r^2 w^2))")
Ptot = sp.simplify(cases["C1    P_tot [pairs, whole history]"])
ratio = sp.simplify(Ptot / hsq ** 2)
print(f"   P_tot / h_r^4 = {ratio}   (dims {dim(ratio)}; hbar-free) -> P_tot = (1/400) (h_r^2)^2 (w r/c)^4 (w/delta)")
print(f"   check: {sp.simplify(Ptot - hsq**2 * w**4 * r**4 / (400 * c**4) * w / d)}")
print("   So the in-out pair number is a quartic functional of the CLASSICAL strain with no hbar: the 'N^2 coherent enhancement'")
print("   is identical to (classical h)^4 rewritten in graviton units; nothing beyond the classical second-order field squared.")

print("\n" + "=" * 100)
print("(iv) N^2 is not specific to coherence: B&O eq. 14 for the (incoherent, Gaussian P-function) background is")
print("     dP/dtdV = 8 pi G^2 rho^2/15, also quadratic in graviton number.  Rewrite eq. 8 per volume with rho = N w/V:")
V = sp.symbols("V", positive=True)
Nn, wn, sn, Gs = sp.symbols("N w_s sigma_w G_N", positive=True)
eq8 = 3 * Gs**2 * Nn**2 * wn**3 * sn**2 / (25 * sp.pi)
eq14V = 8 * sp.pi * Gs**2 * (Nn * wn / V)**2 / 15 * V
rr = sp.simplify(eq8 / eq14V)
print(f"     eq.8 / (eq.14 x V) = {rr}   -> equal when V w sig^2 = {sp.simplify(sp.solve(sp.Eq(rr,1),V)[0]*wn*sn**2)}"
      "  (B&O: 'V w sig^2 -> 40 pi^2/9')")
print("     So the 'coherent enhancement' is a smaller effective volume (higher peak h^2 at the focus), i.e. the")
print("     classical spatial concentration of h^4, not an extra power of N.")
print("=" * 100)
