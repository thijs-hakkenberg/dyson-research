---
paper: "02-swarm-coordination-scaling"
version: "cu"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-05"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript targets an important and under-served niche: *parametric, closed-form sizing* of hierarchical coordination traffic for very large spacecraft swarms under a strict per-node information budget, with an explicit bridge to TDMA schedulability. The “rate ladder” (info-rate → MAC/slot efficiency → half-duplex partitioning → schedulability margin → recommended PHY) is a useful engineering artifact, and the explicit statement that results are *per-cluster preliminary design estimates* (not externally validated) is appropriately candid.

Novelty is strongest in (i) the two-test feasibility framing tied to a standards-grounded \(\gamma(R_{\text{PHY}})\) and (ii) the practitioner-oriented sizing workflow (Algorithm 1 + tables). However, much of the “validation” remains internal consistency checking across tools built from the same assumptions; without independent empirical anchoring, the paper’s contribution is best positioned as a *design methodology / sizing heuristic* rather than a predictive performance study.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The decomposition into Layer 1 byte budget and Layer 2 TDMA airtime is directionally sound and generally well executed. The manuscript improves over common pitfalls by: (a) separating logical per-node info budgets from PHY rate, (b) explicitly modeling slot timing and fixed-time overheads, and (c) emphasizing that “\(C_{\text{raw}}=C_{\text{info}}/\gamma\)” is a conversion, not a third feasibility test.

Concerns remain: (i) the DES is “cycle-aggregated,” so it cannot substantiate claims about slot-level contention, queueing within a cycle, or realistic ARQ dynamics; (ii) the GE model’s coherence-time assumption is acknowledged but still drives strong conclusions; (iii) several key parameters (acquisition time, guard, ACK placement, half-duplex turnaround) are asserted with limited evidence and materially affect the 30 vs 35 kbps recommendation.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Internal logic is mostly consistent, and the manuscript explicitly flags boundary conditions and non-modeled effects. The “stress-case \(\eta_S \approx 46\%\)” is now better contextualized as a continuous-duty upper bound, and the campaign duty factor \(d\) is a reasonable abstraction for episodic command campaigns.

Remaining logic gaps are primarily about *coupling* that the framework currently suppresses:
- The three-layer story (byte budget, MAC efficiency, TDMA airtime) is presented as two tests plus a heuristic, but in practice the user must avoid double-counting and must understand when each is binding. The paper tries to address this with the boxed note, yet the narrative still occasionally oscillates between “two-layer” and “rate ladder” as if they were independent checks.
- The ARQ feasibility argument mixes (a) a *structural* result from GE coherence across a cycle with (b) a *time-budget* result (reserved retransmission slots). Those are different mechanisms; the paper should separate “channel mixing makes intra-cycle ARQ ineffective” from “even if ARQ were useful, it may not fit in the margin.”

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
Overall organization is strong for a long paper: clear notation, explicit “what is modeled vs not,” and a helpful claim-evidence tier table. The revised upfront statement about Model C vs Model S and the “common mistake” warning materially improve reader comprehension.

That said, the manuscript is dense and sometimes repetitive (multiple places restate the 24/30/35 kbps conclusion). Some key definitions are easy to misread:
- \(\eta\) excludes baseline telemetry but \(\eta_{\text{total}}\) includes it; this is fine, but many readers will instinctively interpret “overhead” as *including* baseline. Consider renaming \(\eta\) to “coordination overhead beyond baseline” or similar throughout figures/tables.
- \(\alpha_{\text{RX}}\) is “derived from schedule,” but it is then used in Eq. (coord_phy) as if it were a quasi-parameter; reinforce that \(\alpha_{\text{RX}}\) is not free and is itself a function of \(R_{\text{PHY}}, \gamma, k_c, S\), and chosen superframe structure.

---

## 5. Ethical Compliance  
**Rating: 4 (Good)**  
Data/code availability is commendably explicit (repo + tag + environment). AI disclosure is present and appropriately scoped (ideation/editing only). No human/animal subjects; no obvious dual-use red flags beyond generic autonomy.

