# Prior-art check: fuchs-shell, angle "missed"

- Finding: fuchs-shell (Fuchs et al. 2024, CQG 41 095013, arXiv:2405.02709): limits of the positive-energy shell, results (a)-(e)
- Angle: missed (adversarial; strategies the citations/direct/topical runs did not use)
- Date: 2026-10-27

## Plan
Strategies not yet used: Google Scholar-style phrasing via WebSearch, critics/collaborators (Bobrick, Martire, Lentz, Visser, Santiago, Schuster, Rodal, Alcubierre, Natario, Lobo, Van Den Broeck, Gonzalez-Diaz, Garattini, Zatrimaylov), theses, proceedings, blogs/Q&A (physics.stackexchange, Reddit), Visser's Shapiro delay/advance papers (Visser-Bassett-Liberati), Wald/Gao time-delay theorems, Weinberg-style Sagnac in stationary spacetimes, Kerr Sagnac/gravitomagnetic clock effect (Tartaglia, Cohen-Mashhoon), Bobrick-Martire follow-ups, Lentz positive-energy soliton, Short 2021 (Lentz error), Mattingly et al. 2021 (Alcubierre vs Lentz), Helmerich thesis, Fell-Heisenberg, Rodal, TMF2024 proceedings, Garattini-Zatrimaylov, Meyler-Fuchs hybrid, Zatrimaylov, Gonzalez-Diaz.

## Log
(appended below)

### Step 1 (searches)
- lit_search inspire "warp drive Shapiro delay advance positive energy shell" --since 2021: 0 hits (INSPIRE ANDs long queries)
- WebSearch (extended) "Fuchs Constant velocity physical warp drive ... critique larger velocity": only paper/mirrors/summaries; no critique of shift limits found. Mentions Barzegar review (ADM energy) only.
- lit_search "refersto:arxiv:2102.06824" (Bobrick-Martire citers, 2024+; 25 records, NOT searched by earlier runs). New titles beyond what earlier runs read: Abellan et al CQG 41 105011 (2024, lapse bubble, inspire 2781928); Santos-Pereira thesis 2508.20348; Chowdhury 2404.15948; Davis 2024 "GR FTL propulsion"; Jusufi 2609.05554; Helmerich AIAA conf 2404.10855; Minotti 2603.26986 (unrelated); Sato 2608.27900 (unrelated).
- WebSearch "Meyler Fuchs hybrid warp drive philarchive": single-author unrefereed preprint (philarchive.org/rec/MEYTMH), toroidal plasma shell, claims energy reduction; not opened yet.
- WebSearch stackexchange/reddit: none found (press only: space.com, ACU 2021 etc.)

### Step 2
- INSPIRE sweep "t warp and date > 2024" (28 records), "t Alcubierre and date>2024" (6), "t Natario...", etc. New (not read by earlier runs): Rodal 2507.09724 (metamaterial coupling; no Fuchs cite), Santos-Pereira 2512.12541 (no Fuchs), Jusufi 2609.05554 (no Fuchs), Santos-Pereira thesis 2508.20348 (no Fuchs), Bolivar piecewise anisotropic bubbles (Annals Phys 481 170147; trivial lapse), Lee "Warp anisotropy" (string compactification, unrelated). Bolivar 2609.36211 cites Fuchs only as ref [8] (reference list; all earlier runs read it).
- INSPIRE author queries Fuchs/Sellers/Melcher/Bobrick(A.) post-2022: no further warp papers by the Fuchs-team beyond 2404.03095, 2404.10855, 2405.02709.
- WebFetch philarchive.org/rec/MEYTMH: HTTP 403 (not read).
- WebSearch Warp Factory GitHub docs: nothing on WarpShell parameters. 'warpax' tool is in Le 2602.18023 (already covered).

