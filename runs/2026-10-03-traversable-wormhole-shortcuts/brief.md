# Brief: Traversable wormholes: shortcuts, negative energy, and what holds them open
slug: 2026-10-03-traversable-wormhole-shortcuts | depth: deep | type: feasibility | date: 2026-10-03

## Question as asked
"Can a traversable wormhole carry a payload, or even a signal, between two distant points sooner than light travelling between them through the surrounding space, and can one be held open at all without negative energy? Weigh the classical Morris–Thorne and thin-shell wormholes against the constructions proposed since 2017 that use quantum effects or ordinary matter: Gao–Jafferis–Wall, Maldacena–Qi, Maldacena–Milekhin–Popov, Fu–Grado-White–Marolf, Maldacena–Milekhin's "humanly traversable" wormholes, and the Einstein–Dirac–Maxwell solutions of Blázquez-Salcedo, Knoll and Radu, with their critiques. For each, check by calculation which energy conditions it violates, including the averaged null energy condition along the throat, and whether the path through it is a true shortcut or longer than the path outside. Treat the self-consistent achronal averaged null energy condition, and chronology protection against wormhole time machines, as central cruxes. For whatever survives, what would it take to create or widen one enough to pass a payload, in mass, energy and technology, and what is the nearest experiment or observation that could test any part of it, including the 2022 "wormhole on a quantum processor" and astronomical searches for natural wormholes?"

## Question made precise

Four sub-questions:
- **Q1 Shortcut.** Is there a traversable wormhole, consistent with admissible physics, through which a signal or payload sent from near one mouth arrives near the other mouth before any signal sent through the surrounding space could?
- **Q2 Support.** Can a wormhole be held open, and traversable, without negative energy? Answer separately for each sense of "negative energy" defined below: pointwise, averaged along the throat, and averaged along an achronal geodesic.
- **Q3 Cost.** For each construction that survives Q1 and Q2 as a traversable wormhole, shortcut or not: what would it take to create it, or widen it enough to pass a given payload? Give mass, energy, charge, field strengths, environment and technology, and the orders-of-magnitude gap to what has been demonstrated.
- **Q4 Tests.** What is the nearest experiment or observation that could test any part of the answer? Include the 2022 quantum-processor experiment and astronomical searches for natural wormholes.

### Definitions
- **Traversable wormhole:** a spacetime with a throat (a minimal 2-surface that flares out) through which a causal curve passes from one mouth to the other without meeting a horizon or singularity, open long enough for that passage. For each construction, say whether it is:
  - **two-sided:** it connects two separate asymptotic regions or two boundaries;
  - **one-sided:** its two mouths sit in one shared ambient space.
- **Shortcut ("sooner than light through the surrounding space"):**
  - *One-sided wormholes.* A causal curve through the throat links an event near mouth A to an event near mouth B that no causal curve confined to the exterior can link. Operationally:
    - put static observers at a stated radius outside each mouth, with clocks synchronised through the exterior;
    - compare the earliest arrival time through the throat, T_thru, with the exterior light-travel time, T_ext;
    - it is a shortcut if T_thru < T_ext.

    Report T_thru/T_ext, and also the traveller's proper time τ_thru, which can be short even when T_thru > T_ext.
  - *Two-sided constructions with no shared ambient space* (Gao–Jafferis–Wall, Maldacena–Qi). The comparison is with the non-gravitational channel that makes them traversable: the boundary coupling, or the classical communication it stands for. Say whether the wormhole delivers anything earlier than that channel, or without it.
- **Signal and payload:**
  - a *signal* is at minimum one bit or qubit carried by one quantum;
  - a *payload* is a positive-energy object, taken at two sizes: 1 kg, and a human (about 70 kg and 2 m, with tidal accelerations survivable at about Earth gravity; verify the criterion against Morris & Thorne 1988).

  Track the energy, size and information each construction can pass, and the back-reaction: a payload's positive energy can close the throat.
