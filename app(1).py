import streamlit as st
import requests
import pandas as pd
import time
import io

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Montréal Open Data Explorer",
    page_icon="🗺️",
    layout="wide",
)

# ── Translations ──────────────────────────────────────────────────────────────
TRANSLATIONS = {
    "en": {
        "page_title": "🗺️ Montréal Open Data Explorer",
        "page_subtitle": (
            "Retrieve any dataset from the **[Ville de Montréal Open Data portal](https://donnees.montreal.ca)** "
            "by entering its **Resource ID**. Preview the data directly in the app or download it as a CSV file."
        ),
        "sidebar_header": "⚙️ Configuration",
        "resource_id_label": "Resource ID",
        "resource_id_placeholder": "e.g. cc41b532-f12d-40fb-9f55-eb58c9a2b12b",
        "resource_id_help": "Found in the URL of any dataset on donnees.montreal.ca",
        "limit_rows_label": "Limit rows (faster preview)",
        "max_rows_label": "Max rows to fetch",
        "fetch_btn": "🔍 Fetch Data",
        "sidebar_caption": (
            "Data source: [Données ouvertes – Ville de Montréal](https://donnees.montreal.ca)  \n"
            "Built with Streamlit · [Source code on GitHub](https://github.com)"
        ),
        "dataset_header": "📂 Dataset",
        "resource_id_caption": "Resource ID",
        "connecting_spinner": "Connecting to the Montréal Open Data API…",
        "error_msg": "❌ Failed to retrieve data. Please verify the Resource ID and try again.",
        "no_records": "⚠️ No records found for this Resource ID.",
        "rows_fetched": "Rows fetched",
        "columns": "Columns",
        "est_memory": "Est. memory",
        "preview_header": "🔎 Data Preview",
        "filter_label": "Filter rows (searches all columns)",
        "filter_caption": "Showing {shown} matching rows out of {total}",
        "col_info_expander": "📋 Column information",
        "col_name": "Column",
        "col_nonnull": "Non-null",
        "col_null": "Null",
        "col_dtype": "Dtype",
        "col_sample": "Sample",
        "download_header": "⬇️ Download",
        "download_btn": "📥 Download as CSV",
        "download_caption": "File will be saved as `{filename}`",
        "idle_info": "👈 Enter a **Resource ID** in the sidebar and click **Fetch Data** to get started.",
        "how_to_header": "💡 How to find a Resource ID",
        "how_to_body": (
            "1. Go to **[donnees.montreal.ca](https://donnees.montreal.ca)**\n"
            "2. Search for any dataset (e.g. *Travaux*, *Permis*, *Accidents*)\n"
            "3. Click on the dataset, then select a **resource/file**\n"
            "4. The Resource ID appears in the page URL:\n"
            "   `https://donnees.montreal.ca/dataset/.../resource/<resource-id>`\n"
            "5. Paste it into the sidebar field above."
        ),
        "example_ids_header": "**Example Resource IDs to try:**",
        "example_table": (
            "| Dataset | Resource ID |\n"
            "|---|---|\n"
            "| Permis d'occupation du domaine public (Travaux) | `cc41b532-f12d-40fb-9f55-eb58c9a2b12b` |"
        ),
        "progress_text": "Fetched {fetched} / {total} records…",
        "warn_no_resource": "Please enter a Resource ID.",
        "language_toggle": "🇫🇷 Français",
    },
    "fr": {
        "page_title": "🗺️ Explorateur – Données ouvertes de Montréal",
        "page_subtitle": (
            "Récupérez n'importe quel jeu de données du **[portail de données ouvertes de la Ville de Montréal](https://donnees.montreal.ca)** "
            "en entrant son **identifiant de ressource**. Prévisualisez les données dans l'application ou téléchargez-les en CSV."
        ),
        "sidebar_header": "⚙️ Configuration",
        "resource_id_label": "Identifiant de ressource",
        "resource_id_placeholder": "ex. cc41b532-f12d-40fb-9f55-eb58c9a2b12b",
        "resource_id_help": "Visible dans l'URL de n'importe quel jeu de données sur donnees.montreal.ca",
        "limit_rows_label": "Limiter les lignes (aperçu rapide)",
        "max_rows_label": "Nombre max de lignes à récupérer",
        "fetch_btn": "🔍 Récupérer les données",
        "sidebar_caption": (
            "Source : [Données ouvertes – Ville de Montréal](https://donnees.montreal.ca)  \n"
            "Construit avec Streamlit · [Code source sur GitHub](https://github.com)"
        ),
        "dataset_header": "📂 Jeu de données",
        "resource_id_caption": "Identifiant de ressource",
        "connecting_spinner": "Connexion à l'API de données ouvertes de Montréal…",
        "error_msg": "❌ Impossible de récupérer les données. Vérifiez l'identifiant de ressource et réessayez.",
        "no_records": "⚠️ Aucun enregistrement trouvé pour cet identifiant de ressource.",
        "rows_fetched": "Lignes récupérées",
        "columns": "Colonnes",
        "est_memory": "Mémoire estimée",
        "preview_header": "🔎 Aperçu des données",
        "filter_label": "Filtrer les lignes (recherche dans toutes les colonnes)",
        "filter_caption": "Affichage de {shown} lignes correspondantes sur {total}",
        "col_info_expander": "📋 Informations sur les colonnes",
        "col_name": "Colonne",
        "col_nonnull": "Non-nul",
        "col_null": "Nul",
        "col_dtype": "Type",
        "col_sample": "Exemple",
        "download_header": "⬇️ Téléchargement",
        "download_btn": "📥 Télécharger en CSV",
        "download_caption": "Le fichier sera enregistré sous `{filename}`",
        "idle_info": "👈 Entrez un **identifiant de ressource** dans la barre latérale et cliquez sur **Récupérer les données** pour commencer.",
        "how_to_header": "💡 Comment trouver un identifiant de ressource",
        "how_to_body": (
            "1. Allez sur **[donnees.montreal.ca](https://donnees.montreal.ca)**\n"
            "2. Recherchez un jeu de données (ex. *Travaux*, *Permis*, *Accidents*)\n"
            "3. Cliquez sur le jeu de données, puis sélectionnez une **ressource/fichier**\n"
            "4. L'identifiant de ressource apparaît dans l'URL de la page :\n"
            "   `https://donnees.montreal.ca/dataset/.../resource/<identifiant>`\n"
            "5. Collez-le dans le champ ci-dessus."
        ),
        "example_ids_header": "**Exemples d'identifiants de ressource :**",
        "example_table": (
            "| Jeu de données | Identifiant de ressource |\n"
            "|---|---|\n"
            "| Permis d'occupation du domaine public (Travaux) | `cc41b532-f12d-40fb-9f55-eb58c9a2b12b` |"
        ),
        "progress_text": "Récupéré {fetched} / {total} enregistrements…",
        "warn_no_resource": "Veuillez entrer un identifiant de ressource.",
        "language_toggle": "🇬🇧 English",
    },
}

