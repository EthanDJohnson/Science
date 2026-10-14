"""Falsifier C4-2 (scale angle): size of the linear (one off-shell graviton) photon-pair channel of a real
compact-binary source, against B&O's per-packet fusion total (the size C4 attributes to a real source).

Method (natural units hbar = c = 1, metric (+,-,-,-), toolkit conventions of qft_production.py Part D):
  N_pairs = (1/4) int d^4K/(2pi)^4 theta(K0) rho2(s) X2,  X2 = h~* Pi2 h~,  rho2(photon) = s^2/(40 pi)
  (toolkit stress_spectral_densities, checked there against Han-Lykken-Zhang and Redi-Tesi c1 = 16).
  The metric perturbation of the source: h_bar~ = 16 pi G T~/s, h = h_bar - (1/2) eta tr(h_bar).
  Source: circular Newtonian binary, quadrupole order (k a << 1, v << 1):
     T(x,t) = T_W(x) e^{-i w t} + c.c., w = 2 Omega,
     T^ij(k) = -(1/2) w^2 I_W^ij, T^0i = -(1/2) w k_j I_W^ij, T^00 = -(1/2) k_i k_j I_W^ij  (conserved),
     I_W = (mu a^2/4) [[1, i, 0], [i, -1, 0], [0, 0, 0]].
  Time integral: |2 pi delta(K0 - w)|^2 -> 2 pi delta(K0 - w) T_obs, so
     N_lin = (T_obs/4) int_{|k|<w} d^3k/(2pi)^3 rho2(w^2 - k^2) X2(w, k).
  Check: the same T_W on the light cone through Weinberg's formula
     dP/dOmega = (G w^2/pi) [T*^{lam nu} T_{lam nu} - (1/2)|T^lam_lam|^2]   must give L = (32/5) G mu^2 a^4 Omega^6.
"""
import sys, math
import numpy as np
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import qft_production as qp

ETA = np.diag([1.0, -1.0, -1.0, -1.0])


def T_upper(w, kvec, IW):
    """Upper-index T^{mu nu}(w, k) of the quadrupole source (complex 4x4)."""
    T = np.zeros((4, 4), dtype=complex)
    T[1:, 1:] = -0.5 * w * w * IW
    t0i = -0.5 * w * (IW @ kvec)
    T[0, 1:] = t0i
    T[1:, 0] = t0i
    T[0, 0] = -0.5 * kvec @ IW @ kvec
    return T


def conservation_residual(w, kvec, IW):
    T = T_upper(w, kvec, IW)
    K_low = np.array([w, -kvec[0], -kvec[1], -kvec[2]])
    return np.max(np.abs(K_low @ T))  # K_mu T^{mu nu}


def X2_of(w, kvec, IW, G):
    T = T_upper(w, kvec, IW)
    Tlow = ETA @ T @ ETA
    s = w * w - kvec @ kvec
    hbar = 16 * math.pi * G * Tlow / s
    tr = np.einsum("ab,ab->", np.linalg.inv(ETA), hbar)
    h = hbar - 0.5 * ETA * tr
    X2, X0 = qp._metric_weights(np.array(w), np.array(kvec[0]), np.array(kvec[1]), np.array(kvec[2]), h[None, :, :])
    return float(np.ravel(X2)[0]), s


def weinberg_power(w, IW, G, n=48):
    """GW power from Weinberg 10.4.13 with the same T_W, integrated over directions (|k| = w)."""
    xs, ws = np.polynomial.legendre.leggauss(n)
    phis = np.linspace(0, 2 * math.pi, 2 * n, endpoint=False)
    P = 0.0
    for c, wc in zip(xs, ws):
        sn = math.sqrt(1 - c * c)
        for ph in phis:
            kv = w * np.array([sn * math.cos(ph), sn * math.sin(ph), c])
            T = T_upper(w, kv, IW)
            Tlow = ETA @ T @ ETA
            tt = np.real(np.einsum("ab,ab->", np.conj(T), Tlow))
            tr = np.einsum("ab,ab->", Tlow, np.linalg.inv(ETA) @ np.eye(4))  # T^lam_lam = eta_{lam nu} T^{lam nu}
            tr = np.einsum("ab,ab->", ETA, T)
            P += (G * w * w / math.pi) * (tt - 0.5 * abs(tr) ** 2) * wc * (2 * math.pi / (2 * n))
    return P


def N_lin_per_time(w, IW, G, nk=40, nc=32, nphi=48):
    """N_lin / T_obs = (1/4) int_{|k|<w} d^3k/(2pi)^3 rho2 X2."""
    xk, wk = np.polynomial.legendre.leggauss(nk)
    kk = 0.5 * w * (xk + 1)
    wkk = 0.5 * w * wk
    xc, wc = np.polynomial.legendre.leggauss(nc)
    phis = np.linspace(0, 2 * math.pi, nphi, endpoint=False)
    tot = 0.0
    maxres = 0.0
    for k, wkv in zip(kk, wkk):
        for c, wcv in zip(xc, wc):
            sn = math.sqrt(1 - c * c)
            for ph in phis:
                kv = k * np.array([sn * math.cos(ph), sn * math.sin(ph), c])
                X2, s = X2_of(w, kv, IW, G)
                rho2 = float(qp.stress_spectral_densities([s], "photon")[0][0])
                tot += rho2 * X2 * k * k * wkv * wcv * (2 * math.pi / nphi)
                maxres = max(maxres, conservation_residual(w, kv, IW))
    return 0.25 * tot / (2 * math.pi) ** 3, maxres


