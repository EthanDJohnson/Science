# Analysis: empiricist (Hume: what has actually been observed)
status: final

## Method applied
Separate observation from inference for each claim in B&O; give base rates for "new vacuum process from a single unrefereed theory preprint" claims; find analogues; state what an honest skeptic would need. Owner of the ULDM-channel calculation (eqs. 16-18) per the brief.

## Findings
F1. B&O's ULDM text (v2, p. 5), read directly: [new: Blas & Oller, arXiv:2607.24930v2 p. 5, full-text, "In the regime where the decay happens into states of high occupation number,m DM≤ω s ≲m DM(1 +v 2/2),N ϕ can enhance the rate enormously, dP dt ≃ G2m5 DMN2 0v6 128 Nϕ,(17) withσ ω ≈m DMv2/2. Using Eq. (16), the converted net power isW ϕ = 9πGm 2 DMv3N2 0 256 H2 0 ΩDM."] and [same source, p. 5, full-text, "Wϕ∼10 14xMW 10−21 eV mDM 2 v 10−3 3 W,(18) corresponding to rates of emission of∼10 54 s−1 form= 10−21 eV"]. The Discussion (p. 6) adds that ULDM luminosities "may correspond to stellar ones in the cases of large DM densities, as may be the case in the solitons of galactic centers". No "1/16" coefficient appears in the v2 text (grep: no match); the brief's "1/16" is not B&O's printed main-text form. Observation status: these are theoretical statements; nothing in the ULDM channel has been observed by anyone [D-66, D-67].
F2. B&O's fiducial ULDM mass is itself observationally disfavoured: [new: Rogers & Peiris 2021, PRL 126, 071302, abstract, "a 95% lower limit ma>2×10-20 eV. This strongly disfavors (>99.7% credibility) the canonical ULA with 10-22 eV<ma<10-21 eV"]. Eq. 16 is normalised at 1e-22 eV and eq. 18 at 1e-21 eV, both inside the disfavoured window (for a ULDM that is all of the dark matter, the case eq. 16 assumes through Omega_DM).
F3. No individual supermassive black hole binary (the source class eq. 18 needs, M ~ 1e10 Msun, nHz-uHz band) has yet been detected by any PTA: [new: Horlaville et al. 2026, ApJ 1003, 229, abstract, "ongoing pulsar timing array (PTA) experiments aim to detect the first individual system"]. The PTA observation is a background [D-35]; the eq. 18 source is not an observed object.
F4. Observational bound on vacuum GW damping. The only direct test of GW amplitude loss over cosmological paths is the GW-vs-EM distance comparison of GW170817: [new: Lagos et al. 2019, PRD 99, 083504, arXiv abstract via fetch_text, full-text, "GW170817 constrains $c_M = -9^{+21}_{-28}$ ($68.3\%$ credibility)"]. Converted in calc (F7) to an allowed amplitude change of order 10% over ~40 Mpc. B&O's predicted depletion (1e-66 to 1e-57 over 410 Mpc [D-47]) and the null (0) both sit far inside this bound; Jones-Singleton's 1e11 m decay length [D-53] is excluded by the existence of detections at 1e25 m (GW150914 at 410 Mpc [D-30]). Observation therefore discriminates only against large damping, not between B&O and zero.

