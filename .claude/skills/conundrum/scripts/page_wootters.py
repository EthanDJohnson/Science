#!/usr/bin/env python3
"""Finite-dimensional Page-Wootters (conditional-probability) clocks for /conundrum (numpy only).

What it computes
    A "universe" = clock C (dimension d_C) + system S (dimension d_S) in a global stationary state
    annihilated by the constraint (a finite Wheeler-DeWitt equation)
        J = H_C (x) 1 + 1 (x) H_S + H_CS,          J |Psi>> = 0.
    * Physical states: the exact null space of J (SVD), and, for commensurate spectra, the
      group-averaging projector P = (w0/2pi) int_0^{2pi/w0} ds e^{-iJs}, evaluated exactly as the
      N-point average (1/N) sum_n e^{-iJ s_n}, s_n = 2 pi n/(N w0), N > max|spec J|/w0
      (the discrete average keeps eigenvalues m*w0 with m = 0 mod N, i.e. only m = 0).
    * Clock time states |t> = sum_k e^{-i E_k t} |E_k> over an orthonormal eigenbasis of H_C
      (the computational basis if H_C is diagonal), unnormalised: <t|t> = d_C.
    * Conditional states psi_S(t) = (<t| (x) 1)|Psi>> and their norm, P(t) ~ ||psi_S(t)||^2.
    * Equally spaced clock E_k = w (k + k0), k = 0..d-1: the lattice states |t_j>, t_j = 2 pi j/(d w),
      are orthogonal (<t_j|t_k> = d delta_jk), {|t_j><t_j|/d} is a projective clock reading, and the
      covariant POVM is E(t) dt = (w/2pi)|t><t| dt on one period (int E = 1).

Key identity (why an uncoupled clock is always "exact")
    d/dt <t| = i <t| H_C, so for J = H_C + H_S (no coupling) (<t|(x)1) J Psi = 0 gives
    i d/dt psi_S(t) = H_S psi_S(t) EXACTLY, for every t and ANY clock spectrum (equally spaced or
    not, degenerate or not). What a non-ideal clock breaks is therefore not the conditional
    Schroedinger equation but:
      (a) coverage: only system energies e with -e in spec(H_C) survive in Psi;
      (b) readability: |t> are orthogonal only for equally spaced spectra at lattice spacing
          2 pi/(d w); otherwise "reading t" is a non-orthogonal POVM with finite resolution, and
          conditioning on a finite-resolution reading gives a MIXED system state (dephasing
          rho_nm -> rho_nm exp(-sigma^2 (e_n-e_m)^2 / 2) for a Gaussian reading error sigma);
      (c) degeneracy: the time states see only one direction per clock eigenspace, the map
          physical state -> psi_S is not injective, and (1/T) int |t><t| dt does not tend to 1;
      (d) interaction H_CS: i d/dt psi_S = H_S psi_S + <t|H_CS|Psi>>, not closed in psi_S; the
          effective generator can be non-Hermitian (non-unitary) or time-dependent, and if the
          physical subspace is larger than the system's (rank loss) psi_S(t) does not determine
          psi_S(t') at all: the time-nonlocal Schroedinger equation of Smith & Ahmadi (2019).
      Exactly solvable coupling (Smith & Ahmadi 2019, Eq. 23, Newtonian gravity):
          H_CS = -lam H_C (x) H_S, lam = G/(c^4 x)  =>  i d/dt psi = H_S (1 - lam H_S)^{-1} psi.
    Two-time probabilities (extension):
      * Kuchar's naive conditional probability P(b at t2 | a at t1) = <P1 P2 P1>/<P1>, with
        P_i = |t_i><t_i|/<t_i|t_i> (x) Pi; for distinct lattice times the clock projectors are
        orthogonal, so it is 0 instead of the textbook |<b|U(t2-t1)|a>|^2.
      * Giovannetti-Lloyd-Maccone (2015): add a memory M written by an impulsive von Neumann
        coupling at t1; then P(b | a) = ||(<t2| (x) Pi_b (x) <a|_M) Psi||^2 / ||(<t2| (x) <a|_M) Psi||^2
        = |<b|U(t2 - t1)|a>|^2. Built here as the lattice history state
        Psi = (1/d) sum_j |t_j> (x) phi_SM(t_j) on an equally spaced clock (GLM Eq. 34 with the
        integral over t replaced by the orthogonal lattice). Without the measurement this equals
        the Page-Wootters null state exactly (checked in the self-test).

Assumptions and validity range
    Finite dimensions, Hermitian H_C, H_S, H_CS; hbar = 1 inside. Exact null space needs exact
    resonances e_S = -E_C (to tolerance tol * max(1, ||J||)); if none exist the physical space is
    empty and a ValueError is raised. Group averaging requires spec(J) in w0 * Z. GLM lattice
    history states require t1, t2 on the lattice. No relativity: the "gravity" coupling is the
    Newtonian mass-energy coupling of Smith & Ahmadi, valid for weak fields (lam * E << 1).

Units
    Natural units hbar = 1 inside: an energy is given as an angular frequency (rad/s) and time in s,
    so products E*t are phases. SI helpers: omega_from_energy(E_J) = E/hbar (rad/s),
    energy_from_omega(w) = hbar w (J), gravity_lambda(x_m) = hbar G/(c^4 x) in s (the natural-unit
    lam that multiplies two angular frequencies). The command line accepts "1 eV" (energy, divided by
    hbar) or "1e9 1/s" (taken as an angular frequency in rad/s; write "2*pi*429 THz" for cycles).

Python usage
    import sys; sys.path.insert(0, ".claude/skills/conundrum/scripts")
    import numpy as np, page_wootters as pw
    HC = pw.equally_spaced_clock(4, 1.0, k0=-1.5)               # E = -1.5, -0.5, 0.5, 1.5 (rad/s)
    HS = 0.5 * np.array([[0, 1], [1, 0]])                        # qubit, Rabi frequency 1 rad/s
    m = pw.PWModel(HC, HS)
    Psi = m.physical_state(np.array([1, 0]))                     # group-average |t=0> (x) |0>
    rows = m.track(Psi, [0, 0.5, 2 * np.pi / 4])                 # norm, fidelity, residual
    m.effective_generator(0.3)                                  # rank, generator, non-Hermiticity

Command line (from the project root)
    python3 .claude/skills/conundrum/scripts/page_wootters.py selftest
    python3 .claude/skills/conundrum/scripts/page_wootters.py qubit --d 8 --omega "1e9 1/s" --gap "3e9 1/s" --sigma "0.1 ns"
    python3 .claude/skills/conundrum/scripts/page_wootters.py interact --d 6 --g 0.2
    python3 .claude/skills/conundrum/scripts/page_wootters.py clock --d 16 --omega "2*pi*429 THz"
    python3 .claude/skills/conundrum/scripts/page_wootters.py gravity --energy "2*pi*429 THz" --distance "1 mm"
"""
from __future__ import annotations

