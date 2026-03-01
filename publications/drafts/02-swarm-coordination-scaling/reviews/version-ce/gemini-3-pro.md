---
paper: "02-swarm-coordination-scaling"
version: "ce"
modelId: "gemini-3-pro"
modelName: "Gemini 3 Pro"
reviewed: "2026-02-28"
recommendation: "Unknown"
---

Here is a comprehensive peer review of the manuscript (Version CE), structured according to IEEE Transactions on Aerospace and Electronic Systems standards.

---

# Peer Review Report

**Manuscript Title:** Design Equations and Parametric Sizing for Hierarchical Coordination in Large Autonomous Space Swarms
**Version:** CE

## 1. Significance & Novelty
**Rating: 5 (Excellent)**
The manuscript addresses a critical gap in the aerospace literature: the specific scaling properties of coordination protocols for "mega-constellation" scale swarms ($10^4$--$10^5$ nodes). While much existing literature focuses on routing (ISL) or small-scale formation flying ($<100$ nodes), this work provides closed-form sizing equations for the intermediate coordination layer. The distinction between message-layer byte budgets and physical-layer schedulability is a significant conceptual contribution that prevents the common error of assuming bandwidth equals capacity in half-duplex RF systems.

## 2. Methodological Soundness
**Rating: 5 (Excellent)**
The multi-layered verification approach is robust. The authors employ analytical derivation, cycle-aggregated Discrete Event Simulation (DES), a slot-level TDMA simulator, and a packet-level standards derivation. The explicit cross-validation between these models (e.g., Table VIII mapping claims to verification methods) is exemplary. The derivation of $\gamma$ (MAC efficiency) from CCSDS Proximity-1 standards rather than arbitrary assumption adds significant engineering rigor.

## 3. Validity & Logic
**Rating: 4 (Good)**
The logic is generally sound. The two-layer feasibility framework is logically consistent. The handling of the "stress case" versus "routine operations" via the campaign duty factor ($d$) resolves previous ambiguity regarding workload realism. However, the reliance on a static topology for bandwidth sizing, while justified for co-planar clusters, glosses over the transient control overhead of cross-plane re-association, though the authors acknowledge this limitation.

## 4. Clarity & Structure
**Rating: 5 (Excellent)**
The paper is exceptionally well-written. The notation is consistent, and the distinction between different types of overhead ($\eta_0$, $\eta_{cmd}$, baseline) is clearly defined in Section III.E. Figures are legible and directly support the text. The "Claim Map" (Table XV) is a helpful structural device that aids the reviewer and reader in tracking validation.

## 5. Ethical Compliance
**Rating: 5 (Excellent)**
The authors provide a clear Data Availability statement with a repository link. The acknowledgment of AI-assisted ideation is transparent and complies with emerging publication standards.

## 6. Scope & Referencing
**Rating: 4 (Good)**
The literature review covers relevant domains (swarm robotics, constellation management, networking). The connection to CCSDS standards is strong. However, the paper could better contextualize the "RF-backup" assumption against recent commercial trends moving toward purely optical backbones (e.g., SDA Transport Layer), explaining *why* a UHF backup remains a critical design driver for resilience.

---

## Major Issues

1.  **Contextualization of the RF-Backup Requirement**
    *   **Issue:** The entire sizing analysis hinges on the 1 kbps RF-backup channel being the bottleneck. While the authors justify this as a safety-critical mode, many modern mega-constellation architectures (e.g., Starlink, SDA) are moving toward relying heavily on redundant optical paths and ground entry points, potentially viewing a UHF omni system as unnecessary SWaP (Size, Weight, and Power) overhead.
    *   **Why it matters:** If the RF backup is not a universal requirement, the strict TDMA constraints derived here apply only to a subset of mission architectures.
    *   **Remedy:** In the Introduction or Discussion, explicitly argue why the RF backup remains essential even for optical-native constellations (e.g., "black start" recovery, tumbling spacecraft where pointing is lost, common-mode optical failure).

2.  **Unicast Command Latency in Stress Scenarios**
    *   **Issue:** The paper notes that unicast commands (Type 2) require a 22-cycle stagger (Eq. 7). While mathematically correct, the operational impact of a 220-second command dissemination latency during a "stress" scenario is not fully explored.
    *   **Why it matters:** A "stress" scenario often implies urgency (e.g., immediate collision avoidance). If the system requires 3+ minutes to command the fleet via unicast, the utility of this mode is questionable.
    *   **Remedy:** Add a brief discussion on the operational concept for Type 2 commands. Are these non-urgent configuration changes? If urgent, does this force a fallback to broadcast (Type 1) commands?

## Minor Issues

1.  **Table I (Notation):** The definition of $C_{node}$ is "Per-node bandwidth allocation." It would be clearer to specify "RF-backup bandwidth allocation" to avoid confusion with the high-speed optical links mentioned later.
2.  **Section IV.A (TDMA Frame Model):** The derivation of $\gamma=0.949$ vs. $\gamma=0.76$ is clear, but the text should explicitly state that $0.76$ is the *conservative* value used for all subsequent feasibility checks to avoid reader confusion.
3.  **Fig. 6 (Fleet Reuse):** The caption mentions "Normal operations... are non-binding." It would be helpful to explicitly state the value of $f_{RF}$ used for the "Normal" region in the caption (presumably $<1\%$).
4.  **Reference Style:** Ensure all references (e.g., [1] Starlink) are updated to the most recent available data or archival sources where possible, as web links may rot.

---

## Overall Recommendation
**Recommendation: Accept with Minor Revisions**

This is a high-quality manuscript that offers a rigorous, quantitative framework for sizing coordination protocols in large satellite constellations. The authors have successfully addressed the complexity of scaling by decomposing the problem into byte-level and airtime-level constraints.

The introduction of the campaign duty factor ($d$) successfully bridges the gap between theoretical worst-case bounds and realistic operational profiles. The derivation of the MAC efficiency parameter ($\gamma$) from CCSDS standards adds significant practical value, moving the work beyond abstract theory.

The requested revisions are primarily interpretative: strengthening the justification for the RF-backup design driver and clarifying the operational impact of unicast latency. Once these are addressed, the paper will make a valuable contribution to *IEEE TAES*.

---

## Constructive Suggestions

1.  **Strengthen the "Why UHF?" Argument:** Add a sentence in Section IV.A.1 explicitly linking the 1 kbps constraint to "tumbling safe-mode" where high-gain optical or Ka-band links are impossible to close. This cements the relevance of the analysis.
2.  **Visualizing the Stagger:** In Figure 7 (Unicast Stagger), consider annotating the "Broadcast" point ($q=0$) and the "Full Unicast" point ($q=1$) with their specific latency values (10s vs 220s) to make the trade-off immediately visible.
3.  **Gamma Lookup Table:** Consider adding a small "Practitioner's Lookup Table" for $\gamma$ that lists values for common modulation/coding schemes (e.g., BPSK 1/2, QPSK 7/8) alongside the derived 24/30 kbps values. This would increase the paper's utility as a reference handbook.