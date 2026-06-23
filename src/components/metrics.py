"""Summary metrics component."""

import streamlit as st
import pandas as pd


def render_metrics(filtered: pd.DataFrame):
    """Render summary metrics."""
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Books shown", f"{len(filtered):,}")
    c2.metric(
        "Avg price",
        f"£{filtered['price'].mean():.2f}" if len(filtered) else "—",
    )
    c3.metric(
        "Avg rating",
        f"{filtered['rating'].mean():.1f} ★" if len(filtered) else "—",
    )
    c4.metric("Categories", filtered["category"].nunique())
    c5.metric(
        "In stock",
        filtered["availability"].str.contains("In stock", na=False).sum(),
    )

    st.divider()

    if filtered.empty:
        st.warning("No books match your current filters. Try widening the range.")
        return False
    return True
