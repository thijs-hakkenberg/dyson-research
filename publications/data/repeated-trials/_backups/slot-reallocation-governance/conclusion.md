---
questionId: "rq-1-40"
questionSlug: "slot-reallocation-governance"
type: "discussion-conclusion"
generatedBy: "claude-opus-4-6"
generated: "2026-02-07"
roundCount: 2
terminationReason: "unanimous-conclude"
---

# Slot Reallocation Governance Protocol: Discussion Conclusion

## Summary

The discussion converged on a **tiered-authority, quarantine-first governance model** built around an append-only slot state machine where slots are retired and minted rather than reassigned. This architectural choice—treating the slot lifecycle as an immutable log rather than a mutable registry—dramatically simplifies formal verification on the seL4 kernel and eliminates an entire class of state synchronization failures. The protocol operates primarily at the cluster coordinator level (Tier 2), with beacon spacecraft (Tier 3) involved only for cross-cluster boundary events and catalog reconciliation, ensuring that the system functions within the 7–30 day autonomous operation window without ground-in-the-loop approval for time-critical decisions.

The most significant insight to emerge was that **slot reallocation is fundamentally a trajectory uncertainty propagation problem with a governance wrapper**, not primarily a distributed consensus challenge. The correctness and efficiency of the entire protocol depends on how accurately the swarm can predict a failed node's future trajectory, which in turn determines quarantine zone sizing—the single largest driver of operational impact on neighboring nodes. This reframing elevated passive tracking capability (retroreflectors and fail-safe RF beacons on every node) from a nice-to-have to a critical design requirement, as the difference between tracked and untracked dead nodes translates to quarantine zones differing by orders of magnitude in volume (tens of meters vs. kilometers of cross-track uncertainty at 7 days).

The discussion also established that the binding constraint on reallocation operations is the ΔV budget (0.5–5 m/s/year), not communication bandwidth or computational capacity. Pre-positioned spare nodes (5% of cluster population) eliminate cascading slot migrations that would compound ΔV costs, while a dedicated 20% ΔV reserve per node ensures collision avoidance capacity survives even correlated multi-failure events. The consensus protocol for intra-cluster decisions should be Raft-based (crash fault tolerance), not Byzantine fault tolerant, reflecting the actual threat model of hardware failures in authenticated, formally verified nodes.

## Key Points

- **Append-only slot lifecycle**: Slots transition through NOMINAL → SUSPECT → QUARANTINED → RETIRED, and are never reused with the same ID. Replacement capacity is provided by minting new slots with fresh identifiers and authentication keys. This is the foundational architectural decision enabling formal verification and audit trail integrity.

- **Quarantine-first with trajectory-aware geometry**: Every failure triggers a mandatory minimum 72-hour quarantine. Quarantine zones propagate with the failed node's predicted orbit (not fixed to the original slot location), with inflation rates determined by trajectory uncertainty class (ballistic/tracked vs. tumbling/untracked). The original slot becomes safe to reoccupy once the dead node has drifted sufficiently far.

- **Passive tracking is a hard requirement**: Every node must carry corner cube retroreflectors (~50g × 4) and a fail-safe RF beacon (~100g, independent power) to enable neighbor-based trajectory estimation after primary system failure. Without passive tracking, quarantine zones grow to multi-kilometer scale and can consume 5–15 adjacent slots; with it, quarantine is limited to 1–3 slots.

- **Tiered authority with autonomous cluster operations**: Cluster coordinators (Tier 2) have full authority for intra-cluster quarantine, retirement, and slot minting without beacon approval. Beacons (Tier 3) handle cross-cluster propagation, boundary conflicts, and master catalog reconciliation asynchronously. This eliminates the latency bottleneck while maintaining global consistency.

- **ΔV conservation through spare pre-positioning and reserves**: A 5% spare node population per cluster eliminates cascading operational node migrations. A mandatory 20% per-node ΔV reserve, enforced by the cluster coordinator, is dedicated exclusively to collision avoidance. Single reallocation events are hard-capped at 0.05 m/s per affected node (10% of minimum annual budget).

