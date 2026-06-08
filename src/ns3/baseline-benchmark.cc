/* =============================================================================
 * Phase 3 Baseline Benchmark: Single Bottleneck TCP Congestion Experiment
 * Project: DRL for Congestion Control and Throughput Optimization
 * OpenSpec Change 02: ns3-baseline-benchmark
 *
 * Topology:
 *   Sender ─── Access Link ─── Bottleneck Router ─── Access Link ─── Receiver
 *
 * Supported TCP variants: TcpNewReno, TcpCubic, TcpBbr (if available)
 *
 * Usage:
 *   ./ns3 run 'scratch/baseline-benchmark --tcpVariant=TcpNewReno
 *              --scenario=S1 --simDuration=60 --seed=42 --runId=run_001
 *              --outputDir=/path/to/experiments/raw_logs'
 *
 * PHASE 3 SCOPE:
 *   - NO ns3-gym, NO DQN, NO RL environment
 *   - Only baseline TCP measurement
 * =============================================================================
 */

#include "ns3/applications-module.h"
#include "ns3/core-module.h"
#include "ns3/flow-monitor-helper.h"
#include "ns3/internet-module.h"
#include "ns3/network-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/traffic-control-module.h"

#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>

using namespace ns3;

NS_LOG_COMPONENT_DEFINE("BaselineBenchmark");

// ─── Scenario Parameters ───────────────────────────────────────────────────
struct ScenarioConfig
{
    std::string scenarioId;
    std::string bottleneckBw;    // Bottleneck link bandwidth (e.g., "10Mbps")
    std::string bottleneckDelay; // Bottleneck link one-way delay
    std::string accessBw;        // Sender/receiver access link BW
    std::string accessDelay;     // Sender/receiver access link delay
    uint32_t queueSize;          // Bottleneck queue size (packets)
    double simDuration;          // Total simulation time (seconds)
    double measureStart;         // Start collecting metrics at (seconds)
    std::string description;
};

ScenarioConfig
GetScenarioConfig(const std::string& scenarioId, double simDuration)
{
    ScenarioConfig cfg;
    cfg.simDuration = simDuration;

    if (scenarioId == "S1" || scenarioId == "scenario_a")
    {
        // S1: Stable low-delay bottleneck (MVP-required)
        cfg.scenarioId = "S1";
        cfg.bottleneckBw = "10Mbps";
        cfg.bottleneckDelay = "10ms";
        cfg.accessBw = "100Mbps";
        cfg.accessDelay = "1ms";
        cfg.queueSize = 100;
        cfg.measureStart = 5.0; // Skip first 5s warmup
        cfg.description = "Stable low-delay bottleneck: 10Mbps BW, 10ms delay";
    }
    else if (scenarioId == "S2" || scenarioId == "scenario_b")
    {
        // S2: Stable high-delay bottleneck (MVP-required)
        cfg.scenarioId = "S2";
        cfg.bottleneckBw = "10Mbps";
        cfg.bottleneckDelay = "50ms";
        cfg.accessBw = "100Mbps";
        cfg.accessDelay = "1ms";
        cfg.queueSize = 100;
        cfg.measureStart = 5.0;
        cfg.description = "Stable high-delay bottleneck: 10Mbps BW, 50ms delay";
    }
    else if (scenarioId == "S3")
    {
        // S3: Variable bandwidth (should-have, non-blocking)
        cfg.scenarioId = "S3";
        cfg.bottleneckBw = "10Mbps";
        cfg.bottleneckDelay = "10ms";
        cfg.accessBw = "100Mbps";
        cfg.accessDelay = "1ms";
        cfg.queueSize = 50; // Smaller queue for variable BW effect
        cfg.measureStart = 5.0;
        cfg.description = "Variable bandwidth-like: 10Mbps BW, small queue, 10ms delay";
    }
    else if (scenarioId == "S4")
    {
        // S4: Cross traffic (optional)
        cfg.scenarioId = "S4";
        cfg.bottleneckBw = "10Mbps";
        cfg.bottleneckDelay = "10ms";
        cfg.accessBw = "100Mbps";
        cfg.accessDelay = "1ms";
        cfg.queueSize = 100;
        cfg.measureStart = 5.0;
        cfg.description = "Bottleneck with cross traffic (1 interfering flow)";
    }
    else
    {
        // Default fallback to S1
        NS_LOG_WARN("Unknown scenario '" << scenarioId << "', defaulting to S1");
        return GetScenarioConfig("S1", simDuration);
    }

    return cfg;
}

