---
paper: "02-swarm-coordination-scaling"
version: "cr"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-04"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript targets an important and under-served design question: how to *size* coordination communications for very large (10³–10⁵) autonomous swarms using closed-form relationships rather than only bespoke simulations. The two-layer feasibility framing (message-layer byte budget + TDMA airtime schedulability) is a useful organizing contribution, and the “rate ladder” that translates a per-node info budget into a coordinator PHY recommendation is practitioner-relevant. The explicit separation of baseline telemetry from protocol overhead is also valuable and clearer than many prior constellation “bandwidth” papers.

Novelty is moderate rather than high: hierarchical aggregation, AoI, GE loss, and TDMA efficiency modeling are individually well-known. The paper’s novelty is in integrating them into a coherent sizing procedure with explicit parameters (e.g., \(d, q, k_c, \gamma\)) and making the coordinator-ingress bottleneck and half-duplex superframe constraints explicit.

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The analytical accounting is mostly consistent and the layering is conceptually sound. The slot-efficiency derivation anchored to CCSDS Proximity-1 framing is a reasonable *parameter estimate* approach, and the paper is candid that it is not measured validation. The DES is appropriately scoped for message-layer distributions and campaign burstiness, and the slot-level simulator is the right tool to expose TDMA/ARQ coupling.

However, several methodological choices still limit scientific strength: (i) the DES largely verifies equations it shares; (ii) the GE model is a design assumption without calibration; (iii) the TDMA schedule assumptions (centralized scheduling, perfect sync, no contention, no co-channel interference within a channel) are strong and not stress-tested; and (iv) queueing/processing models are asserted but not tightly connected to results (e.g., the MMPP/D/1 mention is not used to derive bounds).

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Internal logic is improved versus earlier versions (as implied by the CR notes): you now clearly (a) contextualize the \(\eta_S\approx 46\%\) case as a continuous-duty upper bound with \(d\ll 1\) in realistic operations, (b) distinguish Model C vs Model S and state that decisions use Model C, and (c) avoid double-counting by explicitly labeling \(C_{\text{raw}}=C_{\text{coord,info}}/\gamma\) as a conversion.

Remaining validity concerns are about boundary conditions and hidden coupling: \(\alpha_{\text{RX}}\) is “derived from schedule,” but the schedule itself is implicitly designed around fitting ingress; ARQ slot reservation and ACK-in-guard assumptions are delicate; and feasibility conclusions depend strongly on the assumed acquisition/guard constants and on the interpretation of “per-slot acquisition” versus “per-superframe tracking.”

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
The paper is generally well structured, with clear definitions (Layer 1 vs Layer 2), a helpful notation table, and a coherent “rate ladder.” The explicit “do not double-count” box is excellent. The campaign duty factor \(d\) is now framed in an operationally interpretable way (Table of duty mappings + mixture example), which directly addresses workload realism concerns.

Some sections remain dense and occasionally repetitive (e.g., multiple restatements of 30 kbps minimum / 35 kbps recommended). A few claims are easy to misread because Model S results appear in prominent tables (e.g., Table IV-D) even with footnotes; readers may still propagate the wrong feasibility conclusion.

## 5. Ethical Compliance  
**Rating: 4 (Good)**  
Strong data availability statement with code and tag; explicit AI disclosure; clear statement that results lack external validation. This is unusually good for the area.

Two items to tighten for reproducibility: specify exact commit hash in addition to tag; provide a manifest of scripts to regenerate each figure/table, and document random seed handling for bootstrap CIs and Monte Carlo replications.

## 6. Scope & Referencing  
**Rating: 4 (Good)**  
The manuscript fits IEEE TAES / Adv. Space Res. scope: comms sizing, autonomy-supporting architectures, and swarm/constellation operations. Referencing is broad and mostly appropriate (CCSDS, AoI survey, DTN, routing, SWIM/Raft, DVB-RCS2).

Gaps: more direct engagement with (i) TDMA/DAMA scheduling literature in satellite return links beyond a single DVB-RCS2 reference (e.g., performance impacts of acquisition bursts, synchronization overheads, and demand assignment), (ii) LEO ISL MAC studies (even if optical-focused), and (iii) queueing-tail approximations for ON/OFF sources (to support the “1.15–1.30× mean” buffer heuristics more rigorously).

---

# Major Issues

1) **Three-layer feasibility framing is stated, but the “third layer” (MAC efficiency) still risks conceptual confusion**  
**Why it matters:** You emphasize a “two-layer” framework (byte budget + airtime), but also introduce \(1/\gamma\) conversions and “rate ladder” steps that can be misinterpreted as an additional feasibility constraint. Practitioners may double-apply \(\gamma\) or treat \(C_{\text{raw}}\) as a separate test.  
**Remedy:**  
- Make the framework explicitly *two constraints + one conversion* everywhere. Consider renaming “Layer 2” to “Airtime schedulability,” and label \(\gamma\) strictly as a *slot-structure conversion factor* used inside Layer 2.  
- In Algorithm 1, rewrite to compute airtime directly from slot time (line 4/5) and remove any implication that \(C_{\text{raw}}\) is separately checked.

