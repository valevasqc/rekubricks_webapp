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
