"""
CSS styling for the Books Dashboard.
"""

CUSTOM_CSS = """
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
"""