2) **\(\gamma\) unification (0.76/0.745 CCSDS-based) is mostly consistent, but there are still places where Model S results may leak into conclusions**  
**Why it matters:** The manuscript is making a design recommendation (35 kbps) that is sensitive to \(\gamma\) and slot timing. Any ambiguity about which model underlies which claim undermines trust. Table IV-D (joint interaction) uses Model S; readers may incorrectly infer 24 kbps viability under “no loss.”  
**Remedy:**  
- Visually watermark Model S tables/figures (“Upper-bound timing model; not design-valid”) and move Table IV-D to an appendix or explicitly title it “Coupling demonstration under relaxed timing (Model S).”  
- Add a one-line “decision table” listing which sections/tables are Model C-only, and which are Model S demonstrations.

3) **Campaign duty factor \(d\) improves workload realism, but the mapping from real operations to \(d\) remains partly ad hoc and cluster-correlation assumptions are under-justified**  
**Why it matters:** Your headline “routine \(\eta\approx 5\)–10%” depends on \(d\) and the assumed correlation scope (node/cluster/regional). Without clearer grounding, reviewers will see \(d\) as a tunable knob that can make any architecture look feasible.  
**Remedy:**  
- Provide at least one end-to-end worked example from a published operational concept (e.g., a station-keeping cadence + orbit-raising campaign + anomaly response) that yields \(d\) and correlation scope from first principles.  
- Report sensitivity of buffer tails and \(\eta\) to (a) \(L_{\text{on}}\) and (b) correlation scope, in a compact plot/table, and state recommended conservative choices.

4) **Stress-case \(\eta_S\approx 46\%\) is better contextualized, but the paper still mixes “continuous-duty bound” with “episodic worst-case” in ways that could be misread**  
**Why it matters:** A 46% protocol overhead (67% total including baseline) is alarmingly high at 1 kbps/node; if a reader believes this is typical, they may dismiss the architecture. Conversely, if it is truly <1% of time, the system must demonstrate safe behavior during those bursts.  
**Remedy:**  
- Make the stress case explicitly a *design envelope point* and present a “time-at-load” chart (even schematic) showing the mixture model already described in text.  
- State what happens operationally when stress bursts occur: what degrades first (AoI, command latency, drops), and what safety mechanisms apply.

5) **DES verification value: currently framed correctly as code verification, but still occupies substantial narrative weight without delivering independent insight beyond the distribution tails**  
**Why it matters:** Top-tier journals will discount simulation that reproduces its own equations. Your strongest DES value is tail/buffer sizing under correlated campaigns; everything else should be minimized or repositioned.  
**Remedy:**  
- Compress mean-agreement discussion to a short V&V paragraph; move extensive “DES matches <0.1%” statements to an appendix.  
- Expand the distributional contribution: quantify how tail multipliers vary with \(d\), \(L_{\text{on}}\), and GE parameters, and provide a simple practitioner rule (e.g., buffer multiplier as a function of \(d\) and correlation length).

6) **Packet-level/standards-based \(\gamma\) derivation is a parameter estimate, not independent validation; the manuscript states this, but the “validated via CCSDS” phrasing remains too strong**  
**Why it matters:** “Validated” implies empirical confirmation. Here you compute \(\gamma\) from nominal framing and assumed acquisition/guard. That is anchoring, not validation. Over-claiming will trigger reviewer pushback.  
**Remedy:**  
- Replace “validated via CCSDS” with “anchored to CCSDS framing assumptions” throughout (abstract, intro bullets, conclusions).  
- Add a short uncertainty analysis: treat \(T_{\text{acq}}\) and \(T_{\text{guard}}\) as distributions and propagate to \(R_{\text{PHY,min}}\) to show robustness of the 35 kbps recommendation.

7) **ARQ×TDMA coupling result is interesting but depends on a specific ARQ design (reserved retransmission slots, ACK-in-guard) and GE coherence assumptions**  
**Why it matters:** The conclusion “ARQ infeasible at 30 kbps” is contingent. Alternative designs (no intra-cycle ARQ, HARQ, selective repeat across cycles, piggyback ACKs, or fewer reserved slots) can change the feasibility boundary.  
**Remedy:**  
- Clearly label the ARQ policy as one design point and state what class of ARQ strategies the conclusion applies to.  
- Add at least one alternative policy comparison (even analytically): e.g., “no intra-cycle ARQ, inter-cycle only” vs “intra-cycle stop-and-wait,” with AoI/latency trade.

