"""Unit tests for swarm_mc -- Monte Carlo engine for swarm coordination."""

import math

import numpy as np
import pytest

from swarm_mc import (
    ScalingAnalysisResult,
    Stats,
    SwarmCoordinationOutput,
    SwarmCoordinationResult,
    TopologyComparisonResult,
    aggregate_results,
    calculate_stats,
    confidence_interval,
    find_optimal_config,
    generate_scaling_configs,
    run_swarm_coordination_mc,
    run_topology_comparison,
)
from swarm_model import (
    SwarmCoordinationConfig,
    SwarmCoordinationRunResult,
)


# ===== TestCalculateStats =====


class TestCalculateStats:
    """Test calculate_stats helper."""

    def test_basic_stats(self):
        values = [1.0, 2.0, 3.0, 4.0, 5.0]
        stats = calculate_stats(values)
        assert stats.mean == pytest.approx(3.0)
        assert stats.median == pytest.approx(3.0)
        assert stats.min == pytest.approx(1.0)
        assert stats.max == pytest.approx(5.0)
        assert stats.stddev > 0

    def test_single_value(self):
        stats = calculate_stats([42.0])
        assert stats.mean == pytest.approx(42.0)
        assert stats.median == pytest.approx(42.0)
        assert stats.stddev == pytest.approx(0.0)
        assert stats.min == pytest.approx(42.0)
        assert stats.max == pytest.approx(42.0)

    def test_empty(self):
        stats = calculate_stats([])
        assert stats.mean == pytest.approx(0.0)
        assert stats.stddev == pytest.approx(0.0)

    def test_percentiles(self):
        values = list(range(1, 101))  # 1..100
        stats = calculate_stats(values)
        assert stats.p5 == pytest.approx(5.95, abs=1.0)
        assert stats.p95 == pytest.approx(95.05, abs=1.0)

    def test_numpy_array_input(self):
        arr = np.array([10.0, 20.0, 30.0])
        stats = calculate_stats(arr)
        assert stats.mean == pytest.approx(20.0)


# ===== TestConfidenceInterval =====


class TestConfidenceInterval:
    """Test confidence_interval helper."""

    def test_narrow_for_identical(self):
        values = [5.0] * 100
        lo, hi = confidence_interval(values)
        assert lo == pytest.approx(5.0, abs=0.01)
        assert hi == pytest.approx(5.0, abs=0.01)

    def test_wider_for_spread(self):
        narrow = [5.0] * 100
        spread = list(np.random.default_rng(42).normal(5.0, 2.0, 100))
        ci_narrow = confidence_interval(narrow)
        ci_spread = confidence_interval(spread)
        width_narrow = ci_narrow[1] - ci_narrow[0]
        width_spread = ci_spread[1] - ci_spread[0]
        assert width_spread > width_narrow

    def test_contains_mean(self):
        values = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        lo, hi = confidence_interval(values)
        mean = np.mean(values)
        assert lo <= mean <= hi

    def test_empty(self):
        lo, hi = confidence_interval([])
        assert lo == pytest.approx(0.0)
        assert hi == pytest.approx(0.0)

    def test_different_confidence_levels(self):
        values = list(np.random.default_rng(42).normal(10.0, 1.0, 200))
        ci_90 = confidence_interval(values, 0.90)
        ci_95 = confidence_interval(values, 0.95)
        ci_99 = confidence_interval(values, 0.99)
        width_90 = ci_90[1] - ci_90[0]
        width_95 = ci_95[1] - ci_95[0]
        width_99 = ci_99[1] - ci_99[0]
        assert width_90 < width_95 < width_99


# ===== TestRunSwarmCoordinationMC =====


