---
paper: "02-swarm-coordination-scaling"
version: "j"
modelId: "claude-opus-4-6"
modelName: "Claude Opus 4.6"
reviewed: "2026-02-23"
recommendation: "Major Revision"
---



# Peer Review: "Characterizing Hierarchical Coordination Scaling for Large Autonomous Space Swarms: A Discrete Event Simulation Study"

**Manuscript Version:** J
**Venue:** IEEE Transactions on Aerospace and Electronic Systems

---

## 1. Significance & Novelty

**Rating: 3 (Adequate)**

The paper addresses a genuine gap in the literature: the systematic characterization of coordination architectures in the $10^3$–$10^5$ node regime, which sits between well-studied swarm robotics scales (~100 agents) and the aspirational scales of mega-constellations (~$10^4$–$10^5$). The motivation is timely given Starlink's expansion trajectory and the emergence of competing constellations. The coordinator bandwidth parameterization (Section IV-G) and the link availability analysis with retransmission (Section IV-F) are practical contributions that provide actionable design guidance.

However, the core finding—that a hierarchical architecture with fixed cluster size and fixed per-node bandwidth yields $O(1)$ overhead ratio—is, as the authors themselves acknowledge (Section IV-D), "a direct mathematical consequence of the hierarchical message structure—not a surprising emergent property." The DES confirms the constant factor ($\eta \approx 21\%$) and the absence of second-order effects, but the intellectual contribution of confirming a straightforward analytical prediction via simulation is modest. The paper would be substantially more novel if it included the sectorized mesh comparator (acknowledged as future work in Section V-C) or if the DES revealed unexpected scaling phenomena. As it stands, the simulation largely confirms what the analytical model predicts, and the most interesting comparisons (hierarchical vs. practical decentralized alternatives) are deferred.

The exception-based telemetry validation, while carefully executed, models a Bernoulli thinning of a Poisson process—a well-understood statistical operation. The multi-scale validation at $N \in \{10^4, 10^5\}$ with errors within 1% of analytical predictions (Table VIII) is reassuring but unsurprising. The remaining two optimizations (dynamic spatial partitioning, heterogeneous hardware) that would provide more novel contributions remain unvalidated.

---

## 2. Methodological Soundness

**Rating: 2 (Needs Improvement)**

**Node sampling scheme.** The most significant methodological concern is the node sampling approach ($r_s = \min(1, 1000/N)$), which means that for $N = 10^5$, only 1% of nodes are actually simulated per coordination cycle. While the sampling validation (Table VII) shows agreement within ~0.9 percentage points at $N \leq 20{,}000$, the validation does not extend to $N = 10^5$—precisely the scale at which the paper's headline results are reported. The claim that "no scale-dependent second-order effects" emerge (abstract, Section IV-D) is undermined by the fact that the simulation does not actually model all $10^5$ nodes interacting simultaneously. Queueing contention, scheduling collisions, and burst effects at the coordinator—the very phenomena the DES is supposed to detect—are attenuated by the 1% sampling rate. The authors should either (a) run full-fidelity simulations at $N = 10^5$ (even if computationally expensive) or (b) provide a rigorous analytical argument for why the sampling preserves second-order effects.

**Monte Carlo sample size.** The use of 2–5 runs per configuration is extremely low for a Monte Carlo study. At 2 runs, bootstrap confidence intervals are essentially meaningless (the BCa method requires $n \geq 5$ for reliable bias correction). The claim of "95% confidence intervals" from 2 runs is statistically unsound. The paper states that "95% bootstrap CIs are within ±5% of reported means" (Table V footnote), but with 2 samples, the CI width is dominated by the prior assumptions of the bootstrap, not the data. A minimum of 30 runs per configuration would be standard for the claims being made.

**Wall-clock runtime.** The reported runtimes (0.2s for $N=10^3$ to 15s for $N=10^5$) are suspiciously fast for a year-long DES with $T_c = 10$s resolution. A year at 10-second resolution requires ${\sim}3.15 \times 10^6$ cycles. Even with 1% sampling at $N = 10^5$, that is $10^3$ nodes $\times$ $3.15 \times 10^6$ cycles $= 3.15 \times 10^9$ events—difficult to process in 15 seconds in Python. This suggests either (a) the simulation is far more abstracted than described, or (b) not all events are actually processed. The authors should clarify the actual event count per run and the degree of abstraction.

**Queueing model mismatch.** The centralized baseline uses an $M/D/1$ model, but the arrival process is not Poisson: all $N$ nodes report at rate $r = 0.1$ msg/s, and with $T_c = 10$s, each node sends exactly one message per cycle. This is a deterministic arrival process (or at best, a superposition of $N$ periodic sources with random phase), not Markovian. The $M/D/1$ formula (Eq. 2) is therefore an approximation whose accuracy depends on the phase randomization assumption. This should be acknowledged.

