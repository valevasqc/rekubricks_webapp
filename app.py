"""RekuBricks Web Application.

Flask backend that reads piece data from Excel and renders a catalog
with a client-side cart and WhatsApp integration.
"""
from typing import List, Dict, Optional
from flask import Flask, render_template
import pandas as pd
import os

# TODO: flesh out UI --- IGNORE ---
app = Flask(__name__)

EXCEL_PATH = "data/bricklink_pieces.xlsx"
# TODO: connect to SQL --- IGNORE ---

# Global cache to store loaded data (loaded once at startup)
_pieces_cache: Optional[List[Dict]] = None
_categories_cache: Optional[List[str]] = None

def load_pieces() -> List[Dict]:
    """Load and clean piece data from the Excel file.

    Returns a list of row dicts ready for rendering; applies defensive
    defaults for missing columns and values.
    
    Uses cache if available to avoid reloading on every request.
    """
    global _pieces_cache
    
    # Return cached data if available
    if _pieces_cache is not None:
        return _pieces_cache
    
    print("Loading pieces from Excel (this should only happen once)...")
    df = pd.read_excel(EXCEL_PATH)
    
    # Handle missing Price column gracefully
    if "Price" not in df.columns:
        df["Price"] = 0.0
    
    # Handle missing Category column gracefully
    if "Category" not in df.columns:
        df["Category"] = "Otros"
    
    # Handle missing ID columns gracefully (for backward compatibility)
    if "ID_COLOR" not in df.columns:
        df["ID_COLOR"] = ""
    if "ID_MOLDE" not in df.columns:
        df["ID_MOLDE"] = df["Piece_ID"]  # Use Piece_ID as fallback
    
    # Clean and validate data
    df = df.dropna(subset=['Piece_ID', 'Piece_Name'])  # Remove rows without essential data
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0.0)  # Convert price to numeric
    df['Image_URL'] = df['Image_URL'].fillna('N/A')  # Handle missing images
    df['Color'] = df['Color'].fillna('Sin color')  # Handle missing colors
    df['Category'] = df['Category'].fillna('Sin categoría')  # Handle missing categories
    df['ID_COLOR'] = df['ID_COLOR'].fillna('')  # Handle missing ID_COLOR
    df['ID_MOLDE'] = df['ID_MOLDE'].fillna('')  # Handle missing ID_MOLDE
    
    # Convert to string and clean special characters
    df['Piece_ID'] = df['Piece_ID'].astype(str).str.strip() # TODO: consieder using only ID_MOLDE+COLOR instead
    df['Piece_Name'] = df['Piece_Name'].astype(str).str.strip()
    df['Color'] = df['Color'].astype(str).str.strip()
    df['Category'] = df['Category'].astype(str).str.strip()
    df['Image_URL'] = df['Image_URL'].astype(str).str.strip()
    df['ID_COLOR'] = df['ID_COLOR'].astype(str).str.strip().replace('nan', '')  # Convert NaN string to empty
    df['ID_MOLDE'] = df['ID_MOLDE'].astype(str).str.strip().replace('nan', '')  # Convert NaN string to empty
    
    # Remove any rows where essential fields are empty after cleaning
    df = df[df['Piece_ID'] != '']
    df = df[df['Piece_Name'] != '']
    df = df[df['Image_URL'] != '']
    df = df[df['Image_URL'] != 'N/A']
    
    # Cache the results
    _pieces_cache = df.to_dict(orient="records")
    print(f"Loaded and cached {len(_pieces_cache)} pieces")
    
    return _pieces_cache

def get_categories() -> List[str]:
    """Extract unique categories from the Excel file.

    Returns a sorted list of unique category names; if the column is
    missing, returns the fallback category.
    
    Uses cache if available to avoid reloading on every request.
    """
    global _categories_cache
    
    # Return cached data if available
    if _categories_cache is not None:
        return _categories_cache
    
    print("Loading categories from Excel (this should only happen once)...")
    df = pd.read_excel(EXCEL_PATH)
    
    # Handle missing Category column gracefully
    if "Category" not in df.columns:
        _categories_cache = ["Sin categoría"]
        return _categories_cache
    
    # Get unique categories, excluding NaN values
    categories = df["Category"].dropna().unique().tolist()
    _categories_cache = sorted(categories)
    print(f"Loaded and cached {len(_categories_cache)} categories")
    
    return _categories_cache

def warmup_cache():
    """Preload data into cache on application startup."""
    print("=" * 60)
    print("WARMUP: Preloading data into cache...")
    print("=" * 60)
    load_pieces()
    get_categories()
    print("=" * 60)
    print("WARMUP: Complete! Application ready to serve requests.")
    print("=" * 60)

@app.route("/")
def index():
    """Main route that loads pieces and renders the catalog page."""
    pieces = load_pieces()
    categories = get_categories()
    return render_template("index.html", pieces=pieces, categories=categories)

# Warmup cache when app starts
warmup_cache()

if __name__ == "__main__":
    # For local development only
    # In production (Render), use: gunicorn app:app
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)