"""lens-mechanist: the acceleration phase of a positive-energy warp shell (brief premise 5).

Units: SI unless marked "geo" (G = c = 1, lengths in metres).
Parts
 A  Momentum density a localized interior shift needs (linearized momentum constraint),
    for the Fuchs et al. 2024 shift profile; total, positive and negative parts.
 B  Linear-theory cap on the interior shift that counter-streaming positive matter can make.
 C  Linear-theory 'induction' drag of interior inertial frames by a pushed shell.
 D  Momentum and energy that must be supplied or ejected to start and stop (shell vs payload).
 E  Interior clock slowing on the Alpha Centauri coast, and payload drift if the shift is
    ramped by internal currents alone.
"""
import sys
import numpy as np
import sympy as sp

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import warp_shell as ws  # toolkit rebuild of Fuchs et al. 2024

G = 6.67430e-11; c = 2.99792458e8
MJ = 1.898e27; Msun = 1.989e30
yr = 3.15576e7; ly = 9.4607e15

# ---------------------------------------------------------------- A: symbolic check
x, y, z, b0 = sp.symbols("x y z beta0", real=True)
r = sp.sqrt(x**2 + y**2 + z**2)
f = sp.Function("f")
beta = [b0 * f(r), 0, 0]                       # beta_i = beta0 f(r) x-hat (flat slice, linear)
X = [x, y, z]
K = [[-sp.Rational(1, 2) * (sp.diff(beta[j], X[i]) + sp.diff(beta[i], X[j])) for j in range(3)] for i in range(3)]
trK = sum(K[i][i] for i in range(3))
# linearized momentum constraint (geo): 8 pi j_i = d_j (K_ij - delta_ij K)
jx_geo = sum(sp.diff(K[0][jj] - (trK if jj == 0 else 0), X[jj]) for jj in range(3)) / (8 * sp.pi)
# closed form claimed: j_x = -(beta0/16pi)[f'' sin^2(th) + f' (1+cos^2(th))/r], th from x axis
rr = sp.symbols("rr", positive=True)
fp = sp.Derivative(f(rr), rr); fpp = sp.Derivative(f(rr), rr, 2)
cos2 = x**2 / r**2
closed = -(b0 / (16 * sp.pi)) * (fpp * (1 - cos2) + fp * (1 + cos2) / rr)
pt = {x: sp.Rational(3, 10), y: sp.Rational(-7, 10), z: sp.Rational(11, 10)}
# test with a concrete f to avoid unevaluated-derivative bookkeeping
ftest = sp.Lambda(rr, sp.exp(-rr**2) * rr**3)
lhs = jx_geo.subs(f, ftest).doit().subs(pt)
rhs = closed.subs(f, ftest).doit().subs(rr, r).subs(pt)
print("A0 symbolic check of closed-form j_x (should be ~0):", float(sp.N(lhs - rhs).subs(b0, 1)))

# ---------------------------------------------------------------- A: Fuchs profile
R1, R2 = 10.0, 20.0
M_ADM = 4.51050343896829e27     # kg, from warp_shell.py at the published parameters (Finding 2)
rg = np.linspace(R1 + 1e-6, R2 - 1e-6, 20001)
S = ws.shift_profile(rg, R1, R2)
fprime = np.gradient(S, rg); fpp = np.gradient(fprime, rg)
mu = np.linspace(-1, 1, 801)                  # cos(theta from x axis)
RR, MU = np.meshgrid(rg, mu, indexing="ij")
for b in (0.02, 0.04):
    jx = -(b / (16 * np.pi)) * (fpp[:, None] * (1 - MU**2) + fprime[:, None] * (1 + MU**2) / RR)  # geo, 1/m^2
    w = 2 * np.pi * RR**2                       # dV = 2 pi r^2 dr dmu
    integrand = jx * w
    Ptot = np.trapezoid(np.trapezoid(integrand, mu, axis=1), rg)
    Ppos = np.trapezoid(np.trapezoid(np.clip(integrand, 0, None), mu, axis=1), rg)
    Pneg = np.trapezoid(np.trapezoid(np.clip(integrand, None, 0), mu, axis=1), rg)
    conv = c**3 / G                             # geo momentum [m] -> SI kg m/s
    print(f"A  beta_int={b}: P_total={Ptot*conv:.3e} kg m/s (geo {Ptot:.3e} m); "
          f"P_+={Ppos*conv:.3e}, P_-={Pneg*conv:.3e} kg m/s; P_+/(M_ADM c)={Ppos*conv/(M_ADM*c):.3e}")
    # thin two-layer equivalent: beta(0) = (4G P/c^3)(1/R1 - 1/R2)
    P2 = b * c**3 / (4 * G * (1 / R1 - 1 / R2))
    print(f"   two-layer harmonic-gauge equivalent P = {P2:.3e} kg m/s; P/(M_ADM c) = {P2/(M_ADM*c):.3e}; "
          f"counter-stream speed if each layer holds M/2: u = {2*P2/M_ADM/c:.3f} c")

