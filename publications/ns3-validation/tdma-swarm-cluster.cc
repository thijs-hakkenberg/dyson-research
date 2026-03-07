/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * tdma-swarm-cluster.cc — NS-3 scenario for TDMA swarm cluster validation
 *
 * Independent packet-level simulation to validate the analytical TDMA
 * model in Paper 02 ("Swarm Coordination Scaling").  This scenario
 * creates a star-topology cluster of N nodes (1 coordinator + N-1
 * members) and runs TDMA-scheduled communication for a configurable
 * number of cycles.
 *
 * The simulation derives all timing from first principles:
 *   - Payload framing (CCSDS Proximity-1 inspired)
 *   - FEC expansion (LDPC rate 7/8 or configurable)
 *   - PHY-rate airtime
 *   - Guard intervals (propagation + turnaround + jitter)
 *   - Stochastic antenna acquisition (LogNormal)
 *   - Gilbert-Elliott correlated channel losses
 *   - Stop-and-wait ARQ within cycle margin
 *
 * It does NOT import the Python analytical model.  The gamma (slot
 * efficiency) and deadline miss rate EMERGE from NS-3's own packet-
 * level dynamics.  Agreement within 3-8% of the analytical model
 * validates the paper's claims; systematic disagreement would reveal
 * analytical assumptions that need correction.
 *
 * Output:
 *   - Per-cycle CSV: cycle, sent, received, lost, retx, ingress_ms,
 *     egress_ms, margin_ms, deadline_miss, gamma
 *   - Aggregate summary to stdout
 *   - FlowMonitor XML (if enabled)
 *
 * Usage:
 *   ./ns3 run scratch/tdma-swarm-cluster -- \
 *     --clusterSize=100 --phyRateBps=30000 --numCycles=100 \
 *     --slotConfig=0 --fecRate=0.875 --geEnabled=true \
 *     --stochasticAcq=false --maxRetx=0 --outputPrefix="results/baseline"
 *
 * Authors: Project Dyson (independent validation team)
 * Date: 2026
 */

#include "tdma-net-device.h"
#include "tdma-scheduler.h"
#include "ge-channel-model.h"

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/internet-module.h"
#include "ns3/flow-monitor-module.h"
#include "ns3/applications-module.h"

#include <fstream>
#include <iomanip>
#include <sstream>
#include <cmath>
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
#include <iostream>

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("TdmaSwarmCluster");

// ============================================================================
// Configuration structure for the scenario
// ============================================================================

struct ScenarioConfig
{
    // Cluster topology
    uint32_t clusterSize = 100;        // Total nodes (coordinator + members)

    // Physical layer
    double   phyRateBps = 30000.0;     // PHY rate in bps
    double   fecRate = 0.875;          // FEC code rate (7/8)
    uint32_t payloadBytes = 256;       // Ephemeris payload (S_eph)

    // TDMA parameters
    double   cycleDurationSec = 10.0;  // T_c
    uint32_t slotConfig = 0;           // 0=cold-start, 1=multi-pkt, 2=tracking, 3=bitmap
    uint32_t packetsPerSlot = 3;       // For Config B
    double   guardTimeMs = 4.7;        // Guard interval
    double   acquisitionTimeMs = 5.0;  // Fixed acquisition time
    bool     stochasticAcq = false;    // Enable LogNormal acquisition
    double   acqMuLnMs = 1.6094;      // ln(5.0) for median 5 ms
    double   acqSigmaLn = 0.3;        // LogNormal sigma

    // Channel model
    bool     geEnabled = false;        // Enable GE channel
    double   pGoodToBad = 0.05;        // GE: P(G->B)
    double   pBadToGood = 0.50;        // GE: P(B->G)
    double   pLossGood = 0.01;         // Packet loss in Good state
    double   pLossBad = 0.90;          // Packet loss in Bad state
    bool     perSlotGe = false;        // GE transitions per-slot vs per-cycle

    // ARQ
    uint32_t maxRetx = 0;             // Max retransmission attempts
    uint32_t retxReservedSlots = 0;   // Reserved retransmission slots (M_r)

    // Interference (modeled as increased loss)
    uint32_t numInterferers = 0;       // Number of co-channel interferers
    double   interfererDistance = 3.0; // Relative distance (in cluster radii)

    // Simulation
    uint32_t numCycles = 100;          // Number of TDMA cycles to simulate
    uint32_t seed = 42;                // RNG seed

