---
paper: "02-swarm-coordination-scaling"
version: "ci"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-01"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript’s core contribution—closed-form sizing equations that connect (i) per-node message-layer byte budgets to (ii) half-duplex TDMA airtime feasibility via an explicit efficiency parameter \(\gamma\)—is valuable and relatively uncommon in the swarm/constellation coordination literature. The explicit separation of “Layer 1 byte feasibility” and “Layer 2 TDMA schedulability” is a strong organizing idea, and the paper is unusually practitioner-oriented (Algorithm 1, margin tables, design-point recommendation).

Novelty is strongest in the *integration* (byte accounting + coordinator ingress bottleneck + TDMA superframe timing + correlated-loss recovery curves) rather than in any single model element. The work is less novel where it reuses standard constructs (GE channel, AoI under Bernoulli sampling, basic TDMA budgeting), but the combination at \(10^3\)–\(10^5\) scale with explicit parametric sizing is meaningful.

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The analytical accounting is generally sound and the “three-tool” approach (cycle-aggregated DES, slot-level TDMA simulator, packet-level \(\gamma\) derivation) is directionally appropriate. However, several modeling choices blur what is being “validated” versus what is being “instantiated,” and some claims depend sensitively on parameters that are only weakly justified (e.g., acquisition dwell per slot, ranging overhead assumptions, GE coherence mapping).

The DES is explicitly cycle-aggregated and therefore cannot validate any intra-cycle effects; the paper is mostly careful about this, but still occasionally uses DES agreement as rhetorical support for equations that are essentially the DES’s own bookkeeping. The slot-level simulator *does* add value (deadline misses, ARQ coupling), but its assumptions should be more crisply specified (slot structure, retransmission placement policy, whether retransmissions steal egress time, etc.).

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Internal logic is mostly coherent, and Version CI improves several earlier pitfalls by (i) introducing a campaign duty factor \(d\), (ii) unifying \(\gamma\) to the CCSDS-derived 0.760/0.745 values for design conclusions, and (iii) explicitly labeling the stress case as a continuous-duty upper bound.

That said, there remain a few logic/consistency issues:
- The manuscript sometimes mixes “information-rate” vs “PHY-rate” vs “slot-time feasibility” in ways that could mislead a practitioner (especially around the 27 kbps / 30 kbps / 35 kbps narrative).
- The three-layer feasibility story (“byte budget, MAC efficiency, TDMA airtime”) is conceptually good, but the middle layer (\(\eta/\gamma\)) is only a rough utilization proxy; the paper should more clearly prevent readers from treating it as a sufficient condition.

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
Overall structure is strong: notation table, explicit model tiering, claim map, and a clear separation between message-layer and slot-level. The “Model S vs Model C” disambiguation is helpful and (mostly) consistently applied.

Clarity issues are concentrated in (i) the exact definition and use of \(\gamma\) across sections (product decomposition vs time-domain vs rate dependence), and (ii) the workload semantics behind \(\eta_{\text{cmd}}\) and the duty factor \(d\) (independent Bernoulli vs ON/OFF vs cluster-correlated). These are all present, but the “default” workload stochastic process used for headline numbers should be stated more explicitly and earlier.

## 5. Ethical Compliance  
**Rating: 4 (Good)**  
Good: open-source code and a tagged repository; explicit AI disclosure; clear parameter table; claim-evidence mapping.

Gaps: For reproducibility, the review would benefit from (i) commit hash in addition to tag, (ii) explicit instructions to regenerate each key figure/table (a “reproduce Fig. X” script list), and (iii) archival references where possible (several key operational references are non-archival web pages).

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
The paper is broadly within IEEE TAES / space systems networking/autonomy scope. Referencing is decent for distributed algorithms and AoI, and CCSDS anchoring is appropriate.

However, the MAC/TDMA literature coverage is thin given the centrality of “schedulability” and “efficiency” claims. Consider adding and contrasting with: (i) classic satellite DAMA/TDMA return-link scheduling work beyond DVB-RCS2, (ii) deterministic real-time scheduling analogs (superframe feasibility as a utilization/deadline problem), and (iii) more recent LEO ISL MAC papers (even if not directly applicable) to contextualize the NS-3 gap.

---

