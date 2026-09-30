#!/usr/bin/env python3
"""Constraints lens: neutron-star maximum mass with a dark fermion chi in chemical equilibrium (toy TOV).

PURPOSE: an independent order-of-magnitude check of the neutron-star bound on dark decay (D-88: M_max ~ 0.7 Msun
for a free chi) and of how much repulsive chi self-interaction restores 2 Msun (D-77: m_A'/g' <~ 45-60 MeV).

MODEL (this lens's own toy; NOT a published EOS):
  * Neutron matter: E/A(n) = a u^alpha + b u^beta, u = n/n0, n0 = 0.16 fm^-3, with a = 13.0 MeV, alpha = 0.5,
    b = 5.0 MeV, beta = 2.4 -- the two-power functional form used for QMC neutron-matter fits; parameters chosen
    here so that the pure-neutron star reaches M_max ~ 2 Msun. mu_n = m_n + a(1+alpha)u^alpha + b(1+beta)u^beta,
    P_n = n (a alpha u^alpha + b beta u^beta).
  * chi: free spin-1/2 Fermi gas of mass m_chi, plus optional repulsive vector self-interaction
    eps += G n_chi^2/2, mu_chi = sqrt(k^2 + m^2) + G n_chi, G = (g/m_V)^2 (natural units).
  * Chemical equilibrium n <-> chi (the dark decay itself): mu_chi = mu_n; no chi-n interaction; T = 0.
  * TOV in geometric units (km), RK4 in r; M_max from a scan of central mu.
  Validation: a pure free-neutron gas must give the Oppenheimer-Volkoff limit ~0.71 Msun.
Units: MeV, fm internally; 1 MeV/fm^3 = 1.32384e-6 km^-2 (G/c^4 applied); Msun = 1.47663 km.
"""
import math
import numpy as np

HBARC = 197.3269804      # MeV fm
MN = 939.56542052        # MeV
N0 = 0.16                # fm^-3
A_, AL, B_, BE = 13.0, 0.5, 5.0, 2.4
CONV = 1.32384e-6        # km^-2 per MeV/fm^3
MSUN_KM = 1.47663


def fermi_gas(k, m):
    """free spin-1/2 gas: n (fm^-3), eps (MeV/fm^3), P (MeV/fm^3) at Fermi momentum k (MeV)."""
    if k <= 0:
        return 0.0, 0.0, 0.0
    E = math.sqrt(k * k + m * m)
    t = math.asinh(k / m)
    n = k**3 / (3 * math.pi**2)
    eps = (k * E * (2 * k * k + m * m) - m**4 * t) / (8 * math.pi**2)
    P = (k * E * (2 * k * k - 3 * m * m) + 3 * m**4 * t) / (24 * math.pi**2)
    h3 = HBARC**3
    return n / h3, eps / h3, P / h3


def neutron_toy(mu):
    """n, eps, P of the toy neutron matter at chemical potential mu (MeV); zero if mu <= m_n."""
    if mu <= MN:
        return 0.0, 0.0, 0.0
    f = lambda u: A_ * (1 + AL) * u**AL + B_ * (1 + BE) * u**BE - (mu - MN)
    lo, hi = 0.0, 1.0
    while f(hi) < 0:
        hi *= 2
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if f(mid) < 0 else (lo, mid)
    u = 0.5 * (lo + hi)
    n = u * N0
    ea = A_ * u**AL + B_ * u**BE
    return n, n * (MN + ea), n * (A_ * AL * u**AL + B_ * BE * u**BE)


def chi_gas(mu, m, G_eff):
    """chi at chemical potential mu with repulsion G_eff (MeV fm^3)."""
    if mu <= m:
        return 0.0, 0.0, 0.0
    g = lambda k: math.sqrt(k * k + m * m) + G_eff * fermi_gas(k, m)[0] - mu
    lo, hi = 0.0, math.sqrt(mu * mu - m * m)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if g(mid) < 0 else (lo, mid)
    k = 0.5 * (lo + hi)
    n, e, P = fermi_gas(k, m)
    return n, e + 0.5 * G_eff * n * n, P + 0.5 * G_eff * n * n


