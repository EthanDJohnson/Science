# Brief: The wide-binary low-acceleration anomaly — real or estimator artefact, and what Gaia DR4 will show
slug: 2026-10-11-wide-binary-anomaly-gaia-dr4 | depth: deep | type: anomaly | date: 2026-10-11

## Question as asked
"Is the low-acceleration 'wide-binary anomaly' in Gaia data real, or an artefact of how it is estimated, and what will Gaia DR4 show? Chae and collaborators report that wide binary stars with internal accelerations below about 1e-9 m/s² move faster than Newtonian gravity allows. The boost is γ = G_eff/G of about 1.4–1.5 near 1e-10 m/s², and 1.3–1.6 across analyses, as MOND predicts. Banik, Cookson, El-Badry and others find results consistent with Newton (γ ≈ 1). Weigh the estimators; hierarchical triples and hidden companions; projection, eccentricity and perspective corrections; mass estimates; and sample selection. Then file dated, numerical forecasts, before Gaia DR4 is released, for the γ that each estimator family will return on DR4 data."

## Question made precise
The question is read as: **(a) which of the competing explanations for the disagreement between published wide-binary gravity tests on Gaia DR3 is right, with what credence, and (b) what value of γ will each estimator family return on Gaia DR4 data, filed as a dated, scorable forecast before DR4 opens on 2 December 2026 at 12:00 CET.** The answer is a ranked, mutually exclusive slate of explanations for the DR3 disagreement, plus a prediction matrix with one column per estimator family.

Definitions of loaded terms:
- **Wide binary.** A gravitationally bound pair of main-sequence stars (white dwarfs only if a paper uses them), with projected separation s of roughly 0.2–30 kau, resolved as two sources by Gaia, within roughly 200–300 pc. Chance-alignment pairs, unbound comoving pairs (cluster or moving-group members, dissolving pairs), and pairs with an unresolved third body are **contaminants**, not wide binaries.
- **Internal Newtonian acceleration g_N.** g_N = G M_tot / r², where r is the 3D separation and M_tot the total mass of the pair, or the paper's stated proxy (often with r estimated statistically from s). Every γ in this run is reported **with the g_N bin it refers to and how that g_N is defined.**
- **γ = G_eff/G.** The factor by which gravity would have to be boosted for Keplerian dynamics with G replaced by γG to reproduce the observed relative velocities in a given g_N bin. Equivalents:
  - Chae's Γ ≡ log10 √γ, so γ = 10^(2Γ);
  - a velocity-boost factor b = v_obs/v_Newton, so γ = b²;
  - Banik et al.'s α_grav, which interpolates between a Newtonian template (α = 0) and their MOND template (α = 1). The conversion to γ is part of the scoring rule below.
  For MOND, "Keplerian orbits with G_eff = γ(g_N) G" is an **approximation**, labelled as such. Real MOND, with the Galactic external field effect (EFE), is non-linear and anisotropic. No field solver is built in this run.
- **Normalized relative velocity ṽ.** ṽ = v_p / √(G M_tot / s), the sky-projected relative velocity divided by the Newtonian circular speed at the projected separation. For any bound pair with s ≤ r, ṽ ≤ √(2γ), so ṽ ≤ √2 under Newton.
- **"Real."** The data show a γ above 1 in the low-acceleration regime that survives correct modelling of triples and hidden companions, contamination, projection, eccentricity, perspective, masses and selection. It is a property of gravity, or at least of something other than the estimator and the sample. **"Artefact"** means an unmodelled or mismodelled astrophysical or instrumental effect, or a property of the estimator, produces the measured γ > 1.
- **Estimator families.** Boufourou's taxonomy (arXiv:2608.24556), plus a fourth family. Every published analysis is mapped to exactly one, and the mapping is part of the evidence:
  1. **full-median:** statistics of the whole ṽ (or v_p) distribution, such as medians, quantiles or full-distribution χ², compared bin by bin with a Newtonian calibration. Chae 2023 and 2024 and Hernandez's samples are candidates; the research decides.
  2. **tail-truncated:** robust estimators that cut or down-weight the high-ṽ tail, for example only pairs with ṽ below a threshold, or a trimmed or Huber estimator.
  3. **mixture-likelihood:** a likelihood over the full ṽ distribution, with explicit components for the gravity law, triples, chance alignments and unbound pairs, fitted together. Banik et al. 2024, Cookson et al. 2026 and Pittordis & Sutherland are candidates.
  4. **Bayesian 3D orbit fits:** per-system or hierarchical inference of orbits from positions and proper motions, plus radial velocities where available (Chae 2025 arXiv:2502.09373; Chae et al. 2026 arXiv:2601.21728; Saad & Ting on how sensitive the deprojection is).