8) **Generalized \(\gamma\) expression is useful, but practitioner usability is limited by parameter ambiguity (what exactly is \(T_{\text{acq}}\) per slot vs per frame?)**  
**Why it matters:** Practitioners need to map their modem behavior to your terms. Misinterpreting acquisition/tracking can shift \(\gamma\) materially and invalidate the 30/35 kbps boundary.  
**Remedy:**  
- Provide a small taxonomy table: “cold-start per slot,” “reacquire per burst,” “continuous tracking,” with typical \(T_{\text{acq}}\) and how to measure it.  
- Include a measurement recipe: how to estimate \(\gamma\) from radio logs (slot start-to-end vs payload time).

---

# Minor Issues

1) **Terminology:** avoid “validated via CCSDS” (use “anchored/derived from CCSDS framing”).  
2) **Algorithm 1, line 3:** the expression for \(\eta_{\text{total}}\) mixes \(p_{\text{cmd}}\) and \(d\); earlier you define \(\eta=\eta_0+d\eta_{\text{cmd}}\). Ensure \(p_{\text{cmd}}\) is consistently defined (probability per cycle vs per-node fraction) and not double-counted with \(d\).  
3) **\(\alpha_{\text{RX}}\) definition:** sometimes described as “derived from schedule,” but then used to compute \(R_{\text{PHY,min}}\). Consider defining the schedule first, then deriving \(\alpha_{\text{RX}}\) deterministically from ingress slots + reserved ARQ slots.  
4) **Table IV-A feasibility ladder:** clarify whether the 20.2 kbps “info-rate” includes coordinator’s own report or only members (you use \(k_c-1\)).  
5) **Guard/ACK statement in Table IV-C footnote:** “ACK transmitted within jitter sub-slot” is nonstandard and could be contentious; add a short timing diagram or move to appendix.  
6) **GE model:** you state transitions occur once per \(T_c\); explicitly note that this makes intra-cycle ARQ ineffective by construction when \(\tau_c\ge T_c\).  
7) **Fleet reuse (R=3) justification:** currently an order-of-magnitude argument; fine, but label it as such more prominently and avoid implying sufficiency for all antenna patterns.  
8) **AoI mission coupling:** the comparison to a 24h TCA window is helpful, but also mention tighter control loops (formation keeping) where 440 s tails are unacceptable—then clarify that those use periodic reporting or optical ISL.  
9) **Reference hygiene:** several “non-archival accessed Feb 2026” references are acceptable in moderation, but consider adding more archival sources for constellation operations and TDMA efficiency.  
10) **Units:** ensure consistent kbps meaning (information vs PHY). You do a good job overall, but a few sentences still read ambiguously.

---

# Overall Recommendation  
**Recommendation:** **Major Revision**

The manuscript has a strong practitioner-oriented core: a clean separation between byte-budget feasibility and TDMA airtime feasibility, a standards-anchored way to compute \(\gamma\), and a clear explanation of why coordinator ingress—not fleet size per se—sets the S-band coordination-channel sizing. The revised version appears to have materially improved workload realism via the campaign duty factor \(d\), corrected/updated the \(\gamma\) value to the CCSDS-anchored 0.74–0.76 range, and more responsibly framed the \(\eta_S\approx 46\%\) stress case as a continuous-duty bound rather than typical operations.

However, for a top-tier journal, the paper still over-relies on internal consistency checks (DES vs closed-form) and remains vulnerable to misinterpretation around Model S vs Model C, “validation” language around \(\gamma\), and the contingency of the ARQ×TDMA coupling result on specific protocol/timing assumptions. The contribution is promising and likely publishable, but it needs sharper boundary conditions, clearer operational mapping for \(d\), and a more rigorous presentation of what is *demonstrated* versus what is *assumed*.

---

# Constructive Suggestions (ordered by impact)

1) **Tighten claims and language around validation:** replace “validated” with “anchored/derived,” and add a short uncertainty propagation for \(T_{\text{acq}}, T_{\text{guard}}, \gamma\) → \(R_{\text{PHY,min}}\).  
2) **Make Model C dominance unmissable:** move Model S coupling demo to appendix or heavily label it; add a one-page “Which model underlies which figure/table” map.  
3) **Strengthen the duty-factor realism:** add one or two operationally grounded duty-factor derivations (with cited cadences) and provide sensitivity to correlation length/scope.  
4) **Expand the *unique* DES value:** focus DES results on tails/buffers under correlated ON/OFF + GE, and provide a compact sizing rule; de-emphasize mean matching.  
5) **Broaden ARQ policy discussion:** present at least one alternative (inter-cycle-only recovery) as a first-class design option and quantify the AoI/latency trade.  
6) **Improve practitioner usability of generalized \(\gamma\):** add a taxonomy + measurement recipe for estimating \(\gamma\) from real modem behavior/logs.  
7) **Clarify Algorithm 1 and parameter definitions:** ensure \(d\), \(p_{\text{cmd}}\), and \(f_{\text{decision}}\) are not overlapping knobs; unify notation and provide a minimal worked example running the algorithm.