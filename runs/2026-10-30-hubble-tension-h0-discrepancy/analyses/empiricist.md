# Analysis: empiricist (Hume)
status: final

## Method applied
What has actually been observed, by which instrument, how many times and by whom, kept apart from what is inferred through a model (ΛCDM Boltzmann fits, lens mass models, N-body cosmic variance, peculiar-velocity reconstructions). Each local and early result is placed on an observation/inference ledger with its replication status; base rates come from past disagreements between established precision methods; analogues come from earlier H0 and age crises and from particle-physics precision anomalies.

## Findings

1. **No H0 in this problem is a direct observation; the question is how many inference steps each result takes and which of them are model-based.** The early side observes θ_* (100θ_* = 1.0411 ± 0.0003) and the spectra; H0 = 67–68 km/s/Mpc follows only through a ΛCDM expansion history [D-01, D-40]. The SH0ES ladder observes Cepheid fluxes and periods, parallaxes, DEB angular sizes, maser kinematics and SN light curves; what it actually measures is M_B (−19.253 ± 0.027 mag), and H0 follows through the Pantheon+ Hubble-flow intercept [D-06, D-21]. The magnitude form is closer to the observation: the SH0ES–CMB-SPA gap is 0.195 mag (9.4%) [calc: runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-empiricist_replication.py].
2. **The early-side observation has been replicated on independent hardware; its H0 inference has not been tested model-free.** Planck, ACT DR6 and SPT-3G D1 are three different telescopes, receivers, scan strategies and sky areas. Each gives 66.5–67.6 km/s/Mpc alone under ΛCDM (Planck PR4 67.64 ± 0.52, ACT 66.51 ± 0.64, SPT 66.66 ± 0.60) [D-02, D-41, D-42, D-43]. Hardware replication of this kind excludes an instrument- or foreground-specific CMB systematic as the main cause. It cannot exclude a shared *model* assumption, because all three use the same Boltzmann physics. Observations that share neither the CMB hardware nor the CMB anisotropies, BAO+BBN at 68.50 ± 0.58 [D-08] and the inverse ladder at 67.19 +0.66/−0.64 [D-48], still assume the standard r_d. The strongest model-light early-side observation is the sound-horizon-free H0 (69.2–70.3, ±1.3–1.4) [D-49], which sits *between* the two sides.
3. **The 73 value has been replicated by only one team at ≤ 1.5% precision.** SH0ES's HST and JWST photometry agree to −0.01 ± 0.03 mag [D-09, D-78]. That is a replication of the photometry on new hardware, by the same team, on hosts the same team selected; it does not test Cepheid physics, SN standardisation or anchors [D-09]. The independent ladder team (CCHP) gets 70.39 ± 1.94 (TRGB, total error) and 67.8–68.8 with JWST alone [D-24, D-25, D-26]. The SH0ES-side reanalyses of CCHP's own JWST data give 72.1–73.3 [D-27, D-28], so the disagreement concerns analysis choices and calibrator samples applied to shared observations, not new observations [D-80].
4. **Local results that exclude the SH0ES team still sit above the early value, at about 3σ rather than 6σ.** Each comparison is with CMB-SPA 67.19 ± 0.38, uncorrelated, two-sided:
   - SH0ES 73.49 ± 0.93: 6.27σ.
   - CCHP 70.39 ± 1.94: 1.62σ.
   - SBF 73.8 ± 2.40: 2.72σ.
   - TDCOSMO 71.1 +2.4/−2.3: 1.68σ.
   - masers 71.6 ± 3.7: 1.19σ.
   - sirens 71.7 +9.4/−7.5: 0.60σ.
   - One-step methods combined (time delays, masers, sirens): 71.27 ± 1.93, **2.07σ**.
   - All local results without the SH0ES team (CCHP, SBF, one-step): 71.56 ± 1.19, **3.50σ**. With the NGC 4258 anchor (about 1.5%) treated as common to CCHP and SBF: 71.47 ± 1.27, **3.24σ**.
   - Without any SN Ia (SBF plus one-step): 72.26 ± 1.51, 3.27σ.

   Against BAO+BBN (68.50 ± 0.58) the non-SH0ES local mean is only 2.31σ high [calc: runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-empiricist_replication.py]. This matches the TDCOSMO companion's own statement, 3.7σ for a no-SN late combination and 2.7σ after excluding the ladder entirely, both against Planck alone [D-57, D-90].
