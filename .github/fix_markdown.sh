#!/bin/bash
# Auto-fix common markdownlint errors

echo "Running markdown auto-fix..."

# Install markdownlint if not present
if ! command -v markdownlint-cli2 &> /dev/null; then
  echo "Installing markdownlint-cli2..."
  npm install -g markdownlint-cli2
fi

# Run with auto-fix where possible
markdownlint-cli2 --fix "**/*.md"

echo "Auto-fix complete. Run lint again to check remaining issues."
echo "Manual fixes may still be needed for MD013 (long lines) and complex cases."