import math
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (_HERE, os.path.normpath(os.path.join(_HERE, "..", "..", "..", ".claude", "skills", "conundrum", "scripts")),
           ".claude/skills/conundrum/scripts"):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from unit_tools import C, G, HBAR  # noqa: E402  (CODATA values shared by the toolkit)

TWO_PI = 2.0 * math.pi


# ---------------------------------------------------------------- SI helpers
def omega_from_energy(E_joule: float) -> float:
    """Angular frequency (rad/s) of an energy in J: w = E / hbar."""
    return E_joule / HBAR


def energy_from_omega(omega: float) -> float:
    """Energy in J of an angular frequency in rad/s: E = hbar w."""
    return HBAR * omega


def gravity_lambda(distance_m: float) -> float:
    """Natural-unit coupling lam (s) of Smith & Ahmadi's H_CS = -(G/(c^4 x)) H_C H_S, with H in rad/s.

    In SI lam_SI = G/(c^4 x) (1/J); multiplying two energies E_C E_S = hbar^2 w_C w_S and dividing the
    constraint by hbar gives lam = hbar G/(c^4 x) in seconds."""
    if distance_m <= 0:
        raise ValueError("distance must be positive")
    return HBAR * G / (C**4 * distance_m)


# ---------------------------------------------------------------- linear algebra
def _herm(H, name: str) -> np.ndarray:
    H = np.atleast_2d(np.asarray(H, dtype=complex))
    if H.ndim != 2 or H.shape[0] != H.shape[1]:
        raise ValueError(f"{name} must be a square matrix")
    if not np.all(np.isfinite(H)):
        raise ValueError(f"{name} has non-finite entries")
    scale = max(1.0, float(np.abs(H).max()))
    if np.abs(H - H.conj().T).max() > 1e-10 * scale:
        raise ValueError(f"{name} is not Hermitian")
    return 0.5 * (H + H.conj().T)


def expm(A: np.ndarray) -> np.ndarray:
    """Matrix exponential by scaling and squaring with a degree-24 Taylor series (no eigensolver)."""
    A = np.asarray(A, dtype=complex)
    nrm = np.abs(A).sum(axis=1).max() if A.size else 0.0
    s = max(0, int(math.ceil(math.log2(nrm / 0.25))) if nrm > 0.25 else 0)
    X = A / (2.0**s)
    term = np.eye(A.shape[0], dtype=complex)
    out = term.copy()
    for k in range(1, 25):
        term = term @ X / k
        out = out + term
    for _ in range(s):
        out = out @ out
    return out


def equally_spaced_clock(d: int, omega: float, k0: float = 0.0) -> np.ndarray:
    """Diagonal clock Hamiltonian E_k = omega (k + k0), k = 0..d-1 (rad/s). k0 = -(d-1)/2 is symmetric."""
    if int(d) != d or d < 2:
        raise ValueError("clock dimension d must be an integer >= 2")
    if not omega > 0:
        raise ValueError("clock spacing omega must be positive")
    return np.diag(omega * (np.arange(int(d)) + k0)).astype(complex)


def _eig_clock(HC: np.ndarray):
    if np.abs(HC - np.diag(np.diag(HC))).max() == 0.0:
        return np.real(np.diag(HC)).copy(), np.eye(HC.shape[0], dtype=complex)
    E, V = np.linalg.eigh(HC)
    return E, V


