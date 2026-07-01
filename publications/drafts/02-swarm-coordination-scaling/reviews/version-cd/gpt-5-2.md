---
paper: "02-swarm-coordination-scaling"
version: "cd"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-28"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript tackles an important and under-served problem: providing *closed-form, parametric sizing* for coordination communications in very large spacecraft swarms (10³–10⁵). The separation of (i) message-layer byte budget and (ii) PHY/MAC schedulability (TDMA airtime, half-duplex) is a meaningful framing that many papers blur. The addition of a standards-grounded derivation for MAC efficiency (γ) is also a step toward engineering realism.

Novelty is strongest in the *design-equation packaging* (including the three-layer feasibility checks and the coordinator ingress sizing) rather than in fundamentally new coordination algorithms. The work reads as an engineering sizing/feasibility paper; for T-AES/ASR that can be valuable if the assumptions and validation boundaries are very explicit and the “what practitioners should do with this” is sharpened.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The methodology is generally coherent: analytic byte accounting, a cycle-aggregated DES for distributions, a slot-level TDMA simulator for half-duplex schedulability, and a packet-level framing model to anchor γ in CCSDS. That said, several modeling choices create ambiguity about what is being “validated” versus “reproduced,” and some assumptions (broadcast semantics, fixed cluster membership, campaign model, loss coherence) are pivotal enough that they need tighter justification and/or sensitivity.

The Monte Carlo setup (30 reps, 1-year runs, bootstrap CIs) is fine for mean overhead and some tails, but the tails being emphasized (AoI P99, recovery P95) are largely driven by closed-form geometric/Markov relationships; the DES is not clearly adding independent uncertainty quantification beyond confirming those relationships.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Internally, the paper is mostly consistent and the duty-factor gating is a reasonable remedy to “continuous stress workload” realism concerns. The manuscript also does a better job than earlier versions (as implied by your notes) of contextualizing the stress case as a continuous-duty upper bound and separating η₀ vs η_cmd.

However, there are remaining logical tensions:
- The “topology-invariant command overhead” conclusion depends critically on a *broadcast* command model and centralized command generation; later sections discuss unicast staggering and consensus alternatives, but the main claims still read too general.
- The three-layer feasibility framework is directionally right, but Layer 2 (“η_total/γ”) is not a true feasibility test and can mislead if read as such; Layer 3 is the real constraint, and it depends on *directionality*, half-duplex partitioning, and addressing mix.
- The γ unification is improved (0.76 from CCSDS framing), but the manuscript still mixes “γ at 24 kbps” with “design at 30 kbps” in ways that can confuse; rate-dependence is acknowledged but not consistently propagated through all key capacity numbers and tables.

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
The paper is well organized, with helpful notation, a clear decomposition of overhead, and a strong “claim map” table. The explicit disambiguation of DES vs slot-sim vs packet-level is also good practice.

Clarity issues remain in (i) what exactly η includes/excludes in each table/plot, (ii) the relationship between “1 kbps per node budget” and “24–30 kbps coordinator PHY,” and (iii) the operational meaning of AoI results (especially the 440 s P99) for actual swarm functions. Some tables (e.g., cross-model comparison) appear to mix parameterizations in a way that invites misinterpretation.

---

## 5. Ethical Compliance  
**Rating: 4 (Good)**  
Data/code availability is strong (tagged repository, environment listed). The AI-assisted ideation disclosure is present—good and increasingly necessary.

Two improvements needed for reproducibility: (1) provide a deterministic “paper reproduction script” that regenerates every figure/table from the tagged release; (2) clearly document all default parameter files and how they map to the manuscript’s “representative instantiation,” including any differences between DES/slot-sim/pkt-sim parameter sets.

---

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
The paper is broadly in scope for T-AES (space communications/architectures, autonomy-enabling comms constraints). Referencing is decent across distributed systems, swarm robotics, and CCSDS standards.

