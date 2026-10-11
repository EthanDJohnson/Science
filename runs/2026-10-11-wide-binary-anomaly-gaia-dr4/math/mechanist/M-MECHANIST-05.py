"""M-MECHANIST-05: mass-estimate bias. Model: v_p^2 = γ G M_true / s × f (f = geometry/orbit factor, same law in both zones).
ṽ_est^2 = v_p^2 s / (G M_est) = γ (M_true/M_est) f. Template estimator: γ_hat = median(ṽ_est^2)/median(f) = γ M_true/M_est.
Calibrated (Chae-style) estimator: γ_hat = median(ṽ_low^2)/median(ṽ_cal^2) = γ (k_low/k_cal), k = M_true/M_est per zone.
Claims (F8, F9, cand D): −10% M_est → γ × 1/0.9 = 1.111 for template families; calibrated E1b cancels a uniform bias;
wide-only −10% passes one-for-one (E1b 1.104); a ≈25% wide-only underestimate gives ≈ +0.3. Sensitivity numbers are the lens's.
(Second-order effect ignored by the identity: the g_N proxy also shifts by 0.046 dex, moving bin edges slightly.)"""
import sys, math
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import sympy as sp
from math_checks import identity, quantity, limit, inequality, finish
g, G, Mt, Me, s, f, kl, kc = sp.symbols("g G M_t M_e s f k_l k_c", positive=True)
vt2 = (g * G * Mt / s * f) * s / (G * Me)
identity(vt2 / f, g * Mt / Me)                     # template: γ_hat = γ M_true/M_est
identity((g * kl * f) / (1 * kc * f), g * kl / kc)  # calibrated: ratio of zone factors (cal zone Newtonian)
identity(((g * kl * f) / (kc * f)).subs(kl, kc), g)  # uniform bias cancels
limit(g * Mt / Me, "M_e", Mt, "g")                   # unbiased mass recovers γ
quantity("1/0.9", "1.111", rel_tol=1e-3)
ref = dict(E1a=1.090, E2a=1.063, E3=1.021, E4=1.119, E1b=1.003)
both = dict(E1a=1.204, E2a=1.167, E3=1.146, E4=1.217, E1b=0.993)
for k in ref:
    print(f"{k}: ratio −10% both zones = {both[k]/ref[k]:.4f}; shift {both[k]-ref[k]:+.3f}")
    target = 1.0 if k == "E1b" else 1 / 0.9
    quantity(f"{both[k]/ref[k]}", f"{target}", rel_tol=0.025)   # lens's ±0.02 per entry
print(f"E1b wide-only: {1.104/1.003:.4f} (predicted 1/0.9 = {1/0.9:.4f})")
quantity(f"{1.104/1.003}", f"{1/0.9}", rel_tol=0.02)
for lo, hi in ((1.05, 1.37), (1.003, 1.37), (1.0, 1.30)):
    print(f"wide-only underestimate needed to raise {lo} to {hi}: {1 - lo/hi:.3f}")
inequality("1 - 1.05/1.37", ">=", "0.20"); inequality("1 - 1.003/1.37", "<=", "0.30")
raise SystemExit(finish())
