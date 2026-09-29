# Research: theory
Mandate: governing theory and established results (equations, theorems, proven vs conjectured, standard references) for the problem of time.
Access: lit_search INSPIRE ok, arXiv ok (sparse hits; INSPIRE covered most), Crossref/Semantic Scholar ok; fetch_text worked on arxiv.org PDFs and the INSPIRE API (abstracts); Penrose PDF (sciencenet.cn) HTTP 403; WebFetch not used

## Claims
- [RT-01] CLAIM: In canonical GR (closed universe), the classical observables commute with the constraints and are therefore constants of motion along any foliation; the quantum analogue (state annihilated by the Hamiltonian constraint, physical matrix elements time-independent, no Schrödinger/Heisenberg distinction) is the "frozen formalism" (facet 1). Established as a property of Dirac quantization; whether it is a defect or a feature is a matter of position.
  SOURCE: Isham 1992/1993, "Canonical quantum gravity and the problem of time", NATO ASI Salamanca lectures, arXiv:gr-qc/9210011, https://arxiv.org/pdf/gr-qc/9210011
  QUOTE: "This so-called ‘frozen formalism’ caused much confusion when it was first discovered since it seems to imply that nothing happens in a quantum theory of gravity." and "an observable is automatically a constant of motion with respect to evolution along the foliation associated with any choice of lapse function N and shift vector N. This is the ‘frozen formalism’ of classical, canonical general relativity."
  ACCESS: full-text
  STATUS: textbook-or-review
  CONFIDENCE: high
- [RT-02] CLAIM: Isham's review identifies the multiple-choice problem (facet 2): there is generically no geometrically natural internal time and classically all choices have equal standing, but at the quantum level there is no reason to suppose the resulting quantum theories are equivalent. Also that Rovelli's evolving-constants scheme (facet 6) faces multiple-choice and Hilbert-space problems, judged "no worse" than other approaches.
  SOURCE: Isham 1992, arXiv:gr-qc/9210011, https://arxiv.org/pdf/gr-qc/9210011
  QUOTE: "The Multiple Choice Problem. Generically, there is no geometrically natural choice for the internal spacetime coordinates and, classically, all have an equal standing. However, this classical cornucopia becomes a real problem at the quantum level since there is no reason to suppose that the theories corresponding to..." ; "It seems most unlikely that a single Hilbert space can be used for all possible choices of an internal time function T . Thus the multiple choice and Hilbert space problems appear once more. These are real difficulties and need to be taken seriously. However, they are no worse than those that arise in any of the other approaches to the problem of time"
  ACCESS: full-text
  STATUS: textbook-or-review
  CONFIDENCE: high
