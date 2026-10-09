"""Idealizer lens: linearized thick-wall 'warp shell' - the momentum currents a physical
interior shift needs, the NEC cap on the shift, the Sagnac (gravitomagnetic-flux) observable,
and the light-time comparison (shift 'advance' vs Shapiro delay).

Geometric units G = c = 1, lengths in metres; SI conversions printed where stated.
Model (all idealizations stated):
  * weak field: metric = Minkowski + h, linear in M and in beta, cross terms M*beta dropped;
  * static spherical shell, R1 < r < R2, mass M, density rho(r) (uniform unless stated);
  * covariant shift g_0z = w = beta * S(r), S = 1 for r < R1, 0 for r > R2 (Fuchs-type);
  * T_0i = (1/16 pi) [curl curl w]_i (checked with gr_tensors: lens-idealizer_jcheck.py);
  * stresses p << rho (Newtonian shell); NEC tested in the type-I-block form
       T_kk = rho - 2|T_0i n^i| + p_nn >= 0  for null k = (1, n),  minimized over n:
       requires |T_0i| <= (rho + p)/2.  p = 0 is used (stated variants with p = 0.1 rho).
"""
import math
import numpy as np

G = 6.67430e-11; C = 299792458.0
MJ = 1.898e27

def profiles():
    """S(s) on s in [0,1] (s = (r-R1)/(R2-R1)): returns dict name -> (S, S', S'') in s."""
    out = {}
    out["cubic smoothstep"] = (lambda s: 1 - (3*s**2 - 2*s**3),
                               lambda s: -(6*s - 6*s**2),
                               lambda s: -(6 - 12*s))
    out["quintic smoothstep"] = (lambda s: 1 - (10*s**3 - 15*s**4 + 6*s**5),
                                 lambda s: -(30*s**2 - 60*s**3 + 30*s**4),
                                 lambda s: -(60*s - 180*s**2 + 120*s**3))
    # Fuchs et al. eq. (28) sigmoid (Rb = 0), in s: f = 1/(exp(1/(s-1) + 1/s) + 1), S = 1 - f
    def fs(s):
        a = 1.0/(s - 1.0) + 1.0/s
        return 1.0/(np.exp(np.clip(a, -700, 700)) + 1.0)
    def num_d(fun, s, k):
        hh = 1e-5
        if k == 1:
            return (fun(s + hh) - fun(s - hh))/(2*hh)
        return (fun(s + hh) - 2*fun(s) + fun(s - hh))/hh**2
    out["Fuchs sigmoid"] = (lambda s: 1 - fs(s),
                            lambda s: -num_d(fs, s, 1),
                            lambda s: -num_d(fs, s, 2))
    return out

def jfield(Sd, Sdd, r, ca, R1, R2):
    """T_0i/beta components for w = beta*S(r) zhat; ca = cos(alpha), alpha from z axis.
    Returns (j_z, j_perp) per unit beta, geometric units [1/m^2]."""
    D = R2 - R1
    fp = Sd/D; fpp = Sdd/D**2
    sa2 = 1 - ca**2
    jz = (-fpp*sa2 - fp*(1 + ca**2)/r)/(16*math.pi)
    jp = (ca*np.sqrt(sa2)*(fpp - fp/r))/(16*math.pi)
    return jz, jp

def analyse(M_geo, R1, R2, name, prof, nr=1500, na=721, p_frac=0.0, verbose=True):
    S, Sd, Sdd = prof
    s = np.linspace(1e-4, 1 - 1e-4, nr)
    r = R1 + s*(R2 - R1)
    ca = np.linspace(-1, 1, na)
    RR, CA = np.meshgrid(r, ca, indexing="ij")
    SS = np.repeat(s[:, None], na, axis=1)
    jz, jp = jfield(Sd(SS), Sdd(SS), RR, CA, R1, R2)
    jmag = np.sqrt(jz**2 + jp**2)
    rho0 = 3*M_geo/(4*math.pi*(R2**3 - R1**3))
    # (i) uniform density: beta_max = (rho+p)/(2 max|j|)
    b_unif = rho0*(1 + p_frac)/(2*jmag.max())
    # (ii) best-shaped density rho = 2|j|/beta pointwise (mass budget): beta = M / int 2|j| dV
    dV = 2*math.pi*RR**2  # d(cos a) dr factor: dV = 2 pi r^2 dr dcos
    integ = np.trapezoid(np.trapezoid(2*jmag*dV, ca, axis=1), r)
    b_shaped = M_geo*(1 + p_frac)/integ
    # Sagnac / gravitomagnetic flux along the z axis: oint w dz (linear, N = 1)
    zline = np.linspace(R1, R2, 20001)
    Sint = 2*(R1 + np.trapezoid(S((zline - R1)/(R2 - R1)), zline))   # int_{-inf}^{inf} S(|z|) dz [m]
    if verbose:
        print(f"  [{name}] R1={R1} m R2={R2} m M={M_geo:.4g} m (2M/R2={2*M_geo/R2:.3f}), p/rho={p_frac}:")
        print(f"     max|T_0i|/beta = {jmag.max():.4e} 1/m^2, rho0 = {rho0:.4e} 1/m^2")
        print(f"     beta_max (uniform rho, NEC) = {b_unif:.4e};  beta_max (best-shaped rho) = {b_shaped:.4e}")
        print(f"     int S(|z|) dz along axis = {Sint:.3f} m")
    return b_unif, b_shaped, Sint

