"""Theory-facet calculations (analysis only, no hardware numbers claimed).

A. Delay-limited loop bandwidth: for a loop L(s) = wc/s * exp(-s*tau) (rate loop / integrator-like plant)
   and for PD on a double integrator, the largest gain-crossover frequency wc that keeps a phase margin PM
   when the total effective delay is tau_eff = tau_sense + tau_compute + T/2 (ZOH) [+ any motor lag].
B. Look-ahead needed at speed v: stopping bound  v*tau + v^2/(2a) <= s  (closed form) and Falanga et al. 2019
   lateral-dodge bound v = s/(tau + 2 sqrt(r/a)).
C. Elasticities (d ln v / d ln x) of both bounds with respect to s, tau, a, analytic and finite-difference.
D. Point-mass time-optimal rest-to-rest time t = 2 sqrt(d/a) with a = g sqrt((T/W)^2 - 1) (level flight, thrust
   vector tilted, altitude held) -- the thrust-to-weight ceiling reference.

Units: SI (m, s, rad, m/s^2). g = 9.81 m/s^2. Inputs are illustrative generic values (not measured data); the
measured values belong to the quantitative facet.
"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
from control_tools import loop_margins

G = 9.81
print("=== Inputs/units: SI; g = %.2f m/s^2 ===" % G)

# ---------------- A. delay margin and bandwidth ----------------
print("\n[A] Verification: L = wc/s * exp(-s tau); closed form PM = pi/2 - wc*tau, delay margin = (pi/2)/wc")
print("  (loop_margins' delay_margin is the EXTRA delay beyond tau already in L; total tolerable delay = tau + tool dm.")
print("   Grid is offset so that wc is not exactly a grid point -- an exact hit makes the sign-change crossing search miss it.)")
for wc, tau in [(20.0, 0.010), (50.0, 0.020), (100.0, 0.005)]:
    L = lambda s, wc=wc, tau=tau: wc / s * np.exp(-s * tau)
    m = loop_margins(L, 0.1371, 1.0e4 * 1.0137, 4001)
    pm_cf = (math.pi / 2 - wc * tau)
    print("  wc=%6.1f rad/s tau=%5.1f ms : PM tool=%.4f rad  closed-form=%.4f rad | total delay tolerated: tool tau+dm=%.5f s closed-form pi/(2 wc)=%.5f s"
          % (wc, tau * 1e3, m['phase_margin_deg'] * math.pi / 180, pm_cf, tau + m['delay_margin'], (math.pi / 2) / wc))

print("\n  Max wc for integrator-like loop with phase margin PM, effective delay tau_eff (wc = (pi/2 - PM)/tau_eff):")
print("  tau_eff[ms]   wc(PM=45deg)[rad/s]  f=wc/2pi[Hz]   wc(PM=60deg)[rad/s]  f[Hz]")
for te in [2, 5, 10, 20, 40]:
    t = te * 1e-3
    w45 = (math.pi / 2 - math.radians(45)) / t
    w60 = (math.pi / 2 - math.radians(60)) / t
    print("  %6.1f        %8.1f           %6.1f        %8.1f           %6.1f" % (te, w45, w45 / 2 / math.pi, w60, w60 / 2 / math.pi))

print("\n  Effective delay budget: tau_eff = tau_sense + tau_compute + T/2 (ZOH half-sample) -- examples")
for (ts, tc, T) in [(0.002, 0.001, 0.001), (0.002, 0.002, 0.002), (0.020, 0.005, 0.005), (0.050, 0.010, 0.0167)]:
    print("   tau_sense=%5.1f ms tau_compute=%4.1f ms T=%5.2f ms -> tau_eff=%6.2f ms" % (ts * 1e3, tc * 1e3, T * 1e3, (ts + tc + T / 2) * 1e3))

print("\n  PD on double integrator P=1/s^2: C = kp + kd s, delay tau. Max delay margin over wc for fixed zero placement wz = wc/3")
def dm_pd(wc, tau_unused=0.0, ratio=3.0):
    # choose kd so zero at wz = wc/ratio; kp = kd*wz ; scale gain so |L(j wc)| = 1
    wz = wc / ratio
    L0 = lambda s: (wz + s) / (s * s)
    k = 1.0 / abs(L0(1j * wc))
    L = lambda s: k * (wz + s) / (s * s)
    m = loop_margins(L, wc / 997.0, wc * 1013.0, 6001)
    return m['phase_margin_deg'], m['delay_margin']
for wc in [10.0, 30.0, 100.0]:
    pm, dm = dm_pd(wc)
    pm_cf = math.degrees(math.atan(3.0))   # phase of (1 + s/wz) at wc = atan(wc/wz); plant -180 => PM = atan(3)
    print("   wc=%6.1f rad/s: PM tool=%.3f deg closed-form atan(3)=%.3f deg | delay margin = %.2f ms ; wc*delay_margin=%.4f rad (closed form %.4f)"
          % (wc, pm, pm_cf, dm * 1e3, wc * dm, math.radians(pm_cf)))

# ---------------- B. look-ahead ----------------
def v_stop(s, tau, a):
    # v tau + v^2/(2a) = s  -> v = a(-tau + sqrt(tau^2 + 2 s / a))
    return a * (-tau + math.sqrt(tau * tau + 2 * s / a))
def v_falanga(s, tau, a, r=0.5):
    return s / (tau + 2 * math.sqrt(r / a))
def s_needed_stop(v, tau, a):
    return v * tau + v * v / (2 * a)

print("\n[B] Verification of stopping bound by direct integration (dt=1e-5 s): vehicle at speed v runs blind for tau then brakes at a")
def sim_stop(v, tau, a, dt=1e-5):
    x = 0.0; t = 0.0
    while t < tau:
        x += v * dt; t += dt
    vv = v
    while vv > 0:
        x += vv * dt; vv -= a * dt
    return x
for (v, tau, a) in [(10, 0.05, 20.0), (20, 0.1, 40.0), (30, 0.02, 30.0)]:
    print("   v=%4.1f m/s tau=%5.1f ms a=%5.1f m/s^2 : closed form s=%.4f m, simulated s=%.4f m" %
          (v, tau * 1e3, a, s_needed_stop(v, tau, a), sim_stop(v, tau, a)))
print("   limit tau=0: v=sqrt(2 a s): s=10 m a=20 -> %.4f vs %.4f" % (v_stop(10, 0, 20), math.sqrt(2 * 10 * 20)))

print("\n  Max safe speed [m/s]: stop-before-obstacle bound v_stop, and Falanga lateral-dodge bound v_F (r=0.5 m)")
print("  a[m/s^2]=lateral/brake accel ; s=sensing range")
print("   s[m]  tau[ms]  a=10(1g)   a=20(2g)   a=40(4g) | Falanga: a=10    a=20    a=40")
for s in [3.0, 6.0, 10.0]:
    for tau in [0.0, 0.02, 0.05, 0.1]:
        row = [v_stop(s, tau, a) for a in (10, 20, 40)]
        rowf = [v_falanga(s, tau, a) for a in (10, 20, 40)]
        print("   %4.1f  %5.0f   %8.2f  %8.2f  %8.2f |       %7.2f %7.2f %7.2f" % (s, tau * 1e3, *row, *rowf))

# ---------------- C. elasticities ----------------
print("\n[C] Elasticities d ln v / d ln x of the two bounds (finite difference 1e-4 vs analytic)")
def elas(f, args, i, h=1e-4):
    a1 = list(args); a2 = list(args)
    a1[i] *= (1 + h); a2[i] *= (1 - h)
    return (math.log(f(*a1)) - math.log(f(*a2))) / (math.log(1 + h) - math.log(1 - h))
for (s, tau, a) in [(6.0, 0.05, 20.0), (6.0, 0.02, 40.0), (10.0, 0.1, 20.0)]:
    # analytic stop-bound: v = a(-tau + sqrt(tau^2+2s/a)), q = sqrt(tau^2+2s/a)
    q = math.sqrt(tau * tau + 2 * s / a); v = v_stop(s, tau, a)
    e_s_an = (s / a / q) * a / v           # dv/ds = 1/q
    e_tau_an = tau * a * (-1 + tau / q) / v
    # dv/da = (-tau + q) + a*(-s/a^2)/q  -> times a/v
    e_a_an = a * ((-tau + q) - s / (a * q)) / v
    print("   stop bound s=%.1f tau=%.0f ms a=%.0f : v=%.2f m/s | e_s FD=%.4f an=%.4f | e_tau FD=%.4f an=%.4f | e_a FD=%.4f an=%.4f | sum e_s... (v homogeneous check e_s+e_tau*? skip)"
          % (s, tau * 1e3, a, v, elas(v_stop, (s, tau, a), 0), e_s_an, elas(v_stop, (s, tau, a), 1), e_tau_an, elas(v_stop, (s, tau, a), 2), e_a_an))
    print("   Falanga bound same inputs      : v=%.2f m/s | e_s=%.4f | e_tau=%.4f | e_a=%.4f   (analytic e_s=1, e_tau=-tau/(tau+2sqrt(r/a)), e_a=+sqrt(r/a)/(tau+2sqrt(r/a)))"
          % (v_falanga(s, tau, a), elas(v_falanga, (s, tau, a), 0), elas(v_falanga, (s, tau, a), 1), elas(v_falanga, (s, tau, a), 2)))
    d = 2 * math.sqrt(0.5 / a)
    print("      analytic Falanga e_tau=%.4f e_a=%.4f" % (-tau / (tau + d), (d / 2) / (tau + d)))

print("\n  Crossing speed where latency term equals braking term in the stop bound: v*tau = v^2/(2a)  ->  v_x = 2 a tau")
for (a, tau) in [(20.0, 0.05), (20.0, 0.02), (40.0, 0.05), (10.0, 0.1)]:
    print("   a=%.0f m/s^2 tau=%.0f ms : v_x = %.2f m/s (below this speed the blind-flight distance v*tau exceeds the braking distance; above it the braking distance v^2/(2a) dominates the look-ahead need)"
          % (a, tau * 1e3, 2 * a * tau))

# ---------------- D. thrust-to-weight ceiling ----------------
print("\n[D] Point-mass bound: a_h = g sqrt((T/W)^2 - 1) (level, altitude held); rest-to-rest bang-bang t = 2 sqrt(d/a_h); peak v = sqrt(a_h d)")
def a_h(twr): return G * math.sqrt(twr * twr - 1)
def t_bb(d, a): return 2 * math.sqrt(d / a)
def sim_bb(d, a, dt=1e-5):
    x = v = t = 0.0
    while x < d / 2:
        v += a * dt; x += v * dt; t += dt
    return 2 * t
print("   Verification of bang-bang closed form by integration: d=10 m a=30 m/s^2 -> closed %.4f s, integrated %.4f s" % (t_bb(10, 30), sim_bb(10, 30)))
print("   limit T/W->1: a_h=%.3f (expect 0); T/W=sqrt(2): a_h=%.3f (expect g=%.3f)" % (a_h(1.0), a_h(math.sqrt(2)), G))
print("   T/W    a_h[m/s^2]  a_h/g   t(d=10m)[s]   v_peak(d=10m)[m/s]   v_avg(d=10m)[m/s]")
for twr in [2, 3, 4, 6, 8]:
    a = a_h(twr)
    print("   %3.0f    %7.2f    %5.2f   %7.3f      %7.2f             %7.2f" % (twr, a, a / G, t_bb(10, a), math.sqrt(a * 10), 10 / t_bb(10, a)))
print("   Elasticity of rest-to-rest time to a_h: d ln t/d ln a = -1/2 exactly; elasticity of a_h to T/W = (T/W)^2/((T/W)^2-1):")
for twr in [2, 4, 8]:
    print("      T/W=%d : %.4f" % (twr, twr ** 2 / (twr ** 2 - 1)))
