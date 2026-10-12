#!/usr/bin/env python3
"""Adversarial re-derivation of the task-D (stochastic / CMB / SA / ULDM) findings, independent of the task-D scripts
and (except where stated) of qft_second_order.

Sections
 A  sigma(g g -> gamma gamma) from the LITERATURE-normalised gravitational Compton amplitudes crossed to the t-channel
    (Bjerrum-Bohr, Holstein, Plante, Vanhove 2015, arXiv:1410.4148, eq. 5.2: D1 = 8 pi G s^2/t and 8 pi G u^2/t),
    checked against their/Skobelev's CM Compton cross section (eq. 5.6), then crossed: |M| = 8 pi G t^2/s, u^2/s.
 B  Gamma/rho^2 for an isotropic, unpolarised, incoherent gas by a lab-frame Monte Carlo with explicit boosts and a
    sampled CM photon direction (no closed-form sigma used), for a broad non-monochromatic spectrum.
 C  SI number for 2 Gamma via a natural-units (eV) route; Delta N_eff needed for B&O's 1e-110.
 D  |Phi| of eq. 15 / S9 by direct quadrature (radiation + matter + Lambda).
 E  Eq. S11 transcribed from the paper text; massless limit and resonant (threshold) limit with mpmath.
 F  Eqs. 16 and 18 with independently typed constants.
 G  CMB factor: rate-equation algebra (sympy) and the Rayleigh-Jeans average in B&O's ring model (scipy dblquad).
 H  tau_phi/tau for PHYSICAL coherent profiles: ratio of the photon and scalar coefficients already logged by the
    task-A runs (taskA3b_*.log and taskA4_physical.log), parsed here (these are module/spinor-engine numbers).
Units: hbar = c = 1 unless SI is stated; G = 1 in sections A, B.
"""
import math, re, os
import numpy as np
from scipy import integrate
import mpmath as mp
import sympy as sp

PI = math.pi
NOTES = "/home/user/Science/checks/2026-10-11-blas-oller-gw-decay/notes"
rng = np.random.default_rng(20261012)

def hdr(t):
    print("\n" + "=" * 100 + "\n" + t + "\n" + "=" * 100)

# ------------------------------------------------------------------------------------------------ A
hdr("A  literature-normalised amplitudes: Compton check (BHPV eq. 5.6) and crossed g g -> gamma gamma sigma")
G = 1.0
# Compton gamma g -> gamma g, CM: |D|^2 summed over the 4 nonzero helicity amplitudes, averaged over 4 initial states
for th in (0.5, 1.3, 2.7):
    s = 4.0; w = math.sqrt(s) / 2
    t = -s * math.sin(th / 2) ** 2; u = -s * math.cos(th / 2) ** 2
    msq_avg = (2 * (8 * PI * G * s * s / t) ** 2 + 2 * (8 * PI * G * u * u / t) ** 2) / 4
    dsig = msq_avg / (64 * PI ** 2 * s)
    bhpv = 2 * G ** 2 * w ** 2 * (1 + math.cos(th / 2) ** 8) / math.sin(th / 2) ** 4
    print(f"  theta={th}: dsigma/dOmega from eq.5.2 amplitudes = {dsig:.12g};  BHPV/Skobelev eq. 5.6 = {bhpv:.12g}")
# crossed (s <-> t): |M| = 8 pi G t^2/s and 8 pi G u^2/s for the two photon helicity assignments of ONE graviton
# helicity class; the other class gives 0 (whichever it is, the unpolarised average below does not care).
for s in (1.0, 3.7):
    f = lambda c: (8 * PI * G) ** 2 * ((s * (1 - c) / 2) ** 4 + (s * (1 + c) / 2) ** 4) / s ** 2 / (64 * PI ** 2 * s)
    sig = 0.5 * 2 * PI * integrate.quad(f, -1, 1, epsabs=0, epsrel=1e-13)[0]   # 1/2 identical photons, full sphere
    print(f"  s={s}: sigma(nonzero helicity class) = {sig:.12g};  (4/5) pi G^2 s = {0.8 * PI * s:.12g};"
          f"  unpolarised (2 of 4 classes) = {sig / 2:.12g} = (2/5) pi G^2 s: {0.4 * PI * s:.12g}")

