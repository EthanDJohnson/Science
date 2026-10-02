"""Engineer lens: build requirements and orders-of-magnitude gaps (SI units throughout).

Parts
 A. Fuchs et al. 2024 shell at published parameters (via toolkit warp_shell.py) and scaled.
 B. Scaling laws: fixed-compactness density/mass vs radius; weak-field gravitomagnetic
    counterflow estimate of the momentum needed for an interior shift beta (OURS, order of magnitude).
 C. Trip energies: photon rocket pushing the shell vs payload alone (rocket_tools.py).
 D. Superluminal options: negative energy required vs demonstrated Casimir negative energy.
 E. Experiments: predicted effect vs demonstrated sensitivity.
Demonstrated values and their sources are listed in the analysis file (engineer.md).
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
from warp_shell import build_shell
from rocket_tools import trip, relativistic_mass_ratio, LY, G0

G = 6.67430e-11; c = 2.99792458e8; hbar = 1.054571817e-34
MJ = 1.898e27; MSUN = 1.989e30
def gap(req, dem): return math.log10(abs(req) / abs(dem))

# ---------------- demonstrated capability (sources in engineer.md) ----------------
DEM = dict(
    ISS_mass_kg=419725.0,            # NASA facts page
    world_energy_J_per_yr=5.922e20,  # D-46
    static_pressure_Pa=1e12,         # D-44 (>1 TPa DAC)
    nanodiamond_yield_Pa=460e9,      # D-44
    PSP_speed_c=6.41e-4,             # D-45
    osmium_density=2.26e4,           # standard handbook value (densest element), unsourced here
)
n0 = 0.16e45                         # nuclear saturation number density, 0.16 fm^-3 (standard, unsourced)
rho_nuc = n0 * 1.67493e-27           # kg/m^3
print("== Demonstrated / reference ==")
for k, v in DEM.items(): print(f"  {k} = {v:.4g}")
print(f"  nuclear saturation density (0.16 fm^-3 x m_n) = {rho_nuc:.3e} kg/m^3; rho c^2 = {rho_nuc*c**2:.3e} Pa")

# ---------------- A. the shell ----------------
print("\n== A. Fuchs 2024 shell, rebuilt (warp_shell.py, default smoothing spans = ours) ==")
cases = [("published R1=10,R2=20 m", 4.49e27, 10.0, 20.0),
         ("scaled x10 (payload R1=100 m, ours)", 4.49e28, 100.0, 200.0)]
shells = {}
for name, M, R1, R2 in cases:
    s = build_shell(M, R1, R2, beta_warp=0.02)
    sm = s.summary(); ec = s.energy_conditions_static()
    shells[name] = (M, R1, R2, sm)
    print(f"-- {name}: M_ADM = {sm['M_ADM_kg']:.4e} kg = {sm['M_ADM_Mjup']:.3f} M_J = {sm['M_ADM_Msun']:.3e} M_sun")
    print(f"   compactness 2GM/(c^2 R2) = {sm['compactness_ADM_at_R2']:.3f}; max 2Gm/(c^2 r) = {sm['max_2Gm_over_c2r']:.3f}")
    print(f"   peak eps = {sm['eps_peak_J_m3']:.3e} J/m^3 (rho = {sm['rho_peak_kg_m3']:.3e} kg/m^3); peak p_r = {sm['p_r_peak_Pa']:.3e} Pa; p_t in [{sm['p_t_min_Pa']:.3e}, {sm['p_t_max_Pa']:.3e}] Pa")
    print(f"   zero-shift shell ECs (exact type I): " + ", ".join(f"{k}={'holds' if ec[k]['holds'] else 'FAILS'}" for k in ['NEC','WEC','SEC','DEC']) + f"; max |p|/eps = {ec['max_|p|/eps']['value']:.3f}")
    print(f"   static lapse at centre = {sm['lapse_static_centre']:.4f} (interior clock rate vs infinity)")
    pmax = max(sm['p_r_peak_Pa'], sm['p_t_max_Pa'])
    print(f"   GAPS (log10 required/demonstrated):")
    print(f"     mass vs ISS                  : {gap(M, DEM['ISS_mass_kg']):6.2f}")
    print(f"     Mc^2 vs world energy per year: {gap(M*c**2, DEM['world_energy_J_per_yr']):6.2f}  (Mc^2 = {M*c**2:.3e} J)")
    print(f"     peak density vs osmium       : {gap(sm['rho_peak_kg_m3'], DEM['osmium_density']):6.2f}")
    print(f"     peak density vs nuclear sat. : {gap(sm['rho_peak_kg_m3'], rho_nuc):6.2f}")
    print(f"     peak stress vs 1 TPa static  : {gap(pmax, DEM['static_pressure_Pa']):6.2f}")
    print(f"     peak stress vs nanodiamond   : {gap(pmax, DEM['nanodiamond_yield_Pa']):6.2f}")
    print(f"     peak stress vs rho_nuc c^2   : {gap(pmax, rho_nuc*c**2):6.2f}")
print(f"   speed 0.02c vs Parker Solar Probe: {gap(0.02, DEM['PSP_speed_c']):.2f}; 0.04c: {gap(0.04, DEM['PSP_speed_c']):.2f}")

# ---------------- B. scaling laws ----------------
print("\n== B. Scaling at fixed compactness C = 2GM/(c^2 R2) = 1/3, R1 = R2/2 (ours) ==")
Cc = 1/3
def M_of(R2): return Cc * c**2 * R2 / (2*G)
def rho_mean(R2): return M_of(R2) / (4/3*math.pi*(R2**3 - (R2/2)**3))
for R2 in [20, 200, 2e3, 2e4]:
    print(f"  R2 = {R2:8.0f} m: M = {M_of(R2):.3e} kg ({M_of(R2)/MSUN:.3e} M_sun), mean rho = {rho_mean(R2):.3e} kg/m^3")
# radius at which mean density equals nuclear / osmium:  rho_mean ∝ 1/R2^2
k = rho_mean(1.0)
for lab, rho in [("nuclear saturation", rho_nuc), ("osmium", DEM['osmium_density'])]:
    R2 = math.sqrt(k / rho); print(f"  mean density = {lab} ({rho:.3g}) at R2 = {R2:.3e} m, M = {M_of(R2):.3e} kg = {M_of(R2)/MSUN:.3e} M_sun")
print("  law: M = C c^2 R2/(2G) ∝ R2 ; rho_mean ∝ C/R2^2 ; stress ~ rho c^2 x O(C) ∝ C^2/R2^2 (Newtonian G M rho/R)")

print("\n== B2. Weak-field gravitomagnetic counterflow estimate (OURS, order of magnitude) ==")
print("  Linearised GR: a mass current with momentum P on a shell of radius R gives a uniform interior")
print("  h_0i = 4 G P/(c^3 R). Counterflowing +P at R1 and -P at R2 gives interior beta = (4G P/c^3)(1/R1 - 1/R2)")
print("  with zero net exterior momentum. Momentum is bounded by energy: c P <= E_flow (DEC, u -> c).")
for beta, R1, R2 in [(0.02, 10, 20), (0.04, 10, 20), (0.02, 100, 200), (1e-6, 10, 20)]:
    Eflow = beta * c**4 / (4*G*(1/R1 - 1/R2))
    print(f"  beta={beta:g}, R1={R1}, R2={R2} m: E_flow,min = {Eflow:.3e} J = {Eflow/c**2:.3e} kg-equiv = {Eflow/c**2/MJ:.3e} M_J;"
          f" at u=0.1c needs mass {10*Eflow/c**2:.3e} kg; at u=10 km/s needs {Eflow/c**2*c/1e4:.3e} kg")
M_pub = 4.49e27
Eflow_pub = 0.02 * c**4 / (4*G*(1/10 - 1/20))
print(f"  published shell: E_flow,min / (M c^2) = {Eflow_pub/(M_pub*c**2):.3f}  -> effective counterflow speed ~ {Eflow_pub/(M_pub*c**2):.3f} c if half the mass flows each way")
print("  law: beta ~ (2G E_flow/(c^4 R1)) for R2 = 2 R1, i.e. beta ~ compactness x (u/c). Gap shrinks linearly in beta and R1.")

# ---------------- C. trip energies ----------------
print("\n== C. Trip: 1e5 kg payload to alpha Cen (4.37 ly) ==")
m_pay = 1e5
for v in [0.02, 0.04]:
    r1 = relativistic_mass_ratio(v_exhaust=c, v_final=v*c)
    rss = r1**2                                    # start and stop
    for label, m in [("shell+payload", M_pub + m_pay), ("payload alone", m_pay)]:
        prop = (rss - 1) * m
        print(f"  v={v}c photon rocket start+stop: mass ratio {rss:.4f}; {label}: propellant {prop:.3e} kg, energy {prop*c**2:.3e} J"
              f" = {prop*c**2/DEM['world_energy_J_per_yr']:.3e} world-years; gap vs 1 world-year {gap(prop*c**2, DEM['world_energy_J_per_yr']):.2f}")
    L = 2*math.atanh(v)                            # rapidity path length, start and stop (assumption)
    print(f"  Le radiative steering m_i/m_f = e^(3L), L = 2 artanh(v) = {L:.4f}: ratio {math.exp(3*L):.4f} vs photon rocket {rss:.4f}")
    print(f"  coast time at {v}c: {4.37/v:.1f} yr (flat space, acceleration time neglected)")
t = trip(distance=4.37*LY, accel=G0, v_exhaust=c)
print(f"  1 g photon rocket, payload only: ship {t['ship_years']:.2f} yr, Earth {t['earth_years']:.2f} yr, peak beta {t['peak_beta']:.3f}, mass ratio {t['mass_ratio']:.2f}, propellant energy {(t['mass_ratio']-1)*m_pay*c**2:.3e} J")
print(f"  shell/payload mass ratio = {M_pub/m_pay:.2e} (log10 {math.log10(M_pub/m_pay):.2f})")

# ---------------- D. superluminal: negative energy ----------------
print("\n== D. Superluminal options: negative energy required vs demonstrated (Casimir) ==")
cG = c**4 / G
# Alcubierre tanh profile, Delta = 2/sigma = 1 m, peak Eulerian density at the wall equator: (c^4/G)(1/32pi) v^2 f'^2, f'max ~ sigma/2
for v in [1.0, 10.0]:
    sigma = 2.0
    rho_req = cG / (32*math.pi) * v**2 * (sigma/2)**2
    print(f"  Alcubierre R=100 m, Delta=1 m, v={v}c: peak |rho| ~ {rho_req:.3e} J/m^3")
a = 1e-7                                       # Mohideen & Roy 1998 smallest separation 0.1 um
rho_cas = math.pi**2 * hbar * c / (720 * a**4)
E_cas_1m2 = math.pi**2 * hbar * c * 1.0 / (720 * a**3)
print(f"  Casimir parallel-plate energy density at a = 0.1 um: -{rho_cas:.3e} J/m^3; a 1 m^2 cavity holds -{E_cas_1m2:.3e} J (hypothetical area)")
rho_req10 = cG/(32*math.pi)*100*1.0
print(f"  density gap (v=10c): {gap(rho_req10, rho_cas):.2f} orders; (v=1c): {gap(rho_req10/100, rho_cas):.2f}")
for lab, Ekg in [("Alcubierre v=10c tanh [D-28]", 7.48e31), ("Alcubierre v=1c tanh [D-28]", 7.48e29),
                 ("Natario v=1c [D-34]", 6.0e33), ("Rodal E- at v=c [D-36]", 1.33e44/c**2),
                 ("Alcubierre at QI-limited wall v=10c [D-29]", 6.9e63)]:
    print(f"  {lab}: |E| = {Ekg*c**2:.3e} J; gap vs 1 m^2 Casimir cavity {gap(Ekg*c**2, E_cas_1m2):.1f}; vs world-year {gap(Ekg*c**2, DEM['world_energy_J_per_yr']):.1f}")
for Ms in [20, 50]:
    E = Ms*MSUN*c**2
    print(f"  Lentz v=10c, R=100 m, w=1 m, {Ms} M_sun [D-30a]: E = {E:.2e} J; gap vs NIF 8.6 MJ [D-47] {gap(E, 8.6e6):.1f}; vs world-year {gap(E, DEM['world_energy_J_per_yr']):.1f}")
d_QI = 1.6e-32; d_LHC = hbar*c/(13.6e12*1.602176634e-19)
print(f"  QI-limited wall 1.6e-32 m vs LHC probe scale hbar c/13.6 TeV = {d_LHC:.2e} m: {gap(d_LHC, d_QI):.1f} orders; vs 1 angstrom tolerance {gap(1e-10, d_QI):.1f}")
print("  scaling: Alcubierre |E| ∝ v^2 R^2/Delta ; Natario ∝ v^2 R^4/Delta^3 [D-28, D-34]")

# ---------------- E. experiments ----------------
print("\n== E. Experiments: predicted effect vs demonstrated sensitivity ==")
F_sig = 5e-16; ASD_dem = 3e-12; T = 1e6
sigF = ASD_dem / math.sqrt(T)
print(f"  Archimedes: signal ~{F_sig:.0e} N; prototype {ASD_dem:.0e} N/rtHz -> sigma over {T:.0e} s = {sigF:.1e} N; gap {gap(sigF, F_sig):.2f} orders;"
      f" torque need 1e-13 vs 7e-13 N m/rtHz: {gap(7e-13, 1e-13):.2f}")
# lab frame dragging at centre of a rotating ring (order of magnitude Omega ~ 2 G m omega/(c^2 R))
m, R, urim = 1e4, 1.0, 1e3
Om = 2*G*m*(urim/R)/(c**2*R)
print(f"  lab rotor m={m:.0e} kg, R={R} m, rim {urim:.0e} m/s: Omega_LT ~ {Om:.2e} rad/s vs GINGERINO 2e-15 rad/s: gap {gap(2e-15, Om):.1f} orders")
beta_lab = 4*G*m*urim/(c**3*R)
print(f"  same mass as counterflow: interior beta ~ {beta_lab:.2e}; Sagnac-like delay over 1 m ~ {beta_lab*1/c:.2e} s vs Fuchs shell 7.6e-9 s")
print(f"  Fuchs observable: 7.6 ns needs the full 2.4 M_J shell; gap to lab beta: {gap(0.02, beta_lab):.1f} orders in beta")
# Tajmar balance: photon-thrust threshold
print(f"  Tajmar balance: limit < 0.003 uN/W vs photon 0.0033 uN/W; Eagleworks claim 1.2 uN/W excluded by {gap(1.2, 0.003):.2f} orders")
# GW memory from accelerating the shell to 0.04c (order of magnitude h ~ 4 G dE_kin/(c^4 d))
KE = 0.5*M_pub*(0.04*c)**2
for d_pc in [1e3, 1e6]:
    d = d_pc*3.0857e16
    print(f"  GW memory from shell boost (KE {KE:.2e} J) at {d_pc:.0e} pc: h ~ {4*G*KE/(c**4*d):.1e}")

# ---------------- F. assembly heat and smoothing sensitivity ----------------
print("\n== F. Assembly binding energy (Newtonian order of magnitude) and smoothing sensitivity ==")
Eb = G*M_pub**2/15.0
print(f"  G M^2 / R_mean(15 m) = {Eb:.2e} J = {Eb/(M_pub*c**2):.2f} M c^2 released as heat on assembly; = {Eb/DEM['world_energy_J_per_yr']:.2e} world-years")
for frac in [0.5, 1.0, 2.0]:
    s = build_shell(4.49e27, 10.0, 20.0, beta_warp=0.02, span_P=frac)
    sm = s.summary(); ec = s.energy_conditions_static()
    print(f"  span_P = {frac} m: peak p_t = {sm['p_t_max_Pa']:.3e} Pa, min p_t = {sm['p_t_min_Pa']:.3e} Pa, max|p|/eps = {ec['max_|p|/eps']['value']:.3f}, DEC {'holds' if ec['DEC']['holds'] else 'FAILS'}")
