# S1 + S2 Final Technical Validation — the actual v4.2 body geometry

Base: Anaconda v4.2 only (`anaconda-wordpress-snippet-v4.2 (6).html`, 2,644 lines,
SHA-256 `f41db032…`, **unmodified** — read-only reference throughout).
Status: design-only validation. No base code changed, no Stage-1 work started,
no new design changes proposed, no amendment opened. This report closes the
pre-approval question you raised: does S1 + S2 hold up on the *actual* v4.2
body geometry, dynamically, with proofs and simulated evidence kept strictly
apart? Everything here remains subject to your explicit Stage-1 approval.

**Method in one line.** The executable probe (`scripts/validation_probe.py`)
ports the actual v4.2 body — girth profile, gait blending, rate-limited
turning, head advance, spine follow-chain (L1509–1517), gait wave + ring
rebuild (L1525–1571), self-intersection guard `_relaxBody` (L1674–1738) —
into a deterministic simulation, runs the design's absorption → projection →
cap-5 → Stage-8 repair chain on top of it frame after frame (5 scenarios ×
4 configurations × 420 frames), and measures the five validation points.
Two runs produce byte-identical output (SHA-256 `ee92ad98…`), embedded
verbatim in §10.

Classification discipline, unchanged from the solution report:
**PROVEN** = exact mathematical proof (no linearization, no configuration
assumptions); **VERIFIED** = executed numerically by the probe on the stated
domains; **EMPIRICAL** = observed on tests, coverage-dependent, never stated
as a universal guarantee; **NOT CLAIMED** = refused rather than asserted.

---

## 0. Executive verdict

| # | Validation point | Verdict | Basis |
|---|---|---|---|
| 1 | S1 preserves the natural body path; no kinks, stretching, sliding artifacts, or unnatural downstream displacement | **PASS** | PROVEN (exact direction identity + Th. V1′ + lateral-zero identity) + VERIFIED on all 5 dynamic scenarios (§3) |
| 2 | S2's reduced budget causes no instability and does not prevent smooth movement | **PASS** | VERIFIED: engagement 0 % in dynamics, enforced Σ\|e\| ≤ 0.0025 every frame, jerk ≤ 0.0002, drain unchanged; engaged case (worked example) holds all gates (§4) |
| 3 | Self-collision clearance remains non-negative after repair in the tested configurations | **PASS** | PROVEN floor (margin − Λ = 0) + VERIFIED: echo ≤ Λ everywhere; floor respected on 363/363 at-margin coil frames and 420/420 at-margin wall frames; static adversarial regressions ≥ 0 (§5) |
| 4 | Skin pattern, body deformation, overlapping sections stay visually continuous | **PASS** | VERIFIED: rule-isolated rendered difference **exactly 0** (bitwise); marker-motion ratio ≤ 1.02 vs native; figures produced (§6) |
| 5 | All existing v4.2 movement and interaction features remain unaffected | **PASS** | VERIFIED: gait/wave state bit-identical across all configurations, guard mechanism bit-identical at frame 0, repair anchors ring 0 exactly, follow-chain no-op on the repaired chain (§7) |

The two findings you should weigh before approving (neither is a defect of
S1/S2; both are pre-existing properties now measured on the real geometry):
the panic-coil transient, where the *solver* (not the repair) lags a demand
surge — the design chain still reduces the worst guard violation ~10× vs
native (§5) — and the +1.9e-6 stall residual under S2 on the worked example,
frozen by the budget-independent L1-stall (§4). Both are covered by the
measured-π gate R-FINAL, exactly as before.

---

## 1. What was validated, and the probe conventions

**Configurations compared** (all on the same ported v4.2 body):

| Config | Stage-8 rule | cap-5 budget Λ | Meaning |
|---|---|---|---|
| `native` | — (no design chain) | — | v4.2 behavior alone; invariance reference |
| `v1.10` | OLD (working-direction) | 0.0042 | the currently documented design |
| `S1` | fixed-direction | 0.0042 | rule change alone |
| `S1+S2` | fixed-direction | 0.0025 | the proposed package |

**Scenarios** (each 420 frames at dt = 1/60 s, deterministic, no RNG):

| ID | Scenario | Exercises |
|---|---|---|
| SC-A | cruise straight (gait cruise) | baseline smoothness, zero-demand floor |
| SC-B | crawl S-weave (gait crawl, weave 0.46) | natural S-path preservation |
| SC-C | run U-turn (gait fast, 180° over 90 frames) | large fold, direction identity through the turn |
| SC-D | panic coil (speed 2.3 → 1.05, sustained max-rate turn) | sustained self-overlap demand, guard + repair stress |
| SC-E | wall glide along the margin line (parallel wall at r + R_BODY + MARGIN) | sustained wall demand, at-margin floor every frame |

**Probe conventions (stated so nothing is hidden):**

- **D1 — native layer = exact v4.2 ports.** Gait blending (L1440–1451),
  rate-limited turning (L1463–1475), speed integrator (L1481–1483),
  locomotion (L1493–1506), follow-chain (L1509–1517), wave + ring rebuild
  (L1525–1571), guard (L1674–1738) are line-by-line ports; G0 asserts the
  port (RAD knots, follow-chain behavior). Behavior-layer AI (wander
  targets, multi-snake avoid, tongue/jaw/head-loft cosmetics) carries no
  body-geometry information and is replaced by the scenario scripts; alert
  lift is 0 because no scenario freezes. These are harness choices, not
  design changes.
- **D2 — design layer = established v1.8–v1.10 harness conventions.**
  R_BODY = 0.05 capsule model, MARGIN = 0.0025, caps 1–5, rope-kernel
  projection, paired transfer (X = P + `_ro` invariant), Stage-8 repair on
  the material chain P. Nothing about S1/S2 alters these.
- **D3 — demand source.** The per-frame repair-chain demand is the residual
  self-overlap that v4.2's *own* guard geometry still reports on the
  post-relax render chain (the guard formula of L1686–1701 evaluated once
  on R), plus wall demand in SC-E, blurred with v4.2's own 3-tap
  (L1718–1721), then passed through caps 1–3. The Stage-1 solver's own
  input derivation may differ; the repair-chain conclusions (exactness,
  echo bounds) are PROVEN for arbitrary admissible fields and therefore do
  not depend on this choice — only the scenario numbers are D3-conditional
  (VERIFIED under D3).

