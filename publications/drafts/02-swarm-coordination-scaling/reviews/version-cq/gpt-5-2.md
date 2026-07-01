---
paper: "02-swarm-coordination-scaling"
version: "cq"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-04"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript targets an important gap: providing *closed-form* sizing relationships for hierarchical coordination traffic and TDMA schedulability at \(10^3\)–\(10^5\) nodes, with byte-level accounting and explicit separation of message-layer utilization (\(\eta\)) from slot-structure efficiency (\(\gamma\)). That decomposition—plus an explicit “rate ladder” from info-rate to PHY-rate—is practically valuable for early mission design. The novelty is strongest in (i) the three-part feasibility logic (byte budget, MAC/slot efficiency, and superframe airtime) and (ii) the explicit coordinator-ingress bottleneck quantified to a narrow S-band rate range.

That said, the paper’s novelty is **more “engineering synthesis + parametric design equations” than “new theory”**, and the authors correctly acknowledge limited external validation. For a top-tier journal, the contribution is still potentially publishable, but only if the validation story and the scope of claims are tightened so the work is clearly positioned as a *design methodology* rather than a predictive performance model.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The modeling choices are generally reasonable for a sizing paper: cycle-aggregated DES for message-layer distributions, a slot-level simulator for TDMA deadline misses and ARQ coupling, and analytic cross-checks for means/tails (AoI geometric tail; Markov recovery under GE). The canonical overhead definition (baseline excluded from \(\eta\)) is a welcome clarification.

However, several methodological aspects remain underjustified or internally fragile: (i) the GE model is explicitly not calibrated, yet it is used to motivate the 35 kbps recommendation via ARQ margin; (ii) the “packet-level validation” is not truly independent—it is a *standards-derived calculation* of \(\gamma\), not a measured/implemented framing efficiency; (iii) the slot model’s handling of ACK “inside guard” is unconventional and needs a more defensible timing diagram and rationale; and (iv) the DES queueing claims (MMPP/D/1 tails) are plausible but not supported by either fitted models or sensitivity to buffer policy/priority classes.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
The paper is largely logically consistent and improves over earlier versions by explicitly stating boundary conditions and avoiding double counting (\(C_{\text{raw}}=C_{\text{info}}/\gamma\) as unit conversion). The duty-factor \(d\) is now clearly presented as a campaign-level gating mechanism, and the stress case is labeled as an upper bound.

Remaining validity concerns are mainly about **what is being claimed vs. what is proven**:
- The 35 kbps recommendation is presented as robust, but it partly rests on ARQ demand estimates under an assumed GE coherence structure (\(\tau_c \ge T_c\)). If that assumption is wrong (or if ARQ is designed differently), the recommendation can shift materially.
- The “three-layer feasibility framework” is described as byte budget + MAC efficiency + TDMA airtime, but in practice MAC efficiency is not a separate feasibility layer; it is a parameter feeding the airtime test. The manuscript states this (“Do not double-count”), but the presentation still risks confusing readers.
- Some rate-dependent \(\gamma\) values (e.g., \(\gamma_{50}=0.695\)) appear counterintuitive given Eq. (31): with fixed time overheads, \(\gamma\) typically *increases* with PHY rate. If you are instead changing acquisition/guard/framing assumptions with rate, that dependency must be explicitly defined and justified.

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
Overall structure is strong: clear notation table, explicit “Model C vs Model S” statement up front, a well-organized results roadmap, and repeated reminders about what is and is not validated. Tables like the rate ladder and superframe budget are particularly helpful to practitioners.

Clarity issues remain in a few high-stakes places:
- The definition and usage of \(\gamma\) across sections must be audited for consistency (24 vs 30 kbps values, and the rate-dependence logic).
- The distinction between “coordination channel,” “per-node logical budget,” and “coordinator ingress PHY” is improved but still easy to misread; a single consolidated diagram showing these rates/allocations would reduce ambiguity.
- Section IV-D (joint interaction) uses Model S and then relies on Model C for feasibility claims; this is acceptable but needs even more explicit framing to prevent readers from misquoting the 24 kbps results.

---

