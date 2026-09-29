# Research: theory
Mandate: governing theory and established results for Alcubierre-type warp drives: metric, energy conditions, quantum inequalities, horizons, causality, theorems.
Access: lit_search INSPIRE ok, arXiv ok; fetch_text.py on arxiv.org PDFs ok; WebFetch domains that worked: none used

## Claims
- [RT-01] CLAIM: Alcubierre (1994) metric in 3+1 form is ds² = -dt² + (dx - v_s f(r_s) dt)² + dy² + dz² (G=c=1), f = tanh-type top-hat with parameters R (radius) and σ (steepness); Eulerian observers (normal to t=const) see an energy density T_αβ n^α n^β = -(1/8π)(v_s² ρ²/(4 r²))(df/dr_s)² which is nowhere positive, so the weak and dominant energy conditions fail (and Alcubierre says SEC fails too). Alcubierre himself notes QFT permits negative energy (Casimir).
  SOURCE: Alcubierre M. 1994, "The warp drive: hyper-fast travel within general relativity", Class. Quantum Grav. 11 L73, https://arxiv.org/pdf/gr-qc/0009013
  QUOTE: "ds2 = −dt2 + ( dx − vs f (rs) dt ) 2 + dy2 + dz2" ; "The fact that this expression is everywhere negative implies that the weak and dominant energy conditions are violated. In a similar way one can show that the strong energy condition is also violated." ; "We see then that, just as it happens with wormholes, one needs exotic matter to travel faster than the speed of light."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-02] CLAIM: Eulerian-observer energy density is T^tt = -(v²/32π)[(∂f/∂x)² + (∂f/∂y)²] (G=c=1; x,y transverse to motion in that paper's z-axis convention), distributed in a toroid around the axis of travel; total energy is E = -(1/12) v_b² ∫ r² (df/dr)² dr for a spherically symmetric f (Pfenning-Ford form, geometric units). Scaling: E ∝ v², ∝ R², ∝ 1/(wall thickness) [Lobo-Visser: E ~ -v²R²σ for tanh profile in the large-σR limit].
  SOURCE: Lobo & Visser 2004, "Fundamental limitations on 'warp drive' spacetimes", Class. Quantum Grav. 21 5871, https://arxiv.org/pdf/gr-qc/0406083 ; Pfenning & Ford 1997, Class. Quantum Grav. 14 1743, https://arxiv.org/pdf/gr-qc/9702026
  QUOTE: (Lobo-Visser) "Tµν Uµ Uν = − v2 32π [ ( ∂f ∂x ) 2 + ( ∂f ∂y ) 2] < 0" ; "Note that the energy requirements for the warp bubble scale quadraticall y with bubble velocity, quadratically with bubble size, and inversely as the thickness of the bubble wall." (Pfenning-Ford) "E = − 1 12 v2 b ∫ ∞ 0 r2 ( d f (r) dr ) 2 dr (26)"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-03] CLAIM: The Alcubierre spacetime violates the NEC (not just WEC), for all v: the direction-averaged null-energy along the axis of motion is -(v²/8π)[(∂f/∂x)² + (∂f/∂y)²] < 0. Even un-averaged, a term linear in v means NEC is violated in one of the two null directions at arbitrarily low v. Lobo-Visser also show the same holds for the Natário warp drive (non-perturbative NEC/WEC violation, persisting to arbitrarily low speed), and that even at low speed the net negative energy in the field must be a significant fraction of the ship's mass in a linearized treatment.
  SOURCE: Lobo & Visser 2004, Class. Quantum Grav. 21 5871, https://arxiv.org/pdf/gr-qc/0406083
  QUOTE: "which is manifestly negative, and so the NEC is violated for a ll v." ; "For both the Al cubierre and Nat´ ario warp drives we ﬁnd that even at low speeds the net (negative) energy stored i n the warp ﬁelds must be a signiﬁcant fraction of the mass of the spaceship."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-04] CLAIM: Pfenning-Ford (1997) apply the Ford-Roman quantum inequality (QI) to the Alcubierre wall in a locally flat patch and find the wall thickness is only Δ ≲ 10² v_b Planck lengths for a chosen α = 1/10 (their Eq. 22 bound involves α, the ratio of sampling time to minimum radius of curvature; SCOPE: order-of-magnitude, uses the 4D free massless scalar QI with sampling time short vs. radius of curvature, and Δ defined by their linear-ramp shape function); total energy for R = 100 m is then E ≈ -6.2e65 v_b grams ~ -3e20 M_galaxy v_b (their units: 1e12 M_sun = 2e45 g). Increasing v_b thickens the wall but energy still grows ∝ v_b² /Δ ~ v_b (net linear in v_b at fixed R).
  SOURCE: Pfenning & Ford 1997, "The unphysical nature of 'warp drive'", Class. Quantum Grav. 14 1743, https://arxiv.org/pdf/gr-qc/9702026
  QUOTE: "∆ ≤ 102 vb LP lanck , (23) where LP lanck is the Planck length. Thus, unless vb is extremely large, the wall thickness cannot be much above the Planck scale." ; "E ≤ −6. 2 × 1070 vb LP lanck ∼ − 6. 2 × 1065 vb grams. (29)" ; "the energy required for a warp bubble is on the order of E ≤ −3 × 1020 Mgalaxy vb . (31)"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-05] CLAIM: Olum (1998) theorem: with a definition of superluminal travel that requires a path to reach a destination surface earlier than any neighbouring path, and assuming the generic condition and no singularities, superluminal travel requires weak-energy-condition violation (proof goes via the Raychaudhuri equation for a null geodesic, i.e. it is really a violation of R_ab K^a K^b >= 0 along the path). Scope: classical GR; "generic condition" holds whenever there is any normal matter or transverse tidal force on the path; it also shows a flat-space-in-odd-coordinates example is not superluminal, which limits what counts as a genuine warp drive.
  SOURCE: Olum K.D. 1998, "Superluminal travel requires negative energies", Phys. Rev. Lett. 81, 3567, https://arxiv.org/pdf/gr-qc/9805003
  QUOTE: "With this deﬁnition (and assuming the generic condition) I prove that superluminal travel req uires weak-energy- condition violation." ; "The generic condition holds whenever there is any normal matter or any transverse tidal force anywhere on P ."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-06] CLAIM: Ford-Roman quantum inequality (QI) for the free massless scalar field in 4D Minkowski: the energy density averaged along an inertial observer's worldline with Lorentzian sampling of width t0 obeys ρ̂ ≡ (t0/π)∫⟨T00⟩dt/(t²+t0²) ≥ -3/(32π² t0⁴) (natural units ħ=c=1), for all t0. Massive scalar bound is -3G(y)/(32π² t0⁴) with G→1 as m→0; the electromagnetic bound is a factor 2 more negative. SCOPE: free fields, flat spacetime, inertial observer; proven for these fields, not a general theorem for interacting fields or curved backgrounds. In SI, the magnitude is ħc·3/(32π² (c t0)⁴).
  SOURCE: Ford & Roman 1997, "Restrictions on negative energy density in flat spacetime", Phys. Rev. D 55, 2082, https://arxiv.org/pdf/gr-qc/9607003
  QUOTE: "ˆρ ≡ t0 π ∫ ∞ −∞ ⟨T00⟩dt t2 +t2 0 ≥ − 3 32π2t04, (1) for all choices of the sampling time, t0." ; "the right-hand side of the bound in the electromagnetic ﬁeld ca se is smaller (i.e., more negative) by a factor of 2."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-07] CLAIM: Quantum interest: QFT permits negative energy density but a negative pulse must be followed by a compensating positive pulse with separation inversely proportional to amplitude; the "quantum interest conjecture" (positive pulse must overcompensate, by an amount increasing with separation) is PROVEN by Ford and Roman only for delta-function pulses of massless scalar fields in 2D and 4D flat spacetime; beyond that it remains a conjecture. This bounds duration of negative-energy pulses and means sustained (steady-state) negative energy from generic QFT states is not available.
  SOURCE: Ford & Roman 1999, "The quantum interest conjecture", Phys. Rev. D 60, 104018, https://arxiv.org/pdf/gr-qc/9901074
  QUOTE: "Although quantum ﬁeld theory allows local negative energy d ensities and ﬂuxes, it also places severe restrictions upon the magnitud e and extent of the negative energy." ; "we prove that the conjecture is indeed true, at least for δ-function pulses composed of massless scalar ﬁelds in Minkowski spacetime."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-08] CLAIM: Horizon / control problem: an observer at the centre of an Alcubierre bubble with v > c is causally separated from the bubble wall, so cannot create or steer the bubble on demand; Everett-Roman generalize Krasnikov's 2D tube (a pre-laid track along the path, flat inside, light cones opened for one-way superluminal travel) to 4D, showing that a single tube has no closed timelike curves but two non-overlapping tubes make a time machine, and that tubes also need unphysically thin layers of negative energy density. Krasnikov tubes are outside the brief's scope except as infrastructure/reframe.
  SOURCE: Everett & Roman 1997, "A superluminal subway: the Krasnikov tube", Phys. Rev. D 56, 2100, https://arxiv.org/pdf/gr-qc/9702049
  QUOTE: "Hence such an observer can n either create a warp bubble on demand nor control one once it has been created ." ; "a time machine can be con structed with a system of two non-overlapping tubes. Furthermore, it is de monstrated that Krasnikov tubes, like warp bubbles and traversable wormhol es, also involve un- physically thin layers of negative energy density"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-09] CLAIM: Causality: Everett (1996) exhibited a simple modification of the Alcubierre metric that contains closed causal loops, verifying Alcubierre's conjecture (details of the modification not read; abstract only). Chronology protection (Hawking) is a CONJECTURE, not a theorem, and is not proven to forbid this; whether CTC arise depends on assuming a bubble can be produced at will.
  SOURCE: Everett A.E. 1996, "Warp drive and causality", Phys. Rev. D 53, 7365 (INSPIRE abstract; abstract only)
  QUOTE: "Alcubierre recently exhibited a spacetime which, within the framework of general relativity, allows travel at superluminal speeds if matter with a negative energy density can exist, and conjectured that it should be possible to use similar techniques to construct a theory containing closed causal loops and, thus, travel backwards in time. We verify this conjecture by exhibiting a simple modiﬁcation"
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-10] CLAIM: Semiclassical instability (Hiscock 1997): for a conformally invariant scalar field in a 2D reduction of the Alcubierre metric, <T_μν> is regular for v < c, but diverges (near the horizon that forms when the apparent speed exceeds c; leading term <ρ> ~ -(f')²/(48π)[f-(1-1/v0)]^-2) for v > c; interpreted as Hawking-like flux from the horizon. SCOPE: 2D, free conformal scalar, eternal-warp-drive state; author says "if the instability is not an artifact of working in two dimensions" backreaction would preclude v > c.
  SOURCE: Hiscock W.A. 1997, "Quantum effects in the Alcubierre warp drive spacetime", Class. Quantum Grav. 14 L183, https://arxiv.org/pdf/gr-qc/9707024
  QUOTE: "The stress-energy is foun d to diverge if the apparent velocity of the spaceship exceeds the speed of ligh t. If such behav- ior occurs in four dimensions, then it appears implausible t hat “warp drive” behavior in a spacetime could be engineered, even by an arbit rarily advanced civilization."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-11] CLAIM: Finazzi-Liberati-Barceló (2009) treat a warp drive created from initially flat spacetime (dynamical, 2D-type analysis of a quantum field's RSET): an observer at the bubble centre would generically see a thermal Hawking flux; the flux is "extremely high" if the exotic matter comes from a quantum field obeying QIs; and the RSET grows exponentially in time near/on the front wall of a superluminal bubble, so warp drives are unstable to semiclassical backreaction. SCOPE: superluminal case (horizons form); subluminal bubbles have no horizon; result rests on a specific model (2D/quantum scalar field in the RSET calculation) and a Boulware-like vacuum, not a full 4D self-consistent solution.
  SOURCE: Finazzi, Liberati, Barceló 2009, "Semiclassical instability of dynamical warp drives", Phys. Rev. D 79, 124017, https://arxiv.org/pdf/0904.0141
  QUOTE: "an observer located at the center of a superluminal warp-drive bubble wo uld generically experience a thermal ﬂux of Hawking particles. On the other side, such Hawking ﬂux will be generically extremely high if the exotic matter supporting the warp drive has its origin in a quantum ﬁeld satisfying some form of quantum inequalities. Most of all, we ﬁnd that the RSET wil l exponentially grow in time close to, and on, the front wall of the superluminal bubble. Conseq uently, one is led to conclude that the warp-drive geometries are unstable against semiclassical backreaction."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-12] CLAIM: Visser-Bassett-Liberati (VBL) argue perturbatively (linearized gravity about Minkowski) that the NEC forces light cones to narrow, so Shapiro delay is a delay not an advance and NEC-obeying matter cannot give effective FTL; Gao & Wald (2000) objected that comparing light cones to a background is gauge dependent; Barceló et al. 2023 argue both are correct in different paradigms (VBL fits a non-geometric "harmonic background" paradigm). So the NEC-violation requirement is a theorem in the Olum (gauge-invariant path-arrival) form, and a perturbative result in the VBL form; neither is a QFT statement.
  SOURCE: Visser, Bassett & Liberati 2000, Nucl. Phys. B (Proc. Suppl.) 88, 267, https://arxiv.org/pdf/gr-qc/9810026 ; Barceló et al. 2023/2024, "The harmonic background paradigm, or why gravity is attractive", Gen. Rel. Grav. 56, 116, https://arxiv.org/pdf/2307.11472
  QUOTE: (VBL) "the NEC forces the light cones to contract (narrow). Given the NE C, the Shapiro time delay in any weak gravitational ﬁeld is always a delay relative to the Minkowski background, and never an advance." (Barceló) "Their result was soon challenged by Gao and Wald [Cl ass. Quantum Grav. 17, 4999, (2000)] who argued that this relation is gauge dependent and therefore lacks physical signiﬁcance. In this paper, we clear up this controversy by showing that bo th papers are correct but need to be interpreted in distinct paradigms."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-13] CLAIM: Natário (2002) zero-expansion warp drive: a shift X with ∇·X = 0 carries the bubble with no contraction/expansion of the Eulerian volume element; the Eulerian energy density in the ADM form is ρ = (1/16π)(θ² − K_ij K^ij) with θ = ∇·X, so for θ = 0, ρ = −K_ij K^ij/(16π) ≤ 0, zero only if K_ij ≡ 0. Natário proves that a warp drive spacetime (flat Cauchy surfaces, this class) cannot satisfy both the weak and strong energy conditions; his spherical example has ρ = −(v_s²/8π)[3(f')² cos²θ + (f' + r f''/2)² sin²θ] (G=c=1, polar angle θ from the axis; f is his profile). So zero expansion does not remove the negative Eulerian energy; it changes its distribution/magnitude.
  SOURCE: Natário J. 2002, "Warp drive with zero expansion", Class. Quantum Grav. 19, 1157, https://arxiv.org/pdf/gr-qc/0110086
  QUOTE: "Thus if θ = 0 we have ρ ≤ 0, and ρ = 0 iﬀ Kij ≡ 0." ; "yielding the energy density (as measured by Eulerian observ ers) ρ = − 1 16π KijK ij = − v2 s 8π [ 3(f ′)2 cos2 θ + ( f ′ + r 2 f ′′ ) 2 sin2 θ ]"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-14] CLAIM: Van Den Broeck (1999) modifies Alcubierre's spatial metric so a tiny-neck bubble (outer surface radius R ~ 3e-15 m, inner wall Δ̃ ~ 1e-15 m, α = 1e17, pocket of ~100 m proper size inside) reduces total negative mass to "a few solar masses" (SI: E_II,+ = 4.9e30 kg positive; negative comparable, ~few M_sun = few 2e30 kg), for v_s of order c. SCOPE: his own parameter choices for v_s ≈ 1 (v ~ c), and he checks the Ford-Roman QI for Eulerian observers (which parameter plays the role of the ≲1e2 v_s L_P wall was not resolved here); he states the geometry "still has structure with sizes only a few orders of magnitude above the Planck scale; this seems to be generic for spacetimes allowing superluminal travel", and that generating enough negative energy is unresolved. The negative energy density is still huge (tiny wall).
  SOURCE: Van Den Broeck C. 1999, "A 'warp drive' with reasonable total energy requirements", Class. Quantum Grav. 16, 3973, https://arxiv.org/pdf/gr-qc/9905084
  QUOTE: "A spacetime is pre sented for which the total negative mass needed is of the order of a few so lar masses, accompanied by a comparable amount of positive energy." ; "Both EII, − and EII, + are in the order of a few solar masses." ; "the geometry still has structure with si zes only a few orders of magnitude above the Planck scale; this seems to be generic fo r spacetimes allowing superluminal travel."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-15] CLAIM: Consensus status of the energy-condition question (Santiago-Schuster-Visser 2022, a critique of Lentz, Bobrick-Martire and Fell-Heisenberg): they say those three papers only assert, and do not prove, that comoving Eulerian observers are the relevant set; in their framework all physically reasonable warp drives violate the WEC and the strong and dominant energy conditions, and under plausible subsidiary conditions also the NEC. Known prior results they list: Alcubierre drives violate WEC and NEC; Natário zero-expansion drives violate WEC; generic Natário drives violate DEC and either SEC or WEC. Caveat: their NEC result is conditional on "plausible subsidiary conditions" (not unconditional) and the general theorem is Olum's; positive-energy claims (Lentz etc.) are covered by the critiques/frontier facets.
  SOURCE: Santiago, Schuster & Visser 2022, "Generic warp drives violate the null energy condition", Phys. Rev. D 105, 064038, https://arxiv.org/pdf/2105.03079
  QUOTE: "within the framework adopted by those three papers all physically reasonable warp drives will certainly violate the WEC, and both the strong and dominant energy conditions. Under plausible subsidiary conditions the null energy condition is also violated." ; "While warp drives are certainly interesting examples of speculative physics, the violation of the energy conditions, at least within the framework of standard general relativity, is unavoidable."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-16] CLAIM: QFT status of "negative energy is allowed but limited": pointwise energy conditions fail in QFT, but averaged conditions hold in restricted settings. Wald & Yurtsever proved the averaged null energy condition (ANEC) for Hadamard states of a massless scalar in any globally hyperbolic 2D spacetime along complete achronal null geodesics (and results for 4D Minkowski), and argued ANEC cannot hold for all states of a massless field in all 4D spacetimes; ANEC is thus a theorem only under those hypotheses (complete, achronal null geodesic), which is why the brief treats it as usable "where assumptions hold". Kontou & Sanders review: Olum proved a warp drive cannot satisfy the WEC; Alcubierre bubble necessarily involves causality violations (Everett).
  SOURCE: Kontou & Sanders 2020, "Energy conditions in general relativity and quantum field theory", Class. Quantum Grav. 37, 193001, https://arxiv.org/pdf/2003.01815
  QUOTE: "Wald and Yurtsever [20] proved that the AANEC holds for all Hadamard states of a massless scalar ﬁeld in any globally hy- perbolic, two-dimensional spacetime along any complete, achronal null geodesic." ; "In four dimensions, Wald and Yurtsever [20] argued that the ANEC cannot hold for all states of a massless ﬁeld in all spacetimes." ; "Olum [180] proved that it is not"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high
