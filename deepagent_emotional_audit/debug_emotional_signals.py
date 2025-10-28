#!/usr/bin/env python3
"""
Debug emotional signal extraction and loss calculation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from emotional_metrics.signal_extraction import extract_emotional_signals
from emotional_metrics.loss_calculation import calculate_emotional_loss
from emotional_test_cases.test_conversations import load_test_conversations

def debug_signals():
    """Debug what signals are being extracted"""
    print("🔍 DEBUGGING EMOTIONAL SIGNAL EXTRACTION")
    print("=" * 60)
    
    conversations = load_test_conversations()
    
    for i, conv in enumerate(conversations):
        print(f"\n📝 Conversation {i+1}: {conv['id']}")
        print(f"Original: '{conv['original']}'")
        print(f"Compressed: '{conv['compressed']}'")
        
        # Extract signals
        original_signals = extract_emotional_signals(conv['original'])
        compressed_signals = extract_emotional_signals(conv['compressed'])
        
        print(f"Original signals: {original_signals}")
        print(f"Compressed signals: {compressed_signals}")
        
        # Calculate loss
        loss = calculate_emotional_loss(original_signals, compressed_signals)
        print(f"Emotional loss: {loss}")
        
        print("-" * 50)

def test_specific_cases():
    """Test specific emotional cases"""
    print("\n🧪 TESTING SPECIFIC EMOTIONAL CASES")
    print("=" * 60)
    
    test_cases = [
        ("I'm really frustrated that my account isn't working!", "Account not working."),
        ("I'm absolutely thrilled about our new project!", "Project timeline discussed."),
        ("I'm quite concerned about the budget constraints.", "Budget concerns."),
        ("This idea is amazing! I'm so excited!", "Ideas discussed.")
    ]
    
    for original, compressed in test_cases:
        print(f"\nOriginal: '{original}'")
        print(f"Compressed: '{compressed}'")
        
        orig_signals = extract_emotional_signals(original)
        comp_signals = extract_emotional_signals(compressed)
        
        print(f"Original emotions: {orig_signals}")
        print(f"Compressed emotions: {comp_signals}")
        
        loss = calculate_emotional_loss(orig_signals, comp_signals)
        print(f"Loss: {loss['overall_loss']:.3f}")

if __name__ == "__main__":
    debug_signals()
    test_specific_cases()