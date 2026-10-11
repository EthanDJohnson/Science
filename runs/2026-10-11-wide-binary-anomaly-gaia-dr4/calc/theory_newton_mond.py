"""Theory-facet checks for the wide-binary run (numpy only, SI unless stated).

A. Kepler identities: <r>/a = 1 + e^2/2 (time average), v~ <= sqrt(2), <sin theta> = pi/4.
B. Newtonian v~ = v_p / sqrt(G M / s) distribution vs eccentricity distribution
   (random mean anomaly, isotropic orientation, selection in a narrow projected-separation bin
   for a population dN/da ~ a^-1.6). Equivalent spurious gamma = (median v~ / median v~_thermal)^2.
C. MOND: EFE-dominated asymptote eta = nu_ext (1 + K0/3) (Banik & Zhao 2018 eq 16) checked against
   their Table 3 (simple: nu_ext 1.5602, eta 1.4228; standard: 1.1462, 1.0726), and the Chae & Milgrom
   (2022) circular-orbit AQUAL fit used by Chae 2024 (eq 22) gamma_g(g_N), g_N <-> s mapping.
D. Inner-binary velocity perturbation relative to the wide-orbit velocity, and an estimate of the
   median-v~ shift from a triple fraction (crude: instantaneous inner velocity, no Gaia averaging).
"""
import numpy as np

rng = np.random.default_rng(12345)
G = 6.674e-11
MSUN = 1.989e30
AU = 1.496e11
A0 = 1.2e-10  # m/s^2


def solve_kepler(M, e):
    E = M + e * np.sin(M)
    for _ in range(60):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E


def sample_ecc(kind, n):
    if kind == "circular":
        return np.zeros(n)
    if isinstance(kind, float):
        return np.full(n, kind)
    alpha = {"uniform": 0.0, "thermal": 1.0, "alpha1.3": 1.3, "alpha2": 2.0, "alpha4": 4.0}[kind]
    return rng.random(n) ** (1.0 / (alpha + 1.0))


def vtilde_sample(kind, n, sbin=True):
    """Return (vtilde, weight). Units: GM=1, a drawn log-uniform over a in [0.05,20]*s0 (s0=1)."""
    e = sample_ecc(kind, n)
    lna = rng.uniform(np.log(0.05), np.log(20.0), n)
    a = np.exp(lna)
    M = rng.uniform(0, 2 * np.pi, n)
    E = solve_kepler(M, e)
    r = a * (1 - e * np.cos(E))
    # position/velocity in orbital plane (GM=1)
    x = a * (np.cos(E) - e)
    y = a * np.sqrt(1 - e**2) * np.sin(E)
    n_mean = a ** -1.5
    Edot = n_mean / (1 - e * np.cos(E))
    vx = -a * np.sin(E) * Edot
    vy = a * np.sqrt(1 - e**2) * np.cos(E) * Edot
    # isotropic orientation: random rotation, line of sight = z
    cosi = rng.uniform(-1, 1, n)
    Om = rng.uniform(0, 2 * np.pi, n)
    om = rng.uniform(0, 2 * np.pi, n)
    def rot(px, py):
        c, s = np.cos(om), np.sin(om)
        X1 = c * px - s * py
        Y1 = s * px + c * py
        sini = np.sqrt(1 - cosi**2)
        X = np.cos(Om) * X1 - np.sin(Om) * cosi * Y1
        Y = np.sin(Om) * X1 + np.cos(Om) * cosi * Y1
        Z = sini * Y1
        return X, Y, Z
    X, Y, _ = rot(x, y)
    VX, VY, _ = rot(vx, vy)
    s = np.hypot(X, Y)
    vp = np.hypot(VX, VY)
    vt = vp / np.sqrt(1.0 / s)  # v_c(s) = sqrt(GM/s)
    w = a ** -0.6  # dN/dlna ~ a^-0.6  <=> dN/da ~ a^-1.6
    if sbin:
        m = (s > 0.9) & (s < 1.1)
        return vt[m], w[m], r[m], a[m]
    return vt, w, r, a


def wmedian(x, w):
    i = np.argsort(x)
    cw = np.cumsum(w[i])
    return x[i][np.searchsorted(cw, 0.5 * cw[-1])]


