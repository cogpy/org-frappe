## Monorepo Integration

This repository has been enhanced to support monorepo integration of 182 Frappe-related repositories.

### Quick Start

To clone all Frappe repositories into this monorepo:

```bash
./clone-repositories.sh
```

This will clone all 182 repositories listed in `github.csv` into the `cloned-repos/` directory, with `.git` directories removed for seamless integration.

### What's Included

- **182 repositories** from the Frappe ecosystem
- Clone script with Git LFS support and parallel processing
- Comprehensive documentation in `MONOREPO_INTEGRATION.md`
- Repository list in `github.csv`

### Why This Approach?

Rather than committing ~3.7GB of code directly to git, we provide tooling to clone repositories on-demand. This keeps the repository lightweight while enabling full monorepo functionality.

### Learn More

See [MONOREPO_INTEGRATION.md](MONOREPO_INTEGRATION.md) for complete documentation on the monorepo integration including:
- Clone script usage
- Customization options
- Repository statistics
- Maintenance procedures

---

