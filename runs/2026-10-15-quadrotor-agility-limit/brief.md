# Brief: What limits the agility of an autonomous quadrotor
slug: 2026-10-15-quadrotor-agility-limit | depth: standard | type: mechanism | date: 2026-10-15

## Question as asked

For a quadrotor flying autonomously on onboard sensing and computation alone, which limit binds
first on closed-loop agility — rotor and actuator bandwidth, state-estimation latency, unmodelled
aerodynamics, or how far ahead it can perceive — and what would it take to move that limit?

## Question made precise

**The vehicle.** A multirotor of take-off mass between about 0.2 and 1.5 kg, the class the agile-flight
literature actually flies and publishes parameters for (3–5 inch racing airframes and research
platforms such as Agilicious; the Crazyflie class at tens of grams is a different regime and is
evidence only by analogy). Four rotors in a planar configuration, fixed-pitch propellers,
unidirectional thrust unless a source says otherwise.

**Onboard only.** All sensing and all computation on the vehicle: IMU, one or more cameras (frame or
event), optional rangefinder, and the vehicle's own processor. No motion-capture, no external
position reference, no GNSS, no off-board compute and no off-board radio link in the control loop.
Learned policies trained off-board are admissible; the trained policy must run onboard. A result
obtained with motion capture or off-board compute is evidence about the controller, not about this
question, and must be labelled as such.

**Closed-loop agility** is the maximum average speed, in m/s, at which the vehicle completes a gate
sequence or obstacle course **it has not seen before** with at least a 90 per cent success rate over
a stated number of trials, together with the fraction of the platform's own time-optimal traversal
time that it achieves. Two numbers, because a vehicle can be fast and far from its own limit.
Where a source reports only peak speed, peak acceleration, or performance on a course the system
was tuned on, that is a different quantity and must be recorded as such.

**"Binds first"** means: the limit whose relaxation, holding every other limit fixed, produces the
largest improvement in the agility metric. It is a sensitivity, and it is therefore computable —
perturb one limit in a model and measure the change — and also falsifiable: a candidate is refuted
if relaxing it changes the metric little, or if relaxing a rival changes it more. State the
sensitivity as a dimensionless elasticity (per cent change in speed per per cent change in the
limit) wherever a number can be had.

**Admissible physics and engineering.** Established rigid-body dynamics, rotor aerodynamics
(momentum and blade-element theory), linear and nonlinear control theory, estimation theory, and
hardware specifications from datasheets or measurements. Speculative hardware (actuators or sensors
not demonstrated at this scale) is admissible only when labelled.

**Horizon.** Two readings, kept apart: (a) what binds on hardware that exists and has been flown,
as of 2026; (b) what would bind if the current binding limit were removed with components available
within about five years. Answer (a) first.

## Hidden premises to test

1. **That one limit dominates.** Several limits may be within a factor of two of each other, in
   which case the honest answer is that none dominates and the question's framing is the problem.
2. **That the limits are separable.** Perception range, estimation latency and aerodynamic error all
   scale with speed, so a sensitivity computed at one speed may not hold at another, and the "first"
   limit may change along the speed axis. Say where each candidate's regime begins and ends.
3. **That the limit is in the vehicle at all.** It may be in the task: an agility metric defined on
   an *unseen* course makes the required look-ahead distance, not the vehicle, the binding term.
4. **That thrust-to-weight is not simply the answer.** It is the textbook limit on acceleration and
   must be computed first and then either established as the binding term or set aside with a number.
5. **That published speeds measure what the question asks.** Much of the literature reports peak
   speed on a known course with motion capture. That is not this metric.
6. **That the autonomy gap is a limit of the same kind.** Human pilots fly these airframes faster
   than any autonomous system; whether the gap is hardware, estimation, perception or policy is
   itself one of the candidate answers, not a background fact.

## What counts as an answer

A ranked slate of candidate binding limits, mutually exclusive on "which dominates", each with:

- the limit's measured value on current hardware, with units and a source (for example a motor time
  constant in ms, an end-to-end estimation latency in ms, a usable perception range in m);
- the sensitivity of the agility metric to it, computed and not asserted;
- the regime in which it binds, since the answer may change with speed;
- the decisive experiment or calculation that would separate it from its nearest rival, with who
  could run it and what it would cost;
- and an explicit statement of whether the evidence for it is a verified model, a model-error
  result, or a hardware demonstration.