// ─── Main ─────────────────────────────────────────────────────────────────
int
main(int argc, char* argv[])
{
    // ── Command-line parameters ──
    std::string tcpVariant = "TcpNewReno";
    std::string scenarioId = "S1";
    double simDuration = 60.0;
    uint32_t seed = 42;
    uint32_t run = 1;
    std::string runId = "run_001";
    std::string outputDir = "/tmp/ns3-baseline-output";
    bool enableCrossTraffic = false;
    bool verbose = false;

    CommandLine cmd(__FILE__);
    cmd.AddValue("tcpVariant",
                 "TCP congestion control variant (TcpNewReno, TcpCubic, TcpBbr)",
                 tcpVariant);
    cmd.AddValue("scenario", "Scenario ID: S1, S2, S3, S4", scenarioId);
    cmd.AddValue("simDuration", "Total simulation duration (seconds)", simDuration);
    cmd.AddValue("seed", "Random seed", seed);
    cmd.AddValue("run", "Run number", run);
    cmd.AddValue("runId", "Run identifier string (e.g., run_001)", runId);
    cmd.AddValue("outputDir", "Directory for output CSV and log files", outputDir);
    cmd.AddValue("crossTraffic",
                 "Enable cross traffic (for S4)",
                 enableCrossTraffic);
    cmd.AddValue("verbose", "Enable verbose logging", verbose);
    cmd.Parse(argc, argv);

    // ── Random seed ──
    RngSeedManager::SetSeed(seed);
    RngSeedManager::SetRun(run);

    // ── TCP variant setup ──
    TypeId tcpTid;
    std::string tcpName = tcpVariant;
    bool tcpFound = true;
    if (TypeId::LookupByNameFailSafe(tcpVariant, &tcpTid))
    {
        Config::SetDefault("ns3::TcpL4Protocol::SocketType", TypeIdValue(tcpTid));
    }
    else
    {
        NS_LOG_WARN("TCP variant '" << tcpVariant
                                   << "' not found. Falling back to TcpNewReno.");
        tcpFound = false;
        tcpName = "TcpNewReno_fallback";
        TypeId fallbackTid;
        TypeId::LookupByNameFailSafe("ns3::TcpNewReno", &fallbackTid);
        Config::SetDefault("ns3::TcpL4Protocol::SocketType",
                           TypeIdValue(fallbackTid));
    }

    // ── Scenario config ──
    ScenarioConfig cfg = GetScenarioConfig(scenarioId, simDuration);
    double measureStart = cfg.measureStart;
    double measureEnd = simDuration - 2.0;
    if (measureEnd <= measureStart)
        measureEnd = simDuration;

    if (verbose)
    {
        LogComponentEnable("BaselineBenchmark", LOG_LEVEL_INFO);
    }

    std::cout << "=== ns-3.40 Baseline Benchmark ===" << std::endl;
    std::cout << "Scenario:    " << cfg.scenarioId << " | " << cfg.description << std::endl;
    std::cout << "TCP Variant: " << tcpVariant << (tcpFound ? "" : " (NOT FOUND → fallback to NewReno)") << std::endl;
    std::cout << "Seed:        " << seed << " | Run: " << runId << std::endl;
    std::cout << "Duration:    " << simDuration << "s | Measure: " << measureStart << "s–" << measureEnd << "s" << std::endl;
    std::cout << "Output dir:  " << outputDir << std::endl;
    std::cout << std::endl;

    // ── Nodes ──
    // sender(0) --- router0(1) --- router1(2) --- receiver(3)
    NodeContainer senderNode, router0Node, router1Node, receiverNode;
    senderNode.Create(1);
    router0Node.Create(1);
    router1Node.Create(1);
    receiverNode.Create(1);

    // For S4 cross traffic, add a cross sender
    NodeContainer crossSenderNode;
    if (scenarioId == "S4" || enableCrossTraffic)
    {
        crossSenderNode.Create(1);
    }

    // ── Point-to-Point links ──
    PointToPointHelper accessLink, bottleneckLink;

    // Access link: sender → router0 (high BW, low delay)
    accessLink.SetDeviceAttribute("DataRate", StringValue(cfg.accessBw));
    accessLink.SetChannelAttribute("Delay", StringValue(cfg.accessDelay));
    accessLink.SetQueue("ns3::DropTailQueue",
                        "MaxSize",
                        StringValue("100p"));

    // Bottleneck link: router0 → router1 (constrained BW)
    bottleneckLink.SetDeviceAttribute("DataRate", StringValue(cfg.bottleneckBw));
    bottleneckLink.SetChannelAttribute("Delay", StringValue(cfg.bottleneckDelay));
    bottleneckLink.SetQueue("ns3::DropTailQueue",
                            "MaxSize",
                            StringValue(std::to_string(cfg.queueSize) + "p"));

    // Install devices
    NetDeviceContainer devSenderRouter = accessLink.Install(senderNode.Get(0), router0Node.Get(0));
    NetDeviceContainer devBottleneck = bottleneckLink.Install(router0Node.Get(0), router1Node.Get(0));
    NetDeviceContainer devRouterReceiver = accessLink.Install(router1Node.Get(0), receiverNode.Get(0));

    // Cross traffic link (S4)
    NetDeviceContainer devCrossSenderRouter;
    if (!crossSenderNode.IsEmpty())
    {
        devCrossSenderRouter = accessLink.Install(crossSenderNode.Get(0), router0Node.Get(0));
    }

    // ── Internet stack ──
    InternetStackHelper internet;
    internet.Install(senderNode);
    internet.Install(router0Node);
    internet.Install(router1Node);
    internet.Install(receiverNode);
    if (!crossSenderNode.IsEmpty())
    {
        internet.Install(crossSenderNode);
    }

    // ── IP addresses ──
    Ipv4AddressHelper ipv4;

    ipv4.SetBase("10.1.1.0", "255.255.255.0");
    Ipv4InterfaceContainer ifSenderRouter = ipv4.Assign(devSenderRouter);

    ipv4.SetBase("10.1.2.0", "255.255.255.0");
    Ipv4InterfaceContainer ifBottleneck = ipv4.Assign(devBottleneck);

    ipv4.SetBase("10.1.3.0", "255.255.255.0");
    Ipv4InterfaceContainer ifRouterReceiver = ipv4.Assign(devRouterReceiver);

    if (!crossSenderNode.IsEmpty())
    {
        ipv4.SetBase("10.1.4.0", "255.255.255.0");
        ipv4.Assign(devCrossSenderRouter);
    }

    Ipv4GlobalRoutingHelper::PopulateRoutingTables();

    // ── TCP Socket config ──
    Config::SetDefault("ns3::TcpSocket::SegmentSize", UintegerValue(1448));
    Config::SetDefault("ns3::TcpSocket::SndBufSize", UintegerValue(1 << 20));
    Config::SetDefault("ns3::TcpSocket::RcvBufSize", UintegerValue(1 << 20));

    // ── Applications: bulk sender → packet sink ──
    uint16_t port = 5001;
    Address receiverAddr(InetSocketAddress(ifRouterReceiver.GetAddress(1), port));

    // Receiver (Packet Sink)
    PacketSinkHelper sinkHelper("ns3::TcpSocketFactory",
                                InetSocketAddress(Ipv4Address::GetAny(), port));
    ApplicationContainer sinkApps = sinkHelper.Install(receiverNode.Get(0));
    sinkApps.Start(Seconds(0.0));
    sinkApps.Stop(Seconds(simDuration));

    // Sender (Bulk Send)
    BulkSendHelper sourceHelper("ns3::TcpSocketFactory", receiverAddr);
    sourceHelper.SetAttribute("MaxBytes", UintegerValue(0)); // Unlimited
    ApplicationContainer sourceApps = sourceHelper.Install(senderNode.Get(0));
    sourceApps.Start(Seconds(0.5));
    sourceApps.Stop(Seconds(simDuration - 0.5));

    // Cross traffic application (S4)
    if (!crossSenderNode.IsEmpty())
    {
        uint16_t crossPort = 5002;
        Address crossReceiverAddr(InetSocketAddress(ifRouterReceiver.GetAddress(1), crossPort));
        PacketSinkHelper crossSinkHelper("ns3::TcpSocketFactory",
                                         InetSocketAddress(Ipv4Address::GetAny(), crossPort));
        ApplicationContainer crossSinkApps = crossSinkHelper.Install(receiverNode.Get(0));
        crossSinkApps.Start(Seconds(0.0));
        crossSinkApps.Stop(Seconds(simDuration));

        BulkSendHelper crossSourceHelper("ns3::TcpSocketFactory", crossReceiverAddr);
        crossSourceHelper.SetAttribute("MaxBytes", UintegerValue(0));
        ApplicationContainer crossSourceApps = crossSourceHelper.Install(crossSenderNode.Get(0));
        crossSourceApps.Start(Seconds(5.0)); // Cross traffic starts at 5s
        crossSourceApps.Stop(Seconds(simDuration - 0.5));
    }

    // ── Flow Monitor ──
    FlowMonitorHelper flowMonHelper;
    Ptr<FlowMonitor> flowMonitor = flowMonHelper.InstallAll();

    // ── Run simulation ──
    Simulator::Stop(Seconds(simDuration));
    Simulator::Run();

    // ── Collect FlowMonitor statistics ──
    flowMonitor->CheckForLostPackets();
    Ptr<Ipv4FlowClassifier> classifier =
        DynamicCast<Ipv4FlowClassifier>(flowMonHelper.GetClassifier());
    FlowMonitor::FlowStatsContainer stats = flowMonitor->GetFlowStats();

    // ── Aggregate main flow metrics ──
    uint64_t totalRxBytes = 0;
    uint64_t totalTxPackets = 0;
    uint64_t totalRxPackets = 0;
    uint64_t totalLostPackets = 0;
    double totalDelaySum = 0.0;
    double totalJitterSum = 0.0;
    uint32_t flowCount = 0;

    for (auto& kv : stats)
    {
        Ipv4FlowClassifier::FiveTuple t = classifier->FindFlow(kv.first);
        // Only count flows on port 5001 (main TCP flow)
        if (t.destinationPort != port)
            continue;

        const FlowMonitor::FlowStats& fs = kv.second;
        totalRxBytes += fs.rxBytes;
        totalTxPackets += fs.txPackets;
        totalRxPackets += fs.rxPackets;
        totalLostPackets += fs.lostPackets;
        totalDelaySum += fs.delaySum.GetSeconds();
        totalJitterSum += fs.jitterSum.GetSeconds();
        flowCount++;
    }

    // ── Compute metrics ──
    double measureDuration = measureEnd - measureStart;
    if (measureDuration <= 0)
        measureDuration = simDuration;

    // Throughput: rxBytes in simulation / duration (approximate)
    double throughputMbps =
        (totalRxBytes * 8.0) / (simDuration * 1e6);

    // Average delay (one-way, ms)
    double avgDelayMs = (totalRxPackets > 0)
                            ? (totalDelaySum / totalRxPackets) * 1000.0
                            : 0.0;

    // Loss rate
    double lossRate = (totalTxPackets > 0)
                          ? (double)totalLostPackets / totalTxPackets
                          : 0.0;

    // Provisional utility (normalized, provisional weights per Change 02)
    double bottleneckBwMbps = 10.0; // S1/S2/S3/S4 all use 10Mbps bottleneck
    double maxExpectedDelayMs =
        (scenarioId == "S2" || scenarioId == "scenario_b") ? 300.0 : 100.0;

    double throughputNorm = std::min(throughputMbps / bottleneckBwMbps, 1.0);
    double delayNorm = std::min(avgDelayMs / maxExpectedDelayMs, 1.0);
    double utilityScore = throughputNorm - 0.1 * delayNorm - 10.0 * lossRate;

    // ── Print summary ──
    std::cout << "=== Results ===" << std::endl;
    std::cout << std::fixed << std::setprecision(4);
    std::cout << "  RxBytes:          " << totalRxBytes << " bytes" << std::endl;
    std::cout << "  TxPackets:        " << totalTxPackets << std::endl;
    std::cout << "  RxPackets:        " << totalRxPackets << std::endl;
    std::cout << "  LostPackets:      " << totalLostPackets << std::endl;
    std::cout << "  Throughput:       " << throughputMbps << " Mbps" << std::endl;
    std::cout << "  Avg Delay:        " << avgDelayMs << " ms" << std::endl;
    std::cout << "  Loss Rate:        " << lossRate << std::endl;
    std::cout << "  Utility Score:    " << utilityScore << " (provisional)" << std::endl;
    std::cout << std::endl;

    // ── Write output files ──
    // Create output dir
    std::string mkdirCmd = "mkdir -p " + outputDir;
    if (system(mkdirCmd.c_str()) != 0)
    {
        NS_LOG_WARN("Could not create output directory: " << outputDir);
    }

    // Per-run raw log CSV
    std::string rawLogPath = outputDir + "/" + cfg.scenarioId + "_" + tcpName +
                             "_seed" + std::to_string(seed) + "_" + runId + "_raw.csv";
    {
        std::ofstream rawLog(rawLogPath);
        rawLog << "scenario_id,method,run_id,seed,rx_bytes,tx_packets,rx_packets,"
               << "lost_packets,throughput_mbps,avg_delay_ms,loss_rate,"
               << "utility_score,sim_duration,flow_count,"
               << "ns3_version,tcp_variant_found,notes\n";
        rawLog << cfg.scenarioId << "," << tcpName << "," << runId << ","
               << seed << "," << totalRxBytes << "," << totalTxPackets << ","
               << totalRxPackets << "," << totalLostPackets << ","
               << std::fixed << std::setprecision(6)
               << throughputMbps << "," << avgDelayMs << "," << lossRate << ","
               << utilityScore << "," << simDuration << "," << flowCount << ","
               << "3.40" << "," << (tcpFound ? "YES" : "NO_FALLBACK")
               << ",delay_estimate_method:delaySum_per_packet\n";
        rawLog.close();
    }
    std::cout << "  Raw log:   " << rawLogPath << std::endl;

    // Append to summary CSV
    std::string summaryPath = outputDir + "/../summaries/baseline_summary.csv";
    {
        // Write header if file doesn't exist
        std::ifstream checkFile(summaryPath);
        bool needHeader = !checkFile.good();
        checkFile.close();

        std::ofstream summaryLog(summaryPath, std::ios::app);
        if (needHeader)
        {
            summaryLog << "scenario_id,method,run_id,seed,throughput_mbps,"
                       << "avg_delay_ms,loss_rate,utility_score,sim_duration,"
                       << "tcp_variant_found,notes\n";
        }
        summaryLog << cfg.scenarioId << "," << tcpName << "," << runId << ","
                   << seed << ","
                   << std::fixed << std::setprecision(6)
                   << throughputMbps << "," << avgDelayMs << "," << lossRate << ","
                   << utilityScore << "," << simDuration << ","
                   << (tcpFound ? "YES" : "NO_FALLBACK")
                   << ",delay_estimate_method:delaySum_per_packet\n";
        summaryLog.close();
    }
    std::cout << "  Summary CSV: " << summaryPath << std::endl;

    // FlowMonitor XML
    std::string xmlPath = outputDir + "/" + cfg.scenarioId + "_" + tcpName +
                          "_seed" + std::to_string(seed) + "_" + runId + "_flowmonitor.xml";
    flowMonitor->SerializeToXmlFile(xmlPath, true, true);
    std::cout << "  FlowMonitor: " << xmlPath << std::endl;

    Simulator::Destroy();
    std::cout << std::endl << "Simulation complete." << std::endl;
    return 0;
}
