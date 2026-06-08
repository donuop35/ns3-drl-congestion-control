/* ===========================================================================
 * Phase 4: OpenGym Congestion Control Environment
 * Project: DRL for Congestion Control and Throughput Optimization
 * OpenSpec Change 03: opengym-env | Change 04: dqn-mvp-agent
 *
 * This ns-3 simulation implements a single bottleneck RL environment
 * via ns3-gym (OpenGym). It follows the MDP defined in Change 03:
 *
 * Observation (shape=5):
 *   [throughput_norm, delay_norm, loss_norm, cwnd_norm, prev_action_norm]
 *
 * Action: Discrete(3) = {0: decrease, 1: keep, 2: increase}
 *
 * Reward: r = alpha*throughput_norm - beta*delay_norm - lambda*loss_norm
 *   Default: alpha=1.0, beta=0.1, lambda=10.0 (provisional)
 *
 * Topology: Sender -> AccessLink -> Router0 -> BottleneckLink -> Router1 -> Receiver
 *
 * PHASE 4 SCOPE: RL environment only. No Phase 3 baseline artifacts modified.
 * ===========================================================================
 */

#include "ns3/applications-module.h"
#include "ns3/core-module.h"
#include "ns3/flow-monitor-module.h"
#include "ns3/internet-module.h"
#include "ns3/network-module.h"
#include "ns3/opengym-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/traffic-control-module.h"
#include "ns3/ipv4-flow-classifier.h"

#include <fstream>
#include <iomanip>
#include <sstream>
#include <string>
#include <vector>

using namespace ns3;

NS_LOG_COMPONENT_DEFINE("OpenGymCongestionEnv");

// ===========================================================================
// Scenario config (inherits Phase 3 topology)
// ===========================================================================
struct ScenarioConfig {
    std::string id;
    std::string bottleneckBw;
    std::string bottleneckDelay;
    std::string accessBw;
    std::string accessDelay;
    uint32_t    queueSizePkts;
    double      simDuration;
    double      stepInterval;   // RL decision interval (seconds)
    std::string description;
};

ScenarioConfig GetScenario(const std::string& sid, double dur)
{
    ScenarioConfig c;
    c.id          = sid;
    c.simDuration = dur;
    c.stepInterval = 0.5;  // 500ms RL step (one decision per 500ms)

    if (sid == "S1") {
        c.bottleneckBw    = "10Mbps";
        c.bottleneckDelay = "10ms";
        c.accessBw        = "100Mbps";
        c.accessDelay     = "1ms";
        c.queueSizePkts   = 100;
        c.description     = "Low-delay bottleneck (10 Mbps, 10 ms)";
    } else if (sid == "S2") {
        c.bottleneckBw    = "10Mbps";
        c.bottleneckDelay = "50ms";
        c.accessBw        = "100Mbps";
        c.accessDelay     = "1ms";
        c.queueSizePkts   = 100;
        c.description     = "High-delay bottleneck (10 Mbps, 50 ms)";
    } else {
        // Default to S1
        NS_LOG_WARN("Unknown scenario '" << sid << "', defaulting to S1");
        return GetScenario("S1", dur);
    }
    return c;
}

// ===========================================================================
// Global state for RL step metrics
// ===========================================================================
static double g_stepThroughput   = 0.0;  // Mbps in last step
static double g_stepDelay        = 0.0;  // ms in last step
static double g_stepLoss         = 0.0;  // fraction in last step
static double g_stepCwnd         = 0.0;  // estimated cwnd (bytes, normalized)
static uint32_t g_prevAction     = 1;    // last applied action (0=dec,1=keep,2=inc)
static double g_sendRate         = 5.0;  // current application send rate (Mbps)
static double g_bottleneckBwMbps = 10.0; // normalizer
static double g_maxDelayMs       = 100.0;
static uint32_t g_stepIndex      = 0;
static bool   g_done             = false;

// FlowMonitor
static Ptr<FlowMonitor>        g_flowMonitor;
static FlowMonitorHelper       g_flowMonHelper;
static Ptr<Ipv4FlowClassifier> g_classifier;

// Application
static Ptr<OnOffApplication>   g_senderApp;
static double                   g_lastRxBytes  = 0.0;
static double                   g_lastTxPkts   = 0.0;
static double                   g_lastRxPkts   = 0.0;
static double                   g_lastLostPkts = 0.0;
static double                   g_lastDelaySum = 0.0;
static double                   g_stepStart    = 0.0;

