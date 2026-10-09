"""Examiner lens: the shortcut test (brief, 'Worked calculations: examiner').

For each one-sided construction: T_thru (earliest arrival through the throat, static-observer /
exterior-synchronised clocks), T_ext (exterior light time), the ratio, and the traveller proper time.
Also: the throat 'time shift' Delta that makes shortcut-ness directional, the MM throat's proper
spatial length vs its time length, and the rocket that would give the same proper-time saving.

Units: SI unless stated; geometric (G = c = 1) lengths in metres where marked.
Inputs are dossier values: MM r_e = 1.5e7 m (Q-01), l ~ 3e3 ly (Q-02), metric MM eqs (2.4),(2.7)
(fetched, arXiv:2008.06618 p.4); Ellis b0 = 1 m (Q-24); thin shell M = 1 Msun, a = 10 km (Q-29).
"""
import math
import sys

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import wormhole_tools as wt  # noqa: E402

c = 299792458.0            # m/s
G = 6.67430e-11            # m^3 kg^-1 s^-2
MSUN = 1.98847e30          # kg
LY = 9.4607304725808e15    # m
YR = 3.15576e7             # s (Julian year)
AU = 1.495978707e11        # m

print("=" * 78)
print("1. Ellis-Bronnikov throat (Phi = 0, r(l) = sqrt(l^2 + b0^2)), b0 = 1 m, as a ONE-SIDED")
print("   wormhole: mouths a distance D apart in nearly flat ambient space (zero ADM mass, so no")
print("   O(M) Shapiro term), time shift Delta = 0 (throat identifies equal exterior-synced times).")
print("   Observers static at areal radius r_obs on the facing sides of the mouths, so the exterior")
print("   observer-to-observer distance is D - 2 r_obs. Approximation: two-sheet Ellis metric used")
print("   near each mouth; valid for D >> r_obs.")
b0 = 1.0
th = wt.ProperThroat("sqrt(l**2 + b0**2)", "0", {"b0": b0})
for r_obs in (10.0, 100.0):
    l_obs = math.sqrt(r_obs**2 - b0**2)
    tr_light = th.transit(-l_obs, l_obs, v=1.0)
    tr_slow = th.transit(-l_obs, l_obs, v=0.1)
    for D in (1e3, AU, LY):
        cmp_ = wt.compare_paths(tr_light["t_coord_s"], ext_distance_m=D - 2 * r_obs)
        print(f"  r_obs = {r_obs:6.0f} m, D = {D:.3e} m: T_thru = {cmp_['t_thru_s']:.4e} s, "
              f"T_ext = {cmp_['t_ext_s']:.4e} s, T_thru/T_ext = {cmp_['ratio']:.3e}, shortcut = {cmp_['shortcut']}")
    print(f"    payload at v = 0.1 c (local static frame): t_coord = {tr_slow['t_coord_s']:.4e} s, "
          f"tau_traveller = {tr_slow['tau_traveller_s']:.4e} s, proper length = {tr_slow['proper_length_m']:.4f} m")

print("=" * 78)
print("2. Schwarzschild thin-shell (Visser) wormhole, M = 1 Msun, a = 10 km, as ONE-SIDED, Delta = 0.")
print("   Observers static at r_obs = 100 km on the facing sides. T in infinity-clock seconds;")
print("   static-observer clocks run slow by sqrt(1 - 2M/r_obs), same factor at both mouths, so the")
print("   ratio is unchanged. Exterior: flat D - 2 r_obs plus weak-field radial Shapiro delay")
print("   2M ln((D - r_obs)/r_obs) from each mouth's positive ADM mass (approximation).")
Mg = wt.mass_to_geom(MSUN)      # m
a = 1.0e4
r_obs = 1.0e5
sh = wt.ThinShell.schwarzschild(M=Mg, a=a)
tr = sh.transit(r_obs, r_obs, v=1.0)
red = math.sqrt(1 - 2 * Mg / r_obs)
print(f"  M (geometric) = {Mg:.2f} m; T_thru (infinity clocks) = {tr['t_coord_s']:.4e} s; "
      f"on observer clocks = {tr['t_coord_s'] * red:.4e} s; proper length = {tr['proper_length_m']:.4e} m")
for D in (1e7, AU, LY):
    shap = 2 * (2 * Mg * math.log((D - r_obs) / r_obs)) / c
    t_ext = (D - 2 * r_obs) / c + shap
    cmp_ = wt.compare_paths(tr["t_coord_s"], t_ext_s=t_ext)
    print(f"  D = {D:.3e} m: T_ext = {t_ext:.4e} s (Shapiro part {shap:.3e} s), ratio = {cmp_['ratio']:.3e}, "
          f"shortcut = {cmp_['shortcut']}")
tr01 = sh.transit(r_obs, r_obs, v=0.1)
print(f"  payload at v = 0.1 c: t_coord = {tr01['t_coord_s']:.4e} s, tau = {tr01['tau_traveller_s']:.4e} s")

