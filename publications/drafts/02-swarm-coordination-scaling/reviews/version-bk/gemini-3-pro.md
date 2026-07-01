---
paper: "02-swarm-coordination-scaling"
version: "bk"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-27"
recommendation: "Accept"
---

Here is a rigorous peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version BK), prepared for *IEEE Transactions on Aerospace and Electronic Systems*.

---

# Peer Review Report

**Manuscript ID:** [Assigned by Editor]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Target Journal:** IEEE Transactions on Aerospace and Electronic Systems

## Review Criteria

### 1. Significance & Novelty
**Rating: 5 (Excellent)**

This paper addresses a critical and timely gap in the literature: the scalability of coordination architectures for mega-constellations ($10^4$--$10^5$ nodes). While existing literature covers swarm robotics (typically small scale) and networking routing (ISL topology), there is a distinct lack of closed-form sizing equations for the *coordination* layer—specifically regarding byte-level budgets under constrained links.

The derivation of "design equations" that link physical layer constraints (TDMA airtime, bandwidth) with application-layer metrics (Age of Information, recovery time) is a significant contribution. The distinction between architecture-specific overhead ($\eta_0$) and workload-dependent traffic ($\eta_{cmd}$) provides a valuable heuristic for system architects. The focus on the "RF backup" regime (1 kbps) as the design-driving case is insightful and operationally grounded, distinguishing this work from purely optical-ISL networking papers.

### 2. Methodological Soundness
**Rating: 4 (Good)**

The methodology combines closed-form analytical derivations with a cycle-aggregated Discrete Event Simulation (DES) for verification. This dual approach is robust. The use of a Gilbert-Elliott (GE) model to capture correlated link losses is appropriate for the LEO environment (tumbling, shadowing), and the distinction between intra-cycle and inter-cycle recovery is handled well mathematically.

However, there is a slight disconnect regarding the physical layer validation. The authors acknowledge this as "future work" (Section V-A), but the reliance on a derived MAC efficiency factor ($\gamma$) is a heavy lift for the analytical section. While the derivation of $\gamma \approx 0.95$ (conservatively 0.85) in Section IV-A is logical, the paper would be stronger if it explicitly discussed the impact of Doppler shifts on guard times for LEO-to-LEO links more rigorously, rather than just stating a 1ms jitter margin. Additionally, the assumption of static cluster membership for a 1-year simulation of a mega-constellation is a strong simplification, though the authors do attempt to bound the error in Section V-B.

### 3. Validity & Logic
**Rating: 5 (Excellent)**

The logic flows clearly from problem statement to derivation to verification. The results are internally consistent. The cross-checks between the DES and the analytical models (Table V and Fig. 12) show impressive agreement ($<0.1\%$), which validates the implementation of the simulation against the equations.

The analysis of the "stress-case" command workload is particularly strong. Identifying that per-node unicast commands are not single-cycle feasible (requiring a 22-cycle stagger) is a crucial operational finding that validates the logic of the sizing equations. The argument that the coordinator bottleneck vanishes at $\geq 10$ kbps is well-supported by the data.

### 4. Clarity & Structure
**Rating: 4 (Good)**

The manuscript is generally well-written and dense with technical content. The structure follows a standard IEEE format. The distinction between "byte budget" and "schedulability" is made clearly.

*Minor Critique:* The notation is sometimes dense. For instance, the transition between discussing $\eta$ (overhead) and $\eta_{total}$ (utilization including baseline) requires careful reading. Table I (Notation) helps, but the text occasionally switches between these metrics rapidly. Figure 5 (TDMA frame) is referenced in the text but seems to be missing from the provided LaTeX source (or is perhaps Fig 3? The text references "Fig. 5" in context of TDMA, but the list includes `fig-tdma-comparison.pdf` as Fig 4). *Correction: The text references Section IV-A for TDMA, and Fig 4 is the relevant figure.*

### 5. Ethical Compliance
**Rating: 5 (Excellent)**

The authors provide a specific acknowledgment regarding AI assistance in the "Acknowledgment" section, citing a specific internal report on multi-model deliberation. This transparency is commendable and aligns with emerging publication standards. No obvious conflicts of interest or ethical lapses regarding data fabrication are apparent.

### 6. Scope & Referencing
**Rating: 5 (Excellent)**

