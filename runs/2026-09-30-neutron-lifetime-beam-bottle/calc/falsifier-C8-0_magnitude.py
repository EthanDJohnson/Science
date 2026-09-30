"""Falsifier C8-0 (magnitude): can ONE proton-side effect give both
(1) a 1.1% deficit of absolutely counted protons in BL1 (tau long by ~9.9 s) and
(2) a +0.00285 shift of aSPECT's a (|a| low by 2.7%)?

Units: energies in eV (proton kinetic T), MeV for electron kinematics (hbar=c=1);
times in s; fractions dimensionless.

Model: proton recoil spectrum w(T; a) from n -> p e nu with weight
F(Z=1,E) p_e E_e (E0-E_e)^2 (1 + a beta cos) (b = 0), nonrelativistic proton recoil.
aSPECT: integral spectrometer, transmission for isotropic protons with rB = 0.203
(Beck et al. 2020, arXiv:1908.04785): fraction of angles with T(1 - rB sin^2) > eU.
Fit: y(U) = N (Y0(U) + a Y1(U)), linear in (N, N a), Poisson weights, equal time per U.
Retardation settings assumed: 50,150,250,300,400,500,600 V (aSPECT used >= 50 V).
"""
import numpy as np

me = 0.51099895; Mn = 939.56542; Mp = 938.27209
E0 = (Mn**2 - Mp**2 + me**2) / (2 * Mn)          # total e energy endpoint, MeV
alpha = 1 / 137.036
lam = 1.27641
a_true = (1 - lam**2) / (1 + 3 * lam**2)
a_aspect = -0.10402
Da_req = a_aspect - a_true
print(f"E0 = {E0:.5f} MeV; a(PERKEO III lam) = {a_true:.5f}; aSPECT a = {a_aspect}; required Da = {Da_req:+.5f} ({Da_req/abs(a_true)*100:.2f}% of |a|)")

NE, NC = 3000, 400
Ee = np.linspace(me * 1.00001, E0 * 0.999999, NE)
pe = np.sqrt(Ee**2 - me**2); beta = pe / Ee; Enu = E0 - Ee; pnu = Enu
eta = alpha * Ee / pe
F = 2 * np.pi * eta / (1 - np.exp(-2 * np.pi * eta))
wE = F * pe * Ee * Enu**2
c = (np.arange(NC) + 0.5) / NC * 2 - 1
PE, CC = np.meshgrid(pe, c, indexing="ij")
PNU = np.meshgrid(pnu, c, indexing="ij")[0]
BETA = np.meshgrid(beta, c, indexing="ij")[0]
WE = np.meshgrid(wE, c, indexing="ij")[0]
T = (PE**2 + PNU**2 + 2 * PE * PNU * CC) / (2 * Mp) * 1e6   # eV
W0 = WE.ravel(); W1 = (WE * BETA * CC).ravel(); T = T.ravel()
norm = W0.sum()
W0 = W0 / norm; W1 = W1 / norm
Tmax = T.max()
print(f"Tmax = {Tmax:.1f} eV (expected ~751 eV)")

rB = 0.203
U = np.array([50., 150., 250., 300., 400., 500., 600.])

def Ftr(Tv, u):
    x = (1 - u / np.maximum(Tv, 1e-9)) / rB
    out = np.where(x >= 1, 1.0, 1 - np.sqrt(np.clip(1 - x, 0, 1)))
    return np.where(Tv > u, out, 0.0)

FT = np.array([Ftr(T, u) for u in U])           # (nU, npts)
Y0 = FT @ W0; Y1 = FT @ W1

def fit_a(eps):
    w = W0 + a_true * W1
    y = FT @ (w * eps)
    sig2 = y.copy()                              # Poisson, equal time
    A = np.vstack([Y0, Y1]).T / np.sqrt(sig2)[:, None]
    bb = y / np.sqrt(sig2)
    P, *_ = np.linalg.lstsq(A, bb, rcond=None)
    return P[1] / P[0]

def deficit(eps):
    w = W0 + a_true * W1
    return 1 - (w * eps).sum() / w.sum()

print(f"closure: undistorted fit a = {fit_a(np.ones_like(T)):.6f}")

# (i) threshold loss of all protons below Tc
print("\n(i) sharp low-energy loss, eps = 0 for T < Tc")
for Tc in [10, 20, 30, 40, 50, 60, 80, 100, 150, 200]:
    e = (T >= Tc).astype(float)
    print(f"  Tc = {Tc:4d} eV: BL1-type count deficit = {deficit(e)*100:6.3f}%  -> dtau = {deficit(e)/(1-deficit(e))*878.3:6.2f} s ; aSPECT Da = {fit_a(e)-a_true:+.5f}")
