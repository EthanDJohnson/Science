# Research: critiques
status: final
Mandate: published objections, comments and replies to Blas & Oller (arXiv:2607.24930), and earlier claims/no-go results on GW -> photon or graviton decay in vacuum; classical-nonlinearity and outgoing-wave arguments.
Access: lit_search INSPIRE ok (arXiv endpoint timed out or rate-limited on several calls); WebSearch ok; fetch_text.py worked on arxiv.org/pdf for 2607.24930, 2508.11558, 2606.28297, 1505.04843. Publisher PDFs (Gibbons 1975, Garriga-Verdaguer 1991, Deser 1975, Dorca-Verdaguer 1993) not reachable free; abstracts only.

Headline finding for this facet: as of 2026-10-13, INSPIRE lists 0 citations of arXiv:2607.24930 (refersto query returned 0 results), and a WebSearch for comments or rebuttals found none. No published objection, erratum or reply to B&O exists in the indexed literature. The objections below are therefore (a) B&O's own stated caveats, (b) the pre-existing no-go and conflicting literature that B&O cite, and (c) closely related 2026 work (Redi & Tesi, Khusnutdinov) that bears on it. Items marked "inference" are this researcher's reading, not a published rebuttal.

## Claims
- [RC-01] CLAIM: No published comment, rebuttal or erratum to B&O (arXiv:2607.24930, v2 is the current version on the abs page) was found. INSPIRE shows 0 citations for it, and `refersto:arxiv:2607.24930` returned 0 results (searched 2026-10-13).
  SOURCE: INSPIRE-HEP record https://inspirehep.net/literature/3183912 (via lit_search.py); fetch_text of https://arxiv.org/abs/2607.24930 shows "this version, v2".
  QUOTE: "Gravitational waves decay in vacuum 2026 | Blas, Diego et al. | preprint (no journal ref) | 0 citations arXiv:2607.24930"
  ACCESS: abstract
  STATUS: preprint
  CONFIDENCE: medium (indexing lag; a search of the days after posting can miss new preprints)

- [RC-02] CLAIM: B&O themselves state that the process is forbidden classically in pure vacuum by the "quadratic coupling of photons", and that semiclassical treatments give no particle production for an individual plane-wave GW, citing Schwinger 1951, Gibbons 1975, Deser 1975, Dunne 2004, Khusnutdinov 2026 and Garriga-Verdaguer 1991 as refs [21-26]. Their claimed effect is therefore explicitly outside the exact-plane-wave no-go results and rests on non-plane (wave-packet, finite-bandwidth) structure.
  SOURCE: Blas & Oller 2026, arXiv:2607.24930 (v2), p. 1, https://arxiv.org/pdf/2607.24930
  QUOTE: "the quadratic coupling of photons forbids it at the classical level from pure vacuum (this is different if one considers decays in a medium). Regarding semiclas- sical calculations, no particle production occurs for an individual plane-wave GW [21–26] (see [27, 28] for other limits where the process exists, and GWs are involved)."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RC-03] CLAIM: B&O claim the effect "admits a semiclassical description once the metric is solved to second order": the amplitude is equivalent to photon creation in the classical background h^c taken at second order, including the metric induced by the GW stress-energy. This is B&O's own statement that the N^2 effect is classical Einstein-Maxwell nonlinearity (hidden premise 10), not a distinctly quantum phenomenon; it also says the result "supersedes previous semiclassical calculations", which is a claim a critic must test against the Gibbons/Deser/Khusnutdinov results (these are for exact plane waves, which have a single null direction and no second-order induced source).
  SOURCE: Blas & Oller 2026, arXiv:2607.24930 (v2), p. 1-2
  QUOTE: "the calculation we will perform is equivalent to that of considering the creation of photons in a back- groundh c, once considered at second order (including in particular the induced metric sourced by the energy- momentum tensor of the GWs, cf. Fig. 1). To the best of our knowledge, this also supersedes previous semiclas- sical calculations."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high (the quotation); the inference about plane waves is mine

