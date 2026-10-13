# Task A (B&O eqs. 6-8, S6, S10-S11): derivation notes for the check scripts

Scripts: `calc/taskA1_helicity_labels.py`, `calc/taskA2_pair_phases.py`, `calc/taskA3_S6_rate.py`,
`calc/taskA3b_physical_shell.py`, `calc/taskA4_scalar_channel.py`; shared code `calc/bo_common.py` (spinor closed
forms, patterns) and `calc/bo_ring.py` (ring/shell quadrature). Run logs: `notes/*.log`.

## Normalisation chain (B&O conventions, omega_s = omega, band sigma)
- [a(k), a+(k')] = (2pi)^3 2k delta^3; a_l(k)|f> = f_l(k)|f>; N = sum_l int dk~ |f_l|^2, dk~ = d^3k/((2pi)^3 2k).
  Both helicities = Theta on the shell gives N = Theta^2 omega sigma/(2 pi^2), i.e. B&O's Theta^2 = 2 pi^2 N/(omega sigma).
- T = (1/4) int M b+ b+ a a (so <q1 q2|T|k1 k2> = M); <q1 q2|T|f> = (1/2) int dk1~ dk2~ sum f f M (2pi)^4 delta^4.
  B&O's 4 pi G in eq. 7 is this 1/2 times 8 pi G.
- P = (1/2) sum_s int dq1~ dq2~ |A|^2 (identical photons). Integrating the photons gives dPhi_2 = dOmega/(32 pi^2) and
  (2pi)^4 delta^4(K - K'); with |k_i| = omega in denominators this is exactly the prefactor G^2/(16384 pi^9 omega^4) of S6.
- Ring: for fixed K the set {k : |K/2 -+ k| in the band} has d^3k = a b da db d alpha/K exactly (a, b = |k1|, |k2|),
  so its volume is 2 pi (omega sigma)^2/K (Monte-Carlo check in taskA3_S6_rate (b)). In the CM the graviton axis lies
  in the plane perpendicular to K at azimuth alpha.
- With 2 pi delta(E) -> T: dP/dt = C G^2 N^2 omega^3 sigma^2, C = J/(8192 pi^5),
  J = int dK dOmega_K dOmega_cm beta sum_final |int d alpha m|^2, m = amplitude with unit-normalised profile tensors
  (int dOmega |h|^2 = 1).
- Exact energy delta instead: int over the four band offsets of delta(d1 + d2 - d1' - d2') = (2/3) sigma^3
  (Irwin-Hall n = 4 density at the centre), versus B&O's sigma^4 T/(2 pi): P_total = (dP/dt) x 4 pi/(3 sigma).

## Spinor closed forms (independent route, bo_common)
- KLT: M(1,2,3,4) = s12 A(1,2,3,4) A~(1,2,4,3) with photon = gluon x scalar, graviton = gluon x gluon:
  A(1^-,2^+,3^-,4^+) = <13>^4/(<12><23><34><41>), A~(1_phi,2_phi,4^+,3^-) = <13>^2<23>^2/(<12><24><43><31>) give
  M(1_gam^-, 2_gam^+, 3^{--}, 4^{++}) = (kappa/2)^2 s12 <13>^5<23>/(<12>^2<34>^2<41><24>), |M| = (kappa/2)^2 s13^2/s12.
  Little-group weights checked by hand (t^2, t^-2, t^4, t^-4 for particles 1..4).
- Incoming momentum P: lam(-P) = i lam(P), lamt(-P) = i lamt(P); the i's cancel (graviton slots carry weight 4).
- Massless scalar: M(1_phi, 2_phi, 3^{--}, 4^{++}) = (kappa/2)^2 <3|1|4]^4/(s12 s13 s14).
- A general TT tensor H is projected on (eps^- eps^-, eps^+ eps^+) built from the same spinors; the module's full
  amplitude equals this route with ratio 1 to 1e-12 for random kinematics and random complex tensors (taskA1 2b,
  taskA4 amps), so the module's relative phases are confirmed independently.

## Label bookkeeping
- Head-on CM: J_z(gg) = l1 - l2 (graviton 2 moves along -z); photon pair J_n = s1 - s2.
- Nonzero: l1 = -l2 (J_z = +-4) and s1 = -s2 (J_n = +-2); |M| = 8 pi G [(P_{g,+2} - q_{gam,-1})^2]^2/s.
- B&O eq. 6 nonzero entries have lambda1 = lambda2 and mu1 = mu2: only consistent as spin projections on common axes.
- S10 (scalars): A++ (m^4) = physical same helicities (J_z = 0), A+- = physical opposite (J_z = +-4); this is
  the opposite of the crossed-Compton (in, out) reading (Compton flip -> same physical helicities).

## Patterns (calc/bo_common.pattern)
bo_plus: e_th e_th - e_ph e_ph (polar frame, isotropic; = f_+ = f_- real in the module's e_+- convention);
bo_cross: e_th e_ph + e_ph e_th; circ: e_+ e_+; binary: Lambda(n)(x+iy)(x+iy); linear: Lambda(n) z z.
Only products f_+(k1) f_-(k2) enter for massless final states, so a common rephasing f_+ -> e^{i chi} f_+,
f_- -> e^{-i chi} f_- (a common rotation of linear polarisations) cannot change any rate (bo_cross = bo_plus).
