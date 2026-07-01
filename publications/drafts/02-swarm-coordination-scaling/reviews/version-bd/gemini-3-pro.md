---
paper: "02-swarm-coordination-scaling"
version: "bd"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

**Review of Manuscript Version BD**
**"Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms"**

**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems
**Recommendation:** Minor Revision

---

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This manuscript addresses a timely and critical gap in the literature: the scalability of command and control (C2) architectures for mega-constellations ($10^4$--$10^5$ nodes). While existing literature covers swarm robotics (typically $N < 100$) or networking/routing (ISL topology), there is a scarcity of rigorous analysis regarding the *management plane* overhead for fleets of this magnitude, particularly under bandwidth-constrained "RF backup" conditions.

The novelty lies in the derivation of closed-form "practitioner's equations" that are validated against a discrete event simulation (DES). The distinction between topology-invariant command traffic and architecture-specific overhead is a valuable insight that clarifies where optimization efforts should be focused. The focus on the 1 kbps regime is particularly relevant for defining safety-critical lower bounds for autonomous operations.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The methodology combines standard queueing theory ($M/D/1$, $M/D/c$), geometric probability, and Gilbert-Elliott (GE) link models with a custom DES. The approach is generally rigorous. The authors are careful to distinguish between "byte budget" (information theoretic) and "schedulability" (TDMA frame constraints), which is a common pitfall in this domain.

However, there is one specific area regarding the consensus mechanism that requires further justification (see Major Issues). The assumption that a Raft election can complete in 3--5 seconds over a 1 kbps link with a cluster size of $k_c=100$ is optimistic and warrants a more detailed link-budget analysis for the control traffic involved in the election phase.

### 3. Validity & Logic
**Rating: 5 (Excellent)**

The conclusions are well-supported by the data. The authors effectively use the "Global-State Mesh" as a theoretical upper bound and the "Centralized" model as a processing lower bound to frame their Hierarchical solution. The analysis of the Gilbert-Elliott model is sophisticated, particularly the insight in Section IV.D regarding the decoupling of link losses from queue overflows under dedicated TDMA links.

The limitations section is honest, particularly regarding the lack of physical-layer validation (MAC contention beyond $\gamma$, antenna pointing). The logic regarding the "Bandwidth-Robustness Tradeoff" (Section IV.F) is sound and provides a balanced view of why one might choose a mesh over a hierarchy despite the bandwidth penalty.

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The structure is logical, moving from theoretical formulation to simulation verification, and then to parameter sensitivity. The "Roadmap" in Section IV is helpful. The tables are dense but highly informative, specifically Table I (Notation) and Table V (Bandwidth Breakdown). The distinction between "Nominal," "Event-Driven," and "Stress-Case" workloads helps the reader understand the operational envelope.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a clear disclosure regarding the use of AI for ideation in the Acknowledgments, which complies with emerging standards for transparency. No human subjects or hazardous materials are involved.

### 6. Scope & Referencing
**Rating: 5 (Excellent)**

The paper fits perfectly within the scope of *IEEE TAES*. It bridges the gap between astrodynamics (constellation sizing), communications (link budgets), and systems engineering. The references are comprehensive, covering historical concepts (O'Neill), current commercial reality (Starlink, Kuiper), and theoretical distributed systems (Lamport, Lynch).

---

### Major Issues

**1. Raft Election Timing on 1 kbps Links (Section III.B.2)**
The manuscript states: *"Total handoff window: 3--5 s including Raft election."* and *"Emergency re-election uses a seed handoff (~2 kB, 16 s at 1 kbps)."*
There appears to be a discrepancy here. If the seed handoff takes 16s, the total window cannot be 3-5s. Furthermore, a Raft election involves `RequestVote` and `RequestVoteResponse` messages. In a cluster of $k_c=100$, even if only a few candidates emerge, the control traffic overhead on a 1 kbps shared channel (or even the coordinator's specific channel) is non-trivial.
*   **Critique:** At 1 kbps, the transmission of a single 100-byte packet takes 0.8 seconds. If a leader fails and a new election is triggered, the latency to achieve a quorum among 100 nodes might exceed 3-5 seconds due to serialization delay and contention, especially if the system reverts to Slotted ALOHA during the leaderless interim.
*   **Requirement:** Please clarify the link budget and message sequence for the election specifically. If the 3-5s figure assumes the optical ISL is active, please state that explicitly. If it assumes the 1 kbps RF backup, the math needs to be revisited or the duration increased.

### Minor Issues

**1. TDMA Guard Time & Position Uncertainty (Section IV.A)**
The paper argues that even at 100 km position uncertainty, the guard time impact is minimal. While mathematically true for the *propagation* delay, large position uncertainties often correlate with clock drift (if GNSS is denied). The paper mentions TCXO drift, but does not explicitly link the position uncertainty to the acquisition time required at the start of a slot. If a node is 100 km off, does the coordinator's beamwidth still cover it, or is a scanning loss incurred? A brief sentence clarifying the beamwidth assumption would strengthen the TDMA feasibility argument.

**2. Table II Interpretation**
In Table II, the column for "100 kbps" shows $\eta_{stress} = 0.46\%$. While mathematically correct (linear scaling), it implies the protocol is negligible at high bandwidths. It might be worth noting that at 100 kbps, the *latency* bottleneck might shift from transmission time to processing time or propagation time, changing the dominant design constraint.

**3. Figure 6 Caption**
The caption describes the plot as "Overhead trajectory (log-linear)." Please verify the axis scales. If the X-axis (Fleet Size) is logarithmic and the Y-axis (Overhead) is linear, "semilog-x" is the standard terminology.

**4. Equation 10 (Geometric Approximation)**
The text notes that the geometric approximation overestimates P95 by 0-1 cycles. It would be helpful to explicitly state that this makes Eq. 10 a *conservative* design tool, which is a positive attribute for systems engineering.

---

### Overall Recommendation
**Minor Revision**

The paper is technically sound and presents a valuable contribution to the field of space systems engineering. The analytical models are robust and well-validated by the simulation. The only significant technical query relates to the timing feasibility of the consensus election mechanism under the specific constraints of the low-bandwidth backup link. Once this is clarified or corrected, the manuscript is suitable for publication.

---

### Constructive Suggestions

1.  **Refine the Election Analysis:** Add a small subsection or a detailed footnote breaking down the message flow of the Raft election under the 1 kbps constraint. If the 3-5s target is unachievable over RF, simply updating the recovery time to a more realistic value (e.g., 30s) would not invalidate the paper's main results, as the focus is on steady-state bandwidth sizing.
2.  **Beamwidth/Pointing Assumption:** Explicitly state the assumed antenna beamwidth for the coordinator. This validates the claim that 100 km position uncertainty does not result in link loss due to pointing errors, reinforcing the TDMA guard time argument.
3.  **Visualizing the Trade-off:** Consider adding a small "Design Guideline" box or table that summarizes the "Bandwidth vs. Robustness" trade-off between the Hierarchical and Sectorized Mesh architectures. This would highlight the practical utility of the work for system architects.
4.  **Future Work - Hybrid Architectures:** In the discussion, you might briefly mention the potential for a hybrid architecture (Hierarchical for command/control, Mesh for local collision avoidance) as a way to bridge the capability gaps identified in Table XI.