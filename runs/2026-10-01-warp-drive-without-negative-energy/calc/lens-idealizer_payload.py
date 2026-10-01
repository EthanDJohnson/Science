"""Idealizer lens: what the shift does (and does not do) for a payload; start/stop budget.

SI unless stated; geometric (G = c = 1, metres) where marked.
1. Interior lapse of the 2024 shell (run tool warp_shell.py, beta = 0.02) and the speed of
   cavity Eulerian observers relative to the cavity-comoving (Killing) payload; time for an
   Eulerian observer to cross the cavity and hit the wall.
2. Net momentum carried by the shift's wall currents (should be zero: surface term).
3. Start/stop momentum and photon-rocket propellant for the shell vs the bare payload.
4. Naive weak-field linear-acceleration dragging coefficient 4GM/(c^2 R) (ours; harmonic gauge,
   ignoring the stresses of whatever pushes the shell).
"""
import math, sys
import numpy as np
sys.path.insert(0, "runs/2026-10-01-warp-drive-without-negative-energy/tools")
from warp_shell import build_shell

G = 6.67430e-11; C = 299792458.0; MJ = 1.898e27
M = 4.49e27; R1 = 10.0; R2 = 20.0

print("=== 1. Cavity kinematics in the paper's comoving frame ===")
for beta in (0.02, 0.04):
    s = build_shell(M=M, R1=R1, R2=R2, beta_warp=beta)
    g = s.metric_cartesian(0.0, 0.0, 0.0, 0.0)
    g00, g0x = g[0][0], g[0][1]
    e2a = -g00
    N = math.sqrt(e2a + g0x**2)          # ADM lapse (h_xx = 1 in the flat cavity)
    u_rel = abs(g0x)/N                   # Eulerian speed relative to Killing observers (units of c)
    t_cross = 2*R1/(u_rel*C)             # coordinate-ish time to cross the cavity diameter
    print(f"  beta_warp={beta}: g00 = {g00:.6f} (payload clock rate sqrt(-g00) = {math.sqrt(e2a):.6f}, "
          f"same as the unshifted shell), g0x = {g0x:.4f}, N = {N:.6f}")
    print(f"     cavity Eulerian observers move at {u_rel:.4f} c relative to the cavity walls; "
          f"they reach the wall within ~{t_cross*1e6:.2f} microseconds")
s0 = build_shell(M=M, R1=R1, R2=R2, beta_warp=0.0)
g0 = s0.metric_cartesian(0.0, 0.0, 0.0, 0.0)
print(f"  unshifted shell: g00 = {g0[0][0]:.6f}  -> identical g00: no proper-time gain for the payload")

print()
print("=== 2. Net momentum of the shift currents (linear, geometric units) ===")
# T_0z per unit beta for w = beta*S(r) zhat, cubic smoothstep, integrated over the wall
nr, na = 4000, 2001
r = np.linspace(R1, R2, nr); ca = np.linspace(-1, 1, na)
RR, CA = np.meshgrid(r, ca, indexing="ij")
sv = (RR - R1)/(R2 - R1); D = R2 - R1
fp = -(6*sv - 6*sv**2)/D; fpp = -(6 - 12*sv)/D**2
jz = (-fpp*(1 - CA**2) - fp*(1 + CA**2)/RR)/(16*math.pi)
P = np.trapezoid(np.trapezoid(jz*2*math.pi*RR**2, ca, axis=1), r)
Pabs = np.trapezoid(np.trapezoid(np.abs(jz)*2*math.pi*RR**2, ca, axis=1), r)
print(f"  int T_0z dV / beta = {P:.3e} m  vs  int |T_0z| dV / beta = {Pabs:.3e} m  (ratio {P/Pabs:.1e}: net zero)")
print("  => the 'warp' carries no net momentum; moving the payload means moving the whole mass M.")

print()
print("=== 3. Start-and-stop budget at 0.04 c (photon rocket, ideal) ===")
b = 0.04
g = 1/math.sqrt(1 - b**2)
p_shell = g*M*b*C
ratio_one = math.sqrt((1 + b)/(1 - b))        # mass ratio per burn, photon rocket
ratio_ss = ratio_one**2
for name, m in [("shell + payload (M = 4.49e27 kg)", M), ("payload alone (1e5 kg)", 1e5)]:
    prop = m*(ratio_ss - 1)
    print(f"  {name}: momentum per burn = {g*m*b*C:.3e} kg m/s; start+stop mass ratio = {ratio_ss:.4f}; "
          f"propellant = {prop:.3e} kg ({prop/MJ:.3e} M_J)")
print(f"  ratio of propellant needs = {M/1e5:.2e}")

print()
print("=== 4. Naive weak-field linear dragging of interior frames by an accelerated shell (ours) ===")
for R in (R1, R2, 100.0):
    c4 = 4*G*M/(C**2*R)
    print(f"  4GM/(c^2 R) at R = {R:g} m: {c4:.3f}  (>~1 means linear theory fails; strong dragging)")
print("  A fraction ~4GM/(c^2 R) of the shell's acceleration is felt as free fall inside: a property of")
print("  any massive shell, shift or not.")
