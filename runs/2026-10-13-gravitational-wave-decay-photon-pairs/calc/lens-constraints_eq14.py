"""Constraints lens: B&O eq. 14 against kinetic theory, and the SGWB's cosmic photon injection.

Part A. Independent route to eq. 14. For an INCOHERENT, isotropic, unpolarised graviton gas of number density n
at angular frequency w, the Boltzmann collision rate per volume (identical initial particles: 1/2) is
    Gamma = (1/2) n^2 < sigma_unpol(s) (1 - cos theta) >_iso,  s = 2 w^2 (1 - cos theta).
sigma from qft_second_order (physical helicity amplitudes, final photon 1/2 included). B&O eq. 14 says
Gamma = 8 pi G^2 rho^2 / 15 (pairs per volume per time), rho = n w. Natural units hbar = c = 1, G = 1.
Part B. SI rates and cosmic energy injection for a primordial SGWB at the DeltaN_eff bound, with and without
CMB stimulation (1 + 2 f), f = 1/(e^{hbar w/kT} - 1); integrate Delta rho_gamma / rho_gamma over ln a. The
plasma cut-off (lens-constraints_plasma.py) is reported separately; here it is ignored (generous to B&O).
"""
import sys, math
import numpy as np
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import qft_second_order as q2

print("=== Part A: eq. 14 coefficient by kinetic theory ===")
s = 4.0
sRL = q2.sigma_total(s, "R", "L", final="photon")
sRL_cf = q2.sigma_total_massless_closed_form(s, "R", "L", final="photon")
sRR = q2.sigma_total(s, "R", "R", final="photon")
spp = q2.sigma_total(s, "plus", "plus", final="photon")
spx = q2.sigma_total(s, "plus", "cross", final="photon")
print(f"  sigma(R,L)/(pi G^2 s) numeric = {sRL/(math.pi*s):.6f}, closed form = {sRL_cf/(math.pi*s):.6f} (4/5 = 0.8)")
print(f"  sigma(R,R)/(pi G^2 s) = {sRR/(math.pi*s):.3e} (selection rule: 0)")
print(f"  sigma(plus,plus)/(pi G^2 s) = {spp/(math.pi*s):.6f}, sigma(plus,cross) = {spx/(math.pi*s):.6f} (2/5 = 0.4)")
sig_unpol = 0.25 * (2 * sRL + 2 * sRR) / s       # per unit s, average over (R,L),(L,R),(R,R),(L,L)
print(f"  sigma_unpol/(pi G^2 s) = {sig_unpol/math.pi:.6f}")

# isotropic average through beams_pair_rate (two plane waves of equal w, h; average of linear pol pairs)
def gamma_over_n2(theta):
    tot = 0.0
    for p1, p2 in (("plus", "plus"), ("plus", "cross"), ("cross", "plus"), ("cross", "cross")):
        r = q2.beams_pair_rate(1.0, 1e-3, 1.0, 1e-3, theta, p1, p2, final="photon", G=1.0)
        tot += 0.25 * r["pair_rate"] / (r["n1"] * r["n2"])
    return tot, r["rho1"] / r["n1"]

for nGL in (8, 12, 16):
    x, wts = np.polynomial.legendre.leggauss(nGL)
    acc = 0.0
    for xi, wi in zip(x, wts):
        th = math.acos(xi)
        if th < 1e-9:
            continue
        g, _ = gamma_over_n2(th)
        acc += wi * 0.5 * g          # d(cos)/2 isotropic average of n1 n2 sigma v
    Gamma_over_n2 = 0.5 * acc         # 1/2 identical initial gravitons in one gas
    # with w = 1, rho = n w = n, so Gamma/rho^2 = Gamma/n^2
    print(f"  Gauss-Legendre n = {nGL:2d}: Gamma/(G^2 rho^2) = {Gamma_over_n2:.6f};  8 pi/15 = {8*math.pi/15:.6f};"
          f" ratio = {Gamma_over_n2/(8*math.pi/15):.6f}")
print("  closed form: (1/2) (2 pi/5)(2)(4/3) = 8 pi/15 exactly: <(1-cos)^2>_iso = 4/3")

print("\n=== Part B: SGWB at DeltaN_eff bounds; eq. 14 in SI and cosmic injection ===")
hbar = 1.054571817e-34; c = 2.99792458e8; e = 1.602176634e-19; kB = 1.380649e-23
G_SI = 6.67430e-11
MPl_eV = 1.220890e19 * 1e9
eV4_to_m3s = (e / (hbar * c)) ** 3 * (e / hbar)       # 1 eV^4 rate density -> m^-3 s^-1
Jm3_to_eV4 = (hbar * c / e) ** 3 / e                    # 1 J/m^3 -> eV^4
T0 = 2.7255
a_rad = 7.565767e-16
rho_g0 = a_rad * T0 ** 4
print(f"  rho_CMB today = {rho_g0:.4e} J/m^3")
Hub = 67.4e3 / 3.0857e22
Om = 0.315
rho_c = 3 * Hub ** 2 / (8 * math.pi * G_SI) * c ** 2
Og = rho_g0 / rho_c
Or = Og * (1 + 0.2271 * 3.046)
OL = 1 - Om - Or
print(f"  rho_crit c^2 = {rho_c:.4e} J/m^3, Omega_gamma = {Og:.4e}, Omega_r = {Or:.4e}")