One improvement: provide a minimal reproducibility checklist in the repository (exact command lines / configs to regenerate key tables/figures, and deterministic seeds for at least one canonical run), because the paper relies heavily on simulation artifacts.

---

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
The paper is plausibly within T-AES scope (space comms + autonomy + distributed coordination). Referencing is broad, but some citations are either non-archival (Kuiper pages, DARPA program pages) or only loosely connected to the quantitative parts. More importantly, several literatures that would strengthen the technical positioning are underused:
- Deterministic TDMA schedulability / real-time analysis (e.g., network calculus applications to TDMA, or classic satellite DAMA/TDMA analyses beyond DVB-RCS2).
- Space link layer/MAC literature for inter-satellite links and Proximity-1-like implementations (measured acquisition/turnaround/slot efficiency where available).
- Queueing models for ON/OFF sources and MMPP/D/1 buffer tails (since you explicitly claim DES value there).

---

# Major Issues

1. **The “three-layer feasibility framework” is conceptually right but operationally ambiguous; risks double-counting and misapplication.**  
   **Why it matters:** Practitioners will use this as a sizing recipe. If they treat byte budget, MAC efficiency, and TDMA airtime as separate independent constraints, they can (i) incorrectly declare infeasibility or (ii) miss a binding constraint. The manuscript partially addresses this (“common mistake” box) but still mixes the layers in narrative and tables.  
   **Remedy:**  
   - Make the framework *explicitly two tests* (A: information byte budget; B: time schedulability) and demote “MAC efficiency” to a *derived mapping* inside Test B.  
   - Add a short “Worked sizing example” (one page, step-by-step) showing exactly how a reader goes from \((k_c,S,T_c)\) to \(R_{\text{PHY}}\) without applying both Eq. (coord_phy) and slot-level ingress again.  
   - Add a decision tree: “If \(R_{\text{PHY}}\ge 10\) kbps/node regime → TDMA check not needed; else do Test B.”

2. **\(\gamma\) unification (0.76 CCSDS-grounded replacing earlier 0.85) appears mostly consistent, but the paper still contains subtle cross-rate inconsistencies and a practitioner hazard: \(\gamma\) is rate-dependent and *decreases* with \(R_{\text{PHY}}\).**  
   **Why it matters:** Many engineers assume higher PHY rate increases usable throughput proportionally. Here, fixed-time overheads mean \(\gamma(R)\) decreases with rate, which can surprise readers and can invert intuitions in optimization studies. Any inconsistency in which \(\gamma\) is used where will directly shift the 30 vs 35 kbps conclusion.  
   **Remedy:**  
   - Add a single authoritative table of \(\gamma(R)\) values used everywhere (24/30/35/50) and ensure every downstream numeric example cites it.  
   - In Algorithm 1, ensure that \(T_{\text{slot}}\) computation is *identical* to Eq. (gamma_time) and Table gamma decomposition (currently there is risk of mismatch because line 5 uses \((S\times 8 + O_{\text{frame}})/(R_{\text{FEC}}R_{\text{PHY}})\), while Eq. (gamma_time) treats payload and FEC parity separately and frames as FEC-coded; these are equivalent only if carefully defined—spell out equivalence or align expressions verbatim).  
   - Add a brief “rate paradox” note: increasing \(R_{\text{PHY}}\) reduces slot time but also reduces \(\gamma\); show net effect remains favorable for your parameter range.

3. **Campaign duty factor \(d\) improves workload realism, but its mapping to operations remains weak and could be misread as “hand-waving away” the stress case.**  
   **Why it matters:** The central critique of prior versions (implied by your prompt) is realism of continuous command load. You now state the 46% case is episodic (<1% time), but the derivation of that “<1%” mixture and its dependence on mission type (orbit raising vs station keeping vs collision avoidance) is not rigorous.  
   **Remedy:**  
   - Provide an explicit formula for time-weighted utilization and show one or two mission archetypes (e.g., initial deployment month vs steady-state year) with justified \(d\) values and durations.  
   - Clarify whether \(d\) gates *command generation at the coordinator* only, or also affects reporting (status/alerts). If only commands, say so consistently.  
   - Consider adding a sensitivity plot: \(\eta(d)\) and (separately) buffer multiplier \(M(d)\) for correlated ON/OFF campaigns to show how quickly tails worsen.

