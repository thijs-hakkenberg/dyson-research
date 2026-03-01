"""Swarm coordination simulation model for Dyson swarm elements.

Self-contained discrete-event simulator that models coordination of
large-scale Dyson swarm elements under three network topologies
(centralized, hierarchical, mesh).  Addresses research questions on
architecture at scale, coordinator duty cycling, and fleet coordination
constraints.

Ported from the TypeScript modules in
``src/lib/services/simulation/swarm-coordination/``.
"""

from __future__ import annotations

__version__ = "1.0.0"

import heapq
import math
import random as _stdlib_random
from dataclasses import dataclass, field
from typing import Any, Literal, Optional

import numpy as np
from numpy.random import Generator

# ---------------------------------------------------------------------------
# Literal types
# ---------------------------------------------------------------------------
CoordinationTopology = Literal["centralized", "hierarchical", "mesh", "sectorized_mesh"]
NodeStatus = Literal["operational", "coordinator", "failed", "recovering"]
EventType = Literal[
    "message_send",
    "message_receive",
    "coordinator_handoff",
    "node_failure",
    "node_recovery",
    "collision_warning",
    "gossip_round",
    "state_sync",
]

# ---------------------------------------------------------------------------
# Physical / protocol constants
# ---------------------------------------------------------------------------
SPEED_OF_LIGHT_KM_S: float = 299_792
"""Speed of light used for communication-delay calculations (km/s)."""

INTER_NODE_DISTANCE_KM: float = 1_000
"""Typical inter-node spacing in a Dyson swarm (km)."""

REGIONAL_DISTANCE_KM: float = 50_000
"""Distance to a regional coordinator in the hierarchical topology (km)."""

CENTRAL_DISTANCE_KM: float = 150_000_000
"""Average distance to the central coordinator (~1 AU) (km)."""

MESSAGE_SIZES: dict[str, int] = {
    "ephemeris": 256,
    "heartbeat": 32,
    "handoff": 8192,
    "gossip": 128,
    "collision": 64,
    "cluster_summary": 512,
    "region_summary": 1024,
    "coordination_command": 512,
    "coordination_heartbeat": 64,
    "collision_alert": 128,
}
"""Message sizes in bytes by type."""

HANDOFF_STATE_SIZE_BYTES: int = 8192
"""Cluster ephemeris data transferred during coordinator handoff."""

HANDOFF_VERIFICATION_ROUNDS: int = 3
"""Number of verification rounds during coordinator handoff."""

HANDOFF_TIMEOUT_SECONDS: float = 30.0
"""Timeout for a coordinator handoff attempt (seconds)."""

SECONDS_PER_DAY: int = 86_400


# ---------------------------------------------------------------------------
# Core dataclasses
# ---------------------------------------------------------------------------
@dataclass
class SwarmCoordinationConfig:
    """Configuration for a swarm coordination simulation run."""

    node_count: int = 10_000
    """Number of nodes in the swarm (1 000 -- 1 000 000)."""

    coordination_topology: CoordinationTopology = "hierarchical"
    """Network topology for coordination."""

    cluster_size: int = 100
    """Nodes per cluster for hierarchical topology (50--200)."""

    coordinator_duty_cycle_hours: float = 24.0
    """Hours before coordinator handoff (1--168 h)."""

    bandwidth_per_node_kbps: float = 1.0
    """Bandwidth per node in kbps (0.1--10)."""

    node_failure_rate_per_year: float = 0.02
    """Annual failure rate per node (0.01--0.05)."""

    coordinator_power_w: float = 18.0
    """Power consumption when acting as coordinator (W)."""

    base_power_w: float = 5.0
    """Base power consumption for regular nodes (W)."""

    simulation_days: int = 90
    """Simulation duration in days (30--365)."""

    seed: int = 42
    """Random seed for reproducibility."""

    max_events: Optional[int] = None
    """Override maximum events processed (default: node_count * simulation_days * 10)."""

    enable_exception_telemetry: bool = False
    """When True, hierarchical nodes only report when state changes exceed threshold."""

    exception_threshold: float = 0.01
    """Probability that a node's state has changed enough to require a report (0--1).

    For exception_threshold=0.01, ~1% of nodes report each cycle.
    For exception_threshold=0.30, ~30% of nodes report each cycle.
    """

    link_availability: float = 1.0
    """Probability that any given message is successfully delivered (0--1).

    1.0 = perfect links, 0.5 = 50% duty-cycle / link availability.
    """

    coordinator_link_capacity_kbps: float = 0.0
    """Maximum ingress+egress bandwidth for a single cluster coordinator (kbps).

    0.0 = unlimited (coordinator pools its cluster's bandwidth, the default
    assumption in Versions A--G).  A positive value caps the coordinator's
    aggregate inbound+outbound rate, causing message drops when the rate
    exceeds the capacity.  Sweep values: 1, beta*k_c for beta in [0.1, 1.0].
    """

    max_retransmissions: int = 0
    """Maximum retransmission attempts for a lost message within T_c (0 = none).

    When >0, a message that fails the link_availability Bernoulli trial is
    re-attempted up to max_retransmissions times, each attempt consuming
    additional time = propagation_delay.  The message is dropped if all
    attempts fail.
    """

    sync_sample_rate: float = 0.0
    """Override node sampling rate for state-sync events.

    0.0 = automatic (min(1.0, 1000/N)).  A positive value forces the
    fraction of nodes that participate in each sync cycle.  Use 1.0 for
    full-fidelity simulation (all nodes active every cycle).
    """

    coordinator_scheduling: Literal["random", "tdma"] = "random"
    """MAC scheduling model for intra-cluster coordinator ingress.

    "random" = nodes transmit at random phase within T_c (Poisson-like arrivals).
    "tdma" = nodes transmit in deterministic TDMA slots within T_c, eliminating
    intra-cycle burstiness.  Guard time overhead is controlled by
    guard_time_fraction.
    """

    guard_time_fraction: float = 0.15
    """Fraction of each TDMA slot consumed by guard time (0--0.5).

    Only used when coordinator_scheduling="tdma".  A value of 0.15
    corresponds to MAC efficiency gamma=0.85.
    """

    workload_profile: Literal["stress", "nominal", "event_driven", "distributed"] = "stress"
    """Workload profile controlling coordinator-to-member command traffic.

    "stress" = one unique 512 B command per member per cycle (conservative
        upper bound; models continuous per-node maneuver directives).
    "nominal" = no per-member commands; coordinator sends cluster summary
        upstream only.  Members still send ephemeris + heartbeats.
    "event_driven" = commands sent only to nodes experiencing events
        (conjunction, maneuver), modeled as Bernoulli with p_event per
        node per cycle.
    "distributed" = commands generated by intra-cluster consensus (Raft)
        rather than centrally.  Each consensus round produces
        k_c × vote_msg_size bytes of traffic.  Number of rounds
        controlled by distributed_consensus_rounds.
    """

    event_command_probability: float = 0.01
    """Probability that a node requires an individual command per cycle.

    Only used when workload_profile="event_driven".  Default 0.01 means
    ~1% of nodes receive per-node commands each cycle on average.
    """

    campaign_duty_factor: float = 1.0
    """Fraction of cycles in which commands are active (d in [0,1]).

    Scales all command traffic uniformly.  d=1.0 = continuous (stress-case).
    d=0.01 = commands active 1% of cycles (realistic orbit-raising campaign).
    d=0.10 = commands active 10% of cycles (intensive reconfiguration).
    Applied to all workload profiles except "nominal" (which has no commands).
    """

    campaign_mode: str = "bernoulli"
    """Campaign activation model: "bernoulli" or "on_off".

    "bernoulli": i.i.d. per-cycle coin flip with probability d.
    "on_off": Markov ON/OFF model with geometric ON/OFF durations.
      Mean ON length = campaign_on_length cycles.
      Mean OFF length computed from d: L_off = L_on * (1-d) / d.
      Produces identical marginal d but temporally correlated bursts.
    """

    campaign_on_length: int = 1
    """Mean ON duration in cycles for ON/OFF campaign model.

    Only used when campaign_mode="on_off".  L_on=1 is equivalent to Bernoulli.
    L_on=100 means campaigns persist for ~100 consecutive active cycles.
    """

    distributed_consensus_rounds: int = 3
    """Number of Raft consensus rounds for distributed workload profile.

    Only used when workload_profile="distributed".  Each round generates
    k_c × vote_msg_size bytes of intra-cluster consensus traffic.
    Default 3 matches Raft's typical RequestVote + 2 AppendEntries rounds.
    """

    distributed_vote_msg_bytes: int = 128
    """Vote/consensus message size for distributed workload (bytes).

    Only used when workload_profile="distributed".
    """

    enforce_airtime: bool = False
    """When True, track per-cycle airtime and enforce T_c deadline.

    Each message consumes airtime = slot_duration_ms based on TDMA slot
    model.  If cumulative airtime exceeds T_c × 1000, excess messages
    are flagged as deadline misses and dropped.
    """

    airtime_slot_duration_ms: float = 92.7
    """TDMA slot duration in ms for airtime enforcement.

    Only used when enforce_airtime=True.  Default 92.7 ms corresponds to
    the slot-sim nominal slot duration at 24 kbps.
    """

    airtime_turnaround_ms: float = 2.0
    """TX/RX turnaround time in ms for airtime enforcement.

    Only used when enforce_airtime=True.
    """

    link_model: Literal["bernoulli", "gilbert_elliott"] = "bernoulli"
    """Link loss model.

    "bernoulli" = i.i.d. per-message loss with probability (1 - link_availability).
    "gilbert_elliott" = two-state Markov chain with correlated burst losses.
        The steady-state availability depends on transition probabilities
        and per-state loss rates (see ge_* parameters).
    """

    ge_p_good_to_bad: float = 0.05
    """Gilbert-Elliott: probability of transitioning good->bad per cycle.

    Controls mean duration of good state = 1/ge_p_good_to_bad cycles.
    Default 0.05 = mean 20 cycles (200 s) between outage onsets.
    """

    ge_p_bad_to_good: float = 0.5
    """Gilbert-Elliott: probability of transitioning bad->good per cycle.

    Controls mean outage duration = 1/ge_p_bad_to_good cycles.
    Default 0.5 = mean 2 cycles (20 s) outage, modeling Earth occlusion.
    """

    ge_p_loss_good: float = 0.01
    """Gilbert-Elliott: message loss probability in good state."""

    ge_p_loss_bad: float = 0.90
    """Gilbert-Elliott: message loss probability in bad state."""

    enable_phase_stagger: bool = False
    """When True, stagger cluster coordinator reporting phases deterministically.

    Only used with hierarchical topology and random scheduling.  Each cluster
    coordinator fires at offset = (cluster_index / n_clusters) * T_c,
    spreading regional coordinator inbound traffic evenly across the cycle.
    Non-coordinator members still use random phase offsets.
    """

    aoi_sigma_0_m: float = 10.0
    """Initial post-update ephemeris position error (metres).

    Used for the lightweight AoI-to-position-error coupling model:
    sigma(t) = sigma_0 + sigma_dot * AoI.
    """

    aoi_sigma_dot_m_per_s: float = 0.5
    """Along-track position uncertainty growth rate (m/s).

    Typical LEO value ~0.5 m/s from atmospheric drag uncertainty.
    Used for AoI-to-position-error coupling model.
    """

    sector_size: int = 0
    """Number of nearest orbital neighbors for sectorized mesh gossip.

    0 = automatic (ceil(sqrt(N))).  Only used for sectorized_mesh topology.
    Each node gossips with its sector_size nearest neighbors.
    """


@dataclass
class SwarmNode:
    """Individual swarm node state."""

    id: str
    status: NodeStatus
    cluster_id: str
    is_coordinator: bool
    coordinator_time_seconds: float = 0.0
    power_consumed_wh: float = 0.0
    messages_sent: int = 0
    messages_received: int = 0
    last_update_time: float = 0.0
    failure_time: Optional[float] = None


@dataclass
class Cluster:
    """Cluster state for hierarchical topology."""

    id: str
    node_ids: list[str]
    coordinator_id: str
    regional_coordinator_id: Optional[str] = None
    messages_processed: int = 0
    last_handoff_time: float = 0.0
    failed_handoffs: int = 0


@dataclass
class Message:
    """Message in the coordination network."""

    id: str
    sender_id: str
    receiver_id: str
    size_bytes: int
    send_time: float
    receive_time: Optional[float] = None
    delivered: bool = False
    message_type: str = "ephemeris"


@dataclass
class SimEvent:
    """A single discrete-event simulation event."""

    type: EventType
    time: float
    node_id: str
    cluster_id: Optional[str] = None
    data: Optional[dict[str, Any]] = None

    def __lt__(self, other: SimEvent) -> bool:
        """Comparison for heapq ordering (min-heap on *time*)."""
        return self.time < other.time


@dataclass
class PropagationStats:
    """Propagation statistics for a time window."""

    avg_propagation_ms: float = 0.0
    max_propagation_ms: float = 0.0
    p95_propagation_ms: float = 0.0
    message_count: int = 0