# Ten scored sections (requested format)

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
Closed-form sizing framework that ties message budgets to TDMA airtime feasibility at swarm scale is a useful contribution; novelty is mainly integrative.

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
Solid first-order modeling; some assumptions (acquisition per slot, GE mapping, retransmission policy) need tighter specification and sensitivity.

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Mostly consistent; a few rate/efficiency/feasibility narratives risk confusion; utilization proxy could be misread as a criterion.

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
Well organized; Model S vs C is helpful; some cross-section parameter consistency needs tightening.

## 5. Ethical Compliance  
**Rating: 4 (Good)**  
Open code + AI disclosure are strong; reproducibility instructions could be more “push-button.”

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
Appropriate venue; TDMA/MAC scheduling literature context is lighter than expected.

## 7. Results Quality & Statistical Rigor  
**Rating: 3 (Adequate)**  
MC replication count is fine for mean overhead; tail metrics are treated carefully. But several “design-point” conclusions hinge on deterministic budgets rather than statistical uncertainty bounds on timing parameters.

## 8. Validation & Verification Strength  
**Rating: 3 (Adequate)**  
Packet-level \(\gamma\) derivation is meaningful; slot-level sim adds real value. DES “verification” mostly confirms bookkeeping; external validation remains absent (acknowledged).

## 9. Practical Utility / Engineering Actionability  
**Rating: 4 (Good)**  
Algorithm 1, margin inventory, and explicit “30 kbps minimum / 35 kbps recommended” are actionable. Needs clearer guidance on how to measure/choose \((T_{\text{acq}},T_{\text{guard}},p_{BG},p_B)\) in practice.

## 10. Consistency, Parameter Hygiene, and Traceability  
**Rating: 3 (Adequate)**  
Version CI improves \(\gamma\) unification and duty factor framing, but there are still small inconsistencies (e.g., the \(\gamma_{C,24}\) 0.760 vs 0.765 note; multiple places where “27 kbps” is described as info-rate vs PHY-rate ambiguously).

---

# Major Issues

1. **Ambiguity between information-rate requirement, PHY-rate requirement, and airtime feasibility (27 kbps vs 30 kbps vs 35 kbps narrative)**  
   - **Why it matters:** Practitioners could misinterpret “27 kbps at \(\gamma=0.760\)” as a PHY requirement when it is sometimes presented as such, while elsewhere 30 kbps is the minimum due to superframe timing and half-duplex partitioning. This is central to the paper’s primary engineering conclusion.  
   - **Remedy:** Create one consolidated “rate ladder” figure/table early in Results IV-A:  
     - \(C_{\text{coord,info}} \approx 20.2\) kbps (pure payload bits)  
     - \(C_{\text{coord,PHY}} \approx C_{\text{coord,info}}/\gamma\) (slot overhead)  
     - \(R_{\text{PHY,min}}\) from *time feasibility* \(T_{\text{ing}}+T_{\text{egr}}\le T_c\) including \(\alpha_{\text{RX}}\)  
     - “Recommended” = add explicit margin target (e.g., 10–20%) and show how 35 kbps meets it.  
     Also standardize language: reserve “kbps” with qualifiers **info-rate** vs **PHY-rate** everywhere.

2. **Three-layer feasibility framework is conceptually right but operationally underspecified; \(\eta_{\text{total}}/\gamma < 0.5\) screening rule is arbitrary**  
   - **Why it matters:** The screening indicator could be adopted as a design rule despite being neither necessary nor sufficient. For a journal article, the threshold needs justification or should be reframed as a heuristic.  
   - **Remedy:** Either (a) provide a short derivation/empirical justification: show false-positive/false-negative rates versus the actual Layer-2 feasibility check across a sweep of \(k_c, R_{\text{PHY}}, T_{\text{acq}}, T_{\text{guard}}\), or (b) demote it explicitly to “illustrative heuristic; do not use for certification,” and move it to Discussion/Limitations.

3. **DES verification: limited incremental value beyond confirming the same equations; distributional claims need stronger separation from “equation checking”**  
   - **Why it matters:** The manuscript itself acknowledges Tier-1 is not independent validation. Reviewers/readers will ask why the DES is needed at all if it reproduces closed-form means. The paper’s strongest DES value is tail/buffer behavior under correlated duty processes—this should be foregrounded, while “DES matches analytical <0.1%” should be deemphasized.  
   - **Remedy:** Reframe DES section/results:  
     - Make distributional outputs (buffer CDFs, peak ingress quantiles under ON/OFF and cluster-correlated campaigns) the primary DES deliverable.  
     - Move “<0.1% agreement” to an appendix or brief V&V note.  
     - Add at least one *new* DES result that cannot be obtained from the closed form (e.g., drop probability vs buffer size under ON/OFF with cluster correlation, or time-to-recover AoI distribution under combined GE + campaign bursts).

