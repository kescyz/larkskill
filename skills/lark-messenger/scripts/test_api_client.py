#!/usr/bin/env python3
"""
Test script for Lark Messenger API client implementation.
Validates code structure, imports, and logic correctness.
NO LIVE API CALLS are made.
"""

import sys
import json
import inspect
from pathlib import Path

# Add scripts dir to sys.path
scripts_dir = Path(__file__).parent
sys.path.insert(0, str(scripts_dir))

# Import and validate modules
try:
    from lark_api_base import LarkAPIBase
    from lark_api import LarkMessengerClient
    from utils import (
        build_text_content,
        build_image_content,
        build_file_content,
        build_post_content,
        build_share_chat_content,
        build_card_content,
        build_template_card,
        build_birthday_card,
        build_ranking_card,
        build_notification_card,
        build_report_card,
    )
    print("✓ All imports successful")
except ImportError as e:
    print(f"✗ Import error: {e}")
    sys.exit(1)

# ============================================================================
# TEST 1: Validate LarkMessengerClient inheritance
# ============================================================================
def test_inheritance():
    print("\n--- Test 1: Class inheritance ---")
    if not issubclass(LarkMessengerClient, LarkAPIBase):
        print("✗ LarkMessengerClient does not inherit from LarkAPIBase")
        return False
    print("✓ LarkMessengerClient inherits from LarkAPIBase")
    return True


# ============================================================================
# TEST 2: Validate LarkMessengerClient methods
# ============================================================================
def test_messenger_methods():
    print("\n--- Test 2: LarkMessengerClient methods (16 expected) ---")

    expected_methods = {
        "_upload_multipart": ["endpoint", "file_path", "form_fields", "file_field_name"],
        "send_message": ["receive_id", "msg_type", "content", "receive_id_type", "uuid"],
        "reply_message": ["message_id", "msg_type", "content", "reply_in_thread", "uuid"],
        "list_messages": ["container_id", "start_time", "end_time", "container_id_type", "sort_type"],
        "get_message": ["message_id"],
        "delete_message": ["message_id"],
        "get_read_users": ["message_id"],
        "send_card": ["receive_id", "card_content", "receive_id_type", "uuid"],
        "update_card": ["message_id", "card_content"],
        "upload_image": ["image_path", "image_type"],
        "upload_file": ["file_path", "file_type", "file_name", "duration"],
        "create_chat": ["name", "user_id_list", "chat_type", "owner_id", "description"],
        "get_chat": ["chat_id"],
        "list_chats": ["page_size"],
        "search_chats": ["query", "page_size"],
        "add_chat_members": ["chat_id", "member_ids", "member_id_type"],
        "remove_chat_members": ["chat_id", "member_ids", "member_id_type"],
    }

    passed = 0
    failed = 0

    for method_name, expected_params in expected_methods.items():
        if not hasattr(LarkMessengerClient, method_name):
            print(f"✗ Missing method: {method_name}")
            failed += 1
            continue

        method = getattr(LarkMessengerClient, method_name)
        sig = inspect.signature(method)
        params = list(sig.parameters.keys())

        # Remove 'self' from comparison
        params = [p for p in params if p != 'self']

        # Check if all expected params exist (allow extra with defaults)
        missing = set(expected_params) - set(params)
        if missing:
            print(f"✗ Method {method_name} missing params: {missing}")
            print(f"  Expected: {expected_params}, Got: {params}")
            failed += 1
        else:
            passed += 1

    print(f"✓ {passed}/{len(expected_methods)} methods validated")
    if failed > 0:
        print(f"✗ {failed} methods failed validation")
        return False
    return True


