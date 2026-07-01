# Version CL Review Summary

## Recommendations

| Reviewer | Recommendation | Change from CK |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | Maintained (2M/3m vs 3M/5m) |
| GPT-5.2 | **Major Revision** | Maintained (9M/8m vs 7M/7m) |
| Claude Opus 4.6 | **Major Revision** | Maintained (5M/11m vs 5M/13m) |

## What CL Fixed (Acknowledged by Reviewers)

1. **Manuscript compression** — Gemini: "dense but well-structured"; Claude: length concern now implicit rather than top-level major issue; paper reduced from 18 to 14 pages
2. **Acquisition-conditional design table** — GPT CK #1 (acquisition modeling) no longer appears as major issue; table added
3. **α_RX derived in Algorithm 1** — GPT acknowledges derivation but wants notation table updated (still listed as 0.908)
4. **Feasibility vocabulary** — "Two-layer" used consistently; Claude agrees but GPT now pushes for 3 explicit layers
5. **GE sensitivity elevated** — Claude CK #4 (GE empirical grounding) no longer top-level major; GPT CK #7 (GE as primary) resolved
6. **Stress-case labeled synthetic bound** — Claude: "well-motivated addition"; GPT: "right framing" but still over-emphasized
7. **Campaign duty factor d** — All three acknowledge improvement; GPT wants reverse-derived example
8. **DES/slot-sim scope distinction** — Tool scope sentence ("two address different failure modes") acknowledged

## Major Issues Remaining

### Priority 1: Workload Justification Table (GPT #1)
Link each message type and size to a concrete coordination function (formation control, fault response, station-keeping) with citations. Add reverse-derived d example: given X maneuvers/day and Y parameters per maneuver, derive d and S_cmd. Elevate ON/OFF and cluster-correlated duty models to co-equal defaults.

### Priority 2: Stress-Case Presentation Order (GPT #2, Claude #4)
Lead with nominal/event results; stress-case as bounding envelope. Add η(d) figure with annotated mission phases. When stating "TDMA required," qualify: for high-utilization regime only. Move 46% from Table II prominence; add d=0.10 row or footnote.

### Priority 3: γ Consistency Audit (GPT #3)
Add explicit "Model C used for all feasibility claims" compliance note. Ensure all η_total/γ ratios, rate ladders, and feasibility tables use γ(R_PHY) function consistently. Annotate each table/figure with the γ model used.

### Priority 4: DES Presentation Compression (GPT #5, Claude #1)
Reduce mean-matching to one V&V paragraph. Expand distributional results: P95/P99 ingress bytes, overflow probability vs buffer size across Bernoulli/ON-OFF/cluster-correlated models. Move detailed agreement to repository.

### Priority 5: Validation Roadmap (Claude #2)
Add subsection specifying: (a) what ISL channel measurements are needed (p_BG, p_B, coherence statistics for 2-3 mechanisms); (b) what NS-3 simulation would test (MAC contention, antenna scheduling, multi-cluster interference); (c) quantitative acceptance criteria (e.g., if measured γ differs >10% from Eq. 12, rate ladder shifts one step).

### Priority 6: Packet-Level Retitling (GPT #6, Claude #3)
Rename Section IV-J to "Physical-Layer Parameter Anchoring." Add: "This derivation validates the γ parameter value, not the sizing equations that consume it."

### Priority 7: ARQ Retransmission Policy Specification (GPT #7)
Specify: ACK/NACK timing, number and placement of retransmission slots, whether retransmissions preempt egress, selective repeat vs go-back-N. Add sensitivity: miss rate vs ARQ budget fraction. Consider "no intra-cycle ARQ + prioritized inter-cycle recovery" alternative.

### Priority 8: α_RX Notation Table Fix (GPT #8, Claude minor #2)
Mark α_RX as "derived from schedule" in notation table. Remove specific numeric value (0.908). Provide general expression under superframe structure.

### Priority 9: CSMA Claim Softening (GPT #9)
Rephrase "CSMA suffices" to "airtime budget is non-binding under assumed traffic; contention performance not evaluated."

### Priority 10: 1 kbps Constraint Justification (Gemini #1)
In Introduction/System Model, explicitly argue: coordination architecture sized for lowest common denominator (survival mode) to ensure architectural invariance across failure modes. Make this the central argument.