- **Raft consensus over BFT**: Intra-cluster slot state transitions use leader-based Raft consensus requiring the coordinator plus 2 independent witnesses, providing crash fault tolerance with O(n) message complexity. The threat model (authenticated nodes running formally verified code) does not justify the O(n²) overhead of Byzantine fault tolerance.

## Unresolved Questions

1. **Correlated failure resilience**: What happens when a solar particle event or common-mode hardware defect causes 5+ simultaneous failures within a single cluster? The cumulative quarantine zone expansion and avoidance ΔV costs could exceed available budgets. Monte Carlo simulation of correlated failure scenarios—particularly the interaction between multiple expanding quarantine zones in dense orbital regions—is needed to validate that the protocol degrades gracefully rather than catastrophically.

2. **Cluster coordinator failure during active reallocation**: If the cluster coordinator itself fails mid-quarantine (while managing another node's failure), the Raft leader election must complete and the new coordinator must reconstruct the in-progress quarantine state from the append-only log. The timing and correctness of this handover during an active safety-critical operation needs formal analysis and simulation, particularly if the coordinator failure is correlated with the original failure event.

3. **Long-term slot density evolution over 50 years**: With 1–3% annual attrition and periodic spare replenishment, how does the distribution of active vs. retired slots evolve over decades? Retired slots leave behind predicted debris trajectories that constrain future slot minting. Does the orbital volume eventually become fragmented in ways that reduce achievable packing density, and if so, when does cluster boundary reorganization become necessary?

4. **Fail-safe RF beacon design and interference management**: The proposed independent RF beacon for passive tracking must survive the same failure that kills the primary satellite systems, operate on independent power, and not interfere with the swarm's inter-satellite communication links. The specific frequency, power, modulation scheme, and electromagnetic compatibility constraints with the primary communication system remain unspecified.

## Recommended Actions

1. **Develop and simulate the trajectory uncertainty propagation model**: Build a high-fidelity simulation of failed node trajectory evolution under the three uncertainty classes (ballistic/tracked, tumbling/tracked, untracked) incorporating solar radiation pressure, gravitational perturbations, and realistic passive tracking measurement noise. Use this to generate validated quarantine zone inflation parameters—the numerical values that will be hardcoded into the flight software. This is the highest-priority task because every other protocol parameter (neighbor avoidance ΔV, quarantine duration, slot spacing) derives from these uncertainty bounds.

2. **Run Monte Carlo correlated failure campaigns**: Using the planned 10,000+ node simulation environment, inject correlated failure scenarios (2–10 simultaneous failures per cluster, spatially clustered and randomly distributed) and measure: aggregate avoidance ΔV consumed, number of secondary slot quarantines triggered, time to catalog convergence, and whether the 10⁻⁶ collision probability threshold is maintained throughout. Identify the failure multiplicity at which the protocol breaks down and design circuit-breaker mechanisms (e.g., cluster-wide safe mode, emergency beacon escalation) for those scenarios.

3. **Formally specify and verify the slot state machine on seL4**: Translate the NOMINAL → SUSPECT → QUARANTINED → RETIRED → MINTED state machine into a formally verified seL4 kernel service with mathematically proven properties: no state can be skipped, transitions require cryptographically valid attestations from the required quorum, and the append-only log cannot be modified retroactively. This should be an early deliverable that anchors the flight software architecture.

4. **Prototype the passive tracking subsystem**: Design, build, and test the fail-safe RF beacon and retroreflector package as a standalone hardware module. Validate detection range, Doppler measurement accuracy, and trajectory reconstruction precision using ground-based or ISS-based experiments. Establish the mass, power, and volume budget with sufficient confidence to include in the satellite bus design. This is on the critical path because it affects satellite mechanical and electrical design.

5. **Define the beacon catalog reconciliation protocol**: Specify the exact mechanism by which beacon spacecraft merge asynchronous cluster-level updates into the master ephemeris catalog, detect and resolve conflicts (e.g., overlapping quarantine zones from adjacent clusters), and rebroadcast the reconciled catalog. Test update propagation latency and correctness under realistic communication delay and partition scenarios, particularly the 30-day autonomous operation case where clusters may have diverged significantly before reconnection.