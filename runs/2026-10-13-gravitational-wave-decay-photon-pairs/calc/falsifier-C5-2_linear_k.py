"""Falsifier C5-2 (scale): compute the linear-channel coefficient k in P_lin = k (hbar w / E_Pl)^2 N_GW.

Process: source stress tensor T -> its own (off-shell) metric h~ = 16 pi G T~/K^2 at time-like K -> photon pair
via the gravity vertex L = -(1/2) h_{mu nu} T_EM^{mu nu}. Uses the toolkit's tested Born spectral machinery
(qft_production.born_metric_general, rho2_photon = s^2/(40 pi)). Natural units hbar = c = 1, G = 1 (scale-free:
the ratio P_lin / (G w^2 N_GW) is a pure number). Source: a Gaussian-windowed rotating mass quadrupole
(circular-binary pattern) or a linear quadrupole, with a Gaussian form factor exp(-k^2 R^2/2) for finite size,
v = w R. Conservation K_mu T^{mu nu} = 0 is built in (exact for the point quadrupole times any F(|k|)).

Comparison: N_GW = (2G/5) int_0^inf dw/(2pi) w^5 sum_ij |I~_ij^STF(w)|^2 (quadrupole formula, same I~).
Semi-analytic cross-check for F = 1: P_lin = (8 c2/3)(2pi)... computed as a 1D integral below.
"""
import sys, math
import numpy as np
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import qft_production as q

PI = math.pi
G = 1.0
w0 = 1.0
ETA = np.diag([1.0, -1.0, -1.0, -1.0])


def make_source(pattern, tau, R, amp=1e-3):
    # I_ij(t) = amp * Re[e_ij exp(-i w0 t)] * exp(-t^2/(2 tau^2)); keep positive-frequency part only (K0 > 0)
    if pattern == "circular":
        e = np.array([[1, 1j, 0], [1j, -1, 0], [0, 0, 0]], dtype=complex) / 2.0  # rotating binary, STF
    elif pattern == "linear":
        e = np.diag([-1.0, -1.0, 2.0]).astype(complex) / 2.0                      # linear oscillator along z, STF
    else:
        raise ValueError(pattern)

    def Itil(K0):
        # FT of amp*(1/2) e exp(-i w0 t) exp(-t^2/2tau^2) with convention int dt e^{i K0 t}
        return amp * 0.5 * math.sqrt(2 * PI) * tau * np.exp(-0.5 * (K0 - w0) ** 2 * tau ** 2)

    def htilde4(K0, Kx, Ky, Kz):
        k = np.stack([Kx, Ky, Kz], axis=-1)
        I = Itil(K0)[..., None, None] * e                       # I~_ij(K0)
        F = np.exp(-0.5 * (Kx ** 2 + Ky ** 2 + Kz ** 2) * R ** 2)[..., None, None]
        Tij = -0.5 * K0[..., None, None] ** 2 * I               # T~^{ij}
        T0i = -0.5 * K0[..., None] * np.einsum("...j,...ij->...i", k, I)
        T00 = -0.5 * np.einsum("...i,...j,...ij->...", k, k, I)
        T = np.zeros(K0.shape + (4, 4), dtype=complex)
        T[..., 0, 0] = T00
        T[..., 0, 1:] = T0i
        T[..., 1:, 0] = T0i
        T[..., 1:, 1:] = Tij
        T = T * F
        Tlow = np.einsum("am,...mn,nb->...ab", ETA, T, ETA)     # lower indices
        s = K0 ** 2 - (Kx ** 2 + Ky ** 2 + Kz ** 2)
        return 16 * PI * G * Tlow / s[..., None, None]           # spin-2 part is all that matters (Pi2 removes traces)

    def N_gw():
        w = np.linspace(1e-6, w0 + 12 / tau, 200001)
        STF2 = float(np.sum(np.abs(e) ** 2))
        integrand = w ** 5 * np.abs(Itil(w)) ** 2 * STF2
        return (2 * G / 5) * np.trapezoid(integrand, w) / (2 * PI)

    def P_semi_pointlike():
        # point source: X2 = (16 pi G)^2 |T_TT|^2/s^2 with |T_TT|^2 = (K0^4/4) sum|I^STF|^2 (k -> 0 limit of the
        # spin-2 projection); N = (1/4) int d^4K/(2pi)^4 rho2 X2, rho2 = s^2/(40 pi); d^3k over |k| < K0
        w = np.linspace(1e-6, w0 + 12 / tau, 200001)
        STF2 = float(np.sum(np.abs(e) ** 2))
        integrand = 0.25 * (1 / (40 * PI)) * (16 * PI * G) ** 2 * (w ** 4 / 4) * np.abs(Itil(w)) ** 2 * STF2 \
            * (4 * PI / 3) * w ** 3 / (2 * PI) ** 4
        return np.trapezoid(integrand, w)

    return htilde4, N_gw, P_semi_pointlike


