# Check: theory
status: final

| Claim | Verdict | Note |
|---|---|---|
| RT-01 flatness with linear rotor drag (Faessler 2018) | verified | Abstract wording matches exactly (arXiv:1712.02402 via fetch_text). RA-L venue not independently checked, but consistent with known record. |
| RT-02 point-mass bang-bang; quadrotor underactuation | verified | Both quotes found verbatim in arXiv:2108.04537 p.13 (appendix A/B). |
| RT-03 polynomial times 2.165/1.938/1.699 vs 1.614 s; 5.3% | verified | Fig. 6 text matches. 1.699/1.614 = 1.0527, so 5.3% is right. The "provably suboptimal" gloss is the authors' qualitative argument; the quoted caption supports it. Setting is the paper's illustrative example (it is not hardware). |
| RT-04 full model 2.00% / 2.68% slower; times 0.89 to 1.93 s, 6 to 15 m | verified (minor) | Table III and quote match. Table also has 3 m (0.89 to 0.92 s), so the range really is 3 to 15 m, not 6 to 15 m. The 1.93 s maximum is at 15 m and 0.89 s is at 3 m (ref [22]). The claim's "6 to 15 m" is slightly off, with no effect on the percentages. |
| RT-05 non-convex; local optimum (flip); fix with bang-bang initialisation | verified | Quote found verbatim (p.17), and the flip explanation is in the same passage. |
| RT-06 Falanga Eqs 8-9: v = s/(tau + 2 sqrt(r/u2)) | verified | Eq 8 and 9 text matches (garbled root layout as stated). Eq 8 rearranges algebraically to the claimed form, and the units are consistent. Scope caveats (constant longitudinal speed, cannot change velocity) are in the paper's text. |
| RT-07 delays/RHP "impose severe limits"; delays not avoided by sensor/actuator placement | verified | Both quotes found (AM 2020 draft p.465, p.469). The "severe limits" quote is the ch.14 intro. |
| RT-08 omega_gc <= z tan(phi_ap/2), 0.6 z at pi/3 (eq 14.11) | verified | Quote found verbatim, p.476. Quadrotor applicability is flagged by the author as their own reading, so it is not a sourced claim. |
| RT-09 Bode integral / waterbed | verified | Quote found verbatim (p.469). The extra gloss about delay raising the sensitivity peak is an inference, but standard. |
| RT-10 large-signal limits from actuator rate and power | verified | Quote found verbatim (p.465). The "treated as separate nonlinear limit" gloss is fair. |
| RT-11 Song et al.: OC vs RL; >12 g, 108 km/h | verified | Quote and numbers found (arXiv:2310.10943; 12.58 g, 108 km/h). The paper states motion capture and lower latency were used (Fig. 6 caption), which the claim leaves unchecked. So this is controller evidence only, per the brief. Published in Science Robotics 2023 (vol. 8, issue 82, per the PDF header). |
| RT-12 VINS has four unobservable DOF; bias, velocity, roll and pitch observable (Martinelli) | verified | Both quotes in the IJRR PDF (author-hosted UMN copy) p.2-3. The claim "proved" holds for the point-feature model; they also show the linearised EKF loses one direction, which the claim does not mention but which is outside its scope. |
| RT-13 four unobservable directions persist with full self-calibration (Yang 2022) | verified | Abstract text matches (arXiv:2201.09170). Preprint status was labelled correctly. The claim's details on rolling shutter and time offset were not re-checked, only the headline. |
| RT-14 ZOH adds about T/2 delay; tau_eff sum | verified (weak source) | The slide only says "PHASE LOSS due to half-sample delay may DESTABILIZE"; it does not state the T/2 phase wL formula. The T/2 result is standard sampled-data theory, so the claim is correct but the source supports only the qualitative statement. The claim already marks it secondary. |
| RT-15 delay-limited bandwidth: PM = pi/2 - wc tau; numbers | verified | I recomputed. The log shows the tool matches the closed form. 0.785/0.524 rad, 157 rad/s = 25 Hz at 5 ms, and PD atan(3) = 71.57 deg with 1.249/wc delay margin are all in the log. |
| RT-16 stopping bound v_max = a(-tau + sqrt(tau^2 + 2s/a)); elasticities | verified (one soft) | I recomputed v = 14.52 m/s at (6 m, 20, 50 ms). The log matches e_s=0.53, e_a=0.47, e_tau=-0.064 and the Falanga elasticities. The closing "5 to 15 times" ratio e_s/e_tau from the log's cases is roughly 4.2 to 14, so the lower end is slightly generous (the 10 m, 100 ms Falanga case gives 4.2). |
| RT-17 thrust-to-weight ceiling, a_h = g sqrt((T/W)^2-1), times | verified | Hand check gives 16.99, 37.99, 77.86 m/s^2, t = 1.53 s at T/W=2, and elasticity 4/3 = 1.33. 10% T/W gives ~5% speed (0.5 x 1.07) is right. |
| RT-18 Sun et al.: >78% error reduction; up to 20 m/s, 5 g, motion capture | verified | Quote and speed/acceleration figures found in arXiv:2109.01365 p.1. Hardware under motion capture, correctly labelled. T-RO venue not independently checked. |
| RT-19 NMPC weight instability from actuator delay in sim | verified | Quote found verbatim (p.11). |
| RT-20 Smith predictor architecture | verified | Quote found (AM 2020 draft p.520). Implication paragraph is flagged as the author's inference. |

## Summary
20 claims checked: 20 verified, none contradicted or misattributed. Minor points: RT-04 range should read 3 to 15 m (the 0.89 s time is the 3 m case); RT-14's source supports only the qualitative statement; RT-16's "5 to 15 times" is nearer 4 to 14; RT-11's hardware result used motion capture (so it is not onboard-only evidence). Not checked: venues for Faessler (RA-L) and Sun (T-RO); that Yang 2022 has since appeared in T-RO (from memory, not verified here); Falanga's figures.
