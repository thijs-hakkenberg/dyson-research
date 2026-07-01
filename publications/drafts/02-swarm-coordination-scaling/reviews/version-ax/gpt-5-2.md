---
paper: "02-swarm-coordination-scaling"
version: "ax"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-27"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 4/5**

The manuscript tackles an important and timely problem: how to *dimension* coordination/command-and-control messaging for very large autonomous space swarms (10³–10⁵, with discussion toward 10⁶) under severe “RF-backup” bandwidth constraints. The focus on **byte-level accounting** and producing **closed-form sizing equations** (coordinator ingress, AoI tails under exception telemetry, correlated-loss recovery) is practically valuable and relatively uncommon in the aerospace swarm/constellation literature, which often stays at higher architectural levels or focuses on routing rather than coordination traffic budgets.

The strongest novelty claim is not a new protocol per se, but a **synthesis**: translating coordination mechanisms (summaries/heartbeats/election/commands) into parametric design equations and validating those equations via a fast Monte Carlo DES. For practitioners, the coordinator-ingress sizing (21–25 kbps under TDMA framing assumptions) and the explicit separation between topology-invariant baseline telemetry vs. protocol overhead are useful “engineering handles.”

That said, the novelty framing occasionally overreaches (e.g., “No prior work has systematically compared … using byte-level traffic accounting…”). There is relevant work in constellation networking, DTN operations, and large-scale distributed systems sizing that could partially overlap in spirit even if not in this exact regime. The paper would benefit from tightening the novelty statement to “to our knowledge, no prior open literature provides…” and explicitly delineating what is new versus what is assembled from known results.

---

## 2. Methodological Soundness — **Rating: 3/5**

The paper is methodologically careful in *some* respects: assumptions are often stated explicitly (message sizes, cycle time, coordinator processing time, GE coherence per cycle), and the authors correctly emphasize that the DES is for **verification, not physical-layer validation** (Section III-A; Section V-A). The analytic cross-checks are a strength: AoI P99 under geometric exception reporting (Eq. 23) matches DES; Markov-chain recovery curves are compared against DES (Section IV-C). The “per-run P99 then aggregate” approach in Table IV-B’s footnote is also a good practice to avoid pseudo-replication.

However, several modeling choices materially affect the key claims and need stronger justification and/or sensitivity analysis:
- **Coordinator ingress “token bucket” Model B** (Section IV-A) is argued to be equivalent to TDMA smoothing, but the statement “tokens accumulate during idle inter-cycle intervals, not from deferred reports” is confusing: tokens carry across cycles *by definition*, and the key question is whether the traffic can be scheduled so that arrivals are sufficiently regular to avoid deadline misses. A clearer mapping between (i) physical TDMA slotting, (ii) arrival process at the coordinator, and (iii) the token-bucket abstraction is needed to avoid the appearance of “cheating the deadline.”
- The **half-duplex constraint** is acknowledged (Section IV-A) but not integrated into the capacity sizing and overhead results. In stress-case, the coordinator egress is enormous (commands to 100 nodes per cycle) and the text suggests a “separate downlink slot allocation or dedicated subchannel.” This is not a minor implementation detail; it is a second bottleneck that can dominate feasibility in RF-backup mode. If the paper’s headline overhead numbers include commands, then the feasibility of delivering those commands over the assumed RF channel should be modeled consistently with half-duplex timing.
- The **sectorized mesh** model uses a global position oracle and capped neighbor heartbeats; this is fine as an abstraction, but it weakens the fairness of the comparison if the hierarchical case assumes TDMA-friendly structure while the mesh case implicitly assumes distributed scheduling without modeling its control overhead and contention dynamics.

Reproducibility is helped by the open-source claim and tag, but the manuscript would benefit from including (i) a short pseudo-code or algorithm block for the DES cycle update and (ii) explicit formulas for each overhead component (not just the final linear rule), so that readers can independently re-derive Table VIII/IX without running code.

---

## 3. Validity & Logic — **Rating: 3/5**

Many conclusions are directionally supported by the analysis: (i) hierarchical aggregation avoids O(N²) global-state dissemination; (ii) commands dominate stress-case bandwidth independent of topology; (iii) correlated loss bursts can make intra-cycle retransmissions ineffective under a long coherence-time GE model; and (iv) exception telemetry trades bandwidth for AoI tails in a predictable geometric manner. The manuscript is also commendably explicit about its limitations and the “verification not validation” stance.

The main validity concern is **internal consistency between the assumed RF-backup physical access model and the reported traffic feasibility**. The paper simultaneously assumes:
- per-node average budget 1 kbps,
- coordinator ingress 21–25 kbps via TDMA,
- half-duplex coordinator with ingress consuming ~9.18 s of a 10 s cycle for kc=100,
- stress-case commands of 512 B × 100 nodes per cycle (≈ 41 kbps of payload, before MAC/FEC/guards).

