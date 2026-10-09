"""Engineer lens: cost table and orders-of-magnitude gaps for building/widening traversable wormholes.
All inputs SI unless stated. Geometric-unit formulas are converted with c^4/G (N) and c^2/G (kg/m).
Sources of required-side formulas:
  - Ellis / Morris-Thorne throat stress rho = -c^4/(8 pi G b0^2) (dossier Q-24, Q-27); exotic 'mass' Omega = -2 b0 c^2/G (Q-26)
  - Ford-Roman band a0 <~ (r0/(8 f^4 lP))^(1/3) lP, f = 0.01 (Q-21)
  - Thin shell (flat limit M->0 of Q-29): sigma = -c^4/(2 pi G a) J/m^2; shell mass = 4 pi a^2 sigma/c^2 = -2 a c^2/G
  - MMP (arXiv:1807.04726 eqs 5.30-5.31, 5.28, 5.43; hbar=c=1): r_e = sqrt(pi) q lP/g ; ell = 16 r_e^3/(G q);
      |E_min| = G q^2/(256 r_e^3) = g^2/(256 pi r_e) ; T = 1/(2 pi ell); validity ell << q^3 lP
      N_eff extension (MY ASSUMPTION): Casimir term scales by N_eff -> ell = 16 r_e^3/(G N q), |E_min| = N^2 g^2/(256 pi r_e)
  - extremal mouth: M = r_e c^2/G ; horizon field (SI, extremal RN, F = g_m B): B_h = c^2 sqrt(mu0/(4 pi G))/r_e
  - Schwinger-type pair creation exponent for an extremal magnetic pair in field B: pi M c^3/(hbar g_m B), g_m = sqrt(4 pi G/mu0) M
      (reduces to S_BH = pi r_e^2/lP^2 at B = B_h; Garfinkle-Strominger-type e^{S} enhancement noted, not derived here)
Demonstrated anchors (see analysis file for sourcing):
  Casimir smallest measured gap 0.2 um (D-19); 45.5 T DC (Hahn 2019 Nature title); 1200 T destructive [search-summary];
  38 pK [search-summary]; world primary energy 592 EJ in 2024 [search-summary]; Sycamore 164 two-qubit gates, N = 7 Majoranas (Q-37).
"""
import math
G=6.67430e-11; c=2.99792458e8; hbar=1.054571817e-34; kB=1.380649e-23; mu0=1.25663706212e-6
lP=math.sqrt(hbar*G/c**3); EP=math.sqrt(hbar*c**5/G); MP=math.sqrt(hbar*c/G); eV=1.602176634e-19
Msun=1.98847e30
L=lambda x: math.log10(x)
def hdr(s): print("\n=== "+s+" ===")

# ---------------- demonstrated anchors ----------------
d_cas=0.2e-6                       # m, smallest measured Casimir gap (Decca 2003, D-19)
u_cas=math.pi**2*hbar*c/(720*d_cas**4)   # J/m^3 magnitude, ideal plates
P_cas=math.pi**2*hbar*c/(240*d_cas**4)   # Pa
sig_cas=math.pi**2*hbar*c/(720*d_cas**3) # J/m^2 magnitude per unit plate area
u_cas10=math.pi**2*hbar*c/(720*(10e-9)**4)
B_dc=45.5; B_pulse=1200.0
T_lab=38e-12
E_world=592e18                      # J per year (2024)
gates_demo=164; N_demo=7
hdr("Demonstrated anchors")
print("Casimir at 0.2 um: |u| = %.3e J/m^3, P = %.3e Pa, |E/A| = %.3e J/m^2"%(u_cas,P_cas,sig_cas))
print("Casimir at 10 nm (ideal, unmeasured): |u| = %.3e J/m^3"%u_cas10)
print("B: %.1f T DC, %.0f T destructive; T_min = %.1e K; world energy = %.3e J/yr (= %.3e kg c^2/yr)"%(B_dc,B_pulse,T_lab,E_world,E_world/c**2))
print("lP = %.4e m, EP = %.4e J, MP = %.4e kg"%(lP,EP,MP))

