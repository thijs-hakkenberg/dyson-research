---
paper: "02-swarm-coordination-scaling"
version: "ck"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-03"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript tackles a practically important and under-served problem: *parametric sizing* for hierarchical coordination in very large space swarms (10³–10⁵ nodes) with explicit byte accounting and a TDMA schedulability layer. The clearest novelty is the “rate ladder” and the explicit separation of (i) message-layer byte budget/utilization from (ii) physical-layer airtime feasibility, plus the practitioner-facing closed-form equations (notably the generalized \(\gamma(R_{\text{PHY}})\) expression) and the explicit identification of coordinator ingress as the binding bottleneck. The CCSDS-grounded \(\gamma\) anchoring is a meaningful improvement over earlier “assume \(\gamma\)” treatments and materially changes conclusions (24 kbps infeasible; 30 kbps minimum; 35 kbps recommended).

That said, the work remains primarily a *design-estimation framework* with internal consistency checks rather than an empirically validated predictive model. For a top-tier aerospace systems journal, the contribution is still publishable, but the narrative must be disciplined: it should be positioned as a sizing methodology + sensitivity/design curves, not as a validated performance claim about real ISLs.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The methodology is generally coherent: analytical sizing → cycle-aggregated DES for distributions/queue tails → slot-level TDMA simulator for airtime feasibility and ARQ coupling → packet-level CCSDS framing to anchor \(\gamma\). The separation of tool scopes is well stated and helps avoid a common pitfall (DES “validating” its own equations).

However, several modeling choices materially affect conclusions and need stronger justification or sensitivity: (a) acquisition modeling (per-slot cold-start vs amortized), (b) half-duplex partitioning via \(\alpha_{\text{RX}}\) being treated as a near-fixed scalar derived from a particular schedule, (c) GE coherence tied to \(T_c\) (conservative in one sense, optimistic in another), and (d) the “command semantics” assumption that makes \(\eta_{\text{cmd}}\) topology-invariant. These are acceptable as *assumptions*, but the method would be more sound if the paper provided clearer “if/then” boundaries (when each assumption holds) and showed sensitivity where conclusions flip (e.g., 30 vs 35 kbps depends strongly on acquisition amortization and ARQ policy).

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Internal logic is mostly consistent and improved relative to what is implied as earlier versions:  
- The campaign duty factor \(d\) is now explicitly used to contextualize the stress case as a continuous-duty upper bound, and routine \(d\in[0.01,0.10]\) is mapped to operational analogues. This addresses “workload realism” concerns better than a single stress number.  
- The \(\gamma\) unification at 0.761 (CCSDS-derived) is stated clearly and appears consistently applied to key feasibility claims (notably the 24 kbps infeasibility under Model C).  
- The three-step feasibility workflow (byte budget → rate translation → explicit TDMA timing) is a strong logical structure.

Remaining validity concerns are mainly about *interpretation* and *parameter coupling*:  
- The paper sometimes blurs “coordinator ingress info-rate” vs “required PHY rate” vs “TDMA schedule feasibility.” Most of the time it is careful, but there are still spots where a reader could misread “27 kbps” as a PHY requirement rather than “info-rate before \(\alpha_{\text{RX}}\) and schedule overhead.”  
- The AoI P99=440 s result is correctly identified as a *sampling-policy tail*, not network delay; nevertheless, it is presented in summary tables alongside network-driven metrics, which may mislead.  
- The ARQ infeasibility statements are correct *under the specified ARQ scheduling policy and coherence model*, but are at risk of being over-generalized.

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
The manuscript is unusually explicit about definitions (\(\eta\) vs baseline, loss taxonomy, tool scope disambiguation, feasibility steps). Tables such as the rate ladder and superframe budget are strong and practitioner-friendly. The explicit “screening heuristic is not a design criterion” warning is also good.

Areas to improve:  
- The paper is long and occasionally repeats the same conclusion (24 infeasible, 30 minimum, 35 recommended) without adding new evidence. Consider tightening.  
- “Model S vs Model C” is clear, but the paper sometimes uses Model S for ARQ coupling demonstrations while key conclusions are Model C; this is valid but should be signposted more strongly at each such result (“this ARQ coupling example uses Model S slots; Model C would be tighter/looser because …”).  
- Some claims are stated with an engineering certainty tone that conflicts with the explicit “no external validation” caveat. Align tone with evidence tiering.

