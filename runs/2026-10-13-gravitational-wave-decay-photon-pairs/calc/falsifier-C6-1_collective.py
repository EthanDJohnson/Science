"""Falsifier C6-1 (evidence angle): does Sawyer's collective 'quantum break'
(PRL 124, 101301 (2020), arXiv:1910.08835) undercut C6's claim that the
isotropic-background fusion rate is the incoherent kinetic rate (eq. 14)?

Part A: re-derive sigma(RL -> gamma gamma) from the amplitude magnitudes
        quoted verbatim in Sawyer eq. (2), |A| = 8 pi G T^2/S and 8 pi G U^2/S,
        and the isotropic kinetic coefficient 8 pi/15 (natural units).
Part B: Sawyer's collective growth rate mu = 2 x 8 pi G n (his scaled time
        s = 8 pi G n t, linear-instability eigenvalues +-2 in 1/s), natural
        units -> SI: G n -> (G hbar / c^3) n c = l_P^2 n c  [s^-1].
        Compare with the kinetic per-graviton rate, H0, and plasma detuning,
        for real backgrounds.
Part C: general bound mu/H = 6 (rho_GW/rho_tot) (H/omega) for any epoch.
"""
import math
import sympy as sp

# ---------------- Part A ----------------
G, s, c = sp.symbols('G s c', positive=True)
t = -s*(1-c)/2
u = -s*(1+c)/2
M2 = (8*sp.pi*G)**2*(t**4 + u**4)/s**2          # sum over the two photon channels
dsig_dOmega = M2/(64*sp.pi**2*s)
sigma = sp.Rational(1, 2)*2*sp.pi*sp.integrate(dsig_dOmega, (c, -1, 1))  # 1/2 identical photons
print("A1 sigma(RL->gg) =", sp.simplify(sigma), " expected 4*pi*G**2*s/5:",
      sp.simplify(sigma - sp.Rational(4, 5)*sp.pi*G**2*s) == 0)
w, n, x = sp.symbols('omega n x', positive=True)
sig_unpol = sp.Rational(1, 2)*sp.Rational(4, 5)*sp.pi*G**2*(2*w**2*(1-x))  # 1/2 of pairs are RL/LR
avg = sp.Rational(1, 2)*sp.integrate(sig_unpol*(1-x), (x, -1, 1))
Gamma_V = sp.Rational(1, 2)*n**2*avg
print("A2 Gamma/V / (G^2 rho^2) =", sp.simplify(Gamma_V/(G**2*(n*w)**2)), "= 8 pi/15 ?",
      sp.simplify(Gamma_V/(G**2*(n*w)**2) - 8*sp.pi/15) == 0)

# ---------------- Part B ----------------
hbar = 1.054571817e-34; cc = 2.99792458e8; GN = 6.67430e-11
lP2 = GN*hbar/cc**3
H0 = 67.4e3/3.0857e22                      # s^-1
rho_c = 3*H0**2/(8*math.pi*GN)*cc**2       # J/m^3
rho_gam = 4.17e-14                         # J/m^3 (a T0^4)
print(f"B0 l_P^2 = {lP2:.3e} m^2, H0 = {H0:.3e} s^-1, rho_c c^2 = {rho_c:.3e} J/m^3")

