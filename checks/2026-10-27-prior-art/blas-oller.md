# Prior art: Blas & Oller, "Gravitational waves decay in vacuum" (arXiv:2607.24930), our independent check
status: final
Checked: 2026-10-27. Finding dated 2026-10-12.

## The finding

Source in this repository: `checks/2026-10-11-blas-oller-gw-decay/report.md`. Its section 1 is the bottom line, section 3 the verdict table and section 8 the corrections of 2026-10-27. Scripts are in that folder's `calc/` and logs in its `notes/`.

**The paper.** D. Blas and J. A. Oller (B&O), arXiv:2607.24930. It is an unpublished preprint: v1 was posted 27 Jul 2026 and v2 on 31 Jul 2026. v1 had a longer title, "Gravitational waves decay in vacuum: a low energy effect of quantized gravitation".

B&O claim that a gravitational wave, treated as a coherent graviton state, decays into photon pairs in vacuum through graviton fusion, g g → γγ. Their eq. 8 gives the rate as dP/dt = 3G²N²ω³σ²/(25π) pairs per unit time. From this they derive:
- the photon luminosity of binaries (Fig. 2);
- the depletion of a stochastic background (eq. 14);
- CMB stimulation (a factor 1+2f);
- a cosmological integration (eq. 19/S12);
- decay into ultralight dark matter (eqs. 16-18).

**What our check confirms within their model:**
- the eq. 6 magnitudes;
- the 3/(25π) coefficient;
- eq. 14, 8πG²ρ²/15;
- the drop-out of coherent intermediate gravitons;
- the ħ counting;
- the S10 amplitudes and the scalar 7/(450π).

**Our six points:**
- **P1 (helicity phases).** The eq. 6 labels are spin projections on a common axis, not physical helicities. A rephasing-invariant product shows that no phase convention makes all the amplitudes real at once, yet eq. 7 adds them as real positive numbers. For physical coherent states the eq. 8 coefficient is 0.25-0.60 of 3/(25π), depending on the polarisation pattern, and exactly 0 for a circularly polarised wave.
- **P2 (wrong field).** The in-state |f> = S_source|0> carries the Pauli-Jordan field (retarded minus advanced). That field is an incoming spherical shell that focuses on the source and then re-expands. About 85% of the eq. 8 probability (l = 0) is generated within one wavelength of that focus.
- **P3 (δ(0) → T).** Kept exactly, the energy delta gives a finite in-out total of (4/25)G²N²ω³σ pairs. Eq. 8 is the peak of a sinc⁴ time profile with effective duration 4π/(3σ), not a sustained rate.
- **P4 (no decay in flight).** For a physical outgoing wave, the pair yield beyond radius r_min falls as r_min⁻³, and the rate falls as r⁻⁴ while the shell passes r. This is a formation-length effect. So there is no sustained decay, no reaction time τ and no depletion along the path. That contradicts eqs. 9-12, footnote 4 and S12, which overcount by 3σ/(4πH), about 1.7e21 in one example.
- **P5 (binning).** B&O present fractional-bandwidth binning as giving a lower bound. It is not a guaranteed lower bound and overestimates for long bins.
- **P6 (profile).** Eq. 5 uses a Gaussian profile, but eq. 7 and S6 use a top hat. The 3/(25π) coefficient is specific to the top hat. At equal N and σ, the Gaussian gives a 4π larger peak rate and a 3.76× larger total.

**Open.** Production close to the source is not computed. We do not claim B&O's merger numbers are orders of magnitude too large. We claim they describe production near the source while it radiates, not decay of the wave in vacuum.

## Verdict

**Partly anticipated.** No paper, comment or reply makes any of P1-P6 about Blas & Oller. As of 2026-10-27 the paper has no citations in INSPIRE, OpenAlex or the Semantic Scholar search listing, and its latest version is still v2.

One core point is partly anticipated: P4's far-from-source, plane-wave limit is established physics.
- Gibbons (1975): a gravitational wave far from its source propagates "without hindrance by quantum effects".
- Liu (2007): no dissipation into any local quantum field theory, "regardless of the nature and the strength of the interaction".
- Khusnutdinov (2026): photons made collinear with a plane wave "would remain there and leave with the sandwich".

B&O themselves concede the plane-wave no-production result. The coherent-state, spherical-wave part of P4 is not found anywhere, and neither are P1, P2, P3, P5 or P6. The physical principles behind P1 and P2 are standard textbook and amplitudes-literature material.