4. **Packet-level validation (Section IV-J) anchors \(\gamma\), but the mapping from CCSDS Proximity-1 to a swarm ISL TDMA slot is not fully defensible**  
   - **Why it matters:** The central “24 infeasible / 30 feasible / 35 recommended” conclusion hinges on \(\gamma\) and on per-slot acquisition/guard assumptions. Proximity-1 is plausible, but using it for repeated short-burst TDMA slots with a 5 ms “acquisition dwell per slot” is a strong assumption; many systems amortize acquisition across bursts or use continuous synchronization.  
   - **Remedy:** Add a subsection explicitly distinguishing:  
     - **Cold-start acquisition** (rare) vs **slot-to-slot tracking** (common)  
     - Whether \(T_{\text{acq}}\) applies per slot, per frame, per burst, or per superframe  
     - Provide two bounding cases: “per-slot acquisition” (current) and “per-superframe acquisition” (amortized), and show how the design point shifts. This would materially strengthen the robustness of conclusions.

5. **Campaign duty factor \(d\): improved realism, but default workload semantics remain potentially misleading for “routine operations”**  
   - **Why it matters:** The paper’s response to workload realism concerns is largely through \(d\), but the stress-case command model is still “512 B command per node per cycle” (fleet-wide), which is extreme. You do contextualize it as an upper bound and episodic, but the “routine \(\eta \approx 5\)–10%” claim depends on the assumed \(d\) and on the command semantics (broadcast vs unicast fraction \(q\)).  
   - **Remedy:** Provide a compact practitioner recipe: given a mission phase, how to estimate \(d\) and \(q\) from operational concepts (e.g., maneuvers per day, fraction of nodes commanded, typical command size). Include one additional workload profile where commands target only a subset of nodes (e.g., \(f_{\text{target}}\) of nodes per cycle) to demonstrate scaling of \(\eta_{\text{cmd}}\) with partial participation.

6. **GE correlated-loss modeling: useful sensitivity curves, but the coherence-time argument and ARQ infeasibility conclusion need tighter coupling to the TDMA timing model**  
   - **Why it matters:** You correctly state ARQ infeasibility is structural when \(\tau_{\text{coh}}\ge T_c\). However, the slot-level simulator results mix Model S and Model C in ways that could confuse the conclusion’s dependence on CCSDS overheads. Also, the retransmission policy (where retransmissions fit) should be explicit.  
   - **Remedy:**  
     - State explicitly the retransmission scheduling policy (do retransmissions occur immediately after a slot? at end of ingress? do they preempt egress?).  
     - Provide one table/figure repeating the ARQ coupling result under Model C at 30 kbps (even if it trivially shows “still infeasible under per-cycle coherence”), so the reader doesn’t have to reconcile Model S vs C mentally.

7. **Generalized \(\gamma\) expression: good, but needs a “how to use it” calibration checklist**  
   - **Why it matters:** Eq. (69) is potentially very useful, but only if engineers can map their radio/framing/FEC/acquisition to \(O_{\text{frame}}, R_{\text{FEC}}, T_{\text{guard}}, T_{\text{acq}}\). Right now, the paper gives one CCSDS instantiation and notes rate dependence, but not a general calibration workflow.  
   - **Remedy:** Add a short boxed checklist: “To compute \(\gamma\) for your system: (1) choose payload size \(S\); (2) compute framing bits; (3) choose coding and interleaving; (4) determine whether acquisition is per-slot or per-burst; (5) compute guard from geometry + timing error; (6) validate by measuring slot airtime on hardware or waveform sim.”

---

# Minor Issues

1. **\(\gamma_{C,24}\) numerical inconsistency:** text notes 0.765 \(\approx\) 0.760 and also mentions slot 115.5 ms vs 111.5 ms due to rounding. This is fine, but it appears in a way that may undermine confidence. Consider carrying more significant figures internally and rounding consistently in all tables.

2. **Terminology:** “MAC efficiency” is used for \(\gamma\), but \(\gamma\) includes PHY framing/FEC/acquisition. Consider renaming to “slot efficiency” consistently (you do in many places).