- [RT-03] CLAIM: Kuchař's review "Time and interpretations of quantum gravity" (first circulated 1992; reprinted IJMPD 20 (2011) 3) critically examines ten attempts to circumvent the frozen-time problem in canonical quantum gravity and finds shortcomings in each; it is the standard source for the facet taxonomy (with Isham).
  SOURCE: Kuchař, "Time and interpretations of quantum gravity", Int.J.Mod.Phys.D 20 (2011) 3, doi:10.1142/S0218271811019347, https://inspirehep.net/literature/327212
  QUOTE: "In canonical quantization of gravity, the state functional does not seem to depend on time. This hampers the physical interpretation of quantum gravity. I critically examine ten major attempts to circumvent this problem and discuss their shortcomings."
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-04] CLAIM: Trinity theorem (Höhn-Smith-Lock 2021): for a (Dirac-quantized) system with a clock, three approaches to relational quantum dynamics are equivalent: (1) relational Dirac observables in the clock-neutral picture, (2) the Page-Wootters relational Schrödinger picture, (3) the relational Heisenberg picture from quantum symmetry reduction (quantum deparametrization). Equivalence holds under a condition that the clock is "well-behaved" (does not couple to the evolving degrees of freedom, i.e. the ideal/non-interacting clock case in the original paper), with covariant POVM clocks used to accommodate non-ideal clocks. Proven for the class of (group-)covariant clock POVMs with a constraint that is linear in the clock Hamiltonian; this is a mathematical result, not a physical resolution of the interacting-clock case.
  SOURCE: Höhn, Smith, Lock, "The Trinity of Relational Quantum Dynamics", Phys. Rev. D 104, 066001 (2021), arXiv:1912.00033, https://arxiv.org/pdf/1912.00033
  QUOTE: "Constituting three faces of the same dynamics, we call this equivalence the trinity." and "amounting to the requirement that a physical clock be “well-behaved” and does not couple to the evolving degrees of freedom, these three proposals are actually a manifestation of the same relational quantum theory"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-05] CLAIM: The trinity paper claims to answer three standard criticisms of Page-Wootters (facet 6, and Kuchař's propagator objection): PW conditional states are not constraint-violating but are the quantum analogue of a gauge-fixed description of a gauge-invariant quantity; normalization ambiguity absent; Kuchař's "wrong propagators" objection is resolved without approximations or ideal clocks, by using conditional probabilities of relational observables (not naive two-time projections). Non-monotonic realistic clocks (Unruh-Wald) handled by POVMs. This is the authors' own claim; replies in the literature (e.g. on ideal versus realistic clocks, and on the physical-Hilbert-space inner product) should be checked by the critiques facet.
  SOURCE: Höhn, Smith, Lock 2021, arXiv:1912.00033
  QUOTE: "The trinity furthermore resolves a previously reported normalization ambiguity and clarifies the role of entanglement in the PW formalism. The trinity finally permits us to resolve Kuchař’s criticism that the PW formalism yields wrong propagators by showing how conditional probabilities of relational observables give the correct transition probabilities. Unlike previous proposals, our resolution does not invoke approximations, ideal clocks or..."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-06] CLAIM: The trinity extends to relativistic settings (constraint quadratic in clock momentum, e.g. Klein-Gordon-type) only per frequency superselection sector; the clock time is then defined via a positive-frequency (positive/negative) restriction, so global time (facet 4) and inner-product (facet 3) issues survive as sector-wise, not fully removed.
  SOURCE: Höhn, Smith, Lock, "Equivalence of Approaches to Relational Quantum Dynamics in Relativistic Settings", Front. Phys. 9, 587083 (2021), arXiv:2007.00580
  QUOTE: "Here we show that this `trinity' of relational quantum dynamics holds in relativistic settings per frequency superselection sector."
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-07] CLAIM: Thermal-time hypothesis (Connes-Rovelli 1994): in a generally covariant quantum theory the time flow is not a universal property of the dynamics but is defined by the state; mathematically it is the Tomita-Takesaki modular group of the state on the observable algebra (von Neumann algebra). It reduces to ordinary Hamiltonian time for a Gibbs state of a non-covariant system. It is a hypothesis, not a theorem; the Tomita-Takesaki theorem itself is a theorem. State-dependence of time and relation to geometric time (e.g. Minkowski/Unruh) are shown only for special cases. Flow of time is "not frozen" though the system is always in equilibrium for that flow.
  SOURCE: Connes & Rovelli 1994, "Von Neumann algebra automorphisms and time-thermodynamics relation in general covariant quantum theories", Class. Quantum Grav. 11, 2899, arXiv:gr-qc/9406019
  QUOTE: "in a generally covariant quantum theory the physical time-flow is not a universal property of the mechanical theory, but rather it is determined by the thermodynamical state of the system (”thermal time hypothesis”). We implement this hypothesis by using a key structural property of von Neumann algebras: the Tomita-Takesaki theorem, which allows to derive a time-flow, namely a one-parameter group of automorphisms of the observable algebra, from a generic thermal physical state." and "If the system is not generally covariant and is in a Gibbs state, then this postulate reduces to the Hamiltonian equations"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-08] CLAIM: No-go for QFT with arbitrary-foliation evolution (facet 5, and premise 1 about QFTCS): Torre-Varadarajan show that for a free Klein-Gordon field on flat R x T^n (n>1) the canonical transformation evolving between a flat Cauchy surface and a generic final Cauchy surface cannot be unitarily implemented on the Fock space (failure of Hilbert-Schmidt condition, an ultraviolet effect). Evolution between surfaces related by an isometry is unitary; n=1 (2D) is unitary. Implication: even on a fixed flat background, Tomonaga-Schwinger "many-fingered time" unitarity fails beyond Poincare-related slices; it is a proven result for the free field, expected (not proven) to hold on Minkowski space.
  SOURCE: Torre & Varadarajan 1999, "Functional evolution of free quantum fields", Class. Quantum Grav. 16, 2651, arXiv:hep-th/9811222
  QUOTE: "We show that this canonical transformation cannot, in general, be unitarily implemented on the Fock space for free quantum fields on flat spacetimes of dimension greater than 2." and "Indeed, it is easy to see that evolution between any two Cauchy surfaces related by an isometry is unitarily implemented." and "Thus we expect that functional evolution will not be unitarily implemented on Minkowski spacetime."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-09] CLAIM: Unimodular gravity (Unruh 1989): Λ becomes an integration constant, the Hamiltonian constraint is replaced by a secondary constraint, and a time variable conjugate to Λ (four-volume time) appears, giving a nonzero Hamiltonian-like generator and a Schrödinger equation. Speculative as a quantum-gravity proposal; classically equivalent to GR with Λ as an integration constant.
  SOURCE: Unruh 1989, "A Unimodular Theory of Canonical Quantum Gravity", Phys. Rev. D 40, 1048, https://inspirehep.net/literature/24850
  QUOTE: "Einstein's theory of gravity is reformulated so that the cosmological constant becomes an integration constant of the theory, rather than a "coupling" constant. However, in the Hamiltonian form of the theory, the Hamiltonian constraint is missing, while the usual momentum constraints are still present. Replacing the Hamiltonian constraint is a secondary constraint, which introduces the cosmologic…"
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: medium
- [RT-10] CLAIM: Clock dependence in quantum cosmology (facet 2) is concretely exhibited: in a flat FLRW model with massless scalar plus perfect fluid, quantised relationally, unitarity and recollapse behaviour depend on which clock (scalar field or fluid/Lambda time) is chosen; model-specific result (Gielen & Menéndez-Pidal), not a general theorem.
  SOURCE: Gielen & Menéndez-Pidal, "Unitarity, clock dependence and quantum recollapse in quantum cosmology", Class. Quantum Grav. 39 (2022) 075011, arXiv:2109.02660
  QUOTE: "We have previously shown that requiring unitary evolution in the “fluid” time leads to a boundary condition at the singularity and generic singularity resolution, while in the volume time semiclassical states follow the classical singular trajectories. Here we analyse the third option of using the scalar field as a clock, finding further dramatic differences to the previous cases: the boundary condition arising from unitarity is now at infinity. Rather than singularity resolution, this theory features a quantum recollapse of the universe at large volume" and "We argue that using a Dirac quantisation would not resolve the issue."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: medium

