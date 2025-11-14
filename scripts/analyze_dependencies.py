#!/usr/bin/env python3
"""
Dependency Analysis Script for Frappe Monorepo
Analyzes package.json and setup.py files to create a dependency graph
"""

import os
import json
import sys
from pathlib import Path
from collections import defaultdict

def find_package_files(packages_dir):
    """Find all package.json and setup.py files in the packages directory"""
    package_files = []
    
    for root, dirs, files in os.walk(packages_dir):
        if 'package.json' in files:
            package_files.append(os.path.join(root, 'package.json'))
        if 'setup.py' in files:
            package_files.append(os.path.join(root, 'setup.py'))
    
    return package_files

def analyze_package_json(filepath):
    """Extract dependencies from package.json"""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            
        package_name = data.get('name', os.path.basename(os.path.dirname(filepath)))
        dependencies = {}
        
        if 'dependencies' in data:
            dependencies.update(data['dependencies'])
        if 'devDependencies' in data:
            dependencies.update(data['devDependencies'])
        
        return {
            'name': package_name,
            'type': 'node',
            'path': filepath,
            'dependencies': dependencies
        }
    except Exception as e:
        print(f"Error analyzing {filepath}: {e}", file=sys.stderr)
        return None

def analyze_setup_py(filepath):
    """Extract basic info from setup.py"""
    try:
        package_name = os.path.basename(os.path.dirname(filepath))
        
        return {
            'name': package_name,
            'type': 'python',
            'path': filepath,
            'dependencies': {}
        }
    except Exception as e:
        print(f"Error analyzing {filepath}: {e}", file=sys.stderr)
        return None

def create_dependency_graph(packages_dir):
    """Create a dependency graph of all packages"""
    package_files = find_package_files(packages_dir)
    packages = []
    
    for filepath in package_files:
        if filepath.endswith('package.json'):
            pkg = analyze_package_json(filepath)
        elif filepath.endswith('setup.py'):
            pkg = analyze_setup_py(filepath)
        else:
            continue
        
        if pkg:
            packages.append(pkg)
    
    return packages

def generate_report(packages, output_file):
    """Generate a dependency report"""
    with open(output_file, 'w') as f:
        f.write("# Frappe Monorepo Dependency Analysis\n\n")
        
        # Count by type
        node_packages = [p for p in packages if p['type'] == 'node']
        python_packages = [p for p in packages if p['type'] == 'python']
        
        f.write(f"## Summary\n\n")
        f.write(f"- Total packages: {len(packages)}\n")
        f.write(f"- Node.js packages: {len(node_packages)}\n")
        f.write(f"- Python packages: {len(python_packages)}\n\n")
        
        # List all packages by category
        categories = defaultdict(list)
        for pkg in packages:
            path_parts = Path(pkg['path']).parts
            if 'packages' in path_parts:
                idx = path_parts.index('packages')
                if idx + 1 < len(path_parts):
                    category = path_parts[idx + 1]
                    categories[category].append(pkg['name'])
        
        f.write("## Packages by Category\n\n")
        for category, pkgs in sorted(categories.items()):
            f.write(f"### {category.title()} ({len(pkgs)} packages)\n\n")
            for pkg_name in sorted(pkgs):
                f.write(f"- {pkg_name}\n")
            f.write("\n")

def main():
    repo_root = Path(__file__).parent.parent
    packages_dir = repo_root / 'packages'
    output_file = repo_root / 'DEPENDENCY_ANALYSIS.md'
    
    print(f"Analyzing packages in {packages_dir}...")
    packages = create_dependency_graph(packages_dir)
    
    print(f"Found {len(packages)} packages")
    print(f"Generating report to {output_file}...")
    generate_report(packages, output_file)
    
    print("Analysis complete!")

if __name__ == '__main__':
    main()