- **Hidden companions and triples.** Hierarchical systems in which one or both components is itself an unresolved binary. Such a companion shifts the photocentre and the velocity, by orbital motion and by photocentre wobble averaged over Gaia's baseline, and makes the luminosity-based mass wrong. The **multiple fraction f_multi** is the fraction of wide pairs with at least one such inner binary that matters for the velocity.
- **Gaia DR4.** Gaia's fourth data release, covering 66 months of the nominal mission, against 34 months for DR3. Per ESA's DR4 overview (verify) it adds epoch astrometry, epoch photometry and epoch radial velocities, plus non-single-star solutions including acceleration solutions. The archive opens on 2 December 2026 at 12:00 CET (ESA Gaia news, item of 2026-10-08, rechecked at framing on 2026-10-11).

Admissible physics:
- **Established:** Newtonian gravity and GR in the weak-field limit; stellar astrophysics, meaning mass–luminosity relations, binary and triple statistics, and Galactic tides; Gaia astrometric and spectroscopic error models.
- **Speculative, allowed only when labelled:** MOND (AQUAL or QUMOND), modelled here through a cited, parametrised boost γ(g_N) with the EFE, and any other modified-gravity or dark-matter explanation the research finds.
- **Framing of the physics question:** the run does not have to decide whether MOND is true in general. It has to decide whether **these data** show a boost. Galaxy-scale evidence for or against MOND enters only as a prior, labelled as such and weighed down.

The horizon has two tiers:
- **Now:** which explanation of the DR3 disagreement is best supported today.
- **DR4:** what the first DR4-based analyses will report by the scoring date.

## Hidden premises to test
1. **The data are the same.** The groups use different samples (Chae: El-Badry et al. 2021-based, d < 200 pc, with a specific quality-cut set; Banik et al.: d < 250 pc, s of 2–30 kau, v_p-based). "Same data, different γ" may partly be different data. Check how much of the γ spread is sample and how much is estimator, for example by Boufourou's re-analysis of Chae's 81,088 pairs.
2. **The multiple fraction can be calibrated on Newtonian-regime pairs.** Chae calibrates f_multi at high acceleration (g_N ≳ 1e-8 m/s²) and carries it to low acceleration. That works only if f_multi and the inner-binary period distribution do not depend on separation. Test against Moe & Di Stefano-type statistics and against the excess of close companions in wide pairs.
3. **Triples bias γ upward under Newton.** Boufourou says a full-median estimator gives γ ≈ 1.08–1.13 from purely Newtonian catalogues with 20–30% residual triples. Test this independently. Also test whether that bias is large enough to explain Chae's γ ≈ 1.4–1.5, or only part of it.
4. **Robust estimators are unbiased.** Tail truncation or mixture fits could suppress a real MOND signal if the MOND ṽ distribution moves weight into the tail they cut or absorb. Boufourou says injection-recovery shows they recover an injected boost. Test with γ_inj ∈ {1.0, 1.2, 1.4}.
5. **Eccentricity distribution.** It rises with separation (Hwang, Ting & Zakamska 2022: α of roughly 1.2–1.3 at 1–10 kau, to be verified). Does a mismatch between the assumed and the true distribution produce a spurious γ in a ṽ-distribution test, of what size, and in which family?
6. **Projection and perspective.** Do the projection corrections, from v_p to 3D and from s to r, and the perspective-rotation corrections, which matter for pairs with large angular separation and large proper motion, affect the families differently? What does Saad & Ting's sensitivity of deprojection to priors imply for the Bayesian 3D fits?
7. **Mass estimates.** Errors in the mass–luminosity or mass–magnitude relation, metallicity effects, and unresolved companions all bias M_tot and so ṽ. γ scales as 1/M, so a 10% mass bias is a 10% γ bias. Test whether it can differ between the high- and low-acceleration bins.
8. **Sample selection and quality cuts.** Chae & Yoon (arXiv:2607.14450) say quality cuts bias the null results. Test whether cuts on RUWE, parallax S/N, magnitude or separation select against triples differently with separation, and in which direction they bias γ.
9. **Statistics.** Is the null side underpowered at low acceleration, as Chae & Yoon say, or is the disagreement many σ, as Boufourou's 16σ rejection of γ = 1.4 says? Compute the expected σ_stat per family on DR3 and on DR4.
10. **The MOND prediction is ~1.4 in this regime.** With the EFE from the Galactic field (g_ext ≈ 1.8–2 × 10⁻¹⁰ m/s² near the Sun), the expected boost depends on the interpolating function. Banik & Zhao's simple function gives about 1.44 well below a0, and other choices give 1.35–1.40. Compute γ_MOND(g_N) and its spread, so that "consistent with MOND" has a number.
11. **DR4 settles it.** DR4 brings better proper motions (roughly (66/34)^1.5 ≈ 2.7× smaller errors, to be verified), epoch RVs, and acceleration solutions that flag hidden companions. Does it break the estimator dependence, or do both camps keep their estimators and their γ?

