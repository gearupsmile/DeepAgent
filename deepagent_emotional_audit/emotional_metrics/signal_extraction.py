"""
Improved emotional signal extraction that works better for compressed text
"""

import re

def extract_emotional_signals(text):
    """
    Extract emotional signals from text using improved keyword matching
    """
    if not text or not isinstance(text, str):
        return {'neutral': 0.5}
    
    text_lower = text.lower()
    signals = {}
    
    # Enhanced emotional keyword matching with weights
    emotional_keywords = {
        'joy': {
            'keywords': ['happy', 'excited', 'great', 'wonderful', 'amazing', 'love', 'fantastic', 'good', 'nice', 'thrilled'],
            'weight': 0.8
        },
        'sadness': {
            'keywords': ['sad', 'unhappy', 'disappointed', 'sorry', 'regret', 'unfortunate', 'bad'],
            'weight': 0.7
        },
        'anger': {
            'keywords': ['angry', 'mad', 'frustrated', 'annoyed', 'outrage', 'furious', 'upset'],
            'weight': 0.9
        },
        'fear': {
            'keywords': ['scared', 'afraid', 'worried', 'concerned', 'anxious', 'nervous', 'fear'],
            'weight': 0.8
        },
        'surprise': {
            'keywords': ['surprised', 'shocked', 'amazed', 'unexpected', 'astonished'],
            'weight': 0.6
        },
        'trust': {
            'keywords': ['trust', 'confident', 'believe', 'reliable', 'dependable'],
            'weight': 0.7
        },
        'anticipation': {
            'keywords': ['excited', 'looking forward', 'anticipate', 'expect', 'waiting', 'hope'],
            'weight': 0.6
        },
        'excitement': {
            'keywords': ['excited', 'thrilled', 'eager', 'enthusiastic', 'pumped', 'energy'],
            'weight': 0.8
        },
        'frustration': {
            'keywords': ['frustrated', 'annoyed', 'irritated', 'displeased', 'upset'],
            'weight': 0.8
        },
        'satisfaction': {
            'keywords': ['satisfied', 'pleased', 'content', 'happy', 'good', 'great'],
            'weight': 0.7
        },
        'confusion': {
            'keywords': ['confused', 'unsure', 'uncertain', 'puzzled', 'bewildered'],
            'weight': 0.6
        },
        'confidence': {
            'keywords': ['confident', 'sure', 'certain', 'definite', 'positive'],
            'weight': 0.7
        }
    }
    
    # Count emotional words and calculate intensity
    for emotion, data in emotional_keywords.items():
        keywords = data['keywords']
        base_weight = data['weight']
        
        count = sum(1 for keyword in keywords if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower))
        
        if count > 0:
            # Base intensity from keyword count
            intensity = min(0.3 + (count * 0.15), 1.0) * base_weight
            
            # Check for intensity modifiers
            intensifiers = ['very', 'really', 'extremely', 'incredibly', 'absolutely', 'so']
            reducers = ['slightly', 'a bit', 'somewhat', 'mildly', 'little']
            
            for intensifier in intensifiers:
                if re.search(r'\b' + re.escape(intensifier) + r'\b', text_lower):
                    intensity = min(intensity * 1.3, 1.0)
            
            for reducer in reducers:
                if re.search(r'\b' + re.escape(reducer) + r'\b', text_lower):
                    intensity = max(intensity * 0.7, 0.1)
            
            signals[emotion] = round(intensity, 3)
    
    # For very short/compressed text, try to infer emotions from context
    if len(text.split()) <= 3 and not signals:
        if any(word in text_lower for word in ['not working', 'broken', 'error', 'issue']):
            signals['frustration'] = 0.6
        elif any(word in text_lower for word in ['excited', 'thrilled', 'great']):
            signals['excitement'] = 0.6
        elif any(word in text_lower for word in ['concern', 'worry', 'problem']):
            signals['fear'] = 0.6
        elif any(word in text_lower for word in ['happy', 'good', 'nice']):
            signals['joy'] = 0.6
    
    # If no emotions detected, return neutral baseline
    if not signals:
        signals['neutral'] = 0.5
    
    return signals