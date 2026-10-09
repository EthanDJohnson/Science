# Analysis: decomposer (methodical doubt and decomposition)
status: final

## Method applied
Rewrite Q1–Q4 as a tree of sub-questions ending at items a calculation, measurement or cited theorem can settle; build a ledger of every premise (measured / derived / assumed / unknown); name the load-bearing assumption and its test; sort sub-questions into settled-by-dossier and open.

## Findings
1. **Q2 splits into three questions with three different answers, set by which "negative energy" is meant.** (a) Pointwise: every static or dynamic throat violates the NEC somewhere at or near the throat (Hochberg–Visser, proved, local geometry only) [K-02], and essentially every QFT violates every pointwise condition anyway [K-11], [D-26]. "Without pointwise negative energy" is therefore closed: no, for every construction, including BKR, where the Dirac field becomes the NEC-violating source [D-10a], [D-11]. (b) ANEC along some complete null geodesic: required for asymptotically flat, globally hyperbolic traversable wormholes (topological censorship, proved) [K-01]. Every quantum-supported construction supplies it: GJW [D-01], MQ (∫T₊₊ = −2φ_r) [D-04], FGM [D-05], MMP along the field-line circles [D-06]. (c) ANEC along a complete *achronal* null geodesic: only this sense stays open. Long wormholes have no complete achronal null geodesic through them [K-07f], [D-27], so they need not violate it. The answer to "held open without negative energy?" is therefore "no" in senses (a) and (b), and "yes, conditionally" in sense (c), for MMP, MM and (marginally) FGM 2019.
2. **In every surviving construction the negative energy comes from ordinary quantum fields, not from exotic classical matter.** The sources are Casimir-like vacuum energy of fermions in Landau levels (MMP, MM) [D-06], [D-08], boundary-coupling-induced one-loop stress (GJW, MQ) [D-01], [D-04], and quotient-topology Casimir energy (FGM) [D-05]. The one family that claimed classical "no exotic matter" support (EDM) fails on three independent grounds: it is not a solution in the symmetric case [D-10b]; the asymmetric version is dynamically non-traversable [D-11]; and the static obstruction is numerical but strong [D-12]. Hidden premise 3 is confirmed: "ordinary matter" does not mean "no negative energy".
3. **Graham–Olum's conjecture, quoted from its own abstract, is the hinge for Q1.** [new: Graham & Olum 2007, arXiv:0705.3193 (PRD 76, 064001), abstract, "requiring only that there is no self-consistent space-time in semiclassical gravity in which ANEC is violated on a complete, {\em achronal} null geodesic. We indicate why such a condition might be expected to hold and show that it is sufficient to rule out wormholes and closed timelike curves."] Both "wormholes" (in their theorem's class) and CTCs fall under one conjecture, so the two cruxes the brief names are not independent (see Finding 5).
4. **Graham–Olum's proved theorem does not cover one-sided wormholes; a shortcut ban for one-sided wormholes is derived, not proved.** Their topological-censorship theorem assumes a simply connected spacetime, so "the wormholes we rule out are only those which connect one asymptotically flat region to another, not those which connect a region to itself" [new: Graham & Olum 2007, arXiv:0705.3193 PDF p. 5, full-text, "We must also restrict ourselves to simply-connected spacetimes, which means that the wormholes we rule out are only those which connect one asymptotically flat region to another, not those which connect a region to itself."]. Their own counterexample is exactly the long wormhole [new: same, p. 5–6, full-text, "suppose the throat of the wormhole is longer than the distance between the mouths on the outside. Any causal path through the wormhole emerges in the future of the place where it entered, and thus is not achronal. We can still find fastest paths through the wormhole, but they are chronal."]. The converse step is the decomposer's derivation, not a theorem: in a static one-sided *shortcut* wormhole, the fastest causal curve through the throat in its homotopy class is a complete null geodesic, and no curve in another class (exterior, or multiple passes) beats it, so it is achronal. Self-consistent achronal ANEC would then forbid it. MMP assert the same conclusion ("short wormholes ... are not allowed by the Einstein equations combined with the achronal average null energy condition") [D-06], and Kontou says the condition "seems to prohibit" shortcut wormholes [D-27]. Status of "one-sided shortcut ⇒ achronal ANEC violation": **derived**, with the static, generic-condition and completeness steps assumed. FGM 2019 call their own version "general arguments (GSL)" [D-07].

