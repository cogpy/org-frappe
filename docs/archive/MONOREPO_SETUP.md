## Monorepo Integration

This repository has been enhanced to support monorepo integration of 182 Frappe-related repositories.

### Quick Start

See [QUICKSTART.md](QUICKSTART.md) for a step-by-step guide, or run:

```bash
# Validate setup
./validate-monorepo-setup.sh

# Clone all 182 repositories
./clone-repositories.sh
```

This will clone all 182 repositories listed in `github.csv` into the `cloned-repos/` directory, with `.git` directories removed for seamless integration.

### What's Included

- **182 repositories** from the Frappe ecosystem
- Clone script with Git LFS support and parallel processing
- Validation script to verify setup
- Comprehensive documentation:
  - [QUICKSTART.md](QUICKSTART.md) - Quick start guide
  - [MONOREPO_INTEGRATION.md](MONOREPO_INTEGRATION.md) - Full documentation
- Repository list in `github.csv`

### Why This Approach?

Rather than committing ~3.7GB of code directly to git, we provide tooling to clone repositories on-demand. This keeps the repository lightweight while enabling full monorepo functionality.

### Learn More

- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **Full Documentation**: [MONOREPO_INTEGRATION.md](MONOREPO_INTEGRATION.md)
- **Validation**: Run `./validate-monorepo-setup.sh`

---

