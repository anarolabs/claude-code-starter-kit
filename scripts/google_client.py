#!/usr/bin/env python3
"""
Shared Google Workspace client.
Uses service account with domain-wide delegation for authentication.
No OAuth flows - just works.

Setup:
    1. Place your service account JSON key at ~/.config/claude-code/google-service-account.json
    2. Set your email in ~/.config/claude-code/config.json
    3. Run: python3 scripts/test_google_connection.py
"""
import io
import json
import sys
import warnings
from pathlib import Path

# Suppress Python deprecation warnings from google-api-core
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Monkey-patch to suppress Google's print() calls during import
import builtins
_original_print = builtins.print
def _silent_print(*args, **kwargs):
    if args and "error occurred" in str(args[0]).lower():
        return
    _original_print(*args, **kwargs)
builtins.print = _silent_print

# Configuration
CONFIG_DIR = Path.home() / ".config/claude-code"
CONFIG_FILE = CONFIG_DIR / "config.json"
DEFAULT_KEY_PATH = CONFIG_DIR / "google-service-account.json"

def _load_config():
    """Load user configuration."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}

config = _load_config()

SERVICE_ACCOUNT_FILE = Path(config.get("service_account_key", str(DEFAULT_KEY_PATH)))
IMPERSONATE_USER = config.get("google_email", "")

if not IMPERSONATE_USER:
    # Fallback: check if config.json exists but has no email
    if CONFIG_FILE.exists():
        print("ERROR: 'google_email' not set in ~/.config/claude-code/config.json", file=sys.stderr)
    else:
        print("ERROR: Config not found. Run: bash scripts/setup_google.sh YOUR_KEY.json YOUR_EMAIL", file=sys.stderr)
    sys.exit(1)

# Scopes for all Google services
SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/calendar.events",
]


def _check_dependencies():
    """Check if required packages are installed."""
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        return True
    except ImportError:
        print("ERROR: Missing Google API dependencies", file=sys.stderr)
        print("Install with: pip install google-auth google-auth-oauthlib google-api-python-client", file=sys.stderr)
        return False


def _load_credentials():
    """Load service account credentials with domain-wide delegation."""
    if not SERVICE_ACCOUNT_FILE.exists():
        print(f"ERROR: Service account file not found at {SERVICE_ACCOUNT_FILE}", file=sys.stderr)
        print("Run: bash scripts/setup_google.sh YOUR_KEY.json YOUR_EMAIL", file=sys.stderr)
        sys.exit(1)

    from google.oauth2 import service_account

    credentials = service_account.Credentials.from_service_account_file(
        str(SERVICE_ACCOUNT_FILE),
        scopes=SCOPES
    )

    # Impersonate the user via domain-wide delegation
    delegated_credentials = credentials.with_subject(IMPERSONATE_USER)

    return delegated_credentials


def get_gmail_service():
    """Get authenticated Gmail API service."""
    if not _check_dependencies():
        sys.exit(1)
    from googleapiclient.discovery import build
    credentials = _load_credentials()
    return build("gmail", "v1", credentials=credentials)


def get_drive_service():
    """Get authenticated Google Drive API service."""
    if not _check_dependencies():
        sys.exit(1)
    from googleapiclient.discovery import build
    credentials = _load_credentials()
    return build("drive", "v3", credentials=credentials)


def get_docs_service():
    """Get authenticated Google Docs API service."""
    if not _check_dependencies():
        sys.exit(1)
    from googleapiclient.discovery import build
    credentials = _load_credentials()
    return build("docs", "v1", credentials=credentials)


def get_sheets_service():
    """Get authenticated Google Sheets API service."""
    if not _check_dependencies():
        sys.exit(1)
    from googleapiclient.discovery import build
    credentials = _load_credentials()
    return build("sheets", "v4", credentials=credentials)


def get_calendar_service():
    """Get authenticated Google Calendar API service."""
    if not _check_dependencies():
        sys.exit(1)
    from googleapiclient.discovery import build
    credentials = _load_credentials()
    return build("calendar", "v3", credentials=credentials)


def verify_setup():
    """Verify service account setup is working."""
    print(f"Service account file: {SERVICE_ACCOUNT_FILE}")
    print(f"Impersonating user: {IMPERSONATE_USER}")
    print(f"Scopes: {len(SCOPES)} configured")
    print()

    if not SERVICE_ACCOUNT_FILE.exists():
        print("ERROR: Service account file not found")
        return False

    try:
        service = get_gmail_service()
        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])
        print(f"Gmail:    OK ({len(labels)} labels)")

        service = get_drive_service()
        results = service.files().list(pageSize=1).execute()
        print(f"Drive:    OK")

        service = get_docs_service()
        print(f"Docs:     OK")

        service = get_sheets_service()
        print(f"Sheets:   OK")

        service = get_calendar_service()
        results = service.calendarList().list(maxResults=1).execute()
        print(f"Calendar: OK")

        print("\nAll services connected.")
        return True

    except Exception as e:
        print(f"\nERROR: {str(e)}", file=sys.stderr)
        if "invalid_grant" in str(e).lower():
            print("\nDomain-wide delegation may not be configured correctly.", file=sys.stderr)
            print("Check: admin.google.com > Security > API Controls > Domain Wide Delegation", file=sys.stderr)
        return False


if __name__ == "__main__":
    print("Google Workspace Client - Setup Verification")
    print("=" * 50)
    verify_setup()