5. **A long wormhole cannot become a time machine without first becoming a shortcut, so both cruxes rest on one conjecture.** Kinematics: take mouths at rest with exterior light time d/c and throat transit L/c (exterior coordinate time), and let −s be the lag built up between the mouth clocks by MTY mouth motion or by parking a mouth at a different potential. Then the throat route is a shortcut once −s > (L − d)/c, and a CTC exists once −s ≥ (L + d)/c. Because −s builds up continuously, any route to a CTC crosses the shortcut threshold first, for long throats (L > d) as well as short ones [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-decomposer_timeshift.py]. During that stage a complete achronal null geodesic runs through the throat (Finding 4). So self-consistent achronal ANEC, if true, stops the conversion at the shortcut stage, before any chronology horizon forms. Hawking-type chronology protection [K-12] is then a second line of defence, needed only if achronal ANEC fails. This is a derived claim; its assumption is that the mouths' clock lag is the only thing that changes (no change of topology or of throat length during the motion). The mechanist lens owns the reference numbers; these are my own.
6. **MM numbers for the conversion (my own calculation; scale only).** Take ℓ ≈ 3×10³ ly, so L = πℓ ≈ 9.4×10³ ly [Q-02], [Q-06], and treat ℓ as fixed while d varies (an approximation; in MM, ℓ and d are tied). At d = 1000 ly the shortcut needs a lag of about 8.4×10³ yr, and a CTC about 1.04×10⁴ yr. MTY motion of one 2×10³⁴ kg mouth [Q-04] at 0.1c gives γ = 1.005, which needs an exterior trip of about 1.7×10⁶ yr and a kinetic energy of about 9×10⁴⁸ J (about 51 M_☉c²). At 0.9c the trip is about 1.5×10⁴ yr and the energy about 2.3×10⁵¹ J (1.3×10⁴ M_☉c²). Parking a mouth at lapse α = 0.5 for about 1.7×10⁴ yr does the same. For contrast, a hypothetical 1 m Ellis throat between mouths 1 ly apart has T_thru/T_ext ≈ 2×10⁻¹⁵, and a lag of about 1 yr would turn it into a time machine [calc: same file]. Short throats are therefore the dangerous case for chronology. Long throats are protected by their own length only quantitatively, not in principle.
7. **No two-sided construction delivers anything earlier than, or without, its coupling channel, so Q1 is closed for them.** GJW: no signal passes in the decoupled system, it "cannot be used to violate causality", and only "a few bits" pass [D-01], [D-02], [K-15]. MQ needs the external coupling [D-04]. The comparison the brief asks for is settled: no.
8. **No existing one-sided construction is a shortcut, by its authors' own numbers.** MMP: transit/d > 2 [Q-12]. MM: πℓ > d for any d [Q-06], with T_thru/T_ext ≈ 9.4 at d = 1000 ly and π at d = ℓ [calc: same file]. FGM 2019: t_min = d + logs, which approaches d from above [Q-13]. What these offer is proper-time compression (MM: about 0.16 s for the traveller against about 9.4×10³ yr outside [Q-06]), not causal advance (hidden premise 4).
9. **Payload capacity in principle is not the binding constraint for MM, unlike GJW.** A payload must stay below MM's |E_bin| ≈ 5×10⁹ kg [Q-02] (their own 10³ kg ship condition [Q-03]). That gives m/|E_bin| = 2×10⁻¹⁰ for 1 kg and 1.4×10⁻⁸ for a 70 kg human [calc: same file]. GJW/MSY pass only "a few bits" (a parametric bound) [K-15], and the GJW window is shorter than the Planck time [Q-16]. Hidden premise 10 therefore splits: it is binding for the AdS two-sided constructions and not binding for MM. MM's binding constraints are instead tidal size (r_e > 1.5×10⁷ m [Q-01]), the speculative sector [Q-03], [K-22], refrigeration [Q-07], and formation (none known) [D-08].
10. **Hidden premise 2 is confirmed and sharpened.** Pointwise NEC violation is forced and generic, and so carries no information [K-02], [K-11]. ANEC along chronal null lines is violated by MMP and costs nothing in principle [D-06]. The discriminating quantity is ANEC on complete *achronal* geodesics, and the discriminating geometric fact is L > d (throat longer than the exterior path). Volume-integrated NEC measures [D-C9], [K-21] answer none of Q1–Q2.