F5. ULDM algebra checks out. Substituting eq. 16 (N_phi = 9 pi H0^2 Omega_DM x / (4 G m^4 v^3)) into eq. 17 and multiplying by 2m (two scalars of energy ~m per event) gives exactly B&O's printed W_phi = 9 pi G m^2 v^3 N0^2 H0^2 Omega_DM x/256. The sympy ratio is 1 [calc: runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/lens-empiricist_uldm.py]. N_phi(1e-22 eV, v = 1e-3, x = 1) = 5.75e87 against B&O's 6e87. The eq. 18 number, using B&O's ISCO relation m ~ omega_s ~ 8800 pi (Msun/M) s^-1 (M = 1.82e10 Msun at 1e-21 eV), is W_phi = 3.8e13 W x_MW (E_rel = 2/65 M c^2, B&O's merger scaling [D-27]) or 8.6e13 W x_MW (E_rel = 3/65 M c^2). The emission rate is 2.4e53 to 5.4e53 scalars/s. Both match B&O's "1e14 W x_MW" and "~1e54 s^-1" to within a factor of about 3 (SI). This confirms and extends [D-50]. Verdict on the arithmetic: confirmed within B&O's model, but eq. 17's own derivation (the v^6 power) was not re-derived here (see Assumptions).
F6. **Eq. 17's resonance condition cannot be met by a real chirp.** All values at m = 1e-21 eV and v = 1e-3 c (SI):
  - Eq. 17 needs sigma_omega = m v^2/2 = 7.6e-13 rad/s, so a packet coherent for 1/sigma_omega = 1.3e12 s (4.2e4 yr). The ULDM coherence time is 1.3e5 yr.
  - A 1.8e10 Msun equal-mass binary at f = 2.4e-7 Hz (period 48 d) has f/fdot = 2.4e7 s (Newtonian quadrupole). It therefore stays inside the fractional resonance band v^2/2 = 5e-7 for only 12 s, a shortfall of 9e-12.
  - Only the gravitons that lie spectrally inside the band count: N_band = 1.4e89, against B&O's N0 = 6.2e95 (the whole merger's energy). The rate goes as N0^2, so it drops by (N_band/N0)^2 = 5.1e-14, and the self-consistent W_phi is about 2 W x_MW, not 4e13 W x_MW.
  - Both ratios are independent of m: at m = 2e-20 eV, the Lyman-alpha floor, the shortfall is the same 9e-12 and W_phi(in-band) = 5e-3 W x_MW.

  Even this ~2 W assumes the eq. 17 form holds when the packet is 1e11 times shorter than the coherence time it assumes, which it does not, so 2 W is generous [calc: runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/lens-empiricist_uldm.py]. Verdict: eq. 18 has the right arithmetic but the wrong quantity. Its own validity window (D-61 type) is violated by about 11 orders of magnitude in duration.
