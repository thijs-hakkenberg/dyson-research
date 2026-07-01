---
paper: "02-swarm-coordination-scaling"
version: "by"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-28"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4/5 (Good)**

The manuscript targets a real and timely gap: practitioners lack *closed-form, byte-accounted sizing relationships* for hierarchical coordination at \(10^4\)–\(10^5\) spacecraft, especially under tight backup-RF constraints. The paper’s framing of “three feasibility layers” (byte budget \(\eta\), MAC efficiency \(\gamma\), and TDMA airtime schedulability) is a useful conceptual contribution that aligns well with how real systems fail: not only by average throughput, but by schedule feasibility under half-duplex and burstiness. The explicit separation \(\eta=\eta_0+\eta_{\text{cmd}}\) is also valuable for design trades, and the “coordinator ingress sizing” equation is practically actionable.

Novelty is strongest in (i) the message-layer parametric design equations tied to explicit byte accounting, (ii) the explicit mapping of correlated-loss recovery (GE) to cycle-level coordination and the intra-cycle ARQ infeasibility result under slow-mixing obstructions, and (iii) the attempt to cross-check with a slot-level TDMA simulator and provide \(\gamma\)-sensitivity breakpoints (Table 9). These are useful contributions for early-phase architecture sizing.

That said, some novelty claims are somewhat overstated because the framework is intentionally *message-layer* and abstracts away major binding constraints in space ISLs (contact/visibility, pointing, interference, multi-cluster scheduling beyond the simple reuse factor). The paper is still a good contribution, but it should position itself more explicitly as a *first-order sizing framework* rather than implying it resolves “coordination scaling” broadly.

---

## 2. Methodological Soundness  
**Rating: 3/5 (Adequate)**

The methodology is generally appropriate for the stated goal (closed-form sizing + fast DES for envelope exploration). The cycle-aggregated DES is defensible for byte budgets and inter-cycle phenomena (e.g., AoI under exception reporting, GE cross-cycle recovery). Reproducibility is a strength: the manuscript provides parameters (Table 5), verification taxonomy, and a public code release tag.

However, there are several methodological mismatches between what is *measured* and what is *claimed*. The DES uses a “fluid-server ingress” with drop-tail (Section III-A) while the key binding constraint in the 1 kbps regime is *TDMA superframe feasibility* and half-duplex scheduling (Section IV-A). You partially address this with a separate slot-level simulator, but the paper then mixes results from two models (fluid-server DES vs. slot-level TDMA) in a way that could mislead readers about what is actually enforced. For example: Table 12 (“Coordination success vs link availability”) reports retransmission outcomes without enforcing airtime, yet later the paper emphasizes ARQ infeasibility under RF-backup superframe constraints. This needs clearer separation of regimes and a more systematic integration of the slot-level constraints into the end-to-end performance evaluation.

Statistically, the Monte Carlo approach is acceptable for mean overhead (which is nearly deterministic given fixed message sizes), but tail claims need more care. AoI P99 is computed from many time samples, but those samples are highly dependent (periodic process + geometric gaps). Bootstrapping over per-run P99 values is not necessarily wrong, but the paper should clarify the resampling unit and independence assumptions. Similarly, GE recovery tail estimates are validated against a Markov model, which is good, but the mapping from physical obstruction processes to GE parameters remains qualitative.

---

## 3. Validity & Logic  
**Rating: 3/5 (Adequate)**

Many conclusions are logically supported *within the model*: e.g., \(\eta\) being \(O(1)\) under hierarchical aggregation (Eq. 3 and Table 13), command traffic dominating stress-case overhead (Table 6 and Section IV-E), and intra-cycle ARQ being ineffective under per-cycle GE coherence (Section IV-C and Table 11). The paper is also commendably explicit about what is not modeled and where \(\gamma\) is acting as an abstraction boundary (Abstract; Sections IV-A, V-A).

The main validity concern is that several “system-level” conclusions depend strongly on assumptions that are not merely parameter choices but structural: (i) centralized command generation making \(\eta_{\text{cmd}}\) topology-invariant (Sections I-C, IV-A “Command generation locus”), (ii) broadcast semantics for stress commands (Type 1) being the dominant mode, and (iii) static clustering for a year with only a small amortized reassociation overhead (Section V-B). These assumptions are plausible but not universally representative. In particular, the “topology-invariant command overhead” conclusion is only true under a specific control-plane semantics; under distributed planning, intra-cluster consensus and state distribution can easily dominate \(\eta_0\), and under unicast-heavy tasking the decisive constraint becomes airtime schedulability (your own Eq. 15–16 show this).

A second logic issue is the interplay between AoI and bandwidth. You correctly state AoI under exception reporting depends on \(p_{\text{exc}}\) and \(T_c\) (Table 2 footnote), but later you also discuss backup RF regimes where fleet-level reuse inflates \(T_c^{\text{fleet}}\) (Eq. 12). That inflation should directly worsen AoI tails; yet Table 2 indicates AoI P99 is unchanged across 1/10/100 kbps. This is only true if \(T_c\) is held fixed and reuse is non-binding; the paper should explicitly connect AoI to \(T_c^{\text{fleet}}\) when \(f_{\text{RF}}\) exceeds the non-binding threshold.

