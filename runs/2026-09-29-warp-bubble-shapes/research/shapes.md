# Research: shapes
Mandate: find the "white paper" on lower-energy warp-bubble shapes, and every other published geometry claimed to lower the energy of an Alcubierre-type drive, with scaling, baseline, assumptions and later disputes.
Access: lit_search INSPIRE ok, arXiv ok (lit_search) but export.arxiv.org API returned nothing (rate-limited), so abstracts were read via the INSPIRE API and full texts via arxiv.org/pdf + pypdf; NTRS API + PDFs ok; WebFetch blocked (jbis.org.uk failed DNS; centauri-dreams.org blocked by proxy). WebFetch domains that worked: none.

Conventions: "E" is the total Eulerian energy on t = const unless stated. "Alcubierre baseline" numbers are for the original tanh shape function. Mass-equivalents use M = E/c^2 (SI). Statements marked [my arithmetic] are my own conversions, not the papers'.

## Claims

### A. The "white paper" candidates (White, NASA JSC)

- [RS-01] CLAIM: White's "Warp Field Mechanics 101" (NTRS 20110015936; DARPA/NASA 100 Year Starship Symposium, Orlando, 30 Sep 2011; document type CONFERENCE_PAPER) is the source of the "thicker wall = less energy" claim. For the Alcubierre tanh-shell metric at fixed target velocity and bubble radius R, White finds that thickening the wall sigma greatly reduces the required peak energy density and the integrated energy "orders of magnitude", at the cost of shrinking the flat interior. The text gives no closed-form scaling in R, v or sigma and no total-energy number in SI. The plotted case is v = 10c, 10 m diameter volume (from the companion slides). Baseline: the same bubble with a thin wall. Assumption: Alcubierre metric, Eulerian energy density T00 = -(1/8pi) v^2 rho^2/(4 r^2) (df/dr)^2, no quantum-inequality constraint on wall thickness is discussed.
  SOURCE: White, H., "Warp Field Mechanics 101", 100YSS 2011 conference paper, https://ntrs.nasa.gov/api/citations/20110015936/downloads/20110015936.pdf
  QUOTE: "as the warp bubble is allowed to get thicker, the required density is drastically greatly reduced, but the toroid grows from a thin equatorial belt to a diffuse donut. The advantage of allowing a thicker warp bubble wall is that the integration of the total energy density for the right-most field is orders of magnitude less that the left-most field. The drawback is that the volume of the flat space-time in the center of the bubble is reduced."
  ACCESS: full-text
  STATUS: preprint (NTRS conference paper; see RS-03 for the JBIS version)
  CONFIDENCE: high

- [RS-02] CLAIM: The same paper calls this its own new result and admits the SI total is still hard. Its conclusion says the peak energy density "can be greatly reduced by allowing the wall thickness of the warp bubble to increase", and that the analysis "also indicate[s] a corresponding reduction in total energy when converted from geometric units (G=c=1) to SI units, but still show[s] that the idea will not be an easy task." It does not address the quantum-inequality limit on wall thickness (Pfenning-Ford, RS-07).
  SOURCE: White 2011, same PDF as RS-01 (conclusion)
  QUOTE: "A significant finding from this effort new to the literature is that for a target velocity and spacecraft size, the peak energy density requirement can be greatly reduced by allowing the wall thickness of the warp bubble to increase."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: high

- [RS-03] CLAIM: A peer-reviewed-journal version exists: JBIS 66 (2013) 242-247, titled "Warp Field Mechanics 101" (author H. White). The title was confirmed by a WebSearch summary (ADS entry 2013JBIS...66..242W) and the citation by Lentz's reference list (INSPIRE: journal J.Br.Interplanet.Soc., vol 66, 2013, pp 242-7). I could not open the JBIS/ADS page, so I have not checked whether the JBIS text differs from the NTRS text.
  SOURCE: Lentz 2020 reference list via INSPIRE API (arXiv:2006.07125 references: "White H 2013 Journal of the British Interplanetary Society 66 242-247"); search result "Warp Field Mechanics 101 - ADS", https://ui.adsabs.harvard.edu/abs/2013JBIS...66..242W/abstract
  SUMMARY: "The paper 'Warp Field Mechanics 101' was authored by Harold G. White and published in 2013 in the Journal of the British Interplanetary Society, volume 66, pages 242-247."
  ACCESS: search-summary
  STATUS: secondary
  CONFIDENCE: medium