F7. Even at face value nothing is observable (SI): W_phi = 3.8e18 W at x_MW = 1e5, which is 1.0e-8 Lsun and 1.1e-31 of a merger's peak GW luminosity (3.6e49 W [D-29]). The fraction of GW energy converted over a 1.4e6 s merger is 5e-32. Reaching 1 Lsun would need x = 1e13 times the cosmic mean DM density. B&O's "stellar" luminosities in galactic-centre solitons (p. 6) therefore need x ~ 1e13 (face value) or ~1e26 (in-band). The products are 1e-21 eV scalars coupled only gravitationally, so no instrument has a channel for them. The only observable is GW depletion, at 1e-32 against PTA amplitude errors of ~30% [D-35] [calc: lens-empiricist_uldm.py]. The GW170817 c_M bound allows an amplitude change of -17% to +6% (68%) over ~40 Mpc [calc: same, section 5; F4].
F8. A prior claim of exactly this process was falsified by observation. Jones & Singleton proposed attenuation via G+G -> gamma gamma [new: Jones & Singleton 2015, arXiv:1505.04843 (IJMPD 24, 1544017), full-text abstract via fetch_text, "we propose that the Unruh-DeWitt detector response implies a "decay" or attenuation of gravitons, $G$, into photons, $\gamma$, via $G + G \rightarrow \gamma + \gamma $ or $G \rightarrow \gamma + \gamma + G$. Over large distances such a decay/attenuation may have consequences in regard to the detection of gravitational waves."]. Their decay length, ~1e11 m [D-53], is 1e14 times shorter than the 1.3e25 m path of GW150914 [D-30], which was detected with the GR-predicted amplitude. This is the single direct observational test of the claim class "GWs decay into photon pairs in vacuum", and the large-effect version failed it.
F9. The photon analogue of graviton fusion (light-by-light scattering) is a real, confirmed vacuum process, but it was seen only with crossing, strongly non-collinear quasi-real photons in extreme fields [new: ATLAS Collaboration 2017, arXiv:1702.01625 (Nature Phys., doi 10.1038/nphys4208), full-text abstract via fetch_text, "Light-by-light scattering ($\gamma\gamma\rightarrow\gamma\gamma$) is a quantum-mechanical process that is forbidden in the classical theory of electrodynamics. This reaction is accessible at the Large Hadron Collider thanks to the large electromagnetic field strengths generated by ultra-relativistic colliding"] (quote truncated at the fetch boundary). The structural contrast matters: gamma gamma -> gamma gamma is loop-level and classically forbidden, whereas g g -> gamma gamma is tree level. Its N^2 part therefore has a classical second-order Einstein-Maxwell counterpart, as B&O v2 concede [D-16, D-54]. Inference: the analogue supports "fusion is real for crossing waves", not "a single outgoing beam decays".
F10. Observation vs inference, B&O consequences. No B&O number has an observational counterpart:
  - The Fig. 2 photons (6e-13 eV, 150 Hz) cannot reach any receiver: the plasma cutoff in the ISM, VLISM, solar wind and ionosphere is 1.6 kHz to 9 MHz [D-40, D-62], and B&O concede this in footnote 4 [D-19].
  - The flux at Earth is 1e-46 photons m^-2 s^-1 against a CMB Rayleigh-Jeans foreground 2e43 times brighter [D-46].
  - The SGWB injected energy falls 1e91 to 1e119 below the distortion thresholds [D-45].
  - Photofission needs nu >~ 5e20 Hz, far above binary frequencies [D-64].
  - Path depletion is 1e-66 to 1e-57, against 2-11% calibration [D-39, D-47].

  The CMB stimulation factor 1 + 2f_gamma = 7.6e8 at 150 Hz [D-43] is an extrapolation of a Planck spectrum that has never been measured below ~GHz (ARCADE-2 starts at 3 GHz and already shows an unexplained excess [D-09]). It is an inference, not an observation.

## Lens-specific outputs

### O1. Observation ledger (what has been measured vs inferred)
| Claim | Observed? (instrument, conditions, uncertainty, replication) | Inferred / theorised | Status |
|---|---|---|---|
| GWs propagate 1e25 m with GR amplitude | Yes: LIGO/Virgo GW150914 at D_L = 410 +160 -180 Mpc [D-30]; GW170817 GW vs EM distance, c_M = -9 +21 -28 (68%) (F4); replicated across ~100s of events (catalogues not retrieved here) | Large vacuum damping excluded | Observed, replicated |
| B&O eq. 8 coefficient 3/(25 pi) | No (pure calculation) | Toolkit `gw_coherent_fusion.py` reproduces it in B&O's real-sign top-hat model (tools.md, not re-run by me) | Theory, unreplicated in literature (0 citations [D-66]) |
| GW -> gamma gamma photons from binaries (Fig. 2) | No; unobservable (plasma cutoff, D-62) | Rate, tau, L_gamma | Inference only |
| GW depletion tau_h | No; 1e-66 predicted vs ~1e-1 sensitivity | | Untestable |
| SGWB emissivity ~1e-110 m^-3 s^-1 | No | Depends on rho_GW, itself only bounded [D-33, D-34] | Untestable |
| CMB stimulation (1 + 2f) at Hz | CMB not measured below ~GHz; ARCADE excess at 3 GHz [D-09] | Planck extrapolation over 9 decades | Inference |
| CMB mu, y constraints on sources | FIRAS limits exist [D-08] | B&O's injection 1e91+ below them [D-45] | Constraints vacuous for GW -> gamma gamma |
| ULDM N_phi ~ 6e87 | DM density measured (0.3-0.6 GeV/cm^3 [D-41]); ULDM itself not detected; 1e-22 to 1e-21 eV disfavoured by Lyman-alpha (F2) | Occupation number | Inference on a disfavoured parameter point |
| ULDM W_phi ~ 1e14 x_MW W | No source exists (no individual SMBHB detected, F3); no detector channel | Resonance fails by 1e11 (F6) | Right arithmetic, wrong quantity |
| Prior claim: G+G -> gamma gamma attenuation (Jones-Singleton) | Tested by GW detection at 410 Mpc | Decay length 1e11 m | Falsified (F8) |