def part_A():
    print("=== A. Kepler identities ===")
    for e in (0.0, 0.3, 0.7, 0.95):
        Mm = rng.uniform(0, 2 * np.pi, 400000)
        E = solve_kepler(Mm, e)
        print(f"e={e}: <r>/a numeric={np.mean(1 - e*np.cos(E)):.4f}  analytic 1+e^2/2={1+e*e/2:.4f}")
    th = np.arccos(rng.uniform(-1, 1, 1000000))
    print(f"<sin theta> isotropic = {np.mean(np.sin(th)):.4f} (pi/4 = {np.pi/4:.4f})")
    for kind in ("circular", "thermal", "alpha4", 0.99):
        vt, w, r, a = vtilde_sample(kind, 1500000, sbin=False)
        print(f"max v~ ({kind}) = {vt.max():.4f}  (bound: sqrt2 = {np.sqrt(2):.4f})")


def part_B():
    print("\n=== B. Newtonian median v~ and spurious gamma from eccentricity mismatch (s-bin selected) ===")
    res = {}
    for kind in ("circular", 0.5, "uniform", "thermal", "alpha1.3", "alpha2", "alpha4"):
        vt, w, r, a = vtilde_sample(kind, 6000000)
        med = wmedian(vt, w)
        q16, q84 = wmedian(vt, w), None
        frac_gt1 = np.sum(w[vt > 1]) / np.sum(w)
        res[str(kind)] = med
        print(f"f(e)={kind!s:9s} N_sel={len(vt):7d} median v~={med:.4f}  frac(v~>1)={frac_gt1:.3f}  mean(r/s)={np.sum(w*r)/np.sum(w):.3f}")
    ref = res["thermal"]
    for k, m in res.items():
        print(f"  equivalent gamma if a thermal template is used for truth f(e)={k}: (med/med_thermal)^2 = {(m/ref)**2:.3f}")
    ref2 = res["alpha1.3"]
    for k, m in res.items():
        print(f"  equivalent gamma if an alpha=1.3 template is used for truth f(e)={k}: {(m/ref2)**2:.3f}")


def nu_simple(y):
    return 0.5 + np.sqrt(0.25 + 1.0 / y)


def nu_standard(y):
    return np.sqrt(0.5 + np.sqrt(0.25 + 1.0 / y**2))  # mu(x)=x/sqrt(1+x^2)


def mu_x_simple(x):
    return x * x / (1 + x)


def mu_x_standard(x):
    return x * x / np.sqrt(1 + x * x)


def part_C():
    print("\n=== C. MOND EFE-dominated limit (Banik & Zhao 2018 eq 16) and Chae-Milgrom fit ===")
    for name, nu, mux in (("simple", nu_simple, mu_x_simple), ("standard", nu_standard, mu_x_standard)):
        # find x=g_ext/a0 giving nu_ext of Table 3
        target = {"simple": 1.5602, "standard": 1.1462}[name]
        lo, hi = 0.05, 50.0
        for _ in range(200):
            mid = np.sqrt(lo * hi)
            y = mux(mid)
            if nu(y) > target:
                lo = mid  # larger x => smaller nu
            else:
                hi = mid
        x = np.sqrt(lo * hi)
        y = mux(x)
        h = 1e-5
        K0 = (np.log(nu(y * (1 + h))) - np.log(nu(y * (1 - h)))) / (np.log(1 + h) - np.log(1 - h))
        eta = nu(y) * (1 + K0 / 3)
        print(f"{name}: x=g_ext/a0={x:.3f} (g_ext={x*A0:.3e} m/s^2 for a0=1.2e-10) y_ext={y:.4f} nu_ext={nu(y):.4f} K0={K0:.4f} eta={eta:.4f}; max boost nu_ext(1+K0/2)={nu(y)*(1+K0/2):.4f}; min nu_ext={nu(y):.4f}")
    print("  Table 3 (BZ18): simple nu_ext 1.5602, eta_QUMOND 1.4228; standard nu_ext 1.1462, eta 1.0726  -> compare above")
    # Chae & Milgrom 2022 fit used by Chae 2024 eq 22
    print("\nChae 2024 eq 22 gamma_g(g_N) = g/g_N, simple nu, beta=1.1, gamma_exp=1.2:")
    def nuhat(y):
        h = 1e-6
        return (np.log(nu_simple(y * (1 + h))) - np.log(nu_simple(y * (1 - h)))) / (np.log(1 + h) - np.log(1 - h))
    def gam_g(gN, gext_over_a0=1.90, beta=1.1, gexp=1.2):
        x = gext_over_a0
        gNext = x * x / (1 + x) * A0
        yb = np.sqrt((gN / A0) ** 2 + (beta * gNext / A0) ** 2)
        return nu_simple(yb) * (1 + (np.tanh(beta * gNext / gN)) ** gexp * nuhat(yb) / 3.0)
    for lg in (-8.0, -9.0, -9.5, -10.0, -10.15, -10.5, -11.0):
        gN = 10 ** lg
        row = [gam_g(gN, 1.90), gam_g(gN, 1.71), gam_g(gN, 2.09)]
        print(f"  log10 g_N={lg:6.2f}: gamma_g={row[0]:.3f}  (g_ext/a0=1.90) | 1.71: {row[1]:.3f} | 2.09: {row[2]:.3f}")
    print("  (the tanh^gamma term vanishes at high g_N so gamma_g -> nu(y)->1)")
    # s <-> g_N mapping
    print("\ng_N -> r, s for total mass M (r=sqrt(GM/g_N); Chae maps s ~ r/1.2):")
    for M in (1.0, 1.5, 2.0):
        for lg in (-9.5, -10.0):
            r = np.sqrt(G * M * MSUN / 10 ** lg) / AU
            print(f"  M={M} Msun, log g_N={lg}: r={r:,.0f} au, s=r/1.2={r/1.2:,.0f} au; r_M=sqrt(GM/a0)={np.sqrt(G*M*MSUN/A0)/AU:,.0f} au")


