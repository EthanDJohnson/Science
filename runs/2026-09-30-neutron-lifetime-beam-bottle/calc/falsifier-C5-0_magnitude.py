"""Falsifier C5-0 (magnitude): can n -> X+ e- nubar (X+ -> 2A0 + e+) carry the ~1.1% proton-beam gap?

Units: masses/energies in MeV (hbar = c = 1 for kinematics); times in s; rates in s^-1.
Checks:
 (1) mass window of X+ (on-shell 9Be stability, n kinematics);
 (2) a STABLE (or long-lived) X+ in the BL1 Penning trap: mass ~ m_p, charge +1, recoil < 800 eV well
     -> trapped and counted like a proton. Fraction escaping axially (T_axial > 800 eV) vs m_X;
 (3) short-lived X+: fraction still counted vs tau_X for BL1 trapping periods 5 and 10 ms;
 (4) the same n-X-e-nu vertex plus X -> 2A e+ makes every BOUND neutron decay via an off-shell X*
     (n -> e- nubar e+ 2A, energy release > 100 MeV). Rate vs Gamma_X, compared with nucleon-decay
     lifetime bounds -> lower bound on tau_X.  Window  tau_X(BL1 max) vs tau_X(nuclear min).
"""
import numpy as np

mn, mp, me = 939.56542, 938.27209, 0.51100
HBAR = 6.582119569e-22  # MeV s
YR = 3.15576e7
S_9Be_2an = 1.57270   # 9Be -> 2alpha + n threshold (AME2020 value as used in M-CONSTRAINTS-07), MeV
S_16O = 15.6636       # S_n(16O), MeV (AME2020)
S_2H = 2.22457        # S_n(2H), MeV

tau_st, tau_pb = 877.82, 887.7   # s: storage (UCNtau) and proton beam (BL1)
G1 = 1/tau_st - 1/tau_pb         # s^-1, required exotic partial rate
print(f"Required exotic partial rate Gamma_X-branch = {G1:.4e} s^-1 (Br = {G1*tau_st*100:.3f}% of total)")

# ---- (1) mass window
mX_lo = mn - me - S_9Be_2an
mX_hi = mn - me
print(f"(1) X+ mass window: {mX_lo:.4f} < m_X < {mX_hi:.4f} MeV ; m_p = {mp} ; |m_X - m_p| < {max(mp-mX_lo, mX_hi-mp):.3f} MeV")
print(f"    q/m of X+ equals the proton's to within {max(mp-mX_lo, mX_hi-mp)/mp*100:.3f}%")

# ---- (2) recoil energies and BL1 axial escape
rng = np.random.default_rng(1)
def recoil_sample(mX, N=400000):
    E0 = (mn**2 - mX**2 + me**2)/(2*mn)   # max electron total energy
    # sample E_e from p E (E0-E)^2 (no Coulomb) by rejection
    E = rng.uniform(me, E0, 4*N); p = np.sqrt(E**2 - me**2)
    w = p*E*(E0-E)**2; keep = rng.uniform(0, w.max(), E.size) < w
    E = E[keep][:N]; p = p[keep][:N]
    pnu = E0 - E  # approx (neglect recoil energy)
    c = rng.uniform(-1, 1, E.size)   # e-nu angle, no correlation (a=0)
    pX = np.sqrt(p**2 + pnu**2 + 2*p*pnu*c)
    T = pX**2/(2*mX)*1e6   # eV
    cosal = rng.uniform(-1, 1, E.size)  # isotropic recoil direction relative to B axis
    return T, T*cosal**2
print("(2) BL1 well depth +800 eV (Nico 2005). Recoil of X+ and fraction with axial KE > 800 eV:")
for mX in [mX_lo, 937.8, mp, 938.6, 938.9]:
    T, Tax = recoil_sample(mX)
    print(f"    m_X = {mX:.4f} MeV: T_max = {T.max():7.1f} eV, <T> = {T.mean():6.1f} eV, "
          f"f(T>800) = {np.mean(T>800):.4f}, f(T_axial>800) = {np.mean(Tax>800):.4f}")