// Reward weights (provisional per Change 03/04)
static double ALPHA = 1.0;
static double BETA  = 0.1;
static double LAMBDA_W = 10.0;

// Episode config
static uint32_t MAX_STEPS = 100;  // max steps per episode
static std::string g_outputDir = "/tmp/ns3-opengym-output";
static std::string g_scenarioId = "S1";
static uint32_t g_port = 5001;

// ===========================================================================
// OpenGym Environment class
// ===========================================================================
class DrlCongestionEnv : public OpenGymEnv
{
public:
    DrlCongestionEnv();
    ~DrlCongestionEnv() override = default;

    static TypeId GetTypeId();

    // OpenGym interface
    Ptr<OpenGymSpace>  GetObservationSpace() override;
    Ptr<OpenGymSpace>  GetActionSpace() override;
    Ptr<OpenGymDataContainer> GetObservation() override;
    float              GetReward() override;
    bool               GetGameOver() override;
    std::string        GetExtraInfo() override;
    bool               ExecuteActions(Ptr<OpenGymDataContainer> action) override;

private:
    void CollectStepMetrics();
    void ApplySendRateAction(uint32_t action);
};

NS_OBJECT_ENSURE_REGISTERED(DrlCongestionEnv);

DrlCongestionEnv::DrlCongestionEnv() {}

TypeId DrlCongestionEnv::GetTypeId()
{
    static TypeId tid = TypeId("ns3::DrlCongestionEnv")
        .SetParent<OpenGymEnv>()
        .AddConstructor<DrlCongestionEnv>();
    return tid;
}

Ptr<OpenGymSpace> DrlCongestionEnv::GetObservationSpace()
{
    // Shape = 5: [throughput_norm, delay_norm, loss_norm, cwnd_norm, prev_action_norm]
    uint32_t parameterNum = 5;
    float low  = 0.0;
    float high = 1.0;
    std::vector<uint32_t> shape = {parameterNum};
    std::string dtype = TypeNameGet<float>();
    Ptr<OpenGymBoxSpace> space = CreateObject<OpenGymBoxSpace>(low, high, shape, dtype);
    NS_LOG_INFO("ObservationSpace: shape=" << parameterNum << " [throughput_norm, delay_norm, loss_norm, cwnd_norm, prev_action_norm]");
    return space;
}

Ptr<OpenGymSpace> DrlCongestionEnv::GetActionSpace()
{
    // Discrete(3): {0: decrease, 1: keep, 2: increase}
    Ptr<OpenGymDiscreteSpace> space = CreateObject<OpenGymDiscreteSpace>(3);
    NS_LOG_INFO("ActionSpace: Discrete(3) {0=decrease, 1=keep, 2=increase}");
    return space;
}

void DrlCongestionEnv::CollectStepMetrics()
{
    g_flowMonitor->CheckForLostPackets();
    FlowMonitor::FlowStatsContainer stats = g_flowMonitor->GetFlowStats();

    double stepDuration = Simulator::Now().GetSeconds() - g_stepStart;
    if (stepDuration <= 0) stepDuration = 1.0;

    double rxBytes   = 0.0;
    double txPkts    = 0.0;
    double rxPkts    = 0.0;
    double lostPkts  = 0.0;
    double delaySum  = 0.0;
    uint32_t flowCount = 0;

    for (auto& kv : stats) {
        Ipv4FlowClassifier::FiveTuple t = g_classifier->FindFlow(kv.first);
        if (t.destinationPort != g_port) continue;
        const FlowMonitor::FlowStats& fs = kv.second;
        rxBytes  += fs.rxBytes  - g_lastRxBytes;
        txPkts   += fs.txPackets - g_lastTxPkts;
        rxPkts   += fs.rxPackets - g_lastRxPkts;
        lostPkts += fs.lostPackets - g_lastLostPkts;
        delaySum += fs.delaySum.GetSeconds() - g_lastDelaySum;
        flowCount++;

        // Update running totals for next delta
        g_lastRxBytes   = fs.rxBytes;
        g_lastTxPkts    = fs.txPackets;
        g_lastRxPkts    = fs.rxPackets;
        g_lastLostPkts  = fs.lostPackets;
        g_lastDelaySum  = fs.delaySum.GetSeconds();
    }

    // Compute step metrics
    g_stepThroughput = (rxBytes * 8.0) / (stepDuration * 1e6);  // Mbps
    g_stepDelay      = (rxPkts > 0) ? (delaySum / rxPkts) * 1000.0 : 0.0;  // ms
    g_stepLoss       = (txPkts > 0) ? (lostPkts / txPkts) : 0.0;

    // Pseudo-cwnd: proportional to current send rate
    // (true cwnd not directly accessible in application-level control)
    g_stepCwnd = g_sendRate / g_bottleneckBwMbps;  // normalized [0,1]

    g_stepStart = Simulator::Now().GetSeconds();
}

