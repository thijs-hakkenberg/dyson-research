"""Scientific property tests — verify economic invariants and physical constraints."""

import numpy as np
import pytest

from isru_model import (
    BASELINE,
    earth_delivery_time,
    find_crossover,
    find_crossover_npv,
    find_crossover_npv_phased,
    unit_to_time,
)


class TestCrossoverExistence:
    def test_baseline_undiscounted_exists(self, baseline):
        cross = find_crossover(baseline)
        assert cross < 20000

    def test_baseline_npv_exists(self, baseline):
        cross = find_crossover_npv(baseline)
        assert cross < 20000

    def test_optimistic_earlier(self, optimistic_params, baseline):
        opt = find_crossover_npv(optimistic_params)
        base = find_crossover_npv(baseline)
        assert opt < base

    def test_conservative_later(self, conservative_params, baseline):
        con = find_crossover_npv(conservative_params)
        base = find_crossover_npv(baseline)
        assert con > base


class TestDiscountRateEffect:
    def test_npv_gte_undiscounted(self, baseline):
        undisc = find_crossover(baseline)
        npv = find_crossover_npv(baseline)
        assert npv >= undisc

    def test_monotonic_in_r(self, baseline):
        rates = [0.0, 0.03, 0.05, 0.08, 0.10]
        crossovers = []
        for r in rates:
            p = baseline.copy()
            p["r"] = r
            crossovers.append(find_crossover_npv(p))
        # Higher r → later crossover (weakly monotonic)
        for i in range(len(crossovers) - 1):
            assert crossovers[i] <= crossovers[i + 1]


class TestCapitalSensitivity:
    def test_higher_K_later_crossover(self, baseline):
        cross_low = find_crossover_npv({**baseline, "K": 30e9})
        cross_high = find_crossover_npv({**baseline, "K": 100e9})
        assert cross_high > cross_low


class TestLaunchCostSensitivity:
    def test_higher_launch_earlier_crossover(self, baseline):
        cross_low_launch = find_crossover_npv({**baseline, "p_launch": 500})
        cross_high_launch = find_crossover_npv({**baseline, "p_launch": 2000})
        assert cross_high_launch < cross_low_launch


class TestLearningRateSensitivity:
    def test_higher_lr_e_earlier_crossover(self, baseline):
        """Higher LR_E = slower learning → manufacturing stays expensive → ISRU wins earlier."""
        cross_fast = find_crossover_npv({**baseline, "LR_E": 0.80})
        cross_slow = find_crossover_npv({**baseline, "LR_E": 0.90})
        assert cross_slow < cross_fast


class TestNoISRULearning:
    def test_lr_i_one_still_converges(self, baseline):
        """Even without ISRU learning, crossover exists (at larger N)."""
        p = baseline.copy()
        p["LR_I"] = 1.0
        cross = find_crossover_npv(p, N_max=40000)
        assert cross < 40000


class TestPhasedCapital:
    def test_phased_lte_lumpsum(self, baseline):
        lump = find_crossover_npv(baseline)
        phased = find_crossover_npv_phased(baseline, K_years=5)
        assert phased <= lump


class TestDeliveryTimingComparison:
    def test_earth_lte_isru_timing(self, baseline):
        """Earth delivery is always faster (no ramp-up delay)."""
        ns = np.arange(1, 10001, dtype=float)
        t_earth = earth_delivery_time(ns, baseline["prod_rate"])
        t_isru = unit_to_time(ns, baseline["prod_rate"], baseline["t0"], baseline["k_ramp"])
        assert np.all(t_earth <= t_isru)
