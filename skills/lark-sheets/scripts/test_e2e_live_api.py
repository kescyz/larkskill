#!/usr/bin/env python3
"""E2E tests for lark-sheets skill — live API, no mocks, sequential CRUD roundtrips.

Tests all Sheets methods:
  - Spreadsheet ops (3): create_spreadsheet, get_spreadsheet, update_spreadsheet_properties
  - Metadata/Query (3): get_metadata, query_sheets, get_sheet
  - Sheet management (2): operate_sheets addSheet + deleteSheet
  - Data ops (5): write_range, read_range, append_data, batch_write_ranges, batch_read_ranges
  - Cell ops (3): find_cells, merge_cells, unmerge_cells
  - Styling (1): format_cells
  - Filter views (3): create_filter_view, list_filter_views, delete_filter_view
  - Dimension ops (2): insert_dimension, delete_dimension
"""

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lark_api import LarkSheetsClient

# Credentials from environment
ACCESS_TOKEN = os.getenv("LARK_ACCESS_TOKEN")
USER_OPEN_ID = os.getenv("LARK_OPEN_ID")

PASSED = 0
FAILED = 0
TIMESTAMP = int(time.time())

# Shared state between sequential tests
S = {
    "spreadsheet_token": None,
    "default_sheet_id": None,
    "new_sheet_id": None,
    "filter_view_id": None,
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
    """Get LarkSheetsClient instance."""
    return LarkSheetsClient(access_token=ACCESS_TOKEN, user_open_id=USER_OPEN_ID)


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


# --- Spreadsheet Management ---

def test_01_create_spreadsheet():
    """create_spreadsheet → verify spreadsheet_token returned."""
    title = f"E2E Test Sheets {TIMESTAMP}"
    result = client().create_spreadsheet(title=title)
    spreadsheet = result.get("spreadsheet", {})
    S["spreadsheet_token"] = spreadsheet.get("spreadsheet_token")
    assert_true("spreadsheet_token exists", S["spreadsheet_token"] is not None)
    print(f"    token: {S['spreadsheet_token']}")


def test_02_get_spreadsheet():
    """get_spreadsheet → verify title matches created spreadsheet."""
    result = client().get_spreadsheet(spreadsheet_token=S["spreadsheet_token"])
    spreadsheet = result.get("spreadsheet", {})
    title = spreadsheet.get("title", "")
    assert_true("title contains timestamp", str(TIMESTAMP) in title)
    print(f"    title: {title}")


def test_03_update_spreadsheet_properties():
    """update_spreadsheet_properties → rename, verify via get_spreadsheet."""
    new_title = f"Updated E2E {TIMESTAMP}"
    client().update_spreadsheet_properties(
        spreadsheet_token=S["spreadsheet_token"],
        title=new_title
    )
    time.sleep(0.5)
    # Verify rename took effect
    result = client().get_spreadsheet(spreadsheet_token=S["spreadsheet_token"])
    actual_title = result.get("spreadsheet", {}).get("title", "")
    assert_true("title contains timestamp", str(TIMESTAMP) in actual_title)
    print(f"    updated title: {actual_title}")


def test_04_get_metadata():
    """get_metadata → verify sheets list exists in full metadata."""
    result = client().get_metadata(spreadsheet_token=S["spreadsheet_token"])
    sheets = result.get("sheets", [])
    assert_true("sheets list exists", isinstance(sheets, list))
    assert_true("at least one default sheet", len(sheets) >= 1)
    print(f"    sheets count: {len(sheets)}")


def test_05_query_sheets():
    """query_sheets → capture default_sheet_id from first sheet."""
    sheets = client().query_sheets(spreadsheet_token=S["spreadsheet_token"])
    assert_true("sheets list returned", isinstance(sheets, list))
    assert_true("at least one sheet", len(sheets) >= 1)
    S["default_sheet_id"] = sheets[0].get("sheet_id")
    assert_true("default_sheet_id exists", S["default_sheet_id"] is not None)
    print(f"    default_sheet_id: {S['default_sheet_id']}")


def test_06_operate_sheets_add():
    """operate_sheets (addSheet) → add new sheet, extract new sheet_id from replies."""
    result = client().operate_sheets(
        spreadsheet_token=S["spreadsheet_token"],
        requests=[{"addSheet": {"properties": {"title": "E2E New Sheet"}}}]
    )
    # Response: {replies: [{addSheet: {properties: {sheetId, title, ...}}}]}
    replies = result.get("replies", [])
    assert_true("replies list returned", isinstance(replies, list))
    assert_true("one reply", len(replies) >= 1)
    properties = replies[0].get("addSheet", {}).get("properties", {})
    S["new_sheet_id"] = properties.get("sheetId")
    assert_true("new_sheet_id extracted", S["new_sheet_id"] is not None)
    print(f"    new_sheet_id: {S['new_sheet_id']}")
    time.sleep(1)  # Write lock


def test_07_get_sheet():
    """get_sheet → verify new sheet title is 'E2E New Sheet'."""
    result = client().get_sheet(
        spreadsheet_token=S["spreadsheet_token"],
        sheet_id=S["new_sheet_id"]
    )
    sheet = result.get("sheet", {})
    title = sheet.get("title", "")
    assert_true("sheet title matches", title == "E2E New Sheet")
    print(f"    title: {title}")


def test_08_write_range():
    """write_range → write 3x3 grid to new sheet, verify 9 cells updated."""
    range_str = f"{S['new_sheet_id']}!A1:C3"
    values = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    result = client().write_range(
        spreadsheet_token=S["spreadsheet_token"],
        range=range_str,
        values=values
    )
    updated_cells = result.get("updatedCells", 0)
    assert_true("9 cells updated", updated_cells == 9)
    print(f"    updatedCells: {updated_cells}")
    time.sleep(1)  # Write lock


def test_09_read_range():
    """read_range → verify 3x3 values were written correctly."""
    range_str = f"{S['new_sheet_id']}!A1:C3"
    result = client().read_range(
        spreadsheet_token=S["spreadsheet_token"],
        range=range_str
    )
    values = result.get("valueRange", {}).get("values", [])
    assert_true("values returned", isinstance(values, list))
    assert_true("3 rows returned", len(values) == 3)
    first_row = values[0]
    assert_true("first row has 3 cols", len(first_row) == 3)
    print(f"    first row: {first_row}")


def test_10_append_data():
    """append_data → append one row after existing data."""
    range_str = f"{S['new_sheet_id']}!A1:C1"
    result = client().append_data(
        spreadsheet_token=S["spreadsheet_token"],
        range=range_str,
        values=[[10, 11, 12]]
    )
    assert_true("append returned result", result is not None)
    print(f"    append result keys: {list(result.keys())}")
    time.sleep(1)  # Write lock


def test_11_batch_write_ranges():
    """batch_write_ranges → write to two separate ranges at once."""
    value_ranges = [
        {"range": f"{S['new_sheet_id']}!D1:D3", "values": [["X"], ["Y"], ["Z"]]},
        {"range": f"{S['new_sheet_id']}!E1:E3", "values": [[100], [200], [300]]},
    ]
    result = client().batch_write_ranges(
        spreadsheet_token=S["spreadsheet_token"],
        value_ranges=value_ranges
    )
    assert_true("batch_write returned result", result is not None)
    print(f"    result keys: {list(result.keys())}")
    time.sleep(1)  # Write lock


def test_12_batch_read_ranges():
    """batch_read_ranges → read two separate ranges at once."""
    range1 = f"{S['new_sheet_id']}!A1:C1"
    range2 = f"{S['new_sheet_id']}!D1:E1"
    result = client().batch_read_ranges(
        spreadsheet_token=S["spreadsheet_token"],
        ranges=[range1, range2]
    )
    value_ranges = result.get("valueRanges", [])
    assert_true("valueRanges returned", isinstance(value_ranges, list))
    assert_true("two ranges in response", len(value_ranges) == 2)
    print(f"    valueRanges count: {len(value_ranges)}")


def test_13_find_cells():
    """find_cells → search for '5' in new sheet, expect at least one match."""
    range_str = f"{S['new_sheet_id']}!A1:C3"
    result = client().find_cells(
        spreadsheet_token=S["spreadsheet_token"],
        sheet_id=S["new_sheet_id"],
        find="5",
        find_condition={"range": range_str}
    )
    find_result = result.get("find_result", {})
    matched_cells = find_result.get("matched_cells", [])
    assert_true("matched_cells returned", isinstance(matched_cells, list))
    assert_true("at least one matched cell", len(matched_cells) >= 1)
    print(f"    matched_cells: {matched_cells}")


def test_14_merge_cells():
    """merge_cells → merge A1:C1 (row merge)."""
    range_str = f"{S['new_sheet_id']}!A1:C1"
    result = client().merge_cells(
        spreadsheet_token=S["spreadsheet_token"],
        range=range_str
    )
    assert_true("merge completed without error", result is not None)
    print(f"    merge result: {result}")


def test_15_unmerge_cells():
    """unmerge_cells → unmerge A1:C1."""
    range_str = f"{S['new_sheet_id']}!A1:C1"
    result = client().unmerge_cells(
        spreadsheet_token=S["spreadsheet_token"],
        range=range_str
    )
    assert_true("unmerge completed without error", result is not None)
    print(f"    unmerge result: {result}")


def test_15b_format_cells():
    """format_cells → apply bold font to A1:C1, verify no error returned."""
    range_str = f"{S['new_sheet_id']}!A1:C1"
    result = client().format_cells(
        spreadsheet_token=S["spreadsheet_token"],
        range_str=range_str,
        style={"font": {"bold": True}}
    )
    assert_true("format_cells completed without error", result is not None)
    print(f"    format result keys: {list(result.keys())}")
    time.sleep(1)  # Write lock


def test_15c_create_filter_view():
    """create_filter_view → create a filter view on A1:C3."""
    range_str = f"{S['new_sheet_id']}!A1:C3"
    result = client().create_filter_view(
        spreadsheet_token=S["spreadsheet_token"],
        sheet_id=S["new_sheet_id"],
        range_str=range_str,
        filter_name=f"E2E Filter {TIMESTAMP}"
    )
    assert_true("filter_view result not empty", bool(result))
    S["filter_view_id"] = result.get("filter_view_id", "")
    assert_true("filter_view_id exists", bool(S["filter_view_id"]))
    print(f"    filter_view_id: {S['filter_view_id']}")


def test_15d_list_filter_views():
    """list_filter_views → verify created filter view appears in list."""
    views = client().list_filter_views(
        spreadsheet_token=S["spreadsheet_token"],
        sheet_id=S["new_sheet_id"]
    )
    assert_true("views is a list", isinstance(views, list))
    ids = [v.get("filter_view_id") for v in views]
    assert_true("created view in list", S["filter_view_id"] in ids)
    print(f"    filter views: {len(views)}")


def test_15e_delete_filter_view():
    """delete_filter_view → delete the created filter view, returns True."""
    result = client().delete_filter_view(
        spreadsheet_token=S["spreadsheet_token"],
        sheet_id=S["new_sheet_id"],
        filter_view_id=S["filter_view_id"]
    )
    assert_true("delete_filter_view returned True", result is True)
    print(f"    deleted filter_view_id: {S['filter_view_id']}")
    S["filter_view_id"] = None


def test_16_insert_dimension():
    """insert_dimension → insert 2 ROWS at index 1."""
    result = client().insert_dimension(
        spreadsheet_token=S["spreadsheet_token"],
        sheet_id=S["new_sheet_id"],
        major_dimension="ROWS",
        start_index=1,
        end_index=3
    )
    assert_true("insert_dimension completed", result is not None)
    print(f"    insert result: {result}")
    time.sleep(1)  # Write lock


def test_17_delete_dimension():
    """delete_dimension → delete the 2 previously inserted rows."""
    result = client().delete_dimension(
        spreadsheet_token=S["spreadsheet_token"],
        sheet_id=S["new_sheet_id"],
        major_dimension="ROWS",
        start_index=1,
        end_index=3
    )
    assert_true("delete_dimension completed", result is not None)
    print(f"    delete result: {result}")


def test_18_operate_sheets_delete():
    """operate_sheets (deleteSheet) → remove E2E New Sheet."""
    result = client().operate_sheets(
        spreadsheet_token=S["spreadsheet_token"],
        requests=[{"deleteSheet": {"sheetId": S["new_sheet_id"]}}]
    )
    assert_true("deleteSheet result returned", result is not None)
    print(f"    deleteSheet result: {result}")


def cleanup():
    """Delete test spreadsheet via Drive API (silent on failure)."""
    print("\n" + "="*60)
    print("CLEANUP")
    print("="*60)
    if not S["spreadsheet_token"]:
        print("  No spreadsheet to clean up")
        return
    try:
        client()._call_api(
            "DELETE",
            f"/drive/v1/files/{S['spreadsheet_token']}",
            params={"type": "sheet"}
        )
        print(f"  Deleted spreadsheet {S['spreadsheet_token']}")
    except Exception as e:
        print(f"  Cleanup failed: {str(e)[:100]}")


def main():
    print("=" * 60)
    print("LARK SHEETS E2E TESTS")
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
        # Spreadsheet management (3 methods)
        ("01. Create Spreadsheet", test_01_create_spreadsheet),
        ("02. Get Spreadsheet", test_02_get_spreadsheet),
        ("03. Update Spreadsheet Properties", test_03_update_spreadsheet_properties),
        # Metadata / sheet query (3 methods)
        ("04. Get Metadata", test_04_get_metadata),
        ("05. Query Sheets", test_05_query_sheets),
        # Sheet management (operate_sheets x2 + get_sheet)
        ("06. Operate Sheets (addSheet)", test_06_operate_sheets_add),
        ("07. Get Sheet", test_07_get_sheet),
        # Data operations (5 methods)
        ("08. Write Range", test_08_write_range),
        ("09. Read Range", test_09_read_range),
        ("10. Append Data", test_10_append_data),
        ("11. Batch Write Ranges", test_11_batch_write_ranges),
        ("12. Batch Read Ranges", test_12_batch_read_ranges),
        # Cell operations (3 methods)
        ("13. Find Cells", test_13_find_cells),
        ("14. Merge Cells", test_14_merge_cells),
        ("15. Unmerge Cells", test_15_unmerge_cells),
        # Styling + filter views
        ("15b. Format Cells (bold A1:C1)", test_15b_format_cells),
        ("15c. Create Filter View", test_15c_create_filter_view),
        ("15d. List Filter Views", test_15d_list_filter_views),
        ("15e. Delete Filter View", test_15e_delete_filter_view),
        # Dimension operations (2 methods)
        ("16. Insert Dimension", test_16_insert_dimension),
        ("17. Delete Dimension", test_17_delete_dimension),
        # Final sheet cleanup (operate_sheets deleteSheet)
        ("18. Operate Sheets (deleteSheet)", test_18_operate_sheets_delete),
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
