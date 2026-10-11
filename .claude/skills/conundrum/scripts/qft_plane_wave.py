#!/usr/bin/env python3
"""qft_plane_wave: particle production by plane waves and null backgrounds to ALL orders in the amplitude,
with every function saying exactly WHICH quantity it returns (numpy only; builds on qft_production.py).

Why this tool exists
    qft_production.py (qp) treats a plane wave at first order (Born): every Fourier component of a
    source-free wave has K^2 = 0, so the first-order yield of massive pairs vanishes. That leaves open
    whether the zero survives at strong amplitude. This module answers it non-perturbatively, on a
    lattice (Parts A-B) and with Gibbons' exact modes in a gravitational sandwich wave (Part C). The
    traps it keeps apart: in-in mean numbers versus in-out amplitudes and vacuum persistence; plane
    waves versus packets (a pattern switched on in time IS a packet); real production versus the
    transient dressing while the field is on; particles versus pairs (real field: pairs = half).
    Every public function's docstring has a "Quantity:" line and a "Valid when:" line, and inputs
    outside that range raise ValueError.

Units (read this first)
    Natural units hbar = c = 1, Heaviside-Lorentz electromagnetism (e^2 = 4 pi alpha), exactly as qp.
    Pick ONE energy unit (e.g. the mass m, or eV) and give masses, momenta, frequencies and V(t, z)
    (an energy^2) in it; times and lengths are then in 1/energy. Like qp (precedent: page_wootters.py)
    this deviates from schemas.md's "SI in the Python API": the helpers length_to_inverse_eV,
    length_from_inverse_eV and qp.time_to_inverse_eV / qp.time_from_inverse_eV convert, and the command
    line accepts units through unit_tools.Q ("0.511 MeV", "2e-11 m", "1e-20 s").

PART A. Lattice Bogoliubov solver: real scalar in 1+1 dimensions, any V(t, z)
-----------------------------------------------------------------------------
    (d_t^2 - d_z^2 + m^2 + V(t, z)) phi = 0 on a periodic box z in [-L/2, L/2), N grid points (N even).
    * Spectral Galerkin, de-aliased: modes k_n = 2 pi n / L with |n| < N/3 (the 2/3 rule), each with the
      EXACT continuum dispersion omega_k^2 = k^2 + m^2. V enters through its Fourier coefficients
      V_q(t) = (1/N) sum_j V(t, z_j) e^{-i q z_j} as the Toeplitz matrix V_{n-n'} for |n - n'| < N/3, so
      the product V phi never aliases. V must be band-limited to |q| < (N/3)(2 pi/L): the dropped tail
      max |V_q| (N/3 <= |n| <= N/2, relative to max |V_q|) is reported as 'band_tail' and refused
      above band_tol (default 1e-9).
    * Mode functions: in-mode p is f_p = sum_k F_kp(t) e^{ikz}/sqrt(L), F'' = -(omega^2 + V_hat(t)) F,
      F(t0) = diag(e^{-i w_in t0}/sqrt(2 w_in)), w_in^2 = k^2 + m^2 + V(t0) (V must be z-independent at
      both window ends; it may differ between them, e.g. the tanh model).
    * Exact linear symplectic evolution of all 2N_k x N_k mode data: a 4th-order 6-stage splitting
      (Blanes & Moan 2002, method S6) of the exact free flow (rotation by omega_k h) and the exact kick
      F' -> F' - h V_hat F. Each factor is symplectic, so alpha alpha^dag - beta beta^dag = 1 holds to
      roundoff at ANY step size ('symplectic_error'); accuracy comes from step halving.
    * Out-region: f_p = sum_k (alpha_pk g_k + beta_pk g_k^*), g_k = e^{ikz - i w_out t}/sqrt(2 w_out L):
          alpha_pk = sqrt(w/2) e^{+iwt1} (F_kp + i F'_kp/w),  beta_{p,-k} = sqrt(w/2) e^{-iwt1} (F_kp - i F'_kp/w).
      N_out(k) = sum_p |beta_pk|^2 = <in| a_out,k^dag a_out,k |in>   (IN-IN mean number in out-mode k);
      Tr beta^dag beta = sum_k N_out(k)  = total mean number of PARTICLES in the box; real field: each
          pair puts one particle in k and one in p, so pairs = particles / 2;
      |beta_pk|^2: in-mode p's contribution to N_out(k) (at first order: mean number of pairs (k, p));
      alpha_pk: IN-OUT scattering amplitude among positive-frequency modes (what the wave does to a
          particle: phase shifts, momentum transfer), not a number;
      vacuum persistence |<0_out|0_in>|^2 = 1/|det alpha| = det(1 + beta beta^dag)^(-1/2): IN-OUT
          probability that nothing at all is made; 1 - it ~ pairs only at weak field.
    * Precision floor per entry delta_pk = max(step-halving change of beta, roundoff 4 eps sqrt(kicks N_k)
      max|alpha|, window-end mismatch |V - mean V|/(4 w_min^2) and adiabaticity/4). 'total_floor' =
      sum delta^2 is the Tr beta^dag beta that numerical noise alone would show: Tr <= total_floor means
      "zero to the floor". Relative error of Tr: (2 sqrt(Tr floor) + floor)/Tr; above flag_rel (1%) the
      result is flagged resolved=False.
    * lattice_born gives the first-order |beta_pk|^2 on the same lattice (diagnostic: compare amplitudes).

PART B. Null, subluminal and superluminal patterns (what the lattice shows)
---------------------------------------------------------------------------
    pattern_potential: V = eps exp(-t^2/(2T^2)) cos(q z - w t), phase velocity v = w/|q|.
    * v = 1, NULL (V = V(t - z) apart from the envelope): an eternal null pattern conserves the
      light-front momentum P_- = H - P (exactly, also on the truncated lattice: the scheme is covariant
      under t, z -> t + a, z + a), and every pair has P_- = (w1 - k1) + (w2 - k2) > 0, so it makes
      NOTHING, to all orders (Gibbons 1975 for gravitational sandwich waves, Schwinger for EM plane waves).
    * In a periodic box the pattern MUST be switched on (no in/out region otherwise), and switching makes
      it a packet: co-moving pairs of total momentum nq gain Delta_n = sqrt(n^2 q^2 + 4 m^2) - n q from
      the envelope. The leakage falls only exponentially in T (high orders defeat the Gaussian's
      exp(-Delta^2 T^2); measured eps = 0.3 m^2, q = m, k_c = 1.375 m: 6e-7, 2e-11, 7e-16, 2e-20, 8e-25 at
      T = 6, 10, 14, 18, 22 /m), so the null zero needs slow switching. Self-test: T = 26/m gives Tr = 3e-26, the
      measured noise level (the subluminal pattern plateaus at 1.4e-26), below the solver's conservative floor
      (6e-23, a roundoff bound).
    * Lattice caveat: mode k's light-front dressing spreads over harmonics k + jq, |j| up to about
      eps/(2 p_- q), p_- = w - k -> m^2/(2k). Near the band edge (+k_c) a strong pattern needs more
      harmonics than the band holds; the truncated lattice then breaks light-front positivity and makes
      SPURIOUS pairs that grow with T and N (measured, eps = 1.5 m^2, q = m: Tr = 10.8, 18.6 at T = 6, 10 with
      N = 36 and 38, 183 with N = 48). Check in N.
    * v < 1, subluminal: static in the frame moving with v (keep m^2 + V > 0: pattern_potential refuses
      |eps| >= m^2): spacelike support, nothing in the slow-switching limit.
    * v > 1, superluminal: homogeneous in the frame moving with 1/v: timelike support s = q^2 (v^2 - 1);
      pairs at first order when s >= 4 m^2, resonant where (w1 + w2, k1 + k2) = (v q, q); the number grows
      with T (a rate; at strong eps faster, by parametric amplification). On a lattice the resonant pairs
      must lie inside the band: v = 2.5, q = m, k_c = 1.375 m gives 7.2, 17.8, 47 particles at T = 6, 10,
      14 /m (pair (1.125, -0.125) m; exact/Born 1.3, 2.2, 4.1), but v = 3 (resonant pair near (1.6, -0.6) m,
      outside) leaves only switching leakage, FALLING with T: 0.28, 0.05, 0.006.
    * Weak field, 1+1 D Born (first order, in-in): N_pairs = int dK0 dKz/(2pi)^2 theta(K0) |V~|^2 rho_1+1(s),
      rho_1+1(s) = 1/(2 sqrt(s (s - 4m^2))) (real field, identical-particle 1/2 included). Integrating
      rho_1+1(s; m^2 + k_perp^2) over d^2k_perp/(2pi)^2 gives qp's beta/(16 pi), hence
          rho_1+1(s; m^2) = -4 pi d rho_3+1/d(m^2),
      and born_pairs_1p1 evaluates qp.born_scalar_planar's integral and differentiates it in m^2
      (Richardson), next to a direct evaluation of the 1+1 formula.

PART C. Gibbons' exact scalar modes in a plane sandwich gravitational wave
--------------------------------------------------------------------------
    Metric (Gibbons 1975 eq. 2.1; the PDF text reads "ds2 = dUdV + H^tyXWdU2 - dX'dX1", our reading):
        ds^2 = dU dV + H_ij(U) X^i X^j dU^2 - dX^i dX^i,  U = t - z, V = t + z;
    sandwich: H = 0 outside [U1, U2]; vacuum wave: tr H = 0 ('+': H = diag(h, -h); 'x': off-diagonal).
    * Jacobi (geodesic deviation) matrices: P'' = -H P with P(U_a) = 1, P'(U_a) = 0, and Q'' = -H Q with
      Q(U_a) = 0, Q'(U_a) = 1 (U_a before the wave); Wronskian P^T Q' - P'^T Q = 1 (checked).
    * Rosen coordinates (Gibbons eq. 2.5): X = P x, V = v + x^T P^T P' x gives ds^2 = du dv - a_ij dx^i dx^j,
      a = P^T P. In them the Klein-Gordon equation is solved exactly (Gibbons eqs. 3.1-3.3, whose exponents
      the PDF extraction garbles; derived again here, with e^{-i w t} as positive frequency):
          phi_{k,c} = (det a)^{-1/4} exp(i k.x - i c v - (i/4c) int^u (k^T a^{-1} k + m^2) du'),  c > 0,
      with int (P^T P)^{-1} du = P^{-1} Q (no 1/P^2 integral). In Brinkmann coordinates:
          phi = |det P|^{-1/2} exp(i k.P^{-1}X + i c X^T P'P^{-1} X - i c V - (i/4c)(k.P^{-1}Q k + m^2 (U - U_a))).
      Before the wave this is the plane wave with w = c + (k^2 + m^2)/(4c), k_z = (k^2 + m^2)/(4c) - c,
      so c = (w - k_z)/2 > 0 is positive frequency. With phi = e^{-icV} psi the KG equation is exactly
      i d_U psi = [-lap_X/(4c) + c X^T H X + m^2/(4c)] psi (a Schroedinger equation; mass 2c).
    * beta = 0: d_V is a Killing vector, so every mode keeps its e^{-icV}; on the null surfaces U = const
      (Gibbons' substitute Cauchy surfaces) the KG product (f, g) = i int dV d^2X (f* d_V g - g d_V f*)
      vanishes between c > 0 and c' < 0, however strong the wave. gibbons_packet demonstrates it by an
      explicit projection of an exact packet onto out-modes (FFT over V and X on the null surface U_b).
    * The wave still acts: geodesics at rest before it at X0 leave with dX/dtau = P'(U) X0 (velocity
      memory; square pulse: Chakraborty & Kar 2022 eqs. 16-17), and an exact packet's mean transverse
      momentum after the wave is 2c P' X0 + Q' k0 (Ehrenfest, exact for this quadratic problem): alpha
      is a non-trivial unitary (lensing), beta = 0.
    * Caustics: where det P = 0 the Rosen chart breaks down (Gibbons: "the basis breaks down when the
      chart breaks down"); the functions refuse U at or beyond the first zero of det P.
    * Bridge to Part B: at fixed Rosen momentum k, chi = a^{1/4} phi obeys 4 d_u d_v chi + (m^2 + k^T a^{-1} k) chi
      = 0, i.e. the 1+1 problem with a null potential V(u): the mechanism of Part B's null zero.

Assumptions and validity range
    Free fields in a classical, prescribed background (no back-reaction). Part A: adiabatic in AND out
    regions where V is z-independent with m^2 + V > 0; the box is periodic (a localized pattern wraps),
    and particle numbers between the ends are NOT computed (transient dressing). Part C: test field on an
    exact plane-wave spacetime, U before the first caustic.

Python usage
    import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
    import numpy as np, qft_plane_wave as pw
    pat = pw.pattern_potential(eps=0.3, n_q=8, v=3.0, T=6.0, L=16 * np.pi, m=1.0)   # superluminal
    r = pw.lattice_bogoliubov(pat["V"], 16 * np.pi, 36, 1.0, *pat["window"])
    r["total"], r["pairs"], r["total_floor"], r["vacuum_persistence"]           # particles, pairs (in-in)
    pw.born_pairs_1p1(lambda K0, Kz: np.exp(-(K0 - 3)**2 - (Kz - 1)**2), m=1.0, s_max=60, y_max=6)
    H = lambda U: np.multiply.outer(0.25 * ((U >= -1) & (U <= 1)), np.diag([1.0, -1.0]))  # '+' square pulse
    pw.velocity_memory(H, [0.5, 0.3], -2.0, 2.0, breaks=(-1.0, 1.0))["velocity"]          # classical, exact
    pw.gibbons_packet(H, -1.25, 1.25, c=1.0, m=1.0, X0=[0.5, 0.3], sigma=1.0, breaks=(-1.0, 1.0))["beta_norm"]  # 0

Command line (from the project root)
    python3 .claude/skills/conundrum/scripts/qft_plane_wave.py selftest
    python3 .claude/skills/conundrum/scripts/qft_plane_wave.py pattern --eps 0.3 --nq 8 --v 3 --T 6 --L 50.27 --N 36
    python3 .claude/skills/conundrum/scripts/qft_plane_wave.py pattern --m "0.511 MeV" --eps 0.3 --nq 8 --v 1 --T "2.9e-20 s" --L "1.94e-11 m"
    python3 .claude/skills/conundrum/scripts/qft_plane_wave.py gibbons --A0 0.5 --a 1 --c 1 --x0 0.5 --y0 0.3
    python3 .claude/skills/conundrum/scripts/qft_plane_wave.py convergence      (slow: switching leakage vs T, N; floor vs steps)
"""
from __future__ import annotations

