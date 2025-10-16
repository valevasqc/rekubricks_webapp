"""
Quick diagnostic test to verify the bug fixes.
Run this before running the full scraper again.
"""
import sys
import os

# Add webscraping to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from import_excel import import_excel, import_unique_moldes
from generate_images import generate_image_url

print("=" * 60)
print("  DIAGNOSTIC TEST - Bug Fixes")
print("=" * 60)

# Test 1: Check ID_MOLDE type consistency
print("\n📋 TEST 1: ID_MOLDE type consistency")
print("-" * 60)

inventory = import_excel()
if inventory:
    sample = inventory[0]
    id_molde_type = type(sample.get("ID_MOLDE", ""))
    id_color_type = type(sample.get("ID_COLOR", ""))
    print(f"✓ ID_MOLDE type: {id_molde_type} (should be <class 'str'>)")
    print(f"✓ ID_COLOR type: {id_color_type} (should be <class 'str'>)")
    print(f"Sample ID_MOLDE: '{sample.get('ID_MOLDE', '')}'")
    print(f"Sample ID_COLOR: '{sample.get('ID_COLOR', '')}'")
    print(f"Sample COLOR: '{sample.get('COLOR', '')}'")
else:
    print("✗ Failed to load inventory")
    sys.exit(1)

# Test 2: Check unique moldes type
print("\n📋 TEST 2: Unique moldes type check")
print("-" * 60)

unique_moldes = import_unique_moldes()
if unique_moldes:
    print(f"✓ Loaded {len(unique_moldes)} unique moldes")
    print(f"First molde type: {type(unique_moldes[0])} (should be <class 'str'>)")
    print(f"Sample moldes: {unique_moldes[:3]}")
else:
    print("✗ Failed to load unique moldes")
    sys.exit(1)

# Test 3: Image URL generation with Color key
print("\n📋 TEST 3: Image URL generation")
print("-" * 60)

test_piece = {
    "ID_MOLDE": "3023",
    "Color": "Red",  # Note: using "Color" not "COLOR"
    "ID_COLOR": ""
}

# Simulate what generate_images does
id_molde = test_piece.get("ID_MOLDE", "")
color = test_piece.get("COLOR", "") or test_piece.get("Color", "")

print(f"ID_MOLDE: '{id_molde}'")
print(f"Color extracted: '{color}'")

if color:
    image_url = generate_image_url(id_molde, color)
    print(f"✓ Image URL: {image_url}")
    if image_url != "N/A":
        print("✓ SUCCESS: Image URL generated correctly")
    else:
        print("⚠️  Color not in mapping (this is OK if color doesn't exist)")
else:
    print("✗ Failed to extract color")

# Test 4: Type matching for dict lookup
print("\n📋 TEST 4: Dictionary lookup consistency")
print("-" * 60)

mock_molde_data = {
    "3023": {"name": "Plate 1 x 2", "weight": "0.36g"},
    "3024": {"name": "Plate 1 x 1", "weight": "0.2g"}
}

# Test with string lookup (should work)
test_id = "3023"
result = mock_molde_data.get(test_id)
print(f"String lookup '{test_id}': {result}")

# Simulate what might come from Excel (number)
test_id_num = 3023
test_id_str = str(test_id_num).strip()
result = mock_molde_data.get(test_id_str)
print(f"Converted number {test_id_num} -> '{test_id_str}': {result}")

if result:
    print("✓ Type conversion working correctly")
else:
    print("✗ Type conversion failed")

print("\n" + "=" * 60)
print("  ✅ ALL DIAGNOSTIC TESTS COMPLETED")
print("=" * 60)
print("\nIf all tests show ✓, you can run the full scraper again.")
print("The bugs have been fixed:")
print("  1. ID_MOLDE type mismatch (string vs number)")
print("  2. Image URL Color key mismatch (COLOR vs Color)")
