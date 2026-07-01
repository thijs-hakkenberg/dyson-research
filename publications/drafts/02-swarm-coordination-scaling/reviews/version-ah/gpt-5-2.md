---
paper: "02-swarm-coordination-scaling"
version: "ah"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-27"
recommendation: "Accept"
---

## 1. Significance & Novelty — **Rating: 4/5 (Good)**

The manuscript tackles a real and timely problem: coordination scaling for very large autonomous spacecraft swarms (10³–10⁵, with discussion toward 10⁶). The paper’s central value is not proposing a new coordination protocol per se, but providing a **quantitative design-space characterization** with explicit byte accounting under a tight per-node control-plane budget (1 kbps) and exploring coordinator ingress constraints, AoI quality trade-offs, and correlated-loss effects. For T-AES readership, the focus on **engineering-relevant sizing rules** (e.g., coordinator ingress 21–50 kbps depending on scheduling) is a meaningful contribution.

The novelty claim is mostly credible in the specific combination of: (i) hierarchical coordination framing for space swarms at these sizes, (ii) cycle-aggregated DES with full participation and byte-level accounting, and (iii) explicit comparison against two intentionally extreme baselines plus a more realistic “sectorized mesh.” The AoI treatment and the GE loss study are not novel in isolation, but their integration into a constellation/swarm coordination sizing narrative is useful.

