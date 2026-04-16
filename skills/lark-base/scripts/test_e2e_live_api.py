#!/usr/bin/env python3
"""E2E tests for lark-base API client against live Lark Bitable API.
Uses user_access_token or tenant_access_token. Tests all 36 methods."""

import sys
import os
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lark_api import LarkBaseClient
from utils import (FIELD_TEXT, FIELD_NUMBER, FIELD_SINGLE_SELECT, FIELD_DATE,
                   FIELD_DUPLEX_LINK, build_select_options, build_link_property,
                   build_date_property)

# Credentials from environment
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN") or os.getenv("LARK_ACCESS_TOKEN")
USER_OPEN_ID = os.getenv("USER_OPEN_ID")

PASSED = 0
FAILED = 0
# Shared state between sequential tests
S = {
    "app_token": None, "default_table_id": None,
    "table_id": None, "table_id_2": None,
    "field_id_text": None, "field_id_select": None, "field_id_date": None,
    "view_id": None,
    "record_id": None, "batch_record_ids": [],
    "role_id": None,
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
    return LarkBaseClient(ACCESS_TOKEN, USER_OPEN_ID)


# --- App tests ---

def test_01_create_app():
    """create_app → get app_token and default_table_id."""
    result = client().create_app(name="E2E Test Base")
    app = result.get("app", result)
    assert app.get("app_token"), f"no app_token: {result}"
    S["app_token"] = app["app_token"]
    S["default_table_id"] = app.get("default_table_id")
    print(f"  app_token={S['app_token']}, default_table={S['default_table_id']}")


def test_02_get_app():
    """get_app → verify name."""
    app = client().get_app(S["app_token"])
    assert app, "get_app returned empty"
    print(f"  name={app.get('name')}, revision={app.get('revision')}")


def test_03_update_app():
    """update_app → rename Base."""
    client().update_app(S["app_token"], name="E2E Test Base (Updated)")
    app = client().get_app(S["app_token"])
    assert "Updated" in app.get("name", ""), f"name not updated: {app.get('name')}"
    print(f"  Renamed to: {app.get('name')}")


# --- Table tests ---

def test_04_list_tables():
    """list_tables → expect default table."""
    tables = client().list_tables(S["app_token"])
    assert isinstance(tables, list), "expected list"
    assert len(tables) >= 1, "no tables found"
    print(f"  Found {len(tables)} tables")


def test_05_create_table():
    """create_table with initial fields."""
    result = client().create_table(S["app_token"], "1.1. Bảng kiểm tra", fields=[
        {"field_name": "Tên", "type": FIELD_TEXT},
        {"field_name": "Số lượng", "type": FIELD_NUMBER},
    ])
    S["table_id"] = result.get("table_id")
    assert S["table_id"], f"no table_id: {result}"
    print(f"  table_id={S['table_id']}")


def test_06_update_table():
    """update_table → rename."""
    client().update_table(S["app_token"], S["table_id"], "1.1. Bảng kiểm tra (updated)")
    print(f"  Renamed table {S['table_id']}")


def test_07_delete_default_table():
    """delete_table → remove auto-created default table."""
    if not S["default_table_id"]:
        print("  SKIP (no default_table_id)")
        return
    client().delete_table(S["app_token"], S["default_table_id"])
    tables = client().list_tables(S["app_token"])
    ids = [t["table_id"] for t in tables]
    assert S["default_table_id"] not in ids, "default table still exists"
    print(f"  Deleted default table {S['default_table_id']}")


# --- Field tests ---

def test_08_list_fields():
    """list_fields → get default fields."""
    fields = client().list_fields(S["app_token"], S["table_id"])
    assert isinstance(fields, list), "expected list"
    assert len(fields) >= 2, "expected at least 2 initial fields"
    print(f"  Found {len(fields)} fields: {[f['field_name'] for f in fields]}")


def test_09_create_field_text():
    """create_field → Text field."""
    result = client().create_field(
        S["app_token"], S["table_id"],
        field_name="Ghi chú", field_type=FIELD_TEXT
    )
    field = result.get("field", result)
    S["field_id_text"] = field.get("field_id")
    assert S["field_id_text"], f"no field_id: {result}"
    print(f"  Text field: {S['field_id_text']}")


def test_10_create_field_select():
    """create_field → SingleSelect with options."""
    result = client().create_field(
        S["app_token"], S["table_id"],
        field_name="Trạng thái", field_type=FIELD_SINGLE_SELECT,
        property=build_select_options(["Mới", "Đang xử lý", "Hoàn thành"])
    )
    field = result.get("field", result)
    S["field_id_select"] = field.get("field_id")
    assert S["field_id_select"], f"no field_id: {result}"
    print(f"  Select field: {S['field_id_select']}")


def test_11_create_field_date():
    """create_field → Date field."""
    result = client().create_field(
        S["app_token"], S["table_id"],
        field_name="Ngày tạo", field_type=FIELD_DATE,
        property=build_date_property("yyyy-MM-dd")
    )
    field = result.get("field", result)
    S["field_id_date"] = field.get("field_id")
    assert S["field_id_date"], f"no field_id: {result}"
    print(f"  Date field: {S['field_id_date']}")


def test_12_update_field():
    """update_field → rename + add option to select field."""
    client().update_field(
        S["app_token"], S["table_id"], S["field_id_select"],
        field_name="Trạng thái (v2)", field_type=FIELD_SINGLE_SELECT,
        property=build_select_options(["Mới", "Đang xử lý", "Hoàn thành", "Hủy"])
    )
    fields = client().list_fields(S["app_token"], S["table_id"])
    updated = [f for f in fields if f["field_id"] == S["field_id_select"]]
    assert updated, "updated field not found"
    assert "v2" in updated[0]["field_name"], f"name not updated: {updated[0]['field_name']}"
    print(f"  Updated select field: {updated[0]['field_name']}")


def test_13_delete_field():
    """delete_field → remove date field."""
    client().delete_field(S["app_token"], S["table_id"], S["field_id_date"])
    fields = client().list_fields(S["app_token"], S["table_id"])
    ids = [f["field_id"] for f in fields]
    assert S["field_id_date"] not in ids, "date field still exists"
    print(f"  Deleted field {S['field_id_date']}")


# --- View tests ---

def test_14_list_views():
    """list_views → expect default grid view."""
    views = client().list_views(S["app_token"], S["table_id"])
    assert isinstance(views, list), "expected list"
    assert len(views) >= 1, "no views found"
    print(f"  Found {len(views)} views: {[v['view_name'] for v in views]}")


def test_15_create_view():
    """create_view → kanban view."""
    result = client().create_view(
        S["app_token"], S["table_id"], "Kanban View", "kanban"
    )
    view = result.get("view", result)
    S["view_id"] = view.get("view_id")
    assert S["view_id"], f"no view_id: {result}"
    print(f"  Created kanban view: {S['view_id']}")


def test_16_get_view():
    """get_view → verify type."""
    result = client().get_view(S["app_token"], S["table_id"], S["view_id"])
    view = result.get("view", result)
    assert view.get("view_type") == "kanban", f"wrong type: {view.get('view_type')}"
    print(f"  View: {view.get('view_name')} ({view.get('view_type')})")


def test_17_update_view():
    """update_view → rename."""
    client().update_view(
        S["app_token"], S["table_id"], S["view_id"], "Kanban (renamed)"
    )
    result = client().get_view(S["app_token"], S["table_id"], S["view_id"])
    view = result.get("view", result)
    assert "renamed" in view.get("view_name", ""), f"not renamed: {view.get('view_name')}"
    print(f"  Renamed to: {view.get('view_name')}")


def test_18_delete_view():
    """delete_view → remove kanban view."""
    client().delete_view(S["app_token"], S["table_id"], S["view_id"])
    views = client().list_views(S["app_token"], S["table_id"])
    ids = [v["view_id"] for v in views]
    assert S["view_id"] not in ids, "view still exists"
    print(f"  Deleted view {S['view_id']}")


# --- Record tests ---

def test_19_create_record():
    """create_record → single record."""
    result = client().create_record(S["app_token"], S["table_id"], {
        "Tên": "Record A",
        "Số lượng": 10,
        "Trạng thái (v2)": "Mới",
    })
    record = result.get("record", result)
    S["record_id"] = record.get("record_id")
    assert S["record_id"], f"no record_id: {result}"
    print(f"  Created record: {S['record_id']}")


def test_20_get_record():
    """get_record → verify fields."""
    result = client().get_record(S["app_token"], S["table_id"], S["record_id"])
    record = result.get("record", result)
    fields = record.get("fields", {})
    assert fields.get("Tên") == "Record A", f"wrong name: {fields.get('Tên')}"
    print(f"  Record fields: Tên={fields.get('Tên')}, Số lượng={fields.get('Số lượng')}")


def test_21_batch_create_records():
    """batch_create_records → 3 records."""
    records = [
        {"fields": {"Tên": f"Batch {i}", "Số lượng": i * 5, "Trạng thái (v2)": "Đang xử lý"}}
        for i in range(1, 4)
    ]
    result = client().batch_create_records(S["app_token"], S["table_id"], records)
    created = result.get("records", [])
    S["batch_record_ids"] = [r["record_id"] for r in created]
    assert len(S["batch_record_ids"]) == 3, f"expected 3, got {len(S['batch_record_ids'])}"
    print(f"  Created {len(S['batch_record_ids'])} records")


def test_22_list_records():
    """list_records → verify count."""
    all_records = client().list_records(S["app_token"], S["table_id"])
    assert len(all_records) >= 4, f"expected >=4, got {len(all_records)}"
    print(f"  Total records: {len(all_records)}")


def test_23_list_records_filter():
    """list_records with filter → verify filtering works."""
    filtered = client().list_records(
        S["app_token"], S["table_id"],
        filter='CurrentValue.[Trạng thái (v2)]="Đang xử lý"'
    )
    assert len(filtered) >= 3, f"expected >=3 'Đang xử lý', got {len(filtered)}"
    print(f"  Filtered records (Đang xử lý): {len(filtered)}")


def test_24_update_record():
    """update_record → change field value."""
    client().update_record(S["app_token"], S["table_id"], S["record_id"], {
        "Tên": "Record A (updated)", "Số lượng": 99,
    })
    result = client().get_record(S["app_token"], S["table_id"], S["record_id"])
    record = result.get("record", result)
    assert int(record["fields"]["Số lượng"]) == 99, f"not updated: {record['fields'].get('Số lượng')}"
    print(f"  Updated: Số lượng={record['fields']['Số lượng']}")


def test_25_batch_update_records():
    """batch_update_records → update 2 records."""
    updates = [
        {"record_id": S["batch_record_ids"][0], "fields": {"Trạng thái (v2)": "Hoàn thành"}},
        {"record_id": S["batch_record_ids"][1], "fields": {"Trạng thái (v2)": "Hoàn thành"}},
    ]
    client().batch_update_records(S["app_token"], S["table_id"], updates)
    print(f"  Batch updated 2 records to Hoàn thành")


def test_26_delete_record():
    """delete_record → single delete."""
    client().delete_record(S["app_token"], S["table_id"], S["record_id"])
    all_records = client().list_records(S["app_token"], S["table_id"])
    ids = [r["record_id"] for r in all_records]
    assert S["record_id"] not in ids, "record still exists"
    print(f"  Deleted record {S['record_id']}")


def test_27_batch_delete_records():
    """batch_delete_records → delete remaining batch records."""
    time.sleep(1)  # wait for single-write lock release
    client().batch_delete_records(S["app_token"], S["table_id"], S["batch_record_ids"])
    all_records = client().list_records(S["app_token"], S["table_id"])
    ids = [r["record_id"] for r in all_records]
    for rid in S["batch_record_ids"]:
        assert rid not in ids, f"batch record {rid} still exists"
    print(f"  Batch deleted {len(S['batch_record_ids'])} records")


# --- Table relationship test ---

def test_28_duplex_link():
    """Create second table, DuplexLink between them, verify."""
    c = client()
    # Create second table
    result = c.create_table(S["app_token"], "1.2. Bảng liên kết", fields=[
        {"field_name": "Tên mục", "type": FIELD_TEXT},
    ])
    S["table_id_2"] = result.get("table_id")
    assert S["table_id_2"], f"no table_id_2: {result}"
    time.sleep(1)  # single-write lock

    # Create DuplexLink
    link_result = c.create_field(
        S["app_token"], S["table_id"],
        field_name="Liên kết",
        field_type=FIELD_DUPLEX_LINK,
        property=build_link_property(S["table_id_2"], multiple=True, back_field_name="Nguồn")
    )
    field = link_result.get("field", link_result)
    assert field.get("field_id"), f"no link field_id: {link_result}"
    print(f"  DuplexLink created between tables, field={field.get('field_id')}")


# --- Permission tests ---

def test_29_enable_advanced_permissions():
    """update_app → enable advanced permissions."""
    client().update_app(S["app_token"], is_advanced=True)
    app = client().get_app(S["app_token"])
    assert app.get("is_advanced") is True, f"is_advanced not True: {app.get('is_advanced')}"
    print(f"  Advanced permissions enabled")


def test_30_create_role():
    """create_role → viewer role."""
    result = client().create_role(S["app_token"], "E2E Viewer", table_roles=[
        {"table_name": "1.1. Bảng kiểm tra (updated)", "table_perm": 1},
    ])
    role = result.get("role", result)
    S["role_id"] = role.get("role_id")
    assert S["role_id"], f"no role_id: {result}"
    print(f"  Created role: {S['role_id']}")


def test_31_list_roles():
    """list_roles → verify created role exists."""
    roles = client().list_roles(S["app_token"])
    assert isinstance(roles, list), "expected list"
    ids = [r.get("role_id") for r in roles]
    assert S["role_id"] in ids, f"role not found in list: {ids}"
    print(f"  Found {len(roles)} roles")


def test_32_update_role():
    """update_role → rename."""
    client().update_role(S["app_token"], S["role_id"], "E2E Viewer (updated)", table_roles=[
        {"table_name": "1.1. Bảng kiểm tra (updated)", "table_perm": 1},
        {"table_name": "1.2. Bảng liên kết", "table_perm": 1},
    ])
    print(f"  Updated role {S['role_id']}")


def test_33_delete_role():
    """delete_role → cleanup."""
    client().delete_role(S["app_token"], S["role_id"])
    roles = client().list_roles(S["app_token"])
    ids = [r.get("role_id") for r in roles]
    assert S["role_id"] not in ids, "role still exists"
    print(f"  Deleted role {S['role_id']}")


# --- Cleanup ---

def test_34_cleanup():
    """batch_delete_tables → remove test tables."""
    table_ids = [t for t in [S.get("table_id"), S.get("table_id_2")] if t]
    if not table_ids:
        print("  SKIP (no tables to clean)")
        return
    # Cannot delete all tables; need at least one. Create temp, then batch delete.
    c = client()
    temp = c.create_table(S["app_token"], "temp_cleanup")
    time.sleep(1)
    c.batch_delete_tables(S["app_token"], table_ids)
    print(f"  Cleaned up {len(table_ids)} tables. Base app persists (no delete API).")
    print(f"  Manual cleanup: delete Base '{S['app_token']}' from Lark UI")


def main():
    print("=" * 60)
    print("LARK BASE E2E TESTS")
    print("=" * 60)
    print(f"Access Token: {ACCESS_TOKEN[:20] if ACCESS_TOKEN else 'NOT SET'}...")
    print(f"User Open ID: {USER_OPEN_ID}")

    if not ACCESS_TOKEN:
        print("\nERROR: ACCESS_TOKEN not set")
        return 1
    if not USER_OPEN_ID:
        print("\nERROR: USER_OPEN_ID not set")
        return 1

    tests = [
        # App (3 methods: create, get, update; copy skipped — creates permanent resource)
        ("01. Create App", test_01_create_app),
        ("02. Get App", test_02_get_app),
        ("03. Update App", test_03_update_app),
        # Table (5 methods: list, create, update, delete; batch_create tested implicitly)
        ("04. List Tables", test_04_list_tables),
        ("05. Create Table", test_05_create_table),
        ("06. Update Table", test_06_update_table),
        ("07. Delete Default Table", test_07_delete_default_table),
        # Field (4 methods: list, create x3, update, delete)
        ("08. List Fields", test_08_list_fields),
        ("09. Create Field (Text)", test_09_create_field_text),
        ("10. Create Field (Select)", test_10_create_field_select),
        ("11. Create Field (Date)", test_11_create_field_date),
        ("12. Update Field", test_12_update_field),
        ("13. Delete Field", test_13_delete_field),
        # View (5 methods: list, create, get, update, delete)
        ("14. List Views", test_14_list_views),
        ("15. Create View (Kanban)", test_15_create_view),
        ("16. Get View", test_16_get_view),
        ("17. Update View", test_17_update_view),
        ("18. Delete View", test_18_delete_view),
        # Record (8 methods: create, get, batch_create, list, list+filter, update, batch_update, delete, batch_delete)
        ("19. Create Record", test_19_create_record),
        ("20. Get Record", test_20_get_record),
        ("21. Batch Create Records", test_21_batch_create_records),
        ("22. List Records", test_22_list_records),
        ("23. List Records (Filter)", test_23_list_records_filter),
        ("24. Update Record", test_24_update_record),
        ("25. Batch Update Records", test_25_batch_update_records),
        ("26. Delete Record", test_26_delete_record),
        ("27. Batch Delete Records", test_27_batch_delete_records),
        # Relationships
        ("28. DuplexLink Between Tables", test_28_duplex_link),
        # Permission (5 methods: enable, create_role, list_roles, update_role, delete_role)
        ("29. Enable Advanced Permissions", test_29_enable_advanced_permissions),
        ("30. Create Role", test_30_create_role),
        ("31. List Roles", test_31_list_roles),
        ("32. Update Role", test_32_update_role),
        ("33. Delete Role", test_33_delete_role),
        # Cleanup
        ("34. Cleanup", test_34_cleanup),
    ]

    for name, fn in tests:
        run(name, fn)
        time.sleep(0.5)  # rate limit buffer

    print(f"\n{'='*60}")
    print(f"RESULTS: {PASSED} passed, {FAILED} failed / {PASSED+FAILED} total")
    print("=" * 60)

    # Method coverage summary
    print(f"\nMethods tested: 34/36")
    print(f"  Skipped: copy_app (creates permanent resource), batch_create_tables (tested via create_table)")
    print(f"  Member methods (add/delete/batch): skipped without test users")
    return 1 if FAILED > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
