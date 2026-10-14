"""Falsifier C4-1 (evidence angle): size of the off-shell (time-like, 'linear') photon-pair
channel of a real oscillating quadrupole source, built only from published coefficients:
  (i)  Redi & Tesi 2026 (arXiv:2606.28297) eq. 6: N = c_J/(2560 pi) Int d^4q/(2pi)^4 theta(q^2) W.W(-q),
       with c_J = 16 for photons, and their eq. 9 tensor term W.W = (1/2)(q^2)^2 h_ij^2 (TT);
  (ii) Han, Lykken, Zhang 1999 (hep-ph/9811350) eq. 46: Gamma(h~ -> gamma gamma) = kappa^2 m^3/(160 pi),
       with reduced Planck mass Mbar = sqrt(2)/kappa, i.e. kappa^2 = 16 pi G  ->  Gamma = G m^3 / 10.
The two routes must give the same coefficient of G^2 Int theta(q0) theta(q^2) T* P2 T.
Units: natural (hbar = c = 1) for coefficients; SI for astrophysical numbers (hbar cancels in N_pairs).
"""
import numpy as np
import sympy as sp

pi = sp.pi
G = sp.symbols('G', positive=True)

# ---- route (i): Redi-Tesi.  h_munu = -16 pi G (T - eta T/2)/q^2 (harmonic gauge); P2 kills trace part.
# W.W = (1/2) (q^2)^2 h P2 h = (1/2) (16 pi G)^2 T P2 T ; integral over theta(q^2) counts q0>0 and q0<0.
cJ = 16
coef_RT_both = sp.Rational(cJ, 2560) / pi * sp.Rational(1, 2) * (16 * pi * G) ** 2
coef_RT_pos = 2 * coef_RT_both            # per Int theta(q0)theta(q^2) d^4q/(2pi)^4 T*P2T
# ---- route (ii): Kallen-Lehmann. rho(s) = (1/pi) Im Pi / s^2, Im Pi = sqrt(s) Gamma(sqrt s) = G s^2/10
rho = G / (10 * pi)
# N_emit(s) = Int d^3k/((2pi)^3 2E) (1/Mbar^2) T*P2T = 8 pi G Int d^4q/(2pi)^4 2pi delta(q^2-s) theta(q0) T*P2T
coef_KL_pos = rho * 8 * pi * G * 2 * pi
print("Coefficient of G^2 Int_{q0>0, q^2>0} d^4q/(2pi)^4 T*P2T:")
print("  Redi-Tesi eq.6 (c_J=16):", sp.simplify(coef_RT_pos / G**2), "=", float(coef_RT_pos / G**2))
print("  HLZ width + spectral   :", sp.simplify(coef_KL_pos / G**2), "=", float(coef_KL_pos / G**2))
print("  agree:", sp.simplify(coef_RT_pos - coef_KL_pos) == 0)

# ---- polarisation sum for a massive spin-2 (mass^2 = w0^2 (1 - x^2), x = p/w0) with conserved,
# traceless long-wavelength source T_ij; angular average.  T00 = x^2 A, T0i = x B_i, A = n.T.n, B = T.n
x = sp.symbols('x', positive=True)
avgA, avgB = sp.Rational(2, 15), sp.Rational(1, 3)    # <|A|^2>, <|B|^2> in units of |T|^2
polsum = sp.Rational(2, 3) * x**4 * avgA - 2 * x**2 * avgB + 1
massless_TT = 1 - 2 * avgB + sp.Rational(1, 2) * avgA
print("massive-pol angular average <polsum>(x) =", sp.expand(polsum), "; massless TT average =", massless_TT)

# Monte-Carlo check of <|A|^2> and <|B|^2> for random complex symmetric traceless T
rng = np.random.default_rng(1)
M = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
T = (M + M.T) / 2; T -= np.trace(T) / 3 * np.eye(3)
n = rng.normal(size=(400000, 3)); n /= np.linalg.norm(n, axis=1)[:, None]
A = np.einsum('ni,ij,nj->n', n, T, n); B = n @ T.T
T2 = np.sum(abs(T)**2)
print("MC <|A|^2>/|T|^2 = %.4f (2/15 = %.4f);  <|B|^2>/|T|^2 = %.4f (1/3)" %
      (np.mean(abs(A)**2) / T2, 2 / 15, np.mean(np.sum(abs(B)**2, axis=1)) / T2))

# f(x) = N_emit(s)/N_g = x * <polsum> / (2/5);  ds = 2 w0^2 x dx
I = sp.integrate(2 * x * x * polsum / massless_TT, (x, 0, 1))
k = sp.simplify(rho / G * I)    # N_pairs = k * G w0^2 * N_g  (natural units)
print("Int_0^{w0^2} f ds / w0^2 =", I, "=", float(I))
print("k = I/(10 pi) =", k, "=", float(k))
k = float(k)

# ---- astrophysical numbers (SI). N_pairs = k (G/c^5) Int w dE   (hbar cancels)
Gs, c, hbar, Ms = 6.674e-11, 2.998e8, 1.0546e-34, 1.989e30
EP = np.sqrt(hbar * c**5 / Gs)
print("\nSI numbers")
for Erad in (2.0, 3.0):
    E = Erad * Ms * c**2; w = 2 * np.pi * 150; sig = 200.0
    Ng = E / (hbar * w)
    Plin = k * (hbar * w / EP)**2 * Ng
    Plin2 = k * Gs * E * w / c**5
    PBO = (4 / 25) * Gs**2 * E**2 * w * sig / c**10
    print(f"GW150914 merger, E = {Erad} Msun c^2: N_g = {Ng:.3e}, (hbar w/E_P)^2 = {(hbar*w/EP)**2:.3e}, "
          f"P_lin = {Plin:.3e} (check {Plin2:.3e}) pairs; B&O eq.8 x T_eff = {PBO:.3e}; ratio = {Plin/PBO:.1f}")

def chirp_lin(Mc_sun, f1, f2):
    Mc = Mc_sun * Ms; O1, O2 = np.pi * f1, np.pi * f2
    I_wdE = 0.4 * Mc * (Gs * Mc)**(2 / 3) * (O2**(5 / 3) - O1**(5 / 3))    # Int w |dE|, J/s
    E = 0.5 * Mc * (Gs * Mc)**(2 / 3) * (O2**(2 / 3) - O1**(2 / 3))
    return k * Gs / c**5 * I_wdE, E

for name, Mc, f1, f2, Pfus in (("GW170817 30-1600 Hz", 1.188, 30, 1600, 2.83e-8),
                               ("GW150914 inspiral 35-68 Hz", 28.0, 35, 68, 2.75e-8)):
    N, E = chirp_lin(Mc, f1, f2)
    print(f"{name}: E_GW = {E:.3e} J = {E/(Ms*c**2):.3e} Msun c^2; P_lin = {N:.3e} pairs; "
          f"fusion (M-IDEALIZER-10) = {Pfus:.2e}; ratio = {N/Pfus:.2e}")

# long-wavelength validity: k a <= w a = 2 v
for name, v in (("GW150914 merger", 0.53), ("GW170817 at 100 Hz", 0.16)):
    print(f"{name}: max |k| a = 2 v/c = {2*v:.2f}")
