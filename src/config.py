"""
Configuration and constants for the Books Dashboard.
"""

# Page Configuration
PAGE_CONFIG = {
    "page_title": "Books Dashboard",
    "page_icon": "📚",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Data Configuration
DATA_PATH = "all_books.csv"

# Plotly Chart Configuration
CHART_CFG = {
    "displayModeBar": False,
    "scrollZoom": False,
}

# Hover label styling
HOVER_LABEL = dict(
    bgcolor="white",
    bordercolor="#e8eaf0",
    font_size=13,
    font_color="#1a1a2e",
)

# Rating colors for charts
RATING_COLORS = {
    1: "#f87171",
    2: "#fb923c",
    3: "#facc15",
    4: "#4ade80",
    5: "#34d399",
}

# App metadata
APP_TITLE = "📚 Books Catalog Dashboard"
APP_SUBTITLE = "Data scraped from books.toscrape.com · BeautifulSoup Day 3"
