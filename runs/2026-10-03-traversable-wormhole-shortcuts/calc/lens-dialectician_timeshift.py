"""Dialectician lens: what happens to a LONG (non-shortcut) wormhole when its mouths
acquire a relative clock offset Delta (Morris-Thorne-Yurtsever mouth motion or
gravitational time dilation)?

Part A  kinematics (exact, c = 1 bookkeeping, then years / light-years):
  signal B -> A through throat, exterior-synchronised clocks, mouth B clock lagging by Delta:
     T_eff(B->A) = T_thru - Delta ;  T_eff(A->B) = T_thru + Delta
  shortcut (B->A) iff T_thru - Delta < d          -> Delta_s   = T_thru - d
  closed causal loop iff (T_thru - Delta) + d < 0 -> Delta_CTC = T_thru + d
  In between, the B->A throat null geodesic is achronal (argued in the analysis).
  Input anchors: Maldacena-Milekhin RS II worked example, ell ~ 3e3 ly, T_thru = pi*ell/c (dossier Q-02, Q-06).

Part B  2D CFT Casimir on a twisted circle (t,x) ~ (t+Delta, x+L), |Delta| < L
  (toy for the lowest-Landau-level fermions of MMP along a closed field-line loop):
     T_{--}, T_{++} = -(pi c/12) / (L -/+ Delta)^2 ; energy density T_tt = sum.
  Verified here by an explicit boost from the frame in which the identification is
  purely spatial (L' = sqrt(L^2 - Delta^2)).

Part C  toy MMP energetics with the twist (Q-10 form, hbar = c = 1):
     E(l) = r_e^3/(G l^2) - (q/8) * (l/2) * [1/(l+Delta)^2 + 1/(l-Delta)^2]
  reduces to MMP's E = r_e^3/(G l^2) - q/(8 l) at Delta = 0 (min l0 = 16 r_e^3/(G q),
  E_min = -G q^2/(256 r_e^3)). Dimensionless x = l/l0, delta = Delta/l0:
     e(x) = 1/(2x^2) - (x/2)[1/(x+delta)^2 + 1/(x-delta)^2]
  Find delta_c above which the metastable minimum disappears.
  TOY ASSUMPTIONS: loop length ~ throat length (d << l), adiabatic Delta, 2D CFT
  Casimir form carried over, no change of r_e, no gravitational back-reaction beyond Q-10.
"""
import math
import numpy as np

YR = 365.25 * 86400.0          # s
LY = 9.4607e15                 # m
C = 2.99792458e8               # m/s

print("=== Part A: thresholds for MM-type long wormhole (SI / years) ===")
ell_ly = 3.0e3                 # MM worked example, Q-02
T_thru_yr = math.pi * ell_ly   # external crossing pi*ell/c in years (ell in ly)
print(f"ell = {ell_ly:.3g} ly ; T_thru = pi*ell/c = {T_thru_yr:.4g} yr  (Q-06 quotes 9.4e3 yr)")
for d_ly in (1.0e2, 1.0e3, 3.0e3):
    Ds = T_thru_yr - d_ly
    Dc = T_thru_yr + d_ly
    print(f"\n d = {d_ly:.3g} ly: T_thru/T_ext = {T_thru_yr/d_ly:.3g}; "
          f"shortcut onset Delta_s = {Ds:.4g} yr; CTC onset Delta_CTC = {Dc:.4g} yr; "
          f"shortcut window width = 2d = {2*d_ly:.3g} yr")
    for eps, label in ((1e-6, "Galactic potential difference ~1e-6"),
                       (5e-5, "mouth orbiting at 0.01c (v^2/2c^2)"),
                       (5e-3, "mouth orbiting at 0.1c"),
                       (0.1, "mouth parked at ~5 r_s of a massive BH (0.1 redshift)")):
        print(f"   eps = {eps:.1e} ({label}): time to shortcut = {Ds/eps:.3g} yr, "
              f"to CTC = {Dc/eps:.3g} yr")

print("\n=== Part B: twisted-circle Casimir, closed form vs explicit boost (c_CFT = 1) ===")
def closed_form(L, D, cc=1.0):
    Tmm = -math.pi * cc / 12.0 / (L - D) ** 2
    Tpp = -math.pi * cc / 12.0 / (L + D) ** 2
    return Tpp, Tmm

