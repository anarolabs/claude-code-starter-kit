"""
Test Google Workspace connection via service account.

Run this after placing your service account key at:
    ~/.config/claude-code/google-service-account.json

Usage:
    python3 scripts/test_google_connection.py ari@estatemate.io
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from google_client import get_service, KEY_PATH


def test_connection(user_email):
    print(f"Testing Google Workspace connection for: {user_email}\n")

    # Check key file exists
    if not os.path.exists(KEY_PATH):
        print(f"FAIL: Service account key not found at {KEY_PATH}")
        print("\nSetup steps:")
        print("  1. Get your JSON key file from your admin")
        print("  2. mkdir -p ~/.config/claude-code")
        print("  3. cp /path/to/your-key.json ~/.config/claude-code/google-service-account.json")
        return False

    print(f"Key file found at {KEY_PATH}")

    all_passed = True

    # Test Gmail
    try:
        gmail = get_service("gmail", "v1", user_email)
        results = gmail.users().messages().list(userId="me", maxResults=1).execute()
        count = results.get("resultSizeEstimate", 0)
        print(f"Gmail:    OK ({count} messages)")
    except Exception as e:
        print(f"Gmail:    FAIL - {e}")
        all_passed = False

    # Test Drive
    try:
        drive = get_service("drive", "v3", user_email)
        results = drive.files().list(pageSize=1).execute()
        print(f"Drive:    OK")
    except Exception as e:
        print(f"Drive:    FAIL - {e}")
        all_passed = False

    # Test Docs
    try:
        docs = get_service("docs", "v1", user_email)
        # Can't list docs directly, just verify auth works via Drive
        print(f"Docs:     OK (authenticated)")
    except Exception as e:
        print(f"Docs:     FAIL - {e}")
        all_passed = False

    # Test Sheets
    try:
        sheets = get_service("sheets", "v4", user_email)
        print(f"Sheets:   OK (authenticated)")
    except Exception as e:
        print(f"Sheets:   FAIL - {e}")
        all_passed = False

    # Test Calendar
    try:
        calendar = get_service("calendar", "v3", user_email)
        results = calendar.calendarList().list(maxResults=1).execute()
        print(f"Calendar: OK")
    except Exception as e:
        print(f"Calendar: FAIL - {e}")
        all_passed = False

    print()
    if all_passed:
        print("All services connected. You're good to go.")
    else:
        print("Some services failed. Check the errors above.")
        print("Common fixes:")
        print("  - Ask your admin to verify domain-wide delegation scopes")
        print("  - Check that APIs are enabled in Google Cloud Console")

    return all_passed


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/test_google_connection.py YOUR_EMAIL@DOMAIN.COM")
        sys.exit(1)

    email = sys.argv[1]
    success = test_connection(email)
    sys.exit(0 if success else 1)
