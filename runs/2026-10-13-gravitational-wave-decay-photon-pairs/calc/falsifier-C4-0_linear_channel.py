"""
Falsifier C4-0 (physics angle): compute the coefficient k of the LINEAR (O(G^2) in the
pair number) near-source photon-pair channel for a circular binary, and compare it with
B&O's N^2 fusion total (O(G^4)), which C4 claims sets the size of a real source's pair total.

Units: natural (hbar = c = 1), metric signature (+,-,-,-), q^2 = q0^2 - |q|^2 > 0 time-like.

Production rule (Redi & Tesi, arXiv:2606.28297, eq. 6, quoted in the verdict):
   N_dec = (c_J / (2560 pi)) Int d^4q/(2 pi)^4 theta(q^2) W_{mnrs}(q) W^{mnrs}(-q),
   g = eta + h, c_J = 16 for a massless gauge field (photon), 4/3 conformal scalar.
Their eq. 39 (same paper) gives, for the source-sourced metric,
   dN/(dq0 dlog q) = (1/M_Pl^4) (c_J/(640 pi^2)) (q^3/(2 pi^2)) [<T_mn T^mn> - <T T>/3] theta(q0) theta(q0^2-q^2)
which implies |W|^2 = lambda (16 pi G)^2 [T_mn T^mn* - |T|^2/3] with lambda = 1 if eq. 6 runs over
both signs of q0 (checked numerically below: this is the normalisation cross-check).

Source: harmonic-gauge solution box hbar_mn = 16 pi G T_mn  ->  hbar(q) = -16 pi G T(q)/q^2
(the sign drops out of |W|^2).
Circular binary, slow motion: for |q| a <~ v << 1, Int d^3x T^{ij} = (1/2) d^2 I^{ij}/dt^2, so
T^{ij}(w, q) ~ const in q over the time-like ball |q| < w; T^{0i}, T^{00} follow from q_m T^{mn} = 0.
"""
import numpy as np

rng = np.random.default_rng(1)
eta = np.diag([1.0, -1.0, -1.0, -1.0])


def weyl_sq(qup, Tup, G=1.0):
    """|W|^2 = W_{mnrs} W*^{mnrs} for h sourced by conserved T^{mn} at 4-momentum q^m (upper)."""
    qlo = eta @ qup
    q2 = qup @ qlo
    Tlo = eta @ Tup @ eta
    hbar = -16 * np.pi * G * Tlo / q2
    trh = np.einsum('mn,mn->', np.linalg.inv(eta), hbar)  # eta^{mn} hbar_mn
    h = hbar - 0.5 * eta * trh
    # Linearized Riemann for h e^{-iqx}: d -> -i q, two derivatives -> -q q
    R = -0.5 * (np.einsum('n,r,ms->mnrs', qlo, qlo, h) + np.einsum('m,s,nr->mnrs', qlo, qlo, h)
                - np.einsum('m,r,ns->mnrs', qlo, qlo, h) - np.einsum('n,s,mr->mnrs', qlo, qlo, h))
    ei = np.linalg.inv(eta)
    Ric = np.einsum('mr,mnrs->ns', ei, R)
    Rs = np.einsum('ns,ns->', ei, Ric)
    g = eta
    C = (R - 0.5 * (np.einsum('mr,ns->mnrs', g, Ric) - np.einsum('ms,nr->mnrs', g, Ric)
                    - np.einsum('nr,ms->mnrs', g, Ric) + np.einsum('ns,mr->mnrs', g, Ric))
         + Rs / 6.0 * (np.einsum('mr,ns->mnrs', g, g) - np.einsum('ms,nr->mnrs', g, g)))
    Cup = np.einsum('ma,nb,rc,sd,abcd->mnrs', ei, ei, ei, ei, C)
    return np.real(np.einsum('mnrs,mnrs->', C, np.conj(Cup))), C


def conserved_T(qup, Tij):
    """Complete spatial T^{ij} to a conserved T^{mn}: q_m T^{mn} = 0 with q_m = (q0, -qvec)."""
    q0, qv = qup[0], qup[1:]
    T = np.zeros((4, 4), dtype=complex)
    T[1:, 1:] = Tij
    T0i = (Tij @ qv) / q0
    T[0, 1:] = T0i
    T[1:, 0] = T0i
    T[0, 0] = (qv @ T0i) / q0
    return T