    // Output
    std::string outputPrefix = "results/baseline";
    bool     enableFlowMonitor = false;
    bool     verbose = false;

    // JSON config file (optional, overrides command-line for sweeps)
    std::string configFile = "";
};

// ============================================================================
// JSON config parser (minimal, for sweep configs)
// ============================================================================

/**
 * \brief Parse a simple JSON config file for parameter sweeps.
 *
 * This is a minimal parser that handles the sweep config format:
 *   { "paramName": [value1, value2, ...], ... }
 *
 * Only used for automated sweep execution via test-tdma-swarm.sh.
 */
static std::vector<double>
extractJsonArray (const std::string& json, const std::string& key)
{
    std::vector<double> result;
    size_t pos = json.find ("\"" + key + "\"");
    if (pos == std::string::npos) return result;

    size_t start = json.find ("[", pos);
    size_t end = json.find ("]", start);
    if (start == std::string::npos || end == std::string::npos) return result;

    std::string arrayStr = json.substr (start + 1, end - start - 1);
    std::istringstream iss (arrayStr);
    std::string token;
    while (std::getline (iss, token, ','))
    {
        // Trim whitespace and quotes
        size_t first = token.find_first_not_of (" \t\n\r\"");
        size_t last = token.find_last_not_of (" \t\n\r\"");
        if (first != std::string::npos)
        {
            std::string val = token.substr (first, last - first + 1);
            try { result.push_back (std::stod (val)); }
            catch (...) {} // Skip non-numeric entries
        }
    }
    return result;
}

static std::vector<std::string>
extractJsonStringArray (const std::string& json, const std::string& key)
{
    std::vector<std::string> result;
    size_t pos = json.find ("\"" + key + "\"");
    if (pos == std::string::npos) return result;

    size_t start = json.find ("[", pos);
    size_t end = json.find ("]", start);
    if (start == std::string::npos || end == std::string::npos) return result;

    std::string arrayStr = json.substr (start + 1, end - start - 1);
    std::istringstream iss (arrayStr);
    std::string token;
    while (std::getline (iss, token, ','))
    {
        size_t first = token.find_first_of ('"');
        size_t last = token.find_last_of ('"');
        if (first != std::string::npos && last > first)
        {
            result.push_back (token.substr (first + 1, last - first - 1));
        }
    }
    return result;
}

// ============================================================================
// Interference model
// ============================================================================

/**
 * \brief Compute additional loss probability from co-channel interference.
 *
 * Models interference as additional noise power from nearby clusters
 * operating on the same frequency.  The SINR degradation depends on
 * the ratio of interferer distance to cluster radius.
 *
 * SINR = S / (N + I)
 * where I = P_tx / R^2 (free-space path loss from interferer)
 *
 * For R = 3 cluster radii: I/S ~ 1/9 -> ~0.5 dB SINR loss
 * For R = 7 cluster radii: I/S ~ 1/49 -> ~0.1 dB SINR loss
 *
 * We model this as an additive packet loss probability:
 *   p_interference = 0.05 * (numInterferers / R^2)
 *
 * This is conservative (worst-case alignment, no directionality gain).
 */
static double
computeInterferenceLoss (uint32_t numInterferers, double relativeDistance)
{
    if (numInterferers == 0 || relativeDistance <= 0.0)
    {
        return 0.0;
    }
    double interference = 0.05 * static_cast<double>(numInterferers)
                          / (relativeDistance * relativeDistance);
    return std::min (interference, 0.5); // cap at 50%
}

// ============================================================================
// Run a single configuration
// ============================================================================

struct SingleRunResult
{
    double gammaScheduler;       // Scheduler-computed gamma
    double gammaMeasured;        // Mean measured gamma from simulation
    double gammaStd;             // Std dev of measured gamma
    double marginMeanMs;         // Mean margin in ms
    double marginMinMs;          // Minimum margin in ms
    double deliveryRate;         // Fraction of reports delivered
    double deadlineMissRate;     // Fraction of cycles with deadline miss
    uint32_t totalDeadlineMisses;
    uint32_t totalRetransmissions;
    uint32_t numCycles;
    std::vector<TdmaCycleStats> cycleStats;
};

