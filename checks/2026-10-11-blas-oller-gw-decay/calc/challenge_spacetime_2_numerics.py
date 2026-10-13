"""Referee 2 (Task B, numerics): independent re-derivation of the load-bearing numbers.
A. algebra (sympy): V_eff, 3/(25 pi), diamond factor 4pi/(3 sig), eq.9/10 -> N_gamma(tau)
B. GW150914-like SI numbers from scratch (CODATA constants)
C. own radial-transform of an outgoing wave psi = h_l(wr) Y_l0 e^{-iwt} (steady, w=1),
   scalar proxy weight rho ~ s^2, different windows and an exp(-r/R) regulator:
   r_min^-3 scaling (l=0) and l=2 / l=0 near-field ratio.
"""
import numpy as np, sympy as sp
from scipy.special import spherical_jn, spherical_yn

print("=== A. algebra ===")
G,N,w,sig,eps,t,E,x,D,lam = sp.symbols('G N w sigma epsilon t E x D lambda', positive=True)
rate8 = 3*G**2*N**2*w**3*sig**2/(25*sp.pi)
Veff = sp.Rational(8,15)*sp.pi*G**2*(N*w)**2/rate8
print("V_eff from eq.8 =", sp.simplify(Veff), "; equals 5 lam^3/(9 pi eps^2) with lam=2pi/w, eps=sig/w:",
      sp.simplify(Veff - (5*(2*sp.pi/w)**3/(9*sp.pi*(sig/w)**2)))==0)
L = sig - sp.Abs(x)
intL = sp.integrate((sig-x),(x,0,sig))*2; intL2 = sp.integrate((sig-x)**2,(x,0,sig))*2
print("int L dE =", intL, " int L^2 dE =", intL2, " T_eff = 2pi int L^2/(int L)^2 =", sp.simplify(2*sp.pi*intL2/intL**2))
Ng = G**2*N**2*6*w**3*sig**2*t/(25*sp.pi)
tau = 25*sp.pi/(6*G**2*(N*w)**2*w*sig**2)
print("eq.9 at t = tau(eq.10):", sp.simplify(Ng.subs(t,tau)), "photon(s)  -> tau = time to FIRST photon")
print("steady mapping N=L t/w, sig=1/t:", sp.simplify(rate8.subs({N:sp.Symbol('L')*t/w, sig:1/t})), "=",
      float(3/(25*np.pi)), "G^2 L^2 w")

print("\n=== B. GW150914-like, SI ===")
Gn=6.67430e-11; c=2.99792458e8; hbar=1.054571817e-34; Msun=1.98847e30
Erel=2*Msun*c**2; om=2*np.pi*150.0; tm=5e-3; sg=1/tm
N0=Erel/(hbar*om)
tP2=hbar*Gn/c**5            # G in units hbar=c=1 -> s^2 when energies are in 1/s
r8=3*tP2**2*N0**2*om**3*sg**2/(25*np.pi)
tauSI=25*np.pi/(6*tP2**2*(N0*om)**2*om*sg**2)
print(f"N0 = {N0:.4e}; eq.8 dP/dt = {r8:.4e} pairs/s; photons/s = {2*r8:.4e}; tau = {tauSI:.4e} s; rate*t_m = {r8*tm:.4e}; tau/t_m = {tauSI/tm:.3e} (B&O require tau << 1/sig)")
Dm=410*3.0857e22; kw=om/c
print(f"w D = {kw*D if False else kw*Dm:.4e}; focus strain l=0 (2 w D h) = {2*kw*Dm*1e-21:.3f}")
lam_m=c/150; print(f"lambda = {lam_m/1e3:.1f} km, lambda/2pi = {lam_m/2/np.pi/1e3:.1f} km; GM_tot/c^2 (65 Msun) = {Gn*65*Msun/c**2/1e3:.0f} km")

print("\n=== C. own outgoing-wave radial transform (w=1, steady) ===")
gaunt = {0:{0:1/np.sqrt(4*np.pi)}, 2:{0:0.28209479177388197,2:0.18022375157287848,4:0.24179553580619426}}
def h1(l,x): return spherical_jn(l,x)+1j*spherical_yn(l,x)
def win(r,rmin,kind):
    if kind=='exp8': return 1-np.exp(-(r/rmin)**8)
    if kind=='poly':  # C2 smoothstep from 0.5 rmin to 1.5 rmin
        u=np.clip((r-0.5*rmin)/rmin,0,1); return u**3*(10-15*u+6*u**2)
def K(l,rmin,kind,R):
    rmax=6*R; dr=0.04
    r=np.arange(dr*0.5, rmax, dr)
    f=r**2*h1(l,r)**2*win(r,rmin,kind)*np.exp(-r/R)
    q=np.concatenate([np.linspace(1e-3,1.9,300), 2-np.geomspace(0.1,1e-5,500)])
    s=4-q**2; tot=np.zeros_like(q)
    for L,cL in gaunt[l].items():
        RL=np.array([np.sum(spherical_jn(L,qq*r)*f)*dr for qq in q])
        tot+=cL**2*np.abs(RL)**2
    y=q**2*s**2*tot
    return np.trapezoid(y,q)
for kind in ['exp8','poly']:
    print(f"window {kind}:")
    for rmin in [1.0, 2*np.pi, 2*2*np.pi]:
        k0a=K(0,rmin,kind,40); k0b=K(0,rmin,kind,80)
        k2a=K(2,rmin,kind,40); k2b=K(2,rmin,kind,80)
        print(f"  r_min = {rmin/2/np.pi:.3f} lambda: K_l0 = {k0a:.4e} (R=40) {k0b:.4e} (R=80); K_l2 = {k2a:.4e} / {k2b:.4e};  K_l2/K_l0 = {k2b/k0b:.2f}")
print("l=0 scaling, window exp8, R = 30 r_min:")
ks=[]
rms=[2*np.pi*m for m in (1,2,4)]
for rm in rms:
    ks.append(K(0,rm,'exp8',30*rm)); print(f"  r_min={rm/2/np.pi:.0f} lambda: K_l0 = {ks[-1]:.4e}")
print("  local slopes:", [round(np.log(ks[i+1]/ks[i])/np.log(2),3) for i in range(2)])

print("\n=== D. analysis' l=0-proxy near-zone numbers rescaled by the l=2/l=0 near-field ratio ===")
# inputs printed by taskB_outgoing.py / taskB_outgoing_l2.py (re-run 2026-10-12) and section C above
ratio_steady_l0 = 6.884e-02     # (proxy x C_coh)/B&O-applied at r_min = lambda/2pi, l=0
g_bin = 0.03968
merger_l0 = 1.909e-09; bo_tm = r8*tm
for lab,R2 in [("own exp8 window",126.48),("own poly window",111.08),("taskB_outgoing_l2",254.49)]:
    print(f"  {lab}: K_l2/K_l0 = {R2:.1f} -> steady ratio to B&O-applied (no g) = {ratio_steady_l0*R2:.2f}, "
          f"with binary g = {ratio_steady_l0*R2*g_bin:.3f}; merger pairs beyond lambda/2pi = {merger_l0*R2:.2e} vs B&O rate x t_m = {bo_tm:.2e} (ratio {merger_l0*R2/bo_tm:.2f})")
