#!/usr/bin/env bash
# ============================================================================
# test-tdma-swarm.sh — Automated validation test suite for TDMA swarm cluster
#
# Builds the NS-3 scenario and runs a series of validation checks against
# the analytical model predictions from Paper 02.
#
# Each check has a clear PASS/FAIL criterion.  The tests are designed to
# verify that NS-3's independently-derived results agree with the analytical
# model within expected tolerances.
#
# Usage:
#   cd <ns3-directory>
#   cp -r <this-directory> scratch/tdma-swarm-cluster
#   bash scratch/tdma-swarm-cluster/test-tdma-swarm.sh
#
# Requirements:
#   - NS-3 built and ns3 wrapper available in PATH or current directory
#   - The tdma-swarm-cluster scenario copied to scratch/
#
# Exit code: 0 if all checks pass, 1 if any check fails.
# ============================================================================

set -euo pipefail

# Determine NS-3 runner
NS3_RUN=""
if command -v ./ns3 &>/dev/null; then
    NS3_RUN="./ns3 run"
elif command -v ns3 &>/dev/null; then
    NS3_RUN="ns3 run"
else
    echo "ERROR: Cannot find NS-3 runner (./ns3 or ns3 in PATH)."
    echo "Please run this script from the NS-3 top-level directory."
    exit 1
fi

SCENARIO="scratch/tdma-swarm-cluster"
RESULTS_DIR="scratch/tdma-swarm-cluster/results"
mkdir -p "$RESULTS_DIR"

PASS_COUNT=0
FAIL_COUNT=0

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

pass() {
    echo -e "  ${GREEN}PASS${NC}: $1"
    PASS_COUNT=$((PASS_COUNT + 1))
}

fail() {
    echo -e "  ${RED}FAIL${NC}: $1"
    FAIL_COUNT=$((FAIL_COUNT + 1))
}

info() {
    echo -e "  ${YELLOW}INFO${NC}: $1"
}

# ============================================================================
# Step 0: Build
# ============================================================================
echo "================================================================"
echo "  Building TDMA Swarm Cluster scenario"
echo "================================================================"

if $NS3_RUN --no-build $SCENARIO -- --help &>/dev/null 2>&1; then
    info "Scenario already built."
else
    echo "Building..."
    $NS3_RUN $SCENARIO --no-build 2>&1 || {
        echo "Attempting full build..."
        ./ns3 build $SCENARIO 2>&1
    }
fi

echo ""

# ============================================================================
# Test 1: Baseline gamma at 30 kbps, N=100, cold-start
# Expected: gamma in [0.70, 0.80] (analytical model gives ~0.73)
# ============================================================================
echo "================================================================"
echo "  Test 1: Baseline gamma at 30 kbps, N=100, cold-start"
echo "================================================================"

$NS3_RUN $SCENARIO -- \
    --clusterSize=100 --phyRateBps=30000 --fecRate=0.875 \
    --slotConfig=0 --numCycles=100 --geEnabled=false \
    --stochasticAcq=false \
    --outputPrefix="$RESULTS_DIR/test1" 2>&1 | tee "$RESULTS_DIR/test1_stdout.txt"

# Extract measured gamma from the summary CSV
GAMMA_MEASURED=$(tail -1 "$RESULTS_DIR/test1_summary.csv" | cut -d',' -f18)
info "Measured gamma = $GAMMA_MEASURED"

# Check: gamma in [0.70, 0.80]
if (( $(echo "$GAMMA_MEASURED >= 0.70 && $GAMMA_MEASURED <= 0.80" | bc -l) )); then
    pass "gamma = $GAMMA_MEASURED is in [0.70, 0.80]"
else
    fail "gamma = $GAMMA_MEASURED is NOT in [0.70, 0.80]"
fi

echo ""

# ============================================================================
# Test 2: Zero deadline misses at 35 kbps, no loss
# Expected: 0 deadline misses (35 kbps gives comfortable margin)
# ============================================================================
echo "================================================================"
echo "  Test 2: Zero deadline misses at 35 kbps, no loss"
echo "================================================================"

$NS3_RUN $SCENARIO -- \
    --clusterSize=100 --phyRateBps=35000 --fecRate=0.875 \
    --slotConfig=0 --numCycles=200 --geEnabled=false \
    --stochasticAcq=false \
    --outputPrefix="$RESULTS_DIR/test2" 2>&1 | tee "$RESULTS_DIR/test2_stdout.txt"

