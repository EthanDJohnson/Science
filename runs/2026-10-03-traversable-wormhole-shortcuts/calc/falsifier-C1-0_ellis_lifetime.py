"""Falsifier C1-0 (physics): can a labelled-phantom Ellis shortcut stay open long enough
for a fast 1 kg payload, despite its unstable radial mode?

Units: SI unless marked. Geometric (G = c = 1) lengths in metres.

Inputs (sourced):
- Gonzalez, Guzman & Sarbach 2009 (arXiv:0806.0608), massless ghost-scalar (Ellis) wormhole:
  exactly one unstable mode exp(beta t); for the symmetric case gamma1 = 0 the ground-state
  energy obeys -3 <= E0 = -beta^2 <= -11/8 (units of the throat areal radius b0, c = 1),
  so the e-folding time tau_e lies in [1/sqrt(3), 1/sqrt(11/8)] * b0/c.
  We use the WORST case tau_e = b0/(sqrt(3) c) (fastest growth).
- Ellis throat r(l) = sqrt(l^2 + b0^2), Phi = 0; transit time from wormhole_tools.ProperThroat.

Model assumptions (mine, stated):
- The seed amplitude of the unstable mode is eps ~ (energy put in) / (throat mass scale b0 c^2/G).
  A payload of mass m gives eps_pay = G m / (c^2 b0). The throat goes nonlinear after
  N_avail = ln(1/eps) e-folds (O(1) threshold).
- Ambient seeds: CMB energy in a b0^3 volume, and a single vacuum quantum hbar c / b0.
- The payload must cross the region |l| <= l_obs (observers at areal radius R_obs) before
  the mode is nonlinear: N_needed = T_cross / tau_e.
"""
import math
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import wormhole_tools as wt  # noqa: E402

G = 6.67430e-11      # m^3 kg^-1 s^-2
C = 2.99792458e8     # m/s
HBAR = 1.054571817e-34
LY = 9.4607e15       # m
AU = 1.495978707e11  # m
U_CMB = 4.17e-14     # J/m^3, CMB energy density at T = 2.725 K (a T^4)

tau_e_fast = 1 / math.sqrt(3.0)     # in b0/c, worst case (fastest growth)
tau_e_slow = 1 / math.sqrt(11 / 8)  # in b0/c, slowest allowed growth
print(f"Gonzalez et al. bound: tau_e in [{tau_e_fast:.4f}, {tau_e_slow:.4f}] b0/c; worst case used = {tau_e_fast:.4f} b0/c")
print()

for b0 in (1.0, 505.0, 1000.0):
    th = wt.ProperThroat("sqrt(l**2 + b0**2)", "0", params={"b0": b0})
    for R_over_b0 in (3.0, 10.0):
        R_obs = R_over_b0 * b0
        l_obs = math.sqrt(R_obs**2 - b0**2)
        for v in (1.0, 0.1, 10e3 / C):
            tr = th.transit(-l_obs, l_obs, v=v)
            T = tr["t_coord_s"]
            tau_e_s = tau_e_fast * b0 / C
            N_need = T / tau_e_s
            print(f"b0 = {b0:7.1f} m, R_obs = {R_over_b0:4.1f} b0, v = {v:.3e} c: "
                  f"T_cross = {T:.4e} s, tau_e = {tau_e_s:.4e} s, e-folds needed = {N_need:.4e}")
    # shortcut ratios against exterior light time at d = 1 AU, 1 ly (observers at 10 b0, v = c)
    tr = th.transit(-math.sqrt(99) * b0, math.sqrt(99) * b0, v=1.0)
    for name, d in (("1 AU", AU), ("1 ly", LY)):
        T_ext = (d - 2 * 10 * b0) / C
        print(f"   shortcut: b0 = {b0} m, d = {name}: T_thru = {tr['t_coord_s']:.4e} s, T_ext = {T_ext:.4e} s, ratio = {tr['t_coord_s']/T_ext:.3e}")
    # seeds
    M_scale = b0 * C**2 / G
    for m in (1.0, 70.0):
        eps = m / M_scale
        print(f"   payload m = {m:5.1f} kg: throat mass scale b0c^2/G = {M_scale:.3e} kg, eps = {eps:.3e}, e-folds available = {math.log(1/eps):.2f}")
    eps_cmb = U_CMB * b0**3 / (M_scale * C**2)
    eps_q = (HBAR * C / b0) / (M_scale * C**2)
    print(f"   ambient seeds: CMB in b0^3: eps = {eps_cmb:.3e} (N = {math.log(1/eps_cmb):.1f}); one vacuum quantum hbar c/b0: eps = {eps_q:.3e} (N = {math.log(1/eps_q):.1f})")
    print(f"   open time if seeded only by one vacuum quantum: {math.log(1/eps_q)*tau_e_fast*b0/C:.3e} s = {math.log(1/eps_q)*tau_e_fast:.1f} b0/c")
    print()

# robustness: how much larger could the payload's coupling to the unstable mode be
# and still leave the 1 kg, v = c, R_obs = 10 b0 crossing intact at b0 = 1 m?
b0 = 1.0
th = wt.ProperThroat("sqrt(l**2 + b0**2)", "0", params={"b0": b0})
T = th.transit(-math.sqrt(99) * b0, math.sqrt(99) * b0, v=1.0)["t_coord_s"]
N_need = T / (tau_e_fast * b0 / C)
eps = 1.0 / (b0 * C**2 / G)
margin = math.log(1 / eps) - N_need
print(f"Robustness at b0 = 1 m, 1 kg, v = c, R_obs = 10 b0: N_avail - N_needed = {margin:.2f} e-folds,"
      f" i.e. the seed could be {math.exp(margin):.2e} times larger and the payload still crosses first")
