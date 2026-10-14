"""Falsifier C8, refuter 2 (scale): required vs achievable for B&O's ULDM channel (eqs. 16-18).

SI units throughout unless marked "natural" (hbar = c = 1).
Independent re-implementation (does not import the lens scripts):
 1. eq. 16-18 face value at m = 1e-21 eV, v = 1e-3 (B&O merger scaling E_rel = 2/65 M c^2, ISCO frequency).
 2. Resonance requirement (1/sigma) vs time a Newtonian equal-mass chirp spends in the v^2/2 band.
 3. Three ways to correct the face value: duty cycle, in-band N^2, and both; spread across 1e-22..2e-20 eV.
 4. Geometry: where the resonant (head-on within 2v) kinematics can exist (r <~ hbar c/m) vs binary separation and lambda/2pi.
 5. Bose-factor smearing: final-state momentum spread >= hbar/(2R) for a production region of size R (labelled estimate).
 6. Astrophysical relevance: overdensity x needed for 1 Lsun and for a 10% PTA amplitude effect; soliton x estimate
    from Schive et al. 2014 (PRL 113, 261302) eqs. (3) and (6).
"""
import math

hbar = 1.054571817e-34; c = 2.99792458e8; G = 6.67430e-11; eV = 1.602176634e-19
Msun = 1.98847e30; pc = 3.0856775814913673e16; kpc = 1e3 * pc; Lsun = 3.828e26
rho_crit_h2 = 1.87834e-26  # kg/m^3 per h^2
rho_DM = 0.120 * rho_crit_h2  # cosmic mean DM density, kg/m^3 (Omega_c h^2 = 0.120)
E_Pl = math.sqrt(hbar * c**5 / G)  # J

def setup(m_eV, v=1e-3, Erel_frac=2/65):
    mc2 = m_eV * eV
    w = mc2 / hbar                     # rad/s, resonance omega_s ~ m
    f = w / (2 * math.pi)              # Hz GW frequency
    M = c**3 / (6**1.5 * math.pi * G * f)  # total mass with ISCO GW frequency f (kg)
    Erel = Erel_frac * M * c**2
    N0 = Erel / (hbar * w)
    n = rho_DM / (mc2 / c**2)          # number density at x = 1, m^-3
    p = (mc2 / c) * v                  # momentum m v c... (SI momentum = m v_phys, v_phys = v c)
    cell = (4 * math.pi / 3) * p**3 / (2 * math.pi * hbar)**3
    Nphi = n / cell
    # eq. 17 natural: dP/dt = G^2 m^5 N0^2 v^6 Nphi / 128 -> SI: (mc2)^5/(E_Pl^4 hbar)
    dPdt = (mc2**5 / (E_Pl**4 * hbar)) * N0**2 * v**6 * Nphi / 128
    W = 2 * mc2 * dPdt
    sigma = w * v**2 / 2               # rad/s
    return dict(mc2=mc2, w=w, f=f, M=M, Erel=Erel, N0=N0, Nphi=Nphi, dPdt=dPdt, W=W, sigma=sigma, v=v)

def chirp(s):
    M, f, v = s['M'], s['f'], s['v']
    Mc = M / 4**0.6
    fdot = (96/5) * math.pi**(8/3) * (G*Mc/c**3)**(5/3) * f**(11/3)
    dEdf = (math.pi**(2/3)/3) * G**(2/3) * Mc**(5/3) * f**(-1/3)
    df = f * v**2 / 2
    t_in = df / fdot
    N_band = dEdf * df / (hbar * s['w'])
    return dict(fdot=fdot, t_in=t_in, N_band=N_band, dEdf=dEdf)

print("=== 1. Face value of eqs. 16-18 (B&O merger scaling, x = 1) ===")
s = setup(1e-21)
print(f"m = 1e-21 eV: f_GW = {s['f']:.4e} Hz, M = {s['M']/Msun:.4e} Msun, N0 = {s['N0']:.4e}, N_phi = {s['Nphi']:.4e}")
print(f"  W_phi(face, x=1) = {s['W']:.4e} W  (B&O eq.18: ~1e14 W x_MW);  scalars/s = {s['W']/s['mc2']:.3e}")
print(f"  check N_phi at 1e-22 eV: {setup(1e-22)['Nphi']:.4e} (B&O eq.16: 6e87)")

