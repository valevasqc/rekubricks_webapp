# === LEER DATOS DEL INVENTARIO DESDE EXCEL ===
import pandas as pd
import os

def import_excel():
    # Get the project root directory (one level up from webscraping folder)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    excel_path = os.path.join(project_root, "data", "datos_inventario.xlsx")
    
    inventory_df = pd.read_excel(excel_path)
    inventory_df.columns = [col.strip().upper() for col in inventory_df.columns] 

    inventory_df = inventory_df.rename(columns={ # Renombrar según los nombres de columnas
        "ID": "ID_COLOR",       
        "ID MOLDE": "ID_MOLDE",
        "COLOR": "COLOR"
    })

    inventory_df = inventory_df.fillna("")
    pieces = inventory_df.to_dict(orient="records")
    print(f"Se cargaron {len(pieces)} piezas desde el Excel.")
    return pieces