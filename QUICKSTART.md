# Quick Start Guide: Monorepo Integration

This guide helps you quickly get started with the Frappe monorepo integration.

## Prerequisites

- Git with LFS support
- Python 3.x
- Bash shell
- ~4GB free disk space
- Internet connection

## Steps

### 1. Validate Your Setup

First, verify that everything is configured correctly:

```bash
./validate-monorepo-setup.sh
```

Expected output:
```
✓ All tests passed! The monorepo integration setup is valid.
```

### 2. Clone All Repositories

To clone all 182 Frappe repositories:

```bash
./clone-repositories.sh
```

This will:
- Clone all repositories into `cloned-repos/` directory
- Remove `.git` directories from each repo
- Process 10 repos in parallel for speed
- Take approximately 5-10 minutes depending on your connection

### 3. Verify Results

After cloning completes, you can verify:

```bash
ls cloned-repos/ | wc -l    # Should show 182
du -sh cloned-repos/         # Should show ~3.7GB
```

## Directory Structure

After cloning:

```
org-frappe/
├── cloned-repos/           # All 182 cloned repositories (not committed to git)
│   ├── hrms/
│   ├── erpnext/
│   ├── books/
│   └── ... (179 more)
├── github.csv              # List of all repositories
├── clone-repositories.sh   # Clone script
├── validate-monorepo-setup.sh  # Validation script
├── MONOREPO_INTEGRATION.md     # Full documentation
└── README.md               # Main project README
```

## Important Notes

### Not Committed to Git

The `cloned-repos/` directory is **intentionally not committed** to git (it's in `.gitignore`). This keeps the repository lightweight and fast to clone.

### Updating Repositories

To update all cloned repositories to their latest versions:

```bash
rm -rf cloned-repos/
./clone-repositories.sh
```

### Selective Cloning

To clone only specific repositories:

1. Create a custom CSV file with only the repos you want
2. Edit `clone-repositories.sh` to point to your CSV file
3. Run the script

## Troubleshooting

### "Git LFS not found"

Install Git LFS:
```bash
# Ubuntu/Debian
sudo apt-get install git-lfs

# macOS
brew install git-lfs

# Then initialize
git lfs install
```

### "Python not found"

Ensure Python 3 is installed:
```bash
python3 --version
```

### Clone fails for specific repos

Some repositories might be private, archived, or moved. The script will continue cloning others and report which ones failed at the end.

### Disk space issues

The full clone requires ~4GB. Check available space:
```bash
df -h .
```

## Advanced Usage

### Change Parallelism

Edit `PARALLEL_JOBS` in `clone-repositories.sh`:
```bash
PARALLEL_JOBS=5  # Clone 5 at a time instead of 10
```

### Custom Clone Location

Edit `REPO_DIR` in `clone-repositories.sh`:
```bash
REPO_DIR="/path/to/your/directory"
```

## Getting Help

- **Full Documentation**: See [MONOREPO_INTEGRATION.md](MONOREPO_INTEGRATION.md)
- **Frappe Framework**: See [README.md](README.md)
- **Issues**: Open an issue on GitHub

## Next Steps

After cloning, you can:
- Browse the source code of all Frappe projects
- Search across all repositories
- Build custom integrations
- Analyze code patterns and dependencies
- Create unified documentation

For more details, see [MONOREPO_INTEGRATION.md](MONOREPO_INTEGRATION.md).
