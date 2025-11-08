#!/bin/bash
# Script to clone all 182 Frappe repositories into the monorepo
# This script clones repositories with Git LFS enabled and removes .git directories

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/cloned-repos"
CSV_FILE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/github.csv"
PARALLEL_JOBS=10

echo "============================================"
echo "Frappe Monorepo - Repository Clone Script"
echo "============================================"
echo ""

# Check if CSV file exists
if [ ! -f "$CSV_FILE" ]; then
    echo "Error: github.csv not found!"
    exit 1
fi

# Create directory for cloned repos
mkdir -p "$REPO_DIR"

# Initialize Git LFS
echo "Initializing Git LFS..."
git lfs install 2>&1 | head -1
echo ""

# Extract repository list from CSV
python3 << EOF > /tmp/repos_list.txt
import csv
import sys

csv_file = '$CSV_FILE'

try:
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            if len(row) >= 2:
                print(f"{row[0]}\t{row[1]}")
except Exception as e:
    print(f"Error reading CSV: {e}", file=sys.stderr)
    sys.exit(1)
EOF

total_repos=$(wc -l < /tmp/repos_list.txt)
echo "Found $total_repos repositories to clone"
echo "Cloning $PARALLEL_JOBS repositories at a time..."
echo ""

# Function to clone a single repository
clone_repo() {
    local url="$1"
    local name="$2"
    local count="$3"
    local total="$4"
    local target_dir="$5/$name"
    
    if GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 "$url" "$target_dir" > /dev/null 2>&1; then
        rm -rf "$target_dir/.git"
        echo "✓ [$count/$total] $name"
        return 0
    else
        echo "✗ [$count/$total] $name (failed)"
        return 1
    fi
}

export -f clone_repo
export REPO_DIR

# Clone repositories in parallel
count=0

while IFS=$'\t' read -r url name; do
    count=$((count + 1))
    
    # Run clone in background
    clone_repo "$url" "$name" "$count" "$total_repos" "$REPO_DIR" &
    
    # Wait after every batch
    if [ $((count % PARALLEL_JOBS)) -eq 0 ]; then
        wait
    fi
done < /tmp/repos_list.txt

# Wait for remaining jobs
wait

echo ""
echo "============================================"
echo "Cloning Complete!"
echo "============================================"
echo "Total repositories: $total_repos"
echo "Location: $REPO_DIR"
echo ""

# Calculate total size and count successful clones
if [ -d "$REPO_DIR" ]; then
    total_size=$(du -sh "$REPO_DIR" | cut -f1)
    cloned_count=$(find "$REPO_DIR" -mindepth 1 -maxdepth 1 -type d | wc -l)
    echo "Successfully cloned: $cloned_count repositories"
    echo "Total size: $total_size"
fi

# Cleanup
rm -f /tmp/repos_list.txt

echo ""
echo "All repositories have been cloned without .git directories."
echo "They are ready to be integrated into the monorepo."
