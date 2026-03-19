---
questionId: "rq-1-40"
questionSlug: "slot-reallocation-governance"
type: "discussion-conclusion"
generatedBy: "claude-opus-4-6"
generated: "2026-02-24"
roundCount: 3
terminationReason: "unanimous-conclude"
---

# Slot Reallocation Governance Protocol: Discussion Conclusion

## Summary

Across three rounds of discussion, a strong and detailed consensus emerged around a **quarantine-first, tiered-authority governance model** for managing slot reallocation in the Swarm Control System. The core principle—**the swarm must be safe before it is efficient**—drove every architectural decision. Failed nodes do not disappear; they become uncontrolled objects whose trajectories must be characterized before any slot can be reassigned. This led to a seven-state slot lifecycle (ACTIVE → SUSPECT → QUARANTINE → FENCED → ESCALATED/VACANT → LEASED → ACTIVE) implemented as a formally verifiable deterministic state machine on the seL4 microkernel, with explicit transition guards that prevent any shortcutting of safety-critical intermediate states.

The authority hierarchy crystallized around a clean separation: **cluster coordinators hold autonomous, unilateral safety authority** (failure declaration, quarantine zone computation, neighbor collision avoidance commands) while **beacon spacecraft hold exclusive reassignment and catalog amendment authority** with global cross-cluster visibility. Safety decisions are deterministic computations given shared state, not consensus negotiations—deliberately avoiding the latency and complexity of Byzantine fault-tolerant protocols for time-critical actions. Raft-style consensus is reserved for non-urgent coordinator election, and catalog amendments require dual-beacon confirmation to prevent single-point-of-failure corruption of the swarm-wide ephemeris.

The most consequential quantitative finding was that **neighbor-nudge ΔV costs are the binding constraint** on the entire protocol. At a 3% annual failure rate, quarantine-related neighbor adjustments can consume 0.12–1.2 m/s/year—potentially exceeding the 0.5 m/s/year lower bound of the propulsion budget. This finding forces a feedback loop into propulsion system sizing and swarm topology design, and validates the absorb-rather-than-replace strategy where vacated slots are retired into an overcapacity pool rather than filled by migrating existing nodes.

## Key Points

- **Quarantine-first is non-negotiable.** No slot is reassigned until the failed node's drift trajectory is characterized to within one keep-out tube diameter over a 30-day propagation horizon. Quarantine zones are asymmetric drift cones (not spheres) that shrink over time as neighboring nodes track the debris, minimizing the number of affected neighbors and conserving ΔV.

- **Safety authority is local and deterministic; reassignment authority is global and confirmed.** Cluster coordinators declare quarantines unilaterally within seconds. Beacon spacecraft authorize permanent catalog amendments with dual-beacon cross-confirmation, adding minutes to hours of latency that is acceptable because quarantine already provides the safety envelope.

- **The seven-state slot machine enforces safety invariants architecturally.** Every transition is a predicate over observable variables (heartbeat counters, conjunction probabilities, ΔV reserves). No transition depends on ground-in-the-loop input. The QUARANTINE→ACTIVE shortcut is structurally impossible, guaranteeing that FENCED and VACANT are mandatory waypoints.

- **ΔV budget analysis reveals the 0.5 m/s/year lower bound is likely insufficient** for interior swarm nodes subject to neighbor-nudge demands. A minimum of 1.5 m/s/year is recommended for non-peripheral nodes, with 15–25% of the annual budget reserved as a governance reserve for quarantine-related adjustments.

- **Absorb losses rather than migrate replacements.** The swarm should be designed with 5–10% slot overcapacity. Vacated slots are retired; replacement nodes launched in subsequent batches occupy new slots from the overcapacity pool, consuming zero migration ΔV from existing nodes. Migration is reserved only for critical topology slots (communication relays, power beaming geometry keystones).

- **Correlated failures are the existential risk.** A solar particle event or firmware defect batch causing >5% cluster loss within 24 hours triggers cluster-wide safe mode (2× keep-out tubes, halved screening intervals, suspended non-essential operations). This scenario is the primary justification for the beacon tier's existence and must be the focus of Monte Carlo simulation campaigns.

## Unresolved Questions

1. **Does the ΔV budget actually close?** The analysis shows neighbor-nudge costs at 3% failure rate can consume 24–240% of a 0.5 m/s/year budget. Rigorous simulation with realistic failure distributions, cluster geometries, and solar radiation pressure models is needed to determine whether 1.5 m/s/year is sufficient or whether propulsion system requirements must be further revised. This is a potential project-level design driver.

2. **How should cross-cluster ESCALATED events be resolved?** When a drifting failed node exits one cluster's jurisdiction and enters another's, the handoff protocol between cluster coordinators—and the beacon's role in adjudicating conflicting quarantine zones at cluster boundaries—remains underspecified. The interaction geometry and communication latency between adjacent clusters needs detailed modeling.

3. **What is the optimal heartbeat interval and confirmation threshold?** The discussion converged on 3–5 missed heartbeats at 5–10 second intervals (15–50 seconds to failure declaration), but the tradeoff between false-positive rate and detection latency has not been quantified against realistic communication disruption statistics (solar conjunction shadowing, antenna pointing errors, transient interference).

4. **How should the DORMANT/retirement decision be made?** The cost-benefit threshold for permanently retiring a vacated slot versus holding it for future replacement—considering local energy collection value, conjunction density, and remaining swarm lifetime—needs a formal decision framework that balances capacity loss against governance overhead.

## Recommended Actions

1. **Formally specify and verify the seven-state slot machine.** Produce a TLA+ or Alloy model of the state machine with all transition guards, and verify key safety properties (no QUARANTINE→ACTIVE shortcut, no VACANT without beacon confirmation, liveness under coordinator failover). This specification becomes a binding input to the seL4 kernel software architecture.

2. **Run Monte Carlo ΔV budget simulations.** Using the planned 10,000-node simulation environment, model 50-year swarm lifetimes with stochastic failure injection (1–3% annual rate, including correlated failure bursts). Track cumulative ΔV consumption per node for station-keeping, neighbor nudges, and slot migration. Determine the minimum propulsion budget that keeps all nodes within their ΔV envelope at 95th-percentile failure scenarios. Feed results back into propulsion system requirements.

3. **Prototype the dual-beacon catalog amendment protocol.** Implement the signed delta-update mechanism (node ID, orbital elements, covariance, slot state, dual-beacon signatures) and test update propagation latency, bandwidth consumption, and consistency recovery after 30-day autonomous operation periods. Specifically stress-test the degraded single-beacon mode with expanded quarantine margins.

4. **Model slot adjacency graphs and identify critical topology slots.** For representative Phase 1 swarm geometries (1,000–3,000 nodes), compute the slot adjacency graph and identify slots whose failure triggers disproportionate neighbor-nudge cascades or communication topology fragmentation. Assign these slots higher-capability nodes with ≥3 m/s/year ΔV budgets and prioritize them for replacement rather than retirement.

5. **Establish the propulsion budget feedback loop as a project-level decision.** The finding that 0.5 m/s/year may be insufficient for interior nodes is a potential requirements conflict with the automotive-grade component cost targets. Convene a trade study between propulsion system capability, swarm density (inter-node spacing), failure rate assumptions, and governance protocol ΔV demands to find the feasible design space. This trade must be resolved before Phase 1 preliminary design review.