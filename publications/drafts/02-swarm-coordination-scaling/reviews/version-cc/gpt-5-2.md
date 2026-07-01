---
paper: "02-swarm-coordination-scaling"
version: "cc"
modelId: "gpt-5-2"
modelName: "GPT-5.2"
reviewed: "2026-02-28"
recommendation: "Major Revision"
---

## 1. Significance & Novelty  
**Rating: 4 (Good)**  
The manuscript targets a real gap: *parametric, closed-form sizing* for hierarchical coordination traffic at \(10^3\)–\(10^5\) nodes under a tight per-node budget, with explicit separation of (i) message-layer byte budget, (ii) MAC efficiency, and (iii) TDMA airtime feasibility. The “three-layer feasibility” framing plus the coordinator-ingress bottleneck equation are practically valuable, and the paper is unusually explicit about what is and is not modeled. The addition of a standards-grounded \(\gamma\) (CCSDS Proximity-1) is a meaningful improvement over earlier “assumed efficiency” treatments.

Novelty is more *engineering synthesis* than new theory: most individual ingredients (AoI, GE channels, TDMA budgeting, hierarchical aggregation) are known, but the paper’s contribution is in unifying them into a coherent sizing workflow with design-point conclusions (e.g., “30 kbps minimum viable coordinator PHY given \(\gamma=0.76\)”). That is appropriate for T-AES if the validation story and assumptions are tightened.

---

## 2. Methodological Soundness  
**Rating: 3 (Adequate)**  
The analytical accounting is straightforward and mostly correct; the slot-level TDMA simulator is the right tool to check superframe schedulability and ARQ–airtime coupling; and the packet-level \(\gamma\) derivation is a strong step toward physical realism. The DES is efficient and supports Monte Carlo sweeps.

However, several modeling choices materially affect conclusions and are not yet handled with sufficient rigor: (a) the “campaign duty factor” \(d\) is treated as Bernoulli i.i.d. per-cycle while the paper simultaneously argues campaigns are temporally correlated; (b) the GE coherence assumption (state constant over a full 10 s cycle) is pivotal to the “ARQ infeasible” conclusion; and (c) the PHY/MAC boundary is partially double-counted/unclear in places (e.g., analytic “ingress 6,930 ms” vs slot/pkt “9,078 ms” with \(\gamma=0.76\)). These are fixable but currently weaken methodological robustness.

---

## 3. Validity & Logic  
**Rating: 3 (Adequate)**  
Internal logic is generally consistent: the decomposition \(\eta=\eta_0+d\eta_{\text{cmd}}\) clarifies workload realism; the stress-case is now framed as a continuous-duty upper bound; and the three-layer feasibility framework correctly distinguishes “fits in bytes” vs “fits in airtime.”

Remaining validity concerns are about *interpretation and boundary conditions*:
- The stress-case \(\eta_S\approx 46\%\) is repeatedly used as a sizing driver while the operational narrative says RF-backup is \(<1\%\) of lifetime and campaigns are episodic. This is not wrong, but the paper must more explicitly define what is being “made safe” under RF-backup (what functions are preserved, what are degraded) and which workload is the RF-backup requirement driver.
- Several “threshold” statements (e.g., “TDMA required when \(\eta_{\text{total}}/\gamma>50\%\)”) read heuristic; they need derivation or be labeled as rule-of-thumb tied to half-duplex partitioning assumptions.

---

## 4. Clarity & Structure  
**Rating: 4 (Good)**  
The manuscript is well organized, with clear notation, tables, and a useful “claim map.” The authors do a good job disambiguating DES vs slot-level vs packet-level tools, which is often a source of confusion in networking-for-space papers.

Clarity issues remain in a few high-impact spots: the definition and use of \(\gamma\) is not perfectly consistent across sections; the “baseline telemetry excluded from \(\eta\)” convention is good but occasionally leads to confusing statements like “Nominal includes 1 heartbeat” while baseline is status only; and some computed numbers (e.g., ingress time in Table 18) appear to mix “raw PHY time” and “effective time after overhead.”