Ptr<OpenGymDataContainer> DrlCongestionEnv::GetObservation()
{
    CollectStepMetrics();

    std::vector<uint32_t> shape = {5};
    Ptr<OpenGymBoxContainer<float>> box = CreateObject<OpenGymBoxContainer<float>>(shape);

    // Normalize: clip to [0, 1]
    float t_norm = (float)std::min(g_stepThroughput / g_bottleneckBwMbps, 1.0);
    float d_norm = (float)std::min(g_stepDelay / g_maxDelayMs, 1.0);
    float l_norm = (float)std::min(g_stepLoss, 1.0);
    float c_norm = (float)std::min(g_stepCwnd, 1.0);
    float a_norm = (float)(g_prevAction) / 2.0f;  // [0,1]

    box->AddValue(t_norm);
    box->AddValue(d_norm);
    box->AddValue(l_norm);
    box->AddValue(c_norm);
    box->AddValue(a_norm);

    NS_LOG_INFO("Obs: t_norm=" << t_norm << " d_norm=" << d_norm
                << " l_norm=" << l_norm << " c_norm=" << c_norm
                << " a_norm=" << a_norm);
    return box;
}

float DrlCongestionEnv::GetReward()
{
    // r = alpha*t_norm - beta*d_norm - lambda*l_norm
    float t_norm = (float)std::min(g_stepThroughput / g_bottleneckBwMbps, 1.0);
    float d_norm = (float)std::min(g_stepDelay / g_maxDelayMs, 1.0);
    float l_norm = (float)std::min(g_stepLoss, 1.0);

    float reward = (float)(ALPHA * t_norm - BETA * d_norm - LAMBDA_W * l_norm);
    // Clip to [-1, 1] for numerical stability
    reward = std::max(-1.0f, std::min(1.0f, reward));

    NS_LOG_INFO("Reward: " << reward
                << " (t=" << t_norm << " d=" << d_norm << " l=" << l_norm << ")");
    return reward;
}

bool DrlCongestionEnv::GetGameOver()
{
    g_stepIndex++;
    g_done = (g_stepIndex >= MAX_STEPS);
    return g_done;
}

std::string DrlCongestionEnv::GetExtraInfo()
{
    // info dict: baseline-compatible metrics + RL metadata
    std::ostringstream ss;
    ss << std::fixed << std::setprecision(6);
    ss << "{"
       << "\"scenario_id\":\"" << g_scenarioId << "\","
       << "\"step_index\":" << g_stepIndex << ","
       << "\"raw_throughput_mbps\":" << g_stepThroughput << ","
       << "\"raw_delay_ms\":" << g_stepDelay << ","
       << "\"raw_loss_rate\":" << g_stepLoss << ","
       << "\"send_rate_mbps\":" << g_sendRate << ","
       << "\"action_applied\":" << g_prevAction << ","
       << "\"delay_estimate_method\":\"delaySum_per_packet\","
       << "\"reward_alpha\":" << ALPHA << ","
       << "\"reward_beta\":" << BETA << ","
       << "\"reward_lambda\":" << LAMBDA_W
       << "}";
    return ss.str();
}

void DrlCongestionEnv::ApplySendRateAction(uint32_t action)
{
    // Rate control abstraction: agent controls application send rate
    // This is Fallback Option B (sender-side rate-control abstraction)
    // as specified in Change 04 action mapping fallback hierarchy.
    const double STEP_MBPS = 1.0;  // ±1 Mbps per action
    const double MIN_RATE  = 1.0;
    const double MAX_RATE  = g_bottleneckBwMbps * 1.2;  // allow slight overshoot

    double newRate = g_sendRate;
    if (action == 0) {
        newRate -= STEP_MBPS;
    } else if (action == 2) {
        newRate += STEP_MBPS;
    }
    // action == 1: keep current rate

    newRate = std::max(MIN_RATE, std::min(MAX_RATE, newRate));

    if (g_senderApp) {
        g_senderApp->SetAttribute("DataRate",
            DataRateValue(DataRate((uint64_t)(newRate * 1e6))));
        g_sendRate = newRate;
    }

    g_prevAction = action;
    NS_LOG_INFO("Action=" << action << " -> sendRate=" << g_sendRate << " Mbps");
}

