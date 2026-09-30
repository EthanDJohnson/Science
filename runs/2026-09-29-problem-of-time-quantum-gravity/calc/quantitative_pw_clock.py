"""Finite-dimensional Page-Wootters clock: numerical check of resolution limits. Dimensionless (hbar = 1).
Clock: d levels, H_C = -eps*diag(0..d-1), so a system frequency omega = j*eps is matched by clock level j.
System: qubit, H_S = diag(0, omega). Constraint C = H_C x 1 + 1 x H_S. Physical states = null space of C.
Time states |t_n> = d^-1/2 sum_k exp(+2 pi i k n/d)|E_k>, t_n = n*2pi/(d*eps): resolution dt = T/d, T = 2pi/eps.
Conditional state psi(t_n) = <t_n|Psi>. Checks: (i) ideal case omega = j*eps, 0<=j<=d-1 recovers exp(-i H_S t) exactly
(fidelity 1 at all d clock ticks); (ii) omega = (j+eta)*eps: best approximate state (system sector s paired with the clock
level k minimising |E_k + omega_s|) has residual |C Psi| = |eta| eps/sqrt(2) and conditional evolution at frequency j*eps,
so phase error at time t is eta*eps*t; (iii) omega > (d-1)*eps: no clock level within eps/2 of -omega, residual grows."""
import numpy as np

def build(d, eps, omega):
    HC = -eps*np.diag(np.arange(d, dtype=float))
    HS = np.diag([0.0, omega])
    return np.kron(HC, np.eye(2)) + np.kron(np.eye(d), HS)

def run(d, eps, omega, psi0):
    C = build(d, eps, omega)
    Psi = np.zeros((d, 2), dtype=complex)
    for s, ws in enumerate([0.0, omega]):
        k = int(np.argmin(np.abs(-eps*np.arange(d) + ws)))
        Psi[k, s] = psi0[s]
    Psi = Psi.reshape(-1)
    resid = np.linalg.norm(C @ Psi)/np.linalg.norm(Psi)
    P = Psi.reshape(d, 2)
    ks = np.arange(d); T = 2*np.pi/eps
    fids, phase_err = [], []
    for n in range(d):
        bra = np.exp(-2j*np.pi*ks*n/d)/np.sqrt(d)   # <t_n|E_k> = conj of |t_n> components
        cond = bra @ P
        cond = cond/np.linalg.norm(cond)
        t = n*T/d
        exact = np.array([psi0[0], psi0[1]*np.exp(-1j*omega*t)]); exact /= np.linalg.norm(exact)
        fids.append(abs(np.vdot(exact, cond))**2)
    return min(fids), resid

psi0 = np.array([1, 1])/np.sqrt(2)
eps = 1.0
print("d  omega/eps  min conditional-state fidelity over the d clock ticks   residual |C Psi|/|Psi| (units of eps)")
for d in (4, 8, 16, 32):
    for om in (1.0, 2.0, float(d-1), 1.25, 1.5, 2.4, float(d)+0.5):
        f, r = run(d, eps, om, psi0)
        print("%3d %8.3f   %.6f   %.4f" % (d, om, f, r))
print("Integer omega/eps <= d-1: fidelity 1 (exact Schrodinger recovery, ideal clock).")
print("Non-integer omega/eps: residual = |eta|*eps/sqrt(2) with eta the distance to the nearest integer; the constraint cannot be met exactly.")
print("Max representable omega = (d-1)*eps = 2pi(d-1)/T; worst-case frequency mismatch eps/2 = pi/T.")