4. **Stress-case \(\eta_S \approx 46\%\) is now labeled as a continuous-duty upper bound, but the manuscript still uses it rhetorically in ways that blur “upper bound” vs “representative.”**  
   **Why it matters:** Readers may quote “67% total utilization” as typical. This affects perceived feasibility and could draw reviewer skepticism.  
   **Remedy:**  
   - Rename “stress” to “continuous-duty bound” throughout, and reserve “stress test” for short bursts with explicit \(d\ll 1\).  
   - In the abstract and conclusion, keep the 46% number but always pair it with the episodic duty factor statement and a concrete example (e.g., “orbit-raising for X days → \(d\approx 0.05\)”).

5. **DES verification value remains limited; it mostly confirms equations and adds one tail plot under a specific burst model.**  
   **Why it matters:** A top-tier journal will ask: what does the DES contribute beyond closed-form? You state the incremental value is distributional tails, but the tail result depends heavily on the assumed campaign ON/OFF process and drop-tail buffer model.  
   **Remedy:**  
   - Strengthen the DES contribution by adding at least one additional burstiness model (e.g., heavy-tailed ON durations or clustered events) and show how buffer sizing multiplier \(M\) changes.  
   - Alternatively, replace/augment DES tail claims with an analytic approximation (MMPP/D/1 bounds or Kingman-style approximations) to generalize beyond the chosen ON/OFF process.  
   - If you keep only one burst model, clearly label the buffer rule as “illustrative” and avoid presenting \(M=1.30\) as broadly applicable.

6. **Packet-level validation (Section IV-J) is not independent validation; it is parameter anchoring, and this limits the strength of the 35 kbps recommendation.**  
   **Why it matters:** You correctly disclaim this, but the paper still leans heavily on “CCSDS-grounded” \(\gamma\) as if it were a validated efficiency. In practice, acquisition time distributions, ranging, and implementation details can dominate.  
   **Remedy:**  
   - Reframe IV-J as “standards-based parameterization” and remove any language that could be interpreted as validation.  
   - Provide a bounded uncertainty analysis: treat \(T_{\text{acq}}\) and \(T_{\text{guard}}\) as random variables (or ranges) and propagate to \(R_{\text{PHY,min}}\) with a simple worst-case or percentile approach. Fig. margin_sensitivity is a start; make it central to the recommendation, not auxiliary.

7. **Generalized \(\gamma\) expression is useful, but the paper does not fully capitalize on it for practitioners.**  
   **Why it matters:** Eq. (gamma_time) is one of the most reusable artifacts. Practitioners need a clear “plug-in” recipe and warnings about common pitfalls (whether framing is FEC-coded, what counts as acquisition, whether guard includes ACK, etc.).  
   **Remedy:**  
   - Add a short “How to measure/estimate each term” table: \(T_{\text{acq}}, T_{\text{guard}}, O_{\text{frame}}, R_{\text{FEC}}\), and whether ACK fits inside guard.  
   - Provide a ready-to-use spreadsheet-style formulation or a small pseudocode snippet that mirrors the repository implementation.

---

# Minor Issues

