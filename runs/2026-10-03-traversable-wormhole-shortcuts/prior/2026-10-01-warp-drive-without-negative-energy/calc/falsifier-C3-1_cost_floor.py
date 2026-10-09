"""Falsifier C3-1: is the photon rocket really the cost floor for starting and
stopping the 2024 warp shell (M = 4.511e27 kg incl. 1e5 kg payload, v = 0.04 c)?

SI units throughout. Compares, for start + stop (two legs, each delta-p = gamma M v):
  (a) ideal photon rocket (C3's floor): mass ratio (1+b)/(1-b), exhaust energy (m_i - m_f) c^2
  (b) self-contained reaction-mass rocket with optimal fixed exhaust speed u (relativistic
      rocket equation, exhaust kinetic energy counted as the energy cost): mass ratio vs energy
  (c) external beam on a perfect reflector (no recycling), Doppler-exact, per leg
  (d) external beam with photon recycling N passes (Bae-type), low-speed estimate pc/(2N),
      floored by energy conservation at the kinetic energy delivered
  (e) kinetic energy (gamma-1) M c^2: floor for any scheme that does not recover energy
"""
import math

c = 2.99792458e8
M = 4.511e27            # kg, shell + payload (final mass, as in M-MECHANIST-08)
b = 0.04
g = 1 / math.sqrt(1 - b * b)
p = g * M * b * c       # momentum per leg
KE = (g - 1) * M * c**2
world_yr = 592.2e18     # J/yr (dossier value, quoted in M-MECHANIST-08)

print(f"momentum per leg p = {p:.4e} kg m/s")
print(f"kinetic energy at 0.04c KE = {KE:.4e} J")

# (a) photon rocket, start+stop, final mass M
R_ph = (1 + b) / (1 - b)
E_ph = (R_ph - 1) * M * c**2
print(f"(a) photon rocket start+stop: mass ratio {R_ph:.5f}, exhaust energy {E_ph:.4e} J "
      f"= {E_ph/world_yr:.3e} world-years; E/KE = {E_ph/KE:.1f}")

# (b) relativistic reaction-mass rocket, exhaust speed u (fraction of c), total delta-rapidity 2*atanh(b)
dchi = 2 * math.atanh(b)
best = None
for i in range(1, 200001):
    u = i * 1e-5            # u/c from 1e-5 to 2.0 -> restrict below 1
    if u >= 1:
        break
    if dchi / u > 700:
        continue
    ratio = math.exp(dchi / u)   # Ackeret relativistic rocket: dchi = (u/c) ln(m_i/m_f)
    # exhaust energy in the instantaneous rest frame: rest-mass lost (m_i - m_f) c^2 splits into
    # exhaust rest mass m_ex and exhaust kinetic energy; per unit rest-mass lost, exhaust KE fraction
    # = 1 - sqrt(1-u^2) (gamma_ex m_ex = dm, KE = (gamma_ex - 1) m_ex = dm (1 - 1/gamma_ex)).
    E_kin = (ratio - 1) * M * c**2 * (1 - math.sqrt(1 - u * u))
    if best is None or E_kin < best[2]:
        best = (u, ratio, E_kin)
u, ratio, Ebest = best
print(f"(b) optimal reaction-mass rocket: u = {u:.4f} c, mass ratio {ratio:.3f}, "
      f"exhaust kinetic energy {Ebest:.4e} J; photon/optimal = {E_ph/Ebest:.1f} "
      f"({math.log10(E_ph/Ebest):.2f} orders)")
# mass ratio at u -> c recovers the photon rocket
print(f"    check u->c: exp(dchi/0.99999) = {math.exp(dchi/0.99999):.5f} "
      f"vs photon {R_ph:.5f}; any u<c gives a larger mass ratio (mass-ratio floor holds)")

# (c) perfect reflector pushed by an external beam from rest to b (exact):
# energy delivered to sail per unit beam energy; integrate dE_beam with Doppler.
# For a mirror moving at beta, beam energy dE_b reflected gives dp = (dE_b/c)(1+ (1-beta)/(1+beta)) ... use
# standard result: beam energy needed to reach beta from rest = M c^2 * (gamma(1+beta)-1)/... compute numerically.
n = 200000
Eb = 0.0
bb = 0.0
dbeta = b / n
for k in range(n):
    bm = (k + 0.5) * dbeta
    gm = 1 / math.sqrt(1 - bm * bm)
    dp = M * c * gm**3 * dbeta          # d(gamma M beta c)
    # momentum transfer per unit incident lab-frame beam energy for a receding mirror:
    # incident E, reflected E (1-bm)/(1+bm): dp = (E/c)(1 + (1-bm)/(1+bm)) = (2E/c)/(1+bm)
    # but beam energy that reaches the mirror per unit time also reduced; count energy that hits the mirror.
    Eb += dp * c * (1 + bm) / 2
print(f"(c) reflective sail, start leg, beam energy hitting mirror = {Eb:.4e} J "
      f"= {Eb/(E_ph/2):.3f} of one photon-rocket leg; on-board mass lost = 0")
for N in (1, 100, 1540, 3000):
    EN = max(p * c / (2 * N), KE)
    print(f"(d) recycled beam N = {N:5d}: beam energy per leg ~ max(pc/2N, KE) = {EN:.4e} J "
          f"= {EN/(E_ph/2):.4f} of a photon-rocket leg")
print(f"(e) KE floor / photon-rocket leg = {KE/(E_ph/2):.4f}  ({math.log10((E_ph/2)/KE):.2f} orders below)")
print(f"    photon-rocket start+stop energy in world-years {E_ph/world_yr:.3e} (log10 {math.log10(E_ph/world_yr):.2f}); "
      f"KE x2 in world-years {2*KE/world_yr:.3e} (log10 {math.log10(2*KE/world_yr):.2f})")
print("PASS" if abs(math.exp(dchi) - R_ph) < 1e-12 else "FAIL", "identity exp(2 atanh b) = (1+b)/(1-b)")
print("PASS" if ratio > R_ph else "FAIL", "optimal-energy reaction rocket needs a larger mass ratio than the photon rocket")
print("PASS" if Ebest < E_ph else "FAIL", "optimal-energy reaction rocket needs less energy than the photon rocket")