- **Energy conditions.** Signature (−,+,+,+); T_kk ≡ T_μν k^μ k^ν.
  - *Pointwise:* NEC (T_kk ≥ 0 for every null k), WEC, SEC and DEC.
  - *ANEC:* ∫ T_kk dλ ≥ 0 along a complete null geodesic, λ affine.
  - *Achronal ANEC:* ANEC required only on achronal complete null geodesics, those with no two points timelike-related.
  - *Self-consistent achronal ANEC* (Graham & Olum 2007): no self-consistent semiclassical spacetime violates ANEC on a complete achronal null geodesic.
  - Also quantum energy inequalities (QEIs, Ford–Roman type), the quantum null energy condition (QNEC) and the smeared null energy condition (SNEC) where relevant.
- **"Negative energy" and "exotic matter."** "Negative energy" means T_μν u^μ u^ν < 0 for some observer (WEC violation), unless a construction's argument turns on NEC or ANEC. "Exotic matter" means matter that violates the NEC classically. Keep apart:
  - negative energy from ordinary quantum fields (Casimir-type vacuum energy);
  - exotic classical matter;
  - classical fields whose energy is not bounded below (for example classical Dirac fields).
- **"Check by calculation."** For each construction, compute or reproduce:
  - the sign and size of ρ + p along the throat;
  - the ANEC integral along the radial (throat-crossing) null geodesic;
  - whether that geodesic is achronal in the full spacetime, including boundary couplings and exterior paths;
  - T_thru against T_ext.

  Use `gr_tensors.py` for explicit metrics. Where a construction is perturbative (Gao–Jafferis–Wall, Maldacena–Qi, Maldacena–Milekhin–Popov, Fu–Grado-White–Marolf), reproduce the published integral, and say where a published value is quoted rather than recomputed.
