"""Generate image URLs without HTTP using color_ids and Bricklink patterns."""
from typing import List, Dict
from color_ids import color_ids


def generate_image_url(id_molde: str, color_name: str, id_color: str | None = None) -> str:
    """
    Generate Bricklink image URL without making HTTP requests.
    
    URL Pattern: https://img.bricklink.com/P/{color_id}/{id_molde}.jpg
    
    Args:
        id_molde (str): The piece mold ID
        color_name (str): Color name (will be normalized to uppercase)
        id_color (str): Optional specific color ID override
    
    Returns:
        str: Image URL or "N/A" if color_id cannot be determined
    """
    # Prefer provided numeric ID_COLOR when available
    if id_color and str(id_color).strip().isdigit():
        color_id = str(id_color).strip()
    else:
        # Normalize color name and map to ID
        color_normalized = color_name.strip().upper()
        color_id = color_ids.get(color_normalized, None)
    
    if color_id:
        # Use standard Bricklink image URL pattern
        return f"https://img.bricklink.com/P/{color_id}/{id_molde}.jpg"
    else:
        # If color not in mapping, cannot generate URL without scraping
        return "N/A"


def batch_generate_image_urls(pieces_list: List[Dict]) -> List[Dict]:
    """
    Generate image URLs for a list of pieces.
    
    Args:
        pieces_list (list): List of piece dicts with keys:
            - ID_MOLDE
            - COLOR
            - ID_COLOR (optional)
    
    Returns:
        list: Same list with 'Image_URL' field added
    """
    print("\n🖼️  Generando URLs de imágenes...")
    
    total = len(pieces_list)
    generated = 0
    failed = 0
    
    for piece in pieces_list:
        id_molde = piece.get("ID_MOLDE", "")
        # Handle both "COLOR" (from import_excel) and "Color" (from merge function)
        color = piece.get("COLOR", "") or piece.get("Color", "")
        id_color = piece.get("ID_COLOR", "")
        
        image_url = generate_image_url(id_molde, color, id_color)
        piece["Image_URL"] = image_url
        
        if image_url != "N/A":
            generated += 1
        else:
            failed += 1
    
    print(f"✓ URLs generadas: {generated}/{total}")
    if failed > 0:
        print(f"⚠️  URLs no generadas (color no mapeado): {failed}/{total}")
    print()
    
    return pieces_list