print("=" * 78)
print("3. Maldacena-Milekhin 2020 ('humanly traversable'), metric MM (2.4) outside, (2.7) AdS2xS2 inside,")
print("   matched with t = l*tau, rho = l (r - r_e)/r_e^2 (my matching; MM state t-rescaling (2.8)).")
r_e = 1.5e7                 # m (Q-01)
ell = 3e3 * LY              # m (Q-02, 'l ~ 3x10^3 ly')
gam = ell / r_e
print(f"  r_e = {r_e:.3e} m ({r_e / c:.4f} light-s); l = {ell:.3e} m; gamma = l/r_e = {gam:.3e} (MM: ~2e12)")
T_thru = math.pi * ell / c
tau = math.pi * r_e / c
print(f"  T_thru = pi l / c = {T_thru:.4e} s = {T_thru / YR:.4e} yr; tau_traveller ~ pi r_e / c = {tau:.4f} s")
for frac in (1.0, 0.1, 0.01):
    d = frac * ell
    print(f"  d = {frac:5.2f} l = {d / LY:.3e} ly: T_ext = d/c = {d / c / YR:.4e} yr; T_thru/T_ext = {T_thru / (d / c):.4e}; "
          f"tau/T_ext = {tau / (d / c):.3e}")

r_obs = 2 * r_e
print(f"  Proper radial length mouth-to-mouth between static observers at r_obs = 2 r_e = {r_obs:.2e} m,")
print("  and coordinate (asymptotic) light time, for several matching points rho_c (result must not")
print("  depend on rho_c in the overlap 1 << rho_c << gamma):")
for rho_c in (1e3, 1e6, 1e9):
    x_c = rho_c * r_e**2 / ell                     # r_c - r_e
    x_o = r_obs - r_e
    side_len = r_e * math.asinh(rho_c) + (x_o - x_c) + r_e * math.log(x_o / x_c)
    side_t = ell * math.atan(rho_c) + ((x_o - x_c) + 2 * r_e * math.log(x_o / x_c) - r_e**2 / x_o + r_e**2 / x_c)
    print(f"    rho_c = {rho_c:.0e}: L_prop = {2 * side_len:.4e} m = {2 * side_len / c:.3f} light-s; "
          f"T_thru(light) = {2 * side_t / c / YR:.5e} yr")
Lprop_closed = 2 * r_e * (math.log(2 * gam * (r_obs - r_e) / r_e) + (r_obs - r_e) / r_e)
print(f"  closed form 2 r_e [ln(2 gamma (r_obs - r_e)/r_e) + (r_obs - r_e)/r_e] = {Lprop_closed:.4e} m "
      f"= {Lprop_closed / c:.3f} light-s")
print(f"  => spatially the throat is {Lprop_closed / ell:.2e} of l: a spatial 'shortcut' by ~{math.log10(ell / Lprop_closed):.0f}"
      " orders, yet a temporal detour (ratio >= pi at d = l): the delay is lapse (redshift), not length.")

print("  Rocket that gives the same proper-time saving through the EXTERIOR at d = l:")
for m in (1.0, 70.0):
    g_eq = (ell / c) / tau
    KE = (g_eq - 1) * m * c**2
    print(f"    m = {m:5.1f} kg: gamma_eq = {g_eq:.3e}; kinetic energy (gamma-1) m c^2 = {KE:.3e} J")
Ebin = 4.5e26
print(f"    (MM binding energy |E_bin| ~ {Ebin:.1e} J, Q-02; mouth mass ~2.0e34 kg, Q-04)")

print("  Payload rest energy against MM |E_bin| (conserved Killing energy of a payload at rest far away):")
for m in (1.0, 70.0):
    print(f"    m = {m:5.1f} kg: m c^2 = {m * c**2:.3e} J; m c^2/|E_bin| = {m * c**2 / Ebin:.2e}; "
          f"locally boosted energy gamma m c^2 at the throat centre = {gam * m * c**2:.3e} J")

print("=" * 78)
print("4. Time shift Delta (directional shortcut) for a one-sided wormhole with static mouths:")
print("   exterior-synced arrival A->B through throat = T_w + Delta; B->A = T_w - Delta; exterior = D/c.")
print("   shortcut A->B iff Delta < D/c - T_w;  CTC iff |Delta| > T_w + D/c.")
for name, Tw, D in (("Ellis b0=1 m, r_obs=10 m, D=1 ly", 2 * math.sqrt(99.0) / c, LY),
                    ("MM, d = l", T_thru, ell),
                    ("MM, d = 0.01 l", T_thru, 0.01 * ell)):
    thr_short = D / c - Tw
    thr_ctc = Tw + D / c
    print(f"  {name}: T_w = {Tw:.4e} s, D/c = {D / c:.4e} s; shortcut A->B needs Delta < {thr_short:.4e} s "
          f"({thr_short / YR:.4e} yr); CTC needs |Delta| > {thr_ctc:.4e} s ({thr_ctc / YR:.4e} yr); "
          f"shortcut-without-CTC window width 2D/c = {2 * D / c / YR:.4e} yr")

print("=" * 78)
print("5. Two-sided constructions: earliest arrival relative to the boundary channel (structural).")
print("   GJW (Q-15): message must be inserted Delta_t ~ R ln(R/(h l_P)) BEFORE the coupling at t = 0")
print("   and emerges AFTER it; with the coupling off nothing arrives (D-01). So arrival is never")
print("   earlier than, nor without, the coupling. Illustrative R ln(R/(h l_P)) for h = 1:")
for R_over_lP in (1e2, 1e10, 1e60):
    print(f"    R/l_P = {R_over_lP:.0e}: Delta_t/R = ln(R/l_P) = {math.log(R_over_lP):.2f}")
