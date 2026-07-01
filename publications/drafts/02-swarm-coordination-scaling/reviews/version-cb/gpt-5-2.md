---
paper: "02-swarm-coordination-scaling"
version: "cb"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-28"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript targets a real gap: “back-of-the-envelope but defensible” sizing equations for hierarchical coordination at \(10^3\)–\(10^5\) spacecraft with byte-level accounting and explicit feasibility boundaries. The three-layer feasibility framing (byte budget, MAC efficiency, TDMA airtime) is a useful conceptual contribution, and the explicit separation \(\eta_0\) vs. \(\eta_{\text{cmd}}\) plus a duty-factor \(d\) is practitioner-oriented. The standards-grounded \(\gamma\) derivation is a meaningful improvement over prior “assumed efficiency” approaches.

Novelty is strongest as an engineering synthesis (closed-form sizing + verification ladder + design curves), less as a new algorithm or new theory. For T-AES, the contribution is likely acceptable if the validation story is tightened and assumptions are scoped more rigorously.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The analytical accounting is straightforward and mostly correct; the Monte Carlo DES is fast and appropriate for parametric sweeps; and the slot-level TDMA simulator adds real value for schedulability and ARQ/GE coupling. However, there is an internal-method mismatch: the DES uses a fluid-server ingress abstraction while the paper’s key feasibility claim at 1 kbps hinges on strict TDMA superframe timing. The paper handles this by moving schedulability to an analytical/slot-sim layer, but then some DES-derived metrics (e.g., “drops vs. capacity”) risk being over-interpreted unless clearly marked as *not enforcing TDMA*.

The GE model is reasonable for burst losses, but the mapping from physical phenomena to the assumed coherence-time (per-cycle) remains only qualitatively justified; that’s acceptable if presented as conservative bounding, but the paper sometimes reads as predictive.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
The logic is generally coherent, and Version CB clearly improved several earlier weak spots: (i) the campaign duty factor \(d\) now directly addresses workload realism; (ii) \(\gamma=0.76\) is derived from CCSDS framing and is used consistently in most places; (iii) the stress case \(\eta_S\approx 46\%\) is more explicitly framed as a continuous-duty upper bound.

Remaining validity concerns are mainly about (a) a few numerical inconsistencies/ambiguities in the \(\gamma\) and timing calculations, (b) the meaning of “baseline telemetry excluded from \(\eta\)” while later tables mix “per-node per-cycle messages include status + heartbeat,” and (c) the degree to which the “DES verification” is presented as validation rather than implementation consistency.

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
The paper is unusually explicit about assumptions, layers, and what is/waswo isn’t modeled. Tables (duty factor, schedulability, \(\gamma\) decomposition, superframe budget) are helpful and mostly well aligned with practitioner needs. The verification taxonomy and claim map are a good addition and improve transparency.

Clarity issues: the paper sometimes interleaves “message-layer” and “PHY/MAC airtime” quantities without always flagging the conversion; and a few key definitions (e.g., what exactly is included in \(\eta_0\) vs baseline; whether heartbeats are “protocol overhead” but status is “baseline telemetry”) need one canonical statement early and strict adherence thereafter.

---

## 5. Ethical Compliance  
**Rating: 4 (Good)**  
Open-source code and a tagged release are provided, with environment specs—good reproducibility posture. The AI-assisted ideation disclosure is explicit and appropriate. No human subjects or sensitive data.

One improvement: include a minimal “reproduction recipe” (exact command line / config file names) and archive the tagged release via Zenodo (or similar) to provide a DOI, which many top-tier journals increasingly prefer.

---

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
The references cover distributed algorithms, AoI, GE/Lutz, CCSDS, and constellation context. For a T-AES/space comms audience, the literature on TDMA for space/LEO ISLs and proximity/formation-flying comms could be strengthened (e.g., spaceborne TDMA implementations, scheduled MAC in LEO, practical half-duplex constraints, and relevant CCSDS recommended practices beyond Prox-1). The “sectorized mesh” comparator is clearly labeled as functionally different, which is good, but then its role in the narrative should be reduced to avoid confusion about architectural competition.

---

# Major Issues

1) **The DES “verification” currently risks being circular and over-credited**  
- **Why it matters:** The manuscript repeatedly notes that DES matches closed-form “as expected by construction,” but still uses DES outputs to support claims. Reviewers/readers will discount this unless the DES is shown to test something *not already embedded* in the equations (e.g., queueing transients with bursty \(d\), buffer overflow under stochastic arrivals, or multi-factor interactions not in the closed form).  
- **Remedy:**  
  - Reframe DES matching as *implementation consistency only* (one paragraph, then move on).  
  - Promote the *distributional* results (bimodality under \(d<1\), buffer sizing quantiles, sensitivity to buffer depth) as the primary DES value.  
  - Add at least one DES experiment that is not trivially implied by the equations, e.g.: finite coordinator buffer sizing vs. loss bursts and duty-factor bursts with explicit overflow probability targets, or non-synchronized cluster phases producing correlated regional bursts.