@dataclass
class TierMessageBreakdown:
    """Per-tier message counts for hierarchical topology analysis."""

    intra_cluster_msgs: int = 0
    inter_cluster_msgs: int = 0
    central_msgs: int = 0
    gossip_msgs: int = 0


@dataclass
class SwarmCoordinationRunResult:
    """Result of a single simulation run."""

    run_id: int = 0
    config: Optional[SwarmCoordinationConfig] = None
    communication_overhead_percent: float = 0.0
    bottleneck_threshold_nodes: float = 0.0
    coordinator_availability_percent: float = 100.0
    power_variance_percent: float = 0.0
    avg_update_propagation_ms: float = 0.0
    max_update_propagation_ms: float = 0.0
    failed_handoffs: int = 0
    message_drop_rate: float = 0.0
    total_messages_sent: int = 0
    total_messages_delivered: int = 0
    avg_messages_per_node_per_day: float = 0.0
    total_energy_kwh: float = 0.0
    coordinator_bandwidth_kbps: float = 0.0
    tier_breakdown: Optional[TierMessageBreakdown] = None
    exception_telemetry_reduction: float = 1.0
    """Ratio of actual to expected messages under exception telemetry (1.0 = no reduction)."""
    message_loss_rate: float = 0.0
    """Fraction of messages lost due to link unavailability (0.0 = no loss)."""
    coordinator_unavailability_events: int = 0
    """Number of times a coordinator's link failed (hierarchical topology)."""
    total_bytes_sent: int = 0
    """Total bytes sent (all message types including baseline ephemeris) in the DES."""
    protocol_bytes_sent: int = 0
    """Protocol bytes sent (excluding baseline ephemeris) in the DES."""
    coordinator_drops: int = 0
    """Messages dropped due to coordinator bandwidth saturation."""
    retransmission_count: int = 0
    """Total retransmission attempts made."""
    total_bytes_attempted: int = 0
    """Total bytes attempted (including retransmissions) -- offered load."""
    protocol_bytes_attempted: int = 0
    """Protocol bytes attempted (including retransmissions) -- offered load."""
    aoi_mean_seconds: float = 0.0
    """Mean Age-of-Information at coordinators (seconds since last status update)."""
    aoi_p99_seconds: float = 0.0
    """99th-percentile Age-of-Information at coordinators."""
    aoi_max_seconds: float = 0.0
    """Maximum Age-of-Information observed at any coordinator."""
    aoi_samples: int = 0
    """Number of AoI samples collected."""
    # Per-message-class byte decomposition
    ephemeris_bytes_sent: int = 0
    """Ephemeris bytes sent (256 B per report)."""
    heartbeat_bytes_sent: int = 0
    """Heartbeat/ACK bytes sent (32 B sectorized, 64 B hierarchical)."""
    command_bytes_sent: int = 0
    """Coordination command bytes sent (512 B per command)."""
    summary_bytes_sent: int = 0
    """Cluster + region summary bytes sent (512 B + 1024 B)."""
    alert_bytes_sent: int = 0
    """Collision alert bytes sent (128 B each)."""
    gossip_bytes_sent: int = 0
    """Gossip bytes sent (128 B per exchange, mesh topologies)."""
    # AoI-to-ephemeris coupling
    aoi_mean_position_error_m: float = 0.0
    """Mean along-track position uncertainty from AoI (metres)."""
    # Airtime enforcement metrics
    airtime_utilization_mean: float = 0.0
    """Mean fraction of T_c consumed by message airtime (0 if enforce_airtime=False)."""
    airtime_deadline_misses: int = 0
    """Number of cycles where cumulative airtime exceeded T_c."""
    airtime_limited_delivery: float = 0.0
    """Delivery rate with airtime enforcement applied (0 if enforce_airtime=False)."""
    # Distributed workload metrics
    distributed_consensus_bytes: int = 0
    """Total bytes consumed by distributed consensus traffic."""
    aoi_p99_position_error_m: float = 0.0
    """P99 along-track position uncertainty from AoI (metres)."""
    # Cross-cycle recovery tracking (GE correlated loss)
    cross_cycle_recovery_mean: float = 0.0
    """Mean number of consecutive failed cycles before successful delivery."""
    cross_cycle_recovery_p95: float = 0.0
    """95th percentile of consecutive failed cycles before recovery."""
    cross_cycle_recovery_count: int = 0
    """Number of recovery events observed (transitions from >=1 failed cycles to success)."""
    cross_cycle_max_streak: int = 0
    """Maximum consecutive failed cycles observed for any member."""
    cross_cycle_recovery_rate_by_cycle: list[float] = field(default_factory=list)
    """Cumulative recovery fraction at each cycle count [1, 2, ..., 10]."""
    coordinator_ingress_bytes_per_cycle: list[int] = field(default_factory=list)
    """Per-cycle coordinator ingress bytes (summed across all coordinators)."""


@dataclass
class NetworkStructure:
    """Network structure produced by topology initialization."""

    nodes: list[SwarmNode]
    clusters: list[Cluster]
    central_coordinator_id: str
    mesh_neighbors: Optional[dict[str, list[str]]] = None

    def __post_init__(self) -> None:
        self.rebuild_indices()

    def rebuild_indices(self) -> None:
        """Build O(1) lookup dicts for nodes and clusters."""
        self._node_map: dict[str, int] = {
            n.id: i for i, n in enumerate(self.nodes)
        }
        self._cluster_map: dict[str, int] = {
            c.id: i for i, c in enumerate(self.clusters)
        }

    def get_node(self, node_id: str) -> Optional["SwarmNode"]:
        """O(1) node lookup by ID."""
        idx = self._node_map.get(node_id)
        return self.nodes[idx] if idx is not None else None

    def get_cluster(self, cluster_id: str) -> Optional["Cluster"]:
        """O(1) cluster lookup by ID."""
        idx = self._cluster_map.get(cluster_id)
        return self.clusters[idx] if idx is not None else None


@dataclass
class HandoffResult:
    """Result of a coordinator handoff attempt."""

    success: bool
    cluster: Cluster
    nodes: list[SwarmNode]
    new_coordinator_id: Optional[str] = None


# ---------------------------------------------------------------------------
# Message-passing helpers
# ---------------------------------------------------------------------------
def light_time_delay(distance_km: float) -> float:
    """Return one-way light-time delay in milliseconds."""
    return (distance_km / SPEED_OF_LIGHT_KM_S) * 1_000


def calculate_bandwidth_requirement(
    topology: CoordinationTopology,
    node_count: int,
    cluster_size: int,
    update_interval_seconds: float,
) -> float:
    """Return required bandwidth in kbps for the given topology and node count."""
    ephemeris_size = MESSAGE_SIZES["ephemeris"]

    if topology == "centralized":
        messages_per_second = node_count / update_interval_seconds
        bits_per_second = messages_per_second * ephemeris_size * 8
        return bits_per_second / 1_000

    if topology == "hierarchical":
        num_clusters = math.ceil(node_count / cluster_size)
        num_regions = math.ceil(num_clusters / 10)
        # Intra-cluster: each member sends 256-byte ephemeris to coordinator
        cluster_msgs = node_count / update_interval_seconds
        cluster_bps = cluster_msgs * ephemeris_size * 8
        # Cluster->Region: coordinator sends a single compressed cluster summary
        region_msgs = num_clusters / update_interval_seconds
        region_bps = region_msgs * MESSAGE_SIZES["cluster_summary"] * 8
        # Region->Central: regional coordinator sends a single region summary
        central_msgs = num_regions / update_interval_seconds
        central_bps = central_msgs * MESSAGE_SIZES["region_summary"] * 8
        total_bps = cluster_bps + region_bps + central_bps
        return total_bps / 1_000

    if topology == "sectorized_mesh":
        # Sectorized mesh: nodes partitioned into sectors of size ~sqrt(N).
        # Traffic model:
        #  1. Each node sends ONE status report (256 B) to its sector coordinator
        #     per cycle (same as hierarchical intra-cluster).
        #  2. Each node exchanges heartbeats with f_gossip sector neighbors.
        #     Heartbeat = 8 B (node ID + status flags).  f_gossip = min(sector_k-1, 10).
        #  3. Sector coordinators relay compressed summaries (512 B) to adjacent
        #     sectors (2 adjacent sectors per coordinator).
        #
        # Per-node bytes/cycle = 256 (status) + f_gossip * 8 (heartbeats)
        # Per-coordinator bytes/cycle += 2 * 512 (inter-sector relay)
        sector_k = cluster_size if cluster_size > 0 else math.ceil(math.sqrt(node_count))
        n_sectors = max(1, math.ceil(node_count / sector_k))
        f_gossip = min(sector_k - 1, 10)  # cap gossip fanout
        heartbeat_size = MESSAGE_SIZES["heartbeat"]  # 32 bytes
        status_bytes = node_count * ephemeris_size  # 256 B per node
        heartbeat_bytes = node_count * f_gossip * heartbeat_size
        inter_sector_bytes = n_sectors * 2 * MESSAGE_SIZES.get("cluster_summary", 512)
        total_bytes_per_cycle = status_bytes + heartbeat_bytes + inter_sector_bytes
        total_bps = total_bytes_per_cycle * 8 / update_interval_seconds
        return total_bps / 1_000

    # mesh (global state)
    gossip_fanout = min(5, math.ceil(math.log2(node_count)))
    gossip_rounds = math.ceil(math.log2(node_count))
    messages_per_round = node_count * gossip_fanout
    rounds_per_second = 1.0 / update_interval_seconds
    messages_per_second = messages_per_round * rounds_per_second / gossip_rounds
    bits_per_second = messages_per_second * MESSAGE_SIZES["gossip"] * 8
    return bits_per_second / 1_000


def calculate_propagation_delay(
    topology: CoordinationTopology,
    node_count: int,
    cluster_size: int,
    processing_delay_ms: float = 1.0,
) -> float:
    """Return expected message propagation delay in milliseconds."""
    if topology == "centralized":
        return light_time_delay(CENTRAL_DISTANCE_KM) * 2 + processing_delay_ms

    if topology == "hierarchical":
        num_clusters = math.ceil(node_count / cluster_size)
        hops = 1 + math.ceil(math.log10(max(1, num_clusters)))
        local_delay = light_time_delay(INTER_NODE_DISTANCE_KM)
        regional_delay = light_time_delay(REGIONAL_DISTANCE_KM)
        return local_delay + regional_delay * (hops - 1) + processing_delay_ms * hops

    if topology == "sectorized_mesh":
        # Sectorized: information propagates via sector-to-sector relay.
        # With sector_size ~ sqrt(N), need ~sqrt(N) hops for global coverage.
        sector_k = cluster_size if cluster_size > 0 else math.ceil(math.sqrt(node_count))
        n_sectors = math.ceil(node_count / max(1, sector_k))
        hops = math.ceil(math.sqrt(max(1, n_sectors)))
        hop_delay = light_time_delay(INTER_NODE_DISTANCE_KM) + processing_delay_ms
        return hops * hop_delay

    # mesh (global state)
    gossip_rounds = math.ceil(math.log2(node_count))
    round_delay = light_time_delay(INTER_NODE_DISTANCE_KM) + processing_delay_ms
    return gossip_rounds * round_delay


def calculate_communication_overhead(
    required_kbps: float,
    bandwidth_per_node_kbps: float,
    node_count: int,
) -> float:
    """Return communication overhead as a percentage of total capacity."""
    total_capacity_kbps = bandwidth_per_node_kbps * node_count
    return (required_kbps / total_capacity_kbps) * 100


def per_coordinator_bandwidth_kbps(
    cluster_size: int,
    update_interval_seconds: float = 10.0,
) -> float:
    """Return the peak bandwidth required by a single cluster coordinator (kbps).

    A coordinator receives *cluster_size* ephemeris messages per interval from
    its members and sends one compressed cluster summary upstream.  This
    function returns the peak inbound + outbound rate.
    """
    ephemeris_size = MESSAGE_SIZES["ephemeris"]
    # Inbound: cluster_size ephemeris messages per interval
    inbound_bps = (cluster_size * ephemeris_size * 8) / update_interval_seconds
    # Outbound: one compressed cluster summary per interval
    outbound_bps = (MESSAGE_SIZES["cluster_summary"] * 8) / update_interval_seconds
    return (inbound_bps + outbound_bps) / 1_000


def create_message(
    sender_id: str,
    receiver_id: str,
    message_type: str,
    send_time: float,
) -> Message:
    """Create a new network message."""
    return Message(
        id=f"msg-{sender_id}-{receiver_id}-{send_time:.3f}",
        sender_id=sender_id,
        receiver_id=receiver_id,
        size_bytes=MESSAGE_SIZES.get(message_type, MESSAGE_SIZES["ephemeris"]),
        send_time=send_time,
        delivered=False,
        message_type=message_type,
    )