- [RS-04] CLAIM: "Warp Field Mechanics 102: Energy Optimization" (NTRS 20130011213, JSC-CN-28185, Jan 2013) is a slide deck (NTRS type PRESENTATION), not a paper, and is not peer reviewed. It is the item whose title matches "energy" and "shapes". Its slides (a) show the tanh-shell energy density and York time for <v> = 10c and a 10 m diameter volume at several wall thicknesses, headed "Bubble Topology Optimization"; (b) say "Changing topology greatly reduces the energy required" and "But space-time is really stiff: c^4/8piG"; (c) propose oscillating the bubble intensity, using a Chung-Freese brane-world metric so that dU/dt ~ c in the bulk and the effective stiffness of spacetime drops ("Reduces stiffness of spacetime!"); (d) plot "Exotic Mass Warp Requirements" for a 10 m diameter bubble at v = 10c against shell-thickness fraction and bulk velocity dU/dt, with reference masses (Jupiter 1.9x10^27 kg, Earth 6.0x10^24 kg, ...). The plot is a scanned image, so its numeric values could not be extracted; the axis labels and reference masses are garbled OCR. "Topology" here means the wall-thickness change from thin toroidal belt to a fat donut, not a new spacetime topology. The oscillation and higher-dimension "stiffness" step is a conjecture with no derivation in the deck.
  SOURCE: White, H., "Warp Field Mechanics 102: Energy Optimization", NASA JSC presentation, https://ntrs.nasa.gov/api/citations/20130011213/downloads/20130011213.pdf
  QUOTE: "Changing topology greatly reduces the energy required / But space-time is really stiff: c4/8πG / Can we further reduce the energy required by reducing the stiffness? / Maybe…but we need to engage higher dimensional models to do so"
  ACCESS: full-text
  STATUS: fringe (unrefereed slides; the oscillation/bulk-velocity trick is unsupported speculation)
  CONFIDENCE: high for what the slides say; low for the physics of the oscillation idea

- [RS-05] CLAIM: The "Jupiter to Voyager 1" comparison is on White's own slide, as a plot and not in words. Slide 16 of "Warp Field Mechanics 102" (NTRS 20130011213), titled "Exotic Mass Warp Requirements, 10m diameter, v_apparent = 10c", plots total exotic mass (kg, 10^0 to 10^28) against shell thickness fraction (10^-5, "thinner bubble/ring", to 10^0, "thicker bubble/ring", "no flat space left in bubble"), with one curve per bulk velocity dU/dt (0c, 0.9c, 0.999c, 0.99999c, 0.9999999c, 0.999999999c). Reference masses run from Jupiter (1.9x10^27 kg) down to Voyager, with a Jupiter photo pinned to the top-left and a Voyager photo to the bottom-right. Read off the plot by eye (approximate): the thin-shell, no-oscillation curve sits near 10^28 kg (Jupiter class) and the thickest-shell, fastest-oscillation curve near 10^3 kg (Voyager class; slide 2 gives Voyager 1 as 0.722 t). The dU/dt dependence comes from a speculative bulk-velocity (Chung-Freese null-geodesic) relation shown on the slide, not from standard GR. [Corrected by the orchestrator after rendering the slide to an image; the researcher's first version said the figure was not in the NTRS documents and rested on press summaries only.]
  SOURCE: White, "Warp Field Mechanics 102: Energy Optimization", NASA JSC, Jan 2013, slides 2 and 16, https://ntrs.nasa.gov/api/citations/20130011213/downloads/20130011213.pdf
  QUOTE: "Exotic Mass Warp Requirements, 10m diameter, v apparent=10c" (slide 16 title); "Voyager 1 mission: 0.722 t spacecraft" (slide 2). The plot values themselves are read from the rendered image, not from text.
  ACCESS: full-text
  STATUS: fringe
  CONFIDENCE: medium

- [RS-06] CLAIM: No published rebuttal aimed specifically at White's thick-wall or oscillation claims was found. The thick-wall scaling itself agrees with the standard Alcubierre result E ~ v^2 R^2/Delta (RS-07, RS-13), so thickening does reduce E at fixed R; the objection is that (i) quantum-inequality analysis for free fields forces Delta to ~100 Planck lengths (RS-07), and (ii) a thick wall leaves little or no flat interior ("no flat space left in bubble" on the 102 plot). Rodal (2025 preprint) refutes a different "low-energy warp drive via engineered gravitational coupling" idea (RS-22), not White's.
  SOURCE: synthesis of RS-01, RS-04, RS-07
  SUMMARY: (no single source; absence of rebuttal recorded under Gaps)
  ACCESS: search-summary
  STATUS: secondary
  CONFIDENCE: medium

### B. Baseline and quantum-inequality limits

