---
paper: "02-swarm-coordination-scaling"
version: "cz"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-05"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript targets an important and under-served niche: *closed-form, byte-accounted sizing* of coordination traffic for very large spacecraft swarms, with explicit separation between (i) message-layer budget feasibility and (ii) TDMA airtime feasibility. The two-test framing and the “rate ladder” from information-rate → PHY-rate (with half-duplex partitioning) is practically useful for early-phase design. The explicit campaign duty factor \(d\) is a meaningful step toward workload realism compared with always-on stress traffic.

Novelty is strongest in the *engineering synthesis* (Algorithm 1 + rate ladder + \(\gamma(R_{\mathrm{PHY}})\) time-domain expression) rather than in new theory. The paper is candid about limited external validation, which is appropriate but also limits archival impact unless the claims are carefully scoped.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The analytical accounting is generally consistent, and the TDMA schedulability check is framed in a way that engineers can reproduce. The CCSDS-based \(\gamma\) derivation is an improvement over earlier “fixed \(\gamma\)” assumptions and is mostly applied consistently.

However, several methodological choices materially affect the key conclusion (“24 kbps infeasible, 30 kbps minimum, 35 kbps recommended”): (a) per-slot acquisition time \(T_{\mathrm{acq}}\) (5 ms) and its assumed *per-slot* nature, (b) the treatment of ACKs “inside guard/jitter,” (c) the definition/derivation of \(\alpha_{\mathrm{RX}}\) and its use in the heuristic, and (d) the GE coherence assumption that makes intra-cycle ARQ ineffective “by construction.” These are defensible as design assumptions, but they need sharper justification and clearer separation between *what is derived* vs *what is assumed*.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Internal logic is mostly coherent, and the manuscript does a good job warning readers not to double-count the heuristic and slot-level check. The stress-case contextualization (46% as continuous-duty upper bound, <1% time) is a clear improvement, and the duty-factor mixture example helps.

Remaining validity concerns are about *boundary conditions and coupling*:
- The three-layer feasibility story (byte budget, MAC efficiency, TDMA airtime) is stated as two tests, but the narrative still sometimes treats “\(1/\gamma\)” as quasi-independent. The paper must be extremely consistent that \(\gamma\) is purely a mapping inside Test B, not a separate feasibility layer.
- Some “feasible/infeasible” statements depend on schedule micro-structure (ACK placement, reacquisition model). Those should be presented as conditional results, not absolute boundaries.

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
Overall organization is strong: notation table, explicit “two-test feasibility framework” box, rate ladder table, and Algorithm 1 are effective. The manuscript is unusually explicit about V&V tiers and validation gaps—commendable for this topic.

Clarity issues remain where the paper mixes “Model S vs Model C” results (e.g., Table IV-D) and where definitions of baseline vs overhead vs total utilization could still confuse readers. Some claims are repeated with slightly different numbers (e.g., \(\gamma\) values, margins) and would benefit from a single “authoritative source of truth” (likely the rate ladder + feasibility table).

---

## 5. Ethical Compliance  
**Rating: 4 (Good)**  
- **Reproducibility/data:** Code and tag are provided; parameter tables are included; this is above average.  
- **AI disclosure:** Explicitly disclosed and appropriately scoped (prose editing only; no results).  
- **Caveat:** For a top-tier journal, consider adding a reproducibility checklist: exact commit hash, instructions to regenerate each key figure/table, and random seed handling (you state sequential seeds; specify determinism and how to reproduce bootstrap CIs).

---

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
The work fits IEEE TAES / space systems communications and autonomy. Referencing is broad and mostly appropriate (CCSDS, AoI, Raft, DTN, DVB-RCS2). That said:
- The MAC/TDMA literature in satellite ISLs and proximity links could be strengthened (even if only to justify why deterministic TDMA is assumed and what alternatives would change).
- For GE/burst-loss modeling, citing additional space/LEO channel measurement studies (even if not ISL-specific) would help contextualize parameter choices and coherence-time regimes.

---

# Major Issues

1) **Key conclusion hinges on per-slot acquisition assumption; needs stronger justification and alternate cases**  
**Why it matters:** The “24 kbps infeasible / 30 kbps minimum / 35 kbps recommended” result is driven heavily by fixed-time overheads, especially \(T_{\mathrm{acq}}=5\) ms *per slot*. If practical implementations maintain lock across a burst/superframe (or use shorter reacquisition), \(\gamma\) increases materially and the boundary shifts.  
**Specific remedy:**  
- Promote the “acquisition architecture” discussion into the main feasibility argument: explicitly compute feasibility under (i) per-slot acquisition, (ii) per-burst acquisition, (iii) continuous tracking, and show how the recommended PHY rate changes.  
- In Table VIII (rate feasibility) add columns for these acquisition modes (or provide a parallel table).  
- Clarify whether CCSDS Prox-1 actually implies per-slot acquisition in your intended burst TDMA operation, or whether this is a conservative engineering assumption.