import math
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (_HERE, ".claude/skills/conundrum/scripts"):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import qft_production as qp  # noqa: E402  (mode solver, Born spectral forms, SI helpers)
from unit_tools import C, E_CHARGE, HBAR  # noqa: E402  (CODATA values shared by the toolkit)

PI = math.pi
_EPS = np.finfo(float).eps

# Blanes & Moan 2002 (J. Comput. Appl. Math. 142, 313), 6-stage 4th-order symmetric splitting "S6":
# e^{a1 h A} e^{b1 h B} e^{a2 h A} ... e^{b1 h B} e^{a1 h A}. The paper is paywalled (not quoted); the
# coefficients are checked by the self-test through 4th-order convergence (error ratio ~16 per halving).
_BM_A1, _BM_A2, _BM_A3 = 0.0792036964311957, 0.353172906049774, -0.0420650803577195
_BM_B1, _BM_B2 = 0.209515106613362, -0.143851773179818
_BM_A = (_BM_A1, _BM_A2, _BM_A3, 1.0 - 2.0 * (_BM_A1 + _BM_A2 + _BM_A3), _BM_A3, _BM_A2, _BM_A1)
_BM_B = (_BM_B1, _BM_B2, 0.5 - (_BM_B1 + _BM_B2), 0.5 - (_BM_B1 + _BM_B2), _BM_B2, _BM_B1)


# ---------------------------------------------------------------- SI helpers
def length_to_inverse_eV(L_m: float) -> float:
    """Convert a length in m to natural units 1/eV: L_nat = L_SI e/(hbar c).

    Quantity: length in 1/eV (hbar = c = 1).
    Valid when: L_m is a length in metres."""
    return L_m * E_CHARGE / (HBAR * C)


def length_from_inverse_eV(L_nat: float) -> float:
    """Convert a length given in 1/eV (natural units) to metres: L_SI = L_nat hbar c / e.

    Quantity: length in m.
    Valid when: L_nat is a length in units of 1/eV."""
    return L_nat * HBAR * C / E_CHARGE


# ---------------------------------------------------------------- input checks
def _finite(x, name: str) -> float:
    x = float(x)
    if not math.isfinite(x):
        raise ValueError(f"{name} must be finite")
    return x


def _eval_V(V_of_tz, ts: np.ndarray, z: np.ndarray) -> np.ndarray:
    """V on the (time, grid) product, shape (len(ts), len(z)); broadcasting first, a loop as fallback."""
    try:
        out = np.asarray(V_of_tz(ts[:, None], z[None, :]), dtype=float)
        out = np.broadcast_to(out, (len(ts), len(z)))
    except (ValueError, TypeError, IndexError):
        out = np.array([np.broadcast_to(np.asarray(V_of_tz(float(t), z), dtype=float), z.shape) for t in ts])
    if not np.all(np.isfinite(out)):
        raise ValueError("V(t, z) returned non-finite values")
    return out


# ---------------------------------------------------------------- Part A: lattice solver
def _lattice_grid(L: float, N: int) -> dict:
    n_max = (N - 1) // 3                            # kept |n| < N/3 (2/3 rule)
    n = np.arange(-n_max, n_max + 1)
    D = n[:, None] - n[None, :]
    fq = np.fft.fftfreq(N, 1.0 / N).round().astype(int)
    return {"n": n, "k": 2 * PI * n / L, "z": -0.5 * L + L * np.arange(N) / N, "idx": np.mod(D, N),
            "band": np.abs(D) < N / 3.0, "tail": np.abs(fq) >= N / 3.0,
            "sign": np.where(np.arange(N) % 2 == 0, 1.0, -1.0)}   # e^{-iq z_j} with z_0 = -L/2: (-1)^n (N even)


def _lattice_check(V_of_tz, L, N, m, t0, t1):
    L, m, t0, t1 = _finite(L, "L"), _finite(m, "m"), _finite(t0, "t0"), _finite(t1, "t1")
    if L <= 0 or m < 0 or t1 <= t0:
        raise ValueError("need L > 0, m >= 0 and t0 < t1")
    if int(N) != N or N < 8 or N % 2:
        raise ValueError("N must be an even integer >= 8")
    g = _lattice_grid(L, int(N))
    ends = []
    for t in (t0, t1):
        Vz = _eval_V(V_of_tz, np.array([t]), g["z"])[0]
        mean = float(Vz.mean())
        ends.append((mean, float(np.max(np.abs(Vz - mean)))))
    return L, int(N), m, t0, t1, g, ends