2) **The three-layer feasibility framework is good but not yet mathematically “closed” (Layer boundaries and criteria are partly ad hoc)**  
- **Why it matters:** Practitioners need a crisp decision procedure: given \((k_c,T_c,S,\gamma,R_{\text{PHY}},\alpha_{\text{RX}})\), determine feasibility and required rate. Currently, “TDMA required when \(\eta_{\text{total}}/\gamma>50\%\)” and some other thresholds are heuristic and not consistently derived from the airtime equations.  
- **Remedy:** Provide a single “Feasibility Algorithm” (even as pseudocode) that:  
  1. computes message-layer offered load;  
  2. computes required PHY rate given \(\gamma\);  
  3. checks superframe airtime with ingress/egress partitioning;  
  4. outputs required \(R_{\text{PHY}}\) and whether unicast staggering is needed.  
  Also, explicitly define the 50% criterion (half-duplex split? required egress reserve?) and tie it to Eqs. (29)–(30) (\(\alpha_{\text{RX}}\), \(T_{\text{cmd}}\), etc.).

3) **\(\gamma\) unification to 0.76 is a strong improvement, but there are internal inconsistencies in how \(\gamma\) and “slot time” are used**  
- **Why it matters:** A central claim is “24 kbps infeasible; 30 kbps minimum viable” based on \(\gamma=0.76\). Any ambiguity in the \(\gamma\) definition (payload-only vs. payload+header; inclusion of acquisition; dependence on PHY rate) undermines that boundary.  
- **Specific concerns:**  
  - Eq. (13) computes \(\gamma=0.949\) using “data portion” 2112 bits (payload+overheads) over slot time 92.7 ms, then later \(\gamma\) is defined as \(T_{\text{data}}/T_{\text{slot}}\). That “data” is not payload-only.  
  - Eq. (63) (\(\gamma\) general) mixes bits and a term \((T_{\text{guard}}+T_{\text{acq}})\times R_{\text{PHY}}/1000\). Dimensional correctness depends on \(R_{\text{PHY}}\) units (bps vs kbps) and the 1000 factor; as written, it is easy to misapply.  
- **Remedy:**  
  - Define \(\gamma\) once, precisely: “ratio of **payload bits** to total transmitted+idle bits/time per slot,” and then ensure all computations use that.  
  - Provide a worked numerical example using Eq. (63) reproducing Table IV-J’s 0.760 exactly, showing all intermediate bit counts and times.  
  - Ensure that the slot-level simulator and packet-level simulator use the same definition and report the same components.

4) **Stress-case contextualization improved, but the workload semantics still need stronger grounding and clearer interpretation**  
- **Why it matters:** \(\eta_S\approx 46\%\) is now framed as a continuous-duty upper bound, and \(d\) addresses realism; that’s good. But the stress workload is still “512 B command per node per cycle” which is extremely strong and may be misread as typical. Also, the paper states commands dominate and are topology-invariant “given centralized command generation,” but then introduces alternative distributed planning with Raft traffic—this is important and should be integrated more cleanly.  
- **Remedy:**  
  - Provide one or two mission vignettes with plausible command rates/sizes (e.g., station-keeping campaign, collision-avoidance broadcast, formation retargeting) and map them to \(d\), \(S_{\text{cmd}}\), and unicast fraction \(q\).  
  - Move “centralized vs distributed planning” into a dedicated subsection with a clear comparison table of \(\eta_{\text{cmd}}\) vs \(\eta_{\text{consensus}}\) and what assumptions change.

5) **Packet-level validation (Section IV-J) is valuable, but it is not yet an “independent validation” of feasibility—only of \(\gamma\)**  
- **Why it matters:** The paper claims “packet-level validation confirms 30 kbps minimum viable.” In reality, it confirms that for one framing/FEC/acquisition assumption, \(\gamma\approx0.76\). The “minimum viable” conclusion also depends on guard time, acquisition dwell, half-duplex partitioning, and whether additional control traffic exists.  
- **Remedy:**  
  - Rephrase IV-J as “standards-grounded parameterization of \(\gamma\)” rather than “validation.”  
  - Add a sensitivity sweep in IV-J over acquisition dwell (e.g., 0–10 ms), guard (geometry uncertainty), and FEC rate, and show the resulting required \(R_{\text{PHY}}\) for feasibility. This would turn IV-J into a practitioner-ready design chart and make the “30 kbps” claim robust (or appropriately conditional).

