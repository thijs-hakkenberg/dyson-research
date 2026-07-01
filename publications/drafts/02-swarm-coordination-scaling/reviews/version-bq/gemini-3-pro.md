---
paper: "02-swarm-coordination-scaling"
version: "bq"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Accept"
---

## Peer Review: IEEE Transactions on Aerospace and Electronic Systems

**Manuscript ID:** [Assigned by Editor]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Version:** BQ

---

### Review Criteria

**1. Significance & Novelty**
**Rating: 5 (Excellent)**

This manuscript addresses a critical and timely gap in the literature regarding mega-constellations ($10^3$--$10^5$ nodes). While significant prior work exists on Inter-Satellite Link (ISL) routing (data plane) and swarm robotics (control plane for small $N$), there is a scarcity of rigorous analysis on the *management plane* for large-scale constellations under bandwidth constraints.

The derivation of closed-form sizing equations for hierarchical coordination is a novel contribution. Specifically, the distinction between "byte budget feasibility" and "TDMA airtime feasibility" (highlighted by the 22-cycle unicast stagger finding) provides a nuanced view often missing in high-level architectural studies. The focus on the "RF-backup" regime (1 kbps) as the design-driving constraint for survivability is a valuable engineering insight.

**2. Methodological Soundness**
**Rating: 4 (Good)**

The methodology combines closed-form analytical derivations with a cycle-aggregated Discrete Event Simulation (DES). This hybrid approach is appropriate for the scale of the problem ($10^5$ nodes), where packet-level simulation would be computationally prohibitive. The authors are transparent about the abstraction level (message-layer events).

However, the Gilbert-Elliott (GE) link model implementation requires scrutiny. The assumption that the channel state is constant over the entire coordination cycle ($T_c = 10$ s) is a strong simplification. While the authors argue this is conservative for recovery analysis, it effectively discretizes channel availability at a very coarse grain. A discussion on how a shorter coherence time (e.g., $T_{coh} \ll T_c$) might affect intra-cycle retransmission efficacy would strengthen the validity of the "Regime B" analysis.

**3. Validity & Logic**
**Rating: 5 (Excellent)**

The conclusions are logically derived from the premises. The paper rigorously distinguishes between different types of overhead ($\eta_0$ vs. $\eta_{cmd}$) and clearly delineates the boundaries of the proposed architecture. The cross-verification between the analytical models and the DES (agreement $<0.1\%$) builds high confidence in the implementation.

The analysis of the "Stress-case" workload is particularly strong. By identifying that unicast commands are not single-cycle feasible under the assumed constraints, the authors avoid the common pitfall of assuming that if the bytes fit the average throughput, the system is schedulable. The logic regarding the "Coordinator Capacity Sizing" (Section IV-A) is sound, particularly the convergence of random-phase and token-bucket models toward the TDMA limit.

**4. Clarity & Structure**
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The density of information is high, yet the structure remains logical. The "Key Notation" table is helpful, and the progression from sizing equations to workload profiles to topology comparisons is intuitive.

The distinction between the three feasibility layers (Byte, MAC, Airtime) in the Abstract and Conclusion is a powerful framing device that helps the reader navigate the complex constraints. Figures are legible and informative, particularly Figure 5 (TDMA comparison) and Figure 8 (Inter-cycle recovery).

**5. Ethical Compliance**
**Rating: 5 (Excellent)**

The authors provide a clear acknowledgment of AI-assisted ideation in the Acknowledgment section, citing a specific internal report/methodology. This transparency is commendable and aligns with emerging best practices. No other ethical concerns are apparent.

**6. Scope & Referencing**
**Rating: 5 (Excellent)**

The paper fits squarely within the scope of *IEEE TAES*, bridging aerospace systems engineering and electronic communications. The reference list is comprehensive, covering historical foundations (Kleinrock, Reynolds), current operational systems (Starlink, OneWeb), and relevant theoretical work (AoI, Consensus). The inclusion of CCSDS standards (Proximity-1, Space Packet Protocol) grounds the theoretical work in practical engineering reality.

---

### Major Issues

