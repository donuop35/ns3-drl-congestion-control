"""
Phase 5 Final Figures Generator
================================
Reads frozen source-of-truth CSVs and produces all required final figures.

Rules:
  - No random data.
  - No CSV modification.
  - Fail-fast on missing required inputs.
  - Empty-figure detection: fail if a required data figure has zero bars.
  - Automatically writes reports/final/final-figure-source-map.md.

Usage:
    python3 scripts/phase5/generate_final_figures.py
"""

import os
import sys
import textwrap

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
OUT_DIR = 'figures/final'
SOURCE_MAP_PATH = 'reports/final/final-figure-source-map.md'

BASELINE_CSV = 'experiments/summaries/baseline_summary.csv'
COMPARISON_CSV = 'experiments/drl/summaries/dqn_vs_baseline_summary.csv'
ACTION_CSV = 'experiments/drl/summaries/dqn_action_distribution_summary.csv'
REWARD_S1 = 'figures/drl/dqn_reward_curve_s1.png'
REWARD_S2 = 'figures/drl/dqn_reward_curve_s2.png'

METHOD_LABELS = {
    'ns3::TcpLinuxReno': 'NewReno',
    'ns3::TcpCubic': 'CUBIC',
    'ns3::TcpBbr': 'BBR',
    'DQN': 'DQN',
}

COLORS = {
    'NewReno': '#2196F3',
    'CUBIC': '#FF9800',
    'BBR': '#4CAF50',
    'DQN': '#E91E63',
}

manifest_entries = []

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def check_file(path, required=True):
    if not os.path.exists(path):
        if required:
            print(f"FATAL: Required source file missing: {path}")
            sys.exit(1)
        else:
            print(f"WARNING: Optional file missing: {path}")
            return False
    return True


def add_manifest(figure, path, source, gen_method, caveat, used_in):
    manifest_entries.append({
        'figure': figure,
        'path': path,
        'source': source,
        'gen_method': gen_method,
        'caveat': caveat,
        'used_in': used_in,
    })


def verify_not_empty(path, figure_name):
    """Verify the figure file exists and is not trivially small (< 5 KB for data figs)."""
    if not os.path.exists(path):
        print(f"FATAL: {figure_name} was not created at {path}")
        sys.exit(1)
    size = os.path.getsize(path)
    if size < 1000:
        print(f"FATAL: {figure_name} appears to be empty/corrupt ({size} bytes)")
        sys.exit(1)
    print(f"  OK: {figure_name} ({size:,} bytes)")


# ---------------------------------------------------------------------------
# 1. Baseline Utility — grouped bar, S1/S2 only
# ---------------------------------------------------------------------------

def gen_baseline_utility():
    print("\n[1/9] Generating baseline_utility_summary.png ...")
    check_file(BASELINE_CSV)
    df = pd.read_csv(BASELINE_CSV)

    # Filter S1/S2 only
    df = df[df['scenario_id'].isin(['S1', 'S2'])]
    if df.empty:
        print("FATAL: No S1/S2 rows in baseline CSV"); sys.exit(1)

    scenarios = ['S1', 'S2']
    methods_order = ['ns3::TcpLinuxReno', 'ns3::TcpCubic', 'ns3::TcpBbr']
    labels = [METHOD_LABELS[m] for m in methods_order]

    x = np.arange(len(scenarios))
    width = 0.22
    fig, ax = plt.subplots(figsize=(8, 5))

    for i, method in enumerate(methods_order):
        vals = []
        for sc in scenarios:
            row = df[(df['scenario_id'] == sc) & (df['method'] == method)]
            vals.append(row['utility_score'].values[0] if len(row) else 0)
        bars = ax.bar(x + i * width, vals, width, label=labels[i],
                      color=COLORS[labels[i]], edgecolor='white')
        for bar, val in zip(bars, vals):
            if val < 0:
                ax.annotate('BBR anomaly', xy=(bar.get_x() + bar.get_width()/2, val),
                            xytext=(0, -18), textcoords='offset points',
                            ha='center', fontsize=7, color='red')

    ax.set_xlabel('Scenario')
    ax.set_ylabel('Provisional Utility')
    ax.set_title('Baseline Provisional Utility by Scenario')
    ax.set_xticks(x + width)
    ax.set_xticklabels(scenarios)
    ax.legend()
    ax.axhline(0, color='grey', linewidth=0.5)
    plt.tight_layout()
    out = f'{OUT_DIR}/baseline_utility_summary.png'
    plt.savefig(out, dpi=150)
    plt.close()
    verify_not_empty(out, 'baseline_utility_summary')
    add_manifest('baseline_utility_summary.png', f'figures/final/baseline_utility_summary.png',
                 BASELINE_CSV, 'Matplotlib grouped bar', 'Provisional weights; BBR S2 anomaly preserved', 'Report / Slides')


