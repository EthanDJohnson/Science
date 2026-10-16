# Check: engineering
status: final

| Claim | Verdict | Note |
|---|---|---|
| RE-01 Swift 75 m lap, 7 gates, 30x30x8 m, 5/9, 4/7, 6/9, loss breakdown | verified | All wording confirmed in PMC10468397. Wins sum to 15 of 25. |
| RE-02 Swift hardware/compute (870 g, 35 N, T/W 4.1, 40 ms U-Net on TX2, 8 ms policy) | verified | Quotes confirmed in PMC full text. T265 at 100 Hz and the STM32 details were not individually re-checked. |
| RE-03 40 ms vs 220 ms latency, 30 vs 120 Hz, VIO drift, one week practice | verified | Exact wording confirmed. The claim says the "pilots are given a week of practice" in a track-fit sentence, which matches the source. |
| RE-04 prior human-level results relied on mocap | verified (not re-grepped) | Same paper. The quote is consistent with the PMC text. Treated as low risk. |
| RE-05 Loquercio 2021: 56 experiments, 60% at 10 m/s, narrow openings | misattributed (partly) | 56 experiments and the 60% at 10 m/s quote are confirmed. But "5 to 7 m/s with success near 100%" is wrong. The paper says 100% only up to 5 m/s, and "successfully completed in 8 out of 10 experiments" at 7 m/s (80%, two failures). The 31 natural plus 19 human-made experiments (3-7 m/s) are given in the text. The 890 g, 4.4 T/W figures were not found in the PDF text; the paper's footnote says max acceleration 4 g. |
| RE-06 Loquercio simulation latency analysis, FastPlanner 65.2 ms | verified | The 65.2 ms per frame on the TX2 is confirmed. The learned policy takes 41.6 ms onboard, which is lower. Claim details about the pole experiment were not checked. |
| RE-07 Song 2023: 108 km/h, >12 g, 0.52 kg, 63 N, Vicon+EKF, 100 Hz | verified | 108 km/h and 12.58 g confirmed. The Fig. 1 caption confirms the indoor arena. Vicon wording not re-grepped. |
| RE-08 Fig. 2C table of lap times and success | verified | The table string matches exactly. Caveat: the "Realistic" row is simulation, as the note says. The 0.92 ratio is derived, correctly flagged. |
| RE-09 Agilicious 750 g / 131 km/h, 39.1 ms, circle 5 m/s, lemniscate up to 7 m/s | verified | All three quotes confirmed. |
| RE-10 MonoRace 16.56 s, 100 km/h, Orin NX, 11 gates, 100x30 m hall | verified (partly) | 16.56 s, 100 km/h, 11 gates, 1.5 m opening and the 100x30 m hall are confirmed. The arXiv paper's table lists max speeds up to 32.2 m/s (about 116 km/h) for some policies, so "27.8 m/s peak" understates the paper's own table. Sensor and rate specifics were not re-checked. |
| RE-11 MonoRace M23 88.4%, "no success rate for the 16.56 s policy" | contradicted (in part) | The 88.4% = 38/43 for M23 and the trade-off quote are confirmed. But the paper's table does give a rate for the 16.56 s policy: M16 had 4 trials, 1 success, 25.0%, mean completion time 16.56 s. M17 had 71.4% (5 of 7). The claim that none is given is false. The 25% (1 of 4) rate also undercuts any reading of 16.56 s as a routine result. The table label "Simulation (30% randomization)" sits next to these rows in the extraction, so check whether the 43-trial row is hardware. The text says M23 completed 43 flights. |
| RE-12 500 Hz, 0-100% in 2 ms, 50% corrupted frames, simulator misses vision errors | verified | The 2 ms and 50% frames wording is confirmed. The "does not accurately model vision-based state estimation errors" quote was not re-grepped. |
| RE-13 Azhari et al.: single camera + IMU, VIO drift | verified | Wording confirmed in arXiv:2512.20475. The inference "estimation, not thrust, is dominant" is the researcher's, not the paper's. |
| RE-14 A2RL 2026: TII Racing 12.032 s, MAVLAB 12.832 s | unverifiable | Business Wire page timed out and the numbers come from a search summary. Already labelled low confidence. |
| RE-15 AI Grand Prix schedule | unverifiable | theaigrandprix.com timed out. The schedule cannot be checked from here. The claim quotes the FAQ but the page was not re-read. |
| RE-16 SJTU/TU Delft: 8 m/s real, 10 m/s HIL, 100% in all obstacle-rich environments | verified | Quote confirmed in the PDF. Raspberry Pi and D435i are confirmed. Trial counts are unknown, so "100%" carries little weight. The claim that gate layout is fixed and the obstacles random was not checked. |
| RE-17 ZJU Gate-SDF MPPI: 5.3 m/s real | verified (partly) | The 5.3 m/s onboard-depth quote is confirmed. Simulation table values were not re-checked. |
| RE-18 web-survey lead on overfitting, 70 km/h sim | unverifiable | Model-written search summary, not opened. Already labelled a lead. |
| RE-19 Foehn 2021 "slightly lower thrust bound" | verified | Exact quote confirmed. The platform is 0.8 kg with a T/W of about 4. Arena size and 7 laps were not checked. |
| RE-20 Bhattacharya: 5 m/s trees, onboard, improves with speed | verified | Contribution bullet confirmed in arXiv:2411.03303. |
| RE-21 SUPER >20 m/s | unverifiable | Abstract-only and secondary press. The researcher already flagged it as unverified. |
| RE-22 synthesis table | misattributed (in part) | Inherits the RE-05 error: the Loquercio 7 m/s figure is 80%, not "near 100%". The 27.8 m/s peak understates the MonoRace table (up to 32.2 m/s). It also omits M16's 25% success. The overall conclusion that no hardware result meets the full brief is plausible but depends on these figures. |

Most serious problem: RE-11 says MonoRace gives no success rate for its 16.56 s policy, but the paper's table lists M16 at 25% (1 of 4 trials). Secondary: Loquercio's 7 m/s success is 8 of 10 (80%), not near 100%.