---

## 4. Clarity & Structure  
**Rating: 4/5 (Good)**

The manuscript is well organized, with clear research questions and a consistent set of symbols (Table 1). The “three feasibility layers” framing is communicated well, and the paper does a good job of providing both analytical equations and simulation cross-checks. Tables 2, 6, 9, 10, and 15 are particularly useful to a design-oriented audience.

Clarity suffers in a few places due to model interleaving and terminology. The paper uses “1 kbps regime” to mean a per-node *budget*, while the coordinator PHY is 24–30 kbps; this is explained (Section III-E), but readers may still misinterpret results unless the distinction is reiterated wherever coordinator rates are discussed. Similarly, “baseline telemetry excluded from \(\eta\)” is fine, but then \(\eta_{\text{total}}=\eta+20.5\%\) is used as a proxy for channel utilization; this can confuse readers about what is actually transmitted under each workload profile (e.g., Table 14 says nominal \(\eta=5\%\) but \(\eta_{\text{total}}=26\%\), which is substantial).

A structural improvement would be to consolidate the “design equations summary” (Section V-C) earlier (end of Methods or start of Results) and then treat simulation as validation and sensitivity. Right now, key equations are scattered (e.g., Eq. 13–14 feasibility constraints appear deep in IV-A), making it harder for readers to extract the core sizing recipe.

---

## 5. Ethical Compliance  
**Rating: 4/5 (Good)**

The manuscript includes an explicit disclosure of AI-assisted ideation in the Acknowledgment, which is consistent with emerging transparency norms. The disclosure states that AI assisted ideation but “is not validated here,” which is appropriate and avoids overstating AI-derived content.

Two improvements are needed for IEEE T-AES style completeness: (i) add a brief statement on whether any proprietary or sensitive operational data were used (it appears none were), and (ii) clarify authorship responsibility (e.g., “authors take full responsibility for content and validation”), which is increasingly expected when AI tools are mentioned. Conflicts of interest are not addressed; even if none exist, IEEE submissions typically include a COI statement during submission rather than in-manuscript, but you may add a brief “no competing interests” line if the journal permits.

---

## 6. Scope & Referencing  
**Rating: 4/5 (Good)**

The topic is appropriate for IEEE Transactions on Aerospace and Electronic Systems: it connects autonomy/coordination architectures to communication feasibility, reliability, and timing—core T-AES themes. The references cover distributed algorithms, AoI, satellite networking, and relevant standards (CCSDS). The use of Lutz/ITU-R for GE grounding is reasonable.

Referencing could be strengthened in two ways. First, the paper leans on several non-archival sources for constellation operations (e.g., Starlink filings, Amazon overview pages). That is sometimes unavoidable, but key claims about operational practices and scaling pain points should be supported with more archival or at least technical-report sources (e.g., peer-reviewed analyses of Starlink operations, conjunction mitigation studies, or FCC technical appendices where available). Second, the MAC/PHY abstraction via \(\gamma\) would benefit from citing representative LEO ISL MAC studies (TDMA/FDMA scheduling, half-duplex constraints, pointing acquisition overhead), since \(\gamma\) is central to your schedulability conclusions.

---

## Major Issues

1. **Model integration inconsistency (fluid-server DES vs slot-level TDMA) affects key claims.**  
   - The DES does not enforce airtime/half-duplex scheduling, yet several headline results (ARQ infeasibility, coordinator capacity, schedulability) are fundamentally airtime-driven (Sections III-A, IV-A, IV-D). The slot-level simulator validates some cases, but end-to-end results (drops, AoI under loss, delivery success) are still largely DES-based.  
   **Required change:** clearly partition results into (a) message-layer byte feasibility (DES/closed-form) and (b) airtime schedulability (slot-level), and avoid presenting DES outcomes as if they include TDMA constraints. Ideally, incorporate a simplified airtime constraint into DES (e.g., per-cycle service limited by superframe time) or run more of the key performance metrics in the slot-level model.

2. **Command workload semantics drive the main “topology-invariant overhead” conclusion.**  
   - The claim that command traffic dominates and is topology-invariant hinges on centralized command generation and broadcast addressing (Sections I-C, IV-A “Command generation locus”, IV-E). Under distributed planning, consensus/state exchange may not be negligible; under unicast-heavy commands, airtime dominates (Eq. 15–16).  
   **Required change:** add at least one alternative command-generation/decision architecture case study (even analytic) showing how \(\eta_{\text{cmd}}\) and/or \(\eta_0\) changes, and clarify which conclusions remain robust.

