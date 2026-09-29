#!/usr/bin/env python3
"""Constraint audit of clock-based positions with the toolkit page_wootters.py (hbar = 1 inside;
energies as angular frequencies in rad/s; SI where stated).

A  Unruh-Wald / Pauli (K-02): a clock with bounded spectrum has no sharp (projective) time
   observable at arbitrary t; its covariant time POVM is unsharp, with Mandelstam-Tamm limits.
B  Kuchar's two-time objection (K-03): naive projector conditional probability vs the
   Giovannetti-Lloyd-Maccone memory construction, compared with the Born rule.
C  Interacting clock (Smith-Ahmadi Newtonian coupling): size of the correction in SI and
   whether the effective generator stays Hermitian (unitary) - compared with a generic coupling.
D  Thermal time (Connes-Rovelli) in finite dimensions: modular Hamiltonian K = -ln rho equals
   beta H only for a Gibbs state; misalignment for a non-Gibbs state.
"""
import math
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
import page_wootters as pw
from unit_tools import HBAR, C, G

np.set_printoptions(precision=6, suppress=True)
TWO_PI = 2 * math.pi

# ---------------------------------------------------------------- A
print("A. Unruh-Wald / Pauli: sharpness of finite-clock time states (w = 1 rad/s)")
for d in (4, 16, 64):
    HC = pw.equally_spaced_clock(d, 1.0, k0=-(d - 1) / 2)
    m = pw.PWModel(HC, np.diag([0.0, 1.0]))
    cm = m.clock_metrics()
    step = cm["lattice_step"]
    off = [float(m.overlap(f * step)[0]) for f in (0.25, 0.5, 1.0, 1.5)]
    print(f"  d={d:3d}: lattice step {step:.4f} s, |<t|t+tau>|/d at tau = (0.25,0.5,1,1.5) steps = "
          f"{off[0]:.3f}, {off[1]:.3f}, {off[2]:.2e}, {off[3]:.3f}; MT bound pi/(2 dE) = {cm['mandelstam_tamm_bound']:.4f} s; "
          f"POVM defect over one period = {cm['povm_defect']:.1e}")
print("  -> time states are orthogonal only on the lattice; at other tau they overlap: the time")
print("     observable is a covariant POVM, not a projector, as Unruh-Wald's assumptions require for escape.")

# ---------------------------------------------------------------- B
print("\nB. Kuchar two-time probability vs GLM memory vs Born rule (qubit, Rabi H = 0.5 sigma_x, d = 8, w = 1)")
d, w = 8, 1.0
HS = 0.5 * np.array([[0, 1], [1, 0]], dtype=complex)
# resonant clock for the qubit eigenvalues +-0.5: equally spaced E = w(k - 3.5): contains -0.5 and +0.5
HC = pw.equally_spaced_clock(d, w, k0=-(d - 1) / 2)
m = pw.PWModel(HC, HS)
psi0 = np.array([1, 0], dtype=complex)
Psi = m.physical_state(psi0)
P0 = np.diag([1, 0]).astype(complex); P1 = np.diag([0, 1]).astype(complex)
times = TWO_PI * np.arange(d) / (d * w)
E, V = np.linalg.eigh(HS)
U = lambda t: V @ np.diag(np.exp(-1j * E * t)) @ V.conj().T  # noqa: E731
for (j1, j2) in [(1, 3), (2, 5), (0, 4)]:
    t1, t2 = times[j1], times[j2]
    kn = pw.kuchar_naive(m, Psi, t1, t2, P0, P1)
    glm = pw.glm_two_time(HS, psi0, d, w, j1, j2)["P_b_given_a"][0, 1]
    born = abs((U(t2 - t1))[1, 0]) ** 2
    print(f"  t1 = {t1:.3f}, t2 = {t2:.3f}: Kuchar naive P(1|0) = {kn:.3e}; GLM P(1|0) = {glm:.6f}; Born |<1|U|0>|^2 = {born:.6f}")
kn_same = pw.kuchar_naive(m, Psi, times[2], times[2], P0, P0)
print(f"  same-time naive P(0 at t|0 at t) = {kn_same:.6f} (only equal times survive, as Kuchar says)")