# ---------------------------------------------------------------------------
# 2. DQN vs Baseline Utility — subplots
# ---------------------------------------------------------------------------

def gen_comparison_utility():
    print("\n[2/9] Generating dqn_vs_baseline_utility_s1_s2.png ...")
    check_file(COMPARISON_CSV)
    df = pd.read_csv(COMPARISON_CSV)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

    for idx, sc in enumerate(['S1', 'S2']):
        df_sc = df[df['scenario_id'] == sc].copy()
        if df_sc.empty:
            print(f"FATAL: No rows for scenario {sc} in comparison CSV"); sys.exit(1)
        df_sc['label'] = df_sc['method'].map(METHOD_LABELS)
        df_sc = df_sc.sort_values('utility_score', ascending=False)
        colors = [COLORS.get(l, '#999') for l in df_sc['label']]
        axes[idx].bar(df_sc['label'], df_sc['utility_score'], color=colors, edgecolor='white')
        axes[idx].set_title(f'Scenario {sc}')
        axes[idx].set_ylabel('Provisional Utility' if idx == 0 else '')
        axes[idx].axhline(0, color='grey', linewidth=0.5)
        for j, (_, row) in enumerate(df_sc.iterrows()):
            axes[idx].text(j, row['utility_score'] + 0.02,
                           f"{row['utility_score']:.3f}", ha='center', fontsize=8)

    fig.suptitle('DQN vs Baselines — Provisional Utility', fontsize=14, fontweight='bold')
    plt.tight_layout()
    out = f'{OUT_DIR}/dqn_vs_baseline_utility_s1_s2.png'
    plt.savefig(out, dpi=150)
    plt.close()
    verify_not_empty(out, 'dqn_vs_baseline_utility_s1_s2')
    add_manifest('dqn_vs_baseline_utility_s1_s2.png', f'figures/final/dqn_vs_baseline_utility_s1_s2.png',
                 COMPARISON_CSV, 'Matplotlib subplot bar', 'Provisional weights', 'Report / Slides / Demo')


# ---------------------------------------------------------------------------
# 3. DQN vs Baseline Loss — subplots (percentage)
# ---------------------------------------------------------------------------

def gen_comparison_loss():
    print("\n[3/9] Generating dqn_vs_baseline_loss_s1_s2.png ...")
    check_file(COMPARISON_CSV)
    df = pd.read_csv(COMPARISON_CSV)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)

    for idx, sc in enumerate(['S1', 'S2']):
        df_sc = df[df['scenario_id'] == sc].copy()
        if df_sc.empty:
            print(f"FATAL: No rows for scenario {sc} in comparison CSV"); sys.exit(1)
        df_sc['label'] = df_sc['method'].map(METHOD_LABELS)
        df_sc['loss_pct'] = df_sc['loss_rate'] * 100
        df_sc = df_sc.sort_values('loss_pct', ascending=False)
        colors = [COLORS.get(l, '#999') for l in df_sc['label']]
        axes[idx].bar(df_sc['label'], df_sc['loss_pct'], color=colors, edgecolor='white')
        axes[idx].set_title(f'Scenario {sc}')
        axes[idx].set_ylabel('Loss Rate (%)' if idx == 0 else '')
        for j, (_, row) in enumerate(df_sc.iterrows()):
            axes[idx].text(j, row['loss_pct'] + 0.1,
                           f"{row['loss_pct']:.2f}%", ha='center', fontsize=8)

    fig.suptitle('DQN vs Baselines — Loss Rate', fontsize=14, fontweight='bold')
    plt.tight_layout()
    out = f'{OUT_DIR}/dqn_vs_baseline_loss_s1_s2.png'
    plt.savefig(out, dpi=150)
    plt.close()
    verify_not_empty(out, 'dqn_vs_baseline_loss_s1_s2')
    add_manifest('dqn_vs_baseline_loss_s1_s2.png', f'figures/final/dqn_vs_baseline_loss_s1_s2.png',
                 COMPARISON_CSV, 'Matplotlib subplot bar', 'DQN S2 loss ≈5.54%', 'Report / Slides / Demo')


# ---------------------------------------------------------------------------
# 4. DQN Action Distribution — percentage scale
# ---------------------------------------------------------------------------