- [RS-07] CLAIM: Pfenning and Ford (1997) give the Alcubierre baseline. For a constant-velocity bubble with the thin-shell approximation, E = -(1/12) v_b^2 (R^2/Delta + Delta/12) (G = c = 1, Eulerian energy integrated over proper volume at t = 0). The quantum inequality (free massless scalar field, sampling time set by the minimum curvature radius) limits the wall to Delta <= 10^2 v_b L_Planck (evaluated for a parameter alpha = 1/10). For R = 100 m this gives E <= -6.2x10^65 v_b grams (= -6.2x10^62 v_b kg), about 10 orders of magnitude above the mass of the visible universe. If Delta = 1 m were allowed, the paper says "on the order of a quarter of a solar mass". [my arithmetic: (1/12)(100 m)^2/(1 m) x c^2/G = 1.12x10^30 kg = 0.56 M_sun for v_b = 1, i.e. 1.5x our smoke-test 1/18 coefficient, and about twice the "quarter solar mass" in the text; E scales as v^2 R^2/Delta, and since Delta_max ~ v the QI-limited total scales ~ v.]
  SOURCE: Pfenning, M.J. and Ford, L.H., 1997, "The unphysical nature of 'warp drive'", Class. Quantum Grav. 14, 1743, arXiv:gr-qc/9702026
  QUOTE: "It will be shown that the bubble wall thickness is on the order of only a few hundred Planck lengths. Then we will show that the total integrated energy density needed to maintain the warp metric with such thin walls is physically unattainable." (abstract); "E ≤ −6.2 × 10^70 v_b L_Planck ∼ −6.2 × 10^65 v_b grams" (Eq. 29); "For every order of magnitude by which the velocity increases, the total negative energy required to generate the warp drive metric also increases by the same magnitude." (Sec. 5)
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RS-08] CLAIM: Scope limit on RS-07. The quantum-inequality wall bound was derived for a free massless scalar field in a locally flat region. Loup et al. and Bobrick-Martire both argue that it does not bind sources that are not free quantum fields, and Krasnikov (2003) argues large E_tot need not exclude "shortcuts". So the 10^62 kg baseline is a semiclassical free-field estimate, not a theorem about all matter.
  SOURCE: Krasnikov, S., 2003, "The Quantum inequalities do not forbid space-time shortcuts", Phys. Rev. D 67, 104013, arXiv:gr-qc/0207057 (abstract via INSPIRE); Loup, Waite, Halerewicz 2001, arXiv:gr-qc/0107097 (full text)
  QUOTE: "By explicit examples I prove that: 1) the relevant quantum inequality does not (always) imply large energy densities: 2) large densities may not lead to large values of E_tot: 3) large E_tot, being physically meaningless in some relevant situations, does not necessarily exclude shortcuts." (Krasnikov abstract); "Pfenning applied [7] a quantum inequality for a free, massless scalar field to the Alcubierre warp even though the Alcubierre spacetime is not the result of a free, massless scalar field." (Loup et al.)
  ACCESS: abstract (Krasnikov), full-text (Loup)
  STATUS: peer-reviewed (Krasnikov); preprint (Loup)
  CONFIDENCE: medium

### C. Modified spatial geometry

- [RS-09] CLAIM: Van Den Broeck (1999) multiplies the spatial metric by a conformal factor B(r_s) so that a microscopic Alcubierre bubble encloses a large flat "pocket" (ds^2 = -dt^2 + B^2[(dx - v_s f dt)^2 + dy^2 + dz^2]). His worked example: alpha = 10^17 (B = 1 + alpha inside), inner radius R~ = 10^-15 m, transition width Delta~ = 10^-15 m, outer bubble radius R = 3x10^-15 m, so the pocket has a 200 m inner diameter. Energies (Eulerian, t = 0, G = c = 1 converted to kg): wall region IV E ~ -6.3x10^29 v_s kg; region II negative part -1.4x10^30 kg, positive part +4.9x10^30 kg, i.e. "a few solar masses" of negative energy plus a comparable positive amount. Baseline: Pfenning-Ford E ~ -6.2x10^62 v_s kg for a 100 m radius bubble. Reduction: about 32 orders of magnitude (from 10^62 to 10^30 kg). Assumptions: wall thickness at the QI limit Delta <= 10^2 v_s L_P; B is a degree-80 polynomial chosen to avoid sub-Planck curvature radii (minimum curvature radius 1.4x10^-34 m, "about ten Planck lengths"); QI checked only for Eulerian observers.
  SOURCE: Van Den Broeck, C., 1999, "A 'warp drive' with reasonable total energy requirements", Class. Quantum Grav. 16, 3973, arXiv:gr-qc/9905084
  QUOTE: "A spacetime is presented for which the total negative mass needed is of the order of a few solar masses, accompanied by a comparable amount of positive energy. This puts the warp drive in the mass scale of large traversable wormholes." (abstract); "Apart from the fact that the total energies are of stellar magnitude, there are the unreasonably large energy densities involved, as was equally the case for the original Alcubierre drive." (Sec. 4)
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RS-10] CLAIM: Van Den Broeck himself, in the same paper, says the result "doesn't mean that the proposal is realistic", the structure still has sizes "only a few orders of magnitude above the Planck scale", and the drive still needs unreasonable energy densities; in a follow-up review he concludes superluminal bubbles "seem an unlikely possibility" while "subluminal bubbles may still be possible".
  SOURCE: Van Den Broeck, C., 1999, "On the (im)possibility of warp bubbles", arXiv:gr-qc/9906050 (preprint, no journal ref per INSPIRE); gr-qc/9905084 Sec. 4
  QUOTE: "Superluminal warp bubbles seem an unlikey possibility within the framework of general relativity and quantum field theory, although subluminal bubbles may still be possible." (abstract of gr-qc/9906050, spelling as printed)
  ACCESS: abstract
  STATUS: preprint
  CONFIDENCE: high

