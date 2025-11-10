#!/usr/bin/env python3
"""
Script to integrate repositories from cloned-repos into the packages directory
in batches, following the categorization mapping.
"""

import os
import json
import shutil
import subprocess
from pathlib import Path

# Load categorization
with open('/home/ubuntu/repo_categorization.json', 'r') as f:
    mapping = json.load(f)

# Define source and target directories
SOURCE_DIR = Path('/home/ubuntu/org-frappe/cloned-repos')
TARGET_DIR = Path('/home/ubuntu/org-frappe/packages')

def integrate_batch(category, repos, batch_num, total_batches):
    """Integrate a batch of repositories into the monorepo."""
    print(f"\n{'='*60}")
    print(f"Batch {batch_num}/{total_batches}: {category.upper()}")
    print(f"Integrating {len(repos)} repositories")
    print(f"{'='*60}\n")
    
    # Create category directory if it doesn't exist
    category_dir = TARGET_DIR / category
    category_dir.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    for i, repo in enumerate(repos, 1):
        source = SOURCE_DIR / repo
        target = category_dir / repo
        
        if not source.exists():
            print(f"  ✗ [{i}/{len(repos)}] {repo} - SOURCE NOT FOUND")
            continue
        
        if target.exists():
            print(f"  ⚠ [{i}/{len(repos)}] {repo} - already exists, skipping")
            continue
        
        try:
            # Move the repository
            shutil.move(str(source), str(target))
            print(f"  ✓ [{i}/{len(repos)}] {repo} → packages/{category}/")
            success_count += 1
        except Exception as e:
            print(f"  ✗ [{i}/{len(repos)}] {repo} - ERROR: {e}")
    
    print(f"\n  Successfully integrated: {success_count}/{len(repos)}")
    return success_count

def main():
    # Define integration order (layered approach)
    integration_order = [
        'core',
        'infrastructure',
        'tools',
        'libs',
        'apps',
        'integrations',
        'regional',
        'docs',
        'utilities',
        'archive'
    ]
    
    total_integrated = 0
    batch_num = 0
    
    for category in integration_order:
        if category not in mapping['categorization']:
            continue
        
        repos = mapping['categorization'][category]['repositories']
        
        # Process in batches of 10
        for i in range(0, len(repos), 10):
            batch_num += 1
            batch_repos = repos[i:i+10]
            total_batches = sum((len(mapping['categorization'][cat]['repositories']) + 9) // 10 
                              for cat in integration_order 
                              if cat in mapping['categorization'])
            
            count = integrate_batch(category, batch_repos, batch_num, total_batches)
            total_integrated += count
    
    print(f"\n{'='*60}")
    print(f"INTEGRATION COMPLETE")
    print(f"Total repositories integrated: {total_integrated}")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
