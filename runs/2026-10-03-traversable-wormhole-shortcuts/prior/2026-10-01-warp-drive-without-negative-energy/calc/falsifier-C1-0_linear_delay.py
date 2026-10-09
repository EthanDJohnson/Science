"""Falsifier C1-0 (physics angle).

Part 1. Linear theory (G = c = 1, lengths in m): a stationary source gives
  hbar_ab(x) = 4 * int T_ab(x') / |x - x'| d^3x'.
For a null ray k = (1, n), h_ab k^a k^b = hbar_ab k^a k^b (trace term drops out since k is null),
and the one-way delay relative to flat space is
  dt = (1/2) * int h_kk dlambda = 2 * int dlambda int T_kk(x') / |x(lambda) - x'| d^3x'.
With NEC, T_kk >= 0 pointwise and the kernel is positive, so dt >= 0 for ANY ray, generic or not.
We test the attack case: the counter-streaming warp shell (two thin shells R1 < R2, dust streams
with velocities u1 > 0 and u2 < 0 along x, zero net momentum), which produces a uniform interior
shift beta = 4 P (1/R1 - 1/R2). We search for the parameters most favourable to an advance on the +x
ray through the centre and check whether the delay can go negative.

Part 2. 1+1 unit-lapse shift metric ds^2 = -dt^2 + (dx - X dt)^2 with X = const inside, 0 outside.
A free payload entering from rest at infinity has Killing energy E = 1. Find its interior coordinate
velocity and its exit velocity: does the shift hand the payload any net velocity relative to the exterior?
"""
import numpy as np
import sympy as sp

G = 6.674e-11; c = 2.998e8
M_SI = 4.511e27            # kg, ADM mass of the run's rebuilt shell
M = G * M_SI / c**2        # geometric mass, m
R1, R2 = 10.0, 20.0        # m
print("=== Part 1: linear one-way delay through a counter-streaming shell (geometric, m) ===")
print(f"M_geo = {M:.4f} m (M = {M_SI:.3e} kg)")

def line_integral(R, D):
    # int_{-D}^{D} dlambda / max(|lambda|, R) along a ray through the centre
    return 2.0 * (1.0 + np.log(D / R))

def delays(f1, u1, D):
    """f1: fraction of the mass-energy on shell 1; u1 in (0,1); shell 2 speed fixed by zero net momentum.
    Returns (dt_plus, dt_minus, beta, u2) in metres of light-travel (divide by c for seconds)."""
    E1 = f1 * M; E2 = (1 - f1) * M
    P = E1 * u1                      # momentum of stream 1 (+x)
    u2 = -P / E2                     # zero net momentum
    if abs(u2) >= 1.0:
        return None
    # dust stream: T_00 = eps, T_0x = -eps*u, T_xx = eps*u^2 (lower indices, signature -+++)
    # +x ray k=(1,1,0,0): T_kk = eps (1-u)^2 ; -x ray: eps (1+u)^2
    Qp = [E1 * (1 - u1)**2, E2 * (1 - u2)**2]
    Qm = [E1 * (1 + u1)**2, E2 * (1 + u2)**2]
    I = [line_integral(R1, D), line_integral(R2, D)]
    dtp = 2 * sum(q * i for q, i in zip(Qp, I))
    dtm = 2 * sum(q * i for q, i in zip(Qm, I))
    beta = 4 * P * (1 / R1 - 1 / R2)
    return dtp, dtm, beta, u2

for D in (1e3, 1e5):
    best = None
    for f1 in np.linspace(0.01, 0.99, 197):
        for u1 in np.linspace(0.0, 0.999, 1000):
            r = delays(f1, u1, D)
            if r is None:
                continue
            if best is None or r[0] < best[0][0]:
                best = (r, f1, u1)
    (dtp, dtm, beta, u2), f1, u1 = best
    print(f"D = {D:.0e} m: minimum +x delay over (f1, u1) = {dtp:.4e} m = {dtp / c * 1e9:.3f} ns "
          f"at f1 = {f1:.3f}, u1 = {u1:.3f}, u2 = {u2:.3f}; -x delay {dtm / c * 1e9:.3f} ns; "
          f"interior linear shift beta = {beta:.3f}")
    r0 = delays(0.5, 0.0, D)
    print(f"   same shell with no streams (beta = 0): +x delay {r0[0] / c * 1e9:.3f} ns")
# at the run's beta = 0.02 and 0.04, with equal halves
for btarget in (0.02, 0.04):
    P = btarget / (4 * (1 / R1 - 1 / R2)); u1 = P / (0.5 * M)
    r = delays(0.5, u1, 1e3)
    print(f"beta = {btarget}: P_geo = {P:.4f} m, u1 = {u1:.4f}; +x delay {r[0] / c * 1e9:.2f} ns, -x {r[1] / c * 1e9:.2f} ns "
          f"(linear, thin shells, D = 1e3 m)")
print("Analytic: every term E_i (1 -+ u_i)^2 * 2(1+ln(D/R_i)) >= 0; the +x delay vanishes only if all the")
print("mass-energy moves at u = +1 (null dust along the ray), where zero net momentum is impossible.")

print()
print("=== Part 2: free payload through a unit-lapse shift region (1+1, geometric) ===")
X, v = sp.symbols('X v', real=True)
ut = 1 / ((1 - X**2) + X * v)                      # from E = (1-X^2) u^t + X u^x = 1, u^x = v u^t
norm = sp.simplify(ut**2 * ((1 - X**2) + 2 * X * v - v**2) - 1)
sols = sp.solve(sp.numer(sp.together(norm)), v)
print("interior coordinate velocities with E = 1 (payload from rest at infinity):", sols)
Erest = sp.simplify((1 - X**2) / sp.sqrt(1 - X**2))
print("Killing energy of a payload at rest relative to the shell inside: E =", Erest,
      "; at X = 0.04:", float(Erest.subs(X, 0.04)))
print("Exterior (X = 0) with E = 1: v = 0. A payload from rest drifts with the Eulerian flow (v = X) inside")
print("and leaves at rest: the shift gives no net velocity relative to the exterior.")
