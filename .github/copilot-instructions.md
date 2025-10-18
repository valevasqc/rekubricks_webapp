<!-- Project-specific AI agent instructions for RekuBricks -->
# RekuBricks — Full-stack LEGO Catalog Web Application

Production-ready e-commerce catalog with optimized webscraping pipeline, Flask backend, and vanilla JavaScript frontend. Built for Guatemala market (WhatsApp integration, Quetzal pricing).

## Architecture Overview

**3-tier data flow:**
```
datos_inventario.xlsx → [modular webscraper] → bricklink_pieces.xlsx → [Flask/Pandas] → Dynamic HTML catalog
```

**Key components:**
- `webscraping/` — Modular Bricklink scraper (BeautifulSoup + requests) with 5 specialized modules
- `app.py` — Flask backend with type hints and defensive data cleaning
- `templates/index.html` + `static/` — Cart system with localStorage persistence
- `data/` — Excel files (input inventory + scraped output)

**Webscraper V2 Architecture (modular):**
```
webscraping.py (orchestrator)
├── import_excel.py       → Load inventory + unique moldes
├── scrape_moldes.py      → Scrape ~1000 ID_MOLDEs (name, weight)
├── process_categories.py → Classify pieces using categories.py
└── generate_images.py    → Build URLs via color_ids (no HTTP)
```

## Critical Patterns

### 1. Data ID Schema (affects all layers)
Frontend uses **composite IDs** for cart uniqueness:
```javascript
// Button data-id format: "pieceId-color-normalized"
data-id="{{ piece['Piece_ID'] + '-' + (piece['Color']|replace(' ','-')|lower) }}"
```
But also stores separate `data-id-color` and `data-id-molde` for WhatsApp order messages. **Never break this multi-ID pattern** — cart state depends on it.

### 2. Excel Column Normalization
`import_excel.py` uppercases ALL columns: `ID` → `ID_COLOR`, `ID MOLDE` → `ID_MOLDE`. When adding columns to Excel processing, always:
```python
df.columns = [col.strip().upper() for col in df.columns]
df = df.rename(columns={"NEW COL": "NEW_COL"})
# CRITICAL: Convert ID columns to strings and strip 'nan'
df["ID_MOLDE"] = df["ID_MOLDE"].astype(str).str.strip().replace('nan', '')
```

### 3. Type Hints are Standard
All Python modules now use type hints (`typing.List`, `typing.Dict`, etc.). When adding functions, follow this pattern:
```python
def my_function(pieces: List[Dict[str, Any]]) -> List[Dict]:
    """Concise one-line summary.
    
    Longer description if needed; use Returns/Args sections.
    """
    return processed_pieces
```

### 4. NaN Handling Philosophy
`app.py` uses **defensive defaults** everywhere:
```python
df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0.0)
df['Category'] = df['Category'].fillna('Sin categoría')
df = df[df['Image_URL'] != 'N/A']  # Drop unusable rows
```
**Always add new columns with `.fillna()` + validation filters** — frontend expects clean data.

### 5. localStorage Cart State
Cart persists across sessions via `localStorage.rekubricksCart`. Uses **event delegation** for dynamic button updates:
```javascript
// Must target .add-to-cart-btn specifically, not parent divs
document.querySelector(`.add-to-cart-btn[data-id="${id}"]`)
```
When adding cart features, update `updateCartDisplay()`, `updateCardButton()`, and `saveCart()` in sync.

### 6. Brand Color System
**Strict palette** (REKUBRICKS brand):
- Primary red: `#e10800` (minor accents)
- Yellow: `#ffe403` (highlights)
- Blue: `#003465` (main accents, backgrounds, gradients)

Minor variations are allowed to maintain visual cohesion. Neutral colors (grays, whites) can be used freely. See `static/style.css` for gradient formulas.

## Scraping Constraints

