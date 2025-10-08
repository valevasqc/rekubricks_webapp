import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from color_ids import color_ids
from import_excel import import_excel

pieces = import_excel()
# pieces = [
#     {"ID_COLOR": "", "ID_MOLDE": "4073", "COLOR": "BLACK"},
#     {"ID_COLOR": "", "ID_MOLDE": "98138", "COLOR": "TRANS YELLOW"},
#     {"ID_COLOR": "302301", "ID_MOLDE": "3023", "COLOR": "WHITE"}
# ]

results = []
headers = {"User-Agent": "Mozilla/5.0"}

for piece in pieces:
    pid = piece["ID_MOLDE"]
    color_name = piece["COLOR"].strip().upper()

    # === COLOR ID ===
    color_id = color_ids.get(color_name, None)

    # Página general siempre para nombre y peso
    general_url = f"https://www.bricklink.com/v2/catalog/catalogitem.page?P={pid}"
    general_resp = requests.get(general_url, headers=headers)
    if general_resp.status_code != 200:
        print(f"Error al acceder {pid}")
        results.append({
            "Piece_ID": pid,
            "Piece_Name": "N/A",
            "Color": piece["COLOR"].title(),
            "Image_URL": "N/A",
            "Weight": "N/A"
        })
        continue

    general_soup = BeautifulSoup(general_resp.text, "html.parser")

    # === NOMBRE DE LA PIEZA ===
    title_tag = general_soup.find("h1", {"id": "item-name-title"})
    piece_name = title_tag.text.strip() if title_tag else "N/A"

    # === PESO ===
    weight_tag = general_soup.find("span", {"id": "item-weight-info"})
    weight = weight_tag.text.strip() if weight_tag else "N/A"

    # === IMAGEN ===
    if color_id:
        # URL directa al color-specific image
        img_url = f"https://img.bricklink.com/P/{color_id}/{pid}.jpg"
    else:
        img_tag = general_soup.select_one("td.pciMainImageHolder img")
        img_src = img_tag.get("src") if img_tag else ""
        img_url = "https:" + img_src if img_src and not img_src.startswith("http") else img_src
        if not img_url:
            img_url = "N/A"

    # === GUARDAR DATOS ===
    results.append({
        "Piece_ID": pid,
        "Piece_Name": piece_name,          
        "Color": piece["COLOR"].title(),  
        "Image_URL": img_url,
        "Weight": weight
    })

    print(f"Scraping {pid} ({piece['COLOR'].title()})...")

    time.sleep(1.5 + random.random())  # Respetar al sitio

# Guardar en Excel (sobrescribe si existe)
df = pd.DataFrame(results)
df.to_excel("bricklink_pieces.xlsx", index=False)

print("Scraping completado. Archivo guardado como 'bricklink_pieces.xlsx'")
