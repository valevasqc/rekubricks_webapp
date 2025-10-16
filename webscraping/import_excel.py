# === LEER DATOS DEL INVENTARIO DESDE EXCEL ===
import pandas as pd
import os


def import_excel():
    """
    Import full inventory with all color variants from datos_inventario.xlsx.
    
    Returns:
        list: List of piece dictionaries with ID_COLOR, ID_MOLDE, COLOR
    """
    # Get the project root directory (one level up from webscraping folder)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    excel_path = os.path.join(project_root, "data", "datos_inventario.xlsx")
    
    inventory_df = pd.read_excel(excel_path)
    inventory_df.columns = [col.strip().upper() for col in inventory_df.columns] 

    inventory_df = inventory_df.rename(columns={
        "ID": "ID_COLOR",       
        "ID MOLDE": "ID_MOLDE",
        "COLOR": "COLOR"
    })

    inventory_df = inventory_df.fillna("")
    
    # Convert ID_MOLDE and ID_COLOR to strings to match scraper format
    inventory_df["ID_MOLDE"] = inventory_df["ID_MOLDE"].astype(str).str.strip()
    inventory_df["ID_COLOR"] = inventory_df["ID_COLOR"].astype(str).str.strip()
    
    # Remove 'nan' string values
    inventory_df["ID_MOLDE"] = inventory_df["ID_MOLDE"].replace('nan', '')
    inventory_df["ID_COLOR"] = inventory_df["ID_COLOR"].replace('nan', '')
    
    pieces = inventory_df.to_dict(orient="records")
    print(f"✓ Se cargaron {len(pieces)} piezas desde datos_inventario.xlsx")
    return pieces


def import_unique_moldes():
    """
    Import unique ID_MOLDEs from id_molde.xlsx for scraping.
    
    Returns:
        list: List of unique ID_MOLDE strings
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    excel_path = os.path.join(project_root, "data", "id_molde.xlsx")
    
    try:
        moldes_df = pd.read_excel(excel_path)
        # Normalize column names
        moldes_df.columns = [col.strip().upper() for col in moldes_df.columns]
        
        # Try common column name variations
        if "ID_MOLDE" in moldes_df.columns:
            moldes = moldes_df["ID_MOLDE"].astype(str).str.strip().unique().tolist()
        elif "ID MOLDE" in moldes_df.columns:
            moldes = moldes_df["ID MOLDE"].astype(str).str.strip().unique().tolist()
        elif "MOLDE" in moldes_df.columns:
            moldes = moldes_df["MOLDE"].astype(str).str.strip().unique().tolist()
        else:
            # Use first column as fallback
            moldes = moldes_df.iloc[:, 0].astype(str).str.strip().unique().tolist()
        
        # Remove empty strings and 'nan'
        moldes = [m for m in moldes if m and m.lower() != 'nan']
        
        print(f"✓ Se cargaron {len(moldes)} ID_MOLDEs únicos desde id_molde.xlsx")
        return moldes
    
    except FileNotFoundError:
        print("⚠️  Archivo id_molde.xlsx no encontrado. Extrayendo IDs únicos de datos_inventario.xlsx...")
        # Fallback: extract unique moldes from full inventory
        pieces = import_excel()
        moldes = list(set([p["ID_MOLDE"] for p in pieces if p["ID_MOLDE"]]))
        print(f"✓ Se extrajeron {len(moldes)} ID_MOLDEs únicos del inventario completo")
        return moldes
    except Exception as e:
        print(f"❌ Error al leer id_molde.xlsx: {e}")
        return []