# proton check (SM): T_max should be ~751 eV
T, Tax = recoil_sample(mp)
print(f"    sanity: proton-mass recoil max {T.max():.1f} eV (Nico 2005 quotes 751 eV)")

# gap reproduced if uncounted fraction u: proton beam measures Gamma_beta + (1-u) Gamma_X
def gap(u):
    Gb = 1/tau_pb; Gt = 1/tau_st
    Gp = Gb + (1-u)*(Gt-Gb)
    return 1/Gp - tau_st
T, Tax = recoil_sample(mX_lo)
u_max = np.mean(Tax > 800)
print(f"    stable X+: max uncounted fraction (lightest allowed m_X) u = {u_max:.3f} -> beam shift {gap(u_max):.2f} s of needed {tau_pb-tau_st:.2f} s")
print(f"    stable X+ with m_X = m_p: u = 0 -> beam shift {gap(0.0):.2f} s")

# ---- (3) unstable X+: fraction counted in BL1 (born uniformly in trapping period Tt, counted if alive at extraction)
print("(3) Short-lived X+: counted fraction f = (tau/T)(1-exp(-T/tau)); beam shift reproduced:")
for Tt in [5e-3, 10e-3]:
    for tX in [1e-6, 1e-4, 1e-3, 3e-3, 1e-2, 1e-1]:
        f = tX/Tt*(1-np.exp(-Tt/tX))
        print(f"    T_trap = {Tt*1e3:.0f} ms, tau_X = {tX:.0e} s: counted f = {f:.4f}, shift = {gap(1-f):.2f} s")
# tau_X max for >= 90% of the gap (f <= 0.1) at T = 5 ms (the more demanding BL1 subset)
from math import exp
def f_count(tX, Tt): return tX/Tt*(1-exp(-Tt/tX))
for Tt in [5e-3, 10e-3]:
    lo, hi = 1e-9, 1.0
    for _ in range(200):
        mid = np.sqrt(lo*hi)
        if f_count(mid, Tt) > 0.1: hi = mid
        else: lo = mid
    print(f"    T_trap = {Tt*1e3:.0f} ms: tau_X <= {lo:.3e} s needed for f <= 0.10 (>= ~90% of gap)")
tauX_max = 5e-4  # s, from T = 5 ms (f<=0.1)

# ---- (4) off-shell X* decay of bound neutrons
def F(E0):
    """beta phase-space integral int_{me}^{E0} p E (E0-E)^2 dE (MeV^5), no Coulomb"""
    if E0 <= me: return 0.0
    E = np.linspace(me, E0, 4001); p = np.sqrt(np.maximum(E**2-me**2, 0))
    return np.trapezoid(p*E*(E0-E)**2, E)

def bound_rate_coeff(mX, S, mA, Qcut, nX=2.5):
    """Gamma_bound / (Gamma_1 * hbarGamma_X)  in MeV^-1, narrow-width off-shell tail:
       Gamma_bound = Gamma_1/F(E0free) * int dm* F(W - m*) * [hbarGamma_X(m*)/(2 pi (mX - m*)^2)],
       W = mn - S (energy available to e + nu + X*), Gamma_X(m*) = Gamma_X (Q*/Q)^nX with Q = mX - 2mA - me.
       m* restricted to [max(2mA+me, W-me-Qcut), W-me] (conservative truncation of the far off-shell tail)."""
    E0free = (mn**2 - mX**2 + me**2)/(2*mn)
    W = mn - S
    lo = max(2*mA + me, W - me - Qcut); hi = W - me
    if hi <= lo or hi >= mX: return 0.0
    ms = np.linspace(lo, hi, 3001)
    Q = mX - 2*mA - me
    integ = np.array([F(W - m) for m in ms]) * (np.maximum(ms - 2*mA - me, 0.0)/Q)**nX / (2*np.pi*(mX - ms)**2)
    return np.trapezoid(integ, ms)/F(E0free)