- **Chronology protection.** Two questions:
  - can a wormhole, shortcut or not, be made into a time machine by moving its mouths (Morris, Thorne & Yurtsever 1988) or by gravitational time dilation?
  - do semiclassical effects prevent it (Hawking's 1992 conjecture; Kim & Thorne 1991; Kay, Radzikowski & Wald 1997)?

  Distinguish theorem from conjecture throughout.
- **"Create" and "widen."**
  - *Create:* produce a wormhole in a spacetime that has none, by topology change, by pair creation of black holes joined by a bridge, or by enlarging a microscopic or primordial wormhole.
  - *Widen:* increase the throat size, or the time it stays traversable, of an existing wormhole.

### Admissible physics
- **Established:**
  - classical GR in 4D;
  - QFT on curved spacetime and semiclassical gravity (G_μν = 8π⟨T_μν⟩);
  - proven energy inequalities and ANEC theorems, within their stated assumptions.
- **Established theoretical frameworks that are not our universe:** AdS/CFT holography and 2D Jackiw–Teitelboim (JT) gravity, used by Gao–Jafferis–Wall and Maldacena–Qi. The analysis must say what transfers to asymptotically flat 4D spacetime.
- **Speculative, allowed only when labelled:**
  - hypothetical dark sectors and extra dimensions, as Maldacena–Milekhin 2020 needs;
  - magnetic monopoles in the amounts required;
  - modified gravity (Einstein–Gauss–Bonnet, f(R), Horndeski, braneworlds) whose effective stress tensor violates the NEC;
  - phantom fields;
  - quantum-gravity topology change and quantum-foam wormholes.

### Horizon for "viable"
- **In principle:** consistent with established physics plus labelled extensions, with unlimited resources.
- **In practice:** with technology plausible within about 100 years.

For each, give the orders-of-magnitude gap.

## Hidden premises to test
1. **That "sooner than light through the surrounding space" is well defined for every construction.** Two-sided wormholes have no surrounding space. One-sided ones need a stated synchronisation. The traveller's proper time can be short even when the arrival seen from outside is late.
2. **That holding a wormhole open requires "negative energy" in the sense the question means.** Pointwise NEC violation at a throat is forced in GR (flare-out, Hochberg–Visser). The decisive quantity may instead be ANEC along the throat geodesic, together with whether that geodesic is achronal.
3. **That the post-2016 constructions avoid negative energy.** They may instead get it from ordinary quantum fields (Casimir-like vacuum energy), so "ordinary matter" need not mean "no negative energy". The "no exotic matter" claim of Blázquez-Salcedo, Knoll and Radu rests on classical Dirac fields and symmetry assumptions that critics dispute.
4. **That a wormhole that is not a shortcut is useless.** It might still save the traveller proper time, give a private channel, or test quantum gravity.
5. **That the self-consistent achronal ANEC is established.** It is a conjecture with partial proofs, and violations are claimed in backgrounds that are not self-consistent. If it fails, shortcuts and time machines are back on the table.
6. **That a shortcut leads to a time machine, and that chronology protection stops it.** Both links are argued, not proven. Also test whether a long, non-shortcut wormhole could become a time machine through mouth motion.
7. **That the 2022 quantum-processor experiment created or tested a wormhole.** It ran a teleportation protocol on a few qubits with a learned Hamiltonian. Whether its dynamics are gravitational is contested.
8. **That astronomical searches constrain the wormholes in question.** Most searches assume a classical Ellis-type or negative-mass lens. The semiclassical constructions look from outside like black holes, some near-extremal and magnetically charged.
9. **That a wormhole can be created at all.** Topology-change theorems (Geroch 1967; Tipler 1977) restrict classical creation. Pair creation of connected black holes, or growth from microscopic wormholes, are quantum routes with uncertain rates.
10. **That a payload can be scaled up.** Bounds on how much energy and information can pass (Maldacena, Stanford & Yang 2017; Freivogel et al.), and back-reaction, may cap payloads far below 1 kg for the constructions that work.
11. **That results from AdS and from 2D models carry over to 4D asymptotically flat spacetime.**

## What counts as an answer
- **A table with one row per construction:**
  - Morris–Thorne, for example the Ellis–Bronnikov throat;
  - Visser thin-shell wormholes, including the polyhedral (cubic) ones;
  - Gao–Jafferis–Wall, with Maldacena–Stanford–Yang;
  - Maldacena–Qi;
  - Maldacena–Milekhin–Popov;
  - Fu–Grado-White–Marolf 2018 (self-supporting quotients) and 2019 (asymptotically flat, short transit times);
  - Maldacena–Milekhin 2020;
  - Blázquez-Salcedo–Knoll–Radu 2021, with its critiques and any later Einstein–Dirac–Maxwell work.

  Columns:
  - one- or two-sided;
  - what holds it open;
  - pointwise energy conditions violated;
  - ANEC along the throat: its sign, and the computed value or the reproduced published value;
  - whether the throat geodesic is achronal;
  - T_thru against T_ext (shortcut or not), and the traveller's proper time;
  - size, mass and charge scales;
  - stability;
  - status: peer-reviewed or not, and the critiques.
- **Calibrated answers to Q1–Q4,** with credences, separating in principle from in practice.
- **The role of the two cruxes,** the self-consistent achronal ANEC and chronology protection: what each forbids, the evidence for each, and what a violation would imply.
- **For each surviving construction, what creating or widening it would take** for a single qubit, 1 kg and a human:
  - mass, energy, magnetic charge or field;
  - environment, for example isolation from the cosmic microwave background;
  - timescales;
  - the orders-of-magnitude gap to demonstrated technology, and the technology readiness level (TRL).
- **The nearest tests.** For each one: what it would actually test, the sensitivity required against what has been achieved, and a realistic date. Cover:
  - the 2022 Sycamore experiment and its critiques;
  - microlensing searches for negative-mass and Ellis-type lenses;
  - black-hole shadows (EHT);
  - gravitational-wave echoes;
  - searches for magnetically charged black holes;
  - laboratory tests of negative energy and QEIs (Casimir measurements, squeezed light).

## Research facets
Added on 2026-10-08, after the first dossier, to scope the relaunch that brings in the 2026-10-01 warp-drive run (see Prior runs). The research notes already exist: extend them, and carry from that run only what bears on this question. Each facet carries only the items listed for it.
- **theory:** the wormhole metrics and the theorems with their assumptions. From the warp run, carry the superluminal-travel and time-advance theorems (Olum 1998; Visser, Bassett & Liberati 2000; Gao & Wald 2000 with its caveat on K′; Penrose–Sorkin–Woolgar; the positive-mass theorems) and the compactness bounds where they bear on thin shells. Leave the warp-only theorems (Natário; Santiago, Schuster & Visser) behind unless the argument transfers to a throat. Leaves numbers to quantitative and objections to critiques.
- **quantitative:** throat sizes, masses, ρ + p, ANEC values, payload and information bounds. From the warp run, carry the quantum-inequality bounds and the thickness bounds on negative-energy regions (Ford–Roman, Pfenning–Ford, Fewster), each with its assumptions and sampling conventions. Leave warp-bubble energy budgets behind.
- **critiques:** objections to each construction and the no-go results. From the warp run, carry objections to "no exotic matter" claims where the same argument applies to holding a throat open, and the horizon and instability results for superluminal configurations (Everett–Roman; Finazzi, Liberati & Barceló) as they bear on shortcuts.
- **engineering:** laboratory negative energy, the quantum-processor experiments, astronomical searches, and the routes to creating a wormhole. From the warp run, carry the demonstrated Casimir energies and pressures, the squeezed-light negative energy densities, and the demonstrated-capability anchors used for orders-of-magnitude gaps.
- **frontier:** wormhole and energy-condition work of the last five years, newest first. From the warp run, carry its recent energy-condition results only where they bear on wormholes, then search for work newer than 2026-10-01.

## Worked calculations
Lenses run at the same time and can't read each other's work. Each item below has one owner, and the owner's result is the reference the slate builder, the refuters and the judge use. Another lens that needs the number computes its own and says so.
- **constraints: the energy-condition table.** For each construction: the sign and size of ρ + p along the throat; the ANEC integral along the radial null geodesic; whether that geodesic is achronal in the full spacetime. Use `wormhole_tools.py` for the Morris–Thorne, Ellis and thin-shell rows; for the perturbative constructions, reproduce the published integral and say which values are quoted rather than recomputed.
- **examiner: the shortcut test.** For each one-sided construction, T_thru/T_ext and τ_thru at stated observer radii, with the synchronisation stated. For each two-sided construction, whether anything arrives earlier than, or without, the boundary-coupling channel.
- **mechanist: the time-machine conversion.** For mouth motion (Morris, Thorne & Yurtsever 1988) and for gravitational time dilation: the mouth speed, duration or potential difference needed for closed timelike curves at a given mouth separation, and whether the throat geodesic becomes chronal.
- **engineer: the cost table.** For each surviving construction, creating or widening it for a qubit, 1 kg and a human: mass, energy, charge or field, environment, timescale, the orders-of-magnitude gap and the TRL. Also the required sensitivity against the achieved one for each nearest test.

## Known constraints, prior attempts, and user-supplied data

Leads from the framing, to verify; none has been checked yet:
- **Classical wormholes:**
  - Morris & Thorne 1988 (Am. J. Phys.);
  - Morris, Thorne & Yurtsever 1988 (PRL), on turning wormholes into time machines;
  - Visser 1989, on thin-shell and polyhedral wormholes;
  - Poisson & Visser 1995, on thin-shell stability;
  - Visser's book "Lorentzian Wormholes" (1995);
  - the often-quoted figure of about a Jupiter mass of exotic matter for a 1 m throat.
- **Theorems and bounds:**
  - topological censorship (Friedman, Schleich & Witt 1993);
  - Hochberg & Visser 1997–98: a generic throat requires NEC violation;
  - Gao & Wald 2000: the time-delay theorem;
  - Ford & Roman 1996: QFT constrains wormhole geometries, with exotic matter confined to thin bands;
  - Visser, Kar & Dadhich 2003: arbitrarily small violations;
  - Graham & Olum 2007: the self-consistent achronal ANEC rules out closed timelike curves, and wormholes connecting different asymptotically flat regions;
  - Urban & Olum 2010;
  - Wall 2010: the achronal ANEC from the generalised second law;
  - Kontou & Olum 2015;
  - proofs of ANEC in flat space (Faulkner et al. 2016; Hartman, Kundu & Tajdini 2017);
  - the Kontou & Sanders 2020 review of energy conditions.
- **Chronology protection:** Hawking 1992; Kim & Thorne 1991; Kay, Radzikowski & Wald 1997; Frolov & Novikov 1990.
- **Constructions since 2016:**
  - Gao, Jafferis & Wall (arXiv:1608.05687; JHEP 2017);
  - Maldacena, Stanford & Yang 2017 (arXiv:1704.05333);
  - Maldacena & Qi 2018 (arXiv:1804.00491);
  - Maldacena, Milekhin & Popov 2018 (arXiv:1807.04726);
  - Fu, Grado-White & Marolf 2018 (arXiv:1807.07917) and 2019 (arXiv:1908.03273);
  - Maldacena & Milekhin 2020 (arXiv:2008.06618; PRD 2021);
  - Blázquez-Salcedo, Knoll & Radu 2021 (arXiv:2010.07317; PRL);
  - critiques and follow-ups, including Konoplya & Zhidenko 2022 (PRL) and Kain 2023;
  - Freivogel et al. 2019, on bounds on information transfer.
- **Experiment and observation:**
  - Jafferis et al. 2022 (Nature 612, 51), the critique by Kobrin, Schuster & Yao 2023, and the authors' reply;
  - Brown et al., "Quantum gravity in the lab" (teleportation by size);
  - Cramer et al. 1995, natural wormholes as gravitational lenses;
  - Takahashi & Asada 2013, an SDSS bound;
  - Abe 2010;
  - Dai & Stojkovic 2019;
  - Cardoso, Franzin & Pani 2016, ringdown echoes;
  - Garfinkle & Strominger 1991, pair creation of magnetically charged black holes.
- **Toolkit:** `gr_tensors.py` has the Morris–Thorne metric with Φ(r) and b(r), and its ρ = b'/(8πr²) is checked. It has no ANEC line integral and no thin-shell junction conditions. A calculator for both, `wormhole_tools`, was confirmed at framing, built during research, and promoted into the toolkit as `.claude/skills/conundrum/scripts/wormhole_tools.py` after its self-test passed (38/38); use that copy.
- **User-supplied data:** none so far.

## Prior runs
- 2026-10-01-warp-drive-without-negative-energy (2026-10-01): update. A complete, source-checked deep run on negative energy for warp drives. Its energy-condition theorems, quantum-inequality bounds, superluminal-travel theorems and laboratory negative-energy measurements bear on Q1 and Q2. Added at the user's request on 2026-10-08, after the first dossier had been compiled without it.
- 2026-09-29-alcubierre-negative-energy (2026-09-29): ignore. A quick run whose sources were never checked. The 2026-10-01 run took it as leads and re-found and checked what it needed.
- 2026-09-29-warp-bubble-shapes (2026-09-29): ignore. A partial, unchecked run on warp-bubble shapes.
- 2026-09-29-problem-of-time-quantum-gravity (2026-09-29): ignore. Unrelated.
- 2026-09-30-neutron-lifetime-beam-bottle (2026-09-30): ignore. Unrelated.
