"""Schema loading and validation"""

import json
from pathlib import Path
from typing import Dict

def load_schema(schema_path: str) -> Dict[str, str]:
    """
    Load a JSON schema file.
    
    Args:
        schema_path: Path to schema JSON file
        
    Returns:
        Dictionary mapping field names to types
        
    Raises:
        FileNotFoundError: If schema file doesn't exist
        json.JSONDecodeError: If schema is invalid JSON
        ValueError: If schema format is invalid
    """
    path = Path(schema_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    
    with open(path, 'r') as f:
        schema = json.load(f)
    
    if not isinstance(schema, dict):
        raise ValueError("Schema must be a JSON object (dictionary)")
    
    # Validate that all values are type strings
    valid_types = {'string', 'number', 'boolean', 'array', 'object'}
    for field, type_name in schema.items():
        if type_name not in valid_types:
            raise ValueError(
                f"Invalid type '{type_name}' for field '{field}'. "
                f"Must be one of: {', '.join(valid_types)}"
            )
    
    return schema
