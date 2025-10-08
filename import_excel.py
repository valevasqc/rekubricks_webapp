# === LEER DATOS DEL INVENTARIO DESDE EXCEL ===
import pandas as pd

def import_excel():
    inventory_df = pd.read_excel("datos_inventario.xlsx")
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