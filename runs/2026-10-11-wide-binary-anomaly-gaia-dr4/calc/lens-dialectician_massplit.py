"""Dialectician lens, calc 2.
(a) Gamma conversions for the 36-pair family-4 dataset (D-26) and Chae 2025 (D-25): Gamma -> gamma = 10^(2 Gamma).
(b) Mass-split-at-fixed-separation test: MOND's boost is a function of g_N = G M / r^2, so at fixed
    projected separation s low-mass pairs (lower g_N) should be boosted MORE than high-mass pairs.
    Hidden-triple contamination acts through the velocity kick relative to v_c(s) and the light-based
    mass deficit, which is (to first order) not organised by g_N. Compare gamma_med in M_est terciles at
    fixed s, Newton+triples vs MOND (chae2024 preset). Template: clean Newtonian catalogue, same bins.
Units: s in au (printed), masses in Msun, accelerations m s^-2; gamma dimensionless.
"""
import sys
import numpy as np
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import wide_binary_population as wbp  # noqa: E402

print("(a) Gamma -> gamma conversions")
for lab, G_ in [("Chae+26 all, gN<10^-9.1", 0.102), ("Chae+26 all, gN<10^-9.5", 0.132),
                ("Chae+26 minus 2 systems, <10^-9.1", 0.042), ("minus 2, <10^-9.5", 0.057),
                ("minus 2, <10^-10.1", 0.085), ("Chae 2025 MOND regime", 0.085),
                ("Chae 2025 high-g", 0.000), ("Chae 2024b new sample", 0.068)]:
    print(f"  {lab:38s} Gamma={G_:.3f} -> gamma={10 ** (2 * G_):.3f}")

AU = wbp.AU
MSUN = wbp.MSUN
N = 200000
sbins = [(2000, 3500), (3500, 6000), (6000, 12000), (12000, 30000)]


def cat(gravity, ft, seed):
    return wbp.generate(N, gravity=gravity, f_triple=ft, seed=seed, release="DR3",
                        s_range=(1500 * AU, 30000 * AU))


ref = cat(1.0, 0.0, 500)
# mass terciles from the template (fixed edges, M_est in Msun)
edges = np.quantile(ref["M_est"] / MSUN, [0, 1 / 3, 2 / 3, 1])
print(f"\n(b) M_est tercile edges [Msun]: {np.round(edges, 3)}")


def med_grid(c):
    out = np.zeros((len(sbins), 3))
    sa = c["s"] / AU
    m = c["M_est"] / MSUN
    for i, (lo, hi) in enumerate(sbins):
        for j in range(3):
            k = (sa >= lo) & (sa < hi) & (m >= edges[j]) & (m < edges[j + 1]) & (c["vtilde"] < 5)
            out[i, j] = np.median(c["vtilde"][k])
    return out


R = med_grid(ref)
for lab, gr, ft, seed in [("Newton f_t=0.2", 1.0, 0.2, 1), ("Newton f_t=0.3", 1.0, 0.3, 2),
                          ("MOND chae2024 f_t=0", "chae2024", 0.0, 3),
                          ("MOND chae2024 f_t=0.2", "chae2024", 0.2, 4)]:
    c = cat(gr, ft, seed)
    g = (med_grid(c) / R) ** 2
    print(f"  {lab}")
    for i, (lo, hi) in enumerate(sbins):
        d = g[i, 0] - g[i, 2]
        print(f"    s {lo:5d}-{hi:5d} au: gamma_med lowM {g[i,0]:.3f} midM {g[i,1]:.3f} highM {g[i,2]:.3f} | low-high {d:+.3f}")
# MOND expectation at bin centres, for reference
print("\n  chae2024 gamma_MOND at g_N = G M/(1.2 s)^2 for M = 0.8 / 1.3 / 2.0 Msun:")
for lo, hi in sbins:
    sc = np.sqrt(lo * hi) * AU
    vals = [float(wbp.gamma_mond(np.array([wbp.G * M * MSUN / (1.2 * sc) ** 2]), model="chae2024")[0]) for M in (0.8, 1.3, 2.0)]
    print(f"    s ~ {sc/AU:6.0f} au: " + " ".join(f"{v:.3f}" for v in vals))
