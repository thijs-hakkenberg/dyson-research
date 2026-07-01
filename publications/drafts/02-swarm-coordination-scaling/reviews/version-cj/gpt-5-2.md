---
paper: "02-swarm-coordination-scaling"
version: "cj"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-02"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript’s main contribution is a *practitioner-facing sizing framework* that explicitly separates (i) message-layer byte-budget feasibility from (ii) PHY/MAC TDMA airtime schedulability, and then ties both to coordinator ingress sizing. This “two (and effectively three) layer” framing—byte budget → MAC efficiency via \(\gamma\) → explicit TDMA superframe timing—is a valuable structuring device for early-phase swarm/constellation architecture trades, especially in the under-served \(10^3\)–\(10^5\) scale regime. The paper also offers closed-form expressions, design ladders, and a concrete recommended PHY rate (35 kbps) grounded in CCSDS Proximity-1 framing assumptions.

Novelty is strongest in: (a) the explicit \(\gamma\) grounding and its consequences on feasibility boundaries; (b) the integration of half-duplex TDMA timing constraints with workload semantics (broadcast vs unicast staggering); and (c) the emphasis on distributional (tail) coordinator buffer sizing under correlated campaign processes. The GE recovery curves are potentially useful, but would benefit from clearer mapping to ISL empirical regimes or a stronger justification of parameter priors.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The analytical sizing equations are generally coherent and the paper is careful about what is “verification” vs “validation.” The use of three simulation layers (cycle-aggregated DES, slot-level TDMA, packet-level \(\gamma\) derivation) is methodologically reasonable for the questions posed, and the manuscript appropriately states that Tier-1 agreement is expected by construction.

However, several modeling choices materially affect conclusions and need tighter treatment: (i) the interplay between \(\gamma\) as a scalar efficiency and explicit TDMA timing (risk of double-counting or inconsistent application); (ii) the GE coherence-time assumption and its coupling to ARQ and TDMA margin; (iii) coordinator ingress modeled as a “fluid server” in DES while TDMA feasibility is evaluated elsewhere—this split is fine, but the boundaries must be made airtight so readers don’t misinterpret DES drops vs TDMA deadline misses.

Monte Carlo configuration (30 reps, 1-year runs) is fine for mean overhead and many tail metrics, but some tail claims (P99/P95) would benefit from reporting uncertainty or sensitivity to run length and sampling cadence.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Internal logic is mostly consistent, and the manuscript is unusually explicit about limitations and evidence tiers. The campaign duty factor \(d\) is a meaningful improvement: it directly addresses “continuous stress-case realism” by making the stress-case a *continuous-duty upper bound* rather than an implied nominal regime. The stress-case contextualization is largely successful.

That said, there are logic/consistency hazards:
- The manuscript sometimes treats “coordinator ingress \(\approx 27\) kbps” as if it were an info-rate and elsewhere as a PHY-rate after \(\gamma\) adjustments. This is partly clarified by the “rate ladder,” but the narrative still risks confusion.  
- The “three-layer feasibility” is described as two layers in several places. In practice you have: Layer 1 byte budget, Layer 2 TDMA airtime, and a bridging MAC-efficiency translation via \(\gamma\) (plus half-duplex \(\alpha_{\mathrm{RX}}\)). This should be consistently presented to avoid readers thinking \(\eta/\gamma\) is itself a feasibility test.  
- The GE/ARQ infeasibility conclusion is valid *under the stated coherence assumption*, but the paper should more sharply distinguish “structurally ineffective due to correlated state across retransmissions” from “infeasible due to TDMA margin.” Right now both mechanisms appear, but the causal chain is easy to misread.

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
Overall organization is strong: notation table, clear separation of models (Model S vs Model C), evidence tiers, and a well-structured results section. The “rate ladder” table and feasibility algorithm are good for practitioners.

