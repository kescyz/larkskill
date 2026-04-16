#!/usr/bin/env python3
"""E2E tests for lark-contacts API client against live Lark Contact API.
Uses tenant_access_token for most operations.

Note: search_users requires user_access_token (LARK_ACCESS_TOKEN env var).
Skipped (too destructive for automated tests):
  - create_user / update_user / delete_user: affect real org members
  - create_department / delete_department: affect org structure
"""

import sys
import os
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lark_api import LarkContactsClient

# Credentials from environment
TENANT_TOKEN = os.getenv("TENANT_TOKEN") or os.getenv("LARK_TENANT_TOKEN")
USER_OPEN_ID = os.getenv("USER_OPEN_ID")
USER_EMAIL = os.getenv("USER_EMAIL") or os.getenv("TEST_EMAIL")
# search_users requires user_access_token (different from tenant token)
USER_ACCESS_TOKEN = os.getenv("LARK_ACCESS_TOKEN")

PASSED = 0
FAILED = 0
STATE = {"first_group_id": None, "child_dept_id": None}


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
        print(f"  FAIL (exception): {str(e)[:120]}")


def test_1_get_user():
    """Get own profile by open_id, verify rich fields."""
    client = LarkContactsClient(TENANT_TOKEN, USER_OPEN_ID)
    user = client.get_user(USER_OPEN_ID)
    assert user, "get_user returned empty"
    assert user.get("open_id") == USER_OPEN_ID, f"open_id mismatch: {user.get('open_id')}"
    assert user.get("name"), "missing name"
    # Verify rich fields beyond MCP's 11
    rich = [f for f in ["city", "join_time", "employee_type", "status", "gender", "country"]
            if f in user]
    print(f"  User: {user.get('name')} | Rich fields: {rich}")


def test_2_list_department_members():
    """List users in root department."""
    client = LarkContactsClient(TENANT_TOKEN, USER_OPEN_ID)
    members = client.list_department_members("0", page_size=10)
    assert isinstance(members, list), "expected list"
    assert len(members) > 0, "no members in root dept"
    print(f"  Found {len(members)} members. First: {members[0].get('name')}")


def test_3_batch_resolve_ids():
    """Resolve known email to open_id."""
    if not USER_EMAIL:
        print("  SKIP (USER_EMAIL not set)")
        return
    client = LarkContactsClient(TENANT_TOKEN, USER_OPEN_ID)
    result = client.batch_resolve_ids(emails=[USER_EMAIL])
    user_list = result.get("user_list", [])
    assert user_list, "no users resolved"
    resolved = user_list[0]
    print(f"  {resolved.get('email')} -> {resolved.get('user_id')}")


def test_4_get_user_by_email():
    """Email -> full profile convenience method."""
    if not USER_EMAIL:
        print("  SKIP (USER_EMAIL not set)")
        return
    client = LarkContactsClient(TENANT_TOKEN, USER_OPEN_ID)
    user = client.get_user_by_email(USER_EMAIL)
    assert user, "get_user_by_email returned None"
    assert user.get("name"), "missing name in full profile"
    print(f"  {USER_EMAIL} -> {user.get('name')} ({user.get('open_id')})")


def test_5_get_department():
    """Get root department info."""
    client = LarkContactsClient(TENANT_TOKEN, USER_OPEN_ID)
    dept = client.get_department("0")
    assert dept, "get_department returned empty"
    print(f"  Root dept: {dept.get('name')} | Members: {dept.get('member_count', 'N/A')}")


def test_6_get_org_chart():
    """List top-level departments."""
    client = LarkContactsClient(TENANT_TOKEN, USER_OPEN_ID)
    depts = client.get_org_chart("0", fetch_child=False)
    assert isinstance(depts, list), "expected list"
    if depts:
        STATE["child_dept_id"] = depts[0].get("open_department_id")
        print(f"  {len(depts)} top-level depts. First: {depts[0].get('name')}")
    else:
        print(f"  0 sub-departments (flat org)")


def test_7_get_department_path():
    """Get ancestor chain of a known dept."""
    dept_id = STATE.get("child_dept_id")
    if not dept_id:
        print("  SKIP (no child dept from test_6)")
        return
    client = LarkContactsClient(TENANT_TOKEN, USER_OPEN_ID)
    path = client.get_department_path(dept_id, id_type="open_department_id")
    assert isinstance(path, list), "expected list"
    names = [d.get("name") for d in path]
    print(f"  Path ({len(path)} ancestors): {' -> '.join(names)}")


def test_8_list_groups():
    """List all user groups."""
    client = LarkContactsClient(TENANT_TOKEN, USER_OPEN_ID)
    groups = client.list_groups()
    assert isinstance(groups, list), "expected list"
    if groups:
        STATE["first_group_id"] = groups[0].get("id")
        print(f"  {len(groups)} groups. First: {groups[0].get('name')}")
    else:
        print(f"  0 groups (none in org)")


def test_9_get_group_and_members():
    """Get group detail + list members."""
    gid = STATE.get("first_group_id")
    if not gid:
        print("  SKIP (no groups from test_8)")
        return
    client = LarkContactsClient(TENANT_TOKEN, USER_OPEN_ID)
    group = client.get_group(gid)
    assert group, "get_group returned empty"
    members = client.list_group_members(gid)
    assert isinstance(members, list), "expected list"
    print(f"  Group '{group.get('name')}': {len(members)} members")


def test_10b_search_users():
    """search_users removed from contacts skill — use MCP search_users instead.
    This test is a no-op placeholder."""
    print("  SKIP (search_users moved to lark-token-manager MCP — no API scope needed)")


def test_10_get_user_invalid_id():
    """Invalid user ID should raise."""
    client = LarkContactsClient(TENANT_TOKEN, USER_OPEN_ID)
    try:
        client.get_user("invalid_open_id_xxx")
        raise AssertionError("Should have raised exception")
    except Exception as e:
        if "invalid_open_id_xxx" in str(e).lower() or "error" in str(e).lower() or "Lark API" in str(e):
            print(f"  Correctly raised: {str(e)[:80]}")
        else:
            raise


def main():
    print("=" * 60)
    print("LARK CONTACTS E2E TESTS")
    print("=" * 60)
    print(f"Tenant Token: {TENANT_TOKEN[:20] if TENANT_TOKEN else 'NOT SET'}...")
    print(f"User Open ID: {USER_OPEN_ID}")
    print(f"User Email:   {USER_EMAIL or 'NOT SET'}")

    if not TENANT_TOKEN:
        print("\nERROR: TENANT_TOKEN not set")
        return 1
    if not USER_OPEN_ID:
        print("\nERROR: USER_OPEN_ID not set")
        return 1

    tests = [
        ("1. Get User (own profile)", test_1_get_user),
        ("2. List Department Members", test_2_list_department_members),
        ("3. Batch Resolve IDs", test_3_batch_resolve_ids),
        ("4. Get User by Email", test_4_get_user_by_email),
        ("5. Get Department", test_5_get_department),
        ("6. Get Org Chart", test_6_get_org_chart),
        ("7. Get Department Path", test_7_get_department_path),
        ("8. List Groups", test_8_list_groups),
        ("9. Get Group + Members", test_9_get_group_and_members),
        ("10b. Search Users", test_10b_search_users),
        ("10. Invalid User ID", test_10_get_user_invalid_id),
    ]

    for name, fn in tests:
        run(name, fn)
        time.sleep(1)

    print(f"\n{'='*60}")
    print(f"RESULTS: {PASSED} passed, {FAILED} failed / {PASSED+FAILED} total")
    print("=" * 60)
    return 1 if FAILED > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