- [RC-04] CLAIM: B&O's state is built as a coherent state of the S-matrix of a classical source, hence its classical field is the retarded "radiated field" of the source via the Pauli-Jordan function (their eq. 5), which "far from the source" is an outgoing spherical wave packet h ~ cos(omega_s (r-t))/r * exp(-(r-t)^2 sigma_w^2/2), a burst of duration ~1/sigma_w. B&O take this as an *initial* state ("coherent states as initial states"). This is the exact point at issue in hidden premise 1: the same source operator S acting on |0> as an in-state defines a field that is "outgoing" only when the Pauli-Jordan function is read as retarded; the quote shows B&O describe it as the retarded/outgoing field. A critic must test whether using it as an in-state at t -> -infinity is consistent (inference, not a published objection).
  SOURCE: Blas & Oller 2026, arXiv:2607.24930 (v2), pp. 1-2
  QUOTE: "hc µν =⟨f| ˆhµν|f⟩= √ 8πG Z d4y∆ rad(x−y)µναβTαβ s ,(5) is the classical radiated field by the source, and ∆rad(x− y)µναβ is the Pauli-Jordan function [30, 31]." and "far from the source, the classical field of Eq. (5) tends asymptotically to the outgoing spherical wave packet, hc µν(r−t)∝ cos(ωs(r−t)) r exp  −(r−t) 2σ2 ω/2  ."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high (quotation)

