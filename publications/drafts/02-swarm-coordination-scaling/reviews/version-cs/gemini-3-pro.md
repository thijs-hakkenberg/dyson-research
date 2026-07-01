---
paper: "02-swarm-coordination-scaling"
version: "cs"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-03-04"
recommendation: "Unknown"
---

Here is a rigorous peer review of the manuscript "Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms" (Version CS).

---

# Peer Review Report

**Journal:** IEEE Transactions on Aerospace and Electronic Systems
**Manuscript ID:** [Assigned by Editor]
**Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Version:** CS

## 1. Significance & Novelty
**Rating: 4 (Good)**
The paper addresses a critical gap in the literature: the lack of closed-form sizing relationships for coordination architectures in the $10^3$--$10^5$ node regime (mega-constellations). While existing literature covers small swarms or centralized management, this work provides a bridge for the "middle ground" of hierarchical autonomy. The derivation of a two-layer feasibility framework (byte budget vs. TDMA airtime) is a significant contribution for systems engineers. The novelty lies not in the invention of new protocols, but in the rigorous parameterization and sizing of existing concepts (Raft, TDMA, CCSDS framing) for this specific scale.

## 2. Methodological Soundness
**Rating: 5 (Excellent)**
The methodology is robust. The authors employ a multi-tiered approach: analytical derivation, cycle-aggregated Discrete Event Simulation (DES), and a dedicated slot-level timing simulator. The explicit separation of "Model C" (CCSDS-grounded) and "Model S" (simplified) is a strong methodological choice that prevents over-optimistic conclusions. The use of Gilbert-Elliott (GE) models to stress-test the TDMA schedule against correlated losses is appropriate. The "Validation Gap" section (V-A) is refreshingly honest about the lack of external hardware validation, which enhances credibility rather than diminishing it.

## 3. Validity & Logic
**Rating: 5 (Excellent)**
The internal logic is consistent. The transition from the 24 kbps infeasibility finding to the 30 kbps minimum and 35 kbps recommendation is mathematically sound and well-supported by the slot-structure analysis. The distinction between the logical 1 kbps budget and the physical link rate is clearly maintained. The handling of the "stress case" ($d=1$) as a bounding condition rather than a nominal operating point resolves potential concerns about unrealistic workload assumptions.

## 4. Clarity & Structure
**Rating: 4 (Good)**
The manuscript is dense but well-organized. The "Rate Ladder" (Table III) and the "Feasibility Test" (Algorithm 1) are excellent synthesis tools for the reader. However, the density of acronyms and parameters in the abstract and introduction can be overwhelming. The distinction between $\eta$ (protocol overhead) and $\eta_{total}$ is clear, but the reader must pay close attention to the definitions in Section III-E to follow the math.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement with a GitHub link (a strong plus for reproducibility). The acknowledgment of AI assistance in the ideation phase is transparent and complies with emerging publication standards.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The scope is well-suited for TAES. The referencing is extensive, covering standard astrodynamics texts (Vallado, Wertz), networking theory (Kleinrock, Bertsekas/Gallager equivalents), and relevant CCSDS standards. The inclusion of recent mega-constellation filings (SpaceX, Amazon) grounds the work in current industrial reality.

---

## Major Issues

1.  **Justification of Spatial Reuse ($R=3$) Validity**
    *   **Issue:** The paper asserts that a spatial reuse factor of $R=3$ is sufficient based on a free-space path loss argument ($>20$ dB isolation at 500 km).
    *   **Why it matters:** If $R=3$ is insufficient due to sidelobes or the "near-far" problem in dynamic orbits (where a distant cluster's transmitter might overpower a local receiver due to geometry), the fleet-level capacity collapses.
    *   **Remedy:** While full NS-3 simulation is out of scope, the authors should add a brief calculation or discussion regarding the *Interference-to-Noise Ratio (INR)* threshold assumed. Acknowledging that $R$ might need to be 7 (standard hexagonal cellular reuse) in worst-case geometries would be a prudent conservative bound to mention.

2.  **Unicast Command Latency Contextualization**
    *   **Issue:** The derivation of the 19-cycle stagger ($L_{cmd} \approx 190$ s) for unicast commands is mathematically correct, but its operational impact is under-discussed.
    *   **Why it matters:** A 3-minute latency for commanding specific nodes might be unacceptable for certain fault-recovery scenarios (e.g., cancelling a thruster firing).
    *   **Remedy:** Explicitly state in Section IV-E or Discussion that time-critical unicast interventions must bypass this queue (perhaps via the optical ISL) or that the system is architecturally limited to non-time-critical unicast updates via RF.

3.  **Raft Consensus Overhead Variability**
    *   **Issue:** Equation 6 presents consensus overhead, but the text notes it can range from 2.8% to 31% depending on $f_{decision}$.
    *   **Why it matters:** If a cluster becomes unstable (frequent leadership changes), the control channel could saturate, preventing the very commands needed to stabilize it.
    *   **Remedy:** Add a "stability condition" equation or statement defining the maximum leadership turnover rate before the control channel saturates (i.e., solve Eq. 6 for $f_{decision}$ where $\eta_{total} = 1$).

## Minor Issues

1.  **Abstract Density:** The abstract contains a very high density of numerical results. Consider moving the specific $\gamma$ values (0.745 vs 0.761) to the body to improve readability, focusing the abstract on the *implication* (24 kbps is insufficient).
2.  **Table II Footnotes:** The footnotes in Table II are quite long. Consider moving the detailed message size justification (Note 'd') into the main text of Section III-D.
3.  **Figure 2 Readability:** Ensure the axis labels on Figure 2 (Recovery CDF) are large enough to be legible when printed in the two-column format.
4.  **Clarification of "Information Rate":** In Table III, Step 1, explicitly reiterate that "20.2 kbps" includes the packet headers (network layer) but excludes the MAC/PHY overheads, to avoid confusion with "payload rate."

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a high-quality, rigorous engineering paper that provides valuable design tools for the aerospace community. The authors have successfully addressed the complexity of scaling coordination to $10^5$ nodes by decomposing the problem into logical byte budgets and physical time-slot constraints.

The most critical improvements needed are:
1.  Strengthening the caveats around spatial reuse ($R=3$).
2.  Clarifying the operational constraints imposed by the unicast command stagger.
3.  Ensuring the "stability boundary" for consensus traffic is explicitly defined.

Once these minor points are addressed, the paper will be a definitive reference for sizing future swarm coordination architectures.

## Constructive Suggestions (Ordered by Impact)

1.  **Add a "Safety Valve" for Unicast:** In the discussion of the 19-cycle stagger, suggest a "priority override" mechanism where a unicast command could displace the broadcast slot for one cycle if immediate safety action is required.
2.  **Expand on GE Parameter Selection:** While the sensitivity sweep in Fig. 2b is excellent, adding a sentence recommending that missions with specific orbit geometries (e.g., sun-synchronous vs. equatorial) perform ray-tracing to estimate their specific $p_{BG}$ would be helpful.
3.  **Visualizing the Rate Ladder:** Consider a small graphical inset or modification to Figure 3 that visually maps the "Rate Ladder" (Table III) onto the $\gamma$ curve, showing exactly where the "margin" opens up.
4.  **Algorithm 1 Refinement:** In Algorithm 1, Line 10, instead of just "Warning," suggest "Consider increasing $R_{PHY}$ or reducing $k_c$." This reminds the reader that cluster size is a tunable lever.