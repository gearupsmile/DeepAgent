#!/usr/bin/env python3
"""
Run emotional audit using ACTUAL DeepAgent compression
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from emotional_test_cases.test_conversations import get_all_test_cases
from deepagent_integrations import get_actual_deepagent_memory_folding, analyze_emotional_filters

def run_actual_deepagent_audit():
    """Run audit using actual DeepAgent memory folding"""
    test_cases = get_all_test_cases()
    
    print("🔬 RUNNING ACTUAL DEEPAGENT EMOTIONAL AUDIT")
    print("=" * 60)
    
    all_filters = []
    
    for i, case in enumerate(test_cases[:3]):  # Test first 3 cases for now
        print(f"\n🎯 TEST CASE {i+1}: {case['scenario']}")
        print(f"Emotional Ground Truth: {case['emotional_ground_truth']['primary_emotion']}")
        
        # Get actual DeepAgent compression
        compressed = get_actual_deepagent_memory_folding(case['conversation'], "Test emotional conversation")
        
        if compressed and 'emotional_filters_detected' in compressed:
            filters = compressed['emotional_filters_detected']
            all_filters.extend(filters)
            
            print(f"🚫 EMOTIONAL FILTERS DETECTED: {len(filters)}")
            for filter_desc in filters:
                print(f"   - {filter_desc}")
        
        print("-" * 50)
    
    # Summary of systematic emotional filtering
    print("\n" + "=" * 60)
    print("📊 SYSTEMATIC EMOTIONAL FILTERING ANALYSIS")
    print("=" * 60)
    
    unique_filters = list(set(all_filters))
    print(f"Total unique emotional filters: {len(unique_filters)}")
    
    for filter_desc in unique_filters:
        count = all_filters.count(filter_desc)
        print(f"🔧 {filter_desc} (appears in {count} cases)")

if __name__ == "__main__":
    run_actual_deepagent_audit()