"""Falsifier C3-0: independent check of Van Den Broeck (VdB) region II energy, curvature and QI.
Region II metric (comoving): ds^2 = -dt^2 + B(r)^2 (dr^2 + r^2 dOmega^2), K_ij = 0, lapse 1.
B = 1 + alpha(-(n-1) w^n + n w^(n-1)), w = (Rt + Dt - r)/Dt   [VdB 1999 eqs 12-13].
Eulerian rho (geometric, 1/m^2) = (1/8pi)(B'^2/B^4 - 2B''/B^3 - 4B'/(B^3 r))   [VdB eq 11].
Orthonormal Riemann R_1212 = B'^2/B^4 - B''/B^3 - B'/(B^3 r)  [VdB eq 19]; other sectional curvature
K_23 (tangential plane) = -(2B'/(B^3 r)) - B'^2/B^4 ... computed here from conformal-flat Ricci, as a check.
Ford-Roman massless-scalar QI (geometric): rho >= -3 L_P^2 / (32 pi^2 tau0^4), tau0 = 0.1 r_c.
SI conversion: mass density kg/m^3 = rho[1/m^2] * c^2/G.
"""
import mpmath as mp

mp.mp.dps = 60
G, c, hbar = mp.mpf("6.6743e-11"), mp.mpf("2.99792458e8"), mp.mpf("1.054571817e-34")
LP = mp.sqrt(hbar * G / c**3)
KGM = c**2 / G  # kg per metre (geometric length -> kg); kg/m^3 per 1/m^2
MSUN = mp.mpf("1.989e30")


def run(alpha, n, Rt, Dt, N=60000, label=""):
    alpha, Rt, Dt = mp.mpf(alpha), mp.mpf(Rt), mp.mpf(Dt)

    def parts(r):
        w = (Rt + Dt - r) / Dt
        B = 1 + alpha * (-(n - 1) * w**n + n * w ** (n - 1))
        B1 = -(alpha / Dt) * n * (n - 1) * (w ** (n - 2) - w ** (n - 1))
        B2 = (alpha / Dt**2) * n * (n - 1) * ((n - 2) * w ** (n - 3) - (n - 1) * w ** (n - 2))
        return B, B1, B2

    Em = Ep = mp.mpf(0)
    rho_min, r_rho = mp.mpf(0), None
    Kmax, r_K = mp.mpf(0), None
    h = Dt / N
    for i in range(N):
        r = Rt + h * (i + mp.mpf("0.5"))
        B, B1, B2 = parts(r)
        rho = (B1**2 / B**4 - 2 * B2 / B**3 - 4 * B1 / (B**3 * r)) / (8 * mp.pi)
        dE = rho * 4 * mp.pi * B**3 * r**2 * h
        if rho < 0:
            Em += dE
        else:
            Ep += dE
        if rho < rho_min:
            rho_min, r_rho = rho, r
        R1212 = B1**2 / B**4 - B2 / B**3 - B1 / (B**3 * r)
        # tangential-tangential sectional curvature of conformally flat 3-metric (om = ln B):
        o1 = B1 / B
        K23 = (-2 * o1 / r - o1**2) / B**2
        K = max(abs(R1212), abs(K23))
        if K > Kmax:
            Kmax, r_K = K, r
    rc = 1 / mp.sqrt(Kmax)
    tau0 = mp.mpf("0.1") * rc
    bound = 3 * LP**2 / (32 * mp.pi**2 * tau0**4)
    wr = (Rt + Dt - r_rho) / Dt
    wK = (Rt + Dt - r_K) / Dt
    print(f"--- {label}: alpha={mp.nstr(alpha,3)}, n={n}, Rt={mp.nstr(Rt,3)} m, Dt={mp.nstr(Dt,3)} m; pocket radius alpha*Rt = {mp.nstr(alpha*Rt,3)} m")
    print(f"  E_II- = {mp.nstr(Em*KGM,4)} kg ({mp.nstr(Em*KGM/MSUN,3)} M_sun);  E_II+ = {mp.nstr(Ep*KGM,4)} kg")
    print(f"  peak rho = {mp.nstr(rho_min,4)} /m^2 = {mp.nstr(rho_min*KGM,4)} kg/m^3 at w = {mp.nstr(wr,4)}; in units 1/Dt^2: {mp.nstr(rho_min*Dt**2,4)}")
    print(f"  max orthonormal sectional |K| = {mp.nstr(Kmax,4)} /m^2 at w = {mp.nstr(wK,4)} -> r_c = {mp.nstr(rc,4)} m = Dt/{mp.nstr(Dt/rc,4)} = {mp.nstr(rc/LP,4)} L_P")
    print(f"  QI bound (tau0 = 0.1 r_c) = -{mp.nstr(bound*KGM,4)} kg/m^3 vs |rho_pk| {mp.nstr(-rho_min*KGM,4)} kg/m^3 -> "
          + ("SATISFIED (margin %s)" % mp.nstr(bound / -rho_min, 3) if -rho_min < bound else "VIOLATED by factor %s" % mp.nstr(-rho_min / bound, 3)))
    return Em, rho_min, rc


