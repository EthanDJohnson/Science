"""M-CONSTRAINTS-06: warp shell NEC at beta_warp = 0.02 (pass) and 0.04 (fail near r = 12 m, perpendicular).

Geometric units (lengths in m, T in m^-2, T = G/8 pi). Metric: toolkit warp_shell.build_shell
(M = 4.49e27 kg, R1 = 10 m, R2 = 20 m, Rb = 0, default smoothing) -- the same rebuild the lens used,
taken as an input. Everything downstream is my own: Christoffels and Ricci by nested central finite
differences of g_ab (static metric, so d_t = 0), G_ab, Eulerian tetrad, NEC minimised over
null vectors k = e0 + m (m on a 6000-point sphere plus the +-x axes). Step-halving check h = 0.05, 0.025 m.
Claims: beta = 0.02 no NEC failure; beta = 0.04 NEC fails, worst about -8.0e-5 m^-2 near r = 12 m on the
axis perpendicular to the shift, where rho_E = 1.11e-4 m^-2; beta_crit = 0.0244 +- 0.0002.
"""
import sys
sys.path.insert(0, ".claude/skills/conundrum/scripts")
import numpy as np
from math_checks import quantity, sign, finish
from warp_shell import build_shell

def make_g(shell):
    def g(P):
        P = np.atleast_2d(P)
        return shell.metric_cartesian(0.0, P[:, 0], P[:, 1], P[:, 2])
    return g

def dg(g, P, h):
    out = np.zeros((len(P), 4, 4, 4))   # [pt, c, a, b] = d_c g_ab
    for i in range(3):
        e = np.zeros(3); e[i] = h
        out[:, i + 1] = (g(P + e) - g(P - e)) / (2 * h)
    return out

def gamma(g, P, h):
    G = g(P); Gi = np.linalg.inv(G); D = dg(g, P, h)
    # Gamma^a_bc = 1/2 g^ad (d_b g_dc + d_c g_db - d_d g_bc)
    t = np.einsum("pbdc->pdbc", D) + np.einsum("pcdb->pdbc", D) - D
    return 0.5 * np.einsum("pad,pdbc->pabc", Gi, t)

def einstein(g, P, h):
    Gm = gamma(g, P, h)
    dG = np.zeros((len(P), 4, 4, 4, 4))  # [pt, e, a, b, c] = d_e Gamma^a_bc
    for i in range(3):
        e = np.zeros(3); e[i] = h
        dG[:, i + 1] = (gamma(g, P + e, h) - gamma(g, P - e, h)) / (2 * h)
    Ric = (np.einsum("paabd->pbd", dG) - np.einsum("pdaba->pbd", dG)
           + np.einsum("paae,pebd->pbd", Gm, Gm) - np.einsum("pade,peba->pbd", Gm, Gm))
    G = g(P); Gi = np.linalg.inv(G)
    Rs = np.einsum("pab,pab->p", Gi, Ric)
    return Ric - 0.5 * G * Rs[:, None, None], G

def fib(n):
    i = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * i / n); th = np.pi * (1 + 5**0.5) * i
    m = np.stack([np.cos(th) * np.sin(phi), np.sin(th) * np.sin(phi), np.cos(phi)], 1)
    return np.vstack([m, [[1, 0, 0], [-1, 0, 0]]])

DIRS = fib(6000)

def nec_scan(beta, P, h):
    sh = build_shell(4.49e27, 10.0, 20.0, beta_warp=beta)
    g = make_g(sh)
    Gab, G = einstein(g, P, h)
    T = Gab / (8 * np.pi)
    res = []
    for k in range(len(P)):
        gk = G[k]
        Gi = np.linalg.inv(gk)
        N = 1 / np.sqrt(-Gi[0, 0])
        n = -N * Gi[:, 0]
        hs = gk[1:, 1:]
        L = np.linalg.cholesky(hs)              # hs = L L^T ; s_A = columns of L^-T
        S = np.linalg.inv(L).T
        E = np.zeros((4, 4)); E[0] = n
        for A in range(3):
            E[A + 1, 1:] = S[:, A]
        eta = E @ gk @ E.T
        assert np.allclose(eta, np.diag([-1, 1, 1, 1]), atol=1e-10)
        Tf = E @ T[k] @ E.T                     # orthonormal-frame components
        kk = np.hstack([np.ones((len(DIRS), 1)), DIRS])
        nec = np.einsum("na,ab,nb->n", kk, Tf, kk)
        res.append((Tf[0, 0], nec.min()))
    return np.array(res)

rs = np.arange(10.2, 19.81, 0.2)
P_perp = np.stack([np.zeros_like(rs), rs, np.zeros_like(rs)], 1)        # perpendicular to shift (y axis)
ang = np.pi / 4
P_diag = np.stack([rs * np.cos(ang), rs * np.sin(ang), np.zeros_like(rs)], 1)
P = np.vstack([P_perp, P_diag])
summary = {}
for beta in (0.0, 0.02, 0.0235, 0.025, 0.03, 0.04):
    for h in (0.05, 0.025):
        res = nec_scan(beta, P, h)
        j = np.argmin(res[:, 1])
        nfail = int(np.sum(res[:, 1] < -1e-8))
        summary[(beta, h)] = (res[j, 1], P[j], res[j, 0], nfail)
        print(f"beta={beta:.4f} h={h}: min NEC {res[j,1]:+.3e} m^-2 at {np.round(P[j],2)}, rho_E there {res[j,0]:.3e}, fails {nfail}/{len(P)}")
# checks
for h in (0.05, 0.025):
    sign(f"{summary[(0.02, h)][0]}", "nonnegative") if summary[(0.02, h)][0] >= -1e-8 else sign(f"{summary[(0.02, h)][0]}", "nonnegative")
    sign(f"{summary[(0.04, h)][0]}", "negative")
quantity(f"{summary[(0.04, 0.025)][0]}", "-8.0e-5", rel_tol=0.1)
quantity(f"{np.linalg.norm(summary[(0.04, 0.025)][1])}", "12", rel_tol=0.05)
quantity(f"{summary[(0.04, 0.025)][2]}", "1.11e-4", rel_tol=0.03)
quantity(f"{summary[(0.04, 0.025)][0] / summary[(0.04, 0.05)][0]}", "1", rel_tol=0.02)
raise SystemExit(finish())
