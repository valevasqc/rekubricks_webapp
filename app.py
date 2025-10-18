"""RekuBricks Web Application.

Flask backend that reads piece data from Excel and renders a catalog
with a client-side cart and WhatsApp integration.
"""
from typing import List, Dict
from flask import Flask, render_template
import pandas as pd
import os
from waitress import serve  
# TODO: flesh out UI

app = Flask(__name__)

EXCEL_PATH = "data/bricklink_pieces.xlsx"
# TODO: connect to SQL

def load_pieces() -> List[Dict]:
    """Load and clean piece data from the Excel file.

    Returns a list of row dicts ready for rendering; applies defensive
    defaults for missing columns and values.
    """
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
    
    return df.to_dict(orient="records")

def get_categories() -> List[str]:
    """Extract unique categories from the Excel file.

    Returns a sorted list of unique category names; if the column is
    missing, returns the fallback category.
    """
    df = pd.read_excel(EXCEL_PATH)
    
    # Handle missing Category column gracefully
    if "Category" not in df.columns:
        return ["Sin categoría"]
    
    # Get unique categories, excluding NaN values
    categories = df["Category"].dropna().unique().tolist()
    return sorted(categories)

@app.route("/")
def index():
    """Main route that loads pieces and renders the catalog page."""
    pieces = load_pieces()
    categories = get_categories()
    return render_template("index.html", pieces=pieces, categories=categories)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # fallback for local dev
    serve(app, host="0.0.0.0", port=port)