# ---------------------------------------------------------------- the model
class PWModel:
    """Clock (x) system with constraint J = H_C (x) 1 + 1 (x) H_S + H_CS (all in rad/s)."""

    def __init__(self, H_C, H_S, H_CS=None, tol: float = 1e-9):
        self.HC = _herm(H_C, "H_C")
        self.HS = _herm(H_S, "H_S")
        self.dC, self.dS = self.HC.shape[0], self.HS.shape[0]
        n = self.dC * self.dS
        if H_CS is None:
            self.HCS = np.zeros((n, n), dtype=complex)
            self.coupled = False
        else:
            self.HCS = _herm(H_CS, "H_CS")
            if self.HCS.shape != (n, n):
                raise ValueError(f"H_CS must be {n}x{n} (clock (x) system ordering)")
            self.coupled = bool(np.abs(self.HCS).max() > 0)
        self.J = np.kron(self.HC, np.eye(self.dS)) + np.kron(np.eye(self.dC), self.HS) + self.HCS
        self.tol = tol
        self.EC, self.VC = _eig_clock(self.HC)
        self.ES, self.VS = np.linalg.eigh(self.HS)
        self._K = None

    # --- physical states
    def physical_basis(self) -> np.ndarray:
        """Orthonormal basis (columns) of ker J by SVD, threshold tol * max(1, ||J||_2)."""
        if self._K is None:
            _, s, vh = np.linalg.svd(self.J)
            thr = self.tol * max(1.0, s[0] if s.size else 0.0)
            self._K = vh[s <= thr].conj().T
        return self._K

    def physical_projector(self) -> np.ndarray:
        K = self.physical_basis()
        return K @ K.conj().T

    def group_average(self, omega0: float, N: int = None) -> np.ndarray:
        """Exact group-averaging projector for spec(J) in omega0*Z (ValueError otherwise)."""
        if not omega0 > 0:
            raise ValueError("omega0 must be positive")
        m = np.linalg.eigvalsh(self.J) / omega0
        if np.abs(m - np.round(m)).max() > 1e-8:
            raise ValueError("spectrum of J is not commensurate with omega0; use the exact null space")
        M = int(np.abs(np.round(m)).max())
        N = M + 1 if N is None else int(N)
        if N <= M:
            raise ValueError(f"need N > max|spec J|/omega0 = {M} to avoid aliasing")
        U1 = expm(-1j * self.J * (TWO_PI / (N * omega0)))
        P = np.zeros_like(U1)
        U = np.eye(U1.shape[0], dtype=complex)
        for _ in range(N):
            P += U
            U = U @ U1
        return P / N

    def time_state(self, t: float) -> np.ndarray:
        """|t> = sum_k e^{-i E_k t}|E_k> in the computational basis (norm^2 = d_C)."""
        return self.VC @ np.exp(-1j * self.EC * t)

    def conditional(self, Psi: np.ndarray, t: float) -> np.ndarray:
        """psi_S(t) = (<t| (x) 1)|Psi>> (unnormalised)."""
        return self.time_state(t).conj() @ np.asarray(Psi).reshape(self.dC, self.dS)

    def physical_state(self, psi0, t0: float = 0.0) -> np.ndarray:
        """Group average (projection onto ker J) of |t0> (x) psi0; the Page-Wootters history state."""
        psi0 = np.asarray(psi0, dtype=complex).ravel()
        if psi0.size != self.dS or np.linalg.norm(psi0) == 0:
            raise ValueError("psi0 must be a nonzero vector of the system dimension")
        K = self.physical_basis()
        if K.shape[1] == 0:
            raise ValueError("ker J is empty: no system energy e has -e (shifted by H_CS) in the clock spectrum")
        v = np.kron(self.time_state(t0), psi0)
        Psi = K @ (K.conj().T @ v)
        if np.linalg.norm(Psi) < 1e-12 * np.linalg.norm(v):
            raise ValueError("|t0> (x) psi0 has no component in ker J (psi0 lies in non-resonant levels)")
        return Psi

    def resonant_weight(self, psi0) -> float:
        """Uncoupled case: weight of psi0 on system levels e with -e in spec(H_C)."""
        if self.coupled:
            raise ValueError("resonant_weight is defined for the uncoupled constraint only")
        psi0 = np.asarray(psi0, dtype=complex).ravel()
        c = self.VS.conj().T @ psi0
        scale = max(1.0, np.abs(self.EC).max(), np.abs(self.ES).max())
        res = np.array([np.any(np.abs(self.EC + e) <= self.tol * scale) for e in self.ES])
        return float(np.sum(np.abs(c[res]) ** 2) / np.sum(np.abs(c) ** 2))

    def evolve(self, psi, t: float, H=None) -> np.ndarray:
        """e^{-i H t} psi (default H = H_S), by eigendecomposition."""
        if H is None:
            E, V = self.ES, self.VS
        else:
            E, V = np.linalg.eigh(_herm(H, "H"))
        return V @ (np.exp(-1j * E * t) * (V.conj().T @ psi))

    def track(self, Psi, times, t0: float = 0.0, H_ref=None) -> list:
        """Per time: ||psi_S(t)||^2 relative to t0, fidelity with e^{-iH_ref (t-t0)} psi_S(t0), residual."""
        ref0 = self.conditional(Psi, t0)
        n0 = np.vdot(ref0, ref0).real
        HCSPsi = self.HCS @ Psi
        rows = []
        for t in times:
            psi = self.conditional(Psi, t)
            nn = np.vdot(psi, psi).real
            ref = self.evolve(ref0, t - t0, H_ref)
            fid = abs(np.vdot(ref, psi)) ** 2 / (np.vdot(ref, ref).real * nn) if nn > 0 else 0.0
            res = np.linalg.norm(self.conditional(HCSPsi, t)) / math.sqrt(nn) if nn > 0 else float("inf")
            rows.append({"t": float(t), "norm2_rel": nn / n0, "fidelity": float(fid), "schrodinger_residual": float(res),
                         "psi": psi / math.sqrt(nn) if nn > 0 else psi})
        return rows

    def effective_generator(self, t: float) -> dict:
        """Effective conditional dynamics at clock time t over the whole physical subspace.

        M(t) = (<t| (x) 1) K maps physical-state coordinates to psi_S(t); i dM/dt = -(<t|H_C (x) 1) K = D(t).
        If M(t) has full column rank r, psi_S(t) determines the physical state and i d/dt psi = G psi with
        G = D M^+ (time-local). Reported: rank vs r (rank < r: psi_S(t) does not fix its own future,
        i.e. memory / time-nonlocality), non-Hermiticity of G on range M (non-unitarity), and G itself."""
        K = self.physical_basis()
        r = K.shape[1]
        tau = self.time_state(t)
        Kr = K.reshape(self.dC, self.dS, r)
        M = np.einsum("c,csr->sr", tau.conj(), Kr)
        row = tau.conj() @ self.HC
        D = -np.einsum("c,csr->sr", row, Kr)
        s = np.linalg.svd(M, compute_uv=False)
        rank = int(np.sum(s > 1e-9 * max(1.0, s[0] if s.size else 0.0)))
        out = {"t": float(t), "physical_dim": r, "rank": rank, "injective": rank == r and r > 0}
        if out["injective"]:
            Mp = np.linalg.pinv(M)
            Gm = D @ Mp
            PR = M @ Mp
            out["G"] = Gm
            out["nonhermiticity"] = float(np.linalg.norm(PR @ (Gm - Gm.conj().T) @ PR, 2))
        return out

    def clock_metrics(self, T_window: float = None) -> dict:
        """Resolution and speed limits of the clock's time states (uniform weights 1/d over E_k)."""
        E = self.EC
        d = E.size
        dE = float(np.std(E))
        mean_minus_ground = float(np.mean(E) - E.min())
        out = {"d": d, "delta_E": dE, "mean_minus_ground": mean_minus_ground,
               "mandelstam_tamm_bound": math.pi / (2 * dE) if dE > 0 else float("inf"),
               "margolus_levitin_bound": math.pi / (2 * mean_minus_ground) if mean_minus_ground > 0 else float("inf")}
        gaps = np.diff(np.sort(E))
        spacing = gaps.min() if gaps.size else 0.0
        equal = spacing > 0 and np.allclose(gaps, spacing, rtol=1e-9, atol=0)
        out["equally_spaced"] = bool(equal)
        out["degenerate"] = bool(np.any(gaps <= 1e-12 * max(1.0, np.abs(E).max())))
        if equal:
            out["lattice_step"] = TWO_PI / (d * spacing)
            out["period"] = TWO_PI / spacing
        # first orthogonality time and half-overlap time on a fine scan (+ bisection)
        span = (E.max() - E.min()) or 1.0
        tmax = 4 * TWO_PI / (gaps[gaps > 0].min() if np.any(gaps > 0) else span)
        ts = np.linspace(0, tmax, 20000)
        ov = self.overlap(ts)
        out["t_half"] = _first_crossing(self.overlap, ts, ov, 0.5)
        out["t_orth"] = _first_crossing(self.overlap, ts, ov, 1e-12, zero=True)
        if T_window is None:
            T_window = out.get("period", 1e3 * TWO_PI / span)
        out["povm_window"] = T_window
        out["povm_defect"] = self.povm_defect(T_window)
        return out

    def overlap(self, tau) -> np.ndarray:
        """|<t|t+tau>| / d_C."""
        tau = np.atleast_1d(np.asarray(tau, dtype=float))
        return np.abs(np.exp(-1j * np.outer(tau, self.EC)).sum(axis=1)) / self.EC.size

    def povm_defect(self, T: float) -> float:
        """|| (1/T) int_0^T |t><t| dt - 1 ||_2 (0: the time states resolve the identity on [0, T])."""
        dE = self.EC[:, None] - self.EC[None, :]
        x = dE * T
        with np.errstate(invalid="ignore", divide="ignore"):
            A = np.where(np.abs(x) < 1e-12, 1.0 + 0j, (np.exp(-1j * x) - 1) / (-1j * x))
        A = self.VC @ A @ self.VC.conj().T
        return float(np.linalg.norm(A - np.eye(self.dC), 2))

    def coarse_conditional(self, Psi, t: float, sigma: float, n: int = 4001, width: float = 10.0) -> dict:
        """System state given a clock reading t with Gaussian error sigma (s):
        rho(t) ~ int dt' exp(-(t'-t)^2/(2 sigma^2)) psi_S(t') psi_S(t')^dagger, trace-normalised."""
        if not sigma > 0:
            raise ValueError("sigma must be positive (sigma -> 0 is the sharp conditional state)")
        ts = np.linspace(t - width * sigma, t + width * sigma, n)
        w = np.exp(-((ts - t) ** 2) / (2 * sigma**2))
        w[0] *= 0.5
        w[-1] *= 0.5
        X = np.array([self.conditional(Psi, tp) for tp in ts])
        rho = np.einsum("i,ia,ib->ab", w, X, X.conj())
        rho /= np.trace(rho).real
        return {"rho": rho, "purity": float(np.trace(rho @ rho).real)}