Clarity issues remain:
- \(\gamma\) is central but appears in multiple forms (\(\gamma_{C,24}\), \(\gamma_{C,30}\), \(\gamma(R)\), decomposition product, time-domain calculation) with a footnote admitting discrepancies. This undermines confidence unless cleaned up.  
- Some claims are repeated with slightly different numbers (e.g., slot time and \(\gamma\) values), and the reader must chase footnotes/tables to reconcile them.  
- The distinction between “coordination channel 35 kbps” vs “RF-backup 2.5 kbps” vs “per-node budget 1 kbps” is explained, but because the paper frequently says “1 kbps regime” while simultaneously selecting 30–35 kbps PHY, a reader can still get lost. A single consolidated figure showing the channel hierarchy and where each analysis applies would help.

---

## 5. Ethical Compliance  
**Rating: 4 (Good)**  
Open-source code and tag are provided; parameter table is detailed; tools and environment are specified. The AI disclosure is unusually transparent and appropriate.

Two improvements needed for reproducibility:
- Provide a deterministic “reproduce key tables/figures” script list (Makefile or one-command runner) and archive the exact outputs used in the paper (or provide hashes).  
- Clarify whether any external non-archival sources (e.g., Starlink ops filings, web pages) are required to reproduce claims; ideally, isolate them as contextual only.

---

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
The paper is broadly in-scope for IEEE TAES / Adv. Space Research (architectures, comms constraints, autonomy coordination). References cover distributed systems and some space comm standards, but several key literature gaps remain:

- TDMA scheduling and satellite MAC literature beyond DVB-RCS2 (e.g., return-link scheduling, DAMA, satellite mesh TDMA, and more recent LEO ISL MAC studies if any are public).  
- AoI in scheduled/TDMA systems and AoI under correlated losses (you cite surveys, but not much on AoI-tail design under burst losses).  
- Queueing for MMPP/D/1 tails (you mention it, but no citations to matrix-analytic methods / tail bounds that could strengthen claims).

---

# Major Issues

1) **Inconsistent and potentially confusing application of \(\gamma\) (risk of double counting + narrative inconsistency)**  
**Why it matters:** \(\gamma\) is used both as (i) a multiplicative MAC efficiency translating info-rate to PHY-rate and (ii) as an implied slot-time driver in TDMA timing. If the same overhead (framing/FEC/acq/guard) is counted once in \(\gamma\) and again in explicit slot durations, conclusions about “24 kbps infeasible / 30 kbps feasible / recommend 35 kbps” can appear fragile or circular. The manuscript also contains multiple slightly different \(\gamma\) and slot-time calculations (0.760 vs 0.765; slot 111.5 ms vs 115.5 ms).  
**Remedy:**  
- Create a single “source of truth” definition: either define \(T_{\text{slot}}(R)\) directly and derive \(\gamma\) from it, or define \(\gamma(R)\) and never recompute slot time inconsistently.  
- Remove the footnote discrepancy by recomputing all \(\gamma\) and slot durations with unrounded intermediate values and publishing the exact bit counts (ASM, header, FCS, etc.) and acquisition/guard assumptions used in *every* table.  
- Add a short consistency check: show that \(T_{\text{slot}} = (S\times 8/R_{\text{PHY}})/\gamma\) matches the explicit packet-level simulator within <0.5% for each rate.

2) **The “three-layer feasibility framework” is not consistently formalized as three layers**  
**Why it matters:** The paper claims “two-layer feasibility” but repeatedly introduces an intermediate translation (\(\eta/\gamma\), plus half-duplex \(\alpha_{\mathrm{RX}}\)) and even a screening heuristic. Practitioners could misapply \(\eta_{\text{total}}/\gamma\) as a sufficient condition, despite warnings.  
**Remedy:**  
- Explicitly define a 3-step workflow:  
  (L1) byte-budget feasibility (\(\eta_{\text{total}}\le 1\));  
  (L2) PHY-rate feasibility via efficiency (\(R_{\text{PHY}} \ge C_{\text{info}}/(\gamma\alpha_{\mathrm{RX}})\));  
  (L3) TDMA superframe timing feasibility (Eqs. 33–34).  
- Relegate the \(\eta_{\text{total}}/\gamma < 0.50\) heuristic to an appendix or clearly label it as “non-binding empirical observation for this parameter set,” not a general rule.

