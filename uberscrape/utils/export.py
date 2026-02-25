"""Export utilities for different output formats"""

import json
import csv
from pathlib import Path
from typing import List, Dict, Any

def export_results(results: List[Dict[str, Any]], output_path: str):
    """
    Export results to JSON or CSV based on file extension.
    
    Args:
        results: List of extracted data dictionaries
        output_path: Output file path (.json or .csv)
        
    Raises:
        ValueError: If output format is not supported
    """
    path = Path(output_path)
    suffix = path.suffix.lower()
    
    if suffix == '.json':
        _export_json(results, path)
    elif suffix == '.csv':
        _export_csv(results, path)
    else:
        raise ValueError(
            f"Unsupported output format: {suffix}. Use .json or .csv"
        )

def _export_json(results: List[Dict], path: Path):
    """Export to JSON file"""
    with open(path, 'w') as f:
        json.dump(results, f, indent=2, default=str)

def _export_csv(results: List[Dict], path: Path):
    """Export to CSV file"""
    if not results:
        # Create empty CSV
        with open(path, 'w') as f:
            f.write('')
        return
    
    # Get all unique keys from all results
    all_keys = set()
    for result in results:
        all_keys.update(result.keys())
    
    # Remove internal keys
    all_keys.discard('source')
    all_keys.discard('parse_error')
    
    # Sort keys for consistent column order
    fieldnames = sorted(all_keys)
    
    # Write CSV
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        
        for result in results:
            # Flatten complex types to JSON strings
            row = {}
            for key in fieldnames:
                value = result.get(key)
                if isinstance(value, (list, dict)):
                    row[key] = json.dumps(value)
                else:
                    row[key] = value
            
            writer.writerow(row)
