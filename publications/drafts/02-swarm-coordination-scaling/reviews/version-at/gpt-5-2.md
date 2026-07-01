---
paper: "02-swarm-coordination-scaling"
version: "at"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-27"
recommendation: "Unknown"
---

## 1. Significance & Novelty — **Rating: 4/5 (Good)**

The manuscript targets a practically important question: how to *size* hierarchical coordination for very large autonomous spacecraft swarms under a constrained “RF-backup” budget, and how key mechanisms (ingress burstiness, exception telemetry/AoI, correlated losses) translate into closed-form sizing rules. The emphasis on *byte-level accounting* coupled to simple design equations is a meaningful contribution for practitioners, and the paper’s intent to provide “engineering sizing” rather than yet another conceptual architecture is valuable for T-AES readership.

Novelty is strongest in (i) the explicit coordinator-ingress sizing under different scheduling/traffic-shaping abstractions (Section IV-A), (ii) the AoI quantification under exception telemetry with a clean geometric-tail cross-check (Section IV-B, Eq. (34)), and (iii) the inter-cycle recovery characterization under Gilbert–Elliott burst losses with a design-curve sweep (Section IV-C, Fig. 9). The “compositionality/independence” claim (Section IV-D) is also interesting, though it is highly conditional on the pipeline ordering and point-to-point links; as written, it risks being over-interpreted as a general property.

The main novelty limitation is that the stress-case headline overhead (~46%) is dominated by an assumed “one 512 B command per node per cycle” workload (Section IV-E), which is not clearly tied to realistic operational concepts for mega-constellations or swarms. The paper does acknowledge this as a bound, but the narrative still centers that number. If the paper reframes around *workload-parametric* sizing (and validates the workload assumptions better), the significance would increase.

---

## 2. Methodological Soundness — **Rating: 3/5 (Adequate)**

The cycle-aggregated DES is appropriate for message-layer sizing and enables large-N sweeps (Section III-A). The paper is commendably explicit about what is modeled vs. abstracted (Table 8), provides parameter tables (Table 7), and claims open-source release with a tag. The analytical cross-checks are a strength: AoI P99 matches the geometric expression (Eq. (34)), and overhead matches traffic accounting within 0.1% (Table 16). These are the right kinds of sanity checks for a sizing paper.

However, several modeling choices materially affect conclusions but are not justified with sufficient rigor for T-AES. The most important is the separation between “per-node average budget” (1 kbps) and “coordinator instantaneous ingest rate” (≥24 kbps) (Section III-F): the architecture implicitly assumes burst-capable radios, tight time synchronization, and feasible TDMA slotting at the cluster scale. The TDMA feasibility argument is currently order-of-magnitude (prop-delay vs slot duration) but omits key contributors: guard time sizing logic, sync error budgets, half-duplex turnaround, and link-layer framing/ARQ overhead. Since the coordinator-capacity result is one of the headline contributions (21–50 kbps), the abstraction around MAC/PHY needs either (a) stronger justification with bounds, or (b) a sensitivity study showing robustness to plausible overheads and sync errors.

Statistically, “30 MC replications” is usually fine for mean overhead (which is near-deterministic given fixed accounting), but it is not obviously sufficient for tail metrics like maximum loss streaks (Section IV-C) and P99 AoI when combined with failures and link outages. Also, the DES validation of the GE recovery curve uses “3 MC replications” in Fig. 9(a) (caption), which is too light for a claim framed as “DES-validated” design curves. Consider increasing replications for tail/streak metrics and reporting confidence bands on recovery percentiles.

---

## 3. Validity & Logic — **Rating: 3/5 (Adequate)**

Most conclusions are directionally supported by the internal logic: overhead constancy in N follows from O(N) message count with fixed per-node budgets; AoI under exception telemetry indeed has a geometric tail; and correlated burst losses do defeat within-cycle retransmissions (Section IV-C). The paper is generally careful to label centralized and global-mesh as intentional bounds (Section I-C, Section III-B/III-D), which helps interpret comparisons.

The main validity risk is the *interpretation* of the coordinator ingress sizing and the “independence/compositionality” claim. In Section IV-D, the finding “GE retransmissions add 22% offered load but produce zero additional coordinator drops” is an artifact of modeling loss before ingress and assuming independent point-to-point links. This is acknowledged, but the paper still elevates it as a “DES-specific contribution that validates compositional use” (Section IV roadmap; Section IV-D). For T-AES, the manuscript should more sharply separate: (i) a conditional property of the chosen pipeline abstraction vs. (ii) a generalizable engineering principle. At minimum, the paper should state the exact necessary conditions (loss before queue; no shared medium; no MAC coupling; fixed TDMA schedule; no retransmission backoff collisions) and discuss how quickly the result breaks under more realistic RF fallback.