3) **Campaign duty factor \(d\): improved realism, but still underspecified statistically and operationally**  
**Why it matters:** The paper’s central rebuttal to “stress-case unrealistic” is \(d\). But \(d\) is used in multiple stochastic forms (Bernoulli per-cycle per-node, ON/OFF Markov, cluster-correlated ON/OFF), and the sizing implications differ mainly in tails/buffers. Without a recommended *default* duty model and guidance on mapping mission concepts to \((d, L_{\text{on}}, \text{correlation scope})\), practitioners may select overly optimistic assumptions.  
**Remedy:**  
- Provide a recommended baseline duty model for sizing (e.g., cluster-correlated ON/OFF with conservative \(L_{\text{on}}\)) and justify it.  
- Add a table mapping the worked examples (orbit raising, station keeping, collision avoidance, software updates) to: \(d\), \(L_{\text{on}}\), correlation level (node vs cluster vs region), and expected peak coordinator ingress distribution.  
- Clarify which results (e.g., 25 kbps vs 50 kbps drop elimination via phase staggering) depend on which duty model.

4) **GE model: useful sensitivity curves, but weak grounding and ambiguous mapping to ISL mechanisms**  
**Why it matters:** The paper is careful to call GE parameters “illustrative,” yet it still reports concrete recovery numbers (P95=4 cycles) prominently (abstract/table). Without clearer priors, reviewers/readers may treat these as predictive. Also, the coherence-time discussion mixes “state transitions per cycle” with “per-slot coherence” in a way that could be misread as a physical claim rather than a modeling knob.  
**Remedy:**  
- Move the default GE parameter set out of “representative instantiation” and label it “illustrative example point,” while emphasizing the design curves as the real output.  
- Provide a clearer mapping from physical blockage duration distributions to \(p_{BG}\) (e.g., if blockage duration is geometric/exponential with mean \(\bar{T}_B\), then \(p_{BG}\approx T_c/\bar{T}_B\) under memoryless assumption).  
- Add one additional sensitivity dimension: show P95 recovery as a function of \(T_c\) (since \(T_c\) is a design variable and directly changes the coherence regime).

5) **DES verification value: still risks being perceived as “confirming its own equations”**  
**Why it matters:** You explicitly acknowledge Tier-1 is code verification, but a large fraction of results remain mean-value matches. The *real* DES value is tail/buffer behavior under correlated campaigns and losses; this should be elevated and expanded to justify the DES’s inclusion.  
**Remedy:**  
- Promote distributional results to a primary contribution: add at least one design rule derived from DES tails (e.g., buffer sizing factor vs \(d\), \(L_{\text{on}}\), and correlation scope).  
- Quantify tail uncertainty (e.g., CI on P99 buffer occupancy across replications).  
- Consider adding one “failure of mean-only sizing” example where mean-based capacity would pass but tail-based buffer overflow becomes non-negligible.

6) **Packet-level validation (Section IV-J) anchors \(\gamma\), but remains an internal construction rather than independent validation**  
**Why it matters:** Deriving \(\gamma\) from CCSDS framing is valuable, but it is not “validation” in the empirical sense; it is parameter derivation. Also, Proximity-1 is proximity link protocol; its applicability to LEO ISL coordinator channel needs a more explicit justification (or a statement that it is used as a conservative stand-in).  
**Remedy:**  
- Rename “packet-level validation” to “standards-grounded parameter derivation” consistently (you already do this title-wise—carry the language through the narrative).  
- Justify why Proximity-1 framing/assumptions (ASM, acquisition per burst, etc.) are appropriate or conservative for the intended ISL coordinator channel, and list what would change under alternative CCSDS/space link layers.

7) **Generalized \(\gamma\) expression: good idea, but not yet packaged for practitioner use**  
**Why it matters:** Eq. (46) is potentially one of the most reusable artifacts, but the paper does not provide a worked example beyond the default case, nor guidance on which terms dominate in which regimes.  
**Remedy:**  
- Add a short “dominance” note: at low rates, \(T_{\text{guard}}+T_{\text{acq}}\) dominates; at higher rates, framing/FEC dominates.  
- Provide a worked calculation for two payload sizes (e.g., 128 B and 512 B) and two acquisition models (per-slot vs per-superframe), and show resulting \(\gamma\) and required \(R_{\text{PHY,min}}\).

---

# Minor Issues

