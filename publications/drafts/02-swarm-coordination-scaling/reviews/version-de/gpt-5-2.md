---
paper: "02-swarm-coordination-scaling"
version: "de"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-03-05"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript targets an important and under-served niche: *closed-form, per-cluster sizing equations* for hierarchical coordination in very large space swarms under tight per-node bit budgets, with an explicit bridge from message-layer accounting to TDMA airtime feasibility. The two-test framing (byte budget + schedulability) and the explicit “rate ladder” are genuinely useful for early-phase architecture trades, and the paper is unusually explicit about what is and is not validated.  

Novelty is strongest in (i) the explicit decomposition into Test A/Test B with a practitioner-facing sizing algorithm, and (ii) the standards-anchored, rate-dependent \(\gamma(R_{\text{PHY}})\) expression tied to Proximity-1 framing assumptions. The work is less novel in the underlying ingredients (TDMA airtime checks, GE channels, AoI tails under Bernoulli sampling), but the *integration* and the *design-equation packaging* are valuable.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The analytical accounting is mostly coherent and the simulation stack is well-described (cycle-aggregated DES + slot-level simulator + packet-level \(\gamma\) derivation). The manuscript appropriately positions DES as Tier-1 verification and emphasizes the lack of Tier-3 validation.  

However, there are methodological weaknesses that limit confidence in quantitative recommendations: (i) the TDMA schedulability analysis relies on deterministic slot assignment and fixed per-slot acquisition overhead that is not independently measured; (ii) the GE model is explicitly “what-if,” but some conclusions (e.g., ARQ infeasibility at 30 kbps) are sensitive to the coherence assumption and how retransmissions are provisioned; (iii) the reuse/interference argument is too thin for a journal-grade feasibility claim; and (iv) several “binding” conclusions depend critically on the assumed message sizes and cycle period, with limited justification beyond plausibility.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Internal logic is generally consistent, and Version DE improves clarity around:  
- the campaign duty factor \(d\) as workload realism control,  
- the stress-case \(\eta_S \approx 46\%\) being a continuous-duty bound, and  
- \(\gamma\) being a parameter inside Test B rather than a separate feasibility layer.  

That said, there are still points where the logic risks over-claiming: the “three-layer feasibility framework” is described as two tests (A/B) plus a “unit conversion within Test B,” but the narrative sometimes treats these as separable gates. Also, the “packet-level validation” is not independent validation; it is a standards-based parameter estimate feeding the same equations. This is acknowledged, but some recommendation language remains stronger than the evidence tier supports.

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
The paper is dense but unusually explicit about definitions, tiered V&V, and boundary conditions. The notation table and the boxed feasibility framework help. The “rate ladder” and superframe budget table are strong. The explicit warning that Model S is not used for recommendations is good and addresses a common reviewer concern.  

Remaining clarity issues: some key quantities (\(\eta_0\), “baseline 20.5%,” what exactly is counted as ingress vs egress) appear in multiple places and can still be misread. Also, the relationship between \(C_{\text{node}}\) (logical allocation) and the 35 kbps physical channel could be explained more crisply with a single canonical diagram.

---

## 5. Ethical Compliance  
**Rating: 4 (Good)**  
Reproducibility is strong for a modeling paper: code and configuration are provided with a tag; parameters are tabulated; and limitations/validation gaps are explicitly stated. AI disclosure is present and reasonably specific (ideation + prose editing only).  

One missing piece for top-tier reproducibility: the repo tag is given, but the paper should specify (i) exact commit hash, (ii) which scripts regenerate which figures/tables, and (iii) expected runtime per figure/table (or a Makefile-like pipeline).