Similarly, the stress-case overhead and “safe-mode floor” (Section IV-F; Discussion summary equations) are presented crisply, but the logic depends on mapping MAC efficiency γ to effective capacity without quantifying overhead sources (framing, coding, sync, ranging, acknowledgments). Given that the paper’s core message is “RF backup viability,” the conclusions would be more convincing if γ were derived or bounded from a concrete CCSDS/proximity-style link budget and protocol stack rather than treated as a free scalar in [0.7, 0.9].

---

## 4. Clarity & Structure — **Rating: 4/5 (Good)**

The paper is well organized: clear RQs (Section I-B), explicit baselines and interpretation notes (Section I-C), simulation abstraction disclosure (Table 8), and a Results roadmap (start of Section IV). Tables are generally effective, especially the traffic accounting (Table 11), coordinator ingress comparison (Table 12), AoI table (Table 13), and topology comparison (Table 18). The abstract is dense but largely accurate and aligned with the results.

That said, the manuscript sometimes mixes “message-layer accounting” with “system-level operational claims” without enough separation. For example, the abstract and conclusion state “validated” and “design equations compose” in a way that may read stronger than warranted given the abstractions. Also, the hierarchical architecture description (Section III-C) includes several operational assertions (handoff windows, power draw, election sizes) that feel under-sourced; these are plausible but should be either referenced, parameterized, or explicitly labeled as assumptions.

There are also a few places where definitions could be tightened to avoid reader confusion: the use of \(p_{\text{link}}\) sometimes denotes availability (success probability) and elsewhere “loss probability” is used (e.g., Section IV-C starts with “i.i.d. losses” then uses \(p_{\text{link}}=0.5\) in Table 23 as “link availability”). Standardizing notation (e.g., \(p_s\) success, \(p_\ell\) loss) would improve clarity.

---

## 5. Ethical Compliance — **Rating: 4/5 (Good)**

The manuscript includes an explicit disclosure of AI-assisted ideation in the Acknowledgment, naming models used and clarifying that those aspects are not validated here. This is consistent with emerging IEEE expectations around transparency, and it is better than the typical vague statement.

Two improvements are advisable. First, the disclosure should be moved (or duplicated) into a dedicated “Disclosure” or “Ethics” note earlier (e.g., end of Introduction or Data Availability) because readers may miss it in acknowledgments. Second, the authors should clarify whether any text, code, figures, or analysis were generated by AI tools, and whether the authors verified correctness—IEEE venues increasingly expect this specificity.

No human/animal subjects are involved; no obvious ethical red flags beyond the need for clearer COI/authorship transparency. The author block uses a placeholder “Project Dyson Research Team”; for IEEE T-AES submission this is not acceptable long-term, but the manuscript notes names/affiliations will be provided for final publication.

---

## 6. Scope & Referencing — **Rating: 3/5 (Adequate)**

The topic is appropriate for IEEE Transactions on Aerospace and Electronic Systems: constellation/swarm coordination, comms architecture scaling, reliability under outage, and parametric sizing are squarely in scope. The references cover distributed algorithms, AoI, gossip, DTN, constellation networking, and some operational constellation context.

However, the referencing is uneven in two ways. (1) Several key operational claims rely on non-archival sources (e.g., Kuiper overview page; McDowell’s site; some DARPA pages). Those are acceptable for context but not for core quantitative assumptions. (2) The paper would benefit from citing more directly relevant work on: LEO TT&C constraints and spectrum coordination; inter-satellite link scheduling (especially TDMA/beam hopping); and constellation operations architectures (including published Starlink/OneWeb technical filings beyond high-level references). Also, for the queueing and AoI parts, there is room to cite standard results for batch-service or gated polling models closer to the “\(D[k_c]/D/1\)” behavior described (Section III-C; Table 19).

Finally, the manuscript positions itself as filling a gap: “No prior work has systematically compared … byte-level traffic accounting under a fixed per-node budget” (Section I-A). This claim is plausible but should be softened or better supported by a more systematic related-work argument; otherwise reviewers may challenge it as overly broad.

---

## Major Issues

1. **MAC/PHY abstraction is too weak for the headline coordinator-ingress sizing claim (Section III-F; IV-A; Eq. (31)).**  
   The paper’s key sizing result (21–50 kbps coordinator ingress for \(k_c=100\)) depends on TDMA feasibility, synchronization, guard times, framing overhead, and half-duplex constraints—yet these are abstracted and collapsed into \(\gamma\). For T-AES, either:  
   - provide a concrete link-layer model (even coarse) that derives plausible \(\gamma\) and slot structure, or  
   - add a rigorous sensitivity/bounding analysis showing that conclusions hold across realistic sync/guard/ARQ overheads and turnaround times.

2. **The “joint independence/compositionality” conclusion is over-claimed and needs tighter conditions (Section IV-D).**  
   The observed independence is largely a modeling artifact (loss applied before ingress; independent links; no shared-medium contention). The paper acknowledges this but still frames it as validating “composition without cross-factor correction.” This should be rewritten as a conditional result with explicit necessary/sufficient conditions and a brief counterexample model (e.g., shared RF with retransmission-induced contention) to demonstrate non-compositionality.

