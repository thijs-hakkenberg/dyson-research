---
paper: "02-swarm-coordination-scaling"
version: "dm"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-07"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript targets a real gap: early-stage *closed-form sizing* for hierarchical coordination traffic in very large swarms under explicit byte budgets and TDMA airtime constraints. The two-test decomposition (byte budget vs. schedulability) is a useful organizing principle, and the effort to ground the TDMA efficiency factor \(\gamma\) in CCSDS Proximity-1 framing is valuable for aerospace practitioners. The campaign duty factor \(d\) is a meaningful step toward workload realism compared to “always-on” command models.  

Novelty is moderate-to-high: many pieces exist separately (TDMA efficiency accounting, hierarchical aggregation, GE channels, AoI), but the paper’s contribution is the integration into a parametric sizing workflow with explicit per-cluster equations and a practitioner-oriented ladder from info-rate to PHY-rate.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The analytical framework is generally sound for preliminary sizing, and the separation between Test A (bytes) and Test B (time) is appropriate. However, several methods are not yet publication-ready due to (i) placeholder “TODO” results in Section IV-J/IV-K, (ii) some internal inconsistencies in framing overhead between Model C and NS-3, and (iii) the DES/slot-sim/NS-3 V&V narrative not fully closing the loop with concrete, reproducible quantitative outputs (beyond the stated 3–8% band).  

The GE modeling is positioned correctly as a what-if tool, but the mapping from GE parameters and coherence regime (\(\tau_c\)) to actual ISL conditions remains speculative; this is acceptable if clearly labeled as such and sensitivity is emphasized, but the current text occasionally reads as if the default GE parameters are “conservative truth” for ISL.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
The core logic—convert message requirements to info-rate, then inflate by \(\gamma^{-1}\) and half-duplex duty to test TDMA airtime—is coherent. The contextualization of the \(\eta_S\approx 46\%\) stress case as a continuous-duty upper bound occurring <1% of the time is the right direction and addresses a common reviewer concern (unrealistic always-on workloads).  

That said, the “three-layer feasibility framework (byte budget, MAC efficiency, TDMA airtime)” is described in the prompt, while the manuscript asserts *two tests* and insists \(C_{\text{raw}}=C_{\text{info}}/\gamma\) is not a third test. This is defensible, but the manuscript must be extremely consistent in presentation: right now it sometimes reads like \(\gamma\) is both a conversion and a quasi-independent feasibility gate. Also, the AoI-based justification for the 1% miss threshold is plausible but under-argued (assumptions about how misses translate to AoI tails are not rigorously derived).

---

## 4. Clarity & Structure  
**Rating: 3 (Adequate)**  
The paper is generally well organized and readable, with helpful tables (notation, rate ladder, superframe budget). The explicit “rate ladder” (Table III) is particularly practitioner-friendly.  

However, clarity is materially impacted by:  
- The presence of “TODO” placeholders in results sections (unacceptable for a journal submission).  
- Some numerical/accounting inconsistencies (e.g., 88 vs 104 bits framing; NS-3 described as “none share code,” but parameters differ, so the comparison is not cleanly isolating abstraction error).  
- Occasional ambiguity about which \(\gamma\) value is used in which step (24 vs 30 vs 35 kbps; \(\gamma_{30}\) used in Table III but feasibility claims “use Model C” across rates).  

---

## 5. Ethical Compliance  
**Rating: 4 (Good)**  
Strong: code and data availability are explicitly stated with a repository tag; AI-use disclosure is explicit and appropriately constrained to ideation/editing. Reproducibility is plausible *if* the repository contains the exact scripts/configs to regenerate every figure/table and if the “TODO” items are resolved. Consider adding an archival DOI (Zenodo) at acceptance.

---

## 6. Scope & Referencing  
**Rating: 4 (Good)**  
The topic fits IEEE TAES / ASR scope well (space comms, autonomy, coordination, protocol sizing). Referencing is broadly appropriate (CCSDS, DVB-RCS2, AoI, DTN, swarm robotics).  

Gaps: you should cite more directly comparable “burst TDMA efficiency” and “short packet satellite MAC” work beyond DVB-RCS2 (e.g., recent LEO return-link burst scheduling, short-packet PHY/MAC overhead analyses, and CCSDS Proximity-1 implementation notes if publicly available). Also, the “centralized scales to \(10^6\) via \(M/D/c\)” claim needs either a clearer citation or removal/softening—SMAD is not a queueing proof.