def estimate_message_count(
    topology: CoordinationTopology,
    node_count: int,
    cluster_size: int,
    duration_seconds: float,
    update_interval_seconds: float,
) -> int:
    """Estimate total message count for the given topology over *duration_seconds*."""
    updates = math.ceil(duration_seconds / update_interval_seconds)

    if topology == "centralized":
        return node_count * updates

    if topology == "hierarchical":
        num_clusters = math.ceil(node_count / cluster_size)
        num_regions = math.ceil(num_clusters / 10)
        return (node_count + num_clusters + num_regions) * updates

    if topology == "sectorized_mesh":
        sector_k = cluster_size if cluster_size > 0 else math.ceil(math.sqrt(node_count))
        return node_count * sector_k * updates

    # mesh (global state)
    gossip_fanout = min(5, math.ceil(math.log2(node_count)))
    gossip_rounds = math.ceil(math.log2(node_count))
    return node_count * gossip_fanout * gossip_rounds * updates


# ---------------------------------------------------------------------------
# MessageQueue
# ---------------------------------------------------------------------------
class MessageQueue:
    """FIFO message queue with congestion modelling and drop tracking."""

    def __init__(self, max_queue_size: int = 10_000) -> None:
        self._queue: list[Message] = []
        self._total_processed: int = 0
        self._total_dropped: int = 0
        self._propagation_times: list[float] = []
        self._max_queue_size: int = max_queue_size

    # -- mutators ----------------------------------------------------------
    def is_full(self) -> bool:
        """Return ``True`` if the queue has reached its capacity."""
        return len(self._queue) >= self._max_queue_size

    def enqueue(self, message: Message) -> bool:
        """Add *message* to the queue.  Returns ``False`` if dropped."""
        if len(self._queue) >= self._max_queue_size:
            self._total_dropped += 1
            return False
        self._queue.append(message)
        return True

    def dequeue(self, current_time: float) -> Optional[Message]:
        """Dequeue the oldest message, mark it delivered at *current_time*."""
        if not self._queue:
            return None
        self._queue.sort(key=lambda m: m.send_time)
        message = self._queue.pop(0)
        message.receive_time = current_time
        message.delivered = True
        self._total_processed += 1
        propagation_ms = (current_time - message.send_time) * 1_000
        self._propagation_times.append(propagation_ms)
        return message

    def process_messages(
        self,
        current_time: float,
        bandwidth_bps: float,
        duration_seconds: float,
    ) -> list[Message]:
        """Process messages up to the bandwidth limit over *duration_seconds*."""
        processed: list[Message] = []
        bytes_processed = 0.0
        max_bytes = (bandwidth_bps * duration_seconds) / 8.0

        while self._queue and bytes_processed < max_bytes:
            front = self._queue[0]
            if bytes_processed + front.size_bytes > max_bytes:
                break
            msg = self.dequeue(current_time)
            if msg is not None:
                processed.append(msg)
                bytes_processed += msg.size_bytes
        return processed

    # -- queries -----------------------------------------------------------
    def size(self) -> int:
        """Return the current queue depth."""
        return len(self._queue)

    def get_stats(self) -> dict[str, float]:
        """Return processed / dropped / dropRate statistics."""
        total = self._total_processed + self._total_dropped
        return {
            "processed": self._total_processed,
            "dropped": self._total_dropped,
            "dropRate": self._total_dropped / total if total > 0 else 0.0,
        }

    def get_propagation_stats(self) -> PropagationStats:
        """Return propagation-time statistics across delivered messages."""
        if not self._propagation_times:
            return PropagationStats()
        sorted_times = sorted(self._propagation_times)
        total = sum(sorted_times)
        p95_idx = int(len(sorted_times) * 0.95)
        return PropagationStats(
            avg_propagation_ms=total / len(sorted_times),
            max_propagation_ms=sorted_times[-1],
            p95_propagation_ms=sorted_times[p95_idx],
            message_count=len(sorted_times),
        )

    def clear(self) -> None:
        """Remove all messages from the queue (stats are kept)."""
        self._queue.clear()


# ---------------------------------------------------------------------------
# Coordinator model helpers
# ---------------------------------------------------------------------------
def create_node(
    node_id: str,
    cluster_id: str,
    is_coordinator: bool = False,
) -> "SwarmNode":
    """Create a new :class:`SwarmNode`."""
    return SwarmNode(
        id=node_id,
        status="coordinator" if is_coordinator else "operational",
        cluster_id=cluster_id,
        is_coordinator=is_coordinator,
    )


def create_cluster(
    cluster_id: str,
    node_count: int,
    coordinator_node_id: str,
) -> tuple["Cluster", list["SwarmNode"]]:
    """Create a :class:`Cluster` with *node_count* nodes.

    Returns a ``(cluster, nodes)`` tuple.
    """
    nodes: list[SwarmNode] = []
    for i in range(node_count):
        nid = f"{cluster_id}-node-{i}"
        is_coord = nid == coordinator_node_id
        nodes.append(create_node(nid, cluster_id, is_coord))

    # Ensure at least one coordinator exists
    if not any(n.is_coordinator for n in nodes) and nodes:
        nodes[0].is_coordinator = True
        nodes[0].status = "coordinator"

    coord_id = next(
        (n.id for n in nodes if n.is_coordinator),
        nodes[0].id if nodes else coordinator_node_id,
    )
    cluster = Cluster(
        id=cluster_id,
        node_ids=[n.id for n in nodes],
        coordinator_id=coord_id,
    )
    return cluster, nodes


def calculate_power_consumption(
    node: SwarmNode,
    duration_seconds: float,
    base_power_w: float,
    coordinator_power_w: float,
) -> float:
    """Return energy consumed (Wh) by *node* over *duration_seconds*."""
    hours = duration_seconds / 3600.0
    power = coordinator_power_w if node.is_coordinator else base_power_w
    return power * hours


def update_node_power(
    node: SwarmNode,
    duration_seconds: float,
    base_power_w: float,
    coordinator_power_w: float,
) -> "SwarmNode":
    """Return a copy of *node* with updated power and coordinator time."""
    power_wh = calculate_power_consumption(
        node, duration_seconds, base_power_w, coordinator_power_w
    )
    new = SwarmNode(
        id=node.id,
        status=node.status,
        cluster_id=node.cluster_id,
        is_coordinator=node.is_coordinator,
        coordinator_time_seconds=(
            node.coordinator_time_seconds + duration_seconds
            if node.is_coordinator
            else node.coordinator_time_seconds
        ),
        power_consumed_wh=node.power_consumed_wh + power_wh,
        messages_sent=node.messages_sent,
        messages_received=node.messages_received,
        last_update_time=node.last_update_time,
        failure_time=node.failure_time,
    )
    return new


def calculate_coordinator_availability(
    cluster: Cluster,
    nodes: list[SwarmNode],
    simulation_duration_seconds: float,
) -> float:
    """Return coordinator availability as a percentage (0--100)."""
    total_coord_time = sum(
        n.coordinator_time_seconds
        for n in nodes
        if n.cluster_id == cluster.id
    )
    expected_time = simulation_duration_seconds
    handoff_gap_seconds = cluster.failed_handoffs * HANDOFF_TIMEOUT_SECONDS
    effective = min(total_coord_time - handoff_gap_seconds, expected_time)
    return (effective / expected_time) * 100.0


def perform_handoff(
    cluster: Cluster,
    nodes: list[SwarmNode],
    current_time: float,
    rng: Generator,
) -> "HandoffResult":
    """Attempt a coordinator handoff.  Returns a :class:`HandoffResult`."""
    # Find eligible candidates
    candidates = [
        n
        for n in nodes
        if n.cluster_id == cluster.id
        and n.status == "operational"
        and n.id != cluster.coordinator_id
    ]

    if not candidates:
        new_cluster = Cluster(
            id=cluster.id,
            node_ids=list(cluster.node_ids),
            coordinator_id=cluster.coordinator_id,
            regional_coordinator_id=cluster.regional_coordinator_id,
            messages_processed=cluster.messages_processed,
            last_handoff_time=current_time,
            failed_handoffs=cluster.failed_handoffs + 1,
        )
        return HandoffResult(
            success=False, cluster=new_cluster, nodes=nodes, new_coordinator_id=None
        )

    candidates.sort(key=lambda n: n.coordinator_time_seconds)
    new_coord = candidates[0]

    # 1 % random handoff failure
    if rng.random() < 0.01:
        new_cluster = Cluster(
            id=cluster.id,
            node_ids=list(cluster.node_ids),
            coordinator_id=cluster.coordinator_id,
            regional_coordinator_id=cluster.regional_coordinator_id,
            messages_processed=cluster.messages_processed,
            last_handoff_time=current_time,
            failed_handoffs=cluster.failed_handoffs + 1,
        )
        return HandoffResult(
            success=False, cluster=new_cluster, nodes=nodes, new_coordinator_id=None
        )

    # Successful handoff
    updated_nodes: list[SwarmNode] = []
    for n in nodes:
        if n.id == cluster.coordinator_id:
            updated_nodes.append(
                SwarmNode(
                    id=n.id,
                    status="operational",
                    cluster_id=n.cluster_id,
                    is_coordinator=False,
                    coordinator_time_seconds=n.coordinator_time_seconds,
                    power_consumed_wh=n.power_consumed_wh,
                    messages_sent=n.messages_sent,
                    messages_received=n.messages_received,
                    last_update_time=n.last_update_time,
                    failure_time=n.failure_time,
                )
            )
        elif n.id == new_coord.id:
            updated_nodes.append(
                SwarmNode(
                    id=n.id,
                    status="coordinator",
                    cluster_id=n.cluster_id,
                    is_coordinator=True,
                    coordinator_time_seconds=n.coordinator_time_seconds,
                    power_consumed_wh=n.power_consumed_wh,
                    messages_sent=n.messages_sent,
                    messages_received=n.messages_received,
                    last_update_time=n.last_update_time,
                    failure_time=n.failure_time,
                )
            )
        else:
            updated_nodes.append(n)

    new_cluster = Cluster(
        id=cluster.id,
        node_ids=list(cluster.node_ids),
        coordinator_id=new_coord.id,
        regional_coordinator_id=cluster.regional_coordinator_id,
        messages_processed=cluster.messages_processed,
        last_handoff_time=current_time,
        failed_handoffs=cluster.failed_handoffs,
    )
    return HandoffResult(
        success=True,
        cluster=new_cluster,
        nodes=updated_nodes,
        new_coordinator_id=new_coord.id,
    )


def calculate_power_variance(nodes: list[SwarmNode]) -> float:
    """Return the coefficient of variation of power consumption (percent)."""
    if not nodes:
        return 0.0
    powers = np.array([n.power_consumed_wh for n in nodes])
    mean_p = powers.mean()
    return 0.0 if mean_p == 0.0 else 100.0 * (powers.std() / mean_p)


def fail_node(node: SwarmNode, failure_time: float) -> SwarmNode:
    """Return a copy of *node* in ``failed`` status."""
    return SwarmNode(
        id=node.id,
        status="failed",
        cluster_id=node.cluster_id,
        is_coordinator=False,
        coordinator_time_seconds=node.coordinator_time_seconds,
        power_consumed_wh=node.power_consumed_wh,
        messages_sent=node.messages_sent,
        messages_received=node.messages_received,
        last_update_time=node.last_update_time,
        failure_time=failure_time,
    )


def needs_handoff(
    cluster: Cluster,
    current_time: float,
    duty_cycle_seconds: float,
) -> bool:
    """Return ``True`` if the cluster's coordinator needs to hand off."""
    return current_time - cluster.last_handoff_time >= duty_cycle_seconds


def get_operational_nodes(
    nodes: list[SwarmNode],
    cluster_id: str,
) -> list[SwarmNode]:
    """Return operational or coordinator-status nodes in the given cluster."""
    return [
        n
        for n in nodes
        if n.cluster_id == cluster_id and n.status in ("operational", "coordinator")
    ]


def calculate_handoff_time(bandwidth_kbps: float) -> float:
    """Return handoff duration in seconds given *bandwidth_kbps*."""
    transfer_time = (HANDOFF_STATE_SIZE_BYTES * 8) / (bandwidth_kbps * 1_000)
    verification_time = HANDOFF_VERIFICATION_ROUNDS * 0.1
    return transfer_time + verification_time


def calculate_total_energy(nodes: list[SwarmNode]) -> float:
    """Return total energy consumed by all nodes in kWh."""
    return sum(n.power_consumed_wh for n in nodes) / 1_000.0


# ---------------------------------------------------------------------------
# Topology initialization and routing
# ---------------------------------------------------------------------------
def _initialize_centralized(node_count: int) -> NetworkStructure:
    """Build a centralized network where all nodes talk to one coordinator."""
    nodes: list[SwarmNode] = []
    cluster_id = "central"
    central_id = "central-coordinator"
    nodes.append(create_node(central_id, cluster_id, True))
    for i in range(node_count - 1):
        nodes.append(create_node(f"node-{i}", cluster_id, False))
    cluster = Cluster(
        id=cluster_id,
        node_ids=[n.id for n in nodes],
        coordinator_id=central_id,
    )
    return NetworkStructure(
        nodes=nodes, clusters=[cluster], central_coordinator_id=central_id
    )