### O2. Base rates (reference classes)
The claim is not a measured anomaly. No instrument has reported anything B&O explain. The relevant reference class is "a new consequence of an established effective field theory, from one group, unrefereed, interpretation revised between v1 and v2 [D-54]." Named cases:
- **Jones & Singleton 2015, same process (G+G -> gamma gamma attenuation):** a large effect, falsified by GW detections (F8). Outcome: failed.
- **Collinear Bogoliubov photon production by plane GWs (Jones, McDougall, Singleton):** contested by Green-function methods and unresolved after ~10 years [D-51]. Outcome: open, narrowed to the exactly collinear sector.
- **Sawyer 2020, collective g g -> gamma gamma in dense graviton clouds [D-06, D-68]:** no follow-up or observation. Outcome: open.
- **Gertsenshtein effect (1962):** accepted theory, never observed, and needs a background B [D-05]. Outcome: real but unobserved after 60 years.
- **Light-by-light scattering (Euler-Heisenberg 1936):** confirmed 2017 (F9), about 80 years after prediction, and only for crossing photons in extreme fields. Outcome: real, required crossing kinematics.
- **Zwicky's 1929 "tired light"** (free radiation loses energy in vacuum): rejected by supernova time dilation. This is general knowledge, not fetched here; included as the archetype of the "free wave decays in vacuum" claim class.

Pattern:
- Of the claims that free radiation loses energy in vacuum, the two that met observation (tired light; Jones-Singleton) failed it. That is 0 of 2.
- Established-EFT consequences that are real have survived as theory, but at tiny size they stay unobserved for decades (Gertsenshtein, light-by-light). When observed, they required non-collinear crossing.
- Failures of single-group EFT claims are usually "the wrong quantity computed correctly" (wrong state, wrong limit, or a rate that is really a total), not wrong algebra. The toolkit's own design note says the same of QFT production (tools.md: "QFT production errors are usually the wrong quantity computed correctly"). This is a judgement, not a statistic: no source gives a numerical survival rate for such preprints.

### O3. Analogues
- **Schwinger and plane waves (QED):** a single plane EM wave of any intensity makes no pairs, because both field invariants vanish (textbook; not fetched). Production needs crossing or focused configurations. This is the exact counterpart of Gibbons for gravity [D-56, D-57].
- **Light-by-light scattering:** confirmed only for crossing photons (F9).
- **Colliding plane GWs (Dorca-Verdaguer):** production occurs in the strong-field interaction region of two counter-propagating waves [D-04].
- **Nonlinear optics:** frequency mixing needs phase-matched, non-collinear or crossing beams. A collinear massless beam has s = 0 [D-55].

What they suggest: graviton fusion is real where independent wavevectors cross. That means a stochastic background of crossing waves (eq. 14, a legitimate crossing-beam rate in principle, negligible in size [D-44]) and the near zone of a source. It does not mean an outgoing wave at r >> lambda, whose wavevectors become locally collinear [D-55, hidden premise 5]. The analogues favour "near-source production, no free-wave decay" over "decay in vacuum".