---

## 5. Ethical Compliance  
**Rating: 4 (Good)**  
Data/code availability is strong (repo tag, environment, tools). AI assistance is disclosed in Acknowledgment. That is good practice.

Two improvements needed for reproducibility: (i) provide a *single* configuration file or table mapping that reproduces each key figure/table (especially those used to justify “30 kbps minimum”), and (ii) specify exact CCSDS Proximity-1 framing assumptions used to compute the 104-bit overhead (fields included, any interleaving, etc.) so another group can independently recreate \(\gamma=0.76\).

---

## 6. Scope & Referencing  
**Rating: 3 (Adequate)**  
The paper is in-scope for T-AES (space comms/architectures, autonomy support, protocol sizing). Citations cover swarm robotics, distributed algorithms, AoI, GE, and CCSDS.

Gaps: the MAC/TDMA discussion would benefit from citing space-appropriate scheduled-access work (e.g., Proximity-1 operational analyses, LEO crosslink MAC studies, or DTN/LTP/CFDP scheduling papers) and from positioning against “constellation operations network management” literature beyond Starlink/OneWeb press-style sources. Several references are non-archival; that’s acceptable for context but should not support key technical claims.

---

# Major Issues

1. **\(\gamma\) application is not fully consistent; risk of mixing “time-based” vs “bit-based” efficiencies.**  
   **Why it matters:** The headline conclusion “24 kbps infeasible, 30 kbps minimum viable” hinges on \(\gamma=0.76\). Any inconsistency in how \(\gamma\) is applied (payload vs framing vs guard/acquisition) undermines the central design point. Table 18 (“Analyt ingress 6,930 ms” vs slot/pkt “9,078 ms”) suggests two different accounting baselines.  
   **Remedy:**  
   - Define \(\gamma\) *once* as: \(\gamma \equiv \frac{\text{payload bits}}{\text{total transmitted bits-equivalent including time overhead}}\) for the specific PHY rate and slot structure.  
   - Provide a single “time per 256 B report” derivation that yields 9,078 ms for 99 members at 30 kbps with \(\gamma=0.76\), and ensure every equation/table uses that same mapping.  
   - Audit all places where \(1/\gamma\) is applied (e.g., Eq. 14 vs Eq. 16 vs Eq. 34 summary) and ensure coordinator sizing uses \(\gamma\) consistently: \(C_{\text{coord,PHY}} \ge \frac{(k_c-1)S_{\text{eph}}8}{T_c\gamma}\).

2. **Campaign duty factor \(d\): mean realism addressed, but burst realism and queueing implications are underdeveloped.**  
   **Why it matters:** The manuscript explicitly notes Bernoulli \(d\) understates temporal autocorrelation and is optimistic for peak buffer occupancy—yet buffer sizing and coordinator ingress variability are central. Practitioners care about worst-hour/day behavior, not just annual mean \(\eta(d)\).  
   **Remedy:** Add a second campaign model (e.g., ON/OFF Markov with mean ON length \(L_{\text{on}}\)) and show how (i) coordinator buffer CDF, (ii) drop probability under finite buffers, and (iii) any AoI transient metrics change for fixed marginal \(d\). Even a small sweep (e.g., \(L_{\text{on}}\in\{1,10,100,1000\}\) cycles) would materially strengthen the “workload realism” claim.

3. **Stress-case contextualization improved, but requirements mapping is still ambiguous (what must RF-backup support?).**  
   **Why it matters:** The paper sizes RF-backup around the most constrained regime, but mixes “safe-mode exception-only reporting” with “stress-case continuous command” in ways that can read contradictory. If RF-backup is for safe-mode, then stress-case command every cycle may not be a relevant requirement; if it is a requirement, the operational concept must justify it.  
   **Remedy:** Add a short “requirements table” that states, per operating mode (optical nominal vs RF-backup), which workload profile(s) are required (N/E/S), what functions are supported (e.g., collision alerts broadcast, heartbeat, minimal ephemeris), and which are deferred. Then explicitly state: “30 kbps is required to support *RF-backup with full periodic ephemeris ingestion for \(k_c=100\)*” (or whatever the true requirement is).

