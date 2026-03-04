#!/usr/bin/env python3
"""
Google Calendar operations.
Uses service account with domain-wide delegation.

Usage:
    # Today's events
    python3 calendar_operations.py --today

    # Next N days (default 7)
    python3 calendar_operations.py --upcoming 3

    # Date range
    python3 calendar_operations.py --range 2026-02-09 2026-02-14

    # Specific calendar (default: primary)
    python3 calendar_operations.py --today --calendar "work@example.com"

    # List available calendars
    python3 calendar_operations.py --list-calendars

    # Create an event
    python3 calendar_operations.py --create-event --title "Focus block" --start 2026-02-09T09:00:00 --end 2026-02-09T10:00:00
    python3 calendar_operations.py --create-event --title "Deep work" --start 2026-02-09T14:00:00 --end 2026-02-09T15:30:00 --description "EstateMate sprint" --color 9
"""
import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from google_client import get_calendar_service


def list_calendars(service):
    """List all calendars accessible to the user."""
    results = service.calendarList().list().execute()
    calendars = []
    for cal in results.get("items", []):
        calendars.append({
            "id": cal["id"],
            "summary": cal.get("summary", "(no name)"),
            "primary": cal.get("primary", False),
            "access_role": cal.get("accessRole", "unknown"),
        })
    return calendars


def get_events(service, calendar_id, time_min, time_max, max_results=50):
    """Fetch events in a time range."""
    results = service.events().list(
        calendarId=calendar_id,
        timeMin=time_min,
        timeMax=time_max,
        maxResults=max_results,
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    events = []
    for event in results.get("items", []):
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["end"].get("date"))

        attendees = []
        for a in event.get("attendees", []):
            attendees.append({
                "email": a.get("email"),
                "name": a.get("displayName"),
                "status": a.get("responseStatus"),
                "self": a.get("self", False),
            })

        events.append({
            "id": event.get("id"),
            "title": event.get("summary", "(no title)"),
            "start": start,
            "end": end,
            "all_day": "date" in event["start"],
            "location": event.get("location"),
            "description": event.get("description"),
            "status": event.get("status"),
            "html_link": event.get("htmlLink"),
            "attendees": attendees,
            "organizer": event.get("organizer", {}).get("email"),
            "conference": _extract_conference(event),
        })

    return events


def create_event(service, calendar_id, title, start, end, description=None, color_id=None):
    """Create a calendar event.

    Args:
        title: Event summary/title.
        start: ISO datetime string (e.g. 2026-02-09T09:00:00).
        end: ISO datetime string (e.g. 2026-02-09T10:00:00).
        description: Optional event description.
        color_id: Optional Google Calendar color ID (1-11).
    """
    # Detect timezone from system locale, default to Europe/Berlin
    import time
    tz_name = time.tzname[0] if time.tzname[0] else "Europe/Berlin"
    # Map common abbreviations
    tz_map = {"CET": "Europe/Berlin", "CEST": "Europe/Berlin", "PST": "America/Los_Angeles",
              "PDT": "America/Los_Angeles", "EST": "America/New_York", "EDT": "America/New_York"}
    timezone_str = tz_map.get(tz_name, "Europe/Berlin")

    body = {
        "summary": title,
        "start": {"dateTime": start, "timeZone": timezone_str},
        "end": {"dateTime": end, "timeZone": timezone_str},
    }
    if description:
        body["description"] = description
    if color_id:
        body["colorId"] = str(color_id)

    result = service.events().insert(calendarId=calendar_id, body=body).execute()
    return {
        "id": result.get("id"),
        "title": result.get("summary"),
        "start": result["start"].get("dateTime"),
        "end": result["end"].get("dateTime"),
        "html_link": result.get("htmlLink"),
        "status": result.get("status"),
    }


def _extract_conference(event):
    """Extract video conference link if present."""
    conf = event.get("conferenceData")
    if not conf:
        return None
    for ep in conf.get("entryPoints", []):
        if ep.get("entryPointType") == "video":
            return ep.get("uri")
    return None


def _date_to_rfc3339(date_str, end_of_day=False):
    """Convert YYYY-MM-DD to RFC3339 timestamp."""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    if end_of_day:
        dt = dt.replace(hour=23, minute=59, second=59)
    return dt.strftime("%Y-%m-%dT%H:%M:%S") + "Z"


def main():
    parser = argparse.ArgumentParser(description="Google Calendar operations")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--today", action="store_true", help="Show today's events")
    group.add_argument("--upcoming", type=int, metavar="DAYS", help="Show next N days")
    group.add_argument("--range", nargs=2, metavar=("START", "END"), help="Date range (YYYY-MM-DD)")
    group.add_argument("--list-calendars", action="store_true", help="List available calendars")
    group.add_argument("--create-event", action="store_true", help="Create a calendar event")

    parser.add_argument("--calendar", default="primary", help="Calendar ID (default: primary)")
    parser.add_argument("--max", type=int, default=50, help="Max events to return")

    # Event creation arguments
    parser.add_argument("--title", help="Event title (for --create-event)")
    parser.add_argument("--start", help="Start time ISO format, e.g. 2026-02-09T09:00:00 (for --create-event)")
    parser.add_argument("--end", help="End time ISO format, e.g. 2026-02-09T10:00:00 (for --create-event)")
    parser.add_argument("--description", help="Event description (for --create-event)")
    parser.add_argument("--color", type=int, choices=range(1, 12), metavar="1-11", help="Google Calendar color ID (for --create-event)")

    args = parser.parse_args()
    service = get_calendar_service()

    if args.list_calendars:
        calendars = list_calendars(service)
        print(json.dumps(calendars, indent=2))
        return

    if args.create_event:
        if not args.title or not args.start or not args.end:
            parser.error("--create-event requires --title, --start, and --end")
        result = create_event(
            service, args.calendar, args.title, args.start, args.end,
            description=args.description, color_id=args.color,
        )
        print(json.dumps(result, indent=2))
        return

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if args.today:
        time_min = _date_to_rfc3339(today)
        time_max = _date_to_rfc3339(today, end_of_day=True)
    elif args.upcoming:
        time_min = _date_to_rfc3339(today)
        end = (datetime.now(timezone.utc) + timedelta(days=args.upcoming)).strftime("%Y-%m-%d")
        time_max = _date_to_rfc3339(end, end_of_day=True)
    elif args.range:
        time_min = _date_to_rfc3339(args.range[0])
        time_max = _date_to_rfc3339(args.range[1], end_of_day=True)

    events = get_events(service, args.calendar, time_min, time_max, args.max)
    print(json.dumps(events, indent=2))


if __name__ == "__main__":
    main()
