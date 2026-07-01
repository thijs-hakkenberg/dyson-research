---
paper: "02-swarm-coordination-scaling"
version: "aj"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-27"
recommendation: "Major Revision"
---

## 1. Significance & Novelty (Rating: 4/5)

The manuscript targets a real and increasingly urgent problem: how coordination/control-plane architectures scale for very large autonomous spacecraft swarms (10³–10⁵, with discussion extending toward 10⁶). The paper’s core novelty is not a new coordination algorithm per se, but a systematic *byte-accounted*, parametric design-space characterization across multiple topologies under an explicit per-node control-plane budget (1 kbps) and with clearly separated “baseline telemetry” vs “protocol overhead” accounting (Section 3.6–3.8, Tables 8–10). This framing is valuable for aerospace systems engineers who need first-order sizing and sensitivity guidance rather than algorithmic proofs.

The strongest contribution is the *engineering-style decomposition* with analytic cross-checks and then DES-based joint-condition verification (Sections 4.A–4.D). In particular, the coordinator ingress sizing bracket (21–50 kbps depending on access model; Section 4.A, Tables 11–12) and the AoI tail quantification under exception reporting (Section 4.B, Eq. (22), Table 13) are crisp, interpretable results. The explicit statement that the DES is used primarily to verify compositionality (rather than to discover emergent behavior) is unusually candid and helps position the paper properly.

That said, some “headline” novelty claims are partially undercut by the fact that many results are analytically determined by the traffic model (e.g., constant η with N is essentially guaranteed once message counts scale linearly and the hierarchy depth is fixed). The manuscript is still publishable on novelty grounds because it provides an integrated, reproducible reference model and consolidates several practically important sizing results in one place—but it should more clearly distinguish what is *derived* vs what is *validated by simulation* and why DES is necessary beyond arithmetic accounting.

---

## 2. Methodological Soundness (Rating: 3/5)

The simulation framework is generally well-specified for a message-layer study: cycle-aggregated DES with explicit byte counting, queue models at coordinators, and Monte Carlo replications (Section 3.1–3.4, Table 7). The paper does a good job stating what is abstracted (Table 8) and repeatedly reminds the reader that results are message-layer offered load scaled by 1/γ for MAC effects (Sections 3.6, 4.A, 4.F). The inclusion of analytical cross-checks (Pollaczek–Khinchine for M/D/1, AoI geometric tail, retransmission success under GE) is a strength and increases confidence that the implementation is not producing spurious artifacts.

However, there are several methodological tensions that should be addressed before publication:

1) **Time scale feasibility and “one-year simulation” claim.** With \(T_c=10\) s, one year corresponds to ~3.15 million cycles. With full participation at \(N=10^5\), generating/processing per-cycle events for all nodes implies on the order of 3e11 node-cycle “message generations” if done literally. Yet the runtime claim is ~7 seconds per run at \(N=10^5\) (Section 3.5). This suggests substantial aggregation/vectorization (which is fine), but the manuscript currently describes full-participation DES in a way that reads like explicit per-node per-cycle event handling. You need to reconcile the algorithmic complexity and provide enough implementation detail (e.g., vectorized counting vs explicit event objects) so readers can assess whether “DES” is an accurate characterization or whether this is closer to deterministic accounting with small stochastic overlays.

2) **Queueing/arrival modeling inconsistencies.** For centralized arrivals, you justify Poisson approximation via random phase offsets and Palm–Khintchine (Section 3.2.1). For coordinator ingress burstiness, you use random-phase periodic sources and then impose either strict cycle deadlines or token buckets (Section 4.A). That is reasonable, but the paper mixes “queue service rate” models (µc, µr) with “hard byte budgets per cycle” capacity models (C_coord) in a way that is not always internally consistent. In particular, Table 11 defines drops due to “capacity window,” but it is unclear whether drops occur due to byte budget exhaustion, message-processing service limits, buffer overflow, or a combination. You should explicitly define the service discipline and the mapping between kbps capacity and message service in the coordinator ingress model.

3) **GE model parameterization and interpretation.** The GE channel is defined per-cycle with state transitions (Table 7), but the “matched steady-state availability” statement in Section 4.C is potentially confusing: your GE parameters yield ~80% time in good state, but within good state loss is 1% and within bad state loss is 90%. The resulting *mean success probability per attempt* is not simply “80% availability.” You do later focus on “bad-state burst” behavior (27.1% with 3 attempts), which is fine, but the paper should compute and report the implied overall per-attempt success probability and average burst length (expected run length in bad state is \(1/p_{BG}=5\) cycles) to ground the “4–7 cycles recovery” claim.