---

## 5. Ethical Compliance  
**Rating: 4 (Good)**  
Data availability is strong (repo + tag). Reproducibility details (Python versions, libraries, runtime) are provided. AI disclosure is present and reasonably specific (ideation + prose editing only; not used for results). That is appropriate.

One gap: the manuscript should specify exactly what is in the released dataset (raw MC outputs? processed aggregates?) and provide a minimal “reproduce key figures” script entrypoint and expected hashes or checksums for key outputs. This is minor but increasingly expected.

---

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
The references cover constellation ops, distributed algorithms, AoI, CCSDS standards, GE modeling, and some satellite networking. For IEEE TAES / ASR scope, the paper fits.

However, there are notable literature gaps in (i) TDMA scheduling theory for satellite/space links (beyond DVB-RCS2), (ii) crosslink MACs and acquisition/tracking overhead in operational LEO systems (even if proprietary, there are secondary sources/patents/measurement papers), and (iii) queueing under MMPP arrivals (you mention it but do not cite canonical results beyond Kleinrock). Also, several “non-archival accessed Feb 2026” references are acceptable as context but should not be load-bearing.

---

# Major Issues

1) **Acquisition modeling is a first-order driver of the 30 vs 35 kbps recommendation, but the baseline assumption (per-slot cold-start \(T_{\text{acq}}=5\) ms) is not sufficiently justified for ISL TDMA.**  
- **Why it matters:** Your conclusion “35 kbps recommended; 30 kbps theoretical minimum; 24 infeasible” hinges on \(\gamma\) and superframe margin. If acquisition is amortized per burst/superframe (common in many TDMA implementations with continuous tracking), the minimum viable PHY rate can drop materially (you acknowledge this). This changes the practitioner takeaway and could invalidate the “24 kbps leads to 100% deadline misses” framing for some radio designs.  
- **Remedy:** Promote acquisition architecture to a *top-level design axis* rather than a footnote/bounding case. Add a table that shows minimum viable \(R_{\text{PHY}}\) for (a) per-slot acquisition, (b) per-superframe acquisition, and (c) “hybrid” (e.g., reacquire every \(m\) slots). Then restate the recommendation conditionally: “If per-slot acquisition, recommend 35 kbps; if tracking across slots, 30 kbps is sufficient with margin.” Provide a clear mapping to CCSDS Prox-1 “burst” semantics vs ISL continuous carrier tracking.

2) **\(\alpha_{\text{RX}}\) is treated as an input but is actually an output of the schedule and traffic mix; the framework risks circularity or hidden coupling.**  
- **Why it matters:** Eq. (24) \(R_{\text{PHY,min}} \ge C_{\text{coord,info}}/(\gamma\alpha_{\text{RX}})\) and the unicast stagger equations depend on \(\alpha_{\text{RX}}\), but \(\alpha_{\text{RX}}\) itself depends on ingress slot count, slot duration (hence \(\gamma\)), retransmissions, and egress requirements. Using \(\alpha_{\text{RX}}=0.908\) “at \(k_c=100\), 30 kbps Model C” makes the equation less general than advertised.  
- **Remedy:** Recast \(\alpha_{\text{RX}}\) as a *derived variable* from \(T_{\text{ingress}}\) and \(T_{\text{egress}}\): e.g., \(\alpha_{\text{RX}} = T_{\text{ingress}}/T_c\) under a given scheduling policy, or define it as a design choice with constraints. Update Algorithm 1 to compute \(\alpha_{\text{RX}}\) from the slot budget (or remove it and directly use the timing inequalities as the canonical feasibility test). This will strengthen the “three-layer feasibility” claim.

3) **The “three-step feasibility workflow” is strong, but the manuscript alternates between a 2-layer and 3-step framing; it needs a single consistent conceptual model.**  
- **Why it matters:** Readers may be confused whether MAC efficiency translation is a separate feasibility layer or just a mapping. This matters because you explicitly warn that \(\eta_{\text{total}}/\gamma\) is not a feasibility test, yet it is presented in key tables.  
- **Remedy:** Standardize terminology: either (a) two layers (byte budget; TDMA timing) with an intermediate mapping step, or (b) three layers with the middle one explicitly labeled “necessary condition only.” Then ensure every table/figure uses the same framing. Consider moving \(\eta_{\text{total}}/\gamma\) to an appendix or visually marking it as “screening only.”

