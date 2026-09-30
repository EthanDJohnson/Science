"""falsifier-C1-0: does the QGEM phase carry any problem-of-time content?

SI units throughout. Uses mpmath at 50 digits so that O(1e-38) effects are resolved.

Part A. Bose et al. 2017 write the phase with ONE external time tau common to all
branches: phi_ij = G m1 m2 tau / (hbar r_ij).  Christodoulou-Rovelli re-read the same
number as a rest-mass clock phase m c^2 dtau / hbar with dtau = tau * G m /(c^2 r).
Show the two readings give identical numbers (algebraic identity), so observing the
phase cannot tell 'absolute Newtonian time + branch-dependent potential' from
'superposed proper times'.

Part B. The only piece of the phase that depends on WHICH time runs in each branch
(external lab time tau versus the branch's own proper time tau_b = tau(1 - Phi_b/c^2))
is the second-order term phi * (Phi_b/c^2).  Compute its size.

Part C. Discrimination power among C2..C6: all predict the same leading phase
(candidates.md line 67 'shared with C3-C5'; C6's GPP decoherence exponent is also computed).
"""
import mpmath as mp

mp.mp.dps = 50
G = mp.mpf('6.67430e-11')      # m^3 kg^-1 s^-2
c = mp.mpf('299792458')         # m/s
hbar = mp.mpf('1.054571817e-34')  # J s
tP = mp.sqrt(hbar * G / c**5)   # s

m = mp.mpf('1e-14')             # kg, each mass (Bose et al. 2017)
d = mp.mpf('450e-6')            # m, centre separation
dx = mp.mpf('250e-6')           # m, half-splitting
for tau in (mp.mpf(1), mp.mpf('2.5')):
    rs = {'LR(near)': d - dx, 'mid': d, 'RL(far)': d + dx}
    print(f"=== tau = {mp.nstr(tau,3)} s ===")
    # Part A: Newtonian external-time phases vs rest-mass proper-time phases
    for k, r in rs.items():
        phi_newton = G * m * m * tau / (hbar * r)
        dtau_proper = tau * G * m / (c**2 * r)          # s, redshift of mass 2's clock in mass 1's potential
        phi_proper = m * c**2 * dtau_proper / hbar
        print(f"A {k:9s} r={mp.nstr(r,4)} m  phi_Newton={mp.nstr(phi_newton,12)} rad"
              f"  phi_propertime={mp.nstr(phi_proper,12)} rad  diff={mp.nstr(phi_newton-phi_proper,3)} rad"
              f"  dtau={mp.nstr(dtau_proper,4)} s")
    dphi = G*m*m*tau/hbar*(1/(d-dx) - 1/(d+dx))
    print(f"A witness phase (near - far) = {mp.nstr(dphi,6)} rad")
    # Part B: branch-time ambiguity: replace tau by branch proper time tau(1 - Phi/c^2)
    # Phi = G m / r (self-consistent potential of partner) and Earth term g*h common to branches
    for k, r in rs.items():
        frac = G * m / (c**2 * r)                        # dimensionless
        phi = G*m*m*tau/(hbar*r)
        print(f"B {k:9s} branch-time correction to phase = phi*Phi/c^2 = {mp.nstr(phi*frac,4)} rad"
              f"  (fraction {mp.nstr(frac,4)})")
    # Earth potential difference across a vertical splitting 2*dx (if interferometer vertical)
    g = mp.mpf('9.80665')
    frac_earth = g * 2 * dx / c**2
    print(f"B Earth redshift across 2*dx = {mp.nstr(frac_earth,4)} (fraction) ; fixed-background, not superposed-source")
    # Part C: GPP (C6) decoherence exponent for the spatial superposition, using energy difference
    # of the gravitational interaction between branches as omega12
    omega12 = G*m*m*(1/(d-dx) - 1/(d+dx))/hbar          # rad/s
    expo = mp.mpf(3)/2 * tP**(mp.mpf(4)/3) * tau**(mp.mpf(2)/3) * omega12**2
    print(f"C omega12 (branch energy split) = {mp.nstr(omega12,4)} rad/s ; GPP exponent = {mp.nstr(expo,4)}")
    print(f"C => C2..C6 predicted witness phases agree to within ~{mp.nstr(expo,2)} (dimensionless)")
print("t_P =", mp.nstr(tP, 6), "s")
