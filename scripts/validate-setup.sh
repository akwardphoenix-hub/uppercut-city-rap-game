#!/usr/bin/env bash
set -euo pipefail

echo "🔍 Validating project setup..."
echo ""

# Check required files exist
echo "✓ Checking required files..."
required_files=(
  "package.json"
  "tsconfig.json"
  "vite.config.ts"
  "playwright.config.ts"
  ".eslintrc.cjs"
  "src/main.tsx"
  "src/App.tsx"
  "src/lib/config.ts"
  "src/lib/audit.ts"
  "src/services/councilData.ts"
  "public/data/council-proposals.json"
  "e2e/01-app-loads.spec.ts"
  ".github/workflows/test.yml"
  ".github/copilot-instructions.md"
)

for file in "${required_files[@]}"; do
  if [ ! -f "$file" ]; then
    echo "❌ Missing required file: $file"
    exit 1
  fi
done
echo "  All required files present ✓"
echo ""

# Check package.json has required scripts
echo "✓ Checking package.json scripts..."
required_scripts=("dev" "build" "preview" "typecheck" "lint" "test:e2e")
for script in "${required_scripts[@]}"; do
  if ! grep -q "\"$script\":" package.json; then
    echo "❌ Missing script in package.json: $script"
    exit 1
  fi
done
echo "  All required scripts present ✓"
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
  echo "❌ node_modules not found. Run 'npm install' first."
  exit 1
fi
echo "✓ node_modules exists"
echo ""

# Run typecheck
echo "✓ Running typecheck..."
if npm run typecheck > /dev/null 2>&1; then
  echo "  Typecheck passed ✓"
else
  echo "❌ Typecheck failed"
  exit 1
fi
echo ""

# Run lint
echo "✓ Running lint..."
if npm run lint > /dev/null 2>&1; then
  echo "  Lint passed ✓"
else
  echo "❌ Lint failed"
  exit 1
fi
echo ""

# Run build
echo "✓ Running build..."
if npm run build > /dev/null 2>&1; then
  echo "  Build passed ✓"
else
  echo "❌ Build failed"
  exit 1
fi
echo ""

# Check build output
echo "✓ Checking build output..."
if [ ! -d "dist" ]; then
  echo "❌ dist directory not found"
  exit 1
fi
if [ ! -f "dist/index.html" ]; then
  echo "❌ dist/index.html not found"
  exit 1
fi
if [ ! -f "dist/data/council-proposals.json" ]; then
  echo "❌ dist/data/council-proposals.json not found (fixture not copied)"
  exit 1
fi
echo "  Build output looks good ✓"
echo ""

echo "✅ All validation checks passed!"
echo ""
echo "Next steps:"
echo "  1. Install Playwright browsers: npx playwright install chromium"
echo "  2. Run E2E tests: npm run test:e2e"