def part_D():
    print("\n=== D. Inner-binary velocity perturbation ===")
    Mwide = 1.5  # Msun total wide mass
    for s_au in (3000.0, 10000.0):
        vc = 29.78 * np.sqrt(Mwide / s_au)  # km/s, 29.78 km/s = sqrt(GMsun/1au)
        print(f"wide pair M={Mwide} Msun, s={s_au:.0f} au: v_c(s)={vc:.3f} km/s")
        for a_in in (1.0, 3.0, 10.0, 30.0, 100.0, 300.0):
            mB, q = 0.8, 0.5
            m1 = mB / (1 + q)
            m2 = q * m1
            vrel = 29.78 * np.sqrt(mB / a_in)
            vA = vrel * m2 / mB  # reflex speed of primary about inner CoM
            P = np.sqrt(a_in**3 / mB)  # yr
            fpc = abs(q / (1 + q) - q**4 / (1 + q**4))  # luminosity ratio ~ q^4 (illustrative)
            print(f"   a_in={a_in:6.0f} au P={P:8.2f} yr: reflex v_A={vA:7.3f} km/s = {vA/vc:6.2f} v_c(s); photocentre factor {fpc:.2f} -> {fpc*vrel/vc:6.2f} v_c(s)")
    # crude MC: triple fraction -> median v~ shift (instantaneous inner velocity, thermal wide, Opik inner a in [3,300] au)
    print("\nCrude MC: median v~ vs triple fraction (thermal wide orbits; inner Opik a_in in 3-300 au;")
    print("  photocentre factor 0.3 x v_rel, random 2D direction/phase; NO Gaia averaging, so an upper bound):")
    vt, w, r, a = vtilde_sample("thermal", 4000000)
    n = len(vt)
    # need vector v~; approximate extra by adding in quadrature with random angle in plane: vp_new^2 = vp^2 + dv^2 + 2 vp dv cos(phi)
    s_au = 5000.0
    Mw = 1.5
    vc = 29.78 * np.sqrt(Mw / s_au)
    base_med = wmedian(vt, w)
    for ftrip in (0.0, 0.1, 0.2, 0.3):
        is_t = rng.random(n) < ftrip
        a_in = np.exp(rng.uniform(np.log(3.0), np.log(300.0), n))
        vrel = 29.78 * np.sqrt(0.8 / a_in) * rng.uniform(0.5, 1.0, n)  # orbital phase factor
        dv = 0.3 * vrel / vc
        phi = rng.uniform(0, 2 * np.pi, n)
        v2 = vt**2 + np.where(is_t, dv**2 + 2 * vt * dv * np.cos(phi), 0.0)
        vnew = np.sqrt(np.maximum(v2, 0))
        med = wmedian(vnew, w)
        print(f"  f_triple={ftrip:.1f}: median v~={med:.4f}; (med/med0)^2 = {(med/base_med)**2:.3f}; frac(v~>1.5)={np.sum(w[vnew>1.5])/np.sum(w):.3f}; frac(v~>sqrt2)={np.sum(w[vnew>np.sqrt(2)])/np.sum(w):.3f}")


if __name__ == "__main__":
    part_A()
    part_B()
    part_C()
    part_D()