1) **Terminology:** You frequently say “1 kbps regime” while using 30–35 kbps PHY for the coordinator channel. Consider consistently saying “1 kbps *per-node budget* regime” vs “30–35 kbps coordinator PHY.”  

2) **Numeric consistency:** Reconcile slot time/bit counts causing 111.5 ms vs 115.5 ms and \(\gamma=0.760\) vs 0.765. This should not be left to a footnote; it’s central.  

3) **Table labeling:** Some tables mix “info-rate” and “PHY-rate” without always labeling units as kbps-info vs kbps-PHY. Add explicit column headers.  

4) **AoI interpretation:** AoI P99 = 440 s is derived from geometric sampling; you should explicitly state that this is *not* a network-induced latency tail but a *sampling policy tail*. Otherwise readers may think the network is causing 7+ minute delays.  

5) **Centralized baseline:** You repeatedly caution it is compute-only. Consider either removing it or adding a second centralized comms-limited baseline (e.g., ground contact duty cycle / spectrum-limited return link) so the comparison is less artificial.  

6) **Unicast staggering:** The unicast equations are useful; clarify whether per-node unicast commands are assumed to be serialized by design, and whether piggybacking/multiplexing multiple unicasts into one longer burst is allowed (which would change acquisition overhead assumptions).  

7) **Evidence tier table:** Table 21 is good. Consider adding a column “depends on \(\gamma\) assumption?” for quick reading.  

8) **Citations:** Some “non-archival accessed Feb 2026” sources may be frowned upon in IEEE TAES. Where possible, replace with archival sources or explicitly mark as contextual only.

---

## Overall Recommendation  
**Recommendation:** Major Revision  

The manuscript has a strong core idea—closed-form sizing equations coupled to a clear feasibility framework—and it is unusually transparent about V&V tiers and limitations. The campaign duty factor \(d\) is a substantive improvement that addresses workload realism concerns: it correctly reframes the 46% stress-case as a continuous-duty upper bound and gives practitioners a knob for episodic operations. The CCSDS-grounded \(\gamma\) derivation is also a meaningful step beyond arbitrary MAC-efficiency assumptions, and the broadcast vs unicast schedulability distinction is practically important.

The main reasons for major revision are (i) the centrality of \(\gamma\) and lingering inconsistencies/rounding discrepancies that undermine confidence in the 24 vs 30 vs 35 kbps boundary; (ii) the need to formalize the feasibility framework as a consistent multi-step procedure (and demote heuristics); and (iii) the need to strengthen the practitioner mapping for \(d\) and GE parameters so that the design curves and sizing rules can be applied without inadvertently optimistic assumptions. Addressing these points would significantly improve technical rigor and usability without requiring fundamentally new experiments.

---

## Constructive Suggestions (ordered by impact)

1) **Unify \(\gamma\), slot time, and all rate-feasibility numbers into a single consistent calculation pipeline** (publish exact bit fields and unrounded values; ensure every table uses the same definitions).  

2) **Recast feasibility as a 3-step test (byte budget → rate/efficiency → TDMA timing)** and ensure the narrative never suggests \(\eta/\gamma\) is a feasibility condition.  

3) **Strengthen the duty-factor section into a practitioner-ready “how to pick \(d\)” guide** including correlation scope and ON-duration defaults; add a conservative recommended default model for sizing.  

4) **Reframe GE results to emphasize sensitivity curves over the single default point**; add a simple mapping from mean blockage duration to \(p_{BG}\), and add sensitivity to \(T_c\).  

5) **Elevate DES tail analysis into a concrete design output** (buffer sizing factor rules vs campaign correlation), with uncertainty reporting for tail metrics.  

6) **Clarify the standards grounding scope**: Proximity-1 as conservative stand-in for ISL; list what changes under alternative framing/acquisition architectures (per-superframe tracking, multiplexed bursts, different FEC).  

7) **Add one consolidated “mode/channel stack” figure** showing optical ISL, coordinator channel (S-band 35 kbps), RF-backup (UHF 2.5 kbps), and where each analysis applies; this will reduce persistent reader confusion.

If the authors make the above revisions—especially the \(\gamma\) unification and feasibility formalization—I expect the paper could become a solid, citable design reference for early-phase swarm coordination sizing.