profs = profiles()
Mfu = G*4.49e27/C**2      # Fuchs et al. mass in metres [D-21]
print(f"Fuchs et al. parameters [D-21]: M = 4.49e27 kg -> {Mfu:.4f} m (geometric); R1 = 10 m, R2 = 20 m")
print()
print("=== 1. NEC cap on the shift at the 2024 shell's parameters (linear theory) ===")
res = {}
for name, pr in profs.items():
    res[name] = analyse(Mfu, 10.0, 20.0, name, pr)
print("  with p = 0.1 rho (Fuchs-scale stresses), cubic:")
analyse(Mfu, 10.0, 20.0, "cubic smoothstep", profs["cubic smoothstep"], p_frac=0.1)

print()
print("=== 2. Convergence (Fuchs sigmoid, grid doubling) ===")
for nr, na in [(750, 361), (1500, 721), (3000, 1441)]:
    b1, b2, _ = analyse(Mfu, 10.0, 20.0, "Fuchs sigmoid", profs["Fuchs sigmoid"], nr=nr, na=na, verbose=False)
    print(f"  nr={nr} na={na}: beta_max uniform = {b1:.6e}, shaped = {b2:.6e}")

print()
print("=== 3. Scaling law: beta_max vs compactness and wall fraction (cubic profile) ===")
print("  2M/R2   R1    R2   D/R2   beta_unif   beta_shaped   beta_unif/[(2M/R2)(D/R2)]   beta_shaped/[(2M/R2)(D/R2)]")
for comp in [0.05, 0.333]:
    for R1, R2 in [(10, 11), (10, 12), (10, 15), (10, 20), (10, 40), (10, 100), (100, 200)]:
        Mg = comp*R2/2
        b1, b2, _ = analyse(Mg, float(R1), float(R2), "cubic", profs["cubic smoothstep"], verbose=False)
        D = (R2 - R1)/R2
        print(f"  {comp:5.3f} {R1:5d} {R2:5d} {D:6.3f}  {b1:.4e}   {b2:.4e}     {b1/(comp*D):.4f}                  {b2/(comp*D):.4f}")

print()
print("=== 4. Sagnac observable vs Fuchs et al. Table 1 (7.6 ns at v_warp = 0.04) [D-25] ===")
for name in profs:
    Sint = res[name][2]
    dt = 2*0.04*Sint/C
    print(f"  {name}: round-trip difference 2*beta*int S dz / c at beta=0.04 = {dt*1e9:.2f} ns "
          f"(one-way {dt*0.5e9:.2f} ns); linear, N = 1 (a lapse N<1 inside raises it by ~1/N^2)")

print()
print("=== 5. Light-time along the z axis: shift 'advance' vs Shapiro delay (linear, harmonic) ===")
# Newtonian potential of the uniform shell on the axis; delay density -2*Phi; advance density w = beta*S
def Phi_shell(r, M, R1, R2):
    rho = 3*M/(4*math.pi*(R2**3 - R1**3))
    r = np.abs(r)
    out = np.empty_like(r)
    a = r <= R1; b = (r > R1) & (r < R2); c = r >= R2
    out[a] = -2*math.pi*rho*(R2**2 - R1**2)
    m_in = 4*math.pi*rho*(r[b]**3 - R1**3)/3
    out[b] = -m_in/r[b] - 2*math.pi*rho*(R2**2 - r[b]**2)
    out[c] = -M/r[c]
    return out
for name in ["cubic smoothstep", "Fuchs sigmoid"]:
    S = profs[name][0]
    for L in [20.0, 100.0, 1e4]:
        z = np.linspace(-L, L, 400001)
        delay = np.trapezoid(-2*Phi_shell(z, Mfu, 10.0, 20.0), z)
        Sz = np.where(np.abs(z) < 10, 1.0, np.where(np.abs(z) > 20, 0.0, S(np.clip((np.abs(z) - 10)/10, 1e-9, 1 - 1e-9))))
        adv1 = np.trapezoid(Sz, z)
        bnec = res[name][0]; bshp = res[name][1]
        print(f"  [{name}] baseline +-{L:g} m: Shapiro delay = {delay:.3f} m ({delay/C*1e9:.2f} ns); "
              f"advance per unit beta = {adv1:.3f} m")
        print(f"     beta needed for net advance = {delay/adv1:.4f};  NEC cap (uniform rho) = {bnec:.4e} "
              f"-> advance/delay at cap = {bnec*adv1/delay:.4f};  shaped cap {bshp:.4e} -> {bshp*adv1/delay:.4f}")
print("  Note: in linear harmonic gauge the delay density (1/2) h_kk = 2 int T_kk/|x-x'| d^3x' is")
print("  pointwise >= 0 whenever the NEC holds (Visser-Bassett-Liberati), so no segment can show a net advance.")

print()
print("=== 6. Reference-case scaling of the shell (ours): fixed 2M/R2 = 0.333, R2 = 2 R1 ===")
for R1 in [10.0, 100.0]:
    R2 = 2*R1; Mg = 0.333*R2/2
    b1, b2, _ = analyse(Mg, R1, R2, "cubic", profs["cubic smoothstep"], verbose=False)
    Mkg = Mg*C**2/G
    print(f"  R1 = {R1:g} m: M = {Mkg:.3e} kg = {Mkg/MJ:.3f} M_J; beta_max uniform = {b1:.4e}, shaped = {b2:.4e} "
          "(scale-free at fixed compactness and R2/R1)")
