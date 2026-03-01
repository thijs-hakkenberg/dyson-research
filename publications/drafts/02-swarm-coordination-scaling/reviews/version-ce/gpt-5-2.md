---
paper: "02-swarm-coordination-scaling"
version: "ce"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-28"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript targets an important and under-served niche: *parametric, closed-form sizing* of coordination communications for very large (10³–10⁵) autonomous space swarms, with explicit separation between message-layer byte budgets and physical-layer schedulability. The “two-layer feasibility” framing (byte budget → TDMA/half-duplex airtime) plus coordinator-ingress sizing equations is a useful contribution for early-phase system design. The paper’s strongest novelty is not the use of DES/TDMA simulation per se, but the *engineering-style design equations* and the explicit identification of the RF-backup (1 kbps/node) regime as the design driver.

That said, some claims of novelty are overstated because many components (hierarchical aggregation, AoI, GE burst-loss modeling, TDMA efficiency factorization) are individually well-known. The novelty is in the *integration* and the specific sizing workflow; the paper should sharpen that positioning.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The analytical accounting is generally consistent, and the paper is careful to distinguish (i) message-layer accounting, (ii) slot-level TDMA timing, and (iii) packet-level derivation of γ from CCSDS framing. The campaign duty factor \(d\) and the ON/OFF alternative are appropriate mechanisms to address workload realism and burstiness.

However, several methodological choices materially affect conclusions and need stronger justification or sensitivity analysis: (a) the workload semantics that make command traffic “topology invariant,” (b) the half-duplex superframe partitioning and its dependence on acquisition/guard assumptions, and (c) the GE coherence-time assumption (per-cycle) that drives the “ARQ infeasible” conclusion in the RF-backup regime. The Monte Carlo setup (30 replications) is fine for mean overhead but thin for tail claims unless the sampling methodology is very clearly defined (some is, but not all).

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Internal logic is mostly coherent, and Version CE is improved in several key areas:  
- The campaign duty factor \(d\) is now explicitly used to contextualize the stress case as a continuous-duty upper bound, and the paper provides plausible example mappings to mission phases.  
- The γ unification at **0.76** (standards-grounded) is a meaningful improvement over the earlier “assumed 0.85”-style approach; the rate dependence (0.760 at 24 kbps vs 0.745 at 30 kbps) is explicitly acknowledged.  
- The three-layer narrative (byte budget, MAC efficiency, TDMA airtime) is closer to sound now, with the caveat that “\(\eta_{\text{total}}/\gamma\)” is a necessary condition rather than a separate feasibility layer (the manuscript says this, but the overall exposition still sometimes treats it as a “layer”).

Key validity gaps remain: the DES “verification” largely confirms equations that are embedded in the simulator; the independent validation value is limited unless the simulator includes mechanisms not present in the closed-form model (beyond distributional burstiness). Also, some numerical inconsistencies/ambiguities appear around coordinator ingress sizing (use of \(k_c\) vs \(k_c-1\), and the 20.3 vs 20.5 kbps figures), which matters because the TDMA margin is tight.

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
The manuscript is generally well organized, with clear notation, a useful claim/verification map, and explicit separation of tool scopes (DES vs slot-sim vs packet-level). Tables are mostly informative and the paper does a better-than-average job of stating what is and is not modeled.

Still, the paper is long and occasionally repetitive; several sections restate the same conclusions (e.g., “DES matches analytic by construction,” “30 kbps minimum viable”). Some terminology could be tightened: “three-layer” vs “two-layer + translation,” “overhead” vs “utilization,” and “MAC efficiency” vs “PHY efficiency” (since γ bundles FEC and acquisition, which many readers will not call MAC).

---

## 5. Ethical Compliance  
**Rating: 4 (Good)**  
The paper provides code and tag information, parameter tables, and an explicit AI-assisted ideation disclosure. That is strong.

Two improvements are needed for reproducibility: (i) ensure the repository contains exact scripts to regenerate every figure/table (not just “code exists”), and (ii) provide a deterministic run manifest (seeds per experiment) or instructions to reproduce confidence intervals and tail statistics.

---

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
The topic fits IEEE TAES / Adv. Space Res. The literature coverage is broad, but it is also somewhat “survey-like” and includes multiple non-archival references (Starlink filings, DARPA pages, Amazon Kuiper overview). That is acceptable as context, but the technical backbone should rely more on archival sources for constellation operations, ISL MAC/PHY constraints, and TDMA/Proximity-1 implementations.