4) **DES “distributional value” is partially undermined because the most critical tail risk in your narrative is TDMA deadline miss under ARQ—yet DES cannot represent that mechanism.**  
- **Why it matters:** You correctly state DES drops are queue overflow, not TDMA misses. But the paper’s safety-critical argument (“undersizing causes 100% deadline misses → zero status reports”) is TDMA-timing-driven, not coordinator-queue-driven. The DES tails (buffer CDF) therefore address a different risk than the one emphasized in the introduction/contributions.  
- **Remedy:** Either (a) add a TDMA-aware queueing/tail metric from the slot-level simulator (e.g., distribution of margin, retransmission backlog, fraction of nodes missing per-cycle deadline), or (b) downshift the prominence of DES tails and clearly state that the slot-level simulator is the tail-risk tool for airtime feasibility while DES is for campaign burstiness at the message layer.

5) **Packet-level validation of \(\gamma\) is useful, but it is not “independent validation” of the overall sizing framework; the paper should avoid implying it is.**  
- **Why it matters:** Section IV-J anchors \(\gamma\) to CCSDS framing, which is valuable. But it does not validate assumptions about acquisition time, guard time, half-duplex switching, or actual modem behavior, nor does it validate the traffic model. Calling it “validation” risks reviewer pushback.  
- **Remedy:** Rename IV-J from “validation” language to “standards-based parameter anchoring” (you already use that phrase elsewhere). Add a short paragraph explicitly stating what is and is not validated: “We validate the arithmetic mapping from CCSDS framing to \(\gamma\); we do not validate radio acquisition dynamics or channel statistics.”

6) **Workload realism: the campaign duty factor \(d\) helps, but the stress case still embeds a strong semantic assumption (512 B command per node per cycle) that dominates conclusions and is not tied to a control/mission requirement.**  
- **Why it matters:** \(\eta_S\approx46\%\) remains a headline number. Even if framed as an upper bound, reviewers will ask: what control loop or autonomy function truly needs 512 B/10 s/node continuously? Without a mission-driven justification, the stress case can look arbitrary and may be criticized as inflating the need for TDMA and higher PHY rate.  
- **Remedy:** Provide one concrete autonomy/operations mapping that could plausibly generate that command volume (e.g., continuous formation reconfiguration with per-node state constraints), or explicitly relabel it as a *synthetic worst-case byte budget bound* rather than a plausible operational mode. Alternatively, define stress as “maximal allowed by byte budget under assumed message sizes” and show a range of command sizes/frequencies.

7) **GE channel mapping to ISL self-blockage remains speculative; the design curves are good, but the paper should better separate “illustrative parameter point” from “recommended design point.”**  
- **Why it matters:** You correctly say no open ISL GE measurements exist. Yet the text sometimes uses the default \(p_{BG}=0.50\) to derive fairly specific claims (P95=4 cycles, ARQ structurally ineffective, expected retransmission demand ~726 ms). These are highly parameter-dependent.  
- **Remedy:** Make the sensitivity curves the primary result and demote single-point numbers to examples. Add a short “how to fit GE parameters from logs” subsection (even if hypothetical): given burst length distribution → estimate \(p_{BG}\); given conditional PER in blocked/unblocked → estimate \(p_B,p_G\). This would materially improve practitioner utility.

---

# Minor Issues

1) **Potential confusion in Table 1 notation:** \(\gamma_{24}=0.761\) and \(\gamma_{30}=0.745\) are labeled as if they are fixed constants, but later \(\gamma(R_{\text{PHY}})\) is a function. Consider consistent notation: \(\gamma_C(24\text{ kbps})\), \(\gamma_C(30\text{ kbps})\).  

2) **Table 2 “Coordinator bottleneck? Yes (20.3 kbps)”** reads like a PHY rate, but it is an info-rate. Label explicitly “info-rate” to avoid misinterpretation.  

3) **AoI table caption:** “Age of Information at Cluster Coordinators” includes cases where AoI is dominated by exception sampling. Consider adding a column or footnote: “AoI here is sampling-policy-driven; network delay negligible under assumed no deadline misses.”  