---

## 7. Technical Depth & Rigor  
**Rating: 3 (Adequate)**  
Good depth in slot timing decomposition and the attempt to connect miss probability to AoI requirements. The generalized expressions (e.g., \(\gamma\) equation, feasibility inequalities) are useful.  

But rigor is weakened by: incomplete independent validation, limited formal uncertainty propagation (e.g., acquisition time distribution, \(\gamma\) uncertainty, and their impact on \(R_{\text{PHY,min}}\)), and some places where conclusions are stronger than the demonstrated evidence (e.g., robustness across “all designs” when alternative designs table contains approximate values).

---

## 8. Practical Relevance & Implementability  
**Rating: 4 (Good)**  
The sizing procedure (Algorithm 1), rate ladder, and explicit default parameters are practically useful. The campaign duty factor \(d\) is a pragmatic knob for mission phases. The falsification conditions section is excellent and should be kept.  

To be implementable, practitioners need: (i) a clean recipe to compute \(\gamma(R)\) with all constants unambiguously defined and consistent across analytical and NS-3 models, and (ii) a clear statement of what must be measured on hardware (acquisition time distribution, turnaround time, framing overhead, coherence time).

---

## 9. Verification, Validation & Reproducibility Strength  
**Rating: 2 (Below Average)**  
The *intent* is good (tiered V&V; independent NS-3). But as written, Section IV-J contains placeholders and admits mismatched framing overhead (88 vs 104 bits) and stochastic acquisition vs fixed mean; that makes the 3–8% discrepancy hard to interpret as “abstraction error” versus “parameter mismatch.” Independent validation is only compelling if the two models instantiate *the same* physical/MAC assumptions and still differ due to simulator granularity. Right now, the comparison conflates multiple differences.  

Also, DES “reproduces means (<0.1%)” is essentially a self-check; that’s fine as Tier 1, but it should not be framed as validation of the model—only of the implementation.

---

## 10. Presentation Quality of Results & Claims  
**Rating: 3 (Adequate)**  
Key claims are concrete (35 kbps recommendation; \(\gamma\approx 0.73\)–0.76; coordinator ingress ~20 kbps info-rate; ~27 kbps after \(\gamma\)). The “stress-case as continuous-duty upper bound” is now better contextualized.  

However, several “robustness” and “validated” claims are currently overstated relative to the evidence shown in the manuscript text because the NS-3 and alternative slot structure sections are not finalized and include approximations/TODOs.

---

# Major Issues

1. **NS-3 validation is not yet publication-grade (placeholders + parameter mismatch).**  
   - **Why it matters:** The manuscript explicitly positions NS-3 as *independent validation* of \(\gamma\) and feasibility boundaries. If the NS-3 results are incomplete or not “apples-to-apples,” the strongest credibility lever of the paper collapses.  
   - **Remedy:**  
     1) Remove all “TODO” text and provide the actual numeric results (tables with mean/CI across runs) for \(\gamma_{\text{NS-3}}(R)\) and miss rates.  
     2) Run two NS-3 configurations:  
        - **Matched-assumptions run:** enforce the *same* framing bits (104), deterministic acquisition (=5 ms), same guard, same FEC rate assumptions as Model C. The remaining discrepancy then reflects packet-level scheduling/serialization effects.  
        - **Realism run:** include your stochastic acquisition and any NS-3-native framing choices, but then explicitly label it as a *different physical assumption set* and do not interpret the delta as abstraction error.  
     3) Report confidence intervals and sample sizes; show sensitivity of feasibility boundary to the observed \(\gamma\) delta (e.g., recompute \(R_{\text{PHY,min}}\) using \(\gamma_{\text{NS-3}}\)).

2. **\(\gamma\) “unification” (0.76 CCSDS-based) must be consistently applied across all computations and narrative.**  
   - **Why it matters:** Prior versions apparently used \(\gamma=0.85\). This version claims CCSDS-based \(\gamma\approx 0.73\)–0.76 and says “All feasibility claims use Model C.” Any lingering use of older \(\gamma\) values (even implicitly) would invalidate the 30/35 kbps boundary.  
   - **Remedy:** Add a one-page “consistency ledger” in the main paper (not only supplement): list each table/figure/claim that uses \(\gamma\), specify which rate (\(\gamma_{24},\gamma_{30},\gamma_{35}\)) and constants. Also, ensure Table II, Table III, Table IV, and the abstract use \(\gamma\) values consistent with Eq. (7) and the stated overhead bits (104) and acquisition/guard times.