static SingleRunResult
runSingleConfig (const ScenarioConfig& cfg)
{
    // ---- Seed NS-3 RNG ----
    RngSeedManager::SetSeed (cfg.seed);
    RngSeedManager::SetRun (1);

    // ---- Create scheduler ----
    Ptr<TdmaScheduler> scheduler = CreateObject<TdmaScheduler> ();

    uint32_t nMembers = cfg.clusterSize - 1;
    TdmaSlotConfig slotCfg = static_cast<TdmaSlotConfig>(cfg.slotConfig);

    // Configure guard time
    scheduler->SetGuardTimeSec (cfg.guardTimeMs / 1000.0);

    // Configure acquisition time
    if (cfg.stochasticAcq)
    {
        scheduler->SetStochasticAcquisition (cfg.acqMuLnMs, cfg.acqSigmaLn);
    }
    else
    {
        scheduler->SetFixedAcquisitionTimeSec (cfg.acquisitionTimeMs / 1000.0);
    }

    // Initialize scheduler (derives all timing from first principles)
    scheduler->Initialize (
        nMembers,
        cfg.cycleDurationSec,
        cfg.phyRateBps,
        cfg.payloadBytes,
        cfg.fecRate,
        slotCfg,
        cfg.packetsPerSlot,
        cfg.retxReservedSlots
    );

    // Log scheduler-computed values
    TdmaSlotTiming timing = scheduler->GetSlotTiming ();
    NS_LOG_INFO ("Scheduler timing:"
                 << " slot=" << (timing.totalSlotSec * 1000.0) << " ms"
                 << " data=" << (timing.dataTimeSec * 1000.0) << " ms"
                 << " guard=" << (timing.guardTimeSec * 1000.0) << " ms"
                 << " acq=" << (timing.acquisitionTimeSec * 1000.0) << " ms"
                 << " gamma=" << timing.gammaSlot
                 << " coded_bits=" << timing.codedTotalBits
                 << " schedulable=" << (scheduler->IsSchedulable () ? "YES" : "NO"));

    // ---- Create GE channel template ----
    Ptr<GeChannelModel> geTemplate = CreateObject<GeChannelModel> ();
    if (cfg.geEnabled)
    {
        geTemplate->SetPgb (cfg.pGoodToBad);
        geTemplate->SetPbg (cfg.pBadToGood);
        geTemplate->SetPLossGood (cfg.pLossGood);
        geTemplate->SetPLossBad (cfg.pLossBad);
        geTemplate->SetFecRate (cfg.fecRate);
        geTemplate->SetPerSlotTransitions (cfg.perSlotGe);
        geTemplate->Enable ();
    }
    else
    {
        // No loss: disable the error model
        geTemplate->SetPLossGood (0.0);
        geTemplate->SetPLossBad (0.0);
        geTemplate->Disable ();
    }

    // Apply interference as additional loss
    double interferLoss = computeInterferenceLoss (cfg.numInterferers,
                                                    cfg.interfererDistance);
    if (interferLoss > 0.0)
    {
        double newPGood = cfg.pLossGood + interferLoss * (1.0 - cfg.pLossGood);
        double newPBad = std::min (0.99, cfg.pLossBad + interferLoss * (1.0 - cfg.pLossBad));
        geTemplate->SetPLossGood (newPGood);
        geTemplate->SetPLossBad (newPBad);
        geTemplate->Enable ();
    }

    // ---- Create TDMA coordinator device ----
    // In this simulation, we don't create a full NS-3 topology with
    // PointToPointNetDevice.  Instead, we use TdmaNetDevice as a
    // self-contained simulation engine that models the TDMA protocol
    // at the packet level, using NS-3's event scheduler and RNG.
    //
    // This is equivalent to creating N PointToPoint links but faster
    // and more focused on the MAC-layer behavior we're validating.

    Ptr<Node> coordinatorNode = CreateObject<Node> ();
    Ptr<TdmaNetDevice> coordinator = CreateObject<TdmaNetDevice> ();
    coordinator->SetRole (TDMA_COORDINATOR);
    coordinator->SetNode (coordinatorNode);
    coordinator->SetScheduler (scheduler);
    coordinator->SetGeChannel (geTemplate);
    coordinator->SetNumCycles (cfg.numCycles);
    coordinator->SetPayloadBytes (cfg.payloadBytes);
    coordinator->SetMaxRetransmissions (cfg.maxRetx);
    coordinator->SetStochasticAcquisition (cfg.stochasticAcq);

    // ---- Run simulation ----
    coordinator->Start ();

    // Total simulation time = numCycles * T_c
    double totalTimeSec = cfg.numCycles * cfg.cycleDurationSec;
    Simulator::Stop (Seconds (totalTimeSec + 1.0));
    Simulator::Run ();

    // ---- Collect results ----
    auto aggStats = coordinator->GetAggregateStats ();
    auto cycleStats = coordinator->GetCycleStats ();

    SingleRunResult result;
    result.gammaScheduler = scheduler->GetGamma ();
    result.gammaMeasured = aggStats.meanGamma;
    result.marginMeanMs = aggStats.meanMarginSec * 1000.0;
    result.marginMinMs = aggStats.minMarginSec * 1000.0;
    result.deliveryRate = aggStats.deliveryRate;
    result.deadlineMissRate = aggStats.deadlineMissRate;
    result.totalDeadlineMisses = aggStats.totalDeadlineMisses;
    result.totalRetransmissions = aggStats.totalRetransmissions;
    result.numCycles = aggStats.totalCycles;
    result.cycleStats = cycleStats;

    // Compute gamma std dev
    if (cycleStats.size () > 1)
    {
        double sumSq = 0.0;
        for (const auto& s : cycleStats)
        {
            double diff = s.actualGamma - result.gammaMeasured;
            sumSq += diff * diff;
        }
        result.gammaStd = std::sqrt (sumSq / (cycleStats.size () - 1));
    }
    else
    {
        result.gammaStd = 0.0;
    }

    Simulator::Destroy ();
    return result;
}