- [RT-17] CLAIM: Hidden-premise check (theory side): the Eulerian frame is convenient but the theorems concern all observers/null vectors. For the Alcubierre class the NEC along ±axis contains a term linear in v (RT-03), so NEC violation appears at any speed including v<c; superluminality is not needed to require negative energy, but superluminality (Olum) makes it unavoidable in a gauge-invariant sense. Conversely Olum's proof requires a null-geodesic congruence with no conjugate points and the generic condition; a metric that only "looks" superluminal (his flat-space-in-odd-coordinates example) does not need negative energy. Any positive-energy warp claim must therefore be subluminal (or not truly superluminal in Olum's sense), or hide a WEC/NEC violation for some other observers (the point Santiago et al. press). [our synthesis of RT-03, RT-05, RT-15]
  SOURCE: synthesis of Lobo & Visser 2004; Olum 1998; Santiago et al. 2022 (see RT-03, RT-05, RT-15)
  SUMMARY: "Derived from cited quotes above, not a new source."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: medium

## Gaps
- Not opened this run: Ford-Roman QI for curved backgrounds and Fewster's general QEI results (Fewster 2012 "Lectures on quantum energy inequalities", arXiv:1208.5399, only cited in Santiago et al.); the exact formula behind Pfenning-Ford Eq. (22) (the coefficient and the meaning of α); numeric Pfenning-Ford QI wall bound in metres (the smoke-test note gives ~51 Planck lengths at R=100 m, Δ convention differs - not rechecked here).
- Hawking chronology protection and Everett's specific CTC construction: only the abstract of Everett 1996 was seen; no primary source for Hawking's conjecture retrieved.
- McMonigal-Lewis-O'Byrne (effects on particles the bubble meets), Clark-Hiscock-Larson null geodesics (horizon structure), tidal forces: left to other facets (critiques/quantitative).
- Gao & Wald 2000 original not opened (only Barceló et al. 2023's account of it).
- The positive-energy claims (Lentz, Bobrick-Martire, Fell-Heisenberg) were not studied here beyond their critique in RT-15.
- lit_search results: INSPIRE ok; arXiv search returned results too but the arXiv API was not rate-limited; PDFs fetched via fetch_text.py all ok. WebSearch not used.