Plus a null candidate ("no single limit dominates in this class") and a reframe candidate (the
metric or the premise is wrong).

## Research facets

- **theory**: the control- and estimation-theoretic bounds that apply regardless of hardware — the
  achievable closed-loop bandwidth given a loop delay (and how a sample period and a computation
  delay enter it), fundamental limits from right-half-plane dynamics and from bounded actuator rate,
  differential flatness and time-optimal trajectory theory for quadrotors (what the platform's own
  optimum is), the perception-latency-to-speed relation (how far ahead you must see to stop or turn),
  and estimation-theoretic bounds on attitude and velocity from an IMU plus a camera. Owns what is
  *proved*; leaves measured values to `quantitative` and demonstrations to `engineering`.
- **quantitative**: the measured numbers, each with units, conditions and source — take-off mass,
  inertia, thrust-to-weight, motor and propeller time constants and thrust/torque coefficients,
  maximum rotor-speed slew rate, IMU sample rate and noise density, gyro bias stability, camera frame
  rate, exposure and motion blur, event-camera latency, end-to-end VIO latency and drift, onboard
  compute throughput and control-loop period, battery specific energy and power limits, and the
  aerodynamic coefficients (drag, blade flapping, rotor interaction) with the speeds they were
  measured at. Leaves bounds to `theory` and demonstrations to `engineering`.
- **critiques**: the case against each candidate limit — papers arguing that a *different* limit
  binds, negative results, failed sim-to-real transfers, failed or partial reproductions, published
  cases where a method that worked in simulation failed in flight, and critiques of the benchmarks
  and metrics themselves (including whether "unseen course" results are really unseen). Also the
  arguments that the human-pilot gap is not what it appears.
- **engineering**: what has actually been flown, platform by platform — the demonstrated speeds and
  success rates with their trial counts, which sensing and compute were onboard and which were not,
  whether the course was seen in advance, and who ran it (the Nature drone-racing result, Agilicious,
  high-speed flight in the wild, event-camera flight, learned and MPC policies on the same hardware);
  the released code and benchmark suites, since a performance claim in this field usually rests on an
  artefact rather than on the paper's text; and the platforms, sensors and compute arriving next, with
  target numbers and dates. Keep hardware results and simulation results in separate claims.

## Worked calculations

Each must be computed, printed with its inputs, and cited; the slate builder, the refuters and the
judge use the owner's number as the reference.

- **The platform's time-optimal traversal time**, and the fraction of it the best demonstrated
  autonomous flight achieves — the denominator the whole agility metric depends on. Owner: the
  simulator lens.
- **The delay margin of the attitude and the position loop**, against the measured end-to-end
  latency budget, and the closed-loop bandwidth that latency permits. Owner: the simulator lens.
- **The acceleration and jerk ceiling set by rotor and motor bandwidth**, from the motor time
  constant and the thrust-coefficient curve, against the thrust-to-weight ceiling. Owner: the
  constraints lens.
- **The look-ahead distance required at a given speed** to avoid an unseen obstacle, against the
  usable perception range, and the speed at which they cross. Owner: the mechanist lens.
- **The sensitivity (elasticity) of the agility metric to each candidate limit**, perturbing one
  limit at a time in a verified model. Owner: the simulator lens. This is the quantity the question
  turns on, so it must come with its verification table.

Lenses run at the same time and cannot read each other, so a lens that needs another's number
computes its own and says so.

## Known constraints, prior attempts, and user-supplied data

None supplied. The question was chosen for this run; no earlier work in this project touches it.

## Prior runs

- 2026-09-29-alcubierre-negative-energy (2026-09-29): ignore. Warp-drive negative energy; no overlap.
- 2026-09-29-problem-of-time-quantum-gravity (2026-09-29): ignore. Quantum gravity; no overlap.
- 2026-10-01-warp-drive-without-negative-energy (2026-10-01): ignore. No overlap.
- 2026-10-13-gravitational-wave-decay-photon-pairs (2026-10-13): ignore. No overlap.
- 2026-09-30-neutron-lifetime-beam-bottle (2026-09-30): ignore. No overlap.

Every earlier run in this project is in general relativity, quantum field theory or particle
physics. `prior_runs.py` matched them at 10–20 per cent on shared common words only. None carries
evidence that bears on this question, so all are ignored and no agent sees them.