# ---------------------------------------------------------------- C
print("\nC. Smith-Ahmadi gravitational clock-system coupling, H_eff = H_S (1 - lam H_S)^-1")
wS = TWO_PI * 429.228e12          # Sr clock transition, rad/s
for x in (1e-3, 1.0):
    lam = pw.gravity_lambda(x)
    print(f"  x = {x:g} m: lam = hbar G/(c^4 x) = {lam:.3e} s; fractional frequency shift lam*w_S = {lam*wS:.3e}")
E_needed = 1e-18 * C**4 / G
print(f"  shift reaches 1e-18 (current clock level) only if E_S/x >= 1e-18 c^4/G = {E_needed:.3e} J/m"
      f" (= {E_needed/C**2:.3e} kg of mass-energy per metre)")
# exact finite model: unitarity check of effective generator, SA coupling vs generic coupling
lam = 0.05
HS2 = np.diag([0.0, 1.0]).astype(complex)
HCg = pw.resonant_clock_for(HS2, lam, extra=(-2.0, -3.0))
mg = pw.PWModel(HCg, HS2, pw.gravity_coupling(HCg, HS2, lam))
eg = mg.effective_generator(0.7)
Gref = pw.gravity_generator(HS2, lam)
print(f"  toy (lam = 0.05, dimensionless units): physical dim {eg['physical_dim']}, rank {eg['rank']}, "
      f"non-Hermiticity {eg.get('nonhermiticity', float('nan')):.2e}; eigenvalues H_eff {np.linalg.eigvalsh(Gref)} vs H_S/(1-lam H_S) [0, {1/(1-lam):.6f}]")
rng = np.random.default_rng(7)
for gcoup in (0.05, 0.2):
    for trial in range(1):
        HCr = pw.equally_spaced_clock(6, 1.0, k0=-2.5)
        HSr = np.diag([-0.5, 0.5, 1.5]).astype(complex)
        A = rng.normal(size=(18, 18)) + 1j * rng.normal(size=(18, 18))
        Hint = gcoup * (A + A.conj().T) / 2
        try:
            mr = pw.PWModel(HCr, HSr, Hint, tol=1e-9)
            K = mr.physical_basis()
            print(f"  generic Hermitian coupling g = {gcoup}: physical dim {K.shape[1]} (exact null space of J)")
        except ValueError as ex:
            print(f"  generic coupling g = {gcoup}: {ex}")
print("  (a generic coupling usually destroys the exact null space: the constraint must be fine-tuned")
print("   or the clock enlarged; see the tool's 'interact' mode for the non-unitary/time-nonlocal regime)")

# ---------------------------------------------------------------- D
print("\nD. Thermal time in finite dimensions (hbar = k_B = 1): modular flow vs Hamiltonian flow")
H = np.diag([0.0, 1.0, 2.5, 4.0]).astype(complex)
beta = 0.7


def logm_h(rho):
    ev, vec = np.linalg.eigh(rho)
    return vec @ np.diag(np.log(ev)) @ vec.conj().T


gibbs = np.diag(np.exp(-beta * np.diag(H).real)); gibbs /= np.trace(gibbs)
Kg = -logm_h(gibbs)
shift = np.trace(Kg - beta * H) / 4
print(f"  Gibbs state: ||K - beta H - c|| = {np.linalg.norm(Kg - beta*H - shift*np.eye(4)):.2e} -> modular time s maps to t = beta*s")
Xr = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4)); Xr = Xr @ Xr.conj().T
for eps in (0.01, 0.1, 0.5):
    rho = (1 - eps) * gibbs + eps * Xr / np.trace(Xr)
    K = -logm_h(rho)
    comm = np.linalg.norm(K @ H - H @ K) / (np.linalg.norm(K) * np.linalg.norm(H))
    # best proportionality K ~ b H + c
    Hc = H - np.trace(H) / 4 * np.eye(4); Kc = K - np.trace(K) / 4 * np.eye(4)
    b = np.real(np.trace(Kc @ Hc)) / np.real(np.trace(Hc @ Hc))
    resid = np.linalg.norm(Kc - b * Hc) / np.linalg.norm(Kc)
    print(f"  non-Gibbs admixture eps = {eps}: ||[K,H]||/(||K|| ||H||) = {comm:.3e}; best fit K = {b:.4f} H + c, residual {resid:.3e}")
print("  -> the thermal-time flow is the mechanical time flow only for a KMS (Gibbs) state of that H;")
print("     otherwise it is a different flow, and proper time must be recovered some other way.")
