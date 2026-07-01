---
paper: "02-swarm-coordination-scaling"
version: "cs"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-04"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript’s core contribution—closed-form, *per-cluster* sizing equations that separate (i) message-layer byte budget/utilization from (ii) TDMA airtime schedulability—is valuable and fairly novel for the “10³–10⁵ nodes” regime. The explicit “rate ladder” and the practitioner-facing Algorithm 1 are strong. The work is positioned as *preliminary design sizing* rather than validated performance prediction, which is appropriate given the admitted validation gap.

That said, the novelty is somewhat diluted by (a) heavy reliance on self-consistency checks (DES reproducing the same accounting) and (b) limited independent validation of the critical parameter(s) that drive the main design recommendation (γ, acquisition time, guard, half-duplex partition). The paper is still publishable in a top-tier venue if the authors tighten claims and improve the evidentiary separation between “derivation,” “anchoring,” and “validation.”

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The analytical decomposition (η vs. γ, plus Layer-2 airtime) is generally sound and clearly motivated. The TDMA slot model is explicit and the CCSDS-based γ derivation is a step forward. The GE sensitivity curves are useful as *design curves*.

However, several methodological choices still risk overconfidence in the 30/35 kbps conclusion: (i) the half-duplex partitioning via α_RX is derived from the same schedule being tested (not wrong, but it reduces the independence of “Layer 2” as a check), (ii) ARQ modeling is simplified and partially demonstrated under Model S (upper bound), and (iii) the packet-level “validation” is primarily parameter estimation from a standard plus assumed times, not an independent measurement.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Internal logic is mostly consistent, and the manuscript is much clearer than earlier versions typically are on “what is assumed vs. what is claimed.” The duty factor d is now explicitly treated as a workload realism parameter and the 46% stress case is framed as a continuous-duty bound.

Remaining validity concerns are primarily about boundary conditions and double-counting/under-counting risks:
- The paper repeatedly asserts “two-layer feasibility,” but in practice there are at least **three** constraints: information byte budget, TDMA airtime, and **reliability/recovery** (loss + ARQ policy) which can force additional airtime or multi-cycle latency. You do discuss ARQ×TDMA coupling, but it is not fully integrated into the feasibility test in Algorithm 1 beyond a generic “margin warning.”
- Several conclusions depend on *specific* choices (k_c=100, S=256B, T_c=10s, acquisition=5 ms, guard=4.7 ms, LDPC 7/8). The general scaling form is given, but the paper’s rhetoric sometimes reads like a robust “recommendation” rather than a conditional design point.

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
The manuscript is well organized and unusually explicit about definitions (baseline vs η, model C vs S, evidence tiers). Tables like the rate ladder, feasibility table, and claim map are helpful. The “Do not double-count” callout is excellent.

Clarity issues that remain:
- The manuscript is long and sometimes repeats key points (e.g., Model S disclaimers, “no external validation”) at the cost of tightening the actual design logic.
- Some parameters appear “derived” but are in fact schedule-dependent choices (α_RX, egress allocations). This is fine, but needs sharper wording to avoid implying these are externally validated constants.

---

## 5. Ethical Compliance  
**Rating: 4 (Good)**  
Strong reproducibility posture: code + tag, environment, and datasets. AI disclosure is present and appropriately scoped (ideation + prose only). No human-subject concerns.

One missing element for top-tier reproducibility: you should provide a *single command/script* (or Makefile) that regenerates every figure/table used for decision claims, plus a checksum of the tag/commit. Many IEEE reviewers now look for “one-click rebuild” for simulation papers.

