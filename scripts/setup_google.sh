#!/usr/bin/env bash
# Google Workspace setup for Claude Code
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
KEY_FILE="$TARGET_DIR/google-service-account.json"
CONFIG_FILE="$TARGET_DIR/config.json"

mkdir -p "$TARGET_DIR"

# Copy key file with secure permissions
cp "$KEY_SOURCE" "$KEY_FILE"
chmod 600 "$KEY_FILE"

echo "Service account key installed at: $KEY_FILE"

# Write config file
python3 -c "
import json, os
config_path = os.path.expanduser('$CONFIG_FILE')
config = {}
if os.path.exists(config_path):
    with open(config_path) as f:
        config = json.load(f)
config['google_email'] = '$USER_EMAIL'
config['service_account_key'] = '$KEY_FILE'
with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)
print(f'Config written to: {config_path}')
print(f'  google_email: $USER_EMAIL')
"

echo ""

# Install dependencies
echo "Installing Google API dependencies..."
pip install --quiet google-auth google-auth-oauthlib google-api-python-client 2>/dev/null || \
pip3 install --quiet google-auth google-auth-oauthlib google-api-python-client

echo ""
echo "Testing connection..."
echo ""

# Run verification
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$SCRIPT_DIR/google_client.py"