## 5. Ethical Compliance  
**Rating: 5 (Excellent)**  
Strong data availability statement with code tag, environment, and runtime. Clear AI disclosure (ideation/editing only, not results). No human/animal subjects. The manuscript is unusually transparent about validation gaps and limitations, which is commendable.

One suggestion: include a reproducibility checklist itemizing (i) exact commit hash/tag (already given), (ii) command lines/scripts to regenerate each key figure/table, and (iii) random seeds used for the figures in the paper.

---

## 6. Scope & Referencing  
**Rating: 4 (Good)**  
The paper is within scope for IEEE TAES / ASR as a systems/architectures + comms sizing contribution. Referencing is broad and mostly appropriate (CCSDS, AoI, DTN, mega-constellation routing, swarm robotics, queueing).

Gaps:
- More direct engagement with **satellite TDMA/DAMA** literature beyond DVB-RCS2 would help (e.g., return-link scheduling analyses, superframe design, or CCSDS scheduling guidance if available).
- For correlated loss, GE is fine, but readers will expect at least a nod to **burst-error channel coding/interleaving** and why it is not considered (or how it would map into \(\gamma\) and/or effective \(p_G,p_B\)).
- For AoI, consider citing work on AoI under losses and retransmissions (beyond the survey) if you are drawing operational conclusions.

---

# Major Issues

1) **“Packet-level validation” is not independent validation; it is parameter anchoring.**  
**Why it matters:** The manuscript repeatedly positions CCSDS-based \(\gamma\) as “anchored,” but readers may interpret Section IV-J as empirical validation. In reality it is a standards-derived time accounting (useful, but not validation). For a top-tier journal, this distinction must be unambiguous because the 30/35 kbps recommendation hinges on \(\gamma\).  
**Remedy:**  
- Rename Section IV-J to “Standards-based \(\gamma\) derivation (parameter anchoring)” (you partly do this in the claim map, but align the section title and narrative).  
- Add a short paragraph explicitly stating: “No implemented Proximity-1 modem measurements are used; \(\gamma\) is computed from nominal framing and assumed acquisition/guard.”  
- Provide a small sensitivity table: if \(T_{\text{acq}}\) is 0/2/5/10 ms and guard is 3/5/10 ms, what are \(\gamma\) and \(R_{\text{PHY,min}}\)? (Some of this exists in Fig. 6; make it numerically explicit.)

2) **Rate dependence and consistency of \(\gamma\) needs a full audit (potential internal inconsistency).**  
**Why it matters:** Eq. (31) implies \(\gamma\) depends on payload time vs. (payload + overhead). If overhead times are constant, \(\gamma\) should increase with PHY rate. Yet Table 11 shows \(\gamma_{24}=0.761\), \(\gamma_{30}=0.745\), \(\gamma_{50}=0.695\) (decreasing with rate), which is surprising unless overhead *increases* with rate or the computation changes definitions (e.g., different acquisition assumptions, different framing, or different guard scaling). Any inconsistency here undermines the central “\(\gamma\)-conditional design equation” claim.  
**Remedy:**  
- Add an explicit definition: which terms are constant in *time* vs constant in *bits*, and whether \(T_{\text{acq}}\) and \(T_{\text{guard}}\) are rate-dependent.  
- Include the computed breakdown for 30 and 50 kbps analogous to Table 9 (currently only 24 kbps is decomposed).  
- If \(\gamma_{50}\) is a typo or computed with different assumptions, correct it and regenerate Fig. 7 / Table 11 accordingly.

3) **The “three-layer feasibility framework” should be formalized as two tests + one conversion to avoid conceptual confusion.**  
**Why it matters:** Practitioners may misapply the method by treating \(\gamma\) as a separate “layer” and double-penalizing throughput (you warn against this, but the manuscript still uses “two-layer” and “three-layer” language in different places). Confusion here leads directly to wrong rate sizing.  
**Remedy:**  
- Standardize terminology: either (A) “two-layer feasibility: byte budget (Layer 1) and superframe airtime (Layer 2), with \(\gamma\) as a parameter in Layer 2,” or (B) “three-step sizing: byte budget check, \(\gamma\) computation, airtime check.”  
- Update the abstract and contributions to use the same language consistently.

