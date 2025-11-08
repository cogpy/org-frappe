# Frappe Monorepo Integration

This repository contains the infrastructure to integrate 182 Frappe repositories into a unified monorepo structure.

## Overview

Instead of committing all 182 repositories (approximately 3.7GB) directly into git, we provide a script that clones them on-demand. This approach:

- Keeps the git repository lightweight
- Allows easy updates of individual repositories
- Maintains clean git history
- Enables efficient CI/CD pipelines

## Quick Start

### Validate Setup

Before cloning, verify that the monorepo integration setup is valid:

```bash
chmod +x validate-monorepo-setup.sh
./validate-monorepo-setup.sh
```

This validation script checks:
- CSV file integrity (182 repositories)
- Clone script availability and syntax
- Documentation files
- Git and Python 3 availability
- `.gitignore` configuration

### Clone All Repositories

Run the provided script to clone all 182 repositories:

```bash
chmod +x clone-repositories.sh
./clone-repositories.sh
```

This will:
- Clone all 182 repositories listed in `github.csv`
- Remove `.git` directories from each repository
- Place them in the `cloned-repos/` directory
- Use Git LFS for efficient cloning
- Process 10 repositories in parallel

### Repository List

The `github.csv` file contains the complete list of 182 Frappe repositories to be integrated:

- **Python**: 102 repositories
- **JavaScript**: 28 repositories  
- **HTML**: 14 repositories
- **Vue**: 13 repositories
- **Unknown/Other**: 8 repositories
- **TypeScript**: 6 repositories
- **CSS**: 4 repositories
- **Shell**: 4 repositories
- **Dart**: 1 repository
- **Kotlin**: 1 repository
- **Rust**: 1 repository

### Directory Structure

After running the clone script:

```
.
├── github.csv                  # List of repositories
├── clone-repositories.sh       # Clone script
├── MONOREPO_INTEGRATION.md    # This file
└── cloned-repos/              # Cloned repositories (gitignored)
    ├── hrms/
    ├── books/
    ├── erpnext/
    ├── frappe/
    ├── bench/
    └── ... (177 more)
```

## Integration Details

### Cloning Strategy

- **Depth**: Shallow clone (`--depth 1`) for minimal size
- **Git LFS**: Enabled with `GIT_LFS_SKIP_SMUDGE=1` for efficiency
- **Parallel**: 10 repositories cloned simultaneously
- **No Submodules**: `.git` directories are removed after cloning

### Why Not Commit to Git?

Committing 3.7GB of code would:
- Bloat the git repository significantly
- Make cloning this repo slow
- Create merge conflicts when repositories are updated
- Complicate the git history

Instead, the clone script allows:
- Fast repository cloning
- Easy updates by re-running the script
- Selective cloning if needed
- Clean separation of concerns

## Requirements

- Git with LFS support
- Python 3.x
- Bash shell
- Sufficient disk space (~4GB)
- Internet connection for cloning

## Customization

### Clone Specific Repositories

Edit `github.csv` to include only the repositories you need, then run the clone script.

### Change Clone Location

Modify the `REPO_DIR` variable in `clone-repositories.sh`:

```bash
REPO_DIR="/your/custom/path"
```

### Adjust Parallelism

Change the `PARALLEL_JOBS` variable to control how many repositories are cloned simultaneously:

```bash
PARALLEL_JOBS=5  # Clone 5 at a time instead of 10
```

## Maintenance

### Update Repositories

To update all cloned repositories:

```bash
rm -rf cloned-repos/
./clone-repositories.sh
```

### Add New Repositories

1. Add the repository to `github.csv`
2. Re-run the clone script

## Repository Statistics

- **Total Repositories**: 182
- **Total Size**: ~3.7GB (uncompressed)
- **Primary Language**: Python (56%)
- **Clone Time**: ~5-10 minutes (depending on connection)

## License

Individual repositories maintain their own licenses. Please refer to each repository for license information.

## Contributing

This is an integration repository. For contributing to individual Frappe projects, please visit their respective repositories on GitHub.

## Support

For issues related to:
- **Individual repositories**: Contact the respective repository maintainers
- **This integration**: Open an issue in this repository