print("(4) Off-shell X* decay of bound neutrons: coefficient C = Gamma_bound/(Gamma_1 * hbar*Gamma_X) [MeV^-1]")
print("    and the minimum tau_X = hbar*C*Gamma_1/Gamma_bound,max for nucleon-lifetime bounds tau_N (per neutron)")
results = []
for nuc, S in [("2H", S_2H), ("16O", S_16O)]:
    for mA in [370., 400., 430., 460.]:
        for Qcut, nX in [(1.0, 4.0), (1.0, 2.5), (20.0, 2.5)]:
            C = bound_rate_coeff(mp, S, mA, Qcut, nX)
            if C == 0:
                print(f"    {nuc:3s} m_A={mA:.0f} Qcut={Qcut:4.0f} nX={nX}: channel closed"); continue
            line = f"    {nuc:3s} m_A={mA:.0f} MeV, Qcut={Qcut:4.0f} MeV, nX={nX}: C = {C:.3e} MeV^-1;"
            for tauN_yr in [1e25, 1e29, 1.7e32]:
                Gb_max = 1/(tauN_yr*YR)
                tX_min = HBAR*C*G1/Gb_max
                line += f" tau_N>{tauN_yr:.0e} yr -> tau_X > {tX_min:.1e} s;"
                results.append((nuc, mA, Qcut, nX, tauN_yr, tX_min))
            print(line)
worst = min(r[5] for r in results if r[4] == 1e25)
print(f"    Weakest lower bound on tau_X over all rows with a very weak tau_N > 1e25 yr: {worst:.2e} s")
print(f"    BL1 requires tau_X <= {tauX_max:.1e} s -> gap between windows = factor {worst/tauX_max:.1e}")
wSK = min(r[5] for r in results if r[4] == 1.7e32 and r[0]=="16O")
print(f"    16O with Super-K-scale tau_N > 1.7e32 yr (weakest row): tau_X > {wSK:.2e} s = {wSK/YR:.2e} yr; factor {wSK/tauX_max:.1e} over BL1 max")
print("(5) Critical per-neutron lifetime tau_N* above which the tau_X window closes (tau_X,min > BL1 max 5e-4 s):")
print("    tau_N* = tau_Xmax / (hbar * C * Gamma_1); most conservative settings Qcut = 1 MeV, nX = 4")
for nuc, S in [("2H", S_2H), ("16O", S_16O)]:
    for mX in [mX_lo + 0.01, mp, 938.9]:
        for mA in [370., 400., 460.]:
            C = bound_rate_coeff(mX, S, mA, 1.0, 4.0)
            if C <= 0 or not np.isfinite(C):
                print(f"    {nuc:3s} m_X={mX:.3f} m_A={mA:.0f}: channel closed/on-shell"); continue
            tN = tauX_max/(HBAR*C*G1)/YR
            print(f"    {nuc:3s} m_X={mX:.3f} MeV m_A={mA:.0f} MeV: C = {C:.3e} MeV^-1 -> tau_N* = {tN:.2e} yr")
print("(6) Escape sliver: off-shell route closed in nucleus if 2 m_A + 2 m_e > m_n - S (nothing left for e- nubar e+ 2A)")
for nuc, S in [("2H", S_2H), ("9Be(2a+n)", S_9Be_2an), ("16O", S_16O)]:
    print(f"    {nuc:10s}: closed for m_A > {(mn - S - 2*me)/2:.3f} MeV")
print(f"    X+ -> 2A e+ open only for m_A < (m_X,max - m_e)/2 = {(mX_hi - me)/2:.3f} MeV")
print(f"    deuterons in 1 kt D2O: {1e9/20.03*2*6.02214e23:.2e} (one neutron each); "
      f"at tau_N* = 1.14e18 yr -> {1e9/20.03*2*6.02214e23/1.14e18:.1e} decays/yr")
# sanity: free neutron on-shell limit of the formula -> the BW integral over the peak gives Gamma_1 (check normalization)
print("    sanity: C scales as 1/(2 pi delta) for small Qcut; 2H delta =", round((mn-S_2H-me)-mp,3), "MeV below m_X (needs m* < m_X: ", (mn-S_2H-me) < mp, ")")