## What counts as an answer
- **A ranked, mutually exclusive slate with credences** for the cause of the DR3 disagreement. It must include at least:
  - **an estimator artefact:** the full-median family is biased upward under Newton by residual triples and contamination, the true γ ≈ 1, and the robust families are right;
  - **an f_multi calibration error on the null side:** the robust or mixture families absorb or under-model a real boost, the true γ ≈ 1.3–1.5, and the anomaly is real;
  - **a sample or selection effect:** the γ spread comes mainly from different samples and cuts, and the true value is whatever the best-defined sample gives;
  - **a mass or eccentricity systematic** common to all families, which would shift every family the same way;
  - **an intermediate value:** true γ between 1.05 and 1.3, with neither camp right;
  - **a reframe**, if the research supports one, for example that the question "γ in a bin" is ill-posed because the EFE makes the MOND boost anisotropic and dependent on orientation.
- **For each candidate:** its causal chain and weakest link; the γ it predicts per family on DR3, against the published values; the evidence for and against it, by dossier ID; and its DR4 prediction per family.
- **An injection-recovery reproduction (the key new output).** An independent generator, not Boufourou's code, produces Newtonian catalogues with f_triple ∈ {0, 0.1, 0.2, 0.3} and MOND-injected catalogues (γ ∈ {1.2, 1.4}). Each estimator family is run on them, and the result says whether Boufourou's 1.08–1.13 Newtonian bias for the full median is reproduced, and whether the robust families recover injected boosts without bias. The sensitivity to the eccentricity distribution, the mass error and the noise level must be stated.
- **A prediction matrix,** with one column per estimator family on DR4 (full-median, tail-truncated, mixture-likelihood, Bayesian 3D fit) and one row per candidate. Each cell holds the predicted γ in the scoring bin.
- **The DR4 forecast** (computed by the main session after the report, from the judge's credences and the statistician's conditional predictions). For each family, the forecast gives:
  - the median, the 68% interval, P(γ ∈ [0.95, 1.05]) and P(γ > 1.25), conditional on Newton and conditional on MOND;
  - the combined forecast, weighted by the judge's probabilities.