1.  **Gilbert-Elliott Coherence Time Justification:**
    In Section IV-C, the GE model assumes the channel state is constant within each $T_c = 10$ s cycle. This forces all intra-cycle retransmissions ($M_r=2$) to fail if the cycle starts in a "Bad" state. While the authors claim this is conservative for recovery, it may be overly pessimistic for *throughput* if the physical obstruction dynamics (e.g., antenna tumbling) have a frequency higher than 0.1 Hz.
    *   *Critique:* If the coherence time is actually 1 second, intra-cycle retries might succeed.
    *   *Requirement:* Please add a brief justification or sensitivity note regarding the physical basis for the 10s coherence assumption. Is it based on specific tumbling rates or structural shadowing models?

2.  **Sectorized Mesh MAC Overhead:**
    In Section III-B-4 and Table IV, the Sectorized Mesh is compared against the Hierarchy. The Hierarchy benefits from an assumed TDMA efficiency ($\gamma = 0.85$). However, the text notes that achieving $\gamma=0.85$ in a mesh without a central coordinator is difficult.
    *   *Critique:* The comparison might be unfair to the Hierarchy if the Mesh is also granted $\gamma=0.85$ in the efficiency calculations, or unfair to the Mesh if the overheads are compared without adjusting for the likely lower MAC efficiency (CSMA/CA $\approx 0.4$) of the Mesh.
    *   *Requirement:* Explicitly state what $\gamma$ value was used to calculate the "Effective Overhead" for the Sectorized Mesh in Table IV and Figure 12. If the Mesh requires CSMA, the divergence in performance is likely even more drastic than presented.

---

### Minor Issues

1.  **Table V (Superframe Budget):** The "Unallocated margin" is 623 ms. The text mentions that under GE steady-state, retransmissions would require ~740 ms, exceeding this margin. It would be helpful to explicitly link this calculation in the text near Table V to reinforce why intra-cycle ARQ is disabled in "Regime B."
2.  **Equation 5 (Mesh Complexity):** The notation $O(N \cdot f \cdot \log N) = O(N^2)$ assumes $f \approx N / \log N$. Please clarify this substitution explicitly in the text immediately following the equation for readers less familiar with gossip protocol scaling.
3.  **Section IV-D (Joint Interaction):** The statement that "GE losses and coordinator queue occupancy are independent" (Table VIII) is counter-intuitive to many readers who assume TCP-like backoff or link-layer repeats that consume buffer space. The explanation "lost messages never reach the queue" is correct for this model (UDP-like drop), but a sentence clarifying that this assumes *no transport-layer flow control* would prevent confusion.
4.  **Reference 1:** "Jonathan's Space Report" is cited as non-archival. While acceptable, citing the specific issue number or date of the report used for the Starlink numbers would improve reproducibility.
5.  **Typos/Formatting:**
    *   Section III-B-2: "RequestVote: 100 B broadcast... quorum = 51 responders". Ensure the distinction between the broadcast request and the unicast responses is clear in the bandwidth accounting.

---

### Overall Recommendation

**Accept with Minor Revisions**

This is a high-quality manuscript that offers significant practical and theoretical contributions to the field of autonomous spacecraft coordination. The derivation of the "stress-case" constraints and the rigorous accounting of overheads provide a solid foundation for future system architects. The requested revisions are primarily clarifications regarding model assumptions (specifically the GE coherence time and Mesh MAC efficiency) rather than flaws in the fundamental logic.

---

### Constructive Suggestions

1.  **Add a "Physical Layer Reality Check" paragraph:** In the Discussion, explicitly map the $\gamma$ parameter to specific radio technologies (e.g., "For an S-band radio with X modulation, preamble Y..."). This grounds the abstract $\gamma$ in hardware reality.
2.  **Visualizing the Unicast Stagger:** A small timing diagram illustrating the "Type 2" unicast command stagger (22 cycles) vs. the "Type 1" broadcast would make the "Airtime Feasibility" argument immediately accessible to visual learners.
3.  **Expand on "Safe Mode":** The concept of "Safe-mode floor" in the Summary is excellent. Consider expanding on how the system transitions to this mode. Does the coordinator explicitly signal "Switch to Exception-Only"? Or is it a timeout-based fallback?
4.  **Clarify "Fluid Server" vs. TDMA:** In Section III-A, explicitly state: "While the DES uses a fluid server model for byte counting, the feasibility of the link is strictly limited by the TDMA frame constraints derived in Section IV-A." This preempts concerns about the simulation fidelity.