## Is the finding itself right?

Nothing in this pass contradicts the finding.

**Direct checks against B&O's text** (arXiv v2, `fetch_text.py`, by the versions and cite-check runs and re-run here where marked):
- **Our quotes are accurate.** All 19 double-quoted B&O passages in report section 2 are verbatim in v2. No equation, number or figure changed from v1 to v2. The arXiv comment says "results unchanged", and a word-level diff of the two versions agrees.
- **Eq. 7 adds the eq. 6 magnitudes with the same sign.** A sympy check confirms 4πG(s²−2tu)/s = ½(8πG t²/s + 8πG u²/s) when s+t+u = 0 (`calc/bo_eq7_algebra.py`). v2 has no passage on phases or interference. This is the premise of P1.
- **B&O's own wording matches the P2 setup.** They write "the final state after the source is active is |f> = S|0>" and use it as the initial state of the γγ process. They also call the eq. 5 kernel "the Pauli-Jordan function". They never discuss its incoming half: v2 has no relevant hits for "advanced", "incoming", "formation" or "focus".
- **The P3 and P4 targets are in v2.** These are the S6 step "2πδ(0)→T, the interaction time", eqs. 9-12, the depletion sentence, footnote 4 ("the sphere of radius τ") and S12.
- **B&O concede the plane-wave limit.** Their p. 1 says "no particle production occurs for an individual plane-wave GW [21–26]" (re-verified today).

**Independent recomputations done for this judgement:**
- **P1 invariant (new script, `calc/bo_p1_p6_independent.py`).** The script builds the invariant only from little-group-covariant spinor expressions, not from the check's module. Any expression with the right helicity weights differs from the true amplitude by a real function of the s_ij, so this fixes arg I up to a sign or π.
  - The magnitudes reproduce t²/s and u²/s.
  - All nine phases match taskA1 exactly. For example, they are +63.87°, −17.09° and −125.78° for photons at θ = 60°, φ = 17°.
  - Phases away from 0 and π mean that no phase convention makes all the eq. 6 amplitudes real at once. This confirms P1's key step.
  - The 0.25-0.60 coefficients themselves were not recomputed here.
- **P6 ratios (same script).** With R(t) ∝ |f̃(t)|⁴ in the narrow-band limit, at equal N and σ, sympy gives:
  - a Gaussian/top-hat peak ratio of exactly 4π;
  - a total ratio of 3√(π/2) = 3.7599;
  - ∫sinc⁴(σt/2)dt = 4π/(3σ), the T_eff of P3.
- **P3 bookkeeping** (`calc/coherent_deltaT_check.py`, coherent run). The eq. 8 rate × 4π/(3σ) equals (4/25)G²N²ω³σ exactly.
- **P4 exponent** (`calc/plane_wave_scaling.py`, plane-wave run). From eq. 6, the rate between nearly parallel gravitons goes as θ⁴. With θ ~ λ/r this gives r⁻⁴, matching P4's exponent. That is a consistency check only, not a rederivation.

**Wording that should be tightened.** These are not errors in the physics.
- **P5.** B&O's binning sentence continues: "However, four terms are involved by squaring the modulus of Eq. (7) ... and they increase the decoherence as ϵ grows." Our overestimate (σt_ε)²/(4π²) is computed only for long bins (σt_ε > 50). The median allowed bin has σt_ε = 2.684, where no ratio was computed (report section 8). So P5 should say "not a guaranteed lower bound; overestimates for long bins; size open".
- **P6.** B&O state the switch openly ("For convenience, we approximate the previous profile by a narrow-band top-hat distribution"). The new point is the consequence for the coefficient, not that the switch was hidden.
- **The open item.** The 0.3-0.7 estimate counts pairs made just outside λ/2π. Production inside λ/2π was not computed (report section 8).
- **P2's last step is analytic only.** The claim that the physical field is the retarded one when the source sits inside the time-ordered product was not checked numerically (report section 6.2). The published identities below support it.

**Not re-checked by anyone in this pass:**
- the r_min⁻³ coherent-state yields;
- the 85% focus fraction;
- the physical-shell coefficients 0.25-0.60;
- the 1.66e21 S12 overcount.

These rest on the original check's scripts, several of which have independent cross-routes (report section 5).

## Point by point