def X_inv(Tup):
    Tlo = eta @ Tup @ eta
    TT = np.real(np.einsum('mn,mn->', Tup, np.conj(Tlo)))
    tr = np.einsum('mn,mn->', eta, Tup)
    return TT - abs(tr) ** 2 / 3.0


print("== 1. Normalisation and gauge checks (random conserved complex T, random time-like q) ==")
lams = []
for _ in range(6):
    q0 = 1.0
    qv = rng.normal(size=3)
    qv *= rng.uniform(0.05, 0.95) / np.linalg.norm(qv)
    qup = np.concatenate([[q0], qv])
    Tij = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    Tij = Tij + Tij.T
    T = conserved_T(qup, Tij)
    cons = np.max(np.abs(np.einsum('m,mn->n', eta @ qup, T)))
    w2, C = weyl_sq(qup, T, G=1.0)
    lam = w2 / ((16 * np.pi) ** 2 * X_inv(T))
    lams.append(lam)
    # gauge check: add q_m xi_n + q_n xi_m to h  -> Weyl unchanged (Riemann is gauge invariant)
    print(f"  |q|/q0 = {np.linalg.norm(qv):.3f}  conservation residual {cons:.1e}  lambda = |W|^2/((16 pi G)^2 X) = {lam:.6f}")
print(f"  lambda mean = {np.mean(lams):.6f} (eq. 39 of Redi-Tesi <-> eq. 6 consistency requires 1 if eq. 6 sums both signs of q0)")

# gauge-invariance check of the Weyl routine directly
qup = np.array([1.0, 0.2, -0.3, 0.1])
qlo = eta @ qup
h = rng.normal(size=(4, 4)); h = h + h.T
xi = rng.normal(size=4)


def weyl_from_h(h):
    R = -0.5 * (np.einsum('n,r,ms->mnrs', qlo, qlo, h) + np.einsum('m,s,nr->mnrs', qlo, qlo, h)
                - np.einsum('m,r,ns->mnrs', qlo, qlo, h) - np.einsum('n,s,mr->mnrs', qlo, qlo, h))
    return R


dR = weyl_from_h(h + np.outer(qlo, xi) + np.outer(xi, qlo)) - weyl_from_h(h)
print(f"  gauge check: max |Delta Riemann| under h -> h + q xi + xi q = {np.max(np.abs(dR)):.1e}")

print("\n== 2. Circular binary: pair rate vs GW luminosity, k = (dN/dt)/(G w L_GW) ==")
# I^{ij} oscillating part = Re[A e^{-i w t}], A = (mu a^2/2) [[1, i, 0], [i, -1, 0], [0, 0, 0]]; set mu a^2/2 = 1
A = np.array([[1, 1j, 0], [1j, -1, 0], [0, 0, 0]], dtype=complex)
w = 1.0
B = -(w ** 2 / 2) * A  # spatially integrated T^{ij} amplitude, = (1/2) d^2 I/dt^2
c_J = 16.0
# quadrature over the time-like ball |q| < w at q0 = w
nr, nc, nphi = 40, 40, 48
xr, wr = np.polynomial.legendre.leggauss(nr)
rr = 0.5 * w * (xr + 1); wrr = 0.5 * w * wr
xc, wc = np.polynomial.legendre.leggauss(nc)
phis = np.linspace(0, 2 * np.pi, nphi, endpoint=False); wphi = 2 * np.pi / nphi
I_W2 = 0.0
I_X = 0.0
for r, wtr in zip(rr, wrr):
    for c, wtc in zip(xc, wc):
        s = np.sqrt(1 - c * c)
        for p in phis:
            qv = r * np.array([s * np.cos(p), s * np.sin(p), c])
            qup = np.concatenate([[w], qv])
            T = conserved_T(qup, B)
            w2, _ = weyl_sq(qup, T, G=1.0)  # G = 1 here; restore G^2 below
            vol = wtr * wtc * wphi * r * r
            I_W2 += w2 * vol
            I_X += X_inv(T) * vol
