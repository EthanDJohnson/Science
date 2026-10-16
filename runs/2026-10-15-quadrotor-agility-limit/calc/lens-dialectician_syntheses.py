"""Dialectician lens: three syntheses, each computed.

All SI units unless stated. g = 9.81 m/s^2.

S1. Perception-actuation coupling through body tilt (resolves "aerodynamics binds"
    vs "perception binds"): a body-fixed forward camera loses the direction of
    travel from its field of view once the vehicle tilts to accelerate. This caps
    usable horizontal acceleration well below the thrust-to-weight ceiling.

S2. Latency measured against course feature spacing (resolves "seen 28-32 m/s"
    vs "unseen 5-10 m/s" on the same vehicle class): the outer loop must track a
    reference whose temporal frequency is v / L, L = gate or obstacle spacing.

S3. First-order actuator lag is not transport delay (resolves "40 ms latency caps
    the loop at 3 Hz" vs "racing quads fly at 30 m/s"): a known pole is invertible,
    a delay is not; and the lag costs accel only on manoeuvres short vs tau_m.
"""
import math

g = 9.81
print("=" * 72)
print("S1. FoV-limited acceleration: tilt vs field of view")
print("=" * 72)


def a_fov(mount_deg, vfov_deg):
    """Max horizontal accel (m/s^2) keeping the horizontal velocity direction
    inside the camera cone. Body pitches nose-down by theta = atan(a/g); the
    travel direction then sits theta above body-x, the camera axis sits
    mount_deg above body-x, so need theta <= mount + vfov/2."""
    theta_max = math.radians(mount_deg + vfov_deg / 2.0)
    if theta_max >= math.radians(89.0):
        return float("inf")
    return g * math.tan(theta_max)


def a_thrust(twr):
    return g * math.sqrt(twr ** 2 - 1.0)


print(f"thrust ceiling at T/W 4.4 (A-20 platform): {a_thrust(4.4):.2f} m/s^2 "
      f"= {a_thrust(4.4)/g:.2f} g")
print(f"thrust ceiling at T/W 12.35 (mocap platform): {a_thrust(12.35):.2f} m/s^2 "
      f"= {a_thrust(12.35)/g:.2f} g")
print()
rows = [
    ("D435i depth, level mount", 0, 58),
    ("D435i depth, 30 deg up-tilt (A-20 above 7 m/s)", 30, 58),
    ("D435i depth, 45 deg up-tilt", 45, 58),
    ("MonoRace-class wide cam 115 deg vert, level", 0, 115),
    ("MonoRace-class wide cam, 30 deg up-tilt", 30, 115),
    ("hemispherical / omnidirectional", 0, 180),
]
for name, mount, vfov in rows:
    a = a_fov(mount, vfov)
    cap = min(a, a_thrust(4.4))
    print(f"{name:48s} mount={mount:3d} VFoV={vfov:4d} -> "
          f"a_FoV={a:8.2f} m/s^2 ({a/g:5.2f} g); binding a = {cap:6.2f} m/s^2 "
          f"({cap/g:4.2f} g) [{'FoV' if a < a_thrust(4.4) else 'thrust'}]")
print()


def v_dodge(s, tau, a, r=0.5):
    """Falanga lateral-dodge bound D-31: v = s / (tau + 2 sqrt(r/a))."""
    return s / (tau + 2.0 * math.sqrt(r / a))


def v_stop(s, tau, a):
    """Stop-before-obstacle bound D-32/A-33."""
    return a * (-tau + math.sqrt(tau ** 2 + 2.0 * s / a))


s, tau, r = 6.0, 0.050, 0.5
a_T = a_thrust(4.4)
a_F = a_fov(30, 58)
print(f"Loquercio-class inputs: s = {s} m, tau = {tau*1e3:.0f} ms, r = {r} m")
for label, a in (("thrust-limited", a_T), ("FoV-limited (30 deg, 58 deg VFoV)", a_F)):
    print(f"  {label:36s} a = {a:6.2f} m/s^2 -> v_dodge = {v_dodge(s,tau,a,r):5.2f} m/s, "
          f"v_stop = {v_stop(s,tau,a):5.2f} m/s")
print(f"  ratio of accels  = {a_T/a_F:.2f};  ratio of dodge speeds = "
      f"{v_dodge(s,tau,a_T,r)/v_dodge(s,tau,a_F,r):.2f}")
