import pandas as pd
import matplotlib.pyplot as plt
import os
import shutil

# Ensure directories
os.makedirs('figures/final', exist_ok=True)

# 1. Text-based diagrams
def create_text_diagram(filename, title, text):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('off')
    ax.text(0.5, 0.9, title, fontsize=16, ha='center', fontweight='bold')
    ax.text(0.5, 0.4, text, fontsize=12, ha='center', va='center', bbox=dict(facecolor='lightgray', alpha=0.5, boxstyle='round,pad=1'))
    plt.tight_layout()
    plt.savefig(f'figures/final/{filename}')
    plt.close()

create_text_diagram('system_pipeline.png', 'System Architecture Pipeline', 'ns-3.40 (Environment)\n<-->\nns3-gym (ZMQ Interface)\n<-->\nStable-Baselines3 (DQN Agent)')
create_text_diagram('single_bottleneck_topology.png', 'Single Bottleneck Topology', 'Sender (Node 0)\n|\n|\nv\nBottleneck Router (Node 1) -> Receiver (Node 2)\n[Data Rate: 10Mbps, Delay: 10ms/50ms]')
create_text_diagram('mdp_formulation.png', 'MDP Formulation', 'State (5 dims): Throughput, Delay Proxy, Loss Rate, Cwnd, Rtx\nAction (3 discrete): Decrease (-), Keep (=), Increase (+)\nReward: (alpha * throughput) - (beta * delay) - (lambda * loss)')
create_text_diagram('key_findings_summary.png', 'Key Findings Summary', '1. S1 (Low Delay): DQN learned near-capacity policy (100% Increase).\n2. S2 (High Delay): DQN struggles with high loss (5.54%).\n3. Limitation: Action is a sender-side rate abstraction, not kernel-level cwnd.\n4. Limitation: Delay is a proxy, not true TCP RTT.')

# 2. Baseline Utility
try:
    df_baseline = pd.read_csv('experiments/summaries/baseline_summary.csv')
    fig, ax = plt.subplots(figsize=(8, 5))
    df_baseline.set_index('scenario_id')[['utility_score']].plot(kind='bar', ax=ax)
    plt.title('Baseline Utility Score Comparison (S1 & S2)')
    plt.ylabel('Utility Score (Provisional)')
    plt.tight_layout()
    plt.savefig('figures/final/baseline_utility_summary.png')
    plt.close()
except Exception as e:
    print(f"Skipping baseline utility: {e}")

# 3. DQN vs Baseline Utility
try:
    df_comp = pd.read_csv('experiments/drl/summaries/dqn_vs_baseline_summary.csv')
    # Filter and plot
    fig, ax = plt.subplots(figsize=(10, 6))
    for scenario in ['s1', 's2']:
        df_s = df_comp[df_comp['scenario_id'] == scenario]
        if not df_s.empty:
            plt.bar([f"{algo} ({scenario})" for algo in df_s['method']], df_s['utility_score'])
    plt.title('DQN vs Baseline Utility Score (S1 & S2)')
    plt.ylabel('Utility Score (Provisional)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('figures/final/dqn_vs_baseline_utility_s1_s2.png')
    plt.close()

    # Loss Rate
    fig, ax = plt.subplots(figsize=(10, 6))
    for scenario in ['s1', 's2']:
        df_s = df_comp[df_comp['scenario_id'] == scenario]
        if not df_s.empty:
            plt.bar([f"{algo} ({scenario})" for algo in df_s['method']], df_s['loss_rate'])
    plt.title('DQN vs Baseline Loss Rate (S1 & S2)')
    plt.ylabel('Loss Rate')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('figures/final/dqn_vs_baseline_loss_s1_s2.png')
    plt.close()
except Exception as e:
    print(f"Skipping DQN vs Baseline: {e}")

# 4. DQN Action Distribution
try:
    df_action = pd.read_csv('experiments/drl/summaries/dqn_action_distribution_summary.csv')
    fig, ax = plt.subplots(figsize=(8, 5))
    df_action.set_index('scenario_id')[['action_0_decrease_pct', 'action_1_keep_pct', 'action_2_increase_pct']].plot(kind='bar', ax=ax)
    plt.title('DQN Action Distribution (S1 & S2)')
    plt.ylabel('Percentage (%)')
    plt.tight_layout()
    plt.savefig('figures/final/dqn_action_distribution_s1_s2.png')
    plt.close()
except Exception as e:
    print(f"Skipping Action Distribution: {e}")

# 5. DQN Reward Curves
# Combine existing images since we don't have the full trace logs path immediately
try:
    from PIL import Image
    im1 = Image.open('figures/drl/dqn_reward_curve_s1.png')
    im2 = Image.open('figures/drl/dqn_reward_curve_s2.png')
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    dst.save('figures/final/dqn_reward_curves_s1_s2.png')
except Exception as e:
    print(f"Skipping reward curves merge: {e}")

print("Final figures generated successfully.")
