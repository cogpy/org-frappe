#!/usr/bin/env python3
"""
Update workspace dependencies in package.json files to use workspace:* protocol.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Set

def find_package_names() -> Dict[str, str]:
    """Find all package names and their paths in the monorepo."""
    packages = {}
    packages_dir = Path("/home/ubuntu/org-frappe/packages")
    
    for package_json in packages_dir.rglob("package.json"):
        try:
            with open(package_json, 'r') as f:
                data = json.load(f)
                if 'name' in data:
                    packages[data['name']] = str(package_json.parent)
        except Exception as e:
            print(f"Error reading {package_json}: {e}")
    
    return packages

def update_package_dependencies(package_json_path: Path, known_packages: Set[str]) -> bool:
    """Update a package.json to use workspace:* for internal dependencies."""
    try:
        with open(package_json_path, 'r') as f:
            data = json.load(f)
        
        updated = False
        
        for dep_type in ['dependencies', 'devDependencies', 'peerDependencies']:
            if dep_type in data:
                for dep_name in data[dep_type]:
                    if dep_name in known_packages:
                        current_version = data[dep_type][dep_name]
                        if not current_version.startswith('workspace:'):
                            data[dep_type][dep_name] = 'workspace:*'
                            updated = True
                            print(f"  Updated {dep_name}: {current_version} -> workspace:*")
        
        if updated:
            with open(package_json_path, 'w') as f:
                json.dump(data, f, indent=2)
                f.write('\n')
        
        return updated
    except Exception as e:
        print(f"Error updating {package_json_path}: {e}")
        return False

def main():
    print("Finding all packages in the monorepo...")
    packages = find_package_names()
    print(f"Found {len(packages)} packages")
    
    print("\nPackages found:")
    for name in sorted(packages.keys()):
        print(f"  - {name}")
    
    print("\nUpdating workspace dependencies...")
    known_package_names = set(packages.keys())
    updated_count = 0
    
    packages_dir = Path("/home/ubuntu/org-frappe/packages")
    for package_json in packages_dir.rglob("package.json"):
        print(f"\nChecking {package_json}...")
        if update_package_dependencies(package_json, known_package_names):
            updated_count += 1
    
    print(f"\nUpdated {updated_count} package.json files")

if __name__ == "__main__":
    main()
