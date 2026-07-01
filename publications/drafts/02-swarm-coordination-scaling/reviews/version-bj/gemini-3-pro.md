---
paper: "02-swarm-coordination-scaling"
version: "bj"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

Here is the peer review for the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version BJ).

***

# Peer Review Report
**Journal:** IEEE Transactions on Aerospace and Electronic Systems
**Manuscript ID:** [Assigned by Editor]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Version:** BJ

## Review Criteria

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This paper addresses a critical and timely gap in the aerospace literature: the specific communication sizing requirements for autonomous mega-constellations ($10^3$--$10^5$ nodes). While existing literature covers routing in mega-constellations (Handley, Del Portillo) or swarm control algorithms (Brambilla, Dorigo), there is a distinct lack of work that bridges the gap between high-level control architectures and the byte-level engineering constraints of low-bandwidth space links.

The novelty lies in the derivation of closed-form "design equations" that link control topology to physical layer constraints (bandwidth, duty cycle, error rates). The distinction between "architecture-specific" overhead ($\sim5\%$) and "workload-dependent" overhead is a valuable contribution that clarifies where the engineering bottlenecks actually lie. The analysis of the "RF-backup" regime (1 kbps) is particularly significant for system reliability engineering, as this is often the mode that determines constellation survival during anomalies.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The methodology combines analytical derivation (queueing theory, Markov chains) with a custom cycle-aggregated Discrete Event Simulation (DES). This dual approach is robust. The authors are careful to define their atomic units (message-layer events) and justify their abstractions (e.g., the cycle-aggregated approach for speed). The use of the Gilbert-Elliott (GE) model to capture correlated link losses is appropriate for the space environment, where obstructions or pointing errors create bursty errors.

However, there is a slight disconnect regarding the physical layer validation. The authors acknowledge this as a "Validation Gap" (Section V-A) and suggest NS-3 as future work. While the message-layer analysis is sound, the assumption that MAC-layer contention can be purely abstracted via a scalar efficiency factor $\gamma$ (derived in Eq. 8) is a strong simplification, particularly when discussing the "Sectorized Mesh" where hidden-node problems might degrade $\gamma$ significantly more than in a TDMA hierarchy. The derivation of $\gamma \approx 0.95$ (conservatively 0.85) for TDMA is mathematically sound based on the slot structure provided.

### 3. Validity & Logic
**Rating: 5 (Excellent)**

The logic flow is rigorous. The paper systematically moves from defining the problem to deriving equations, validating them via DES, and then exploring sensitivity. The conclusions regarding the "Coordinator Bottleneck" are well-supported by the data. The finding that the stress-case unicast command load is not single-cycle deliverable (requiring a 22-cycle stagger) is a crucial operational insight that follows directly from the math.

The distinction between "link loss," "queue drop," and "deadline miss" is handled with precision. The analysis of the Gilbert-Elliott model is particularly strong, demonstrating why intra-cycle retransmission fails in bursty channels and correctly identifying inter-cycle recovery as the necessary mechanism. The "Joint Parameter Interaction" section (IV-D) effectively demonstrates that these variables can be treated independently, which simplifies the design process for future engineers.

### 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is generally well-written and dense with technical content. The structure follows a standard IEEE format. The "Key Notation" table is helpful. The distinction between the three workload profiles (Nominal, Event, Stress) is clear.

There are, however, areas where the density of information hinders readability. For instance, the "Sectorized Mesh" description in Section III-B-4 is somewhat fragmented between the model definition and the sensitivity analysis. Additionally, the distinction between "Ingress" and "Egress" constraints in the TDMA section could be visually mapped better; Table VI is excellent, but a timing diagram (Gantt chart style) of the TDMA superframe would significantly aid the reader in visualizing the 623ms margin.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors include a specific acknowledgment regarding the use of AI tools for "ideation," citing a specific methodology paper. This transparency is commendable and aligns with emerging best practices. No human subjects are involved. The research appears ethically sound.

### 6. Scope & Referencing
**Rating: 5 (Excellent)**

The scope is perfectly aligned with *IEEE TAES*. It bridges electronic systems (communications) and aerospace operations. The references are comprehensive, covering historical foundations (Kleinrock, Lamport), current constellation operations (Starlink, OneWeb), and relevant networking protocols (DTN, BPv7). The inclusion of recent swarm robotics literature ensures the control theory aspect is well-grounded.

***

## Major Issues