# ---------------- 1. Ellis / Morris-Thorne ----------------
hdr("1. Ellis/Morris-Thorne throat: required vs Casimir")
f=0.01
for label,b0 in [("qubit (b0=1 um)",1e-6),("1 kg (b0=0.1 m)",0.1),("human (b0=1 m)",1.0),("human, MM tidal (b0=1.5e7 m)",1.5e7)]:
    rho=c**4/(8*math.pi*G*b0**2)    # |rho| in J/m^3 (= Pa)
    Om=2*b0*c**2/G                  # kg
    band=(b0/(8*f**4*lP))**(1/3)*lP
    print("%-30s |rho|=%.2e J/m^3  gap vs Casimir(0.2um)=%.1f  vs ideal 10nm=%.1f orders; |Omega|=%.2e kg; FR band<=%.2e m (vs 0.2um gap: %.1f orders thinner; vs 1e-10 m atom: %.1f)"%(
        label,rho,L(rho/u_cas),L(rho/u_cas10),Om,band,L(d_cas/band),L(1e-10/band)))
b_eq=math.sqrt(c**4/(8*math.pi*G*u_cas))
print("Scaling |rho| ~ b0^-2: equals Casimir |u|(0.2um) only at b0 = %.2e m = %.2e ly"%(b_eq,b_eq/9.4607e15))
b_band=(d_cas/lP)**3*8*f**4*lP
print("Scaling band ~ b0^(1/3): band reaches 0.2 um only at b0 = %.2e m (observable-universe radius ~4.4e26 m): %.1f orders larger"%(b_band,L(b_band/4.4e26)))
b_band_atom=(1e-10/lP)**3*8*f**4*lP
print("band reaches atomic 1e-10 m at b0 = %.2e m"%b_band_atom)
# Casimir plate area to supply exotic mass-energy for 1 m throat
A_need=2*1.0*c**2/G*c**2/sig_cas
print("Plate area at 0.2 um to hold |Omega| c^2 for b0=1 m: %.2e m^2 (Earth surface 5.1e14 m^2: %.1f orders)"%(A_need,L(A_need/5.1e14)))

# ---------------- 2. thin shell ----------------
hdr("2. Visser thin shell, flat-space limit")
for label,a in [("qubit a=1 um",1e-6),("1 kg a=0.1 m",0.1),("human a=1 m",1.0)]:
    sig=c**4/(2*math.pi*G*a); ms=2*a*c**2/G
    print("%-16s |sigma|=%.2e J/m^2 gap vs Casimir |E/A|(0.2um)=%.1f orders; |m_shell|=%.2e kg"%(label,sig,L(sig/sig_cas),ms))
a_eq=c**4/(2*math.pi*G*sig_cas)
print("Scaling sigma ~ 1/a: equals Casimir areal energy only at a = %.2e m (%.1f orders beyond observable universe)"%(a_eq,L(a_eq/4.4e26)))

# ---------------- 3. MMP Standard-Model version ----------------
hdr("3. MMP, Standard-Model embedding (r_e << 1/TeV)")
def mmp(r_e,g,N=1.0):
    q=g*r_e/(math.sqrt(math.pi)*lP)               # flux units
    ell=16*r_e**3/(lP**2*N*q)                       # m  (G=lP^2 in hbar=c=1 lengths)
    Emin=N**2*g**2*hbar*c/(256*math.pi*r_e)         # J
    T=hbar*c/(2*math.pi*ell*kB)                     # K
    M=r_e*c**2/G
    Bh=c**2*math.sqrt(mu0/(4*math.pi*G))/r_e
    valid=ell/(q**3*lP)
    return q,ell,Emin,T,M,Bh,valid
def pair_exp(M,B):
    gm=math.sqrt(4*math.pi*G/mu0)*M
    return math.pi*M**2*c**3/(hbar*gm*B)   # Schwinger form pi m^2 c^3/(hbar * charge * field)
rTeV=hbar*c/(1e12*eV)
print("1/TeV = %.3e m"%rTeV)
for g in (0.06,0.3):
  for N in (1,54):
    q,ell,Emin,T,M,Bh,valid=mmp(rTeV,g,N)
    print("g=%.2f N_eff=%2d r_e=%.2e m: q=%.2e, ell=%.3e m, |E_min|=%.2e J = %.2e GeV, T_req<%.2e K, M=%.2e kg/mouth, B_h=%.2e T, ell/(q^3 lP)=%.1e"%(
        g,N,rTeV,q,ell,Emin,Emin/eV/1e9,T,M,Bh,valid))