def _first_crossing(f, ts, vals, level, zero=False):
    idx = np.nonzero(vals <= level)[0] if not zero else np.nonzero(vals <= 1e-3)[0]
    idx = idx[idx > 0]
    if idx.size == 0:
        return float("nan")
    i = idx[0]
    a, b = ts[i - 1], ts[i]
    if zero:  # refine a zero of |overlap| by minimising around the dip
        lo, hi = a, min(ts[-1], b + (b - a))
        for _ in range(100):
            m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
            if f(m1)[0] < f(m2)[0]:
                hi = m2
            else:
                lo = m1
        tz = 0.5 * (lo + hi)
        return float(tz) if f(tz)[0] < 1e-6 else float("nan")
    for _ in range(100):
        m = 0.5 * (a + b)
        if f(m)[0] > level:
            a = m
        else:
            b = m
    return float(0.5 * (a + b))


# ---------------------------------------------------------------- couplings
def gravity_coupling(H_C, H_S, lam: float) -> np.ndarray:
    """Smith & Ahmadi (2019) Newtonian coupling H_CS = -lam H_C (x) H_S (lam in s, H in rad/s)."""
    return -lam * np.kron(_herm(H_C, "H_C"), _herm(H_S, "H_S"))


def gravity_generator(H_S, lam: float) -> np.ndarray:
    """Closed form of Smith & Ahmadi Eq. (23): H_eff = H_S (1 - lam H_S)^{-1}."""
    H_S = _herm(H_S, "H_S")
    Id = np.eye(H_S.shape[0])
    A = Id - lam * H_S
    if np.min(np.abs(np.linalg.eigvalsh(A))) < 1e-12:
        raise ValueError("1 - lam H_S is singular: outside the weak-coupling validity range")
    return H_S @ np.linalg.inv(A)


def resonant_clock_for(H_S, lam: float = 0.0, extra=()) -> np.ndarray:
    """Diagonal clock containing E = -e/(1 - lam e) for each system eigenvalue e (plus extra levels)."""
    e = np.linalg.eigvalsh(_herm(H_S, "H_S"))
    E = [-x / (1 - lam * x) for x in e] + list(extra)
    return np.diag(np.array(E, dtype=float)).astype(complex)


