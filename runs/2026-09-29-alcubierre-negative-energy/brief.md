# Brief: Negative-energy options for a superluminal Alcubierre-type drive
slug: 2026-09-29-alcubierre-negative-energy | depth: quick | type: feasibility | date: 2026-09-29

## Question as asked
"Considering Alcubierre drives, what are viable engineering options for the negative energy required to travel at superluminal effective speeds?"

Scope set by the user at framing:
- Judge viability both in principle (GR plus QFT) and in practice (buildable this century).
- Cover ways to supply the negative energy: Casimir and squeezed-vacuum sources, and exotic matter.
- Cover ways to shrink or avoid it: Van Den Broeck's geometry, Natário's zero-expansion drive, White's thick-wall and oscillating variants, and the recent positive-energy claims (Lentz; Bobrick and Martire; Fell and Heisenberg) together with their critiques.
- For each option, give the energy required (in solar or Jupiter masses, or kg, in scientific notation) against what has been demonstrated, the orders-of-magnitude gap, and how it scales with bubble radius, wall thickness and speed.
- Treat quantum-inequality limits on wall thickness, horizons and causality, and tidal forces on the ship as constraints.

## Question made precise
- **Warp drive.** A spacetime of the Natário class, ds² = −c²dt² + δ_ij (dx^i − β^i dt)(dx^j − β^j dt), whose shift β carries a region of nearly flat space at speed v along x. Alcubierre's drive has β = (v f(r_s), 0, 0), with f = 1 inside the bubble radius R and f = 0 outside a wall of thickness Δ. Variants that also change the lapse or the spatial metric count as warp drives if they carry a ship-sized, nearly flat region; this covers Van Den Broeck, Lentz, Bobrick–Martire and Fell–Heisenberg. Wormholes and Krasnikov tubes are out of scope, except as a reframe or as pre-laid infrastructure.
- **Wall thickness.** Conventions differ, so every number states which one it uses:
  - Alcubierre uses the steepness σ.
  - Pfenning–Ford use Δ = (1 + tanh²σR)² / (2σ tanh σR), which is about 2/σ for σR ≫ 1.
  - For v in units of c and G = c = 1, a tanh profile gives E ≈ −v²R²/(18Δ). Pfenning–Ford's linear ramp gives −v²R²/(12Δ).
- **Superluminal effective speed.** Measured in the asymptotically flat exterior where the trip starts and ends. The bubble goes between two points at rest there in less time t than light would take through empty space, so v > c. Here t is the proper time of those points, and of a ship at the bubble's centre, which moves on a geodesic. Locally, the ship never outruns light.
- **Negative energy.** An observer with 4-velocity u measures the energy density ρ_u = T_μν u^μ u^ν.
  - The default budget is the Eulerian energy (normal observers to the t = const slices), integrated over a slice. E_− is the integral of its negative part and E_tot is the full integral.
  - Convert to mass with M = |E|/c², and report in kg and in M_sun (1.989e30 kg) or M_J (1.898e27 kg).
  - A drive needs negative energy if any observer measures ρ_u < 0 (the weak energy condition fails), or if the null energy condition fails. Positive energy for Eulerian observers alone doesn't settle it.
- **Viable engineering option.** One of:
  - a concrete way to source the stress-energy the metric needs, meaning the energy density and the stresses and fluxes that go with it, at the required place, size and duration;
  - a change of geometry that needs less negative energy, or none.

  In either case the whole package has to work: supply, geometry, creating and controlling the bubble, and the ship's survival.
- **Admissible physics.**
  - **Established:** classical GR, and QFT on curved spacetime with semiclassical gravity (G_μν = 8πG⟨T_μν⟩/c⁴). This includes the proven quantum inequalities and the averaged null energy condition, where their assumptions hold.
  - **Conjectures** such as quantum interest and chronology protection may be used when labelled as conjectures.
  - **Speculative extensions** are allowed only when labelled [speculative]: extra dimensions and brane worlds, Einstein–Cartan torsion, modified gravity, non-minimally coupled or phantom fields, negative-mass matter. They never count toward "viable in principle under established physics".
- **Horizon for "viable".** Give two verdicts for each option:
  - **In principle:** consistent with the admissible physics, and under which assumptions.
  - **In practice:** buildable by 2100, from demonstrated capability plus credible extrapolation, with a technology readiness level (TRL).
- **Constraints every option must pass:**
  - **Quantum inequalities:** how thin the wall can be, and how long and how large a negative-energy region can be.
  - **Horizons:** at v > c the ship cannot signal the front wall. Can it create, steer or stop the bubble? A pre-laid track counts as an option if labelled.
  - **Causality:** whether superluminal bubbles allow closed timelike curves.
  - **Semiclassical stability:** Hawking-like flux, and growth of the renormalized stress-energy at horizons.
  - **Tidal forces:** on the ship and crew, using the tidal tensor rather than raw Riemann components; also on what the bubble passes or arrives at.

## Hidden premises to test
1. **That superluminal warp drives must violate an energy condition at all.**
   - Lentz (2021), Bobrick & Martire (2021) and Fell & Heisenberg (2021) claim positive energy, for some observers or only below light speed.
   - Olum (1998), Visser, Bassett & Liberati (2000) and Santiago, Schuster & Visser (2022) argue the opposite.
   - Which claims are superluminal, and which energy condition holds for which observers?
2. **That total Eulerian energy is the right budget.**
   - Casimir-type sources come with a specific stress tensor, with large pressures, and exist only next to positive-energy matter.
   - Quantum inequalities limit density × duration and size, not the total.