3. **Equation labeling:** Eq. (52) \(C_{\text{raw}} = C_{\text{coord}}/\gamma\) is potentially confusing because elsewhere \(C_{\text{coord}}\) is already a rate parameter. Ensure \(C_{\text{coord}}\) is always either info-rate or PHY-rate, not both.

4. **AoI interpretation:** You state “TDMA slots do not affect the inter-cycle metric.” True for periodic updates, but if queueing/deadline misses occur, AoI *is* affected. You do discuss losses separately, but consider one sentence clarifying the condition (no deadline misses, fixed \(T_c\)).

5. **Centralized baseline comparability:** you include a caveat, but Fig. 16 may still invite misinterpretation as a communications comparison. Consider visually separating “compute-only” baselines or moving them to an appendix.

6. **References:** Several key operational claims rely on non-archival sources. Where possible, add archival alternatives (FCC filings are better; for Starlink operations, consider peer-reviewed or conference analyses if available).

7. **Algorithm 1:** Line 7 uses \(R_{\text{PHY}} < C_{\text{coord,info}}/\gamma\) as an initial feasibility check, but later you incorporate \(\alpha_{\text{RX}}\) and explicit ingress/egress timing. Consider aligning the early check with the time-feasibility check (or clearly label it as a necessary-but-not-sufficient precheck).

---

# Overall Recommendation  
**Recommendation:** **Major Revision**

The paper is promising and closer to publishable than many early-stage “swarm scaling” manuscripts: it has a clear design objective, explicit assumptions, and a genuinely useful unification of byte budgeting with TDMA airtime feasibility. Version CI notably improves workload realism via the campaign duty factor \(d\), corrects/anchors \(\gamma\) using CCSDS-derived values (0.760/0.745), and more appropriately frames the \(\eta_S \approx 46\%\) stress case as a continuous-duty upper bound rather than a typical operating point.

The main reasons for Major Revision are not “more experiments,” but *tightening the engineering logic and defensibility* of the central sizing conclusions. In particular, the narrative around 27/30/35 kbps needs a single, unambiguous ladder from info-rate to PHY-rate to schedule feasibility; the “screening indicator” should be justified or demoted; and the CCSDS/Proximity-1-based \(\gamma\) derivation should explicitly treat acquisition as a per-slot vs per-burst assumption with bounding cases. Strengthening these points would make the framework substantially more credible and easier to apply correctly.

---

# Constructive Suggestions (ordered by impact)

1. **Unify the rate/feasibility story into one canonical workflow figure/table** (info-rate → \(\gamma\) → slot time → half-duplex partition → margin target → recommended PHY). Make every kbps number in the abstract and IV-A explicitly labeled.

2. **Add acquisition amortization bounds** in Section IV-J: per-slot \(T_{\text{acq}}\) (current) vs per-superframe/per-burst amortized \(T_{\text{acq}}\). Show how the minimum feasible PHY rate changes; this will significantly strengthen the CCSDS anchoring.

3. **Reframe DES as distributional/tail analysis** rather than “verification,” and add one additional DES-only result (e.g., buffer size vs overflow probability under ON/OFF + cluster-correlated campaigns).

4. **Clarify and formalize the three-layer feasibility framework**: define Layer 1 (byte), Layer 2 (airtime), and explicitly label \(\eta/\gamma\) as a heuristic utilization proxy unless you provide an empirical ROC-style justification.

5. **Strengthen the duty-factor \(d\) realism bridge**: add a partial-participation command model (\(f_{\text{target}}\)) and a short mapping recipe from operational events to \(d, q, f_{\text{target}}\).

6. **Specify retransmission scheduling policy** in the slot-level simulator and replicate at least one ARQ coupling result under Model C (even if it confirms “still infeasible”).

7. **Improve practitioner usability of Eq. (69)** by adding a calibration checklist and a minimal worked example beyond CCSDS Prox-1 (e.g., “if your system has continuous tracking, set \(T_{\text{acq}}\to 0\)”).

8. **Broaden TDMA/DAMA referencing** to better situate the schedulability analysis and to anticipate reviewer pushback that “this is just basic TDMA math” (your novelty is in applying it to this coordination sizing problem with explicit overhead accounting).

If you address the major issues above—especially the acquisition assumption bounding and the rate ladder clarity—I expect the manuscript could move to a strong “Minor Revision / Accept” trajectory for a top-tier aerospace systems journal.