# ---------------------------------------------------------------- two-time probabilities
def kuchar_naive(model: PWModel, Psi, t1: float, t2: float, Pi_a, Pi_b) -> float:
    """Kuchar's naive P(b at t2 | a at t1) = <Psi|P1 P2 P1|Psi> / <Psi|P1|Psi>, P_i = |t_i><t_i|/<t_i|t_i> (x) Pi."""
    def P(t, Pi):
        v = model.time_state(t)
        return np.kron(np.outer(v, v.conj()) / np.vdot(v, v).real, np.asarray(Pi, dtype=complex))
    P1, P2 = P(t1, Pi_a), P(t2, Pi_b)
    p1 = np.vdot(Psi, P1 @ Psi).real
    if p1 <= 1e-300:
        raise ValueError("outcome a at t1 has zero probability")
    return float(np.vdot(Psi, P1 @ P2 @ P1 @ Psi).real / p1)


def glm_history_state(H_S, psi0, d: int, omega: float, j1: int, basis=None):
    """GLM (2015) lattice history state with a memory written at t_{j1} = 2 pi j1/(d omega).

    Clock: equally spaced, d levels, lattice t_j = 2 pi j/(d omega), j = 0..d-1. Memory M has d_S + 1
    levels: |r> = index d_S (ready) and |a> = index a. The impulsive coupling at t1 maps
    psi (x) |r> -> sum_a (Pi_a psi) (x) |a> (Pi_a = |b_a><b_a| for the columns b_a of `basis`).
    Returns (Psi as array [d, d_S, d_S+1] normalised so <t_j|Psi> = phi(t_j), times, basis)."""
    H_S = _herm(H_S, "H_S")
    dS = H_S.shape[0]
    if not (0 <= j1 < d):
        raise ValueError("j1 must be a lattice index 0..d-1")
    B = np.eye(dS, dtype=complex) if basis is None else np.asarray(basis, dtype=complex)
    if np.abs(B.conj().T @ B - np.eye(dS)).max() > 1e-10:
        raise ValueError("basis must be unitary (columns = measurement eigenvectors)")
    E, V = np.linalg.eigh(H_S)
    U = lambda t: V @ np.diag(np.exp(-1j * E * t)) @ V.conj().T  # noqa: E731
    psi0 = np.asarray(psi0, dtype=complex) / np.linalg.norm(psi0)
    times = TWO_PI * np.arange(d) / (d * omega)
    t1 = times[j1]
    phi = np.zeros((d, dS, dS + 1), dtype=complex)
    for j, t in enumerate(times):
        if j < j1:
            phi[j, :, dS] = U(t) @ psi0
        else:
            pre = U(t1) @ psi0
            for a in range(dS):
                phi[j, :, a] = U(t - t1) @ (B[:, a] * np.vdot(B[:, a], pre))
    return phi, times, B


def glm_two_time(H_S, psi0, d: int, omega: float, j1: int, j2: int, basis=None) -> dict:
    """P(b at t2 | a at t1) from the GLM memory construction, conditioning on clock lattice time t_{j2}."""
    if not j2 >= j1:
        raise ValueError("need j2 >= j1 (the memory records the earlier measurement)")
    phi, times, B = glm_history_state(H_S, psi0, d, omega, j1, basis)
    dS = B.shape[0]
    # history state Psi = (1/d) sum_j |t_j> (x) phi_j ; <t_j2|Psi> = phi_j2 because <t_j|t_k> = d delta_jk
    cond = phi[j2]
    P = np.zeros((dS, dS))
    for a in range(dS):
        va = cond[:, a]
        pa = np.vdot(va, va).real
        for b in range(dS):
            P[a, b] = abs(np.vdot(B[:, b], va)) ** 2 / pa if pa > 0 else float("nan")
    return {"t1": float(times[j1]), "t2": float(times[j2]), "P_b_given_a": P}


