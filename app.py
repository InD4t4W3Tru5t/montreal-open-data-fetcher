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
            "Browse and download datasets from the "
            "**[Ville de Montréal Open Data portal](https://donnees.montreal.ca)**."
        ),
        "sidebar_header": "⚙️ Configuration",
        "nav_browser": "📚 Dataset Browser",
        "nav_fetcher": "🔍 Fetch by Resource ID",
        "sidebar_caption": (
            "Data source: [Données ouvertes – Ville de Montréal](https://donnees.montreal.ca)  \n"
            "Built with Streamlit · [Source code on GitHub](https://github.com)"
        ),
        "browser_title": "📚 Dataset Browser",
        "browser_subtitle": "Browse all available datasets from the Montréal Open Data portal.",
        "search_datasets": "Search datasets",
        "search_placeholder": "e.g. permis, travaux, accidents…",
        "loading_catalog": "Loading dataset catalog…",
        "catalog_error": "❌ Could not load the dataset catalog. Please try again.",
        "results_count": "{count} dataset(s) found",
        "no_results": "No datasets match your search.",
        "col_title": "Title",
        "col_org": "Organization",
        "col_resources": "Resources",
        "col_updated": "Last updated",
        "col_notes": "Description",
        "select_dataset": "Select a dataset to preview",
        "dataset_detail_title": "📂 Dataset details",
        "resources_available": "Resources available",
        "res_name": "Name",
        "res_format": "Format",
        "res_id": "Resource ID",
        "fetch_this": "Fetch this resource",
        "preview_header": "🔎 Preview",
        "download_header": "⬇️ Download",
        "download_btn": "📥 Download as CSV",
        "download_btn_raw": "📥 Download {fmt} file",
        "download_caption": "File: `{filename}`",
        "rows_fetched": "Rows fetched",
        "columns": "Columns",
        "est_memory": "Est. memory",
        "filter_label": "Filter rows",
        "filter_caption": "Showing {shown} of {total} rows",
        "col_info_expander": "📋 Column information",
        "col_name": "Column",
        "col_nonnull": "Non-null",
        "col_null": "Null",
        "col_dtype": "Dtype",
        "col_sample": "Sample",
        "fetcher_title": "🔍 Fetch by Resource ID",
        "fetcher_subtitle": (
            "Enter any Resource ID from the Montréal Open Data portal to preview and download the dataset."
        ),
        "resource_id_label": "Resource ID",
        "resource_id_placeholder": "e.g. cc41b532-f12d-40fb-9f55-eb58c9a2b12b",
        "resource_id_help": "Found in the URL of any dataset on donnees.montreal.ca",
        "limit_rows_label": "Limit rows (faster preview)",
        "max_rows_label": "Max rows to fetch",
        "fetch_btn": "🔍 Fetch Data",
        "resource_id_caption": "Resource ID",
        "connecting_spinner": "Connecting to the Montréal Open Data API…",
        "downloading_spinner": "Downloading file…",
        "error_msg": "❌ Failed to retrieve data. Please verify the Resource ID and try again.",
        "download_error": "❌ Could not download the file. The URL may be unavailable.",
        "no_records": "⚠️ No records found for this Resource ID.",
        "warn_no_resource": "Please enter a Resource ID.",
        "idle_info": "👈 Enter a **Resource ID** and click **Fetch Data** to get started.",
        "how_to_header": "💡 How to find a Resource ID",
        "how_to_body": (
            "1. Use the **Dataset Browser** tab on the left\n"
            "2. Or go to **[donnees.montreal.ca](https://donnees.montreal.ca)**\n"
            "3. Open any dataset and click on a resource tab\n"
            "4. Copy the UUID from the URL: `.../resource/<resource-id>`"
        ),
        "progress_text": "Fetched {fetched} / {total} records…",
        "language_toggle": "Français",
        "dataset_header": "📂 Dataset",
        "loading_total": "Checking total record count…",
        "total_records_info": "This resource contains **{total:,} rows** in total.",
        "limit_rows_browser": "Limit rows",
        "max_rows_browser": "Rows to fetch (out of {total:,} total)",
        "fetch_all_warning": "Fetching all {total:,} rows may take a while depending on dataset size.",
        "non_csv_info": (
            "ℹ️ This resource is in **{fmt}** format and cannot be previewed in-app. "
            "You can download it directly below."
        ),
        "non_csv_fetcher_info": (
            "ℹ️ This Resource ID points to a **{fmt}** file. "
            "Direct preview is not available — you can download it below."
        ),
        "checking_resource": "Checking resource type…",
        "unknown_format": "UNKNOWN",
    },
    "fr": {
        "page_title": "🗺️ Explorateur – Données ouvertes de Montréal",
        "page_subtitle": (
            "Parcourez et téléchargez les jeux de données du "
            "**[portail de données ouvertes de la Ville de Montréal](https://donnees.montreal.ca)**."
        ),
        "sidebar_header": "⚙️ Configuration",
        "nav_browser": "📚 Navigateur de données",
        "nav_fetcher": "🔍 Récupérer par identifiant",
        "sidebar_caption": (
            "Source : [Données ouvertes – Ville de Montréal](https://donnees.montreal.ca)  \n"
            "Construit avec Streamlit · [Code source sur GitHub](https://github.com)"
        ),
        "browser_title": "📚 Navigateur de données",
        "browser_subtitle": "Parcourez tous les jeux de données disponibles sur le portail de données ouvertes de Montréal.",
        "search_datasets": "Rechercher des jeux de données",
        "search_placeholder": "ex. permis, travaux, accidents…",
        "loading_catalog": "Chargement du catalogue…",
        "catalog_error": "❌ Impossible de charger le catalogue. Veuillez réessayer.",
        "results_count": "{count} jeu(x) de données trouvé(s)",
        "no_results": "Aucun jeu de données ne correspond à votre recherche.",
        "col_title": "Titre",
        "col_org": "Organisation",
        "col_resources": "Ressources",
        "col_updated": "Dernière mise à jour",
        "col_notes": "Description",
        "select_dataset": "Sélectionnez un jeu de données",
        "dataset_detail_title": "📂 Détails du jeu de données",
        "resources_available": "Ressources disponibles",
        "res_name": "Nom",
        "res_format": "Format",
        "res_id": "Identifiant de ressource",
        "fetch_this": "Récupérer cette ressource",
        "preview_header": "🔎 Aperçu",
        "download_header": "⬇️ Téléchargement",
        "download_btn": "📥 Télécharger en CSV",
        "download_btn_raw": "📥 Télécharger le fichier {fmt}",
        "download_caption": "Fichier : `{filename}`",
        "rows_fetched": "Lignes récupérées",
        "columns": "Colonnes",
        "est_memory": "Mémoire estimée",
        "filter_label": "Filtrer les lignes",
        "filter_caption": "Affichage de {shown} lignes sur {total}",
        "col_info_expander": "📋 Informations sur les colonnes",
        "col_name": "Colonne",
        "col_nonnull": "Non-nul",
        "col_null": "Nul",
        "col_dtype": "Type",
        "col_sample": "Exemple",
        "fetcher_title": "🔍 Récupérer par identifiant de ressource",
        "fetcher_subtitle": (
            "Entrez n'importe quel identifiant de ressource du portail de données ouvertes de Montréal "
            "pour prévisualiser et télécharger le jeu de données."
        ),
        "resource_id_label": "Identifiant de ressource",
        "resource_id_placeholder": "ex. cc41b532-f12d-40fb-9f55-eb58c9a2b12b",
        "resource_id_help": "Visible dans l'URL de n'importe quel jeu de données sur donnees.montreal.ca",
        "limit_rows_label": "Limiter les lignes (aperçu rapide)",
        "max_rows_label": "Nombre max de lignes à récupérer",
        "fetch_btn": "🔍 Récupérer les données",
        "resource_id_caption": "Identifiant de ressource",
        "connecting_spinner": "Connexion à l'API de données ouvertes de Montréal…",
        "downloading_spinner": "Téléchargement du fichier…",
        "error_msg": "❌ Impossible de récupérer les données. Vérifiez l'identifiant et réessayez.",
        "download_error": "❌ Impossible de télécharger le fichier. L'URL est peut-être indisponible.",
        "no_records": "⚠️ Aucun enregistrement trouvé pour cet identifiant de ressource.",
        "warn_no_resource": "Veuillez entrer un identifiant de ressource.",
        "idle_info": "👈 Entrez un **identifiant de ressource** et cliquez sur **Récupérer les données** pour commencer.",
        "how_to_header": "💡 Comment trouver un identifiant de ressource",
        "how_to_body": (
            "1. Utilisez l'onglet **Navigateur de données** à gauche\n"
            "2. Ou allez sur **[donnees.montreal.ca](https://donnees.montreal.ca)**\n"
            "3. Ouvrez un jeu de données et cliquez sur un onglet de ressource\n"
            "4. Copiez l'UUID dans l'URL : `.../resource/<identifiant>`"
        ),
        "progress_text": "Récupéré {fetched} / {total} enregistrements…",
        "language_toggle": "English",
        "dataset_header": "📂 Jeu de données",
        "loading_total": "Vérification du nombre total d'enregistrements…",
        "total_records_info": "Cette ressource contient **{total:,} lignes** au total.",
        "limit_rows_browser": "Limiter les lignes",
        "max_rows_browser": "Lignes à récupérer (sur {total:,} au total)",
        "fetch_all_warning": "Récupérer les {total:,} lignes peut prendre du temps selon la taille du jeu de données.",
        "non_csv_info": (
            "ℹ️ Cette ressource est au format **{fmt}** et ne peut pas être prévisualisée dans l'application. "
            "Vous pouvez la télécharger directement ci-dessous."
        ),
        "non_csv_fetcher_info": (
            "ℹ️ Cet identifiant pointe vers un fichier **{fmt}**. "
            "L'aperçu n'est pas disponible — vous pouvez le télécharger ci-dessous."
        ),
        "checking_resource": "Vérification du type de ressource…",
        "unknown_format": "INCONNU",
    },
}