---

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
The paper fits IEEE TAES / Adv. Space Research in theme (swarm/constellation coordination, comms constraints). Referencing is broad, but some key adjacent literatures are underused given your claims:
- **LEO ISL MAC/TDMA scheduling and link acquisition** literature beyond CCSDS/DVB-RCS2 (even if not identical) could better contextualize γ, acquisition, and guard assumptions.
- **AoI under erasures / correlated loss** has a large literature; you use the geometric sampling tail result, but you could cite AoI with retransmissions and burst channels to justify inter-cycle recovery choices.
- For the “hierarchical coordination” framing: some constellation operations/ISL architecture papers (Iridium NEXT, Starlink ISL discussions, or academic LEO ISL scheduling) would strengthen the grounding.

---

# Ten scored sections (as requested)

## 7. Workload Realism & Duty Factor Modeling (d)  
**Rating: 4 (Good)**  
The duty factor is a meaningful knob and you now map it to mission phases with an ESA anchor. The explicit statement “46% is continuous-duty upper bound, <1% time” is a clear improvement.

Remaining gap: the *distribution* of campaigns (cluster-correlated ON/OFF) is only lightly explored. If coordinator buffer sizing is a key “DES value,” you should tie d and correlation structure more directly to real operational timelines (orbit-raising cadence, contact opportunities, maneuver windows).

## 8. TDMA/MAC Modeling & Three-layer Feasibility Framework  
**Rating: 3 (Adequate)**  
The framework is close to solid, but it is not fully “three-layer” in practice. You present (i) byte budget, (ii) MAC efficiency conversion C_raw = C_info/γ, and (iii) TDMA airtime. Then you explicitly say the MAC efficiency step is *not* a third test. That’s fine—but then the paper should stop calling it “three-layer” elsewhere (or reframe it as “two-layer + conversion factor”).

Also, the feasibility test should explicitly include **retransmission airtime reservation** as part of Layer 2 when ARQ is enabled, rather than treating it as a post-hoc margin discussion.

## 9. DES/Monte Carlo Value and Verification Strategy  
**Rating: 3 (Adequate)**  
You are admirably honest that DES reproduces its own equations. The distributional buffer sizing is the main incremental value, and that is a legitimate use of DES.

But to justify DES in a top-tier paper, you should add at least one result that cannot be obtained from your closed-form means with trivial algebra—e.g., quantify overflow probability vs buffer size under correlated campaigns + GE + failures, or show tail latency/AoI under joint burstiness and coordinator outages with confidence intervals.

## 10. Independent Validation / Packet-level Anchoring (Section IV-J)  
**Rating: 2 (Below Average)**  
Section IV-J is an improvement (γ=0.74–0.76 grounded in CCSDS framing), but it still does not constitute independent validation. It is a parameter *estimate* using nominal overhead bits plus assumed acquisition time; the most sensitive component (T_acq) is assumed. The “DVB-RCS2 measured slot efficiency 0.70–0.85” citation helps but is not clearly translated into a conservative bound for Proximity-1-like ISLs.

For a top-tier venue, you either need (a) a modest hardware-in-the-loop/SDR measurement of acquisition + framing overhead for a representative modem, or (b) a much stronger uncertainty quantification showing how conclusions move across plausible distributions of T_acq, guard, and implementation overhead.

---

# Major Issues (must address)

1) **Feasibility framework is not fully integrated with loss recovery (ARQ) as a first-class constraint.**  
**Why it matters:** Your headline recommendation (30 kbps minimum, 35 kbps recommended) is driven largely by *airtime margin* and whether ARQ can fit. Yet Algorithm 1 and the Layer-2 feasibility equations do not explicitly incorporate retransmission slot reservation based on a target delivery probability or GE parameters. This makes the “recommended 35 kbps” feel partly ad hoc.  
**Remedy:** Extend Algorithm 1 / Layer-2 test to include an explicit ARQ reservation term, e.g.  
- choose a target per-cycle delivery (or AoI bound),  
- compute expected/quantile retransmissions under GE (or worst-case under slow-mixing),  
- reserve \(M_r\) retransmission slots and re-check \(T_{\text{ing}}(1+\bar M_r)\le T_c\alpha_{RX}\).  
At minimum, add a “Layer 2b: recovery airtime” check with a clearly stated design target (e.g., “P95 recovery within 1 cycle” or “per-cycle delivery ≥ X%”).