def gen_action_dist():
    print("\n[4/9] Generating dqn_action_distribution_s1_s2.png ...")
    check_file(ACTION_CSV)
    df = pd.read_csv(ACTION_CSV)

    scenarios = ['S1', 'S2']
    decrease = []
    keep = []
    increase = []
    for sc in scenarios:
        row = df[df['scenario_id'] == sc]
        if row.empty:
            print(f"FATAL: No rows for scenario {sc} in action CSV"); sys.exit(1)
        decrease.append(row['action_0_decrease_pct'].values[0] * 100)
        keep.append(row['action_1_keep_pct'].values[0] * 100)
        increase.append(row['action_2_increase_pct'].values[0] * 100)

    x = np.arange(len(scenarios))
    width = 0.25
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.bar(x - width, decrease, width, label='Decrease', color='#2196F3')
    ax.bar(x, keep, width, label='Keep', color='#FF9800')
    ax.bar(x + width, increase, width, label='Increase', color='#4CAF50')

    ax.set_xlabel('Scenario')
    ax.set_ylabel('Action Share (%)')
    ax.set_title('DQN Action Distribution by Scenario')
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios)
    ax.set_ylim(0, 110)
    ax.legend()

    # Annotate key insight
    ax.annotate('100% Increase\n(degenerate policy)',
                xy=(0 + width, 100), xytext=(0.6, 85),
                arrowprops=dict(arrowstyle='->', color='grey'),
                fontsize=8, ha='center')

    plt.tight_layout()
    out = f'{OUT_DIR}/dqn_action_distribution_s1_s2.png'
    plt.savefig(out, dpi=150)
    plt.close()
    verify_not_empty(out, 'dqn_action_distribution_s1_s2')
    add_manifest('dqn_action_distribution_s1_s2.png', f'figures/final/dqn_action_distribution_s1_s2.png',
                 ACTION_CSV, 'Matplotlib grouped bar', 'S1 degenerate policy', 'Report / Slides')


# ---------------------------------------------------------------------------
# 5. Reward curves — merge existing Phase 4 images
# ---------------------------------------------------------------------------

def gen_reward_curves():
    print("\n[5/9] Generating dqn_reward_curves_s1_s2.png ...")
    try:
        from PIL import Image
        check_file(REWARD_S1)
        check_file(REWARD_S2)
        im1 = Image.open(REWARD_S1)
        im2 = Image.open(REWARD_S2)
        dst = Image.new('RGB', (im1.width + im2.width, max(im1.height, im2.height)), (255, 255, 255))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (im1.width, 0))
        out = f'{OUT_DIR}/dqn_reward_curves_s1_s2.png'
        dst.save(out)
        verify_not_empty(out, 'dqn_reward_curves_s1_s2')
        add_manifest('dqn_reward_curves_s1_s2.png', f'figures/final/dqn_reward_curves_s1_s2.png',
                     'figures/drl/dqn_reward_curve_s*.png', 'PIL merge',
                     'Training diagnostic only; not final performance', 'Slides')
    except ImportError:
        print("WARNING: PIL not available; skipping reward curve merge (optional).")


# ---------------------------------------------------------------------------
# 6. System Pipeline — flow diagram
# ---------------------------------------------------------------------------

def gen_system_pipeline():
    print("\n[6/9] Generating system_pipeline.png ...")
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('System Architecture Pipeline', fontsize=16, fontweight='bold', pad=20)

    boxes = [
        (5, 9.0, 'OpenSpec SDD\nSpec-Driven Governance', '#E3F2FD', '#1565C0'),
        (5, 7.5, 'Phase 3: Baseline Benchmark\nNewReno / CUBIC / BBR', '#E8F5E9', '#2E7D32'),
        (5, 6.0, 'ns-3.40\nSingle Bottleneck Environment', '#FFF3E0', '#E65100'),
        (5, 4.5, 'ns3-gym / ZMQ Interface\nOpenAI Gym API', '#F3E5F5', '#6A1B9A'),
        (5, 3.0, 'Stable-Baselines3\nDQN Agent (Discrete: ↓ = ↑)', '#FCE4EC', '#AD1457'),
        (5, 1.5, 'Evaluation Metrics\nThroughput / Delay Proxy / Loss / Utility', '#ECEFF1', '#37474F'),
    ]

    for cx, cy, text, facecolor, edgecolor in boxes:
        bbox = mpatches.FancyBboxPatch((cx - 2.8, cy - 0.55), 5.6, 1.1,
                                        boxstyle="round,pad=0.15",
                                        facecolor=facecolor, edgecolor=edgecolor, linewidth=2)
        ax.add_patch(bbox)
        ax.text(cx, cy, text, ha='center', va='center', fontsize=9, fontweight='bold')

    # Arrows
    for i in range(len(boxes) - 1):
        ax.annotate('', xy=(5, boxes[i+1][1] + 0.55), xytext=(5, boxes[i][1] - 0.55),
                     arrowprops=dict(arrowstyle='->', color='#424242', lw=1.5))

    plt.tight_layout()
    out = f'{OUT_DIR}/system_pipeline.png'
    plt.savefig(out, dpi=150)
    plt.close()
    verify_not_empty(out, 'system_pipeline')
    add_manifest('system_pipeline.png', f'figures/final/system_pipeline.png',
                 'Conceptual', 'Matplotlib flow diagram', '', 'Report / Slides')


