#!/bin/bash
# Create GitHub Actions CI/CD workflow for the monorepo

mkdir -p .github/workflows

cat > .github/workflows/monorepo-ci.yml << 'WORKFLOW_EOF'
name: Monorepo CI/CD

on:
  push:
    branches: [develop, main]
  pull_request:
    branches: [develop, main]

jobs:
  setup:
    runs-on: ubuntu-latest
    outputs:
      affected: ${{ steps.affected.outputs.projects }}
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Setup pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 8
      
      - name: Install dependencies
        run: pnpm install
      
      - name: Determine affected projects
        id: affected
        run: |
          if [ "${{ github.event_name }}" == "pull_request" ]; then
            AFFECTED=$(npx nx show projects --affected --base=origin/${{ github.base_ref }} --head=HEAD --json)
          else
            AFFECTED=$(npx nx show projects --affected --base=HEAD~1 --head=HEAD --json)
          fi
          echo "projects=$AFFECTED" >> $GITHUB_OUTPUT
  
  lint:
    needs: setup
    runs-on: ubuntu-latest
    if: needs.setup.outputs.affected != '[]'
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Setup pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 8
      
      - name: Install dependencies
        run: pnpm install
      
      - name: Lint affected projects
        run: npx nx affected -t lint --parallel=3
  
  test:
    needs: setup
    runs-on: ubuntu-latest
    if: needs.setup.outputs.affected != '[]'
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Setup pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 8
      
      - name: Install dependencies
        run: pnpm install
      
      - name: Test affected projects
        run: npx nx affected -t test --parallel=3
  
  build:
    needs: [lint, test]
    runs-on: ubuntu-latest
    if: needs.setup.outputs.affected != '[]'
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Setup pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 8
      
      - name: Install dependencies
        run: pnpm install
      
      - name: Build affected projects
        run: npx nx affected -t build --parallel=3
WORKFLOW_EOF

echo "Created GitHub Actions workflow at .github/workflows/monorepo-ci.yml"
