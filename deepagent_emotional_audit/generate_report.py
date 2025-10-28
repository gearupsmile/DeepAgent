#!/usr/bin/env python3
"""
Generate a comprehensive emotional audit report
"""

import json
from datetime import datetime

def generate_report():
    """Generate a comprehensive report"""
    try:
        with open('results/emotional_audit_results.json', 'r') as f:
            results = json.load(f)
    except:
        print("No results found. Run the audit first.")
        return
    
    print("=" * 70)
    print("🎭 DEEPAGENT EMOTIONAL AUDIT REPORT")
    print("=" * 70)
    
    # Executive Summary
    baseline = results['baseline_analysis']
    task_analysis = results['task_impact_analysis']
    dimension_impact = results['dimension_impact']
    
    avg_loss = sum(conv['overall_loss'] for conv in baseline) / len(baseline)
    task_failures = sum(1 for task in task_analysis if task['task_success_rate']['task_failure'])
    
    print(f"\n📊 EXECUTIVE SUMMARY")
    print(f"   Conversations Analyzed: {len(baseline)}")
    print(f"   Average Emotional Loss: {avg_loss:.1%}")
    print(f"   Task Failures Due to Compression: {task_failures}/{len(baseline)}")
    
    if dimension_impact:
        top_dimension = max(dimension_impact.items(), key=lambda x: x[1])
        print(f"   Most Critical Emotion: {top_dimension[0].upper()} (Impact: {top_dimension[1]:.3f})")
    
    # Detailed Analysis
    print(f"\n🔍 DETAILED ANALYSIS")
    print("-" * 70)
    
    for i, (conv, task) in enumerate(zip(baseline, task_analysis), 1):
        print(f"\n{i}. {conv['conversation_id'].replace('_', ' ').title()}")
        print(f"   Emotional Loss: {conv['overall_loss']:.1%}")
        print(f"   Task Success: {'✅' if task['task_success_rate']['success_rate'] > 0.6 else '⚠️' if task['task_success_rate']['success_rate'] > 0.3 else '❌'} {task['task_success_rate']['success_rate']:.0%}")
        print(f"   Key Emotions Lost: {', '.join(list(conv['dimensional_loss'].keys())[:3])}")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS")
    print("-" * 70)
    
    if avg_loss > 0.5:
        print("❌ CRITICAL: High emotional loss detected. Review compression algorithms.")
    elif avg_loss > 0.2:
        print("⚠️  MODERATE: Some emotional context lost. Consider emotion-aware compression.")
    else:
        print("✅ GOOD: Emotional context well preserved.")
    
    if task_failures > 0:
        print(f"🚨 {task_failures} tasks failed due to emotional context loss.")
        print("   Focus on preserving critical emotions in key conversations.")
    
    if dimension_impact:
        critical_emotions = [dim for dim, impact in dimension_impact.items() if impact > 0.1]
        if critical_emotions:
            print(f"🎯 Prioritize preserving: {', '.join(critical_emotions).upper()}")
    
    print(f"\n📅 Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)

if __name__ == "__main__":
    generate_report()