The AoI and GE citations are appropriate. For MAC/TDMA in satellite/spacecraft contexts, the paper would benefit from citing more directly relevant work on Proximity-1/space TDMA implementations, half-duplex scheduling, and link-layer performance under burst errors (including CCSDS ARQ/FEC guidance where applicable).

---

# Major Issues

1. **The “three-layer feasibility framework” is not yet conceptually clean (Layer 1 vs “\(\eta/\gamma\)” vs Layer 2).**  
   - **Why it matters:** Practitioners need a crisp decision procedure. Right now, \(\eta_{\text{total}}/\gamma\) is sometimes presented as a “layer,” sometimes as a translation, and sometimes as a threshold for “TDMA required.” This risks misapplication.  
   - **Remedy:** Present a single algorithmic feasibility test (flowchart or pseudocode):  
     1) Compute message-layer offered load (\(\eta_{\text{total}}\)).  
     2) Translate to required raw rate via γ *for the chosen PHY/MAC* (not as an independent layer).  
     3) If half-duplex TDMA: check *time-budget inequalities* (Eqs. 34–35) using slot duration from Eq. 44 / Table 35; if CSMA/ALOHA: check stability region/throughput model.  
     4) Output required PHY rate and whether 1-cycle completion holds (including unicast staggering).  
     Also remove/soften heuristic statements like “TDMA required when \(\eta_{\text{total}}/\gamma > 50\%\)” unless derived from the half-duplex partition (show derivation).

2. **Coordinator ingress sizing mixes \(k_c\) and \(k_c-1\) inconsistently; tight margins make this nontrivial.**  
   - **Why it matters:** At \(k_c=100\), the TDMA design point is near feasibility. A 1% accounting mismatch can flip “24 kbps feasible/infeasible” conclusions or margin claims.  
   - **Remedy:** Standardize: ingress demand should use \(k_c-1\) *if the coordinator does not send to itself*, and explicitly state whether the coordinator also transmits a status report that must be received/relayed. Update all related equations and numeric examples consistently: Eq. for \(C_{\text{TDMA}}\), the 20.3/20.5 kbps statement, Table 35 superframe counts (99 slots), and any “\(k_c S_{\text{eph}}\)” expressions (including in the abstract and contributions list).

3. **The campaign duty factor \(d\) improves realism, but the workload model still risks being interpreted as representative without enough empirical anchoring.**  
   - **Why it matters:** The headline results (\(\eta_0\approx 5\%\), stress \(\eta_S\approx 46\%\), “routine 5–10%”) depend strongly on the assumed command message size/frequency and on the definition of “active command cycle.” Without stronger grounding, reviewers/readers may view \(d\) as a tunable knob that can justify almost any overhead.  
   - **Remedy:** Add a short subsection that (i) clearly distinguishes *command campaigns* (maneuver sequences) from *control loops* (formation keeping), and (ii) provides at least one externally sourced operational analogue (even terrestrial/airborne swarm ops, or published constellation maneuver cadence) to justify plausible \(d\) ranges. At minimum, provide sensitivity plots for \(\eta(d)\) across \(S_{\text{cmd}}\in\{64,128,256,512,1024\}\) B and \(T_c\in\{1,5,10,30\}\) s so practitioners can map to their mission.

4. **γ unification at 0.76 is a clear improvement, but it is not applied consistently as a *rate-dependent* quantity in all feasibility statements.**  
   - **Why it matters:** Section IV-J correctly notes \(\gamma(30\text{ kbps})\approx 0.745\). Yet earlier sections (and some tables) still speak as if γ=0.76 applies at 30 kbps. This affects margins, and the paper’s central claim is a tight feasibility boundary.  
   - **Remedy:** Enforce a rule: whenever a numeric schedulability/margin claim is made, specify the PHY rate and the corresponding \(\gamma(R_{\text{PHY}})\) used. Consider introducing \(\gamma_{24}\) and \(\gamma_{30}\) symbols or always writing \(\gamma(R_{\text{PHY}})\). Update Table 14/35/36 and the abstract where needed.

5. **Stress-case contextualization is better, but “\(\eta_S\approx 46\%\)” is still easy to misread as typical.**  
   - **Why it matters:** Many readers will cite the stress number out of context. The paper does say “continuous duty upper bound” and “<1% time,” but the narrative still foregrounds 46% repeatedly.  
   - **Remedy:** Reframe results so that the *primary* reported operational point is a duty-factor-weighted annual average (or distribution) with explicit campaign examples, and the 46% case is clearly labeled “continuous-duty bound.” A simple figure showing \(\eta\) CDF over a year under ON/OFF campaigns (not just per-cycle ingress CDF) would help.