# ---------------------------------------------------------------- B: linear cap
C1 = 2 * G * M_ADM / (c**2 * R1); C2 = 2 * G * M_ADM / (c**2 * R2)
print(f"B  Fuchs shell: C1=2GM/(c^2 R1)={C1:.3f}, C2={C2:.3f}; linear cap beta_cc,max = C1 - C2 = {C1-C2:.3f} (units of c)")
for ratio in (1.1, 2.0, 10.0):
    # largest C1 allowed if outer compactness kept below Buchdahl 8/9 at R2
    C2max = 8 / 9; C1v = C2max * ratio
    print(f"   R2/R1={ratio}: with C2=8/9, C1={C1v:.2f}, cap C1-C2={C1v - C2max:.2f} (linear theory far outside validity if >~0.1)")

# ---------------------------------------------------------------- C: induction drag
for R in (R1, R2):
    kappa = 4 * G * M_ADM / (c**2 * R)
    print(f"C  linear drag fraction kappa=4GM/(c^2 R) at R={R:.0f} m: {kappa:.2f} (>~0.1 means linear theory fails)")
for Mtest_MJ, Rtest in ((1e-6, 10.0), (1e-3, 10.0), (1.0, 100.0)):
    Mt = Mtest_MJ * MJ
    print(f"   M={Mtest_MJ} M_J, R={Rtest} m: kappa={4*G*Mt/(c**2*Rtest):.3e}")

# ---------------------------------------------------------------- D: start and stop budgets
m_pay = 1e5
print("D  ideal photon (or beamed-GW) rocket, start then stop, final mass fixed")
for v in (0.02, 0.04, 0.1):
    gam = 1 / np.sqrt(1 - v**2)
    MR = (1 + v) / (1 - v)                     # start+stop mass ratio, photon exhaust
    for name, m in (("shell+payload", M_ADM + m_pay), ("payload alone", m_pay)):
        p = gam * m * v * c
        Eej = (MR - 1) * m * c**2
        print(f"   v={v}c {name:14s}: momentum to supply {p:.3e} kg m/s; mass ratio {MR:.4f}; "
              f"exhaust energy {Eej:.3e} J = {Eej/c**2:.3e} kg = {Eej/c**2/MJ:.3e} M_J; "
              f"= {Eej/5.922e20:.2e} world-years (592.2 EJ/yr)")
    print(f"   ratio shell/payload exhaust energy = {(M_ADM+m_pay)/m_pay:.3e}")
    KE = (gam - 1) * M_ADM * c**2
    print(f"   shell kinetic energy (gamma-1)Mc^2 at {v}c = {KE:.3e} J")

# ---------------------------------------------------------------- E: clocks and drift
N0 = 0.7611845283738221           # centre lapse from warp_shell.py, published parameters
D = 4.37 * ly
for v in (0.02, 0.04):
    tE = D / (v * c) / yr
    tau = tE * np.sqrt(1 - v**2) * N0
    print(f"E  coast {v}c to alpha Cen: exterior time {tE:.1f} yr; passenger proper time with lapse {N0:.3f}: {tau:.1f} yr "
          f"(without shell {tE*np.sqrt(1-v**2):.1f} yr)")
u_rel = 0.02626577282673753      # Eulerian speed rel. shell at centre (warp_shell.py)
print(f"E  payload kicked to {u_rel:.4f} c relative to shell crosses R1=10 m in {R1/(u_rel*c)*1e6:.2f} microseconds")
print(f"E  shell recoil if a 1e5 kg payload gains {u_rel:.4f} c: {m_pay*u_rel*c/M_ADM:.3e} m/s")

