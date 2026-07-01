---
paper: "02-swarm-coordination-scaling"
version: "bh"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Minor Revision"
---

Here is a rigorous peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version BH), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

***

# Peer Review Report

**Manuscript Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## Review Criteria

### 1. Significance & Novelty
**Rating: 4 (Good)**

The manuscript addresses a critical and timely gap in the literature: the scalability of coordination architectures for "mega-constellations" ($10^3$--$10^5$ nodes). While existing literature covers routing (ISLs) and small-scale swarms ($<100$ agents), there is a distinct lack of closed-form sizing relationships for the intermediate "constellation management" layer at this scale. The derivation of specific design equations for bandwidth, latency, and recovery under a hierarchical topology is a valuable contribution to the practitioner's toolkit.

The novelty lies in the specific focus on the *control plane* traffic (telemetry, commands, consensus) rather than the *user plane* (broadband data), which is often conflated in networking papers. The distinction between "architecture-specific" overhead ($\sim5\%$) and "workload-dependent" overhead is a significant insight that clarifies where the bottlenecks actually lie (command distribution vs. topology maintenance).

However, the significance is slightly tempered by the reliance on a static topology assumption for dynamic orbital environments. While the authors argue this is acceptable for steady-state sizing, the novelty would be enhanced by more rigorously addressing the dynamic maintenance of the hierarchy itself (cluster re-formation costs) beyond a brief mention in the limitations.

### 2. Methodological Soundness
**Rating: 5 (Excellent)**

The methodology is robust and well-executed. The authors employ a dual approach: analytical derivation (closed-form equations) backed by a custom Cycle-Aggregated Discrete Event Simulation (DES). The use of the DES to verify the implementation consistency of the equations (to $<0.1\%$) is excellent practice.

Specific strengths include:
*   **Gilbert-Elliott (GE) Model Implementation:** The handling of correlated losses is sophisticated. The authors correctly identify that intra-cycle retransmissions are ineffective during bad-state bursts when the coherence time exceeds the cycle time, and they provide a solid Markov-chain analysis for inter-cycle recovery.
*   **TDMA Frame Analysis:** The derivation of $\gamma$ (MAC efficiency) based on explicit slot structures (preamble, guard times, etc.) rather than an arbitrary constant adds significant credibility to the physical layer assumptions.
*   **Statistical Rigor:** The use of 30 Monte Carlo replications with bootstrap confidence intervals and the careful distinction between per-run aggregation and pooling for tail statistics (Section IV-B) demonstrates high statistical competence.

### 3. Validity & Logic
**Rating: 4 (Good)**

The conclusions are generally well-supported by the data. The central finding—that the hierarchy is sustainable at 1 kbps provided specific scheduling disciplines are used—is logically sound based on the presented math. The distinction between "unicast" and "broadcast" command distribution is crucial, and the paper rightly identifies unicast as the stress case that breaks single-cycle delivery.

There is one logical tension regarding the "Coordinator Failure Transient" (Section III-B-2). The paper claims a 3-5s election via Raft over optical ISL, but also notes a "RF-backup" mode where optical links might be down. If the coordinator fails *because* the node is tumbling or power-negative (common failure modes), the optical ISL is likely mispointed. The reliance on optical ISL for fast recovery seems optimistic for a "backup" scenario. The RF-backup recovery analysis ($\sim60$s) is present but could be emphasized more as the design-driving case for reliability, just as 1 kbps is the design-driving case for bandwidth.

### 4. Clarity & Structure
**Rating: 5 (Excellent)**

The manuscript is exceptionally well-written. The structure is logical, moving from problem definition to model, then results, and finally discussion. The "Practitioner Toolkit" approach—summarizing key equations in the Discussion—is very helpful for TAES readers.

The distinction between "Status Reports" (baseline) and "Protocol Overhead" ($\eta$) is defined clearly early on, preventing confusion. Figures are referenced appropriately, and the tables (particularly Table I: Notation and Table X: Schedulability) are information-dense and effective. The writing style is concise and professional.

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors include a specific acknowledgment regarding "AI-assisted ideation," citing the tools used (Claude, Gemini, GPT) and the scope of their use (ideation, not validation). This transparency meets and exceeds current standard ethical guidelines for AI disclosure. There are no apparent conflicts of interest or ethical concerns regarding the research content.

### 6. Scope & Referencing
**Rating: 4 (Good)**