2) **Model S is used for the ARQ×TDMA coupling demonstration, but the paper’s key conclusions are under Model C.**  
**Why it matters:** Table IV-D (deadline miss coupling) is the *only* “emergent” finding, but it is demonstrated under the simplified timing model where 24 kbps is feasible absent ARQ—whereas under Model C, 24 kbps is infeasible regardless. This weakens the practical relevance of the coupling result to the actual recommended design point.  
**Remedy:** Replicate the coupling experiment under **Model C** at 30 kbps and 35 kbps (and perhaps 28–40 kbps sweep), showing (i) miss probability vs reserved retransmission slots, (ii) delivery/AoI impact, and (iii) sensitivity to T_acq. If coupling is negligible at 35 kbps but material at 30 kbps, that directly supports the recommendation.

3) **γ “unification” appears mostly consistent (0.74–0.76), but you still have scattered places where γ is treated as a constant rather than γ(R_PHY).**  
**Why it matters:** Rate dependence is central to your feasibility boundary. Any lingering constant-γ usage can silently bias computed margins and could invalidate the “24 infeasible / 30 feasible” boundary if misapplied.  
**Remedy:** Add a systematic audit:  
- Ensure every place that uses γ specifies γ_24, γ_30, or γ(R_PHY).  
- In tables/figures, label γ explicitly with the rate.  
- Consider adding a short “γ usage checklist” in an appendix: where γ enters equations, what value is used, and why.

4) **Campaign duty factor d addresses realism, but the paper still lacks a defensible operational workload model tying d to command semantics and coordination cycle.**  
**Why it matters:** The main criticism readers will have is “1 command per node per cycle is unrealistic; therefore 46% is irrelevant.” You respond by making it an upper bound and introducing d, which is good—but you don’t fully justify why d=0.10 is a conservative default across mission classes, nor how command sizes/frequency relate to actual constellation ops.  
**Remedy:** Strengthen the mapping from operations to parameters: provide a small table of *command classes* (broadcast schedule update, maneuver plan, software patch, collision alert) with typical sizes, fanout (broadcast vs unicast fraction q), and typical cadence. Then compute implied d (or p_cmd) from those cadences. This would make d more than a free knob.

5) **DES “verification” still reads too much like validation; the paper needs at least one externally grounded cross-check beyond CCSDS bit accounting.**  
**Why it matters:** Top-tier journals expect some independent anchoring. Right now, Tier-2 is mostly “slot-sim reveals coupling” and “γ computed from standards.” That is not validation of real-world feasibility.  
**Remedy (choose one feasible path):**  
- **Minimal measurement path:** Measure acquisition/turnaround timing and framing overhead using an SDR or COTS radio in a lab loopback, and report empirical γ distribution (mean/variance) under representative conditions.  
- **Network simulation path:** Use NS-3 (even small-scale) to show contention-free TDMA schedule feasibility and to bound additional overhead from control/sync.  
If neither is possible, tighten claims further: explicitly state that “35 kbps recommended” is conditional on assumed T_acq and implementation; present it as a *design study* not a recommendation.

6) **Fleet-level reuse (R, F, f_RF) is too hand-wavy relative to how prominently it is used to argue scalability.**  
**Why it matters:** The paper’s scope is “large swarms,” but the fleet-level extension is acknowledged as order-of-magnitude. Still, Eq. (fleet reuse) can be misread as a validated scaling law.  
**Remedy:** Either (a) demote fleet reuse to an appendix with clearer caveats and remove any implication of rigorous scalability at fleet level, or (b) add a simple interference/geometry model (even coarse) that yields R as a function of antenna pattern, EIRP, required C/I, and cluster geometry, with sensitivity bands.

---

# Minor Issues

