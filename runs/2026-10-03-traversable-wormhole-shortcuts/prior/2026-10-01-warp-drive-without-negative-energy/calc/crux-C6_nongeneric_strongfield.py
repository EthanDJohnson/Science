"""Crux C6, branch (c): does a non-generic fastest path in a STRONG-FIELD,
NEC-satisfying, asymptotically flat spacetime give an advance over exterior light?

Model (geometric units G = c = 1, lengths in m): static, spherically symmetric,
  ds^2 = -f dt^2 + dr^2/f + r^2 dOmega^2,  f = 1 - 2 m(r)/r,
which forces p_r = -rho (so T_ab k^a k^b = 0 for radial null k), and
  p_perp = -rho - r rho'/2.
Density: de Sitter core rho0 for r < R1, C^1 smoothstep fall to 0 at R2, vacuum
(Schwarzschild) outside.  NEC: rho + p_r = 0 >= 0, rho + p_perp = -r rho'/2 >= 0
(rho' <= 0).  WEC: rho >= 0.  DEC: |p_perp| <= rho checked numerically.
The radial ray through the centre has R_ab k^a k^b = 0 everywhere and k is a
principal null direction of the (type D / conformally flat) Weyl tensor, so it
FAILS Olum's generic condition along its whole length: branch (c) exactly.

Test: static emitter A at (r = D, phi = pi) and receiver B at (r = D, phi = 0).
Find every null geodesic A -> B (radial b = 0, plus any b with swept angle = pi),
and compare coordinate (= asymptotic static-clock) arrival times.  If the
non-generic radial ray arrives before every exterior (lensed-ring) ray, branch (c)
yields a one-way advance over exterior light with the NEC holding; otherwise not.
"""
import mpmath as mp

mp.mp.dps = 20
R1, R2 = mp.mpf(10), mp.mpf(20)


def smooth(x):  # 1 at x<=0 -> 0 at x>=1, C^1
    if x <= 0:
        return mp.mpf(1)
    if x >= 1:
        return mp.mpf(0)
    return 1 - (3 * x**2 - 2 * x**3)


def make_model(C):
    """C = 2M/R2 (compactness at outer edge)."""
    # m(r) = 4 pi rho0 * I(r), I(r) = int_0^r S s^2 ds ; exact polynomial integrals via quad
    I_R2 = mp.quad(lambda s: smooth((s - R1) / (R2 - R1)) * s**2, [0, R1, R2])
    M = C * R2 / 2
    rho0 = M / (4 * mp.pi * I_R2)
    cache = {}

    def m(r):
        if r >= R2:
            return M
        if r <= R1:
            return 4 * mp.pi * rho0 * r**3 / 3
        key = r
        if key not in cache:
            cache[key] = 4 * mp.pi * rho0 * (R1**3 / 3 + mp.quad(
                lambda s: smooth((s - R1) / (R2 - R1)) * s**2, [R1, r]))
        return cache[key]

    def f(r):
        return 1 - 2 * m(r) / r if r > 0 else mp.mpf(1)

    def rho(r):
        return rho0 * smooth((r - R1) / (R2 - R1))

    return M, rho0, m, f, rho


def ec_check(rho0, rho, f):
    worst_nec_perp, worst_dec, fmin = mp.inf, mp.inf, mp.inf
    for i in range(1, 400):
        r = R2 * 1.2 * i / 400
        h = mp.mpf("1e-6")
        drho = (rho(r + h) - rho(r - h)) / (2 * h)
        p_perp = -rho(r) - r * drho / 2
        worst_nec_perp = min(worst_nec_perp, rho(r) + p_perp)
        worst_dec = min(worst_dec, rho(r) - abs(p_perp))
        fmin = min(fmin, f(r))
    return worst_nec_perp, worst_dec, fmin


def turning_point(b, f, D):
    # largest root of r^2 - f(r) b^2 = 0 below D
    g = lambda r: r**2 - f(r) * b**2
    lo, hi = mp.mpf("1e-12"), D
    # scan downward from D for sign change
    n = 800
    prev_r, prev_g = hi, g(hi)
    for k in range(1, n + 1):
        r = hi * (1 - mp.mpf(k) / n)
        if r <= 0:
            break
        gr = g(r)
        if gr <= 0 < prev_g:
            return mp.findroot(g, (r, prev_r), solver="bisect")
        prev_r, prev_g = r, gr
    return None


