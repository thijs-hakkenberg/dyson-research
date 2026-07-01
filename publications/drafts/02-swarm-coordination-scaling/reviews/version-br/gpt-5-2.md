---
paper: "02-swarm-coordination-scaling"
version: "br"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-27"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 4/5 (Good)**

The manuscript targets a real and increasingly important problem: coordination and communications sizing for very large autonomous spacecraft swarms (10³–10⁵ nodes) under constrained per-node bandwidth. The paper’s framing around *closed-form sizing equations* and the “three feasibility layers” (byte budget, MAC efficiency, TDMA airtime schedulability) is a useful design-oriented contribution. The explicit separation of topology-dependent overhead (\(\eta_0\)) from workload-dependent command load (\(\eta_{\text{cmd}}\)) is also a valuable conceptual simplification that can help practitioners reason about architecture trade spaces.

The novelty claim is mostly credible: many works address routing/ISLs, DTN scheduling, or small-swarm coordination, but fewer provide byte-accounted parametric equations validated by simulation at 10⁵ scale. The paper’s emphasis on “message-layer” sizing and the explicit treatment of half-duplex TDMA superframe feasibility (Table 11) distinguishes it from more abstract coordination literature.

That said, some novelty is weakened by the fact that several “core findings” are driven by assumed message semantics that are not inherent to hierarchical coordination (e.g., the stress-case command model being topology-invariant because commands are centrally generated and counted as per-node information regardless of PHY broadcast/unicast). This is acknowledged, but the manuscript would benefit from a clearer statement of what is fundamentally architectural vs. what is an artifact of the workload model and accounting conventions.

Overall, the paper is significant and likely to be of interest to T-AES readers working on constellation ops, distributed autonomy, and comms architecture sizing, but it needs tightening to ensure the claimed generality matches the assumptions.

---

## 2. Methodological Soundness — **Rating: 3/5 (Adequate)**

The methodological approach—closed-form derivations cross-checked by a cycle-aggregated DES, plus an independent slot-level TDMA feasibility simulator—is a strength. The paper is unusually explicit about what is and is not modeled, and provides a public repository/tag, which supports reproducibility. Analytical cross-checks (e.g., AoI P99 Eq. (18), coordinator capacity Eq. (10)) matching DES within stated tolerances is good practice.

However, several modeling choices materially affect the conclusions and need stronger justification and/or sensitivity treatment:

* **Traffic model and accounting**: The paper defines \(\eta\) as information-content bytes per node per cycle rather than airtime consumption, then separately treats airtime feasibility for TDMA. This is reasonable, but it creates a risk of double-counting/under-counting when comparing architectures with different addressing modes (broadcast vs unicast) and different MAC coordination burdens (centralized TDMA vs distributed medium access). In particular, the sectorized mesh comparison assumes \(\gamma=0.85\) is achievable without modeling distributed TDMA overhead (the paper notes this, but the quantitative comparison still relies on the optimistic \(\gamma\)).

* **DES vs TDMA coupling**: The DES uses a fluid-server ingress and explicitly does **not** enforce TDMA/half-duplex constraints (Section IV-D “model enforcement note”). Yet several results (e.g., coordinator drops vs capacity; joint interactions Table 14) are interpreted operationally. Because TDMA airtime constraints *do* couple loss/ARQ/half-duplex scheduling (as you correctly show in Section IV-A), the separation of “queue drops” from “airtime deadline misses” is not merely a detail—it can change feasibility conclusions under burstiness, retransmissions, and multi-message egress.

* **Gilbert–Elliott coherence assumption**: GE state is constant over the entire \(T_c=10\) s cycle, which structurally makes intra-cycle retransmissions ineffective “by construction” (Section IV-C). You acknowledge this, but then use it to motivate design conclusions (e.g., “intra-cycle ARQ infeasible; rely on inter-cycle repetition”). The slot-level simulator does provide supporting evidence under the assumed model, but the physical plausibility of “constant state for 10 s across all slots” needs stronger grounding (or a sensitivity case with sub-cycle transitions).

