---
paper: "02-swarm-coordination-scaling"
version: "ch"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-01"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript targets a real and under-served need: *parametric sizing* of coordination communications for very large spacecraft swarms (10³–10⁵), with explicit separation of message-layer offered load from PHY/MAC schedulability. The “two-layer feasibility” framing (byte budget → TDMA airtime) plus closed-form coordinator ingress sizing is practically valuable, especially for early-phase architecture trades. The standards-grounded derivation of slot efficiency (γ) and its impact on the 24 vs 30 kbps boundary is a meaningful improvement over the common “assume an efficiency” approach.

Novelty is strongest in (i) the explicit feasibility workflow (Algorithm 1) that combines byte accounting with half-duplex superframe constraints, and (ii) the γ unification anchored to CCSDS framing. Novelty is weaker in the DES itself (cycle-aggregated DES is not new) and in some queueing/latency parts that largely restate known AoI/GE ideas in this application context.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The analytical byte accounting is generally consistent and the TDMA airtime modeling is a solid addition. The manuscript is careful to distinguish Model S vs Model C and to base feasibility claims on Model C—this addresses a common pitfall.

However, several methodological choices remain only partially justified or are internally “tight” in ways that matter for aerospace-grade conclusions: (i) the half-duplex partitioning and superframe margin at 30 kbps is extremely thin, making results sensitive to unmodeled timing variance and control-plane needs; (ii) the GE model is used appropriately as a sensitivity family, but the mapping from physical mechanisms to (pBG, pB, coherence) remains speculative; (iii) the DES “verification” is correctly described as internal consistency, but still occupies substantial space relative to the independent value it adds.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
The logic of the three-layer narrative—(a) message-layer byte budget, (b) MAC efficiency via γ, (c) TDMA airtime schedulability—is mostly coherent, and the manuscript explicitly notes that η_total/γ is necessary but not sufficient. The stress-case η_S ≈ 46% is now better contextualized as a continuous-duty upper bound, and the campaign duty factor *d* is a good mechanism to address realism.

Remaining validity risks are primarily about *interpretation boundaries*:
- The paper sometimes blurs “coordinator ingress sizing” (uplink member→coordinator) with “hierarchical coordination feasibility” as a whole, while later acknowledging hierarchical coordination is suspended in RF-backup mode. That is defensible, but it needs crisper separation of *which link* and *which mode* the sizing applies to.
- The “TDMA required when η_total/γ > 50%” heuristic appears in Table 15/Algorithm 1; it is plausible but not derived, and could mislead readers into treating it as a criterion rather than a rule-of-thumb.

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
Overall organization is strong: clear notation table, explicit model disambiguation (DES vs slot-sim vs packet derivation), and a useful claim/evidence tier map. The revised γ values (0.760/0.745) are prominently stated and appear consistently in most feasibility claims.

Clarity issues remain in (i) several places where “info-rate” vs “PHY rate” vs “per-node budget” are mixed in prose, and (ii) the manuscript’s repeated emphasis that 1 kbps is “design-driving” while simultaneously stating hierarchical coordination is suspended during RF-backup. Readers may ask: if hierarchy is suspended, why is RF-backup driving the hierarchical TDMA sizing? The answer seems to be: the *backup RF channel is not 1 kbps*; the *cluster coordinator ingress PHY* is 24–30 kbps, and the 1 kbps is per-node budget allocation—this needs a single, unambiguous diagram or boxed explanation.

---

## 5. Ethical Compliance  
**Rating: 4 (Good)**  
Good: open-source code and tag provided; parameters listed; toolchain stated; AI assistance disclosed in acknowledgments. That is above-average for reproducibility.

Minor concern: the AI disclosure is high-level; IEEE journals increasingly expect a brief statement of *what content* was AI-assisted (e.g., ideation only, not text/figures/data). You partly do this (“motivated aspects… but not validated here”), but I recommend a more explicit scope statement (no AI-generated results, no AI-written text beyond editing, etc., if true).

---

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
The paper is in-scope for T-AES / Adv. Space Res. (architecture sizing, comms feasibility, autonomy coordination). Referencing is broad and mostly appropriate (CCSDS, AoI, GE, consensus, DTN, mega-constellations).

Gaps:
- TDMA/MAC literature for satellite crosslinks is thin. You note lack of open descriptions for Starlink/Iridium, but you could still cite related satellite TDMA standards/practices beyond Proximity-1 (e.g., DVB-RCS2 concepts, or generic satellite DAMA/TDMA references, even if not ISL-specific).
- For AoI, you use the geometric inter-arrival result; consider citing a canonical AoI under Bernoulli sampling / renewal processes result (you cite surveys, which helps, but a more directly relevant theorem/reference would strengthen).

