"""Own helper (not the lens's or toolkit's code): constant-density TOV shell, geometric units (m).
Shell R1 < r < R2, density rho0, empty flat cavity. Integrate inward from R2 with P(R2) = 0,
alpha(R2) = sqrt(1 - 2m/R2). dP/dr = -(rho+P)(m+4 pi r^3 P)/(r(r-2m)); dln(alpha)/dr = (m+4 pi r^3 P)/(r(r-2m)).
"""
import math

G, c = 6.67430e-11, 2.99792458e8


def shell(M_kg, R1, R2, pressure=True, n=200000):
    m_tot = G * M_kg / c**2
    rho0 = 3 * m_tot / (4 * math.pi * (R2**3 - R1**3))
    def rhs(r, P, la):
        m = 4 * math.pi / 3 * rho0 * (r**3 - R1**3)
        Pe = P if pressure else 0.0
        q = (m + 4 * math.pi * r**3 * Pe) / (r * (r - 2 * m))
        return (-(rho0 + Pe) * q if pressure else 0.0), q
    h = -(R2 - R1) / n
    r, P, la = R2, 0.0, 0.5 * math.log(1 - 2 * m_tot / R2)
    for _ in range(n):   # RK4
        k1 = rhs(r, P, la)
        k2 = rhs(r + h / 2, P + h / 2 * k1[0], la)
        k3 = rhs(r + h / 2, P + h / 2 * k2[0], la)
        k4 = rhs(r + h, P + h * k3[0], la)
        P += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        la += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        r += h
    return dict(m=m_tot, rho0=rho0, alpha_R2=math.sqrt(1 - 2 * m_tot / R2), alpha_in=math.exp(la), P_R1=P)