// ============================================================================
// Output functions
// ============================================================================

/**
 * \brief Write per-cycle CSV output.
 */
static void
writeCycleCsv (const std::string& filename,
               const std::vector<TdmaCycleStats>& stats)
{
    std::ofstream ofs (filename);
    ofs << "cycle,sent,received,lost,retransmissions,"
        << "ingress_ms,egress_ms,margin_ms,deadline_miss,gamma\n";

    for (const auto& s : stats)
    {
        ofs << s.cycleNumber << ","
            << s.reportsSent << ","
            << s.reportsReceived << ","
            << s.reportsLost << ","
            << s.retransmissions << ","
            << std::fixed << std::setprecision (3)
            << (s.ingressDurationSec * 1000.0) << ","
            << (s.egressDurationSec * 1000.0) << ","
            << (s.marginSec * 1000.0) << ","
            << (s.deadlineMiss ? 1 : 0) << ","
            << std::setprecision (6)
            << s.actualGamma << "\n";
    }

    ofs.close ();
    std::cout << "  Wrote per-cycle CSV: " << filename << std::endl;
}

/**
 * \brief Write aggregate summary CSV (one row per configuration).
 */
static void
writeSummaryCsv (const std::string& filename,
                 const ScenarioConfig& cfg,
                 const SingleRunResult& result)
{
    // Append to file (create header if new)
    bool fileExists = false;
    {
        std::ifstream check (filename);
        fileExists = check.good () && check.peek () != std::ifstream::traits_type::eof ();
    }

    std::ofstream ofs (filename, std::ios::app);
    if (!fileExists)
    {
        ofs << "cluster_size,phy_rate_bps,fec_rate,slot_config,"
            << "guard_time_ms,acq_time_ms,stochastic_acq,"
            << "ge_enabled,p_gb,p_bg,p_loss_good,p_loss_bad,"
            << "max_retx,num_interferers,interferer_distance,"
            << "num_cycles,gamma_scheduler,gamma_measured,gamma_std,"
            << "margin_mean_ms,margin_min_ms,"
            << "delivery_rate,deadline_miss_rate,"
            << "total_deadline_misses,total_retransmissions\n";
    }

    ofs << cfg.clusterSize << ","
        << cfg.phyRateBps << ","
        << cfg.fecRate << ","
        << cfg.slotConfig << ","
        << cfg.guardTimeMs << ","
        << cfg.acquisitionTimeMs << ","
        << (cfg.stochasticAcq ? 1 : 0) << ","
        << (cfg.geEnabled ? 1 : 0) << ","
        << cfg.pGoodToBad << ","
        << cfg.pBadToGood << ","
        << cfg.pLossGood << ","
        << cfg.pLossBad << ","
        << cfg.maxRetx << ","
        << cfg.numInterferers << ","
        << cfg.interfererDistance << ","
        << result.numCycles << ","
        << std::fixed << std::setprecision (6)
        << result.gammaScheduler << ","
        << result.gammaMeasured << ","
        << result.gammaStd << ","
        << std::setprecision (3)
        << result.marginMeanMs << ","
        << result.marginMinMs << ","
        << std::setprecision (6)
        << result.deliveryRate << ","
        << result.deadlineMissRate << ","
        << result.totalDeadlineMisses << ","
        << result.totalRetransmissions << "\n";

    ofs.close ();
}

