# Version CM Review Summary

## Recommendations

| Reviewer | Recommendation | Change from CL |
|----------|---------------|----------------|
| Gemini 3 Pro | **Accept with Minor Revisions** | Maintained (3M/4m vs 2M/3m) |
| GPT-5.2 | **Major Revision** | Improved (8M/7m vs 9M/8m) |
| Claude Opus 4.6 | **Major Revision** | Maintained (5M/12m vs 5M/11m) |

## What CM Fixed (Acknowledged by Reviewers)

1. **Workload justification** — GPT: "message size breakdown is appropriate"; message sizes now traceable to CCSDS SPP and SMAD
2. **Campaign duty factor d** — All three acknowledge d=0.10 routine row and reverse-derived d=0.0016; GPT still wants formal derivation method
3. **γ consistency audit** — GPT: "you correctly replace the earlier optimistic γ"; footnote c added; but Model S still appears in some plots
4. **Validation roadmap** — Claude: "validation gaps acknowledged"; Gemini: "strong reproducibility posture"; DVB-RCS2 anchoring noted
5. **Physical-Layer Parameter Anchoring retitle** — Claude: "correctly characterized as parameter anchoring"; GPT: "you mostly do this correctly"
6. **ARQ retransmission policy** — GPT acknowledges stop-and-wait, ACK mini-slot, M_r slots; wants more formal schedule
7. **α_RX notation fix** — GPT: "acknowledges derivation"; wants notation table fully updated
8. **CSMA claim softened** — No longer a top issue for any reviewer
9. **1 kbps architectural invariance** — Gemini: "1 kbps constraint is well-motivated"
10. **Oscillator drift** — Not mentioned negatively; absorbed
11. **Double-counting note** — GPT: "the 'do not double-count' paragraph is particularly helpful"
12. **Stress-case d=0.10 row** — GPT: "clear improvement versus static 'always-stress' interpretation"

## Major Issues Remaining

### Priority 1: Two-Layer Framework Canonical Definition (GPT #1)
The abstract/intro say "two-layer framework" but later text says "three-tier decomposition" (baseline/architecture/workload). Some readers interpret η_total/γ as a third layer. Add a single canonical boxed definition: (i) baseline vs η decomposition is accounting, not a feasibility layer; (ii) feasibility layers are exactly two: bytes and airtime; (iii) η_total/γ is only a screening heuristic. Ensure abstract matches.

### Priority 2: Duty Factor d Formal Derivation (GPT #2)
The 60× gap between reverse-derived d=0.0016 and conservative default d=0.10 undermines the "routine η≈5-10%" claim. Provide: (a) table of d computed from ESA ~10 maneuvers/spacecraft/yr with explicit assumptions; (b) sensitivity of η and P99 buffer to d∈[10⁻⁴, 10⁻¹]; (c) clarify if d is for peak design within an outage window vs annual average.

### Priority 3: Model C Enforcement / Model S Relegation (GPT #3, Claude minor #1)
Model S still appears in figure captions and some tables alongside Model C. Risk: readers cherry-pick optimistic bound. Every recommendation-supporting figure/table must have explicit "Model C" label. Consider moving Model S to appendix or single "optimistic bound" subsection.

### Priority 4: Ingress vs Egress Separation (GPT #4)
Stress-case language conflates coordinator ingress (status traffic, independent of d) with command egress (dependent on d). Safety-critical "100% deadline misses" is about ingress feasibility, not stress-case commands. Add a simple dependency diagram: what depends on d, what depends on k_c, what depends on γ.

### Priority 5: Formal Superframe Schedule (GPT #5, Claude #4)
α_RX derivation needs a rigorous schedule specification. Unclear how α_RX changes with added control slots, retransmission pools, or unicast fraction q. Provide: (a) formal superframe definition with ordered segments; (b) closed-form α_RX as function of k_c, M_r, control-plane options; (c) margins under at least two schedule variants.

### Priority 6: DES Presentation — Tail Model Contingency (GPT #6, Claude #1)
DES confirms its own equations (acknowledged). Incremental value is tail/buffer sizing under campaign correlation, but results are model-contingent. Either: (a) add one structurally different arrival model (heavy-tailed ON, Hawkes/self-exciting); or (b) explicitly scope tail guidance as "valid for geometric ON/OFF with these parameters."

### Priority 7: Narrow Binding Regime (Claude #3)
TDMA schedulability analysis binding only at 1 kbps (<1% of operational lifetime). At ≥10 kbps everything trivially feasible. Either: (a) reframe around the RF-backup/deep-space regime where analysis is binding; or (b) extend to more demanding scenarios (larger k_c, shorter T_c, multi-hop).

### Priority 8: MAC Contention Analysis (Claude #4)
No contention analysis despite recommending specific PHY rates for safety-critical coordination. The 730 ms margin at 30 kbps could be consumed by slot collisions from clock drift, hidden terminals, multi-cluster interference. At minimum: sensitivity showing how many slot collisions the margin absorbs.

### Priority 9: GE Empirical Grounding (Claude #5, Gemini #1)
p_BG=0.50 described as "illustrative" with no ISL measurements. "Actual P95 recovery could be ~3× higher or lower." State in abstract/conclusion that p_BG=0.50 is a design assumption. Cite any available ISL data (EDRS, LCRD, Mars relay). Present recommendation as conditional on GE parameters.

### Priority 10: Promote Time-Domain γ (GPT #8, Claude minor #3)
Eq. γ_general mixes bits and ms·bps—error-prone. Make time-domain form (Eq. γ_time) the primary equation; demote dimensional form to appendix or alternate. Provide pseudocode function for γ computation with units.