3. **Clarify the feasibility framework layering: two tests vs three layers (and ensure no double-counting).**  
   - **Why it matters:** Reviewers will scrutinize whether byte budget, \(\gamma\) conversion, and TDMA scheduling are independent constraints or the same constraint expressed differently. Confusion here risks rejection as “framework ambiguity.”  
   - **Remedy:** Add a schematic (one figure) showing dataflow:  
     - Inputs \(\to\) compute \(\eta_{\text{total}}\) (Test A)  
     - Inputs \(\to\) compute slot time via \(\gamma\) \(\to\) compute \(T_{\text{ing}},T_{\text{egr}},T_{\text{ARQ}}\) (Test B)  
     - Show explicitly that \(\gamma\) is embedded within Test B, not a separate gate.  
     Also audit equations: Eq. (10) and Eq. (11) should be shown as derived from Eq. (13)–(14), not introduced as a quasi-third check.

4. **Workload realism via campaign duty factor \(d\): good concept, but needs stronger empirical/operational grounding.**  
   - **Why it matters:** The headline utilization numbers (\(\eta\approx 5\)–10% routine; 46% stress) depend critically on how \(d\) maps to mission phases. Without credible justification, \(d\) can look like a free knob chosen to make results feasible.  
   - **Remedy:** In the main text (not only supplement), include a short table mapping 3–5 representative mission phases to \((d,p_{\text{cmd}},q)\) with references or engineering rationale (e.g., station-keeping cadence, CA event rate bounds, reconfiguration campaigns). Also explicitly state whether \(d\) gates *only commands* or also other episodic traffic (alerts, elections).

5. **Stress-case contextualization is improved but still risks misinterpretation.**  
   - **Why it matters:** Saying “\(\eta_S\sim 46\%\) occurs <1% of operational time” is helpful, but readers may still interpret the system must be stable at that load continuously, or conversely dismiss it as arbitrary.  
   - **Remedy:** Define “continuous-duty upper bound” precisely: is it \(p_{\text{cmd}}=1\) every cycle for all nodes? For how long? What operational scenario would drive that? Then show a short “burst campaign” example: e.g., \(d=1\) for 30 minutes/day implies X% of time and yields Y average utilization and Z worst-case backlog (if any).

6. **DES verification adds limited value as currently presented; strengthen or de-emphasize.**  
   - **Why it matters:** “DES reproduces means (<0.1%)” mainly proves the DES implements the same equations. Journals will view this as weak validation unless the DES is used to produce nontrivial emergent behavior or distributional properties not captured analytically.  
   - **Remedy:** Either:  
     - **Option A (strengthen):** Use DES to validate *distributional* predictions (e.g., tail of recovery time, AoI tail under exception reporting, deadline miss distribution under stochastic acquisition/ARQ), and show an analytic approximation vs DES.  
     - **Option B (de-emphasize):** Move Tier-1 DES verification to supplement and keep the main paper focused on analytic sizing + NS-3 independent check.

7. **Alternative slot structures table is too approximate to support “robust across all designs” claims.**  
   - **Why it matters:** Table VII uses “\(\sim\)” values; yet the abstract and conclusion claim robustness across all designs. That over-claims.  
   - **Remedy:** Provide fully computed \(\gamma\) and \(R_{\text{PHY,min}}\) for each structure using the same accounting method, and (ideally) one NS-3 confirmation point per structure at 30 and/or 35 kbps. If you cannot, soften the claim to “indicative.”

8. **AoI-based 1% miss threshold justification needs a more rigorous link from miss rate to AoI tail.**  
   - **Why it matters:** The 1% threshold is central to Test B feasibility. If the AoI argument is hand-wavy, the feasibility criterion looks arbitrary.  
   - **Remedy:** Provide a short derivation or bounding argument: for periodic updates with independent per-cycle delivery with probability \(1-\epsilon\), AoI tail relates to geometric runs of misses. Even a simple bound (e.g., \(P(\text{AoI} > mT_c)=\epsilon^{m-1}\) under independence) would clarify assumptions; then discuss correlation (GE) and how that changes the tail.

---

# Minor Issues