/**
 * \brief Print aggregate results to stdout.
 */
static void
printSummary (const ScenarioConfig& cfg, const SingleRunResult& result)
{
    std::cout << "\n"
              << "================================================================\n"
              << "  TDMA Swarm Cluster Validation — NS-3 Results\n"
              << "================================================================\n"
              << "\n"
              << "Configuration:\n"
              << "  Cluster size:       " << cfg.clusterSize << " nodes\n"
              << "  PHY rate:           " << cfg.phyRateBps << " bps ("
                                          << (cfg.phyRateBps / 1000.0) << " kbps)\n"
              << "  FEC rate:           " << cfg.fecRate << "\n"
              << "  Payload:            " << cfg.payloadBytes << " bytes\n"
              << "  Cycle duration:     " << cfg.cycleDurationSec << " s\n"
              << "  Slot config:        " << cfg.slotConfig
                << " (" << (cfg.slotConfig == 0 ? "cold-start"
                          : cfg.slotConfig == 1 ? "multi-packet"
                          : cfg.slotConfig == 2 ? "tracking"
                          : "bitmap-ACK") << ")\n"
              << "  Guard time:         " << cfg.guardTimeMs << " ms\n"
              << "  Acquisition:        " << cfg.acquisitionTimeMs << " ms"
                << (cfg.stochasticAcq ? " (stochastic)" : " (fixed)") << "\n"
              << "  GE channel:         " << (cfg.geEnabled ? "enabled" : "disabled") << "\n";
    if (cfg.geEnabled)
    {
        std::cout
              << "    P(G->B):          " << cfg.pGoodToBad << "\n"
              << "    P(B->G):          " << cfg.pBadToGood << "\n"
              << "    P(loss|Good):     " << cfg.pLossGood << "\n"
              << "    P(loss|Bad):      " << cfg.pLossBad << "\n";
    }
    std::cout
              << "  Max retransmissions:" << cfg.maxRetx << "\n"
              << "  Interferers:        " << cfg.numInterferers << "\n"
              << "  Num cycles:         " << cfg.numCycles << "\n"
              << "\n"
              << "Results:\n"
              << "  Scheduler gamma:    " << std::fixed << std::setprecision (4)
                                          << result.gammaScheduler << "\n"
              << "  Measured gamma:     " << result.gammaMeasured
                << " +/- " << result.gammaStd << "\n"
              << "  Gamma difference:   "
                << std::abs (result.gammaScheduler - result.gammaMeasured)
                << " (" << std::setprecision (1)
                << (std::abs (result.gammaScheduler - result.gammaMeasured)
                    / result.gammaScheduler * 100.0) << "%)\n"
              << std::setprecision (3)
              << "  Margin (mean):      " << result.marginMeanMs << " ms\n"
              << "  Margin (min):       " << result.marginMinMs << " ms\n"
              << "  Delivery rate:      " << std::setprecision (4) << result.deliveryRate << "\n"
              << "  Deadline miss rate: " << result.deadlineMissRate << "\n"
              << "  Total misses:       " << result.totalDeadlineMisses
                << " / " << result.numCycles << "\n"
              << "  Total retx:         " << result.totalRetransmissions << "\n"
              << "================================================================\n"
              << std::endl;
}

// ============================================================================
// Sweep execution
// ============================================================================

/**
 * \brief Run a parameter sweep from a JSON config file.
 *
 * Reads the sweep parameters and runs all combinations, writing
 * results to the summary CSV.
 */