# ---------------- dimensionless run: G = 1, mu a^2 = 1, Omega = 1 (natural units) ----------------
G = 1.0
Om = 1.0
w = 2 * Om
IW = 0.25 * np.array([[1, 1j, 0], [1j, -1, 0], [0, 0, 0]])  # mu a^2 = 1
L_quad = 32.0 / 5.0 * G * Om ** 6
L_wein = weinberg_power(w, IW, G)
print(f"[check] Weinberg power with this T_W: {L_wein:.6f}; quadrupole (32/5) G mu^2 a^4 Om^6 = {L_quad:.6f}; ratio {L_wein/L_quad:.6f}")

for (nk, nc, nphi) in [(16, 16, 24), (32, 24, 40)]:
    rate, res = N_lin_per_time(w, IW, G, nk, nc, nphi)
    k_lin = rate / (G * w * L_quad)
    print(f"[grid nk={nk},nc={nc},nphi={nphi}] N_lin/T_obs = {rate:.6e} (natural units); k_lin = N_lin/(G w E_GW) = {k_lin:.6e}; max conservation residual {res:.1e}")

# Ratio to B&O's fusion total in its Parseval form P_fus = (12 pi/25) G^2 w Int L^2 dt (natural units)
# For a steady source over T_obs: N_lin/P_fus = k_lin G w L T / ((12 pi/25) G^2 w L^2 T) = (25 k_lin/(12 pi)) / (G L)
c_ratio = 25 * k_lin / (12 * math.pi)
print(f"N_lin/P_fus = {c_ratio:.4e} x (L_P/L_GW)   [L_P = c^5/G]")

# ---------------- SI numbers ----------------
Gsi = 6.67430e-11; c = 2.99792458e8; Msun = 1.98892e30; hbar = 1.054571817e-34
LP = c ** 5 / Gsi
print(f"L_P = c^5/G = {LP:.4e} W (SI)")

# GW150914 with B&O inputs: E = 2 Msun c^2, f = 150 Hz, sigma = 200 rad/s
for EM in (2.0, 3.0):
    E = EM * Msun * c ** 2
    wg = 2 * math.pi * 150.0
    sig = 200.0
    N_lin = k_lin * Gsi * wg * E / c ** 5
    P_BO = 4.0 / 25.0 * Gsi ** 2 * E ** 2 * wg * sig / c ** 10
    print(f"GW150914 E={EM} Msun c^2: G w E/c^5 = {Gsi*wg*E/c**5:.3e}; N_lin = {N_lin:.3e} pairs; B&O top-hat total P = {P_BO:.3e}; ratio N_lin/P = {N_lin/P_BO:.3e}")
# profile-free comparison with L = 3.6e49 W
Lpk = 3.6e49
print(f"GW150914 at L = 3.6e49 W: N_lin/P_fus = {c_ratio*LP/Lpk:.3e}")

# GW170817 whole Newtonian chirp 30-1600 Hz, Mc = 1.188 Msun (same inputs as M-IDEALIZER-10)
Mc = 1.188 * Msun
def int_w_dE(f1, f2):
    w1, w2 = 2 * math.pi * f1, 2 * math.pi * f2
    # |dE| = (1/3) Mc^{5/3} G^{2/3} 2^{-2/3} w^{-1/3} dw  (E_orb = -(1/2) Mc (G Mc w/2)^{2/3})
    return (1.0 / 3.0) * Mc ** (5.0 / 3.0) * Gsi ** (2.0 / 3.0) * 2 ** (-2.0 / 3.0) * 0.6 * (w2 ** (5.0 / 3.0) - w1 ** (5.0 / 3.0))
Nlin_170817 = k_lin * Gsi / c ** 5 * int_w_dE(30.0, 1600.0)
print(f"GW170817 chirp 30-1600 Hz: N_lin = {Nlin_170817:.3e} pairs; B&O-model chirp total 2.83e-8 (M-IDEALIZER-10): ratio {Nlin_170817/2.83e-8:.3e}")
# GW150914 inspiral 35-68 Hz, Mc = 28 Msun
Mc = 28 * Msun
Nlin_insp = k_lin * Gsi / c ** 5 * int_w_dE(35.0, 68.0)
print(f"GW150914 inspiral 35-68 Hz: N_lin = {Nlin_insp:.3e} pairs; B&O-model 2.75e-8: ratio {Nlin_insp/2.75e-8:.3e}")
# Galactic WD binary: L_GW = 1.697e28 W (M-IDEALIZER-10); ratio is frequency-independent for a steady source
Lwd = 1.697e28
print(f"WD binary L = 1.697e28 W: N_lin/P_fus = {c_ratio*LP/Lwd:.3e}; N_lin per year at f_GW = 3 mHz = {k_lin*Gsi*2*math.pi*3e-3*Lwd*3.156e7/c**5:.3e} pairs")
# Upper envelope of N_lin for any source: G w E/c^5 = (G E/c^4)(w/c) = (r_m/2)(w/c); with w <~ c/(G M/c^2)
print("Envelope: N_lin = k_lin (G E/c^4)(w/c); for E <= M c^2 and w <~ c^3/(G M): N_lin <~ k_lin x O(1)")