def by_boost(L, D, cc=1.0):
    # frame where identification vector (D, L) is purely spatial: boost with v = D/L
    Lp = math.sqrt(L * L - D * D)
    rho = -math.pi * cc / (6.0 * Lp ** 2)      # T_t't' = T_x'x' = rho, T_t'x' = 0
    Tp = np.array([[rho, 0.0], [0.0, rho]])     # components (t', x')
    v = D / L
    g = 1.0 / math.sqrt(1 - v * v)
    # coordinates: t' = g (t - v x), x' = g (x - v t); T_ab = Lambda^c_a Lambda^d_b T'_cd
    Lam = np.array([[g, -g * v], [-g * v, g]])  # d(t',x')/d(t,x)
    T = Lam.T @ Tp @ Lam
    Ttt, Ttx, Txx = T[0, 0], T[0, 1], T[1, 1]
    # null components with x^+- = t +- x : T_{++} = (Ttt + 2Ttx + Txx)/4 etc.
    Tpp = (Ttt + 2 * Ttx + Txx) / 4.0
    Tmm = (Ttt - 2 * Ttx + Txx) / 4.0
    return Tpp, Tmm, Ttt

for (L, D) in ((1.0, 0.0), (1.0, 0.3), (1.0, 0.9), (1.0, 0.99)):
    cf = closed_form(L, D)
    bb = by_boost(L, D)
    print(f" L={L}, Delta={D}: closed T++={cf[0]:.6g}, T--={cf[1]:.6g} | boost T++/T--: "
          f"{bb[0]:.6g}, {bb[1]:.6g}  (ordering depends on boost sign; set equal) ; T_tt={bb[2]:.6g}")
print(" Ratio of the enhanced chirality at the shortcut onset to its Delta=0 value: (L/(L-Delta_s))^2, L = T_thru + d, L-Delta_s = 2d")
for ratio_name, Tth, d in (("MM d = ell", math.pi * 3e3, 3e3), ("MM d = ell/3", math.pi * 3e3, 1e3),
                           ("MM d = ell/30", math.pi * 3e3, 1e2)):
    L = Tth + d
    print(f"   {ratio_name}: ((T_thru+d)/(2d))^2 = {(L/(2*d))**2:.4g}")

print("\n=== Part C: toy MMP energetics with twist ===")
def e(x, dl):
    return 1.0 / (2 * x * x) - (x / 2.0) * (1.0 / (x + dl) ** 2 + 1.0 / (x - dl) ** 2)

# check Delta = 0
xs = np.linspace(0.2, 5, 200001)
ev = e(xs, 0.0)
i = np.argmin(ev)
print(f" delta=0: min at x = {xs[i]:.5f}, e = {ev[i]:.6f} (expect 1, -0.5 i.e. E_min = -G q^2/(256 r_e^3))")
# consistency: |E_bin|/M_e = (r_e/l0)^2 ; MM gamma = ell/r_e ~ 2e12 (Q-02)
gam = 2e12
print(f" |E_min|/M_e = (r_e/l0)^2 -> for gamma = 2e12: {1/gam**2:.3g} (dossier Q-05: 2.5e-25)")

def has_local_min(dl):
    x = np.linspace(dl * (1 + 1e-6) + 1e-9, 5.0, 400001)
    y = e(x, dl)
    dy = np.diff(y)
    # local minimum: derivative changes sign from - to +
    s = np.sign(dy)
    idx = np.where((s[:-1] < 0) & (s[1:] > 0))[0]
    if len(idx) == 0:
        return None
    j = idx[0] + 1
    # barrier: local max between delta and min
    jmax = np.where((s[:-1] > 0) & (s[1:] < 0))[0]
    bar = None
    if len(jmax):
        k = jmax[0] + 1
        bar = (x[k], y[k] - y[j])
    return x[j], y[j], bar

for dl in (0.0, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5):
    r = has_local_min(dl) if dl > 0 else (1.0, -0.5, None)
    print(f" delta = {dl:.2f}: local min -> {r}")

lo, hi = 0.0, 1.0
for _ in range(60):
    mid = 0.5 * (lo + hi)
    if has_local_min(mid) is not None:
        lo = mid
    else:
        hi = mid
print(f" delta_c (metastable minimum disappears) = {lo:.4f} (Delta_c / l0)")
r = has_local_min(lo * 0.999)
print(f" just below delta_c: x_min = {r[0]:.4f}, so (x_min - delta)/x_min = {(r[0]-lo)/r[0]:.4f}")
print(" Beyond delta_c the toy energy decreases monotonically as l -> Delta+ (loop becomes null): "
      "e -> -infinity, i.e. the Casimir sector pulls the loop toward the chronology horizon.")