### Step 3 (verified items)
- Bobrick & Martire 2021 (arXiv:2102.06824) p.1 (fetch_text --grep coordinate): "In a coordinate system with x -> x' = x - v_s t, this internal region is described explicitly by the Minkowski flat metric." (Alcubierre interior shift = pure coordinate change; EARLIER explicit statement of the gauge half of (d), for the Alcubierre drive.) p.2: negative energy general for superluminal drives (Olum 1998, Visser et al 2000). p.8: momentum flux and E, J_i defined in comoving frame; E,J only from warped region.
- Visser, Bassett, Liberati, Superluminal censorship, gr-qc/9810026 (Nucl.Phys.Proc.Suppl. 88, 267; 1998): abstract verified: "Given the NEC, the Shapiro time delay in any weak gravitational field is always a delay relative to the Minkowski background, and never an advance." (background for (c); Fuchs cites it as ref [21]).
- Gao & Wald gr-qc/0007021 CQG 17 4999 (2000): NEC + null generic condition => time delay theorems (background for (c)).
- Alcubierre gr-qc/0009013 abstract verified (exotic matter needed).
- Sagnac in GR: Tartaglia gr-qc/9806019 (PRD 58 064009, 1998) co/counter-rotating light travel-time difference in a Kerr field; Maraner & Zendri 1110.1643 (GRG 44, 1713) Sagnac time shift, clock synchronization, AB analogy. Background for (d). No warp content.

### Step 4 (Le versions not read before)
- Le 2602.18023 v5 (fetch_text p.22-24, 46pp): sec 3.6 says "The Fuchs shell's energy-condition compliance is designed at vs = 0.02"; Fuchs shell R1=10,R2=20, 2M=6.6687 (compactness 2M/R2 = 0.3334), "the Fuchs material stress is velocity-independent where the flat-slice drives' stress scales as vs^2"; "Result. The Fuchs constant-velocity shell is Type I with a non-negative NEC margin throughout its sampled shell wall and interior"; R2^2 min(rho+p_i)=+0.021 (matched), +0.022 (own params); notes companion [53]=2605.25417 reports Type-IV in density smoothing tail. Lemma 1 (flat-slice unit-lapse only): 8 pi |j| = 1/2 |curl curl beta|; Lemma 2: momentum channel closed on gradient shifts; "every other wall-localized vortical shift sources a wall momentum ... that turns the wall Type IV where it dominates". General mechanism for shift -> momentum flux -> Type IV; NOT applied to Fuchs shell beyond 0.02; no beta scan. => background/partly.
- Le 2605.25417 v2 abstract (fetch_text): T-shell (own construction) Type-IV onset imaginary eigenvalue "grows linearly with the matter tilt, instantiating the shift-vorticity mechanism of the companion certifier"; peak shift 0.0071 (v0=0.1). Not Fuchs shell.
- Le 2606.22531 v2/v3: Fuchs cited as constant-velocity positive-energy shell; v3 p.28 repeats Barzegar TOV dispute ("We take no position on that dispute"). Nothing on shift limits/Sagnac. (Earlier runs read v1, v4.)
- WebSearch (extended) on shift-limit/compactness follow-ups: only returned Le 2602.18023 and 2606.22531, Santos-Pereira thesis; no threshold paper. WebSearch on interview/Jupiter mass: UAH press only (fetch_text SSL fail; press quote not verified, not used).