def _initialize_hierarchical(
    node_count: int, cluster_size: int, rng: Generator
) -> NetworkStructure:
    """Build a hierarchical network with cluster and regional coordinators."""
    nodes: list[SwarmNode] = []
    clusters: list[Cluster] = []
    num_clusters = math.ceil(node_count / cluster_size)
    regional_coordinators: list[str] = []

    node_index = 0
    for c in range(num_clusters):
        region_id = c // 10
        cid = f"cluster-{c}"
        n_in_cluster = min(cluster_size, node_count - node_index)
        coord_id = f"{cid}-node-0"
        cluster, cluster_nodes = create_cluster(cid, n_in_cluster, coord_id)

        if c % 10 == 0:
            regional_coordinators.append(coord_id)
            cluster.regional_coordinator_id = coord_id
        else:
            if region_id < len(regional_coordinators):
                cluster.regional_coordinator_id = regional_coordinators[region_id]

        nodes.extend(cluster_nodes)
        clusters.append(cluster)
        node_index += n_in_cluster

    central_id = regional_coordinators[0] if regional_coordinators else (
        nodes[0].id if nodes else "central-0"
    )
    return NetworkStructure(
        nodes=nodes, clusters=clusters, central_coordinator_id=central_id
    )


def _initialize_mesh(
    node_count: int, rng: Generator
) -> NetworkStructure:
    """Build a mesh network with random gossip neighbours."""
    nodes: list[SwarmNode] = []
    for i in range(node_count):
        nid = f"mesh-node-{i}"
        nodes.append(create_node(nid, "mesh", False))

    gossip_fanout = min(5, math.ceil(math.log2(node_count)))
    mesh_neighbors: dict[str, list[str]] = {}

    for node in nodes:
        candidates = [n.id for n in nodes if n.id != node.id]
        k = min(gossip_fanout, len(candidates))
        chosen_indices = rng.choice(len(candidates), size=k, replace=False)
        mesh_neighbors[node.id] = [candidates[idx] for idx in chosen_indices]

    central_id = nodes[0].id if nodes else "mesh-node-0"
    cluster = Cluster(
        id="mesh",
        node_ids=[n.id for n in nodes],
        coordinator_id=central_id,
    )
    return NetworkStructure(
        nodes=nodes,
        clusters=[cluster],
        central_coordinator_id=central_id,
        mesh_neighbors=mesh_neighbors,
    )


def _initialize_sectorized_mesh(
    node_count: int, sector_size: int, rng: Generator
) -> NetworkStructure:
    """Build a sectorized mesh where each node gossips with nearest neighbors.

    Nodes are assigned to sectors of size *sector_size*.  Each node's gossip
    neighbors are all nodes in the same sector (local gossip).  Inter-sector
    relay is handled by boundary nodes that also gossip with adjacent sectors.

    This models a spatially-partitioned gossip protocol where each node
    communicates with O(sqrt(N)) orbital neighbors, yielding O(N * sqrt(N))
    = O(N^{3/2}) total messages per cycle.
    """
    nodes: list[SwarmNode] = []
    for i in range(node_count):
        nid = f"sector-node-{i}"
        nodes.append(create_node(nid, "sector-0", False))

    # Assign nodes to sectors based on index (modeling orbital proximity)
    n_sectors = math.ceil(node_count / max(1, sector_size))
    sectors: list[list[int]] = [[] for _ in range(n_sectors)]
    for i in range(node_count):
        sector_idx = i // max(1, sector_size)
        if sector_idx >= n_sectors:
            sector_idx = n_sectors - 1
        sectors[sector_idx].append(i)
        nodes[i] = create_node(f"sector-node-{i}", f"sector-{sector_idx}", False)

    # Build neighbor map: intra-sector + adjacent sector boundary nodes
    mesh_neighbors: dict[str, list[str]] = {}
    for s_idx, sector_members in enumerate(sectors):
        for node_idx in sector_members:
            nid = nodes[node_idx].id
            neighbors: list[str] = []
            # Intra-sector: all other nodes in same sector
            for other_idx in sector_members:
                if other_idx != node_idx:
                    neighbors.append(nodes[other_idx].id)
            # Inter-sector: boundary nodes of adjacent sectors
            for adj_s in [s_idx - 1, s_idx + 1]:
                if 0 <= adj_s < n_sectors and adj_s != s_idx:
                    adj_members = sectors[adj_s]
                    if adj_members:
                        # Connect to the nearest boundary node
                        boundary_idx = adj_members[-1] if adj_s < s_idx else adj_members[0]
                        neighbors.append(nodes[boundary_idx].id)
            mesh_neighbors[nid] = neighbors

    central_id = nodes[0].id if nodes else "sector-node-0"
    # Create one cluster per sector for tracking; mark sector coordinators
    clusters: list[Cluster] = []
    for s_idx, sector_members in enumerate(sectors):
        cid = f"sector-{s_idx}"
        coord_idx = sector_members[0] if sector_members else 0
        nodes[coord_idx].is_coordinator = True
        nodes[coord_idx].status = "coordinator"
        cluster = Cluster(
            id=cid,
            node_ids=[nodes[i].id for i in sector_members],
            coordinator_id=nodes[coord_idx].id,
        )
        clusters.append(cluster)

    return NetworkStructure(
        nodes=nodes,
        clusters=clusters,
        central_coordinator_id=central_id,
        mesh_neighbors=mesh_neighbors,
    )


def initialize_network(
    config: SwarmCoordinationConfig,
    rng: Generator,
) -> NetworkStructure:
    """Dispatch to the appropriate topology initializer."""
    topo = config.coordination_topology
    if topo == "centralized":
        return _initialize_centralized(config.node_count)
    if topo == "hierarchical":
        return _initialize_hierarchical(config.node_count, config.cluster_size, rng)
    if topo == "sectorized_mesh":
        sector_k = config.sector_size if config.sector_size > 0 else math.ceil(math.sqrt(config.node_count))
        return _initialize_sectorized_mesh(config.node_count, sector_k, rng)
    return _initialize_mesh(config.node_count, rng)


# -- routing ---------------------------------------------------------------
def _centralized_routing(
    network: NetworkStructure,
    source_node_id: str,
) -> list[tuple[str, str]]:
    """Centralized: all messages go to / from the central coordinator."""
    if source_node_id == network.central_coordinator_id:
        return [
            (source_node_id, n.id)
            for n in network.nodes
            if n.id != source_node_id and n.status != "failed"
        ]
    return [(source_node_id, network.central_coordinator_id)]


def _hierarchical_routing(
    network: NetworkStructure,
    source_node_id: str,
) -> list[tuple[str, str]]:
    """Hierarchical: upward aggregation routes.

    - Regular node → cluster coordinator (ephemeris, 256 B)
    - Cluster coordinator → regional coordinator (cluster_summary, 512 B)
    - Regional coordinator → central coordinator (region_summary, 1024 B)

    Downward dissemination (coordination commands, 512 B per member) is
    handled via batch accounting in ``_handle_state_sync`` to avoid
    generating O(k_c) individual events per coordinator per cycle.
    """
    routes: list[tuple[str, str]] = []
    source = network.get_node(source_node_id)
    if source is None:
        return routes
    cluster = network.get_cluster(source.cluster_id) if source.cluster_id else None
    if cluster is None:
        return routes

    if source_node_id == cluster.coordinator_id:
        # --- Upward: coordinator sends summary ---
        if (
            cluster.regional_coordinator_id
            and cluster.regional_coordinator_id != source_node_id
        ):
            # Cluster coordinator → regional coordinator (cluster_summary)
            routes.append((source_node_id, cluster.regional_coordinator_id))
        elif source_node_id != network.central_coordinator_id:
            # Regional coordinator (not central) → central (region_summary)
            routes.append((source_node_id, network.central_coordinator_id))
    else:
        # Regular node sends ephemeris to coordinator
        routes.append((source_node_id, cluster.coordinator_id))
    return routes


def _mesh_routing(
    network: NetworkStructure,
    source_node_id: str,
) -> list[tuple[str, str]]:
    """Mesh: gossip to neighbours."""
    neighbors = (network.mesh_neighbors or {}).get(source_node_id, [])
    return [
        (source_node_id, nid)
        for nid in neighbors
        if (lambda n: n is not None and n.status != "failed")(network.get_node(nid))
    ]


_SECTORIZED_MESH_MAX_GOSSIP: int = 10
"""Maximum gossip neighbors per state_sync event for sectorized mesh.

In the proper sectorized mesh model, each node sends heartbeats (8 B) to
min(sector_k - 1, 10) neighbors per cycle.  This cap limits per-event
routing to keep the DES tractable while matching the analytical model.
"""


def _sectorized_mesh_routing(
    network: NetworkStructure,
    source_node_id: str,
) -> list[tuple[str, str]]:
    """Sectorized mesh: status to sector coordinator + heartbeats to neighbors.

    Returns routes for:
    1. Status report (ephemeris, 256 B) to the sector coordinator
    2. Heartbeats (32 B) to up to _SECTORIZED_MESH_MAX_GOSSIP other neighbors

    Coordination commands from sector coordinator to members are handled
    via batch accounting in ``_handle_state_sync``.

    The sector coordinator route is placed first so that
    ``_classify_message_type`` can distinguish it (ephemeris) from peer
    heartbeats.
    """
    source = network.get_node(source_node_id)
    if source is None:
        return []
    cluster = network.get_cluster(source.cluster_id) if source.cluster_id else None

    routes: list[tuple[str, str]] = []
    # 1. Status report to sector coordinator (unless we ARE the coordinator)
    if cluster and cluster.coordinator_id != source_node_id:
        coord_node = network.get_node(cluster.coordinator_id)
        if coord_node and coord_node.status != "failed":
            routes.append((source_node_id, cluster.coordinator_id))

    # 2. Heartbeats to mesh neighbors (excluding coordinator, already added)
    neighbors = (network.mesh_neighbors or {}).get(source_node_id, [])
    coord_id = cluster.coordinator_id if cluster else None
    live = [
        nid for nid in neighbors
        if nid != coord_id
        and (lambda n: n is not None and n.status != "failed")(network.get_node(nid))
    ]
    routes.extend(
        (source_node_id, nid) for nid in live[:_SECTORIZED_MESH_MAX_GOSSIP]
    )
    return routes


def get_message_routing(
    topology: CoordinationTopology,
    network: NetworkStructure,
    source_node_id: str,
) -> list[tuple[str, str]]:
    """Return ``(sender, receiver)`` pairs for an update from *source_node_id*."""
    if topology == "centralized":
        return _centralized_routing(network, source_node_id)
    if topology == "hierarchical":
        return _hierarchical_routing(network, source_node_id)
    if topology == "sectorized_mesh":
        return _sectorized_mesh_routing(network, source_node_id)
    return _mesh_routing(network, source_node_id)


def get_hop_count(
    topology: CoordinationTopology,
    node_count: int,
    cluster_size: int,
) -> int:
    """Return the number of hops for message propagation."""
    if topology == "centralized":
        return 2
    if topology == "hierarchical":
        num_clusters = math.ceil(node_count / cluster_size)
        levels = 1 + math.ceil(math.log10(max(1, num_clusters)))
        return levels * 2
    if topology == "sectorized_mesh":
        sector_k = cluster_size if cluster_size > 0 else math.ceil(math.sqrt(node_count))
        n_sectors = math.ceil(node_count / max(1, sector_k))
        return math.ceil(math.sqrt(max(1, n_sectors)))
    # mesh (global state)
    return math.ceil(math.log2(node_count))


def estimate_bottleneck_threshold(
    topology: CoordinationTopology,
    cluster_size: int,
    bandwidth_per_node_kbps: float,
) -> float:
    """Estimate the node count at which latency exceeds 1 second."""
    target_latency_ms = 1_000.0
    processing_delay_ms = 1.0

    if topology == "centralized":
        msgs_per_sec = (bandwidth_per_node_kbps * 1_000) / (
            MESSAGE_SIZES["ephemeris"] * 8
        )
        return math.floor(msgs_per_sec * (target_latency_ms / 1_000))

    if topology == "hierarchical":
        msgs_per_sec = (bandwidth_per_node_kbps * 1_000) / (
            MESSAGE_SIZES["ephemeris"] * 8
        )
        coordinator_capacity = msgs_per_sec * (target_latency_ms / 1_000)
        return coordinator_capacity * cluster_size * 100

    if topology == "sectorized_mesh":
        sector_k = cluster_size if cluster_size > 0 else math.ceil(math.sqrt(1_000_000))
        hop_time_ms = light_time_delay(INTER_NODE_DISTANCE_KM) + processing_delay_ms
        max_hops = target_latency_ms / hop_time_ms
        return (max_hops ** 2) * sector_k

    # mesh (global state)
    round_time_ms = 10.0 + processing_delay_ms
    max_rounds = target_latency_ms / round_time_ms
    return 2.0 ** max_rounds