print(f"  observed hardware at 90% success (A-20): 5 m/s; 80% at 7 m/s; 60% at 10 m/s")
# what sensing range would the two accels need to reproduce 10 m/s?
for label, a in (("thrust-limited", a_T), ("FoV-limited", a_F)):
    s_need = 10.0 * (tau + 2.0 * math.sqrt(r / a))
    print(f"  range needed for v = 10 m/s, {label:16s}: s = {s_need:5.2f} m")
print()

print("=" * 72)
print("S2. Delay-limited outer loop vs course feature spacing")
print("=" * 72)


def wc_max(tau_eff, pm_deg=45.0):
    """A-32 / D-25: wc <= (pi/2 - PM)/tau_eff for L = (wc/s) e^{-s tau}."""
    return (math.pi / 2.0 - math.radians(pm_deg)) / tau_eff


def v_cap(tau_eff, L, k=1.0, pm_deg=45.0):
    """Reference manoeuvre frequency omega_ref = 2 pi v / L must satisfy
    k * omega_ref <= wc_max. k = 1 marginal tracking, k = 2-3 good tracking."""
    return wc_max(tau_eff, pm_deg) * L / (2.0 * math.pi * k)


cases = [
    ("Swift, seen gate track", 0.040, 75.0 / 7.0),
    ("MonoRace, seen gate track", 0.040, 150.0 / 11.0),
    ("Loquercio, unseen forest clutter", 0.100, 4.0),
    ("Loquercio, unseen forest clutter (L = 2 m)", 0.100, 2.0),
    ("unseen clutter with 17 ms image delay", 0.030, 4.0),
]
for name, tau_eff, L in cases:
    w = wc_max(tau_eff)
    print(f"{name:44s} tau_eff={tau_eff*1e3:5.1f} ms  wc={w:6.2f} rad/s "
          f"({w/(2*math.pi):4.2f} Hz)  L={L:5.2f} m -> "
          f"v(k=1)={v_cap(tau_eff,L,1):6.2f}  v(k=2)={v_cap(tau_eff,L,2):6.2f} m/s")
print()
r_pred = (150.0 / 11.0 / 0.040) / (4.0 / 0.100)
print(f"predicted seen:unseen speed ratio from L/tau alone = {r_pred:.2f}")
print("observed mean-speed ratio (MonoRace ~18 m/s seen vs A-20 7 m/s unseen) = "
      f"{18.0/7.0:.2f}; peak ratio 32.2/10 = {32.2/10:.2f}")
print("=> the L/tau bound is TIGHT in clutter and SLACK by about "
      f"{r_pred/(32.2/10):.1f}x on the gate track: regime split, not a single limit")
print()
# elasticities of the L/tau cap
print("elasticities of v_cap: d ln v / d ln L = +1 exactly; d ln v / d ln tau_eff = -1 exactly")
eps = 1e-4
for name, tau_eff, L in cases[:3]:
    e_tau = (math.log(v_cap(tau_eff * (1 + eps), L)) - math.log(v_cap(tau_eff, L))) / eps
    e_L = (math.log(v_cap(tau_eff, L * (1 + eps))) - math.log(v_cap(tau_eff, L))) / eps
    print(f"  numeric check {name:44s} e_tau={e_tau:+.4f} e_L={e_L:+.4f}")
print()

print("=" * 72)
print("S3. First-order actuator lag vs pure transport delay")
print("=" * 72)
tau_m = 0.0391  # A-03 motor (thrust) time constant


def wc_lag(tau, pm_deg=45.0):
    """L = (wc/s) * 1/(1 + s tau): PM = 90 - atan(wc tau) deg."""
    return math.tan(math.radians(90.0 - pm_deg)) / tau


print(f"tau = {tau_m*1e3:.1f} ms (A-03 motor thrust time constant)")
for pm in (45.0, 60.0):
    wl, wd = wc_lag(tau_m, pm), wc_max(tau_m, pm)
    print(f"  PM = {pm:4.0f} deg: wc with first-order lag = {wl:6.2f} rad/s "
          f"({wl/(2*math.pi):5.2f} Hz);  with pure delay = {wd:6.2f} rad/s "
          f"({wd/(2*math.pi):5.2f} Hz);  ratio = {wl/wd:4.2f}")