2) **ACK-in-guard treatment is under-justified and risks hidden double counting / schedule infeasibility**  
**Why it matters:** You claim a 0.5 ms ACK mini-slot “fits inside jitter sub-slot” without additional allocation. This is a nonstandard and fragile assumption: guard time is typically “dead time” to prevent overlap under uncertainty; using it for deterministic transmissions requires tight timing guarantees and changes the meaning of guard. If incorrect, your margins shrink and feasibility boundaries shift.  
**Specific remedy:**  
- Make ACK timing explicit in the superframe budget: either allocate ACK airtime explicitly or provide a rigorous argument with timing diagram showing deterministic offset, required clock sync, and residual uncertainty bounds.  
- If ACKs are optional, present two ARQ variants: (a) explicit ACK slots (conservative), (b) implicit/NACK-only or aggregated ACK at end of ingress (common in scheduled systems).

3) **\(\alpha_{\mathrm{RX}}\) is presented as “derived,” but it is also used as a parameter in the PHY heuristic—needs tighter definition**  
**Why it matters:** The heuristic \(R_{\mathrm{PHY,min}} \ge C_{\mathrm{coord,info}}/(\gamma\alpha_{\mathrm{RX}})\) can be misapplied unless \(\alpha_{\mathrm{RX}}\) is uniquely determined by the schedule and includes/excludes ARQ consistently. Currently \(\alpha_{\mathrm{RX}}\) changes with \(M_r\) and rate, but the heuristic appears in places as if it were a fixed fraction.  
**Specific remedy:**  
- Define \(\alpha_{\mathrm{RX}}\) formally as a *schedule decision variable* (or as the computed ingress fraction under a specific canonical schedule).  
- Provide a short derivation showing when the heuristic is equivalent to Test B and when it is only a lower bound (e.g., when egress is non-negligible, when ARQ slots are reserved, when unicast staggering is used).  
- In Algorithm 1, compute \(R_{\mathrm{PHY,min}}\) without separately using \(\alpha_{\mathrm{RX}}\) (since it is computed from \(T_{\mathrm{ing}}\)), or clearly state it is purely a reporting quantity.

4) **GE “coherence once per cycle” assumption makes intra-cycle ARQ ineffective by construction; value of ARQ coupling result is therefore limited**  
**Why it matters:** The paper highlights ARQ×TDMA coupling as an emergent finding (52.7% misses), but Section IV-C also states that intra-cycle retransmissions see the same GE state, so ARQ is structurally ineffective when \(\tau_c \ge T_c\). That makes “ARQ demand” and its schedulability less informative, and the coupling table (Table IV-D) is based on Model S timing anyway.  
**Specific remedy:**  
- Either (a) revise the GE model to allow intra-cycle state evolution when \(\tau_c \ll T_c\) (even a two-timescale Markov model: per-slot transitions within a cycle), or (b) explicitly demote ARQ×TDMA coupling to an illustrative artifact of the slow-mixing regime and focus on *inter-cycle recovery* as the main result.  
- If you keep both regimes, provide a regime map: \(\tau_c/T_c\) vs recommended policy (no ARQ + inter-cycle vs ARQ-enabled), and recompute schedulability under a fast-mixing intra-cycle loss model.

5) **Three-layer feasibility narrative still risks confusion; tighten the “two tests only” claim and remove ambiguous phrasing**  
**Why it matters:** You emphasize “two-test feasibility” but repeatedly compute \(C_{\mathrm{raw}}=C_{\mathrm{info}}/\gamma\) and discuss “MAC efficiency” as if it were a separate layer. Reviewers/readers may interpret this as a third check or double-count overhead.  
**Specific remedy:**  
- Make a single canonical pipeline figure: Information bytes → Test A; Information bytes + slot model (\(\gamma\)) → airtime → Test B.  
- Remove or rephrase any text that implies “MAC efficiency test.” Keep \(1/\gamma\) strictly as a conversion within Test B.

6) **Workload realism via duty factor \(d\) is improved, but still lacks operational grounding and sensitivity to correlation structure**  
**Why it matters:** The main critique of earlier versions (as you anticipate) is whether \(d\) is a realistic workload abstraction. You now provide a mixture calculation and phase mapping, which helps, but the model still assumes a particular ON/OFF structure and cluster-level correlation. The <1% figure depends on these choices.  
**Specific remedy:**  
- Provide a sensitivity table: average \(\bar{\eta}\) and P95/P99 coordinator ingress under (i) Bernoulli per-cycle, (ii) ON/OFF with varying \(L_{\mathrm{on}}\), (iii) heavier-tailed ON durations.  
- Clearly separate “duty factor as time fraction active” from “within-active campaign command probability \(p_{\mathrm{cmd}}\)”—you do this, but reinforce with an example showing two different pairs \((d,p_{\mathrm{cmd}})\) that produce same mean but different burstiness and buffer needs.

