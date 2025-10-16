"""
Module to extract and match categories from piece names.
Uses predefined category list and intelligent matching.
"""
from categories import categories


def extract_category_from_name(piece_name):
    """
    Extract category from piece name by matching against known categories.
    
    Strategy:
    1. Try exact match with first word (uppercase)
    2. Try partial match with known categories
    3. Handle special cases (e.g., "Curved Slope")
    4. Default to "MISCELLANEOUS" if no match
    
    Args:
        piece_name (str): The full piece name from Bricklink
    
    Returns:
        str: Matched category name
    """
    if not piece_name or piece_name == "N/A":
        return "MISCELLANEOUS"
    
    # Normalize the name to uppercase for matching
    name_upper = piece_name.upper().strip()
    
    # Special handling for multi-word categories
    # Check these first before single-word matching
    multi_word_categories = [
        "CURVED SLOPE",
        "MINIFIGURE",
        "BASEPLATE"
    ]
    
    for category in multi_word_categories:
        if name_upper.startswith(category):
            return category
    
    # Check if first word matches any category
    first_word = name_upper.split()[0] if name_upper.split() else ""
    
    for category in categories:
        if first_word == category:
            return category
    
    # Try partial matching - check if any category appears in the name
    for category in categories:
        if category in name_upper:
            return category
    
    # Default fallback
    return "MISCELLANEOUS"


def batch_categorize(molde_data):
    """
    Add category field to molde data dictionary.
    
    Args:
        molde_data (dict): Dictionary mapping id_molde -> {name, weight}
    
    Returns:
        dict: Updated dictionary with 'category' field added
    """
    print("\n📂 Categorizando piezas...")
    
    for id_molde, data in molde_data.items():
        category = extract_category_from_name(data["name"])
        data["category"] = category
    
    # Print category distribution
    category_counts = {}
    for data in molde_data.values():
        cat = data.get("category", "MISCELLANEOUS")
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    print("\n📊 Distribución de categorías:")
    for cat in sorted(category_counts.keys()):
        print(f"   {cat}: {category_counts[cat]}")
    
    print(f"✓ Categorización completada\n")
    
    return molde_data