Reproducibility is promising due to the repository link and parameter tables, but IEEE TAES reviewers typically expect enough methodological detail in the manuscript that results are interpretable even without reading code. Right now, several key mechanics are only partially specified (drop mechanism, election timing, how “regional coordinators pooled bandwidth” is modeled, etc.).

---

## 3. Validity & Logic (Rating: 3/5)

Many conclusions are supported by the presented analysis, and the manuscript is generally careful with caveats. The AoI P99 calculation (Eq. (22)) matching DES is convincing, and the retransmission contrast between i.i.d. and burst losses is logically correct (Section 4.C). The coordinator ingress sizing arguments are plausible and the TDMA feasibility vignette is helpful (Section 4.A).

The main validity concern is that several “system-level” conclusions rely on assumptions that are either (i) not modeled, or (ii) modeled in a way that structurally enforces the desired independence. The clearest example is the “joint independence” result (Section 4.D, Table 15): you conclude GE retransmissions and coordinator saturation compose independently because losses occur before ingress queuing, and retransmissions that fail do not arrive. That is true *by construction* for a point-to-point, non-contention model where C_coord is an ingress limiter rather than a shared channel. The paper acknowledges this conditionality, but the current presentation still risks overgeneralization. I recommend reframing this as a *model property* that clarifies which coupling mechanisms are absent—and explicitly stating that a different result is expected under shared-medium or even under coordinator-side scheduling constraints (e.g., if the coordinator must allocate receive slots and retransmissions consume those slots).

A second logic issue is the interpretation of the centralized baseline. You correctly note that compute does not diverge until ~10⁶ with provisioning (Section 4.F), and that spectrum/ground availability are binding. However, the paper’s centralized model is still somewhat stylized: it treats the “ground coordinator” as a queueing server for messages, but does not explicitly account for ground contact windows, routing via gateways, or Starlink-like ISL-to-ground backhaul. Since one of the headline comparative claims is “spectrum independence” and “ground outage minutes/day,” the centralized baseline would benefit from a more explicit model of contact scheduling or at least a sensitivity analysis showing how those outage assumptions map to coordination gaps.

Finally, the manuscript sometimes blurs “protocol overhead” (η excluding baseline telemetry) and “total utilization.” You do define this carefully (Section 3.6), but some later statements (e.g., about retransmission pushing “offered load to 80.5% exceeding channel capacity when combined with baseline telemetry,” Section 4.G Link Availability) could be clearer by consistently reporting both η and η_total when making feasibility claims.

---

## 4. Clarity & Structure (Rating: 4/5)

Overall organization is strong: the paper sets up research questions, defines baselines as intentional bounds, specifies metrics and traffic accounting, then presents results with analytic cross-checks. The explicit tables for traffic accounting (Table 10), abstraction scope (Table 8), and parameter summary (Table 7) are particularly helpful for readers who want to reuse the model.

The abstract is dense but largely accurate; it does a good job stating assumptions (1 kbps/node, message-layer estimates, γ scaling) and summarizing key quantitative results. One improvement: the abstract currently includes several claims that depend on nuanced interpretation (e.g., centralized baseline “does not diverge computationally until N≈10⁶,” and the “hierarchical advantage is fault tolerance and spectrum independence”). These are defensible, but they are not purely simulation outputs; they are scenario-based interpretations. Consider signaling in the abstract which items are “from DES” vs “from analytical sizing / scenario assumptions.”

A few places would benefit from tightening to avoid reader confusion:
- Section 3.1 describes a priority queue with 1-second resolution collision events, but Table 8 says store-and-forward/DTN is “not modeled,” whereas Section 4.C discusses inter-cycle store-and-forward recovery. You appear to implement buffering/retry across cycles for missed reports, which is a form of store-and-forward at the message layer. Either adjust Table 8 wording or clarify that you model *application-layer buffering* but not BPv7/DTN routing behaviors.
- The sectorized mesh model (Section 3.2.4) uses a heuristic \(k_s=\lceil\sqrt{N}\rceil\) with an argument involving screening radius scaling with nearest-neighbor distance. This is interesting, but currently reads as hand-wavy. If it is only a comparator, consider simplifying: define sector size as a parameter and show sensitivity, rather than embedding a questionable scaling derivation.

Figures are referenced appropriately, but since the PDF figures are not visible in the LaTeX excerpt, ensure the captions are sufficiently self-contained (many already are). Also ensure all “Section V-C” references are consistent with IEEE numbering; you currently refer to “Section V-C” in Section 3.1, but the Discussion is Section 5 and Limitations are 5.2—so this may be a leftover from an earlier draft.

