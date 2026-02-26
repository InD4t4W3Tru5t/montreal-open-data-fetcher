# 🗺️ Montréal Open Data Explorer

A Streamlit app to browse, preview, and download datasets from the **[Ville de Montréal Open Data portal](https://donnees.montreal.ca)**.

---

## Features

- **Dataset Browser** — browse the full catalog, search by keyword, and explore dataset details
- **Fetch by Resource ID** — directly fetch any dataset by its CKAN resource UUID
- **In-app preview** — paginated data table with row filtering and column info
- **CSV download** — export any tabular dataset as a UTF-8 CSV
- **Large file support** — ZIP, SHP, and other binary files open via a direct external link (no server buffering)
- **Row limit slider** — control how many rows to fetch with a safe slider that guards against edge cases
- **Bilingual UI** — toggle between English and Français at any time

---

## Pages

### 📚 Dataset Browser
1. Search the catalog by keyword
2. Select a dataset from the dropdown — **nothing loads until you make a selection**
3. Browse the available resources (CSV, JSON, ZIP, SHP, etc.)
4. Select a resource — **nothing loads until you make a selection**
5. For tabular resources: choose a row limit, then click **Fetch this resource**
6. For binary/large files (ZIP, SHP, RAR…): a direct download link is shown — no in-app buffering

### 🔍 Fetch by Resource ID
1. Paste any resource UUID from [donnees.montreal.ca](https://donnees.montreal.ca)
2. Optionally limit the number of rows
3. Click **Fetch Data**

---

## Installation

```bash
pip install streamlit requests pandas
streamlit run montreal_app.py
```

---

## Configuration

| Constant | Default | Description |
|---|---|---|
| `PAGE_SIZE` | `1000` | Rows fetched per API call |
| `MAX_RETRIES` | `5` | Retry attempts with exponential backoff |
| `SLIDER_THRESHOLD` | `101` | Minimum rows required to display the limit slider |
| `LINK_ONLY_FORMATS` | `ZIP, SHP, RAR, 7Z, TAR, GZ` | Formats served as a direct external link |
| `CSV_FORMATS` | `CSV, TSV, XLS, XLSX` | Formats fetched via the DataStore API |

---

## Data Source

[Données ouvertes – Ville de Montréal](https://donnees.montreal.ca)  
API base URL: `https://donnees.montreal.ca/api/3/action/`

---

## Changelog

### Latest
- Empty selectboxes by default — no auto-fetch on page load
- ZIP / SHP / binary files now use a direct external link instead of server-side buffering (prevents crash)
- `safe_slider()` guards against `min == max` edge case on small datasets