- [RS-11] CLAIM: DISPUTED. Bobrick and Martire (2021) argue the Van Den Broeck solution is equivalent to Alcubierre once written in the inner observer's coordinates, and that the low energy quoted for the inner region comes from its energy expression lacking the dependence on B(0) and velocity: they expect the inner-region energy to scale with B(0)^2 v_s^2. They also note the outer wall is still 100 v_s Planck lengths thick, so the Planck-scale-thin wall remains. This is a derivation in their appendix, not a numerical recomputation, and I did not find a reply from Van Den Broeck.
  SOURCE: Bobrick, A. and Martire, G., 2021, "Introducing Physical Warp Drives", Class. Quantum Grav. 38, 105009, arXiv:2102.06824, Appendix A.2
  QUOTE: "Therefore, in summary, the Van Den Broeck solution is equivalent to the Alcubierre solution." ... "the total energy in the inner Region 1, and of the Van Den Broeck metric as a whole, is comparable to that of the standard Alcubierre solution of similar dimensions. Our derivation suggests that the total energy should be proportional to B(0)^2, through the v_s^2 term. The absence in the van den Broeck expression for Region 1 of dependence on B(0) or on the velocity at all, potentially explains why the energies they obtain for that region are small."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: medium (their argument is a rebuttal by derivation; no independent numerical check found)

### D. Lapse-function modification

- [RS-12] CLAIM: Loup, Waite and Halerewicz (2001) insert a lapse function A(ct, rho) into the Alcubierre metric and claim the ship-frame energy density falls as 1/A^4 (T00 = -(v_s^4 c^4/8piG)(dg/drho)^2 sin^2(theta)/A^4), "reducing the negative energy requirements ... arbitrarily as a function of A". Their QI analysis says a large A also raises the minimum allowed wall thickness (Delta <= 10^2 (v/c) l_P A0), so they divide Pfenning's "-0.068 solar mass" figure by A0^4 for "several orders of magnitude" more. Baseline: Pfenning-Ford, with their solar-mass-scale case (thick wall) rather than the 10^62 kg case. Key assumptions: A is nearly constant through the negative-energy region; only the "ship frame" energy is reduced, and they concede the WEC is still violated in other frames. It is an arXiv preprint (INSPIRE lists no journal ref; Lentz's reference list prints a JBIS URL, "2013.66.242", after this entry, which matches the White 2013 JBIS item, so it looks like a misplaced link and does not show Loup et al. was refereed); the first author lists a personal address and says the work "does not reflect" his employer. I found no published critique of it and only 7 citations on INSPIRE; treat as unrefereed and not independently checked.
  SOURCE: Loup, F., Waite, D., Halerewicz, E. Jr., 2001, "Reduced total energy requirements for a modified Alcubierre warp drive spacetime", arXiv:gr-qc/0107097
  QUOTE: "It can be shown that negative energy requirements within the Alcubierre spacetime can be greatly reduced when one introduces a lapse function into the Einstein tensor. Thereby reducing the negative energy requirements of the warp drive spacetime arbitrarily as a function of A(ct,ρ)." (abstract); "Since the ship forms the warp, satisfying that there is very little ship frame negative energy may be enough."
  ACCESS: full-text
  STATUS: preprint
  CONFIDENCE: medium for what it claims; low that the result is sound

### E. Shape-function and flattening optimisation