# ── Session state ─────────────────────────────────────────────────────────────
if "lang" not in st.session_state:
    st.session_state.lang = "en"


def t(key):
    """Return translated string for the active language."""
    return TRANSLATIONS[st.session_state.lang][key]


# ── Constants ─────────────────────────────────────────────────────────────────
BASE_URL = "https://donnees.montreal.ca/api/3/action/datastore_search"
PACKAGE_URL = "https://donnees.montreal.ca/api/3/action/resource_show"
MAX_RETRIES = 5
PAGE_SIZE = 1_000


# ── API helpers ───────────────────────────────────────────────────────────────
def fetch_page(resource_id, offset=0, limit=PAGE_SIZE):
    params = {"resource_id": resource_id, "limit": limit, "offset": offset}
    base_wait = 5
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(BASE_URL, params=params, timeout=60)
            if resp.status_code == 429:
                time.sleep(base_wait * (2 ** attempt))
                continue
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException:
            if attempt < MAX_RETRIES - 1:
                time.sleep(base_wait * (2 ** attempt))
    return None


def fetch_resource_name(resource_id):
    try:
        resp = requests.get(PACKAGE_URL, params={"id": resource_id}, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if data.get("success"):
            return data["result"].get("name", resource_id)
    except Exception:
        pass
    return resource_id


def fetch_all_records(resource_id, max_rows=None):
    all_records = []
    total = None
    offset = 0

    progress_bar = st.progress(0, text=t("progress_text").format(fetched=0, total="?"))

    while True:
        data = fetch_page(resource_id, offset=offset)
        if data is None or not data.get("success"):
            st.error(t("error_msg"))
            progress_bar.empty()
            return None

        result = data["result"]
        if total is None:
            total = result["total"]

        records = result["records"]
        if not records:
            break

        all_records.extend(records)
        fetched = len(all_records)
        pct = min(int(fetched / total * 100), 100) if total > 0 else 100
        progress_bar.progress(pct, text=t("progress_text").format(fetched=f"{fetched:,}", total=f"{total:,}"))

        offset += len(records)

        if max_rows and fetched >= max_rows:
            all_records = all_records[:max_rows]
            break
        if offset >= total:
            break

        time.sleep(0.3)

    progress_bar.empty()

    if not all_records:
        st.warning(t("no_records"))
        return None

    df = pd.DataFrame(all_records)
    if "_id" in df.columns and len(df.columns) > 1:
        df = df.drop(columns=["_id"], errors="ignore")
    return df


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    # Language toggle button at the very top
    if st.button(t("language_toggle"), use_container_width=True):
        st.session_state.lang = "fr" if st.session_state.lang == "en" else "en"
        st.rerun()

    st.divider()
    st.header(t("sidebar_header"))

    resource_id = st.text_input(
        t("resource_id_label"),
        value="cc41b532-f12d-40fb-9f55-eb58c9a2b12b",
        placeholder=t("resource_id_placeholder"),
        help=t("resource_id_help"),
    )

    limit_rows = st.checkbox(t("limit_rows_label"), value=True)
    max_rows = st.slider(t("max_rows_label"), 100, 10_000, 2_000, step=100) if limit_rows else None

    fetch_btn = st.button(t("fetch_btn"), use_container_width=True, type="primary")

    st.divider()
    st.caption(t("sidebar_caption"))


# ── Main page ─────────────────────────────────────────────────────────────────
st.title(t("page_title"))
st.markdown(t("page_subtitle"))
st.divider()

if fetch_btn:
    if not resource_id.strip():
        st.warning(t("warn_no_resource"))
    else:
        resource_id = resource_id.strip()
        dataset_name = fetch_resource_name(resource_id)

        st.subheader(f"{t('dataset_header')}: `{dataset_name}`")
        st.caption(f"{t('resource_id_caption')}: `{resource_id}`")

        with st.spinner(t("connecting_spinner")):
            df = fetch_all_records(resource_id, max_rows=max_rows)

        if df is not None:
            # Metrics
            c1, c2, c3 = st.columns(3)
            c1.metric(t("rows_fetched"), f"{len(df):,}")
            c2.metric(t("columns"), f"{len(df.columns):,}")
            c3.metric(t("est_memory"), f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")

            # Preview
            st.subheader(t("preview_header"))
            search_term = st.text_input(t("filter_label"), "")
            if search_term:
                mask = df.apply(
                    lambda col: col.astype(str).str.contains(search_term, case=False, na=False)
                ).any(axis=1)
                display_df = df[mask]
                st.caption(t("filter_caption").format(shown=f"{len(display_df):,}", total=f"{len(df):,}"))
            else:
                display_df = df

            st.dataframe(display_df, use_container_width=True, height=450)

            # Column info
            with st.expander(t("col_info_expander")):
                col_info = pd.DataFrame({
                    t("col_name"): df.columns,
                    t("col_nonnull"): df.notna().sum().values,
                    t("col_null"): df.isna().sum().values,
                    t("col_dtype"): df.dtypes.astype(str).values,
                    t("col_sample"): [
                        str(df[c].dropna().iloc[0]) if df[c].notna().any() else "N/A"
                        for c in df.columns
                    ],
                })
                st.dataframe(col_info, use_container_width=True, hide_index=True)

            # Download
            st.subheader(t("download_header"))
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
            csv_bytes = csv_buffer.getvalue().encode("utf-8-sig")
            filename = f"{dataset_name.replace(' ', '_')}_{resource_id[:8]}.csv"
            st.download_button(
                label=t("download_btn"),
                data=csv_bytes,
                file_name=filename,
                mime="text/csv",
                use_container_width=True,
                type="primary",
            )
            st.caption(t("download_caption").format(filename=filename))

else:
    st.info(t("idle_info"))
    st.subheader(t("how_to_header"))
    st.markdown(t("how_to_body"))
    st.markdown(t("example_ids_header"))
    st.markdown(t("example_table"))