3. **AoI analysis is incomplete under fleet-level reuse and degraded \(T_c\).**  
   - Eq. 12 inflates \(T_c^{\text{fleet}}\) when RF-backup fraction grows, which directly worsens AoI tails, yet Table 2 suggests AoI P99 is unchanged across bandwidth regimes.  
   **Required change:** explicitly extend Eq. 18 to use \(T_c^{\text{fleet}}\) (or show conditions when \(T_c^{\text{fleet}}=T_c\) holds), and report AoI sensitivity to reuse groups \(G\).

4. **Parameter realism and sensitivity for key “design point” choices needs strengthening.**  
   - Several headline numbers (24–30 kbps coordinator PHY, \(\gamma=0.85\), \(k_c=100\), \(S_{\text{eph}}=256\) B, \(T_c=10\) s) are plausible but not justified from mission requirements or typical subsystem constraints.  
   **Required change:** add a short “parameter provenance” subsection (or table column) explaining why each default is representative, and provide a sensitivity sweep for at least \(T_c\), \(S_{\text{eph}}\), and \(k_c\) jointly (since superframe feasibility couples them).

---

## Minor Issues

1. **Coordinator ingress equation inconsistency:**  
   - Abstract: \(C_{\text{coord}} \ge k_c S_{\text{eph}} \times 8 /(T_c\gamma)\).  
   - Section V-C summary: \(C_{\text{coord}} \ge k_c S_{\text{eph}} \times 8 / T_c\) (missing \(\gamma\)).  
   Please make the definition consistent: is \(C_{\text{coord}}\) PHY rate or message-layer goodput? (Section III-E suggests \(C_{\text{coord}}\) is link rate and MAC scales by \(1/\gamma\), but IV-A uses \(C_{\text{TDMA}}\) with \(\gamma\) explicitly.)

2. **Baseline utilization accounting could confuse readers.**  
   - You exclude baseline telemetry from \(\eta\) but then discuss “total channel utilization” \(\eta_{\text{total}}\). Consider consistently reporting both offered load and total utilization in key tables (e.g., Table 14).

3. **Latency discussion mixes models and resolutions.**  
   - Table 16 notes TDMA wait-for-slot delay up to \(T_c\) is not included, while earlier latency claims cite \(\sim 260\) ms mean. Consider adding a “TDMA-aligned latency” estimate (e.g., expected wait \(\approx T_c/2\) unless slot fixed per node).

4. **Sectorized mesh comparator presentation remains potentially distracting.**  
   - You repeatedly note it is not functionally comparable (good), but then still present overhead comparisons (Tables/Figs). Consider moving the sectorized mesh to an appendix or tightening its role as a “local monitoring baseline” with explicit non-comparability.

5. **Small notation/definition nits:**  
   - Table 1: \(C_{\text{coord}}\) labeled “kbps” but equations use bps; ensure unit consistency.  
   - Eq. 3 message count omits bidirectionality; later you say \(\eta\) includes both directions—clarify what Eq. 3 counts.

---

## Overall Recommendation  
**Major Revision**

The paper is promising and likely publishable after revision, but several core claims currently rest on a split modeling approach (message-layer DES vs slot-level TDMA) without a fully consistent end-to-end evaluation under the binding airtime constraints. In addition, key conclusions about command-dominated, topology-invariant overhead depend on narrow workload semantics that should be broadened or more carefully scoped. Addressing these issues would substantially improve rigor and make the sizing framework more trustworthy for T-AES readers.

---

## Constructive Suggestions

1. **Unify the feasibility layers into a single “sizing workflow” and enforce Layer-3 constraints in performance results.**  
   Add a simple per-cycle airtime service constraint to the DES (even if approximate), or re-run key metrics (drops, delivery, AoI under loss) in the slot-level simulator for at least one representative cluster and then scale analytically.

2. **Add an alternative coordination semantics case (distributed planning) and quantify its overhead.**  
   For example: a Raft/consensus-based intra-cluster decision model where commands are generated locally and only summaries propagate upward. Provide \(\eta_{\text{consensus}}\) and show when it dominates/doesn’t, compared to centralized command traffic.

3. **Extend AoI analysis to include fleet-level reuse inflation.**  
   Replace \(T_c\) with \(T_c^{\text{fleet}}\) in Eq. 18 where applicable, and provide a small table/figure of AoI P95/P99 vs \(f_{\text{RF}}\), \(F\times R\), and \(k_c\).

4. **Clarify the meaning and calibration of \(\gamma\) with a more explicit budget.**  
   Provide a table decomposing \(\gamma\) into (i) framing/headers/CRC, (ii) guard/turnaround, (iii) FEC rate, (iv) ranging/sync overhead, (v) acquisition/pointing overhead (if any). This will help readers map \(\gamma=0.85\) to real radios.

5. **Tighten units and definitions; make coordinator capacity equations consistent across abstract/body/summary.**  
   Decide whether \(C_{\text{coord}}\) is PHY or goodput and apply consistently; update Section V-C and Table 1 accordingly. This is small but important because the coordinator sizing equation is one of the paper’s main deliverables.