# ------------------------------------------------------------------------------------------------ B
hdr("B  lab-frame Monte Carlo of Gamma/rho^2 (isotropic, unpolarised, incoherent; broad spectrum; explicit boosts)")

def iso(n):
    c = rng.uniform(-1, 1, n); p = rng.uniform(0, 2 * PI, n); s_ = np.sqrt(1 - c * c)
    return np.stack([s_ * np.cos(p), s_ * np.sin(p), c], axis=1)

def boost_to_cm(P, k):
    """boost 4-vectors k (n,4) into the rest frame of P (n,4)."""
    M = np.sqrt(P[:, 0] ** 2 - np.sum(P[:, 1:] ** 2, axis=1))
    b = P[:, 1:] / P[:, :1]; b2 = np.sum(b * b, axis=1); g = P[:, 0] / M
    bk = np.sum(b * k[:, 1:], axis=1)
    k0 = g * (k[:, 0] - bk)
    coef = np.where(b2 > 0, (g - 1) * bk / np.where(b2 > 0, b2, 1), 0.0)
    kv = k[:, 1:] + (coef - g * k[:, 0])[:, None] * b
    return np.column_stack([k0, kv]), M

def mc_gamma(sampler, n=2_000_000, reps=8):
    vals = []
    for _ in range(reps):
        E1, E2 = sampler(n), sampler(n)
        k1 = np.column_stack([E1, E1[:, None] * iso(n)]); k2 = np.column_stack([E2, E2[:, None] * iso(n)])
        P = k1 + k2
        k1c, M = boost_to_cm(P, k1)
        s = M ** 2
        qd = iso(n); q1c = np.column_stack([M / 2, (M / 2)[:, None] * qd])
        t = -2 * (k1c[:, 0] * q1c[:, 0] - np.sum(k1c[:, 1:] * q1c[:, 1:], axis=1))
        uu = -s - t
        msq_opp = (8 * PI) ** 2 * (t ** 4 + uu ** 4) / s ** 2
        # helicity classes uniform over 4: 2 radiate (msq_opp), 2 do not
        rad = rng.integers(0, 2, n)
        msq = rad * msq_opp
        # sigma v_Moller = (1/(4 E1 E2)) * int dPhi2 |M|^2 * (1/2 identical);  int dPhi2 = 4 pi E[.]/(32 pi^2)
        sv = msq / (4 * E1 * E2) * (4 * PI / (32 * PI ** 2)) * 0.5
        # Gamma = (1/2) n^2 E[sigma v] over uniform helicity classes; rho = n <E>
        vals.append(0.5 * np.mean(sv) / np.mean(np.concatenate([E1, E2])) ** 2)
    v = np.array(vals); return v.mean(), v.std(ddof=1) / math.sqrt(len(v))

samplers = {
    "monochromatic w=1": lambda n: np.ones(n),
    "thermal-like (Gamma(3) number spectrum)": lambda n: rng.gamma(3.0, 1.0, n),
    "flat in ln k over 3 decades": lambda n: np.exp(rng.uniform(0, math.log(1e3), n)),
}
for name, smp in samplers.items():
    m, e = mc_gamma(smp)
    print(f"  {name:42s}: Gamma/rho^2 = {m:.5f} +- {e:.5f}   (8 pi/15 = {8 * PI / 15:.5f})")
print("  note: <E1 E2> = <E>^2 for independent energies, so the factorisation sigma v ~ k1 k2 makes the result spectrum-")
print("  independent; the MC verifies that with explicit kinematics, not with the closed form.")