---

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
The citations cover distributed algorithms, AoI, GE channels, CCSDS, and some constellation context. For IEEE TAES / space comms audiences, the referencing is *serviceable* but not yet “journal-complete” on MAC/TDMA and space link practice. In particular, the work would benefit from deeper engagement with:  
- CCSDS cross-support / return-link scheduling analogs,  
- classic demand-assigned TDMA and satellite MAC literature beyond DVB-RCS2,  
- space proximity link implementations and measured acquisition/turnaround behaviors,  
- inter-satellite interference/reuse analyses (multi-interferer C/I, antenna patterns).

---

# Major Issues

1) **The “three-layer feasibility framework” is not consistently presented as two tests with one embedded conversion; risk of conceptual confusion**  
- **Why it matters:** Practitioners may incorrectly apply “byte budget,” “MAC efficiency,” and “TDMA airtime” as three independent gates, double-counting \(\gamma\) or mixing the heuristic with explicit slot accounting. This undermines the main contribution (a clean sizing procedure).  
- **Remedy:** In the Discussion/Design Equations section, add a single figure showing:  
  \[
  \text{Information bytes (Test A)} \rightarrow \text{slot time via } \gamma(R_{\text{PHY}}) \rightarrow \text{superframe schedulability (Test B)}
  \]
  and explicitly label “\(C_{\text{raw}}=C_{\text{info}}/\gamma\)” as *a mapping*, not a test. Then audit the manuscript for any language implying a third feasibility test and standardize terminology (“Test A, Test B, mapping”).

2) **Campaign duty factor \(d\) improves realism, but the workload model is still under-specified for “<1% of time” claims**  
- **Why it matters:** The headline result that \(\eta_S \approx 46\%\) occurs <1% of time depends on the assumed mixture (0.95/0.049/0.001) and implicitly on burst length distributions and correlation scope. Without a defensible mapping from mission operations to \(d\) and \(p_{\text{cmd}}\), the realism argument remains fragile.  
- **Remedy:** Provide an explicit operational workload model (even if stylized) that generates the stated mixture: define distributions for campaign start times, durations \(L_{\text{on}}\), and command probabilities within campaigns; then show sensitivity of yearly-average \(\bar{\eta}\) and P95/P99 buffer occupancy to (i) \(L_{\text{on}}\), (ii) correlation scope, and (iii) higher-than-expected CA/update tempos. A compact tornado plot or 2–3 scenario table would suffice.

3) **\(\gamma\) “unification” to 0.76 (and rate-dependent values) is improved, but consistency checks are still needed across all derived numbers**  
- **Why it matters:** The paper’s central quantitative recommendation (30 kbps min, 35 kbps recommended) is highly sensitive to \(\gamma\), and past versions apparently used different values. Any residual inconsistency will be fatal in review because it suggests arithmetic drift.  
- **Remedy:** Add a “parameter ledger” table listing the exact \(\gamma_{24},\gamma_{30},\gamma_{35}\) used in *every* table/figure that depends on them, and a one-line derivation reference (Eq. (35) + parameter set). Then run a manuscript-wide audit: every time a numeric result uses \(\gamma\), show the exact \(\gamma(R_{\text{PHY}})\) value used (or cite the ledger). Also ensure the abstract’s \(\gamma \approx 0.70\text{–}0.76\) aligns with Table I and Table XIV.

4) **Stress-case contextualization is improved, but the paper still risks implying feasibility under continuous-duty operations without fully addressing egress contention and unicast staggering operationally**  
- **Why it matters:** A reader may interpret “Full-load (bcast) single-cycle feasible” as “continuous high-rate coordination is fine,” but in real operations high command loads often include targeted/unicast actions (updates, individualized maneuvers), which trigger 19-cycle staggering and change control-loop semantics.  
- **Remedy:** Strengthen the operational interpretation: explicitly distinguish *control-plane viability* (broadcast safety commands) from *fleet management throughput* (unicast-heavy actions). Add a short subsection: “What degrades first under sustained high duty?” including: (i) command completion time distribution under varying \(q\), (ii) AoI impact if unicast consumes egress, and (iii) any coupling to safety requirements.