# ---------------------------------------------------------------- self-test
def selftest(verbose: bool = True) -> bool:
    """Compare with closed forms and published results. Returns True if all pass."""
    results = []

    def check(name, got, want, tol):
        ok = bool(abs(got - want) <= tol)
        results.append(ok)
        if verbose:
            print(f"{'PASS' if ok else 'FAIL'}  {name}: {got:.10g} (expected {want:.10g}, tol {tol:g})")

    sx = np.array([[0, 1], [1, 0]], dtype=complex)

    # 1. Rabi formula (textbook two-level result, e.g. Sakurai, Modern QM, sec. 5.5):
    #    H = (Omega/2) sigma_x, |0> -> P(|1>, t) = sin^2(Omega t / 2). Ideal equally spaced clock d = 4,
    #    E = -1.5, -0.5, 0.5, 1.5 rad/s covers the system energies -+0.5 rad/s exactly.
    m = PWModel(equally_spaced_clock(4, 1.0, k0=-1.5), 0.5 * sx)
    Psi = m.physical_state([1, 0])
    tl = [TWO_PI * k / 4 for k in range(4)] + [0.37, 1.91]   # lattice times t_k = 2 pi k/(d w) and two off-lattice
    rows = m.track(Psi, tl)
    for r in rows[:4] + rows[5:]:
        check(f"Rabi: P(1) at t = {r['t']:.4f} s equals sin^2(t/2)", abs(r["psi"][1]) ** 2, math.sin(r["t"] / 2) ** 2, 1e-12)
    check("ideal clock: fidelity with e^{-i H_S t} psi(0), worst over times", min(r["fidelity"] for r in rows), 1.0, 1e-12)
    check("ideal clock: conditional norm constant (unitary)", max(abs(r["norm2_rel"] - 1) for r in rows), 0.0, 1e-12)

    # 2. Lattice orthogonality <t_j|t_k> = d delta_jk (finite geometric series) and the history state
    #    Psi = (1/d) sum_j |t_j> (x) psi(t_j) (Page-Wootters; GLM 2015 Eq. 34 writes it as
    #    "|Psi>> = int dt |t>_T (x) ..."); here it must equal the group-averaged physical state.
    d = 4
    Tm = np.array([m.time_state(TWO_PI * j / d) for j in range(d)])
    check("lattice time states orthogonal: max |<t_j|t_k> - d delta_jk|", np.abs(Tm.conj() @ Tm.T - d * np.eye(d)).max(), 0.0, 1e-12)
    hist = sum(np.kron(Tm[j], m.conditional(Psi, TWO_PI * j / d)) for j in range(d)) / d
    check("history state (1/d) sum_j |t_j> psi(t_j) reproduces Psi", np.linalg.norm(hist - Psi), 0.0, 1e-12)

    # 3. Group averaging = exact null-space projector; kernel dimension by exact counting.
    #    Clock E = 0..4 (w = 1), system e = 0, -1, -2 and a non-resonant -0.5: resonant pairs (k=n) -> dim 3.
    #    J has half-integer eigenvalues, so average over w0 = 0.5 rad/s.
    m3 = PWModel(equally_spaced_clock(5, 1.0), np.diag([0.0, -1.0, -2.0, -0.5]))
    check("kernel dimension = number of resonant (clock, system) pairs", m3.physical_basis().shape[1], 3, 0)
    Pg = m3.group_average(0.5)
    check("group averaging (w0 = 0.5, exact N-point) equals null-space projector", np.abs(Pg - m3.physical_projector()).max(), 0.0, 1e-10)
    check("resonant weight of uniform psi0 (3 of 4 levels)", m3.resonant_weight(np.ones(4)), 0.75, 1e-12)

    # 4. Margolus & Levitin, Physica D 120, 188 (1998), arXiv quant-ph/9710043, p. 5: the state
    #    "|psi0> = (|0> + |2E>)/sqrt 2 ... evolves in a time t = h/4E into |psi_t> = (|0> - |2E>)/sqrt 2 which is
    #    orthogonal ... both of the bounds Eq. (4) and Eq. (5) are achieved." A d = 2 clock (E = 0, w) is
    #    that state with 2E = w: t_orth = pi/w = ML bound pi/(2 (E - E0)) = MT bound pi/(2 dE).
    m4 = PWModel(equally_spaced_clock(2, 1.0), np.diag([0.0, -1.0]))
    cm = m4.clock_metrics()
    check("d=2 clock: first orthogonality time = pi/w", cm["t_orth"], math.pi, 1e-9)
    check("d=2 clock saturates Margolus-Levitin pi/(2(E-E0))", cm["margolus_levitin_bound"], math.pi, 1e-12)
    check("d=2 clock saturates Mandelstam-Tamm pi/(2 dE)", cm["mandelstam_tamm_bound"], math.pi, 1e-12)

    # 5. Large-d limit (Dirichlet kernel, closed form of the geometric sum):
    #    |<t|t+tau>|/d = |sin(d w tau/2) / (d sin(w tau/2))| -> 0 at fixed tau, lattice step 2 pi/(d w) -> 0,
    #    and tau_step * dE -> 2 pi sqrt((d^2-1)/12)/d -> pi/sqrt(3) (variance of a discrete uniform law).
    for dd in (8, 64, 1001):
        md = PWModel(equally_spaced_clock(dd, 1.0), np.diag([0.0, -1.0]))
        tau = 0.9
        check(f"d={dd}: overlap at tau = 0.9 s equals Dirichlet kernel", md.overlap(tau)[0],
              abs(math.sin(dd * tau / 2) / (dd * math.sin(tau / 2))), 1e-10)
    cm = PWModel(equally_spaced_clock(1001, 1.0), np.diag([0.0, -1.0])).clock_metrics()
    check("d=1001: lattice step x dE -> pi/sqrt(3)", cm["lattice_step"] * cm["delta_E"], math.pi / math.sqrt(3), 1e-5)
    check("d=1001: lattice step >= Mandelstam-Tamm bound (ratio -> 2/sqrt 3)",
          cm["lattice_step"] / cm["mandelstam_tamm_bound"], 2 / math.sqrt(3), 1e-5)

    # 6. Smith & Ahmadi, Quantum 3, 160 (2019), arXiv 1712.00081, p. 8-9: "Hint = -G/(c^4 d) HC (x) HS" gives
    #    "i d/dt|psiS(t)> = HS (IS - G/(c^4 d) HS)^-1 |psiS(t)> = [HS + G/(c^4 d) HS^2 + O(G^2/(c^8 d^2))]|psiS(t)>" (Eq. 23).
    #    Finite clock tuned to contain the resonances -e/(1 - lam e) plus two spectator levels.
    lam = 0.08
    # qutrit (for a qubit H_S^2 is proportional to 1, so the O(lam) term would be only a global phase)
    HS6 = np.array([[0.3, 0.2, 0.0], [0.2, -0.5, 0.15], [0.0, 0.15, 0.8]], dtype=complex)
    HC6 = resonant_clock_for(HS6, lam, extra=(0.9, -1.3))
    m6 = PWModel(HC6, HS6, gravity_coupling(HC6, HS6, lam))
    Heff = gravity_generator(HS6, lam)
    eg = m6.effective_generator(0.7)
    check("gravity coupling: effective generator = H_S (1 - lam H_S)^-1 (Eq. 23)", np.abs(eg["G"] - Heff).max(), 0.0, 1e-9)
    Psi6 = m6.physical_state([1, 0, 0])
    r6 = m6.track(Psi6, [0.0, 1.3, 4.0], H_ref=Heff)
    check("gravity coupling: fidelity with exp(-i H_eff t)", min(r["fidelity"] for r in r6), 1.0, 1e-10)
    r6b = m6.track(Psi6, [12.0])
    check("gravity coupling: uncorrected Schroedinger evolution now fails (1 - fidelity > 1e-3)",
          float(1 - r6b[0]["fidelity"] > 1e-3), 1.0, 0)
    small = 1e-4
    lin = _herm(HS6, "H") + small * _herm(HS6, "H") @ _herm(HS6, "H")
    # limit lam -> 0: H_eff = H_S + lam H_S^2 + O(lam^2) (second form of Eq. 23); O(lam^2) ~ 1e-8 x ||H_S||^3
    check("weak-coupling limit: H_eff - (H_S + lam H_S^2) is O(lam^2)", np.abs(gravity_generator(HS6, small) - lin).max(), 0.0, 1e-7)

    # 7. Finite-resolution clock reading: Gaussian error sigma dephases the energy basis by the normal
    #    characteristic function exp(-sigma^2 Delta^2 / 2), Delta = e_n - e_m (here Delta = 1 rad/s).
    sig = 0.6
    cc = m.coarse_conditional(Psi, 1.0, sig)
    rho_e = m.VS.conj().T @ cc["rho"] @ m.VS
    sharp = m.conditional(Psi, 1.0)
    sharp = m.VS.conj().T @ (sharp / np.linalg.norm(sharp))
    check("Gaussian clock error: |rho_01| / |rho_01(sharp)| = exp(-sigma^2/2)",
          abs(rho_e[0, 1]) / abs(sharp[0] * sharp[1].conj()), math.exp(-sig**2 / 2), 1e-9)

    # 8. Two-time probabilities. Textbook sequential (Lueders) rule: P(b at t2 | a at t1) = |<b|U(t2-t1)|a>|^2.
    #    GLM 2015 (arXiv 1504.04215) abstract: "we show how the model allows one to reproduce the correct
    #    statistics of sequential measurements performed on a system at different times."
    dg, j1, j2 = 16, 3, 9
    HSq = 0.5 * sx + 0.3 * np.diag([1.0, -1.0])
    g = glm_two_time(HSq, [0.6, 0.8], dg, 1.0, j1, j2)
    E, V = np.linalg.eigh(HSq)
    U21 = V @ np.diag(np.exp(-1j * E * (g["t2"] - g["t1"]))) @ V.conj().T
    check("GLM memory: P(b=1 at t2 | a=0 at t1) = |<1|U(t2-t1)|0>|^2", g["P_b_given_a"][0, 1], abs(U21[1, 0]) ** 2, 1e-12)
    check("GLM memory: P(b=0 at t2 | a=1 at t1) = |<0|U(t2-t1)|1>|^2", g["P_b_given_a"][1, 0], abs(U21[0, 1]) ** 2, 1e-12)
    # Before t1 the GLM history state (memory ready) must coincide with the Page-Wootters null state.
    mq = PWModel(np.diag(np.linspace(-7.5, 7.5, dg)), HSq)   # not resonant with HSq: use lattice history directly
    phi, times, _ = glm_history_state(HSq, [0.6, 0.8], dg, 1.0, j1)
    check("GLM history before t1: memory ready, psi(t_j) = e^{-iH t_j} psi0",
          np.linalg.norm(phi[2, :, 2] - mq.evolve(np.array([0.6, 0.8], dtype=complex), times[2])), 0.0, 1e-12)
    Pi0, Pi1 = np.diag([1.0, 0.0]), np.diag([0.0, 1.0])
    check("Kuchar's naive two-time probability vanishes for distinct lattice times",
          kuchar_naive(m, Psi, TWO_PI * 1 / 4, TWO_PI * 3 / 4, Pi1, Pi0), 0.0, 1e-12)

    # 9. Diagnostics with exact expected counts (not independent references).
    #    Degenerate clock E = 0, 1, 1, 2 with system e = 0, -1: ker J has dim 3 but psi_S has dim 2 -> not injective,
    #    and (1/T) int |t><t| cannot resolve the identity (defect = 1 exactly: the degenerate 2x2 block is all ones).
    mdg = PWModel(np.diag([0.0, 1.0, 1.0, 2.0]), np.diag([0.0, -1.0]))
    eg = mdg.effective_generator(0.4)
    check("degenerate clock: physical dim 3, conditional rank 2", 10 * eg["physical_dim"] + eg["rank"], 32, 0)
    check("degenerate clock: POVM defect over one period = 1", mdg.povm_defect(TWO_PI), 1.0, 1e-12)
    check("equally spaced clock: POVM defect over one period = 0", m.povm_defect(TWO_PI), 0.0, 1e-12)
    #    Unequally spaced, uncoupled clock: Schroedinger evolution still exact (d<t|/dt = i<t|H_C).
    HSu = np.diag([0.0, -1.0, -np.sqrt(2)])
    mu = PWModel(np.diag([0.0, 1.0, np.sqrt(2), 3.3]), HSu)
    Psiu = mu.physical_state(np.ones(3) / np.sqrt(3))
    check("unequally spaced clock: fidelity 1 at arbitrary t", min(r["fidelity"] for r in mu.track(Psiu, [0.3, 2.2, 17.0])), 1.0, 1e-12)

    passed = all(results)
    if verbose:
        print(f"\n{sum(results)}/{len(results)} checks passed")
    return passed


