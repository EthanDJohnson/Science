"""falsifier-C8-2_bounds.py  (refuter 2 of C8, angle: bounds)

Question: can ONE proton-detection-side cause produce both
  (i) BL1 reading +1.1% long  (an absolute proton-count deficit of ~1.1%), and
  (ii) aSPECT's |a| low by ~2.7% (a = -0.10402 vs -0.10687 from PERKEO III lambda)?

aSPECT extracts a from the SHAPE of the integral proton spectrum N(U) with a free
normalisation (Beck 2020, arXiv:1908.04785, Eq. 7: "strong correlation (>0.9) among
the fit parameters N0 and a").  So an energy-independent efficiency cancels.
Only a recoil-energy (T) dependence of the detection efficiency eps(T) moves a.
We compute:
  A. the SM (b=0) recoil spectrum w(T;a) (leading order, no recoil-order/RC terms);
  B. the aSPECT transmission function (Beck 2020 Eq. 4, r_B = 0.203);
  C. the fitted a when synthetic data built with a_true = -0.10687 and an efficiency
     eps(T) are fit with (N0, a) free, for several eps(T) shapes;
  D. the eps(T) needed for a_fit = -0.10402, and the spectrum-averaged loss it implies;
  E. the implied below-threshold loss at 15 keV if that slope is a detector-energy effect
     (proton energy at the aSPECT SDD is 15.0-15.75 keV, Beck 2020 p.8);
  F. aCORN (proton-involving a measurement) against 'same bias' and 'no bias'.
Units: energies in eV (SI-derived), masses in eV/c^2; a, lambda dimensionless.
"""
import numpy as np

me = 510998.95        # eV
Mp = 938272088.0      # eV
Mn = 939565420.0      # eV
Delta = Mn - Mp       # eV
E0 = Delta - (Delta**2 - me**2) / (2 * Mn)  # max electron total energy incl. recoil (approx)

def fermi(E):
    # nonrelativistic Fermi function, Z=1 (daughter proton), adequate for shape study
    p = np.sqrt(E**2 - me**2)
    eta = (1/137.035999) * E / p
    x = 2 * np.pi * eta
    return x / (1 - np.exp(-x))

# Electron energy grid
NE = 4000
E = np.linspace(me * 1.000001, E0 * 0.999999, NE)
pe = np.sqrt(E**2 - me**2)
Enu = E0 - E
beta = pe / E
wE = fermi(E) * pe * E * Enu**2

Tmax = ((pe + Enu)**2).max() / (2 * Mp)
NT = 3000
Tgrid = np.linspace(0.0, Tmax, NT + 1)
Tc = 0.5 * (Tgrid[1:] + Tgrid[:-1])

def recoil_spectrum_parts(Tc):
    """return w0(T), w1(T) so that w(T;a) = w0 + a*w1 (unnormalised)."""
    w0 = np.zeros_like(Tc)
    w1 = np.zeros_like(Tc)
    for i, T in enumerate(Tc):
        pp2 = 2 * Mp * T
        c = (pp2 - pe**2 - Enu**2) / (2 * pe * Enu)
        ok = np.abs(c) <= 1
        jac = Mp / (pe * Enu)          # dcos/dT
        g = wE * jac * ok
        w0[i] = np.trapezoid(g, E)
        w1[i] = np.trapezoid(g * beta * np.where(ok, c, 0.0), E)
    return w0, w1

w0, w1 = recoil_spectrum_parts(Tc)
dT = Tgrid[1] - Tgrid[0]

rB = 0.203
def Ftr(T, U):
    T = np.asarray(T)
    out = np.zeros_like(T)
    hi = T >= U / (1 - rB)
    mid = (T > U) & ~hi
    out[hi] = 1.0
    x = (1 - U / T[mid]) / rB
    out[mid] = 1 - np.sqrt(1 - x)
    return out

Us = np.array([50., 70., 250., 300., 400., 500., 600.])   # aSPECT-like retardation points (V)
Fm = np.array([Ftr(Tc, U) for U in Us])

def integral(eps, a):
    w = (w0 + a * w1) * eps
    return Fm @ w * dT

a_true = -0.10687   # PERKEO III lambda -> a  (M-DIALECTICIAN-05)
a_asp = -0.10402    # aSPECT 2024
lam = 1.27641
print(f"check: a(lambda=1.27641) = {(1-lam**2)/(1+3*lam**2):.5f}")
print(f"Tmax = {Tmax:.1f} eV (Beck 2020 quotes 751 eV)")

def fit_a(y):
    # y = N0*(A0 + a*A1); fit N0, a by weighted LS, weights 1/y (Poisson, equal time)
    A0 = Fm @ w0 * dT
    A1 = Fm @ w1 * dT
    W = 1 / y
    best = None
    for a in np.linspace(-0.14, -0.07, 70001):
        m = A0 + a * A1
        N0 = np.sum(W * y * m) / np.sum(W * m * m)
        chi = np.sum(W * (y - N0 * m) ** 2)
        if best is None or chi < best[0]:
            best = (chi, a, N0)
    return best[1]

