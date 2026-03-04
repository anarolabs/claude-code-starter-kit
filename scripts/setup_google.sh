#!/usr/bin/env bash
# Google Workspace setup for Claude Code
# Run this after getting your service account JSON key from your admin.
#
# Usage:
#   bash scripts/setup_google.sh /path/to/your-key.json your-email@domain.com

set -euo pipefail

KEY_SOURCE="${1:-}"
USER_EMAIL="${2:-}"

if [[ -z "$KEY_SOURCE" || -z "$USER_EMAIL" ]]; then
    echo "Usage: bash scripts/setup_google.sh /path/to/your-key.json your-email@domain.com"
    echo ""
    echo "Example:"
    echo "  bash scripts/setup_google.sh ~/Downloads/my-service-account.json ari@estatemate.io"
    exit 1
fi

if [[ ! -f "$KEY_SOURCE" ]]; then
    echo "Error: Key file not found at $KEY_SOURCE"
    exit 1
fi

# Create config directory
TARGET_DIR="$HOME/.config/claude-code"
TARGET_FILE="$TARGET_DIR/google-service-account.json"

mkdir -p "$TARGET_DIR"

# Copy key file
cp "$KEY_SOURCE" "$TARGET_FILE"
chmod 600 "$TARGET_FILE"

echo "Service account key installed at: $TARGET_FILE"
echo ""

# Install dependencies
echo "Installing Google API dependencies..."
pip install --quiet google-auth google-auth-oauthlib google-api-python-client

echo ""
echo "Testing connection..."
echo ""

# Run connection test
python3 "$(dirname "$0")/test_google_connection.py" "$USER_EMAIL"