print("\n=== 2. Required coherence vs achievable (Newtonian equal-mass chirp) ===")
for m in (1e-22, 1e-21, 2e-20):
    s = setup(m); ch = chirp(s)
    req = 1 / s['sigma']
    print(f"m = {m:.0e} eV: sigma = {s['sigma']:.4e} rad/s, required 1/sigma = {req:.4e} s = {req/3.156e7:.3e} yr;"
          f" time in band = {ch['t_in']:.4e} s; achievable/required = {ch['t_in']/req:.4e}")

print("\n=== 3. Corrected power, x = 1 (three corrections) ===")
for m in (1e-22, 1e-21, 2e-20):
    s = setup(m); ch = chirp(s)
    duty = ch['t_in'] * s['sigma']
    inband = (ch['N_band'] / s['N0'])**2
    W = s['W']
    print(f"m = {m:.0e} eV: W_face = {W:.3e} W; duty-cycle x{duty:.3e} -> {W*duty:.3e} W;"
          f" in-band (N_band/N0)^2 = {inband:.3e} -> {W*inband:.3e} W; both -> {W*duty*inband:.3e} W")
    # Energy actually in the band vs E_rel
    print(f"    energy in resonance band = {ch['N_band']*hbar*s['w']:.3e} J = {ch['N_band']*hbar*s['w']/s['Erel']:.3e} of E_rel")

print("\n=== 4. Geometry of the resonant kinematics (m = 1e-21 eV) ===")
s = setup(1e-21)
Rcomp = hbar * c / s['mc2']
lam_red = c / s['w']
Om_orb = math.pi * s['f']
a = (G * s['M'] / Om_orb**2)**(1/3)
r_isco = 6 * G * s['M'] / c**2
r_g = G * s['M'] / c**2
print(f"hbar c/m = {Rcomp:.4e} m; lambda/2pi = c/omega = {lam_red:.4e} m (identical by construction: omega = m)")
print(f"binary separation at f = {a:.4e} m; r_ISCO = {r_isco:.4e} m; GM/c^2 = {r_g:.4e} m")
print(f"production radius / binary separation = {Rcomp/a:.3f}; / r_ISCO = {Rcomp/r_isco:.3f}")
print(f"gravitational fine-structure alpha = G M m/(hbar c) = {r_g/Rcomp:.3f}")
print(f"head-on window 2v = {2*s['v']:.1e} rad; isotropic pair-solid-angle fraction (2v)^2/4 = {(2*s['v'])**2/4:.1e}")

print("\n=== 5. Bose-factor smearing (labelled order-of-magnitude estimate) ===")
for R_over in (1.0, 10.0, 100.0):
    R = R_over * Rcomp
    dp = hbar / (2 * R)
    p_occ = s['mc2'] / c * s['v']
    frac = min(1.0, (p_occ / dp)**3)
    print(f"R = {R_over:g} x hbar c/m: final momentum spread >= {dp/(s['mc2']/c):.3e} m c vs occupied |p| <= {s['v']:.0e} m c;"
          f" occupied fraction of final states ~ {frac:.3e}")

print("\n=== 6. Astrophysical relevance (m = 1e-21 eV) ===")
s = setup(1e-21); ch = chirp(s)
T = (1/200.0) * (s['M']/Msun/65)      # B&O-style signal duration scaling, s
frac_per_x = s['W'] * T / s['Erel']
print(f"signal duration T = {T:.3e} s; face-value converted fraction of E_rel per unit x = {frac_per_x:.3e}")
inband = (ch['N_band']/s['N0'])**2
for label, Wx in (("face", s['W']), ("in-band", s['W']*inband)):
    print(f"  {label}: x for 1 Lsun = {Lsun/Wx:.3e}; x for 10% amplitude loss (20% energy) = {0.2/(Wx*T/s['Erel']):.3e}")
print(f"  hard bound: Omega_phi produced <= frac * Omega_GW <= {frac_per_x:.2e} x (Omega_GW <= 1)")

