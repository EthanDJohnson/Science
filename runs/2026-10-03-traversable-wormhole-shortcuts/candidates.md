# Candidate answers
exclusive: no (feasibility options plus reframes. C2 (long, non-shortcut wormholes), C6 (narrower ban), C7 (clock offset) and C8 (two-sided bookkeeping) can all hold together with the null C1. C3, C4 and C5 each contradict part of C1: C3 and C4 its no-shortcut leg, C5 its no-support-without-negative-energy leg)
lenses merged: decomposer, examiner, mechanist, dialectician, idealizer, engineer, constraints (analyses/*.md), each read against its math check in math/*.md (refuted items: M-DECOMPOSER-08, M-DECOMPOSER-09, M-MECHANIST-05, M-MECHANIST-06, M-IDEALIZER-07)
status: final

Units: SI unless marked; "geometric" means G = c = 1 (lengths in m); "natural" means ħ = c = 1. T_thru is the earliest arrival through the throat, T_ext is the exterior light-travel time, and Δ is the lag of one mouth's clock behind exterior-synchronised time.

## C1: No viable option: no admissible traversable wormhole beats light through the exterior or its coupling channel, none stays open without negative null energy, and none could pass 1 kg in practice.
type: null
from: EXAMINER-A, MECHANIST-A, IDEALIZER-A, CONSTRAINTS-A, DIALECTICIAN-A, DIALECTICIAN-E, ENGINEER-A, DECOMPOSER-A (its no-shortcut half), DECOMPOSER-B (as the strongest variant), IDEALIZER-D, DIALECTICIAN-C, MECHANIST-C (its Q2 half), CONSTRAINTS-C (its sense-by-sense reading of "negative energy")
argument: The null has three legs.
- **(i) No shortcut (Q1).**
  - *One-sided constructions on record.* Every one has T_thru/T_ext ≥ 1.
    - MM 2020: T_thru = πℓ/c = 9.42×10³ yr, so T_thru/T_ext = π at d = ℓ, 31 at 0.1ℓ and 314 at 0.01ℓ [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-examiner_shortcut.py; M-EXAMINER-04 verified]. MM write "the time through the wormhole is always longer than through the outside, π𝓁 > d" [new: Maldacena & Milekhin, arXiv:2008.06618 p. 7, ACCESS full-text].
    - MMP: transit/d > 2 [Q-12].
    - FGM 2019: t_min = d + logs, approaching 1 from above but not crossing it [Q-13].
    - For each, the throat geodesic is chronal by a positive margin (MM: T_thru/T_ext = 3.15 to 9425 for d = 2990 to 1 ly) [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-constraints_perturbative.py; M-CONSTRAINTS-13 verified].
  - *Two-sided constructions.* Nothing arrives earlier than the boundary coupling, or without it.
    - GJW: nothing passes when decoupled [D-01]. The message must be inserted R ln(R/(h l_P)) ≈ 4.6R to 138R before the coupling (R/l_P = 10² to 10⁶⁰, h = 1) [calc: lens-examiner_shortcut.py; M-EXAMINER-08]. The coupling makes the throat geodesics "no longer achronal" [new: Gao, Jafferis & Wall, arXiv:1608.05687v3, ACCESS full-text].
    - MSY: "a few bits", a parametric bound [D-02, K-15].
    - Maldacena–Qi: the ANEC was reproduced in JT gravity, ∫T_kk dλ = −φ_r/(4πG) = −2φ_r/(8πG), and the ray is chronal in the coupled system [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-constraints_perturbative.py; M-CONSTRAINTS-11 verified, convention mapping to MQ unchecked].
  - *Shortcut geometries.* They exist only as designer classical geometries (C4), which need achronal-ANEC violation or labelled phantom matter and are unstable.
  - *Why the published constructions are long.* The self-consistent achronal ANEC conjecture forbids negative ANEC on a complete achronal null geodesic [K-07a]. Achronal ANEC is proved for general QFTs in AdS₂×S^{d−2} [new: Rosso 2020, JHEP 07 (2020) 023, arXiv:2005.06476, ACCESS abstract], so the MMP/MM throat cannot carry such a violation on its own.
- **(ii) No support without negative energy (Q2).**
  - *Pointwise:* NEC violation at or near any throat is a theorem [K-02].
  - *ANEC on some complete null geodesic:* forced for asymptotically flat, globally hyperbolic traversable wormholes [K-01].
  - *Every static, spherical, horizon-free two-ended throat:* the radial ANEC is strictly negative, whatever the matter: I = −(E/4π)∫e^{−Φ}(r′/r)² dl < 0 (geometric) [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-constraints_ec_table.py; M-CONSTRAINTS-02 verified].
  - *The post-2016 constructions:* GJW, MQ, FGM, MMP and MM all use Casimir-type negative null energy of ordinary quantum fields [D-01, D-04 to D-08], so "ordinary matter" does not mean "no negative energy".
  - *Observer dependence.* The WEC violation is forced through the NEC, but a static observer can still see positive energy density. In a Morris–Thorne family with b = r₀(1 + α(1 − r₀/r)), ρ > 0 everywhere, yet a radially moving observer at the throat measures negative energy for v > √α c (0.7071c at α = 0.5) [calc: lens-constraints_ec_table.py; M-CONSTRAINTS-03]. So "negative energy density" can be confined to fast observers, while the negative null energy cannot be removed.
  - *The only open sense:* "without negative energy" holds only for achronal ANEC, and only for long wormholes [K-07f].
- **(iii) No payload in practice (about 100 yr).**
  - *The cheapest real-universe row is the Standard-Model MMP pair.* It needs magnetic charge, which has never been observed [D-25]. Pair creation needs a field 34.2 orders above the 1200 T pulsed record. The pair's rest energy, 4.8×10²⁵ J, equals about 8×10⁴ years of world primary energy. A 1 kg payload needs 24.2 to 29.1 more orders of binding energy [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-engineer_cost_table.py; M-ENGINEER-05, M-ENGINEER-07, M-ENGINEER-09 verified; the 1200 T anchor is [new: physicsworld.com, ACCESS search-summary]].
  - *A human* needs MM's labelled speculative sector (C2).
  - *The classical rows* are 38 to 57 orders from demonstrated negative energy (C4).
- **Strongest variant (DECOMPOSER-B, strained).** No traversable wormhole is realisable in our universe at all.
  - Every 4D asymptotically flat row is unstable, transient, speculative or not a solution.
  - MMP's stability is unproven [D-C5, F-01].
predictions:
- *If true:*
  - every future self-consistent semiclassical one-sided solution has Δ_B = t_B(exterior) − t_B(throat) ≤ 0, for a single emission event read on one clock at B (the examiner's synchronisation-free test);
  - FGM-type t_min − d stays ≥ 0 at higher order;
  - no two-sided protocol passes more qubits than the bits its coupling exchanges;
  - the in-practice gaps stay above about 5 orders for every row.
- *If false:* a back-reacted solution with T_thru < T_ext, or a stable shortcut supported by admissible fields.
evidence for: [K-01] [K-02] [K-07] [D-01]–[D-08] [D-27]; MM's "π𝓁 > d" quote; Rosso 2020 (abstract); the shortcut test table [calc: lens-examiner_shortcut.py]; the energy-condition table [calc: lens-constraints_ec_table.py, lens-constraints_perturbative.py]; the cost table [calc: lens-engineer_cost_table.py]. All of these math checks are verified.
evidence against:
- *The in-principle leg rests on a conjecture.* The self-consistent achronal ANEC is a conjecture [K-07a, D-C3]. Wall's derivation fails once gravitons are quantised [K-07c].
- *The one-sided extension is an argued step, not a theorem.* Graham–Olum's wormhole theorem assumes simple connectedness [new: Graham & Olum 2007, arXiv:0705.3193 p. 5, ACCESS full-text]. The lenses' bridge "one-sided shortcut ⇒ complete achronal throat geodesic" was **refuted** for misaligned mouths (M-DECOMPOSER-08; see C6). So the null's Q1 leg in principle rests on the conjecture plus that unproved step.
- *The strong variant is strained.* MMP is a peer-reviewed self-consistent perturbative 4D solution [D-06], so the DECOMPOSER-B variant fails unless an MMP instability is shown.
decisive test:
- *What:* a second-order (back-reacted) computation of FGM 2019's minimum transit time, to see whether t_min − d stays ≥ 0. Alternatively, a self-consistent semiclassical solution with ANEC < 0 on a complete achronal null geodesic, which would refute the null.
- *Who:* semiclassical-gravity theorists, using FGM's perturbative methods [D-07].
- *Precision:* the sign of t_min − d at second order.
- *When:* no date is known.
- *In practice:* any detection of macroscopic magnetic charge, or a laboratory QEI violation in J/m³, would reopen the practice leg; neither is scheduled [D-25, D-C6].

## C2: Long 4D wormholes held open by quantum-field Casimir energy on chronal null lines (MMP, FGM 2019, MM) are traversable in principle but never shortcuts; Standard-Model fields pass only qubit-scale signals.
type: option
from: DECOMPOSER-A (support half), CONSTRAINTS-B, ENGINEER-B, ENGINEER-C, ENGINEER-G, IDEALIZER-E, EXAMINER-B (proper-time half), DECOMPOSER-C (proper-time half), MECHANIST-C, DIALECTICIAN-C
argument:
- **Why they are allowed.**
  - *Chronal throat lines.* The ANEC-violating null lines are chronal: field-line circles in MMP, whose ANEC per loop is −πc/(3L) (natural) [calc: lens-constraints_perturbative.py; M-CONSTRAINTS-12]. The throat crossing has T_thru > T_ext, which is Graham–Olum's own long-wormhole counterexample [new: Graham & Olum 2007, p. 5–6, ACCESS full-text, "We can still find fastest paths through the wormhole, but they are chronal."]. So the conjecture does not touch them [K-07f, D-27].
  - *Flat-space QIs don't apply.* The sampling time 0.01 r_e exceeds the magnetic length l_B = r_e√(2/q) by 3.3×10⁵ to 2.8×10¹⁸ [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-constraints_qi.py; M-CONSTRAINTS-10, lower end corrected from about 10⁶].
  - *The EFT no-go is escaped.* The near-extremal EFT no-go [K-18] is avoided through Casimir energy.
- **Sub-hypothesis (a): MMP with Standard-Model fields (established fields plus magnetic charge).**
  - *Size and charge.* r_e ≲ 1/TeV ≈ 2×10⁻¹⁹ m [Q-11]; each mouth 2.7×10⁸ kg. Flux q = 4.1×10¹⁴ at hypercharge g = 0.06 (engineer), or 2.1×10¹⁵ at g = e (constraints).
  - *Throat.* Length 2.1 cm to 1.1 m (engineer, N_eff = 54 to 1), or 0.23 m with external transit 2.4 ns (constraints, N_f = 1).
  - *Binding.* |E_min| = 4.5 MeV to 13 GeV (engineer), or 113 MeV (constraints). So only single quanta below about 10⁸ eV pass.
  - *Temperature.* The environment must be colder than 0.3 to 17 mK (engineer), or 9.9 mK (constraints).
  - *Sources.* [calc: lens-engineer_cost_table.py; lens-constraints_budgets.py; M-ENGINEER-05, M-CONSTRAINTS-16 verified]. The coupling and N-scaling readings are the lenses' own assumptions.
  - *Widening lowers capacity.* At fixed fields |E_min| = g²ħc/(256π r_e) (M-ENGINEER-01).
- **Sub-hypothesis (b): FGM 2019 (4D, Λ = 0, transient).**
  - *Transit and stability.* t_min = d + logs; traversability is exponentially fragile; the mouths merge on a timescale of about d^{3/2} (geometric) [D-07].
  - *Strut.* It needs a cosmic-string strut with Gμ/c² = 2(GM/(c²d))², which is 2×10⁻⁶ at d = 10³ GM/c².
  - *Thermal.* Holes heavier than 4.5×10²² kg are colder than the CMB, so they need CMB isolation [calc: lens-engineer_cost_table.py; M-ENGINEER-11].
- **Sub-hypothesis (c): MM 2020 at human scale (labelled speculative: RS II plus a dark U(1)).**
  - *Throat size.* r_e > 1.5×10⁷ m under MM's criterion of 20 g over 0.5 m [Q-01]. This comes from the boost-invariant longitudinal tide of the AdS₂×S² throat, not from ultra-relativistic crossing (M-IDEALIZER-07 refuted the "universal floor" wording). The MT-like criterion of 1 g over 2 m gives 1.35×10⁸ m (corrected by M-DECOMPOSER-09 from 6.8×10⁷ m).
  - *Mouths.* 2.0×10³⁴ kg (1.0×10⁴ M_☉) each [Q-04].
  - *Times.* The traveller's proper time is 0.157 s, against 9.42×10³ yr outside. At d = ℓ, τ/T_ext = 1.66×10⁻¹².
  - *Rocket equivalent.* A rocket would need γ = 6.0×10¹¹ to match this, which costs 3.8×10³⁰ J for 70 kg [calc: lens-examiner_shortcut.py; M-EXAMINER-06].
  - *"Long" is temporal, not spatial.* The proper throat length is only 8.99×10⁸ m (3.0 light-seconds) [M-EXAMINER-05].
  - *Payload is not the binding limit.* mc²/|E_bin| = 1.4×10⁻⁸ for 70 kg [M-EXAMINER-07]. The payload cap is ℓ ≤ r_e√(M/m), which is 2.7×10⁷ ly for a human [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-idealizer_cost.py; M-IDEALIZER-09].
  - *What does bind: species count.* MM quote N_f > 10⁵² [Q-03]; the lenses' own scaling gives 2.4×10⁵⁴ to 3.4×10⁵⁵, against a cap of about 10³² [K-22; M-ENGINEER-08, M-IDEALIZER-10].
  - *What does bind: temperature.* The dark sector must be below 10⁻²⁶ eV [Q-07]. The ambient bath must be below ħc/(k_Bℓ) = 8.1×10⁻²³ K (constraints), or below about 5×10⁻²² K for CMB photons boosted by 2γ² (M-ENGINEER-10 correction of the engineer's 2.9×10⁻²¹ K).
  - *What does bind: formation.* No formation mechanism is known [D-08]. The Schwinger-form pair-creation exponent at 1200 T is 5.2×10⁹² (engineer's approximation, M-ENGINEER-09).
predictions:
- *If true:*
  - the mouths look like near-extremal, magnetically charged black holes, with no Ellis lensing gutters [D-22];
  - T_thru ≥ T_ext for every probe;
  - transmission depends on the probe: low-frequency scalars are mostly reflected, while charged massless fermions pass at about unit probability [D-C5];
  - a complete linear stability analysis of MMP finds no mode growing faster than the transit time.
- *If false:*
  - a fast-growing MMP mode appears in some sector;
  - or MMP fails to be self-consistent once the fermion response (including the anomaly trace) is included [F-01].
evidence for: [D-06] [D-07] [D-08] [Q-10] [Q-11] [K-07f] [K-18] [D-27]; the MMP energy minimum was reproduced three times (M-CONSTRAINTS-12, M-ENGINEER-01, M-DIALECTICIAN-06). The one-line model |E_neg| = M(r_e/ℓ)² reproduces MM's 2.5×10⁻²⁵ and 5×10⁹ kg exactly (M-IDEALIZER-08).
evidence against:
- *Stability rests on preprints.* MMP's stability evidence is preprints only [D-C5, F-01]; Bilotta reports the interior is "unstable to large fluctuations" [D-C5].
- *FGM 2019 is fragile and needs an unobserved strut.* It is fragile, and no cosmic string has been observed [D-07].
- *Magnetic charge and formation.* No magnetic charge has been seen at any scale [D-25]. MM has no formation mechanism [D-08].
- *Mouth motion threatens "never shortcuts".* Mouth clock offsets can move a long wormhole into the shortcut window (C7). In a 2D toy, the long MMP equilibrium disappears:
  - at Δ/l₀ = 0.1495 (dialectician, M-DIALECTICIAN-07);
  - or at 0.25 to 0.56 of the no-feedback shortcut threshold (mechanist, range corrected by M-MECHANIST-06).
  So "never shortcuts" may hold only while Δ ≈ 0.
- *The SM-MMP numbers rest on lens assumptions.* They use the lenses' g and N_eff readings. At N = 1 the engineer (g = 0.06) and constraints (g = e) lenses differ by a factor of about 25 in |E_min| (4.5 MeV against 113 MeV) and about 5 in throat length (1.1 m against 0.23 m).
decisive test:
- *Theory:* a complete linear (then nonlinear) stability analysis of MMP in every sector, beyond the O(α) truncation. Sadhukhan covers one sector [F-01]. Semiclassical theorists could do it. It needs growth rates compared with the transit time πℓ/c. No date is known.
- *Observation:* searches for primordial magnetically charged black holes, which Bai et al. say could extend the Parker bound "by several orders of magnitude using the large-scale coherent magnetic fields in Andromeda" [new: Bai et al. 2020, JHEP 10, 210, arXiv:2007.03703, ACCESS abstract]. This is the only search class that targets MMP-type objects.

## C3: Shortcuts, and hence time machines, are possible in principle because the self-consistent achronal ANEC fails: a back-reacted semiclassical spacetime can violate ANEC on a complete achronal throat geodesic.
type: option
from: DECOMPOSER-D, EXAMINER-F, DIALECTICIAN-D, CONSTRAINTS-F, MECHANIST-A (its stated weakest link)
argument:
- **The condition is unproven.**
  - It is a conjecture, not a theorem [K-07a, D-C3]. Wall's GSL derivation fails once linearised gravitons are quantised [K-07c], and Kontou–Sanders list its validity in curved spacetime as open [D-26].
  - Known achronal-ANEC violations:
    - Urban–Olum: a violation that "can be made as large as desired ... the achronal averaged null energy condition is likewise violated" [new: Urban & Olum 2010, arXiv:0910.5925, ACCESS abstract];
    - holographic models: Ishibashi, Maeda & Mefford find "holographic models which violate the achronal ANEC for 3+1 and 4+1-dimensional boundary theories" [new: Ishibashi, Maeda & Mefford 2019, arXiv:1903.11806, ACCESS abstract];
    - positive-frequency Dirac fields: they violate ANEC on fixed wormhole backgrounds [D-12].
- **If it fails, short throats are huge shortcuts.**
  - A 1 m Ellis throat between mouths 1 ly apart has T_thru/T_ext = 2.1×10⁻¹⁵ [calc: lens-examiner_shortcut.py; M-EXAMINER-02; also M-DECOMPOSER-05].
  - It becomes a time machine at a clock lag of only d/c: 3.3 ns at 1 m, 499 s at 1 AU, 1 yr at 1 ly [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-mechanist_timemachine.py; M-MECHANIST-02].
- **Sub-hypothesis (a): a self-consistent Urban–Olum-type violation** (conformally coupled fields in a back-reacted conformally flat spacetime).
- **Sub-hypothesis (b): the FGM 2018 quotient.** Its boundary-to-boundary transit t* beats half the boundary circle (light time πℓ) iff |ΔV| > 2ℓe^{−πr₊/ℓ} [calc: lens-constraints_perturbative.py / CONSTRAINTS-F algebra; M-CONSTRAINTS-17 verified as algebra only; the comparison path is the lens's modelling choice].
- **Sub-hypothesis (c): a failure beyond semiclassical gravity** (quantised gravitons, interacting fields in curved space).
predictions:
- *If true:*
  - a self-consistent back-reacted spacetime with ANEC < 0 on a complete achronal null geodesic;
  - FGM 2019 at second order gives t_min < d;
  - a short one-sided throat appears as a semiclassical solution.
- *If false:* every violation stays confined to fixed backgrounds or chronal geodesics, which are Kontou's three classes [D-27].
evidence for: [K-07a] (conjecture status) [K-07c] [D-C3] [D-26]; Urban & Olum (abstract); Ishibashi et al. (abstract); [D-12].
evidence against:
- *No self-consistent violation is known.* Every known violation is test-field or fixed-background; Kontou finds the condition "free of counterexamples in semiclassical gravity" [D-27].
- *A violation is not enough for a shortcut.* Ishibashi et al.'s own boundary is "causally proper", with fastest null geodesics lying on the boundary.
- *Proofs and authors' arguments go the other way.*
  - The condition is proved in AdS₂×S², dS and AdS (Rosso 2020, ACCESS abstract) and in flat space [K-07d].
  - MMP argue that short wormholes "are not allowed by the Einstein equations combined with the achronal average null energy condition" [D-06].
- *The source problem remains even if the conjecture fails.* A shortcut still needs a negative-energy source at throat scale, and free-field QIs confine it to Planck-thin bands (C4).
- *Unverified load.* Urban–Olum is load-bearing yet only abstract-checked here; the dossier lists RC-03 as unchecked [D-C3].
decisive test:
- *What:* back-react the Urban–Olum stress tensor self-consistently, or compute FGM 2019's minimum transit time at second order (the same calculation as C1's test, read with the opposite sign).
- *Who:* semiclassical theorists.
- *Precision:* the sign of ∫T_kk dλ on a complete achronal geodesic in a solution of G = 8π⟨T⟩.
- *When:* no date is known.

## C4: Classical exotic-matter wormholes (Morris–Thorne/Ellis, Visser thin-shell and polyhedral) give shortcuts of any designed T_thru/T_ext in principle, given labelled phantom or modified-gravity matter.
type: option
from: EXAMINER-D, IDEALIZER-C, ENGINEER-D, CONSTRAINTS-D
argument: GR "solved in reverse" accepts any mouth separation [new: Graham & Olum 2007, arXiv:0705.3193, ACCESS full-text, "one simply solves Einstein's equations in reverse"].
- **Transit times.**
  - *Ellis, b₀ = 1 m, observers at 10 m.* T_thru = 6.64×10⁻⁸ s. T_thru/T_ext = 2.0×10⁻² (1 km), 1.3×10⁻¹⁰ (1 AU), 2.1×10⁻¹⁵ (1 ly). The traveller's proper time is 6.6×10⁻⁷ s at 0.1c.
  - *Schwarzschild thin shell, M = 1 M_☉, a = 10 km.* T_thru = 6.52×10⁻⁴ s, with ratios 2.0×10⁻² to 2.1×10⁻¹¹ [calc: lens-examiner_shortcut.py; M-EXAMINER-02, M-EXAMINER-03 verified].
- **Energy-condition table.**
  - *Ellis, b₀ = 1 m.* ρ + p_l = −9.63×10⁴² J/m³ at the throat. All four pointwise conditions are violated at every scanned point. The radial ANEC is −E/(8b₀) = −1.51×10⁴³ J/m² per unit E [calc: lens-constraints_ec_table.py; M-CONSTRAINTS-01].
  - *Exotic mass.* |M| ≈ (1 to 2) b₀c²/G = 1.35×10²⁷ to 2.69×10²⁷ kg per metre of radius. With a proper-volume measure the coefficient is π/2 (M-IDEALIZER-04).
  - *Slow flare.* It shrinks the ANEC as 1/√(b₀L) (−3.5×10⁻³ m⁻¹ at L = 10⁴ b₀, geometric), but never changes its sign [M-CONSTRAINTS-04].
- **Sub-hypothesis (a): Ellis/Morris–Thorne with a phantom scalar.** A slow crossing (10 km/s) needs only b₀ ≥ 505 m (20 g over 0.5 m) or 4.5 km (1 g over 2 m), that is 0.34 or 3.1 M_☉ of negative mass, and takes 0.16 s or 1.4 s [calc: lens-idealizer_cost.py; M-IDEALIZER-06].
- **Sub-hypothesis (b): thin shell.**
  - σ = −c⁴/(2πGa) = −1.9×10⁴³ J/m² at a = 1 m (flat limit); shell mass −2.7×10²⁷ kg [M-CONSTRAINTS-05, M-ENGINEER-04].
  - Linear stability needs β² > 3.5 (a = 2.5M) or β² < 0 (a > 3M) [M-CONSTRAINTS-06].
- **Sub-hypothesis (c): Visser cube (polyhedral).**
  - Face-centred rays carry zero stress, so their ANEC is exactly 0 [new: Visser 1989, PRD 39, 3182, arXiv:0809.0907, ACCESS full-text, "the stress energy is zero"].
  - The edges carry line mass −c²/(8G) = −1.68×10²⁶ kg/m, about −2.0×10²⁷ kg for a 1 m cube [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-constraints_budgets.py; M-CONSTRAINTS-15].
  - The face ray is null-non-generic, so focusing-based theorems may not bite (the constraints lens's inference, low confidence).
predictions:
- *If viable:* a stabilised phantom-supported shortcut survives numerical evolution with a payload, and a curved-space QEI leaves room for macroscopic throats.
- *If not:* ghost throats collapse or expand under a weak positive pulse, as already found [D-13], and curved-space QEIs tighten the bound.
evidence for: [D-15] [Q-24]–[Q-29]; the energy-condition and shortcut tables (verified); Visser 1989 (full-text).
evidence against:
- *Admissible fields fail the QIs.*
  - A 1 m throat exceeds the single-field Ford–Roman bound by 1.6×10⁶².
  - A free-field throat must be ≤ 4.9×10³ l_P = 7.9×10⁻³² m (f = 0.01).
  - A negative-energy band must be ≤ 1.84×10⁻²¹ m thick at r₀ = 1 m, or else ≥ 1.6×10⁶² species are needed [calc: lens-constraints_qi.py; M-CONSTRAINTS-07, M-CONSTRAINTS-08; also M-IDEALIZER-11].
- *Laboratory gap.* The gap to demonstrated (Casimir) negative energy is 38 to 57 orders, and no throat size closes both the density gap and the band gap [calc: lens-engineer_cost_table.py; M-ENGINEER-02 to M-ENGINEER-04].
- *Instability.* Ghost-scalar throats have one unstable mode [D-13]. Thin shells need superluminal or imaginary sound speed [D-14, M-CONSTRAINTS-06].
- *Achronal ANEC.* In two-ended versions the radial geodesic is achronal (M-CONSTRAINTS-14), so if built from quantum fields they violate the self-consistent achronal ANEC.
- *Creation.* Tipler: topology change "within a finite region ... must be accompanied by singularities" [new: Tipler 1977, Annals Phys. 108, 1, ACCESS abstract].
- *Phantom matter.* It is labelled speculative in the brief.
decisive test:
- *Theory:* a numerical evolution of a stabilised phantom (or modified-gravity) shortcut throat with a payload pulse; or a curved-space QEI (Fewster–Smith type) evaluated on the Ellis throat. Numerical-relativity groups could do either; Kain-type spherical codes already exist [D-13].
- *Experiment:* a time-resolved laboratory sub-vacuum energy density in J/m³ compared with the Fewster–Eveson bound. None exists [D-20, D-C6].

## C5: Einstein–Dirac–Maxwell fields hold an asymptotically flat traversable wormhole open without exotic matter.
type: option
from: DECOMPOSER-E, MECHANIST-C (EDM half), DIALECTICIAN-C (P4–P6), ENGINEER-F, CONSTRAINTS-E, EXAMINER finding 11
argument:
- **Sub-hypothesis (a): symmetric BKR 2021.** Two gauged massive fermions in a singlet state, described as "a quantum wave function rather than a quantum field", with Q_e/M > 1 and q/μ < 1 (Planck units) [D-09, Q-19].
- **Sub-hypothesis (b): asymmetric smooth solutions.** Konoplya–Zhidenko [D-10c], and Dzhunushaliev et al. 2026, read as an abstract only [D-C2].
- **Sub-hypothesis (c): positive-frequency Dirac sources.** Weinbaum finds they violate ANEC on fixed wormhole backgrounds [D-12].
- **Scope.** This is the only candidate that answers "yes" to "held open without exotic matter" in the brief's classical sense. It is two-sided, so it is never a shortcut.
predictions:
- *If true:* a smooth, two-ended, positive-frequency EDM solution exists and stays traversable under dynamical evolution.
- *If false (dialectician P4 to P6):*
  - any two-ended solution uses negative-frequency or non-normalisable modes, or collapses;
  - any positive-frequency survivor is one-sided and long;
  - throats stay near the Planck scale.
evidence for: [D-09] [D-C2] (the for side); [D-12] (test-field ANEC violation).
evidence against:
- *Exotic by definition.* By the brief's own definition the Dirac field is exotic, because it violates the NEC [D-10a, D-11].
- *ANEC on an achronal geodesic.* For any static two-ended asymptotically flat throat the radial ANEC is strictly negative (M-CONSTRAINTS-02) and the radial geodesic is achronal (M-CONSTRAINTS-14). Read as semiclassical, an EDM wormhole would therefore violate the self-consistent achronal ANEC.
- *No valid solution.*
  - The symmetric solutions are not solutions [D-10b].
  - The asymmetric ones collapse to black holes, with null rays trapped [D-11].
  - Positive-frequency sources give only partial wormholes [D-12].
- *Scale.*
  - Kain's throats are 1.2×10⁻³³ to 8.1×10⁻³³ m, with fermion mass μ̄ = 0.2 m_P = 4.35×10⁻⁹ kg = 4.8×10²¹ m_e [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-dialectician_edm_scale.py; M-DIALECTICIAN-08].
  - q/μ < 1 needs a fermion of 7×10¹⁷ to 4×10¹⁸ GeV, 15.6 to 21.9 orders beyond known charged fermions [M-ENGINEER-12].
  - A Planck-size throat "would not be traversable" [D-27].
decisive test:
- *What:* a Weinbaum-type search extended to the Maxwell-coupled asymmetric branch, plus a dynamical evolution of the Dzhunushaliev et al. 2026 solutions with their frequency content checked.
- *Who:* the Kain and Weinbaum groups' methods [D-11, D-12].
- *Precision:* whether a positive-frequency, two-ended solution exists and whether null rays escape under evolution.
- *When:* no date is known.

## C6: Even granting the self-consistent achronal ANEC, the shortcut ban is narrower than stated: it forbids only shortcuts threaded by a complete achronal throat geodesic, so misaligned one-sided shortcuts escape it.
type: reframe
from: IDEALIZER-B; DECOMPOSER finding 4 and L6 as corrected by M-DECOMPOSER-08; EXAMINER finding 9 and hidden premise 14; MECHANIST finding 3; CONSTRAINTS F17 (polyhedral face rays)
argument: The doubtful premise is that the conjecture, if true, excludes every one-sided shortcut.
- **Graham–Olum's own theorem does not reach one-sided shortcuts.** It assumes simple connectedness, "which means that the wormholes we rule out are only those which connect one asymptotically flat region to another, not those which connect a region to itself" [new: Graham & Olum 2007, arXiv:0705.3193 p. 5, ACCESS full-text].
- **Two independent toy models agree.** Both use a point-mouth handle in flat space.
  - *Idealizer model.* A complete through-ray is achronal iff the gluing is aligned (On = n) and L ≤ D·n̂ (M-IDEALIZER-01 verified). Mirror gluing (O = −I, the standard Visser cut-and-paste orientation) gives no achronal complete through-ray even at L = 0 (M-IDEALIZER-02 verified) [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-idealizer_handle.py].
  - *Decomposer model.* The math check **refuted** the decomposer's claim that "a one-sided shortcut implies a complete achronal throat geodesic". The corrected form: such a geodesic exists iff −d < τ ≤ d·max|e·n̂| over directions n̂ fixed by the mouth rotation. A static throat with L = 0.5d and mouths rotated by 10° or 180° is a shortcut (ratio 0.5), yet every throat-crossing null geodesic is chronal (M-DECOMPOSER-08).
- **The other routes have the same topological gap.**
  - *Covering space:* blocked, because Casimir support "depends on the actual topology of space, so we cannot go to the covering space" [new: Maldacena, Milekhin & Popov, arXiv:1807.04726, ACCESS full-text].
  - *Wall's GSL route:* "If as the result of nontrivial topology the I+ and I− lie in the same asymptotic region ... the horizon generators will no longer be achronal" [new: Wall 2010, arXiv:0910.5751, ACCESS full-text].
  - *FGM:* they concede "it is difficult to use arguments about causal curves connecting distant points to rigorously bound wormhole transit times" [new: Fu, Grado-White & Marolf, arXiv:1908.03273, ACCESS full-text].
- **Sub-hypothesis (b): polyhedral face rays.** They have ANEC exactly 0 and are null-non-generic [F17, C4c], a second escape from focusing-based arguments (low confidence).
- **What survives the reframe.** Every mouth-motion route to a CTC still passes through an epoch with an achronal throat geodesic: −d < τ ≤ 0 always qualifies, checked at R = 180° and τ = −0.5d (M-DECOMPOSER-08, "what survives"). Graham–Olum's Theorem 3 also forbids a compactly generated Cauchy horizon under the conjecture [new: Graham & Olum 2007 p. 6, ACCESS full-text]. So the loophole yields at most a static misaligned shortcut that cannot be turned into a time machine without meeting the ban.
- **Consequence for Q1.** Its in-principle answer rests on the conjecture plus an extra, so far unproved step. The ban on one-sided quantum shortcuts is an expectation, not a theorem.
predictions:
- *If the reframe is right:*
  - no proof extends the ban to multiply connected spacetimes;
  - a self-consistent mirror-glued, Casimir-supported throat with L < d would violate nothing proved;
  - finite mouths narrow the loophole by O(a/d) but do not close it.
- *If it is wrong:*
  - a quantum-focusing or GSL theorem for causal horizons in multiply connected spacetimes excludes all one-sided shortcuts;
  - or curved-exterior, finite-mouth geometry restores a complete achronal through-line. Near-grazing rays give achronal segments of length about d/ε², which nobody has computed.
evidence for: Graham–Olum p. 5 (full-text); M-IDEALIZER-01, M-IDEALIZER-02 and M-DECOMPOSER-08 (verified/refuted as stated); MMP, Wall and FGM quotes (full-text).
evidence against:
- *Toy models only.* Point mouths, flat exterior, no back-reaction; the general curved-exterior form of L6 was not proved either way (math/decomposer.md, Unverified).
- *Expectations go the other way.* MMP [D-06] and Kontou [D-27] expect a ban.
- *No candidate solution exists.* Nobody has a self-consistent short one-sided quantum solution.
- *Practice is unchanged.* The reframe changes the logic, not the answer in practice.
decisive test:
- *Cheapest calculation:* achronality of complete through-throat null geodesics for finite mouths in a curved (Schwarzschild-like) exterior with rotated or mirror gluing, extending M-DECOMPOSER-08.
- *Decisive theory:* a GSL or quantum-focusing argument for causal horizons in multiply connected spacetimes; or a self-consistent mirror-glued Casimir throat with L < d.
- *Who:* mathematical-relativity and semiclassical theorists.
- *When:* no date is known.

## C7: A wormhole's shortcut status depends on its mouths' clock offset Δ: long wormholes become one-way shortcuts at Δ = T_thru − d before time machines at T_thru + d, so one barrier governs both cruxes.
type: reframe
from: MECHANIST-B, DIALECTICIAN-B, EXAMINER-C, DECOMPOSER-C, DECOMPOSER-F, MECHANIST-D (rival sub-hypothesis ii), MECHANIST-E (corollary)
argument: The doubtful premises are that "shortcut" is a property of the geometry, and that long wormholes "can not be converted into time machines" [new: Maldacena & Milekhin, arXiv:2008.06618 p. 2 footnote, ACCESS full-text].
- **Thresholds.** Δ_s = T_thru − d/c and Δ_CTC = T_thru + d/c; the window between them is 2d/c wide. Verified independently six times: M-DECOMPOSER-01, M-EXAMINER-01, M-MECHANIST-01, M-DIALECTICIAN-01, M-IDEALIZER-03, M-CONSTRAINTS-13.
- **MM numbers** (ℓ = 3×10³ ly held fixed).
  - *d = 1000 ly:* Δ_s = 8.4×10³ yr, Δ_CTC = 1.04×10⁴ yr.
  - *d = ℓ:* Δ_s = 6.4×10³ yr, Δ_CTC = 1.24×10⁴ yr.
- **Accumulating the offset** (for the shortcut lag; the CTC lag needs about 1.24 times more, per the M-DECOMPOSER-04 note).
  - *Mouth motion at 0.1c:* about 1.7×10⁶ yr, with 9.1×10⁴⁸ J (51 M_☉c²) per leg for one 2×10³⁴ kg mouth.
  - *Mouth motion at 0.9c:* about 1.5×10⁴ yr and 2.3×10⁵¹ J.
  - *Mouth parked at the Sgr A* ISCO:* 2.9×10⁴ yr to the shortcut, 3.6×10⁴ yr to the CTC.
  - *Circling at 10³ ly:* needs 1.9×10³⁰ N from an external agent.
  - [calc: lens-mechanist_timemachine.py; lens-decomposer_timeshift.py; runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-dialectician_timeshift.py; M-MECHANIST-03, M-MECHANIST-04, M-DECOMPOSER-04, M-DIALECTICIAN-02 verified]
- **FGM 2019.** Δ_s is only the log term [M-DIALECTICIAN-01].
- **Achronality inside the window.** For Δ_s < Δ < Δ_CTC, the throat segment and the on-axis complete throat geodesic are achronal (M-DIALECTICIAN-03; off-axis geodesics stay chronal part of the way). So under the conjecture, protection must act at Δ_s, 2d/c before Hawking's chronology horizon. MM's footnote then holds only dynamically, when mouth lifetime × redshift asymmetry ε < T_thru − d.
- **Rival sub-hypotheses for what stops conversion.**
  - *(i) The conjecture acts at Δ_s:* the support fails, the throat lengthens, or the solution ceases to exist.
  - *(ii) Vacuum polarisation acts at Δ_CTC (Hawking/Kim–Thorne). Strained:*
    - the divergence is "extremely weak", δg ∼ (l_P/D)(l_P/Δt) [new: Kim & Thorne 1991, PRD 43, 3929, ACCESS abstract];
    - a Roman ring makes the vacuum polarisation "arbitrarily small" [new: Visser 1997, PRD 55, 5212, arXiv:gr-qc/9702043, ACCESS abstract];
    - Kay–Radzikowski–Wald give support, not proof [K-12].
  - *(iii) The mouth pair dies first:* coalescence, accretion collapse [D-08], or fragility [D-07].
- **Toy dynamics** (2D twisted-loop Casimir model of MMP).
  - *What stands.* The total energy-density enhancement is κ = L²(L²+Δ²)/((L−Δ)²(L+Δ)²). The long equilibrium is lost at Δ/l₀ = 0.1495 (M-DIALECTICIAN-07), or at 0.25 to 0.56 Δ_s (M-MECHANIST-06, which corrected 0.52 to 0.56). Read only as a sign: the Casimir sector shortens the throat toward the shortcut (positive feedback), so protection, if any, must come from outside the supporting field.
  - *Corrected by M-MECHANIST-05 (refuted labelling).* Along the would-be achronal (closing) null direction, T_kk = −πc/(3(L+Δ)²) (natural units) **weakens** as Δ grows: by a factor 0.31 at Δ_s for MM with D/c = 10³ yr. The ANEC per lap stays finite, −πc/(12L), at Δ = L. The (L/(L−Δ))² enhancement belongs to the non-closing direction. So the claim that the negative null energy on the achronal geodesic grows toward the threshold is not supported; it shrinks but stays negative.
- **Corollary (MECHANIST-E).** A natural short-throat one-sided wormhole with mouths in unequal potentials drifts into a time machine on astrophysical times (M-MECHANIST-04):
  - 8.5×10⁸ yr, with one mouth 0.01 pc from Sgr A* and the other 8 kpc away;
  - about 2×10¹⁰ yr across a flat 220 km/s rotation curve;
  - 2.3×10⁴ yr for a 1 AU throat with one mouth on Earth's surface.
predictions:
- *P1 (if true):* a self-consistent MMP or FGM 2019 solution with an asymmetric mouth redshift loses stationarity, or lengthens T_thru, before Δ reaches T_thru − d.
- *P2:* if instead such a solution enters the window 2d/c wide intact, the self-consistent achronal ANEC is falsified without any CTC forming.
- *Corollary:* no long-lived natural short throats exist with mouths in unequal potentials.
- *If false:* a dynamical mechanism locks Δ = 0 (for example the symmetric binary orbit), so the premise that Δ can accumulate fails.
evidence for: the six verified threshold checks; MM footnote and p. 7 coalescence statement, "parametrically longer than the traversal time" [new: arXiv:2008.06618 p. 7, ACCESS full-text]; MTY 1988: "that wormhole can be converted into a time machine" [new: Morris, Thorne & Yurtsever 1988, PRL 61, 1446, ACCESS abstract].
evidence against:
- *Toy models.* Point mouths, flat exterior, constant Δ, and a 2D loop standing in for MMP's lowest-Landau-level fermions.
- *Δ = 0 is only a reading.* That the static MM/MMP solutions have Δ = 0 is the examiner's reading, not stated in the papers.
- *Achronal epoch is not shortcut epoch for misaligned mouths.* The identification fails there (M-DECOMPOSER-08), though every route to a CTC still crosses an achronal epoch.
- *The examiner's framing.* The examiner keeps shortcut and time machine as separate thresholds: a shortcut alone is not a time machine.
decisive test:
- *What:* solve MMP (or FGM 2019) self-consistently with the twisted identification (t, x) ~ (t + Δ, x + L), or with asymmetric mouth redshift, and find whether stationary solutions exist for Δ > T_thru − d.
- *Who:* semiclassical theorists using MMP's lowest-Landau-level framework.
- *Precision:* existence or non-existence of solutions across the 2d/c window.
- *When:* no date is known; no source in the dossier treats long-wormhole time shifts.

## C8: Two-sided wormholes (GJW, Maldacena–Qi) and quantum-processor analogues are teleportation with geometric bookkeeping: they never beat their coupling channel, and Sycamore-type runs test size winding, not spacetime.
type: reframe
from: EXAMINER-E, IDEALIZER-F, ENGINEER-E, DIALECTICIAN-F, MECHANIST-F, DECOMPOSER finding 7
argument: The doubtful premises are hidden premise 1, that "earlier than the channel" is a meaningful test for two-sided constructions, and hidden premise 7, that the 2022 experiment created or tested a wormhole.
- **Two-sided constructions.**
  - The bulk wormhole and the boundary coupling are two descriptions of one process.
  - The message emerges only after the coupling acts [D-01, Q-15]. Quanta passed are ≲ a constant × the bits exchanged [K-15], and the GJW window is open for less than a Planck time [Q-16].
  - Sending a 1 kg payload as quanta through a throat of R = 1 m needs about mcR/ħ = 2.8×10⁴² quanta, each paid for in classical bits [calc: runs/2026-10-03-traversable-wormhole-shortcuts/calc/lens-idealizer_qi_twosided.py; M-IDEALIZER-12].
- **The Sycamore experiment.**
  - It used 164 two-qubit gates on 9 qubits, with a learned Hamiltonian of 7 Majorana fermions and 5 fully commuting terms [Q-37].
  - Size winding and the coupling-sign asymmetry are necessary features of a gravity dual, not sufficient ones [D-C1].
- **Sub-hypotheses within the reframe.**
  - *(a) Jafferis side:* the signatures survive with chaotic Hamiltonians at larger N. Byun et al. ran N = 8 with I_PT of order 0.01 [Q-39, F-05].
  - *(b) Kobrin–Schuster–Yao side:* the signatures are an artefact of the commuting learned Hamiltonian [D-C1].
- **Gap to the controlled regime.**
  - Chaotic sparse SYK at N = 20 to 100 needs 3.2×10⁴ to 8.0×10⁵ gates and an error per gate of 2.2×10⁻⁵ to 8.7×10⁻⁷. The demonstrated effective error is ≈ 4.2×10⁻³, so the gap is 2.3 to 3.7 orders [calc: lens-engineer_cost_table.py; M-ENGINEER-13; the gate model is the engineer's unsourced estimate].
  - Sparse SYK keeps the holographic physics "even when k is of order unity" [new: Xu, Swingle et al., arXiv:2008.02303, ACCESS abstract].
  - TRL is about 4 as a simulator and 1 as a gravity test [F-19, engineer table C].
predictions:
- *If true:*
  - teleported qubits never exceed the classical bits the coupling carries;
  - fidelity drops to zero when the classical L→R step is cut;
  - in chaotic runs at larger N, the coupling-sign asymmetry becomes operator-generic and peaks near the scrambling time, which grows like log N (dialectician P7). A commuting learned model does not show this for untrained operators.
- *If false:* some protocol delivers information before, or in excess of, its coupling channel.
evidence for: [D-01] [D-02] [D-03] [D-16] [D-C1] [K-15] [Q-15]–[Q-17] [Q-37] [Q-39]; GJW "no longer achronal" (full-text).
evidence against:
- *The reply.* Jafferis et al. argue that the critique concerns "counterfactual scenarios" [D-C1].
- *Weak data.* Byun et al. is a preprint with a small signal [Q-39].
- *The mechanism does transfer.* It reaches 4D one-sided spacetimes through MMP and FGM 2019 (constraints Table 3), so the "bookkeeping" reading covers only the two-sided rows.
- *Maybe no reframe is needed.* The brief's own two-sided definition already compares against the coupling channel.
decisive test:
- *What:* chaotic sparse-SYK teleportation at N ≥ 20, with the coupling-sign (ANEC-sign) asymmetry measured for untrained operators as a function of N and time, plus a control with the classical channel cut.
- *Who:* quantum-hardware groups (Google, IBM, Quantinuum platforms used so far [D-16, D-17, Q-39]).
- *Precision:* error per gate of about 10⁻⁵.
- *When:* N ≈ 20 plausibly within about 5 to 10 yr (the engineer's estimate, unsourced).