---

## 2. The actual v4.2 body geometry as ported (read-only citations)

| Quantity | Value | Source |
|---|---|---|
| Rings N | 80 | L104 |
| Segment SEG | 0.10 u (body ≈ 7.9 u) | L105 |
| Girth profile knots | (0.00, 0.238) … (0.32, 0.352) … (1.00, 0.018), monotone cubic Fritsch–Carlson | L107–148 |
| Sampled girth max | RAD[26] = 0.3520; radiusAt(0.32) = 0.352000 (knot-exact) | probe G0 |
| WAVE_SLIP | 1.6 | L1230 |
| Gaits (rest/crawl/cruise/fast/escape/turn) | waveK 0.34–0.46, waveA 0.026–0.058, … | L1222–1227, blended at 3.5/s (L1447–1451) |
| Guard domain | rings 4..61, pairs \|i−j\| ∈ [10, 60), axis early-out 0.85 | L1681–1690 |
| Guard threshold | minD = (RAD_i + RAD_j)·0.98 (tail-drape exemption rings ≥ N−18) | L1691, L1678–1680 |
| Guard caps / factor | 0.030 (neck) / 0.018, f = 0.45, 4 Gauss–Seidel passes | L1697–1698, L1677 |
| Guard smoothing | 3-tap 0.25/0.5/0.25 → low-pass 3.0 (neck) / 2.1 s⁻¹ → magnitude cap 0.22 | L1716–1735 |
| Follow-chain | hard renormalize each ring to SEG along the working direction | L1509–1517 |
| Design-layer capsule | R_BODY = 0.05, MARGIN = 0.0025, self-pairs \|i−j\| ≥ 9 | established harness (v1.8–v1.10) |

Two collision layers coexist by established convention: the **real-geometry
guard** (visual girth RAD, thresholds ≈ 0.6 u — this is what the player sees
and what `_relaxBody` resolves) and the **design-layer capsule model**
(R_BODY = 0.05 — this is what the T6 wires, MARGIN and the repair-echo
bounds are defined on). The probe measures both and never mixes them.

---

## 3. Point 1 — S1 preserves the natural body path

**What is PROVEN (algebra, no linearization — carried over from the solution
report, re-exercised by the probe every frame):**

1. *Exact direction identity.* S1 places each ring at
   `Q'_{k+1} = Q'_k + SEG·t_k` with `t_k` = **input** segment direction. The
   repaired polyline therefore has exactly the input's directions with every
   segment snapped to SEG: zero added turning, i.e. **no kink can be
   introduced by construction**, for any input, any magnitude.
2. *Lateral-zero identity.* The relative repair motion of consecutive rings
   is `δ_{k+1} − δ_k = −e_k·t_k` — purely along the body axis. Its component
   perpendicular to `t_k` is exactly zero: **no lateral sliding artifact**
   for any input.
3. *Theorem V1′.* Ring displacement ≤ Σ|e_k| ≤ Λ per frame: **no unnatural
   downstream displacement** beyond the budget.
4. *Exact rope.* Post-repair |len − SEG| = 0 to machine precision; the
   native follow-chain is a no-op on the repaired chain (measured ≤ 1.5e−14
   across all runs — the float64 lattice floor), so the repair never fights
   the native constraint.

**What is VERIFIED (dynamic, actual geometry — probe V1 table):**

| Scenario | rule | max heading change (rad) | max \|len−SEG\| | max ring disp (u) | max lateral rel | Σ\|disp\| cum (u) |
|---|---|---|---|---|---|---|
| SC-A/B/C | S1, S1+S2 | ≤ 5.3e−15 | ≤ 8.7e−16 | 0 | ≤ 5.2e−16 | 0 |
| SC-D coil | OLD | **5.9e−03** | 3.6e−16 | 0.00098 | **5.9e−04** | 0.046 |
| SC-D coil | S1, S1+S2 | **5.3e−15** | 8.6e−16 | 0.00115 ≤ Λ | **5.0e−16** | 0.059 |
| SC-E wall | OLD | 1.6e−04 | 9.0e−16 | 0.00021 | 1.6e−05 | 0.012 |
| SC-E wall | S1, S1+S2 | **1.3e−15** | 1.9e−15 | 0.00021 ≤ Λ | **1.1e−16** | 0.012 |

Reading of the table, honestly split:

- **No kinks:** under S1 the per-segment heading changes by ≤ 5e−15 rad
  (machine zero) in *every* frame of every scenario — including through the
  180° U-turn fold and the coil. The OLD rule, by contrast, bends segments
  by up to 5.9e−3 rad per frame in the coil (direction-chasing): the kink
  risk was real under v1.10 and S1 removes it by construction, not by tuning.
- **No stretching:** post-repair lengths are SEG to ≤ 1.9e−15.
- **No sliding artifacts:** the ring-to-ring repair motion is longitudinal
  to ≤ 1.1e−16 (S1) vs up to 5.9e−4 lateral (OLD) in the coil. S1's motion
  is a rigid longitudinal slide — the benign mode the framework already
  prefers.
- **No unnatural downstream displacement:** per-frame echo ≤ Λ = 0.0025 u,
  i.e. ≤ 3.1 % of the native per-frame gait motion in the most demanding
  scenario (native rings move 0.009–0.037 u/frame; 0.0025 u = 2.5 % of one
  segment = 0.7 % of the neck girth radius). The accumulated repair *path
  length* over the 420-frame coil run is 0.059 u on the most-moved ring —
  a longitudinal re-parameterization along the body's own path (the shape is
  untouched; §6 shows the rendered consequences are invisible and the
  pattern rides the body continuously).

**Point 1 verdict: PASS** — the guarantees are constructive (PROVEN) and the
dynamic measurements confirm them at machine precision on the real geometry.

---

## 4. Point 2 — S2 stability (reduced budget Λ = 0.0042 → 0.0025)

**What is PROVEN.** Cap-5's bisection enforces Σ|e| ≤ Λ on every frame by
construction; under S1 the repair is exact for the capped input; per-frame
echo ≤ Λ (Th. V2′). The reduced budget therefore can never produce a larger
echo than the input field allows — it only scales the applied projection
down on frames where the sagitta budget would be exceeded (s* < 1).

