# Setup Instructions

## Prerequisites

- Node.js 20.x
- npm (comes with Node.js)

## Installation Steps

1. **Install Dependencies**
   ```bash
   npm ci
   ```

2. **Install Playwright Browsers** (Required for E2E tests)
   ```bash
   npx playwright install chromium
   ```
   
   Or with system dependencies:
   ```bash
   npx playwright install --with-deps chromium
   ```

   **Note**: In restricted network environments (like CI sandboxes with firewall rules), Playwright browser installation may fail. The GitHub Actions workflow handles this automatically with the `--with-deps` flag.

3. **Verify Setup**
   ```bash
   npm run typecheck  # Should pass
   npm run lint       # Should pass
   npm run build      # Should pass
   ```

4. **Run E2E Tests** (requires Playwright browsers installed)
   ```bash
   npm run test:e2e
   ```

## Development

- **Start dev server**: `npm run dev` (http://localhost:5173)
- **Build for production**: `npm run build`
- **Preview production build**: `npm run preview` (http://localhost:4173)
- **Run typecheck**: `npm run typecheck`
- **Run linter**: `npm run lint`

## Offline-First Architecture

This project is designed to work **completely offline** during development and testing:

- All data comes from `/public/data/*.json` fixtures
- No external API calls during tests
- E2E tests use the built preview server (local only)
- Feature flag `VITE_OFFLINE=1` enforces local data loading

## Pre-Publish Check

Run the complete check script before merging:

```bash
./scripts/pre-publish-check.sh
```

Or on Windows (run steps manually):

```cmd
npm ci
npm run typecheck
npm run lint
npm run build
npx playwright install chromium
npm run test:e2e
```

## Troubleshooting

### Playwright Installation Issues

If you encounter network errors when installing Playwright browsers:

1. Check your network connectivity
2. Try using a proxy if behind a corporate firewall
3. In CI environments, ensure the workflow uses `npx playwright install --with-deps chromium`
4. Pre-download browsers manually if needed (see Playwright docs)

### Build Issues

If the build fails:

1. Clear node_modules and reinstall: `rm -rf node_modules package-lock.json && npm install`
2. Clear build cache: `rm -rf dist`
3. Check TypeScript errors: `npm run typecheck`
4. Check linting errors: `npm run lint`