4) **Campaign duty factor \(d\): improved, but still lacks workload realism linkage and sensitivity to burst structure.**  
**Why it matters:** The paper’s earlier realism concern was that \(\eta_S\approx 46\%\) could be misread as “typical.” Version CQ now states \(d\ll 1\) and gives a mixture example, which is good. But the mapping from real operations to \(d\) is still somewhat ad hoc, and the *burst structure* (ON/OFF correlation length, correlation scope) affects buffers and potentially AoI under drops.  
**Remedy:**  
- Provide a clearer operational derivation for the default \(d=0.10\): e.g., “X reconfiguration days per year, each lasting Y minutes/hours,” or tie it to published Starlink/OneWeb maneuver cadence if available.  
- Expand the sensitivity: keep mean \(d\) fixed but vary \(L_{\text{on}}\) and correlation scope; report impact on (i) buffer exceedance probability and (ii) any induced drop/AoI under finite buffer. Currently you show buffer CDF shifts, but do not connect it to service policy and drop consequences.

5) **ARQ×TDMA coupling result is interesting but not yet decision-grade for the 35 kbps recommendation.**  
**Why it matters:** The 35 kbps recommendation is justified as “accommodating ARQ under GE losses,” but the GE parameters and the ARQ design are both simplified (stop-and-wait, fixed reserved slots, coherence \(\ge T_c\), ACK in guard). A different ARQ (selective repeat, HARQ, interleaving, or simply no intra-cycle ARQ) could change the needed margin.  
**Remedy:**  
- Reframe the recommendation: “35 kbps provides margin for *some* intra-cycle retransmission strategies under slow-mixing loss; if intra-cycle ARQ is disabled, 30 kbps suffices but increases AoI by \(T_c\) per loss event.”  
- Add one additional ARQ policy comparison in the slot-sim: e.g., (i) no intra-cycle ARQ, (ii) intra-cycle ARQ with \(M_r\) reserved, (iii) inter-cycle prioritized retransmission. Report deadline misses and AoI impact for each at 30 and 35 kbps.

6) **ACK-in-guard assumption needs a rigorous timing justification (or removal).**  
**Why it matters:** Guard time is typically reserved to absorb uncertainty; consuming it for deterministic ACKs is possible only if your guard budget explicitly includes a scheduled control sub-slot and the residual uncertainty is still bounded. Otherwise, you are effectively shrinking the guard without accounting for it, which inflates \(\gamma\) and feasibility margin.  
**Remedy:**  
- Provide a precise superframe timing diagram showing: propagation uncertainty, turnaround, jitter margin, and where ACK fits.  
- Alternatively, allocate explicit ACK mini-slots in Table 7 and reflect them in \(\gamma\)/margin. Then redo the margin analysis and confirm 30 vs 35 kbps conclusions remain unchanged.

7) **DES “verification” adds limited scientific value unless tied to decisions beyond mean matching.**  
**Why it matters:** You correctly state that DES reproducing the equations is code verification, not validation. The incremental value is distributional tails under correlated campaigns—but the manuscript stops short of translating those tails into design requirements (buffer sizes, drop probabilities, performance degradation).  
**Remedy:**  
- Add a short “Design implication” subsection: given buffer size \(B\), what is the drop probability under each campaign model, and what is the resulting AoI/availability impact?  
- Alternatively, reduce DES emphasis and focus the paper more tightly on the closed-form equations + slot-level feasibility, if you cannot connect DES tails to outcomes.

---

# Minor Issues

1) **\(\gamma\) unification number:** The prompt mentions “0.76 validated via CCSDS replacing 0.85.” In this version, \(\gamma\approx 0.74\)–0.76 is used; ensure no residual 0.85 references remain anywhere (including figure captions, code defaults, or repository README).  

2) **Table 11 (“PHY Rate Feasibility”)**: clarify why \(\gamma\) decreases with rate (or fix if erroneous). Add a footnote describing which parameters change with \(R_{\text{PHY}}\).  