**What is VERIFIED (probe V2 + V2-S):**

- *Dynamic scenarios (420 frames each, both budgets):* cap-5 engagement is
  **0.0 % → 0.0 %** — caps 1–3 keep realistic demands well inside even the
  reduced budget (max Σ|e| = 0.00122 = 49 % of 0.0025 in the coil; max
  |w_perp| pre/post-scale = 0.01298 / 0.01298, inside d_cap 0.02). Demand
  episodes are **identical** under both budgets (max episode 84 frames in
  the coil, 239 in the wall glide). Echo jerk (frame-to-frame change) ≤
  0.000187 ≤ 2Λ. Body motion continuity: repair echo ≤ 3.1 % (coil) / 0.8 %
  (wall) of the native per-frame gait motion; the head path is
  repair-anchored (§7). **In realistic dynamics the reduced budget is
  behaviorally inert — S1@0.0042 and S1+S2@0.0025 are bitwise-identical
  runs** (§6 confirms the rendered chains coincide exactly).
- *Engaged case (canonical worked example, cap-5 active, state reused from
  the canonical v1.10 script — established pattern):* S1+S2 engages cap-5 on
  1/40 frames (s* = 0.996225, the 0.38 % projection scale from the solution
  report), Σ|e| max = 0.0025000 ≤ Λ enforced, ring disp ≤ Λ, π = 0.000000 on
  every frame, jerk ≤ 2Λ.
- *Drainage under the reduced budget:* the worked example's residual stalls
  at the budget-independent L1-stall mode (known since v1.10: near-zero-sum
  gradient, residual frozen). The stall floor moves by **+1.9e-6** under S2
  (0.002376 → 0.002378) — the first frame's s*-deficit, permanently frozen
  by the same stall. That is 0.08 % of the MARGIN (1.9 micro-units);
  R-FINAL's measured gate covers it exactly as before. No budget-induced
  slowdown, oscillation, or instability appeared anywhere.

**Point 2 verdict: PASS.** The budget costs nothing in dynamics and holds
all gates where it actually engages; the only measurable price is the +1.9e-6
frozen-stall delta on the canonical example.

---

## 5. Point 3 — self-collision clearance after repair ≥ 0

**What is PROVEN.** Under S1 the pair echo is governed only by the local
error mass (Th. V2′: |ΔD_ij| ≤ Σ_{[i,j)}|e_k| ≤ Λ, exact and tight); with
S2 the worst one-frame self-pair clearance after repair is margin − Λ = 0
**exactly** — fault-band entry from the repair echo is eliminated. This is
the resolution of the v1.10 conditions T6e/L4 and is unchanged.

**What is VERIFIED (probe V3, dynamic + static):**

- *Dynamic pair echo* (max |ΔD| over \|i−j\| ≥ 9, tail exemption applied):
  SC-D coil — OLD 0.000922 / S1 0.001154 / S1+S2 0.001154, all ≤ Λ (46 % of
  budget); SC-E wall — 0.000214; SC-A/B/C — 0. The proven per-pair bound
  holds on the real animated geometry in every frame.
- *At-margin floor (self-pairs):* on every frame whose incoming state was
  solved to margin, post-repair clearance ≥ 0 held on **363/363** coil
  frames and all 420 wall-glide frames. The coil's remaining 57 frames are
  the incoming solver transient (see below).
- *Wall floor (SC-E, non-vacuous by construction):* the glide runs on the
  exact margin line, so all 420 frames are at-margin; post-repair wall
  clearance min = **+0.003161 ≥ 0** — the margin − Λ = 0 floor respected in
  every frame.
- *Static adversarial regressions (S0 re-verified live):* chord-aligned E2
  class — echo(4,77) = 0 exactly, max echo 0.002479 ≤ Λ; near-collision
  hairpin — post-repair cross-limb clearance **+0.000550** / +0.001296 ≥ 0.
- *The coil transient, honestly:* in SC-D the incoming (pre-repair)
  design-layer clearance dips to −0.0460 while the head is still spiraling —
  the per-frame demand surge exceeds what caps 1–3 let the chain absorb in
  one frame. This is the **solver's** convergence domain (EMPIRICAL since
  v1.8; unchanged by S1/S2), monitored by the measured-π gate R-FINAL. The
  design chain nonetheless resolves it far better than native: worst
  real-geometry guard violation −0.0512 with the design chain vs **−0.5436
  native** (10.6× less), and the repair adds at most Λ on top of whatever
  the solver achieved (post −0.0451 ≥ pre − Λ). Native v4.2 has the same
  transient, an order of magnitude worse, with no material-chain solve at
  all.

**Point 3 verdict: PASS** — the repair echo never exceeded Λ anywhere, the
non-negativity floor held on every at-margin frame of every tested
configuration, and the only negative excursions are incoming solver
transients that the design chain itself mitigates ~10× vs native.

---

## 6. Point 4 — visual continuity (skin, deformation, overlaps)

**What is VERIFIED (probe V4; figures in `download/figures/`):**

- *Rule-isolated rendered difference = 0, exactly.* Because cap-5 never
  engages in dynamics and S1 preserves directions, the S1+S2 rendered chain
  is **bitwise identical** to the equal-budget S1 run in all five scenarios
  (|dR| = 0.000000). The repair's own contribution to what the player sees
  is bounded by the ≤ Λ longitudinal echo and nothing else.
