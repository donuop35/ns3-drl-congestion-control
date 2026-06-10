import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

os.makedirs('figures/final', exist_ok=True)
manifest_entries = []

def check_csv(path):
    if not os.path.exists(path):
        print(f"ERROR: Missing required source file: {path}")
        sys.exit(1)

def add_manifest(figure, source, gen_method, caveat, used_in):
    manifest_entries.append(f"| {figure} | `figures/final/{figure}` | `{source}` | {gen_method} | {caveat} | {used_in} |")

# 1. Text-based diagrams
def create_text_diagram(filename, title, text, source="Conceptual", used_in="Slides/Report"):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('off')
    ax.text(0.5, 0.9, title, fontsize=16, ha='center', fontweight='bold')
    ax.text(0.5, 0.4, text, fontsize=12, ha='center', va='center', bbox=dict(facecolor='lightgray', alpha=0.5, boxstyle='round,pad=1'))
    plt.tight_layout()
    plt.savefig(f'figures/final/{filename}')
    plt.close()
    add_manifest(filename, source, "Matplotlib text", "Conceptual diagram", used_in)
    print(f"Generated: {filename}")

create_text_diagram('system_pipeline.png', 'System Architecture Pipeline', 'ns-3.40 (Environment)\n<-->\nns3-gym (ZMQ Interface)\n<-->\nStable-Baselines3 (DQN Agent)')
create_text_diagram('single_bottleneck_topology.png', 'Single Bottleneck Topology', 'Sender (Node 0)\n|\n|\nv\nBottleneck Router (Node 1) -> Receiver (Node 2)\n[Data Rate: 10Mbps, Delay: 10ms/50ms]')
create_text_diagram('mdp_formulation.png', 'MDP Formulation', 'State (5 dims): Throughput, Delay Proxy, Loss Rate, Cwnd, Rtx\nAction (3 discrete): Decrease (-), Keep (=), Increase (+)\nReward: (1.0 * throughput) - (0.1 * delay) - (10.0 * loss)')
create_text_diagram('key_findings_summary.png', 'Key Findings Summary', '1. S1 (Low Delay): DQN near-capacity policy (100% Increase).\n2. S2 (High Delay): DQN high loss limitation (5.54%).\n3. Limitation: Action is Sender-side Rate Abstraction.\n4. Limitation: Delay is FlowMonitor Proxy.')

# 2. Baseline Utility
f_baseline = 'experiments/summaries/baseline_summary.csv'
check_csv(f_baseline)
df_baseline = pd.read_csv(f_baseline)
fig, ax = plt.subplots(figsize=(8, 5))
df_baseline.set_index('scenario_id')[['utility_score']].plot(kind='bar', ax=ax)
plt.title('Baseline Provisional Utility Score Comparison')
plt.ylabel('Provisional Utility')
plt.xlabel('Scenario (S1=10ms, S2=50ms)')
plt.tight_layout()
plt.savefig('figures/final/baseline_utility_summary.png')
plt.close()
add_manifest('baseline_utility_summary.png', f_baseline, "Matplotlib bar chart", "Provisional weights applied", "Report/Slides")
print("Generated: baseline_utility_summary.png")

# 3. DQN vs Baseline Comparison
f_comp = 'experiments/drl/summaries/dqn_vs_baseline_summary.csv'
check_csv(f_comp)
df_comp = pd.read_csv(f_comp)

# Plot Utility
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for idx, scenario in enumerate(['s1', 's2']):
    df_s = df_comp[df_comp['scenario_id'] == scenario]
    axes[idx].bar(df_s['method'], df_s['utility_score'], color=['blue', 'orange', 'green', 'red'])
    axes[idx].set_title(f'Scenario {scenario.upper()} Provisional Utility')
    axes[idx].set_ylabel('Provisional Utility')
    axes[idx].set_ylim(-0.2, 1.0)
    axes[idx].tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.savefig('figures/final/dqn_vs_baseline_utility_s1_s2.png')
plt.close()
add_manifest('dqn_vs_baseline_utility_s1_s2.png', f_comp, "Matplotlib grouped bar", "Provisional weights applied", "Report/Slides/Demo")
print("Generated: dqn_vs_baseline_utility_s1_s2.png")

# Plot Loss Rate
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for idx, scenario in enumerate(['s1', 's2']):
    df_s = df_comp[df_comp['scenario_id'] == scenario]
    axes[idx].bar(df_s['method'], df_s['loss_rate'], color=['blue', 'orange', 'green', 'red'])
    axes[idx].set_title(f'Scenario {scenario.upper()} Loss Rate')
    axes[idx].set_ylabel('Loss Rate (Fraction)')
    axes[idx].set_ylim(0, 0.06)
    axes[idx].tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.savefig('figures/final/dqn_vs_baseline_loss_s1_s2.png')
plt.close()
add_manifest('dqn_vs_baseline_loss_s1_s2.png', f_comp, "Matplotlib grouped bar", "Exposes DQN S2 high loss anomaly", "Report/Slides/Demo")
print("Generated: dqn_vs_baseline_loss_s1_s2.png")

# 4. DQN Action Distribution
f_action = 'experiments/drl/summaries/dqn_action_distribution_summary.csv'
check_csv(f_action)
df_action = pd.read_csv(f_action)
fig, ax = plt.subplots(figsize=(8, 5))
df_action.set_index('scenario_id')[['action_0_decrease_pct', 'action_1_keep_pct', 'action_2_increase_pct']].plot(kind='bar', ax=ax)
plt.title('DQN Action Distribution (S1 & S2)')
plt.ylabel('Percentage (%)')
plt.xlabel('Scenario')
plt.legend(['Decrease', 'Keep', 'Increase'])
plt.tight_layout()
plt.savefig('figures/final/dqn_action_distribution_s1_s2.png')
plt.close()
add_manifest('dqn_action_distribution_s1_s2.png', f_action, "Matplotlib bar chart", "Shows S1 degenerate policy", "Report/Slides")
print("Generated: dqn_action_distribution_s1_s2.png")

# 5. DQN Reward Curves (Copy / Merge)
try:
    from PIL import Image
    im1 = Image.open('figures/drl/dqn_reward_curve_s1.png')
    im2 = Image.open('figures/drl/dqn_reward_curve_s2.png')
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    dst.save('figures/final/dqn_reward_curves_s1_s2.png')
    add_manifest('dqn_reward_curves_s1_s2.png', "figures/drl/dqn_reward_curve_s*.png", "PIL merge", "Training reward != performance", "Slides")
    print("Generated: dqn_reward_curves_s1_s2.png")
except Exception as e:
    print(f"Skipping reward curves merge: {e}")

# Write figure source map
with open('reports/final/final-figure-source-map.md', 'w') as f:
    f.write("# Final Figure Source Map\n\n")
    f.write("| Figure | Path | Source CSV / Artifact | Generation Method | Caveat | Used In |\n")
    f.write("|--------|------|-----------------------|-------------------|--------|---------|\n")
    for entry in manifest_entries:
        f.write(entry + "\n")
print("Generated source map: reports/final/final-figure-source-map.md")
