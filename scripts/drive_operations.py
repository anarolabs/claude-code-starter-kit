#!/usr/bin/env python3
"""
Google Drive operations.
Uses service account with domain-wide delegation.

Usage:
    # Search files
    python3 drive_operations.py --search "budget 2025" [--max 10]

    # List folder contents
    python3 drive_operations.py --list FOLDER_ID [--max 20]

    # List root folder
    python3 drive_operations.py --list root

    # Get file metadata
    python3 drive_operations.py --get FILE_ID

    # Read file content (Google Docs/Sheets export or download)
    python3 drive_operations.py --read FILE_ID [--format txt|pdf|docx]

    # Download file
    python3 drive_operations.py --download FILE_ID --output /path/to/file

    # Rename file
    python3 drive_operations.py --rename FILE_ID --name "New Name"

    # Delete file (move to trash)
    python3 drive_operations.py --delete FILE_ID

    # Permanently delete file
    python3 drive_operations.py --delete FILE_ID --permanent
"""
import argparse
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from google_client import get_drive_service


# MIME type mappings for exports
EXPORT_FORMATS = {
    "txt": "text/plain",
    "pdf": "application/pdf",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "csv": "text/csv",
    "html": "text/html",
}


def search_files(query: str, max_results: int = 10):
    """Search files in Drive."""
    service = get_drive_service()

    # Build search query - fullText contains for content search
    drive_query = f"fullText contains '{query}' and trashed = false"

    try:
        results = service.files().list(
            q=drive_query,
            pageSize=max_results,
            fields="files(id, name, mimeType, modifiedTime, size, parents, webViewLink)"
        ).execute()

        files = results.get("files", [])

        output = [{
            "id": f["id"],
            "name": f["name"],
            "mime_type": f["mimeType"],
            "modified": f.get("modifiedTime"),
            "size": f.get("size"),
            "url": f.get("webViewLink")
        } for f in files]

        print(json.dumps({"results": output, "count": len(output)}, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


def list_folder(folder_id: str, max_results: int = 20):
    """List contents of a folder."""
    service = get_drive_service()

    # Handle 'root' as special case
    if folder_id.lower() == "root":
        query = "'root' in parents and trashed = false"
    else:
        query = f"'{folder_id}' in parents and trashed = false"

    try:
        results = service.files().list(
            q=query,
            pageSize=max_results,
            fields="files(id, name, mimeType, modifiedTime, size, webViewLink)",
            orderBy="folder,name"
        ).execute()

        files = results.get("files", [])

        output = [{
            "id": f["id"],
            "name": f["name"],
            "type": "folder" if f["mimeType"] == "application/vnd.google-apps.folder" else "file",
            "mime_type": f["mimeType"],
            "modified": f.get("modifiedTime"),
            "size": f.get("size"),
            "url": f.get("webViewLink")
        } for f in files]

        print(json.dumps({"contents": output, "count": len(output)}, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


def get_file_metadata(file_id: str):
    """Get file metadata."""
    service = get_drive_service()

    try:
        file = service.files().get(
            fileId=file_id,
            fields="id, name, mimeType, modifiedTime, createdTime, size, parents, webViewLink, description"
        ).execute()

        print(json.dumps({
            "id": file["id"],
            "name": file["name"],
            "mime_type": file["mimeType"],
            "created": file.get("createdTime"),
            "modified": file.get("modifiedTime"),
            "size": file.get("size"),
            "parents": file.get("parents", []),
            "url": file.get("webViewLink"),
            "description": file.get("description")
        }, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


def read_file_content(file_id: str, export_format: str = "txt"):
    """Read file content. For Google Docs/Sheets, exports to specified format."""
    service = get_drive_service()

    try:
        # First get file metadata to check type
        file = service.files().get(fileId=file_id, fields="mimeType, name").execute()
        mime_type = file["mimeType"]

        # Google Docs/Sheets need export
        if mime_type.startswith("application/vnd.google-apps"):
            export_mime = EXPORT_FORMATS.get(export_format, "text/plain")

            request = service.files().export_media(fileId=file_id, mimeType=export_mime)
            content = request.execute()

            if isinstance(content, bytes):
                try:
                    content = content.decode("utf-8")
                except UnicodeDecodeError:
                    # Binary content (like PDF)
                    content = f"[Binary content - {len(content)} bytes]"

            print(json.dumps({
                "id": file_id,
                "name": file["name"],
                "format": export_format,
                "content": content
            }, indent=2))

        else:
            # Regular file - download
            request = service.files().get_media(fileId=file_id)
            content = request.execute()

            if isinstance(content, bytes):
                try:
                    content = content.decode("utf-8")
                except UnicodeDecodeError:
                    content = f"[Binary content - {len(content)} bytes]"

            print(json.dumps({
                "id": file_id,
                "name": file["name"],
                "content": content
            }, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


def download_file(file_id: str, output_path: str, export_format: str = None):
    """Download file to local path. For Google Docs/Sheets, export_format overrides the default."""
    service = get_drive_service()

    try:
        # Get file metadata
        file = service.files().get(fileId=file_id, fields="mimeType, name").execute()
        mime_type = file["mimeType"]

        # Google Docs/Sheets need export
        if mime_type.startswith("application/vnd.google-apps"):
            if export_format and export_format in EXPORT_FORMATS:
                export_mime = EXPORT_FORMATS[export_format]
            elif mime_type == "application/vnd.google-apps.document":
                export_mime = EXPORT_FORMATS["docx"]
            elif mime_type == "application/vnd.google-apps.spreadsheet":
                export_mime = EXPORT_FORMATS["xlsx"]
            else:
                export_mime = EXPORT_FORMATS["pdf"]
            request = service.files().export_media(fileId=file_id, mimeType=export_mime)
        else:
            request = service.files().get_media(fileId=file_id)

        content = request.execute()

        # Write to file
        output = Path(output_path)
        output.write_bytes(content if isinstance(content, bytes) else content.encode())

        print(json.dumps({
            "success": True,
            "file_id": file_id,
            "name": file["name"],
            "output": str(output),
            "size": len(content)
        }, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


def rename_file(file_id: str, new_name: str):
    """Rename a file."""
    service = get_drive_service()

    try:
        # Get current name for confirmation
        old_file = service.files().get(fileId=file_id, fields="name").execute()
        old_name = old_file["name"]

        # Update the name
        file = service.files().update(
            fileId=file_id,
            body={"name": new_name},
            fields="id, name, webViewLink"
        ).execute()

        print(json.dumps({
            "success": True,
            "file_id": file_id,
            "old_name": old_name,
            "new_name": file["name"],
            "url": file.get("webViewLink")
        }, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


def delete_file(file_id: str, permanent: bool = False):
    """Delete a file (move to trash or permanently delete)."""
    service = get_drive_service()

    try:
        # Get file name for confirmation
        file = service.files().get(fileId=file_id, fields="name").execute()
        file_name = file["name"]

        if permanent:
            # Permanently delete
            service.files().delete(fileId=file_id).execute()
            action = "permanently deleted"
        else:
            # Move to trash
            service.files().update(
                fileId=file_id,
                body={"trashed": True}
            ).execute()
            action = "moved to trash"

        print(json.dumps({
            "success": True,
            "file_id": file_id,
            "name": file_name,
            "action": action
        }, indent=2))

    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Google Drive operations for Anaro Labs")

    # Operation flags
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--search", metavar="QUERY", help="Search files")
    group.add_argument("--list", metavar="FOLDER_ID", help="List folder contents (use 'root' for root)")
    group.add_argument("--get", metavar="FILE_ID", help="Get file metadata")
    group.add_argument("--read", metavar="FILE_ID", help="Read file content")
    group.add_argument("--download", metavar="FILE_ID", help="Download file")
    group.add_argument("--rename", metavar="FILE_ID", help="Rename file")
    group.add_argument("--delete", metavar="FILE_ID", help="Delete file (move to trash)")

    # Options
    parser.add_argument("--max", type=int, default=10, help="Max results (default: 10)")
    parser.add_argument("--format", choices=["txt", "pdf", "docx", "xlsx", "csv", "html"], default="txt",
                        help="Export format for Google Docs (default: txt)")
    parser.add_argument("--output", help="Output path for download")
    parser.add_argument("--name", help="New name for rename operation")
    parser.add_argument("--permanent", action="store_true", help="Permanently delete instead of trash")

    args = parser.parse_args()

    if args.search:
        search_files(args.search, args.max)

    elif args.list:
        list_folder(args.list, args.max)

    elif args.get:
        get_file_metadata(args.get)

    elif args.read:
        read_file_content(args.read, args.format)

    elif args.download:
        if not args.output:
            parser.error("--download requires --output")
        download_file(args.download, args.output, export_format=args.format)

    elif args.rename:
        if not args.name:
            parser.error("--rename requires --name")
        rename_file(args.rename, args.name)

    elif args.delete:
        delete_file(args.delete, args.permanent)


if __name__ == "__main__":
    main()
