---
paper: "02-swarm-coordination-scaling"
version: "bw"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

# Peer Review: IEEE Transactions on Aerospace and Electronic Systems

**Manuscript Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Version:** BW

## 1. Significance & Novelty
**Rating: 5**

This manuscript addresses a critical and timely gap in the literature: the scalability of command and control (C2) architectures for mega-constellations ($10^4$--$10^5$ nodes). While existing literature covers swarm robotics (typically $N<100$) or networking routing (ISL/DTN), there is a paucity of work rigorously quantifying the *coordination* overhead for autonomous operations at the scale of Starlink or Kuiper, particularly under degraded conditions.

The novelty lies in the derivation of closed-form "design equations" specifically for the RF-backup regime (1 kbps). The distinction between "byte budget feasibility" and "TDMA airtime schedulability" (specifically regarding the unicast stagger analysis in Section IV-A) is a significant contribution that highlights non-obvious bottlenecks in large-scale fleet management. This work moves beyond qualitative architecture discussions to provide systems engineers with hard sizing constraints.

## 2. Methodological Soundness
**Rating: 4**

The methodology is generally robust, employing a tripartite approach: analytical derivation, cycle-aggregated discrete event simulation (DES), and a slot-level TDMA simulator.
*   **Strengths:** The use of a Gilbert-Elliott (GE) model to capture correlated channel losses is appropriate for the LEO environment (tumbling/obstruction). The separation of the DES (for fleet-wide statistics) and the slot-level simulator (for timing validation) is a pragmatic approach to handling the computational load of $10^5$ nodes.
*   **Weaknesses:** The DES relies on a "fluid server" model for coordinator ingress (Section III-A), while the analytical section proves that TDMA slotting is the binding constraint. While the authors acknowledge this and use the slot-level simulator to validate, the paper would benefit from a more explicit discussion of where the fluid approximation fails (e.g., does it underestimate jitter?). Additionally, the assumption of static cluster membership (Section III-B) is a strong simplification for non-coplanar constellations, though the authors attempt to bound the error.

## 3. Validity & Logic
**Rating: 5**

The conclusions are logically sound and well-supported by the data presented.
*   The argument that the 1 kbps RF-backup mode is the "design-driving edge case" is convincing. If the system cannot survive an optical ISL outage, it is not autonomous.
*   The comparison between the Hierarchical topology and the Sectorized Mesh is handled fairly. The authors explicitly define the functional scope (equivalent state awareness) and demonstrate that achieving cluster-wide awareness via mesh at 1 kbps is mathematically impossible due to the $O(N)$ vs $O(k_c)$ scaling differences.
*   The identification of the "Unicast Stagger" (22 cycles) as a Layer 3 constraint is a key insight. It logically follows that if bandwidth is fixed, serialization delay for unique commands must increase, but quantifying this specifically for the TDMA frame is valuable.

## 4. Clarity & Structure
**Rating: 4**

The paper is well-organized and written with high technical density.
*   **Strengths:** Tables I (Notation) and V (TDMA Budget) are excellent references. The distinction between $\eta$ (protocol overhead) and $\eta_{total}$ (including baseline) is maintained consistently.
*   **Weaknesses:** The Abstract is extremely dense with numerical results, making it somewhat difficult to parse on a first read. In Section IV-A, the transition between discussing "Coordinator Ingress" and "Command Egress" could be smoother; the distinction between Type 1 (broadcast) and Type 2 (unicast) commands is critical but appears somewhat late in the text.

## 5. Ethical Compliance
**Rating: 5**

The authors provide a clear acknowledgment of AI-assisted ideation (Claude, Gemini, GPT) in the Acknowledgment section, citing a specific internal methodology paper. This aligns with emerging transparency standards. There are no human subject concerns. The research appears ethically sound.

## 6. Scope & Referencing
**Rating: 5**