# Soliton overdensity estimate, Schive et al. 2014 eq. (6) and eq. (3), a = 1
def soliton_x(m_eV, Mh):
    m22 = m_eV / 1e-22
    Mmin = 4.4e7 * m22**-1.5
    Mc = 0.25 * (Mh / Mmin)**(1/3) * Mmin          # Msun, mass within x_c
    # eq.(3): rho(x) = rho0/(1+0.091 (x/xc)^2)^8, rho0 = 1.9 (m/1e-23)^-2 (xc/kpc)^-4 Msun/pc^3
    # M(<xc) = 4 pi rho0 xc^3 I, I = int_0^1 u^2/(1+0.091u^2)^8 du
    Nn = 20000; I = sum(((i+0.5)/Nn)**2/(1+0.091*((i+0.5)/Nn)**2)**8 for i in range(Nn))/Nn
    m23 = m_eV / 1e-23
    # Mc = 4 pi * 1.9 m23^-2 (xc/kpc)^-4 Msun/pc^3 * xc^3 * I ; xc in pc: (xc/kpc)^-4 xc^3 = 1e12 / xc_pc
    xc_pc = 4*math.pi*1.9*m23**-2*1e12*I / Mc
    rho0 = 1.9 * m23**-2 * (xc_pc/1e3)**-4 * Msun / pc**3   # kg/m^3
    return Mc, xc_pc, rho0 / rho_DM

for Mh in (1e12, 1e14, 1e15):
    Mc, xc, x = soliton_x(1e-21, Mh)
    print(f"  soliton (isolated, Schive 2014) in M_h = {Mh:.0e} Msun halo, m = 1e-21 eV: M_c = {Mc:.3e} Msun, x_c = {xc:.3e} pc,"
          f" peak x = {x:.3e}; face W = {s['W']*x:.3e} W = {s['W']*x/Lsun:.3e} Lsun; in-band = {s['W']*inband*x/Lsun:.3e} Lsun")
print(f"  binary mass / soliton mass (M_h = 1e15): {s['M']/Msun/soliton_x(1e-21,1e15)[0]:.1f}")

print("\n=== 7. Best case over binary mass: any binary passing through f = m/(2 pi hbar), m = 1e-21 eV ===")
print("N_eff = gravitons in the resonance band within one coherence time 1/sigma = N_band * min(1, (1/sigma)/t_in);")
print("eq.17/18 W scales as N0^2 at fixed m, v, x, so W_best = W_face(1.8e10 Msun) * (N_eff/N0_face)^2.")
s = setup(1e-21)
Wf, N0f, f, sig = s['W'], s['N0'], s['f'], s['sigma']
best = (0, None)
for k in range(0, 161):
    Mc = 10**(1 + k * 0.0625) * Msun   # chirp mass 1e1 .. 1e11 Msun
    fdot = (96/5) * math.pi**(8/3) * (G*Mc/c**3)**(5/3) * f**(11/3)
    dEdf = (math.pi**(2/3)/3) * G**(2/3) * Mc**(5/3) * f**(-1/3)
    df = f * s['v']**2 / 2
    t_in = df / fdot
    Nb = dEdf * df / (hbar * s['w'])
    Neff = Nb * min(1.0, (1/sig) / t_in)
    W = Wf * (Neff / N0f)**2
    # the binary must not have merged before f: ISCO frequency of total mass M = 4^0.6 Mc must exceed f
    M = 4**0.6 * Mc
    f_isco = c**3 / (6**1.5 * math.pi * G * M)
    if f_isco >= f and W > best[0]:
        best = (W, Mc/Msun, t_in, Neff)
    if k % 16 == 0:
        print(f"  Mc = {Mc/Msun:.2e} Msun: t_in = {t_in:.3e} s, N_band = {Nb:.3e}, N_eff = {Neff:.3e}, W = {W:.3e} W (x=1), pre-ISCO = {f_isco >= f}")
print(f"  maximum over pre-ISCO binaries: W = {best[0]:.3e} W x_MW at Mc = {best[1]:.3e} Msun (t_in = {best[2]:.3e} s, N_eff = {best[3]:.3e})")
fb_merger = 200.0 / (2*math.pi*150.0)   # B&O GW150914 inputs sigma_w = 200 rad/s, f = 150 Hz (scale-free ratio)
print(f"  B&O's own merger packet: fractional bandwidth sigma_w/omega_s = {fb_merger:.3f}; eq.17 needs {s['v']**2/2:.1e}; mismatch = {fb_merger/(s['v']**2/2):.3e}")
print(f"  generous merger bound (face rate for t_in only): energy per merger <= {Wf*chirp(s)['t_in']:.3e} J x = {Wf*chirp(s)['t_in']/s['Erel']:.3e} of E_rel per unit x")