print("  => as raw phase loss the lag and the delay are within a factor ~1.3:")
print("     the difference is INVERTIBILITY, not phase.")
tau_transport = 0.002  # gyro-to-motor on-board path, assumption stated in the analysis
for pm in (45.0, 60.0):
    print(f"  with the lag pole cancelled by lead and only {tau_transport*1e3:.0f} ms "
          f"transport left: wc <= {wc_max(tau_transport, pm):7.1f} rad/s "
          f"({wc_max(tau_transport, pm)/(2*math.pi):6.1f} Hz) at PM {pm:.0f} deg")
print()


def accel_fraction(T_man, tau):
    """Mean of a first-order step response over [0, T]: 1 - (tau/T)(1 - e^{-T/tau}).
    Fraction of commanded accel actually delivered over a manoeuvre of length T."""
    return 1.0 - (tau / T_man) * (1.0 - math.exp(-T_man / tau))


print(f"actuator-lag accel loss over a manoeuvre of duration T (tau = {tau_m*1e3:.1f} ms):")
for T in (0.05, 0.10, 0.16, 0.23, 0.50, 1.00):
    f = accel_fraction(T, tau_m)
    # speed elasticity to accel ~ 0.45 (A-33 dodge-bound e_a)
    print(f"  T = {T*1e3:6.0f} ms -> a_eff/a_cmd = {f:5.3f} "
          f"(loss {100*(1-f):5.1f} %), speed cost ~ {100*(1-f**0.45):5.1f} %")
T_dodge_T = 2.0 * math.sqrt(0.5 / a_T)
T_dodge_F = 2.0 * math.sqrt(0.5 / a_F)
print(f"  dodge duration 2 sqrt(r/a): thrust-limited {T_dodge_T*1e3:.0f} ms "
      f"(a_eff/a = {accel_fraction(T_dodge_T, tau_m):.3f}); "
      f"FoV-limited {T_dodge_F*1e3:.0f} ms (a_eff/a = {accel_fraction(T_dodge_F, tau_m):.3f})")
print("  => actuator lag becomes a first-order term only for manoeuvres below "
      "about 150 ms, i.e. r/a small: high speed in tight clutter.")
print()
print("=" * 72)
print("Cross-check: which single relaxation buys the most speed in clutter?")
print("=" * 72)
base = dict(s=6.0, tau=0.100, a=a_F, r=0.5)
v0 = v_dodge(base["s"], base["tau"], base["a"], base["r"])
print(f"baseline (s=6 m, tau=100 ms, a = FoV-limited {a_F:.1f} m/s^2): v = {v0:.2f} m/s")
pert = 1.10
for key in ("s", "tau", "a"):
    kw = dict(base)
    kw[key] = base[key] * pert
    v1 = v_dodge(kw["s"], kw["tau"], kw["a"], kw["r"])
    e = math.log(v1 / v0) / math.log(pert)
    print(f"  +10 % in {key:4s}: v = {v1:5.2f} m/s, elasticity = {e:+.3f}")
# removing the FoV cap entirely (wide camera) is not a 10 % change but a factor
v_wide = v_dodge(base["s"], base["tau"], min(a_thrust(4.4), a_fov(30, 115)), base["r"])
print(f"  swap to a 115 deg-VFoV camera at 30 deg tilt (a = "
      f"{min(a_thrust(4.4), a_fov(30,115)):.1f} m/s^2): v = {v_wide:.2f} m/s "
      f"({100*(v_wide/v0-1):+.1f} %)")
v_range = v_dodge(12.0, base["tau"], base["a"], base["r"])
print(f"  double the usable range to 12 m instead: v = {v_range:.2f} m/s "
      f"({100*(v_range/v0-1):+.1f} %)")
v_lat = v_dodge(base["s"], 0.030, base["a"], base["r"])
print(f"  cut latency 100 -> 30 ms instead: v = {v_lat:.2f} m/s "
      f"({100*(v_lat/v0-1):+.1f} %)")
print()
print("=" * 72)
print("S1 corollary: thrust-to-weight at which the FoV cap takes over")
print("=" * 72)
print("a_FoV = g tan(theta_max) needs thrust T/W = sec(theta_max); above that,")
print("extra thrust cannot be used without losing the travel direction from the cone.")
for name, mount, vfov in rows[:5]:
    th = math.radians(min(mount + vfov / 2.0, 89.0))
    twr_sat = 1.0 / math.cos(th)
    print(f"  {name:48s} theta_max={math.degrees(th):5.1f} deg -> "
          f"T/W_saturation = {twr_sat:6.2f}")
print("  (platform T/W is 4.1-4.5 on every onboard-only vehicle in the dossier, A-13)")
