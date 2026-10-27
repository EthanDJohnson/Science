"""Pointwise (local) QI scan of Van Den Broeck's region II, to test Krasnikov's (2003, gr-qc/0207057,
footnote 8) remark that VdB's profile 'violates the quantum inequality (e.g. in w = 0.98)'.

VdB applied the QI only at the density peak with tau0 = 0.1 * (GLOBAL minimum curvature radius).
The flat-space QI (Ford-Roman, massless scalar) applies for any tau0 small compared with the LOCAL
curvature radius, so at each w we use tau0 = beta * r_c(w), r_c(w) = 1/sqrt(max_k |R_k(w)|), where
R_k are the orthonormal Riemann components derived (and checked against eqs 11, 19) in
vdb_qi_recompute.py Step A:
  T00   = (B'^2/B^4 - 2B''/B^3 - 4B'/(rB^3))/(8 pi)
  R_rtrt = B'^2/B^4 - B''/B^3 - B'/(rB^3)      R_tptp = -B'(rB' + 2B)/(r B^4)
Observers are static (region II is ultrastatic after x' = x - v t), so the Lorentzian time
average of T00 equals T00. We also report the proper radial distance over which r_c changes,
to check tau0 is small compared with it (so the local-flatness assumption is not abused).
"""
import mpmath as mp
mp.mp.dps = 60
G_N = mp.mpf("6.67430e-11"); C = mp.mpf(299792458); HBAR = mp.mpf("1.054571817e-34")
LP2 = HBAR * G_N / C**3; LP = mp.sqrt(LP2); C2_G = C**2 / G_N
n = 80

def fields(w, a, D, Rt):
    g = -(n - 1) * w**n + n * w**(n - 1)
    gw = n * (n - 1) * w**(n - 2) * (1 - w)                    # dB/dw / alpha
    gww = n * (n - 1) * w**(n - 3) * ((n - 2) - (n - 1) * w)    # d2B/dw2 / alpha
    B = a * g + 1
    Bp = -a * gw / D                                            # d/dr = -(1/D) d/dw
    Bpp = a * gww / D**2
    r = Rt + D - w * D
    T00 = (Bp**2 / B**4 - 2 * Bpp / B**3 - 4 * Bp / (r * B**3)) / (8 * mp.pi)
    Rrt = Bp**2 / B**4 - Bpp / B**3 - Bp / (r * B**3)
    Rtp = -Bp * (r * Bp + 2 * B) / (r * B**4)
    return B, T00, max(abs(Rrt), abs(Rtp))

def scan(label, a, D, Rt, beta=mp.mpf("0.1")):
    a, D, Rt = mp.mpf(a), mp.mpf(D), mp.mpf(Rt)
    print(f"\n== {label}: alpha={mp.nstr(a,3)}, Dt={mp.nstr(D,3)} m ==")
    worst = None
    rows = []
    M = 2000
    for i in range(1, M):
        w = mp.mpf(i) / M
        B, T00, Rm = fields(w, a, D, Rt)
        if T00 >= 0:
            continue
        rc = 1 / mp.sqrt(Rm)
        bound = -3 * LP2 / (32 * mp.pi**2 * (beta * rc)**4)      # geometric units, m^-2
        ratio = T00 / bound                                     # >1 means violated
        rows.append((w, T00, rc, ratio, B))
        if worst is None or ratio > worst[3]:
            worst = (w, T00, rc, ratio, B)
    for wq in (mp.mpf("0.349"), mp.mpf("0.576"), mp.mpf("0.9"), mp.mpf("0.95"), mp.mpf("0.98")):
        B, T00, Rm = fields(wq, a, D, Rt)
        rc = 1 / mp.sqrt(Rm)
        bound = -3 * LP2 / (32 * mp.pi**2 * (beta * rc)**4)
        print(f" w={mp.nstr(wq,4)}: B={mp.nstr(B,4)}, T00={mp.nstr(T00*C2_G,4)} kg/m^3, local r_c={mp.nstr(rc,4)} m,"
              f" tau0={mp.nstr(beta*rc,3)} m, bound={mp.nstr(bound*C2_G,4)} kg/m^3, |T00|/|bound|={mp.nstr(T00/bound,4)}")
    w, T00, rc, ratio, B = worst
    # proper-distance scale on which r_c varies at the worst point: ds = B dr = B D dw
    h = mp.mpf("1e-6")
    rc_p = 1 / mp.sqrt(fields(w + h, a, D, Rt)[2]); rc_m = 1 / mp.sqrt(fields(w - h, a, D, Rt)[2])
    drc_ds = (rc_p - rc_m) / (2 * h) / (B * D)
    lvar = abs(rc / drc_ds)
    print(f" worst local violation at w={mp.nstr(w,4)}: T00={mp.nstr(T00*C2_G,4)} kg/m^3, r_c={mp.nstr(rc,4)} m,"
          f" |T00|/|bound| = {mp.nstr(ratio,4)}; r_c varies on proper scale {mp.nstr(lvar,3)} m vs tau0={mp.nstr(beta*rc,3)} m")
    nviol = sum(1 for row in rows if row[3] > 1)
    print(f" fraction of negative-T00 grid points violating local QI: {nviol}/{len(rows)}")
    # Planck-density comparison (Krasnikov eq. 7: negative |rho| must be >~ Planck density)
    rho_planck = C**5 / (HBAR * G_N**2)   # kg/m^3
    print(f" Planck density = {mp.nstr(rho_planck,4)} kg/m^3; peak |T00| here = "
          f"{mp.nstr(max(abs(row[1]) for row in rows)*C2_G,4)} kg/m^3")

