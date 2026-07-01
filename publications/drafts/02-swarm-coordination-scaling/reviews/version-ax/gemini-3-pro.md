---
paper: "02-swarm-coordination-scaling"
version: "ax"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

Here is the peer review for the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version AX), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

***

# Peer Review Report

**Manuscript Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## Review Criteria

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This paper addresses a critical and timely gap in the literature: the specific scaling properties of autonomous coordination for "mega-constellations" ($10^3$--$10^5$ nodes). While existing literature covers swarm robotics (typically $<100$ agents) and traditional constellation management (centralized, $<1000$ nodes), the intermediate regime of autonomous, bandwidth-constrained large-scale swarms is under-explored. The derivation of closed-form design equations for this specific regime is a high-value contribution for system architects.

The novelty lies in the rigorous "byte-level" accounting combined with queueing theory to produce usable sizing heuristics (e.g., the 21–25 kbps coordinator ingress requirement). The distinction between "offered" vs. "delivered" overhead under Gilbert-Elliott loss conditions is particularly insightful. The paper moves beyond generic graph-theory abstractions to address concrete engineering constraints (RF backup budgets, half-duplex radios, TDMA framing), which fits the scope of *IEEE TAES* perfectly.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The methodology combines analytical derivation (queueing theory, Markov chains) with discrete event simulation (DES) for verification. This dual approach is robust. The authors are careful to distinguish between *verification* (checking the math against the code) and *validation* (checking the model against reality), which is a sign of rigorous scholarship. The use of a Gilbert-Elliott (GE) model to capture correlated channel losses is appropriate for the LEO environment, where obstructions or interference often occur in bursts.

However, there is a slight disconnect in the "Joint Parameter Interaction" section (IV-D). The paper claims pipeline decoupling holds for dedicated links but acknowledges it breaks down under shared-medium contention. Given that the 1 kbps RF-backup scenario often implies omnidirectional antennas and shared spectrum (e.g., S-band), the reliance on point-to-point assumptions for the decoupling result is a limitation. While the authors acknowledge this, the strength of the "decoupling" claim in the abstract should be tempered or explicitly linked to the TDMA assumption.

### 3. Validity & Logic
**Rating: 5 (Excellent)**

The logic flow is tight and persuasive. The decomposition of latency into propagation, serialization, and queueing components (Table VIII) is clear. The argument that hierarchical architectures are superior not because of latency (where they lag centralized systems) but because of fault tolerance and ground-independence is well-supported by the data.

The analysis of the "Coordinator Failure Transient" (Section III-B-2) is logically sound. The use of Age of Information (AoI) as a primary metric for coordination quality is appropriate for control systems. The derivation of the TDMA frame efficiency ($\gamma \approx 0.95$, conservatively 0.85) is physically grounded in radio hardware realities (turnaround times, propagation delay). The conclusion that command traffic dominates overhead in stress cases is a significant, non-obvious finding that logically follows from the traffic accounting.

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The structure is logical, moving from problem definition to model description, results, and discussion. The use of "Research Questions" (RQ1-RQ3) in the introduction helps frame the contributions.

Tables are dense but informative; Table V (Traffic Accounting) and Table VII (Scaling) are particularly useful for reproducibility. The distinction between "Stress," "Nominal," and "Event-driven" workloads (Section IV-E) clarifies the operational envelope well. The definitions of metrics (Section III-G) are precise.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a specific "Acknowledgment" section detailing the use of AI tools (Claude, Gemini, GPT) for ideation, explicitly stating that the validation was performed via standard methods. This transparency sets a high standard for ethical disclosure. No conflicts of interest are apparent. The open-source availability of the simulation code (GitHub link provided) supports reproducibility and ethical transparency.

### 6. Scope & Referencing
**Rating: 4 (Good)**

The paper is well-scoped for *TAES*. It bridges the gap between networking (communications) and guidance/navigation/control (autonomy). The references are generally strong, covering foundational queueing theory (Kleinrock), swarm robotics (Dorigo, Brambilla), and recent mega-constellation literature (Handley, Del Portillo).

One minor gap is the lack of comparison to specific Delay Tolerant Networking (DTN) routing overheads beyond a passing mention of BPv7. While the paper focuses on coordination rather than general data transport, a brief quantitative comparison of the proposed header overheads vs. standard BPv7 bundle headers would strengthen the contextualization.

***

## Major Issues

