# Version CK Review Summary

## Recommendations

| Reviewer | Recommendation | Change from CJ |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | Maintained |
| GPT-5.2 | **Major Revision** | Maintained |
| Claude Opus 4.6 | **Major Revision** | Maintained |

## What CK Fixed (Acknowledged by Reviewers)

1. **γ unification** — All three note consistent γ₂₄=0.761, γ₃₀=0.745 with time-domain computation; no discrepancies found
2. **Three-step feasibility workflow** — GPT notes "strong logical structure"; Claude notes screening heuristic is "appropriately caveated"
3. **Campaign duty factor d** — GPT: "substantive improvement that addresses workload realism"; Claude: "well done" with practitioner recipe
4. **Packet-level reframing** — Partial progress; Claude notes footnote ‡ in claim map but wants main text to be more explicit
5. **Scope limitation** — Both GPT and Claude note "preliminary design estimates" and validation gap transparency
6. **GE parameter mapping** — p_BG ≈ T_c/T̄_B formula acknowledged; geometric shadowing justification noted
7. **Second γ worked example** — Claude acknowledges Ka-band example; GPT notes "potentially one of the most reusable artifacts"
8. **Mission-phase mapping** — Table duty_mapping acknowledged by Claude
9. **AoI sampling policy tail** — GPT: "correctly identified as sampling-policy tail"
10. **Thundering herd back-off** — Gemini notes improved treatment but raises sync assumption

## Major Issues Remaining

### Priority 1: Manuscript Length and Density (Claude #3, GPT implicit)
Paper is ~12,000+ words body text + extensive tables/figures. All three reviewers suggest trimming. Claude recommends moving practitioner recipes, worked examples, failure-mode analyses to supplementary. Target: ~8,000 words body text.

### Priority 2: Acquisition Architecture as First-Order Design Axis (GPT #1)
The 30 vs 35 kbps recommendation hinges on per-slot cold-start acquisition assumption. If amortized per-superframe, minimum viable PHY drops to ~25 kbps. Need conditional recommendation table: per-slot → 35 kbps; per-superframe → 30 kbps; hybrid → intermediate.

### Priority 3: α_RX Derivation (GPT #2)
α_RX = 0.908 is treated as an input but is actually derived from the schedule. This creates perceived circularity. Need to either derive α_RX within Algorithm 1 from the slot budget or replace it with direct timing inequalities.

### Priority 4: S-band vs UHF Operational Concept (Gemini #1)
TDMA sizing applies to S-band coordination channel (35 kbps), not UHF RF-backup (2.5 kbps). The text creates tension by saying hierarchy is "suspended" during RF-backup while sizing for hierarchical ingress. Need clearer mode/link-to-analysis mapping.

### Priority 5: DES Compression — Different Bottleneck (GPT #4, Claude #1)
DES tails address coordinator buffer overflow (message-layer), but the safety-critical argument is about TDMA deadline misses (slot-level). Either add slot-level tail metrics or explicitly state DES and slot-sim address different failure modes.

### Priority 6: GE Sensitivity Curves as Primary (GPT #7, Claude #4)
Default p_BG=0.50 results (P95=4 cycles) presented with precision suggesting confidence; no ISL measurements exist. Promote Fig. 5b sensitivity sweep as primary result; demote single-point numbers to examples.

### Priority 7: Feasibility Framework Vocabulary Unification (GPT #3, Claude #5)
Paper alternates between "2-layer" and "3-step" framing. Either commit to 2 layers with a mapping step, or 3 layers with middle as necessary-only. Remove screening heuristic from Algorithm 1.

### Priority 8: Stress-Case Semantic Justification (GPT #6)
512 B command per node per cycle continuously (the stress case) is not tied to a specific mission/autonomy requirement. Either provide a plausible scenario or relabel as synthetic sizing bound.

## Minor Issues (25 total)

### Gemini (5 minor)
1. Table I: d is "duty factor" but used as Bernoulli probability — clarify
2. Fig. 6: Star/Diamond markers may be illegible in B&W
3. GE antenna mispointing τ_c: cite ADCS slew rates
4. Eq. 5: G used for groups conflicts with Antenna Gain / ALOHA G
5. "h" vs "s" units consistency

### GPT (7 minor)
1. γ notation: γ₂₄ looks like a constant; use γ_C(24 kbps) for clarity
2. Table II "20.3 kbps": label as info-rate
3. AoI table: add column/footnote for sampling-policy-driven AoI
4. Algorithm 1 line 4: necessary-only check should be labeled
5. "100% TDMA deadline misses at 24 kbps" in intro: verify corresponds to Model C (not Model S + ARQ)
6. Non-archival references: avoid for quantitative claims
7. η₀ ≈ 5% vs heartbeat alone 5.1%: explain or widen range

### Claude (13 minor)
1. Abstract >250 words (IEEE T-AES guideline)
2. Eq. 1: n_r not explicitly stated in equation context
3. Table II footnote a: AoI independence from C_node assumes byte budget not binding
4. "Hierarchical coordination suspension" should appear earlier
5. Eq. 14: prefer time-domain (Eq. 15) as primary form
6. Table VI: "GE+Exc" header cryptic — expand
7. Fig. 3: check x-axis legibility at column width
8. ESA maneuver cadence scaling with N² fleet size
9. Eq. 5: Raft pipelining assumption
10. Runtime ~7s explanation
11. Reference [1] sourcing strength
12. Table I: f_RF and F used only in Eq. 6 — consider local definition
13. "Version CK" in metadata: remove for submission

## Progress Trajectory

| Version | Gemini | GPT | Claude |
|---------|--------|-----|--------|
| CJ | Accept w/ Minor (3M/4m) | Major (7M/8m) | Major (5M/12m) |
| CK | **Accept w/ Minor (3M/5m)** | **Major (7M/7m)** | **Major (5M/13m)** |

**Assessment:** Gemini maintained Accept with Minor; the safety/locus-of-control concern is new but addressable. GPT maintained Major Revision but concerns shifted: γ consistency (CJ #1) is resolved; new issues are acquisition conditionality, α_RX derivation, and feasibility vocabulary. Claude maintained Major Revision with similar issues to CJ but acknowledges γ unification and duty factor improvements. The core technical content is accepted; the path to Accept is: (1) significant manuscript compression, (2) conditional design recommendation by acquisition architecture, (3) derive α_RX from schedule, (4) clarify S-band vs UHF operational modes, (5) unify feasibility vocabulary.

## Recommended Next Steps for CL

1. **Compress manuscript ~25%**: Move Ka-band example, γ calibration checklist, mission-phase table, margin inventory, thundering herd details to supplementary material
2. **Add acquisition-conditional design table**: R_PHY,min for per-slot / per-superframe / hybrid acquisition
3. **Derive α_RX within Algorithm 1**: Replace externally-supplied α_RX with computed value from timing budget
4. **Clarify S-band ↔ UHF mode-to-analysis mapping**: Add sentence to mode_map table linking TDMA sizing to S-band, not UHF
5. **Add slot-level tail metric**: Distribution of per-cycle margin or deadline-miss fraction from slot-sim
6. **Promote GE sensitivity sweep as primary**: Present Fig. 5b first; demote default-point numbers to examples
7. **Unify feasibility vocabulary**: Commit to "2 layers + screening step" or "3 steps" consistently
8. **Justify stress-case semantics**: Tie 512 B/node/cycle to a plausible autonomy scenario or relabel as synthetic bound
9. **Shorten abstract to ≤250 words**
10. **Remove screening heuristic from Algorithm 1**: Move to separate remark
