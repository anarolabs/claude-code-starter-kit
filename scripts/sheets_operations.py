#!/usr/bin/env python3
"""
Google Sheets operations.
Uses service account with domain-wide delegation.

Usage:
    # Create new spreadsheet
    python3 sheets_operations.py --create --title "Spreadsheet Title"

    # Read sheet data
    python3 sheets_operations.py --read SPREADSHEET_ID [--range "Sheet1!A1:Z100"]

    # Write data to sheet
    python3 sheets_operations.py --write SPREADSHEET_ID --range "Sheet1!A1" --data '[["a","b"],["c","d"]]'

    # Append rows to sheet
    python3 sheets_operations.py --append SPREADSHEET_ID --data '[["row1col1","row1col2"],["row2col1","row2col2"]]'

    # Upload CSV to new spreadsheet
    python3 sheets_operations.py --upload-csv --file /path/to/file.csv --title "Spreadsheet Title"

    # Upload CSV to existing spreadsheet (replaces content)
    python3 sheets_operations.py --upload-csv --file /path/to/file.csv --sheet-id SPREADSHEET_ID
"""
import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from google_client import get_sheets_service, get_drive_service


def create_spreadsheet(title: str, folder_id: str = None):
    """Create a new Google Spreadsheet."""
    sheets_service = get_sheets_service()
    drive_service = get_drive_service()

    try:
        # Create the spreadsheet
        spreadsheet = sheets_service.spreadsheets().create(
            body={"properties": {"title": title}}
        ).execute()

        spreadsheet_id = spreadsheet["spreadsheetId"]
        spreadsheet_url = spreadsheet["spreadsheetUrl"]

        # If folder specified, move the file
        if folder_id:
            file = drive_service.files().get(fileId=spreadsheet_id, fields="parents").execute()
            previous_parents = ",".join(file.get("parents", []))
            drive_service.files().update(
                fileId=spreadsheet_id,
                addParents=folder_id,
                removeParents=previous_parents,
                fields="id, parents"
            ).execute()

        print(json.dumps({
            "success": True,
            "spreadsheet_id": spreadsheet_id,
            "title": title,
            "url": spreadsheet_url
        }, indent=2))
        return spreadsheet_id

    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2), file=sys.stderr)
        sys.exit(1)


def read_sheet(spreadsheet_id: str, range_name: str = "Sheet1"):
    """Read data from a Google Spreadsheet."""
    sheets_service = get_sheets_service()

    try:
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()

        values = result.get("values", [])

        print(json.dumps({
            "success": True,
            "spreadsheet_id": spreadsheet_id,
            "range": range_name,
            "rows": len(values),
            "data": values
        }, indent=2))
        return values

    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2), file=sys.stderr)
        sys.exit(1)


def write_sheet(spreadsheet_id: str, range_name: str, data: list):
    """Write data to a Google Spreadsheet."""
    sheets_service = get_sheets_service()

    try:
        body = {"values": data}
        result = sheets_service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()

        print(json.dumps({
            "success": True,
            "spreadsheet_id": spreadsheet_id,
            "range": range_name,
            "updated_cells": result.get("updatedCells", 0),
            "updated_rows": result.get("updatedRows", 0)
        }, indent=2))

    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2), file=sys.stderr)
        sys.exit(1)


def append_sheet(spreadsheet_id: str, data: list, range_name: str = "Sheet1"):
    """Append rows to a Google Spreadsheet."""
    sheets_service = get_sheets_service()

    try:
        body = {"values": data}
        result = sheets_service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()

        updates = result.get("updates", {})
        print(json.dumps({
            "success": True,
            "spreadsheet_id": spreadsheet_id,
            "updated_range": updates.get("updatedRange", ""),
            "updated_rows": updates.get("updatedRows", 0)
        }, indent=2))

    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2), file=sys.stderr)
        sys.exit(1)


def upload_csv(file_path: str, title: str = None, spreadsheet_id: str = None):
    """Upload a CSV file to Google Sheets."""
    sheets_service = get_sheets_service()

    # Read CSV file
    csv_path = Path(file_path)
    if not csv_path.exists():
        print(json.dumps({
            "success": False,
            "error": f"File not found: {file_path}"
        }, indent=2), file=sys.stderr)
        sys.exit(1)

    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        data = list(reader)

    if not data:
        print(json.dumps({
            "success": False,
            "error": "CSV file is empty"
        }, indent=2), file=sys.stderr)
        sys.exit(1)

    try:
        # Create new spreadsheet if no ID provided
        if not spreadsheet_id:
            if not title:
                title = csv_path.stem  # Use filename without extension

            spreadsheet = sheets_service.spreadsheets().create(
                body={"properties": {"title": title}}
            ).execute()
            spreadsheet_id = spreadsheet["spreadsheetId"]
            spreadsheet_url = spreadsheet["spreadsheetUrl"]
            created_new = True
        else:
            # Get existing spreadsheet URL
            spreadsheet = sheets_service.spreadsheets().get(
                spreadsheetId=spreadsheet_id
            ).execute()
            spreadsheet_url = spreadsheet["spreadsheetUrl"]
            created_new = False

        # Clear existing content if updating existing sheet
        if not created_new:
            sheets_service.spreadsheets().values().clear(
                spreadsheetId=spreadsheet_id,
                range="Sheet1"
            ).execute()

        # Write the CSV data
        body = {"values": data}
        result = sheets_service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range="Sheet1!A1",
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()

        print(json.dumps({
            "success": True,
            "spreadsheet_id": spreadsheet_id,
            "url": spreadsheet_url,
            "title": title or spreadsheet.get("properties", {}).get("title", ""),
            "created_new": created_new,
            "rows": len(data),
            "columns": len(data[0]) if data else 0
        }, indent=2))

    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e)
        }, indent=2), file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Google Sheets operations")

    # Operation flags
    parser.add_argument("--create", action="store_true", help="Create new spreadsheet")
    parser.add_argument("--read", metavar="SPREADSHEET_ID", help="Read spreadsheet data")
    parser.add_argument("--write", metavar="SPREADSHEET_ID", help="Write data to spreadsheet")
    parser.add_argument("--append", metavar="SPREADSHEET_ID", help="Append rows to spreadsheet")
    parser.add_argument("--upload-csv", action="store_true", help="Upload CSV file to spreadsheet")

    # Parameters
    parser.add_argument("--title", help="Spreadsheet title (for create/upload-csv)")
    parser.add_argument("--range", default="Sheet1", help="Cell range (default: Sheet1)")
    parser.add_argument("--data", help="JSON array of data (for write/append)")
    parser.add_argument("--file", help="Path to CSV file (for upload-csv)")
    parser.add_argument("--sheet-id", help="Existing spreadsheet ID (for upload-csv)")
    parser.add_argument("--folder", help="Google Drive folder ID to place spreadsheet in")

    args = parser.parse_args()

    if args.create:
        if not args.title:
            parser.error("--create requires --title")
        create_spreadsheet(args.title, args.folder)

    elif args.read:
        read_sheet(args.read, args.range)

    elif args.write:
        if not args.data:
            parser.error("--write requires --data")
        data = json.loads(args.data)
        write_sheet(args.write, args.range, data)

    elif args.append:
        if not args.data:
            parser.error("--append requires --data")
        data = json.loads(args.data)
        append_sheet(args.append, data, args.range)

    elif args.upload_csv:
        if not args.file:
            parser.error("--upload-csv requires --file")
        upload_csv(args.file, args.title, args.sheet_id)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