### O4. What an honest skeptic would require, and whether it exists
| Requirement | Exists? |
|---|---|
| An independent group reproduces eq. 8 in B&O's model | Partly: the toolkit's `gw_coherent_fusion.py` (built in this run) reproduces 3/(25 pi) and 7/(450 pi) for the real-sign top-hat model, gives zero for a pure-circular packet, and otherwise gives pattern-dependent values (tools.md). No published replication [D-66] |
| An in-in calculation for the retarded (outgoing) field showing that production persists at r >> lambda | No; no source [dossier section 6]. Analogues (O3) point the other way |
| A classical second-order Einstein-Maxwell check of the N^2 part | No [dossier section 6]; B&O v2 itself says a semiclassical description exists [D-16] |
| Reconciliation with plane-wave no-go results and Ai-Ellis-Pradler's inclusive-rate result | No [D-51, D-71c] |
| Any observation of GW -> photons, GW depletion, or GW -> ULDM | No, and none is possible within 20 years: every channel falls short by >= 1e30 (F7, F10, [D-45, D-46, D-47]) |
| ULDM eq. 17: a source coherent for 1/sigma_omega ~ 4e4 yr in a 5e-7 band at f = m/h | No such source; real chirps fall short by 9e-12 (F6) |

Conclusion for Q5: no regime, source or observation within the horizon can detect GW -> gamma gamma or GW -> phi phi, or be constrained by it. The question is observationally empty. It can only be settled by theoretical replication.

## Calculations
- `runs/2026-10-13-gravitational-wave-decay-photon-pairs/calc/lens-empiricist_uldm.py` (log beside it). Natural units for the formulas, SI for the outputs.
  - (1) Sympy: eq. 16 into eq. 17, times 2m, equals B&O's printed W_phi (ratio 1).
  - (2) N_phi(1e-22 eV) = 5.75e87. At m = 1e-22, 1e-21 and 2e-20 eV: M = 1.82e11, 1.82e10 and 9.1e8 Msun, and W_phi(x = 1) = 3.8e15, 3.8e13 and 9.6e10 W (E_rel = 2/65 M c^2), or 8.6e15, 8.6e13 and 2.2e11 W (3/65).
  - (3) Resonance at 1e-21 eV: 1/sigma_omega = 1.32e12 s, time in band = 12 s (ratio 9.2e-12), (N_band/N0)^2 = 5.1e-14, in-band W_phi = 2.0 W x_MW. At 2e-20 eV the in-band W_phi = 4.9e-3 W x_MW.
  - (4) W_phi/Lsun = 1.0e-8 and W_phi/L_GW,peak = 1.1e-31 at x = 1e5. x = 1.0e13 is needed for 1 Lsun. The converted GW energy fraction is 5.4e-32.
  - (5) GW170817 c_M range -37 to +12 (68%), equivalent to d_GW/d_EM - 1 from -0.17 to +0.06 at z = 0.0099.

