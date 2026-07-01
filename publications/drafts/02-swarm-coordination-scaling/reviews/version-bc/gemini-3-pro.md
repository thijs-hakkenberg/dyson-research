---
paper: "02-swarm-coordination-scaling"
version: "bc"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

Here is a comprehensive peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version BC), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review Report

**Manuscript Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## Review Summary

This paper presents a parametric sizing analysis for hierarchical coordination architectures in large-scale autonomous satellite swarms ($10^3$--$10^5$ nodes). It derives closed-form equations for bandwidth, latency (Age of Information), and reliability, validating them against a custom discrete event simulation (DES). The central contribution is the characterization of the "RF-backup" regime (1 kbps/node), demonstrating that hierarchical coordination is feasible with $\sim$5% overhead for nominal operations but requires up to 46% for stress-case command dissemination.

The paper is technically sound, highly relevant to the emerging era of mega-constellations, and offers practical "practitioner's toolkit" equations. However, there are specific areas regarding physical layer abstraction and the comparison with mesh topologies that require refinement to meet the rigorous standards of *IEEE TAES*.

---

## Detailed Review Criteria

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

**Assessment:**
The paper addresses a critical and timely gap in the literature. While routing in mega-constellations (Starlink, Kuiper) is well-studied, the *command and control* (C2) plane for autonomous operations at this scale is under-explored. Most existing literature focuses on small swarms ($<100$ nodes) or centralized management. Bridging the gap to $10^5$ nodes with specific byte-level accounting is a significant contribution.

The distinction between "architecture-specific" overhead (maintenance traffic) and "workload-dependent" overhead (commands) is a valuable insight that corrects common misconceptions about the cost of hierarchy. The focus on the RF-backup regime (1 kbps) is particularly operationally relevant, as this is the "safe mode" bottleneck that drives system survival during optical link failures.

### 2. Methodological Soundness
**Rating: 4 (Good)**

**Assessment:**
The methodology combines standard queueing theory ($M/D/1$, $D[k]/D/1$) with a custom cycle-aggregated DES. The statistical approach is rigorous: 30 Monte Carlo replications, bootstrap confidence intervals, and clear separation of independent variables. The validation of closed-form equations against the DES is successful (errors $<0.1\%$).

However, the abstraction of the physical layer (PHY) is a limitation that needs stronger justification. The derivation of $\gamma$ (MAC efficiency) in Section IV.A is analytical but optimistic. The assumption that TDMA slots can be perfectly aligned without significant guard time overhead beyond 4.7ms in a distributed, potentially tumbling swarm (during contingencies) is a strong assumption. While the authors acknowledge this as a "validation gap," the paper would benefit from a sensitivity analysis on $\gamma$ specifically regarding synchronization errors, rather than just treating it as a fixed efficiency factor.

### 3. Validity & Logic
**Rating: 4 (Good)**

**Assessment:**
The logic flow is generally tight. The derivation of the Gilbert-Elliott (GE) recovery time is mathematically sound and provides a useful design curve for practitioners. The "pipeline decoupling" finding (Section IV.D)—that link losses do not inflate coordinator queues under dedicated links—is a subtle but correct and important point.

A minor logical weakness exists in the comparison with the "Sectorized Mesh." The authors note that the mesh provides only local awareness while the hierarchy provides cluster-wide awareness, yet they compare byte overhead directly. While the paper acknowledges this functional discrepancy (Section III.B.4), the comparison in Figure 11 (Topology Summary) could be misleading if a reader assumes equivalent functionality. The paper should more explicitly state that the hierarchy is "buying" more global state for its lower overhead compared to the mesh's high cost for local state.

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

**Assessment:**
The manuscript is exceptionally well-written. The structure is logical, moving from problem definition to simulation framework, then results, and finally discussion. The "Practitioner Toolkit" summary in Section V.D is a fantastic addition that increases the paper's utility.

The notation is consistent (Table I is helpful). Figures are generally clear, though Figure 11 (Topology Summary) is dense and might benefit from being split or simplified. The distinction between "offered" and "delivered" overhead is maintained carefully throughout the text, which is crucial for this type of analysis.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

**Assessment:**
The authors include a specific acknowledgment regarding AI-assisted ideation (Claude, Gemini, GPT), citing a specific methodology paper. This transparency is commendable and aligns with emerging best practices. No conflicts of interest are apparent. The research involves simulation of theoretical systems and raises no human subject concerns.

### 6. Scope & Referencing
**Rating: 4 (Good)**

**Assessment:**
The scope is well-suited for *TAES*. The references are a good mix of classical theory (Kleinrock, Lamport), space systems engineering (Wertz, CCSDS standards), and recent networking literature (HotNets, IEEE INFOCOM).

One missing area is the comparison to Delay Tolerant Networking (DTN) bundle protocol overheads beyond just citing the standard. Since the paper discusses intermittent links and storage, briefly discussing how Bundle Protocol headers might impact the byte-level accounting (which currently assumes raw CCSDS packets) would strengthen the "implementation realism."

