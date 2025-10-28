#!/usr/bin/env python3
"""
Verify the emotional loss calculation fix
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from emotional_metrics.signal_extraction import extract_emotional_signals
from emotional_metrics.loss_calculation import calculate_emotional_loss

def test_fixed_loss_calculation():
    """Test the fixed loss calculation"""
    print("🧪 TESTING FIXED LOSS CALCULATION")
    print("=" * 50)
    
    test_cases = [
        {
            'original': "I'm really frustrated that my account isn't working!",
            'compressed': "Account not working.",
            'description': "Frustration in original, neutral in compressed"
        },
        {
            'original': "I'm absolutely thrilled about our new project!",
            'compressed': "Project timeline.",
            'description': "Excitement in original, neutral in compressed"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {case['description']}")
        print(f"Original: '{case['original']}'")
        print(f"Compressed: '{case['compressed']}'")
        
        orig_signals = extract_emotional_signals(case['original'])
        comp_signals = extract_emotional_signals(case['compressed'])
        
        print(f"Original signals: {orig_signals}")
        print(f"Compressed signals: {comp_signals}")
        
        loss = calculate_emotional_loss(orig_signals, comp_signals)
        print(f"Emotional loss: {loss['overall_loss']:.3f}")
        print(f"Dimensional losses: {loss['dimensional_loss']}")
        
        if loss['overall_loss'] > 0:
            print("✅ SUCCESS: Loss is now being calculated!")
        else:
            print("❌ ISSUE: Loss is still zero")

if __name__ == "__main__":
    test_fixed_loss_calculation()