MISSES=$(tail -1 "$RESULTS_DIR/test2_summary.csv" | cut -d',' -f23)
info "Deadline misses = $MISSES"

if [ "$MISSES" = "0" ]; then
    pass "Zero deadline misses at 35 kbps no-loss"
else
    fail "Expected 0 deadline misses, got $MISSES"
fi

echo ""

# ============================================================================
# Test 3: 100% deadline misses at 24 kbps, cold-start, N=100
# Expected: 100% miss rate (24 kbps is infeasible for 100 nodes)
# Analytical: 99 slots * ~105 ms/slot = ~10,395 ms > T_c = 10,000 ms
# ============================================================================
echo "================================================================"
echo "  Test 3: 100% deadline misses at 24 kbps, N=100"
echo "================================================================"

$NS3_RUN $SCENARIO -- \
    --clusterSize=100 --phyRateBps=24000 --fecRate=0.875 \
    --slotConfig=0 --numCycles=50 --geEnabled=false \
    --stochasticAcq=false \
    --outputPrefix="$RESULTS_DIR/test3" 2>&1 | tee "$RESULTS_DIR/test3_stdout.txt"

MISS_RATE=$(tail -1 "$RESULTS_DIR/test3_summary.csv" | cut -d',' -f22)
info "Deadline miss rate = $MISS_RATE"

# Check: miss rate >= 0.99 (allowing tiny floating-point tolerance)
if (( $(echo "$MISS_RATE >= 0.99" | bc -l) )); then
    pass "~100% deadline misses at 24 kbps (miss_rate=$MISS_RATE)"
else
    fail "Expected ~100% deadline misses, got miss_rate=$MISS_RATE"
fi

echo ""

# ============================================================================
# Test 4: Stochastic acquisition produces wider distribution
# Compare fixed vs stochastic acquisition at 30 kbps
# Expected: stochastic has larger ingress time variance
# ============================================================================
echo "================================================================"
echo "  Test 4: Stochastic acquisition variance check"
echo "================================================================"

# Fixed acquisition
$NS3_RUN $SCENARIO -- \
    --clusterSize=100 --phyRateBps=30000 --fecRate=0.875 \
    --slotConfig=0 --numCycles=200 --geEnabled=false \
    --stochasticAcq=false \
    --outputPrefix="$RESULTS_DIR/test4_fixed" 2>&1 > "$RESULTS_DIR/test4_fixed_stdout.txt"

# Stochastic acquisition
$NS3_RUN $SCENARIO -- \
    --clusterSize=100 --phyRateBps=30000 --fecRate=0.875 \
    --slotConfig=0 --numCycles=200 --geEnabled=false \
    --stochasticAcq=true \
    --outputPrefix="$RESULTS_DIR/test4_stoch" 2>&1 > "$RESULTS_DIR/test4_stoch_stdout.txt"

# Extract gamma std dev from summary CSVs
GAMMA_STD_FIXED=$(tail -1 "$RESULTS_DIR/test4_fixed_summary.csv" | cut -d',' -f19)
GAMMA_STD_STOCH=$(tail -1 "$RESULTS_DIR/test4_stoch_summary.csv" | cut -d',' -f19)

info "Gamma std (fixed acq):      $GAMMA_STD_FIXED"
info "Gamma std (stochastic acq): $GAMMA_STD_STOCH"

# For fixed acquisition with no loss, gamma std should be ~0 (deterministic)
# For stochastic, gamma std should be measurably larger
if (( $(echo "$GAMMA_STD_STOCH > $GAMMA_STD_FIXED" | bc -l) )); then
    pass "Stochastic acquisition produces wider gamma distribution"
else
    fail "Expected stochastic gamma_std > fixed gamma_std"
fi

echo ""

# ============================================================================
# Test 5: GE channel reduces delivery rate
# Expected: GE-default causes delivery_rate < 1.0
# ============================================================================
echo "================================================================"
echo "  Test 5: GE channel reduces delivery rate"
echo "================================================================"

