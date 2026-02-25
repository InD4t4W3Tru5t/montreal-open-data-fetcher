# 🗺️ Montréal Open Data Explorer

A Streamlit app to explore and download datasets from the [Ville de Montréal Open Data portal](https://donnees.montreal.ca) using a Resource ID.

## Features

- Fetch any dataset by Resource ID via the CKAN DataStore API
- Interactive data preview with keyword filtering
- Column metadata (null counts, data types, sample values)
- One-click CSV download (UTF-8 BOM for Excel compatibility)
- Paginated fetch with retry logic and rate-limit handling
- Row limit slider for fast previews on large datasets
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