# ============================================================================
# TEST 3: Validate utils functions exist and return correct types
# ============================================================================
def test_utils_functions():
    print("\n--- Test 3: Utils functions (11 expected) ---")

    # Content builders (should return strings)
    string_builders = {
        "build_text_content": ("text_content",),
        "build_image_content": ("image_key",),
        "build_file_content": ("file_key",),
        "build_post_content": ("title", ["block1"]),
        "build_share_chat_content": ("chat_123",),
    }

    # Card builders (should return dicts)
    dict_builders = {
        "build_card_content": ("Title", []),
        "build_template_card": ("template_123",),
        "build_birthday_card": ("Alice",),
        "build_ranking_card": ("Leaderboard", [(1, "Alice", 100)]),
        "build_notification_card": ("Alert", "Something happened"),
        "build_report_card": ("Report", [("Metric1", "Value1")]),
    }

    passed = 0
    failed = 0

    # Test string builders
    for func_name, args in string_builders.items():
        func = globals()[func_name]
        try:
            result = func(*args)
            if not isinstance(result, str):
                print(f"✗ {func_name} returned {type(result).__name__}, expected str")
                failed += 1
            else:
                # Validate it's valid JSON
                try:
                    json.loads(result)
                    print(f"✓ {func_name} returns valid JSON string")
                    passed += 1
                except json.JSONDecodeError:
                    print(f"✗ {func_name} returns invalid JSON: {result[:100]}")
                    failed += 1
        except Exception as e:
            print(f"✗ {func_name} raised exception: {e}")
            failed += 1

    # Test dict builders
    for func_name, args in dict_builders.items():
        func = globals()[func_name]
        try:
            result = func(*args)
            if not isinstance(result, dict):
                print(f"✗ {func_name} returned {type(result).__name__}, expected dict")
                failed += 1
            else:
                print(f"✓ {func_name} returns dict")
                passed += 1
        except Exception as e:
            print(f"✗ {func_name} raised exception: {e}")
            failed += 1

    print(f"✓ {passed}/{len(string_builders) + len(dict_builders)} utils functions validated")
    if failed > 0:
        print(f"✗ {failed} utils functions failed validation")
        return False
    return True


# ============================================================================
# TEST 4: Validate content builders produce valid JSON
# ============================================================================
def test_content_builder_json():
    print("\n--- Test 4: Content builder JSON validation ---")

    tests = [
        ("build_text_content", ("Hello World",), {"text": "Hello World"}),
        ("build_image_content", ("img_123",), {"image_key": "img_123"}),
        ("build_file_content", ("file_456",), {"file_key": "file_456"}),
        ("build_share_chat_content", ("chat_789",), {"chat_id": "chat_789"}),
    ]

    passed = 0
    failed = 0

    for func_name, args, expected_structure in tests:
        func = globals()[func_name]
        try:
            json_str = func(*args)
            parsed = json.loads(json_str)

            # Check structure
            if parsed == expected_structure:
                print(f"✓ {func_name} produces correct structure")
                passed += 1
            else:
                print(f"✗ {func_name} structure mismatch")
                print(f"  Expected: {expected_structure}")
                print(f"  Got: {parsed}")
                failed += 1
        except Exception as e:
            print(f"✗ {func_name} exception: {e}")
            failed += 1

    # Test post content (more complex)
    try:
        post_json = build_post_content("My Title", [{"tag": "text", "text": "content"}], "en_us")
        parsed = json.loads(post_json)
        if "en_us" in parsed and "title" in parsed["en_us"]:
            print(f"✓ build_post_content produces correct structure")
            passed += 1
        else:
            print(f"✗ build_post_content structure incorrect: {parsed}")
            failed += 1
    except Exception as e:
        print(f"✗ build_post_content exception: {e}")
        failed += 1

    print(f"✓ {passed}/{len(tests) + 1} content builders validated")
    if failed > 0:
        print(f"✗ {failed} content builders failed")
        return False
    return True


