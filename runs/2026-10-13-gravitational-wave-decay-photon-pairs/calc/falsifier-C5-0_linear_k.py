"""Falsifier C5-0 (physics): compute the linear-channel coefficient k that C5 leaves uncomputed.

Process: a classical matter/field source with stress tensor T^{mu nu}(x) emits an off-shell graviton
of time-like momentum q (q^2 = -m^2 < 0 in signature -+++, i.e. invariant mass m) which converts to
two photons.  Amplitude linear in h (so yield linear in N = E_GW/(hbar w)).

Natural units hbar = c = 1, Heaviside-Lorentz; g = eta + h, kappa^2 = 32 pi G (canonical graviton,
coupling -(kappa/2) h_{mu nu} T^{mu nu}).

Route A (explicit amplitudes):  P = Int d^4q/(2pi)^4 theta(q0) theta(m^2) (kappa^2/(2 m^3)) Gamma(m) |T^TT(q)|^2
   with Gamma(m) = width of a spin-2 state of mass m -> gamma gamma for coupling kappa/2 (computed below
   from explicit Maxwell stress-tensor matrix elements, expected kappa^2 m^3/(320 pi)).
Route B (Redi-Tesi, dossier D-60): N = (c_J/(2560 pi)) Int d^4q/(2pi)^4 theta(q^2) W(q).W(-q), c_J = 16,
   with W the linearised Weyl tensor of h^TT = 16 pi G T^TT/m^2 (computed below).
Both must give P = A G^2 Int d^4q/(2pi)^4 theta(q0)theta(m^2) |T^TT|^2.

Then k := Pdot_pairs / (G w P_GW) for a quadrupole (long-wavelength) source at frequency w, with
P_GW computed in the same Fourier convention (checked against 32/5 G mu^2 a^4 Omega^6).
"""
import numpy as np
import itertools

eta = np.diag([-1.0, 1.0, 1.0, 1.0])

# ---------------------------------------------------------------- Part 1: Gamma(spin-2 -> gamma gamma)
def F_low(k_up, e_up):
    """F_{mu nu} (lower) for outgoing photon: i(k_mu e_nu - k_nu e_mu) with conjugated pol (real here)."""
    k = eta @ k_up
    e = eta @ e_up
    return 1j * (np.outer(k, e) - np.outer(e, k))

def T_matrix_element(k1, e1, k2, e2):
    """<gamma(k1,e1) gamma(k2,e2)| T^{mu nu} |0>, T = F^{mu a}F^nu_a - 1/4 eta F^2 (upper indices)."""
    F1, F2 = F_low(k1, e1), F_low(k2, e2)
    F1u = eta @ F1 @ eta   # F^{mu nu}
    F2u = eta @ F2 @ eta
    # F^{mu a} F^{nu}_a = F^{mu a} F^{nu b} eta_{ab}
    term = F1u @ eta @ F2u.T + F2u @ eta @ F1u.T
    F1F2 = np.sum(F1 * F2u)  # F1_{ab} F2^{ab}
    etainv = eta  # eta^{mu nu} = eta numerically
    return term - 0.5 * etainv * F1F2

def spin2_basis():
    """Orthonormal real symmetric traceless 3x3 basis (5 elements), sum eps_ij^2 = 1."""
    B = []
    s2 = np.sqrt(2.0)
    for (i, j) in [(0, 1), (0, 2), (1, 2)]:
        M = np.zeros((3, 3)); M[i, j] = M[j, i] = 1 / s2; B.append(M)
    M = np.diag([1, -1, 0]) / s2; B.append(M)
    M = np.diag([1, 1, -2]) / np.sqrt(6); B.append(M)
    return B

