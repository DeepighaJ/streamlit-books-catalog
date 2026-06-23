"""
Books Dashboard - Day 3 (Updated)
Run with: streamlit run dashboard.py
"""

import pandas as pd
import plotly.express as px
import streamlit as st


# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Books Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# CUSTOM CSS  — clean card-based UI, better sidebar, styled metrics
# ---------------------------------------------------------------------------

st.markdown("""
<style>

/* ---- page background ---- */
.stApp { background-color: #f5f6fa; }

/* ---- sidebar ---- */
[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e8eaf0;
}
[data-testid="stSidebar"] .stMarkdown h2 {
    font-size: 15px;
    font-weight: 600;
    color: #1a1a2e;
    margin-bottom: 4px;
}

/* ---- metric cards ---- */
[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e8eaf0;
    border-radius: 10px;
    padding: 14px 18px;
}
[data-testid="stMetric"] label {
    font-size: 12px !important;
    color: #6b7280 !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
[data-testid="stMetricValue"] {
    font-size: 22px !important;
    font-weight: 700 !important;
    color: #1a1a2e !important;
}

/* ---- section headers ---- */
h2 { color: #1a1a2e !important; font-weight: 600 !important; }
h3 { color: #374151 !important; font-weight: 600 !important; font-size: 16px !important; }

/* ---- chart containers ---- */
[data-testid="stPlotlyChart"] {
    background: #ffffff;
    border: 1px solid #e8eaf0;
    border-radius: 12px;
    padding: 12px;
}

/* ---- dataframe ---- */
[data-testid="stDataFrame"] {
    border: 1px solid #e8eaf0;
    border-radius: 10px;
    overflow: hidden;
}

/* ---- selectbox and text input ---- */
[data-testid="stSelectbox"] > div > div,
[data-testid="stTextInput"] > div > div > input {
    border-radius: 8px !important;
    border-color: #e8eaf0 !important;
    background: #ffffff !important;
}

/* ---- book detail card ---- */
.book-card {
    background: #ffffff;
    border: 1px solid #e8eaf0;
    border-radius: 12px;
    padding: 22px 26px;
    margin-top: 8px;
}
.book-card .bc-title {
    font-size: 17px;
    font-weight: 700;
    color: #1a1a2e;
    margin-bottom: 6px;
}
.book-card .bc-cat {
    display: inline-block;
    background: #eef2ff;
    color: #4f46e5;
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 99px;
    margin-bottom: 14px;
}
.book-card .bc-row {
    display: flex;
    gap: 32px;
    margin-bottom: 14px;
}
.book-card .bc-stat { flex: 1; }
.book-card .bc-stat-label {
    font-size: 11px;
    color: #9ca3af;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 2px;
}
.book-card .bc-stat-value {
    font-size: 20px;
    font-weight: 700;
    color: #1a1a2e;
}
.book-card .bc-field {
    font-size: 13px;
    color: #4b5563;
    margin-bottom: 6px;
    line-height: 1.5;
}
.book-card .bc-field b { color: #1a1a2e; }
.book-card .bc-upc {
    font-family: monospace;
    background: #f3f4f6;
    padding: 2px 8px;
    border-radius: 5px;
    font-size: 12px;
    color: #6366f1;
}
.book-card .bc-desc {
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid #f0f0f5;
    font-size: 13px;
    color: #6b7280;
    line-height: 1.7;
    max-height: 140px;
    overflow-y: auto;
}
.star-gold { color: #f59e0b; font-size: 16px; }

/* ---- divider ---- */
hr { border-color: #e8eaf0 !important; margin: 8px 0 !important; }

/* ---- sort row ---- */
.sort-label {
    font-size: 13px;
    color: #6b7280;
    font-weight: 500;
    margin-bottom: 4px;
}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------------------------

@st.cache_data
def load_data(path: str = "all_books.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df["price"]       = pd.to_numeric(df["price"],       errors="coerce")
    df["rating"]      = pd.to_numeric(df["rating"],      errors="coerce")
    df["stock_count"] = pd.to_numeric(df["stock_count"], errors="coerce")
    df["stars"]       = df["rating"].apply(
        lambda r: "★" * int(r) + "☆" * (5 - int(r)) if pd.notna(r) else "N/A"
    )
    return df


try:
    df = load_data()
except FileNotFoundError:
    st.error("⚠️  `all_books.csv` not found. Run `python scrape_all_books.py` first.")
    st.stop()


# ---------------------------------------------------------------------------
# PLOTLY CHART CONFIG — disables the modebar (crop/zoom toolbar)
# ---------------------------------------------------------------------------

CHART_CFG = {
    "displayModeBar": False,        # removes the toolbar entirely
    "scrollZoom": False,
}

# Shared hover style used across all charts
HOVER_LABEL = dict(
    bgcolor="white",
    bordercolor="#e8eaf0",
    font_size=13,
    font_color="#1a1a2e",
)


# ---------------------------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown("## 🔍 Filter books")
    st.divider()

    all_categories = sorted(df["category"].dropna().unique())
    selected_categories = st.multiselect(
        "Category",
        options=all_categories,
        default=all_categories,
    )

    st.divider()
    min_price = float(df["price"].min())
    max_price = float(df["price"].max())
    price_range = st.slider(
        "Price range (£)",
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price),
        step=0.5,
    )

    st.divider()
    min_rating = st.selectbox("Minimum rating (stars)", [1, 2, 3, 4, 5], index=0)

    st.divider()
    in_stock_only = st.checkbox("In stock only", value=False)

    st.divider()
    keyword = st.text_input("Search title or description", placeholder="e.g. love, dark…")


# ---------------------------------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------------------------------

filtered = df.copy()
if selected_categories:
    filtered = filtered[filtered["category"].isin(selected_categories)]
filtered = filtered[
    (filtered["price"] >= price_range[0]) &
    (filtered["price"] <= price_range[1])
]
filtered = filtered[filtered["rating"] >= min_rating]
if in_stock_only:
    filtered = filtered[filtered["availability"].str.contains("In stock", na=False)]
if keyword:
    kw = keyword.lower()
    filtered = filtered[
        filtered["title"].str.lower().str.contains(kw, na=False) |
        filtered["description"].fillna("").str.lower().str.contains(kw, na=False)
    ]


# ---------------------------------------------------------------------------
# HEADER
# ---------------------------------------------------------------------------

st.markdown("## 📚 Books Catalog Dashboard")
st.caption("Data scraped from books.toscrape.com · BeautifulSoup Day 3")
st.divider()


# ---------------------------------------------------------------------------
# SUMMARY METRICS
# ---------------------------------------------------------------------------

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Books shown",   f"{len(filtered):,}")
c2.metric("Avg price",     f"£{filtered['price'].mean():.2f}"  if len(filtered) else "—")
c3.metric("Avg rating",    f"{filtered['rating'].mean():.1f} ★" if len(filtered) else "—")
c4.metric("Categories",    filtered["category"].nunique())
c5.metric("In stock",      filtered["availability"].str.contains("In stock", na=False).sum())

st.divider()

if filtered.empty:
    st.warning("No books match your current filters. Try widening the range.")
    st.stop()


# ---------------------------------------------------------------------------
# CHARTS — row 1
# ---------------------------------------------------------------------------

col_l, col_r = st.columns(2)

with col_l:
    st.markdown("### Price distribution")
    fig = px.histogram(
        filtered, x="price", nbins=30,
        labels={"price": "Price (£)", "count": "Books"},
        color_discrete_sequence=["#6366f1"],
    )
    fig.update_traces(
        hovertemplate="<b>£%{x:.2f}</b><br>%{y} books<extra></extra>",
    )
    fig.update_layout(
        margin=dict(t=8, b=8, l=8, r=8),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        bargap=0.05,
        hoverlabel=HOVER_LABEL,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f5"),
    )
    st.plotly_chart(fig, use_container_width=True, config=CHART_CFG)

with col_r:
    st.markdown("### Rating breakdown")
    rc = (
        filtered["rating"].value_counts().sort_index().reset_index()
    )
    rc.columns = ["rating", "count"]
    rc["label"] = rc["rating"].apply(lambda r: "★" * int(r))
    RATING_COLORS = {1:"#f87171", 2:"#fb923c", 3:"#facc15", 4:"#4ade80", 5:"#34d399"}
    rc["color"] = rc["rating"].map(RATING_COLORS)
    fig = px.bar(
        rc, x="label", y="count",
        labels={"label": "Stars", "count": "Books"},
        color="rating",
        color_discrete_map={k: v for k, v in RATING_COLORS.items()},
    )
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>%{y} books<extra></extra>",
    )
    fig.update_layout(
        margin=dict(t=8, b=8, l=8, r=8),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        showlegend=False,
        hoverlabel=HOVER_LABEL,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f5"),
    )
    st.plotly_chart(fig, use_container_width=True, config=CHART_CFG)


# ---------------------------------------------------------------------------
# CHARTS — row 2
# ---------------------------------------------------------------------------

col_l2, col_r2 = st.columns(2)

with col_l2:
    st.markdown("### Books per category")
    cat_counts = (
        filtered["category"].value_counts().reset_index()
    )
    cat_counts.columns = ["category", "count"]
    fig = px.bar(
        cat_counts.head(15), x="count", y="category", orientation="h",
        labels={"count": "Number of books", "category": ""},
        color="count",
        color_continuous_scale=[[0,"#c7d2fe"],[1,"#4f46e5"]],
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>%{x} books<extra></extra>",
    )
    fig.update_layout(
        margin=dict(t=8, b=8, l=8, r=8),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        coloraxis_showscale=False,
        yaxis=dict(categoryorder="total ascending", showgrid=False),
        xaxis=dict(showgrid=True, gridcolor="#f0f0f5"),
        hoverlabel=HOVER_LABEL,
        height=380,
    )
    st.plotly_chart(fig, use_container_width=True, config=CHART_CFG)

with col_r2:
    st.markdown("### Average price by category")
    avg_p = (
        filtered.groupby("category")["price"]
        .mean().sort_values(ascending=False)
        .head(15).reset_index()
    )
    avg_p.columns = ["category", "avg_price"]
    fig = px.bar(
        avg_p, x="avg_price", y="category", orientation="h",
        labels={"avg_price": "Avg price (£)", "category": ""},
        color="avg_price",
        color_continuous_scale=[[0,"#fed7aa"],[1,"#ea580c"]],
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Avg: £%{x:.2f}<extra></extra>",
    )
    fig.update_layout(
        margin=dict(t=8, b=8, l=8, r=8),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        coloraxis_showscale=False,
        yaxis=dict(categoryorder="total ascending", showgrid=False),
        xaxis=dict(showgrid=True, gridcolor="#f0f0f5"),
        hoverlabel=HOVER_LABEL,
        height=380,
    )
    st.plotly_chart(fig, use_container_width=True, config=CHART_CFG)


# ---------------------------------------------------------------------------
# CHART — scatter (full width)
# ---------------------------------------------------------------------------

st.markdown("### Price vs rating")
fig = px.scatter(
    filtered, x="price", y="rating",
    color="category",
    hover_data={"title": True, "stock_count": True, "category": False},
    labels={"price": "Price (£)", "rating": "Stars", "category": "Category"},
    opacity=0.75,
)
fig.update_traces(
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>"
        "Price: £%{x:.2f}<br>"
        "Rating: %{y} ★<br>"
        "In stock: %{customdata[1]}<extra></extra>"
    ),
    marker_size=8,
)
fig.update_layout(
    margin=dict(t=8, b=8, l=8, r=8),
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    hoverlabel=HOVER_LABEL,
    legend_title="Category",
    xaxis=dict(showgrid=True, gridcolor="#f0f0f5"),
    yaxis=dict(showgrid=True, gridcolor="#f0f0f5", dtick=1),
    height=380,
)
st.plotly_chart(fig, use_container_width=True, config=CHART_CFG)


# ---------------------------------------------------------------------------
# CHART — stock availability donut (two columns: donut + mini stats)
# ---------------------------------------------------------------------------

st.markdown("### Stock availability")
donut_col, stats_col = st.columns([2, 1])

with donut_col:
    avail_counts = (
        filtered["availability"]
        .value_counts()
        .reset_index()
    )
    avail_counts.columns = ["availability", "count"]

    fig = px.pie(
        avail_counts,
        names="availability",
        values="count",
        hole=0.55,
        color_discrete_sequence=["#4f46e5", "#e0e7ff", "#6366f1"],
    )
    fig.update_traces(
        # Labels shown directly on each slice — no separate legend needed
        textinfo="label+percent",
        textposition="outside",
        hovertemplate="<b>%{label}</b><br>%{value} books (%{percent})<extra></extra>",
        pull=[0.03] * len(avail_counts),        # slight pull on every slice
    )
    fig.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        paper_bgcolor="#ffffff",
        showlegend=False,                        # removes the floating legend box
        hoverlabel=HOVER_LABEL,
        height=320,
    )
    st.plotly_chart(fig, use_container_width=True, config=CHART_CFG)

# Mini breakdown stats beside the donut
with stats_col:
    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)
    total = len(filtered)
    for _, row in avail_counts.iterrows():
        pct = row["count"] / total * 100 if total else 0
        st.markdown(f"""
        <div style="background:#ffffff;border:1px solid #e8eaf0;border-radius:10px;
                    padding:14px 18px;margin-bottom:10px;">
            <div style="font-size:11px;color:#9ca3af;font-weight:600;
                        text-transform:uppercase;letter-spacing:0.04em;margin-bottom:4px;">
                {row['availability']}
            </div>
            <div style="font-size:22px;font-weight:700;color:#1a1a2e;">{row['count']:,}</div>
            <div style="font-size:12px;color:#6b7280;margin-top:2px;">{pct:.1f}% of shown books</div>
        </div>
        """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# BOOK TABLE
# ---------------------------------------------------------------------------

st.divider()
st.markdown("### 📋 Book list")

sort_c, order_c, _ = st.columns([2, 2, 4])
with sort_c:
    sort_by = st.selectbox("Sort by", ["price", "rating", "title", "stock_count"], index=0)
with order_c:
    asc = st.radio("Order", ["Ascending", "Descending"], horizontal=True) == "Ascending"

display_df = (
    filtered[["title", "price", "rating", "availability", "stock_count", "category"]]
    .sort_values(sort_by, ascending=asc)
    .reset_index(drop=True)
)
display_df.index += 1

st.dataframe(
    display_df,
    use_container_width=True,
    height=300,
    column_config={
        "price":       st.column_config.NumberColumn("Price (£)",  format="£%.2f"),
        "rating":      st.column_config.NumberColumn("Rating ★",   format="%d ★"),
        "stock_count": st.column_config.NumberColumn("In stock",   format="%d"),
    },
)


# ---------------------------------------------------------------------------
# BOOK DETAIL  — auto-suggest search (type to filter the dropdown instantly)
# ---------------------------------------------------------------------------

st.divider()
st.markdown("### 🔎 Book detail")

# Two-step approach: text input narrows the dropdown in real time.
search_col, select_col = st.columns([1, 2])

with search_col:
    book_search = st.text_input(
        "Type to search books",
        placeholder="e.g. sapiens, dark…",
        key="book_search",
        label_visibility="visible",
    )

# Filter available titles by what the user typed
all_titles = sorted(filtered["title"].dropna().unique())
if book_search:
    matched = [t for t in all_titles if book_search.lower() in t.lower()]
else:
    matched = all_titles

with select_col:
    if matched:
        selected_title = st.selectbox(
            f"Matching books ({len(matched)})",
            options=matched,
            key="book_select",
        )
    else:
        st.warning("No books match your search.")
        selected_title = None


# Render the selected book as a styled card
if selected_title:
    book = filtered[filtered["title"] == selected_title].iloc[0]
    stars_html = f'<span class="star-gold">{"★" * int(book["rating"])}{"☆" * (5 - int(book["rating"]))}</span>'
    stock_val = int(book["stock_count"]) if pd.notna(book.get("stock_count")) else "?"
    url = book.get("url", "")
    upc = book.get("upc", "")
    desc = book.get("description", "")
    avail = book.get("availability", "")
    cat  = book.get("category", "")

    st.markdown(f"""
    <div class="book-card">
        <div class="bc-title">{book['title']}</div>
        <span class="bc-cat">{cat}</span>
        <div class="bc-row">
            <div class="bc-stat">
                <div class="bc-stat-label">Price</div>
                <div class="bc-stat-value">£{book['price']:.2f}</div>
            </div>
            <div class="bc-stat">
                <div class="bc-stat-label">Rating</div>
                <div class="bc-stat-value">{stars_html}</div>
            </div>
            <div class="bc-stat">
                <div class="bc-stat-label">In stock</div>
                <div class="bc-stat-value">{stock_val}</div>
            </div>
        </div>
        <div class="bc-field"><b>Availability:</b> {avail}</div>
        <div class="bc-field"><b>UPC:</b> <span class="bc-upc">{upc}</span></div>
        <div class="bc-field"><b>URL:</b> <a href="{url}" target="_blank">{url}</a></div>
        {"<div class='bc-desc'>" + desc + "</div>" if pd.notna(desc) and desc else ""}
    </div>
    """, unsafe_allow_html=True)