---

## 5. Ethical Compliance (Rating: 4/5)

The manuscript includes an explicit disclosure of AI-assisted ideation in the Acknowledgment, naming tools and clarifying that the concept is not validated in the current study. This is aligned with emerging transparency norms and is preferable to non-disclosure. The data/code availability statement is also strong and supports reproducibility.

Two items to improve for IEEE TAES norms:
- The author list is anonymized (“Project Dyson Research Team”) with a placeholder footnote. That is presumably for double-blind review, but TAES typically uses single-blind. Ensure the submission policy is followed; if anonymization is required for review, fine, but then remove “Project Dyson” branding elements that may deanonymize.
- Conflicts of interest are not discussed. If “Project Dyson” is an organization with a public mission or potential commercial stake, add a short COI statement (even if “none”) and clarify governance/funding sources if relevant.

No human/animal subjects issues appear. The main ethical dimension is responsible communication: the paper generally avoids overclaiming, but should continue to be careful that “fault tolerance” and “spectrum independence” are contextual conclusions rather than universally true properties.

---

## 6. Scope & Referencing (Rating: 4/5)

The topic is appropriate for IEEE Transactions on Aerospace and Electronic Systems: it sits at the intersection of space systems architecture, autonomous coordination, and communication/network scalability. The paper also has a strong systems-engineering flavor (budgets, duty cycles, link capacity sizing), which fits TAES readership.

Referencing is broad and mostly relevant: constellation/ISL routing (Handley, del Portillo, Akyildiz), DTN/BPv7, distributed algorithms, AoI surveys, and swarm robotics surveys are all appropriate. Some references are non-archival (SpaceX webpage, DARPA pages). That is acceptable in moderation, but key factual claims (e.g., “Starlink operations,” “7000 active satellites mid-2024,” “coordination challenges during conjunction events”) would be stronger with archival or at least regulatory filings, technical reports, or peer-reviewed sources. Consider adding references to FCC filings, SpaceX/ESA technical publications, or academic analyses of Starlink operations and conjunction handling.

One gap: the paper leans heavily on queueing theory and AoI, but could cite more directly related work on hierarchical/federated spacecraft autonomy and distributed space traffic management concepts (beyond F6 and federated satellites). Even a short discussion of how your hierarchical model relates to existing spacecraft autonomy architectures (e.g., onboard planning/executive frameworks, distributed mission operations) would help.

---

## Major Issues

1. **Reconcile “one-year, full-participation DES” with claimed runtimes and event modeling.**  
   As written (Sections 3.1, 3.5, 4.5), the computational load implied by 1-year simulation at \(T_c=10\) s and \(N=10^5\) is enormous if implemented literally. You need to explain the implementation strategy (vectorized aggregation, analytical counting per cycle, sampling, or event compression) and ensure terminology matches (DES vs analytical Monte Carlo). Without this, reviewers may doubt the validity of the simulation claims.

2. **Clarify coordinator ingress capacity/drop model and its relationship to queueing service.**  
   Section 4.A introduces Model A/B byte-budget enforcement, while Table 7 lists coordinator processing capacities (µc, µr) and a message buffer size. It is unclear which mechanism causes drops in Table 11/15 and whether message-processing service limits ever bind. Provide a single, unambiguous model: arrival process → buffering → service discipline → capacity constraint → drop condition, and specify whether C_coord is a link limiter, a scheduler limiter, or an application-layer acceptance limiter.

3. **Store-and-forward modeling inconsistency.**  
   Table 8 states DTN/store-and-forward is not modeled, but Section 4.C explicitly analyzes “inter-cycle store-and-forward recovery” and buffer requirements. If you implement cross-cycle buffering/retry, state precisely what is modeled (application-layer ARQ across cycles) and what is not (routing, custody transfer, BP convergence, multi-hop delays). Otherwise the reader may misinterpret the results as DTN claims.

4. **Centralized baseline needs a clearer communication/spectrum model if spectrum/ground availability are key differentiators.**  
   Section 4.F argues centralized compute scales, but spectrum and outages bind. Yet the centralized model itself is primarily a processing queue. If you want to claim “100 Mbps aggregate uplink at N=10^5” and “7–29 min/day lost coordination,” you should formalize these as part of the baseline model (even as a simple contact/outage process) or present them as external scenario calculations clearly separated from the DES comparisons.