Statistically, 30 replications are likely sufficient for mean overhead estimates (given low variance), but tail metrics (AoI P99, recovery P95) deserve clearer reporting of estimator stability (e.g., CI widths for P95 recovery, not only AoI). Also, the year-long simulation horizon is fine, but some modeled events (e.g., coordinator failures at 2%/yr) are rare at cluster level; it is unclear whether the reported availability curves are simulation-derived or largely analytical/illustrative.

---

## 3. Validity & Logic — **Rating: 3/5 (Adequate)**

Many conclusions are supported within the paper’s model boundaries: e.g., \(\eta\) being \(O(1)\) for hierarchy, the dominance of command bytes in the stress profile, the coordinator ingress sizing around 20–30 kbps for \(k_c=100\), and the AoI P99 under exception telemetry matching the geometric model. The explicit superframe budget (Table 11) is a strong piece of evidence for the half-duplex constraint and helps translate byte budgets into schedule feasibility.

The main validity concern is *external validity*: several “design-driving” conclusions hinge on assumptions that may not hold in realistic space comms operations. Examples:
* The claim “at \(\ge 10\) kbps per node all message-layer constraints are non-binding” (abstract; Table 2) presumes proportional scaling of coordinator PHY, dedicated scheduled access, and no antenna/visibility constraints—yet those are often the binding constraints at higher rates. The paper acknowledges this, but the conclusion is stated strongly and may be misread as operational guidance.
* The interpretation that GE losses and coordinator queue drops are independent (Table 14) is true in the fluid-server + erasure-before-queue model, but not necessarily in a shared-medium or TDMA airtime-limited regime where lost packets still consume slots and retransmissions consume airtime (which you also show). The paper should avoid presenting decoupling as a general property of hierarchical coordination rather than a property of the chosen abstraction.

The logic around “topology-invariant command traffic” is internally consistent given your definition of \(\eta\) as information content per node, but it becomes confusing when combined with the airtime feasibility layer where broadcast vs unicast radically changes schedulability (Eq. (12) and Table 16). This is an important point, but it needs cleaner exposition: readers may (reasonably) expect “overhead” to reflect channel resource consumption, not logical information volume.

Limitations are acknowledged (Section V), but a few are so central (MAC contention; distributed scheduling overhead; visibility/pointing) that they should be elevated earlier (e.g., end of Introduction or early in Simulation Framework) to prevent over-interpretation of the quantitative results.

---

## 4. Clarity & Structure — **Rating: 4/5 (Good)**

The manuscript is generally well organized, with a clear roadmap in Section IV and consistent notation (Table 1). The separation of analytical equations, DES validation, and slot-level TDMA checks is clear and aligns well with the “design equations” goal. Tables are mostly effective, especially Table 11 (superframe budget), Table 16 (three-layer feasibility), and Table 18 (topology comparison with caveats).

The abstract is information-dense and mostly accurate, but it risks overwhelming readers and includes several very specific numerical claims (e.g., “623 ms per-cycle margin,” “AoI P99 = 440 s,” “P95 recovery in 4 cycles”) without stating the key assumptions (e.g., \(T_c=10\) s, \(k_c=100\), GE coherence per cycle). Consider adding 1–2 short parenthetical qualifiers in the abstract to prevent misinterpretation.

Some definitions and terminology could be tightened:
* “Baseline telemetry (20.5%) excluded from \(\eta\)” is used throughout; this is fine, but readers may struggle to compare with conventional channel utilization metrics. The paper does provide \(\eta_{\text{total}}\), but the narrative sometimes shifts between \(\eta\), \(\eta_{\text{total}}\), and \(\eta/\gamma\) without reminding the reader which is being discussed.
* The sectorized mesh is presented as a “baseline” but has narrower functional scope (you do state this). Still, the comparison could be clearer if the paper explicitly states: “sectorized mesh is not a full substitute for hierarchical coordination; it is a local-neighborhood monitoring comparator.”

Figures are referenced appropriately, but since the review is based on LaTeX source only, I note a likely compilation issue: `\includegraphics{fig-cross-cycle-recovery}` lacks a file extension unlike other figures; this may break builds depending on compiler settings.

---

## 5. Ethical Compliance — **Rating: 4/5 (Good)**