# ---------------------------------------------------------------- F: pointwise |T^0x| vs energy density, ramp stress
sh = ws.build_shell(4.49e27, 10.0, 20.0, beta_warp=0.0)
rr_, rho_ = np.asarray(sh.r), np.asarray(sh.rho_grid)
S_ = ws.shift_profile(rr_, 10.0, 20.0)
f1 = np.gradient(S_, rr_); f2 = np.gradient(f1, rr_)
with np.errstate(divide="ignore", invalid="ignore"):
    jmax_per_beta = np.maximum(np.abs(f2 + f1 / rr_), np.abs(2 * f1 / rr_)) / (16 * np.pi)   # geo, per unit beta0
    eps_geo = G * rho_ / c**2                                                            # geo energy density
    ratio = np.where(eps_geo > 0, jmax_per_beta / eps_geo, np.inf)
mask = (jmax_per_beta > 0)
worst = np.nanmax(ratio[mask & (rho_ > 0)]) if np.any(mask & (rho_ > 0)) else np.nan
unsupported = np.any(mask & (rho_ <= 0))
i_w = np.nanargmax(np.where(mask & (rho_ > 0), ratio, -1))
print(f"F  linear |T^0x|_max/eps per unit beta_int: worst {worst:.3e} at r={rr_[i_w]:.3f} m "
      f"(rho there {rho_[i_w]:.3e} kg/m^3); any momentum where rho<=0: {unsupported}")
print(f"   => beta_int at which |T^0x| = eps somewhere (crude linear DEC-type cap for this density profile): {1/worst:.3f} c")
i_bulk = np.argmin(np.abs(rr_ - 15.0))
print(f"   at r=15 m: ratio per unit beta {ratio[i_bulk]:.3e}; at beta=0.02 -> {0.02*ratio[i_bulk]:.3e}")
# ramp: S_ramp ~ beta0 |f'| /(8 pi c tau) (geo); require S_ramp <= 0.1 eps at the bulk point
for ctau in (10.0, 1e3, 3e8):
    Sr = 0.04 * np.abs(f1[i_bulk]) / (8 * np.pi * ctau)
    print(f"   ramp to beta=0.04 over c*tau={ctau:.0e} m (tau={ctau/c:.2e} s): S_ramp/eps at r=15 m = {Sr/eps_geo[i_bulk]:.3e}")
# pushing the whole shell with a photon beam at 1 g
A = 9.80665; P_push = M_ADM * A * c; Lsun = 3.828e26
print(f"F  photon-pushed shell at 1 g: exhaust power {P_push:.3e} W = {P_push/Lsun:.2e} L_sun; time to 0.04c {0.04*c/A/86400:.1f} days")
print(f"   payload alone at 1 g: {m_pay*A*c:.3e} W")
bad = mask & (rho_ <= 0)
if np.any(bad):
    print(f"F  momentum-without-density points: r in [{rr_[bad].min():.4f}, {rr_[bad].max():.4f}] m, n={bad.sum()}, "
          f"max |T^0x| per unit beta there = {jmax_per_beta[bad].max():.3e} geo (vs peak {jmax_per_beta.max():.3e})")
    print(f"   density support: rho>0 for r in [{rr_[rho_>0].min():.4f}, {rr_[rho_>0].max():.4f}] m; shift gradient support "
          f"[{rr_[mask].min():.4f}, {rr_[mask].max():.4f}] m")

# ---------------------------------------------------------------- G: lab-scale induction drag and GW-rocket cost
for Mlab, Rlab in ((1e3, 1.0), (1e6, 10.0)):
    print(f"G  lab induction drag kappa=4GM/(c^2R): M={Mlab:.0e} kg, R={Rlab} m -> {4*G*Mlab/(c**2*Rlab):.2e}")
for v in (0.04,):
    leg = 1 - np.sqrt((1 - v) / (1 + v)); both = 1 - (1 - v) / (1 + v)
    print(f"G  beamed-GW (or photon) self-propulsion to {v}c: radiated fraction one leg {leg:.4f}, start+stop {both:.4f} of initial mass; "
          f"for M_ADM: {both*M_ADM:.3e} kg = {both*M_ADM*c**2:.3e} J")
print(f"G  superkick 15,000 km/s = {15e6/c:.4f} c")
