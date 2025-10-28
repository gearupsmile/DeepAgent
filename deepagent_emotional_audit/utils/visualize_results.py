"""
Simple visualization for emotional audit results
"""

import json
import matplotlib.pyplot as plt
import os
import numpy as np

def load_results():
    """Load the latest results"""
    try:
        with open('results/emotional_audit_results.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading results: {e}")
        return None

def plot_emotional_loss_vs_task_success(results):
    """Plot emotional loss vs task success"""
    if not results:
        print("No results to visualize")
        return
    
    baseline = results.get('baseline_analysis', [])
    task_analysis = results.get('task_impact_analysis', [])
    
    if not baseline or not task_analysis:
        print("Incomplete data for visualization")
        return
    
    # Prepare data
    conv_ids = [conv['conversation_id'] for conv in baseline]
    emotional_losses = [conv['overall_loss'] for conv in baseline]
    task_success_rates = [task['task_success_rate']['success_rate'] for task in task_analysis]
    task_failures = [1 if task['task_success_rate'].get('task_failure') else 0 for task in task_analysis]
    
    # Create plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot 1: Emotional Loss by Conversation
    colors = ['red' if fail else 'green' for fail in task_failures]
    bars = ax1.bar(conv_ids, emotional_losses, color=colors)
    ax1.set_title('Emotional Loss by Conversation')
    ax1.set_ylabel('Emotional Loss')
    ax1.set_xlabel('Conversation ID')
    ax1.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for bar, value in zip(bars, emotional_losses):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                f'{value:.3f}', ha='center', va='bottom', fontsize=8)
    
    # Plot 2: Emotional Loss vs Task Success
    scatter = ax2.scatter(emotional_losses, task_success_rates, c=colors, s=100, alpha=0.7)
    ax2.set_title('Emotional Loss vs Task Success Rate')
    ax2.set_xlabel('Emotional Loss')
    ax2.set_ylabel('Task Success Rate')
    
    # Add conversation labels
    for i, conv_id in enumerate(conv_ids):
        ax2.annotate(conv_id, (emotional_losses[i], task_success_rates[i]), 
                    xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    # Add correlation line if meaningful
    if len(emotional_losses) > 1:
        try:
            z = np.polyfit(emotional_losses, task_success_rates, 1)
            p = np.poly1d(z)
            ax2.plot(emotional_losses, p(emotional_losses), "r--", alpha=0.5)
            ax2.text(0.05, 0.95, f"Trend: y = {z[0]:.2f}x + {z[1]:.2f}", 
                    transform=ax2.transAxes, fontsize=10, verticalalignment='top')
        except:
            pass
    
    plt.tight_layout()
    
    # Save figure
    if not os.path.exists('figures'):
        os.makedirs('figures')
    
    plt.savefig('figures/emotional_audit_results.png', dpi=300, bbox_inches='tight')
    print("📊 Visualization saved to: figures/emotional_audit_results.png")
    plt.show()

def print_dimension_impact(results):
    """Print which emotional dimensions matter most"""
    dimension_impact = results.get('dimension_impact', {})
    
    if dimension_impact:
        print("\n📊 Most Impactful Emotional Dimensions:")
        print("-" * 50)
        for dimension, impact in sorted(dimension_impact.items(), key=lambda x: x[1], reverse=True):
            if impact > 0:
                print(f"  {dimension:15} impact: {impact:.3f}")
            else:
                print(f"  {dimension:15} impact: {impact:.3f} (no impact)")
    else:
        print("\n📊 No dimension impact data available")
    
    # Show high impact cases
    high_impact = results.get('comparative_analysis', {}).get('high_impact_cases', [])
    if high_impact:
        print(f"\n🚨 High Impact Cases ({len(high_impact)}):")
        for case in high_impact[:3]:  # Show top 3
            print(f"  {case['conversation_id']}: Impact Score {case['impact_score']:.3f}")

if __name__ == "__main__":
    results = load_results()
    if results:
        plot_emotional_loss_vs_task_success(results)
        print_dimension_impact(results)
    else:
        print("No results found. Run the audit first.")