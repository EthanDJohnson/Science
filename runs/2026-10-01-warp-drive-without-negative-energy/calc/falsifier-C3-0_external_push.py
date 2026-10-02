"""Falsifier C3-0: is the photon rocket really the cost floor for starting and stopping a shell?

SI units throughout. c = 299792458 m/s.
M = 4.511e27 kg (shell 4.511e27 kg incl. 1e5 kg payload, final-mass convention of M-MECHANIST-08).
Compares, for start + stop at v = 0.04 c and at the corrected cap beta = 0.0239:
 (a) ideal photon rocket (isolated, self-contained, null exhaust): exhaust energy and mass ratio;
 (b) isolated vehicle with MASSIVE reaction mass m_r = k*M left behind (exact 2-body relativistic kinematics):
     energy released and mass ratio (shows the photon rocket minimises mass ratio, not energy);
 (c) externally pushed: perfect-mirror light sail, single bounce (exact relativistic integral), shell mass ratio = 1;
 (d) externally pushed against a much heavier body (mass driver / N-bounce recycling limit): energy floor = (gamma-1) M c^2.
"""
import math

c = 299792458.0
M = 4.511e27          # kg, final rest mass (shell + payload)
m_pay = 1e5           # kg
world_year = 5.922e20  # J/yr (592.2 EJ, as quoted in M-MECHANIST-08)


def photon_rocket(v):
    r = (1 + v) / (1 - v)              # start + stop, initial/final mass
    E = (r - 1) * M * c**2             # exhaust energy, final-mass convention
    return r, E


def ke(v, m=M):
    g = 1 / math.sqrt(1 - v * v)
    return (g - 1) * m * c**2


def reaction_mass(v, k):
    """One leg, isolated, from rest: shell (rest mass M, final) at v, reaction mass k*M (rest mass)
    recoils with equal and opposite momentum. Energy released Q = sum of final energies - sum of rest energies."""
    g = 1 / math.sqrt(1 - v * v)
    p = g * M * v * c
    mr = k * M
    E_r = math.sqrt((mr * c**2)**2 + (p * c)**2)
    Q = (g * M * c**2 - M * c**2) + (E_r - mr * c**2)
    # mass ratio counting the reaction mass and the fuel mass-energy Q/c^2 as initial mass
    ratio = (M + mr + Q / c**2) / M
    return Q, ratio


def sail_single_bounce(v, n=200000):
    """Perfect mirror, normal incidence, beam from the rest frame. dE_beam = M c^2 (1+b)/2 gamma^3 db."""
    s = 0.0
    h = v / n
    for i in range(n):
        b = (i + 0.5) * h
        s += (1 + b) / 2 * (1 - b * b)**-1.5 * h
    return s * M * c**2


for v in (0.04, 0.0239):
    print(f"=== v = {v} c ===")
    r, Epr = photon_rocket(v)
    print(f"(a) photon rocket start+stop: mass ratio {r:.5f}; exhaust energy {Epr:.4e} J = {Epr/world_year:.3e} world-years")
    K = ke(v)
    print(f"    kinetic energy per leg (gamma-1)Mc^2 = {K:.4e} J; start+stop without recovery 2KE = {2*K:.4e} J")
    print(f"    ratio photon-rocket exhaust / 2KE = {Epr/(2*K):.2f}")
    for k in (0.1, 1.0, 10.0, 1e3):
        Q, ratio = reaction_mass(v, k)
        # two legs: second leg starts from the (lighter) moving vehicle; to keep it simple quote per-leg x2 as energy
        print(f"(b) isolated, massive reaction mass k={k:g} M per leg: energy released per leg {Q:.4e} J "
              f"(x2 = {2*Q:.4e} J, {2*Q/Epr:.4f} of photon-rocket exhaust); one-leg mass ratio {ratio:.4f} "
              f"vs photon-rocket one-leg {math.sqrt(r):.5f}")
    Es = sail_single_bounce(v)
    print(f"(c) perfect-mirror sail, single bounce, per leg: beam energy {Es:.4e} J = {Es/(M*c**2):.5f} Mc^2; "
          f"x2 = {2*Es:.4e} J = {2*Es/Epr:.3f} of photon-rocket exhaust; shell mass ratio 1")
    print(f"    small-v check: Mc^2 (v/2 + v^2/4) = {M*c**2*(v/2+v*v/4):.4e} J")
    print(f"(d) N-bounce recycling / mass driver floor -> 2KE = {2*K:.4e} J = {2*K/world_year:.3e} world-years; "
          f"shell mass ratio 1")
    print(f"    payload-alone 2KE = {2*ke(v, m_pay):.4e} J; shell/payload bill ratio = {M/m_pay:.4e} (mechanism-independent)")
    # momentum per leg
    g = 1 / math.sqrt(1 - v * v)
    print(f"    momentum per leg gamma M v = {g*M*v*c:.4e} kg m/s")
    print()

# consistency: photon rocket per-leg ratio equals e^{rapidity}
for v in (0.04, 0.0239):
    print(f"check e^atanh(v) = {math.exp(math.atanh(v)):.6f}, sqrt((1+v)/(1-v)) = {math.sqrt((1+v)/(1-v)):.6f}")
# limit v -> 0: photon-rocket exhaust / KE -> 2c/v  (per leg: v M c^2 vs v^2 M c^2/2)
for v in (1e-3, 1e-2, 0.04):
    print(f"v={v}: per-leg photon exhaust/KE = {(math.sqrt((1+v)/(1-v))-1)/(1/math.sqrt(1-v*v)-1):.2f}, 2/v = {2/v:.2f}")
