"""Falsifier C2-2 (scale): how much can a Standard-Model-field MMP wormhole carry?

Tests C2's clause "Standard-Model fields pass only qubit-scale signals" / "only single
quanta below about 1e8 eV pass".

Inputs (SI unless stated):
- MMP (arXiv:1807.04726) eq. 5.30-5.31 as quoted in dossier Q-10 and verified in
  M-ENGINEER-01: E(l) = r_e^3/(G l^2) - q/(8 l), l* = 16 r_e^3/(G q N), |E_min| = N^2 g^2 hbar c/(256 pi r_e),
  with q = g r_e/(sqrt(pi) l_P) (the lenses' readings; N-scaling is the engineer lens's assumption).
- MMP p.13: signal sent in at t=0 emerges at t = pi*l; "l also sets the energy gap for excitations deep
  inside the wormhole" -> E_gap ~ hbar c / l (order of magnitude; O(1) factor = conformal dimension).
- MMP p.19: binding energy "is larger than the gap by a factor of q".
- Lowest-Landau-level degeneracy per charged flavour = q (number of flux quanta) -> q parallel 2D channels.
"""
import math

HBAR = 1.054571817e-34      # J s
C = 2.99792458e8            # m/s
G = 6.67430e-11             # m^3 kg^-1 s^-2
EV = 1.602176634e-19        # J
LP = math.sqrt(HBAR * G / C**3)
HBARC = HBAR * C
ME_C2 = 0.51099895e6 * EV   # electron rest energy, J
MNU_C2_MAX = 0.8 * EV       # KATRIN-type upper bound on neutrino mass (anchor only)

r_e = HBARC / (1e12 * EV)   # 1/TeV in m
print(f"r_e = hbar c/TeV = {r_e:.4e} m, l_P = {LP:.4e} m")

cases = [("g=0.06, N=1 (engineer)", 0.06, 1),
         ("g=0.06, N=54 (engineer)", 0.06, 54),
         ("g=0.3028, N=1 (constraints)", 0.30282212, 1)]

print("\n=== 1. Energy budget in units of the throat gap ===")
for name, g, N in cases:
    q = g * r_e / (math.sqrt(math.pi) * LP)
    ell = 16 * r_e**3 / (LP**2 * q * N)
    Emin = N**2 * g**2 * HBARC / (256 * math.pi * r_e)
    Egap = HBARC / ell
    T_thru = math.pi * ell / C
    ratio = Emin / Egap
    print(f"{name}: q = {q:.3e}, l = {ell:.3e} m, pi l/c = {T_thru:.3e} s")
    print(f"   |E_min| = {Emin:.3e} J = {Emin/EV:.3e} eV; E_gap ~ hbar c/l = {Egap:.3e} J = {Egap/EV:.3e} eV")
    print(f"   |E_min|/E_gap = {ratio:.3e}; analytic N q/16 = {N*q/16:.3e} (MMP p.19: 'larger than the gap by a factor of q')")
    channels = q * N
    print(f"   LLL channels (q per flavour x N) = {channels:.3e}")

    print("=== 2. Quanta and bits in flight per transit, and steady rate ===")
    P = Emin / T_thru
    n_gap = min(ratio, channels)
    n_e = Emin / ME_C2
    n_nu = Emin / MNU_C2_MAX
    print(f"   max steady power through throat P = |E_min|/(pi l/c) = {P:.3e} W")
    print(f"   gap-scale quanta in flight (<= channels): {n_gap:.3e}; rate {n_gap/T_thru:.3e} /s; "
          f"bits/quantum if channel index used: log2(channels) = {math.log2(channels):.1f}")
    print(f"   quanta exiting as electrons (E >= m_e c^2): in flight <= {n_e:.3e}; rate <= {n_e/T_thru:.3e} /s")
    print(f"   quanta at the neutrino-mass anchor 0.8 eV: in flight <= {n_nu:.3e}; rate <= {n_nu/T_thru:.3e} /s")
    print(f"   conservative information rate (1 bit per electron, no channel coding) >= {n_e/T_thru:.3e} bit/s")
    print(f"   payload check: 1 kg c^2 / |E_min| = {1*C**2/Emin:.3e}; one proton (938.3 MeV) / |E_min| = {938.272e6*EV/Emin:.3e}")

    print("=== 3. Clock offset needed for a shortcut, and its cost by mouth motion ===")
    M = r_e * C**2 / G
    Delta = T_thru  # upper bound: Delta > T_thru - T_ext with T_ext > 0
    for v in (1.0, 1e3, 1e5):
        beta2 = (v / C)**2
        one_minus_inv_gamma = beta2 / (1 + math.sqrt(1 - beta2))  # = 1 - sqrt(1-beta^2), cancellation-free
        t_needed = Delta / one_minus_inv_gamma
        KE = 0.5 * M * v**2
        print(f"   v = {v:.0e} m/s: time to accumulate Delta = {Delta:.2e} s is {t_needed:.3e} s; "
              f"mouth KE = {KE:.3e} J (mouth mass {M:.3e} kg); KE/|E_min| = {KE/Emin:.3e}")
    print()

print("=== 4. MMP's own validity window: r_e << d < 1/TeV (MMP p.27). Scan r_e below 1/TeV ===")
print("   Conditions checked: q >> 1 (LLL, semiclassical) and l >> d with d = 10 r_e (long wormhole).")
for g, N in ((0.06, 1), (0.30282212, 1)):
    for r in (r_e, r_e / 10, 1e-22, 1e-25, 1e-28, 1e-30):
        q = g * r / (math.sqrt(math.pi) * LP)
        ell = 16 * r**3 / (LP**2 * q * N)
        Emin = N**2 * g**2 * HBARC / (256 * math.pi * r)
        d = 10 * r
        ok = (q > 100) and (ell > 10 * d) and (d <= r_e)
        print(f"   g={g:.3f} N={N} r_e={r:.2e} m: q={q:.2e}, l={ell:.2e} m, pi l/c={math.pi*ell/C:.2e} s, "
              f"|E_min|={Emin/EV:.2e} eV = {Emin:.2e} J, electrons in flight<={Emin/ME_C2:.2e}, "
              f"1 kg c^2/|E_min|={C**2/Emin:.2e}, d=10r_e<=1/TeV & long & q>100: {ok}")
