---
paper: "02-swarm-coordination-scaling"
version: "bg"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---



# Peer Review: "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"

**Manuscript Version:** BG
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap: the absence of closed-form sizing equations for hierarchical coordination architectures at the $10^3$–$10^5$ node scale with byte-level traffic accounting. The authors correctly identify that swarm robotics literature operates at 10–100 agents, constellation management at ~$10^4$, and networking literature treats routing but not coordination overhead. The "practitioner toolkit" framing—providing design equations that scale linearly with bandwidth—is a useful contribution concept.

However, the novelty is more limited than presented. The core analytical results are relatively straightforward applications of queueing theory (M/D/1, M/D/c), geometric distributions for AoI under exception reporting (Eq. 12), and two-state Markov chains for Gilbert-Elliott recovery. None of these individual derivations is new; the contribution is their assembly into a coherent sizing framework for a specific architecture. This is valuable engineering work, but the paper occasionally overstates its novelty—e.g., the claim "to our knowledge, no prior work provides closed-form parametric sizing relationships" (Section I-A) is strong given that CCSDS link budgets and standard telecom sizing exercises routinely perform similar accounting at different abstraction levels. The distinction should be more precisely drawn: it is the *combination* of hierarchical coordination topology, byte-level accounting, and parametric scaling across 3 orders of magnitude that is novel, not the individual techniques.

The central finding—that architecture-specific overhead is only ~5% and commands dominate—is interesting but somewhat anticlimactic: it essentially says that the coordination *topology* doesn't matter much because the *payload* (commands) dominates. This is a useful result but limits the paper's impact as an architecture comparison.

---

## 2. Methodological Soundness

**Rating: 3 (Adequate)**

The methodology has a fundamental circularity that needs to be addressed more directly. The DES and the closed-form equations operate at the *same* message-layer abstraction—the DES is essentially a programmatic re-implementation of the same byte-counting arithmetic. The <0.1% agreement (Table VI) is therefore expected by construction, not a meaningful validation. The authors acknowledge this ("checks implementation consistency," Section I-C and Section III-A), but the paper's structure and rhetoric sometimes blur the line between verification (internal consistency) and validation (correspondence to reality). The abstract's phrasing "An open-source Monte Carlo tool verifies implementation consistency to <0.1%" is appropriately hedged, but statements elsewhere are less careful.

The Gilbert-Elliott model is well-handled analytically, and the inter-cycle recovery analysis (Section IV-C) with its parametric design curves (Fig. 5) is the strongest methodological contribution. The physical mapping of GE parameters to three LEO obstruction mechanisms (structural shadowing, antenna mispointing, Earth occultation) is helpful for practitioners. However, the per-cycle coherence assumption—GE state constant within $T_c = 10$~s—is a strong simplification. The authors argue it is conservative for recovery (shorter coherence would help) but do not address the case where coherence time is *much longer* than $T_c$ (e.g., Earth occultation at ~35 min), where the per-cycle transition model with $p_{BG} = 0.005$ becomes a poor approximation of a deterministic outage of known duration. A deterministic-outage overlay model would be more appropriate for occultation.

The Monte Carlo configuration (30 replications) is adequate for mean estimation but marginal for tail statistics. The P99 AoI values are computed as means of per-run P99s (Table IV footnote), which is methodologically sound, but the confidence intervals are not reported for all tail metrics. The claim of SD < 0.001% for overhead is credible given the deterministic nature of the byte counting, but the tail statistics (P95 recovery, P99 AoI) deserve explicit CI reporting throughout.

The sectorized mesh comparison (Section III-B.4) has a significant methodological issue: the capped-fanout variant (cap = 10) provides fundamentally different functionality (3.2% sector coverage) than the hierarchy (100% cluster awareness). Table VIII acknowledges this, but the overhead comparison in Table VII and throughout the paper still implicitly treats them as alternatives, which is misleading. The "1.35–1.95× higher" overhead claim for the sectorized mesh is not an apples-to-apples comparison.

---

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The analytical derivations are internally consistent and the cross-checks are thorough. The AoI geometric model (Eq. 12) matches the DES to within 1 second (441 vs. 440 s), and the Markov recovery CDF matches the DES (Fig. 5a). The TDMA frame budget (Table III) is carefully itemized with 623 ms margin, and the ingress/egress feasibility constraints (Eqs. 8–9) correctly identify that intra-cycle retransmission is infeasible at $k_c = 100$ under 24 kbps half-duplex.

However, several logical issues warrant attention:

**The 1 kbps design point.** The paper devotes enormous effort to analyzing the 1 kbps regime, then acknowledges (Table I, Section III-E) that "at ≥10 kbps, the coordinator bottleneck and TDMA requirement vanish" and the equations become "operationally unnecessary." The 1 kbps is justified as "S-band RF backup during optical ISL outages (<1% of operational time)." This raises the question: why is the entire paper organized around a regime that applies <1% of the time? The bandwidth-scaling table (Table I) should be promoted earlier and the paper should more clearly frame the 1 kbps analysis as a worst-case bound rather than the primary operating point.

**The stress-case unicast problem.** The 22-cycle staggering requirement for per-node unicast commands (Eq. 7, Table V) is a significant operational limitation that is somewhat buried. If every node needs a unique command every cycle, the system cannot deliver it—this is not just a scheduling inconvenience but a fundamental capacity shortfall. The paper should discuss what mission scenarios actually require per-node unicast at every cycle and whether the 22-cycle latency is operationally acceptable.

**Joint independence claim.** The pipeline decoupling result (Section IV-D, Table V) showing identical drops under "No Loss" and "GE Only" is presented as a DES contribution, but it follows trivially from the dedicated-link assumption: if lost packets never reach the queue, queue behavior is independent of loss. The paper acknowledges this ("Under dedicated links... GE losses and coordinator queue occupancy are independent") but still presents it as a finding requiring DES verification. The more interesting result—that this decoupling breaks under shared-medium contention—is mentioned only in passing.

**Coordinator failure analysis.** The coordinator failure transient (Section III-B.2) estimates ~60 s RF-backup recovery, affecting ~100 nodes. At 2%/yr failure rate with 1,000 clusters, this gives ~20 failures/yr fleet-wide. However, the analysis assumes independent failures. Correlated failures (solar particle events, batch manufacturing defects) could simultaneously affect multiple coordinators—this is listed as a limitation but deserves quantitative bounding.

---

## 4. Clarity & Structure

**Rating: 3 (Adequate)**

The paper is dense but generally well-organized. The roadmap at the beginning of Section IV is helpful, and the design equations summary (Section V-C) provides a useful practitioner reference. The notation table (Table I) is appreciated.

However, the paper suffers from several clarity issues:

**Length and repetition.** The manuscript is extremely long for a journal paper (~12,000 words of body text plus extensive tables). Key results are stated in the abstract, restated in the introduction, restated in the contributions list, and then derived in the results section. The overhead value η ≈ 46% appears at least 15 times. Significant compression is possible without loss of content—particularly in Sections III-B (topology models) and IV-F (verification), where the message is simple (O(N) scaling, <0.1% agreement) but the exposition is lengthy.

**Notation overload.** The paper uses η, η_E, η_S, η_total, η_eff, η_0, η_sector, η_sync, and η with various subscripts. While each is defined, the proliferation makes it difficult to track which overhead metric is being discussed at any given point. A consolidated notation table distinguishing these variants would help.

**Figure quality.** All figures are referenced but provided as PDF placeholders (fig-*.pdf). Without seeing the actual figures, I cannot assess their quality, but the captions are generally informative. The paper would benefit from a single summary figure combining the key design curves (overhead vs. N, AoI vs. p_exc, recovery vs. p_BG) into a compact multi-panel format.

**The "Version BG" designation** in the title metadata and abstract is unusual and should be removed for publication. The acknowledgment of AI tools (Claude 4.6, Gemini 3 Pro, GPT-5.2) with model version numbers that do not exist as of my knowledge raises questions about the provenance of this work.

---

## 5. Ethical Compliance

**Rating: 4 (Good)**

The paper includes an explicit acknowledgment of AI-assisted ideation (Acknowledgment section), which is commendable and increasingly expected. The disclosure is appropriately scoped: "motivated aspects of the coordinator architecture but is not validated here." The reference to a methodology paper [43] on multi-model AI deliberation provides traceability.

The anonymous authorship ("Project Dyson Research Team") with a note that "Individual author names and affiliations will be provided for final publication per IEEE policy" is acceptable for review but must be resolved before publication. IEEE requires named authors who can certify the work.

The open-source data availability statement with a specific repository tag (paper-02-v-bg) and complete environment specification (Python 3.12, NumPy 2.x, etc.) is excellent practice and supports reproducibility.

One concern: the AI model version numbers cited (Claude 4.6, Gemini 3 Pro, GPT-5.2) do not correspond to any publicly released models as of my knowledge cutoff. If these are speculative or fictional version numbers, this should be corrected to reflect actual tools used.

---

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in scope, addressing autonomous spacecraft coordination at scale. The reference list (52 items) covers the relevant domains: constellation operations, swarm robotics, distributed systems, queueing theory, and space communications standards.