- [RS-13] CLAIM: Bobrick and Martire (2021) give a shape optimisation of the Alcubierre drive itself. With Alcubierre's Eulerian energy E = -(v_s^2/16) integral dx integral rho d rho (df/d rho)^2, flattening the bubble along the direction of travel by a factor alpha_X (f(x - x_s, rho) -> f(alpha_X (x - x_s), rho)) gives E -> E/alpha_X. Choosing alpha_X = 1 + v^2 gives E -> E/(1+v^2), asymptotically removing the velocity dependence of E. The energy-optimal radial shape from a variational calculation is f = min(r0/r_s, 1), which lowers |E| by "about a factor of three" relative to Alcubierre's tanh shape for a similar size. The abstract advertises "optimizations for the Alcubierre metric that decrease the negative energy requirements by two orders of magnitude"; the body text I read shows the 1/alpha_X law and the factor-3 result, and I inferred (not verified) that the two orders correspond to alpha_X of order 100. Assumptions: axisymmetric Alcubierre metric; extreme flattening pushes the x-direction thickness to near-Planck scale, which satisfies the quantum inequalities but the paper notes it "does not satisfy the averaged null energy conditions".
  SOURCE: Bobrick, A. and Martire, G., 2021, Class. Quantum Grav. 38, 105009, arXiv:2102.06824, Secs. 4.1-4.2, 5.3, App. A.3
  QUOTE: "flattening the warp drive by a factor of αX (αX > 1) ... leads to the energy reduction by E→ E/αX." ... "Using this slower-decreasing shape reduces the energy requirement for a similarly sized Alcubierre drive by about a factor of three."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high for the 1/alpha_X and factor-3 statements; medium for "two orders" attribution

- [RS-14] CLAIM: Bobrick-Martire's central conceptual result limits every shape trick: "any warp drive, including the Alcubierre drive, is a shell of regular or exotic material moving inertially with a certain velocity. Therefore, any warp drive requires propulsion." They construct subluminal, spherically symmetric, positive-energy warp drives with known physics, and say their conclusions "do not support" Lentz's superluminal positive-energy claim.
  SOURCE: Bobrick and Martire 2021, arXiv:2102.06824 (abstract; Sec. 5.2)
  QUOTE: "We present the first general model for subliminal positive-energy, spherically symmetric warp drives; construct superluminal warp-drive solutions which satisfy quantum inequalities; provide optimizations for the Alcubierre metric that decrease the negative energy requirements by two orders of magnitude" (abstract)
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

### F. Zero-expansion and irrotational flows

- [RS-15] CLAIM: Natário (2002) builds a warp drive with zero expansion (no contraction/expansion of volume elements). The abstract makes no energy-reduction claim, and I found none in the literature: Lobo and Visser (2004) verify that both the Alcubierre and Natário drives violate the classical energy conditions non-perturbatively and, in linearised gravity, "even at low speeds the net (negative) energy stored in the warp fields must be a significant fraction of the mass of the spaceship". Rodal (2024, IJTP) finds Natário's curvature invariants are 35 times larger than Alcubierre's for identical bubble parameters. So the lead "Natário lowers the energy" is dropped; Natário changes the flow, not the energy scale.
  SOURCE: Natário, J., 2002, "Warp drive with zero expansion", Class. Quantum Grav. 19, 1157, arXiv:gr-qc/0110086; Lobo, F.S.N. and Visser, M., 2004, "Fundamental limitations on 'warp drive' spacetimes", Class. Quantum Grav. 21, 5871, arXiv:gr-qc/0406083; Rodal, J., 2024, "A Closer Look at Natário's Zero-Expansion Warp Drive", Int. J. Theor. Phys. 63, 168, arXiv:2512.19837
  QUOTE: "We demonstrate that Natário's spacetime exhibits curvature invariant amplitudes 35 times greater than Alcubierre's, given identical warp-bubble parameters, making Natário's concept even less viable." (Rodal abstract); "For both the Alcubierre and Natario warp drives we find that even at low speeds the net (negative) energy stored in the warp fields must be a significant fraction of the mass of the spaceship." (Lobo-Visser abstract)
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RS-16] CLAIM: Rodal (2026, Gen. Relativ. Gravit. 58, 1) presents an irrotational (curl-free shift) warp drive with a closed-form potential. At identical (rho, sigma, v/c) its peak proper-energy deficit is reduced by a factor of about 38 relative to Alcubierre and about 2.6x10^3 relative to Natário, and its peak NEC violation is more than 60 times smaller than Natário's. Scope: these are LOCAL peak measures, not total energy; the paper also reports the slice-integrated net proper energy is consistent with zero (|E+ - E-|/(E+ + E-) = 0.04%) and that the drive is Hawking-Ellis Type I. Single-author work whose citation count on INSPIRE was 4 at retrieval; not independently replicated.
  SOURCE: Rodal, J., "A warp drive with predominantly positive invariant energy density and global Hawking-Ellis Type I", Gen. Relativ. Gravit. 58, 1 (2026), arXiv:2512.18008
  QUOTE: "its peak proper-energy deficit is reduced by a factor of ≈ 38 relative to Alcubierre and ≈ 2.6×10^3 relative to Natário, and its peak NEC violation is more than 60× smaller than Natário."
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: medium