- [RC-05] CLAIM: Gibbons (1975): a quantized massive scalar field in the classical exact plane sandwich gravitational wave of arbitrary profile and polarization has no particle production (the abstract states this for a *massive* scalar). The massless case is the open loophole: Bogolyubov beta can be non-zero for exactly collinear massless modes. Scope: exact plane wave of infinite transverse extent; a classical c-number background; no back-reaction.
  SOURCE: G. W. Gibbons, 1975, Quantized Fields Propagating in Plane Wave Space-Times, Commun. Math. Phys. 45, 191, doi:10.1007/BF01629249
  QUOTE: "This paper contains an account of the interaction of a quantized massive scalar field with the classicalc number gravitational field of a plane sandwich wave of arbitrary profile and polarization. It is shown that the time varying gravitational field of the wave produces no particles and the Feynman propagator for the problem is calculated exactly."
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RC-06] CLAIM: Conflicting results on massless fields in an exact plane GW (a live, unresolved literature conflict, relevant because B&O's coherent-state process lies in the non-plane regime that this conflict does not decide): the Green-function / DeWitt-Schwinger approach gives no massless particle production, while the Bogolyubov-coefficient approach (Garriga-Verdaguer 1991; Dorca-Verdaguer 1993) gives beta ~ delta(k_v + l_v) non-zero for exactly collinear massless quanta, a flux aligned with the GW. Khusnutdinov (Eur. Phys. J. Plus 141, 532, 2026) computes massless vector and scalar Green's functions three ways and finds no production, and says the tension is unresolved.
  SOURCE: N. Khusnutdinov 2026, Quest for particles production in the plane gravitational wave spacetime, EPJ Plus 141, 532, arXiv:2508.11558, https://arxiv.org/pdf/2508.11558
  QUOTE: "The results coincide exactly with the DeWitt–Schwinger expansion, indicating no massless particles production in this background. Contrasting interpretations, based on Bogolyubov coefficient calculations predicting massless particle creation, are also addressed." and "This results in an apparent contradiction between the two approaches to particle production calculations. The standard method based on the Green-function formalism [8] predicts no particle creation, whereas the Bogolyubov approach suggests a flux of photons in the direction of the GW . The aim of this paper is to draw the attention of the physics community to this unresolved issue."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RC-07] CLAIM: Source of the collinear loophole: Garriga-Verdaguer's Bogolyubov beta is proportional to a delta function in the light-cone momentum, which vanishes for massive quanta (k_v + l_v > 0) but can vanish for massless ones. So the non-zero massless beta is a statement about exactly parallel momenta; it is a measure-zero set for wave packets of finite angular spread and, in a 1 -> 2 reading, matches the kinematic rule that massless decays are collinear-only (brief, Known constraints). This bears on Q3.
  SOURCE: Khusnutdinov 2026, arXiv:2508.11558, p. 2
  QUOTE: "For massive par- ticles,k v +l v >0, ensuringβ=0; for massless particles, the sum can vanish, allowingβ̸=0."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RC-08] CLAIM: Garriga-Verdaguer (1991): for exact gravitational plane waves, quantum scattering cross sections equal classical geodesic ones; the expectation value of the scalar-field stress tensor between scattering states diverges where classical geodesics focus. Scope: scalar test field on a fixed plane-wave background, so it is a no-go for test fields, not for second-order back-reaction of fields on GW.
  SOURCE: J. Garriga and E. Verdaguer 1991, Scattering of quantum particles by gravitational plane waves, Phys. Rev. D 43, 391, doi:10.1103/PhysRevD.43.391
  QUOTE: "We consider the coupling of quantum massless and massive scalar particles with exact gravitational plane waves. The cross section for scattering of the quantum particles by the waves is shown to coincide with the classical cross section for scattering of geodesics. The expectation value of the scalar field stress tensor between scattering states diverges at the points where classical test particl"
  ACCESS: abstract (truncated by lit_search output)
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RC-09] CLAIM: Where particle production by gravitational waves does exist, it needs two (or more) crossing waves, not one: Dorca & Verdaguer (1993) quantize a scalar field on the head-on collision of two gravitational plane waves, where the waves focus into a non-singular Killing-Cauchy horizon and the interaction region is locally isometric to the interior of a Schwarzschild black hole. B&O cite this as a case where the process exists. It is a strong-field (focusing) case, not a weak-field freely propagating wave.
  SOURCE: M. Dorca and E. Verdaguer 1993, Quantum fields interacting with colliding plane waves: particle creation, Nucl. Phys. B 403, 770, doi:10.1016/0550-3213(93)90370-5
  QUOTE: "The quantization of a scalar field on a spacetime representing the head on collision of two gravitational plane waves is studied. In the spacetime considered the waves focus into a non-singular Killing-Cauchy horizon. The interaction region of the waves is locally isometric to a region inside the event horizon of a Schwarzschild black hole with the Killing-Cauchy horizon corresponding to the even"
  ACCESS: abstract (truncated by lit_search output)
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RC-10] CLAIM: Redi & Tesi (2026, posted a month before B&O and cited by it as ref [28]) give a general "particle yield from metric perturbations" formula: yield is controlled by the unequal-time stress-energy correlator on its *time-like* support, and "null-like tensor and vector perturbations do not produce particles". The same object on the *light-like* support gives GW emission. This is the cleanest published statement of the structure behind the Q2/Q3 objection: an on-shell (null-supported) GW does not by itself make particles at the order they work (linear in the metric perturbation squared in the stress tensor); production needs off-shell, time-like support, e.g. near a time-dependent source. Scope: their setting is early-Universe sub-horizon inhomogeneities (production at first order in the perturbation's two-point function), not B&O's second-order coherent-state fusion; applying it to B&O is an inference.
  SOURCE: M. Redi and A. Tesi 2026, Particle Production from Inhomogeneities: the off-shell side of gravitational waves, arXiv:2606.28297, https://arxiv.org/pdf/2606.28297
  QUOTE: "The resulting particle yield probes the time-like support of this correlator, and in the tensor case the same object con- trols gravitational-wave emission when evaluated on the light-like support." and "Notice that null-like tensor and vector perturbations do not produce particles."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium (quotes verbatim; applying them to B&O's second-order process is an inference)

- [RC-11] CLAIM: Earlier vacuum-attenuation claim that conflicts in size with B&O: Jones & Singleton (2015 Gravity Research Foundation essay, IJMPD 24, 1544017) propose, from an Unruh-DeWitt detector response to a GW background, a "decay" G+G -> gamma gamma or G -> gamma gamma G, and estimate a mean decay length of ~1e11 m (10^-5 light-year) for a solar-mass-scale source at omega ~ 1e2 s^-1, with Gamma = xi_0^2 omega^4 r /(32 c^3) growing linearly with r, so that "detecting gravitational waves at large distances may be hard or impossible". This is far stronger than B&O's G^2 N^2 result (B&O's binary photon luminosities are tiny in comparison) and, if right, would already contradict the observation of GW150914 at ~410 Mpc. B&O do not cite it. It is an essay with a detector-response (not S-matrix) derivation; classify as weakly supported.
  SOURCE: P. Jones and D. Singleton 2015, Gravitons to Photons - attenuation of gravitational waves, Int. J. Mod. Phys. D 24, 1544017, arXiv:1505.04843, https://arxiv.org/pdf/1505.04843
  QUOTE: "the approximate mean decay length would be ⟨r⟩ ∼ 1011m = 10 − 5ly." and "The UD detector calcula tion, followed by the mean free path estimate given above, indicates that detecting gra vitational waves at large distances may be hard or impossible due to the attenuation of the gr avitational wave coming from the conversion of gravitons to photons."
  ACCESS: full-text
  STATUS: peer-reviewed (essay); weakly supported
  CONFIDENCE: medium (that this is their claim: high; the GW150914 comparison is an inference)

- [RC-12] CLAIM: Related Jones-Singleton line (g+g -> gamma+gamma as the motivation for a rate of massless-scalar creation in a *linear plane-wave* background) was published in Phys. Rev. D 95, 065010 (2017), 31 citations. It treats the process via a perturbative plane-wave background, i.e. the Gibbons/Deser regime in which production vanishes for the exact solution, so its non-zero rate is an artefact or a different regime; the 2024 PRD Letter by Chakraborty et al. also reports perturbative scalar production in a linear GW background. These are conflicting results on the same question and are not cited as critiques by B&O. Marking as "conflicting, unreconciled".
  SOURCE: P. Jones, D. Singleton et al. 2017, Particle production in a gravitational wave background, Phys. Rev. D 95, 065010, arXiv:1610.02973; T. Chakraborty et al. 2024, Particle creation in a linear gravitational wave background, Phys. Rev. D 110, L021701, arXiv:2404.01840
  QUOTE: "We study the possibility that massless particles, such as photons, are produced by a gravitational wave. That such a process should occur is implied by tree-level Feynman diagrams such as two gravitons turning into two photons, i.e., g+g→γ+γ. Here we calculate the rate at which a gravitational wave creates a massless scalar field." (Jones et al.) and "we show that scalar particles may indeed be produced in a perturbative manner." (Chakraborty et al.)
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: medium (I did not read either full text; whether their perturbative production survives the Gibbons/Khusnutdinov no-go is not checked)

- [RC-13] CLAIM: Gertsenshtein (graviton-photon conversion) needs an external field and is not vacuum decay: all current literature treats it as GW -> single photon in a background magnetic field B, a 1 -> 1 process, with conversion probability scaling as (B L)^2 G and quenched by plasma (effective photon mass) above ~1 PeV in the Galactic field. Used by the inverse-Gertsenshtein papers to constrain high-frequency GWs. It is a different, B-field-dependent channel and gives no precedent for vacuum decay into photon pairs.
  SOURCE: S. Ramazanov et al. 2023, Shimmering gravitons in the gamma-ray sky, JCAP 06 (2023) 019, arXiv:2304.11222; A. Palessandro 2024, Graviton-photon oscillations as a probe of quantum gravity, CQG 41, 215011, arXiv:2405.01407
  QUOTE: "We address this question by studying graviton-to-photon conversion — the inverse-Gertsenshtein effect — in the magnetic field of the Milky Way. We find that above ∼ 1 PeV the effective photon mass grows large enough to quench the conversion rate." (Ramazanov et al.) and "The Gertsenshtein effect could in principle be used to detect a single graviton by firing it through a region filled with a constant magnetic field that enables its conversion to a photon" (Palessandro)
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RC-14] CLAIM: B&O's own caveats about their approximation: they drop terms involving a-dagger a "because of energy conservation in the narrow-band limit sigma_w/omega_s << 1". So the headline eq. 8 holds only for narrow-band packets; the 1/sigma_w ~ burst-duration dependence arises exactly where narrow-band (long-burst) and finite-time (short-burst) pictures meet, the regime hidden premises 3 and 6 target. Whether the narrow-band limit survives for a merger chirp (fractional bandwidth ~ O(1)) is a point a critic must test (B&O address this by binning, premise 6).
  SOURCE: Blas & Oller 2026, arXiv:2607.24930 (v2), p. 2 (footnote 2)
  QUOTE: "When sandwiched between the coherent states, other contribu- tions involvinga†aare suppressed because of energy conservation in the narrow-band limitσ ω/ωs ≪1."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RC-15] CLAIM: B&O frame the process as requiring N^2 coherence and say a classical description is "arguably generically sufficient" for observable sources, while claiming the quantum calculation is "absolutely necessary" to see the small M_P^-2 beaten. That sits in tension with their own "semiclassical description": if the same rate follows from the classical Einstein-Maxwell second-order equations (their eq. 5 plus the induced metric), then ħ cancels in the pair *energy*, and "decay" of a quantum state versus classical energy transfer is a matter of description (hidden premise 10). Inference: classical second-order GR + Maxwell gives a radiated EM field sourced by h x h products, so the physical content is the classical EM wave sourced by two GWs, which in vacuum is generated only where the product of the two fields is non-null (not along a single null ray).
  SOURCE: Blas & Oller 2026, arXiv:2607.24930 (v2), p. 1
  QUOTE: "Given the large occupation numbers of the states emitted by most observable sources [17, 18], it is arguable that a classical description is generically sufficient." and "we show that the effect admits a semiclassical description once the metric is solved to second order."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium (quotes high; the classical-nonlinearity reading is mine)

