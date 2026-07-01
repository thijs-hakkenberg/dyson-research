---
paper: "02-swarm-coordination-scaling"
version: "bm"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Accept"
---

## Peer Review: IEEE Transactions on Aerospace and Electronic Systems

**Manuscript ID:** [Assumed from Context]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Version:** BM

---

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

**Assessment:**
This manuscript addresses a critical and timely gap in the literature: the scaling behavior of coordination architectures for "mega-constellations" ($10^4$--$10^5$ nodes). While existing literature covers swarm robotics (typically $N < 100$) and traditional constellation management (centralized), there is a paucity of rigorous analysis for the intermediate regime of autonomous, large-scale space systems.

The primary contribution—a set of closed-form sizing equations validated by discrete event simulation (DES)—is highly significant for system architects. The distinction between "byte budget feasibility," "MAC efficiency," and "TDMA airtime schedulability" (Table V) is a novel and valuable conceptual framework that moves beyond simple bandwidth summing. The finding that command traffic, rather than topology maintenance, dominates the stress-case bandwidth budget is a crucial insight for future operations concepts.

### 2. Methodological Soundness
**Rating: 4 (Good)**

**Assessment:**
The methodology is rigorous within its stated scope. The use of a cycle-aggregated DES to validate analytical equations is appropriate. The queueing theoretic models (Batch $D[k_c]/D/1$ for coordinators) are correctly applied. The Gilbert-Elliott (GE) model for correlated link losses is implemented with necessary nuance, specifically the distinction between intra-cycle and inter-cycle recovery.

However, a specific assumption requires stronger justification: the "Static Topology" assumption for the 1-year duration. While the authors address cross-plane re-association in the Limitations (Section V.B), the assumption that cluster membership remains static for a full year in a large-scale LEO swarm is optimistic given orbital perturbations and differential drag, even within co-planar formations. While this likely does not invalidate the *bandwidth* results, it may underestimate the signaling overhead required for cluster maintenance.

### 3. Validity & Logic
**Rating: 5 (Excellent)**

**Assessment:**
The conclusions are logically derived from the data. The authors are careful to distinguish between "message-layer" predictions and "physical-layer" realities, using the parameter $\gamma$ (MAC efficiency) to bridge the gap. The analysis of the "Stress (unicast)" workload profile is particularly strong; the derivation that per-node unicast commands are not single-cycle deliverable (requiring a 22-cycle stagger) is a non-intuitive finding that validates the need for this level of detailed modeling.

The comparison with the "Sectorized Mesh" is fair and balanced. The authors explicitly note the difference in functional scope (local awareness vs. fleet coordination), preventing a false equivalency between the architectures.

### 4. Clarity & Structure
**Rating: 4 (Good)**

**Assessment:**
The paper is dense but well-organized. The progression from sizing equations to AoI analysis to loss recovery is logical. Tables are highly informative, particularly Table V (Workload Feasibility) and Table VIII (Topology Comparison).

There is, however, potential for confusion regarding the bandwidth definitions. The paper uses $C_{\text{node}} = 1$ kbps as a "traffic budget" and $C_{\text{coord}} \approx 24$ kbps as a "PHY rate." While Section III.E clarifies this distinction ("Peak vs. average rate"), the early sections could be clearer that $C_{\text{node}}$ is an allocated average throughput constraint, not necessarily a hardware link limit.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

**Assessment:**
The authors provide a specific acknowledgment regarding AI-assisted ideation (Claude, Gemini, GPT), citing a methodology paper. This transparency is commendable and aligns with emerging best practices for AI disclosure in academic publishing. No conflicts of interest are apparent.

### 6. Scope & Referencing
**Rating: 5 (Excellent)**

**Assessment:**
The paper fits squarely within the scope of *IEEE TAES*, bridging space systems engineering, communications, and autonomous control. The referencing is comprehensive, covering historical foundations (Kleinrock, Lamport), current commercial context (Starlink, Kuiper), and relevant protocols (CCSDS, DTN).