def width_spin2_to_gg(m=1.0, kappa=1.0, nth=40, nph=80):
    B = spin2_basis()
    xs, ws = np.polynomial.legendre.leggauss(nth)
    phs = (np.arange(nph) + 0.5) * 2 * np.pi / nph
    widths = []
    for eps3 in B:
        eps = np.zeros((4, 4)); eps[1:, 1:] = eps3
        tot = 0.0
        for c, w in zip(xs, ws):
            s = np.sqrt(1 - c * c)
            for ph in phs:
                n = np.array([s * np.cos(ph), s * np.sin(ph), c])
                k1 = np.concatenate([[m / 2], m / 2 * n]); k2 = np.concatenate([[m / 2], -m / 2 * n])
                # transverse basis for n
                a = np.array([1.0, 0, 0]) if abs(n[0]) < 0.9 else np.array([0, 1.0, 0])
                p1 = np.cross(n, a); p1 /= np.linalg.norm(p1); p2 = np.cross(n, p1)
                pols = [np.concatenate([[0], p1]), np.concatenate([[0], p2])]
                msq = 0.0
                for e1 in pols:
                    for e2 in pols:
                        M = T_matrix_element(k1, e1, k2, e2)
                        amp = (kappa / 2) * np.sum(eps * M)  # eps_{mu nu} M^{mu nu}, eps spatial
                        msq += abs(amp) ** 2
                tot += w * (2 * np.pi / nph) * msq
        # dPhi_2 = dOmega/(32 pi^2) for massless; 1/2 identical photons; Gamma = (1/2m) Int dPhi 1/2 |M|^2
        widths.append(tot / (32 * np.pi ** 2) * 0.5 / (2 * m))
    return np.array(widths)

G1 = width_spin2_to_gg()
print("Part 1: Gamma(spin-2, m=1 -> gamma gamma), coupling kappa/2 with kappa=1, each of 5 pols:")
print("   ", np.round(G1, 8))
print("   expected kappa^2 m^3/(320 pi) =", 1 / (320 * np.pi))
print("   ratio computed/expected =", G1.mean() * 320 * np.pi)
c_gam = G1.mean()

# Route A coefficient: P = Int (kappa^4/16 m^4) * [Int dPhi 1/2 M M*] |T^TT|^2 ; Int dPhi 1/2 |eps.M|^2 = 2 m Gamma/(kappa^2/4)
# => integrand = kappa^2 Gamma/(2 m^3) |T^TT|^2 = kappa^4 c_gam/2 |T^TT|^2 (Gamma = c_gam kappa^2 m^3)
kappa2_over_G = 32 * np.pi
A_routeA = (kappa2_over_G ** 2) * c_gam / 2
print("Route A: P = A G^2 Int d4q/(2pi)^4 th(q0)th(m^2)|T^TT|^2,  A =", A_routeA, " (8 pi/5 =", 8 * np.pi / 5, ")")

# ---------------------------------------------------------------- Part 2: Redi-Tesi route
def lin_riemann(hq, q):
    """Linearised Riemann R_{mu nu rho sigma} for h_{mu nu} e^{i q.x}, d_mu -> i q_mu (q lower)."""
    R = np.zeros((4, 4, 4, 4), dtype=complex)
    for m_, n_, r_, s_ in itertools.product(range(4), repeat=4):
        R[m_, n_, r_, s_] = 0.5 * (-(q[n_] * q[r_]) * hq[m_, s_] - (q[m_] * q[s_]) * hq[n_, r_]
                                    + (q[m_] * q[r_]) * hq[n_, s_] + (q[n_] * q[s_]) * hq[m_, r_])
    return R

def weyl(R):
    g = eta  # lower-index metric
    gi = eta
    Ric = np.einsum('ab,ambn->mn', gi, R)
    Rs = np.einsum('mn,mn->', gi, Ric)
    C = R.copy()
    for a, b, c, d in itertools.product(range(4), repeat=4):
        C[a, b, c, d] -= 0.5 * (g[a, c] * Ric[b, d] - g[a, d] * Ric[b, c] - g[b, c] * Ric[a, d] + g[b, d] * Ric[a, c])
        C[a, b, c, d] += Rs / 6 * (g[a, c] * g[b, d] - g[a, d] * g[b, c])
    return C

