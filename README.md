
# RekuBricks - Catálogo Web de Piezas LEGO

[Enlace a GitHub](https://github.com/valevasqc/rekubricks_webapp)

**Alumnos:** Valeria Vásquez, Pedro Marroquín, Andrés Juárez, Julio Girón, Andrea Nisthal  

---

## Descripción del Proyecto

**RekuBricks** es una aplicación web completa para la venta de piezas LEGO que combina:

1. **Webscraper automatizado** que extrae información de piezas desde [Bricklink.com](https://www.bricklink.com/)
2. **Aplicación web** con catálogo interactivo, carrito de compras y sistema de pedidos
3. **Integración con WhatsApp** para facilitar el proceso de venta

El objetivo es crear una plataforma **simple y funcional** donde los clientes puedan navegar piezas LEGO, agregarlas a un carrito y realizar pedidos a través de WhatsApp **sin necesidad de registro**.

---

## Arquitectura del Sistema

```
rekubricks_webapp/
│
├── 🚀 app.py                     # Backend Flask - servidor principal
│
├── 📂 templates/
│   └── index.html                # Interfaz principal (HTML + Jinja2)
│
├── 📂 static/
│   ├── style.css                 # Estilos CSS responsivos
│   ├── script.js                 # Lógica JavaScript (carrito, búsqueda, WhatsApp)
│   └── logo.png                  # Logo de la marca
│
├── 📂 data/
│   ├── bricklink_pieces.xlsx     # Base de datos principal (generada por scraper)
│   └── datos_inventario.xlsx     # Inventario de entrada (opcional)
│
└── 📂 webscraping/               # Módulo de extracción de datos
    ├── webscraping.py            # Orquestador del scraping (por ID_MOLDE)
    ├── scrape_moldes.py          # Extrae nombre y peso por ID_MOLDE
    ├── generate_images.py        # Genera URLs de imagen por color (sin requests)
    ├── process_categories.py     # Clasifica piezas por categoría
    ├── import_excel.py           # Procesador de inventario local (IDs/colores)
    ├── categories.py             # Lista de categorías
    └── color_ids.py              # Mapeo de colores a IDs de Bricklink
```

---

## Flujo de Datos

### 1. **Extracción de Datos (Webscraping)**
```
datos_inventario.xlsx → webscraping.py → Bricklink (scraping) → bricklink_pieces.xlsx
```

- Lee inventario local con columnas: `ID`, `ID_COLOR`, `ID_MOLDE`, `COLOR`
- Mapea colores a IDs numéricos usando `color_ids.py`
- Extrae de Bricklink nombre y peso por `ID_MOLDE` (menos requests, con rate limiting)
- Genera URLs de imagen por color sin requests usando `color_ids.py`
- Genera Excel final con: `Piece_ID`, `ID_COLOR`, `ID_MOLDE`, `Piece_Name`, `Color`, `Image_URL`, `Weight`, `Category`, `Price`

### 2. **Procesamiento Web (Flask + Pandas)**
```
bricklink_pieces.xlsx → app.py → HTML dinámico
```

- Carga y limpia datos (manejo de valores NaN, validación)
- Extrae categorías automáticamente
- Renderiza tarjetas con información completa

### 3. **Interacción del Usuario (Frontend)**
```
Navegación → Búsqueda/Filtros → Carrito → WhatsApp
```

- **Búsqueda en tiempo real** por nombre, color o ID
- **Filtros por categoría** dinámicos
- **Carrito persistente** (localStorage)
- **Generación automática** de mensaje de WhatsApp

---


## Instrucciones de Ejecución

### **Requisitos Previos**
```bash
# Verificar Python 3.7+
python --version

# Crear entorno virtual (recomendado)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
```

### **Instalación de Dependencias**
```bash
pip install flask requests beautifulsoup4 pandas openpyxl
```

### **1. Ejecutar Webscraper (Opcional)**
```bash
cd webscraping
python webscraping.py
```
> ⚠️ **Nota:** Tarda aprox 2 horas correr el scraper completo (incluye rate limiting educado entre requests). Se pueden usar valores de ejemplo (incluidos en comentarios de `webscraping.py`).

### **2. Iniciar Aplicación Web**
```bash
# Desde la raíz del proyecto
python app.py
```

### **3. Acceder al Sistema**
```
🌐 URL: http://127.0.0.1:5000
📱 Compatible con dispositivos móviles
```

---

## Estado del Proyecto

### **Completado:**
- [x] Scraper funcional con manejo de errores
- [x] Optimización: scraping por ID_MOLDE y generación de imágenes sin requests
- [x] Aplicación web responsive completa
- [x] Sistema de carrito con persistencia
- [x] Búsqueda y filtrado en tiempo real
- [x] Integración WhatsApp Business

### **Mejoras futuras:**
- [] Hosting
- [] Conexión a base de datos SQL de inventarios
- [] Compras desde la página
- [] Rediseño de la interfaz de usuario
- [] Mostrar imágenes locales