# ------------------------------------------------------------------------------------------------ C
hdr("C  2 Gamma in SI via natural units (eV), and the Delta N_eff that reproduces B&O's 1e-110")
hbar_eVs = 6.582119569e-16; hbarc_eVm = 1.973269804e-7; Mpl = 1.220890e28   # eV (G = 1/Mpl^2)
J_per_eV = 1.602176634e-19
kB_eV = 8.617333262e-5; T0 = 2.7255
Tg = kB_eV * T0
rho_gam_eV4 = PI ** 2 / 15 * Tg ** 4
print(f"  rho_gamma = {rho_gam_eV4:.4e} eV^4 = {rho_gam_eV4 / hbarc_eVm ** 3 * J_per_eV:.4e} J/m^3")
def two_gamma_SI(dNeff):
    rho = 7 / 8 * (4 / 11) ** (4 / 3) * dNeff * rho_gam_eV4             # eV^4
    Gam = 8 * PI / 15 * rho ** 2 / Mpl ** 4                               # eV^4 = pairs per eV^3 per (eV^-1 time)
    return 2 * Gam / hbarc_eVm ** 3 / hbar_eVs, rho
for d in (0.04, 0.1, 0.29, 0.5):
    v, rho = two_gamma_SI(d)
    print(f"  Delta N_eff = {d:5.2f}: rho_GW = {rho / hbarc_eVm ** 3 * J_per_eV:.3e} J/m^3;  2 Gamma = {v:.3e} photons m^-3 s^-1")
dneed = 0.29 * math.sqrt(1e-110 / two_gamma_SI(0.29)[0])
print(f"  2 Gamma = 1e-110 requires Delta N_eff = {dneed:.4f};  ratio at the 2-sigma bound 0.29: {two_gamma_SI(0.29)[0] / 1e-110:.1f}")

# ------------------------------------------------------------------------------------------------ D
hdr("D  |Phi| of eq. 15 / S9 (constant g_*; radiation + matter + Lambda), SI")
Gsi = 6.67430e-11; c = 2.99792458e8; hbar = 1.054571817e-34
H0 = 67.4e3 / 3.0856775814913673e22
rho_g_SI = rho_gam_eV4 / hbarc_eVm ** 3 * J_per_eV
rho_crit = 3 * H0 ** 2 * c ** 2 / (8 * PI * Gsi)
Om_r = rho_g_SI * (1 + 7 / 8 * (4 / 11) ** (4 / 3) * 3.044) / rho_crit
Om_m = 0.315; Om_L = 1 - Om_m - Om_r
rho_co = 7 / 8 * (4 / 11) ** (4 / 3) * 0.29 * rho_g_SI
H = lambda z: H0 * math.sqrt(Om_r * (1 + z) ** 4 + Om_m * (1 + z) ** 3 + Om_L)
pref = 16 * PI / 15 * Gsi ** 2 * hbar * rho_co / c ** 7          # dimensionless x (1/H in s)
# int_0^zmax (1+z)^4/H dz in log variable
f = lambda x: (1 + math.expm1(x)) ** 5 / H(math.expm1(x))       # z = e^x - 1, dz = (1+z) dx
Iz = integrate.quad(f, 0, math.log(1 + 1e28), limit=400, epsrel=1e-10)[0]
analytic_RD = (1e28) ** 3 / 3 / (H0 * math.sqrt(Om_r))
print(f"  Omega_r = {Om_r:.4e}; rho_co(dNeff=0.29) = {rho_co:.3e} J/m^3")
print(f"  |Phi| = {pref * Iz:.3e} s  (RD-only closed form z^3/(3 H0 sqrt(Om_r)): {pref * analytic_RD:.3e} s;  B&O ~1e-25 Hz^-1)")

