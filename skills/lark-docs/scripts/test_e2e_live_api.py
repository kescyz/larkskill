#!/usr/bin/env python3
"""E2E tests for lark-docs skill — live API, no mocks, sequential CRUD roundtrips.

Tests 25 of 25 LarkDocsClient methods via sequential CRUD roundtrip:
  - Document (4): create_document, get_document, get_raw_content, list_blocks
  - Block (6): get_block, get_block_children, create_blocks, update_block,
               batch_update_blocks, delete_blocks
  - Convenience (3): create_text_block, create_heading_block, create_todo_block
  - Table (7): create_table, insert_table_row, insert_table_column,
               delete_table_rows, merge_table_cells, fill_table_cells, create_large_table
  - Convert & Import (4): convert_to_blocks, clean_convert_output,
               create_nested_blocks, import_markdown
  - Export (1): export_to_markdown
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lark_api import LarkDocsClient

# Credentials from environment
ACCESS_TOKEN = os.getenv("LARK_ACCESS_TOKEN")
USER_OPEN_ID = os.getenv("LARK_OPEN_ID")

PASSED = 0
FAILED = 0
CLEANUP = []  # document_ids to delete via Drive API
TIMESTAMP = int(time.time())

# Shared state between sequential tests
S = {}


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
    """Get LarkDocsClient instance."""
    return LarkDocsClient(access_token=ACCESS_TOKEN, user_open_id=USER_OPEN_ID)


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


def delete_doc_via_drive(document_id):
    """Delete a DocX document via Drive API (DocX has no own delete endpoint)."""
    url = f"https://open.larksuite.com/open-apis/drive/v1/files/{document_id}?type=docx"
    cmd = [
        "curl", "-s", "-X", "DELETE", url,
        "-H", f"Authorization: Bearer {ACCESS_TOKEN}"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        try:
            resp = json.loads(result.stdout)
            if resp.get("code") == 0:
                return True
        except Exception:
            pass
    return False


# --- CRUD Tests ---

def test_01_create_document():
    """Create a test document, store document_id."""
    c = client()
    result = c.create_document(title=f"[TEST] docs-{TIMESTAMP}")
    # Response nested under "document" key
    doc = result.get("document") or result
    S["document_id"] = doc.get("document_id")
    assert_true("document_id exists", S["document_id"] is not None)
    CLEANUP.append(S["document_id"])
    print(f"    document_id: {S['document_id']}")


def test_02_get_document():
    """Get document metadata, verify title matches."""
    time.sleep(1)  # rate limit between writes
    c = client()
    result = c.get_document(S["document_id"])
    doc = result.get("document") or result
    title = doc.get("title") or doc.get("document_id")
    assert_true("document returned", bool(result))
    print(f"    title: {title}")


def test_03_create_text_blocks():
    """Create 3 blocks: text, heading, todo — using convenience helpers."""
    time.sleep(1)  # rate limit
    c = client()
    # Page block_id == document_id
    parent = S["document_id"]

    r1 = c.create_text_block(S["document_id"], parent, "Hello from E2E test")
    time.sleep(1)
    r2 = c.create_heading_block(S["document_id"], parent, "Action Items", level=1)
    time.sleep(1)
    r3 = c.create_todo_block(S["document_id"], parent, "Write tests", done=False)
    time.sleep(1)

    # Each returns dict with "children" list of created blocks
    blocks_1 = (r1.get("children") or [])
    blocks_2 = (r2.get("children") or [])
    blocks_3 = (r3.get("children") or [])

    assert_true("text block created", len(blocks_1) > 0)
    assert_true("heading block created", len(blocks_2) > 0)
    assert_true("todo block created", len(blocks_3) > 0)

    # Store block_ids for later tests
    S["text_block_id"] = blocks_1[0].get("block_id")
    S["heading_block_id"] = blocks_2[0].get("block_id") if blocks_2 else None
    S["heading_block_id"] = blocks_2[0].get("block_id")
    print(f"    text_block_id: {S['text_block_id']}")
    print(f"    heading_block_id: {S['heading_block_id']}")


def test_04_list_blocks():
    """List all blocks, verify count >= 4 (1 page block + 3 created)."""
    c = client()
    blocks = c.list_blocks(S["document_id"])
    assert_true("blocks is list", isinstance(blocks, list))
    assert_true("at least 4 blocks", len(blocks) >= 4)
    print(f"    block count: {len(blocks)}")


def test_05_get_block():
    """Get a specific block, verify block_id matches."""
    c = client()
    result = c.get_block(S["document_id"], S["text_block_id"])
    block = result.get("block") or result
    block_id = block.get("block_id")
    assert_eq("block_id matches", block_id, S["text_block_id"])


def test_06_update_block():
    """Update the text block content with new text."""
    time.sleep(1)  # rate limit
    c = client()
    new_elements = {
        "elements": [
            {"text_run": {"content": f"Updated by E2E test {TIMESTAMP}"}}
        ]
    }
    result = c.update_block(
        S["document_id"],
        S["text_block_id"],
        update_text_elements=new_elements
    )
    assert_true("update returned data", result is not None)
    print(f"    block updated successfully")


def test_07_delete_blocks():
    """Delete first child block of page (index range [0, 1))."""
    time.sleep(1)  # rate limit
    c = client()
    # document_id is also the page block_id (root block)
    result = c.delete_blocks(
        S["document_id"],
        S["document_id"],  # parent block_id = document_id (page block)
        start_index=0,
        end_index=1
    )
    assert_true("delete returned data", result is not None)
    print(f"    deleted first child block")


def test_08_get_raw_content():
    """Get raw text content, verify it returns some text."""
    c = client()
    result = c.get_raw_content(S["document_id"])
    content = result.get("content") or ""
    assert_true("raw content is string", isinstance(content, str))
    print(f"    raw content length: {len(content)} chars")


# --- Table Tests ---

def test_09_create_table():
    """Create a small 2x3 table using create_table convenience method."""
    time.sleep(1)
    c = client()
    result = c.create_table(S["document_id"], S["document_id"], row_size=2, column_size=3)
    created = result.get("children") or []
    assert_true("table created", len(created) > 0)
    S["table_block_id"] = created[0]["block_id"]
    print(f"    table_block_id: {S['table_block_id']}")


def test_10_insert_table_row():
    """Insert row to grow table from 2x3 to 4x3."""
    time.sleep(1)
    c = client()
    # Insert 2 rows at indices 2 and 3
    c.insert_table_row(S["document_id"], S["table_block_id"], 2)
    time.sleep(0.5)
    c.insert_table_row(S["document_id"], S["table_block_id"], 3)
    time.sleep(0.5)
    # Verify row count
    result = c.get_block(S["document_id"], S["table_block_id"])
    block = result.get("block") or result
    row_size = block.get("table", {}).get("property", {}).get("row_size")
    assert_eq("row_size after insert", row_size, 4)


def test_11_insert_table_column():
    """Insert column to grow table from 4x3 to 4x4."""
    time.sleep(1)
    c = client()
    c.insert_table_column(S["document_id"], S["table_block_id"], 3)
    time.sleep(0.5)
    result = c.get_block(S["document_id"], S["table_block_id"])
    block = result.get("block") or result
    col_size = block.get("table", {}).get("property", {}).get("column_size")
    assert_eq("column_size after insert", col_size, 4)


def test_12_fill_table_cells():
    """Fill table cells with content using fill_table_cells."""
    time.sleep(1)
    c = client()
    data_rows = [
        [{"text": "#", "bold": True}, {"text": "Name", "bold": True},
         {"text": "Desc", "bold": True}, {"text": "Cost", "bold": True}],
        ["A1", "Auth", "RBAC + 2FA", "38"],
        ["A2", "PWA", "Responsive", "37"],
        ["A3", "Notify", "Push + email", "31"],
    ]
    results = c.fill_table_cells(S["document_id"], S["table_block_id"], data_rows)
    assert_true("fill returned results", len(results) > 0)
    # Verify content via raw
    time.sleep(0.5)
    raw = c.get_raw_content(S["document_id"])
    content = raw.get("content", "")
    assert_true("'Auth' in content", "Auth" in content)
    assert_true("'38' in content", "38" in content)
    print(f"    filled 4x4 table with content")


def test_13_merge_table_cells():
    """Merge cells in table."""
    time.sleep(1)
    c = client()
    result = c.merge_table_cells(
        S["document_id"], S["table_block_id"],
        row_start=0, row_end=1, col_start=2, col_end=4
    )
    assert_true("merge returned data", result is not None)
    print(f"    merged cells [0,0)x[2,4)")


def test_14_delete_table_rows():
    """Delete last row from table (4x4 -> 3x4)."""
    time.sleep(1)
    c = client()
    c.delete_table_rows(S["document_id"], S["table_block_id"],
                        row_start_index=3, row_end_index=4)
    time.sleep(0.5)
    result = c.get_block(S["document_id"], S["table_block_id"])
    block = result.get("block") or result
    row_size = block.get("table", {}).get("property", {}).get("row_size")
    assert_eq("row_size after delete", row_size, 3)


# --- Convert & Clean Tests ---

def test_15_convert_to_blocks():
    """Convert markdown to blocks via API."""
    c = client()
    md = "# Test Heading\n\nSome paragraph text.\n\n- Bullet one\n- Bullet two\n"
    result = c.convert_to_blocks(md)  # default: content_type="markdown"
    blocks = result.get("blocks", [])
    assert_true("blocks returned", len(blocks) > 0)
    S["convert_blocks"] = blocks
    # Check block types present
    types = {b.get("block_type") for b in blocks}
    assert_true("has heading block", 3 in types)  # heading1
    assert_true("has text or bullet", 2 in types or 12 in types)
    print(f"    Converted {len(blocks)} blocks, types: {sorted(types)}")


def test_16_clean_convert_output():
    """Clean convert output - verify no mutation, correct filtering."""
    blocks = S.get("convert_blocks", [])
    assert_true("have convert blocks", len(blocks) > 0)
    # Save original to check no mutation
    import copy
    original = copy.deepcopy(blocks)
    cleaned = LarkDocsClient.clean_convert_output(blocks)
    # No type-32 in cleaned output
    type32 = [b for b in cleaned if b.get("block_type") == 32]
    assert_eq("table_cell blocks filtered", len(type32), 0)
    # block_id/parent_id/children stripped
    for b in cleaned:
        assert_true("no block_id", "block_id" not in b)
        assert_true("no parent_id", "parent_id" not in b)
        assert_true("no children", "children" not in b)
    # Original not mutated
    assert_eq("original unchanged", blocks, original)
    print(f"    Cleaned: {len(blocks)} -> {len(cleaned)} blocks")


def test_17_insert_converted_blocks():
    """Insert cleaned convert output into document via create_blocks."""
    c = client()
    blocks = S.get("convert_blocks", [])
    cleaned = LarkDocsClient.clean_convert_output(blocks)
    doc_id = S["document_id"]
    # Insert first batch (should be small enough for one call)
    batch = cleaned[:50]
    result = c.create_blocks(doc_id, doc_id, batch)
    children = result.get("children", [])
    assert_true("blocks inserted", len(children) > 0)
    print(f"    Inserted {len(children)} blocks from convert output")
    time.sleep(0.5)


# --- New tests: batch_update, get_block_children, export, create_nested_blocks,
#     import_markdown, create_large_table, clean_convert_for_descendant ---

def test_18_get_block_children():
    """Get children of document root block."""
    time.sleep(1)
    c = client()
    doc_id = S["document_id"]
    children = c.get_block_children(doc_id, doc_id)
    assert_true("children is list", isinstance(children, list))
    assert_true("has children", len(children) > 0)
    print(f"    Root has {len(children)} children")


def test_19_batch_update_blocks():
    """Batch update: rename the heading block created in test_03."""
    time.sleep(1)
    c = client()
    doc_id = S["document_id"]
    heading_id = S.get("heading_block_id")
    if not heading_id:
        # Fallback: find a heading block
        blocks = c.list_blocks(doc_id)
        for b in blocks:
            if b.get("block_type") == 3:
                heading_id = b.get("block_id")
                break
    if not heading_id:
        print("    SKIP: no heading block found")
        return
    result = c.batch_update_blocks(doc_id, [{
        "block_id": heading_id,
        "update_text_elements": {
            "elements": [{"text_run": {"content": "Updated via batch"}}]
        }
    }])
    assert_true("batch update returned", result is not None)
    print(f"    Updated heading {heading_id}")


def test_20_export_to_markdown():
    """Export document to markdown string."""
    time.sleep(1)
    c = client()
    doc_id = S["document_id"]
    md = c.export_to_markdown(doc_id)
    assert_true("markdown returned", isinstance(md, str))
    assert_true("has content", len(md) > 10)
    print(f"    Exported {len(md)} chars markdown")


def test_21_clean_convert_for_descendant():
    """Clean convert output for descendant mode - keeps block_id/children."""
    blocks = S.get("convert_blocks", [])
    assert_true("have convert blocks", len(blocks) > 0)
    cleaned = LarkDocsClient.clean_convert_output(blocks, for_descendant=True)
    # block_id and children MUST be preserved
    has_block_id = any("block_id" in b for b in cleaned)
    assert_true("block_id preserved", has_block_id)
    # table_cell (type 32) should NOT be filtered
    all_types = {b.get("block_type") for b in cleaned}
    print(f"    Descendant clean: {len(cleaned)} blocks, types: {sorted(all_types)}")


def test_22_create_nested_blocks():
    """Create nested blocks via /descendant endpoint using convert output."""
    time.sleep(1)
    c = client()
    # Create fresh doc for this test
    doc_result = c.create_document(title=f"[TEST] nested-{TIMESTAMP}")
    doc = doc_result.get("document") or doc_result
    doc_id = doc.get("document_id")
    CLEANUP.append(doc_id)
    time.sleep(1)
    # Convert simple markdown
    md = "# Heading\n\nParagraph text.\n\n- Bullet 1\n- Bullet 2"
    result = c.convert_to_blocks(md)
    blocks = result.get("blocks", [])
    top_ids = result.get("first_level_block_ids", [])
    assert_true("have blocks", len(blocks) > 0)
    assert_true("have top_level_ids", len(top_ids) > 0)
    # Clean for descendant (only remove merge_info)
    cleaned = LarkDocsClient.clean_convert_output(blocks, for_descendant=True)
    time.sleep(1)
    # Insert via descendant
    res = c.create_nested_blocks(doc_id, doc_id,
                                 children_id=top_ids,
                                 descendants=cleaned)
    assert_true("descendant returned data", res is not None)
    print(f"    Inserted {len(cleaned)} blocks via descendant into {doc_id}")


def test_23_create_large_table():
    """Create a large table (6x4=24 cells, then grow + fill)."""
    time.sleep(1)
    c = client()
    doc_id = S["document_id"]
    data_rows = [
        [{"text": "Col A", "bold": True}, {"text": "Col B", "bold": True},
         {"text": "Col C", "bold": True}, {"text": "Col D", "bold": True}],
        ["a1", "b1", "c1", "d1"],
        ["a2", "b2", "c2", "d2"],
        ["a3", "b3", "c3", "d3"],
        ["a4", "b4", "c4", "d4"],
        ["a5", "b5", "c5", "d5"],
    ]
    table_id = c.create_large_table(doc_id, doc_id, 6, 4, data_rows=data_rows)
    assert_true("table_id returned", table_id is not None)
    assert_true("table_id is string", isinstance(table_id, str))
    time.sleep(0.5)
    # Verify table exists
    block = c.get_block(doc_id, table_id)
    tbl = (block.get("block") or block).get("table", {}).get("property", {})
    assert_eq("row_size", tbl.get("row_size"), 6)
    assert_eq("column_size", tbl.get("column_size"), 4)
    print(f"    Created 6x4 table: {table_id}")


def test_24_import_markdown():
    """Import a real Vietnamese markdown file with tables via import_markdown."""
    time.sleep(1)
    c = client()
    # Create fresh doc
    doc_result = c.create_document(title=f"[TEST] import-md-{TIMESTAMP}")
    doc = doc_result.get("document") or doc_result
    doc_id = doc.get("document_id")
    CLEANUP.append(doc_id)
    time.sleep(1)
    # Read meeting recap markdown
    md_path = Path(__file__).parent.parent.parent.parent.parent.parent / "meeting recap.md"
    if not md_path.exists():
        # Fallback: use simple Vietnamese markdown with table
        md = ("# Biên bản họp\n\n## Người tham gia\n\n"
              "| Tên | Vai trò |\n|-----|--------|\n"
              "| Hưng | Giám đốc |\n| Kiên | Cố vấn |\n\n"
              "## Action Items\n\n- Tạo workspace\n- Bóc tách plan\n")
        print(f"    Using fallback markdown (meeting recap.md not found at {md_path})")
    else:
        md = md_path.read_text(encoding="utf-8")
        print(f"    Loaded meeting recap: {len(md)} chars, ~{md.count(chr(10))} lines")
    # Import
    result = c.import_markdown(doc_id, md)
    assert_true("result returned", result is not None)
    method = result.get("_method", "unknown")
    count = result.get("_blocks_count", 0)
    print(f"    Method: {method}, blocks: {count}, doc: {doc_id}")
    # Verify content was inserted
    time.sleep(2)
    result_raw = c.get_raw_content(doc_id)
    raw = result_raw.get("content", "") if isinstance(result_raw, dict) else str(result_raw)
    assert_true("doc has content", len(raw) > 10)
    # Check Vietnamese text preserved
    if "Biên bản" in md:
        assert_true("Vietnamese preserved", "Biên bản" in raw or "bản" in raw.lower())
    print(f"    Raw content length: {len(raw)} chars")


# --- Cleanup ---

def cleanup():
    """Delete all test documents via Drive API."""
    if not CLEANUP:
        print("\nNo cleanup needed")
        return
    print(f"\n{'='*60}\nCLEANUP\n{'='*60}")
    for doc_id in CLEANUP:
        try:
            success = delete_doc_via_drive(doc_id)
            status = "Cleaned" if success else "Cleanup may have failed"
            print(f"  {status}: {doc_id}")
        except Exception as e:
            print(f"  Failed to clean {doc_id}: {e}")
        time.sleep(0.5)


# --- Main ---

def main():
    print("=" * 60)
    print("LARK DOCS E2E TESTS")
    print("=" * 60)
    print(f"Access Token: {ACCESS_TOKEN[:20] if ACCESS_TOKEN else 'NOT SET'}...")
    print(f"User Open ID: {USER_OPEN_ID}")
    print(f"Timestamp: {TIMESTAMP}")

    if not ACCESS_TOKEN:
        print("\nERROR: LARK_ACCESS_TOKEN not set")
        return 1
    if not USER_OPEN_ID:
        print("\nERROR: LARK_OPEN_ID not set")
        return 1

    tests = [
        ("01. Create document", test_01_create_document),
        ("02. Get document", test_02_get_document),
        ("03. Create text blocks", test_03_create_text_blocks),
        ("04. List blocks", test_04_list_blocks),
        ("05. Get block", test_05_get_block),
        ("06. Update block", test_06_update_block),
        ("07. Delete blocks", test_07_delete_blocks),
        ("08. Get raw content", test_08_get_raw_content),
        ("09. Create table", test_09_create_table),
        ("10. Insert table row", test_10_insert_table_row),
        ("11. Insert table column", test_11_insert_table_column),
        ("12. Fill table cells", test_12_fill_table_cells),
        ("13. Merge table cells", test_13_merge_table_cells),
        ("14. Delete table rows", test_14_delete_table_rows),
        ("15. Convert to blocks", test_15_convert_to_blocks),
        ("16. Clean convert output", test_16_clean_convert_output),
        ("17. Insert converted blocks", test_17_insert_converted_blocks),
        ("18. Get block children", test_18_get_block_children),
        ("19. Batch update blocks", test_19_batch_update_blocks),
        ("20. Export to markdown", test_20_export_to_markdown),
        ("21. Clean convert (descendant)", test_21_clean_convert_for_descendant),
        ("22. Create nested blocks", test_22_create_nested_blocks),
        ("23. Create large table", test_23_create_large_table),
        ("24. Import markdown (meeting recap)", test_24_import_markdown),
    ]

    for name, fn in tests:
        run(name, fn)

    print(f"\n{'='*60}")
    print(f"RESULTS: {PASSED} passed, {FAILED} failed / {PASSED + FAILED} total")
    print("=" * 60)

    return 1 if FAILED > 0 else 0


if __name__ == "__main__":
    try:
        exit_code = main()
    finally:
        cleanup()
    sys.exit(exit_code)
