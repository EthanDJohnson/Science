"""Dialectician lens: kinematics of the Fuchs et al. 2024 warp shell (synthesis S1).

Model (ours, labelled approximations):
  * Static TOV shell, constant density between R1 and R2, P(R2)=0, integrated inward,
    to get the lapse alpha_in in the flat cavity (Schwarzschild-like coordinates, gamma_ij = delta_ij
    in the cavity because m(r)=0 there). A pressure-free lapse integral is a second estimate.
  * Interior warp: constant shift b = beta_warp = 0.02 (Fuchs p. 17) in the cavity, metric
    ds^2 = -alpha^2 dt^2 + (dx + b dt)^2  (flat; t = asymptotic Killing time).
  * Linearized momentum density of the wall from the momentum constraint with flat slices,
    beta_x = b*S(r):  8 pi j_x = (b/2) (d_y^2 + d_z^2) S  (unit lapse, linear in b; crude).
Geometric units G=c=1 (lengths in m) unless SI stated.
"""
import numpy as np
from scipy.integrate import solve_ivp, quad

G = 6.674e-11; c = 2.998e8
M_kg = 4.49e27; R1 = 10.0; R2 = 20.0
m = G * M_kg / c**2                      # m (geometric mass)
V = 4/3*np.pi*(R2**3 - R1**3)
rho = m / V                              # m^-2 (geometric density, mass/volume)
print(f"geometric mass m = GM/c^2 = {m:.4f} m; 2m/R2 = {2*m/R2:.4f}; 2m/R1 = {2*m/R1:.4f}")
print(f"mean geometric density rho = {rho:.4e} m^-2  (SI {rho*c**2/G:.3e} kg/m^3)")

# --- TOV inward integration (constant density shell) ---
def rhs(r, y):
    mm, P, lna = y
    if r < R1 or r > R2:
        dm = 0.0
    else:
        dm = 4*np.pi*r**2*rho
    rr = rho if R1 <= r <= R2 else 0.0
    fac = (mm + 4*np.pi*r**3*P) / (r*(r - 2*mm))
    return [dm, -(rr + P)*fac, fac]
y0 = [m, 0.0, 0.5*np.log(1 - 2*m/R2)]
sol = solve_ivp(rhs, [R2, R1], y0, rtol=1e-10, atol=1e-14)
m1, P1, lna1 = sol.y[:, -1]
alpha_TOV = np.exp(lna1)
# pressure-free estimate
def rhs0(r, y):
    mm, lna = y
    dm = 4*np.pi*r**2*rho
    return [dm, mm/(r*(r-2*mm))]
s0 = solve_ivp(rhs0, [R2, R1], [m, 0.5*np.log(1-2*m/R2)], rtol=1e-10)
alpha_P0 = np.exp(s0.y[1, -1])
print(f"residual mass at R1 (should be ~0): {m1:.3e} m")
print(f"TOV pressure left at R1 (Fuchs smooth this away): P(R1) = {P1:.3e} m^-2 = {P1/rho:.3f} rho")
print(f"cavity lapse alpha_in: TOV {alpha_TOV:.4f}; pressure-free {alpha_P0:.4f}; alpha(R2) = {np.sqrt(1-2*m/R2):.4f}")

b = 0.02
for name, a in [("TOV", alpha_TOV), ("P=0", alpha_P0)]:
    v_loc = b/a
    dil = 1 - np.sqrt(1 - (b/a)**2)
    L = 2*R1
    sag = 2*b*L/(a**2 - b**2)/c
    print(f"[{name}] u_i=0 passenger speed relative to static (Killing) observers v_loc = b/alpha = {v_loc:.4f} c")
    print(f"[{name}] extra clock deficit of a payload held at rest in the shell: 1 - sqrt(1-(b/alpha)^2) = {dil:.3e}"
          f"  (= {dil*3.156e7:.3e} s per year of its own time, approx)")
    print(f"[{name}] Sagnac-type co/counter light-time difference across cavity diameter {L} m: {sag*1e9:.2f} ns")
t_cross = 2*R1/(b*c)
print(f"u_i=0 passenger crosses cavity diameter 2R1 = {2*R1} m at coordinate speed b = {b} c in {t_cross*1e6:.2f} us (Killing time)")

# --- linearized momentum density of the wall, Fuchs sigmoid ---
def make_S(Rb):
    b1, b2 = R1 + Rb, R2 - Rb
    def S(r):
        r = np.asarray(r, float)
        out = np.where(r <= b1, 1.0, 0.0)
        mid = (r > b1) & (r < b2)
        rm = r[mid]
        arg = (b2 - b1)*(1/(rm - b2) + 1/(rm - b1))
        arg = np.clip(arg, -700, 700)
        out[mid] = 1 - 1/(np.exp(arg) + 1)
        return out
    return S, b1, b2

for Rb in [0.0, 1.0, 2.0]:
    S, b1, b2 = make_S(Rb)
    r = np.linspace(b1 + 1e-6, b2 - 1e-6, 40001)
    Sv = S(r); dr = r[1]-r[0]
    S1 = np.gradient(Sv, dr); S2 = np.gradient(S1, dr)
    mu = np.linspace(-1, 1, 401)            # cos(theta)
    Rg, MU = np.meshgrid(r, mu, indexing='ij')
    S1g = np.interp(Rg, r, S1); S2g = np.interp(Rg, r, S2)
    lap_perp = S2g*(1 - MU**2) + S1g*(1 + MU**2)/Rg      # (d_y^2+d_z^2) S
    jx = (b/2)*lap_perp/(8*np.pi)
    # net momentum: integral over volume, dV = 2 pi r^2 dr dmu
    Px = np.trapezoid(np.trapezoid(jx*2*np.pi*Rg**2, mu, axis=1), r)
    Pabs = np.trapezoid(np.trapezoid(np.abs(jx)*2*np.pi*Rg**2, mu, axis=1), r)
    jmax = np.abs(jx).max()
    bcap_DEC = b*rho/jmax          # |j| <= rho (DEC-type scale)
    bcap_NEC = b*rho/(2*jmax)      # 2|j| <= rho + p, with p ~ 0 (NEC-type scale)
    print(f"Rb={Rb} m: net P_x = {Px:.3e} m (geometric) vs total |P| = {Pabs:.3e} m -> ratio {Px/Pabs:.2e}")
    print(f"   max|j_x| = {jmax:.3e} m^-2 = {jmax/rho:.3f} rho at b={b};  crude caps b_max ~ {bcap_NEC:.3f} (NEC scale) to {bcap_DEC:.3f} (DEC scale)")

# scaling check: self-similar shell R1=100, R2=200, M x10
for k in [1, 10]:
    rho_k = (m*k)/(4/3*np.pi*((R2*k)**3 - (R1*k)**3))
    print(f"scale x{k}: rho*Delta^2 = {rho_k*(R2*k-R1*k)**2:.4e} (dimensionless; b_cap scales with this at fixed shape)")