11. **The one known achronal-ANEC violation is a test-field result, so it leaves the self-consistent conjecture standing.** Confirming RC-03, which the dossier lists as unchecked: [new: Urban & Olum 2010, arXiv:0910.5925 (PRD 81, 024039), abstract, "The violation is dependent on the quantum state and can be made as large as desired. ... Since all geodesics in conformally flat spacetimes are achronal, the achronal averaged null energy condition is likewise violated."]. The background is fixed rather than self-consistent, which is why Graham–Olum's restriction to self-consistent spacetimes carries the weight [D-C3], [D-27]. The load-bearing premise is therefore the *self-consistency* clause, not achronality alone.

## Lens-specific outputs

### Sub-question tree

Root: can a traversable wormhole beat light through the surrounding space (Q1), can it be held open without negative energy (Q2), what would it cost (Q3), and what tests it (Q4)?

- **Q1 Shortcut**
  - Q1.1 Is "shortcut" defined for this construction? Two-sided: compare with the coupling channel. One-sided: needs synchronisation through the exterior (brief definitions). *Leaf: definitional.*
  - Q1.2 Two-sided (GJW, MQ): does anything arrive earlier than, or without, the coupling? *Leaf: published statements* [D-01], [D-02], [D-04]. SETTLED: no.
  - Q1.3 One-sided constructions on record (MMP, MM, FGM 2019): T_thru/T_ext? *Leaf: published values + calc* [Q-06], [Q-12], [Q-13]. SETTLED: all ≥ 1.
  - Q1.4 Could any one-sided shortcut exist in admissible physics?
    - Q1.4a Does a one-sided shortcut require ANEC violation on a complete achronal null geodesic? *Leaf: theorem.* PARTLY OPEN: proved only for simply connected two-region spacetimes (Graham–Olum Theorem 1). For one-sided, derived (Finding 4) and asserted by MMP [D-06] and Kontou [D-27].
    - Q1.4b Does self-consistent semiclassical gravity forbid that violation? *Leaf: theorem or counterexample.* OPEN: conjecture [K-07a]; partial proofs [K-07b–d]; test-field counterexample only (Finding 11). **Load-bearing.**
    - Q1.4c With labelled speculative matter (phantom fields, modified gravity), do short static geometries exist? *Leaf: calc.* SETTLED as geometry: Ellis and thin-shell throats exist and can be short (Finding 6), but they are unstable [D-13], [D-14] and need pointwise, ANEC and achronal-ANEC violation by classical exotic matter.
  - Q1.5 Shortcut → time machine?
    - Q1.5a Kinematic thresholds: shift (L − d)/c for a shortcut, (L + d)/c for a CTC. *Leaf: calc.* SETTLED (Finding 5).
    - Q1.5b Can a long wormhole skip the shortcut stage? *Leaf: continuity argument.* SETTLED as derived: no, unless topology or throat length changes discontinuously.
    - Q1.5c Does semiclassical back-reaction stop a CTC from forming? *Leaf: theorem.* OPEN: KRW is proved for linear fields at compactly generated Cauchy horizons, presented as "support"; Hawking's is a conjecture [K-12], [D-C4].
- **Q2 Support**
  - Q2.1 Without pointwise NEC violation? SETTLED: no [K-02].
  - Q2.2 Without ANEC violation along any complete null geodesic? SETTLED: no, for asymptotically flat, globally hyperbolic spacetimes [K-01]; each construction supplies it (Finding 1).
  - Q2.3 Without achronal-ANEC violation? SETTLED as "yes, for long wormholes" [K-07f], [D-06], [D-27], conditional on MMP being a valid self-consistent solution (Q2.5).
  - Q2.4 Is the negative energy ordinary-QFT, classical exotic, or unbounded classical Dirac? SETTLED for MMP, MM, GJW, MQ and FGM: ordinary QFT (Casimir-like). EDM: CONTESTED and strongly disfavoured [D-C2], [D-10]–[D-12].
  - Q2.5 Does each construction survive back-reaction and stability? PARTLY OPEN.
    - MMP: probe-dependent transmission [D-C5]; linear stability is preliminary [F-01].
    - FGM 2019: exponentially fragile, and the mouths merge on a timescale ∼ d^{3/2} [D-07].
    - MM: accumulated infall makes it collapse [D-08].
    - Ellis and thin-shell throats: unstable [D-13], [D-14].
