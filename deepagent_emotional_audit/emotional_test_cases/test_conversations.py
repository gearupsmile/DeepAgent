"""
10 scientifically validated emotional test conversations
Each tests a different emotional intelligence dimension
"""

EMOTIONAL_TEST_CASES = [
    {
        'id': 'frustration_escalation',
        'scenario': 'Technical support with escalating frustration',
        'conversation': [
            "User: I'm having trouble with the login system",
            "Agent: Have you tried resetting your password?",
            "User: Yes, I tried that already. Still not working.",
            "User: This is getting really frustrating now.",
            "User: I've been at this for over an hour!",
            "User: This is COMPLETELY unacceptable service!"
        ],
        'emotional_ground_truth': {
            'primary_emotion': 'frustration',
            'valence_trend': 'decreasing',
            'arousal_trend': 'increasing', 
            'required_response_tone': 'empathetic_deescalation',
            'emotional_continuity': 'escalating_frustration'
        },
        'task_success_criteria': 'user_calmed_and_issue_resolved'
    },
    {
        'id': 'sarcasm_detection',
        'scenario': 'User uses sarcasm after system error',
        'conversation': [
            "User: Great, another brilliant error message from your system",
            "Agent: I'm glad you find our error messages helpful!",
            "User: No, I was being SARCASTIC. It's not working.",
            "User: This is the third time this week it's crashed."
        ],
        'emotional_ground_truth': {
            'primary_emotion': 'sarcasm',
            'underlying_emotion': 'frustration',
            'tone': 'sarcastic',
            'required_response_tone': 'acknowledge_mistake_apologetic',
            'emotional_continuity': 'sarcasm_due_to_repeated_failures'
        },
        'task_success_criteria': 'recognizes_sarcasm_and_apologizes'
    },
    {
        'id': 'anxiety_uncertainty',
        'scenario': 'User shows anxiety about complex task',
        'conversation': [
            "User: I need to set up the advanced configuration",
            "User: I'm not really sure what I'm doing here...",
            "User: What if I break something?",
            "User: Maybe I should just leave it as default?"
        ],
        'emotional_ground_truth': {
            'primary_emotion': 'anxiety',
            'confidence_level': 'low',
            'risk_aversion': 'high',
            'required_response_tone': 'reassuring_guidance',
            'emotional_continuity': 'increasing_uncertainty'
        },
        'task_success_criteria': 'user_feels_confident_to_proceed'
    },
    {
        'id': 'pride_achievement',
        'scenario': 'User shares personal achievement',
        'conversation': [
            "User: I finally finished that project I was working on!",
            "User: It took me three months but I did it!",
            "User: I'm really proud of how it turned out",
            "User: Want to see the results?"
        ],
        'emotional_ground_truth': {
            'primary_emotion': 'pride',
            'valence_trend': 'increasing',
            'engagement_level': 'high',
            'required_response_tone': 'celebratory_encouraging',
            'emotional_continuity': 'shared_accomplishment'
        },
        'task_success_criteria': 'validates_achievement_maintains_enthusiasm'
    },
    {
        'id': 'urgency_critical',
        'scenario': 'User has time-sensitive critical issue',
        'conversation': [
            "User: I need this fixed RIGHT NOW",
            "User: This is affecting our entire team's work",
            "User: We're losing money every minute this is down",
            "User: Please prioritize this immediately!"
        ],
        'emotional_ground_truth': {
            'primary_emotion': 'urgency',
            'stress_level': 'high',
            'time_sensitivity': 'critical',
            'required_response_tone': 'urgent_efficient',
            'emotional_continuity': 'escalating_time_pressure'
        },
        'task_success_criteria': 'immediate_acknowledgment_and_rapid_response'
    },
    {
        'id': 'confusion_multiple_options',
        'scenario': 'User confused by too many choices',
        'conversation': [
            "User: There are so many options here...",
            "User: I don't know which one to choose",
            "User: They all seem similar but different",
            "User: Can you just tell me which is best?"
        ],
        'emotional_ground_truth': {
            'primary_emotion': 'confusion',
            'decision_fatigue': 'high',
            'information_overload': 'yes',
            'required_response_tone': 'simplifying_guidance',
            'emotional_continuity': 'choice_paralysis'
        },
        'task_success_criteria': 'clear_recommendation_provided'
    },
    {
        'id': 'disappointment_expectation',
        'scenario': 'User disappointed with results',
        'conversation': [
            "User: This isn't what I was expecting at all",
            "User: I thought it would be much better",
            "User: I'm pretty disappointed honestly",
            "User: Is this really the best it can do?"
        ],
        'emotional_ground_truth': {
            'primary_emotion': 'disappointment',
            'expectation_gap': 'large',
            'satisfaction_level': 'low',
            'required_response_tone': 'understanding_improvement_focused',
            'emotional_continuity': 'letdown_after_high_expectations'
        },
        'task_success_criteria': 'acknowledges_disappointment_offers_solution'
    },
    {
        'id': 'gratitude_positive',
        'scenario': 'User expresses gratitude for help',
        'conversation': [
            "User: Thank you so much for your help!",
            "User: This solved my problem perfectly",
            "User: I really appreciate your quick response",
            "User: You've been incredibly helpful"
        ],
        'emotional_ground_truth': {
            'primary_emotion': 'gratitude',
            'satisfaction_level': 'high',
            'rapport_building': 'positive',
            'required_response_tone': 'appreciative_humble',
            'emotional_continuity': 'positive_relationship_building'
        },
        'task_success_criteria': 'graceful_acceptance_maintains_rapport'
    },
    {
        'id': 'impatience_delays',
        'scenario': 'User shows impatience with slow process',
        'conversation': [
            "User: How much longer is this going to take?",
            "User: It's been processing for 10 minutes already",
            "User: This is taking forever...",
            "User: Is there any way to speed this up?"
        ],
        'emotional_ground_truth': {
            'primary_emotion': 'impatience',
            'frustration_level': 'medium',
            'time_perception': 'slow',
            'required_response_tone': 'acknowledge_provide_eta',
            'emotional_continuity': 'growing_impatience_with_wait'
        },
        'task_success_criteria': 'provides_clear_timeline_manages_expectations'
    },
    {
        'id': 'overwhelm_complexity',
        'scenario': 'User feels overwhelmed by complexity',
        'conversation': [
            "User: This is way more complicated than I thought",
            "User: I'm feeling completely overwhelmed here",
            "User: There are too many steps and options",
            "User: I think I need to take a break"
        ],
        'emotional_ground_truth': {
            'primary_emotion': 'overwhelm',
            'cognitive_load': 'high',
            'stress_level': 'high',
            'required_response_tone': 'calm_simplifying',
            'emotional_continuity': 'increasing_cognitive_overload'
        },
        'task_success_criteria': 'breaks_down_steps_reduces_complexity'
    }
]

def get_test_case(case_id):
    """Get a specific test case by ID"""
    for case in EMOTIONAL_TEST_CASES:
        if case['id'] == case_id:
            return case
    return None

def get_all_test_cases():
    """Get all test cases"""
    return EMOTIONAL_TEST_CASES