---

# Major Issues

1) **Ambiguity in what “1 kbps design point” is driving, given hierarchical coordination is suspended in RF-backup mode**  
**Why it matters:** A central narrative is that the 1 kbps regime is “design-driving,” yet the manuscript states hierarchical coordination is suspended during RF-backup due to coordinator ingress needs. This can read as internally contradictory: if hierarchy is suspended, why size hierarchical TDMA around that regime?  
**Remedy:** Add a concise “channel/mode map” figure/table early (Intro or Simulation Framework) clarifying:  
- per-node *budget* (1 kbps) vs coordinator ingress *PHY* (≥30 kbps) vs RF-backup *link capability* (~2.5 kbps)  
- which coordination functions run in each mode (full hierarchy vs beacon-only safe mode)  
- which feasibility tests apply to which links.  
Also adjust wording: the design-driving regime is the *low-rate, high-overhead coordinator ingress superframe feasibility* (24–30 kbps), not the 1 kbps RF-backup link which cannot support hierarchy.

2) **The “three-layer feasibility framework” is conceptually right but not mathematically pinned down as three distinct layers**  
**Why it matters:** You describe “two-layer” (byte budget, airtime) but also treat η_total/γ as a quasi-layer. Some tables/Algorithm steps risk making η_total/γ look like a decision boundary. Reviewers/readers may challenge whether the framework is rigorous or just bookkeeping.  
**Remedy:** Formalize the framework with explicit definitions:  
- Layer 1: message-layer feasibility: offered information bits per cycle ≤ C_node·T_c (or ≤ allocated budget)  
- Layer 2: PHY/MAC feasibility: existence of schedule satisfying ingress/egress inequalities (Eqs. 35–36) given half-duplex and slot structure  
- η_total/γ: a *derived utilization indicator* for certain MAC assumptions, not a layer.  
Then revise Algorithm 1 and Table 15 to label η_total/γ as “screening heuristic” and point to the definitive inequalities.

3) **DES verification value is still overstated relative to its independence**  
**Why it matters:** You correctly acknowledge Tier 1 is internal consistency, but the Results section still uses DES vs closed-form agreement as supportive evidence in multiple places. For a top-tier journal, readers will want either (i) true independent validation, or (ii) a sharper statement that DES is primarily for distributional/tail metrics and for campaign stochasticity, not for confirming mean equations.  
**Remedy:** Rebalance: shorten repetitive “DES matches analytical” statements and instead emphasize the unique DES outputs (buffer CDFs under ON/OFF, tail AoI under exception gating, etc.). Consider moving the “<0.1% agreement” to an appendix or a single consolidated paragraph.

4) **Packet-level validation (Section IV-J) anchors γ well, but still lacks an “independent check” against real/representative PHY timing variability**  
**Why it matters:** Your main feasibility boundary (24 infeasible, 30 barely feasible) hinges on small timing terms (acquisition, guard, ranging). A standards-based derivation is good, but practical radios often have additional overhead (AGC settling, PLL lock variability, interleaver flush, ranging sequences, etc.). Without either empirical timing distributions or a robust worst-case bound, the “30 kbps minimum” could be challenged as fragile.  
**Remedy:** Strengthen IV-J and margin analysis by:  
- explicitly listing which Proximity-1 timing elements are included/excluded and why  
- providing a “robust design” recommendation more prominently (you mention ~35 kbps; elevate this as the recommended minimum if aerospace-grade margin is desired)  
- optionally adding a simple uncertainty propagation: treat T_acq and T_guard as random variables with stated bounds and show probability of infeasibility at 30 kbps.

5) **Campaign duty factor d improves realism, but the workload model still under-represents fleet-correlated campaigns—the very scenario that creates stress**  
**Why it matters:** You now contextualize η_S as continuous-duty upper bound and provide ON/OFF bursts, which is good. But the most operationally relevant “stress” is often *correlated across many nodes* (e.g., conjunction response, mass orbit raising, software patching). Independent Bernoulli per node may understate coordinator ingress burstiness and buffer needs at higher layers (regional/ground), even if per-cluster uplink is fixed-slot TDMA.  
**Remedy:** Add one correlated campaign model variant (even a simple “all nodes in a cluster ON together with probability d_cluster”) and show its effect on (i) coordinator buffer tails, (ii) regional burstiness, and (iii) any links that are not fixed-slot. This can be a small additional experiment but would materially strengthen the realism argument.

