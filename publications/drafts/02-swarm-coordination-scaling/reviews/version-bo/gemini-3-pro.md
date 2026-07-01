---
paper: "02-swarm-coordination-scaling"
version: "bo"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

Here is a rigorous peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version BO), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review Report

**Manuscript Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## Review Criteria

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This manuscript addresses a critical and timely gap in the literature: the scalability of coordination architectures for "mega-constellations" ($10^4$--$10^5$ nodes). While existing literature covers routing (networking) or small-scale formation flying (GNC), there is a distinct lack of rigorous sizing models for the *coordination layer*—specifically the command and control (C2) traffic overhead required to maintain fleet coherence.

The derivation of closed-form sizing equations (the "three feasibility layers") is a significant contribution. The distinction between architecture-specific overhead ($\eta_0 \approx 5\%$) and workload-dependent traffic ($\eta_{cmd}$) provides a valuable heuristic for system architects. The focus on the "RF-backup" regime (1 kbps) as the design-driving constraint is a novel and practical insight, moving beyond the optimistic assumption that optical inter-satellite links (ISLs) will always be available. This work will likely serve as a foundational reference for sizing future autonomous constellation management systems.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The methodology combines analytical derivation with a custom Cycle-Aggregated Discrete Event Simulation (DES). The approach is generally robust. The authors effectively use the DES not to "discover" the overhead (which is arithmetic) but to validate the interaction of queueing dynamics, Gilbert-Elliott (GE) losses, and protocol latencies—interactions that are difficult to capture in pure closed-form equations.

However, there is a slight disconnect regarding the Physical Layer (PHY) validation. The authors explicitly state that PHY validation (MAC contention) is future work, yet they rely heavily on a derived MAC efficiency factor ($\gamma \approx 0.85-0.95$) to claim feasibility. While the derivation of $\gamma$ in Section IV.A is logical based on TDMA frame structures, the assumption of perfect synchronization and zero contention during the "RF-backup" mode (where GNSS might be denied) is a strong one. The paper acknowledges this but could benefit from a more critical discussion of how $\gamma$ degrades if synchronization slips.

### 3. Validity & Logic
**Rating: 5 (Excellent)**

The logic flow is tight and persuasive. The decomposition of the problem into byte-budget, MAC efficiency, and airtime scheduling is rigorous. The authors are careful to distinguish between "link loss" (PHY) and "queue drop" (buffer overflow), and the analysis of the Gilbert-Elliott model is mathematically sound.

The counter-intuitive finding that intra-cycle retransmission is ineffective under correlated fading (Section IV.C) is well-supported by the data and provides a strong logical basis for the proposed inter-cycle recovery strategy. The comparison against reference baselines (Centralized and Global-State Mesh) effectively brackets the performance of the hierarchical approach, demonstrating that it is the only viable option for the $10^5$ node scale under bandwidth constraints.

### 4. Clarity & Structure
**Rating: 4 (Good)**

The paper is written with high technical density but remains readable. The notation is consistent (Table I is helpful), and the distinction between the three workload profiles (Nominal, Event, Stress) helps contextualize the results.

There are minor structural issues. The "Results" section (Section IV) is very long and contains some derivations (e.g., the TDMA frame calculation in IV.A) that might fit better in the System Model or a dedicated Analysis section. Additionally, the distinction between "Analytical" and "DES" results is sometimes blurred in the text, though the tables usually clarify this. The abstract is dense with numbers; slightly streamlining it to focus on the *implications* of those numbers would improve readability.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors include a specific acknowledgment regarding the use of AI tools for "ideation," citing a specific internal report. This transparency aligns with emerging academic standards. There are no apparent conflicts of interest or ethical concerns regarding the research subject matter.

### 6. Scope & Referencing
**Rating: 4 (Good)**

The scope is well-aligned with *IEEE TAES*. The references are a good mix of classical networking theory (Kleinrock, Lamport), space systems engineering (Wertz, Vallado), and recent mega-constellation literature (Handley, Del Portillo).

One minor gap is the lack of comparison to specific Delay Tolerant Networking (DTN) bundle protocol overheads. While BPv7 is cited, the paper assumes a generic header/payload structure. A brief mention of how standard CCSDS/DTN overheads might impact the $\eta$ values would strengthen the practical applicability of the results.

---

## Major Issues