def gamma14_SI(rho_J):
    rho = rho_J * Jm3_to_eV4
    return 8 * math.pi / 15 * rho ** 2 / MPl_eV ** 4 * eV4_to_m3s

for dN in (0.3, 0.1, 0.05):
    rgw = dN * 0.2271 * rho_g0
    G14 = gamma14_SI(rgw)
    print(f"  DeltaN_eff = {dN:4.2f}: rho_GW = {rgw:.3e} J/m^3, eq.14 pair rate = {G14:.3e} m^-3 s^-1,"
          f" photon rate = {2*G14:.3e} m^-3 s^-1")
# LVK-limited (Omega_GW(25 Hz) <= 2.8e-9, flat; treated as total, [D-34])
rgw_lvk = 2.8e-9 * rho_c
print(f"  LVK O1-O4a (Omega 2.8e-9 as total): rho_GW = {rgw_lvk:.3e} J/m^3, pair rate = {gamma14_SI(rgw_lvk):.3e} m^-3 s^-1")

def H(z):
    return Hub * math.sqrt(Or * (1 + z) ** 4 + Om * (1 + z) ** 3 + OL)

def injection(f0, dN, stim, zmin, zmax, n=4000):
    """Delta rho_gamma/rho_gamma accumulated from zmin to zmax (energy redshifts like radiation)."""
    r = dN * 0.2271                     # rho_GW/rho_gamma, constant for a primordial background
    lnz = np.linspace(math.log(1 + zmin), math.log(1 + zmax), n)
    acc = 0.0
    for i in range(n - 1):
        zz = math.exp(0.5 * (lnz[i] + lnz[i + 1])) - 1
        dl = lnz[i + 1] - lnz[i]
        rg = rho_g0 * (1 + zz) ** 4
        G = gamma14_SI(r * rg)
        Ephot = hbar * 2 * math.pi * f0 * (1 + zz)   # J per photon
        x = Ephot / (kB * T0 * (1 + zz))
        fac = (1 + (2 / math.expm1(x) if x < 700 else 0.0)) if stim else 1.0
        q = 2 * G * Ephot * fac                       # J m^-3 s^-1
        acc += q / (H(zz) * rg) * dl
    return acc

print("  Delta rho_gamma/rho_gamma injected (eq. 14, DeltaN_eff = 0.3, plasma ignored):")
for f0 in (25.0, 1e4, 1e9, 1e14):
    for (lab, z1, z2) in (("y  1e3-1e5", 1e3, 1e5), ("mu 1e5-3e6", 1e5, 3e6)):
        a1 = injection(f0, 0.3, False, z1, z2)
        a2 = injection(f0, 0.3, True, z1, z2)
        a2b = injection(f0, 0.3, True, z1, z2, n=6000)
        print(f"    f0 = {f0:8.1e} Hz, {lab}: unstimulated {a1:.3e}, stimulated {a2:.3e} (n=6000: {a2b:.3e})")
print("  FIRAS thresholds: mu < 9e-5 -> Delta rho/rho < ~6.4e-5 (mu = 1.4 Delta rho/rho); |y| < 1.5e-5 -> Delta rho/rho < 6e-5 [D-08]")
print("  analytic scale (stimulated, RJ): Delta rho/rho per e-fold ~ (8 pi/15) r^2 rho_g 4 kT/(H rho_g) ~ r^2 (T/M_Pl)^3 x O(10)")
for z in (1e3, 1e5, 3e6):
    T_eV = 8.617333e-5 * T0 * (1 + z)
    print(f"    z = {z:.0e}: (T/M_Pl)^3 = {(T_eV/MPl_eV)**3:.3e}")

print("\n=== Part C: depletion time of a primordial SGWB today (eq. 14 taken at face value) ===")
for f0 in (25.0, 1e-8 * 3.17):
    rgw = 0.3 * 0.2271 * rho_g0
    G14 = gamma14_SI(rgw)
    Eph = hbar * 2 * math.pi * f0
    x = Eph / (kB * T0)
    for stim in (False, True):
        fac = (1 + (2 / math.expm1(x) if x < 700 else 0.0)) if stim else 1.0
        tau = rgw / (2 * G14 * Eph * fac)
        print(f"  f0 = {f0:.3e} Hz, stim={stim}: tau_deplete = {tau:.3e} s = {tau/4.35e17:.3e} t_H")
