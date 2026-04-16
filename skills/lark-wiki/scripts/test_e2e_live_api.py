#!/usr/bin/env python3
"""E2E tests for lark-wiki skill — live API, no mocks, sequential CRUD roundtrips.

Tests 13 Wiki methods (skips move_docs_to_wiki + get_task for MVP):
  - Space ops (4): list_spaces, get_space, create_space, update_space_setting
  - Node ops (6): create_node, get_node, list_nodes, move_node, copy_node, update_title
  - Member ops (3): add_member, delete_member, search_wiki
"""

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lark_api import LarkWikiClient

# Credentials from environment
ACCESS_TOKEN = os.getenv("LARK_ACCESS_TOKEN")
USER_OPEN_ID = os.getenv("LARK_OPEN_ID")
TEST_USER_OPENID = os.getenv("LARK_TEST_USER_OPENID")
WIKI_SPACE_ID = os.getenv("LARK_WIKI_SPACE_ID")

PASSED = 0
FAILED = 0
TIMESTAMP = int(time.time())

# Shared state between sequential tests
S = {
    "space_id": None,
    "node_token": None,
    "node_token_2": None,
    "copied_node_token": None,
    "moved_node_token": None,
    "list_spaces_result": None,
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
    """Get LarkWikiClient instance."""
    return LarkWikiClient(access_token=ACCESS_TOKEN, user_open_id=USER_OPEN_ID)


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


# --- Space tests ---

def test_01_list_spaces():
    """test_list_spaces → list spaces, assert returns list."""
    result = client().list_spaces()
    items = result.get("items", [])
    assert_true("items is list", isinstance(items, list))
    S["list_spaces_result"] = result
    print(f"    Found {len(items)} spaces")


def test_02_get_space():
    """test_get_space → get first space from list, assert space_id."""
    # Use provided space ID or get first from list
    if WIKI_SPACE_ID:
        space_id = WIKI_SPACE_ID
    else:
        items = S["list_spaces_result"].get("items", [])
        if not items:
            print("    SKIP: No spaces available")
            return
        space_id = items[0].get("space_id")

    result = client().get_space(space_id=space_id)
    assert_true("space_id exists", result.get("space_id") == space_id)
    print(f"    Space name: {result.get('name', 'N/A')}")


def test_03_create_space():
    """test_create_space → create test space, track for later (no delete API for spaces)."""
    time.sleep(0.5)  # rate limit
    space_name = f"E2E Test Space {TIMESTAMP}"
    result = client().create_space(name=space_name)
    S["space_id"] = result.get("space_id")
    assert_true("space_id exists", S["space_id"] is not None)
    print(f"    Created space: {S['space_id']}")


def test_04_update_space_setting():
    """test_update_space_setting → update create_setting on test space."""
    time.sleep(0.5)  # rate limit
    result = client().update_space_setting(
        space_id=S["space_id"],
        create_setting="allow"
    )
    setting = result
    assert_true("create_setting updated", setting.get("create_setting") == "allow")


# --- Node tests ---

def test_05_create_node():
    """test_create_node → create docx node in test space root."""
    time.sleep(0.5)  # rate limit
    node_title = f"E2E Test Node {TIMESTAMP}"
    result = client().create_node(
        space_id=S["space_id"],
        obj_type="docx",
        title=node_title
    )
    S["node_token"] = result.get("node_token")
    assert_true("node_token exists", S["node_token"] is not None)
    print(f"    Created node: {S['node_token']}")


def test_06_get_node():
    """test_get_node → get created node, assert obj_type."""
    time.sleep(0.5)  # rate limit
    result = client().get_node(token=S["node_token"])
    assert_true("node_token matches", result.get("node_token") == S["node_token"])
    assert_eq("obj_type is docx", result.get("obj_type"), "docx")


def test_07_list_nodes():
    """test_list_nodes → list nodes in space, assert returns list."""
    time.sleep(0.5)  # rate limit
    result = client().list_nodes(space_id=S["space_id"])
    items = result.get("items", [])
    assert_true("items is list", isinstance(items, list))
    print(f"    Found {len(items)} nodes in space")


def test_08_update_title():
    """test_update_title → rename node."""
    time.sleep(0.5)  # rate limit
    new_title = f"E2E Test Node Updated {TIMESTAMP}"
    result = client().update_title(
        space_id=S["space_id"],
        node_token=S["node_token"],
        title=new_title
    )
    assert_true("update_title completed", result is not None)
    # Verify by fetching
    time.sleep(0.5)
    node = client().get_node(token=S["node_token"])
    assert_eq("title updated", node.get("title"), new_title)


def test_09_copy_node():
    """test_copy_node → copy node within same space."""
    time.sleep(0.5)  # rate limit
    copy_title = f"E2E Copy {TIMESTAMP}"
    result = client().copy_node(
        space_id=S["space_id"],
        node_token=S["node_token"],
        title=copy_title
    )
    S["copied_node_token"] = result.get("node_token")
    assert_true("copied node_token exists", S["copied_node_token"] is not None)
    print(f"    Copied node: {S['copied_node_token']}")


def test_10_move_node():
    """test_move_node → move copied node."""
    time.sleep(0.5)  # rate limit
    # Create a parent node first
    parent_title = f"E2E Parent {TIMESTAMP}"
    parent_result = client().create_node(
        space_id=S["space_id"],
        obj_type="docx",
        title=parent_title
    )
    S["node_token_2"] = parent_result.get("node_token")
    time.sleep(0.5)

    # Move copied node under parent
    move_result = client().move_node(
        space_id=S["space_id"],
        node_token=S["copied_node_token"],
        target_parent_token=S["node_token_2"]
    )
    S["moved_node_token"] = S["copied_node_token"]
    assert_true("move completed", move_result is not None)


def test_11_search_wiki():
    """test_search_wiki → search by keyword (may need sleep for indexing)."""
    time.sleep(1)  # Allow indexing
    result = client().search_wiki(query=f"E2E Test {TIMESTAMP}")
    items = result.get("items", [])
    assert_true("items is list", isinstance(items, list))
    print(f"    Found {len(items)} search results")


# --- Member tests ---

def test_12_add_member():
    """test_add_member → add member using LARK_TEST_USER_OPENID."""
    if not TEST_USER_OPENID:
        print("    SKIP: No LARK_TEST_USER_OPENID")
        return

    time.sleep(0.5)  # rate limit
    result = client().add_member(
        space_id=S["space_id"],
        member_type="openid",
        member_id=TEST_USER_OPENID,
        member_role="member"
    )
    member = result
    assert_true("member added", member.get("member_id") == TEST_USER_OPENID)


def test_13_delete_member():
    """test_delete_member → remove member (requires body in DELETE)."""
    if not TEST_USER_OPENID:
        print("    SKIP: No LARK_TEST_USER_OPENID")
        return

    time.sleep(0.5)  # rate limit
    result = client().delete_member(
        space_id=S["space_id"],
        member_id=TEST_USER_OPENID,
        member_type="openid",
        member_role="member"
    )
    assert_true("member deleted", result is not None)


def main():
    print("=" * 60)
    print("LARK WIKI E2E TESTS")
    print("=" * 60)
    print(f"Access Token: {ACCESS_TOKEN[:20] if ACCESS_TOKEN else 'NOT SET'}...")
    print(f"User Open ID: {USER_OPEN_ID}")
    print(f"Test User OpenID: {TEST_USER_OPENID if TEST_USER_OPENID else 'NOT SET'}")
    print(f"Wiki Space ID (optional): {WIKI_SPACE_ID if WIKI_SPACE_ID else 'NOT SET'}")

    if not ACCESS_TOKEN:
        print("\nERROR: ACCESS_TOKEN not set")
        return 1
    if not USER_OPEN_ID:
        print("\nERROR: USER_OPEN_ID not set")
        return 1

    tests = [
        # Space (4 methods: list, get, create, update_setting)
        ("01. List Spaces", test_01_list_spaces),
        ("02. Get Space", test_02_get_space),
        ("03. Create Space", test_03_create_space),
        ("04. Update Space Setting", test_04_update_space_setting),
        # Node (6 methods: create, get, list, update_title, copy, move)
        ("05. Create Node", test_05_create_node),
        ("06. Get Node", test_06_get_node),
        ("07. List Nodes", test_07_list_nodes),
        ("08. Update Title", test_08_update_title),
        ("09. Copy Node", test_09_copy_node),
        ("10. Move Node", test_10_move_node),
        # Search (1 method: search_wiki)
        ("11. Search Wiki", test_11_search_wiki),
        # Member (2 methods: add_member, delete_member)
        ("12. Add Member", test_12_add_member),
        ("13. Delete Member", test_13_delete_member),
    ]

    for name, fn in tests:
        run(name, fn)
        # Rate limit: 5 QPS per token
        # Most tests already have time.sleep(0.5), add buffer
        time.sleep(0.2)

    print(f"\n{'='*60}")
    print(f"RESULTS: {PASSED} passed, {FAILED} failed / {PASSED+FAILED} total")
    print("=" * 60)

    # Summary
    print(f"\nMethods tested: 13/15")
    print(f"  Skipped: move_docs_to_wiki, get_task (async complexity, not in MVP)")
    print(f"\nNOTE: Wiki spaces and nodes cannot be deleted via API.")
    print(f"  Created space: {S['space_id']}")
    print(f"  Please manually clean up in Lark UI if needed.")

    return 1 if FAILED > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
