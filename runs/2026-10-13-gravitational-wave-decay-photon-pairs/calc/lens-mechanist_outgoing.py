"""Mechanist lens: where does g g -> gamma gamma happen for an OUTGOING wave, and does it persist (a 'decay')?

Causal chain test. Local fusion rate per volume for two crossing plane waves (toolkit qft_second_order,
in-in leading order) as a function of crossing angle theta; then a spherical outgoing shell of energy E,
thickness L = c/sigma, at radius r, whose local wave-vector spread is theta(r). Two bracketing models:
  Fresnel (upper):   theta_F(r) = (k r)^(-1/2)  (stationary-phase width of directions contributing at a point)
  gradient (lower):  theta_g(r) = (k r)^(-1)    (transverse amplitude variation on scale r)
both capped at pi/2 (r <~ 1/k: source/near zone, where this model is not valid anyway).
Pairs made while the shell crosses [r, r+dr]: dN = Gamma(rho(r), theta(r)) * 4 pi r^2 L * dr / c, with the
local field split into two equal half-energy 'beams' crossing at theta (an O(1) bookkeeping choice).
Units: SI (J, m, s, rad/s). Compared with B&O eq. 8 read as a sustained rate over the 410 Mpc path.
"""
import math
import sys

import numpy as np

sys.path.insert(0, ".claude/skills/conundrum/scripts")
import qft_second_order as q2  # noqa: E402

G_SI, c, hbar = 6.67430e-11, 2.99792458e8, 1.054571817e-34
Msun = 1.98892e30
Mpc = 3.0857e22

# GW150914-like inputs as B&O (D-27): E_rel = 2 Msun c^2, f = 150 Hz, sigma_w = 200 rad/s
E = 2 * Msun * c ** 2
f = 150.0
w = 2 * math.pi * f
sig = 200.0
k = w / c
L = c / sig
print(f"Inputs (SI): E = {E:.3e} J, f = {f} Hz, w = {w:.1f} rad/s, sigma_w = {sig} rad/s, L = c/sigma = {L:.3e} m,"
      f" 1/k = {1/k:.3e} m")

# 1. theta scaling of the two-beam rate at fixed strain (plus/plus, equal frequency)
h = 1e-21
print("\n1. Two-beam rate per volume vs crossing angle (h = 1e-21 each, plus/plus), SI pairs m^-3 s^-1")
ths = [1.0, 0.3, 0.1, 0.03, 0.01]
rates = []
for th in ths:
    r = q2.beams_pair_rate_SI(w, h, th)
    rates.append(r["pair_rate_SI"])
    print(f"  theta = {th:6.3f} rad: Gamma = {r['pair_rate_SI']:.4e}, rho each = {r['rho1_SI']:.4e} J/m^3")
slope = math.log(rates[-1] / rates[-2]) / math.log(ths[-1] / ths[-2])
print(f"  small-angle power law: Gamma ~ theta^{slope:.3f} (expect 4: s ~ theta^2, sigma ~ G^2 s, flux ~ theta^2)")
rho_ref = q2.beams_pair_rate_SI(w, h, 1.0)["rho1_SI"]
Grate = {th: rr for th, rr in zip(ths, rates)}
r_head = q2.beams_pair_rate_SI(w, h, math.pi)["pair_rate_SI"]
print(f"  head-on (theta = pi): Gamma = {r_head:.4e}")


def gamma_local(rho_total, theta):
    """pairs per m^3 per s, two half-energy beams at angle theta; Gamma ~ rho1 rho2, theta^4 law below 0.01."""
    th = min(theta, math.pi / 2)
    if th >= 0.01:
        g = q2.beams_pair_rate_SI(w, h, th)["pair_rate_SI"]
    else:
        g = Grate[0.01] * (th / 0.01) ** 4
    return g * (0.5 * rho_total / rho_ref) ** 2


def dN_dr(r, model):
    rho = E / (4 * math.pi * r * r * L)
    th = (k * r) ** -0.5 if model == "fresnel" else (k * r) ** -1.0
    return gamma_local(rho, th) * 4 * math.pi * r * r * L / c


print("\n2. Pairs made by the outgoing shell beyond radius r (integral r..infinity), two theta(r) models")
rs = np.logspace(math.log10(1 / k), math.log10(410 * Mpc), 400)
for model in ("fresnel", "gradient"):
    vals = np.array([dN_dr(x, model) for x in rs])
    # cumulative from outside in (log-trapezoid on dN/dlnr)
    integrand = vals * rs
    tail = np.zeros_like(rs)
    for i in range(len(rs) - 2, -1, -1):
        tail[i] = tail[i + 1] + 0.5 * (integrand[i] + integrand[i + 1]) * math.log(rs[i + 1] / rs[i])
    sl = math.log(vals[-1] / vals[-50]) / math.log(rs[-1] / rs[-50])
    print(f"  model {model}: dN/dr ~ r^{sl:.2f} at large r")
    for rr, lab in ((1 / k, "1/k"), (10 / k, "10/k"), (1e3 / k, "1e3/k"), (1.496e11, "1 AU"), (3.0857e19, "1 kpc")):
        i = int(np.argmin(np.abs(rs - rr)))
        print(f"    N(>r = {lab:6s} = {rs[i]:.2e} m) = {tail[i]:.3e} pairs")

# 3. B&O eq. 8 read as sustained rate: dP/dt = 3 G^2 E^2 w sigma^2 / (25 pi c^10) (SI form of their eq. 8)
dPdt = 3 * G_SI ** 2 * E ** 2 * w * sig ** 2 / (25 * math.pi * c ** 10)
T_eff = 4 * math.pi / (3 * sig)
D = 410 * Mpc
print("\n3. B&O eq. 8 (SI form 3 G^2 E^2 w sigma^2/(25 pi c^10))")
print(f"  dP/dt = {dPdt:.3e} pairs/s; x T_eff = 4pi/(3 sigma) = {T_eff:.4f} s -> per-packet total {dPdt*T_eff:.3e} pairs")
print(f"  read as sustained along D = 410 Mpc (t = {D/c:.3e} s): {dPdt*D/c:.3e} pairs, energy {dPdt*D/c*2*hbar*w:.3e} J"
      f" = {dPdt*D/c*2*hbar*w/E:.3e} of E")
print(f"  B&O validity tau << 1/sigma: (pair time 1/(dP/dt) = {1/dPdt:.3e} s) vs 1/sigma = {1/sig:.3e} s")
print("  (sigma/w = %.3f: the narrow-band premise is marginal at B&O's own GW150914 point)" % (sig / w))