class TestRunSwarmCoordinationMC:
    """Test run_swarm_coordination_mc core MC runner."""

    def test_returns_result(self):
        cfg = SwarmCoordinationConfig(
            node_count=100,
            coordination_topology="hierarchical",
            cluster_size=25,
            simulation_days=5, sync_sample_rate=0.1,
            seed=42,
        )
        output = run_swarm_coordination_mc(cfg, runs=3)
        assert isinstance(output, SwarmCoordinationOutput)
        assert output.runs == 3
        assert output.execution_time_ms > 0

    def test_reproducible(self):
        cfg = SwarmCoordinationConfig(
            node_count=100,
            coordination_topology="hierarchical",
            cluster_size=25,
            simulation_days=5, sync_sample_rate=0.1,
            seed=42,
        )
        out1 = run_swarm_coordination_mc(cfg, runs=3)
        out2 = run_swarm_coordination_mc(cfg, runs=3)
        assert out1.result.communication_overhead_percent == pytest.approx(
            out2.result.communication_overhead_percent
        )

    def test_confidence_interval_present(self):
        cfg = SwarmCoordinationConfig(
            node_count=100,
            coordination_topology="hierarchical",
            cluster_size=25,
            simulation_days=5, sync_sample_rate=0.1,
            seed=42,
        )
        output = run_swarm_coordination_mc(cfg, runs=5)
        ci = output.result.confidence_interval_95
        assert isinstance(ci, tuple)
        assert len(ci) == 2
        assert ci[0] <= ci[1]

    def test_progress_callback(self):
        cfg = SwarmCoordinationConfig(
            node_count=100,
            coordination_topology="hierarchical",
            cluster_size=25,
            simulation_days=5, sync_sample_rate=0.1,
            seed=42,
        )
        calls = []

        def on_progress(cur, total, pct):
            calls.append((cur, total, pct))

        run_swarm_coordination_mc(cfg, runs=3, on_progress=on_progress)
        assert len(calls) == 3
        assert calls[-1][0] == 3  # final call is run 3 of 3

    def test_aggregated_fields(self):
        cfg = SwarmCoordinationConfig(
            node_count=100,
            coordination_topology="hierarchical",
            cluster_size=25,
            simulation_days=5, sync_sample_rate=0.1,
            seed=42,
        )
        output = run_swarm_coordination_mc(cfg, runs=4)
        r = output.result
        assert r.communication_overhead_percent >= 0
        assert r.coordinator_availability_percent >= 0
        assert r.bottleneck_threshold_nodes >= 0


# ===== TestRunTopologyComparison =====


class TestRunTopologyComparison:
    """Test run_topology_comparison."""

    def test_three_topologies(self):
        cfg = SwarmCoordinationConfig(
            node_count=100,
            coordination_topology="hierarchical",
            cluster_size=25,
            simulation_days=5, sync_sample_rate=0.1,
            seed=42,
        )
        result = run_topology_comparison(cfg, runs_per=3)
        assert isinstance(result, TopologyComparisonResult)
        assert len(result.configs) == 3
        assert len(result.results) == 3

    def test_optimal_index_valid(self):
        cfg = SwarmCoordinationConfig(
            node_count=100,
            coordination_topology="hierarchical",
            cluster_size=25,
            simulation_days=5, sync_sample_rate=0.1,
            seed=42,
        )
        result = run_topology_comparison(cfg, runs_per=3)
        assert 0 <= result.optimal_config_index < 3

    def test_analysis_keys(self):
        cfg = SwarmCoordinationConfig(
            node_count=100,
            coordination_topology="hierarchical",
            cluster_size=25,
            simulation_days=5, sync_sample_rate=0.1,
            seed=42,
        )
        result = run_topology_comparison(cfg, runs_per=3)
        assert "bestLatency" in result.analysis
        assert "bestBandwidth" in result.analysis
        assert "bestPower" in result.analysis
        assert "recommendation" in result.analysis

    def test_custom_topologies(self):
        cfg = SwarmCoordinationConfig(
            node_count=100,
            coordination_topology="hierarchical",
            cluster_size=25,
            simulation_days=5, sync_sample_rate=0.1,
            seed=42,
        )
        result = run_topology_comparison(
            cfg, topologies=["centralized", "hierarchical"], runs_per=3
        )
        assert len(result.configs) == 2
        assert len(result.results) == 2


# ===== TestGenerateScalingConfigs =====


class TestGenerateScalingConfigs:
    """Test generate_scaling_configs."""

    def test_correct_count(self):
        cfg = SwarmCoordinationConfig(seed=42)
        configs = generate_scaling_configs(cfg)
        # Default: 7 node counts
        assert len(configs) == 7

    def test_cluster_size_scales(self):
        cfg = SwarmCoordinationConfig(seed=42)
        configs = generate_scaling_configs(cfg)
        # Cluster size should be min(200, max(50, floor(sqrt(N))))
        for c in configs:
            expected_cs = min(200, max(50, int(math.floor(math.sqrt(c.node_count)))))
            assert c.cluster_size == expected_cs

    def test_custom_node_counts(self):
        cfg = SwarmCoordinationConfig(seed=42)
        counts = [100, 500, 1000]
        configs = generate_scaling_configs(cfg, node_counts=counts)
        assert len(configs) == 3
        assert [c.node_count for c in configs] == counts

    def test_preserves_base_fields(self):
        cfg = SwarmCoordinationConfig(
            bandwidth_per_node_kbps=2.0,
            node_failure_rate_per_year=0.05,
            seed=42,
        )
        configs = generate_scaling_configs(cfg)
        for c in configs:
            assert c.bandwidth_per_node_kbps == 2.0
            assert c.node_failure_rate_per_year == 0.05


