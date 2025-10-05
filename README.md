# uppercut-city-rap-game
Legendary Rap Battle 🥊

## Offline Dev / Tests
- This repo is configured for **offline-first** development.
- All data loads from `/public/data/*.json`.
- To run:
  - `npm ci`
  - `npx playwright install chromium`
  - `npm run build && npm run test:e2e`

If you see firewall blocks (esm.ubuntu.com, api.github.com), that's expected in the agent sandbox. The **copilot-setup-steps** pre-installs what it needs before firewall rules apply.

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
