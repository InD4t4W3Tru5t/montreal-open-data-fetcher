import streamlit as st
import requests
import pandas as pd
import time
import io

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Montréal Open Data Explorer",
    page_icon="🗺️",
    layout="wide",
)

# ── Header ───────────────────────────────────────────────────────────────────
st.title("🗺️ Montréal Open Data Explorer")
st.markdown(
    """
    Retrieve any dataset from the **[Ville de Montréal Open Data portal](https://donnees.montreal.ca)**  
    by entering its **Resource ID**. You can preview the data directly in the app or download it as a CSV file.
    """
)
st.divider()

# ── Constants ────────────────────────────────────────────────────────────────
BASE_URL = "https://donnees.montreal.ca/api/3/action/datastore_search"
PACKAGE_URL = "https://donnees.montreal.ca/api/3/action/resource_show"
MAX_RETRIES = 5
PAGE_SIZE = 1_000


# ── Helpers ──────────────────────────────────────────────────────────────────
def fetch_page(resource_id: str, offset: int = 0, limit: int = PAGE_SIZE) -> dict | None:
    """Fetch a single page of results from the Montreal CKAN DataStore."""
    params = {"resource_id": resource_id, "limit": limit, "offset": offset}
    base_wait = 5
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(BASE_URL, params=params, timeout=60)
            if resp.status_code == 429:
                wait = base_wait * (2 ** attempt)
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException:
            if attempt < MAX_RETRIES - 1:
                time.sleep(base_wait * (2 ** attempt))
    return None


def fetch_resource_name(resource_id: str) -> str:
    """Try to get the human-readable name for a resource."""
    try:
        resp = requests.get(PACKAGE_URL, params={"id": resource_id}, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if data.get("success"):
            return data["result"].get("name", resource_id)
    except Exception:
        pass
    return resource_id


def fetch_all_records(resource_id: str, max_rows: int | None = None) -> pd.DataFrame | None:
    """Paginate through the API and return a DataFrame of all (or up to max_rows) records."""
    all_records = []
    total = None
    offset = 0

    progress_bar = st.progress(0, text="Fetching data…")

    while True:
        data = fetch_page(resource_id, offset=offset)
        if data is None or not data.get("success"):
            st.error("❌ Failed to retrieve data. Please verify the Resource ID and try again.")
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
        progress_bar.progress(pct, text=f"Fetched {fetched:,} / {total:,} records…")

        offset += len(records)

        if max_rows and fetched >= max_rows:
            all_records = all_records[:max_rows]
            break
        if offset >= total:
            break

        time.sleep(0.3)  # be polite to the API

    progress_bar.empty()

    if not all_records:
        st.warning("⚠️ No records found for this Resource ID.")
        return None

    df = pd.DataFrame(all_records)
    # Drop CKAN internal rank column if present
    df = df.drop(columns=["_id"], errors="ignore") if "_id" in df.columns and len(df.columns) > 1 else df
    return df


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configuration")

    resource_id = st.text_input(
        "Resource ID",
        value="cc41b532-f12d-40fb-9f55-eb58c9a2b12b",
        placeholder="e.g. cc41b532-f12d-40fb-9f55-eb58c9a2b12b",
        help="Found in the URL of any dataset on donnees.montreal.ca",
    )

    limit_rows = st.checkbox("Limit rows (faster preview)", value=True)
    max_rows = st.slider("Max rows to fetch", 100, 10_000, 2_000, step=100) if limit_rows else None

    fetch_btn = st.button("🔍 Fetch Data", use_container_width=True, type="primary")

    st.divider()
    st.caption(
        "Data source: [Données ouvertes – Ville de Montréal](https://donnees.montreal.ca)  \n"
        "Built with Streamlit · [Source code on GitHub](https://github.com)"
    )

# ── Main panel ────────────────────────────────────────────────────────────────
if fetch_btn:
    if not resource_id.strip():
        st.warning("Please enter a Resource ID.")
    else:
        resource_id = resource_id.strip()
        dataset_name = fetch_resource_name(resource_id)

        st.subheader(f"📂 Dataset: `{dataset_name}`")
        st.caption(f"Resource ID: `{resource_id}`")

        with st.spinner("Connecting to the Montréal Open Data API…"):
            df = fetch_all_records(resource_id, max_rows=max_rows)

        if df is not None:
            # ── Metrics row ──────────────────────────────────────────────
            col1, col2, col3 = st.columns(3)
            col1.metric("Rows fetched", f"{len(df):,}")
            col2.metric("Columns", f"{len(df.columns):,}")
            col3.metric("Est. memory", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")

            # ── Data preview ─────────────────────────────────────────────
            st.subheader("🔎 Data Preview")
            search_term = st.text_input("Filter rows (searches all columns)", "")
            if search_term:
                mask = df.apply(
                    lambda col: col.astype(str).str.contains(search_term, case=False, na=False)
                ).any(axis=1)
                display_df = df[mask]
                st.caption(f"Showing {len(display_df):,} matching rows out of {len(df):,}")
            else:
                display_df = df

            st.dataframe(display_df, use_container_width=True, height=450)

            # ── Column info ──────────────────────────────────────────────
            with st.expander("📋 Column information"):
                col_info = pd.DataFrame({
                    "Column": df.columns,
                    "Non-null": df.notna().sum().values,
                    "Null": df.isna().sum().values,
                    "Dtype": df.dtypes.astype(str).values,
                    "Sample": [str(df[c].dropna().iloc[0]) if df[c].notna().any() else "N/A" for c in df.columns],
                })
                st.dataframe(col_info, use_container_width=True, hide_index=True)

            # ── Download ─────────────────────────────────────────────────
            st.subheader("⬇️ Download")
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
            csv_bytes = csv_buffer.getvalue().encode("utf-8-sig")

            filename = f"{dataset_name.replace(' ', '_')}_{resource_id[:8]}.csv"
            st.download_button(
                label="📥 Download as CSV",
                data=csv_bytes,
                file_name=filename,
                mime="text/csv",
                use_container_width=True,
                type="primary",
            )
            st.caption(f"File will be saved as `{filename}`")

else:
    st.info("👈 Enter a **Resource ID** in the sidebar and click **Fetch Data** to get started.")

    st.subheader("💡 How to find a Resource ID")
    st.markdown(
        """
        1. Go to **[donnees.montreal.ca](https://donnees.montreal.ca)**
        2. Search for any dataset (e.g. *Travaux*, *Permis*, *Accidents*)
        3. Click on the dataset, then select a **resource/file**
        4. The Resource ID appears in the page URL:  
           `https://donnees.montreal.ca/dataset/.../resource/**<resource-id>**`
        5. Paste it into the sidebar field above.

        **Example Resource IDs to try:**
        | Dataset | Resource ID |
        |---|---|
        | Permis d'occupation du domaine public (Travaux) | `cc41b532-f12d-40fb-9f55-eb58c9a2b12b` |
        """
    )