---

### Major Issues

1.  **Clarification of the 1 kbps Constraint:**
    The premise that 1 kbps is the "design-driving edge case" for S-band backup needs more context. Modern S-band transceivers for CubeSats often achieve 9.6--100 kbps. If the 1 kbps limit is derived from a specific link budget (e.g., omni-directional antennas on tumbling spacecraft at max slant range), this should be explicitly stated. If it is an arbitrary "safe mode" allocation, the paper should justify why it is so low. This value drives the entire "Stress Case" bottleneck analysis; if the backup link were 10 kbps, many of the identified constraints (e.g., the 22-cycle unicast stagger) would vanish.

2.  **Centralized Baseline Comparison (Fig. 10):**
    In Figure 10 and Table VIII, the Centralized architecture is shown to scale to $N \approx 10^6$ based on a processing limit ($M/D/c$). This is a theoretical compute bound, but in reality, a centralized architecture for $10^5$ satellites would be bound by *uplink spectrum availability* and *ground station visibility*, not server CPU cycles. Comparing the *compute* limit of the centralized approach against the *bandwidth* limit of the mesh approach is an "apples-to-oranges" comparison. The authors should either add a spectral/uplink constraint to the centralized model or explicitly label the centralized curve as "Compute-Bound Only (Idealized)" to avoid misleading readers about the viability of centralized control for $10^6$ nodes.

### Minor Issues

*   **Section III.A (DES Architecture):** The text states the simulation is "cycle-aggregated." It would be helpful to clarify if this implies synchronous execution (all nodes step together) or if there is drift modeling.
*   **Section IV.A (TDMA Frame):** The derivation of $\gamma = 0.949$ is optimistic. The assumption of 4.7 ms guard time covers propagation and turnaround, but does not account for clock drift between synchronization beacons if GNSS is denied. A brief mention of clock stability requirements (e.g., TCXO quality) to maintain this guard time would strengthen the argument.
*   **Table I (Notation):** The symbol $r$ is defined as "Status reporting rate" in Table II but appears as part of the utilization formula in Table I. Ensure consistency.
*   **Fig. 6 (Overhead Decomposition):** The legend or caption should clarify if "Summaries" includes both cluster and region summaries.
*   **Typos:**
    *   Section III.B.2: "RequestVote: 100 B broadcast... quorum = 51 responders required." Technically, in Raft, the *response* is what confirms the vote, so the traffic is bidirectional. The accounting seems to cover this, but the phrasing is slightly imprecise.

### Overall Recommendation
**Accept with Minor Revisions**

**Justification:**
This is a high-quality, rigorous paper that provides valuable design tools for the aerospace engineering community. The analytical contributions are novel and well-validated. The requested revisions focus on clarifying assumptions (link budget, centralized baseline constraints) rather than correcting fundamental flaws. The manuscript is likely to become a standard reference for sizing autonomous constellation networks.

### Constructive Suggestions

1.  **Add a "Link Budget Justification" Subsection:** Briefly explain the physical basis for the 1 kbps constraint. Is it based on a specific link margin calculation (e.g., 1W TX, 0 dBi gain, 1000 km range)? This grounds the theoretical analysis in physical reality.
2.  **Refine the Centralized Baseline:** In Table VIII, add a footnote or column indicating that the Centralized limit ignores spectral constraints. This ensures the comparison with the bandwidth-limited hierarchical model is contextually accurate.
3.  **Expand on "Dynamic Topology" in Discussion:** While the simulation uses static topology, add a paragraph in the Discussion estimating the cost of dynamic clustering. For example, "If 1% of nodes change clusters per cycle, the re-association overhead adds $X$ bytes, which is negligible compared to the command traffic." This defends the static assumption quantitatively.
4.  **Visualizing the "Feasibility Layers":** Consider adding a small flowchart or diagram illustrating the three layers (Byte Budget $\to$ MAC Efficiency $\to$ Airtime Scheduling). This would help readers visualize the "sieve" through which a design must pass to be considered feasible.