Gaps: the MAC/TDMA literature for satellite ISLs and half-duplex scheduling is not as deeply engaged as it could be (beyond CCSDS Prox-1). Also, the “mega-constellation” networking literature cited is more routing-focused; you should add work on ISL MAC scheduling, satellite TDMA superframes, and practical ranging/acquisition overheads for smallsat crosslinks (including any vendor/app notes if archival sources exist). The AoI discussion could cite more directly AoI under periodic sampling + erasures (many results exist) to avoid the impression that the AoI P99 is “discovered” rather than a direct consequence of a geometric model.

---

## 7. Technical Depth  
**Rating: 4 (Good)**  
The derivations are mostly straightforward but useful. The packet-level γ decomposition is a concrete engineering contribution (if correct and consistently applied). The half-duplex airtime feasibility check and the unicast staggering equation are practically relevant.

Depth is limited where the paper gestures at “consensus overhead” and “distributed planning” without a fully consistent alternative workload model. If you keep those sections, they should either be (i) clearly labeled as illustrative back-of-envelope extensions, or (ii) supported by a consistent message model and feasibility check.

---

## 8. Results & Evidence  
**Rating: 3 (Adequate)**  
Results are extensive, but the evidentiary value is mixed because many plots/tables are effectively restatements of the same accounting assumptions. The slot-level simulator does add genuine value by revealing ARQ×TDMA coupling and half-duplex deadline misses—this is a real contribution.

The AoI and GE recovery results are largely analytic; the DES confirmation is fine, but the paper should not oversell it as validation. Also, the “30 kbps minimum viable” claim is compelling *if* γ and acquisition/guard assumptions are defensible; right now, the 5 ms acquisition dwell is asserted as “typical” and needs either citation or sensitivity.

---

## 9. Practical Relevance  
**Rating: 4 (Good)**  
The sizing equations, feasibility layers, and coordinator ingress sizing are actionable for early-phase architecture trades. The duty factor (d) is a useful knob to translate “stress case” into campaign realism—this directly addresses workload realism concerns.

To maximize practical relevance, the paper should include a short “how to use this” procedure (inputs → compute η₀, η_cmd, γ(R_PHY), Layer 1–3 checks → choose k_c, R_PHY, d bounds) and provide a worked example beyond the single default instantiation (e.g., two alternative S_eph sizes, different T_c, and a non-broadcast command mix).

---

## 10. Overall Presentation Quality  
**Rating: 4 (Good)**  
Overall presentation is strong for a sizing/engineering paper: notation table, claim map, layered feasibility, and clear parameter tables. The main weaknesses are consistency (γ and rate dependence), and ensuring the “validation tiers” are not interpreted as stronger than they are.

---

# Major Issues

1. **γ (0.76) is not propagated consistently across all “minimum viable rate / margin” claims, and rate-dependence is under-integrated.**  
   **Why it matters:** The headline conclusion (“30 kbps is minimum viable”) hinges on γ. You acknowledge γ is rate-dependent (0.760 @24 kbps, 0.745 @30 kbps), but many computations and tables appear to treat γ as fixed while simultaneously comparing 24 vs 30 kbps feasibility. This risks an internal inconsistency and undermines the standards-grounded argument.  
   **Remedy:**  
   - Define **γ(R_PHY)** as the default, and whenever you compute capacity/margins at 30 kbps, use γ(30 kbps) explicitly.  
   - Add a single “master” table: for R_PHY ∈ {24, 30, 50} kbps, list γ(R_PHY), slot time, ingress time, egress time, and margin.  
   - Audit every instance where 0.76 is used and ensure it is either (i) explicitly “γ at 24 kbps,” or (ii) replaced by γ(R_PHY).  
   - In Eq. (gamma_general), check units (the “/1000” term is suspicious unless R_PHY is in kbps; currently it states bps). Fix and re-derive numerically.