# ------------------------------------------------------------------------------------------------ E
hdr("E  eq. S11 as printed (my transcription), massless and resonant limits (mpmath)")
mp.mp.dps = 40
def S11_coeff(m, w):
    """dP/dt / [G^2 N^2 sigma^2 (1+2N_phi)] from eq. S11:
       1/(15360 pi w^2) int_{4m^2}^{4w^2} ds / (s^{3/2} sqrt(4w^2-s)) [ s^{3/2} sig (912 m^4 - 136 m^2 s + 7 s^2)
       + 7680 m^7 arccot(2m/sqrt(s-4m^2)) + 480 m^4 (s - 14 m^2) sqrt(s) arcsinh(sqrt(s/(4m^2) - 1)) ]."""
    m = mp.mpf(m); w = mp.mpf(w)
    def br(s):
        sig = mp.sqrt(1 - 4 * m * m / s)
        out = s ** 1.5 * sig * (912 * m ** 4 - 136 * m * m * s + 7 * s * s)
        if m > 0:
            out += 7680 * m ** 7 * mp.acot(2 * m / mp.sqrt(s - 4 * m * m))
            out += 480 * m ** 4 * (s - 14 * m * m) * mp.sqrt(s) * mp.asinh(mp.sqrt(s / (4 * m * m) - 1))
        return out
    # substitution s = 4m^2 + (4w^2-4m^2) sin^2(x) removes both endpoint singularities
    a, b = 4 * m * m, 4 * w * w
    def g(x):
        s = a + (b - a) * mp.sin(x) ** 2
        if s <= a or s >= b or s == 0:
            return mp.mpf(0)          # integrand -> 0 at both ends after the substitution
        ds = 2 * (b - a) * mp.sin(x) * mp.cos(x)
        return br(s) / (s ** 1.5 * mp.sqrt(b - s)) * ds
    I = mp.quad(g, [0, mp.pi / 4, mp.pi / 2])
    return I / (15360 * mp.pi * w * w)
print(f"  m = 0, w = 1: coefficient = {mp.nstr(S11_coeff(0, 1), 15)};  7/(450 pi) = {mp.nstr(7 / (450 * mp.pi), 15)}")
print(f"  photons eq. 8: 3/(25 pi) = {3 / (25 * PI):.10f};  tau_phi/tau (both (1+..) -> 1) = {(3 / (25 * PI)) / float(S11_coeff(0, 1)):.10f}  vs 54/7 = {54 / 7:.10f}")
for d in ("1e-2", "1e-4", "1e-6", "1e-8"):
    dd = mp.mpf(d); m = mp.mpf(1)
    C = S11_coeff(m, m * (1 + dd)) * 2     # (1 + 2 N_phi) -> 2 N_phi
    print(f"  resonant: delta = {d}: [dP/dt]/(G^2 N^2 sigma^2 N_phi m^3 delta) = {mp.nstr(C / dd, 12)}  (1/16 = 0.0625)")

# ------------------------------------------------------------------------------------------------ F
hdr("F  eqs. 16 and 18 (independently typed constants)")
eV_J = J_per_eV
h_ = 0.674
rho_crit_eVm3 = 3 * (100e3 * h_ / 3.0856775814913673e22) ** 2 * c ** 2 / (8 * PI * Gsi) / eV_J
for mDM in (1e-22, 1e-21):
    n = 0.26 * rho_crit_eVm3 / mDM                           # m^-3
    p_over_2pihbar = mDM * 1e-3 / (2 * PI * hbarc_eVm)       # m^-1
    Nphi = n / (4 * PI / 3 * p_over_2pihbar ** 3)
    print(f"  m = {mDM:.0e} eV: N_phi (x_MW = 1, sphere |p| < m v) = {Nphi:.3e}   [eq. 16: 6e87 (1e-22/m)^4 = {6e87 * (1e-22 / mDM) ** 4:.1e}]")
