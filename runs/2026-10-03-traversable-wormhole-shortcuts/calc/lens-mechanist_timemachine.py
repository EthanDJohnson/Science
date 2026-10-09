"""Mechanist lens: time-machine conversion of a one-sided traversable wormhole.

Model (special and general relativity, units stated per line):
- Mouths A and B static in a common exterior, separation D (light time D/c).
- Throat traversal time T_w, measured in each mouth's own proper time (static throat;
  short throat T_w ~ 0, MM/MMP long throat T_w = pi*l/c).
- Mouth B's clock lags the exterior-synchronised clock of A by Delta (accumulated by
  mouth motion or by sitting deeper in a gravitational potential).
- Identification through the throat: A-clock tau  <->  B-clock tau + T_w (A->B direction).
  Then: T_thru(A->B) = T_w + Delta ; T_thru(B->A) = T_w - Delta (exterior-synchronised time).
  Shortcut (B->A) iff T_w - Delta < D/c  ->  Delta > Delta_sc = T_w - D/c.
  Closed null curve (B->A via throat, A->B via exterior) iff Delta > Delta_ctc = T_w + D/c.
- Mouth motion (MTY 1988 kinematics): lag rate 1 - 1/gamma for speed v.
- Gravitational (Frolov-Novikov type): lag rate 1 - sqrt(1 - 2 phi) static, or
  1 - sqrt(1 - 3 phi) on a circular geodesic orbit, phi = GM/(r c^2), Schwarzschild.
- 2D toy of the MMP support: chiral-pair (c=1) CFT on a loop of light-length L with
  twisted identification (t, x) ~ (t + Delta, x + L). Boost to the untwisted frame and
  transform the rest-frame Casimir stress tensor.
"""
import math
import sympy as sp

c = 2.99792458e8          # m/s
G = 6.67430e-11           # SI
yr = 3.15576e7            # s (Julian)
ly = c * yr               # m
pc = 3.0857e16            # m
Msun = 1.98892e30         # kg

print("=== A. Thresholds (exterior-synchronised time) ===")
def thresholds(Tw, D_lt):
    return Tw - D_lt, Tw + D_lt

# MM worked case: external throat time pi*l/c = 9.4e3 yr (Q-06), l ~ 3e3 ly (Q-02)
Tw_MM = 9.4e3  # yr
for D in [1.0, 100.0, 1.0e3, 3.0e3]:
    sc, ctc = thresholds(Tw_MM, D)
    print(f"MM: T_w={Tw_MM:.3g} yr, D/c={D:.3g} yr -> Delta_sc={sc:.4g} yr, Delta_ctc={ctc:.4g} yr")
for D_lt_s, label in [(1.0 / c, "1 m"), (1.496e11 / c, "1 AU"), (yr, "1 ly")]:
    sc, ctc = thresholds(0.0, D_lt_s)
    print(f"short throat (T_w=0), D={label}: already shortcut; Delta_ctc = D/c = {ctc:.4g} s = {ctc/yr:.4g} yr")

print("\n=== B. Mouth motion (MTY kinematics) ===")
def lag_rate_v(beta):
    return 1.0 - math.sqrt(1.0 - beta**2)
for beta in [0.01, 0.1, 0.5, 0.9, 0.99]:
    print(f"beta={beta}: lag rate 1-1/gamma = {lag_rate_v(beta):.4e}; gamma-1 = {1/math.sqrt(1-beta**2)-1:.4e}")
# Short throat, D = 1 ly, Delta_ctc = 1 yr
for beta in [0.1, 0.9]:
    T = 1.0 / lag_rate_v(beta)
    print(f"short throat D=1 ly, beta={beta}: coordinate time of motion T = {T:.4g} yr")
# Short throat, D = 1 m: Delta_ctc = 3.34 ns
for beta in [0.1]:
    T = (1.0 / c) / lag_rate_v(beta)
    print(f"short throat D=1 m, beta={beta}: T = {T:.4g} s")