7) **Packet-level “validation” of \(\gamma\) is not independent; currently it is a standards-based parameter calculation**  
**Why it matters:** Section IV-J is useful, but it is not validation in the empirical sense. The manuscript mostly acknowledges this, yet some phrasing (“validated via CCSDS”) could be read as stronger than warranted.  
**Specific remedy:**  
- Replace any “validated” wording with “anchored/parameterized from CCSDS nominal framing.”  
- Add a short “implementation uncertainty” subsection quantifying how \(\gamma\) changes with plausible ranges of \(T_{\mathrm{acq}}\), turnaround, and framing choices, and propagate that uncertainty to \(R_{\mathrm{PHY,min}}\) and the 35 kbps recommendation.

---

# Minor Issues

1) **Consistency of \(\gamma\) values and rounding:** Ensure all tables/claims use the same unrounded intermediate computation (you state this in Table IV-J; enforce globally).  
2) **Baseline vs \(\eta\) vs \(\eta_{\text{total}}\):** Consider renaming \(\eta\) to \(\eta_{\text{overhead}}\) in figures/tables to reduce confusion.  
3) **Table IV-D uses Model S only:** This is clearly footnoted, but many readers will still over-interpret it. Consider moving it to an appendix or adding a companion Model C version (even if trivial/infeasible at 24 kbps).  
4) **Cluster coordinator “summary 512 B with 371 B metadata/CRC”:** That breakdown reads ad hoc; justify why metadata is so large or redefine summary size as an assumed fixed packet size.  
5) **Fleet reuse factor \(R=3\) justification:** currently “order of magnitude.” Add a simple link budget / antenna pattern placeholder or cite a representative sidelobe/isolation reference; otherwise keep fleet-level reuse as explicitly speculative.  
6) **AoI P99 discussion:** Good that you attribute 440 s to sampling tail. Consider emphasizing that network feasibility does not improve AoI tail unless \(p_{\mathrm{exc}}\) changes—preempt misinterpretation.  
7) **Algorithm 1 line 3 uses \(\eta_0=5\%\) as constant:** but you later note it varies slightly with \(k_c\). Either compute \(\eta_0(k_c)\) or state “use 5% conservative bound.”  
8) **Terminology:** “validated via CCSDS, replacing earlier 0.85” — avoid “validated.” Use “revised/anchored.”

---

## Overall Recommendation  
**Recommendation:** **Major Revision**

The paper is promising and substantially improved in transparency and engineering usefulness. The duty-factor \(d\) addition and the shift to a CCSDS-grounded \(\gamma(R_{\mathrm{PHY}})\approx 0.70\text{–}0.76\) are meaningful steps, and the stress-case \(\eta_S\approx 46\%\) is now better contextualized as a continuous-duty upper bound rather than a typical operating point. The two-test feasibility framework (byte budget vs TDMA airtime) is a good organizing principle and could become a practical reference.

The main reason for Major Revision is that the headline PHY sizing conclusion (30 kbps minimum / 35 kbps recommended) remains highly sensitive to a few schedule/PHY assumptions (per-slot acquisition, ACK placement, and coherence regime). These assumptions are not wrong, but they must be elevated to first-class design choices with alternate cases computed, and the manuscript must avoid language implying empirical validation where none exists. Strengthening the ARQ/GE treatment to cover both slow- and fast-mixing regimes (or narrowing the claim scope) would also materially improve scientific solidity.

---

## Constructive Suggestions (ordered by impact)

1) **Recast PHY sizing as a small set of explicitly enumerated “implementation modes”** (per-slot acquisition vs per-burst vs tracking; explicit ACK slots vs aggregated ACK), and recompute Table VII/VIII under each.  
2) **Make the superframe timing fully explicit** with a diagram and conservative accounting: guard is guard; ACKs are scheduled airtime. Provide margins under both optimistic and conservative ACK handling.  
3) **Upgrade GE/ARQ analysis to two-timescale loss modeling** (per-slot transitions within a cycle for \(\tau_c\ll T_c\)), and show how ARQ feasibility changes; otherwise narrow ARQ claims to the slow-mixing regime.  
4) **Tighten the “two-test” narrative** with a single pipeline figure and remove any residual implication of a third “MAC efficiency test.”  
5) **Strengthen workload realism evidence for \(d\)** by adding a sensitivity analysis over burst-length distributions and correlation scopes, and show how buffer sizing changes even at fixed mean \(\bar{\eta}\).  
6) **Standardize language around \(\gamma\)**: “standards-anchored estimate,” not “validated,” and quantify uncertainty propagation to \(R_{\mathrm{PHY,min}}\).  
7) **Add a short practitioner checklist** (what to measure on a modem to instantiate Eq. (53): \(T_{\mathrm{acq}}\) distribution, turnaround, framing, achieved \(\gamma\)), and explicitly map those to rate selection via Table IX.

If you address the acquisition/ACK/schedule assumptions transparently and broaden or properly scope the ARQ/GE regime claims, the manuscript would be much closer to publishable quality for a top-tier aerospace systems journal.