5) **DES “verification value” remains limited; distributional tail is useful but currently too conditional to support general buffer-sizing guidance**  
- **Why it matters:** The DES is positioned as contributing mainly tails/buffers, yet the buffer multipliers (1.30×, 1.50×) are explicitly conditional on one ON/OFF model. Without clearer generalization or bounding, the DES adds limited publishable value beyond confirming means.  
- **Remedy:** Either (A) elevate the DES contribution by adding a small family of burst models (geometric ON, heavy-tailed ON such as Pareto/lognormal, and correlated cluster events) and report how buffer multipliers change; or (B) narrow the claims: present the DES tail result as an illustrative case study only, and remove/soften any implication of general buffer sizing guidance.

6) **Packet-level \(\gamma\) derivation is not independent validation; currently it is framed partly as “validation” and may overstate confidence**  
- **Why it matters:** Using CCSDS framing to compute \(\gamma\) is a *parameter estimate*, not validation of the TDMA schedule feasibility in an ISL environment (acquisition success rates, Doppler tracking, implementation-specific overhead). Reviewers will penalize any “validated via CCSDS” phrasing if it suggests empirical confirmation.  
- **Remedy:** Replace “validated via CCSDS” language everywhere with “standards-anchored parameterization” (you already do this in places; make it universal). Add a short paragraph stating explicitly: “CCSDS constrains framing bits and typical procedures, but does not validate acquisition time distributions, turnaround latency, or achieved throughput under Doppler/pointing dynamics.”

7) **Fleet-level reuse/interference analysis is too preliminary for the implied conclusions**  
- **Why it matters:** The per-cluster sizing may be correct, but fleet feasibility hinges on reuse \(R\), antenna patterns, and aggregate interference. The text itself shows \(R=3\) becomes marginal/insufficient with 6 interferers. This is a major gap relative to TAES expectations when making fleet-scale statements.  
- **Remedy:** Tighten scope: explicitly label fleet reuse as *illustrative* and remove any “non-binding at \(f_{\text{RF}}\le 1.2\%\)” style conclusions unless backed by a multi-interferer model. Alternatively, include a simple stochastic geometry / hex-grid aggregate interference model with antenna sidelobe assumptions and show \(R\) required vs sidelobe level and cluster density.

8) **ARQ×TDMA coupling result is interesting but currently demonstrated under Model S in the key table; needs a Model C counterpart to support decision relevance**  
- **Why it matters:** Table XIII is explicitly “Model S only (NOT for design).” That makes the main “emergent” slot-level result less compelling. Readers need the coupling quantified under the actual recommended timing model (Model C), even if the conclusion is “24 kbps infeasible regardless.”  
- **Remedy:** Add a Model C version of the coupling sweep (even if only for 30/35 kbps) showing miss probability vs \(M_r\) and GE parameters under cold-start acquisition. The key question: at 30 kbps Model C, what is the miss rate for \(M_r=1\) under the stated GE demand and reserved window? At 35 kbps, what is the margin distribution?

9) **Generalized \(\gamma\) expression is useful, but practitioners need a clearer “how to measure/instantiate” recipe and error propagation**  
- **Why it matters:** Eq. (35) is central. Without a crisp measurement protocol and uncertainty propagation, it risks being seen as algebraic restatement rather than actionable engineering.  
- **Remedy:** Promote the “Measurement protocol for \(\gamma\)” (currently in Validation Roadmap) into the Design Equations section, and add a compact uncertainty propagation example: given measured \(T_{\text{acq}}\) P95 and \(T_{\text{turn}}\) P95, compute \(\gamma\) CI and resulting \(R_{\text{PHY,min}}\) CI.

---

# Minor Issues