# find Tc for 1.1% deficit
from bisect import bisect
Tcs = np.linspace(1, 300, 3000)
defs = np.array([deficit((T >= t).astype(float)) for t in Tcs[::10]])
idx = np.argmin(abs(defs - 0.0111)); Tc11 = Tcs[::10][idx]
e = (T >= Tc11).astype(float)
print(f"  Tc for 1.11% deficit ~ {Tc11:.0f} eV; aSPECT Da there = {fit_a(e)-a_true:+.6f} (required {Da_req:+.5f})")
das = np.array([fit_a((T >= t).astype(float)) - a_true for t in Tcs[::10]])
j = np.argmin(abs(das - Da_req))
print(f"  Tc for aSPECT Da = required: {Tcs[::10][j]:.0f} eV, Da = {das[j]:+.5f}, BL1 deficit = {defs[j]*100:.2f}% -> dtau = {defs[j]/(1-defs[j])*878.3:.1f} s")

# (ii) linear low-energy-favoured loss eps = 1 - k (1 - T/Tmax)
print("\n(ii) linear loss eps = 1 - k(1 - T/Tmax)")
g = (1 - T / Tmax)
d1 = fit_a(1 - 0.01 * g) - a_true
k = Da_req / d1 * 0.01
e = 1 - k * g
print(f"  k needed for Da = {k:.4f} (fit check Da = {fit_a(e)-a_true:+.5f}); BL1 deficit if same eps = {deficit(e)*100:.2f}% -> dtau = {deficit(e)/(1-deficit(e))*878.3:.1f} s (needed 9.9 s)")

# (iii) exponential low-energy loss eps = 1 - k exp(-T/T0)
print("\n(iii) eps = 1 - k exp(-T/T0)")
for T0 in [10, 15, 20, 22, 25, 30, 50, 100, 200, 400]:
    g = np.exp(-T / T0)
    d1 = fit_a(1 - 0.01 * g) - a_true
    k = Da_req / d1 * 0.01
    e = 1 - k * g
    ok = "unphysical (k>1)" if k > 1 else ""
    print(f"  T0 = {T0:3d} eV: k = {k:.3f} {ok}; BL1 deficit = {deficit(e)*100:.2f}% -> dtau = {deficit(e)/(1-deficit(e))*878.3:.1f} s")

# (iv) maximum Da per unit lost fraction: remove a thin band at energy Tb
print("\n(iv) sensitivity: Da per unit removed fraction, thin band [Tb, Tb+10 eV]")
best = 0
for Tb in np.arange(0, 750, 10):
    band = (T >= Tb) & (T < Tb + 10)
    e = np.where(band, 0.99, 1.0)
    f = deficit(e)
    if f <= 0: continue
    s = (fit_a(e) - a_true) / f
    if s > best: best, Tbest = s, Tb   # positive direction (|a| reduced), as aSPECT requires
print(f"  max positive dDa/df = {best:+.4f} at Tb = {Tbest} eV (loss of protons in this band raises a toward aSPECT)")
fmin = Da_req / best
print(f"  minimum lost fraction in aSPECT to shift a by {Da_req:+.5f}: {fmin*100:.2f}% of protons")

# (v) time scaling of an in-flight proton loss (residual-gas charge exchange)
t_BL1 = 10e-3      # s, BL1 trapping time scale (dossier: 5 ms vs 10 ms trap cycles)
t_aSP = 10e-6      # s, aSPECT proton TOF scale (Beck 2020: t0 = 7.2-10.0 us, tau ~ 2.8 us)
f_aSP = 0.0111 * t_aSP / t_BL1
print(f"\n(v) same gas density & cross-section: loss in aSPECT = 1.11% x {t_aSP/t_BL1:.0e} = {f_aSP:.2e}")
print(f"    max Da from that loss = {f_aSP*best:+.2e} vs required {Da_req:+.5f}: ratio {Da_req/(f_aSP*best):.0f}x short")
print(f"    pressure ratio aSPECT/BL1 needed = {fmin/f_aSP:.0f}")

# (v-b) retardation-set robustness: drop 150 V (use 50,250,300,400,500,600)
FT_full = FT
sel = np.array([u != 150. for u in U])
FT = FT_full[sel]; Y0 = FT @ W0; Y1 = FT @ W1
g = (1 - T / Tmax); d1 = fit_a(1 - 0.01 * g) - a_true; k = Da_req / d1 * 0.01
print(f"\n(v-b) settings without 150 V: linear k = {k:.4f}, BL1 dtau = {deficit(1-k*g)/(1-deficit(1-k*g))*878.3:.1f} s; "
      f"threshold 25 eV Da = {fit_a((T>=25).astype(float))-a_true:+.6f}")
FT = FT_full; Y0 = FT @ W0; Y1 = FT @ W1

# (vi) coincidence ratio: SM mapping of lambda shift to tau
dlam = -0.0094   # |lambda| shift
tau_ratio = (1 + 3 * lam**2) / (1 + 3 * (lam + dlam)**2) - 1
a_shift = (1 - (lam + dlam)**2) / (1 + 3 * (lam + dlam)**2) - a_true
print(f"\n(vi) SM: |lam| -{abs(dlam)} -> tau_beta +{tau_ratio*100:.2f}% ({tau_ratio*878.7:.1f} s), Da = {a_shift:+.5f}")
print(f"    ratio (Da/|a|)/(dtau/tau) implied by SM = {a_shift/abs(a_true)/tau_ratio:.2f}")