print(f"L_P = {mp.nstr(LP,5)} m; c^2/G = {mp.nstr(KGM,5)} kg/m")
# 1) VdB's stated parameters (his eq. 7)
run("1e17", 80, "1e-15", "1e-15", label="VdB stated params (eq. 7)")
# 2) What VdB's QI numbers imply: evaluate his own dimensionless results with Dt = 1e-15/alpha = 1e-32 m
Dt_implied = mp.mpf("1e-32")
rho_vdb = mp.mpf(490) / Dt_implied**2  # his eq 14: T00 = -4.9e2 / Dt^2
rc_vdb = Dt_implied / mp.mpf("72.5")  # his eq 20
b_vdb = 3 * LP**2 / (32 * mp.pi**2 * (mp.mpf("0.1") * rc_vdb) ** 4)
print(f"--- VdB's eqs 14, 20, 22 evaluated with Dt = 1e-32 m: LHS {mp.nstr(-rho_vdb*KGM,3)} kg/m^3, r_c {mp.nstr(rc_vdb,3)} m, RHS -{mp.nstr(b_vdb*KGM,3)} kg/m^3")
rho_vdb15 = mp.mpf(490) / mp.mpf("1e-15") ** 2
rc_15 = mp.mpf("1e-15") / mp.mpf("72.5")
b_15 = 3 * LP**2 / (32 * mp.pi**2 * (mp.mpf("0.1") * rc_15) ** 4)
print(f"--- VdB's eqs 14, 20, 22 evaluated with his stated Dt = 1e-15 m: LHS {mp.nstr(-rho_vdb15*KGM,3)} kg/m^3, r_c {mp.nstr(rc_15,3)} m,"
      f" RHS -{mp.nstr(b_15*KGM,3)} kg/m^3 -> violated by {mp.nstr(rho_vdb15/b_15,3)}")
# 3) General condition: rho_pk ~ k_rho / Dt^2, r_c = Dt / k_c. QI passes iff rho_pk < 3 LP^2/(32 pi^2 (0.1 r_c)^4)
#    -> Dt^2 < 3e4 LP^2 k_c^4 ... solve Dt_max for VdB's k_rho = 490, k_c = 72.5
k_rho, k_c = mp.mpf(490), mp.mpf("72.5")
Dt_max = mp.sqrt(3 * mp.mpf(10) ** 4 * k_c**4 / (32 * mp.pi**2 * k_rho)) * LP
print(f"--- QI-pass condition with VdB's profile constants: Dt < {mp.nstr(Dt_max,3)} m = {mp.nstr(Dt_max/LP,3)} L_P; r_c < {mp.nstr(Dt_max/k_c/LP,3)} L_P")
# 4) Narrower form: Planck-scale rescaled pocket keeping a 100 m pocket (alpha*Rt = 100 m)
run("1e34", 80, "1e-32", "1e-32", label="rescaled pocket, Dt = Rt = 1e-32 m")
run("1e35", 80, "1e-33", "1e-33", label="rescaled pocket, Dt = Rt = 1e-33 m")