6. **DES verification provides limited independent value and risks being viewed as circular.**  
   - **Why it matters:** A top-tier journal will expect simulations to validate or stress the analysis, not simply reproduce it. The manuscript acknowledges “expected by construction,” which is honest, but then still uses DES agreement as “verification.”  
   - **Remedy:** Either (a) reposition DES as *an implementation artifact to compute distributions under bursty workloads and failures* (and reduce emphasis on “matches closed-form”), or (b) add at least one mechanism in DES not present in the closed-form equations and show divergence/insight (e.g., finite buffers + correlated ON/OFF campaigns + coordinator rotation transients + priority traffic). If you keep the verification claim, explicitly list which equations are not encoded directly and are emergent.

7. **Packet-level validation (Section IV-J) is helpful but still not fully “independent validation” of γ or feasibility.**  
   - **Why it matters:** The packet-level simulator appears to compute γ via a deterministic overhead product using assumed constants (FEC rate, acquisition dwell). That is more of a *standards-based calculation* than a validation. Also, acquisition dwell (5 ms) is asserted as “typical” without citation or sensitivity.  
   - **Remedy:** (i) Provide a sensitivity sweep over \(T_{\text{acq}}\) and guard time to show robustness of the 30 kbps threshold. (ii) Clarify what the packet-level simulator actually simulates (queueing? framing? BER→PER? or just bit accounting). If it is deterministic accounting, call it that. (iii) Cite a source or provide rationale for acquisition dwell and for using Proximity-1 assumptions for ISL.

8. **Half-duplex TDMA model assumes a specific superframe structure that may not generalize; practitioners need a clearer mapping.**  
   - **Why it matters:** The key conclusion “30 kbps minimum viable” depends on (a) 99 ingress slots, (b) one command broadcast + heartbeat per cycle, (c) half-duplex turnaround counts, and (d) whether sync/ranging is in-band. Different implementations (e.g., piggybacked sync, longer payload aggregation, variable slot packing) could change the boundary.  
   - **Remedy:** Add a “generalized superframe” parameterization: number of ingress slots per cycle, payload aggregation factor, control-plane overhead per cycle, and whether ranging/sync are amortized. Then re-express Table 35 as an instance of that general model.

9. **GE model conclusions hinge on coherence-time choice; the paper partially addresses this, but the design guidance is still ambiguous.**  
   - **Why it matters:** The statement “intra-cycle ARQ infeasible” is only true in the slow-mixing regime. The paper does show a coherence sensitivity figure, but the engineering takeaway could be misapplied.  
   - **Remedy:** Provide a clear decision boundary: for a given coherence time distribution, what fraction of cycles are in “slow-mixing” vs “fast-mixing,” and what ARQ policy is recommended? Alternatively, explicitly scope the ARQ infeasibility claim to RF-backup with blockage-dominated coherence \(\tau_c \ge T_c\), and recommend inter-cycle repetition/FEC rather than ARQ.

10. **Some architecture comparisons are not functionally comparable (centralized compute queue; sectorized mesh), risking misleading “bounds.”**  
   - **Why it matters:** The centralized baseline is compute-only and omits the true bottlenecks (contact windows, spectrum, uplink scheduling). The sectorized mesh is “local monitoring only” and not comparable to “cluster command.” Presenting them as bounds is fine, but it must be unmistakably framed as such.  
   - **Remedy:** Strengthen the “capability matrix” narrative by explicitly stating which requirements each architecture satisfies, and avoid plotting them together without strong caveats. Consider adding a “communications bottleneck” term to the centralized baseline or removing quantitative comparisons that imply centralized is feasible to 10⁶ in practice.

---

# Minor Issues