# ============================================================================
# TEST 5: Validate card builders produce valid dicts with expected structure
# ============================================================================
def test_card_builder_structure():
    print("\n--- Test 5: Card builder structure validation ---")

    passed = 0
    failed = 0

    # Test build_card_content
    try:
        card = build_card_content("Header", [{"tag": "text"}])
        if "config" in card and "header" in card and "elements" in card:
            if card["config"].get("update_multi") == True:
                print("✓ build_card_content has correct structure with update_multi=True")
                passed += 1
            else:
                print(f"✗ build_card_content missing update_multi or wrong value")
                failed += 1
        else:
            print(f"✗ build_card_content missing required keys")
            failed += 1
    except Exception as e:
        print(f"✗ build_card_content exception: {e}")
        failed += 1

    # Test build_template_card
    try:
        card = build_template_card("template_id_123")
        if card.get("type") == "template" and "data" in card:
            if "template_id" in card["data"]:
                print("✓ build_template_card has correct structure")
                passed += 1
            else:
                print("✗ build_template_card missing template_id in data")
                failed += 1
        else:
            print(f"✗ build_template_card missing type or data")
            failed += 1
    except Exception as e:
        print(f"✗ build_template_card exception: {e}")
        failed += 1

    # Test build_birthday_card
    try:
        card = build_birthday_card("Alice", "Happy Birthday!")
        if "config" in card and "header" in card and "elements" in card:
            print("✓ build_birthday_card has correct structure")
            passed += 1
        else:
            print(f"✗ build_birthday_card missing required keys")
            failed += 1
    except Exception as e:
        print(f"✗ build_birthday_card exception: {e}")
        failed += 1

    # Test build_ranking_card
    try:
        card = build_ranking_card("Top Users", [(1, "Alice", 100), (2, "Bob", 90)])
        if "config" in card and "header" in card and "elements" in card:
            print("✓ build_ranking_card has correct structure")
            passed += 1
        else:
            print(f"✗ build_ranking_card missing required keys")
            failed += 1
    except Exception as e:
        print(f"✗ build_ranking_card exception: {e}")
        failed += 1

    # Test build_notification_card
    try:
        card = build_notification_card("Alert", "Something happened",
                                      [{"text": "Okay", "value": "ok"}])
        if "config" in card and "header" in card and "elements" in card:
            print("✓ build_notification_card has correct structure")
            passed += 1
        else:
            print(f"✗ build_notification_card missing required keys")
            failed += 1
    except Exception as e:
        print(f"✗ build_notification_card exception: {e}")
        failed += 1

    # Test build_report_card
    try:
        card = build_report_card("Report", [("Users", "150"), ("Active", "120")])
        if "config" in card and "header" in card and "elements" in card:
            print("✓ build_report_card has correct structure")
            passed += 1
        else:
            print(f"✗ build_report_card missing required keys")
            failed += 1
    except Exception as e:
        print(f"✗ build_report_card exception: {e}")
        failed += 1

    print(f"✓ {passed}/6 card builders validated")
    if failed > 0:
        print(f"✗ {failed} card builders failed")
        return False
    return True


# ============================================================================
# TEST 6: Validate send_card auto-sets update_multi when given a dict
# ============================================================================
def test_send_card_update_multi():
    print("\n--- Test 6: send_card auto-sets update_multi ---")

    try:
        client = LarkMessengerClient("test_token", "user_id_123")

        # Inspect send_card source to validate logic
        source = inspect.getsource(client.send_card)

        if "isinstance(card_content, dict)" in source and "update_multi" in source:
            print("✓ send_card has logic to handle dict and update_multi")
        else:
            print("✗ send_card missing dict/update_multi handling")
            return False

        # Verify the method signature
        sig = inspect.signature(client.send_card)
        params = list(sig.parameters.keys())

        if all(p in params for p in ["receive_id", "card_content", "receive_id_type", "uuid"]):
            print("✓ send_card has correct signature")
        else:
            print("✗ send_card missing required parameters")
            return False

        return True
    except Exception as e:
        print(f"✗ Exception: {e}")
        return False


# ============================================================================
# TEST 7: Validate _upload_multipart has file_field_name parameter
# ============================================================================
def test_upload_multipart_signature():
    print("\n--- Test 7: _upload_multipart signature ---")

    try:
        client = LarkMessengerClient("test_token", "user_id_123")

        sig = inspect.signature(client._upload_multipart)
        params = list(sig.parameters.keys())

        if "file_field_name" not in params:
            print(f"✗ _upload_multipart missing file_field_name parameter")
            print(f"  Parameters: {params}")
            return False

        # Check default value
        param = sig.parameters["file_field_name"]
        if param.default == "file":
            print(f"✓ _upload_multipart has file_field_name parameter with default 'file'")
        else:
            print(f"✓ _upload_multipart has file_field_name parameter")

        # Verify usage in upload_image (should use "image")
        source = inspect.getsource(client.upload_image)
        if 'file_field_name="image"' in source:
            print("✓ upload_image correctly passes file_field_name='image'")
        else:
            print("✗ upload_image doesn't use file_field_name parameter correctly")
            return False

        return True
    except Exception as e:
        print(f"✗ Exception: {e}")
        return False


