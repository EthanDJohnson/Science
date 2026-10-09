# Research: theory
status: final
Mandate: governing theory and established results (equations, theorems, proven vs. conjectured, standard references) for traversable wormholes, energy conditions (ANEC / achronal ANEC), chronology protection, and the post-2016 constructions.
Access: lit_search INSPIRE ok, arXiv rate-limited (HTTP 429) on several queries; fetch_text on arxiv.org/pdf ok for all arXiv papers cited; Morris-Thorne 1988 PDF extraction failed (image PDF); WebFetch not used (WebSearch only for Konoplya-Zhidenko and Morris-Thorne leads)

## Claims
- [RT-01] CLAIM: Self-consistent achronal ANEC (Graham & Olum 2007) is stated as a CONJECTURE: no self-consistent semiclassical solution violates ANEC on a complete achronal null geodesic. Plain ANEC is violated by quantum fields (compactified Minkowski, Schwarzschild); the achronal version has no known violations and is claimed sufficient to rule out CTCs and wormholes connecting different asymptotically flat regions. Not proven in general (only suggested via a tube-of-flat-space argument for minimally coupled scalar).
  SOURCE: Graham & Olum 2007, "Achronal averaged null energy condition", Phys. Rev. D 76, 064001, https://arxiv.org/pdf/0705.3193
  QUOTE: "Condition 1 (self-consistent achronal ANEC) There is no self-consistent solution in semiclassical gravity in which ANEC is violated on a complete, achronal null geodesic. We conjecture that all semiclassical systems obey self-consistent achronal ANEC."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-02] CLAIM: Graham-Olum's rationale: a proof for achronal geodesics is expected by extending the flat-tube argument; the 1+1D massless scalar case was proved by Wald and Yurtsever; the proof for a general spacetime is explicitly left to future work (as of 2007).
  SOURCE: Graham & Olum 2007, https://arxiv.org/pdf/0705.3193
  QUOTE: "We expect that any spacetime could be slightly deformed in the vicinity of a given geodesic to produce the necessary tube, so that self-consistent achronal ANEC could be proved along similar lines, but such a proof will have to await future work."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-03] CLAIM: Hochberg & Visser: NEC is generically violated at or near the 2D throat surface of a traversable wormhole (flare-out condition generalised beyond spherical symmetry, dynamic wormholes); complementary to topological censorship, which only guarantees ANEC violation along SOME null geodesics. Frame caveat: with Brans-Dicke-type decompositions, violations can be hidden in the scalar sector but the total NEC violation is frame independent.
  SOURCE: Hochberg & Visser, "Generic wormhole throats" (arXiv:gr-qc/9710001, Haifa workshop proceedings; this is NOT the PRL). The peer-reviewed dynamic-wormhole paper is Hochberg & Visser 1998, "The Null energy condition in dynamic wormholes", Phys. Rev. Lett. 81, 746, arXiv:gr-qc/9802048 (the companion PRD 58, 044021 is gr-qc/9802046), https://arxiv.org/pdf/gr-qc/9710001
  QUOTE: "the null energy condition (NEC) is generically violated at some points on or near the two-dimensional surface comprising the wormhole throat." ; "The topological censorship theorem tells us that in a spacetime containing a traversable wormhole the averaged null energy condition must be violated along at least some (not all) null geodesics" ; (PRL abstract, gr-qc/9802048, re-fetched) "We extend previous proofs that violations of the null energy condition (NEC) are a generic and universal feature of traversable wormholes to completely non-symmetric time-dependent wormholes. We show that the analysis can be phrased purely in terms of local geometry at and near the wormhole throat, and do not have to make any technical assumptions about asymptotic flatness or other global properties"
  ACCESS: full-text
  STATUS: peer-reviewed (the PRL; the proceedings quote is from a conference paper). Corrected after source check: journal ref was wrong.
  CONFIDENCE: high
- [RT-04] CLAIM: Gao-Jafferis-Wall (2016): in AdS (eternal BTZ, 2+1D bulk) a boundary coupling between the two CFTs yields a one-loop quantum stress tensor with NEGATIVE AVERAGED null energy; its backreaction makes the Einstein-Rosen bridge traversable. Two-sided, no shared ambient space; the authors state it cannot be used to violate causality. ANEC violation is a prerequisite for traversability.
  SOURCE: Gao, Jafferis & Wall 2017, "Traversable Wormholes via a Double Trace Deformation", JHEP 12 (2017) 151, https://arxiv.org/pdf/1608.05687
  QUOTE: "After turning on an interaction that couples the two boundaries of an eternal BTZ black hole, we find a quantum matter stress tensor with negative average null energy, whose gravitational backreaction renders the Einstein-Rosen bridge traversable. ... However, it cannot be used to violate causality."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-05] CLAIM: GJW consistency with AdS/CFT: no signal can pass through the bulk in the decoupled system; the averaged null energy at linear order is i*eps*<[∫dU T_UU, A]> and vanishes for the TFD state because TFD is invariant under H_R - H_L; traversability requires the double-trace coupling (the boundary coupling is the non-gravitational channel).
  SOURCE: Gao, Jafferis & Wall 2017, https://arxiv.org/pdf/1608.05687
  QUOTE: "in the decoupled system, no operator on the left can influence the right, which implies that no signal can be transmitted between the boundaries through the bulk."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-06] CLAIM: Maldacena-Milekhin-Popov (MMP): 4D Einstein-Maxwell plus charged massless fermions; two oppositely (magnetically) charged near-extremal black holes joined by a LONG wormhole whose throat is supported by negative Casimir-like energy of the fermions in the lowest Landau level along magnetic field lines. ANEC is violated along null lines wrapping the field-line circle, but those null lines are NOT achronal. The authors say it does not lead to causality violations in the ambient space. Caveat noted by authors: in the covering space it would join different universes and the wormhole would be short, "should be forbidden by causality"; the solution depends on actual topology so cannot go to covering space.
  SOURCE: Maldacena, Milekhin & Popov 2018/2023, "Traversable wormholes in four dimensions", Class. Quantum Grav. 40, 155016, https://arxiv.org/pdf/1807.04726
  QUOTE: "The vacuum stress tensor develops a negative null-null component leading to a violation of the average null energy condition along the null lines wrapping around the cylinder. Of course, these null lines are not achronal, see figure 2." ; "It is a long wormhole that does not lead to causality violations in the ambient space."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-07] CLAIM: MMP energy minimisation: total energy (relative to two extremal BHs) E = r_e^3/(G_N l^2) - q/(8 l) (Casimir term), minimised at l = 16 r_e^3/(G_N q) with E_min = -G_N q^2 /(256 r_e^3) (units as in paper, G_N, l_p conventions; hbar=c=1 natural units); the throat length is fixed by Einstein equations and the geometry is smooth despite epsilon below extremality bound.
  SOURCE: Maldacena, Milekhin & Popov, https://arxiv.org/pdf/1807.04726 (eqs 5.30-5.31)
  QUOTE: "We now set the value of l by minimizing this, and we get l = 16 r_e^3/(G_N q) ... E_min = -G_N q^2/(256 r_e^3)" (extraction garbled in the PDF text; recompute/verify from the equation before use)
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: low (extraction garbled)
- [RT-08] CLAIM: Maldacena-Qi (2018): nearly-AdS2 (JT) eternal traversable wormhole supported by negative null energy of quantum fields (large N number of fields needed for control) under an external coupling between two boundaries (or two coupled SYK systems). Derivation of the ANEC requirement is the 2D special case of topological censorship: the integrated null energy ∫dX+ T_{X+X+} = -2 phi_r must be negative because the dilaton grows toward both boundaries (-(sin^2σ ∂+φ)|_{-inf}^{+inf} = ∫ T). A finite amount of negative energy suffices. Two-sided, 2D, AdS.
  SOURCE: Maldacena & Qi 2018, "Eternal traversable wormhole", arXiv:1804.00491 (not yet verified as published; check journal ref), https://arxiv.org/pdf/1804.00491
  QUOTE: "We construct a nearly-AdS2 solution describing an eternal traversable wormhole. The solution contains negative null energy generated by quantum fields under the influence of an external coupling between the two boundaries." ; "This problem is a special case of the general topological censorship result [24, 25] that forbids"
  ACCESS: full-text
  STATUS: preprint (published in 2018? unverified; arXiv only confirmed)
  CONFIDENCE: high for the quoted content