However, several referencing gaps exist:

**Missing key references.** The paper does not cite recent work on autonomous constellation management that is directly relevant: (1) Legge et al.'s work on distributed space systems architectures; (2) the extensive literature on satellite cluster flight and formation flying coordination (e.g., Scharf et al., "A survey of spacecraft formation flying guidance and control"); (3) recent work on LEO mega-constellation collision avoidance automation (e.g., Merz et al. at ESA). The CCSDS Proximity-1 reference [35] is appropriate for the TDMA frame model but the paper should also cite CCSDS 401.0 (RF and modulation) for the link budget context.

**Non-archival sources.** Several references are non-archival (SpaceX FCC filings, Amazon web pages, DARPA program pages, DoD fact sheets). While some are unavoidable for current operational systems, the paper should minimize reliance on these and note their non-archival status more consistently. Reference [1] includes "Jonathan's Space Report" as a secondary source with appropriate caveats.

**Self-citation.** Reference [43] (Project Dyson multi-model AI paper) is cited but appears to be an unpublished working paper at a project URL. This should be clearly marked as a preprint or working paper, and the paper should not depend on it for any critical claims.

**Age of references.** The core distributed systems references (Lamport 1978, Kleinrock 1975, Demers 1987) are classics and appropriate. However, the swarm robotics and multi-agent sections could benefit from more recent references (2022–2025) on large-scale multi-robot coordination.

---

## Major Issues

1. **Validation gap is too large for the claims made.** The paper's central deliverable—"closed-form sizing equations"—is verified only against a DES that implements the same message-layer abstraction. No physical-layer, packet-level, or hardware-in-the-loop validation exists. While the authors acknowledge this (Section V-A), the paper's title ("Design Equations") and framing imply a level of engineering readiness that is not yet justified. The equations are *hypotheses* about what matters at the message layer, not validated design tools. **Recommendation:** Either (a) include at least a single-cluster NS-3 simulation to bridge the abstraction gap, or (b) significantly temper the claims, changing "design equations" to "preliminary sizing estimates" or similar, and restructuring the abstract and conclusion to foreground the validation gap.

2. **The sectorized mesh comparison is not apples-to-apples.** The hierarchical architecture provides full cluster awareness (100% of $k_c$ peers) while the capped sectorized mesh provides 3.2% sector coverage. Comparing their overheads (46% vs. 65%) without normalizing for functional scope is misleading. Table VIII helps but is insufficient—the overhead comparison should either (a) be restricted to architectures with equivalent functionality, or (b) include a normalized metric (e.g., overhead per peer monitored). **Recommendation:** Add a "cost per peer" metric: hierarchical monitors 100 peers at 46% overhead (0.46%/peer); sectorized monitors 10 peers at 65% overhead (6.5%/peer). This would actually *strengthen* the hierarchical case.

3. **The 1 kbps design point dominates the paper but applies <1% of operational time.** The paper should be restructured to present the bandwidth-parametric results (Table I) as the primary contribution, with the 1 kbps analysis as the constraining worst case. Currently, a reader must reach Section III-E to learn that the coordinator bottleneck "vanishes" at ≥10 kbps. **Recommendation:** Lead with the parametric scaling and present 1 kbps as the design-driving edge case, not the default.

4. **The GE model is inappropriate for Earth occultation.** At $p_{BG} = 0.005$ (occultation regime), the per-cycle Markov model poorly approximates a deterministic outage of ~35 minutes. The geometric recovery distribution will have heavy tails that do not match the sharp recovery when the satellite exits Earth's shadow. **Recommendation:** Add a deterministic-outage model for the occultation case and restrict the GE model to stochastic obstructions (shadowing, mispointing).

---

## Minor Issues

1. **Eq. 2 (M/D/1 waiting time):** The standard Pollaczek-Khinchine formula for M/D/1 is $W_q = \rho / (2\mu_s(1-\rho))$, which is correct as written, but the paper should note this is the *mean* waiting time and clarify units (seconds).

2. **Table II (Simulation Parameters):** The collision avoidance rate footnote references "see text" but the text discussion ($10^{-4}$/node/s) appears only later. Cross-reference the specific section.

3. **Section III-B.2:** "Coordinator rotation: state transfer (10–50 MB) over optical ISL (80–400 ms), excluded from η." The 80 ms figure implies 10 MB / 1 Gbps = 80 ms, but 50 MB / 1 Gbps = 400 ms. This should be stated explicitly rather than leaving the reader to infer the calculation.

