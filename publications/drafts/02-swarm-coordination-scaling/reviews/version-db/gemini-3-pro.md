---
paper: "02-swarm-coordination-scaling"
version: "db"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-05"
recommendation: "Unknown"
---

**Review of Manuscript Version DB**
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty
**Rating: 5 (Excellent)**
This manuscript addresses a critical and widening gap in aerospace literature: the "missing middle" between small-scale swarm robotics (10-100 agents) and centralized mega-constellation management. As commercial constellations target $10^4$--$10^5$ nodes, the scalability of coordination architectures becomes a primary design driver. The derivation of closed-form sizing equations that link byte-level protocol overhead to physical-layer TDMA constraints is a significant contribution. The novelty lies in the rigorous "bottom-up" parameterization of the slot efficiency ($\gamma$) based on CCSDS standards, moving beyond the arbitrary efficiency factors often found in high-level system studies.

## 2. Methodological Soundness
**Rating: 5 (Excellent)**
The methodology has matured significantly in this version. The transition to a "Two-Test" feasibility framework (Test A: Byte Budget; Test B: TDMA Airtime) provides a robust analytical structure. The explicit derivation of $\gamma$ via "Model C" (CCSDS Proximity-1 framing) rather than the simplified "Model S" adds necessary rigor. The use of Discrete Event Simulation (DES) for distributional analysis (buffer tails) while relying on closed-form equations for mean-value sizing represents a proper use of simulation tools. The distinction between code verification (Tier 1) and external validation (Tier 3) is intellectually honest and methodologically sound.

## 3. Validity & Logic
**Rating: 5 (Excellent)**
The logical progression from link budget $\to$ per-node allocation $\to$ protocol overhead $\to$ TDMA schedulability is tight. The paper effectively addresses previous concerns regarding workload realism by introducing the campaign duty factor ($d$), allowing for a clear distinction between continuous background traffic and episodic stress cases. The identification of the "ARQ coupling" effect—where intra-cycle retransmissions become structurally ineffective at low data rates due to slot timing—is a strong, counter-intuitive finding that validates the need for the detailed slot-level analysis.

## 4. Clarity & Structure
**Rating: 4 (Good)**
The manuscript is dense, packing a significant amount of mathematical derivation and operational logic into the page limit. The "Rate Ladder" (Table IV) is an excellent pedagogical device that clarifies the relationship between information rate, overhead, and required PHY rate. However, some figure captions (e.g., Fig. 3, Fig. 4) are excessively long and contain discursive text that belongs in the body. The distinction between Model S (simplified) and Model C (CCSDS) is handled well, but the authors must ensure casual readers do not accidentally use Model S equations for design.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement pointing to a repository with source code and datasets. The disclosure regarding AI-assisted ideation/editing is transparent and consistent with current IEEE guidelines.

## 6. Scope & Referencing
**Rating: 5 (Excellent)**
The literature review is comprehensive, bridging the gap between classical networking (queueing theory, ALOHA), space standards (CCSDS, ECSS), and modern autonomy (Raft, swarm logic). The references are appropriate for TAES.

---

## Major Issues

1.  **Interference and Spatial Reuse Assumptions ($R=3$)**
    *   **Issue:** The paper assumes a spatial reuse factor of $R=3$ is sufficient to close the link budget ($C/I > 20$ dB) based on a "back-of-envelope" calculation involving patch antenna patterns.
    *   **Why it matters:** In a dense shell (e.g., 550 km), sidelobe interference from adjacent clusters could drastically raise the noise floor, invalidating the link budget that underpins the 1 kbps allocation. If $R$ needs to be 7 or 12, the available bandwidth per cluster drops proportionally.
    *   **Remedy:** While a full antenna simulation is out of scope, the authors should add a sensitivity note or a "Warning" block in the Discussion. Explicitly state that $R=3$ is a lower bound and that realistic antenna sidelobes might require higher $R$ (and thus higher $F$ or lower throughput).

2.  **Operational Risk of "Suspended" Hierarchy**
    *   **Issue:** The paper states that during RF-backup (UHF), hierarchical coordination is "suspended" and nodes enter safe-hold. The analysis of the "Thundering Herd" Raft election upon recovery is presented, but the operational risk of this suspension is under-emphasized.
    *   **Why it matters:** If a cluster loses optical lock and the coordinator fails simultaneously (the triple fault), the swarm is effectively lobotomized for ~300+ seconds. For collision avoidance, this latency is critical.
    *   **Remedy:** In Section III-B (Coordinator Failure Transient), explicitly discuss the *safety implications* of this 300s gap. Is the passive safety of the orbit sufficient to survive this window without active coordination? A brief sentence confirming orbital safety margins during this "dead time" is needed.

## Minor Issues

1.  **Figure Caption Length:** The captions for Figure 3 and Figure 4 are paragraphs. Move the interpretative text to the main body and keep captions descriptive.
2.  **Gamma Notation:** In Table I, $\gamma$ is defined with specific values for 24, 30, and 35 kbps. Ensure the text consistently uses the notation $\gamma(R_{PHY})$ to reinforce that this is a function, not a constant.
3.  **Equation 11 Layout:** The fraction in Equation 11 is slightly cluttered. Consider defining the denominator terms ($T_{overhead} = T_{FEC} + ...$) separately for visual clarity.
4.  **Abstract Clarity:** The phrase "CCSDS Proximity-1 framing anchors $\gamma \approx 0.70$--$0.76$" is excellent. Consider adding "(Model C)" to the abstract to align with the terminology used throughout the paper.

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a high-quality manuscript that provides a rigorous, standards-based framework for sizing communication in large space swarms. The authors have successfully addressed the limitations of previous "toy models" by integrating CCSDS framing overheads, realistic campaign duty cycles, and correlated channel losses into a cohesive set of design equations.

The "Two-Test" framework is a valuable contribution to the field, offering a practical tool for systems engineers. The analysis of the "stress case" ($d=1$) vs. routine operations ($d=0.1$) resolves prior concerns about workload realism. The paper is technically sound, and the validation approach (distinguishing between internal verification and external validation) is commendable.

The requested revisions are primarily cautionary: ensuring the assumptions regarding spatial reuse ($R=3$) and the operational risks of the backup mode are clearly contextualized so that practitioners do not apply the equations outside their valid envelope.

## Constructive Suggestions

1.  **Strengthen the "What-If" GE Guidance:** In Section IV-C, you describe the GE model as a "what-if design tool." To make this more actionable, consider adding a small lookup table or bulleted list suggesting reasonable $p_{BG}$ / $p_{GB}$ starting points for different orbital regimes (e.g., "Tumbling/Safe Mode," "Stabilized/Station-Keeping," "Maneuvering").
2.  **Visualizing the Rate Ladder:** Table IV is great. It might be even more impactful as a simple flow-chart figure (Information Rate $\to$ +Overhead $\to$ +Half-Duplex $\to$ +Margin $\to$ Recommended PHY), visually demonstrating how 20 kbps of data becomes a 35 kbps requirement.
3.  **Clarify "Logical" vs "Physical" Link:** In the Introduction or System Model, reinforce that the "1 kbps per node" is a *logical traffic policing* limit, not a physical link capability. This prevents confusion about why a 35 kbps link is used for 1 kbps of traffic. (Table III does this well, but a mention in the text would help).