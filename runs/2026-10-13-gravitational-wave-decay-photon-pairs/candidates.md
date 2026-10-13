# Candidate answers
exclusive: no (C1 excludes C2–C5 on the headline question, and C3 and C4 conflict on the size of the physical near-source yield; C6–C8 answer sub-questions Q2 and Q4 and are compatible with C2–C5)
lenses merged: mechanist, examiner, empiricist, dialectician, idealizer, constraints (analyses/*.md), each read against its math check in math/<lens>.md
status: final

Conventions. B&O = Blas & Oller, arXiv:2607.24930 v2. Units: natural units (hbar = c = 1, Heaviside–Lorentz) for amplitudes, coefficients and rates; SI for astrophysical numbers, as marked. "Pairs" are photon pairs (photons = 2 x pairs). GW150914 reference inputs are B&O's (E_rel = 2 Msun c^2, f = 150 Hz, sigma_w = 200 rad/s) [D-27] unless stated; the LVK 2016 value E = 3.0 Msun c^2 [D-28] multiplies every pair number by 2.25. "[M-...]" cites the math-check row that re-derived a number. Calc paths are relative to the project root.

Math-check status carried into this slate:
- Refuted: M-MECHANIST-02 (mechanist finding 2: "aligned linear polarisations reproduce B&O's real-sign eq. 7 value, flat in photon azimuth"). Corrected form, used below: for a single collision axis the two opposite-helicity channels interfere only as cos(8 phi + const) in photon azimuth, so B&O's real-sign value is the azimuthal maximum, and the azimuth-integrated rate equals the incoherent sum; a linearly polarised pair gives 6/7 of B&O's per-collision value, a pure (+2,-2) pair 12/7, same helicity 0. Coherent summation over many collision axes was not addressed.
- Refuted: M-DIALECTICIAN-10 (an O(1) coefficient only). The unpolarised collinear factor is sigma(1 - cos theta) = (pi/5) G^2 w^2 theta^4 (natural units), not (2 pi/5); the theta^4 law stands.
- Unverified: the toolkit's physical-pattern coefficients (circular binary 0.562, linear quadrupole 0.3125, isotropic_plus 0.225, pure circular 0 relative to B&O) and the coherent-versus-kinetic ratios 0.982 and 0.931 [M-MECHANIST-06, M-EXAMINER-12, M-IDEALIZER-14]; eq. 17's v^6 and 1/128 [M-EMPIRICIST-07]; the binning claim of idealizer F12 [M-IDEALIZER-15]; the linear-channel scaling P_lin ~ k (hbar w/E_Pl)^2 N, whose coefficient k is uncomputed (M-EXAMINER-09 checks only the arithmetic built on it).

## C1: A freely propagating gravitational wave decays into photon pairs in vacuum at B&O's eq. 8 rate, sustained along its path, giving a finite lifetime and cumulative path depletion.
type: mechanism
from: MECHANIST-C, EXAMINER-C, EMPIRICIST-C, DIALECTICIAN-E, IDEALIZER-C, CONSTRAINTS-E; large-attenuation variant EMPIRICIST-E, CONSTRAINTS-G
argument: B&O's chain:
- a coherent graviton state D(f)|0> whose field is sqrt(8 pi G) Int Delta_rad T_s, with Delta_rad "the Pauli-Jordan function" (eq. 5) [D-10];
- tree-level g g -> gamma gamma amplitudes (eq. 6) combined into a real-sign "unpolarized" amplitude (t^2 + u^2)/s (eq. 7) [D-12];
- 2 pi delta(0) -> T with T ~ 1/sigma_w, giving dP/dt = 3 G^2 N^2 w_s^3 sigma_w^2/(25 pi) (natural units; a pair rate) [D-14, D-21].

B&O read this as a decay that persists along the path: "depleting at time τ_h = τE_rel/ω_s" (p. 3), and W_gamma is integrated over "the GW propagation sphere" in S12 (p. 11) [new: B&O v2, ACCESS full-text, quoted in dialectician F9 and constraints F6]. Inside B&O's model the arithmetic is right, reproduced by an independent route:
- 3/(25 pi) = (4/25)/(4 pi/3) [idealizer F1; M-IDEALIZER-01];
- scalar 7/(450 pi) and tau_phi = (54/7) tau [M-IDEALIZER-02];
- eqs. 9–12 and their hbar counting [M-IDEALIZER-03, M-CONSTRAINTS-04].

Named sub-hypotheses:
- (a) B&O size, GW150914 (SI): R = 1.4e-4 pairs/s, tau = 3.6e3 s, tau_h = 1.3e82 s; path depletion over 410 Mpc 3.3e-66 (vacuum) or 2.5e-57 (CMB-stimulated) [D-42, D-47; M-DIALECTICIAN-01, M-CONSTRAINTS-14]. The consequences built on it are the Fig. 2 photon luminosities, the footnote-4 flux at the sphere of radius c tau, and the eq. 19/S12 cosmological integration that feeds the Fig. 3 mu/y, EBL and photofission bounds [D-19; constraints F0].
- (b) large-attenuation variant (Jones & Singleton): G + G -> gamma gamma attenuation with decay length ~1e11 m at w ~ 1e2 s^-1, Gamma growing linearly in r [D-53; new: Jones & Singleton 2015, arXiv:1505.04843, ACCESS full-text (abstract via fetch_text), empiricist F8].
predictions: If true:
- the photon number counted beyond radius R grows linearly with R at R >> lambda, at an r-independent rate;
- B&O's eq. 19 energies follow, along with the Fig. 3 bounds;
- the GW energy lost over 410 Mpc is 3.3e-66 (unobservable);
- under variant (b), the GW150914 amplitude at 410 Mpc would carry a factor exp(-6.3e13) [M-CONSTRAINTS-14].

If false: the yield beyond R falls with R (C2), and eq. 8 is a per-packet quantity (C3/C4).
evidence for: The within-model arithmetic is verified (above). B&O's text explicitly reads the rate as a path decay [dialectician F9]. Tree-level g g -> gamma gamma is non-zero for non-collinear gravitons, |M| = 8 pi G t^2/s and 8 pi G u^2/s for opposite helicities [D-01; M-MECHANIST-01]. Size (a) is contradicted by no observation, because its predicted depletion lies 56–65 orders of magnitude below data [constraints F5; empiricist F4].
evidence against:
- **Collinear kinematics.** The local two-beam rate falls as theta^4 for nearly collinear gravitons. For h = 1e-21 and 150 Hz it is 2.9e-101 m^-3 s^-1 head-on and 1.8e-110 m^-3 s^-1 at 0.01 rad (SI) [mechanist F3; M-MECHANIST-03]. The unpolarised coefficient is pi/5, not 2 pi/5 [M-DIALECTICIAN-10, refuted coefficient only; DIALECTICIAN-E cited the uncorrected form].
- **Plane waves produce nothing.**
  - An exact plane-wave source has Fourier support only on q^2 = 0, so its yield is zero [examiner F4; M-EXAMINER-06].
  - In geometric optics Gamma(x) = (2 pi/5) G^2 T_mn T^mn, which vanishes for null stress [idealizer F5; M-IDEALIZER-06].
  - The pp-wave null dust has G_ab G^ab = 0 [M-CONSTRAINTS-13].
  - B&O concede that a single plane wave produces nothing [D-17]. The no-go results [D-56, D-57, D-60] agree.
- **The yield beyond R of a retarded outgoing wave converges.** Three independent toys find it falling as (w R)^-3:
  - examiner: smooth windows, R^-2 for a sharp cut, convergent either way [M-EXAMINER-04];
  - constraints: slope -2.995 at w R = 320 [M-CONSTRAINTS-08];
  - idealizer: exact asymptote 0.0632 (kr)^-3 for an l = 2 mode with m = 2 [M-IDEALIZER-07/08];
  - mechanist's shell estimate gives r^-3 to r^-5 [M-MECHANIST-04].
- **The rate step is bookkeeping.**
  - P = R x T_eff, with T_eff = 4 pi/(3 sigma) = 0.021 s, gives 2.9e-6 pairs per GW150914 packet.
  - Reading R as sustained over 410 Mpc over-counts by t_prop/T_eff = 2.0e18 [dialectician F1–F2; M-DIALECTICIAN-01, M-DIALECTICIAN-02].
  - B&O's own condition tau << 1/sigma fails by tau sigma = 7.2e5 [D-61].
- **Eq. 19 over-counts and breaks energy conservation.**
  - It over-counts each burst by X = sigma t_prop = 6.6e21 to 6.6e41 across 1e-10 to 1e10 eV.
  - It breaks energy conservation at the top of Fig. 3: C X = 34 at 1e10 eV for L = 1e-3 c^5/G [constraints F10; M-CONSTRAINTS-07].
- **Plasma closes the channel.**
  - g g -> gamma gamma is kinematically forbidden for w < w_p: warm ISM 1.56 kHz, VLISM 2.54 kHz [M-CONSTRAINTS-09, M-IDEALIZER-13].
  - In the mean IGM, production at 150 Hz stops beyond r_max = 4.0e8 to 3.2e9 m (SI) [constraints F1].
- **Variant (b) is excluded by observation.**
  - GW150914 was seen at 410 Mpc with <= 11.29% amplitude calibration, which requires an energy e-folding length > 5.3e25 m [M-CONSTRAINTS-14; D-39].
  - GW170817 gives c_M = -9 +21 -28 (68%), i.e. d_GW/d_EM - 1 in [-0.17, +0.06] [new: Lagos et al. 2019, PRD 99, 083504, ACCESS full-text (arXiv abstract page), empiricist F4; M-EMPIRICIST-05].
decisive test: A spin-2 in-in (Schwinger–Keldysh) calculation at O(G^2) of the photon number made beyond radius R by the retarded field of a quadrupole source (a circular binary), with the source in the Hamiltonian.
- C1 needs d ln P(>R)/d ln R = +1 at R >> lambda. C2 predicts about -3, or at least below -1. The sign of the slope settles it.
- Who could do it: any group using the coherent-state waveform formalisms [D-02, D-03] or the Redi–Tesi functional [D-60], or B&O themselves.
- When: none is published as of 2026-10-13 [D-66; dossier section 6].

## C2: No vacuum decay: an outgoing gravitational wave's photon-pair production converges within a few wavelengths of its source, so there is no lifetime, no path depletion and nothing observable.
type: null
from: MECHANIST-A, EXAMINER-B, CONSTRAINTS-A, EMPIRICIST-A, IDEALIZER-A (its no-decay half), DIALECTICIAN-A (its no-decay half); strong variant DIALECTICIAN-F, IDEALIZER-E, CONSTRAINTS-H
argument:
- **Kinematics.** Pair production needs a time-like total momentum q = k1 + k2, with s = 2 w1 w2 (1 - cos theta_12) > 0 [D-55; M-MECHANIST-09]. With sigma ~ G^2 s and a flux factor (1 - cos theta), the local rate goes as theta^4 [M-MECHANIST-03; coefficient per M-DIALECTICIAN-10].
- **An outgoing wave becomes locally plane.** The Fresnel spread is theta^2 ~ 1/(w r), so s ~ 4 w c/r. The toy confirms that the time-like content sits at kappa ~ 1/R [constraints F4; M-CONSTRAINTS-08].
- **Production beyond R falls as (lambda/2 pi R)^3.**
  - Constraints, as fractions of the near-zone yield for GW150914 (SI): 4.0e-3 beyond R = lambda, 9.6e-18 beyond 1 AU, 1.6e-59 beyond 410 Mpc [M-CONSTRAINTS-08].
  - Examiner toy: 2.7e-3 beyond w R = 10 and 2.9e-6 beyond w R = 100, with a window uncertainty of about 2x [M-EXAMINER-04, M-EXAMINER-07].
  - Idealizer, with the corrected asymptote 0.0632 (kr)^-3: 7.5e-10 pairs beyond lambda, 1.8e-24 beyond 1 AU, 2.9e-66 beyond 410 Mpc [M-IDEALIZER-09].
  - Convergence needs only a local spread falling faster than a fixed power; even a constant spread converges as 1/r [M-MECHANIST-04].
- **Consequences that rest on sustained emission fall.** These are Fig. 2 read as a luminosity along the path, the footnote-4 flux at radius c tau, tau_h, eq. 19/S12, and the Fig. 3 CMB, EBL and photofission bounds.
  - Eq. 19 over-counts each GW150914 burst by sigma t_prop = 8.4e18 [examiner F6; M-EXAMINER-07], and X = 6.6e21 to 6.6e41 across the Fig. 3 range [M-CONSTRAINTS-07].
  - No corrected photon bound beats the gravitational DeltaN_eff bound on the same GWs below hbar w ~ 0.1 E_Pl [constraints F9; M-CONSTRAINTS-06].
  - The photofission and EBL source classes are subsumed by their own Hawking evaporation bounds, which are stronger by >= 3e2 [constraints F11; M-CONSTRAINTS-11].
  - Hz-kHz photons are forbidden in the warm ISM, the VLISM, the solar wind and the ionosphere, and in the early universe at 1+z > ~1300 for photons of 150 Hz today (1+z > 1261–1269 per the checks) [D-62; M-CONSTRAINTS-09, M-EXAMINER-10, M-IDEALIZER-13].
- **The question is observationally empty.** B&O's predictions and zero cannot be told apart by any channel; every one falls short by >= 1e30 [empiricist F10, O4; D-45, D-46, D-47].
- **Scope.** The null does not deny production near the source (C3–C5) or in multi-directional ensembles (C6).
- **Strong variant (named, not claimed).** "Identically zero for every vacuum GW configuration" is rated strained or eliminated by the lenses. Tree-level fusion of non-collinear gravitons is non-zero [D-01], eq. 14 is non-zero [M-IDEALIZER-05], and colliding plane waves do produce particles [D-04].
predictions: If true:
- the in-in yield of a retarded outgoing packet beyond R falls faster than R^-1 (toys: R^-3) and saturates at a near-source total;
- no standard-siren GW/EM distance comparison shows path loss beyond GR;
- no Hz-kHz photon or spectral-distortion signal is ever attributed to GWs.

If false: some non-collinear component survives at r >> lambda (quadrupole angular structure, nonlinear memory, tails) and gives a yield that grows with R.
evidence for:
- The kinematic and toy calculations above.
- The plane-wave no-go results: Gibbons, for a massive scalar only [D-56]; Khusnutdinov, for massless scalar and vector fields [D-57]; Deser, search-summary only and unverified [D-58]; the Redi–Tesi time-like-support rule [D-60]. B&O concede the plane-wave case [D-17].
- Analogues: light-by-light scattering has been seen only with crossing photons in extreme fields [new: ATLAS 2017, arXiv:1702.01625, ACCESS full-text (abstract via fetch_text), empiricist F9]. The QED single-plane-wave null is cited by empiricist as general knowledge, not fetched.
evidence against:
- **The r-dependence rests on toys.** Every r-dependence result comes from a scalar toy (monopole or l = 2) or a geometric-optics kinetic proxy, never a spin-2 in-in calculation [scope notes in math/examiner.md, math/idealizer.md, math/constraints.md].
- **The exponent is not robust.** It depends on the window sharpness (a sharp cut tends to R^-2) [M-EXAMINER-04] and on the vertex weight s^p (exponent -(p+1)) [M-CONSTRAINTS-08].
- **The angular-spread premise is unsourced.** theta ~ (kr)^-1/2 or (kr)^-1 has no source [D-55; dossier section 6].
- **Memory and tails are not computed.** Constraints flags them as the possible exception and expects them to make pairs only of energy <~ hbar sigma [constraints, What would change my mind].
- **The collinear Bogoliubov dispute is open** [D-51], though in that sector the amplitude vanishes [D-13].
decisive test: The same spin-2 in-in retarded calculation as in C1, including the second-order memory and tail terms at q0 ~ 2w, gives the slope of P(>R).
- Observationally, only large damping is testable: standard-siren GW/EM distance ratios at the ~1e-2 level in later observing runs [empiricist, What would change my mind]. LVK IR1 is planned from November 2026, and O5 has no fixed date [D-70].

## C3: Eq. 8 is right arithmetic for the wrong state: the per-packet yield of a time-symmetric, imploding-then-re-expanding graviton shell, so a real source's outgoing wave yields substantially less.
type: reframe
from: EXAMINER-A, DIALECTICIAN-A (its rate-as-total half), IDEALIZER-A (its eq. 8 half), MECHANIST-B (its state and focus part; its eq. 7 part restated per M-MECHANIST-02)
argument:
- **Which field the state carries.**
  - B&O's eq. 5 field uses the Pauli-Jordan function [D-10], which is G_ret - G_adv.
  - As a free in-state it equals the retarded outgoing wave after the source and minus the advanced (converging) wave before it: a shell that implodes onto the source and re-expands [examiner F1, mechanist F7].
  - The mathematics is verified [M-EXAMINER-01, M-MECHANIST-07]. Whether B&O's state is exactly this in-state is a reading of the source [D-71a]; "used as in-state" was not found verbatim [D-10].
- **Where the yield comes from (scalar monopole toy).**
  - The purely outgoing and purely incoming self-terms have exactly zero time-like Fourier amplitude [M-EXAMINER-02].
  - The whole yield comes from the head-on incoming x outgoing cross term within |t|, r <~ c/sigma of the source [examiner F2; M-EXAMINER-05].
  - The idealizer's standing-wave (in + out) proxy reproduces B&O's in-state total to O(1): R(>1) ≈ 1.1 after correcting the plateau from 1.21 to 1.36 [idealizer F6; M-IDEALIZER-07/08].
- **The retarded field yields less, for the same late-time wave and the same N (natural units).**
  - Examiner toy: 1/12 of the time-symmetric total for a contact vertex (exact) and 0.020 for |M|^2 ∝ s^2 [M-EXAMINER-03].
  - Idealizer outgoing proxy, yield beyond kr = 1: 0.069 of B&O's total (lens value; the small-kr entries were not independently integrated) [idealizer F6; M-IDEALIZER-08].
  - Mechanist shell, beyond 1/k: 4e-8 to 7e-8 pairs, against B&O's 2.9e-6, i.e. 0.014–0.024 [M-MECHANIST-04, M-MECHANIST-05].
- **The 2 pi delta(0) -> T "rate" is this total divided by T_eff** = 4 pi/(3 sigma) (top hat) [dialectician F1; M-DIALECTICIAN-02].
- **The eq. 7 helicity sum overstates further** (corrected from the refuted mechanist F2).
  - For a single collision axis, B&O's real-sign sum is the azimuthal maximum, not a realisable total.
  - Azimuth-integrated per-collision factors relative to B&O: linear pair 6/7, pure (+2,-2) 12/7, same helicity 0. The per-axis range is [0, 12/7] [M-MECHANIST-02, M-MECHANIST-01].
  - The toolkit's whole-state pattern factors are 0.562 (circular binary), 0.3125 (linear quadrupole) and 0 (pure circular). They are unverified, and the math check advises care because they combine helicity channels across azimuths [M-MECHANIST-06, M-IDEALIZER-14].
- **Named sub-hypotheses.**
  - (a) B&O's dropped Feynman-propagator term [D-18] is what selects the time-symmetric field [examiner hardest question 10].
  - (b) The in-out probability equals the in-in mean pair number at this order [D-03; examiner premise 13], so the discrepancy lies in the state and not in the observable.
predictions: If true:
- <h> of B&O's state at t = -10/sigma, r = 10 c/sigma is a non-zero incoming shell;
- a retarded-source in-in total at O(G^2) is about 0.02–0.1 x (eq. 8 x T_eff), before pattern factors, and is made at r <~ 5 lambda/2pi;
- for GW150914 that is <~ 3e-7 pairs (SI; 0.1 x 2.9e-6).

If false: B&O's state carries only the retarded field, and the retarded total equals eq. 8 x T_eff to O(1) (C4).
evidence for: As above. The convergence of the outgoing yield (C2) is shared evidence.
evidence against:
- The toys are scalar (monopole, l = 2), not spin-2, and none includes the r < 1/w region of a real source, where the free-graviton model fails and an O(1) share could be made [examiner F7; idealizer F6, F8].
- B&O assert that the extra Feynman-propagator term "vanishes when convoluted with the external coherent states" [D-18].
- The idealizer reads B&O's numbers as "of the right order as an in-state idealisation" (IDEALIZER-B, i.e. C4).
- MECHANIST-B's original eq. 7 claim (aligned linear polarisations realise B&O's value) was refuted [M-MECHANIST-02]. It is used here only in its corrected form, which strengthens the "less" direction for a single axis but says nothing about multi-axis coherent sums.
decisive test:
- **Cheap, analytic:** evaluate B&O's eq. 5 field at early times. An incoming shell confirms the state identity [examiner hardest question 1].
- **Decisive:** a spin-2 in-in calculation with the retarded quadrupole source, giving the ratio of its total pair number to eq. 8 x T_eff. C3 predicts 0.02–0.1; C4 predicts 0.3–3.
- Who could do it: the same groups as in C1. Nothing is published [dossier section 6].

## C4: A real source produces a finite, distance-independent photon-pair total near itself, of the order of B&O's per-packet total (eq. 8 times ~1/sigma_w), far too small to observe.
type: mechanism
from: IDEALIZER-B, CONSTRAINTS-B, MECHANIST-B, DIALECTICIAN-A, DIALECTICIAN-D, EMPIRICIST-B
argument:
- **The invariant content of B&O's model is a total.**
  - P = (4/25) G^2 N^2 w^3 sigma (top hat, natural units). By Parseval this equals P = (12 pi/25) G^2 w Int L_GW(t)^2 dt / c^10 (SI) for any narrow-band profile, chirped profiles included [idealizer F3; M-IDEALIZER-04].
  - The dialectician's luminosity-set form 4 pi^2 c_rate G^2 L^2 w/c^10 with c_rate = 3/(25 pi) is the same law (identity: 4 pi^2 x 3/(25 pi) = 12 pi/25) [M-DIALECTICIAN-07].
- **Sizes for GW150914 (SI).**
  - 2.9e-6 pairs (rate x T_eff), or 6.6e-6 for E = 3 Msun c^2 [M-IDEALIZER-09].
  - 7.0e-7 to 1.6e-6 pairs (rate x 1/sigma), i.e. (3/(100 pi))(r_m/l)^2(w/sigma) with r_m/l = 3.9e-3 to 5.9e-3 [M-CONSTRAINTS-05].
  - 7e-6 to 1.4e-5 pairs from the profile-free law with L = 3.6e49 W for 5–10 ms [M-IDEALIZER-09].
  - Hoop cap: <~ 0.1 pairs per burst at sigma/w = 0.1 before stimulation, at any w and E [M-CONSTRAINTS-04].
  - CMB final-state stimulation (x 7.6e8 at 150 Hz) would give 5e2 to 1.2e3 pairs if it applied. That part is classical and needs propagating modes [M-CONSTRAINTS-05, M-EMPIRICIST-06; D-43].
- **Chirps.**
  - Whole-chirp yields: GW170817 (30 Hz–1.6 kHz) 2.8e-8 pairs; GW150914 inspiral (35–68 Hz) 2.8e-8 pairs; Galactic WD binary 4e-43 pairs per year.
  - The integrand grows as Omega^4, so the merger dominates [M-IDEALIZER-10].
  - B&O's Fig. 2a recipe keeps sigma_b = eps w for t_b > 1/(eps w), so it over-estimates its own model's chirp total by (sigma_b t_b/2 pi)^2: 36 for GW170817 at 100 Hz, and ~3.8e19 for a WD binary with an assumed t_eps = 1e13 s. Their "lower bound" is an upper bound [dialectician F4–F5; M-DIALECTICIAN-04/05/06; the crossover at 2 pi is approximate].
- **Where it is made.**
  - At r <~ c/w = 318 km = 3.3 GM/c^2 for GW150914, which is the merger itself, in the strong field [M-EXAMINER-08, M-IDEALIZER-09].
  - At ~3 orbital separations for GW170817 at 100 Hz, which is the near zone [M-EXAMINER-08].
  - The flat-space free-graviton model is therefore not valid where the yield is made [examiner F7, premise 12].
- **Down-factors.**
  - Physical patterns: 0.3–0.6 (unverified, see the header).
  - Corrected eq. 7: per-axis factors 6/7 (linear) to 12/7 (pure opposite helicity) [M-MECHANIST-02].
  - Finite bandwidth: -4.6% at sigma/w = 0.1 [M-IDEALIZER-01].
- **Unobservable.**
  - The conversion is W_gamma/L_GW = (6/(25 pi))(L/L_P)(hbar w/E_P)^2 ≈ 4e-85 for GW150914 (SI) [M-CONSTRAINTS-06].
  - 150 Hz photons need n_e < 2.8e-4 cm^-3 to propagate [D-62]. Their free-free absorption length in the IGM is 0.57–37 Mpc [M-CONSTRAINTS-10].
  - At face value the flux at Earth would be 1e-46 photons m^-2 s^-1, against a CMB Rayleigh-Jeans foreground 2e43 times brighter [D-46].
predictions: If true:
- the retarded in-in total per event lies within a factor ~3 of eq. 8 x T_eff (times pattern factors 0.3–0.6);
- it does not depend on the distance travelled;
- it scales as (r_m/l)^2 (w/sigma), and for chirps it tracks w Int L_GW^2 dt, not the bandwidth;
- it is zero in host gas with n_e > (f/8980 Hz)^2 cm^-3.

If false: the total is <~ 0.1 x (C3), another channel dominates (C5), or strong-field corrections change it by orders of magnitude.
evidence for: As above. B&O's eq. 13 itself calls binary luminosities "very weak", comparable to Hawking emission [D-19].
evidence against:
- C3's toys put the retarded share at 0.02–0.1 of B&O's total for r >~ 1/k [M-EXAMINER-03, M-IDEALIZER-08, M-MECHANIST-04]. The r < 1/w share that would restore O(1) is computed nowhere.
- The pattern factors are unverified.
- MECHANIST-B's eq. 7 statement was refuted and enters here only in its corrected form [M-MECHANIST-02].
- The idealizer's "binning reproduces the total" (F12) is unverified, and it fails for simultaneous non-chirping bands [M-IDEALIZER-15].
- B&O's narrow-band condition is only marginal at GW150914, sigma/w = 0.21 [D-61; mechanist F5].
decisive test: Feed numerical-relativity h_mn of a GW150914-like merger, including h^(2), into the Redi–Tesi functional with c_J = 16 [D-60], and compare the result with (12 pi/25) G^2 w Int L^2 dt / c^10 [mechanist M2, idealizer IDEALIZER-B].
- C4 predicts agreement within ~3. Not done or published.

## C5: Near a real source, photon pairs come mainly from the source's own dynamical field (off-shell linear channel during merger-ringdown, remnant Hawking emission), not from N^2 graviton fusion.
type: mechanism
from: EXAMINER-D; mechanist chain M3 and finding 10 (no candidate ID); constraints F11 (no candidate ID)
argument:
- **The production rule.** The Redi–Tesi pair yield from a classical metric perturbation is ∝ Int theta(q^2) |W(q)|^2 (gauge fields c_J = 16), with support on time-like q only [D-60].
- **Sub-hypothesis (a): the linear channel.**
  - The source's own off-shell field has time-like Fourier components, so it makes pairs with an amplitude linear in h.
  - Examiner's dimensional estimate is P_lin ~ k (hbar w/E_Pl)^2 N, against fusion's c_tot G^2 N^2 w^3 sigma.
  - So P_BO/P_lin = (c_tot/k) G E sigma/c^5: 3.2e-4/k for GW150914 (P_lin/k = 9.3e-3 pairs) and 3.0e-8/k for the GW170817 100 Hz bin [examiner F8; M-EXAMINER-09 checks the arithmetic only; k is uncomputed].
- **Sub-hypothesis (b): remnant Hawking emission.**
  - W_H/W_gamma = 341 for one 65 Msun BH and 2.7e3 for two components, independent of mass [constraints F11; M-CONSTRAINTS-11].
  - B&O's own eq. 13 gives 1e2 to 1e3 [D-19, D-43].
- **Sub-hypothesis (c): merger and ringdown.** At v ~ c these have time-like support and make massless quanta at O(h^2) [mechanist M3; D-52]. Their photon number is not extracted in any source [dossier section 6].
predictions: If true:
- the per-event pair yield near the source exceeds the N^2 fusion total;
- k >~ 3e-4 for GW150914;
- the yield scales as N (∝ E/(hbar w)) rather than N^2.

If false: k << 3e-4, and fusion (C3/C4) is the leading pair channel at the merger.
evidence for: The Redi–Tesi time-like-support rule [D-60]; Chakraborty et al.'s perturbative production by linear, non-plane GW profiles (scalars; photon size not extracted) [D-52]; the Hawking ratio [M-CONSTRAINTS-11].
evidence against:
- k is uncomputed. The scaling is dimensional analysis [math/examiner.md, Unverified].
- **The inspiral case fails.** For a quasi-circular inspiral the near-zone field oscillates at q0 = 2 Omega on scales ~a, so q0/|q| ~ v < 1. The support is space-like and gives no massless production; time-like support starts only beyond r > lambda_GW/pi [mechanist F10a; M-MECHANIST-10, verified for a single rigidly rotating harmonic]. That undercuts the GW170817 inspiral ratio and leaves only merger and ringdown.
- Hawking emission of the remnant is a separate process, not GW-induced. It competes only in the count of "pairs per event".
decisive test: Compute k for (i) a circular binary and (ii) an NR merger-ringdown, using the Redi–Tesi kernel with c_J = 16 and the source's T~ at time-like q [examiner hardest question 6].
- C5 survives if k >~ 3e-4 for GW150914.
- Mechanist F10a predicts k ≈ 0 for the inspiral phase.

## C6: Sustained vacuum fusion exists only in multi-directional ensembles: for an isotropic stochastic background B&O's eq. 14 is exactly the incoherent kinetic rate, and it is negligibly small.
type: mechanism
from: MECHANIST-D, DIALECTICIAN-B, IDEALIZER-D, CONSTRAINTS-D
argument:
- **Eq. 14 is exactly kinetic theory, derived three ways.**
  - Gamma/V = (1/2) n^2 <sigma (1 - cos theta)>, with sigma(RL) = (4 pi/5) G^2 s and sigma(RR) = 0, gives 8 pi G^2 rho^2/15 (natural units) = (8 pi/15) G^2 rho_E^2/c^7 (SI).
  - The result is hbar-free and independent of the spectrum [dialectician F10, idealizer F4, constraints F3; M-DIALECTICIAN-09, M-IDEALIZER-05, M-CONSTRAINTS-01].
  - The cross sections are toolkit inputs, consistent with the verified amplitudes [M-MECHANIST-01].
  - A second route, (2 pi/5) G^2 T_mn T^mn, gives the same [M-IDEALIZER-05].
- **Sizes (SI).**
  - 2.8e-109, 3.1e-110 and 7.7e-111 pairs m^-3 s^-1 at DeltaN_eff = 0.3, 0.1 and 0.05; 1.6e-115 at the LVK limit [M-CONSTRAINTS-02, M-IDEALIZER-11]. B&O's ~1e-110 matches DeltaN_eff ~ 0.05–0.1 [D-71d].
  - Delta rho/rho <= 4.3e-79 in the mu window (stimulated, plasma ignored), against FIRAS ~6e-5: a shortfall >= 1e71 [M-CONSTRAINTS-03].
  - Energy fraction converted per Hubble time: 1.5e-108 [M-IDEALIZER-11]. Depletion time: 6.8e115 s (stimulated) [M-CONSTRAINTS-03].
- **Plasma.** The 25 Hz LVK band makes no photons at z > 1100. Production at z = 1e5 needs f0 > 1.3 kHz [M-CONSTRAINTS-09].
- **Coherence adds nothing.** The coherent two-cap yield equals the kinetic rate x the overlap 4-volume (ratios 0.982 and 0.931; unverified) [idealizer F13; M-IDEALIZER-14].
predictions: If true:
- the rate scales as rho_GW^2, is independent of phase coherence, and vanishes for a collimated background;
- no CMB, EBL, N_eff or depletion signature appears at any planned sensitivity (PIXIE-class headroom is 3e3 in mu and 1e4 in y [D-36]).

If false: a coherent or anisotropic structure in real backgrounds, or a plasma or finite-temperature correction, changes the coefficient by more than O(1).
evidence for: Three independent derivations agree to 1e-8 [above]. The rate is the in-in rate for a random-phase background [constraints, validity domains; D-03].
evidence against:
- Treating Omega_GW(25 Hz) as the total rho_GW ignores bandwidth [D-44].
- Whether an ensemble rate counts as "decay of a GW in vacuum" in the brief's sense is partly a question of definition.
- The cross sections are not re-derived outside the toolkit except through the amplitudes [math/constraints.md, scope].
- The plasma closes the channel wherever w < w_p.
decisive test: There is no observational test: the shortfall is >= 1e71 against PIXIE-class headroom of ~1e4 [D-36].
- Theoretical test: derive sigma(RL -> gamma gamma) = (4 pi/5) G^2 s independently of the toolkit, and check that a random-phase isotropic coherent state gives the kinetic rate.

## C7: The "N^2 coherent enhancement" is classical second-order field nonlinearity driving photon-vacuum pair creation, not a quantum decay of gravitons; the pair number is hbar-independent.
type: reframe
from: EXAMINER-E, DIALECTICIAN-C, MECHANIST-E; idealizer F2 and F13, constraints F8 (no candidate IDs)
argument:
- **hbar counting.**
  - With N = E/(hbar w), eq. 8's pair rate is 3 G^2 E^2 w sigma^2/(25 pi c^10) (SI), and d ln R/d ln hbar = 0.
  - The photon power W = 2 R hbar w is linear in hbar.
  - The Rayleigh-Jeans-stimulated power, 12 G^2 E^2 kT w sigma^2/(25 pi c^10), is hbar-free [M-DIALECTICIAN-03, M-CONSTRAINTS-04, M-IDEALIZER-03].
- **No classical emission from F = 0.** Classical Maxwell on a fixed metric keeps F = 0 [D-17, D-54].
- **What the effect is.**
  - The pair number is a functional of the classical wave (like a Bogoliubov |beta|^2).
  - N^2 is (h_c)^4, i.e. the n^2 of binary collisions.
  - The process is photon-vacuum pair creation on the second-order metric h^(2), which B&O v2 concede is "equivalent" [D-16].
  - The kinetic rate reproduces eq. 14 exactly (C6), and for crossing beams the coherent yield equals kinetic x overlap (unverified ratios 0.982 and 0.931) [idealizer F13].
- **The stimulated (1 + 2 f_gamma) part.** It is classical parametric scattering of the ambient field by h^(2) [mechanist M4], net of absorption, consistent with the Ai–Ellis–Pradler compensation [D-71c]. The Hz-band CMB occupation f = 3.8e8 extrapolates the Planck spectrum ~9 decades below its lowest measurement (ARCADE-2 starts at 3 GHz) [empiricist F10; D-09, D-43].
- **What follows.** Whether production persists becomes the hbar-free question of whether h^(2) of an outgoing wave has time-like Fourier support far from the source. The calculations behind C2 answer it: no.
predictions: If true:
- a Redi–Tesi-type Maxwell yield (c_J = 16) on the classical O(h^2) metric reproduces P with no graviton quantisation;
- an incoherent background with the same rho gives the same rate as a coherent one.

If false: a coherent-state in-out calculation differs from the semiclassical h^(2) yield at leading order.
evidence for: As above. B&O v2 state that with stimulation "all the hbar disappear" [D-54].
evidence against:
- B&O v1 call it "a quantum process forbidden classically and semi-classically", and the v2 Discussion still says it "vanishes in the classical limit" [D-54].
- Applying D-60 to h^(2) is an inference that Redi–Tesi do not make [D-60].
- No lens computed the semiclassical h^(2) yield explicitly.
- Constraints note that the unstimulated power is a spontaneous effect linear in hbar [constraints F8]. That is consistent with the claim (the number is classical, the energy is quantum), but it keeps "quantum" in the energy bookkeeping.
decisive test: For two crossing plane GW beams, compute the Maxwell pair yield on the classical O(h^2) metric with the D-60 functional, and compare it with the kinetic two-beam rate w^4 h^4 (1 - cos theta)^2/(1280 pi c^3) (SI) [M-MECHANIST-03].
- This is a cheap, tree-level calculation that any refuter can do.

## C8: Gravitational waves convert into ultralight-dark-matter scalar pairs at astrophysically relevant rates through Bose-enhanced resonant fusion, as B&O's eqs. 16–18 state for supermassive binaries.
type: mechanism
from: EMPIRICIST-D (B&O's positive claim, rated eliminated), CONSTRAINTS-F (negative on eqs. 17–18); mechanist finding 8, idealizer F10 (no candidate IDs)
argument:
- **B&O's chain (natural units).**
  - Non-resonant regime (w >> m): dP/dt = 7 G^2 N0^2 w^3 sigma^2/(450 pi).
  - Resonant regime, m <= w <~ m(1 + v^2/2) with sigma_w ~ m v^2/2: dP/dt ≃ G^2 m^5 N0^2 v^6 N_phi/128 (eq. 17).
  - N_phi = 5.7e87 at 1e-22 eV and v = 1e-3 c.
  - W_phi = 9 pi G m^2 v^3 N0^2 H0^2 Omega_DM x/256, i.e. W_phi ~ 1e14 W x_MW at 1e-21 eV (eq. 18), with "~1e54 s^-1" emissions and "stellar" luminosities in galactic-centre solitons [new: B&O v2 pp. 5–6, ACCESS full-text, empiricist F1; D-26, D-50, D-67].
- **The arithmetic checks.**
  - Substituting eq. 16 into eq. 17 gives ratio 1.
  - W_phi = 3.8e13 to 8.6e13 W x_MW at M = 1.82e10 Msun (SI) [M-EMPIRICIST-01, M-EMPIRICIST-02].
  - 7/(450 pi) and tau_phi = (54/7) tau are reproduced [M-IDEALIZER-02].
  - The brief's "1/16" coefficient does not appear in the v2 text [empiricist F1].
- **Named sub-hypotheses.**
  - (a) Non-resonant production, a near-source total like the photon case.
  - (b) Resonant Bose-enhanced production (eqs. 17–18).
  - (c) Soliton-enhanced "stellar" luminosities.
predictions: If true:
- SMBH binaries of ~1e10 Msun radiate ~1e14 W x_MW into ULDM (SI), and more in dense solitons;
- the only signature is GW depletion, a converted energy fraction of ~5e-32 per merger at x_MW = 1e5 [M-EMPIRICIST-04], against PTA amplitude errors of ~30% [D-35; empiricist F7].

If false: the resonant rate for a real chirp is <~ 2 W x_MW, and it is zero for an outgoing wave beyond r ~ lambda/2pi.
evidence for: Algebra and numbers are verified within B&O's model [above]. The local DM density is measured at 0.3–0.6 GeV/cm^3 [D-41].
evidence against:
- **No real chirp stays in resonance long enough.** The resonance needs coherence for 1/sigma = 1.3e12 s, but a 1.8e10 Msun chirping binary spends 12 s in the 5e-7 band: a shortfall of 9e-12 [M-EMPIRICIST-03, M-CONSTRAINTS-12].
- **In-band suppression.** It is (N_band/N0)^2 = 5.1e-14, which gives W_phi ~ 2 W x_MW (SI). The "only in-band gravitons count" premise is the lens's inference [M-EMPIRICIST-03].
- **Kinematics.** The resonant channel needs gravitons within 2v = 2e-3 rad of head-on, which an outgoing wave at r >> lambda lacks [M-MECHANIST-08, M-IDEALIZER-12, M-CONSTRAINTS-12]. In the non-resonant regime the final momenta ~w >> m v lie outside the occupied ULDM phase space, so there is no Bose factor [idealizer F10, analytic].
- **The fiducial masses are disfavoured.** 1e-22 to 1e-21 eV is disfavoured at > 99.7% credibility, with m_a > 2e-20 eV [new: Rogers & Peiris 2021, PRL 126, 071302, ACCESS abstract, empiricist F2].
- **No source observed.** No individual SMBH binary has been detected [new: Horlaville et al. 2026, ApJ 1003, 229, ACCESS abstract, empiricist F3].
- **Too small even at face value.** W_phi/L_GW = 1.1e-31 at x = 1e5, and 1 Lsun needs x = 1e13 [M-EMPIRICIST-04].
- **Eq. 17 itself is not re-derived.** Its v^6 and 1/128 are unverified, though the shortfall does not depend on them [M-EMPIRICIST-07].
decisive test: Compute the time-dependent Bose-enhanced rate for a chirping SMBH binary, with the resonance width resolved (the chirp's spectral density in the v^2/2 band) and the head-on kinematic restriction imposed.
- C8 needs >~ 1e13 W x_MW. The empiricist and constraints lenses predict <~ 2 W x_MW in-band, and zero beyond r ~ hbar c/m = 2e14 m at 1e-21 eV [M-CONSTRAINTS-12].