The scope is well-aligned with TAES, specifically the "Space Systems" and "Command and Control" interest areas. The referencing is adequate, covering seminal works in swarm robotics (Brambilla, Dorigo), constellation operations (Wertz), and networking (Handley).

However, the paper would benefit from tighter integration with CCSDS standards beyond just the packet format. For instance, referencing CCSDS File Delivery Protocol (CFDP) regarding the "Class 2" reliable transfer for the large state handoffs would strengthen the operational realism. Additionally, more recent references on "Mega-Constellation" specific control algorithms (beyond routing) from 2020-2024 would strengthen the "Related Work" section.

---

## Major Issues

1.  **RF-Backup vs. Optical Dependency in Failure Recovery:**
    In Section III-B-2, the "Nominal handoff" relies on optical ISL (Gbps) for Raft consensus. However, the 1 kbps constraint is explicitly justified in Section III-E as the "design-driving worst case... during optical ISL outages." There is a logical disconnect here: if we are designing for the 1 kbps RF-backup case because optical is unavailable, we cannot assume optical is available for the coordinator election that might be triggered by that very outage. The paper should explicitly analyze the "Double Fault" scenario (Coordinator Failure + Optical Outage) as the true worst-case for availability, or clarify why these events are uncorrelated.

2.  **Unicast Command Latency & Operational Utility:**
    Table VIII shows that stress-case unicast commands require 22 cycles (220 seconds) to stagger. While the math is correct, the operational validity of a command loop with >3 minute latency for a "stress case" (potentially an emergency) is debatable. The paper should explicitly discuss whether this latency renders the architecture unsuitable for certain classes of emergency response (e.g., rapid collision avoidance requiring immediate thrusting), or if those commands are small enough to bypass the bulk queue.

---

## Minor Issues

1.  **Table II (Design Equation Scaling):** The footnote "AoI depends on $p_{exc}$ and $T_c$, not $C_{node}$" is slightly misleading. If $C_{node}$ is too low (causing congestion/drops), AoI *does* degrade. It should clarify "assuming sufficient capacity to avoid drops."
2.  **Section III-B-2 (Topology Dynamics):** The claim that "static cluster membership... is exact for co-planar formations" is a strong statement. Even in co-planar formations, drift and station-keeping maneuvers cause relative motion over a year. "Exact" should be changed to "Valid approximation."
3.  **Equation 8 (Gamma Derived):** The derivation assumes a specific preamble/guard size. It would be beneficial to state the assumed modulation order (e.g., BPSK/QPSK) that translates the 24 kbps rate into the symbol rate required for the guard time calculation.
4.  **Figure 6 (Overhead Decomposition):** The caption mentions "Summaries <1%". Visually, this is hard to verify. A small table inset or explicit percentage in the text would help.
5.  **Typos/Formatting:**
    *   Section III-A: "Palm--Khintchine" (spelling check).
    *   Table VI: The column header "Direction" is slightly ambiguous for "TX/RX turnaround". Perhaps "Mode" is better.

---

## Overall Recommendation
**Minor Revision**

The manuscript represents a high-quality contribution to the field of autonomous space systems. The analytical models are rigorous, and the simulation results provide strong validation. The primary reason for "Minor Revision" rather than "Accept" is the need to clarify the failure recovery logic in the RF-backup regime (Major Issue 1) to ensure the "worst-case" design philosophy is consistently applied throughout the paper. Once this logical tension is resolved and the operational implications of the unicast latency are clarified, the paper will be an excellent addition to TAES.

---

## Constructive Suggestions

1.  **Add a "Double Fault" Row to Table X:** Explicitly list the recovery time and overhead for a Coordinator Failure occurring during an Optical ISL outage. This completes the "worst-case" analysis.
2.  **Refine the "Sectorized Mesh" Comparison:** In Section IV-G, explicitly acknowledge that while the Mesh has higher overhead, it likely has lower latency for *local* neighbor-to-neighbor alerts (like collision avoidance) compared to the hierarchical path (Node -> Cluster -> Node). This adds nuance to the trade-off beyond just bandwidth.
3.  **Expand on "Command Prioritization":** Briefly mention how a priority queue (not currently modeled) would alleviate the 22-cycle delay for critical alerts vs. routine maintenance commands. This defends the architecture against the high latency criticism.
4.  **Visualizing the Design Envelope:** Consider adding a "Design Region" plot (e.g., $N$ vs. $C_{node}$) that shades the feasible region for Hierarchical vs. Mesh, highlighting where the 1 kbps constraint makes Hierarchy the *only* viable option.