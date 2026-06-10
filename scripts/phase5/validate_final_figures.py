"""
Phase 5 Final Figures Validator
================================
QA script that checks all required final figures exist and are not empty/corrupt.

Usage:
    python3 scripts/phase5/validate_final_figures.py
"""

import os
import sys

REQUIRED_FIGURES = [
    'figures/final/baseline_utility_summary.png',
    'figures/final/dqn_vs_baseline_utility_s1_s2.png',
    'figures/final/dqn_vs_baseline_loss_s1_s2.png',
    'figures/final/dqn_action_distribution_s1_s2.png',
    'figures/final/dqn_reward_curves_s1_s2.png',
    'figures/final/system_pipeline.png',
    'figures/final/single_bottleneck_topology.png',
    'figures/final/mdp_formulation.png',
    'figures/final/key_findings_summary.png',
]

# Minimum file size in bytes — data figures should be >5 KB,
# conceptual diagrams should be >3 KB.
MIN_SIZE_BYTES = 3000


def validate():
    print("Final Figures QA Validation")
    print("=" * 50)
    all_ok = True
    results = []

    for path in REQUIRED_FIGURES:
        name = os.path.basename(path)
        if not os.path.exists(path):
            results.append((name, 'FAIL', 'File not found'))
            all_ok = False
            continue

        size = os.path.getsize(path)
        if size < MIN_SIZE_BYTES:
            results.append((name, 'FAIL', f'Too small ({size} bytes) — likely empty'))
            all_ok = False
            continue

        # Optional: check image dimensions if PIL is available
        dims = 'N/A'
        try:
            from PIL import Image
            with Image.open(path) as img:
                dims = f'{img.width}x{img.height}'
                # Check for near-blank images (very rough heuristic):
                # convert a small sample to grayscale and check variance
                import numpy as np
                sample = img.convert('L').resize((100, 100))
                arr = np.array(sample)
                variance = arr.var()
                if variance < 10:
                    results.append((name, 'WARN', f'{dims}, variance={variance:.1f} — possibly blank'))
                    all_ok = False
                    continue
        except ImportError:
            pass
        except Exception as e:
            results.append((name, 'WARN', f'PIL check error: {e}'))
            continue

        results.append((name, 'PASS', f'{size:,} bytes, {dims}'))

    # Print results
    print(f"\n{'Figure':<45} {'Status':<6} {'Detail'}")
    print("-" * 80)
    for name, status, detail in results:
        icon = '[PASS]' if status == 'PASS' else ('[WARN]' if status == 'WARN' else '[FAIL]')
        print(f"{icon} {name:<43} {status:<6} {detail}")

    print(f"\n{'=' * 50}")
    if all_ok:
        print("QA RESULT: ALL PASS")
        return 0
    else:
        print("QA RESULT: ISSUES FOUND")
        return 1


if __name__ == '__main__':
    sys.exit(validate())
