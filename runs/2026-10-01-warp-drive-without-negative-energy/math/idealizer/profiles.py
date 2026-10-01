"""Own helper for the M-IDEALIZER checks (not the lens's code): shift profiles S(r) on R1 < r < R2
and the linear NEC caps. Geometric units (G = c = 1), lengths in metres.
Linear theory, unit lapse, flat slices: T_0i = (beta/16pi) V_i, V = curl curl (S z-hat)
= a c r-hat - b z-hat, a = S'' - S'/r, b = S'' + S'/r, c = cos(theta)   (derived in M-IDEALIZER-05).
NEC for isotropic p: |T_0i| <= (rho + p)/2 (derived in M-IDEALIZER-06).
"""
import numpy as np

G_SI, C_SI = 6.67430e-11, 2.99792458e8
KG_TO_M = G_SI/C_SI**2


def derivs(kind, rr, R1, R2):
    D = R2 - R1
    x = (rr - R1)/D
    if kind == "cubic":        # S = 1 - (3x^2 - 2x^3)
        return -6*x*(1 - x)/D, -(6 - 12*x)/D**2
    if kind == "quintic":      # S = 1 - (10x^3 - 15x^4 + 6x^5)
        return -30*x**2*(1 - x)**2/D, -(60*x - 180*x**2 + 120*x**3)/D**2
    if kind == "sigmoid":      # Fuchs et al. eq. (28), Rb = 0: S = 1 - 1/(exp(D(1/(r-R2) + 1/(r-R1))) + 1)
        u1, u2 = rr - R1, rr - R2
        arg = D*(1/u2 + 1/u1); a1 = D*(-1/u2**2 - 1/u1**2); a2 = D*(2/u2**3 + 2/u1**3)
        f = 1/(1 + np.exp(np.clip(arg, -700, 700))); q = f*(1 - f)
        f1 = -q*a1; f2 = -(f1*(1 - 2*f)*a1 + q*a2)
        return -f1, -f2
    raise ValueError(kind)


def S_of(kind, rr, R1, R2):
    D = R2 - R1
    x = np.clip((rr - R1)/D, 0, 1)
    if kind == "cubic":
        return 1 - (3*x**2 - 2*x**3)
    if kind == "quintic":
        return 1 - (10*x**3 - 15*x**4 + 6*x**5)
    u1, u2 = rr - R1, rr - R2
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        arg = D*(1/u2 + 1/u1)
        S = 1 - 1/(1 + np.exp(np.clip(arg, -700, 700)))
    return np.where(rr <= R1, 1.0, np.where(rr >= R2, 0.0, S))


def caps(kind, M, R1, R2, nr=20000, nc=801, p_over_rho=0.0):
    """Return (beta_uniform, beta_shaped_spherical, beta_shaped_pointwise)."""
    rr = np.linspace(R1, R2, nr + 2)[1:-1]
    S1, S2 = derivs(kind, rr, R1, R2)
    a = S2 - S1/rr; b = S2 + S1/rr
    m = np.maximum(np.abs(b), 2*np.abs(S1)/rr)          # max over angle of |V|
    rho = 3*M/(4*np.pi*(R2**3 - R1**3))
    beta_uni = 8*np.pi*rho*(1 + p_over_rho)/m.max()
    dr = (R2 - R1)/(nr + 1)
    beta_sph = 2*M/np.sum(m*rr**2*dr)                     # rho(r) = (beta/8pi) m(r), total M
    cc = np.linspace(-1, 1, nc)
    Vabs = np.sqrt(np.maximum(cc[None, :]**2*(a[:, None]**2 - 2*a[:, None]*b[:, None]) + b[:, None]**2, 0))
    wc = np.full(nc, 2/(nc - 1)); wc[[0, -1]] /= 2
    intV = np.sum(Vabs*(2*np.pi*rr**2*dr)[:, None]*wc[None, :])
    beta_pt = 8*np.pi*M/intV                              # rho = 2|T_0i| pointwise, total M
    return beta_uni, beta_sph, beta_pt
