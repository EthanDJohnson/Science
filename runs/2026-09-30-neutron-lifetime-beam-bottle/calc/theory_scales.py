"""Theory-facet scale checks (SI and eV). Constants are CODATA-2018 values typed from memory (not fetched):
mu_N = 3.15245125844e-8 eV/T, mu_n/mu_N = -1.91304273, Q-value of n decay = 0.782 MeV (m_n - m_p - m_e).
Shows: (1) Zeeman energy |mu_n| B at 4.6 T and 5 T vs Q; (2) resonance field for Delta m (Berezhiani);
(3) missing branching fraction implied by beam/bottle pairs; (4) SM n->H nu and radiative branches relative to gap."""
mu_N = 3.15245125844e-8  # eV/T
mu_n = 1.91304273 * mu_N  # eV/T magnitude
Q = 0.782e6  # eV
print("mu_n = %.3f neV/T" % (mu_n * 1e9))
for B in (4.6, 4.8, 5.0, 6.6):
    print("B = %.1f T: |mu_n|B = %.1f neV ; ratio to Q = %.2e" % (B, mu_n * B * 1e9, mu_n * B / Q))
for dm in (60, 100, 200, 280):  # neV
    print("Delta m = %d neV: B_res = %.2f T" % (dm, dm * 1e-9 / mu_n))
pairs = [(888.0, 878.0), (888.0, 879.4), (887.7, 877.75), (888.0, 877.2)]
for tb, tt in pairs:
    br = 1 - tt / tb
    gam = 1 / tt - 1 / tb
    print("beam %.2f bottle %.2f: Br_missing = %.4f ; dGamma = %.3e 1/s" % (tb, tt, br, gam))
print("bound-state branch 4e-6 vs 1.1e-2 gap: ratio = %.0f" % (1.1e-2 / 4e-6))
print("radiative branch 3.35e-3 vs gap 1.1e-2 ratio = %.1f" % (1.1e-2 / 3.35e-3))