2. **The three-layer feasibility framework is conceptually good but currently risks misleading readers about Layer 2.**  
   **Why it matters:** Layer 2 (“η_total/γ”) is necessary but not sufficient; Layer 3 (half-duplex airtime with directionality and addressing) is the true schedulability test. Presenting Layer 2 as a “feasibility layer” may lead practitioners to stop too early.  
   **Remedy:**  
   - Rename Layer 2 to something like **“PHY utilization lower bound”** or **“necessary condition”**.  
   - Explicitly state: *Layer 2 passing does not imply schedulability; Layer 3 must be checked whenever half-duplex and slotting are relevant.*  
   - Provide a compact algorithm/pseudocode for the three checks with clear pass/fail outputs.

3. **Workload realism: duty factor (d) helps, but the stress-case (η_S≈46%) still needs sharper operational interpretation and mapping to plausible campaign durations.**  
   **Why it matters:** Reviewers will still ask “who commands every satellite every 10 s continuously?” You now label it as a continuous-duty upper bound (good), but you should anchor d to real mission phases (orbit raising, collision response, safe-mode) with time fractions.  
   **Remedy:**  
   - Provide 2–3 concrete duty-factor scenarios (e.g., orbit-raising for X days, station-keeping weekly, emergency response) and compute annualized average η and peak η.  
   - For the ON/OFF Markov campaign, report not just ingress CDF but also **required buffer size vs. P99/P999** under plausible L_on.

4. **DES “verification” is still largely self-confirmation; the manuscript should tighten the claim about what DES adds.**  
   **Why it matters:** Top-tier journals will penalize “simulation validates equations” when simulation implements the same equations. You correctly acknowledge this in places, but the narrative still sometimes implies validation strength.  
   **Remedy:**  
   - Reframe DES as **distributional characterization** and **composition testing** (joint interactions) rather than verification of means.  
   - Move the “DES matches closed-form <0.1%” to an appendix or compress it; emphasize instead the *bimodality/heavy-tail* results and any nontrivial emergent behavior.

5. **Packet-level validation (Section IV-J) is valuable but not yet fully “independent” because γ is still partly assumed (guard, acquisition) and the simulator details are thin.**  
   **Why it matters:** The key contribution “γ=0.76 validated via CCSDS” will be scrutinized. If guard and acquisition are not standards-mandated, γ is not truly anchored.  
   **Remedy:**  
   - Separate **standards-mandated overhead** (ASM, headers, FEC rate) from **implementation/operational overhead** (acquisition dwell, ranging).  
   - Provide sensitivity: vary T_acq ∈ {0, 2, 5, 10} ms and show resulting γ and minimum feasible R_PHY for k_c=100.  
   - Document the packet-level simulator precisely: framing fields included, interleaving, whether idle fill exists, whether acquisition is per-slot or per-burst, etc.

6. **Command addressing model (broadcast vs per-node unicast mix q) is central but underused in the main conclusions.**  
   **Why it matters:** Many realistic coordination commands are not pure broadcast; if q is nontrivial, Layer 3 airtime becomes dominant and can inflate completion time/AoI. Your Eq. (unicast_stagger_q) is good but feels like a side branch.  
   **Remedy:**  
   - Promote q to a first-class parameter in the workload model and feasibility tables.  
   - Add a figure/table: feasible region in (q, k_c, R_PHY) space for single-cycle completion.  
   - Clarify what fraction of commands in your intended application are broadcastable.

7. **AoI result (P99=440 s) is mathematically consistent but operationally ambiguous and potentially alarming without context.**  
   **Why it matters:** Readers may interpret 440 s stale state as unacceptable for collision avoidance or formation flight. You partly address this by noting TCAs are hours, but that conflates screening vs maneuver decision loops.  
   **Remedy:**  
   - Explicitly separate **what variable AoI is measuring** (exception telemetry updates) from **the control loop** that would require <10 s updates.  
   - Provide a short “AoI requirement mapping” table: which functions tolerate 440 s, which do not, and which channel (RF backup vs optical ISL) supports them.

---

# Minor Issues