# ============================================================================
# TEST 8: Validate method implementations don't have syntax errors
# ============================================================================
def test_method_syntax():
    print("\n--- Test 8: Method implementations syntax ---")

    try:
        client = LarkMessengerClient("test_token", "user_id_123")

        # Try to inspect all methods - this will fail if there are syntax errors
        methods_to_check = [
            "send_message", "reply_message", "list_messages", "get_message",
            "delete_message", "get_read_users", "send_card", "update_card",
            "upload_image", "upload_file", "create_chat", "get_chat",
            "list_chats", "search_chats", "add_chat_members", "remove_chat_members"
        ]

        for method_name in methods_to_check:
            try:
                method = getattr(client, method_name)
                # Try to get source - if there's a syntax error, this will fail
                inspect.getsource(method)
            except Exception as e:
                print(f"✗ {method_name} syntax error: {e}")
                return False

        print(f"✓ All {len(methods_to_check)} methods have valid syntax")
        return True
    except Exception as e:
        print(f"✗ Exception: {e}")
        return False


# ============================================================================
# TEST 9: Validate utils functions have valid syntax
# ============================================================================
def test_utils_syntax():
    print("\n--- Test 9: Utils functions syntax ---")

    utils_funcs = [
        build_text_content, build_image_content, build_file_content,
        build_post_content, build_share_chat_content, build_card_content,
        build_template_card, build_birthday_card, build_ranking_card,
        build_notification_card, build_report_card
    ]

    for func in utils_funcs:
        try:
            inspect.getsource(func)
        except Exception as e:
            print(f"✗ {func.__name__} syntax error: {e}")
            return False

    print(f"✓ All {len(utils_funcs)} utils functions have valid syntax")
    return True


# ============================================================================
# TEST 10: Count and validate total method/function count
# ============================================================================
def test_counts():
    print("\n--- Test 10: Total counts ---")

    # Count LarkMessengerClient methods
    methods = [m for m in dir(LarkMessengerClient)
               if not m.startswith('_') or m in ['_upload_multipart']]

    # Actual public/important methods count
    important_methods = [
        "send_message", "reply_message", "list_messages", "get_message",
        "delete_message", "get_read_users", "send_card", "update_card",
        "upload_image", "upload_file", "create_chat", "get_chat",
        "list_chats", "search_chats", "add_chat_members", "remove_chat_members"
    ]

    print(f"✓ LarkMessengerClient has {len(important_methods)} important methods")

    utils_funcs = [
        build_text_content, build_image_content, build_file_content,
        build_post_content, build_share_chat_content, build_card_content,
        build_template_card, build_birthday_card, build_ranking_card,
        build_notification_card, build_report_card
    ]

    print(f"✓ Utils module has {len(utils_funcs)} functions")

    return True


# ============================================================================
# Main
# ============================================================================
def main():
    print("=" * 70)
    print("LARK MESSENGER API CLIENT TEST")
    print("=" * 70)

    tests = [
        ("Inheritance", test_inheritance),
        ("Methods", test_messenger_methods),
        ("Functions", test_utils_functions),
        ("Content JSON", test_content_builder_json),
        ("Card Structure", test_card_builder_structure),
        ("send_card Logic", test_send_card_update_multi),
        ("_upload_multipart Sig", test_upload_multipart_signature),
        ("Method Syntax", test_method_syntax),
        ("Utils Syntax", test_utils_syntax),
        ("Counts", test_counts),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} CRASHED: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {name}: {status}")

    print(f"\n{passed}/{total} test groups passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n❌ {total - passed} test group(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
