
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
    ├── webscraping.py            # Script principal de scraping
    ├── import_excel.py           # Procesador de inventario local
    └── color_ids.py             # Mapeo de colores a IDs de Bricklink
```

---

## Flujo de Datos

### 1. **Extracción de Datos (Webscraping)**
```
datos_inventario.xlsx → webscraping.py → Bricklink API → bricklink_pieces.xlsx
```

- Lee inventario local con columnas: `ID`, `ID_COLOR`, `ID_MOLDE`, `COLOR`
- Mapea colores a IDs numéricos usando `color_ids.py`
- Extrae de Bricklink: nombre, peso, imagen por color
- Genera Excel final con: `Piece_ID`, `ID_COLOR`, `ID_MOLDE`, `Piece_Name`, `Color`, `Image_URL`, `Weight`

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

## Tecnologías Utilizadas

### **Backend**
- **Python 3.13** - Lenguaje principal
- **Flask** - Framework web
- **Pandas** - Procesamiento de datos
- **BeautifulSoup4** - Web scraping
- **Requests** - Cliente HTTP

### **Frontend**
- **HTML5** + **CSS3** - Estructura y estilos
- **JavaScript ES6** - Interactividad
- **Jinja2** - Templates dinámicos

### **Almacenamiento**
- **Excel (XLSX)** - Base de datos principal
- **localStorage** - Persistencia del carrito

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
> ⚠️ **Nota:** Respeta robots.txt de Bricklink. El scraper incluye delays automáticos.

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

### **Completado (100%)**
- [x] Scraper funcional con manejo de errores
- [x] Aplicación web responsive completa
- [x] Sistema de carrito con persistencia
- [x] Búsqueda y filtrado en tiempo real
- [x] Integración WhatsApp Business
- [x] Procesamiento robusto de datos (NaN, validaciones)
- [x] Interfaz de usuario moderna y accesible

### **🎯 Funcionalidades Principales**
1. **Catálogo dinámico** con 19 piezas diferentes
2. **Búsqueda instantánea** por múltiples campos
3. **Carrito persistente** entre sesiones
4. **Pedidos automáticos** vía WhatsApp (+502 5377 1641)
5. **Responsive design** para todos los dispositivos

### **📈 Métricas del Sistema**
- **Tiempo de carga:** < 2 segundos
- **Compatibilidad:** Chrome, Firefox, Safari, Edge
- **Responsive:** Mobile-first design
- **Accesibilidad:** Contraste AAA, navegación por teclado

---

## 📝 Formato de Mensaje WhatsApp

```
Hola, quisiera realizar un pedido:

Detalle:
- ID Esp: 302326, Item: 3023, Nombre: Plate 1 x 2, Color: Black, Cantidad: 2
- Item: 4073, Nombre: Plate, Round 1 x 1, Color: Trans Yellow, Cantidad: 1

Subtotal: Q0.00
```

---

## 🔧 Configuración Técnica

### **Variables de Entorno**
```python
# app.py
DEBUG = True
PORT = 5000
HOST = '127.0.0.1'
```

### **Estructura de Datos**
```python
# Columnas del Excel principal
['Piece_ID', 'ID_COLOR', 'ID_MOLDE', 'Piece_Name', 'Color', 'Image_URL', 'Weight']

# Formato del carrito (localStorage)
{
  "id": "unique-id",
  "pieceId": "4073", 
  "idColor": "302326",
  "idMolde": "4073",
  "name": "Plate 1 x 2",
  "color": "Black",
  "quantity": 2,
  "price": 0.0
}
```

---

## 🎓 Valor Académico

Este proyecto demuestra:

1. **Integración Full-Stack** - Backend Python + Frontend JavaScript
2. **Web Scraping Ético** - Respeto a robots.txt y rate limiting
3. **Diseño Centrado en el Usuario** - UX/UI responsivo y accesible
4. **Gestión de Datos** - ETL con Pandas, validación y limpieza
5. **Arquitectura Escalable** - Separación de responsabilidades
6. **Integración de APIs** - WhatsApp Business API
7. **Persistencia Client-Side** - localStorage y gestión de estado

---

## 👥 Equipo de Desarrollo

- **Valeria Vásquez** - Full-Stack Development, UI/UX Design
- **Pedro Marroquín** - Backend Development, Data Processing  
- **Andrés Juárez** - Frontend Development, JavaScript
- **Julio Girón** - Web Scraping, Data Validation
- **Andrea Nisthal** - Testing, Documentation, QA

---

## 📞 Contacto

**REKUBRICKS** - "Conecta la felicidad"

- 📱 WhatsApp: +502 5377 1641
- 📷 Instagram: [@reku_bricks](https://www.instagram.com/reku_bricks/)
- 📘 Facebook: [brickmarketgt](https://www.facebook.com/brickmarketgt/)

---

*Proyecto desarrollado para SI105. Taller de Ingeniería II - Universidad Francisco Marroquín (2025)*
