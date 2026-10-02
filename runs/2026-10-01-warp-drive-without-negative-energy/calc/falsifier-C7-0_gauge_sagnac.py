"""Falsifier C7-0 (physics): is the interior shift of a stationary shell an invariant?
Units: geometric (G = c = 1) for the symbolic part; SI for numbers.

1. A stationary metric keeps its Killing vector d/dt under t = t' + F(x,y,z) (F time-independent).
   g'_0i = g_0i + g_00 dF/dx^i. Choose F = (beta/N^2) x in the flat cavity -> cavity shift vanishes.
   Check symbolically that the cavity metric becomes diag(-N^2, 1 + beta^2/N^2, 1, 1) (static, prolate)
   with N^2 - beta^2 = -g_00 kept.
2. The Sagnac one-form omega = g_0i dx^i / (-g_00) changes by -dF: loop integrals are invariant,
   so the only invariant content is the holonomy (gravitomagnetic flux, B_g = d omega, wall-confined).
3. Counterflow energy floor: E_flow >= 2 c P per stream pair, with P from the two models in the run.
4. Clock of a shell-static payload: rate sqrt(-g_00), unchanged when g_00 is held fixed (toolkit/paper);
   the 3.4e-4 'deficit' is relative to the Eulerian observer only.
"""
import sympy as sp

t, tp, x, y, z, N, b = sp.symbols("t tp x y z N beta", positive=True)
# interior: ds^2 = -N^2 dt^2 + (dx + beta dt)^2 + dy^2 + dz^2  (convention g_0x = +beta)
X = [t, x, y, z]
g = sp.Matrix([[-N**2 + b**2, b, 0, 0], [b, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
F = (b / (N**2 - b**2)) * x  # exact resynchronization (use -g_00 = N^2 - beta^2)
# new coords (tp, x, y, z) with t = tp + F
Xp = [tp, x, y, z]
tsub = tp + F
J = sp.Matrix([[sp.diff(e, v) for v in Xp] for e in [tsub, x, y, z]])
gp = sp.simplify(J.T * g * J)
print("1. cavity metric after t = t' + beta x/(N^2-beta^2):")
sp.pprint(gp)
print("   g'_0x =", sp.simplify(gp[0, 1]), "; g'_00 =", sp.simplify(gp[0, 0]), "; g'_xx =", sp.simplify(gp[1, 1]))
print("   g'_xx equals N^2/(N^2-beta^2):", sp.simplify(gp[1, 1] - N**2 / (N**2 - b**2)) == 0)

# 2. Sagnac one-form transformation, generic stationary metric components
g00 = sp.Function("g00")(x, y, z)
g0 = [sp.Function(f"g0{i}")(x, y, z) for i in (1, 2, 3)]
Fg = sp.Function("F")(x, y, z)
# under t = t' + F: g'_0i = g_0i + g_00 * dF/dx^i
omega = [g0[i] / (-g00) for i in range(3)]
omegap = [(g0[i] + g00 * sp.diff(Fg, [x, y, z][i])) / (-g00) for i in range(3)]
diff = [sp.simplify(omegap[i] - omega[i] + sp.diff(Fg, [x, y, z][i])) for i in range(3)]
print("2. omega' - omega + dF (should be 0,0,0):", diff, "-> loop integrals of omega invariant")

# 3. counterflow energy floors (SI)
c = 2.99792458e8
M_adm, M_pub = 4.511e27, 4.49e27
P_smooth = 6.758e34   # kg m/s per sign, rebuild profile (M-MECHANIST-03)
P_layers = 4.04e34    # kg m/s per stream, two thin layers at R1, R2 (M-ENGINEER-05)
G = 6.67430e-11
beta_layers = 4 * G * P_layers / c**3 * (1 / 10.0 - 1 / 20.0)
print(f"3. two-layer model beta from P = {P_layers:.3e}: {beta_layers:.4f}")
for name, P in (("rebuild profile", P_smooth), ("two thin layers", P_layers)):
    E = 2 * c * P
    print(f"   {name}: P = {P:.3e} kg m/s, E_flow >= 2cP = {E:.3e} J = {E/(M_adm*c**2):.4f} M_ADM c^2"
          f" = {E/(M_pub*c**2):.4f} M_pub c^2; whole-mass counterflow u = 2P/M = {2*P/M_adm/c:.4f} c")

# 4. clocks
e2a = 0.5793  # -g_00 in cavity (toolkit, quoted in M-IDEALIZER-10), held fixed under shift
for beta in (0.0, 0.02, 0.04):
    Nb = (e2a + beta**2) ** 0.5
    rate_static = e2a ** 0.5
    rate_euler = Nb
    print(f"4. beta={beta}: shell-static clock rate sqrt(-g00) = {rate_static:.6f} (same for all beta); "
          f"Eulerian lapse N = {Nb:.6f}; static/Eulerian deficit = {1-rate_static/Nb:.3e}")