1. **Eq. (gamma_general) units:** term “(T_guard + T_acq) × R_PHY / 1000” conflicts with R_PHY labeled in bps. Make units consistent and show one worked numeric substitution.  
2. **Table cross_model:** “Analyt ingress 30 kbps = 6,930 ms” vs slot/pkt 9,078 ms suggests different assumptions (γ=1? half-duplex partitioning? guard/acq?). Clarify what each column includes.  
3. **η₀ audit inconsistency:** text says heartbeats 5.1%, summaries 0.4%, election <0.1% ⇒ 5.6%, but earlier η₀≈5%. You mention coordinator self-exclusion; make this explicit with the exact formula.  
4. **Coordinator ingress sizing equation in abstract:** uses “k_c S_eph × 8 /(T_c γ)” but ingress is *k_c−1* members; be consistent (or state approximation).  
5. **Failure/availability numbers:** Table says hierarchical availability 99.5%; later says per-coordinator availability >99.99% and 99.5% is conservative. Provide the conservative model explicitly (what cascading effects assumed).  
6. **Sectorized mesh comparator:** ensure it is not perceived as a strawman; consider moving it to an appendix or tightening language further to avoid “not comparable” while still presenting it.  
7. **Link budget table:** “Max rate ~2.5 kbps” depends strongly on required Eb/N0 and coding; consider adding coding assumption consistent with the γ/FEC discussion.  
8. **Terminology:** “validated via CCSDS” should be softened to “derived/anchored” unless you have empirical radio measurements.  
9. **Static topology:** you quantify reassociation overhead; good. Consider adding a sensitivity for higher churn (e.g., cross-plane clusters) to show robustness of <0.5%.

---

# Overall Recommendation  
**Recommendation:** **Major Revision**

The manuscript has a solid core contribution: a layered sizing framework with closed-form equations and a credible half-duplex TDMA feasibility check, plus an effort to ground MAC efficiency in CCSDS framing. The duty-factor parameterization is a meaningful improvement for workload realism, and the stress-case is now closer to being appropriately framed as a continuous-duty upper bound. The slot-level simulator’s finding about ARQ infeasibility under correlated per-cycle GE coherence is also a genuine and useful insight.

The main reasons for major revision are (i) consistency and correctness around γ and its rate dependence (this underpins the key 30 kbps conclusion), (ii) sharpening what is and is not validated (DES vs analytic vs slot vs packet-level), and (iii) elevating addressing mix (broadcast/unicast fraction) and operational duty-factor scenarios into the main narrative so the results are not misread as overly general. Addressing these points would substantially strengthen credibility and practitioner utility.

---

# Constructive Suggestions (ordered by impact)

1. **Do a full γ audit and make γ(R_PHY) the default everywhere.** Add a single consolidated feasibility/margin table for 24/30 kbps with γ computed at each rate and with clear inclusion/exclusion of acquisition/guard/ranging.  
2. **Recast the three-layer framework to emphasize Layer 3 as the decisive test** under half-duplex TDMA, and rename Layer 2 as a necessary condition. Provide a step-by-step “how to size” procedure.  
3. **Promote command addressing mix q to a primary parameter** and present feasibility regions in (q, k_c, R_PHY). Make clear which mission classes justify q≈0.  
4. **Strengthen workload realism with 2–3 concrete duty-factor campaign narratives** (durations and fractions of year), and report annualized averages plus peak/buffer requirements under ON/OFF campaigns.  
5. **Clarify validation claims:** tighten language so “verification” means code consistency; reserve “validation” for standards anchoring and any independent checks.  
6. **Make packet-level γ derivation more defensible:** separate standards-mandated vs implementation overhead, cite acquisition dwell or bracket it with sensitivity, and document simulator assumptions.  
7. **Operationalize AoI:** add a short requirements mapping and avoid conflating screening alerts with maneuver loop requirements.  
8. **Provide a reproducibility entry point:** one command/script to regenerate all manuscript figures/tables from the tagged repo, plus a parameter manifest for each simulator tier.