static void
runSweep (const ScenarioConfig& baseCfg, const std::string& configFile)
{
    // Read config file
    std::ifstream ifs (configFile);
    if (!ifs.is_open ())
    {
        std::cerr << "ERROR: Cannot open config file: " << configFile << std::endl;
        return;
    }
    std::string json ((std::istreambuf_iterator<char>(ifs)),
                       std::istreambuf_iterator<char>());
    ifs.close ();

    // Parse sweep parameters
    auto phyRates = extractJsonArray (json, "phyRateBps");
    auto clusterSizes = extractJsonArray (json, "clusterSize");
    auto maxRetxVals = extractJsonArray (json, "maxRetx");
    auto slotConfigs = extractJsonArray (json, "slotConfig");
    auto geStates = extractJsonStringArray (json, "geState");
    auto interference = extractJsonStringArray (json, "interference");

    // Defaults if not specified
    if (phyRates.empty ()) phyRates.push_back (baseCfg.phyRateBps);
    if (clusterSizes.empty ()) clusterSizes.push_back (baseCfg.clusterSize);
    if (maxRetxVals.empty ()) maxRetxVals.push_back (baseCfg.maxRetx);
    if (slotConfigs.empty ()) slotConfigs.push_back (baseCfg.slotConfig);
    if (geStates.empty ()) geStates.push_back ("no-loss");
    if (interference.empty ()) interference.push_back ("none");

    std::string summaryFile = baseCfg.outputPrefix + "_sweep_summary.csv";

    uint32_t totalConfigs = phyRates.size () * clusterSizes.size ()
                            * maxRetxVals.size () * slotConfigs.size ()
                            * geStates.size () * interference.size ();
    uint32_t configIdx = 0;

    std::cout << "Running sweep: " << totalConfigs << " configurations" << std::endl;

    for (double rate : phyRates)
    {
        for (double sz : clusterSizes)
        {
            for (double mr : maxRetxVals)
            {
                for (double sc : slotConfigs)
                {
                    for (const auto& ge : geStates)
                    {
                        for (const auto& interf : interference)
                        {
                            configIdx++;
                            ScenarioConfig cfg = baseCfg;
                            cfg.phyRateBps = rate;
                            cfg.clusterSize = static_cast<uint32_t>(sz);
                            cfg.maxRetx = static_cast<uint32_t>(mr);
                            cfg.slotConfig = static_cast<uint32_t>(sc);

                            // GE state
                            if (ge == "no-loss")
                            {
                                cfg.geEnabled = false;
                            }
                            else if (ge == "GE-default")
                            {
                                cfg.geEnabled = true;
                                cfg.pGoodToBad = 0.05;
                                cfg.pBadToGood = 0.50;
                                cfg.pLossGood = 0.01;
                                cfg.pLossBad = 0.90;
                            }
                            else if (ge == "GE-severe")
                            {
                                cfg.geEnabled = true;
                                cfg.pGoodToBad = 0.10;
                                cfg.pBadToGood = 0.30;
                                cfg.pLossGood = 0.05;
                                cfg.pLossBad = 0.95;
                            }

                            // Interference
                            if (interf == "none")
                            {
                                cfg.numInterferers = 0;
                            }
                            else if (interf == "1-interferer-R=3")
                            {
                                cfg.numInterferers = 1;
                                cfg.interfererDistance = 3.0;
                            }
                            else if (interf == "1-interferer-R=7")
                            {
                                cfg.numInterferers = 1;
                                cfg.interfererDistance = 7.0;
                            }

                            std::cout << "  [" << configIdx << "/"
                                      << totalConfigs << "] "
                                      << "N=" << cfg.clusterSize
                                      << " R=" << (cfg.phyRateBps/1000)
                                      << "k M_r=" << cfg.maxRetx
                                      << " cfg=" << cfg.slotConfig
                                      << " GE=" << ge
                                      << " interf=" << interf
                                      << " ... " << std::flush;

                            auto result = runSingleConfig (cfg);

                            std::cout << "gamma=" << std::fixed
                                      << std::setprecision (3)
                                      << result.gammaMeasured
                                      << " miss=" << result.deadlineMissRate
                                      << std::endl;

                            writeSummaryCsv (summaryFile, cfg, result);
                        }
                    }
                }
            }
        }
    }

    std::cout << "\nSweep complete. Results: " << summaryFile << std::endl;
}

// ============================================================================
// Main
// ============================================================================

