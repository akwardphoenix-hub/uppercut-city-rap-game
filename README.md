# uppercut-city-rap-game
Legendary Rap Battle 🥊

## Offline Dev / Tests
- This repo is configured for **offline-first** development.
- All data loads from `/public/data/*.json`.
- To run:
  - `npm ci`
  - `npx playwright install chromium`
  - `npm run build && npm run test:e2e`

If you see firewall blocks (esm.ubuntu.com, api.github.com), that's expected in agent sandboxes.

## Build & Test Commands

- **Install dependencies**: `npm ci`
- **Typecheck**: `npm run typecheck`
- **Lint**: `npm run lint`
- **Build**: `npm run build`
- **Dev server**: `npm run dev`
- **Preview (for E2E)**: `npm run preview` (http://localhost:4173)
- **E2E tests**: `npm run test:e2e`
- **E2E UI mode**: `npm run test:e2e:ui`
- **Test report**: `npm run test:report`
- **Pre-publish check**: `npm run prepublish-check`

## Important: Frozen Documentation

⚠️ **Documentation files in this repository are frozen as source of truth and should NOT be auto-regenerated during CI runs.** This prevents infinite loops and ensures stable builds.

**CI Stability Rules:**
1. CI must never leave the repo dirty (`git status` must be clean after build/test)
2. Pre-publish script only lints, builds, and runs tests - no regeneration
3. Documentation should only be updated manually by maintainers, never auto-regenerated in CI
4. Do NOT add `.github/copilot-setup.yml` or `copilot-setup-steps.yml` files

Frozen files include:
- `README.md`, `SETUP.md`, `IMPLEMENTATION_SUMMARY.md`, `NETWORK_BLOCKING_FIXES.md`
- `.github/copilot-instructions.md` and `.github/instructions/*.md`
- Configuration files: `scripts/pre-publish-check.sh`

See `.frozen-docs` for the complete list. Manual documentation updates should be done through pull requests only.

## Architecture

**Project**: Masternode Council / Harmonizer / Uppercut City  
**Stack**: Vite + React + TypeScript + Tailwind + Playwright E2E  
**Policy**: No external network during tests. Use local fixtures/mocks only.

### Key Directories

- `/src/lib/` - Configuration and utilities
- `/src/services/` - Data layer (all network calls)
- `/src/components/` - React components
- `/public/data/` - Local JSON fixtures
- `/e2e/` - Playwright E2E tests
- `/.github/instructions/` - Copilot coding guidelines

### Conventions

- TypeScript strict mode enabled
- Functional React components with explicit props
- All UI accessible by default (roles, labels)
- Audit trail for every action
- Harmonic Math: never return raw NaN/∞