**Rate limiting is mandatory:**
```python
time.sleep(1.5 + random.random())  # Between each request
headers = {"User-Agent": "Mozilla/5.0"}  # Always set
```

**Image URL logic (NO HTTP requests for images):**
1. `generate_images.py` prefers numeric `ID_COLOR` if provided: `https://img.bricklink.com/P/{ID_COLOR}/{id_molde}.jpg`
2. Else maps color name via `color_ids.get(COLOR.upper())` to construct URL
3. Returns "N/A" if color unmapped (no scraping fallback in V2)

**Scraping selectors (only for ID_MOLDE metadata):**
- Title: `h1#item-name-title`
- Weight: `span#item-weight-info`

**Key optimization:** Scrape ~1000 unique ID_MOLDEs once, reuse data across ~4000+ color variants. Image URLs generated without requests.

## Developer Workflows

**Setup (from project root):**
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install flask pandas openpyxl requests beautifulsoup4
```

**Run scraper (slow — ~2hrs full inventory):**
```bash
cd webscraping
python webscraping.py  # Writes to ../data/bricklink_pieces.xlsx
```

**Run web app:**
```bash
python app.py  # → http://127.0.0.1:5000
```

**No build step, no package.json** — pure Python backend + vanilla JS frontend.

## Common Edits

**Add new Excel column:**
1. Update `load_pieces()` in `app.py`:
   ```python
   if "NewCol" not in df.columns:
       df["NewCol"] = "default"
   df['NewCol'] = df['NewCol'].fillna('default')
   ```
2. Update Jinja template: `{{ piece['NewCol']|e }}`

**Add search filter:**
Modify `applyFilters()` in `static/script.js`:
```javascript
const matchesNewField = card.getAttribute('data-newfield').includes(term);
```

**Add Bricklink color:**
Add to `webscraping/color_ids.py`: `"TRANS PINK": 224` (keys are UPPERCASE, no spaces in keys).

## WhatsApp Integration Details

Phone: `+50253771641` (hardcoded in `script.js`)

**Message format** (auto-generated):
```
Hola, quisiera realizar un pedido:

Detalle:
- ID Esp: 123, Item: 3023, Color: Red, Cantidad: 2
- Item: 4073, Color: Black, Cantidad: 1

Subtotal: Q45.50
```

Clean `.0` from numeric IDs: `String(id).replace('.0', '')` before message generation.

## Search Behavior (Recent Change)

Search **resets category filter to 'all'** automatically:
```javascript
function searchProducts(term) {
    currentCategory = 'all';
    document.getElementById('categoryFilter').value = 'all';
    applyFilters();
}
```
Don't revert this — it's intentional UX improvement.

## File References

**Backend:** `app.py` (Flask routes + type hints), `webscraping/webscraping.py` (orchestrator)  
**Scraper modules:** `scrape_moldes.py`, `generate_images.py`, `process_categories.py`, `import_excel.py`  
**Frontend:** `templates/index.html` (Jinja2), `static/script.js` (cart + search), `static/style.css`  
**Data:** `data/bricklink_pieces.xlsx` (output), `data/datos_inventario.xlsx` (input), `data/id_molde.xlsx` (unique molds)  
**Config:** `webscraping/color_ids.py` (200+ color→ID mappings), `webscraping/categories.py` (21 categories)

## Gotchas & TODOs

- Cart counter shows **unique items** (not total quantity): `cart.length` not `.reduce()`
- Excel `Piece_ID` may be either `ID_COLOR` or `ID_MOLDE` depending on scraper logic
- Social icons in header use `target="_blank"` — keep for UX
- No authentication/database — stateless Flask app with Excel as "DB"
- **Known TODOs in code:**
  - `app.py`: Connect to SQL (line 14), flesh out UI (line 9), consider using ID_MOLDE+COLOR composite key (line 48)
  - `script.js`: Allow local images via GCP (line 122), add quantity validation (line 291)
  - `color_ids.py`: Auto-populate from website (line 86)