1. **Remove all “TODO” comments** in the manuscript; they are disqualifying for review-ready submission.  
2. **Framing overhead inconsistency:** Model C uses \(O_{\text{frame}}=104\) bits; NS-3 description uses 88 bits and says “16-bit difference,” but 104–88 = 16 bits—fine—yet you must ensure every place uses the intended value and explain why CCSDS framing is 104 in the analytic model (what fields).  
3. **Check \(\gamma\) numbers vs Eq. (7):** provide a small table in the main text with computed \(\gamma\) at 24/30/35 kbps for the default slot payload size (256 B) and constants.  
4. **Algorithm 1:** Line 10 uses \(T_{\text{ARQ}} \leftarrow M_r \cdot T_{\text{slot}}\); but earlier Eq. (13) uses \((1+\bar{M}_r)\) multiplying ingress slots. Clarify whether ARQ consumes additional slots per member (more realistic) or a single extra slot (current algorithm reads like one slot total).  
5. **Half-duplex factor \(\alpha_{\text{RX}}\):** define explicitly whether it is a design choice or a computed consequence of ingress slot allocation; you treat it as computed output, but then use it in Eq. (11) as if it were a parameter.  
6. **Fleet-level reuse \(R=7\):** clearly label as placeholder assumption and avoid using it to claim non-binding fleet scaling unless supported by an interference study or at least a geometric reuse argument.  
7. **Command traffic accounting:** clarify whether command bytes are counted against the same 1 kbps/node “logical budget” even though they are coordinator egress; currently \(\eta_{\text{cmd}}\) is normalized by \(C_{\text{node}}T_c\), which is per-node allocation—this is conceptually odd for coordinator-to-member broadcast unless you justify the policy.  
8. **Typographic/consistency:** ensure all figures have file extensions and compile (e.g., `fig-cross_cycle_recovery` missing `.pdf` in includegraphics).  
9. **Reference support:** claims like “global-state mesh saturates at ~1000” should be backed by a citation or a brief derivation, otherwise soften.  
10. **Units:** be consistent with kbps definition (1000 vs 1024); IEEE typically assumes SI (1000). State it once.

---

## Overall Recommendation  
**Recommendation:** **Major Revision**

The paper has a strong premise and is close to being a useful practitioner reference: closed-form sizing, explicit overhead accounting, CCSDS-grounded \(\gamma\), and a clean separation between byte budget and TDMA schedulability. The campaign duty factor \(d\) is a meaningful improvement toward workload realism, and the stress-case is better framed as an upper bound rather than a typical operating point. The rate ladder and falsification conditions are notable strengths.

However, the manuscript is not yet ready for acceptance because the independent validation and “robustness” claims are not fully supported in the current version: NS-3 sections contain placeholders and conflate assumption mismatches with abstraction error; alternative slot structure results are approximate; and some internal consistency issues remain around ARQ airtime accounting and how \(\alpha_{\text{RX}}\) is treated. Addressing these items with finalized results, clean apples-to-apples comparisons, and tightened consistency would likely elevate the work to publishable quality.

---

## Constructive Suggestions (ordered by impact)

1. **Finalize and harden Section IV-J (NS-3):** remove placeholders, run matched-assumption experiments, publish numeric tables + CIs, and recompute feasibility boundary using \(\gamma_{\text{NS-3}}\).  
2. **Add a main-text “\(\gamma\) ledger” and consistency audit:** ensure every numeric conclusion uses the CCSDS-based \(\gamma\) values (0.73–0.76) consistently.  
3. **Fix ARQ airtime modeling consistency:** clarify whether ARQ consumes per-node extra slots; align Eq. (13), Algorithm 1, and Table IX logic.  
4. **Strengthen \(d\) realism:** add a concise mission-phase mapping table with defensible parameter choices and clarify what traffic \(d\) gates.  
5. **Quantify alternative slot structures without “\(\sim\)”** (or soften claims). Provide computed \(\gamma\) and margins for each structure.  
6. **Tighten the AoI/miss-rate argument:** provide a short derivation/bound and discuss GE correlation effects on AoI tails.  
7. **De-emphasize DES as “validation” unless it produces independent distributional insights** beyond confirming means; otherwise move details to supplement.  
8. **Clarify policy/interpretation of the 1 kbps/node allocation** vis-à-vis coordinator egress/broadcast traffic to avoid confusion in \(\eta_{\text{cmd}}\) normalization.  

If these revisions are completed with consistent accounting and fully reproducible validation results, the manuscript would present a compelling and practically useful sizing methodology suitable for a top-tier aerospace systems journal.