**Collision avoidance rate.** The $10^{-4}$/node/s rate is justified by a "1,000:1 ratio of screening events to actual maneuvers," but this ratio is not sourced. The ESA reference [esa_space_env] reports maneuver rates, not screening event rates. The sensitivity analysis (varying from $10^{-5}$ to $10^{-3}$) partially mitigates this concern, but the baseline parameterization should be better justified.

---

## 3. Validity & Logic

**Rating: 3 (Adequate)**

The paper is generally careful about distinguishing DES-measured results from analytical predictions, and the "Baseline Interpretation Note" (Section I-C) is a commendable addition that prevents misinterpretation of the reference baselines. The traffic accounting (Table IV) and metric definitions (Section III-F) are thorough and support reproducibility.

However, several logical issues weaken the conclusions:

**Circular reasoning in the core result.** The overhead metric $\eta$ is defined as total coordination bytes divided by $N \times C_{\text{node}}$. For the hierarchical topology, total bytes $\propto N$ (by construction of the message model), and the denominator is $N \times C_{\text{node}}$. The ratio is therefore $O(1)$ by definition. The DES "confirms" this by generating messages according to the same model. The paper acknowledges this (Section IV-D, first paragraph) but then claims the DES contribution is confirming "no scale-dependent second-order effects." Given the 1% sampling rate at large $N$, the DES's ability to detect such effects is questionable (see Methodological Soundness above).

**Table V vs. Table VI inconsistency.** The paper notes that Tables V and VI "are not directly comparable because different cluster sizes yield different overhead at the same fleet size" (Section III-E). However, the text frequently discusses both tables in the same context without clearly flagging which parameterization applies. For example, Table V reports $\eta = 2.9\%$ at $N = 10^5$ with optimized $k_c = 100$, while Table VI reports $\eta = 21.5\%$ at $N = 10^5$ with fixed $k_c = 100$. The factor-of-7 difference is confusing and suggests that the overhead metric may be computed differently in the two tables (one possibly excluding baseline telemetry, the other including it, or one using the optimized cluster size sweep from Table V). This discrepancy needs explicit reconciliation.

**Coordinator bandwidth analysis.** The finding that $C_{\text{coord}} \geq 25$ kbps is required (Table IX) is presented as a novel parameterization, but it follows directly from the arithmetic: $100 \times 256 \times 8 / 10 = 20.48$ kbps, plus margin. The DES adds the observation that 5 kbps of margin suffices for burst effects, which is useful but minor.

**Link availability model.** The Bernoulli i.i.d. link model is acknowledged as a simplification, but the results (Table VIII) are presented with precision that may overstate confidence. In LEO, link outages are strongly correlated (Earth occlusion affects all links in a geometric shadow simultaneously), and the i.i.d. assumption significantly understates the impact of link loss on coordination success. The retransmission analysis is valuable but should be qualified more strongly.

---

## 4. Clarity & Structure

**Rating: 4 (Good)**

The paper is well-organized and clearly written. The four-level structure (Introduction → Framework → Results → Discussion) is logical, and the progressive disclosure of results (topology comparison → optimization → scaling → validation → sensitivity) builds understanding effectively. The explicit traffic accounting table (Table IV) and metric definitions (Section III-F) are exemplary and should be standard practice in simulation studies.

The abstract is comprehensive but long (over 250 words); it could be tightened by removing the specific numerical values for $\beta_{\min}$ and $p_{\text{link}}$ thresholds, which are better suited to the conclusion. The "Baseline Interpretation Note" (Section I-C) is well-placed and prevents a common misreading.

Figures are referenced appropriately but cannot be evaluated since they are external PDF files. The figure captions are descriptive and self-contained, which is good practice. Table formatting is consistent and readable, though Table III (Simulation Parameters) is dense and would benefit from grouping parameters by subsystem (communication, processing, failure, Monte Carlo) with visual separators—which the authors have partially done with italic subheadings.

One structural issue: the paper is very long for a journal article (approximately 12,000 words of body text plus tables). Some material could be moved to supplementary material, particularly the sampling validation (Section IV-D-1, Table VII), which is methodological housekeeping rather than a primary result.

---

## 5. Ethical Compliance

**Rating: 4 (Good)**