- **The scoring rule,** stated now and to be filed verbatim with the forecast (refinements allowed until the forecast is committed, never afterwards):
  - **Papers that count:** the first three preprints posted to arXiv between 2026-12-02 and 2027-06-30 that use Gaia DR4 astrometry, are wide-binary gravity tests, and report γ (or a quantity convertible to γ by the rules here) in a low-acceleration bin. Each is mapped to one estimator family by the method definitions above. A family with no qualifying paper by the scoring date is unscored. If more than one paper falls in a family, the first posted counts and later ones are reported but unscored. Boufourou's pre-registered protocol result counts in whatever family it uses, if it is among the first three.
  - **Bin:** the paper's own lowest-acceleration γ estimate whose g_N range lies wholly below 10^-9.5 m/s² and contains 10^-10 m/s². If none does, the estimate whose bin centre in log g_N is closest to −10.0. If the paper quotes only a single low-acceleration γ, that value. The research may sharpen this before filing (for example to Chae's standard bins); it is frozen when the forecast is committed.
  - **Conversions:**
    - Γ → γ = 10^(2Γ);
    - velocity boost b → γ = b²;
    - Banik-type α_grav → γ = 1 + α_grav (γ_MOND,paper − 1), where γ_MOND,paper is the boost the paper's own MOND template implies in the scoring bin (its v_rel ratio squared). If the paper doesn't state it, use our γ_MOND(g_N) with the Banik & Zhao 2018 simple-function EFE value at the bin centre, as computed in the run.
  - **Score:** for each scored family, the log predictive density of the reported central γ under our combined forecast distribution, plus whether it falls in our 68% interval. The scoring date is 2027-06-30.
  - **Filing:** committed and pushed to this public repository, and a PR opened to main, before 2026-12-02 12:00 CET (target 2026-11-25). Recorded with `prior_runs.py mark` as a scorable prediction.

## Research facets
- **theory:**
  - owns: the Newtonian expectation for the ṽ distribution as a function of eccentricity distribution, projection and the time-averaged separation ⟨r⟩ = a(1 + e²/2); the effect of an inner binary on the photocentre and the velocity;
  - owns: the MOND prediction with the Galactic EFE as a function of g_N (Banik & Zhao 2018 MNRAS 480, 2660; the AQUAL vs QUMOND difference; interpolating functions; the anisotropy of the EFE boost); the parametrised γ(g_N) the calculators use, with citations;
  - leaves measured values to quantitative, critiques to critiques, and Gaia instrument facts to engineering.
- **quantitative:**
  - owns: every published γ, Γ, α_grav or equivalent with its bin, sample size, estimator and quoted errors, from Chae 2023, 2024, 2025 and 2026, Chae & Yoon 2026, Hernandez et al., Banik et al. 2024, Cookson et al. 2026, Pittordis & Sutherland 2023 and Pittordis, Sutherland & Shepherd 2025, Boufourou 2026 and any others;
  - owns: the triple, multiple and contamination fractions (Moe & Di Stefano 2017, El-Badry et al. 2021 and 2024, Hwang et al. 2023 on close companions in wide pairs); the eccentricity distributions with separation (Hwang, Ting & Zakamska 2022); the mass–luminosity relations used;
  - maps each published analysis onto one estimator family, quoting the method sentence that justifies the mapping;
  - leaves the critique of each method to critiques, and DR3 or DR4 instrument facts to engineering.
- **critiques:**
  - owns: estimator and systematics critiques on both sides: Banik et al. on Chae; Chae on Banik et al. and on Cookson et al.; Hernandez on cuts and on kinematic contamination; Boufourou's forensic analysis; Chae & Yoon's three reasons for null results; Saad & Ting on deprojection; Pasquini et al. (arXiv:2602.04661) on radial velocities and hidden companions; Clarke, Loeb and others on perspective effects;
  - owns: the replies to each of these, and any published reproduction or re-analysis;
  - leaves the numbers themselves to quantitative.
- **engineering:**
  - owns: the measurements themselves: Gaia DR3 astrometric precision (parallax and proper-motion errors as a function of G), the RUWE and its use as a binarity flag, the Gaia RVS radial-velocity precision; the El-Badry, Rix & Heintz 2021 catalogue's construction and chance-alignment probabilities; each group's sample cuts and resulting N;
  - owns: what DR4 adds, per ESA's DR4 overview (epoch astrometry, epoch RVs, non-single-star and acceleration solutions, the time baseline), the expected precision improvement, how many DR4 wide binaries an analysis is likely to use, and Boufourou's pre-registered DR4 protocol (Zenodo doi:10.5281/zenodo.22073431; check whether v1.0 has been frozen);
  - leaves the published γ values to quantitative.