- [RT-09] CLAIM: Fu-Grado-White-Marolf 2018: perturbative framework showing Z2-quotient wormholes (globally hyperbolic quotients of spacetimes with bifurcate Killing horizons) become traversable by first-order back-reaction of quantum fields in Hartle-Hawking-type states, with the traversal time tf growing as extremality is approached, suggesting a non-perturbative self-supporting eternal wormhole; works with few quantum fields, unlike Maldacena-Qi's large-N. The key quantity ∫dU<T_kk> along non-contractible cycles is negative (Casimir-like) but the wormhole needs non-contractible cycles, i.e. orbifold/quotient topology.
  SOURCE: Fu, Grado-White & Marolf 2018, "A perturbative perspective on self-supporting wormholes", arXiv:1807.07917 (CQG 36, 045006 -- unverified), https://arxiv.org/pdf/1807.07917
  QUOTE: "our perturbative analysis indicates the back-reacted wormhole remains traversable at later and later times as this limit is approached. This suggests that a fully non-perturbative treatment would find a self-supporting eternal traversable wormhole."
  ACCESS: full-text
  STATUS: preprint/peer-reviewed (journal ref unverified)
  CONFIDENCE: high for quote
- [RT-10] CLAIM: Fu-Grado-White-Marolf 2019: asymptotically flat 4D (zero cosmological constant) pair of oppositely charged black holes with perturbative back-reaction of bulk quantum fields in Hartle-Hawking states; at finite temperature wormhole becomes traversable for appropriately timed signals with minimum transit time t_transit = d + (log terms) for mouth separation d (c=1), i.e. at best matches, not beats, the exterior light-travel time d, and is shorter than MMP's eternally traversable wormhole by more than a factor of 2. Traversability exponentially fragile (destroyed by exponentially small perturbations); background unstable (BHs merge on ~d^{3/2}).
  SOURCE: Fu, Grado-White & Marolf 2019, "Traversable Asymptotically Flat Wormholes with Short Transit Times", Class. Quantum Grav. 36, 245018, https://arxiv.org/pdf/1908.03273
  QUOTE: "a wormhole with mouths separated by a distance d becomes traversable with a minimum transit time tmin transit = d + logs. Thus tmin transit/d is smaller than for the eternally traversable MMP wormholes by more than a factor of 2, and approaches the value that, at least in higher dimensions, would be the theoretical minimum."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-11] CLAIM: FGM 2019 explicitly cites the prohibition (Gao-Wald / Graham-Olum / Galloway et al.) against wormholes providing the fastest causal curves between distant points: for d to infinity the transit time approaches the minimum consistent with that prohibition (no true shortcut; d + logs), with "time delay" defined relative to Minkowski propagation across d.
  SOURCE: Fu, Grado-White & Marolf 2019, https://arxiv.org/pdf/1908.03273
  QUOTE: "the minimum transit time consistent with the above-mentioned prohibition against wormholes providing the fastest causal curves between distant points [8, 9]. However, in such cases traversability is exponentially fragile, and can be destroyed by exponentially small perturbations."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-12] CLAIM: Maldacena-Milekhin 2020 "Humanly traversable wormholes": claims humanly traversable wormhole solutions exist in a Randall-Sundrum II braneworld (beyond-Standard-Model, SPECULATIVE extra dimension); traveller subject to tidal forces like falling into an extremal BH, a ~ size/r_e^2 with r_e the throat/BH scale.
  SOURCE: Maldacena & Milekhin 2021, "Humanly traversable wormholes", Phys. Rev. D 103, 066007, https://arxiv.org/pdf/2008.06618
  QUOTE: "We point out that there can be humanly traversable wormhole solutions in some previously considered theories for physics beyond the Standard Model, namely the Randall-Sundrum model." ; "the tidal acceleration felt by the observer would be roughly a∼ (size)/r_e^2"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-13] CLAIM: Maldacena-Milekhin 2020 tidal requirement: with tolerable tidal acceleration ~20 g (g=9.8 m/s^2) for short durations and traveller size ~0.5 m, a ~ size/r_e^2 gives r_e > 1.5e7 m (light-crossing ~0.05 s) (SI). With a spaceship of ~1e3 kg and requirement |E_bin| > 1e3 kg they find N_f > 1e52 species in the free-fermion model, vs a bound N_f < M_pl^2/TeV^2 ~ 1e32 (Bekenstein-like) -> the simple 4D free-fermion MMP model cannot be humanly traversable; they therefore go to a strongly coupled / holographic (Randall-Sundrum II, speculative) matter sector.
  SOURCE: Maldacena & Milekhin 2021, Phys. Rev. D 103, 066007, https://arxiv.org/pdf/2008.06618
  QUOTE: "we need re > 10^7 m. If we further assume that the mass of the spaceship is about 10^3 kg, we also need the condition |Ebin|> 10^3 kg. This then implies that re|Ebin|∝ Nf(g^2 Nf)> 10^7 m× 10^3 kg → Nf > 10^52 (2.16) This value of Nf is too large if we want the UV cutoff of the local field theory to be above the TeV scale, since we expect that Nf < M_pl^2/(TeV)^2 ~ 10^32"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-14] CLAIM: Maldacena-Milekhin human-traversability criterion: tidal acceleration a ~ size/r_e^2 < ~20 g for short durations, giving r_e > 1.5e7 m for 0.5 m size. (Morris-Thorne's own criterion is Earth gravity ~1 g; MM use a much looser 20 g. To verify against MT 1988 separately.)
  SOURCE: Maldacena & Milekhin 2021, https://arxiv.org/pdf/2008.06618
  QUOTE: "20g >a∼ size/r_e^2 → re > 1.5×10^7 m∼.05s (3.26) where we assumed that the size is about 0.5m."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-15] CLAIM: Gao-Wald (2000) time-delay theorem: in a null-geodesically-complete spacetime satisfying the (pointwise) NEC and null generic condition, for any compact K there is a compact K' such that a fastest null geodesic between two points outside K' cannot enter K -> no "time advance" through a compact region (suggestive of no wormhole shortcut), in any dimension; but theorem gives no control over the size of K' and the authors say a strong "no time advance" interpretation is hard to argue. It assumes pointwise NEC, which wormholes violate; its quantum/ANEC extension is what Graham-Olum and FGM refer to.
  SOURCE: Gao & Wald 2000, "Theorems on gravitational time delay and related issues", Class. Quantum Grav. 17, 4999, https://arxiv.org/pdf/gr-qc/0007021
  QUOTE: "Thus, the theorem suggests that “time advance” is not possible, although it is difficult to make a strong argument for this interpretation, since the theorem gives little control over the size of the region K′." ; (p. 10, discussion) "However, since K ′ could be far larger than K, it is difficult to make a strong argument for this kind of interpretation of the theorem." ; (Theorem 1 hypotheses) "Let (M, gab) be a null geodesically complete spacetime satisfying the null energy condition (2) and the null generic condition (see eq.(9))." ; "our results hold in any spacetime dimension."
  NOTE: re-fetched this run; the earlier version's "K' far larger" sentence was labelled a quote but the p. 5 wording differs; both sentences are now verbatim (p. 5 and p. 10). Check file flagged this as non-verbatim.
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
  PRIOR: 2026-10-01-warp-drive-without-negative-energy (2026-10-01), was RT-06; re-verified (Theorem 1 hypotheses and the K' caveat both re-fetched)
- [RT-16] CLAIM: Blazquez-Salcedo-Knoll-Radu (BKR 2021): asymptotically flat, spherically symmetric, singularity-free traversable wormholes in 4D Einstein-Dirac-Maxwell with two gauged massive fermions in a singlet spinor state; Dirac matter treated as a quantum WAVE FUNCTION (not a quantum field), semiclassical; smoothness requires total electric charge and traversability needs mass/charge ratio < 1; claims "without needing any form of exotic matter". Their Fig.1 shows a "thin layer energy density at the throat" epsilon_T, i.e. throat energy density is part of the analysis; no ANEC integral reported (to verify).
  SOURCE: Blazquez-Salcedo, Knoll & Radu 2021, "Traversable wormholes in Einstein-Dirac-Maxwell theory", Phys. Rev. Lett. 126, 101102, https://arxiv.org/pdf/2010.07317
  QUOTE: "We construct a specific example of a class of traversable wormholes in Einstein-Dirac-Maxwell theory in four spacetime dimensions, without needing any form of exotic matter." ; "In our approach, the Dirac matter is described by a quantum wave function rather than a quantum field."
  ACCESS: full-text
  STATUS: peer-reviewed (PRL ref unverified in fetched text)
  CONFIDENCE: high for quotes
- [RT-17] CLAIM (secondary): Konoplya & Zhidenko, PRL 128, 091104 (2022), "Traversable Wormholes in General Relativity", presented asymmetric Einstein-Dirac-Maxwell wormholes; Kain (2023, arXiv:2305.11217) argued from numerical evolution that EDM wormholes are not traversable (black holes form). Wording from search summary only; fetch required.
  SOURCE: web search results, https://arxiv.org/abs/2206.12250 (comment) ; https://arxiv.org/pdf/2305.11217
  SUMMARY: "numerical evolution of the static solutions forward in time indicates that black holes form that are connected by the wormhole, leading to the conclusion that Einstein-Dirac-Maxwell wormholes are not traversable"
  ACCESS: search-summary
  STATUS: secondary
  CONFIDENCE: low
- [RT-18] CLAIM: Kain 2023 (arXiv:2305.11217): numerical evolution of static asymmetric Einstein-Dirac-Maxwell (EDM) wormholes: the lapse collapses, black holes form around the throat, and null geodesics that cross the throat are trapped inside a black hole; conclusion "EDM wormholes are not traversable" (while noting the author cannot rule out some other asymmetric EDM wormhole behaving differently). Kain stresses NEC violation is insufficient to establish traversability. Static solutions are, however, regular and asymptotically flat and use no phantom field.
  SOURCE: Kain 2023, "Are Einstein-Dirac-Maxwell wormholes traversable?", arXiv:2305.11217 (journal ref unverified), https://arxiv.org/pdf/2305.11217
  QUOTE: "Although there exist null geodesics that travel through the wormhole, we find that they are trapped inside a black hole and are unable to travel arbitrarily far away. We conclude that Einstein-Dirac-Maxwell wormholes are not traversable." ; "An important takeaway is that violation of the null energy condition is an insufficient condition for determining if a static wormhole solution is traversable."
  ACCESS: full-text
  STATUS: preprint (published version unverified)
  CONFIDENCE: high for quote; stability conclusion is numerical, limited to simulated parameter sets
- [RT-19] CLAIM: Critique of BKR's "no exotic matter" language (Bolokhov, Bronnikov, Krasnikov, Skvortsova 2021): by the standard definition (exotic = violates the NEC) exotic matter is unavoidable at any throat, so the Dirac fields BECOME exotic matter; also notes that nu'(0) != 0 only requires non-Z2-symmetric configuration, not a thin shell; also cites Danielson et al. who argue BKR's solution fails junction/matching conditions for Maxwell and Dirac fields.
  SOURCE: Bolokhov, Bronnikov, Krasnikov & Skvortsova 2021, "A Note on 'Traversable Wormholes in Einstein-Dirac-Maxwell Theory'", Grav. Cosmol. 27, 401, https://arxiv.org/pdf/2104.10933
  QUOTE: "The words in the abstract, that the wormhole solutions are obtained "without needing any form of exotic matter," look misleading since exotic matter (by definition, matter violating the Null Energy Condition) is quite necessary at a wormhole throat [4]. It would be better to say that Dirac spinor fields become exotic matter under certain circumstances."
  ACCESS: full-text
  STATUS: peer-reviewed (Grav. Cosmol.; short note)
  CONFIDENCE: high
- [RT-20] CLAIM: Konoplya-Zhidenko (PRL 128, 091104, 2022; arXiv:2106.05034) constructed asymmetric (non-Z2) wormholes from smooth gravitational plus charged Dirac fields in EDM; a comment (arXiv:2206.12250) says their imposed throat condition N'(0)=0 is unnecessary and that solutions are ground/excited states labelled by Dirac field nodes. Does not itself address time-dependent stability.
  SOURCE: Comment on "Traversable Wormholes in General Relativity" (arXiv:2206.12250), https://arxiv.org/pdf/2206.12250
  QUOTE: "R. A. Konoplya and A. Zhidenko have constructed an asymmetric wormhole solution, which is not symmetric about the throat and is compounded from smooth gravitational and charged Dirac fields."
  ACCESS: full-text
  STATUS: preprint (comment)
  CONFIDENCE: high
- [RT-21] CLAIM: Wall (2010) PROVED (under stated auxiliary assumptions: CPT, existence of a suitable renormalisation scheme for generalised entropy, GSL for causal horizons, extra-strong cosmic censorship, horizons persisting under perturbation) that for quantum fields minimally coupled to semiclassical Einstein gravity ANEC holds on null lines (complete achronal null geodesics). Given ANEC on null lines, theorems exist for positivity of energy, topological censorship and no CTCs. Caveat: theorems fail once the linearised graviton field is quantised (renormalised shear squared violates).
  SOURCE: Wall 2010, "Proving the Achronal Averaged Null Energy Condition from the Generalized Second Law", Phys. Rev. D 81, 024038, https://arxiv.org/pdf/0910.5751
  QUOTE: "It is proven that for any quantum fields minimally coupled to semiclassical Einstein gravity, the averaged null energy condition (ANEC) on null lines is a consequence of the generalized second law of thermodynamics for causal horizons. Auxiliary assumptions include CPT and the existence of a suitable renormalization scheme for the generalized entropy."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-22] CLAIM: Wall's text records the status of the achronal ANEC: proved by Wald & Yurtsever for minimally coupled free scalars in curved 2D, or in 4D with bifurcate Killing horizon; Graham & Olum proposed it for all semiclassically self-consistent spacetimes and showed it suffices for a topological-censorship theorem ruling out traversable wormholes (connecting asymptotic regions) and no-CTC theorems.
  SOURCE: Wall 2010, https://arxiv.org/pdf/0910.5751
  QUOTE: "This version of ANEC has been proven by Wald and Yurtsever [12] in the case of minimally coupled free scalar fields, either on a curved two-dimensional spacetime, or on a four-dimensional spacetime with a bifurcate Killing horizon."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-23] CLAIM: ANEC in flat-space QFT: Faulkner-Leigh-Parrikar-Wang (2016) gave a general argument from monotonicity of relative entropy (assuming relevant quantities well defined in the continuum limit; not a fully rigorous proof for all QFTs); Hartman-Kundu-Tajdini (2017) derived it from causality for any unitary Lorentz-invariant QFT with an interacting UV conformal fixed point. Both are for Minkowski space (and static bifurcate Killing horizons for FLPW), NOT for general curved spacetime. Hartman et al: ANEC has no known counterexamples in consistent QFT assuming the null geodesic is achronal.
  SOURCE: Hartman, Kundu & Tajdini 2017, "Averaged Null Energy Condition from Causality", JHEP 07 (2017) 066, https://arxiv.org/pdf/1610.05308 ; Faulkner, Leigh, Parrikar & Wang 2016, JHEP 09 038, https://arxiv.org/pdf/1605.08072
  QUOTE: "the ANEC has no known counterexamples in consistent quantum field theories (assuming also that the null geodesic is achronal [7])" (Hartman et al.) ; "In summary, there is substantial evidence so far to suggest that the ANEC is satisfied by generic quantum field theories on Minkowski space-time, but a general proof has been missing hitherto" (Faulkner et al.)
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-24] CLAIM: Kontou-Sanders 2020 review: all pointwise energy conditions are violated by essentially any QFT; the achronal ANEC (AANEC) "comes closest to being generally valid"; proofs: 2D Minkowski for all fields with a mass gap, higher-D Minkowski partial; validity in curved spacetime remains an open question that they list as of interest. They list ways ANEC-violating counterexamples fail (equations of motion/Einstein equation violated, wrong-sign effective G, or Planck-scale transversal size).
  SOURCE: Kontou & Sanders 2020, "Energy conditions in general relativity and quantum field theory", Class. Quantum Grav. 37, 193001, https://arxiv.org/pdf/2003.01815
  QUOTE: "all pointwise energy conditions are necessarily violated by essentially any quantum field theory" ; "comes closest to being generally valid is the achronal averaged null energy condition (AANEC)" ; "Particular questions of interest include the general validity, or otherwise, of the AANEC in higher dimensional Minkowski space and in curved spacetimes"
  ACCESS: full-text
  STATUS: textbook-or-review
  CONFIDENCE: high
