import argparse
import os
from pathlib import Path
import random
import numpy as np
from generate_config_util import generate_mixture_config

def generate_random_proportions(categories):
    """Generate random proportions using Dirichlet distribution for uniform sampling from simplex."""
    # weights = [random.random() for _ in categories]
#     total = sum(weights)
#     return {cat: weight/total for cat, weight in zip(categories, weights)}

    alpha = np.ones(len(categories))  # All ones for uniform distribution
    weights = np.random.dirichlet(alpha)
    return {cat: weight for cat, weight in zip(categories, weights)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--categories", nargs="+", required=True, help="List of category names")
    parser.add_argument("--template", required=True, help="Path to template YAML file")
    parser.add_argument("--output-dir", required=True, help="Output directory for generated configs") 
    parser.add_argument("--total-files", type=int, required=True, help="Total number of files to sample")
    parser.add_argument("--num-configs", type=int, required=True, help="Number of config files to generate")
    parser.add_argument("--root-data-dir", required=True, help="Root directory containing category subdirectories with data files")
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate multiple config files
    for i in range(args.num_configs):
        # Generate random proportions for categories
        proportions = generate_random_proportions(args.categories)
        
        output_path = output_dir / f"config_{i}.yaml"
        
        config_path = generate_mixture_config(
            category_proportions=proportions,
            root_data_dir=args.root_data_dir,
            total_files=args.total_files,
            template_yaml_path=args.template,
            output_yaml_path=str(output_path)
        )
        print(f"Generated config file {i+1}/{args.num_configs}: {config_path}")