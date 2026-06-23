"""Book table component."""

import streamlit as st
import pandas as pd


def render_table(filtered: pd.DataFrame):
    """Render book list table with sorting options."""
    st.divider()
    st.markdown("### 📋 Book list")

    sort_c, order_c, _ = st.columns([2, 2, 4])
    with sort_c:
        sort_by = st.selectbox(
            "Sort by", ["price", "rating", "title", "stock_count"], index=0
        )
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
            "price": st.column_config.NumberColumn("Price (£)", format="£%.2f"),
            "rating": st.column_config.NumberColumn("Rating ★", format="%d ★"),
            "stock_count": st.column_config.NumberColumn("In stock", format="%d"),
        },
    )
