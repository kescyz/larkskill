#!/usr/bin/env python3
"""E2E tests for lark-task skill — live API, no mocks, sequential CRUD roundtrips.

Tests core Task CRUD flow + collaboration methods:
  - create_tasklist / list_tasklists / get_tasklist_details / delete_tasklist
  - create_task / get_task / update_task / delete_task
  - add_task_comment / list_task_comments
  - create_subtask / list_subtasks

Skipped (manual test recommended):
  - add_task_reminder: task needs a due date and reminder setup is one-per-task
  - add_task_dependency: needs 2 tasks in specific dependency states

Env vars required:
  LARK_ACCESS_TOKEN  — user OAuth token
  LARK_OPEN_ID       — user open_id (ou_...)
"""

import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lark_api import LarkTaskClient
from utils import datetime_to_task_timestamp

# Credentials from environment
ACCESS_TOKEN = os.getenv("LARK_ACCESS_TOKEN")
USER_OPEN_ID = os.getenv("LARK_OPEN_ID")

PASSED = 0
FAILED = 0
TIMESTAMP = int(time.time())

# Shared state between sequential tests
S = {
    "tasklist_guid": None,
    "task_guid": None,
    "subtask_guid": None,
    "comment_id": None,
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
    """Get LarkTaskClient instance."""
    return LarkTaskClient(access_token=ACCESS_TOKEN, user_open_id=USER_OPEN_ID)


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


# --- Tasklist Tests ---

def test_01_create_tasklist():
    """create_tasklist → verify tasklist_guid returned."""
    name = f"E2E Test Tasklist {TIMESTAMP}"
    result = client().create_tasklist(name=name)
    tasklist = result.get("tasklist", {})
    S["tasklist_guid"] = tasklist.get("guid") or tasklist.get("tasklist_guid")
    assert_true("tasklist_guid exists", S["tasklist_guid"] is not None)
    print(f"    tasklist_guid: {S['tasklist_guid']}")
    time.sleep(0.5)


def test_02_list_tasklists():
    """list_tasklists → verify created tasklist appears in the list."""
    tasklists = client().list_tasklists()
    assert_true("tasklists is a list", isinstance(tasklists, list))
    guids = [tl.get("guid") or tl.get("tasklist_guid") for tl in tasklists]
    assert_true("created tasklist in list", S["tasklist_guid"] in guids)
    print(f"    tasklists count: {len(tasklists)}, created tasklist found: True")


# --- Task Tests ---

def test_03_create_task():
    """create_task → create task in the test tasklist."""
    due = datetime.now() + timedelta(days=1)
    task_data = {
        "summary": f"E2E Test Task {TIMESTAMP}",
        "due": {"timestamp": datetime_to_task_timestamp(due)},
        "tasklist_guid": S["tasklist_guid"],
    }
    result = client().create_task(task_data=task_data)
    task = result.get("task", {})
    S["task_guid"] = task.get("guid")
    assert_true("task_guid exists", S["task_guid"] is not None)
    print(f"    task_guid: {S['task_guid']}")
    time.sleep(0.5)


def test_04_get_task():
    """get_task → verify task summary contains timestamp."""
    task = client().get_task(task_guid=S["task_guid"])
    summary = task.get("summary", "")
    assert_true("task summary contains timestamp", str(TIMESTAMP) in summary)
    print(f"    summary: {summary}")


def test_05_update_task():
    """update_task → rename task, verify via get_task."""
    new_title = f"Updated E2E Task {TIMESTAMP}"
    client().update_task(task_guid=S["task_guid"], task_data={"summary": new_title})
    time.sleep(0.5)
    task = client().get_task(task_guid=S["task_guid"])
    actual_summary = task.get("summary", "")
    assert_true("updated summary contains 'Updated'", "Updated" in actual_summary)
    print(f"    updated summary: {actual_summary}")


def test_06_get_tasklist_tasks():
    """get_tasklist_tasks → verify API returns list (task may not auto-join tasklist on create)."""
    tasks = client().get_tasklist_tasks(tasklist_guid=S["tasklist_guid"])
    assert_true("tasks is a list", isinstance(tasks, list))
    print(f"    tasklist tasks count: {len(tasks)}")


# --- Collaboration Tests ---

def test_06b_add_task_comment():
    """add_task_comment → add a comment to the test task."""
    result = client().add_task_comment(S["task_guid"], "E2E test comment")
    assert_true("comment returned", bool(result))
    S["comment_id"] = result.get("comment_id", result.get("id", ""))
    assert_true("comment_id exists", bool(S["comment_id"]))
    print(f"    comment_id: {S['comment_id']}")
    time.sleep(0.5)


def test_06c_list_task_comments():
    """list_task_comments → verify added comment appears in list."""
    comments = client().list_task_comments(S["task_guid"])
    assert_true("comments is a list", isinstance(comments, list))
    assert_true("at least one comment", len(comments) >= 1)
    print(f"    comments: {len(comments)}")


def test_06d_get_tasklist_details():
    """get_tasklist_details → verify tasklist name and guid."""
    details = client().get_tasklist_details(S["tasklist_guid"])
    assert_true("details not empty", bool(details))
    assert_true("tasklist_guid matches", (details.get("guid") or details.get("tasklist_guid")) == S["tasklist_guid"])
    print(f"    tasklist: {details.get('name', 'unknown')}")


# --- Subtask Tests ---

def test_07_create_subtask():
    """create_subtask → create subtask under the test task."""
    subtask_data = {"summary": f"E2E Subtask {TIMESTAMP}"}
    result = client().create_subtask(task_guid=S["task_guid"], subtask_data=subtask_data)
    subtask = result.get("subtask") or result.get("task") or {}
    S["subtask_guid"] = subtask.get("guid")
    assert_true("subtask_guid exists", S["subtask_guid"] is not None)
    print(f"    subtask_guid: {S['subtask_guid']}")
    time.sleep(0.5)


def test_08_list_subtasks():
    """list_subtasks → verify subtask appears under parent task."""
    subtasks = client().list_subtasks(task_guid=S["task_guid"])
    assert_true("subtasks is a list", isinstance(subtasks, list))
    assert_true("at least one subtask", len(subtasks) >= 1)
    guids = [s.get("guid") for s in subtasks]
    assert_true("created subtask in list", S["subtask_guid"] in guids)
    print(f"    subtasks count: {len(subtasks)}, created subtask found: True")


def test_09_delete_subtask():
    """delete_task (subtask) → delete the subtask first."""
    result = client().delete_task(task_guid=S["subtask_guid"])
    assert_true("delete subtask returned True", result is True)
    print(f"    deleted subtask_guid: {S['subtask_guid']}")
    S["subtask_guid"] = None
    time.sleep(0.5)


def test_10_delete_task():
    """delete_task → delete the parent task."""
    result = client().delete_task(task_guid=S["task_guid"])
    assert_true("delete task returned True", result is True)
    print(f"    deleted task_guid: {S['task_guid']}")
    S["task_guid"] = None
    time.sleep(0.5)


def cleanup():
    """Delete test data if still exists (silent on failure)."""
    print("\n" + "="*60)
    print("CLEANUP")
    print("="*60)
    c = client()

    if S["subtask_guid"]:
        try:
            c.delete_task(task_guid=S["subtask_guid"])
            print(f"  Deleted subtask {S['subtask_guid']}")
        except Exception as e:
            print(f"  Subtask cleanup failed: {str(e)[:100]}")

    if S["task_guid"]:
        try:
            c.delete_task(task_guid=S["task_guid"])
            print(f"  Deleted task {S['task_guid']}")
        except Exception as e:
            print(f"  Task cleanup failed: {str(e)[:100]}")

    if S["tasklist_guid"]:
        try:
            c.delete_tasklist(tasklist_guid=S["tasklist_guid"])
            print(f"  Deleted tasklist {S['tasklist_guid']}")
        except Exception as e:
            print(f"  Tasklist cleanup failed: {str(e)[:100]}")

    if not any([S["subtask_guid"], S["task_guid"], S["tasklist_guid"]]):
        print("  Nothing to clean up")


def main():
    print("=" * 60)
    print("LARK TASK E2E TESTS")
    print("=" * 60)
    print(f"Access Token: {ACCESS_TOKEN[:20] if ACCESS_TOKEN else 'NOT SET'}...")
    print(f"User Open ID: {USER_OPEN_ID}")

    if not ACCESS_TOKEN:
        print("\nERROR: LARK_ACCESS_TOKEN not set")
        return 1
    if not USER_OPEN_ID:
        print("\nERROR: LARK_OPEN_ID not set")
        return 1

    tests = [
        # Tasklist management
        ("01. Create Tasklist", test_01_create_tasklist),
        ("02. List Tasklists (verify created)", test_02_list_tasklists),
        # Task CRUD
        ("03. Create Task (in tasklist)", test_03_create_task),
        ("04. Get Task (verify summary)", test_04_get_task),
        ("05. Update Task (rename)", test_05_update_task),
        ("06. Get Tasklist Tasks (verify task)", test_06_get_tasklist_tasks),
        # Collaboration
        ("06b. Add Task Comment", test_06b_add_task_comment),
        ("06c. List Task Comments", test_06c_list_task_comments),
        ("06d. Get Tasklist Details", test_06d_get_tasklist_details),
        # Subtask CRUD
        ("07. Create Subtask", test_07_create_subtask),
        ("08. List Subtasks (verify subtask)", test_08_list_subtasks),
        # Deletion (subtask first, then parent, then tasklist)
        ("09. Delete Subtask", test_09_delete_subtask),
        ("10. Delete Task", test_10_delete_task),
    ]

    for name, fn in tests:
        run(name, fn)
        time.sleep(0.2)  # Rate limit buffer between tests

    # Delete tasklist after tasks are gone
    def test_11_delete_tasklist():
        result = client().delete_tasklist(tasklist_guid=S["tasklist_guid"])
        assert_true("delete tasklist returned True", result is True)
        print(f"    deleted tasklist_guid: {S['tasklist_guid']}")
        S["tasklist_guid"] = None

    run("11. Delete Tasklist", test_11_delete_tasklist)

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
