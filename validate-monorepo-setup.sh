#!/bin/bash
# Validation script to verify the monorepo integration setup

set -eo pipefail

echo "============================================"
echo "Monorepo Integration Setup Validation"
echo "============================================"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CSV_FILE="$SCRIPT_DIR/github.csv"
CLONE_SCRIPT="$SCRIPT_DIR/clone-repositories.sh"
DOC_FILE="$SCRIPT_DIR/MONOREPO_INTEGRATION.md"

passed=0
failed=0

# Test 1: Check if CSV file exists and is valid
echo "Test 1: Checking github.csv..."
if [ -f "$CSV_FILE" ]; then
    repo_count=$(python3 << EOF
import csv
with open('$CSV_FILE', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    count = sum(1 for row in reader if len(row) >= 2)
    print(count)
EOF
)
    if [ "$repo_count" -gt 0 ]; then
        echo "  ✓ CSV file exists with $repo_count repositories"
        passed=$((passed + 1))
    else
        echo "  ✗ CSV file is empty or invalid"
        failed=$((failed + 1))
    fi
else
    echo "  ✗ CSV file not found"
    failed=$((failed + 1))
fi

# Test 2: Check if clone script exists and is executable
echo "Test 2: Checking clone-repositories.sh..."
if [ -f "$CLONE_SCRIPT" ]; then
    if [ -x "$CLONE_SCRIPT" ]; then
        if bash -n "$CLONE_SCRIPT" 2>/dev/null; then
            echo "  ✓ Clone script exists and is executable"
            passed=$((passed + 1))
        else
            echo "  ✗ Clone script has syntax errors"
            failed=$((failed + 1))
        fi
    else
        echo "  ✗ Clone script is not executable"
        failed=$((failed + 1))
    fi
else
    echo "  ✗ Clone script not found"
    failed=$((failed + 1))
fi

# Test 3: Check if documentation exists
echo "Test 3: Checking MONOREPO_INTEGRATION.md..."
if [ -f "$DOC_FILE" ]; then
    echo "  ✓ Documentation file exists"
    passed=$((passed + 1))
else
    echo "  ✗ Documentation file not found"
    failed=$((failed + 1))
fi

# Test 4: Check if .gitignore excludes cloned-repos
echo "Test 4: Checking .gitignore configuration..."
if grep -q "^cloned-repos/" "$SCRIPT_DIR/.gitignore" 2>/dev/null; then
    echo "  ✓ .gitignore properly excludes cloned-repos/"
    passed=$((passed + 1))
else
    echo "  ✗ .gitignore does not exclude cloned-repos/"
    failed=$((failed + 1))
fi

# Test 5: Check if Python 3 is available
echo "Test 5: Checking Python 3 availability..."
if command -v python3 >/dev/null 2>&1; then
    py_version=$(python3 --version)
    echo "  ✓ Python 3 is available ($py_version)"
    passed=$((passed + 1))
else
    echo "  ✗ Python 3 is not available"
    failed=$((failed + 1))
fi

# Test 6: Check if Git is available
echo "Test 6: Checking Git availability..."
if command -v git >/dev/null 2>&1; then
    git_version=$(git --version)
    echo "  ✓ Git is available ($git_version)"
    passed=$((passed + 1))
else
    echo "  ✗ Git is not available"
    failed=$((failed + 1))
fi

# Summary
echo ""
echo "============================================"
echo "Validation Summary"
echo "============================================"
echo "Passed: $passed"
echo "Failed: $failed"
echo ""

if [ $failed -eq 0 ]; then
    echo "✓ All tests passed! The monorepo integration setup is valid."
    echo ""
    echo "To clone all 182 repositories, run:"
    echo "  ./clone-repositories.sh"
    exit 0
else
    echo "✗ Some tests failed. Please fix the issues above."
    exit 1
fi