### Step 5 (Sagnac/holonomy/NEC-background, verified abstracts via fetch_text/lit_search)
- Ashtekar & Magnon, "The Sagnac effect in general relativity", J.Math.Phys. 16, 341 (1975), inspire 98249. Abstract (lit_search): "The Sagnac effect is a phase shift observed between two beams of light traversing in opposite directions the same closed path around a rotating object... In this context the effect provides an operational definition of rotation." Background for (d).
- Anandan, "The Sagnac effect in relativistic and nonrelativistic physics", PRD 24, 338 (1981), inspire 164834: abstract verified "distinction between classical Sagnac effect and quantum Sagnac effect... group-theoretic derivation".
- Schuster, Santiago, Visser, "ADM mass in warp drive spacetimes", arXiv:2205.15950 (GRG 55, 14): sec 4 "black-warp" (Schwarzschild + moving irrotational Natario shift): fetch_text p.15 "Since rho = 0 by construction, there is consequently an entire hemisphere where rho + p < 0 and the NEC is explicitly violated." => linear-in-v NEC violation when a massive vacuum background carries a shift; background mechanism for (b) (momentum flux vs. energy density), not the Fuchs shell.
- Ralph & Chang, "Spinning up a Time Machine", PRD 102, 124013 (arXiv:2007.14627): Alcubierre drive on a rotating platform; fetch_text p.2: "The anisotropy of light speed in the tangential directions, in a rotating frame leads to the well-known Sagnac effect in optics." Metric has g_{t phi} shift cross term; analogy only; not a shell, no holonomy/gauge analysis => background/unrelated.
- Lentz 2201.00652 (MG16 proceedings summary) and Huey 2311.07193 (membrane models, WEC): surfaced by web search; abstracts only; no Fuchs shell shift-limit content.
- WebSearch "warp drive Sagnac shift holonomy": nothing treating Sagnac/holonomy of warp shells; WebSearch material strength/hoop stress: nothing.
- Andreasson gr-qc/0605097 (CMP 274, 399): Buchdahl inequality for shells with anisotropic pressure (abstract seen: Buchdahl 2M/R<=8/9 rests on isotropy+monotone density; "In this work neither of..."), background for (b)/(e) compactness bound.

### Step 6 (more checks)
- Garattini & Zatrimaylov, "Black Holes, Warp Drives, and Energy Conditions", arXiv:2408.04495 (PLB 856, 138910): abstract verified "the black hole's gravitational field can alleviate the violations of the weak energy condition (WEC) and the null energy condition (NEC)". No Fuchs cite (fetch_text NO MATCH). Background for (b): massive background gives positive-energy room.
- Abellan, Bolivar, Vasilev, arXiv:2305.03736 (2023): isotropic/anisotropic fluids on spherical warp metric; "In general there are regions of spacetime where the energy conditions can be at least partially satisfied." Predates Fuchs; not about shell shift cap. Background/unrelated.
- Garcia-Moreno thesis 2510.18419 (327pp): NO MATCH for 'Fuchs'. Santos-Pereira thesis 2508.20348: NO MATCH for 'Fuchs'. Chowdhury 2404.15948: only cites Helmerich AIAA paper in ref list.
- Citers (2024+) of Lentz 2006.07125, Fell-Heisenberg 2104.06488, SSV-ADM 2205.15950 listed via INSPIRE: all titles already in earlier runs or non-bearing (Davis 2024 FTL propulsion, Simmonds perfect-fluid spheres, Sato Vlasov core-shell: not read, titles unrelated).
- INSPIRE "t comment/reply and t warp drive": 0; Crossref "Comment on Constant velocity physical warp drive solution": none. INSPIRE authors Fuchs/Sellers/Melcher/Helmerich/Bobrick(A.): no warp papers beyond 2404.03095, 2404.10855, 2405.02709.
- WebFetch applied-physics.gitbook.io/warp-factory: overview only, no WarpShell parameters.
- WebSearch exact numbers (0.0239, 6.86 ns, 0.539, graphene): nothing. WebSearch HN/physicsforums/reddit: only press (thedebrief, sciencealert, interestingengineering). philarchive Meyler-Fuchs: HTTP 403 via fetch_text and WebFetch, only search-summary.
- arXiv API 429 on retry.
## VERDICT: partly-anticipated (qualitative pieces only). No makes-same-point found. New partial anticipation vs earlier runs: Bobrick-Martire 2021 explicit coordinate-transformation statement for the Alcubierre/bubble interior (gauge half of (d)); Visser-Bassett-Liberati/Gao-Wald as earlier theorem for (c) 'advance needs NEC violation'; Sagnac-as-closed-loop invariant (Ashtekar-Magnon 1975, Anandan 1981) as background for (d).
