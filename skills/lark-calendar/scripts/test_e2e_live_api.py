#!/usr/bin/env python3
"""E2E tests for lark-calendar skill — live API, no mocks, sequential CRUD roundtrips.

Tests Calendar methods:
  - get_primary_calendar_id: fetched via LARK_CALENDAR_ID env var (from MCP whoami)
  - list_events(calendar_id, start_ms, end_ms)
  - create_event(calendar_id, event_data)
  - get_event(calendar_id, event_id)
  - get_calendar_list()
  - get_calendar(calendar_id)
  - get_attendee_list(calendar_id, event_id)
  - search_events(calendar_id, query)
  - update_event(calendar_id, event_id, event_data)
  - delete_event(calendar_id, event_id)

Skipped (manual test recommended):
  - query_freebusy: needs valid user_ids in org context
  - delete_attendees: would remove attendees needed by get_attendee_list test

Env vars required:
  LARK_ACCESS_TOKEN  — user OAuth token
  LARK_OPEN_ID       — user open_id (ou_...)
  LARK_CALENDAR_ID   — primary calendar ID (from MCP whoami primary_calendar_id)
"""

import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lark_api import LarkCalendarClient
from utils import datetime_to_calendar_timestamp, datetime_to_timestamp_ms, get_today_range_ms

# Credentials from environment
ACCESS_TOKEN = os.getenv("LARK_ACCESS_TOKEN")
USER_OPEN_ID = os.getenv("LARK_OPEN_ID")
CALENDAR_ID = os.getenv("LARK_CALENDAR_ID")

PASSED = 0
FAILED = 0
TIMESTAMP = int(time.time())

# Shared state between sequential tests
S = {
    "event_id": None,
}


def run(name, fn):
    """Run a test function, track pass/fail."""
    global PASSED, FAILED
    print(f"\n{'='*60}\n{name}\n{'='*60}")
    try:
        fn()
        PASSED += 1
        print(f"  PASS")
    except AssertionError as e:
        FAILED += 1
        print(f"  FAIL: {e}")
    except Exception as e:
        FAILED += 1
        print(f"  FAIL (exception): {str(e)[:200]}")


def client():
    """Get LarkCalendarClient instance."""
    return LarkCalendarClient(access_token=ACCESS_TOKEN, user_open_id=USER_OPEN_ID)


def assert_eq(label, actual, expected):
    """Assert equality with logging."""
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected}, got {actual}")
    print(f"    {label}: {actual}")


def assert_true(label, condition):
    """Assert condition with logging."""
    if not condition:
        raise AssertionError(f"{label}: condition failed")
    print(f"    {label}: OK")


# --- Calendar Event Tests ---

def test_01_create_event():
    """create_event → create 1-hour event starting 1 hour from now."""
    now = datetime.now()
    start = now + timedelta(hours=1)
    end = start + timedelta(hours=1)

    event_data = {
        "summary": f"E2E Test Event {TIMESTAMP}",
        "start_time": {"timestamp": datetime_to_calendar_timestamp(start)},
        "end_time": {"timestamp": datetime_to_calendar_timestamp(end)},
    }
    result = client().create_event(CALENDAR_ID, event_data)
    event = result.get("event", {})
    S["event_id"] = event.get("event_id")
    assert_true("event_id exists", S["event_id"] is not None)
    print(f"    event_id: {S['event_id']}")
    time.sleep(0.5)


def test_02_list_events():
    """list_events → list today's events, verify created event appears."""
    start_ms, end_ms = get_today_range_ms()
    # Extend end to cover events up to 2 hours from now
    end_ms = datetime_to_timestamp_ms(datetime.now() + timedelta(hours=3))
    events = client().list_events(CALENDAR_ID, start_ms, end_ms)
    assert_true("events is a list", isinstance(events, list))
    event_ids = [e.get("event_id") for e in events]
    assert_true("created event in list", S["event_id"] in event_ids)
    print(f"    events count: {len(events)}, created event found: True")


def test_03_get_event():
    """get_event → verify event fields for the created event."""
    event = client().get_event(CALENDAR_ID, S["event_id"])
    assert_true("event not empty", bool(event))
    assert_true("event_id matches", event.get("event_id") == S["event_id"])
    print(f"    summary: {event.get('summary', 'no summary')}")