- **frontier:**
  - owns: 2025–2026 preprints and talks, newest first: Boufourou (arXiv:2608.24556) and any responses to it; Chae & Yoon (arXiv:2607.14450); Chae et al. 2026 (arXiv:2601.21728); Cookson et al. 2026 (arXiv:2602.24035); Saad & Ting (arXiv:2603.11015); Pasquini et al. (arXiv:2602.04661); Pittordis, Sutherland & Shepherd (arXiv:2504.07569); any DR4-readiness or pre-registration work; any statement by either camp of what it expects from DR4. Each is labelled with its evidential status (refereed, preprint, talk);
  - reports a result already in a journal only when something newer exists, and otherwise leaves it to the facet that owns it.

## Worked calculations
- **mechanist** (owner of the key new output):
  - the injection-recovery reproduction of Boufourou's synthetic results, using the run's two calculators (generator and estimators, independent of Boufourou's code): Newtonian catalogues with f_triple ∈ {0, 0.1, 0.2, 0.3}, injected γ ∈ {1.2, 1.4}, ~1e5 pairs per catalogue, every estimator family run on each;
  - the sensitivity of each family's bias to the eccentricity distribution (Hwang et al. vs thermal), to a ±10% mass bias, to chance-alignment contamination, and to the inner-binary period distribution;
  - the verdict: Boufourou reproduced, partly reproduced or refuted, with numbers. This is the reference for the slate builder, the refuters and the judge.
- **statistician** (owner of the conditional DR4 predictions):
  - per estimator family, the predictive distribution of the DR4 γ in the scoring bin conditional on Newton (true γ = 1) and on MOND (true γ = γ_MOND(bin)): median, 68% interval, P(γ ∈ [0.95, 1.05]) and P(γ > 1.25). Each combines the family's bias distribution (from its own run of the calculators; lenses can't read each other), σ_stat scaled analytically to DR4's sample size, and the spread from analysts' choices (cuts, f_multi priors);
  - the tension between the published DR3 results within and across families, using `stats_tools.py`;
  - a table the main session can combine directly with the judge's credences.
- **constraints:**
  - γ_MOND(g_N) with the EFE for at least two interpolating functions (Banik & Zhao 2018 simple function; the standard or n = 2 function), at the scoring bin and across 1e-11 to 1e-8 m/s²; the bound ṽ < √(2γ) and what the observed ṽ tail implies.
- **empiricist:**
  - the table mapping every published analysis to an estimator family, with its γ in the scoring bin, sample, N and error; the base rate of estimator-dependent "anomalies" in comparable astrophysical tests.
- **main session**, after report.md is saved: the combined DR4 forecast per family, weighted by the judge's credences, in a logged calc script (`runs/<slug>/calc/dr4_forecast.py`, run with `math_run.py`), appended to report.md as "## DR4 forecast".

## Known constraints, prior attempts, and user-supplied data
No user-supplied data. The user's framing notes, kept for the agents:
- **Boufourou** (arXiv:2608.24556, single author, 25 Aug 2026; checked at framing on arXiv):
  - says a full-median estimator yields γ = 1.08–1.13 on purely Newtonian synthetic catalogues with 20–30% residual triples;
  - on Chae 2024's 81,088 pairs, gets γ = 1.045 [1.025, 1.068] with robust estimators and 1.05 [1.04, 1.07] with a mixture fit, rejecting γ = 1.4 at about 16σ;
  - expects σ_stat(γ) < 0.005 on DR4;
  - has a pre-registered DR4 protocol on Zenodo (doi:10.5281/zenodo.22073431, draft v0.95; a frozen v1.0 is promised before 2 Dec) that predicts no γ.
  - His code is public under the MIT licence. **Agents may read it for method only.** Our generator and estimators must be built independently from published physics, so that the reproduction is a real check.