- [RT-11] CLAIM: Page-Wootters (1983): treating the time parameter as unobservable makes energy obey a superselection rule (observables commute with H, so are stationary); ordinary dynamics is recovered as correlations between a system and an internal clock in a stationary (H_total|Psi>>=0) state. Conceptually this dissolves facet 1 for a system with a good clock; the price is that "dynamics" is entanglement/correlation, and for non-ideal clocks the effective evolution is only approximately unitary.
  SOURCE: Page & Wootters 1983, "Evolution without evolution: Dynamics described by stationary observables", Phys. Rev. D 27, 2885, https://inspirehep.net/literature/13239
  QUOTE: "Because the time parameter in the Schrödinger equation is not observable, energy apparently obeys a superselection rule in the same sense that charge does. That is, observables must all commute with the Hamiltonian and hence be stationary. This means that it is consistent with all observations to assume that any closed system such as the Universe is in a stationary state. We show how the observed dynamic evolution of a system can be described entirely in terms of stationary observables as a dependence upon internal clock readings."
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-12] CLAIM: Semiclassical/Born-Oppenheimer time (Kiefer-Singh 1991): expanding the full functional Wheeler-DeWitt equation in powers of the gravitational constant gives a Schrödinger equation for matter on a classical background plus correction terms in two classes: (i) breakdown of the classical background picture, (ii) quantum-gravitational corrections to the matter fields themselves; class (ii) is independent of the factor ordering of the gravitational kinetic term. Time is emergent and approximate (valid at leading orders in 1/M ~ G), not fundamental. Speculative as quantum gravity (WDW itself is unproven), but the expansion is a mathematically definite result within WDW.
  SOURCE: Kiefer & Singh 1991, "Quantum gravitational corrections to the functional Schrödinger equation", Phys. Rev. D 44, 1067, https://inspirehep.net/literature/305361
  QUOTE: "We derive corrections to the Schrödinger equation which arise from the quantization of the gravitational field. This is achieved through an expansion of the full functional Wheeler-DeWitt equation with respect to powers of the gravitational constant. The correction terms fall into two classes: One describes the breakdown of the classical background picture while the other corresponds to quantum gravitational corrections for the matter fields themselves. The latter are independent of the factor ordering which is chosen for the gravitational kinetic term."
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-13] CLAIM: The semiclassical-time derivations are not unique: different approaches to the WDW Born-Oppenheimer expansion (Kiefer-Singh; a Banks-type/Brout-type scheme; a version treating the Schrödinger equation as fundamental with time from an observer's reference frame) each give at order O(1/M) a temporal Schrödinger equation for matter in curved spacetime with quantum-gravitational corrections, but the equations and corrections differ between the approaches (checked in a closed isotropic model with a scalar field decomposed into modes). Related: nonunitarity of the correction terms is a known issue in the BO scheme (Di Gioia et al. 2021, PRD 103, 103511, title only seen).
  SOURCE: Ayala Oña, Kamenshchik, et al. 2023, "On the Appearance of Time in the Classical Limit of Quantum Gravity", Universe 9, 85, arXiv:2302.12551, https://arxiv.org/abs/2302.12551
  QUOTE: "In each of the approaches, in the order O(1/M), a temporal Schrodinger equation for matter fields in curved spacetime with quantum gravitational corrections is obtained. However, equations and corrections are different in various a..." [abstract truncated by fetch tool]
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: medium
- [RT-14] CLAIM: Matter clocks that deparametrize (Brown-Kuchař dust): coupling GR to incoherent dust makes the dust proper time and comoving coordinates canonical variables; the Hamiltonian constraint can be solved for the momentum conjugate to dust time, and quantization gives a functional Schrödinger equation whose Hamiltonian density is independent of the dust variables (so dust time separates and there is a physical Hamiltonian, the square root of a gravitational quadratic form). Cost: a privileged dynamical reference frame and time foliation is added to the theory (extra matter content), and factor-ordering ambiguities: quantum theories from the two constraint forms need not coincide. Solves facets 1 and 3 for this matter model; facet 2 persists (dust is one clock among many); facet 4 (global time) holds only while dust is non-crossing.
  SOURCE: Brown & Kuchař 1995, "Dust as a standard of space and time in canonical quantum gravity", Phys. Rev. D 51, 5600, arXiv:gr-qc/9409001, https://arxiv.org/pdf/gr-qc/9409001
  QUOTE: "The coupling of the metric to an incoherent dust introduces into spacetime a privileged dynamical reference frame and time foliation. The comoving coordinates of the dust particles and the proper time along the dust worldlines become canonical coordinates in the phase space of the system. The Hamiltonian constraint can be resolved with respect to the momentum that is canonically conjugate to the dust time. Imposition of the resolved constraint as an operator restriction on the quantum states yields a functional Schrödinger equation." and "Due to factor-ordering ambiguities, the quantum theories constructed from H↑(x) and H↑0(x) do not necessarily coincide"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-15] CLAIM: Unimodular time: in Unruh's unimodular formulation the Hamiltonian constraint is replaced by a secondary constraint that introduces Λ as an integration constant; the quantum theory has ordinary Schrödinger-form time development (time conjugate to Λ, i.e. 4-volume time) and does not obey the Wheeler-DeWitt equation. The author names the key weakness: a nondynamical background spacetime volume element must be introduced. (Replaces the partial abstract quote in RT-09.)
  SOURCE: Unruh 1989, Phys. Rev. D 40, 1048, via INSPIRE record https://inspirehep.net/literature/24850
  QUOTE: "The quantum version has a normal "Schrödinger" form of time development, and the wave function does not obey the usual "Wheeler-DeWitt" equation, making the interpretation of the theory much simpler. The small value of the cosmological constant in the Universe at present becomes a genuine question of initial conditions, rather than a question of why one of the coupling constants has a particular value. The key "weakness" of this formulation is that one must introduce a nondynamic background spacetime volume element."
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RT-16] CLAIM: Histories formulation (Hartle): generalized sum-over-histories quantum mechanics for closed systems needs neither a preferred time nor a definition of measurement. Familiar Hamiltonian QM with a preferred time is presented as an approximation valid when the universe (via its initial condition and dynamics) exhibits a classical spacetime that can supply a time. For closed cosmological spacetimes there is no preferred time, energy or covariant Hamiltonian. It dissolves facets 1 and 5 at the cost of leaving the decoherence functional, measure and the identification of a physical time to be supplied by the classical limit; it also depends on a consistent-histories interpretation (premise 8).
  SOURCE: Hartle 1992, "Space-time quantum mechanics and the quantum mechanics of space-time", Les Houches lectures, arXiv:gr-qc/9304006, https://arxiv.org/pdf/gr-qc/9304006
  QUOTE: "familiar Hamiltonian quantum mechanics with its preferred notion of time is an approximation to a more general sum-over-histories quantum mechanics of spacetime geometry that is appropriate for those epochs and those scales when the universe, as a consequence of its initial condition and dynamics, does exhibit a classical spacetime geometry that can supply a notion of t[ime]" and "for closed cosmological spacetimes there is no preferred notion of time, therefore no preferred notion of energy, therefore no covariant notion of Hamiltonian and no covariant notion of the ground state of a Hamiltonian."
  ACCESS: full-text
  STATUS: textbook-or-review
  CONFIDENCE: high