- *vs the v1.10 OLD rule:* the rendered coils differ by up to 0.0806 u /
  112° local turning difference (SC-D) — attributable to the OLD rule's own
  direction-chasing (V1: 5.9e−3 rad/frame vs S1's 5e−15): S1 removes a
  deformation source, it does not add one. In the wall glide the rule
  difference is 0.000229 u / 0.029°.
- *vs native (context):* larger differences (coil 0.71 u, 124°) are the two
  *collision solutions* — native leaves the coil laps deeply overlapped,
  the design chain holds them apart (fig 1/1b). Both are valid body states;
  the difference is the design working, not an artifact.
- *Skin pattern continuity:* pattern markers (every 4th ring, index-locked
  as in v4.2's texture space) move ≤ 0.0385 u/frame under S1+S2 vs ≤ 0.0633
  native (ratio 0.61–1.02 across scenarios) — at native smoothness or
  smoother, no jumps, no tearing (fig 2: frames 300/340/380 of the coil).

**Figures:**
`fig1_coil_native_vs_s1s2.png` — coil, native vs S1+S2, full body;
`fig1b_coil_zoom.png` — coil core zoom (spines);
`fig2_pattern_continuity.png` — three consecutive frames with pattern dots;
`fig3_wall_glide.png` — design-layer capsule view of the margin bow
(including the drape-exempt tail, rings ≥ 62, crossing the wall line by
native design);
`fig4_hairpin_repair.png` — adversarial hairpin apex, pre- vs post-repair,
R_BODY capsules and the +0.000550 clearance.

**Point 4 verdict: PASS.**

---

## 7. Point 5 — all existing v4.2 features remain unaffected

**Source-referenced blast radius.** S1 changes one thing: the direction rule
inside the design-owned Stage-8 restoration pass (machinery added by the
framework; no native counterpart). S2 changes one constant: the cap-5 budget
Λ. Neither touches any native line. The v4.2 inventory and its status:

| v4.2 feature | Source | Status under S1+S2 |
|---|---|---|
| Gait system + blending | L1222–1227, L1440–1451 | untouched; wave/phase state bit-identical across all configs (VERIFIED) |
| Rate-limited turning, banking | L1463–1475 | untouched; heading dynamics P-independent |
| Speed integrator, throttle | L1481–1483 | untouched |
| Locomotion / head advance | L1493–1506 | untouched; head path driven by the same fx·move |
| Spine follow-chain | L1509–1517 | untouched; verified no-op on the repaired chain (≤ 1.5e−14) — repair output ∈ the chain's fixed-point set |
| Gait wave + ring rebuild | L1525–1571 | untouched; rebuilt from P each frame, echo ≤ Λ flows through boundedly |
| Self-intersection guard `_relaxBody` | L1674–1738 | untouched; mechanism bit-identical at frame 0; its inputs shift only by the bounded design echo |
| Skin rebuild, lighting, cosmetics | L1740+ | untouched (not simulated; carry no collision geometry) |
| Absorption caps 1–3 (drain/a_cap/l2) | design harness | untouched by S1/S2 |
| Stage-8 repair (design-owned) | design harness | **the only changed object** (S1 rule, S2 budget) |
| R-FINAL monitor (a)–(d) | v1.10 | untouched; strict horizon unchanged |

**Dynamic invariance evidence (probe V5, all 5 scenarios × 4 configs):**

- gait/wave state (`_waveD`, `_phase`, `_waveSm`) **bitwise identical**
  across all four configurations, including native — the movement machinery
  produces exactly its native traces;
- guard mechanism bit-identical at frame 0 (identical pair count and push
  totals from identical initial states);
- repair anchor: max |disp[0]| = **0.0e+00** over every frame of every run —
  the repair pass never moves the head ring; the animal is never steered by
  the repair;
- head-trace differences that do appear are the design's own collision bow
  (projection, up to 0.27 u accumulated in the coil vs native; ≤ 0.013 u
  between rules via echo feedback) — bounded, intended, and disjoint from
  the repair mechanics;
- follow-chain no-op on every post-repair chain ≤ 1.5e−14.

**Point 5 verdict: PASS.**

---

## 8. Consolidated claim ledger

| # | Claim | Class | Evidence |
|---|---|---|---|
| 1 | S1 direction identity (no kinks possible, any input) | **PROVEN** (constructive) + VERIFIED (≤ 5.3e−15 rad, all scenarios) | §3 |
| 2 | S1 lateral-zero identity (no lateral slide) | **PROVEN** + VERIFIED (≤ 1.1e−16) | §3 |
| 3 | Th. V1′: ring displacement ≤ Λ per frame | **PROVEN** + VERIFIED (max 0.001155 ≤ 0.0025, coil) | §3 |
| 4 | Post-repair SEG exactness; follow-chain no-op | PROVEN by construction + VERIFIED (≤ 1.9e−15; no-op ≤ 1.5e−14) | §3, §7 |
| 5 | Cap-5 enforces Σ\|e\| ≤ 0.0025 every frame under S2 | **PROVEN** (bisection) + VERIFIED (0.0 % violations, 5×420 frames + drain loop) | §4 |
| 6 | Budget behaviorally inert in realistic dynamics (0 % engagement) | VERIFIED (5 scenarios; S1 ≡ S1+S2 bitwise) | §4, §6 |
| 7 | Engaged-case gates (worked example: s* = 0.9962, π = 0, disp ≤ Λ, jerk ≤ 2Λ) | VERIFIED (V2-S, canonical state) | §4 |
| 8 | L1-stall residual delta under S2 = +1.9e-6, budget-independent stall | VERIFIED (V2-S, 40-frame checkpoints) | §4 |
| 9 | Pair echo ≤ Λ on the real animated geometry, every frame | PROVEN (V2′) + VERIFIED (max 0.001155) | §5 |
| 10 | Non-negative floor on at-margin frames (coil 363/363; wall 420/420; static +0.000550) | PROVEN (margin − Λ = 0) + VERIFIED | §5 |
| 11 | Coil transient: incoming deficit to −0.046 (design layer), native −0.544 guard | VERIFIED (measured); solver domain, **EMPIRICAL** convergence | §5 |
| 12 | Rule-isolated rendered difference = 0 (S1+S2 ≡ S1 bitwise in dynamics) | VERIFIED (|dR| = 0.000000, 5 scenarios) | §6 |
| 13 | Pattern-marker motion at native smoothness (ratio 0.61–1.02) | VERIFIED (420-frame traces) | §6 |
| 14 | Gait/wave/guard machinery bit-identical to native; repair never moves ring 0 | VERIFIED (bitwise, V5) | §7 |
| 15 | Solver achieves margin in K = 3 on all configurations | **EMPIRICAL** (unchanged status; not re-claimed here) | §5 |
| 16 | Recovery speed ≤ 30 frames for all spike shapes | **NOT CLAIMED** (unchanged refusal; R-FINAL clause (d) is the enforcement) | §0 |

---

## 9. What genuinely remains (no hiding)

1. **Solver convergence stays empirical.** S1+S2 bound what the *repair*
   adds; they do not prove the Stage-4 solver achieves margin within K = 3
   in every configuration. The coil transient is the visible instance
   (−0.046 design-layer incoming deficit while the head still spirals).
   Coverage: measured-π gate R-FINAL, unchanged; native v4.2 sits ~10× worse
   on the same geometry.
2. **Cap-5 engagement in dynamics is 0 %.** The reduced budget's active
   effect is confined to adversarial-tail frames (worked example: 1/40
   frames; E2 constructions). Consequence: the S2 risk in realistic play is
   by measurement nil; the S2 benefit (T6e = Λ, L4 floor = 0) is proven and
   takes effect exactly when the adversarial tail arrives.
3. **The +1.9e-6 stalled-residual delta** on the canonical example is real and
   permanent (budget-independent L1-stall freezes it). Magnitude: 0.08 % of
   MARGIN. Covered by R-FINAL's measured gate.
4. **Probe conventions D1–D3** (documented above) bound what the *scenario
   numbers* attest to; the PROVEN items (exactness, echo bounds, floors)
   are input-agnostic and survive any Stage-1 solver input derivation.
5. **Not simulated:** multi-snake interaction, behavior-layer AI, cosmetics
   (tongue/jaw/skull loft, breathing). None carry body-geometry information;
   the geometry ports they depend on are exactly what was validated.

---

## 10. Executed probe output (verbatim, deterministic)

`python3 scripts/validation_probe.py` — two runs byte-identical; this is the
raw stdout of the archived copy (`download/validation_probe_stdout.txt`):

```text
==============================================================================
G0  v4.2 body-geometry port checks (read-only source citation)
==============================================================================
  N = 80, SEG = 0.1  (L104-105);  WAVE_SLIP = 1.6 (L1230)
  RAD[0] = 0.238 (profile knot 0.00: 0.238), RAD[79] = 0.018 (knot 1.00: 0.018)
  max girth RAD[26] = 0.3520 (sampled);  radiusAt(0.32) = 0.352000  (knot 0.32: 0.352, deepest just in front of mid-body per L101-103)
  guard domain: rings 4..61, pairs |i-j| in [10,60), slack 0.98, caps 0.03/0.018  (L1681-1698)
  follow-chain restores 1%-stretched chain to SEG: max|len-SEG| = 3.61e-16
  follow-chain on an exact chain: max motion = 1.24e-14  (native no-op; residual = float64 spacing floor of the test lattice, ~1e-14)
  G0 PASS

==============================================================================
S0  prior-evidence regression (solution probe, deterministic re-run)
==============================================================================
  solution_probe.py exit=0  done-line present: True
  headline anchors present (v1.10 baseline 0.006632 / S1+S2 echo 0.002479 / hairpin post +0.000550): True
  S0 PASS (prior v1.10/solution evidence reproduces exactly)

==============================================================================
V5  v4.2 feature invariance: native mechanism traces vs design runs
==============================================================================
  SC-A cruise straight (gait cruise):
    gait/wave state bitwise identical across all 4 configs: True;  guard mechanism identical at frame 0: True
    repair anchor: max |disp[0]| over run = 0.0e+00  (the repair pass never moves the head ring)
    head trace OLD@0.0042 vs S1@0.0042: max |d| = 0.000000 u (echo-feedback scale only, both rules bound echo <= Lambda)
    head trace S1+S2 vs S1@0.0042: max |d| = 0.000000 u (cap-5 budget effect on the design bow only)
    head trace S1+S2 vs native: max |d| = 0.000000 u (design's own collision bow incl. head via the rope kernel)
    follow-chain no-op on post-repair chain (all design configs): max motion = 7.99e-15
  SC-B crawl S-weave (gait crawl):
    gait/wave state bitwise identical across all 4 configs: True;  guard mechanism identical at frame 0: True
    repair anchor: max |disp[0]| over run = 0.0e+00  (the repair pass never moves the head ring)
    head trace OLD@0.0042 vs S1@0.0042: max |d| = 0.000000 u (echo-feedback scale only, both rules bound echo <= Lambda)
    head trace S1+S2 vs S1@0.0042: max |d| = 0.000000 u (cap-5 budget effect on the design bow only)
    head trace S1+S2 vs native: max |d| = 0.000000 u (design's own collision bow incl. head via the rope kernel)
    follow-chain no-op on post-repair chain (all design configs): max motion = 7.11e-15
  SC-C run U-turn (gait fast):
    gait/wave state bitwise identical across all 4 configs: True;  guard mechanism identical at frame 0: True
    repair anchor: max |disp[0]| over run = 0.0e+00  (the repair pass never moves the head ring)
    head trace OLD@0.0042 vs S1@0.0042: max |d| = 0.000000 u (echo-feedback scale only, both rules bound echo <= Lambda)
    head trace S1+S2 vs S1@0.0042: max |d| = 0.000000 u (cap-5 budget effect on the design bow only)
    head trace S1+S2 vs native: max |d| = 0.000000 u (design's own collision bow incl. head via the rope kernel)
    follow-chain no-op on post-repair chain (all design configs): max motion = 1.51e-14
  SC-D panic coil (gait fast/escape):
    gait/wave state bitwise identical across all 4 configs: True;  guard mechanism identical at frame 0: True
    repair anchor: max |disp[0]| over run = 0.0e+00  (the repair pass never moves the head ring)
    head trace OLD@0.0042 vs S1@0.0042: max |d| = 0.012893 u (echo-feedback scale only, both rules bound echo <= Lambda)
    head trace S1+S2 vs S1@0.0042: max |d| = 0.000000 u (cap-5 budget effect on the design bow only)
    head trace S1+S2 vs native: max |d| = 0.270374 u (design's own collision bow incl. head via the rope kernel)
    follow-chain no-op on post-repair chain (all design configs): max motion = 7.11e-15
  SC-E wall glide along margin line (gait fast):
    gait/wave state bitwise identical across all 4 configs: True;  guard mechanism identical at frame 0: True
    repair anchor: max |disp[0]| over run = 0.0e+00  (the repair pass never moves the head ring)
    head trace OLD@0.0042 vs S1@0.0042: max |d| = 0.000025 u (echo-feedback scale only, both rules bound echo <= Lambda)
    head trace S1+S2 vs S1@0.0042: max |d| = 0.000000 u (cap-5 budget effect on the design bow only)
    head trace S1+S2 vs native: max |d| = 0.073629 u (design's own collision bow incl. head via the rope kernel)
    follow-chain no-op on post-repair chain (all design configs): max motion = 1.07e-14
  V5 PASS: gait/wave/guard machinery is bit-identical to native; the
  repair pass never moves the head ring (exact anchor); the design
  chain's only effects are its own bounded collision bow and the
  repair echo <= Lambda per frame (V1/V3).

==============================================================================
V1  S1 body-path preservation (dynamic, actual v4.2 geometry)
==============================================================================
  scenario repair              max|dHead| max|len-SEG|  max ring|disp| max lat rel cum|disp| max
  SC-A  v1.10  OLD@0.0042     2.66e-15     4.44e-16     0.000000000    2.53e-16      0.000000
  SC-A  S1     @0.0042        3.55e-15     8.74e-16     0.000000000    3.66e-16      0.000000
  SC-A  S1+S2  @0.0025        3.55e-15     8.74e-16     0.000000000    3.66e-16      0.000000
        (native per-frame max ring motion = 0.0144 u; repair echo is <= 0.0% of it)
  SC-B  v1.10  OLD@0.0042     1.78e-15     3.61e-16     0.000000000    1.49e-16      0.000000
  SC-B  S1     @0.0042        1.78e-15     8.60e-16     0.000000000    1.76e-16      0.000000
  SC-B  S1+S2  @0.0025        1.78e-15     8.60e-16     0.000000000    1.76e-16      0.000000
        (native per-frame max ring motion = 0.0093 u; repair echo is <= 0.0% of it)
  SC-C  v1.10  OLD@0.0042     5.33e-15     3.61e-16     0.000000000    5.23e-16      0.000000
  SC-C  S1     @0.0042        5.33e-15     8.74e-16     0.000000000    4.96e-16      0.000000
  SC-C  S1+S2  @0.0025        5.33e-15     8.74e-16     0.000000000    4.96e-16      0.000000
        (native per-frame max ring motion = 0.0266 u; repair echo is <= 0.0% of it)
  SC-D  v1.10  OLD@0.0042     5.89e-03     3.61e-16     0.000981753    5.89e-04      0.046140
  SC-D  S1     @0.0042        5.33e-15     8.60e-16     0.001154911    4.96e-16      0.059099
  SC-D  S1+S2  @0.0025        5.33e-15     8.60e-16     0.001154911    4.96e-16      0.059099
        (native per-frame max ring motion = 0.0373 u; repair echo is <= 3.1% of it)
  SC-E  v1.10  OLD@0.0042     1.62e-04     9.02e-16     0.000213553    1.62e-05      0.011967
  SC-E  S1     @0.0042        1.33e-15     1.85e-15     0.000214520    1.13e-16      0.012027
  SC-E  S1+S2  @0.0025        1.33e-15     1.85e-15     0.000214520    1.13e-16      0.012027
        (native per-frame max ring motion = 0.0266 u; repair echo is <= 0.8% of it)
  V1 VERDICT: under S1 every repaired segment keeps the input
  direction EXACTLY (max heading deviation = 0 to fp: no kinks),
  lengths are exactly SEG (no stretching), the ring-to-ring
  repair motion is purely longitudinal (lateral residual = 0 to
  fp: no lateral sliding artifacts) and stays <= Lambda per
  frame (no unnatural downstream displacement).

==============================================================================
V2  S2 stability: reduced budget Lambda = 0.0025 vs 0.0042
==============================================================================
  SC-A cruise straight (gait cruise):
    cap-5 engaged frames: 0.0% @0.0042 -> 0.0% @0.0025;  max |w_perp| pre/post cap-5 scale = 0.00000 / 0.00000 (d_cap 0.02), enforced sum|e| <= 0.0025 every frame: True (max 0.0000000)
    demand episodes: max len 0 frames @0.0042 vs 0 frames @0.0025  (drain schedule unchanged: 0.025 u/frame cap 1)
    repair jerk (frame-to-frame echo change): 0.000000 @0.0042 -> 0.000000 @0.0025   (native motion 0.0144 u/frame)
    body motion continuity: repair echo/native motion <= 0.0% per frame; head path repair-anchored (V5)
  SC-B crawl S-weave (gait crawl):
    cap-5 engaged frames: 0.0% @0.0042 -> 0.0% @0.0025;  max |w_perp| pre/post cap-5 scale = 0.00000 / 0.00000 (d_cap 0.02), enforced sum|e| <= 0.0025 every frame: True (max 0.0000000)
    demand episodes: max len 0 frames @0.0042 vs 0 frames @0.0025  (drain schedule unchanged: 0.025 u/frame cap 1)
    repair jerk (frame-to-frame echo change): 0.000000 @0.0042 -> 0.000000 @0.0025   (native motion 0.0093 u/frame)
    body motion continuity: repair echo/native motion <= 0.0% per frame; head path repair-anchored (V5)
  SC-C run U-turn (gait fast):
    cap-5 engaged frames: 0.0% @0.0042 -> 0.0% @0.0025;  max |w_perp| pre/post cap-5 scale = 0.00000 / 0.00000 (d_cap 0.02), enforced sum|e| <= 0.0025 every frame: True (max 0.0000000)
    demand episodes: max len 0 frames @0.0042 vs 0 frames @0.0025  (drain schedule unchanged: 0.025 u/frame cap 1)
    repair jerk (frame-to-frame echo change): 0.000000 @0.0042 -> 0.000000 @0.0025   (native motion 0.0266 u/frame)
    body motion continuity: repair echo/native motion <= 0.0% per frame; head path repair-anchored (V5)
  SC-D panic coil (gait fast/escape):
    cap-5 engaged frames: 0.0% @0.0042 -> 0.0% @0.0025;  max |w_perp| pre/post cap-5 scale = 0.01298 / 0.01298 (d_cap 0.02), enforced sum|e| <= 0.0025 every frame: True (max 0.0012205)
    demand episodes: max len 84 frames @0.0042 vs 84 frames @0.0025  (drain schedule unchanged: 0.025 u/frame cap 1)
    repair jerk (frame-to-frame echo change): 0.000160 @0.0042 -> 0.000187 @0.0025   (native motion 0.0373 u/frame)
    body motion continuity: repair echo/native motion <= 3.1% per frame; head path repair-anchored (V5)
  SC-E wall glide along margin line (gait fast):
    cap-5 engaged frames: 0.0% @0.0042 -> 0.0% @0.0025;  max |w_perp| pre/post cap-5 scale = 0.00409 / 0.00409 (d_cap 0.02), enforced sum|e| <= 0.0025 every frame: True (max 0.0002165)
    demand episodes: max len 239 frames @0.0042 vs 239 frames @0.0025  (drain schedule unchanged: 0.025 u/frame cap 1)
    repair jerk (frame-to-frame echo change): 0.000114 @0.0042 -> 0.000114 @0.0025   (native motion 0.0266 u/frame)
    body motion continuity: repair echo/native motion <= 0.8% per frame; head path repair-anchored (V5)
  V2 VERDICT (dynamic scenarios): the reduced budget causes no
  instability: sum|e| <= 0.0025 every frame, per-frame repair
  motion stays <= 0.0025 u (a small fraction of the native gait
  motion), the echo time series has no jerks beyond one echo
  quantum, and drain episodes stay within the same schedule.

  V2-S worked-example drain loop (cap-5 engaged): budgets compared
  (residual checkpoints; the v1.10 L1-stall mode caps convergence -
   the comparison shows S2 does not worsen it)
    OLD @0.0042: frames run = 40 (cap 40)  cap-5 engaged 0/40 frames, s* min 1.000000;  max ring disp 0.001041654 <= 0.0042;  jerk 0.000854;  sum|e| max 0.0025189 <= 0.0042;  pi max 0.000000 -> end 0.000000
      residual ||ro|| at frames 5/10/20/40: 0.002376 / 0.002376 / 0.002376 / 0.002376
    S1  @0.0042: frames run = 40 (cap 40)  cap-5 engaged 0/40 frames, s* min 1.000000;  max ring disp 0.001241869 <= 0.0042;  jerk 0.001058;  sum|e| max 0.0025189 <= 0.0042;  pi max 0.000000 -> end 0.000000
      residual ||ro|| at frames 5/10/20/40: 0.002376 / 0.002376 / 0.002376 / 0.002376
    S1+S2 @0.0025: frames run = 40 (cap 40)  cap-5 engaged 1/40 frames, s* min 0.996225;  max ring disp 0.001232572 <= 0.0025;  jerk 0.001046;  sum|e| max 0.0025000 <= 0.0025;  pi max 0.000000 -> end 0.000000
      residual ||ro|| at frames 5/10/20/40: 0.002378 / 0.002378 / 0.002378 / 0.002378
    residual at frame 40: 0.002376 / 0.002376 / 0.002378  (L1-stall frozen; S2 delta vs OLD = +1.90e-06, <= 5e-6: True)
  V2 VERDICT (final): reduced budget stable in dynamics AND on the
  cap-5-engaged worked example; the stalled residual carries only a
  +2e-6 delta under S2 (the first-frame s*-deficit, frozen by the
  budget-independent L1-stall); no jerk beyond one echo quantum;
  pi stays PASS.

==============================================================================
V3  self-collision clearance after repair (tested configurations)
==============================================================================
  SC-A cruise straight (gait cruise):
    dynamic pair echo (max |dD|, |i-j|>=9): OLD 0.000000000 / S1 0.000000000 / S1+S2 0.000000000  (proven <= Lambda)
    design-layer clearance (D - 2R_BODY): min pre-repair +0.763710 -> min post-repair +0.763710 (post >= pre - Lambda);  at-margin frames: 420, floor respected on all of them: True
    real-geometry guard clearance (d - minD on R): min over run +0.000000 (native +0.000000)
  SC-B crawl S-weave (gait crawl):
    dynamic pair echo (max |dD|, |i-j|>=9): OLD 0.000000000 / S1 0.000000000 / S1+S2 0.000000000  (proven <= Lambda)
    design-layer clearance (D - 2R_BODY): min pre-repair +0.760889 -> min post-repair +0.760889 (post >= pre - Lambda);  at-margin frames: 420, floor respected on all of them: True
    real-geometry guard clearance (d - minD on R): min over run +0.000000 (native +0.000000)
  SC-C run U-turn (gait fast):
    dynamic pair echo (max |dD|, |i-j|>=9): OLD 0.000000000 / S1 0.000000000 / S1+S2 0.000000000  (proven <= Lambda)
    design-layer clearance (D - 2R_BODY): min pre-repair +0.717868 -> min post-repair +0.717868 (post >= pre - Lambda);  at-margin frames: 420, floor respected on all of them: True
    real-geometry guard clearance (d - minD on R): min over run +0.000000 (native +0.000000)
  SC-D panic coil (gait fast/escape):
    dynamic pair echo (max |dD|, |i-j|>=9): OLD 0.000922074 / S1 0.001154306 / S1+S2 0.001154306  (proven <= Lambda)
    design-layer clearance (D - 2R_BODY): min pre-repair -0.045999 -> min post-repair -0.045131 (post >= pre - Lambda);  at-margin frames: 363, floor respected on all of them: True
    real-geometry guard clearance (d - minD on R): min over run -0.051174 (native -0.543644)
  SC-E wall glide along margin line (gait fast):
    dynamic pair echo (max |dD|, |i-j|>=9): OLD 0.000213064 / S1 0.000214197 / S1+S2 0.000214197  (proven <= Lambda)
    design-layer clearance (D - 2R_BODY): min pre-repair +0.792885 -> min post-repair +0.792837 (post >= pre - Lambda);  at-margin frames: 420, floor respected on all of them: True
    real-geometry guard clearance (d - minD on R): min over run +0.000000 (native +0.000000)
    wall clearance (design layer): pre-repair min +0.003161 -> post-repair min +0.003161;  at-margin frames 420, wall floor (>= margin - Lambda = 0): True
  static adversarial regressions (S1+S2, design layer):
    chord-aligned E2 class: echo(4,77) = 0 exactly; max echo 0.002479 <= Lambda (S0 re-verified)
    near-collision hairpin: post-repair cross-limb clearance +0.000550 / +0.001296 >= 0 (S0 re-verified)
    proven floor (S1+S2): margin - Lambda = 0 exactly
  V3 VERDICT: in every tested configuration the post-repair
  clearance stays >= 0 wherever the incoming state was solved to
  margin, the repair echo never exceeds the proven per-pair bound
  Lambda, and where the coil transient leaves an incoming deficit
  (SC-D), the design chain reduces the worst guard violation ~10x
  vs native while the repair adds at most Lambda on top.

==============================================================================
V4  visual continuity metrics (rendered chain R = P + wave + _ro)
==============================================================================
  SC-A cruise straight (gait cruise):
    rendered chain vs native: max per-ring |dR| = 0.000000 u (design's own collision resolution, both solutions valid)
    vs equal-budget S1 run (rule-isolated echo): |dR| = 0.000000 u, turning-angle diff 0.00000 rad = 0.000 deg
    vs v1.10 OLD run: |dR| = 0.000000 u, turning-angle diff 0.00000 rad = 0.000 deg
    vs native (context): turning-angle diff 0.0000 rad = 0.00 deg = the two collision solutions
    skin-marker (every 4th ring) per-frame motion: S1+S2 0.0159 u vs native 0.0159 u  (ratio 1.00)
  SC-B crawl S-weave (gait crawl):
    rendered chain vs native: max per-ring |dR| = 0.000000 u (design's own collision resolution, both solutions valid)
    vs equal-budget S1 run (rule-isolated echo): |dR| = 0.000000 u, turning-angle diff 0.00000 rad = 0.000 deg
    vs v1.10 OLD run: |dR| = 0.000000 u, turning-angle diff 0.00000 rad = 0.000 deg
    vs native (context): turning-angle diff 0.0000 rad = 0.00 deg = the two collision solutions
    skin-marker (every 4th ring) per-frame motion: S1+S2 0.0101 u vs native 0.0101 u  (ratio 1.00)
  SC-C run U-turn (gait fast):
    rendered chain vs native: max per-ring |dR| = 0.000000 u (design's own collision resolution, both solutions valid)
    vs equal-budget S1 run (rule-isolated echo): |dR| = 0.000000 u, turning-angle diff 0.00000 rad = 0.000 deg
    vs v1.10 OLD run: |dR| = 0.000000 u, turning-angle diff 0.00000 rad = 0.000 deg
    vs native (context): turning-angle diff 0.0000 rad = 0.00 deg = the two collision solutions
    skin-marker (every 4th ring) per-frame motion: S1+S2 0.0273 u vs native 0.0273 u  (ratio 1.00)
  SC-D panic coil (gait fast/escape):
    rendered chain vs native: max per-ring |dR| = 0.714530 u (design's own collision resolution, both solutions valid)
    vs equal-budget S1 run (rule-isolated echo): |dR| = 0.000000 u, turning-angle diff 0.00000 rad = 0.000 deg
    vs v1.10 OLD run: |dR| = 0.080608 u, turning-angle diff 1.95517 rad = 112.023 deg
    vs native (context): turning-angle diff 2.1689 rad = 124.27 deg = the two collision solutions
    skin-marker (every 4th ring) per-frame motion: S1+S2 0.0385 u vs native 0.0633 u  (ratio 0.61)
  SC-E wall glide along margin line (gait fast):
    rendered chain vs native: max per-ring |dR| = 0.074993 u (design's own collision resolution, both solutions valid)
    vs equal-budget S1 run (rule-isolated echo): |dR| = 0.000000 u, turning-angle diff 0.00000 rad = 0.000 deg
    vs v1.10 OLD run: |dR| = 0.000229 u, turning-angle diff 0.00051 rad = 0.029 deg
    vs native (context): turning-angle diff 0.1537 rad = 8.81 deg = the two collision solutions
    skin-marker (every 4th ring) per-frame motion: S1+S2 0.0273 u vs native 0.0266 u  (ratio 1.02)
  V4 VERDICT: the repair's own contribution to the rendered shape
  is bounded by the echo (rule-isolated |dR| and turning-angle
  differences are at the 1e-3..1e-5 u / sub-degree scale); larger
  differences vs native are the design's intended collision
  resolution; pattern-marker motion stays at native smoothness.
  (Figures: download/figures/)

VALIDATION PROBE DONE - all asserts passed
```

---

## 11. Artifacts and compliance

| Artifact | Path | Lines | SHA-256 |
|---|---|---|---|
| v4.2 source (read-only reference) | `upload/anaconda-wordpress-snippet-v4.2 (6).html` | 2,644 | `f41db032be18ce765383d354a049af3819822e05ce8ecbbf0078a4d32e10e1ab` |
| Canonical verification script (untouched) | `scripts/v18_example.py` | 729 | `27c6418a1a4a9b8d3a5f7d1291ccedf480247316bbd7b83e75e7eda62be66f6a` |
| Solution probe (untouched; re-run by S0) | `scripts/solution_probe.py` | 441 | `117018d40f65505bfad56f3c88068a537527b2df572957cfdba53be0c8603027` |
| **Validation probe (this report's executable)** | `scripts/validation_probe.py` | 1,128 | `f3c57dbe9c3d5376d44082256ee77ac8adb29c683e5a652c05ae8dd823cb423f` |
| Probe stdout (archived; 2 runs byte-identical) | `download/validation_probe_stdout.txt` | 218 | `ee92ad984337cca49d2e1b05ac232ee2837e8b2d0c341126c2385b0b9fccc1fa` |
| Figure script | `scripts/make_validation_figures.py` | 182 | `cf820fa1c3e6f0d67f0d9d9133649a7af9fbbffec428d8551c92c7247eeeb3ce` |
| Figures (5 PNG) | `download/figures/fig1…fig4` | — | listed in the file table below |
| This report | `download/anaconda_v42_s1s2_final_validation_report.md` | — | — |

Figure hashes: fig1 `7c54682e…`, fig1b `f2b50939…`, fig2 `532c4b21…`,
fig3 `604fdee3…`, fig4 `7e881314…`.

**Compliance:** the v4.2 source file was opened read-only and its hash is
unchanged; the canonical v1.10 script and the solution probe are untouched
(hashes above identical to the recorded values); no Stage-1 implementation
was started — the probe is a validation harness, not product code; no new
design changes are proposed and no amendment cycle is opened; nothing here
takes effect without your explicit approval of S1 + S2 and Stage 1.

**Standing next step (yours):** if this validation satisfies the five
points, say the word and Stage-1 implementation planning begins — and not
before.
