"""Crux C7: (1) hbar counting of the rival channels (C3/C4 fusion total, C5 linear channel, stimulated part);
(2) full second-order (contact + t/u + s) background-field two-beam rate vs crossing angle at fixed strain:
small-angle law (support of the bilinear h1 x h1, not of h^(2)), and G-independence at fixed strain.
Units: (1) SI symbols; (2) natural units (hbar = c = 1), omega = 1, rates in units of omega^4."""
import sys, math
import sympy as sp
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import qft_second_order as q2

hbar, G, c, E, w, sig, k, kT, ctot = sp.symbols("hbar G c E omega sigma k kT c_tot", positive=True)
Gn = G / (hbar * c**5)          # G in natural units -> SI: G/(hbar c^5) has units 1/energy^2
N = E / (hbar * w)

def dlog(expr):
    return sp.simplify(sp.diff(sp.log(expr), hbar) * hbar)

# (a) B&O per-packet fusion total (C3/C4 object): P = (4/25) G^2 N^2 w^3 sigma * (1/sigma^... ) -> use rate*T_eff
rate = sp.Rational(3, 25) / sp.pi * Gn**2 * N**2 * (hbar * w)**3 * (hbar * sig)**2 / hbar   # pairs/s
rate = sp.simplify(rate)
print("eq.8 pair rate (SI):", rate, " dln/dln hbar =", dlog(rate))
P_pk = sp.simplify(rate * 4 * sp.pi / (3 * sig))
print("per-packet total P = R*T_eff (SI):", P_pk, " dln/dln hbar =", dlog(P_pk))

# (b) C5 linear channel: P_lin = k (hbar w / E_Pl)^2 N, E_Pl^2 = hbar c^5/G
EPl2 = hbar * c**5 / G
P_lin = sp.simplify(k * (hbar * w)**2 / EPl2 * N)
print("C5 P_lin (SI):", P_lin, " dln/dln hbar =", dlog(P_lin))
ratio = sp.simplify(P_pk / P_lin)
print("P_BO/P_lin:", ratio, " dln/dln hbar =", dlog(ratio))

# (c) stimulated part, Rayleigh-Jeans occupation f = kT/(hbar w): extra pair number 2 f P
f = kT / (hbar * w)
P_stim = sp.simplify(2 * f * P_pk)
print("stimulated pair number (RJ):", P_stim, " dln/dln hbar =", dlog(P_stim))
print("stimulated power 2*P_stim*hbar*w per packet:", sp.simplify(2 * P_stim * hbar * w), " dln/dln hbar =",
      dlog(2 * P_stim * hbar * w))

# (2) full background-field two-beam rate, R/L, small-angle law at fixed strain h
h = 1e-3
print("\nfull second-order two-beam rate, R/L, omega=1, h=1e-3 (natural units)")
prev = None
for th in [1e-1, 1e-2, 1e-3]:
    r = q2.beams_pair_rate(1.0, h, 1.0, h, th, "R", "L")["pair_rate"]
    closed = h**4 * (1 - math.cos(th))**2 / (1280 * math.pi)
    line = f"theta={th:.0e}: rate={r:.6e}  closed-form(plus/plus) w^4h^4(1-cos)^2/(1280pi)={closed:.6e}"
    if prev is not None:
        line += f"  slope dln/dln theta={math.log(r/prev[1])/math.log(th/prev[0]):.4f}"
    print(line)
    prev = (th, r)
for Gv in [1.0, 1e-3]:
    r = q2.beams_pair_rate(1.0, h, 1.0, h, 0.5, "R", "L", G=Gv)["pair_rate"]
    print(f"G={Gv:g}: R/L rate at theta=0.5 = {r:.12e}")

# (3) GW150914 value of the hbar-free C5 ratio P_BO/P_lin * k = (4/25) G E sigma / c^5 (SI), B&O inputs [D-27]
Gs, cs, Msun = 6.67430e-11, 2.99792458e8, 1.98847e30   # CODATA 2018 G; exact c; IAU nominal solar mass
E_rel, sigma_w = 2 * Msun * cs**2, 200.0                # J, rad/s
print(f"\nGW150914: k * P_BO/P_lin = (4/25) G E sigma/c^5 = {0.16 * Gs * E_rel * sigma_w / cs**5:.3e} (dimensionless)")
print("R/L full rate / plus-plus closed form at theta=1e-3:", 4.973591e-28 / 6.216989e-29)
