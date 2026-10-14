"""Falsifier C5-1: compute the linear-channel coefficient k that C5 leaves uncomputed.

Natural units hbar = c = 1 (G kept explicit, set G = 1 inside the ratio), signature (-,+,+,+).

Linear channel: classical source T^{mu nu}(q) -> one off-shell graviton (q^2 < 0 in mostly-plus,
i.e. time-like) -> photon pair.  Yield from Redi & Tesi arXiv:2606.28297 eq. (6):
   N = (c_J/(2560 pi)) Int d^4q/(2pi)^4 theta(time-like) W(q).W(-q),  c_J = 16 for a gauge field,
integral over both signs of q0.
Step 1 checks numerically that, for h-bar_{mu nu} = 16 pi G T_{mu nu}/q^2 (harmonic gauge, conserved T),
   W.W* = (1/2)(16 pi G)^2 (T.T* - |T^mu_mu|^2/3)
so N = (8 pi/5) G^2 Int_{q0>0, time-like} d^4q/(2pi)^4 (T.T* - |T|^2/3).
Step 2 fixes the graviton-number normalisation dN_GW/dt = (G w/pi) Int dOmega (T.T* - |T|^2/2)
by reproducing the quadrupole luminosity of a circular binary.
Step 3 computes k = (dN_lin/dt)/(G w^2 dN_GW/dt) for a circular binary (long-wavelength source,
|q| a << 1) and for a linear (head-on/oscillating) quadrupole.
Step 4 compares with C5's threshold k >~ 3.2e-4 (GW150914) and with Rahvar 2026 (arXiv:2606.17178),
whose scalar linear-order power P_dyn = A (M/Msun)^(10/3) (f/100 Hz)^(16/3), A ~ 1e-30 erg/s.
"""
import numpy as np

rng = np.random.default_rng(1)
eta = np.diag([-1.0, 1.0, 1.0, 1.0])


def conserved_T(Tij, q0, qv):
    """Upper-index T^{mu nu} from spatial T^{ij} using q_mu T^{mu nu} = 0 (mostly plus)."""
    T = np.zeros((4, 4), dtype=complex)
    T[1:, 1:] = Tij
    T0j = (qv @ Tij) / q0
    T[0, 1:] = T0j
    T[1:, 0] = T0j
    T[0, 0] = (qv @ Tij @ qv) / q0**2
    return T


def contract2(A, B):
    """A^{mu nu} B*^{mu nu} with indices lowered by eta."""
    return np.einsum('ab,cd,ac,bd->', eta, eta, A, np.conj(B))


def trace(T):
    return np.einsum('ab,ab->', eta, T)


def weyl_sq(Tup, qup):
    """Linearised Weyl^2 for h-bar = 16 pi T / q^2 (G = 1)."""
    ql = eta @ qup
    q2 = qup @ eta @ qup
    Tl = eta @ Tup @ eta
    hb = 16 * np.pi * Tl / q2
    trhb = np.einsum('ab,ab->', np.linalg.inv(eta), hb)
    h = hb - 0.5 * eta * trhb
    # Riemann R_{mnrs} = 1/2 (d_n d_r h_ms + d_m d_s h_nr - d_m d_r h_ns - d_n d_s h_mr), d -> i q
    q = ql
    R = 0.5 * (-np.einsum('n,r,ms->mnrs', q, q, h) - np.einsum('m,s,nr->mnrs', q, q, h)
               + np.einsum('m,r,ns->mnrs', q, q, h) + np.einsum('n,s,mr->mnrs', q, q, h))
    gi = np.linalg.inv(eta)
    Ric = np.einsum('ac,abcd->bd', gi, R)
    Rs = np.einsum('bd,bd->', gi, Ric)
    g = eta
    W = (R - 0.5 * (np.einsum('mr,ns->mnrs', g, Ric) - np.einsum('ms,nr->mnrs', g, Ric)
                    - np.einsum('nr,ms->mnrs', g, Ric) + np.einsum('ns,mr->mnrs', g, Ric))
         + Rs / 6 * (np.einsum('mr,ns->mnrs', g, g) - np.einsum('ms,nr->mnrs', g, g)))
    Wup = np.einsum('ma,nb,rc,sd,abcd->mnrs', gi, gi, gi, gi, W)
    return np.einsum('mnrs,mnrs->', W, np.conj(Wup)).real