## Candidate answers (at least 3; the null and a reframe count)
- [EMPIRICIST-A] The question is observationally empty. No observation supports GW -> gamma gamma (or -> phi phi) in vacuum, none can test it within 20 years, and B&O's predictions and zero are observationally indistinguishable. The only observational fact in play is that large vacuum GW damping is excluded (GW150914 at 410 Mpc; the GW170817 distance agreement to ~10%). | status: surviving | Every channel falls 1e30 to 1e119 short (F7, F10, [D-45, D-46, D-47]), and the falsified Jones-Singleton version (F8) shows that observation bites only on large effects. | Prediction: no future GW-vs-EM distance comparison shows path loss beyond its errors, and no Hz-kHz photon or spectral-distortion signal is attributed to GWs. The decisive test is theoretical: an independent in-in calculation for a retarded outgoing wave. | confidence: high
- [EMPIRICIST-B] (reframe) Base rates and analogues point to production by crossing wavevectors: the near zone of a source, or independent crossing waves (SGWB). Analogues and base rates do not support a sustained decay of a freely propagating outgoing wave. B&O's arithmetic is probably right in their model, and the physical quantity is probably a near-source total, not a vacuum decay rate. | status: surviving | Rests on: the plane-wave no-go results in QED (Schwinger) and GR [D-56, D-57]; light-by-light seen only in crossing beams (F9); Dorca-Verdaguer colliding waves [D-04]; collinear kinematics s -> 0 [D-55]; and the reference-class pattern that single-group EFT claims fail on "wrong quantity", not algebra (O2). The dossier offers no direct calculation of the r-dependence, so this rests on analogy. | Prediction: an in-in yield for an outgoing packet saturates within r ~ lambda of the source, and the eq. 8 "rate" maps to a finite near-source total; the yield of a pure-circular packet is zero. | confidence: medium
- [EMPIRICIST-C] GWs decay in vacuum into photon pairs as B&O claim, with eq. 8 as a sustained rate and depletion tau_h along the path. | status: strained | No observation supports it, and none could (F10). The only observational test of this claim class falsified its large-effect version (F8). The analogues (O3) all require crossing kinematics, and B&O's own validity condition tau << 1/sigma_omega fails at the nominal GW150914 point [D-42, D-61]. It is not eliminated, because nothing observed contradicts an effect of size 1e-66. | Prediction: an independent in-in calculation finds production at r >> lambda that persists without falling off. | confidence: low
- [EMPIRICIST-D] The ULDM channel (eqs. 16-18) gives astrophysically relevant ("stellar") luminosities from SMBH mergers. | status: eliminated (as a physical or observable consequence; the arithmetic is confirmed) | The algebra is exact (F5). However: eq. 17's resonance needs a coherence of 1.3e12 s where a real chirp spends 12 s in band, and the in-band N^2 suppression is 5e-14 (F6). The fiducial mass is disfavoured by Lyman-alpha (F2). No individual source has been detected (F3). At x = 1e5, W_phi/L_GW = 1e-31, and the products have no detection channel (F7). | Prediction: a correct treatment with the chirp's spectral density in the 5e-7 band gives at most ~W-scale, not 1e14 x_MW W. | confidence: high
- [EMPIRICIST-E] (null for large effects) Vacuum GW attenuation large enough to matter (Jones-Singleton size, decay length ~1e11 m). | status: eliminated | GW150914 was detected over 1.3e25 m with GR amplitude [D-30], and the GW170817 distances agree to ~10% (F4, F8). | confidence: high

## What would change my mind
- An independent published in-in (Schwinger-Keldysh) calculation with a retarded source showing a pair rate that persists, without falling off, at r >> lambda. That would move EMPIRICIST-C up and B down.
- A demonstration that the ULDM eq. 17 regime can be fed by a near-monochromatic, long-lived source (for example a slowly inspiralling SMBHB far from merger, in a 5e-7 band). That would need a source living ~1e12 s in band at large N; for 1e-21 eV such a source would be a wide binary with far lower GW luminosity. It would revive part of EMPIRICIST-D, at a size not computed here.
- Any measurement of GW-EM distance disagreement growing with distance (O5 or third-generation standard sirens), which would reopen large damping (E). Nothing of the kind is reported [D-34, F4].

## Assumptions I relied on
- B&O's ISCO relation m ~ omega_s ~ 8800 pi (Msun/M) s^-1 and E_rel = (2 or 3)/65 M c^2 for SMBH mergers. I assume mass-scaling of GW150914-like waveforms, as B&O do [D-27].
- Newtonian quadrupole chirp rate at f_ISCO for the time in band. Near merger this is order-of-magnitude only, but the 1e-11 shortfall is far beyond any PN correction.
- The in-band graviton number N_band = (dE/df)(f v^2/2)/(hbar omega) is the right input for a rate with sigma_omega = m v^2/2. This is my inference about how B&O's narrow-band formula should be fed. I did not re-derive eq. 17's v^6 power or the SM S10/S11 integral; I took eq. 17 as printed.
- Lagos et al.'s c_M bound converted to a distance ratio with alpha_M ~ c_M at z << 1. This is a modified-gravity parametrisation used here only as an empirical bound on any amplitude damping.
- Toolkit `gw_coherent_fusion.py` results quoted from tools.md, not re-run by this lens.
- Base-rate cases (tired light, Schwinger plane-wave null) not fetched are labelled general knowledge.
