
# RekuBricks Webscraper + Web App

[Enlace a GitHub](https://github.com/valevasqc/rekubricks_webapp)
**Alumnos:** Valeria Vásquez, Pedro Marroquín, Andrés Juárez, Julio Girón, Andrea Nisthal

## Descripción General

Este proyecto tiene **dos componentes principales**:

1. **Webscraper en Python** que obtiene información de piezas LEGO desde [Bricklink](https://www.bricklink.com/) y la guarda en un archivo Excel.
2. **Aplicación web básica con Flask** que lee el archivo Excel generado y muestra las piezas en tarjetas (cards) con imagen, nombre, color y precio (placeholder), además de permitir agregar piezas a un carrito temporal.

El objetivo final es que el usuario pueda seleccionar piezas y **enviar el contenido del carrito por WhatsApp**, sin necesidad de crear cuentas ni iniciar sesión.

---

## Estructura del Proyecto

```
bricklink_webapp/
│
├─ app.py                     # Backend Flask - renderiza la página web con las piezas
│
├─ templates/
│   └─ index.html             # Plantilla principal con Jinja2 (HTML)
│
├─ static/
│   └─ style.css              # Estilos CSS para las tarjetas y layout
│
├─ data/
│   └─ bricklink_pieces.xlsx  # Datos generados por el scraper (entrada de la web)
│
└─ webscraping/              # Módulos auxiliares del scraper
    ├─ webscraping.py        # Script principal de scraping
    ├─ import_excel.py       # Lee datos de inventario local
    └─ color_ids.py         # Diccionario de nombres de color → IDs Bricklink
```

---

## Flujo de Datos

1. **Entrada**:
   Un archivo `datos_inventario.xlsx` opcional, con columnas `ID`, `ID MOLDE`, `COLOR`.
   Se convierte en una lista de piezas usando `import_excel.py`.

2. **Scraping**:
   Por cada pieza:
   * Se busca el `colorID` correspondiente en `color_ids.py`.
   * Se construyen URLs de Bricklink (específicas por color si aplica).
   * Se extraen **nombre**, **imagen**, y **peso** con `BeautifulSoup`.

3. **Salida**:
   Se genera `data/bricklink_pieces.xlsx` con columnas:
   * `Piece_ID`
   * `Piece_Name`
   * `Color`
   * `Image_URL`
   * `Weight`

4. **Visualización Web**:
   Flask lee el Excel y renderiza las piezas como tarjetas con:
   * Imagen
   * Nombre
   * Color
   * Precio (por ahora en 0.0)
   * Botón para agregar al carrito

---

## Dependencias

* Python 3.x
* `Flask`
* `requests`
* `beautifulsoup4`
* `pandas`
* `openpyxl`

Instalación rápida:

```bash
python -m pip install flask requests beautifulsoup4 pandas openpyxl
```

---

## ▶Cómo Ejecutar

1. **Ejecutar el scraper** para actualizar la base de datos:

```bash
cd webscraping
python webscraping.py
```

Esto genera/actualiza `data/bricklink_pieces.xlsx`.

2. **Levantar la aplicación web**:

```bash
cd ..
python app.py
```

3. Visitar en el navegador:
   👉 [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## Estado Actual

**Completado:**

* Scraper funcional con Excel de salida.
* Interfaz básica en Flask mostrando las piezas en tarjetas.

**En desarrollo (siguientes pasos):**

* Implementar el carrito dinámico en la web (JS).
* Introducir precios y calcular total automáticamente.
* Generar mensaje de WhatsApp con: **nombre**, **ID**, **color**, **cantidad**, **precio**.
* (Opcional a futuro) Añadir base de datos para persistencia e inventario en tiempo real.