def eos_table(kind, m_chi=None, mV_over_g=None, npts=1500):
    G_eff = 0.0 if not mV_over_g else HBARC**3 / mV_over_g**2
    mu_min = MN if kind in ("neutron", "free_n") else m_chi
    mus = mu_min + (6000.0 - mu_min) * np.linspace(0, 1, npts) ** 2.5
    P, E = [], []
    for mu in mus[1:]:
        if kind == "free_n":
            nn, en, pn = fermi_gas(math.sqrt(mu * mu - MN * MN), MN)
            nc = ec = pc = 0.0
        else:
            nn, en, pn = neutron_toy(mu)
            nc, ec, pc = chi_gas(mu, m_chi, G_eff) if kind == "n+chi" else (0.0, 0.0, 0.0)
        P.append(pn + pc); E.append(en + ec)
    P, E = np.array(P), np.array(E)
    return np.log(P), np.log(E), P, E


def tov(Pc, tab, dr):
    lP, lE = tab[0], tab[1]
    eps_of = lambda p: math.exp(np.interp(math.log(p), lP, lE)) if p > 0 else 0.0
    Psurf = math.exp(lP[0]) * 1.0001

    def rhs(r, P, m):
        e = eps_of(P) * CONV
        Pg = P * CONV
        dP = -(e + Pg) * (m + 4 * math.pi * r**3 * Pg) / (r * (r - 2 * m)) / CONV
        dm = 4 * math.pi * r * r * e
        return dP, dm

    r = dr
    m = 4 / 3 * math.pi * r**3 * eps_of(Pc) * CONV
    P = Pc
    while P > Psurf and r < 200:
        k1 = rhs(r, P, m)
        k2 = rhs(r + dr / 2, P + dr / 2 * k1[0], m + dr / 2 * k1[1])
        k3 = rhs(r + dr / 2, P + dr / 2 * k2[0], m + dr / 2 * k2[1])
        k4 = rhs(r + dr, P + dr * k3[0], m + dr * k3[1])
        Pn = P + dr / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        if Pn <= Psurf:
            break
        m += dr / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        P = Pn
        r += dr
    return m / MSUN_KM, r


def mmax(tab, dr, nscan=28):
    Pvals = np.exp(np.linspace(math.log(tab[2][0]) + 4.0, math.log(tab[2][-1]) - 0.5, nscan))
    best = (0, 0, 0)
    for Pc in Pvals:
        M, R = tov(Pc, tab, dr)
        if M > best[0]:
            best = (M, R, Pc)
    return best


def causal_ok(tab, Pc=None):
    P, E = tab[2], tab[3]
    cs2 = np.diff(P) / np.diff(E)
    if Pc is not None:
        cs2 = cs2[P[1:] <= Pc]
    return float(cs2.max())


cases = [("free neutron gas (OV check)", "free_n", None, None),
         ("toy neutron matter, no chi", "neutron", None, None),
         ("toy n + free chi, m_chi = 937.993 MeV", "n+chi", 937.993, None),
         ("toy n + free chi, m_chi = 938.543 MeV", "n+chi", 938.543, None)]
for mvg in (200.0, 100.0, 60.0, 45.0, 30.0):
    cases.append((f"toy n + chi (937.993) with repulsion m_V/g = {mvg:.0f} MeV", "n+chi", 937.993, mvg))

print(f"{'case':58s} {'M_max (Msun)':>13s} {'R (km)':>7s} | {'M_max dr/1.5':>12s} | max c_s^2")
for lab, kind, mc, mvg in cases:
    tab = eos_table(kind, mc, mvg)
    M1, R1, Pc1 = mmax(tab, 0.03)
    M2, R2, Pc2 = mmax(tab, 0.02)
    print(f"{lab:58s} {M1:13.3f} {R1:7.2f} | {M2:12.3f} | {causal_ok(tab):.2f} (all P); {causal_ok(tab, Pc1):.2f} (P <= Pc of M_max star)")

print("\nBorn-level chi-chi elastic cross-section for the repulsion needed (sigma = m_chi^2 G^2/(4 pi), contact limit):")
for mvg in (60.0, 45.0, 30.0):
    G = 1 / mvg**2                      # MeV^-2
    sig_MeV = 937.993**2 * G**2 / (4 * math.pi)
    sig_cm2 = sig_MeV * (HBARC * 1e-13) ** 2
    m_g = 937.993 * 1.78266192e-27      # g
    alpha_D_over = 937.993 / mvg / (4 * math.pi)   # alpha' m_chi / m_V for g = 1 (Born validity needs << 1)
    print(f"  m_V/g = {mvg:.0f} MeV: sigma = {sig_cm2:.2e} cm^2, sigma/m = {sig_cm2/m_g:.2f} cm^2/g "
          f"(Born parameter alpha' m_chi/m_V = {alpha_D_over:.2f} for g=1: Born {'unreliable' if alpha_D_over > 0.3 else 'ok'})")
