# Webscraper V2 - Optimized Architecture

## Overview

The new webscraper reduces scraping time by ~75% and minimizes ban risk by scraping only unique ID_MOLDEs (~1000) instead of all color variants (~4000+).

## Architecture

### Modular Components

1. **scrape_moldes.py** - Scrapes unique ID_MOLDEs from Bricklink
2. **process_categories.py** - Extracts categories from piece names
3. **generate_images.py** - Generates image URLs without HTTP requests
4. **import_excel.py** - Loads input data (id_molde.xlsx, datos_inventario.xlsx)
5. **webscraping_v2.py** - Main orchestrator pipeline
6. **test_scraper.py** - Test suite for validation

### Data Flow

```
id_molde.xlsx (~1000 unique IDs)
    ↓
[Scrape ID_MOLDEs] → name, weight
    ↓
[Extract Categories] → category from name
    ↓
datos_inventario.xlsx (~4000+ pieces)
    ↓
[Merge Data] → reuse name/weight/category for all color variants
    ↓
[Generate Images] → create URLs using color_ids mapping
    ↓
bricklink_pieces.xlsx (complete dataset)
```

## Key Improvements

### Efficiency Gains

- **~75% fewer HTTP requests**: Scrape 1000 IDs instead of 4000+ pieces
- **No image scraping**: URLs generated from pattern (no requests needed)
- **Batch categorization**: Intelligent category extraction from names
- **Rate limit friendly**: Configurable delays, polite user-agent

### Risk Reduction

- **Minimal server load**: Far fewer requests to Bricklink
- **Smart retries**: Handles failures gracefully
- **Fallback logic**: Works even if id_molde.xlsx is missing

## Usage

### 1. Run Tests (Recommended First)

```bash
cd webscraping
python test_scraper.py
```

Tests 4 components with small samples:
- Single molde scrape
- Category extraction
- Image URL generation  
- Small batch scrape (3 pieces)

### 2. Run Full Scraper

```bash
cd webscraping
python webscraping_v2.py
```

Expected time: ~30-40 minutes (vs ~2+ hours with old scraper)

### 3. Legacy Scraper (Still Available)

```bash
cd webscraping
python webscraping.py  # Old version for comparison
```

## Input Files

### Required

**data/datos_inventario.xlsx** - Full inventory with all color variants
- Columns: `ID` (or ID_COLOR), `ID MOLDE`, `COLOR`
- ~4000+ rows with color variants

### Optional

**data/id_molde.xlsx** - Unique mold IDs only
- Column: `ID_MOLDE` (or similar)
- ~1000 unique rows
- If missing: auto-extracts from datos_inventario.xlsx

### Configuration

**webscraping/categories.py** - Predefined category list
```python
categories = ["BRICK", "PLATE", "TILE", ...]
```

**webscraping/color_ids.py** - Color name to ID mapping
```python
color_ids = {
    "RED": 5,
    "BLUE": 7,
    ...
}
```

## Output Format

**data/bricklink_pieces.xlsx** - Compatible with existing website

Columns:
- `Piece_ID` - Frontend identifier (ID_COLOR or ID_MOLDE)
- `ID_COLOR` - Specific color variant ID
- `ID_MOLDE` - Base mold ID
- `Piece_Name` - Full piece name
- `Color` - Color name (title case)
- `Image_URL` - Generated image URL
- `Weight` - Piece weight
- `Category` - Extracted category
- `Price` - Default 0.0 (set manually)

## Category Extraction Logic

Categories are extracted from piece names using this strategy:

1. **Multi-word categories first**: "CURVED SLOPE", "MINIFIGURE"
2. **First word match**: "BRICK 2 x 4" → "BRICK"
3. **Partial match**: Search anywhere in name
4. **Fallback**: "MISCELLANEOUS" if no match

Example:
```python
"Plate 2 x 4" → "PLATE"
"Brick 1 x 2" → "BRICK"
"Minifigure Head" → "MINIFIGURE"
"Unknown Item" → "MISCELLANEOUS"
```

## Image URL Generation

Images are generated using Bricklink's URL pattern without HTTP requests:

**Pattern**: `https://img.bricklink.com/P/{color_id}/{id_molde}.jpg`

Example:
```python
ID_MOLDE: "3023"
COLOR: "RED" → color_id: 5
URL: https://img.bricklink.com/P/5/3023.jpg
```

If color not in `color_ids` mapping, URL is set to "N/A".

## Error Handling

- **Failed scrapes**: Sets name/weight to "N/A", continues
- **Missing moldes**: Uses "N/A" values for missing data
- **Network errors**: Logs error, continues with next item
- **Missing files**: Tries fallback extraction from inventory

## Configuration Options

### Rate Limiting

In `webscraping_v2.py`, adjust delay range:

```python
molde_data = scrape_multiple_moldes(
    unique_moldes, 
    delay_range=(1.5, 2.5)  # Min, Max seconds between requests
)
```

Recommended: 1.5-2.5 seconds to be respectful to Bricklink

### Test Sample Size

In `test_scraper.py`, adjust test pieces:

```python
test_moldes = ["3023", "3024", "3001"]  # Add more IDs to test
```

## Troubleshooting

### "No ID_MOLDEs loaded"
- Check that `id_molde.xlsx` exists in `data/` folder
- Verify column name is "ID_MOLDE" or similar
- Script will auto-fallback to extracting from inventory

### "Many failed scrapes"
- Increase `delay_range` to be more conservative
- Check internet connection
- Verify Bricklink site is accessible

### "Image URLs showing N/A"
- Color not in `color_ids.py` mapping
- Add missing colors to `webscraping/color_ids.py`
- Use uppercase color names: `"TRANS YELLOW": 224`

### "Categories all MISCELLANEOUS"
- Check piece names are being scraped correctly
- Verify categories.py has correct list
- May need to add custom category logic

## Performance Comparison

| Metric | Old Scraper | New Scraper V2 | Improvement |
|--------|-------------|----------------|-------------|
| Requests | ~4000+ | ~1000 | 75% reduction |
| Time | ~2+ hours | ~30-40 min | 70% faster |
| Ban risk | High | Low | Much safer |
| Maintainability | Low | High | Modular |

## Future Enhancements

Potential improvements:
- [ ] Parallel scraping with thread pool (use cautiously)
- [ ] Caching layer for scraped moldes
- [ ] Auto-price estimation from Bricklink
- [ ] Image validation (check if URLs return 200)
- [ ] Progress bar with ETA
- [ ] Resume from checkpoint on failure

## Files Reference

```
webscraping/
├── webscraping_v2.py          # Main orchestrator (NEW)
├── scrape_moldes.py            # Scraping module (NEW)
├── process_categories.py       # Category extraction (NEW)
├── generate_images.py          # Image URL generator (NEW)
├── import_excel.py             # Updated input loader
├── test_scraper.py             # Test suite (NEW)
├── categories.py               # Category definitions
├── color_ids.py                # Color ID mapping
└── webscraping.py              # Legacy scraper (preserved)
```

## Questions or Issues?

Check test output first:
```bash
python test_scraper.py
```

Review module docstrings:
```python
python -c "import scrape_moldes; help(scrape_moldes)"
```
