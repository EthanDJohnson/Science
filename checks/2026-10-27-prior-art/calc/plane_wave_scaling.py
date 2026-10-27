"""Small-angle scaling of g g -> gamma gamma from B&O eq. 6 (|M| = 8 pi G t^2/s or u^2/s).

Question: for two gravitons of energy w that are nearly parallel (relative angle theta, as in a
plane wave or in a distant part of a spherical wave), how do the amplitude, the cross-section and
the reaction rate scale with theta?  Units G = 1, hbar = c = 1.

Only the invariants matter: s = 2 w^2 (1 - cos theta), t = -s (1 - cos phi)/2, u = -s (1 + cos phi)/2
with phi the CM scattering angle. Then |M| ~ 8 pi G t^2/s ~ s, so |M|^2 ~ s^2, the 2-body massless
phase-space factor is 1/(8 pi) (s-independent), the cross-section is sigma = |M|^2/(2 s) * PS ~ s,
and the rate per pair of beams is  sigma * v_Moller with v_Moller = (1 - cos theta) ~ s/(2 w^2), so
rate ~ s^2 ~ theta^4.  The script checks these exponents numerically (log-log slopes) with the
helicity amplitudes A++++ = A---- = 8 pi G t^2/s and A++-- = A--++ = 8 pi G u^2/s summed over
final-state photon helicity configurations as B&O's eq. 6 does (pattern only; it does not
settle phases, which is point P1 and is not used here).

Usage: python3 plane_wave_scaling.py
"""
import numpy as np

G = 1.0
w = 1.0


def sigma_of_s(s, n=20001):
    """Angle-integrated |M|^2 / (2 s) / (8 pi), summed over the two eq.-6 amplitudes (1/2 for identical photons)."""
    cphi = np.linspace(-1.0, 1.0, n)
    t = -s * (1.0 - cphi) / 2.0
    u = -s * (1.0 + cphi) / 2.0
    m_tt = 8 * np.pi * G * t**2 / s
    m_uu = 8 * np.pi * G * u**2 / s
    m2 = m_tt**2 + m_uu**2
    ps = 1.0 / (8 * np.pi)  # two-body massless phase space integrated over solid angle = 1/(8 pi) x (dcos/2)
    integrand = m2 * ps / 2.0  # d cos(phi)/2 average
    sigma = np.trapezoid(integrand, cphi) / (2 * s) * 0.5  # 1/2 identical photons
    return sigma


def main():
    thetas = np.array([1e-1, 3e-2, 1e-2, 3e-3, 1e-3])
    rows = []
    for th in thetas:
        s = 2 * w**2 * (1 - np.cos(th))
        amp = 8 * np.pi * G * (s / 4.0)  # |M| at phi = pi/2 -> t^2/s = s/4 (reference value)
        sig = sigma_of_s(s)
        vm = 1 - np.cos(th)
        rate = sig * vm
        rows.append((th, s, amp, sig, rate))
        print(f"theta={th:8.1e}  s={s:10.3e}  |M|(phi=pi/2)={amp:10.3e}  sigma={sig:10.3e}  sigma*vMoller={rate:10.3e}")
    rows = np.array(rows)
    lt = np.log(rows[:, 0])
    for name, col in (("|M|", 2), ("sigma", 3), ("rate = sigma*v_Moller", 4)):
        slope = np.polyfit(lt, np.log(rows[:, col]), 1)[0]
        print(f"log-log slope of {name:22s} vs theta: {slope:6.3f}")
    print("Expected slopes: |M| -> 2, sigma -> 2, rate -> 4 (so ~ (lambda/r)^4 for theta ~ lambda/r).")


if __name__ == "__main__":
    main()
