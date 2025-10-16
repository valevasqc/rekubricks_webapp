"""Optimized Bricklink Webscraper (V2).

Purpose
-------
Scrape unique molds (ID_MOLDE) from Bricklink to collect name and weight,
categorize pieces, merge with local inventory (all color variants), and
generate image URLs without per-color HTTP requests.

Highlights
----------
- Scrapes only ~1000 unique ID_MOLDEs (instead of 4000+ variants)
- Reuses scraped data across color variants
- Generates image URLs via color_ids mapping (no requests)
- Reduces scraping time and minimizes ban risk

Inputs
------
- data/id_molde.xlsx: Unique mold IDs (~1000 entries)
- data/datos_inventario.xlsx: Full inventory with color variants (~4000+)
- webscraping/categories.py: Predefined category list

Output
------
- data/bricklink_pieces.xlsx: Dataset compatible with the Flask app
"""

import pandas as pd
import os
from typing import Dict, List, Any
from import_excel import import_excel, import_unique_moldes
from scrape_moldes import scrape_multiple_moldes
from process_categories import batch_categorize
from generate_images import batch_generate_image_urls


def merge_molde_data_with_inventory(molde_data: Dict[str, Dict[str, Any]],
                                    inventory_pieces: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Merge scraped ID_MOLDE data with full inventory (all color variants).

    Args:
        molde_data: Scraped data keyed by id_molde with fields {name, weight, category}.
        inventory_pieces: Full inventory records with color variants.

    Returns:
        Complete piece records ready for export to Excel.
    """
    print("\n🔄 Fusionando datos de moldes con inventario completo...")
    
    results = []
    missing_moldes = set()
    
    for piece in inventory_pieces:
        id_molde = str(piece.get("ID_MOLDE", "")).strip()
        id_color = str(piece.get("ID_COLOR", "")).strip()
        color = piece.get("COLOR", "")
        
        # Get molde data (name, weight, category)
        if id_molde and id_molde in molde_data:
            molde_info = molde_data[id_molde]
            piece_name = molde_info.get("name", "N/A")
            weight = molde_info.get("weight", "N/A")
            category = molde_info.get("category", "MISCELLANEOUS")
        else:
            # Molde not found in scraped data
            piece_name = "N/A"
            weight = "N/A"
            category = "MISCELLANEOUS"
            missing_moldes.add(id_molde)
        
    # Determine Piece_ID for frontend compatibility
    # Use ID_COLOR if exists, otherwise use ID_MOLDE
        piece_id = id_color if id_color else id_molde
        
        results.append({
            "Piece_ID": piece_id,
            "ID_COLOR": id_color,
            "ID_MOLDE": id_molde,
            "Piece_Name": piece_name,
            "Color": color.title() if color else "",
            "Weight": weight,
            "Category": category,
            "Price": ""  # Default price - to be set manually
        })
    
    if missing_moldes:
        print(f"⚠️  {len(missing_moldes)} ID_MOLDEs no encontrados en datos scrapeados")
    
    print(f"✓ Fusión completada: {len(results)} piezas generadas\n")
    
    return results


def save_to_excel(pieces_data: List[Dict[str, Any]], output_filename: str = "bricklink_pieces.xlsx") -> str:
    """Save processed data to an Excel file.

    Args:
        pieces_data: List of piece dictionaries.
        output_filename: Output filename (without path).

    Returns:
        Full path to the saved file.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    output_path = os.path.join(project_root, "data", output_filename)
    
    df = pd.DataFrame(pieces_data)
    
    # Ensure column order matches expected format
    column_order = [
        "Piece_ID",
        "ID_COLOR", 
        "ID_MOLDE",
        "Piece_Name",
        "Color",
        "Image_URL",
        "Weight",
        "Category",
        "Price"
    ]
    
    # Reorder columns if present
    existing_cols = [col for col in column_order if col in df.columns]
    df = df[existing_cols]
    
    df.to_excel(output_path, index=False)
    
    return output_path


def main() -> None:
    """Main execution pipeline for the optimized webscraper."""
    print("\n" + "=" * 70)
    print("  REKUBRICKS WEBSCRAPER V2 - Optimized")
    print("=" * 70)
    
    # Step 1: Load unique ID_MOLDEs for scraping
    print("\n📥 PASO 1: Cargar IDs únicos")
    print("-" * 70)
    unique_moldes = import_unique_moldes()
    
    if not unique_moldes:
        print("❌ No se pudieron cargar ID_MOLDEs. Abortando.")
        return
    
    # Step 2: Scrape data for unique moldes only
    print("\n🌐 PASO 2: Scraping de ID_MOLDEs únicos")
    print("-" * 70)
    molde_data = scrape_multiple_moldes(unique_moldes)
    
    # Step 3: Extract and assign categories
    print("\n📂 PASO 3: Extraer categorías")
    print("-" * 70)
    molde_data = batch_categorize(molde_data)
    
    # Step 4: Load full inventory with color variants
    print("\n📥 PASO 4: Cargar inventario completo")
    print("-" * 70)
    inventory_pieces = import_excel()
    
    # Step 5: Merge molde data with inventory
    print("\n🔀 PASO 5: Fusionar datos")
    print("-" * 70)
    complete_pieces = merge_molde_data_with_inventory(molde_data, inventory_pieces)
    
    # Step 6: Generate image URLs (no HTTP requests)
    print("\n🖼️  PASO 6: Generar URLs de imágenes")
    print("-" * 70)
    complete_pieces = batch_generate_image_urls(complete_pieces)
    
    # Step 7: Save to Excel
    print("\n💾 PASO 7: Guardar resultados")
    print("-" * 70)
    output_path = save_to_excel(complete_pieces)
    
    # Summary
    print("\n" + "=" * 70)
    print("  ✅ SCRAPING COMPLETADO")
    print("=" * 70)
    print(f"📊 Total de piezas procesadas: {len(complete_pieces)}")
    print(f"📊 ID_MOLDEs únicos scrapeados: {len(molde_data)}")
    print(f"📄 Archivo guardado: {output_path}")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
