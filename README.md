# 🗺️ Montréal Open Data Explorer

A Streamlit app to browse, preview, and download datasets from the [Ville de Montréal Open Data portal](https://donnees.montreal.ca).

## Features

- **Dataset Browser** — browse the full catalog, search by keyword, select a dataset and explore its resources
- **Fetch by Resource ID** — enter any Resource ID directly to preview or download the data
- Tabular resources (CSV, TSV, XLS, XLSX) are fetched via the CKAN DataStore API with full preview
- Non-tabular resources (GeoJSON, JSON, XML, SHP, KML, PDF…) are downloaded directly in their original format
- Row count displayed before fetching so you know the dataset size upfront
- Adjustable row limit slider (based on actual total) with option to fetch everything
- Interactive data preview with keyword filtering
- Column metadata (null counts, data types, sample values)
- One-click CSV download (UTF-8 BOM for Excel compatibility)
- Paginated fetch with retry logic and rate-limit handling
- Full French / English language toggle

## Stack

- [Streamlit](https://streamlit.io) — web app framework
- [Pandas](https://pandas.pydata.org) — data manipulation
- [Requests](https://docs.python-requests.org) — HTTP calls to the CKAN API
- [Montréal Open Data (CKAN)](https://donnees.montreal.ca) — data source

## Getting Started

```bash
git clone https://github.com/<your-username>/montreal-opendata-explorer.git
cd montreal-opendata-explorer

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```

Open your browser at **http://localhost:8501**.

## Deploy on Streamlit Community Cloud

1. Push this repo to GitHub (public)
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app**, select your repo, set main file to `app.py`
4. Click **Deploy**

## How to Find a Resource ID

1. Use the **Dataset Browser** tab directly in the app
2. Or browse [donnees.montreal.ca](https://donnees.montreal.ca), open a dataset, and copy the UUID from the URL: `.../resource/<resource-id>`

### Example

| Dataset | Resource ID |
|---|---|
| Permis d'occupation du domaine public | `cc41b532-f12d-40fb-9f55-eb58c9a2b12b` |

## Project Structure

```
montreal-opendata-explorer/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## License

MIT
