"""
Integration with ACTUAL DeepAgent memory compression
"""

import sys
import os
import json

# Add DeepAgent source to path
sys.path.append('../src')

def get_actual_deepagent_memory_folding(conversation, question):
    """
    Use DeepAgent's ACTUAL memory folding on our emotional test cases
    """
    try:
        from prompts.prompts_deepagent import (
            get_episode_memory_instruction,
            get_working_memory_instruction, 
            get_tool_memory_instruction
        )
        
        # Convert conversation to reasoning history format
        reasoning_history = format_as_reasoning_history(conversation, question)
        
        # Get their ACTUAL compression prompts
        episodic_prompt = get_episode_memory_instruction(question, reasoning_history)
        working_prompt = get_working_memory_instruction(question, reasoning_history)
        
        print("🔍 DEEPAGENT'S ACTUAL COMPRESSION PROMPTS:")
        print("Episodic Memory Prompt:")
        print(episodic_prompt[:500] + "...")  # First 500 chars
        print("\nWorking Memory Prompt:") 
        print(working_prompt[:500] + "...")
        
        # This is where we'd call their LLM to get compressed memory
        # For now, return their prompt structure analysis
        return {
            'episodic_prompt': episodic_prompt,
            'working_prompt': working_prompt,
            'emotional_filters_detected': analyze_emotional_filters(episodic_prompt, working_prompt)
        }
        
    except ImportError as e:
        print(f"❌ Cannot import DeepAgent: {e}")
        return None

def format_as_reasoning_history(conversation, question):
    """
    Format conversation as DeepAgent's reasoning history
    """
    reasoning_lines = []
    
    for i, utterance in enumerate(conversation):
        if utterance.startswith("User:"):
            reasoning_lines.append(f"User: {utterance[6:]}")
        elif utterance.startswith("Agent:"):
            reasoning_lines.append(f"Assistant: {utterance[7:]}")
        else:
            reasoning_lines.append(utterance)
    
    return "\n".join(reasoning_lines)

def analyze_emotional_filters(episodic_prompt, working_prompt):
    """
    Analyze exactly what emotional content their prompts filter out
    """
    filters = []
    
    # Check episodic memory filters
    if "major milestones" in episodic_prompt and "strategic decisions" in episodic_prompt:
        filters.append("Filters out emotional states - only keeps factual events")
    
    if "subgoal completions" in episodic_prompt:
        filters.append("Filters out emotional reactions to successes/failures")
    
    # Check working memory filters  
    if "ONLY immediate goals" in working_prompt and "current challenges" in working_prompt:
        filters.append("Filters out emotional continuity and historical mood")
    
    if "Ignore completed/historical information" in working_prompt:
        filters.append("Explicitly discards emotional history and rapport building")
    
    # Check for emotional keywords that are MISSING
    emotional_terms = ['emotion', 'feeling', 'sentiment', 'tone', 'mood', 'frustration', 'satisfaction']
    missing_emotional_terms = []
    
    combined_prompts = episodic_prompt + working_prompt
    for term in emotional_terms:
        if term not in combined_prompts.lower():
            missing_emotional_terms.append(term)
    
    if missing_emotional_terms:
        filters.append(f"Never mentions emotional concepts: {', '.join(missing_emotional_terms)}")
    
    return filters

def extract_emotional_content_from_compressed(compressed_output):
    """
    Analyze what emotional content survives DeepAgent's compression
    """
    if not compressed_output:
        return {'emotional_content': 'NONE', 'surviving_emotional_signals': []}
    
    emotional_signals = []
    
    # Check episodic memory
    episodic = compressed_output.get('episodic', {})
    if episodic:
        emotional_in_episodic = search_for_emotional_content(episodic)
        emotional_signals.extend(emotional_in_episodic)
    
    # Check working memory  
    working = compressed_output.get('working', {})
    if working:
        emotional_in_working = search_for_emotional_content(working)
        emotional_signals.extend(emotional_in_working)
    
    if emotional_signals:
        return {
            'emotional_content': 'MINIMAL',
            'surviving_emotional_signals': emotional_signals
        }
    else:
        return {
            'emotional_content': 'NONE', 
            'surviving_emotional_signals': []
        }

def search_for_emotional_content(memory_section):
    """
    Search for any emotional content that accidentally survived compression
    """
    emotional_indicators = []
    
    # Convert to string for searching
    memory_text = json.dumps(memory_section) if isinstance(memory_section, dict) else str(memory_section)
    
    emotional_keywords = {
        'frustration': ['frustrat', 'annoy', 'angry', 'mad'],
        'satisfaction': ['happy', 'satisf', 'good', 'great', 'thank'],
        'urgency': ['urgent', 'immediately', 'asap', 'critical'],
        'confusion': ['confus', 'unsure', 'not sure', 'don\'t know'],
        'pride': ['proud', 'achievement', 'accomplish'],
        'anxiety': ['worr', 'anxious', 'nervous', 'concern']
    }
    
    for emotion, keywords in emotional_keywords.items():
        for keyword in keywords:
            if keyword in memory_text.lower():
                emotional_indicators.append(f"{emotion} (via '{keyword}')")
                break  # Only count once per emotion
    
    return emotional_indicators