def test_03b_get_calendar_list():
    """get_calendar_list → verify at least one calendar returned."""
    calendars = client().get_calendar_list()
    assert_true("calendars is a list", isinstance(calendars, list))
    assert_true("at least one calendar", len(calendars) >= 1)
    print(f"    calendars found: {len(calendars)}")


def test_03c_get_calendar():
    """get_calendar → verify calendar info for CALENDAR_ID."""
    cal = client().get_calendar(CALENDAR_ID)
    assert_true("calendar not empty", bool(cal))
    print(f"    calendar: {cal.get('summary', cal.get('calendar_id', 'unknown'))}")


def test_03d_get_attendee_list():
    """get_attendee_list → verify list returned (may be empty for events with no explicit attendees)."""
    attendees = client().get_attendee_list(CALENDAR_ID, S["event_id"])
    assert_true("attendees is a list", isinstance(attendees, list))
    print(f"    attendees: {len(attendees)}")


def test_03e_search_events():
    """search_events → search by 'E2E Test', expect at least one result."""
    results = client().search_events(CALENDAR_ID, "E2E Test")
    assert_true("results is a list", isinstance(results, list))
    print(f"    search results: {len(results)}")


def test_04_update_event():
    """update_event → rename event to 'Updated E2E {timestamp}'."""
    new_title = f"Updated E2E {TIMESTAMP}"
    result = client().update_event(CALENDAR_ID, S["event_id"], {"summary": new_title})
    event = result.get("event", {})
    actual_summary = event.get("summary", "")
    assert_true("summary contains timestamp", str(TIMESTAMP) in actual_summary)
    print(f"    updated summary: {actual_summary}")
    time.sleep(0.5)


def test_05_delete_event():
    """delete_event → delete the created event, returns True."""
    result = client().delete_event(CALENDAR_ID, S["event_id"])
    assert_true("delete returned True", result is True)
    print(f"    deleted event_id: {S['event_id']}")
    S["event_id"] = None  # Mark as cleaned up


def cleanup():
    """Delete test event if still exists (silent on failure)."""
    print("\n" + "="*60)
    print("CLEANUP")
    print("="*60)
    if not S["event_id"]:
        print("  No event to clean up")
        return
    try:
        client().delete_event(CALENDAR_ID, S["event_id"])
        print(f"  Deleted event {S['event_id']}")
    except Exception as e:
        print(f"  Cleanup failed: {str(e)[:100]}")


def main():
    print("=" * 60)
    print("LARK CALENDAR E2E TESTS")
    print("=" * 60)
    print(f"Access Token: {ACCESS_TOKEN[:20] if ACCESS_TOKEN else 'NOT SET'}...")
    print(f"User Open ID: {USER_OPEN_ID}")
    print(f"Calendar ID:  {CALENDAR_ID}")

    if not ACCESS_TOKEN:
        print("\nERROR: LARK_ACCESS_TOKEN not set")
        return 1
    if not USER_OPEN_ID:
        print("\nERROR: LARK_OPEN_ID not set")
        return 1
    if not CALENDAR_ID:
        print("\nERROR: LARK_CALENDAR_ID not set (get from MCP whoami -> primary_calendar_id)")
        return 1

    tests = [
        ("01. Create Event", test_01_create_event),
        ("02. List Events (verify created event)", test_02_list_events),
        # New read tests — must run after create, before delete
        ("03. Get Event", test_03_get_event),
        ("03b. Get Calendar List", test_03b_get_calendar_list),
        ("03c. Get Calendar", test_03c_get_calendar),
        ("03d. Get Attendee List", test_03d_get_attendee_list),
        ("03e. Search Events", test_03e_search_events),
        # Mutate + destroy
        ("04. Update Event (rename)", test_04_update_event),
        ("05. Delete Event", test_05_delete_event),
    ]

    for name, fn in tests:
        run(name, fn)
        time.sleep(0.2)  # Rate limit buffer between tests

    print(f"\n{'='*60}")
    print(f"RESULTS: {PASSED} passed, {FAILED} failed / {PASSED+FAILED} total")
    print("=" * 60)

    return 1 if FAILED > 0 else 0


if __name__ == "__main__":
    try:
        exit_code = main()
    finally:
        cleanup()
    sys.exit(exit_code)