$NS3_RUN $SCENARIO -- \
    --clusterSize=100 --phyRateBps=35000 --fecRate=0.875 \
    --slotConfig=0 --numCycles=200 --geEnabled=true \
    --pGoodToBad=0.05 --pBadToGood=0.50 \
    --pLossGood=0.01 --pLossBad=0.90 \
    --stochasticAcq=false --maxRetx=0 \
    --outputPrefix="$RESULTS_DIR/test5" 2>&1 | tee "$RESULTS_DIR/test5_stdout.txt"

DELIVERY=$(tail -1 "$RESULTS_DIR/test5_summary.csv" | cut -d',' -f21)
info "Delivery rate under GE = $DELIVERY"

# GE steady-state bad prob = 0.05/(0.05+0.50) = 0.0909
# Expected loss ~ 0.01*(1-0.0909) + 0.90*0.0909 ~ 0.091
# So delivery ~ 0.91
if (( $(echo "$DELIVERY < 1.0 && $DELIVERY > 0.80" | bc -l) )); then
    pass "GE channel causes delivery_rate=$DELIVERY (expected ~0.91)"
else
    fail "Unexpected delivery_rate=$DELIVERY under GE channel"
fi

echo ""

# ============================================================================
# Test 6: ARQ improves delivery under GE
# Expected: M_r=1 improves delivery compared to M_r=0
# ============================================================================
echo "================================================================"
echo "  Test 6: ARQ improves delivery rate under GE"
echo "================================================================"

$NS3_RUN $SCENARIO -- \
    --clusterSize=100 --phyRateBps=35000 --fecRate=0.875 \
    --slotConfig=0 --numCycles=200 --geEnabled=true \
    --pGoodToBad=0.05 --pBadToGood=0.50 \
    --pLossGood=0.01 --pLossBad=0.90 \
    --stochasticAcq=false --maxRetx=1 \
    --outputPrefix="$RESULTS_DIR/test6" 2>&1 | tee "$RESULTS_DIR/test6_stdout.txt"

DELIVERY_ARQ=$(tail -1 "$RESULTS_DIR/test6_summary.csv" | cut -d',' -f21)
info "Delivery rate with ARQ M_r=1 = $DELIVERY_ARQ"
info "Delivery rate without ARQ     = $DELIVERY"

if (( $(echo "$DELIVERY_ARQ > $DELIVERY" | bc -l) )); then
    pass "ARQ improves delivery: $DELIVERY_ARQ > $DELIVERY"
else
    fail "Expected ARQ to improve delivery: got $DELIVERY_ARQ <= $DELIVERY"
fi

echo ""

# ============================================================================
# Test 7: Tracking mode (Config C) has higher gamma than cold-start
# Expected: gamma_tracking > gamma_cold_start
# ============================================================================
echo "================================================================"
echo "  Test 7: Tracking mode gamma > cold-start gamma"
echo "================================================================"

$NS3_RUN $SCENARIO -- \
    --clusterSize=100 --phyRateBps=30000 --fecRate=0.875 \
    --slotConfig=2 --numCycles=100 --geEnabled=false \
    --stochasticAcq=false \
    --outputPrefix="$RESULTS_DIR/test7" 2>&1 > "$RESULTS_DIR/test7_stdout.txt"

GAMMA_TRACK=$(tail -1 "$RESULTS_DIR/test7_summary.csv" | cut -d',' -f18)
info "Gamma (cold-start):     $GAMMA_MEASURED"
info "Gamma (tracking mode):  $GAMMA_TRACK"

if (( $(echo "$GAMMA_TRACK > $GAMMA_MEASURED" | bc -l) )); then
    pass "Tracking mode gamma ($GAMMA_TRACK) > cold-start gamma ($GAMMA_MEASURED)"
else
    fail "Expected tracking gamma > cold-start gamma"
fi

echo ""

# ============================================================================
# Summary
# ============================================================================
echo "================================================================"
echo "  Test Summary"
echo "================================================================"
echo ""
echo "  Passed: $PASS_COUNT"
echo "  Failed: $FAIL_COUNT"
echo "  Total:  $((PASS_COUNT + FAIL_COUNT))"
echo ""

if [ "$FAIL_COUNT" -gt 0 ]; then
    echo -e "  ${RED}SOME TESTS FAILED${NC}"
    exit 1
else
    echo -e "  ${GREEN}ALL TESTS PASSED${NC}"
    exit 0
fi
