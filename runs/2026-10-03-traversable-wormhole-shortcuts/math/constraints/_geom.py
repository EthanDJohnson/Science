"""Minimal independent curvature routines for the constraints math checks (diagonal or general metric).
Signature (-,+,+,+); conventions: Gamma^a_bc, Riemann R^a_bcd = d_c Gamma^a_db - ..., Ricci R_bd = R^a_bad."""
import sympy as sp


def christoffel(g, x):
    n = len(x)
    gi = sp.simplify(g.inv())
    G = [[[0] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                G[a][b][c] = sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], x[c]) + sp.diff(g[d, c], x[b])
                                                           - sp.diff(g[b, c], x[d])) for d in range(n)) / 2)
    return G


def riemann(g, x):
    n = len(x)
    Gm = christoffel(g, x)
    R = [[[[0] * n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    R[a][b][c][d] = sp.simplify(sp.diff(Gm[a][d][b], x[c]) - sp.diff(Gm[a][c][b], x[d])
                                                + sum(Gm[a][c][e] * Gm[e][d][b] - Gm[a][d][e] * Gm[e][c][b]
                                                      for e in range(n)))
    return R, Gm


def ricci(g, x):
    n = len(x)
    R, Gm = riemann(g, x)
    Ric = sp.zeros(n, n)
    for b in range(n):
        for d in range(n):
            Ric[b, d] = sp.simplify(sum(R[a][b][a][d] for a in range(n)))
    return Ric, R, Gm


def einstein_mixed(g, x):
    """G^a_b and the Ricci tensor (lower indices)."""
    Ric, R, Gm = ricci(g, x)
    gi = g.inv()
    Rs = sp.simplify(sum(gi[a, b] * Ric[a, b] for a in range(len(x)) for b in range(len(x))))
    Gmix = sp.simplify(gi * Ric - sp.eye(len(x)) * Rs / 2)
    return Gmix, Ric, R, Gm, Rs


def kretschmann(g, x, R):
    n = len(x)
    gi = g.inv()
    # lower first index: R_abcd = g_ae R^e_bcd ; diagonal metric assumed for speed
    tot = 0
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    Rl = g[a, a] * R[a][b][c][d]
                    if Rl == 0:
                        continue
                    Ru = gi[b, b] * gi[c, c] * gi[d, d] * Rl
                    tot += Rl * Ru * gi[a, a] * g[a, a] if False else Rl * Ru * gi[a, a]
    return sp.simplify(tot)