# ── Session state ─────────────────────────────────────────────────────────────
if "lang"            not in st.session_state: st.session_state.lang            = "en"
if "fetch_triggered" not in st.session_state: st.session_state.fetch_triggered = False
if "fetched_rid"     not in st.session_state: st.session_state.fetched_rid     = None
if "fetched_name"    not in st.session_state: st.session_state.fetched_name    = None
if "fetched_df"      not in st.session_state: st.session_state.fetched_df      = None
if "last_pkg_title"  not in st.session_state: st.session_state.last_pkg_title  = None
if "last_res_label"  not in st.session_state: st.session_state.last_res_label  = None
if "res_total_count" not in st.session_state: st.session_state.res_total_count = None


def t(key):
    return TRANSLATIONS[st.session_state.lang][key]


# ── Constants ─────────────────────────────────────────────────────────────────
BASE_URL       = "https://donnees.montreal.ca/api/3/action/datastore_search"
PACKAGE_SEARCH = "https://donnees.montreal.ca/api/3/action/package_search"
PACKAGE_URL    = "https://donnees.montreal.ca/api/3/action/resource_show"
MAX_RETRIES    = 5
PAGE_SIZE      = 1_000
CSV_FORMATS    = {"CSV", "TSV", "XLS", "XLSX"}


