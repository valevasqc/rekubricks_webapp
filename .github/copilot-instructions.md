<!-- Project-specific AI agent instructions for RekuBricks -->
# RekuBricks — Full-stack LEGO Catalog Web Application

Production-ready e-commerce catalog with webscraping pipeline, Flask backend, and vanilla JavaScript frontend. Built for Guatemala market (WhatsApp integration, Quetzal pricing).

## Architecture Overview

**3-tier data flow:**
```
datos_inventario.xlsx → [webscraping] → bricklink_pieces.xlsx → [Flask/Pandas] → Dynamic HTML catalog
```

**Key components:**
- `webscraping/` — Bricklink scraper (BeautifulSoup + requests)
- `app.py` — Flask backend with aggressive data cleaning
- `templates/index.html` + `static/` — Cart system with localStorage persistence
- `data/` — Excel files (input inventory + scraped output)

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
```

### 3. NaN Handling Philosophy
`app.py` uses **defensive defaults** everywhere:
```python
df['Price'] = pd.to_numeric(df['Price'], errors='coerce').fillna(0.0)
df['Category'] = df['Category'].fillna('Sin categoría')
df = df[df['Image_URL'] != 'N/A']  # Drop unusable rows
```
**Always add new columns with `.fillna()` + validation filters** — frontend expects clean data.

### 4. localStorage Cart State
Cart persists across sessions via `localStorage.rekubricksCart`. Uses **event delegation** for dynamic button updates:
```javascript
// Must target .add-to-cart-btn specifically, not parent divs
document.querySelector(`.add-to-cart-btn[data-id="${id}"]`)
```
When adding cart features, update `updateCartDisplay()`, `updateCardButton()`, and `saveCart()` in sync.

### 5. Brand Color System
**Strict palette** (REKUBRICKS brand):
- Primary red: `#e10800` (prices, accents)
- Yellow: `#ffe403` (highlights)
- Blue: `#003465` (backgrounds, gradients)

Use these values literally — no hex variations. See `static/style.css` for gradient formulas.

## Scraping Constraints

**Rate limiting is mandatory:**
```python
time.sleep(1.5 + random.random())  # Between each request
headers = {"User-Agent": "Mozilla/5.0"}  # Always set
```

**Image URL logic:**
1. If `color_ids.get(COLOR)` exists: use `https://img.bricklink.com/P/{colorID}/{pid}.jpg`
2. Else: scrape `td.pciMainImageHolder img` from general page

**Selectors (in order of preference):**
- Title: `h1#item-name-title` (current) → fallback to table selectors
- Weight: `span#item-weight-info`
- Image: Constructed URL > scraped `img src`

Test scraper with 3-5 pieces first: `pieces = [{"ID_MOLDE": "3023", "COLOR": "RED", "ID_COLOR": ""}]` in `webscraping.py`.

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

**Backend:** `app.py` (Flask routes), `webscraping/webscraping.py` (scraper), `webscraping/import_excel.py` (Excel parser)  
**Frontend:** `templates/index.html` (Jinja2), `static/script.js` (cart logic), `static/style.css` (responsive design)  
**Data:** `data/bricklink_pieces.xlsx` (generated output), `data/datos_inventario.xlsx` (manual input)  
**Config:** `webscraping/color_ids.py` (color mapping — 200+ entries)

## Gotchas

- CSS has duplicate rule warnings (line 307) — ignore unless breaking
- Cart counter shows **unique items** (not total quantity): `cart.length` not `.reduce()`
- Excel `Piece_ID` may be either `ID_COLOR` or `ID_MOLDE` depending on scraper logic (line 68-69 in `webscraping.py`)
- Social icons in header use `target="_blank"` — keep for UX
- No authentication/database — stateless Flask app with Excel as "DB"