Under those numbers, stress-case command dissemination **cannot fit** in the remaining ~0.8 s of the cycle at 24 kbps PHY, and even if placed in another frame, it competes with ingress unless there is (a) a second RF chain, (b) orthogonal spectrum, or (c) a different time allocation that reduces ingress utilization. The paper notes this but treats it as “secondary”; for the stress-case headline (η≈46%, total utilization ≈67%), this is arguably *primary*. As written, the reader could conclude the stress-case is feasible under the RF-backup channel, when it may not be without additional assumptions.

A second logic issue is the “pipeline decoupling” claim (Section IV-D). It is correct under orthogonal links where losses occur independently before queueing, but the DES appears to enforce coordinator ingress via byte budgets and treat losses as removing messages before they reach the coordinator. In real TDMA, failed transmissions still consume slot time, so **losses do consume capacity** (time), even if they don’t increase queue occupancy. Thus, the decoupling is true for *queue saturation* but not necessarily for *cycle feasibility* under half-duplex TDMA timing. This distinction should be made explicit; otherwise the independence result may be overstated.

---

## 4. Clarity & Structure — **Rating: 4/5**

Overall organization is strong: clear RQs, contributions, a consistent definition of overhead η excluding baseline telemetry, and a results roadmap (Section IV). Tables are generally informative, and the manuscript does a good job flagging abstraction boundaries (Table 7) and caveats (e.g., centralized baseline asymmetry).

The abstract is information-dense and mostly accurate, but it verges on “results dump.” For T-AES readership, consider reducing the number of numeric claims in the abstract and emphasizing the *design equations* and key implications (e.g., coordinator ingress sizing; AoI/bandwidth trade; correlated-loss recovery curves). Also, the abstract currently mixes message-layer utilization, MAC efficiency γ, and coordinator ingress requirements in a way that can confuse non-specialists.

A few places would benefit from clearer definitions and consistency:
- The manuscript uses “drops,” “misses,” “deadline misses,” and “losses” with overlapping meaning (Section IV-A). A short taxonomy (e.g., PHY loss vs. ingress drop vs. late-arrival miss) would help.
- Equation numbering and cross-references are mostly fine, but some claims would be easier to follow if accompanied by explicit formulas (e.g., the 20.5% baseline derivation from 256 B every 10 s at 1 kbps is simple but should be shown once).

Figures are referenced appropriately, but several key feasibility arguments hinge on TDMA/half-duplex timing; a single figure showing the **cycle time budget** (ingress slots + guard + beacon + egress slots) for nominal vs stress-case would greatly improve clarity.

---

## 5. Ethical Compliance — **Rating: 4/5**

The manuscript includes an explicit disclosure of AI-assisted ideation in the Acknowledgment and clarifies that those aspects are not validated. This is aligned with emerging transparency expectations. Data/code availability is provided with a tag, which supports reproducibility.

Two minor points:
- The “Project Dyson Research Team” placeholder authorship is understandable for review, but for IEEE compliance the final submission must include author identities and affiliations; the current note is acceptable as a temporary measure but should be flagged for final.
- If the project has any organizational or funding relationships that could be perceived as conflicts (e.g., commercial constellation operators), those should be disclosed in the final version.

---

## 6. Scope & Referencing — **Rating: 4/5**

The topic fits IEEE T-AES well: spacecraft autonomy, constellation operations, and communication-constrained coordination. The paper bridges aerospace operations and distributed systems/queueing theory, which is within the journal’s remit.

Referencing is broad and generally appropriate (swarm robotics, gossip, Raft, AoI survey, constellation routing papers, CCSDS standards). However, several citations are non-archival (Amazon Kuiper overview, DARPA webpages, Project Dyson publication). While such references can be acceptable for context, key technical claims should rely more on archival sources when possible. Also, some constellation-ops claims (e.g., Starlink operational coordination details) are difficult to verify from FCC filings and non-archival sources; consider tempering those statements or supporting them with peer-reviewed/archival analyses.

The paper would also benefit from citing work on:
- **LEO contact scheduling / TT&C scaling** and spectrum constraints (more directly tied to the centralized baseline caveat),
- **TDMA/Proximity-1/space link layer** performance analyses beyond Proximity-1 spec,
- **Age-of-information under periodic + lossy channels** (beyond the geometric exception model), if the authors want to generalize AoI claims.

---

## Major Issues

1. **Stress-case feasibility under half-duplex TDMA is not modeled consistently with the headline overhead results.**  
   - Location: Section IV-A (“Half-duplex TX/RX partitioning”), Table 10/12/13 and stress-case definition in Section IV-E.  
   - Why it matters: The paper reports η≈46% including 512 B commands per node per cycle, but under the same RF-backup assumptions the coordinator has insufficient time to transmit those commands if ingress already consumes ~92% of the cycle. This is a core feasibility constraint, not an implementation detail.  
   - Required fix: Either (a) explicitly assume orthogonal command channels / second RF chain / separate spectrum and include that in the system model and overhead accounting, or (b) revise stress-case to a feasible RF-backup workload and/or compute the required PHY rate / frame partition to support it.