### G. Positive-energy solitons and shells

- [RS-17] CLAIM: Lentz (2021) constructs "hyper-fast" solitons from hyperbolic-relation shift-vector potentials sourced by a positive-energy plasma plus EM fields. Energy scaling is stated as E_tot ~ C v_s^2 R^2 / w (C a form factor of order unity; R = central-region radius; w = shell thickness, w << R). For R = 100 m and w = 1 m he quotes E_tot ~ (few)x10^-1 M_sun v_s, "of the same magnitude as the estimate of Ref. [3] (Pfenning-Ford) for an Alcubierre solution of the same dimensions". So the claim is positivity of energy density, NOT a lower total energy than a thick-wall Alcubierre. Lentz suggests earlier optimisations (Van Den Broeck; White 2013; Loup et al.) "may provide significant savings" for his solitons too, i.e. not yet applied. Assumptions: Eulerian energy density positive; superluminal shift; the QI wall limit is argued not to apply because the source is not a Casimir-type free field.
  SOURCE: Lentz, E.W., 2021, "Breaking the warp barrier: hyper-fast solitons in Einstein-Maxwell-plasma theory", Class. Quantum Grav. 38, 075015, arXiv:2006.07125
  QUOTE: "For solitons where the radial extent of the central region R is much larger than the thickness of the energy-density laden boundary shell w (w≪R), the energy is estimated to be Etot∼C vs^2 R^2/w ... The required energy for a positive-energy soliton with central regions radius R = 100 m and average source thickness along the z-axis w = 1 m approaches a mass equivalent of Etot∼(few)×10^-1 M⊙ vs, which is of the same magnitude as the estimate of Ref. [3] for an Alcubierre solution of the same dimensions"
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

- [RS-18] CLAIM: DISPUTED. Santiago, Schuster and Visser (2022, PRD) address the three positive-energy / low-violation claims (Lentz, Bobrick-Martire, Fell-Heisenberg) and argue they only show positive energy for one family of observers (comoving Eulerian); the WEC requires all timelike observers. Their conclusion: within that framework "all physically reasonable warp drives will certainly violate the WEC, and both the strong and dominant energy conditions", and under plausible subsidiary conditions the null energy condition too. A separate preprint by Celmaster and Rubin (2025) says a direct calculation of Lentz's stress-energy finds negative Eulerian energy density in some regions, that Lentz's derivation contains "several derivation errors", and that even a repaired geometry violates the WEC in the Eulerian frame. Celmaster-Rubin is unrefereed and I have not seen a published reply from Lentz.
  SOURCE: Santiago, J., Schuster, S., Visser, M., 2022, "Generic warp drives violate the null energy condition", Phys. Rev. D 105, 064038, arXiv:2105.03079; Celmaster, B. and Rubin, S., 2025, "Violations of the Weak Energy Condition for Lentz Warp Drives", arXiv:2511.18251
  QUOTE: "the WEC requires all timelike observers to see positive energy density." ... "within the framework adopted by those three papers all physically reasonable warp drives will certainly violate the WEC, and both the strong and dominant energy conditions." (Santiago et al. abstract); "We demonstrate that Lentz's claim is incorrect." (Celmaster-Rubin abstract)
  ACCESS: abstract
  STATUS: peer-reviewed (Santiago et al.); preprint (Celmaster-Rubin)
  CONFIDENCE: high

