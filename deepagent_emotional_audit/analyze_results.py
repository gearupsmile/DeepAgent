"""
Quick analysis of emotional audit results
"""

import json

def analyze_results():
    with open('results/emotional_audit_results.json', 'r') as f:
        results = json.load(f)
    
    print("🎯 EMOTIONAL AUDIT RESULTS SUMMARY")
    print("=" * 50)
    
    # Basic stats
    n_conversations = len(results['baseline_analysis'])
    avg_loss = sum(conv['overall_loss'] for conv in results['baseline_analysis']) / n_conversations
    task_failures = sum(1 for task in results['task_impact_analysis'] if task['task_success_rate']['task_failure'])
    
    print(f"Conversations analyzed: {n_conversations}")
    print(f"Average emotional loss: {avg_loss:.3f}")
    print(f"Task failures due to compression: {task_failures}/{n_conversations}")
    
    # Most impacted dimension
    top_dimension = max(results['dimension_impact'].items(), key=lambda x: x[1]) if results['dimension_impact'] else ('none', 0)
    print(f"Most impactful dimension: {top_dimension[0]} (impact: {top_dimension[1]:.3f})")
    
    # Correlation insight
    correlation = results['comparative_analysis']['overall_correlation']['emotional_loss_task_failure_correlation']
    print(f"Correlation (loss vs failure): {correlation:.3f}")
    
    if correlation > 0.3:
        print("💡 INSIGHT: Strong correlation between emotional loss and task failure!")
    elif correlation > 0.1:
        print("💡 INSIGHT: Moderate correlation detected")
    else:
        print("💡 INSIGHT: Weak correlation - emotional loss may not be primary factor")

if __name__ == "__main__":
    analyze_results()