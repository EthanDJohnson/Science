# Math check: dialectician
status: final

Units: SI throughout (m, s, m/s^2, rad/s); angles quoted in degrees and converted to radians inside
the checks. g = 9.81 m/s^2 (the value that reproduces the lens's numbers). Every check was
re-derived from the definitions and the dossier's stated bound forms (D-25, D-31, D-32, D-33), not
from the lens's script, which was neither read nor run.

| ID | Claim (finding) | Statement checked | Checks | Verdict | Log |
|---|---|---|---|---|---|
| M-DIAL-01 | FoV-limited acceleration a_FoV = g tan(phi + VFoV/2) and its values (F4, S1; DIAL-F, DIAL-A) | Constant-altitude force balance T cos(theta) = mg, T sin(theta) = ma gives a = g tan(theta); body-fixed camera axis phi above body-x, vertical half-angle VFoV/2; the horizontal travel direction lies in the cone iff phi - VFoV/2 <= theta <= phi + VFoV/2, so a <= g tan(phi + VFoV/2). Domain g > 0, phi >= 0, VFoV > 0, phi + VFoV/2 < 90 deg | force balance and cone criterion re-derived; cap confirmed by bisection on the cone membership test (rel. diff 4e-16); identity a = g tan(atan(a/g)); consistency g sqrt((T/W)^2 - 1) = g tan(theta); small-angle limit a_FoV/(g(phi+VFoV/2)) -> 1; monotonicity in the half-angle; units (acceleration, speed) | verified | math/dialectician/M-DIAL-01.py.log |
| M-DIAL-02 | T/W saturation T/W_sat = sec(phi + VFoV/2) (F10; DIAL-F) | Constant-altitude flight gives T/W = sec(theta) (dimensionless); the cone criterion caps theta at phi + VFoV/2 and sec is increasing on [0, 90 deg), so T/W_sat = sec(phi + VFoV/2). Values 1.14 / 1.94 / 3.63 / 1.86 / 22.93 | all five values reproduced (max rel. diff 0.3 %); second route through a_FoV and T/W = sqrt(1 + (a/g)^2) agrees; identity sec = sqrt(1 + tan^2); hover limit sec -> 1 at theta = 0; divergence as the cone edge reaches the vertical; monotonicity; dimensionlessness from T/(mg) | verified | math/dialectician/M-DIAL-02.py.log |
| M-DIAL-03 | Latency-vs-spacing bound v <= w_c L/(2 pi k), w_c = (pi/2 - PM)/tau, and the predicted seen:unseen ratio 8.52 (F5, S2, C2; DIAL-E) | Integrator loop with pure delay: phase -pi/2 - w tau, so PM = pi/2 - w tau and w_c = (pi/2 - PM)/tau (D-25); reference manoeuvre frequency v/L, k cycles per feature, so v <= w_c L/(2 pi k). Domain tau > 0, 0 <= PM < pi/2, L > 0, k >= 1 | bound re-derived; 33.48 / 16.74 (tau 40 ms, L = 75/7 = 10.714 m), 5.00 / 2.50 (tau 100 ms, L = 4 m), 16.67 / 8.33 (tau 30 ms, L = 4 m) all reproduced; elasticities +1.000000 in L and -1.000000 in tau confirmed symbolically and numerically; PM -> 0 and tau -> 0 limits; units (frequency, speed). The ratio claim fails: (L_gate/tau_gate)/(L_clutter/tau_clutter) = 6.696, not 8.52 | refuted (ratio only; bound, speeds and elasticities verified) | math/dialectician/M-DIAL-03.py.log |
| M-DIAL-04 | Lag vs delay crossover ratios, inverted-pole inner loop, and the large-signal delivered fraction (F6, S3, C3; DIAL-C) | Lag loop (K/s)/(1+s tau): PM = pi/2 - atan(w tau) so w_c = tan(pi/2 - PM)/tau; delay loop (K/s)e^{-s tau}: w_c = (pi/2 - PM)/tau; ratio tan(x)/x with x = pi/2 - PM. Step response a_cmd(1 - e^{-t/tau}) has mean fraction 1 - (tau/T)(1 - e^{-T/tau}) over [0, T]. tau = 39.1 ms | 25.575 vs 20.087 rad/s (ratio 1.2732) at PM 45 deg and 14.766 vs 13.391 (ratio 1.1027) at PM 60 deg reproduced; crossover verified by evaluating the loop phase (-135.000 deg); 392.70 rad/s = 62.50 Hz at 2 ms, PM 45 deg; the fraction formula derived by symbolic integration and cross-checked by 2e5-point quadrature (0.4357, 0.6393, 0.7450, 0.7597, 0.8305, 0.9609 at T = 50, 100, 150, 160, 230, 1000 ms); tan(x)/x > 1 on (0, pi/2); T -> oo limit 1; small-T series T/(2 tau) - T^2/(6 tau^2); units | verified | math/dialectician/M-DIAL-04.py.log |
| M-DIAL-05 | A 150 ms manoeuvre around r = 0.5 m needs a > ~90 m/s^2 ~ 9 g (F6, C3; DIAL-C) | Bang-bang lateral displacement r in time t with bounded acceleration a: r = 2 (1/2) a (t/2)^2 = a t^2/4, so t = 2 sqrt(r/a) (the D-31 lateral term) and a = 4r/t^2. Domain r, t, a > 0; point mass, no drag, instantaneous command reversal | a = 88.89 m/s^2 = 9.06 g at t = 150 ms, r = 0.5 m; inverse check t_lat(90 m/s^2) = 149.07 ms; bang-bang identities and their inversion; a -> oo and t -> oo limits; units (acceleration, time); T/W 4.4 gives 42.03 m/s^2 (4.28 g) and T/W 12.35 gives 120.76 m/s^2 (12.31 g), bracketing the threshold as the lens says | verified | math/dialectician/M-DIAL-05.py.log |
| M-DIAL-06 | Clutter-regime dodge-bound elasticities and the three finite swaps (F7, F11; DIAL-A, DIAL-E) | v = s/(tau + 2 sqrt(r/a)) (D-31) at s = 6 m, tau = 0.1 s, r = 0.5 m, a = 16.33 m/s^2; elasticities d ln v/d ln s = 1, d ln v/d ln tau = -tau/D, d ln v/d ln a = sqrt(r/a)/D with D = tau + 2 sqrt(r/a). Domain s, tau, r, a > 0 | baseline v = 13.3344 m/s reproduced; analytic e_s = +1, e_a = +0.3889, e_tau = -0.2224; the lens's +0.387 and -0.231 reproduced exactly as forward 10 per cent differences; swaps +100.00 %, +41.44 %, +18.42 % reproduced; symbolic elasticity identities; proved 0 < e_a < 1/2 and |e_tau| < 1 over the whole domain (so e_s always dominates); tau -> 0 limits (1/2, 0) and a -> oo limit v -> s/tau; units | verified | math/dialectician/M-DIAL-06.py.log |
| M-DIAL-07 | Contradiction-1 prediction: 15.0 m/s with perfect aero, ~26 m/s at 12 m range, "(ii) wins by >50 per cent" | Same dodge bound with a = a_FoV = 16.33 m/s^2, r = 0.5 m; case (i) s = 6 m, tau = 50 ms; case (ii) s = 12 m | 15.00 m/s at (6 m, 50 ms) and 26.67 m/s at (12 m, 100 ms) reproduced; (ii)/(i) = 1.778 (+77.8 %) and, at equal latency, exactly 2.000 (+100 %), so ">50 per cent" holds either way; doubling-range identity; halving latency proved strictly weaker than doubling range over the whole domain; s -> oo limit; units | verified | math/dialectician/M-DIAL-07.py.log |
| M-DIAL-08 | d ln v/d ln(T/W) ~ +0.5 at T/W >= 4 (F2) | a_h = g sqrt((T/W)^2 - 1) (D-33); rest-to-rest bang-bang over fixed distance d gives t = 2 sqrt(d/a), v_avg = sqrt(a d)/2, hence d ln v/d ln a = 1/2 exactly and d ln v/d ln(T/W) = (1/2)(T/W)^2/((T/W)^2 - 1). Domain T/W > 1, d > 0 | 0.5333 at T/W 4, 0.5272 at 4.4, 0.5033 at 12.35 (numerical log-derivative agrees with the closed form); D-33's a_h elasticity 1.0667 at T/W 4 reproduced; T/W -> oo limits (1 and 1/2); divergence at hover (so "+0.5" is a high-thrust statement only); inequality e > 1/2 everywhere; units | verified | math/dialectician/M-DIAL-08.py.log |
| M-DIAL-09 | "At s = 3 m rather than 6 m every range-limited bound halves" (F3; DIAL-A) | Dodge bound v = s/(tau + 2 sqrt(r/a)) is linear in s (elasticity exactly 1); stop bound v = a(-tau + sqrt(tau^2 + 2s/a)) (D-32) has range elasticity strictly between 1/2 and 1. Domain s, tau, r, a > 0 | dodge: 13.334 -> 6.667 m/s, ratio exactly 0.5000, elasticity 1 confirmed symbolically; stop: 12.460 -> 8.399 m/s, ratio 0.6741 (a 32.6 per cent fall, not 50), elasticity 0.5579 at tau = 100 ms; proved 1/2 < e_s < 1 for the stop bound over the domain; tau -> 0 limits sqrt(2 a s) and 1/2; units | refuted (as stated; the dodge-bound branch holds) | math/dialectician/M-DIAL-09.py.log |
| M-DIAL-10 | Seen-vs-unseen observed speed ratios and the aero-cost comparison (F1, C2, F8; DIAL-D) | Arithmetic only on quoted values: 27.8-32.2 m/s seen vs 5-10 m/s unseen; "factor of 3-6"; "observed ratio 2.57-3.22"; "slack by ~2.6x"; 5.14 s vs 4.92 s = "~4 per cent"; 2.00-2.68 per cent of traversal time vs a factor 3-6 | full ratio range 2.780-6.440 (so the quoted "3-6" understates the span and its lower end is 2.78, not 3); 3.22 = 32.2/10 reproduced, 2.78 = 27.8/10 reproduced, 2.57 not reproducible from any pair of stated speeds; slack = 2.08x with the lens's own L = 10.71 m and observed 3.22 (2.64x only with the untraceable 8.5 and 3.22); 5.14/4.92 - 1 = 4.472 per cent; inequality 1/(1 - 0.0268) = 1.0275 < 2.78 verified, so the "few per cent cannot explain a factor of 3-6" step holds | unverified (the 2.57 lower end; the rest verified) | math/dialectician/M-DIAL-10.py.log |

## Refuted

- **M-DIAL-03 (the predicted seen:unseen ratio only).** The S2 bound itself, its four quoted speeds
  and its two elasticities (+1 in L, -1 in tau_eff) are verified. But the ratio it predicts is
  (L_gate/tau_gate)/(L_clutter/tau_clutter), which with the lens's own stated inputs
  (L_gate = 75 m / 7 gates = 10.714 m, tau = 40 ms; L_clutter = 4 m, tau = 100 ms) is **6.696**, not
  the 8.52 reported in the Calculations section and in contradiction 2. 8.52 requires
  L_gate = 13.6 m (ratio 8.50); likewise the "spacing alone accounts for L_gate/L_clutter ~ 3.4"
  line needs 13.6 m, whereas 10.714/4 = 2.679. Two different gate spacings are in use, both inside
  the "L ~ 10-14 m" range the lens states, but the published numbers are not mutually consistent.
  Corrected form: with L_gate = 10.714 m the predicted ratio is 6.70 and the gate-track slack
  against an observed ratio of 3.22 is **2.08x**, not 2.6x (it is 2.6x only against the
  untraceable observed 2.57). Depends on it: contradiction 2's "slack by ~2.6x on the gate track",
  finding 5's regime split, and candidate DIAL-E's "the ranking changes across regimes" (DIAL-E's
  qualitative claim survives, since the slack remains > 2 either way).
- **M-DIAL-09 ("at s = 3 m every range-limited bound halves").** True for the D-31 dodge bound,
  which is exactly linear in s. False for the other range-limited bound the dossier carries, the
  D-32 stop bound: at tau = 100 ms, a = 16.33 m/s^2 it falls from 12.460 to 8.399 m/s, i.e. by
  32.6 per cent, because its range elasticity is 0.558 (and is provably in (1/2, 1) for tau > 0,
  tending to 1/2 as tau -> 0). Corrected form: "bounds linear in the range halve; the stop bound
  falls by about a third". Depends on it: finding 3's "every range-limited bound halves" and the
  strength (not the sign) of DIAL-A's short-range argument, whose dodge-bound branch stands.

## Unverified

- **M-DIAL-10, the lower end of the "observed 2.57-3.22" seen:unseen ratio.** Every other number in
  the row reproduces, but 2.57 does not follow from any pair of speeds the analysis states
  (27.8/10 = 2.78, 32.2/10 = 3.22, and the widest stated pairing is 2.78-6.44). It would need a
  seen-course speed of 25.7 m/s or an unseen speed of 12.5 m/s, neither of which appears in the
  findings. Where the derivations part ways is the input, not the arithmetic; the inputs are not
  stated, so I could not settle it. It matters only for the "slack by ~2.6x" figure (see
  M-DIAL-03). Also noted, not separately refuted: finding 1's "factor of 3-6" is 2.78-6.44 on its
  own numbers.
- Not checked at all (no mathematics of the lens's own to re-derive): the literature values
  entering findings 8 and 9 (0.419 -> 0.324 m tracking RMSE, 55/67/71/100 per cent success,
  2.00-2.68 per cent model-fidelity penalty, 78 per cent tracking-error cut, 40 ms sensorimotor
  latency, 39.1 ms motor time constant, 58 deg vertical depth FoV, 0.3-3 m depth range). Those are
  source questions. Assumption L-4 (a ~2 ms inner-loop transport delay) is an input, not a result:
  M-DIAL-04 verifies the conditional, and the lens's own ledger says the cascade resolution fails
  if the true transport delay is tens of ms.

### Minor corrections that do not change a verdict

- M-DIAL-02: "these vehicles carry 2-4x more thrust than their cameras let them use" is 2.11x to
  2.32x at T/W 4.1-4.5 against T/W_sat = 1.942; the upper end of "2-4x" is not reached.
- M-DIAL-04: the inner-loop figure "260-390 rad/s (42-63 Hz)" is quoted as following from "1-2 ms"
  of transport delay. It actually corresponds to a 2 ms delay at phase margins of 60-45 deg; 1 ms
  at PM 45 deg gives 785 rad/s (125 Hz). The error is conservative, so DIAL-C is unaffected.
- M-DIAL-04/05: "a_eff/a_cmd <= 0.76 at tau = 39.1 ms" with T ~ 150 ms gives 0.745; 0.760 is the
  value at T = 160 ms. The inequality as written still holds.
- M-DIAL-06: the lens's e_a = +0.387 and e_tau = -0.231 are forward 10 per cent differences; the
  analytic values are +0.3889 and -0.2224, so the elasticity spread |e_s/e_tau| is 4.50 rather than
  the quoted 4.3x, and |e_s/e_a| is 2.571. The ranking and DIAL-A are unaffected.
- M-DIAL-07: the "~26 m/s with 12 m of range" figure uses tau = 100 ms while the sentence before it
  uses tau = 50 ms (which would give 30.0 m/s). The ">50 per cent" conclusion holds under either
  latency, and at equal latency the gain is exactly +100 per cent.

## Formalizable

- **M-DIAL-01 / M-DIAL-02.** For phi >= 0, V > 0 with phi + V/2 < pi/2: the set
  {theta : phi - V/2 <= theta <= phi + V/2} contains 0 iff theta <= phi + V/2 (given theta >= 0),
  and tan and sec are strictly increasing on [0, pi/2); hence sup{g tan theta} = g tan(phi + V/2)
  and sup{sec theta} = sec(phi + V/2). Finite-dimensional, pure trigonometry.
- **M-DIAL-03.** For v(L, tau) = c L/tau with c > 0: L d ln v/d L = 1 and tau d ln v/d tau = -1
  identically, independently of c (hence of PM and k).
- **M-DIAL-04.** tan(x)/x > 1 for all x in (0, pi/2); and f(T) = 1 - (tau/T)(1 - e^{-T/tau}) is
  strictly increasing on (0, oo) with f(0+) = 0, f(oo) = 1 and f(T) = T/(2 tau) + O(T^2).
- **M-DIAL-06.** For v = s/(tau + 2 sqrt(r/a)) with s, tau, r, a > 0: e_s = 1 exactly,
  e_a = sqrt(r/a)/(tau + 2 sqrt(r/a)) in (0, 1/2), e_tau = -tau/(tau + 2 sqrt(r/a)) in (-1, 0), and
  e_a + |e_tau| = 1 - e_a < 1; so e_s strictly dominates both for every parameter value. This is
  the inequality DIAL-A rests on and it is provable in closed form.
- **M-DIAL-09.** For v(s) = a(-tau + sqrt(tau^2 + 2s/a)) with a, tau, s > 0, the elasticity
  s v'(s)/v(s) lies strictly in (1/2, 1), with limit 1/2 as tau -> 0; hence no scaling of s by
  lambda < 1 scales v by lambda.
- **M-DIAL-08.** For w > 1, (1/2) w^2/(w^2 - 1) > 1/2 and decreases monotonically to 1/2 as
  w -> oo.
