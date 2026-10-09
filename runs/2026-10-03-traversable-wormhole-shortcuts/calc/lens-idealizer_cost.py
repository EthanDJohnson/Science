"""Idealizer: universal mass scale of a throat, tidal size limits, and the negative-energy fraction of a
Casimir-balanced long throat (MMP-type), with the payload cap m <= |E_neg|.

Units: SI unless stated; geometric (G = c = 1, metres) for wormhole_tools internals; natural (hbar = c = 1)
for the MMP energy function. Constants from CODATA via literal values below.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from wormhole_tools import ProperThroat, MorrisThorne, ThinShell, geom_to_kg
from gr_tensors import Spacetime

G = 6.67430e-11; c = 2.99792458e8; hbar = 1.054571817e-34; Msun = 1.98892e30; ly = 9.4607e15; g0 = 9.80665
lP = math.sqrt(hbar * G / c**3)

print("=== 1. Universal mass scale of a throat of areal radius r: r c^2/G (SI) ===")
for b0 in [1e-12, 1e-6, 1.0, 1e3, 1.5e7]:
    mt = MorrisThorne(f"{b0}**2/r", "0", r0=b0)
    v = mt.vkd()
    sh = ThinShell("1", None, a=b0)          # flat-space (M = 0) thin-shell wormhole
    print(f" r = {b0:9.3g} m: r c^2/G = {b0 * c**2 / G:9.3e} kg | Ellis int rho dV (both sheets) = {v['int_rho_dV_kg']:+.3e} kg"
          f" | flat thin-shell mass 4 pi a^2 sigma = {sh.mass_kg():+.3e} kg (= {sh.mass() / b0:+.3f} a)")
et = ProperThroat("sqrt(l**2 + b0**2)", "0", params={"b0": 1.0})
an = et.anec()
print(f" Ellis b0 = 1 m ANEC along radial null geodesic: {an['anec_geom_per_m']:+.6f} /m (closed form -1/8 = -0.125); agree by parts: {an['agree']}")

print("\n=== 2. Tidal size limit for a traveller crossing an Ellis throat at local speed v ===")
l, t, th, ph, b0s = sp.symbols("l t theta phi b0", positive=True)
r = sp.sqrt(l**2 + b0s**2)
st = Spacetime(sp.diag(-1, 1, r**2, r**2 * sp.sin(th)**2), [t, l, th, ph])
Rm = st.riemann()
R_thl = sp.simplify(Rm[2][1][2][1])       # R^theta_{l theta l} (orthonormal, g_ll = 1)
R_tht = sp.simplify(Rm[2][0][2][0])       # R^theta_{t theta t}
print(f" gr_tensors: R^theta_l theta l = {R_thl}; at l=0: {sp.simplify(R_thl.subs(l, 0))}; R^theta_t theta t = {R_tht}")
print(" boosted radial observer: transverse tidal |da| = gamma^2 v^2 |R_thl(0)| xi = gamma^2 v^2 xi / b0^2 (geometric)")
print(" => b0 >= gamma (v) sqrt(xi / a_max)   [v in m/s, xi body length m, a_max m/s^2]")
for name, xi, amax in [("MM criterion: 0.5 m, 20 g", 0.5, 20 * g0), ("MT-like: 2 m, 1 g", 2.0, g0)]:
    for v in [1e4, 1e6, 0.1 * c, 0.9 * c, 0.999 * c]:
        gam = 1 / math.sqrt(1 - (v / c)**2)
        bmin = gam * v * math.sqrt(xi / amax)
        print(f"  {name}: v = {v / c:.3g} c -> b0 >= {bmin:9.3e} m, exotic |int rho dV| = b0 c^2/G >= {bmin * c**2 / G:9.3e} kg"
              f" = {bmin * c**2 / G / Msun:.3g} Msun; crossing time ~ pi b0/v = {math.pi * bmin / v:.3g} s")
print(" ultra-relativistic limit (gamma v -> c, the MM case): b0 >= c sqrt(xi/a_max):",
      f"{c * math.sqrt(0.5 / (20 * g0)):.3e} m (MM), {c * math.sqrt(2 / g0):.3e} m (MT-like)")

print("\n=== 3. Casimir-balanced long throat (MMP eqs 5.30-5.31 form, N flavours assumed multiplicative), hbar=c=1 ===")
re, Gs, q, ell, N = sp.symbols("r_e G q ell N", positive=True)
E = re**3 / (Gs * ell**2) - N * q / (8 * ell)
ell_star = sp.solve(sp.diff(E, ell), ell)[0]
Emin = sp.simplify(E.subs(ell, ell_star))
M = re / Gs
ratio = sp.simplify(-Emin / M - (re / ell_star)**2)
print(f" ell* = {ell_star}; E_min = {Emin}; |E_min|/M - (r_e/ell*)^2 = {ratio}  (0 => |E_neg| = M (r_e/ell)^2)")
gam_MM = 2e12
Me = 1.5e7 * c**2 / G
print(f" MM check: gamma = ell/r_e ~ {gam_MM:.0e} -> (r_e/ell)^2 = {gam_MM**-2:.2e} (Q-05 quotes |E_bin|/M_e ~ 2.5e-25);"
      f" M_e = {Me:.3e} kg -> |E_neg| ~ {Me / gam_MM**2:.2e} kg (Q-02 quotes ~5e9 kg)")

print("\n=== 4. Payload cap m <= |E_neg| = M (r_e/ell)^2  =>  ell <= r_e sqrt(M/m); no-shortcut needs pi ell > d ===")
for name, m in [("1 kg", 1.0), ("human 70 kg", 70.0), ("MM ship 1e3 kg", 1e3)]:
    for rr in [1.5e7, 1.36e8]:
        Mm = rr * c**2 / G
        ellmax = rr * math.sqrt(Mm / m)
        print(f"  {name}, r_e = {rr:.3g} m (M = {Mm:.2e} kg): ell_max = {ellmax:.2e} m = {ellmax / ly:.2e} ly;"
              f" max consistent mouth separation d < pi ell_max = {math.pi * ellmax / ly:.2e} ly;"
              f" external transit pi ell_max/c = {math.pi * ellmax / c / 3.156e7:.2e} yr; proper ~ pi r_e/c = {math.pi * rr / c:.3f} s")

print("\n=== 5. Species requirement in the same model (rough; charge normalisation kappa = r_e^2/(G q^2) = pi/g^2, g^2 N < 1) ===")
# m <= |E_neg| with ell* = 16 r_e^3/(G N q), q = r_e/sqrt(kappa G):  m <= N^2/(256 kappa r_e)  (hbar=c=1)
for m in [1e3]:
    mr = m * c * 1.5e7 / hbar           # m r_e in hbar = c = 1 (dimensionless)
    # kappa = pi/g^2 >= pi N  (g^2 N < 1): N^2 >= 256 pi N m r_e  => N >= 256 pi m r_e
    Nreq = 256 * math.pi * mr
    print(f"  m = {m:g} kg, r_e = 1.5e7 m: m r_e/(hbar/c) = {mr:.2e}; N >= 256 pi m r_e = {Nreq:.1e}"
          f" (MM quote N_f > 1e52 [Q-03]; UV-cutoff bound N < 1e32 [K-22])")

print("\n=== 6. Signal (one quantum) through a classical exotic throat: r >= wavelength ===")
for lam in [1e-12, 1e-6, 0.3]:
    print(f"  wavelength {lam:g} m -> throat >= {lam:g} m -> |negative mass| ~ r c^2/G = {lam * c**2 / G:.2e} kg; r/l_P = {lam / lP:.2e}")