print("Linear channel coefficient k = P_lin / [(hbar w0/E_Pl)^2 N_GW] = P_lin/(G w0^2 N_GW), natural units, G = w0 = 1")
print("analytic point-source narrow-band prediction: k = 1/(6 pi) =", 1 / (6 * PI))
tau = 10.0  # sigma/w ~ 0.1
smax = (w0 + 6 / tau) ** 2
kmax = w0 + 6 / tau
results = {}
for pattern in ["circular", "linear"]:
    for R in [0.0, 0.3, 0.5, 0.8]:
        h4, Ngw, Psemi = make_source(pattern, tau, R)
        N = Ngw()
        out = {}
        for (ns, nk) in [(60, 60), (100, 100)]:
            r = q.born_metric_general(h4, s_max=smax, kappa_max=kmax, field="photon", n_s=ns, n_k=nk, n_c=8, n_p=8)
            out[(ns, nk)] = r["pairs"]
        Pa, Pb = out[(60, 60)], out[(100, 100)]
        kk = Pb / (G * w0 ** 2 * N)
        results[(pattern, R)] = kk
        line = f"{pattern:8s} v = w0 R = {R:.1f}: N_GW = {N:.4e}, P_lin(60x60) = {Pa:.5e}, P_lin(100x100) = {Pb:.5e}, " \
               f"grid change {abs(Pb - Pa) / Pb:.1e}, k = {kk:.5f}"
        if R == 0.0:
            line += f", semi-analytic k = {Psemi() / (G * w0 ** 2 * N):.5f}"
        print(line)

print()
kreq = 3.2e-4
print(f"C5 threshold (candidates.md): k >= {kreq:.1e} for GW150914")
for key, kk in results.items():
    print(f"  {key}: k = {kk:.4f}, k/k_required = {kk / kreq:.0f}")

# SI numbers for GW150914 (B&O inputs E = 2 Msun c^2, f = 150 Hz; LVK E = 3.0 Msun c^2)
Gsi, c, hbar, Msun = 6.674e-11, 2.998e8, 1.0546e-34, 1.989e30
print()
print("GW150914, SI: P_lin = k * G E w / c^5 (since (hbar w/E_Pl)^2 N = G E w/c^5)")
for E_ms in [2.0, 3.0]:
    for f in [150.0, 250.0]:
        E = E_ms * Msun * c ** 2
        w = 2 * PI * f
        base = Gsi * E * w / c ** 5
        for key in [("circular", 0.0), ("circular", 0.5), ("linear", 0.5)]:
            print(f"  E = {E_ms} Msun c^2, f = {f:.0f} Hz, {key}: (hbar w/E_Pl)^2 N = {base:.3e} pairs/k, "
                  f"P_lin = {results[key] * base:.2e} pairs")
P_BO_low, P_BO_high = 7.0e-7, 1.4e-5
print(f"  C4 fusion totals quoted in candidates.md: {P_BO_low:.1e} to {P_BO_high:.1e} pairs")
base = Gsi * 2.0 * Msun * c ** 2 * 2 * PI * 150 / c ** 5
print(f"  ratio P_lin/P_fusion at B&O inputs (k = circular v=0.5): {results[('circular', 0.5)] * base / P_BO_high:.0f} "
      f"to {results[('circular', 0.5)] * base / P_BO_low:.0f}")