- **Chae & Yoon** (arXiv:2607.14450, 16 July 2026, written before Boufourou; checked at framing) attribute null results to three things: skipping the calibration of the multiple fraction on Newtonian-regime pairs, bias from data-quality cuts, and insufficient statistics. They say proper modelling cannot remove the anomaly.
- **No large data files are committed.** Any Gaia query is a small, documented subset (at most a few thousand rows, with the ADQL saved in `runs/<slug>/calc/`).

Starting points for the researchers. These are leads from the user and the framing session, not established claims; each must be found and quoted before use.
- Cookson, Banik, El-Badry et al. 2026 (MNRAS; arXiv:2602.24035).
- Banik, Pittordis, Sutherland, Famaey, Ibata, Mieske & Zhao 2024, MNRAS 527, 4573 (verify the volume and pages).
- Chae 2023, ApJ 952, 128; Chae 2024a, ApJ 960, 114; Chae 2024b, ApJ 972, 186 (verify each); Chae 2025 (arXiv:2502.09373); Chae et al. 2026 (arXiv:2601.21728), the Bayesian 3D fits.
- Hernandez, Cookson & Cortés, and Hernandez & Kroupa (verify).
- Saad & Ting (arXiv:2603.11015), on deprojection sensitivity.
- Pasquini et al. (arXiv:2602.04661), on radial velocities.
- Pittordis & Sutherland 2023 (Open J. Astrophys.); Pittordis, Sutherland & Shepherd 2025 (arXiv:2504.07569).
- Banik & Zhao 2018, MNRAS 480, 2660, the MOND prediction with the EFE.
- Hwang, Ting & Zakamska 2022 (MNRAS 512, 3383; verify), separation-dependent eccentricities.
- El-Badry, Rix & Heintz 2021, MNRAS 506, 2269, the wide-binary catalogue.
- Moe & Di Stefano 2017, ApJS 230, 15, multiplicity statistics.
- ESA Gaia DR4 overview page (cosmos.esa.int/web/gaia/release), for DR4 contents.

## Calculators (built by toolsmiths during research)
- **`wide_binary_population`:** generates synthetic wide-binary catalogues. It covers Keplerian orbits with an effective G = γ(g_N)·G (labelled as an approximation), separation-dependent eccentricity distributions (thermal, uniform, Hwang-type power law with α(s)), random orbital phase in mean anomaly, isotropic orientation, hierarchical triples with photocentre wobble and Gaia-baseline time averaging, chance-alignment and unbound contaminants, mass-estimate errors, Gaia-like proper-motion and parallax noise, and the cited parametrised MOND boost γ(g_N; a0, g_ext, interpolating function). It outputs arrays: s, v_p, M_est, distance, flags. Numpy only. Self-test anchors:
  - ṽ < √(2γ) for every bound pair;
  - ⟨sin θ⟩ = π/4 for isotropic projection;
  - time-averaged ⟨r⟩ = a(1 + e²/2);
  - γ = 1 reproduces Newtonian Keplerian speeds;
  - the γ(g_N) function reaches its cited deep-MOND and Newtonian limits.
- **`wide_binary_estimators`:** takes arrays (s, v_p, M, g_N proxy, errors) and implements the estimator families: full-median, tail-truncated (threshold and trimmed variants), mixture-likelihood (gravity × {binary, triple, chance-alignment} components), and a simplified Bayesian deprojection fit. It returns γ per g_N bin with bootstrap errors, plus σ_stat scaling to a target N. It **must not import the generator**. Its self-test uses analytic ṽ distributions: for circular orbits with isotropic projection the ṽ distribution is known in closed form, and the estimators must return γ = 1 and γ = 1.4 from distributions drawn analytically at those values.
- Both: ~1e5 pairs, self-test in under a minute, σ_stat scaled analytically to DR4's N.

## Prior runs
None bear on this question.
- 2026-09-30-neutron-lifetime-beam-bottle (2026-09-30): ignore. It is unrelated (neutron lifetime) and matched only on the generic word "anomaly". Its run.json is the model for how this run's forecast is recorded as a scorable prediction.
- The other runs (warp drives, wormholes, problem of time): ignore. They are unrelated.