4. **Eq. 7 (unicast stagger):** The denominator uses $\alpha_{RX}$ which is defined implicitly but never given a numerical value. From Table III, $\alpha_{RX} \approx 9177/10000 = 0.918$, giving $1 - \alpha_{RX} = 0.082$, and $16.9/0.082 \approx 206$, not 22. The calculation appears to use $1 - \alpha_{RX} = 0.8$ (800 ms), which corresponds to the "remaining ~0.8 s" mentioned earlier. Clarify: is $\alpha_{RX}$ the fraction of $T_c$ or the absolute time? The inconsistency between 623 ms margin (Table III) and 800 ms (Eq. 7) needs resolution.

5. **Table IV (AoI results):** The periodic baseline shows Mean AoI = 4.9 s, but under perfect periodic reporting at $T_c = 10$ s, the theoretical mean AoI is $T_c/2 + s_{proc}/2 = 5.0025$ s. The 4.9 s value suggests a slight modeling artifact; explain or correct.

6. **Section IV-A:** "Model A (hard per-cycle deadline, no carry-over) requires 50 kbps under random-phase arrivals; Model B (token-bucket, 25 kB depth) requires 21 kbps." These models are referenced but never formally defined. Either define them or remove the references.

7. **Bibliography:** Reference [1] cites an FCC filing from March 2023 but notes "accessed Feb. 2026." If this paper is being submitted in 2025, the access date is in the future. Correct to the actual access date.

8. **Abstract:** "Gilbert-Elliott inter-cycle recovery P95 in 4 cycles" should specify "at $p_{BG} = 0.50$" for completeness, as this is highly parameter-dependent.

9. **Section III-B.4:** The $\sqrt{N}$ sector sizing heuristic ("conjunction screening volume contains $O(\sqrt{N})$ nodes when the screening radius scales with mean nearest-neighbor distance") needs a derivation or reference. This is not obvious for arbitrary orbital distributions.

10. **Table VI:** "η_DES = 46.0% at all 8 intermediate sizes (5k–80k); omitted for brevity" — this is fine but the italic formatting within the table is awkward. Consider a footnote instead.

---

## Overall Recommendation

**Major Revision**

The paper addresses a real engineering need—parametric sizing tools for large autonomous space swarms—and provides a coherent analytical framework with careful internal consistency checks. The Gilbert-Elliott recovery analysis and parametric design curves are genuinely useful contributions. However, the paper has four significant issues that prevent acceptance in its current form: (1) the validation gap between message-layer analysis and physical reality is too large for the "design equations" framing; (2) the topology comparison is not functionally normalized; (3) the paper is organized around a regime (1 kbps) that applies <1% of operational time; and (4) the GE model is misapplied to deterministic outages. Additionally, the paper is substantially too long and repetitive. A major revision addressing these structural issues, adding at minimum a packet-level single-cluster validation, and compressing the presentation by ~30% would produce a strong contribution suitable for T-AES.

---

## Constructive Suggestions

1. **Add a packet-level validation for one cluster.** An NS-3 simulation of a single 100-node cluster under TDMA with realistic PHY (including synchronization, guard times, and half-duplex constraints) would bridge the most critical validation gap. The complete superframe budget in Table III provides the specification. Even showing that the message-layer predictions hold within 10% at the packet level would dramatically strengthen the paper.

2. **Restructure around bandwidth-parametric results.** Make Table I the organizing framework. Present the design equations as functions of $C_{node}$, show that at ≥10 kbps most constraints vanish, and then deep-dive into the 1 kbps worst case. This reframing would make the paper more useful to practitioners who may operate at various bandwidth points.

3. **Introduce a "cost per function" normalization.** Define overhead-per-peer-monitored or overhead-per-bit-of-awareness as a normalized comparison metric. This would make the hierarchical vs. sectorized mesh comparison fair and would likely strengthen the paper's case for hierarchical coordination.

4. **Add a deterministic-outage model for Earth occultation.** The GE model is excellent for stochastic obstructions but inappropriate for predictable geometric outages. A simple model where occultation duration is computed from orbital geometry, with the GE model handling residual stochastic losses during the visible arc, would be more physically meaningful and would differentiate the paper from generic channel-modeling work.

5. **Compress by ~30%.** The paper can be significantly shortened by: (a) removing repetitive restatements of η ≈ 46%; (b) consolidating the topology model descriptions (Section III-B) into a single table with a brief narrative; (c) moving the detailed TDMA frame analysis to an appendix; and (d) eliminating the global-state mesh, which serves only as a trivially infeasible upper bound and adds little insight. Target 8,000–9,000 words of body text.