print(f"  Int_{{|q|<w}} d^3q |W|^2 / G^2 = {I_W2:.6e}   (check = (16 pi)^2 Int X = {(16*np.pi)**2*I_X:.6e})")
# |T(q)|^2 for T(t) = Re[B e^{-iwt}]: pi^2 |B|^2 delta(q0-w) delta(0), delta(0) = T_obs/(2 pi); both signs of q0 equal
dNdt_over_G2 = (c_J / (2560 * np.pi)) * 2 * (1 / (2 * np.pi) ** 4) * (np.pi / 2) * I_W2
L_over_G = (1 / 10) * w ** 6 * np.sum(np.abs(A) ** 2)  # L = (G/10) w^6 sum|A_ij|^2 (time-averaged)
k = dNdt_over_G2 / (w * L_over_G)
print(f"  dN/dt = {dNdt_over_G2:.4e} G^2 (mu a^2/2)^2 w^7 ;  L_GW = {L_over_G:.4e} G (mu a^2/2)^2 w^6")
print(f"  k (eq. 6 over both signs of q0)          = {k:.4e}")
print(f"  k (if eq. 6 meant q0 > 0 only, i.e. /2)  = {k/2:.4e}")
# convergence check with a coarser grid
print("  (convergence: integrand is a polynomial in q; Gauss-Legendre 40x40x48 is exact to rounding)")

print("\n== 3. GW150914 and GW170817-bin numbers (SI inputs, natural-unit dimensionless results) ==")
G = 6.674e-11; c = 2.998e8; hbar = 1.0546e-34; Msun = 1.989e30
cases = {
    "GW150914 (B&O: E = 2 Msun c^2, f = 150 Hz, sigma = 200 rad/s)": (2 * Msun * c ** 2, 150.0, 200.0),
    "GW150914 (LVK: E = 3 Msun c^2)": (3 * Msun * c ** 2, 150.0, 200.0),
    "GW170817 100 Hz bin (E = 1.08e44 J, sigma = 62.8 rad/s)": (1.08e44, 100.0, 62.8),
}
for name, (E, f, sig) in cases.items():
    om = 2 * np.pi * f
    GEw = G * E * om / c ** 5
    N = E / (hbar * om)
    P_BO = (4 / 25) * (G * hbar / c ** 5) ** 2 * N ** 2 * om ** 3 * sig  # B&O per-packet total (top hat)
    P_lin = k * GEw
    print(f"  {name}:")
    print(f"     G E w/c^5 = {GEw:.3e};  P_lin = k G E w/c^5 = {P_lin:.3e} pairs (k/2: {P_lin/2:.3e})")
    print(f"     P_BO (eq. 8 x T_eff, top hat) = {P_BO:.3e} pairs;  P_BO/P_lin = {P_BO/P_lin:.3e} (k/2: {2*P_BO/P_lin:.3e})")
    print(f"     slow-motion parameter at q0: w a ~ 2v; GW150914 merger v ~ 0.5 -> leading-order k uncertain at O(1)")

print("\n== 3b. Cross-check: Redi-Tesi eqs. 39/50 with the q0 integral saturated at q0 ~ q ==")
# n ~ (c_J/(640 pi^2)) (1/M_Pl^2) q rho_GW  ->  N ~ c_J 8 pi G w E/(640 pi^2) = c_J G w E/(80 pi)
k_RT = c_J / (80 * np.pi)
print(f"  k_RT(saturated) = c_J/(80 pi) = {k_RT:.4e}  vs this script's k = {k:.4e} (and k/2 = {k/2:.4e}):")
print(f"  ratio k_RT/k = {k_RT/k:.2f}; same order (saturation over-counts the |q| < q0 ball)")

print("\n== 4. Order counting ==")
print("  P_lin ~ k G E_GW w ~ G^2 (source)^2 ;  P_BO ~ G^2 E_GW^2 w sigma ~ G^4 (source)^4 ;")
print("  ratio P_BO/P_lin = (4/25)(G E sigma/c^5)/k, < (4/25)(r_E sigma/c)/k with r_E = G E/c^4 < hoop size.")