6) **Airtime modeling of command egress vs ingress is under-specified for mixed traffic and half-duplex operation**  
- **Why it matters:** The paper’s tight margins (e.g., ~900 ms at 30 kbps) mean small omissions matter. It is unclear whether the superframe includes time for coordinator-to-member acknowledgments, control-plane beacons beyond the 0.3 ms sync, or any contention resolution. Also, the “\(\alpha_{\text{RX}}=0.8\)” used in stagger equations appears without a strong derivation (and seems inconsistent with the superframe table where ingress dominates ~92%).  
- **Remedy:**  
  - Explicitly define \(\alpha_{\text{RX}}\) and compute it from the superframe budget for the nominal case; then use that computed value consistently.  
  - Clarify what additional control/management traffic is assumed (or explicitly excluded) in the TDMA superframe.  
  - If ACKs are excluded, justify (e.g., erasure model with no link-layer ACK; reliability via repetition and AoI tolerance).

---

# Minor Issues

1) **Definition drift for “baseline telemetry” vs “status reports”**: early text says baseline telemetry is 256 B and excluded from \(\eta\), but later “all profiles include 1 status report and 1 heartbeat” in the workload envelope section. Make one canonical statement and align all tables.  

2) **Equation (63) units**: clarify whether \(R_{\text{PHY}}\) is in bps or kbps; the “/1000” factor is otherwise confusing.  

3) **Table IV-J cross-model comparison**: “Analyt ingress 30 kbps = 6,930 ms” vs slot/pkt ingress 9,078 ms suggests different accounting (message-layer vs TDMA slot time). Label the columns explicitly as “message-layer serialization time” vs “TDMA airtime incl. guard/acq/FEC.”  

4) **“TDMA required? No at \(\eta/\gamma<36\%\)”**: this appears as a claim in the intro scaling table; provide a citation or derivation (CSMA efficiency/throughput model), or soften wording.  

5) **Coordinator processing model**: 5 ms/msg deterministic is fine for sizing, but when claiming “not binding,” show sensitivity (e.g., 1–20 ms) to support the conclusion at \(k_c=200\).  

6) **Global-state mesh upper bound**: the 73 MB/node/cycle number should show the assumed state size and dissemination method; currently it reads abrupt.  

7) **Fleet reuse**: Eq. (24) assumes perfect spatial reuse and no adjacent-channel interference; add a short note that \(R\) is an empirical/engineering factor and give plausible ranges.

---

## Overall Recommendation  
**Recommendation:** **Major Revision**

The manuscript is promising and substantially improved in Version CB—particularly the introduction of campaign duty factor \(d\), the consistent move to \(\gamma=0.76\) derived from CCSDS, and the clearer positioning of \(\eta_S\approx46\%\) as a continuous-duty upper bound. The three-layer feasibility framework is a strong organizing idea and could become a useful reference for practitioners sizing safe-mode coordination channels.

The main reason for Major Revision is not formatting but scientific positioning and internal consistency: the DES is still presented too close to “validation” when it largely confirms its own assumptions; the feasibility decision procedure needs to be more explicit and less heuristic; and the \(\gamma\)/airtime definitions must be tightened to avoid ambiguity in the central “24 kbps infeasible / 30 kbps minimum” conclusion. Section IV-J is a good step toward independent grounding, but it should be reframed and expanded as a parametric sensitivity/robustness analysis rather than a single-point confirmation.

---

## Constructive Suggestions (ordered by impact)

1) **Add a single end-to-end feasibility procedure (algorithm + worked example)** that takes inputs and outputs required \(R_{\text{PHY}}\), feasibility by layer, and stagger cycles \(L_{\text{cmd}}(q)\).  

2) **Unify \(\gamma\) rigorously**: one definition, one decomposition, one worked example reproducing \(\gamma=0.76\), and consistent use across all timing tables/figures.  

3) **Strengthen IV-J into a design chart**: sweep acquisition dwell, guard time, and FEC rate; show required PHY rate vs those parameters for \(k_c=100\).  

4) **Re-scope DES claims**: demote “DES matches equations” to implementation consistency; elevate buffer-quantile sizing and bursty-duty-factor distributional results as the DES’s real contribution.  

5) **Clarify workload realism with two mission vignettes** mapping to \((d,q,S_{\text{cmd}})\), and present stress-case explicitly as a bounding continuous-duty scenario.  

6) **Make half-duplex ingress/egress partitioning explicit and consistent** (\(\alpha_{\text{RX}}\) derived from the superframe, used everywhere).  

7) **Bolster related work in scheduled MAC/TDMA for space links** (spaceborne TDMA practice, half-duplex constraints, and any relevant CCSDS operational guidance), to better match a top-tier aerospace/space comms journal audience.