- **Q3 Cost** (for the survivors MMP, MM and FGM 2019; GJW and MQ are not in our universe)
  - Q3.1 Throat size for a human: r_e > 1.5×10⁷ m under MM's 20 g criterion [Q-01], or about 6.8×10⁷ m under the MT-like 1 g criterion [Q-52], [D-C8]. SETTLED up to the choice of criterion.
  - Q3.2 Mouth mass: about 2×10³⁴ kg [Q-04]. SETTLED. Charge: OPEN because of the unit convention [D-C7].
  - Q3.3 Payload back-reaction: m/|E_bin| ≈ 10⁻¹⁰ to 10⁻⁸ for MM (Finding 9). SETTLED in scale.
  - Q3.4 Formation route: OPEN/UNKNOWN. None is given for MM [D-08]; no Garfinkle–Strominger rate was retrieved; the topology-change theorems were not retrieved (dossier §6).
  - Q3.5 Gap to demonstrated technology: mass about 26+ orders [F-19]; classical-throat tension against Casimir pressure 10³⁷ to 10⁴² [Q-32]. SETTLED in order of magnitude.
- **Q4 Tests**
  - Q4.1 Sycamore: tests size-winding teleportation in a learned 7-fermion Hamiltonian; no spacetime was made [D-16]; whether it is gravitational is contested [D-C1]. SETTLED: "not a wormhole".
  - Q4.2 Lensing, echoes, shadows, S2: probe only classical Ellis or negative-mass objects or horizon replacements [D-22]–[D-24]. SETTLED: they do not reach MMP/MM.
  - Q4.3 A direct test of the load-bearing crux? OPEN. No experiment or observation tests self-consistent achronal ANEC. No laboratory QEI test of the relevant type exists [D-C6]. It is decided by theory: a proof in 4D semiclassical gravity with quantised gravitons, or a self-consistent counterexample.
  - Q4.4 An ingredient test: magnetic charge. MoEDAL excludes 1 to 3 g_D up to 75 GeV/c² [D-25], [Q-46]. SETTLED as a null result, but it is far from MMP/MM scales.

### Assumption ledger

