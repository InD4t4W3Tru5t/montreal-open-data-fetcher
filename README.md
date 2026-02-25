# 🗺️ Montréal Open Data Explorer

A **Streamlit** web application that lets you retrieve any dataset from the
[Ville de Montréal Open Data portal](https://donnees.montreal.ca) using its
**Resource ID**, preview it interactively, and download it as a CSV file.

## ✨ Features

- 🔍 **Fetch any dataset** by Resource ID via the CKAN DataStore API
- 📊 **Interactive data preview** with in-app filtering
- 📋 **Column metadata** (nulls, dtypes, sample values)
- ⬇️ **One-click CSV download** (UTF-8 BOM for Excel compatibility)
- ⚡ **Paginated fetch** with exponential back-off and rate-limit handling
- 🎚️ **Row limit slider** for fast previews of large datasets

---

## 🚀 Quickstart (local)

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/montreal-opendata-explorer.git
cd montreal-opendata-explorer

# 2. Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

Open your browser at **http://localhost:8501**.

---

## ☁️ Deploy on Streamlit Community Cloud (free)

1. Push this repository to **GitHub** (public repo).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app** → select your repo → set **Main file path** to `app.py`.
4. Click **Deploy** – that's it! Your app gets a public URL instantly.

---

## 📂 Project Structure

```
montreal-opendata-explorer/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## 🔑 How to Find a Resource ID

1. Browse [donnees.montreal.ca](https://donnees.montreal.ca)
2. Open any dataset and click on a resource/file tab
3. Copy the UUID from the page URL:  
   `https://donnees.montreal.ca/dataset/.../resource/**<resource-id>**`

### Example IDs

| Dataset | Resource ID |
|---|---|
| Permis d'occupation du domaine public (Travaux MTL) | `cc41b532-f12d-40fb-9f55-eb58c9a2b12b` |

---

## 🛠️ Tech Stack

| Tool | Role |
|---|---|
| [Streamlit](https://streamlit.io) | Web app framework |
| [Pandas](https://pandas.pydata.org) | Data manipulation |
| [Requests](https://docs.python-requests.org) | HTTP calls to CKAN API |
| [Montréal Open Data (CKAN)](https://donnees.montreal.ca) | Data source |

---

## 📄 License

MIT — feel free to fork and adapt.
