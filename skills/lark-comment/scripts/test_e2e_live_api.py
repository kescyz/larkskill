#!/usr/bin/env python3
"""E2E tests for lark-comment skill — live API, no mocks, sequential CRUD roundtrips.

Tests all 4 Comment methods:
  - add_comment(file_token, file_type, content)
  - list_comments(file_token, file_type)
  - add_reply(file_token, file_type, comment_id, content)
  - solve_comment(file_token, file_type, comment_id, is_solved=True)

Env vars required:
  LARK_ACCESS_TOKEN  — user OAuth token
  LARK_OPEN_ID       — user open_id (ou_...)
  LARK_FILE_TOKEN    — docx/doc/sheet file token to comment on
  LARK_FILE_TYPE     — file type: doc | docx | sheet | file (default: docx)
"""

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lark_api import LarkCommentClient

# Credentials from environment
ACCESS_TOKEN = os.getenv("LARK_ACCESS_TOKEN")
USER_OPEN_ID = os.getenv("LARK_OPEN_ID")
FILE_TOKEN = os.getenv("LARK_FILE_TOKEN")
FILE_TYPE = os.getenv("LARK_FILE_TYPE", "docx")

PASSED = 0
FAILED = 0
TIMESTAMP = int(time.time())

# Shared state between sequential tests
S = {
    "comment_id": None,
    "reply_id": None,
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
    """Get LarkCommentClient instance."""
    return LarkCommentClient(access_token=ACCESS_TOKEN, user_open_id=USER_OPEN_ID)


def assert_true(label, condition):
    """Assert condition with logging."""
    if not condition:
        raise AssertionError(f"{label}: condition failed")
    print(f"    {label}: OK")


# --- Comment Tests ---

def test_01_add_comment():
    """add_comment → add global comment to the test file."""
    result = client().add_comment(
        file_token=FILE_TOKEN,
        file_type=FILE_TYPE,
        content=f"E2E Test Comment {TIMESTAMP}"
    )
    assert result, "add_comment returned empty"
    S["comment_id"] = result.get("comment_id")
    assert_true("comment_id exists", bool(S["comment_id"]))
    print(f"    comment_id: {S['comment_id']}")
    time.sleep(0.5)


def test_02_list_comments():
    """list_comments → verify created comment appears in list."""
    comments = client().list_comments(
        file_token=FILE_TOKEN,
        file_type=FILE_TYPE
    )
    assert_true("comments is a list", isinstance(comments, list))
    assert_true("at least one comment", len(comments) >= 1)
    ids = [c.get("comment_id") for c in comments]
    assert_true("created comment in list", S["comment_id"] in ids)
    print(f"    comments found: {len(comments)}, created comment found: True")


def test_03_add_reply():
    """add_reply → add a reply to the created comment thread."""
    result = client().add_reply(
        file_token=FILE_TOKEN,
        file_type=FILE_TYPE,
        comment_id=S["comment_id"],
        content=f"E2E Test Reply {TIMESTAMP}"
    )
    assert result, "add_reply returned empty"
    S["reply_id"] = result.get("reply_id")
    assert_true("reply_id exists", bool(S["reply_id"]))
    print(f"    reply_id: {S['reply_id']}")
    time.sleep(0.5)


def test_04_solve_comment():
    """solve_comment → mark the comment as resolved, returns True."""
    result = client().solve_comment(
        file_token=FILE_TOKEN,
        file_type=FILE_TYPE,
        comment_id=S["comment_id"],
        is_solved=True
    )
    assert_true("solve_comment returned True", result is True)
    print(f"    solved comment_id: {S['comment_id']}")


def main():
    print("=" * 60)
    print("LARK COMMENT E2E TESTS")
    print("=" * 60)
    print(f"Access Token: {ACCESS_TOKEN[:20] if ACCESS_TOKEN else 'NOT SET'}...")
    print(f"User Open ID: {USER_OPEN_ID}")
    print(f"File Token:   {FILE_TOKEN}")
    print(f"File Type:    {FILE_TYPE}")

    if not ACCESS_TOKEN:
        print("\nERROR: LARK_ACCESS_TOKEN not set")
        return 1
    if not USER_OPEN_ID:
        print("\nERROR: LARK_OPEN_ID not set")
        return 1
    if not FILE_TOKEN:
        print("\nERROR: LARK_FILE_TOKEN not set (provide a docx/doc/sheet file token)")
        return 1

    tests = [
        ("01. Add Comment", test_01_add_comment),
        ("02. List Comments (verify created)", test_02_list_comments),
        ("03. Add Reply", test_03_add_reply),
        ("04. Solve Comment (mark resolved)", test_04_solve_comment),
    ]

    for name, fn in tests:
        run(name, fn)
        time.sleep(0.2)  # Rate limit buffer between tests

    print(f"\n{'='*60}")
    print(f"RESULTS: {PASSED} passed, {FAILED} failed / {PASSED+FAILED} total")
    print("=" * 60)

    return 1 if FAILED > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