| Our point | Status | Closest prior work (citation, link, date, status) | Verified quote |
|---|---|---|---|
| P1 helicity phases: eq. 6 labels are common-axis spin projections; no convention makes them all real; physical coefficient 0.25-0.60 of 3/(25π), 0 for circular | Not found. Background only | H. E. Haber, TASI lectures on spin formalism (Jacob-Wick convention), [hep-ph/9405376](https://arxiv.org/abs/hep-ph/9405376), 1994, lecture notes. Also Kallberg, Brodin & Marklund, CQG 23 L7, [gr-qc/0410005](https://arxiv.org/abs/gr-qc/0410005), 2004/2006, peer-reviewed (classical stimulated four-wave version; relative phase of the GW and EM envelopes) | Haber: "These two results yield states that differ by a phase, so a convention is required." Kallberg et al.: "initial amplitudes and relative phases of the wave envelopes" |
| P2 wrong field: S_source\|0> as an in-state carries the Pauli-Jordan field, with an incoming shell focusing on the source; about 85% of the probability is made at the focus | Not found as applied. The underlying identity is standard | Kosower, Maybee & O'Connell, JHEP 02 (2019) 137, [arXiv:1811.10950](https://arxiv.org/abs/1811.10950), 2018, peer-reviewed. Cristofoli, Gonzo, Kosower & O'Connell, PRD 106, 056007, [arXiv:2107.10193](https://arxiv.org/abs/2107.10193), 2021, peer-reviewed. B&O themselves name the kernel "the Pauli-Jordan function" | KMOC eq. 6.26: "F_ret(x) − F_adv(x) = −F_in(x) + F_out(x)". Cristofoli et al.: "In the far future, where the observer measures the wavetrain emitted from the scattering event, G_adv will vanish." |
| P3 δ(0) → T: finite total (4/25)G²N²ω³σ; eq. 8 is the peak of a sinc⁴ profile, T_eff = 4π/(3σ) | Not found. QED analogue only | Dinu, Heinzl, Ilderton, Marklund & Torgrimsson, PRD 90, 045025, [arXiv:1405.7291](https://arxiv.org/abs/1405.7291), 2014, peer-reviewed (light-by-light scattering, finite pulses). B&O flag the step only as an approximation valid for 1/σ ≫ τ | Dinu et al.: "We find that models which do not account for pulse duration can overestimate all signals in near head-on collisions by up to an order of magnitude." |
| P4 no decay in flight: yield beyond r_min ∝ r_min⁻³ (formation length); no τ, no depletion; S12 overcounts by 3σ/(4πH) | **Partly anticipated** (the plane-wave, far-from-source limit only, which B&O concede). The coherent-state spherical result, r_min⁻³, formation length and S12 overcount are not found | G. W. Gibbons, Commun. Math. Phys. 45, 191, [doi:10.1007/BF01629249](https://doi.org/10.1007/BF01629249), 1975, peer-reviewed. X. Liu, [arXiv:0706.0231](https://arxiv.org/abs/0706.0231), 2007, preprint (not cited by B&O). N. Khusnutdinov, Eur. Phys. J. Plus 141, 532, [arXiv:2508.11558](https://arxiv.org/abs/2508.11558), 2025/2026, peer-reviewed | Gibbons: "This means that a gravitational wave far from its source will propagate without hindrance by quantum effects." Liu: "It shows that gravitational waves far from its source propagate without dissipation via any quantum field theoretic effects." Khusnutdinov: "...they would remain there and leave with the sandwich. After passing the GW package, we cannot detect the created photons." |
| P5 binning is not a lower bound (it overestimates for long bins) | Not found in any verified source. B&O half-state the concern themselves. An AI-written review may overlap, but it is **unverified** | B&O v2, [arXiv:2607.24930v2](https://arxiv.org/pdf/2607.24930v2), 31 Jul 2026, preprint (the same sentence is in v1). The Pith AI review (pith.science, dated 3 Aug 2026, not peer-reviewed) could not be read: 0 characters by `fetch_text.py`, only a WebFetch paraphrase | B&O: "Dividing the GW into fractional bandwidth bins ϵ yields a lower bound on the emissivity, as any residual coherence between bins is neglected. However, four terms are involved by squaring the modulus of Eq. (7) to calculate the probability, and they increase the decoherence as ϵ grows." Pith: no verified quote |
| P6 Gaussian (eq. 5) vs top hat (eq. 7/S6); 3/(25π) is specific to the top hat; ×4π peak, ×3.76 total | Not found. B&O disclose the switch but not its consequence | B&O v2 p. 2, [arXiv:2607.24930v2](https://arxiv.org/pdf/2607.24930v2), preprint. Dinu et al. 2014 (above) is a QED analogue about idealised pulse shapes | B&O: "For convenience, we approximate the previous profile by a narrow-band top-hat distribution" |
| Open item: production near the source (not one of our claims) | Context only | Rahvar, [arXiv:2606.17178](https://arxiv.org/abs/2606.17178), 2026, preprint. Franchino-Viñas, Varacalli & Zanusso, [arXiv:2608.25540](https://arxiv.org/abs/2608.25540), 2026, preprint. Chakraborty & Majumdar, PRD 110, L021701, [arXiv:2404.01840](https://arxiv.org/abs/2404.01840), 2024 | Rahvar (v1 only): "Our calculation is valid in the weak-field, large-separation inspiral regime and is not expected to capture the strong-field, nonlinear merger phase." |

## Closest prior work

**Commentary on Blas & Oller itself.** No verified item exists.
- INSPIRE record 3183912 shows 0 citations. I re-ran `refersto:recid:3183912` today and it returned 0.
- OpenAlex and the Semantic Scholar search listing also show 0 citations.
- There is no comment, reply, erratum, journal version, news item or talk.
- A web-search summary claiming the paper appeared as "PRD 113, 106022" was a conflation with a different Blas paper, arXiv:2512.14864.
- The one third-party item is the Pith review, an AI-generated referee report dated 3 Aug 2026 that no human has reviewed. Its page is bot-gated: `fetch_text.py` returned 0 characters, so its wording is **unverified**. As paraphrased by WebFetch, it says eq. 8 assumes a real top-hat profile with no spectral phase, and that a chirp's phase curvature inside a bin suppresses the rate. That would be a thin overlap with P5 and P6. The paraphrase also says it does not call the lower bound wrong and does not touch P1-P4.

**P4: plane waves do not decay far from their source.** These works are the partial anticipation.
- **Gibbons 1975** (B&O ref. [22]) treats a quantised scalar test field on an exact plane-wave metric. He finds no particle creation and a vanishing renormalised stress tensor. He also gives the kinematic reason, hedged with "presumably": "the creation of one or more particles with timelike or lightlike momentum would violate the conservation of momentum unless the created particles were massless and precisely aligned with the momentum of the graviton" (verified, p. 10).
- **Liu 2007** extends this to any local causal QFT coupled covariantly to gravity, interacting ones included. He explicitly raises the worry that soft photons from interacting QED could accumulate "over a cosmic distance". He uses a c-number plane-wave metric, quantised matter, no gravitons ("We exclude gravitons from this field theory") and no spherical wave. B&O do not cite it. It is the most general published statement of P4's far-zone limit.
- **Khusnutdinov 2026** (B&O ref. [25]) shows the same for the Maxwell field, and adds that photons made collinear with the wave would leave with it.
- **Background:** Deser 1975 (ref. [23]), Garriga & Verdaguer 1991 (ref. [26]) and Dunne quoting Schwinger (ref. [24]): "at least two plane waves are necessary to produce a pair" (verified).
- **How it relates.** B&O write that "no particle production occurs for an individual plane-wave GW [21–26]" and that "we will go beyond this limit". In v2 they say their calculation is equivalent to second-order photon creation in the classical background h^c.
  - Together with Liu's theorem, this implies that whatever B&O compute must come from where h^c is not a plane wave. That inference is ours, not anyone's published statement.
  - Our P2 and P4 locate that region: the focus and the source zone.
  - The published works give the plane-wave limit only. Nobody computes a finite spherical wave, the r_min⁻³ yield, a formation length for gravitons, or the S12 overcount.

**P4 kinematic ingredients** (background; none concerns B&O):
- Fiore & Modanese 1996 (massless decay phase space "reduces to a line");
- Bonnor 1969 ("two parallel beams shining in the same sense ... do not interact");
- Faraoni & Dumse 1999;
- Tolman, Ehrenfest & Podolsky 1931 (abstract only: "Test rays moving parallel to the pencil or pulse do so with uniform unit velocity");
- Sawyer 2020 (B&O ref. [16]): the coupling factor is "peaked in favor of opposing momenta and vanishing for parallel momenta". He applies it to head-on beams inside the source region, not to a wave far away.

Analogues from other fields: vacuum nonlinearity confined to a laser focus (Fedotov & Narozhny 2007: "almost localized inside the focal region") and γγ opacity suppressed far from a compact source (Granot et al. 2008). No r⁻³ law was verified in either.

**P2: retarded minus advanced, and in-in versus in-out.** The identity behind P2 is standard. Its application to a source-made coherent state reused as an in-state was not found.
- **KMOC 2018/2019**, eq. 6.26, gives F_ret − F_adv = −F_in + F_out. Fitting the boundary conditions "requires subtracting the incoming radiation field which is present in the advanced solution".
- **Cristofoli et al. 2021** show that the coherent-state field built from a source current is ∫J(G_ret − G_adv), with G_adv vanishing only in the far future.
- **Other in-in versus in-out papers:** Caron-Huot et al. 2023, Aoude et al. 2026 (arXiv:2603.17903), Copinger, Ilderton et al. 2024 and Skagerstam et al. 2018. These separate retarded in-in expectation values from time-ordered in-out amplitudes, and show that physical fields from a classical source are retarded.
- **B&O's own ref. [30]** (Ilderton & Seipt 2017) has no hits for "retarded", "advanced", "in-in" or "Pauli".
- **Status.** P2 applies known identities to this case. That application is new as far as these searches reach.

**P1: helicity phases.**
- Haber (Jacob-Wick) establishes that two-particle helicity states carry convention- and azimuth-dependent phases. The phase ξ_λ = (−1)^(s−λ) e^(−2iλφ) is verified.
- Sawyer keeps explicit relative signs in a helicity superposition of graviton beams.
- Kallberg et al. find that the direction of coherent gg ↔ γγ conversion depends on the relative phase of the GW and EM envelopes, in a stimulated, all-plus-polarised classical setting. The cite-check downgraded this to background.
- None of these addresses eq. 6/7, the rephasing invariant, the 0.25-0.60 range or the zero for circular polarisation.
- Choi, Shim & Song 1995 is unrelated: its phase remark concerns a fixed polarisation basis.

**P3 and P6.**
- Dinu et al. 2014 is the only analogue: in QED, idealised infinite-pulse models overestimate finite-pulse signals by up to ten times.
- No gravity or graviton-fusion version, and nothing on Gaussian versus top-hat coefficients, was found.

**Earlier claims of the same channel.** These bear on the novelty of B&O's own claim, not on ours.
- Jones & Singleton 2015 proposed "a 'decay' or attenuation of gravitons, G, into photons, γ, via G + G → γ + γ".
- Jones, McDougall & Singleton 2017 and the Jones et al. 2019 review followed.
- B&O do not cite these, while writing that their semiclassical calculation "was missing in the literature".
- These works predict attenuation in flight, the opposite of P4. The review's phrase "except perhaps close to the source" refers to larger amplitude there, not to a formation length.
- Brandenberger et al. 2022 (parametric resonance) and Chakraborty & Majumdar 2024 are likewise competing production claims.
- Modanese 2017, read for this judgement, is unrelated. It studies single-graviton decay into collinear gravitons or vacuum fluctuations. Verified abstract: "We find that the probability of this decay process is also very small, and compatible with the existence of gravitational waves with very long propagation range."

**Production principle.**
- Redi & Tesi 2026 (B&O ref. [28], new in v2): "Notice that null-like tensor and vector perturbations do not produce particles". Particle production probes the time-like support of the source correlator, while GW emission probes the light-like support.
- Garani, Redi & Tesi 2025 is the earlier general framework.
- Both concern early-universe sources and are consistent with P2 and P4 in spirit only.

## Coverage

**Citation trail**
- **INSPIRE:**
  - `refersto:recid:3183912`, `refersto:arxiv:2607.24930` and fulltext "Gravitational waves decay in vacuum": 0 citers. The recid query was re-run today with the same result.
  - Author searches for Blas and Oller after 2026-08-15 found nothing.
  - Topical abstract and title queries for 2026 found nothing.
  - Citers of Gibbons, Garriga-Verdaguer, Dorca-Verdaguer, Jones et al. (2015, 2017), Sawyer, Kallberg et al., Brandenberger et al. and Fiore-Modanese were checked; none critiques B&O.
- **OpenAlex:** cited_by_count 0.
- **Semantic Scholar:** the search listing shows 0 citations. The citations endpoint returned HTTP 429 in three runs, and again on my retry today.
- **DataCite** (arXiv DOIs, titles and abstracts to 2026-10-26; coverage partial): 14+ queries, and only B&O matched.
- **Crossref:** no journal version.
- **arXiv:** the abstract page and v1/v2 PDFs were read; v3 returns 404. The arXiv search API and `lit_search --source arxiv` timed out or returned 429 in every run, including mine today. So a brand-new arXiv paper not yet indexed by INSPIRE could be missed; INSPIRE can lag by about two weeks.

**Topical literature**
- **Plane-wave QFT:** Gibbons, Deser, Garriga-Verdaguer, Dorca-Verdaguer, Khusnutdinov, Liu, Elder-Fugleberg.
- **Massless kinematics:** Fiore-Modanese, Bonnor, Faraoni-Dumse, Tolman et al.
- **Amplitudes and in-in work:** KMOC, Waveforms from amplitudes, Caron-Huot et al., Aoude et al., Copinger et al., Skagerstam et al., Aoude-Ochirov, Britto et al.
- **Helicity formalism:** Haber, Choi et al.
- **Strong-field QED:** Dinu et al., Fedotov-Narozhny, Bulanov et al., Dunne, Copinger et al.
- **γγ opacity:** Granot et al.
- **Earlier channel claims:** Jones et al., Sawyer, Brandenberger et al., Chakraborty-Majumdar, Modanese.
- **Production frameworks:** Redi-Tesi, Garani-Redi-Tesi, Rahvar, Franchino-Viñas et al.

All 59 searcher items were opened and re-rated by the cite-check run. Its metadata corrections are adopted here:
- hep-ph/0104067 is by F. Gelis;
- Fedotov's paper has two authors;
- the Arza INSPIRE record is 1815671;
- Brandenberger et al. is PDU 40, 101202;
- the Rahvar quote is from v1 only.

**Public channels**
- WebSearch covered news, Reddit, Hacker News, StackExchange, PhysicsForums, Bluesky, Mastodon, X, YouTube, seminar listings and Spanish-language press. It found only the preprint, the Pith review and our own PR.
- alphaXiv has no comments, but it was read only through a paraphrase.
- Unreachable: scirate (403), ResearchGate (403), Google Scholar and ADS. The Pith page was unreadable by `fetch_text.py`.
- Social media is poorly indexed, so absence there is weak evidence.

**Not opened**
- Skobelev 1975 and Tourrenc 1970 (the original gg → γγ papers; no free text);
- Jacob & Wick 1959 (original);
- the full texts of Deser, Garriga-Verdaguer and Dorca-Verdaguer (abstracts only);
- the full Tolman et al. scan (no text layer);
- Bonnor 1970;
- the Landau-Pomeranchuk-Migdal and Ter-Mikaelian formation-length originals;
- the peeling and type-N radiation literature;
- the full Chakraborty-Majumdar and Rahvar papers.

Private channels (referee reports, email) are unseen by nature.

## What this means

What is new:
- **P1:** the rephasing invariant, which independently reproduces here, and the polarisation-dependent coefficients, including 0 for circular polarisation.
- **P2:** applying the standard identity ret − adv = out − in to a source-made coherent state reused as an in-state. It locates B&O's probability at a fictitious focus.
- **P3:** the finite total and the sinc⁴ profile.
- **P4:** the r_min⁻³ yield for a finite spherical wave, and the overcount it implies in S12.
- **P6:** the consequence for the coefficient, 4π in peak rate and 3.76 in total; this re-derives exactly here.

None of these appears in the literature searched, and nobody has commented on B&O at all.

What is not new:
- P4's far-field conclusion for plane waves is Gibbons 1975 and Liu 2007, and B&O already concede it. A write-up should credit them, and Liu especially, since B&O do not cite him. It should present P4 as extending their result to the coherent-state, finite-radius case.
- P5 and P6 should be worded as sharpening caveats B&O half-state, not as hidden errors.

The finding is worth writing up, and worth sending to the authors as a polite technical note. B&O are reachable, and the paper is an unpublished preprint that is still at v2. P1 and P3 are the easiest to check quickly, and P2 is the most consequential.

Two cautions:
1. Our own check is already publicly readable as GitHub PR #16 in EthanDJohnson/Science (merged 13 Oct 2026). It was readable without login, so any PDF given to Ethan Van Winkle should be treated as describing a result that is already public.
2. Any write-up should call B&O an unpublished preprint (v2, 31 Jul 2026), not a published paper.