# MM mouth (Q-04: 2.0e34 kg), D = 1e3 ly
M_MM = 2.0e34
sc, ctc = thresholds(Tw_MM, 1.0e3)
for beta in [0.1, 0.5, 0.9]:
    r = lag_rate_v(beta)
    gm1 = 1 / math.sqrt(1 - beta**2) - 1
    E = gm1 * M_MM * c**2
    print(f"MM mouth, D=1e3 ly, beta={beta}: T_sc = {sc/r:.4g} yr, T_ctc = {ctc/r:.4g} yr; "
          f"kinetic energy per leg (gamma-1)Mc^2 = {E:.3e} J = {E/(Msun*c**2):.3g} Msun c^2")
# Excursion check: out-and-back at beta for T_ctc reaches beta*c*T/2
beta = 0.1
print(f"MM, beta=0.1, out-and-back max excursion = {beta*thresholds(Tw_MM,1e3)[1]/lag_rate_v(beta)/2:.3g} ly (vs l ~ 3e3 ly)")
# circular orbit of radius R at beta: required acceleration
R = 1.0e3 * ly
a = (0.1 * c)**2 / R
print(f"MM mouth on circle R=1e3 ly at 0.1c: a = {a:.3e} m/s^2, force = {a*M_MM:.3e} N; "
      f"mutual gravity of other mouth at R: {G*M_MM/R**2:.3e} m/s^2")

print("\n=== C. Gravitational time dilation (Frolov-Novikov type) ===")
def lag_static(phi):
    return 1.0 - math.sqrt(1.0 - 2.0 * phi)
def lag_orbit(phi):
    return 1.0 - math.sqrt(1.0 - 3.0 * phi)
M_sgr = 4.3e6 * Msun
rg_sgr = G * M_sgr / c**2
print(f"Sgr A*: GM/c^2 = {rg_sgr:.4e} m")
cases = [("Earth surface vs far (static)", G*5.972e24/(6.371e6*c**2), lag_static),
         ("neutron star surface 1.4 Msun, 12 km (static)", G*1.4*Msun/(12e3*c**2), lag_static),
         ("Sgr A* ISCO r=6GM/c^2 (orbit)", 1/6, lag_orbit),
         ("Sgr A* r=0.01 pc (orbit)", rg_sgr/(0.01*pc), lag_orbit),
         ("Sgr A* r=1 pc (orbit)", rg_sgr/(1.0*pc), lag_orbit)]
for name, phi, f in cases:
    print(f"{name}: phi={phi:.4e}, lag rate={f(phi):.4e}")
# Short throat natural wormhole: one mouth at 0.01 pc from Sgr A*, other at D = 8 kpc
D_lt = 8e3 * pc / c / yr
r = lag_orbit(rg_sgr/(0.01*pc))
print(f"short throat, D = 8 kpc (D/c = {D_lt:.4g} yr), mouth at 0.01 pc of Sgr A*: T_ctc = {D_lt/r:.4g} yr")
# Galactic flat rotation curve, 1 kpc vs 8 kpc, v_c = 220 km/s, both on circular orbits
dphi = (220e3/c)**2 * math.log(8.0)
D_lt2 = 7e3 * pc / c / yr
print(f"flat rotation curve 1 vs 8 kpc: delta phi = {dphi:.4e}; D/c = {D_lt2:.4g} yr; T_ctc = {D_lt2/dphi:.4g} yr")
# Earth-surface vs space, D = 1 AU
phiE = G*5.972e24/(6.371e6*c**2)
print(f"short throat D=1 AU, mouth on Earth surface vs free space: T_ctc = {(1.496e11/c)/phiE/yr:.4g} yr")
# MM wormhole, one mouth at Sgr A* ISCO, D = 1e3 ly
print(f"MM, mouth at Sgr A* ISCO, D=1e3 ly: T_sc = {thresholds(Tw_MM,1e3)[0]/lag_orbit(1/6):.4g} yr, "
      f"T_ctc = {thresholds(Tw_MM,1e3)[1]/lag_orbit(1/6):.4g} yr")

