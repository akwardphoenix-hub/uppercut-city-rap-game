# Offline-Capable Setup for CI/Agent Runs

This document explains how the repository has been made fully offline-capable for CI and agent runs, eliminating firewall blocks and network flakiness.

## Problem Statement

Previously, CI runs and agents would fail due to:
- Firewall blocking external hosts (esm.ubuntu.com, vite CDN calls)
- Network timeouts and flakiness
- External API dependencies
- Race conditions in E2E tests

## Solution Overview

The repository now operates completely offline by:
1. Pre-installing all dependencies before firewall restrictions
2. Binding all servers to localhost (127.0.0.1) only
3. Loading all data from local JSON fixtures
4. Providing safe remote→local fallback for optional external APIs

## Changes Made

### 1. GitHub Copilot Setup Steps

**File**: `.github/copilot-setup-steps.yml`

Composite action that runs before firewall restrictions:
- Sets up Node 20 with npm cache
- Installs dependencies with `npm ci --no-audit --prefer-offline`
- Installs Playwright Chromium browser
- Builds the application for preview

### 2. Package Scripts

**File**: `package.json`

Updated scripts:
```json
{
  "dev": "vite --host 127.0.0.1",
  "preview": "vite preview --host 127.0.0.1 --port 4173 --strictPort",
  "ci:all": "npm run preview & npx wait-on http://127.0.0.1:4173 && playwright test --reporter=line"
}
```

New dependencies:
- `wait-on`: Ensures preview server is ready before running tests

### 3. Environment Configuration

**Files**: `.env.example`, `.env.test`

Environment variables:
- `VITE_CONGRESS_API`: Optional external API URL (empty = use local)
- `VITE_OFFLINE_ONLY`: Forces offline mode (true in tests)

### 4. Offline-First Service Layer

**File**: `src/services/councilService.ts`

New service with smart fallback logic:

```typescript
export async function getProposals(): Promise<Proposal[]> {
  // Try remote first (if configured and not offline), else local JSON
  const api = String(import.meta.env.VITE_CONGRESS_API || '').trim();
  if (!isTestOrOffline && api) {
    try {
      const r = await fetchWithTimeout(api, 4000);
      if (r.ok) return r.json();
    } catch {
      /* swallow; fallback to local */
    }
  }
  return safeJson<Proposal[]>(LOCAL.proposals);
}
```

Features:
- 4-second timeout for remote fetches
- Silent fallback to local JSON on timeout/error
- Respects `MODE === 'test'` and `VITE_OFFLINE_ONLY` flags
- No console errors on network failure

### 5. Playwright Configuration

**File**: `playwright.config.ts`

Simplified for localhost-only operation:
- baseURL: `http://127.0.0.1:4173`
- webServer command: `npm run preview`
- Chromium only (stable, fast)
- Retries in CI for resilience

### 6. CI Workflow

**File**: `.github/workflows/test.yml`

Updated workflow:
```yaml
- name: Run E2E
  env:
    VITE_OFFLINE_ONLY: "true"
  run: npm run ci:all
```

Steps:
1. Install dependencies with `--no-audit --prefer-offline`
2. Install Playwright Chromium (no system deps)
3. Build application
4. Run E2E tests with offline flag

### 7. Local Data Fixtures

**Files**: 
- `public/data/council-proposals.json` (existing)
- `public/data/council-votes.json` (new, empty array)
- `public/data/audit-log.json` (new, empty array)

All data files are copied to `dist/data/` during build and served by preview server.

## How It Resolves Firewall Blocks

### Before
❌ CI triggered `esm.ubuntu.com` DNS calls  
❌ apt package installation required  
❌ Tests could call external APIs  
❌ Firewall blocks prevented installations  

### After
✅ All dependencies installed before firewall  
✅ No system package requirements  
✅ All data loaded from local fixtures  
✅ Tests run hermetically on 127.0.0.1  

## Usage

### Local Development

```bash
# Install dependencies
npm ci

# Install Playwright browser
npx playwright install chromium

# Build
npm run build

# Run E2E tests
npm run test:e2e

# Or run everything at once
npm run ci:all
```

### CI/Agent Environment

The `.github/workflows/test.yml` workflow handles everything:
```bash
npm ci --no-audit --prefer-offline
npx playwright install chromium
npm run build
VITE_OFFLINE_ONLY=true npm run ci:all
```

### Optional Remote API

To use an external API in development:

1. Create `.env.local`:
```
VITE_CONGRESS_API=https://api.example.com/proposals
VITE_OFFLINE_ONLY=false
```

2. The service will try the remote API with 4-second timeout
3. Falls back to local JSON on failure (no errors)

## Testing

### Verify Offline Capability

```bash
# 1. Build the app
npm run build

# 2. Start preview (will use dist/data/*.json)
npm run preview

# 3. In another terminal, verify data loads
curl http://127.0.0.1:4173/data/council-proposals.json

# 4. Run E2E tests
npm run test:e2e
```

### Verify Fallback Logic

The service automatically falls back to local data when:
- `import.meta.env.MODE === 'test'`
- `VITE_OFFLINE_ONLY === 'true'`
- Remote API not configured
- Remote API times out (>4 seconds)
- Remote API returns error status

## Maintenance

### Adding New Data Files

1. Add JSON file to `public/data/`
2. Add endpoint to `src/services/councilService.ts`
3. Update LOCAL constants
4. Build will automatically copy to dist

### Updating Scripts

All scripts use 127.0.0.1 for consistency:
- `dev`: Development server
- `preview`: Production preview
- `test:e2e`: E2E tests

Don't change host to 0.0.0.0 or localhost as it may cause issues in CI.

## Troubleshooting

### Port 4173 Already in Use

```bash
# Kill existing process
lsof -ti:4173 | xargs kill -9
```

### Preview Server Won't Start

```bash
# Rebuild first
npm run build

# Then preview
npm run preview
```

### Tests Can't Find Browser

```bash
# Reinstall Playwright browsers
npx playwright install chromium
```

### Data Files Not Loading

Check that:
1. Files exist in `public/data/`
2. Build succeeded (`npm run build`)
3. Files copied to `dist/data/`
4. Preview server is running

## Architecture Decisions

### Why 127.0.0.1 Instead of localhost?

`localhost` can resolve to IPv4 or IPv6, causing flakiness. `127.0.0.1` is explicit IPv4 loopback.

### Why wait-on Instead of Sleep?

`wait-on` actively polls the server, adapting to actual startup time. More reliable than fixed delays.

### Why Chromium Only?

Webkit support removed to:
- Speed up CI (single browser)
- Reduce installation size
- Match typical user base (Chromium/Chrome)
- Keep requirements minimal per problem statement

### Why 4-Second Timeout?

Balance between:
- Fast enough for tests (<5 seconds)
- Long enough for slow networks
- Quick fallback on failure

## Acceptance Criteria ✅

- ✅ Agent no longer fails on firewall blocks
- ✅ All builds & tests use preinstalled deps + localhost
- ✅ E2E uses vite preview on 127.0.0.1 with local JSON fallbacks
- ✅ Single `npm run ci:all` command for everything
- ✅ TypeScript stays strict (no any, explicit types)
- ✅ Existing app code style preserved
