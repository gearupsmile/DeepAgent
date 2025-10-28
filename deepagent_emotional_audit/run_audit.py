#!/usr/bin/env python3
"""
DeepAgent Emotional Audit Runner
Integrates Day 2 (Baseline Analysis) and Day 3 (Task Impact Analysis)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from emotional_metrics.loss_calculation import calculate_emotional_loss
from emotional_metrics.signal_extraction import extract_emotional_signals
from emotional_test_cases.test_conversations import load_test_conversations
from comparative_analysis import run_comparative_analysis
from utils.helpers import save_results, load_config

def run_baseline_analysis():
    """Day 2: Run Baseline Analysis"""
    print("=== Day 2: Running Baseline Analysis ===")
    
    # Load test conversations
    conversations = load_test_conversations()
    print(f"Loaded {len(conversations)} test conversations")
    
    # Process through DeepAgent's memory compression
    loss_results = []
    for conv in conversations:
        original_signals = extract_emotional_signals(conv['original'])
        compressed_signals = extract_emotional_signals(conv['compressed'])
        
        loss_metrics = calculate_emotional_loss(original_signals, compressed_signals)
        loss_metrics['conversation_id'] = conv['id']
        loss_results.append(loss_metrics)
    
    # Generate initial loss matrix
    loss_matrix = create_loss_matrix(loss_results)
    save_results(loss_matrix, 'baseline_loss_matrix.json')
    
    print("Baseline analysis completed")
    return loss_results

def run_task_impact_analysis(loss_results):
    """Day 3: Task Impact Analysis"""
    print("\n=== Day 3: Running Task Impact Analysis ===")
    
    conversations = load_test_conversations()
    
    # Define task success metrics and calculate correlations
    task_analysis = []
    for loss_data in loss_results:
        conv_id = loss_data['conversation_id']
        conversation = next(c for c in conversations if c['id'] == conv_id)
        
        # Calculate task success metrics
        task_success = calculate_task_success(conversation)
        
        # Correlate emotional loss with task failure
        correlation_data = {
            'conversation_id': conv_id,
            'task_success_rate': task_success,
            'emotional_loss': loss_data['overall_loss'],
            'dimensional_loss': loss_data['dimensional_loss'],
            'correlation': calculate_correlation(loss_data, task_success)
        }
        task_analysis.append(correlation_data)
    
    # Identify which emotional dimensions matter most
    dimension_impact = analyze_dimension_impact(task_analysis)
    
    print("Task impact analysis completed")
    return task_analysis, dimension_impact

def calculate_task_success(conversation):
    """Calculate task success metrics for each conversation"""
    original_task_outcome = analyze_task_outcome(conversation['original'], conversation['task_type'])
    compressed_task_outcome = analyze_task_outcome(conversation['compressed'], conversation['task_type'])
    
    # Determine if task failed due to compression
    task_failure = (
        original_task_outcome['success'] is True and 
        compressed_task_outcome['success'] is False
    )
    
    return {
        'original_success': original_task_outcome['success'],
        'compressed_success': compressed_task_outcome['success'],
        'success_rate': compressed_task_outcome['success_rate'],
        'task_failure': task_failure,
        'task_type': conversation['task_type']
    }

def analyze_task_outcome(conversation_text, task_type):
    """Analyze task outcome from conversation text with task-specific criteria"""
    text_lower = conversation_text.lower()
    
    # Task-specific success indicators
    task_indicators = {
        'customer_support': {
            'success': ['fixed', 'resolved', 'working', 'thank you', 'grateful', 'helpful', 'solved', 'great', 'perfect'],
            'failure': ['not working', 'broken', 'frustrated', 'angry', 'useless', 'waste', 'cancel', 'unsubscribe', 'horrible']
        },
        'project_planning': {
            'success': ['agreed', 'timeline', 'deadline', 'confident', 'excited', 'motivated', 'plan', 'ready', 'approved'],
            'failure': ['delay', 'behind', 'concerned', 'worried', 'unsure', 'problem', 'issue', 'uncertain', 'risk']
        },
        'negotiation': {
            'success': ['agreement', 'middle ground', 'compromise', 'deal', 'settled', 'acceptable', 'agreed', 'partnership'],
            'failure': ['stuck', 'disagreement', 'walk away', 'unacceptable', 'reject', 'conflict', 'dispute', 'deadlock']
        },
        'brainstorming': {
            'success': ['creative', 'excited', 'amazing', 'innovative', 'breakthrough', 'energy', 'great', 'wonderful', 'perfect'],
            'failure': ['stuck', 'blocked', 'uninspired', 'frustrated', 'confused', 'nothing', 'empty', 'blank']
        }
    }
    
    indicators = task_indicators.get(task_type, {'success': [], 'failure': []})
    
    success_words = [word for word in indicators['success'] if word in text_lower]
    failure_words = [word for word in indicators['failure'] if word in text_lower]
    
    success_count = len(success_words)
    failure_count = len(failure_words)
    
    if success_count > failure_count:
        success_rate = min(0.5 + (success_count * 0.1), 1.0)
        return {'success': True, 'success_rate': success_rate}
    elif failure_count > success_count:
        success_rate = max(0.1 - (failure_count * 0.1), 0.0)
        return {'success': False, 'success_rate': success_rate}
    else:
        # If equal or no clear indicators, use emotional tone
        if any(word in text_lower for word in ['frustrated', 'angry', 'worried', 'concerned']):
            return {'success': False, 'success_rate': 0.3}
        elif any(word in text_lower for word in ['excited', 'happy', 'confident', 'great']):
            return {'success': True, 'success_rate': 0.7}
        else:
            return {'success': None, 'success_rate': 0.5}

def calculate_correlation(loss_data, task_success):
    """Calculate correlation between emotional loss and task failure"""
    emotional_loss = loss_data['overall_loss']
    task_failure = 1.0 if task_success['task_failure'] else 0.0
    
    # Simple correlation calculation
    # In practice, you might use scipy.stats or numpy for more sophisticated analysis
    return abs(emotional_loss * task_failure)

def analyze_dimension_impact(task_analysis):
    """Identify which emotional dimensions matter most for task success"""
    dimension_impacts = {}
    
    for analysis in task_analysis:
        dimensional_loss = analysis.get('dimensional_loss', {})
        task_failure = analysis.get('task_success_rate', {}).get('task_failure', False)
        
        for dimension, loss in dimensional_loss.items():
            if dimension not in dimension_impacts:
                dimension_impacts[dimension] = []
            
            # Calculate impact: loss multiplied by task failure (1.0 if failed, 0.0 if succeeded)
            impact = loss * (1.0 if task_failure else 0.0)
            dimension_impacts[dimension].append(impact)
    
    # Calculate average impact per dimension (only for dimensions with data)
    dimension_impact_scores = {}
    for dim, impacts in dimension_impacts.items():
        if impacts:  # Only calculate if we have data
            avg_impact = sum(impacts) / len(impacts)
            dimension_impact_scores[dim] = avg_impact
    
    # Return sorted by impact, but ensure we always return a dict
    return dict(sorted(dimension_impact_scores.items(), key=lambda x: x[1], reverse=True))

def create_loss_matrix(loss_results):
    """Generate initial loss matrix from baseline analysis"""
    matrix = {}
    for result in loss_results:
        matrix[result['conversation_id']] = {
            'overall_loss': result['overall_loss'],
            'dimensional_loss': result['dimensional_loss'],
            'signal_preservation': result.get('signal_preservation', {})
        }
    return matrix

def main():
    """Main execution function"""
    print("Starting DeepAgent Emotional Audit...")
    
    # Day 2: Baseline Analysis
    loss_results = run_baseline_analysis()
    
    # Day 3: Task Impact Analysis  
    task_analysis, dimension_impact = run_task_impact_analysis(loss_results)
    
    # Run comparative analysis
    comparative_results = run_comparative_analysis(loss_results, task_analysis)
    
    # Save final results
    final_results = {
        'baseline_analysis': loss_results,
        'task_impact_analysis': task_analysis,
        'dimension_impact': dimension_impact,
        'comparative_analysis': comparative_results
    }
    
    save_results(final_results, 'emotional_audit_results.json')
    
    print("\n=== Emotional Audit Complete ===")
    print(f"Processed {len(loss_results)} conversations")
    
    # FIX: Handle empty dimension_impact
    if dimension_impact:
        print(f"Most impactful dimension: {list(dimension_impact.keys())[0]}")
    else:
        print("Most impactful dimension: None detected")
    
    return final_results

if __name__ == "__main__":
    main()