2. **“Pipeline decoupling” independence result is overstated without accounting for time/slot consumption by failed transmissions.**  
   - Location: Section IV-D and Table 8 discussion.  
   - Why it matters: In TDMA, a failed transmission still occupies a slot; correlated losses can reduce delivered throughput and can force additional slots if retries are scheduled, coupling loss to time budget even if not to queue occupancy.  
   - Required fix: Reframe the result as “decoupling from *queue saturation* under orthogonal links,” and add a companion analysis for “decoupling does not imply decoupling from *frame time feasibility* under half-duplex TDMA.”

3. **Coordinator ingress sizing models need clearer physical interpretation and deadline handling.**  
   - Location: Section IV-A (Model A vs Model B; “tokens accumulate during idle inter-cycle intervals”).  
   - Why it matters: The difference between 21 kbps and 50 kbps is central to the design recommendation. The mapping from random-phase arrivals to TDMA scheduling to token-bucket smoothing must be unambiguous.  
   - Required fix: Provide a single unified model: either explicitly assume TDMA slot assignment (deterministic arrivals) and size accordingly, or if random-phase is assumed, show how scheduling is achieved and what information is required (time sync, slot assignment dissemination, guard time).

4. **Centralized baseline comparison is asymmetric and could mislead despite caveats.**  
   - Location: Section III-B (M/D/c), Table 1, Section IV-G.  
   - Why it matters: The paper draws conclusions about centralized scaling (e.g., not diverging until 10⁶) but explicitly does not model the dominant constraints (spectrum, contact windows). Even with caveats, readers may over-interpret.  
   - Required fix: Either (a) add a simple comm-limited centralized uplink model (even coarse) to complement the compute queue, or (b) substantially reduce the prominence of the centralized “10⁶” claim and keep it as a limited compute-only observation.

---

## Minor Issues

- **Equation/parameter consistency:** In Eq. (20) (TDMA capacity), you use \((k_c-1)\) rather than \(k_c\). If the coordinator does not transmit ephemeris, then ingress should be \(k_c\) member reports; using \(k_c-1\) needs explanation (is one node the coordinator and not sending a report?). This choice affects the 20.5 kbps calculation slightly and should be consistent everywhere.
- **Baseline telemetry derivation:** The 20.5% baseline (204.8 bps) is correct for 256 B every 10 s, but show the computation once explicitly near the definition of η for readability.
- **Terminology:** “Zero-drop” is used for both “no buffer overflow drops” and “no deadline misses.” Consider separating “overflow drop” vs “late miss.”
- **Figure file reference:** `\includegraphics{fig-cross-cycle-recovery}` lacks an extension while others include `.pdf`. Ensure consistent compilation.
- **Sectorized mesh heuristic:** The \(\sqrt{N}\) neighbor argument (Section III-B-4) is plausible but currently hand-wavy. Either cite a screening-volume scaling reference or label it clearly as a heuristic and show sensitivity to alternative exponents/caps.
- **Non-archival references:** Several web references are acceptable for context but should not support key quantitative claims. Consider replacing/augmenting with archival sources where feasible.

---

## Overall Recommendation — **Major Revision**

The manuscript has strong potential and contains genuinely useful design-oriented results, but several central claims (especially the stress-case overhead and coordinator sizing recommendations) are not yet fully consistent with the physical access constraints the paper itself introduces (half-duplex TDMA timing, command egress feasibility). Addressing these issues requires reworking parts of the system model and revising the interpretation of key results, not just editorial changes. With a clearer and internally consistent link/frame model and a more careful statement of the decoupling/feasibility conditions, the paper could be a solid contribution to T-AES.

---

## Constructive Suggestions

1. **Add a “cycle time budget” model and make stress-case feasibility explicit.**  
   Provide a table/figure that allocates \(T_c\) into: sync beacon, \(k_c\) ingress slots, coordinator processing, and egress slots for heartbeats + commands. Then state the additional assumptions required for stress-case (e.g., separate downlink channel, higher PHY rate, or longer \(T_c\)). Recompute headline results under each assumption.

2. **Unify coordinator ingress sizing under one physically grounded access scheme.**  
   If TDMA is the intended design, make TDMA the primary model (deterministic arrivals) and treat random-phase as a “no-scheduling fallback.” If token-bucket is retained, explicitly map it to TDMA (slotting implies bounded burstiness) and clarify how “deadline misses” are handled.

3. **Refine the “pipeline decoupling” claim to distinguish queueing vs. frame-time coupling.**  
   Add a short proposition-style statement: decoupling holds for ingress queue occupancy under orthogonal links, but not necessarily for time-slot resource usage. If possible, add a small extension experiment where failed transmissions still consume slot time and show the effect on completion probability.

4. **Strengthen the centralized baseline (or de-emphasize it).**  
   Add a coarse comm-limited centralized model: per-station capacity, number of stations, contact fraction, and required aggregate uplink. Even a back-of-the-envelope bound would prevent the compute-only \(M/D/c\) result from being misread as “centralized scales fine.”

5. **Expand sensitivity analysis on the most decision-relevant parameters.**  
   In addition to \(p_{BG}\) and \(p_B\), include sensitivity to \(T_c\), command rate \(p_{\text{cmd}}\), and coordinator half-duplex constraints (single vs dual RF chain; orthogonal command channel). These directly affect whether the architecture is feasible in RF-backup mode and would make the design equations more actionable.