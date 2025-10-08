# Bricklink Webscraper (Python)

Alumnos: Valeria Vásquez, Pedro Marroquín, Andrés Juárez, Julio Girón, Andrea Nisthal

## Descripción

Este proyecto obtiene datos de piezas LEGO desde [Bricklink](https://www.bricklink.com/) y los guarda en un archivo Excel. Actualmente extrae:

* **Nombre de la pieza** (`Piece_Name`)
* **Color** (`Color`)
* **URL de la imagen** (`Image_URL`)
* **Peso** (`Weight`)

En la siguiente iteración, se planea crear una **aplicación web simple** que permita visualizar estas piezas, armar un carrito temporal y enviar el contenido del carrito por **WhatsApp**, sin necesidad de iniciar sesión.

---

## Archivos

* **`webscraping.py`**
  Script principal de scraping. Lee la lista de piezas o usando `import_excel()`, obtiene las páginas correspondientes de Bricklink, analiza el HTML con `BeautifulSoup` y guarda los resultados en `bricklink_pieces.xlsx`.

* **`import_excel.py`**
  Función auxiliar que lee `datos_inventario.xlsx` y devuelve una lista de diccionarios con las claves: `ID_COLOR`, `ID_MOLDE`, `COLOR`.

* **`color_ids.py`**
  Diccionario que mapea nombres de colores en mayúsculas a los `colorID` de Bricklink, usado para construir URLs específicas por color.

---

## Flujo de Datos

1. **Entrada:** `datos_inventario.xlsx`. Cada fila representa una pieza LEGO con su color y ID de molde.
2. **Búsqueda de ColorID:** Para cada pieza, el script revisa `color_ids.py` para obtener el `colorID`.
3. **Scraping:**
   * Página específica de color (`catalogItemIn.asp`) para la imagen si existe `colorID`.
   * Página genérica (`catalogitem.page`) siempre usada para obtener nombre de pieza y peso.
4. **Salida:** `bricklink_pieces.xlsx` con columnas:
   * `Piece_ID`
   * `Piece_Name`
   * `Color`
   * `Image_URL`
   * `Weight`

---

## Dependencias

* Python 3.x
* `requests`
* `beautifulsoup4`
* `pandas`
* `openpyxl` (para Excel)

Instalación:

```bash
python -m pip install requests beautifulsoup4 pandas openpyxl
```

---

## Cómo Ejecutar

1. Agrega o actualiza piezas en `pieces` o en `datos_inventario.xlsx`.
2. Ejecuta el scraper:

```bash
python webscraping.py
```

3. El archivo `bricklink_pieces.xlsx` se sobrescribirá en el directorio del proyecto.

---

## Próximos Pasos del Proyecto: Aplicación Web

La siguiente fase es crear una **aplicación web básica** que:

* Muestre las piezas obtenidas desde `bricklink_pieces.xlsx`.
* Permita armar un carrito temporal (sin guardar estado entre recargas).
* Envíe los detalles del carrito por **WhatsApp**.

Esta versión será funcional pero mínima: no tendrá cuentas de usuario, base de datos ni persistencia. Iteraciones futuras podrían incluir **interfaz más atractiva**, **base de datos para inventario** y **manejo de sesiones**.