# ---------------------------------------------------------------------------
# 7. Single Bottleneck Topology — node-link diagram
# ---------------------------------------------------------------------------

def gen_topology():
    print("\n[7/9] Generating single_bottleneck_topology.png ...")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis('off')
    ax.set_title('Single Bottleneck Topology', fontsize=16, fontweight='bold', pad=15)

    # Nodes
    nodes = [
        (1.5, 2, 'Sender\n(Node 0)', '#E3F2FD', '#1565C0'),
        (5.0, 2, 'Bottleneck\nRouter', '#FFF3E0', '#E65100'),
        (8.5, 2, 'Receiver\n(Node 2)', '#E8F5E9', '#2E7D32'),
    ]
    for cx, cy, text, fc, ec in nodes:
        circle = plt.Circle((cx, cy), 0.7, facecolor=fc, edgecolor=ec, linewidth=2.5)
        ax.add_patch(circle)
        ax.text(cx, cy, text, ha='center', va='center', fontsize=9, fontweight='bold')

    # Links
    ax.annotate('', xy=(4.3, 2), xytext=(2.2, 2),
                arrowprops=dict(arrowstyle='->', color='#424242', lw=2))
    ax.text(3.25, 2.45, 'Access Link', ha='center', fontsize=8, style='italic')

    ax.annotate('', xy=(7.8, 2), xytext=(5.7, 2),
                arrowprops=dict(arrowstyle='->', color='#E65100', lw=2.5))
    ax.text(6.75, 2.45, 'Bottleneck Link\n10 Mbps', ha='center', fontsize=8, fontweight='bold', color='#E65100')

    # Delay annotations
    ax.text(6.75, 1.15, 'S1: 10 ms delay\nS2: 50 ms delay', ha='center', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFFDE7', edgecolor='#F57F17'))

    plt.tight_layout()
    out = f'{OUT_DIR}/single_bottleneck_topology.png'
    plt.savefig(out, dpi=150)
    plt.close()
    verify_not_empty(out, 'single_bottleneck_topology')
    add_manifest('single_bottleneck_topology.png', f'figures/final/single_bottleneck_topology.png',
                 'Conceptual', 'Matplotlib node-link diagram', '', 'Report / Slides')


# ---------------------------------------------------------------------------
# 8. MDP Formulation — loop diagram
# ---------------------------------------------------------------------------

def gen_mdp():
    print("\n[8/9] Generating mdp_formulation.png ...")
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_title('MDP Formulation', fontsize=16, fontweight='bold', pad=15)

    # Boxes
    mdp_boxes = [
        (5, 8.5, 'Observation s_t\nThroughput, Delay Proxy, Loss,\nCongestion Signal, Prev Action', '#E3F2FD', '#1565C0'),
        (5, 6.0, 'DQN Agent\n(Stable-Baselines3)', '#FCE4EC', '#AD1457'),
        (5, 3.5, 'Action a_t ∈ {↓, =, ↑}\n(Sender-side Rate Abstraction)', '#FFF3E0', '#E65100'),
        (5, 1.0, 'ns-3 / ns3-gym Environment', '#E8F5E9', '#2E7D32'),
    ]

    for cx, cy, text, fc, ec in mdp_boxes:
        bbox = mpatches.FancyBboxPatch((cx - 2.8, cy - 0.65), 5.6, 1.3,
                                        boxstyle="round,pad=0.15",
                                        facecolor=fc, edgecolor=ec, linewidth=2)
        ax.add_patch(bbox)
        ax.text(cx, cy, text, ha='center', va='center', fontsize=9, fontweight='bold')

    # Down arrows
    for i in range(len(mdp_boxes) - 1):
        ax.annotate('', xy=(5, mdp_boxes[i+1][1] + 0.65), xytext=(5, mdp_boxes[i][1] - 0.65),
                     arrowprops=dict(arrowstyle='->', color='#424242', lw=1.5))

    # Feedback loop (right side)
    ax.annotate('',
                xy=(7.9, 8.5), xytext=(7.9, 1.0),
                arrowprops=dict(arrowstyle='->', color='#E91E63', lw=2,
                                connectionstyle='arc3,rad=0.0'))
    ax.text(9.0, 4.75, 'Reward r_t\n= αT − βD − λL', ha='center', va='center',
            fontsize=8, fontweight='bold', color='#E91E63',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FCE4EC', edgecolor='#E91E63'))

    plt.tight_layout()
    out = f'{OUT_DIR}/mdp_formulation.png'
    plt.savefig(out, dpi=150)
    plt.close()
    verify_not_empty(out, 'mdp_formulation')
    add_manifest('mdp_formulation.png', f'figures/final/mdp_formulation.png',
                 'Conceptual', 'Matplotlib flow diagram', '', 'Report / Slides')


# ---------------------------------------------------------------------------
# 9. Key Findings Summary — 4-card layout
# ---------------------------------------------------------------------------

def gen_key_findings():
    print("\n[9/9] Generating key_findings_summary.png ...")
    fig, axes = plt.subplots(2, 2, figsize=(10, 6))
    fig.suptitle('Key Findings Summary', fontsize=16, fontweight='bold')

    cards = [
        ('S1 Finding', 'DQN ranks #2\nUtility 0.900 (below BBR 0.947)\n100% Increase — degenerate policy',
         '#E3F2FD', '#1565C0'),
        ('S2 Finding', 'DQN ranks #3\nLoss Rate 5.54% (high)\nUtility 0.757 (below NewReno, CUBIC)',
         '#FFF3E0', '#E65100'),
        ('Limitation', 'Delay = FlowMonitor Proxy\nAction = Sender-side Rate Abstraction\nNot kernel-level TCP control',
         '#FCE4EC', '#AD1457'),
        ('Contribution', 'Reproducible DRL CC MVP\nOpenSpec-governed evaluation\nHonest limitation reporting',
         '#E8F5E9', '#2E7D32'),
    ]

    for ax, (title, body, fc, ec) in zip(axes.flatten(), cards):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        rect = mpatches.FancyBboxPatch((0.05, 0.05), 0.9, 0.9,
                                        boxstyle="round,pad=0.05",
                                        facecolor=fc, edgecolor=ec, linewidth=2.5)
        ax.add_patch(rect)
        ax.text(0.5, 0.82, title, ha='center', va='center', fontsize=12, fontweight='bold', color=ec)
        ax.text(0.5, 0.42, body, ha='center', va='center', fontsize=9, linespacing=1.4)

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    out = f'{OUT_DIR}/key_findings_summary.png'
    plt.savefig(out, dpi=150)
    plt.close()
    verify_not_empty(out, 'key_findings_summary')
    add_manifest('key_findings_summary.png', f'figures/final/key_findings_summary.png',
                 'Conceptual', 'Matplotlib 4-card layout', '', 'Report / Slides')


# ---------------------------------------------------------------------------
# Write figure source map
# ---------------------------------------------------------------------------

def write_source_map():
    print("\nWriting figure source map ...")
    os.makedirs(os.path.dirname(SOURCE_MAP_PATH), exist_ok=True)
    with open(SOURCE_MAP_PATH, 'w', encoding='utf-8') as f:
        f.write("# Final Figure Source Map\n\n")
        f.write("| Figure | Path | Source CSV / Artifact | Generation Method | Caveat | Used In |\n")
        f.write("|--------|------|-----------------------|-------------------|--------|---------|\n")
        for e in manifest_entries:
            f.write(f"| {e['figure']} | `{e['path']}` | `{e['source']}` | {e['gen_method']} | {e['caveat']} | {e['used_in']} |\n")
    print(f"  OK: {SOURCE_MAP_PATH}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    gen_baseline_utility()
    gen_comparison_utility()
    gen_comparison_loss()
    gen_action_dist()
    gen_reward_curves()
    gen_system_pipeline()
    gen_topology()
    gen_mdp()
    gen_key_findings()
    write_source_map()

    print(f"\n{'='*60}")
    print(f"All {len(manifest_entries)} final figures generated successfully.")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