| # | Premise | Class | Basis | If it fails |
|---|---|---|---|---|
| L1 | Classical GR + semiclassical gravity (G = 8π⟨T⟩) is valid at the throat | assumed | Brief's admissible physics; MMP and MM throats are macroscopic. Planck-size throats are excluded [D-27] | GJW (open time < Planck time [Q-16]) and EDM (throat 75–498 l_P [Q-18]) fall outside the regime: their "traversability" is not a semiclassical statement |
| L2 | "Negative energy" = WEC violation, with NEC/ANEC/achronal ANEC kept separate | assumed (definition) | Brief | Q2 flips between "no" (pointwise, ANEC) and "yes" (achronal ANEC) |
| L3 | Any throat violates the NEC pointwise | derived (theorem) | Hochberg–Visser [K-02] | Would reopen "no exotic matter"; no credible route |
| L4 | Topological censorship: an asymptotically flat, globally hyperbolic traversable wormhole needs ANEC violation | derived (theorem) | FSW [K-01] | Not expected |
| L5 | Self-consistent achronal ANEC holds | **assumed (conjecture)** | GO 2007; partial proofs [K-07]; no self-consistent counterexample [D-27] | Shortcuts and CTCs return (Q1 flips) |
| L6 | A one-sided shortcut carries a complete achronal null geodesic through the throat | derived (decomposer + MMP/Kontou statements) | Finding 4 | If false, one-sided shortcuts escape L5 even if L5 holds; Q1 reopens |
| L7 | Long wormholes have no complete achronal null geodesic through them | derived (theorem-level, GO p. 5–6) | Finding 4 quote; [K-07f] | Would bring MMP and MM under L5 and threaten them |
| L8 | MMP is a valid self-consistent semiclassical solution | derived (perturbative, peer-reviewed) | [D-06]; Q-10 | Q2.3 "yes" loses its only Standard-Model-compatible example |
| L9 | MMP is stable on transit timescales | unknown | [D-C5], [F-01] preliminary | Q3 survivors shrink to MM (speculative) and FGM (transient) |
| L10 | Results from AdS and 2D transfer to 4D asymptotically flat spacetime | unknown | No source treats it (dossier §6) | GJW, MQ and FGM 2018 say nothing about our universe beyond mechanism |
| L11 | RS II + dark U(1) exist (MM) | assumed (labelled speculative) | [D-08], [Q-03] | The humanly traversable row is eliminated |
| L12 | The mouth time lag builds up continuously, with throat length and topology fixed | assumed | Finding 5 | A discontinuous route could skip the shortcut stage; none is known |
| L13 | Shortcut is measured with static observers, synchronised through the exterior | assumed (definition) | Brief | Another synchronisation could make T_thru/T_ext frame-dependent; achronality is frame-free, so the verdict is not |
| L14 | The tidal criterion is 20 g over 0.5 m (MM) or 1 g over 2 m (MT) | assumed (choice) | [D-C8] | Throat-size anchor moves by a factor of about 4.5 |
| L15 | The MM charge in a stated convention | unknown | [D-C7] | Charge and field column of the cost table uncertain |
| L16 | The Sycamore dynamics are gravitational | contested | [D-C1] | Q4 "nearest test" loses its only lab-gravity claim; it was never a wormhole in any case |
| L17 | Astronomical searches assume classical Ellis/negative-mass lenses | measured (scope of searches) | [D-22]–[D-24] | — |
| L18 | Casimir negative energy is real and measurable | measured | [D-19], [Q-31], [Q-33] | — |
| L19 | QEIs (Fewster–Eveson, Ford–Roman) hold for free fields | derived (theorem) | [K-08], [K-09]; contested for squeezed light only in a modified form [D-C6] | Throat-band bounds [Q-20], [Q-21] loosen |
| L20 | Formation is possible at all (topology change, pair creation) | unknown | Not retrieved (dossier §6) | Q3 is moot |
| L21 | Positive-energy payload infall closes the throat | derived (numerical, spherical) | [D-13] Kain 2026; [D-08] | Payload limits loosen |

### Load-bearing assumption

**L5, the self-consistent achronal ANEC (with L6 as its bridge to one-sided wormholes).**

Why it is load-bearing:
- Everything else in Q1 is settled by published statements and by geometry.
- If L5 holds (and L6 holds), no admissible wormhole is a shortcut, and no wormhole can be converted into a time machine, because conversion passes through a shortcut stage first (Finding 5).
- If L5 fails, both answers flip together. Short throats then become shortcuts by factors like 10⁻¹⁵ at 1 ly (Finding 6), and become time machines with a clock lag of only about d/c.

Q2 has a separate load-bearing premise, L2, but it is definitional: the answer depends on which energy condition is meant, and Finding 1 states all three answers.

What would test L5:
- *Theory.* (i) A proof of achronal ANEC for interacting fields in 4D curved spacetime with quantised linear gravitons, which would remove Wall's caveat [K-07c]. (ii) Or a self-consistent semiclassical solution (back-reacted, not test-field) with ANEC < 0 on a complete achronal geodesic, for example a one-sided short-throat analogue of MMP or FGM solved to back-reaction order. (iii) A cheaper test of L6: compute, in FGM 2019's perturbative solution, whether t_min − d stays positive at second order. A negative value would be a self-consistent counterexample.
- *Experiment.* None is feasible. A laboratory measurement can test only flat-space QEIs (L19), not self-consistency in curved spacetime.

### Settled vs open