print("\n=== D. 2D twisted-loop Casimir (symbolic) ===")
Lsym, Dl, cc = sp.symbols('L Delta c_central', positive=True)
Lp = sp.sqrt(Lsym**2 - Dl**2)                      # proper loop length in untwisted frame
rho_rest = -sp.pi * cc / (6 * Lp**2)               # 2D CFT on circle, periodic, hbar=c_light=1
# rest frame: T_tt = T_xx = rho_rest, T_tx = 0. Null components with k_pm = d_t +- d_x:
Tkk_rest = rho_rest + rho_rest                      # T_tt + T_xx (T_tx = 0)
# Boost: rapidity eta with tanh(eta) = Delta/L; T_kk(+) -> e^{2eta} T_kk_rest (direction that closes)
e2eta = (Lsym + Dl) / (Lsym - Dl)
Tpp = sp.simplify(Tkk_rest / e2eta)
Tmm = sp.simplify(Tkk_rest * e2eta)
print("T_kk (one null direction) =", sp.factor(Tpp))
print("T_kk (other null direction) =", sp.factor(Tmm))
# check: Delta -> 0 gives -pi c/(3 L^2) for both
print("Delta->0 limit:", sp.simplify(Tpp.subs(Dl, 0)), sp.simplify(Tmm.subs(Dl, 0)))
# enhancement of total null support relative to untwisted
kappa = sp.simplify((Tpp + Tmm) / (2 * Tkk_rest.subs(Dl, 0)))
print("kappa = (T_++ + T_--)/(2 T_kk(Delta=0)) =", sp.factor(kappa))
# numeric: MM case at the shortcut threshold, L = T_w + D, Delta = T_w - D
for D in [1.0, 100.0, 1.0e3, 3.0e3]:
    L = Tw_MM + D; Dv = Tw_MM - D
    k_dir = (L / (L - Dv))**2
    k_tot = float(kappa.subs({Lsym: L, Dl: Dv}))
    print(f"MM D={D:g} ly at Delta_sc: closing-direction enhancement (L/(L-Delta))^2 = {k_dir:.4g}; kappa_total = {k_tot:.4g}")

print("\n=== E. Toy feedback: MMP energetics with Casimir coefficient scaled by kappa ===")
# MMP (Q-10): l_eq = 16 r_e^3/(G q) ∝ 1/(Casimir coefficient). Toy: T_w(Delta) = T_w0 / kappa(L = T_w + D, Delta)
def kappa_num(L, Dv):
    return 0.5 * L**2 * (1/(L - Dv)**2 + 1/(L + Dv)**2)
def solve_Tw(Tw0, D, Dv):
    # find roots of f(x) = x*kappa(x+D, Dv) - Tw0 for x > max(0, Dv - D)
    lo = max(1e-12, Dv - D + 1e-9)
    xs = [lo + (Tw0*2 - lo) * i / 20000 for i in range(20001)]
    roots = []
    prev = xs[0] * kappa_num(xs[0] + D, Dv) - Tw0
    for x in xs[1:]:
        f = x * kappa_num(x + D, Dv) - Tw0
        if prev * f < 0:
            roots.append(x)
        prev = f
    return roots
Tw0 = 9.4e3; D = 1.0e3
print(f"T_w0 = {Tw0} yr, D/c = {D} yr")
for Dv in [0, 2000, 4000, 5000, 6000, 7000, 8000, 8400]:
    roots = solve_Tw(Tw0, D, Dv)
    tag = []
    for x in roots:
        state = "shortcut" if Dv > x - D else "long"
        tag.append(f"{x:.4g} ({state})")
    print(f"Delta={Dv:5d} yr: equilibrium T_w roots = {tag if tag else 'none'}")

print("\n=== F. Toy fold location: largest Delta with a 'long' equilibrium ===")
def long_root(Tw0, D, Dv):
    # long branch: x with Dv < x - D (throat slower than exterior B->A)
    lo = Dv + D + 1e-6
    hi = 4 * Tw0
    n = 40000
    prev = None
    best = None
    for i in range(n + 1):
        x = lo + (hi - lo) * i / n
        f = x * kappa_num(x + D, Dv) - Tw0
        if prev is not None and prev * f < 0:
            best = x
        prev = f
    return best
for D in [100.0, 1000.0, 3000.0]:
    last = None
    for k in range(0, 9400, 10):
        r = long_root(Tw0, D, float(k))
        if r is None:
            break
        last = (k, r)
    k, r = last
    print(f"D/c={D:g} yr: long branch exists up to Delta ~ {k} yr (T_w there = {r:.4g} yr); "
          f"no-feedback shortcut threshold T_w0 - D = {Tw0-D:g} yr; fold/threshold = {k/(Tw0-D):.3g}")