- [RS-19] CLAIM: Fell and Heisenberg (2021) decompose the Eulerian energy of shift-vector solitons and give an example configuration (parameters (Pi, r, V, sigma) = (1/4, 6, 10, 1) in the paper's units; the length unit was not identified in the text I read) with positive Eulerian energy density everywhere, central shift magnitude 1.26 (superluminal), maximum density rho_max ~ 3.2x10^26 kg/m^3 and total energy E_total ~ 9.25x10^43 J, compared with the Sun's rest-mass energy 1.78x10^47 J, i.e. "four orders of magnitude" smaller. [my arithmetic: 9.25x10^43 J / c^2 = 1.03x10^27 kg, about 0.54 Jupiter masses.] The paper itself says any attempt to build this configuration would "more than likely" form a black hole, that the exterior is Schwarzschild-like rather than Minkowski (nonzero ADM mass), and that horizons and the sub- to super-luminal transition are unanalysed. Baseline: classical Alcubierre (the text cites an energy "several orders of magnitude more than all the energy content in the observable universe"). The bubble size and wall thickness of the example are not given in metres, so this is not a like-for-like comparison with the R = 100 m cases. Disputed in the sense of RS-18 (positive for Eulerian observers only).
  SOURCE: Fell, S.D.B. and Heisenberg, L., 2021, "Positive energy warp drive from hidden geometric structures", Class. Quantum Grav. 38, 155020, arXiv:2104.06488
  QUOTE: "The total energy present on any initial hypersurface can be found to be approximately Etotal≈ 9.25∗10^43 J, which is still enormous, but quite small in astronomical terms." ... "More than likely, any attempt to construct this specific configuration will form a black hole."
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high for numbers as quoted; low for comparability

- [RS-20] CLAIM: Fuchs et al. (2024, Class. Quantum Grav. 41, 095013) give a constant-velocity SUBLUMINAL warp shell that satisfies all the energy conditions: a stable regular matter shell plus a shift-vector distribution matched to Alcubierre. Example: shell inner/outer radii R1 = 10 m, R2 = 20 m, mass M = 4.49x10^27 kg (2.365 Jupiter masses), drive velocity v_warp = 0.04c. The energy cost is the shell's positive ADM mass, so it is not a lower-energy Alcubierre variant; it trades negative energy for a Jupiter-scale positive mass, with no acceleration phase solved and no superluminal capability. This is a positive-mass alternative, not a reduction of an Alcubierre energy.
  SOURCE: Fuchs, J., Helmerich, C., Bobrick, A., Sellers, L., et al., 2024, "Constant velocity physical warp drive solution", Class. Quantum Grav. 41, 095013, arXiv:2405.02709
  QUOTE: "we present a solution for a constant-velocity subluminal warp drive that satisfies all of the energy conditions. The solution involves combining a stable matter shell with a shift vector distribution that closely matches well-known warp drive solutions such as the Alcubierre metric." (abstract); "For a shell with parameters: R1 = 10 m, R2 = 20 m, M = 4.49× 10^27 kg (2.365 Jupiter masses)" (Sec. 3)
  ACCESS: full-text
  STATUS: peer-reviewed
  CONFIDENCE: high

### H. Other claimed routes to lower energy

- [RS-21] CLAIM: Obousy and Cleaver (2008, JBIS 61, 364) propose changing the radius of a compact extra dimension to tune the Casimir-driven cosmological constant locally and produce the expansion/contraction of an Alcubierre-type bubble, with "calculations of the energy requirements" and a Planck-limited "ultimate" speed. I have only the abstract; the energy numbers were not read. The proposal rests on a speculative higher-dimensional Casimir mechanism. Fringe-adjacent, used as inspiration for White's Eagleworks work (White cites Chung-Freese branes).
  SOURCE: Obousy, R.K. and Cleaver, G., 2008, "Warp Drive: A New Approach", J. Br. Interplanet. Soc. 61, 364, arXiv:0712.1649
  QUOTE: "Calculations of the energy requirements of such a drive are performed and an 'ultimate' speed limit, based on the Planckian limits on the size of the extra dimensions is found."
  ACCESS: abstract
  STATUS: peer-reviewed (JBIS); speculative physics
  CONFIDENCE: low

- [RS-22] CLAIM: Rodal (2025 preprint) rebuts recent "low-energy" warp concepts in which the gravitational coupling kappa in G = kappa T is replaced by an engineered spatially varying scalar field. He argues a prescribed non-dynamical kappa(x) is inconsistent with the contracted Bianchi identity (forcing nabla_mu T^{mu nu} != 0) and a dynamical kappa gives a scalar-tensor theory excluded by |gamma - 1| <~ 10^-5 constraints. This is a critique of a different energy-reduction route from the shape ones above; the concept it targets is not named in the abstract.
  SOURCE: Rodal, J., 2025, "On the Infeasibility of Low-Energy Warp Drive via Metamaterial Gravitational Coupling", arXiv:2507.09724 (no journal ref per INSPIRE)
  QUOTE: "We show that the idea fails on both theoretical and experimental grounds."
  ACCESS: abstract
  STATUS: preprint
  CONFIDENCE: medium

- [RS-23] CLAIM: DeBenedictis and Ilijic (2018) show that in Einstein-Cartan gravity torsion terms from spin allow warp-drive spacetimes that respect the energy conditions, with derived limits (the abstract is truncated in the search output). This changes the gravity theory, so it is speculative extension, not GR + QFT.
  SOURCE: DeBenedictis, A. and Ilijic, S., 2018, "Energy condition respecting warp drives: the role of spin in Einstein-Cartan theory", Class. Quantum Grav. 35, 215001, arXiv:1807.09745
  QUOTE: "It turns out that with the addition of spin, the torsion terms in Einstein–Cartan gravity do allow for energy condition respecting warp drives."
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: medium

- [RS-24] CLAIM: Numerical survey context. The Warp Factory paper (Helmerich et al. 2024) states that so far proposed solutions have been "unphysical, requiring energy condition violations and large energy requirements" and provides tooling to evaluate energy conditions for arbitrary metrics. Useful as the modern check on all the shapes above.
  SOURCE: Helmerich, C., Fuchs, J., Bobrick, A., Sellers, L., et al., 2024, "Analyzing warp drive spacetimes with Warp Factory", Class. Quantum Grav. 41, 095009, arXiv:2404.03095
  QUOTE: "So far the proposed solutions have been unphysical, requiring energy condition violations and large energy requirements."
  ACCESS: abstract
  STATUS: peer-reviewed
  CONFIDENCE: high

### I. Cross-cutting notes

- [RS-25] CLAIM: The quoted reductions are not like-for-like, which weakens any ranking of shapes by "energy". Baselines and parameters (from the claims above): Pfenning-Ford Alcubierre R = 100 m, Delta ~ 100 v L_P: about -6x10^62 kg (v = 1); Van Den Broeck: outer R = 3x10^-15 m, pocket 200 m, wall at the QI limit: about -10^30 kg, negative plus positive parts different, and disputed by Bobrick-Martire; White: v = 10c, 10 m diameter, thickening from thin to "no flat space left", energy in geometric units, no SI totals printed; Lentz and Pfenning-Ford thick wall: R = 100 m, Delta or w = 1 m, few x 10^-1 M_sun v (about 10^29-10^30 kg); Fell-Heisenberg: about 10^27 kg, units of length unspecified; Fuchs: subluminal (0.04c), R = 10-20 m, 4.5x10^27 kg positive mass. The thin-versus-thick wall choice (Delta = 100 Planck lengths vs 1 m) alone changes the Alcubierre R = 100 m baseline by about 32 orders of magnitude, so a "reduction" claim that changes only Delta (White; thick-wall Lentz) is not a shape-independent saving. All of the totals use Eulerian energy on t = const, which Santiago et al. argue is not observer-independent. [my arithmetic and synthesis from RS-07, RS-09, RS-17, RS-19, RS-20]
  SOURCE: synthesis of the cited papers
  SUMMARY: (derived; see the individual claims)
  ACCESS: full-text
  STATUS: secondary
  CONFIDENCE: medium

- [RS-26] CLAIM: Which paper the user probably remembers. The best match for "a white paper on shapes that need less energy" is White's NASA JSC deck "Warp Field Mechanics 102: Energy Optimization" (NTRS 20130011213, 2013), whose slides say "Bubble Topology Optimization" and "Changing topology greatly reduces the energy required" (RS-04), with the toroidal/donut bubble and the oscillating-intensity idea; the companion paper "Warp Field Mechanics 101" (NTRS 20110015936, 2011; JBIS 2013) holds the written thick-wall argument (RS-01). Van Den Broeck 1999 (RS-09) is the leading peer-reviewed alternative, since it is the classic "different shape, far less energy" result (few solar masses versus 10^62 kg).
  SOURCE: synthesis of RS-01, RS-04, RS-09
  SUMMARY: (inference, not a documented fact about the user's memory)
  ACCESS: full-text
  STATUS: secondary
  CONFIDENCE: medium

## Gaps
- The exact numbers on the "Exotic Mass Warp Requirements" plot in White's 102 slides. The slide is a scanned image with garbled OCR text, so values can only be read by eye from a rendered image (RS-05). The deck states no SI totals in words.
- The JBIS 66:242 text itself (paywalled or blocked); only its title and citation were confirmed by search summary.
- A primary transcript or slides for White's 2012 100YSS talk and for any Eagleworks note giving an explicit energy formula for the "donut" (toroidal) shape or the oscillating bubble.
- No published critique aimed at White's oscillation/bulk-velocity trick, nor any published reply to Bobrick-Martire's Van Den Broeck equivalence claim, nor a published reply from Lentz to Celmaster-Rubin. Searched INSPIRE and arXiv by title, author and keyword; absence is not proof.
- Time-varying / oscillating-bubble energies from a peer-reviewed source: none found beyond White's slides.
- Alcubierre's 1994 paper and the Alcubierre-Lobo review chapter (arXiv:1701.05750-type) were not opened; the Krasnikov tube (Everett-Roman 1997), which trades bubble for a tube, was found but its energy claims were not read. Ford-Roman quantum-inequality derivations and the "-0.068 solar mass" Pfenning figure cited by Loup et al. were not traced to source.
- Obousy-Cleaver's actual energy numbers (abstract only).
