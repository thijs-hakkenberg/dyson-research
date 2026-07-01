---
paper: "02-swarm-coordination-scaling"
version: "bg"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Accept"
---

# Peer Review: IEEE Transactions on Aerospace and Electronic Systems

**Manuscript ID:** [Assigned by Editor]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Version:** BG

## Review Criteria

### 1. Significance & Novelty
**Rating: 5**

This manuscript addresses a critical and timely problem in aerospace engineering: the scalability of command and control (C2) architectures for mega-constellations ($10^4+$ nodes). As commercial entities propose constellations exceeding 100,000 satellites, traditional centralized ground-in-the-loop coordination becomes untenable due to latency and spectrum constraints.

The novelty lies in the derivation of **closed-form sizing equations** specifically for hierarchical topologies in this domain. While hierarchical control is well-established in robotics, its rigorous application to orbital mechanics constraints (e.g., specific orbital regimes, conjunction screening latencies) with byte-level accounting is a significant contribution. The paper successfully bridges the gap between high-level distributed systems theory and practical link-budget engineering. The distinction between "architecture-specific" overhead ($\sim 5\%$) and "workload-dependent" overhead is a valuable insight for system architects.

### 2. Methodological Soundness
**Rating: 4**

The methodology combines analytical derivation with a cycle-aggregated Discrete Event Simulation (DES). The approach is generally robust, but relies on specific abstractions that require careful interpretation:

1.  **Cycle-Aggregated DES:** The simulation steps in $T_c = 10$s increments. This is computationally efficient for verifying logical correctness and queue depths over year-long durations. However, it abstracts away physical layer (PHY) and MAC-layer contention dynamics (e.g., packet collisions, hidden nodes), relying instead on efficiency factors ($\gamma$). The authors acknowledge this "Validation Gap" in Section V-A, which is intellectually honest, but it limits the assessment of real-world RF behavior.
2.  **Gilbert-Elliott (GE) Model Implementation:** The assumption that the channel state remains constant for the entire duration of a coordination cycle ($T_c=10$s) and transitions only at boundaries is a strong simplification. While it facilitates the "inter-cycle recovery" analysis, real-world channel fading or structural shadowing does not align neatly with protocol cycle boundaries. This may artificially quantize the recovery behavior.
3.  **Parameter Space:** The sweep across bandwidths (1 kbps to 100 kbps) and cluster sizes is comprehensive. The choice of 1 kbps as a design driver is extremely conservative but defensible as a "safe mode" baseline.

### 3. Validity & Logic
**Rating: 5**

The conclusions are logically sound and tightly coupled to the data presented.
*   **Scaling Claims:** The finding that the coordinator bottleneck vanishes at $\geq 10$ kbps is well-supported by the sizing equations (Table I).
*   **Overhead Accounting:** The distinction between topology-invariant baseline telemetry and protocol overhead is handled with high precision. The match between analytical predictions and DES results (<0.1%) validates the internal consistency of the equations.
*   **Latency vs. Conjunction:** The mapping of Age of Information (AoI) P99 values (440s) to operational Time-to-Closest-Approach (TCA) tolerances is a strong practical validation step that grounds the theoretical work in operational reality.

### 4. Clarity & Structure
**Rating: 5**

The manuscript is exceptionally well-written. The structure is logical, following a standard progression from theory to simulation to results.
*   **Tables:** The tables are dense but highly informative. Table I (Scaling) and Table VIII (Schedulability) are particularly effective summaries.
*   **Notation:** The notation is consistent. The definition of $\eta$ vs $\eta_{total}$ is handled carefully to avoid confusion.
*   **Abstract:** The abstract is quantitative and accurately reflects the paper's contributions.

### 5. Ethical Compliance
**Rating: 5**

The authors include a specific acknowledgment regarding AI-assisted ideation (Claude, Gemini, GPT), citing a "Multi-model AI deliberation" paper. This transparency regarding the use of AI tools in the research process is commendable and aligns with emerging best practices. No conflicts of interest are apparent.

### 6. Scope & Referencing
**Rating: 5**

The paper fits perfectly within the scope of *IEEE TAES*, specifically the areas of Space Systems and Networked Systems. The reference list is comprehensive, spanning foundational queueing theory (Kleinrock), distributed consensus (Lamport, Raft), and modern constellation literature (Handley, Del Portillo). The inclusion of swarm robotics literature (Brambilla, Dorigo) provides necessary context for the multi-agent aspects.

---

## Major Issues

**1. Gilbert-Elliott (GE) Coherence Time Assumption**
In Section IV-C and Section III-B, the GE model assumes the channel state is constant within a cycle ($T_c=10$s). This effectively forces a "block fading" model where the block length equals the protocol period.
*   *Critique:* This assumption pre-determines the failure of intra-cycle retransmissions ($M_r$) during a "Bad" state. If the coherence time were actually 1s, intra-cycle retries might succeed. Conversely, if the coherence time is 60s (antenna mispointing), the state persists across multiple cycles.
*   *Requirement:* The authors should explicitly discuss the sensitivity of their results to the ratio of Coherence Time ($\tau_c$) to Cycle Time ($T_c$). The current text mentions "fast-mixing" vs "slow-mixing," but the simulation appears locked to the $T_c$ boundary. A brief discussion or analytical note on how non-aligned fading would alter the "Inter-cycle P95" would strengthen the physical validity.

**2. Unicast Command Latency in Stress Cases**
Table VIII and Eq. 10 highlight that unicast commands to all nodes require 22 cycles (220s) at 1 kbps.
*   *Critique:* This is a massive operational constraint. While the paper acknowledges it, the implications for "emergency" operations are understated. If a fleet-wide emergency maneuver is required (e.g., solar storm safing), a 220s dissemination latency could be catastrophic.
*   *Requirement:* The discussion should explicitly frame this as a "Command Dissemination Bottleneck." It suggests that for large clusters ($k_c=100$) on low-bandwidth links, *multicast* or *broadcast* command addressing is not just efficient, but mandatory for safety-critical operations.

---

## Minor Issues

1.  **Eq. 5 (Message Count):** The term $N/(k_c \cdot k_r)$ represents regional summaries. Ensure $k_r$ is clearly defined in the text near the equation as "clusters per region" (it is defined in Table II, but helpful to reiterate in text).
2.  **Table II (Bandwidth Breakdown):** The "Global-State Mesh" column lists overhead as ">1 kbps" and "Exceeds." It would be helpful to provide the estimated value (e.g., "~73 MB" as mentioned in text) to emphasize the order-of-magnitude difference.
3.  **Section IV-A (TDMA Frame):** The derivation of $\gamma = 0.949$ vs the used $0.85$ is good conservatism. However, does the 4.7ms guard time account for clock drift *between* synchronizations if the GNSS is denied for long periods? A brief mention of oscillator stability requirements (e.g., TCXO quality) would add engineering depth.
4.  **Fig. 5 (Joint Interaction):** The columns for "No Loss" and "GE Only" are identical. While the text explains this is due to pipeline decoupling (link loss $\neq$ queue drop), visually it looks like a simulation error. A caption note explicitly stating "Link losses do not affect queue occupancy under dedicated TDMA" would help the reader.
5.  **Typos:**
    *   Section III-B: "The simulation assumes *static* cluster membership..." - Consider clarifying if this includes "static" relative to the orbital plane or the ground. (Context implies orbital plane/neighbors).

---

## Overall Recommendation
**Accept with Minor Revisions**

This is a high-quality paper that provides a much-needed theoretical foundation for sizing the communication networks of future mega-constellations. The derivation of closed-form equations verified by simulation constitutes a significant contribution to the field. The requested revisions are primarily regarding the clarification of channel model assumptions and emphasizing the operational implications of the command dissemination bottleneck.

---

## Constructive Suggestions

1.  **Add a "Design Guide" Subsection:** In the Conclusion or Discussion, add a brief bulleted list of "Rules of Thumb" for practitioners. E.g., "If bandwidth > 10 kbps, coordinator queuing is negligible," "If $T_c < \tau_{coherence}$, disable intra-cycle retries."
2.  **Visualizing the Unicast Bottleneck:** Consider adding a small subplot to Figure 7 or 8 showing "Command Dissemination Time" vs. "Cluster Size" for Unicast vs. Broadcast. This would visually drive home the 22-cycle delay issue.
3.  **Refine the GE Model Justification:** Explicitly state that setting the GE transition at cycle boundaries provides an *upper bound* on recovery time (conservative) because it prevents "lucky" mid-cycle recoveries. This solidifies the claim that the design curves are safe for sizing.