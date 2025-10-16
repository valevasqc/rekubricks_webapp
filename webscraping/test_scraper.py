"""
Test script for webscraper V2 with small sample.
Run this before the full scraper to verify everything works.
"""

import sys
from scrape_moldes import scrape_molde_data, scrape_multiple_moldes
from process_categories import extract_category_from_name, batch_categorize
from generate_images import generate_image_url


def test_single_molde_scrape():
    """Test scraping a single known ID_MOLDE."""
    print("\n🧪 TEST 1: Scraping single ID_MOLDE (3023)")
    print("-" * 50)
    
    result = scrape_molde_data("3023")
    
    if result:
        print(f"✓ Name: {result['name']}")
        print(f"✓ Weight: {result['weight']}")
        return True
    else:
        print("✗ Failed to scrape")
        return False


def test_category_extraction():
    """Test category extraction from various piece names."""
    print("\n🧪 TEST 2: Category extraction")
    print("-" * 50)
    
    test_cases = [
        ("Plate 2 x 4", "PLATE"),
        ("Brick 2 x 2", "BRICK"),
        ("Tile 1 x 1 with Groove", "TILE"),
        ("Slope 45 2 x 1", "SLOPE"),
        ("Minifigure Head", "MINIFIGURE"),
        ("Unknown Piece Type", "MISCELLANEOUS"),
    ]
    
    all_passed = True
    for name, expected in test_cases:
        result = extract_category_from_name(name)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{name}' → {result} (expected: {expected})")
        if result != expected:
            all_passed = False
    
    return all_passed


def test_image_generation():
    """Test image URL generation."""
    print("\n🧪 TEST 3: Image URL generation")
    print("-" * 50)
    
    test_cases = [
        ("3023", "RED", "3023-red"),
        ("3023", "BLUE", "3023-blue"),
        ("4073", "BLACK", "4073-black"),
        ("98138", "TRANS YELLOW", "98138-trans-yellow"),
    ]
    
    for id_molde, color, description in test_cases:
        url = generate_image_url(id_molde, color)
        if url != "N/A":
            print(f"✓ {description}: {url}")
        else:
            print(f"⚠️  {description}: Color not mapped")
    
    return True


def test_small_batch_scrape():
    """Test scraping a small batch of ID_MOLDEs."""
    print("\n🧪 TEST 4: Small batch scrape (3 pieces)")
    print("-" * 50)
    
    test_moldes = ["3023", "3024", "3001"]
    
    molde_data = scrape_multiple_moldes(test_moldes, delay_range=(0.5, 1.0))
    
    if len(molde_data) == len(test_moldes):
        print(f"✓ All {len(test_moldes)} moldes scraped successfully")
        
        # Add categories
        molde_data = batch_categorize(molde_data)
        
        # Display results
        for id_molde, data in molde_data.items():
            print(f"\n  ID: {id_molde}")
            print(f"  Name: {data['name']}")
            print(f"  Weight: {data['weight']}")
            print(f"  Category: {data['category']}")
        
        return True
    else:
        print(f"✗ Only {len(molde_data)}/{len(test_moldes)} moldes scraped")
        return False


def run_all_tests():
    """Run all tests and report results."""
    print("\n" + "=" * 70)
    print("  WEBSCRAPER V2 - TEST SUITE")
    print("=" * 70)
    
    results = {
        "Single Scrape": test_single_molde_scrape(),
        "Category Extraction": test_category_extraction(),
        "Image Generation": test_image_generation(),
        "Batch Scrape": test_small_batch_scrape(),
    }
    
    print("\n" + "=" * 70)
    print("  TEST RESULTS")
    print("=" * 70)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n✅ All tests passed! Ready to run full scraper.")
    else:
        print("\n⚠️  Some tests failed. Review before running full scraper.")
    
    print("=" * 70 + "\n")
    
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