6) **Generalized γ expression is useful, but dimensional clarity and parameter naming need tightening for practitioner use**  
**Why it matters:** Eq. (51) is a key practitioner takeaway. As written, it mixes bits, bytes, bps, and ms with a 10^-3 factor; it is easy to misuse. Also, O_frame is “bits,” S is “bytes,” R_PHY is “bps,” while earlier tables use kbps.  
**Remedy:** Provide a boxed “how to compute γ” with a worked numerical example using exactly one unit system (SI base units), and define O_frame precisely (does it include ASM? address? CRC? any padding?). Consider providing a companion “time-domain” formula as the primary and the bit-domain as derived, to reduce unit mistakes.

---

# Minor Issues

1) **Consistency of γ values:** You state γ_C,24 = 0.760 and γ_C,30 = 0.745; ensure every table using γ uses the correct subscript (some places still say “γ_24 = 0.760 reference” while discussing 30 kbps feasibility).  
2) **Rounding discrepancy footnote:** The 111.5 ms vs 115.5 ms slot time discrepancy is potentially confusing. Consider eliminating the discrepancy by recomputing with consistent rounding and showing intermediate values.  
3) **“TDMA required when η_total/γ > 50%”** appears as if a rule; label as heuristic and cite the definitive test.  
4) **AoI section:** clarify that Eq. (29) is for geometric inter-report intervals with deterministic service and no queueing/loss coupling; currently it reads more general than it is.  
5) **Queueing model for centralized baseline:** the M/D/1 compute bound is fine as a reference, but it is so disconnected from comms that it risks being a strawman. Consider tightening or moving it to Related Work/Discussion as a bounding argument.  
6) **Terminology:** “stress-case commands account for >60% of stress-case traffic” is confusing because stress-case already includes commands by definition; consider “of overhead beyond baseline” or similar.  
7) **Table 3 (bandwidth regimes):** AoI P99 constant across bandwidth is true under your model, but readers may misinterpret; add a note that this assumes exception probability unchanged and no queueing/priority changes.  
8) **MAC contention not modeled:** you already state this; I suggest adding one sentence warning that CSMA feasibility at ≥10 kbps is not guaranteed in dense interference conditions.  
9) **Figure references:** a few figures lack file extensions or have inconsistent naming (e.g., `fig-unicast-stagger` missing `.pdf` in source).  
10) **Non-archival citations:** several operational references are non-archival; acceptable as context, but keep key technical claims anchored to archival/standard documents where possible.

---

# Overall Recommendation  
**Recommendation:** **Major Revision**

The manuscript has a strong core contribution—closed-form sizing with a clear separation between message-layer load and TDMA airtime feasibility—and the updated CCSDS-grounded γ (0.760) is a substantive improvement that tightens and clarifies the 24 vs 30 kbps boundary. The campaign duty factor *d* and the explicit framing of η_S ≈ 46% as a continuous-duty upper bound meaningfully address workload realism concerns compared to earlier versions.

The main reasons for Major Revision are not “more experiments for their own sake,” but the need to (i) remove lingering conceptual ambiguities around what exactly is design-driving (1 kbps vs 30 kbps coordinator PHY vs RF-backup infeasibility for hierarchy), (ii) formalize the feasibility framework so η_total/γ is clearly a heuristic and TDMA airtime inequalities are the decisive condition, and (iii) strengthen the robustness of the key feasibility conclusion given the very thin 30 kbps margin under Model C. The DES component should be repositioned to emphasize the distributional insights it uniquely provides rather than agreement with its own equations.

---

# Constructive Suggestions (ordered by impact)

1) **Add a “Modes & Links” clarification artifact** (one figure/table) that disambiguates: per-node budget, coordinator PHY, RF-backup capability, and which coordination functions run in each.  
2) **Tighten the feasibility framework exposition**: define layers formally; demote η_total/γ to screening; make Eqs. (35–36) the explicit feasibility gate everywhere.  
3) **Make the 30 kbps conclusion robust**: elevate the conservative 35–38 kbps recommendation (or present 30 kbps as “standards-default minimum, low margin”) and add an uncertainty/worst-case timing discussion.  
4) **Add one correlated campaign model variant** to complement Bernoulli and ON/OFF, demonstrating buffer/ingress tail sensitivity under realistic fleet- or cluster-correlated operations.  
5) **Refactor DES validation narrative**: compress internal-consistency checks; highlight tail/buffer results and any insights that are not obtainable from closed form.  
6) **Improve practitioner usability of γ generalization**: provide a boxed recipe + consistent units + one fully worked example; define O_frame unambiguously.  
7) **Strengthen MAC/TDMA literature context**: add a few satellite TDMA/DAMA references beyond Proximity-1 to show awareness of broader practice, even if ISL-specific details are proprietary.