# ── Helpers ───────────────────────────────────────────────────────────────────
def is_tabular(fmt: str) -> bool:
    """Return True if the format can be fetched via the DataStore API."""
    return fmt.upper() in CSV_FORMATS


@st.cache_data(ttl=3600, show_spinner=False)
def load_catalog():
    all_packages = []
    start, rows  = 0, 100
    while True:
        try:
            resp = requests.get(
                PACKAGE_SEARCH,
                params={"rows": rows, "start": start, "sort": "metadata_modified desc"},
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
            if not data.get("success"):
                break
            results = data["result"]["results"]
            if not results:
                break
            all_packages.extend(results)
            start += len(results)
            if start >= data["result"]["count"]:
                break
            time.sleep(0.2)
        except Exception:
            break
    return all_packages


@st.cache_data(ttl=600, show_spinner=False)
def get_resource_total(resource_id):
    """Lightweight call to get total row count from the DataStore."""
    try:
        resp = requests.get(
            BASE_URL,
            params={"resource_id": resource_id, "limit": 1, "offset": 0},
            timeout=20,
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("success"):
            return data["result"]["total"]
    except Exception:
        pass
    return None


@st.cache_data(ttl=600, show_spinner=False)
def get_resource_meta(resource_id):
    """Return (format, url) for a resource ID via resource_show."""
    try:
        resp = requests.get(PACKAGE_URL, params={"id": resource_id}, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if data.get("success"):
            r = data["result"]
            return (r.get("format", ""), r.get("url", ""), r.get("name", resource_id))
    except Exception:
        pass
    return ("", "", resource_id)


def download_raw_file(url: str, filename: str, fmt: str):
    """Download a non-CSV file from its URL and offer it as a download button."""
    try:
        with st.spinner(t("downloading_spinner")):
            resp = requests.get(url, timeout=60)
            resp.raise_for_status()
            file_bytes = resp.content
        mime_map = {
            "JSON":    "application/json",
            "GEOJSON": "application/geo+json",
            "XML":     "application/xml",
            "SHP":     "application/zip",
            "KML":     "application/vnd.google-earth.kml+xml",
            "PDF":     "application/pdf",
            "XLS":     "application/vnd.ms-excel",
            "XLSX":    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        }
        mime = mime_map.get(fmt.upper(), "application/octet-stream")
        st.download_button(
            label=t("download_btn_raw").format(fmt=fmt.upper()),
            data=file_bytes,
            file_name=filename,
            mime=mime,
            use_container_width=True,
            type="primary",
        )
        st.caption(t("download_caption").format(filename=filename))
    except Exception:
        st.error(t("download_error"))


def fetch_page(resource_id, offset=0, limit=PAGE_SIZE):
    params    = {"resource_id": resource_id, "limit": limit, "offset": offset}
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


def fetch_all_records(resource_id, max_rows=None):
    all_records  = []
    total        = None
    offset       = 0
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
        pct     = min(int(fetched / total * 100), 100) if total > 0 else 100
        progress_bar.progress(
            pct,
            text=t("progress_text").format(fetched=f"{fetched:,}", total=f"{total:,}"),
        )
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
        df = df.drop(columns=["_id"])
    return df


def render_data_panel(df, resource_id, dataset_name):
    """Metrics, preview, column info, CSV download."""
    st.caption(f"{t('resource_id_caption')}: `{resource_id}`")

    c1, c2, c3 = st.columns(3)
    c1.metric(t("rows_fetched"), f"{len(df):,}")
    c2.metric(t("columns"),      f"{len(df.columns):,}")
    c3.metric(t("est_memory"),   f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")

    st.subheader(t("preview_header"))
    search_term = st.text_input(t("filter_label"), value="", key=f"filter_{resource_id}")
    if search_term:
        mask = df.apply(
            lambda col: col.astype(str).str.contains(search_term, case=False, na=False)
        ).any(axis=1)
        display_df = df[mask]
        st.caption(t("filter_caption").format(shown=f"{len(display_df):,}", total=f"{len(df):,}"))
    else:
        display_df = df

    st.dataframe(display_df, use_container_width=True, height=420)

    with st.expander(t("col_info_expander")):
        col_info = pd.DataFrame({
            t("col_name"):    df.columns,
            t("col_nonnull"): df.notna().sum().values,
            t("col_null"):    df.isna().sum().values,
            t("col_dtype"):   df.dtypes.astype(str).values,
            t("col_sample"):  [
                str(df[c].dropna().iloc[0]) if df[c].notna().any() else "N/A"
                for c in df.columns
            ],
        })
        st.dataframe(col_info, use_container_width=True, hide_index=True)

    st.subheader(t("download_header"))
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
    csv_bytes = csv_buffer.getvalue().encode("utf-8-sig")
    filename  = f"{dataset_name.replace(' ', '_')}_{resource_id[:8]}.csv"
    st.download_button(
        label=t("download_btn"),
        data=csv_bytes,
        file_name=filename,
        mime="text/csv",
        use_container_width=True,
        type="primary",
    )
    st.caption(t("download_caption").format(filename=filename))


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    if st.button(t("language_toggle"), use_container_width=True):
        st.session_state.lang = "fr" if st.session_state.lang == "en" else "en"
        st.rerun()

    st.divider()
    st.header(t("sidebar_header"))

    page = st.radio(
        label="Navigation",
        options=["browser", "fetcher"],
        format_func=lambda x: t("nav_browser") if x == "browser" else t("nav_fetcher"),
        label_visibility="collapsed",
    )

    if page == "fetcher":
        st.divider()
        resource_id_input = st.text_input(
            label=t("resource_id_label"),
            value="cc41b532-f12d-40fb-9f55-eb58c9a2b12b",
            placeholder=t("resource_id_placeholder"),
            help=t("resource_id_help"),
        )
        limit_rows = st.checkbox(t("limit_rows_label"), value=True)
        max_rows   = (
            st.slider(t("max_rows_label"), 100, 10_000, 2_000, step=100)
            if limit_rows else None
        )
        fetch_btn = st.button(t("fetch_btn"), use_container_width=True, type="primary")
    else:
        resource_id_input = None
        max_rows          = None
        fetch_btn         = False

    st.divider()
    st.caption(t("sidebar_caption"))


# ── Main page header ──────────────────────────────────────────────────────────
st.title(t("page_title"))
st.markdown(t("page_subtitle"))
st.divider()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: Dataset Browser
# ══════════════════════════════════════════════════════════════════════════════
if page == "browser":
    st.subheader(t("browser_title"))
    st.markdown(t("browser_subtitle"))

    search_query = st.text_input(
        t("search_datasets"),
        placeholder=t("search_placeholder"),
        key="catalog_search",
    )

    with st.spinner(t("loading_catalog")):
        catalog = load_catalog()

    if not catalog:
        st.error(t("catalog_error"))
        st.stop()

    if search_query:
        q = search_query.lower()
        catalog = [
            p for p in catalog
            if q in (p.get("title") or "").lower()
            or q in (p.get("notes") or "").lower()
            or any(q in (r.get("name") or "").lower() for r in p.get("resources", []))
        ]

    st.caption(t("results_count").format(count=len(catalog)))

    if not catalog:
        st.info(t("no_results"))
        st.stop()

    rows = []
    for pkg in catalog:
        org      = pkg.get("organization") or {}
        last_mod = (pkg.get("metadata_modified") or "")[:10]
        rows.append({
            t("col_title"):     pkg.get("title", pkg.get("name", "N/A")),
            t("col_org"):       org.get("title", "N/A") if isinstance(org, dict) else "N/A",
            t("col_resources"): len(pkg.get("resources", [])),
            t("col_updated"):   last_mod,
        })

    dataset_titles = [pkg.get("title", pkg.get("name", "N/A")) for pkg in catalog]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, height=320, hide_index=True)

    selected_title = st.selectbox(
        label=t("select_dataset"),
        options=dataset_titles,
        key="pkg_selectbox",
    )

    if selected_title != st.session_state.last_pkg_title:
        st.session_state.last_pkg_title  = selected_title
        st.session_state.fetch_triggered = False
        st.session_state.fetched_df      = None
        st.session_state.last_res_label  = None
        st.session_state.res_total_count = None

    selected_pkg = next(
        (p for p in catalog if p.get("title", p.get("name")) == selected_title), None
    )

    if selected_pkg:
        st.subheader(t("dataset_detail_title"))

        notes = selected_pkg.get("notes") or ""
        if notes:
            with st.expander(t("col_notes"), expanded=False):
                st.markdown(notes[:800] + ("…" if len(notes) > 800 else ""))

        resources = selected_pkg.get("resources", [])
        st.markdown(f"**{t('resources_available')}**: {len(resources)}")

        if resources:
            res_rows = []
            for r in resources:
                res_rows.append({
                    t("res_name"):   r.get("name", "N/A"),
                    t("res_format"): (r.get("format") or "N/A").upper(),
                    t("res_id"):     r.get("id", "N/A"),
                })
            st.dataframe(pd.DataFrame(res_rows), use_container_width=True, hide_index=True)

            def res_label(r):
                fmt  = (r.get("format") or "N/A").upper()
                name = r.get("name") or r.get("id", "N/A")
                return f"{name}  [{fmt}]"

            res_labels         = [res_label(r) for r in resources]
            selected_res_label = st.selectbox(
                label=t("fetch_this"),
                options=res_labels,
                key="res_selectbox",
            )

            if selected_res_label != st.session_state.last_res_label:
                st.session_state.last_res_label  = selected_res_label
                st.session_state.fetch_triggered = False
                st.session_state.fetched_df      = None
                st.session_state.res_total_count = None

            selected_res = resources[res_labels.index(selected_res_label)]
            rid          = selected_res.get("id", "")
            res_name     = selected_res.get("name", rid)
            res_fmt      = (selected_res.get("format") or "").upper()
            res_url      = selected_res.get("url", "")

            # ── Non-tabular resource: direct download only ────────────────
            if res_fmt and not is_tabular(res_fmt):
                st.info(t("non_csv_info").format(fmt=res_fmt))
                st.subheader(t("download_header"))
                ext      = res_fmt.lower()
                filename = f"{res_name.replace(' ', '_')}_{rid[:8]}.{ext}"
                download_raw_file(res_url, filename, res_fmt)

            # ── Tabular resource: fetch + preview ─────────────────────────
            else:
                if st.session_state.res_total_count is None and rid:
                    with st.spinner(t("loading_total")):
                        st.session_state.res_total_count = get_resource_total(rid)

                total_count = st.session_state.res_total_count

                if total_count and total_count > 0:
                    st.info(t("total_records_info").format(total=total_count))
                    limit_rows_browser = st.checkbox(
                        t("limit_rows_browser"), value=True, key="limit_rows_browser_cb"
                    )
                    if limit_rows_browser:
                        browser_max_rows = st.slider(
                            label=t("max_rows_browser").format(total=total_count),
                            min_value=100,
                            max_value=total_count,
                            value=min(2_000, total_count),
                            step=max(100, total_count // 100),
                            key="browser_row_slider",
                        )
                    else:
                        browser_max_rows = None
                        st.warning(t("fetch_all_warning").format(total=total_count))
                else:
                    browser_max_rows = None

                if st.button(t("fetch_this"), type="primary", use_container_width=True):
                    with st.spinner(t("connecting_spinner")):
                        df = fetch_all_records(rid, max_rows=browser_max_rows)
                    if df is not None:
                        st.session_state.fetch_triggered = True
                        st.session_state.fetched_rid     = rid
                        st.session_state.fetched_name    = res_name
                        st.session_state.fetched_df      = df

                if st.session_state.fetch_triggered and st.session_state.fetched_df is not None:
                    st.subheader(t("preview_header"))
                    render_data_panel(
                        st.session_state.fetched_df,
                        st.session_state.fetched_rid,
                        st.session_state.fetched_name,
                    )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: Fetch by Resource ID
# ══════════════════════════════════════════════════════════════════════════════
elif page == "fetcher":
    st.subheader(t("fetcher_title"))
    st.markdown(t("fetcher_subtitle"))

    if fetch_btn:
        if not resource_id_input.strip():
            st.warning(t("warn_no_resource"))
        else:
            rid = resource_id_input.strip()

            # Resolve format from resource_show
            with st.spinner(t("checking_resource")):
                res_fmt, res_url, res_name = get_resource_meta(rid)

            res_fmt_upper = res_fmt.upper() if res_fmt else ""

            st.subheader(f"{t('dataset_header')}: `{res_name}`")

            # ── Non-tabular: direct download ──────────────────────────────
            if res_fmt_upper and not is_tabular(res_fmt_upper):
                st.info(t("non_csv_fetcher_info").format(fmt=res_fmt_upper))
                st.subheader(t("download_header"))
                ext      = res_fmt_upper.lower()
                filename = f"{res_name.replace(' ', '_')}_{rid[:8]}.{ext}"
                download_raw_file(res_url, filename, res_fmt_upper)

            # ── Tabular: fetch + preview ──────────────────────────────────
            else:
                with st.spinner(t("connecting_spinner")):
                    df = fetch_all_records(rid, max_rows=max_rows)
                if df is not None:
                    render_data_panel(df, rid, res_name)
    else:
        st.info(t("idle_info"))
        st.subheader(t("how_to_header"))
        st.markdown(t("how_to_body"))