# ---------------------------------------------------------------- command line
def _omega(text: str) -> float:
    """Parse '1 eV' (energy -> E/hbar) or '1e9 1/s' (angular frequency, rad/s) via unit_tools."""
    from unit_tools import Q
    q = Q(text)
    try:
        return q.expect("energy").si / HBAR
    except Exception:
        return q.expect("frequency").si


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("selftest")
    qp = sub.add_parser("qubit", help="equally spaced d-level clock + qubit H_S = (gap/2) sigma_x")
    qp.add_argument("--d", type=int, default=8)
    qp.add_argument("--omega", required=True, help="clock spacing, e.g. '1e9 1/s' or '1 ueV'")
    qp.add_argument("--gap", required=True, help="qubit splitting (Rabi frequency); +-gap/2 must lie in the clock spectrum omega*(k-(d-1)/2), so gap/omega = 1, 3, 5... for even d and 2, 4... for odd d")
    qp.add_argument("--sigma", help="Gaussian clock-reading error, e.g. '0.1 ns'")
    cp = sub.add_parser("clock", help="resolution and speed limits of an equally spaced d-level clock")
    cp.add_argument("--d", type=int, required=True)
    cp.add_argument("--omega", required=True)
    ip = sub.add_parser("interact", help="generic coupling g (clock hopping) (x) sigma_z, clock spacing 1 rad/s, qubit gap 1 rad/s")
    ip.add_argument("--d", type=int, default=6)
    ip.add_argument("--g", type=float, default=0.2, help="coupling in units of the clock spacing")
    gp = sub.add_parser("gravity", help="Smith-Ahmadi Newtonian clock-system correction lam*E")
    gp.add_argument("--energy", required=True, help="system energy scale, e.g. '2*pi*429 THz' or '1 eV'")
    gp.add_argument("--distance", required=True, help="clock-system distance, e.g. '1 mm'")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "selftest":
            return 0 if selftest() else 1
        if args.cmd == "qubit":
            w, gap = _omega(args.omega), _omega(args.gap)
            ratio = gap / (2 * w)
            k0 = -(args.d - 1) / 2
            m = PWModel(equally_spaced_clock(args.d, w, k0=k0), 0.5 * gap * np.array([[0, 1], [1, 0]]))
            Psi = m.physical_state([1, 0])
            print(f"clock: d = {args.d}, spacing {w:.6g} rad/s, energies {w * k0:.4g}..{w * (args.d - 1 + k0):.4g} rad/s; "
                  f"system +-gap/2 = +-{ratio:.4g} spacings; resonant weight {m.resonant_weight([1, 0]):.4g}")
            step = TWO_PI / (args.d * w)
            print(f"lattice step 2 pi/(d w) = {step:.6g} s; period {TWO_PI / w:.6g} s")
            print(f"{'t (s)':>12} {'P(|1>)':>10} {'sin^2(gap t/2)':>15} {'fidelity':>10} {'norm rel':>9}")
            for r in m.track(Psi, [k * step for k in range(args.d)]):
                print(f"{r['t']:12.5g} {abs(r['psi'][1])**2:10.6f} {math.sin(gap * r['t'] / 2)**2:15.6f} {r['fidelity']:10.8f} {r['norm2_rel']:9.6f}")
            if args.sigma:
                from unit_tools import Q
                s = Q(args.sigma).expect("time").si
                cc = m.coarse_conditional(Psi, step, s)
                rho_e = m.VS.conj().T @ cc["rho"] @ m.VS
                sh = m.VS.conj().T @ m.conditional(Psi, step)
                sh = sh / np.linalg.norm(sh)
                print(f"clock error sigma = {s:.4g} s at t = {step:.4g} s: purity {cc['purity']:.6f}; energy-basis coherence "
                      f"factor {abs(rho_e[0, 1]) / abs(sh[0] * sh[1].conj()):.6f} "
                      f"(closed form exp(-sigma^2 gap^2/2) = {math.exp(-(s * gap)**2 / 2):.6f})")
        elif args.cmd == "clock":
            w = _omega(args.omega)
            m = PWModel(equally_spaced_clock(args.d, w), np.diag([0.0]))
            cm = m.clock_metrics()
            print(f"d = {cm['d']}, spacing {w:.6g} rad/s ({energy_from_omega(w):.4g} J)")
            print(f"lattice step 2 pi/(d w) = {cm['lattice_step']:.6g} s; period {cm['period']:.6g} s; half-overlap time {cm['t_half']:.6g} s")
            print(f"Mandelstam-Tamm pi/(2 dE) = {cm['mandelstam_tamm_bound']:.6g} s; Margolus-Levitin pi/(2(E-E0)) = {cm['margolus_levitin_bound']:.6g} s")
            print(f"POVM defect over one period: {cm['povm_defect']:.3g}")
        elif args.cmd == "interact":
            d = args.d
            HC = equally_spaced_clock(d, 1.0, k0=-(d - 1) / 2)
            X = np.diag(np.ones(d - 1), 1) + np.diag(np.ones(d - 1), -1)
            HS = 0.5 * np.array([[0, 1], [1, 0]])
            HCS = args.g * np.kron(X, np.diag([1.0, -1.0]))
            m = PWModel(HC, HS, HCS)
            K = m.physical_basis()
            print(f"clock d = {d} (spacing 1 rad/s), qubit gap 1 rad/s, H_CS = {args.g} X_C (x) sigma_z; dim ker J = {K.shape[1]}")
            if K.shape[1] == 0:
                ev = np.linalg.eigvalsh(m.J)
                shift = float(ev[np.argmin(np.abs(ev))])
                print(f"the coupling detunes every resonance (no exact null space); retuning H_S -> H_S - ({shift:.6g} rad/s) 1 "
                      f"so that J has an exact zero eigenvalue")
                m = PWModel(HC, HS - shift * np.eye(2), HCS)
                K = m.physical_basis()
                print(f"dim ker J after retuning = {K.shape[1]}")
            Psi = K[:, 0]
            for t in (0.0, 0.5, 1.0, 2.0, 3.0):
                eg = m.effective_generator(t)
                r = m.track(Psi, [t])[0]
                extra = (f"non-Hermiticity of G {eg['nonhermiticity']:.3g}" if eg["injective"]
                         else "not injective: psi_S(t) does not determine the physical state (time-nonlocal)")
                print(f"t = {t:4.1f} s: rank {eg['rank']}/{eg['physical_dim']}; norm rel {r['norm2_rel']:.4g}; "
                      f"fidelity vs e^(-i H_S t) {r['fidelity']:.6f}; residual {r['schrodinger_residual']:.3g}; {extra}")
        else:
            from unit_tools import Q
            w = _omega(args.energy)
            x = Q(args.distance).expect("length").si
            lam = gravity_lambda(x)
            print(f"lam = hbar G/(c^4 x) = {lam:.4g} s; fractional correction lam*E = {lam * w:.4g} "
                  f"(H_eff = H_S/(1 - lam H_S); below double precision if < 1e-16, so use this analytic value)")
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