- [RT-25] CLAIM: Topological censorship theorem (Friedman, Schleich & Witt 1993): PROVED theorem. If an asymptotically flat, globally hyperbolic spacetime satisfies ANEC (on all inextendible null geodesics), every causal curve from past to future null infinity is deformable to a curve in a simply connected neighbourhood of infinity, so no traversable wormhole (observers outside black holes cannot probe topology). A traversable wormhole in that setting therefore requires ANEC violation along some inextendible null geodesic. The authors note ANEC is violated by renormalised free-field stress tensors in generic spacetimes (Wald-Yurtsever); the open question is a weaker semiclassical condition (the achronal version).
  SOURCE: Friedman, Schleich & Witt 1993, "Topological Censorship", Phys. Rev. Lett. 71, 1486, https://arxiv.org/pdf/gr-qc/9305017
  QUOTE: "Theorem 1. If an asymptotically flat, globally hyperbolic spacetime (M, gab) satisfies the averaged null energy condition, then every causal curve from J- to J+ is deformable to γ0 rel J."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-26] CLAIM: Maldacena-Stanford-Yang 2017: GR forbids traversable wormholes in the sense that no signal can go through faster than outside; GJW evade this by coupling the two boundaries of a thermofield double. Information bound: the effective channel depends on the coupling g only through the phase exp(-i g <V>), so 0 <= g<V> < 2π, the interaction can be set up with just a few bits of exchange, and "we can't send more than a few bits" (probe approximation, at or slightly before the scrambling time). Two-sided, nearly-AdS2.
  SOURCE: Maldacena, Stanford & Yang 2017, "Diving into traversable wormholes", Fortsch. Phys. 65, 1700034, https://arxiv.org/pdf/1704.05333
  QUOTE: "It is well known that traversable wormholes are forbidden in general relativity. This says that we cannot send a signal through the wormhole faster than we can send it through the outside." ; "The interaction with such values of g can be set up with just a few bits of exchange, so we can't send more than a few bits."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-27] CLAIM: Chronology protection is a CONJECTURE (Hawking 1992, Phys. Rev. D 46, 603). Kay-Radzikowski-Wald 1997 PROVED theorems for QFT on spacetimes with a compactly generated Cauchy horizon: no extension of the field algebra satisfies F-locality at base points (past terminal accumulation points) of the horizon, i.e. the theory breaks down there. Interpreted as support for, not proof of, chronology protection; the authors say one must enter a regime where quantum gravity dominates and refrain from speculating about a complete quantum gravity. Time-machine models (Kim-Thorne, Gott, Grant) contain self-intersecting null geodesics.
  SOURCE: Kay, Radzikowski & Wald 1997, "Quantum field theory on spacetimes with a compactly generated Cauchy horizon", Commun. Math. Phys. 183, 533, https://arxiv.org/pdf/gr-qc/9603012
  QUOTE: "Thus, the theorems may be interpreted as giving support to Hawking's 'Chronology Protection Conjecture', according to which the laws of physics prevent one from manufacturing a 'time machine'." ; "in order to manufacture a time machine, it would be necessary at the very least to enter a regime where quantum effects of gravity itself will be dominant."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-28] CLAIM: Visser-Kar-Dadhich 2003: the amount of ANEC/energy-condition-violating matter at a traversable wormhole can be made ARBITRARILY SMALL by a suitable measure (volume integrals of p_r and p_t made arbitrarily small while volume integral of rho vanishes by construction) in spherically symmetric static examples; they conclude topological censorship is more like the area-increase theorem than the positive-mass theorem (small violations suffice). Caveat: this is a statement about the integrated volume measure, not that the NEC is respected, and not a statement about cost in mass/energy of a human-sized throat or about achronality.
  SOURCE: Visser, Kar & Dadhich 2003, "Traversable wormholes with arbitrarily small energy condition violations", Phys. Rev. Lett. 90, 201102, https://arxiv.org/pdf/gr-qc/0301003
  QUOTE: "We develop a suitable measure for quantifying this notion, and demonstrate the existence of spacetime geometries containing traversable wormholes that are supported by arbitrarily small quantities of "exotic matter"."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-29] CLAIM: Freivogel et al. 2019/2020: for GJW wormholes the wormhole is open for a proper time shorter than the Planck time; yet signal transmission can sometimes stay semiclassical. For black holes with horizons of order the AdS radius information cannot be reliably sent; large black holes (horizon >> AdS radius) allow more. 2+1D (BTZ) analysis, probe regime.
  SOURCE: Freivogel, Galante, Nikolakopoulou & Rotundo 2020, "Traversable wormholes in AdS and bounds on information transfer", JHEP 01 (2020) 050, https://arxiv.org/pdf/1907.13140
  QUOTE: "Although we find that the wormhole is open for a proper time shorter than the Planck time, the transmission of a signal through the wormhole can sometimes remain within the semiclassical regime. For black holes with horizons of order the AdS radius, information cannot be reliably sent through the wormhole."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-30] CLAIM: Ford-Roman 1996 (arXiv:gr-qc/9510071): quantum inequalities limit the magnitude and spatial/temporal extent of negative energy, sitting between pointwise and averaged conditions; used to constrain wormhole geometries (limits on ANEC violation constrain allowable wormhole geometries). Specific "thin band/Jupiter mass" numbers NOT confirmed in fetched text.
  SOURCE: Ford & Roman 1996, "Quantum field theory constrains traversable wormhole geometries", Phys. Rev. D 53, 5496, https://arxiv.org/pdf/gr-qc/9510071
  QUOTE: "A second type of constraint upon violations of the weak energy condition are "quantum inequalities" (QI's), which limit the magnitude and spatial or temporal extent of negative energy [9]-[13]."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high for quote; quantitative thin-band claims not verified