The Acknowledgment section transparently discloses the use of AI-assisted ideation (Claude 4.6, Gemini 3 Pro, GPT-5.2) and clearly states that the AI-generated concepts are "not validated in the current study." This is an appropriate level of disclosure. The data availability statement provides a repository URL (though the commit hash is marked as pending, which should be resolved before publication).

The author attribution is unusual ("Project Dyson Research Team" with a footnote promising individual names for final publication). While this is acceptable for review, IEEE policy requires named authors with specific contribution statements. The footnote should be resolved.

One minor concern: the references to future AI model versions (Claude 4.6, GPT-5.2) in the Acknowledgment suggest the paper may be set in a near-future timeframe, which is unusual for a technical manuscript. If these are actual tools used, the version numbers should be verified; if they are speculative, this should be noted.

---

## 6. Scope & Referencing

**Rating: 3 (Adequate)**

The paper is appropriate for IEEE T-AES in scope, addressing autonomous spacecraft coordination with quantitative simulation results. The reference list (48 items) is comprehensive and covers the relevant literature in constellation management, swarm robotics, distributed systems, and queueing theory.

However, several important references are missing or inadequately cited:

- **No references to actual ISL performance data** from Starlink or other constellations. The 1–10 Gbps optical ISL assumption is stated without citation.
- **No references to TDMA scheduling** literature to support the claim that coordinator bandwidth is "a scheduling problem, not a hardware scaling problem" (Section IV-G).
- **No references to space network simulation tools** (e.g., STK, GMAT, ns-3 with satellite extensions) that could validate or contextualize the custom DES.
- The **Olfati-Saber and Murray [olfati_consensus]** and **Ren and Beard [ren_beard]** references are mentioned in Related Work but their relevance to the hierarchical architecture is not developed.
- Several references are non-archival (SpaceX website, Amazon website, DARPA program pages, DOD fact sheets). While understandable for operational systems, the paper relies on these for key claims about current constellation sizes and operational practices. At least 6 of 48 references are non-archival.

The paper does not cite recent work on **distributed space systems simulation** (e.g., Nag et al., "Autonomous spacecraft operations," IEEE Aerospace Conference, 2020s) or **LEO constellation coordination protocols** that have appeared since 2020.

---

## Major Issues

1. **Node sampling undermines the core claim.** The headline result—"no scale-dependent second-order effects"—is tested using a simulation that samples only 1% of nodes at $N = 10^5$. This sampling rate suppresses precisely the phenomena (queueing contention, scheduling collisions, burst effects) that the DES is supposed to detect. The sampling validation (Table VII) only extends to $N = 20{,}000$. Either full-fidelity runs at $N = 10^5$ or a rigorous proof that sampling preserves second-order effects is required.

2. **Insufficient Monte Carlo replication.** Two runs per configuration is inadequate for statistical claims. The bootstrap CIs reported are unreliable at $n = 2$. Minimum 30 runs per configuration, or a justification based on the low variance of the deterministic message model (which would itself undermine the need for Monte Carlo).

3. **Table V / Table VI overhead discrepancy.** The factor-of-7 difference in reported overhead ($2.9\%$ vs. $21.5\%$ at $N = 10^5$, both with $k_c = 100$) is not adequately explained. The footnote stating the tables are "not directly comparable" is insufficient—the reader needs to understand what differs in the overhead computation.

4. **Circularity of the core result.** The $O(1)$ overhead ratio is a mathematical identity given the message model and the overhead definition. The DES confirms this identity but does not test it against alternative outcomes, because the simulation generates messages according to the same model. The contribution should be reframed more modestly: the DES quantifies the constant factor and validates the implementation, but does not "discover" the scaling property.

5. **Absence of a realistic decentralized comparator.** The global-state mesh is acknowledged as an intentional upper bound, and the sectorized mesh is identified as future work. Without a realistic decentralized comparator, the paper cannot support claims about the relative merit of hierarchical coordination—only about its absolute overhead level. This significantly limits the paper's contribution to architecture selection.

---

## Minor Issues

1. **Eq. (2):** The $M/D/1$ waiting time formula $W_q = \rho / [2\mu(1-\rho)]$ is correct for the P-K formula applied to deterministic service, but the notation is slightly non-standard. Typically written as $W_q = \rho^2 / [2\lambda(1-\rho)]$ or equivalently $\rho / [2\mu(1-\rho)]$. Clarify that this is the waiting time (excluding service).

2. **Section III-B-3:** The claim that "convergence to full state dissemination requires $O(\log N)$ rounds" for gossip with constant fanout is correct, but the subsequent jump to $O(N^2)$ total information flow conflates message complexity with information complexity. The $O(N^2)$ bound is on total *information* (each of $N$ nodes needs $N$ entries), not on messages. This distinction should be clearer.

