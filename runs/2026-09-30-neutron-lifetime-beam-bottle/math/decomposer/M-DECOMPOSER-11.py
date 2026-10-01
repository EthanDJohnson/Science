"""M-DECOMPOSER-11 (F11): phase-space average <m_e/E> and the Fierz-shifted tau_beta.
Spectrum dGamma/dW ∝ p W (W0 - W)^2 F(Z=1, W), W = E/m_e (total), p = sqrt(W^2-1), W0 from two-body-recoil endpoint
E0 = (mn^2 - mp^2 + me^2)/(2 mn). Fermi function (relativistic, point-like with nuclear radius R):
F = 2(1+g)(2pR)^(2(g-1)) exp(pi eta) |Gamma(g + i eta)|^2 / Gamma(2g+1)^2, g = sqrt(1-alpha^2), eta = alpha W/p.
Gamma ∝ (1+3 lam^2)(1 + b <m_e/E>)  =>  tau_beta(b, lam) = tau_beta(lam) / (1 + b <m_e/E>). SI (s); masses MeV."""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
sys.path.insert(0, "runs/2026-09-30-neutron-lifetime-beam-bottle/math/decomposer")
import mpmath as mp
from math_checks import limit, identity, finish
from _inputs import near, q, BL1, UCNT
from _sm import *

mp.mp.dps = 20
mn, mpr, me = 939.56542052, 938.27208816, 0.51099895
alpha = 1 / 137.035999
E0 = (mn ** 2 - mpr ** 2 + me ** 2) / (2 * mn)
W0 = E0 / me
R = 0.84e-15 / 3.8615926796e-13   # proton radius in units of hbar/(m_e c)
print(f"E0 = {E0:.6f} MeV total, W0 = {W0:.5f}, R = {R:.3e}")
g = math.sqrt(1 - alpha ** 2)
def F(W):
    p = mp.sqrt(W ** 2 - 1); eta = alpha * W / p
    return 2 * (1 + g) * (2 * p * R) ** (2 * (g - 1)) * mp.exp(mp.pi * eta) * abs(mp.gamma(g + 1j * eta)) ** 2 / mp.gamma(2 * g + 1) ** 2
def avg(fermi):
    w = (lambda W: mp.sqrt(W ** 2 - 1) * W * (W0 - W) ** 2 * (F(W) if fermi else 1))
    return mp.quad(lambda W: w(W) / W, [1, W0]) / mp.quad(w, [1, W0])
a_F = float(avg(True)); a_0 = float(avg(False))
print(f"<m_e/E> with Fermi function {a_F:.5f}; without {a_0:.5f}")
near("<m/E> Fermi", a_F, 0.6555, 0.0005); near("<m/E> no Coulomb", a_0, 0.6542, 0.0005)
b, sb = -0.0181, 0.0065; lam, sl = 1.2724, 0.0013
t0 = tau_beta(lam, C=C_TAN); t = t0 / (1 + b * a_F)
eb = t * a_F * sb / (1 + b * a_F); el = abs(dtau_dlam(lam, t)) * sl
efix = q(2 * t * VUD_E / VUD, t * DRV_E / (1 + DRV))
for rho in (0.0, -0.5, 0.5):
    # rho = corr(b, lam); dtau/db < 0 and dtau/dlam < 0 so positive rho adds
    e = math.sqrt(eb ** 2 + el ** 2 + 2 * rho * eb * el + efix ** 2)
    print(f"rho(b,lam) = {rho:+.1f}: tau_beta = {t:.2f} +- {e:.2f} s (b {eb:.2f}, lam {el:.2f}, fixed {efix:.2f})")
e0 = math.sqrt(eb ** 2 + el ** 2 + efix ** 2)
near("Fierz tau_beta", t, 893.70, 0.05)
near("Fierz tau_beta error (rho = 0)", e0, 4.18, 0.05)
z1 = (t - BL1[0]) / q(e0, BL1[1]); z2 = (t - UCNT[0]) / q(e0, UCNT[1])
print(f"above BL1 {z1:.2f} sigma, above UCNtau {z2:.2f} sigma")
near("vs BL1", z1, 1.3, 0.05); near("vs UCNtau", z2, 3.8, 0.05)
# limits: b -> 0 recovers the SM; massless-electron limit of the Fierz average (W0 -> large) goes to 0
limit("t0/(1 + bb*a)", "bb", 0, "t0")
x = mp.mpf(50)
big = mp.quad(lambda W: mp.sqrt(W**2-1)*(x-W)**2, [1, x]) / mp.quad(lambda W: mp.sqrt(W**2-1)*W*(x-W)**2, [1, x])
print(f"<1/W> without Coulomb at W0 = 50: {float(big):.4f} (-> 0 as W0 -> inf, the massless limit)")
raise SystemExit(finish())