- [RT-17] CLAIM: Realistic-clock decoherence (Gambini-Porto-Pullin 2004): ordinary QM presupposes an ideal classical external clock; with realistic (finite-precision, Salecker-Wigner-bounded) clocks the evolution ceases to be unitary and a universal decoherence arises. Authors' estimate is that the rate is fast enough to eliminate the black-hole information puzzle. This is a modification-of-QM proposal (facet 7/measurement interplay); the magnitude is an estimate specific to their optimal-clock model and is disputed elsewhere (critiques/quantitative facets should check). Contrast with trinity result RT-04/05, which recovers exactly unitary relational evolution for ideal or covariant-POVM clocks.
  SOURCE: Gambini, Porto & Pullin 2004, "Realistic clocks, universal decoherence and the black hole information paradox", Phys. Rev. Lett. 93, 240401, arXiv:hep-th/0406260
  QUOTE: "When one introduces realistic clocks, quantum mechanics ceases to be unitary and a fundamental mechanism of decoherence of quantum states arises. We estimate the rate of universal loss of unitarity using optimal realistic clocks. In particular we observe that the rate is rapid enough to eliminate the black hole information puzzle"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-18] CLAIM: Postquantum classical gravity (Oppenheim): a consistent theory of classical spacetime coupled to quantum matter with dynamics linear in the density matrix, completely positive and trace preserving, reducing to GR in the classical limit; the price is that the theory must be fundamentally stochastic in both the metric and the matter, i.e. it modifies the dynamical laws of QM (denies premise 7 that gravity must be quantized). Time is then the classical spacetime's time (background-like, with stochastic fluctuations), so it removes the frozen-formalism problem rather than solving it. Speculative; empirically distinguishable via metric-noise and decoherence-rate bounds (quantitative facet).
  SOURCE: Oppenheim 2023, "A Postquantum Theory of Classical Gravity?", Phys. Rev. X 13, 041040, arXiv:1811.03116
  QUOTE: "The assumption that general relativity is classical necessarily modifies the dynamical laws of quantum mechanics – the theory must be fundamentally stochastic in both the metric degrees of freedom and in the quantum matter fields." and "the pathologies of the semiclassical Einstein’s equations have nothing to do with treating one system classically, and everything to do with taking expectation values, and thus losing sight of correlations."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-19] CLAIM: Non-monotonic realistic clocks (Unruh-Wald problem, facet 4 in quantum form) are addressed in the trinity framework by covariant POVMs, which the authors state "resolve the non-monotonicity issue of realistic quantum clocks reported by Unruh and Wald." This is a claim by the authors of the trinity paper; it treats non-ideal clocks with a constraint linear in the clock Hamiltonian.
  SOURCE: Höhn, Smith, Lock 2021, arXiv:1912.00033
  QUOTE: "we develop a quantization procedure for relational Dirac observables using covariant POVMs which encompass non-ideal clocks and resolve the non-monotonicity issue of realistic quantum clocks reported by Unruh and Wald."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: medium