- [RT-31] CLAIM: Morris-Thorne 1988 human-travel criterion (secondary): tidal acceleration between two parts of a 2 m body not to exceed Earth gravity (~g); implies minimum throat radius of order several Earth radii/tens of thousands of km for the simple zero-tidal-spec metrics; throat needs radial tension exceeding energy density (tau > rho c^2), i.e. NEC violation. Compare Maldacena-Milekhin's looser 20 g criterion (RT-14). PDF extraction of the MT paper failed, so exact figures (e.g. 8.64 Earth radii) are unverified.
  SOURCE: Morris & Thorne 1988, "Wormholes in spacetime and their use for interstellar travel: A tool for teaching general relativity", Am. J. Phys. 56, 395, search-summary only
  SUMMARY: "The tidal accelerations between two parts of a traveler's body, separated by 2 meters, should not exceed Earth's gravitational acceleration ... the throat requires enormous outward radial tension, with the tension exceeding the local energy density."
  ACCESS: search-summary
  STATUS: secondary
  CONFIDENCE: low
- [RT-32] CLAIM: The brief's "ANEC along the throat" for Morris-Thorne metric is analytic: for ds^2 = -e^{2Φ}dt^2 + dr^2/(1-b/r) + r^2 dΩ^2, ρ = b'/(8π r^2) and the NEC along the radial null direction is ρ + p_r = (1/8π r^2)[b'... ] which at the throat (b = r0, flare-out b'(r0) < 1) gives ρ + p_r = (b' - b/r)/(8π r^2) < 0 at r0 (G = c = 1). Not recomputed here; recomputation is in the quantitative facet. (Own statement of standard result, marked unverified.)
  SOURCE: standard result; Hochberg & Visser https://arxiv.org/pdf/gr-qc/9710001 (not quoted)
  SUMMARY: derived formula is standard (Morris-Thorne 1988); not verified against a fetched quote
  ACCESS: search-summary
  STATUS: textbook-or-review
  CONFIDENCE: medium

- [RT-33] CLAIM: Olum (1998) theorem, carried from the warp run: with superluminal travel defined as a path that reaches a destination surface earlier than any neighbouring path, and assuming the generic condition, the existence of such a path P requires WEC violation at some point of P. Assumptions: classical GR, generic condition (holds whenever there is any normal matter or transverse tidal force on P), no singularities. Transfer to wormholes (my reading, not Olum's text): the theorem constrains a path that beats NEIGHBOURING paths. A wormhole shortcut beats paths in another homotopy class, and a throat already violates NEC (RT-03), so the theorem does not by itself exclude a wormhole shortcut; it says only that any such shortcut sits on a WEC-violating path, which a throat provides. Olum's own text does not mention wormholes (search for "wormhole" in the paper found no match).
  SOURCE: Olum K.D. 1998, "Superluminal travel requires negative energies", Phys. Rev. Lett. 81, 3567, https://arxiv.org/pdf/gr-qc/9805003
  QUOTE: "With this definition (and assuming the generic condition) I prove that superluminal travel requires weak-energy- condition violation." ; "The generic condition holds whenever there is any normal matter or any transverse tidal force anywhere on P ." ; "Thus we see that any spacetime that admits superluminal travel on some path P (and thus, according to our definition, that satisfies Condition 1) and th at satisfies the generic condition on P , must also violate the weak energy condition at some point of P ."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high for the theorem statement; medium for the transfer reading
  PRIOR: 2026-10-01-warp-drive-without-negative-energy (2026-10-01), was RT-03; re-verified
- [RT-34] CLAIM: Olum (1998) places his theorem next to the Tipler and Hawking theorems: those rule out building closed timelike curves from a compact region unless there is WEC violation or a singularity on the boundary of the causality-violating region, while Olum's theorem "rules out the existence, rather than construction" (the sentence is cut off in our extraction) of superluminal paths. He also says extending the theorem to cover more time machines than Tipler and Hawking is "not easily accomplished", because inside a CTC region every point lies in the future of every other, so the surfaces Sigma_A and Sigma_B cannot be built. Bears on the time-machine link of hidden premise 6: the WEC-violation requirement for time machines is a separate theorem, not a corollary of the shortcut theorem.
  SOURCE: Olum K.D. 1998, https://arxiv.org/pdf/gr-qc/9805003
  QUOTE: "These theorems rule out the construction of closed timelike curves (CTC’s) from a compact region unless there is WEC violation or a singularity on the bo undary of the causality violating region." ; "Inside a CTC-containing region, each point will be in the future of each other point. Thus one cannot construct surfaces Σ A and Σ B with the required properties."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
  PRIOR: 2026-10-01-warp-drive-without-negative-energy (2026-10-01), was RT-03 (second half; new quote this run)
- [RT-35] CLAIM: Visser, Bassett & Liberati (2000) state that wormhole-mediated effective FTL travel "necessarily involves" NEC violation, citing rigorous theorems, and add a perturbative argument for warp-type light-cone tipping: in linearised Einstein gravity about Minkowski space, NEC makes the Shapiro effect a delay and never an advance, and any object within the light cones is delayed relative to the minimum Minkowski traversal time. Scope: weak-field perturbation around Minkowski space, conference-proceedings level ("we argue"); the NEC-violation requirement for wormholes comes from the cited topological/throat theorems (RT-03, RT-25), not from this note. Their caveat: voids in lensing can give a time advance relative to an FRW background, which is not NEC violation.
  SOURCE: Visser M., Bassett B., Liberati S. 2000, "Superluminal censorship", Nucl. Phys. B Proc. Suppl. 88, 267, https://arxiv.org/pdf/gr-qc/9810026
  QUOTE: "It is well established, via a number of rigorous theorems, that any possibil- ity of eﬀective FTL travel via traversable worm- holes necessarily involves NEC violations [1–4]." ; "Given the NEC, the Shapiro time delay in any weak gravitational field is always a delay relative to the Minkowski background, and never an advance."
  ACCESS: full-text
  STATUS: peer-reviewed (conference proceedings)
  CONFIDENCE: high
  PRIOR: 2026-10-01-warp-drive-without-negative-energy (2026-10-01), was RT-07; re-verified
- [RT-36] CLAIM: Penrose, Sorkin & Woolgar (1993) positive-mass theorem rests on causal structure: positive energy density focuses and retards null geodesics, while negative total mass would advance them. It uses the null-geodesic retardation near infinity (Shapiro-type delay in O(1/r) fields) and does not look behind horizons. Gao-Wald's Theorem 1 "expresses a key aspect" of this argument (RT-15). This is the mechanism behind "a shortcut means negative energy somewhere": a wormhole that gave a time advance between asymptotic regions would be in tension with positive ADM mass unless NEC (or ANEC) fails along the relevant geodesics. Scope: the theorem assumes NEC-type focusing; it is not a no-wormhole theorem, since a throat violates NEC.
  SOURCE: Penrose R., Sorkin R.D., Woolgar E. 1993, "A positive mass theorem based on the focusing and retardation of null geodesics", arXiv:gr-qc/9301015 (no journal ref listed by INSPIRE), https://arxiv.org/pdf/gr-qc/9301015
  QUOTE: "A positive mass theorem for General Relativity Theory is proved. The proof is 4-dimensional in nature, and relies completely on arguments pertaining to causal structure, the basic idea being that positive energy-density focuses null geodesics, and correspondingly retards them, whereas a negative total mass would advance them. Because it is not concerned with what lies behind horizons, this new theorem a pplies in some situations not covered by previous positivity theorems."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high for the abstract; medium for the transfer to wormholes (my reading)
  PRIOR: 2026-10-01-warp-drive-without-negative-energy (2026-10-01), was RT-14; re-verified (abstract now confirmed in full text). The Schoen-Yau / Witten spinor proof carried as a "standard reference" in the warp run was NOT re-opened and is not carried.
- [RT-37] CLAIM: Compactness bound for thin shells, carried from the warp run with a narrow scope: Andréasson (2008) proves sup 2m(r)/r <= ((1+2Omega)^2 - 1)/(1+2Omega)^2 for static spherically symmetric matter with rho >= 0, p >= 0 and p + 2 p_T <= Omega rho, sharp, with equality approached by an infinitely thin shell with p = 0 and 2 p_T = Omega rho; Omega = 1 gives Buchdahl's 2M/R <= 8/9, and DEC-obeying matter with p >= 0 has Omega = 3. SCOPE FOR WORMHOLES: the hypotheses require rho >= 0, so the bound does NOT apply to a Visser thin-shell wormhole, whose junction shell needs negative surface energy density for the Schwarzschild-type exterior (standard result, not quoted here; see Gaps). It bears only on (a) positive-energy shells added around a throat, e.g. a payload shell, and (b) the horizon-formation limit when positive mass is piled near a throat. Arithmetic (mine): Omega = 3 gives 2M/R <= 48/49.
  SOURCE: Andréasson H. 2008, "Sharp bounds on 2m/r of general spherically symmetric static objects", J. Differential Equations 245, 2243, https://arxiv.org/pdf/gr-qc/0702137
  QUOTE: "The bound that we obtain for 2 m/r is sharp in the sense that an in- ﬁnitely thin shell of matter, with 2 m/r equal to the critical value, will sat- isfy a form of the generalized TOV equation which allows ρ and pT to be measures ( p = 0 here)." ; "Note that when Ω = 1 the original bound by Buchdahl is recovered. The assumptions on t he matter model are very general and in particular any model with p ≥ 0 which satisﬁes the dominant energy condition satisﬁes the hypothe ses with Ω = 3 ."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high for the theorem; medium for the stated non-applicability (my reading)
  PRIOR: 2026-10-01-warp-drive-without-negative-energy (2026-10-01), was RT-13; re-verified
- [RT-38] CLAIM: Newer than the warp run's date window but bearing on hidden premise 3: Weinbaum (2026, PRD 114, 084004) shows that classical positive-frequency Dirac fields on certain FIXED wormhole geometries can violate ANEC (so they are candidates to source a throat), but a numerical search for static, spherically symmetric, asymptotically flat Einstein-Dirac solutions with definite frequency, angular momentum and parity finds only "partial-wormhole solutions": regular throat and correct asymptotics at one end that cannot be continued to a second asymptotically flat end. He says the earlier Einstein-Dirac-Maxwell claims did not account for single-particle states not self-interacting electromagnetically and having positive-frequency modes. Scope: numerical evidence for that field ansatz, not a theorem; the abstract's final sentence about reflection-symmetric cases was truncated in our extraction.
  SOURCE: Weinbaum R.J. 2026, "Obstructions to traversable wormholes in Einstein-Dirac theory", Phys. Rev. D 114, 084004, arXiv:2607.28738, https://arxiv.org/pdf/2607.28738
  QUOTE: "We find “partial-wormhole solutions,” describing a regular wormhole throat with correct asymptotics at one end of the wormhole, but we find that these solutions cannot be continued to a second asymptotically flat end." ; "classical, positive-frequency Dirac fields on certain fixed wormhole geometries can violate ANEC, so they are indeed candidates for sourcing traversable wormholes."
  ACCESS: full-text
  STATUS: peer-reviewed (per INSPIRE journal ref; text read from the arXiv version)
  CONFIDENCE: medium (numerical; critiques facet should assess)
- [RT-39] CLAIM: Pastén et al. (2026, CQG 43, 115014) formulate wormhole traversability as a local, covariant null-defocusing condition from the Raychaudhuri equation, independent of the metric ansatz, and prove that any genuinely traversable wormhole in unimodular gravity violates the NEC; unimodular gravity keeps the local focusing structure of GR, so this restates the GR throat theorem (RT-03) for that theory rather than adding a new constraint for GR. Relevant to the brief's "modified gravity" extension: unimodular gravity gives no escape.
  SOURCE: Pastén E. et al. 2026, "Null Raychaudhuri equation and the impossibility of traversable wormholes in unimodular gravity", Class. Quantum Grav. 43, 115014, arXiv:2602.00524, https://arxiv.org/pdf/2602.00524
  QUOTE: "We prove that any genuinely traversable wormhole in unimodular gravity necessarily violates the null energy condition, establish- ing a general local no–go theorem for wormholes supported by ordinary matter in this framework."
  ACCESS: full-text
  STATUS: peer-reviewed (per INSPIRE journal ref)
  CONFIDENCE: medium
- [RT-40] CLAIM: Altunkaynak & Tuncer (2025, arXiv:2512.22928) claim a throat-area monotonicity theorem for traversable AdS wormholes: after a traversable window opened by an ANEC-violating GJW-type deformation, subsequent signal matter obeying pointwise NEC cannot increase the throat cross-section area; combined with a bit-thread max-flow argument they propose Q_max <= A_min/(4 G_N) qubits. Scope: holographic/AdS, semiclassical, a "geometric proxy" bound; it would imply that a payload of ordinary positive-energy matter cannot widen a throat (hidden premise 10). Single unrefereed preprint by authors outside the established wormhole groups; quantities not checked against Maldacena-Stanford-Yang (RT-26) or Freivogel et al. (RT-29), which bound the same thing more concretely.
  SOURCE: Altunkaynak F.B., Tuncer A. 2025, "Area Monotonicity of Wormhole Throats and a Geometric Bound on Information Transfer", arXiv:2512.22928, https://arxiv.org/pdf/2512.22928
  QUOTE: "any subsequent signal-carrying matter satisfying the pointwise null energy condition (NEC) causes the throat cross-sectional area to be non-increasing. Second, we utilize this monotonicity to derive a semiclassical geometric upper bound on the number of independent quantum degrees of freedom (qubits) transmissible through the wormhole. This bound Qmax≤A min/4GN"
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: low
- [RT-41] CLAIM: Poisson & Visser (1995) analyse linearised stability of Schwarzschild thin-shell wormholes (thin-shell formalism, junction at the throat, shell radius a0, mass M, equation-of-state parameter beta0^2 = dp/dsigma). Stability requires beta0^2 above or below a bound depending on a0/M, with the sign of the inequality flipping at a0 = 3M (their eqs 31-32), and for the usual range requires "perverse" speeds of sound; the shell's surface energy density sigma0 is negative, so it is already "exotic matter" and ordinary positivity arguments do not apply. This supplies the premise for the scope statement in RT-37 (Andréasson's rho >= 0 hypothesis fails for such shells). Numerical details of the stability region are in their Fig. 1 and are not reproduced here.
  SOURCE: Poisson E., Visser M. 1995, "Thin-shell wormholes: linearization stability", Phys. Rev. D 52, 7318, https://arxiv.org/pdf/gr-qc/9506083
  QUOTE: "we are already dealing with “ex- otic matter,” in the sense that the surface energy density σ0 is negative. Thus, naive arguments depending on the stability of matter and the positivity of energy should be taken with a grain of salt." ; "insisting on stability seems possible only at the cost of requiring somewhat perverse restrictions on the speed of sound."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high for the quotes; the PRD volume/page is from memory and unverified against a fetched record
  
## Gaps
- Warp-run items NOT carried because they do not transfer to a throat: Natário's drive theorem and Santiago-Schuster-Visser's NEC theorem for unit-lapse flat-slice shifts (RT-01 to RT-05 of the warp run); the Lentz / Fell-Heisenberg / Bobrick-Martire / Fuchs shell results. The Schoen-Yau / Witten spinor positive-mass theorem was not re-opened.
- The conditions under which Olum's neighbouring-path definition of superluminal travel applies to a wormhole between two mouths in different homotopy classes are not addressed in Olum 1998; RT-33's transfer is my reading. No paper found that applies Olum 1998 to wormholes explicitly (not searched exhaustively).
- Visser 1989 original thin-shell junction paper not opened; RT-41 (Poisson & Visser) supplies the negative-sigma0 statement for the Schwarzschild case only.
- Searched for work newer than 2026-10-01 (lit_search --since 2026, "traversable wormhole", "averaged null energy condition"): nothing dated after 2026-10-01 turned up that contradicts a carried claim; the latest items seen are from 2026-07/09 (Weinbaum, Pastén, Freivogel et al. "How traversable is a traversable wormhole?" arXiv:2606.12528, left to the frontier facet).
- Corrections made this run following the source check: RT-03 journal ref (PRL is gr-qc/9802048, not gr-qc/9710001) and RT-15 quote wording.
- Morris & Thorne 1988, Morris-Thorne-Yurtsever 1988, Visser 1989/1995, Poisson-Visser 1995, Hawking 1992, Kim-Thorne 1991, Frolov-Novikov 1990, Geroch 1967, Tipler 1977 are not on arXiv or were image PDFs: no verbatim quotes. MT tidal/Jupiter-mass figures remain search-summary or unverified (the "Jupiter mass for a 1 m throat" figure was not found or confirmed).
- Ford-Roman thin-band quantitative claims, Kontou-Olum 2015 and Urban-Olum 2010 not fetched.
- Published numerical ANEC values for GJW, the MMP Casimir integral and FGM t_transit corrections were not reproduced (quantitative facet); only structural statements quoted. MMP eq 5.30-5.31 extraction is garbled (RT-07 low confidence).
- Journal refs for Maldacena-Qi (arXiv:1804.00491), FGM 2018 and Kain 2023 not confirmed from fetched text.
- Konoplya-Zhidenko PRL itself (arXiv:2106.05034) and the Danielson et al. matching-condition critique were not opened; Kanai et al. 2026 (arXiv:2511.21017, PRD 113 064026, no-go theorems for wormholes as perturbations of near-horizon BH geometries) seen only via lit_search abstract.
- No source states a proof that the self-consistent achronal ANEC holds in general curved spacetime; status is conjecture with partial proofs (2D free scalar, Wall's GSL derivation under assumptions, flat-space QFT proofs).
- RT-32 formula (ρ+p_r at the Morris-Thorne throat) is a standard derivation, not a fetched quote.