3) **Algorithm 1 Layer 1 line:** \(\eta_{\text{total}} \leftarrow \eta_0 + d \cdot p_{\text{cmd}} S_{\text{cmd}} \times 8 /(C_{\text{node}}T_c)+\eta_{\text{baseline}}\). But earlier \(\eta_{\text{cmd}}\) already encodes stress-case command load; ensure \(p_{\text{cmd}}\) and \(d\) are not double-gating in some scenarios (stress profile uses \(p_{\text{cmd}}=1\) and \(d=1\)). Consider clarifying intended semantics: \(p_{\text{cmd}}\) within-cycle probability vs campaign-level duty factor.  

4) **Baseline telemetry definition:** baseline is uplink-only node→coordinator, but heartbeat is downlink; ensure \(\eta_0\) accounting is directionally consistent with the TDMA egress time budget (Table 7) and byte budget definitions.  

5) **Spatial reuse argument:** the reuse factor \(R=3\) justification is very approximate. Consider tightening language to “order-of-magnitude plausibility” and clearly label as an assumption requiring RF interference simulation/analysis.  

6) **AoI mission coupling:** statements like “AoI P99 is <0.5% of a 24h TCA window” are fine, but be careful: conjunction assessment often needs timely covariance and intent updates; the relevant timescale may be much shorter than 24h for maneuver execution. You partly note optical ISL for maneuver execution—consider emphasizing that AoI requirements are mission-dependent and your AoI analysis is mainly about coordination telemetry freshness, not collision-avoidance decision latency.  

7) **Terminology:** “mega-constellations” vs “swarms” vs “fleets” is used interchangeably; consider a short definitional sentence early on.

---

## Overall Recommendation  
**Recommendation:** **Major Revision**

The paper has a strong engineering core—especially the explicit coordinator-ingress bottleneck sizing, the separation of byte budget vs airtime, and the clear rate ladder culminating in a 30 kbps minimum / 35 kbps recommended design point under Model C. The manuscript is also unusually transparent about assumptions and the absence of external validation, which is a significant strength for a sizing-oriented contribution.

The main reasons for Major Revision are (i) the central parameter \(\gamma\) shows potentially inconsistent rate dependence and must be made internally watertight; (ii) the “validation” narrative needs tightening so that standards-based calculations are not misconstrued as empirical validation; and (iii) the ARQ×TDMA coupling and duty-factor workload realism need to be connected more directly to decision-grade recommendations (or the claims should be narrowed accordingly). Addressing these points would make the paper a credible, practitioner-oriented design methodology suitable for a top-tier aerospace systems journal.

---

## Constructive Suggestions (ordered by impact)

1) **Fix and fully document \(\gamma(R_{\text{PHY}})\)**: provide decompositions at 24/30/50 kbps, explain which overheads are time-constant vs bit-constant, and ensure Fig. 7/Table 11 align with Eq. (31).  

2) **Recast Section IV-J as “parameter anchoring,” not validation**, and explicitly separate: (a) standards-based accounting, (b) assumed acquisition/guard, and (c) what would be measured in hardware.  

3) **Strengthen the 35 kbps recommendation by policy comparison**: show at least two retransmission strategies and their impact at 30 vs 35 kbps under slow-mixing loss; alternatively, narrow the recommendation to “35 kbps if intra-cycle ARQ is required under burst loss.”  

4) **Make the feasibility framework terminology consistent** (two tests + \(\gamma\) computation), and add a one-page “how to use this” practitioner flow (Algorithm 1 is close—tighten semantics of \(d\) vs \(p_{\text{cmd}}\)).  

5) **Translate DES tail results into design consequences**: buffer size → overflow probability → drop/AoI/availability impact under correlated campaigns.  

6) **Clarify ACK timing**: either allocate explicit ACK time or provide a rigorous guard-budget argument with residual uncertainty.  

7) **Expand workload realism mapping**: provide a clearer empirical basis for default \(d\), and add sensitivity to burst length/correlation scope at fixed mean \(d\).

If the authors address Items 1–4 convincingly (and ideally 5–6), the manuscript would be substantially stronger and much closer to publishable quality in IEEE TAES / ASR.