---

## Major Issues

1.  **TDMA Synchronization in RF-Backup Mode:**
    The paper relies heavily on TDMA ($\gamma \approx 0.85-0.95$) to close the link budget at the coordinator. However, the operational context is often a "backup" or "safe mode" where GNSS might be denied or the satellite might be tumbling.
    *   *Critique:* If GNSS is denied, maintaining the microsecond-level timing required for efficient TDMA across a 500km cluster is non-trivial. The paper mentions a "sync beacon" (0.8% overhead), but does not account for the *propagation delay variance* relative to the guard time if nodes have high position uncertainty during a contingency.
    *   *Requirement:* Please expand the justification for $\gamma$ in Section IV.A. Specifically, address how slot timing is maintained if position uncertainty grows (which is implied by the high AoI in exception-based telemetry). If $\gamma$ drops to 0.5 due to larger guard times, does the architecture break?

2.  **Sectorized Mesh Fairness:**
    In Section III.B.4 and Table V, the Sectorized Mesh is penalized for having high overhead ($\sim$65%) while providing only "local" awareness.
    *   *Critique:* The comparison assumes the mesh *must* send heartbeats to 10 neighbors. However, mesh protocols often use adaptive beaconing. The current comparison feels like a "strawman" designed to make the hierarchy look better.
    *   *Requirement:* Acknowledge that the mesh overhead is high *because* the authors have imposed a specific update rate and neighbor count. A fairer comparison might be: "To achieve equivalent latency to the hierarchy, the mesh requires X bandwidth." If the mesh is allowed to have higher latency (multi-hop), its bandwidth requirement might drop. Clarify that the hierarchy is optimized for *bandwidth efficiency* at the cost of *centralized reliance*, whereas the mesh optimizes for *robustness* at the cost of *bandwidth*.

---

## Minor Issues

1.  **Table I (Notation):** The symbol $\eta$ is defined as "Protocol overhead fraction," but later $\eta_{total}$ includes the baseline. Ensure the text explicitly distinguishes between $\eta$ (protocol only) and channel utilization (protocol + baseline) in every instance to avoid confusion.
2.  **Section III.A (DES):** The text states "Physical-layer validation... is future work." It would be beneficial to explicitly state *why* NS-3 or OMNeT++ was not used for this study (presumably due to the computational cost of simulating $10^5$ nodes for a full year).
3.  **Section IV.C (GE Model):** The assumption that the GE state is constant within a cycle ($T_c=10s$) is conservative for burst length but optimistic for recovery if the channel changes faster. Briefly mention how a fast-fading channel (coherence time $\ll 10s$) would alter the results (likely improving intra-cycle recovery).
4.  **Figure 6 (AoI):** The y-axis is log-scale? Please clarify in the caption, as the visual growth looks linear but the text describes geometric effects.
5.  **Equation 8 (AoI Analytic):** The ceiling function is used. Is this an approximation or exact for discrete time steps? Clarify if $T_c$ is the quantization step.
6.  **Typos:**
    *   Section IV.A: "hardware: 25 kB buffer" - ensure capitalization of 'kB' vs 'kb' is consistent throughout (Bytes vs bits).
    *   References: Check formatting of [1] and [3] (non-archival URLs) to ensure they meet IEEE standards (access dates are provided, which is good).

---

## Overall Recommendation

**Recommendation: Minor Revision**

**Justification:**
The manuscript is high-quality, novel, and methodologically rigorous within its defined scope. The analytical models are valuable for the community. The requested revisions regarding TDMA synchronization robustness and the nuance of the mesh comparison are necessary to ensure the conclusions are unassailable, but they do not require re-running the core simulations. The paper is well on its way to being a significant reference for swarm coordination.

---

## Constructive Suggestions

1.  **Add a "Guard Time Sensitivity" Plot:** In Section IV.A, add a small subplot or discussion showing how $\gamma$ (and thus system feasibility) degrades as a function of position uncertainty/timing error. This would robustly answer the "GNSS-denied" critique.
2.  **Refine the Mesh Comparison Narrative:** Instead of framing the mesh simply as "high overhead," frame it as a trade-off space. "The mesh pays a 1.5x bandwidth penalty for local robustness; the hierarchy saves bandwidth by centralizing state." This is a more neutral and scientific framing.
3.  **Expand on DTN/BPv7:** In the discussion, add a paragraph estimating the overhead of wrapping these messages in CCSDS Bundle Protocol (RFC 9171). If BPv7 adds ~50-100 bytes per packet, does the 1 kbps budget still hold? This connects the theoretical work to practical implementation standards.
4.  **Visualizing the "Design Envelope":** Figure 9 (Workload Comparison) is good. Consider annotating it with a "Feasibility Region" shaded area that shows where the 1 kbps limit is hit for different $\gamma$ values. This would visually link the bandwidth, MAC efficiency, and workload sections.