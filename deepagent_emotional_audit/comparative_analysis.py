"""
Comparative analysis between emotional loss and task performance
"""

def run_comparative_analysis(loss_results, task_analysis):
    """Run comprehensive comparative analysis"""
    
    # Combine loss and task data
    combined_data = []
    for loss_data, task_data in zip(loss_results, task_analysis):
        combined = {
            **loss_data,
            **task_data
        }
        combined_data.append(combined)
    
    # Calculate overall correlations
    overall_correlation = calculate_overall_correlation(combined_data)
    
    # Identify critical thresholds
    thresholds = identify_critical_thresholds(combined_data)
    
    return {
        'combined_data': combined_data,
        'overall_correlation': overall_correlation,
        'critical_thresholds': thresholds,
        'high_impact_cases': identify_high_impact_cases(combined_data)
    }

def calculate_overall_correlation(combined_data):
    """Calculate overall correlation metrics"""
    emotional_losses = [d['overall_loss'] for d in combined_data]
    task_failures = [1.0 if d['task_success_rate']['task_failure'] else 0.0 for d in combined_data]
    
    # Simple correlation calculation
    if len(emotional_losses) > 1:
        correlation = sum((el - sum(emotional_losses)/len(emotional_losses)) * 
                         (tf - sum(task_failures)/len(task_failures)) 
                         for el, tf in zip(emotional_losses, task_failures)) / len(emotional_losses)
    else:
        correlation = 0
    
    return {
        'emotional_loss_task_failure_correlation': correlation,
        'analysis': "Positive correlation indicates emotional loss contributes to task failure"
    }

def identify_critical_thresholds(combined_data):
    """Identify critical emotional loss thresholds that cause task failure"""
    failure_cases = [d for d in combined_data if d['task_success_rate']['task_failure']]
    
    if failure_cases:
        avg_loss_failure = sum(d['overall_loss'] for d in failure_cases) / len(failure_cases)
        max_loss_failure = max(d['overall_loss'] for d in failure_cases)
        min_loss_failure = min(d['overall_loss'] for d in failure_cases)
    else:
        avg_loss_failure = max_loss_failure = min_loss_failure = 0
    
    return {
        'average_loss_task_failure': avg_loss_failure,
        'max_loss_task_failure': max_loss_failure,
        'min_loss_task_failure': min_loss_failure,
        'critical_threshold': min_loss_failure if failure_cases else 0.5
    }

def identify_high_impact_cases(combined_data):
    """Identify cases where emotional loss had highest impact on tasks"""
    high_impact = []
    
    for data in combined_data:
        impact_score = (data['overall_loss'] * 
                       (1.0 if data['task_success_rate']['task_failure'] else 0.3))
        
        if impact_score > 0.5:  # Threshold for high impact
            high_impact.append({
                'conversation_id': data['conversation_id'],
                'impact_score': impact_score,
                'emotional_loss': data['overall_loss'],
                'task_failure': data['task_success_rate']['task_failure'],
                'critical_dimensions': get_critical_dimensions(data['dimensional_loss'])
            })
    
    return sorted(high_impact, key=lambda x: x['impact_score'], reverse=True)

def get_critical_dimensions(dimensional_loss):
    """Identify which emotional dimensions had the highest loss"""
    return dict(sorted(dimensional_loss.items(), key=lambda x: x[1], reverse=True)[:3])