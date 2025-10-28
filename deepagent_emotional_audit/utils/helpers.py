"""
Utility helper functions for DeepAgent Emotional Audit
"""

import json
import os
import numpy as np
from datetime import datetime
import logging

def setup_logging():
    """Setup basic logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('emotional_audit.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def save_results(data, filename, output_dir='results'):
    """
    Save results to JSON file
    """
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Add timestamp to data
        if isinstance(data, dict):
            data['_metadata'] = {
                'timestamp': datetime.now().isoformat(),
                'filename': filename
            }
        
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger = setup_logging()
        logger.info(f"Results saved to: {filepath}")
        return True
        
    except Exception as e:
        logger = setup_logging()
        logger.error(f"Error saving results to {filename}: {e}")
        return False

def load_results(filename, output_dir='results'):
    """
    Load results from JSON file
    """
    try:
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger = setup_logging()
        logger.info(f"Results loaded from: {filepath}")
        return data
        
    except Exception as e:
        logger = setup_logging()
        logger.error(f"Error loading results from {filename}: {e}")
        return None

def load_config(config_file='config.json'):
    """
    Load configuration from JSON file
    """
    default_config = {
        'emotional_dimensions': ['joy', 'sadness', 'anger', 'fear', 'surprise', 'trust', 'anticipation'],
        'loss_thresholds': {
            'low': 0.2,
            'medium': 0.5,
            'high': 0.8
        },
        'task_success_metrics': {
            'completion_rate': 0.7,
            'user_satisfaction': 0.6
        },
        'analysis_settings': {
            'correlation_method': 'pearson',
            'significance_level': 0.05,
            'bootstrap_iterations': 1000
        }
    }
    
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                user_config = json.load(f)
                # Merge with default config
                default_config.update(user_config)
        
        return default_config
        
    except Exception as e:
        logger = setup_logging()
        logger.warning(f"Could not load config file {config_file}, using defaults: {e}")
        return default_config

def calculate_correlation(x_values, y_values):
    """
    Calculate correlation between two sets of values
    """
    try:
        if len(x_values) != len(y_values):
            raise ValueError("Input arrays must have the same length")
        
        if len(x_values) < 2:
            return 0.0
        
        x = np.array(x_values)
        y = np.array(y_values)
        
        # Pearson correlation
        correlation = np.corrcoef(x, y)[0, 1]
        
        # Handle NaN values
        if np.isnan(correlation):
            return 0.0
            
        return float(correlation)
        
    except Exception as e:
        logger = setup_logging()
        logger.error(f"Error calculating correlation: {e}")
        return 0.0

def normalize_scores(scores, method='minmax'):
    """
    Normalize scores to 0-1 range
    """
    try:
        if not scores:
            return []
        
        scores_array = np.array(scores)
        
        if method == 'minmax':
            if np.max(scores_array) == np.min(scores_array):
                return [0.5] * len(scores)  # All same values
            normalized = (scores_array - np.min(scores_array)) / (np.max(scores_array) - np.min(scores_array))
        elif method == 'zscore':
            if np.std(scores_array) == 0:
                return [0.5] * len(scores)  # All same values
            normalized = (scores_array - np.mean(scores_array)) / np.std(scores_array)
            # Scale to 0-1
            normalized = (normalized - np.min(normalized)) / (np.max(normalized) - np.min(normalized))
        else:
            normalized = scores_array
        
        return normalized.tolist()
        
    except Exception as e:
        logger = setup_logging()
        logger.error(f"Error normalizing scores: {e}")
        return scores

def format_results_table(results, max_width=80):
    """
    Format results as a readable table
    """
    if not results:
        return "No results to display"
    
    try:
        # Determine column widths
        headers = list(results[0].keys())
        col_widths = {}
        
        for header in headers:
            max_len = len(header)
            for result in results:
                value = str(result.get(header, ''))
                max_len = max(max_len, len(value))
            col_widths[header] = min(max_len + 2, 30)  # Cap width
        
        # Create header
        table = []
        header_line = " | ".join(header.ljust(col_widths[header]) for header in headers)
        separator = "-+-".join('-' * col_widths[header] for header in headers)
        
        table.append(header_line)
        table.append(separator)
        
        # Add rows
        for result in results:
            row = " | ".join(str(result.get(header, '')).ljust(col_widths[header]) for header in headers)
            table.append(row)
        
        return "\n".join(table)
        
    except Exception as e:
        logger = setup_logging()
        logger.error(f"Error formatting table: {e}")
        return str(results)

def export_to_csv(data, filename, output_dir='results'):
    """
    Export data to CSV format
    """
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        filepath = os.path.join(output_dir, filename)
        
        if isinstance(data, list) and len(data) > 0:
            import csv
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        elif isinstance(data, dict):
            # Convert dict to list of dicts for CSV
            rows = []
            for key, value in data.items():
                if isinstance(value, dict):
                    row = {'key': key, **value}
                else:
                    row = {'key': key, 'value': value}
                rows.append(row)
            
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
        
        logger = setup_logging()
        logger.info(f"Data exported to CSV: {filepath}")
        return True
        
    except Exception as e:
        logger = setup_logging()
        logger.error(f"Error exporting to CSV {filename}: {e}")
        return False

def get_timestamp():
    """
    Get current timestamp in readable format
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def validate_emotional_signals(signals):
    """
    Validate emotional signals dictionary
    """
    if not isinstance(signals, dict):
        return False
    
    valid_dimensions = ['joy', 'sadness', 'anger', 'fear', 'surprise', 'trust', 'anticipation', 
                       'excitement', 'frustration', 'satisfaction', 'confusion', 'confidence']
    
    for dimension, value in signals.items():
        if dimension not in valid_dimensions:
            return False
        if not isinstance(value, (int, float)) or value < 0 or value > 1:
            return False
    
    return True

# Initialize logging when module is imported
logger = setup_logging()