# sanity: no distortion returns a_true
a_cl = fit_a(integral(np.ones_like(Tc), a_true))
print(f"closure: fit of undistorted data -> a = {a_cl:.5f}")
print("PASS closure" if abs(a_cl-a_true)<2e-6 else "FAIL closure")
print("PASS Tmax" if abs(Tmax-751)<3 else "FAIL Tmax")
# sensitivity to an offset in U (compare Beck 2020: da/a = 1.4e-4 per mV)
def fit_with_Ushift(dU):
    Fm_s = np.array([Ftr(Tc, U + dU) for U in Us])
    y = Fm_s @ ((w0 + a_true * w1)) * dT
    return fit_a(y)
aU = fit_with_Ushift(0.080)
print(f"validation: U offset +80 mV -> da/a = {(aU-a_true)/abs(a_true)*100:+.2f}%  (Beck 2020: ~1%)")

# A. uniform loss of 1.1% (what BL1 needs) -> effect on a
eps_u = np.full_like(Tc, 1 - 0.011)
au = fit_a(integral(eps_u, a_true))
print(f"A. uniform 1.1% loss: a_fit = {au:.5f}, da/a = {(au-a_true)/abs(a_true)*100:+.3f}%")

# B. linear-in-T loss eps = 1 - eta*(1 - T/Tmax): loss largest at low T
target = a_asp
def a_for_eta(eta):
    eps = 1 - eta * (1 - Tc / Tmax)
    return fit_a(integral(eps, a_true))
for eta in [0.001, 0.005, 0.01, 0.02]:
    ae = a_for_eta(eta)
    print(f"B. eta={eta:.3f}: a_fit={ae:.5f}, da/a={(ae-a_true)/abs(a_true)*100:+.2f}%")
# solve for eta giving target (linear response)
e1 = 0.01
s = (a_for_eta(e1) - a_true) / e1
eta_need = (target - a_true) / s
a_chk = a_for_eta(eta_need)
wnorm = (w0 + a_true * w1)
avg_loss = np.sum(wnorm * eta_need * (1 - Tc / Tmax)) / np.sum(wnorm)
print(f"D. eta needed for a_fit = {target}: {eta_need:.4f} (check a_fit = {a_chk:.5f})")
print(f"   i.e. efficiency difference eps(Tmax)-eps(0) = {eta_need*100:.2f}% across 0-{Tmax:.0f} eV")
print(f"   spectrum-averaged loss implied = {avg_loss*100:.2f}%")
print(f"   slope at SDD energy (15.0-15.75 keV): {eta_need*100/(Tmax/1000):.2f}% per keV")

# E. if detector-energy driven with loss L(E) ~ E^-n, L(15 keV) = slope*E/n
for n in [0.5, 1.0, 2.0]:
    L15 = (eta_need / (Tmax / 1000)) * 15.0 / n
    L30 = L15 * (15.0 / 30.0) ** n
    print(f"E. power law n={n}: implied below-threshold loss at 15 keV = {L15*100:.1f}%, at 30 keV (BL1-like) = {L30*100:.1f}%")

# C. sharp low-energy cutoff: lose all protons with T < Tcut
for Tcut in [50., 100., 150., 200.]:
    eps = np.where(Tc < Tcut, 0.0, 1.0)
    ac = fit_a(integral(eps, a_true))
    lost = np.sum(wnorm * (Tc < Tcut)) / np.sum(wnorm)
    print(f"C. cutoff T<{Tcut:.0f} eV lost ({lost*100:.1f}% of all protons): a_fit={ac:.5f}, da/a={(ac-a_true)/abs(a_true)*100:+.2f}%")

# F. aCORN
lam_P3, s_P3 = -1.27641, 0.00056
lam_asp, s_asp = -1.2668, 0.0027
lam_ac, s_ac = -1.2796, 0.0062
bias = lam_asp - lam_P3
pred_biased = lam_P3 + bias
z_b = (lam_ac - pred_biased) / np.hypot(s_ac, np.hypot(s_asp, s_P3))
z_u = (lam_ac - lam_P3) / np.hypot(s_ac, s_P3)
print(f"F. proton-side lambda bias (aSPECT - PERKEO III) = {bias:+.4f}")
print(f"   aCORN vs 'same bias' prediction {pred_biased:.4f}: z = {z_b:.2f} sigma")
print(f"   aCORN vs unbiased PERKEO III: z = {z_u:.2f} sigma")
print(f"   likelihood ratio unbiased:biased = {np.exp((z_b**2 - z_u**2)/2):.1f}")
print(f"   aCORN vs aSPECT directly: z = {(lam_ac-lam_asp)/np.hypot(s_ac,s_asp):.2f} sigma")