1. **Algorithm 1:** line 3 uses \(\eta_0=5\%\) as fixed; but \(\eta_0\) depends on \(k_c\) via summary amortization (0.4% at \(k_c=100\)). Either parameterize \(\eta_0(k_c)\) or explicitly state you conservatively fix it.  
2. **ACK-in-guard claim:** Table “superframe” footnote says ACK mini-slot is transmitted “within the jitter sub-slot.” This is nonstandard and could be contentious; at minimum, clarify timing diagram and whether ACK requires additional turnaround or guard.  
3. **24 kbps infeasibility numbers:** Table rate_feasibility shows ingress 11,108 ms and margin -1,300 ms, while earlier text cites ingress 11,435 ms and -1,635 ms. Reconcile (different inclusion of egress? rounding?); this is exactly the kind of inconsistency reviewers flag because it affects the main conclusion.  
4. **\(\gamma\) at 35 kbps worked example:** you compute \(T_{\text{FEC}}=293/35000\) ms but earlier FEC parity bits for 256B payload at 7/8 is 308 bits (Table gamma_decomposition). Ensure parity-bit computation is consistent across rates (it should scale with payload bits; if shortened/punctured, explain).  
5. **Terminology:** “coordinator ingress” vs “TDMA ingress” vs “RX fraction” could be standardized; consider a diagram showing the superframe segments and mapping to variables.  
6. **Fleet reuse factor \(R\):** currently an order-of-magnitude argument; consider moving it to limitations earlier or reduce its prominence in main results to avoid over-claiming fleet-scale feasibility.  
7. **Non-archival references:** Several program web pages are fine for context but should not be used to support quantitative claims.  
8. **Baseline 20.5%:** This is a critical anchor; consider a one-line derivation in the text near Eq. (eta_canonical) (256B per 10s at 1 kbps).  
9. **Exception reporting AoI:** You present Eq. (aoi_analytic) as upper bound under i.i.d. sampling; consider explicitly stating that in correlated event processes AoI tails can be heavier.  
10. **Units:** Ensure consistent kbps vs kbit/s vs bps, and “information-rate” vs “PHY-rate” labeling in all tables.

---

## Overall Recommendation  
**Recommendation:** **Major Revision**

The manuscript has strong potential as a *design-equations / sizing-methodology* paper for hierarchical swarm coordination links, and the revisions addressing workload realism (via duty factor \(d\)), explicit Model C vs Model S separation, and CCSDS-grounded \(\gamma\approx 0.70\text{–}0.76\) are meaningful improvements. The central engineering conclusion—24 kbps infeasible, 30 kbps minimum, 35 kbps recommended under stated timing and ARQ needs—is plausible and presented in a practitioner-friendly “rate ladder.”

However, for a top-tier aerospace systems journal, the paper still needs tighter internal consistency on the key numbers (24/30/35 kbps margins, parity/framing timing), clearer operationalization of the feasibility framework to prevent misuse, and a stronger justification of the workload duty factor mapping. The DES/slot-sim components should either be strengthened to provide insight beyond equation confirmation (e.g., robustness to alternative burstiness models) or their claims should be narrowed further. Finally, Section IV-J must be positioned unambiguously as parameterization/anchoring rather than validation, with uncertainty propagation elevated to support the PHY recommendation.

---

## Constructive Suggestions (ordered by impact)

1. **Add a worked end-to-end sizing example** (single canonical case + one sensitivity case) that walks through Test A and Test B without double-counting, and explicitly shows where \(\gamma(R)\) enters.  
2. **Reconcile all timing/feasibility numbers** for 24/30/35 kbps in one authoritative table derived from one authoritative slot-time equation; ensure text references match.  
3. **Strengthen the \(d\) mapping**: provide mission-phase durations and compute time-weighted \(\eta\) for at least two archetypal missions (deployment vs steady-state), plus a sensitivity to \(d\).  
4. **Elevate uncertainty analysis**: treat \(T_{\text{acq}}\), \(T_{\text{guard}}\), and achieved \(\gamma\) as ranges/distributions and propagate to \(R_{\text{PHY,min}}\); make this the basis of the 35 kbps recommendation.  
5. **Clarify ARQ conclusions** by separating (i) channel-mixing effectiveness (GE coherence) from (ii) time-budget feasibility (reserved slots). Consider presenting two recommended operating modes: “no intra-cycle ARQ + inter-cycle recovery” vs “reserved ARQ slots,” with explicit AoI/throughput trade.  
6. **Broaden DES tail evidence**: add at least one alternative burstiness model or provide an analytic approximation for MMPP/D/1 tail/buffer sizing to generalize beyond the chosen ON/OFF process.  
7. **Make \(\eta_0\) parameterized** (at least as a function of \(k_c\)) in Algorithm 1 and the sizing equations summary, or clearly state conservative bounding.  
8. **Provide a practitioner measurement table for Eq. (gamma_time)** describing how to obtain each term from modem logs/bench tests and what typical ranges are.