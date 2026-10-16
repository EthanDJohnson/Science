# Check: critiques
status: final

| Claim | Verdict | Note |
|---|---|---|
| RC-01 Swift known layout, 75 m lap, 1 week practice, 40 ms TX2 pass | verified | All quotes match the Europe PMC full text (via find_fulltext). The text also reports 40 ms human-vs-Swift sensorimotor latency, which is a different 40 ms. |
| RC-02 VIO drift, GP drift model about 50 s of flight | verified | "substantial drift" and "approximately 50 s of flight time" match. The claim calls the model a Gaussian-process odometry-drift model; the 50 s is described as residual identification, so the exact model type was not re-checked. |
| RC-03 Swift not faster on all segments; same weight, shape and propulsion; 120 ms earlier start | verified | Wording matches. The claim's "optimizes trajectories on a longer timescale" hypothesis quote was not grepped. |
| RC-04 Song et al. table and mechanism | verified | Table row values match exactly. The "both OC methods fail" quote was not grepped. Resolves the claim's open point: the paper says real-world state came from a Vicon motion-capture system plus EKF, so the real-world rows are not onboard-only. Trial counts are still not found. |
| RC-05 RL wins by optimising a better objective; 9 % arithmetic | verified | Quotes match. 5.35/4.92 = 1.087, so about 9 % slower, consistent. The 4.92 s figure is the nominal-sim trajectory-tracking time. |
| RC-06 NeuroBEM quotes, 65 km/h, 0.8 m to 0.3 m, 50 % | verified | Abstract and conclusion match. The abstract says "over 50%" positional-RMSE reduction and "50% reduced prediction errors". Published at RSS 2021 per the paper header. |
| RC-07 Hanover survey quotes | verified | Both quotes match the arXiv text. The journal reference (T-RO 40) was not checked. |
| RC-08 Loquercio speed-axis results | misattributed | Hardware results match: 8 of 10 at 7 m/s, 60 % at 10 m/s, and the perception and aerodynamics attributions. The "average success rate of 70% at 10 m/s" is from the simulation benchmark (Flightmare, 10 forest seeds per method), not the real-world runs. So "two figures in one paper" is a hardware-versus-simulation difference. The sim forest figure is 60 %. The "failures at 7 m/s" quote is in the text. The 19 experiments at 3-7 m/s in human-made environments match. |
| RC-09 Falanga bound as described by Loquercio | verified | The "limiting factor" quote matches the opening text. The point-mass quote was not separately grepped. The claim's own flag that Falanga was not opened is honest. |
| RC-10 SkyDreamer / TU Delft critique | verified | Both quotes match. The first quote lacks the leading "their performance". The claim itself is correctly marked preprint. |
| RC-11 Dream to Fly HIL only; 240 h | verified | Quote matches the arXiv text. ICRA 2026 DOI/status was not checked. |
| RC-12 AlphaPilot 130 ms, 35/60 Hz, +/-7.5 m/s and 12 m/s^2 | verified | Matches. The claim correctly flags Fig. 5 values as illustrative. The velocity-cap quote was not grepped. |
| RC-13 Foehn time-optimal, motion capture, collective-thrust critique | verified | Fig. 1 caption and "rather than the actual constraint of limited single rotor thrusts" match. |
| RC-14 UZH-FPV dataset | unverifiable | The project page confirms the SplitS track added 1 Dec 2023 with peak speeds up to 100 km/h. The "goal" sentence, the 27 sequences and the 10 km figures were not checked against the paper. The row is rightly marked search-summary. |
| RC-15 Green et al. 2026 | verified | Abstract and Vicon/workstation text match. |
| RC-16 Zhao et al. 2026 | verified | Abstract quote matches. |
| RC-17 A2RL 2025 | unverifiable | The Wikipedia table confirms MAVLAB first in the AI vs Human Challenge and 14 teams qualified. The "17 s for two laps of 170 m" figure was not checked; it comes from a search summary. |

Most serious: RC-08 mixes a simulation 70 % figure with hardware results. Also, RC-04's open question is resolved: the Song et al. real-world flights used Vicon, not onboard sensing.