- [RT-20] CLAIM: Kuchař's third criticism, as restated in the trinity paper, is that the PW conditional probability for two times, Prob(q' when τ' | q when τ), gives the wrong propagator; the trinity paper defines a new two-time conditional probability from relational Dirac observables in the clock-neutral picture that, on reduction, gives the correct transition probabilities. The paper also lists (criticism 2) that the naive PW effect operator e_T(τ)⊗e_S(f) does not commute with the constraint and so throws |ψ_phys> out of the physical Hilbert space, which the paper argues is a misreading. Toy-model check of this is assigned to the idealizer/math checkers.
  SOURCE: Höhn, Smith, Lock 2021, arXiv:1912.00033, Sec. VIII.C
  QUOTE: "Such an effect operator does not commute with the constraint operator ĈH, and thus the measurement throws |ψphys⟩ out of the physical Hilbert space. The Page-Wootters formalism would thus be based on a postulate that violates the constraint. 3. Wrong propagators: When applied to answering the fundamental dynamical question — ‘If one finds the system at position q at time τ, what is the probability of finding it at position q′ at time τ′?’" and "We introduce a new two-time conditional probability using relational observables at the level of the a priori clock-neutral picture."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

## Gaps
- Pauli's theorem (no self-adjoint time operator conjugate to a semibounded H), and the Wheeler-DeWitt/ADM constraint algebra (Dirac algebra, Hořava-Lifshitz, shape dynamics/CMC time): not fetched this run; state only from the brief as a lead, not as a claim.
- Banks 1985 and Brout-Venturi: no accessible full text found; only Kiefer-Singh abstract and Ayala Oña et al. abstract used. Di Gioia et al. 2021 (nonunitarity in BO corrections) seen only as a reference title.
- Penrose 1996 (gravity-induced collapse, time-translation ambiguity of superposed spacetimes) and Diósi 1987: Penrose PDF returned HTTP 403; no quote obtained. Diósi-Penrose bounds belong to the quantitative facet.
- Not searched: Rovelli 1991 / Dittrich partial-complete observables, Barbour timeless, causal sets, Hořava-Lifshitz, holographic time, Smith-Ahmadi quantum clocks paper; Giovannetti-Lloyd-Maccone; Unruh-Wald 1989 paper itself (only cited via trinity paper).
- No fetch of Kuchař's full text; only the abstract; his specific "conditional probability" objections are recorded secondhand via the trinity paper (RT-20), to be checked by the critiques facet.