# ---------------------------------------------------------------------------
# EventQueue (min-heap on event.time)
# ---------------------------------------------------------------------------
class EventQueue:
    """Priority queue of :class:`SimEvent` objects backed by a binary heap."""

    def __init__(self) -> None:
        self._heap: list[SimEvent] = []

    def push(self, event: SimEvent) -> None:
        """Add an event to the queue."""
        heapq.heappush(self._heap, event)

    def pop(self) -> Optional[SimEvent]:
        """Remove and return the earliest event, or ``None`` if empty."""
        if not self._heap:
            return None
        return heapq.heappop(self._heap)

    def peek(self) -> Optional[SimEvent]:
        """Return the earliest event without removing it."""
        return self._heap[0] if self._heap else None

    def is_empty(self) -> bool:
        return len(self._heap) == 0

    def size(self) -> int:
        return len(self._heap)


# ---------------------------------------------------------------------------
# Discrete-event simulator
# ---------------------------------------------------------------------------
class SwarmCoordinationSimulator:
    """Discrete-event simulator for swarm coordination.

    Instantiate with a :class:`SwarmCoordinationConfig` and call
    :meth:`run` to execute the simulation, which returns a
    :class:`SwarmCoordinationRunResult`.
    """

    def __init__(self, config: SwarmCoordinationConfig) -> None:
        self.config = config
        self.rng: Generator = np.random.default_rng(config.seed)
        self.event_queue = EventQueue()
        self.simulation_duration_seconds: float = (
            config.simulation_days * SECONDS_PER_DAY
        )
        self.duty_cycle_seconds: float = config.coordinator_duty_cycle_hours * 3600.0

        # Initialize network
        self.network: NetworkStructure = initialize_network(config, self.rng)
        self.message_queue = MessageQueue(config.node_count * 10)
        self.current_time: float = 0.0
        self.total_messages_sent: int = 0
        self.total_messages_delivered: int = 0
        self.propagation_times: list[float] = []
        self._tier_breakdown = TierMessageBreakdown()

        # Exception telemetry tracking
        self._exception_expected_msgs: int = 0
        self._exception_actual_msgs: int = 0

        # Link availability tracking
        self._link_lost_msgs: int = 0
        self._link_attempted_msgs: int = 0
        self._coordinator_unavailability_events: int = 0

        # DES byte tracking for overhead calculation
        self._total_bytes_sent: int = 0
        self._protocol_bytes_sent: int = 0  # excludes baseline ephemeris

        # Coordinator bandwidth tracking
        self._coordinator_drops: int = 0
        # Per-coordinator byte counters reset each sync interval
        self._coordinator_bytes_this_interval: dict[str, float] = {}
        self._coordinator_interval_start: float = 0.0

        # Retransmission tracking
        self._retransmission_count: int = 0
        # Offered-load byte tracking (includes retransmission attempts)
        self._total_bytes_attempted: int = 0
        self._protocol_bytes_attempted: int = 0

        # Per-message-class byte counters for overhead decomposition
        self._ephemeris_bytes_sent: int = 0
        self._heartbeat_bytes_sent: int = 0
        self._command_bytes_sent: int = 0
        self._summary_bytes_sent: int = 0   # cluster + region summaries
        self._alert_bytes_sent: int = 0     # collision alerts
        self._gossip_bytes_sent: int = 0    # mesh/sectorized gossip

        # Age-of-Information (AoI) tracking at coordinators
        # Maps coordinator_id -> {member_node_id -> last_update_time}
        self._coordinator_last_update: dict[str, dict[str, float]] = {}
        # Collected AoI samples (sampled periodically, not every cycle)
        self._aoi_samples: list[float] = []
        self._aoi_sample_interval: float = max(100.0, self.simulation_duration_seconds / 1000)

        # Stdlib RNG seeded from config for exception/link Bernoulli draws
        self._stdlib_rng = _stdlib_random.Random(config.seed)

        # Gilbert-Elliott link state: per-node (True=good, False=bad)
        self._ge_link_states: dict[str, bool] = {}
        if config.link_model == "gilbert_elliott":
            for node in self.network.nodes:
                self._ge_link_states[node.id] = True  # start in good state
        self._ge_last_transition_time: float = 0.0

        # Cross-cycle recovery tracking: per-member consecutive loss streaks
        # Tracks how many consecutive cycles each member's ephemeris failed
        # to reach its coordinator.  Upon successful delivery after >=1 failures,
        # the streak length is recorded for distribution analysis.
        self._member_loss_streak: dict[str, int] = {}
        self._recovery_streaks: list[int] = []

        # Airtime enforcement tracking
        self._airtime_per_cycle: list[float] = []  # ms consumed per cycle
        self._airtime_deadline_misses: int = 0
        self._airtime_delivered: int = 0
        self._airtime_attempted: int = 0
        # Per-coordinator airtime within current cycle
        self._coordinator_airtime_this_cycle: dict[str, float] = {}

        # Distributed consensus traffic tracking
        self._distributed_consensus_bytes: int = 0

        # Per-cycle coordinator ingress tracking (for distributional analysis)
        self._coordinator_ingress_this_cycle: int = 0
        self._coordinator_ingress_per_cycle: list[int] = []

        # ON/OFF Markov campaign state
        self._campaign_on: bool = False  # start OFF
        d = self.config.campaign_duty_factor
        L_on = max(1, self.config.campaign_on_length)
        # Transition probabilities: P(ON→OFF) = 1/L_on, P(OFF→ON) derived from steady-state d
        self._campaign_p_on_to_off = 1.0 / L_on
        if d > 0 and d < 1:
            L_off = L_on * (1.0 - d) / d
            self._campaign_p_off_to_on = 1.0 / max(1.0, L_off)
        elif d >= 1:
            self._campaign_p_off_to_on = 1.0  # always ON
            self._campaign_on = True
        else:
            self._campaign_p_off_to_on = 0.0  # always OFF

        self._initialize_simulation()

    # -- initialization helpers --------------------------------------------
    def _initialize_simulation(self) -> None:
        """Schedule all starting events."""
        self._schedule_state_sync_events(0.0)
        if self.config.coordination_topology == "hierarchical":
            self._schedule_handoff_events(0.0)
        self._schedule_failure_events()
        if self.config.coordination_topology == "mesh":
            self._schedule_gossip_rounds(0.0)

    def _schedule_state_sync_events(self, start_time: float) -> None:
        """Schedule the first batch of state sync events (lazy scheduling).

        Instead of pre-scheduling events for the entire simulation, schedule
        only the first round.  Each handled ``state_sync`` event re-schedules
        the next round for its node via :meth:`_reschedule_state_sync`.

        We use a consistent T_c = 10 s for all topologies (matching the
        reporting rate r = 0.1 msg/s, so T_c = 1/r = 10 s).  For large
        swarms we sample a subset of nodes per round and scale counts
        accordingly in _generate_result().

        Intra-cycle timing depends on ``coordinator_scheduling``:
        - ``"random"``: each node fires at a uniform random phase offset
          within [0, T_c), modeling uncoordinated arrivals (Poisson-like).
        - ``"tdma"``: nodes assigned deterministic TDMA slots within T_c,
          with guard time between slots.  This eliminates burstiness.
        """
        self._sync_interval = 10.0  # T_c = 1/r = 10 s for all topologies
        if self.config.sync_sample_rate > 0.0:
            self._sync_sample_rate = self.config.sync_sample_rate
        else:
            self._sync_sample_rate = min(1.0, 1_000 / self.config.node_count)

        # Build per-cluster node lists for TDMA slot assignment
        is_tdma = self.config.coordinator_scheduling == "tdma"
        cluster_node_idx: dict[str, int] = {}  # per-cluster slot counter

        # Phase-stagger: build cluster-index map for deterministic coordinator offsets
        is_stagger = (
            self.config.enable_phase_stagger
            and self.config.coordination_topology == "hierarchical"
            and not is_tdma
        )
        cluster_phase_offset: dict[str, float] = {}
        if is_stagger:
            n_clusters = len(self.network.clusters)
            for ci, cluster in enumerate(self.network.clusters):
                cluster_phase_offset[cluster.id] = (
                    (ci / max(1, n_clusters)) * self._sync_interval
                )

        for node in self.network.nodes:
            if node.status == "failed":
                continue
            if self.rng.random() >= self._sync_sample_rate:
                continue

            if is_tdma and self.config.coordination_topology == "hierarchical":
                # TDMA: deterministic slot within [0, T_c)
                cid = node.cluster_id or "default"
                slot_idx = cluster_node_idx.get(cid, 0)
                cluster_node_idx[cid] = slot_idx + 1
                gamma = 1.0 - self.config.guard_time_fraction
                slot_duration = self._sync_interval * gamma / max(1, self.config.cluster_size)
                offset = slot_idx * (self._sync_interval / max(1, self.config.cluster_size))
                t = start_time + min(offset, self._sync_interval * 0.99)
            elif is_stagger and node.is_coordinator:
                # Phase-stagger: coordinator fires at deterministic offset
                # based on cluster index to spread regional coordinator inbound
                cid = node.cluster_id or "default"
                offset = cluster_phase_offset.get(cid, 0.0)
                t = start_time + offset
            else:
                # Random phase: uniform random offset within [0, T_c)
                offset = float(self.rng.uniform(0, self._sync_interval))
                t = start_time + offset

            self.event_queue.push(
                SimEvent(
                    type="state_sync",
                    time=t,
                    node_id=node.id,
                    cluster_id=node.cluster_id,
                )
            )

    def _reschedule_state_sync(self, node: "SwarmNode", current_time: float) -> None:
        """Schedule the next state_sync for *node* after the sync interval.

        Once a node is selected during initialisation (with probability
        ``_sync_sample_rate``), it fires every interval for the remainder of
        the simulation.  Re-sampling here would cause exponential decay of
        active nodes, making byte-rate measurements meaningless.

        Under TDMA scheduling, the node fires at the same slot offset every
        cycle (deterministic).  Under random scheduling, it fires at T_c
        intervals from its current time (preserving its random phase).
        """
        # Align next fire time to the next cycle boundary + same offset
        # This preserves TDMA slot assignment or random phase offset
        next_time = current_time + self._sync_interval
        if next_time < self.simulation_duration_seconds:
            self.event_queue.push(
                SimEvent(
                    type="state_sync",
                    time=next_time,
                    node_id=node.id,
                    cluster_id=node.cluster_id,
                )
            )

    def _schedule_handoff_events(self, start_time: float) -> None:
        """Schedule only the first coordinator handoff per cluster (lazy)."""
        t = start_time + self.duty_cycle_seconds
        if t < self.simulation_duration_seconds:
            for cluster in self.network.clusters:
                self.event_queue.push(
                    SimEvent(
                        type="coordinator_handoff",
                        time=t,
                        node_id=cluster.coordinator_id,
                        cluster_id=cluster.id,
                    )
                )

    def _reschedule_handoff(self, cluster_id: str, current_time: float) -> None:
        """Schedule the next coordinator handoff for *cluster_id*."""
        next_time = current_time + self.duty_cycle_seconds
        if next_time < self.simulation_duration_seconds:
            cluster = self.network.get_cluster(cluster_id)
            if cluster is not None:
                self.event_queue.push(
                    SimEvent(
                        type="coordinator_handoff",
                        time=next_time,
                        node_id=cluster.coordinator_id,
                        cluster_id=cluster.id,
                    )
                )

    def _schedule_gossip_rounds(self, start_time: float) -> None:
        """Schedule only the first gossip round (lazy)."""
        self._gossip_interval = 10.0  # Consistent T_c = 10 s across all topologies
        t = start_time
        if t < self.simulation_duration_seconds:
            self.event_queue.push(
                SimEvent(
                    type="gossip_round",
                    time=t,
                    node_id="mesh-coordinator",
                    data={"round": 0},
                )
            )

    def _reschedule_gossip(self, current_time: float, current_round: int) -> None:
        """Schedule the next gossip round."""
        next_time = current_time + self._gossip_interval
        if next_time < self.simulation_duration_seconds:
            self.event_queue.push(
                SimEvent(
                    type="gossip_round",
                    time=next_time,
                    node_id="mesh-coordinator",
                    data={"round": current_round + 1},
                )
            )

    def _schedule_failure_events(self) -> None:
        annual_rate = self.config.node_failure_rate_per_year
        seconds_per_year = 365.0 * 24.0 * 3600.0
        rate_per_second = annual_rate / seconds_per_year

        for node in self.network.nodes:
            if node.is_coordinator:
                continue
            failure_time = self.rng.exponential(1.0 / rate_per_second)
            if failure_time < self.simulation_duration_seconds:
                self.event_queue.push(
                    SimEvent(
                        type="node_failure",
                        time=failure_time,
                        node_id=node.id,
                        cluster_id=node.cluster_id,
                    )
                )

    # -- event loop --------------------------------------------------------
    def run(self) -> SwarmCoordinationRunResult:
        """Execute the full simulation and return the result."""
        events_processed = 0
        # Default max_events accounts for:
        # - sampled_nodes state_sync events per cycle
        # - Each state_sync generates ~routes_per_event message_receive events
        # - Additional handoff, failure, gossip events
        # Cycles per day = 86400 / T_c = 8640 (at T_c=10s).
        if self.config.max_events is not None:
            max_events = self.config.max_events
        else:
            sampled_nodes = max(1, int(self.config.node_count * self._sync_sample_rate))
            cycles_per_day = 86400.0 / 10.0  # T_c = 10s
            # Estimate routes per event: hierarchical/centralized=1, sectorized=10, mesh=5
            if self.config.coordination_topology == "sectorized_mesh":
                events_per_sync = 1 + _SECTORIZED_MESH_MAX_GOSSIP  # state_sync + message_receives
            elif self.config.coordination_topology == "mesh":
                events_per_sync = 6  # gossip_round + ~5 exchanges
            else:
                events_per_sync = 3  # state_sync + ~2 message_receives
            max_events = int(sampled_nodes * cycles_per_day * self.config.simulation_days * events_per_sync * 1.5)
        # Batch power updates: only update when >=60s have elapsed
        last_power_time: float = 0.0
        power_update_interval = 60.0
        # AoI sampling at periodic intervals
        last_aoi_sample_time: float = 0.0
        # Gilbert-Elliott state transitions (once per sync interval)
        last_ge_transition_time: float = 0.0

        while not self.event_queue.is_empty() and events_processed < max_events:
            event = self.event_queue.pop()
            if event is None:
                break
            if event.time > self.simulation_duration_seconds:
                break

            # Batch power updates at intervals instead of every event
            if event.time - last_power_time >= power_update_interval:
                elapsed = event.time - last_power_time
                self._update_power_consumption(elapsed)
                last_power_time = event.time

            # Periodic AoI sampling
            if event.time - last_aoi_sample_time >= self._aoi_sample_interval:
                self._sample_aoi(event.time)
                last_aoi_sample_time = event.time

            # Gilbert-Elliott link state transitions (once per sync interval)
            if (
                self.config.link_model == "gilbert_elliott"
                and event.time - last_ge_transition_time >= self._sync_interval
            ):
                self._update_ge_link_states()
                last_ge_transition_time = event.time

            self.current_time = event.time
            self._process_event(event)
            events_processed += 1

        # Final power update for remaining time
        remaining_power = self.simulation_duration_seconds - last_power_time
        if remaining_power > 0:
            self._update_power_consumption(remaining_power)

        return self._generate_result()

    def _process_event(self, event: SimEvent) -> None:
        handlers = {
            "state_sync": self._handle_state_sync,
            "message_send": self._handle_message_send,
            "message_receive": self._handle_message_receive,
            "coordinator_handoff": self._handle_coordinator_handoff,
            "node_failure": self._handle_node_failure,
            "node_recovery": self._handle_node_recovery,
            "gossip_round": self._handle_gossip_round,
            "collision_warning": self._handle_collision_warning,
        }
        handler = handlers.get(event.type)
        if handler:
            handler(event)

    # -- Gilbert-Elliott link model ----------------------------------------
    def _update_ge_link_states(self) -> None:
        """Transition Gilbert-Elliott link states for all active nodes.

        Called once per sync interval (T_c).  Each node's link independently
        transitions between good (True) and bad (False) states according to
        Markov transition probabilities.
        """
        p_gb = self.config.ge_p_good_to_bad
        p_bg = self.config.ge_p_bad_to_good
        for node_id in self._ge_link_states:
            if self._ge_link_states[node_id]:  # good state
                if self._stdlib_rng.random() < p_gb:
                    self._ge_link_states[node_id] = False
            else:  # bad state
                if self._stdlib_rng.random() < p_bg:
                    self._ge_link_states[node_id] = True

    def _link_delivers(self, sender_id: str) -> bool:
        """Return True if the message is successfully delivered.

        Uses the configured link model (Bernoulli or Gilbert-Elliott).
        """
        if self.config.link_model == "gilbert_elliott":
            in_good = self._ge_link_states.get(sender_id, True)
            p_loss = self.config.ge_p_loss_good if in_good else self.config.ge_p_loss_bad
            return self._stdlib_rng.random() >= p_loss
        # Bernoulli i.i.d.
        if self.config.link_availability >= 1.0:
            return True
        return self._stdlib_rng.random() <= self.config.link_availability

    # -- event handlers ----------------------------------------------------
    def _handle_state_sync(self, event: SimEvent) -> None:
        node = self._find_node(event.node_id)
        if node is None or node.status == "failed":
            return

        # --- Exception-based telemetry filtering (hierarchical only) ---
        # When enabled, only nodes whose state changed beyond threshold report.
        # Modelled probabilistically: each node has exception_threshold probability
        # of being "unstable" (needing to report) per cycle.
        if (
            self.config.enable_exception_telemetry
            and self.config.coordination_topology == "hierarchical"
            and not node.is_coordinator
        ):
            self._exception_expected_msgs += 1
            if self._stdlib_rng.random() > self.config.exception_threshold:
                # Node is stable -- skip reporting this cycle
                node.last_update_time = self.current_time
                self._reschedule_state_sync(node, self.current_time)
                return
            self._exception_actual_msgs += 1

        routes = get_message_routing(
            self.config.coordination_topology, self.network, event.node_id
        )
        ephemeris_delivered = False
        for sender_id, receiver_id in routes:
            # Determine message type and size based on sender/receiver roles
            msg_type = self._classify_message_type(sender_id, receiver_id)
            msg_size = MESSAGE_SIZES.get(msg_type, MESSAGE_SIZES["ephemeris"])

            # --- Per-cycle coordinator ingress tracking (distributional) ---
            recv_node = self._find_node(receiver_id)
            if recv_node and recv_node.is_coordinator:
                self._coordinator_ingress_this_cycle += msg_size

            # --- Coordinator bandwidth cap ---
            if self.config.coordinator_link_capacity_kbps > 0:
                # Check if receiver is a coordinator -- inbound traffic
                receiver_node = self._find_node(receiver_id)
                if receiver_node and receiver_node.is_coordinator:
                    coord_id = receiver_id
                    bytes_so_far = self._coordinator_bytes_this_interval.get(coord_id, 0.0)
                    # Scale cap by sample_rate: the DES only simulates a fraction
                    # of members, but the coordinator would receive from ALL members
                    # in the real fleet.  Scaling the cap down is equivalent to
                    # scaling the observed bytes up.
                    if self.config.coordinator_scheduling == "tdma":
                        # TDMA: deterministic slots, guard time reduces effective
                        # capacity but eliminates burstiness.  No drops if total
                        # offered load fits within (1 - guard) * capacity.
                        gamma = 1.0 - self.config.guard_time_fraction
                        max_bytes = (
                            (self.config.coordinator_link_capacity_kbps * 1_000 / 8)
                            * self._sync_interval
                            * gamma
                            * self._sync_sample_rate
                        )
                    else:
                        # Random phase: full capacity available but burstiness
                        # causes drops at lower utilizations.
                        max_bytes = (
                            (self.config.coordinator_link_capacity_kbps * 1_000 / 8)
                            * self._sync_interval
                            * self._sync_sample_rate
                        )
                    if bytes_so_far + msg_size > max_bytes:
                        self._coordinator_drops += 1
                        continue
                    self._coordinator_bytes_this_interval[coord_id] = bytes_so_far + msg_size

            # --- Link availability filter with retransmission ---
            # Supports both Bernoulli and Gilbert-Elliott link models via
            # the unified _link_delivers() method.
            delivered = True
            retries_used = 0
            self._link_attempted_msgs += 1
            # Offered-load byte tracking: count every transmission attempt
            self._total_bytes_attempted += msg_size
            is_protocol = msg_type != "ephemeris"
            if is_protocol:
                self._protocol_bytes_attempted += msg_size
            needs_loss_check = (
                self.config.link_model == "gilbert_elliott"
                or self.config.link_availability < 1.0
            )
            if needs_loss_check:
                if not self._link_delivers(sender_id):
                    delivered = False
                    # Attempt retransmissions
                    for _attempt in range(self.config.max_retransmissions):
                        self._retransmission_count += 1
                        self._link_attempted_msgs += 1
                        self._total_bytes_attempted += msg_size
                        if is_protocol:
                            self._protocol_bytes_attempted += msg_size
                        if self._link_delivers(sender_id):
                            delivered = True
                            retries_used = _attempt + 1
                            break
                    if not delivered:
                        self._link_lost_msgs += 1
                        if self.config.coordination_topology == "hierarchical":
                            receiver_node = self._find_node(receiver_id)
                            sender_node = self._find_node(sender_id)
                            if (receiver_node and receiver_node.is_coordinator) or (
                                sender_node and sender_node.is_coordinator
                            ):
                                self._coordinator_unavailability_events += 1
                        # Cross-cycle tracking: increment loss streak for
                        # member→coordinator ephemeris messages
                        if msg_type == "ephemeris":
                            streak = self._member_loss_streak.get(sender_id, 0)
                            self._member_loss_streak[sender_id] = streak + 1
                        continue

            # --- Airtime enforcement ---
            # When enabled, check whether this message would push the
            # coordinator's cumulative ingress airtime beyond T_c.
            if self.config.enforce_airtime and msg_type == "ephemeris":
                receiver_node_at = self._find_node(receiver_id)
                if receiver_node_at and receiver_node_at.is_coordinator:
                    coord_id_at = receiver_id
                    airtime_so_far = self._coordinator_airtime_this_cycle.get(coord_id_at, 0.0)
                    slot_ms = self.config.airtime_slot_duration_ms
                    T_c_ms = self._sync_interval * 1000
                    self._airtime_attempted += 1
                    if airtime_so_far + slot_ms > T_c_ms:
                        self._airtime_deadline_misses += 1
                        continue  # drop: airtime budget exceeded
                    self._coordinator_airtime_this_cycle[coord_id_at] = airtime_so_far + slot_ms
                    self._airtime_delivered += 1

            # --- Overhead accounting (unconditional) ---
            # Count bytes for overhead measurement regardless of queue state.
            # The queue models congestion/latency; byte counting measures
            # protocol traffic volume.
            self.total_messages_sent += 1
            self._total_bytes_sent += msg_size
            if msg_type != "ephemeris":
                self._protocol_bytes_sent += msg_size
            # Per-message-class byte tracking
            if msg_type == "ephemeris":
                self._ephemeris_bytes_sent += msg_size
            elif msg_type in ("cluster_summary", "region_summary"):
                self._summary_bytes_sent += msg_size
            elif msg_type == "heartbeat":
                self._heartbeat_bytes_sent += msg_size
            elif msg_type == "gossip":
                self._gossip_bytes_sent += msg_size
            sender = self._find_node(sender_id)
            if sender:
                sender.messages_sent += 1
            self._classify_tier_message(sender_id, receiver_id)

            # --- Track ephemeris delivery for companion heartbeat ---
            if msg_type == "ephemeris":
                ephemeris_delivered = True
                # Cross-cycle tracking: record recovery if member had
                # consecutive failed cycles, then reset streak
                streak = self._member_loss_streak.get(sender_id, 0)
                if streak > 0:
                    self._recovery_streaks.append(streak)
                    self._member_loss_streak[sender_id] = 0

            # --- AoI tracking: record successful delivery to coordinator ---
            if msg_type == "ephemeris":
                receiver_node = self._find_node(receiver_id)
                if receiver_node and receiver_node.is_coordinator:
                    if receiver_id not in self._coordinator_last_update:
                        self._coordinator_last_update[receiver_id] = {}
                    self._coordinator_last_update[receiver_id][sender_id] = self.current_time

            # --- Queue for latency tracking ---
            msg = create_message(sender_id, receiver_id, msg_type, self.current_time)
            msg.size_bytes = msg_size
            if self.message_queue.enqueue(msg):
                base_delay_ms = calculate_propagation_delay(
                    self.config.coordination_topology,
                    self.config.node_count,
                    self.config.cluster_size,
                )
                serialization_ms = 0.0
                if msg_size > MESSAGE_SIZES["ephemeris"]:
                    serialization_ms = (msg_size * 8) / (self.config.bandwidth_per_node_kbps * 1_000) * 1_000
                delay_ms = base_delay_ms + serialization_ms
                delay_ms += retries_used * base_delay_ms
                delay_s = delay_ms / 1_000.0
                self.event_queue.push(
                    SimEvent(
                        type="message_receive",
                        time=self.current_time + delay_s,
                        node_id=receiver_id,
                        data={"messageId": msg.id},
                    )
                )
        # --- Protocol extras: batch-accounted command dissemination ---
        # Coordination commands (512 B each) from coordinators to members.
        # Batch-accounted rather than individually routed to avoid generating
        # O(k_c) events per coordinator per cycle in the DES.
        #
        # Workload profiles control command volume:
        #   stress:       one unique 512 B command per member per cycle
        #   nominal:      no per-member commands (cluster summary only)
        #   event_driven: commands to p_event fraction of members per cycle
        if node.is_coordinator and self.config.coordination_topology in (
            "hierarchical", "sectorized_mesh"
        ):
            cluster = self._find_cluster(node.cluster_id)
            if cluster and self.config.workload_profile != "nominal":
                # Campaign duty factor: determine if commands are active this cycle.
                if self.config.campaign_mode == "on_off":
                    # ON/OFF Markov: transition state, then use current state
                    if self._campaign_on:
                        if self._stdlib_rng.random() < self._campaign_p_on_to_off:
                            self._campaign_on = False
                    else:
                        if self._stdlib_rng.random() < self._campaign_p_off_to_on:
                            self._campaign_on = True
                    duty_active = self._campaign_on
                else:
                    # Bernoulli: i.i.d. per-cycle coin flip with probability d.
                    duty_active = self._stdlib_rng.random() <= self.config.campaign_duty_factor
                cmd_size = MESSAGE_SIZES["coordination_command"]
                n_members = 0
                if duty_active:
                    for mid in cluster.node_ids:
                        if mid != node.id:
                            m = self._find_node(mid)
                            if m is not None and m.status != "failed":
                                n_members += 1
                # Event-driven: only a fraction of members need commands
                if self.config.workload_profile == "event_driven":
                    n_event = 0
                    for _ in range(n_members):
                        if self._stdlib_rng.random() <= self.config.event_command_probability:
                            n_event += 1
                    n_members = n_event
                # Distributed: Raft consensus replaces centralized commands.
                # Each round generates k_c × vote_msg_size bytes of traffic.
                # Total consensus bytes = rounds × k_c × vote_size.
                # We model this as equivalent command traffic from the
                # coordinator's perspective.
                if self.config.workload_profile == "distributed":
                    n_rounds = self.config.distributed_consensus_rounds
                    vote_size = self.config.distributed_vote_msg_bytes
                    # Consensus traffic: each round, every member exchanges
                    # a vote/append message.  Total bytes per consensus:
                    consensus_bytes = n_rounds * n_members * vote_size
                    self._distributed_consensus_bytes += consensus_bytes
                    self._total_bytes_sent += consensus_bytes
                    self._protocol_bytes_sent += consensus_bytes
                    self._total_bytes_attempted += consensus_bytes
                    self._protocol_bytes_attempted += consensus_bytes
                    # The equivalent "commands" are the consensus decisions;
                    # n_members commands are still generated (one decision per
                    # node), but the overhead is from consensus rounds.
                # Exception telemetry: coordinator only responds to nodes that
                # reported. Model as Bernoulli thinning of the command set.
                if (
                    self.config.enable_exception_telemetry
                    and self.config.coordination_topology == "hierarchical"
                ):
                    n_reporting = 0
                    for _ in range(n_members):
                        if self._stdlib_rng.random() <= self.config.exception_threshold:
                            n_reporting += 1
                    n_members = n_reporting
                # Apply link loss per-command (unified model)
                needs_loss = (
                    self.config.link_model == "gilbert_elliott"
                    or self.config.link_availability < 1.0
                )
                # Offered-load: all n_members commands are attempted
                attempted_cmd_bytes = n_members * cmd_size
                self._total_bytes_attempted += attempted_cmd_bytes
                self._protocol_bytes_attempted += attempted_cmd_bytes
                if needs_loss:
                    n_delivered = 0
                    for _ in range(n_members):
                        if self._link_delivers(node.id):
                            n_delivered += 1
                        else:
                            # Retransmission attempts
                            for _r in range(self.config.max_retransmissions):
                                self._retransmission_count += 1
                                # Count retransmission bytes as offered
                                self._total_bytes_attempted += cmd_size
                                self._protocol_bytes_attempted += cmd_size
                                if self._link_delivers(node.id):
                                    n_delivered += 1
                                    break
                else:
                    n_delivered = n_members
                cmd_bytes = n_delivered * cmd_size
                self._total_bytes_sent += cmd_bytes
                self._protocol_bytes_sent += cmd_bytes
                self._command_bytes_sent += cmd_bytes
                self.total_messages_sent += n_members
                self._tier_breakdown.intra_cluster_msgs += n_members

        # --- Hierarchical-only protocol extras: heartbeat + collision alert ---
        if self.config.coordination_topology == "hierarchical":
            # Heartbeat/ACK (64 B): regular node → coordinator, same link as ephemeris
            if not node.is_coordinator and ephemeris_delivered:
                hb_size = MESSAGE_SIZES["coordination_heartbeat"]
                self._total_bytes_sent += hb_size
                self._protocol_bytes_sent += hb_size
                self._heartbeat_bytes_sent += hb_size
                self._total_bytes_attempted += hb_size
                self._protocol_bytes_attempted += hb_size
                self.total_messages_sent += 1
                self._tier_breakdown.intra_cluster_msgs += 1
            # Collision alert (128 B): Bernoulli event, p = 10^-4/s * T_c
            if self._stdlib_rng.random() < 1e-4 * self._sync_interval:
                alert_size = MESSAGE_SIZES["collision_alert"]
                self._total_bytes_sent += alert_size
                self._protocol_bytes_sent += alert_size
                self._alert_bytes_sent += alert_size
                self._total_bytes_attempted += alert_size
                self._protocol_bytes_attempted += alert_size
                self.total_messages_sent += 1
                self._tier_breakdown.intra_cluster_msgs += 1

        node.last_update_time = self.current_time
        # Reset per-coordinator byte counters periodically
        if self.current_time - self._coordinator_interval_start >= self._sync_interval:
            self._coordinator_bytes_this_interval.clear()
            # Record per-cycle coordinator ingress for distributional analysis
            self._coordinator_ingress_per_cycle.append(self._coordinator_ingress_this_cycle)
            self._coordinator_ingress_this_cycle = 0
            # Record airtime utilization for this cycle before resetting
            if self.config.enforce_airtime and self._coordinator_airtime_this_cycle:
                T_c_ms = self._sync_interval * 1000
                for _cid, airtime_ms in self._coordinator_airtime_this_cycle.items():
                    self._airtime_per_cycle.append(airtime_ms / T_c_ms)
                self._coordinator_airtime_this_cycle.clear()
            self._coordinator_interval_start = self.current_time
        # Lazy reschedule: queue the next state_sync for this node
        self._reschedule_state_sync(node, self.current_time)

    def _sample_aoi(self, current_time: float) -> None:
        """Sample Age-of-Information at all coordinators.

        For each coordinator, compute AoI = current_time - last_update_time
        for each cluster member. Nodes that have never reported have
        AoI = current_time (since simulation start).
        """
        if not self._coordinator_last_update:
            return
        for coord_id, member_updates in self._coordinator_last_update.items():
            coord_node = self._find_node(coord_id)
            if coord_node is None or coord_node.status == "failed":
                continue
            # Find the cluster this coordinator belongs to
            cluster = None
            if coord_node.cluster_id:
                cluster = self.network.get_cluster(coord_node.cluster_id)
            if cluster is None:
                continue
            # Compute AoI for each member in the cluster
            for member_id in cluster.node_ids:
                if member_id == coord_id:
                    continue  # coordinator knows its own state
                last_update = member_updates.get(member_id, 0.0)
                aoi = current_time - last_update
                self._aoi_samples.append(aoi)

    def _handle_message_send(self, event: SimEvent) -> None:
        # Sending is handled inline in state_sync
        pass

    def _handle_message_receive(self, event: SimEvent) -> None:
        node = self._find_node(event.node_id)
        if node is None or node.status == "failed":
            return

        bandwidth_bps = self.config.bandwidth_per_node_kbps * 1_000
        processed = self.message_queue.process_messages(
            self.current_time, bandwidth_bps, 0.1
        )
        for msg in processed:
            self.total_messages_delivered += 1
            if msg.receive_time is not None:
                prop_ms = (msg.receive_time - msg.send_time) * 1_000
                self.propagation_times.append(prop_ms)
            receiver = self._find_node(msg.receiver_id)
            if receiver:
                receiver.messages_received += 1
                receiver.last_update_time = self.current_time

    def _handle_coordinator_handoff(self, event: SimEvent) -> None:
        cluster = self._find_cluster(event.cluster_id)
        if cluster is None:
            return
        if not needs_handoff(cluster, self.current_time, self.duty_cycle_seconds):
            return
        result = perform_handoff(
            cluster, self.network.nodes, self.current_time, self.rng
        )
        idx = next(
            (i for i, c in enumerate(self.network.clusters) if c.id == cluster.id),
            -1,
        )
        if idx >= 0:
            self.network.clusters[idx] = result.cluster
        self.network.nodes = result.nodes
        # Lazy reschedule next handoff for this cluster
        self._reschedule_handoff(event.cluster_id, self.current_time)

    def _handle_node_failure(self, event: SimEvent) -> None:
        idx = self._find_node_index(event.node_id)
        if idx < 0:
            return
        node = self.network.nodes[idx]
        if node.status == "failed":
            return

        self.network.nodes[idx] = fail_node(node, self.current_time)

        if node.is_coordinator:
            cluster = next(
                (c for c in self.network.clusters if c.coordinator_id == node.id),
                None,
            )
            if cluster:
                self.event_queue.push(
                    SimEvent(
                        type="coordinator_handoff",
                        time=self.current_time + 1.0,
                        node_id=node.id,
                        cluster_id=cluster.id,
                    )
                )

        # Schedule recovery (MTTR 1--7 days)
        mttr_seconds = (self.rng.integers(1, 8)) * SECONDS_PER_DAY
        if self.current_time + mttr_seconds < self.simulation_duration_seconds:
            self.event_queue.push(
                SimEvent(
                    type="node_recovery",
                    time=self.current_time + mttr_seconds,
                    node_id=event.node_id,
                    cluster_id=event.cluster_id,
                )
            )

    def _handle_node_recovery(self, event: SimEvent) -> None:
        idx = self._find_node_index(event.node_id)
        if idx < 0:
            return
        node = self.network.nodes[idx]
        if node.status != "failed":
            return
        self.network.nodes[idx] = SwarmNode(
            id=node.id,
            status="operational",
            cluster_id=node.cluster_id,
            is_coordinator=False,
            coordinator_time_seconds=node.coordinator_time_seconds,
            power_consumed_wh=node.power_consumed_wh,
            messages_sent=node.messages_sent,
            messages_received=node.messages_received,
            last_update_time=node.last_update_time,
            failure_time=None,
        )

    def _handle_gossip_round(self, event: SimEvent) -> None:
        if self.config.coordination_topology != "mesh":
            return
        mesh_neighbors = self.network.mesh_neighbors or {}
        n_nodes = len(self.network.nodes)
        # Sample a fixed number of node indices directly
        n_sample = min(1_000, n_nodes)
        indices = self.rng.choice(n_nodes, size=n_sample, replace=False)
        max_gossip_msgs = min(1_000, n_nodes)
        msgs_this_round = 0

        queue_has_space = not self.message_queue.is_full()
        for idx in indices:
            if msgs_this_round >= max_gossip_msgs or not queue_has_space:
                break
            node = self.network.nodes[idx]
            if node.status == "failed":
                continue
            neighbors = mesh_neighbors.get(node.id, [])
            for nid in neighbors:
                if msgs_this_round >= max_gossip_msgs:
                    break
                neighbor = self.network.get_node(nid)
                if neighbor is None or neighbor.status == "failed":
                    continue
                # --- Link availability filter (unified model) ---
                self._link_attempted_msgs += 1
                gossip_size = MESSAGE_SIZES["gossip"]
                self._total_bytes_attempted += gossip_size
                self._protocol_bytes_attempted += gossip_size
                needs_loss = (
                    self.config.link_model == "gilbert_elliott"
                    or self.config.link_availability < 1.0
                )
                if needs_loss and not self._link_delivers(node.id):
                    self._link_lost_msgs += 1
                    continue
                msg = create_message(node.id, nid, "gossip", self.current_time)
                if self.message_queue.enqueue(msg):
                    self.total_messages_sent += 1
                    self._total_bytes_sent += msg.size_bytes
                    self._protocol_bytes_sent += msg.size_bytes
                    self._gossip_bytes_sent += msg.size_bytes
                    node.messages_sent += 1
                    self._tier_breakdown.gossip_msgs += 1
                    msgs_this_round += 1
                else:
                    queue_has_space = False
                    break
            if not queue_has_space:
                break
        # Lazy reschedule next gossip round
        current_round = (event.data or {}).get("round", 0)
        self._reschedule_gossip(self.current_time, current_round)

    def _handle_collision_warning(self, event: SimEvent) -> None:
        self.total_messages_sent += 1

    # -- power update ------------------------------------------------------
    def _update_power_consumption(self, elapsed_seconds: float) -> None:
        if elapsed_seconds <= 0:
            return
        base_w = self.config.base_power_w
        coord_w = self.config.coordinator_power_w
        hours = elapsed_seconds / 3600.0
        for node in self.network.nodes:
            power = coord_w if node.is_coordinator else base_w
            node.power_consumed_wh += power * hours
            if node.is_coordinator:
                node.coordinator_time_seconds += elapsed_seconds

    # -- result generation -------------------------------------------------
    def _generate_result(self) -> SwarmCoordinationRunResult:
        queue_stats = self.message_queue.get_stats()
        prop_stats = self.message_queue.get_propagation_stats()

        # --- DES-measured overhead from actual message byte counts ---
        # The DES samples a fraction of nodes (sample_rate) and may terminate
        # early due to max_events.  We compute the *rate* of bytes per second
        # observed during the simulated window, scale by 1/sample_rate to
        # estimate fleet-wide rate, then express as % of fleet bandwidth.
        # Protocol overhead (η) excludes baseline ephemeris (topology-invariant)
        # to match the traffic accounting definition in the paper.
        scale_factor = 1.0 / max(self._sync_sample_rate, 1e-9)
        simulated_seconds = max(1.0, self.current_time)  # actual simulated time
        protocol_bps = self._protocol_bytes_sent / simulated_seconds * scale_factor * 8
        fleet_capacity_bps = self.config.node_count * self.config.bandwidth_per_node_kbps * 1_000
        overhead = (protocol_bps / fleet_capacity_bps) * 100.0 if fleet_capacity_bps > 0 else 0.0

        bottleneck = estimate_bottleneck_threshold(
            self.config.coordination_topology,
            self.config.cluster_size,
            self.config.bandwidth_per_node_kbps,
        )

        coord_availability = 100.0
        if self.config.coordination_topology == "hierarchical":
            avails = [
                calculate_coordinator_availability(
                    c, self.network.nodes, self.simulation_duration_seconds
                )
                for c in self.network.clusters
            ]
            if avails:
                coord_availability = sum(avails) / len(avails)

        power_var = calculate_power_variance(self.network.nodes)
        total_failed = sum(c.failed_handoffs for c in self.network.clusters)

        avg_prop = prop_stats.avg_propagation_ms
        max_prop = prop_stats.max_propagation_ms
        if self.propagation_times:
            avg_prop = sum(self.propagation_times) / len(self.propagation_times)
            max_prop = max(self.propagation_times)
        if avg_prop == 0.0:
            avg_prop = calculate_propagation_delay(
                self.config.coordination_topology,
                self.config.node_count,
                self.config.cluster_size,
            )
            max_prop = avg_prop * 2.0

        # Exception telemetry reduction factor
        if self._exception_expected_msgs > 0:
            exception_reduction = (
                self._exception_actual_msgs / self._exception_expected_msgs
            )
        else:
            exception_reduction = 1.0

        # Link availability loss rate
        if self._link_attempted_msgs > 0:
            link_loss_rate = self._link_lost_msgs / self._link_attempted_msgs
        else:
            link_loss_rate = 0.0

        # AoI statistics
        aoi_mean = 0.0
        aoi_p99 = 0.0
        aoi_max = 0.0
        aoi_count = len(self._aoi_samples)
        if self._aoi_samples:
            aoi_arr = np.array(self._aoi_samples)
            aoi_mean = float(np.mean(aoi_arr))
            aoi_p99 = float(np.percentile(aoi_arr, 99))
            aoi_max = float(np.max(aoi_arr))

        # AoI-to-ephemeris coupling: along-track position uncertainty
        # σ(t) = σ₀ + σ̇ · AoI
        aoi_mean_pos = self.config.aoi_sigma_0_m + self.config.aoi_sigma_dot_m_per_s * aoi_mean
        aoi_p99_pos = self.config.aoi_sigma_0_m + self.config.aoi_sigma_dot_m_per_s * aoi_p99

        # Cross-cycle recovery statistics
        cc_mean = 0.0
        cc_p95 = 0.0
        cc_count = len(self._recovery_streaks)
        cc_max = 0
        cc_cdf: list[float] = []
        if self._recovery_streaks:
            cc_arr = np.array(self._recovery_streaks)
            cc_mean = float(np.mean(cc_arr))
            cc_p95 = float(np.percentile(cc_arr, 95))
            cc_max = int(np.max(cc_arr))
            # Cumulative recovery fraction at each cycle count [1..10]
            for k in range(1, 11):
                cc_cdf.append(float(np.mean(cc_arr <= k)))

        return SwarmCoordinationRunResult(
            run_id=0,
            config=self.config,
            communication_overhead_percent=overhead,
            bottleneck_threshold_nodes=bottleneck,
            coordinator_availability_percent=coord_availability,
            power_variance_percent=power_var,
            avg_update_propagation_ms=avg_prop,
            max_update_propagation_ms=max_prop,
            failed_handoffs=total_failed,
            message_drop_rate=queue_stats["dropRate"],
            total_messages_sent=self.total_messages_sent,
            total_messages_delivered=self.total_messages_delivered,
            avg_messages_per_node_per_day=(
                self.total_messages_sent
                / max(1, self.config.node_count)
                / max(1, self.config.simulation_days)
            ),
            total_energy_kwh=calculate_total_energy(self.network.nodes),
            coordinator_bandwidth_kbps=per_coordinator_bandwidth_kbps(
                self.config.cluster_size, 10.0
            ),
            tier_breakdown=TierMessageBreakdown(
                intra_cluster_msgs=self._tier_breakdown.intra_cluster_msgs,
                inter_cluster_msgs=self._tier_breakdown.inter_cluster_msgs,
                central_msgs=self._tier_breakdown.central_msgs,
                gossip_msgs=self._tier_breakdown.gossip_msgs,
            ),
            exception_telemetry_reduction=exception_reduction,
            message_loss_rate=link_loss_rate,
            coordinator_unavailability_events=self._coordinator_unavailability_events,
            total_bytes_sent=self._total_bytes_sent,
            protocol_bytes_sent=self._protocol_bytes_sent,
            coordinator_drops=self._coordinator_drops,
            retransmission_count=self._retransmission_count,
            total_bytes_attempted=self._total_bytes_attempted,
            protocol_bytes_attempted=self._protocol_bytes_attempted,
            aoi_mean_seconds=aoi_mean,
            aoi_p99_seconds=aoi_p99,
            aoi_max_seconds=aoi_max,
            aoi_samples=aoi_count,
            ephemeris_bytes_sent=self._ephemeris_bytes_sent,
            heartbeat_bytes_sent=self._heartbeat_bytes_sent,
            command_bytes_sent=self._command_bytes_sent,
            summary_bytes_sent=self._summary_bytes_sent,
            alert_bytes_sent=self._alert_bytes_sent,
            gossip_bytes_sent=self._gossip_bytes_sent,
            aoi_mean_position_error_m=aoi_mean_pos,
            aoi_p99_position_error_m=aoi_p99_pos,
            cross_cycle_recovery_mean=cc_mean,
            cross_cycle_recovery_p95=cc_p95,
            cross_cycle_recovery_count=cc_count,
            cross_cycle_max_streak=cc_max,
            cross_cycle_recovery_rate_by_cycle=cc_cdf,
            # Airtime enforcement metrics
            airtime_utilization_mean=(
                float(np.mean(self._airtime_per_cycle))
                if self._airtime_per_cycle else 0.0
            ),
            airtime_deadline_misses=self._airtime_deadline_misses,
            airtime_limited_delivery=(
                self._airtime_delivered / max(1, self._airtime_attempted)
                if self.config.enforce_airtime else 0.0
            ),
            # Distributed workload metrics
            distributed_consensus_bytes=self._distributed_consensus_bytes,
            # Per-cycle coordinator ingress distribution
            coordinator_ingress_bytes_per_cycle=self._coordinator_ingress_per_cycle,
        )

    # -- helpers -----------------------------------------------------------
    def _classify_message_type(self, sender_id: str, receiver_id: str) -> str:
        """Return the message type key based on sender/receiver roles.

        This implements message-size heterogeneity: different tiers produce
        different message sizes (ephemeris=256B, cluster_summary=512B,
        region_summary=1024B, handoff=8192B).
        """
        if self.config.coordination_topology != "hierarchical":
            if self.config.coordination_topology == "mesh":
                return "gossip"
            if self.config.coordination_topology == "sectorized_mesh":
                # Status report to OWN sector coordinator = ephemeris (256 B);
                # peer-to-peer (including cross-sector) = heartbeat (32 B)
                sender = self._find_node(sender_id)
                if sender and sender.cluster_id:
                    cluster = self.network.get_cluster(sender.cluster_id)
                    if cluster and receiver_id == cluster.coordinator_id:
                        return "ephemeris"
                return "heartbeat"
            return "ephemeris"

        sender = self._find_node(sender_id)
        receiver = self._find_node(receiver_id)
        if sender is None or receiver is None:
            return "ephemeris"

        # Check if this is a coordinator sending to regional coordinator
        if sender.is_coordinator:
            sender_cluster = self._find_cluster(sender.cluster_id)
            if sender_cluster is not None:
                regional_id = sender_cluster.regional_coordinator_id
                if regional_id and receiver_id == regional_id and sender_id != receiver_id:
                    return "cluster_summary"

        # Check if this is a regional coordinator sending to central
        if receiver_id == self.network.central_coordinator_id and sender_id != receiver_id:
            sender_cluster = self._find_cluster(sender.cluster_id)
            if sender_cluster and sender_cluster.regional_coordinator_id == sender_id:
                return "region_summary"

        # Default: node-to-coordinator ephemeris
        return "ephemeris"

    def _classify_tier_message(self, sender_id: str, receiver_id: str) -> None:
        """Classify a message by tier and update the breakdown counters."""
        if self.config.coordination_topology == "sectorized_mesh":
            self._tier_breakdown.gossip_msgs += 1
            return
        if self.config.coordination_topology != "hierarchical":
            # For non-hierarchical topologies, all sync messages are intra-cluster
            self._tier_breakdown.intra_cluster_msgs += 1
            return

        sender = self._find_node(sender_id)
        receiver = self._find_node(receiver_id)
        if sender is None or receiver is None:
            self._tier_breakdown.intra_cluster_msgs += 1
            return

        # Check if receiver is the central coordinator
        if receiver_id == self.network.central_coordinator_id and sender_id != receiver_id:
            # Check if sender is a regional coordinator (i.e. it is a cluster
            # coordinator that also serves as regional coordinator and is sending
            # to central) -- treat as central tier message
            sender_cluster = self._find_cluster(sender.cluster_id)
            if sender_cluster and sender_cluster.regional_coordinator_id == sender_id:
                self._tier_breakdown.central_msgs += 1
                return

        # Check if receiver is a regional coordinator (inter-cluster message)
        sender_cluster = self._find_cluster(sender.cluster_id)
        if sender_cluster is not None:
            regional_id = sender_cluster.regional_coordinator_id
            if regional_id and receiver_id == regional_id and sender_id != receiver_id:
                # Sender is a cluster coordinator sending to regional coordinator
                if sender.is_coordinator:
                    self._tier_breakdown.inter_cluster_msgs += 1
                    return

        # Default: intra-cluster message (member <-> coordinator)
        self._tier_breakdown.intra_cluster_msgs += 1

    def _find_node(self, node_id: str) -> Optional[SwarmNode]:
        return self.network.get_node(node_id)

    def _find_node_index(self, node_id: str) -> int:
        return self.network._node_map.get(node_id, -1)

    def _find_cluster(self, cluster_id: Optional[str]) -> Optional[Cluster]:
        if cluster_id is None:
            return None
        return self.network.get_cluster(cluster_id)


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import time

    print("=" * 72)
    print("Swarm Coordination Model -- single-run demo")
    print("=" * 72)

    cfg = SwarmCoordinationConfig(
        node_count=1_000,
        coordination_topology="hierarchical",
        cluster_size=100,
        coordinator_duty_cycle_hours=24,
        bandwidth_per_node_kbps=1.0,
        node_failure_rate_per_year=0.02,
        coordinator_power_w=18.0,
        base_power_w=5.0,
        simulation_days=30,
        seed=42,
    )

    print(f"\nConfig: {cfg.node_count} nodes, {cfg.coordination_topology} topology, "
          f"{cfg.simulation_days} days")

    t0 = time.perf_counter()
    sim = SwarmCoordinationSimulator(cfg)
    result = sim.run()
    elapsed = time.perf_counter() - t0

    print(f"\nSimulation completed in {elapsed:.2f} s")
    print(f"  Communication overhead : {result.communication_overhead_percent:.2f} %")
    print(f"  Bottleneck threshold   : {result.bottleneck_threshold_nodes:,.0f} nodes")
    print(f"  Coordinator availability: {result.coordinator_availability_percent:.2f} %")
    print(f"  Power variance         : {result.power_variance_percent:.2f} %")
    print(f"  Avg propagation delay  : {result.avg_update_propagation_ms:.2f} ms")
    print(f"  Max propagation delay  : {result.max_update_propagation_ms:.2f} ms")
    print(f"  Failed handoffs        : {result.failed_handoffs}")
    print(f"  Message drop rate      : {result.message_drop_rate:.4f}")
    print(f"  Total messages sent    : {result.total_messages_sent:,}")
    print(f"  Total messages delivered: {result.total_messages_delivered:,}")
    print(f"  Avg msgs/node/day      : {result.avg_messages_per_node_per_day:.2f}")
    print(f"  Total energy           : {result.total_energy_kwh:.2f} kWh")