3. **That published reductions compare like with like:** the same R, Δ and its convention, v, and energy measure.
4. **That lab negative energy can be scaled, concentrated into a wall, and separated from its positive-energy source.** The source can be the plates, the cavity walls or the compensating pulse.
5. **That the geometry tricks leave a usable ship.**
   - Van Den Broeck's pocket hangs on a neck a few orders of magnitude above the Planck length.
   - A thick wall shrinks the flat interior.
   - Natário's drive still has negative Eulerian energy density.
6. **That the ship can create, steer and stop the bubble from inside,** given the horizon at v > c.
7. **That exotic-matter candidates supply negative energy in the GR sense.** For example, "negative effective mass" in condensed matter isn't negative energy density.

## What counts as an answer
- **A ranked list of options.** For each one:
  - its mechanism;
  - the energy it requires: E_−, plus E_tot where they differ, in kg and in M_sun or M_J;
  - the best demonstrated value of the same quantity, with its source;
  - the gap in orders of magnitude, in total energy and in energy density, and in wall thickness and duration where those bind;
  - its scaling exponents in R, Δ and v;
  - the binding constraint;
  - an in-principle verdict, with the theorem or bound that decides it;
  - an in-practice verdict for 2100, with its TRL.
- **A common reference case, so options compare like with like.**
  - A flat ship region of radius about 100 m: R = 100 m for Alcubierre, the pocket radius for Van Den Broeck.
  - v = 10c, which covers 4.37 ly (Alpha Centauri) in about 0.44 yr.
  - Δ = 1 m, and also Δ at the quantum-inequality limit.
  - When a paper uses other parameters (often v = c), give its own number and the converted one, and mark the conversion as ours.
- **A status for each positive-energy claim:**
  - superluminal or not;
  - which energy conditions it meets, for which observers;
  - whether it survived published critique.
- **The null and a reframe, ranked alongside the options.** The null is "no viable option within admissible physics".
- **Demonstrated lab values.** Quick depth has no engineering facet, so the quantitative research should record them:
  - Casimir energy and energy density at measured gaps and areas;
  - squeezed-vacuum negative energy density and duration;
  - any claimed exotic-matter measurement.

## Known constraints, prior attempts, and user-supplied data
Earlier work in this repository, not literature values. Reuse its sources, but re-open a source before quoting it, and recheck numbers before relying on them.
- **`runs/2026-09-29-warp-bubble-shapes/research/shapes.md`:** 26 sourced claims by one researcher on energy-reducing geometries, with its gaps listed. It had no separate source check. It covers:
  - White's "Warp Field Mechanics" 101 and 102;
  - Van Den Broeck; Loup et al.; Natário; Rodal;
  - Bobrick–Martire, Lentz and Fell–Heisenberg, with the critique by Santiago, Schuster and Visser;
  - Fuchs et al.
- **`examples/smoke-test-constraints-lens/`:** one lens's calculations on a hand-written dossier.
  - A tanh bubble with R = 100 m, Δ = 1 m and v = c needs E = −6.7e46 J, or −7.5e29 kg.
  - The free-field quantum inequality limits the wall to about 51 Planck lengths, which raises that to about −9.0e62 kg.
  - Casimir plates weigh at least 7.7e9 times their energy deficit.
  - The required energy density is 10^33.4 times that of an ideal 1 nm Casimir gap.
  - The Natário-class Eulerian energy density is −|∇×β|²/(32π) ≤ 0.
- **`runs/2026-09-29-warp-bubble-shapes/calc/wall_thickness.py`:** consider a spherical bubble with a flat interior of radius R and a wall of thickness D. No profile beats E_min = −(v²/12) R(R + D)/D (geometric units), which tends to −v²R/12, so thickening has diminishing returns.
- **`runs/2026-09-29-warp-bubble-shapes/calc/interior_tides.py`:** the tidal tensor for R = 50 m, v = c and a 10 m wall.
  - The stretch is 0.04 g/m near the centre, 36 g/m at 10 m out and 2,000 g/m at 15 m.
  - Tides scale as v².
  - Outside the bubble, they exceed 100 g/m out to 170 km.
  - Compute tides this way (the tidal tensor, in mpmath), not from raw Riemann components.

**Toolkit.**
- `gr_tensors.py` has the Alcubierre and Van Den Broeck metrics built in.
- Other drives go in through `Spacetime.from_adm`: Natário, Lentz, Bobrick–Martire, Fell–Heisenberg.
- `unit_tools.py` has `Msun` and `Mjup`.
- This run adds no new calculators.

**Leads for sources the earlier notes lack.** Verify each before use.
- The warp drive and its limits: Alcubierre 1994; Pfenning & Ford 1997; the Ford–Roman quantum inequalities; Lobo & Visser 2004.
- Energy-condition theorems: Olum 1998; Visser, Bassett & Liberati 2000.
- Semiclassical instability: Hiscock 1997; Finazzi, Liberati & Barceló 2009.
- Horizons and causality: Krasnikov 1998; Everett & Roman 1997; Everett 1996.
- Effects on what the bubble meets: McMonigal, Lewis & O'Byrne 2012.
- Casimir measurements: Lamoreaux 1997; Mohideen & Roy 1998; Bressi et al. 2002.
- Squeezed light: Vahlbruch et al. 2016.
- Casimir-cavity claims: White et al. 2021, worldline numerics.
