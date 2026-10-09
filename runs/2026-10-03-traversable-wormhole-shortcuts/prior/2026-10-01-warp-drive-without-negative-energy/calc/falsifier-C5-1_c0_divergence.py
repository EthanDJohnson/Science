"""Falsifier C5-1: does Lentz's stated loophole (Eulerian energy density only C^0 on
planes x = 0, y = 0) evade the divergence identity for unit-lapse, flat-slice,
curl-free shifts?

Geometric units (G = c = 1). Shift X = grad(phi), N = 1, h_ij = delta_ij.
16 pi rho_E = (lap phi)^2 - phi_ij phi_ij  (SSV eq. 4.1 with K_ij = phi_ij).

Lentz (arXiv:2201.00652 p.6) argues the divergence theorem needs the total
divergence to be "at least first order smooth everywhere". Test: build phi that is
C^2 everywhere but whose third derivatives jump on x = 0 AND y = 0 (so rho_E is
C^0, exactly Lentz's regularity), and compute the bulk integral of rho_E split
into the four quadrants of (x, y). Also a C^1 case (phi_xx jumps) for contrast.
Separable phi = g(x) g(y) h(z) lets the 3D integral factor into 1D integrals,
each evaluated piecewise on (-inf, 0) and (0, inf) at 30 digits.
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 30
x, y, z = sp.symbols('x y z', real=True)
s = sp.Symbol('s', real=True)


def run(label, g_minus, g_plus, hz):
    # g piecewise in s: g_minus for s<0, g_plus for s>0
    # 16 pi rho = (lap)^2 - sum phi_ij^2 for phi = G(x) G(y) H(z)
    # Write phi_ij in terms of 1D derivative symbols, expand, integrate termwise.
    G0, G1, G2 = sp.symbols('G0 G1 G2')  # placeholders for x-factor derivs
    F0, F1, F2 = sp.symbols('F0 F1 F2')  # y-factor
    H0, H1, H2 = sp.symbols('H0 H1 H2')  # z-factor
    lap = G2*F0*H0 + G0*F2*H0 + G0*F0*H2
    hess = [[G2*F0*H0, G1*F1*H0, G1*F0*H1],
            [G1*F1*H0, G0*F2*H0, G0*F1*H1],
            [G1*F0*H1, G0*F1*H1, G0*F0*H2]]
    expr = sp.expand(lap**2 - sum(hess[i][j]**2 for i in range(3) for j in range(3)))
    # 1D integrals of monomials Gi*Gj over half-lines
    def half_int(gexpr, a, b, i, j):
        di = sp.diff(gexpr, s, i)
        dj = sp.diff(gexpr, s, j)
        f = sp.lambdify(s, di*dj, 'mpmath')
        return mp.quad(f, [a, b])
    hz_ = hz
    def full_int_h(i, j):
        f = sp.lambdify(s, sp.diff(hz_, s, i)*sp.diff(hz_, s, j), 'mpmath')
        return mp.quad(f, [-mp.inf, 0, mp.inf])
    halves = {'-': (g_minus, -mp.inf, 0), '+': (g_plus, 0, mp.inf)}
    total = mp.mpf(0)
    print(f"--- {label} ---")
    # check continuity of g and its derivatives at 0
    for k in range(4):
        jm = sp.limit(sp.diff(g_minus, s, k), s, 0, '-')
        jp = sp.limit(sp.diff(g_plus, s, k), s, 0, '+')
        print(f"  jump in g^({k}) at 0: {sp.simplify(jp - jm)}")
    for sx in '-+':
        for sy in '-+':
            q = mp.mpf(0)
            for term in expr.as_ordered_terms():
                coeff, mon = term.as_coeff_Mul()
                powsG = [mon.as_powers_dict().get(Gk, 0) for Gk in (G0, G1, G2)]
                powsF = [mon.as_powers_dict().get(Fk, 0) for Fk in (F0, F1, F2)]
                powsH = [mon.as_powers_dict().get(Hk, 0) for Hk in (H0, H1, H2)]
                def idx(p):
                    l = []
                    for k, n in enumerate(p):
                        l += [k]*n
                    return l
                gi, fi, hi = idx(powsG), idx(powsF), idx(powsH)
                assert len(gi) == len(fi) == len(hi) == 2
                ge, a, b = halves[sx]
                fe, c, d = halves[sy]
                q += mp.mpf(float(coeff)) * half_int(ge, a, b, *gi) * half_int(fe, c, d, *fi) * full_int_h(*hi)
            print(f"  quadrant x{sx} y{sy}: integral of 16*pi*rho_E = {mp.nstr(q, 12)}")
            total += q
    print(f"  TOTAL integral of 16*pi*rho_E over R^3 = {mp.nstr(total, 6)}")
    return total


h = sp.exp(-s**2)
# Case A (Lentz regularity): g in C^2, g''' jumps at 0 -> rho_E continuous, not C^1
a = sp.Rational(3, 2)
gA_m = sp.exp(-s**2)*(1 + s/2)
gA_p = sp.exp(-s**2)*(1 + s/2 + a*s**3)
run("Case A: phi C^2, third derivative jumps on x=0 and y=0 (rho_E C^0)", gA_m, gA_p, h)
# Case B: g in C^1, g'' jumps -> rho_E itself jumps
bq = sp.Rational(2, 1)
gB_m = sp.exp(-s**2)*(1 + s/2)
gB_p = sp.exp(-s**2)*(1 + s/2 + bq*s**2)
run("Case B: phi C^1, second derivative jumps (rho_E discontinuous)", gB_m, gB_p, h)
print("Conclusion check: quadrant pieces are nonzero (see above) yet the total is 0 to working precision,")
print("so a C^0 (or even discontinuous) rho_E does not evade int rho_E = 0; positivity")
print("everywhere would force rho_E = 0 almost everywhere.")