1.  **MAC Layer Contention vs. Abstracted $\gamma$:**
    The paper relies heavily on the parameter $\gamma$ (MAC efficiency) to bridge the gap between the message-layer simulation and physical reality. While the TDMA derivation (Section IV-A) is sound for *established* clusters, it glosses over the contention required to *join* the cluster or recover from synchronization loss.
    *   *Critique:* The paper states that if sync is lost, the system reverts to Slotted ALOHA ($\gamma \approx 0.36$). However, in a saturated stress-case scenario ($\eta > 60\%$), Slotted ALOHA collapses (throughput $\to 0$), not just degrades. The paper mentions this briefly, but the implications of a "coordination collapse" during a high-stress event (e.g., a solar storm causing both GNSS loss and high command traffic) need more explicit analysis.
    *   *Requirement:* Please expand the discussion in Section IV-A or V-C to explicitly address the "death spiral" risk where high load + sync loss leads to zero throughput, and propose a specific back-off or priority mechanism (e.g., "monitoring-only" fallback) to prevent this.

2.  **Coordinator Ingress vs. Egress Asymmetry:**
    Section IV-A focuses heavily on *ingress* capacity (21–25 kbps). However, the stress-case workload is dominated by *commands* (512 B/node), which is an *egress* flow from the coordinator to the members.
    *   *Critique:* If the coordinator is half-duplex (as stated), and ingress takes ~92% of the cycle (Section IV-A, "Half-duplex TX/RX partitioning"), there is very little time left for the coordinator to broadcast the bulky command updates. The current text suggests commands might need a "separate downlink slot," but this contradicts the 1 kbps aggregate budget constraint if that downlink isn't accounted for.
    *   *Requirement:* You must reconcile the ingress time-consumption with the egress bandwidth requirement for the stress case. If ingress takes 9s of a 10s cycle, can the coordinator physically transmit 512B * 100 nodes = 51KB of commands in the remaining 1s? At 24 kbps, 1s only allows ~3KB. This suggests the stress case is infeasible under the half-duplex assumption without a separate frequency channel or a much longer cycle time. This is a potential physical-layer violation in the model.

***

## Minor Issues

1.  **Abstract, Line 8:** "AoI under exception telemetry (P99 = 440 s)." Please clarify if this is the *peak* AoI or the *steady-state* distribution P99.
2.  **Section III-B-2 (Hierarchical Topology):** The text mentions "Regional coordinators forward 1024-byte region summaries." Please clarify if this aggregation is lossy. If 100 cluster summaries (512B each) become one 1024B region summary, that is a massive compression ratio. What information is lost?
3.  **Section IV-C (Correlated Loss):** The definition of "coherence assumption" implies the state is constant for the *entire* 10s cycle. This is a very strong assumption. Real LEO channels might have fast fading (ms scale) superimposed on slow shadowing. Acknowledge that this assumption maximizes the "burstiness" impact (worst-case for intra-cycle retry).
4.  **Figure 5 (Recovery):** The caption mentions "Markov-chain analytical model." Please ensure the equation for this model is explicitly written in the text near the figure, or clearly referenced if it is Eq. 11.
5.  **Typos/Formatting:**
    *   Table I: "Status reporting rate r" is listed as 0.1 msg/s. Ensure this is consistent with $T_c = 10s$.
    *   References: Ensure all URL access dates are consistent (some say "Feb 2026").

***

## Overall Recommendation

**Recommendation: Minor Revision**

**Justification:**
This is a high-quality paper that makes a significant contribution to the field of space systems engineering. The derivation of closed-form design equations for swarm coordination is novel and immediately useful. The simulation framework is rigorous. However, the "Major Issue" regarding the physical feasibility of the Coordinator Egress (commands) during the stress case under half-duplex constraints represents a potential flaw in the sizing logic that must be addressed. The authors likely have an answer (e.g., broadcast commands rather than unicast, or multi-cycle command distribution), but it is not currently clear in the text. Once this and the contention collapse mode are clarified, the paper is well-suited for publication.

***

## Constructive Suggestions

1.  **Resolve the Egress Bottleneck:** Explicitly calculate the time required for the coordinator to transmit stress-case commands. If it exceeds the idle time in the TDMA frame, propose a solution (e.g., "Commands are broadcast to the whole cluster in one slot, not unicast," or "Commands span multiple cycles").
2.  **Add a "Safe Mode" Floor:** In your design equations, define a minimum $\gamma$ or maximum $\eta$ for "Safe Mode" operation (e.g., when sync is lost). This would provide a lower bound for system robustness.
3.  **Strengthen the "Decoupling" Claim:** In the abstract and conclusion, qualify the "pipeline decoupling" result with "assuming dedicated/orthogonal links." This prevents readers from misapplying the result to shared-spectrum ALOHA implementations.
4.  **Visualizing the Frame:** Consider adding a small timing diagram (Figure) showing the TDMA slot structure, specifically illustrating the Guard Time, Preamble, and the Ingress vs. Egress partitioning within the $T_c$ window. This would clarify the half-duplex constraints immediately.