print("=== Step 1: Weyl^2 identity at random time-like q (G = 1) ===")
for i in range(4):
    q0 = 1.0
    qv = rng.normal(size=3)
    qv *= rng.uniform(0.05, 0.95) / np.linalg.norm(qv)
    Tij = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    Tij = Tij + Tij.T
    Tup = conserved_T(Tij, q0, qv)
    qup = np.array([q0, *qv])
    lhs = weyl_sq(Tup, qup)
    rhs = 0.5 * (16 * np.pi)**2 * (contract2(Tup, Tup) - abs(trace(Tup))**2 / 3).real
    print(f"|q|/q0 = {np.linalg.norm(qv):.3f}: W.W* = {lhs:.6e}, (1/2)(16pi)^2(TT*-|T|^2/3) = {rhs:.6e}, ratio = {lhs/rhs:.10f}")
cJ = 16.0
coef = cJ / (2560 * np.pi) * 2 * 0.5 * (16 * np.pi)**2
print(f"Redi-Tesi coefficient (c_J=16, both q0 signs, q0>0 kept): {coef:.6f}  vs 8 pi/5 = {8*np.pi/5:.6f}")


def F_on(A, q0, n):
    T = conserved_T(A, q0, q0 * n)
    return (contract2(T, T) - 0.5 * abs(trace(T))**2).real


def F_off(A, q0, qv):
    T = conserved_T(A, q0, qv)
    return (contract2(T, T) - abs(trace(T))**2 / 3).real


def sphere_avg(f, nth=48, nph=48):
    x, w = np.polynomial.legendre.leggauss(nth)
    phis = (np.arange(nph) + 0.5) * 2 * np.pi / nph
    tot = 0.0
    for ct, wt in zip(x, w):
        st = np.sqrt(1 - ct**2)
        for ph in phis:
            tot += wt * f(np.array([st * np.cos(ph), st * np.sin(ph), ct]))
    return tot * (2 * np.pi / nph)  # = Int dOmega


def k_for(A, w=1.0, nr=24):
    """k = (dN_lin/dt) / (G w^2 dN_GW/dt), long-wavelength source (T_ij independent of q)."""
    IOn = sphere_avg(lambda n: F_on(A, w, n))
    dNgw = w / np.pi * IOn  # per G
    xr, wr = np.polynomial.legendre.leggauss(nr)
    rr = 0.5 * w * (xr + 1)
    wrr = 0.5 * w * wr
    Ioff = 0.0
    for r, wt in zip(rr, wrr):
        Ioff += wt * r**2 * sphere_avg(lambda n: F_off(A, w, r * n), 24, 24)
    dNlin = 8 * np.pi / 5 * Ioff / (2 * np.pi)**3  # per G^2
    return dNlin / (w**2 * dNgw), dNgw, IOn


print("\n=== Step 2: normalisation check against the quadrupole formula (G = 1) ===")
mu, a, Om = 1.0, 1.0, 0.5
w = 2 * Om
B = -(w**2 / 2) * (0.5 * mu * a**2) * np.array([[1, 1j, 0], [1j, -1, 0], [0, 0, 0]])
A_circ = B / 2  # positive-frequency amplitude: T(q0) = A 2pi delta(q0 - w) + c.c.
k_c, dNgw, _ = k_for(A_circ, w)
L_num = w * dNgw
L_quad = 32 / 5 * mu**2 * a**4 * Om**6
print(f"circular binary: L from dN/dt = {L_num:.6e}, (32/5) mu^2 a^4 Omega^6 = {L_quad:.6e}, ratio = {L_num/L_quad:.6f}")