### Priority 11: Thundering Herd Backoff Parameters (Gemini #2)
100 nodes reacting simultaneously to coordinator timeout. Slotted ALOHA collapses under G>1. Specify initial backoff window size. Verify if 160s estimate accounts for collision storm or assumes steady-state.

### Priority 12: Unicast Latency Operational Concept (Gemini #3)
190s unicast stagger may be unacceptable for collision avoidance. Expand which commands are acceptable at 190s (orbit raising, software updates) vs which must use broadcast (safety-critical alerts).

### Priority 13: Packet-Level Validation Language (GPT #7, Claude #2)
"Cross-model consistency" and "packet-level TDMA simulator" read like framework validation. Only genuinely emergent finding is ARQ×TDMA coupling (52.7% misses). Tighten to: "standards-based framing + assumed acquisition/guard model."

## Minor Issues (23 total)

### Gemini (4 minor)
1. q definition: clarify 10% of nodes receive unicast or 10% of commands are unicast
2. Regional ingress: brief sentence why not capacity-constrained
3. Fig 5 markers: ensure star/diamond visible in print
4. Algorithm 1: replace hardcoded 0.205 with η_baseline reference

### GPT (7 minor)
1. Terminology: "RF-backup channel (1 kbps)" vs "S-band coordination channel (35 kbps)" — consistently call 1 kbps an allocation, 30-35 kbps a cluster PHY
2. Table bandwidth_scaling: add PHY equivalent to prevent mixing info-rate and PHY-rate
3. Table superframe: no explicit ACK mini-slot overhead line item
4. GE parameter mapping: state explicitly it's first-order for geometric burst lengths
5. AoI p_exc caveat: move to first paragraph of AoI section; rename p_exc to p_rep
6. Reference hygiene: non-archival web pages shouldn't support parameter claims
7. Eq. γ_general: provide range for T_acq and show how γ and 30/35 kbps move

### Claude (12 minor)
1. Inconsistent γ subscripting: γ₂₄, γ₃₀, γ_C,24, γ_C,30, γ_S, unsubscripted γ
2. Table I notation density: split primary/derived; forward references
3. Eq. 13 unit conversion: 10⁻³ error-prone; present only Eq. 14 in main text
4. "Project Dyson Research Team" authorship: IEEE requires individual names
5. Non-archival references: [3] Kuiper, [18] DARPA OFFSET, [19] DoD Replicator, [22] Blackjack
6. Fig. 1 not evaluable from LaTeX source
7. Section III-B-2: coordinator self-exclusion footnote should be main text
8. "Stress-case" terminology: standardize stress-case vs stress case vs stress bound
9. Algorithm 1 line 2: hardcoded 0.205 should reference baseline definition
10. Table II AoI column: footnote about AoI independence should be more prominent
11. Deep-space applicability claim unsupported (LEO parameterization)
12. Eq. 6 N_R undefined (presumably Raft rounds)

## Progress Trajectory

| Version | Gemini | GPT | Claude |
|---------|--------|-----|--------|
| CJ | Accept w/ Minor (3M/4m) | Major (7M/8m) | Major (5M/12m) |
| CK | Accept w/ Minor (3M/5m) | Major (7M/7m) | Major (5M/13m) |
| CL | Accept w/ Minor (2M/3m) | Major (9M/8m) | Major (5M/11m) |
| CM | **Accept w/ Minor (3M/4m)** | **Major (8M/7m)** | **Major (5M/12m)** |

**Assessment:** Gemini stable at Accept w/ Minor. GPT improved 9→8 major (workload justification, CSMA softening, retitle addressed). Claude stable at 5 major. The three reviewers converge on similar persistent gaps: (1) GPT/Claude both want formal schedule specification; (2) GPT/Claude both want DES tail claims scoped; (3) Claude wants contention analysis or margin quantification; (4) GPT wants Model C enforced everywhere; (5) all three want GE stated as design assumption.

**Key insight for CN:** Many GPT and Claude issues overlap. Addressing 5-6 items can resolve multiple reviewer concerns simultaneously:
- Formal superframe → fixes GPT #5, Claude #4 (MAC contention margin), partial Claude #3 (binding regime)
- Model C enforcement → fixes GPT #3, Claude minor #1
- DES tail scoping → fixes GPT #6, Claude #1
- d sensitivity table → fixes GPT #2
- Two-layer boxed definition → fixes GPT #1, GPT #4 (ingress/egress separation)

## Recommended Next Steps for CN

1. **Add boxed two-layer definition** with ingress/egress dependency: what depends on d, k_c, γ
2. **Add d sensitivity table**: d ∈ {0.001, 0.01, 0.05, 0.10} → η, P99 buffer, margin
3. **Enforce Model C**: add "Model C" label to every feasibility table/figure; move Model S to single paragraph
4. **Formal superframe specification**: segment order, slot counts, closed-form α_RX(k_c, M_r, q)
5. **Contention margin calculation**: how many slot collisions 730 ms absorbs at 30/35 kbps
6. **Scope DES tail claims**: add explicit "valid for geometric ON/OFF" qualifier
7. **Promote Eq. γ_time as primary**: demote Eq. γ_general to "alternate form"
8. **Conditional PHY recommendation table**: if γ ∈ [0.65,0.70] → 40 kbps; [0.70,0.80] → 35 kbps; [0.80,0.90] → 30 kbps
9. **State GE p_BG as design assumption** in abstract and conclusion
10. **Thundering herd backoff params**: specify window size, verify collision storm accounting
11. **Unicast latency acceptability**: broadcast for safety-critical, unicast for non-urgent
12. **Remove deep-space applicability claim** (unsupported by LEO parameterization)
13. **Fix N_R undefined** in Eq. 6
14. **Standardize stress-case terminology**
