#!/usr/bin/env python3
"""Decomposer lens: settle three sub-questions left open in the dossier with finite models.

Units: hbar = 1 inside the finite models (energies are angular frequencies in rad/s, times in s).
Part 3 uses SI.

Part 1 (facet 1 / K-03): Kuchar's naive two-time conditional probability vs the
        Giovannetti-Lloyd-Maccone (GLM) memory construction, qubit + d = 8 equally spaced clock.
Part 2 (facet 2, multiple choice): one physical state of a 3-part universe A (x) B (x) S with an
        A-S interaction. Conditioning on clock B (uncoupled) gives exactly unitary dynamics of A(x)S;
        conditioning on clock A (coupled) gives a non-Hermitian / time-dependent effective generator
        for B(x)S. Same state, same constraint, different clock -> different kind of dynamics.
Part 3 (hidden premise 1 / size of the conflict): how big are the "quantum time" effects in the
        regimes where QM and GR time have both been probed?
"""
import math
import sys

import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import page_wootters as pw  # noqa: E402
from unit_tools import C, G, HBAR  # noqa: E402

np.set_printoptions(precision=4, suppress=True)

print("=" * 70)
print("PART 1: Kuchar two-time objection in a finite Page-Wootters model (hbar = 1)")
d, w = 8, 1.0
HC = pw.equally_spaced_clock(d, w, k0=-3.5)          # E = -3.5 .. 3.5 rad/s, contains -+0.5
HS = 0.5 * np.array([[0, 1], [1, 0]], dtype=complex)  # Rabi qubit, eigenvalues +-0.5 rad/s
m = pw.PWModel(HC, HS)
psi0 = np.array([1, 0], dtype=complex)
Psi = m.physical_state(psi0)
Pi = [np.diag([1, 0]).astype(complex), np.diag([0, 1]).astype(complex)]
times = 2 * math.pi * np.arange(d) / (d * w)
j1, j2 = 1, 4
t1, t2 = times[j1], times[j2]
_E, _V = np.linalg.eigh(HS)
U = lambda t: _V @ np.diag(np.exp(-1j * _E * t)) @ _V.conj().T  # noqa: E731  (exact e^{-i H_S t})
print(f"clock d = {d}, spacing {w} rad/s, lattice t1 = {t1:.4f} s, t2 = {t2:.4f} s")
for a in range(2):
    for b in range(2):
        naive = pw.kuchar_naive(m, Psi, t1, t2, Pi[a], Pi[b])
        textbook = abs(U(t2 - t1)[b, a]) ** 2
        print(f"  P(b={b} at t2 | a={a} at t1): naive Kuchar = {naive:.6f}   textbook |<b|U|a>|^2 = {textbook:.6f}")
glm = pw.glm_two_time(HS, psi0, d, w, j1, j2)
print("  GLM memory construction P[a,b] =\n", glm["P_b_given_a"])
tb = np.array([[abs(U(t2 - t1)[b, a]) ** 2 for b in range(2)] for a in range(2)])
print("  textbook table P[a,b] =\n", tb)
print(f"  max |GLM - textbook| = {np.abs(glm['P_b_given_a'] - tb).max():.2e}")
# equal-time check of the naive rule: should reproduce the single-time Born rule
naive_eq = pw.kuchar_naive(m, Psi, t1, t1, Pi[0], Pi[0])
print(f"  naive rule at t2 = t1 (a = b = 0): {naive_eq:.6f} (expected 1: repeated projective measurement)")

print("=" * 70)
print("PART 2: multiple-choice problem in a 3-part finite universe (hbar = 1)")
dA = 3
HA = pw.equally_spaced_clock(dA, 1.0)                  # E_A = 0, 1, 2 rad/s
sx = np.array([[0, 1], [1, 0]], dtype=complex)
sz = np.diag([1, -1]).astype(complex)
Delta, g = 0.7, 0.3                                    # rad/s
HSq = 0.5 * Delta * sz
XA = np.zeros((dA, dA), dtype=complex)
for k in range(dA - 1):
    XA[k, k + 1] = XA[k + 1, k] = 1
H_AS = np.kron(HA, np.eye(2)) + np.kron(np.eye(dA), HSq) + g * np.kron(XA, sx)   # A (x) S, 6x6
eAS = np.linalg.eigvalsh(H_AS)
HB = np.diag(-eAS).astype(complex)                     # resonant (unequally spaced) clock B, 6 levels
print(f"spec(H_A(x)S) with A-S coupling g = {g} rad/s: {eAS}")