cases = [
    ("DeltaNeff=0.3 at 25 Hz", 0.227*0.3*rho_gam, 25.0),
    ("LVK Omega=2.8e-9 at 25 Hz", 2.8e-9*rho_c, 25.0),
    ("PTA-like Omega=1e-8 at 3.2e-9 Hz", 1e-8*rho_c, 3.2e-9),
    ("DeltaNeff=0.3 all at 1e-10 Hz (extreme)", 0.227*0.3*rho_gam, 1e-10),
]
n_e_igm = 2e-7*1e6                          # m^-3 (mean IGM, 2e-7 cm^-3)
omega_p = 5.64e4*math.sqrt(n_e_igm/1e6)    # rad/s, 5.64e4 sqrt(n_e/cm^-3)
for name, rho, f in cases:
    om = 2*math.pi*f
    nGW = rho/(hbar*om)
    mu = 16*math.pi*lP2*cc*nGW                       # Sawyer growth rate, s^-1
    gam_kin = (16*math.pi/15)*GN**2*rho*om/cc**7*cc**0  # per-graviton kinetic rate
    # SI check of kinetic per-graviton: 2*(8pi/15)G^2 rho^2/c^7 / n
    gam_kin = 2*(8*math.pi/15)*GN**2*rho**2/cc**7/nGW
    detune = omega_p**2/(2*om) if om > omega_p else float('inf')
    lnN = math.log(nGW*(cc/H0)**3)
    print(f"B {name}: rho={rho:.2e} J/m^3, n={nGW:.2e} m^-3, mu={mu:.2e} s^-1, "
          f"mu/H0={mu/H0:.1e}, T_B~lnN/mu={lnN/mu:.1e} s (lnN={lnN:.0f}), "
          f"kinetic/graviton={gam_kin:.1e} s^-1, mu/kinetic={mu/gam_kin:.1e}, "
          f"IGM detuning={detune:.2e} rad/s (omega_p={omega_p:.1f} rad/s)")

# ---------------- Part C ----------------
# mu/H = 16 pi G n / H, n = rho_GW/omega, H^2 = 8 pi G rho_tot/3
# => mu/H = 16 pi G rho_GW/(omega H) = 6 (rho_GW/rho_tot) (H/omega)   (natural units)
for frac in [0.04, 1.0]:
    for H_over_w in [1e-2, 1e-10, 1e-20]:
        print(f"C rho_GW/rho_tot={frac}, H/omega={H_over_w:.0e}: mu/H = {6*frac*H_over_w:.1e}")
# numeric cross-check of the identity at today's values for case 1
rho = 0.227*0.3*rho_gam; om = 2*math.pi*25
lhs = 16*math.pi*lP2*cc*(rho/(hbar*om))/H0
rhs = 6*(rho/rho_c)*(H0/om)
print(f"C check identity (today, case 1): lhs={lhs:.4e}, rhs={rhs:.4e}, ratio={lhs/rhs:.6f}")

# ---------------- Part D ----------------
# Toolkit-independent route to the eq. 14 coefficient: start from the published
# UNPOLARISED gravitational Compton cross section (dossier D-01, Bjerrum-Bohr et al.,
# agreeing with Skobelev 1975):  dsigma/dt (g gamma -> g gamma) = 2 pi G^2 (s^4+u^4)/(s^2 t^2).
# Helicity-summed |M|^2 = 4 (initial avg) * 16 pi s^2 * dsigma/dt; cross s <-> t
# (sum over all helicities is crossing-invariant for bosons) -> g g -> gamma gamma.
S, T, U = sp.symbols('S T U')
dsdt = 2*sp.pi*G**2*(S**4 + U**4)/(S**2*T**2)
sumM2_compton = sp.simplify(4*16*sp.pi*S**2*dsdt)
print("D1 sum|M|^2 (Compton) =", sumM2_compton)
sumM2_fusion = sumM2_compton.subs({S: T, T: S}, simultaneous=True)
print("D2 crossed s<->t, sum|M|^2 (gg->yy) =", sp.simplify(sumM2_fusion))
ss = sp.symbols('ss', positive=True)
fus = sumM2_fusion.subs({S: ss, T: -ss*(1-c)/2, U: -ss*(1+c)/2})
sig_unpol_D = sp.Rational(1, 4)*sp.Rational(1, 2)*2*sp.pi*sp.integrate(fus/(64*sp.pi**2*ss), (c, -1, 1))
print("D3 sigma_unpol(gg->yy) from Compton crossing =", sp.simplify(sig_unpol_D),
      " equals (2 pi/5) G^2 s:", sp.simplify(sig_unpol_D - sp.Rational(2, 5)*sp.pi*G**2*ss) == 0)
sig_D = sig_unpol_D.subs(ss, 2*w**2*(1-x))
GamD = sp.Rational(1, 2)*n**2*sp.Rational(1, 2)*sp.integrate(sig_D*(1-x), (x, -1, 1))
print("D4 Gamma/V/(G^2 rho^2) via Compton crossing =", sp.simplify(GamD/(G**2*(n*w)**2)))
