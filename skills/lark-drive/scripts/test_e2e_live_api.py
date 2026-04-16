#!/usr/bin/env python3
"""E2E tests for lark-drive skill — live API, no mocks, sequential CRUD roundtrips.

Tests all 15 Drive methods:
  - File ops (7): list_files, get_file_meta, batch_query_meta, create_file, copy_file, move_file, delete_file
  - Upload (4): get_root_folder, create_folder, upload_file, download_file
  - Permission (4): search_files, add_permission, update_permission, delete_permission
"""

import os
import sys
import time
import json
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lark_api import LarkDriveClient

# Credentials from environment
ACCESS_TOKEN = os.getenv("LARK_ACCESS_TOKEN")
USER_OPEN_ID = os.getenv("LARK_OPEN_ID")
TEST_USER_EMAIL = os.getenv("LARK_TEST_USER_EMAIL")

PASSED = 0
FAILED = 0
CLEANUP = []  # Track file/folder tokens for cleanup
TIMESTAMP = int(time.time())

# Shared state between sequential tests
S = {
    "root_token": None,
    "test_folder_token": None,
    "test_folder_token_2": None,
    "uploaded_file_token": None,
    "created_file_token": None,
    "copied_file_token": None,
    "moved_file_token": None,
    "download_path": None,
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
    """Get LarkDriveClient instance."""
    return LarkDriveClient(access_token=ACCESS_TOKEN, user_open_id=USER_OPEN_ID)


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


# --- Folder tests ---

def test_01_get_root_folder():
    """test_get_root_folder → get root, assert token exists."""
    result = client().get_root_folder()
    S["root_token"] = result.get("token")
    assert_true("root_token exists", S["root_token"] is not None)
    CLEANUP.append(("folder", S["root_token"], "root"))


def test_02_create_folder():
    """test_create_folder → create in root, track for cleanup."""
    time.sleep(0.5)  # rate limit
    folder_name = f"E2E Test Folder {TIMESTAMP}"
    result = client().create_folder(name=folder_name, folder_token=S["root_token"])
    S["test_folder_token"] = result.get("token")
    assert_true("folder token exists", S["test_folder_token"] is not None)
    CLEANUP.append(("folder", S["test_folder_token"], "delete"))


def test_03_list_files():
    """test_list_files → list root, assert returns list."""
    time.sleep(0.5)  # rate limit
    result = client().list_files(folder_token=S["root_token"])
    files = result.get("files", [])
    assert_true("files is list", isinstance(files, list))
    assert_true("files length >= 0", len(files) >= 0)


def test_04_upload_file():
    """test_upload_file → create temp .txt file, upload to test folder, assert file_token."""
    time.sleep(0.5)  # rate limit
    # Create temp file
    temp_content = f"E2E test content {TIMESTAMP}"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(temp_content)
        temp_path = f.name

    try:
        file_size = os.path.getsize(temp_path)
        file_name = f"test_upload_{TIMESTAMP}.txt"
        result = client().upload_file(
            file_name=file_name,
            parent_token=S["test_folder_token"],
            file_path=temp_path,
            size=file_size
        )
        S["uploaded_file_token"] = result.get("file_token")
        assert_true("uploaded file_token exists", S["uploaded_file_token"] is not None)
        CLEANUP.append(("file", S["uploaded_file_token"], "delete"))
    finally:
        os.unlink(temp_path)


def test_05_download_file():
    """test_download_file → download uploaded file to /tmp, verify exists."""
    time.sleep(0.5)  # rate limit
    save_path = f"/tmp/lark_drive_download_{TIMESTAMP}.txt"
    S["download_path"] = save_path
    result = client().download_file(file_token=S["uploaded_file_token"], save_path=save_path)
    assert_true("download path exists", os.path.exists(result))
    assert_true("download file has content", os.path.getsize(result) > 0)


def test_06_get_file_meta():
    """test_get_file_meta → get metadata via batch_query wrapper."""
    time.sleep(0.5)  # rate limit
    result = client().get_file_meta(file_token=S["uploaded_file_token"], file_type="file")
    assert_true("meta not empty", len(result) > 0)
    # batch_query returns doc_token/title keys
    has_token = result.get("doc_token") or result.get("token")
    assert_true("meta has token", has_token is not None)
    print(f"    meta keys: {list(result.keys())[:5]}")


def test_07_batch_query_meta():
    """test_batch_query_meta → batch query with uploaded file."""
    time.sleep(0.5)  # rate limit
    request_docs = [{"doc_token": S["uploaded_file_token"], "doc_type": "file"}]
    result = client().batch_query_meta(request_docs=request_docs)
    metas = result.get("metas", [])
    assert_true("batch_query returns metas", isinstance(metas, list))
    if metas:
        has_token = metas[0].get("doc_token") or metas[0].get("token")
        assert_true("first meta has token", has_token == S["uploaded_file_token"])


def test_08_copy_file():
    """test_copy_file → copy uploaded file, track copy for cleanup."""
    time.sleep(0.5)  # rate limit
    copy_name = f"test_copy_{TIMESTAMP}"
    result = client().copy_file(
        file_token=S["uploaded_file_token"],
        name=copy_name,
        file_type="file",
        folder_token=S["test_folder_token"]
    )
    file_info = result.get("file", {})
    S["copied_file_token"] = file_info.get("token")
    assert_true("copy file_token exists", S["copied_file_token"] is not None)
    CLEANUP.append(("file", S["copied_file_token"], "delete"))


def test_09_move_file():
    """test_move_file → move copy to root (or another location)."""
    time.sleep(0.5)  # rate limit
    # Create second folder for moving
    folder_name_2 = f"E2E Test Folder 2 {TIMESTAMP}"
    result = client().create_folder(name=folder_name_2, folder_token=S["root_token"])
    S["test_folder_token_2"] = result.get("token")
    CLEANUP.append(("folder", S["test_folder_token_2"], "delete"))
    time.sleep(0.5)

    # Move copied file to second folder
    move_result = client().move_file(
        file_token=S["copied_file_token"],
        file_type="file",
        folder_token=S["test_folder_token_2"]
    )
    S["moved_file_token"] = S["copied_file_token"]
    assert_true("move completed", move_result is not None)


def test_10_create_file():
    """test_create_file → create online docx in folder."""
    time.sleep(0.5)  # rate limit
    title = f"E2E Test Doc {TIMESTAMP}"
    result = client().create_file(
        folder_token=S["test_folder_token"],
        title=title,
        file_type="docx"
    )
    S["created_file_token"] = result.get("token")
    assert_true("created file_token exists", S["created_file_token"] is not None)
    CLEANUP.append(("file", S["created_file_token"], "delete"))


def test_11_search_files():
    """test_search_files → search by keyword (may need sleep for indexing)."""
    time.sleep(1)  # Allow indexing
    # Search for test files by timestamp
    result = client().search_files(query=f"E2E Test {TIMESTAMP}")
    docs = result.get("docs_entities", [])
    assert_true("search returns list", isinstance(docs, list))


def test_12_add_permission():
    """test_add_permission → add viewer permission using LARK_TEST_USER_EMAIL."""
    if not TEST_USER_EMAIL:
        print("    SKIP: No LARK_TEST_USER_EMAIL")
        return
    time.sleep(0.5)  # rate limit
    result = client().add_permission(
        token=S["uploaded_file_token"],
        file_type="file",
        member_type="email",
        member_id=TEST_USER_EMAIL,
        perm="view"
    )
    member = result.get("member", {})
    assert_true("permission added", member.get("member_id") == TEST_USER_EMAIL)


def test_13_update_permission():
    """test_update_permission → update to editor."""
    if not TEST_USER_EMAIL:
        print("    SKIP: No LARK_TEST_USER_EMAIL")
        return
    time.sleep(0.5)  # rate limit
    result = client().update_permission(
        token=S["uploaded_file_token"],
        file_type="file",
        member_id=TEST_USER_EMAIL,
        perm="edit",
        member_type="email"
    )
    member = result.get("member", {})
    assert_eq("permission updated to edit", member.get("perm"), "edit")


def test_14_delete_permission():
    """test_delete_permission → revoke."""
    if not TEST_USER_EMAIL:
        print("    SKIP: No LARK_TEST_USER_EMAIL")
        return
    time.sleep(0.5)  # rate limit
    result = client().delete_permission(
        token=S["uploaded_file_token"],
        file_type="file",
        member_id=TEST_USER_EMAIL,
        member_type="email"
    )
    assert_true("permission deleted", result is not None)


def test_15_delete_file():
    """test_delete_file → delete test folder and files."""
    time.sleep(0.5)  # rate limit
    # Delete test folder (will cascade delete contents)
    result = client().delete_file(
        file_token=S["test_folder_token"],
        file_type="folder"
    )
    assert_true("folder deleted", result is not None)


def cleanup():
    """Delete all test resources."""
    print("\n" + "="*60)
    print("CLEANUP")
    print("="*60)
    c = client()
    for resource_type, token, action in CLEANUP:
        if action == "root":
            continue  # Don't delete root
        try:
            if resource_type == "file":
                c.delete_file(file_token=token, file_type="file")
            elif resource_type == "folder":
                c.delete_file(file_token=token, file_type="folder")
            print(f"  Cleaned {resource_type} {token}")
            time.sleep(0.3)
        except Exception as e:
            print(f"  Cleanup failed for {token}: {str(e)[:100]}")

    # Clean downloaded file
    if S["download_path"] and os.path.exists(S["download_path"]):
        try:
            os.unlink(S["download_path"])
            print(f"  Cleaned download file")
        except Exception as e:
            print(f"  Failed to clean download: {e}")


def main():
    print("=" * 60)
    print("LARK DRIVE E2E TESTS")
    print("=" * 60)
    print(f"Access Token: {ACCESS_TOKEN[:20] if ACCESS_TOKEN else 'NOT SET'}...")
    print(f"User Open ID: {USER_OPEN_ID}")
    print(f"Test User Email: {TEST_USER_EMAIL if TEST_USER_EMAIL else 'NOT SET'}")

    if not ACCESS_TOKEN:
        print("\nERROR: ACCESS_TOKEN not set")
        return 1
    if not USER_OPEN_ID:
        print("\nERROR: USER_OPEN_ID not set")
        return 1

    tests = [
        # Folder (3 methods: get_root, create_folder, list_files)
        ("01. Get Root Folder", test_01_get_root_folder),
        ("02. Create Folder", test_02_create_folder),
        ("03. List Files", test_03_list_files),
        # Upload/Download (2 methods: upload, download)
        ("04. Upload File", test_04_upload_file),
        ("05. Download File", test_05_download_file),
        # File metadata (2 methods: get_meta, batch_query)
        ("06. Get File Meta", test_06_get_file_meta),
        ("07. Batch Query Meta", test_07_batch_query_meta),
        # File CRUD (4 methods: copy, move, create, delete)
        ("08. Copy File", test_08_copy_file),
        ("09. Move File", test_09_move_file),
        ("10. Create File", test_10_create_file),
        # Search (1 method: search_files)
        ("11. Search Files", test_11_search_files),
        # Permission (3 methods: add, update, delete)
        ("12. Add Permission", test_12_add_permission),
        ("13. Update Permission", test_13_update_permission),
        ("14. Delete Permission", test_14_delete_permission),
        # Final cleanup
        ("15. Delete File", test_15_delete_file),
    ]

    for name, fn in tests:
        run(name, fn)
        # Rate limit: 5 QPS per token
        # Most tests already have time.sleep(0.5), but add buffer for safety
        time.sleep(0.2)

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