1) **Terminology: “three-layer feasibility framework.”** You mostly implement two-layer + conversion. Use consistent naming throughout to avoid reviewer confusion.  
2) **α_RX definition:** You define it as “derived from schedule” but then use it in Eq. (coord_phy) like an external parameter. Consider eliminating α_RX from the closed form by substituting α_RX = T_ing/T_c and expressing R_PHY,min directly in terms of slot components.  
3) **Table IV-D labeling:** The “MODEL S TIMING—UPPER-BOUND” disclaimer is good, but the table remains central. Consider moving it to an appendix unless you add the Model C counterpart.  
4) **AoI discussion:** You correctly interpret P99=440 s as sampling-tail, but you should explicitly separate “AoI due to sampling policy” from “AoI due to network loss/recovery,” possibly with an additive decomposition under independence assumptions.  
5) **GE coherence assumption:** You state GE transitions once per T_c; this bakes in ARQ inefficacy. You do acknowledge this, but consider adding a second case where transitions occur per slot (fast-mixing) to show the full range (you partially do). Put both into the feasibility procedure as selectable regimes.  
6) **Command message size justification:** You cite CCSDS SPP maximums; that’s not the same as typical operational command sizes. Consider adding at least one citation or ops doc indicating typical maneuver plan uplink sizes (even terrestrial analogs) or justify with a “conservative envelope” framing.  
7) **Units and rounding:** Several margins (e.g., “-1,300 ms” vs earlier “-1,635 ms”) appear in different places; ensure these are consistent with the same egress allocation and unrounded intermediates.

---

# Overall Recommendation  
**Recommendation:** **Major Revision**

The manuscript is promising and closer to publishable than many “sizing framework” papers because it is explicit about assumptions, provides reusable equations, and cleanly separates byte budget from airtime schedulability. The duty factor d addition and the CCSDS-based γ (≈0.74–0.76) are meaningful improvements, and the stress-case η_S≈46% is now more appropriately contextualized as a continuous-duty upper bound rather than a typical workload.

The main blockers for a top-tier acceptance are (1) the incomplete integration of reliability/recovery (ARQ under GE) into the feasibility framework and Algorithm 1, and (2) the limited independent validation of the key parameter(s) driving the 30/35 kbps boundary, especially acquisition time and the practical γ distribution. Additionally, the one “emergent” finding (ARQ×TDMA coupling) is currently demonstrated under Model S rather than the CCSDS-grounded Model C used for recommendations, weakening its decision relevance. Addressing these issues—either by adding Model C coupling results and incorporating ARQ reservation into the feasibility test, or by tightening claims and reframing recommendations as conditional design-study outputs—would substantially strengthen the paper.

---

# Constructive Suggestions (ordered by impact)

1) **Make ARQ/recovery a first-class part of Layer-2 feasibility.** Add a “recovery airtime” term and a clear design target (delivery or recovery within K cycles). Update Algorithm 1 accordingly.  
2) **Re-run the ARQ×TDMA coupling study under Model C at 30 and 35 kbps.** Show miss probability vs retransmission reservation and GE parameters; directly connect to why 35 kbps is recommended.  
3) **Add uncertainty quantification on γ and T_acq.** Treat T_acq as a random variable (or bounded interval) and propagate to R_PHY,min; present a robustness plot: P(feasible) vs R_PHY under plausible distributions.  
4) **Strengthen workload realism mapping.** Provide command class taxonomy with typical cadence, fanout q, and sizes; compute implied d and show that routine ops indeed sit in η≈5–10%.  
5) **Clarify “two-layer vs three-layer.”** Standardize terminology; if you keep “three-layer,” define the third as a genuine constraint (e.g., reliability) rather than a unit conversion.  
6) **Increase DES value with a nontrivial tail result.** For example: overflow probability vs buffer size under correlated campaigns + failures; or AoI tail under joint outages and inter-cycle recovery.  
7) **Demote or strengthen fleet reuse.** Either provide a simple C/I-based reuse model with sensitivity, or move reuse discussion to limitations/appendix and reduce reliance on it for scaling claims.