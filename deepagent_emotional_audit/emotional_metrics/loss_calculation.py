"""
Calculate emotional context loss between original and compressed
"""

def calculate_emotional_loss(original_signals, compressed_signals, ground_truth):
    """
    Calculate emotional context loss
    """
    losses = {}
    
    # 1. Emotional keyword loss
    original_emotions = set(original_signals.get('emotional_keywords', {}).keys())
    compressed_emotions = set(compressed_signals.get('emotional_keywords', {}).keys())
    
    emotion_overlap = len(original_emotions.intersection(compressed_emotions))
    emotion_union = len(original_emotions.union(compressed_emotions))
    
    if emotion_union > 0:
        losses['emotion_detection'] = 1 - (emotion_overlap / emotion_union)
    else:
        losses['emotion_detection'] = 0.0
    
    # 2. Sentiment trend loss
    original_trend = original_signals.get('sentiment_trend', 'neutral')
    compressed_trend = compressed_signals.get('sentiment_trend', 'neutral')
    losses['sentiment_trend'] = 0.0 if original_trend == compressed_trend else 1.0
    
    # 3. Urgency detection loss
    original_urgency = original_signals.get('urgency_indicators', 'low')
    compressed_urgency = compressed_signals.get('urgency_indicators', 'low')
    losses['urgency_detection'] = 0.0 if original_urgency == compressed_urgency else 1.0
    
    # 4. Frustration level loss
    original_frustration = original_signals.get('frustration_level', 'low')
    compressed_frustration = compressed_signals.get('frustration_level', 'low')
    frustration_map = {'low': 0, 'medium': 0.5, 'high': 1.0}
    
    original_score = frustration_map.get(original_frustration, 0)
    compressed_score = frustration_map.get(compressed_frustration, 0)
    losses['frustration_level'] = abs(original_score - compressed_score)
    
    # 5. Check if required emotional response is preserved
    required_tone = ground_truth.get('required_response_tone', 'neutral')
    # This would need actual response analysis - placeholder for now
    losses['response_appropriateness'] = 0.5  # Placeholder
    
    return losses

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