def contract_full(C1, C2):
    up = np.einsum('ae,bf,cg,dh,efgh->abcd', eta, eta, eta, eta, C2)
    return np.sum(C1 * up)

rng = np.random.default_rng(1)
m = 1.0
qlow = np.array([-m, 0, 0, 0])  # q_mu lower for q^mu = (m,0,0,0)
ratios = []
for trial in range(4):
    A = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3)); A = A + A.T; A -= np.trace(A) / 3 * np.eye(3)
    h = np.zeros((4, 4), dtype=complex); h[1:, 1:] = A
    C = weyl(lin_riemann(h, qlow))
    Cm = weyl(lin_riemann(np.conj(h), -qlow))  # W(-q) of a real field = conj
    WW = contract_full(C, Cm).real
    ratios.append(WW / (m ** 4 * np.sum(abs(A) ** 2)))
print("Part 2: W(q).W(-q) / (m^4 |h^TT|^2) for random TT h at rest-frame time-like q:", np.round(ratios, 10))
WWfac = np.mean(ratios)
cJ = 16.0
# theta(q^2) in RT covers q0>0 and q0<0 (factor 2 vs theta(q0)); h^TT = 16 pi G T^TT/m^2
A_routeB = cJ / (2560 * np.pi) * 2 * WWfac * (16 * np.pi) ** 2
print("Route B (Redi-Tesi, c_J=16): A =", A_routeB, "  ratio B/A =", A_routeB / A_routeA)

# ---------------------------------------------------------------- Part 3: k for a quadrupole source
def F_offshell(S, qvec, w):
    """|T^TT|^2 = T.T* - |tr T|^2/3 for conserved T with T^ij = S (long-wavelength), q=(w,qvec)."""
    T = np.zeros((4, 4), dtype=complex)
    T[1:, 1:] = S
    T[0, 1:] = T[1:, 0] = S @ qvec / w
    T[0, 0] = qvec @ S @ qvec / w ** 2
    Tl = eta @ T @ eta
    TT = np.sum(Tl * np.conj(T)).real
    tr = np.sum(np.diag(eta) * np.diag(T))
    return TT - abs(tr) ** 2 / 3

def Lambda_onshell(S, n):
    P = np.eye(3) - np.outer(n, n)
    ST = P @ S @ P
    ST = ST - 0.5 * P * np.trace(ST)
    return np.sum(abs(ST) ** 2)

w = 1.0
S_circ = np.array([[1, 1j, 0], [1j, -1, 0], [0, 0, 0]], dtype=complex)
S_lin = np.diag([-0.5, -0.5, 1.0]).astype(complex)
nu, nth, nph = 24, 48, 96
us, uw = np.polynomial.legendre.leggauss(nu); us = 0.5 * (us + 1); uw = 0.5 * uw
cs, cw = np.polynomial.legendre.leggauss(nth)
phs = (np.arange(nph) + 0.5) * 2 * np.pi / nph; dph = 2 * np.pi / nph
for name, S in [("circular binary", S_circ), ("linear quadrupole", S_lin)]:
    ball = 0.0; sph = 0.0
    for c, wc in zip(cs, cw):
        s = np.sqrt(1 - c * c)
        for ph in phs:
            n = np.array([s * np.cos(ph), s * np.sin(ph), c])
            sph += wc * dph * Lambda_onshell(S, n)
            for u, wu in zip(us, uw):
                ball += wc * dph * wu * u ** 2 * w ** 3 * F_offshell(S, u * w * n, w)
    S2 = np.sum(abs(S) ** 2)
    # Pdot_pairs = A G^2 Int d3q/(2pi)^3 |T^TT|^2 ; P_GW = (kappa^2/4)(w^2/(8 pi^2)) Int dOmega Lambda = (G w^2/pi) Int dOmega Lambda
    Pdot_over_G2 = A_routeA * ball / (2 * np.pi) ** 3
    PGW_over_G = w ** 2 / np.pi * sph
    k = Pdot_over_G2 / (w * PGW_over_G)
    print(f"Part 3 [{name}]: Int_ball F d3q /(w^3 |S|^2) = {ball / S2:.6f} (closed form 4pi*67/315 = {4 * np.pi * 67 / 315:.6f});"
          f" Int dOmega Lambda/|S|^2 = {sph / S2:.6f} (8pi/5 = {8 * np.pi / 5:.6f})")
    print(f"   k = Pdot_pairs/(G w P_GW) = {k:.6f}   closed form 67/(630 pi) = {67 / (630 * np.pi):.6f}")