def sweep_and_time(b, f, D, M):
    r0 = turning_point(b, f, D)
    if r0 is None:
        return None
    # make sure the start point is on the allowed side (r^2 - f b^2 >= 0)
    while r0**2 - f(r0) * b**2 < 0:
        r0 = r0 * (1 + mp.mpf("1e-17"))
    fixed = [p for p in (R1, R2, 3 * R2, 30 * R2, 300 * R2) if r0 < p < D]
    geo = [r0 + (D - r0) * mp.mpf(10) ** (-k) for k in range(1, 12)]
    pts = sorted(set([r0] + fixed + geo + [D]))
    # substitution r = r0 + u^2 removes the 1/sqrt endpoint singularity
    def phi_int(u):
        r = r0 + u**2
        return 2 * u * (b / r**2) / mp.sqrt(max(mp.mpf("1e-40"), 1 - f(r) * b**2 / r**2))

    def t_int(u):
        r = r0 + u**2
        return 2 * u * (1 / f(r)) / mp.sqrt(max(mp.mpf("1e-40"), 1 - f(r) * b**2 / r**2))

    us = [mp.sqrt(p - r0) for p in pts]
    dphi = 2 * mp.quad(phi_int, us)
    T = 2 * mp.quad(t_int, us)
    return dphi, T


def radial_time(f, D):
    pts = [p for p in (mp.mpf(0), R1, R2, 3 * R2, 30 * R2, 300 * R2) if p < D] + [D]
    pts = sorted(set(pts + [D * mp.mpf(10) ** (-k) for k in range(1, 8)]))
    return 2 * mp.quad(lambda r: 1 / f(r), pts)


print("geometric units (G=c=1), lengths and times in m; 1 m of light time = 3.336 ns")
for C in (mp.mpf("0.1"), mp.mpf("0.3"), mp.mpf("0.5"), mp.mpf("0.7")):
    M, rho0, m, f, rho = make_model(C)
    nec_perp, dec, fmin = ec_check(rho0, rho, f)
    print(f"\n=== compactness 2M/R2 = {float(C):.2f}: M = {float(M):.3f} m, rho0 = {float(rho0):.3e} m^-2, "
          f"min f = {float(fmin):.4f} (no horizon if > 0)")
    print(f"  NEC radial: rho + p_r = 0 exactly; NEC transverse min(rho+p_perp) = {float(nec_perp):.3e} m^-2 "
          f"(>= 0 pass); DEC min(rho-|p_perp|) = {float(dec):.3e} m^-2")
    for D in (mp.mpf(1e3), mp.mpf(1e4), mp.mpf(1e5)):
        Trad = radial_time(f, D)
        # scan b for swept angle = pi
        bs = [mp.mpf(x) for x in ([0.5, 1, 2, 4, 6, 8, 12, 16, 20, 25, 30, 40, 60, 80, 120, 160, 240,
                                  320, 480, 640, 960, 1280, 1920, 2560])]
        bs = [b for b in bs if b < D / 4]
        vals = []
        for b in bs:
            res = sweep_and_time(b, f, D, M)
            if res is not None:
                vals.append((b, res[0] - mp.pi))
        roots = []
        for (b1, g1), (b2, g2) in zip(vals, vals[1:]):
            if g1 * g2 < 0:
                lo, hi, glo = b1, b2, g1
                for _ in range(45):  # plain bisection on swept angle - pi
                    mid = (lo + hi) / 2
                    gm = sweep_and_time(mid, f, D, M)[0] - mp.pi
                    if gm * glo > 0:
                        lo, glo = mid, gm
                    else:
                        hi = mid
                roots.append((lo + hi) / 2)
        print(f"  D = {float(D):.0e} m: radial (non-generic) T - 2D = {float(Trad - 2*D):+.4f} m")
        for bb in roots:
            dphi, T = sweep_and_time(bb, f, D, M)
            where = "exterior vacuum ray" if turning_point(bb, f, D) > R2 else "ray through matter"
            print(f"     lensed ray b = {float(bb):.3f} m ({where}), r_min = {float(turning_point(bb, f, D)):.3f} m: "
                  f"T - 2D = {float(T - 2*D):+.4f} m;  radial minus this = {float(Trad - T):+.4f} m "
                  f"-> {'RADIAL ADVANCED' if Trad < T else 'radial delayed (no advance)'}")
        if not roots:
            print("     no lensed ray found in scan")

# self-checks
flat = lambda r: mp.mpf(1)
Tflat = radial_time(flat, mp.mpf(1e4))
print(("PASS" if abs(Tflat - 2e4) < 1e-12 else "FAIL") + f": flat-space radial time = {float(Tflat)} m (expect 20000)")
res = sweep_and_time(mp.mpf(100), flat, mp.mpf(1e4), 0)
exp_phi = mp.pi - 2*mp.asin(mp.mpf(100)/1e4); exp_T = 2*mp.sqrt(mp.mpf(1e8) - 1e4)
print(("PASS" if abs(res[0]-exp_phi) < 1e-8 and abs(res[1]-exp_T) < 1e-6 else "FAIL") + f": flat-space b=100 m sweep {float(res[0]):.10f} (expect {float(exp_phi):.10f}), T {float(res[1]):.6f} m (expect {float(exp_T):.6f})")
