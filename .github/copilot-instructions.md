<!-- Project-specific Copilot instructions for AI coding agents -->
# Bricklink Webscraper — AI agent guide

Short, actionable notes to help an AI agent be productive editing and extending this repository.

- Entry points
  - `webscraping/webscraping.py` — main scraper. Builds URLs per piece, requests Bricklink pages, parses name/image/weight and writes `data/bricklink_pieces.xlsx`.
  - `webscraping/import_excel.py` — reads `data/datos_inventario.xlsx` and returns a list of piece dicts (keys are uppercased: `ID_COLOR`, `ID_MOLDE`, `COLOR`).
  - `webscraping/color_ids.py` — mapping from UPPERCASED color names to Bricklink `colorID` integers used to construct color-specific image URLs.
  - `app.py` + `templates/index.html` — a minimal Flask front-end that reads `data/bricklink_pieces.xlsx` and renders pieces (used for demo UI).

- Big picture / data flow
  - Input: optional `data/datos_inventario.xlsx` or an inline `pieces` list in `webscraping/webscraping.py`.
  - Lookup: map piece `COLOR` -> `colorID` using `webscraping/color_ids.py` (keys are uppercase; trim whitespace.)
  - Scrape: request the general Bricklink page `catalogitem.page?P={pid}` for name and weight. If `colorID` exists, construct image URL `https://img.bricklink.com/P/{colorID}/{pid}.jpg` else extract image from the general page.
  - Output: `data/bricklink_pieces.xlsx` with columns `Piece_ID, Piece_Name, Color, Image_URL, Weight`.

- Project-specific conventions and gotchas
  - Column names from Excel are normalized to UPPERCASE inside `import_excel.py`. Expect keys `ID`, `ID MOLDE`, and `COLOR` when editing Excel parsing.
  - `color_ids.py` may contain duplicate/overridden keys; use the dict as-is unless asked to dedupe.
  - Requests use a simple User-Agent and synchronous sleeps: keep `headers = {"User-Agent": "Mozilla/5.0"}` and `time.sleep(1.5 + random.random())` to avoid excessive load on Bricklink.
  - Output paths are relative: scraper writes `../data/bricklink_pieces.xlsx` when run from `webscraping/` directory — be careful with working directory when running scripts.

- Selectors & parsing heuristics
  - Piece title: prefer `h1#item-name-title`, fallback to older table-based selectors used in the repo.
  - Weight: check `span#item-weight-info` on the general page.
  - Image: if `colorID` present prefer constructed `img.bricklink.com` URL; otherwise use `td.pciMainImageHolder img` or other fallback selectors.

- Developer workflows (discoverable and tested here)
  - Install deps manually: `python -m pip install requests beautifulsoup4 pandas openpyxl` (no requirements.txt in repo).
  - Run scraper (small sample first): edit `webscraping/webscraping.py` to use a short `pieces` list (3–5 items) or call `import_excel()` and run `python webscraping/webscraping.py` from the project root.
  - Run the demo web UI: `python app.py` (Flask app reads `data/bricklink_pieces.xlsx`).

- When changing scraping logic
  - Preserve polite delays and User-Agent. Test on a very small sample to avoid accidental heavy traffic to Bricklink.
  - Add fallback selectors; Bricklink pages differ between endpoints.

- Where to look for related code
  - `webscraping/webscraping.py` — scraping logic and current selectors
  - `webscraping/import_excel.py` — Excel input normalization
  - `webscraping/color_ids.py` — color mapping (update by adding UPPERCASE keys)
  - `app.py`, `templates/index.html`, `static/` — small Flask demo UI and CSS

- Examples (copyable edits)
  - Use Excel input: replace sample `pieces = [...]` in `webscraping/webscraping.py` with `pieces = import_excel()` and uncomment the `from import_excel import import_excel` import.
  - Add color: to support a new color name add UPPERCASED key to `webscraping/color_ids.py`, e.g. `"TRANS PINK": 999`.

If anything here is unclear or you want stricter linting/tests/CI, tell me what to add and I will update this file.
<!-- Project-specific Copilot instructions for AI coding agents -->
# Project: Bricklink Webscraper (Python)

These short instructions help an AI coding agent be productive in this small Python project that scrapes Bricklink and writes results to Excel.

- Entry points
  - `webscraping.py` — main scraper script. Reads a `pieces` list (or uses `import_excel.import_excel()`), requests Bricklink pages, parses name, image URL and weight, and writes `bricklink_pieces.xlsx`.
  - `import_excel.py` — helper that reads `datos_inventario.xlsx` and returns a list of piece dicts with keys `ID_COLOR`, `ID_MOLDE`, `COLOR`.
  - `color_ids.py` — local mapping of uppercased color names to Bricklink color IDs used to build color-specific requests.

- Big picture and data flow
  - Input: `datos_inventario.xlsx` (optional). `import_excel()` produces a list of pieces (dicts).
  - For each piece: determine `colorID` via `color_ids` mapping. Build either a color-specific URL (`catalogItemIn.asp?P={pid}&colorID={color_id}`) or the generic item page (`catalogitem.page?P={pid}`).
  - Fetch HTML with `requests`, parse with `BeautifulSoup` to extract title, image src and weight (weight sometimes only on generic page). Save results to `bricklink_pieces.xlsx` via `pandas`.

- Key patterns to preserve
  - The code uses synchronous requests + polite delays: keep the `time.sleep(1.5 + random.random())` pause between requests.
  - HTML selectors vary by page variant. `webscraping.py` first tries `h1#item-name-title`, then `table td font b` for the title. Image selectors depend on whether the request used `catalogItemIn.asp` or `catalogitem.page`.
  - `color_ids.py` contains duplicate and overridden keys; prefer reading and using the current dict as-is (do not dedupe automatically unless asked).

- Conventions and small gotchas
  - Column names in `datos_inventario.xlsx` are normalized to UPPERCASE in `import_excel.py`. Use `ID`, `ID MOLDE`, and `COLOR` column names or update the renames accordingly.
  - The project expects to run with Python and the following libraries: `requests`, `beautifulsoup4`, and `pandas`. There is no requirements file in the repo — create one if adding dependencies.
  - Filenames and outputs are relative to the project root. `bricklink_pieces.xlsx` will be created/overwritten in the same folder as `webscraping.py`.

- Examples to reference when making edits
  - To use Excel input: replace the sample `pieces = [...]` in `webscraping.py` with `pieces = import_excel()` and uncomment the `from import_excel import import_excel` import.
  - To add a new color: add an UPPERCASED key to `color_ids.py`, e.g. `"TRANS PINK": 999`.

- When changing scraping logic
  - Always test on a small sample (3–5 pieces) to avoid accidental heavy traffic to Bricklink.
  - Keep the `headers = {"User-Agent": "Mozilla/5.0"}` and respect robots and rate limits. Any increase in concurrency requires explicit review.
  - When adding new selectors, include fallback selectors and preserve the existing heuristics (many Bricklink pages differ between endpoints).

- Developer workflows (quick commands)
  - Install dependencies (if using venv): `python -m pip install requests beautifulsoup4 pandas openpyxl`
  - Run the scraper interactively: `python webscraping.py`

- Where to look for follow-ups
  - If weights are missing, inspect `general_url = f"https://www.bricklink.com/v2/catalog/catalogitem.page?P={pid}"` parsing in `webscraping.py`.
  - If color lookup fails, check capitalization and whitespace of names in `pieces` vs `color_ids` keys.

If anything here is unclear or you'd like the agent to follow stricter style, tests, or add a requirements file, tell me which direction to take and I'll update this file.