4) **Algorithm 1:** line 4 checks \(R_{\text{PHY}} < C_{\text{coord,info}}/\gamma\) and returns infeasible, but later Layer 2 timing check is the real feasibility. This early check is only a necessary condition and might reject feasible schedules if \(\alpha_{\text{RX}}<1\) is needed. Clarify and align with the stated 3-step process.  

5) **“100% TDMA deadline misses under Model C at 24 kbps”** is asserted in the intro safety-criticality paragraph; ensure the cited table corresponds to Model C (some miss-rate results are under Model S + ARQ). If the “100% miss” is specifically “no-loss but Model C overhead makes ingress exceed \(T_c\),” state that explicitly.  

6) **Reference quality:** Several operational claims rely on non-archival sources (Amazon Kuiper overview, DARPA pages). That’s fine for context but avoid using them to support quantitative technical claims.  

7) **Consistency of \(\eta_0\):** You state \(\eta_0\approx5\%\) but the heartbeat alone is 5.1% by your own breakdown; later a footnote explains the discrepancy. Consider making \(\eta_0\) explicitly “~5–6% depending on coordinator self-traffic exclusion” to avoid appearing inconsistent.

---

## Overall Recommendation  
**Recommendation:** **Major Revision**

The manuscript has a strong core: a clear sizing framework that cleanly separates byte-budget feasibility from TDMA airtime feasibility, and a valuable standards-based anchoring of \(\gamma\) that materially changes the design conclusion (24 kbps infeasible under CCSDS-style overhead; 30 kbps minimum; 35 kbps recommended with ARQ margin). The campaign duty factor \(d\) is a substantive improvement that addresses workload realism by explicitly contextualizing the 46% stress case as a continuous-duty upper bound and providing operationally plausible duty ranges.

The main reasons for major revision are not “more experiments,” but conceptual tightening and conditionalization of conclusions: the 30 vs 35 kbps recommendation is highly sensitive to acquisition/tracking architecture and to how \(\alpha_{\text{RX}}\) is defined/derived; the DES tail analysis is valuable but currently addresses a different bottleneck than the safety-critical TDMA miss narrative; and the GE single-point parameterization is still too prominent relative to the (good) sensitivity design curves. With clearer separation of necessary vs sufficient feasibility conditions, explicit derivation of \(\alpha_{\text{RX}}\), and more conditional recommendations around acquisition/ARQ/coherence regimes, this could be a strong TAES-style “design equations + sizing methodology” paper.

---

## Constructive Suggestions (ordered by impact)

1) **Make the PHY-rate recommendation explicitly conditional on acquisition/tracking architecture** (per-slot vs per-burst vs amortized) and show a compact decision table for \(R_{\text{PHY,min}}\) and recommended margin under each case.

2) **Eliminate \(\alpha_{\text{RX}}\) as an externally supplied constant**: derive it from the schedule (or remove it and use only explicit timing inequalities). This will strengthen the “general sizing equations” claim and reduce perceived circularity.

3) **Reframe “validation” as “anchoring” and “internal consistency” throughout**, and ensure the abstract/introduction do not overstate predictive accuracy. Your claim map is excellent—use it to align tone everywhere.

4) **Unify the feasibility framework vocabulary** (2 layers with a mapping step, or 3 layers with the middle as necessary-only). Then update all tables/figures accordingly, especially those showing \(\eta_{\text{total}}/\gamma\).

5) **Strengthen workload semantics justification**: either provide a plausible autonomy/control scenario that could generate the stress command rate, or explicitly define stress as a synthetic upper bound for sizing rather than an operationally expected mode.

6) **Promote GE sensitivity curves as the main output** and demote the default parameter point to an example. Add a short “how to fit GE parameters from logs” recipe to improve practitioner uptake.

7) **Add a TDMA-tail metric from the slot-level simulator** (deadline-miss distribution, retransmission backlog distribution, or per-node missed-update streak distribution) to complement DES buffer CDFs and better support the safety-critical argument.

8) **Tighten presentation** by reducing repeated restatements of the same feasibility conclusion; consolidate into one “design takeaway” section with bullet-point conditions and outputs.

If you want, I can also provide a targeted checklist of “must-fix before acceptance” edits keyed to specific sections/equations/tables (e.g., Algorithm 1, Tables 2/7/13/18) to streamline the revision.