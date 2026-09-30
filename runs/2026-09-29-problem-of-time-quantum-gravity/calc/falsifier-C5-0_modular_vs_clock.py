"""Falsifier C5-0: does modular (thermal) time coincide with clock time where C5 says it should?

Units: hbar = 1 in parts A-B (dimensionless model units; "time" = model time).
Part C in SI (hbar, k_B) with lifetimes in s and temperatures in K.

A. Finite-dimensional analogue of the CLPW observer-dressed de Sitter state (Type II_1, density matrix rho = 1):
   the maximally mixed (tracial) state on M_n, purified on M_n (x) M_n. Modular operator
   Delta = rho (x) rho'^{-1}. For rho = 1/n: Delta = 1 => modular flow sigma_s(a) = a for all s.
   Meanwhile an inner "clock" automorphism Ad exp(iQt) with Q = Q^dag in the algebra (CLPW: H_obs = q is in the
   algebra) is non-trivial and leaves the tracial state invariant (stationary / equilibrium).
B. Contrast: Gibbs state rho = e^{-beta H}/Z -> modular flow = Hamiltonian flow with t = beta*s (C5's coincidence case).
C. Martinetti-Rovelli diamond (Hislop-Longo modular flow of the Minkowski vacuum, conformal field) along the
   inertial worldline at the centre of a diamond of half-lifetime L: dt/ds = pi (L^2 - t^2)/L.
   Integrated: s(t) = (1/(2 pi)) ln((L+t)/(L-t)). Finite proper time 2L -> infinite modular parameter.
   Local thermal-time temperature T(t) = (hbar/k_B) ds/dt ; at centre T = 2 hbar/(pi k_B * lifetime).
"""
import numpy as np
from scipy.linalg import expm, logm

rng = np.random.default_rng(7)
n = 4

def rand_herm(n):
    X = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    return (X + X.conj().T) / 2

def modular_flow(rho, a, s):
    # For a faithful state with density matrix rho on M_n, sigma_s(a) = rho^{is} a rho^{-is}
    # (Tomita-Takesaki; conventions sign of s irrelevant here)
    L = logm(rho)
    U = expm(1j * s * L)
    return U @ a @ U.conj().T

def modular_operator_doubled(rho):
    # Delta = rho (x) (rho^T)^{-1} on H (x) H for the canonical purification |sqrt(rho)>>
    return np.kron(rho, np.linalg.inv(rho.T))

a = rand_herm(n)
Q = np.diag([0.0, 1.0, 2.0, 3.0])  # clock energy operator in the algebra (model units)

print("=== A. Tracial state (CLPW analogue: density matrix = identity) ===")
rho_tr = np.eye(n) / n
Delta = modular_operator_doubled(rho_tr)
print(f"n = {n}; ||Delta - 1|| = {np.linalg.norm(Delta - np.eye(n*n)):.3e}  (modular operator)")
for s in [0.5, 1.0, 5.0]:
    d_mod = np.linalg.norm(modular_flow(rho_tr, a, s) - a)
    U = expm(1j * Q * s)
    a_clock = U @ a @ U.conj().T
    d_clk = np.linalg.norm(a_clock - a)
    inv = abs(np.trace(rho_tr @ a_clock) - np.trace(rho_tr @ a))
    print(f"s = t = {s:4.1f}: ||sigma_s(a) - a|| = {d_mod:.3e} (modular, trivial);  "
          f"||Ad e^(iQt)(a) - a|| = {d_clk:.3f} (clock, non-trivial);  |state change under clock flow| = {inv:.1e}")

print("\n=== B. Gibbs state wrt Q: modular flow = clock flow with t = beta*s ===")
for beta in [0.5, 2.0]:
    rho_g = expm(-beta * Q); rho_g /= np.trace(rho_g)
    s = 0.7
    U = expm(1j * Q * (-beta * s))  # rho^{is} = e^{-i beta Q s}/Z^{is}
    d = np.linalg.norm(modular_flow(rho_g, a, s) - U @ a @ U.conj().T)
    print(f"beta = {beta}: ||sigma_s(a) - Ad e^(-i beta Q s)(a)|| = {d:.2e} at s = {s}")
print("beta -> 0 (maximally mixed): time per unit modular parameter t = beta*s -> 0, flow trivial (part A).")

print("\n=== C. Diamond (Martinetti-Rovelli), Minkowski vacuum, inertial observer (SI) ===")
hbar = 1.054571817e-34  # J s
kB = 1.380649e-23       # J/K
life = 1.0              # s, lifetime of observer = 2L
Lh = life / 2
for t in [0.0, 0.25, 0.4, 0.49, 0.499]:
    dtds = np.pi * (Lh**2 - t**2) / Lh     # s of proper time per unit modular parameter
    s_of_t = np.log((Lh + t) / (Lh - t)) / (2 * np.pi)
    T = hbar / kB / dtds                    # K
    print(f"t = {t:6.3f} s: dt/ds = {dtds:.4e} s, s(t) = {s_of_t:8.4f}, local thermal-time T = {T:.4e} K")
print(f"Centre check: 2 hbar/(pi kB lifetime) = {2*hbar/(np.pi*kB*life):.4e} K (Martinetti-Rovelli formula)")
print("Ratio dt/ds(t=0.49 s)/dt/ds(t=0) =", f"{(Lh**2-0.49**2)/Lh**2:.4f}",
      "-> modular time is not affine in proper time for an inertial clock in the vacuum")