The paper includes an explicit disclosure of AI-assisted ideation in the Acknowledgment, specifying tools and clarifying that the AI output is not validated. This is aligned with emerging transparency norms and is preferable to omission.

Potential issues:
* The author list is replaced by “Project Dyson Research Team” with a footnote promising final names later. IEEE policy generally requires author identities at submission/review stages (double-blind exceptions aside). If this is an anonymized review version, it should be stated explicitly; otherwise, it may raise compliance concerns.
* The repository is linked and tagged, which is good for reproducibility. Ensure the repository includes license/attribution and that any datasets do not include restricted information (likely not applicable here).

No obvious ethical red flags in the modeling itself, but the manuscript should be careful not to over-claim operational applicability given unmodeled constraints—this is more “responsible communication” than formal ethics, but relevant in safety-critical aerospace contexts.

---

## 6. Scope & Referencing — **Rating: 4/5 (Good)**

The topic fits IEEE T-AES: it combines aerospace system architecture with comms scheduling, reliability, and distributed autonomy. The paper is strongly systems-oriented with quantitative sizing guidance, which is appropriate for the journal.

References are broadly relevant and include key works on mega-constellation routing (Handley; del Portillo), DTN/CCSDS standards, distributed algorithms (Lynch, Lamport, Raft), and AoI survey literature. The inclusion of CCSDS Proximity-1 and SPP is a plus for realism.

A few referencing/scope improvements would strengthen the positioning:
* For MAC/TDMA feasibility and half-duplex scheduling, consider citing classic satellite TDMA framing and/or more recent LEO inter-satellite MAC scheduling papers (beyond routing). Right now, the MAC layer is mostly handled via \(\gamma\) and your own frame model; adding external references would help validate assumptions (guard times, turnaround, framing overheads).
* The centralized baseline is explicitly compute-only (M/D/c), not comms-limited; that’s fine as a bound, but it makes the “baseline” less meaningful for T-AES readers unless complemented by at least a back-of-envelope ground contact/uplink spectrum bound or a citation-based discussion.

---

## Major Issues

1. **Mismatch between DES enforcement and TDMA/half-duplex feasibility (core validity risk).**  
   The DES results on drops and joint interactions (e.g., Table 14) are generated with a fluid-server ingress and do not enforce TDMA slotting or half-duplex partitioning, while the paper’s feasibility claims heavily rely on TDMA airtime constraints (Section IV-A, Table 11). This split is acceptable if framed as “byte/queue-layer” vs “airtime-layer,” but several interpretations read as operational conclusions. You should either (a) integrate the TDMA scheduler into the DES for the key scenarios, or (b) more strictly limit claims from DES tables to the fluid-server model and provide parallel airtime-feasibility results for the same parameter sweeps.

2. **GE coherence-time assumption makes ARQ failure largely an artifact of model construction.**  
   In Section IV-C, the GE state is constant within a full 10 s cycle, ensuring all intra-cycle retries see the same state. This strongly drives the conclusion “intra-cycle ARQ is ineffective,” which then feeds into design guidance. A required revision is to add at least one sensitivity case with sub-cycle GE transitions (e.g., slot-level Markov state changes or coherence time distribution) and show how recovery/feasibility changes.

3. **Overhead metric \(\eta\) conflates information content and channel resource usage across broadcast/unicast.**  
   The paper states \(\eta\) counts information content per node, not PHY time, which is fine, but then uses \(\eta\) for cross-topology comparisons where MAC coordination costs differ greatly (hierarchical scheduled TDMA vs sector mesh). This is especially problematic when concluding command traffic is topology-invariant. You should provide an additional metric: *airtime utilization* (or “resource overhead”) that accounts for broadcast vs unicast transmissions and includes MAC coordination overhead assumptions explicitly.

4. **Sectorized mesh comparison is not apples-to-apples and may mislead without stronger normalization.**  
   You acknowledge narrower functional scope and distributed TDMA challenges, but the quantitative comparisons (e.g., Table 9, Table 18, “14× difference per peer”) depend on assumptions (cap=10, \(\gamma=0.85\), limited neighbor monitoring). This section needs either (a) a clearer statement that it is *not* a competing architecture for the same coordination problem, or (b) a revised mesh model that provides comparable functional coverage (e.g., ensuring each node monitors all sector peers, then showing infeasibility under 1 kbps).