# P_GW normalisation check: circular binary, T^ij(t) = Re[S e^{-iwt}], S = (1/2)(-w^2) I_hat, I_hat = (mu a^2/2)[[1,i],[i,-1]]
mu_, a_, Om = 1.0, 1.0, 1.0
wgw = 2 * Om
Ihat = mu_ * a_ ** 2 / 2 * np.array([[1, 1j, 0], [1j, -1, 0], [0, 0, 0]])
S = 0.5 * (-wgw ** 2) * Ihat
That = S / 2  # positive-frequency Fourier amplitude
sph = 0.0
for c, wc in zip(cs, cw):
    s = np.sqrt(1 - c * c)
    for ph in phs:
        sph += wc * dph * Lambda_onshell(That, np.array([s * np.cos(ph), s * np.sin(ph), c]))
PGW = wgw ** 2 / np.pi * sph  # in units of G
print("P_GW normalisation check: computed/(32/5 G mu^2 a^4 Omega^6) =", PGW / (32 / 5))

# ---------------------------------------------------------------- Part 4: sizes (SI)
k = 67 / (630 * np.pi)
G, c = 6.674e-11, 2.998e8
Msun = 1.989e30
LP = c ** 5 / G
print("\nPart 4 (SI). k =", k, "; required by C5 for GW150914: k >~ 3.15e-4 ; k/3.15e-4 =", k / 3.15e-4)
# M-EXAMINER-09 inputs: P_lin/k = 9.27e-3 (GW150914), 1.87e-6 (GW170817 100 Hz bin); P_BO = 2.92e-6, 5.60e-14
for name, PlinK, PBO in [("GW150914 (E=2 Msun c^2, 150 Hz)", 9.27e-3, 2.92e-6), ("GW170817 100 Hz bin", 1.87e-6, 5.60e-14)]:
    print(f"  {name}: P_lin = {k * PlinK:.3e} pairs vs N^2 fusion P_BO = {PBO:.3e}; P_lin/P_BO = {k * PlinK / PBO:.3e}")
# profile-free comparison: P_BO = (12 pi/25) G^2 w Int L^2 dt / c^10 ; P_lin = k G w Int L dt / c^5
Lpk = 3.6e49
print("  L_Planck = c^5/G =", f"{LP:.3e} W; GW150914 L_peak/L_P = {Lpk / LP:.3e}")
print("  fusion/linear = (12 pi/(25 k)) * G <L>_L / c^5 <= ", f"{12 * np.pi / (25 * k):.2f} * L_peak/L_P = {12 * np.pi / (25 * k) * Lpk / LP:.3e}")
print("  fusion would need <L>_L > ", f"{25 * k / (12 * np.pi):.3e} L_P = {25 * k / (12 * np.pi) * LP:.3e} W to beat the linear channel")
# inspiral-only illustration (assumed inputs, labelled): E_insp ~ 1 Msun c^2 radiated below f_GW ~ 50 Hz (conservative low w)
E_insp, f_insp = 1.0 * Msun * c ** 2, 50.0
P_insp = k * G * 2 * np.pi * f_insp * E_insp / c ** 5
print(f"  inspiral-only illustration (assumed E = 1 Msun c^2 at f = 50 Hz): P_lin = {P_insp:.3e} pairs = {P_insp / 2.92e-6:.1f} x whole-event fusion P_BO")