4. **Three-layer feasibility framework is promising but needs a more formal link between Layer 2 (MAC efficiency) and Layer 3 (TDMA airtime).**  
   **Why it matters:** Layer 2 currently uses \(\eta_{\text{total}}/\gamma\) as an “effective utilization” proxy; Layer 3 then does explicit airtime. Without a clear theorem/derivation, Layer 2 can be misread as sufficient for schedulability.  
   **Remedy:**  
   - State explicitly: Layer 2 is a *necessary but not sufficient* condition for scheduled half-duplex feasibility.  
   - Provide a short derivation showing under what assumptions \(\eta_{\text{total}}/\gamma < 1\) relates to airtime feasibility, and why half-duplex partitioning motivates the ~50% heuristic (or replace the heuristic with explicit inequalities like Eqs. 27–28 using \(\alpha_{\text{RX}}\)).

5. **DES “verification” value remains limited; it mainly confirms its own accounting and does not validate against independent phenomena.**  
   **Why it matters:** The paper correctly admits DES/analytic agreement is expected. Reviewers/readers will ask: what new insight does DES provide beyond means already available in closed form? The current answer is “distributional ingress variability,” which is good but could be stronger.  
   **Remedy:** Elevate DES contributions by adding at least one result that cannot be obtained from the closed-form equations as written, e.g.:  
   - joint distribution of ingress burst + GE burst leading to drop probability under finite buffer,  
   - tail of coordinator queue under ON/OFF campaigns,  
   - sensitivity of AoI tails under combined loss + campaign correlation.  
   Alternatively, reduce DES emphasis and present it as an implementation aid rather than a validation pillar.

6. **Packet-level validation (Section IV-J) is helpful but not fully “independent validation” of the overall model.**  
   **Why it matters:** Deriving \(\gamma\) from CCSDS framing anchors one parameter, but it does not validate the traffic model, the half-duplex timing, or the acquisition/guard assumptions. Also, “5 ms acquisition dwell typical S-band ISL” is not sourced strongly and may dominate \(\gamma\).  
   **Remedy:**  
   - Provide citations or engineering justification for acquisition dwell (or treat it as a parameter and show sensitivity).  
   - Show \(\gamma(S)\) vs payload size \(S\) to demonstrate the general expression is correct and useful (practitioners will vary report sizes).  
   - Clarify which parts of Proximity-1 are being modeled (e.g., ASM, addressing mode, control field sizes) and whether the 104-bit overhead is per frame or per transfer frame.

7. **Generalized \(\gamma\) expression (Eq. 41) has dimensional/notation ambiguity and needs tightening for practitioner use.**  
   **Why it matters:** This is positioned as a practitioner tool. As written, it mixes bits, milliseconds, and a “/1000” factor that is easy to misuse; also \(R_{\text{PHY}}\) is sometimes called “bps” but the equation suggests “kbps.”  
   **Remedy:** Rewrite Eq. 41 in a dimensionally explicit form, e.g.  
   \[
   \gamma=\frac{S8}{\frac{S8+O_{\text{frame}}}{R_{\text{FEC}}}+R_{\text{PHY}}(T_{\text{guard}}+T_{\text{acq}})}
   \]
   with \(T\) in seconds and rates in bps, and provide a worked numeric example reproducing \(\gamma=0.760\).

---

# Minor Issues