1.  **TDMA Synchronization in RF-Backup Mode:**
    The paper identifies the 1 kbps RF-backup mode as the design-driving case. It also relies on a high MAC efficiency ($\gamma \approx 0.85$) achieved via TDMA. However, the RF-backup mode is most likely to be needed exactly when the primary systems (optical ISL, potentially GNSS) are compromised. If GNSS is denied, maintaining the microsecond-level synchronization required for tight TDMA slots becomes a distributed clock synchronization problem. The paper mentions a "sync beacon," but does not rigorously analyze the drift/jitter budget for a $10^5$ node swarm relying solely on RF beacons. If synchronization fails, the system reverts to Slotted ALOHA ($\gamma \approx 0.36$), where the stress-case workload ($\eta_{total} \approx 67\%$) would cause collapse. This risk needs to be explicitly bounded.

2.  **Coordinator Failure & Recovery Timeline:**
    Section III.B.2 mentions a "Double-fault scenario" (Coordinator failure + Optical outage) requiring ~160s for recovery via RF. This is a critical vulnerability window. The analysis assumes the *new* coordinator has perfect state immediately after the "seed handoff." In reality, the new coordinator must rebuild the cluster state from scratch (receiving reports from 100 nodes). Does this state-rebuilding phase cause a spike in command latency or a risk of collision during the handover? The transient dynamics of this handover deserve a more detailed look or at least a clearer set of assumptions.

---

## Minor Issues

1.  **Equation (1) Notation:** In Eq. (1), $\rho = \frac{\lambda}{\mu_s}$. Standard queueing notation usually defines $\mu$ as the service rate. Ensure the units match (messages/sec vs. processing time). The text later clarifies $\mu_s = 1000$ msg/s, which is correct, but the definition of $\rho$ as utilization should be explicit.
2.  **Figure 2 (Architecture Diagram):** The text describes a four-level hierarchy, but the figure caption mentions "Ground -> Regional -> Cluster -> Node." Ensure the diagram visualizes the *data flow* direction clearly, particularly for the summary aggregation moving up the chain versus commands moving down.
3.  **Table VII (Duty Cycle):** The "Power Var." and "Handoff Success" columns are derived from models not fully detailed in the text. A brief footnote explaining the derivation of the Power CV (Coefficient of Variation) would be helpful for reproducibility.
4.  **Section IV.A (TDMA Frame):** The calculation $2112 / 24000 = 88.0$ ms is correct. However, the text says "Guard time comprises propagation uncertainty... at 500 km... differential propagation is ~1.7 ms." Is 500 km the maximum range or the average? If it's the cluster diameter, the max range to the coordinator is 250km? Please clarify if this is worst-case slant range.
5.  **Typos/Formatting:**
    *   Section III.B.2: "RequestVote: 100 B broadcast... quorum = $k_c/2 + 1$". Clarify if this is Raft-specific terminology (it appears to be).
    *   Table IV: "P99 AoI (s)" column—the value 441 matches the text, but the table header says "P99 AoI". Ensure consistency in capitalization.

---

## Overall Recommendation

**Minor Revision**

This is a high-quality paper that makes a strong contribution to the field of space systems engineering. The analytical models are rigorous, and the simulation results provide good validation. The "Major Issues" identified above do not require new simulations, but rather a more transparent discussion of the risks associated with synchronization loss in the backup mode and the transient dynamics of coordinator handover. Addressing these points will make the paper robust enough for publication in *TAES*.

---

## Constructive Suggestions

1.  **Add a "Synchronization Sensitivity" Subsection:** In Section IV (perhaps near the TDMA discussion), add a short paragraph or graph estimating the impact of clock drift on $\gamma$. If the guard time must increase from 4.7ms to 20ms due to clock drift in a GNSS-denied environment, how much does $\gamma$ drop? This would robustly address the feasibility of the RF-backup mode.
2.  **Clarify "State Rebuild" vs. "Handoff":** Explicitly distinguish between the time to elect a new coordinator (Raft) and the time for that coordinator to become *operationally effective* (i.e., receiving fresh ephemeris from all members). This adds nuance to the availability argument.
3.  **Expand on DTN Overhead:** Briefly discuss how the 256-byte status report aligns with CCSDS Bundle Protocol headers. If BPv7 adds ~100 bytes of overhead, does the 1 kbps budget still hold? A simple sentence stating that "Message sizes assume compressed headers or raw Space Packet Protocol; full DTN bundling may require increasing $C_{node}$ to 1.5 kbps" would protect the paper from criticism regarding protocol overheads.
4.  **Visualizing the Feasibility Layers:** Consider a figure that visualizes the "Three Feasibility Layers" (Byte, MAC, Airtime) as a Venn diagram or a sieve, showing how the Stress Unicast workload passes the first two but is caught by the third. This would be a powerful graphical abstract for the paper.