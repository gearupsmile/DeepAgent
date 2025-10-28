"""
Emotional signal extraction from conversation text
Simple rule-based and keyword-based approach
"""

def extract_emotional_signals(conversation):
    """
    Extract emotional signals from conversation text
    Returns dict of emotional metrics
    """
    full_text = ' '.join(conversation)
    
    signals = {
        'emotional_keywords': extract_emotional_keywords(full_text),
        'sentiment_trend': calculate_sentiment_trend(conversation),
        'urgency_indicators': detect_urgency_indicators(full_text),
        'frustration_level': detect_frustration_level(full_text),
        'confidence_indicators': detect_confidence_indicators(full_text),
        'rapport_indicators': detect_rapport_indicators(full_text)
    }
    
    return signals

def extract_emotional_keywords(text):
    """Detect emotional keywords in text"""
    emotion_keywords = {
        'frustration': ['frustrating', 'annoying', 'unacceptable', 'ridiculous', 'useless'],
        'anger': ['angry', 'mad', 'furious', 'outrageous', 'complaint'],
        'sarcasm': ['brilliant', 'great', 'wonderful', 'fantastic', 'perfect'],  # Often sarcastic in complaints
        'anxiety': ['unsure', 'nervous', 'anxious', 'worried', 'concerned', 'what if'],
        'urgency': ['immediately', 'right now', 'urgent', 'asap', 'emergency', 'critical'],
        'pride': ['proud', 'achievement', 'accomplished', 'success', 'finished'],
        'gratitude': ['thank you', 'thanks', 'appreciate', 'helpful', 'grateful'],
        'confusion': ['confused', 'not sure', 'don\'t know', 'uncertain', 'which one'],
        'overwhelm': ['overwhelmed', 'too much', 'complicated', 'complex', 'too many'],
        'impatience': ['how long', 'taking forever', 'slow', 'hurry up', 'waiting']
    }
    
    detected = {}
    text_lower = text.lower()
    
    for emotion, keywords in emotion_keywords.items():
        count = sum(1 for keyword in keywords if keyword in text_lower)
        if count > 0:
            detected[emotion] = count
    
    return detected

def calculate_sentiment_trend(conversation):
    """Simple sentiment trend across conversation turns"""
    sentiment_scores = []
    
    for turn in conversation:
        if any(word in turn.lower() for word in ['thank', 'appreciate', 'great', 'good', 'perfect']):
            sentiment_scores.append(1)
        elif any(word in turn.lower() for word in ['frustrat', 'angry', 'mad', 'disappoint', 'bad']):
            sentiment_scores.append(-1)
        else:
            sentiment_scores.append(0)
    
    if len(sentiment_scores) < 2:
        return 'neutral'
    
    # Check trend
    if sentiment_scores[-1] > sentiment_scores[0]:
        return 'improving'
    elif sentiment_scores[-1] < sentiment_scores[0]:
        return 'worsening'
    else:
        return 'stable'

def detect_urgency_indicators(text):
    """Detect urgency in conversation"""
    urgent_phrases = ['right now', 'immediately', 'asap', 'emergency', 'critical', 'urgent']
    text_lower = text.lower()
    
    urgency_score = sum(1 for phrase in urgent_phrases if phrase in text_lower)
    
    if urgency_score >= 2:
        return 'high'
    elif urgency_score == 1:
        return 'medium'
    else:
        return 'low'

def detect_frustration_level(text):
    """Detect frustration level"""
    frustration_words = ['frustrat', 'annoying', 'ridiculous', 'useless', 'stupid', 'hate']
    text_lower = text.lower()
    
    frustration_count = sum(1 for word in frustration_words if word in text_lower)
    
    if frustration_count >= 3:
        return 'high'
    elif frustration_count >= 1:
        return 'medium'
    else:
        return 'low'

def detect_confidence_indicators(text):
    """Detect user confidence level"""
    low_confidence = ['unsure', 'not sure', 'don\'t know', 'maybe', 'perhaps', 'could be']
    high_confidence = ['certain', 'definitely', 'sure', 'know', 'confident']
    
    text_lower = text.lower()
    
    low_count = sum(1 for phrase in low_confidence if phrase in text_lower)
    high_count = sum(1 for phrase in high_confidence if phrase in text_lower)
    
    if low_count > high_count:
        return 'low'
    elif high_count > low_count:
        return 'high'
    else:
        return 'neutral'

def detect_rapport_indicators(text):
    """Detect rapport-building language"""
    rapport_phrases = ['thank you', 'please', 'appreciate', 'helpful', 'good job', 'thanks']
    text_lower = text.lower()
    
    rapport_score = sum(1 for phrase in rapport_phrases if phrase in text_lower)
    
    if rapport_score >= 2:
        return 'strong'
    elif rapport_score == 1:
        return 'moderate'
    else:
        return 'weak'