bool DrlCongestionEnv::ExecuteActions(Ptr<OpenGymDataContainer> action)
{
    Ptr<OpenGymDiscreteContainer> discrete =
        DynamicCast<OpenGymDiscreteContainer>(action);
    if (discrete) {
        uint32_t act = discrete->GetValue();
        ApplySendRateAction(act);
        return true;
    }
    NS_LOG_WARN("ExecuteActions: could not cast action container");
    return false;
}

// ===========================================================================
// Main
// ===========================================================================
int main(int argc, char* argv[])
{
    // ── Parameters ──────────────────────────────────────────────────────────
    uint32_t openGymPort  = 5555;
    std::string scenario  = "S1";
    double simDuration    = 60.0;
    uint32_t seed         = 42;
    uint32_t maxSteps     = 100;
    double stepInterval   = 0.5;  // seconds
    double alpha          = 1.0;
    double beta           = 0.1;
    double lambdaW        = 10.0;
    std::string outputDir = "/tmp/ns3-opengym-output";
    bool verbose          = false;

    CommandLine cmd(__FILE__);
    cmd.AddValue("openGymPort",  "OpenGym ZMQ port",          openGymPort);
    cmd.AddValue("scenario",     "Scenario ID: S1 or S2",     scenario);
    cmd.AddValue("simDuration",  "Total simulation duration",  simDuration);
    cmd.AddValue("seed",         "Random seed",                seed);
    cmd.AddValue("maxSteps",     "Max RL steps per episode",   maxSteps);
    cmd.AddValue("stepInterval", "RL decision interval (s)",   stepInterval);
    cmd.AddValue("alpha",        "Reward throughput weight",   alpha);
    cmd.AddValue("beta",         "Reward delay weight",        beta);
    cmd.AddValue("lambdaW",      "Reward loss weight",         lambdaW);
    cmd.AddValue("outputDir",    "Output directory",           outputDir);
    cmd.AddValue("verbose",      "Verbose logging",            verbose);
    cmd.Parse(argc, argv);

    // ── Global state setup ───────────────────────────────────────────────────
    RngSeedManager::SetSeed(seed);
    RngSeedManager::SetRun(1);
    ALPHA     = alpha;
    BETA      = beta;
    LAMBDA_W  = lambdaW;
    MAX_STEPS = maxSteps;
    g_outputDir  = outputDir;
    g_scenarioId = scenario;

    if (verbose) {
        LogComponentEnable("OpenGymCongestionEnv", LOG_LEVEL_INFO);
    }

    ScenarioConfig cfg = GetScenario(scenario, simDuration);
    g_bottleneckBwMbps = 10.0;
    g_maxDelayMs = (scenario == "S2") ? 300.0 : 100.0;
    g_sendRate   = 5.0;  // Start at 50% of bottleneck

    std::cout << "=== Phase 4 OpenGym Congestion Env ===" << std::endl;
    std::cout << "Scenario: " << cfg.id << " | " << cfg.description << std::endl;
    std::cout << "OpenGym port: " << openGymPort << std::endl;
    std::cout << "Max steps: " << maxSteps << " | Step interval: " << stepInterval << "s" << std::endl;
    std::cout << "Reward: alpha=" << alpha << " beta=" << beta << " lambda=" << lambdaW << std::endl;
    std::cout << std::endl;

    // ── OpenGym interface ────────────────────────────────────────────────────
    Ptr<OpenGymInterface> openGym = CreateObject<OpenGymInterface>(openGymPort);

    // ── Nodes ────────────────────────────────────────────────────────────────
    NodeContainer sender, router0, router1, receiver;
    sender.Create(1);
    router0.Create(1);
    router1.Create(1);
    receiver.Create(1);

    // ── Links ────────────────────────────────────────────────────────────────
    PointToPointHelper accessLink, bottleneckLink;
    accessLink.SetDeviceAttribute("DataRate", StringValue(cfg.accessBw));
    accessLink.SetChannelAttribute("Delay", StringValue(cfg.accessDelay));
    accessLink.SetQueue("ns3::DropTailQueue", "MaxSize", StringValue("100p"));

    bottleneckLink.SetDeviceAttribute("DataRate", StringValue(cfg.bottleneckBw));
    bottleneckLink.SetChannelAttribute("Delay", StringValue(cfg.bottleneckDelay));
    bottleneckLink.SetQueue("ns3::DropTailQueue", "MaxSize",
        StringValue(std::to_string(cfg.queueSizePkts) + "p"));

    NetDeviceContainer devSR  = accessLink.Install(sender.Get(0),  router0.Get(0));
    NetDeviceContainer devBN  = bottleneckLink.Install(router0.Get(0), router1.Get(0));
    NetDeviceContainer devRR  = accessLink.Install(router1.Get(0), receiver.Get(0));

    // ── Internet stack ───────────────────────────────────────────────────────
    InternetStackHelper inet;
    inet.Install(sender);
    inet.Install(router0);
    inet.Install(router1);
    inet.Install(receiver);

    Ipv4AddressHelper ipv4;
    ipv4.SetBase("10.1.1.0", "255.255.255.0");
    Ipv4InterfaceContainer ifSR = ipv4.Assign(devSR);
    ipv4.SetBase("10.1.2.0", "255.255.255.0");
    ipv4.Assign(devBN);
    ipv4.SetBase("10.1.3.0", "255.255.255.0");
    Ipv4InterfaceContainer ifRR = ipv4.Assign(devRR);
    Ipv4GlobalRoutingHelper::PopulateRoutingTables();

    // ── TCP config ───────────────────────────────────────────────────────────
    Config::SetDefault("ns3::TcpL4Protocol::SocketType",
                       TypeIdValue(TypeId::LookupByName("ns3::TcpLinuxReno")));
    Config::SetDefault("ns3::TcpSocket::SegmentSize", UintegerValue(1448));
    Config::SetDefault("ns3::TcpSocket::SndBufSize", UintegerValue(1 << 20));
    Config::SetDefault("ns3::TcpSocket::RcvBufSize", UintegerValue(1 << 20));

    // ── Applications (OnOff sender, rate-controlled) ─────────────────────────
    Address sinkAddr(InetSocketAddress(ifRR.GetAddress(1), g_port));
    PacketSinkHelper sink("ns3::TcpSocketFactory",
                          InetSocketAddress(Ipv4Address::GetAny(), g_port));
    ApplicationContainer sinkApps = sink.Install(receiver.Get(0));
    sinkApps.Start(Seconds(0.0));
    sinkApps.Stop(Seconds(simDuration));

    OnOffHelper source("ns3::TcpSocketFactory", sinkAddr);
    source.SetAttribute("DataRate",  DataRateValue(DataRate((uint64_t)(g_sendRate * 1e6))));
    source.SetAttribute("PacketSize", UintegerValue(1448));
    source.SetAttribute("OnTime",    StringValue("ns3::ConstantRandomVariable[Constant=1]"));
    source.SetAttribute("OffTime",   StringValue("ns3::ConstantRandomVariable[Constant=0]"));

    ApplicationContainer sourceApps = source.Install(sender.Get(0));
    g_senderApp = sourceApps.Get(0)->GetObject<OnOffApplication>();
    sourceApps.Start(Seconds(0.5));
    sourceApps.Stop(Seconds(simDuration - 0.5));

    // ── FlowMonitor ──────────────────────────────────────────────────────────
    g_flowMonitor = g_flowMonHelper.InstallAll();
    g_classifier = DynamicCast<Ipv4FlowClassifier>(g_flowMonHelper.GetClassifier());

    // ── OpenGym environment ──────────────────────────────────────────────────
    Ptr<DrlCongestionEnv> env = CreateObject<DrlCongestionEnv>();
    env->SetOpenGymInterface(openGym);

    // Schedule first RL notification
    g_stepStart = 0.5;
    for (double t = 0.5 + stepInterval; t < simDuration - 0.5; t += stepInterval) {
        Simulator::Schedule(Seconds(t), &OpenGymInterface::NotifyCurrentState, openGym);
    }

    // ── Run ──────────────────────────────────────────────────────────────────
    Simulator::Stop(Seconds(simDuration));
    Simulator::Run();

    openGym->NotifySimulationEnd();
    Simulator::Destroy();

    std::cout << "Simulation complete." << std::endl;
    return 0;
}