q,ell,Emin,T,M,Bh,valid=mmp(rTeV,0.06,1)
S=math.pi*rTeV**2/lP**2
print("Formation mass-energy (2 mouths) = %.2e J = %.2e yr of world primary energy (gap %.1f orders vs 1 yr)"%(2*M*c**2,2*M*c**2/E_world,L(2*M*c**2/E_world)))
print("Pair-creation exponent at 1200 T: %.2e ; at 45.5 T: %.2e ; at B_h: %.3e (S_BH=%.3e). Field gap B_h/1200 T = %.1f orders"%(
    pair_exp(M,B_pulse),pair_exp(M,B_dc),pair_exp(M,Bh),S,L(Bh/B_pulse)))
print("Payload: 1 kg c^2 = %.2e J vs |E_min|(g=0.06,N=54) = %.2e J: gap %.1f orders; size gap 0.1 m / 1/TeV = %.1f orders"%(
    c**2,mmp(rTeV,0.06,54)[2],L(c**2/mmp(rTeV,0.06,54)[2]),L(0.1/rTeV)))
print("Mouth mass in GeV/c^2: %.2e (vs MoEDAL monopole exclusion 75 GeV: %.1f orders)"%(M*c**2/eV/1e9,L(M*c**2/eV/1e9/75)))
print("Flux units needed (monopole-equivalents): %.2e ; demonstrated: 0"%q)

# ---------------- 4. MMP widened / MM human scale ----------------
hdr("4. Widened MMP / Maldacena-Milekhin human scale")
r_h=1.5e7
for g in (0.06,):
    q,ell,Emin,T,M,Bh,valid=mmp(r_h,g,1)
    print("pure MMP, N=1, g=%.2f, r_e=1.5e7 m: |E_min|=%.2e J (cf. 1 photon of 1 meV = 1.6e-22 J); M=%.2e kg = %.2e Msun; B_h=%.2e T (gap vs 45.5 T: %.1f, vs 1200 T: %.1f orders)"%(
        g,Emin,M,M/Msun,Bh,L(Bh/B_dc),L(Bh/B_pulse)))
# N_eff needed for payload energy with g^2 N <= 1  -> |E_min| <= N hbar c/(256 pi r_e)
for label,mpay,r in [("1 kg, r_e=0.1 m",1.0,0.1),("human 70 kg, r_e=1.5e7 m",70.0,1.5e7),("ship 1e3 kg, r_e=1.5e7 m",1e3,1.5e7)]:
    Nreq=mpay*c**2*256*math.pi*r/(hbar*c)
    print("%-26s N_eff needed (with g^2 N = 1) >= %.2e ; vs SM 54: %.1f orders; vs MM cap 1e32: %.1f orders"%(label,Nreq,L(Nreq/54),L(Nreq/1e32)))
print("(MM 2020 quote their own requirement N_f > 1e52 for the 1e3 kg ship; my scaling differs by the factor above -> order-of-magnitude only)")
Mmm=r_h*c**2/G
print("MM formation mass-energy 2 mouths = %.2e J = %.2e yr world energy (%.1f orders)"%(2*Mmm*c**2,2*Mmm*c**2/E_world,L(2*Mmm*c**2/E_world)))
print("MM pair-creation exponent at 1200 T: %.2e ; S_BH = %.2e"%(pair_exp(Mmm,B_pulse),math.pi*r_h**2/lP**2))
# CMB boost requirement
gam=2e12   # MM eq 3.27 gamma = ell/r_e (Q-02)
E_tol=1.0*eV
T_req=E_tol/(kB*gam**2)
print("CMB seen boosted by gamma^2=%.1e: 2.725 K -> %.2e eV per photon. Ambient T for <1 eV: %.2e K (gap vs CMB %.1f orders, vs 38 pK lab %.1f orders)"%(
    gam**2,gam**2*kB*2.725/eV,T_req,L(2.725/T_req),L(T_lab/T_req)))
T_dark=1e-26*eV/kB
print("Dark sector T < 1e-26 eV = %.2e K (gap vs 38 pK lab: %.1f orders)"%(T_dark,L(T_lab/T_dark)))
H0=67.4e3/3.0857e22; OL=0.685; HL=H0*math.sqrt(OL)
for Tt,lab in [(T_req,"photon <1 eV"),(T_dark,"1e-26 eV")]:
    t=math.log(2.725/Tt)/HL/3.156e7
    print("Cosmic expansion cools CMB to %.1e K (%s) after ~%.2e yr (Lambda-dominated, H_L=%.2e /s)"%(Tt,lab,t,HL))
TdS=hbar*HL/(2*math.pi*kB)
print("de Sitter floor T_dS = %.2e K"%TdS)