5. **The local classes do not contradict each other.** Grouped χ² across Cepheid-SN, TRGB-SN, non-SN ladder and one-step gives between-group χ² = 2.90 for 3 dof (p = 0.41, 0.83σ), and SH0ES vs CCHP is 1.44σ treated as independent (they share NGC 4258 and some hosts, so the true figure is larger) [calc: runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-empiricist_replication.py]. With today's errors the data cannot tell "everyone local measures ~73" from "the true local value is ~70–71 and SH0ES is high". The non-SH0ES classes are too imprecise (1.2–3.7 km/s/Mpc each) to tell those two apart.
6. **The early side has a small internal disagreement of its own.** CMB-SPA 67.19 ± 0.38 against DESI BAO+BBN 68.50 ± 0.58 gives χ² = 3.57 for 1 dof, a PDG scale factor of 1.89, about 1.9σ. This is the known DESI–CMB Ω_m discrepancy (2.3–2.8σ by the collaborations' own tests) [D-45, D-87] [calc: runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-empiricist_replication.py]. It lies along Ω_m h³ = const and does not move H0 toward 73 [D-87].
7. **Evidence ceilings (minimum Bayes factors, Sellke bound).** These bounds say how much the p-value alone can count against "one common H0":
   - SH0ES vs CMB (6.27σ): odds against the null up to about 4.7 × 10⁷.
   - Non-SH0ES local vs CMB (3.24σ): up to about 45:1.
   - One-step only (2.07σ): up to about 2.9:1.

   So the claim that the tension is decisive rests on the SH0ES measurement. Without it, the evidence is suggestive [calc: runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-empiricist_replication.py].
8. **Precision a ladder-free method needs to settle it.** To separate 73.0 from 67.19 (CMB-SPA error included), a single one-step H0 needs σ ≤ 1.90 km/s/Mpc (2.6%) at 3σ and σ ≤ 1.10 (1.5%) at 5σ. To separate 73 from 70, the more realistic question after the CCHP results, it needs σ ≤ 1.00 (1.4%) at 3σ and 0.60 (0.8%) at 5σ [calc: runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-empiricist_replication.py]. TDCOSMO-2026 is at 3.3% [D-31], so a two- to four-fold improvement is required. Treu's review-level forecast is about 40 lenses for 1% (dossier §6, Schedules; no D-ID, review-level forecast only).
9. **Lensed supernovae add two more single-object one-step points, one on each side.** SN Refsdal: [new: Kelly et al. 2023, Science 380 abh1322, arXiv:2305.06367 abstract, full-text, "Using eight cluster lens models, we infer H0 = 64.8 +4.4-4.3 km / s / Mpc ... Using the two models most consistent with the observations, we find H0 = 66.6 +4.1-3.3 km / s / Mpc"]. SN H0pe: [new: Agrawal et al. 2026, ApJ 1002 187, abstract, "the second lensed SN to yield a measurement of the Hubble constant by the time-delay cosmography method, finding H0=75.4−5.5+8.1km s−1Mpc−1"]. Adding both:
   - one-step mean: 70.53 ± 1.71, 1.91σ above CMB-SPA;
   - non-SH0ES local mean: 71.21 ± 1.13, 3.37σ [calc: runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-empiricist_replication.py].

   Each is a single object with cluster-lens models that move H0 by several km/s/Mpc. This replicates the *method*, not a value.
10. **The independent ladder team states the gap at about 3σ.** [new: Freedman et al. 2025 (CCHP status report), arXiv:2408.06153, full-text, "When including this systematic uncertainty in the supernova calibration, the tension is reduced to 3.0 σ , and is reflecting a more conservative assessment of the measurement's reliability."] CCHP also writes [same source, full-text] that R16 distances corrected to the R22 scale give "72.05± 1.74 km s−1 Mpc−1, resulting in a lower (2.6σ) and much less interesting Hubble tension". These are CCHP's own arguments, contested by SH0ES [D-80], but they show that the ~3σ figure is not this lens's alone.
11. **Base rate: heavy-tailed errors make a nominal 6σ disagreement far less rare than the Gaussian figure.** [new: Bailey 2017, RSOS 4 160600, full-text (Europe PMC published version), "Published scientific measurements typically have non-Gaussian almost-Cauchy ν ∼ 2−4 Student's t -error distributions, with up to 10% of results in disagreement by greater than 5 σ . These heavy tails occur in even the most careful modern research"]. With unit-scale Student's t as an illustration, the chance probability of each disagreement becomes:

    | Disagreement | Gaussian | t, ν = 2 | t, ν = 3 | t, ν = 4 |
    |---|---|---|---|---|
    | SH0ES vs CMB, nominal 6.27σ | 3.6 × 10⁻¹⁰ | 0.025 | 0.008 | 0.003 |
    | Non-SH0ES local vs CMB, 3.24σ | 0.0012 | 0.08 | 0.05 | 0.03 |

    [calc: runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-empiricist_baserates.py]. This does not make the tension a fluke. It means that a single team's 6σ is not by itself decisive evidence of a real effect. Bailey's case list includes a 50σ G_N result from PTB that took 8 years to trace to an "erroneous assumption about their electrostatic torque transmitter unit" [same source, full-text].
12. **Base rate by structure of the anomaly.** This lens's tally of 21 historical precision disagreements (18 resolved) is in Lens-specific outputs, table C:
    - Anomalies carried by a single experiment, team or input ended as new physics in 0 of 12 cases (Wilson 95% upper bound 0.24).
    - Anomalies seen by two or more methods with independent systematics ended as new physics in about 3.5 of 6 (solar and atmospheric neutrinos, cosmic acceleration, and half of the 1990s age crisis).
    - Over all resolved cases, systematics, shared inputs or statistics account for 14 of 18 [calc: runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-empiricist_baserates.py].

    The H0 tension straddles the two classes. Its 6σ part is single-team (SH0ES) against multi-method (CMB × 3 instruments, BAO+BBN, inverse ladder). Its multi-method local part (CCHP, SBF, lenses, masers) is only about 3.2–3.5σ from CMB-SPA and 2.1–2.3σ from BAO+BBN (finding 4).
13. **Several premises in the dossier rest on simulation or model inference, not observation** (Lens-specific outputs, table B):
    - The ΛCDM cosmic variance σ(H0^loc) = 0.31 km/s/Mpc is an N-body result [D-10, D-37]. The observational bound on a void comes separately from the SN Hubble diagram (|δ| > 20% excluded at 4–5σ) [D-11]. The empirical local-structure scatter, σ_H0 = 0.60% against a predicted ~0.42% [D-37], is larger than the simulation predicts, but still about 0.4 km/s/Mpc, far below the gap.
    - Peculiar-velocity corrections come from constrained-simulation reconstructions (Manticore-Local) and move masers by −1.6 to −2.1 [D-32], the TRGB two-rung result by large amounts [D-34], and a forward Pantheon+ intercept from 74.3 to 71.4 [D-82] (preprints). These shifts are as large as the CCHP–SH0ES difference, and they are model outputs.
    - Every early-time new-physics H0 (69–71) is a Boltzmann-code fit to hardware data [D-52, D-53]. The data are observations; the H0 under EDE is an inference whose prior-volume dependence is itself disputed [D-83].
14. **Hardware replication has excluded specific sub-hypotheses outright.**
    - Cepheid photometric crowding as the main cause: JWST against HST, −0.01 ± 0.03 mag, with distance-growing crowding rejected at 8.2σ [D-09, D-78], against the 0.1–0.2 mag needed [D-79b]. This is the one ladder sub-hypothesis that new hardware (JWST NIRCam) has directly tested. The test was run by one team on its own hosts, so an independent repeat would strengthen it.
    - A Planck-specific foreground or A_L problem: ACT and SPT on different hardware give equal or lower H0 [D-02, D-43], and A_L shrinks in PR4 [D-79a].
    - A large local void: the SN Hubble diagram [D-11], and flow corrections that *raise* local H0 [D-36].

## Lens-specific outputs

### A. Observation / inference ledger, by measurement class

| Class | What is observed (instrument) | What is inferred, and through which model | Replication: teams × hardware | Status |
|---|---|---|---|---|
| Cepheid-SN (SH0ES) 73.49 ± 0.93 [D-20] | Cepheid periods and fluxes (HST WFC3, JWST NIRCam); Gaia parallaxes; LMC/SMC DEB angular sizes; NGC 4258 maser kinematics; SN Ia light curves (Pantheon+ compilation) | M_B = −19.253 ± 0.027 mag [D-21] via P–L relation, metallicity term, reddening law; H0 via Hubble-flow intercept at 0.023 < z < 0.15 | 1 team; 2 telescopes (photometry replicated, −0.01 ± 0.03 mag) [D-09]; journal status of the 2025 update unconfirmed | Observed (photometry); inferred (M_B, H0) |
| TRGB/JAGB-SN (CCHP) 70.39 ± 1.94 [D-24]; JWST-only 67.8–68.8 [D-25, D-26] | TRGB and JAGB magnitudes (HST ACS, JWST NIRCam); NGC 4258 anchor; CSP SN photometry | M_B via tip-detection / JAGB mode; H0 via CSP Hubble flow | 1 team. The same JWST data reanalysed by the SH0ES side give 72–73 [D-27, D-28] | Same observations, discordant inferences |
| Non-SN ladders: SBF 73.8 ± 2.4 [D-29]; TF 73.3 ± 4.1 [D-30] | SBF fluctuation magnitudes (HST, recalibrated with JWST TRGB); HI line widths | Zero point via TRGB (NGC 4258) or Cepheid/TRGB hosts | SBF: 1 team, 3.3%. TF shares calibration hosts (not independent) | Observed, low precision |
| Time delays: TDCOSMO 71.1 +2.4/−2.3 [D-31] | Light curves of lensed quasars (monitoring); stellar kinematics (JWST NIRSpec, Keck) | Time-delay distance via lens mass model; mass-sheet degeneracy constrained by kinematics; Ω_m prior | 1 collaboration (blind); MSD treatment alone moved the error 2% → 8% [D-16]; lens modelling moves sirens+lenses by ~8 km/s/Mpc [D-91] | Observed delays; heavily model-mediated H0 |
| Lensed SNe: Refsdal 64.8 +4.4/−4.3, H0pe 75.4 +8.1/−5.5 [new, findings 9] | Image time delays (HST, JWST) | Cluster lens models | 1 object each, several modelling teams | Method demonstrated; values not precise |
| Masers 71.6 ± 3.7 (stat) [D-32] | VLBI disk kinematics, spot accelerations | Disk model; peculiar-velocity correction from constrained simulations (−1.6 to −2.1) | 1 data set (MCP), 3 analyses (73.9, 70.1, 71.6) | Observed; PV correction is simulation-based |
| Sirens 71.7 +9.4/−7.5 [D-33] | GW strain (LIGO/Virgo/KAGRA); one EM counterpart | Waveform-model distance; galaxy-catalogue redshifts | 1 collaboration; 236 events | Observed, uninformative at present precision |
| CMB under ΛCDM: Planck 67.64 ± 0.52, ACT 66.51 ± 0.64, SPT 66.66 ± 0.60 [D-41–D-43] | TT/TE/EE spectra, θ_* to 0.03% [D-40] | H0 via ΛCDM expansion history from z_* to 0 | 3 independent instruments | Observation strongly replicated; H0 is a model inference |
| BAO+BBN 68.50 ± 0.58 [D-45] | Galaxy/quasar/Lyα clustering (DESI); deuterium in QSO absorbers [D-46] | r_d from ω_b + standard pre-recombination physics; ΛCDM shape | 1 BAO survey (DR2, preprint); earlier SDSS concordant | Independent of CMB hardware; shares r_d physics |
| Inverse ladder 67.19 +0.66/−0.64 [D-48] | BAO + uncalibrated SNe (DES-SN5YR) | r_d from CMB; SN standardisation non-evolving | Several groups and SN compilations agree (~67–68) [D-07] | Shares r_d with CMB |
| Sound-horizon-free 69.2–70.3 [D-49]; equality 65–71 [D-50] | Uncalibrated BAO + θ_* + lensing / galaxy shapes | ΛCDM matter-radiation-equality scale | Pre-DESI-DR2; DESI DR1 shared between the two D-49 sets | Model-light; low precision; between the sides |

### B. Simulation- or model-derived steps that the conclusion leans on (inference side of the ledger)

| Claim | Rests on | Hardware check that exists | Missing demonstration, and its cost |
|---|---|---|---|
| ΛCDM cosmic variance of local H0 = 0.31 km/s/Mpc [D-10] | N-body halo catalogues with R16 SN geometry | SN Hubble diagram excludes \|δ\| > 20% [D-11]; empirical scatter 0.60% [D-37] | Repeat on the 2022 SH0ES/Pantheon+ selection: analysis-only, months |
| Peculiar-velocity corrections of 1–3 km/s/Mpc (masers, TRGB two-rung, Pantheon+ intercept) [D-32, D-34, D-82] | Manticore-Local constrained realisations | None independent; 80-realisation variance dominates the TRGB two-rung error [D-34] | Direct distances to flow tracers (DESI peculiar-velocity survey, 4MOST); years |
| H0 under EDE / m_e / PMF = 69–71 [D-52, D-53, D-94] | Boltzmann fits; Bayesian vs profile-likelihood dispute | ACT, SPT and Planck NPIPE all bound f_EDE without a detection [D-53, D-75] | SPT-3G Ext and Simons Observatory damping-tail spectra; 2027–2030 |
| Time-delay H0 [D-31] | Lens mass models + MSD + kinematics | Blind analysis; robust across cosmologies | ~40 lenses with spatially resolved kinematics for ~1% (review forecast, dossier §6) |
| Required r_s cut 7.7–8.3% [D-56] | Scaling arithmetic | n/a (theory) | n/a |
| SH0ES "~6σ" | SH0ES-team analysis, SH0ES-selected hosts | JWST photometry agrees [D-09] | Independent-team re-reduction of all 37–55 calibrator hosts with a common SN photometric system; a JWST cycle-scale programme plus analysis |

### C. Base rates: persistent disagreements between established precision methods

| Case | Structure | Outcome | Source |
|---|---|---|---|
| Hubble 1929 H0 ≈ 500; Baade 1952 two Cepheid populations | ladder-internal | primary-indicator calibration error, factor ~2 | background knowledge, not source-checked here |
| Sandage vs de Vaucouleurs, 50 vs 100 (1970s–90s) | two-team ladder dispute | resolved between them, HST Key Project | [new: Schwarzschild 1999, Physics Today 52 19, abstract, "H0 ... was uncertain to within a factor of two. Estimates ranged from 50 to 100 km/s per megapars…"] |
| 1990s age crisis (GC ages vs 1/H0) | multi-method | mixed: Hipparcos recalibration (systematic) + Λ (new physics) | [new: Pont et al. 1999, IAU Symp. 183, abstract, "Earlier studies (Reid 1997, Gratton et al. 1997) have reported larger distances than expected, especially for the most metal-poor clusters, implying much younger ages"] |
| Solar neutrino deficit; atmospheric anomaly; cosmic acceleration | multi-method, multi-hardware | new physics | background knowledge |
| Proton radius 2010–2019 | precise new method vs established consensus | consensus methods were biased; new e-H agrees with μH | [new: Lumpay et al. 2025, arXiv:2501.11195, abstract, "Recent studies, such as those by Xiong et al. and Bezginov et al., have consistently found a smaller proton radius of about 0.84 femtometers, in line with muonic hydrogen measurements"] |
| Muon g-2 vs data-driven SM, 2006–2025 | experiment (2 labs) vs theory input | shared input on the theory side (HVP); lattice SM agrees | [new: Charity 2026, PoS EPS-HEP2025 037, abstract, "The measurement is consistent with the current Standard Model (SM) value, provided by the g−2 Theory Initiative's latest White Paper [2], which uses lattice QCD te…"] |
| CDF W mass 2022 | single experiment | not confirmed by CMS | [new: Bruschini 2025 thesis, abstract, "The result agrees with both the Standard Model and the worldaverage of direct measurements"] |
| PTB G_N 50σ; CODATA α 6.5σ | single experiment / single input | apparatus assumption; calculation error | [new: Bailey 2017, full-text, quoted in finding 11] |
| Reactor ν anomaly; LHCb R_K; OPERA; BICEP2; Pioneer | single experiment / input | systematic or input | background knowledge |
| Planck A_L; S8 (KiDS-1000 era) | single experiment; multi-survey | reduced by reanalysis | [D-79a, D-54] |
| Neutron lifetime; Newton's G spread; gallium anomaly | two- or multi-method | unresolved | background knowledge |

Tally: [calc: runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-empiricist_baserates.py].
- Resolved single-team, single-experiment or single-input cases: 0 of 12 ended as new physics.
- Resolved multi-method cases: about 3.5 of 6 ended as new physics.
- All resolved cases: 14 of 18 ended as systematics, shared inputs or statistics.

The classification is this lens's own, and the sample is small and selected for fame.

### D. Analogues and what they suggest

- **1990s age crisis.** This is the closest analogue: an H0-linked tension between a stellar ladder and cosmology. A new astrometric mission recalibrated a rung, and new physics (Λ) was also real. Gaia DR4 (2 Dec 2026, dossier §6) is the direct counterpart for the MW Cepheid anchor, and a mixed outcome has precedent.
- **Sandage–de Vaucouleurs.** Two ladder teams, each with errors too small, converged between their values. The SH0ES (73.5) vs CCHP (70.4) dispute, 1.44σ nominal, has the same form. The non-SH0ES local mean of 71.2–71.6 sits between them.
- **Proton radius.** The precise single method was right and the multi-method consensus was biased. This is a warning against counting agreement among methods that share an input: here, the early-side shared r_d physics and the local-side shared NGC 4258 and Pantheon+ photometry.
- **Muon g-2.** A long-standing ~4–5σ precision tension dissolved through a shared input on one side, not new physics. The analogous shared inputs here are the SN Ia calibration compilation (Pantheon+ vs CSP shifts of 0.8–2 km/s/Mpc [D-25]) and r_d.
- **Solar neutrinos.** New physics won only after the anomaly was seen with different hardware *and* a model-independent decisive test (SNO's neutral- vs charged-current measurement) was run. The H0 counterpart is a ladder-free, model-light H0 at ≤ 1.5% (finding 8).

### E. What an honest skeptic would require, and whether it exists

| Requirement | Exists? |
|---|---|
| A local H0 ≥ 72 at ≤ 1.5% from a team independent of SH0ES, with its own calibrator selection and SN photometry | **No.** CCHP gets 70.4 ± 1.9 [D-24]; SBF 73.8 ± 2.4 (3.3%) [D-29] |
| A ladder-free one-step H0 at ≤ 1.5% (5σ against 67.2 if the truth is 73) | **No.** Best is TDCOSMO at 3.3% [D-31] |
| A ladder blind analysis | **Partial.** TDCOSMO and H0DN are blind; no SH0ES R22 or CCHP blinding statement was found (dossier §6) |
| Reciprocal reanalysis of the SH0ES and CCHP data in one SN photometric system | **Partial.** SH0ES-side reanalyses of CCHP data exist [D-27, D-28]; no CCHP reply; Hoyt calls for independent low-z SN analyses [D-80] |
| For early new physics: a detection without a ladder prior, replicated on two CMB instruments | **No.** Bounds only from ACT, SPT and Planck NPIPE [D-75]; the eROSITA 3.2σ [D-94] and the profile-likelihood f_EDE ≈ 0.09 [D-53] are not replicated by SPT |
| For a late-time M_B/G_eff transition: a direct observation of an M_B step at z ~ 0.01 | **No** [D-92] |
| For local structure: an observed underdensity of δ ≈ −0.5 to −0.8 on ~100 h⁻¹ Mpc | **No.** Excluded by SN data [D-11, D-77] |

## Calculations

- `runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-empiricist_replication.py` (log beside it) computes local H0 combinations by replication class, their tensions with CMB-SPA and BAO+BBN, a grouped χ², the gaps in magnitudes, minimum Bayes factors and the precision needed. All values in km/s/Mpc unless stated:
  - One-step: 71.27 ± 1.93, 2.07σ from CMB-SPA. Non-SH0ES local: 71.56 ± 1.19, 3.50σ; 71.47 ± 1.27 (3.24σ) with the NGC 4258 correlation. No SN Ia: 72.26 ± 1.51, 3.27σ.
  - With the lensed SNe added: one-step 70.53 ± 1.71 (1.91σ); non-SH0ES local 71.21 ± 1.13 (3.37σ).
  - SH0ES vs CMB-SPA: 6.27σ, 0.195 mag (9.4%). Non-SH0ES local vs CMB-SPA: 0.137 mag (6.5%).
  - Between-class χ² among local classes: 2.90 for 3 dof (p = 0.41). CMB-SPA vs BAO+BBN: χ² = 3.57, S = 1.89.
  - Sellke maximum odds against one common H0: 4.7 × 10⁷ (SH0ES), 45 (non-SH0ES), 2.9 (one-step).
  - Precision needed: 1.10 km/s/Mpc (1.5%) for 5σ between 73 and 67.19; 0.60 km/s/Mpc (0.8%) for 5σ between 73 and 70.
- `runs/2026-10-30-hubble-tension-h0-discrepancy/calc/lens-empiricist_baserates.py` (log beside it) computes Student's t two-sided tails, checked against the exact Cauchy and ν = 2 values (PASS), and the historical-case tally with Wilson intervals:
  - Unit-scale t(ν = 2 to 4) at 6.27σ gives 0.025 to 0.003; at 3.24σ, 0.08 to 0.03.
  - New-physics share: 0/12 in resolved single-source cases; 3.5/6 in multi-method cases.

## Candidate answers (at least 3; the null and a reframe count)

- [EMPIRICIST-A] **Distance-ladder systematic located in the SN-calibration step of the SH0ES Cepheid ladder.** The suspects are calibrator-host selection, the low-z SN photometric compilation (Pantheon+ against CSP), and peculiar-velocity or selection treatment, not Cepheid photometry. It would place the true local value near 70–72 and remove roughly half of the 0.195 mag gap. | status: surviving | why: Several observations point there:
  - the independent team gets 70.4 ± 1.9, and 67.8–68.8 from JWST alone [D-24, D-25, D-26];
  - the same JWST data give 68–73 depending on which calibrators and which SN compilation are used [D-25 Hoyt: Pantheon+ +2 km/s/Mpc at 3.1σ, against +0.8 for CSP; D-27, D-28];
  - SN-standardisation, selection and flow reanalyses move H0 by 1–3 km/s/Mpc [D-35, D-82, D-88];
  - every non-SH0ES local class sits at 70.4–73.8, with mean 71.2–71.6 (finding 4).

  The crowding sub-hypothesis is eliminated by JWST against HST, −0.01 ± 0.03 mag [D-09, D-78], against the 0.1–0.2 mag needed. Metallicity and the MW anchor are strained: dropping the metallicity term gives 73.08, and dropping the MW parallaxes gives 73.61 [D-23]. Evidence against the candidate as a whole: SBF (73.8 ± 2.4) and the H0DN leave-one-out variants stay at 72.5–73.6 [D-23, D-29], and SH0ES attributes the CCHP difference to *CCHP's* sample selection [D-28]. | distinguishing prediction or test: a full-sample (≥ 35-host) TRGB/JAGB recalibration by CCHP, or a third team, with a common SN photometric system lands at 70–71 (candidate) rather than 72.5–73.5. Gaia DR4 (Dec 2026) tests only the MW-anchor sub-hypothesis, and H0DN without MW parallaxes is already 73.61 [D-23]. | confidence: medium
- [EMPIRICIST-B] **Reframe: the robustly observed anomaly is two separate things.** The first is a ~3 km/s/Mpc (~0.1 mag in M_B) calibration disagreement between SH0ES and the rest of the local data. The second is a ~4 km/s/Mpc (~0.13 mag, ~6%) residual between all non-SH0ES local results and the early value. That residual stands at 3.2–3.5σ against CMB-SPA and 2.1–2.3σ against BAO+BBN, so it is suggestive but not yet established. The "~6σ, 8–9%" framing rests on one team. | status: surviving | why: The calculation shows 6.27σ for SH0ES against 3.24–3.50σ without SH0ES, with maximum odds of 4.7 × 10⁷ against about 45 (findings 4, 7). It matches CCHP's own ~3σ [new: Freedman 2025, finding 10] and TDCOSMO's 2.7–3.7σ for no-ladder or no-SN combinations [D-90]. Base rates favour systematics for single-team anomalies (0/12) and give multi-method anomalies roughly even odds (finding 12). | distinguishing prediction or test: a ladder-free H0 at ≤ 1.5% (TDCOSMO-scale lens sample with JWST/ELT kinematics, or Rubin/Roman lensed SNe). If it gives ≥ 72.5, the residual is real and the early-side model is wrong. If it gives ≤ 69, the whole gap is local calibration. | confidence: medium
- [EMPIRICIST-C] **Null: statistical fluctuation plus underestimated errors spread over several measurements, with no single dominant cause.** | status: strained as the whole explanation; surviving as a contributor | why: Heavy-tailed measurement errors (Student's t, ν ≈ 2–4) give a nominal 6.27σ gap a chance probability of about 0.003–0.025 rather than 4 × 10⁻¹⁰ [new: Bailey 2017; calc baserates]. The local classes are mutually consistent (p = 0.41), and the early side has its own 1.9σ CMB–BAO+BBN offset (finding 6). Against the null as the whole story: the gap has kept its sign and roughly its size through every SH0ES update from R22 to 2025, across HST and JWST [D-20]. Also, 7 of the 8 non-SH0ES local point estimates (CCHP, SBF, TF, TDCOSMO, masers, sirens, H0pe; all but Refsdal) lie above CMB-SPA [findings 4, 9]. | distinguishing prediction or test: under the null, future independent local measurements scatter around the early value; under the others they do not. A ≤ 1.5% one-step value within 1σ of 67–68 would revive it. | confidence: low
- [EMPIRICIST-D] **Early-time new physics (EDE, ΔN_eff/SIDR, varying m_e, PMF) raising the early-universe H0.** | status: strained | why: No detection without a ladder prior has been replicated on independent CMB hardware. Planck NPIPE, ACT and SPT give upper bounds (f_EDE < 0.061–0.12) [D-53, D-75], and ACT finds no preference for any of these models [D-13]. N_eff = 2.86 ± 0.13 [D-74]. The positive hints come from model-dependent analysis choices: profile likelihood with Planck ℓ < 1000 and no SPT [D-53], and eROSITA plus external data [D-94]; neither is replicated. Best fits reach 69–71.4, which would close at most the non-SH0ES residual of EMPIRICIST-B, not the SH0ES value [D-52, D-53]. | distinguishing prediction or test: an f_EDE or ΔN_eff detection at > 3σ in SPT-3G Ext or Simons Observatory damping-tail data without a ladder prior, with the same sign in ACT. | confidence: medium
- [EMPIRICIST-E] **Late-time new physics changing H(z) after recombination** (evolving or phantom dark energy, low-z transitions). | status: eliminated for H(z) variants; strained for M_B/G_eff variants | why: The inverse ladder is an observation chain (BAO + uncalibrated SNe) that fixes H0·r_d and gives 67–68 for any smooth H(z). Plausible SN systematics move it by < 0.1 km/s/Mpc [D-07, D-48, D-70], and DESI's w0wa preference *lowers* H0 [D-12, D-51]. M_B or G_eff transitions [D-92] escape this argument but have no positive observation. | distinguishing prediction or test: a step of ~0.2 mag in SN Ia M_B, or in Cepheid/TRGB physics, between z < 0.01 calibrators and the Hubble flow, testable with distance-limited calibrators against z ~ 0.02–0.05 SNe with SBF or TRGB distances. | confidence: high (H(z) variants eliminated); low (M_B variants)
- [EMPIRICIST-F] **Local structure (underdensity or bulk flow).** | status: eliminated as the dominant cause | why: The bound is observational. The SN Hubble diagram excludes |δ| > 20% at 4–5σ [D-11], and flow corrections *raise* local H0 by +0.6 (SNe) and +1.4 (SBF) [D-36]. The needed δ ≈ −0.5 to −0.8 [D-37, D-10] is ~20σ in ΛCDM (an N-body inference). The empirical local-structure scatter of 0.60% [D-37] is about 0.4 km/s/Mpc. | distinguishing prediction or test: Banik's claim that expansion converges to CMB-consistent values for z ≳ 0.2 [D-84] is testable with high-z calibrated SNe from Roman. | confidence: high
- [EMPIRICIST-G] **Early-universe analysis systematic (CMB foregrounds, likelihood, A_L, BAO reconstruction).** | status: eliminated as dominant | why: Three independent CMB instruments agree on low H0 [D-02], PR4 removes the A_L preference [D-79a], and likelihood choice moves H0 by ~0.24 [D-41]. BAO+BBN with no CMB anisotropies gives 68.5 [D-08]. The residual CMB–DESI offset (1.9σ here, 2.3–2.8σ in collaboration tests) moves H0 *up* only to 68.5, not toward 73 [D-87]. | distinguishing prediction or test: Simons Observatory and SPT-3G Ext should reproduce 67–68 under ΛCDM. A shift of ≥ 1 km/s/Mpc between experiments would reopen it. | confidence: high

## What would change my mind

- A local H0 ≥ 72.5 at ≤ 1.5% from a ladder-free method, or from a team independent of SH0ES using a common SN system, would move me from EMPIRICIST-A/B toward "the gap is real and the early-side model is wrong". Combined with a replicated ladder-prior-free f_EDE or ΔN_eff detection, it would strongly favour EMPIRICIST-D.
- A CCHP-style full-sample (35–55 host) TRGB/JAGB result at ≥ 72.5 would strain EMPIRICIST-A. A SH0ES full-sample TRGB/JAGB result with CSP photometry at ≤ 70.5 would confirm it.
- A ≤ 1.5% one-step H0 at 67–68.5 would make EMPIRICIST-A/C the whole story.
- If Gaia DR4 MW parallaxes shift the MW-anchored Cepheid zero point by ≥ 0.05 mag, the anchor sub-hypothesis would revive.
- A SH0ES reply showing the Percival, Dong or Wojtak–Hjorth corrections [D-88, D-82, D-35] are wrong would weaken EMPIRICIST-A's SN-calibration branch.

## Assumptions I relied on

- The dossier's current values and supersession choices (D-20, D-24, D-29, D-31–D-33, D-44, D-45) are correct. Several key local values are preprints (TDCOSMO-2026, the masers, GWTC-5.0) or have unconfirmed journal status (Riess 2025) [D-20, D-31–D-33].
- The combinations treat classes as independent except for an approximate 1.5% NGC 4258 term. Real correlations are larger: NGC 4258 is shared by SH0ES, CCHP, SBF and JAGB, and SH0ES re-observes CCHP hosts. This probably makes the non-SH0ES significance (3.2–3.5σ) a slight overestimate. The statistician owns the full covariance.
- Asymmetric errors were symmetrised for the weighted means (the mean of the up and down errors).
- Student's t base rates use unit scale for illustration. Bailey's fitted core widths are not reproduced.
- The historical-case tally is my classification of a small sample selected for fame. Several cases cite background knowledge, labelled as such.
- I treat CMB-SPA 67.19 ± 0.38 as the early reference. H0DN's 67.24 ± 0.35 is unreconciled with it [D-44] but differs negligibly.