1.  **Sectorized Mesh MAC Efficiency ($\gamma$) Assumption:**
    In Section IV-F (Topology Comparison), the paper compares the Hierarchical approach (using TDMA, $\gamma=0.85$) against the Sectorized Mesh. However, the paper does not explicitly detail the MAC assumption for the Mesh. If the Mesh uses CSMA or ALOHA, $\gamma$ would drop significantly (likely $<0.4$) as traffic scales, potentially causing collapse earlier than the "bandwidth" limit suggests. The comparison in Fig. 10 and Table VIII seems to compare "Protocol Overhead" (bytes) but might under-penalize the Mesh for MAC inefficiency.
    *   *Action:* Please explicitly state the $\gamma$ value used for the Sectorized Mesh curves in Fig. 10. If it is assumed to be 0.85 (TDMA), justify how a distributed mesh achieves TDMA synchronization without the central coordinator. If it is ALOHA, ensure the overhead calculation accounts for the retransmissions required due to collisions, or explicitly state that the comparison is "byte-level only" and ignores MAC contention.

2.  **Coordinator Failure & Recovery Timing:**
    Section III-B-2 mentions a "RF-backup handoff" taking ~60s. However, Section IV-H-2 (Duty Cycle) mentions a "System Availability" of 99.5%. There is a subtle interplay here: if a coordinator fails while in the "Bad" GE state (correlated failure), the election messages might also be blocked.
    *   *Action:* Clarify if the "System Availability" calculation in Table IX accounts for the time to elect a new coordinator *during* a communication outage, or if it assumes the link is available for the election. If the failure is power-related (tumbling), the link is likely down. A brief discussion on "Double Fault" scenarios (Coordinator Failure + Link Outage) would strengthen the robustness analysis.

***

## Minor Issues

1.  **Abstract Clarity:** The phrase "Gilbert-Elliott inter-cycle recovery P95 in 4 cycles" is slightly opaque in the abstract without context. Consider rephrasing to "Recovery from bursty link errors (Gilbert-Elliott) requires 4 cycles (P95) using inter-cycle mechanisms."
2.  **Table I (Notation):** The symbol $S_{\text{eph}}$ is used in the text (Eq. 8) but is not explicitly defined in Table I. It appears to be the Status Report Size (256 B), but consistency would be helpful.
3.  **Equation 8 (TDMA Capacity):** The equation uses $S_{\text{eph}}$. Please confirm if this includes the overhead bits (preamble, header, CRC) or if those are accounted for in $\gamma$. The text says "Payload ($S_{\text{eph}} \times 8$)", implying $S_{\text{eph}}$ is pure data. Ensure the equation aligns with the derivation of $\gamma$ in Eq. 7.
4.  **Figure 4 (TDMA Comparison):** The y-axis label "Coordinator Utilization" should specify if this is "Time Utilization" or "Buffer Utilization." Based on the context, it is time/slot utilization, but clarification prevents ambiguity.
5.  **Section IV-A (Egress):** The text states "Egress: ~200 ms". Later it says "Total egress window... 0.82 s". It would be helpful to explicitly label the 200ms as "Required Active TX Time" to distinguish it from the "Available Window."

***

## Overall Recommendation
**Minor Revision**

This is a high-quality paper that offers significant practical value to the spacecraft operations and systems engineering communities. The derivation of sizing equations is rigorous, and the simulation results provide strong validation. The issues noted above are primarily regarding clarification of assumptions (specifically regarding the Mesh MAC and double-fault scenarios) rather than fundamental flaws in the analysis. With these clarifications, the paper will be an excellent addition to *IEEE TAES*.

***

## Constructive Suggestions

1.  **Add a TDMA Timing Diagram:** Replace or augment the text description in Section IV-A with a visual timing diagram of the 10s Superframe. Show the Ingress block, the Guard times, the Egress block (Broadcast), and the "Unallocated Margin." This will make the feasibility argument (Table VI) instantly intuitive.
2.  **Expand the "Validation Gap" into a "Roadmap":** Section V-A is honest but brief. Expand this to briefly describe *how* a packet-level simulation (e.g., NS-3) should be configured to validate these findings. For example, suggest specific propagation models or MAC protocols that would serve as the "ground truth" for the next phase of research.
3.  **Strengthen the "Sectorized Mesh" Context:** In the Introduction or Related Work, emphasize that the Sectorized Mesh is included primarily as a *comparative baseline* for overhead, rather than a fully optimized proposal. This protects the paper from criticism that the Mesh implementation is "naive" (e.g., lacking sophisticated compression or optimized gossip).
4.  **Operationalize the "Design Equations":** Consider adding a small "Summary Box" or a distinct subsection in the Conclusion titled "Guide for Practitioners." List the 3-4 critical equations (Ingress Capacity, AoI, Recovery Time) with a 1-sentence explanation of when to use them. This increases the paper's utility for working engineers.