### Priority 11: Oscillator Drift Sensitivity (Gemini #2)
Brief sensitivity: GNSS denial duration impact on T_guard. If drift exceeds 4.7 ms guard, how quickly does γ degrade?

### Priority 12: Layer Vocabulary (GPT #4 vs Claude #5)
GPT wants 3 explicit layers (info bytes → γ mapping → TDMA schedulability). Claude wants consistent 2 layers. Resolution: keep 2 layers but add explicit "do not double count" note with η/γ mapping as an intermediate step, not a layer.

## Minor Issues (22 total)

### Gemini (3 minor)
1. d vs q interaction: clarify d gates generation, q dictates transmission cost
2. Fig 6: add horizontal line at γ ≈ 0.75 feasibility boundary
3. Typos: "binding bottleneck" clarify if RF-backup-only; symbol consistency η₀, η_cmd

### GPT (8 minor)
1. "1 kbps design point" → consistently say "1 kbps per-node information budget within a 30-35 kbps shared PHY"
2. Eq. 54 units: 10⁻³ factor error-prone; provide unit-checked version
3. Table II AoI invariance: add explanation that AoI dominated by sampling policy
4. Global-state mesh: show 73 MB intermediate assumptions (rounds × payload × fanout)
5. Static topology: add one quantified worst-case transient example
6. Acquisition wording: tighten "assumed" vs "standard-derived" vs "hardware-typical"
7. Figure file extensions: ensure consistent .pdf inclusion
8. Baseline 20.5%: add η_total in more tables/plots

### Claude (11 minor)
1. Eq. 12 units: 10⁻³ conversion error-prone; dimensional analysis note
2. α_RX in Table I: mark as derived
3. Section III-B-2: justify 512 B aggregation sufficiency for 100 nodes
4. GE parameter table: state steady-state availability π_G = 0.909 explicitly
5. Fig. 4: add 1-2 more DES validation points (p_BG = 0.30, 0.70)
6. Algorithm 1 line 10: reference specific equation for L_cmd
7. Power model (5W/15-20W): either develop or remove
8. Eq. forward reference: fix text flow for γ_derived
9. Reference [1]: remove non-archival "Jonathan's Space Report"
10. Table X: rename "Pkt-γ" to "CCSDS γ anchoring"
11. Section V-B: clarify "correlated modes" means spatial correlation

## Progress Trajectory

| Version | Gemini | GPT | Claude |
|---------|--------|-----|--------|
| CJ | Accept w/ Minor (3M/4m) | Major (7M/8m) | Major (5M/12m) |
| CK | Accept w/ Minor (3M/5m) | Major (7M/7m) | Major (5M/13m) |
| CL | **Accept w/ Minor (2M/3m)** | **Major (9M/8m)** | **Major (5M/11m)** |

**Assessment:** Gemini improved (fewer issues). Claude minor count decreased. GPT major count increased from 7→9, but 2 CK majors resolved (acquisition modeling, GE as primary) and 4 new majors emerged (workload justification, γ audit, ARQ spec, CSMA claim). The core framework is accepted by all; the path to Accept is: (1) workload justification with citations, (2) stress-case de-emphasis in presentation order, (3) γ consistency audit annotations, (4) DES compression + distributional expansion, (5) validation roadmap, (6) ARQ policy specification, (7) α_RX notation fix, (8) CSMA claim softening, (9) 1 kbps central argument, (10) layer vocabulary "do not double count" note.

## Recommended Next Steps for CM

1. **Add workload justification table**: message type → coordination function → size → citation
2. **Reorder results**: nominal/event first, stress-case as envelope; add d=0.10 to Table II
3. **γ audit annotations**: add "Model C" label to each feasibility table/figure
4. **Compress DES mean-matching**: one paragraph; expand distributional tail metrics
5. **Add validation roadmap subsection**: ISL measurements needed, NS-3 scope, acceptance criteria
6. **Retitle Section IV-J**: "Physical-Layer Parameter Anchoring"
7. **Specify ARQ retransmission policy**: ACK timing, slot placement, sensitivity
8. **Fix α_RX in notation table**: mark "derived"; remove specific value
9. **Soften CSMA claim**: "airtime non-binding" not "CSMA suffices"
10. **Strengthen 1 kbps argument**: survival-mode sizing as architectural invariance
11. **Add oscillator drift calculation**: GNSS denial → T_guard impact
12. **Add "do not double count" note**: η/γ mapping is intermediate, not a layer