int
main (int argc, char *argv[])
{
    ScenarioConfig cfg;

    // ---- Command-line parsing ----
    CommandLine cmd (__FILE__);
    cmd.AddValue ("clusterSize", "Total cluster size N (coordinator + members)",
                  cfg.clusterSize);
    cmd.AddValue ("phyRateBps", "Physical layer rate in bps",
                  cfg.phyRateBps);
    cmd.AddValue ("fecRate", "FEC code rate (e.g. 0.875 for rate 7/8)",
                  cfg.fecRate);
    cmd.AddValue ("payloadBytes", "Ephemeris payload size in bytes",
                  cfg.payloadBytes);
    cmd.AddValue ("cycleDuration", "TDMA cycle duration T_c in seconds",
                  cfg.cycleDurationSec);
    cmd.AddValue ("slotConfig", "Slot config: 0=cold, 1=multi, 2=track, 3=bitmap",
                  cfg.slotConfig);
    cmd.AddValue ("packetsPerSlot", "Packets per slot (Config B)",
                  cfg.packetsPerSlot);
    cmd.AddValue ("guardTimeMs", "Guard interval in ms",
                  cfg.guardTimeMs);
    cmd.AddValue ("acquisitionTimeMs", "Fixed acquisition time in ms",
                  cfg.acquisitionTimeMs);
    cmd.AddValue ("stochasticAcq", "Enable stochastic acquisition (LogNormal)",
                  cfg.stochasticAcq);
    cmd.AddValue ("acqMuLnMs", "LogNormal mu for acquisition (ln(ms))",
                  cfg.acqMuLnMs);
    cmd.AddValue ("acqSigmaLn", "LogNormal sigma for acquisition",
                  cfg.acqSigmaLn);
    cmd.AddValue ("geEnabled", "Enable Gilbert-Elliott channel",
                  cfg.geEnabled);
    cmd.AddValue ("pGoodToBad", "GE: P(Good -> Bad)",
                  cfg.pGoodToBad);
    cmd.AddValue ("pBadToGood", "GE: P(Bad -> Good)",
                  cfg.pBadToGood);
    cmd.AddValue ("pLossGood", "Packet loss in Good state",
                  cfg.pLossGood);
    cmd.AddValue ("pLossBad", "Packet loss in Bad state",
                  cfg.pLossBad);
    cmd.AddValue ("perSlotGe", "GE transitions per-slot (vs per-cycle)",
                  cfg.perSlotGe);
    cmd.AddValue ("maxRetx", "Max ARQ retransmissions per slot",
                  cfg.maxRetx);
    cmd.AddValue ("retxReservedSlots", "Reserved retransmission slots M_r",
                  cfg.retxReservedSlots);
    cmd.AddValue ("numInterferers", "Number of co-channel interferer clusters",
                  cfg.numInterferers);
    cmd.AddValue ("interfererDistance", "Interferer distance (in cluster radii)",
                  cfg.interfererDistance);
    cmd.AddValue ("numCycles", "Number of TDMA cycles to simulate",
                  cfg.numCycles);
    cmd.AddValue ("seed", "RNG seed",
                  cfg.seed);
    cmd.AddValue ("outputPrefix", "Output file prefix",
                  cfg.outputPrefix);
    cmd.AddValue ("enableFlowMonitor", "Enable FlowMonitor XML output",
                  cfg.enableFlowMonitor);
    cmd.AddValue ("verbose", "Enable verbose logging",
                  cfg.verbose);
    cmd.AddValue ("configFile", "JSON config file for parameter sweeps",
                  cfg.configFile);
    cmd.Parse (argc, argv);

    // ---- Logging ----
    if (cfg.verbose)
    {
        LogComponentEnable ("TdmaSwarmCluster", LOG_LEVEL_ALL);
        LogComponentEnable ("TdmaNetDevice", LOG_LEVEL_INFO);
        LogComponentEnable ("TdmaScheduler", LOG_LEVEL_INFO);
        LogComponentEnable ("GeChannelModel", LOG_LEVEL_DEBUG);
    }
    else
    {
        LogComponentEnable ("TdmaSwarmCluster", LOG_LEVEL_INFO);
    }

    // ---- Sweep mode ----
    if (!cfg.configFile.empty ())
    {
        runSweep (cfg, cfg.configFile);
        return 0;
    }

    // ---- Single run ----
    auto result = runSingleConfig (cfg);

    // ---- Output ----
    printSummary (cfg, result);

    // Write per-cycle CSV
    std::string cycleCsvFile = cfg.outputPrefix + "_cycles.csv";
    writeCycleCsv (cycleCsvFile, result.cycleStats);

    // Write summary CSV
    std::string summaryFile = cfg.outputPrefix + "_summary.csv";
    writeSummaryCsv (summaryFile, cfg, result);

    return 0;
}
