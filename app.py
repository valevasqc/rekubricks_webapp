from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

def load_pieces():
    df = pd.read_excel("data/bricklink_pieces.xlsx")
    
    # Handle missing Price column gracefully
    if "Price" not in df.columns:
        df["Price"] = 0.0
    
    # Handle missing Category column gracefully
    if "Category" not in df.columns:
        df["Category"] = "Sin categoría"
    
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
    df['Piece_ID'] = df['Piece_ID'].astype(str).str.strip()
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
    
    pieces = df.to_dict(orient="records")
    return pieces

def get_categories():
    df = pd.read_excel("data/bricklink_pieces.xlsx")
    
    # Handle missing Category column gracefully
    if "Category" not in df.columns:
        return ["Sin categoría"]
    
    # Get unique categories, excluding NaN values
    categories = df["Category"].dropna().unique().tolist()
    return sorted(categories)

@app.route("/")
def index():
    pieces = load_pieces()
    categories = get_categories()
    
    # Debug: print first few pieces to see what we're getting
    print("Debug - First 3 pieces:")
    for i, piece in enumerate(pieces[:3]):
        print(f"Piece {i+1}: {piece}")
    
    print(f"Debug - Total pieces: {len(pieces)}")
    print(f"Debug - Categories: {categories}")
    
    return render_template("index.html", pieces=pieces, categories=categories)

if __name__ == "__main__":
    app.run(debug=True)
