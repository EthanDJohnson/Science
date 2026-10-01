"""M-CONSTRAINTS-09 (F12, K8): neutron-star maximum mass with a dark fermion chi in chemical equilibrium.
My own TOV solver and EOS (not the lens's). Geometric units G = c = 1, lengths in km; EOS in MeV/fm^3.
Species i (spin-1/2, degeneracy 2): n_i = k_i^3/(3 pi^2); eps_i = free Fermi gas + C_i n_i^2/2 (vector repulsion,
C_i = (hbar c)^3/(m_V/g)^2 MeV fm^3); mu_i = sqrt(k_i^2 + m_i^2) + C_i n_i; P = sum mu_i n_i - eps (T = 0).
Equilibrium n <-> chi: mu_chi = mu_n. Neutron toy EOS: vector repulsion with (m_V/g)_n = 60 MeV (my choice, stiff).
Checks: (a) free neutron gas -> Oppenheimer-Volkoff limit ~0.71 Msun (known law); (b) pure toy neutron matter M_max;
(c) toy neutrons + free chi (m_chi = 937.993, 938.543 MeV) -> lens says 0.687-0.688 Msun, EOS-insensitive;
(d) chi with self-repulsion m_V/g = 200/100/60/45/30 MeV -> lens 1.13/1.62/1.90/2.06/2.21 Msun (its own toy EOS)."""
import math
import numpy as np
from scipy.optimize import brentq
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
from math_checks import quantity, inequality, finish

HC = 197.3269804
MN = 939.56542
MEV_FM3_TO_KM2 = 1.3234e-6      # G/c^4 * (1 MeV/fm^3) in km^-2
MSUN_KM = 1.476625


def eps_free(k, m):   # MeV/fm^3, k and m in MeV
    s = math.sqrt(k * k + m * m)
    return (k * s * (2 * k * k + m * m) - m**4 * math.log((k + s) / m)) / (8 * math.pi**2) / HC**3


def species(mu, m, C):
    """Fermi momentum k (MeV) with sqrt(k^2+m^2) + C n(k) = mu; returns n (fm^-3), eps, mu."""
    if mu <= m:
        return 0.0, 0.0
    f = lambda k: math.sqrt(k * k + m * m) + C * (k / HC) ** 3 / (3 * math.pi**2) - mu
    kmax = math.sqrt(mu * mu - m * m)
    k = kmax if C == 0 else brentq(f, 0.0, kmax * (1 + 1e-12))
    n = (k / HC) ** 3 / (3 * math.pi**2)
    return n, eps_free(k, m) + 0.5 * C * n * n


def eos_table(parts, mu_max=4000.0, N=1500):
    P, E = [], []
    for mu in np.linspace(MN + 1e-3, mu_max, N):
        ns, es = zip(*[species(mu, m, C) for m, C in parts])
        eps = sum(es)
        p = mu * sum(ns) - eps
        if p > 1e-8:
            P.append(p); E.append(eps)
    P, E = np.array(P), np.array(E)
    cs2 = np.gradient(P, E)
    return P, E, cs2


def tov(Pc, P, E, dr=0.02):
    lp, le = np.log(P), np.log(E)
    eps_of = lambda p: math.exp(np.interp(math.log(p), lp, le))
    def rhs(r, y):
        p, m = y
        if p <= P[0]:
            return 0.0, 0.0
        e = eps_of(p) * MEV_FM3_TO_KM2
        pk = p * MEV_FM3_TO_KM2
        dp = -(e + pk) * (m + 4 * math.pi * r**3 * pk) / (r * (r - 2 * m)) / MEV_FM3_TO_KM2
        return dp, 4 * math.pi * r * r * e
    r = 1e-4
    y = [Pc, 4 / 3 * math.pi * r**3 * eps_of(Pc) * MEV_FM3_TO_KM2]
    while y[0] > P[0] * 1.0001 and r < 200:
        k1 = rhs(r, y); k2 = rhs(r + dr / 2, [y[i] + dr / 2 * k1[i] for i in range(2)])
        k3 = rhs(r + dr / 2, [y[i] + dr / 2 * k2[i] for i in range(2)]); k4 = rhs(r + dr, [y[i] + dr * k3[i] for i in range(2)])
        y = [y[i] + dr / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(2)]
        r += dr
        if y[0] <= 0:
            break
    return y[1] / MSUN_KM, r


def mmax(parts, dr=0.02):
    P, E, cs2 = eos_table(parts)
    best, cmax = 0.0, 0.0
    for Pc in np.geomspace(max(P[0] * 50, 1e-2), P[-1] * 0.95, 40):
        M, R = tov(Pc, P, E, dr)
        if M > best:
            best = M
            cmax = float(np.max(cs2[P <= Pc]))
    return best, cmax


C = lambda mvg: HC**3 / mvg**2
free_n = [(MN, 0.0)]
M_ov, _ = mmax(free_n); M_ov2, _ = mmax(free_n, dr=0.01)
print(f"   (a) free neutron gas M_max = {M_ov:.3f} Msun (dr 0.01 km: {M_ov2:.3f}); literature OV ~0.71")
quantity(f"{M_ov!r}", "0.71", rel_tol=0.02)
toy = [(MN, C(60.0))]
M_toy, c_toy = mmax(toy)
print(f"   (b) toy neutron matter (m_V/g = 60 MeV) M_max = {M_toy:.3f} Msun, max cs2 = {c_toy:.2f}")
res = {}
for mchi in (937.993, 938.543):
    M, c = mmax(toy + [(mchi, 0.0)])
    res[mchi] = M
    print(f"   (c) toy n + free chi (m_chi = {mchi}) M_max = {M:.3f} Msun, max cs2 = {c:.2f}")
M_free2, _ = mmax(free_n + [(937.993, 0.0)])
print(f"   (c') free n + free chi M_max = {M_free2:.3f} Msun (EOS-insensitivity test)")
quantity(f"{res[937.993]!r}", "0.69", rel_tol=0.05)
inequality(f"{res[937.993]!r}", "<", "1.0")
for mvg, lensM in [(200, 1.13), (100, 1.62), (60, 1.90), (45, 2.06), (30, 2.21)]:
    M, c = mmax(toy + [(937.993, C(float(mvg)))])
    print(f"   (d) chi repulsion m_V/g = {mvg} MeV: M_max = {M:.2f} Msun (lens {lensM}), max cs2 = {c:.2f}")
raise SystemExit(finish())