3. **Workload model—especially stress-case—needs stronger operational grounding (Section IV-E; Table 10; Table 14).**  
   “One 512 B command per node per cycle” drives the 46% headline and safe-mode threshold \(\gamma_{\min}=0.46\). The manuscript should justify when such a workload occurs (what mission, what control loop, why 10 s cadence, why 512 B) or reframe results primarily around \(p_{\text{cmd}}\) with realistic ranges derived from operational scenarios (conjunction screening, station-keeping, orbit raising, fault management).

4. **Static clustering and absence of orbital/visibility dynamics may materially change conclusions about RF-backup viability (Section III-C; Limitations).**  
   Earth occlusion, contact windows, and cross-plane relative motion can introduce correlated outages and re-association overhead bursts. The paper notes this, but given the focus on RF backup (<1% time) and fault tolerance during ground outages, visibility-driven correlation is central. At minimum, add a simplified deterministic occlusion model or a worst-case outage schedule to test whether AoI/recovery/buffer sizing still holds.

---

## Minor Issues

- **Notation inconsistency for link probability.**  
  Table 23 uses \(p_{\text{link}}\) as “link availability,” while Section IV-C discusses “losses” and uses \(p_{\text{loss}}\). Standardize throughout and ensure equations match the table definitions.

- **Equation (31) TDMA capacity uses \((k_c-1)\) rather than \(k_c\).**  
  Eq. (31) \(C_{\text{TDMA}} = \frac{(k_c - 1) S_{\text{eph}} 8}{T_c \gamma}\): why minus 1? If excluding the coordinator’s own report, state it explicitly; otherwise use \(k_c\).

- **Figure reference / file naming issue.**  
  Fig. 9 includes `\includegraphics{fig-cross-cycle-recovery}` without extension while others include `.pdf`. Ensure consistent compilation.

- **GE recovery “DES bars (3 MC replications)” (Fig. 9 caption) conflicts with earlier “30 MC replications per configuration” (Section III-E).**  
  Clarify which metrics use 30 vs 3 replications and why; for tail recovery, 3 is likely insufficient.

- **Centralized baseline queueing model is underutilized.**  
  Section III-B introduces M/D/1 and M/D/c, but later comparisons emphasize spectrum/latency instead of queueing. Consider trimming or aligning the baseline analysis to what is actually compared.

- **Some quantitative claims need citations or to be labeled assumptions.**  
  Examples: “15 W additional draw” and “within typical solar-panel margins” (Section III-C, power); “98–99.5% per station availability” (Section IV-F). Either cite or mark as assumed.

---

## Overall Recommendation — **Major Revision**

The paper has strong potential and several genuinely useful closed-form sizing results, but key conclusions rest on under-justified MAC/PHY and operational workload assumptions. Tightening the conditions for the “independence/compositionality” claim, strengthening the realism of the RF-backup link model (or bounding it), and grounding workload profiles in operational scenarios are necessary before the manuscript meets IEEE T-AES standards for methodological rigor and defensible engineering guidance.

---

## Constructive Suggestions

1. **Add a minimal but concrete link-layer model to replace (or substantiate) \(\gamma\).**  
   For example: specify a TDMA frame with slot structure (preamble, sync, header, payload, CRC, guard), half-duplex turnaround, and optional ARQ; then compute an *effective* \(\gamma\) range and show coordinator-ingress feasibility under those parameters. Even a simplified CCSDS Proximity-1-based budget would materially strengthen Section IV-A and the “safe-mode floor.”

2. **Reframe workload results around a scenario-derived \(p_{\text{cmd}}\) distribution and cadence \(T_c\).**  
   Keep stress-case as a bound, but add at least one operationally grounded scenario (e.g., conjunction campaign affecting X% of nodes for Y minutes per orbit; orbit-raising phase; anomaly response) and show resulting \(\eta(t)\), AoI, and coordinator capacity. This will make the 5–46% envelope credible rather than arbitrary.

3. **Strengthen the GE inter-cycle recovery validation and reporting.**  
   Increase MC replications for Fig. 9, report confidence intervals on mean/P95 recovery cycles, and clarify the Markov-chain model used (state definition and derivation of \(p_{\text{eff}}\) in the design summary). Consider including worst-case burst lengths and implications for buffer sizing and AoI.

4. **Make the “compositionality” claim precise and test a counterfactual.**  
   Add a short experiment with a shared-medium abstraction (even a simple slotted ALOHA contention model) to demonstrate coupling between retransmissions and ingress saturation, thereby delimiting applicability. Alternatively, explicitly list assumptions under which independence holds and present it as a conditional lemma.

5. **Address dynamic clustering / visibility correlation with a lightweight extension.**  
   Introduce a simple model of periodic occlusion/outage windows (deterministic or Markov-modulated) and occasional cluster re-association events, then re-evaluate AoI tails and buffer sizing. Even a “stress visibility” sensitivity would significantly improve external validity for RF-backup operation.