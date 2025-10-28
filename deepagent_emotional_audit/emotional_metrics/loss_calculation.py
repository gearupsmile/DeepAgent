"""
Fixed emotional loss calculation that handles missing emotions
"""

def calculate_emotional_loss(original_signals, compressed_signals):
    """
    Calculate emotional context loss between original and compressed versions
    Handles cases where emotions are missing in compressed version
    """
    dimensional_loss = {}
    
    # If compressed only has neutral, we need to calculate loss for all original emotions
    has_only_neutral = len(compressed_signals) == 1 and 'neutral' in compressed_signals
    
    for dimension, orig_val in original_signals.items():
        if dimension in compressed_signals:
            # Emotion exists in both - calculate direct loss
            comp_val = compressed_signals[dimension]
            loss = abs(orig_val - comp_val)
        elif has_only_neutral:
            # Emotion missing in compressed - treat as complete loss for that emotion
            # Neutral (0.5) vs strong emotion (0.8) = loss of 0.3
            comp_val = compressed_signals['neutral']
            loss = abs(orig_val - comp_val)
        else:
            # Emotion completely missing - maximum loss
            loss = 1.0
        
        dimensional_loss[dimension] = loss
    
    # Calculate overall loss
    if dimensional_loss:
        overall_loss = sum(dimensional_loss.values()) / len(dimensional_loss)
    else:
        # If no emotions to compare, no loss
        overall_loss = 0
    
    return {
        'overall_loss': overall_loss,
        'dimensional_loss': dimensional_loss,
        'signal_preservation': calculate_signal_preservation(original_signals, compressed_signals)
    }

def calculate_signal_preservation(original, compressed):
    """Calculate what percentage of emotional signals were preserved"""
    preserved_count = 0
    total_signals = len(original)
    
    # If compressed only has neutral, consider it as partial preservation
    has_only_neutral = len(compressed) == 1 and 'neutral' in compressed
    
    for dim, orig_val in original.items():
        if dim in compressed:
            comp_val = compressed[dim]
            # Consider preserved if within 30% of original value
            if abs(orig_val - comp_val) <= 0.3:
                preserved_count += 1
        elif has_only_neutral:
            # With neutral compression, check if emotion is somewhat preserved
            comp_val = compressed['neutral']
            if abs(orig_val - comp_val) <= 0.4:  # More lenient for neutral
                preserved_count += 1
        # Else: emotion completely missing, not preserved
    
    return {
        'preservation_rate': preserved_count / total_signals if total_signals > 0 else 0,
        'preserved_count': preserved_count,
        'total_signals': total_signals
    }

def aggregate_emotional_loss(loss_dict):
    """
    Aggregate individual loss metrics into overall score
    """
    weights = {
        'emotion_detection': 0.25,
        'sentiment_trend': 0.20,
        'urgency_detection': 0.15,
        'frustration_level': 0.20,
        'response_appropriateness': 0.20
    }
    
    total_loss = 0.0
    total_weight = 0.0
    
    for loss_type, loss_value in loss_dict.items():
        weight = weights.get(loss_type, 0.1)
        total_loss += loss_value * weight
        total_weight += weight
    
    if total_weight > 0:
        return total_loss / total_weight
    else:
        return total_loss

def calculate_task_impact(emotional_loss, task_success):
    """
    Simple correlation between emotional loss and task success
    """
    if emotional_loss > 0.7 and not task_success:  # High loss, task failed
        return 'critical_impact'
    elif emotional_loss > 0.5 and not task_success:  # Medium loss, task failed  
        return 'significant_impact'
    elif emotional_loss > 0.3 and task_success:  # Some loss but task succeeded
        return 'moderate_impact'
    else:
        return 'minimal_impact'