---

## Minor Issues

1. **Figure includegraphics extension inconsistency:** `\includegraphics{fig-cross-cycle-recovery}` (no extension) vs others using `.pdf`. This may break compilation depending on LaTeX settings.

2. **Centralized model parameter ambiguity:** In Section III-B-1, you set \(\mu_s=1000\) msg/s and state “\(\rho=1.0\) at \(N=10,000\) for \(c=1\).” This implies \(r=0.1\) msg/s, but it would help to explicitly connect to Table 3’s \(r\) to avoid confusion.

3. **Eq. (7) / hierarchy message count vs bidirectional traffic:** Eq. (7) counts messages as \(N + N/k_c + N/(k_ck_r)\), but later you state \(\eta\approx46\%\) includes both directions. Consider clarifying whether Eq. (7) is uplink-only status/summary count or total message count including downlink heartbeats/commands.

4. **Table 6 “key notation” vs later usage:** Symbols like \(C_{\text{raw}}\) and \(\alpha_{\text{RX}}\) appear later but are not in the key notation table. Add them for readability.

5. **Duty cycle/availability table reads partly illustrative:** Table 22 mixes “handoff success,” “system availability,” and qualitative “handoff cost.” If these are not derived from the DES, label them as analytical/illustrative and provide equations or move to Discussion.

6. **Abstract density:** Consider trimming some numerical details and emphasizing assumptions (e.g., \(k_c=100\), \(T_c=10\) s) to improve accessibility.

---

## Overall Recommendation — **Major Revision**

The paper has strong potential and contains several valuable design-oriented results, but key conclusions rely on abstractions that are not consistently enforced across simulation components (fluid-server DES vs TDMA airtime constraints), and the correlated-loss/ARQ conclusions are heavily shaped by the GE coherence assumption. Addressing these issues—primarily by adding sensitivity cases and aligning the simulation evidence with the scheduling constraints—would substantially strengthen validity and make the sizing equations more defensible for T-AES publication.

---

## Constructive Suggestions

1. **Add an “airtime/resource utilization” metric alongside \(\eta\).**  
   Define a channel-resource metric that counts transmissions (not per-node information) and explicitly distinguishes broadcast vs unicast. Report both \(\eta_{\text{info}}\) and \(\eta_{\text{air}}\) for the stress-case; this will resolve confusion around “topology-invariant commands” and make cross-architecture comparisons more meaningful.

2. **Introduce a sub-cycle GE sensitivity study (slot-level Markov).**  
   Keep your per-cycle GE as a conservative bound, but add at least one alternative: GE transitions per slot (or every \(m\) slots) with the same steady-state availability, and re-evaluate (i) intra-cycle ARQ feasibility, (ii) inter-cycle recovery P95, and (iii) superframe margin impact at 24–30 kbps.

3. **Unify (or more tightly couple) DES and TDMA feasibility for key tables.**  
   For coordinator drop/capacity sweeps (Fig. 6, Table 14), add a parallel evaluation where “drops” include airtime deadline misses under the TDMA schedule (even if simplified). Alternatively, clearly relabel these as “queue drops under fluid-server ingress” and provide a separate “airtime feasibility map” for the same parameter grid.

4. **Strengthen the sectorized mesh comparison with explicit MAC coordination cost.**  
   Either (a) add a distributed TDMA control overhead term (even a conservative bound) for the mesh to justify any \(\gamma\) assumption, or (b) present mesh results under a more realistic contention efficiency range (e.g., \(\gamma=0.3\)–0.5) and show how conclusions change.

5. **Elevate key assumptions and applicability conditions earlier (end of Introduction).**  
   Add a short “Model Applicability” paragraph summarizing: dedicated scheduled access assumption, half-duplex coordinator RF backup regime, static clustering, message-layer accounting, and what operational constraints are explicitly excluded (visibility, pointing, spectrum regulation). This will reduce the risk of over-interpreting the quantitative claims.