
# RekuBricks

A web-based LEGO parts catalog with integrated shopping cart and WhatsApp ordering system for the Guatemala market.

🔗 **[Live Demo](https://rekubricks.onrender.com/)**

## Features

- **Smart Search & Filtering** - Real-time search by piece name, color, or ID with dynamic category filters
- **Persistent Shopping Cart** - Client-side cart with localStorage persistence across sessions
- **WhatsApp Integration** - One-click order generation with automatic message formatting
- **Automated Data Pipeline** - Optimized web scraper that extracts piece data from Bricklink
- **Dynamic Catalog** - Responsive product cards with images, categories, and pricing
- **Mobile-Friendly** - Fully responsive design for all devices

## Tech Stack

- **Backend:** Flask, Pandas
- **Frontend:** Vanilla JavaScript, HTML5, CSS3
- **Data:** Excel-based inventory management
- **Scraping:** BeautifulSoup4, Requests

---

## Quick Start

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

1. Clone the repository
```bash
git clone https://github.com/valevasqc/rekubricks_webapp.git
cd rekubricks_webapp
```

2. Create and activate virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies
```bash
pip install flask pandas openpyxl requests beautifulsoup4
```

4. Run the application
```bash
python app.py
```

5. Open your browser to `http://127.0.0.1:5000`

## Project Structure

```
rekubricks_webapp/
├── app.py                        # Flask application server
├── templates/
│   └── index.html                # Main catalog interface
├── static/
│   ├── style.css                 # Responsive styles
│   ├── script.js                 # Cart and search logic
│   └── logo.png                  # Brand assets
├── data/
│   ├── bricklink_pieces.xlsx     # Processed catalog data
│   └── datos_inventario.xlsx     # Input inventory
└── webscraping/                  # Data extraction pipeline
    ├── webscraping.py            # Main orchestrator
    ├── scrape_moldes.py          # Piece metadata scraper
    ├── generate_images.py        # Image URL generator
    ├── process_categories.py     # Category classifier
    ├── import_excel.py           # Inventory processor
    ├── categories.py             # Category definitions
    └── color_ids.py              # Bricklink color mappings
```

## Data Pipeline

The scraper optimizes data collection by processing unique piece molds (~1,000) and reusing metadata across color variants (~4,000+):

### 1. Data Extraction
```
datos_inventario.xlsx → webscraping.py → Bricklink → bricklink_pieces.xlsx
```

- Loads local inventory with piece IDs and color mappings
- Scrapes piece names and weights from Bricklink per unique mold ID
- Generates image URLs using color-to-ID mapping (no additional HTTP requests)
- Applies automatic categorization based on piece names
- Outputs complete dataset: `Piece_ID`, `ID_COLOR`, `ID_MOLDE`, `Piece_Name`, `Color`, `Image_URL`, `Weight`, `Category`, `Price`

### 2. Web Application
```
bricklink_pieces.xlsx → Flask/Pandas → Dynamic HTML
```

- Loads and validates catalog data with defensive defaults
- Extracts unique categories for filtering
- Renders responsive product cards with Jinja2 templates

### 3. User Interaction
```
Browse → Search/Filter → Add to Cart → WhatsApp Order
```

- Client-side search matches name, color, or piece ID
- Dynamic category filtering
- Persistent cart stored in localStorage
- Automated WhatsApp message generation with order details

## Running the Web Scraper

The scraper is optional if you already have processed data. To regenerate the catalog:

```bash
cd webscraping
python webscraping.py
```

> **Note:** Full scrape takes approximately 2 hours due to polite rate limiting. The scraper respects Bricklink's servers with randomized delays between requests.

## Configuration

### WhatsApp Integration
Edit `static/script.js` to configure the target phone number:
```javascript
const phoneNumber = '+50253771641'; // Format: country code + number
```

### Color Mappings
Add or modify Bricklink color IDs in `webscraping/color_ids.py`:
```python
color_ids = {
    "RED": 5,
    "BLUE": 7,
    // Add more mappings
}
```

### Categories
Customize piece categories in `webscraping/categories.py` to match your inventory classification needs.

## Roadmap

- [ ] Database integration (SQL) for inventory management
- [ ] Admin panel for catalog updates
- [ ] Direct payment processing
- [ ] User authentication and order history
- [ ] Enhanced UI/UX with modern framework


## License

This project is open source and available under the MIT License.

## Contact

For questions or support, please open an issue on GitHub.