# ---------------- 5. FGM 2019 ----------------
hdr("5. FGM 2019 (charged pair + cosmic string, Hartle-Hawking state)")
M_HH=hbar*c**3/(8*math.pi*G*kB*2.725)
print("Schwarzschild-formula mass with T_H = T_CMB: %.2e kg (Moon 7.35e22 kg); smaller holes are hotter than the CMB"%M_HH)
for M in (M_HH,Msun):
    for d in (1e3*G*M/c**2,):
        F=2*G*M**2/d**2
        print("M=%.2e kg, d=1e3 GM/c^2=%.2e m: string tension mu c^2 = F = %.2e N, G mu/c^2 = %.2e"%(M,d,F,G*F/c**4))

# ---------------- 6. EDM ----------------
hdr("6. Einstein-Dirac-Maxwell: q/mu < 1 (Planck units) requirement")
alpha=1/137.035999
for name,m_GeV,Qf in [("electron",0.000511,1.0),("top quark",172.6,2/3)]:
    for conv,qP in [("Gaussian q=Qf*sqrt(alpha)",Qf*math.sqrt(alpha)),("HL q=Qf*sqrt(4 pi alpha)",Qf*math.sqrt(4*math.pi*alpha))]:
        mu=m_GeV*1e9*eV/(MP*c**2)
        print("%-9s %-28s q/mu = %.2e (gap %.1f orders); mass needed for q/mu<1: %.2e GeV"%(name,conv,qP/mu,L(qP/mu),qP*MP*c**2/eV/1e9))
print("Kain static throat 75-500 lP = %.1e to %.1e m"%(75.28*lP,498.4*lP))

# ---------------- 7. quantum-simulation analogue ----------------
hdr("7. Quantum-processor analogue (sparse SYK teleportation)")
eps_eff=math.log(2)/gates_demo
print("Sycamore: F < 1/2 of noiseless at 164 gates -> effective error per gate >= %.2e"%eps_eff)
for N in (20,50,100):
    k=4; nT=10
    Gt=2*(k*N)*(N/2)*nT*2   # terms * JW string CNOTs * Trotter steps * 2 sides
    eps_need=math.log(2)/Gt
    print("N=%3d Majoranas, k=%d, %d Trotter steps: ~%.1e two-qubit gates (%.1f orders above 164); error/gate needed <= %.1e (%.1f orders below Sycamore effective)"%(
        N,k,nT,Gt,L(Gt/gates_demo),eps_need,L(eps_eff/eps_need)))
# payload as teleported quantum state
for lab,n in [("qubit",1),("1 kg water (atoms)",1000/18.015*6.022e23*3),("70 kg human (atoms)",70*1000/18.015*6.022e23*3)]:
    print("%-22s degrees of freedom ~ %.1e; gap vs 1 teleported qubit: %.1f orders"%(lab,n,L(n)))
R=0.1; E=1.0*c**2
print("Bekenstein bound for 1 kg in R=0.1 m: %.2e bits"%(2*math.pi*R*E/(hbar*c*math.log(2))))

# ---------------- 8. Test sensitivities ----------------
hdr("8. Nearest tests: required vs achieved")
print("S2 orbit: need 1e-6 m/s^2, achieved 4e-4 (gap %.1f), projected 2e-5 (gap %.1f)"%(L(4e-4/1e-6),L(2e-5/1e-6)))
lam=1.3e-3; D_earth=1.27e7; res=lam/D_earth
uas=math.pi/180/3600*1e-6
print("EHT nominal resolution lambda/D = %.2e rad = %.1f uas"%(res,res/uas))
for M_s,Dist,lab in [(1e4,1e3*3.0857e16,"1e4 Msun at 1 kpc"),(1e4,1e4*3.0857e16,"1e4 Msun at 10 kpc"),(4.3e6,8.28e3*3.0857e16,"Sgr A* (4.3e6 Msun, 8.28 kpc)")]:
    rg=G*M_s*Msun/c**2
    th_RN=2*4*rg/Dist; th_S=2*3*math.sqrt(3)*rg/Dist
    print("%-32s shadow diam: extremal RN %.3f uas vs Schwarzschild %.3f uas (RN/S = %.3f); gap to resolution %.1f orders"%(lab,th_RN/uas,th_S/uas,th_RN/th_S,L(res/th_RN)))
t_echo=9.4e3*3.156e7
print("MM echo delay ~ pi ell/c = 9.4e3 yr = %.2e s vs ~2 yr observing run: %.1f orders"%(t_echo,L(9.4e3/2)))
