"""Falsifier C4-0: where does Lentz's positive total Eulerian energy come from?

Geometric units G = c = 1 (lengths in arbitrary units L; energies in L).
Lentz 2021 (arXiv 2006.07125) metric class: unit lapse, flat slices h_ij = delta_ij, shift N_i = d_i phi
(curl-free), with phi parameterised by (z, s), s = |x| + |y| (his eq. 17 set-up). Eulerian density (his eq. 6-7):
    16 pi E = K^2 - K^i_j K^j_i  with K_ij = -(1/2)(d_i N_j + d_j N_i) = -d_i d_j phi
            = (Lap phi)^2 - |Hess phi|^2   = d_i( d_i phi Lap phi - d_j phi d_i d_j phi )   (a pure divergence)
So for a compactly supported (or fast-decaying) shift, int E d^3x = 0 in the sense of distributions.

With phi = g(z, |x|+|y|) and g_s(z,0) != 0, N_x = sign(x) g_s jumps across x = 0 (likewise N_y across y = 0):
  - absolutely continuous part (x, y != 0):   E_ac   = (1/4pi) (g_ss g_zz - g_zs^2)
  - sheet on x = 0 (and y = 0):               E_sh   = (1/4pi) g_s (g_ss + g_zz) delta(x)   at s = |y|
  - line on x = y = 0:                        E_line = (1/2pi) g_s^2 delta(x) delta(y)
(derived by expanding Lentz's eq. 7 with d_x N_x = 2 delta(x) g_s + g_ss, etc.)
Method A: exact reduction to (z, s) integrals (area element of |x|+|y| <= s is 4 s ds).
Method B: independent 3D finite differences of Lentz's eq. 7 on a Cartesian grid; cells straddling x=0 / y=0
          pick up the delta contributions automatically.
"""
import numpy as np

PI = np.pi


def g_fun(z, s, s0, a=1.0, b=0.5):
    return np.exp(-(z / a) ** 2 - ((s - s0) / b) ** 2)


def derivs(z, s, s0, a=1.0, b=0.5):
    g = g_fun(z, s, s0, a, b)
    gz = -2 * z / a**2 * g
    gs = -2 * (s - s0) / b**2 * g
    gzz = (4 * z**2 / a**4 - 2 / a**2) * g
    gss = (4 * (s - s0) ** 2 / b**4 - 2 / b**2) * g
    gzs = (4 * z * (s - s0) / (a**2 * b**2)) * g
    return g, gz, gs, gzz, gss, gzs


def method_a(s0, n=4001):
    z = np.linspace(-6, 6, n)
    s = np.linspace(0, s0 + 5, n)
    Z, S = np.meshgrid(z, s, indexing="ij")
    g, gz, gs, gzz, gss, gzs = derivs(Z, S, s0)
    dz, ds = z[1] - z[0], s[1] - s[0]
    e_ac = (gss * gzz - gzs**2) / (4 * PI)
    E_ac = np.trapezoid(np.trapezoid(e_ac * 4 * S, s, axis=1), z)
    # two sheets (x=0 and y=0), each covering s=|y| in (-inf, inf) -> 2 * int_0^inf ds
    e_sh = gs * (gss + gzz) / (4 * PI)
    E_sh = 2 * 2 * np.trapezoid(np.trapezoid(e_sh, s, axis=1), z)
    E_line = np.trapezoid((gs[:, 0] ** 2) / (2 * PI), z)
    pos = np.trapezoid(np.trapezoid(np.clip(e_ac, 0, None) * 4 * S, s, axis=1), z)
    neg = np.trapezoid(np.trapezoid(np.clip(e_ac, None, 0) * 4 * S, s, axis=1), z)
    return E_ac, E_sh, E_line, pos, neg


def method_b(s0, n):
    L = s0 + 4.5
    x = np.linspace(-L, L, n)
    zz = np.linspace(-6, 6, n)
    h, hz = x[1] - x[0], zz[1] - zz[0]
    X, Y, Z = np.meshgrid(x, x, zz, indexing="ij")
    phi = g_fun(Z, np.abs(X) + np.abs(Y), s0)
    # shift at cell faces via central differences on a staggered sense: use np.gradient (2nd order interior)
    Nx, Ny, Nz = np.gradient(phi, h, h, hz)
    dxNx, dyNx, dzNx = np.gradient(Nx, h, h, hz)
    dxNy, dyNy, dzNy = np.gradient(Ny, h, h, hz)
    dxNz, dyNz, dzNz = np.gradient(Nz, h, h, hz)
    e16 = (2 * dxNx * dyNy + 2 * dxNx * dzNz + 2 * dzNz * dyNy
           - 0.5 * (dxNy + dyNx) ** 2 - 0.5 * (dxNz + dzNx) ** 2 - 0.5 * (dzNy + dyNz) ** 2)
    E = e16 / (16 * PI)
    dV = h * h * hz
    total = E.sum() * dV
    away = (np.abs(X) > 3 * h) & (np.abs(Y) > 3 * h)
    E_away = E[away].sum() * dV
    return total, E_away, total - E_away


def method_c(s0, n):
    """3D midpoint quadrature of the analytic smooth part E_ac (cell centres never lie on x=0 or y=0);
    validates the 4 s ds reduction used in method A."""
    L = s0 + 5.0
    edges = np.linspace(-L, L, n + 1)
    xc = 0.5 * (edges[1:] + edges[:-1])
    zedges = np.linspace(-6, 6, n + 1)
    zc = 0.5 * (zedges[1:] + zedges[:-1])
    X, Y, Z = np.meshgrid(xc, xc, zc, indexing="ij")
    g, gz, gs, gzz, gss, gzs = derivs(Z, np.abs(X) + np.abs(Y), s0)
    e_ac = (gss * gzz - gzs**2) / (4 * PI)
    return e_ac.sum() * (edges[1] - edges[0]) ** 2 * (zedges[1] - zedges[0])


if __name__ == "__main__":
    print("Geometric units, arbitrary length unit L; energies in L (G = c = 1).")
    for s0 in (0.0, 0.8, 1.5):
        E_ac, E_sh, E_line, pos, neg = method_a(s0)
        print(f"\n[s0 = {s0}] N_x, N_y jump on x=0, y=0 wherever g_s != 0; line term {'absent (g_s(z,0)=0)' if s0 == 0 else 'present (g_s(z,0)!=0)'}")
        for n in (120, 200):
            print(f"  Method C (3D midpoint, analytic E_ac, n={n}): E_ac = {method_c(s0, n):+.6e}")
        print(f"  Method A: E_ac (smooth part) = {E_ac:+.6e}  [pos part {pos:+.4e}, neg part {neg:+.4e}]")
        print(f"            E_sheets = {E_sh:+.6e}, E_line = {E_line:+.6e}, sheets+line = {E_sh + E_line:+.6e}")
        print(f"            TOTAL = {E_ac + E_sh + E_line:+.3e}   (identity predicts 0)")
        for n in (121, 181):
            tot, away, near = method_b(s0, n)
            print(f"  Method B (3D FD, n={n}): total {tot:+.5e}; off-plane part {away:+.5e}; on-plane cells {near:+.5e}")