1. **Equation/number hygiene:** multiple places use 20.3 kbps vs 20.5 kbps; standardize and show the exact arithmetic (99×256 B×8 / 10 s = 20.2752 kbps).  
2. **Terminology:** γ includes FEC and acquisition; calling it “MAC efficiency” is arguably misleading—consider “link-layer efficiency” or “airtime efficiency.”  
3. **Table 14 (Notation):** \(\gamma\) is defined as 0.76 at 24 kbps, but later you also use 0.745 at 30 kbps; note rate dependence in the notation table.  
4. **Table 12 (Bandwidth breakdown):** “Commands 410 bps” assumes 512 B per 10 s; write 409.6 bps to avoid confusion.  
5. **AoI section:** clarify whether AoI is computed per node-to-coordinator stream and then aggregated, and whether “P99 AoI” is across nodes, time, coordinators, or runs (some is stated; make it unambiguous in one sentence).  
6. **Coordinator CPU model:** deterministic 5 ms/message is plausible but unreferenced; either cite a representative flight CPU throughput or present it as an arbitrary placeholder and show that link, not CPU, binds over a range.  
7. **Link budget table:** provide modulation/coding assumptions consistently with γ/FEC (e.g., if using LDPC 7/8 in γ, reflect coding gain or required Eb/N0 accordingly, or explicitly separate “uncoded BPSK” link budget from “coded throughput”).  
8. **Non-archival references:** reduce reliance where possible for key factual claims; keep them as context.  
9. **Figure captions:** some captions assert conclusions (“confirms physical necessity”)—prefer neutral description and leave interpretation to text.  
10. **Typographic:** a few places use “kbps” while equations use “bps”; ensure consistent units and conversions in Eq. (46) and Table 36.

---

## Overall Recommendation  
**Recommendation:** **Major Revision**

The paper has a strong engineering intent and several genuinely useful elements (duty-factor realism knob, standards-grounded γ, explicit half-duplex airtime test, and clear separation of simulation tool scopes). Version CE clearly improves prior weaknesses by (i) contextualizing the 46% stress case as a continuous-duty bound, (ii) replacing an assumed γ with a CCSDS-grounded γ≈0.76, and (iii) making the TDMA airtime constraint explicit rather than implied.

The remaining blockers are primarily about *conceptual crispness and independence of validation*. The feasibility framework needs to be presented as a clean decision procedure without ambiguity about “layers,” and the tight feasibility boundary (24 vs 30 kbps) requires stricter consistency in \(k_c\) vs \(k_c-1\), γ rate dependence, and the assumed superframe overheads (guard/acquisition). Finally, the DES and packet-level “validation” should be repositioned or strengthened so they provide non-circular evidence or additional insight beyond confirming the equations used to build them.

---

## Constructive Suggestions (ordered by impact)

1. **Add a one-page “How to use this framework” procedure** (inputs → compute \(\eta\) → compute \(\gamma(R)\) → compute slot time → check ingress/egress inequalities → output minimum PHY rate and whether 1-cycle completion holds).  
2. **Unify all coordinator-ingress expressions** to one consistent convention (\(k_c-1\) vs \(k_c\)) and update every dependent numeric claim/table/abstract statement.  
3. **Make γ explicitly rate-dependent everywhere** and update tables/notation accordingly; avoid using γ=0.76 at 30 kbps unless you explicitly choose that conservatism and quantify the effect.  
4. **Strengthen Section IV-J by sensitivity, not just decomposition:** sweep \(T_{\text{acq}}\), \(T_{\text{guard}}\), and FEC rate; show the boundary for minimum feasible PHY rate as a contour plot.  
5. **Recast DES as distributional/burstiness analysis** and reduce the emphasis on “verification by matching analytic.” Add at least one result that the equations do not trivially predict (e.g., buffer overflow probability vs \(C_{\text{coord}}\) under ON/OFF + GE; or time-to-recover distributions including coordinator rotation).  
6. **Tighten the stress-case narrative:** present routine (d=0.01–0.10) as the main operational regime; keep d=1 as a clearly labeled upper bound. Consider reporting annual-average utilization for the three example campaigns.  
7. **Clarify the applicability of the GE/ARQ conclusion:** explicitly scope “ARQ infeasible” to slow-mixing blockage regimes; provide a simple rule-of-thumb mapping from measured coherence time to recommended recovery strategy.  
8. **Improve comparability of baselines:** either add a communications-limited centralized baseline (even a coarse contact-window/spectrum model) or more strongly bracket the centralized compute-only model as non-comparable.  
9. **Align link budget assumptions with coding/throughput assumptions** (or explicitly state they are separate illustrative calculations).  
10. **Add a short practitioner-facing table of “default parameters and where to measure them”** (e.g., \(T_{\text{acq}}\), guard time components, payload sizes, coherence time, \(p_{BG}\), etc.), since the framework is meant for early sizing.

If the authors address Items 1–5 rigorously, the manuscript would be much closer to publishable in a top-tier venue because the main contribution—an actionable sizing workflow bridging message-layer and airtime schedulability—would be both clearer and more defensible.