The paper fits perfectly within the scope of *IEEE TAES*, specifically the intersection of space systems operations and electronic communication systems. The references are comprehensive, spanning classical queueing theory (Kleinrock), distributed algorithms (Lamport, Lynch), and modern constellation literature (Starlink, Kuiper, 3GPP/CCSDS standards). The inclusion of CCSDS Proximity-1 and BPv7 references demonstrates grounding in actual space protocols.

---

## Major Issues

1.  **TDMA Guard Time Justification:** In Section IV-A ("TDMA frame model"), the derivation of $\gamma$ assumes a guard time of 4.7ms based on propagation uncertainty and turnaround. In large swarms ($N=10^5$), relative velocities between intra-cluster nodes can be significant (km/s range). The paper mentions "Doppler" is not modeled. While the 1ms jitter margin might cover this, a more explicit calculation of the Doppler-induced timing error for LEO orbits is necessary to justify that 4.7ms is sufficient to prevent slot collisions, especially given the tight packing ($\gamma=0.95$).
2.  **Coordinator Failure Recovery:** Section III-B mentions a "Double-fault scenario" where RF-backup recovery takes ~60s. However, the impact of this 60s outage on the *rest* of the fleet's routing or collision avoidance is not fully explored. If a coordinator fails during a conjunction event, does the hierarchy fail safe? The paper touches on this in Section IV-B (AoI), but a more explicit link between the 60s recovery time and the "Time to Closest Approach" (TCA) safety margins would strengthen the operational relevance.

## Minor Issues

1.  **Figure Referencing:** Ensure all figures referenced in the text match the labels in the final PDF. The text flow regarding the TDMA structure is dense; a timing diagram (Gantt chart style) of the Superframe (Table VIII) would be very helpful visually.
2.  **Equation 10 (AoI):** The ceiling function is used. Please clarify if $T_c$ is a strict integer multiple or if this is an approximation.
3.  **Table IV (Sectorized Mesh):** The column "HB/node (B)" jumps from 160 to 320 to 640. Please double-check the arithmetic based on Eq. 7. For Cap=5, $(5-1)*32 = 128$, plus header? Eq 7 says $256 + \min(k_s-1, 10) \times 32$. The table values seem to represent *total* overhead bytes, but the label says "HB/node". Clarify if this column includes the status report (256B) or just Heartbeats.
4.  **Section IV-C (GE Model):** The assumption that "intra-cycle retry is ineffective... by model construction" is honest, but perhaps too conservative. In reality, a 10s cycle might see channel coherence times of 0.1s-1s. A brief sentence acknowledging that real-world performance might be *better* than the GE model prediction would be beneficial.
5.  **Typos:**
    *   Section I-A: "mid-2024" (ensure this is consistent with publication date).
    *   Table VI: "Drops" column for 50 kbps is 0. Is this exactly zero or just very low? (Presumably zero due to capacity > demand).

## Overall Recommendation

**Accept with Minor Revisions**

This is a high-quality paper that provides a necessary theoretical foundation for the operation of large-scale satellite swarms. The derivation of sizing equations is rigorous, and the simulation results support the analytical conclusions. The "stress-case" analysis of command traffic is a standout contribution that will be useful to system architects. The revisions requested are primarily for clarification and strengthening the physical layer justifications, which do not require new simulations.

## Constructive Suggestions

1.  **Add a TDMA Timing Diagram:** Replace or augment Table VIII with a visual timeline of the 10s cycle. Show the ingress slots, the guard times, and the egress block. This will make the "half-duplex" constraint and the "unicast stagger" problem immediately intuitive to the reader.
2.  **Expand Doppler Analysis:** In Section IV-A, add a brief calculation: $\Delta t = (v_{rel}/c) \times T_{prop}$. Show that for typical LEO relative velocities, this fits comfortably within the allocated guard time. This preempts criticism about physical layer realism.
3.  **Clarify "Sectorized Mesh" Overhead:** In Table IV, explicitly state in the caption or table header that the byte counts include/exclude specific headers to ensure the math is reproducible by the reader.
4.  **Strengthen the "Future Work" Section:** Explicitly mention that future packet-level simulations (NS-3) should investigate the "hidden terminal" problem if the cluster shape changes, which might degrade $\gamma$ further than the theoretical TDMA model suggests.