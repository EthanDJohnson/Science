#!/usr/bin/env python3
"""Idealizer lens, model M1: finite Page-Wootters universe (clock (x) system, one constraint).

Units: hbar = 1; energies are angular frequencies (rad/s), times in s (dimensionless in the toy runs).
Uses the tested toolkit calculator page_wootters.py.

Parts
 A. Ideal (equally spaced, uncoupled) clock: conditional evolution = Schroedinger, norm constant.
 B. Kuchar naive two-time probability vs GLM memory construction (Kuchar objection in the model).
 C. Interacting clock (Smith-Ahmadi Newtonian mass-energy coupling): effective generator, redshift,
    deviation from Schroedinger vs coupling lam; weak-coupling scaling.
 D. Generic weak interaction H_CS = g * random Hermitian: non-Hermiticity of effective generator vs g.
 E. "Unimodular" limit: the clock is ideal when its constraint is linear in a momentum with spectrum R;
    finite d approximates it with time resolution T/d -> check resolution scaling ~ 1/d.
 F. Thermal time in the model: modular flow of the reduced system state vs relational (PW) flow.
"""
import sys
import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import page_wootters as pw  # noqa: E402

np.set_printoptions(precision=4, suppress=True)
rng = np.random.default_rng(1)

print("=== A. Ideal uncoupled clock (d=8, omega_clock=1 rad/s) + qubit (Rabi 1 rad/s) ===")
d = 8
HC = pw.equally_spaced_clock(d, 1.0, k0=-(d - 1) / 2)   # E = -3.5..3.5
HS = 0.5 * np.array([[0, 1], [1, 0]], dtype=complex)    # eigen +-0.5 -> resonant with clock
m = pw.PWModel(HC, HS)
Psi = m.physical_state(np.array([1, 0]))
rows = m.track(Psi, np.linspace(0, 2 * np.pi, 9))
print(" min fidelity", min(r["fidelity"] for r in rows), " max |norm2_rel-1|",
      max(abs(r["norm2_rel"] - 1) for r in rows))

print("\n=== B. Kuchar two-time objection in the same model ===")
P0 = np.diag([1, 0]).astype(complex)
P1 = np.diag([0, 1]).astype(complex)
tl = 2 * np.pi * np.arange(d) / d
for j2 in (1, 2, 3):
    pk = pw.kuchar_naive(m, Psi, tl[0], tl[j2], P0, P1)
    glm = pw.glm_two_time(HS, np.array([1, 0]), d, 1.0, 0, j2)
    exact = abs(m.evolve(np.array([1, 0], dtype=complex), tl[j2])[1]) ** 2
    print(f" t2-t1={tl[j2]:.4f}: naive Kuchar P(1|0)={pk:.3e}; GLM memory P(1|0)={glm['P_b_given_a'][0,1]:.6f};"
          f" textbook |<1|U|0>|^2={exact:.6f}")
# naive form at non-lattice times (non-orthogonal clock states)
for dt in (0.1, 0.3):
    pk = pw.kuchar_naive(m, Psi, 0.0, dt, P0, P1)
    exact = abs(m.evolve(np.array([1, 0], dtype=complex), dt)[1]) ** 2
    print(f" off-lattice dt={dt}: naive Kuchar P(1|0)={pk:.4e} vs textbook {exact:.4e}")

print("\n=== C. Interacting clock: Smith-Ahmadi H_CS = -lam H_C (x) H_S ===")
HS2 = np.diag([0.0, 1.0]).astype(complex)     # qubit with gap 1 rad/s
for lam in (1e-3, 1e-2, 5e-2, 1e-1):
    HCr = pw.resonant_clock_for(HS2, lam, extra=(0.5, 2.0, -3.0))
    HCS = pw.gravity_coupling(HCr, HS2, lam)
    mg = pw.PWModel(HCr, HS2, HCS)
    psi0 = np.array([1, 1]) / np.sqrt(2)
    Pg = mg.physical_state(psi0)
    ts = np.linspace(0, 20, 41)
    r_plain = mg.track(Pg, ts)
    Heff = pw.gravity_generator(HS2, lam)
    r_eff = mg.track(Pg, ts, H_ref=Heff)
    freq = np.real(np.diag(Heff))
    print(f" lam={lam:g}: eff gap={freq[1]-freq[0]:.6f} (1/(1-lam)={1/(1-lam):.6f});"
          f" min fid vs H_S over t<=20: {min(r['fidelity'] for r in r_plain):.6f};"
          f" vs H_eff: {min(r['fidelity'] for r in r_eff):.12f}; frac. shift/lam = {(freq[1]-freq[0]-1)/lam:.4f}")