print("\n=== Step 3: k for physical quadrupole patterns ===")
print(f"circular binary (m = 2, rotating): k = {k_c:.5e}")
A_lin = np.array([[1, 0, 0], [0, -0.5, 0], [0, 0, -0.5]], dtype=complex)
k_l, _, _ = k_for(A_lin, 1.0)
print(f"linear (axisymmetric) quadrupole:  k = {k_l:.5e}")
for nr in (12, 24):
    print(f"convergence, circular, nr = {nr}: k = {k_for(A_circ, w, nr)[0]:.6e}")
print(f"analytic guess 1/(15 pi^2) x (F_off/F_on mean ratio): 1/(15 pi^2) = {1/(15*np.pi**2):.5e}")

print("\n=== Step 4: GW150914 and GW170817 comparisons (C5's numbers, M-EXAMINER-09) ===")
PlinOverK = 9.27e-3  # pairs, GW150914, E = 2 Msun c^2, 150 Hz
PBO = 2.92e-6
for name, k in (("circular", k_c), ("linear", k_l)):
    Plin = k * PlinOverK
    print(f"{name}: P_lin = {Plin:.3e} pairs; P_BO = {PBO:.2e}; P_lin/P_BO = {Plin/PBO:.1f}; "
          f"vs retarded fusion 0.02-0.1 P_BO: {Plin/(0.1*PBO):.0f}-{Plin/(0.02*PBO):.0f}")
    print(f"   GW170817 100 Hz bin: P_BO/P_lin = 3.0e-8/k = {3.0e-8/k:.2e}")
print(f"C5 threshold k >~ 3.2e-4; margin circular = {k_c/3.2e-4:.1f}, linear = {k_l/3.2e-4:.1f}")

print("\n=== Step 5: Rahvar 2026 implied k (SI) ===")
Gs, cs, hb, Ms = 6.674e-11, 2.998e8, 1.0546e-34, 1.989e30
M = 1.0 * Ms
Mc = M * 0.25**0.6
f = 100.0
L = 32 / 5 * cs**5 / Gs * (Gs * Mc * np.pi * f / cs**3)**(10 / 3)
om = 2 * np.pi * f
Pdyn = 1e-30 * 1e-7  # W
kR = Pdyn / (Gs * hb * om**2 / cs**5 * L)
print(f"M = 1 Msun equal-mass, f_GW = 100 Hz: L_GW = {L:.3e} W; G hbar w^2/c^5 = {Gs*hb*om**2/cs**5:.3e}")
print(f"Rahvar P_dyn = {Pdyn:.1e} W -> implied k_scalar = {kR:.3e} (scalar, per energy not pairs)")
print(f"scaling check: P_lin = k G hbar w^2 L/c^5 ~ M^(10/3) w^(16/3) -> exponents: M {10/3:.3f}, w {2+10/3:.3f} (Rahvar: 10/3, 16/3)")
print(f"conformal-scalar k from this calc (c_J = 4/3): circular {k_c/12:.3e}")

print("\n=== Step 6: powers at GW150914 peak (SI), linear channel vs B&O fusion vs remnant Hawking ===")
Lpk = 3.6e49  # W, peak GW luminosity
f150 = 150.0
w150 = 2 * np.pi * f150
x = Gs * hb * w150**2 / cs**5
Plin_W = k_c * x * Lpk  # each pair carries energy ~ hbar q0 = hbar w
R_BO = 1.4e-4  # pairs/s, B&O face value (D-42)
W_BO = 2 * R_BO * hb * w150  # photon power, each photon ~ hbar w_s
W_H = 341 * W_BO  # M-CONSTRAINTS-11 ratio (one 65 Msun BH)
print(f"G hbar w^2/c^5 at 150 Hz = {x:.3e}")
print(f"linear-channel pair power at peak = k x that x L_pk = {Plin_W:.3e} W; pair rate = {Plin_W/(hb*w150):.3e} /s")
print(f"B&O unstimulated photon power = {W_BO:.3e} W (pair rate {R_BO:.1e} /s)")
print(f"remnant Hawking photon power (341 x B&O) = {W_H:.3e} W")
print(f"ratios: linear/BO = {Plin_W/W_BO:.0f}; Hawking/linear = {W_H/Plin_W:.2f}")