scan("v1-v4 eq.7", "1e34", "1e-32", "1e-32")
scan("v5 / published eq.7", "1e17", "1e-15", "1e-15")
scan("Planck-variant smaller, Dt=1e-33", "1e35", "1e-33", "1e-33")


# ---- refined: sampling time limited by BOTH the local curvature radius and the proper distance
# over which the curvature radius changes (L_var), so the local-flatness assumption holds ----
def rc_of(w, a, D, Rt):
    return 1 / mp.sqrt(fields(w, a, D, Rt)[2])

def refined(label, a, D, Rt, beta=mp.mpf("0.1")):
    a, D, Rt = mp.mpf(a), mp.mpf(D), mp.mpf(Rt)
    print(f"\n== refined {label}: tau0 = {beta} * min(r_c, L_var) ==")
    h = mp.mpf("1e-7")
    M = 1000
    worst = None
    Eneg_tot = mp.mpf(0); Eneg_viol = mp.mpf(0)
    for i in range(1, M):
        w = mp.mpf(i) / M
        B, T00, Rm = fields(w, a, D, Rt)
        if T00 >= 0:
            continue
        rc = 1 / mp.sqrt(Rm)
        drc_ds = (rc_of(w + h, a, D, Rt) - rc_of(w - h, a, D, Rt)) / (2 * h) / (B * D)
        lvar = abs(rc / drc_ds) if drc_ds != 0 else mp.inf
        tau0 = beta * min(rc, lvar)
        bound = -3 * LP2 / (32 * mp.pi**2 * tau0**4)
        ratio = T00 / bound
        r = Rt + D - w * D
        dE = 4 * mp.pi * r**2 * B**3 * T00 * D / M        # crude Riemann sum of E_II,- (metres)
        Eneg_tot += dE
        if ratio > 1:
            Eneg_viol += dE
        if worst is None or ratio > worst[0]:
            worst = (ratio, w, T00, rc, lvar, tau0)
        if i in (349, 576, 700, 800, 900, 950, 980):
            print(f" w={mp.nstr(w,3)}: T00={mp.nstr(T00*C2_G,4)} kg/m^3, r_c={mp.nstr(rc,3)} m, L_var={mp.nstr(lvar,3)} m,"
                  f" tau0={mp.nstr(tau0,3)} m, |T00|/|bound|={mp.nstr(ratio,4)}")
    ratio, w, T00, rc, lvar, tau0 = worst
    print(f" worst: w={mp.nstr(w,4)}, T00={mp.nstr(T00*C2_G,4)} kg/m^3, r_c={mp.nstr(rc,3)} m, L_var={mp.nstr(lvar,3)} m,"
          f" tau0={mp.nstr(tau0,3)} m, violated by {mp.nstr(ratio,4)}")
    print(f" E_II,- (Riemann sum) = {mp.nstr(Eneg_tot*C2_G,4)} kg; share sitting where the local QI is violated:"
          f" {mp.nstr(Eneg_viol/Eneg_tot,6)}")

refined("v1-v4 eq.7", "1e34", "1e-32", "1e-32")
refined("v5 / published eq.7", "1e17", "1e-15", "1e-15")