- **Settled by the dossier (plus this lens's arithmetic):**
  - Q1.1 to Q1.3, Q1.4c, Q1.5a and Q1.5b (derived);
  - Q2.1 to Q2.4 (EDM strongly disfavoured);
  - Q3.1 (up to the choice of criterion), Q3.2 (mass), Q3.3 and Q3.5;
  - Q4.1, Q4.2 and Q4.4.
- **Open:**
  - Q1.4a: a theorem for one-sided wormholes;
  - **Q1.4b: self-consistent achronal ANEC (load-bearing)**;
  - Q1.5c: chronology protection, demoted to second line by Finding 5;
  - Q2.5: MMP stability and probe dependence;
  - Q3.2: charge convention;
  - Q3.4: formation;
  - Q4.3: no direct test of the crux;
  - L10: what transfers from AdS and 2D to our universe.

## Calculations
- `runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-decomposer_timeshift.py` (log `.py.log` beside it). It computes:
  - **Thresholds.** The mouth-clock lag that makes a one-sided wormhole a shortcut, (L − d)/c, and the lag that makes it a time machine, (L + d)/c. The CTC/shortcut lag ratio is 1.93 at L = πd and 1.22 at L = 10d.
  - **MM conversion figures** (ℓ = 3×10³ ly held fixed, L = 9425 ly):
    - lags at d = 1000 ly: 8425 yr for a shortcut, 1.04×10⁴ yr for a CTC;
    - MTY mouth motion at 0.1c: exterior trip 1.68×10⁶ yr, kinetic energy 9.1×10⁴⁸ J (50.7 M_☉c²) for one 2×10³⁴ kg mouth;
    - at 0.9c: trip 1.49×10⁴ yr, kinetic energy 2.3×10⁵¹ J;
    - parking at lapse 0.5: 1.69×10⁴ yr.
  - **Ellis contrast** (b₀ = 1 m, observers at R = 10 m, SI): T_thru = 6.6×10⁻⁸ s. T_thru/T_ext = 0.020 at d = 1 km, 1.3×10⁻¹⁰ at 1 AU and 2.1×10⁻¹⁵ at 1 ly.
  - **MM payload ratios:** m/|E_bin| = 2×10⁻¹⁰ (1 kg), 1.4×10⁻⁸ (70 kg), 2×10⁻⁷ (10³ kg).

## Candidate answers (at least 3; the null and a reframe count)
- [DECOMPOSER-A] **Conditional no-shortcut, yes-to-support-by-quantum-fields.**
  - Claim:
    - Wormholes can be held open in admissible semiclassical physics (MMP in 4D with Standard-Model-like fermions; MM with a labelled speculative sector; FGM 2019 transiently).
    - They do this with negative energy from ordinary quantum fields, which violates the NEC pointwise and the ANEC along chronal lines, but not on any achronal geodesic.
    - Every such wormhole is long, so none is a shortcut. One-sided shortcuts, and time machines made by moving mouths, are excluded if and only if self-consistent achronal ANEC holds, which is a conjecture with no known self-consistent counterexample.
  - Status: surviving.
  - Why: each step is either a theorem [K-01], [K-02], an authors' own statement [D-06], [D-07], [Q-06], or a derivation stated here (Findings 4–5).
  - Distinguishing test: a back-reacted semiclassical solution with a short one-sided throat would refute A. A second-order FGM 2019 calculation giving t_min < d would also refute it. A proof of achronal ANEC with quantised gravitons would promote A from conditional to established.
  - Confidence: medium-high on the structure; medium on L5.
- [DECOMPOSER-B] **Null: no traversable wormhole is realisable in our universe at all.**
  - Claim: every 4D asymptotically flat construction is unstable or transient (FGM 2019 merges and is exponentially fragile; MM collapses from infall; Ellis and thin shells are unstable), needs a speculative sector (MM), or fails as a solution (EDM). MMP's stability is unproven. So the only "survivors" are AdS/2D models that do not transfer.
  - Status: strained.
  - Why strained: MMP is a peer-reviewed self-consistent perturbative solution using Standard-Model-like fermions at sub-TeV size [D-06], [Q-11], and the only stability work so far finds no growing mode in one sector [F-01] (preliminary). B needs a demonstrated MMP instability, or a failure of L10 that also covers MMP (it does not, since MMP is 4D).
  - Distinguishing test: a complete MMP linear stability analysis (all sectors, beyond O(α)) that finds a growing mode faster than the transit time would move B to surviving. Finding none would eliminate B for MMP.
  - Confidence: low-medium.
- [DECOMPOSER-C] **Reframe: the question's two halves are one question, and the real answer is proper-time compression without causal advance.**
  - Claim:
    - "Sooner than light outside" and "turning a wormhole into a time machine" are governed by the same quantity, ANEC on achronal geodesics. That quantity vanishes as a constraint exactly when the throat is longer than the exterior path, and any CTC route passes through a shortcut first (Finding 5).
    - What wormholes can offer is the traveller's proper-time saving (MM: about 0.16 s against about 9.4×10³ yr outside), a private channel, and quantum-gravity tests.
    - "Without negative energy" has three answers by sense: no, no, and yes for long wormholes.
  - Status: surviving (as a reframe that sharpens A rather than competing with it).
  - Distinguishing test: C predicts that any proposed time-machine protocol for a long wormhole will show an intermediate epoch with T_thru < T_ext, during which back-reaction must act. A calculation of a mouth-motion protocol that reaches a CTC with T_thru ≥ T_ext throughout (a topology or throat-length jump) would refute C's merger of the cruxes.
  - Confidence: medium-high.
- [DECOMPOSER-D] **Shortcuts (and hence time machines) are allowed in principle, because achronal ANEC fails.**
  - Claim: Urban–Olum show achronal-ANEC violation "as large as desired", and Wall's derivation fails for quantised gravitons. So L5 is unproven and possibly false, and a short one-sided wormhole could be a self-consistent shortcut.
  - Status: strained.
  - Why strained: the only violations are on fixed backgrounds, not self-consistent (Finding 11) [D-C3], [D-27]. No construction since 2016 achieves a short throat. MMP's authors argue that short throats are forbidden [D-06].
  - Distinguishing test: same as A's refutation test. D predicts that a back-reacted short throat will be found; A predicts it will not.
  - Confidence: low.
- [DECOMPOSER-E] **Classical Einstein–Dirac–Maxwell fields hold a wormhole open without exotic matter.**
  - Status: eliminated.
  - Why: the NEC must be violated at any throat [K-02], so the Dirac field is the exotic matter [D-10a]. The symmetric solutions are not solutions [D-10b]. The asymmetric ones collapse into black holes [D-11]. Positive-frequency sources give no two-ended solution [D-12].
  - Distinguishing test: a smooth, two-ended, dynamically stable EDM solution with positive-frequency sources that survives evolution, which would reopen E.
  - Confidence (in the elimination): high.
- [DECOMPOSER-F] **A long (non-shortcut) wormhole can be turned into a time machine by mouth motion while evading the achronal-ANEC crux.**
  - Status: eliminated as stated (strained if discontinuous routes are allowed).
  - Why: the lag passes (L − d)/c before (L + d)/c, so the wormhole is a shortcut first (Finding 5). For MM this needs about 8×10³ yr of lag, and about 10⁴⁹ J at 0.1c for one 2×10³⁴ kg mouth (Finding 6).
  - Distinguishing test: as in C, a CTC-forming protocol without a shortcut epoch.
  - Confidence: medium.

## What would change my mind
- **A self-consistent counterexample to achronal ANEC.** Either a back-reacted semiclassical spacetime with ANEC < 0 on a complete achronal null geodesic, or a second-order FGM 2019 result with t_min < d. Either moves D up and A down.
- **A proof covering one-sided spacetimes.** If L6 were shown false (a one-sided static shortcut with no complete achronal geodesic through it), Q1 would reopen even with L5 true.
- **An MMP instability.** A full stability analysis finding a fast growing mode would move B toward surviving.
- **A published long-wormhole time-machine protocol** with no shortcut epoch, which would split the two cruxes again (refuting C and F).

## Assumptions I relied on
- **Static mouths with exterior synchronisation (L13).** ℓ is held fixed while d varies in the MM conversion figures, which is only a scale estimate, since MM tie ℓ to d.
- **Continuity of the mouth-clock lag (L12).**
- **The Finding 4 argument** that the fastest causal curve through a one-sided shortcut throat is complete and achronal. It is adapted from Graham–Olum's Theorem 1 proof sketch and is not a published theorem for one-sided spacetimes.
- **Dossier values taken as given:** Q-02, Q-04, Q-06, Q-12 and Q-13. MM's E_bin is taken as the payload ceiling following their own ship condition [Q-03].