1) **Abstract wording:** “CCSDS Proximity-1 framing anchors \(\gamma\approx0.70\text{–}0.76\)”—the lower end (0.70) appears to come from higher rates (e.g., 50 kbps) or uncertainty; clarify with one phrase (“over 24–50 kbps under cold-start acquisition”).  
2) **Notation table:** \(\alpha_{\text{RX}}\) described as “computed output … example 0.908 at 30 kbps, \(M_r=0\)”—good; ensure it is never later treated as tunable.  
3) **Baseline 20.5%:** You exclude it from \(\eta\) but include it in \(\eta_{\text{total}}\). This is fine, but some tables mix \(\eta\) and \(\eta_{\text{total}}\); consider consistently reporting both or always labeling which is used in feasibility.  
4) **Coordinator summary size justification:** The breakdown sums to 512 B but leaves “metadata/CRC 371 B” unusually large; consider explaining why this overhead is so high (or revise).  
5) **GE coherence assumption:** You correctly state ARQ ineffectiveness is structural when \(\tau_c \ge T_c\). Consider adding a short note that reserving fixed retransmission slots is a worst-case provisioning choice; adaptive ARQ could change schedulability.  
6) **Figure references:** Ensure all figures are included and compile (e.g., `fig-cross-cycle-recovery` missing extension).  
7) **Link budget table:** “System noise temp (290K + 50K) = -173.7 dBm/Hz” is actually \(N_0\) in dBm/Hz; label as noise spectral density to avoid confusion.  
8) **C/I calculation:** The patch pattern assumption (“-10 dBi at 60° off-axis”) should be cited or clearly flagged as an assumption.  
9) **Queueing claims:** “P99 buffer is 20–30% above deterministic” is plausible but unsupported; either cite a derivation or label as observed in DES under a specific model.  
10) **Reference hygiene:** Several “non-archival accessed Feb 2026” references are acceptable for context but should not support technical claims.

---

## Overall Recommendation  
**Recommendation:** **Major Revision**

The manuscript is promising and closer to publishable than many early-phase sizing papers: it is explicit about assumptions, provides reproducible code, and offers a coherent practitioner-facing sizing workflow. The improved handling of the campaign duty factor \(d\), the consistent positioning of \(\eta_S\approx46\%\) as a continuous-duty bound, and the move to standards-anchored \(\gamma\) values (0.761/0.745/0.732) materially strengthen the work.

The main remaining obstacles are (i) evidence-tier alignment (avoid any implication that CCSDS “validates” \(\gamma\) or that DES adds more than conditional tail insight), (ii) decision-relevant slot-level results under Model C (not just Model S), (iii) a more defensible workload realism story behind “<1% of time,” and (iv) tightening or clearly scoping fleet-level reuse/interference statements. Addressing these would convert the paper from a well-written internal design memo into a journal-grade contribution.

---

## Constructive Suggestions (ordered by impact)

1) **Add Model C slot-sim results for ARQ×TDMA coupling** (miss rates/margins at 30 vs 35 kbps across \(M_r\) and at least two GE settings).  
2) **Formalize the workload model behind \(d\)**: define the stochastic campaign process, show sensitivity of \(\bar{\eta}\) and buffer tail multipliers to burst-length and correlation scope, and justify the “<1% stress” statement.  
3) **Create a single canonical feasibility diagram and terminology audit** to eliminate any residual “three-layer test” confusion and prevent double-counting \(\gamma\).  
4) **Strengthen the practitioner instantiation of Eq. (35)**: move the \(\gamma\) measurement protocol + uncertainty propagation into the Design Equations section; provide a worked numeric example.  
5) **Tighten fleet-level reuse claims**: either scope them as illustrative or add an aggregate-interference model sufficient to support a recommended reuse factor range.  
6) **Audit all \(\gamma\)-dependent numbers for consistency** and add a ledger table mapping each table/figure to the exact \(\gamma(R_{\text{PHY}})\) used.  
7) **Clarify operational implications of unicast staggering** under high duty: what mission functions tolerate 190 s, and what functions must remain broadcast/optical.

If these revisions are made, the paper would have a strong chance of meeting the bar for TAES/ASR as a reproducible, clearly-scoped sizing methodology with defensible quantitative recommendations.