def _lattice_run(V_of_tz, g, m, t0, t1, n, w_in, c0=0.0):
    """Propagate the mode matrix (F, F') from the in-vacuum at t0 to t1 with n S6 steps.

    The kick F' -= h V_hat F is done pseudo-spectrally with the band-limited V (its |n| >= N/3 tail zeroed):
    for kept modes (|n| < N/3) this equals the Toeplitz product with V_{n-n'} masked to |n - n'| < N/3 exactly
    (no wrapped index lands on a nonzero coefficient), and FFTs avoid BLAS threading. For N_k <= 40 the same
    masked Toeplitz matrix is applied by matmul (cheaper per call at that size)."""
    k, z = g["k"], g["z"]
    Nk, N = len(k), len(z)
    h = (t1 - t0) / n
    w0 = np.sqrt(np.maximum(k * k + m * m + c0, 0.0))               # exact free flow at m^2 + c0, kick by V - c0
    w0s = np.where(w0 > 0, w0, 1.0)
    flows = []
    for a in _BM_A:
        c, s = np.cos(w0 * a * h)[:, None], np.sin(w0 * a * h)[:, None]
        sw = np.where(w0 > 0, s[:, 0] / w0s, a * h)[:, None]           # sin(w h)/w -> h at w = 0
        flows.append((c, sw, -(w0[:, None] * s)))
    offs = np.cumsum(_BM_A)[:6] * h
    F = np.diag(np.exp(-1j * w_in * t0) / np.sqrt(2 * w_in)).astype(complex)
    G = -1j * w_in[:, None] * F
    rows = np.mod(g["n"], N)                                          # FFT index of kept mode n
    sg = np.where(g["n"] % 2 == 0, 1.0, -1.0)[:, None]                # e^{i k z_j} = (-1)^n e^{2 pi i n j/N}, z_0 = -L/2
    keep_q = ~g["tail"]
    buf = np.zeros((N, Nk), dtype=complex)
    small = Nk <= 40                     # small matmuls beat FFT call overhead; larger ones go pseudo-spectral (no BLAS)
    chunk = max(1, int(2 ** 20 // (6 * max(N, Nk * Nk if small else 0))))
    tail = 0.0
    vmax = 0.0
    j = 0
    while j < n:
        nc = min(chunk, n - j)
        ts = (t0 + h * (j + np.arange(nc)))[:, None] + offs[None, :]
        Vq = np.fft.fft(_eval_V(V_of_tz, ts.ravel(), z) - c0, axis=1)
        a_tail = np.abs(Vq[:, g["tail"]])
        tail = max(tail, float(a_tail.max()) if a_tail.size else 0.0)
        vmax = max(vmax, float(np.abs(Vq).max()), abs(c0) * N)
        if small:                                                      # masked Toeplitz V_{n-n'}, |n - n'| < N/3
            M = np.where(g["band"][None], (Vq * (g["sign"] / N))[:, g["idx"]], 0.0) \
                * np.tile(np.asarray(_BM_B) * h, nc)[:, None, None]
        else:                                                          # band-limited V on the grid
            Vbl = np.fft.ifft(Vq * keep_q, axis=1).real[:, :, None]
        for s in range(nc):
            for i in range(6):
                c, sw, ws = flows[i]
                F, G = c * F + sw * G, ws * F + c * G
                if small:
                    G = G - M[6 * s + i] @ F
                else:
                    buf[rows] = sg * F
                    gk = np.fft.fft(Vbl[6 * s + i] * np.fft.ifft(buf, axis=0), axis=0)[rows]
                    G = G - (_BM_B[i] * h) * (sg * gk)
            c, sw, ws = flows[6]
            F, G = c * F + sw * G, ws * F + c * G
        j += nc
    return F, G, tail / max(vmax, 1e-300)


def _lattice_extract(F, G, t1, w_out):
    ph = np.exp(1j * w_out * t1)[:, None]
    sq = np.sqrt(w_out / 2.0)[:, None]
    Aint = sq * ph * (F + 1j * G / w_out[:, None])                    # [k, p] = alpha_pk
    Bint = sq / ph * (F - 1j * G / w_out[:, None])                    # [k, p] = beta_{p, -k}
    return Aint.T.copy(), Bint[::-1, :].T.copy()                      # [p, k]; modes sorted, so -k is the reversed index


def lattice_bogoliubov(V_of_tz, L: float, N: int, m: float, t0: float, t1: float, steps: int = 512,
                       rtol: float = 1e-7, max_steps: int = 2 ** 15, band_tol: float = 1e-9,
                       strict: bool = False, flag_rel: float = 1e-2) -> dict:
    """All-orders Bogoliubov matrices of a real scalar in 1+1 D with any band-limited V(t, z), periodic box.

    V_of_tz(t, z) returns V (energy^2) and must broadcast over numpy arrays t (column) and z (row);
    z runs over [-L/2, L/2). Steps double from `steps` until the step-halving change of beta is below
    rtol |beta| for every entry above the floor, or max_steps is reached. Output matrices are indexed
    [p_in, k_out] over the kept modes 'k' (sorted, |n| < N/3).

    Quantity: dict with 'total' = Tr beta^dag beta, the IN-IN mean number of PARTICLES in the box after
        the background has switched off (dimensionless, total, not a rate); 'pairs' = total/2 (real field);
        'n_out' = sum_p |beta_pk|^2, the in-in mean number in out-mode k; 'beta' (beta_pk; |beta_pk|^2 is
        in-mode p's share of n_out(k), at first order the mean number of pairs (k, p)); 'alpha' (IN-OUT
        scattering amplitudes among positive-frequency modes); 'vacuum_persistence' = 1/|det alpha|, the
        IN-OUT probability that nothing at all is made; the precision floor 'floor' (per entry) and
        'total_floor', 'total_relerr', 'resolved', 'band_tail', 'symplectic_error', 'steps'.
    Valid when: N even >= 8, L > 0, m >= 0, t0 < t1; V(t, z) z-independent at both window ends with
        k^2 + m^2 + V > 0 for all kept modes there and adiabatic ends; V band-limited to |q| < N/3 (2 pi/L)
        (relative tail <= band_tol); classical prescribed background (no back-reaction)."""
    L, N, m, t0, t1, g, ends = _lattice_check(V_of_tz, L, N, m, t0, t1)
    k = g["k"]
    (v_in, inh_in), (v_out, inh_out) = ends
    w2_in, w2_out = k * k + m * m + v_in, k * k + m * m + v_out
    if np.any(w2_in <= 0) or np.any(w2_out <= 0):
        raise ValueError("k^2 + m^2 + V must be > 0 for every kept mode at both window ends (no particle "
                         "interpretation otherwise; m = 0 needs V > 0 there)")
    w_in, w_out = np.sqrt(w2_in), np.sqrt(w2_out)
    wmin2 = float(min(w2_in.min(), w2_out.min()))
    inh = max(inh_in, inh_out)
    if inh > 1e-6 * wmin2:
        raise ValueError(f"V still depends on z at a window end (|V - mean| = {inh:.3g} > 1e-6 omega_min^2): "
                         "extend the window until the pattern has switched off")
    d = 1e-4 * (t1 - t0)
    eps_end = 0.0
    for t, w2 in ((t0, w2_in), (t1, w2_out)):
        vp = _eval_V(V_of_tz, np.array([t - d, t + d]), g["z"]).mean(axis=1)
        eps_end = max(eps_end, abs(vp[1] - vp[0]) / (2 * d) / (2.0 * float(w2.min()) ** 1.5))
    if eps_end > 1e-3:
        raise ValueError(f"window ends are not adiabatic (|d omega/dt|/omega^2 = {eps_end:.3g} > 1e-3): "
                         "extend the window")
    if int(steps) != steps or steps < 2 or max_steps < 2 * steps:
        raise ValueError("need integer steps >= 2 and max_steps >= 2 steps")
    end_amp = max(inh / (4 * wmin2), eps_end / 4.0)
    Nk = len(k)

    c0 = 0.5 * (v_in + v_out) if min(k * k + m * m) + 0.5 * (v_in + v_out) > 0 else 0.0   # reference shift

    def run(n):
        F, G, tail = _lattice_run(V_of_tz, g, m, t0, t1, n, w_in, c0)
        if tail > band_tol:
            raise ValueError(f"V is not band-limited to |q| < N/3 (2 pi/L): relative spectral tail {tail:.3g} > "
                             f"{band_tol:g}; raise N (or smooth V)")
        A, B = _lattice_extract(F, G, t1, w_out)
        return A, B, tail

    n = int(steps)
    _, B1, _ = run(n)
    while True:
        A2, B2, tail = run(2 * n)
        err = np.abs(B2 - B1)
        roundoff = 4.0 * _EPS * math.sqrt(6 * 2 * n * Nk) * max(1.0, float(np.abs(A2).max()))
        floor_amp = np.maximum(np.maximum(err, roundoff), end_amp)
        above = np.abs(B2) > 200 * floor_amp
        tol_amp = np.maximum(rtol * np.abs(B2), 2 * roundoff)
        converged = bool(np.all(err[above] <= tol_amp[above])) if np.any(above) else True
        if converged or 4 * n > max_steps:
            break
        n, B1 = 2 * n, B2
    b2 = np.abs(B2) ** 2
    total = float(b2.sum())
    floor = floor_amp ** 2
    total_floor = float(floor.sum())
    relerr = (2 * math.sqrt(total * total_floor) + total_floor) / total if total > 0 else math.inf
    resolved = relerr <= flag_rel
    if strict and not resolved:
        raise ValueError(f"Tr beta^dag beta = {total:.3g} is not resolved above the precision floor {total_floor:.3g} "
                         f"(relative error {relerr:.3g} > {flag_rel:g})")
    sym = float(np.abs(A2 @ A2.conj().T - B2 @ B2.conj().T - np.eye(Nk)).max())
    _, logdet = np.linalg.slogdet(A2)
    return {"k": k, "alpha": A2, "beta": B2, "beta2": b2, "n_out": b2.sum(axis=0), "total": total,
            "pairs": 0.5 * total, "floor": floor, "total_floor": total_floor, "total_relerr": relerr,
            "resolved": bool(resolved), "consistent_with_zero": total <= total_floor, "steps": 2 * n,
            "converged": converged, "band_tail": tail, "symplectic_error": sym,
            "vacuum_persistence": float(math.exp(-logdet)), "log_vacuum_persistence": float(-logdet),
            "omega_in": w_in, "omega_out": w_out, "eps_end": eps_end, "end_inhomogeneity": inh}


def lattice_born(V_of_tz, L: float, N: int, m: float, t0: float, t1: float, panels: int = None) -> dict:
    """First-order (Born) Bogoliubov coefficients on the same lattice, for comparison with lattice_bogoliubov.

    beta1_pk = (i / (2 sqrt(w_p w_k))) int dt e^{-i (w_p + w_k) t} V_{-(p+k)}(t)  (V_q: Fourier coefficient),
    by composite 16-point Gauss-Legendre in t (V_q with |q| >= N/3 taken as 0, as in the lattice solver).
    Quantity: dict with 'beta2' = |beta1_pk|^2 (first-order in-in share of out-mode k from in-mode p; at
        this order the mean number of pairs (k, p)), 'total' (first-order mean number of PARTICLES,
        dimensionless) and 'pairs' = total/2.
    Valid when: |V| << m^2 + k^2 (first order: compare with lattice_bogoliubov), V -> 0 at both window ends,
        V band-limited as for lattice_bogoliubov, and the time grid resolves V (check by doubling panels)."""
    L, N, m, t0, t1, g, ends = _lattice_check(V_of_tz, L, N, m, t0, t1)
    if m <= 0:
        raise ValueError("lattice_born needs m > 0 (the k = 0 mode has no particle interpretation at m = 0)")
    for mean, inh in ends:
        if abs(mean) + inh > 1e-6 * m * m:
            raise ValueError("Born needs V -> 0 at both window ends")
    k, n = g["k"], g["n"]
    w = np.sqrt(k * k + m * m)
    if panels is None:
        panels = int(math.ceil(4.0 * float(w.max()) * (t1 - t0) / PI)) + 8
    x, wx = np.polynomial.legendre.leggauss(16)
    edges = np.linspace(t0, t1, int(panels) + 1)
    tt = (0.5 * (edges[1:] - edges[:-1])[:, None] * x + 0.5 * (edges[1:] + edges[:-1])[:, None]).ravel()
    wt = (0.5 * (edges[1:] - edges[:-1])[:, None] * wx).ravel()
    Vh = np.fft.fft(_eval_V(V_of_tz, tt, g["z"]), axis=1) * (g["sign"] / N)      # (nt, N)
    S = -(n[:, None] + n[None, :])                                               # q = -(p + k)
    ok = np.abs(S) < N / 3.0
    Om = w[:, None] + w[None, :]
    beta = np.zeros((len(k), len(k)), dtype=complex)
    for i in range(len(k)):
        cols = np.where(ok[i])[0]
        ph = np.exp(-1j * np.outer(tt, Om[i, cols])) * wt[:, None]
        beta[i, cols] = np.sum(ph * Vh[:, np.mod(S[i, cols], N)], axis=0)
    beta *= 1j / (2 * np.sqrt(np.outer(w, w)))
    b2 = np.abs(beta) ** 2
    return {"k": k, "beta1": beta, "beta2": b2, "total": float(b2.sum()), "pairs": 0.5 * float(b2.sum())}


def pattern_potential(eps: float, n_q: int, v: float, T: float, L: float, m: float, omega: float = None,
                      ends: float = 7.5) -> dict:
    """The switched travelling pattern V(t, z) = eps exp(-t^2/(2T^2)) cos(q z - w t), q = 2 pi n_q / L, w = v |q|.

    n_q = 0 gives a homogeneous V(t) = eps exp(-t^2/2T^2) cos(omega t) (pass omega). Classification of
    the ETERNAL pattern by K = (w, q): v = 1 null (K^2 = 0: light-front momentum conserved, no pairs to
    all orders); v < 1 subluminal (spacelike; static in the frame moving with v); v > 1 superluminal
    (timelike, s = q^2 (v^2 - 1); homogeneous in the frame moving with 1/v); n_q = 0 homogeneous.
    Quantity: dict with 'V' (callable (t, z) -> energy^2), 'window' (t0, t1) = +-ends T in 1/energy,
        'kind', 's' = K^2 of the carrier (energy^2), 'q', 'omega'.
    Valid when: T > 0, L > 0, integer n_q >= 0 (q must be a box harmonic), v > 0; subluminal patterns
        need |eps| < m^2 (m^2 + V > 0 everywhere, else a static tachyonic region); ends >= 7 (the
        Gaussian leaves eps e^{-ends^2/2} at the window ends, which lattice_bogoliubov counts in its floor)."""
    eps, v, T, L, m = (_finite(x, nm) for x, nm in ((eps, "eps"), (v, "v"), (T, "T"), (L, "L"), (m, "m")))
    if int(n_q) != n_q or n_q < 0 or T <= 0 or L <= 0 or m < 0 or ends < 7:
        raise ValueError("need integer n_q >= 0, T > 0, L > 0, m >= 0 and ends >= 7")
    q = 2 * PI * int(n_q) / L
    if n_q == 0:
        if omega is None or not omega >= 0:
            raise ValueError("a homogeneous pattern (n_q = 0) needs omega >= 0")
        w, kind = float(omega), "homogeneous"
    else:
        if not v > 0:
            raise ValueError("phase velocity v must be > 0")
        w = v * q
        kind = "null" if abs(v - 1.0) < 1e-12 else ("superluminal" if v > 1 else "subluminal")
        if kind == "subluminal" and abs(eps) >= m * m:
            raise ValueError("subluminal pattern with |eps| >= m^2: m^2 + V < 0 in a static region (tachyonic "
                             "instability in its rest frame); keep |eps| < m^2")
        if kind == "null":
            w = q

    def V(t, z, eps=eps, q=q, w=w, T=T):
        return eps * np.exp(-0.5 * (np.asarray(t) / T) ** 2) * np.cos(q * np.asarray(z) - w * np.asarray(t))
    return {"V": V, "window": (-ends * T, ends * T), "kind": kind, "s": w * w - q * q, "q": q, "omega": w}


def pair_spectral_density_1p1(s, m: float):
    """Two-particle spectral density of phi^2/2 for a REAL scalar in 1+1 D: rho = 1/(2 sqrt(s (s - 4 m^2))).

    rho(K) = sum over pair states (2pi)^2 delta^2(K - p1 - p2) |<p1 p2|phi^2/2|0>|^2 = Phi_2/2, the 1+1 D
    two-body phase space Phi_2 = 1/sqrt(s (s - 4m^2)) times the identical-particle 1/2. Equals
    -4 pi d/d(m^2) of qp.pair_spectral_density_scalar (the 3+1 beta/(16 pi)).
    Quantity: rho(s) in 1/energy^2, per PAIR state; the 1+1 Born yield is N_pairs = int d^2K/(2pi)^2
        theta(K0) |V~(K)|^2 rho(K^2) (mean number of PAIRS, dimensionless; particles = 2 x pairs).
    Valid when: m > 0 and s real; returns 0 for s <= 4 m^2 (integrable 1/sqrt singularity at threshold)."""
    s = qp._arr(s, "s")
    m = _finite(m, "m")
    if m <= 0:
        raise ValueError("m must be > 0 (in 1+1 D the massless pair density is collinear-singular)")
    th = 4 * m * m
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(s > th, 0.5 / np.sqrt(np.where(s > th, s * (s - th), 1.0)), 0.0)


def born_pairs_1p1(Vtilde, m: float, s_max: float, y_max: float, n_s: int = 160, n_y: int = 160,
                   rel_step: float = 1e-3) -> dict:
    """First-order (Born) mean number of pairs of a REAL scalar in 1+1 D from V(t, z), through qp's planar formula.

    Vtilde(K0, Kz) = int dt dz e^{i(K0 t - Kz z)} V(t, z) (arrays in, complex out). 'pairs' uses
    rho_1+1(s; m^2) = -4 pi d rho_3+1/d(m^2): -4 pi d/d(m^2) of qp.born_scalar_planar(...)['pairs_per_area']
    by Richardson-extrapolated central differences (steps rel_step m^2 and twice that); 'pairs_direct'
    integrates pair_spectral_density_1p1 directly (s = 4m^2 + u^2, rapidity y); 'mismatch' compares them.
    Quantity: dict with 'pairs' (mean number of PAIRS, in-in, first order, total over all space and time,
        dimensionless), 'particles' = 2 x pairs, 'pairs_direct', 'mismatch'.
    Valid when: first order in V; m > 0; |V~| negligible for s > s_max or |y| > y_max; s_max > 4 m^2 (1 + 2 rel_step);
        the Gauss grids resolve V~ (check by doubling n_s, n_y and y_max)."""
    m, s_max, y_max = _finite(m, "m"), _finite(s_max, "s_max"), _finite(y_max, "y_max")
    if m <= 0 or not (0 < rel_step < 0.1):
        raise ValueError("need m > 0 and 0 < rel_step < 0.1")
    th = 4 * m * m
    if not s_max > th * (1 + 2 * rel_step) or not y_max > 0:
        raise ValueError("need s_max > 4 m^2 (1 + 2 rel_step) and y_max > 0")
    u, wu = qp._gauss_legendre(0.0, math.sqrt(s_max - th), n_s)
    y, wy = qp._gauss_legendre(-y_max, y_max, n_y)
    Uu, Y = np.meshgrid(u, y, indexing="ij")
    S = th + Uu * Uu
    rs = np.sqrt(S)
    # rho_1+1 ds = 2u du / (2 sqrt(s) u) = du / sqrt(s): smooth across threshold
    val = np.abs(np.asarray(Vtilde(rs * np.cosh(Y), rs * np.sinh(Y)))) ** 2 / rs
    direct = float(np.einsum("i,j,ij->", wu, wy, val) / (2 * (2 * PI) ** 2))
    m2 = m * m
    d = rel_step * m2

    def n3(mm2):
        return qp.born_scalar_planar(Vtilde, math.sqrt(mm2), s_max, y_max, "real", 0.0, n_s, n_y)["pairs_per_area"]
    d1 = (n3(m2 + d) - n3(m2 - d)) / (2 * d)
    d2 = (n3(m2 + 2 * d) - n3(m2 - 2 * d)) / (4 * d)
    pairs = -4 * PI * (4 * d1 - d2) / 3
    return {"pairs": pairs, "particles": 2 * pairs, "pairs_direct": direct,
            "mismatch": abs(pairs / direct - 1) if direct != 0 else abs(pairs)}


# ---------------------------------------------------------------- Part C: Gibbons plane-wave modes
def _H_array(H_of_U, U: np.ndarray) -> np.ndarray:
    try:
        Hs = np.asarray(H_of_U(U), dtype=float)
        if Hs.shape != (len(U), 2, 2):
            raise ValueError
    except (ValueError, TypeError, IndexError):
        Hs = np.array([np.asarray(H_of_U(float(u)), dtype=float) for u in U])
    if Hs.shape != (len(U), 2, 2) or not np.all(np.isfinite(Hs)):
        raise ValueError("H_of_U must return finite 2x2 matrices H_ij(U)")
    if np.max(np.abs(Hs - np.swapaxes(Hs, 1, 2))) > 1e-12 * max(1.0, float(np.abs(Hs).max())):
        raise ValueError("H_ij(U) must be symmetric")
    return Hs


def gibbons_jacobi(H_of_U, U_a: float, U, breaks=(), h_max: float = None, allow_caustic: bool = False) -> dict:
    """Jacobi (geodesic-deviation) matrices of the plane wave ds^2 = dU dV + H_ij X^i X^j dU^2 - dX^2.

    P'' = -H P, P(U_a) = 1, P'(U_a) = 0 and Q'' = -H Q, Q(U_a) = 0, Q'(U_a) = 1, by classical RK4 on the
    4x4 fundamental matrix (step matrices built in one batch, products by a log-depth scan), with nodes at
    every requested U and every break (place breaks where H jumps; stage points are taken one-sided).
    Quantity: dict of classical Jacobi data, each shape (len(U), 2, 2): 'P' (dimensionless), 'dP' = P'
        (1/length), 'Q' (length), 'dQ' = Q' (dimensionless), 'I' = P^{-1} Q = int_{U_a}^U (P^T P)^{-1} dU
        (length), 'S' = P' P^{-1} (symmetric, 1/length); 'detP', 'wronskian_error' = max |P^T Q' - P'^T Q - 1|,
        'first_caustic' (first U with det P <= 0, or inf). U and X are lengths, H is in 1/length^2.
    Valid when: H = 0 at and before U_a (flat in-region), U >= U_a, all U before the first caustic
        (det P > 0; refused otherwise: the Rosen chart breaks down there; allow_caustic=True keeps P, P', Q, Q'
        for classical geodesics, which pass through caustics, and sets I, S to NaN where det P = 0); H symmetric
        and piecewise smooth with its jumps listed in breaks; accuracy O(h_max^4 |H|^2) (default
        h_max = 2e-3/sqrt(max(1, |H|)))."""
    U_a = _finite(U_a, "U_a")
    U = np.atleast_1d(np.asarray(U, dtype=float))
    if not np.all(np.isfinite(U)) or np.any(U < U_a):
        raise ValueError("need finite U >= U_a")
    U_top = float(U.max())
    probe = np.linspace(U_a, max(U_top, U_a + 1e-9), 4001)
    Hp = _H_array(H_of_U, probe)
    Hmax = float(np.abs(Hp).max())
    H_a = np.abs(_H_array(H_of_U, np.array([U_a, U_a - 1e-9 * max(1.0, abs(U_a))]))).max()
    span = U_top - U_a
    if H_a > 0 and H_a * span * span > 1e-10 and H_a > 1e-10 * Hmax:   # H span^2: the deviation it would seed
        raise ValueError("H must vanish at U_a: start the integration in the flat region before the wave")
    if h_max is None:
        h_max = 2e-3 / math.sqrt(max(1.0, Hmax))
    nodes = np.unique(np.concatenate([[U_a], [b for b in breaks if U_a < b < U_top], U]))
    segs = []
    for a_, b_ in zip(nodes[:-1], nodes[1:]):
        ns = max(1, int(math.ceil((b_ - a_) / h_max)))
        segs.append(a_ + (b_ - a_) * np.arange(ns) / ns)
    if segs:
        u0 = np.concatenate(segs)
        u1 = np.concatenate([np.append(s_[1:], b_) for s_, b_ in zip(segs, nodes[1:])])
    else:
        u0 = u1 = np.zeros(0)
    h = u1 - u0
    tiny = 1e-13 * h                                     # one-sided stage points: the correct side of a jump in H

    def A(u):
        out = np.zeros((len(u), 4, 4))
        out[:, 0:2, 2:4] = np.eye(2)
        out[:, 2:4, 0:2] = -_H_array(H_of_U, u)
        return out
    I4 = np.eye(4)
    if len(h):
        A0, Am, A1 = A(u0 + tiny), A(0.5 * (u0 + u1)), A(u1 - tiny)
        hh = h[:, None, None]
        K1 = A0
        K2 = Am @ (I4 + 0.5 * hh * K1)
        K3 = Am @ (I4 + 0.5 * hh * K2)
        K4 = A1 @ (I4 + hh * K3)
        R = I4 + hh / 6.0 * (K1 + 2 * K2 + 2 * K3 + K4)
        Sc = R.copy()
        d = 1
        while d < len(Sc):                               # Hillis-Steele scan: Sc[j] = R_j ... R_0
            Sc[d:] = Sc[d:] @ Sc[:-d].copy()
            d *= 2
        Phi = np.concatenate([I4[None], Sc])            # at u0[0] = U_a, then after each step
        ugrid = np.concatenate([[u0[0]], u1])
    else:
        Phi, ugrid = I4[None], np.array([U_a])
    detP_all = Phi[:, 0, 0] * Phi[:, 1, 1] - Phi[:, 0, 1] * Phi[:, 1, 0]
    bad = np.where(detP_all <= 0)[0]
    first_caustic = float(ugrid[bad[0]]) if len(bad) else math.inf
    if np.any(U >= first_caustic) and not allow_caustic:
        raise ValueError(f"U beyond the first caustic (det P = 0 near U = {first_caustic:.6g}): the Rosen chart and "
                         "Gibbons' basis break down there; evaluate before it")
    pos = np.searchsorted(ugrid, U)
    pos = np.minimum(pos, len(ugrid) - 1)                           # every requested U is a node: exact match
    Ph = Phi[pos]
    P, Q, dP, dQ = Ph[:, 0:2, 0:2], Ph[:, 0:2, 2:4], Ph[:, 2:4, 0:2], Ph[:, 2:4, 2:4]
    detP = P[:, 0, 0] * P[:, 1, 1] - P[:, 0, 1] * P[:, 1, 0]
    safe = np.abs(detP) > 0
    Pinv = np.full_like(P, np.nan)
    Pinv[safe] = np.linalg.inv(P[safe])
    I = Pinv @ Q
    I = 0.5 * (I + np.swapaxes(I, 1, 2))
    S = dP @ Pinv
    S = 0.5 * (S + np.swapaxes(S, 1, 2))
    W = np.swapaxes(P, 1, 2) @ dQ - np.swapaxes(dP, 1, 2) @ Q
    return {"U": U, "P": P, "dP": dP, "Q": Q, "dQ": dQ, "I": I, "S": S, "Pinv": Pinv,
            "detP": detP, "wronskian_error": float(np.abs(W - np.eye(2)).max()),
            "first_caustic": first_caustic}


def gibbons_mode(U, V, X1, X2, k, c: float, m: float, H_of_U, U_a: float, breaks=()):
    """Gibbons' exact positive-frequency scalar mode in a plane wave, in Brinkmann coordinates (U, V, X).

    phi = |det P|^{-1/2} exp(i k.P^{-1}X + i c X^T P'P^{-1} X - i c V - (i/4c)(k.P^{-1}Q k + m^2 (U - U_a))),
    equal to the plane wave e^{i k.X - i c V - i (k^2 + m^2)(U - U_a)/(4c)} before the wave (U = t - z,
    V = t + z, frequency w = c + (k^2 + m^2)/(4c)).
    Quantity: complex mode function phi (dimensionless, unit-amplitude plane wave before the wave; KG norm
        2c (2pi)^3 delta^3 on U = const), broadcast over U, V, X1, X2. It is ONE in-mode, not a number of particles.
    Valid when: c > 0 (positive frequency; c < 0 modes are the complex conjugates), m >= 0, k a transverse
        2-vector (Rosen momentum, = the physical transverse momentum before the wave), U_a in the flat
        region before the wave, U_a <= U before the first caustic (see gibbons_jacobi)."""
    c, m = _finite(c, "c"), _finite(m, "m")
    if c <= 0 or m < 0:
        raise ValueError("need c > 0 (positive frequency) and m >= 0")
    k = np.asarray(k, dtype=float)
    if k.shape != (2,) or not np.all(np.isfinite(k)):
        raise ValueError("k must be a finite transverse 2-vector")
    U, V, X1, X2 = np.broadcast_arrays(*(np.asarray(a, dtype=float) for a in (U, V, X1, X2)))
    Uu, inv = np.unique(U.ravel(), return_inverse=True)
    jac = gibbons_jacobi(H_of_U, U_a, Uu, breaks)
    Pinv, S, I, det = jac["Pinv"][inv], jac["S"][inv], jac["I"][inv], jac["detP"][inv]
    X = np.stack([X1.ravel(), X2.ravel()], axis=-1)
    kx = np.einsum("ni,nij,j->n", X, np.swapaxes(Pinv, 1, 2), k)       # k.P^{-1}X = X.P^{-T}k
    quad = np.einsum("ni,nij,nj->n", X, S, X)
    kIk = np.einsum("i,nij,j->n", k, I, k)
    phase = kx + c * quad - c * V.ravel() - (kIk + m * m * (U.ravel() - U_a)) / (4 * c)
    return (np.abs(det) ** -0.5 * np.exp(1j * phase)).reshape(U.shape)


def kg_residual_brinkmann(phi, H_of_U, U, V, X1, X2, m: float, d: float = 1e-2) -> dict:
    """Finite-difference Klein-Gordon residual of a candidate mode phi(U, V, X1, X2) in the plane wave.

    In Brinkmann coordinates (g^{UV} = 2, g^{VV} = -4 X^T H X, sqrt(-g) = 1/2) the KG operator is
        (box + m^2) phi = 4 d_U d_V phi - 4 X^T H X d_V^2 phi - (d_X1^2 + d_X2^2) phi + m^2 phi,
    evaluated with 4th-order central differences of step d at each sample point.
    Quantity: dict with 'residual' = max over points of |(box + m^2) phi| / sum of the four terms' moduli
        (dimensionless; ~ (d k)^4 for an exact solution, O(1) for a wrong one) and 'per_point'.
    Valid when: phi is smooth on the stencil (no jump of H within 2d of a point; before any caustic), d small
        compared with 1/(local wavenumber); m >= 0."""
    m, d = _finite(m, "m"), _finite(d, "d")
    if m < 0 or d <= 0:
        raise ValueError("need m >= 0 and d > 0")
    U, V, X1, X2 = (np.atleast_1d(np.asarray(a, dtype=float)) for a in np.broadcast_arrays(U, V, X1, X2))
    st = np.array([-2.0, -1.0, 0.0, 1.0, 2.0]) * d
    w1 = np.array([1.0, -8.0, 0.0, 8.0, -1.0]) / (12 * d)
    w2 = np.array([-1.0, 16.0, -30.0, 16.0, -1.0]) / (12 * d * d)
    o = np.ones(5)
    UV = phi(U[:, None, None] + st[None, :, None], V[:, None, None] + st[None, None, :],
             X1[:, None, None] * o[None, :, None] * o[None, None, :], X2[:, None, None] * o[None, :, None] * o[None, None, :])
    dUdV = np.einsum("a,nab,b->n", w1, UV, w1)
    dVV = UV[:, 2, :] @ w2
    XX1 = phi(U[:, None], V[:, None], X1[:, None] + st, X2[:, None] * o) @ w2
    XX2 = phi(U[:, None], V[:, None], X1[:, None] * o, X2[:, None] + st) @ w2
    ph = UV[:, 2, 2]
    Hs = _H_array(H_of_U, U)
    X = np.stack([X1, X2], axis=-1)
    hX = np.einsum("ni,nij,nj->n", X, Hs, X)
    terms = [4 * dUdV, -4 * hX * dVV, -(XX1 + XX2), m * m * ph]
    R = np.abs(sum(terms)) / np.maximum(sum(np.abs(t) for t in terms), 1e-300)
    return {"residual": float(R.max()), "per_point": R}


def square_pulse_geodesic(A0: float, a: float, U, X0) -> dict:
    """Closed-form geodesics of the '+' square pulse (Chakraborty & Kar 2022, eqs. 8, 14-17).

    H = diag(A0^2, -A0^2) for -a <= U <= a (their A+ = 2 A0^2 with x'' = -(1/2) A+ x), zero elsewhere;
    a particle at rest before the pulse at X0 = (x0, y0):
        x = x0 cos(A0 (U + a)), y = y0 cosh(A0 (U + a)) inside; after (U >= a):
        x = x0 [cos(2 a A0) - A0 (U - a) sin(2 a A0)], y = y0 [cosh(2 a A0) + A0 (U - a) sinh(2 a A0)].
    Quantity: dict with 'X' (transverse position, length) and 'dX_dU' (= dX/dtau, transverse velocity in
        units of c, for a particle at rest before the pulse, since dU/dtau = 1 is conserved).
    Valid when: A0 >= 0, a > 0; '+' polarization; exact (no approximation)."""
    A0, a = _finite(A0, "A0"), _finite(a, "a")
    if A0 < 0 or a <= 0:
        raise ValueError("need A0 >= 0 and a > 0")
    U = np.atleast_1d(np.asarray(U, dtype=float))
    x0, y0 = (float(v) for v in np.asarray(X0, dtype=float))
    th = A0 * (np.clip(U, -a, a) + a)
    after = U > a
    du = np.where(after, U - a, 0.0)
    cx, sx = np.cos(th), np.sin(th)
    cy, sy = np.cosh(th), np.sinh(th)
    x = x0 * np.where(after, cx - A0 * du * sx, cx)
    y = y0 * np.where(after, cy + A0 * du * sy, cy)
    inside = (U >= -a) & (U <= a)
    vx = x0 * np.where(after | inside, -A0 * sx, 0.0)
    vy = y0 * np.where(after | inside, A0 * sy, 0.0)
    return {"X": np.stack([x, y], axis=-1), "dX_dU": np.stack([vx, vy], axis=-1)}


def velocity_memory(H_of_U, X0, U_a: float, U_b: float, breaks=()) -> dict:
    """Velocity and displacement memory of a test particle at rest before a plane wave (exact, from Jacobi).

    A particle at rest at transverse position X0 before the wave follows X(U) = P(U) X0; dU/dtau = 1 is
    conserved, so its transverse velocity is dX/dtau = P'(U) X0 (constant once the wave has passed).
    Also returned: the first-order (weak-wave) formula -(int_{U_a}^{U_b} H dU) X0.
    Quantity: dict with 'velocity' (dX/dtau after the wave, units of c: classical, exact), 'displacement'
        ((P - 1) X0, length), 'velocity_first_order' (weak-wave approximation, units of c).
    Valid when: U_b after the wave (otherwise the instantaneous dX/dU at U_b); caustics are allowed (geodesics
        cross them); H = 0 at U_a; breaks list the jumps of H."""
    X0 = np.asarray(X0, dtype=float)
    if X0.shape != (2,) or not np.all(np.isfinite(X0)):
        raise ValueError("X0 must be a finite transverse 2-vector")
    jac = gibbons_jacobi(H_of_U, U_a, [U_b], breaks, allow_caustic=True)
    pts = np.unique(np.concatenate([[U_a], [b for b in breaks if U_a < b < U_b], [U_b]]))
    intH = np.zeros((2, 2))
    xg, wg = np.polynomial.legendre.leggauss(16)
    for a_, b_ in zip(pts[:-1], pts[1:]):
        # composite 16-point Gauss panels of width <= 0.25 (profiles vary on scales >~ 1 in the self-test; refine
        # by passing breaks at sharp features)
        panels = max(4, int(math.ceil((b_ - a_) / 0.25)))
        e = np.linspace(a_, b_, panels + 1)
        x = (0.5 * (e[1:] - e[:-1])[:, None] * xg + 0.5 * (e[1:] + e[:-1])[:, None]).ravel()
        w = (0.5 * (e[1:] - e[:-1])[:, None] * wg).ravel()
        intH += np.einsum("n,nij->ij", w, _H_array(H_of_U, x))
    return {"velocity": jac["dP"][0] @ X0, "displacement": jac["P"][0] @ X0 - X0,
            "velocity_first_order": -intH @ X0, "P": jac["P"][0], "dP": jac["dP"][0]}


def _packet_closed_form(jac_one, X1, X2, c, m, X0, sigma, k0, U, U_a):
    """psi(U, X) of the Gaussian in-packet int d^2k g(k) phi_k e^{+icV}, g = exp(-sigma^2|k-k0|^2/2 - i k.X0)."""
    Pinv, S, I, det = jac_one["Pinv"], jac_one["S"], jac_one["I"], jac_one["detP"]
    X = np.stack([X1, X2], axis=-1)
    A = sigma ** 2 * np.eye(2) + 0.5j / c * I
    Ainv = np.linalg.inv(A)
    lam = np.linalg.eigvalsh(I)
    sqrt_detA = np.prod(np.sqrt(sigma ** 2 + 0.5j * lam / c))     # each factor has Re > 0: principal branch
    b = sigma ** 2 * k0 + 1j * (X @ Pinv.T - X0)                     # P^{-1}X as a row vector: X @ P^{-T}
    expo = 0.5 * np.einsum("...i,ij,...j->...", b, Ainv, b) - 0.5 * sigma ** 2 * float(k0 @ k0)
    quad = np.einsum("...i,ij,...j->...", X, S, X)
    return (abs(det) ** -0.5 * (2 * PI / sqrt_detA) * np.exp(expo + 1j * c * quad - 1j * m * m * (U - U_a) / (4 * c)))


def gibbons_packet(H_of_U, U_a: float, U_b: float, c: float, m: float, X0, sigma: float, k0=(0.0, 0.0),
                   breaks=(), n_grid: int = 128, n_V: int = 8, half_width: float = None) -> dict:
    """An exact Gaussian packet of Gibbons in-modes, projected onto Minkowski out-modes on the null surface U = U_b.

    In-packet: Psi = int d^2k g(k) phi_{k,c}, g = exp(-sigma^2 |k - k0|^2/2 - i k.X0): before the wave a
    Gaussian of width sigma at X0 with transverse momentum k0 and light-front momentum c. After the wave
    (U_b, flat) it is projected with the null-surface KG product i int dV d^2X (f* d_V g - g d_V f*) onto
    out-modes e^{i p.X - i c' V} (c' > 0, alpha) and their conjugates (beta), by FFT over a periodic V-cell
    of n_V points (period 2 pi/c) and the X-grid.
    Quantity: dict with 'alpha_norm' (= sum |alpha|^2 / incoming KG norm: fraction of the packet in
        positive-frequency out-modes; 1 for unitarity), 'beta_norm' (= sum_k |beta_{packet,k}|^2 / incoming
        norm: this normalized in-mode's contribution to the in-in out-particle number <in|N_out|in>, i.e. its
        overlap with negative-frequency out-modes; Gibbons: exactly 0), 'p_mean' (mean transverse
        momentum after the wave, energy), 'p_mean_classical' = 2c P' X0 + Q' k0, 'X_mean',
        'X_mean_classical' = P X0 + Q k0/(2c), 'grid' and 'psi' (the packet on the X-grid at U_b).
    Valid when: c > 0, sigma > 0, m >= 0, U_a in the flat region before the wave, U_b after it (or anywhere for
        the mean values) and before the first caustic; the X-grid holds the packet and resolves its local
        transverse momentum (refused otherwise: raise n_grid)."""
    c, m, sigma = _finite(c, "c"), _finite(m, "m"), _finite(sigma, "sigma")
    if c <= 0 or m < 0 or sigma <= 0:
        raise ValueError("need c > 0, m >= 0 and sigma > 0")
    if int(n_grid) != n_grid or n_grid < 16 or n_grid % 2 or int(n_V) != n_V or n_V < 4:
        raise ValueError("need even n_grid >= 16 and n_V >= 4")
    X0, k0 = np.asarray(X0, dtype=float), np.asarray(k0, dtype=float)
    if X0.shape != (2,) or k0.shape != (2,):
        raise ValueError("X0 and k0 must be transverse 2-vectors")
    jac = gibbons_jacobi(H_of_U, U_a, [U_b], breaks)
    one = {key: jac[key][0] for key in ("Pinv", "S", "I", "detP", "P", "dP", "Q", "dQ")}
    Xcl = one["P"] @ X0 + one["Q"] @ k0 / (2 * c)
    pcl = 2 * c * one["dP"] @ X0 + one["dQ"] @ k0
    A = sigma ** 2 * np.eye(2) + 0.5j / c * one["I"]
    # psi ~ exp(-(1/2) (X - Xc)^T Gam (X - Xc) + i p.X): |psi|^2 has covariance (2 Re Gam)^{-1}, |psi~(p)|^2 (2 Re Gam^{-1})^{-1}
    Gam = one["Pinv"].T @ np.linalg.inv(A) @ one["Pinv"] - 2j * c * one["S"]
    Gam = 0.5 * (Gam + Gam.T)
    ev_x, ev_p = np.linalg.eigvalsh(np.real(Gam)), np.linalg.eigvalsh(np.real(np.linalg.inv(Gam)))
    if np.any(ev_x <= 0) or np.any(ev_p <= 0):
        raise ValueError("the packet is not a normalizable Gaussian at U_b (check U_b, sigma and the caustic)")
    std, std_p = 1.0 / np.sqrt(2.0 * ev_x), 1.0 / np.sqrt(2.0 * ev_p)
    if half_width is None:
        half_width = 7.0 * float(std.max())                           # |psi|^2 mass beyond 7 std: ~3e-12
    dx = 2 * half_width / n_grid
    p_need = float(np.abs(pcl).max()) + 7.0 * float(std_p.max())
    if p_need > 0.9 * PI / dx:
        raise ValueError(f"X-grid too coarse: needs |p| up to {p_need:.3g} but resolves {PI / dx:.3g}; raise n_grid")
    x1 = Xcl[0] + dx * (np.arange(n_grid) - n_grid // 2)
    x2 = Xcl[1] + dx * (np.arange(n_grid) - n_grid // 2)
    G1, G2 = np.meshgrid(x1, x2, indexing="ij")
    psi = _packet_closed_form(one, G1, G2, c, m, X0, sigma, k0, U_b, U_a)
    Vg = (2 * PI / c) * np.arange(n_V) / n_V                        # one period of e^{-icV}
    Psi = np.exp(-1j * c * Vg)[:, None, None] * psi[None]
    coef = np.fft.fftn(Psi) / n_V                                     # V-bin j holds e^{-i c' V} with c' = -j c
    cprime = -np.fft.fftfreq(n_V, 1.0 / n_V) * c
    # null-surface KG norm per unit V-length of a component e^{-i c' V} psi'(X): 2 |c'| int |psi'|^2 d^2X,
    # with int |psi'|^2 d^2X = dx^2 sum_X |psi'|^2 = (dx/n_grid)^2 sum_p |FFT_X psi'|^2 (Parseval)
    w_c = 2 * np.abs(cprime) * (dx / n_grid) ** 2 * np.sum(np.abs(coef) ** 2, axis=(1, 2))
    norm_in = 2 * c * 4 * PI ** 3 / sigma ** 2                        # 2c int |(2pi/sigma^2) e^{-|X-X0|^2/2sigma^2}|^2 d^2X
    alpha_norm = float(w_c[cprime > 0].sum()) / norm_in               # positive-frequency out-modes
    beta_norm = float(w_c[cprime < 0].sum()) / norm_in                # negative-frequency out-modes (particles)
    p1 = 2 * PI * np.fft.fftfreq(n_grid, dx)
    prob = np.abs(np.fft.fft2(psi)) ** 2
    P1, P2 = np.meshgrid(p1, p1, indexing="ij")
    pm = np.array([np.sum(P1 * prob), np.sum(P2 * prob)]) / np.sum(prob)
    dens = np.abs(psi) ** 2
    xm = np.array([np.sum(G1 * dens), np.sum(G2 * dens)]) / np.sum(dens)
    return {"alpha_norm": alpha_norm, "beta_norm": beta_norm, "p_mean": pm, "p_mean_classical": pcl,
            "X_mean": xm, "X_mean_classical": Xcl, "grid": (x1, x2), "psi": psi,
            "jacobi": one, "wronskian_error": jac["wronskian_error"]}


def _lightfront_splitstep(H_of_U, U_a, U_b, c, m, psi0, x1, x2, steps, breaks=()):
    """Independent check: i d_U psi = [-lap/(4c) + c X^T H X + m^2/(4c)] psi by S6 split-step Fourier."""
    dx1, dx2 = x1[1] - x1[0], x2[1] - x2[0]
    p1 = 2 * PI * np.fft.fftfreq(len(x1), dx1)
    p2 = 2 * PI * np.fft.fftfreq(len(x2), dx2)
    Kin = (p1[:, None] ** 2 + p2[None, :] ** 2 + m * m) / (4 * c)
    G1, G2 = np.meshgrid(x1, x2, indexing="ij")
    XX = (c * G1 * G1, 2 * c * G1 * G2, c * G2 * G2)
    pts = np.unique(np.concatenate([[U_a], [b for b in breaks if U_a < b < U_b], [U_b]]))
    psi = np.fft.fft2(psi0.astype(complex))                         # kept in momentum space between kicks
    for a_, b_ in zip(pts[:-1], pts[1:]):
        ns = max(1, int(round(steps * (b_ - a_) / (U_b - U_a))))
        h = (b_ - a_) / ns
        kin = [np.exp(-1j * a * h * Kin) for a in _BM_A]
        offs = np.cumsum(_BM_A)[:6] * h
        Hs = _H_array(H_of_U, (a_ + h * np.arange(ns)[:, None] + offs[None, :]).ravel()).reshape(ns, 6, 2, 2)
        for j in range(ns):
            for i in range(6):
                Vx = Hs[j, i, 0, 0] * XX[0] + Hs[j, i, 0, 1] * XX[1] + Hs[j, i, 1, 1] * XX[2]
                psi = np.fft.fft2(np.exp(-1j * _BM_B[i] * h * Vx) * np.fft.ifft2(kin[i] * psi))
            psi = kin[6] * psi
    return np.fft.ifft2(psi)


# ---------------------------------------------------------------- self-test
def selftest(verbose: bool = True) -> bool:
    """Compare with closed forms, an independent solver, published results and exact limits. True if all pass."""
    results = []

    def check(name, got, want, tol, rel=False):
        err = abs(got - want) / (abs(want) if rel and want != 0 else 1.0)
        ok = bool(err <= tol)
        results.append(ok)
        if verbose:
            print(f"{'PASS' if ok else 'FAIL'}  {name}: {got:.10g} (expected {want:.10g}, {'rel' if rel else 'abs'} tol {tol:g})")

    def plus(prof):           # '+' polarization H = prof(U) diag(1, -1), vectorised
        return lambda U: np.multiply.outer(prof(np.asarray(U, dtype=float)), np.diag([1.0, -1.0]))

    # ============ PART C: Gibbons' plane sandwich wave (cheap, first) ============
    # C1. Square pulse, Chakraborty & Kar 2022 (arXiv:2202.10661) eq. 8 "A+(u) = 2 A2 0[Θ( u + a) − Θ( u − a)]",
    #     eqs. 14-15 "¨x + 1 2A+(u)x = 0 (14) ¨y − 1 2 A+(u)y = 0 (15)" (PDF extraction drops the fraction bar and the
    #     superscript: x'' + (1/2) A+ x = 0, so H = diag(A0^2, -A0^2) on |U| <= a), and their closed-form geodesics,
    #     eqs. 16-17: "x(u) = α u ≤ −a α cos[A0(u + a)] −a ≤ u ≤ a αA0(a − u) sin[2aA0] + α cos[2aA0] u ≥ a (16)",
    #     "y(u) = β u ≤ −a β cosh[A0(u + a)] −a ≤ u ≤ a βA0(u − a) sinh[2aA0] + β cosh[2aA0] u ≥ a (17)" (a piecewise
    #     definition flattened by the extraction; encoded in square_pulse_geodesic).
    #     Tolerance 1e-11: RK4 with h = 2e-3 on a piecewise-constant H (jumps on nodes) errs ~1e-13 over the run.
    A0, a = 0.5, 1.0
    Hsq = plus(lambda U: A0 ** 2 * ((U >= -a) & (U <= a)))
    Us = np.array([-0.3, 0.7, 1.0, 1.6, 2.0])
    X0 = np.array([0.5, 0.3])
    jac = gibbons_jacobi(Hsq, -2.0, Us, breaks=(-a, a))
    ck = square_pulse_geodesic(A0, a, Us, X0)
    check("square pulse: Jacobi P X0, P' X0 vs Chakraborty & Kar eqs. 16-17 (max abs error)",
          float(max(np.abs(np.einsum("nij,j->ni", jac["P"], X0) - ck["X"]).max(),
                    np.abs(np.einsum("nij,j->ni", jac["dP"], X0) - ck["dX_dU"]).max())), 0.0, 1e-11)
    check("Jacobi: Wronskian P^T Q' - P'^T Q = 1 (symplectic, max abs error)", jac["wronskian_error"], 0.0, 1e-11)

    # C2. Strong smooth wave where the weak-wave memory formula fails: x'' = -(2/w^2) sech^2(U/w) x has the exact
    #     solution x = -x0 tanh(U/w) (check: x'' = 2 sech^2 tanh/w^2 x0), so a particle at rest before the wave
    #     ends at rest at -x0: zero velocity memory along x, although -x0 int H dU = -4 x0/w (first order). Compare
    #     Chakraborty & Kar 2022, p. 9: "In general, pulse proﬁles satisfying ∫ +∞ −∞ A+(u)du ⁄= 0, always have nonzero
    #     velocity memory [39, 40]" - true at first order and off the axis, not for this strong profile on the x axis.
    #     Tolerances: RK4 global error ~1e-13 over U in [-20, 20] (h = 2e-3/sqrt(2)); GL quadrature of sech^2 ~1e-15.
    w = 1.0
    Hpt = plus(lambda U: 2.0 / w ** 2 / np.cosh(U / w) ** 2)
    vm = velocity_memory(Hpt, X0, -20.0, 20.0)
    jp = gibbons_jacobi(Hpt, -20.0, [-1.0, 0.5, 3.0], allow_caustic=True)
    check("sech^2 profile: Jacobi P_xx = -tanh(U/w) at U = -1, 0.5, 3 (max abs error)",
          float(np.abs(jp["P"][:, 0, 0] + np.tanh(np.array([-1.0, 0.5, 3.0]) / w)).max()), 0.0, 1e-11)
    check("sech^2 profile: exact velocity memory along x is 0 (reflectionless)", float(vm["velocity"][0]), 0.0, 1e-11)
    check("... while the first-order memory -x0 int H dU = -4 x0/w is O(1): first order fails at strong field",
          float(vm["velocity_first_order"][0]), -4.0 * X0[0] / w, 1e-12, rel=True)

    # C3. Weak-wave limit: velocity memory -> -(int H dU) X0 (first order); the deviation is O(h0^2), so it drops
    #     4x when h0 halves. Gaussian '+' profile h0 exp(-U^2/2).
    devs = []
    for h0 in (0.02, 0.01):
        vg = velocity_memory(plus(lambda U, h0=h0: h0 * np.exp(-0.5 * U * U)), X0, -9.0, 9.0)
        devs.append(float(np.abs(vg["velocity"] - vg["velocity_first_order"]).max() / np.abs(vg["velocity_first_order"]).max()))
    check(f"weak wave: velocity memory -> -X0 int H dU, deviation {devs[0]:.2e} at h0 = 0.02 is O(h0) relative "
          "(ratio for h0 halving in [1.8, 2.2])", devs[0] / devs[1], 2.0, 0.2)

    # C4. Gibbons' modes solve the Klein-Gordon equation: 4th-order finite differences of the exact mode in Brinkmann
    #     coordinates, both polarizations (Gaussian profile, H = h0 e^{-U^2/2}[[cos, sin], [sin, -cos]](0.6)), k != 0,
    #     inside and after the wave (before the caustic). FD truncation (d k)^4/90 with d = 1e-2: < 1e-8; the
    #     tolerance 1e-7 leaves room for roundoff ~1e-12/d^2. The flat-space plane wave at the same points must FAIL
    #     (residual > 1e-3), so the check has teeth.
    th = 0.6
    Hx = lambda U: np.multiply.outer(0.2 * np.exp(-0.5 * np.asarray(U, dtype=float) ** 2),   # noqa: E731
                                     np.array([[math.cos(th), math.sin(th)], [math.sin(th), -math.cos(th)]]))
    kk, cc = np.array([0.7, -0.4]), 0.6
    Up, Vp = np.array([0.3, -0.8, 1.2]), np.array([0.2, 1.0, -0.4])
    X1p, X2p = np.array([0.8, -1.1, 0.4]), np.array([-0.5, 0.9, 1.2])
    res = kg_residual_brinkmann(lambda U, V, x, y: gibbons_mode(U, V, x, y, kk, cc, 1.0, Hx, -7.5), Hx, Up, Vp, X1p, X2p, 1.0)
    flat = kg_residual_brinkmann(lambda U, V, x, y: np.exp(1j * (kk[0] * x + kk[1] * y - cc * V
                                                              - (kk @ kk + 1.0) * (U + 7.5) / (4 * cc))), Hx, Up, Vp, X1p, X2p, 1.0)
    check("Gibbons mode (+ and x polarization): relative KG residual by finite differences", res["residual"], 0.0, 1e-7)
    check(f"... the flat-space plane wave fails the same test (residual {flat['per_point'].min():.2g} > 1e-3)",
          float(flat["per_point"].min() > 1e-3), 1.0, 0)

    # C5. beta = 0 by explicit projection: an exact Gaussian packet of in-modes (c = 1, sigma = 1, at X0) through the
    #     square pulse, projected on U_b = 1.25 onto Minkowski out-modes (FFT over V and X). Gibbons 1975 p. 198:
    #     "we see that only solutions with the same c ... fail to be orthogonal. Thus the coefficients ... connecting
    #     any two bases (defined by their corresponding charts) vanish" (the omitted parts, a_ij(u) and the beta
    #     symbols, are garbled by the PDF extraction) and "The final result is the same: no matter how strong the
    #     wave-no particle creation takes place." Velocity memory: Elbistan et al. 2023 (arXiv:2306.14271) abstract,
    #     "Particles at rest before the arrival of a burst of gravitational wave move, after the wave has passed, with
    #     constant velocity along diverging geodesics." Tolerances: beta is roundoff (FFT of a single V-harmonic,
    #     ~1e-32); the alpha norm misses the |psi|^2 tail beyond 7 std (~1e-12); <p> is exact (Ehrenfest) up to
    #     the RK4 Jacobi error (~1e-13) and the grid tail (~1e-11).
    A0s, a_s = 0.3, 1.0
    Hs = plus(lambda U: A0s ** 2 * ((U >= -a_s) & (U <= a_s)))
    pk = gibbons_packet(Hs, -1.25, 1.25, 1.0, 1.0, X0, 1.0, breaks=(-a_s, a_s), n_grid=64)
    v_ck = square_pulse_geodesic(A0s, a_s, [1.25], X0)["dX_dU"][0]
    check("projection: in-packet weight in NEGATIVE-frequency out-modes (in-in particles per incoming particle)",
          pk["beta_norm"], 0.0, 1e-25)
    check("projection: weight in positive-frequency out-modes = incoming KG norm (unitary alpha)", pk["alpha_norm"], 1.0, 1e-10)
    check("quantum kick = classical memory: packet <p_perp> after the wave vs 2c x (C&K eq. 16-17 velocity), max abs",
          float(np.abs(pk["p_mean"] - 2 * 1.0 * v_ck).max()), 0.0, 1e-9)
    check(f"... and the kick is not zero (|<p_perp>| = {np.linalg.norm(pk['p_mean']):.3f} vs 0 before)",
          float(np.linalg.norm(pk["p_mean"]) > 0.05), 1.0, 0)

    # C6. The exact packet against an INDEPENDENT numerical solution of the light-front Schroedinger equation
    #     i d_U psi = [-lap/(4c) + c X^T H X + m^2/(4c)] psi (split-step Fourier, S6, 100 steps), on a periodic box
    #     1.5 x wider than the projection grid (same spacing) so that the packet's tail does not wrap (on the
    #     +-7 std grid it does, at the 2e-6 level). Tolerance 1e-10: measured 6e-13 (S6 time error at 100 steps and
    #     the remaining tail wrap are both below it).
    x1, x2 = pk["grid"]
    dxp = x1[1] - x1[0]
    xb1 = pk["X_mean_classical"][0] + dxp * (np.arange(96) - 48)
    xb2 = pk["X_mean_classical"][1] + dxp * (np.arange(96) - 48)
    G1, G2 = np.meshgrid(xb1, xb2, indexing="ij")
    psi0 = (2 * PI) * np.exp(-((G1 - X0[0]) ** 2 + (G2 - X0[1]) ** 2) / 2.0)
    ps = _lightfront_splitstep(Hs, -1.25, 1.25, 1.0, 1.0, psi0, xb1, xb2, 100, breaks=(-a_s, a_s))
    ex = _packet_closed_form(pk["jacobi"], G1, G2, 1.0, 1.0, X0, 1.0, np.zeros(2), 1.25, -1.25)
    check("exact Gibbons packet vs split-step Fourier solution (relative L2 difference)",
          float(np.linalg.norm(ps - ex) / np.linalg.norm(ex)), 0.0, 1e-10)

    # ============ PART A: lattice solver against an independent solver and closed forms ============
    m, L, N = 1.0, 16 * PI, 36                   # k_c = 1.375 m, 23 modes
    # A1. Homogeneous V(t) = eps e^{-t^2/2T^2} cos(t), eps = 0.3 m^2: modes decouple, so the lattice's beta_{p,-p} must
    #     equal qp.bogoliubov_boson per mode (an independent 2x2 Magnus solver). Tolerance 1e-6 relative on resolved
    #     modes: the lattice runs at rtol 1e-6 on beta, a conservative step-halving estimate (the finer run's error is
    #     ~1/16 of it), qp at 1e-7; measured agreement 2e-8.
    hom = pattern_potential(0.3, 0, 0.0, 8.0, L, m, omega=1.0)
    rh = lattice_bogoliubov(hom["V"], L, N, m, *hom["window"], rtol=1e-6, steps=1024)
    kl = rh["k"]
    ref = qp.bogoliubov_boson(lambda t: kl * kl + m * m + hom["V"](t, 0.0), *hom["window"])
    b_pp = np.abs(rh["beta"][np.arange(len(kl)), np.arange(len(kl))[::-1]]) ** 2      # beta_{p,-p}
    good = ref["resolved"] & (ref["beta2"] > 1e-12)
    check("homogeneous V(t), eps = 0.3 m^2: lattice |beta_{p,-p}|^2 vs qp.bogoliubov_boson (max rel., resolved modes)",
          float(np.max(np.abs(b_pp[good] / ref["beta2"][good] - 1))), 0.0, 1e-6)
    offd = rh["beta2"].copy()
    offd[np.arange(len(kl)), np.arange(len(kl))[::-1]] = 0.0
    check("homogeneous V(t): no k-mixing (off-anti-diagonal sum |beta|^2 below the floor)",
          float(offd.sum() <= rh["total_floor"]), 1.0, 0)
    #     In-out vacuum persistence 1/|det alpha| = prod over modes of 1/|alpha_p| (qp: 'vacuum_persistence_mode' =
    #     1/|alpha_k|^2 per PAIR (k, -k); the k = 0 mode is single). Tolerance 1e-8 relative.
    vp_qp = float(np.prod(np.sqrt(ref["vacuum_persistence_mode"])))
    check("in-out vacuum persistence 1/|det alpha| = prod_p 1/|alpha_p| from qp", rh["vacuum_persistence"], vp_qp, 1e-8, rel=True)
    #     First order fails here by tens of orders of magnitude: the carrier (w = 1 < 2m) cannot make a pair, so
    #     first-order Born sees only the envelope's tail, while the exact yield comes from two-quantum absorption.
    rb = lattice_born(hom["V"], L, N, m, *hom["window"])
    check(f"... at this amplitude first-order Born is clearly wrong: Born/exact = {rb['total'] / rh['total']:.1e} (< 1e-20)",
          float(rb["total"] / rh["total"] < 1e-20), 1.0, 0)

    # A2. Tanh model (in/out masses differ), homogeneous V = m^2 (B tanh(rho t) - B) + 2B m^2... i.e. omega^2 =
    #     k^2 + m^2 (A + B tanh(rho t)) with A = 2, B = 1: arXiv:2204.02786 (Birrell & Davies sec. 3.4) eq. 3.133
    #     "a2(η) =A +B tanh(ρη)" and eq. 3.140b "|βk|2 = sinh2(πω−/ρ) sinh(πω1/ρ) sinh(πω2/ρ)" [extraction drops the
    #     fraction bar: sinh^2(pi w_-/rho) / (sinh(pi w1/rho) sinh(pi w2/rho))], via qp.tanh_model_beta2.
    #     Tolerance 1e-6 relative (solver rtol 1e-7 on beta; measured 1e-8).
    rho = 2.0
    rt = lattice_bogoliubov(lambda t, z: (1.0 + np.tanh(rho * np.asarray(t))) * m * m + 0.0 * np.asarray(z),
                            L, N, m, -25.0 / rho, 25.0 / rho)
    tb = np.abs(rt["beta"][np.arange(len(kl)), np.arange(len(kl))[::-1]]) ** 2
    exact = qp.tanh_model_beta2(kl, m, 2.0, 1.0, rho)
    check("tanh model through the lattice vs Bernard-Duncan closed form (eq. 3.140b), max rel. over 23 modes",
          float(np.max(np.abs(tb / exact - 1))), 0.0, 1e-6)

    # ============ PART B: null, subluminal and superluminal patterns at the same amplitude ============
    # B1. Superluminal (v = 2.5, s = 5.25 m^2 > 4 m^2): timelike support; the lattice pair (1.125, -0.125) m is
    #     resonant within 0.013 m, so the number must be resolved and GROW with the switching time (a rate; measured
    #     7.2 and 17.8 particles at T = 6 and 10/m), unlike B2-B3. At this eps first order fails here too (exact/Born
    #     2.2 at T = 10: parametric amplification of the resonant pair). The symplectic identity holds to roundoff
    #     (exact splitting factors), and the S6 coefficients are 4th order (step-halving error ratio in [12, 20]).
    sup = pattern_potential(0.3, 8, 2.5, 6.0, L, m)
    rs = lattice_bogoliubov(sup["V"], L, N, m, *sup["window"])
    sup10 = pattern_potential(0.3, 8, 2.5, 10.0, L, m)
    rs10 = lattice_bogoliubov(sup10["V"], L, N, m, *sup10["window"], rtol=1e-6)
    check(f"superluminal pattern (v = 2.5): Tr beta^dag beta = {rs['total']:.4g} -> {rs10['total']:.4g} particles for "
          f"T = 6 -> 10/m: resolved, >> floor, growing (ratio > 2)",
          float(rs["resolved"] and rs10["resolved"] and rs["total"] > 1e6 * rs["total_floor"]
                and rs10["total"] > 2 * rs["total"]), 1.0, 0)
    rb10 = lattice_born(sup10["V"], L, N, m, *sup10["window"])
    check(f"... and first-order Born is clearly wrong at this amplitude: exact/Born = {rs10['total'] / rb10['total']:.3f} (> 1.5)",
          float(rs10["total"] / rb10["total"] > 1.5), 1.0, 0)
    check("superluminal: alpha alpha^dag - beta beta^dag = 1 (max abs; exactly symplectic steps)", rs["symplectic_error"], 0.0, 1e-10)
    g = _lattice_grid(L, N)
    win = np.sqrt(g["k"] ** 2 + m * m)
    Bs = [_lattice_extract(*_lattice_run(sup["V"], g, m, *sup["window"], n, win)[:2], sup["window"][1], win)[1]
          for n in (200, 400, 800)]
    ratio = float(np.abs(Bs[1] - Bs[0]).max() / np.abs(Bs[2] - Bs[1]).max())
    check(f"S6 splitting is 4th order: step-halving error ratio {ratio:.2f} (in [12, 20])", ratio, 16.0, 4.0)
    #     lattice_born (first-order formula, a time quadrature) against the all-orders lattice at weak amplitude
    #     eps = 0.01 m^2: the difference is O(eps^2) relative, enhanced by the resonant pair's parametric gain
    #     (measured 3.4e-4 here; 3.1e-4 and 7.8e-5 at eps = 0.01 and 0.005 for the non-resonant v = 3): tol 10 eps^2.
    weak = pattern_potential(0.01, 8, 2.5, 6.0, L, m)
    rw = lattice_bogoliubov(weak["V"], L, N, m, *weak["window"])
    bw = lattice_born(weak["V"], L, N, m, *weak["window"])
    check("weak superluminal pattern (eps = 0.01 m^2): lattice / lattice_born - 1", rw["total"] / bw["total"] - 1, 0.0, 1e-3)

    # B2. NULL pattern (v = 1), same eps, switched slowly (T = 26/m): light-front momentum conservation; zero to the
    #     floor, although the same eps makes particles homogeneously (A1) and superluminally (B1). Gibbons 1975, abstract
    #     (p. 191): "the time varying gravitational field of the wave produces no particles", and p. 192: "is analogous
    #     to the corresponding result for electro- magnetic waves proved by Schwinger [7]". The wave still acts: alpha differs
    #     from 1 (phase shifts) while beta = 0. Faster switching leaks (a packet): 6e-7, 2e-11, 7e-16, 2e-20, 8e-25
    #     at T = 6, 10, 14, 18, 22/m; at T = 26 Tr is at the noise level (~3e-26), below the floor (a roundoff bound).
    nul = pattern_potential(0.3, 8, 1.0, 26.0, L, m)
    rn = lattice_bogoliubov(nul["V"], L, N, m, *nul["window"], steps=512)
    check(f"null pattern V(t - z), eps = 0.3 m^2: Tr beta^dag beta = {rn['total']:.2e} <= floor {rn['total_floor']:.2e}",
          float(rn["consistent_with_zero"]), 1.0, 0)
    check(f"... yet the wave acts on particles: max |alpha_pk - delta_pk| = {np.abs(rn['alpha'] - np.eye(len(kl))).max():.3f} > 1e-3",
          float(np.abs(rn["alpha"] - np.eye(len(kl))).max() > 1e-3), 1.0, 0)
    # B3. Subluminal pattern (v = 0.5, m^2 + V > 0): static in its rest frame (spacelike support, gap >= 2m - 0.5 m
    #     per quantum), so it reaches the floor already at T = 14/m (measured 1e-26).
    sub = pattern_potential(0.3, 8, 0.5, 14.0, L, m)
    rsub = lattice_bogoliubov(sub["V"], L, N, m, *sub["window"], steps=512)
    check(f"subluminal pattern (v = 0.5): Tr beta^dag beta = {rsub['total']:.2e} <= floor {rsub['total_floor']:.2e}",
          float(rsub["consistent_with_zero"]), 1.0, 0)

    # B4. Weak superluminal PACKET V = eps exp(-t^2/2T^2 - z^2/2W^2) cos(q z - w t) (q = 1, w = 3, T = 2, W = 2.5) in a
    #     big box, against qp's first-order planar Born formula mapped to 1+1 D by rho_1+1 = -4 pi d rho_3+1/d(m^2)
    #     (born_pairs_1p1). The first correction is O(eps^2) relative (measured 0.17 eps^2): tolerance 0.3 eps^2, and
    #     the deviation must scale as eps^2 (ratio in [3, 5] for eps halving).
    Tp, Wp, qq, ww, Lp, Np = 2.0, 2.5, 1.0, 3.0, 36.0, 72

    def Vt(K0, Kz):
        return PI * Tp * Wp * (np.exp(-(K0 - ww) ** 2 * Tp * Tp / 2 - (Kz - qq) ** 2 * Wp * Wp / 2)
                               + np.exp(-(K0 + ww) ** 2 * Tp * Tp / 2 - (Kz + qq) ** 2 * Wp * Wp / 2))
    bp = born_pairs_1p1(Vt, m, 30.0, 2.5, n_s=128, n_y=128)   # V~ < 1e-16 beyond s = 30, |y| = 2.5
    check("born_pairs_1p1: -4 pi d/dm^2 of qp.born_scalar_planar = direct 1+1 spectral integral (rel.)",
          bp["mismatch"], 0.0, 1e-9)
    devs = []
    for eps in (0.02, 0.01):
        Vp = (lambda t, z, eps=eps: eps * np.exp(-0.5 * (np.asarray(t) / Tp) ** 2 - 0.5 * (np.asarray(z) / Wp) ** 2)
              * np.cos(qq * np.asarray(z) - ww * np.asarray(t)))
        rp = lattice_bogoliubov(Vp, Lp, Np, m, -8 * Tp, 8 * Tp, steps=128)
        devs.append(abs(rp["pairs"] / (eps * eps * bp["pairs"]) - 1))
        check(f"weak superluminal packet, eps = {eps}: lattice pairs (all orders) vs qp planar Born mapped to 1+1 D, "
              f"|ratio - 1| = {devs[-1]:.2e} <= 0.3 eps^2", devs[-1], 0.0, 0.3 * eps * eps)
    check("... deviation is O(eps^2): ratio for eps halving in [3, 5]", devs[0] / devs[1], 4.0, 1.0)

    passed = all(results)
    if verbose:
        print(f"\n{sum(results)}/{len(results)} checks passed")
    return passed


def _convergence() -> int:
    """Slow studies (not in the self-test): null switching leakage vs T, N-dependence, floor vs steps."""
    m, L = 1.0, 16 * PI
    print("Switched patterns eps = 0.3 m^2, q = m, L = 16 pi/m, N = 36: Tr beta^dag beta (particles) and floor vs T")
    for T in (6.0, 10.0, 14.0, 18.0, 22.0, 26.0):
        row = []
        for v in (1.0, 0.5, 2.5, 3.0):
            pat = pattern_potential(0.3, 8, v, T, L, m)
            r = lattice_bogoliubov(pat["V"], L, 36, m, *pat["window"], steps=1024)
            row.append(f"v={v}: {r['total']:.3e} (floor {r['total_floor']:.1e})")
        print(f"  T = {T:5.1f}: " + "; ".join(row))
    print("Lattice caveat: strong null pattern eps = 1.5 m^2 (light-front dressing exceeds the band): Tr vs T and N")
    for N in (36, 48):
        for T in (6.0, 10.0):
            pat = pattern_potential(1.5, 8, 1.0, T, L, m)
            r = lattice_bogoliubov(pat["V"], L, N, m, *pat["window"], steps=1024)
            print(f"  N = {N}, T = {T}: Tr = {r['total']:.3e} (spurious: grows with T, changes with N)")
    print("Weak superluminal packet: lattice pairs/eps^2 vs N (L = 36/m)")
    for N in (56, 72, 96, 128):
        Vp = lambda t, z: 0.01 * np.exp(-t * t / 8 - z * z / 12.5) * np.cos(np.asarray(z) - 3 * np.asarray(t))  # noqa: E731
        try:
            r = lattice_bogoliubov(Vp, 36.0, N, m, -16.0, 16.0, steps=128)
            print(f"  N = {N}: pairs/eps^2 = {r['pairs'] / 1e-4:.10g}, band tail {r['band_tail']:.1e}")
        except ValueError as exc:
            print(f"  N = {N}: refused ({exc})")
    return 0


# ---------------------------------------------------------------- command line
def _energy(text: str) -> float:
    """An energy: a bare number (already in the natural unit) or e.g. '0.511 MeV' (-> eV)."""
    try:
        return float(text)
    except ValueError:
        from unit_tools import Q
        return Q(text).expect("energy").si / E_CHARGE


def _inverse_energy(text: str, kind: str) -> float:
    """A time or length: a bare number (in 1/natural unit) or with units (-> 1/eV)."""
    try:
        return float(text)
    except ValueError:
        from unit_tools import Q
        q = Q(text).expect(kind).si
        return qp.time_to_inverse_eV(q) if kind == "time" else length_to_inverse_eV(q)


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("selftest")
    sub.add_parser("convergence", help="slow: switching leakage vs T, lattice caveat vs N, Born packet vs N")
    pp = sub.add_parser("pattern", help="switched pattern eps e^{-t^2/2T^2} cos(q z - v q t) on the lattice: particles, "
                                        "floor, first-order comparison")
    pp.add_argument("--m", default="1", help="mass: a number (your natural unit) or e.g. '0.511 MeV'")
    pp.add_argument("--eps", type=float, required=True, help="amplitude in units of m^2")
    pp.add_argument("--nq", type=int, required=True, help="q = 2 pi nq / L (box harmonic)")
    pp.add_argument("--v", type=float, required=True, help="phase velocity in units of c (1 = null)")
    pp.add_argument("--T", required=True, help="switching time: a number in 1/m or e.g. '1e-20 s'")
    pp.add_argument("--L", required=True, help="box length: a number in 1/m or e.g. '2e-11 m'")
    pp.add_argument("--N", type=int, default=36, help="grid points (kept modes |n| < N/3)")
    gp = sub.add_parser("gibbons", help="'+' square pulse (Chakraborty & Kar): memory, exact packet, projection")
    for nm, df in (("A0", None), ("a", None), ("c", "1"), ("x0", "0.5"), ("y0", "0.3"), ("sigma", "1")):
        gp.add_argument(f"--{nm}", type=float, required=df is None, default=None if df is None else float(df))
    args = ap.parse_args(argv)
    try:
        if args.cmd == "selftest":
            return 0 if selftest() else 1
        if args.cmd == "convergence":
            return _convergence()
        if args.cmd == "pattern":
            m_unit = _energy(args.m)
            if m_unit <= 0:
                raise ValueError("m must be > 0")
            # every quantity in ONE natural unit (bare numbers: yours; with units: eV), then in units of m
            T = _inverse_energy(args.T, "time") * m_unit
            Lb = _inverse_energy(args.L, "length") * m_unit
            pat = pattern_potential(args.eps, args.nq, args.v, T, Lb, 1.0)
            r = lattice_bogoliubov(pat["V"], Lb, args.N, 1.0, *pat["window"], steps=512)
            print(f"{pat['kind']} pattern: eps = {args.eps} m^2, q = {pat['q']:.6g} m, omega = {pat['omega']:.6g} m, "
                  f"K^2 = {pat['s']:.4g} m^2, T = {T:.6g}/m, L = {Lb:.6g}/m, {len(r['k'])} modes (k_c = {r['k'].max():.4g} m)")
            print(f"Tr beta^dag beta = {r['total']:.6g} particles in the box (in-in), pairs = {r['pairs']:.6g}; "
                  f"precision floor {r['total_floor']:.2g} -> " + ("zero to the floor" if r["consistent_with_zero"] else
                                                                 f"resolved = {r['resolved']}"))
            print(f"in-out vacuum persistence |<0out|0in>|^2 = {r['vacuum_persistence']:.10g}; steps {r['steps']}; "
                  f"band tail {r['band_tail']:.1e}")
            if pat["kind"] in ("null", "subluminal") and not r["consistent_with_zero"]:
                print("note: an eternal null/subluminal pattern makes nothing; what is left comes from switching it on and "
                      "off (a packet): it falls exponentially as T grows")
            if args.eps != 0:
                rb = lattice_born(pat["V"], Lb, args.N, 1.0, *pat["window"])
                print(f"first-order (Born) particles on the same lattice: {rb['total']:.6g}"
                      + (f" (exact/Born = {r['total'] / rb['total']:.4g})" if rb["total"] > 0 else ""))
            return 0
        if args.cmd == "gibbons":
            A0, a = args.A0, args.a
            if not (A0 > 0 and a > 0):
                raise ValueError("need A0 > 0 and a > 0")
            H = lambda U: np.multiply.outer(A0 * A0 * ((np.asarray(U) >= -a) & (np.asarray(U) <= a)),  # noqa: E731
                                            np.diag([1.0, -1.0]))
            X0 = np.array([args.x0, args.y0])
            Ub = a + 0.25 * a
            ck = square_pulse_geodesic(A0, a, [Ub], X0)
            vm = velocity_memory(H, X0, -1.25 * a, Ub, breaks=(-a, a))
            print(f"'+' square pulse H = diag(A0^2, -A0^2) on |U| <= a (A0 = {A0}, a = {a}); particle at rest at X0 = {X0}")
            print(f"velocity memory dX/dtau = {vm['velocity']} (Jacobi) = {ck['dX_dU'][0]} (Chakraborty & Kar); "
                  f"first-order -X0 int H = {vm['velocity_first_order']}")
            pk = gibbons_packet(H, -1.25 * a, Ub, args.c, 1.0, X0, args.sigma, breaks=(-a, a), n_grid=128)
            print(f"exact packet (c = {args.c}, sigma = {args.sigma}) projected on U = {Ub:.4g}: negative-frequency weight "
                  f"{pk['beta_norm']:.2e} (Gibbons: 0), positive-frequency weight {pk['alpha_norm']:.12f}")
            print(f"mean transverse momentum after the wave {pk['p_mean']} = 2c x memory {2 * args.c * vm['velocity']}")
            return 0
    except (ValueError, KeyError) as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
