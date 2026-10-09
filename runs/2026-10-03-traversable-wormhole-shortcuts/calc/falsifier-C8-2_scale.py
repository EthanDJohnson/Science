"""Falsifier C8-2 (scale angle): checks the scale numbers behind candidate C8.

1. Payload quanta N = m c R / hbar for 1 kg through R = 1 m (SI).
2. Gate count for chaotic sparse-SYK wormhole teleportation, rebuilt from a SOURCED
   per-Trotter-step count (Granet, Kikuchi, Dreyer, Rinaldi, arXiv:2507.07530:
   "for N = 24 Majorana fermions, we get an average number of two-qubit gates around
   1022 per Trotter step, before circuit optimization"), scaled as N^2 (kN terms times
   O(N) Jordan-Wigner string length), times 3 Hamiltonian evolutions (L backward,
   L forward, R forward) times n_T = 10 Trotter steps. TFD preparation is NOT included,
   so this is a lower bound. Compared with the engineer lens model 2 k N^2 n_T, k = 4.
3. Required error per gate for a total circuit fidelity F (independent errors):
   eps = ln(1/F)/n_g, for F = 1/2 (lens criterion) and F = 0.05 (a mitigated-signal
   criterion, my assumption). Compared with achieved: 4.22e-3 (2022 Sycamore,
   lens-derived), 2.2e-3 (Granet et al. 2025 effective per two-qubit gate on
   trapped-ion hardware, "an average number of errors per TQ gate equal to 0.0022"),
   1e-3 (their quoted component benchmark).
4. Maldacena-Qi transfer-time ratio: free coupled fermions transfer in du0 ~ 1/mu;
   with SYK interactions the wormhole transfer time du ~ 1/t', with
   du/du0 ~ (mu/J)^((1-2D)/(2(1-D))) (MQ arXiv:1804.00491 p.28), D = 1/4 for q = 4.
   Dimensionless (J = 1 units); order-one prefactors not known, scaling only.
"""
import math

hbar = 1.054571817e-34  # J s
c = 2.99792458e8        # m/s

print("== 1. Payload quanta ==")
m, R = 1.0, 1.0
Nq = m * c * R / hbar
print(f"m c R / hbar for 1 kg, 1 m: {Nq:.3e} quanta (dimensionless)")
m_h, R_h = 70.0, 1.0
print(f"70 kg, 1 m: {m_h*c*R_h/hbar:.3e} quanta")

print("\n== 2. Gate count: sourced per-step scaling vs lens model ==")
g24 = 1022.0  # two-qubit gates per Trotter step at N = 24 (Granet et al.)
nT, n_evol, k = 10, 3, 4
rows = []
for N in (20, 24, 50, 100):
    g_src = g24 * (N / 24.0) ** 2 * n_evol * nT
    g_lens = 2 * k * N**2 * nT
    rows.append((N, g_src, g_lens))
    print(f"N = {N:3d}: sourced-scaling n_g = {g_src:.3e}; lens 2kN^2 n_T = {g_lens:.3e}; "
          f"ratio lens/sourced = {g_lens/g_src:.2f} ({math.log10(g_lens/g_src):+.2f} orders)")

print("\n== 3. Required vs achieved error per gate ==")
achieved = {"2022 Sycamore (lens, F=1/2 at 164 gates)": math.log(2) / 164,
            "2025 trapped-ion effective (Granet et al.)": 2.2e-3,
            "2025 trapped-ion component benchmark": 1.0e-3}
for name, e in achieved.items():
    print(f"achieved {name}: {e:.2e}")
for F in (0.5, 0.05):
    print(f"-- circuit fidelity target F = {F}")
    for N, g_src, g_lens in rows:
        for label, ng in (("sourced", g_src), ("lens", g_lens)):
            eps = math.log(1 / F) / ng
            gaps = ", ".join(f"{math.log10(e/eps):.2f}" for e in achieved.values())
            print(f"   N = {N:3d} ({label:7s}): eps_req = {eps:.2e}; gap (orders) vs "
                  f"[2022, 2025 eff, 2025 comp] = [{gaps}]")

print("\n== 4. Maldacena-Qi: wormhole transfer vs bare coupling ==")
D = 0.25
expo = (1 - 2 * D) / (2 * (1 - D))
print(f"exponent (1-2D)/(2(1-D)) at D = 1/4: {expo:.4f}")
print(f"E_gap exponent 1/(2-2D) = {1/(2-2*D):.4f} (MQ eq. 5.77 says mu^(2/3))")
print("\n== 5. Decisive-test lever arm: scrambling time ~ ln N ==")
for N1, N2 in ((20, 100), (8, 24), (24, 100)):
    print(f"ln({N2})/ln({N1}) = {math.log(N2)/math.log(N1):.3f}; "
          f"difference ln N2 - ln N1 = {math.log(N2)-math.log(N1):.3f} (units of 1/lambda_L)")
print()
for r in (1e-1, 1e-2, 1e-3, 1e-4, 1e-6):
    ratio = r ** expo
    print(f"mu/J = {r:.0e}: du/du0 ~ {ratio:.3e}  (wormhole route faster by ~{1/ratio:.1f}x, "
          f"up to an O(1) prefactor)")