5. **Sectorized mesh comparator: strengthen justification or treat as a parameterized sensitivity case.**  
   The \(k_s=\sqrt{N}\) derivation (Section 3.2.4) is not rigorous and could be contested. Since the sectorized mesh is used to support quantitative claims (e.g., 1.35–1.95× overhead), either (i) justify sector sizing with a clearer geometric/operational argument and/or citations, or (ii) present sector size and neighbor cap as independent parameters and report results as a sensitivity family rather than a single “realistic” comparator.

---

## Minor Issues

- **Section cross-reference inconsistency:** Section 3.1 references “Section V-C” but the manuscript’s Section 5 is Discussion with subsections 5.1/5.2. Update cross-references.
- **Table 16 (Link availability) footnote labels:** The table uses superscripts a/b/c but the note text appears mismatched (“Offered … \textsuperscript{b} … \textsuperscript{c}”). Verify superscripts and the statement “exceeds 100% at \(p_{\text{link}}\le 0.5\)”—it says “\textsuperscript{c}” but the column shows “80.5” and “90.2” for η offered (excluding baseline). Make explicit whether “exceeds 100%” refers to η_total including baseline and MAC.
- **Global-state mesh accounting:** In Table 3 footnote, the arithmetic for “send+receive ≈ 51 MB” appears inconsistent with the preceding expression (2×256×100×17×59 ≈ 51.4 MB is fine), but then “with 1.4× redundancy ≈ 73 MB” is plausible; consider adding a short sentence explaining where 1.4× comes from (empirical? literature?).
- **Duty cycle table derivations:** Section 4.G duty-cycle derivations contain several numerical claims (e.g., transfer time 80 ms at 10 MB/1 Gbps is correct; but earlier you state 10–50 MB transfers take 1–10 s in Section 3.2.2, which conflicts). Harmonize these assumptions: either optical ISL is 1–10 Gbps (then 10–50 MB is ~0.08–0.4 s), or include protocol/setup overhead to reach 1–10 s—state it.
- **Terminology:** You use “cluster coordinator ingress capacity” in kbps but also use µc in msg/s. Consider consistently expressing coordinator constraints in either bits/s with serialization or in msg/s with fixed message sizes; mixing both invites confusion.
- **Minor LaTeX/IEEE style:** Ensure all URLs are IEEE-compliant; consider using `\url{}` consistently (you do). Check that “non-archival” references are acceptable and minimize them.

---

## Overall Recommendation

**Major Revision**

The paper is timely, mostly well-structured, and contains several useful quantitative sizing results with good analytical cross-checks. However, there are core modeling clarity issues—particularly the feasibility/description of the “one-year full-participation DES,” the precise coordinator drop/capacity mechanism, and inconsistencies around store-and-forward and handoff transfer timing—that must be resolved to ensure the results are interpretable and defensible to TAES standards. These are fixable with improved model specification, reconciled assumptions, and (ideally) a small set of additional validation/sensitivity experiments.

---

## Constructive Suggestions

1. **Add a “Model Mechanics” subsection that precisely defines the simulation state update per cycle.**  
   Include pseudocode or a step-by-step pipeline: message generation → link loss → arrival at coordinator → capacity enforcement (C_coord) → queue/service (µc) → summary generation → command dissemination. Explicitly state what is computed analytically vs simulated stochastically. This will also resolve the runtime/full-participation skepticism.

2. **Unify coordinator capacity modeling: choose one primary abstraction and map alternatives cleanly.**  
   For example, define coordinator ingress as a *receive scheduler* with capacity C_coord bits/s and optional buffering across cycles (token bucket). If you keep µc/µr, show that processing is non-binding under all reported configurations (or report where it binds). Provide one diagram/table mapping (C_coord, µc, buffer) → drop condition.

3. **Formalize the centralized baseline’s “spectrum/availability” constraints as a simple stochastic contact/outage model.**  
   Even a two-state ground-contact process (available/unavailable with given duty factor) would let you compute the “unhandled screening events” metric within the same modeling framework, rather than as an external narrative. This would make the centralized vs hierarchical comparison more rigorous.

4. **Strengthen the sectorized mesh comparator by parameterizing sector size and neighbor cap and reporting a small sensitivity grid.**  
   Replace the \(\sqrt{N}\) argument with: “we evaluate k_s in {100, 300, 1000} and cap in {5,10,20,50}” (or similar) and show how the overhead ratio changes. This would make the comparator more robust and less dependent on a contested heuristic.

5. **Add a short validation experiment at the packet/MAC level for the coordinator ingress TDMA vignette (even if simplified).**  
   You already list this as future work, but one minimal experiment (e.g., compute slot schedule feasibility with propagation uncertainty + guard times; or a toy ns-3 TDMA link with γ estimation) would substantially strengthen the credibility of the 21–25 kbps recommendation and the chosen γ range.