## Gaps
- No comment, reply or erratum to B&O found (INSPIRE citations 0 as of 2026-10-13; WebSearch found none). Re-check INSPIRE `refersto:arxiv:2607.24930` just before the report.
- Deser 1975 (J. Phys. A 8, 1972), "Plane waves do not polarize the vacuum": INSPIRE returned no matching record; no abstract seen. Relied on B&O's citation only. PAPER TO REQUEST: doi:10.1088/0305-4470/8/12/012 | Deser, Plane waves do not polarize the vacuum | exact scope of the no-go (photon-photon/graviton propagator corrections on a plane-wave background) and whether it covers Einstein-Maxwell second-order sourcing.
- Full texts of Gibbons 1975, Garriga-Verdaguer 1991, Dorca-Verdaguer 1993 not reachable free; only abstracts quoted. PAPER TO REQUEST: doi:10.1103/PhysRevD.43.391 | Scattering of quantum particles by gravitational plane waves | the explicit statement of beta for massless modes and the collinearity condition.
- Not found: any explicit published argument that coherent-state "decay" of an outgoing wave vanishes beyond r ~ lambda, or that 2 pi delta(0) -> T is invalid (these are the theory/idealizer/dialectician calculations in this run, not literature).
- Not found: published classical Einstein-Maxwell second-order calculation of photon radiation by two crossing GWs (Gertsenshtein-style, no background B). Searches "photon production gravitational wave collision Einstein-Maxwell" returned nothing in INSPIRE.
- arXiv API was rate-limited or timed out on several lit_search calls; INSPIRE covered the same papers.