# ===== TestFindOptimalConfig =====


class TestFindOptimalConfig:
    """Test find_optimal_config."""

    def test_returns_valid_index(self):
        # Create some dummy results with varying quality
        results = [
            SwarmCoordinationResult(
                communication_overhead_percent=50.0,
                coordinator_availability_percent=90.0,
                avg_update_propagation_ms=1000.0,
                message_drop_rate=0.05,
            ),
            SwarmCoordinationResult(
                communication_overhead_percent=10.0,
                coordinator_availability_percent=99.0,
                avg_update_propagation_ms=100.0,
                message_drop_rate=0.01,
            ),
            SwarmCoordinationResult(
                communication_overhead_percent=30.0,
                coordinator_availability_percent=95.0,
                avg_update_propagation_ms=500.0,
                message_drop_rate=0.02,
            ),
        ]
        topologies = ["centralized", "hierarchical", "mesh"]
        idx = find_optimal_config(results, topologies)
        assert 0 <= idx < 3
        # The second result (index 1) should score highest: low overhead,
        # high availability, low latency, low drop rate
        assert idx == 1

    def test_single_result(self):
        results = [
            SwarmCoordinationResult(
                communication_overhead_percent=20.0,
                coordinator_availability_percent=95.0,
                avg_update_propagation_ms=200.0,
                message_drop_rate=0.01,
            ),
        ]
        idx = find_optimal_config(results, ["hierarchical"])
        assert idx == 0

    def test_equal_results(self):
        r = SwarmCoordinationResult(
            communication_overhead_percent=20.0,
            coordinator_availability_percent=95.0,
            avg_update_propagation_ms=200.0,
            message_drop_rate=0.01,
        )
        results = [r, r, r]
        idx = find_optimal_config(results, ["centralized", "hierarchical", "mesh"])
        assert 0 <= idx < 3


# ===== TestAggregateResults =====


class TestAggregateResults:
    """Test aggregate_results."""

    def test_aggregates_correctly(self):
        runs = []
        for i in range(5):
            r = SwarmCoordinationRunResult(
                run_id=i,
                communication_overhead_percent=10.0 + i,
                bottleneck_threshold_nodes=1000.0,
                coordinator_availability_percent=99.0,
                power_variance_percent=5.0,
                avg_update_propagation_ms=100.0,
                max_update_propagation_ms=200.0,
                failed_handoffs=0,
                message_drop_rate=0.01,
            )
            runs.append(r)

        agg = aggregate_results(runs)
        assert agg.communication_overhead_percent == pytest.approx(12.0)
        assert agg.coordinator_availability_percent == pytest.approx(99.0)
        assert agg.bottleneck_threshold_nodes == pytest.approx(1000.0)

    def test_stddev_nonzero_for_varied(self):
        runs = []
        for i in range(10):
            r = SwarmCoordinationRunResult(
                run_id=i,
                communication_overhead_percent=float(i * 5),
                bottleneck_threshold_nodes=1000.0,
                coordinator_availability_percent=99.0,
                power_variance_percent=5.0,
                avg_update_propagation_ms=100.0,
                max_update_propagation_ms=200.0,
                failed_handoffs=i,
                message_drop_rate=0.01,
            )
            runs.append(r)

        agg = aggregate_results(runs)
        assert agg.communication_overhead_std_dev > 0
        assert agg.failed_handoffs_std_dev > 0

    def test_ci_contains_mean(self):
        runs = []
        for i in range(20):
            r = SwarmCoordinationRunResult(
                run_id=i,
                communication_overhead_percent=10.0 + np.random.default_rng(42 + i).normal(0, 1),
            )
            runs.append(r)

        agg = aggregate_results(runs)
        lo, hi = agg.confidence_interval_95
        assert lo <= agg.communication_overhead_percent <= hi