# (i) clock = B, system = A (x) S (no clock-system coupling)
mB = pw.PWModel(HB, H_AS)
KB = mB.physical_basis()
print(f"clock B: physical dim = {KB.shape[1]}")
fid_B, herm_B = [], []
for t in [0.37, 1.1, 2.9, 5.3]:
    eg = mB.effective_generator(t)
    herm_B.append(eg["nonhermiticity"])
    fid_B.append(np.abs(eg["G"] - H_AS).max())
print(f"  clock B: max non-Hermiticity of generator = {max(herm_B):.2e}; max |G - H_AS| = {max(fid_B):.2e}")

# (ii) clock = A, system = B (x) S, with coupling g X_A (x) 1_B (x) sx
dB = HB.shape[0]
H_sys = np.kron(HB, np.eye(2)) + np.kron(np.eye(dB), HSq)      # B (x) S, 12x12
H_CS = g * np.kron(XA, np.kron(np.eye(dB), sx))                # A (x) B (x) S
mA = pw.PWModel(HA, H_sys, H_CS)
KA = mA.physical_basis()
print(f"clock A: physical dim = {KA.shape[1]} (must equal clock-B value: same constraint, permuted)")
rows = []
for t in [0.37, 1.1, 2.9, 5.3]:
    eg = mA.effective_generator(t)
    if eg["injective"]:
        G_t = eg["G"]
        rows.append((t, eg["rank"], eg["nonhermiticity"], G_t))
        print(f"  clock A, t = {t:.2f} s: rank {eg['rank']}/{eg['physical_dim']}, non-Hermiticity {eg['nonhermiticity']:.3e}")
    else:
        print(f"  clock A, t = {t:.2f} s: rank {eg['rank']}/{eg['physical_dim']} -> not injective (time-nonlocal)")
if len(rows) >= 2:
    dG = max(np.abs(rows[i][3] - rows[0][3]).max() for i in range(1, len(rows)))
    print(f"  clock A: max change of effective generator between listed times = {dG:.3e} rad/s (time dependence)")
# norm of conditional state under clock A for one physical state (probability of clock reading)
PsiA = KA[:, 0]
ns = [np.linalg.norm(mA.conditional(PsiA, t)) ** 2 for t in np.linspace(0, 2 * math.pi, 9)]
print(f"  clock A: ||psi(t)||^2 over one period (unnormalised): min {min(ns):.4f}, max {max(ns):.4f}")
PsiB = KB[:, 0]
nsB = [np.linalg.norm(mB.conditional(PsiB, t)) ** 2 for t in np.linspace(0, 2 * math.pi, 9)]
print(f"  clock B: ||psi(t)||^2 over same times: min {min(nsB):.4f}, max {max(nsB):.4f} (constant = unitary)")

print("=" * 70)
print("PART 3: sizes of 'quantum time' effects in probed regimes (SI)")
gE = 9.80665  # m/s^2
# (a) Earth redshift across 1 mm (classical background) -- dossier Q-06 check
print(f"(a) fractional redshift g*dh/c^2 at dh = 1 mm: {gE*1e-3/C**2:.3e} (dimensionless)")
# (b) Smith-Ahmadi mass-energy coupling of a clock to a system: lam * omega (dimensionless)
w_opt = 2 * math.pi * 429e12  # rad/s, Sr optical clock transition
for x in [1e-3, 1.0]:
    lam = pw.gravity_lambda(x)
    print(f"(b) Smith-Ahmadi lam*omega for omega = 2pi*429 THz, x = {x:g} m: lam = {lam:.3e} s, lam*omega = {lam*w_opt:.3e}")
# (c) proper-time difference between two interferometer arms separated by dh for time T,
#     and the Zych-type visibility of a two-level internal clock, V = |cos(dE*dtau/(2 hbar))|
for dh, T in [(1e-3, 1.0), (0.25, 1.0), (1.0, 1.0)]:
    dtau = gE * dh * T / C**2
    V = abs(math.cos(w_opt * dtau / 2))
    print(f"(c) dh = {dh:g} m, T = {T:g} s: dtau = {dtau:.3e} s, internal-clock phase = {w_opt*dtau:.3e} rad, V = {V:.6f}")
# (d) metric superposition: difference in proper-time rate at distance r from a mass m delocalised by dx
#     d(Phi)/c^2 ~ G m dx / (r^2 c^2)
for mkg, r, dx in [(1e-14, 450e-6, 250e-6), (1e-3, 1e-3, 1e-6)]:
    frac = G * mkg * dx / (r**2 * C**2)
    print(f"(d) source m = {mkg:g} kg delocalised by {dx:g} m at r = {r:g} m: fractional rate difference = {frac:.3e}")
tP = math.sqrt(HBAR * G / C**5)
print(f"Planck time t_P = {tP:.3e} s")
