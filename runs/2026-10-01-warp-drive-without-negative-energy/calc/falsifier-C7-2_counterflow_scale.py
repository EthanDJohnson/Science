"""Falsifier C7, refuter 2 (scale): engineering scale of the counterflow reading of the 2024 warp shell.

SI units unless marked geo (G = c = 1, metres).
Linear GR, harmonic gauge, two thin counter-streaming sheets (+P at R1, -P at R2):
  beta = (4 G P / c^3) (1/R1 - 1/R2)          [verified in M-ENGINEER-05]
With half of M on each sheet at speed u (|u| << c):  P = (M/2) u gamma
  => beta = C * (u gamma / c) * (R2/R1 - 1),   C = 2GM/(c^2 R2).
"""
import math

G = 6.67430e-11
c = 2.99792458e8
MJUP = 1.898e27

M = 4.5105e27          # kg, M_ADM of the toolkit rebuild (warp_shell.py output)
R1, R2 = 10.0, 20.0    # m
beta = 0.02            # paper's energy-condition-checked shift
C = 2 * G * M / (c**2 * R2)
print(f"rebuild: M_ADM = {M:.4e} kg = {M/MJUP:.3f} MJup; C = 2GM/(c^2 R2) = {C:.4f}")
Mc2 = M * c**2
print(f"Mc^2 = {Mc2:.3e} J")

# 1. two-sheet minimum momentum per stream for beta = 0.02
P2 = beta * c**3 / (4 * G * (1 / R1 - 1 / R2))
print("\n[1] two-sheet (minimum-P) geometry")
print(f"  P per stream = {P2:.3e} kg m/s ; DEC floor E_flow >= 2cP = {2*c*P2:.3e} J = {2*c*P2/Mc2:.4f} Mc^2")
u2 = 2 * P2 / (M * c)
print(f"  whole-mass counterflow speed u = 2P/(Mc) = {u2:.4f} c")

# 2. actual Fuchs eq.28 profile: P+ per sign from M-MECHANIST-03 log (linear, beta = 0.02)
Pp = 6.758e34
print("\n[2] Fuchs eq.(28) sigmoid profile, P+ = 6.758e34 kg m/s per sign (M-MECHANIST-03)")
print(f"  ratio P+/P_two-sheet = {Pp/P2:.3f}")
print(f"  DEC floor E_flow >= 2cP+ = {2*c*Pp:.3e} J = {2*c*Pp/Mc2:.4f} Mc^2")
up = 2 * Pp / (M * c)
print(f"  whole-mass counterflow speed u = 2P+/(Mc) = {up:.4f} c")

# 3. kinetic energy locked in the counterflow (internal, recoverable, zero net momentum)
for u in (u2, up):
    g = 1 / math.sqrt(1 - u**2)
    print(f"  counterflow KE at u = {u:.3f} c: (gamma-1) M c^2 = {(g-1)*Mc2:.3e} J = {(g-1):.2e} Mc^2")

# 4. is 'about 0.07 C' the largest drag positive matter can make? DEC-limited linear counterflow
print("\n[4] linear counterflow beta/C = (u gamma) (R2/R1 - 1) at fixed geometry R2/R1 = 2")
beta_cap = 0.02386
print(f"  NEC cap of the rebuild profile: beta_crit = {beta_cap}, beta_crit/C = {beta_cap/C:.4f}")
for u in (0.0716, 0.1, 0.3, 0.5):
    g = 1 / math.sqrt(1 - u**2)
    b = C * u * g * (R2 / R1 - 1)
    print(f"  u = {u:.3f} c: beta = {b:.4f}, beta/C = {b/C:.3f}, x NEC-cap = {b/beta_cap:.2f}  (linear; invalid as beta -> O(N))")

# 5. 'shift per unit compactness' is not a geometry-free figure of merit
print("\n[5] beta/C at fixed u = 0.06 c for other aspect ratios (linear two-sheet law)")
for ratio in (1.05, 1.2, 2.0, 5.0, 10.0):
    b_over_C = 0.06 * (ratio - 1)
    # local compactness of inner sheet carrying M/2 at R1: G M/(c^2 R1) = C * ratio / 2
    C_in = C * ratio / 2
    print(f"  R2/R1 = {ratio:5.2f}: beta/C = {b_over_C:.4f}; inner-sheet local 2G(M/2)/(c^2 R1) = {C_in:.3f} at C = {C:.3f}"
          + ("  (exceeds Buchdahl 8/9)" if C_in > 8 / 9 else ""))

# 6. cost against a rocket: photon rocket start + stop, mass ratio (1+v)/(1-v)
print("\n[6] photon-rocket start-and-stop propellant (ideal)")
mpay = 1e5
for v in (0.026, 0.04):
    r = (1 + v) / (1 - v)
    print(f"  v = {v} c: ratio {r:.5f}; shell+payload propellant {(r-1)*(M+mpay):.3e} kg ;"
          f" payload alone {(r-1)*mpay:.3e} kg ; cost ratio {(M+mpay)/mpay:.2e}")
print(f"  counterflow set-up energy (u = {up:.3f} c) / payload-alone photon-rocket energy at 0.04c:"
      f" {((1/math.sqrt(1-up**2))-1)*Mc2 / (((1.04/0.96)-1)*mpay*c**2):.2e}")

# 7. dynamic stress of turning the poloidal counterflow at the wall ends vs the shell's own TOV stresses
rho = 1.531e23   # kg/m^3, rebuild peak density
for u in (u2, up):
    q = rho * (u * c)**2
    print(f"  rho u^2 at u = {u:.3f} c: {q:.3e} Pa ; vs rebuild p_t,max 3.866e39 Pa: {q/3.866e39:.3e}")