The paper is squarely within the scope of *IEEE TAES*. It bridges the gap between astrodynamics (constellation sizing), communications (link budgets/MAC), and systems engineering. The references are comprehensive, covering historical concepts (O'Neill), current operational systems (Starlink, OneWeb), and relevant theoretical foundations (swarms, AoI).

---

## Major Issues

1.  **Justification of the 1 kbps Constraint:**
    While the authors state that 1 kbps is the "RF-backup regime," this value seems aggressively low even for a backup mode in modern S-band or UHF systems, which often achieve 9.6--32 kbps even with omni-directional antennas. Since the entire bottleneck analysis (TDMA requirements, ARQ infeasibility) hinges on this 1 kbps limit, the paper needs a stronger physical-layer justification for *why* 1 kbps is the correct floor. Is this driven by link budget closure at maximum slant range with tumbling spacecraft (0 dBi gain)? Explicitly stating the link budget assumptions that lead to 1 kbps would strengthen the premise.

2.  **Static Topology vs. Cross-Plane Dynamics:**
    In Section III-B, the authors assume static cluster membership. For mega-constellations (e.g., Walker-Delta patterns), cross-plane links are highly dynamic. While the authors claim re-association overhead is $<0.5\%$, this dismisses the *latency* and *risk* of topology churn. If a coordinator fails *during* a high-churn period, the recovery time might exceed the calculated values. The authors should either simulate a dynamic scenario or provide a more rigorous analytical bound on why topology churn does not invalidate the "Design Equations."

3.  **Fluid-Server vs. TDMA Discrepancy:**
    The DES uses a fluid-server model (Section III-A), but the results emphasize that TDMA slotting is required (Section IV-A). A fluid model inherently underestimates the "wait-for-slot" latency. While Table VII shows latency breakdown, it is unclear if the DES results for AoI (Table VI) incorporate the average $T_c/2$ wait time inherent to TDMA, or if they only reflect fluid processing. If the DES ignores framing latency, the AoI results might be optimistic. This needs clarification.

## Minor Issues

*   **Abstract:** The sentence "Gilbert-Elliott inter-cycle recovery P95 in 4 cycles" is telegraphic and hard to parse. Consider rephrasing for flow.
*   **Table I:** $S_{eph}$ is listed as 256 B. Is this the payload only, or does it include the MAC headers discussed in Section IV-A? Consistency in "Message Size" vs "Frame Size" is needed.
*   **Section IV-A (Eq. 9):** The derivation of $\gamma = 0.949$ is clear, but the decision to revert to 0.85 is described as "conservative." It would be helpful to list exactly what the delta (0.099) represents (e.g., guard bands, pilot tones).
*   **Figure 5 (Unicast Stagger):** The caption mentions "crosses" for simulation validation, but they may be hard to see if the figure is printed in black and white. Ensure markers are distinct.
*   **Typos/Grammar:**
    *   Section I-A: "Expansions to 42,000+ satellites... create qualitatively different coordination problems" - correct, but perhaps cite the specific FCC filings for the 42k number to be precise.
    *   Section IV-C: "GE intra-cycle recovery 27% (vs. 87.5% i.i.d.)" - Clarify if this is per-packet or per-cycle success probability.

## Overall Recommendation
**Minor Revision**

The manuscript represents a high-quality contribution to the field of space systems engineering. The analytical framework is novel and the results are non-intuitive (specifically the ARQ infeasibility and unicast stagger). The major issues listed above regarding the 1 kbps justification and fluid/TDMA discrepancy can be addressed with textual clarifications and perhaps one additional analytical paragraph, without requiring new simulation runs.

## Constructive Suggestions

1.  **Add a "Link Budget Justification" Subsection:** Briefly detail the link budget parameters (TX power, slant range, frequency, antenna gain, noise figure) that result in the 1 kbps constraint. This validates the "Design-Driving" premise.
2.  **Clarify DES Latency Accounting:** Explicitly state in Section III-A whether the DES adds a random $[0, T_c]$ delay to messages to simulate TDMA framing wait times. If not, acknowledge this as a source of AoI optimism.
3.  **Enhance the Command Type Discussion:** Move the definition of Type 1 (Broadcast) vs. Type 2 (Unicast) commands earlier, perhaps to Section III-E (Traffic Accounting). This distinction is vital for understanding the stress-case results.
4.  **Visualize the Superframe:** Figure 4 (TDMA comparison) is good, but a diagram showing the actual *structure* of the 10s Superframe (Ingress slots -> Guard -> Egress Broadcast -> Egress Unicast) would make the "Unicast Stagger" problem immediately intuitive to the reader.