That said, the paper sometimes overstates “architecture choice vs workload assumptions” as a general conclusion. Under the authors’ own accounting, **commands dominate** the stress case (Fig. “decomposition” and Table \#bw breakdown), so it is unsurprising that workload dominates. This is still a valuable result, but it should be framed as: *given the assumed message classes and command model, workload dominates*. The paper would be stronger if it explicitly delineated which parts are expected/tautological (linear scaling with command probability) versus which are genuinely informative (coordinator ingress burstiness thresholds; independence result conditional on point-to-point links).

---

## 2. Methodological Soundness — **Rating: 3/5 (Adequate)**

The cycle-aggregated DES is appropriate for the stated goal (message-layer sizing and scaling). The manuscript is commendably explicit about what is modeled vs abstracted (Table “Simulation Abstraction Scope”), defines traffic accounting clearly (Table “Traffic Accounting”), and provides parameter tables and code availability with a tag—this supports reproducibility.

However, several modeling choices materially affect headline results and need tighter justification or sensitivity:
- **Coordinator ingress models (Model A/B/TDMA/phase-stagger):** The 50 kbps “deadline/no carry-over” bound vs 21 kbps leaky-bucket recommendation is plausible, but the paper currently mixes *queueing*, *link scheduling*, and *deadline semantics* in a way that can confuse what exactly is capacity-limiting. In particular, it is unclear whether “drops due to coordinator bandwidth saturation” (Table “coord_bw”) are drops at a link shaper, a receiver buffer, or a per-cycle accounting artifact. The token bucket depth choice (one full cycle worth of bytes) effectively assumes cross-cycle buffering equivalent to allowing late reports—this is an architectural assumption that should be tied to control requirements (i.e., what does the coordinator do with stale reports?).
- **Validation:** The paper states validation against M/D/1 mean latency within 2% and gossip bounds for N≤1000. That is helpful, but the most critical results (coordinator ingress thresholds; AoI tails under exception telemetry; GE vs i.i.d. retransmission) are essentially analytically derivable under the paper’s assumptions. The DES adds value mainly for joint interactions and multi-factor sweeps, but those results depend strongly on event ordering and abstraction choices. The “independence” finding (Section IV-D) is correct *given the model*, but the model excludes the most common mechanism that would couple them (shared-medium contention / MAC). Since the paper repeatedly emphasizes a 1 kbps RF-backup regime, the absence of a shared-medium MAC model becomes more consequential.
- **Statistical treatment:** 30 Monte Carlo runs with bootstrap CIs is fine, but the manuscript itself notes near-deterministic outputs (SD < 0.001% for overhead). For metrics like P99 AoI, tails can be sensitive; you do provide an analytic quantile cross-check (Eq. for AoI P99), which is good. For correlated loss and drops, reporting confidence intervals (even if small) would improve rigor and align with IEEE expectations.

Overall, the methodology is serviceable for a message-layer sizing study, but the paper needs clearer separation between (a) what the DES truly discovers versus (b) what follows directly from the deterministic traffic model, and stronger sensitivity/robustness discussion around the abstraction choices that drive the coordinator capacity conclusions.

---

## 3. Validity & Logic — **Rating: 3/5 (Adequate)**

Most conclusions are consistent with the presented results and with the paper’s own caveats. The overhead invariance with N is logically implied by the fixed-depth hierarchy and per-node constant message generation, and the manuscript correctly acknowledges this. The AoI geometric tail result is correctly derived and matches simulation (Eq. AoI P99 vs Table “aoi_results”). The GE retransmission degradation is also correctly explained by conditioning on the bad state.

The main validity risk is that some “engineering” conclusions are drawn from abstractions that omit the dominant real-world coupling mechanisms:
- The coordinator ingress sizing (21–25 kbps “recommended”) is tightly tied to **perfect scheduling or buffering semantics**. In practice, the coordinator’s ability to accept 100 inbound transmissions per 10 s cycle depends on ranging/pointing, half-duplex constraints, and MAC design. The paper acknowledges MAC is abstracted and uses an efficiency factor γ, but the coordinator ingress problem is not just a multiplicative γ penalty; it is also about **collision-free multiplexing** and time/frequency resource allocation. Your TDMA vignette helps, but it uses several assumptions (guard time breakdown, “co-moving cluster,” Doppler negligible, and a mixed RF/optical statement) that should be made more internally consistent and traceable.
- The “realistically provisioned centralized baseline (c=N/kc) does not diverge until N≈10⁶” conclusion (Section IV-F and abstract) is plausible for processing, but it implicitly assumes uplink spectrum and ground contact are solvable. You do state spectrum/latency are binding, but the narrative still risks confusing readers: the baseline is framed as “centralized ground processing,” yet later the key constraints are communications and availability rather than processing. This is not wrong, but the paper should more explicitly define what is being bounded (compute vs comms vs autonomy) and avoid implying a single “divergence” point.
- The “independence” conclusion in IV-D is logically valid but should be stated even more narrowly: it is an artifact of modeling losses as occurring *before* coordinator capacity accounting on independent point-to-point links. In any shared channel (RF backup) or even in optical systems with shared acquisition/scheduling constraints, interaction is likely.

The paper does a good job acknowledging limitations (Section V-B), but some headline statements in the abstract are stronger than what the abstraction supports (especially coordinator capacity and independence claims).

---

## 4. Clarity & Structure — **Rating: 4/5 (Good)**

The manuscript is generally well organized, with clear RQs, explicit baselines, and a helpful “roadmap” at the start of Results. Tables defining traffic accounting, parameters, and abstraction scope are strong and improve interpretability. The paper is also unusually explicit about what is included/excluded in η, which is excellent.

There are, however, several clarity issues that impede comprehension for readers outside your immediate modeling context:
- **Terminology overload and consistency:** “coordination cycle” is used both as a synchronization interval and as a deadline boundary; “reporting rate r” is equated to 1/Tc, but later exception telemetry changes effective reporting without changing Tc. This is fine, but needs crisp wording: Tc is the scheduler period; effective per-node update process changes with p_exc.
- **Coordinator bandwidth pooling vs explicit C_coord:** The text first emphasizes that k_c reports imply ~20.5 kbps inbound, exceeding 1 kbps by 20×, “resolved through TDMA-based bandwidth pooling,” but later says you *do not assume* fully pooled bandwidth and instead parameterize C_coord. This is potentially confusing: is pooling an architectural property, or a design option reflected by choosing β?
- **Figures referenced but not shown here:** The narrative depends on multiple figures (phase stagger, TDMA comparison, decomposition). Ensure captions are self-contained and that axes/units are unambiguous. In particular, any plot of “drops” should specify normalization (drops per year? per run? per coordinator?).

The abstract is dense but mostly accurate; still, it contains several very specific numerical claims (e.g., “P99 AoI 440 s,” “retransmission recovery 27%,” “independently compose without cross-factor correction”) that are correct under assumptions but should be explicitly flagged as **model-conditional** in one short phrase to avoid overgeneralization.

---

## 5. Ethical Compliance — **Rating: 4/5 (Good)**

The manuscript includes an AI-assisted ideation disclosure in the Acknowledgment, which is increasingly expected and is handled transparently. The disclosure states AI tools were used for ideation and that a companion methodology paper exists. No obvious ethical red flags appear in the simulation study itself.

Two improvements would strengthen compliance and perception:
1. Add a brief statement clarifying whether any AI system contributed to text generation, code generation, or data analysis beyond ideation (many venues now want this explicitly).
2. The author list is “Project Dyson Research Team” with deferred individual names/affiliations. IEEE policy typically requires author identities for review/publication (double-check T-AES process). If this is a placeholder for anonymized review, it should be stated explicitly as such; otherwise it may be non-compliant at submission.

Conflict of interest is not discussed; if there are none, a standard “no competing interests” statement is helpful.

---

## 6. Scope & Referencing — **Rating: 4/5 (Good)**

The topic fits IEEE T-AES well: constellation operations, autonomy, coordination architectures, and communications constraints. The paper positions itself at the intersection of distributed algorithms, swarm robotics, and satellite networking, which is appropriate.

Referencing is generally adequate and includes foundational distributed systems (Lynch, Lamport, Raft), gossip (Demers), DTN/BPv7, and relevant constellation/networking works (Handley, del Portillo, Akyildiz). AoI references are current and appropriate.

Concerns/gaps:
- Several operational references are **non-archival web pages** (SpaceX/Kuiper/DARPA program pages). For T-AES, these are acceptable as contextual citations but should not underpin quantitative claims. Where you cite “Starlink operations” or conjunction challenges, consider adding more archival sources (e.g., FCC filings, peer-reviewed/IAA proceedings, or operator technical papers).
- The “physical-layer vignette” cites SMAD for link budget plausibility, but the vignette mixes optical and RF assumptions (aperture vs dBi antenna) and asserts BER/throughput without a concrete link budget table. If you keep this vignette, add at least one archival comms reference more directly connected to LEO ISL link budgets and TDMA framing/guard times beyond CCSDS Proximity-1 (which is not an ISL standard per se).

---

## Major Issues

1. **Coordinator ingress capacity result needs sharper system-model definition and stronger justification.**  
   In Section IV-A (Coordinator Capacity Sizing), the 21–50 kbps “zero-drop” thresholds depend on whether capacity can carry over across cycles (token bucket), whether reports have hard deadlines, and whether TDMA is available. These are *control semantics* and *MAC/scheduling* assumptions, not merely bandwidth. The manuscript should:
   - Define precisely what constitutes a “drop” and where it occurs (link shaper vs receiver buffer vs deadline expiry).
   - State whether late reports (arriving after Tc) are useful or discarded; if discarded, token-bucket carry-over may not be valid for “zero-drop” in a control sense.
   - Provide a sensitivity on token bucket depth σ and/or allowed staleness (e.g., accept reports up to Tc+Δ).

2. **The “independence/compositionality” claim (Section IV-D, abstract) is too strong without modeling the RF-backup/shared-medium regime that motivates 1 kbps/node.**  
   You correctly note independence is conditional on point-to-point ISLs and would not hold under shared-medium contention. However, because the paper’s central constraint is an RF-backup-like 1 kbps budget, readers will naturally question whether shared-medium coupling dominates in the most relevant regime. At minimum, the abstract and conclusion should explicitly say: *independence holds only under per-link losses on dedicated point-to-point links; it is not expected under shared-medium RF*.

3. **Centralized baseline framing is internally inconsistent and risks misleading comparison.**  
   The paper alternates between (i) centralized as an intentional compute bottleneck (c=1), (ii) centralized as realistically provisioned (c=N/kc), and (iii) centralized as limited by spectrum/latency/availability rather than compute. This is all true, but the comparison should be restructured so that:
   - The baseline is clearly decomposed into compute, uplink spectrum, latency, and autonomy constraints.
   - “Does not diverge until N≈10⁶” is explicitly “compute does not diverge,” not “centralized coordination does not diverge.”

4. **Physical-layer TDMA feasibility vignette is not sufficiently rigorous for the strength of claims made.**  
   The vignette asserts 24 kbps is achievable at 500 km with 0.1 W and modest antennas/aperture and cites SMAD. For T-AES, either (a) reduce the claim to a qualitative plausibility statement, or (b) add a compact link budget (frequency, bandwidth, modulation/coding, receiver sensitivity/noise figure, margins) and separate RF vs optical cases.

---

## Minor Issues

- **Equation/parameter consistency:**  
  - Table “Simulation Parameters” lists GE transition probabilities p_GB=0.05/cycle and p_BG=0.20/cycle “steady-state avail. 80%”. For a two-state Markov chain, steady-state good probability is p_BG/(p_BG+p_GB)=0.20/(0.25)=0.8, OK. In Section IV-D you use p_BG=0.50 for an 80% availability sweep; that would yield 0.50/(0.55)=0.909. Please reconcile (either change the numbers or state clearly that IV-D uses a different GE parameter set).
- **Table labeling/typos:**  
  - Table “link_availability” footnotes: you reference superscript b/c inconsistently in the last rows (“80.5^b” but footnote says “^c Total offered including baseline exceeds 100%…”). Clean up superscripts.
- **AoI sampling method:** Table “aoi_results” says AoI sampled every 100 s; clarify whether P99 is over time samples × nodes × coordinators pooled, and whether sampling interval biases tail estimation (it can, depending on AoI process).
- **Sectorized mesh derivation:** The heuristic that a screening volume contains O(√N) nodes is not clearly derived; consider tightening or moving to an appendix. As written, it may invite pushback from orbital dynamics readers.
- **Global-state mesh accounting:** Your convergence rounds formula \(R_{conv}=\max(\lceil\log_2 N\rceil,\lceil N/(bf)\rceil)\) is plausible given batching, but the redundancy factor “~1.4×” is asserted without citation or derivation. Either justify or remove the numeric factor and present a range.
- **Availability numbers:** In the duty-cycle section, you derive ~99.96% availability but Table “duty_cycle” lists 99.5% at 24h with a qualitative explanation. Provide the exact model used to compute the table entries, or present them as illustrative rather than computed.

---

## Overall Recommendation — **Major Revision**

The manuscript is promising and contains several useful engineering insights, but key headline claims (coordinator ingress sizing, compositional independence, centralized baseline interpretation, and TDMA feasibility) require tightening of assumptions, clearer model definitions, and either additional sensitivity analyses or moderated conclusions. With revisions that better align claims to the abstraction level and add rigor around the coordinator bandwidth/scheduling semantics, the paper could be a strong T-AES contribution.

---

## Constructive Suggestions

1. **Make coordinator ingress sizing “control-semantic aware.”**  
   Add a small subsection in IV-A defining (i) deadline semantics (are reports useful after Tc?), (ii) buffer/carry-over policy, and (iii) what “zero-drop” means operationally. Then report capacity requirements as a function of allowed staleness (e.g., accept within Tc, 2Tc, etc.) and token bucket depth σ. This would turn the 21 vs 50 kbps split into a principled trade.

2. **Reframe and qualify the compositionality/independence result.**  
   Move the key condition into the theorem-like statement: *independence holds when loss occurs upstream of the coordinator shaper on independent point-to-point links*. Add a short “counterexample” discussion: under RF shared medium, retransmissions increase contention and can shift the coordinator saturation point. Even without implementing a full MAC, you can include a simple contention model (e.g., slotted ALOHA or CSMA approximation) to show non-independence qualitatively.

3. **Fix the centralized baseline narrative by decomposing constraints.**  
   Replace “centralized does not diverge until N≈10⁶” with “centralized compute does not diverge…” and add a compact table comparing centralized vs hierarchical across: compute scaling, spectrum/uplink scaling, autonomy/ground outage, and latency loop closure. This will prevent readers from misinterpreting the baseline as a strawman.

4. **Strengthen (or soften) the physical-layer vignette.**  
   Either (a) add a one-paragraph link budget with explicit assumptions (carrier frequency, coding rate, required Eb/N0, antenna gains/aperture, pointing loss, receiver noise temp, margin), or (b) downgrade the claim to “order-of-magnitude feasibility” and avoid quoting BER values. Also separate RF and optical cases—currently they are blended.

5. **Reconcile GE parameters and add uncertainty reporting for key tables.**  
   Ensure GE parameters are consistent across Table “sim_params,” Section IV-C, and IV-D. Add 95% CIs (or at least min/max across seeds) for coordinator drops and delivery rates in Tables “coord_bw,” “joint_interaction,” and “link_availability,” even if small—this improves reviewability and aligns with the Monte Carlo framing.