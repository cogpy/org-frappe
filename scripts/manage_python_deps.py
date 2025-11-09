#!/usr/bin/env python3
"""
Python Dependency Management Script for Frappe Monorepo

This script scans all packages for Python dependencies and creates a unified
requirements file for the entire monorepo.
"""

import os
import sys
from pathlib import Path
from collections import defaultdict

def find_requirements_files(packages_dir):
    """Find all requirements.txt and pyproject.toml files in packages."""
    req_files = []
    for root, dirs, files in os.walk(packages_dir):
        if 'requirements.txt' in files:
            req_files.append(Path(root) / 'requirements.txt')
        if 'pyproject.toml' in files:
            req_files.append(Path(root) / 'pyproject.toml')
    return req_files

def parse_requirements(req_file):
    """Parse a requirements.txt file and return list of dependencies."""
    deps = []
    try:
        with open(req_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    deps.append(line)
    except Exception as e:
        print(f"Error parsing {req_file}: {e}")
    return deps

def consolidate_dependencies(req_files):
    """Consolidate all dependencies from multiple files."""
    all_deps = defaultdict(set)
    
    for req_file in req_files:
        if req_file.name == 'requirements.txt':
            deps = parse_requirements(req_file)
            for dep in deps:
                # Extract package name (before any version specifier)
                pkg_name = dep.split('==')[0].split('>=')[0].split('<=')[0].split('~=')[0].strip()
                all_deps[pkg_name].add(dep)
    
    return all_deps

def write_consolidated_requirements(all_deps, output_file):
    """Write consolidated requirements to a file."""
    with open(output_file, 'w') as f:
        f.write("# Consolidated Python Dependencies for Frappe Monorepo\n")
        f.write("# Auto-generated - DO NOT EDIT MANUALLY\n\n")
        
        for pkg_name in sorted(all_deps.keys()):
            versions = all_deps[pkg_name]
            if len(versions) == 1:
                f.write(f"{list(versions)[0]}\n")
            else:
                f.write(f"# Multiple versions found for {pkg_name}:\n")
                for v in versions:
                    f.write(f"#   {v}\n")
                f.write(f"{pkg_name}  # TODO: Resolve version conflict\n")

def main():
    """Main function."""
    repo_root = Path(__file__).parent.parent
    packages_dir = repo_root / 'packages'
    output_file = repo_root / 'requirements-consolidated.txt'
    
    print("Scanning for Python dependencies...")
    req_files = find_requirements_files(packages_dir)
    print(f"Found {len(req_files)} dependency files")
    
    print("Consolidating dependencies...")
    all_deps = consolidate_dependencies(req_files)
    print(f"Found {len(all_deps)} unique packages")
    
    print(f"Writing consolidated requirements to {output_file}")
    write_consolidated_requirements(all_deps, output_file)
    
    print("Done!")

if __name__ == '__main__':
    main()