1. **Coordinator ingress equation uses \(k_c\) in abstract/summary but text uses \(k_c-1\).** Standardize (coordinator excluded?) everywhere.  
2. **Baseline vs \(\eta\) confusion:** In Section IV-E “all profiles include 1 heartbeat” but earlier heartbeats are part of \(\eta_0\). Clarify that “profiles” here refer to hierarchical mode only.  
3. **Table 18 (“Analyt ingress 30 kbps = 6,930 ms”)** appears inconsistent with the stated payload and \(\gamma\). Recompute or explain what that analytic number represents (payload-only time?).  
4. **Heuristic thresholds:** “TDMA required when \(\eta_{\text{total}}/\gamma > 50\%\)” needs either derivation or label as a conservative rule-of-thumb tied to \(\alpha_{\text{RX}}\approx 0.9\) etc.  
5. **Link budget:** Provide margin assumptions (required \(E_b/N_0\)) source; BPSK BER \(<10^{-5}\) at 9.6 dB depends on coding/no coding. Align with the FEC assumptions used in \(\gamma\).  
6. **AoI section:** If AoI is insensitive to bandwidth “under this model,” say so explicitly; otherwise readers may generalize incorrectly.  
7. **Sectorized mesh comparator:** Since it is “not competing,” consider moving some of it to an appendix or reducing emphasis to avoid diluting the main story.  
8. **Non-archival references:** Ensure key technical claims (e.g., Starlink ops constraints) are not dependent on non-archival sources.  
9. **Typographic:** A few places use “kbps” for both “kb/s” and “kbps PHY”; define consistently (kb/s vs kbps).  
10. **NS-3 gap:** Consider naming which NS-3 modules or a minimal packet-level contention scenario you expect would change conclusions (e.g., hidden terminal, capture, multi-cluster interference).

---

## Overall Recommendation  
**Recommendation:** **Major Revision**

The manuscript has a strong engineering objective and a useful unifying framework. The improvements over earlier versions are clear and substantive: the campaign duty factor \(d\) directly addresses workload realism concerns; the stress-case is now framed as a continuous-duty upper bound; and the CCSDS-grounded \(\gamma=0.76\) derivation is a meaningful step toward standards realism and supports the “30 kbps minimum viable” claim.

The paper is not yet at top-tier journal standard because the central boundary condition—how \(\gamma\) is defined and applied across layers/tools—still shows internal inconsistencies, and the workload burstiness realism (temporal correlation of campaigns) is acknowledged but not actually treated in the results in a way that would support buffer/drops conclusions. In addition, the validation narrative still leans heavily on self-consistency checks; the packet-level work anchors one parameter but does not yet constitute independent validation of the full sizing workflow.

With a focused revision addressing \(\gamma\) consistency, campaign burst modeling, and a clearer requirements-to-modes mapping for RF-backup vs nominal operations, this could become a valuable reference paper for practitioners sizing hierarchical coordination links in large constellations/swarms.

---

## Constructive Suggestions (ordered by impact)

1. **Unify \(\gamma\) across the entire manuscript** (single definition, dimensional correctness, one worked example reproducing \(\gamma=0.76\), audit all uses).  
2. **Add ON/OFF (Markov) campaign modeling** to complement Bernoulli \(d\), and show its impact on buffer CDF/drop probability and any tail metrics.  
3. **Add an explicit “operating modes vs required workloads/functions” table** to reconcile RF-backup safe-mode narrative with stress-case sizing.  
4. **Strengthen the three-layer feasibility argument** by formally stating necessary vs sufficient conditions and tying Layer 2 to Layer 3 via explicit inequalities rather than heuristics.  
5. **Elevate DES value with at least one genuinely emergent result** (finite-buffer drop probability under correlated campaigns + GE bursts; or joint tails) that cannot be read off the closed-form mean equations.  
6. **Improve Section IV-J practitioner utility**: cite/parameterize acquisition dwell; show \(\gamma\) sensitivity vs payload size and code rate; clearly enumerate Proximity-1 overhead fields used.  
7. **Tighten coordinator ingress sizing statements** (\(k_c\) vs \(k_c-1\), include coordinator self-report or not) and ensure all numeric examples match the stated assumptions.