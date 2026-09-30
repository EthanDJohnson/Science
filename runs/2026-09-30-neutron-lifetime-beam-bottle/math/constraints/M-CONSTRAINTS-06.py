"""M-CONSTRAINTS-06 (F8, F9, K4): Fierz term. Rate  Gamma(b) = Gamma_0 (1 + b <m_e/E_e>),
average over the neutron beta spectrum  dN/dW ∝ F(Z=1,W) p W (W0 - W)^2, W = E_e/m_e (total), p = sqrt(W^2-1).
W0 from 2-body-recoil-corrected endpoint E0 = (m_n^2 - m_p^2 + m_e^2)/(2 m_n). Fermi function: nonrelativistic
Coulomb (Z=1, eta = alpha W/p) and the relativistic point-nucleus form; both reported (b changes at the 1e-4 level).
Needed b: tau_beta(b) = tau_beta0 / (1 + b<m/E>) = 887.7 s with tau_beta0 = 878.50 s (PERKEO III)."""
import math
import mpmath as mp
from _common import near
from math_checks import identity, limit, finish

me, mn, mp_ = 0.51099895, 939.56542052, 938.27208816   # MeV
alpha = 1 / 137.035999
E0 = (mn**2 - mp_**2 + me**2) / (2 * mn)
W0 = E0 / me
print(f"   endpoint E0 = {E0:.5f} MeV, W0 = {W0:.5f}")


def F_nr(W):
    p = math.sqrt(W * W - 1)
    eta = alpha * W / p
    return 2 * math.pi * eta / (1 - math.exp(-2 * math.pi * eta))


def F_rel(W, R=0.8751e-15 / 386.159e-15):   # proton radius in electron Compton units
    p = math.sqrt(W * W - 1)
    g = math.sqrt(1 - alpha**2)
    eta = alpha * W / p
    return float(2 * (1 + g) * (2 * p * R) ** (2 * g - 2) * math.exp(math.pi * eta)
                 * abs(mp.gamma(g + 1j * eta)) ** 2 / mp.gamma(2 * g + 1) ** 2)


def avg(F, N):
    num = den = 0.0
    h = (W0 - 1) / N
    for i in range(N):                     # midpoint rule
        W = 1 + (i + 0.5) * h
        wgt = F(W) * math.sqrt(W * W - 1) * W * (W0 - W) ** 2
        num += wgt / W
        den += wgt
    return num / den


a_nr, a_nr2 = avg(F_nr, 20000), avg(F_nr, 40000)
a_rel = avg(F_rel, 20000)
a_none = avg(lambda W: 1.0, 20000)
print(f"   <1/W>: no Coulomb {a_none:.5f}, NR Fermi {a_nr:.5f} (N 2x: {a_nr2:.5f}), relativistic {a_rel:.5f}")
near("<m_e/E> (NR Fermi)", a_nr, 0.6555, 0.0003)
near("<m_e/E> (rel Fermi)", a_rel, 0.6555, 0.0003)
# limit: alpha -> 0 makes F -> 1
limit("2*pi*a*W/p/(1 - exp(-2*pi*a*W/p))", "a", 0, "1")
b = (878.50 / 887.7 - 1) / a_nr
near("needed b", b, -0.0158, 6e-5)
b_s = __import__("sympy").symbols("b")
t0, t1, m = __import__("sympy").symbols("t0 t1 m", positive=True)
identity((t0 / t1 - 1) / m * m + 1, t0 / t1)   # b<m/E> = t0/t1 - 1  <=> t1 = t0/(1 + b<m/E>)
near("distance from PERKEO III b = 0.017(21)", (b - 0.017) / 0.021, -1.6, 0.06)
near("distance from aSPECT b = -0.0098(193)", (b + 0.0098) / 0.0193, -0.3, 0.06)
raise SystemExit(finish())