3. **Table II (State Completeness):** The hierarchical entry states "aggregated summaries for $O(N)$ fleet," but the aggregation reduces information content. The node does not have $O(N)$ state—it has $O(1)$ fleet summaries. This should be clarified.

4. **Section IV-C (Duty Cycle):** The claim that "cumulative probability of at least one handoff failure per day reaches 5% under our reliability model" at 1-hour duty cycles should include the calculation: $1 - 0.95^{24} \approx 0.708$, not 5%. If the per-handoff success rate is 95% and there are 24 handoffs/day, the daily failure probability is ~71%. Please verify.

5. **Eq. (6):** $\Delta P_{\text{avg}} = \Delta P_{\text{coord}} / k_c = 15\text{W} / 100 = 0.15\text{W}$. This assumes uniform rotation, which requires that the duty cycle $\tau_d$ equals $k_c \times \tau_d / k_c$—i.e., each node serves exactly once per rotation. This is only true if $\tau_d$ is chosen to complete a full rotation. The general formula should be $\Delta P_{\text{avg}} = \Delta P_{\text{coord}} \times (\tau_d / (k_c \times \tau_d)) = \Delta P_{\text{coord}} / k_c$, which is correct but should be stated explicitly.

6. **Section III-A:** "Wall-clock runtime ranges from approximately 0.2 seconds for $N = 10^3$ to approximately 15 seconds for $N = 10^5$ per run." This is surprisingly fast and should be accompanied by the total event count per run to allow the reader to assess simulation fidelity.

7. **Abstract:** At 280+ words, the abstract exceeds the typical IEEE T-AES guideline of ~250 words. Consider condensing.

8. **References:** [starlink_ops] is cited as "2024 (non-archival; accessed February 2026)"—the access date is in the future relative to the citation date. This temporal inconsistency should be resolved.

9. **Section V-B:** The comparison with cellular networks, BGP, and ATC is interesting but superficial. The claim that "none of these systems manages $10^6$ fully autonomous nodes" is true but the comparison would benefit from a table showing the key architectural differences.

10. **Notation:** $O_{\text{protocol}}$ is used in Table I but $\eta$ is used elsewhere for the same quantity. Unify notation.

---

## Overall Recommendation

**Major Revision**

The paper addresses a relevant problem and is well-written with commendable transparency about assumptions and limitations. However, the methodological concerns—particularly the 1% node sampling at the headline scale, the insufficient Monte Carlo replication, and the unexplained overhead discrepancy between Tables V and VI—undermine confidence in the quantitative results. The core finding ($O(1)$ overhead ratio) is mathematically expected and the DES confirmation, while useful, is weakened by the sampling scheme. The absence of a realistic decentralized comparator limits the architectural insights. A major revision addressing the sampling validation at full scale, increasing Monte Carlo replication, reconciling the table discrepancy, and reframing the contribution more modestly would substantially strengthen the paper.

---

## Constructive Suggestions

1. **Run full-fidelity simulations at $N = 10^5$.** Even if this requires reimplementation in a compiled language (C++, Rust) or use of an established DES framework (e.g., OMNeT++), full-fidelity results at the headline scale are essential to support the "no second-order effects" claim. Alternatively, provide a formal proof that the sampling scheme preserves queueing dynamics.

2. **Implement the sectorized mesh comparator.** This is identified as future work but is critical for the paper's contribution. A sectorized mesh with $O(\sqrt{N})$ neighborhood size would provide a realistic decentralized baseline and allow meaningful architectural comparison. Even an analytical treatment with DES validation at one scale would significantly strengthen the paper.

3. **Reconcile Tables V and VI explicitly.** Add a paragraph or footnote explaining exactly why $\eta = 2.9\%$ (Table V) and $\eta = 21.5\%$ (Table VI) at the same $N = 10^5$ and $k_c = 100$. If the difference is due to different overhead definitions (e.g., one includes baseline telemetry, the other excludes it), make this explicit in both table captions.

4. **Increase Monte Carlo replication to $\geq 30$ runs** for the key configurations (at minimum, the 10 fleet sizes in Table VI). If the variance is truly as low as claimed ($<0.5\%$ standard deviation), 30 runs will confirm this quickly and the CIs will be credible. If computational cost is a concern, this further motivates reimplementation in a faster language.

5. **Reframe the contribution around the constant-factor quantification and the practical design guidelines** (coordinator bandwidth, link availability thresholds, duty cycle optimization) rather than the $O(1)$ scaling property, which is analytically trivial. The paper's strongest contributions are the parameterized design space exploration and the concrete hardware requirements—emphasize these.