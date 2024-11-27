import yaml
from pathlib import Path
import random
from datetime import datetime
import os
import shutil

def generate_mixture_config(category_proportions: dict, 
                          root_data_dir: str,
                          total_files: int,
                          template_yaml_path: str,
                          output_yaml_path: str = None) -> str:
    """
    Generate a new config file with randomly selected data files based on category proportions.
    
    Args:
        category_proportions: Dict mapping category names to their proportions (should sum to 1.0)
        root_data_dir: Root directory containing category subdirectories with data files
        total_files: Total number of files to select across all categories
        template_yaml_path: Path to template YAML config file
        output_yaml_path: Path to save the generated config file (optional)
    
    Returns:
        str: Path to the generated config file
    """
    # Validate proportions sum to 1.0 (with small floating point tolerance)
    if not 0.99 <= sum(category_proportions.values()) <= 1.01:
        raise ValueError("Category proportions must sum to 1.0")
    
    # Calculate number of files per category
    category_files = {
        category: int(prop * total_files)
        for category, prop in category_proportions.items()
    }
    
    # Adjust for rounding errors to ensure exact total
    diff = total_files - sum(category_files.values())
    if diff != 0:
        # Add/subtract the difference from the largest category
        largest_category = max(category_proportions.items(), key=lambda x: x[1])[0]
        category_files[largest_category] += diff

    # Select files for each category
    selected_files = []
    for category, num_files in category_files.items():
        category_path = Path(root_data_dir) / category
        if not category_path.exists():
            raise ValueError(f"Category directory not found: {category_path}")
            
        # Get all .npy files in category directory
        available_files = list(category_path.glob("*.npy"))
        if len(available_files) < num_files:
            raise ValueError(f"Not enough files in {category}. Required: {num_files}, Available: {len(available_files)}")
            
        # Randomly select files
        selected = random.sample(available_files, num_files)
        selected_files.extend(selected)

    # Load template YAML
    with open(template_yaml_path, 'r') as f:
        config = yaml.safe_load(f)

    # Update data paths
    config['data']['paths'] = [str(f) for f in selected_files]

    # Generate new run name with weights and timestamp
    weights_str = '-'.join(f"{cat}{prop:.2f}" for cat, prop in category_proportions.items())
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_run_name = f"{config.get('run_name', 'run')}_{weights_str}_{timestamp}"
    config['run_name'] = new_run_name

    # Create output path
    if output_yaml_path is None:
        template_path = Path(template_yaml_path)
        output_path = template_path.parent / f"{template_path.stem}_{timestamp}.yaml"
    else:
        output_path = Path(output_yaml_path)
    
    # Write new config
    with open(output_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)

    return str(output_path)

# Example usage:

