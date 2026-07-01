---
paper: "02-swarm-coordination-scaling"
version: "cm"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-03"
recommendation: "Unknown"
---

Here is a rigorous peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version CM), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review Report

**Manuscript ID:** [Assumed Version CM]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## 1. Significance & Novelty
**Rating: 4 (Good)**
The paper addresses a critical gap in the literature: the "missing middle" between small-scale swarm robotics ($N < 100$) and massive constellation networking ($N > 10,000$). While mega-constellation routing is well-studied, the specific problem of *command and control coordination* (distinct from user data routing) under tight bandwidth constraints is novel. The derivation of closed-form sizing equations for this specific niche is a significant contribution for systems engineers.

## 2. Methodological Soundness
**Rating: 5 (Excellent)**
The methodology is rigorous. The authors employ a multi-fidelity approach: analytical derivation, Discrete Event Simulation (DES) for message-layer statistics, and a slot-level TDMA simulator for physical-layer timing. The explicit separation of "byte budget" (Layer 1) and "airtime schedulability" (Layer 2) is a robust framework. The inclusion of a Gilbert-Elliott (GE) model to test correlated losses adds necessary realism often missing in theoretical swarm papers.

## 3. Validity & Logic
**Rating: 4 (Good)**
The internal logic is consistent. The transition from Version CM's earlier drafts (implied by the prompt's context regarding $\gamma$) to the current CCSDS-anchored values strengthens validity. The identification of the "stress case" as a bounding condition rather than a nominal operating mode is logically sound. However, the reliance on a specific, unverified GE parameterization ($p_{BG}=0.50$) for the primary results remains a slight vulnerability, though the sensitivity sweep mitigates this.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The manuscript is exceptionally well-structured. The distinction between the four operating modes (Normal, Coord Channel, RF-Backup, Per-node budget) is handled with precision in Table II, preventing common confusion. The "Rate Ladder" (Table IV) is a standout pedagogical tool that clearly communicates the derivation path.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear data availability statement pointing to a repository. The AI disclosure is transparent and specific ("AI-assisted ideation... no AI tools used to generate results").

## 6. Scope & Referencing
**Rating: 4 (Good)**
The literature review covers the necessary bases (swarm robotics, CCSDS standards, delay-tolerant networking). The connection to existing standards (CCSDS Proximity-1) is a strong point. The paper fits well within the scope of TAES, specifically the intersection of autonomy and communications.

---

## Major Issues

1.  **Validation of the Gilbert-Elliott (GE) Parameters for ISL**
    *   **Issue:** The paper relies heavily on a GE model with $p_{BG} = 0.50$ (mean bad state duration ~2 cycles) to demonstrate the infeasibility of intra-cycle ARQ at 24 kbps. While the sensitivity sweep (Fig. 6b) is excellent, the specific choice of 0.50 is justified only by geometric arguments about solar panels and tumbling.
    *   **Why it matters:** If the real ISL channel is faster-fading (e.g., multipath from solar panel reflection rather than blockage), intra-cycle ARQ might actually work at lower rates. Conversely, if blockage is longer (thermal stabilization), the P95 recovery time could be much worse.
    *   **Remedy:** Explicitly state that $p_{BG}=0.50$ is a *design assumption* rather than a measured characteristic in the Abstract and Conclusion. The text currently treats the "ARQ infeasibility" as a hard fact, but it is conditional on the assumed coherence time.

2.  **The "Thundering Herd" Recovery Analysis**
    *   **Issue:** Section III-B mentions that if a coordinator fails, 100 nodes attempt Raft election via Slotted ALOHA. The analysis cites a throughput of 900 bps and a 140-160s recovery.
    *   **Why it matters:** Slotted ALOHA collapses under heavy load ($G > 1$). With 100 nodes reacting simultaneously to a timeout, the channel load $G$ will initially be massive. The binary exponential backoff mentioned is crucial, but the paper does not specify the initial backoff window size. If the window is too small, the collision rate will be near 100%, and the 160s estimate will be optimistic.
    *   **Remedy:** Provide the specific backoff parameters used in the calculation or simulation. Verify if the 160s estimate accounts for the initial collision storm or assumes steady-state throughput.

3.  **Unicast Command Latency Contextualization**
    *   **Issue:** The result that unicast commands require a 19-cycle stagger (190s) is mathematically sound but operationally alarming.
    *   **Why it matters:** A 3-minute latency for individual commands might be unacceptable for certain "autonomous" swarm behaviors (e.g., collision avoidance requiring specific delta-v vectors per node).
    *   **Remedy:** The paper briefly mentions using broadcast for safety-critical commands. Please expand on this operational concept. Explicitly discuss *which* commands are acceptable at 190s latency (e.g., orbit raising) versus which must use the broadcast slot (e.g., "drift apart" alerts).

## Minor Issues

1.  **Table I (Notation):** The symbol $q$ is defined as "Unicast fraction," but in Table X (Duty Model), it is listed as 0.1 for Collision Avoidance. Clarify if this means 10% of nodes receive unicast commands, or 10% of commands are unicast.
2.  **Section IV-A (Coordinator Capacity):** The text states "Regional ingress... are not capacity-constrained." A brief sentence explaining *why* (e.g., higher bandwidth link or fewer messages) would help the reader who hasn't memorized Table II.
3.  **Fig. 5 (Margin Sensitivity):** The caption mentions "Star" and "Diamond" markers, but ensure these are clearly visible in the final high-resolution print.
4.  **Algorithm 1:** Line 2 adds `0.205`. It would be clearer to write `+ \eta_{baseline}` or similar, referencing the 20.5% derived earlier, to avoid "magic numbers" in the pseudocode.

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a high-quality, rigorous manuscript that makes a valuable contribution to the field of spacecraft swarm engineering. The authors have successfully navigated the complexity of cross-layer design, providing a framework that links byte-level protocols to physical-layer timing.

The "Two-Layer Feasibility Framework" is a robust tool for systems engineers. The rigorous derivation of $\gamma$ (0.76) from CCSDS standards, replacing generic efficiency assumptions, adds significant credibility. The distinction between the "Stress Case" (46% overhead) and routine operations (5-10%) resolves potential concerns about the viability of the architecture.

The requested revisions are primarily regarding the contextualization of assumptions (specifically the GE channel model and the operational impact of unicast latency) rather than flaws in the derivation. Once these clarifications are made, the paper will be an excellent addition to the journal.

---

## Constructive Suggestions

1.  **Strengthen the "Validation Gap" Section:** You acknowledge the lack of external ISL data. I suggest adding a specific "Call to Action" for experimentalists. List exactly *what* data points a CubeSat mission should log to validate your model (e.g., "We recommend future missions log inter-packet arrival times at 10ms resolution to characterize $p_{BG}$"). This increases the paper's citation potential.
2.  **Visualizing the Stagger:** A small timing diagram illustrating the "19-cycle stagger" for unicast commands would be very helpful. Visualizing how the coordinator interleaves these commands over 190 seconds would make the operational constraint immediately intuitive.
3.  **Clarify "Safe Mode" vs. "RF Backup":** The text distinguishes these, but the terms are close. Perhaps explicitly label the 1 kbps constraint as the "Survival Bandwidth" to emphasize its criticality.