Msun_kg = 1.98847e30
for mDM in (1e-21, 1e-22):
    w = mDM / hbar_eVs                                       # rad/s
    M_Msun = 8800 * PI / w
    Erel = 2 * Msun_kg * c ** 2 * M_Msun / 65
    N0 = Erel / (hbar * w)
    H0nat = hbar_eVs * H0                                    # eV
    W_eV2 = 9 * PI * (mDM / Mpl) ** 2 * 1e-9 * N0 ** 2 * H0nat ** 2 * 0.26 / 256   # eV^2 (= eV/(hbar))
    W = W_eV2 / hbar_eVs * eV_J
    print(f"  m = {mDM:.0e} eV: M = {M_Msun:.3e} Msun, N0 = {N0:.3e}, W_phi(x_MW=1, v=1e-3) = {W:.3e} W"
          f" [eq. 18: {1e14 * (1e-21 / mDM) ** 2:.0e} W]; scalars/s = {W / (mDM * eV_J):.2e}")

# ------------------------------------------------------------------------------------------------ G
hdr("G  CMB stimulation: rate-equation algebra and RJ average in B&O's ring model")
N1, N2, f1, f2 = sp.symbols("N1 N2 f1 f2", positive=True)
net = sp.expand(N1 * N2 * (1 + f1) * (1 + f2) - (1 + N1) * (1 + N2) * f1 * f2)
print("  net =", sp.factor(net - (N1 * N2 * (1 + f1 + f2) - f1 * f2 * (1 + N1 + N2))), "(0 => net = N1N2(1+f1+f2) - f1f2(1+N1+N2))")
# B&O ring model weight (x = K/2w, c = photon CM polar cosine w.r.t. K): (1-x^2)^2 (3 - c^2)^2; RJ: f ~ T/q, q = w(1 +- x c)
num = integrate.dblquad(lambda cc, x: (1 - x * x) ** 2 * (3 - cc * cc) ** 2 / (1 - x * x * cc * cc), 0, 1, -1, 1, epsabs=1e-13)[0]
den = integrate.dblquad(lambda cc, x: (1 - x * x) ** 2 * (3 - cc * cc) ** 2, 0, 1, -1, 1, epsabs=1e-13)[0]
print(f"  RJ <1+f1+f2>/(1+2f(w)) in the ring model = {num / den:.6f}  (task D2 reported 1.049558)")

# ------------------------------------------------------------------------------------------------ H
hdr("H  tau_phi/tau for PHYSICAL coherent profiles (coefficients from the task-A logs)")
def grab(fname, pat):
    txt = open(os.path.join(NOTES, fname)).read()
    return [float(x) for x in re.findall(pat, txt)]
Cg = {"bo_plus": grab("taskA3b_bo_plus_grid2.log", r"C = ([0-9.eE+-]+);")[-1]}
txtA3b = open(os.path.join(NOTES, "taskA3b_smooth.log")).read()
blocks = re.split(r"pattern ", txtA3b)
for b in blocks:
    if b.startswith("binary"):
        Cg["binary"] = float(re.findall(r"C = ([0-9.eE+-]+);", b)[-1])
    if b.startswith("linear"):
        Cg["linear"] = float(re.findall(r"C = ([0-9.eE+-]+);", b)[-1])
txtA4 = open(os.path.join(NOTES, "taskA4_physical.log")).read()
Cs = {}
for key in ("bo_plus", "binary", "linear"):
    Cs[key] = float(re.findall(key + r" grid [^\n]*?C = ([0-9.eE+-]+);", txtA4)[-1])
for key in ("bo_plus", "binary", "linear"):
    print(f"  {key:8s}: C_gamma = {Cg[key]:.8e}, C_phi(m=0) = {Cs[key]:.8e};  tau_phi/tau = C_gamma/C_phi = {Cg[key] / Cs[key]:.4f}"
          f"   (B&O 54/7 = {54 / 7:.4f}; incoherent sigma ratio 12)")
print("  circular profile: both coefficients vanish (no opposite-helicity pairs), ratio undefined.")