print("\n=== D. Generic weak clock-system interaction g*V: non-unitarity/nonlocality of conditional dynamics ===")
d = 6
HC = pw.equally_spaced_clock(d, 1.0, k0=-(d - 1) / 2)
HS3 = np.diag([-0.5, 0.5]).astype(complex)
A = rng.normal(size=(2 * d, 2 * d)) + 1j * rng.normal(size=(2 * d, 2 * d))
V = (A + A.conj().T) / 2
V /= np.linalg.norm(V, 2)
for g in (0.0, 1e-3, 1e-2, 1e-1):
    mm = pw.PWModel(HC, HS3, g * V if g > 0 else None, tol=1e-9)
    K = mm.physical_basis()
    if K.shape[1] == 0:
        # interaction shifts eigenvalues off zero; use nearest-to-zero eigenvectors of J (approx null space)
        w, U = np.linalg.eigh(mm.J)
        idx = np.argsort(np.abs(w))[:2]
        print(f" g={g:g}: exact kernel empty; two smallest |eig J| = {np.abs(w[idx])}")
        # shift constraint so that these are exact zeros: J' = J - sum w_i |u_i><u_i| (clock-level retuning)
        Jfix = mm.J - (U[:, idx] * w[idx]) @ U[:, idx].conj().T
        HCS_fix = Jfix - np.kron(HC, np.eye(2)) - np.kron(np.eye(d), HS3)
        HCS_fix = (HCS_fix + HCS_fix.conj().T) / 2
        mm = pw.PWModel(HC, HS3, HCS_fix, tol=1e-9)
    eg = mm.effective_generator(0.37)
    nh = eg.get("nonhermiticity", float("nan"))
    print(f" g={g:g}: physical dim={eg['physical_dim']}, rank={eg['rank']}, injective={eg['injective']},"
          f" non-Hermiticity of generator={nh:.3e}")

print("\n=== E. Ideal-clock limit: resolution of a d-level clock of period T=2pi ===")
for d in (4, 8, 16, 32, 64):
    mc = pw.PWModel(pw.equally_spaced_clock(d, 1.0), np.diag([0.0, 1.0]))
    cm = mc.clock_metrics()
    print(f" d={d}: t_half={cm['t_half']:.4f}  t_orth={cm['t_orth']:.4f}  t_orth*d/(2pi)={cm['t_orth']*d/(2*np.pi):.4f}"
          f"  povm_defect={cm['povm_defect']:.2e}")

print("\n=== F. Thermal (modular) time vs relational time, 3-level system ===")
ES = np.array([0.0, 1.0, 3.0])
for label, w in (("Gibbs beta=0.7", np.exp(-0.7 * ES)), ("non-Gibbs", np.array([0.5, 0.2, 0.3]))):
    p = w / w.sum()
    K = -np.log(p)             # modular Hamiltonian of rho_S = sum p_n |n><n| (reduced PW state)
    # modular flow generates phases K_n s; relational flow generates E_n t. Proportional iff K_n - K_0 = beta (E_n - E_0)
    ratios = (K[1:] - K[0]) / (ES[1:] - ES[0])
    print(f" {label}: p={p}, (K_n-K_0)/(E_n-E_0) = {ratios} -> "
          f"{'single beta: modular flow = PW time rescaled' if np.allclose(ratios, ratios[0]) else 'no single beta: modular flow is not the PW time'}")
