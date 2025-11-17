#!/usr/bin/env python3
"""
Generate Nx project.json configurations for all packages in the monorepo.
"""

import json
import os
from pathlib import Path
from typing import Dict, List

CATEGORY_TAGS = {
    'core': ['scope:core', 'type:framework'],
    'apps': ['scope:apps', 'type:application'],
    'libs': ['scope:libs', 'type:library'],
    'integrations': ['scope:integrations', 'type:integration'],
    'tools': ['scope:tools', 'type:tool'],
    'infrastructure': ['scope:infrastructure', 'type:infra'],
    'docs': ['scope:docs', 'type:documentation'],
    'regional': ['scope:regional', 'type:localization'],
    'archive': ['scope:archive', 'type:legacy'],
    'utilities': ['scope:utilities', 'type:utility']
}

def generate_project_config(package_path: Path, category: str, package_name: str) -> Dict:
    """Generate an Nx project configuration for a package."""
    relative_path = package_path.relative_to('/home/ubuntu/org-frappe')
    
    # Determine if it's a Python or JavaScript project
    has_package_json = (package_path / 'package.json').exists()
    has_pyproject = (package_path / 'pyproject.toml').exists()
    has_setup_py = (package_path / 'setup.py').exists()
    
    targets = {}
    
    if has_package_json:
        # JavaScript/Node.js project
        targets['build'] = {
            'executor': '@nrwl/workspace:run-commands',
            'options': {
                'command': f'cd {relative_path} && npm run build',
                'cwd': str(relative_path)
            }
        }
        targets['test'] = {
            'executor': '@nrwl/workspace:run-commands',
            'options': {
                'command': f'cd {relative_path} && npm test',
                'cwd': str(relative_path)
            }
        }
    
    if has_pyproject or has_setup_py:
        # Python project
        targets['test'] = {
            'executor': '@nrwl/workspace:run-commands',
            'options': {
                'command': f'cd {relative_path} && python -m pytest',
                'cwd': str(relative_path)
            }
        }
        targets['lint'] = {
            'executor': '@nrwl/workspace:run-commands',
            'options': {
                'command': f'cd {relative_path} && python -m ruff check .',
                'cwd': str(relative_path)
            }
        }
    
    config = {
        'name': package_name,
        '$schema': '../../../node_modules/nx/schemas/project-schema.json',
        'sourceRoot': str(relative_path),
        'projectType': 'library' if category in ['libs', 'utilities', 'core'] else 'application',
        'targets': targets,
        'tags': CATEGORY_TAGS.get(category, ['scope:unknown'])
    }
    
    return config

def main():
    packages_dir = Path('/home/ubuntu/org-frappe/packages')
    created_count = 0
    
    for category_dir in packages_dir.iterdir():
        if not category_dir.is_dir():
            continue
        
        category = category_dir.name
        print(f"\nProcessing category: {category}")
        
        for package_dir in category_dir.iterdir():
            if not package_dir.is_dir():
                continue
            
            package_name = package_dir.name
            project_json_path = package_dir / 'project.json'
            
            # Skip if project.json already exists
            if project_json_path.exists():
                print(f"  Skipping {package_name} (project.json already exists)")
                continue
            
            # Generate configuration
            config = generate_project_config(package_dir, category, package_name)
            
            # Write project.json
            with open(project_json_path, 'w') as f:
                json.dump(config, f, indent=2)
                f.write('\n')
            
            print(f"  Created project.json for {package_name}")
            created_count += 1
    
    print(f"\nCreated {created_count} project.json files")

if __name__ == '__main__':
    main()
