"""
Google Workspace client using service account authentication.

Usage:
    from google_client import get_service

    # Get a Gmail service for ari@estatemate.io
    gmail = get_service("gmail", "v1", "ari@estatemate.io")

    # Get a Drive service
    drive = get_service("drive", "v3", "ari@estatemate.io")

    # Get a Docs service
    docs = get_service("docs", "v1", "ari@estatemate.io")

    # Get a Sheets service
    sheets = get_service("sheets", "v4", "ari@estatemate.io")

Setup:
    1. Place your service account JSON key at ~/.config/claude-code/google-service-account.json
    2. Run: python3 scripts/test_google_connection.py
"""

import os
import sys

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
except ImportError:
    print("Missing dependencies. Install with:")
    print("  pip install google-auth google-auth-oauthlib google-api-python-client")
    sys.exit(1)

DEFAULT_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/calendar",
]

KEY_PATH = os.path.expanduser("~/.config/claude-code/google-service-account.json")


def get_credentials(user_email, scopes=None):
    """Get service account credentials that impersonate the given user."""
    if not os.path.exists(KEY_PATH):
        print(f"Service account key not found at: {KEY_PATH}")
        print("Place your JSON key file there and try again.")
        sys.exit(1)

    credentials = service_account.Credentials.from_service_account_file(
        KEY_PATH,
        scopes=scopes or DEFAULT_SCOPES,
        subject=user_email,
    )
    return credentials


def get_service(service_name, version, user_email, scopes=None):
    """Build a Google API service client.

    Args:
        service_name: API name (e.g., "gmail", "drive", "docs", "sheets", "calendar")
        version: API version (e.g., "v1", "v3")
        user_email: Email to impersonate (e.g., "ari@estatemate.io")
        scopes: Optional list of scopes (defaults to all configured scopes)

    Returns:
        Google API service client
    """
    credentials = get_credentials(user_email, scopes)
    return build(service_name, version, credentials=credentials)
