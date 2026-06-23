"""
Books Dashboard - Refactored
Run with: streamlit run src/app.py
"""

import sys
from pathlib import Path

import streamlit as st

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import PAGE_CONFIG, DATA_PATH, APP_TITLE, APP_SUBTITLE
from src.styles import CUSTOM_CSS
from src.data.loader import load_data
from src.components.sidebar import FilterState
from src.components.metrics import render_metrics
from src.components.charts import (
    render_price_and_rating_charts,
    render_category_charts,
    render_scatter_chart,
    render_stock_availability,
)
from src.components.table import render_table
from src.components.detail import render_detail


def main():
    """Main application entry point."""
    # Page configuration
    st.set_page_config(**PAGE_CONFIG)

    # Apply custom CSS
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # Load data
    try:
        df = load_data(DATA_PATH)
    except FileNotFoundError:
        st.error(
            f"⚠️  `{DATA_PATH}` not found. Run `python scrape_all_books.py` first."
        )
        st.stop()

    # Render sidebar filters
    filter_state = FilterState(df)
    filters = filter_state.render()

    # Apply filters
    filtered = FilterState.apply_filters(df, filters)

    # Header
    st.markdown(f"## {APP_TITLE}")
    st.caption(APP_SUBTITLE)
    st.divider()

    # Metrics and early exit if no data
    if not render_metrics(filtered):
        st.stop()

    # Charts - Row 1
    render_price_and_rating_charts(filtered)

    # Charts - Row 2
    render_category_charts(filtered)

    # Scatter chart
    render_scatter_chart(filtered)

    # Stock availability
    render_stock_availability(filtered)

    # Table
    render_table(filtered)

    # Detail card
    render_detail(filtered)


if __name__ == "__main__":
    main()
